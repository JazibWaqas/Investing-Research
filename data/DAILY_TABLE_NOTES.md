# Daily table: columns, definitions, gaps (built 18 Oct 2026)

`data/daily_table.parquet/` (hive-partitioned by `year`), built by `scripts/daily_table.py`, checked by `scripts/daily_table_check.py`. 577,794 rows, 455 symbols (313 survivors in `prices_raw` plus 142 delisted/merged names from `prices_delisted` that have 5 or more traded sessions; 294 delisted files after dropping 21 duplicates of another symbol by the same 90%-equal-closes test as the upper-lock study, 150 of those are stubs with fewer than 5 traded sessions), 2017-01-02 to 2026-10-16, 101 columns, about 230 MB in memory. The "about 2 million rows" in the brief was an overestimate: 313 names times about 1,660 traded days is the real order of magnitude.

## Rows and sessions

One row per (symbol, session on which the symbol traded: volume above 0 and close above 0). Days it did not trade have no row, but they still count on the calendar: all "t+k", "5d", "20d" windows are counted in market sessions (the 2,480 dates of `prices.load_panel`), not in the symbol's own trades. So `ret_5d` on an illiquid name can span a few days with no trade (it uses the last traded close). `session_idx` is the calendar index of the row.

## Prices

Intraday facts (open, high, low, volume, locks) are from raw OHLCV. Returns use adjusted closes: `data/panel_close_adj.parquet` (total return, dividends added back) for survivors, falling back to the crude chain from `prices.returns(..., "crude")` for delisted names (and for any survivor with no adjusted column). Raw intraday prices are put on the adjusted scale with `adj_close / raw_close` of the same day, so `gap_open` (open against the previous adjusted close) is not distorted by an ex-date. `close` is the raw close. Zero open/high/low values in the feed are treated as missing.

## Feature columns (use data at or before the close of t)

