# Corporate actions: table, adjusted panel, reconciliation

Built 17 Oct 2026 by `scripts/ca/` (build.py, recon.py, notes.py). Price data to 2026-10-16. Nothing here is committed. Every number below is computed by `scripts/ca/notes.py` from the files, not typed.

## What was written

| File | What it is |
|---|---|
| `data/corporate_actions.csv` | 659 placed actions (ex date known): cash 473, bonus 159, split 21, right 6. Columns: symbol, ex_date, type, value, announce_dt, ex_date_source, source_doc, plus sub_price (rights subscription price, where stated). 34 rows have an ex date after 2026-10-16 (declared, not yet traded). |
| `data/panel_close_adj.parquet` | Back-adjusted close, total return: bonus, split and every cash dividend in the table, unexplained suspect days zeroed as the loader does. Last value of each series equals the raw last close. NaN where raw close is NaN. |
| `data/panel_close_adj_pricereturn.parquet` | Same, with bonus and split only (cash ignored). Use this one when comparing years: cash coverage is very uneven (see below). |
| `data/corporate_actions_unplaced.csv` | 465 announcements with a value or ratio but no ex date I could defend (by type: bonus 145, cash 159, right 161; with a value or ratio stated: bonus 28, cash 159, right 161). Not applied anywhere. |
| `data/corporate_actions_pdf_reads.csv` | 98 rows read by eye from 84 filing PDFs (doc id in every row). Input to build.py. |
| `data/raw/filings/` | the PDFs. 153 downloaded by this build (cap 400), one request per second, parsed and viewed only, never executed. Log: `data/raw/filings_downloads.log`. |
| `data/raw/corporate_actions_seed_compare.csv`, `corporate_actions_conflicts.csv` | seed cross-check and rows dropped as duplicates of a better source. |

`prices.returns(close, 'adjusted')` now reads the table instead of falling back to crude. The loader's own rules still apply: cash is added back on the ex date, bonus and split rescale the new price, rights are ignored, and any suspect day the table does not explain is zeroed.

## Read this first: what the table can and cannot do

