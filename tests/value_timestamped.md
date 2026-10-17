# Value with true publication dates

Run 17 Oct 2026. Script `scripts/tests/value_timestamped.py`, raw output `tests/out/value_timestamped.txt`. Every number below is from that output. Returns are percent, 12-month price return unless stated. The spec's section 6 named `tests/value_pubdates.md`; the task named this file, so this is the one written.

## Hypothesis

H1: names with a high earnings yield beat expensive names over the next 12 months, ranked overall (T1) and within sector (T2). H2 (T3): the effect holds among names with ROE above the cohort median. H3 (T4): the effect holds among names in the top-half sectors by 6-month momentum. Verdict options: standalone edge, tiebreaker, nothing. This redoes the seed value test, which used an assumed reporting lag (lesson 18).

## Data

- 108 names in `sa_ratios.csv`, 530 fiscal-year rows (TTM dropped). `pe` is blank on 114 rows: 71 with ROE below 0, 30 with ROE above 0, 13 with ROE blank. All 108 are in the price panel. Sector codes: 26 distinct (current, from the 16 Oct 2026 screener).
- Publication dates: 1,883 annual-result announcements for these names; 1,817 after dropping REVOKED; 154 of those have a title with no parseable period end. Of 530 fiscal-year rows, 455 were matched to an announcement, 1 through the `quarterly_eps.csv` Q4 fallback, 74 are unpublished (no match within 0 to 150 days). Median announcement lag 82 days (range 23 to 147). 22 matched timestamps fall after 15:30 and roll to the next session; none sit at exactly 00:00.
- Prices: `panel_close_adj_pricereturn.parquet` (bonus and split adjusted, price only). Total return: `panel_close_adj.parquet` (cash complete only from Nov 2024).

## Method

One formation date a year, the last panel trading day of October: 29 Oct 2021, 31 Oct 2022, 2023, 2024, 2025. Fundamentals are each name's latest sa_ratios fiscal year whose first tradable session is on or before the formation date; excluded if that year ended over 18 months earlier. `ey_fye` is 1/pe, else roe/pb if pb is positive (loss-makers stay, negative), else the name is dropped. `ey_form = ey_fye x Padj(FYE) / Padj(formation)`. Eligible: traded in the last 10 days and in `liquid_universe(F, 5e6)`. Tercile rule everywhere: percentile rank above 2/3 is top, at or below 1/3 is bottom. T2 ranks inside sectors with at least 3 eligible names. T3 keeps ROE above the cohort median. T4 keeps the top half of sectors (at least 3 of the 108 names with a 6-month return) by equal-weight 6-month return to the formation date. Outcome: formation close to the last panel day of the next October (16 Oct 2026 for the 2025 cohort). Costs: 1.0 pt on top-minus-bottom, 0.5 pt on top-minus-universe. "Universe" is all eligible names in the cohort, in every test. Placebo: shuffle returns inside each ranking unit (equivalent to shuffling ey_form), 2,000 draws, seed 20261017. The same shuffle gives gross and net p-values.

## Results

**Sample accounting** (names removed in sequence from 108)

| Cohort | No published FY | Stale | No ey | No price | Before liquidity | Liquidity removed | Eligible | roe/pb fallback | Loss-makers kept | T2 thin-sector excluded |
|---|---|---|---|---|---|---|---|---|---|---|
| Oct 2021 | 103 | 0 | 0 | 0 | 5 | 1 | 4 | 0 | 0 | n/a |
| Oct 2022 | 25 | 0 | 1 | 0 | 82 | 38 | 44 | 2 | 2 | 12 |
| Oct 2023 | 18 | 3 | 0 | 1 | 86 | 37 | 49 | 6 | 5 | 13 |
| Oct 2024 | 14 | 2 | 2 | 0 | 90 | 21 | 69 | 9 | 8 | 15 |
| Oct 2025 (partial, 11.5 months) | 9 | 2 | 1 | 0 | 96 | 11 | 85 | 11 | 9 | 15 |

Oct 2021 is skipped: 4 eligible names, below 30. That leaves 4 independent episodes.

**Per cohort** (top / bottom tercile; spreads are top minus bottom; win rate is the share of top names beating the universe mean)

T1, overall terciles

