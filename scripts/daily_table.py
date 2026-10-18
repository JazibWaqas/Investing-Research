"""Daily feature + forward-outcome table, one row per (symbol, session the symbol traded), 2017-01-02 to 2026-10-16.
Run: .venv/Scripts/python.exe scripts/daily_table.py   ->  data/daily_table.parquet/year=YYYY/
Columns and definitions: data/DAILY_TABLE_NOTES.md.
Anti-leak rule: every feature column is built only from arrays at index <= t (rolling / shift(+k)); every outcome column
only from arrays at index > t (shift(-k)); validate.py-style checks live in scripts/daily_table_check.py.
"""
import ast
import os
import warnings
import re
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prices import load_panel, returns  # noqa: E402

D = ROOT / "data"
warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
START = pd.Timestamp("2017-01-02")
KL = ["financial_result", "dividend_or_bonus", "material_info", "insider_trade", "board_meeting_notice", "agm", "credit_rating", "other"]
FKEYS = KL + ["insider_buy", "insider_sell"]
FW, MF = [1, 2, 3, 5, 10, 20, 60], [1, 3, 5, 10, 20]
CUT = pd.Timedelta(hours=15, minutes=30)   # filings after 15:30 count on the next session

close0 = load_panel()[0]
CAL = close0.index
if os.environ.get("DT_TRUNC"):   # leak test: rebuild with history cut at this date (see scripts/daily_table_check.py)
    CAL = CAL[CAL <= pd.Timestamp(os.environ["DT_TRUNC"])]
N = len(CAL)
IDX = np.arange(N)
# daily price limit in force (read off the data in tests/volume_ignition_upper_locks.py): 5% to Mar 2020, 7.5% to 5 Jul 2024, 10% after
LIM = pd.Series(np.where(CAL < pd.Timestamp("2020-03-30"), 0.05, np.where(CAL < pd.Timestamp("2024-07-08"), 0.075, 0.10)), CAL)


# ---------------- raw OHLCV: survivors (prices_raw) + delisted, delisted duplicates of another symbol dropped
def rd(f):
    x = pd.read_csv(f, usecols=["date", "open", "high", "low", "close", "volume"], parse_dates=["date"], index_col="date")
    return x[~x.index.duplicated(keep="last")].sort_index()


raw = {f.stem: rd(f) for f in sorted((D / "prices_raw").glob("*.csv"))}
dl = {f.stem: rd(f) for f in sorted((D / "prices_delisted").glob("*.csv")) if f.stem not in raw}
dl = {s: x for s, x in dl.items() if len(x)}
surv = set(raw)
seen = pd.DataFrame({s: x.close for s, x in raw.items()}).reindex(CAL)
for s in list(dl):
    c = dl[s].close.reindex(CAL)
    both = seen.notna() & c.notna().values[:, None]
    n = both.sum().values
    same = ((seen.values == c.values[:, None]) & both.values).sum(0)
    if ((same >= 0.9 * n) & (n >= 100)).any():
        del dl[s]
    else:
        seen[s] = c
ALL = {**raw, **dl}
print(f"{len(raw)} survivors + {len(dl)} delisted (after duplicate removal)")

adj = pd.read_parquet(D / "panel_close_adj.parquet").reindex(index=CAL)
adjpr = pd.read_parquet(D / "panel_close_adj_pricereturn.parquet").reindex(index=CAL)


def crude_level(x):
    """delisted names: price level chained from prices.returns(..., 'crude'), scaled to end at the last raw close"""
    c = x.close.where((x.volume > 0) & (x.close > 0))
    r = returns(c.to_frame("s"), "crude", vol=x.volume.to_frame("s"))["s"]
    lv = (1 + r.fillna(0)).cumprod().where(c.notna())
    return lv / lv.ffill().iloc[-1] * c.ffill().iloc[-1]


