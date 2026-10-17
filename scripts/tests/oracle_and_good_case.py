"""Oracle upper bound and a fixed menu of simple mechanical systems, five 2-year windows, Rs50,000 each.
Run: .venv/Scripts/python.exe -I scripts/tests/oracle_and_good_case.py [pr]    -> tests/out/oracle_and_good_case.txt (and _pr.txt with the arg 'pr')
Trades: tests/out/oracle_trades.csv.  Write-up: tests/oracle_and_good_case.md.

MENU, fixed before any result was looked at (the user asked for these eight, nothing else was added or tuned):
  S1 monthly rotation into the top-3 liquid names by trailing 63-session return
  S2 monthly rotation into the top-3 by return from t-126 to t-21 (6 months, skip the last month)
  S3 52-week-high breakout (close above the prior 252-session high) with a 20% trailing stop on closes, max 3 positions of 1/3 equity
  S4 each month: rank sectors (sector_map baskets, scripts/sector_momentum.py) by 126-session EW return of liquid names, take the top 3 sectors,
     buy the lowest trailing P/E name in each (raw close / sum of the last 4 announced quarterly EPS, EPS adjusted for bonus/splits since the quarter)
  S5 buy a liquid name 20%+ below its 60-session high while its 126-session return is still positive; sell after 60 sessions or at +25%; max 5 positions of 20%
  S6 buy the close after the reaction session of a quarterly result with EPS >= 1.5x the same quarter a year earlier (base > 0) and a reaction-session
     return under 5%; sell after 90 sessions; max 5 positions of 20%.  Needs quarterly_eps.csv announce_dt (first_tradable_date)
  S7 KMI All Share (total return) buy and hold, 0.25% each way
  S8 equal weight of the 10 most liquid names (trailing 60-session median traded value), rebalanced monthly to equal weight
Execution: signal at the close of day t, trade at the close of day t+1 (a name that does not trade that day is skipped; sells wait for the next trade).
Costs: 0.25% per side, plus 0.25% per side slippage when the name's trailing 60-session median traded value is under Rs20m (round trip 0.5% or 1.0%).
Universe: names with trailing 60-session median traded value > Rs5m (rolling, point in time). KMI All Share members only when the window starts on or after
2019-01-28 (first derived membership list); the first two windows use all liquid names.  Survivors only (see delisted check in section A).
Prices: data/panel_close_adj.parquet (bonus/split adjusted, partial dividends); with the argument 'pr' data/panel_close_adj_pricereturn.parquet.
"""
import sys, io, re, ast, glob, collections, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

PR = len(sys.argv) > 1 and sys.argv[1] == "pr"
buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")

raw, vol, tv = P.load_panel()
dates, N, cols = raw.index, len(raw), list(raw.columns)
cidx = {s: i for i, s in enumerate(cols)}
adj = pd.read_parquet(ROOT / "data" / ("panel_close_adj_pricereturn.parquet" if PR else "panel_close_adj.parquet")).reindex(index=dates, columns=cols)
adj_pr = pd.read_parquet(ROOT / "data/panel_close_adj_pricereturn.parquet").reindex(index=dates, columns=cols)

def clean(df):
    """Unadjusted splits/consolidations the corporate-action table missed: a one-session drop of 25%+ (price over Rs10, where the circuit is 10%) or 50%+
    (price over Rs2) after at most 5 sessions of gap is a corporate action, not a trade. Scale the earlier history so the series is continuous."""
    prev = df.ffill().shift(1)
    pos = pd.DataFrame(np.arange(len(df))[:, None] + 0.0 * df.values, df.index, df.columns).where(df.notna())
    gap = pos - pos.ffill().shift(1)
    r = df / prev - 1
    m = ((r <= -0.25) & (prev > 10) | (r <= -0.5) & (prev > 2)) & (gap <= 5) & df.notna()
    ev = []
    df = df.copy()
    for d, c in sorted(zip(*np.where(m.values)), reverse=True):
        f = df.iat[d, c] / prev.iat[d, c]
        df.iloc[:d, c] = df.iloc[:d, c] * f
        ev.append((df.index[d].date(), df.columns[c], r.iat[d, c]))
    return df, sorted(ev)
adj, CLEAN_EV = clean(adj)
adj_pr, _ = clean(adj_pr)
TRADED = adj.notna().values
PX = adj.ffill().values
RAWF = raw.ffill().values
GF = adj_pr.ffill().values / RAWF                       # bonus/split cumulative factor (adj = raw * G)
MTV = tv.rolling(60, min_periods=40).median().shift(1).values   # trailing 60 sessions ending the day before, as prices._med_tv
LIQ = MTV > 5e6
LAST = N - 1
T_MEM_KNOWN = pd.Timestamp("2019-01-28")

