"""Pattern mining on the daily table: 40 pre-registered short-horizon rules. See tests/pattern_mining_daily.md.
Run: .venv/Scripts/python.exe scripts/tests/pattern_mining_daily.py
Raw output: tests/out/pattern_mining_daily.txt (+ _results.csv, _books.csv)

PRE-REGISTRATION (written before any run; nothing below was tuned after seeing results)
=======================================================================================
Data: data/daily_table.parquet. Signals use features at the close of t. Entry at next_open (session t+1, the symbol
must trade then: ret_fwd_1 not null). Costs per trade: 0.5% round trip, plus 0.5% more if median traded value (60d)
is under Rs20m. CGT is not in the returns. Net return = gross - cost.
Execution filter: a signal is dropped if the entry session opens at the limit up (gap_open >= 0.97 x limit in force:
5% to 2020-03-27, 7.5% to 2024-07-05, 10% after), because that open cannot be bought. Rows with |ret_1d| > 35%
are treated as data breaks and never signal. Placebo pools use the same two filters.
Universe: "liquid" = median traded value (60d) above Rs5m (R1, R2, R10, R11, R12, R16 as the brief says). Every other
rule uses names above Rs1m (tradable at Rs50k). Tiers reported: >=Rs20m, Rs5-20m, "under Rs5m" (= Rs1-5m, the floor).

Rules (40):
 R1a  top-1 gainer of the day (ret_1d) among liquid names           R1b  same, excluding names that closed on an upper lock
 R1c  top-1 gainer among names above Rs20m
 R2a  top-3 gainers among liquid                                    R2b  same, excluding upper-locked closes
 R3a  first upper lock (none in prior 20 sessions) after a base: 20-session close range (t-20..t-1) under 15%
 R3b  R3a and vol_ratio_1_20 >= 2
 R4   upper lock today and another in the 2 sessions before
 R5a/b/c  exactly 3 / 4 / 5 consecutive up days (consecutive_up_days)
 R6a/b/c/d  gap_open > 3% and vol_ratio_1_20 >= 2 with a filing since the prior close of class: financial_result /
            material_info / dividend_or_bonus / any (f_total > 0)
 R7   same gap-up and volume with no filing (f_total == 0)
 R8a  ret_1d >= 5% with a financial_result filing      R8b  ret_1d >= 5% without one
 R9   dip of 5%+ (ret_1d <= -5%) where the previous close was within 5% of its 20-session high (max close t-20..t-1)
 R10  KMI index day <= -3%: buy the 3 liquid names that fell least    R11a  the 3 that fell most   R11b  same, not lower-locked
 R12  sector leader (liquid) up >= 7% on the day while another liquid peer in the sector is up < 2% (and > -5%): buy the peer
 R13a/b/c  news-less rise: ret_5d > 8% & no filing in 10 sessions (days_since_last_filing > 10) / ret_5d > 8% & none in 5 /
           ret_5d > 12% & none in 20; each with the sector filter (sector_ret_5d < 3%, index_ret_5d if no sector basket)
           and "_ns" without it. A name that never filed counts as no filing.
 R14  board meeting notice in the last 30 days (next_board_meeting_known) and ret_5d > 5%
 R15  financial_result filing assigned to today and ret_1d >= 3% (the reaction day); buy next open
 R16  Friday with index_ret_1d <= -2%: buy the 3 most liquid names (index proxy) at Monday's open
 R17a new 252-session high today (dist_252_high >= 0)   R17b same and vol_ratio_1_20 >= 2
 R18a dist_252_high <= -20% and exactly 3 up days        R18b same and vol_ratio_1_20 >= 2
 R19  ret_1d >= 5% and vol_ratio_1_20 >= 3   R20  ret_1d <= -5% and vol_ratio_1_20 >= 3
 R21  lower-lock close today   R22  ret_3d <= -10%
Exits (each run separately), from next_open:
 E1 close1   sell at the close of the entry session
 E2 tgt5_3   +5% limit target (touched by the high, table mfe) or the close of session 3
 E3 tgt10_5  +10% limit target or the close of session 5
 E4 lock5    close of the first session that closes at an upper lock (first_upper_lock_within_5), else close of session 5
 E5 red20    close of the first session closing below the prior close, else close of session 20 (cap added so the book can run)
 E6 trail20  20% trailing stop on closes from the running peak of closes (entry price counts), else close of session 20
 X7 open2    (R1 and R2 only, exploratory, not in the 240) sell at the open of the session after the entry session
 When a target is hit the model books exactly the target; the session of the hit is taken as the earliest bound the table
 shows (1, else 3 or 5) for capital release, which is conservative.
Statistics: n signals, independent episodes (a symbol's signals within 10 sessions merged), distinct dates, mean, median,
 win rate (net > 0), share > +10%, share > +50%, worst, all net of costs. In-sample = signal date <= 2026-08-31; out of
 sample = 2026-09-01 to 2026-10-16. Splits: regime (bill>policy / bill<=policy), tier, halves (to 2021, 2022 on), KMI member.
Placebo: each signal replaced by a random name on the same date in the same liquidity tier (4 tiers: >=20m, 5-20m, 1-5m,
 <1m), same exit, same costs. Excess = mean net minus the exact expected placebo mean. p-value: 400 draws of the
 episode-first IS signals (one-sided on the mean).
Multiple testing: 40 rules x 6 exits = 240 tests. Chosen threshold p <= 0.01 (expected false passes 2.4 of 240);
 Benjamini-Hochberg at 10% also shown.
SURVIVOR = all of: (S1) IS episodes >= 100, IS mean net > 0, IS excess > 0, p <= 0.01;
 (S2) both regimes: IS mean net > 0 and excess > 0; (S3) both IS halves mean net > 0 and excess > 0;
 (S4) OOS n >= 10 with mean net > 0 and excess > 0. A rule with S1-S3 but OOS n < 10 is "untested out of sample".
Book: Rs50,000, fully reinvested, up to 3 positions, candidates in order of vol_ratio_1_20 (all of a day's picks split the
 cash equally; a name already held is skipped), costs inside each trade, positions still open at the window end marked at
 the close less costs. Every rolling 30-session window from 2017 to 2026-10-16, plus 2026-08-14..2026-09-15 and
 2026-09-16..2026-10-16. Placebo book: every session random liquid names (>Rs5m) fill the free slots, same exit and costs,
 5 seeds pooled.
"""
import sys
from bisect import bisect_left, bisect_right
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTP = ROOT / "tests" / "out"
NS = 2480                      # calendar sessions
PAD = 30
IS_END = pd.Timestamp("2026-08-31")
OOS_START = pd.Timestamp("2026-09-01")
D_PLC = 400
EXITS = ["close1", "tgt5_3", "tgt10_5", "lock5", "red20", "trail20"]
RNG = np.random.default_rng(20261018)
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


