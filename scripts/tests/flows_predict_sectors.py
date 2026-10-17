"""Do investor flows predict sector returns? (approved spec, 17 Oct 2026)

Run:  .venv/Scripts/python.exe scripts/tests/flows_predict_sectors.py
Writes the raw output to tests/out/flows_predict_sectors.txt. Every number in tests/flows_predict_sectors.md comes from it.
Sections of the output are headed "=== name ===" so the write-up can be assembled from them.
"""
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices  # noqa: E402
from prices import load_panel, returns, liquid_universe  # noqa: E402,F401  (ew_market deliberately unused: survivor-biased)

warnings.filterwarnings("ignore")
OUT = ROOT / "tests" / "out" / "flows_predict_sectors.txt"
LOG = []


def out(s=""):
    print(s)
    LOG.append(str(s))


def table(headers, rows):
    out("| " + " | ".join(headers) + " |")
    out("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        out("| " + " | ".join(str(x) for x in r) + " |")


def sec(name):
    out(f"\n=== {name} ===")


def f3(x):
    return "n/a" if x is None or not np.isfinite(x) else f"{x:+.3f}"


def pc(x, d=1):
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.{d}f}%"


def p0(x):
    return "n/a" if x is None or not np.isfinite(x) else f"{x:.0f}"


# ---------------------------------------------------------------- configuration
SECMAP = {
    "Cement": "CEMENT", "Commercial Banks": "COMMERCIAL BANKS", "Fertilizer": "FERTILIZER",
    "Food and Personal Care Products": "FOOD & PERSONAL CARE PRODUCTS",
    "Oil and Gas Exploration Companies": "OIL & GAS EXPLORATION COMPANIES",
    "Oil and Gas Marketing Companies": "OIL & GAS MARKETING COMPANIES",
    "Power Generation and Distribution": "POWER GENERATION & DISTRIBUTION",
    "Technology and Communication": "TECHNOLOGY & COMMUNICATION", "Textile Composite": "TEXTILE COMPOSITE"}
SECS = list(SECMAP)
SHORT = {"Cement": "Cement", "Commercial Banks": "Banks", "Fertilizer": "Fertilizer", "Food and Personal Care Products": "Food",
         "Oil and Gas Exploration Companies": "E&P", "Oil and Gas Marketing Companies": "OMC",
         "Power Generation and Distribution": "Power", "Technology and Communication": "Tech", "Textile Composite": "Textile"}
NS = len(SECS)
# group -> pre-registered sign (0 = exploratory)
GROUPS = {"fipi": +1, "lipi mutual funds": +1, "lipi insurance companies": +1, "lipi banks / dfi": +1,
          "lipi individuals": -1, "lipi broker proprietary trading": -1,
          "lipi companies": 0, "lipi nbfc": 0, "lipi other organization": 0}
GL = {g: g.replace("lipi ", "") for g in GROUPS}
SIGNLBL = {1: "+", -1: "-", 0: "expl."}
COST = 0.005
MIN_VALUE = 5e6
NPERM = 1000
YEARS = list(range(2017, 2027))
MAIN6 = ["fipi", "lipi mutual funds", "lipi insurance companies", "lipi banks / dfi", "lipi individuals", "lipi broker proprietary trading"]

