# Macro and commodity series

Built 2026-10-17 by `scripts/macro_*.py` (raw downloads in `data/raw/macro/`, untouched). Rows are listed with first and last date. All series are as downloaded; nothing was invented or interpolated.

## Markets (daily)

| File | Source | Rows | Range | Notes |
|---|---|---|---|---|
| kse100, kmi30, kmiallshr, kse30, allshr .csv | PSX data portal `POST /historical` (full daily OHLCV) | 2480 / 2479 / 2473 / 2479 / 2480 | 2016-10-17 (kmiallshr 2016-10-24) to 2026-10-16 | Columns date,value(=close),open,high,low,close,volume. **Portal history starts Oct 2016; 2015 to Oct 2016 not found** (stooq and investing.com are bot-blocked, Yahoo has no PSX index). Volume is index-level share volume. |
| brent.csv, wti.csv | FRED `DCOILBRENTEU`, `DCOILWTICO` (EIA spot, USD/bbl) | 2992 / 2942 | 2015-01-02 to 2026-10-14 | US holidays missing. |
| usdpkr.csv | SBP "Daily Average Banks' Floating Exchange Rates" archive, https://www.sbp.org.pk/assets/document/BFER_Daily_Arch.xlsx, U.S. Dollar row (PKR per USD) | 2888 | 2015-01-02 to 2026-09-30 | Bank average rate, not interbank close. Archive is refreshed periodically, so Oct 2026 is missing. Yahoo `PKR=X` was rejected (spurious values such as 10.0 and inconsistent open/close). |

## Rates and prices

