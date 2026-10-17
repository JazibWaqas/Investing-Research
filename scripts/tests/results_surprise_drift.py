"""Results surprise, drift, leakage, muted-reaction value setup, board-notice effect (PSX).
Run: .venv/Scripts/python.exe -I scripts/tests/results_surprise_drift.py
Prints and saves tests/out/results_surprise_drift.txt. Write-up: tests/results_surprise_drift.md.
YoY change in net income is NOT a consensus surprise (no consensus data exists).
Downloads filing PDFs for the EPS spot-check (1 request per second) to data/raw/filings/; parses text only, never executes.
"""
import sys, io, re, calendar, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P
import psx_api

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
def fp(x, d=1):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:+.{d}%}"
def fn(x, d=2):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}"

COST, NPL, SEED, LAST = 0.005, 20, 20261017, pd.Timestamp("2026-10-16")
P1 = (pd.Timestamp("2020-10-01"), pd.Timestamp("2023-12-31"))
P2 = (pd.Timestamp("2024-01-01"), LAST)
FIL = ROOT / "data" / "raw" / "filings"
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- panel, returns, engine
close, vol, tv = P.load_panel()
dates, N = close.index, len(close.index)
cols = list(close.columns); cidx = {s: i for i, s in enumerate(cols)}
acts_nc = P.load_actions().query("type!='cash'")
ret_pr = P.returns(close, "adjusted", actions=acts_nc)       # bonus/split only (primary)
ret_tr = P.returns(close, "adjusted")                        # total return (robustness, t0 >= 2024-11)
mkt_pr, mkt_tr = P.ew_market(ret_pr), P.ew_market(ret_tr)
liq = (P._med_tv(tv) > 5e6).reindex(index=dates, columns=cols, fill_value=False).values
traded = close.notna().values
prA = pd.read_parquet(ROOT / "data" / "panel_close_adj_pricereturn.parquet").reindex(index=dates, columns=cols)
prF = prA.ffill().values
rawF = close.ffill().values

class Eng:
    def __init__(s, ret, mkt):
        s.cum = (1 + ret.fillna(0)).cumprod().where(close.notna().cummax()).values
        s.cnt = close.notna().cumsum().values
        s.cm = (1 + mkt.reindex(dates).fillna(0)).cumprod().values
    def win(s, sym, ia, ib):
        """excess return close(ia)->close(ib); code 0 ok, 1 window outside panel, 2 no observation in window."""
        ia, ib, sym = np.asarray(ia), np.asarray(ib), np.asarray(sym)
        inc = (ia < 0) | (ib >= N) | (ia >= ib)
        a, b = np.clip(ia, 0, N - 1), np.clip(ib, 0, N - 1)
        nobs = s.cnt[b, sym] - s.cnt[a, sym]
        v = (s.cum[b, sym] / s.cum[a, sym] - 1) - (s.cm[b] / s.cm[a] - 1)
        code = np.where(inc, 1, np.where((nobs <= 0) | np.isnan(v), 2, 0))
        return np.where(code == 0, v, np.nan), code
ENG, ENG_TR = Eng(ret_pr, mkt_pr), Eng(ret_tr, mkt_tr)

out("== RESULTS SURPRISE / DRIFT / LEAKAGE / MUTED VALUE / BOARD NOTICE (PSX). Panel", close.shape, dates[0].date(), "to", dates[-1].date())
out("Returns: primary = bonus/split-only price returns; benchmark = equal-weight market (Rs5m filter) from the same method; cost 0.5% per tradable leg.")
chk = (ENG.cum[-1] / ENG.cum)  # factor from each day to end
ref = prF[-1] / prF
m = np.isfinite(chk) & np.isfinite(ref) & liq
out(f"Sanity: compounded-return panel vs data/panel_close_adj_pricereturn.parquet ratio, liquid name-days: median abs diff {np.nanmedian(np.abs(chk[m] / ref[m] - 1)):.4%}, share >1% {np.mean(np.abs(chk[m] / ref[m] - 1) > 0.01):.2%}")

# ---------------------------------------------------------------- announcements
ann = pd.read_parquet(ROOT / "data" / "announcements.parquet")
ann["dt"] = ann.datetime.dt.tz_localize(None)
fr = ann[ann.klass == "financial_result"].copy()
low = fr.title.str.lower()
fr["is_trans"] = low.str.contains("transmission|annual report")
fr["bad"] = low.str.contains("revoked|other than|board meeting|conclusion|transmission|annual report") | ~low.str.contains("result")
MON = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
MON.update({m.lower(): i for i, m in enumerate(calendar.month_abbr) if m}); MON["sept"] = 9
def parse_period(t):
    t = t.lower()
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", t)
    try:
        if m: return pd.Timestamp(int(m[1]), int(m[2]), int(m[3]))
        m = re.search(r"(\d{1,2})[-./](\d{1,2})[-./](\d{4})", t)
        if m: return pd.Timestamp(int(m[3]), int(m[2]), int(m[1]))
        for m in re.finditer(r"([a-z]{3,9})\.?\s*(\d{1,2})\s*,?\s*(\d{4})", t):
            if m[1] in MON: return pd.Timestamp(int(m[3]), MON[m[1]], int(m[2]))
        for m in re.finditer(r"(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]{3,9})\.?,?\s*(\d{4})", t):
            if m[2] in MON: return pd.Timestamp(int(m[3]), MON[m[2]], int(m[1]))
    except ValueError:
        pass
    return pd.NaT
def kind(l):
    if "half" in l: return "H"
    if re.search(r"year|annual", l): return "Y"
    if re.search(r"quarter|quater|period", l): return "Q"
    return "U"
fr["pdate"] = [parse_period(t) for t in fr.title]
fr["kind"] = [kind(t.lower()) for t in fr.title]
FR = {s: g.sort_values("dt") for s, g in fr[~fr.bad].groupby("symbol")}