# ---------------- announcements -> per-session counts (session = first session on/after the filing's effective date)
an = pd.read_parquet(D / "announcements.parquet")
dt = an.datetime.dt.tz_convert("Asia/Karachi").dt.tz_localize(None)
eff = (dt - CUT).dt.normalize() + pd.Timedelta(days=1)   # at/before 15:30 -> that date, after -> next date
an["sess"] = CAL.searchsorted(eff.values)
an = an[(an.sess < N) & an.symbol.isin(ALL)].copy()
an["kk"] = an.klass.where(an.klass.isin(KL), "other")
ins = an.klass == "insider_trade"
an2 = pd.concat([an, an[ins & (an.direction == "buy")].assign(kk="insider_buy"), an[ins & (an.direction == "sell")].assign(kk="insider_sell")])
FC = {s: g.groupby(["sess", "kk"]).size().unstack(fill_value=0).reindex(index=range(N), columns=FKEYS, fill_value=0)
      for s, g in an2.groupby("symbol")}
ZERO_F = pd.DataFrame(0, index=range(N), columns=FKEYS)

# ---------------- macro
kmi = pd.read_csv(D / "macro/kmiallshr.csv", parse_dates=["date"]).set_index("date").reindex(CAL)
kc, ko = kmi.close.ffill(), kmi.open.values
tb = pd.read_csv(D / "macro/tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"]).set_index("date").y6m
pr = pd.read_csv(D / "macro/policy_rate_decisions.csv", parse_dates=["date"]).set_index("date").rate
spread = tb.reindex(tb.index.union(CAL)).ffill().reindex(CAL) - pr.reindex(pr.index.union(CAL)).ffill().reindex(CAL)
REGIME = np.where(spread.isna(), None, np.where(spread > 0, "bill>policy", "bill<=policy"))

# KMI All Share membership snapshots: derived lists from Jan 2019 plus the exact list of 5 Jun 2026 (last on ties)
snaps = sorted(((pd.Timestamp(re.search(r"(\d{4}-\d{2}-\d{2})", f.name).group(1)), "derived" not in f.name, set(pd.read_csv(f).symbol))
                for f in (D / "index_members").glob("KMI_ALL_*.csv") if "derived" in f.name or "2026-06-05" in f.name), key=lambda z: z[:2])
SNAP_AT = np.searchsorted([z[0] for z in snaps], CAL.values, "right") - 1

# sectors: the S dict in sector_momentum.py (importing the script would run it)
src = (ROOT / "scripts/sector_momentum.py").read_text()
a0 = src.index("S = {") + 4
SECT = ast.literal_eval(src[a0:src.index("\n}", a0) + 2])
SEC = {t: sec for sec, names in SECT.items() for t in names.split()}


def first_after(flag, w, last):
    """offset (1 = next calendar session) of the first True at index > t and <= t+w; NaN if none or the window passes `last`"""
    pos = np.flatnonzero(flag)
    i = np.searchsorted(pos, IDX, "right")
    off = np.where(i < len(pos), pos[np.minimum(i, len(pos) - 1)] - IDX, np.nan) if len(pos) else np.full(N, np.nan)
    return np.where((off <= w) & (IDX + w <= last), off, np.nan)


