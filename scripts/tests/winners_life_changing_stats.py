"""winners_life_changing_stats: late-entry and exit arithmetic for the 34 runs of 5x or more in data/winners_library.csv (PHDL, a price rebase, excluded).
Run: .venv/Scripts/python.exe scripts/tests/winners_life_changing_stats.py  -> tests/out/winners_life_changing_stats.txt

DEFINITIONS (fixed before the results were read; one illustrative path per rule, not a backtest of a strategy: the 34 runs are selected because they ended up 5x or more).
 Prices: adjusted (total return) closes as scripts/tests/winners_population.py (panel_close_adj for survivors, crude chain for delisted names).
 Entry: the close of the session AFTER the signal. Signals: the library's first 252-day high (f252_date) and the first close at 2x the library start price.
 Exit rule A(x): sell at the close on which the close is x below the highest close since entry (x = 20%, 30%, 40%); if never hit, mark at the horizon.
 Rule R(x): as A(x), then buy again at the first close above the highest close reached before the sale, and repeat. Each sale and each purchase costs 0.25% (0.5% a round trip, data/costs.md).
 Horizon: 250 sessions after the peak, or the last trade. Capital gains tax is not deducted. Locks, gaps and illiquid exits are not modelled: a stop price is not a fill price.
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]; D = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

close_raw, vol, tv = P.load_panel(); CAL = close_raw.index
adj = pd.read_parquet(D / "panel_close_adj.parquet").reindex(index=CAL)
lib = pd.read_csv(D / "winners_library.csv")
lib = lib[(lib.multiple >= 5) & (lib.symbol != "PHDL")].sort_values("start_date")
COST = 0.0025


def series(sym, deleted):
    if sym in adj.columns and not deleted:
        return adj[sym].where(close_raw[sym].notna())
    x = pd.read_csv(D / "prices_delisted" / f"{sym}.csv", parse_dates=["date"], index_col="date")
    x = x[~x.index.duplicated(keep="last")].sort_index().reindex(CAL)
    c = x.close.where((x.volume > 0) & (x.close > 0))
    r = P.returns(c.to_frame("s"), "crude", vol=x.volume.to_frame("s"))["s"]
    lv = (1 + r.fillna(0)).cumprod().where(c.notna())
    return lv / lv.ffill().iloc[-1] * c.ffill().iloc[-1]


def final(a, k0, x, end, reenter):
    """a: ffilled closes; returns (final multiple of capital, number of stops)."""
    cap, held, pk, ref, n, entry = 1.0 - COST, True, a[k0], 0.0, 0, a[k0]
    for k in range(k0 + 1, end + 1):
        v = a[k]
        if held:
            pk = max(pk, v)
            if v <= pk * (1 - x):
                cap *= v / entry * (1 - COST); held = False; n += 1; ref = pk
                if not reenter: return cap, n
        else:
            if v > ref:
                held = True; pk = v; entry = v; cap *= 1 - COST
    if held: cap *= a[end] / entry * (1 - COST)
    return cap, n


rows = []
for r in lib.itertuples():
    s = series(r.symbol, r.delisted).ffill()
    last = int(np.flatnonzero(series(r.symbol, r.delisted).notna().values)[-1])
    a = s.values
    i0 = CAL.get_loc(pd.Timestamp(r.start_date)); ip = CAL.get_loc(pd.Timestamp(r.peak_date))
    end = min(ip + 250, last)
    out = dict(symbol=r.symbol, start=r.start_date, mult=round(r.multiple, 1), kmi=r.kmi, tier=r.liq_tier)
    for nm, k in [("f252", CAL.get_loc(pd.Timestamp(r.f252_date)) if isinstance(r.f252_date, str) else None),
                  ("x2", next((k for k in range(i0, ip + 1) if a[k] >= 2 * a[i0]), None))]:
        if k is None or k + 1 > end: continue
        k1 = k + 1
        out[nm + "_entry_x"] = round(a[k1] / a[i0], 2)
        out[nm + "_ahead"] = round(a[ip] / a[k1], 2)
        out[nm + "_hold_to_end"] = round(a[end] / a[k1] * (1 - 2 * COST) - 1, 2)
        for x in (0.2, 0.3, 0.4):
            m, n = final(a, k1, x, end, False); out[f"{nm}_A{int(x*100)}"] = round(m - 1, 2)
            m, n = final(a, k1, x, end, True); out[f"{nm}_R{int(x*100)}"] = round(m - 1, 2)
    rows.append(out)
df = pd.DataFrame(rows)
OUT = ROOT / "tests" / "out" / "winners_life_changing_stats.txt"
L = []
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 100)
L.append("Late-entry arithmetic, 34 runs of 5x or more (return on capital, after 0.5% round trip per trade, before tax; horizon = peak + 250 sessions)\n")
L.append(df.to_string(index=False)); L.append("")
for nm in ("f252", "x2"):
    L.append(f"--- entry at {nm}: n = {df[nm + '_A20'].notna().sum()}")
    L.append(f"peak still ahead of the entry close: median {df[nm + '_ahead'].median():.2f}x; entry close as a multiple of the library start: median {df[nm + '_entry_x'].median():.2f}x")
    for k in ("hold_to_end", "A20", "A30", "A40", "R20", "R30", "R40"):
        c = df[f"{nm}_{k}"].dropna()
        L.append(f"{k:12s} median {c.median():+.0%}  mean {c.mean():+.0%}  share positive {(c > 0).mean():.0%}  share >= +100% {(c >= 1).mean():.0%}  share <= -10% {(c <= -0.10).mean():.0%}  worst {c.min():+.0%}  n {len(c)}")
    L.append("")
ep = df[df.start >= "2022-10-01"]
L.append(f"2022-10 to 2023-11 cohort (n = {len(ep)}) vs 2017 to 2019 (n = {len(df) - len(ep)}), entry f252, A30 median: {ep.f252_A30.median():+.0%} vs {df[df.start < '2022-10-01'].f252_A30.median():+.0%}; A20 median {ep.f252_A20.median():+.0%} vs {df[df.start < '2022-10-01'].f252_A20.median():+.0%}")
# how often a closing trailing stop fires on the way up (entry at the f252 signal; stops counted up to the peak, re-entering on a reclaim)
cnt = {0.2: 0, 0.3: 0, 0.4: 0}; tot = {0.2: 0, 0.3: 0, 0.4: 0}; early = 0; nn = 0
for r in lib.itertuples():
    if not isinstance(r.f252_date, str): continue
    a = series(r.symbol, r.delisted).ffill().values
    ip = CAL.get_loc(pd.Timestamp(r.peak_date)); k1 = CAL.get_loc(pd.Timestamp(r.f252_date)) + 1
    nn += 1
    for x in cnt:
        m, n = final(a, k1, x, ip, True); cnt[x] += n > 0; tot[x] += n
    pk = a[k1]
    for k in range(k1 + 1, ip + 1):
        pk = max(pk, a[k])
        if a[k] <= pk * 0.8:
            early += a[k1:k + 1].max() < 1.5 * a[k1]; break
L.append(f"Stops firing before the peak (entry at the first 252-day high, n = {nn}): a 20% closing stop fired at least once in {cnt[0.2]} runs ({tot[0.2]} times in all), a 30% stop in {cnt[0.3]} ({tot[0.3]}), a 40% stop in {cnt[0.4]} ({tot[0.4]}). A 20% stop fired before the price had risen 50% above entry in {early} runs.")
OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