# ---------------------------------------------------------------- data
sec("data and git state")
close, vol, tv = load_panel()
nsym = close.shape[1]
out(f"panel: {close.shape[0]} dates x {nsym} symbols, {close.index[0].date()} to {close.index[-1].date()}")
susp = pd.read_csv(prices.SUSPECTS, parse_dates=["date"])
out(f"suspected_corporate_actions.csv rows used: {len(susp)}")
gs = subprocess.run(["git", "status", "--short", "data/suspected_corporate_actions.csv"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
gd = subprocess.run(["git", "diff", "--numstat", "data/suspected_corporate_actions.csv"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
out(f"git status of data/suspected_corporate_actions.csv: '{gs}' (modified in working tree, uncommitted); numstat added/removed: {gd}")

symbols = pd.read_csv(ROOT / "data" / "symbols.csv").set_index("symbol").sectorName
col_idx = {s: np.array([j for j, c in enumerate(close.columns) if symbols.get(c) == SECMAP[s]], dtype=int) for s in SECS}
out("symbols per sector in panel (listed 2026-10-16): " + ", ".join(f"{SHORT[s]} {len(col_idx[s])}" for s in SECS))

flraw = pd.read_csv(ROOT / "data" / "macro" / "fipi_lipi_by_sector.csv", parse_dates=["date"])
fdates = pd.DatetimeIndex(sorted(flraw.date.unique()))
out(f"flows by sector: {len(fdates)} flow dates, {fdates[0].date()} to {fdates[-1].date()}; groups {flraw.investor_group.nunique()}, sectors {flraw.sector.nunique()}")
fl = flraw[flraw.sector.isin(SECMAP)]
NET, MISSROWS, MISSDATES = {}, {}, {}
for g in GROUPS:
    d = flraw[flraw.investor_group == g]
    gd_ = fdates.isin(pd.DatetimeIndex(d.date.unique()))
    p = fl[fl.investor_group == g].pivot_table(index="date", columns="sector", values="net_usd_mn", aggfunc="sum").reindex(index=fdates, columns=SECS)
    miss_rows = int((p.isna().values & gd_[:, None]).sum())
    p = p.mask(p.isna() & gd_[:, None], 0.0)          # missing sector row on a date the group reports = 0 net
    p[~gd_] = np.nan                                   # whole date missing for the group = missing
    NET[g], MISSROWS[g], MISSDATES[g] = p, miss_rows, int((~gd_).sum())
BUY = fl.pivot_table(index="date", columns="sector", values="buy_usd_mn", aggfunc="sum").reindex(index=fdates, columns=SECS).fillna(0.0)
sec("data gaps in the by-sector flow file (9 sectors in scope)")
table(["group", "flow dates missing for group", "sector-day rows absent on dates the group reports (filled 0)"],
      [[GL[g], MISSDATES[g], MISSROWS[g]] for g in GROUPS])


def make_signal(clip):
    den = BUY.rolling(20).sum()
    res = {}
    for g in GROUPS:
        x = NET[g]
        if clip:
            lim = 5 * x.abs().shift(1).rolling(250, min_periods=120).median()
            x = x.where(lim.isna() | (lim <= 0), x.clip(lower=-lim, upper=lim))
        res[g] = (x.rolling(20, min_periods=18).sum() / den).values
    return res


SIG = make_signal(False)
SIGC = make_signal(True)

# ---------------------------------------------------------------- returns
def zero_suspects(r):
    r = r.copy()
    ri, ci = r.index, {c: j for j, c in enumerate(r.columns)}
    for s in susp.itertuples():
        if s.symbol in ci and s.date in ri:
            r.iloc[ri.get_loc(s.date), ci[s.symbol]] = 0.0
    return r


R_HEAD = zero_suspects(returns(close, method="crude", vol=vol))
CUM_HEAD = (1 + R_HEAD.fillna(0)).cumprod().values
_prov = prices.provisional_actions()
R_ADJ = zero_suspects(returns(close, method="adjusted", vol=vol, actions=_prov))
CUM_ADJ = (1 + R_ADJ.fillna(0)).cumprod().values
out(f"provisional_actions rows (sensitivity run): {len(_prov)}")
OBS = close.notna().values
NROW = len(close)
DATES = close.index

# first formation row: first panel date with at least 20 flow dates strictly before it
I0 = next(i for i in range(NROW) if fdates.searchsorted(DATES[i], "left") >= 20)
_uni = {}


def uni(i):
    if i not in _uni:
        _uni[i] = np.isin(close.columns, liquid_universe(DATES[i], MIN_VALUE))
    return _uni[i]


def build(cum, h, off):
    """Non-overlapping periods: E = I0+off+k*h, X = E+h. Returns dict of arrays."""
    E, rows = I0 + off, []
    while E + h <= NROW - 1:
        X, lm = E + h, uni(E)
        bret, mret, cnt, ucnt = np.full(NS, np.nan), np.full(NS, np.nan), np.zeros(NS, int), np.zeros(NS, int)
        ok = OBS[E] & OBS[X - 4:X + 1].any(axis=0)       # data rule: obs on E, and obs in the 5 rows ending at X
        fwd = cum[X] / cum[E] - 1
        mom = cum[E] / cum[E - 20] - 1
        for k, s in enumerate(SECS):
            ix = col_idx[s]
            ix = ix[lm[ix]]
            ucnt[k] = len(ix)
            ix = ix[ok[ix]]
            cnt[k] = len(ix)
            if len(ix) >= 2:
                bret[k], mret[k] = fwd[ix].mean(), mom[ix].mean()
        tpos = fdates.searchsorted(DATES[E], "left") - 1
        rows.append((E, tpos, bret - np.nanmean(bret), mret - np.nanmean(mret), cnt, ucnt))
        E += h
    return {"E": np.array([r[0] for r in rows]), "T": np.array([r[1] for r in rows]),
            "F": np.array([r[2] for r in rows]), "M": np.array([r[3] for r in rows]),
            "cnt": np.array([r[4] for r in rows]), "ucnt": np.array([r[5] for r in rows]),
            "date": DATES[[r[0] for r in rows]], "h": h}


# ---------------------------------------------------------------- statistics
def rank_mask(a, m):
    x = np.where(m, a, np.inf)
    o = np.argsort(x, axis=1, kind="stable")
    rk = np.empty(o.shape, float)
    np.put_along_axis(rk, o, np.broadcast_to(np.arange(a.shape[1], dtype=float), o.shape), axis=1)
    return np.where(m, rk, np.nan)


def sp_batch(A, B, minn=6):
    m = ~np.isnan(A) & ~np.isnan(B)
    k = m.sum(1)
    ra, rb = rank_mask(A, m), rank_mask(B, m)
    da, db = ra - np.nanmean(ra, 1, keepdims=True), rb - np.nanmean(rb, 1, keepdims=True)
    ic = np.nansum(da * db, 1) / np.sqrt(np.nansum(da ** 2, 1) * np.nansum(db ** 2, 1))
    ic[k < minn] = np.nan
    return ic


def spreads(A, F, sign, minn=6):
    """long top-3 by sign*A minus the mean of all sectors (F is already an excess return), bottom-3 likewise."""
    m = ~np.isnan(A) & ~np.isnan(F)
    k = m.sum(1)
    top = np.argsort(-np.where(m, sign * A, -np.inf), axis=1, kind="stable")[:, :3]
    bot = np.argsort(np.where(m, sign * A, np.inf), axis=1, kind="stable")[:, :3]
    t = np.take_along_axis(F, top, 1).mean(1)
    b = np.take_along_axis(F, bot, 1).mean(1)
    t[k < minn], b[k < minn] = np.nan, np.nan
    return t, b, top


def resid_matrix(S, M):
    """residual of rank(S) regressed on rank(M), per period, over sectors with both present."""
    Rm = np.full(S.shape, np.nan)
    for p in range(len(S)):
        m = ~np.isnan(S[p]) & ~np.isnan(M[p])
        if m.sum() < 6:
            continue
        a, b = rank_mask(S[p:p + 1], m[None])[0, m], rank_mask(M[p:p + 1], m[None])[0, m]
        beta = np.cov(a, b, bias=True)[0, 1] / max(np.var(b), 1e-12)
        Rm[p, m] = a - a.mean() - beta * (b - b.mean())
    return Rm


_perms = {}


def perms(P):
    if P not in _perms:
        rng = np.random.default_rng(0)
        _perms[P] = np.stack([rng.permutation(P) for _ in range(NPERM)])
    return _perms[P]


def placebo(A, F, sign):
    """Permute period labels of F against A. Returns (mean IC array, net top-3 mean spread array)."""
    P = len(A)
    pm = perms(P)
    Fp = F[pm].reshape(-1, NS)
    At = np.tile(A, (NPERM, 1))
    ic = sp_batch(At, Fp).reshape(NPERM, P)
    t, _, _ = spreads(At, Fp, sign if sign else 1)
    return np.nanmean(ic, 1), np.nanmean(t.reshape(NPERM, P) - COST, 1)


def pct_of(plc, x):
    return 100 * np.mean(plc <= x)


def ic_stats(ic, dates, sgn):
    s = sgn if sgn else 1
    v = ~np.isnan(ic)
    x = ic[v]
    n = len(x)
    mean = x.mean() if n else np.nan
    sd = x.std(ddof=1) if n > 1 else np.nan
    yr = np.asarray(dates.year)
    h1, h2 = ic[v & (dates <= "2021-12-31")], ic[v & (dates > "2021-12-31")]
    ybyy = {y: (np.nanmean(ic[v & (yr == y)]) if (v & (yr == y)).sum() else np.nan, int((v & (yr == y)).sum())) for y in YEARS}
    elig = [y for y in YEARS if ybyy[y][1] >= 6]
    return {"n": n, "mean": mean, "median": np.median(x) if n else np.nan, "sd": sd, "t": mean / (sd / np.sqrt(n)) if n > 1 and sd > 0 else np.nan,
            "win": np.mean(x * s > 0) if n else np.nan, "worst": (x * s).min() * s if n else np.nan,
            "h1": h1.mean() if len(h1) else np.nan, "h2": h2.mean() if len(h2) else np.nan,
            "byyear": ybyy, "elig": len(elig), "ysign": sum(1 for y in elig if ybyy[y][0] * s > 0)}


def sp_stats(x):
    x = x[~np.isnan(x)]
    return {"n": len(x), "mean": x.mean(), "median": np.median(x), "win": np.mean(x > 0), "worst": x.min()} if len(x) else {k: np.nan for k in ("n", "mean", "median", "win", "worst")}


def runs(top, valid, Pn):
    """top: (P,3) sector indices; returns total runs, runs of length>=2, longest run (consecutive valid periods)."""
    tot = long_ = longest = 0
    for k in range(NS):
        cur = 0
        for p in range(Pn):
            inn = valid[p] and k in top[p]
            if inn:
                cur += 1
            if (not inn) or p == Pn - 1:
                if cur:
                    tot += 1
                    long_ += cur >= 2
                    longest = max(longest, cur)
                cur = 0
    return tot, long_, longest


# ---------------------------------------------------------------- headline
PER = {h: build(CUM_HEAD, h, 0) for h in (20, 60)}
for h in (20, 60):
    pr = PER[h]
    sec(f"periods, {h}-day horizon, offset 0")
    out(f"n formation dates {len(pr['E'])}; first E {pr['date'][0].date()}, last E {pr['date'][-1].date()}, last exit {DATES[pr['E'][-1] + h].date()}; "
        f"sectors present with a basket (>=2 names) per period: min {int((~np.isnan(pr['F'])).sum(1).min())}, median {np.median((~np.isnan(pr['F'])).sum(1)):.0f}, max {int((~np.isnan(pr['F'])).sum(1).max())}")

sec("basket member counts, 20-day headline periods (offset 0)")
pr = PER[20]
rows = []
for k, s in enumerate(SECS):
    c, u = pr["cnt"][:, k], pr["ucnt"][:, k]
    rows.append([SHORT[s], int(u.min()), f"{np.median(u):.0f}", int(u.max()), int(c.min()), f"{np.median(c):.0f}", int(c.max()), int((c < 2).sum())])
table(["sector", "liquid names min", "median", "max", "basket names (after data rule) min", "median", "max", "sector-periods dropped (<2 names)"], rows)
pr60 = PER[60]
out(f"60-day periods: sector-periods dropped for <2 names: " + ", ".join(f"{SHORT[s]} {int((pr60['cnt'][:, k] < 2).sum())}" for k, s in enumerate(SECS)))
out(f"20-day total dropped sector-periods: {int((pr['cnt'] < 2).sum())} of {pr['cnt'].size}")

RES = {}   # (clip/adj tag, h, g) -> stats


def run_headline(h):
    pr = PER[h]
    res = {}
    for g, sgn in GROUPS.items():
        S = SIG[g][pr["T"]]
        ic = sp_batch(S, pr["F"])
        st = ic_stats(ic, pr["date"], sgn)
        chk = [spearmanr(S[p], pr["F"][p], nan_policy="omit")[0] for p in range(len(S)) if (~np.isnan(S[p]) & ~np.isnan(pr["F"][p])).sum() >= 6]
        st["chk"] = np.nanmax(np.abs(np.array(chk) - ic[~np.isnan(ic)])) if chk else np.nan
        pm, pn = placebo(S, pr["F"], sgn)
        st["plc"] = np.percentile(pm, [5, 50, 95])
        st["pctile"] = pct_of(pm, st["mean"])
        t, b, top = spreads(S, pr["F"], sgn if sgn else 1)
        st.update(S=S, ic=ic, top=top, tg=t, bg=b, pn=pn, pm=pm)
        res[g] = st
    return res


H = {h: run_headline(h) for h in (20, 60)}
sec("check: batch Spearman vs scipy (max abs difference over all periods and groups, 20-day)")
out(f"{max(H[20][g]['chk'] for g in GROUPS):.2e}")

for h in (20, 60):
    sec(f"headline rank IC per investor group, {h}-day non-overlapping, offset 0")
    rows = []
    for g, sgn in GROUPS.items():
        r = H[h][g]
        yrs = f"{r['ysign']}/{r['elig']}"
        rows.append([GL[g], SIGNLBL[sgn], r["n"], f3(r["mean"]), f3(r["median"]), f"{r['t']:+.2f}", f"{100 * r['win']:.0f}%", f3(r["worst"]),
                     f3(r["h1"]), f3(r["h2"]), yrs, f3(r["plc"][0]), f3(r["plc"][1]), f3(r["plc"][2]), f"{r['pctile']:.1f}"])
    table(["group", "sign", "n periods", "mean IC", "median IC", "t", "win rate", "worst IC", "IC 2017-21", "IC 2022-26", "years w/ sign (eligible)",
           "placebo p5", "p50", "p95", "actual pctile"], rows)
    out("win rate = share of periods with IC in the hypothesised direction (IC>0 for exploratory); worst = worst period IC in the hypothesised direction; "
        "years: calendar years with >=6 periods whose mean IC has the hypothesised sign.")

# ---------------------------------------------------------------- momentum control (20d)
sec("momentum-residual IC, 20-day")
pr = PER[20]
rows = []
for g, sgn in GROUPS.items():
    r = H[20][g]
    Rm = resid_matrix(r["S"], pr["M"])
    ic2 = sp_batch(Rm, pr["F"])
    st2 = ic_stats(ic2, pr["date"], sgn)
    pm, _ = placebo(Rm, pr["F"], sgn if sgn else 1)
    r["resid"] = st2["mean"]
    r["resid_pct"] = pct_of(pm, st2["mean"])
    # rank corr of S with momentum itself
    rm_ic = sp_batch(r["S"], pr["M"])
    r["mom_corr"] = np.nanmean(rm_ic)
    rows.append([GL[g], SIGNLBL[sgn], st2["n"], f3(r["mean"]), f3(st2["mean"]), f"{st2['t']:+.2f}", f3(np.percentile(pm, 5)), f3(np.percentile(pm, 50)), f3(np.percentile(pm, 95)),
                 f"{r['resid_pct']:.1f}", f3(r["mom_corr"])])
table(["group", "sign", "n", "raw mean IC", "residual mean IC", "residual t", "placebo p5", "p50", "p95", "residual actual pctile", "avg rank corr of S with trailing 20d excess return"], rows)

# ---------------------------------------------------------------- spreads (20d and 60d)
for h in (20, 60):
    pr = PER[h]
    sec(f"top-3 long-only spread vs EW of all sectors, {h}-day, per group (excess return per period)")
    rows = []
    for g, sgn in GROUPS.items():
        r = H[h][g]
        gro, net = sp_stats(r["tg"]), sp_stats(r["tg"] - COST)
        ls = sp_stats(r["tg"] - r["bg"])
        valid = ~np.isnan(r["tg"])
        tot, long_, longest = runs(r["top"], valid, len(valid))
        r["gro"], r["net"], r["runs"] = gro, net, (tot, long_, longest)
        npl = r["pn"]
        r["spl"] = np.percentile(npl, [5, 50, 95])
        r["spct"] = pct_of(npl, net["mean"])
        rows.append([GL[g] + ("" if sgn >= 0 else " (bottom 3)") + ("" if sgn else " (top 3)"), gro["n"], pc(gro["mean"]), pc(gro["median"]), f"{100 * gro['win']:.0f}%", pc(gro["worst"]),
                     pc(net["mean"]), pc(net["median"]), f"{100 * net['win']:.0f}%", pc(net["worst"]), pc(ls["mean"]), pc(ls["median"]), f"{tot}/{long_}/{longest}"])
    table(["group (leg chosen)", "n", "gross mean", "gross median", "gross win", "gross worst", "net mean", "net median", "net win", "net worst",
           "top3 minus bottom3 gross mean (not tradable)", "L-S gross median", "pick runs total/len>=2/longest"], rows)
    out("net = gross minus 0.5% round trip charged once per period on the long leg; contrarian series (individuals, broker prop) pick the bottom 3 by S.")
    sec(f"placebo for the net top-3 spread mean, {h}-day")
    table(["group", "actual net mean", "placebo p5", "p50", "p95", "actual pctile"],
          [[GL[g], pc(H[h][g]["net"]["mean"], 2), pc(H[h][g]["spl"][0], 2), pc(H[h][g]["spl"][1], 2), pc(H[h][g]["spl"][2], 2), f"{H[h][g]['spct']:.1f}"] for g in GROUPS])

# ---------------------------------------------------------------- by year
sec("by-year mean IC, 20-day headline: mean (number of periods)")
rows = []
for g in MAIN6:
    rows.append([GL[g]] + [("n/a" if H[20][g]["byyear"][y][1] == 0 else f"{H[20][g]['byyear'][y][0]:+.2f} ({H[20][g]['byyear'][y][1]})") for y in YEARS])
table(["group"] + [str(y) for y in YEARS], rows)
sec("by-year mean IC, 60-day headline: mean (number of periods); no year has 6 periods so none is an eligible episode year")
rows = [[GL[g]] + [("n/a" if H[60][g]["byyear"][y][1] == 0 else f"{H[60][g]['byyear'][y][0]:+.2f} ({H[60][g]['byyear'][y][1]})") for y in YEARS] for g in MAIN6]
table(["group"] + [str(y) for y in YEARS], rows)

# ---------------------------------------------------------------- robustness
sec("robustness: start offsets, mean IC across offsets")
OFFS = {20: list(range(20)), 60: [0, 20, 40]}
rows = []
OFFRES = {}
for h in (20, 60):
    per = {o: build(CUM_HEAD, h, o) for o in OFFS[h]}
    out(f"{h}d periods per offset: " + ", ".join(f"{o}:{len(per[o]['E'])}" for o in OFFS[h]))
    for g, sgn in GROUPS.items():
        means = []
        for o in OFFS[h]:
            pr_ = per[o]
            ic = sp_batch(SIG[g][pr_["T"]], pr_["F"])
            means.append(np.nanmean(ic))
        s = sgn if sgn else 1
        OFFRES[(h, g)] = means
        rows.append([f"{h}d", GL[g], SIGNLBL[sgn], len(means), f3(min(means)), f3(np.median(means)), f3(max(means)), f"{sum(m * s > 0 for m in means)}/{len(means)}"])
table(["horizon", "group", "sign", "offsets", "min mean IC", "median", "max", "offsets with hypothesised sign"], rows)
# corporate action sensitivity and clip
sec("robustness: corporate-action sensitivity (adjusted + provisional_actions + suspect zeroing) and block-deal clip, headline mean IC and t")
PERADJ = {h: build(CUM_ADJ, h, 0) for h in (20, 60)}
SENS = {}
rows = []
for h in (20, 60):
    for g, sgn in GROUPS.items():
        base = H[h][g]
        pa = PERADJ[h]
        sa = ic_stats(sp_batch(SIG[g][pa["T"]], pa["F"]), pa["date"], sgn)
        pc_ = PER[h]
        sc = ic_stats(sp_batch(SIGC[g][pc_["T"]], pc_["F"]), pc_["date"], sgn)
        flip_a, flip_c = np.sign(sa["mean"]) != np.sign(base["mean"]), np.sign(sc["mean"]) != np.sign(base["mean"])
        unres = flip_a or abs(sa["t"] - base["t"]) > 1
        SENS[(h, g)] = (sa, sc, flip_a, flip_c, unres)
        rows.append([f"{h}d", GL[g], SIGNLBL[sgn], f3(base["mean"]), f"{base['t']:+.2f}", f3(sa["mean"]), f"{sa['t']:+.2f}", "SIGN FLIP" if flip_a else "same sign",
                     "UNRESOLVED (needs data/corporate_actions.csv)" if unres else "ok", f3(sc["mean"]), f"{sc['t']:+.2f}", "SIGN FLIP" if flip_c else "same sign"])
table(["horizon", "group", "sign", "headline mean IC", "t", "adjusted mean IC", "t", "adjusted vs headline", "label", "clipped mean IC", "t", "clip vs headline"], rows)

# ---------------------------------------------------------------- signal overlap
sec("average cross-sectional rank correlation between group signals, 20-day headline periods")
gl = list(GROUPS)
Mx = np.full((len(gl), len(gl)), np.nan)
for i, a in enumerate(gl):
    for j, b in enumerate(gl):
        Mx[i, j] = 1.0 if i == j else np.nanmean(sp_batch(H[20][a]["S"], H[20][b]["S"]))
table([""] + [GL[g] for g in gl], [[GL[a]] + [f"{Mx[i, j]:+.2f}" for j in range(len(gl))] for i, a in enumerate(gl)])
for g in ["lipi individuals", "lipi mutual funds", "lipi banks / dfi", "lipi broker proprietary trading"]:
    out(f"fipi vs {GL[g]}: {Mx[0, gl.index(g)]:+.2f}")

# ---------------------------------------------------------------- verdict
sec("verdict against rules (a) to (g), 20-day headline")
rows, passers = [], {}
for g, sgn in GROUPS.items():
    r20, r60 = H[20][g], H[60][g]
    sa, sc, flip_a, flip_c, unres = SENS[(20, g)]
    if sgn == 0:
        rows.append([GL[g], "expl.", "-", "-", "-", "-", "-", "-", "-", "exploratory: cannot enter the watch"])
        continue
    s = sgn
    a = r20["mean"] * s > 0 and r20["t"] * s >= 2
    b = (r20["pctile"] >= 95) if s > 0 else (r20["pctile"] <= 5)
    c = r20["h1"] * s > 0 and r20["h2"] * s > 0 and r20["ysign"] >= 6
    d = r20["net"]["median"] > 0 and r20["net"]["win"] > 0.5
    e = r20["resid"] * s > 0 and abs(r20["resid"]) >= 0.5 * abs(r20["mean"])
    f = (not flip_a) and (not flip_c)
    gg = r60["mean"] * s > 0
    allp = all([a, b, c, d, e, f, gg])
    if allp:
        v = "WATCH (candidate)"
        passers[g] = (r20["pctile"] if s > 0 else 100 - r20["pctile"])
    elif a and b and c:
        v = "context, not a trigger"
    else:
        v = "no"
    yn = lambda z: "pass" if z else "fail"
    rows.append([GL[g], SIGNLBL[s], yn(a), yn(b), yn(c), yn(d), yn(e), yn(f), yn(gg), v])
table(["group", "sign", "(a) sign and t>=2", "(b) beyond placebo 95th", "(c) halves and >=6 yrs", "(d) net spread median>0, win>50%", "(e) residual keeps sign, >=half", "(f) sign holds under adj + clip", "(g) 60d same sign", "verdict"], rows)
# collapse mirrored pairs
final = dict(passers)
for a_ in list(passers):
    for b_ in list(passers):
        if a_ < b_ and a_ in final and b_ in final and abs(Mx[gl.index(a_), gl.index(b_)]) >= 0.5:
            drop = a_ if passers[a_] < passers[b_] else b_
            out(f"mirrored pair collapsed: {GL[a_]} and {GL[b_]} (avg rank corr {Mx[gl.index(a_), gl.index(b_)]:+.2f}); kept {GL[b_ if drop == a_ else a_]} (higher directional placebo percentile)")
            final.pop(drop)
out("final weekly-watch list: " + (", ".join(GL[g] for g in final) if final else "none"))
out("Multiple testing: 9 series x 2 horizons (x IC and spread statistics): 1 to 2 false passes at 5% are expected by chance alone.")

# ---------------------------------------------------------------- H4
sec("H4 market-level foreign selling, setup")
f = pd.read_csv(ROOT / "data" / "macro" / "fipi_lipi.csv", parse_dates=["date"])
fo = f[f.investor_type.isin(["foreign corporates", "foreign individual", "overseas pakistani"])].groupby("date").net_usd_mn.sum()
tot = f.groupby("date").buy_usd_mn.sum()
fo = fo.reindex(tot.index).fillna(0.0)
scaled = (fo.rolling(60).sum() / tot.rolling(60).sum())
vals = scaled.values
kse = pd.read_csv(ROOT / "data" / "macro" / "kse100.csv", parse_dates=["date"]).set_index("date").close
kmi = pd.read_csv(ROOT / "data" / "macro" / "kmiallshr.csv", parse_dates=["date"]).set_index("date").close
kmi_a = kmi.reindex(kse.index, method="ffill")
out(f"fipi_lipi.csv: {len(tot)} flow dates, {tot.index[0].date()} to {tot.index[-1].date()}; scaled 60-day FIPI net / gross buy, first valid {scaled.first_valid_index().date()}")
out(f"KSE100 rows {len(kse)}, {kse.index[0].date()} to {kse.index[-1].date()}; KMI All Share rows {len(kmi)}, KSE100 dates missing from KMI series (forward-filled): {int((~kse.index.isin(kmi.index)).sum())}")
trig = []
first_valid = int(np.argmax(~np.isnan(vals)))
for p in range(first_valid + 250, len(vals)):
    if not np.isnan(vals[p]) and vals[p] <= np.quantile(vals[first_valid:p], 0.10):
        trig.append(p)
out(f"first possible trigger date {tot.index[first_valid + 250].date()}; trigger days {len(trig)}")
kidx = kse.index
krow = lambda d: kidx.searchsorted(d, "right") - 1     # last KSE row on or before d
eps, last, clus = [], None, []
for p in trig:
    r_ = krow(tot.index[p])
    if last is None or r_ - last > 60:
        eps.append(p)
        clus.append([0, p])
    clus[-1][0] += 1
    clus[-1][1] = p
    last = r_
kv, mv = kse.values, kmi_a.values


def fwd(arr, e, n):
    return arr[e + n] / arr[e] - 1 if e + n < len(arr) else np.nan


def ddn(arr, e):
    return arr[e:e + 121].min() / arr[e] - 1 if e + 120 < len(arr) else np.nan


def bottom(e):
    if e - 60 < 0 or e + 120 >= len(kv):
        return np.nan
    w = kv[e - 60:e + 121]
    return float(abs(int(np.argmin(w)) - 60) <= 20)


sec("H4 episode list (mechanical rule: scaled 60-day FIPI net <= expanding 10th percentile; new episode after 60 KSE rows without a trigger)")
rows, E_list = [], []
for p in eps:
    T = tot.index[p]
    e = krow(T) + 1
    E_list.append(e)
    b = bottom(e)
    rows.append([T.date(), kidx[e].date(), f"{vals[p]:+.4f}", pc(fwd(kv, e, 60)), pc(fwd(kv, e, 120)), pc(fwd(mv, e, 60)), pc(fwd(mv, e, 120)),
                 pc(ddn(kv, e)), "n/a (window incomplete)" if np.isnan(b) else ("yes" if b else "no")])
table(["trigger date T", "entry E (close)", "scaled signal", "KSE100 fwd 60d", "KSE100 fwd 120d", "KMI All Share fwd 60d", "KMI fwd 120d", "KSE100 worst drawdown within 120d", "marked bottom (KSE100 min within 20 rows of E)"], rows)
out("trigger clusters (episode first trigger -> last trigger in the same cluster, trigger days): " + "; ".join(f"{tot.index[e].date()} -> {tot.index[c[1]].date()}, {c[0]} days" for e, c in zip(eps, clus)))
out(f"episodes: {len(eps)}. Where the rule fires: 2017-2019: " + (", ".join(str(tot.index[p].date()) for p in eps if tot.index[p].year <= 2019) or "none")
    + "; 2021-2022: " + (", ".join(str(tot.index[p].date()) for p in eps if tot.index[p].year in (2021, 2022)) or "none"))
E_arr = np.array(E_list)
sec("H4 summary vs random-entry placebo and unconditional windows")
elig_lo = krow(tot.index[first_valid + 250]) + 1
elig_hi = len(kv) - 1 - 120
elig = np.arange(elig_lo, elig_hi + 1)
F60k, F120k = np.array([fwd(kv, e, 60) for e in elig]), np.array([fwd(kv, e, 120) for e in elig])
F60m, F120m = np.array([fwd(mv, e, 60) for e in elig]), np.array([fwd(mv, e, 120) for e in elig])
BOT = np.array([bottom(e) for e in elig])


def summ(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    return [len(x), pc(x.mean()), pc(np.median(x)), f"{100 * np.mean(x > 0):.0f}%", pc(x.min())] if len(x) else [0, "n/a", "n/a", "n/a", "n/a"]


rows = []
for lab, arr_, n in (("KSE100 fwd 60d", kv, 60), ("KSE100 fwd 120d", kv, 120), ("KMI All Share fwd 60d", mv, 60), ("KMI All Share fwd 120d", mv, 120)):
    rows.append([lab, "episodes"] + summ([fwd(arr_, e, n) for e in E_arr]))
    # unconditional non-overlapping windows over the eligible period
    rows.append([lab, f"all non-overlapping {n}-day windows, eligible period"] + summ([fwd(arr_, e, n) for e in range(elig_lo, len(arr_) - 1 - n + 1, n)]))
table(["series", "sample", "n", "mean", "median", "win rate", "worst"], rows)
rng = np.random.default_rng(0)
nep = len(E_arr)
dr = [rng.choice(len(elig), size=nep, replace=False) for _ in range(NPERM)] if nep else []
if nep:
    m60k = np.array([np.median(F60k[d]) for d in dr]); m120k = np.array([np.median(F120k[d]) for d in dr])
    m60m = np.array([np.median(F60m[d]) for d in dr]); m120m = np.array([np.median(F120m[d]) for d in dr])
    hit = np.array([np.nanmean(BOT[d]) for d in dr])
    act = lambda arr_, n: np.nanmedian([fwd(arr_, e, n) for e in E_arr])
    actb = np.nanmean([bottom(e) for e in E_arr])
    out(f"\nrandom-entry placebo: {NPERM} draws of {nep} entry dates (no replacement) from E rows {kidx[elig_lo].date()} to {kidx[elig_hi].date()} (full 120-day forward window), seed 0")
    rows = []
    for lab, pl, a_ in (("KSE100 median fwd 60d", m60k, act(kv, 60)), ("KSE100 median fwd 120d", m120k, act(kv, 120)), ("KMI median fwd 60d", m60m, act(mv, 60)),
                        ("KMI median fwd 120d", m120m, act(mv, 120)), ("bottom-hit rate (KSE100)", hit, actb)):
        isb = "bottom" in lab
        fm = (lambda x: f"{100 * x:.0f}%") if isb else pc
        rows.append([lab, fm(a_), fm(np.percentile(pl, 5)), fm(np.percentile(pl, 50)), fm(np.percentile(pl, 95)), f"{pct_of(pl, a_):.1f}"])
    table(["statistic", "episodes (actual)", "placebo p5", "p50", "p95", "actual pctile"], rows)
    out(f"bottom-hit rate among eligible entry rows (all rows): {np.nanmean(BOT):.0%}")
out(f"H4 verdict: {len(eps)} episodes; " + ("fewer than 5 episodes: ANECDOTE whatever the numbers say." if len(eps) < 5 else "5 or more episodes."))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(LOG), encoding="utf-8")
