"""compounders: which PSX businesses compounded, what was visible early, does a growth-core rule beat the index.
Run: .venv/Scripts/python.exe scripts/tests/compounders.py  -> tests/out/compounders.txt   Write-up: tests/compounders.md

PRE-REGISTERED (fixed before any result was seen; not tuned)
 A  Population: total return (dividends reinvested) over every 5-year window starting on a month-end from 2016-12-30,
    and over the decade (2016-12-30 to the last date). Names must be liquid at the window start (60-day median traded
    value > Rs5m). Survivors, 55 listed names missing from the panel, and delisted names are all included.
 B  Early features, 5-year 3x names vs same-cohort same-sector non-3x names. Price-only features (12m momentum, size)
    for annual cohorts; fundamental features and the EPS / re-rating / dividend split only where the data allow.
 C  Growth core: each quarter-end rank liquid KMI names by within-sector percentile of (trailing EPS CAGR, trailing ROE,
    1 - payout), mean of the three. Hold 8 equal weight, equalise semiannually, sell at the next quarter-end when a name
    leaves the top 20 or KMI or the liquid set; refill from the best-ranked. Quality variant adds OCF / net income > 0.7.
    Horizon of the growth term: 3 years as registered; 2 and 1 years run beside it because the data contain only 20 quarters.
    Start = first quarter-end with >= 30 eligible names. Fill at the next session close that is not limit-locked.
    Costs 0.25% a side, plus 0.25% a side when the 60-day median traded value is under Rs20m.
"""
import sys, io, re, glob, os
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
pc = lambda x: "nan" if pd.isna(x) else f"{x*100:+.1f}"
rng = np.random.default_rng(20261018)
MIN_TV, SLIP_TV = 5e6, 20e6

# ------------------------------------------------------------------ data
close0, vol0, tv0 = P.load_panel()
sy = pd.read_csv(ROOT / "data/symbols.csv").set_index("symbol")
BAD_SEC = {"BILLS AND BONDS", "EXCHANGE TRADED FUNDS", "CLOSE - END MUTUAL FUND"}
MERGE = {"TEXTILE COMPOSITE": "TEXTILE", "TEXTILE SPINNING": "TEXTILE", "TEXTILE WEAVING": "TEXTILE",
         "AUTOMOBILE ASSEMBLER": "AUTOS", "AUTOMOBILE PARTS & ACCESSORIES": "AUTOS"}
sector = sy.sectorName.map(lambda x: MERGE.get(x, x))

def read_px(f):
    x = pd.read_csv(f, usecols=["date", "close", "volume"], parse_dates=["date"], index_col="date")
    return x[~x.index.duplicated(keep="last")].sort_index()

extra_c, extra_v, group = {}, {}, {}
lm = [Path(f).stem for f in glob.glob(str(ROOT / "data/prices_listed_missing/*.csv"))]
lm = [s for s in lm if s in sy.index and sy.sectorName[s] not in BAD_SEC and not re.search(r"(PS|CPS)$|^(SGPLR|WAVESAPPR|FPRMR2)$", s)]
dl = pd.read_csv(ROOT / "data/delistings.csv"); dl = dl[dl.price_file == True].dropna(subset=["symbol"])
dl = dl[dl.symbol.map(lambda s: s in sy.index and sy.sectorName[s] not in BAD_SEC)]
for s, kind, d in [(s, "listed_missing", "prices_listed_missing") for s in lm] + [(s, "delisted", "prices_delisted") for s in dl.symbol]:
    x = read_px(ROOT / "data" / d / f"{s}.csv")
    if len(x) == 0: continue
    ok = (x.volume > 0) & (x.close > 0)
    if ok.sum() < 20: continue
    x = x.loc[:x.index[ok][-1]] if kind == "delisted" else x
    extra_c[s] = x.close.where(ok); extra_v[s] = x.volume; group[s] = kind
keep = [c for c in close0.columns if sy.sectorName.get(c, "") not in BAD_SEC]
for c in keep: group[c] = "listed"
days = close0.index
close = pd.concat([close0[keep], pd.DataFrame(extra_c).reindex(days)], axis=1)
vol = pd.concat([vol0[keep], pd.DataFrame(extra_v).reindex(days)], axis=1)
vol = vol.where(~((vol.isna()) & close.notna()), 0.0)
ret = P.returns(close, "adjusted", vol=vol)
# unrecorded splits / consolidations: a one-day move of -60% or worse, or +200% or better, is not a trade (limits are 10%; shells up to ~50%)
_bad = (ret <= -0.6) | (ret >= 2.0)
N_BAD = int(_bad.sum().sum()); BAD_LIST = sorted(set(_bad.stack()[lambda x: x].index.get_level_values(1)))
ret = ret.mask(_bad, 0.0)
tv = (close * vol).fillna(0).where(vol.notna())
medtv = P._med_tv(tv)
LAST = days[-1]
lr = np.log1p(ret.fillna(0).clip(lower=-0.999)).cumsum()
firstobs = close.notna().idxmax(); lastobs = close.apply(lambda c: c.last_valid_index())
tri = np.exp(lr).where(pd.Series(days, days).values[:, None] >= firstobs.values[None, :])   # NaN before first observation
tri_f = tri.ffill()
pr = pd.read_parquet(ROOT / "data/panel_close_adj_pricereturn.parquet")                       # price-only, bonus/split adjusted (survivors)
raw_close = close
liq = (medtv > MIN_TV)

kmi_now = set(pd.read_csv(ROOT / "data/index_members/KMI_ALL_2026-06-05.csv").symbol)
_kf = sorted(glob.glob(str(ROOT / "data/index_members/KMI_ALL_derived_*.csv")))
KMI_L = [(pd.Timestamp(re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1)), set(pd.read_csv(f).symbol)) for f in _kf]
def kmi_at(d):
    ok = [m for t, m in KMI_L if t <= d]
    return ok[-1] if ok else None

pol = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"]).sort_values("date")
tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"]).sort_values("date")
def regime(d):
    r = pol[pol.date <= d]; b = tb[tb.date <= d]
    if not len(r) or not len(b): return "n/a"
    return "bill>policy" if b.y6m.iloc[-1] > r.rate.iloc[-1] else "bill<=policy"
kmi_tr = pd.read_csv(ROOT / "data/macro/kmiallshr.csv", parse_dates=["date"], index_col="date")["value"].reindex(days).ffill()

def pos_on_or_before(d): return days.searchsorted(pd.Timestamp(d), side="right") - 1
def end_of(s, years): return days[pos_on_or_before(s + pd.DateOffset(years=years))]
month_last = pd.Series(days, days).groupby(days.to_period("M")).last()
D0 = days[days.searchsorted(pd.Timestamp("2016-12-30"))]

