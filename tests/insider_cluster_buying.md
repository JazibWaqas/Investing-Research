# Insider cluster buying (PSX, disclosed insider trades)

Evidence date 2026-10-17 (data to 2026-10-16). Script `scripts/tests/insider_cluster_buying.py`, raw output `tests/out/insider_cluster_buying.txt` (every number below is from it), trade table `data/insider_trades.csv`, sample and parse notes `data/INSIDER_TRADES_NOTES.md`. Not committed.

## Hypothesis

H1: when a second distinct insider buys in the open market within 30 days, the stock beats the market over the next 21, 63 and 126 sessions (comparisons: single buys; clusters net of insider sales). H2: sponsor and 10%-holder buys do better than director and CEO buys, which do better than executive buys. H3: a buy by someone who sold in the prior 180 days does worse than a clean buy. H4: insider sales, single and clustered, are followed by underperformance (one-sided).

## Data

- Announcements: 13,120 insider_trade rows, 50.8% with a PDF; titles carry no direction (12,946 untagged), so everything comes from the PDF.
- Sample fixed in advance: 22 whole symbols drawn at random (HCAR, ISL, BIPL, CNERGY, FECTC, WASL, KOHC, GGL, CRTM, BFAGRO, SPL, TELE, EFERT, FFC, NETSOL, GLAXO, SSGC, WAVES, GCWL, RPL, CEPB, CPPL; 609 rows, 62.9% with a PDF) plus every KMI-list filing with a PDF from 2026-06-18 (block a). 497 PDFs read: 113 from a text layer, 384 by eye (373 scans, 11 garbled), 0 unreadable, 9 without trade lines.
- 973 trade lines, 96 duplicate copies removed, 877 unique. Qualifying (market or unstated mode): 473 buys, 202 sells; 88 distinct buyers and 60 distinct sellers. Excluded buys: rights 24, other 28 (preference shares, REIT futures, scheme allotments), gifts 22, off-market 20, ESOP 10, bonus 5, tender 2.
- All 672 priced qualifying lines fall inside the raw close range of the stock around the trade date, so the transcription is price-consistent.
- Filing lag (announcement minus trade date): median 2 days, 90th percentile 10. 5.4% of the sample filings are stamped at or after 15:30 (5.1% of all 6,169 filings with a PDF since 2019).
- Title tags (174) cannot be cross-checked: one tagged row is on a sampled PDF and it has no trade lines.
- Spot check of 5 rows with no PDF on the portal: 4 have none, 1 (CEPB 2019-07-31) has a PDF. Cause: the scraper matched `.pdf` case-sensitively. A re-fetch of the 22 symbols finds 23 hidden insider PDFs (ISL 18); the 2026 window has none. They are outside the fixed 500 cap.

## Method

Event time is the announcement stamp. Entry is the close of the first tradable session (before 15:30 on a trading day with a close: that day; otherwise the next observation; dropped if none within 5 rows). Names below Rs5m trailing median traded value at entry are dropped. Returns are bonus and split adjusted price returns, excess over the equal-weight Rs5m market, minus 0.5% round trip. Horizons are 21, 63 and 126 rows. Overlapping events in a symbol are removed per horizon. Placebo: 1,000 samples with one random same-symbol day within +-365 days per event (liquid, full horizon, same cost). Insider-announcement units fold repeats by the same holder within 30 days. Split: in-sample entry 2019-2023, out-of-sample 2024 to 2026-10-16. Backtest uses the 22 drawn symbols only.

Events before drops: H1 cluster 16 (illiquid at entry 7, usable 9), net-of-sales 15 (6, 9), singles 82 (32, 50), H2 sponsor 30 (21, 9), director 53 (15, 38), executive 17 (3, 14), H3 round-trip 9 (0, 9), clean 98 (41, 57), H4 single 60 (5, 55), H4 cluster 8 (0, 8). Overlap removal and horizon drops are in the raw output; none were lost to missing prices.

## Results (63 sessions, net of 0.5%; p = share of placebo medians at least the event median, at most for H4)

Rows with n below 20 or fewer than 8 entry months are labelled insufficient to conclude in the raw output. In this table only H1 singles (all, IS), H2 director (all), H3 clean (all) and H4 single (all) escape that label; every other row carries it.

