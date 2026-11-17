import pandas as pd, numpy as np, os
os.chdir(r"c:\Users\JazibWaqas\Documents\GitHub\Investing-Research")
k = pd.read_csv("data/macro/kse100.csv", parse_dates=["date"]).sort_values("date").set_index("date").close
k200 = k.rolling(200).mean()
above = k > k200
# early recovery: index crossed above its 200-day within the last 30 sessions, after at least 60 sessions below
cross = above & ~above.shift(1, fill_value=False)
below_run = (~above).astype(int).groupby(above.cumsum()).cumsum().shift(1)
real_cross = cross & (below_run >= 60)
early = pd.Series(False, index=k.index)
for d in k.index[real_cross]:
    i = k.index.get_loc(d); early.iloc[i:i + 30] = True
print("crossings counted:", [d.date() for d in k.index[real_cross]])
a = pd.read_parquet("data/announcements.parquet")
a = a[a.klass == "financial_result"].copy(); a["d"] = a.datetime.dt.tz_localize(None).dt.normalize()
kmi = pd.read_csv("data/kmi_allshare_2026-06-05.csv").symbol.str.replace(r"(XD|XB|XR)$", "", regex=True)
recs = []
for s in kmi:
    p = f"data/prices_raw/{s}.csv"
    if not os.path.exists(p): continue
    d = pd.read_csv(p, parse_dates=["date"]).sort_values("date").set_index("date")
    if len(d) < 300: continue
    c, v = d.close, d.volume
    r = c.pct_change(); vx = v / v.rolling(20).median().shift(1); tv = (c * v).rolling(60).median().shift(1)
    sig = (r >= 0.04) & (r < 0.5) & (vx >= 2) & (tv > 20e6)
    res_days = set(a[a.symbol == s].d)
    for t0 in c.index[sig]:
        i = c.index.get_loc(t0)
        if i + 10 >= len(c): continue
        has_res = any((t0 - pd.Timedelta(days=x)) in res_days for x in range(0, 6))
        recs.append(dict(sym=s, date=t0, early=bool(early.reindex([t0]).fillna(False).iloc[0]), up=bool(above.reindex([t0]).fillna(False).iloc[0]), res=has_res,
                         r3=c.iloc[i + 3] / c.iloc[i] - 1 - 0.005, r10=c.iloc[i + 10] / c.iloc[i] - 1 - 0.005,
                         k10=k.reindex(c.index).ffill().iloc[i + 10] / k.reindex(c.index).ffill().iloc[i] - 1))
R = pd.DataFrame(recs); R = R[R.date >= "2017-01-01"]
R["ex10"] = R.r10 - R.k10
def show(x, lab):
    if len(x) == 0: print(f"{lab:48s} n 0"); return
    print(f"{lab:48s} n {len(x):5d}  names-months {x.groupby([x.sym, x.date.dt.to_period('M')]).ngroups:4d}  3d median {100 * x.r3.median():+5.1f}%  10d median {100 * x.r10.median():+5.1f}%  win10 {(x.r10 > 0).mean():.0%}  vs index 10d median {100 * x.ex10.median():+5.1f}  worst10 {100 * x.r10.min():+5.0f}%")
print("Signal: close +4% or more on 2x the 20-day median volume, liquid (>Rs20m/day) KMI names, after 0.5% cost")
show(R, "all signals 2017-2026")
show(R[~R.early & ~R.up], "index below its 200-day")
show(R[~R.early & R.up], "index above its 200-day (not early)")
show(R[R.early], "first 30 sessions after a 200-day recross")
show(R[R.early & R.res], "  ... and a results filing within 5 days")
show(R[R.early & ~R.res], "  ... no results filing")
show(R[~R.early & R.res], "other times, with a results filing")
print("\nEarly-window signals by episode")
for d0 in k.index[real_cross]:
    x = R[(R.date >= d0) & (R.date < d0 + pd.Timedelta(days=45))]
    if len(x): print(f"  {d0.date()}  n {len(x):3d}  10d median {100 * x.r10.median():+5.1f}%  win {(x.r10 > 0).mean():.0%}  vs index {100 * x.ex10.median():+5.1f}")
