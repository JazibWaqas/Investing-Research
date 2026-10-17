"""Sector sensitivity to Brent, coal, urea, cotton, palm oil, PKR and KSE100 (approved spec, 17 Oct 2026).

    python scripts/tests/commodity_pkr_sensitivity.py [--method crude|adjusted] [--quick]

Writes tests/out/commodity_pkr_sensitivity.txt (raw output) and tests/out/sensitivity_map.csv.
Point in time: baskets are fixed at the formation close from liquid_universe(F); windows are (F, end] buy-and-hold.
Rerun with --method adjusted once data/corporate_actions.csv exists (prices.returns falls back to crude if absent).
"""
import argparse
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from prices import ROOT, SUSPECTS, ew_market, liquid_universe, load_panel, provisional_actions, returns  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--method", default="crude", choices=["crude", "adjusted"])
ap.add_argument("--quick", action="store_true", help="fewer placebo draws, no file output (testing only)")
ARGS = ap.parse_args()
DR_H3, DR_EV = (60, 200) if ARGS.quick else (1000, 2000)
SEED = 20261017
OUT = ROOT / "tests" / "out"
OUT.mkdir(exist_ok=True)


class Tee:
    def __init__(self, path):
        self.f, self.o = open(path, "w", encoding="utf-8"), sys.stdout

    def write(self, s):
        self.f.write(s), self.o.write(s)

    def flush(self):
        self.f.flush(), self.o.flush()


if not ARGS.quick:
    sys.stdout = Tee(OUT / "commodity_pkr_sensitivity.txt")


def H(t):
    print("\n" + "=" * 110 + f"\n{t}\n" + "=" * 110)


pc = lambda x: "   nan" if not np.isfinite(x) else f"{100 * x:6.2f}"

# ------------------------------------------------------------------ panel and returns
close, vol, tv = load_panel()
ret, gap = returns(close, ARGS.method, return_gap=True)
dates, syms = close.index, list(close.columns)
T, LAST = len(dates), len(dates) - 1
R = ret.values
CUM = np.cumsum(np.log1p(np.clip(np.nan_to_num(R), -0.999999, None)), axis=0)
OBS = np.cumsum(~np.isnan(R), axis=0)
sus = pd.read_csv(SUSPECTS, parse_dates=["date"])
FL = np.zeros(R.shape, bool)
sidx = {s: i for i, s in enumerate(syms)}
okr = sus.symbol.isin(sidx) & sus.date.isin(dates)
FL[dates.get_indexer(sus.date[okr]), [sidx[s] for s in sus.symbol[okr]]] = True
FLC = np.cumsum(FL, axis=0)
GPC = np.cumsum(np.nan_to_num(gap.values) > 5, axis=0)
KSE = pd.read_csv(ROOT / "data/macro/kse100.csv", parse_dates=["date"]).set_index("date")["close"].reindex(dates).ffill().values
print(f"method={ARGS.method}; panel {T} dates x {len(syms)} symbols, {dates[0].date()} to {dates[-1].date()}; "
      f"suspect-flagged stock-days used for dropping: {FL.sum()}")
ewm = ew_market(ret)
print(f"cross-check, ew_market (daily-rebalanced, prices.py) compounded 2017-02 to end: "
      f"{(1 + ewm[ewm.index >= '2017-02-01'].dropna()).prod() - 1:+.1%} (survivor-biased, price only)")

PER = pd.PeriodIndex(dates, freq="M")
rows_of = {}
for i, p in enumerate(PER):
    rows_of.setdefault(p, []).append(i)
first_row = {p: r[0] for p, r in rows_of.items()}
last_row = {p: r[-1] for p, r in rows_of.items()}
fifth_row = {p: r[4] for p, r in rows_of.items() if len(r) >= 5}
P = pd.Period
ROW0 = first_row[P("2017-02", "M")]   # first allowed formation


def F(p, kind="d"):
    """Formation row for signal month p: first (kind d) or 5th (kind p) PSX trading day of month p+1."""
    return (first_row if kind == "d" else fifth_row).get(p + 1)


# ------------------------------------------------------------------ baskets
sym = pd.read_csv(ROOT / "data/symbols.csv")
SEC = dict(zip(sym.symbol, sym.sectorName))
GAS = {"SNGP", "SSGC"}
DEF = {
    "E&P": ["OIL & GAS EXPLORATION COMPANIES"], "Refinery": ["REFINERY"], "OMC": ["OIL & GAS MARKETING COMPANIES"],
    "Gas utilities": [], "Fertilizer": ["FERTILIZER"], "Cement": ["CEMENT"], "Power": ["POWER GENERATION & DISTRIBUTION"],
    "Autos": ["AUTOMOBILE ASSEMBLER", "AUTOMOBILE PARTS & ACCESSORIES"], "Pharma": ["PHARMACEUTICALS"],
    "Textiles": ["TEXTILE COMPOSITE", "TEXTILE SPINNING", "TEXTILE WEAVING"], "Tech": ["TECHNOLOGY & COMMUNICATION"],
    "Chemicals": ["CHEMICAL"], "Food": ["FOOD & PERSONAL CARE PRODUCTS", "VANASPATI & ALLIED INDUSTRIES"],
    "Banks": ["COMMERCIAL BANKS"], "Steel/engineering": ["ENGINEERING"],
    "Glass/packaging": ["GLASS & CERAMICS", "PAPER, BOARD & PACKAGING"]}
SECTORS = list(DEF)
GIDX = {}
for g, secs in DEF.items():
    names = [s for s in syms if SEC.get(s) in secs]
    if g == "OMC":
        names = [s for s in names if s not in GAS]
    GIDX[g] = np.array([sidx[s] for s in names], int)
