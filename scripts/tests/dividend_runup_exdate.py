"""Dividend run-ups, ex-date behaviour, cut drift and dividend calendar (quant review, 17 Oct 2026).
Run: .venv/Scripts/python.exe scripts/tests/dividend_runup_exdate.py
Prints and saves tests/out/dividend_runup_exdate.txt, writes catalysts/dividend_calendar.csv.
Write-up: tests/dividend_runup_exdate.md. Reuses scripts/prices.py. Nothing is committed.
"""
import sys, io, re, glob, calendar
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")

rng = np.random.default_rng(17102026)
COST, WHT, YHI = 0.005, 0.85, 0.08
W0, W1 = pd.Timestamp("2024-11-01"), pd.Timestamp("2026-10-16")   # cash coverage window
Y0 = pd.Timestamp("2025-11-01")                                  # trailing-yield validity
NPL, NDRAW = 20, 1000

# ------------------------------------------------------------------ panel, returns, matrices
close, vol, tv = P.load_panel()
dates, cols = close.index, list(close.columns)
T, N = len(dates), len(cols)
cidx = {s: k for k, s in enumerate(cols)}
LAST = T - 1
acts_g = P.load_actions()
acts_n = acts_g.copy(); acts_n.loc[acts_n.type == "cash", "value"] *= WHT
ret_g = P.returns(close, "adjusted", actions=acts_g)
ret_n = P.returns(close, "adjusted", actions=acts_n)
mk_g, mk_n = P.ew_market(ret_g).reindex(dates).fillna(0), P.ew_market(ret_n).reindex(dates).fillna(0)
cum = lambda r: np.log1p(r.clip(lower=-0.999).fillna(0)).cumsum().values
CG, CN = cum(ret_g), cum(ret_n)
CMG, CMN = np.log1p(mk_g.values).cumsum(), np.log1p(mk_n.values).cumsum()
cff = close.ffill().values                      # raw close, carried forward
TRD = close.notna().values
LIQ = (P._med_tv(tv) > 5e6).reindex(index=dates, columns=cols, fill_value=False).values
for d in ["2025-03-03", "2026-01-15", "2026-10-16"]:   # check against the shared loader
    lu = set(P.liquid_universe(pd.Timestamp(d)))
    assert lu == {c for c, v in zip(cols, LIQ[dates.searchsorted(pd.Timestamp(d))]) if v}, d

KM = np.zeros((T, N), bool)
snaps = sorted(glob.glob(str(ROOT / "data/index_members/KMI_ALL_derived_*.csv")))
snap_d = [pd.Timestamp(re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1)) for f in snaps]
for k, (f, d) in enumerate(zip(snaps, snap_d)):
    nxt = snap_d[k + 1] if k + 1 < len(snaps) else pd.Timestamp("2100-01-01")
    m = (dates >= d) & (dates < nxt)
    ix = [cidx[s] for s in pd.read_csv(f).symbol if s in cidx]
    KM[np.ix_(m, ix)] = True

def exc(s, i, j, net=False):
    C, CM = (CN, CMN) if net else (CG, CMG)
    return np.expm1(C[j, s] - C[i, s]) - np.expm1(CM[j] - CM[i])
def stk(s, i, j):
    return np.expm1(CG[j, s] - CG[i, s])

# ------------------------------------------------------------------ corporate actions
ca = pd.read_csv(P.ACTIONS, parse_dates=["ex_date", "announce_dt"])
fx = {}   # symbol -> (ex dates array, factor array) for bonus/split: shares multiply by f
for r in ca[ca.type.isin(["bonus", "split"])].sort_values("ex_date").itertuples():
    f = 1 + r.value if r.type == "bonus" else r.value
    fx.setdefault(r.symbol, ([], []))
    fx[r.symbol][0].append(r.ex_date.to_datetime64()); fx[r.symbol][1].append(f)
fx = {s: (np.array(a, dtype="datetime64[ns]"), np.concatenate([[1.0], np.cumprod(b)])) for s, (a, b) in fx.items()}
def Fc(s, d):
    """cumulative share multiplier of all bonus/splits with ex date <= d (d scalar or array of datetime64)."""
    if s not in fx: return np.ones(np.shape(d)) if np.ndim(d) else 1.0
    xs, cp = fx[s]
    return cp[np.searchsorted(xs, np.asarray(d, dtype="datetime64[ns]"), side="right")]
def share_factor(s, lo, hi):
    """product of bonus/split multipliers with ex date in [lo, hi]."""
    return Fc(s, hi) / Fc(s, np.asarray(lo, dtype="datetime64[ns]") - np.timedelta64(1, "D"))

cash_all = ca[ca.type == "cash"].copy()
n_pre = int((cash_all.ex_date < W0).sum())
n_fut = int((cash_all.ex_date > W1).sum())
cash_all = cash_all[cash_all.ex_date >= W0].copy()
# a payouts row duplicating a seed row (same symbol, same amount, ex within 10 days): keep the seed ex date, borrow announce_dt
drop = []
for r in cash_all[cash_all.ex_date_source != "seed"].itertuples():
    sd = cash_all[(cash_all.symbol == r.symbol) & (cash_all.ex_date_source == "seed") & (cash_all.value == r.value)
                  & ((cash_all.ex_date - r.ex_date).abs() <= pd.Timedelta(days=10))]
    if len(sd):
        cash_all.loc[sd.index[0], "announce_dt"] = r.announce_dt; drop.append(r.Index)
n_dup = len(drop); cash_all = cash_all.drop(index=drop)

# ------------------------------------------------------------------ announcements
an = pd.read_parquet(ROOT / "data/announcements.parquet")
an["dt"] = an.datetime.dt.tz_localize(None)
an = an.sort_values("dt")
RES_OK = re.compile(r"financial (results?|statements?)", re.I)
RES_NO = re.compile(r"transmission|revoked|board meeting|shariah|fund|\betf\b|annual financial statements|audited|mutual", re.I)
is_res = (an.klass == "financial_result") & an.title.str.contains(RES_OK) & ~an.title.str.contains(RES_NO)
CREDIT = re.compile(r"credit|despatch|dispatch|unclaimed|daily dividend|warrant", re.I)
ab = an[an.klass.isin(["financial_result", "dividend_or_bonus"]) & ~an.title.str.contains(CREDIT)]
ab_by = {s: g for s, g in ab.groupby("symbol")}
res_df = an[is_res]
res_by = {s: g for s, g in res_df.groupby("symbol")}
DIVN = re.compile(r"dividend", re.I)
decl_notice = an[(an.klass == "dividend_or_bonus") & an.title.str.contains(DIVN) &
                 an.title.str.contains(r"book closure|entitlement|announcement", case=False) & ~an.title.str.contains(CREDIT)]
dn_by = {s: g.dt.values for s, g in decl_notice.groupby("symbol")}
unp = pd.read_csv(ROOT / "data/corporate_actions_unplaced.csv", parse_dates=["announce_dt"])
unp = unp[unp.type == "cash"]
unp_by = {s: g.announce_dt.values for s, g in unp.groupby("symbol")}

