"""Sector momentum and rate regime on KMI sector baskets, point in time. See tests/sector_momentum_regime.md.
Run: .venv/Scripts/python.exe scripts/tests/sector_momentum_regime.py   (raw output also saved to tests/out/sector_momentum_regime.txt)
"""
import ast, collections, glob, re, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from prices import load_panel, returns, liquid_universe, provisional_actions  # noqa: E402

SEED, NDRAWS, LIQ, COST = 42, 2000, 5e6, 0.005
RENAME = {"ENGRO": "ENGROH", "BYCO": "CNERGY", "ICI": "LCI"}
HIKE = ["Autos", "Islamic banks", "Power"]
CUT = ["Fertilizer", "Pharma", "Cement", "OMC"]
PRIMARY = (6, 0, 3)
GRID = [(L, sk, h) for h in (3, 1) for sk in (0, 1) for L in (3, 6, 12)]
COMBOS = sorted({(L, sk) for L, sk, _ in GRID})
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


def pc(x, d=2):
    return "   nan" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%"


# ======================================================================= data
close, vol, tv = load_panel()
dates, T = close.index, len(close)
cols = list(close.columns)
cix = {c: i for i, c in enumerate(cols)}
closev, volv = close.values, vol.values
obs = np.isfinite(closev)
oc = np.cumsum(obs, axis=0)
LAST = dates[-1]

mr = pd.Series(np.arange(T), index=dates).groupby([dates.year, dates.month]).last().values
if dates[mr[-1]] != (dates[mr[-1]] + pd.offsets.MonthEnd(0)) and dates[mr[-1]].month == LAST.month:
    mr = mr[:-1]  # incomplete month
ME_ROWS, ME_DATES = list(mr), dates[mr]
ER = [r + 1 for r in ME_ROWS]  # entry row = first trading day after formation date
J0 = int(np.where(ME_DATES == pd.Timestamp("2017-11-30"))[0][0])
JL = len(ME_ROWS) - 1
assert ER[JL] <= T - 1

# ---- sector codes and labels (U3)
scr = pd.read_csv(ROOT / "seed/data/fundamentals/screener_20261016.csv")
CODE = {}
for r in scr.itertuples():
    sym = r.symbol if r.symbol in cix else re.sub(r"(XD|XB|XR)$", "", r.symbol)
    if pd.notna(r.sector) and (sym not in CODE or r.symbol == sym):
        CODE[sym] = str(int(r.sector))
tree = ast.parse((ROOT / "scripts/sector_momentum.py").read_text(encoding="utf-8"))
S_DICT = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "S"][0]
votes = collections.defaultdict(collections.Counter)
for lab, names in S_DICT.items():
    for nm in names.split():
        if nm in CODE:
            votes[CODE[nm]][lab] += 1
BANK_CODE = CODE["MEBL"]
MOD_CODES = {CODE["FHAM"], CODE["PAKQATAR"]}
LABEL = {}
for code in sorted(set(CODE.values())):
    if code == BANK_CODE:
        LABEL[code] = "Islamic banks"
    elif code in MOD_CODES:
        LABEL[code] = "Modarabas & takaful"
    elif votes[code]:
        LABEL[code] = votes[code].most_common(1)[0][0]
    else:
        LABEL[code] = f"code{code}"
SHORT = {"Oil refineries": "Refineries", "Steel & engineering": "Steel & eng", "Tech & telecom": "Tech & telecom",
         "Glass, packaging, paper": "Glass/pack/paper", "Gas utilities & misc": "Gas utils & misc", "Food & staples": "Food & staples"}
LABEL = {k: SHORT.get(v, v) for k, v in LABEL.items()}
# note-label names in HIKE/CUT sets already match: Autos, Power, Fertilizer, Pharma, Cement, OMC

# ---- KMI lists (U1)
KMI = {}
for f in sorted(glob.glob(str(ROOT / "data/index_members/KMI_ALL_derived_*.csv"))):
    d = pd.Timestamp(re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1))
    out = set()
    for s in pd.read_csv(f).symbol:
        s = RENAME.get(s, s)
        if s not in cix:
            s = RENAME.get(re.sub(r"(XD|XB|XR)$", "", s), re.sub(r"(XD|XB|XR)$", "", s))
        out.add(s)
    KMI[d] = out
KMI_DATES = sorted(KMI)


def members_at(t):
    ok = [d for d in KMI_DATES if d <= t]
    return KMI[ok[-1] if ok else KMI_DATES[0]]


# ---- universe per formation (U2, U4, U5)
UNI, COV = {}, []
for j in range(J0, JL + 1):
    t, e = ME_DATES[j], ER[j]
    mem = members_at(t)
    priced = [m for m in mem if m in cix]
    liq = set(liquid_universe(dates[e], LIQ))
    liqk = [m for m in priced if m in liq]
    trade = [m for m in liqk if np.isfinite(closev[e, cix[m]])]
    nosec = [m for m in trade if m not in CODE]
    g = collections.defaultdict(list)
    for m in trade:
        if m in CODE:
            g[LABEL[CODE[m]]].append(cix[m])
    UNI[j] = dict(g)
    COV.append(dict(j=j, t=t, members=len(mem), priced=len(priced), liquid=len(liqk), traded=len(trade), nosec=len(nosec),
                    e3=sum(len(v) >= 3 for v in g.values()), e2=sum(len(v) >= 2 for v in g.values())))
COV = pd.DataFrame(COV).set_index("j")
LABELS = sorted({lab for j in UNI for lab in UNI[j]})
LI = {l: i for i, l in enumerate(LABELS)}
NS = len(LABELS)

# ---- macro / regime inputs (D4-D6, G1-G4)
pol = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"])
tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"])
cpi = pd.read_csv(ROOT / "data/macro/cpi.csv").set_index("month").yoy
kmi_px = pd.read_csv(ROOT / "data/macro/kmiallshr.csv", parse_dates=["date"]).set_index("date").close.sort_index()
SPREAD, FALLBACK, CPIDIR, G3, POLR = {}, 0, {}, {}, {}
for j in range(J0, JL + 1):
    t = ME_DATES[j]
    rate = pol[pol.date <= t].iloc[-1].rate
    a6 = tb[(tb.date <= t) & tb.y6m.notna()].iloc[-1]
    if (t - a6.date).days <= 45:
        y = a6.y6m
    else:
        y, FALLBACK = tb[tb.date <= t].iloc[-1].y3m, FALLBACK + 1
    SPREAD[j], POLR[j] = round(y - rate, 4), rate
    pm = t.to_period("M")
    d = cpi[str(pm - 1)] - cpi[str(pm - 4)]
    CPIDIR[j] = "rising" if d > 0 else "falling"
    last = pol[(pol.date <= t) & (pol.date > t - pd.DateOffset(months=12)) & (pol.decision != "hold")]
    G3[j] = "none" if last.empty else last.iloc[-1].decision


