"""Apply the table through prices.returns('adjusted') logic, report which suspected gaps are explained, write panel_close_adj.parquet."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import common
from common import ROOT
import prices

close, vol, tv = common.panel()
actions = prices.load_actions()
pct0, prev, gap, vratio, big0 = prices._moves(close, vol)


def adjust(actions):
    mult, cash = pd.DataFrame(1.0, close.index, close.columns), pd.DataFrame(0.0, close.index, close.columns)
    applied = pd.DataFrame(False, close.index, close.columns)
    for r in actions.itertuples():
        if r.symbol not in close.columns:
            continue
        col = close[r.symbol].dropna().index
        k = col.searchsorted(r.ex_date)
        if k == 0 or k >= len(col):
            continue
        t = col[k]
        applied.at[t, r.symbol] = True
        if r.type == "cash":
            cash.at[t, r.symbol] += r.value
        elif r.type == "bonus":
            mult.at[t, r.symbol] *= 1 + r.value
        elif r.type == "split":
            mult.at[t, r.symbol] *= r.value
    pct = (close * mult + cash) / prev - 1
    big = (pct.abs() > prices.BIG_PCT).where(prev > 10, (pct * prev).abs() > prices.BIG_RS) & close.notna() & prev.notna()
    return pct, big, applied


pct1, big1, applied = adjust(actions)
sus = pd.read_csv(prices.SUSPECTS, parse_dates=["date"])
sus["applied"] = [bool(applied.at[d, s]) if d in applied.index and s in applied.columns else False for s, d in zip(sus.symbol, sus.date)]
sus["still_big"] = [bool(big1.at[d, s]) for s, d in zip(sus.symbol, sus.date)]
sus["explained"] = sus.applied & ~sus.still_big
sus["pct_after"] = [pct1.at[d, s] for s, d in zip(sus.symbol, sus.date)]
med = prices._med_tv(tv)
sus["liquid"] = [bool(med.at[d, s] > 5e6) if d in med.index and pd.notna(med.at[d, s]) else False for s, d in zip(sus.symbol, sus.date)]
sus["mtv_m"] = [round(med.at[d, s] / 1e6, 1) if d in med.index and pd.notna(med.at[d, s]) else np.nan for s, d in zip(sus.symbol, sus.date)]

def adj_panel(act):
    """Back-adjusted close level: obs-to-obs returns from prices.returns('adjusted') chained and scaled so the last close equals the raw last close."""
    ret = prices.returns(close, "adjusted", vol=vol, actions=act)
    out = pd.DataFrame(np.nan, close.index, close.columns)
    for c in close.columns:
        s = close[c].dropna()
        if not len(s):
            continue
        r = ret[c].loc[s.index].fillna(0.0)
        lvl = (1 + r).cumprod()
        out.loc[s.index, c] = (lvl * (s.iloc[-1] / lvl.iloc[-1])).values
    return out, ret


# total-return panel: bonus, split and every cash dividend in the table; still-unexplained suspects zeroed as in 'crude'
adj, ret_tr = adj_panel(actions)
adj.to_parquet(ROOT / "data/panel_close_adj.parquet")
# price-return panel: bonus and split only (cash ignored). Cash coverage is thin before Nov 2024, so use this one for comparisons across years.
adj_px, ret_px = adj_panel(actions[actions.type != "cash"])
adj_px.to_parquet(ROOT / "data/panel_close_adj_pricereturn.parquet")

if __name__ == "__main__":
    print("suspects", len(sus), "explained", int(sus.explained.sum()), "applied but still big", int((sus.applied & sus.still_big).sum()), "unexplained", int((~sus.applied).sum()))
    liq = sus[sus.liquid]
    print("liquid suspects", len(liq), "explained", int(liq.explained.sum()), "unexplained", int((~liq.applied).sum()))
    print(sus.groupby(sus.date.dt.year).agg(n=("explained", "size"), expl=("explained", "sum")).T)
    for s, d in [("LUCK", "2025-04-28"), ("SYS", "2025-06-02"), ("SYS", "2022-03-31"), ("MEBL", "2022-08-22"), ("MEBL", "2021-09-09")]:
        d = pd.Timestamp(d)
        print(s, d.date(), "raw pct", round(pct0.at[d, s], 4), "adjusted pct", round(pct1.at[d, s], 4), "ret", round(ret.at[d, s], 4), "applied", bool(applied.at[d, s]))
