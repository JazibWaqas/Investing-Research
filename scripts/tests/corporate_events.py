"""Corporate-event trades on PSX: buy-backs, bonus/splits, CEO/chair/control changes, unusual-movement letters, rating upgrades, rights issues, KMI additions.
Run: .venv/Scripts/python.exe -I scripts/tests/corporate_events.py   (writes tests/out/corporate_events.txt). Write-up: tests/corporate_events.md.
Point in time: an event is the announcement timestamp. Reaction day R = that session if stamped on a trading day by 15:30, else the next session. Signal is the close of R;
the fill is the close of the first later session that is not upper-locked (close within 0.5% of +10% over the prior close). Fixed exits at 20/60/120 sessions after the fill
(rolled forward if lower-locked), or a 20% close-to-close trailing stop (signal at the close, fill at the next non-lower-locked close, capped at 250 sessions).
Costs: 0.5% round trip, plus 0.5% slippage when the 60-session median traded value before R is under Rs20m. Returns use the total-return adjusted panel; delisted names use the crude return path.
Placebo P1: same symbol, random reaction day within +-250 sessions (outside +-30), same exits and costs, 200 draws. Placebo P2 (main): random (symbol, day) from the whole panel in the same calendar year, same KMI status, liquidity bucket and 20-session run-up bucket, same exits and costs, 200 draws.
"""
import sys, io, re, warnings, glob, os
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
def pc(x, d=1, sign=True):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else (f"{x*100:+.{d}f}%" if sign else f"{x*100:.{d}f}%")

SEED, K, STOP, CAP = 20261018, 200, 0.20, 250
HZ = (20, 60, 120)
EXITS = ["h20", "h60", "h120", "stop"]
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- 1. prices (listed: adjusted panel; delisted: crude path)
close_raw, vol_raw, tv = P.load_panel()
adj = pd.read_parquet(ROOT / "data" / "panel_close_adj.parquet")
cal = close_raw.index
dl_files = sorted(glob.glob(str(ROOT / "data" / "prices_delisted" / "*.csv")))
dl_syms = [os.path.basename(f)[:-4] for f in dl_files]
dc, dv = {}, {}
for f, s in zip(dl_files, dl_syms):
    try:
        x = pd.read_csv(f, usecols=["date", "close", "volume"], parse_dates=["date"], index_col="date")
    except Exception:
        continue
    x = x[~x.index.duplicated(keep="last")].sort_index().reindex(cal)
    dv[s] = x.volume
    dc[s] = x.close.where((x.volume > 0) & (x.close > 0))
dc, dv = pd.DataFrame(dc), pd.DataFrame(dv)
dv = dv.where(dc.notna(), 0.0)
d_ret = P.returns(dc, "crude", vol=dv)
d_adj = (1 + d_ret.fillna(0)).cumprod().where(dc.notna())
C = pd.concat([close_raw, dc], axis=1)                  # raw close, NaN where no trade
A = pd.concat([adj, d_adj], axis=1)
V = pd.concat([vol_raw, dv], axis=1)
TVd = (C * V).fillna(0).where(V.notna())
TVmed = TVd.rolling(60, min_periods=40).median().shift(1)
DELISTED = set(dc.columns)
NR = len(cal)
syms = list(C.columns)
col = {s: i for i, s in enumerate(syms)}
Cn, An, TVn = C.values, A.values, TVmed.values
obs = ~np.isnan(Cn)
prevc = pd.DataFrame(Cn).ffill().shift(1).values
with np.errstate(invalid="ignore", divide="ignore"):
    ulock = obs & (Cn >= prevc * 1.10 * 0.995)
    llock = obs & (Cn <= prevc * 0.90 * 1.005)
# forward-filled adjusted price inside each listing
Af = np.array(pd.DataFrame(An).ffill().values)
lastobs = np.array([np.flatnonzero(obs[:, j])[-1] if obs[:, j].any() else -1 for j in range(len(syms))])
firstobs = np.array([np.flatnonzero(obs[:, j])[0] if obs[:, j].any() else NR for j in range(len(syms))])
Af[np.arange(NR)[:, None] > lastobs[None, :]] = np.nan   # after the last observation: unknown
buy_rows = [np.flatnonzero(obs[:, j] & ~ulock[:, j]) for j in range(len(syms))]
sell_rows = [np.flatnonzero(obs[:, j] & ~llock[:, j]) for j in range(len(syms))]
obs_rows = [np.flatnonzero(obs[:, j]) for j in range(len(syms))]
is_dl = np.array([s in DELISTED for s in syms])

