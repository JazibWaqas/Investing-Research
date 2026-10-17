"""Value with true publication dates (redo of the seed value test).
Run: .venv/Scripts/python.exe scripts/tests/value_timestamped.py
Prints and saves tests/out/value_timestamped.txt. Write-up: tests/value_timestamped.md.
Spec: one formation date a year (last panel day of October), fundamentals = latest fiscal year whose first
tradable session is on or before it, E/P rescaled to the formation price, 12m price return to the next October."""
import sys, io, re, calendar
from datetime import time as dtime
from pathlib import Path
import numpy as np, pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
def pc(x, d=1): return "nan" if pd.isna(x) else f"{x*100:+.{d}f}"   # return as signed percent points

COST_RT, COST_SPREAD = 0.005, 0.010
NDRAW, SEED = 2000, 20261017
FORM_YEARS = [2021, 2022, 2023, 2024, 2025]
MIN_ELIG_2021 = 30

# ------------------------------------------------------------------ data
close_raw, vol, tv = P.load_panel()
pp = pd.read_parquet(ROOT / "data/panel_close_adj_pricereturn.parquet")      # bonus/split adjusted, price only
pt = pd.read_parquet(ROOT / "data/panel_close_adj.parquet")                   # plus cash dividends (partial before Nov 2024)
days = pp.index
pf, ptf = pp.ffill(), pt.ffill()
LAST = days[-1]

sa = pd.read_csv(ROOT / "seed/data/fundamentals/sa_ratios.csv")
sa["t"] = sa.t.str.replace(r"(XD|XB|XR)$", "", regex=True)                     # lesson 14 (no such rows in practice)
names = sorted(sa.t.unique())
fy = sa[sa.date != "TTM"].copy()
fy["fye"] = pd.to_datetime(fy.date)
scr = pd.read_csv(ROOT / "seed/data/fundamentals/screener_20261016.csv")
scr["b"] = scr.symbol.str.replace(r"(XD|XB|XR)$", "", regex=True)
sector = scr[scr.b.isin(names)].drop_duplicates("b").set_index("b").sector.astype(int)

out(f"Value with true publication dates. Run date 2026-10-17. Panel {len(days)} days {days[0].date()} to {LAST.date()}.")
out(f"sa_ratios: {len(names)} names, {len(fy)} fiscal-year rows (TTM dropped); pe blank {fy.pe.isna().sum()}, "
    f"of which roe<0 {((fy.pe.isna()) & (fy.roe < 0)).sum()}, roe>0 {((fy.pe.isna()) & (fy.roe > 0)).sum()}; "
    f"all names in panel: {all(n in pp.columns for n in names)}; sector codes {sector.nunique()}")

