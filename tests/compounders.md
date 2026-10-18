# compounders: which businesses compounded, what was visible early, does a growth rule beat the index

Run 18 Oct 2026. Script `scripts/tests/compounders.py`, raw output `tests/out/compounders.txt`. Data to 16 Oct 2026.

## Hypothesis

(A) Some liquid PSX businesses made 3x or more over five years, and the share that did is a measurable base rate. (B) Features visible at the start separate them from same-sector names that did not. (C) A pre-registered growth-core rule (within-sector rank of trailing EPS CAGR, ROE and 1 minus payout; top 8 equal weight; semiannual rebalance; sell on leaving the top 20 or KMI) beats the KMI All Share total-return index and the equal-weight liquid basket.

## Data

- Prices: 453 listed names in the panel, 44 listed names that were missing from it (`prices_listed_missing`), 117 delisted names with price files; funds, ETFs and bonds excluded. Liquid means 60-day median traded value above Rs5m at the window start.
- **Dividends are a floor.** `corporate_actions.csv` has cash dividends only from about Nov 2024 (6 cash rows for 2017 to 2020). Before that, "total return" for the names is price plus bonus and split. It understates by roughly the dividend yield; the KMI All Share TR comparator includes dividends in full. The 44 listed-missing and all delisted names have no action rows at all.
- 25 one-day moves of -60% or worse or +200% or better (unrecorded splits; 21 names) were set to zero. STL was excluded from the rule universe by hand: two unexplained 28% to 91% one-day drops in 2026 and a P/E of 0.8.
- **Fundamentals are short.** `sa_ratios.csv` starts at FY2020 (a handful of names), mostly FY2022. `quarterly_eps.csv` holds 20 quarters, 2021Q3 to 2026Q2 for 108 of 129 names; only one name reaches back to 2019. The extension to 2019 asked for is not possible. A trailing 3-year EPS CAGR first exists for the TTM ending 2025-06, known from Oct 2025. StockAnalysis annual pages also stop at five fiscal years (checked on LUCK), so there is no other source in reach.
- KMI membership: derived lists from 2019-01 contain current symbols only, so delisted names have no KMI flag before or after.

## Method

Pre-registered in the script header before any result. Windows start on each month-end from 2016-12-30 with end at +5 years; the decade is 2016-12-30 to 2026-10-16 (9.8 years). B uses annual cohorts and a within cohort-sector permutation (5000 draws). C scores at each quarter-end, fills at the next close that is not limit-locked (upper lock on buys, lower on sells; lock = move within 0.5 points of 10%), costs 0.25% a side plus 0.25% a side under Rs20m traded value. Rule start: first quarter-end with at least 30 eligible names. Placebo: 200 random-entry runs with the same dates, costs, fills and the rule's own exit rate. Deviation: the registered horizon is 3 years; 2 and 1 year run beside it only because 3 years gives 1.04 years of history.

## Results

### A. Population

| 5-year start | liquid names | >=2x | >=3x | >=5x | >=10x | names with 3x |
|---|---|---|---|---|---|---|
| 2016-12-30 | 155 | 5.2% | 3.2% | 1.3% | 0.6% | 5 |
| 2017-12-29 | 85 | 4.7% | 2.4% | 0.0% | 0.0% | 2 |
| 2018-12-31 | 97 | 14.4% | 5.2% | 1.0% | 1.0% | 5 |
| 2019-12-31 | 111 | 43.2% | 16.2% | 7.2% | 0.9% | 18 |
| 2020-12-31 | 124 | 40.3% | 23.4% | 7.3% | 1.6% | 29 |
| 2021-09-30 | 137 | 41.6% | 21.2% | 12.4% | 1.5% | 29 |
| pooled, 58 starts | 108 avg | 24.7% | 12.1% | 4.5% | 0.7% | |

75 names had a 3x window; 51 are in KMI now, 4 ended (FFBL, PIAA, PSMC, SERF). Best-window multiple median 4.7x; 34 reached 5x, 9 reached 10x. 38 of the 75 best windows start in 2020 and 25 in 2021. Only 39 independent sector-by-start-year clusters sit behind the 75. Share of liquid names that made 3x in some window, by sector: fertilizer 5 of 7, E&P 3 of 4, power 6 of 9, cement 10 of 16, banks 11 of 18, tech 6 of 12, autos 5 of 16, textiles 2 of 20, investment banks and securities 3 of 15.

The biggest, best-window multiples (dividends partly missing): THCCL 24.2x, SAZEW 16.5x, AGL 15.3x, SYS 14.0x, GAL 12.2x, GHNI 11.8x, FFC 10.8x, PNSC 10.6x, MEBL 10.4x. Full list with sector, KMI flag and window dates is in the raw output.

Decade (155 liquid at the start): median 1.14x; 2x 28.4% (44 names), 3x 20.0% (31), 5x 5.2% (8), 10x 3.2% (5: SAZEW 23.5x, MEBL 22.6x, SYS 18.9x, AHL 10.6x, FFC 10.4x). KMI All Share TR over the span: 2.89x. The median liquid name did not match the index.