| File | Source | Rows | Range | Notes |
|---|---|---|---|---|
| policy_rate_decisions.csv | SBP MPS list https://www.sbp.org.pk/our-operations/publications/monetary-policy-statements/501 (PDFs in `data/raw/macro/mps/`); rates cross-checked to `seed/data/macro/pr.csv` | 84 | 2015-01-31 to 2026-09-14 | Every MPC decision incl. holds and the two March 2020 emergency cuts. `date` is the **announcement** date (MPS date); the seed pr.csv dates are effective dates, usually 1 to 6 days later. Jan 2015, Jul 2015 and Jan 2018 PDFs print no day; their dates (2015-01-31, 2015-07-31, 2018-01-29) are approximate and flagged in `source`. Pre-2015-05 rates (9.5 to 8.5 to 8.0) come from the Jan/Mar 2015 MPS text. |
| tbill_auctions.csv | SBP https://www.sbp.org.pk/assets/document/tb.xlsx ("New Detailed Format") | 308 | 2015-01-07 to 2026-10-14 | Cut-off yield in percent for 3m, 6m, 12m. Blank where a tenor was not offered or no bids accepted (6m 38 blanks, 12m 76, 3m 2). Auction date, not issue date. |
| cpi.csv | `yoy` from seed `cpi_yoy_2015_2026.csv`; `mom` and `yoy_pbs_release` from PBS Monthly Review PDFs (https://www.pbs.gov.pk/price-statistics/, Table 1.a National CPI) | 141 | 2015-01 to 2026-09 | National CPI, base 2015-16. **mom only exists for 2021-06 to 2026-08 (63 months)**; PBS pages only list reviews from Jul 2022 and the earlier ones sit in Table 1.a's lookback. 2015-01 to 2021-05 mom not found. Seed yoy matches PBS to within rounding (0.2 or less) for all 63 overlap months; largest gaps 2025-09 (seed 5.60, PBS table 5.8) and 2024-10 (7.07 vs 7.2). 2026-09 is seed only and not yet on PBS: unverified. Month is the reference month; PBS publishes on the 1st to 2nd working day of the next month. |

## Commodities (monthly)

Source: World Bank Pink Sheet, https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx (updated 2026-10-02). Date is the first of the month; values are monthly averages in nominal USD. 141 rows each, 2015-01 to 2026-09.

| File | Series | Caveat |
|---|---|---|
| coal_rb.csv | Coal, South African (Richards Bay), USD/mt | Some 2022 to 2024 months are World Bank estimates. |
| coal_newcastle.csv | Coal, Australian (Newcastle), USD/mt | Spot to Jan 2022, futures after. |
| urea.csv | Urea, USD/mt | Black Sea fob to Feb 2022, Middle East fob after. |
| dap.csv | DAP, USD/mt, fob US Gulf | |
| cotton.csv | Cotton A Index, USD/kg | |
| palm_oil.csv | Palm oil, USD/mt | Series definition changed Jan 2026 (RBD average export price), so a possible level break. |
| iron_ore.csv | Iron ore 62% Fe cfr China, USD/dmt | Extra, as steel input proxy. |
| steel.csv | FRED `WPU1017` US PPI steel mill products (index, 1982=100), 2015-01 to 2026-09 | **Not a price in USD/t and not Pakistani.** The Pink Sheet has no HRC or scrap series; no free daily HRC found. |

## Not obtained

- **NCCPL FIPI/LIPI daily and monthly, MTS/margin financing**: nccpl.com.pk is behind Cloudflare and returns 403 / "you have been blocked" to curl_cffi (chrome, firefox, safari, edge profiles) and to headless Chrome from this machine. History depth unknown. Needs a manual browser session or an alternative source (e.g. a broker's daily FIPI report).
- **Pakistan Eurobond yields / CDS**: investing.com and stooq are bot-blocked; FRED has no Pakistan 10Y series; nothing free found. Skipped.
- **KSE100 etc. before 2016-10-17.**
- **CPI MoM before 2021-06.**

## Other files found, not pulled

SBP `Forex_Arch.xlsx` (https://www.sbp.org.pk/assets/document/Forex_Arch.xlsx) has weekly and month-end liquid FX reserves from 2011; raw copy in `data/raw/macro/forex_arch.xlsx`. SBP easydata and `kibor-rates-<date>.pdf` offer KIBOR but only daily PDFs.

## fipi_lipi.csv (investor-type flows, added 2026-10-17)

Source: scstrade.com `FIPILIPI.aspx/loadmainsumdetails` (Standard Capital Securities, which republishes NCCPL FIPI/LIPI; nccpl.com.pk itself is Cloudflare-blocked). Fetched by `scripts/fetch_fipi_lipi.py`, one POST per business day.

- Cadence: daily, 2017-01-02 to 2026-10-16, 2,413 trading days, 26,355 rows. Long format: `date, investor_type, buy_usd_mn, sell_usd_mn, net_usd_mn, source_url`. Sell is stored as a positive number (the source prints it negative).
- Units: USD million, converted by the source at its own daily rate. Total value across all markets (regular, future, odd lot etc.), not regular market only. Net sums to about zero across types each day.
- Types: foreign (overseas pakistani, foreign corporates, foreign individual) = FIPI; local (individuals, companies, banks / dfi, mutual funds, insurance companies, nbfc, broker proprietary trading, other organization) = LIPI. Rows for a type are absent on days with no activity (foreign individual 2,260 days; insurance starts 2017-02-08).
- Gaps: five weekdays return a server error and are missing: 2017-06-02, 2023-01-19, 2023-06-05, 2023-08-28, 2025-07-30. Weekday holidays return empty and are skipped.
- Not captured: per-sector and per-market splits (the other endpoints `loadfipiInvestor`, `loadlipi`, `loadfipi` on the same page have them).

## MTS (margin trading system)

No history found. scstrade.com only serves the current day's PDF (`research/Research Reports/General/MTS Report.pdf`, a snapshot saved at `data/raw/flows/scs_mts.pdf`), so no `mts.csv`.

## fipi_lipi_by_sector.csv (sector split, added 2026-10-17)

Source: scstrade.com `FIPILIPI.aspx/loadfipiInvestor`, fetched by `scripts/fetch_fipi_lipi_sector.py` (one POST per business day, 4 retries, resumable: rerun it and it fetches only dates missing from the file). Columns: `date, investor_group, sector, buy_usd_mn, sell_usd_mn, net_usd_mn, source_url`; USD million, sell stored positive.

- Coverage: 2017-01-02 to 2026-10-16, 2,415 trading days, 207,089 rows.
- `investor_group`: `fipi` (all foreign combined, not split into overseas pakistani / corporates / individuals here) and `lipi <type>` for banks / dfi, broker proprietary trading, companies, individuals, insurance companies, mutual funds, nbfc, other organization.
- Sectors (source's top-10 PSX sectors by activity plus a remainder): Cement, Commercial Banks, Fertilizer, Food and Personal Care Products, Oil and Gas Exploration Companies, Oil and Gas Marketing Companies, Power Generation and Distribution, Technology and Communication, Textile Composite, Debt Market (from 2020-10-02 only), and All other Sectors (everything else). Pharma, Refinery, Automobile etc. are inside "All other Sectors". The sector set is fixed, but a row is absent when that group did not trade the sector that day, so counts differ by sector.
- Gaps: 2019-04-19, 2020-06-19 and 2020-11-03 return a server error on this endpoint (they exist in `fipi_lipi.csv`). Conversely the five days missing from `fipi_lipi.csv` (2017-06-02, 2023-01-19, 2023-06-05, 2023-08-28, 2025-07-30) are present here, so summing sectors per group gives a fill for those days.
- Caveat: sector sums were not reconciled against `fipi_lipi.csv` totals.
