# Rate-cycle and inflation turns (redo of seed H1-H6)

Run 17 Oct 2026. Script `scripts/tests/rate_cycle_episodes.py`, raw output `tests/out/rate_cycle_episodes.txt` (every number below is from it; full per-event, per-sector and per-hike tables are there). Paths follow the task header, not the spec's `test_rate_cycles.py` names.

## Hypothesis

H1 after a cut the market rises at 20/60/120 days. H2 the first cut of a cycle is strongest. H3 the first hike is weak. H4 a CPI fall of 1pt+ over 3 months is followed by +44% in 12 months. H5 the 6M T-bill anticipates cuts. H6 sector returns after a first cut persist. The seed pooled 13 overlapping cuts and measured pre-sample cuts from the first index day; both are corrected.

## Data

- KSE100 `data/macro/kse100.csv`, 2,480 rows, 2016-10-17 to 2026-10-16: calendar and headline series. PSX publishes it as a price index (no dividends, none added; lesson 19). That comes from index methodology; the file has no dividend column.
- `prices.load_panel()`: 2,480 dates x 456 symbols (survivors only). Liquid names at t0: 70 (Jan 2018), 81 (Mar 2020), 118 (Jun 2024), 196 (Dec 2025).
- `policy_rate_decisions.csv` (84), `tbill_auctions.csv` (308, 38 blank 6M), `cpi.csv`, `symbols.csv` (37 sectors after dropping ETFs, debt, bills).

## Method

t0 is the close of the first trading day strictly after the announcement; return is close[t0+h]/close[t0]-1; windows past 16 Oct 2026 are incomplete and excluded from statistics. A cycle is a run of same-direction moves; a cluster has no gap above 120 trading days. In sample: 2 cut cycles (2020-03-17, 2024-06-10), 3 cut clusters (adding the 2025-12-15 resumption), 3 hike cycles (2018-01-29, 2021-09-20, 2026-04-27). The five 2015 to May 2016 cuts are not computable and not measured. EW is a buy-and-hold basket of `liquid_universe(t0)` from `returns(close,'crude')`; EWX drops names with a flagged day (suspected-actions log, a -8% to -10.5% normal-volume day above Rs10, or a provisional bonus/split ex-date); EWA uses `method='adjusted'` with `provisional_actions()`. Cost is 0.5% per round trip (net shown). Placebo P1: 10,000 draws of k random dates, t0 from 2016-10-18, same series and horizon, basket rebuilt each draw; percentile = rank of the observed k-mean. For k <= 3 there is no statistical power and percentiles are descriptive.

EW survivorship: the panel holds only symbols listed on 16 Oct 2026, so delisted losers are missing and EW is biased up. KSE100 is the headline.

## Results

### H1 every in-sample cut (gross, KSE100 unless stated)

| cut | cluster | KSE 20 | KSE 60 | KSE 120 | EW 120 | KSE max DD 120 | 120d overlaps prior cut |
|---|---|---|---|---|---|---|---|
| 2020-03-17 | cl4 | +3.0% | +10.3% | +39.8% | +74.6% | -11.2% | no |
| 2020-03-24 | cl4 | +19.2% | +25.0% | +56.1% | +112.3% | -4.8% | yes |
| 2020-04-16 | cl4 | +3.0% | +13.7% | +21.9% | +41.4% | -8.4% | yes |
| 2020-05-15 | cl4 | -1.1% | +18.9% | +21.9% | +38.9% | -8.4% | yes |
| 2020-06-25 | cl4 | +10.8% | +23.2% | +27.8% | +50.0% | -8.4% | yes |
| 2024-06-10 | cl6 | +10.1% | +8.4% | +49.1% | +49.2% | -5.8% | no |
| 2024-07-29 | cl6 | -0.8% | +13.1% | +46.6% | +52.2% | -8.5% | yes |
| 2024-09-12 | cl6 | +7.5% | +38.6% | +41.5% | +34.3% | -8.5% | yes |
| 2024-11-04 | cl6 | +13.3% | +20.8% | +20.6% | +16.6% | -8.5% | yes |
| 2024-12-16 | cl6 | -0.3% | +0.2% | +6.2% | -0.5% | -13.0% | yes |
| 2025-01-27 | cl6 | +1.6% | +2.5% | +24.4% | +12.4% | -13.0% | yes |
| 2025-05-05 | cl6 | +7.2% | +24.2% | +42.8% | +38.4% | -8.8% | yes |
| 2025-12-15 | cl7 | +7.1% | -9.4% | +1.1% | -7.0% | -22.6% | no |

