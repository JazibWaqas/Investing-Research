"""Quality within sector, point in time. Spec in tests/quality_within_sector.md (pre-registered, not tuned).
Run: .venv/Scripts/python.exe scripts/tests/quality_within_sector.py  -> tests/out/quality_within_sector.txt"""
import sys, io, re, glob
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
pc = lambda x: "nan" if pd.isna(x) else f"{x*100:+.1f}"
NDRAW, rng = 2000, np.random.default_rng(20261018)

# ---------------- data
close, vol, tv = P.load_panel()
ret = P.returns(close, "adjusted")
days = close.index; LAST = days[-1]
cumlog = np.log1p(ret.fillna(0).clip(lower=-0.999)).cumsum()
cf = close.ffill()
medtv = P._med_tv(tv)
q = pd.read_csv(ROOT / "data/fundamentals/quarterly_eps.csv", parse_dates=["fiscal_quarter_end", "first_tradable_date"])
lag = (pd.to_datetime(q.announce_dt, utc=True).dt.tz_localize(None).dt.normalize() - q.fiscal_quarter_end).dt.days
LAG95 = int(lag.dropna().quantile(0.95))
q["avail"] = q.first_tradable_date.fillna(q.fiscal_quarter_end + pd.Timedelta(days=LAG95))
q = q.sort_values(["symbol", "fiscal_quarter_end"])
Q = {s: g.reset_index(drop=True) for s, g in q.groupby("symbol")}
sa = pd.read_csv(ROOT / "seed/data/fundamentals/sa_ratios.csv"); sa = sa[sa.date != "TTM"].copy()
sa["fye"] = pd.to_datetime(sa.date); SA = {s: g for s, g in sa.groupby("t")}
act = pd.read_csv(ROOT / "data/corporate_actions.csv", parse_dates=["ex_date"]); act = act[act.type == "cash"]
sym = pd.read_csv(ROOT / "data/symbols.csv").set_index("symbol").sectorName
MERGE = {"TEXTILE COMPOSITE": "TEXTILE", "TEXTILE SPINNING": "TEXTILE", "AUTOMOBILE ASSEMBLER": "AUTOS", "AUTOMOBILE PARTS & ACCESSORIES": "AUTOS"}
sector = sym.map(lambda x: MERGE.get(x, x))

_mem = {}
def members(prefix, d):
    ok = []
    for f in glob.glob(str(ROOT / "data/index_members" / f"{prefix}_*.csv")):
        t = pd.Timestamp(re.search(r"(\d{4}-\d{2}(?:-\d{2})?)", Path(f).stem).group(1))
        if t <= d: ok.append((t, f))
    return list(pd.read_csv(max(ok)[1]).symbol) if ok else []