# ---------------- membership (copied from scripts/walkforward.py)
RENAME = {"ENGRO": "ENGROH", "BYCO": "CNERGY", "ICI": "LCI"}
def norm(s):
    s = RENAME.get(s, s)
    if s not in cidx:
        s = re.sub(r"(XD|XB|XR)$", "", s); s = RENAME.get(s, s)
    return s
LISTS = {}
for f in sorted(glob.glob(str(ROOT / "data/index_members/KMI_ALL_derived_*.csv"))):
    LISTS[pd.Timestamp(re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1))] = {norm(s) for s in pd.read_csv(f).symbol}
LISTS[pd.Timestamp("2026-06-05")] = {norm(s) for s in pd.read_csv(ROOT / "data/index_members/KMI_ALL_2026-06-05.csv").symbol}
_ic = pd.read_csv(ROOT / "data/index_changes.csv"); _ic["effective_date"] = pd.to_datetime(_ic.effective_date, errors="coerce")
CH = _ic[(_ic["index"] == "KMI_ALL") & ~_ic.source_url.astype(str).str.contains("derived")].copy()
CH["symbol"] = CH.symbol.map(norm)
LDATES = sorted(LISTS)
def members_at(t):
    ds = [d for d in LDATES if d <= t]
    d0 = ds[-1] if ds else LDATES[0]
    m = set(LISTS[d0])
    for r in CH[(CH.effective_date > d0) & (CH.effective_date <= t)].sort_values("effective_date").itertuples():
        (m.add if r.action == "add" else m.discard)(r.symbol)
    return m
_memc = {}
def memmask(i):
    """bool array of KMI members, evaluated on the first session of the month of day i (stale within a month, never ahead)."""
    d = dates[i]; k = (d.year, d.month)
    if k not in _memc:
        first = dates[dates.searchsorted(pd.Timestamp(d.year, d.month, 1))]
        m = members_at(first); a = np.zeros(len(cols), bool)
        for s in m:
            if s in cidx: a[cidx[s]] = True
        _memc[k] = a
    return _memc[k]
def universe(i, kmi):
    u = LIQ[i].copy()
    return u & memmask(i) if kmi else u

# ---------------- sectors (copied from scripts/walkforward.py)
scr = pd.read_csv(ROOT / "seed/data/fundamentals/screener_20261016.csv")
CODE = {}
for r in scr.itertuples():
    sym = r.symbol if r.symbol in cidx else re.sub(r"(XD|XB|XR)$", "", r.symbol)
    if pd.notna(r.sector) and (sym not in CODE or r.symbol == sym):
        CODE[sym] = str(int(r.sector))
_tree = ast.parse((ROOT / "scripts/sector_momentum.py").read_text(encoding="utf-8"))
S_DICT = [ast.literal_eval(n.value) for n in _tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "S"][0]
votes = collections.defaultdict(collections.Counter)
for lab, names in S_DICT.items():
    for nm in names.split():
        if nm in CODE: votes[CODE[nm]][lab] += 1
BANK_CODE, MOD_CODES = CODE["MEBL"], {CODE["FHAM"], CODE["PAKQATAR"]}
SHORT = {"Oil refineries": "Refineries", "Steel & engineering": "Steel & eng", "Glass, packaging, paper": "Glass/pack/paper", "Gas utilities & misc": "Gas utils & misc"}
LABEL = {}
for code in sorted(set(CODE.values())):
    lab = "Islamic banks" if code == BANK_CODE else "Modarabas & takaful" if code in MOD_CODES else votes[code].most_common(1)[0][0] if votes[code] else f"code{code}"
    LABEL[code] = SHORT.get(lab, lab)
SEC = {s: LABEL[c] for s, c in CODE.items()}
SECI = np.array([SEC.get(c, "") for c in cols], dtype=object)

# ---------------- signals
def lag(a, k):
    o = np.full_like(a, np.nan); o[k:] = a[:-k]; return o
RET63 = PX / lag(PX, 63) - 1
RET126 = PX / lag(PX, 126) - 1
MOM6_1 = lag(PX, 21) / lag(PX, 126) - 1
dfp = pd.DataFrame(PX)
HI252 = lag(dfp.rolling(252, min_periods=200).max().values, 1)     # prior 252 sessions, excludes today
HI60 = dfp.rolling(60, min_periods=40).max().values                # includes today

# ---------------- quarterly EPS, point in time
E = pd.read_csv(ROOT / "data/fundamentals/quarterly_eps.csv")
E["qe"] = pd.to_datetime(E.fiscal_quarter_end)
E["ftd"] = pd.to_datetime(E.first_tradable_date, errors="coerce")
E["eps"] = E.eps_basic
E["fallback"] = E.ftd.isna()
E["usable"] = E.ftd.fillna(E.qe + pd.Timedelta(days=120))          # no announcement time: assume 120 days (late, so never early)
E = E[E.symbol.isin(cidx)].sort_values(["symbol", "qe"])
EPSBY = {s: g.reset_index(drop=True) for s, g in E.groupby("symbol")}

