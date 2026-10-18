# Winners population, Oct 2016 to Oct 2026: 1,759 price runs, 383 of them tradable

Built 18 Oct 2026 from prices to 16 Oct 2026 by `scripts/tests/winners_population.py` (modes build, engine, tables). Outputs: `data/winners_library.csv` (383 episodes above Rs2m median traded value, all fields), `data/winners_library_thin.csv` (1,376 thinner), `tests/out/winners_population_tables.txt` (every number below), `_snippets.md`, `_breakout_events.csv`. Every figure is conditional on the run having happened; the denominator that turns it into odds is in section 5.

## 1. Short answer

- **Population.** 1,759 runs in 511 names (595 loaded: 456 current, 139 delisted). 383 clear Rs2m; PHDL, a share rebase that looks like 65x, is dropped, leaving 382 in 163 names, 249 KMI members at the start. Median run 2.0x in 116 sessions. 34 reached 5x, each over 302 to 962 sessions, and 23 of the 34 began within three months of a market low (Apr to Aug 2019, Oct 2022 to Jan 2023).
- **Three animals.** 86 sprints (peak within 63 sessions, median 1.5x), 147 runs (64 to 252 sessions, 1.8x), 149 multi-year runs (3.3x). A late reader's odds depend on which one it is, and the start does not say.
- **Late entry.** A first 252-high exists in 68% of runs, 110 sessions after the start at a median 1.46x. Median share of the log gain still ahead then: 0.52 overall, 0.23 for sprints, 0.25 for runs, 0.73 for multi-year. Joining at session 10 left another 1.5x or more in 75% of runs; joining at the first 252-high, 51%.
- **Milking and leaving.** A live 20% trailing stop keeps more than half the gain in only 15% to 23% of runs: the median run holds a 17% pullback inside 20 sessions and 34% hold a 25% fall later recovered. Wide stops (30 to 40%) pay on the long runs and do nothing for the short ones.
- **Causes.** Two thirds of runs are labelled by market context (sector or market wave, post-shock rebound). The name-specific labels the filing tape can see are rare.

## 2. Definitions (fixed before looking at results)

Adjusted closes (bonus, split, partial cash; crude chain for delisted), in market sessions. A window is +50% in 21 to 63 sessions or +100% in 126 to 252; overlapping windows merge into one episode. Start: lowest close in the 20 sessions up to the first window. Peak: highest close up to 21 sessions after the last window. Liquid: median traded value above Rs2m in the 60 sessions before the start. "Ahead" is one minus the log gain made so far over the log gain to the peak. First 252-high: first close above the prior 252-session maximum. Type is the first that applies of: takeover or deal (material_info title with acquisition, offer, merger, start-20 to start+63 sessions), results jump (financial_result up to the start with quarter EPS up 50% or loss to profit), sponsor or buyback (insider buy or buy-back title, same window), policy or sector wave (median liquid sector peer up 30%+ start to peak), shock rebound (KMI All Share 8% below its 20-session high within 20 sessions before the start), rate-cut rotation (start within 60 sessions of the first cut after a hike: 17 Mar 2020, 10 Jun 2024), other (a material_info filing, nothing above), operator or no visible cause. Flags overlap; 114 of 382 carry two or more. Suspect (excluded from statistics, kept in the files): a one-day jump above 50%, a 50% one-day fall around the start, or under 40% of run sessions traded.

## 3. Counts

By start year (thin = non-suspect thin list):

| year | liquid | thin | liquid_5x+ | liquid_median_x | kmi_at_start |
|---|---|---|---|---|---|
| 2016 | 1 | 182 | 0 | 1.66 | 0 |
| 2017 | 31 | 98 | 1 | 1.62 | 23 |
| 2018 | 23 | 66 | 0 | 1.54 | 12 |
| 2019 | 52 | 194 | 7 | 2.73 | 36 |
| 2020 | 33 | 96 | 0 | 2.04 | 20 |
| 2021 | 22 | 53 | 0 | 1.62 | 10 |
| 2022 | 38 | 94 | 12 | 3.92 | 25 |
| 2023 | 54 | 174 | 14 | 2.32 | 38 |
| 2024 | 47 | 137 | 0 | 2.2 | 31 |
| 2025 | 32 | 51 | 0 | 1.82 | 20 |
| 2026 | 49 | 40 | 0 | 1.58 | 34 |

By type (multi_flag = two or more flags):

| type | n | share | multi_flag | kmi |
|---|---|---|---|---|
| policy_sector_wave | 142 | 0.372 | 84 | 117 |
| shock_rebound | 106 | 0.277 | 9 | 57 |
| operator_no_visible_cause | 59 | 0.154 | 0 | 34 |
| other | 39 | 0.102 | 0 | 18 |
| results_jump | 18 | 0.047 | 16 | 15 |
| rate_cut_rotation | 10 | 0.026 | 0 | 3 |
| sponsor_buyback | 5 | 0.013 | 3 | 3 |
| takeover_deal | 3 | 0.008 | 2 | 2 |