# ---------------- scoring
def raw_scores(info, pos):
    """info: date; rows with avail < info are known. pos: panel row of the price. -> DataFrame by symbol."""
    rows = []
    for s, g in Q.items():
        if s not in close.columns or s not in sector.index: continue
        k = g[g.avail < info]
        if len(k) < 4: continue
        l4, l8 = k.tail(4), k.tail(8)
        if (info - l4.fiscal_quarter_end.iloc[-1]).days > 400 or (l4.fiscal_quarter_end.iloc[-1] - l4.fiscal_quarter_end.iloc[0]).days > 290: continue
        px = cf[s].iloc[pos]
        if not px > 0: continue
        ni, ocf = l4.net_income.sum(min_count=4), l4.ocf.sum(min_count=4)
        sh = l4.shares.iloc[-1]
        d = dict(symbol=s, sector=sector[s], ni=ni)
        d["cash"] = np.nan if pd.isna(ni) or pd.isna(ocf) else (0.0 if ni <= 0 else float(np.clip(ocf / ni, 0, 2)))
        d["ep"] = ni / (sh * px) if sh >= 50 and pd.notna(ni) else (l4.eps_basic.sum(min_count=4) / px)
        full8 = len(l8) == 8 and (l8.fiscal_quarter_end.iloc[-1] - l8.fiscal_quarter_end.iloc[0]).days <= 700
        e = l8.eps_basic.values if full8 else None
        d["stab"] = np.nan
        if e is not None and not np.isnan(e).any():
            d["stab"] = -np.inf if e.mean() <= 0 else -e.std(ddof=1) / e.mean()
        # (a) ROE proxy: TTM NI / equity at latest published fiscal year-end (equity = shares x price_FYE / P/B)
        d["roe"], d["roe_fb"] = np.nan, np.nan
        sg = SA.get(s)
        if sg is not None and pd.notna(ni):
            for r in sg.sort_values("fye", ascending=False).itertuples():
                m = k[k.fiscal_quarter_end == r.fye]
                if len(m) and pd.notna(r.pb) and r.pb > 0 and m.shares.iloc[0] >= 50:
                    pf = cf[s].loc[:r.fye]
                    if len(pf) and pf.notna().any() and (r.fye - pf.dropna().index[-1]).days <= 10:
                        d["roe"] = ni / (m.shares.iloc[0] * pf.dropna().iloc[-1] / r.pb)
                    break
        if np.isnan(d["roe"]) and full8:
            ni8 = l8.net_income.values; g_ = (ni8[4:] - ni8[:4]) / np.maximum(np.abs(ni8[:4]), 1)
            if not np.isnan(g_).any(): d["roe_fb"] = -np.std(np.clip(g_, -1, 3), ddof=1)
        # (d) payout: trailing-12m cash dividends / TTM EPS, only when dividend records are complete (from Nov 2024)
        d["pay"] = np.nan
        if info >= pd.Timestamp("2025-11-01"):
            dv = act[(act.symbol == s) & (act.ex_date < info) & (act.ex_date >= info - pd.Timedelta(days=365))].value.sum()
            eps = l4.eps_basic.sum(min_count=4)
            if dv > 0 and eps > 0: d["pay"] = min(dv / eps, 1.5)
        rows.append(d)
    return pd.DataFrame(rows)

def score(df, use_c=True):
    """within-sector percentile ranks, averaged over available components (a,b,c,d)."""
    df = df.copy()
    def rk(col, mask=None):
        x = df[col] if mask is None else df[col].where(mask)
        return x.groupby(df.sector).rank(pct=True)
    fbm = df.roe.isna() & df.roe_fb.notna(); a = rk("roe").fillna(rk("roe_fb", fbm))
    comps = pd.DataFrame({"a": a, "b": rk("cash"), "c": rk("stab") if use_c else np.nan, "d": rk("pay")})
    need = ["a", "b"] + (["c"] if use_c else [])
    df["q"] = comps.mean(axis=1).where(comps[need].notna().all(axis=1))
    df["fb"] = fbm
    return pd.concat([df, comps], axis=1)

def liquid_kmi(info, pos):
    liq = medtv.iloc[pos]; kmi = set(members("KMI_ALL_derived", info))
    return [s for s in close.columns if s in kmi and liq.get(s, 0) > 5e6]

def fwd(pos, months=12):
    tgt = days[pos] + pd.DateOffset(months=months)
    if LAST < tgt: return None
    end = days.searchsorted(tgt)
    return np.expm1(cumlog.iloc[min(end, len(days) - 1)] - cumlog.iloc[pos])

def pick(df, qcol="q"):
    top, bot, qarp, groups = [], [], [], []
    for sec, g in df.dropna(subset=[qcol]).groupby("sector"):
        n = len(g)
        if n < 3: continue
        k = max(1, round(n / 3)); g = g.sort_values(qcol, ascending=False)
        top += list(g.symbol[:k]); bot += list(g.symbol[-k:]); groups.append((list(g.symbol), k))
        h = g.iloc[: int(np.ceil(n / 2))]
        qarp += list(h.sort_values("ep", ascending=False).symbol[: int(np.ceil(len(h) / 2))])
    return top, bot, qarp, groups