def parse_period(title):
    t = title.lower()
    mon = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
    mon.update({m.lower(): i for i, m in enumerate(calendar.month_abbr) if m})
    m = re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", t)
    if m: return int(m[1]), int(m[2])
    m = re.search(r"\b(\d{1,2})[-/. ](\d{1,2})[-/. ](\d{4})", t)
    if m:
        a, b, y = int(m[1]), int(m[2]), int(m[3])
        return (y, b) if b <= 12 else (y, a)
    m = re.search(r"\b([a-z]{3,9})\.?\s*(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})", t)
    if m and m[1] in mon: return int(m[3]), mon[m[1]]
    m = re.search(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]{3,9})\.?,?\s*(\d{4})", t)
    if m and m[2] in mon: return int(m[3]), mon[m[2]]
    m = re.search(r"\b([a-z]{3,9})\.?,?\s*(\d{4})", t)
    if m and m[1] in mon: return int(m[2]), mon[m[1]]
    return None

def t0pos(ts):
    """first tradable session: announcement day if stamped before 15:30 PKT and the day is a session, else the next session."""
    if pd.isna(ts): return -1
    d = ts.normalize(); p = int(dates.searchsorted(d))
    if p < T and dates[p] == d and ts.hour * 60 + ts.minute >= 930: p += 1
    return p if p < T else -1

def decl_for(sym, ann, ex):
    """declaration timestamp per spec 0.3. Returns (ts, how)."""
    g = ab_by.get(sym)
    if pd.notna(ann):
        if g is not None:
            c = g[(g.dt > ann - pd.Timedelta(days=3)) & (g.dt < ann)]
            if len(c) and c.dt.min() < ann: return c.dt.min(), "announce_dt+ruleb"
        return ann, "announce_dt"
    r = res_by.get(sym)      # seed row with no announce_dt: latest true results announcement in the 75 days before ex
    if r is not None:
        c = r[(r.dt >= ex - pd.Timedelta(days=75)) & (r.dt < ex)]
        if len(c): return c.dt.max(), "seed_inferred_from_results"
    return pd.NaT, "none"

# ------------------------------------------------------------------ cash table with declaration times
cash_all["ann"] = cash_all.announce_dt
res = [decl_for(r.symbol, r.ann, r.ex_date) for r in cash_all.itertuples()]
cash_all["decl"] = [x[0] for x in res]; cash_all["how"] = [x[1] for x in res]
cash_all["T0"] = [t0pos(x) for x in cash_all.decl]
cash_all["inpanel"] = cash_all.symbol.isin(cidx)
cash_all["s"] = cash_all.symbol.map(cidx).fillna(-1).astype(int)
cash_all["expos"] = dates.searchsorted(cash_all.ex_date)
# linked results announcement and its period
def link_res(sym, ts):
    r = res_by.get(sym)
    if r is None or pd.isna(ts): return None
    c = r[(r.dt >= ts - pd.Timedelta(days=3)) & (r.dt <= ts + pd.Timedelta(days=1))]
    if not len(c): return None
    return c.iloc[(c.dt - ts).abs().argmin()]
lk = [link_res(r.symbol, r.decl) for r in cash_all.itertuples()]
cash_all["period"] = [parse_period(x.title) if x is not None else None for x in lk]
cash = cash_all[cash_all.ex_date <= W1].copy()          # test window rows with an outcome
fut = cash_all[cash_all.ex_date > W1]

out("=" * 100)
out("DIVIDEND RUN-UPS, EX-DATE BEHAVIOUR, CUT DRIFT AND CALENDAR  (run 2026-10-17)")
out("=" * 100)
out(f"Panel {close.shape[0]} sessions x {N} symbols to {dates[-1].date()}. Adjusted total returns; market = ew_market (Rs5m); net-of-WHT uses cash x0.85 in the actions table (market also net).")
out(f"Cash rows in corporate_actions.csv: {len(ca[ca.type=='cash'])}. Dropped: ex_date before {W0.date()}: {n_pre}. Future ex_date after {W1.date()} (calendar only): {n_fut}.")
out(f"Test-window cash rows after the seed/payouts duplicate fix: {len(cash)} ({n_dup} payouts duplicate of a seed row removed: seed ex date kept). By source: {cash.ex_date_source.value_counts().to_dict()}")
out(f"Symbols not in the price panel: {(~cash.inpanel).sum()}. Ex date not a session: {(dates[np.minimum(cash.expos, LAST)] != cash.ex_date).sum()}.")
out(f"Declaration time: {cash.how.value_counts().to_dict()}; missing: {(cash.T0 < 0).sum()}. Stamped at/after 15:30 PKT (T0 shifted to next session): {int((cash.decl.dt.hour*60+cash.decl.dt.minute >= 930).sum())} of {int(cash.decl.notna().sum())}.")
_h = cash.ann.dt.hour * 60 + cash.ann.dt.minute
out(f"Before spec rule 0.3(b): raw CA announce_dt stamps at/after 15:30 PKT: {int((_h >= 930).sum())} of {int(cash.ann.notna().sum())} rows with a stamp ({int(cash.ann.isna().sum())} rows have no announce_dt). Rule (b) moves the declaration to an earlier results/dividend row when one exists in the 3 days before, which removes most of the after-15:30 cases.")
cash = cash[cash.inpanel].copy()

# event positions per symbol for placebo exclusion (declaration, ex dates, results, bonus/split)
evpos = {}
def addev(s, p):
    if 0 <= p < T: evpos.setdefault(s, []).append(int(p))
for r in cash_all.itertuples():
    addev(r.s, r.T0); addev(r.s, r.expos)
for sym, g in res_by.items():
    if sym in cidx:
        for ts in g.dt: addev(cidx[sym], t0pos(ts))
for r in ca[ca.type.isin(["bonus", "split", "right"])].itertuples():
    if r.symbol in cidx: addev(cidx[r.symbol], dates.searchsorted(r.ex_date))

# ------------------------------------------------------------------ trailing yield matrix (spec 0.2)
def ty_matrix():
    TY = np.full((T, N), np.nan)
    pc = np.vstack([np.full((1, N), np.nan), cff[:-1]])          # raw close of the previous session
    rows = np.where(dates >= Y0)[0]
    td = dates[rows].values
    for sym, g in cash_all.groupby("symbol"):
        if sym not in cidx: continue
        s = cidx[sym]; acc = np.zeros(len(rows))
        for r in g.itertuples():
            ex = np.datetime64(r.ex_date)
            m = (ex > td - np.timedelta64(365, "D")) & (ex <= td - np.timedelta64(1, "D"))
            f = Fc(sym, td - np.timedelta64(1, "D")) / Fc(sym, ex - np.timedelta64(1, "D"))
            acc += np.where(m, r.value / f, 0.0)
        TY[rows, s] = acc
    full_zero = np.zeros(N, bool)
    TY2 = np.full((T, N), np.nan); TY2[rows] = 0.0
    has = np.array([c in set(cash_all.symbol) for c in cols])
    TY2[np.ix_(rows, np.where(has)[0])] = TY[np.ix_(rows, np.where(has)[0])]
    return TY2 / pc
