# Results surprise, drift, leakage, muted-reaction value setup, board-notice effect (PSX, KMI names)

Run 2026-10-17. Script `scripts/tests/results_surprise_drift.py`, raw output `tests/out/results_surprise_drift.txt` (full tables with symbol counts, worst cases, placebo counts and period splits are there).

## Hypothesis
H1: a strong YoY quarter is followed by drift. H2: it leaks before release. H3: a strong quarter with a muted 5-session reaction (within +-3%) and trailing P/E below 6 is mispriced. H4: board notices move the stock and the days before the result run up. Buckets use YoY change in attributable net income, not a surprise versus consensus (none exists).

## Data
- EPS file: 2,460 rows, 129 symbols, quarter ends 2019-09 to 2026-09. Returns are bonus/split-only price returns (cash dividends are near-empty before Nov 2024); benchmark is the equal-weight market, Rs5m filter, same method.
- Basis check (5 names): shares and EPS are restated to today's basis, so P/E uses the adjusted close. Naive raw price / restated EPS is off by exactly the action factor (x5.00 LUCK, SYS, LCI, KOHC; x3.36 MTL). Adjusted price / EPS against adjusted price x shares / TTM income: 1.000 (LCI), 1.084 (LUCK), 1.093 (KOHC), 0.904 (SYS, MTL).
- Event timestamp. 1,976 rows had a joined announce_dt (156 Transmission/Annual Report). 144 events moved to an earlier release (median shift 4.5 days, 90th percentile 24.1; 135 were Transmission stamps). The join had also accepted 45 non-result titles (extension applications, briefings): 26 moved to a later valid release (median 23.6 days), 30 with no valid release were dropped. 484 rows had no announce_dt. Dropped by quarter-end year: 2019 2, 2020 1, 2021 63, 2022 121, 2023 111, 2024 108, 2025 83, 2026 25. 55 used stamps read exactly 08:00; 50 events were after 15:30 (t0 = next session).
- Events: 1,585 with announce_dt, t0 and bucket (including LL); 1,125 after the point-in-time Rs5m filter (127 to 120 symbols). By t0 year: 2022 93 to 47, 2023 370 to 187, 2024 380 to 261, 2025 413 to 342, 2026 324 to 283. LL n = 63 (reported as n only). Test sample 1,062 events, 116 symbols, 25 seasons. Buckets: POS 379, LTP 96, NEG 188, PTL 81, MID 318; Positive 475, Negative 269.
- Using EPS instead of net income changes the bucket for 2.8% of events (54 of 1,931).
- Quarter type: Q1 606, Q2 603, Q3 606, Q4 597 rows (48 unresolved); Q2 comes from half-year releases, Q4 is annual minus nine months.
- Consolidation is unverified for the file, but the spot check shows consolidated attributable income for ATRL, HUBC, FABL, PPL. Holding or group names in the sample: ASC, ENGROH, GGL, JVDC, SLGL, SYM, TREET, WAVES, HUBC, FFC, MFL, EFERT, LUCK, MLCF, DGKC, NML, PPL, SNGP, MEBL, LCI, PAEL, SYS, AGP, ABOT, GHNI, HCAR, PSO.
- Dropped for no price observation: 0. Windows past the panel end: H1 +5: 1, +20: 24, +60: 86; H3 +60: 87, +120: 175.

## Method
t0 is the first panel session on or after the announce date (strictly after if stamped after 15:30 PKT). Excess = stock minus equal-weight market. H1 enters at close(t0+1). Reaction and H2 are descriptive; tradable legs subtract 0.5%. Placebo: 20 random traded, liquid sessions, same symbol and calendar year, same window and cost, fixed seed. Seasons = calendar quarter of t0. H1-H3 split at 2020-10..2023 against 2024..2026-10 (EPS events start late 2020); H4 splits 2017-2021 against 2022-2026.

## Results
**H1 drift, entry close(t0+1), net 0.5%, all periods.** Each cell: median / win rate / event-minus-placebo median. "Seas+" is the share of seasons with a positive median.

