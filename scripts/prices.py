"""Shared price loader. Every later test should import from here.

    from prices import load_panel, returns, ew_market, liquid_universe

Sources (symbol level, prices_raw wins where both exist):
  data/prices_raw/{SYM}.csv        PSX portal, raw OHLCV, 313 KMI names
  seed/data/prices/{SYM}.csv       psxdata, 528 ALLSHR names (empty files and XD/XB/XR duplicates skipped)

Conventions
  * An *observation* is a day with volume > 0 and close > 0. close is NaN on every other day,
    so a stock's return is measured between consecutive observations (never fillna(0)).
    The gap (panel rows since the previous observation) is available via returns(..., return_gap=True).
  * Prices are RAW (unadjusted). Use returns() for returns.
  * Survivorship: only names still listed on 2026-10-16 are in the panel. Delisted and merged names
    are missing, so any equal-weight index built here is flattered. Say so in every write-up.

Return methods
  'crude'     A move is treated as a corporate action and set to 0 if it is beyond +-10.5% (price > Rs10)
              or beyond Rs1.05 (price <= Rs10, PSX Rs1 rule), the day's volume is normal (volume ratio
              <= VOL_NORMAL) and the gap is at most MAX_GAP_ZERO. This is the seed approach. BIASED:
              it deletes real ex-dividend and bonus effects below the threshold only partly (10% bonuses
              stay in as fake -9% days) and deletes dividends above it (lesson 19: do not add yield back
              on top of this).
  'adjusted'  If data/corporate_actions.csv exists (columns symbol, ex_date, type[cash|bonus|right|split],
              value) it is applied as a TOTAL return: cash adds the dividend back on the ex date, bonus and
              split rescale the new price. Rights are ignored (no price information); any remaining
              unexplained suspect day is zeroed as in 'crude'. If the file is absent it falls back to 'crude'.
              An action whose ex_date is a no-trade day is applied on the next observation.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, SEED = ROOT / "data" / "prices_raw", ROOT / "seed" / "data" / "prices"
CLOSE_PQ, VOL_PQ = ROOT / "data" / "panel_close.parquet", ROOT / "data" / "panel_volume.parquet"
ACTIONS = ROOT / "data" / "corporate_actions.csv"
SUSPECTS = ROOT / "data" / "suspected_corporate_actions.csv"

BIG_PCT, BIG_RS = 0.105, 1.05   # 10% circuit + rounding; Rs1 limit on sub-Rs10 stocks + 5 paisa
VOL_NORMAL = 3.0                # volume / trailing 20-row median volume at or below this = "normal"
MAX_GAP_ZERO = 5                # only zero a suspect move if it follows at most this many panel rows
_cache = {}


# ---------- loading ----------
def _read(path):
    try:
        x = pd.read_csv(path, usecols=["date", "close", "volume"], parse_dates=["date"], index_col="date")
    except (ValueError, pd.errors.EmptyDataError):
        return None
    return x[~x.index.duplicated(keep="last")].sort_index() if len(x) else None


def _build():
    files = {}
    for d in (SEED, RAW):  # raw last so it overwrites
        for f in d.glob("*.csv"):
            sym = f.stem
            if d is SEED and re.search(r"(XD|XB|XR)$", sym):  # lesson 14: ex-suffix is not a symbol
                continue
            files[sym] = f
    px = {s: _read(f) for s, f in sorted(files.items())}
    px = {s: x for s, x in px.items() if x is not None}
    close = pd.DataFrame({s: x.close for s, x in px.items()})
    vol = pd.DataFrame({s: x.volume for s, x in px.items()}).sort_index()
    close = close.sort_index()
    inside = vol.notna().cummax() & vol[::-1].notna().cummax()[::-1]   # between first and last file row
    vol = vol.where(~(inside & vol.isna()), 0.0)                        # missing row inside listing = no trade
    obs = (vol > 0) & (close > 0)
    close, vol = close.where(obs), vol.where(vol.notna())
    return close, vol


def _stale():
    if not (CLOSE_PQ.exists() and VOL_PQ.exists()):
        return True
    t = min(CLOSE_PQ.stat().st_mtime, VOL_PQ.stat().st_mtime)
    return any(f.stat().st_mtime > t for d in (RAW, SEED) for f in d.glob("*.csv"))


def load_panel(rebuild=False):
    """-> (close, volume, traded_value), each dates x symbols. close is NaN on no-trade days;
    volume is 0 on no-trade days inside a listing and NaN outside it; traded_value = close*volume
    (0 on no-trade days, NaN outside the listing). Writes the parquet files and the suspect log on rebuild."""
    if "panel" not in _cache or rebuild:
        if rebuild or _stale():
            close, vol = _build()
            close.to_parquet(CLOSE_PQ), vol.to_parquet(VOL_PQ)
            suspects(close, vol).to_csv(SUSPECTS, index=False)
        else:
            close, vol = pd.read_parquet(CLOSE_PQ), pd.read_parquet(VOL_PQ)
        tv = (close * vol).fillna(0).where(vol.notna())
        _cache["panel"] = (close, vol, tv)
    return _cache["panel"]


# ---------- returns ----------
def _moves(close, vol):
    """Per observation: pct move, previous observed close, gap (rows), volume ratio, big-move mask."""
    ix = pd.DataFrame(np.arange(len(close))[:, None] + 0.0 * close.values, close.index, close.columns).where(close.notna())
    prev = close.ffill().shift(1)
    gap = ix - ix.ffill().shift(1)
    vo = vol.where(close.notna())
    vratio = vo / vo.rolling(20, min_periods=5).median().shift(1)
    pct = close / prev - 1
    big = (pct.abs() > BIG_PCT).where(prev > 10, (pct * prev).abs() > BIG_RS)
    return pct, prev, gap, vratio, big & close.notna() & prev.notna()


def suspects(close, vol):
    """Every observation with a big move and normal volume: symbol, date, pct_move, volume_ratio."""
    pct, _, _, vr, big = _moves(close, vol)
    m = (big & ((vr <= VOL_NORMAL) | vr.isna())).stack()
    m = m[m].index
    return pd.DataFrame({"symbol": m.get_level_values(1), "date": m.get_level_values(0),
                         "pct_move": pct.stack().reindex(m).values, "volume_ratio": vr.stack().reindex(m).values})


def load_actions(path=ACTIONS):
    """corporate_actions.csv as a DataFrame (symbol, ex_date, type, value) or None if the file is absent."""
    if not Path(path).exists():
        return None
    a = pd.read_csv(path, parse_dates=["ex_date"])
    return a[a.type.isin(["cash", "bonus", "split"])]


def returns(close, method="crude", vol=None, actions=None, return_gap=False):
    """Daily returns on observation days (NaN on no-trade days; a return after a gap spans the gap).
    method 'crude' or 'adjusted' (see module docstring). vol defaults to the panel volume.
    return_gap=True also returns the gap-length frame (panel rows since previous observation)."""
    if method not in ("crude", "adjusted"):
        raise ValueError(method)
    vol = (load_panel()[1] if vol is None else vol).reindex(index=close.index, columns=close.columns)
    pct, prev, gap, vratio, _ = _moves(close, vol)
    if method == "adjusted":
        actions = load_actions() if actions is None else actions
    else:
        actions = None
    if actions is not None and len(actions):
        mult, cash = pd.DataFrame(1.0, close.index, close.columns), pd.DataFrame(0.0, close.index, close.columns)
        for r in actions.itertuples():
            if r.symbol not in close.columns:
                continue
            col = close[r.symbol].dropna().index
            k = col.searchsorted(r.ex_date)
            if k == 0 or k >= len(col):   # before first / after last observation: nothing to adjust
                continue
            t = col[k]
            if r.type == "cash":
                cash.at[t, r.symbol] += r.value
            elif r.type == "bonus":
                mult.at[t, r.symbol] *= 1 + r.value
            elif r.type == "split":
                mult.at[t, r.symbol] *= r.value
        pct = (close * mult + cash) / prev - 1
    big = (pct.abs() > BIG_PCT).where(prev > 10, (pct * prev).abs() > BIG_RS)
    ret = pct.mask(big & (vratio <= VOL_NORMAL) & (gap <= MAX_GAP_ZERO), 0.0)
    return (ret, gap) if return_gap else ret


# ---------- market and universe ----------
def _med_tv(tv):
    return tv.rolling(60, min_periods=40).median().shift(1)   # trailing 60 rows ending the day before


def ew_market(ret, min_value=5e6, tv=None):
    """Equal-weight daily market return over names whose trailing 60-day median traded value (rows up to
    the previous day) exceeds min_value (Rs). Survivor-biased: see module docstring."""
    tv = load_panel()[2] if tv is None else tv
    liquid = (_med_tv(tv) > min_value).reindex(index=ret.index, columns=ret.columns, fill_value=False)
    return ret.where(liquid).mean(axis=1)


def liquid_universe(date, min_value=5e6):
    """Symbols whose median traded value over the 60 trading days strictly before `date` exceeds min_value
    (at least 40 listed days in the window)."""
    tv = load_panel()[2]
    w = tv[tv.index < pd.Timestamp(date)].tail(60)
    return list(w.columns[(w.median() > min_value) & (w.count() >= 40)])


# ---------- provisional action table (NOT used by returns by default) ----------
def provisional_actions():
    """Best-effort table from data/payouts_raw.csv (about 2 years) and seed/data/corporate_actions.csv, same
    schema as corporate_actions.csv. For reconciling the suspect log only. Payout percentages are assumed to be
    of Rs10 par (UNVERIFIED), ex-date is approximated as 2 trading days before book closure starts (the average dip in 94 large
    payers falls at -2 and -1; real ex-date may be off by a day; seed rows use hand-checked dates and win). Rights are skipped."""
    out = []
    p = pd.read_csv(ROOT / "data" / "payouts_raw.csv")
    close = load_panel()[0]
    for r in p.itertuples():
        m = re.match(r"\s*(\d{2}/\d{2}/\d{4})", str(r[4]))
        nums = [float(x) for x in re.findall(r"(\d+\.?\d*)\s*%", str(r.Details))]
        if not m or not nums or "(R)" in r.Details:
            continue
        start = pd.to_datetime(m.group(1), dayfirst=True)
        ex = close.index[max(close.index.searchsorted(start) - 2, 0)] if start > close.index[0] else start
        if "(B)" in r.Details:
            out.append((r.symbol, ex, "bonus", sum(nums) / 100))
        elif "(D)" in r.Details or "DIVIDEND" in r.Details.upper():
            out.append((r.symbol, ex, "cash", sum(nums) / 100 * 10))
    s = pd.read_csv(ROOT / "seed" / "data" / "corporate_actions.csv", comment="#", parse_dates=["ex_date"])
    ty = {"cash_div": "cash", "bonus": "bonus", "split": "split"}
    val = s.amount_pkr_or_ratio.astype(str).map(lambda v: float(v[:-1]) / 100 if v.endswith("%") else float(v.split(":")[0]) if ":" in v else float(v))
    seed = pd.DataFrame({"symbol": s.ticker, "ex_date": s.ex_date, "type": s.type.map(ty), "value": val})
    new = pd.DataFrame(out, columns=seed.columns)
    dup = new.apply(lambda r: ((seed.symbol == r.symbol) & (seed.type == r.type) & ((seed.ex_date - r.ex_date).abs() <= pd.Timedelta(days=7))).any(), axis=1)
    return pd.concat([seed, new[~dup]]).drop_duplicates(["symbol", "ex_date", "type"]).sort_values(["symbol", "ex_date"]).reset_index(drop=True)


if __name__ == "__main__":
    close, vol, tv = load_panel(rebuild=True)
    n = close.notna().sum()
    print(f"panel {close.shape[0]} dates x {close.shape[1]} symbols, {close.index[0].date()} to {close.index[-1].date()}")
    print(f"symbols with 500+ observations: {(n >= 500).sum()} of {len(n)}")
    sus = pd.read_csv(SUSPECTS, parse_dates=["date"])
    print(f"suspected corporate actions logged: {len(sus)} on {sus.symbol.nunique()} symbols -> {SUSPECTS.name}")
    ret, gap = returns(close, "crude", return_gap=True)
    print(f"returns: {ret.notna().sum().sum()} obs, {(gap > 1).sum().sum()} after a gap, zeroed {int(((ret == 0) & (_moves(close, vol)[4])).sum().sum())}")
    m = ew_market(ret)
    m = m[m.index >= "2017-01-01"].dropna()
    k = pd.read_csv(ROOT / "data" / "macro" / "kse100.csv", index_col=0, parse_dates=True)["close"]
    k = k[k.index >= m.index[0]]
    ew_cum, k_cum = (1 + m).prod() - 1, k.iloc[-1] / k.iloc[0] - 1
    print(f"EW market (crude, Rs5m filter, price only) {m.index[0].date()} to {m.index[-1].date()}: {ew_cum:+.1%}; KSE100 over the same span: {k_cum:+.1%}")
    print(f"liquid names on 2026-10-16: {len(liquid_universe('2026-10-17'))}; average in EW index: {(_med_tv(tv) > 5e6).sum(axis=1)[m.index].mean():.0f}")
    assert returns(close.iloc[:50, :5], "adjusted").shape == (50, 5)
    assert ew_market(ret).notna().sum() > 2000
    print("adjusted falls back to crude:", ACTIONS.exists() is False)