TY = ty_matrix()
TY[:, ~(close.notna().values.any(axis=0))] = np.nan

# ------------------------------------------------------------------ generic machinery
def clusters(i, j):
    """merge events whose exposure sessions [i+1, j] overlap; return cluster id per event."""
    st, en = np.asarray(i) + 1, np.asarray(j)
    order = np.argsort(st, kind="stable"); cid = np.zeros(len(st), int); cur = -1; cend = -1
    for k in order:
        if st[k] > cend: cur += 1; cend = en[k]
        else: cend = max(cend, en[k])
        cid[k] = cur
    return cid

def prep(name, ev, eoff=0, need_trd=False):
    n0 = len(ev)
    ok = (ev.i + eoff < T) & (ev.i >= 0) & (ev.j <= LAST)
    ev = ev[ok]; n_h = n0 - len(ev)
    l1 = LIQ[ev.i + eoff, ev.s]; ev = ev[l1]; n_l = int((~l1).sum())
    k1 = KM[ev.i + eoff, ev.s]; ev = ev[k1]; n_k = int((~k1).sum())
    n_t = 0
    if need_trd:
        t1 = TRD[ev.i, ev.s]; ev = ev[t1]; n_t = int((~t1).sum())
    ev = ev.sort_values(["s", "i"]); keep = []; last = {}
    for r in ev.itertuples():
        if r.i + 1 > last.get(r.s, -1): keep.append(r.Index); last[r.s] = r.j
    n_e = len(ev); ev = ev.loc[keep]
    out(f"  [{name}] input {n0}; no data to window end {n_h}; illiquid {n_l}; not in KMI snapshot {n_k}; no trade at entry {n_t}; kept {n_e}; per-symbol overlap dropped {n_e-len(ev)}; final {len(ev)}")
    return ev.reset_index(drop=True)

def pool(s, L, eoff, need_trd, cond, kind, net, D, lo):
    ii = np.arange(lo, T - L)
    ii = ii[ii + eoff < T]
    m = LIQ[ii + eoff, s] & KM[ii + eoff, s]
    if need_trd or kind == "drop": m &= TRD[ii, s]
    if kind == "drop": m &= TRD[np.minimum(ii + 1, LAST), s]
    if cond is not None: m &= cond(ii, s)
    bad = np.zeros(T, bool)
    for e in evpos.get(s, []): bad[max(0, e - 5 - L): e + 6] = True
    m &= ~bad[ii]
    ii = ii[m]
    if kind == "exc": v = exc(s, ii, ii + L, net)
    elif kind == "raw": v = stk(s, ii, ii + L)
    else: v = (cff[ii, s] - cff[ii + 1, s]) / D
    return v

def st(x):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    if not len(x): return dict(n=0, mean=np.nan, med=np.nan, win=np.nan, worst=np.nan, best=np.nan)
    return dict(n=len(x), mean=x.mean(), med=np.median(x), win=(x > 0).mean(), worst=x.min(), best=x.max())
def pf(x, d=1): return "   n/a" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x*100:+.{d}f}%"
def pw(x): return "  n/a" if x is None or np.isnan(x) else f"{x*100:.0f}%"

RESULTS = []
HDR = ("{:<46s}{:>5s}{:>5s}{:>5s} |{:>8s}{:>8s}{:>5s}{:>8s}{:>8s} |{:>5s}{:>8s}{:>8s}{:>5s}{:>8s}{:>8s} |{:>8s}{:>8s}{:>5s} |{:>6s}{:>6s}"
       ).format("row", "n", "sym", "clu", "mean", "med", "win", "worst", "best", "clu", "mean", "med", "win", "worst", "best", "pl.mean", "pl.med", "win", "p_ev", "p_clu")
def header(): out(HDR)

def evaluate(name, ev, kind="exc", net=False, cost=0.0, sign=1.0, direction="ge", eoff=0, need_trd=False,
             cond=None, lo=None, vals=None, Ds=None, show=True, pl_kind=None, pl_net=None):
    """ev: DataFrame with s,i,j (and sym). vals: precomputed observed metric (else computed by kind).
    The same transform sign*v - cost is applied to observed values and placebo values."""
    lo = lo if lo is not None else int(dates.searchsorted(W0))
    if len(ev) == 0:
        out(f"{name:<46s}  no events"); return None
    s_, i_, j_ = ev.s.values, ev.i.values, ev.j.values
    if vals is None: vals = exc(s_, i_, j_, net) if kind == "exc" else stk(s_, i_, j_)
    v = sign * np.asarray(vals, float) - cost
    cid = clusters(i_, j_)
    cm = pd.Series(v).groupby(cid).mean()
    e, c = st(v), st(cm.values)
    # placebo
    pk = pl_kind or kind; pn = net if pl_net is None else pl_net
    pools, plv = [], []
    for k in range(len(ev)):
        D = Ds[k] if Ds is not None else None
        pv = sign * pool(s_[k], int(j_[k] - i_[k]), eoff, need_trd, cond, pk, pn, D, lo) - cost
        pools.append(pv)
        if len(pv): plv.append(rng.choice(pv, size=min(NPL, len(pv)), replace=False))
    plv = np.concatenate(plv) if plv else np.array([])
    ps = st(plv)
    has = np.array([len(p) > 0 for p in pools])
    p_ev = p_cl = np.nan
    if has.any():
        Dm = np.full((NDRAW, len(ev)), np.nan)
        for k, p in enumerate(pools):
            if len(p): Dm[:, k] = p[rng.integers(len(p), size=NDRAW)]
        med_e = np.nanmedian(Dm, axis=1)
        cmat = np.column_stack([np.nanmean(Dm[:, cid == q], axis=1) if has[cid == q].any() else np.full(NDRAW, np.nan) for q in range(cid.max() + 1)])
        med_c = np.nanmedian(cmat, axis=1)
        cmp = (lambda a, b: a >= b) if direction == "ge" else (lambda a, b: a <= b)
        p_ev, p_cl = cmp(med_e, e["med"]).mean(), cmp(med_c, c["med"]).mean()
    nsym = len(set(s_))
    out("{:<46s}{:>5d}{:>5d}{:>5d} |{:>8s}{:>8s}{:>5s}{:>8s}{:>8s} |{:>5d}{:>8s}{:>8s}{:>5s}{:>8s}{:>8s} |{:>8s}{:>8s}{:>5s} |{:>6.3f}{:>6.3f}".format(
        name[:46], e["n"], nsym, cid.max() + 1, pf(e["mean"]), pf(e["med"]), pw(e["win"]), pf(e["worst"]), pf(e["best"]),
        c["n"], pf(c["mean"]), pf(c["med"]), pw(c["win"]), pf(c["worst"]), pf(c["best"]), pf(ps["mean"]), pf(ps["med"]), pw(ps["win"]), p_ev, p_cl))
    RESULTS.append(dict(name=name, e=e, c=c, ps=ps, p_ev=p_ev, p_cl=p_cl, clu=int(cid.max() + 1), no_pool=int((~has).sum())))
    if show and len(cm) >= 3:
        loo = [np.median(np.delete(cm.values, k)) for k in range(len(cm))]
        out(f"    leave-one-cluster-out: cluster median ranges {pf(min(loo))} to {pf(max(loo))} (full {pf(c['med'])}); dropping the largest cluster by n leaves median {pf(np.median(np.delete(cm.values, int(np.bincount(cid).argmax()))))}")
    if show:
        out(f"    clusters of '{name}' (dates = first to last exposure session; mean = equal-weight over events; placebo events without pool: {int((~has).sum())})")
        for q in range(cid.max() + 1):
            m = cid == q
            out(f"      #{q+1:<3d} {dates[i_[m].min()+1].date()} to {dates[j_[m].max()].date()}  n={m.sum():<3d} mean {pf(cm.iloc[q])}  [{', '.join(sorted(set(ev.sym.values[m])))[:90]}]")
    return dict(v=v, cid=cid, cm=cm)

