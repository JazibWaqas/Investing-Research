"""winners_2026_postmortem: why a 252-high breakout system (S3) did not hold MACFL QUICE PRL CRTM JVDC TPLT in Oct 2025 - Oct 2026, and six pre-registered fixes.
Run: .venv/Scripts/python.exe scripts/tests/winners_2026_postmortem.py [part1|part2|part3|all]   -> tests/out/winners_2026_postmortem_partN.txt
Machinery: the oracle script's source is executed up to its run section (panel, universe, HI252, Sim, windows), with the adjusted panel rebuilt with
dividends at 85% as in rs50k_last_year.py. Write-up: tests/winners_2026_postmortem.md.

PRE-REGISTRATION (written before any variant was run; tests/winners_2026_postmortem.md repeats it). Baseline S3: close above the prior 252-session high, 20% trailing
stop on closes, max 3 positions of 1/3 equity, liquid = trailing 60-session median traded value above Rs5m, KMI members only in windows from 2020-10, signals ranked by
close / prior 252-high, signal at close t and trade at close t+1, costs 0.25%/side (+0.25% under Rs20m).
 F1 rotation: universe liquid (and KMI); eligible = close within 5% of its prior 252-session high (close >= 0.95 * prior high); rank eligible by 63-session return; hold the top 3,
    1/3 equity each, no stop. Reviewed on the last session of each month and on day 0: any holding that is not in the top 6 of the eligible list is sold and vacancies are filled from the top of the list.
 F2 no cap: entries are names that closed above their prior 252-high on any session of the last 5; evaluated every 5th session; 20% trailing stop on closes; weight min(1/n, 1/3) of equity each
    (n = names held), rebalanced every 5th session (trims and top-ups only when the weight is off by more than 10%).
 F3 S3 with a 30% trailing stop.
 F4 S3 with liquidity threshold Rs2m (same 60-session median) and position size capped at 2% of the mean traded value of the last 20 sessions. F4s: same, with 1.5%/side cost on names under Rs5m (stress).
 F5 S3 plus one add of a further 1/3 of equity (limited by cash) when a holding closes at a new high since entry and at least 10% above its entry price.
 F6 = F1 + F3 + F4: rotation as F1 with a 30% trailing stop (vacancies from stops are filled at the next monthly review), Rs2m threshold, 2% of 20-day traded value size cap.
 Placebos (100 draws each): P_bo = breakout timing and slot count of S3 (resp. F3) kept, the names chosen at random from the liquid universe, same stop. P_rot = F1 (resp. F6) with
    the 3 names drawn at random from the eligible (within-5%-of-high) list at each month end, same stop and costs, full turnover.
Windows: the 1-year window 2025-10-16 to 2026-10-16 (already seen: the six winners were known) and the five 2-year windows of the oracle test. The 2024-10 window overlaps the seen year by
 about 12 months, so it is not independent of it. Six variants x six windows = 36 comparisons: read any single win with that in mind (Bonferroni 5% threshold = p < 0.0083).
"""
import sys, io, os, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np, pandas as pd

PARTS = set(sys.argv[1:] or ["all"]); sys.argv = [sys.argv[0]]
run = lambda p: "all" in PARTS or p in PARTS
SIX = ["MACFL", "QUICE", "PRL", "CRTM", "JVDC", "TPLT"]
D0, D1 = "2025-10-16", "2026-10-16"
START = 50000.0