| Bucket | n (+5/+20/+60) | +5 | +20 | +60 | Seas+ at +60 |
|---|---|---|---|---|---|
| POS | 378/366/338 | -0.2% / 48% / +0.7% | -2.0% / 38% / -0.9% | -2.3% / 43% / -0.5% | 15% |
| LTP | 96/92/88 | -1.8% / 32% / -0.8% | -0.4% / 48% / +1.8% | -2.5% / 45% / +1.1% | 50% |
| NEG | 188/186/181 | -0.5% / 46% / +0.7% | -1.5% / 46% / +1.3% | -5.3% / 39% / +0.7% | 22% |
| PTL | 81/79/78 | -1.1% / 36% / +0.1% | -2.4% / 34% / +0.7% | -2.6% / 44% / +2.6% | 38% |
| MID | 318/315/291 | -1.1% / 37% / -0.1% | -2.3% / 35% / -0.4% | -4.9% / 36% / -1.8% | 12% |
| Positive | 474/458/426 | -0.7% / 45% / +0.2% | -1.6% / 40% / -0.3% | -2.3% / 44% / -0.1% | 24% |
| Negative | 269/265/259 | -0.8% / 43% / +0.5% | -2.1% / 42% / +0.7% | -4.4% / 40% / +1.4% | 22% |
| ALL | 1061/1038/976 | -0.8% / 42% / +0.2% | -2.0% / 39% / -0.1% | -3.3% / 41% / +0.2% | 12% |

Positive mean at +60 is +2.0% against a median of -2.3% (lesson 7). Positive worst cases: -22.2% (ZAL 2026-02-26) at +5, -39.1% (PREMA 2025-04-28) at +20, -91.6% (BNL 2025-10-06) at +60. Positive medians, 2020-10..2023 / 2024..2026-10: +5 +0.3% / -1.0%; +20 -1.8% / -1.6%; +60 +1.4% / -2.8%. Total return (t0 from 2024-11, 218 to 266 events): Positive median -0.9%, -1.2%, -3.2%, event-minus-placebo +0.2%, +0.1%, -0.6%. By quarter type at +60, Positive Q4 median -4.3% (n 99), Q3 +1.8% (n 94).

**Reaction close(t0-1) to close(t0+1), not tradable.**

| Bucket | n | Mean | Median / win / event-minus-placebo median |
|---|---|---|---|
| POS | 379 | +0.8% | +0.2% / 52% / +0.5% |
| LTP | 96 | +1.1% | +0.4% / 54% / +0.9% |
| NEG | 188 | -1.8% | -1.9% / 31% / -1.6% |
| PTL | 81 | -4.0% | -3.9% / 20% / -3.5% |
| MID | 318 | -0.9% | -0.9% / 41% / -0.6% |
| Positive | 475 | +0.9% | +0.2% / 52% / +0.6% |
| Negative | 269 | -2.5% | -2.4% / 28% / -2.1% |
| ALL | 1062 | -0.5% | -0.8% / 43% / -0.4% |

**H2 pre-run, not tradable.** Median / win / event-minus-placebo median.

| Bucket | 5 sessions (t0-6 to t0-1) | 10 sessions (t0-11 to t0-1) |
|---|---|---|
| POS | +0.9% / 58% / +1.3% | +1.0% / 55% / +1.5% |
| Positive | +0.6% / 55% / +1.0% | +0.5% / 53% / +1.1% |
| MID | -0.2% / 48% / +0.3% | -0.5% / 47% / +0.2% |
| Negative | -1.3% / 33% / -0.5% | -1.7% / 39% / -0.4% |
| ALL | -0.3% / 47% / +0.3% | -0.4% / 48% / +0.4% |

Leakage rule (Positive above both MID and placebo) is met on medians: Positive minus MID +0.8 points (5 sessions) and +1.0 (10); minus placebo +1.0 and +1.1. It is weak: Positive beats MID in 62% and 69% of 16 seasons; in 2020-10..2023 the 10-session median is +0.0%. H2 and H4 windows overlap; do not add them.