def g1(th):
    return {j: ("cuts" if SPREAD[j] <= -th else "hikes" if SPREAD[j] >= th else "neutral") for j in SPREAD}


G1 = g1(0.5)


def episodes(lab):
    out, js = [], sorted(lab)
    for j in js:
        if out and out[-1][2] == lab[j] and out[-1][1] == j - 1:
            out[-1][1] = j
        else:
            out.append([j, j, lab[j]])
    return out


EPS = episodes(G1)
EPID = {j: k for k, (a, b, _) in enumerate(EPS) for j in range(a, b + 1)}

# ======================================================================= returns variants (R1, R2)
sus = pd.read_csv(ROOT / "data/suspected_corporate_actions.csv", parse_dates=["date"])
r_crude = returns(close, method="crude", vol=vol)
r_head = r_crude.copy()
for s_, d_ in zip(sus.symbol, sus.date):
    if s_ in r_head.columns and d_ in r_head.index:
        r_head.at[d_, s_] = 0.0
r_adj = returns(close, method="adjusted", vol=vol, actions=provisional_actions())
# Sensitivity C (added after inspecting the data, NOT part of the approved spec): headline plus zero every same-day move beyond the
# circuit limit (+-10.5% above Rs10, Rs1.05 below) after at most 5 rows of gap, whatever the volume. crude/adjusted skip these when volume
# is above 3x normal, which is exactly how high-volume split ex-dates (LUCK 5:1, KOHC, THCCL, LCI, face-value splits of 2025-26) survive.
_prev = close.ffill().shift(1)
_pct = close / _prev - 1
_pos = pd.DataFrame(np.arange(len(close))[:, None] + 0.0 * close.values, close.index, close.columns).where(close.notna())
_gap = _pos - _pos.ffill().shift(1)
_big = ((_pct.abs() > 0.105).where(_prev > 10, (_pct * _prev).abs() > 1.05)) & (_gap <= 5) & close.notna()
r_C = r_head.mask(_big, 0.0)
N_BIG_UNFLAGGED = int(((r_head != 0) & _big).sum().sum())


class RV:
    def __init__(self, r):
        self.cum = (1 + r.reindex(index=dates, columns=cols).fillna(0)).cumprod().values
        self.sig = {}
        for L, sk in COMBOS:
            e, s = np.array(ME_ROWS)[np.arange(len(ME_ROWS)) - sk], np.array(ME_ROWS)[np.arange(len(ME_ROWS)) - sk - L]
            self.sig[(L, sk)] = (e, s)

    def signal(self, j, L, sk):
        e, s = self.sig[(L, sk)][0][j], self.sig[(L, sk)][1][j]
        x = self.cum[e] / self.cum[s] - 1
        fr = (oc[e] - oc[s]) / (e - s)
        return np.where(fr >= 0.6, x, np.nan)


STALE = collections.Counter()


def sector_tab(rv, count=False):
    tab = {}
    for j in range(J0, JL + 1):
        e, d = ER[j], {}
        sigs = {c: rv.signal(j, *c) for c in COMBOS}
        for lab, idx in UNI[j].items():
            idx = np.array(idx)
            if count:
                for h in (1, 3):
                    if j + h <= JL:
                        x = ER[j + h]
                        STALE[(h, "name-windows")] += len(idx)
                        STALE[(h, "exit-day stale close")] += int((np.isnan(closev[x, idx]) & np.isfinite(volv[x, idx])).sum())
                        STALE[(h, "series ends in window")] += int(np.isnan(volv[x, idx]).sum())
            if len(idx) < 2:
                continue
            rec = dict(n=len(idx), idx=idx, sig={c: (np.nanmean(sigs[c][idx]) if np.isfinite(sigs[c][idx]).any() else np.nan) for c in COMBOS})
            for h in (1, 3):
                if j + h <= JL:
                    rec[f"r{h}"] = float(np.mean(rv.cum[ER[j + h], idx] / rv.cum[e, idx] - 1))
            d[lab] = rec
        tab[j] = d
    return tab


def bench(tab, j, h):
    return float(np.mean([r[f"r{h}"] for r in tab[j].values() if r["n"] >= 3]))


def kmi_ret(j, h):
    a, b = kmi_px.asof(dates[ER[j]]), kmi_px.asof(dates[ER[j + h]])
    return b / a - 1


def valid_reg(tab, j):
    return sum(1 for r in tab[j].values() if r["n"] >= 3) >= 8


# ======================================================================= stats
def st(x):
    x = np.asarray(x, float)
    n = len(x)
    if n == 0:
        return dict(n=0, mean=np.nan, median=np.nan, win=np.nan, worst=np.nan, best=np.nan, sd=np.nan, t=np.nan)
    sd = x.std(ddof=1) if n > 1 else np.nan
    return dict(n=n, mean=x.mean(), median=np.median(x), win=(x > 0).mean(), worst=x.min(), best=x.max(), sd=sd,
                t=x.mean() / (sd / np.sqrt(n)) if n > 1 and sd > 0 else np.nan)


def nw_t(x, lag):
    x = np.asarray(x, float)
    n, u = len(x), x - x.mean()
    s = (u * u).sum() / n
    for k in range(1, lag + 1):
        s += 2 * (1 - k / (lag + 1)) * (u[k:] * u[:-k]).sum() / n
    return x.mean() / np.sqrt(s / n)


def avg_st(arrs):
    ss = [st(a) for a in arrs if len(a)]
    if not ss:
        return st([])
    return dict(n=np.mean([s["n"] for s in ss]), ntot=sum(s["n"] for s in ss), mean=np.mean([s["mean"] for s in ss]),
                median=np.mean([s["median"] for s in ss]), win=np.mean([s["win"] for s in ss]), worst=min(s["worst"] for s in ss),
                best=max(s["best"] for s in ss), sd=np.mean([s["sd"] for s in ss]), t=np.nanmean([s["t"] for s in ss]) if any(np.isfinite(s["t"]) for s in ss) else np.nan)