def ttm_pe(c, i):
    """trailing P/E at close of day i for column c, or NaN."""
    g = EPSBY.get(cols[c])
    if g is None: return np.nan
    g = g[(g.usable <= dates[i]) & g.eps.notna()].tail(4)
    if len(g) < 4 or not (250 <= (g.qe.iloc[-1] - g.qe.iloc[0]).days <= 295): return np.nan
    tot = 0.0
    for r in g.itertuples():
        q = max(int(dates.searchsorted(r.qe, side="right")) - 1, 0)
        tot += r.eps * GF[q, c] / GF[i, c]
    p = RAWF[i, c]
    return p / tot if tot > 0 and np.isfinite(p) and p > 0 else np.nan

# S6 events: day index of the reaction session -> list of (col, eps_ratio)
EVENTS = collections.defaultdict(list)
for s, g in EPSBY.items():
    c = cidx[s]; byq = {r.qe: r.eps for r in g.itertuples()}
    for r in g.itertuples():
        if r.fallback or pd.isna(r.eps): continue
        prev = [q for q in byq if abs((r.qe - q).days - 365) <= 15]
        if not prev or not (byq[prev[0]] > 0) or r.eps < 1.5 * byq[prev[0]]: continue
        d = int(dates.searchsorted(r.ftd))                          # reaction session
        if d < 1 or d >= N: continue
        EVENTS[d].append((c, r.eps / byq[prev[0]]))

# ---------------- simulator
def side(c, i):
    m = MTV[i, c]
    return 0.0025 + (0.0025 if not (m >= 20e6) else 0.0)

class Sim:
    def __init__(self, i0, name, win, cash=50000.0):
        self.i0, self.cash, self.pos, self.trades, self.name, self.win = i0, cash, {}, [], name, win
        self.eq = []
    def value(self, i): return self.cash + sum(p["sh"] * PX[i, c] for c, p in self.pos.items())
    def buy(self, c, amt, i, reason=""):
        amt = min(amt, self.cash)
        if amt < 1000 or not TRADED[i, c]: return False
        sh = amt * (1 - side(c, i)) / PX[i, c]
        self.cash -= amt
        if c in self.pos:
            p = self.pos[c]; p["sh"] += sh; p["inv"] += amt
        else:
            self.pos[c] = dict(sh=sh, inv=amt, pro=0.0, ei=i, ep=PX[i, c], peak=PX[i, c], part=amt / MTV[i, c] if MTV[i, c] > 0 else np.nan)
        return True
    def sell(self, c, frac, i, reason):
        if c not in self.pos or not TRADED[i, c]: return False
        p = self.pos[c]; sh = p["sh"] * frac
        pro = sh * PX[i, c] * (1 - side(c, i))
        self.cash += pro; p["pro"] += pro; p["sh"] -= sh
        if frac >= 0.9999:
            self.trades.append(dict(system=self.name, window=self.win, symbol=cols[c], entry=dates[p["ei"]], exit=dates[i], reason=reason,
                                    invested=p["inv"], proceeds=p["pro"], ret=p["pro"] / p["inv"] - 1, pnl=p["pro"] - p["inv"], part=p["part"]))
            del self.pos[c]
        return True

