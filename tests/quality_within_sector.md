# Quality within sector (point in time)

Run 18 Oct 2026. Script `scripts/tests/quality_within_sector.py`, raw output `tests/out/quality_within_sector.txt`.

## Hypothesis
Within a PSX sector, names with higher operational quality (return on equity, cash conversion, steady earnings, dividend cover) earn higher 12-month returns than low-quality names, and quality plus cheapness beats the equal-weight liquid KMI basket and KMI30 members.

## Data
- `data/fundamentals/quarterly_eps.csv`: 129 names, StockAnalysis figures, consolidation unverified. The file is effectively 2021Q3 to 2026Q2 (20 quarters); only 18 of 2,460 rows are older. Availability date is `first_tradable_date` (15:30 rule); the 20% of rows without an announcement are assumed available 95 days after quarter end (95th percentile of observed lags).
- `seed/data/fundamentals/sa_ratios.csv`: fiscal-year P/B.
- `data/corporate_actions.csv`: cash dividends, complete only from Nov 2024.
- Returns: `prices.returns(close, "adjusted")` (total return), bought at the close of the formation day.
- Sector: PSX `sectorName` from `data/symbols.csv` (the repo sector tables do not cover every name), with textile composite and spinning merged, and the two auto groups merged. Sectors with fewer than 3 scored names drop out.
- Universe at each formation: KMI All Share member (latest derived list on or before the date) with trailing 60-day median traded value above Rs5m.
- Survivors only (names listed on 16 Oct 2026), so every basket here is flattered.

## Method (definitions fixed in advance, not tuned)
- (a) ROE proxy = trailing-4-quarter net income / equity at the latest published fiscal year end, where equity = shares x price on that year end / P/B. If unavailable (median 16 names per formation), fallback = minus the standard deviation of the last four year-on-year net income growth rates (clipped to -100% to +300%), ranked only against other fallback names.
- (b) Cash conversion = trailing-4-quarter operating cash flow / net income, clipped to 0 to 2; 0 if net income is not positive.
- (c) EPS stability = minus the coefficient of variation of the last 8 quarterly EPS; worst if mean EPS is not positive.
- (d) Payout = trailing 12-month cash dividends / trailing EPS (cap 1.5), only where dividends are recorded and only when the 12-month window lies inside the complete record (formation from Nov 2025). It is therefore never used in the backtest, only in the current screen.
- Score = mean of the within-sector percentile ranks of the available components. Top third and bottom third by within-sector rank (round(n/3) names, at least 1). Quality-plus-value (QARP) = top half by quality, then the cheaper half by earnings yield (trailing net income / (shares x price)), within sector.
- Formation on the first trading day of each month, hold 12 months, overlapping. Annual non-overlapping cohorts are shown for each of the 12 month offsets.
- Placebo: random ranks within the same sectors and counts, 2000 draws of the whole formation path.
- Because (c) needs 8 quarters, the primary sample runs from Sep 2023 to Oct 2025 (26 formations). A second sample using only (a) and (b) runs from Nov 2022 (36 formations).

## Results
Percent, 12-month holds. Win = share of formations above zero.

| Primary (a, b, c), n = 26 formations, 3 annual episodes | mean | median | win | worst |
|---|---|---|---|---|
| Top third, raw | +51.7 | +57.7 | 92% | -7.6 |
| Bottom third, raw | +42.5 | +37.8 | 92% | -14.1 |
| Top minus bottom | +9.2 | +5.8 | 69% | -33.2 |
| QARP minus EW liquid KMI | +4.1 | +2.4 | 54% | -22.2 |
| QARP minus KMI30 members EW | +7.7 | +0.7 | 54% | -14.5 |
| QARP minus all scored names (selection effect) | +2.0 | -0.3 | 46% | -26.3 |
| EW liquid KMI, raw | +46.7 | +51.3 | 92% | -10.0 |

Annual cohorts (formed October): top minus bottom +103.1 (2023), -33.2 (2024), +6.4 (2025). QARP minus KMI +51.6, +16.0, -1.0. The benchmark itself returned +73.7, +91.9, -10.0. Across the 12 month offsets, top minus bottom averages +8.3 (positive in 10 of 12 offsets); QARP minus KMI averages +3.6 (positive in 5 of 12).

Placebo: top minus bottom observed +9.2 against a placebo mean of -0.1 (5 to 95 percent band -10.0 to +9.3), p = 0.054. QARP minus KMI observed +4.1 against placebo +2.1 (band -3.3 to +7.6), p = 0.26. The placebo QARP is already +2.1 above the basket, which is the pure effect of holding the scored names rather than the whole liquid basket.

| Extended (a, b only), n = 36 formations, 3 episodes | mean | median | win | worst |
|---|---|---|---|---|
| Top minus bottom | +22.6 | +8.2 | 67% | -18.4 |
| QARP minus EW liquid KMI | +20.7 | +7.3 | 72% | -18.0 |
| QARP minus KMI30 members EW | +26.6 | +9.6 | 69% | -13.9 |