def maxdd(x):
    c = np.concatenate([[1], np.cumprod(1 + np.asarray(x))])
    return (c / np.maximum.accumulate(c) - 1).min()


# ======================================================================= portfolio contexts (P1-P3)
class Ctx:
    pass


def make_ctx(tab, L, sk, h):
    c = Ctx()
    c.key, c.h = (L, sk, h), h
    js = [j for j in range(J0, JL - h + 1) if sum(1 for r in tab[j].values() if r["n"] >= 3 and np.isfinite(r["sig"][(L, sk)])) >= 8]
    M = len(js)
    c.js, c.M = np.array(js), M
    R, SG = np.full((M, NS), np.nan), np.full((M, NS), np.nan)
    c.B, c.K = np.zeros(M), np.zeros(M)
    for m, j in enumerate(js):
        for lab, r in tab[j].items():
            if r["n"] >= 3 and np.isfinite(r["sig"][(L, sk)]):
                R[m, LI[lab]], SG[m, LI[lab]] = r[f"r{h}"], r["sig"][(L, sk)]
        c.B[m], c.K[m] = bench(tab, j, h), kmi_ret(j, h)
    c.R, c.SG, c.E = R, SG, np.isfinite(SG)
    c.off = (c.js - J0) % h
    pos = {j: m for m, j in enumerate(js)}
    c.pp = np.array([pos.get(j - h, -1) for j in js])
    c.OV = np.zeros((M, NS))
    c.bcost = np.zeros(M)
    for m, j in enumerate(js):
        p = c.pp[m]
        wb = {}
        labs3 = [lab for lab, r in tab[j].items() if r["n"] >= 3]
        for lab in labs3:
            for i in tab[j][lab]["idx"]:
                wb[i] = 1 / len(labs3) / tab[j][lab]["n"]
        if p >= 0:
            jp = js[p]
            for lab, r in tab[j].items():
                rp = tab[jp].get(lab)
                if rp is not None:
                    c.OV[m, LI[lab]] = len(np.intersect1d(r["idx"], rp["idx"])) / max(r["n"], rp["n"])
            wp = {}
            labsp = [lab for lab, r in tab[jp].items() if r["n"] >= 3]
            for lab in labsp:
                for i in tab[jp][lab]["idx"]:
                    wp[i] = 1 / len(labsp) / tab[jp][lab]["n"]
            c.bcost[m] = COST * (1 - sum(min(w, wp.get(i, 0)) for i, w in wb.items()))
        else:
            c.bcost[m] = COST / 2
    return c


def select(c, score, allowed=None):
    sc = np.where(c.E, score, np.nan)
    sc2 = sc if allowed is None else sc + 1000.0 * allowed
    top = np.argsort(-np.nan_to_num(sc2, nan=-np.inf), axis=-1)[..., :3]
    bot = np.argsort(np.nan_to_num(sc, nan=np.inf), axis=-1)[..., :3]
    return top, bot


def leg(c, picks, conservative=False):
    """gross return (D,M), cost (D,M), turnover fraction (D,M; nan for first windows)"""
    D, M, _ = picks.shape
    gross = np.take_along_axis(np.broadcast_to(c.R, (D, M, NS)), picks, axis=2).mean(2)
    oh = np.zeros((D, M, NS), bool)
    np.put_along_axis(oh, picks, True, axis=2)
    turn = np.full((D, M), np.nan)
    for m in range(M):
        p = c.pp[m]
        if p >= 0:
            turn[:, m] = 1 - ((oh[:, m] & oh[:, p]) * c.OV[m]).sum(1) / 3
    cost = np.where(np.isnan(turn), COST / 2, COST * np.nan_to_num(turn))
    if conservative:
        cost = np.full((D, M), COST)
    return gross, cost, turn


def offs(c):
    return [k for k in range(c.h) if (c.off == k).any()]


def agg(c, X):
    """X (D,M) -> per draw: mean, median, win rate, each averaged over start offsets (D,)"""
    ms, md, wn = [], [], []
    for k in offs(c):
        Z = X[:, c.off == k]
        ms.append(Z.mean(1)), md.append(np.median(Z, axis=1)), wn.append((Z > 0).mean(1))
    return np.mean(ms, 0), np.mean(md, 0), np.mean(wn, 0)


def by_off(c, x, mask=None):
    return [x[(c.off == k) & (True if mask is None else mask)] for k in offs(c)]


def pval(draws, obs_, ge=True):
    return float((draws >= obs_).mean())


def placebo_summary(c, X, obs_series):
    """X (D,M) draws of a series; obs_series (M,). Returns dict for mean/median/win."""
    d = agg(c, X)
    o = agg(c, obs_series[None])
    res = {}
    for name, dd, oo in zip(("mean", "median", "win"), d, o):
        res[name] = dict(obs=oo[0], med=np.median(dd), p5=np.percentile(dd, 5), p95=np.percentile(dd, 95), p=pval(dd, oo[0]))
    return res


# ======================================================================= H2 helpers
def month_S(tab, j, minn=2):
    ex = {lab: r["r3"] - bench(tab, j, 3) for lab, r in tab[j].items() if r["n"] >= minn}
    h_, c_ = [ex[l] for l in HIKE if l in ex], [ex[l] for l in CUT if l in ex]
    return (np.mean(h_) - np.mean(c_)) if h_ and c_ else np.nan


def compute_D(Sj, lab):
    """Sj, lab: dict j->value / label, over formation months with a 3m window. D averaged over the 3 start offsets."""
    ds = []
    for k in range(3):
        hs = [Sj[j] for j in Sj if (j - J0) % 3 == k and lab[j] == "hikes" and np.isfinite(Sj[j])]
        cs = [Sj[j] for j in Sj if (j - J0) % 3 == k and lab[j] == "cuts" and np.isfinite(Sj[j])]
        if hs and cs:
            ds.append(np.mean(hs) - np.mean(cs))
    return np.mean(ds) if ds else np.nan