# regime: 6M T-bill above / below policy rate
tb = pd.read_csv(ROOT / "data" / "macro" / "tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"]).set_index("date").y6m
pr = pd.read_csv(ROOT / "data" / "macro" / "policy_rate_decisions.csv", parse_dates=["date"]).set_index("date").rate
tb_c = tb.reindex(cal, method="ffill") if False else tb.reindex(tb.index.union(cal)).ffill().reindex(cal)
pr_c = pr.reindex(pr.index.union(cal)).ffill().reindex(cal)
regime = np.where(tb_c.values > pr_c.values, "bill>policy", "bill<=policy")

# KMI All Share membership at date (latest snapshot on or before; before 2019-01-28 the first snapshot is used)
snaps = []
for f in sorted(glob.glob(str(ROOT / "data" / "index_members" / "KMI_ALL_derived_*.csv"))):
    d = pd.Timestamp(os.path.basename(f)[-14:-4])
    snaps.append((d, set(pd.read_csv(f).symbol)))
snaps.append((pd.Timestamp("2026-06-05"), set(pd.read_csv(ROOT / "data" / "index_members" / "KMI_ALL_2026-06-05.csv").symbol)))
snaps.sort(key=lambda x: x[0])
def is_kmi(sym, d):
    s = snaps[0][1]
    for dd, ss in snaps:
        if dd <= d:
            s = ss
    return sym in s

# ---------------------------------------------------------------- 2. events
ann = pd.read_parquet(ROOT / "data" / "announcements.parquet")
ann["ts"] = ann.datetime.dt.tz_localize(None)
ann["t"] = ann.title.fillna("").str.lower().str.replace(r"[‐-―]", "-", regex=True)
ann = ann[ann.symbol.isin(syms)].copy()
ann = ann[(ann.klass != "insider_trade") & ~ann.t.str.contains("revoked|withdraw", regex=True)]
T = ann.t
def has(p, s=T):
    return s.str.contains(p, regex=True, na=False)

def anchored(df, gap_days, key="symbol"):
    """keep the first event, drop later ones of the same symbol within gap_days of the kept one"""
    keep = []
    for s, g in df.sort_values("ts").groupby(key):
        last = None
        for i, t in zip(g.index, g.ts):
            if last is None or (t - last).days > gap_days:
                keep.append(i); last = t
    return df.loc[keep]

EV = []   # (type, symbol, ts, extra)
def add(typ, df, gap, extra=None):
    d = anchored(df, gap)
    for r in d.itertuples():
        EV.append((typ, r.symbol, r.ts, "" if extra is None else extra(r)))

# E1 buy-backs: programs of open-market buy-backs (sponsor delisting buy-backs, compulsory directions excluded)
bb = ann[has(r"buy[- ]?back|repurchase|purchase of (?:its )?own")]
bb = bb[~has(r"delist|sponsor|minorit|compulsory|undertaking|voluntary|tender notice|revoked|fund of funds|asset management", bb.t)].sort_values(["symbol", "ts"])
appr_re = r"public announcement|approval|decision|special resolution|resolutions? adopted|material information|eogm|intention|offer letter"
fol_re = r"newspaper|clipping|cutting|published|cancel|complet|clos|escrow|dispatch|corrigendum|extension|final report"
prog = []
for s, g in bb.groupby("symbol"):
    pid, last = 0, None
    for i, t in zip(g.index, g.ts):
        if last is not None and (t - last).days > 150:
            pid += 1
        last = t; prog.append((i, s, pid))
bb = bb.join(pd.DataFrame(prog, columns=["i", "symbol", "prog"]).set_index("i")[["prog"]])
approvals, starts = [], []
for (s, p), g in bb.groupby(["symbol", "prog"]):
    a_ = g[has(appr_re, g.t) & ~has(fol_re, g.t)]
    u_ = g[~has(appr_re, g.t) & ~has(r"cancel|complet|clos|escrow|newspaper|clipping|cutting|dispatch", g.t)]
    if len(a_): approvals.append(a_.index[0])
    if len(u_): starts.append(u_.index[0])