GIDX["Gas utilities"] = np.array([sidx[s] for s in sorted(GAS) if s in sidx], int)
TECH_OUT = ["PTC", "TELE", "WTL", "AIRLINK"]   # name-picked: telecom operators / hardware assembler (classification unverified)
GIDX["Tech-lite"] = np.array([i for i in GIDX["Tech"] if syms[i] not in TECH_OUT], int)
GIDX["Exporters"] = np.concatenate([GIDX["Textiles"], GIDX["Tech"]])
GIDX["Exporters-lite"] = np.concatenate([GIDX["Textiles"], GIDX["Tech-lite"]])
GIDX["Importers"] = np.concatenate([GIDX["Autos"], GIDX["Pharma"]])
GIDX["Market"] = np.arange(len(syms))
print("Tech name-picked robustness excludes (those in panel):", [s for s in TECH_OUT if s in sidx])
print("Symbols in panel by basket (all years, liquid or not):", {g: len(i) for g, i in GIDX.items() if g in SECTORS})


@lru_cache(None)
def liq(row):
    u = set(liquid_universe(dates[row]))
    return np.array([s in u for s in syms])


@lru_cache(None)
def window(s, e):
    """Per basket: (return, n liquid, n valid, dropped for flag, dropped for gap, dropped for no obs) over (s, e]."""
    lm = liq(s)
    wr = np.expm1(CUM[e] - CUM[s])
    fl, gp, nb = (FLC[e] - FLC[s]) > 0, (GPC[e] - GPC[s]) > 0, (OBS[e] - OBS[s]) == 0
    okm = lm & ~fl & ~gp & ~nb
    out = {}
    for g, ix in GIDX.items():
        k = okm[ix]
        out[g] = (wr[ix][k].mean() if k.sum() >= 2 else np.nan, int(lm[ix].sum()), int(k.sum()),
                  int((lm & fl)[ix].sum()), int((lm & ~fl & gp)[ix].sum()), int((lm & ~fl & ~gp & nb)[ix].sum()))
    return out


def raw(g, s, e):
    return np.nan if s is None or e is None or e > LAST or s < ROW0 else window(s, e)[g][0]


def ex(g, s, e):
    return raw(g, s, e) - raw("Market", s, e)


def kse_ex(g, s, e):
    r = raw(g, s, e)
    return np.log1p(r) - np.log(KSE[e] / KSE[s]) if np.isfinite(r) else np.nan


def members(g, s, e):
    okm = liq(s) & ~((FLC[e] - FLC[s]) > 0) & ~((GPC[e] - GPC[s]) > 0) & ((OBS[e] - OBS[s]) > 0)
    return [syms[i] for i in GIDX[g] if okm[i]]


try:
    ACT = provisional_actions()
    ACT = ACT[ACT.type.isin(["bonus", "cash"])]
except Exception as exn:   # noqa: BLE001
    ACT = pd.DataFrame(columns=["symbol", "ex_date", "type", "value"])
    print("provisional_actions failed:", exn)
SMALL = ["E&P", "Refinery", "Fertilizer", "Gas utilities"]


def exdates(groups, s, e):
    e = min(e, LAST)
    out = []
    for g in groups:
        ms = [syms[i] for i in GIDX[g] if liq(s)[i]]
        a = ACT[ACT.symbol.isin(ms) & (ACT.ex_date > dates[s]) & (ACT.ex_date <= dates[e])]
        out += [f"{r.symbol} {r.type} {r.ex_date.date()}" for r in a.itertuples()]
    return "; ".join(out) if out else "none found"


# ------------------------------------------------------------------ factors
def month_end(path, col="value"):
    s = pd.read_csv(ROOT / "data/macro" / path, parse_dates=["date"]).set_index("date")[col].dropna()
    g = s.groupby(s.index.to_period("M")).last()
    return g.reindex(pd.period_range(g.index[0], "2026-09", freq="M")).ffill()


def pink(path):
    s = pd.read_csv(ROOT / "data/macro" / path, parse_dates=["date"]).set_index("date")["value"]
    s.index = s.index.to_period("M")
    return s


BRENT, PKR, KSEM = month_end("brent.csv"), month_end("usdpkr.csv"), month_end("kse100.csv", "close")
FAC = {"brent": np.log(BRENT).diff(), "coal": np.log(pink("coal_rb.csv")).diff(), "urea": np.log(pink("urea.csv")).diff(),
       "cotton": np.log(pink("cotton.csv")).diff(), "palm": np.log(pink("palm_oil.csv")).diff(),
       "pkr": np.log(PKR).diff(), "kse100": np.log(KSEM).diff()}
FAC["palm"][P("2026-01", "M")] = np.nan
FAC["urea"][P("2022-03", "M")] = np.nan
FKIND = {"brent": "d", "pkr": "d", "kse100": "d", "coal": "p", "urea": "p", "cotton": "p", "palm": "p"}
SCALE = {"pkr": 0.05}   # per +5% depreciation; everything else per +10% log move
GRID = pd.period_range("2017-01", "2026-09", freq="M")
TG = len(GRID)
XS = {f: s.reindex(GRID).values for f, s in FAC.items()}
print(f"\nFactor months {GRID[0]} to {GRID[-1]} (T={TG}); NaN changes: palm 2026-01, urea 2022-03; "
      f"usdpkr last obs {pd.read_csv(ROOT/'data/macro/usdpkr.csv').date.iloc[-1]} (no PKR signal for 2026-10); "
      f"brent last obs {pd.read_csv(ROOT/'data/macro/brent.csv').date.iloc[-1]}")