| Cohort | n t/m/b | Mean top / bottom | Median top / bottom | Universe | Win | Worst top | Spread mean | Spread median | Net 1.0 | Top-univ net 0.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| Oct 2022 | 15/15/14 | +16.9 / -3.8 | +11.0 / -8.0 | +7.0 | 53% | -25.4 (EPCL) | +20.8 | +19.0 | +19.8 | +9.4 |
| Oct 2023 | 17/16/16 | +50.6 / +69.9 | +39.2 / +33.8 | +66.6 | 35% | -33.2 (LOTCHEM) | -19.3 | +5.4 | -20.3 | -16.5 |
| Oct 2024 | 23/23/23 | +81.5 / +76.0 | +75.0 / +63.4 | +72.8 | 57% | -12.8 (EPCL) | +5.5 | +11.6 | +4.5 | +8.3 |
| Oct 2025 | 29/28/28 | -2.9 / +5.0 | -7.6 / -17.7 | +2.5 | 41% | -39.3 (WAVES) | -7.9 | +10.1 | -8.9 | -5.9 |

T2, within-sector terciles

| Cohort | n t/m/b | Mean top / bottom | Median top / bottom | Universe | Win | Worst top | Spread mean | Spread median | Net 1.0 | Top-univ net 0.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| Oct 2022 | 12/10/10 | +13.8 / +4.6 | +12.5 / -1.8 | +7.0 | 58% | -27.5 (TELE) | +9.2 | +14.3 | +8.2 | +6.3 |
| Oct 2023 | 15/11/10 | +100.0 / +40.6 | +45.1 / +30.3 | +66.6 | 33% | -19.5 (EPCL) | +59.4 | +14.7 | +58.4 | +32.9 |
| Oct 2024 | 22/18/14 | +71.4 / +73.8 | +50.6 / +59.4 | +72.8 | 41% | -12.8 (EPCL) | -2.4 | -8.8 | -3.4 | -1.9 |
| Oct 2025 | 26/24/20 | -7.4 / +2.8 | -15.1 / -10.0 | +2.5 | 27% | -64.7 (UNITY) | -10.2 | -5.2 | -11.2 | -10.4 |

T3, quality (ROE above cohort median)

| Cohort | n t/m/b | Mean top / bottom | Median top / bottom | Win | Worst top | Spread mean | Spread median | Net 1.0 | Top-univ net 0.5 |
|---|---|---|---|---|---|---|---|---|---|
| Oct 2022 | 8/7/7 | +12.3 / +7.9 | +6.3 / +10.3 | 50% | -25.4 (EPCL) | +4.4 | -4.0 | +3.4 | +4.8 |
| Oct 2023 | 8/8/8 | +37.6 / +116.9 | +35.8 / +52.2 | 38% | -19.5 (EPCL) | -79.3 | -16.4 | -80.3 | -29.5 |
| Oct 2024 | 12/11/11 | +71.9 / +27.8 | +61.8 / +31.4 | 50% | -12.8 (EPCL) | +44.1 | +30.4 | +43.1 | -1.3 |
| Oct 2025 | 14/14/14 | -9.0 / -12.0 | -14.0 / -18.2 | 36% | -35.7 (SSGC) | +3.0 | +4.2 | +2.0 | -12.0 |

T4, top-half sectors by momentum

| Cohort | n t/m/b | Mean top / bottom | Median top / bottom | Win | Worst top | Spread mean | Spread median | Net 1.0 | Top-univ net 0.5 |
|---|---|---|---|---|---|---|---|---|---|
| Oct 2022 | 7/7/6 | +15.8 / -14.8 | +0.8 / -18.9 | 43% | -20.6 (GATM) | +30.6 | +19.7 | +29.6 | +8.3 |
| Oct 2023 | 9/9/8 | +59.7 / +19.0 | +45.1 / +21.8 | 33% | +2.1 (HUBC) | +40.7 | +23.3 | +39.7 | -7.4 |
| Oct 2024 | 13/13/12 | +106.7 / +95.4 | +89.4 / +81.2 | 69% | -9.3 (CSAP) | +11.3 | +8.1 | +10.3 | +33.5 |
| Oct 2025 | 13/13/12 | -10.7 / -18.8 | -11.0 / -20.5 | 31% | -39.3 (WAVES) | +8.1 | +9.6 | +7.1 | -13.7 |

**Across cohorts and placebo** (N = 4 episodes, main run: liquidity filter, price return). Placebo columns are gross; subtract 1.0 for net. Universe means: +7.0, +66.6, +72.8, +2.5.