def run(system, win, i0, i1, kmi):
    sim = Sim(i0, system, win["name"])
    pend_sell, pend_buy = {}, []                 # c -> reason ; list of (c, frac_of_equity, expiry_i)
    last_month = None
    for i in range(i0, i1 + 1):
        # 1. execute orders raised at the previous close
        for c in list(pend_sell):
            if sim.sell(c, 1.0, i, pend_sell[c]): del pend_sell[c]
        keep = []
        for (c, fr, ex) in pend_buy:
            if c in sim.pos: continue
            if fr == "EQ":                      # S8 handled below
                continue
            eq = sim.value(i)
            if sim.buy(c, eq * fr, i): continue
            if ex > i: keep.append((c, fr, ex))
        pend_buy = keep
        if system == "S8" and getattr(sim, "reb", None) is not None:
            tg = sim.reb; sim.reb = None
            for c in list(sim.pos):
                if c not in tg: sim.sell(c, 1.0, i, "rotation")
            E_ = sim.value(i); t = E_ / len(tg) if tg else 0
            for c in tg:                        # trim first, then buy
                if c in sim.pos:
                    v = sim.pos[c]["sh"] * PX[i, c]
                    if v > t * 1.0001 and TRADED[i, c]:
                        sim.sell(c, (v - t) / v, i, "trim")
            for c in tg:
                v = sim.pos[c]["sh"] * PX[i, c] if c in sim.pos else 0.0
                if t - v > 0.01 * t: sim.buy(c, t - v, i)
        sim.eq.append(sim.value(i))
        if i == i1: break
        # 2. raise signals at this close for execution at i+1
        u = universe(i, kmi)
        month_end = dates[i].month != dates[i + 1].month or i == i0
        if system in ("S1", "S2", "S4", "S8") and month_end:
            if system == "S1":
                v = np.where(u, RET63[i], np.nan); k = 3
            elif system == "S2":
                v = np.where(u, MOM6_1[i], np.nan); k = 3
            elif system == "S8":
                v = np.where(u, MTV[i], np.nan); k = 10
            if system != "S4":
                ok = np.where(np.isfinite(v))[0]
                tg = [int(c) for c in ok[np.argsort(-v[ok])][:k]]
            else:
                k = 3; tg = []
                sec_ret = collections.defaultdict(list)
                for c in np.where(u & np.isfinite(RET126[i]))[0]:
                    if SECI[c] and SECI[c] != "Modarabas & takaful": sec_ret[SECI[c]].append(c)
                ranked = sorted([s for s, l in sec_ret.items() if len(l) >= 3], key=lambda s: -np.mean(RET126[i, sec_ret[s]]))[:3]
                for s in ranked:
                    best, bpe = None, np.inf
                    for c in sec_ret[s]:
                        pe = ttm_pe(c, i)
                        if np.isfinite(pe) and pe < bpe: best, bpe = c, pe
                    if best is not None: tg.append(best)
            if system == "S8":
                sim.reb = tg
            else:
                for c in list(sim.pos):
                    if c not in tg: pend_sell[c] = "rotation"
                pend_buy = [(c, 1.0 / k, i + 6) for c in tg if c not in sim.pos]
        elif system == "S3":
            for c, p in sim.pos.items():
                p["peak"] = max(p["peak"], PX[i, c])
                if PX[i, c] <= 0.8 * p["peak"]: pend_sell[c] = "trail_stop_20"
            free = 3 - len([c for c in sim.pos if c not in pend_sell]) - 0
            if free > 0:
                cand = np.where(u & TRADED[i] & (PX[i] > HI252[i]))[0]
                cand = [int(c) for c in cand if int(c) not in sim.pos]
                cand.sort(key=lambda c: -PX[i, c] / HI252[i, c])
                pend_buy = [(c, 1 / 3, i + 1) for c in cand[:free]]
        elif system == "S5":
            for c, p in sim.pos.items():
                if i - p["ei"] >= 60: pend_sell[c] = "time_60"
                elif PX[i, c] >= 1.25 * p["ep"]: pend_sell[c] = "target_25"
            free = 5 - len(sim.pos)
            if free > 0:
                cand = np.where(u & TRADED[i] & (PX[i] <= 0.8 * HI60[i]) & (RET126[i] > 0))[0]
                cand = [int(c) for c in cand if int(c) not in sim.pos]
                cand.sort(key=lambda c: -RET126[i, c])
                pend_buy = [(c, 0.2, i + 1) for c in cand[:free]]
        elif system == "S6":
            for c, p in sim.pos.items():
                if i - p["ei"] >= 90: pend_sell[c] = "time_90"
            free = 5 - len(sim.pos)
            ev = [(c, r) for c, r in EVENTS.get(i, []) if u[c] and c not in sim.pos and np.isfinite(PX[i - 1, c]) and PX[i, c] / PX[i - 1, c] - 1 < 0.05]
            ev.sort(key=lambda x: -x[1])
            pend_buy = [(c, 0.2, i + 1) for c, r in ev[:max(free, 0)]]
    for c in list(sim.pos):                      # liquidate at the end with costs; open trades flagged
        sh_before = sim.pos[c]["sh"]
        sim.sell(c, 1.0, i1, "end_open") if TRADED[i1, c] else None
        if c in sim.pos:                         # no trade on the last day: sell at last price, same cost
            p = sim.pos[c]; pro = p["sh"] * PX[i1, c] * (1 - side(c, i1)); sim.cash += pro; p["pro"] += pro
            sim.trades.append(dict(system=system, window=win["name"], symbol=cols[c], entry=dates[p["ei"]], exit=dates[i1], reason="end_open",
                                   invested=p["inv"], proceeds=p["pro"], ret=p["pro"] / p["inv"] - 1, pnl=p["pro"] - p["inv"], part=p["part"])); del sim.pos[c]
    eq = np.array(sim.eq); eq[-1] = sim.cash
    return eq, pd.DataFrame(sim.trades)

# ---------------- windows
WSTARTS = ["2016-12-30", "2018-10-01", "2020-10-01", "2022-10-01", "2024-10-01"]
WINS = []
for s in WSTARTS:
    i0 = int(dates.searchsorted(pd.Timestamp(s)))
    end = min(pd.Timestamp(s) + pd.DateOffset(years=2), dates[-1])
    i1 = int(dates.searchsorted(end, side="right")) - 1
    WINS.append(dict(name=f"{dates[i0]:%Y-%m-%d}", i0=i0, i1=i1, kmi=dates[i0] >= T_MEM_KNOWN))
