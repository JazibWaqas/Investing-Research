# Insider cluster buying (PSX, disclosed insider trades) - run 2, full universe

Evidence date 2026-10-18 (data to 2026-10-16). Script `scripts/tests/insider_cluster_buying.py`, raw output `tests/out/insider_cluster_buying.txt` (every number below is from it), trade table `data/insider_trades.csv` (built by `scripts/insider_run.py`), extraction rates and failure modes in `data/INSIDER_TRADES_NOTES.md`. Run 1 (22 random symbols, 497 hand-read PDFs, verdict "untestable at this size") is kept in `data/insider_trades_run1.csv`. Not committed.

## Hypothesis (pre-registered in run 1, unchanged)

H1: when a second distinct insider buys in the open market within 30 days, the stock beats the market over the next 21, 63 and 126 sessions (comparisons: single buys; clusters net of insider sales). H2: sponsor and 10%-holder buys do better than director and CEO buys, which do better than executive buys. H3: a buy by someone who sold in the prior 180 days does worse than a clean buy. H4: insider sales, single and clustered, are followed by underperformance (one-sided).

## What changed from run 1

- Universe: 195 symbols (the 129 in `quarterly_eps.csv` plus KMI names whose trailing 60-session median traded value was above Rs5m at any time since 2019; the EPS file holds 129 symbols, not 136) instead of 22 random ones.
- Document-id fix: `fetch_announcements.py` matched `.pdf` case-sensitively. After the fix and a re-fetch of every month from 2019-01 to 2026-10, 231 insider_trade rows (2019 on) gained a document id (2019: 10, 2020: 55, 2021: 73, 2022: 23, 2023: 16, 2024: 29, 2025: 25, 2026: 0); 119 of them are in the universe. The portal is also case-sensitive on download: `.PDF` links only resolve with the capital extension.
- Every PDF was read by a program, not by eye: pdfplumber for a text layer, Windows OCR for scans, then a row parser. Hand reading is replaced by a measured, imperfect extractor (see Caveats).
- Rules unchanged: event time is the announcement stamp, entry at the first tradable close, Rs5m liquidity screen at entry, bonus/split-adjusted price returns, excess over the equal-weight Rs5m market, 0.5% round trip, 21/63/126 sessions, overlap removal, 1,000-sample same-symbol placebo, IS 2019-2023 and OOS 2024 on. New: a confidence flag on every parsed row (high, medium, low); the tests use high and medium, a robustness row uses high only. Holder names are matched order-free, and a name that is a token subset of a longer name in the same symbol is merged with it (OCR and spelling variants).

## Data

- 13,120 insider_trade announcements; 6,892 (52.5%) have a PDF. In the universe since 2019: 5,445 rows, 2,549 with a PDF (46.8%; by year 2019 200/582, 2020 313/682, 2021 347/759, 2022 268/585, 2023 236/611, 2024 368/613, 2025 537/899, 2026 280/714). Rows without a PDF are title-only on the portal and cannot be recovered.
- 2,548 of the 2,549 PDFs were read (1 is a 404 on the portal, 1 failed to open): 730 text layer, 1,817 OCR. 1,602 (63%) gave at least one trade row; 946 gave none (notices, rights certificates, broker statements, layouts the parser misses).
- 4,617 trade rows, 471 of them copies of a trade already filed (flagged, not counted). Confidence: high 1,482, medium 2,129, low 1,006. Qualifying lines (market or unstated nature, buy or sell, unique, high or medium): 1,169 buys, 1,496 sells; 311 distinct buyers and 178 distinct sellers (symbol, holder). By announcement year buys/sells: 2019 71/16, 2020 77/135, 2021 141/619, 2022 95/15, 2023 76/330, 2024 272/134, 2025 319/187, 2026 118/60.
- Roles: sells are 1,043 of 1,496 "unknown" role (the 2021 and 2023 sells are dominated by long broker-style listings with no role), so H2 and role-based reading rest on buys.
- Extraction accuracy against the 497 hand-read PDFs of run 1 (match on trade date and share count): 479 of 840 hand-read lines recovered (57%); 406 of 672 open-market lines (60%); in a random 50-PDF sample 46 of 80 lines (26 of 48 PDFs with every line). Precision of parsed rows against the hand reads: high 93%, medium 85%, low 48%. Extra rows beyond the hand reads are mostly broker-list lines and column-order errors. 2,658 of 2,665 qualifying priced lines sit inside the raw close range of the stock around the trade date.
- Filing lag (announcement minus trade date): median 2 days, 90th percentile 10. 5.7% of read filings are stamped at or after 15:30.

## Results (63 sessions, net of 0.5%; p = share of placebo medians at least the event median, at most for H4)

Rows with n below 20 or fewer than 8 entry months are labelled insufficient to conclude in the raw output.

