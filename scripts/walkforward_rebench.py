"""Like-for-like benchmarks and the cap-weighted core (18 Oct 2026). Imports the frozen engine from walkforward.py; no pre-registered rule is changed.
Run: .venv/Scripts/python.exe -I scripts/walkforward_rebench.py      Writes tests/out/walkforward_rebench.txt.
1. ACCRUED basis: before Nov 2024 (corporate_actions.csv has almost no cash dividends) each holding-month accrues the name's last published fiscal-year
   dividend yield (sa_ratios.csv) / 12 at 85%. The 94 cash rows dated before Nov 2024 are dropped from the accrued basis so nothing is counted twice.
2. B2 (cap-weighted core proxy, 12 names), B2-EW, B0-monthly.   3. 70/30 blend of B2 and S3, rebalanced annually.
"""
import sys, io
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import walkforward as W
from walkforward import (ROOT, dates, N, K, ID, IF, M, DEP, C, MINT, LAST, cidx, cols, close, RET, TRI, A_NET, Run, nav_from, stats, waterfill, pc, rs, closeV)
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")

CUT = pd.Timestamp("2024-11-01")
NB, CAP = 12, 0.15

# ================================================================ 1. accrued basis
fy = W.fy.copy()
fy["pubi"] = np.maximum(fy.use_frozen, fy.i_fb4)                       # later of the annual-result announcement (else FYE+4m) and FYE+4m
def make_acc(tag, backfill):
    """backfill (POST-HOC): months before a name's first published sa_ratios row use that first row's yield. Strict mode leaves them at 0."""
    acc = np.zeros((K, len(cols)))                                     # monthly net accrual rate per name and holding month
    for s, g in fy.groupby("t"):
        g = g.sort_values("fye")
        for k in range(K):
            ok = g[g.pubi <= ID[k]]
            y = (ok.iloc[-1] if len(ok) else g.iloc[0] if backfill else None)
            if y is not None and np.isfinite(y.dividendyield): acc[k, cidx[s]] = 0.85 * y.dividendyield / 12
    rate = np.zeros((N, len(cols)))
    for k in range(K):
        hi = ID[k + 1] if k + 1 < K else N - 1
        rate[ID[k] + 1:hi + 1] = acc[k] / (hi - ID[k])
    rate[dates >= CUT] = 0.0
    RET[tag] = r_acc.add(pd.DataFrame(np.where(np.isfinite(rv), rate, 0.0), index=dates, columns=cols))
    TRI[tag] = (1 + RET[tag].fillna(0)).cumprod().values
    return acc
A_ACC = A_NET[~((A_NET.type == "cash") & (pd.to_datetime(A_NET.ex_date) < CUT))]
r_acc = P.returns(close, "adjusted", actions=A_ACC)
rv = r_acc.values
ACC = {"accrued": make_acc("ACC", False), "accrued_bf": make_acc("ACCBF", True)}
BASIS = {"frozen": "TR", "accrued": "ACC", "accrued_bf": "ACCBF"}

# ================================================================ benchmarks (same deposits, same dates, no costs)
def idx_run(path):
    x = pd.read_csv(ROOT / path, parse_dates=["date"]).set_index("date").close.reindex(dates).ffill().values
    nav, npre, u = np.full(N, np.nan), np.zeros(K), 0.0
    for k in range(K):
        iD = ID[k]; npre[k] = u * x[iD]; u += DEP / x[iD]
        hi = ID[k + 1] if k + 1 < K else N
        nav[iD:hi] = u * x[iD:hi]
    return dict(nav=nav, stats=stats(nav, npre), R=None)
BENCH = {"KMI All Share TR": idx_run("data/macro/kmiallshr.csv"), "KMI30 TR": idx_run("data/macro/kmi30.csv"), "KSE100 TR": idx_run("data/macro/kse100.csv")}

# ================================================================ 2. B2, B2-EW
def capw(v):
    w = v / v.sum()
    while (w > CAP + 1e-12).any():
        over = w > CAP
        free = ~over
        ex = (w[over] - CAP).sum(); w[over] = CAP; w[free] += ex * w[free] / w[free].sum()
    return w