Context columns are in the output. Median reaction-day move on cuts is -0.5%: no announcement pop.

### H1 headline, first cut of each cluster (n_eff = 3, no statistical power)

| series | h | mean | median | win | worst | placebo median (5-95%) | obs pctile | net mean |
|---|---|---|---|---|---|---|---|---|
| KSE100 | 20 | +6.7% | +7.1% | 100% | +3.0% | +1.3% (-4.6 to +7.3) | 93 | +6.2% |
| KSE100 | 60 | +3.1% | +8.4% | 67% | -9.4% | +3.7% (-6.7 to +16.3) | 46 | +2.6% |
| KSE100 | 120 | +30.0% | +39.8% | 100% | +1.1% | +7.9% (-7.8 to +26.7) | 97 | +29.5% |
| EW | 20 | +5.3% | +3.9% | 100% | +3.3% | +0.8% (-7.3 to +8.8) | 82 | +4.8% |
| EW | 60 | +3.0% | +11.9% | 67% | -21.5% | +1.9% (-11.7 to +18.8) | 55 | +2.5% |
| EW | 120 | +39.0% | +49.2% | 67% | -7.0% | +5.1% (-15.2 to +28.6) | 99 | +38.5% |

Unconditional single-date KSE100 120d: median +3.3%, win 58%. Worst 120d drawdown: KSE -22.6%, EW -31.1% (Dec 2025). EW minus KSE at 120d: +34.8, +0.1, -8.1 points (2020, 2024, 2025). Greedy non-overlapping KSE sets: 20d n=12 mean +5.1% (win 75%, placebo +1.4%, pctile 98); 60d n=7 +13.6% (86%, pctile 97); 120d n=4 +24.1% (median +23.0%, win 100%, worst +1.1%, placebo +8.0%, pctile 95). The pooled 13-cut mean (+30.8% at 120d) is overlapping, n_eff = 3.

### H2 and H3 (anecdotes, 2 and 3 cases)

| first move | KSE 20 / 60 / 120 | EW 120 | rank at 120d in cycle | later-move median (120d KSE) |
|---|---|---|---|---|
| cut 2020-03-17 | +3.0 / +10.3 / +39.8% | +74.6% | 2 of 5 | +24.8% |
| cut 2024-06-10 | +10.1 / +8.4 / +49.1% | +49.2% | 1 of 8 | +24.4% |
| hike 2018-01-29 | -2.2 / +2.8 / -4.8% | -9.1% | 5 of 9 | -4.6% |
| hike 2021-09-20 | -1.1 / -3.6 / -6.4% | -22.2% | 10 of 11 | +0.1% |
| hike 2026-04-27 | +1.3 / +4.5 / -1.2% (incomplete, 115d) | -1.1% (incomplete) | not computable | none yet |

At 60 days the first cut ranks 5 of 5 (2020) and 5 of 8 (2024). The 2020 cut sat in the COVID crash: KSE100 fell to -10.5% below t0 on 2020-03-25 before rebounding. Shifting the approximate 2018-01-29 t0 by -3 to +3 days gives KSE 20d -3.7% to -1.1%, 60d +1.2% to +3.4%, 120d -9.2% to -1.6%. Complete first hikes at 120d: median KSE -5.6%, EW -15.6%, placebo pctile 15 and 10 (k=2).

### H4 CPI fall of 1pt+ over 3 months (yoy from PBS release where present, 2026-09 excluded)

37 signal months form 13 runs; 11 are measurable after Oct 2016, 10 with a complete 250d window. The largest run (2024-02 to 2025-04) supplies 15 of 37 months (41%); the audit's 21 of 33 was not reproduced (different yoy source).

| run start | months | yoy at start | KSE 120 | KSE 250 |
|---|---|---|---|---|
| 2015-04, 2015-08 | 1, 2 | 2.13, 1.80 | not computable (pre-sample) | |
| 2017-06 | 3 | 3.92 | -9.9% | -10.1% |
| 2018-03 | 1 | 3.23 | -18.7% | -21.1% |
| 2020-03 | 4 | 11.38 | +32.7% | +45.2% |
| 2020-12 | 2 | 7.98 | +5.0% | +1.6% |
| 2021-07 | 2 | 8.40 | -5.3% | -11.0% |
| 2022-11 | 1 | 23.80 | -0.5% | +59.4% |
| 2023-06 | 3 | 29.40 | +40.5% | +81.0% |
| 2023-10 | 1 | 26.80 | +33.5% | +73.3% |
| 2023-12 | 1 | 29.70 | +25.6% | +78.7% |
| 2024-02 | 15 | 23.10 | +20.2% | +73.8% |
| 2026-07 | 1 | 9.20 | -8.4% (incomplete, 49d) | -8.4% (incomplete) |

