"""Results-jump winner cases (knowledge/winners/ATRL_202211.md and seven others, plus _results_jumps.md):
entry and exit simulations, share-of-gain-ahead tables, and a population check of EPS-jump events (twins).
Run from the repo root: .venv/Scripts/python.exe -I scripts/tests/winners_results_jumps.py
Outputs: tests/out/winners_results_jumps_sims.txt, tests/out/winners_results_jumps_twins.txt.

Sim method: buy at the open of the session after the signal date (adjusted open = raw open x adj close / raw close,
falling back to the adjusted close if the open is missing); sell at the open of the session after a close that is the
stated fraction under the highest close since entry; cost 0.5% round trip; before tax; open positions are marked at the
last close (16 Oct 2026). Adjusted closes are total return (bonus, split, dividends). Lock days are not modelled: a buy at
a limit-up open may not fill (flagged in the case files). Twins: every quarterly EPS-jump event (EPS at least 1.5x the same
quarter a year earlier with a positive base, or loss to profit) from data/fundamentals/quarterly_eps.csv, 2021 on,
liquid names (median traded value over the prior 60 sessions above Rs5m), entry at the next session's adjusted close.
The EPS file is StockAnalysis data, not checked against filings, and covers 129 symbols (survivor-heavy, one bull market)."""
import numpy as np
import pandas as pd

P = pd.read_parquet("data/panel_close_adj.parquet")
R = pd.read_parquet("data/panel_close.parquet")
V = pd.read_parquet("data/panel_volume.parquet")
idx = P.index

CASES = {  # symbol: (low or start date, peak date, [signal dates], [stops])
    "ATRL": ("2022-11-28", "2026-10-16", ["2022-10-25", "2023-07-03", "2023-10-10", "2024-12-23", "2026-01-23"], [0.2, 0.25, 0.3, 0.4]),
    "FABL": ("2023-03-24", "2026-07-03", ["2023-04-28", "2023-12-05", "2024-02-07", "2025-08-28", "2026-01-06"], [0.2, 0.25, 0.3]),
    "ILP": ("2023-05-22", "2024-05-24", ["2023-04-18", "2023-06-09", "2023-07-03", "2023-09-22", "2023-10-30", "2023-12-01", "2024-02-23"], [0.2, 0.25, 0.3, 0.4]),
    "NETSOL": ("2023-05-26", "2024-07-18", ["2023-04-27", "2023-07-03", "2023-12-05", "2024-02-12", "2024-05-22"], [0.2, 0.25, 0.3]),
    "TELE": ("2025-05-08", "2025-10-23", ["2025-04-30", "2025-06-23", "2025-10-08", "2025-10-16"], [0.2, 0.25, 0.3]),
    "INIL": ("2025-05-08", "2025-09-15", ["2025-04-25", "2025-05-12", "2025-06-03", "2025-08-19"], [0.2, 0.25, 0.3]),
    "FCEPL": ("2026-03-09", "2026-09-01", ["2026-02-17", "2026-04-24", "2026-04-27", "2026-05-11", "2026-08-21"], [0.2, 0.25, 0.3]),
    "MACFL": ("2026-03-09", "2026-10-14", ["2026-04-29", "2026-04-30", "2026-05-13", "2026-06-15", "2026-09-02"], [0.2, 0.25, 0.3, 0.4]),
}


def opens(sym):
    r = pd.read_csv(f"data/prices_raw/{sym}.csv", parse_dates=["date"]).set_index("date").reindex(idx)
    return r.open.where(r.open > 0) * (P[sym] / R[sym]), r


def fwd(sym, signal):
    O, r = opens(sym)
    c = P[sym]
    si = idx.get_indexer([pd.Timestamp(signal)])[0]
    ei = si + 1
    ent = O.iloc[ei] if not np.isnan(O.iloc[ei]) else c.iloc[ei]
    out = {k: round(float(c.iloc[min(ei + k, len(idx) - 1)] / ent - 1), 3) for k in (5, 10, 20, 40, 60, 120)}
    out["mae20"] = round(float(c.iloc[ei:ei + 21].min() / ent - 1), 3)
    out["mae60"] = round(float(c.iloc[ei:ei + 61].min() / ent - 1), 3)
    print(f"{sym} signal {signal} close {c.iloc[si]:.2f} entry open {ent:.2f} (adj) forward returns by session {out}")


def sim(sym, signal, stop, cost=0.005):
    O, r = opens(sym)
    c = P[sym]
    si = idx.get_indexer([pd.Timestamp(signal)])[0]
    ei = si + 1
    ent = O.iloc[ei] if not np.isnan(O.iloc[ei]) else c.iloc[ei]
    hi = c.iloc[ei]
    last = len(idx) - 1
    exit_i, mdd = None, 0.0
    for i in range(ei, last + 1):
        if np.isnan(c.iloc[i]):
            continue
        hi = max(hi, c.iloc[i])
        mdd = min(mdd, c.iloc[i] / hi - 1)
        if c.iloc[i] <= hi * (1 - stop) and i < last:
            exit_i = i + 1
            break
    why = "stop"
    if exit_i is None:
        exit_i, px, why = last, c.iloc[last], "held to end (marked)"
    else:
        px = O.iloc[exit_i] if not np.isnan(O.iloc[exit_i]) else c.iloc[exit_i]
    net = (px / ent) * (1 - cost) - 1
    low = c.iloc[ei:exit_i + 1].min()
    print(f"  trail {stop:.0%}: buy {idx[ei].date()} {ent:.2f}, exit {idx[exit_i].date()} {px:.2f} ({why}), gross x{px / ent:.2f}, net {net:+.0%}, "
          f"worst close x{low / ent:.2f} of cost, max drop from high {mdd:.0%}, {exit_i - ei} sessions, Rs50k->{50000 * (1 + net):,.0f}, Rs200k->{200000 * (1 + net):,.0f}")