| Test | Mean gross | Median gross | Mean net | Median net | Net positive | Worst cohort net | Mean top-univ net | Placebo median / 5th / 95th | One-sided p |
|---|---|---|---|---|---|---|---|---|---|
| T1 | -0.2 | -1.2 | -1.2 | -2.2 | 2 of 4 | -20.3 | -1.2 (2 of 4) | +0.0 / -17.6 / +17.9 | 0.510 |
| T2 | +14.0 | +3.4 | +13.0 | +2.4 | 2 of 4 | -11.2 | +6.7 (2 of 4) | +2.9 / -15.0 / +20.1 | 0.174 |
| T3 | -6.9 | +3.7 | -7.9 | +2.7 | 3 of 4 | -80.3 | -9.5 (1 of 4) | -0.7 / -26.3 / +25.3 | 0.641 |
| T4 | +22.7 | +21.0 | +21.7 | +20.0 | 4 of 4 | +7.1 | +5.2 (2 of 4) | -0.7 / -28.4 / +28.3 | 0.100 |

The T2 placebo median is +2.9, not zero: ranking inside sectors puts more names in the top group than the bottom group in small sectors, so sector mix differs between the two pools. The placebo contains that effect.

**T4 momentum-only baseline** (eligible names in top-half sectors minus universe) against the T4 value spread:

| Cohort | In top-half sectors / eligible | Momentum minus universe, gross | Net 0.5 | T4 value spread gross | T4 value spread net 1.0 |
|---|---|---|---|---|---|
| Oct 2022 | 20/44 | -2.8 | -3.3 | +30.6 | +29.6 |
| Oct 2023 | 26/49 | +10.3 | +9.8 | +40.7 | +39.7 |
| Oct 2024 | 38/69 | +4.9 | +4.4 | +11.3 | +10.3 |
| Oct 2025 | 38/85 | -16.9 | -17.4 | +8.1 | +7.1 |
| Mean | | -1.1 | -1.6 | +22.7 | +21.7 |

**Total return beside price return** (Oct 2024 and Oct 2025 only; cash dividends complete from Nov 2024). Top / bottom / spread:

| Cohort | Test | Price | Total | Total spread net 1.0 |
|---|---|---|---|---|
| Oct 2024 | T1 | +81.5 / +76.0 / +5.5 | +86.6 / +77.4 / +9.2 | +8.2 |
| Oct 2024 | T2 | +71.4 / +73.8 / -2.4 | +75.0 / +76.3 / -1.2 | -2.2 |
| Oct 2024 | T3 | +71.9 / +27.8 / +44.1 | +78.1 / +32.1 / +46.0 | +45.0 |
| Oct 2024 | T4 | +106.7 / +95.4 / +11.3 | +113.0 / +97.5 / +15.5 | +14.5 |
| Oct 2025 | T1 | -2.9 / +5.0 / -7.9 | -0.4 / +6.1 / -6.5 | -7.5 |
| Oct 2025 | T2 | -7.4 / +2.8 / -10.2 | -5.8 / +4.1 / -9.9 | -10.9 |
| Oct 2025 | T3 | -9.0 / -12.0 / +3.0 | -5.8 / -9.4 / +3.6 | +2.6 |
| Oct 2025 | T4 | -10.7 / -18.8 / +8.1 | -9.0 / -17.9 / +9.0 | +8.0 |

Adding cash moves spreads by at most 4 points and changes no sign.

**Year-fixed-effects regression** (12m price return on within-cohort percentile rank, 0 to 1, cohort dummies):

| Rank | n | Slope (pts, bottom to top) | Ticker-clustered t | Cohort-clustered t |
|---|---|---|---|---|
| Overall | 247 | -9.9 | -0.72 (86 clusters) | -0.74 (4 clusters, unreliable) |
| Within sector | 192 | +3.3 | 0.18 (71 clusters) | 0.17 (4 clusters, unreliable) |

**Monthly check** (fixed formation terciles, 12 months each; the 1 to 16 Oct 2026 stub is dropped, giving 47 months). This is not 47 independent observations.

| Test | Months | Mean spread / month | Median | t | Worst month |
|---|---|---|---|---|---|
| T1 | 47 | +0.24 | -0.49 | 0.40 | -11.6 (Nov 2023) |
| T2 | 47 | +0.63 | +0.53 | 1.07 | -10.7 (Dec 2025) |

## Robustness

Net spreads by cohort (2022 / 2023 / 2024 / 2025) and mean across cohorts, with the placebo p-value:

| Variant | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| Main | +19.8 / -20.3 / +4.5 / -8.9; mean -1.2; p 0.51 | +8.2 / +58.4 / -3.4 / -11.2; mean +13.0; p 0.17 | +3.4 / -80.3 / +43.1 / +2.0; mean -7.9; p 0.64 | +29.6 / +39.7 / +10.3 / +7.1; mean +21.7; p 0.10 |
| No liquidity filter (eligible 82 / 86 / 90 / 96) | +12.1 / -29.9 / -18.4 / -25.9; mean -15.5; p 0.90 | -8.7 / +6.7 / -33.2 / -46.1; mean -20.3; p 0.91 | +12.0 / -67.5 / +46.9 / +6.8; mean -0.4; p 0.49 | +26.8 / +22.0 / -62.6 / -24.3; mean -9.5; p 0.65 |
| roe/pb fallback rows dropped (eligible 42 / 43 / 60 / 74) | +16.1 / -71.4 / +9.5 / +12.9; mean -8.2; p 0.73 | +4.4 / +85.7 / -3.7 / -1.8; mean +21.2; p 0.09 | +3.5 / -92.7 / +40.6 / +2.3; mean -11.6; p 0.71 | +26.7 / -147.7 / +32.9 / +3.2; mean -21.2; p 0.83 |
| Returns winsorised 5/95 within cohort | +16.1 / -6.5 / +5.3 / -2.7; mean +3.1; p 0.28 | +6.0 / +23.9 / -6.4 / -6.9; mean +4.1; p 0.33 | +0.1 / -38.4 / +42.3 / +2.0; mean +1.5; p 0.41 | +22.8 / +39.3 / +3.1 / +2.6; mean +16.9; p 0.04 |

Outliers matter. The largest eligible 12m return per cohort was +79.7 (ATRL), +538.6 (SAZEW), +292.9 (THCCL) and +329.9 (MACFL), against cohort medians of +5.4, +39.2, +62.4 and -12.0. Removing the Oct 2025 maximum alone moves that universe mean from +2.5 to -1.4. The T2 mean of +13.0 comes mostly from Oct 2023 (+58.4); the other three cohorts average -2.1. The fallback rows do not drive the result in T2 (+21.2 without them), but T1 gets worse (-8.2). Without the liquidity filter all four mean net spreads are negative (T3 only -0.4), so the cheap-name results depend on the liquid names.

## Verdict

**Nothing.** Rule applied: standalone needs T1 and T2 net spreads positive in at least 3 of 4 cohorts and above the placebo 95th percentile. T1 is positive in 2 of 4 (mean net -1.2, placebo 95th net +16.9, p 0.51). T2 is positive in 2 of 4 (mean net +13.0, placebo 95th net +19.1, p 0.17). Tiebreaker needs T2 positive in at least 3 of 4; it is 2 of 4. Neither passes. With 4 episodes a standalone verdict cannot be reached at conventional confidence whatever the point estimate. This agrees with lessons 17 and 18: with true publication dates, ranking overall gives no spread, and ranking within sector does not rescue it. The regression slopes are indistinguishable from zero.

T4 was positive in 4 of 4 cohorts (mean net +21.7, p 0.10; winsorised p 0.04), but it is not in the verdict rule, momentum alone added -1.1 on average, its terciles hold 6 to 13 names, and it turns negative with no liquidity filter (-9.5) or without fallback rows (-21.2). It is a lead to retest, not a finding.

## Caveats

- Survivorship: every name was listed on 16 Oct 2026 and the 108 were picked on today's liquidity. Cheap names that later re-rated are over-represented. The formation-date liquidity filter cuts this only partly. Delisted names are absent.
- Restated fundamentals: StockAnalysis shows today's EPS on today's share basis, which can differ from what was published. EPS consolidation status is unverified (lesson 1); holdings such as HUBC, MFL and FFC may be ranked on standalone EPS.
- Sector codes are current, not point in time. Thin sectors (1 to 2 eligible names) drop out of T2, so T1 and T2 use different samples (12 to 15 names a year).
- Matching gaps: 74 of 530 fiscal years have no announcement match, and 154 annual titles carry no parseable period. Unmatched years fall back to the previous year, which is staler and not random. Oct 2021 has no usable data (103 of 108 names have no published year in the file).
- The primary outcome is price only. Total return exists for two cohorts and does not change the picture.
- Market rerating 2022 to 2025 (lesson 9) and sector rerating are not removed by overall terciles; that is why T2 decides the verdict.
- Power: 4 cohorts, the last 11.5 months. The ticker-clustered t overstates precision; the placebo is the main inference. Tercile sizes are 6 to 29 names and single names move cohort means (see Robustness).
- The roe/pb fallback uses a different E/P source from 1/pe: 2, 6, 9 and 11 names a cohort. The 30 positive-ROE blank-pe rows sit inside this.
- Win rates compare each top-tercile name with the equal-weight mean of all eligible names, which a few large winners lift; read them with the medians.
- No live screen was requested in this spec, so none was run.