By KMI flag at the start and liquidity tier (liquid and thin lists, non-suspect; H above Rs20m, M 5 to 20m, L 2 to 5m, thin below Rs2m or under 40 sessions of history):

| kmi | H | M | L | thin | total |
|---|---|---|---|---|---|
| KMI at start | 107 | 84 | 58 | 587 | 836 |
| not KMI | 36 | 52 | 45 | 598 | 731 |

| liq_tier | n | median_x | p90_x | median_sessions | x5plus |
|---|---|---|---|---|---|
| H | 143 | 2.02 | 4.91 | 184.0 | 13 |
| M | 136 | 1.94 | 4.22 | 90.5 | 11 |
| L | 103 | 2.01 | 4.88 | 136.0 | 10 |
| thin | 1185 | 2.04 | 6.65 | 136.0 | 178 |

KMI membership does not mark winners: median 2.02x for members against 1.93x for the rest (liquid). The thin list has 1,185 usable episodes (median 2.04x, 178 at 5x or more); many are stale-quote artefacts that cannot be separated here, so its upper tail is unverified. Of the pilot six only PRL (Rs230m a day) clears Rs2m at its episode start; MACFL, QUICE, CRTM, JVDC and TPLT start at Rs0.05m to 0.8m, in 2023 to 2025 because windows merge.

## 4. By type, and by length of run

Ahead columns are median shares of the log gain still ahead (n for the first 252-high in brackets). "Stop from peak": share of finished runs where selling at the first close 20% under the peak keeps more than half the gain. "Live stop": a 20% trailing stop entered at the first 252-high.

| index | n | median x | sessions to peak | ahead at 1st 252-high (n) | ahead s10 | ahead s20 | ahead s40 | median 60-session drawdown after peak | stop from peak keeps >half | live 20% stop from 1st 252-high keeps >half |
|---|---|---|---|---|---|---|---|---|---|---|
| all liquid | 382 | 2.01 | 116 | 0.52 (261) | 0.95 | 0.92 | 0.78 | -26% | 62% | 15% |

| type | n | median x | sessions to peak | ahead at 1st 252-high (n) | ahead s10 | ahead s20 | ahead s40 | median 60-session drawdown after peak | stop from peak keeps >half | live 20% stop from 1st 252-high keeps >half |
|---|---|---|---|---|---|---|---|---|---|---|
| policy_sector_wave | 142 | 2.18 | 275 | 0.55 (114) | 0.97 | 0.96 | 0.86 | -26% | 73% | 15% |
| shock_rebound | 106 | 1.71 | 77 | 0.37 (51) | 0.89 | 0.84 | 0.59 | -27% | 51% | 10% |
| operator_no_visible_cause | 59 | 1.77 | 80 | 0.52 (38) | 0.98 | 0.95 | 0.88 | -30% | 51% | 9% |
| other | 39 | 1.73 | 100 | 0.67 (29) | 0.96 | 0.93 | 0.76 | -24% | 54% | 28% |
| results_jump | 18 | 2.01 | 105 | 0.33 (15) | 0.85 | 0.76 | 0.65 | -19% | 82% | 7% |
| rate_cut_rotation | 10 | 2.43 | 273 | 0.73 (9) | 0.96 | 0.99 | 0.99 | -33% | 90% | 22% |
| sponsor_buyback | 5 | 4.53 | 420 | 0.78 (5) | 0.96 | 0.93 | 0.82 | -33% | 80% | 60% |
| takeover_deal | 3 | 1.55 | 58 | none | 0.88 | 0.60 | 0.62 | -14% | 67% | n/a |

| dur | n | median x | sessions to peak | ahead at 1st 252-high (n) | ahead s10 | ahead s20 | ahead s40 | median 60-session drawdown after peak | stop from peak keeps >half | live 20% stop from 1st 252-high keeps >half |
|---|---|---|---|---|---|---|---|---|---|---|
| sprint <=63 | 86 | 1.53 | 40 | 0.23 (16) | 0.74 | 0.51 | 0.00 | -25% | 6% | 8% |
| run 64-252 | 147 | 1.77 | 83 | 0.25 (96) | 0.91 | 0.86 | 0.66 | -28% | 58% | 3% |
| multi-year >252 | 149 | 3.32 | 387 | 0.73 (149) | 0.99 | 0.99 | 0.97 | -25% | 100% | 23% |