| series | h | n runs | mean | median | win | worst | placebo median (5-95%) | obs pctile | net mean |
|---|---|---|---|---|---|---|---|---|---|
| KSE100 | 120 | 10 | +12.3% | +12.6% | 60% | -18.7% | +8.1% (-0.9 to +17.9) | 77 | +11.8% |
| KSE100 | 250 | 10 | +37.1% | +52.3% | 70% | -21.1% | +19.8% (+3.1 to +38.5) | 94 | +36.6% |
| EW | 250 | 10 | +31.4% | +53.1% | 60% | -33.8% | +14.1% (-6.0 to +35.8) | 90 | +30.9% |

Six of 10 runs reached +44% at 250d (KSE), but five start between Nov 2022 and Feb 2024 with overlapping windows: about two independent episodes (2020, 2022-24). Mirror (CPI rise of 1pt+, 16 runs): KSE 250d mean +24.3%, median +12.0% (n=15, pctile 69); 120d mean +6.6%, median +0.9% (pctile 38).

### H5 T-bill signal (y6m below the prevailing policy rate)

| first cut | variant | signal auction | N weeks | M1 KSE gross / net | M2 trough (hindsight) |
|---|---|---|---|---|---|
| 2020-03-17 | primary and 50bp | 2020-03-11 (12.51 vs 13.25) | 0.9 | -15.4% / -15.9% | 2019-09-11 |
| 2020-03-17 | 100bp, 2 consecutive | not fired before the cut | | | |
| 2024-06-10 | primary | 2023-11-01 (21.99 vs 22.00) | 31.7 | +37.9% / +37.4% | 2023-06-23 |
| 2024-06-10 | 50bp and 2 consecutive | 2023-11-15 | 29.7 | +26.5% / +26.0% | 2023-06-23 |
| 2024-06-10 | 100bp | 2024-01-10 | 21.7 | +12.3% / +11.8% | 2023-08-31 |

Dec 2025 resumption: primary fired 2025-12-10 by 0.0pp (10.9999 vs 11.0), N = 0.7 weeks. y6m minus policy at the last auction before each cluster-first cut: -0.74 (2020), -1.00 (2024), -0.00 (2025). 2015 cycle: not computable. False positives: primary 1 unresolved (2026-07-08; its 26 weeks run past the last auction), 50bp 1 settled (2026-01-21), 100bp none, 2-consecutive 1 settled (2025-12-24 to 2026-02-18). Auction-level hit rates 84%, 93%, 100%, 86% (of 73, 41, 22, 66 firing auctions) are flattered because the curve stays below policy through a whole easing cycle. Before first hikes y6m exceeded policy by 0.26, 0.49, 0.65pp (first crossing 87.7, 59.7, 7.7 weeks ahead).

### H6 sectors after a first cut (120d excess over EW; baskets need 3+ names)

| cut | top 3 | bottom 3 |
|---|---|---|
| 2020-03-17 | Technology +79.1%, Inv. banks +62.1%, Auto assemblers +42.1% | Power -26.0%, E&P -38.4%, Commercial banks -47.1% |
| 2024-06-10 | Pharma +59.3%, OMCs +59.3%, Fertilizer +40.5% | Glass -34.2%, Power -36.5%, Textile composite -38.3% |
| 2025-12-15 | Insurance +26.6%, Paper +24.2%, Property +19.5% | Cable -10.7%, Textile spinning -14.4%, Inv. banks -17.3% |

Spearman, 2020 vs 2024 sector excess: +0.63 at 60d, -0.06 at 120d (14 sectors). Per-sector placebo (mean 120d excess over the 3 episodes; pctile): Power -19.7% (3rd), Commercial banks -12.0% (5th), Textile composite -16.4% (3rd), Chemical -16.0% (9th); Technology +25.2% (88th), Inv. banks +15.7% (95th); k <= 3. Net of cost each excess falls 0.5 points. Islamic banks (fixed list MEBL, BIPL): two-bank 120d excess -38.2%, -32.5%, +4.0% (mean -22.2%, placebo median +1.2%, pctile 6); the MEBL 2020 and BIPL 2025 windows carry a flagged day.