# ------------------------------------------------------------------ publication timestamps
MONTH = {m.lower()[:3]: i for i, m in enumerate(calendar.month_name) if m}
def parse_period(title):
    t = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", title.lower().replace("revoked", ""))
    m = re.search(r"year\s+ended(.*)", t)
    if not m: return None
    r = m.group(1)
    try:
        if (x := re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", r)): return pd.Timestamp(int(x[1]), int(x[2]), int(x[3]))
        if (x := re.search(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", r)):
            a, b, y = int(x[1]), int(x[2]), int(x[3])
            d, mo = (a, b) if (a > 12 or b <= 12) else (b, a)
            return pd.Timestamp(y, mo, d)
        if (x := re.search(r"([a-z]{3,9})\.?\s*(\d{1,2})\s*,?\s*(\d{4})", r)) and x[1][:3] in MONTH:
            return pd.Timestamp(int(x[3]), MONTH[x[1][:3]], int(x[2]))
        if (x := re.search(r"(\d{1,2})\s*([a-z]{3,9})\.?,?\s*(\d{4})", r)) and x[2][:3] in MONTH:
            return pd.Timestamp(int(x[3]), MONTH[x[2][:3]], int(x[1]))
    except ValueError:
        return None
    return None

ann = pd.read_parquet(ROOT / "data/announcements.parquet")
ann["symbol"] = ann.symbol.str.replace(r"(XD|XB|XR)$", "", regex=True).where(
    ~ann.symbol.isin(names) & ann.symbol.str.replace(r"(XD|XB|XR)$", "", regex=True).isin(names), ann.symbol)
a = ann[(ann.klass == "financial_result") & ann.symbol.isin(names)].copy()
tl = a.title.str.lower()
a = a[tl.str.contains(r"year\s+ended") & ~tl.str.contains(r"half|quarter|six month|nine month|3rd|9 month|qtr")]
n_all_annual = len(a)
a = a[~a.title.str.contains("revoked", case=False)]
a["pend"] = a.title.map(parse_period)
out(f"Annual-result announcements for the 108 names: {n_all_annual}; after dropping REVOKED {len(a)}; period end unparsed {a.pend.isna().sum()}")
a = a.dropna(subset=["pend"])
a["dt"] = a.datetime
a["lag"] = (a.dt.dt.tz_localize(None).dt.normalize() - a.pend).dt.days

q = pd.read_csv(ROOT / "data/fundamentals/quarterly_eps.csv")
q["fq"] = pd.to_datetime(q.fiscal_quarter_end)
q["ad"] = pd.to_datetime(q.announce_dt, utc=True).dt.tz_convert("Asia/Karachi")

def first_tradable(ts):
    d = ts.tz_localize(None).normalize() if ts.tzinfo is None else ts.tz_convert("Asia/Karachi").tz_localize(None).normalize()
    local = ts.tz_convert("Asia/Karachi") if ts.tzinfo is not None else ts
    side = "left" if local.time() <= dtime(15, 30) else "right"
    k = days.searchsorted(d, side=side)
    return days[k] if k < len(days) else pd.NaT

rows = []
for r in fy.itertuples():
    g = a[(a.symbol == r.t) & (a.pend == r.fye) & a.lag.between(0, 150)]
    src, ts = "none", pd.NaT
    if len(g):
        ts, src = g.dt.min(), "announcement"
    elif r.fye.month == 6 and r.fye.day == 30:
        h = q[(q.symbol == r.t) & (q.fq == r.fye) & q.ad.notna()]
        if len(h):
            lag = (h.ad.iloc[0].tz_localize(None).normalize() - r.fye).days
            if 0 <= lag <= 150: ts, src = h.ad.iloc[0], "quarterly_eps"
            else: src = "none_qeps_outside_window"
    rows.append((r.t, r.fye, src, ts, first_tradable(ts) if src in ("announcement", "quarterly_eps") else pd.NaT))
pub = pd.DataFrame(rows, columns=["t", "fye", "src", "ts", "ftd"])
fy = fy.merge(pub, on=["t", "fye"])
out(f"\n== Publication timestamps, {len(fy)} fiscal-year rows")
out(fy.src.value_counts().to_string())
m = fy[fy.src == "announcement"]
out(f"announcement lag from FYE, days: median {m.ts.dt.tz_localize(None).sub(m.fye).dt.days.median():.0f}, "
    f"min {m.ts.dt.tz_localize(None).sub(m.fye).dt.days.min()}, max {m.ts.dt.tz_localize(None).sub(m.fye).dt.days.max()}; "
    f"timestamps at exactly 00:00: {(m.ts.dt.hour.eq(0) & m.ts.dt.minute.eq(0)).sum()}; after 15:30: {(m.ts.dt.time > dtime(15, 30)).sum()}")
out("rows by FYE month: " + fy.fye.dt.month.value_counts().sort_index().to_dict().__str__())

# ------------------------------------------------------------------ cohorts
def oct_last(y): return days[(days.year == y) & (days.month == 10)][-1]
fy_by = {t: g.sort_values("fye") for t, g in fy.groupby("t")}
mom_names = names

def build(Fy, liq=True):
    """-> (eligible df, accounting dict) for formation year Fy."""
    F = oct_last(Fy)
    E = oct_last(Fy + 1) if Fy + 1 <= 2026 else LAST
    if Fy + 1 == 2026: E = LAST
    liquid = set(P.liquid_universe(F, 5e6))
    iF = days.get_loc(F)
    recent = pp.iloc[iF - 9:iF + 1].notna().any()
    rec, acc = [], dict(F=F, E=E, universe=len(names), no_pub=0, stale=0, no_ey=0, no_price=0, liq_removed=0)
    for t in names:
        g = fy_by.get(t)
        g = g[g.ftd.notna() & (g.ftd <= F)] if g is not None else None
        if g is None or not len(g): acc["no_pub"] += 1; continue
        r = g.iloc[-1]
        if (F - r.fye).days > 548: acc["stale"] += 1; continue          # 18 months
        pe, roe, pb = r.pe, r.roe, r.pb
        if pd.notna(pe) and pe > 0: ey, srcy = 1 / pe, "pe"
        elif pd.notna(roe) and pd.notna(pb) and pb > 0: ey, srcy = roe / pb, "roe_pb"
        else: acc["no_ey"] += 1; continue
        pfye, pform = pf.loc[:r.fye, t].iloc[-1] if r.fye >= days[0] else np.nan, pf.loc[F, t]
        if not recent[t] or pd.isna(pfye) or pd.isna(pform): acc["no_price"] += 1; continue
        rec.append(dict(t=t, sector=sector[t], fye=r.fye, ftd=r.ftd, ey_fye=ey, src=srcy, roe=roe,
                        ey=ey * pfye / pform, liquid=t in liquid,
                        ret=pf.loc[E, t] / pform - 1, ret_t=ptf.loc[E, t] / ptf.loc[F, t] - 1))
    df = pd.DataFrame(rec)
    acc["pre_liq"] = len(df)
    if len(df):
        acc["liq_removed"] = int((~df.liquid).sum())
        if liq: df = df[df.liquid]
    acc["eligible"] = len(df)
    acc["fallback"] = int((df.src == "roe_pb").sum()) if len(df) else 0
    acc["lossmakers"] = int((df.ey < 0).sum()) if len(df) else 0
    return df.reset_index(drop=True), acc

# ------------------------------------------------------------------ tests
def pct_rank(x): return x.rank(method="average") / len(x)

def units_for(df, test, F):
    """-> (subset index array, list of unit index arrays). Rank and shuffle happen inside each unit."""
    if test == "T1": return [np.arange(len(df))]
    if test == "T2":
        vc = df.sector.value_counts()
        return [np.flatnonzero((df.sector == s).values) for s in vc[vc >= 3].index]
    if test == "T3":
        med = df.roe.median()
        return [np.flatnonzero((df.roe > med).values)]
    if test == "T4":
        sub = mom_sectors(F, df)
        return [np.flatnonzero(df.sector.isin(sub).values)]

def mom_sectors(F, df):
    """sectors (>=3 of the 108 names with a 6m return) in the top half by equal-weight 6m price return to F."""
    F0 = F - pd.DateOffset(months=6)
    p0, p1 = pf.loc[:F0].iloc[-1], pf.loc[F]
    r = (p1 / p0 - 1)[mom_names].dropna()
    s = pd.DataFrame({"r": r, "s": sector.reindex(r.index)})
    g = s.groupby("s").r.agg(["mean", "count"])
    g = g[g["count"] >= 3]
    return list(g.index[g["mean"] >= g["mean"].median()])

def labels(df, units):
    lab = np.full(len(df), "", dtype=object)
    for u in units:
        p = pct_rank(df.ey.iloc[u])
        lab[u] = np.where(p > 2 / 3, "top", np.where(p <= 1 / 3, "bot", "mid"))
    return lab

def stats(df, lab, ret_col, univ):
    r = df[ret_col].values
    top, bot, mid = r[lab == "top"], r[lab == "bot"], r[lab == "mid"]
    if len(top) == 0 or len(bot) == 0: return None
    um = np.nanmean(univ)
    o = dict(n_top=len(top), n_mid=len(mid), n_bot=len(bot), m_top=np.nanmean(top), m_mid=np.nanmean(mid) if len(mid) else np.nan,
             m_bot=np.nanmean(bot), med_top=np.nanmedian(top), med_bot=np.nanmedian(bot), univ=um,
             win=np.mean(top > um), worst=np.nanmin(top), worst_t=df.t[lab == "top"].values[np.nanargmin(top)])
    o["sp_mean"], o["sp_med"] = o["m_top"] - o["m_bot"], o["med_top"] - o["med_bot"]
    o["sp_net"] = o["sp_mean"] - COST_SPREAD
    o["tu_net"] = o["m_top"] - um - COST_RT
    o["tu_gross"] = o["m_top"] - um
    return o

TESTS = ["T1", "T2", "T3", "T4"]
def run(dfs, ret_col="ret", fall=False):
    """dfs: {year: df}. -> {test: {year: stats}}, plus the unit structures for placebo."""
    res, un = {t: {} for t in TESTS}, {t: {} for t in TESTS}
    for y, df in dfs.items():
        F = oct_last(y)
        univ = df[ret_col].values
        for t in TESTS:
            us = units_for(df, t, F)
            lab = labels(df, us)
            s = stats(df, lab, ret_col, univ)
            if s is None: continue
            res[t][y] = s
            un[t][y] = (us, lab)
    return res, un

def placebo(dfs, un, ret_col="ret", rng=None):
    """Shuffle returns inside each unit (equivalent to shuffling ey), keep tercile masks, 2000 draws.
    -> {test: array of mean-across-cohort gross spreads}"""
    out_ = {}
    for t in TESTS:
        ys = list(un[t])
        if not ys: continue
        draws = np.zeros((NDRAW, len(ys)))
        for j, y in enumerate(ys):
            r = dfs[y][ret_col].values
            us, lab = un[t][y]
            topm, botm = lab == "top", lab == "bot"
            for d in range(NDRAW):
                rr = r.copy()
                for u in us:
                    rr[u] = r[u][rng.permutation(len(u))]
                draws[d, j] = rr[topm].mean() - rr[botm].mean()
        out_[t] = draws.mean(axis=1)
    return out_

def summarize(res, plc, label):
    out(f"\n--- Across cohorts: {label}")
    out("test | N | mean gross | median gross | mean net | median net | k+ net | worst cohort net | mean top-univ net | k+ | placebo gross med / p5 / p95 | p (share >= actual)")
    S = {}
    for t in TESTS:
        ys = list(res[t])
        if not ys: out(t, "no cohorts"); continue
        g = np.array([res[t][y]["sp_mean"] for y in ys]); n = g - COST_SPREAD
        tu = np.array([res[t][y]["tu_net"] for y in ys])
        pl = plc[t]; p = (pl >= g.mean()).mean()
        S[t] = dict(g=g, net=n, tu=tu, ys=ys, kpos=int((n > 0).sum()), N=len(ys), p=p, p5=np.percentile(pl, 5), p50=np.median(pl), p95=np.percentile(pl, 95))
        out(f"{t} | {len(ys)} | {pc(g.mean())} | {pc(np.median(g))} | {pc(n.mean())} | {pc(np.median(n))} | {int((n>0).sum())} of {len(ys)} | {pc(n.min())} | {pc(tu.mean())} | {int((tu>0).sum())} of {len(ys)} | "
            f"{pc(S[t]['p50'])} / {pc(S[t]['p5'])} / {pc(S[t]['p95'])} | {p:.3f}")
    return S

# ------------------------------------------------------------------ build cohorts
out("\n== Sample accounting (sequential: names removed at each step; main run applies the Rs5m liquidity filter)")
out("year | F | outcome end | names | no published FY | stale (>18m) | no ey (pe and roe/pb blank) | no price/not traded in 10d | = before liquidity | liquidity removed | eligible | roe/pb fallback | loss-makers kept (ey<0)")
dfs_main, dfs_nol, accs = {}, {}, {}
for y in FORM_YEARS:
    d_l, ac = build(y, True); d_n, ac_n = build(y, False)
    accs[y] = ac
    out(f"{y} | {ac['F'].date()} | {ac['E'].date()} | {ac['universe']} | {ac['no_pub']} | {ac['stale']} | {ac['no_ey']} | {ac['no_price']} | {ac['pre_liq']} | {ac['liq_removed']} | {ac['eligible']} | {ac['fallback']} | {ac['lossmakers']}")
    dfs_main[y], dfs_nol[y] = d_l, d_n
used = [y for y in FORM_YEARS if accs[y]["eligible"] >= (MIN_ELIG_2021 if y == 2021 else 1)]
for y in FORM_YEARS:
    if y not in used: out(f"Cohort Oct {y} SKIPPED: {accs[y]['eligible']} eligible names (< {MIN_ELIG_2021}).")
dfs_main = {y: dfs_main[y] for y in used}; dfs_nol = {y: dfs_nol[y] for y in used}
for y in used:
    d = dfs_main[y]; sc = d.sector.value_counts()
    thin = int(d.sector.map(sc).lt(3).sum())
    out(f"Oct {y}: thin-sector names excluded from T2 {thin} (sectors with >=3 eligible: {int((sc>=3).sum())}); fiscal-year mix: "
        f"{d.fye.dt.month.value_counts().sort_index().to_dict()}; roe/pb fallback {int((d.src=='roe_pb').sum())}; "
        f"ey_form median {d.ey.median():.3f}; T4 top-half sectors: {mom_sectors(oct_last(y), d)}")
out("Oct 2025 cohort is PARTIAL: ends 2026-10-16, 11.5 months.")

# ------------------------------------------------------------------ main results
rng = np.random.default_rng(SEED)
res, un = run(dfs_main)
plc = placebo(dfs_main, un, rng=rng)
for t in TESTS:
    out(f"\n== {t} by cohort (price return, 12m, gross unless marked net; returns in percent)")
    out("cohort | n top/mid/bot | mean top / mid / bot | median top / bot | universe mean (n) | win rate | worst top (name) | spread mean | spread median | spread net 1.0 | top-univ net 0.5")
    for y, s in res[t].items():
        out(f"Oct {y}{' (partial)' if y==2025 else ''} | {s['n_top']}/{s['n_mid']}/{s['n_bot']} | {pc(s['m_top'])} / {pc(s['m_mid'])} / {pc(s['m_bot'])} | {pc(s['med_top'])} / {pc(s['med_bot'])} | "
            f"{pc(s['univ'])} ({len(dfs_main[y])}) | {s['win']*100:.0f}% | {pc(s['worst'])} ({s['worst_t']}) | {pc(s['sp_mean'])} | {pc(s['sp_med'])} | {pc(s['sp_net'])} | {pc(s['tu_net'])}")
S = summarize(res, plc, "MAIN (liquidity filter, price return)")
ys = used
out("\nPlacebo: shuffle ey_form across the same eligible names (within sector for T2, within subset for T3/T4), 2,000 draws, seed", SEED)

# T4 momentum baseline
out("\n== T4 momentum-only baseline (all eligible names in top-half sectors minus eligible universe) vs T4 value spread")
out("cohort | n in top-half sectors / eligible | momentum EW mean | universe mean | momentum minus universe gross | net 0.5 | T4 value spread gross | T4 value spread net 1.0 | T4 top-tercile minus universe net")
for y in ys:
    d = dfs_main[y]; us = units_for(d, "T4", oct_last(y))[0]
    mm, um = d.ret.values[us].mean(), d.ret.mean()
    s4 = res["T4"][y]
    out(f"Oct {y} | {len(us)}/{len(d)} | {pc(mm)} | {pc(um)} | {pc(mm-um)} | {pc(mm-um-COST_RT)} | {pc(s4['sp_mean'])} | {pc(s4['sp_net'])} | {pc(s4['tu_net'])}")
mo = np.array([dfs_main[y].ret.values[units_for(dfs_main[y], 'T4', oct_last(y))[0]].mean() - dfs_main[y].ret.mean() for y in ys])
out(f"mean momentum-only minus universe, gross {pc(mo.mean())}, net {pc(mo.mean()-COST_RT)}; mean T4 value spread gross {pc(S['T4']['g'].mean())}, net {pc(S['T4']['net'].mean())}")

# ------------------------------------------------------------------ total return
out("\n== Total return (panel_close_adj, cash dividends complete only from Nov 2024) beside price return, Oct 2024 and Oct 2025 cohorts only")
tdfs = {y: dfs_main[y] for y in (2024, 2025) if y in dfs_main}
rest, _ = run(tdfs, "ret_t")
out("cohort | test | price: top / bottom / spread | total: top / bottom / spread | total spread net 1.0 | universe mean price / total")
for y in tdfs:
    for t in TESTS:
        sp, st = res[t][y], rest[t][y]
        out(f"Oct {y} | {t} | {pc(sp['m_top'])} / {pc(sp['m_bot'])} / {pc(sp['sp_mean'])} | {pc(st['m_top'])} / {pc(st['m_bot'])} / {pc(st['sp_mean'])} | {pc(st['sp_net'])} | {pc(sp['univ'])} / {pc(st['univ'])}")

# ------------------------------------------------------------------ regression
out("\n== Year-fixed-effects regression: 12m price return on within-cohort percentile rank of ey_form (0 to 1), cohort dummies")
big = pd.concat([d.assign(cohort=y, rk=pct_rank(d.ey)) for y, d in dfs_main.items()], ignore_index=True)
big["rk_sec"] = np.nan
for y, d in dfs_main.items():
    vc = d.sector.value_counts()
    idx = big.index[(big.cohort == y)]
    for s in vc[vc >= 3].index:
        ii = idx[(d.sector == s).values]
        big.loc[ii, "rk_sec"] = pct_rank(big.loc[ii, "ey"]).values
def reg(x, data, label):
    d = data.dropna(subset=[x])
    X = pd.concat([d[[x]], pd.get_dummies(d.cohort, prefix="c", drop_first=False).astype(float)], axis=1)
    m = sm.OLS(d.ret.values, X.values).fit()
    k1 = m.get_robustcov_results("cluster", groups=pd.factorize(d.t)[0])
    k2 = m.get_robustcov_results("cluster", groups=d.cohort.values)
    out(f"{label}: n {len(d)}, slope {k1.params[0]*100:+.1f} pts per full rank (bottom to top), ticker-clustered t {k1.tvalues[0]:.2f} ({d.t.nunique()} clusters), "
        f"cohort-clustered t {k2.tvalues[0]:.2f} ({d.cohort.nunique()} clusters: UNRELIABLE, 4 clusters)")
reg("rk", big, "overall rank")
reg("rk_sec", big, "within-sector rank (sectors >=3)")

# ------------------------------------------------------------------ monthly
out("\n== Monthly non-overlapping check: EW monthly return of fixed formation-date top and bottom terciles, held 12 months")
me = pd.Series(days, days).groupby(days.to_period("M")).last()
def monthly(dfs, un, t):
    sp = []
    for y in dfs:
        F, E = oct_last(y), accs[y]["E"]
        d = dfs[y]; us, lab = un[t][y]
        ends = [x for x in me if F < x <= E]
        if E == LAST: ends = [x for x in ends if x.to_period("M") != E.to_period("M")]   # drop the 1-16 Oct stub
        prev = F
        for x in ends:
            r = pf.loc[x, d.t].values / pf.loc[prev, d.t].values - 1
            sp.append((y, x, np.nanmean(r[lab == "top"]) - np.nanmean(r[lab == "bot"])))
            prev = x
    return pd.DataFrame(sp, columns=["y", "m", "sp"])
for t in ("T1", "T2"):
    mdf = monthly(dfs_main, un, t); s = mdf.sp
    w = mdf.loc[s.idxmin()]
    out(f"{t}: months {len(s)}, mean spread {pc(s.mean(), 2)} pts/month, median {pc(s.median(), 2)}, t {s.mean()/(s.std()/np.sqrt(len(s))):.2f}, "
        f"worst month {pc(s.min())} ({w.m.date()}); by cohort mean {({int(y): round(float(v)*100,2) for y, v in mdf.groupby('y').sp.mean().items()})}")
out("Months within a cohort share one portfolio: do not read this t as more than four independent episodes.")

# ------------------------------------------------------------------ outlier robustness
out("\n== ROBUSTNESS: outliers. Largest eligible 12m return per cohort, and spreads with returns winsorised at the cohort 5th/95th percentile")
for y in used:
    d = dfs_main[y]; i = d.ret.idxmax()
    out(f"Oct {y}: max {pc(d.ret[i])} ({d.t[i]}, ey rank {pct_rank(d.ey)[i]:.2f}); universe mean {pc(d.ret.mean())}, excluding the max {pc(d.ret.drop(i).mean())}; median {pc(d.ret.median())}")
dfs_w = {y: d.assign(retw=d.ret.clip(d.ret.quantile(.05), d.ret.quantile(.95))) for y, d in dfs_main.items()}
res_w, un_w = run(dfs_w, "retw"); plc_w = placebo(dfs_w, un_w, "retw", rng=np.random.default_rng(SEED + 3))
Sw = summarize(res_w, plc_w, "WINSORISED RETURNS (5/95 within cohort)")
out("Per-cohort winsorised net spreads (pts) T1 / T2 / T3 / T4:")
for y in used:
    out(f"Oct {y}: " + " / ".join(pc(res_w[t][y]["sp_net"]) for t in TESTS))

# ------------------------------------------------------------------ sensitivities
out("\n== SENSITIVITY: no liquidity filter")
for y in used: out(f"Oct {y}: eligible {len(dfs_nol[y])} (with filter {len(dfs_main[y])})")
res_n, un_n = run(dfs_nol); plc_n = placebo(dfs_nol, un_n, rng=np.random.default_rng(SEED + 1))
Sn = summarize(res_n, plc_n, "NO LIQUIDITY FILTER")
out("\n== SENSITIVITY: roe/pb fallback rows dropped (liquidity filter on)")
dfs_nf = {y: d[d.src == "pe"].reset_index(drop=True) for y, d in dfs_main.items()}
for y in used: out(f"Oct {y}: eligible {len(dfs_nf[y])} (with fallback rows {len(dfs_main[y])})")
res_f, un_f = run(dfs_nf); plc_f = placebo(dfs_nf, un_f, rng=np.random.default_rng(SEED + 2))
Sf = summarize(res_f, plc_f, "FALLBACK ROWS DROPPED (loss-makers with a blank pe are gone)")
out("\nPer-cohort net spreads (pts) for the sensitivities, T1 / T2 / T3 / T4:")
for nm, rr in (("main", res), ("no liq", res_n), ("no fallback", res_f)):
    for y in used:
        out(f"{nm} Oct {y}: " + " / ".join(pc(rr[t][y]["sp_net"]) if y in rr[t] else "n/a" for t in TESTS) + "  (n " + "/".join(str(rr[t][y]['n_top']+rr[t][y]['n_mid']+rr[t][y]['n_bot']) if y in rr[t] else "-" for t in TESTS) + ")")

# ------------------------------------------------------------------ verdict
out("\n== PRE-REGISTERED VERDICT")
N = len(used)
need = 3 if N == 4 else int(np.ceil(0.75 * N))
t1, t2 = S["T1"], S["T2"]
stand = t1["kpos"] >= need and t2["kpos"] >= need and (t1["net"].mean() - COST_SPREAD * 0 > t1["p95"] - COST_SPREAD) and (t2["net"].mean() > t2["p95"] - COST_SPREAD)
tieb = t2["kpos"] >= need and t2["net"].mean() > t2["p50"] - COST_SPREAD
out(f"Independent episodes (cohorts with outcome): {N}; required positive cohorts: {need}")
out(f"T1 net spread positive in {t1['kpos']} of {N}; mean net {pc(t1['net'].mean())}; placebo net 95th pct {pc(t1['p95']-COST_SPREAD)}, p {t1['p']:.3f}")
out(f"T2 net spread positive in {t2['kpos']} of {N}; mean net {pc(t2['net'].mean())}; placebo net median {pc(t2['p50']-COST_SPREAD)}, 95th pct {pc(t2['p95']-COST_SPREAD)}, p {t2['p']:.3f}")
verdict = "STANDALONE EDGE" if stand else "TIEBREAKER" if tieb else "NOTHING"
out(f"Rule result: {verdict}. With 4 episodes a standalone verdict cannot be reached at conventional confidence whatever the point estimate.")
open(ROOT / "tests/out/value_timestamped.txt", "w", encoding="utf-8").write(buf.getvalue())