**H3 muted strong quarter, entry close(t0+5), net 0.5%, one setup per symbol per 120 sessions.** Positive 475; reaction and P/E available 429; muted 208; P/E < 6 142; main 61 before dedupe, 51 after (36 symbols, 46 sector-season clusters). The 60 and 120 session windows usually contain the next quarter's result. H3 is a subset of H1 Positive, not independent confirmation.

| Group | n 60 / 120 | Median +60 (vs placebo, win) | Median +120 (vs placebo, win) | +120 median, 2020-10..2023 / 2024..2026-10 |
|---|---|---|---|---|
| Main: Positive, muted, P/E<6 | 47 / 42 | +2.4% (+2.7%, 57%) | +6.4% (+5.0%, 67%) | +2.4% (n21, +1.9% vs placebo) / +19.0% (n21, +15.4%) |
| Tercile: Positive, muted, bottom-tercile P/E | 47 / 40 | -2.0% (-1.2%, 47%) | +1.0% (+0.4%, 55%) | -2.4% / +1.0% |
| (a) Positive, P/E<6, any reaction | 88 / 80 | +2.4% (+3.3%, 56%) | +7.2% (+6.1%, 61%) | +2.2% / +10.5% |
| (b) Positive, muted, P/E>=6 | 84 / 78 | -4.4% (-1.1%, 32%) | -4.3% (+1.3%, 41%) | +2.8% / -5.9% |
| Reference: all Positive | 425 / 389 | -2.6% (-0.6%, 42%) | -2.4% (+0.8%, 47%) | +2.4% / -3.9% |

Main: mean +8.3% / +12.9%; worst -26.0% (MEBL 2024-08-08) / -47.4% (TOWL 2023-09-27); 13 and 12 seasons, 54% and 58% positive; placebo median -0.3% / +1.4%. With and without 2026 refiners is identical: none of the 8 refinery events in 2026 qualified (7 Positive, 2 muted, 5 with P/E < 6, none all three), so the setup that motivated H3 is not in the data as defined. P/E < 6 and the bottom tercile share 39 of 51 setups.

**H4 board notices, KMI names, net 0.5%.** 15,391 notices (REVOKED, "other than financial results" and same-day "in progress" excluded), 14,230 matched to a result within 30 days, 13,466 after earliest-notice dedupe, 3,610 after the point-in-time filter, 2,688 on KMI names (179 symbols); median leg 5 sessions.

| Window | n | Mean / median / win | Seasons, share positive | Placebo median / win | d median, d win |
|---|---|---|---|---|---|
| Notice day (descriptive), all | 2,688 | +0.2% / -0.0% / 50% | 40, 57% | -0.2% / 44% | +0.2%, +6% |
| Tradable leg n0 to t0-1, all | 2,688 | -0.4% / -0.9% / 41% | 40, 5% | -1.0% / 39% | +0.1%, +2% |
| Leg, 2017-2021 | 1,156 | -0.4% / -0.7% / 43% | 20, 10% | -0.9% / 41% | +0.2%, +2% |
| Leg, 2022-2026 | 1,532 | -0.4% / -1.0% / 40% | 20, 0% | -1.1% / 38% | +0.1%, +2% |

All panel names give the same picture (leg median -0.9%, n 3,610).

## Historical H3 setups, ranked by lowest ex-ante P/E
42 setups, quarter ends before 2026-03-31; top 20 shown. ex60 and ex120 are excess net of cost; mdd120 is worst price drawdown within 120 sessions.