# =============================================================================== SAMPLE
out("\n" + "=" * 100 + "\nSECTION 0. SAMPLE\n" + "=" * 100)
mdist = cash_all.ex_date.dt.to_period("M").value_counts().sort_index()
out(f"Ex-date month distribution of the {len(cash_all)+0} cash rows with ex_date from {W0.date()} (includes {len(fut)} future-dated rows; {len(cash)} test-window rows after the in-panel filter):")
out("  all rows from Nov 2024:  " + ", ".join(f"{k}:{v}" for k, v in mdist.items()))
calm = cash_all.ex_date.dt.month.value_counts().sort_index()
out("  by calendar month (all rows from Nov 2024): " + ", ".join(f"{calendar.month_abbr[k]}:{v}" for k, v in calm.items()))
calt = cash.ex_date.dt.month.value_counts().sort_index()
out("  by calendar month (test window, ex <= 2026-10-16): " + ", ".join(f"{calendar.month_abbr[k]}:{v}" for k, v in calt.items()))
out("  Dec rows: %d (all) / %d (test), Jun rows: %d / %d, Oct rows: %d / %d" % (calm.get(12, 0), calt.get(12, 0), calm.get(6, 0), calt.get(6, 0), calm.get(10, 0), calt.get(10, 0)))
out(f"  Note: the spec quotes 379 rows from Nov 2024; that figure includes the {len(fut)} future-dated rows ({len(cash_all)} here after the duplicate fix). Rows with an outcome: {len(cash)}.")

# =============================================================================== H1
out("\n" + "=" * 100 + "\nH1. High yielders (trailing yield > 8%) rise before results / dividend announcement. Effective window from 2025-11-01.\n" + "=" * 100)
resx = []
for sym, g in res_by.items():
    if sym not in cidx: continue
    seen = set()
    for ts in g.dt:
        p = t0pos(ts)
        if p < 0 or ts < Y0 - pd.Timedelta(days=60) or p in seen: continue
        seen.add(p); resx.append((sym, cidx[sym], p, ts))
resx = pd.DataFrame(resx, columns=["sym", "s", "P0", "ts"])
out(f"Results announcements (financial_result, excluding transmissions/revoked/funds) for panel symbols, T0 dedupe by symbol+session: {len(resx)} since Sep 2025; titles-regex excluded {int(((an.klass=='financial_result')&~is_res).sum())} other financial_result rows overall.")
resx["after1530"] = resx.ts.dt.hour * 60 + resx.ts.dt.minute >= 930
resx = resx[resx.ts >= Y0 - pd.Timedelta(days=60)]
ev = resx.copy(); ev["j"] = ev.P0 - 1; ev["i"] = ev.j - 20
n0 = len(ev); ev = ev[(ev.i >= 0) & (dates[np.maximum(ev.i.values, 0)] >= Y0)]
out(f"H1a candidate results with window start >= {Y0.date()}: {len(ev)} (dropped {n0-len(ev)} with window start before it: trailing yield not valid). After-15:30 stamps among kept: {int(ev.after1530.sum())}.")
ev["ty"] = TY[ev.i, ev.s]
out(f"  trailing yield missing: {int(ev.ty.isna().sum())}; high (>8%): {int((ev.ty>YHI).sum())}; low (<=8%): {int((ev.ty<=YHI).sum())}")
ev = ev[ev.ty.notna()]
P0H1 = int(dates.searchsorted(Y0))
hi_c = lambda ii, s: TY[ii, s] > YHI
lo_c = lambda ii, s: TY[ii, s] <= YHI
header()
H1 = {}
for lab, sel, cd in [("high", ev.ty > YHI, hi_c), ("low", ev.ty <= YHI, lo_c)]:
    e2 = prep(f"H1a {lab}", ev[sel], eoff=21)
    H1[lab] = e2
    r = evaluate(f"H1a {lab} yield, 20s to pre-news, gross", e2, eoff=21, cond=cd, lo=P0H1, show=(lab == "high"))
    if lab == "high":
        evaluate("H1a high yield, net of WHT", e2, net=True, eoff=21, cond=cd, lo=P0H1, show=False)
        H1["vals"] = r
# paired cluster view: all events (high + low) in common clusters
allev = pd.concat([H1["high"].assign(g="high"), H1["low"].assign(g="low")], ignore_index=True)
allev["v"] = exc(allev.s.values, allev.i.values, allev.j.values)
allev["cid"] = clusters(allev.i.values, allev.j.values)
out("  H1a clusters (all eligible results windows): high-yield vs low-yield mean excess in the same episode")
rows = []
for q, g in allev.groupby("cid"):
    h, l = g[g.g == "high"].v, g[g.g == "low"].v
    rows.append((q, dates[g.i.min()+1].date(), dates[g.j.max()].date(), len(h), h.mean() if len(h) else np.nan, len(l), l.mean()))
    out(f"      #{q+1:<3d} {rows[-1][1]} to {rows[-1][2]}  high n={len(h):<3d} mean {pf(rows[-1][4])}   low n={len(l):<4d} mean {pf(rows[-1][6])}")
dd = pd.DataFrame(rows, columns=["q", "a", "b", "nh", "mh", "nl", "ml"]).dropna()
dd["d"] = dd.mh - dd.ml
out(f"  high minus low across clusters with both: n={len(dd)}, mean {pf(dd.d.mean())}, median {pf(dd.d.median())}, win {pw((dd.d>0).mean())}")
out("  Expected power: about one year of data and about 4 results seasons, so about 4 independent episodes at best.")

