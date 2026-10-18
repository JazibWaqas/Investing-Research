"""rs50k_last_year: Rs50,000 at the 2025-10-16 close, valued at the 2026-10-16 close. Benchmarks, walk-forward strategies (frozen rules, single deposit),
oracle-script systems S1-S6/S8 on the window, growth core hold, blends, and a CHEATING hindsight reference.
Run: .venv/Scripts/python.exe scripts/tests/rs50k_last_year.py   -> tests/out/rs50k_last_year.txt
Oracle systems run on a total-return panel rebuilt with cash dividends at 85% (the oracle script's own panel uses 100%); walkforward needs no change.
"""
import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
START = 50000.0; D0 = "2025-10-16"
sys.path.insert(0, str(ROOT / "scripts"))
os.environ["WF_START"] = "2018-01"
import numpy as np, pandas as pd

# ---- oracle machinery: run its source up to the run section, with the adj panel rebuilt at 85% dividends
src = (ROOT / "scripts/tests/oracle_and_good_case.py").read_text(encoding="utf-8")
head = src[:src.index("# ===================================================================== run")]
plc_src = src[src.index("rng = np.random.default_rng"):src.index('out("\\n== C. Placebo')]
old = 'adj = pd.read_parquet(ROOT / "data" / ("panel_close_adj_pricereturn.parquet" if PR else "panel_close_adj.parquet")).reindex(index=dates, columns=cols)'
new = '''_a = P.load_actions(); _a.loc[_a.type == "cash", "value"] *= 0.85
_tri = (1 + P.returns(raw, "adjusted", actions=_a).fillna(0)).cumprod()
adj = _tri.where(raw.notna()); adj = adj * (raw.ffill().iloc[-1] / adj.ffill().iloc[-1])'''
assert old in head
sys.argv = [sys.argv[0]]
O = {"__name__": "oracle", "__file__": str(ROOT / "scripts/tests/oracle_and_good_case.py")}
exec(compile(head.replace(old, new), "oracle", "exec"), O)
exec(compile(plc_src, "plc", "exec"), O)
dates, N, cols, PX, TRADED, MTV, cidx = O["dates"], O["N"], O["cols"], O["PX"], O["TRADED"], O["MTV"], O["cidx"]
i0 = int(dates.searchsorted(pd.Timestamp(D0))); i1 = N - 1
assert dates[i0] == pd.Timestamp(D0) and dates[i1] == pd.Timestamp("2026-10-16")
W = dict(name="2025-10-16", i0=i0, i1=i1, kmi=True)
rows = {}      # label -> dict(eq=array i0..i1, n=trades, sec=section)
def mdd(v): v = np.asarray(v); return float((v / np.maximum.accumulate(v) - 1).min())
def add(lab, eq, n, sec): rows[lab] = dict(eq=np.asarray(eq, float), n=n, sec=sec)

# 1. benchmarks (index closes, no costs, no trades)
for lab, f in (("KMI All Share TR", "kmiallshr"), ("KSE100 TR", "kse100"), ("KMI30 TR", "kmi30")):
    s = pd.read_csv(ROOT / f"data/macro/{f}.csv", parse_dates=["date"]).set_index("date").close.reindex(dates).ffill().values
    add(lab, START * s[i0:i1 + 1] / s[i0], 0, "1 benchmarks")

# 2. walk-forward (frozen rules, one deposit; first monthly trade date on/after the start)
import walkforward as wf
assert wf.dates.equals(dates)
K, ID = wf.K, wf.ID
wf.set_pool(None); wf.build_val("frozen"); _, _, sigs = wf.build_feat("TR")
k0 = next(k for k in range(K) if dates[ID[k]] >= pd.Timestamp(D0)); iw = ID[k0]
wf.DEPS = [0.0] * K; wf.DEPS[k0] = START
for st in ("B0", "B1", "S2", "S3", "S4"):
    R = wf.Run(st, "TR", "frozen")
    for k in range(k0, K): wf.step(R, st, k, sigs)
    _, nav = wf.nav_from(R); tr = wf.trades_df(R)
    add(f"WF {st} (frozen, entry {dates[iw].date()})", np.concatenate([np.full(iw - i0, START), nav[iw:i1 + 1]]), len(tr), "2 walk-forward strategies")
    if st == "S3": WF_S3 = tr

# 3. oracle systems
TRD = {}
for s in ("S1", "S2", "S3", "S4", "S5", "S6", "S8"):
    eq, tr = O["run"](s, W, i0, i1, True); TRD[s] = tr
    add(f"{s} oracle-script", eq, len(tr), "3 oracle-script systems")
plc = O["placebo"](W, 200)