print("Pink Sheet monthly AVERAGES: F(t)=5th PSX trading day of month t+1 (release timing ASSUMED, not recorded). "
      "Richards Bay coal has World Bank estimates for some 2022-24 months.")

# ------------------------------------------------------------------ section 3: coverage
H("SECTION 3  BASKET COVERAGE (monthly windows, first PSX day of month u to first day of u+1, u = 2017-02 .. 2026-09)")
cov = []
UM = pd.period_range("2017-02", "2026-09", freq="M")
for g in SECTORS + ["Tech-lite", "Exporters", "Importers"]:
    n_l, bask, d = [], 0, np.zeros(3, int)
    for u in UM:
        w = window(first_row[u], first_row[u + 1])[g]
        n_l.append(w[1])
        bask += np.isfinite(w[0])
        d += w[3:]
    w0 = window(first_row[UM[0]], first_row[UM[0] + 1])[g]
    w1 = window(first_row[UM[-1]], first_row[UM[-1] + 1])[g]
    cov.append((g, bask, int(np.median(n_l)), min(n_l), w0[1], w1[1], *d))
print(f"months in sample = {len(UM)}")
print(pd.DataFrame(cov, columns=["basket", "months_with_basket", "median_liquid_n", "min_liquid_n", "n_2017-02", "n_2026-09",
                                 "drop_suspect_flag", "drop_gap>5", "drop_no_obs"]).to_string(index=False))
print("E&P, Refinery, Fertilizer and Gas utilities are close to single-stock bets; one unflagged sub-threshold bonus can move a window by 3-5 pts.")


# ------------------------------------------------------------------ statistics helpers
def stats(v):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    return (len(v), v.mean(), np.median(v), (v > 0).mean(), v.min()) if len(v) else (0, np.nan, np.nan, np.nan, np.nan)


RNG = np.random.default_rng(SEED)


def placebo(pool, n, actual_median):
    pool = np.asarray(pool, float)
    pool = pool[np.isfinite(pool)]
    if n == 0 or len(pool) < n + 1:
        return None
    V = pool[np.argsort(RNG.random((DR_EV, len(pool))), axis=1)[:, :n]]
    md = np.median(V, 1)
    return dict(pm=np.median(V.mean(1)), pmed=np.median(md), pw=np.median((V > 0).mean(1)),
                lo=np.percentile(md, 5), hi=np.percentile(md, 95), pct=100 * (md <= actual_median).mean())


HDR = (f"{'row':44s} {'n':>3s} {'eps':>3s} | {'mean':>6s} {'median':>6s} {'win%':>5s} {'worst':>6s} | {'netmean':>7s} {'netmed':>6s} {'netwin':>6s} | "
       f"{'plc_mean':>8s} {'plc_med':>7s} {'plc_win':>7s} {'plc5-95 of median':>19s} {'pctile':>6s}")
RES = {}


def trow(label, vals, pool, cost=0.0, eps=None, key=None):
    """Print one results row (all in % points). vals/pool = gross excess; net = gross - cost. The placebo is on the series
    judged (net if cost else gross): same n random entries from `pool`. pctile = share of placebo medians <= actual median."""
    v = np.asarray(vals, float)
    v = v[np.isfinite(v)]
    n, mean, med, win, worst = stats(v)
    nn = stats(v - cost) if cost else None
    judged = v - cost
    jm = np.median(judged) if n else np.nan
    pl = placebo(np.asarray(pool, float) - cost, n, jm) if n else None
    s = f"{label:44.44s} {n:3d} {('-' if eps is None else eps):>3} | {pc(mean)} {pc(med)} {100*win if n else np.nan:5.0f} {pc(worst)} | "
    s += f"{pc(nn[1])}  {pc(nn[2])} {100*nn[3]:6.0f} | " if nn else f"{'-':>7s} {'-':>6s} {'-':>6s} | "
    s += (f"{pc(pl['pm']):>8s} {pc(pl['pmed']):>7s} {100*pl['pw']:7.0f} {pc(pl['lo'])}..{pc(pl['hi'])}   {pl['pct']:5.0f}" if pl else "placebo n/a")
    print(s)
    r = dict(n=n, mean=mean, med=med, win=win, worst=worst, jmed=jm, jpos=(judged > 0).mean() if n else np.nan, pl=pl)
    if key:
        RES[key] = r
    return r


# ------------------------------------------------------------------ H3 regressions
H("SECTION 4  H3  MONTHLY REGRESSIONS (sector excess on factor change; HAC maxlags=3; non-overlapping 1-month windows)")
SPEC = {0: "c", 1: "k1", 2: "k2", 3: "k3"}
Y, YRAW = {}, {}
ALLG = SECTORS + ["Tech-lite"]
for g in ALLG:
    YRAW[g] = np.full(TG, np.nan)
    for key in ["c"] + [f"k{k}{kd}" for k in (1, 2, 3) for kd in "dp"]:
        Y[(g, key)] = np.full(TG, np.nan)
for ti, t in enumerate(GRID):
    s, e = last_row.get(t - 1), last_row.get(t)
    for g in ALLG:
        if s is not None and e is not None and s >= ROW0:
            Y[(g, "c")][ti] = ex(g, s, e)
            YRAW[g][ti] = raw(g, s, e)
        for kind in "dp":
            for k in (1, 2, 3):
                s2, e2 = F(t + k - 1, kind), F(t + k, kind)
                if s2 is not None and e2 is not None:
                    Y[(g, f"k{k}{kind}")][ti] = ex(g, s2, e2)