1. **Bonus and split adjustment is the reliable part.** All 21 splits found (2021 to 2026) are in, and the bonus events with a large price gap are in. Small bonuses (under about 8%) are only in when a PDF or the portal gave the book-closure date; the rest sit in the unplaced file and still appear as fake -5% to -9% days.
2. **Cash dividends are only complete from November 2024.** The portal's payout endpoint covers about two years (362 rows used), the seed adds six names from 2021, and announcement titles almost never state an amount (145 of 3807 cash titles). For 2017 to 2020 there are 6 cash rows in total. So the total-return panel is a price-return series with partial dividends: any 2025-26 versus earlier comparison on `panel_close_adj.parquet` is tilted by about the dividend yield. The equal-weight index (Rs5m filter, from 2017) compounds to +52.9% on bonus and split only, +61.8% with the table's cash, and +44.1% on the crude method. All three are survivor-biased (only names listed on 2026-10-16 are in the panel), so the level is flattered; the differences between them are the point.
3. **Par value.** Cash = percent × par. Par is Rs10 unless a split changed it (par divided by the split ratio, so SYS's April 2026 "100%" is Rs2, which matches the seed) or a document says otherwise: ZAL pays "Re.1" for the portal's 100% (doc 260205), NRSL was Rs5 until its Aug 2021 consolidation (doc 169604). I checked every payouts-based cash event with a yield of 4% or more against the price. Before the fix ZAL (a 27% yield with no price drop at all) was the only failure at 8% or more; between 4% and 8%, SNGP 2025-05 (worst day three days before the computed ex date) and GEMPAPL 2026-03 (a stock at a few rupees) show no dip on the ex date, and neither points to par. Below 4% a wrong par cannot be seen in the price, so other Re1 or Rs5 names remain a risk and are not flagged.
4. **Ex-date rule.** The task said book-closure start minus one business day. The data say two trading days until early March 2026 and one from then on: among 88 payouts with a yield of 3% or more, the worst day in ex-3 to ex+2 is the computed ex date in 61, and PDF-dated events from 2017 to 2024 match their price gaps (PPL 2018 and 2019, AVN 2017, AKBL 2020, SPWL 2021, KAPCO 2022, TPLP 2023). That is T+2 settlement, then T+1. The switch is placed at book-closure starts on or after 2026-03-05 (MTL starting 4 Mar still dips at -2, OGDC starting 7 Mar dips at -1). Splits are different: the entitlement date is the Friday before a Saturday closure and the ex date is the first trading day of the new shares, which is also the date of the exchange's "credit of ordinary shares pursuant to the sub-division" notice (checked on LUCK, SYS, UBL and others).
5. **Where the price decided the date or the size.** Rows with `ex_date_source` of `approx` or `approx_wide` take their date from a price move that matches the stated value (tolerance 1.5% plus 6% of the expected move, wider for big events, ambiguous matches rejected, never for expected moves under 8%): `approx` when within 15 trading days of the announcement, `approx_wide` when later or when the only notice was a credit notice after the fact. `gap_inferred` rows have no stated value at all: a bonus announcement exists for the symbol, exactly one suspect gap fell in the window, and the size is the gap rounded to 5%. Their size can be off by several points (PPL 2018: the gap implied 18.3%, the notice says 15% bonus plus Rs1.50 cash) and larger bonuses are rounded coarsely. 107 such rows. Treat them as "a bonus happened here" rather than as exact.
6. **Date verification.** Book-closure dates from the portal or a PDF were checked against the price when the expected drop is 8% or more. Those where neither the ex date nor the days either side showed even 40% of the expected drop, and no matching gap lay within 3 trading days, went to the unplaced file instead of being applied on a day with no drop: 2 rows (GGL bonus 0.1; TOMCL bonus 0.0975).

## Coverage by year (placed actions, by ex-date year)

| ex year | bonus | cash | right | split | total |
|---|---|---|---|---|---|
| 2016 | 4 | 0 | 0 | 0 | 4 |
| 2017 | 10 | 2 | 0 | 0 | 12 |
| 2018 | 25 | 1 | 0 | 0 | 26 |
| 2019 | 20 | 2 | 0 | 0 | 22 |
| 2020 | 15 | 1 | 0 | 0 | 16 |
| 2021 | 27 | 21 | 0 | 2 | 50 |
| 2022 | 20 | 22 | 0 | 0 | 42 |
| 2023 | 23 | 28 | 0 | 0 | 51 |
| 2024 | 5 | 18 | 1 | 0 | 24 |
| 2025 | 6 | 191 | 3 | 12 | 212 |
| 2026 | 4 | 153 | 2 | 7 | 166 |

By source of the ex date:

| ex year | approx | approx_wide | credit_notice | gap_inferred | payouts_book_closure | pdf_book_closure | pdf_resume_date | seed |
|---|---|---|---|---|---|---|---|---|
| 2016 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| 2017 | 0 | 1 | 0 | 8 | 0 | 3 | 0 | 0 |
| 2018 | 1 | 2 | 0 | 18 | 0 | 5 | 0 | 0 |
| 2019 | 1 | 0 | 0 | 16 | 0 | 5 | 0 | 0 |
| 2020 | 3 | 1 | 0 | 10 | 0 | 2 | 0 | 0 |
| 2021 | 1 | 3 | 0 | 21 | 0 | 3 | 1 | 21 |
| 2022 | 1 | 3 | 0 | 15 | 0 | 2 | 0 | 21 |
| 2023 | 6 | 4 | 0 | 10 | 0 | 10 | 0 | 21 |
| 2024 | 1 | 2 | 0 | 3 | 1 | 1 | 0 | 16 |
| 2025 | 0 | 0 | 6 | 2 | 182 | 0 | 5 | 17 |
| 2026 | 0 | 1 | 5 | 0 | 145 | 0 | 2 | 13 |

Liquid names (60-day median traded value above Rs5m on 1 January) with at least one placed action in the year. The cash column is what limits the total-return panel before 2025:

| year | liquid names (Rs5m, 1 Jan) | with a cash action | with a bonus action | with a split action |
|---|---|---|---|---|
| 2017 | 122 | 2 | 5 | 0 |
| 2018 | 69 | 1 | 8 | 0 |
| 2019 | 83 | 2 | 9 | 0 |
| 2020 | 95 | 1 | 7 | 0 |
| 2021 | 110 | 7 | 17 | 1 |
| 2022 | 96 | 7 | 7 | 0 |
| 2023 | 71 | 9 | 4 | 0 |
| 2024 | 133 | 7 | 3 | 0 |
| 2025 | 160 | 65 | 4 | 6 |
| 2026 | 193 | 57 | 0 | 2 |

Placed rows by source: payouts_book_closure 362, seed 109, gap_inferred 107, pdf_book_closure 31, approx_wide 17, approx 14, credit_notice 11, pdf_resume_date 8.

## Suspected gaps (`data/suspected_corporate_actions.csv`, 801 rows)

A suspect is explained when an action in the table applies on that date and the adjusted move is back inside the circuit band. It is unexplained when no action applies there.

- Explained: **156** of 801. Remaining: **645**.
- Liquid names (traded value above Rs5m, 125 suspects): explained **71**, remaining **54**.
- Applied but still outside the band after adjustment: 0.

| year | suspects | explained | remaining |
|---|---|---|---|
| 2016 | 18 | 4 | 14 |
| 2017 | 65 | 10 | 55 |
| 2018 | 81 | 22 | 59 |
| 2019 | 101 | 17 | 84 |
| 2020 | 119 | 12 | 107 |
| 2021 | 116 | 29 | 87 |
| 2022 | 101 | 22 | 79 |
| 2023 | 121 | 23 | 98 |
| 2024 | 46 | 5 | 41 |
| 2025 | 20 | 8 | 12 |
| 2026 | 13 | 4 | 9 |

What the remaining 645 look like, by the kind of corporate-action announcement the same symbol made in the 100 days before to 45 days after the gap (this says an announcement exists, not that it caused the gap):

| announcement near | down | up | total |
|---|---|---|---|
| bonus | 15 | 3 | 18 |
| cash | 169 | 37 | 206 |
| none | 248 | 131 | 379 |
| right | 41 | 1 | 42 |

"none" means no announcement mentioning dividend, bonus, right or split was found for that symbol in the window; these can be real crashes, data glitches (BML 2026-02-02 is +1,626% on a day with 0.23x normal volume) or actions announced in words my filters missed. Down-gaps next to a "cash" announcement are plausibly ex-dividend days whose amount I could not retrieve, but that is a guess from timing only. Several of the largest down-gaps (FFL 2017 -63%, SGPL 2026 -59%, GGGL 2021 -33%, UNITY 2019 -22%, PRL 2020 -22%) coincide with right-issue announcements; rights are in the table only when the portal listed them and the loader ignores rights, so those days are zeroed.

Twenty largest unexplained gaps in liquid names:

| symbol | date | move | volume ratio | 60d median traded value (Rs m) | announcement near |
|---|---|---|---|---|---|
| BML | 2026-02-02 | 1626.5% | 0.2316 | 103.6 | none |
| FFL | 2017-09-20 | -63.1% | 0.02564 | 9.2 | right |
| SGPL | 2026-08-19 | -59.5% | 0.01048 | 127.4 | right |
| GGGL | 2021-01-14 | -33.1% | 2.183 | 11.5 | right |
| GHGL | 2021-01-14 | -25.9% | 0.6175 | 9.5 | right |
| WAFI | 2021-01-04 | -25.6% | 0.9317 | 89.7 | none |
| MTL | 2022-03-07 | -23.0% | 2.426 | 16.7 | bonus |
| STPL | 2018-05-28 | -23.0% | 1.399 | 25 | right |
| UNITY | 2019-03-13 | -22.4% | 2.853 | 48.8 | right |
| PRL | 2020-03-03 | -22.2% | 0.5726 | 24.1 | right |
| LOADS | 2021-01-12 | -19.6% | 1.812 | 7.1 | right |
| IMAGE | 2021-07-29 | -18.4% | 0.6635 | 26.9 | right |
| GCIL | 2025-04-03 | -17.8% | 0.6363 | 69.7 | cash |
| MTL | 2019-10-17 | -17.2% | 1.417 | 8.7 | bonus |
| NBP | 2026-03-17 | -16.8% | 0.9341 | 2471 | cash |
| PICT | 2024-11-07 | -16.7% | 1.656 | 8 | cash |
| AHL | 2025-10-13 | -16.6% | 2.395 | 11.4 | cash |
| FFL | 2021-10-26 | -16.0% | 1.112 | 35.4 | right |
| PICT | 2023-09-06 | -15.9% | 1.281 | 22.7 | cash |
| KAPCO | 2023-10-16 | -15.1% | 2.886 | 38.3 | cash |

One cause I did read: GCIL 2025-04-03 follows a court-sanctioned demerger (doc 249387: 500 GCWL shares per 1,000 GCIL, notice 10 Mar 2025). The others are not diagnosed.

## The five checks the task named

| symbol | ex date | event | raw move | adjusted move | table rows |
|---|---|---|---|---|---|
| LUCK | 2025-04-28 | 5:1 split | -79.5% | +2.5% | split 5 [pdf_resume_date] |
| SYS | 2025-06-02 | 5:1 split | -81.0% | -5.0% | split 5 [seed] |
| SYS | 2022-03-31 | 100% bonus (+Rs5 cash) | -47.2% | +6.3% | bonus 1 [seed]; cash 5 [seed] |
| MEBL | 2022-08-22 | 10% bonus (+Rs1.75 cash) | -9.5% | +0.8% | bonus 0.1 [seed]; cash 1.75 [seed] |
| MEBL | 2021-09-09 | 15% bonus (+Rs1.50 cash) | -11.8% | +2.5% | bonus 0.15 [seed]; cash 1.5 [seed] |

The adjusted move on each is inside ordinary daily noise, so all five are handled. MEBL 2021 and 2022 and SYS 2022 come from the seed (ground truth); LUCK 2025 from the book-closure notice (doc 249947: Rs10 to Rs2, trading resumed 28 Apr 2025); SYS 2025 is in the seed and agrees with the exchange's credit notice of the same day.

## Seed cross-check

Seed rows: 109 (MEBL, FFC, HUBC, OGDC, SYS, EPCL). 33 of them were also found independently (payouts or price gap); the rest cover 2021 to Oct 2024, which no other source reaches. The seed wins every overlap. Disagreements:

| symbol | type | seed_ex | seed_value | our_ex | our_value | our_source | ex_diff_days | value_ratio_minus_1 |
|---|---|---|---|---|---|---|---|---|
| MEBL | cash | 2026-03-16 | 7 | 2026-03-24 | 7 | payouts_book_closure | 8 | 0 |
| SYS | bonus | 2022-03-31 | 1 | 2022-03-31 | 0.9 | gap_inferred | 0 | -0.1 |

Notes on those: MEBL 2026-03: the seed says ex 16 Mar, the portal's book closure (25 Mar to ...) gives 24 Mar. A Rs7 dividend on a price of about Rs445 is under 2% and cannot be seen in the price, so I cannot arbitrate; the seed date is used. OGDC 2026-03: closure started on a Saturday, so the switch date mattered; the switch was moved to 5 Mar to agree with the seed. SYS 2022-03-31: the seed says 100% bonus, the price-gap estimate was 90% (the gap is 47% plus market noise); the seed is used. Cash amounts that disagreed with the seed: 0.

## Sources and method in one paragraph

Order of trust: seed, then portal payouts (book closure range), then book-closure dates and ratios read from filing PDFs, then price-matched placement of a stated value, then gap-inferred size. Announcement titles state a percentage or a Rs amount in only 344 of the 5460 dividend, bonus, right and split rows found; most notices are "credit of dividend" or "dispatch of bonus certificates" with no number. Most filing PDFs are scanned images with no text layer and no OCR was available, so I read them by eye from rendered pages and typed what they state into `data/corporate_actions_pdf_reads.csv`. Of the 153 documents downloaded, 84 gave at least one row. The rest had a profit-and-loss table or a material-information notice on page 1, were superseded by a better document for the same event, or were never opened. I read page 1 only unless noted, so book-closure dates on page 2 are missing for some rows (those events then rely on a price match). Priority order for downloads: splits, then bonus declarations for the 92 liquid names and the rest of KMI All Share, then results letters for the 40-odd bonus events that had no declaration notice, then the largest unexplained gaps in liquid names. 153 of 400 downloads used. Usable rows per document read were roughly 79% for results letters picked from bonus announcements and 37% for letters picked only by date proximity to an unexplained gap, so the remaining budget was not spent; covering the cash dividends of 92 names across 2017 to 2024 would need roughly 2,000 documents (92 names, 8 years, 2 to 3 declarations a year; an estimate).

## Not done, and what would fix it

- Cash dividends 2017 to Oct 2024 for most names. Needs a dividend history source (the portal shows two years). With one, `build.py` takes it as another row source.
- Small bonuses (under 8%) without a book-closure date. 28 bonus rows have a value but no date; they are in the unplaced file.
- Rights: 161 rights notices are unplaced; ex-right adjustment (theoretical ex-rights price) is not implemented and the loader ignores rights.
- Delisted and merged names are not in the panel (survivorship). FFC/FFBL merger issuance (Dec 2024) is not a price event and is not in the table.
- Weekly or later refresh: rerun `scripts/ca/build.py`, then `recon.py`, then `notes.py`.