### Current setup (from files)

Policy 11.5%, held since the 27 Apr hike. 6M bill 12.3989 on 2026-10-14, +90bp over policy: every H5 variant OFF. CPI yoy 2026-06/07/08: 11.1/9.2/11.1 (PBS); 2026-09: 10.3 (seed, unverified). Jun to Sep change -0.80 (-0.78 on seed yoy), above the -1.0 trigger; verified May to Aug -0.60. Real rate +0.40pp (+1.20pp on the unverified 10.3). Next MPC 26 Oct 2026. Conditions for the next first cut, stated in advance: y6m below the prevailing policy rate at an auction (50bp and 2-auction variants as confirmation) plus a PBS-verified 3-month CPI change of -1.0 or lower. Conditional history from 2 cut cycles, not a forecast.

Proposed frozen row (not appended; a policy-rate row for 26 Oct already exists with cut at 0.02):
`2026-10-17,Policy rate,SBP MPC decision: no cut,2026-10-26,"SBP does not cut at the 26 Oct 2026 MPC (hold or hike)",0.97,"6M T-bill +90bp over policy (H5 OFF); CPI 3m change not <= -1.0; n=2 cycles, conditional history.",,,`

## Robustness

- Bonus handling, EW 120d at cluster-first cuts: +74.6/+49.2/-7.0%; excluding flagged names (6, 34, 152 of 81, 118, 196): +73.5/+44.1/-8.8%; adjusted with provisional actions: +74.6/+49.5/-6.4%. The candidate-bonus rule is loose: in the Dec 2025 window it flags 152 names with a -8% to -10.5% day, a sell-off not bonuses; the provisional table has 12 bonus/split rows, none in these windows. One 10% bonus (about -9.1%) in a 5-name basket costs about 1.8 pts: baskets dilute the bias, not remove it.
- Event sets: cluster-first (n=3), greedy per horizon, pooled (overlapping), first-cut-of-cycle (n=2, 120d KSE mean +44.5%, placebo pctile 100).
- P2, MPC holds (in sample, overlapping): KSE 20d n=39 mean +1.4%, median +0.3%, win 54%; 60d n=37 +5.4%, +5.5%, 62%; 120d n=36 +9.8%, +4.4%, 61%.
- H4 all signal months (overlapping, 33): KSE 250d mean +45.4%, median +59.2%.

## Verdict

H1: weak. KSE100 rose at 120 days after all three cluster-first cuts (+39.8%, +49.1%, +1.1%) against a placebo median of +7.9%, but n=3 gives no power, 60d is a coin flip (median +8.4%, one -9.4%), and the 2025-12 resumption was flat with a -22.6% drawdown. H2: anecdote; the first cut won at 120d in both cycles and lost at 60d. H3: weak, direction consistent (both complete 120d windows negative; 2026 incomplete). H4: weak as a 12-month rule: 6 of 10 runs hit +44% but sit in two episodes, and the mirror also rose. H5: a coincident gauge (cycle starts had y6m at or below policy), weak as a lead (N from 0.9 to 31.7 weeks; the 2024 signal sat 1bp under policy 32 weeks early). H6: not persistent at 120d; power and textiles lagged both times.

Strategy: the curve is above policy, so history gives no cut setup and no reason to add rate-cut exposure ahead of 26 Oct. Do not size on a rate-cycle signal; treat a first cut as a regime marker to check against price and flows.

## Caveats

- n = 2 cut cycles, 3 clusters, 3 hikes: no statistical power.
- EW and sector baskets hold only names listed on 16 Oct 2026 (biased up) and keep part of the bonus bias.
- CPI is rebased retroactively (PBS 2020), so pre-2020 values are not real-time; 2026-09 (10.3) is unverified and excluded from signals.
- 2018-01-29 is approximate; the 2026-04-27 120d window and the 2026-07 CPI run are incomplete.
- KSE100 roughly quadrupled over the sample: read post-event means against the unconditional 120d median +3.3% and mean +8.4%, not zero.
- Sector membership is current PSX sectorName and today's names. M2 troughs use hindsight. The pre-2015-01-31 prevailing rate (9.5) is derived from the first decision row.