| Row | Split | n | Symbols | Months | Mean | Median | Win | Worst (symbol, entry) | Month-clustered median / win | Placebo median / win | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 cluster | all | 7 | 6 | 6 | -1.0% | +1.1% | 57% | -33.2% (GGL, 2021-12-02) | -1.2% / 50% | -2.9% / 43% | 0.264 |
| H1 cluster | IS | 3 | 3 | 3 | -14.5% | -6.9% | 0% | -33.2% (GGL, 2021-12-02) | -6.9% / 0% | -3.0% / 36% | 0.669 |
| H1 cluster | OOS | 4 | 4 | 3 | +9.2% | +8.0% | 100% | +1.1% (SPL, 2026-01-12) | +8.6% / 100% | -0.6% / 49% | 0.150 |
| H1 net-of-sales | all | 7 | 5 | 6 | -1.7% | -3.6% | 43% | -33.2% (GGL, 2021-12-02) | -3.8% / 33% | -2.8% / 44% | 0.565 |
| H1 net-of-sales | OOS | 3 | 3 | 2 | +11.9% | +8.6% | 100% | +7.4% (KOHC, 2026-03-13) | +11.1% / 100% | -1.9% / 48% | 0.170 |
| H1 singles | all | 40 | 15 | 35 | -2.3% | -4.3% | 35% | -33.2% (RPL, 2021-01-06) | -1.6% / 40% | -3.8% / 39% | 0.576 |
| H1 singles | IS | 23 | 12 | 21 | -2.8% | -1.8% | 30% | -33.2% (RPL, 2021-01-06) | -1.6% / 33% | -3.1% / 39% | 0.261 |
| H1 singles | OOS | 17 | 10 | 14 | -1.7% | -5.2% | 41% | -26.9% (BFAGRO, 2026-03-18) | -2.5% / 50% | -4.8% / 38% | 0.523 |
| H2 sponsor_substantial | all | 6 | 4 | 6 | -0.7% | -2.4% | 50% | -26.9% (BFAGRO, 2026-03-18) | -2.4% / 50% | -2.3% / 42% | 0.501 |
| H2 director_ceo | all | 24 | 12 | 21 | -1.1% | -2.6% | 38% | -33.2% (RPL, 2021-01-06) | -1.6% / 38% | -4.6% / 38% | 0.258 |
| H2 director_ceo | OOS | 9 | 6 | 7 | +2.2% | +5.3% | 56% | -16.4% (NETSOL, 2024-09-27) | +3.1% / 57% | -5.0% / 38% | 0.055 |
| H2 executive | all | 13 | 8 | 12 | -1.3% | -1.0% | 46% | -29.8% (GGL, 2021-12-13) | +0.6% / 50% | -1.3% / 45% | 0.481 |
| H3 round-trip | all | 6 | 3 | 6 | +2.6% | -1.0% | 50% | -16.4% (NETSOL, 2024-09-27) | -1.0% / 50% | -4.4% / 40% | 0.285 |
| H3 clean | all | 38 | 16 | 31 | -2.4% | -3.9% | 37% | -33.2% (RPL, 2021-01-06) | -1.8% / 39% | -3.8% / 40% | 0.510 |
| H4 single | all | 35 | 15 | 26 | -0.5% | -2.5% | 43% | -33.2% (RPL, 2021-01-06) | -2.6% / 38% | -5.2% / 36% | 0.814 |
| H4 single | OOS | 16 | 10 | 11 | -2.8% | -6.3% | 44% | -20.2% (HCAR, 2024-05-17) | -6.1% / 27% | -5.0% / 37% | 0.389 |
| H4 cluster | all | 7 | 3 | 5 | +5.6% | +2.8% | 71% | -15.7% (NETSOL, 2025-09-24) | +1.6% / 60% | -6.4% / 33% | 0.891 |

The full grid (21, 63 and 126 sessions, all, IS and OOS, 96 rows) is in the raw output. All-period medians and p at the other horizons:

| Row | 21: n, median, p | 126: n, median, p |
|---|---|---|
| H1 cluster | 8, +3.2%, 0.045 | 7, -4.4%, 0.333 |
| H1 singles | 50, -1.3%, 0.308 | 31, -13.7%, 0.909 |
| H2 sponsor / director / executive | 9, -4.2%, 0.714 / 31, -0.3%, 0.151 / 14, +0.1%, 0.315 | 5, -4.4%, 0.397 / 20, -7.8%, 0.431 / 11, -4.3%, 0.715 |
| H3 round-trip / clean | 8, -2.4%, 0.618 / 48, -0.2%, 0.049 | 5, +5.1%, 0.208 / 30, -11.7%, 0.891 |
| H4 single / cluster | 42, -3.2%, 0.296 / 8, -3.3%, 0.449 | 29, -7.3%, 0.469 / 5, -12.9%, 0.112 |