def fmt_x(x): return "nan" if pd.isna(x) else f"{x:.2f}x"

# ------------------------------------------------------------------ A
def sectionA():
    out("=" * 100); out("A. POPULATION"); out("=" * 100)
    out(f"Data repair: {N_BAD} one-day moves of -60% or worse or +200% or better (unrecorded splits and consolidations; {len(BAD_LIST)} names) were set to zero return.")
    out(f"Panel: {tri.shape[1]} names ({sum(v=='listed' for v in group.values())} listed in panel, {sum(v=='listed_missing' for v in group.values())} listed but missing from the panel, {sum(v=='delisted' for v in group.values())} delisted with price files); {days[0].date()} to {LAST.date()}.")
    out("CAUTION: cash dividends are in corporate_actions.csv only from about Nov 2024 (6 cash rows for 2017-2020), so before that these 'total return' multiples are price plus bonus/split only and understate true total return by the dividend yield (roughly 4 to 7 points a year). The KMI All Share TR comparator includes dividends in full.")
    out("Total return = adjusted returns (cash dividends and bonus/split applied from corporate_actions.csv). The listed-missing and all delisted names have no corporate-action rows: their returns are price-only with moves beyond +-10.5% on normal volume zeroed (crude), so they are understated.")
    starts = [t for t in month_last if t >= D0 and end_of(t, 5) <= LAST and end_of(t, 5) > t and t + pd.DateOffset(years=5) <= LAST + pd.Timedelta(days=4)]
    starts = [D0] + [t for t in starts if t > D0]
    rows, best = [], {}
    for s in starts:
        e = end_of(s, 5)
        L = [c for c in tri.columns if liq.at[s, c] and pd.notna(tri.at[s, c])]
        m = (tri_f.loc[e, L] / tri.loc[s, L]).dropna()
        rows.append(dict(start=s, end=e, n=len(m), **{f"{k}x": (m >= k).mean() for k in (2, 2.5, 3, 5, 10)}, n3=int((m >= 3).sum()), regime=regime(s)))
        for c, v in m.items():
            if c not in best or v > best[c][0]: best[c] = (v, s, e)
    R = pd.DataFrame(rows)
    out(f"\n5-year windows: {len(R)} month-end starts, {R.start.iloc[0].date()} to {R.start.iloc[-1].date()}. Share of the liquid universe at the start that made at least k times (dividends reinvested):")
    out("start        n_liq   >=2x   >=3x   >=5x  >=10x  names>=3x regime")
    anchors = [D0] + [t for t in R.start if t.month == 12 and t.day >= 28] + [R.start.iloc[-1]]
    for _, r in R[R.start.isin(anchors)].iterrows():
        out(f"{r['start'].date()}  {int(r['n']):5d}  {r['2x']*100:5.1f}% {r['3x']*100:5.1f}% {r['5x']*100:5.1f}% {r['10x']*100:5.1f}%  {int(r['n3']):5d}   {r['regime']}")
    out(f"pooled (all {len(R)} overlapping starts, mean of shares): n_liq avg {R.n.mean():.0f}; >=2x {R['2x'].mean()*100:.1f}%, >=2.5x {R['2.5x'].mean()*100:.1f}% (price-plus-bonus proxy for 3x with dividends), >=3x {R['3x'].mean()*100:.1f}%, >=5x {R['5x'].mean()*100:.1f}%, >=10x {R['10x'].mean()*100:.1f}%")
    for g, rr in R.groupby("regime"):
        out(f"  regime at start {g}: {len(rr)} starts, mean n_liq {rr.n.mean():.0f}, >=2x {rr['2x'].mean()*100:.1f}%, >=3x {rr['3x'].mean()*100:.1f}%, >=5x {rr['5x'].mean()*100:.1f}%")
    for y in sorted(R.start.dt.year.unique()):
        rr = R[R.start.dt.year == y]
        out(f"  starts in {y}: {len(rr)} months, >=3x share mean {rr['3x'].mean()*100:.1f}% (range {rr['3x'].min()*100:.1f}-{rr['3x'].max()*100:.1f})")
    # decade
    e10 = LAST
    L = [c for c in tri.columns if liq.at[D0, c] and pd.notna(tri.at[D0, c])]
    dec = (tri_f.loc[e10, L] / tri.loc[D0, L]).dropna()
    yrs = (e10 - D0).days / 365.25
    out(f"\nDecade ({D0.date()} to {e10.date()}, {yrs:.1f} years): liquid at start n={len(dec)}; median multiple {dec.median():.2f}x; >=2x {(dec>=2).mean()*100:.1f}% ({(dec>=2).sum()}), >=3x {(dec>=3).mean()*100:.1f}% ({(dec>=3).sum()}), >=5x {(dec>=5).mean()*100:.1f}% ({(dec>=5).sum()}), >=10x {(dec>=10).mean()*100:.1f}% ({(dec>=10).sum()}). Ended before last date: {int(sum(lastobs[c] < LAST - pd.Timedelta(days=30) for c in dec.index))} names.")
    out(f"  KMI All Share TR over the same span: {kmi_tr.loc[e10]/kmi_tr.loc[D0]:.2f}x")
    # list
    names = sorted([c for c, v in best.items() if v[0] >= 3], key=lambda c: -best[c][0])
    out(f"\nEvery name with a 3x+ five-year window (liquid at window start): {len(names)} names. 'best' = the window start with the highest 5-year multiple.")
    out("symbol   sector                         best_start  5y_mult  dec_mult  KMI_now KMI_at_start  ended  n3_windows")
    allm = {}
    for s in starts:
        e = end_of(s, 5)
        for c in names:
            if liq.at[s, c] and pd.notna(tri.at[s, c]): allm.setdefault(c, []).append(tri_f.at[e, c] / tri.at[s, c])
    recs = []
    for c in names:
        v, s, e = best[c]
        k = kmi_at(s); kat = "n/a" if (k is None or group[c] != "listed") else ("Y" if c in k else "N")
        dm = dec.get(c, np.nan)
        ended = lastobs[c] < LAST - pd.Timedelta(days=30)
        n3 = sum(x >= 3 for x in allm[c])
        recs.append(dict(symbol=c, sector=sector.get(c, "?"), start=s, mult=v, dec=dm, kmi_now=c in kmi_now, kat=kat, ended=ended, n3=n3, nw=len(allm[c])))
        out(f"{c:8s} {str(sector.get(c,'?'))[:30]:30s} {s.date()}  {v:7.2f}  {fmt_x(dm):>8s}  {'Y' if c in kmi_now else 'N':>5s}   {kat:>8s}   {'Y' if ended else '':>3s}   {n3}/{len(allm[c])}")
    B = pd.DataFrame(recs)
    out(f"\nOf the {len(B)}: KMI now {int(B.kmi_now.sum())}; delisted/ended {int(B.ended.sum())}; best-window multiple median {B.mult.median():.2f}x, >=5x {int((B.mult>=5).sum())}, >=10x {int((B.mult>=10).sum())}.")
    out("By sector (n names / liquid names ever in a 5y window / share):")
    liq_ever = {c for s in starts for c in tri.columns if liq.at[s, c] and pd.notna(tri.at[s, c])}
    ss = pd.DataFrame({"n3": B.groupby("sector").size(), "liq": pd.Series({c: sector.get(c, "?") for c in liq_ever}).value_counts()}).fillna(0)
    ss["share"] = ss.n3 / ss.liq
    for sec, r in ss.sort_values("n3", ascending=False).head(14).iterrows(): out(f"  {str(sec)[:34]:34s} {int(r.n3):3d} / {int(r.liq):3d}  {r.share*100:5.1f}%")
    out(f"  all sectors: {int(ss.n3.sum())} / {int(ss.liq.sum())} = {ss.n3.sum()/ss.liq.sum()*100:.1f}% of {len(liq_ever)} names ever liquid at a start")
    ep = B.assign(yr=B.start.dt.year).groupby(["sector", "yr"]).size()
    out(f"Independent episodes: {len(ep)} sector x start-year clusters from {len(B)} names; {B.sector.nunique()} sectors; best-window start years: " + ", ".join(f"{y}:{n}" for y, n in B.start.dt.year.value_counts().sort_index().items()))
    out(f"Decade >=3x names ({int((dec>=3).sum())}): " + ", ".join(f"{c} {v:.1f}x" for c, v in dec[dec >= 3].sort_values(ascending=False).items()))
    return starts, best, B, dec