# ---------------------------------------------------------------- EPS events
e = pd.read_csv(ROOT / "data" / "fundamentals" / "quarterly_eps.csv", parse_dates=["fiscal_quarter_end"])
e = e.rename(columns={"fiscal_quarter_end": "qe"})
out(f"\n== 0. DATA CHECKS\nEPS file rows {len(e)}, symbols {e.symbol.nunique()}, qe {e.qe.min().date()} to {e.qe.max().date()}, duplicate (symbol, qe) rows {e.duplicated(['symbol','qe']).sum()}")
# announce_dt strings carry +05:00; parse keeping the Karachi wall time
assert e.symbol.isin(cidx).all(), "EPS symbol missing from price panel"
e["cur"] = pd.to_datetime(e.announce_dt.str.slice(0, 19), errors="coerce")
e["cur_trans"] = e.announce_title.fillna("").str.lower().str.contains("transmission|annual report")
ME = pd.offsets.MonthEnd(0)
def mshift(qe, months): return qe + pd.DateOffset(months=months) + ME
ix = e.set_index(["symbol", "qe"])
def look(col, shift):
    k = list(zip(e.symbol, [mshift(q, shift) for q in e.qe]))
    return ix[col].reindex(pd.MultiIndex.from_tuples(k, names=["symbol", "qe"])).values
e["ni_ly"], e["eps_ly"] = look("net_income", -12), look("eps_basic", -12)
e["ttm_eps"] = e.eps_basic.values + look("eps_basic", -3) + look("eps_basic", -6) + look("eps_basic", -9)
e["ttm_ni"] = e.net_income.values + look("net_income", -3) + look("net_income", -6) + look("net_income", -9)

# fiscal year end month per symbol (quarter type)
fym = {}
y = fr[(fr.kind == "Y") & ~fr.is_trans & ~fr.bad & fr.pdate.notna()]
for s, g in y.groupby("symbol"): fym[s] = int(g.pdate.dt.month.mode().iloc[0])
yt = e[e.announce_title.fillna("").str.lower().str.contains("year ended") & ~e.cur_trans]
for s, g in yt.groupby("symbol"):
    if s not in fym: fym[s] = int(g.qe.dt.month.mode().iloc[0])
def qtype(s, qe):
    if s not in fym: return "NA"
    return {0: "Q4", 3: "Q1", 6: "Q2", 9: "Q3"}.get((qe.month - fym[s]) % 12, "NA")
e["qtype"] = [qtype(s, q) for s, q in zip(e.symbol, e.qe)]
out(f"Fiscal year-end month resolved for {len(set(fym) & set(e.symbol))} of {e.symbol.nunique()} symbols; quarter type counts {e.qtype.value_counts().to_dict()}")

# earliest financial-result release in [qe+7d, current announce_dt]
new, newdoc, moved, shift_days, trans_only = [], [], [], [], 0
for r in e.itertuples():
    if pd.isna(r.cur):
        new.append(pd.NaT); newdoc.append(""); continue
    g = FR.get(r.symbol)
    pick = None
    if g is not None:
        ok = (g.dt >= r.qe + pd.Timedelta(days=7)) & (g.dt <= r.cur)
        pd_ok = g.pdate.notna() & ((g.pdate - r.qe).abs() <= pd.Timedelta(days=4))
        und = g.pdate.isna()
        kind_ok = ((g.kind == "Y") & (r.qtype in ("Q4", "NA"))) | ((g.kind == "H") & (r.qtype in ("Q2", "NA"))) | \
                  ((g.kind == "Q") & (r.qtype != "Q4")) | (g.kind == "U")
        # a dated title for a different period is excluded by pd_ok; a quarter-type title for a Y/H period is excluded by kind_ok
        c = g[ok & (pd_ok | (und & kind_ok))]
        if len(c): pick = c.iloc[0]
    if pick is not None:
        new.append(pick["dt"]); newdoc.append(str(pick["document_ids"]).split(",")[0].strip())
    elif r.cur_trans:
        new.append(pd.NaT); newdoc.append(""); trans_only += 1
    else:
        new.append(r.cur); newdoc.append("" if pd.isna(r.announce_doc_id) else str(int(r.announce_doc_id)))
e["ann"], e["doc"] = new, newdoc
mv = e.ann.notna() & e.cur.notna() & (e.ann < e.cur)
sh = (e.cur - e.ann)[mv].dt.total_seconds() / 86400
out(f"Rows with joined announce_dt {e.cur.notna().sum()} (of which Transmission/Annual-Report title {int(e.cur_trans.sum())}); rows with NO announce_dt {e.cur.isna().sum()}; Transmission-only (no earlier result row found, dropped) {trans_only}")
out(f"announce_dt moved to an EARLIER release: {int(mv.sum())} events; median shift {sh.median():.1f} days, mean {sh.mean():.1f}, 90th pct {sh.quantile(.9):.1f}, max {sh.max():.1f}; moved events whose old stamp was a Transmission row: {int((mv & e.cur_trans).sum())}")
out("Dropped for no announce_dt (or transmission-only), by quarter-end year:", e[e.ann.isna()].groupby(e.qe.dt.year).size().to_dict(), "of rows by year", e.groupby(e.qe.dt.year).size().to_dict())
out(f"Stamp exactly 08:00 (placeholder-looking) among used announce_dt: {int((e.ann.dropna().dt.strftime('%H:%M') == '08:00').sum())} of {int(e.ann.notna().sum())}")

# t0 on the panel calendar with the 15:30 PKT rule
def t0_idx(ts):
    if pd.isna(ts): return -1
    after = ts.hour * 60 + ts.minute > 15 * 60 + 30
    i = dates.searchsorted(ts.normalize(), side="right" if after else "left")
    return int(i) if i < N else -1