# H1b: enter after board meeting notice
out("\nH1b. Tradable: enter at close of first tradable session after the board_meeting_notice, exit at last pre-news close. Net of 0.5% cost.")
bm = an[(an.klass == "board_meeting_notice") & ~an.title.str.contains(r"revoked|emergent|other than", case=False)]
bm_by = {s: g.dt for s, g in bm.groupby("symbol")}
rows = []
for r in resx.itertuples():
    nt = bm_by.get(r.sym)
    if nt is None: continue
    c = nt[(nt < r.ts) & (nt >= r.ts - pd.Timedelta(days=30))]
    if not len(c): continue
    # a notice maps to the NEXT result of the symbol within 30 days; earlier results between are excluded by T0 ordering
    prev = resx[(resx.sym == r.sym) & (resx.ts < r.ts)].ts
    c = c[c > prev.max()] if len(prev) else c
    if not len(c): continue
    rows.append((r.sym, r.s, r.P0, r.ts, c.min()))
nb = pd.DataFrame(rows, columns=["sym", "s", "P0", "ts", "nts"])
nb["i"] = [t0pos(x) for x in nb.nts]; nb["j"] = nb.P0 - 1
out(f"  results with a matched notice (earliest notice in the 30 days before, after the previous result): {len(nb)} of {len(resx)}")
n0 = len(nb); nb = nb[(nb.i >= 0) & (nb.P0 - nb.i >= 2)]
out(f"  dropped, notice less than 2 sessions before the result: {n0-len(nb)}")
nb = nb[dates[nb.i.values] >= Y0]
nb["ty"] = TY[nb.i, nb.s]; nb = nb[nb.ty.notna()]
out(f"  entry >= {Y0.date()} with valid trailing yield: {len(nb)}; high {int((nb.ty>YHI).sum())}, low {int((nb.ty<=YHI).sum())}")
header()
for lab, sel, cd in [("high", nb.ty > YHI, hi_c), ("low", nb.ty <= YHI, lo_c)]:
    e2 = prep(f"H1b {lab}", nb[sel], need_trd=True)
    evaluate(f"H1b {lab} yield, notice to pre-news, net cost", e2, cost=COST, need_trd=True, cond=cd, lo=P0H1, show=(lab == "high"))

# =============================================================================== H2
out("\n" + "=" * 100 + "\nH2. Behaviour into and on the ex date. Test window 2024-11-01 to 2026-10-16.\n" + "=" * 100)
c2 = cash.copy()
c2["D"] = c2.value
oth = ca[ca.type.isin(["bonus", "split", "right"])][["symbol", "ex_date"]].drop_duplicates()
oth["same"] = True
c2 = c2.merge(oth, on=["symbol", "ex_date"], how="left"); c2["same"] = c2.same.fillna(False).astype(bool)
c2["srcok"] = c2.ex_date_source.isin(["payouts_book_closure", "seed", "pdf_book_closure"])
out(f"Rows: {len(c2)}. ex_date_source not in allowed set (approx/approx_wide/gap_inferred etc.): {int((~c2.srcok).sum())}. Same-day bonus/split/right: {int(c2.same.sum())}.")
c2 = c2[c2.srcok & ~c2.same].copy()
c2["i"] = c2.expos - 10; c2["j"] = c2.expos - 1
out(f"After source and same-day filters: {len(c2)}. Ex date later than last session or no session: {int((c2.expos > LAST).sum())}.")
c2 = c2[c2.expos <= LAST]
header()
# H2a
a = c2[c2.T0 >= 0].copy()
out(f"H2a: rows with a declaration time {len(a)} (missing: {len(c2)-len(a)}). T0 after ex-10 (ex-date not yet public at entry): {int((a.T0 > a.expos-10).sum())}.")
a = a[a.T0 <= a.expos - 10]
a = a[a.i >= 0]
ea = prep("H2a", a.assign(sym=a.symbol), need_trd=True)
evaluate("H2a run-up ex-10 to ex-1, net cost", ea, cost=COST, need_trd=True)
evaluate("H2a run-up, gross (descriptive)", ea, need_trd=True, show=False)
ea["yin"] = ea.value / cff[ea.i.values, ea.s.values]
evaluate("H2a run-up, D/close(ex-10) >= 2%, net cost", ea[ea.yin >= 0.02].reset_index(drop=True), cost=COST, need_trd=True, show=False)
evaluate("H2a run-up, D/close(ex-10) < 2%, net cost", ea[ea.yin < 0.02].reset_index(drop=True), cost=COST, need_trd=True, show=False)

# H2b
b = c2.copy(); b["sym"] = b.symbol
b = b[(b.expos >= 1) & (b.expos <= LAST)]
b["i"] = b.expos - 1; b["j"] = b.expos
n0 = len(b); b = b[TRD[b.j, b.s]]
out(f"H2b/H2c: ex session without a trade for the symbol: {n0-len(b)} dropped.")
b = prep("H2b/c", b, eoff=1)
b["cprev"] = cff[b.i, b.s]; b["cex"] = cff[b.j, b.s]
b["yld"] = b.D / b.cprev; b["ratio"] = (b.cprev - b.cex) / b.D
b["bucket"] = pd.cut(b.yld, [0, .02, .05, 10], labels=["<2%", "2-5%", ">5%"], right=False)
b["grp"] = np.where(b.ex_date_source.isin(["pdf_book_closure", "seed"]), "pdf/seed", "payouts")
out(f"H2b eligible events {len(b)}; by group {b.grp.value_counts().to_dict()}; by bucket {b.bucket.value_counts().to_dict()}")
out("H2b drop ratio = (raw close ex-1 - raw close ex) / gross dividend. Observed ratio and placebo (same symbol, random days, same dividend) in the 'mean/med' columns are ratios x100 shown as %.")
def dr(name, d, show=False):
    if len(d) == 0: out(f"{name:<46s}  no events"); return
    evaluate(name, d, kind="drop", vals=d.ratio.values, Ds=d.D.values, eoff=1, show=show)
sel = b.yld >= 0.02
dr("H2b drop ratio, yield>=2%, all", b[sel], show=True)
dr("H2b drop ratio, yield>=2%, pdf/seed", b[sel & (b.grp == "pdf/seed")])
dr("H2b drop ratio, yield>=2%, payouts", b[sel & (b.grp == "payouts")])
for bk in ["<2%", "2-5%", ">5%"]:
    dr(f"H2b drop ratio, {bk}", b[b.bucket == bk])
    for g in ["pdf/seed", "payouts"]:
        dr(f"H2b drop ratio, {bk}, {g}", b[(b.bucket == bk) & (b.grp == g)])
