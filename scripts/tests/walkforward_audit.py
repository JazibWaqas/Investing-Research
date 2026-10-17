"""Audit checks, S3 post-mortem and trade calibration for the system walk-forward (Opus, 2026-10-17).
Run: .venv/Scripts/python.exe -I scripts/tests/walkforward_audit.py > tests/out/walkforward_audit.txt   (after scripts/walkforward.py)
Reads tests/out/walkforward_trades.csv (frozen headline run) and the walkforward module's point-in-time state."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np, pandas as pd, walkforward as W
pd.set_option("display.width", 400); pd.set_option("display.max_colwidth", 60)
W.set_pool(None); W.build_val("frozen"); W.build_feat("TR")
M, dates, cidx, T, raw = W.M, W.dates, W.cidx, W.TRI["TR"], W.rawF
fy, e = W.fy, W.e

print("== A. sa_ratios pe is on the fiscal-year-end price: implied EPS (raw close at FYE / pe) over the sum of the 4 quarterly EPS")
rows = []
for r in fy.itertuples():
    if not (np.isfinite(r.pe) and r.pe > 0): continue
    g = e[(e.symbol == r.t) & (e.qe > r.fye - pd.Timedelta(days=360)) & (e.qe <= r.fye)]
    if len(g) != 4 or g.eps.isna().any(): continue
    s4, c = g.eps.sum(), cidx[r.t]
    i = max(int(dates.searchsorted(r.fye, side="right")) - 1, 0)
    pa = raw[r.i_ann, c] if r.i_ann >= 0 else np.nan
    rows.append(dict(fy=r.fye.year, fye=abs(np.log(raw[i, c] / r.pe / s4)), ann=abs(np.log(pa / r.pe / s4)), now=abs(np.log(raw[-1, c] / r.pe / s4))))
d = pd.DataFrame(rows)
print(f"n {len(d)}; within 5%: at FYE price {(d.fye < .05).mean():.0%}, at filing price {(d.ann < .05).mean():.0%}, at 16 Oct 2026 price {(d.now < .05).mean():.0%}")
print("median abs log error by FY:"); print(d.groupby("fy")[["fye", "ann", "now"]].median().round(3).to_string())

print("\n== B. Membership: derived lists vs later notices, and members the panel cannot price")
ic = pd.read_csv(W.ROOT / "data/index_changes.csv"); ic["effective_date"] = pd.to_datetime(ic.effective_date, errors="coerce")
ic = ic[(ic["index"] == "KMI_ALL") & ~ic.source_url.astype(str).str.contains("derived")].copy(); ic["symbol"] = ic.symbol.map(W.norm)
bad = 0
for d0, L in sorted(W.LISTS.items()):
    fut = ic[ic.effective_date > d0].sort_values("effective_date").groupby("symbol").first()
    bad += sum(1 for s in L if s in fut.index and fut.loc[s, "action"] == "add")
print(f"names sitting in a list whose next KMI_ALL change is an add: {bad} (over {len(W.LISTS)} lists)")
npn = [sum(s not in cidx for s in W.members_at(m["F"])) for m in M]
print(f"members with no price series (delisted or renamed): mean {np.mean(npn):.1f}, max {max(npn)} a month")

print("\n== C. Quarterly EPS and annual value-row dates")
dd = e[e.dated]; lag = (dd.ann - dd.qe).dt.days; h = dd.ann.dt.hour * 60 + dd.ann.dt.minute
print(f"dated rows {len(dd)}; days from quarter end to filing: min {lag.min()}, median {lag.median():.0f}, max {lag.max()}; re-joined date differs from the file's {int((dd.ann.dt.floor('min') != dd.cur.dt.floor('min')).sum())} "
      f"(earlier {int((dd.ann < dd.cur).sum())}, later {int((dd.ann > dd.cur).sum())}); filed after 15:30 {int((h > 930).sum())}")
L = (dates[np.minimum(fy.use_frozen, W.N - 1)] - fy.fye).dt.days
print(f"value rows usable after FYE: min {L.min()} days, median {L.median():.0f}, max {L.max()}; under 30 days: {int((L < 30).sum())}")

t = pd.read_csv(W.ROOT / "tests/out/walkforward_trades.csv", parse_dates=["entry", "exit"])
t["k"] = [W.KOF[dates.get_loc(x)] for x in t.entry]; t["regime"] = [M[k]["s3"] for k in t.k]; t["vmode"] = [M[k]["value_mode"] for k in t.k]
t["pnl"] = t.proceeds - t.cost
def ix_(r): return dates.get_loc(r.exit) if pd.notna(r.exit) else W.N - 1

print("\n== D. S3 post-mortem: 10 worst and 10 best trades by rupee P&L (ret = trade return over all buys; tri = price path from first buy)")
def info(r):
    ie, ix = dates.get_loc(r.entry), ix_(r); m, c, sec = M[r.k], cidx[r.symbol], W.SEC.get(r.symbol)
    v = m["val"].get(r.symbol, {}); secn = [cidx[x] for x in m["bysec"].get(sec, [])]
    path = T[ie:ix + 1, c]
    ca = W.ACTS[(W.ACTS.symbol == r.symbol) & (W.ACTS.ex_date > dates[ie]) & (W.ACTS.ex_date <= dates[ix]) & (W.ACTS.type != "cash")]
    return dict(sym=r.symbol, entry=r.entry.date(), exit=r.exit.date() if pd.notna(r.exit) else "open", reason=r.reason, pnl_k=round(r.pnl / 1e3), ret=f"{r.ret:+.0%}", nbuys=r.nbuys,
                regime=m["s3"], sector=sec, sec6m=f"{m['sec6'].get(sec, np.nan):+.0%}", ey=f"{v['ey']:.3f}" if v else "-", roe=f"{v['roe']:.2f}" if v else "-",
                raw_px=f"{raw[ie, c]:.1f}->{raw[ix, c]:.1f}", tri=f"{T[ix, c] / T[ie, c] - 1:+.0%}",
                sector_ew=f"{np.nanmean([T[ix, j] / T[ie, j] - 1 for j in secn]):+.0%}" if secn else "-",
                kse=f"{W.kse[ix] / W.kse[ie] - 1:+.0%}", maxdd=f"{(path / np.maximum.accumulate(path)).min() - 1:.0%}",
                bonus_split=";".join(f"{a.ex_date.date()} {a.type} {a.value:g}" for a in ca.itertuples()))
s3 = t[t.strategy == "S3"]
print("WORST"); print(pd.DataFrame([info(r) for r in s3.nsmallest(10, "pnl").itertuples()]).to_string(index=False))
print("BEST"); print(pd.DataFrame([info(r) for r in s3.nlargest(10, "pnl").itertuples()]).to_string(index=False))
print(f"S3 total P&L Rs{s3.pnl.sum() / 1e6:.2f}m; SAZEW Rs{s3[s3.symbol == 'SAZEW'].pnl.sum() / 1e6:.2f}m; LUCK Rs{s3[s3.symbol == 'LUCK'].pnl.sum() / 1e6:.2f}m")
for s in ("ECOP", "CHCC", "TGL", "SAZEW", "LUCK"):
    g = e[(e.symbol == s) & (e.qe >= "2023-06-30")]
    print(s, "quarterly EPS:", " ".join(f"{q:%y%m}:{x}" for q, x in zip(g.qe, g.eps)))

print("\n== E. Calibration by signal type (closed trades; open trades counted separately)")
def typ(r):
    if r.strategy == "B0": return "B0 market name, buy and hold"
    if r.sleeve == "sat": return f"{r.strategy} sat: ignored blowout quarter"
    if r.sleeve == "ew": return f"{r.strategy} EW filler"
    base = {"B1": "B1 value+regime (EY+DY top 5)", "S2": "S2 top-3 momentum sector", "S3": "S3 regime sector", "S4": "S4 regime sector, top 2"}[r.strategy]
    return f"{base}, {'value pick' if r.vmode else 'EW of sector (pre-value)'}" + (f", {r.regime}" if r.strategy in ("S3", "S4") else "")
t["type"] = [typ(r) for r in t.itertuples()]
def agg(g):
    c = g[g.status == "closed"]
    return pd.Series(dict(n=len(c), hit=f"{(c.ret > 0).mean():.0%}", median=f"{c.ret.median():+.1%}", p25=f"{c.ret.quantile(.25):+.1%}", p75=f"{c.ret.quantile(.75):+.1%}",
                          mean=f"{c.ret.mean():+.1%}", worst=f"{c.ret.min():+.1%}", sessions=c.sessions.median(), open=int((g.status == "open").sum()), pnl_m=round(g.pnl.sum() / 1e6, 2)))
print(t.groupby("type").apply(agg).to_string())
print("S3 and S4 value picks, all regimes together:")
print(t[t.strategy.isin(["S3", "S4"]) & (t.sleeve == "core") & t.vmode].groupby("strategy").apply(agg).to_string())
print("\nValue-mode core picks, lump sum from first buy to exit, vs 1,000 placebo sets (random pool name in the same sector; random pool name in U(t)), seed 7")
rng = np.random.default_rng(7)
for st in ("B1", "S2", "S3", "S4"):
    act, ps, pu = [], [], []
    for r in t[(t.strategy == st) & (t.sleeve == "core") & t.vmode].itertuples():
        ie, ix = dates.get_loc(r.entry), ix_(r)
        lr = lambda j: T[ix, j] / T[ie, j] * (1 - W.C) / (1 + W.C) - 1
        ok = lambda s: s != r.symbol and np.isfinite(W.closeV[ie, cidx[s]]) and s in W.POOL
        sec = [cidx[s] for s in M[r.k]["bysec"].get(W.SEC.get(r.symbol), []) if ok(s)]
        act.append(lr(cidx[r.symbol]))
        ps.append(lr(rng.choice(sec, 1000)) if sec else np.full(1000, np.nan))
        pu.append(lr(rng.choice([cidx[s] for s in M[r.k]["U"] if ok(s)], 1000)))
    act, ps, pu = np.array(act), np.array(ps), np.array(pu); f = ~np.isnan(ps[:, 0])
    ms, mu = np.median(ps[f], axis=0), np.median(pu, axis=0)
    print(f"{st}: n {len(act)}, median {np.median(act):+.1%}, hit {(act > 0).mean():.0%} | same-sector placebo {np.median(ms):+.1%}, diff {np.median(act[f]) - np.median(ms):+.1%}, "
          f"actual above {(ms < np.median(act[f])).mean():.0%} of sets | pool placebo {np.median(mu):+.1%}, diff {np.median(act) - np.median(mu):+.1%}, above {(mu < np.median(act)).mean():.0%}")