e["i0"] = [t0_idx(t) for t in e.ann]
e["t0"] = [dates[i] if i >= 0 else pd.NaT for i in e.i0]
out(f"t0 computed for {int((e.i0 >= 0).sum())} events; announced after 15:30 (t0 next session): {int((e.ann.dropna().dt.hour*60 + e.ann.dropna().dt.minute > 930).sum())}")

# buckets on net income, cross-check on EPS
def bucket(x, ly):
    if pd.isna(x) or pd.isna(ly): return None
    if ly > 0:
        if x <= 0: return "PTL"
        g = x / ly - 1
        return "POS" if g > .3 else "NEG" if g < -.3 else "MID"
    return "LTP" if x > 0 else "LL"
e["bucket"] = [bucket(a, b) for a, b in zip(e.net_income, e.ni_ly)]
e["bucket_eps"] = [bucket(a, b) for a, b in zip(e.eps_basic, e.eps_ly)]
e["growth"] = np.where(e.ni_ly > 0, e.net_income / e.ni_ly - 1, np.nan)
both = e.bucket.notna() & e.bucket_eps.notna()
out(f"Rows with NI and NI one year earlier: {int(e.bucket.notna().sum())}; EPS bucket also defined {int(both.sum())}; share whose bucket changes if EPS replaces NI: {(e.bucket[both] != e.bucket_eps[both]).mean():.1%} ({int((e.bucket[both] != e.bucket_eps[both]).sum())} of {int(both.sum())})")
POSITIVE, NEGATIVE = ("POS", "LTP"), ("NEG", "PTL")
sec = pd.read_csv(ROOT / "data" / "symbols.csv").set_index("symbol").sectorName.to_dict()
e["sector"] = e.symbol.map(sec).fillna("UNK")

# point-in-time liquidity
e["s"] = e.symbol.map(cidx)
v = e.i0 >= 0
e["liq"] = False
e.loc[v, "liq"] = liq[e.i0[v].values, e.s[v].astype(int).values]
tst = e[v].sample(25, random_state=1)
assert all((r.symbol in P.liquid_universe(r.t0)) == bool(r.liq) for r in tst.itertuples()), "liquid matrix differs from liquid_universe"
base = e[v & e.bucket.notna()]
out(f"\nEvents with announce_dt, t0 and bucket: {len(base)} (LL included). After point-in-time liquidity filter (Rs5m, liquid_universe(t0)): {int(base.liq.sum())}. Symbols before/after: {base.symbol.nunique()} / {base[base.liq].symbol.nunique()}")
out("By t0 year, before -> after filter:", {int(y): f"{len(g)} -> {int(g.liq.sum())}" for y, g in base.groupby(base.t0.dt.year)})
M = base[base.liq].copy().sort_values(["t0", "symbol"]).reset_index(drop=True)
out("Bucket counts after filter:", M.bucket.value_counts().to_dict(), " (LL is reported as n only)")
M["season"] = M.t0.dt.year.astype(str) + "Q" + M.t0.dt.quarter.astype(str)
out(f"Events outside both sample-split periods (t0 before 2020-10-01): {int((M.t0 < P1[0]).sum())}")
LL = M[M.bucket == "LL"]
M = M[M.bucket != "LL"].reset_index(drop=True)
out(f"LL (loss to loss) n = {len(LL)}; removed from test sample. Test sample {len(M)} events, {M.symbol.nunique()} symbols, seasons {M.season.nunique()}")

# holding companies / groups (lesson 1)
comp = ann.drop_duplicates("symbol").set_index("symbol").company.to_dict()
hold = sorted(s for s in M.symbol.unique() if re.search(r"holding|group|investment|corporation", comp.get(s, ""), re.I))
known = [s for s in ["HUBC", "FFC", "MFL", "ENGRO", "EFERT", "LUCK", "MLCF", "DGKC", "NML", "NCPL", "PPL", "SNGP", "UBL", "MCB", "MEBL", "FFBL", "LCI", "PAEL", "DAWH", "SYS", "TRG", "AGP", "ABOT", "INDU", "GHNI", "HCAR", "PSO"] if s in set(M.symbol)]
out("Holding-company / group names in the sample (consolidation UNVERIFIED, lesson 1):")
out("  by company-name keyword (holding|group|investment|corporation):", ", ".join(f"{s}" for s in hold))
out("  commonly consolidating groups present in sample (my list, not verified from filings):", ", ".join(known))

# ---------------------------------------------------------------- basis check (restated EPS vs back-adjusted price)
out("\n-- Split/bonus basis check (5 names): StockAnalysis EPS/shares are restated to today's share basis; price must be the back-adjusted close")
bn = ["LUCK", "SYS", "LCI", "KOHC", "MTL"]
for s in bn:
    a = acts_nc[(acts_nc.symbol == s) & (acts_nc.ex_date >= "2020-10-01")].sort_values("ex_date")
    fac = float(np.prod(np.where(a.type == "split", a.value, 1 + a.value))) if len(a) else 1.0
    g = e[(e.symbol == s) & e.ttm_eps.notna() & (e.i0 >= 0)].sort_values("qe")
    if g.empty: continue
    r0 = g.iloc[0]
    i = r0.i0 + 4; sc = cidx[s]
    raw_px, adj_px = rawF[i, sc], prF[i, sc]
    sh = e[(e.symbol == s)].sort_values("qe").shares.values
    pe_adj = adj_px / r0.ttm_eps
    shares_latest = e[e.symbol == s].sort_values("qe").shares.iloc[-1]
    pe_cap = adj_px * shares_latest / r0.ttm_ni            # adj price x restated shares / TTM NI : independent of EPS column
    out(f"  {s}: cumulative bonus/split factor since 2020-10 = {fac:.3f} ({len(a)} actions); first TTM event {r0.qe.date()} t0 {r0.t0.date()}; raw close {raw_px:.2f}, adj close {adj_px:.2f} (raw/adj {raw_px/adj_px:.3f}); "
        f"restated TTM EPS {r0.ttm_eps:.2f}; P/E adj/EPS {pe_adj:.2f} vs adj x shares / TTM NI {pe_cap:.2f} (ratio {pe_adj/pe_cap:.3f}); NAIVE raw/EPS {raw_px/r0.ttm_eps:.2f} (off by x{(raw_px/r0.ttm_eps)/pe_adj:.2f}); "
        f"restated shares range {np.nanmin(sh):.0f} to {np.nanmax(sh):.0f}m")