Regime at the window start (6M T-bill vs policy rate): 3x share 14.6% when the bill was above the policy rate (39 starts) and 7.0% when at or below (19 starts). Both are drawn from the same few years, so this is not an independent split.

### B. What was visible early

Price-only features, five annual cohorts (88 winner-cohorts, 52 distinct names), percentile of each winner among same-cohort same-sector non-winners (0.50 is no information):

| Feature | winners | groups | mean percentile | permutation p |
|---|---|---|---|---|
| 12-month momentum | 76 | 36 | 0.51 | 0.83 |
| size (log median traded value) | 81 | 39 | 0.44 | 0.22 |

Winners had a median 12-month momentum of -7% against -3% for non-winners; 39% of winners sat above their cohort median. Sector was the visible variable (table above), not the stock.

Fundamentals can be tested for one cohort only: 52 names liquid at 2023-10-31 with a 1-year EPS growth, a 2.96-year run, winner = 2x. Winners 31 (60%); cement 7 of 7, refineries 4 of 4, E&P 3 of 3. Within-sector Spearman against the demeaned log multiple: 1-year EPS growth -0.03 (p 0.87), ROE +0.06 (0.71), payout -0.07 (0.68), revenue growth +0.28 (0.10), size -0.08 (0.65), P/E -0.24 (0.19), momentum -0.01 (0.96). No correction for seven features; nothing clears 0.10.

Decomposition of the multiple (shares of the log multiple, median per winner):

| Window | winners | EPS growth | re-rating | dividends (floor) | P/E start to end |
|---|---|---|---|---|---|
| 4 years from 2022-10-17, 3x | 17 (16 usable) | 56% | 31% | 4% | 4.7 to 6.2 |
| 3 years from 2023-10-31, 2x | 31 (27 usable) | 38% | 59% | 4% | 5.4 to 7.3 |

Re-rating supplied more than half the log return for 5 of 16 and 15 of 27. A five-year decomposition is not possible: no 5-year window has a start EPS in the data.

### C. The growth-core rule

Every 5-year window and the decade: zero are testable. Longest feasible spans below. "Fixed" is Rs50k once; "deposits" is Rs50k, Rs50k, then Rs100k a month (money-weighted CAGR).

| Variant, start | years | Fixed multiple (CAGR) | KMI TR | EW liquid KMI | Placebo median (rule pctile) | Max DD (rule / KMI) | Turnover/yr |
|---|---|---|---|---|---|---|---|
| 3y growth, 2025-09-30 | 1.04 | 0.88x (-11.7%) | 0.96x | 0.88x | 0.93x (30) | -27.9 / -21.3 | 1.73x |
| 3y + quality | 1.04 | 0.82x | 0.96x | 0.88x | 0.86x (35) | -35.5 / -21.3 | 1.53x |
| 2y growth, 2024-09-30 | 2.04 | 1.73x (+30.6%) | 1.81x (+33.6%) | 1.50x | 1.88x (30) | -28.6 / -21.3 | 1.22x |
| 2y + quality | 2.04 | 1.71x | 1.81x | 1.50x | 1.91x (24) | -33.4 / -21.3 | 1.31x |
| 1y growth, 2023-09-28 | 3.05 | 2.80x (+40.2%) | 2.87x (+41.2%) | 2.19x | 2.80x (51) | -33.1 / -21.3 | 1.46x |
| 1y + quality | 3.05 | 2.82x | 2.87x | 2.19x | 2.69x (56) | -35.7 / -21.3 | 1.36x |

With deposits: 3y 0.97x (-5.6%) vs KMI 0.99x; 2y 1.09x (+8.0%) vs KMI 1.16x (+14.8%), EW 1.04x; 1y 1.34x (+19.8%) vs KMI 1.47x (+26.5%), EW 1.26x. The rule lost to the index in every variant, beat the EW basket in all but the 3-year fixed runs, and sat inside the placebo band (5th to 95th percentile) every time.

Position level (fixed capital, net of costs): 1y variant n 39, mean +26.3%, median +6.6%, win 51%, 26% above +50%, 8% below -30%, worst -35.3%. 2y variant n 23, mean +24.6%, median +10.1%, win 61%, 26% above +50%, 4% below -30%, worst -52.6%. 3y variant n 17, mean -4.7%, median -8.0%, win 24%.

By year (1y variant, fixed): 2024 rule +65.3% vs KMI +64.8%; 2025 +37.6% vs +34.3%; 2026 to date -14.6% vs -3.5%. By regime: bill at or below policy (506 days) rule +126.2% vs KMI +118.8%; bill above policy (249 days) +23.9% vs +32.2%. Today the bill is above the policy rate (12.40% vs 11.50%).

Cohorts: the quarter-end top 8 beat the KMI over the next quarter in 5 of 9 periods, but lost 25.1% (Dec 2025 to Mar 2026) against the index's -14.0%.

**Live screen, 16 Oct 2026** (3-year EPS CAGR, 61 eligible; score is the mean of three within-sector percentiles). Not recommendations; no odds were measured.