out("  Drop ratio detail (mean/median/share with ratio >= 1 / share > 0) by bucket:")
for lab, d in [("yield>=2%", b[sel]), ("yld>=2% pdf/seed", b[sel & (b.grp == "pdf/seed")]), ("yld>=2% payouts", b[sel & (b.grp == "payouts")]), ("<2%", b[b.bucket == "<2%"]), ("2-5%", b[b.bucket == "2-5%"]), (">5%", b[b.bucket == ">5%"])]:
    out(f"    {lab:<16s} n={len(d):<4d} mean ratio {d.ratio.mean():+.2f}  median {d.ratio.median():+.2f}  share>=1 {pw((d.ratio>=1).mean())}  share>0 {pw((d.ratio>0).mean())}  winsor-5/95 mean {d.ratio.clip(d.ratio.quantile(.05), d.ratio.quantile(.95)).mean():+.2f}  p25 {d.ratio.quantile(.25):+.2f}  p75 {d.ratio.quantile(.75):+.2f}")
out("H2b ex-day total-return excess vs ew_market (dividend added back once by the loader), gross and net WHT; windows are single sessions so clusters are ex-dates.")
header()
for lab, d in [("yield>=2%", b[sel]), ("<2%", b[b.bucket == "<2%"]), ("2-5%", b[b.bucket == "2-5%"]), (">5%", b[b.bucket == ">5%"])]:
    evaluate(f"H2b ex-day TR excess {lab}, gross", d, eoff=1, show=False)
    evaluate(f"H2b ex-day TR excess {lab}, net WHT", d, net=True, eoff=1, show=False)

# H2c
out("H2c dividend capture: (raw close ex + k*D)/raw close ex-1 - 1 - 0.5%, k=1 gross, k=0.85 net. Placebo = random-day total return (no dividend) in the same symbols, same transform.")
header()
mday = np.expm1(CMG[b.j.values] - CMG[b.i.values]); mdayn = np.expm1(CMN[b.j.values] - CMN[b.i.values])
for k, lab, mk in [(1.0, "gross D", mday), (WHT, "net 0.85D", mdayn)]:
    f = ((b.cex + k * b.D) / b.cprev - 1).values
    evaluate(f"H2c capture, {lab}, raw return", b, kind="raw", cost=COST, vals=f, need_trd=True, eoff=1, show=(k == 1.0), pl_net=False)
    evaluate(f"H2c capture, {lab}, excess vs mkt", b, kind="exc", cost=COST, vals=f - mk, need_trd=True, eoff=1, show=False, pl_net=False)
for lab, d in [("yield>=2%", b[sel]), (">5%", b[b.bucket == ">5%"])]:
    for k, kl in [(1.0, "gross"), (WHT, "net")]:
        f = ((d.cex + k * d.D) / d.cprev - 1).values
        evaluate(f"H2c capture {lab}, {kl}, raw return", d, kind="raw", cost=COST, vals=f, need_trd=True, eoff=1, show=False, pl_net=False)

# H2d
d_ = c2.copy(); d_["sym"] = d_.symbol; d_["i"] = d_.expos; d_["j"] = d_.expos + 10
n0 = len(d_); d_ = d_[d_.j <= LAST]
out(f"H2d: ex+10 beyond the last session: {n0-len(d_)} dropped.")
d_ = prep("H2d", d_, need_trd=True)
header()
evaluate("H2d buy ex close, hold 10, gross, net cost", d_, cost=COST, need_trd=True)
evaluate("H2d buy ex close, hold 10, net WHT, net cost", d_, net=True, cost=COST, need_trd=True, show=False)
others = sum(1 for r in d_.itertuples() if ((cash.symbol == r.symbol) & (cash.expos > r.i) & (cash.expos <= r.j)).any())
out(f"  H2d windows containing another ex-date of the same symbol (so gross vs net differ only there): {others} of {len(d_)}")

# =============================================================================== H3
out("\n" + "=" * 100 + "\nH3. December and June are dividend seasons with positive excess for high yielders. Valid months Dec 2025 and Jun 2026 (2 episodes).\n" + "=" * 100)
mons = pd.period_range("2025-11", "2026-10", freq="M")
out(f"{'month':<10s}{'formed':<12s}{'nElig':>6s}{'nHigh':>6s} | {'EW excess gross':>16s}{'net WHT':>9s}{'median':>9s}{'win':>6s}{'worst':>9s}{'best':>9s} | {'non-bucket':>10s} | {'p(rand names)':>13s}")
h3rows = {}
for m in mons:
    fi = int(dates.searchsorted(m.start_time)) - 1
    li = int(min(dates.searchsorted((m + 1).start_time) - 1, LAST))
    tag = " (partial to 10-16)" if m == pd.Period("2026-10") else ""
    if dates[fi] < Y0:
        out(f"{str(m):<10s}{str(dates[fi].date()):<12s}  trailing yield not valid before {Y0.date()}: not computed"); continue
    el = LIQ[fi] & KM[fi] & TRD[fi] & ~np.isnan(TY[fi])
    ix = np.where(el)[0]
    hi = ix[TY[fi, ix] > YHI]; lo_ = ix[TY[fi, ix] <= YHI]
    g, n_ = exc(hi, fi, li), exc(hi, fi, li, True)
    allx = exc(ix, fi, li)
    pr = np.array([rng.choice(allx, size=len(hi), replace=False).mean() for _ in range(NDRAW)]) if len(hi) <= len(ix) and len(hi) else np.array([np.nan])
    h3rows[str(m)] = (g.mean() if len(hi) else np.nan)
    out(f"{str(m)+tag:<10s}{str(dates[fi].date()):<12s}{len(ix):>6d}{len(hi):>6d} | {pf(g.mean()):>16s}{pf(n_.mean()):>9s}{pf(np.median(g)) if len(g) else '  n/a':>9s}{pw((g>0).mean()) if len(g) else '':>6s}{pf(g.min()) if len(g) else '':>9s}{pf(g.max()) if len(g) else '':>9s} | {pf(exc(lo_, fi, li).mean()):>10s} | {(pr >= g.mean()).mean() if len(hi) else np.nan:>13.3f}")
valid = [k for k in h3rows if k not in ("2026-10",)]
for tgt in ["2025-12", "2026-06"]:
    oth_ = [h3rows[k] for k in valid if k != tgt and not np.isnan(h3rows[k])]
    out(f"  month placebo for {tgt}: other valid months Nov-based list n={len(oth_)}, mean {pf(np.mean(oth_))}, median {pf(np.median(oth_))}, win {pw(np.mean(np.array(oth_)>0))}; share of other months with bucket excess >= {tgt}: {np.mean(np.array(oth_) >= h3rows[tgt]):.2f}")
out("  Episodes: 2 (Dec 2025, Jun 2026): not testable.")