out("  Reading: shares are constant (min~max) across the action, so EPS is on the post-action basis; adj-price/EPS equals market-cap/NI to within rounding; the naive raw-price/EPS error equals the action factor.")

# P/E at decision close(t0+4)
M["i4"] = M.i0 + 4
okp = (M.i4 < N) & (M.ttm_eps > 0)
M["px4"] = np.where(M.i4 < N, prF[np.minimum(M.i4, N - 1), M.s.astype(int)], np.nan)
M["pe4"] = np.where(okp, M.px4 / M.ttm_eps, np.nan)
# cross-section of P/E for the tercile variant: pit TTM from every event's t0 (age cap 140 sessions)
allv = e[(e.i0 >= 0) & e.ttm_eps.notna()]
tt = pd.DataFrame(np.nan, index=range(N), columns=range(len(cols)))
for r in allv.itertuples(): tt.iat[r.i0, int(r.s)] = r.ttm_eps
ttm_ff = tt.ffill(limit=140).values
pe_mat = np.where(ttm_ff > 0, prF / ttm_ff, np.nan)
pe_mat = np.where(liq, pe_mat, np.nan)
cut = np.full(N, np.nan)
for d in range(N):
    x = pe_mat[d][np.isfinite(pe_mat[d])]
    if len(x) >= 15: cut[d] = np.quantile(x, 1 / 3)
M["cut"] = np.where(M.i4 < N, cut[np.minimum(M.i4, N - 1)], np.nan)
M["tercile"] = M.pe4 <= M.cut

# ---------------------------------------------------------------- placebo draws
year_idx = {y: np.where(dates.year == y)[0] for y in sorted(set(dates.year))}
def draws(sym, base_i, years, minidx=0):
    D = -np.ones((len(sym), NPL), dtype=int)
    for k, (s, i, y) in enumerate(zip(sym, base_i, years)):
        c = year_idx[y]
        c = c[(c >= minidx) & (c != i)]
        c = c[traded[c, s] & liq[c, s]]
        if len(c): D[k, :min(NPL, len(c))] = rng.choice(c, size=min(NPL, len(c)), replace=False)
    return D
SYM, I0 = M.s.astype(int).values, M.i0.values
DR = draws(SYM, I0, M.t0.dt.year.values)
TR_MIN = int(dates.searchsorted(pd.Timestamp("2024-11-01")))
DR_TR = draws(SYM, I0, M.t0.dt.year.values, TR_MIN)

def run_window(eng, sym, base_i, L, D, spec, cost):
    ia, ib = spec(base_i, L)
    ev, code = eng.win(sym, ia, ib)
    s2 = np.repeat(sym[:, None], NPL, 1); L2 = np.repeat(L[:, None], NPL, 1)
    ia2, ib2 = spec(D, L2)
    pl, _ = eng.win(s2.ravel(), ia2.ravel(), ib2.ravel())
    pl = pl.reshape(D.shape); pl[D < 0] = np.nan
    return dict(ev=ev - cost, pl=pl - cost, code=code)
ZL = np.zeros(len(M), dtype=int)
def fixed(a, b): return lambda x, L: (x + a, x + b)
def W(a, b, cost=0.0, eng=ENG, D=None):
    return run_window(eng, SYM, I0, ZL, DR if D is None else D, fixed(a, b), cost)

# ---------------------------------------------------------------- stats
class Info:  # arrays aligned with a window result
    def __init__(s, sym, t0, season, sector):
        s.sym, s.t0, s.season, s.sector = np.asarray(sym), np.asarray(t0), np.asarray(season), np.asarray(sector)
INF = Info(M.symbol, M.t0, M.season, M.sector)

def summ(mask, R, inf=INF):
    mask = np.asarray(mask)
    ev, pl = R["ev"][mask], R["pl"][mask]
    ok = ~np.isnan(ev)
    d = dict(n=int(ok.sum()))
    if d["n"] == 0: return d
    x = ev[ok]; pv = pl[ok].ravel(); pv = pv[~np.isnan(pv)]
    sy, t0, se, sc = inf.sym[mask][ok], inf.t0[mask][ok], inf.season[mask][ok], inf.sector[mask][ok]
    w = int(np.argmin(x))
    sm = pd.Series(x).groupby(se).median()
    d.update(nsym=len(set(sy)), mean=x.mean(), med=np.median(x), win=(x > 0).mean(), worst=x[w], worst_who=f"{sy[w]} {pd.Timestamp(t0[w]).date()}",
             seas=len(sm), seas_med=sm.mean(), seas_pos=(sm > 0).mean(), clu=len(set(zip(sc, se))),
             pl_n=len(pv), pl_mean=pv.mean() if len(pv) else np.nan, pl_med=np.median(pv) if len(pv) else np.nan, pl_win=(pv > 0).mean() if len(pv) else np.nan)
    d["d_med"], d["d_win"] = d["med"] - d["pl_med"], d["win"] - d["pl_win"]
    return d
def per_masks(base_mask, t0s):
    t0s = pd.Series(t0s)
    return [("ALL", base_mask), ("2020-10..2023", base_mask & ((t0s >= P1[0]) & (t0s <= P1[1])).values), ("2024..2026-10", base_mask & ((t0s >= P2[0]) & (t0s <= P2[1])).values)]
def table(groups, R, inf=INF, t0s=None, periods=True):
    rows = []
    for g, m in groups:
        for p, mm in (per_masks(m, inf.t0) if periods else [("ALL", m)]):
            d = summ(mm, R, inf); d.update(grp=g, per=p); rows.append(d)
    return pd.DataFrame(rows)