for typ, ids in (("E1a buyback approval", approvals), ("E1b buyback first purchase", starts)):
    for r in ann.loc[ids].itertuples():
        EV.append((typ, r.symbol, r.ts, ""))

# E2 bonus and split: ex-dates from corporate_actions.csv; declaration = explicit pre-ex title, else the last "financial results" announcement before the ex date
ca = pd.read_csv(ROOT / "data" / "corporate_actions.csv", parse_dates=["ex_date"])
ca = ca[ca.type.isin(["bonus", "split"]) & ca.symbol.isin(syms)]
expl = r"bonus|sub-?division|split"
post = r"credit|dispatch|despatch|fractional|certificate|disposal|warrant"
fr = ann[has(r"^financial results|results for the (year|half|quarter|nine)")]
for r in ca.itertuples():
    w = ann[(ann.symbol == r.symbol) & (ann.ts >= r.ex_date - pd.Timedelta(days=150)) & (ann.ts <= r.ex_date - pd.Timedelta(days=2))]
    e = w[has(expl, w.t) & ~has(post, w.t) & (w.klass != "financial_result")]
    how = "explicit"
    if len(e):
        ts = e.ts.min()
    else:
        f = fr[(fr.symbol == r.symbol) & (fr.ts >= r.ex_date - pd.Timedelta(days=120)) & (fr.ts <= r.ex_date - pd.Timedelta(days=2))]
        if not len(f): continue
        ts, how = f.ts.max(), "results-proxy"
    size = "" if r.type == "split" else ("big>=20%" if r.value >= 0.20 else "small<20%")
    EV.append(("E2a bonus" if r.type == "bonus" else "E2b split", r.symbol, ts, f"{how}|{size}"))

# E3 people and control
gen = r"chairman.{0,6}chief executive.{0,6}managing director|chairman / chief executive / managing director"
role_ceo = r"chief executive|\bceo\b|managing director"
newish = r"appointment|appoint|change of|election of|new "
notre = r"re-?appointment|reappointment|chief (financial|operating|investment|internal)|company secretary|head of"
x = ann[~has(gen)]
ceo = x[has(role_ceo + "|chairman|chairperson", x.t) & has(newish, x.t) & ~has(notre, x.t) & ~has(r"resign|cessation|ceases|retire", x.t) & ~has(r"director.s? interest|disclosure", x.t)]
add("E3a CEO or chairman appointed/changed", ceo, 90)
res = x[has(role_ceo + "|chairman|chairperson", x.t) & has(r"resign|cessation|ceases|retire", x.t) & ~has(r"company secretary|chief (financial|operating)|director\(s\)|directors?$|independent", x.t)]
add("E3b CEO or chairman resigns", res, 90)
g_ = ann[has(gen) & has(r"appointment|change")]
add("E3c role-change form (any of 5 roles)", g_, 90)
ctl = ann[has(r"takeover|substantial acquisition of voting|^change (of|in) management$|^change of management|acquisition of substantial|acquired by the shareholder|shares acquired under section") &
          ~has(r"intention|book closure|change in management fee|corrigendum|extension|fulfil")]
add("E3d control: takeover disclosure / change of management", ctl, 90)

# E4 PSX unusual-movement letter and company reply
un = ann[has(r"unusual|unusal|volatile trading|unusual trading")]
rep_re = r"reply|response|respond|clarif"
add("E4a PSX unusual-movement letter", un[~has(rep_re, un.t) & ~has(r"revoked", un.t)], 20)
rp = ann[has(rep_re) & has(r"unusual|movement|volatile|trading pattern|psx letter|market activity|volume")]
add("E4b company reply to PSX letter", rp[~has(r"agm|annual general|shariah|book closure|annual report|rumou?r", rp.t) | has(r"unusual|movement", rp.t)], 20)

# E5 credit-rating upgrades
up = ann[has(r"upgrad") & has(r"rating|pacra|\bvis\b|ifs|entity")]
add("E5 credit-rating upgrade", up, 30)

# E6 rights issues: declarations (titles) plus payout-portal rights (announce_dt)
rt = ann[has(r"right (issue|shares?)|rights issue|right preference") & has(r"declaration|declar|board resolution|notice of (right|book closure)|extract of resolution|draft offer|material information|intimation|decision|proposed|approv") &
         ~has(r"progress|subscription|noc|allotment|credit|dispatch|despatch|status|unpaid|unsubscribed|auditor|utili|letters? of right|clarification|no objection|resolution for allot")]