# ------------------------------------------------------------------ B
def sectionB(starts, best):
    out("\n" + "=" * 100); out("B. EARLY FEATURES"); out("=" * 100)
    cohorts = [D0] + [days[pos_on_or_before(pd.Timestamp(f"{y}-12-31"))] for y in range(2017, 2021)] + [days[pos_on_or_before(pd.Timestamp("2021-09-30"))]]
    G = []   # (cohort, sector, symbols, winner flag, mom12, size)
    for s in cohorts:
        e = end_of(s, 5); p = days.get_loc(s)
        L = [c for c in tri.columns if liq.at[s, c] and pd.notna(tri.at[s, c]) and c in sector.index]
        m = tri_f.loc[e, L] / tri.loc[s, L]
        mom = (tri.loc[s, L] / tri_f.iloc[max(p - 250, 0)][L]).where(tri.iloc[max(p - 250, 0)][L].notna()) if s >= pd.Timestamp("2017-10-20") else pd.Series(np.nan, L)
        for c in L: G.append(dict(cohort=s, sector=sector[c], symbol=c, win=bool(m[c] >= 3), mult=m[c], mom=mom[c], size=np.log(medtv.at[s, c])))
    G = pd.DataFrame(G)
    out("Cohorts (annual, start dates): " + ", ".join(str(c.date()) for c in cohorts))
    out("cohort      liquid  winners(>=3x 5y)  winner share")
    for c, g in G.groupby("cohort"): out(f"{c.date()}  {len(g):5d}  {int(g.win.sum()):5d}  {g.win.mean()*100:5.1f}%")
    out(f"pooled: {len(G)} name-cohorts, {int(G.win.sum())} winners, {G[G.win].symbol.nunique()} distinct names")
    def perm(G, feat, nperm=5000):
        grp = []
        for (c, sec), g in G.dropna(subset=[feat]).groupby(["cohort", "sector"]):
            if g.win.any() and (~g.win).any() and len(g) >= 3: grp.append((g[feat].values, g.win.values))
        if not grp: return None
        def stat(lab):
            ps = []
            for (x, _), l in zip(grp, lab):
                for w in np.where(l)[0]:
                    o = np.delete(x, w)[~np.delete(l, w)] if False else x[~l]
                    ps.append(((o < x[w]).sum() + 0.5 * (o == x[w]).sum()) / len(o))
            return np.mean(ps), len(ps)
        obs, nw = stat([l for _, l in grp])
        sims = np.array([stat([rng.permutation(l) for _, l in grp])[0] for _ in range(nperm)])
        p = (np.abs(sims - 0.5) >= abs(obs - 0.5)).mean()
        return obs, nw, len(grp), p, np.mean([x[l].mean() - x[~l].mean() for x, l in grp]), np.median([np.median(x[l]) - np.median(x[~l]) for x, l in grp])
    out("\nB1. Price-only features at the window start. Percentile of each winner among same-cohort same-sector non-winners (0.50 = no information; 1.0 = winner highest). Permutation p = labels shuffled inside each cohort-sector group (5000 draws). Groups need >=1 winner, >=1 control, >=3 names.")
    out("feature              winners  groups  mean_percentile   perm_p   mean_diff(win-ctl)")
    for feat, lab in [("mom", "12m momentum (TR)"), ("size", "log median traded value")]:
        r = perm(G, feat)
        if r: out(f"{lab:22s} {r[1]:5d}  {r[2]:5d}     {r[0]:.3f}         {r[3]:.3f}    {r[4]:+.3f} (median diff {r[5]:+.3f})")
    out("(Momentum is undefined for the 2016-12-30 cohort: prices start 2016-10-17.)")
    wm = G[G.win].mom.dropna(); cm = G[~G.win].mom.dropna()
    out(f"Momentum level: winners median {wm.median()*100-100:+.0f}% (n={len(wm)}), non-winners median {cm.median()*100-100:+.0f}% (n={len(cm)}); share of winners with 12m momentum above the cohort's median: {np.mean([ (g.mom[g.win] > g.mom.median()).mean() for _, g in G.dropna(subset=['mom']).groupby('cohort') if g.win.any()])*100:.0f}%")
    out("Winner counts by sector vs liquid names, pooled cohorts (winners / name-cohorts):")
    sc = G.groupby("sector").agg(w=("win", "sum"), n=("win", "size")); sc["sh"] = sc.w / sc.n
    for sec, r in sc.sort_values("w", ascending=False).head(10).iterrows(): out(f"  {str(sec)[:34]:34s} {int(r.w):3d} / {int(r.n):4d}  {r.sh*100:5.1f}%")
    return G