# ---------------- pass 1: per-symbol features and outcomes
rows, R1, R5, LIQ = {}, {}, {}, {}
for s, x0 in ALL.items():
    x = x0.reindex(CAL)
    tr = ((x.volume > 0) & (x.close > 0)).values
    if tr.sum() < 5:
        continue
    first, last = np.flatnonzero(tr)[[0, -1]]
    x.loc[~tr, ["open", "high", "low", "close"]] = np.nan
    x[["open", "high", "low"]] = x[["open", "high", "low"]].where(x[["open", "high", "low"]] > 0)   # zero open/high/low = missing in the feed
    x["volume"] = x.volume.where(tr, 0.0)
    x.iloc[:first, x.columns.get_loc("volume")] = np.nan
    x.iloc[last + 1:, x.columns.get_loc("volume")] = np.nan
    cl, trs = x.close, pd.Series(tr, CAL)
    if s in surv and adj[s].notna().sum() > 0:
        A = adj[s].where(tr)
        fac = (cl / adjpr[s].where(tr)).ffill().bfill().fillna(1.0)   # undo bonus/split in volume so a bonus is not a volume ignition
    else:
        A = crude_level(x).where(tr)
        fac = pd.Series(1.0, CAL)
    Af = A.ffill()
    Af.iloc[last + 1:] = np.nan
    f = A / cl
    o_adj, h_adj, l_adj = x.open * f, x.high * f, x.low * f
    vadj = x.volume * fac
    tv = (cl * x.volume).fillna(0).where(x.volume.notna())
    prev_obs = cl.ffill().shift(1)
    prev_A = Af.shift(1)

    d = pd.DataFrame(index=CAL)
    d["symbol"], d["close"] = s, cl
    d["ret_1d"] = Af / prev_A - 1
    d["ret_open_to_close"] = cl / x.open - 1
    d["gap_open"] = o_adj / prev_A - 1
    for k in (3, 5, 20, 60, 126):
        d[f"ret_{k}d"] = Af / Af.shift(k) - 1
    d["dist_252_high"] = Af / Af.rolling(252, min_periods=126).max() - 1
    d["dist_252_low"] = Af / Af.rolling(252, min_periods=126).min() - 1
    d["vol_ratio_20_120"] = vadj.rolling(20, min_periods=15).mean() / vadj.shift(20).rolling(120, min_periods=100).mean().where(lambda z: z > 0)
    d["vol_ratio_1_20"] = vadj / vadj.shift(1).rolling(20, min_periods=15).mean().where(lambda z: z > 0)
    d["traded_value_median_60"] = tv.rolling(60, min_periods=40).median().shift(1)   # window ends the day before t, as in prices.py
    # locks: close at the era's limit, measured against the previous OBSERVED close; under Rs20 the band is wider, so a floor and a 30% cap
    rr, ra, cheap = cl / prev_obs, A / A.ffill().shift(1), prev_obs < 20
    d["upper_lock"] = ((rr >= (1 + LIM) * 0.995) & (rr <= np.where(cheap, 1.3, (1 + LIM) * 1.015))) & trs
    d["lower_lock"] = ((ra <= (1 - LIM) * 1.005) & (ra >= np.where(cheap, 0.6, (1 - LIM) * 0.985))) & trs
    upf = d.upper_lock.astype(float)
    d["locks_up_5d"], d["locks_up_10d"] = upf.rolling(5).sum(), upf.rolling(10).sum()
    ob = ((Af > prev_A) & trs)[tr]
    d["consecutive_up_days"] = ob.groupby((~ob).cumsum()).cumsum().reindex(CAL)
    # filings known at t
    fc = FC.get(s, ZERO_F)
    for k in FKEYS:
        d[f"f_{k}"] = fc[k].values
    d["f_total"] = fc[KL].sum(axis=1).values
    lastf = pd.Series(np.where(d.f_total > 0, IDX, np.nan), CAL).ffill()
    d["days_since_last_filing"] = IDX - lastf.values
    d["next_board_meeting_known"] = pd.Series(fc.board_meeting_notice.values, CAL).rolling("30D").sum().values > 0
    d["sector"] = SEC.get(s, "other")
    d["index_ret_1d"], d["index_ret_5d"] = (kc / kc.shift(1) - 1).values, (kc / kc.shift(5) - 1).values
    d["regime"], d["regime_spread"] = REGIME, spread.values
    d["kmi_member"] = pd.array([(s in snaps[i][2]) if i >= 0 else None for i in SNAP_AT], dtype="boolean")
    d["liquid"] = d.traded_value_median_60 > 5e6

    # outcomes: strictly after t. Entry = open of the first session the stock trades after t.
    e = pd.Series(np.where(tr, IDX, np.nan), CAL).bfill().shift(-1).values   # NaN if never trades again
    ei = np.nan_to_num(e, nan=0).astype(int)
    has = ~np.isnan(e)
    d["next_open"] = pd.Series(o_adj.values[ei], CAL).where(has)
    ko_e = pd.Series(ko[ei], CAL).where(has)
    for k in FW:
        ok = (e <= IDX + k) & (IDX + k <= last)
        d[f"ret_fwd_{k}"] = (Af.shift(-k) / d.next_open - 1).where(ok)
        d[f"kmi_ret_fwd_{k}"] = (kc.shift(-k) / ko_e - 1).where(ok)
    for k in MF:
        ok = (e <= IDX + k) & (IDX + k <= last)
        d[f"mfe_{k}"] = (h_adj.shift(-1)[::-1].rolling(k, min_periods=1).max()[::-1] / d.next_open - 1).where(ok)
        d[f"mae_{k}"] = (l_adj.shift(-1)[::-1].rolling(k, min_periods=1).min()[::-1] / d.next_open - 1).where(ok)
    d["first_upper_lock_within_3"] = first_after(d.upper_lock.values, 3, last)
    d["first_upper_lock_within_5"] = first_after(d.upper_lock.values, 5, last)
    d["first_red_day"] = first_after(((Af < prev_A) & trs).values, 60, last)
    for k in (5, 10, 20):
        okw = IDX + k <= last
        for key in KL + ["total"]:   # filings in sessions t+1 .. t+k
            d[f"filing_within_{k}_{key}"] = d[f"f_{key}"][::-1].shift(1).rolling(k, min_periods=k).sum()[::-1].where(okw)
    R1[s], R5[s], LIQ[s] = d.ret_1d.where(tr), d.ret_5d.where(tr), d.liquid & tr
    d["session_idx"] = IDX
    rows[s] = d[tr & (CAL >= START)]