add("E6 rights issue declared", rt, 180)
un2 = pd.read_csv(ROOT / "data" / "corporate_actions_unplaced.csv", parse_dates=["announce_dt"])
rp2 = pd.concat([un2[un2.type == "right"][["symbol", "announce_dt"]], ca.iloc[0:0][["symbol"]].assign(announce_dt=pd.NaT)])
c2 = pd.read_csv(ROOT / "data" / "corporate_actions.csv", parse_dates=["announce_dt"])
rp2 = pd.concat([rp2, c2[c2.type == "right"][["symbol", "announce_dt"]]]).dropna()
rp2 = rp2[rp2.symbol.isin(syms)].rename(columns={"announce_dt": "ts"})
rp2["t"] = ""
rall = pd.concat([rt[["symbol", "ts"]], rp2[["symbol", "ts"]]])
rall = rall.reset_index(drop=True)
EV = [e for e in EV if not e[0].startswith("E6")]
d = anchored(rall, 180)
for r in d.itertuples():
    EV.append(("E6 rights issue declared", r.symbol, r.ts, ""))

# E7 KMI All Share additions (index_changes.csv); notice date has no clock time, so primary = known after the close of the notice date
ic = pd.read_csv(ROOT / "data" / "index_changes.csv")
ic = ic[(ic["index"] == "KMI_ALL") & (ic.action == "add") & ic.symbol.isin(syms)].copy()
ic["announce_date"] = pd.to_datetime(ic["announce_date"])
for r in ic.itertuples():
    EV.append(("E7 KMI All Share addition", r.symbol, r.announce_date + pd.Timedelta(hours=18), ""))

ev = pd.DataFrame(EV, columns=["type", "symbol", "ts", "extra"])
ev["date"] = ev.ts.dt.normalize()
ev["late"] = (ev.ts.dt.hour * 60 + ev.ts.dt.minute) > 15 * 60 + 30
pos = cal.searchsorted(ev.date.values)
inidx = (pos < NR) & (cal[np.minimum(pos, NR - 1)] == ev.date.values)
ev["R"] = np.where(inidx & ~ev.late, pos, np.where(inidx & ev.late, pos + 1, pos))
ev = ev[(ev.date >= cal[0] + pd.Timedelta(days=40)) & (ev.R < NR)].reset_index(drop=True)
ev["j"] = ev.symbol.map(col)
ev["year"] = ev.date.dt.year
ev["kmi"] = [is_kmi(s, d) or t.startswith("E7") for s, d, t in zip(ev.symbol, ev.date, ev.type)]   # E7 names are KMI-bound by construction
ev["tvm"] = [TVn[min(r, NR - 1), j] for r, j in zip(ev.R, ev.j)]
ev["tvb"] = np.where(ev.tvm >= 20e6, "TV>=20m", np.where(ev.tvm >= 5e6, "TV 5-20m", "TV<5m"))
ev["reg"] = [regime[min(r, NR - 1)] for r in ev.R]

# ---------------------------------------------------------------- 3. trade engine
def entry(j, R):
    br = buy_rows[j]; k = br.searchsorted(R, "right")
    if k >= len(br) or br[k] - R > 10: return None
    return br[k]

def first_sell(j, x, side="left"):
    sr = sell_rows[j]; k = sr.searchsorted(x, side)
    if k < len(sr): return sr[k]
    return lastobs[j] if (is_dl[j] and lastobs[j] >= 0) else None

def trade(j, R, tvm):
    """-> dict exit -> (net return, entry row, exit row) or None entries; entry row"""
    e = entry(j, R)
    if e is None: return None, {}
    cost = 0.005 + (0.005 if not (tvm >= 20e6) else 0.0)
    p0 = Af[e, j]
    res = {}
    for h, nm in zip(HZ, EXITS[:3]):
        if e + h >= NR and not is_dl[j]: res[nm] = None; continue
        x = first_sell(j, e + h)
        res[nm] = None if x is None or x <= e else (Af[x, j] / p0 - 1 - cost, e, x)
    end = min(e + CAP + 1, NR)
    seg = Af[e:end, j]
    cm = np.fmax.accumulate(seg)
    hit = np.flatnonzero(seg <= (1 - STOP) * cm)
    if len(hit):
        x = first_sell(j, e + hit[0], "right")
    elif e + CAP >= NR and not is_dl[j]:
        x = None
    else:
        x = first_sell(j, e + CAP)
    res["stop"] = None if x is None or x <= e else (Af[x, j] / p0 - 1 - cost, e, x)
    return e, res