i0 = int(dates.searchsorted(pd.Timestamp("2024-10-17")))
WINS.append(dict(name="2024-10-17*", i0=i0, i1=LAST, kmi=True))      # literal "two years ago to today"

KM = pd.read_csv(ROOT / "data/macro/kmiallshr.csv", index_col=0, parse_dates=True)["close"]
KSE = pd.read_csv(ROOT / "data/macro/kse100.csv", index_col=0, parse_dates=True)["close"]
def idxm(s, a, b): return s.asof(dates[b]) / s.asof(dates[a])

def stats(eq, tr, years):
    mult = eq[-1] / eq[0]
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    return dict(mult=mult, cagr=mult ** (1 / years) - 1 if mult > 0 else np.nan, dd=dd, n=len(tr),
                hit=(tr.ret > 0).mean() if len(tr) else np.nan, med=tr.ret.median() if len(tr) else np.nan)

# ---------------- oracle
def oracle(w, mode, step="M", fixed=True, cap=True, kmi=None):
    """Perfect foresight: at each rebalance buy the best next-period names. mode: 'top1', 'top3', 'wf1' (waterfall: fill best names in order, each up to its cap)."""
    i0, i1 = w["i0"], w["i1"]
    if step == "M":
        idx = [i0] + [i for i in range(i0, i1) if dates[i].month != dates[i + 1].month and i > i0] + [i1]
    else:
        idx = list(range(i0, i1, 5)) + [i1]
    idx = sorted(set(idx))
    u0 = universe(i0, w["kmi"])
    cash, pos = 50000.0, {}                    # pos: c -> value
    for a, b in zip(idx[:-1], idx[1:]):
        u = u0 if fixed else universe(a, w["kmi"])
        ok = u & TRADED[a] & TRADED[b] & np.isfinite(PX[a]) & np.isfinite(MTV[a])
        r = np.where(ok, PX[b] / PX[a] - 1, -9)
        rate = np.array([side(c, a) for c in range(len(cols))])
        net = np.where(ok, (1 + r) * (1 - rate) ** 2 - 1, -9)          # full round trip on a rotated name
        order = np.argsort(-net)
        E = cash + sum(pos.values())
        tgt = {}
        capv = 0.01 * MTV[a]
        k = {"top1": 1, "top3": 3, "wf1": 1}[mode]
        if mode == "wf1":
            rem = E
            for c in order:
                if net[c] <= 0 or rem <= 0: break
                x = min(rem, capv[c]) if cap else rem
                tgt[int(c)] = x; rem -= x
        else:
            for c in order[:k]:
                if net[c] <= 0: continue
                x = E / k
                tgt[int(c)] = min(x, capv[c]) if cap else x
        cost = sum(side(c, a) * abs(tgt.get(c, 0) - pos.get(c, 0)) for c in set(tgt) | set(pos))
        tot = sum(tgt.values())
        if tot > 0 and tot > E - cost: tgt = {c: v * (E - cost) / tot for c, v in tgt.items()}
        cash = E - cost - sum(tgt.values())
        pos = {c: v * (PX[b, c] / PX[a, c]) for c, v in tgt.items()}
    return (cash + sum(pos.values())) / 50000.0

def fmt(x, d=2):
    if x is None or not np.isfinite(x): return "-"
    if x >= 1e5: return f"{x:,.0f}"
    return f"{x:,.{d}f}"
def pc(x, d=0): return "-" if x is None or not np.isfinite(x) else f"{x:+.{d}%}"

# ===================================================================== run
SYS = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
RES, TR = {}, []
PLC = {}
out(f"Oracle and good case. Price panel: {'price-return (bonus/split only)' if PR else 'total return, dividends complete only from Nov 2024'}. Data to {dates[-1].date()}.")
out(f"Missed corporate actions repaired (one-session drops of 25%+/50%+, history rescaled, any liquidity): {len(CLEAN_EV)}: " + "; ".join(f"{c} {d} {r:+.0%}" for d, c, r in CLEAN_EV))
out("Windows (start close -> end close):")
for w in WINS:
    out(f"  {w['name']:<12} {dates[w['i0']].date()} -> {dates[w['i1']].date()}  {w['i1'] - w['i0']} sessions  universe: {'KMI All Share liquid' if w['kmi'] else 'all liquid names (membership unknown)'}")

for w in WINS:
    i0, i1 = w["i0"], w["i1"]; yrs = (dates[i1] - dates[i0]).days / 365.25
    eq0 = np.ones(i1 - i0 + 1)
    for s in SYS:
        if s == "S7":
            ix = KM.reindex(dates[i0:i1 + 1], method="ffill").values; eq = ix / ix[0] * 50000 * (1 - 0.0025) ** 2
            tr = pd.DataFrame([dict(system=s, window=w["name"], symbol="KMIALLSHR", entry=dates[i0], exit=dates[i1], reason="end_open", ret=eq[-1] / 50000 - 1,
                                    pnl=eq[-1] - 50000, invested=50000, proceeds=eq[-1], part=np.nan)])
            eq = eq.copy(); eq[0] = 50000
        else:
            eq, tr = run(s, w, i0, i1, w["kmi"])
        st = stats(eq, tr, yrs); RES[(s, w["name"])] = st
        TR.append(tr)