# ------------------------------------------------------------------ fundamentals (shared by B2 and C)
q = pd.read_csv(ROOT / "data/fundamentals/quarterly_eps.csv", parse_dates=["fiscal_quarter_end", "first_tradable_date"])
_lag = (pd.to_datetime(q.announce_dt, utc=True).dt.tz_localize(None).dt.normalize() - q.fiscal_quarter_end).dt.days
LAG95 = int(_lag.dropna().quantile(0.95))
q["avail"] = q.first_tradable_date.fillna(q.fiscal_quarter_end + pd.Timedelta(days=LAG95))
Qd = {s: g.set_index("fiscal_quarter_end").sort_index() for s, g in q.groupby("symbol")}
sa = pd.read_csv(ROOT / "seed/data/fundamentals/sa_ratios.csv"); sa = sa[sa.date != "TTM"].copy(); sa["fye"] = pd.to_datetime(sa.date)
SA = {s: g.sort_values("fye", ascending=False) for s, g in sa.groupby("t")}
ME = pd.offsets.MonthEnd(0)
def qe(E, k): return (E - pd.DateOffset(months=3 * k)) + ME
def ttm_sum(g, E, col):
    v = [g[col].get(qe(E, k), np.nan) for k in range(4)]
    return np.nan if any(pd.isna(x) for x in v) else float(sum(v))
def latest_E(g, d):
    for E in sorted(g.index[g.avail <= d], reverse=True)[:3]:
        if all(qe(E, k) in g.index and g.avail[qe(E, k)] <= d for k in range(4)) and not pd.isna(ttm_sum(g, E, "eps_basic")): return E
    return None
def fund(s, d, h):
    g = Qd.get(s)
    if g is None: return None
    E = latest_E(g, d)
    if E is None or (d - E).days > 300: return None
    Eb = (E - pd.DateOffset(months=12 * h)) + ME
    r = dict(E=E)
    for c in ("eps_basic", "net_income", "revenue"): r[c], r[c + "_b"] = ttm_sum(g, E, c), ttm_sum(g, Eb, c)
    r["ocf"] = ttm_sum(g, E, "ocf")
    return r
def sa_known(s, d):
    g = SA.get(s)
    if g is None: return None
    for r in g.itertuples():
        a = Qd[s].avail.get(r.fye, r.fye + pd.Timedelta(days=LAG95)) if s in Qd else r.fye + pd.Timedelta(days=LAG95)
        if a <= d: return r
    return None
def pay_of(r):
    if pd.notna(r.payoutratio): return float(np.clip(r.payoutratio, 0, 1))
    return 0.0 if (pd.isna(r.dividendyield) or r.dividendyield == 0) else np.nan
def col_of(s): return tri.columns.get_loc(s)

def score_table(d, h, quality=False):
    """Within-sector percentile ranks of (EPS CAGR over h years, ROE, 1 - payout), mean of the three. Universe: KMI All Share
    member at d, 60-day median traded value > Rs5m, EPS TTM > 0 now and h years earlier, ROE and payout known."""
    pos = pos_on_or_before(d); dd = days[pos]; kmi = kmi_at(dd); rows = []
    if kmi is None: return pd.DataFrame()
    for s in Qd:
        if s in DATA_SUSPECT or s not in tri.columns or s not in kmi or pd.isna(sector.get(s)) or not liq.iat[pos, col_of(s)] or pd.isna(tri.iat[pos, col_of(s)]): continue
        f = fund(s, dd, h)
        if f is None or not (f["eps_basic"] > 0 and f["eps_basic_b"] > 0): continue
        r = sa_known(s, dd)
        if r is None or pd.isna(r.roe): continue
        pay = pay_of(r)
        if pd.isna(pay): continue
        ni = f["net_income"]; cn = f["ocf"] / ni if (pd.notna(ni) and ni > 0 and pd.notna(f["ocf"])) else np.nan
        if quality and not (cn > 0.7): continue
        pe = pr[s].iat[pos] / f["eps_basic"] if s in pr.columns and pd.notna(pr[s].iat[pos]) else np.nan
        mom = tri.iat[pos, col_of(s)] / tri_f.iat[max(pos - 250, 0), col_of(s)]
        rows.append(dict(symbol=s, sector=sector[s], cagr=(f["eps_basic"] / f["eps_basic_b"]) ** (1 / h) - 1, roe=r.roe, pay=pay, ocfni=cn, pe=pe, mom=mom, E=f["E"]))
    df = pd.DataFrame(rows)
    if df.empty: return df
    n = df.groupby("sector").symbol.transform("size")
    for c, col in (("cagr", "r_g"), ("roe", "r_r"), ("pay", "r_p")):
        x = df[c] if c != "pay" else -df[c]
        df[col] = x.groupby(df.sector).rank(pct=True).where(n > 1, 0.5)
    df["score"] = df[["r_g", "r_r", "r_p"]].mean(axis=1)
    df = df.sort_values(["score", "symbol"], ascending=[False, True]).reset_index(drop=True)
    df["rank"] = np.arange(1, len(df) + 1)
    return df