| symbol | qe | announce_dt | t0 | ni_growth | react5 | pe | ex60 | ex120 | mdd120 |
|---|---|---|---|---|---|---|---|---|---|
| ATRL | 2022-12-31 | 2023-02-28 09:18 | 2023-02-28 | +278.8% | -2.5% | 0.67 | +2.4% | +37.4% | -1.5% |
| PRL | 2022-09-30 | 2022-10-21 13:20 | 2022-10-21 | - | +1.6% | 0.76 | -7.1% | -10.7% | -25.3% |
| ATRL | 2023-09-30 | 2023-10-10 08:55 | 2023-10-10 | +63.6% | +2.3% | 0.86 | -15.3% | +2.4% | -1.0% |
| TOWL | 2023-06-30 | 2023-09-27 12:15 | 2023-09-27 | +330.6% | -2.0% | 1.19 | -25.4% | -47.4% | -10.2% |
| OGDC | 2023-06-30 | 2023-09-28 13:16 | 2023-09-28 | +198.9% | -2.9% | 1.86 | -9.8% | -11.1% | -2.4% |
| OGDC | 2022-09-30 | 2022-10-25 13:30 | 2022-10-25 | +58.5% | +2.0% | 1.96 | +37.2% | +36.4% | -1.6% |
| BIPL | 2024-03-31 | 2024-04-26 08:23 | 2024-04-26 | +78.4% | -2.1% | 2.03 | -6.1% | -20.2% | -9.2% |
| PPL | 2023-06-30 | 2023-09-20 12:41 | 2023-09-20 | +461.5% | -2.3% | 2.04 | +21.4% | +4.6% | -2.2% |
| PPL | 2022-09-30 | 2022-10-27 12:20 | 2022-10-27 | +56.2% | -2.5% | 2.27 | +64.2% | +39.2% | -2.6% |
| FABL | 2023-12-31 | 2024-02-07 12:26 | 2024-02-07 | +119.4% | -2.0% | 2.38 | +3.0% | +27.5% | -7.1% |
| HUBC | 2024-03-31 | 2024-04-29 11:28 | 2024-04-29 | +52.8% | -0.1% | 2.43 | -2.3% | -42.3% | -30.4% |
| DCR | 2023-12-31 | 2024-02-27 13:02 | 2024-02-27 | +180.5% | -2.4% | 2.53 | +3.5% | +2.4% | +0.0% |
| FABL | 2024-06-30 | 2024-08-28 12:08 | 2024-08-28 | +59.7% | +1.5% | 2.87 | -25.0% | -33.9% | -10.0% |
| FABL | 2022-12-31 | 2023-02-23 12:46 | 2023-02-23 | +68.5% | -2.3% | 3.02 | -9.5% | -8.3% | -12.4% |
| MEBL | 2023-09-30 | 2023-10-19 14:29 | 2023-10-19 | +123.3% | -0.9% | 3.19 | -3.1% | +22.9% | -0.6% |
| LOTCHEM | 2022-12-31 | 2023-02-10 12:21 | 2023-02-10 | +42.5% | +0.6% | 3.20 | +7.4% | -15.0% | -9.9% |
| FCCL | 2022-12-31 | 2023-02-14 12:57 | 2023-02-14 | +64.2% | +1.5% | 3.36 | +3.1% | -11.1% | -2.2% |
| MARI | 2023-09-30 | 2023-10-26 11:49 | 2023-10-26 | +50.6% | +0.7% | 3.39 | +27.1% | +36.5% | +0.0% |
| LUCK | 2023-09-30 | 2023-10-30 08:00 | 2023-10-30 | +224.9% | +2.9% | 3.42 | -7.0% | -7.3% | -1.6% |
| MEBL | 2023-03-31 | 2023-04-19 09:00 | 2023-04-19 | +68.1% | -2.1% | 3.47 | +19.7% | +18.4% | -15.8% |

Across all 42: median ex60 +3.1%, ex120 +6.4%. Across the 20 lowest-P/E: median ex60 +0.0%, ex120 -2.4%. The lowest P/Es (ATRL, PRL, TOWL, OGDC, PPL) sit on windfall or cyclical-peak earnings; DCR's profit includes a Rs2.9bn unrealised fair-value gain.

## Live H3 screen as of close 2026-10-16 (unresolved, not evidence)

