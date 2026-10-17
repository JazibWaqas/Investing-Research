"""Survivorship estimate: equal-weight liquid basket 2017-2026 with and without delisted names (data/prices_delisted).
Run: .venv/Scripts/python.exe scripts/survivorship.py"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import prices as P

ROOT = P.ROOT
close, vol, tv = P.load_panel()
d = pd.read_csv(ROOT / "data/delistings.csv")
d = d[d.price_file]
dc, dv = {}, {}
for s in d.symbol:
    x = pd.read_csv(ROOT / f"data/prices_delisted/{s}.csv", parse_dates=["date"], index_col="date")
    x = x[~x.index.duplicated(keep="last")].sort_index()
    dc[s], dv[s] = x.close, x.volume
dc, dv = pd.DataFrame(dc).reindex(close.index), pd.DataFrame(dv).reindex(close.index)
inside = dv.notna().cummax() & dv[::-1].notna().cummax()[::-1]
dv = dv.where(~(inside & dv.isna()), 0.0)
obs = (dv > 0) & (dc > 0)
dc = dc.where(obs)
C, V = pd.concat([close, dc], axis=1), pd.concat([vol, dv], axis=1)
T = (C * V).fillna(0).where(V.notna())
R = P.returns(C, "crude", vol=V)
cols = list(close.columns)
w, wo = P.ew_market(R, tv=T), P.ew_market(R[cols], tv=T[cols])
a, b = "2017-01-01", "2026-10-16"
cum = lambda r: (1 + r.loc[a:b].fillna(0)).prod() - 1
yrs = (pd.Timestamp(b) - pd.Timestamp(a)).days / 365.25
ann = lambda r: (1 + cum(r)) ** (1 / yrs) - 1
print(f"EW liquid basket {a}..{b}: without delisted cum {cum(wo):.1%} ann {ann(wo):.2%}; with {cum(w):.1%} ann {ann(w):.2%}; gap {ann(wo)-ann(w):.2%}/yr")
# per-name: return from start of last full calendar year to last price (liquid names only: trailing median tv > 5e6 at start)
rows = []
for s in dc.columns:
    p = dc[s].dropna()
    if p.empty: continue
    end = p.index[-1]
    y0 = pd.Timestamp(year=end.year - 1, month=1, day=1)
    q = p[p.index >= y0]
    if len(q) < 20 or q.index[0] > y0 + pd.Timedelta(days=45): continue
    r = R[s].loc[y0:end].fillna(0)
    rows.append((s, end.date(), (1 + r).prod() - 1, T[s].loc[:y0].tail(60).median()))
x = pd.DataFrame(rows, columns=["symbol", "last", "ret_last_full_year_to_end", "med_tv_60d"])
x.to_csv(ROOT / "data/delisted_last_year_returns.csv", index=False)
l = x[x.med_tv_60d > 5e6]
print("all names n", len(x), "median", x.ret_last_full_year_to_end.median(), "mean", x.ret_last_full_year_to_end.mean())
print("liquid-at-start n", len(l), "median", l.ret_last_full_year_to_end.median(), "mean", l.ret_last_full_year_to_end.mean())
# how many delisted names ever enter the liquid basket
liq = (P._med_tv(T) > 5e6)[list(dc.columns)].loc[a:b]
print("delisted names ever in basket:", int(liq.any().sum()), "mean names in basket/day delisted vs all:", liq.sum(axis=1).mean(), (P._med_tv(T)>5e6).loc[a:b].sum(axis=1).mean())
yr = lambda r: (1 + r.fillna(0)).groupby(r.index.year).prod() - 1
print(pd.DataFrame({"without": yr(wo.loc[a:b]), "with": yr(w.loc[a:b])}).assign(gap=lambda t: t["without"] - t["with"]).round(3))