def fmt(df, cl=("grp", "per", "n", "nsym", "mean", "med", "win", "worst", "worst_who", "seas", "seas_med", "seas_pos", "clu", "pl_n", "pl_mean", "pl_med", "pl_win", "d_med", "d_win")):
    d = df.copy()
    for c in cl:
        if c not in d: d[c] = np.nan
    for c in ("mean", "med", "worst", "seas_med", "pl_mean", "pl_med", "d_med"): d[c] = d[c].map(lambda x: fp(x))
    for c in ("win", "seas_pos", "pl_win", "d_win"): d[c] = d[c].map(lambda x: fp(x, 0).replace("+", "") if pd.notna(x) else "-")
    for c in ("n", "nsym", "seas", "clu", "pl_n"): d[c] = d[c].map(lambda x: "-" if pd.isna(x) else f"{int(x)}")
    d["worst_who"] = d["worst_who"].fillna("-")
    return d[list(cl)]
def show(title, df, **k):
    out(f"\n-- {title}"); out(fmt(df, **k).to_string(index=False))
def md(df, cl):
    d = fmt(df, cl=cl)
    return "| " + " | ".join(cl) + " |\n|" + "---|" * len(cl) + "\n" + "\n".join("| " + " | ".join(str(v) for v in r) + " |" for r in d.values)
MDS = {}

B = M.bucket.values
masks = {"POS": B == "POS", "LTP": B == "LTP", "NEG": B == "NEG", "PTL": B == "PTL", "MID": B == "MID"}
masks["Positive"] = masks["POS"] | masks["LTP"]; masks["Negative"] = masks["NEG"] | masks["PTL"]; masks["ALL"] = np.ones(len(M), bool)
GR = [(k, masks[k]) for k in ["POS", "LTP", "NEG", "PTL", "MID", "Positive", "Negative", "ALL"]]
out(f"\nSample used below: {len(M)} events; bucket n: " + ", ".join(f"{k} {int(m.sum())}" for k, m in GR) + f". LL n {len(LL)}.")
out("Naming: bucket = YoY change in attributable net income, NOT a surprise versus consensus (none exists). Excess = stock minus equal-weight market, net cost where tradable.")
out("win rate = share of events with excess (net of 0.5% where tradable) > 0. Seasons = calendar quarter of t0; 'seas_med' = mean over seasons of the season median; 'seas_pos' = share of seasons with positive median; clu = distinct (sector, season) pairs.")
out("Placebo: 20 random traded, liquid sessions per event, same symbol and calendar year, same window and cost; d_med / d_win = event minus placebo.")

# ---------------------------------------------------------------- windows
Rr = W(-1, 1)                                  # reaction (not tradable)
Rp5, Rp10 = W(-6, -1), W(-11, -1)              # pre-run (not tradable)
H1 = {h: W(1, 1 + h, COST) for h in (5, 20, 60)}
R5 = W(-1, 4)                                  # 5-session reaction used by H3
H3 = {h: W(5, 5 + h, COST) for h in (60, 120)}
out("\n-- Dropped events by reason per window (ALL buckets): code1 = window runs past the panel end, code2 = no price observation in the window")
for nm, R in [("reaction t0-1..t0+1", Rr), ("pre-run 5", Rp5), ("pre-run 10", Rp10), ("H1 +5", H1[5]), ("H1 +20", H1[20]), ("H1 +60", H1[60]), ("H3 +60", H3[60]), ("H3 +120", H3[120])]:
    out(f"  {nm}: no-observation {int((R['code'] == 2).sum())}, past panel end {int((R['code'] == 1).sum())}, valid {int((R['code'] == 0).sum())} of {len(M)}")

for h in (5, 20, 60):
    T = table(GR, H1[h]); show(f"H1 DRIFT, entry close(t0+1), exit close(t0+1+{h}), net 0.5%", T)
    MDS[f"H1_{h}"] = T
T = table(GR, Rr); show("REACTION close(t0-1)->close(t0+1) excess, NOT TRADABLE, no cost", T); MDS["REACT"] = T
T = table(GR, Rp5); show("H2 PRE-RUN close(t0-6)->close(t0-1), NOT TRADABLE, no cost", T); MDS["H2_5"] = T
T = table(GR, Rp10); show("H2 PRE-RUN close(t0-11)->close(t0-1), NOT TRADABLE, no cost", T); MDS["H2_10"] = T

out("\n-- H2 leakage test: is the Positive pre-run above both MID and the placebo?")
for nm, R in [("5-session", Rp5), ("10-session", Rp10)]:
    pos, mid, allm = summ(masks["Positive"], R), summ(masks["MID"], R), summ(masks["ALL"], R)
    # season-level paired difference Positive minus MID
    s_ = pd.DataFrame({"v": R["ev"], "se": M.season, "p": masks["Positive"], "m": masks["MID"]}).dropna(subset=["v"])
    sp = s_[s_.p].groupby("se").v.median(); sm_ = s_[s_.m].groupby("se").v.median()
    dd = (sp - sm_).dropna()
    out(f"  {nm}: Positive median {fp(pos['med'])} (mean {fp(pos['mean'])}), MID median {fp(mid['med'])}, ALL median {fp(allm['med'])}, placebo median {fp(pos['pl_med'])}; Positive-MID median gap {fp(pos['med']-mid['med'])}; Positive-placebo median gap {fp(pos['d_med'])}; seasons with Positive median > MID median: {(dd > 0).mean():.0%} of {len(dd)}")
    out(f"    leakage supported only if Positive exceeds both MID and placebo: {'YES' if (pos['med'] > mid['med'] and pos['d_med'] > 0) else 'NO'} on medians")