rows = []
for r in ev.itertuples():
    e, res = trade(r.j, r.R, r.tvm)
    rows.append((e, res))
ev["e"] = [x[0] if x[0] is not None else -1 for x in rows]
for nm in EXITS:
    ev[nm] = [x[1].get(nm)[0] if x[1].get(nm) else np.nan for x in rows]
    ev[nm + "_x"] = [x[1].get(nm)[2] if x[1].get(nm) else -1 for x in rows]
ev["entered"] = ev.e >= 0
# leakage: 20-session run-up before R and the reaction day
def runup(j, R):
    if R < 22: return np.nan
    a, b = Af[R - 21, j], Af[R - 1, j]
    return b / a - 1 if a > 0 and b > 0 else np.nan
def react(j, R):
    a, b = Af[R - 1, j], Af[R, j]
    return b / a - 1 if a > 0 and b > 0 else np.nan
ev["runup"] = [runup(j, R) for j, R in zip(ev.j, ev.R)]
ev["react"] = [react(j, R) for j, R in zip(ev.j, ev.R)]
ev["rb"] = np.where(ev.runup >= 0.20, "runup>=+20%", np.where(ev.runup >= 0, "runup 0..20%", "runup<0"))
ev["pre10"] = [Af[R - 1, j] / Af[R - 11, j] - 1 if R > 12 and Af[R - 11, j] > 0 else np.nan for j, R in zip(ev.j, ev.R)]

# placebo P1: same symbol, K random reaction days within +-250 sessions (outside +-30)  -- controls the stock, but the window contains the event's own run
# placebo P2: matched market: random liquid-market (symbol, day) in the same calendar year, same KMI status, same liquidity bucket and same 20-session run-up bucket as the event
#             (no information about what the event symbol did afterwards, so no hindsight)
nS = len(syms)
RU = np.full((NR, nS), np.nan)
RU[21:] = Af[20:-1] / Af[:-21] - 1
RB = np.where(np.isnan(RU), -1, np.where(RU >= 0.20, 2, np.where(RU >= 0, 1, 0)))
TB = np.where(np.isnan(TVn), 0, np.where(TVn >= 20e6, 3, np.where(TVn >= 5e6, 2, 1)))
snap_dates = [d for d, _ in snaps]
KM = np.array([[sy in ss for sy in syms] for _, ss in snaps])
SI = np.maximum(np.searchsorted(np.array(snap_dates, dtype="datetime64[ns]"), cal.values, side="right") - 1, 0)
yr_rows = {y: np.flatnonzero((cal.year == y) & (np.arange(NR) > 25) & (np.arange(NR) < NR - 3)) for y in range(cal.year.min(), cal.year.max() + 1)}
class PLB:
    def __init__(s_):
        s_.ret = {nm: np.full((len(ev), K), np.nan, dtype=np.float32) for nm in EXITS}
        s_.e = np.full((len(ev), K), -1, dtype=np.int32); s_.j = np.zeros((len(ev), K), dtype=np.int32); s_.tvm = np.full((len(ev), K), np.nan)
        s_.x = {nm: np.full((len(ev), K), -1, dtype=np.int32) for nm in EXITS}
    def put(s_, i, k, j, tvm_, e, res):
        s_.j[i, k] = j; s_.tvm[i, k] = tvm_
        if e is None: return
        s_.e[i, k] = e
        for nm in EXITS:
            if res.get(nm): s_.ret[nm][i, k] = res[nm][0]; s_.x[nm][i, k] = res[nm][2]