out("\n== A. Buy and hold, no costs: names liquid at the window start, start close to end close ==")
BH = {}
for w in WINS:
    i0, i1 = w["i0"], w["i1"]
    u = universe(i0, w["kmi"]) & np.isfinite(PX[i0]) & TRADED[max(i0 - 5, 0):i0 + 1].any(axis=0)
    last_obs = np.array([np.where(TRADED[:i1 + 1, c])[0].max() if TRADED[:i1 + 1, c].any() else -1 for c in range(len(cols))])
    alive = last_obs >= i1 - 20
    ok = u & alive & np.isfinite(PX[i1])
    m = pd.Series(PX[i1] / PX[i0], index=cols)[ok].dropna()
    BH[w["name"]] = m
    out(f"\nWindow {w['name']} ({dates[i0].date()} to {dates[i1].date()}): universe {int(u.sum())} names, {int(ok.sum())} priced at both ends ({int((u & ~alive).sum())} stopped trading before the end)")
    out(f"  >=2x {(m >= 2).mean():.1%} ({(m >= 2).sum()})  >=3x {(m >= 3).mean():.1%} ({(m >= 3).sum()})  >=5x {(m >= 5).mean():.1%} ({(m >= 5).sum()})  lost money {(m < 1).mean():.1%}  "
        f"median {m.median():.2f}x  mean {m.mean():.2f}x  worst {m.min():.2f}x  EW buy-and-hold (no rebalance) {m.mean():.2f}x")
    out(f"  KMI All Share TR {idxm(KM, i0, i1):.2f}x   KSE100 TR {idxm(KSE, i0, i1):.2f}x")
    t = m.sort_values(ascending=False).head(10)
    out("  top 10: " + "; ".join(f"{s} {v:.1f}x ({SEC.get(s, 'n/a')})" for s, v in t.items()))
    ref = {s: PX[i1, cidx[s]] / PX[i0, cidx[s]] for s in ["FFC", "OGDC", "MEBL", "FABL", "PPL", "HUBC"] if s in cidx and np.isfinite(PX[i0, cidx[s]])}
    out("  reference, hindsight-chosen current picks (not point in time, not a test): " + "  ".join(f"{s} {v:.2f}x" for s, v in ref.items()))

# delisted names that would have been in each window-start universe
dfiles = sorted((ROOT / "data/prices_delisted").glob("*.csv"))
dc, dv = {}, {}
for f in dfiles:
    try:
        x = pd.read_csv(f, usecols=["date", "close", "volume"], parse_dates=["date"], index_col="date")
    except Exception:
        continue
    x = x[~x.index.duplicated(keep="last")].sort_index()
    if len(x) < 40: continue
    dc[f.stem], dv[f.stem] = x.close, x.volume
dcl = pd.DataFrame(dc).reindex(dates); dvl = pd.DataFrame(dv).reindex(dates)
inside = dvl.notna().cummax() & dvl[::-1].notna().cummax()[::-1]
dvl = dvl.where(~(inside & dvl.isna()), 0.0)
dcl = dcl.where((dvl > 0) & (dcl > 0))
dret = P.returns(dcl, "crude", vol=dvl)
dtv = (dcl * dvl).fillna(0).where(dvl.notna())
dmtv = dtv.rolling(60, min_periods=40).median().shift(1)
out("\n== A2. Survivorship check: delisted names that were liquid at each window start (crude return adjustment, last trade or window end) ==")
for w in WINS:
    i0, i1 = w["i0"], w["i1"]
    liq = dmtv.iloc[i0] > 5e6
    names = list(liq[liq].index)
    rr = []
    for s in names:
        r = dret[s].iloc[i0 + 1:i1 + 1].fillna(0)
        rr.append((s, (1 + r).prod(), dcl[s].last_valid_index()))
    out(f"  {w['name']}: {len(names)} delisted names liquid at the start; " + ("; ".join(f"{s} {m:.2f}x (last trade {d.date() if d is not None else '-'})" for s, m, d in rr) if rr else "none"))

out("\n== B. Perfect-foresight upper bound (UNATTAINABLE; it only sets the scale). Multiple of Rs50,000 ==")
out("Universe fixed at the window start unless marked 'rolling'. Costs as above (0.5% round trip, 1.0% under Rs20m traded value). 'cap' = position in a name at most 1% of its trailing median daily traded value.")
ORC = {}
for w in WINS:
    r = dict(
        top1_unc=oracle(w, "top1", cap=False), top3_unc=oracle(w, "top3", cap=False),
        top1_cap=oracle(w, "top1"), top3_cap=oracle(w, "top3"), wf1_cap=oracle(w, "wf1"),
        wf1_roll=oracle(w, "wf1", fixed=False), top3_roll=oracle(w, "top3", fixed=False),
        wk3_cap=oracle(w, "top3", step="W"), wkwf_cap=oracle(w, "wf1", step="W"))
    ORC[w["name"]] = r