def targets(k):
    m, F = M[k], M[k]["F"]
    w = tv[tv.index < F].tail(60).median()
    names = [s for s in m["U_all"] if s in m["mem_exit"] and np.isfinite(closeV[ID[k], cidx[s]])]
    top = w[names].sort_values(ascending=False).head(NB)
    return top.index.tolist(), dict(zip(top.index, capw(top.values.astype(float))))
tv = W.tv

def run_b2(basis, equal):
    R = Run("B2-EW" if equal else "B2", basis, "frozen")
    T, tg, hist, dele = R.T, {}, [], 0
    for k in range(K):
        m, iD = M[k], ID[k]
        R.nav_pre[k] = sum(p["u"] * T[iD, p["c"]] for p in R.pos.values())
        tradable = lambda s: np.isfinite(closeV[iD, cidx[s]])
        sells = [s for s in R.pos if s not in m["mem_exit"] and tradable(s)]
        dele += len(sells)
        if m["F"].month in (3, 6, 9, 12) or not tg or any(s not in m["mem_exit"] for s in tg):
            names, wts = targets(k)
            tg = {s: 1 / len(names) for s in names} if equal else wts
            hist.append((m["F"], set(names)))
        pool = DEP
        for s in sells: pool += R.sell(k, s, 1.0, "shariah")
        tg = {s: w for s, w in tg.items() if tradable(s)} or tg
        Vtot = sum(p["u"] * T[iD, p["c"]] for p in R.pos.values()) + pool
        short = {s: w * Vtot - (R.pos[s]["u"] * T[iD, R.pos[s]["c"]] if s in R.pos else 0.0) for s, w in tg.items()}
        alloc = waterfill(pool, short, MINT) or {s: pool * w / sum(tg.values()) for s, w in tg.items()}
        for s, a in alloc.items(): R.buy(k, s, a, "core")
        R.nhold[k] = len(R.pos)
    Um, nav = nav_from(R)
    chk = [R.nav_pre[k] + DEP - R.fees[k] - (Um[ID[k]] * R.T[ID[k]]).sum() for k in range(K)]
    assert max(abs(x) for x in chk) < 1e-4 * DEP
    return dict(R=R, nav=nav, stats=stats(nav, R.nav_pre), hist=hist, dele=dele)

# ================================================================ 3. 70/30 blend (B2 + S3), annual rebalance in the first trade month of each year
def blend(a, b):
    pa, pb = a["stats"]["price"].values, b["stats"]["price"].values
    uA = uB = 0.0
    nav, npre, flow = np.full(N, np.nan), np.zeros(K), 0.0
    for k in range(K):
        iD = ID[k]
        npre[k] = uA * pa[iD] + uB * pb[iD]
        vA, vB = uA * pa[iD] + 0.7 * DEP, uB * pb[iD] + 0.3 * DEP
        if k and M[k]["D"].month == 1:
            tot = vA + vB; mv = abs(vA - 0.7 * tot); flow += mv
            tot -= 2 * C * mv; vA, vB = 0.7 * tot, 0.3 * tot
        uA, uB = vA / pa[iD], vB / pb[iD]
        hi = ID[k + 1] if k + 1 < K else N
        nav[iD:hi] = uA * pa[iD:hi] + uB * pb[iD:hi]
    return dict(nav=nav, stats=stats(nav, npre), flow=flow)

def turnover(r, R):
    yrs, avg = r["stats"]["yrs"], np.mean([r["nav"][ID[k]] for k in range(K)])
    return R.sell_val.sum() / avg / yrs

# ================================================================ run both bases
def run_basis(basis):
    res = W.run_all(basis, "frozen")
    for n in ("B2", "B2-EW"):
        res[n] = run_b2(basis, n == "B2-EW")
    res["Blend"] = blend(res["B2"], res["S3"])
    res["Blend"]["to"] = 0.7 * turnover(res["B2"], res["B2"]["R"]) + 0.3 * turnover(res["S3"], res["S3"]["R"]) + res["Blend"]["flow"] / np.mean([res["Blend"]["nav"][ID[k]] for k in range(K)]) / res["Blend"]["stats"]["yrs"]
    return res