Stop-from-peak is mostly arithmetic: exiting at 80% of the peak keeps more than half only above 1.67x, which 63% of runs exceed. Results-jump, sponsor and takeover rows rest on 18, 5 and 3 episodes. After the peak the median 60-session drawdown is 26%; 69% of runs fell more than 20%, 12% more than 40%.

## 5. What a late reader could have done, and the denominator

Exit multiple of a trailing stop entered at the first 252-high (finished runs, all winners in hindsight):

| group | stop | n | median_x | mean_x | share_gt_1_25 | share_gt_2 | share_lt_1 |
|---|---|---|---|---|---|---|---|
| all liquid | 20% | 248 | 1.01 | 1.25 | 0.24 | 0.1 | 0.49 |
| all liquid | 30% | 248 | 1.02 | 1.5 | 0.38 | 0.17 | 0.48 |
| all liquid | 40% | 248 | 1.01 | 1.63 | 0.38 | 0.23 | 0.48 |
| multi-year | 20% | 146 | 1.14 | 1.47 | 0.38 | 0.16 | 0.34 |
| multi-year | 30% | 146 | 1.34 | 1.88 | 0.57 | 0.27 | 0.27 |
| multi-year | 40% | 146 | 1.42 | 2.11 | 0.56 | 0.35 | 0.29 |
| sprint+run | 20% | 102 | 0.92 | 0.95 | 0.03 | 0.0 | 0.71 |
| sprint+run | 30% | 102 | 0.83 | 0.95 | 0.1 | 0.03 | 0.77 |
| sprint+run | 40% | 102 | 0.78 | 0.94 | 0.12 | 0.05 | 0.75 |
| 5x+ | 20% | 33 | 1.26 | 2.14 | 0.55 | 0.36 | 0.27 |
| 5x+ | 30% | 33 | 2.7 | 3.61 | 0.79 | 0.64 | 0.18 |
| 5x+ | 40% | 33 | 3.42 | 3.98 | 0.88 | 0.82 | 0.12 |

Joining a sprint or a 64 to 252 session run at its first 252-high lost money in 71% of cases at a 20% stop. Joining a multi-year run made a median 1.14x with a 20% stop and 1.42x with 40%; among the 5x runs 1.26x and 3.4x.

The denominator: 1,558 independent first 252-highs of liquid names. 25.6% reached a further +50% (best close, not an exit) within 126 sessions and 18.7% a further +100% within 252. By year the 126-session rate runs from 6% (2017, 2019, 2022) to 38% (2024), a market-regime number first. About three in four first 252-highs did not run, and a breakout buyer holds those too. This file says what winners did; it does not say how to tell them from that denominator.

## 6. Other features of the liquid winners