| Row | Split | n | Symbols | Mean | Median | Win | Worst (symbol, entry) | Month-clustered median / win | Placebo median / win | p |
|---|---|---|---|---|---|---|---|---|---|---|
| H1 cluster | all | 37 | 17 | +2.6% | -0.4% | 46% | -33.2% (GGL, 2021-12-02) | -0.1% / 48% | -0.6% / 49% | 0.473 |
| H1 cluster | IS | 20 | 9 | -2.7% | -3.9% | 35% | -33.2% (GGL, 2021-12-02) | -3.1% / 38% | -1.4% / 46% | 0.811 |
| H1 cluster | OOS | 17 | 11 | +8.8% | +5.0% | 59% | -19.8% (SYM, 2025-01-27) | +2.2% / 62% | +0.4% / 51% | 0.137 |
| H1 net-of-sales | all | 28 | 13 | +2.6% | -2.2% | 43% | -33.2% (GGL, 2021-12-02) | -3.6% / 37% | -0.1% / 49% | 0.799 |
| H1 net-of-sales | OOS | 13 | 7 | +8.8% | +5.0% | 54% | -21.3% (MARI, 2025-04-17) | -4.2% / 38% | +1.8% / 55% | 0.210 |
| H1 singles | all | 97 | 38 | +5.6% | +2.3% | 57% | -33.2% (RPL, 2021-01-06) | +0.4% / 51% | -1.6% / 46% | 0.021 |
| H1 singles | OOS | 38 | 24 | +6.5% | +0.5% | 50% | -26.9% (BFAGRO, 2026-03-18) | -3.3% / 39% | -0.4% / 48% | 0.381 |
| H2 sponsor_substantial | all | 5 | 5 | -5.7% | -8.7% | 20% | -13.3% (POWER, 2020-10-13) | -8.7% / 20% | -2.2% / 42% | 0.793 |
| H2 director_ceo | all | 42 | 15 | +8.2% | +2.5% | 57% | -33.2% (GGL, 2021-12-02) | +2.0% / 54% | -1.3% / 47% | 0.099 |
| H2 director_ceo | OOS | 16 | 8 | +16.8% | +8.3% | 62% | -20.0% (SHFA, 2026-03-09) | +8.5% / 58% | -0.0% / 50% | 0.029 |
| H2 executive | all | 59 | 17 | +6.4% | +1.8% | 54% | -22.7% (SPEL, 2024-09-20) | +2.8% / 62% | +0.9% / 52% | 0.341 |
| H3 round-trip | all | 23 | 9 | +1.4% | -0.6% | 48% | -22.7% (SPEL, 2024-09-20) | +0.5% / 53% | +1.2% / 53% | 0.682 |
| H3 clean | all | 113 | 38 | +5.3% | +1.8% | 55% | -33.2% (RPL, 2021-01-06) | +1.1% / 52% | -1.5% / 46% | 0.033 |
| H4 single | all | 102 | 40 | +5.3% | -2.7% | 46% | -63.6% (PICT, 2023-10-13) | -2.1% / 46% | -0.8% / 48% | 0.119 |
| H4 single | OOS | 58 | 31 | +6.3% | -5.2% | 40% | -31.3% (TRSM, 2025-12-17) | -5.4% / 42% | -0.6% / 48% | 0.010 |
| H4 cluster | all | 33 | 15 | -3.1% | -3.4% | 39% | -45.5% (PICT, 2023-10-26) | -4.2% / 35% | -0.5% / 48% | 0.077 |

The full grid (all, IS and OOS at 21, 63 and 126 sessions) is in the raw output. All-period medians and p at the other horizons:

| Row | 21: n, median, p | 126: n, median, p |
|---|---|---|
| H1 cluster | 44, -0.9%, 0.621 | 33, -5.3%, 0.932 |
| H1 singles | 117, -0.5%, 0.303 | 83, -0.0%, 0.521 |
| H2 sponsor / director / executive | 7, -3.2%, 0.722 / 51, -1.4%, 0.603 / 81, +0.4%, 0.197 | 4, -12.8%, 0.851 / 33, +2.7%, 0.270 / 45, +2.5%, 0.295 |
| H3 round-trip / clean | 34, -1.1%, 0.748 / 149, -0.5%, 0.246 | 18, -1.8%, 0.846 / 92, -0.3%, 0.397 |
| H4 single / cluster | 137, -3.1%, 0.006 / 40, -2.4%, 0.047 | 83, -4.2%, 0.019 / 27, -2.6%, 0.173 |

H2 difference in medians, sponsor minus director (1,000 label shuffles, one-sided): 21 sessions -1.8%, p 0.586 (n 7 and 51); 63 sessions -11.2%, p 0.841 (n 5 and 42); 126 sessions -15.5%, p 0.888 (n 4 and 33). Dropping ASL and AHCL changes nothing.