# ------------------------------------------------------------------ worker (book simulation)
_G = {}


def _init(path, cost, wins):
    _G["path"], _G["cost"], _G["wins"] = path, cost, wins


def _sim(days, bydays, s, e):
    cash = 1.0
    pos = []
    i = bisect_left(days, s)
    n = len(days)
    while i < n and days[i] <= e:
        d = days[i]
        i += 1
        if pos:
            keep = []
            for p in pos:
                if p[0] < d:
                    cash += p[1]
                else:
                    keep.append(p)
            pos = keep
        free = 3 - len(pos)
        if free == 0 or cash <= 1e-9:
            continue
        held = {p[2] for p in pos}
        take = []
        for c in bydays[d]:
            if c[2] not in held:
                take.append(c)
                if len(take) == free:
                    break
        if not take:
            continue
        a = cash / len(take)
        cash = 0.0
        for c in take:
            pos.append((c[3], a * c[4], c[2], c, a))
    for p in pos:
        if p[0] <= e:
            cash += p[1]
        else:
            c = p[3]
            cash += p[4] * c[5][e - c[1] - 1]
    return cash


def run_task(task):
    rows, tt, symc, free, mult = task
    path, cost, wins = _G["path"], _G["cost"], _G["wins"]
    mtm = 1.0 + path[rows] - cost[rows][:, None]
    bydays = {}
    for j in range(len(rows)):
        d = int(tt[j]) + 1
        bydays.setdefault(d, []).append((d, int(tt[j]), int(symc[j]), int(free[j]), float(mult[j]), mtm[j].tolist()))
    days = sorted(bydays)
    return np.array([_sim(days, bydays, s, e) for s, e in wins])


def stat(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) == 0:
        return dict(n=0, mean=np.nan, med=np.nan, win=np.nan, g10=np.nan, g50=np.nan, worst=np.nan)
    return dict(n=len(x), mean=x.mean(), med=np.median(x), win=(x > 0).mean(), g10=(x > .10).mean(), g50=(x > .50).mean(), worst=x.min())


def fs(d):
    if d["n"] == 0:
        return "n=0"
    return (f"n={d['n']} mean={d['mean']*100:.2f}% med={d['med']*100:.2f}% win={d['win']*100:.1f}% "
            f">10%={d['g10']*100:.1f}% >50%={d['g50']*100:.2f}% worst={d['worst']*100:.1f}%")