def pl2(Sj, lab):
    js = sorted(Sj)
    N = len(js)
    lv = [lab[j] for j in js]
    obsD = compute_D(Sj, lab)
    nulls = []
    for s in range(12, N - 11):
        sh = {j: lv[(i + s) % N] for i, j in enumerate(js)}
        nulls.append(compute_D(Sj, sh))
    nulls = np.array([x for x in nulls if np.isfinite(x)])
    return obsD, nulls, float((nulls <= obsD).mean()), float((nulls >= obsD).mean())


def cell(tab, lab, labels_by_j, want, h):
    per, names, eps, nwin = collections.defaultdict(list), [], set(), 0
    for j in range(J0, JL - h + 1):
        if labels_by_j[j] != want or not valid_reg(tab, j):
            continue
        r = tab[j].get(lab)
        if r is None:
            continue
        per[(j - J0) % h].append(r[f"r{h}"] - bench(tab, j, h))
        names.append(r["n"]), eps.add(EPID_OF(labels_by_j, j))
    if not per:
        return None
    a = avg_st(list(per.values()))
    return dict(mean=a["mean"], median=a["median"], win=a["win"], n=a["n"], ntot=a["ntot"], eps=len(eps), names=float(np.median(names)))


def EPID_OF(labels_by_j, j):
    k = j
    while k - 1 >= J0 and labels_by_j[k - 1] == labels_by_j[j]:
        k -= 1
    return k


def fmt_cell(c):
    if c is None:
        return "-"
    flag = " INSUFF" if (c["n"] < 6 or c["eps"] < 2) else ""
    return f"{c['mean'] * 100:+.1f}/{c['median'] * 100:+.1f}/{c['win'] * 100:.0f}% n{c['n']:.1f} e{c['eps']} m{c['names']:.0f}{flag}"


def regime_table(tab, labels_by_j, wants, h, title):
    P(f"\n{title}  cell = mean/median/win  n(windows per offset, avg) e(episodes) m(median names); excess vs sector-EW benchmark B")
    labs = sorted({l for j in tab for l in tab[j]})
    P(f"{'sector':<22}" + "".join(f"{w:>44}" for w in wants))
    for lab in labs:
        row = [fmt_cell(cell(tab, lab, labels_by_j, w, h)) for w in wants]
        if all(x == "-" for x in row):
            continue
        P(f"{lab:<22}" + "".join(f"{x:>44}" for x in row))


# ======================================================================= main
rng = np.random.default_rng(SEED)
P("Sector momentum and rate regime on KMI sector baskets (point in time)")
P(f"run date 2026-10-17; panel {dates[0].date()} to {LAST.date()}; {len(cols)} symbols; random seed {SEED} (np.random.default_rng); placebo draws {NDRAWS}")
P(f"formation months {ME_DATES[J0].date()} to {ME_DATES[JL].date()} ({JL - J0 + 1} month-ends); entry = next trading day close; Rs{LIQ:.0e} liquidity; cost {COST:.1%} round trip")

P("\n== CODE -> LABEL TABLE (U3) ==")
P("code  label                  note-label votes                              KMI-ever names with prices")
kmi_ever = set().union(*KMI.values())
for code in sorted(LABEL, key=lambda c: (LABEL[c], c)):
    nk = sum(1 for m in kmi_ever if CODE.get(m) == code and m in cix)
    if nk or votes[code]:
        P(f"{code:<5} {LABEL[code]:<22} {str(dict(votes[code])) if votes[code] else '':<45} {nk}")
P(f"commercial-banks code {BANK_CODE} -> Islamic banks; modaraba/takaful codes {sorted(MOD_CODES)} -> Modarabas & takaful")
P(f"HIKE set {HIKE}; CUT set {CUT}")

RVS = {"headline": r_head, "A_crude_only": r_crude, "B_adjusted": r_adj, "C_zero_all_beyond_limit": r_C}
TABS, CTX = {}, {}
for nm, r in RVS.items():
    rv = RV(r)
    TABS[nm] = sector_tab(rv, count=(nm == "headline"))
    CTX[nm] = {k: make_ctx(TABS[nm], *k) for k in (GRID if nm == "headline" else [PRIMARY])}
tab, ctx0 = TABS["headline"], CTX["headline"]

P("\n== COVERAGE LOG (U5), per formation ==")
P("j  formation   KMI_members priced liquid traded nosector elig(>=3) elig(>=2) valid_H1(primary)")
validp = set(ctx0[PRIMARY].js)
for j, r in COV.iterrows():
    P(f"{j - J0:>3} {r.t.date()} {r.members:>6} {r.priced:>6} {r.liquid:>6} {r.traded:>6} {r.nosec:>7} {r.e3:>7} {r.e2:>7}  {'Y' if j in validp else '-'}")
P(f"median/min: members {COV.members.median():.0f}/{COV.members.min()}  priced {COV.priced.median():.0f}/{COV.priced.min()}  liquid {COV.liquid.median():.0f}/{COV.liquid.min()}  "
  f"traded {COV.traded.median():.0f}/{COV.traded.min()}  no-sector {COV.nosec.median():.0f}/{COV.nosec.min()} (max {COV.nosec.max()})  elig3 {COV.e3.median():.0f}/{COV.e3.min()}  "
  f"missing price file (survivorship gap) median {(COV.members - COV.priced).median():.0f} max {(COV.members - COV.priced).max()}")
pre = COV[COV.t <= "2018-12-31"]
P(f"pre-2019 sub-period ({len(pre)} months): members median {pre.members.median():.0f}, priced {pre.priced.median():.0f}, liquid {pre.liquid.median():.0f}, elig3 median {pre.e3.median():.0f} min {pre.e3.min()}")
P(f"months with >=8 eligible sectors (primary variant ranks): {len(validp)} of {len(COV)}; months not ranked: {sorted(str(ME_DATES[j].date()) for j in range(J0, JL + 1) if j not in validp)[:40]}")
P("exit-day stale closes / in-window series ends (headline, name-windows):")
for h in (1, 3):
    P(f"  h={h}m: name-windows {STALE[(h, 'name-windows')]}, exit-day stale close {STALE[(h, 'exit-day stale close')]}, series ends in window {STALE[(h, 'series ends in window')]}")