out(f"{'window':<13}{'best1 uncapped':>18}{'best3 uncapped':>18}{'best1 cap(cash)':>17}{'best3 cap':>11}{'waterfall cap':>15}{'roll waterfall':>16}{'roll best3':>12}{'weekly best3':>14}{'weekly wf':>11}")
for w in WINS:
    r = ORC[w["name"]]
    out(f"{w['name']:<13}{fmt(r['top1_unc']):>18}{fmt(r['top3_unc']):>18}{fmt(r['top1_cap']):>17}{fmt(r['top3_cap']):>11}{fmt(r['wf1_cap']):>15}{fmt(r['wf1_roll']):>16}{fmt(r['top3_roll']):>12}{fmt(r['wk3_cap']):>14}{fmt(r['wkwf_cap']):>11}")

# ---------------- placebo
rng = np.random.default_rng(20261018)
def placebo(w, n=200):
    i0, i1 = w["i0"], w["i1"]
    sig = [i for i in range(i0, i1) if dates[i].month != dates[i + 1].month]
    ex = [i0] + [s_ + 1 for s_ in sig if s_ + 1 < i1] + [i1]
    pools = []
    for k in range(len(ex) - 1):
        a, b = ex[k], ex[k + 1]
        u = universe(max(a - 1, i0), w["kmi"]) & TRADED[a] & np.isfinite(PX[b])
        pools.append((a, b, np.where(u)[0]))
    res = np.ones(n)
    for j in range(n):
        v = 1.0
        for a, b, pool in pools:
            if len(pool) < 3: continue
            pick = rng.choice(pool, 3, replace=False)
            g = [(PX[b, c] / PX[a, c]) * (1 - side(c, a)) * (1 - side(c, b)) for c in pick]
            v *= np.mean(g)
        res[j] = v
    return res
out("\n== C. Placebo: 200 random monthly rotations into 3 random liquid names (same dates, same costs, full turnover every month) ==")
for w in WINS:
    PLC[w["name"]] = placebo(w)
    p = PLC[w["name"]]
    out(f"  {w['name']:<13} p5 {np.percentile(p, 5):.2f}x  p25 {np.percentile(p, 25):.2f}x  median {np.median(p):.2f}x  p75 {np.percentile(p, 75):.2f}x  p95 {np.percentile(p, 95):.2f}x  max {p.max():.2f}x  share>=2x {(p >= 2).mean():.1%}  share>=3x {(p >= 3).mean():.1%}")

out("\n== D. Systems, Rs50,000 each window: multiple / CAGR / max drawdown / trades / hit rate / median trade / placebo percentile ==")
out("(n/a = the system had no usable signals or data in that window and stayed in cash; percentile = share of the 200 random paths the system beat)")
TRD = pd.concat(TR, ignore_index=True)
TRD.to_csv(ROOT / "tests/out/oracle_trades.csv" if not PR else ROOT / "tests/out/oracle_trades_pr.csv", index=False)
for w in WINS:
    out(f"\nWindow {w['name']}")
    out(f"{'sys':<5}{'multiple':>9}{'final Rs':>11}{'CAGR':>8}{'maxDD':>8}{'trades':>8}{'hit':>6}{'median':>8}{'plc pct':>9}")
    for s in SYS:
        r = RES[(s, w["name"])]
        na = (s in ("S4", "S6") and r["n"] == 0) or (s in ("S4", "S6") and r["mult"] == 1.0)
        pct = (PLC[w["name"]] < r["mult"]).mean()
        out(f"{s:<5}{(fmt(r['mult']) + 'x') if not na else 'n/a':>9}{fmt(r['mult'] * 50000, 0) if not na else '-':>11}{pc(r['cagr']) if not na else '-':>8}{(pc(r['dd']) if not na else '-'):>8}{r['n']:>8}"
            f"{(f'{r['hit']:.0%}' if np.isfinite(r['hit']) else '-'):>6}{pc(r['med']) if np.isfinite(r['med']) else '-':>8}{(f'{pct:.0%}' if not na else '-'):>9}")
    okS = [s for s in SYS if not (s in ("S4", "S6") and (RES[(s, w['name'])]["n"] == 0 or RES[(s, w['name'])]["mult"] == 1.0))]
    best = max(okS, key=lambda s: RES[(s, w['name'])]["mult"])
    out(f"  best of menu: {best} {RES[(best, w['name'])]['mult']:.2f}x; menu median {np.median([RES[(s, w['name'])]['mult'] for s in okS]):.2f}x; placebo median {np.median(PLC[w['name']]):.2f}x")

