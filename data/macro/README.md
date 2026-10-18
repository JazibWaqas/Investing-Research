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

## External account (added 2026-10-18 by `scripts/macro_external.py`)

Regime inputs for the external-account leg of the method. Raw inputs are in `data/raw/macro/`.

### fx_reserves.csv

- Columns: `date` (week-end Friday), `sbp_reserves_usd_mn` (net reserves held with SBP), `total_reserves_usd_mn` (total liquid FX reserves, SBP plus banks). USD million.
- Source: SBP Forex_Arch, https://www.sbp.org.pk/assets/document/Forex_Arch.xlsx, sheet "Week-end" (raw copy `data/raw/macro/forex_arch.xlsx`). Also listed at https://www.sbp.org.pk/ecodata/.
- Cadence: weekly (week ending Friday). Some weeks are missing where SBP had holidays; the sheet's own footnotes say which.
- Range: 792 rows, 2011-05-07 to 2026-10-09. The latest print (2026-10-09) is the latest in the SBP archive as of the build. I did not find a separate live weekly page; the archive is the SBP series itself.
- Caveats: the sheet carries revision and provisional tags on some dates ("(R)", footnote numbers); these were stripped, and the values are as printed. The SBP-only series rose from 17,118 (2026-08-28) to 21,400 (2026-09-18) in three weeks; the source gives no reason here and it was not checked.

### current_account.csv

- Columns: `month` (YYYY-MM), `cab_usd_mn` (current account balance, USD million; negative is a deficit).
- Source: SBP Summary Balance of Payments as per BPM6, monthly, https://www.sbp.org.pk/assets/document/BPM6_Ach_M.xlsx (linked from https://www.sbp.org.pk/ecodata/). Raw copy `data/raw/macro/BPM6_Ach_M.xlsx`. The file starts 2013-07; only 2015 onward is written here.
- Cadence: monthly, about 2 to 3 weeks after month end. The latest months are provisional and the file's own "P" and "R" markers were not parsed, so which months were revised later is not recorded here.
- Range: 141 rows, 2015-01 to 2026-09. October 2026 is not out yet.
- Caveats: this is the balance-of-payments basis, not the trade-statistics basis. In the header, dates from Apr 2026 onward carry day 26; only the year and month are used.

### import_cover.csv

- Columns: `month`, `reserves_asof` (date of the last weekly print in that month, which is not always the month-end; Sep 2026 uses 2026-09-25), `sbp_reserves_usd_mn`, `total_reserves_usd_mn`, `imports_12m_usd_mn` (trailing 12 months of goods imports, FOB, from the BoP file), `import_cover_total_months` (total reserves / (imports_12m / 12)), `import_cover_sbp_months` (SBP-only reserves on the same basis).
- Source: the two files above. Import cover is computed here; it is not an SBP series.
- Range: 141 rows, 2015-01 to 2026-09. Oct 2026 is left out because no full month of imports exists for it yet.
- Caveat: the method says "reserves" without saying which. Both versions are given; the total-reserves column is the usual headline. Imports are BoP goods FOB, not customs-declared values.

Latest values: week ending 2026-10-09, SBP reserves 21,469.5 and total 26,863.3 USD mn. Current account 2026-09 -356 USD mn; Jan to Sep 2026 -83; Oct 2025 to Sep 2026 -510. Import cover at 2026-09 (reserves as of 2026-09-25): 4.81 months total, 3.85 months SBP-only.

## KSE100 trailing P/E and earnings yield (added 2026-10-18 by `scripts/macro_kse_pe.py`)

### kse100_pe.csv

- Columns: `month` (YYYY-MM, month-end), `pe`, `source` (`computed_kse100_members` on every row).
- Method: P/E = sum of market cap / sum of trailing-four-quarter net income to common, over the KSE100 members in force at that date (snapshot in `data/index_members/`, effective 1 Apr and 1 Oct). Market cap = last close on or before the date x basic shares from the latest quarter available by then, scaled by bonus and split events in `data/corporate_actions.csv` after that quarter. Negative earnings stay in the sum. This is an aggregate ratio, so the largest companies weigh most.
- Source for earnings and shares: StockAnalysis quarterly income statement, https://stockanalysis.com/quote/psx/{SYM}/financials/income-statement/?p=quarterly (raw HTML in `data/raw/stockanalysis/{SYM}_income.html`; pages scraped 2026-10-17). Prices: PSX portal daily history (the repo's `data/prices_*` files, plus `data/raw/macro/psx_hist/` for 35 members that had no file; fetched with `scripts/macro_kse_prices.py`).
- Availability: the announcement date from `data/fundamentals/quarterly_eps.csv` where it is joined; otherwise period end + 90 days.
- Range: 50 rows, 2022-09 to 2026-10. October 2026 uses prices to 2026-10-16. The series starts at the first month with 60 or more members having trailing earnings. From 2022-11 on, 86 to 97 of the 99 to 100 members have inputs. The eight members with no StockAnalysis page are DHPL, FFBL, HGFA, PSMC, SHEL, SSOM, TPLRF1 and YOUW.
- Caveats, all material:
  - Earnings and shares are the current StockAnalysis figures (restated as scraped), not the figures first published. Point in time is approximate.
  - Share counts for a few small bonuses are missing from `corporate_actions.csv` (its notes say so), so those market caps are understated.
  - The membership changes at each snapshot only. Index changes between snapshots are not captured.
  - PSX's own index P/E was not found in the saved pages, and I had no search tool here, so Topline and AHL monthly P/E history was not checked. This series is a computed proxy, not a published PSX figure.
  - The series moves month to month with membership and earnings timing. For example, it falls from 9.52 (2024-09) to 8.04 (2024-10), the month of the 2024-10-01 snapshot, then 9.03 (2024-11). This was not checked against filings.

### earnings_yield_vs_tbill.csv

- Columns: `month`, `kse100_earnings_yield_pct` (100 / pe), `tbill_6m_cutoff_pct` (6-month T-bill cut-off, last auction on or before the month-end), `gap_pct_points` (earnings yield minus T-bill), `tbill_auction_date`. All in percent, not decimals.
- Source: `data/macro/kse100_pe.csv` and `data/macro/tbill_auctions.csv` (SBP tb.xlsx).
- Range: 50 rows, 2022-09 to 2026-10. The earnings yield is an aggregate of trailing earnings, not a forecast return, and the T-bill is a nominal yield that is not dividend-adjusted.

Latest values: 2026-10 P/E 7.86 (through 2026-10-16), earnings yield 12.72%, 6-month T-bill cut-off 12.40% (auction 2026-10-14), gap +0.32 percentage points. Previous month, 2026-09: P/E 8.09, earnings yield 12.36%, T-bill 12.45%, gap -0.09.

### Not built

- PSX's own index P/E: not found in the saved pages (`data/raw/macro/indices_page.html` has none). Not searched further.
- Topline and AHL monthly KSE100 P/E reports: not searched; this session had no web search tool.