def ykey(spec, fac):
    return "c" if spec == 0 else f"k{spec}{FKIND[fac]}"


def yvec(g, spec, fac):
    return YRAW[g] if (fac == "kse100" and spec == 0) else Y[(g, ykey(spec, fac))]


def ols_np(y, x, L=3):
    m = np.isfinite(y) & np.isfinite(x)
    y, x, n = y[m], x[m], int(m.sum())
    if n < 20:
        return np.nan, np.nan, np.nan, n
    X = np.column_stack([np.ones(n), x])
    A = np.linalg.inv(X.T @ X)
    b = A @ X.T @ y
    u = y - X @ b
    Xu = X * u[:, None]
    S = Xu.T @ Xu
    for j in range(1, L + 1):
        G = Xu[j:].T @ Xu[:-j]
        S += (1 - j / (L + 1)) * (G + G.T)
    V = A @ S @ A
    return b[1], b[1] / np.sqrt(V[1, 1]), 1 - u @ u / ((y - y.mean()) @ (y - y.mean())), n


def ols_sm(y, x):
    m = np.isfinite(y) & np.isfinite(x)
    r = sm.OLS(y[m], sm.add_constant(x[m])).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    return r.params[1], r.tvalues[1], r.rsquared, int(m.sum())


PRE = {("E&P", "brent"): 1, ("E&P", "pkr"): 1, ("Refinery", "brent"): 1, ("OMC", "brent"): 1, ("Cement", "coal"): -1,
       ("Textiles", "cotton"): -1, ("Textiles", "pkr"): 1, ("Tech", "pkr"): 1, ("Autos", "pkr"): -1, ("Pharma", "pkr"): -1,
       ("Food", "palm"): -1, ("Fertilizer", "urea"): 1}
CELLS = [(g, f, sp) for f in FAC for g in SECTORS for sp in range(4)]
ACT_RES, maxdiff = {}, 0.0
for g, f, sp in CELLS:
    a, b = ols_sm(yvec(g, sp, f), XS[f]), ols_np(yvec(g, sp, f), XS[f])
    ACT_RES[(g, f, sp)] = a
    if np.isfinite(a[1]):
        maxdiff = max(maxdiff, abs(a[1] - b[1]), abs(a[0] - b[0]))
print(f"{len(CELLS)} cells; numpy Newey-West vs statsmodels HAC(maxlags=3): max abs difference in beta/t = {maxdiff:.2e}")
assert maxdiff < 1e-6

OFFS = RNG.integers(12, TG - 12 + 1, DR_H3)
TD = np.full((DR_H3, len(CELLS)), np.nan)
for d, off in enumerate(OFFS):
    xs = {f: np.roll(x, off) for f, x in XS.items()}
    for ci, (g, f, sp) in enumerate(CELLS):
        TD[d, ci] = ols_np(yvec(g, sp, f), xs[f])[1]
tact = np.array([ACT_RES[c][1] for c in CELLS])
PP = {c: (np.mean(np.abs(TD[:, i]) >= abs(tact[i])) if np.isfinite(tact[i]) else np.nan) for i, c in enumerate(CELLS)}


def scaled(f, sp, beta):
    if f == "kse100" and sp == 0:
        return beta               # raw market beta
    return beta * SCALE.get(f, 0.10) * 100   # pts of monthly excess return per +10% (PKR +5%) log move


print(f"\nCircular-shift placebo: {DR_H3} draws, one random offset in [12, {TG-12}] months per draw applied to all 7 factors.")
rows = []
for (g, f, sp), pv in PP.items():
    be, t, r2, n = ACT_RES[(g, f, sp)]
    pre = PRE.get((g, f))
    if pre and pv < 0.05:
        flag = "SUPPORTED" if np.sign(be) == pre else "pre-registered, placebo-significant but OPPOSITE sign"
    elif pre:
        flag = "pre-registered, not supported"
    else:
        flag = "exploratory, needs out-of-sample check" if pv < 0.05 else ""
    rows.append(dict(sector=g, factor=f, spec=("contemporaneous" if sp == 0 else f"lead k={sp}"), prior=("" if not pre else "+" if pre > 0 else "-"),
                     beta=scaled(f, sp, be), t=t, n=n, r2=r2, placebo_p=pv, flag=flag))
CT = pd.DataFrame(rows)
FMT = lambda x: f"{x:.3f}"
print("\nbeta units: pts of monthly sector excess return per +10% factor log move (PKR per +5%; KSE100 contemporaneous = raw beta of sector return)")
print(CT.to_string(index=False, float_format=FMT))

cnt_act = int((np.abs(tact) >= 2).sum())
cnt_pl = (np.abs(TD) >= 2).sum(axis=1)
print(f"\nMULTIPLE TESTING: actual |t|>=2 cells = {cnt_act} of {int(np.isfinite(tact).sum())}; placebo median = {np.median(cnt_pl):.0f}, "
      f"95th percentile = {np.percentile(cnt_pl, 95):.0f}, share of draws >= actual = {np.mean(cnt_pl >= cnt_act):.3f}")
for sp in range(4):
    ix = [i for i, c in enumerate(CELLS) if c[2] == sp]
    cp = (np.abs(TD[:, ix]) >= 2).sum(1)
    print(f"   spec {SPEC[sp]}: actual {(np.abs(tact[ix]) >= 2).sum()} of {len(ix)}; placebo median {np.median(cp):.0f}, p95 {np.percentile(cp, 95):.0f}")
