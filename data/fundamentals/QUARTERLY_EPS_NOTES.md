# Quarterly EPS history for the liquid universe: notes

Written 2026-10-17 by the data pull for the results-surprise test. Source: StockAnalysis (stockanalysis.com), quarterly pages. The page footer and embedded data say the figures come from S&P Global Market Intelligence. Not checked against PSX filings.

## Files
- `data/fundamentals/quarterly_eps.csv`: one row per symbol and fiscal quarter end. Columns: symbol, fiscal_quarter_end, revenue, net_income, eps_basic, eps_diluted, ocf, shares, consolidated_flag, source_url, announce_dt, first_tradable_date, announce_title, announce_doc_id.
- `data/fundamentals/_fetch_failures.csv`: the 12 failed page requests (6 symbols, two pages each).
- `data/raw/stockanalysis/`: the raw HTML of every page fetched (`{SYM}_income.html`, `{SYM}_cash.html`), about 62 MB. The parse can be re-run from these without new requests.

## Universe
- The 92 names in `seed/data/fundamentals/universe_scored.csv`, all present in `data/prices_raw`.
- Plus KMI names in `data/prices_raw` whose median traded value over their last 60 observed days (close × volume, volume > 0) exceeds Rs5m. 130 names pass that screen, and 44 of them are not in the 92. The union is 136, so the cap of 150 was not reached.

## Fetch
- 272 page requests (136 symbols × 2 pages), curl_cffi chrome impersonation via `scripts/cf.py`, 1.5 s between requests. No Cloudflare challenge or block appeared. The run did not stop early.
- Pages used: `/financials/income-statement/?p=quarterly` and `/financials/cash-flow-statement/?p=quarterly`. The spec's `/financials/?p=quarterly` URL is a summary page. It shows revenue, net income and one EPS row, but not basic and diluted EPS or shares, so the income-statement page was used instead.
- No data for 7 symbols:
  - GCIL, SLM, TPLRF1, BBFL, MWMP and GCWL returned HTTP 404 on both pages.
  - TISL returned 200 on both pages, but the HTML has no quarterly statement tables.
- 129 of 136 symbols have rows. Quarter ends run from 2019-09-30 to 2026-09-30. The median symbol has 20 quarters. LOTCHEM has a 2026-09-30 row.
- All 92 names in the base universe have rows.

## Fields and units
- revenue, net_income, ocf: PKR million, as displayed on the page.
- eps_basic, eps_diluted: Rs per share, as displayed.
- shares: basic shares outstanding in millions, as displayed. The page rounds this to whole millions, so it is unusable for very small share counts. Examples: BUXL shows 1, SGPL shows 18.
- net_income is "Net Income to Common" where the page has it, otherwise "Net Income". This is the figure attributable to shareholders.
- Blanks on the page were left empty: revenue 43 rows, eps_basic and eps_diluted 11 each, shares 11, ocf 18. Some blanks are on loss-making or unusual reporters, e.g. QTECH revenue (18 rows), STL (10), SGPL (6), PICT (5).

## Consolidated or standalone
- The statement pages do not state whether figures are consolidated or standalone. The word "consolidated" appears in none of the 272 pages.
- `consolidated_flag` is therefore empty on all 2,460 rows. Treat EPS as UNVERIFIED for consolidation status. Lesson 1 applies: for holding companies, check the consolidated figure against a filing before use.

## Consistency check
- Net income divided by basic shares, compared with reported basic EPS, agrees within 5% for 96.1% of the 2,440 rows where it can be tested. The median ratio is 1.00.
- The 38 rows off by more than 20% are mostly small-number rounding (EPS of ±0.01 to ±0.02) or the rounded share counts above. BUXL accounts for 20 of them.

## Join to financial result announcements
- Source: `data/announcements.parquet`, klass == financial_result. There are 46,076 such rows.
- Period-end date: parsed from the title. The date formats are "dd-mm-yyyy", "yyyy-mm-dd", "Month dd, yyyy" and "dd Month yyyy". 34,509 rows have a date. The remaining rows (for example "Financial Results for the Quarter Ended" with no date) cannot be matched by title and were not matched.
- Excluded: 1,102 dated candidates that fell outside the window (REVOKED titles are dropped separately). The window is 0 to 150 days from the period end. It removes titles that refer to a period but were filed before it ends or long after, for example "Annual Progress Report for the year ended June 30, 2024", filed in February 2025.
- Choice: the earliest candidate for each (symbol, quarter end) within the window.
- Join rate: 1,976 of 2,460 rows (80.3%) have announce_dt. 127 of 129 symbols have at least one join.
- Joined by quarter-end year: 2020 4 of 5, 2021 188 of 244, 2022 362 of 477, 2023 381 of 487, 2024 397 of 497, 2025 423 of 502, 2026 221 of 246. The 2019 rows (2) did not join.
- Lag from quarter end to announcement: median 31 days, minimum 7, maximum 148.

## Caveats
- Half-year announcements ("Financial Results for the Half Year Ended June 30") are matched to the June quarter. Their figures may be cumulative six-month figures, not the standalone Q2. Check this before using the Q2 surprise.
- Q4 rows come from the annual "Year Ended" announcements. StockAnalysis derives Q4 from the annual figure less nine months, so Q4 EPS is not an independently reported quarter.
- Transmission of Quarterly Report filings are not used. They are a different klass and sometimes carry the only dated filing. Matching them would raise the join rate; this was not measured.
- first_tradable_date applies the 15:30 PKT rule with weekends skipped. PSX holidays are not in the calendar, so this can be a day off on holiday weeks.
- Survivorship: the universe is names listed on 2026-10-16. Delisted and merged names are missing, so any backtest here is flattered.
- No EPS figure has been checked against a company filing or the PSX portal. The values are the StockAnalysis figures as displayed.
