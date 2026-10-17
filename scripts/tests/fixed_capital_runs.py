"""fixed_capital_runs: B0, B1, S2, S3, S4 with ONE Rs50,000 deposit (no later deposits) from six start dates to 2026-10-16.
Run: .venv/Scripts/python.exe scripts/tests/fixed_capital_runs.py   (spawns itself twice: frozen 2018-01 calendar and a 2017-01 calendar for the 2016-12-30 start)
Writes tests/out/fixed_capital_runs.txt. Rules are the frozen ones in knowledge/playbooks/strategy_candidates.md; only the deposit schedule differs (walkforward.DEPS).
"""
import os, sys, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "tests/out"
START = 50000.0
CAL = {"2024-10-01": "2018-01", "2024-01-01": "2018-01", "2022-10-01": "2018-01", "2020-10-01": "2018-01", "2018-10-01": "2018-01", "2016-12-30": "2017-01"}
STRATS = ("B0", "B1", "S2", "S3", "S4")


def worker(cal):
    os.environ["WF_START"] = cal
    sys.path.insert(0, str(ROOT / "scripts"))
    import numpy as np, pandas as pd
    import walkforward as wf
    dates, N, K, ID, M, TR, C = wf.dates, wf.N, wf.K, wf.ID, wf.M, wf.TRI["TR"], wf.C
    wf.set_pool(None); wf.build_val("frozen"); _, _, sigs = wf.build_feat("TR")
    res = {"cal": cal, "K": K}
    if cal == "2018-01":      # default behaviour check: monthly Rs50k deposits must still give the frozen S3 headline
        R = wf.Run("S3", "TR", "frozen")
        for k in range(K): wf.step(R, "S3", k, sigs)
        res["default_S3"] = float(wf.nav_from(R)[1][-1])
    def idx(f): return pd.read_csv(ROOT / "data/macro" / f, parse_dates=["date"]).set_index("date").close.reindex(dates).ffill().values
    INDEX = {"KMI All Share TR": idx("kmiallshr.csv"), "KSE100 TR": idx("kse100.csv"), "KSE100 PR": idx("kse100pr.csv"), "KSE30 PR": idx("kse30.csv")}
    yrs_of = lambda i0: (wf.LAST - dates[i0]).days / 365.25
    def summ(v, i0):      # v = daily value path from i0 (starts at START before cost); multiple, CAGR, max drawdown
        v = np.concatenate([[START], v]); m = v[-1] / START
        return dict(final=float(v[-1]), mult=float(m), cagr=float(m ** (1 / yrs_of(i0)) - 1), mdd=float((v / np.maximum.accumulate(v) - 1).min()))
    rng = np.random.default_rng(20261018)
    res["starts"] = {}
    for sd, c in CAL.items():
        if c != cal: continue
        k0 = next(k for k in range(K) if dates[ID[k]] >= pd.Timestamp(sd)); i0 = ID[k0]
        wf.DEPS = [0.0] * K; wf.DEPS[k0] = START
        o = dict(trade_date=str(dates[i0].date()), k0=k0, pdates=[str(dates[i].date()) for i in ID[k0:] + [N - 1]], strat={}, index={}, names={})
        for st in STRATS:
            R = wf.Run(st, "TR", "frozen")
            for k in range(k0, K): wf.step(R, st, k, sigs)
            Um, nav = wf.nav_from(R)
            chk = max(abs(R.nav_pre[k] + wf.DEPS[k] - R.fees[k] - (Um[ID[k]] * R.T[ID[k]]).sum()) for k in range(k0, K))
            assert chk < 1e-4 * START, chk
            tr = wf.trades_df(R); t = wf.tstat(tr.ret) if len(tr) else dict(n=0, hit=np.nan, med=np.nan, mean=np.nan, worst=np.nan)
            o["strat"][st] = dict(**summ(nav[i0:], i0), trades=len(tr), closed=int((tr.status == "closed").sum()) if len(tr) else 0, sells=int(sum(R.reason_n.values())),
                                  hit=float(t["hit"]), med=float(t["med"]), tmean=float(t["mean"]), worst=float(t["worst"]), names=float(np.mean(R.nhold[k0:])), nav=nav[ID[k0:] + [N - 1]].tolist() if sd == "2024-10-01" else None)
            if st == "S3": o["S3_trades"] = tr.assign(entry=tr.entry.astype(str), exit=tr.exit.astype(str))[["symbol", "entry", "exit", "ret", "status", "reason"]].to_dict("records")
        E = wf.EWRun("EW", "TR", "frozen")
        for k in range(k0, K): E.step(k)
        _, nav = wf.nav_from(E)
        o["index"]["EW liquid KMI basket (monthly rebal., 0.5% costs)"] = dict(**summ(nav[i0:], i0), path=nav[ID[k0:] + [N - 1]].tolist() if sd == "2024-10-01" else None)
        for nm, a in INDEX.items():
            if not np.isfinite(a[i0]): o['index'][nm] = None; continue      # KSE100 PR starts 2020-04-01
            o["index"][nm] = dict(**summ(START * a[i0:] / a[i0], i0), path=(START * a[ID[k0:] + [N - 1]] / a[i0]).tolist() if sd == "2024-10-01" else None)
        # buy-and-hold of each liquid KMI name in U(t0), bought at the trade date, 0.5% round trip, TR basis
        U = [s for s in M[k0]["U"] if np.isfinite(wf.closeV[i0, wf.cidx[s]])]
        rows = []
        for s in U:
            p = TR[i0:, wf.cidx[s]] / TR[i0, wf.cidx[s]] * (1 - C) / (1 + C) * START
            rows.append((s, summ(p, i0)))
        rows.sort(key=lambda x: -x[1]["mult"]); mu = np.array([r[1]["mult"] for r in rows])
        o["names"] = dict(n=len(rows), best=rows[0], tenth=rows[9] if len(rows) > 9 else None, worst=rows[-1], median=float(np.median(mu)), mean=float(mu.mean()), win=float((mu > 1).mean()), ge2=int((mu >= 2).sum()), ge3=int((mu >= 3).sum()),
                          beat_kmi=float((mu > o["index"]["KMI All Share TR"]["mult"]).mean()), top3=[(r[0], r[1]["mult"]) for r in rows[:3]], bottom3=[(r[0], r[1]["mult"]) for r in rows[-3:]])
        # placebo: every 3 months sell everything and buy 4 random names of U(t) equal weight (0.5% round trip per switch), 1,000 sims, end value before exit fee
        ks = list(range(k0, K, 3)); nsim = 1000; val = np.full(nsim, START / (1 + C)); ends = [ID[k] for k in ks[1:]] + [N - 1]
        for k, e in zip(ks, ends):
            pool = [wf.cidx[s] for s in M[k]["U"] if np.isfinite(wf.closeV[ID[k], wf.cidx[s]])]
            cs = np.array([rng.choice(pool, 4, replace=False) for _ in range(nsim)])
            val *= (TR[e, cs] / TR[ID[k], cs]).mean(axis=1)
            if e != N - 1: val *= (1 - C) / (1 + C)
        o["placebo"] = dict(med=float(np.median(val) / START), p5=float(np.percentile(val, 5) / START), p95=float(np.percentile(val, 95) / START), mean=float(val.mean() / START),
                            win=float((val > START).mean()), s3_pct=float((val < o["strat"]["S3"]["final"]).mean()), n=nsim, rotations=len(ks))
        res["starts"][sd] = o
        print("done", sd, file=sys.stderr)
    (OUT / f"fixed_capital_runs_{cal}.json").write_text(json.dumps(res), encoding="utf-8")