nk = [i for i, c in enumerate(CELLS) if c[1] != "kse100"]
cpk = (np.abs(TD[:, nk]) >= 2).sum(1)
print(f"   excluding the KSE100 factor (its contemporaneous cells are market betas): actual {(np.abs(tact[nk]) >= 2).sum()} of {len(nk)}; "
      f"placebo median {np.median(cpk):.0f}, p95 {np.percentile(cpk, 95):.0f}")
print("\nSUPPORTED pre-registered cells (placebo p<0.05 and sign matches prior):")
s_ = CT[CT.flag == "SUPPORTED"]
print(s_.to_string(index=False, float_format=FMT) if len(s_) else "none")
print("\nPre-registered cells, all specs:")
print(CT[CT.prior != ""].to_string(index=False, float_format=FMT))
print("\nSignificant exploratory cells (placebo p<0.05, not pre-registered): exploratory, needs out-of-sample check")
print(CT[CT.flag.str.startswith("exploratory")].to_string(index=False, float_format=FMT))

mp = []
for f in FAC:
    for g in SECTORS:
        q = CT[(CT.sector == g) & (CT.factor == f)]
        r0, r1 = q[q.spec == "contemporaneous"].iloc[0], q[q.spec == "lead k=1"].iloc[0]
        st = [r0.flag, r1.flag]
        status = "supported" if "SUPPORTED" in st else ("exploratory" if any(s.startswith("exploratory") or "OPPOSITE" in s for s in st) else "none")
        unit = ("raw beta (contemp.); pts per +10% (lead)" if f == "kse100" else "pts monthly excess per +5% PKR depreciation" if f == "pkr"
                else "pts monthly excess per +10% factor log move")
        mp.append(dict(sector=g, factor=f, unit=unit, prior=r0.prior, contemp_beta=r0.beta, contemp_t=r0.t, contemp_placebo_p=r0.placebo_p,
                       contemp_n=r0.n, contemp_r2=r0.r2, k1_beta=r1.beta, k1_t=r1.t, k1_placebo_p=r1.placebo_p, k1_n=r1.n, k1_r2=r1.r2,
                       status_contemp=r0.flag, status_k1=r1.flag, status=status))
if not ARGS.quick:
    pd.DataFrame(mp).to_csv(OUT / "sensitivity_map.csv", index=False, float_format="%.4f")
    print(f"\nwrote {OUT / 'sensitivity_map.csv'} ({len(mp)} rows)")

print("\nROBUSTNESS (name-picked, labelled): Tech vs Tech-lite (excluding", TECH_OUT, ") on PKR; beta pts per +5% depreciation")
for g in ("Tech", "Tech-lite"):
    for sp in range(4):
        y = Y[(g, ykey(sp, "pkr"))]
        be, t, r2, n = ols_sm(y, XS["pkr"])
        tt = np.array([ols_np(y, np.roll(XS["pkr"], o))[1] for o in OFFS])
        print(f"   {g:10s} {SPEC[sp]:3s} beta {be*5:7.3f} pts/+5%  NW t {t:6.2f}  n {n}  placebo p {np.mean(np.abs(tt) >= abs(t)):.3f}")

# ------------------------------------------------------------------ H1
H("SECTION 5  H1  BRENT 3-MONTH RISE >= 20%")
b3 = BRENT / BRENT.shift(3) - 1
sig = b3 >= 0.20
onsets = [t for i, t in enumerate(sig.index) if i >= 3 and sig.iloc[i] and not sig.iloc[i - 3:i].any()]
print("Signal months (all, from data):", [str(t) for t in sig.index[sig]])
print("Episode onsets (first signal month after >=3 non-signal months):", [str(t) for t in onsets])
keep = [t for t in onsets if F(t) is not None and F(t) >= ROW0]
print("Kept (formation on/after 2017-02-01):", [str(t) for t in keep], "| dropped as pre-sample:", [str(t) for t in onsets if t not in keep])
print("2020-06 is a rebound off the COVID crash; 2026-03 is in-sample (the hypothesis came from the 2026 refiner setup).")
H1G, KS = ["Refinery", "E&P"], (1, 2, 3)
print("\nPer-episode table (excess vs same-universe EW market, % points; net = gross - 0.5)")
print(f"{'onset':8s} {'Brent3m':>8s} {'sector':9s} " + " ".join(f"{'k'+str(k)+' gross':>9s} {'k'+str(k)+' net':>7s}" for k in KS) + "  members / ex-dates in window (3m)")
for t in keep:
    s = F(t)
    for g in H1G:
        vals = []
        for k in KS:
            v = ex(g, s, F(t + k))
            vals.append(f"{pc(v):>9s} {pc(v - 0.005):>7s}")
        e3 = min(F(t + 3) or LAST, LAST)
        print(f"{str(t):8s} {100*b3[t]:7.1f}% {g:9s} " + " ".join(vals) + f"  {members(g, s, e3)} | {exdates([g], s, e3)}")
print("\nPENDING (window ends after 2026-10-16; excluded from every statistic):")
for t in keep:
    for k in KS:
        e = F(t + k)
        if e is None or e > LAST:
            s = F(t)
            print(f"   onset {t} horizon {k}m: entry {dates[s].date()}, {LAST - s} trading days elapsed, gross excess so far "
                  + ", ".join(f"{g} {pc(ex(g, s, LAST))}%" for g in H1G))


def mpool(g, k=None, before=None, h=None):
    """Excess for entries on the first PSX day of every month u (2017-02 on), horizon k months or h trading days."""
    out = []
    for u in pd.period_range("2017-02", "2026-10", freq="M"):
        if before and u.year >= before:
            continue
        s = first_row[u]
        e = first_row.get(u + k) if h is None else s + h
        if e is not None and e <= LAST:
            out.append(ex(g, s, e))
    return np.array(out)