P(f"extra sensitivity C: {N_BIG_UNFLAGGED} stock-days beyond the circuit limit are NOT zeroed by the headline (high-volume ex-dates); C zeroes them")
P(f"3M T-bill fallback (y3m used because latest y6m auction older than 45 days): {FALLBACK} of {JL - J0 + 1} months")
bl = collections.Counter()
for j in UNI:
    for lab, idx in UNI[j].items():
        bl[lab] += 0
ever = collections.defaultdict(set)
for j in UNI:
    for lab, idx in UNI[j].items():
        ever[lab] |= {cols[i] for i in idx}
P("names ever in each basket (liquid KMI, any month): " + "; ".join(f"{k}:{len(v)}" for k, v in sorted(ever.items())))
P("Islamic banks names: " + ",".join(sorted(ever["Islamic banks"])) + " | Fertilizer: " + ",".join(sorted(ever["Fertilizer"])) + " | OMC: " + ",".join(sorted(ever["OMC"])))

# ---------------------------------------------------------------- T1
P("\n== T1: H1 grid. LS = mean(top 3 sectors) - mean(bottom 3 sectors), gross unless 'net'. Non-overlapping; h=3 rows = average of the 3 start-offset series ==")
P("n = windows per offset (avg). t = plain t (avg across offsets). p = share of 2000 placebo draws (random sector ranks, same months) with mean >= observed.")
P(f"{'L/skip/h':<9}{'n':>5}{'mean':>8}{'median':>8}{'win':>6}{'worst':>8}{'best':>8}{'t':>6}{'p_gross':>8}{'p_net':>7}{'net':>8}{'netCons':>8}{'turn':>6}")
T1 = {}
for key in GRID:
    c = ctx0[key]
    top, bot = select(c, c.SG[None])
    gt, ct, tt = leg(c, top)
    gb, cb, tb_ = leg(c, bot)
    _, ctc, _ = leg(c, top, True)
    _, cbc, _ = leg(c, bot, True)
    LS, LSn, LSc = (gt - gb)[0], (gt - gb - ct - cb)[0], (gt - gb - ctc - cbc)[0]
    keys = rng.random((NDRAWS, c.M, NS), dtype=np.float32)
    ptop, pbot = select(c, keys)
    pgt, pct_, _ = leg(c, ptop)
    pgb, pcb, _ = leg(c, pbot)
    pg = placebo_summary(c, pgt - pgb, LS)
    pn = placebo_summary(c, pgt - pgb - pct_ - pcb, LSn)
    a = avg_st(by_off(c, LS))
    an, ac = avg_st(by_off(c, LSn)), avg_st(by_off(c, LSc))
    turn = np.nanmean((tt + tb_)[0]) / 2
    T1[key] = dict(g=a, net=an, cons=ac, pg=pg, pn=pn, turn=turn, LS=LS, LSn=LSn, ctx=c)
    P(f"{key[0]:>2}/{key[1]}/{key[2]}m {a['n']:>5.1f}{pc(a['mean']):>8}{pc(a['median']):>8}{a['win'] * 100:>5.0f}%{pc(a['worst']):>8}{pc(a['best']):>8}{a['t']:>6.2f}{pg['mean']['p']:>8.3f}{pn['mean']['p']:>7.3f}{pc(an['mean']):>8}{pc(ac['mean']):>8}{turn:>6.2f}"
      + ("   <- PRIMARY" if key == PRIMARY else ""))
    if key[2] == 3:
        a2 = st(LS)
        P(f"   overlapping monthly: n={a2['n']} mean {pc(a2['mean'])} median {pc(a2['median'])} win {a2['win'] * 100:.0f}% worst {pc(a2['worst'])} best {pc(a2['best'])} Newey-West t (lag 2) {nw_t(LS, 2):.2f}  [OVERLAPPING, not independent]")
    if key == PRIMARY:
        for k in offs(c):
            s_ = st(LS[c.off == k])
            P(f"   offset {k} ({['Nov/Feb/May/Aug', 'Dec/Mar/Jun/Sep', 'Jan/Apr/Jul/Oct'][k]}): n={s_['n']} mean {pc(s_['mean'])} median {pc(s_['median'])} win {s_['win'] * 100:.0f}% worst {pc(s_['worst'])} best {pc(s_['best'])} t {s_['t']:.2f}")
        pn_ = T1[key]["pn"]
        P(f"   primary placebo (gross LS): median of placebo means {pc(pg['mean']['med'])}, 5th {pc(pg['mean']['p5'])}, 95th {pc(pg['mean']['p95'])}; observed {pc(pg['mean']['obs'])}; "
          f"median stat p={pg['median']['p']:.3f}, win-rate stat p={pg['win']['p']:.3f}")
        P(f"   primary placebo (net LS):   median of placebo means {pc(pn_['mean']['med'])}, 5th {pc(pn_['mean']['p5'])}, 95th {pc(pn_['mean']['p95'])}; observed {pc(pn_['mean']['obs'])}")

# primary long-only
c = ctx0[PRIMARY]
top, bot = select(c, c.SG[None])
gt, ct, tt = leg(c, top)
LO = gt[0] - c.B
LOn = gt[0] - ct[0] - c.B
LOk = gt[0] - ct[0] - c.K
P("\nPrimary long-only (top 3 sectors, EW): excess vs B (sector-EW), gross / net; and net excess vs KMIALLSHR")
for nm, x in (("LO gross vs B", LO), ("LO net vs B", LOn), ("LO net vs KMIALLSHR", LOk)):
    a = avg_st(by_off(c, x))
    P(f"  {nm:<22} n/off {a['n']:.1f} mean {pc(a['mean'])} median {pc(a['median'])} win {a['win'] * 100:.0f}% worst {pc(a['worst'])} t {a['t']:.2f}")
P(f"  mean turnover top leg {np.nanmean(tt):.2f}; mean B window return {pc(c.B.mean())}; mean KMIALLSHR window return {pc(c.K.mean())}")

# ---------------------------------------------------------------- S3 splits
P("\n== S3 splits, primary variant (6m lookback, no skip, 3m hold). n = windows per offset (avg); values averaged over 3 offsets ==")
LS, LSn = T1[PRIMARY]["LS"], T1[PRIMARY]["LSn"]
yrs = np.array([ME_DATES[j].year for j in c.js])
P(f"{'split':<26}{'n/off':>6}{'LS mean':>9}{'LS med':>8}{'LS win':>7}{'LSnet':>8}{'LOnet vs B':>11}")
splits = [(f"year {y}", yrs == y) for y in sorted(set(yrs))]
half1 = np.array([ME_DATES[j] <= pd.Timestamp("2021-12-31") for j in c.js])
splits += [("half 2017-11..2021-12", half1), ("half 2022-01..2026-06", ~half1),
           ("pre-2019 (2017-11..2018-12)", np.array([ME_DATES[j] <= pd.Timestamp("2018-12-31") for j in c.js])),
           ("2019-01 onward", np.array([ME_DATES[j] > pd.Timestamp("2018-12-31") for j in c.js]))]