# =============================================================================== H4
out("\n" + "=" * 100 + "\nH4. Dividend cut followed by negative drift. Events from T0 >= 2025-11-01.\n" + "=" * 100)
def match_prior(r):
    """prior-year same-period declaration of the same symbol. Returns (row or None, how)."""
    g = cash_all[(cash_all.symbol == r.symbol) & (cash_all.ex_date < r.ex_date - pd.Timedelta(days=200))]
    if r.period is not None:
        pp = (r.period[0] - 1, r.period[1])
        h = g[g.period == pp]
        if len(h): return h.iloc[0], "period"
    lo_, hi_ = r.ex_date - pd.Timedelta(days=365 + 61), r.ex_date - pd.Timedelta(days=365 - 61)
    if lo_ < W0: return None, "prior window before coverage"
    h = g[(g.ex_date >= lo_) & (g.ex_date <= hi_)]
    if len(h): return h.iloc[(h.ex_date - (r.ex_date - pd.Timedelta(days=365))).abs().argmin()], "ex-month"
    return None, "no prior"
dec = cash_all[(cash_all.T0 >= 0) & cash_all.inpanel].copy()
dec = dec[dates[dec.T0.clip(upper=LAST)] >= Y0]
out(f"Declarations (cash rows incl. {len(fut)} future-ex) with T0 >= {Y0.date()}: {len(dec)}")
cls = []
for r in dec.itertuples():
    pr, how = match_prior(r)
    if pr is None: cls.append((np.nan, np.nan, how, "unmatched")); continue
    prior_cur = pr.value / share_factor(r.symbol, pr.ex_date, r.ex_date - pd.Timedelta(days=1))
    ratio = r.value / prior_cur
    cls.append((prior_cur, ratio, how, "cut" if ratio < 0.99 else ("increase" if ratio > 1.01 else "flat")))
dec["prior"], dec["ratio"], dec["how"], dec["cls"] = zip(*cls)
out("  prior-year match: " + str(dec.how.value_counts().to_dict()))
out("  classification: " + str(dec.cls.value_counts().to_dict()))
out(f"  period parsed from linked results title: {int(dec.period.notna().sum())} of {len(dec)}")
cut_ev = dec[dec.cls == "cut"]
out("  Cuts (symbol, ex, amount, prior in current terms, ratio): " + "; ".join(f"{r.symbol} {r.ex_date.date()} {r.value:g} vs {r.prior:.3g} ({r.ratio:.2f})" for r in cut_ev.itertuples()))
# omissions
ro = resx.copy()
ro = ro[dates[ro.P0.clip(upper=LAST).values] >= Y0]
OM_LAST = pd.Timestamp("2026-09-15")
om, n_cov, n_np = [], 0, 0
for r in ro.itertuples():
    pers = None
    lr = res_by[r.sym][res_by[r.sym].dt == r.ts]
    pers = parse_period(lr.title.iloc[0]) if len(lr) else None
    g = cash_all[cash_all.symbol == r.sym]
    prior = pd.DataFrame()
    if pers is not None: prior = g[g.period == (pers[0] - 1, pers[1])]
    if not len(prior):
        prior = g[(g.decl >= r.ts - pd.Timedelta(days=365 + 45)) & (g.decl <= r.ts - pd.Timedelta(days=365 - 45))]
    if not len(prior): n_np += 1; continue
    near = ((g.decl - r.ts).abs() <= pd.Timedelta(days=3)).any()
    near |= any(abs(x - np.datetime64(r.ts)) <= np.timedelta64(3, "D") for x in unp_by.get(r.sym, []))
    near |= any(abs(x - np.datetime64(r.ts)) <= np.timedelta64(3, "D") for x in dn_by.get(r.sym, []))
    if near: continue
    if r.ts > OM_LAST: n_cov += 1; continue
    om.append(r)
om = pd.DataFrame(om)
out(f"  Omissions: results with a prior-year cash dividend for the period {len(ro)-n_np} of {len(ro)} results (no prior-year dividend found: {n_np}); omission = no cash row, unplaced cash row or dividend notice within +-3 days: {len(om)}; results after {OM_LAST.date()} not classified (payouts feed lag): {n_cov}")
if len(om): out("  Omissions: " + "; ".join(f"{r.sym} {r.ts.date()}" for r in om.itertuples()))

def h4_events(kind_df, T0col):
    d = kind_df.copy(); return d
def mk_ev(df, T0col, h, sym_col):
    e = pd.DataFrame(dict(sym=df[sym_col].values, s=df.s.values if "s" in df else df[sym_col].map(cidx).values, T0=df[T0col].values))
    if h == "T0": e["i"], e["j"] = e.T0 - 1, e.T0
    else: e["i"], e["j"] = e.T0, e.T0 + h
    return e
cutdf = cut_ev.rename(columns={"symbol": "sym"})[["sym", "s", "T0"]]
omdf = pd.DataFrame(dict(sym=om.sym, s=om.s, T0=om.P0)) if len(om) else pd.DataFrame(columns=["sym", "s", "T0"])
ctl = dec[dec.cls.isin(["increase", "flat"])].rename(columns={"symbol": "sym"})[["sym", "s", "T0"]]
sets = {"cuts": cutdf, "omissions": omdf, "pooled cut+omit": pd.concat([cutdf, omdf], ignore_index=True), "controls up/flat": ctl}
out(f"Event counts: " + ", ".join(f"{k} {len(v)} ({v.sym.nunique() if len(v) else 0} symbols)" for k, v in sets.items()))
HORIZ = [("T0 reaction", "T0", 1), ("drift +5", 5, 1), ("drift +20", 20, 1), ("drift +60", 60, 1)]
H4V = {}
for hname, h, _ in HORIZ:
    out(f"\n-- {hname}: " + ("last pre-news close to close of T0" if h == "T0" else f"excess from close of T0 to +{h} sessions") + " (descriptive, before cost; p = share of placebo medians <= observed)")
    header()
    for sname, sdf in sets.items():
        if len(sdf) == 0: out(f"{sname:<46s}  no events"); continue
        e2 = mk_ev(sdf, "T0", h, "sym")
        e2 = e2[e2.T0 + (h if h != "T0" else 0) <= LAST]
        eoff = 1 if h == "T0" else 0
        e2 = prep(f"H4 {sname} {hname}", e2, eoff=eoff)
        lo4 = int(dates.searchsorted(Y0))
        r = evaluate(f"H4 {sname} {hname}", e2, eoff=eoff, direction="le", lo=lo4, show=(sname in ("cuts", "omissions", "pooled cut+omit")))
        H4V[(sname, hname)] = (e2, r)
        if h in (20, 60) and sname in ("cuts", "omissions", "pooled cut+omit"):
            evaluate(f"H4 {sname} {hname}, net WHT", e2, net=True, eoff=eoff, direction="le", lo=lo4, show=False)
out("\nH4 exit/avoid reading: gain of selling at the close of T0 and not holding the window = -(excess) - 0.5% cost (round trip). p = share of placebo medians >= observed.")
header()
for sname in ("cuts", "omissions", "pooled cut+omit"):
    for hname in ("drift +5", "drift +20", "drift +60"):
        if (sname, hname) in H4V and len(H4V[(sname, hname)][0]):
            evaluate(f"H4 exit {sname} {hname}", H4V[(sname, hname)][0], sign=-1.0, cost=COST, direction="ge", lo=int(dates.searchsorted(Y0)), show=False)