- Upper locks: median 7 limit closes per run; 2% had none, 35% had 10 or more.
- Filings in the 20 sessions up to the start, against any liquid stock-day: results 49% (baseline 39%), material information 16% (16%), insider 12% (16%), dividend or bonus 14% (14%). 22% had none. Median 2.5 filings before the start, 18.5 during the run. Only results show a tilt. Insider buys are recorded for 1 episode before the start (the direction field is filled for only 174 filings in the archive).
- Sector (238 episodes in the repo's list): peers rose a median 44% and the name beat them in 91%. Of 155 policy-wave flags, 117 had the whole index up 30%+; the sector beat the index by 20 points in 86.
- Index: median KMI move +38% over the run (+205% for 5x runs). Bill above policy at the start in 77% against 69% of liquid stock-days. Brent: median change 0%.
- Foreign flow (NCCPL sector series, 110 episodes in eight sectors): foreigners were net sellers in 70% of runs (median minus US$8.0m); individuals bought a median US$4.4m.
- Engine at the first 252-high of 60 random liquid episodes (59 answered): 20-session analogue median positive in 26 (44%), zero in 4, best +11.7%; positive at 5 sessions in 18, at 60 in 24. Positive-median cases ended 2.05x, the rest 2.19x. The engine does not mark a winner's breakout as special.

## 7. The 30 largest liquid episodes

| symbol | kmi | start_date | peak_date | multiple | sessions_to_peak | liq_tier | type | upper_locks |
|---|---|---|---|---|---|---|---|---|
| SAZEW | True | 2022-10-05 | 2026-02-09 | 43.8 | 830 | L | policy_sector_wave | 47 |
| GAL | True | 2022-12-19 | 2025-09-22 | 15.5 | 680 | M | policy_sector_wave | 48 |
| AGL | False | 2022-10-28 | 2025-08-25 | 15.2 | 695 | L | other | 55 |
| NBP | False | 2023-03-30 | 2026-02-04 | 13.4 | 704 | L | operator_no_visible_cause | 16 |
| PIAHCLA | False | 2022-12-05 | 2025-12-09 | 13.0 | 746 | L | operator_no_visible_cause | 72 |
| TRG | False | 2019-06-10 | 2021-05-18 | 12.7 | 480 | H | shock_rebound | 64 |
| BOP | False | 2023-05-09 | 2026-01-05 | 11.4 | 659 | M | operator_no_visible_cause | 27 |
| PTC | False | 2022-12-09 | 2026-07-03 | 11.2 | 880 | L | other | 42 |
| UBL | False | 2023-01-17 | 2026-02-04 | 10.6 | 755 | H | shock_rebound | 6 |
| FLYNG | True | 2023-08-08 | 2025-06-11 | 10.1 | 452 | L | policy_sector_wave | 28 |
| SYS | False | 2019-06-24 | 2021-09-10 | 10.1 | 548 | L | shock_rebound | 24 |
| GHNI | True | 2023-01-17 | 2025-10-23 | 9.9 | 682 | M | policy_sector_wave | 38 |
| FFC | False | 2023-06-19 | 2026-01-27 | 9.5 | 646 | H | other | 4 |
| PIOC | True | 2022-12-05 | 2025-12-15 | 7.7 | 750 | H | policy_sector_wave | 22 |
| MEBL | True | 2022-12-28 | 2026-04-08 | 7.7 | 811 | H | shock_rebound | 3 |
| ATRL | True | 2022-11-28 | 2026-10-16 | 7.6 | 962 | H | results_jump | 18 |
| AIRLINK | True | 2022-11-22 | 2025-01-02 | 7.2 | 522 | M | operator_no_visible_cause | 30 |
| NRL | True | 2019-07-25 | 2021-03-03 | 6.9 | 400 | M | shock_rebound | 48 |
| DGKC | True | 2023-01-30 | 2025-09-26 | 6.7 | 654 | H | policy_sector_wave | 13 |
| LUCK | True | 2023-01-17 | 2025-12-22 | 6.6 | 724 | H | sponsor_buyback | 5 |
| FFBL | False | 2022-12-20 | 2024-12-16 | 6.5 | 490 | M | shock_rebound | 17 |
| UNITY | True | 2019-05-17 | 2021-06-10 | 6.0 | 508 | H | policy_sector_wave | 48 |
| SSGC | True | 2023-08-29 | 2024-12-30 | 5.7 | 330 | M | policy_sector_wave | 20 |
| PREMA | True | 2023-11-13 | 2025-04-25 | 5.5 | 357 | L | policy_sector_wave | 41 |
| FABL | False | 2023-03-24 | 2026-07-03 | 5.5 | 806 | M | results_jump | 14 |
| CPHL | True | 2023-09-01 | 2025-02-11 | 5.5 | 357 | M | policy_sector_wave | 8 |
| AVN | False | 2019-08-26 | 2021-09-09 | 5.5 | 506 | L | shock_rebound | 47 |
| PIOC | True | 2019-04-18 | 2021-02-16 | 5.4 | 453 | H | policy_sector_wave | 55 |
| PSMC | False | 2022-10-25 | 2024-01-11 | 5.4 | 302 | H | operator_no_visible_cause | 36 |
| MUGHAL | False | 2019-06-27 | 2022-02-09 | 5.3 | 652 | M | policy_sector_wave | 43 |

All 34 runs of 5x or more are multi-year. The other four: FCCL (26 Apr 2023 to 30 Sep 2025, 5.3x, 599 sessions, policy wave), MARI (19 Jul 2023 to 16 Dec 2024, 5.3x, 348, other), BAHL (4 Nov 2022 to 21 Oct 2025, 5.3x, 731, operator) and CLOV (11 Apr 2017 to 10 Aug 2018, 5.1x, 331, sponsor or buyback). None began in 2018, 2020, 2021 or from 2024. The thin list has 178 runs of 5x or more.

## 8. What this does not show

- **Merging.** Bull markets become single 2 to 3 year episodes whose start can sit months before a sensible entry (MACFL starts June 2024, not the pilot's March 2026 base).
- **Causes are mostly unobserved.** About 5,500 of 7,900 material-information filings carry the bare title "Material Information", so title matching found 3 deals and 5 sponsor cases; the pilot's TPLT approach is labelled other. EPS data covers 129 symbols and matched a quarter pair for 56 episodes, so 18 results jumps is a floor. Treat shares by type as market context, not cause.
- **Sector and flows** use the repo's survivor-heavy sector list. KMI membership before Jan 2019 uses the 2019 list (404 of 1,567 non-suspect episodes start earlier).
- **Prices.** Dividends are only partly in the adjusted series; delisted names use the crude chain; stops are on closes and ignore locks, gaps and the 0.5 to 1% round-trip cost.
- **Next step, not run:** compare features at the first 252-high of these winners with the 1,558-event denominator. Until then the library is a lookup of past runs, not a predictor.