# ---------------------------------------------------------------- quarter type
QT = M.qtype.values
out("\n-- Bucket stats by quarter type (Q2 from half-year releases, Q4 derived as annual minus 9M; NA = fiscal year end unresolved)")
out(pd.crosstab(M.bucket, M.qtype).to_string())
QG = [(f"{g} {q}", masks[g] & (QT == q)) for g in ("Positive", "Negative", "MID", "ALL") for q in ("Q1", "Q2", "Q3", "Q4")]
for h in (20, 60):
    T = table(QG, H1[h], periods=False); show(f"H1 excess net at +{h} by quarter type", T); MDS[f"QT_{h}"] = T

# ---------------------------------------------------------------- total return robustness
out("\n-- ROBUSTNESS: TOTAL RETURN (cash dividends added; coverage complete only from Nov 2024), events with t0 >= 2024-11-01, placebo sessions also >= 2024-11-01")
late = (M.t0 >= pd.Timestamp("2024-11-01")).values
for h in (5, 20, 60):
    R = W(1, 1 + h, COST, ENG_TR, DR_TR)
    T = table([(k, m & late) for k, m in GR], R, periods=False); show(f"H1 total return, +{h} net", T); MDS[f"TR_{h}"] = T
    if h == 60: Rtr60 = R
    # same events, price-return, for comparison
    T2 = table([(k + " (price)", m & late) for k, m in GR if k in ("Positive", "Negative", "ALL")], H1[h], periods=False); show(f"  same events, price-return +{h} net", T2)

# ---------------------------------------------------------------- H3
pos_m, react = masks["Positive"], R5["ev"]
muted = np.abs(react) <= 0.03
pe = M.pe4.values
is26ref = ((M.sector == "REFINERY") & (M.t0.dt.year == 2026)).values
def dedupe(mask):
    keep, last = np.zeros(len(M), bool), {}
    for k in np.where(mask)[0][np.argsort(I0[np.where(mask)[0]], kind="stable")]:
        s_ = SYM[k]
        if s_ in last and I0[k] - last[s_] < 120: continue
        keep[k] = True; last[s_] = I0[k]
    return keep
base_h3 = pos_m & muted & (pe < 6)
G3 = {
    "H3 main: Positive, muted +-3%, P/E<6": base_h3,
    "H3 tercile: Positive, muted, P/E bottom tercile": pos_m & muted & M.tercile.values,
    "(a) Positive, P/E<6, any reaction": pos_m & (pe < 6),
    "(b) Positive, muted, P/E>=6": pos_m & muted & (pe >= 6),
    "main excl. 2026 refiners": base_h3 & ~is26ref,
    "main, 2026 refiners only": base_h3 & is26ref,
    "ref: all Positive (entry t0+5)": pos_m.copy(),
}
out(f"\n== H3 MUTED STRONG QUARTER. Positive n {int(pos_m.sum())}; with 5-session reaction and P/E available {int((pos_m & np.isfinite(pe) & np.isfinite(react)).sum())}; muted {int((pos_m & muted).sum())}; P/E<6 {int((pos_m & (pe<6)).sum())}; main (pre-dedupe) {int(base_h3.sum())}; tercile cut available for {int(np.isfinite(M.cut).sum())} of {len(M)} events")
out("Each H3 group is deduped to one setup per symbol per 120 sessions (first kept). 60/120-session windows usually include the next quarter's result. H3 is a subset of H1 Positive and is NOT independent confirmation.")
G3d = {k: (dedupe(v) if not k.startswith("ref") else v) for k, v in G3.items()}
for h in (60, 120):
    T = table(list(G3d.items()), H3[h]); show(f"H3 entry close(t0+5), exit +{h}, net 0.5%", T); MDS[f"H3_{h}"] = T
out("\nH3 groups: pre-dedupe n -> post-dedupe n: " + "; ".join(f"{k}: {int(G3[k].sum())} -> {int(G3d[k].sum())}" for k in G3))
mainm = G3d["H3 main: Positive, muted +-3%, P/E<6"]
out(f"H3 main: distinct symbols {len(set(SYM[mainm]))}, (sector, season) clusters {len(set(zip(M.sector[mainm], M.season[mainm])))}, sectors {M.sector[mainm].value_counts().to_dict()}")
out(f"Tercile cutoff on those dates: median {np.nanmedian(M.cut[mainm]):.2f}; absolute P/E<6 vs bottom tercile overlap: {int((mainm & G3d['H3 tercile: Positive, muted, P/E bottom tercile']).sum())} shared of {int(mainm.sum())}")

# ---------------------------------------------------------------- historical and live H3 lists
def drawdown(k):
    s_, i = SYM[k], I0[k] + 5
    if i >= N: return np.nan
    j = min(i + 120, N - 1)
    path = ENG.cum[i:j + 1, s_] / ENG.cum[i, s_] - 1
    return np.nanmin(path)
def listing(mask):
    rows = []
    for k in np.where(mask)[0]:
        rows.append(dict(symbol=M.symbol[k], qe=M.qe[k].date(), announce_dt=M.ann[k], t0=M.t0[k].date(), ni_growth=M.growth[k], react5=react[k], pe=pe[k],
                         ex60=H3[60]["ev"][k], ex120=H3[120]["ev"][k], mdd120=drawdown(k), doc=M.doc[k], ni=M.net_income[k], eps=M.eps_basic[k], i0=I0[k], s=SYM[k]))
    return pd.DataFrame(rows).sort_values("pe").reset_index(drop=True)
LIVEQ = pd.to_datetime(["2026-03-31", "2026-06-30", "2026-09-30"])
is_live = M.qe.isin(LIVEQ).values
hist = listing(mainm & ~is_live)
def pr_list(df, n=None):
    d = df.copy() if n is None else df.head(n).copy()
    for c in ("ni_growth", "react5", "ex60", "ex120", "mdd120"): d[c] = d[c].map(lambda x: fp(x))
    d["pe"] = d.pe.map(lambda x: fn(x, 2)); d["announce_dt"] = d.announce_dt.dt.strftime("%Y-%m-%d %H:%M")
    return d[["symbol", "qe", "announce_dt", "t0", "ni_growth", "react5", "pe", "ex60", "ex120", "mdd120"]]