# ------------------------------------------------------------------ B2: fundamentals
def sectionB2():
    out("\nB2. Fundamental features: only one cohort is possible. quarterly_eps.csv holds 20 quarters (2021Q3 to 2026Q2 for 108 of 129 names), so a 1-year trailing EPS growth first exists for the TTM ending 2023-06. The cohort starts 2023-10-31 and runs to the last date (2.96 years); winner = total return >= 2.0x (about 29% a year). One regime, one episode: exploratory only.")
    d0 = days[pos_on_or_before(pd.Timestamp("2023-10-31"))]; p0 = days.get_loc(d0)
    rows = []
    for s in Qd:
        if s not in tri.columns or s not in sector.index or pd.isna(sector[s]) or not liq.iat[p0, col_of(s)] or pd.isna(tri.iat[p0, col_of(s)]): continue
        f = fund(s, d0, 1); r = sa_known(s, d0)
        if f is None or r is None: continue
        m = tri_f.at[LAST, s] / tri.at[d0, s]
        ep, eb = f["eps_basic"], f["eps_basic_b"]
        rows.append(dict(symbol=s, sector=sector[s], win=bool(m >= 2), mult=m,
                         g1=(ep / eb - 1) if (ep > 0 and eb > 0) else np.nan, roe=r.roe, pay=pay_of(r),
                         revg=f["revenue"] / f["revenue_b"] - 1 if f["revenue_b"] and f["revenue_b"] > 0 else np.nan,
                         size=np.log(medtv.at[d0, s]), pe=(pr[s].at[d0] / ep) if (ep > 0 and s in pr.columns) else np.nan,
                         mom=tri.at[d0, s] / tri_f.iat[p0 - 250, col_of(s)]))
    F = pd.DataFrame(rows)
    out(f"Names with fundamentals, liquid and sector-tagged at {d0.date()}: {len(F)}; winners (>=2x): {int(F.win.sum())} ({F.win.mean()*100:.0f}%); >=3x: {int((F.mult>=3).sum())}. Median multiple {F.mult.median():.2f}x. KMI All Share TR over the span: {kmi_tr.loc[LAST]/kmi_tr.loc[d0]:.2f}x.")
    feats = [("g1", "TTM EPS growth, 1y"), ("roe", "ROE (latest FY known)"), ("pay", "payout (reinvestment = 1 - payout)"), ("revg", "TTM revenue growth, 1y"), ("size", "log median traded value"), ("pe", "P/E (price / TTM EPS)"), ("mom", "12m momentum")]
    def perm(G, feat, nperm=5000):
        grp = [(g[feat].values, g.win.values) for _, g in G.dropna(subset=[feat]).groupby("sector") if g.win.any() and (~g.win).any() and len(g) >= 3]
        if not grp: return None
        def stat(labs):
            ps = []
            for (x, _), l in zip(grp, labs):
                o = x[~l]
                for w in np.where(l)[0]: ps.append(((o < x[w]).sum() + 0.5 * (o == x[w]).sum()) / len(o))
            return np.mean(ps), len(ps)
        obs, nw = stat([l for _, l in grp]); sims = np.array([stat([rng.permutation(l) for _, l in grp])[0] for _ in range(nperm)])
        return obs, nw, len(grp), (np.abs(sims - 0.5) >= abs(obs - 0.5)).mean()
    out("Percentile of each winner among same-sector non-winners (0.50 = no information). Permutation p: labels shuffled inside each sector, 5000 draws. No correction for 7 features.")
    out("feature                              winners groups  mean_pctile  perm_p   median winners | non-winners")
    for f_, lab in feats:
        r = perm(F, f_)
        if r: out(f"{lab:36s} {r[1]:5d} {r[2]:5d}     {r[0]:.3f}      {r[3]:.3f}    {F[F.win][f_].median():9.3f} | {F[~F.win][f_].median():9.3f}")
    from scipy.stats import spearmanr
    out("Continuous version, all names: Spearman correlation between the within-sector percentile of the feature and the sector-demeaned log 3-year multiple (permutation p: feature shuffled inside each sector, 5000 draws).")
    out("feature                              n    rho     perm_p")
    for f_, lab in feats:
        G = F.dropna(subset=[f_]).copy(); G = G[G.groupby("sector").symbol.transform("size") >= 2]
        G["lm"] = np.log(G.mult); G["lm"] -= G.groupby("sector").lm.transform("mean")
        def rho(G_): return spearmanr(G_.groupby("sector")[f_].rank(pct=True), G_.lm)[0]
        r0 = rho(G); sims = []
        for _ in range(3000):
            H = G.copy(); H[f_] = H.groupby("sector")[f_].transform(lambda x: rng.permutation(x.values)); sims.append(rho(H))
        out(f"{lab:36s} {len(G):3d}  {r0:+.2f}   {(np.abs(np.array(sims)) >= abs(r0)).mean():.3f}")
    out("Winners / names by sector: " + ", ".join(f"{k} {int(v.win.sum())}/{len(v)}" for k, v in F.groupby("sector") if v.win.any()))
    out("\nDecomposition of the total return into EPS growth x re-rating (P/E) x dividends. Shares of ln(total multiple), per winner.")
    def decomp(label, d_start, thr):
        p_s = days.get_loc(d_start); rows = []
        for s in Qd:
            if s not in tri.columns or s not in pr.columns or pd.isna(tri.at[d_start, s]) or not liq.iat[p_s, col_of(s)]: continue
            m = tri_f.at[LAST, s] / tri.at[d_start, s]
            if m < thr: continue
            f0, f1 = fund(s, d_start, 1), fund(s, LAST, 1)
            if f0 is None or f1 is None or not (f0["eps_basic"] > 0 and f1["eps_basic"] > 0): rows.append(dict(symbol=s, mult=m, ok=False)); continue
            pm = pr[s].at[LAST] / pr[s].at[d_start]; er = f1["eps_basic"] / f0["eps_basic"]; dv = m / pm; L = np.log(m)
            rows.append(dict(symbol=s, mult=m, ok=True, eps=np.log(er) / L, rerate=np.log(pm / er) / L, div_=np.log(dv) / L, er=er, pe0=pr[s].at[d_start] / f0["eps_basic"], pe1=pr[s].at[LAST] / f1["eps_basic"]))
        D = pd.DataFrame(rows); o = D[D.ok] if len(D) else D
        out(f"{label}: start {d_start.date()}, winners (TR >= {thr:g}x) {len(D)}, with usable EPS at both ends {len(o)}")
        if len(o):
            out(f"  median share of ln(multiple): EPS growth {o.eps.median()*100:.0f}% (mean {o.eps.mean()*100:.0f}%), re-rating {o.rerate.median()*100:.0f}% (mean {o.rerate.mean()*100:.0f}%), dividends {o['div_'].median()*100:.0f}% (mean {o['div_'].mean()*100:.0f}%)")
            out(f"  EPS ratio median {o.er.median():.2f}x; P/E start median {o.pe0.median():.1f} -> end {o.pe1.median():.1f}; re-rating supplied more than half in {int((o.rerate>0.5).sum())} of {len(o)}; EPS growth supplied more than half in {int((o.eps>0.5).sum())}")
            out("  " + "; ".join(f"{r.symbol} {r.mult:.1f}x (eps {r.eps*100:.0f}% / rerate {r.rerate*100:.0f}% / div {r.div_*100:.0f}%)" for r in o.sort_values("mult", ascending=False).head(12).itertuples()))
    decomp("4-year, 3x", days[pos_on_or_before(pd.Timestamp("2022-10-17"))], 3.0)
    decomp("3-year, 2x", d0, 2.0)
    out("Not possible: a 5-year decomposition. A start EPS needs 4 quarters before the start, and quarters begin 2021-09 for 108 of 129 names, so no 5-year window has a start EPS.")
    return F