H2 difference in medians, sponsor minus director (1,000 label shuffles, one-sided): 21 sessions -3.9%, p 0.912 (n 9 and 31); 63 sessions +0.3%, p 0.501 (n 6 and 24); 126 sessions +3.4%, p 0.405 (n 5 and 20). With and without ASL and AHCL the numbers are identical because neither was drawn into the backtest.

Concentration at 63 sessions: H1 cluster events by year 2021: 2, 2022: 1, 2025: 1, 2026: 3, largest month (2026-03) 29%; the top 3 events sum +35.6% against a negative total (-6.9%), so the sum is carried by a few winners. H4 cluster top 3 events are 158% of the total.

## Robustness (H1 cluster, 63 sessions)

| Variant | n | Median | Win | p | OOS n, median |
|---|---|---|---|---|---|
| Entry at the D+1 close | 7 | +0.8% | 57% | 0.187 | 4, +5.7% |
| Market-mode buys only | 7 | +1.1% | 57% | 0.221 | 4, +8.0% |
| Excluding entries within 10 trading days after a result | 4 | -2.9% | 50% | 0.326 | 1, +1.1% |

5 of the 9 usable H1 cluster events (56%) entered within 10 trading days after a result in the same name, so post-results timing is a real confound. Removing them leaves 4 events.

## Current list (completing announcement 2026-07-18 to 2026-10-16, KMI names)

- H1 buy cluster: one. SHFA, completed 2026-08-06 15:11. Members: Zeeshan Bin Ishtiaque (CEO, director_ceo) bought on 07-10, 07-13, 07-14, 07-15 and 07-16 (1,850 at 530.91, 1,800 at 536, 1,850 at 525.27, 1,929 at 522.36, 1,900 at 532; about Rs1.0m a day); Hubert (executive) bought 200 at 516 on 08-04 (Rs103,200). No qualifying sales in the 30 days. Entry close 2026-08-06; net excess to the 2026-10-16 close -1.8%. It was liquid at entry but is not at Rs5m on the trailing 60 days now.
- H4 sell clusters: two. FCL, completed 2026-08-21: Muhammad Shahzad Mian (executive) sold 881,000 at 28.02 (Rs24.7m) and a second executive sold 5 shares; net excess -4.5%, liquid. MEBL, completed 2026-09-22: Shahzad Abdullah (executive) sold 23,334 at 550.68 (Rs12.8m) after Irfan Siddiqui's spouse sold 10 shares (Rs5,648); net excess +2.5%, liquid.

The count rule makes these clusters of one real insider plus a token trade each time.

## Verdict

Not supported, and untestable at this sample size. H1 had 16 clusters in 22 symbols, 9 usable after the liquidity screen and 7 after overlap removal. Every H1 row is "insufficient to conclude". The out-of-sample half (4 events: median +8.0%, win 100%) is the only encouraging number, against in-sample -6.9% and 0% (3 events) and a placebo median of -0.6%; p is 0.150 and 0.264 for the whole period. At 21 sessions the cluster p is 0.045 on 8 events, but a clean-buy row at the same horizon also gives p 0.049 on 48 events, so a low p there looks like placebo drift in these names, not insiders. H2, H3 and H4 show no ordering: sponsors do not beat directors (p 0.501 at 63 sessions), round-trip buyers are not worse than clean buyers, and sales are not followed by underperformance (H4 single p 0.814). The current SHFA cluster is not an act-on signal: the out-of-sample H1 result is four events, the placebo test does not reject, and the cluster is one repeat buyer plus a Rs103,200 purchase.

## Caveats

- Missing filings: 49.2% of insider rows have no PDF, and 23 more in the drawn symbols were hidden by a scraper bug (ISL 2020 is the worst case). Clusters are undercounted and singles misclassified when the second filing is invisible. Whether filings are missing at random by year or filer is unknown.
- Sample and parse: 22 symbols drive the result, 77% of the PDFs were read by eye, and the eye-read share varies by year (2019 48%, 2024 100%). The price check catches wrong prices, not wrong names.
- Survivorship: prices exist only for names still listed on 2026-10-16, which inflates buys and hides sales before collapses; the equal-weight market is flattered.
- Price-only returns: bonus and split adjusted, no dividends (cash dividends are complete only from Nov 2024), so high-yield names look worse than on total return.
- Regime and overlap: 2023-2025 was a market rerating; events share market paths; month-clustered figures are shown. One repeat buyer pair (Ahmad Shafi with Khalid Bashir or Muhammad Anwar at CRTM, 2021 to 2025) supplies 7 of the 16 clusters.
- Hypothesis H2 came from ASL and AHCL in 2026; both sit outside the backtest.