P1, P2 = PLB(), PLB()
PL_run = np.full((len(ev), K), np.nan, dtype=np.float32)
tvb_code = {"TV<5m": 1, "TV 5-20m": 2, "TV>=20m": 3}
for i, r in enumerate(ev.itertuples()):
    orr = obs_rows[r.j]
    lo, hi = np.searchsorted(orr, r.R - 250), np.searchsorted(orr, r.R + 250, "right")
    cand = orr[lo:hi]; cand = cand[(np.abs(cand - r.R) > 30) & (cand > 22) & (cand < NR - 2)]
    if len(cand) >= 5:
        for k, R2 in enumerate(rng.choice(cand, K)):
            e, res = trade(r.j, R2, r.tvm)
            PL_run[i, k] = runup(r.j, R2)
            P1.put(i, k, r.j, r.tvm, e, res)
    rows_ = yr_rows.get(r.year)
    if rows_ is None or len(rows_) == 0 or np.isnan(r.runup): continue
    rb = 2 if r.runup >= 0.2 else (1 if r.runup >= 0 else 0)
    kk = 0
    for _ in range(6):
        rr = rng.choice(rows_, 3000); jj = rng.integers(0, nS, 3000)
        ok = obs[rr, jj] & (TB[rr, jj] == tvb_code[r.tvb]) & (KM[SI[rr], jj] == r.kmi) & (RB[rr, jj] == rb) & (np.abs(jj - r.j) > 0)
        for R2, j2 in zip(rr[ok], jj[ok]):
            e, res = trade(j2, R2, TVn[R2, j2])
            P2.put(i, kk, j2, TVn[R2, j2], e, res); kk += 1
            if kk >= K: break
        if kk >= K: break

# ---------------------------------------------------------------- 4. statistics
def stats(x):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    if len(x) == 0: return None
    return dict(n=len(x), mean=x.mean(), med=np.median(x), win=(x > 0).mean(), p50=(x > 0.5).mean(), m30=(x < -0.3).mean(), worst=x.min(), best=x.max())
def fmt(s, extra=""):
    if s is None: return "n=0"
    return f"n {s['n']:>4} | mean {pc(s['mean'])} med {pc(s['med'])} win {pc(s['win'],0,False)} >+50% {pc(s['p50'],0,False)} <-30% {pc(s['m30'],0,False)} worst {pc(s['worst'],0)} best {pc(s['best'],0)}{extra}"
def indep(d):
    return f"syms {d.symbol.nunique()}, months {d.date.dt.to_period('M').nunique()}"
def _plac(P, d, nm):
    idx = d.index.values
    sub = P.ret[nm][idx]
    act = d[nm].values
    keep = (~np.isnan(sub).all(axis=1)) & ~np.isnan(act)
    if keep.sum() < 3: return None
    s2 = sub[keep]
    mm = np.nanmean(s2, axis=0); md = np.nanmedian(s2, axis=0)
    a_mean, a_med = np.nanmean(act[keep]), np.nanmedian(act[keep])
    return np.mean(mm), np.median(md), (np.sum(mm >= a_mean) + 1) / (K + 1), (np.sum(md >= a_med) + 1) / (K + 1), int(keep.sum())
def plac(d, nm):
    t = ""
    for lab, P in (("P1 same-symbol", P1), ("P2 matched-market", P2)):
        r_ = _plac(P, d, nm)
        if r_: t += f" || {lab}: mean {pc(r_[0])} med {pc(r_[1])} p(mean) {r_[2]:.3f} p(med) {r_[3]:.3f} (n {r_[4]})"
    return t

SLEEVE_HOLD = 3
def sleeve_core(d):
    """d columns: e (fill row), x (exit row), j, tvm. Rs50k sleeve, every signal, at most 3 positions, each sized at equity/3 or the remaining cash.
    -> final multiple, max drawdown, trades taken, first row, last row"""
    d = d.sort_values("e")
    if not len(d): return None
    cash, pos_, eq_series, taken = 50000.0, [], [], 0
    byrow = {}
    for e_, x_, j_, tv_ in zip(d.e.values, d.x.values, d.j.values, d.tvm.values):
        byrow.setdefault(int(e_), []).append((int(x_), int(j_), tv_))
    t0, t1 = int(d.e.min()), int(d.x.max())
    for t in range(t0, t1 + 1):
        for p in [p for p in pos_ if p["x"] == t]:
            cash += p["sh"] * Af[t, p["j"]] * (1 - p["cost"] / 2); pos_.remove(p)
        eq = cash + sum(p["sh"] * Af[t, p["j"]] for p in pos_)
        for x_, j_, tv_ in byrow.get(t, []):
            if len(pos_) >= SLEEVE_HOLD or cash < 100: continue
            size = min(cash, eq / SLEEVE_HOLD)
            cost = 0.005 + (0.005 if not (tv_ >= 20e6) else 0.0)
            cash -= size; pos_.append(dict(sh=size * (1 - cost / 2) / Af[t, j_], j=j_, x=x_, cost=cost)); taken += 1
        eq_series.append(cash + sum(p["sh"] * Af[t, p["j"]] for p in pos_))
    eqs = np.array(eq_series)
    return eqs[-1] / 50000.0, (eqs / np.maximum.accumulate(eqs) - 1).min(), taken, cal[t0].date(), cal[t1].date()