# ------------------------------------------------------------------ C: growth-core rule
QE = [g.iloc[-1] for _, g in pd.Series(days, days).groupby(days.to_period("Q"))]
QE = [d for d in QE if d >= pd.Timestamp("2023-09-01") and d <= LAST]
DATA_SUSPECT = {"STL"}   # two unrecorded 28-90% one-day price drops in 2026, P/E 0.8: price path not trustworthy
SYMS = [s for s in Qd if s in tri.columns]
SI = {s: i for i, s in enumerate(SYMS)}
Tf = np.nan_to_num(tri_f[SYMS].values)
OBSm = close[SYMS].notna().values
prev_raw = close[SYMS].ffill().shift(1)
RR = (close[SYMS] / prev_raw - 1).values
UL, LL = np.nan_to_num(RR, nan=0) >= 0.095, np.nan_to_num(RR, nan=0) <= -0.095     # lock: within 0.5 points of the +-10% limit
SLIP = (medtv[SYMS].values < SLIP_TV) | np.isnan(medtv[SYMS].values)
KMIW = kmi_tr.values.astype(float)
_cache = {}
def st(d, h, qual):
    k = (d, h, qual)
    if k not in _cache: _cache[k] = score_table(d, h, qual)
    return _cache[k]

def cost(i, p): return 0.0025 + (0.0025 if SLIP[p, i] else 0.0)

def deposits_for(p0, mode):
    if mode == "fixed": return {p0: 50000.0}
    dep, seen = {p0: 50000.0}, {(days[p0].year, days[p0].month)}
    m = 1
    for p in range(p0 + 1, len(days)):
        ym = (days[p].year, days[p].month)
        if ym not in seen:
            seen.add(ym); dep[p] = 50000.0 if m < 2 else 100000.0; m += 1
    return dep

def simulate(selector, start_d, mode):
    """selector(date, held_symbols, rebal) -> list of symbols to hold after the quarter-end review."""
    p0 = days.get_loc(start_d); N = len(days)
    rank_pos = [days.get_loc(d) for d in QE if d >= start_d]; rebal_pos = {p for j, p in enumerate(rank_pos) if j % 2 == 0}
    dep = deposits_for(p0, mode)
    S = len(SYMS); units = np.zeros(S); cash = 0.0; pend = []
    eq = np.full(N, np.nan); flow = np.zeros(N); traded = 0.0
    spend = np.zeros(S); proc = np.zeros(S); eps_ = []; nexit = 0; nheld_prev = 0
    for p in range(p0, N):
        if pend:
            keep = []
            for o in sorted(pend, key=lambda o: o[2] == "buy"):
                sig, i, kind, val = o
                if sig >= p: keep.append(o); continue
                if p - sig > 10: continue
                if not OBSm[p, i] or (kind == "buy" and UL[p, i]) or (kind != "buy" and LL[p, i]): keep.append(o); continue
                c = cost(i, p)
                if kind == "buy":
                    sp_ = min(val, cash) / (1 + c)
                    if sp_ <= 0: continue
                    units[i] += sp_ / Tf[p, i]; cash -= sp_ * (1 + c); traded += sp_; spend[i] += sp_ * (1 + c)
                else:
                    u = units[i] if kind == "sell" else min(units[i], val)
                    pr_ = u * Tf[p, i]; units[i] -= u; cash += pr_ * (1 - c); traded += pr_; proc[i] += pr_ * (1 - c)
                    if units[i] < 1e-9 and kind == "sell":
                        units[i] = 0; eps_.append((SYMS[i], proc[i] / spend[i] - 1, False)); spend[i] = proc[i] = 0
            pend = keep
        if p in dep: cash += dep[p]; flow[p] = dep[p]
        eq[p] = cash + float((units * Tf[p]).sum())
        pendbuy = {o[1] for o in pend if o[2] == "buy"}
        held_i = {i for i in range(S) if units[i] > 0} | pendbuy
        if p in rank_pos:
            held = {SYMS[i] for i in held_i}; rb = p in rebal_pos
            tgt = selector(days[p], held, rb); tgt_i = {SI[s] for s in tgt}
            nexit += len(held_i - tgt_i); nheld_prev += len(held_i)
            total = eq[p]
            for i in held_i - tgt_i: pend.append((p, i, "sell", 0.0))
            if rb and tgt_i:
                each = total / len(tgt_i)
                for i in tgt_i:
                    diff = each - units[i] * Tf[p, i]
                    if diff > 0: pend.append((p, i, "buy", diff))
                    elif diff < 0: pend.append((p, i, "sell_u", -diff / Tf[p, i]))
            else:
                new = tgt_i - held_i
                if new:
                    avail = cash + sum(units[i] * Tf[p, i] for i in held_i - tgt_i)
                    amt = min(total / 8, avail / len(new))
                    for i in new: pend.append((p, i, "buy", amt))
        elif p in dep and p != p0 and held_i:
            for i in held_i: pend.append((p, i, "buy", dep[p] / len(held_i)))
    for i in range(S):
        if units[i] > 0 and spend[i] > 0: eps_.append((SYMS[i], (proc[i] + units[i] * Tf[-1, i]) / spend[i] - 1, True))
    r = np.zeros(N); r[p0 + 1:] = (eq[p0 + 1:] - flow[p0 + 1:]) / eq[p0:-1] - 1
    return dict(p0=p0, eq=eq, flow=flow, twr=r, traded=traded, episodes=eps_, nexit=nexit, nheld=nheld_prev)

def bench_index(idx_vals, start_d, mode):
    p0 = days.get_loc(start_d); dep = deposits_for(p0, mode); N = len(days)
    u = 0.0; eq = np.full(N, np.nan); flow = np.zeros(N); pend = []
    for p in range(p0, N):
        for sig, amt in [o for o in pend if o[0] < p]: u += amt / idx_vals[p]
        pend = [o for o in pend if o[0] >= p]
        if p in dep: flow[p] = dep[p]; pend.append((p, dep[p])); 
        eq[p] = u * idx_vals[p] + sum(a for _, a in pend)
    r = np.zeros(N); r[p0 + 1:] = (eq[p0 + 1:] - flow[p0 + 1:]) / eq[p0:-1] - 1
    return dict(p0=p0, eq=eq, flow=flow, twr=r)