def main():
    OUTP.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(ROOT / "data" / "daily_table.parquet")
    df["year"] = df["year"].astype(str)
    df = df.sort_values(["symbol", "session_idx"]).reset_index(drop=True)
    N = len(df)
    P(f"table rows {N}, symbols {df.symbol.nunique()}, dates {df.date.min().date()} to {df.date.max().date()}")
    sym = pd.factorize(df.symbol)[0].astype(np.int32)
    nsym = sym.max() + 1
    idx = df.session_idx.values.astype(np.int64)
    date = df.date.values
    dts = pd.DatetimeIndex(df.date)
    f = lambda c: df[c].values.astype(np.float64)
    ret1, ret3, ret5 = f("ret_1d"), f("ret_3d"), f("ret_5d")
    tv = f("traded_value_median_60")
    vr1 = f("vol_ratio_1_20")
    rf1 = f("ret_fwd_1")
    nopen = f("next_open")

    # session -> date
    sd = df.drop_duplicates("session_idx").set_index("session_idx").date.reindex(range(NS))
    sess_date = pd.DatetimeIndex(sd.values)
    s0 = int(idx.min())

    # ---- dense adjusted level and helpers
    x = df.ret_1d.fillna(0).astype(np.float64)
    L = (1 + x).groupby(sym).cumprod().values
    Ld = np.full((nsym, NS + PAD), np.nan)
    Ld[sym, idx] = L
    Ld = pd.DataFrame(Ld.T).ffill().values.T            # ffilled from the first trade on (last print held after the last trade)
    Gd = np.full((nsym, NS + PAD), np.nan)
    Gd[sym, idx] = f("gap_open")
    NO = np.full((nsym, NS + PAD), np.nan)
    NO[sym, idx] = nopen
    Ud = np.zeros((nsym, NS + PAD))
    Ud[sym, idx] = df.upper_lock.values.astype(float)

    # ---- forward close path relative to next_open, sessions t+1..t+20
    path = np.full((N, 20), np.nan)
    L1 = Ld[sym, np.minimum(idx + 1, NS + PAD - 1)]
    for k in range(1, 21):
        j = idx + k
        ok = j <= NS - 1
        v = np.where(ok, Ld[sym, np.minimum(j, NS + PAD - 1)] / L1, np.nan)
        path[:, k - 1] = (1 + rf1) * v - 1
    # validation against the table
    for k, c in [(2, "ret_fwd_2"), (3, "ret_fwd_3"), (5, "ret_fwd_5"), (10, "ret_fwd_10"), (20, "ret_fwd_20")]:
        a, b = path[:, k - 1], f(c)
        m = ~np.isnan(a) & ~np.isnan(b)
        dif = np.abs(a[m] - b[m])
        P(f"path check k={k}: compared {m.sum()}, max abs diff {dif.max():.5f}, share > 0.5pp {np.mean(dif > .005)*100:.3f}%")

    # ---- validity: trades, fillable
    era = np.where(sess_date <= pd.Timestamp("2020-03-27"), .05, np.where(sess_date <= pd.Timestamp("2024-07-05"), .075, .10))
    lim = np.concatenate([era, np.full(PAD, .10)])
    egap = Gd[sym, np.minimum(idx + 1, NS + PAD - 1)]
    unfill = egap >= 0.97 * lim[np.minimum(idx + 1, NS + PAD - 1)]
    has_fwd = ~np.isnan(rf1)
    sane = np.abs(ret1) <= 0.35
    # data breaks inside the 20-session forward path (|ret_1d| > 35% on a later traded day, e.g. unadjusted splits) invalidate the row
    Rd = np.zeros((nsym, NS + PAD))
    Rd[sym, idx] = (np.abs(np.nan_to_num(ret1)) > 0.35).astype(float)
    fb = pd.DataFrame(Rd.T)[::-1].rolling(20, min_periods=1).sum()[::-1].shift(-1).values   # breaks in t+1..t+20
    fbreak = fb[idx, sym] > 0
    valid = has_fwd & sane & ~unfill & ~fbreak
    P(f"rows dropped for a data break inside the forward 20 sessions: {np.sum(has_fwd & sane & ~unfill & fbreak)}")
    P(f"rows with next-session trade {has_fwd.sum()}, unfillable (entry opens at limit up) {np.sum(has_fwd & unfill)}, sane {sane.sum()}")

    # ---- tiers and costs
    tier = np.where(tv >= 20e6, 0, np.where(tv >= 5e6, 1, np.where(tv >= 1e6, 2, 3)))
    cost = np.where(tier == 0, .005, .010)
    liquid = tv > 5e6
    u1 = tv >= 1e6

    # ---- exits (gross)
    mfe1, mfe3, mfe5 = f("mfe_1"), f("mfe_3"), f("mfe_5")
    nanp = np.isnan(path)
    ex = {}

    def put(name, ret, off, resolved):
        ex[name] = (np.where(resolved, ret, np.nan), np.where(resolved, off, 9999).astype(np.int64))

    put("close1", path[:, 0], 1, ~nanp[:, 0])
    h1, h3 = mfe1 >= .05, (mfe3 >= .05) | (mfe1 >= .05)
    put("tgt5_3", np.where(h3, .05, path[:, 2]), np.where(h1, 1, 3), h3 | ~nanp[:, 2])
    h1, h3, h5 = mfe1 >= .10, (mfe3 >= .10) | (mfe1 >= .10), (mfe5 >= .10) | (mfe3 >= .10) | (mfe1 >= .10)
    put("tgt10_5", np.where(h5, .10, path[:, 4]), np.where(h1, 1, np.where(h3, 3, 5)), h5 | ~nanp[:, 4])
    o = f("first_upper_lock_within_5")
    has = ~np.isnan(o) & (o >= 1)
    oi = np.where(has, o, 1).astype(int) - 1
    put("lock5", np.where(has, path[np.arange(N), oi], path[:, 4]), np.where(has, o, 5), has | ~nanp[:, 4])
    o = f("first_red_day")
    has = ~np.isnan(o) & (o >= 1) & (o <= 20)
    oi = np.where(has, o, 1).astype(int) - 1
    put("red20", np.where(has, path[np.arange(N), oi], path[:, 19]), np.where(has, o, 20), has | ~nanp[:, 19])
    v = 1 + path
    pk = np.fmax.accumulate(np.concatenate([np.ones((N, 1)), v], axis=1), axis=1)[:, 1:]
    trig = np.zeros((N, 20), bool)
    with np.errstate(invalid="ignore"):
        trig = v <= 0.8 * pk
    anyt = trig.any(1)
    kt = trig.argmax(1)
    put("trail20", np.where(anyt, v[np.arange(N), kt] - 1, path[:, 19]), np.where(anyt, kt + 1, 20), anyt | ~nanp[:, 19])
    nx = NO[sym, np.minimum(idx + 1, NS + PAD - 1)]
    r2 = nx / nopen - 1
    put("open2", r2, 1, ~np.isnan(r2))
    P("exit sanity (all valid rows, gross, no costs): " + "; ".join(
        f"{k}: n={np.sum(valid & ~np.isnan(ex[k][0]))} mean={np.nanmean(np.where(valid, ex[k][0], np.nan))*100:.2f}%" for k in ex))

    # ---- dense rolling features
    Ldf = pd.DataFrame(Ld.T)
    mx20 = Ldf.rolling(20, min_periods=20).max().shift(1).values
    mn20 = Ldf.rolling(20, min_periods=20).min().shift(1).values
    Udf = pd.DataFrame(Ud.T)
    lk20 = Udf.rolling(20, min_periods=1).sum().shift(1).values
    gi = lambda M: M[idx, sym]
    mx, mn, lk = gi(mx20), gi(mn20), gi(lk20)
    prevL = Ld[sym, idx - 1]
    ul = df.upper_lock.values
    ll = df.lower_lock.values
    U1 = Ud[sym, idx - 1] > 0
    U2 = Ud[sym, idx - 2] > 0

    # ---- rules
    sig = {}
    day = idx

    def topk(mask, key, k):
        m = np.flatnonzero(mask)
        t = pd.DataFrame({"d": day[m], "k": key[m], "i": m})
        t["r"] = t.groupby("d")["k"].rank(method="first", ascending=False)
        out = np.zeros(N, bool)
        out[t.i[t.r <= k].values] = True
        return out

    base = sane & ~np.isnan(ret1)
    L5 = base & liquid
    sig["R1a"] = topk(L5, ret1, 1)
    sig["R1b"] = topk(L5 & ~ul, ret1, 1)
    sig["R1c"] = topk(base & (tv >= 20e6), ret1, 1)
    sig["R2a"] = topk(L5, ret1, 3)
    sig["R2b"] = topk(L5 & ~ul, ret1, 3)
    b = base & u1
    r3 = b & ul & (lk == 0) & ((mx / mn - 1) < .15)
    sig["R3a"] = r3
    sig["R3b"] = r3 & (vr1 >= 2)
    sig["R4"] = b & ul & (U1 | U2)
    cud = f("consecutive_up_days")
    for k_ in (3, 4, 5):
        sig[f"R5{'abc'[k_-3]}"] = b & (cud == k_)
    gap = b & (f("gap_open") > .03) & (vr1 >= 2)
    sig["R6a"] = gap & (f("f_financial_result") > 0)
    sig["R6b"] = gap & (f("f_material_info") > 0)
    sig["R6c"] = gap & (f("f_dividend_or_bonus") > 0)
    sig["R6d"] = gap & (f("f_total") > 0)
    sig["R7"] = gap & (f("f_total") == 0)
    sig["R8a"] = b & (ret1 >= .05) & (f("f_financial_result") > 0)
    sig["R8b"] = b & (ret1 >= .05) & (f("f_financial_result") == 0)
    sig["R9"] = b & (ret1 <= -.05) & (prevL / mx >= .95)
    ix1 = f("index_ret_1d")
    d3 = ix1 <= -.03
    sig["R10"] = topk(L5 & d3, ret1, 3)
    sig["R11a"] = topk(L5 & d3, -ret1, 3)
    sig["R11b"] = topk(L5 & d3 & ~ll, -ret1, 3)
    # R12 sympathy lag
    m = np.flatnonzero(L5 & (df.sector.values != "other"))
    t = pd.DataFrame({"d": day[m], "s": df.sector.values[m], "r": ret1[m], "i": m})
    t["rk"] = t.groupby(["d", "s"])["r"].rank(method="first", ascending=False)
    t1 = t.r.where(t.rk == 1).groupby([t.d, t.s]).transform("max")
    t2 = t.r.where(t.rk == 2).groupby([t.d, t.s]).transform("max")
    oth = np.where(t.rk == 1, t2, t1)
    ok12 = (oth >= .07) & (t.r < .02) & (t.r > -.05)
    s12 = np.zeros(N, bool)
    s12[t.i[ok12].values] = True
    sig["R12"] = s12
    dsl = np.nan_to_num(f("days_since_last_filing"), nan=1e9)
    sr5 = f("sector_ret_5d")
    ix5 = f("index_ret_5d")
    secok = np.where(np.isnan(sr5), ix5, sr5) < .03
    for nm, cond in [("a", (ret5 > .08) & (dsl > 10)), ("b", (ret5 > .08) & (dsl > 5)), ("c", (ret5 > .12) & (dsl > 20))]:
        sig[f"R13{nm}"] = b & cond & secok
        sig[f"R13{nm}_ns"] = b & cond
    sig["R14"] = b & df.next_board_meeting_known.values & (ret5 > .05)
    sig["R15"] = b & (f("f_financial_result") > 0) & (ret1 >= .03)
    fri = (dts.dayofweek == 4)
    sig["R16"] = topk(L5 & fri & (ix1 <= -.02), tv, 3)
    d252 = f("dist_252_high")
    sig["R17a"] = b & (d252 >= -1e-6)
    sig["R17b"] = sig["R17a"] & (vr1 >= 2)
    sig["R18a"] = b & (d252 <= -.20) & (cud == 3)
    sig["R18b"] = sig["R18a"] & (vr1 >= 2)
    sig["R19"] = b & (ret1 >= .05) & (vr1 >= 3)
    sig["R20"] = b & (ret1 <= -.05) & (vr1 >= 3)
    sig["R21"] = b & ll
    sig["R22"] = b & (ret3 <= -.10)
    rules = list(sig)
    assert len(rules) == 40, len(rules)
    chk = (sig["R13a"] & valid).sum(), df.is_newsless_rise.values.sum()
    P(f"R13a rows (all, with sector filter, u1 universe) vs table is_newsless_rise rows: {sig['R13a'].sum()} vs {chk[1]} (table has no liquidity floor)")

    # ---- placebo machinery per exit
    key = idx * 4 + tier
    K = (NS + PAD) * 4
    ep_new_all = np.ones(N, bool)
    reg = df.regime.values
    kmi = df.kmi_member.fillna(False).astype(bool).values
    isIS = dts <= IS_END
    isOOS = dts >= OOS_START
    h1 = dts <= pd.Timestamp("2021-12-31")
    exstate = {}
    for e in ex:
        g, off = ex[e]
        net = g - cost
        pool = valid & ~np.isnan(net)
        cnt = np.bincount(key[pool], minlength=K)
        sm = np.bincount(key[pool], weights=net[pool], minlength=K)
        pe = np.where(cnt[key] > 0, sm[key] / np.maximum(cnt[key], 1), np.nan)
        pidx = np.flatnonzero(pool)
        order = np.argsort(key[pidx], kind="stable")
        sorted_net = net[pidx][order]
        start = np.cumsum(cnt) - cnt
        exstate[e] = (net, pool, pe, sorted_net, start, cnt)

    rows_out = []
    pvals = {}
    tests = {}
    sym_np = sym
    for rname in rules:
        for e in EXITS + (["open2"] if rname in ("R1a", "R1b", "R1c", "R2a", "R2b") else []):
            net, pool, pe, sorted_net, start, cnt = exstate[e]
            s_all = sig[rname] & pool
            ii = np.flatnonzero(s_all)
            if len(ii) == 0:
                continue
            new = np.ones(len(ii), bool)
            new[1:] = (sym[ii][1:] != sym[ii][:-1]) | (idx[ii][1:] - idx[ii][:-1] > 10)
            epi = np.zeros(N, bool)
            epi[ii[new]] = True
            r = {"rule": rname, "exit": e}

            def sub(mask, tag):
                mm = s_all & mask
                d = stat(net[mm])
                r[tag] = d
                r[tag + "_exc"] = np.nanmean(net[mm] - pe[mm]) if mm.sum() else np.nan
                r[tag + "_gross"] = np.nanmean((net + cost)[mm]) if mm.sum() else np.nan
                return mm

            mIS = sub(isIS, "IS")
            sub(isOOS, "OOS")
            sub(isIS & (reg == "bill>policy"), "IS_billgt")
            sub(isIS & (reg == "bill<=policy"), "IS_billle")
            sub(isIS & h1, "IS_H1")
            sub(isIS & ~h1, "IS_H2")
            for t_, nm in [(0, "t20m"), (1, "t5_20m"), (2, "t1_5m")]:
                sub(isIS & (tier == t_), nm)
            sub(isIS & kmi, "IS_kmi")
            r["ep"] = int((epi & isIS).sum())
            r["dates"] = len(np.unique(idx[mIS]))
            # placebo
            fi = np.flatnonzero(epi & isIS)
            obs = net[fi].mean() if len(fi) else np.nan
            if len(fi):
                k_ = key[fi]
                u = RNG.random((D_PLC, len(fi)))
                pos = start[k_] + (u * cnt[k_]).astype(np.int64)
                dm = sorted_net[pos].mean(1)
                p = (1 + np.sum(dm >= obs)) / (D_PLC + 1)
                r["p"] = p
                r["ep_first_mean"] = obs
                r["plc_ep_mean"] = dm.mean()
            else:
                r["p"] = np.nan
            ia = np.flatnonzero(mIS)
            if len(ia):
                k_ = key[ia]
                u = RNG.random((5, len(ia)))
                pos = start[k_] + (u * cnt[k_]).astype(np.int64)
                r["PLC"] = stat(sorted_net[pos].ravel())
            else:
                r["PLC"] = stat([])
            rows_out.append(r)
            if e != "open2":
                tests[(rname, e)] = r

    P("")
    P("=" * 100)
    P("RESULTS BY RULE AND EXIT (net of costs, IS = signal date <= 2026-08-31). exc = mean net minus exact expected placebo mean (same date, same tier)")
    for r in rows_out:
        P(f"[{r['rule']} {r['exit']}] ep={r['ep']} dates={r['dates']} IS: {fs(r['IS'])} | gross mean {r['IS_gross']*100:.2f}% exc {r['IS_exc']*100:+.2f}% p={r['p']:.3f}"
          f" | placebo {fs(r['PLC'])}")
        P(f"    OOS: {fs(r['OOS'])} exc {r['OOS_exc']*100:+.2f}%")
        P(f"    regime bill>policy: {fs(r['IS_billgt'])} exc {r['IS_billgt_exc']*100:+.2f}% | bill<=policy: {fs(r['IS_billle'])} exc {r['IS_billle_exc']*100:+.2f}%")
        P(f"    halves H1(<=2021): {fs(r['IS_H1'])} exc {r['IS_H1_exc']*100:+.2f}% | H2: {fs(r['IS_H2'])} exc {r['IS_H2_exc']*100:+.2f}%")
        P(f"    tier >=20m: {fs(r['t20m'])} | 5-20m: {fs(r['t5_20m'])} | 1-5m: {fs(r['t1_5m'])} | KMI members: {fs(r['IS_kmi'])}")

    # ---- results csv
    flat = []
    for r in rows_out:
        d = {"rule": r["rule"], "exit": r["exit"], "ep": r["ep"], "dates": r["dates"], "p": r["p"]}
        for tag in ["IS", "OOS", "IS_billgt", "IS_billle", "IS_H1", "IS_H2", "t20m", "t5_20m", "t1_5m", "IS_kmi", "PLC"]:
            for k_, v_ in r[tag].items():
                d[f"{tag}_{k_}"] = v_
            if tag + "_exc" in r:
                d[f"{tag}_exc"] = r[tag + "_exc"]
                d[f"{tag}_gross"] = r[tag + "_gross"]
        flat.append(d)
    pd.DataFrame(flat).to_csv(OUTP / "pattern_mining_daily_results.csv", index=False)

    # ---- multiple testing
    P("")
    P("=" * 100)
    P("MULTIPLE TESTING")
    keys = [k_ for k_ in tests if not np.isnan(tests[k_]["p"])]
    pv = np.array([tests[k_]["p"] for k_ in keys])
    nt = len(keys)
    P(f"tests with a defined p-value: {nt} (40 rules x 6 exits = 240 pre-registered)")
    for a in (0.05, 0.01, 0.005):
        P(f"  p <= {a}: {np.sum(pv <= a)} of {nt} (expected by chance if all null: {nt*a:.1f})")
    order = np.argsort(pv)
    bh = np.zeros(nt, bool)
    thr = 0
    for rank_, j in enumerate(order, 1):
        if pv[j] <= 0.10 * rank_ / nt:
            thr = rank_
    bh[order[:thr]] = True
    P(f"  Benjamini-Hochberg q=10%: {bh.sum()} tests pass")
    rp = {}
    for k_, p_ in zip(keys, pv):
        rp.setdefault(k_[0], []).append(p_)
    for a in (0.05, 0.01):
        nr = sum(1 for v_ in rp.values() if min(v_) <= a)
        P(f"  rules with at least one exit at p <= {a}: {nr} of {len(rp)}; expected by chance if exits independent {len(rp)*(1-(1-a)**6):.1f}, if perfectly correlated {len(rp)*a:.1f}")
    # direction: p is one-sided for the mean being HIGHER than placebo; also count the other tail
    P(f"  p >= 0.99 (rules WORSE than random entries): {np.sum(pv >= 0.99)} of {nt}")

    # ---- survivors
    P("")
    P("SURVIVOR SCREEN (S1 IS ep>=100, mean>0, excess>0, p<=.01; S2 both regimes mean>0 & excess>0; S3 both halves; S4 OOS n>=10 mean>0 excess>0)")
    surv, untested, s1only = [], [], []
    for k_ in keys:
        r = tests[k_]

        def pos_(tag, nmin=1):
            return r[tag]["n"] >= nmin and r[tag]["mean"] > 0 and r[tag + "_exc"] > 0
        S1 = r["ep"] >= 100 and pos_("IS") and r["p"] <= 0.01
        S2 = pos_("IS_billgt") and pos_("IS_billle")
        S3 = pos_("IS_H1") and pos_("IS_H2")
        n_oos = r["OOS"]["n"]
        S4 = pos_("OOS", 10)
        r["S"] = (S1, S2, S3, S4)
        if S1:
            s1only.append(k_)
        if S1 and S2 and S3:
            (surv if S4 else untested).append(k_)
    P(f"pass S1: {len(s1only)}; S1+S2+S3: {len(surv)+len(untested)}; plus S4: {len(surv)}")
    for k_ in s1only:
        r = tests[k_]
        P(f"  S1 pass {k_} S={r['S']} ep={r['ep']} IS {fs(r['IS'])} exc {r['IS_exc']*100:+.2f}% p={r['p']:.3f} | OOS {fs(r['OOS'])} | regimes {r['IS_billgt']['mean']*100:+.2f}% / {r['IS_billle']['mean']*100:+.2f}% | halves {r['IS_H1']['mean']*100:+.2f}% / {r['IS_H2']['mean']*100:+.2f}%")
    P("SURVIVORS: " + (", ".join(f"{a}/{b}" for a, b in surv) if surv else "none"))
    P("S1-S3 but OOS n<10 or OOS not positive: " + (", ".join(f"{a}/{b}" for a, b in untested) if untested else "none"))
    # top by excess (descriptive, not a test)
    P("")
    P("Top 15 rule/exit by IS excess over placebo with ep>=100 (descriptive)")
    cand = sorted([k_ for k_ in keys if tests[k_]["ep"] >= 100], key=lambda k_: -tests[k_]["IS_exc"])[:15]
    for k_ in cand:
        r = tests[k_]
        P(f"  {k_} ep={r['ep']} IS mean {r['IS']['mean']*100:+.2f}% med {r['IS']['med']*100:+.2f}% exc {r['IS_exc']*100:+.2f}% p={r['p']:.3f} OOS n={r['OOS']['n']} mean {r['OOS']['mean']*100:+.2f}%  S={r['S']}")

    # ---- books
    P("")
    P("=" * 100)
    P("BOOKS: Rs50,000 fully reinvested, up to 3 positions, vol_ratio_1_20 order; 30-session rolling windows")
    s_roll = list(range(s0, NS - 29))
    wins = [(s, s + 29) for s in s_roll]
    swa = (int(np.searchsorted(sess_date.values, np.datetime64("2026-08-14"))), int(np.searchsorted(sess_date.values, np.datetime64("2026-09-15"), side="right") - 1))
    swb = (int(np.searchsorted(sess_date.values, np.datetime64("2026-09-16"))), int(np.searchsorted(sess_date.values, np.datetime64("2026-10-16"), side="right") - 1))
    wins += [swa, swb]
    P(f"windows: {len(s_roll)} rolling 30-session windows, first start {sess_date[s0].date()}, last end {sess_date[NS-1].date()}; special windows idx {swa} ({sess_date[swa[0]].date()}..{sess_date[swa[1]].date()}, {swa[1]-swa[0]+1} sessions) and {swb} ({sess_date[swb[0]].date()}..{sess_date[swb[1]].date()}, {swb[1]-swb[0]+1} sessions)")

    def mk(selmask, e, order_key, rand=False):
        g, off = ex[e]
        net = g - cost
        mult = np.where(np.isnan(net), 1.0, 1 + net)
        free = np.where(off >= 9999, 9999, idx + off)
        ii = np.flatnonzero(selmask & valid & ~np.isnan(path[:, 0]))
        t = pd.DataFrame({"d": idx[ii], "k": order_key[ii], "i": ii})
        t["r"] = t.groupby("d")["k"].rank(method="first", ascending=False)
        t = t[t.r <= 6].sort_values(["d", "r"])
        ii = t.i.values
        return (ii, idx[ii], sym[ii], free[ii], mult[ii])

    tasks, tnames = [], []
    for rname in rules:
        for e in EXITS:
            tasks.append(mk(sig[rname], e, np.nan_to_num(vr1, nan=0.0)))
            tnames.append((rname, e))
    ntask_real = len(tasks)
    pl_names = []
    for e in EXITS:
        for seed in range(5):
            rk = np.random.default_rng(1000 + seed).random(N)
            tasks.append(mk(liquid & (tier <= 1), e, rk))
            pl_names.append((e, seed))
    ctx = get_context("spawn")
    with ctx.Pool(7, initializer=_init, initargs=(path, cost, wins)) as pool_:
        res = pool_.map(run_task, tasks, chunksize=2)
    nr = len(s_roll)

    def dist(a):
        a = np.asarray(a)
        return dict(p10=np.percentile(a, 10), med=np.median(a), p90=np.percentile(a, 90), up=np.mean(a > 1), worst=a.min(), mean=a.mean(), best=a.max())

    plc = {}
    for (e, seed), r_ in zip(pl_names, res[ntask_real:]):
        plc.setdefault(e, []).append(r_)
    plcd = {}
    for e in EXITS:
        allw = np.array(plc[e])
        pooled = allw[:, :nr].ravel()
        plcd[e] = (dist(pooled), allw[:, nr].mean(), allw[:, nr + 1].mean())
        d = plcd[e][0]
        P(f"PLACEBO BOOK exit {e}: p10 {d['p10']:.3f} med {d['med']:.3f} p90 {d['p90']:.3f} share up {d['up']*100:.1f}% worst {d['worst']:.3f} best {d['best']:.2f} | window 14Aug-15Sep {plcd[e][1]:.3f} | 16Sep-16Oct {plcd[e][2]:.3f}")
    brow = []
    for (rname, e), r_ in zip(tnames, res[:ntask_real]):
        d = dist(r_[:nr])
        brow.append(dict(rule=rname, exit=e, act=float(np.mean(np.abs(r_[:nr] - 1) > 1e-12)), **d, w_aug=r_[nr], w_sep=r_[nr + 1], plc_med=plcd[e][0]["med"], plc_up=plcd[e][0]["up"], plc_p90=plcd[e][0]["p90"], plc_p10=plcd[e][0]["p10"], plc_aug=plcd[e][1], plc_sep=plcd[e][2]))
        P(f"BOOK [{rname} {e}] active {np.mean(np.abs(r_[:nr]-1)>1e-12)*100:.0f}% of windows; p10 {d['p10']:.3f} med {d['med']:.3f} p90 {d['p90']:.3f} up {d['up']*100:.1f}% worst {d['worst']:.3f} best {d['best']:.2f} mean {d['mean']:.3f} | 14Aug-15Sep {r_[nr]:.3f} 16Sep-16Oct {r_[nr+1]:.3f} | placebo med {plcd[e][0]['med']:.3f} up {plcd[e][0]['up']*100:.1f}%")
    bd = pd.DataFrame(brow)
    bd.to_csv(OUTP / "pattern_mining_daily_books.csv", index=False)
    P("")
    P("Top 12 books by median (books holding a position in at least half of windows)")
    for _, r in bd[bd.act >= .5].sort_values("med", ascending=False).head(12).iterrows():
        P(f"  {r.rule} {r.exit} p10 {r.p10:.3f} med {r.med:.3f} p90 {r.p90:.3f} up {r.up*100:.1f}% worst {r.worst:.3f} | Aug-Sep {r.w_aug:.3f} Sep-Oct {r.w_sep:.3f} | placebo med {r.plc_med:.3f}")
    P("Top 12 books by share of windows up")
    for _, r in bd[bd.act >= .5].sort_values("up", ascending=False).head(12).iterrows():
        P(f"  {r.rule} {r.exit} p10 {r.p10:.3f} med {r.med:.3f} p90 {r.p90:.3f} up {r.up*100:.1f}% worst {r.worst:.3f} | Aug-Sep {r.w_aug:.3f} Sep-Oct {r.w_sep:.3f} | placebo med {r.plc_med:.3f}")
    P("Top 12 books by p10")
    for _, r in bd[bd.act >= .5].sort_values("p10", ascending=False).head(12).iterrows():
        P(f"  {r.rule} {r.exit} p10 {r.p10:.3f} med {r.med:.3f} p90 {r.p90:.3f} up {r.up*100:.1f}% worst {r.worst:.3f} | Aug-Sep {r.w_aug:.3f} Sep-Oct {r.w_sep:.3f} | placebo med {r.plc_med:.3f}")
    for k_ in (surv + untested):
        r = bd[(bd.rule == k_[0]) & (bd.exit == k_[1])].iloc[0]
        P(f"  screened rule {k_}: p10 {r.p10:.3f} med {r.med:.3f} p90 {r.p90:.3f} up {r.up*100:.1f}% worst {r.worst:.3f} | Aug-Sep {r.w_aug:.3f} Sep-Oct {r.w_sep:.3f} | placebo med {r.plc_med:.3f}")
    (OUTP / "pattern_mining_daily.txt").write_text("\n".join(OUT), encoding="utf-8")


if __name__ == "__main__":
    main()