def pc(x): return "-" if x is None or x != x else f"{x:+.1%}"
def rs(x): return f"{x:,.0f}"


def assemble():
    A = json.loads((OUT / "fixed_capital_runs_2018-01.json").read_text()); B = json.loads((OUT / "fixed_capital_runs_2017-01.json").read_text())
    S = {**A["starts"], **B["starts"]}
    L = []
    w = L.append
    w("== FIXED CAPITAL RUNS: one Rs50,000 deposit, no further deposits, to 2026-10-16. Frozen rules, TR basis (15% withholding on known cash dividends; complete only from Nov 2024).")
    w(f"Default-behaviour check: monthly Rs50k deposits, S3 final = Rs{A['default_S3']:,.0f} (frozen headline Rs17,630,566) -> {'REPRODUCED' if round(A['default_S3']) == 17630566 else 'MISMATCH'}")
    w("Entry = first close of the start month (formed on the prior month-end). 2016-12-30 uses a 2017-01 calendar (K=%d months) because the frozen calendar starts 2018-01; the others use the frozen 2018-01 calendar (regime state carried from 2018-01).\n" % B["K"])
    for sd in CAL:
        o = S[sd]
        w(f"-- START {sd} (entry {o['trade_date']}); strategies' final value is mark-to-market before an exit fee; B0 has no sales except Shariah exits")
        w(f"{'row':<56}{'final Rs':>12}{'multiple':>9}{'CAGR':>9}{'maxDD':>9}{'trades':>8}{'sells':>6}{'hit':>6}{'med trade':>10}{'worst':>8}")
        for st in STRATS:
            s = o["strat"][st]
            w(f"{st:<56}{rs(s['final']):>12}{s['mult']:>9.2f}{pc(s['cagr']):>9}{pc(s['mdd']):>9}{s['trades']:>8}{s['sells']:>6}{s['hit']:>6.0%}{pc(s['med']):>10}{pc(s['worst']):>8}")
        for nm, s in o["index"].items():
            if s is None: w(f"{nm:<56}  n/a (series starts 2020-04-01)"); continue
            w(f"{nm:<56}{rs(s['final']):>12}{s['mult']:>9.2f}{pc(s['cagr']):>9}{pc(s['mdd']):>9}")
        n = o["names"]
        for lab, r in (("best liquid KMI name (buy & hold)", n["best"]), ("10th best", n["tenth"]), ("worst (survivors only)", n["worst"])):
            w(f"{lab + ' ' + r[0]:<56}{rs(r[1]['final']):>12}{r[1]['mult']:>9.2f}{pc(r[1]['cagr']):>9}{pc(r[1]['mdd']):>9}")
        w(f"Names in U(t0): n={n['n']}; buy-and-hold multiple median {n['median']:.2f}, mean {n['mean']:.2f}, win rate (>1.0x) {n["win"]:.0%}, names >=2x {n["ge2"]} and >=3x {n["ge3"]}, beat KMI TR {n['beat_kmi']:.0%}; top3 {[(a, round(b, 1)) for a, b in n['top3']]}; bottom3 {[(a, round(b, 2)) for a, b in n['bottom3']]}")
        p = o["placebo"]
        w(f"Placebo (quarterly rotation into 4 random U(t) names, {p['rotations']} rotations, {p['n']} sims, 0.5% per switch): median {p['med']:.2f}x, 5th-95th {p['p5']:.2f}-{p['p95']:.2f}x, mean {p['mean']:.2f}x, win {p['win']:.0%}; S3 beats {p['s3_pct']:.0%} of sims\n")
    o = S["2024-10-01"]
    w("== MONTH BY MONTH, Rs50,000 entered 2024-10-01 (first close of each month; last row 2026-10-16)")
    s3, kmi, k100, ew = o["strat"]["S3"]["nav"], o["index"]["KMI All Share TR"]["path"], o["index"]["KSE100 TR"]["path"], o["index"]["EW liquid KMI basket (monthly rebal., 0.5% costs)"]["path"]
    w(f"{'date':<12}{'S3':>10}{'KMI TR':>10}{'KSE100 TR':>11}{'EW KMI':>10}{'S3/KMI':>8}")
    for i, x in enumerate(o['pdates']):
        w(f"{x:<12}{s3[i]:>10,.0f}{kmi[i]:>10,.0f}{k100[i]:>11,.0f}{ew[i]:>10,.0f}{s3[i] / kmi[i]:>8.2f}")
    w("\nS3 trades since 2024-10-01 (closed and open): " + "; ".join(f"{t['symbol']} {t['entry']}->{t['exit'] if t['status']=='closed' else 'open'} {t['ret']:+.0%}" for t in o["S3_trades"]))
    (OUT / "fixed_capital_runs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    if len(sys.argv) > 1: worker(sys.argv[1])
    else:
        for cal in ("2018-01", "2017-01"):
            subprocess.run([sys.executable, str(Path(__file__)), cal], check=True, cwd=ROOT)
        assemble()
