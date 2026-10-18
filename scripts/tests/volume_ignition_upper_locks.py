"""Volume ignition with upper locks (the SSGC 2024 call). See tests/volume_ignition_upper_locks.md.
Run: .venv/Scripts/python.exe scripts/tests/volume_ignition_upper_locks.py
Raw output: tests/out/volume_ignition_upper_locks.txt (+ _trades.csv)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from prices import load_panel, returns  # noqa: E402

STRICT = len(sys.argv) > 1 and sys.argv[1] == "strict10"   # literal spec: lock = +-10% always; default: limit in force that day
SUF = "_strict10" if STRICT else ""
RNG = np.random.default_rng(20261018)
OUT = []
EXITS = ["trail20", "T20", "T60", "T120", "lock"]
VARS = ["V1", "V2", "V3", "V4"]
UNIVS = {"liq5": 5e6, "liq1": 1e6}
EXCL = [0]
COOL, MAXWAIT, NPOOL, NPLAC = 60, 10, 50000, 1000


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


# ---------------------------------------------------------------- panels (survivors adjusted TR + delisted crude)
close, vol, tv = load_panel()
adj = pd.read_parquet(ROOT / "data/panel_close_adj.parquet").reindex(index=close.index, columns=close.columns)
adjpr = pd.read_parquet(ROOT / "data/panel_close_adj_pricereturn.parquet").reindex(index=close.index, columns=close.columns)
dl = {}
for f in (ROOT / "data/prices_delisted").glob("*.csv"):
    if f.stem in close.columns:
        continue
    x = pd.read_csv(f, usecols=["date", "close", "volume"], parse_dates=["date"], index_col="date")
    x = x[~x.index.duplicated(keep="last")].sort_index()
    if len(x):
        dl[f.stem] = x
dc = pd.DataFrame({s: x.close for s, x in dl.items()}).reindex(close.index)
dv = pd.DataFrame({s: x.volume for s, x in dl.items()}).reindex(close.index)
inside = dv.notna().cummax() & dv[::-1].notna().cummax()[::-1]
dv = dv.where(~(inside & dv.isna()), 0.0)
dc = dc.where((dv > 0) & (dc > 0))
dup = []
for col in dc.columns:
    ref = pd.concat([close, dc[[c for c in dc.columns if c < col]]], axis=1)
    both = ref.notna() & dc[[col]].notna().values
    same = (ref.values == dc[[col]].values) & both.values
    n = both.values.sum(0)
    if ((same.sum(0) >= 0.9 * n) & (n >= 100)).any():
        dup.append(col)
dc, dv = dc.drop(columns=dup), dv.drop(columns=dup)
dret = returns(dc, "crude", vol=dv)
dlev = (1 + dret.fillna(0)).cumprod().where(dc.notna())
dlev = dlev / dlev.ffill().iloc[-1] * dc.ffill().iloc[-1]
CL = pd.concat([close, dc], axis=1)
ADJ = pd.concat([adj, dlev], axis=1)
TV = pd.concat([tv, (dc * dv).fillna(0).where(dv.notna())], axis=1)
VOL = pd.concat([vol, dv], axis=1)
# share-equivalent volume: undo bonus/split so a 1:1 bonus does not fake a 2x volume ignition (survivors only)
fac = (close / adjpr).ffill().bfill().reindex(columns=VOL.columns).fillna(1.0)
VADJ = VOL * fac
SYMS = list(CL.columns)
days = CL.index
N, END = len(days), len(days) - 1
si = {s: i for i, s in enumerate(SYMS)}
kmi = set(pd.read_csv(ROOT / "data/kmi_allshare_2026-06-05.csv").symbol)
KMI = np.array([s in kmi for s in SYMS])
P(f"Panel {N} days {days[0].date()} to {days[-1].date()}; {close.shape[1]} survivors + {dc.shape[1]} delisted (crude); "
  f"{KMI.sum()} names flagged KMI All Share (list of 5 Jun 2026, hindsight flag)")

# daily price limit in force (read off the data: moves cluster at 5% to Mar 2020, 7.5% to 5 Jul 2024, 10% from 8 Jul 2024)
LIM = np.where(days < pd.Timestamp("2020-03-30"), 0.05, np.where(days < pd.Timestamp("2024-07-08"), 0.075, 0.10))
if STRICT:
    LIM = np.full(N, 0.10)

# unadjusted corporate actions: for a stock priced Rs20 or more the percentage limit binds, so a one-day DROP beyond it cannot be a
# trade (e.g. KML 10:1 split, 6 Oct 2025); a drop of more than 40% is a corporate action at any price. Zero it in the adjusted series.
# Stocks under Rs20 trade with a wider band (moves of 15-25% in a day are common), so their big moves stay. Upward moves are only counted.
nd = nu = 0
ADJ = ADJ.copy()
ANOM = np.zeros((N, ADJ.shape[1]), bool)
for col in ADJ.columns:
    x = ADJ[col].dropna()
    if len(x) < 3:
        continue
    r = x.values[1:] / x.values[:-1]
    L = LIM[days.get_indexer(x.index[1:])]
    pr0 = CL[col].reindex(x.index).values[:-1]
    dn = (r < (1 - L) * 0.985) & ((pr0 >= 20) | (r < 0.6))
    nd += dn.sum()
    nu += ((r > (1 + L) * 1.015) & (pr0 >= 20)).sum()
    if dn.any():
        ANOM[days.get_indexer(x.index[1:])[dn], ADJ.columns.get_loc(col)] = True
        r = np.where(dn, 1.0, r)
        ADJ.loc[x.index, col] = x.values[0] * np.concatenate([[1.0], np.cumprod(r)])
P(f"Adjusted-series clean-up: {nd} one-day drops beyond the limit (price >= Rs20) or over 40% (any price) set to zero return "
  f"(unadjusted splits, data breaks); {nu} upward moves beyond the limit on prices >= Rs20 left in")

Af = ADJ.ffill()
AF = Af.values
CLv = CL.values
ADJv = ADJ.values
obs = CL.notna().values & ADJ.notna().values

# ---------------------------------------------------------------- per-symbol observation arrays and lock flags
SD = {}
UP = np.zeros((N, len(SYMS)), bool)
LO = np.zeros((N, len(SYMS)), bool)
for s, i in si.items():
    r = np.nonzero(obs[:, i])[0]
    if len(r) < 3:
        continue
    cl, px = CLv[r, i], ADJv[r, i]
    up = np.zeros(len(r), bool)
    lo = np.zeros(len(r), bool)
    rr = cl[1:] / cl[:-1]
    ra = px[1:] / px[:-1]
    L = LIM[r[1:]]
    cheap = cl[:-1] < 20       # under Rs20 the band is wider than the percentage limit: a close at or above the limit move counts
    up[1:] = (rr >= (1 + L) * 0.995) & (rr <= np.where(cheap, 1.3, (1 + L) * 1.015))
    lo[1:] = (ra <= (1 - L) * 1.005) & (ra >= np.where(cheap, 0.6, (1 - L) * 0.985))
    UP[r, i], LO[r, i] = up, lo
    SD[s] = dict(rows=r, px=px, up=up, lo=lo, lock=up | lo, last=r[-1], i=i)
P(f"Upper-lock closes in panel: {UP.sum()}, lower-lock closes: {LO.sum()} (mode {'strict +-10% always' if STRICT else 'limit in force: 5% / 7.5% / 10%'}; "
  f"lock = move at or beyond (limit less 0.5%); capped at limit +1.5% for prices >= Rs20, +30% below Rs20; upper on raw close, lower on adjusted close)")

# ---------------------------------------------------------------- regime per day (6M T-bill minus policy rate)
tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"]).set_index("date").y6m
pr = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"]).set_index("date").rate
spread = (tb.reindex(tb.index.union(days)).ffill().reindex(days) - pr.reindex(pr.index.union(days)).ffill().reindex(days))
REG = np.where(spread.values > 0, "bill>policy", "bill<=policy")
REG = np.where(spread.isna().values, "n/a", REG)
YEAR = days.year.values
YQ = days.year.values * 10 + days.quarter.values   # placebo matching key: calendar quarter

# ---------------------------------------------------------------- signals
med60 = TV.rolling(60, min_periods=40).median().values
m20 = VADJ.rolling(20, min_periods=15).mean()
p120 = VADJ.shift(20).rolling(120, min_periods=100).mean()
VR = (m20 / p120.where(p120 > 0)).values
RET20 = (Af / Af.shift(20) - 1).values
UPf = pd.DataFrame(UP.astype(float))
NU5 = UPf.rolling(5).sum().values
NU10 = UPf.rolling(10).sum().values
NU60p = UPf.shift(1).rolling(60, min_periods=60).sum().values
rmax, rmin = Af.shift(1).rolling(20, min_periods=20).max().values, Af.shift(1).rolling(20, min_periods=20).min().values
RNG20 = rmax / rmin - 1
lastobs = pd.DataFrame(np.where(obs, np.arange(N)[:, None], np.nan)).ffill().values
fresh = (np.arange(N)[:, None] - lastobs) <= 5
ok = fresh & (np.arange(N)[:, None] >= 140)
COND = {
    "V1": (VR >= 3) & (NU5 >= 2),
    "V2": (VR >= 3) & (NU10 >= 3),
    "V3": (VR >= 3) & (RET20 > 0.25),
    "V4": UP & (NU60p == 0) & (RNG20 < 0.15),
}


def signals(cond):
    """(sym index, row) of the first true day after >= COOL rows of no true day, per symbol."""
    out = []
    for i in range(cond.shape[1]):
        w = np.nonzero(cond[:, i])[0]
        if not len(w):
            continue
        gap = np.diff(w, prepend=-10**6)
        out += [(i, r) for r in w[gap > COOL]]
    return out


# ---------------------------------------------------------------- trade simulation
def fill(sd, t):
    j = int(np.searchsorted(sd["rows"], t, "right"))
    while j < len(sd["rows"]) and sd["rows"][j] <= t + MAXWAIT and sd["lock"][j]:
        j += 1
    if j >= len(sd["rows"]) or sd["rows"][j] > t + MAXWAIT:
        return None
    return j


def nxt(sd, k):
    """first obs index after k whose close is not locked"""
    j = k + 1
    while j < len(sd["rows"]) and sd["lock"][j]:
        j += 1
    return j if j < len(sd["rows"]) else None


def sim(i, t, rule):
    """-> None (unfillable) or (fill_row, exit_row, gross, net, status, fill_idx, cost); status 0 closed by rule,
    1 still open (alive, marked at last close), 2 symbol ended (delisted; exit at last close)."""
    s = SYMS[i]
    sd = SD.get(s)
    if sd is None:
        return None
    je = fill(sd, t)
    if je is None:
        return None
    px, rows = sd["px"], sd["rows"]
    p0 = px[je]
    alive = sd["last"] >= END - 5
    status, jx = 0, None
    if rule == "trail20":
        seg = px[je:]
        hit = np.nonzero(seg <= 0.8 * np.maximum.accumulate(seg))[0]
        if len(hit):
            jx = nxt(sd, je + int(hit[0]))
    elif rule == "lock":
        lk = np.nonzero(sd["lo"][je + 1:])[0]
        if len(lk):
            jx = nxt(sd, je + 1 + int(lk[0]))
    else:
        jx = int(np.searchsorted(rows, rows[je] + int(rule[1:]), "left"))
        while jx < len(rows) and sd["lock"][jx]:
            jx += 1
        if jx >= len(rows):
            jx = None
    if jx is None:
        jx, status = len(rows) - 1, (1 if alive else 2)
    if ANOM[max(t - 140, 0):rows[jx] + 1, i].any():       # data break (capital reduction, unadjusted split) in the lookback or the hold
        EXCL[0] += 1
        return None
    gross = px[jx] / p0 - 1
    m = med60[t, i]
    cost = 0.005 + (0.005 if not (m >= 20e6) else 0)
    return rows[je], rows[jx], gross, gross - cost, status, je, cost


def stats(x):
    x = np.asarray(x, float)
    return dict(n=len(x), mean=x.mean() * 100, med=np.median(x) * 100, win=(x > 0).mean() * 100,
                p50=(x > .5).mean() * 100, m30=(x < -.3).mean() * 100, worst=x.min() * 100, best=x.max() * 100)


def counted(rule, res):
    """results that enter statistics: time stops need maturity"""
    return [r for r in res if r is not None and not (rule.startswith("T") and r[4] == 1)]


def totrade(x):
    r = x["r"]
    return (r[0], r[1], x["i"], SD[x["sym"]]["px"][r[5]], r[6], r[4], med60[x["sig"], x["i"]])


# ---------------------------------------------------------------- sleeve (Rs50k, up to 3 positions, equal thirds of equity)
def sleeve(trades, cap=50000.0, slots=3):
    """trades: (fill_row, exit_row, sym_i, entry_px, cost, status, tv). -> final multiple, max dd %, taken, skipped"""
    if not trades:
        return None
    trades = sorted(trades, key=lambda x: (x[0], -x[6]))
    ent = {}
    for k, tr in enumerate(trades):
        ent.setdefault(tr[0], []).append(k)
    cash, pos, eq, taken, skipped = cap, {}, [], 0, 0
    for t in range(trades[0][0], N):
        for k in [k for k, p in pos.items() if p["exit"] <= t and trades[k][5] != 1]:   # open ones are held to the end
            p = pos.pop(k)
            cash += p["sh"] * AF[t, p["i"]] * (1 - p["cost"] / 2)
        for k in ent.get(t, []):
            fr, xr, i, p0, cost, st, _ = trades[k]
            if len(pos) >= slots or cash < 100:
                skipped += 1
                continue
            tot = cash + sum(p["sh"] * AF[t, p["i"]] for p in pos.values())
            a = min(cash, tot / slots)
            cash -= a
            pos[k] = dict(sh=a * (1 - cost / 2) / p0, i=i, exit=xr, cost=cost)
            taken += 1
        eq.append(cash + sum(p["sh"] * AF[t, p["i"]] for p in pos.values()))
    eq = np.array(eq)
    return eq[-1] / cap, (eq / np.maximum.accumulate(eq) - 1).min() * 100, taken, skipped


# ---------------------------------------------------------------- placebo pools (random liquid symbol-days, same fill and exits)
POOL = {}
for u, thr in UNIVS.items():
    base = ok & (med60 >= thr) & (np.arange(N)[:, None] < END - 1)
    tt, ii = np.nonzero(base)
    pick = RNG.choice(len(ii), min(NPOOL, len(ii)), replace=False)
    POOL[u] = {}
    for rule in EXITS:
        rs = [(YQ[r[0]], r[3], r[4], r[2]) for r in (sim(ii[k], tt[k], rule) for k in pick) if r is not None]
        POOL[u][rule] = np.array(rs)       # year, net, status, gross
P(f"Placebo pools: up to {NPOOL} random (symbol, day) entries per universe and exit, same fill rule, exits and costs, "
  f"resampled in the signals' own fill-quarter mix, {NPLAC} draws")


def placebo(u, rule, years, real):
    pool = POOL[u][rule]
    if rule.startswith("T"):
        pool = pool[pool[:, 2] != 1]
    cols = []
    for y in sorted(set(years)):
        py = pool[pool[:, 0] == y][:, 1]
        if len(py) < 30:                                  # thin quarter: fall back to the same year
            py = pool[pool[:, 0] // 10 == y // 10][:, 1]
        k = sum(1 for z in years if z == y)
        cols.append(py[RNG.integers(0, len(py), size=(NPLAC, k))])
    M = np.concatenate(cols, axis=1)
    pm, pmean = np.median(M, 1) * 100, M.mean(1) * 100
    return dict(pmed=np.median(pm), pmean=np.median(pmean), p_med=(pm >= real["med"]).mean(), p_mean=(pmean >= real["mean"]).mean(),
                pwin=(M > 0).mean() * 100, pp50=(M > .5).mean() * 100, pm30=(M < -.3).mean() * 100)


# ---------------------------------------------------------------- run
ALL, SIG = {}, {}
for u, thr in UNIVS.items():
    for v in VARS:
        sg = signals(COND[v] & ok & (med60 >= thr))
        SIG[(u, v)] = sg
        for rule in EXITS:
            ALL[(u, v, rule)] = [dict(i=i, sym=SYMS[i], sig=t, r=sim(i, t, rule)) for i, t in sg]

P("\n=== SIGNAL COUNTS (first day after 60 sessions of no signal state, per symbol) ===")
for u in UNIVS:
    for v in VARS:
        sg = SIG[(u, v)]
        L = ALL[(u, v, "T20")]
        got = [x for x in L if x["r"] is not None]
        syms = len({i for i, _ in sg})
        qtr = len({(days[t].year, days[t].quarter) for _, t in sg})
        kn = sum(KMI[i] for i, _ in sg)
        chase = [AF[x["r"][0], x["i"]] / AF[x["sig"], x["i"]] - 1 for x in got]
        P(f"{u} {v}: signals {len(sg)}, fillable within {MAXWAIT} sessions and free of data breaks {len(got)} ({len(got) / max(len(sg), 1):.0%}), symbols {syms}, "
          f"calendar quarters {qtr}, KMI {kn}; median move signal close -> fill close {np.median(chase) * 100:+.1f}% "
          f"(mean {np.mean(chase) * 100:+.1f}%)")

HDR = ("variant exit   |   n syms qtrs | mean   median  win%  >+50% <-30%  worst | plc.med plc.mean p(med) p(mean) plc.win plc>50 plc<-30 | "
       "sleeve   maxDD taken skip | open/ended")
for u in UNIVS:
    P(f"\n=== HEADLINE, universe {u} (60-session median traded value above Rs{UNIVS[u] / 1e6:.0f}m), net returns in % ===")
    P(HDR)
    for v in VARS:
        for rule in EXITS:
            L = ALL[(u, v, rule)]
            c = [x for x in L if x["r"] is not None and not (rule.startswith("T") and x["r"][4] == 1)]
            if not c:
                continue
            st = stats([x["r"][3] for x in c])
            pl = placebo(u, rule, [YQ[x["r"][0]] for x in c], st)
            syms = len({x["i"] for x in c})
            qtr = len({(days[x["r"][0]].year, days[x["r"][0]].quarter) for x in c})
            sl = sleeve([totrade(x) for x in L if x["r"] is not None])
            no = sum(1 for x in c if x["r"][4] == 1)
            ne = sum(1 for x in c if x["r"][4] == 2)
            P(f"{v:4} {rule:7} | {st['n']:3d} {syms:4d} {qtr:4d} | {st['mean']:+6.1f} {st['med']:+6.1f} {st['win']:4.0f} {st['p50']:5.1f} {st['m30']:5.1f} "
              f"{st['worst']:+5.0f} | {pl['pmed']:+6.1f} {pl['pmean']:+6.1f} {pl['p_med']:6.3f} {pl['p_mean']:6.3f} {pl['pwin']:6.0f} {pl['pp50']:6.1f} {pl['pm30']:7.1f} | "
              f"{sl[0]:5.2f}x {sl[1]:6.0f}% {sl[2]:4d} {sl[3]:4d} | {no}/{ne}")


P("\np(med), p(mean) = share of 1000 placebo draws (random liquid entries, same quarters, same exit) at or above the real median / mean; "
  "near 0 = better than random, near 1 = worse.")
P("\n=== CLUSTER CHECK: signals grouped by fill quarter; mean of quarter means, share of quarters with positive mean, overall mean without the best quarter ===")
for u in UNIVS:
    for rule in ("trail20", "T60"):
        for v in VARS:
            c = [x for x in ALL[(u, v, rule)] if x["r"] is not None and not (rule.startswith("T") and x["r"][4] == 1)]
            q = pd.DataFrame({"q": [YQ[x["r"][0]] for x in c], "net": [x["r"][3] * 100 for x in c]})
            g = q.groupby("q").net.agg(["mean", "size"])
            best = g["mean"].idxmax()
            P(f"{u} {rule} {v}: quarters {len(g)}; mean of quarter means {g['mean'].mean():+.1f}; median quarter mean {g['mean'].median():+.1f}; "
              f"positive quarters {(g['mean'] > 0).mean():.0%}; best quarter {best} (n {int(g.loc[best, 'size'])}, mean {g.loc[best, 'mean']:+.1f}); "
              f"overall mean without it {q[q.q != best].net.mean():+.1f}")


def split(u, rule, key, keyname):
    P(f"\n--- split by {keyname}, universe {u}, exit {rule}: n/median%/mean%/win% ---")
    for v in VARS:
        c = [x for x in ALL[(u, v, rule)] if x["r"] is not None and not (rule.startswith("T") and x["r"][4] == 1)]
        g = {}
        for x in c:
            g.setdefault(key(x["r"]), []).append(x["r"][3])
        P(f"{v}: " + "; ".join(f"{k}: {len(a)}/{np.median(a) * 100:+.0f}/{np.mean(a) * 100:+.0f}/{(np.array(a) > 0).mean() * 100:.0f}"
                                for k, a in sorted(g.items())))


for u in UNIVS:
    for rule in ("trail20", "T60"):
        split(u, rule, lambda r: int(YEAR[r[0]]), "fill year")
    for rule in EXITS:
        split(u, rule, lambda r: REG[r[0]], "regime (6M T-bill vs policy rate, at fill)")

P("\n=== KMI flag (hindsight membership), net %, n/median/mean/win%/worst ===")
for u in UNIVS:
    for rule in ("trail20", "T60"):
        for v in VARS:
            row = []
            for lab, f in (("KMI", True), ("non-KMI", False)):
                c = [x["r"][3] for x in ALL[(u, v, rule)] if x["r"] is not None and KMI[x["i"]] == f
                     and not (rule.startswith("T") and x["r"][4] == 1)]
                if c:
                    s = stats(c)
                    row.append(f"{lab} {s['n']}/{s['med']:+.1f}/{s['mean']:+.1f}/{s['win']:.0f}/{s['worst']:+.0f}")
            P(f"{u} {rule} {v}: " + " | ".join(row))
    for v in VARS:
        L = [x for x in ALL[(u, v, "trail20")] if KMI[x["i"]] and x["r"] is not None]
        sl = sleeve([totrade(x) for x in L])
        if sl:
            P(f"{u} {v} KMI-only trail20 sleeve: {sl[0]:.2f}x, max drawdown {sl[1]:.0f}%, taken {sl[2]}, skipped {sl[3]}")

# ---- winners and losers (any variant, liq1, trail20)
P("\n=== 30 largest winners and 30 largest losers: signal from any variant, universe liq1, 20% trailing stop, net % ===")
tag = {}
for v in VARS:
    for x in ALL[("liq1", v, "trail20")]:
        if x["r"] is not None:
            tag.setdefault((x["i"], x["r"][0]), dict(x=x, vs=set()))["vs"].add(v)
rows_ = []
for (i, fr), d in sorted(tag.items()):
    if rows_ and rows_[-1]["i"] == i and fr - rows_[-1]["fill"] <= COOL:     # same episode
        rows_[-1]["vs"] |= d["vs"]
        continue
    r = d["x"]["r"]
    rows_.append(dict(i=i, sym=SYMS[i], sig=days[d["x"]["sig"]].date(), fill=fr, filld=days[fr].date(), exitd=days[r[1]].date(),
                      net=r[3] * 100, st=r[4], vs=set(d["vs"]), kmi=KMI[i]))
W = pd.DataFrame(rows_)
W["vs"] = W.vs.map(lambda s: "+".join(sorted(s)))
P(f"Episodes (same symbol, fills within {COOL} sessions merged): {len(W)}; status 1 = still open, 2 = delisted")
show = lambda d: d[["sym", "sig", "filld", "exitd", "net", "vs", "kmi", "st"]].round(1).to_string(index=False)
P("WINNERS\n" + show(W.sort_values("net", ascending=False).head(30)))
P("LOSERS\n" + show(W.sort_values("net").head(30)))
W.drop(columns=["fill", "i"]).to_csv(ROOT / f"tests/out/volume_ignition_upper_locks{SUF}_trades.csv", index=False)
P(f"All {len(W)} episodes: mean {W.net.mean():+.1f}%, median {W.net.median():+.1f}%, win {(W.net > 0).mean():.0%}; "
  f"top 5 winners hold {W.net.nlargest(5).sum() / W.net[W.net > 0].sum():.0%} of all positive net returns; "
  f"mean with the top 5 removed {W.net.nsmallest(len(W) - 5).mean():+.1f}%")

# ---- SSGC
P("\n=== SSGC ===")
i = si["SSGC"]
for u in UNIVS:
    for v in VARS:
        for (j, t) in SIG[(u, v)]:
            if j != i or days[t] < pd.Timestamp("2023-06-01"):
                continue
            out = []
            for rule in EXITS:
                r = sim(i, t, rule)
                out.append(f"{rule}: " + ("unfillable" if r is None else
                                          f"{days[r[0]].date()}->{days[r[1]].date()} {r[3] * 100:+.0f}%" + (" (open)" if r[4] == 1 else "")))
            P(f"{u} {v} signal {days[t].date()} (vol ratio {VR[t, i]:.1f}, locks5 {NU5[t, i]:.0f}, locks10 {NU10[t, i]:.0f}, "
              f"ret20 {RET20[t, i] * 100:+.0f}%, KMI {KMI[i]}): " + "; ".join(out))
seg = pd.Series(UP[:, i], days)
P("SSGC upper-lock days Oct 2024 to Jan 2025: " + ", ".join(str(d.date()) for d in seg["2024-10-01":"2025-01-31"][lambda s: s].index))

# ---- operator pump round trip
P("\n=== Round trips: share of signals that gave back the whole run or fell hard within 60 sessions of the fill ===")
for u in UNIVS:
    for v in VARS:
        c = [x for x in ALL[(u, v, "T60")] if x["r"] is not None and x["r"][4] != 1]
        if not c:
            continue
        erased = fall30 = peak = 0
        for x in c:
            r, t, i = x["r"], x["sig"], x["i"]
            sd = SD[x["sym"]]
            base = AF[max(t - 20, 0), i]
            seg = sd["px"][r[5]:int(np.searchsorted(sd["rows"], r[0] + 60, "left")) + 1]
            erased += seg[-1] <= base
            fall30 += seg[-1] <= 0.7 * sd["px"][r[5]]
            peak += seg.max() >= 1.2 * sd["px"][r[5]] and seg[-1] <= base
        P(f"{u} {v}: n {len(c)}; close at fill+60 at or below the pre-run price (close 20 sessions before signal): {erased / len(c):.0%}; "
          f"fell 30%+ from fill: {fall30 / len(c):.0%}; rose 20%+ after fill first, then erased the whole run: {peak / len(c):.0%}")
    pl = POOL[u]["T60"]
    pl = pl[pl[:, 2] != 1]
    P(f"{u} random entries, T60: net below -30%: {(pl[:, 1] < -.3).mean():.1%} (n {len(pl)})")

# ---- today's screen
P(f"\n=== TODAY'S SCREEN, {days[-1].date()} (universe liq1; condition true on any of the last 5 sessions; * = KMI All Share) ===")
rows_ = []
for i in range(len(SYMS)):
    for v in VARS:
        for k in range(5):
            t = END - k
            if ok[t, i] and med60[t, i] >= 1e6 and COND[v][t, i]:
                rows_.append((SYMS[i] + ("*" if KMI[i] else ""), v, days[t].date(), round(VR[t, i], 1), int(NU5[t, i]), int(NU10[t, i]),
                              round(RET20[t, i] * 100), round(med60[t, i] / 1e6, 1), "locked now" if UP[END, i] else ""))
                break
T = pd.DataFrame(rows_, columns=["sym", "var", "latest_true", "volratio", "locks5", "locks10", "ret20%", "medTV_Rs_m", "note"])
P(T.sort_values(["var", "sym"]).to_string(index=False) if len(T) else "none")

(ROOT / f"tests/out/volume_ignition_upper_locks{SUF}.txt").write_text("\n".join(OUT), encoding="utf-8")