ypos = 0
for nm, mk in splits:
    a, an, al = avg_st(by_off(c, LS, mk)), avg_st(by_off(c, LSn, mk)), avg_st(by_off(c, LOn, mk))
    if a["n"] == 0 or not np.isfinite(a["mean"]):
        continue
    P(f"{nm:<26}{a['n']:>6.1f}{pc(a['mean']):>9}{pc(a['median']):>8}{a['win'] * 100:>6.0f}%{pc(an['mean']):>8}{pc(al['mean']):>11}")
ym = [avg_st(by_off(c, LS, yrs == y))["mean"] for y in sorted(set(yrs))]
P(f"years with positive LS mean: {sum(m > 0 for m in ym)} of {len(ym)} (offset-averaged). Independent windows per offset: {np.mean([len(x) for x in by_off(c, LS)]):.1f}; sector returns within a window are cross-correlated, so effective n is the window count, not sector-windows.")

# ---------------------------------------------------------------- T2
P("\n== T2: regime x sector, next-3m excess vs B (non-overlapping, mean of the 3 offsets; median and win rate also averaged over offsets) ==")
P("R3 note: bonuses below the circuit (e.g. 10% bonus shows as -9.1%) stay in as fake losses; bonus payers cluster in cement, fertilizer, banks, so those sectors are biased DOWN in this table.")
regime_table(tab, G1, ["cuts", "neutral", "hikes"], 3, "T2a: curve spread (6M T-bill - policy rate) +-50bp, 3m hold")
regime_table(tab, G1, ["cuts", "neutral", "hikes"], 1, "T2b: same, 1m hold (single series)")
regime_table(tab, CPIDIR, ["falling", "rising"], 3, "T2c: CPI direction (3m change of yoy known at t), 3m hold")
regime_table(tab, G3, ["cut", "none", "hike"], 3, "T2d: last non-hold MPS decision in 12 months, 3m hold")
for th in (0.25, 1.0):
    regime_table(tab, g1(th), ["cuts", "neutral", "hikes"], 3, f"T2e: curve spread +-{int(th * 100)}bp (sensitivity only), 3m hold")
cnt = collections.Counter(G1[j] for j in G1)
P(f"\nformation months by G1 label (all {len(G1)}): {dict(cnt)}; by CPI direction {dict(collections.Counter(CPIDIR.values()))}; by G3 {dict(collections.Counter(G3.values()))}")
P("combined curve x CPI cells (descriptive only): months / mean monthly-3m S (overlapping)")
Sall = {j: month_S(tab, j) for j in range(J0, JL - 3 + 1) if valid_reg(tab, j)}
for cl in ("cuts", "neutral", "hikes"):
    for cp in ("falling", "rising"):
        v = [Sall[j] for j in Sall if G1[j] == cl and CPIDIR[j] == cp and np.isfinite(Sall[j])]
        P(f"  {cl:<8}{cp:<8} months {len(v):>3} mean S {pc(np.mean(v)) if v else 'n/a'}")

# ---------------------------------------------------------------- T3
P("\n== T3: regime episodes (G4, +-50bp curve) ==")
P("S = mean excess of eligible HIKE sectors (Autos, Islamic banks, Power) minus mean excess of eligible CUT sectors (Fertilizer, Pharma, Cement, OMC), next 3m, sectors with >=2 names. Mean S over all valid formation months in the episode (overlapping 3m windows).")
P(f"{'start':<12}{'end':<12}{'months':>7}{'label':>9}{'avgSpread':>10}{'mean S':>9}{'S months':>9}")
ep_S = []
for a, b, lb in EPS:
    v = [Sall[j] for j in range(a, b + 1) if j in Sall and np.isfinite(Sall[j])]
    ep_S.append((lb, np.mean(v) if v else np.nan))
    P(f"{str(ME_DATES[a].date()):<12}{str(ME_DATES[b].date()):<12}{b - a + 1:>7}{lb:>9}{np.mean([SPREAD[j] for j in range(a, b + 1)]):>10.2f}{pc(np.mean(v)) if v else '   n/a':>9}{len(v):>9}")
Sj = {j: Sall[j] for j in Sall}
obsD, nulls, pct_obs, pD = pl2(Sj, G1)
P(f"episodes: hikes {sum(1 for e in EPS if e[2] == 'hikes')}, cuts {sum(1 for e in EPS if e[2] == 'cuts')}, neutral {sum(1 for e in EPS if e[2] == 'neutral')}")
P(f"observed D = mean S|hikes - mean S|cuts (avg of 3 offsets) = {pc(obsD)}; circular-shift null: {len(nulls)} shifts (12..N-12 months, N={len(Sj)}), null median {pc(np.median(nulls))}, 5th {pc(np.percentile(nulls, 5))}, 95th {pc(np.percentile(nulls, 95))}; "
  f"observed percentile {pct_obs * 100:.0f}%; one-sided p (null D >= observed) = {pD:.3f}")
hk = [s for l, s in ep_S if l == "hikes" and np.isfinite(s)]
ck = [s for l, s in ep_S if l == "cuts" and np.isfinite(s)]
H2_hike_ok = len(hk) > 0 and sum(s > 0 for s in hk) > len(hk) / 2
H2_cut_ok = len(ck) > 0 and sum(s < 0 for s in ck) > len(ck) / 2
P(f"predicted sign: hikes episodes with S>0: {sum(s > 0 for s in hk)} of {len(hk)}; cuts episodes with S<0: {sum(s < 0 for s in ck)} of {len(ck)}")
for th in (0.25, 1.0):
    o2, n2, pe2, p2 = pl2(Sj, g1(th))
    P(f"sensitivity +-{int(th * 100)}bp (not used to pick): D {pc(o2)}, null shifts {len(n2)}, percentile {pe2 * 100:.0f}%, p {p2:.3f}; episodes {len(episodes(g1(th)))}")