Placebo p = 0.001 (top minus bottom) and 0.000 (QARP minus KMI). October cohorts of QARP minus KMI: +54.1, +36.9, -1.9.

## Robustness
- Split. A 2020-21 versus 2022-26 split is impossible: no fundamentals before 2021Q3 and no formation before Sep 2023. Replacement split by formation date (primary): formed before Sep 2024, top minus bottom +18.0 (n = 12), QARP minus KMI +4.3 mean but median -2.6, win 33%; formed Sep 2024 onwards, top minus bottom +1.7 (median +5.3), QARP minus KMI +3.8 (median +4.9, win 71%).
- Rerating. Every holding window is inside the 2022-25 rerating or its tail, so it cannot be removed by dropping dates. Two reads that remove it: excess over the basket, and the last cohort. The extended sample shows what the rerating does: formations of Nov 2022 to Aug 2023 give QARP minus KMI +46.7 (median +24.6, n = 10) while the basket returned +60.1; restricting the extended signal to the primary window gives +10.6 (median +6.1, win 73%, n = 26), versus +4.1 with (c) included. So most of the extended result is the early window, not the signal.
- Last cohort (formed Sep-Oct 2025, held to Sep-Oct 2026, n = 2 formations): top +1.1, bottom -2.4, QARP -0.4, basket -2.7, KMI30 members +5.6.
- Single components (extended sample, exploratory): cash conversion alone top minus bottom +35.3 (median +14.8, win 83%); ROE proxy alone +6.7 (median +2.6, win 58%, worst -100.2 from one name). Two looks, no correction.

## Verdict
Weak, not proven. Under the pre-registered primary spec, quality within sector has a positive median spread (+5.8 points, 69% of formations) but it comes from three independent years, one of which (Oct 2023, +103) supplies most of the mean and another (Oct 2024) is -33. The placebo gives p = 0.054. Quality-plus-value adds +2.4 points median over the liquid KMI basket, wins in 54% of formations, p = 0.26, and does not beat KMI30 members at the median (+0.7). The less restrictive (a, b) version looks strong, but most of that comes from the fastest part of the rerating, and the placebo does not control for that window. Cash conversion is the only component that looks like it is doing the work; that is a hypothesis for the next data pull, not a finding.

## Caveats
- Three episodes. Everything is inside one rerating regime. No 2020-21 data exists in this file.
- Survivorship: delisted names are absent; the sign of the bias on a quality spread is unknown.
- Dividends: before Nov 2024 the adjusted returns miss many cash dividends, which understates high payers. The payout component was not tested historically.
- Consolidation of EPS unverified (lesson 1). Q4 figures are derived (annual less nine months). Shares are rounded to whole millions; names under 50 million shares use EPS-based yield and the growth fallback for (a). The fallback is used for a median 16 names, so the ROE component is partly something else.
- Operating cash flow is not a quality signal for banks (3 names). Sector sizes are small (median 12 sectors, about 6 names each), so terciles are 1 to 3 names.
- Equity is from the fiscal year end, up to 15 months before the formation date. P/B in `sa_ratios` is assumed to use the price at year end (unverified).
- The current screen below is a display ranking, not part of the tested rule.

## Current screen (prices to 16 Oct 2026; liquid KMI names, 112 scored, 31 pass quality-plus-value)

| Name | Sector | Quality | ROE % | Cash conv. | EPS CV | Payout | E/P % |
|---|---|---|---|---|---|---|---|
| FCL | Cable and electrical | 0.88 | 12.9 | 0.00 | 0.52 | 0.46 | 13.3 |
| FFC | Fertilizer | 0.83 | 33.2 | 1.32 | 0.12 | 0.67 | 11.4 |
| ISL | Engineering | 0.85 | 13.7 | 0.00 | 0.54 | 0.59 | 10.7 |
| PRL | Refinery | 0.83 | 36.9 | 1.01 | 2.87 | n/a | 23.4 |
| IPAK | Paper and packaging | 0.81 | 23.5 | 0.44 | 0.91 | 0.29 | 21.2 |
| PIBTL | Transport | 0.83 | 17.9 | 1.39 | 1.63 | n/a | 13.8 |
| SNGP | Gas marketing | 0.78 | 20.6 | 2.00 | 0.44 | 0.13 | 25.4 |
| NETSOL | Technology | 0.71 | 17.6 | 1.16 | 0.94 | n/a | 22.0 |
| LUCK | Cement | 0.65 | 18.8 | 0.62 | 0.12 | 0.08 | 15.2 |
| ABOT | Pharma | 0.63 | fallback | 0.98 | 0.21 | 0.46 | 9.3 |

FCL and ISL show cash conversion 0.00 (operating cash flow negative), so their scores rest on the other components. PRL earnings are very unstable (CV 2.87). These are screens, not recommendations; none has been checked against a filing.