src = (ROOT / "scripts/tests/oracle_and_good_case.py").read_text(encoding="utf-8")
head = src[:src.index("# ===================================================================== run")]
old = 'adj = pd.read_parquet(ROOT / "data" / ("panel_close_adj_pricereturn.parquet" if PR else "panel_close_adj.parquet")).reindex(index=dates, columns=cols)'
new = '''_a = P.load_actions(); _a.loc[_a.type == "cash", "value"] *= 0.85
_tri = (1 + P.returns(raw, "adjusted", actions=_a).fillna(0)).cumprod()
adj = _tri.where(raw.notna()); adj = adj * (raw.ffill().iloc[-1] / adj.ffill().iloc[-1])'''
assert old in head
O = {"__name__": "oracle", "__file__": str(ROOT / "scripts/tests/oracle_and_good_case.py")}
exec(compile(head.replace(old, new), "oracle", "exec"), O)
dates, N, cols, PX, TRADED, MTV, cidx, LIQ, HI252, RET63 = (O[k] for k in ("dates", "N", "cols", "PX", "TRADED", "MTV", "cidx", "LIQ", "HI252", "RET63"))
Sim, universe, side, SECI, KM, WINS = O["Sim"], O["universe"], O["side"], O["SECI"], O["KM"], O["WINS"]
tvdf = O["tv"]; TV20 = tvdf.rolling(20, min_periods=15).mean().values          # mean traded value of the 20 sessions ending at t
i0 = int(dates.searchsorted(pd.Timestamp(D0))); i1 = N - 1
assert dates[i0] == pd.Timestamp(D0) and dates[i1] == pd.Timestamp(D1)
W1 = dict(name="2025-10-16", i0=i0, i1=i1, kmi=True)
L = []
def out(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
def D(i): return str(dates[i].date())
def mdd(v): v = np.asarray(v); return float((v / np.maximum.accumulate(v) - 1).min())
def tier(m): return "-" if not np.isfinite(m) else "H" if m > 20e6 else "M" if m > 5e6 else "L" if m > 2e6 else "XL"
def first(mask):
    w = np.flatnonzero(mask); return int(w[0]) if len(w) else None
def flush(tag):
    (ROOT / f"tests/out/winners_2026_postmortem_{tag}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
dt = pd.read_parquet(ROOT / "data/daily_table.parquet", columns=["date", "symbol", "close", "ret_1d", "upper_lock", "locks_up_10d", "vol_ratio_1_20", "sector_ret_5d", "dist_252_high",
                                                              "traded_value_median_60", "session_idx", "kmi_member"])
dt = dt[(dt.symbol.isin(SIX)) & (dt.date >= D0)]
ann = pd.read_parquet(ROOT / "data/announcements.parquet")
ann["d"] = pd.to_datetime(ann.datetime, utc=True).dt.tz_convert("Asia/Karachi")
ann = ann[ann.symbol.isin(SIX) & (ann.d >= pd.Timestamp(D0, tz="Asia/Karachi"))]

# ======================================================================================== PART 1
INFO = {}
EV = {}
def part1():
    out("== PART 1. Six names, 16 Oct 2025 - 16 Oct 2026. Adjusted (total return) closes, 1.00 = close of 2025-10-16 ==")
    me = [int(dates.searchsorted(m.end_time, side="right")) - 1 for m in pd.period_range("2025-10", "2026-10", freq="M")]
    me[0] = i0; me[-1] = i1
    out("\n-- monthly close multiple (month end; first column 2025-10-16, last 2026-10-16) and trailing-60-session median traded value, Rs m (tier H>20m M 5-20m L 2-5m XL<2m)")
    out(f"{'':8}" + "".join(f"{dates[i].strftime('%y-%m'):>8}" for i in me))
    for s in SIX:
        c = cidx[s]; out(f"{s:<8}" + "".join(f"{PX[i, c] / PX[i0, c]:>8.2f}" for i in me))
        out(f"{'  tv m':<8}" + "".join(f"{MTV[i, c] / 1e6:>6.1f}{tier(MTV[i, c])[0].lower()} " for i in me))
    out("\n-- peak, base, liquidity")
    out(f"{'sym':<7}{'base date':<12}{'base x':>7} {'peak date':<12}{'peak x':>7}{'end x':>7}{'peak/base':>10}{'end/base':>9}{'peak->end':>10}{'sessions liquid(>5m)':>22}{'first >5m':>12}{'first >2m':>11}{'KMI member at end':>19}")
    for s in SIX:
        c = cidx[s]; x = PX[i0:i1 + 1, c]; pk = int(np.nanargmax(x)) + i0; bs = int(np.nanargmin(PX[i0:pk + 1, c])) + i0 if pk > i0 else i0
        liq = LIQ[i0:i1 + 1, c]; f5 = first(LIQ[i0:i1 + 1, c]); f2 = first(MTV[i0:i1 + 1, c] > 2e6)
        mem = O["memmask"](i1)[c]
        INFO[s] = dict(c=c, pk=pk, bs=bs)
        out(f"{s:<7}{D(bs):<12}{PX[bs, c] / PX[i0, c]:>7.2f} {D(pk):<12}{PX[pk, c] / PX[i0, c]:>7.2f}{PX[i1, c] / PX[i0, c]:>7.2f}{PX[pk, c] / PX[bs, c]:>10.2f}{PX[i1, c] / PX[bs, c]:>9.2f}{PX[i1, c] / PX[pk, c] - 1:>10.0%}"
            f"{liq.sum():>12} of {len(liq)}{(D(i0 + f5) if f5 is not None else 'never'):>12}{(D(i0 + f2) if f2 is not None else 'never'):>11}{str(mem):>19}")
    out("\n-- timeline of observable events (dates = session of the signal close)")
    for s in SIX:
        c = cidx[s]; g = dt[dt.symbol == s].set_index("date")
        if g.empty:                       # TPLT is in the price panel (seed) but not in the daily table: rebuild lock / volume flags from closes and volume (approximate)
            rs = O["raw"][s].dropna(); r1 = rs / rs.shift(1) - 1; vv = O["vol"][s].reindex(rs.index)
            g = pd.DataFrame({"upper_lock": r1 >= 0.0995, "vol_ratio_1_20": vv / vv.rolling(20).mean().shift(1)}, index=rs.index)
            g["locks_up_10d"] = g.upper_lock.astype(int).rolling(10, min_periods=1).sum(); g["sector_ret_5d"] = np.nan; g = g[g.index >= D0]
            out(f"   ({s} is not in the daily table; locks = close >= 9.95% over the previous close, volume ratio from the volume panel: approximate)")
        h = (PX[:, c] > HI252[:, c]) & TRADED[:, c]; h[:i0] = False
        f_hi = first(h[:i1 + 1]); ul = g.index[g.upper_lock.astype(bool)]; f_ul = ul[0] if len(ul) else None
        cl = g.index[g.locks_up_10d >= 3]; f_cl = cl[0] if len(cl) else None
        v3 = g.index[g.vol_ratio_1_20 >= 3]; f_v3 = v3[0] if len(v3) else None
        EV[s] = dict(hi=f_hi, ul=dates.get_loc(f_ul) if f_ul is not None else None, cl=dates.get_loc(f_cl) if f_cl is not None else None, v3=dates.get_loc(f_v3) if f_v3 is not None else None)
        INFO[s].update(EV[s]); INFO[s]["nlocks"] = int(g.upper_lock.sum())
        dd = lambda k: D(EV[s][k]) if EV[s][k] is not None else "never"
        out(f"{s:<7} first 252-high {dd('hi')} (x{PX[f_hi, c] / PX[i0, c]:.2f})  first upper lock {dd('ul')}  first 3-lock cluster (3 locks in 10 sessions) {dd('cl')}  "
            f"first volume >=3x 20d mean {dd('v3')}  upper-lock closes in year {int(g.upper_lock.sum())}  252-high closes in year {int(h.sum())}")
    out("\n-- sector peers vs the name over the move (base date -> peak date). Peers: same sector label, liquid at the peak, self excluded; EW median of price+dividend return; KMI All Share")
    for s in SIX:
        c = cidx[s]; bs, pk = INFO[s]["bs"], INFO[s]["pk"]
        pe = [k for k in range(len(cols)) if SECI[k] == SECI[c] and k != c and LIQ[pk, k] and np.isfinite(PX[bs, k]) and TRADED[pk, k]]
        r = np.array([PX[pk, k] / PX[bs, k] - 1 for k in pe]); kmi = KM.asof(dates[pk]) / KM.asof(dates[bs]) - 1
        sr = dt[(dt.symbol == s) & (dt.date == dates[EV[s]["hi"]])].sector_ret_5d
        srv = float(sr.iloc[0]) if len(sr) and pd.notna(sr.iloc[0]) else float("nan")
        out(f"{s:<7}{SECI[c]:<22} name {PX[pk, c] / PX[bs, c] - 1:+7.0%}  sector peers median {np.median(r) if len(r) else np.nan:+6.0%} (n={len(r)}, best {r.max() if len(r) else np.nan:+.0%})  KMI {kmi:+5.0%}   sector_ret_5d on first-high day {srv:+.1%}")
    out("\n-- share of the eventual gain still ahead at day k after each anchor (log gain from the close at day k to the peak / log gain base -> peak). peak/Pk and end/Pk = multiples from the day-k close")
    out(f"{'sym':<7}{'anchor':<8}{'date':<12}" + "".join(f"{'k=' + str(k):>22}" for k in (0, 5, 10, 20, 40)))
    out(f"{'':27}" + "".join(f"{'ahead  peak/Pk  end/Pk':>22}" for _ in range(5)))
    for s in SIX:
        c = cidx[s]; bs, pk = INFO[s]["bs"], INFO[s]["pk"]
        for nm in ("hi", "ul", "cl", "v3"):
            a = EV[s][nm]
            if a is None: out(f"{s:<7}{nm:<8}{'never':<12}"); continue
            cells = []
            for k in (0, 5, 10, 20, 40):
                j = min(a + k, i1)
                if j > pk: cells.append(f"{'past peak':>22}"); continue
                cells.append(f"{np.log(PX[pk, c] / PX[j, c]) / np.log(PX[pk, c] / PX[bs, c]):>8.0%}{PX[pk, c] / PX[j, c]:>7.2f}x{PX[i1, c] / PX[j, c]:>7.2f}x")
            out(f"{s:<7}{nm:<8}{D(a):<12}" + "".join(cells))
    out("   anchors: hi = first close above prior 252-high, ul = first upper-lock close, cl = first 3 locks in 10 sessions, v3 = first day volume >= 3x prior 20-day mean")
    out("\n-- filings in the window: financial_result and material_info (date Asia/Karachi, title)")
    for s in SIX:
        a = ann[(ann.symbol == s) & ann.klass.isin(["financial_result", "material_info"])].sort_values("d")
        out(f"{s}: results {int((a.klass == 'financial_result').sum())}, material_info {int((a.klass == 'material_info').sum())}; all classes {int((ann.symbol == s).sum())}")
        for r in a.itertuples(): out(f"   {r.d:%Y-%m-%d %H:%M} {r.klass:<17}{str(r.title)[:130]}")
    out("\n-- public events: what had the price already done when each cause became public? (event stamp Asia/Karachi; after 15:30 counts as the next session; base = the move's low; share = log gain base -> event close / log gain base -> peak)")
    EVS = [("MACFL", "2025-10-28 14:06", "Q1 FY26 results (EPS -0.33)"), ("MACFL", "2026-01-02 16:12", "Material Information (text not retrievable)"), ("MACFL", "2026-04-29 08:47", "Q3 results, EPS 1.83 vs 1.03 a year before"),
           ("MACFL", "2026-09-02 08:19", "FY26 results (EPS Q4 0.28)"), ("QUICE", "2025-10-28 14:33", "Q1 results, day of first 252-high and lock"), ("QUICE", "2026-05-15 14:55", "Board approves merger of Indus Fruit Products (375.8m new shares vs 109m existing)"),
           ("PRL", "2026-04-21 13:45", "Q3 results, EPS 15.78 vs -4.09"), ("PRL", "2026-07-21 12:00", "Cabinet approves amended refinery policy (Topline via web search, time assumed)"),
           ("PRL", "2026-09-25 08:00", "Material Information: Upgrade Agreement signed 24 Sep with the Government under the amended policy"),
           ("CRTM", "2026-04-29 13:03", "Q3 results (no material_info filed in the year)"), ("JVDC", "2026-02-27 08:00", "H1 results, EPS Q2 4.08 vs 0.82"),
           ("TPLT", "2026-03-24 12:24", "Material Information: early sukuk redemption"), ("TPLT", "2026-06-24 08:15", "Material Information: international investor interested in a majority stake")]
    out(f"{'sym':<7}{'event time':<17}{'session':<12}{'x base':>7}{'share of gain done':>19}{'event-day ret':>14}{'+5 ses':>8}{'+20 ses':>9}{'to peak':>9}  event")
    for s_, t_, what in EVS:
        c = cidx[s_]; ts = pd.Timestamp(t_); j = int(dates.searchsorted(ts.normalize())) + (1 if ts.hour * 60 + ts.minute >= 15 * 60 + 30 else 0); j = min(j, i1)
        bs, pk = INFO[s_]["bs"], INFO[s_]["pk"]; ok = pk > bs and bs <= j <= pk
        sh = f"{np.log(PX[j, c] / PX[bs, c]) / np.log(PX[pk, c] / PX[bs, c]):>18.0%}" if ok else f"{'n/a (outside base-peak)':>19}"
        out(f"{s_:<7}{t_:<17}{D(j):<12}{PX[j, c] / PX[bs, c]:>7.2f} {sh} {PX[j, c] / PX[j - 1, c] - 1:>13.1%}{PX[min(j + 5, i1), c] / PX[j, c] - 1:>8.0%}{PX[min(j + 20, i1), c] / PX[j, c] - 1:>9.0%}{PX[pk, c] / PX[j, c] - 1 if j <= pk else float('nan'):>9.0%}  {what}")
    out("\n-- engine analogues on the first-signal day (first 252-high close) and on the first upper-lock day")
    import engine
    E = engine.Engine()
    for s in SIX:
        for nm in ("hi", "ul"):
            a = EV[s][nm]
            if a is None or (nm == "ul" and EV[s]["ul"] == EV[s]["hi"]): continue
            m = E.d.index[(E.d.symbol == s) & (E.d.date == dates[a])]
            if len(m) == 0: out(f"{s} {D(a)}: no row in the table"); continue
            sig = E.signature(m[0]); rows, info, oc = E.run(sig)
            out(f"\n{s} {D(a)} ({nm}) signature: " + engine.sig_text(sig) + f"   analogues n5={info['n5']}, {engine.widen_text(info)}")
            for k in (5, 20, 60):
                h = oc["h"][k]
                out(f"   h={k}: " + ("none resolved" if h is None else f"n={h['n']} med {h['med']:+.1%} p25 {h['p25']:+.0%} p75 {h['p75']:+.0%} win {h['win']:.0%} >50% {h['gt50']:.0%} placebo {h['plc']:+.1%} net {h['net']:+.1%}"))

if run("part1"):
    part1(); flush("part1"); L.clear()

# ======================================================================================== runners
NH = (PX > HI252) & TRADED                                   # close above the prior 252-session high (any liquidity, any membership)
NH5 = pd.DataFrame(NH).rolling(5, min_periods=1).max().values.astype(bool)
def stress_side(c, i):
    m = MTV[i, c]
    return 0.0025 + (0.0125 if not (m >= 5e6) else 0.0025 if not (m >= 20e6) else 0.0)     # 1.5%/side under Rs5m, 0.5% Rs5-20m, 0.25% above

def uni(i, w, thr): return (MTV[i] > thr) & (O["memmask"](i) if w["kmi"] else True)

def finish(sim, i1):
    for c in list(sim.pos):
        if TRADED[i1, c]: sim.sell(c, 1.0, i1, "end_open")
        if c in sim.pos:
            p = sim.pos[c]; pro = p["sh"] * PX[i1, c] * (1 - side(c, i1)); sim.cash += pro; p["pro"] += pro
            sim.trades.append(dict(system=sim.name, window=sim.win, symbol=cols[c], entry=dates[p["ei"]], exit=dates[i1], reason="end_open", invested=p["inv"], proceeds=p["pro"],
                                   ret=p["pro"] / p["inv"] - 1, pnl=p["pro"] - p["inv"], part=p["part"])); del sim.pos[c]
    eq = np.array(sim.eq); eq[-1] = sim.cash
    return eq, pd.DataFrame(sim.trades)

def run_bo(w, stop=0.2, thr=5e6, maxpos=3, pyr=False, tvcap=False, stress=False, rng=None, log=None, name="S3"):
    """S3 family: breakout entries ranked by close / prior 252-high, trailing stop on closes, equal 1/3 units. rng -> placebo: same timing and count, random liquid names."""
    old_side = O["side"]
    if stress: O["side"] = stress_side
    try:
        i0_, i1_ = w["i0"], w["i1"]
        sim = Sim(i0_, name, w["name"]); pend_sell, pend_buy = {}, []
        for i in range(i0_, i1_ + 1):
            for c in list(pend_sell):
                if sim.sell(c, 1.0, i, pend_sell[c]): del pend_sell[c]
            keep = []
            for (c, fr, ex, cap, add) in pend_buy:
                if c in sim.pos and not add: continue
                if add and c not in sim.pos: continue
                amt = sim.value(i) * fr
                if cap is not None: amt = min(amt, cap)
                if sim.buy(c, amt, i): continue
                if ex > i: keep.append((c, fr, ex, cap, add))
            pend_buy = keep
            sim.eq.append(sim.value(i))
            if i == i1_: break
            u = uni(i, w, thr)
            for c, p in sim.pos.items():
                p["peak"] = max(p["peak"], PX[i, c])
                if PX[i, c] <= (1 - stop) * p["peak"]: pend_sell[c] = f"trail_stop_{int(stop * 100)}"
            free = maxpos - len([c for c in sim.pos if c not in pend_sell])
            cand = []
            if free > 0:
                cand = [int(c) for c in np.where(u & NH[i])[0] if int(c) not in sim.pos]
                cand.sort(key=lambda c: -PX[i, c] / HI252[i, c])
            if log is not None:
                held = [cols[c] for c in sim.pos]
                for s in SIX:
                    c = cidx[s]
                    if not NH[i, c]: continue
                    if c in sim.pos: st = "held"
                    elif not (MTV[i, c] > thr): st = f"liquidity: median traded value Rs{MTV[i, c] / 1e6:.1f}m"
                    elif w["kmi"] and not O["memmask"](i)[c]: st = "not a KMI All Share member"
                    elif free <= 0: st = "slots full: " + ",".join(held)
                    elif c in cand[:free]: st = "ORDER placed"
                    else: st = f"ranked {cand.index(c) + 1} of {len(cand)} for {free} free slot(s)"
                    log.append((i, s, st))
            if rng is not None and cand:
                pool = np.where(u & TRADED[i])[0]; pool = [int(c) for c in pool if int(c) not in sim.pos]
                k = min(free, len(cand), len(pool)); cand = [int(x) for x in rng.choice(pool, k, replace=False)] if k > 0 else []
            pend_buy = [(c, 1 / maxpos, i + 1, (0.02 * TV20[i, c]) if tvcap else None, False) for c in cand[:max(free, 0)]]
            if pyr:
                for c, p in sim.pos.items():
                    if not p.get("added") and c not in pend_sell and PX[i, c] >= 1.10 * p["ep"] and PX[i, c] >= p["peak"]:
                        pend_buy.append((c, 1 / maxpos, i + 1, None, True)); p["added"] = True
        return finish(sim, i1_)
    finally:
        O["side"] = old_side

def run_rot(w, stop=None, thr=5e6, tvcap=False, rng=None, name="F1"):
    """F1/F6: top 3 of names within 5% of their prior 252-high ranked by 63-session return; monthly review, drop out of top 6 -> sold; placebo draws 3 random eligible names each month."""
    i0_, i1_ = w["i0"], w["i1"]
    sim = Sim(i0_, name, w["name"]); pend_sell, pend_buy = {}, []
    for i in range(i0_, i1_ + 1):
        for c in list(pend_sell):
            if sim.sell(c, 1.0, i, pend_sell[c]): del pend_sell[c]
        keep = []
        for (c, fr, ex, cap) in pend_buy:
            if c in sim.pos: continue
            amt = min(sim.value(i) * fr, sim.cash)
            if cap is not None: amt = min(amt, cap)
            if sim.buy(c, amt, i): continue
            if ex > i: keep.append((c, fr, ex, cap))
        pend_buy = keep
        sim.eq.append(sim.value(i))
        if i == i1_: break
        if stop:
            for c, p in sim.pos.items():
                p["peak"] = max(p["peak"], PX[i, c])
                if PX[i, c] <= (1 - stop) * p["peak"] and c not in pend_sell: pend_sell[c] = f"trail_stop_{int(stop * 100)}"
        if i == i0_ or dates[i].month != dates[i + 1].month:
            u = uni(i, w, thr) & TRADED[i]
            el = np.where(u & (PX[i] >= 0.95 * HI252[i]) & np.isfinite(RET63[i]))[0]
            el = [int(c) for c in el[np.argsort(-RET63[i, el])]]
            if rng is not None:
                el = [int(x) for x in rng.permutation(el)]
            top3, top6 = el[:3], set(el[:6] if rng is None else el[:3])
            for c in list(sim.pos):
                if c not in top6 and c not in pend_sell: pend_sell[c] = "rotation"
            nfree = 3 - len([c for c in sim.pos if c not in pend_sell])
            pend_buy = [(c, 1 / 3, i + 6, (0.02 * TV20[i, c]) if tvcap else None) for c in top3 if c not in sim.pos][:max(nfree, 0)]
    return finish(sim, i1_)

def run_ew(w, stop=0.2, thr=5e6, name="F2"):
    """F2: no position cap. Weekly: add names that closed above their prior 252-high in the last 5 sessions; equal weight min(1/n, 1/3); 20% trailing stop."""
    i0_, i1_ = w["i0"], w["i1"]
    sim = Sim(i0_, name, w["name"]); pend_sell, pend_buy, pend_trim = {}, [], []
    for i in range(i0_, i1_ + 1):
        for c in list(pend_sell):
            if sim.sell(c, 1.0, i, pend_sell[c]): del pend_sell[c]
        for c, fr in pend_trim:
            if c in sim.pos: sim.sell(c, fr, i, "trim")
        for c, amt in pend_buy:
            sim.buy(c, amt, i)
        pend_buy, pend_trim = [], []
        sim.eq.append(sim.value(i))
        if i == i1_: break
        for c, p in sim.pos.items():
            p["peak"] = max(p["peak"], PX[i, c])
            if PX[i, c] <= (1 - stop) * p["peak"]: pend_sell[c] = f"trail_stop_{int(stop * 100)}"
        if (i - i0_) % 5 == 0:
            u = uni(i, w, thr) & TRADED[i]
            tg = sorted(set(c for c in sim.pos if c not in pend_sell) | set(int(c) for c in np.where(u & NH5[i])[0] if int(c) not in pend_sell))
            if tg:
                E_ = sim.value(i); t = E_ * min(1 / len(tg), 1 / 3)
                for c in tg:
                    v = sim.pos[c]["sh"] * PX[i, c] if c in sim.pos else 0.0
                    if v > 1.1 * t: pend_trim.append((c, (v - t) / v))
                    elif v < 0.9 * t: pend_buy.append((c, t - v))
    return finish(sim, i1_)

def stats(eq, tr):
    return dict(mult=eq[-1] / START, dd=mdd(eq), n=len(tr), hit=(tr.ret > 0).mean() if len(tr) else np.nan, med=tr.ret.median() if len(tr) else np.nan)

# ======================================================================================== PART 2
def part2():
    w = W1
    log = []
    eq, tr = run_bo(w, log=log)
    eq0, tr0 = O["run"]("S3", w, i0, i1, True)
    assert abs(eq[-1] - eq0[-1]) < 1e-6 and len(tr) == len(tr0), (eq[-1], eq0[-1])
    out("== PART 2. Why S3 did not hold the six names (replica of oracle S3 reproduces the oracle equity exactly: final Rs{:,.0f}, {} trades) ==".format(eq[-1], len(tr)))
    k = KM.reindex(dates[i0:i1 + 1], method="ffill"); k1 = k[:"2026-04-15"]; pkd = k1.idxmax(); trd = k1[pkd:].idxmin()
    out(f"KMI All Share (index close) first-half peak {pkd.date()} {k[pkd]:,.0f}, trough {trd.date()} {k[trd]:,.0f} ({k[trd] / k[pkd] - 1:+.0%}); year start {k.iloc[0]:,.0f}, end {k.iloc[-1]:,.0f}")
    SH0, SH1 = pkd, trd + pd.Timedelta(days=10)
    out("\n-- the six names: every episode of 'closed above its prior 252-high' and what S3 did with it (consecutive sessions with the same state collapsed)")
    for s in SIX:
        c = cidx[s]; ev = [(i, st) for (i, ss, st) in log if ss == s]
        nsig = int(NH[i0:i1 + 1, c].sum())
        t_s = tr[tr.symbol == s]
        out(f"\n{s}: closes above the prior 252-high in the year {nsig}; S3 trades: {len(t_s)}")
        if not ev: out("   never signalled"); continue
        eps = []
        for i, st in ev:
            kind = st.split(":")[0].split(" for ")[0].split(" of ")[0]
            if eps and i - eps[-1][2] <= 1 and eps[-1][3] == kind: eps[-1][2] = i
            else: eps.append([i, st, i, kind, 0])
            eps[-1][4] += 1
        for a, st, b, kind, n in eps:
            bought = [r for r in t_s.itertuples() if r.entry == dates[min(a + 1, i1)]] if kind == "ORDER placed" else []
            out(f"   {D(a)}{'' if a == b else ' - ' + D(b)} ({n} sessions): {st}" + ("  -> bought next close" if bought else ""))
        for r in t_s.itertuples():
            c_ = cidx[s]; ei = int(dates.get_loc(r.entry)); xi = int(dates.get_loc(r.exit))
            out(f"   TRADE {r.entry.date()} -> {r.exit.date()} {r.ret:+.0%} Rs{r.pnl:,.0f} {r.reason}; entry median traded value Rs{MTV[ei, c_] / 1e6:.1f}m; max close gain after entry {np.nanmax(PX[ei:xi + 1, c_]) / PX[ei, c_] - 1:+.0%}")
    sig_any = {s: any(ss == s and not st.startswith(("liquidity", "not a KMI")) for (_, ss, st) in log) for s in SIX}
    out(f"\nSummary: of the six, with at least one S3-eligible signal (liquid, KMI): {[s for s in SIX if sig_any[s]]}; with an S3 trade: {[s for s in SIX if (tr.symbol == s).any()]}")
    out("\n-- the 12 S3 trades. ext = signal close over prior 252-high; runup = best close vs entry; next10d = return in the 10 sessions after entry; after20/60 = close 20/60 sessions after exit vs the exit close (positive = whipsaw, it recovered); KMI = index return while held")
    out(f"{'sym':<8}{'entry':<11}{'exit':<11}{'days':>5}{'ret':>6}{'Rs':>8} {'reason':<15}{'tv m':>7}{'ext':>6}{'runup':>7}{'next10d':>8}{'after20':>8}{'after60':>8}{'KMI':>6}  sector")
    for r in tr.sort_values("entry").itertuples():
        c = cidx[r.symbol]; ei = int(dates.get_loc(r.entry)); xi = int(dates.get_loc(r.exit)); si = ei - 1
        a20 = PX[min(xi + 20, i1), c] / PX[xi, c] - 1 if xi < i1 else np.nan; a60 = PX[xi + 60, c] / PX[xi, c] - 1 if xi + 60 <= i1 else np.nan
        kk = KM.asof(r.exit) / KM.asof(r.entry) - 1
        out(f"{r.symbol:<8}{str(r.entry.date()):<11}{str(r.exit.date()):<11}{xi - ei:>5}{r.ret:>6.0%}{r.pnl:>8,.0f} {r.reason:<15}{MTV[ei, c] / 1e6:>7.1f}{PX[si, c] / HI252[si, c] - 1:>6.1%}{np.nanmax(PX[ei:xi + 1, c]) / PX[ei, c] - 1:>7.0%}{PX[min(ei + 10, i1), c] / PX[ei, c] - 1:>8.0%}{a20:>8.0%}{a60:>8.0%}{kk:>6.0%}  {SECI[c]}")
    ls = tr[tr.pnl < 0].copy(); ls["grp"] = np.where((ls.exit >= SH0) & (ls.exit <= SH1), "stopped in the Feb-Mar shock window", np.where(ls.exit < pd.Timestamp("2025-12-01"), "failed within 6 weeks (Oct-Nov 2025)", "other stops"))
    out("\nloss attribution (the 9 losing trades): " + "; ".join(f"{g}: {', '.join(d.symbol)} Rs{d.pnl.sum():,.0f}" for g, d in ls.groupby("grp")) + f"; winners Rs{tr[tr.pnl > 0].pnl.sum():,.0f} (TPLT Rs{tr[tr.symbol == 'TPLT'].pnl.sum():,.0f})")
    held_by = {}
    for r in tr.itertuples():
        for i in range(int(dates.get_loc(r.entry)), int(dates.get_loc(r.exit)) + 1): held_by.setdefault(i, []).append(r.symbol)
    npos = [len(held_by.get(i, [])) for i in range(i0, i1 + 1)]
    out(f"\nsessions with 3 positions: {sum(1 for n in npos if n >= 3)} of {len(npos)}; with 0 positions: {sum(1 for n in npos if n == 0)}; mean positions {np.mean(npos):.2f}")
    allsig = [int((uni(i, w, 5e6) & NH[i]).sum()) for i in range(i0, i1)]
    out(f"liquid KMI names at a new 252-high per session: mean {np.mean(allsig):.1f}, max {max(allsig)}; sessions with at least one {sum(1 for n in allsig if n)}")
    out("monthly count of distinct liquid KMI names that made a new 252-high: " + ", ".join(f"{m}:{len(set(c for i in range(i0, i1) if dates[i].strftime('%y-%m') == m for c in np.where(uni(i, w, 5e6) & NH[i])[0]))}" for m in sorted(set(dates[i0:i1].strftime('%y-%m')))))

if run("part2"):
    part2(); flush("part2"); L.clear()

# ======================================================================================== PART 3
VARS = {
    "S3 base": lambda w, rng=None: run_bo(w, rng=rng),
    "F1 rotation": lambda w, rng=None: run_rot(w, rng=rng, name="F1"),
    "F2 no cap": lambda w, rng=None: run_ew(w),
    "F3 stop 30%": lambda w, rng=None: run_bo(w, stop=0.3, rng=rng, name="F3"),
    "F4 Rs2m + 2% cap": lambda w, rng=None: run_bo(w, thr=2e6, tvcap=True, name="F4"),
    "F4s (F4, 1.5% cost <Rs5m)": lambda w, rng=None: run_bo(w, thr=2e6, tvcap=True, stress=True, name="F4s"),
    "F5 pyramid": lambda w, rng=None: run_bo(w, pyr=True, name="F5"),
    "F6 = F1+F3+F4": lambda w, rng=None: run_rot(w, stop=0.3, thr=2e6, tvcap=True, rng=rng, name="F6"),
}
PLAC = {"S3 base": "P_bo(S3)", "F3 stop 30%": "P_bo(F3)", "F1 rotation": "P_rot(F1)", "F6 = F1+F3+F4": "P_rot(F6)"}
NPLC = int(os.environ.get("NPLC", "100"))
def part3():
    wins = [W1] + WINS[:5]
    R = {}      # (variant, window) -> stats
    out("== PART 3. Six pre-registered fixes (see the docstring) on the seen year and the five 2-year windows. Rs50,000 each, costs 0.25%/side (+0.25% under Rs20m), signals at close t, trades at close t+1 ==")
    for w in wins:
        yrs = (dates[w["i1"]] - dates[w["i0"]]).days / 365.25
        kb = KM.asof(dates[w["i1"]]) / KM.asof(dates[w["i0"]])
        out(f"\n--- window {w['name']} -> {D(w['i1'])} ({yrs:.1f} years, universe {'KMI liquid' if w['kmi'] else 'all liquid names'}); KMI All Share index multiple {kb:.2f}x")
        out(f"{'variant':<28}{'mult':>6}{'maxDD':>7}{'trades':>7}{'hit':>6}{'median':>8}{'worst':>7}" + ("   six names held (sessions, return)" if w is W1 else ""))
        for nm, f in VARS.items():
            eq, tr = f(w); st = stats(eq, tr); st["tr"] = tr; st["eq"] = eq; R[(nm, w["name"])] = st
            held = ""
            if w is W1:
                parts = []
                for s in SIX:
                    t_ = tr[tr.symbol == s]
                    if len(t_): parts.append(f"{s} {sum(int(dates.get_loc(r.exit)) - int(dates.get_loc(r.entry)) for r in t_.itertuples())}d {t_.invested.sum() and (t_.proceeds.sum() / t_.invested.sum() - 1):+.0%}")
                held = "   " + (", ".join(parts) if parts else "none")
            out(f"{nm:<28}{st['mult']:>6.2f}{st['dd']:>7.0%}{st['n']:>7}{st['hit']:>6.0%}{st['med']:>8.1%}{tr.ret.min() if len(tr) else float('nan'):>7.0%}{held}")
        if w is W1:
            for nm in ("F1 rotation", "F2 no cap"):
                t_ = R[(nm, w["name"])]["tr"].sort_values("pnl")
                out(f"  {nm} trades in the seen year: {len(t_)}, losers {int((t_.pnl < 0).sum())} (sum Rs{t_[t_.pnl < 0].pnl.sum():,.0f}), winners {int((t_.pnl > 0).sum())} (sum Rs{t_[t_.pnl > 0].pnl.sum():,.0f}); six names Rs{t_[t_.symbol.isin(SIX)].pnl.sum():,.0f}, other names Rs{t_[~t_.symbol.isin(SIX)].pnl.sum():,.0f}")
                out("    worst 6: " + "; ".join(f"{r.symbol} {r.entry.date()}->{r.exit.date()} {r.ret:+.0%}" for r in t_.head(6).itertuples()))
                out("    six names: " + "; ".join(f"{r.symbol} {r.entry.date()}->{r.exit.date()} {r.ret:+.0%} ({r.reason})" for r in t_[t_.symbol.isin(SIX)].sort_values("entry").itertuples()))
        for nm, pl in PLAC.items():
            rng = np.random.default_rng(abs(hash((pl, w["name"]))) % 2**32 if False else (sum(map(ord, pl + w["name"])) * 7919) % 2**32)
            m = np.array([VARS[nm](w, rng=rng)[0][-1] / START for _ in range(NPLC)])
            a = R[(nm, w["name"])]["mult"]; R[(pl, w["name"])] = dict(mult=np.median(m), p10=np.percentile(m, 10), p90=np.percentile(m, 90), rank=(m <= a).mean())
            out(f"{pl:<28}{np.median(m):>6.2f}  placebo p10 {np.percentile(m, 10):.2f} p90 {np.percentile(m, 90):.2f}; the real variant ({a:.2f}x) beats {(m < a).mean():.0%} of {NPLC} draws")
    out("\n== Summary across the five 2-year windows (not the seen year). mult = multiple of Rs50,000 after costs ==")
    w5 = [w["name"] for w in wins[1:]]
    out(f"{'variant':<28}" + "".join(f"{n[:7]:>9}" for n in w5) + f"{'median':>8}{'geomean':>8}{'min':>6}{'>base':>6}{'>KMI':>6}{'mean DD':>8}{'1yr(seen)':>10}")
    kmi = {w["name"]: KM.asof(dates[w["i1"]]) / KM.asof(dates[w["i0"]]) for w in wins}
    out(f"{'KMI All Share (no costs)':<28}" + "".join(f"{kmi[n]:>9.2f}" for n in w5) + f"{np.median([kmi[n] for n in w5]):>8.2f}{np.exp(np.mean(np.log([kmi[n] for n in w5]))):>8.2f}{min(kmi[n] for n in w5):>6.2f}{'':>12}{'':>8}{kmi[wins[0]['name']]:>10.2f}")
    for nm in VARS:
        ms = [R[(nm, n)]["mult"] for n in w5]; b = [R[("S3 base", n)]["mult"] for n in w5]
        out(f"{nm:<28}" + "".join(f"{m:>9.2f}" for m in ms) + f"{np.median(ms):>8.2f}{np.exp(np.mean(np.log(ms))):>8.2f}{min(ms):>6.2f}{sum(m > x for m, x in zip(ms, b)):>6}{sum(R[(nm, n)]['mult'] > kmi[n] for n in w5):>6}"
            f"{np.mean([R[(nm, n)]['dd'] for n in w5]):>8.0%}{R[(nm, wins[0]['name'])]['mult']:>10.2f}")
    out("   >base = windows (of 5) where the variant beat S3 base; >KMI = windows where it beat the index multiple. A 5-of-5 sign test has p = 0.031 one-sided, above the Bonferroni threshold 0.0083 for six variants.")
    out("\nPlacebo rank (share of random draws the real variant beat), by window:")
    for nm, pl in PLAC.items():
        out(f"{nm:<28}" + "".join(f"{n[:7]:>9}" for n in [wins[0]['name']] + w5))
        out(f"{'  placebo median':<28}" + "".join(f"{R[(pl, w['name'])]['mult']:>9.2f}" for w in wins))
        out(f"{'  real beats':<28}" + "".join(f"{R[(pl, w['name'])]['rank']:>9.0%}" for w in wins))
    return R

if run("part3"):
    R3 = part3(); flush("part3"); L.clear()