def sims():
    for sym, (a, b, sigs, stops) in CASES.items():
        c = P[sym]
        lo, pk = c[a], c[b]
        print(f"\n===== {sym}: low/start {a} {lo:.2f}, peak {b} {pk:.2f} (x{pk / lo:.2f}); last {c.iloc[-1]:.2f} = {100 * c.iloc[-1] / pk:.0f}% of peak")
        for d in sigs:
            v = c[:d].iloc[-1]
            print(f"\n-- signal {d}: adj close {v:.2f} = x{v / lo:.2f} of the low; peak/price x{pk / v:.2f}; share of log gain from the low still ahead {np.log(pk / v) / np.log(pk / lo):.2f}")
            fwd(sym, d)
            for s in stops:
                sim(sym, d, s)


def twins():
    Q = pd.read_csv("data/fundamentals/quarterly_eps.csv", parse_dates=["fiscal_quarter_end"])
    Q["ann"] = pd.to_datetime(Q.announce_dt, utc=True, errors="coerce").dt.tz_convert("Asia/Karachi")
    rows = []
    for s, g in Q.groupby("symbol"):
        if s not in P.columns:
            continue
        g = g.sort_values("fiscal_quarter_end").set_index("fiscal_quarter_end")
        for q, r in g.iterrows():
            j = g.index[np.abs((g.index - (q - pd.DateOffset(years=1))).days) <= 10]
            if len(j) == 0 or pd.isna(r.ann) or pd.isna(r.eps_basic):
                continue
            ep = g.loc[j[0], "eps_basic"]
            if pd.isna(ep):
                continue
            jump = (ep > 0 and r.eps_basic >= 1.5 * ep) or (ep <= 0 and r.eps_basic > 0)
            d = r.ann.tz_localize(None).normalize()
            if r.ann.hour * 60 + r.ann.minute > 15 * 60 + 30:
                d += pd.Timedelta(days=1)
            si = idx.searchsorted(d)
            if si >= len(idx) - 1:
                continue
            tv = (R[s] * V[s]).iloc[max(0, si - 60):si].median()
            c = P[s]
            ei = si + 1
            if np.isnan(c.iloc[ei]) or np.isnan(c.iloc[si]):
                continue
            e = c.iloc[ei]
            f = lambda k: c.iloc[ei + k] / e - 1 if ei + k < len(idx) else np.nan
            w, w2 = c.iloc[ei:ei + 21], c.iloc[ei:ei + 127]
            rows.append(dict(sym=s, d=idx[si], jump=jump, eps=r.eps_basic, ep=ep, tv=tv, r20=f(20), r60=f(60),
                             mae20=w.min() / e - 1 if len(w) >= 21 else np.nan,
                             run126=(w2.max() / e - 1 >= 0.5) if len(w2) >= 127 else np.nan, ok126=len(w2) >= 127))
    D = pd.DataFrame(rows)
    D = D[(D.d >= "2021-01-01") & (D.tv > 5e6)]
    print(f"liquid events 2021 on: {len(D)}; EPS-jump events: {int(D.jump.sum())}; symbols {D.sym.nunique()}")

    def summ(x, label):
        print(f"{label}: n {len(x)} | 20-session median {100 * x.r20.median():+.1f}%, win {100 * (x.r20 > 0).mean():.0f}% | 60-session median {100 * x.r60.median():+.1f}%, "
              f"win {100 * (x.r60 > 0).mean():.0f}% | worst close within 20 sessions at or under -15%: {100 * (x.mae20 <= -0.15).mean():.0f}% | "
              f"20-session return at or under -10%: {100 * (x.r20 <= -0.10).mean():.0f}% | +50% at some point within 126 sessions: "
              f"{100 * x[x.ok126].run126.astype(float).mean():.1f}% (n {int(x.ok126.sum())})")
    J = D[D.jump]
    summ(J, "EPS jump")
    summ(D[~D.jump], "other results")
    summ(J[((J.ep > 0) & (J.eps >= 3 * J.ep)) | (J.ep <= 0)], "jump 3x or loss to profit")
    summ(J[(J.ep > 0) & (J.eps < 3 * J.ep)], "jump 1.5x to 3x")
    for y in range(2021, 2027):
        x = J[J.d.dt.year == y]
        if len(x):
            summ(x, f"jump events {y}")


if __name__ == "__main__":
    import contextlib
    with open("tests/out/winners_results_jumps_sims.txt", "w", encoding="utf-8") as fh, contextlib.redirect_stdout(fh):
        sims()
    with open("tests/out/winners_results_jumps_twins.txt", "w", encoding="utf-8") as fh, contextlib.redirect_stdout(fh):
        twins()