print("pass 1 done:", len(rows), "symbols")

# ---------------- sector return (equal weight of liquid peers, self excluded; liquid and traded that day; |move| capped as data-break guard)
R1, R5, LIQ = pd.DataFrame(R1), pd.DataFrame(R5), pd.DataFrame(LIQ)
R1, R5 = R1.where(LIQ & (R1.abs() < 0.5)), R5.where(LIQ & (R5.abs() < 1.0))
grp = {}
for g in SECT:
    cols = [c for c in R1.columns if SEC.get(c) == g]
    if cols:
        grp[g] = (R1[cols].sum(axis=1), R1[cols].count(axis=1), R5[cols].sum(axis=1), R5[cols].count(axis=1))
out = []
for s, d in rows.items():
    g = SEC.get(s)
    if g in grp:
        s1, c1, s5, c5 = (z.reindex(d.index) for z in grp[g])
        a1, a5 = R1[s].reindex(d.index), R5[s].reindex(d.index)
        n1, n5 = c1 - a1.notna(), c5 - a5.notna()
        d["sector_ret_1d"] = (s1 - a1.fillna(0)) / n1.where(n1 > 0)
        d["sector_ret_5d"] = (s5 - a5.fillna(0)) / n5.where(n5 > 0)
    else:
        d["sector_ret_1d"] = d["sector_ret_5d"] = np.nan
    d["is_newsless_rise"] = (d.ret_5d > 0.08) & (d.days_since_last_filing > 10) & (d.sector_ret_5d.fillna(d.index_ret_5d) < 0.03)
    out.append(d)
T = pd.concat(out).reset_index(names="date")
T["year"] = T.date.dt.year.astype("int16")
T["session_idx"] = T.session_idx.astype("int32")
for c in T.columns:
    if c.startswith("f_"):
        T[c] = T[c].astype("int16")
    elif T[c].dtype == "float64":
        T[c] = T[c].astype("float32")
T = T.sort_values(["symbol", "date"]).reset_index(drop=True)
dest = Path(os.environ.get("DT_OUT", D / "daily_table.parquet"))
if dest.exists():
    shutil.rmtree(dest)
ds.write_dataset(pa.Table.from_pandas(T, preserve_index=False), dest, format="parquet", partitioning=["year"],
                 partitioning_flavor="hive")
print(f"wrote {len(T):,} rows x {T.shape[1]} cols, {T.memory_usage(deep=True).sum() / 1e9:.2f} GB in memory -> {dest}")