def sleeve(d, nm):
    d = d[d[nm].notna()]
    return sleeve_core(pd.DataFrame(dict(e=d.e, x=d[nm + "_x"], j=d.j, tvm=d.tvm)))

NSL = 40
def sleeve_placebo(d, nm):
    """sleeve final multiples when every event is replaced by a matched-market random entry (NSL replicates, P2)"""
    idx = d.index.values; res = []
    for k in range(NSL):
        e_ = P2.e[idx, k]; x_ = P2.x[nm][idx, k]; ok = (e_ >= 0) & (x_ > e_)
        if ok.sum() < 3: continue
        r = sleeve_core(pd.DataFrame(dict(e=e_[ok], x=x_[ok], j=P2.j[idx, k][ok], tvm=P2.tvm[idx, k][ok])))
        if r: res.append(r[0])
    return np.array(res)

# ---------------------------------------------------------------- 5. report
types = sorted(ev.type.unique())
out("CORPORATE EVENTS TEST  (run date 2026-10-18; price data to", cal[-1].date(), ")")
out(f"Sessions {NR}; symbols with prices {len(syms)} (delisted {len(DELISTED)}); placebo draws per event {K}; seed {SEED}")
out("Costs: 0.5% round trip, +0.5% slippage when 60-day median traded value < Rs20m. Trailing stop 20% on closes, cap 250 sessions.")
out()
out("EVENT COUNTS (raw announcement matches reduced by anchored de-duplication; events with a price history from Oct 2016):")
ev["dl"] = ev.symbol.isin(DELISTED); ev["delayed"] = (ev.e >= 0) & (ev.e - ev.R > 1)
cnt = ev.groupby("type").agg(events=("symbol", "size"), symbols=("symbol", "nunique"), kmi=("kmi", "sum"), entered=("entered", "sum"), delisted_names=("dl", "sum"), entry_delayed_by_lock=("delayed", "sum"), first=("date", "min"), last=("date", "max"))
out(cnt.to_string())
out()

def cells(d):
    return {"All": d, "KMI member": d[d.kmi], "KMI & TV>=5m": d[d.kmi & (d.tvm >= 5e6)], "KMI & TV>=20m": d[d.kmi & (d.tvm >= 20e6)]}