print("\nH1 summary. Headline = first month of each episode (non-overlapping). Placebo = same n random month-start entries, same names/period,"
      " net of 0.5; pctile = share of placebo medians at or below the actual median.")
print(HDR)
SAMPS = [("full", lambda t: True), ("excl 2026", lambda t: t.year < 2026),
         ("excl 2026 & 2020-06", lambda t: t.year < 2026 and t != P("2020-06", "M"))]
for samp, filt in SAMPS:
    for g in H1G:
        for k in KS:
            vals = [ex(g, F(t), F(t + k)) for t in keep if filt(t)]
            trow(f"H1 {g} {k}m [{samp}]", vals, mpool(g, k, before=2026 if samp != "full" else None), 0.005,
                 eps=int(np.isfinite(vals).sum()), key=("H1", g, k, samp))
    print()
print("Verdict per cell (rule: median net >= placebo p95 of median, >=2/3 episodes positive net, survives excl. 2026):")
allok = True
for g in H1G:
    for k in KS:
        c = []
        for samp in ("full", "excl 2026"):
            r = RES[("H1", g, k, samp)]
            c.append(bool(r["pl"] is not None and r["jmed"] >= r["pl"]["hi"] and r["jpos"] >= 2 / 3))
        fr = RES[("H1", g, k, "full")]
        bad = fr["pl"] is not None and (fr["jmed"] <= fr["pl"]["pmed"] or fr["jpos"] < 0.5)
        v = "supported" if all(c) else ("not supported" if bad else f"inconclusive, n episodes = {fr['n']}")
        allok &= all(c)
        print(f"   {g:9s} {k}m: full pass={c[0]}, excl-2026 pass={c[1]} -> {v}")
print("   H1 overall:", "supported" if allok else "not supported or inconclusive (low power)")

print("\nSecondary: ALL signal months (OVERLAPPING 3m rises, not headline), net of 0.5:")
print(HDR)
smo = [t for t in sig.index[sig] if F(t) is not None and F(t) >= ROW0]
for g in H1G:
    for k in KS:
        trow(f"H1 {g} {k}m [all signal months]", [ex(g, F(t), F(t + k)) for t in smo], mpool(g, k), 0.005, eps=len(keep))
print("\nSecondary: every signal month as 0/1 dummy; y = 1-month excess F(t)->F(t+1); HAC(3); beta in pts:")
D = sig.reindex(GRID).astype(float).values
for g in H1G:
    be, t_, r2, n = ols_sm(Y[(g, "k1d")], D)
    nsig = int(np.nansum(D[np.isfinite(Y[(g, 'k1d')])]))
    print(f"   {g:9s} beta {100*be:6.2f} pts, NW t {t_:5.2f}, n {n}, signal months in sample {nsig}")
print("\nRobustness: excess vs KSE100 (log sector return minus KSE100 log change), headline onsets, gross:")
print(HDR)


def kpool(g, k=None, h=None):
    out = []
    for u in UM:
        s = first_row[u]
        e = first_row.get(u + k) if h is None else s + h
        if e is not None and e <= LAST:
            out.append(kse_ex(g, s, e))
    return np.array(out)


for g in H1G:
    for k in KS:
        vals = [kse_ex(g, F(t), F(t + k)) if F(t + k) is not None and F(t + k) <= LAST else np.nan for t in keep]
        trow(f"H1 {g} {k}m vs KSE100 [full]", vals, kpool(g, k), 0.0, eps=int(np.isfinite(vals).sum()))

# ------------------------------------------------------------------ H2
H("SECTION 6  H2  PKR DEVALUATION: EXPORTERS (textiles + tech) MINUS IMPORTERS (autos + pharma)")
pk = pd.read_csv(ROOT / "data/macro/usdpkr.csv", parse_dates=["date"]).set_index("date")["value"]
l20 = np.log(pk / pk.shift(20))
cross = (l20 >= 0.04) & ~(l20.shift(1) >= 0.04)
trig, last_en = [], -10**9
for d in cross.index[cross]:
    if d < dates[0]:
        trig.append((d, None, "pre-panel, dropped"))
        continue
    en = int(dates.searchsorted(d, side="right"))
    if en >= T:
        trig.append((d, None, "no PSX day after signal"))
        continue
    if en < last_en + 60:
        continue   # lockout
    last_en = en
    trig.append((d, en, "ok" if en >= ROW0 else "pre-2017-02, dropped"))
TR = [(d, en) for d, en, st in trig if st == "ok"]
ENT = [en for _, en in TR]
print("Trigger = first day the trailing 20-row log change of USDPKR crosses up through 4%; 60-trading-day lockout; entry = next PSX close.")
for d, en, st in trig:
    print(f"   signal {d.date()}  20d change {100*l20[d]:5.2f}%  entry {str(dates[en].date()) if en is not None else '-':10}  {st}")
ep, cur = [], []
for d, en in TR:
    if cur and en - cur[-1][1] >= 120:
        ep.append(cur)
        cur = []
    cur.append((d, en))
ep.append(cur)
H2EP = [[x[1] for x in e] for e in ep]
print(f"\nn triggers (in sample) = {len(TR)}; macro episodes (merge triggers <120 trading days apart) = {len(ep)}:")
for e in ep:
    print("   ", [str(d.date()) for d, _ in e])