o3, n3, pe3, p3 = pl2(Sj, {j: ("hikes" if G3[j] == "hike" else "cuts" if G3[j] == "cut" else "neutral") for j in G3})
P(f"G3 labels (last MPS decision hike->hikes, cut->cuts): D {pc(o3)}, null shifts {len(n3)}, percentile {pe3 * 100:.0f}%, p {p3:.3f}")
H2_supported = (pD < 0.05) and H2_hike_ok and H2_cut_ok

# ---------------------------------------------------------------- T4
P("\n== T4: regime-tilt rule RT vs plain momentum top 3 vs B vs KMIALLSHR (primary 6/0/3), net of P2 costs; non-overlapping, averaged over 3 offsets ==")


def rt_allowed(c):
    al = np.zeros((c.M, NS))
    for m, j in enumerate(c.js):
        grp = HIKE if G1[j] == "hikes" else CUT if G1[j] == "cuts" else []
        for lab in grp:
            if lab in LI:
                al[m, LI[lab]] = 1.0
    return al * c.E


def t4_core(c, label_rng=None):
    al = rt_allowed(c)
    topm, _ = select(c, c.SG[None])
    topr, _ = select(c, c.SG[None], al[None])
    out = {}
    for nm, tp in (("RT", topr), ("MOM", topm)):
        g, cst, tn = leg(c, tp)
        out[nm] = dict(net=(g - cst)[0], gross=g[0], turn=np.nanmean(tn))
    out["B"] = dict(net=c.B - c.bcost, gross=c.B)
    out["K"] = dict(net=c.K, gross=c.K)
    out["al"] = al
    out["picks"] = (topr, topm)
    return out


def t4_placebo(c, al):
    res = {}
    keys = rng.random((NDRAWS, c.M, NS), dtype=np.float32)
    for nm, a_ in (("RT", al[None]), ("MOM", None)):
        tp, _ = select(c, keys, a_)
        g, cst, _ = leg(c, tp)
        res[nm] = g - cst
    return res


c = ctx0[PRIMARY]
R4 = t4_core(c)
PL4 = t4_placebo(c, R4["al"])
half1 = np.array([ME_DATES[j] <= pd.Timestamp("2021-12-31") for j in c.js])
T4 = {}
P(f"{'series':<26}{'n/off':>6}{'mean':>8}{'median':>8}{'win':>6}{'worst':>8}{'maxDD':>8}{'p':>7}{'h1 mean':>9}{'h2 mean':>9}{'off0':>8}{'off1':>8}{'off2':>8}")
rows = [("RT net (abs)", R4["RT"]["net"], None, None), ("MOM top3 net (abs)", R4["MOM"]["net"], None, None), ("B net (abs)", R4["B"]["net"], None, None), ("KMIALLSHR (abs)", c.K, None, None),
        ("RT net - B", R4["RT"]["net"] - c.B, PL4["RT"] - c.B[None], "RT"), ("MOM net - B", R4["MOM"]["net"] - c.B, PL4["MOM"] - c.B[None], "MOM"),
        ("RT net - KMIALLSHR", R4["RT"]["net"] - c.K, PL4["RT"] - c.K[None], "RTk"), ("MOM net - KMIALLSHR", R4["MOM"]["net"] - c.K, PL4["MOM"] - c.K[None], "MOMk"),
        ("RT net - MOM net", R4["RT"]["net"] - R4["MOM"]["net"], None, None)]
for nm, x, pl, tag in rows:
    a = avg_st(by_off(c, x))
    dd = np.mean([maxdd(z) for z in by_off(c, x)])
    pv = placebo_summary(c, pl, x)["mean"]["p"] if pl is not None else np.nan
    h1_, h2_ = avg_st(by_off(c, x, half1))["mean"], avg_st(by_off(c, x, ~half1))["mean"]
    om = [st(z)["mean"] for z in by_off(c, x)]
    T4[nm] = dict(a=a, p=pv, h1=h1_, h2=h2_, om=om, dd=dd)
    P(f"{nm:<26}{a['n']:>6.1f}{pc(a['mean']):>8}{pc(a['median']):>8}{a['win'] * 100:>5.0f}%{pc(a['worst']):>8}{pc(dd):>8}{pv:>7.3f}{pc(h1_):>9}{pc(h2_):>9}" + "".join(f"{pc(m_):>8}" for m_ in om))
P(f"mean turnover: RT {R4['RT']['turn']:.2f}, MOM {R4['MOM']['turn']:.2f}; months in hikes/cuts/neutral among ranked months: "
  f"{collections.Counter(G1[j] for j in c.js)}; RT differs from MOM in {int(sum(set(a) != set(b) for a, b in zip(R4['picks'][0][0], R4['picks'][1][0])))} of {c.M} months")
P("p = share of 2000 placebo draws (random sector picks, from the same allowed set the rule uses that month for RT) with mean >= observed, net of the same costs.")
bo = T4["RT net - B"]["a"]

# ---------------------------------------------------------------- T5 sensitivities
P("\n== T5: sensitivities for the primary variant, D and the tilt rule ==")
SENS = {}
for nm in RVS:
    cc = CTX[nm][PRIMARY] if nm != "headline" else ctx0[PRIMARY]
    tb_ = TABS[nm]
    top, bot = select(cc, cc.SG[None])
    gt, ct, _ = leg(cc, top)
    gb, cb, _ = leg(cc, bot)
    LSg, LSn_ = (gt - gb)[0], (gt - gb - ct - cb)[0]
    keys = rng.random((NDRAWS, cc.M, NS), dtype=np.float32)
    ptop, pbot = select(cc, keys)
    pgt, pct_, _ = leg(cc, ptop)
    pgb, pcb, _ = leg(cc, pbot)
    plg, pln = placebo_summary(cc, pgt - pgb, LSg), placebo_summary(cc, pgt - pgb - pct_ - pcb, LSn_)
    Rr = t4_core(cc)
    Pp = t4_placebo(cc, Rr["al"])
    rtB = Rr["RT"]["net"] - cc.B
    pRT = placebo_summary(cc, Pp["RT"] - cc.B[None], rtB)["mean"]["p"]
    mB = Rr["MOM"]["net"] - cc.B
    Sx = {j: month_S(tb_, j) for j in range(J0, JL - 3 + 1) if valid_reg(tb_, j)}
    D_, nl, pe_, pd_ = pl2(Sx, G1)
    SENS[nm] = dict(LSg=avg_st(by_off(cc, LSg)), LSn=avg_st(by_off(cc, LSn_)), pg=plg["mean"]["p"], pn=pln["mean"]["p"], D=D_, pD=pd_, pe=pe_,
                    rt=avg_st(by_off(cc, rtB)), rtp=pRT, mom=avg_st(by_off(cc, mB)), rtk=avg_st(by_off(cc, Rr["RT"]["net"] - cc.K)), M=cc.M)