| # | Symbol | Sector | Score | EPS CAGR | ROE | Payout | OCF/NI | P/E | 12m mom |
|---|---|---|---|---|---|---|---|---|---|
| 1 | IPAK | Paper, packaging | 1.00 | +25.8% | 26.3% | 8% | 0.44 | 4.7 | +42.7% |
| 2 | PRL | Refinery | 1.00 | +105.4% | 45.5% | 0% | 1.01 | 4.3 | +188.0% |
| 3 | THCCL | Cement | 0.92 | +203.0% | 32.9% | 5% | 0.76 | 9.1 | -28.6% |
| 4 | FABL | Banks | 0.83 | +15.7% | 19.7% | 46% | n/m | 6.1 | +4.8% |
| 5 | GGL | Chemical | 0.83 | +116.6% | 16.1% | 0% | 0.74 | 2.0 | -23.9% |
| 6 | GHNI | Autos | 0.83 | +238.3% | 38.6% | 6% | 0.96 | 6.3 | +18.9% |
| 7 | GLAXO | Pharma | 0.83 | +90.4% | 32.4% | 47% | 0.84 | 9.6 | -21.9% |
| 8 | HALEON | Pharma | 0.83 | +163.6% | 47.6% | 55% | 0.49 | 12.1 | -22.8% |
| 9 | ISL | Engineering | 0.83 | +1.4% | 14.1% | 53% | -1.08 | 9.4 | -23.2% |
| 10 | PSO | OMC | 0.83 | +39.8% | 11.4% | 18% | -2.42 | 6.8 | -22.6% |
| 11 | TATM | Textile | 0.83 | +140.3% | 14.2% | 0% | 1.63 | 2.3 | +2.0% |
| 12 | MARI | E&P | 0.78 | +15.7% | 28.8% | 41% | 1.14 | 8.7 | -13.5% |

Quality variant (OCF/NI above 0.7, 32 eligible) top 5: GLAXO, PRL, THCCL, GGL, COLG, then FATIMA, GHNI, MARI, NETSOL, TATM. In the 3-year top 20, the quality top 20 and the 2-year top 20 together: FATIMA, GGL, GHNI, GLAXO, PRL, THCCL. Reading cautions: OCF/NI is meaningless for banks (FABL -11.7); THCCL's latest quarter is 2026-03 (June year-end not yet in); PRL is already +188% in 12 months; LUCK drops out of the 3-year screen because its 2022-06 quarter is missing.

## Robustness

- Price-only features were run on annual cohorts only; denser cohorts were not run.
- The 2.5x pooled share (a price-plus-bonus proxy for 3x with dividends) is 16.7%, against 12.1% at 3x.
- Re-forming the 2-year top 8 every quarter, gross, compounds to 1.91x over the 8 quarters to 30 Sep 2026 (KMI TR 1.87x); the simulated rule nets 1.73x after costs, locks and the top-20 hysteresis (it started a month later in effect: first fills on 1 Oct 2024).
- Seeds fixed (20261018); permutation p-values move in the second decimal between runs.

## Verdict

| Sub-type | Verdict | Exit that worked |
|---|---|---|
| Five-year 3x businesses as a population | Watch: sector is visible (fertilizer, E&P, power, cement, banks), but the multiples are a 2019 to 2021 start-date effect | None measured |
| Picking the 3x name inside its sector on momentum or size | Nothing | n/a |
| Picking on EPS growth, ROE, payout, valuation | Nothing testable at five years; one 3-year cohort: nothing (no p below 0.10) | n/a |
| Growth-core rule, 3-year as registered | Nothing: 1.04 years, 0.88x vs 0.96x | Leaving the top 20 showed no gain over random exits |
| Growth-core 2-year and 1-year | Nothing: behind the index by 0.08x and 0.06x, placebo percentile 30 and 51 | Same |
| Quality variant | Nothing | Same |
| Live screen as a research list | Watch | Qualitative review before any buy |

## Caveats

1. Regime. Every result sits inside a single 2020 to 2026 re-rating (market P/E roughly 3.5x to 9x, lesson 9). 38 of 75 best 3x windows start in 2020. A growth rule that cannot beat the index inside that run has nothing to prove outside it.
2. The pre-registered test is not runnable: five years of growth data do not exist in the repo, so "does a growth rule beat the index over 5-year windows" is unanswered. This run answers only the 1 to 3-year version.
3. Survivors in C: the rule universe is 129 currently listed names with quarterly data; two names were dropped for data (STL, LUCK 3-year).
4. Missing dividends before Nov 2024 depress the multiples in A and B; the index comparator is not like for like there. In C the 3-year variant starts after dividends become complete; the 2-year (from Sep 2024) and 1-year (from Sep 2023) variants have incomplete dividends in their early months against a full-dividend index, which flatters the index.
5. 25 repaired one-day moves and the delisted names (crude returns, last print as exit) add noise to the tail.
6. No multiple-comparison correction on seven features.