FN = {"spread": lambda s, e: raw("Exporters", s, e) - raw("Importers", s, e),
      "spread-lite": lambda s, e: raw("Exporters-lite", s, e) - raw("Importers", s, e),
      "exp-mkt": lambda s, e: ex("Exporters", s, e), "Textiles": lambda s, e: ex("Textiles", s, e),
      "Tech": lambda s, e: ex("Tech", s, e), "Autos": lambda s, e: ex("Autos", s, e), "Pharma": lambda s, e: ex("Pharma", s, e)}
COST = {"spread": 0.01, "spread-lite": 0.01}
SHOW = ["spread", "exp-mkt", "Textiles", "Tech", "Autos", "Pharma"]


def h2v(h, entries):
    return {k: np.array([f(s, s + h) if s + h <= LAST else np.nan for s in entries]) for k, f in FN.items()}


def h2pool(h, lbl, rows_):
    return np.array([FN[lbl](s, s + h) for s in rows_ if s + h <= LAST])


ALLROWS = list(range(ROW0, LAST))
MROWS = [first_row[u] for u in pd.period_range("2017-02", "2026-10", freq="M")]
print("\nPer-trigger table (gross, % points). Pending windows are listed below and excluded.")
print(f"{'entry':11s} {'h':>3s} " + " ".join(f"{k:>9s}" for k in SHOW))
for d, en in TR:
    for h in (20, 60):
        if en + h <= LAST:
            v = h2v(h, [en])
            print(f"{dates[en].date()!s:11s} {h:3d} " + " ".join(f"{pc(v[k][0]):>9s}" for k in SHOW))
print("PENDING H2 triggers:")
pend = False
for d, en in TR:
    for h in (20, 60):
        if en + h > LAST:
            pend = True
            v = h2v(LAST - en, [en])
            print(f"   entry {dates[en].date()} horizon {h}d: {LAST - en} days elapsed; so far spread {pc(v['spread'][0])}%, exp-mkt {pc(v['exp-mkt'][0])}% (gross)")
if not pend:
    print("   none")
print("Small-basket ex-dates: the H2 baskets (textiles, tech, autos, pharma) are not 2-3 name baskets; none listed.")

print("\nH2 headline: n = triggers, eps = macro episodes represented. Costs: spread 1.0, others 0.5. Placebo = same n random trading-day entries.")
print(HDR)
EPV = {}
for h in (20, 60):
    v = h2v(h, ENT)
    for lbl in SHOW + ["spread-lite"]:
        ok_ = [np.isfinite(x) for x in v[lbl]]
        okent = {en for en, o in zip(ENT, ok_) if o}
        nep = sum(1 for e in H2EP if any(x in okent for x in e))
        trow(f"H2 {lbl} {h}d [triggers]", v[lbl], h2pool(h, lbl, ALLROWS), COST.get(lbl, 0.005), eps=nep, key=("H2", lbl, h))
    for lbl in ("spread", "exp-mkt"):
        epv = []
        for e in H2EP:
            xs_ = [v[lbl][ENT.index(x)] for x in e]
            xs_ = [x for x in xs_ if np.isfinite(x)]
            if xs_:
                epv.append(np.mean(xs_) - COST.get(lbl, 0.005))
        EPV[(lbl, h)] = epv
        r = stats(np.array(epv))
        print(f"   episode-level {lbl} {h}d net: episodes {r[0]}, mean {pc(r[1])}, median {pc(r[2])}, positive {100*r[3]:.0f}%, worst {pc(r[4])}  values {[round(float(100*x), 2) for x in epv]}")
    print()
print("H2 verdict (rule: actual median net >= placebo p95 of median, >=2/3 macro episodes positive net):")
for h in (20, 60):
    r, epv = RES[("H2", "spread", h)], EPV[("spread", h)]
    pos = float(np.mean(np.array(epv) > 0)) if epv else np.nan
    okp = bool(r["pl"] and r["jmed"] >= r["pl"]["hi"])
    bad = bool(r["pl"] and (r["jmed"] <= r["pl"]["pmed"] or pos < 0.5))
    print(f"   {h}d: median net {pc(r['jmed'])} vs placebo p95 {pc(r['pl']['hi']) if r['pl'] else 'n/a'} -> {okp}; macro episodes positive net {100*pos:.0f}% of {len(epv)} -> "
          f"{'supported' if okp and pos >= 2/3 else 'not supported' if bad else 'inconclusive, n episodes = ' + str(len(epv))}")

print("\nLens: 5 largest calendar-month PKR depreciations, de-clustered (>=3 months between picks), entry first PSX day of next month.")
m_ = FAC["pkr"].reindex(GRID).dropna().sort_values(ascending=False)
picks = []
for t, v in m_.items():
    if all(abs((t - q).n) >= 3 for q, _ in picks):
        picks.append((t, v))
    if len(picks) == 5:
        break
print("   picks:", [(str(t), f"{100*v:.2f}%") for t, v in picks], "| expected 2023-01, 2022-07, 2019-06, 2020-03, 2018-10")
print("   2020-03 is COVID-confounded (global risk-off, emergency rate cuts).")
LE = [F(t) for t, _ in picks]
print(f"{'month':8s} {'entry':11s} {'h':>3s} " + " ".join(f"{k:>9s}" for k in SHOW))
for (t, _), s in zip(picks, LE):
    for h in (20, 60):
        if s + h <= LAST:
            v = h2v(h, [s])
            print(f"{str(t):8s} {dates[s].date()!s:11s} {h:3d} " + " ".join(f"{pc(v[k][0]):>9s}" for k in SHOW))