out(f"\n== HISTORICAL H3 SETUPS (main definition, deduped, quarter ends before 2026-03-31): n = {len(hist)}. Ranked by LOWEST ex-ante trailing P/E at decision (not by outcome). ex60/ex120 are excess net of 0.5%; mdd120 = worst stock price drawdown from entry close(t0+5) within 120 sessions (not excess).")
LISTN = 20 if len(hist) > 40 else len(hist)
out(pr_list(hist, LISTN).to_string(index=False))
MDS["HIST"] = pr_list(hist, LISTN)
if len(hist): out(f"   all {len(hist)} setups: median ex60 {fp(hist.ex60.median())}, median ex120 {fp(hist.ex120.median())}; top-{LISTN} subset median ex60 {fp(hist.head(LISTN).ex60.median())}, ex120 {fp(hist.head(LISTN).ex120.median())}")

lv = M[is_live & pos_m & muted & (pe < 6)].index.values
lrows = []
for k in lv:
    ie = I0[k] + 5
    if I0[k] + 4 >= N: continue   # decision date after last close
    last_px = prF[N - 1, SYM[k]]
    ex_sf = np.nan; el = max(0, N - 1 - ie)
    if ie <= N - 1:
        a = ENG.cum[ie, SYM[k]]; b = ENG.cum[N - 1, SYM[k]]
        ex_sf = (b / a - 1) - (ENG.cm[N - 1] / ENG.cm[ie] - 1) - COST
    lrows.append(dict(symbol=M.symbol[k], qe=M.qe[k].date(), t0=M.t0[k].date(), ni_growth=M.growth[k], react5=react[k], pe_decision=pe[k], pe_today=last_px / M.ttm_eps[k], sessions_elapsed=el, excess_so_far_net=ex_sf, doc=M.doc[k], ni=M.net_income[k], eps=M.eps_basic[k], i0=I0[k], s=SYM[k]))
live = pd.DataFrame(lrows).sort_values("pe_decision").reset_index(drop=True) if lrows else pd.DataFrame()
out(f"\n== LIVE H3 SCREEN as of close {LAST.date()} (quarter ends 2026-03-31, 2026-06-30, 2026-09-30; decision close(t0+4) <= {LAST.date()}). UNRESOLVED, NOT EVIDENCE. Excess so far is net of 0.5% from entry close(t0+5); 'sessions elapsed' counts sessions since entry (0 = not yet entered). No per-symbol dedupe.")
if len(live):
    d = live.copy()
    for c in ("ni_growth", "react5", "excess_so_far_net"): d[c] = d[c].map(lambda x: fp(x))
    for c in ("pe_decision", "pe_today"): d[c] = d[c].map(lambda x: fn(x, 2))
    out(d[["symbol", "qe", "t0", "ni_growth", "react5", "pe_decision", "pe_today", "sessions_elapsed", "excess_so_far_net"]].to_string(index=False))
    MDS["LIVE"] = d[["symbol", "qe", "t0", "ni_growth", "react5", "pe_decision", "pe_today", "sessions_elapsed", "excess_so_far_net"]]
    out(f"   live n {len(live)}; with entry reached {int((live.sessions_elapsed > 0).sum())}; median excess so far (entered) {fp(live[live.sessions_elapsed>0].excess_so_far_net.median())}")
else:
    out("   (none)")
nlq = M[is_live].groupby(M.qe.dt.strftime("%Y-%m-%d")).size().to_dict()
out(f"   events in live quarter ends in the filtered sample: {nlq}; Positive among them: {int((is_live & pos_m).sum())}")

# ---------------------------------------------------------------- EPS spot check vs filing PDFs
def read_pdf(doc):
    import pdfplumber
    path = FIL / f"{doc}.pdf"
    if not path.exists():
        psx_api.download_document(doc, str(path))
    if path.read_bytes()[:5] != b"%PDF-":
        return None
    with pdfplumber.open(path) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages[:8])
def nums(text):
    v = []
    for m in re.finditer(r"\(?-?\d[\d,]*\.?\d*\)?", text):
        t = m.group(0); neg = t.startswith("(") or t.startswith("-")
        t = t.strip("()-").replace(",", "")
        try: v.append(-float(t) if neg else float(t))
        except ValueError: pass
    return np.array(v)
def spot(df):
    res = []
    for r in df.itertuples():
        if not r.doc or r.doc in ("nan", "None"): res.append(("unreadable", "no doc id", False, False)); continue
        try: txt = read_pdf(r.doc)
        except Exception as ex: res.append(("unreadable", f"download/parse error {type(ex).__name__}", False, False)); continue
        if txt is None or len(txt.strip()) < 200: res.append(("unreadable", "no text layer or not a PDF", False, False)); continue
        v = np.abs(nums(txt))
        if len(v) < 5: res.append(("unreadable", "no numbers", False, False)); continue
        F = prF[min(r.i0 + 4, N - 1), r.s]; F = rawF[min(r.i0 + 4, N - 1), r.s] / F if F > 0 else 1.0
        ni_ok = any(np.any(np.abs(v - abs(r.ni) * k) <= max(0.01 * abs(r.ni) * k, 0.6 * k)) for k in (1e6, 1e3, 1))
        eps_ok = any(np.any(np.abs(v - abs(r.eps) * f) <= max(0.03, 0.01 * abs(r.eps) * f)) for f in (1.0, F)) if pd.notna(r.eps) else False
        res.append(("matched" if ni_ok else "mismatched", f"NI {'found' if ni_ok else 'not found'}, EPS {'found' if eps_ok else 'not found'} (incl. x{F:.2f} action factor)", ni_ok, eps_ok))
    return res
