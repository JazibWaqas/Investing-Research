"""Exploratory: at 17 sessions after each market low, which liquid names doubled within 252 sessions, and what did they look like at t0?
Features known at t0: latest y/y quarterly net-income growth announced by t0 (quarterly_eps.csv, announce_dt or period end + 60 days),
distance below the 252-session high, 60-session return, prior-cycle multiple (winners_library runs that peaked before t0), liquidity."""
import pandas as pd, numpy as np, os
os.chdir(r"c:\Users\JazibWaqas\Documents\GitHub\Investing-Research")
adj = pd.read_parquet("data/panel_close_adj.parquet")
vol = pd.read_parquet("data/panel_volume.parquet").reindex(index=adj.index, columns=adj.columns)
raw = pd.read_parquet("data/panel_close.parquet").reindex(index=adj.index, columns=adj.columns)
tv = (raw * vol).rolling(60, min_periods=40).median()
q = pd.read_csv("data/fundamentals/quarterly_eps.csv")
q["pe"] = pd.to_datetime(q.fiscal_quarter_end); q["avail"] = pd.to_datetime(q.announce_dt.str[:10], errors="coerce").fillna(q.pe + pd.Timedelta(days=60))
w = pd.read_csv("data/winners_library.csv", parse_dates=["start_date", "peak_date"])
lows = {"2020": "2020-03-25", "2023": "2023-06-23", "2024": "2024-06-11", "2025": "2025-04-30"}
idx = adj.index; out = []
for lab, d in lows.items():
    t0 = idx[idx.searchsorted(pd.Timestamp(d)) + 17]; i0 = idx.get_loc(t0)
    for s in adj.columns:
        c = adj[s]
        if pd.isna(c.iloc[i0]) or pd.isna(tv[s].iloc[i0]) or tv[s].iloc[i0] < 20e6: continue
        fut = c.iloc[i0 + 1:i0 + 253].dropna()
        if len(fut) < 100: continue
        mult = fut.max() / c.iloc[i0]
        hist = c.iloc[max(0, i0 - 252):i0 + 1].dropna()
        qq = q[(q.symbol == s) & (q.avail <= t0)].sort_values("pe")
        g = np.nan
        if len(qq):
            last = qq.iloc[-1]; ya = qq[qq.pe == last.pe - pd.DateOffset(years=1)]
            if len(ya) and ya.net_income.iloc[0] > 0: g = last.net_income / ya.net_income.iloc[0] - 1
        prior = w[(w.symbol == s) & (w.peak_date < t0) & (w.peak_date > t0 - pd.DateOffset(years=4))].multiple.max()
        out.append(dict(ep=lab, sym=s, doubled=mult >= 2, mult=mult, ni_g=g, vshi=c.iloc[i0] / hist.max() - 1,
                        r60=c.iloc[i0] / c.iloc[max(0, i0 - 60)] - 1, prior=prior if pd.notna(prior) else 1.0))
R = pd.DataFrame(out)
print("liquid names per episode and doublers within 12 months:")
print(R.groupby("ep").agg(n=("sym", "size"), doubled=("doubled", "sum"), rate=("doubled", "mean")).round(2).to_string())
print("\ndoublers:", {ep: list(g[g.doubled].sort_values("mult", ascending=False).sym) for ep, g in R.groupby("ep")})
def rate(mask, lab):
    x = R[mask]; print(f"  {lab:46s} n {len(x):4d}  doubled {x.doubled.mean():5.0%}  median best multiple {x.mult.median():.2f}")
print("\nDoubling rate by feature at t0 (all four episodes pooled):")
rate(R.ni_g.notna(), "has earnings data")
rate(R.ni_g >= 0.3, "latest profit growth >= +30%")
rate((R.ni_g >= 0) & (R.ni_g < 0.3), "profit growth 0 to +30%")
rate(R.ni_g < 0, "profit falling")
rate(R.prior >= 2.0, "prior-cycle run of 2x+ (peaked within 4 years)")
rate(R.prior < 2.0, "no prior 2x run")
rate(R.vshi <= -0.35, "35%+ below its 1-year high")
rate((R.vshi > -0.35) & (R.vshi <= -0.15), "15% to 35% below")
rate(R.vshi > -0.15, "within 15% of its high")
rate(R.r60 >= 0.15, "already up 15%+ in 60 sessions")
rate((R.ni_g >= 0.3) & (R.vshi > -0.35), "profit +30% and within 35% of high")
rate((R.ni_g >= 0.3) & (R.prior >= 2), "profit +30% and prior 2x run")
rate(R.index >= 0, "everything (base rate)")