print(HDR)
for h in (20, 60):
    v = h2v(h, LE)
    for lbl in SHOW:
        trow(f"H2 lens {lbl} {h}d", v[lbl], h2pool(h, lbl, MROWS), COST.get(lbl, 0.005), eps=len(picks))
    keep2 = np.array([t.year != 2020 for t, _ in picks])
    trow(f"H2 lens spread {h}d excl 2020-03", v["spread"][keep2], h2pool(h, "spread", MROWS), 0.01, eps=int(keep2.sum()))

print("\nRobustness: triggers excluding entries in 2020 (COVID), spread net of 1.0:")
print(HDR)
for h in (20, 60):
    v = h2v(h, [en for d, en in TR if dates[en].year != 2020])
    trow(f"H2 spread {h}d excl 2020", v["spread"], h2pool(h, "spread", ALLROWS), 0.01, eps=len(v["spread"]))
print("\nRobustness (name-picked Tech-lite in exporters): rows 'spread-lite' above. Tech excluded:", TECH_OUT)
print("\nRobustness: exporters / importers vs KSE100 (log sector return minus KSE100 log change), triggers, gross:")
print(HDR)
for h in (20, 60):
    for g in ("Exporters", "Importers"):
        vals = [kse_ex(g, en, en + h) if en + h <= LAST else np.nan for en in ENT]
        pool = np.array([kse_ex(g, s, s + h) for s in ALLROWS if s + h <= LAST])
        trow(f"H2 {g} {h}d vs KSE100", vals, pool, 0.0, eps=None)

# ------------------------------------------------------------------ section 7
H("SECTION 7  TOP BRENT MONTHS EVENT STUDY (de-clustered, ex post ranking; NOT tradable)")
bm = FAC["brent"].reindex(GRID).dropna()


def greedy(series, n, asc):
    out = []
    for t, v in series.sort_values(ascending=asc).items():
        if all(abs((t - q).n) >= 3 for q, _ in out):
            out.append((t, v))
        if len(out) == n:
            break
    return sorted(out)


UP, DN = greedy(bm, 10, False), greedy(bm, 10, True)
rebound = lambda t: any(0 <= (t - q).n <= 3 for q, _ in DN)
allp = sorted([(t, "up", v) for t, v in UP] + [(t, "down", v) for t, v in DN])
epi = 1 + sum((allp[i][0] - allp[i - 1][0]).n >= 6 for i in range(1, len(allp)))
print("(Brent monthly changes below are LOG changes)")
print("UP picks:  ", [(str(t), f"{100*v:+.1f}%", "REBOUND" if rebound(t) else "") for t, v in UP])
print("DOWN picks:", [(str(t), f"{100*v:+.1f}%") for t, v in DN])
print(f"n picks = {len(allp)}; episodes (all picks chronologically merged if <6 months apart) = {epi}; up-picks flagged rebound = "
      f"{sum(rebound(t) for t, _ in UP)} (rebound = a down pick in the 3 months up to and including the up month)")
print("These events SHARE episodes with H1 and with the H3 regressions (2020, 2022, 2026): they are NOT independent confirmations.")
for h in (20, 60):
    print(f"\nPer-event sector excess at {h} trading days (% points, gross); PENDING events excluded")
    print(f"{'dir':4s} {'month':8s} {'entry':11s} " + " ".join(f"{g[:7]:>7s}" for g in SECTORS))
    for t, dr, _ in allp:
        s = F(t)
        if s + h > LAST:
            print(f"{dr:4s} {str(t):8s} {dates[s].date()!s:11s} PENDING: {LAST - s} days elapsed; excess so far " + ", ".join(f"{g} {pc(ex(g, s, LAST))}" for g in ("Refinery", "E&P", "OMC")))
            continue
        print(f"{dr:4s} {str(t):8s} {dates[s].date()!s:11s} " + " ".join(f"{pc(ex(g, s, s + h)):>7s}" for g in SECTORS))
    print(f"\nSmall-basket ex-dates (bonus/cash; provisional table, ~2024-26 only) inside the {h}d windows:")
    for t, dr, _ in allp:
        s = F(t)
        x = exdates(SMALL, s, s + h)
        print(f"   {dr:4s} {t}: {x}")
    print(f"\nSector excess summary at {h} days. n = complete events; placebo = same n random month-start entries, same baskets, gross:")
    print(HDR)
    for dr, L in (("up", UP), ("down", DN)):
        for g in SECTORS:
            vals = [ex(g, F(t), F(t) + h) if F(t) + h <= LAST else np.nan for t, _ in L]
            trow(f"Brent {dr} {g} {h}d", vals, mpool(g, h=h), 0.0)
    print("   Up picks excluding rebounds:")
    for g in ("Refinery", "E&P", "OMC"):
        vals = [ex(g, F(t), F(t) + h) if F(t) + h <= LAST else np.nan for t, _ in UP if not rebound(t)]
        trow(f"Brent up-nonrebound {g} {h}d", vals, mpool(g, h=h), 0.0)

H("SECTION 9  DATA HANDLING NOTES")
print(f"method={ARGS.method}. data/corporate_actions.csv present: {(ROOT/'data/corporate_actions.csv').exists()} (prices.returns falls back to crude if absent).")
print("Returns are price-only; the crude method zeroes large ex-dividend drops and keeps small ones, so high-yield sectors (E&P, fertilizer, power, OMC) are understated. Dividends NOT added back (lesson 19).")
print("Sub-threshold bonus issues (e.g. 10% bonus = -9.1%) remain as fake losses; ex-dates listed above where found; returns not altered.")
print("Done.")