# =============================================================================== CALENDAR
out("\n" + "=" * 100 + "\nSECTION 5. DIVIDEND CALENDAR 2026-10-17 to 2027-10-16\n" + "=" * 100)
kmi_cal = set(pd.read_csv(ROOT / "data/index_members/KMI_ALL_derived_2026-06-05.csv").symbol)
liq_now = set(P.liquid_universe("2026-10-17"))
uni = sorted(s for s in kmi_cal & liq_now if s in cidx)
out(f"KMI_ALL_derived_2026-06-05: {len(kmi_cal)} symbols; liquid_universe('2026-10-17'): {len(liq_now)}; intersection with prices: {len(uni)}")
CAL0, CAL1 = pd.Timestamp("2025-10-16"), pd.Timestamp("2026-10-16")
hist = cash_all[cash_all.ex_date <= CAL1]
lastc = {s: cff[LAST, cidx[s]] for s in uni}
ty_now = {}
for s in uni:
    g = hist[(hist.symbol == s) & (hist.ex_date > CAL0) & (hist.ex_date <= CAL1)]
    amt = sum(r.value / share_factor(s, r.ex_date, CAL1) for r in g.itertuples())
    ty_now[s] = amt / lastc[s]
rank = pd.Series(ty_now).sort_values(ascending=False)
top = list(rank.index[:30])
dbl = []
for s_ in top:   # the 365-day trailing window can hold the same seasonal payment twice (Oct 2025 and Oct 2026)
    g_ = hist[(hist.symbol == s_) & (hist.ex_date > CAL0) & (hist.ex_date <= CAL1)].ex_date.sort_values().tolist()
    if any(abs((y - x).days - 365) <= 20 for x in g_ for y in g_ if y > x): dbl.append(s_)
out(f"Top-30 names whose trailing window holds the same seasonal payment twice (two ex-dates 345-385 days apart), which inflates their trailing yield: {len(dbl)}: {', '.join(dbl)}")
names = an.drop_duplicates("symbol", keep="last").set_index("symbol").company
rows = []; skipped = []
for s in top:
    g = cash_all[cash_all.symbol == s].sort_values("ex_date")
    hist_s = g[g.ex_date <= CAL1]
    adj = lambda r: r.value / share_factor(s, r.ex_date, CAL1)
    allamt = [adj(r) for r in hist_s.itertuples()]
    def one_off(r):
        oth_ = [adj(x) for x in hist_s.itertuples() if x.Index != r.Index]
        if not oth_: return True
        return adj(r) > 2 * np.median(oth_)
    declared = g[g.ex_date > CAL1]
    basis = g[(g.ex_date > CAL0) & (g.ex_date <= CAL1)]
    used = set()
    for r in declared.itertuples():
        # basis row this declared payment repeats: nearest unused prior-year row within 45 days of ex-365d
        best, bd = None, 46
        for b_ in basis.itertuples():
            if b_.Index in used: continue
            dd_ = abs((b_.ex_date + pd.Timedelta(days=365) - r.ex_date).days)
            if dd_ < bd: best, bd = b_, dd_
        if best is not None: used.add(best.Index)
        rows.append(dict(symbol=s, company=names.get(s, ""), status="declared", expected_ex_month=r.ex_date.strftime("%Y-%m"),
                         expected_ex_date=r.ex_date.date(), gross_amount_rs=round(r.value, 4), net_amount_rs=round(WHT * r.value, 4),
                         basis_ex_date=(best.ex_date.date() if best is not None else r.ex_date.date()),
                         basis_amount_rs=round(adj(best), 4) if best is not None else round(r.value, 4),
                         basis_source=(best.ex_date_source if best is not None else r.ex_date_source),
                         trailing_yield_pct=round(100 * ty_now[s], 2), close_2026_10_16=lastc[s], payments_in_history=len(hist_s),
                         one_off_flag=bool(one_off(best if best is not None else r)), added_on="2026-10-17"))
    for b_ in basis.itertuples():
        if b_.Index in used: continue
        # already realized: an actual row within 45 days of basis+365d that went ex on or before 2026-10-16 (the pattern has repeated)
        # one-to-one: each realized row repeats only the basis row whose +365d date is nearest to it
        bl = list(hist_s.itertuples())
        done = [x for x in basis.itertuples() if x.Index != b_.Index and abs((x.ex_date - (b_.ex_date + pd.Timedelta(days=365))).days) <= 45
                and min(bl, key=lambda q: abs((x.ex_date - (q.ex_date + pd.Timedelta(days=365))).days)).Index == b_.Index]
        if done:
            skipped.append(f"{s} basis {b_.ex_date.date()} (repeated on {done[0].ex_date.date()})"); continue
        amt = adj(b_)
        rows.append(dict(symbol=s, company=names.get(s, ""), status="projected",
                         expected_ex_month=(b_.ex_date + pd.DateOffset(years=1)).strftime("%Y-%m"), expected_ex_date="",
                         gross_amount_rs=round(amt, 4), net_amount_rs=round(WHT * amt, 4), basis_ex_date=b_.ex_date.date(),
                         basis_amount_rs=round(amt, 4), basis_source=b_.ex_date_source, trailing_yield_pct=round(100 * ty_now[s], 2),
                         close_2026_10_16=lastc[s], payments_in_history=len(hist_s), one_off_flag=bool(one_off(b_)), added_on="2026-10-17"))
out(f"Projected rows NOT created because the same-period payment already went ex on or before 2026-10-16 ({len(skipped)}): " + "; ".join(skipped))
cal = pd.DataFrame(rows).sort_values(["symbol", "expected_ex_month"])
(ROOT / "catalysts").mkdir(exist_ok=True)
cal.to_csv(ROOT / "catalysts/dividend_calendar.csv", index=False)
out(f"Calendar rows {len(cal)}: declared {int((cal.status=='declared').sum())}, projected {int((cal.status=='projected').sum())}, one_off_flag true {int(cal.one_off_flag.sum())} (rows), on {cal[cal.one_off_flag].symbol.nunique()} symbols; names {cal.symbol.nunique()} of 30.")
out("Top 30 by trailing yield at 2026-10-16 (gross cash with ex in (2025-10-16, 2026-10-16], current share terms, over raw close):")
for k, s in enumerate(top, 1):
    c_ = cal[cal.symbol == s]
    out(f"  {k:>2d} {s:<8s} {100*ty_now[s]:6.2f}%  close {lastc[s]:>9.2f}  payments {int(c_.payments_in_history.iloc[0]) if len(c_) else 0}  rows {len(c_)} (declared {int((c_.status=='declared').sum())}, projected {int((c_.status=='projected').sum())}, one-off {int(c_.one_off_flag.sum())})")

(ROOT / "tests/out").mkdir(exist_ok=True)
(ROOT / "tests/out/dividend_runup_exdate.txt").write_text(buf.getvalue(), encoding="utf-8")