- ret_1d (close to previous session's close), ret_open_to_close (raw close over open), gap_open, ret_3d, ret_5d, ret_20d, ret_60d, ret_126d (adjusted, in sessions).
- dist_252_high, dist_252_low: adjusted close against the max/min adjusted close of the last 252 sessions (needs 126).
- vol_ratio_20_120: mean volume of the last 20 sessions over the mean of the 120 before those (as in the upper-lock study). vol_ratio_1_20: today's volume over the mean of the previous 20. Volume is share-equivalent for survivors (multiplied by raw/price-adjusted close so a bonus is not an ignition).
- traded_value_median_60: median of close times volume over the 60 sessions ending the day BEFORE t (the `prices.py` convention), at least 40 needed. `liquid` = that above Rs5m.
- upper_lock, lower_lock: see below. locks_up_5d, locks_up_10d: count of upper_lock in the last 5/10 sessions including t. consecutive_up_days: consecutive trades with a higher adjusted close, ending at t.
- Filings (from `announcements.parquet`; counts known at t): f_financial_result, f_dividend_or_bonus, f_material_info, f_insider_trade, f_board_meeting_notice, f_agm, f_credit_rating, f_other, f_total, plus f_insider_buy and f_insider_sell (subsets of f_insider_trade by `direction`; the rest are "unknown"). A filing is assigned to the session of its date if stamped at or before 15:30, otherwise to the next session (so "since the previous close" is (previous 15:30, this 15:30]). days_since_last_filing: sessions since the last filing of any class (0 = today); null before the symbol's first filing. next_board_meeting_known: a board_meeting_notice in the last 30 calendar days including t.
- sector: from the `S` dict in `scripts/sector_momentum.py` (the full lists, parsed not imported), else "other". sector_ret_1d, sector_ret_5d: equal-weighted mean of the sector's peers (self excluded) that are liquid and traded that day, with moves beyond 50% (1d) or 100% (5d) dropped as data breaks. Null for "other" and when no peer qualifies.
- index_ret_1d, index_ret_5d: KMI All Share total return (`data/macro/kmiallshr.csv`).
- regime ("bill>policy" / "bill<=policy") and regime_spread: 6M T-bill yield minus policy rate, each the latest value on or before t.
- kmi_member: True/False from the KMI All Share snapshots in `data/index_members/` (derived lists from 2019-01-28, exact list 2026-06-05), the latest snapshot on or before t. Null before 2019-01-28. Between snapshots it is stale by up to six months, and `index_changes.csv` is NOT used (its KMI_ALL rows are what the derived lists were built from). Delisted names that were never in a list read False.
- is_newsless_rise: ret_5d above 8%, days_since_last_filing above 10, and sector_ret_5d below 3% (where the sector has no basket the index's 5-day return is used instead).

## Locks (era-dependent)

The limit in force: 5% up to 27 Mar 2020, 7.5% from 30 Mar 2020 to 5 Jul 2024, 10% from 8 Jul 2024 (read off the data, as in `tests/volume_ignition_upper_locks.py`). upper_lock: the raw close is at least 99.5% of the limit move above the previous traded close and at most the limit plus 1.5% (prices of Rs20 or more), or at most +30% (previous close under Rs20, where the band is wider). lower_lock: same on adjusted closes, floor 0.6 for cheap names. This is a close AT the limit, not a proof that the order book was locked: a stock can close at the limit and have traded all day. Rates: 11.7% of rows in 2017, 4.1% of liquid rows overall (3.7% of all rows in 2026); the 5% era and sub-Rs20 names inflate it.

## Outcome columns (strictly after t)

- next_open: the open (on the adjusted scale) of the first session after t on which the symbol trades. Entry price for everything below. It cannot be bought on a locked-up open; the table does not model fill.
- ret_fwd_k for k = 1, 2, 3, 5, 10, 20, 60: adjusted close at calendar session t+k over next_open, minus 1. Null if the symbol does not trade by t+k (entry later than t+k) or t+k is past its last trade.
- kmi_ret_fwd_k: KMI All Share close at t+k over the index open of the entry session. Excess return = ret_fwd_k - kmi_ret_fwd_k.
- mfe_k, mae_k for k = 1, 3, 5, 10, 20: highest high / lowest low (adjusted) over sessions t+1..t+k, over next_open, minus 1.
- first_upper_lock_within_3, _5: offset in sessions from t (1 = next session) of the first upper_lock in t+1..t+3 / t+5; null if none or the window runs past the last trade. The entry session's own close counts if it locks. first_red_day: same for the first adjusted close below the prior session's close within 60 sessions (null if none, which at 60 is rare but possible).
- filing_within_{5,10,20}_{class} and _total: count of filings assigned to sessions t+1..t+k (so filings after t's cutoff). Null if the window runs past the symbol's last trade.

## How the leak check works

Features are built only with `rolling`, `shift(+k)`, `ffill` and cumulative functions on calendar arrays; outcomes only with `shift(-k)`, reverse rolling and `bfill().shift(-1)`. `scripts/daily_table_check.py` proves it empirically: rebuild the whole table with all inputs cut at 2023-12-29 (`DT_TRUNC=2023-12-29 DT_OUT=<path> daily_table.py`), then compare every one of the 45 feature columns, row for row, with the full build on dates up to the cut. Result: identical (one float-noise flip of is_newsless_rise at exactly 8.0% is ignored). Outcome columns are expected to differ near the cut and are not compared.

## Known gaps

- Survivorship: delisted names are in, but their forward returns stop at the last trade, so a delisting loss after the last print is not captured (see `delistings.csv` and `delisted_last_year_returns.csv`). Forward columns are null where the window passes the last trade, which biases against delisters.
- Delisted names use the crude return chain, which can still contain unadjusted splits and data breaks; a few extreme ret_1d values are real data problems, not signals. Survivors' returns are total return and include dividend add-backs.
- Announcements stamped on weekends/holidays go to the next session; timestamps are minutes-accurate but the cutoff of 15:30 is a simplification (Friday sessions differ). Announcements exist from 2005 but classification and coverage are thinner in the early years.
- kmi_member: null before 2019, stale between snapshots (see above). `liquid` and the sector peers use today's membership of sectors (names listed in `sector_momentum.py` are survivor-heavy), so sector_ret is a hindsight basket.
- Locks as described above; the limit dates are inferred, not from the exchange circulars.
- Index open is used for the KMI excess-return denominator; its data begins 2016-10-24.
- Rows only on traded sessions: a long no-trade gap shows up as one big ret_1d/gap_open on the first trade after it.