def ew_basket_index(start_d):
    """Equal-weight KMI All Share names with 60-day median traded value > Rs5m, rebalanced on the first session of each month,
    0.25% a side on traded value. Returns a wealth index over the panel dates (survivor names in the panel)."""
    N = len(days); W = np.full(N, np.nan); p0 = days.get_loc(start_d)
    mstart = [days.get_loc(g.iloc[0]) for _, g in pd.Series(days, days).groupby(days.to_period("M")) if g.iloc[0] >= start_d] or [p0]
    mstart = [p0] + [p for p in mstart if p > p0] + [N]
    w_prev = pd.Series(dtype=float); level = 1.0
    cols = tri.columns
    for a, b in zip(mstart[:-1], mstart[1:]):
        kmi = kmi_at(days[a]) or set()
        mem = [s for s in cols if s in kmi and liq.iat[a, cols.get_loc(s)] and pd.notna(tri.iat[a, cols.get_loc(s)])]
        w_new = pd.Series(1.0 / len(mem), mem)
        allm = w_prev.index.union(w_new.index)
        turn = (w_new.reindex(allm, fill_value=0) - w_prev.reindex(allm, fill_value=0)).abs().sum() / 2 if len(w_prev) else 1.0
        level *= 1 - 0.005 * turn
        base = tri_f.iloc[a][mem]
        path = (tri_f.iloc[a:b][mem] / base).mean(axis=1)
        W[a:b] = level * path.values
        level = W[b - 1]
        end = tri_f.iloc[b - 1][mem] / base
        w_prev = (w_new * end) / (w_new * end).sum()
    return W

def xirr(flows, finalv, p_end):
    from scipy.optimize import brentq
    ts = [(days[p] - days[min(flows)]).days / 365.25 for p in flows]; T = (days[p_end] - days[min(flows)]).days / 365.25
    f = lambda r: sum(a * (1 + r) ** (T - t) for a, t in zip(flows.values(), ts)) - finalv
    try: return brentq(f, -0.99, 50)
    except ValueError: return np.nan