out("\n== EPS SPOT-CHECK against filing PDFs (earliest result row's document; PDFs saved under data/raw/filings/, parsed as text only). 'matched' = StockAnalysis net income found in the PDF numbers (Rs, Rs'000 or Rs m, 1% tolerance); EPS also tried at restated value and at value x action factor.")
for nm, df in [("historical H3 list", hist.head(LISTN)), ("live H3 list", live)]:
    if not len(df): out(f"  {nm}: empty"); continue
    r_ = spot(df)
    c = pd.Series([x[0] for x in r_]).value_counts().to_dict()
    out(f"  {nm}: n {len(df)}; matched {c.get('matched',0)}, mismatched {c.get('mismatched',0)}, unreadable {c.get('unreadable',0)}; EPS also found in {sum(x[3] for x in r_)}")
    for (k, rr), x in zip(df.iterrows(), r_): out(f"    {rr.symbol} {rr.qe} doc {rr.doc}: {x[0]} - {x[1]}")

# ---------------------------------------------------------------- H4 board notices
out("\n== H4 BOARD MEETING NOTICES (2017-2026, announcements only, all panel names liquid at n0)")
nb = ann[(ann.klass == "board_meeting_notice") & (ann.dt >= "2017-01-01") & ann.symbol.isin(cidx)].copy()
tl = nb.title.str.lower()
rev, oth, inp = tl.str.contains("revoked"), tl.str.contains("other than"), tl.str.contains("in progress")
out(f"notices 2017+ in panel names: {len(nb)}; REVOKED {int(rev.sum())}; 'other than financial results' {int((oth & ~rev).sum())}; 'in progress' (same-day, excluded) {int((inp & ~rev & ~oth).sum())}")
nb = nb[~rev & ~oth & ~inp].sort_values("dt")
res = fr[~fr.bad][["symbol", "dt"]].drop_duplicates().rename(columns={"dt": "rdt"}).sort_values("rdt")
mg = pd.merge_asof(nb[["symbol", "dt", "title"]], res, left_on="dt", right_on="rdt", by="symbol", direction="forward", tolerance=pd.Timedelta(days=30), allow_exact_matches=False)
out(f"kept notices {len(mg)}; matched to a result within 30 days {int(mg.rdt.notna().sum())}")
mg = mg.dropna(subset=["rdt"]).sort_values("dt").groupby(["symbol", "rdt"], as_index=False).first()
out(f"after earliest-notice-per-result dedupe: {len(mg)} notice-result pairs")
mg["in0"] = [t0_idx(t) for t in mg.dt]; mg["it0"] = [t0_idx(t) for t in mg.rdt]
mg = mg[(mg.in0 >= 1) & (mg.it0 >= 0)]
mg["L"] = mg.it0 - 1 - mg.in0
out(f"leg shorter than 1 session (notice and result too close), dropped: {int((mg.L < 1).sum())}")
mg = mg[mg.L >= 1].reset_index(drop=True)
mg["s"] = mg.symbol.map(cidx)
mg["liq"] = liq[mg.in0.values, mg.s.values]
out(f"pairs before liquidity filter {len(mg)}; after point-in-time Rs5m filter at n0: {int(mg.liq.sum())}; median leg length {mg[mg.liq].L.median():.0f} sessions, mean {mg[mg.liq].L.mean():.1f}")
H = mg[mg.liq].reset_index(drop=True)
H["n0"] = dates[H.in0.values]; H["t0"] = dates[H.it0.values]
H["season"] = H.t0.dt.year.astype(str) + "Q" + H.t0.dt.quarter.astype(str)
H["sector"] = H.symbol.map(sec).fillna("UNK")
H4S, H4I, H4L = H.s.values, H.in0.values, H.L.values
DR4 = draws(H4S, H4I, H.n0.dt.year.values)
INF4 = Info(H.symbol, H.n0, H.season, H.sector)
R4a = run_window(ENG, H4S, H4I, H4L, DR4, lambda x, L: (x - 1, x), 0.0)
R4b = run_window(ENG, H4S, H4I, H4L, DR4, lambda x, L: (x, x + L), COST)
out(f"dropped for no price observation / past panel end: notice-day {int((R4a['code']==2).sum())}/{int((R4a['code']==1).sum())}; tradable leg {int((R4b['code']==2).sum())}/{int((R4b['code']==1).sum())} of {len(H)}")
Q4 = [("2017-2021", (H.n0.dt.year <= 2021).values), ("2022-2026", (H.n0.dt.year >= 2022).values)]
G4 = [("ALL", np.ones(len(H), bool))] + Q4
def t4(R):
    rows = []
    for g, m in G4:
        d = summ(m, R, INF4); d.update(grp=g, per="n0 year"); rows.append(d)
    return pd.DataFrame(rows)
T = t4(R4a); show("H4 (i) notice-day excess close(n0-1)->close(n0), DESCRIPTIVE not tradable", T); MDS["H4a"] = T
T = t4(R4b); show("H4 (ii) tradable leg close(n0)->close(t0-1) excess net 0.5%, exit before the result", T); MDS["H4b"] = T
out("   window length varies by notice; placebo uses the same length at random sessions of the same symbol and year. The leg is a pre-result run-up and overlaps the H2 pre-run window: do not add H2 and H4.")

# ---------------------------------------------------------------- save
out("\n== MARKDOWN TABLES (generated)")
MC = ["grp", "per", "n", "nsym", "mean", "med", "win", "worst", "seas", "seas_pos", "pl_n", "pl_med", "pl_win", "d_med", "d_win"]
for k, v in MDS.items():
    if k in ("HIST", "LIVE"):
        out(f"\n[{k}]"); out("| " + " | ".join(v.columns) + " |\n|" + "---|" * len(v.columns) + "\n" + "\n".join("| " + " | ".join(str(x) for x in r) + " |" for r in v.values))
    else:
        out(f"\n[{k}]"); out(md(v, MC))
(ROOT / "tests" / "out" / "results_surprise_drift.txt").write_text(buf.getvalue(), encoding="utf-8")