| symbol | qe | t0 | ni_growth | react5 | pe_decision | pe_today | sessions_elapsed | excess_so_far_net |
|---|---|---|---|---|---|---|---|---|
| STL | 2026-06-30 | 2026-09-24 | - | -0.7% | 0.83 | 0.77 | 11 | -3.7% |
| NML | 2026-06-30 | 2026-09-30 | +51.4% | -1.2% | 3.07 | 3.08 | 7 | -0.6% |
| NML | 2026-03-31 | 2026-04-30 | +88.0% | +2.1% | 4.66 | 3.79 | 108 | -12.9% |
| WAVES | 2026-06-30 | 2026-08-31 | +69.1% | +1.9% | 4.83 | 4.30 | 29 | -4.2% |
| GHNI | 2026-03-31 | 2026-04-17 | +54.2% | +0.4% | 5.06 | 6.34 | 117 | +27.5% |
| ENGROH | 2026-03-31 | 2026-04-27 | +428.2% | +2.1% | 5.56 | 5.28 | 111 | -6.3% |
| OGDC | 2026-06-30 | 2026-09-04 | +215.4% | +1.5% | 5.61 | 5.31 | 25 | -5.1% |
| SLGL | 2026-03-31 | 2026-04-29 | +53.7% | -1.9% | 5.70 | 5.72 | 109 | +3.7% |
| GHGL | 2026-06-30 | 2026-08-27 | +67.2% | +1.0% | 5.71 | 5.42 | 31 | +0.4% |
| GHGL | 2026-03-31 | 2026-04-28 | +39.2% | +2.4% | 5.88 | 6.33 | 110 | +6.6% |
| ECOP | 2026-06-30 | 2026-09-14 | +34.4% | -0.8% | 5.95 | 5.10 | 19 | -8.0% |

Median excess so far -3.7%; none is near 120 sessions. ENGROH's StockAnalysis income is 5.7% below the filing, so its P/E is a little lower than shown.

## Spot check against filings
Historical list (20): automatic text parse matched 2, mismatched 1, unreadable 17 (scanned images). After reading the rendered PDFs by eye: matched 19, mismatched 0, unreadable 1 (MEBL 2023-03-31, no document id). Live list (11): automatic 2/1/8; after visual reading matched 10, mismatched 1 (ENGROH: filing 10,236m, EPS 8.50; StockAnalysis 9,650m, 8.01), unreadable 0. Annual and half-year filings were compared with sums of StockAnalysis quarters. Per-share figures are confirmed as restated (FCCL 2.25 as filed against 2.07; MARI 143.50 against 15.94; LUCK 57.80 against 11.56).

## Robustness
H1 shows no drift in either half; total return from 2024-11 matches price return. H3 main is positive in both halves at +60 (+2.4%, +2.5%), but at +120 it sits in 2024..2026-10 (+19.0%, 7 seasons, 71% positive) and is small earlier (+2.4%). Lesson 9: the 2022-2025 rerating is a tailwind; the placebo in the same names rose a median +3.6% (+120, 2024 on).

## Verdict
- H1: no tradable drift. Positive medians are negative net of cost; event-minus-placebo stays within about 1 point except LTP +20, NEG +60, PTL +60 (1.1 to 2.6 points, 22% to 50% of seasons positive).
- Reaction: the news is priced within two sessions, bad news hardest.
- H2: weak leakage, about 1 point for Positive, not robust across periods.
- H3: not confirmed. The edge is in low absolute P/E, not the muted reaction (group (a) matches main), is absent in the tercile version, and comes from 2024-2026. n = 42 to 47, 12 to 13 seasons.
- H4: nothing; indistinguishable from placebo.

## Caveats
Survivorship: only names listed on 2026-10-16; the benchmark is survivor-biased. The 92 base names and the KMI list are not point-in-time. 20% of symbol-quarters lack announce_dt. StockAnalysis may be revised. Consolidation is verified only for spot-checked names. Price-return primary understates returns for high payers. The 2022-2025 rerating is a tailwind. YoY change is not a consensus surprise. 60 and 120 session windows overlap later results and sector shocks. 08:00 stamps may be placeholders.