# ---------------- formations
mon_first = pd.Series(days, days).groupby(days.to_period("M")).first()
def run(use_c, start, months=12):
    res = []
    for m, t in mon_first.items():
        if t < start: continue
        pos = days.get_loc(t); f = fwd(pos, months)
        if f is None: continue
        L = liquid_kmi(t, pos)
        df = raw_scores(t, pos); df = df[df.symbol.isin(L)]
        df = score(df, use_c); top, bot, qarp, groups = pick(df)
        if len(groups) < 3: continue
        k30 = [s for s in members("KMI30", t) if s in f.index]
        r = lambda L_: f.reindex(L_).mean()
        res.append(dict(t=t, n_scored=int(df.q.notna().sum()), n_sec=len(groups), n_top=len(top), fb=int(df.fb.sum()),
                        top=r(top), bot=r(bot), qarp=r(qarp), n_qarp=len(qarp), kmi=r(L), k30=r(k30),
                        scored_ew=f.reindex([s for g_, _ in groups for s in g_]).mean(),
                        qk=[(f.reindex(g_).values, k) for g_, k in groups]))
    return pd.DataFrame(res).set_index("t")

def stats(x, label):
    x = pd.Series(x).dropna()
    if not len(x): return out(f"{label:<46} n=0")
    out(f"{label:<46} n={len(x):<3} mean {pc(x.mean()):>7} median {pc(x.median()):>7} win {100*(x>0).mean():>4.0f}% worst {pc(x.min()):>7}")

def _one(groups):
    t, b = [], []
    for v, k in groups:
        p = rng.permutation(len(v)); t += list(v[p[:k]]); b += list(v[p[-k:]])
    return np.nanmean(t) - np.nanmean(b)
def _one_qarp(groups, bench):
    s = []
    for v, k in groups:
        n = len(v); p = rng.permutation(n); h = p[: int(np.ceil(n / 2))]; s += list(v[h[: int(np.ceil(len(h) / 2))]])
    return np.nanmean(s) - bench

def cohort_table(series, label):
    s = series.dropna(); out(f"  {label}: October cohorts " + ", ".join(f"{t:%Y-%m} {pc(v)}" for t, v in s[s.index.month == 10].items()))
    byoff = [x for x in (s[s.index.month == mth] for mth in range(1, 13)) if len(x)]
    ep = [x.mean() for x in byoff]
    out(f"  {label}: {len(byoff)} month-offsets, annual cohorts per offset {sorted(set(len(x) for x in byoff))}; mean of offset means {pc(np.mean(ep))}, offsets positive {sum(e > 0 for e in ep)}/{len(ep)}, worst offset mean {pc(min(ep))}")

# ---------------- main
nold = int((q.fiscal_quarter_end < pd.Timestamp("2021-09-30")).sum())
out(f"Quality within sector. Run 2026-10-18. Panel {len(days)} days to {LAST.date()}; adjusted total returns (cash dividends complete only from Nov 2024).")
out(f"quarterly_eps: {q.symbol.nunique()} names; rows with announce timestamp {q.announce_dt.notna().sum()}/{len(q)}; missing-timestamp rows assumed available at quarter end + {LAG95}d (95th pct of observed lag).")
out(f"Rows before 2021-09-30: {nold} of {len(q)}: the file is effectively 2021Q3-2026Q2 (20 quarters). 8-quarter EPS stability first computable Sep 2023.")
PRIM = run(True, pd.Timestamp("2023-09-01"))
EXT = run(False, pd.Timestamp("2022-11-01"))
out(f"\nPRIMARY (a,b,c; d only used from Nov 2025 so never in the backtest): formations {PRIM.index[0]:%Y-%m} to {PRIM.index[-1]:%Y-%m}, {len(PRIM)} monthly; scored names per formation median {PRIM.n_scored.median():.0f} (min {PRIM.n_scored.min()}, max {PRIM.n_scored.max()}); sectors with >=3 names median {PRIM.n_sec.median():.0f}; top-tercile names median {PRIM.n_top.median():.0f}; QARP names median {PRIM.n_qarp.median():.0f}; ROE fallback names median {PRIM.fb.median():.0f}")
out(f"EXTENDED (a,b only, needs 4 quarters): {EXT.index[0]:%Y-%m} to {EXT.index[-1]:%Y-%m}, {len(EXT)} monthly; scored median {EXT.n_scored.median():.0f}, sectors median {EXT.n_sec.median():.0f}")