for typ in types:
    d0 = ev[ev.type == typ]
    out("=" * 120); out(typ, f"| events {len(d0)}, entered {int(d0.entered.sum())}, KMI {int(d0.kmi.sum())}, {indep(d0)}")
    if len(d0) < 15: out("  *** n is small: read as anecdote, not odds ***")
    out("-- A. exits x sample (net of costs; P1 = same symbol random day, P2 = matched random market day)")
    for cname, d in cells(d0).items():
        for nm in EXITS:
            s = stats(d[nm])
            out(f"  {cname:<14} {nm:<5} {fmt(s)}{plac(d, nm) if cname != 'KMI & TV>=20m' else ''}")
    out("-- B. liquidity x KMI (exits h60 and stop)")
    for nm in ("h60", "stop"):
        for b in ("TV>=20m", "TV 5-20m", "TV<5m"):
            for k_, kn in ((True, "KMI"), (False, "non-KMI")):
                d = d0[(d0.tvb == b) & (d0.kmi == k_)]
                if len(d[nm].dropna()): out(f"  {nm:<5} {b:<9} {kn:<8} {fmt(stats(d[nm]))}")
    out("-- C. by signal year (exit h60, All) and by regime (h60 and stop, All)")
    for y, d in d0.groupby("year"):
        s = stats(d.h60)
        if s: out(f"  {y}: n {s['n']:>3} mean {pc(s['mean'])} med {pc(s['med'])} win {pc(s['win'],0,False)}")
    for nm in ("h60", "stop"):
        for g_, d in d0.groupby("reg"):
            out(f"  {nm:<5} {g_:<13} {fmt(stats(d[nm]))}")
    out("-- C2. signals from 2024-11-01 only (cash dividends complete in the adjusted prices), All events")
    dd_ = d0[d0.date >= "2024-11-01"]
    for nm in ("h60", "stop"):
        out(f"  {nm:<5} {fmt(stats(dd_[nm]))}{plac(dd_, nm)}")
    out("-- D. leakage: 20-session run-up before R and reaction-day return (All events)")
    ru, rc = d0.runup.dropna(), d0.react.dropna()
    pr_ = np.nanmedian(PL_run[d0.index.values], axis=0)
    out(f"  run-up: n {len(ru)} mean {pc(ru.mean())} median {pc(ru.median())} share>+20% {pc((ru>0.2).mean(),0,False)} | P1 same-symbol random-day run-up median {pc(np.nanmedian(pr_))}")
    out(f"  reaction day R: n {len(rc)} mean {pc(rc.mean())} median {pc(rc.median())} share>+5% {pc((rc>0.05).mean(),0,False)}")
    out("-- E. by run-up bucket (exit h60 and stop, All)")
    for b, d in d0.groupby("rb"):
        out(f"  {b:<13} h60 {fmt(stats(d.h60))}")
        out(f"  {'':<13} stop {fmt(stats(d.stop))}")
    if d0.extra.str.len().sum():
        out("-- F. sub-labels (extra) (exit h60 and stop, All)")
        for b, d in d0.groupby("extra"):
            out(f"  {b:<28} h60 {fmt(stats(d.h60))}"); out(f"  {'':<28} stop {fmt(stats(d.stop))}")
    if typ.startswith("E4a"):
        out("-- F. prior-10-session move before R (exit h60 and stop, All)")
        for lab, m in (("pre10>=+15%", d0.pre10 >= 0.15), ("pre10 in -15..+15%", (d0.pre10 > -0.15) & (d0.pre10 < 0.15)), ("pre10<=-15%", d0.pre10 <= -0.15)):
            out(f"  {lab:<20} h60 {fmt(stats(d0[m].h60))}{plac(d0[m], 'h60')}"); out(f"  {'':<20} stop {fmt(stats(d0[m].stop))}{plac(d0[m], 'stop')}")
            out(f"  {'':<20} by year n: " + ", ".join(f"{y}:{n}" for y, n in d0[m].groupby('year').size().items()))
    out("-- G. Rs50k sleeve, every signal, max 3 positions (final multiple, max drawdown, trades taken)")
    for cname, d in list(cells(d0).items())[:3]:
        for nm in EXITS:
            r_ = sleeve(d, nm)
            if r_ is None: out(f"  {cname:<14} {nm:<5} none"); continue
            pl_ = sleeve_placebo(d, nm)
            pls = f" | placebo sleeve x p10 {np.percentile(pl_,10):.2f} med {np.median(pl_):.2f} p90 {np.percentile(pl_,90):.2f}, share >= actual {np.mean(pl_ >= r_[0]):.2f}" if len(pl_) else ""
            out(f"  {cname:<14} {nm:<5} x{r_[0]:.2f}  maxDD {pc(r_[1],0)}  taken {r_[2]}  ({r_[3]} to {r_[4]}){pls}")
    out()

# today's screen: events with reaction day in the last 15 sessions, KMI members
out("=" * 120)
out("TODAY'S SCREEN: events with a reaction day in the last 15 sessions (last 60 for splits and rights); price data to", cal[-1].date())
for typ in types:
    cut = NR - (60 if typ.startswith(("E2b", "E6")) else 15)
    d = ev[(ev.type == typ) & (ev.R >= cut)]
    if not len(d): continue
    out(f"-- {typ}: {len(d)} events, {int(d.kmi.sum())} KMI")
    for r in d.sort_values("date").itertuples():
        out(f"   {r.date.date()} {r.symbol:<8} KMI {'Y' if r.kmi else 'n'} {r.tvb:<9} runup20 {pc(r.runup,0)} react {pc(r.react,1)} {r.extra}")
# also events too recent for the data (announced after the last price date) are not present by construction
os.makedirs(ROOT / "tests" / "out", exist_ok=True)
(ROOT / "tests" / "out" / "corporate_events.txt").write_text(buf.getvalue(), encoding="utf-8")

