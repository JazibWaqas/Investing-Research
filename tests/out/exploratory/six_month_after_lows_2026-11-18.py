import pandas as pd, numpy as np, os
os.chdir(r"c:\Users\JazibWaqas\Documents\GitHub\Investing-Research")
adj = pd.read_parquet("data/panel_close_adj.parquet")
k = pd.read_csv("data/macro/kse100.csv", parse_dates=["date"]).sort_values("date").set_index("date").close
k200 = k.rolling(200).mean()
names = ["FCCL","MLCF","LUCK","DGKC","PIOC","OGDC","PPL","MARI","EFERT","FFC","ILP","MEBL","ENGROH","HUBC","GAL","GHNI","PAEL","SAZEW"]
H = 126
# analogue entry points: about 17 sessions after the market low of each turn (where we are now: low 23 Oct, today 18 Nov)
lows = {"Mar 2020": "2020-03-25", "Jun 2023": "2023-06-23", "Jun 2024": "2024-06-11", "Apr 2025 (shock)": "2025-04-30"}
idx = adj.index
def at(d, n): i = idx.searchsorted(pd.Timestamp(d)); return idx[min(i + n, len(idx) - 1)]
print("KSE100 on the same windows:", {lab: f"{100*(k[at(d,17)+pd.Timedelta(days=183):].iloc[0]/k[at(d,17):].iloc[0]-1):+.0f}%" for lab, d in lows.items() if at(d,17)+pd.Timedelta(days=183) < k.index[-1]})
rows = []
for s in names:
    if s not in adj: print("missing", s); continue
    c = adj[s].dropna()
    r = (c.shift(-H) / c - 1).dropna()
    r5 = r[r.index >= "2021-10-01"]
    up = (k > k200).reindex(r5.index).ffill().fillna(False)
    dd = []  # worst dip inside each 6-month hold (from entry), last 5 years
    row = dict(sym=s, p10=100*r5.quantile(.1), med=100*r5.median(), p90=100*r5.quantile(.9), med_up=100*r5[up].median(), win_up=(r5[up] > 0).mean())
    for lab, d in lows.items():
        t0 = at(d, 17)
        if t0 not in c.index: row[lab] = np.nan; continue
        i = c.index.get_loc(t0)
        if i + H >= len(c): row[lab] = np.nan; continue
        w = c.iloc[i:i + H + 1]
        row[lab] = f"{100*(w.iloc[-1]/w.iloc[0]-1):+.0f} (dip {100*(w.min()/w.iloc[0]-1):+.0f})"
    seg = c[c.index >= "2021-10-01"]
    worst = []
    for i in range(0, len(seg) - H, 5):
        w = seg.iloc[i:i + H]; worst.append(w.min() / w.iloc[0] - 1)
    row["typ_dip"] = 100 * np.median(worst); row["bad_dip"] = 100 * np.quantile(worst, .1)
    rows.append(row)
R = pd.DataFrame(rows).set_index("sym")
pd.set_option("display.width", 250)
print(R.round(1).to_string())