def summarize(res, label, mode):
    p0 = res["p0"]; N = len(days); eq = res["eq"]; dep = {p: a for p, a in enumerate(res["flow"]) if a > 0}
    td = sum(dep.values()); fv = eq[-1]; yrs = (LAST - days[p0]).days / 365.25
    idx = np.cumprod(1 + res["twr"][p0:]); dd = (idx / np.maximum.accumulate(idx) - 1).min()
    twr_cagr = idx[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    mwr = xirr(dep, fv, N - 1) if mode == "dep" else (fv / td) ** (1 / yrs) - 1
    to = res["traded"] / 2 / np.nanmean(eq[p0:]) / yrs if "traded" in res else np.nan
    return dict(label=label, multiple=fv / td, mwr=mwr, twr_cagr=twr_cagr, twr_total=idx[-1] - 1, maxdd=dd, turnover=to, final=fv, dep=td, yrs=yrs, idx=pd.Series(idx, days[p0:]))

def sectionC():
    out("\n" + "=" * 100); out("C. GROWTH-CORE RULE"); out("=" * 100)
    out(f"Data limits first. sa_ratios.csv has fiscal years from 2020-06 (a handful of names) and mostly FY2022 onward; quarterly_eps.csv has 20 quarters (2021Q3 to 2026Q2 for 108 of 129 names, 2019Q3 for one). A trailing 3-year EPS CAGR therefore first exists for the TTM ending 2025-06 (base TTM 2022-06), known from about Oct 2025. Every 5-year window and the decade: 0 are testable. The 2-year and 1-year versions run beside the 3-year one so the rule can be seen over a longer span; they are NOT the pre-registered horizon and carry the same single-regime caveat. Announcement lag for rows with no announcement match: {LAG95} days after quarter end (95th percentile of the matched lags).")
    out("Eligible names (KMI All Share, liquid > Rs5m, EPS positive now and at the base, ROE and payout known) by quarter-end:")
    out("quarter-end   " + "  ".join(f"h={h}y all/qual" for h in (3, 2, 1)))
    starts = {}
    for d in QE:
        row = []
        for h in (3, 2, 1):
            a, b = len(st(d, h, False)), len(st(d, h, True)); row.append(f"{a:3d}/{b:3d}   ")
            if a >= 30 and h not in starts: starts[h] = d
        out(f"{d.date()}   " + "      ".join(row))
    out(f"Start dates (first quarter-end with >= 30 eligible names): " + ", ".join(f"h={h}y: {d.date()}" for h, d in sorted(starts.items(), reverse=True)))
    results = {}
    for h in (3, 2, 1):
        if h not in starts: out(f"h={h}y: never reaches 30 eligible names; not run."); continue
        d0 = starts[h]
        for qual in (False, True):
            def sel(d, held, rb, h=h, qual=qual):
                T = st(d, h, qual)
                if T.empty: return []
                top20 = set(T.symbol[:20]); keep = [s for s in T.symbol if s in held and s in top20]
                fill = [s for s in T.symbol if s not in keep][: max(0, 8 - len(keep))]
                return (keep + fill)[:8]
            for mode in ("dep", "fixed"):
                results[(h, qual, mode)] = (simulate(sel, d0, mode), d0)
    # benchmarks
    out("\nResults. 'dep' = Rs50k, Rs50k, then Rs100k a month (first deposit on the start date); 'fixed' = Rs50k once. Money-weighted CAGR for dep, plain CAGR for fixed. Max DD is on the time-weighted index (deposits removed). Turnover = (buys+sells)/2 / average equity / year. Costs and lock rule as pre-registered. Benchmarks take the same deposits at the next close.")
    table, bench = [], {}
    for (h, qual, mode), (res, d0) in results.items():
        for nm, key in (("KMI All Share TR", "kmi"), ("EW liquid KMI basket", "ew")):
            bk = (d0, key)
            if bk not in bench: bench[bk] = KMIW if key == "kmi" else ew_basket_index(d0)
        sm = summarize(res, f"rule h={h}y{' +quality' if qual else ''}", mode)
        km = summarize(bench_index(bench[(d0, "kmi")], d0, mode), "KMI TR", mode)
        ew = summarize(bench_index(bench[(d0, "ew")], d0, mode), "EW basket", mode)
        table.append((h, qual, mode, d0, sm, km, ew, res))
    out("variant                      mode   start       yrs  deposited   final       multiple  CAGR   TWR_total  maxDD  turnover |  KMI TR: multiple CAGR TWR maxDD | EW: multiple CAGR TWR maxDD")
    for h, qual, mode, d0, sm, km, ew, res in table:
        out(f"{sm['label']:26s} {mode:5s} {d0.date()} {sm['yrs']:4.2f} {sm['dep']:10,.0f} {sm['final']:11,.0f}  {sm['multiple']:6.3f}x {pc(sm['mwr']):>6s}% {pc(sm['twr_total']):>8s}% {pc(sm['maxdd']):>6s}% {sm['turnover']:5.2f}x | {km['multiple']:6.3f}x {pc(km['mwr']):>6s}% {pc(km['twr_total']):>7s}% {pc(km['maxdd']):>6s}% | {ew['multiple']:6.3f}x {pc(ew['mwr']):>6s}% {pc(ew['twr_total']):>7s}% {pc(ew['maxdd']):>6s}%")
    # per-position
    out("\nPer-position returns (net of costs; an open position is marked at the last close), fixed-capital runs:")
    out("variant                      n   mean    median  win   >+50%  <-30%  worst   best   open")
    for h, qual, mode, d0, sm, km, ew, res in table:
        if mode != "fixed": continue
        e = np.array([x[1] for x in res["episodes"]])
        if len(e) == 0: continue
        out(f"{sm['label']:26s} {len(e):3d}  {pc(e.mean()):>6s}  {pc(np.median(e)):>6s}  {np.mean(e>0)*100:3.0f}%  {np.mean(e>0.5)*100:4.0f}%  {np.mean(e<-0.3)*100:4.0f}%  {pc(e.min()):>6s} {pc(e.max()):>6s}  {sum(x[2] for x in res['episodes'])}")
    # placebo
    out("\nPlacebo: 200 random-entry runs per variant, fixed capital, same dates, same fill, lock and cost rules, same quarter-end exits for KMI or liquidity loss, and each held name exits with the probability the rule itself showed (exits / holdings at its reviews). Final multiple of the rule vs the placebo distribution:")
    out("variant                      rule_mult  placebo_median  p5     p95    rule_percentile")
    for h, qual, mode, d0, sm, km, ew, res in table:
        if mode != "fixed": continue
        pexit = res["nexit"] / max(res["nheld"], 1)
        def selp(d, held, rb, h=h, qual=qual, pexit=pexit):
            T = st(d, h, qual)
            if T.empty: return []
            el = list(T.symbol); keep = [s for s in held if s in el and rng.random() > pexit]
            pool = [s for s in el if s not in keep]
            return keep + list(rng.choice(pool, size=min(8 - len(keep), len(pool)), replace=False))
        pm = np.array([summarize(simulate(selp, d0, "fixed"), "p", "fixed")["multiple"] for _ in range(200)])
        out(f"{sm['label']:26s} {sm['multiple']:8.3f}x   {np.median(pm):8.3f}x   {np.percentile(pm,5):6.3f} {np.percentile(pm,95):6.3f}   {(pm < sm['multiple']).mean()*100:5.1f}%")
    # year / regime split for the longest run
    h, qual, mode, d0, sm, km, ew, res = [t for t in table if t[0] == min(r[0] for r in table) or True][0]
    best = [t for t in table if t[1] is False and t[2] == "fixed"]
    best = max(best, key=lambda t: t[4]["yrs"])
    h, qual, mode, d0, sm, km, ew, res = best
    out(f"\nYear and regime split, longest run ({sm['label']}, fixed capital, {d0.date()} to {LAST.date()}), time-weighted returns:")
    kmi_r = pd.Series(KMIW, days).pct_change().fillna(0).values; ew_r = pd.Series(bench[(d0, 'ew')], days).pct_change().fillna(0).values
    df = pd.DataFrame({"rule": res["twr"], "kmi": kmi_r, "ew": ew_r}, days).iloc[res["p0"] + 1:]
    df["reg"] = [regime(days[days.get_loc(t) - 1]) for t in df.index]
    for y, g in df.groupby(df.index.year): out(f"  {y}: rule {pc((1+g.rule).prod()-1)}%  KMI TR {pc((1+g.kmi).prod()-1)}%  EW basket {pc((1+g.ew).prod()-1)}%  ({len(g)} days)")
    for rg, g in df.groupby("reg"): out(f"  regime {rg}: {len(g)} days; rule {pc((1+g.rule).prod()-1)}%  KMI TR {pc((1+g.kmi).prod()-1)}%  EW {pc((1+g.ew).prod()-1)}%")
    out(f"  6M T-bill {tb.y6m.iloc[-1]:.2f}% vs policy rate {pol.rate.iloc[-1]:.2f}% on the last date: regime {regime(LAST)}")
    # cohorts: each review's top 8, 6-month forward return
    out("\nCohort check: equal-weight top-8 of each quarter-end ranking, forward return to the next quarter-end (gross), vs KMI TR and the EW basket (h=2y, the longest span with a stable universe):")
    ewW = pd.Series(bench[(starts[2], 'ew')] if (starts[2], 'ew') in bench else ew_basket_index(starts[2]), days)
    for a, b in zip(QE[:-1], QE[1:]):
        T = st(a, 2, False)
        if len(T) < 30: continue
        top = list(T.symbol[:8]); f = (tri_f.loc[b, top] / tri_f.loc[a, top]).mean() - 1
        allr = (tri_f.loc[b, list(T.symbol)] / tri_f.loc[a, list(T.symbol)]).mean() - 1
        out(f"  {a.date()} -> {b.date()}: top-8 {pc(f)}%  all eligible EW {pc(allr)}%  KMI TR {pc(kmi_tr.loc[b]/kmi_tr.loc[a]-1)}%")
    # live screen
    out(f"\nLIVE SCREEN as of {LAST.date()} (information known by then; KMI list of 2026-06-05):")
    for h, qual in ((3, False), (3, True), (2, False)):
        T = score_table(LAST, h, qual)
        out(f"\n  growth horizon {h}y{', quality variant (OCF/NI > 0.7)' if qual else ''}: {len(T)} eligible names. Top 12:")
        out("  rank symbol   sector                       score  EPS_CAGR   ROE   payout OCF/NI   P/E  12m_mom  latest_qtr")
        for r in T.head(12).itertuples():
            out(f"  {r.rank:3d}  {r.symbol:8s} {str(r.sector)[:27]:27s} {r.score:.3f}  {pc(r.cagr):>6s}%  {r.roe*100:5.1f}% {r.pay*100:5.0f}% {r.ocfni:6.2f} {r.pe:6.1f} {pc(r.mom-1):>6s}%  {r.E.date()}")
        if h == 3 and not qual:
            out("  Names in the 3y top 20 that are also in the quality top 20 and the 2y top 20: " + ", ".join(sorted(set(T.symbol[:20]) & set(score_table(LAST, 3, True).symbol[:20]) & set(score_table(LAST, 2, False).symbol[:20]))))
    return table

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "A", "B"): starts, best, Btab, dec = sectionA()
    if mode in ("all", "B"): G = sectionB(starts, best)
    if mode in ("all", "B"): F = sectionB2()
    if mode in ("all", "C"): sectionC()
    (ROOT / "tests/out/compounders.txt").write_text(buf.getvalue(), encoding="utf-8")