out("\n== E. Rank stability across windows (rank by multiple, 1 = best; systems with no signals excluded from that window) ==")
mt = pd.DataFrame({w["name"]: {s: RES[(s, w["name"])]["mult"] for s in SYS} for w in WINS})
for s in ("S4", "S6"):
    for w in WINS:
        if RES[(s, w["name"])]["n"] == 0 or RES[(s, w["name"])]["mult"] == 1.0: mt.loc[s, w["name"]] = np.nan
rk = mt.rank(ascending=False)
out(mt.round(2).to_string()); out("\nranks:"); out(rk.to_string())
main = [w["name"] for w in WINS[:5]]
sp = []
for a_ in range(5):
    for b_ in range(a_ + 1, 5):
        x, y = rk[main[a_]], rk[main[b_]]; ok = x.notna() & y.notna()
        if ok.sum() >= 4: sp.append((main[a_], main[b_], x[ok].corr(y[ok], method="spearman"), int(ok.sum())))
for a_, b_, rho, n_ in sp: out(f"  Spearman rank correlation {a_} vs {b_}: {rho:+.2f} (n={n_} systems)")
if sp: out(f"  mean pairwise {np.mean([x[2] for x in sp]):+.2f}; pairs with positive correlation {sum(x[2] > 0 for x in sp)} of {len(sp)}")
out("  winner per window: " + ", ".join(f"{c}: {mt[c].idxmax()}" for c in mt.columns))
w5 = WINS[4]["name"]
out(f"  rank of the {w5} winner ({mt[w5].idxmax()}) in other windows: " + ", ".join(f"{c}: {int(rk.loc[mt[w5].idxmax(), c]) if pd.notna(rk.loc[mt[w5].idxmax(), c]) else 'n/a'}" for c in main[:-1]))
out("  windows where the system beat S7 (KMI buy and hold) / beat placebo median / made >=1.0x, of the 5 main windows:")
for s in SYS:
    b7 = sum(RES[(s, c)]["mult"] > RES[("S7", c)]["mult"] for c in main if not pd.isna(mt.loc[s, c]))
    bp = sum(RES[(s, c)]["mult"] > np.median(PLC[c]) for c in main if not pd.isna(mt.loc[s, c]))
    po = sum(RES[(s, c)]["mult"] >= 1.0 for c in main if not pd.isna(mt.loc[s, c]))
    nn = sum(not pd.isna(mt.loc[s, c]) for c in main)
    out(f"   {s}: beat S7 in {b7}/{nn}; beat placebo median in {bp}/{nn}; at least 1.0x in {po}/{nn}; reached 2x in {sum(mt.loc[s, c] >= 2 for c in main if not pd.isna(mt.loc[s, c]))}")

out("\n== F. Largest participation: trade size as a share of the name's trailing median daily traded value ==")
for s in SYS:
    t_ = TRD[(TRD.system == s)]
    if len(t_) and t_.part.notna().any(): out(f"  {s}: max {t_.part.max():.2%}, trades above 1%: {(t_.part > 0.01).sum()} of {len(t_)}")

out("\n== G. 2024 to 2026: systems reaching 2x / 3x, and their trades ==")
for w in WINS[4:]:
    out(f"\nWindow {w['name']}: " + "; ".join(f"{s} {RES[(s, w['name'])]['mult']:.2f}x" for s in SYS))
    out(f"  reached 2x: {[s for s in SYS if RES[(s, w['name'])]['mult'] >= 2]}   reached 3x: {[s for s in SYS if RES[(s, w['name'])]['mult'] >= 3]}")
    for s in SYS:
        if RES[(s, w["name"])]["mult"] >= 2 and s != "S7":
            t_ = TRD[(TRD.system == s) & (TRD.window == w["name"])].sort_values("pnl", ascending=False).head(10)
            out(f"  {s} top 10 trades by Rs P&L (of {RES[(s, w['name'])]['n']}):")
            for r in t_.itertuples():
                out(f"    {r.symbol:<9}{r.entry.date()} -> {r.exit.date()}  {r.ret:+.0%}  Rs{r.pnl:,.0f}  {r.reason}  ({SEC.get(r.symbol, 'n/a')})")
    for s in SYS:
        if s not in ("S7",) and RES[(s, w["name"])]["mult"] < 2:
            t_ = TRD[(TRD.system == s) & (TRD.window == w["name"])]
            if len(t_): out(f"  {s} (below 2x) best trade {t_.sort_values('pnl').iloc[-1].symbol} {t_.ret.max():+.0%}; exit reasons: " + ", ".join(f"{k} {v}" for k, v in t_.reason.value_counts().items()))

(ROOT / "tests/out" / ("oracle_and_good_case_pr.txt" if PR else "oracle_and_good_case.txt")).write_text(buf.getvalue(), encoding="utf-8")