def report(R, name):
    out(f"\n=== {name}: 12-month holds, overlapping monthly formations (percent)")
    R = R.copy(); R["spread"] = R.top - R.bot
    stats(R.top, "Top-third quality, raw"); stats(R.bot, "Bottom-third quality, raw")
    stats(R.spread, "Top minus bottom (within sector)")
    stats(R.top - R.scored_ew, "Top minus all scored names EW")
    stats(R.top - R.kmi, "Top minus EW liquid KMI")
    stats(R.qarp, "QARP raw")
    stats(R.qarp - R.kmi, "QARP minus EW liquid KMI")
    stats(R.qarp - R.k30, "QARP minus KMI30 members EW")
    stats(R.qarp - R.scored_ew, "QARP minus all scored EW (selection)")
    stats(R.kmi, "Benchmark: EW liquid KMI raw"); stats(R.k30, "Benchmark: KMI30 members EW raw")
    out("-- annual non-overlapping cohorts")
    cohort_table(R.spread, "top-bottom"); cohort_table(R.qarp - R.kmi, "QARP - KMI"); cohort_table(R.qarp - R.k30, "QARP - KMI30"); cohort_table(R.kmi, "KMI EW raw")
    out("-- placebo: random ranks within the same sectors, same counts, 2000 draws of the whole formation path")
    obs = R.spread.mean(); pb = np.array([np.mean([_one(g) for g in R.qk]) for _ in range(NDRAW)])
    out(f"  top-bottom mean {pc(obs)}; placebo mean {pc(pb.mean())}, 5-95% [{pc(np.percentile(pb,5))}, {pc(np.percentile(pb,95))}]; p(placebo >= obs) = {(pb >= obs).mean():.3f}")
    obs = (R.qarp - R.kmi).mean(); pq = np.array([np.mean([_one_qarp(g, b) for g, b in zip(R.qk, R.kmi)]) for _ in range(NDRAW)])
    out(f"  QARP-KMI mean {pc(obs)}; placebo mean {pc(pq.mean())}, 5-95% [{pc(np.percentile(pq,5))}, {pc(np.percentile(pq,95))}]; p(placebo >= obs) = {(pq >= obs).mean():.3f}")
    return R

RP = report(PRIM, "PRIMARY"); RE = report(EXT, "EXTENDED a,b only")

out("\n=== Splits and rerating")
out("The 2020-21 vs 2022-26 split is NOT possible: fundamentals start 2021Q3 and every formation date is Sep 2023 or later. Split used instead (formation date):")
for nm, R in (("PRIMARY", RP), ("EXTENDED", RE)):
    for lab, m in (("formed before 2024-09", R.index < "2024-09-01"), ("formed 2024-09 onwards", R.index >= "2024-09-01")):
        out(f"[{nm}] {lab}")
        stats((R.top - R.bot)[m], "  top-bottom"); stats((R.qarp - R.kmi)[m], "  QARP - KMI"); stats(R.kmi[m], "  KMI EW raw")
out("Every holding window sits inside the 2022-25 rerating or its tail, so it cannot be excluded by dropping dates. Reads that remove it: excess over the EW KMI basket (above) and the last cohort, formed Sep-Oct 2025:")
for nm, R in (("PRIMARY", RP), ("EXTENDED", RE)):
    m = R.index >= "2025-09-01"
    out(f"[{nm}] formed Sep-Oct 2025 (n={m.sum()}): top {pc(R.top[m].mean())}, bottom {pc(R.bot[m].mean())}, QARP {pc(R.qarp[m].mean())}, KMI EW {pc(R.kmi[m].mean())}, KMI30 EW {pc(R.k30[m].mean())}")