Concentration at 63 sessions: H1 cluster events by year 2019: 2, 2020: 5, 2021: 9, 2022: 4, 2024: 4, 2025: 8, 2026: 5; the top 3 events sum +192% against a total of +95%, so the cluster mean is carried by three winners (the median is negative). H2 director_ceo and H4 single are in the same position (top 3 are 105% and 114% of the total).

## Robustness (H1 cluster, 63 sessions)

| Variant | n | Median | Win | p | OOS n, median |
|---|---|---|---|---|---|
| Entry at the D+1 close | 37 | -3.2% | 43% | 0.869 | 17, +4.9% |
| Market-mode buys only | 31 | +1.1% | 52% | 0.376 | 15, +5.0% |
| Excluding entries within 10 trading days after a result | 28 | -0.2% | 46% | 0.541 | 11, +5.0% |
| High-confidence rows only | 23 | +1.8% | 61% | 0.534 | 10, +6.0% |

15 of 47 usable H1 cluster events (32%) entered within 10 trading days after a result in the same name.

## Current list (completing announcement 2026-07-18 to 2026-10-16, KMI names)

- H1 buy clusters: two, both illiquid at Rs5m on the trailing 60 days. EMCO, completed 2026-08-07 10:28: Ahsan Suhail and Bushra Ahsan bought on 08-05 (71,500 and 217,500 shares at 52.43, Rs3.7m and Rs11.4m), roles not read; net excess to 2026-10-16 -25.8%. SHFA, completed 2026-09-17 14:07: director/CEO-level buyers on 09-14 (Zeeshan Bin Ishtiaque 22,160 at 449.47, Rs10.0m; Taimoor Shah 6,624; Aamer Nazir Ahmad 4,016) plus an executive on 08-27/28 and 09-15; two director sells in the window (Manzoor Ul Haq Qazi, 1,620 shares); net excess to date +5.6%; liquid at entry, not now.
- H4 sell cluster: one. MEBL, completed 2026-09-22: Shahzad Abdullah (executive) sold 23,334 at 550.68 (Rs12.8m) after a spouse-level sale of 10 shares (Rs5,648); net excess +2.5%.
- Run 1's hand-read SHFA cluster of 2026-08-06 (Zeeshan Bin Ishtiaque's five July buys plus an executive) is not reproduced by the parser: the July PDFs were read as no-trade or low-confidence. The current list is therefore a floor, not a census.

## Verdict

Still not supported. n is now 37 H1 cluster events (47 usable, 37 after overlap removal) in 17 symbols, up from 7 in 6, and the result is flat: median -0.4%, win 46%, p 0.473 at 63 sessions, with -3.9% in sample and +5.0% out of sample (17 events, p 0.137). The mean (+2.6%) comes from three winners. Clusters are no better than single buys (H1 singles median +2.3%, p 0.021, but clean buys read the same, +1.8%, p 0.033, which says the placebo drift of these names, not the cluster, is what is being measured). At 21 sessions the cluster p is 0.621 (run 1's 0.045 did not survive). H2: sponsors have only 5 events and did worse than directors; directors and CEOs show the one encouraging row (OOS median +8.3%, p 0.029, 16 events, insufficient to conclude, and the all-period p is 0.099). H3: round trips are no worse than clean buys. H4 is the only one with a signal: single sales are followed by underperformance (21 sessions median -3.1%, p 0.006, 137 events; OOS 63 sessions -5.2%, p 0.010), which fits the hypothesis but sits next to a +5.3% mean driven by outliers (PICT -63.6%). Not an act-on rule for buys; the sell side is worth a follow-up with better role and name data.

## Caveats

- Extraction recall is about 60%, and 37% of PDFs give no row. Clusters are undercounted wherever a filing was missed or misread, and singles are misclassified when the second filing was lost. The loss is not random: it concentrates in wrapped-date tables, multi-line cells, REIT-unit futures notices and broker statements.
- Names come from OCR and are matched by token sets; spelling variants that are not subsets still split one person into two (hiding a cluster) and two people sharing tokens can merge. 1,043 of 1,496 qualifying sells have no role, so H2 and H4 role cuts are thin.
- Missing filings: 53% of insider announcements carry no PDF at all.
- Survivorship: prices exist only for names still listed on 2026-10-16.
- Price-only returns: bonus and split adjusted, no dividends (cash dividends are complete only from Nov 2024).
- Regime and overlap: 2023-2025 was a market rerating; events share market paths; month-clustered figures are shown. One repeat buyer pair (Ahmad Shafi with Khalid Bashir at CRTM) still supplies several clusters.
- Multiple comparisons: about 100 rows are printed; with p cut-offs near 0.05, two or three of them will look good by chance. The 21-session H4 single (p 0.006) is the only one that clears that bar comfortably.