LAB = [("B0", "B0 (buy and hold EW)"), ("EW", "B0-monthly (EW rebal. monthly)"), ("B1", "B1"), ("S2", "S2"), ("S3", "S3"), ("S4", "S4"), ("B2", "B2 cap-wtd 12"), ("B2-EW", "B2-EW 12"), ("Blend", "70/30 B2+S3")]

def to_of(r, n):
    if n == "Blend": return r[n]["to"]
    return turnover(r[n], r[n]["R"])

def main():
    res = {k_: run_basis(b) for k_, b in BASIS.items()}
    kmi = BENCH["KMI All Share TR"]["stats"]["nav"]
    kmiv = kmi
    out("== WALK-FORWARD RE-BENCH, 18 Oct 2026. Frozen engine from scripts/walkforward.py; no rule changed. Deposits 106 x Rs50,000 = Rs5.3m, same dates for all rows.")
    out("ACCRUED is an ESTIMATE: before 1 Nov 2024 each holding-month adds 0.85 x (last published fiscal-year dividend yield in sa_ratios.csv, announcement or FYE+4m, whichever is later) / 12 to the name's return. Names outside sa_ratios (108 names) accrue 0. After Oct 2024 the actual corporate_actions table is used and nothing is accrued. The 94 cash rows before Nov 2024 are dropped from the accrued basis (replaced by the estimate).")
    out("STRICT 'accrued' leaves a name at 0 until its first published sa_ratios row (value data starts 2021-22). 'accrued_bf' (POST-HOC) backfills those months with the name's first published yield.")
    for t, acc_m in ACC.items():
        cov = pd.Series({m["F"].year: np.mean([acc_m[m["k"], cidx[s]] > 0 for s in m["U_all"]]) for m in M[::12]})
        out(f"Share of U(t) names with non-zero accrual, {t} (January of each year): " + ", ".join(f"{y}: {v:.0%}" for y, v in cov.items()) + f"; mean accrual annualised over names that accrue {acc_m[acc_m > 0].mean() * 12:.2%}")
    out("\n== A. LIKE-FOR-LIKE FINAL VALUES (Rs, 16 Oct 2026)")
    rows = []
    for n, lab in LAB:
        f, a, b = res["frozen"][n]["stats"], res["accrued"][n]["stats"], res["accrued_bf"][n]["stats"]
        rows.append(dict(strategy=lab, frozen_Rs=rs(f["nav"]), accrued_Rs=rs(a["nav"]), accrued_bf_Rs=rs(b["nav"]), frozen_vs_KMI=f"{f['nav'] / kmiv:.2f}", accrued_vs_KMI=f"{a['nav'] / kmiv:.2f}", accr_bf_vs_KMI=f"{b['nav'] / kmiv:.2f}"))
    for n, b in BENCH.items():
        rows.append(dict(strategy=n + " (no costs)", frozen_Rs=rs(b["stats"]["nav"]), accrued_Rs=rs(b["stats"]["nav"]), accrued_bf_Rs=rs(b["stats"]["nav"]), frozen_vs_KMI=f"{b['stats']['nav'] / kmiv:.2f}", accrued_vs_KMI=f"{b['stats']['nav'] / kmiv:.2f}", accr_bf_vs_KMI=f"{b['stats']['nav'] / kmiv:.2f}"))
    W.df_out(pd.DataFrame(rows))
    for basis in ("accrued", "accrued_bf", "frozen"):
        r = res[basis]
        out(f"\n== B. STATISTICS, {basis.upper()} basis (CAGR = TWR of unit value; IRR money-weighted; turnover = sells / average NAV / year)")
        rows = []
        for n, lab in LAB:
            s = r[n]["stats"]
            rows.append(dict(strategy=lab, final_Rs=rs(s["nav"]), x_dep=f"{s['nav'] / (K * DEP):.2f}", CAGR=pc(s["cagr"]), IRR=pc(s["irr"]), maxDD=pc(s["mdd"]), DD_trough=f"{s['mdd_date']:%Y-%m}", worst12m=pc(s["w12"]), w12_end=f"{s['w12_end']:%Y-%m}", turnover_pa=f"{to_of(r, n):.0%}"))
        for n, b in BENCH.items():
            s = b["stats"]
            rows.append(dict(strategy=n, final_Rs=rs(s["nav"]), x_dep=f"{s['nav'] / (K * DEP):.2f}", CAGR=pc(s["cagr"]), IRR=pc(s["irr"]), maxDD=pc(s["mdd"]), DD_trough=f"{s['mdd_date']:%Y-%m}", worst12m=pc(s["w12"]), w12_end=f"{s['w12_end']:%Y-%m}", turnover_pa="-"))
        W.df_out(pd.DataFrame(rows))
    ends = [dates[int(dates.searchsorted(pd.Timestamp(f"{y}-12-31"), side="right")) - 1] for y in range(2018, 2026)] + [LAST]
    def yearly(price):
        o, prev = [], None
        for d in ends:
            o.append(price.asof(d) / (price.asof(prev) if prev is not None else price.iloc[ID[0]]) - 1); prev = d
        return o
    for basis in ("accrued", "accrued_bf", "frozen"):
        out(f"\n== C. YEAR-BY-YEAR TWR, {basis.upper()} basis, vs KMI All Share TR (2018 from first trade; 2026 to 16 Oct)")
        tab = {"year": [d.year for d in ends], "KMI_TR": [pc(x) for x in yearly(BENCH["KMI All Share TR"]["stats"]["price"])]}
        for n, lab in LAB: tab[n] = [pc(x) for x in yearly(res[basis][n]["stats"]["price"])]
        W.df_out(pd.DataFrame(tab))
        out("Rs value at each year end, B2 / B2-EW / B0 / KMI TR:")
        rows = []
        for d in ends:
            i = dates.get_loc(d)
            rows.append(dict(date=f"{d:%Y-%m-%d}", B2=rs(res[basis]["B2"]["nav"][i]), B2_EW=rs(res[basis]["B2-EW"]["nav"][i]), B0=rs(res[basis]["B0"]["nav"][i]), KMI_TR=rs(BENCH["KMI All Share TR"]["nav"][i]), B2_vs_KMI=f"{res[basis]['B2']['nav'][i] / BENCH['KMI All Share TR']['nav'][i]:.2f}"))
        W.df_out(pd.DataFrame(rows))
    r = res["frozen"]["B2"]
    out("\n== D. B2 MEMBERSHIP")
    hist = r["hist"]
    ch = [len(b[1] - a[1]) for a, b in zip(hist, hist[1:])]
    out(f"Target reviews {len(hist)} (quarterly plus forced by a KMI deletion). Names entering the top 12 per review: mean {np.mean(ch):.2f}, max {max(ch)}, reviews with no change {sum(c == 0 for c in ch)}. Distinct names ever in the top 12: {len(set().union(*[h[1] for h in hist]))}. KMI-deletion sells: {r['dele']}.")
    out("Top-12 set by year-end review: " + "; ".join(f"{h[0]:%Y-%m}: {' '.join(sorted(h[1]))}" for h in hist if h[0].month == 12))
    R = r["R"]; val = {s: p["u"] * R.T[-1, p["c"]] for s, p in R.pos.items()}; tot = sum(val.values())
    last_t = targets(K - 1)[1]
    out(f"Holdings on {LAST.date()} (weight in book / current target weight; target from the Sep 2026 formation): " + ", ".join(f"{s} {v / tot:.1%}/{last_t.get(s, 0):.1%}" for s, v in sorted(val.items(), key=lambda x: -x[1])))
    out("Size proxy is 60-day median traded value (no share counts), so it favours heavily traded names over the largest by free-float cap. Weights are traded-value weights capped at 15%, not index weights.")
    (ROOT / "tests/out/walkforward_rebench.txt").write_text(buf.getvalue(), encoding="utf-8")

if __name__ == "__main__":
    main()