P(f"{'return series':<14}{'months':>7}{'LS gross':>9}{'LS net':>8}{'p gross':>8}{'p net':>7}{'D':>8}{'D pctile':>9}{'D p':>6}{'RT-B net':>9}{'RT p':>6}{'MOM-B net':>10}{'RT-KMI':>8}")
for nm, s_ in SENS.items():
    P(f"{nm:<14}{s_['M']:>7}{pc(s_['LSg']['mean']):>9}{pc(s_['LSn']['mean']):>8}{s_['pg']:>8.3f}{s_['pn']:>7.3f}{pc(s_['D']):>8}{s_['pe'] * 100:>8.0f}%{s_['pD']:>6.3f}{pc(s_['rt']['mean']):>9}{s_['rtp']:>6.3f}{pc(s_['mom']['mean']):>10}{pc(s_['rtk']['mean']):>8}")
SPEC3 = ("headline", "A_crude_only", "B_adjusted")  # the approved spec reruns A and B; C is an extra
for k in ("LSn", "LSg", "rt", "mom"):
    sg = {nm: int(np.sign(s_[k]["mean"])) for nm, s_ in SENS.items()}
    P(f"sign check {k}: {sg} -> A and B vs headline: {'same sign' if len({sg[n] for n in SPEC3}) == 1 else 'SIGN CHANGES: not robust to price adjustment'}; with extra C: {'same sign' if len(set(sg.values())) == 1 else 'SIGN CHANGES'}")
sgD = {nm: int(np.sign(s_["D"])) for nm, s_ in SENS.items()}
sigD = {nm: bool(s_["pD"] < 0.05) for nm, s_ in SENS.items()}
P(f"sign check D: {sgD}; significant (p<0.05): {sigD} -> {'D significance changes under C: not robust to price adjustment' if len(set(sigD.values())) > 1 else 'unchanged'}")

# ---------------------------------------------------------------- verdicts
P("\n== PRE-SPECIFIED VERDICTS ==")


def checks(name, x, pl_p, base_ser, sens_key, vs_mom=None):
    a = avg_st(by_off(c, x))
    om = [st(z)["mean"] for z in by_off(c, x)]
    hv = [avg_st(by_off(c, x, half1))["mean"], avg_st(by_off(c, x, ~half1))["mean"]]
    ss = {nm: np.sign(s_[sens_key]["mean"]) for nm, s_ in SENS.items() if nm in SPEC3}
    res = [("mean>0", a["mean"] > 0), ("median>0", a["median"] > 0), ("win>50%", a["win"] > 0.5), ("placebo p<0.05", pl_p < 0.05),
           ("all 3 offsets positive", all(m_ > 0 for m_ in om)), ("both halves positive", all(h_ > 0 for h_ in hv)),
           ("same sign A and B", len(set(ss.values())) == 1 and a["mean"] > 0)]
    if vs_mom is not None:
        res.append(("not worse than plain momentum top 3", vs_mom))
    P(f"{name}: " + "; ".join(f"{k}={'Y' if v else 'N'}" for k, v in res) + f"  => {'EDGE' if all(v for _, v in res) else 'NO EDGE'}")
    return all(v for _, v in res)


rtB = R4["RT"]["net"] - c.B
okB = checks("RT net vs B", rtB, T4["RT net - B"]["p"], None, "rt", T4["RT net - MOM net"]["a"]["mean"] >= 0)
okK = checks("RT net vs KMIALLSHR", R4["RT"]["net"] - c.K, T4["RT net - KMIALLSHR"]["p"], None, "rtk", T4["RT net - MOM net"]["a"]["mean"] >= 0)
okM = checks("Plain momentum top 3 net vs B (reference)", R4["MOM"]["net"] - c.B, T4["MOM net - B"]["p"], None, "mom")
h1p = T1[PRIMARY]
SENS_LS = {nm: np.sign(s_["LSn"]["mean"]) for nm, s_ in SENS.items() if nm in SPEC3}
h1_checks = [("net mean>0", h1p["net"]["mean"] > 0), ("net median>0", h1p["net"]["median"] > 0), ("net win>50%", h1p["net"]["win"] > 0.5),
             ("net placebo p<0.05", h1p["pn"]["mean"]["p"] < 0.05),
             ("all 3 offsets positive (net)", all(st(z)["mean"] > 0 for z in by_off(h1p["ctx"], h1p["LSn"]))),
             ("both halves positive (net)", all(avg_st(by_off(h1p["ctx"], h1p["LSn"], mk))["mean"] > 0 for mk in (half1, ~half1))),
             ("same sign A and B", len(set(SENS_LS.values())) == 1 and h1p["net"]["mean"] > 0)]
H1_supported = all(v for _, v in h1_checks)
P("H1 primary (LS net of both-leg costs): " + "; ".join(f"{k}={'Y' if v else 'N'}" for k, v in h1_checks) + f"  => H1 {'SUPPORTED' if H1_supported else 'WEAK / NOT SIGNIFICANT'}")
P(f"H2: PL2 p={pD:.3f} (<0.05: {'Y' if pD < 0.05 else 'N'}); hikes episodes with predicted sign majority: {'Y' if H2_hike_ok else 'N'}; cuts episodes: {'Y' if H2_cut_ok else 'N'} => H2 {'SUPPORTED' if H2_supported else 'NOT SUPPORTED'} (in-sample lists)")
P(f"TILT RULE: RT net vs B => {'EDGE' if okB else 'NO EDGE'}; vs KMIALLSHR => {'EDGE' if okK else 'NO EDGE'}")

Path(ROOT / "tests/out").mkdir(exist_ok=True)
(ROOT / "tests/out/sector_momentum_regime.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
