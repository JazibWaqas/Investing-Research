"""Independent point-in-time OHLCV loader for the Codex event studies.

Raw PSX closes are unadjusted. A >10.5% daily close change when the prior
close exceeds Rs10 is neutralized and recorded, a deliberately coarse proxy
for corporate actions. No dividend cash flows are added.
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
END = pd.Timestamp("2026-10-16")


def load_prices():
    paths = {p.stem.upper(): p for p in (ROOT / "seed/data/prices").glob("*.csv")}
    paths.update({p.stem.upper(): p for p in (ROOT / "data/prices_raw").glob("*.csv")})
    closes, values, action_rows = {}, {}, []
    for symbol, path in sorted(paths.items()):
        try:
            x = pd.read_csv(path, usecols=["date", "close", "volume"], parse_dates=["date"])
        except (ValueError, pd.errors.EmptyDataError):
            continue
        x = x.dropna(subset=["date", "close"]).drop_duplicates("date", keep="last")
        x = x[(x.date <= END) & (x.close > 0)].sort_values("date").set_index("date")
        if x.empty:
            continue
        c = x.close.astype(float)
        raw_ret = c.pct_change(fill_method=None)
        flagged = raw_ret.abs().gt(.105) & c.shift().gt(10)
        for date, value in raw_ret[flagged].items():
            action_rows.append((symbol, date.strftime("%Y-%m-%d"), float(value)))
        closes[symbol] = c
        values[symbol] = (c * x.volume.clip(lower=0)).astype(float)
    close = pd.DataFrame(closes).sort_index()
    traded_value = pd.DataFrame(values).reindex(close.index)
    ret = close.pct_change(fill_method=None)
    mask = ret.abs().gt(.105) & close.shift().gt(10)
    ret = ret.mask(mask, 0.0)
    liquidity = traded_value.rolling(60, min_periods=60).median().shift(1)
    liquid = liquidity.gt(5_000_000)
    ew = ret.where(liquid).mean(axis=1).rename("ew")
    kse = pd.read_csv(ROOT / "data/macro/kse100.csv", parse_dates=["date"])
    kse = kse.drop_duplicates("date").set_index("date").sort_index()["close"]
    kse = kse.reindex(close.index).pct_change(fill_method=None).rename("kse100")
    return {"close": close, "ret": ret, "liquidity": liquidity,
            "ew": ew, "kse100": kse, "actions": pd.DataFrame(action_rows, columns=["symbol", "date", "raw_return"])}


def compound(series):
    values = pd.Series(series).dropna()
    return float(np.prod(1 + values) - 1) if len(values) else np.nan


def stats(values):
    x = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if not len(x):
        return dict(n=0, mean=np.nan, median=np.nan, hit=np.nan, best=np.nan, worst=np.nan)
    return dict(n=len(x), mean=float(x.mean()), median=float(np.median(x)),
                hit=float((x > 0).mean()), best=float(x.max()), worst=float(x.min()))