# 4. growth core hold
def hold(names, tag):
    sim = O["Sim"](i0, tag, W["name"])
    for c in names: assert sim.buy(c, START / len(names), i0), c
    for i in range(i0, i1 + 1): sim.eq.append(sim.value(i))
    for c in list(sim.pos): sim.sell(c, 1.0, i1, "end_open")
    eq = np.array(sim.eq); eq[-1] = sim.cash
    return eq
core = hold([cidx[s] for s in ("LUCK", "MEBL", "SYS", "MARI")], "core")
add("Growth core hold (LUCK MEBL SYS MARI)", core, 4, "4 growth core and blends")
s3 = rows["S3 oracle-script"]["eq"]
for w_ in (0.6, 0.75):
    add(f"{int(w_ * 100)}% core + {int(round((1 - w_) * 100))}% S3 breakout", w_ * core + (1 - w_) * s3, 4 + rows["S3 oracle-script"]["n"], "4 growth core and blends")

# 6. hindsight (CHEATING)
u = O["universe"](i0, True) & TRADED[i0] & np.isfinite(PX[i1])
m = pd.Series(PX[i1] / PX[i0], index=cols)[u].sort_values(ascending=False)
add("CHEATING best-5 liquid KMI names in hindsight (" + " ".join(m.index[:5]) + ")", hold([cidx[s] for s in m.index[:5]], "h5"), 5, "6 hindsight reference")
add("CHEATING single best liquid KMI name in hindsight (" + m.index[0] + ")", hold([cidx[m.index[0]]], "h1"), 1, "6 hindsight reference")

# -------------------------------------------------- report
L = []; w = L.append
w(f"== Rs50,000 at {D0} close, valued {dates[i1].date()} close. Fully reinvested, cash dividends at 85% (only where in data/corporate_actions.csv; complete from Nov 2024), "
  "costs 0.25%/side (+0.25% under Rs20m traded value), final values after exit costs for traded lines; index lines have no costs.")
w(f"{'line':<90}{'final Rs':>10}{'multiple':>9}{'maxDD':>8}{'trades':>7}")
sec = None
for lab, r in rows.items():
    if r["sec"] != sec: sec = r["sec"]; w(f"-- {sec}")
    e = r["eq"]; w(f"{lab:<90}{e[-1]:>10,.0f}{e[-1] / START:>9.2f}{mdd(e):>8.1%}{r['n']:>7}")
    if lab == "S8 oracle-script":
        w(f"  placebo, 200 random monthly rotations into 3 liquid names: p10 {np.percentile(plc, 10):.2f}x (Rs{np.percentile(plc, 10) * START:,.0f}), "
          f"median {np.median(plc):.2f}x (Rs{np.median(plc) * START:,.0f}), p90 {np.percentile(plc, 90):.2f}x (Rs{np.percentile(plc, 90) * START:,.0f})")
w(f"\nWalk-forward trades only on the first session of a month, so its Rs50,000 sits in cash from {D0} to {dates[iw].date()}; the oracle-script systems start {D0} exactly.")
mi = sorted(set([i0] + [int(dates.searchsorted(m_.start_time)) for m_ in pd.period_range("2025-11", "2026-10", freq="M")] + [i1]))
cs = ["S3 oracle-script", "Growth core hold (LUCK MEBL SYS MARI)", "60% core + 40% S3 breakout", "KMI All Share TR"]
w("\n== Month by month (first session of each month; last row 2026-10-16)")
w(f"{'date':<12}{'S3 breakout':>13}{'growth core':>13}{'60/40 blend':>13}{'KMI TR':>10}")
for i in mi: w(f"{str(dates[i].date()):<12}" + "".join(f"{rows[c]['eq'][i - i0]:>{n_},.0f}" for c, n_ in zip(cs, (13, 13, 13, 10))))
w("\n== S3 breakout trades (oracle-script version), by Rs P&L")
for r in TRD["S3"].sort_values("pnl", ascending=False).itertuples():
    w(f"  {r.symbol:<8}{r.entry.date()} -> {r.exit.date()}  {r.ret:+.0%}  Rs{r.pnl:,.0f}  {r.reason}")
w("\n== Walk-forward S3 trades")
for r in WF_S3.itertuples(): w(f"  {r.symbol:<8}{str(r.entry)[:10]} -> {str(r.exit)[:10] if r.status == 'closed' else 'open'}  {r.ret:+.0%}")
w("\n== Core names (price+dividend, no costs): " + "  ".join(f"{s} {PX[i1, cidx[s]] / PX[i0, cidx[s]]:.2f}x" for s in ("LUCK", "MEBL", "SYS", "MARI")))
w("Hindsight top 10 liquid KMI names (no costs): " + "  ".join(f"{s} {v:.2f}x" for s, v in m.head(10).items()))
txt = "\n".join(L) + "\n"
(ROOT / "tests/out/rs50k_last_year.txt").write_text(txt, encoding="utf-8"); print(txt)