out("\nComponent check, top minus bottom on a single component (EXTENDED sample; exploratory)")
for comp in ("a", "b"):
    sp = {}
    for m, t in mon_first.items():
        if t < pd.Timestamp("2022-11-01"): continue
        pos = days.get_loc(t); f = fwd(pos)
        if f is None: continue
        L = liquid_kmi(t, pos); df = raw_scores(t, pos); df = score(df[df.symbol.isin(L)], False)
        df["q2"] = df[comp]; top, bot, _, g = pick(df, "q2")
        if len(g) >= 3: sp[t] = f.reindex(top).mean() - f.reindex(bot).mean()
    stats(pd.Series(sp), f"component {comp}")

out("\nEXTENDED (a,b only) restricted to the PRIMARY formation window (2023-09 onwards), to separate the effect of dropping (c) from the effect of the earlier window")
m = RE.index >= "2023-09-01"
stats((RE.top - RE.bot)[m], "  top-bottom"); stats((RE.qarp - RE.kmi)[m], "  QARP - KMI"); stats((RE.qarp - RE.k30)[m], "  QARP - KMI30")
out("EXTENDED formed 2022-11 to 2023-08 only (market rerating at its fastest)")
m = RE.index < "2023-09-01"
stats((RE.top - RE.bot)[m], "  top-bottom"); stats((RE.qarp - RE.kmi)[m], "  QARP - KMI"); stats(RE.kmi[m], "  KMI EW raw")

# ---------------- current screen
out(f"\n=== Current screen (as of 2026-10-18; prices to {LAST.date()}; quarters announced before then)")
pos = len(days) - 1; info = LAST + pd.Timedelta(days=1)
L = set(liquid_kmi(info, pos)); kmi_now = set(pd.read_csv(ROOT / "data/index_members/KMI_ALL_2026-06-05.csv").symbol)
df = raw_scores(info, pos); df = score(df[df.symbol.isin(L & kmi_now)], True)
df["qpct"] = df.q.groupby(df.sector).rank(pct=True)
cand = []
for sec, g in df.dropna(subset=["q"]).groupby("sector"):
    n = len(g)
    if n < 3: continue
    h = g.sort_values("q", ascending=False).iloc[: int(np.ceil(n / 2))]
    h = h.assign(ep_rank=h.ep.rank(pct=True))
    cand.append(h.sort_values("ep", ascending=False).iloc[: int(np.ceil(len(h) / 2))])
c = pd.concat(cand); c["order"] = (c.qpct + c.ep_rank) / 2; c = c.sort_values("order", ascending=False)
out(f"Liquid KMI names with a full score: {df.q.notna().sum()}; QARP-qualified: {len(c)}. Display order = mean of within-sector quality pct and E/P pct (display rule, not tested).")
out(f"{'sym':<8}{'sector':<32}{'Q':>5}{'ROE%':>7}{'cash':>6}{'CVeps':>7}{'pay':>6}{'E/P%':>7}")
nan = float("nan")
for r in c.head(10).itertuples():
    out(f"{r.symbol:<8}{r.sector[:31]:<32}{r.q:>5.2f}{r.roe*100 if pd.notna(r.roe) else nan:>7.1f}{r.cash:>6.2f}{-r.stab if np.isfinite(r.stab) else nan:>7.2f}{r.pay if pd.notna(r.pay) else nan:>6.2f}{r.ep*100:>7.1f}")
out("ROE = TTM net income / fiscal-year-end equity (nan = fallback used); CVeps = coefficient of variation of last 8 quarterly EPS (lower is steadier); pay = trailing 12m dividends / TTM EPS where recorded.")
out("Rank 11-20 for context: " + ", ".join(f"{r.symbol}({r.q:.2f})" for r in c.iloc[10:20].itertuples()))
(ROOT / "tests/out/quality_within_sector.txt").write_text(buf.getvalue(), encoding="utf-8")
