# Informed capital: does a rise on no public information precede news?

Run 18 Oct 2026. Script `scripts/tests/informed_capital.py`. Raw output `tests/out/informed_capital.txt` (all variants, all splits, both case lists, the name-by-name repeater table).

## Hypothesis

The investor's: on PSX a sustained rise with no public information often precedes news, because insiders know. If true, (a) news-less rises should be followed by filings more often than chance, (b) the stock should keep rising into and after the news, and (c) joining the rise should pay after costs.

## Data

`data/daily_table.parquet` (577,794 stock-days, 455 names including 142 delisted, 2017-01-02 to 2026-10-16) and `data/announcements.parquet` for filing dates and titles. Features are known at the close of t; entry is the next open; costs are 0.5% round trip plus 0.5% under Rs20m median traded value (`data/costs.md`, brokerage rate unverified); 15% CGT on gains is not deducted. ret_10d and the trailing stop use a price index rebuilt from the table's `ret_1d`; it reproduces `ret_5d`, `ret_20d` and `ret_fwd_5` exactly, and my sector-filtered level 1 matches `is_newsless_rise` on 17,313 of its 17,336 days.

## Method

Signals (null `days_since_last_filing` is excluded; any filing class counts, including AGM and "other"):

| Level | Rule | Signal-days | Episodes | Names |
|---|---|---|---|---|
| R1 | ret_5d > 8%, no filing in 10 sessions | 28,791 | 8,001 | 388 |
| R2 | ret_5d > 8%, no filing in 5 | 37,802 | 10,413 | 393 |
| R3 | ret_10d > 12%, no filing in 20 | 16,617 | 3,786 | 370 |
| R1f, R2f, R3f | the same plus sector_ret_5d < 3% (index return where no basket) | 17,313 / 22,188 / 11,163 | 5,935 / 7,571 / 3,163 | 385 / 393 / 362 |
| F1 to F3 (+f) | mirror: ret ≤ -8% or -12%, same filing rules, sector > -3% for the f versions | 6,847 to 28,663 | 2,506 to 9,372 | 332 to 396 |

An episode is a name's first signal day, then a 20-session re-arm; all statistics use episodes. R1f has 5,935 on 1,848 dates, 5,895 in-sample (to 2026-08) and 40 out-of-sample (2026-09 to 2026-10); 83% are under Rs5m median traded value.

Exits: time exits of 5, 10, 20 and 60 sessions from the next open, and a 20% trailing stop on closes (`trail20`, from the volume-ignition test, capped at 120 sessions). **There is no "mining test" file in the repo yet, so I used the exits of the closest existing test, the volume-ignition study; if the mining test uses different exits, rerun.** Placebo: for every episode, 500 random draws of a row on the same date in the same liquidity tier (above Rs20m, Rs5m to 20m, under Rs5m), same exit, same cost; p(med) is the share of draws whose median is at or above the signal's. baseA is the share of the same names' rows in the same months followed by a filing (the table's `filing_within` columns); baseB restricts that to rows in the same silent state, separating "the rise" from "the name has been quiet".

## Results

### 1. Is a news-less rise followed by filings more than chance?

R1f, share of episodes followed by a filing in the next 5, 10 and 20 sessions (obs / baseA / baseB, %):

| Class | 5 sessions | 10 sessions | 20 sessions |
|---|---|---|---|
| financial_result | 1.2 / 5.3 / 1.3 | 9.2 / 10.8 / 9.0 | 25.8 / 24.2 / 26.3 |
| material_info | 1.9 / 1.4 / 2.0 | 3.8 / 2.9 / 3.9 | 7.1 / 6.1 / 7.0 |
| dividend_or_bonus | 0.7 / 0.7 / 0.9 | 1.7 / 1.5 / 1.9 | 3.1 / 2.9 / 3.2 |
| insider_trade | 2.3 / 1.6 / 2.3 | 4.1 / 3.1 / 4.2 | 7.2 / 6.3 / 7.3 |
| board_meeting_notice | 9.6 / 5.9 / 9.3 | 18.0 / 12.2 / 17.7 | 34.4 / 28.7 / 36.1 |
| any of the five | 14.7 / 13.7 / 14.8 | 26.6 / 23.4 / 26.7 | 45.6 / 42.6 / 47.4 |

Any of five within 10 sessions, all variants (obs / baseA / baseB): R1 27.4 / 24.8 / 28.6; R1f 26.6 / 23.4 / 26.7; R2 31.7 / 29.8 / 32.4; R2f 30.5 / 28.2 / 30.4; R3 26.5 / 25.1 / 28.6; R3f 26.3 / 23.8 / 26.9. Mirror falls: F1 26.2 / 23.7 / 27.1; F1f 25.0 / 23.4 / 26.0; F2f 29.4 / 28.2 / 30.4; F3f 26.6 / 26.0 / 28.2.

Against the unconditional base the rise looks informative: 13% more filings (z about 9), with material_info 1.3x, insider_trade 1.3x and board_meeting_notice 1.5x. Against the like-for-like base it is nothing: lifts of 0.94 to 1.03, z between -1.7 and +1.1 for every class at 10 sessions, and exactly chance in total (26.6 vs 26.7). A news-less fall is followed by the same filings as a news-less rise (25.0 vs 26.6; material_info 2.3 vs 3.8 and insider 3.2 vs 4.1, but those names also file more in baseB, 2.5 and 3.5 versus 3.9 and 4.2). The excess comes from silence: a name quiet for ten sessions is nearer its next scheduled notice, whichever way it moved. Board notices and financial results are calendar items; the non-calendar classes are rare (material_info 3.8%, insider_trade 4.1% of episodes). Any-of-five at 10 sessions (obs / baseB) holds across splits: in-sample 26.4 / 26.5, out-of-sample 58.8 / 53.5 (n 34, results season), bill>policy 26.4 / 26.6, bill≤policy 27.0 / 26.9, tier A 38.8 / 41.1, tier B 34.6 / 35.6, tier C 24.5 / 24.3.

### 2. Return path, net, entry at the next open (R1f; placebo in brackets)

| Exit | n | Mean | Median | Win % | >+10% | >+50% | Worst | Placebo median / mean | p(med) |
|---|---|---|---|---|---|---|---|---|---|
| T5 | 5,655 | -0.3 | -1.3 | 39 | 13.0 | 0.4 | -48 | -1.0 / -0.1 | 1.000 |
| T10 | 5,739 | +0.1 | -2.2 | 39 | 16.5 | 1.4 | -76 | -1.0 / +0.5 | 1.000 |
| T20 | 5,779 | +1.5 | -2.5 | 41 | 20.9 | 3.4 | -100 | -1.2 / +1.4 | 1.000 |
| T60 | 5,659 | +4.9 | -4.0 | 43 | 28.4 | 7.6 | -97 | -2.3 / +4.6 | 1.000 |
| trail20 | 5,761 | +3.4 | -9.8 | 34 | 24.3 | 7.3 | -101 | -7.4 / +4.1 | 1.000 |

The median is below the random-entry median at every exit and the mean is the same as random (p(mean) 0.38 at T20, 0.88 at trail20). R1, R2, R3 and the f versions give T20 medians of -1.4 to -3.0, means +1.0 to +2.2, p(med) 1.000. By liquidity (R1f, T20, n / mean / median / win %): tier A 541 / -0.5 / -3.7 / 38; tier B 432 / -0.2 / -3.3 / 43; tier C 4,806 / +1.9 / -2.3 / 41. Regime, T20 mean and median: bill>policy +0.6 / -2.6 (n 4,195); bill≤policy +3.8 / -2.2 (n 1,584); at trail20 the mean is +0.1 against +12.2. Out-of-sample (n 21 at T20): mean +4.7, median -4.9, carried by three episodes above +50%; trail20 (n 13) mean -13.6. 17.8% of entries are on sessions that close at the upper lock (open possibly unfillable); excluding them gives T20 +0.2 / -3.0. Over 20 sessions the median MFE is +10.2%, MAE -11.1%; 18.5% of entries trade 20% below the open.

### 3. From the news day onward (R1f; 1,574 of 5,935 episodes have one of the five classes within 10 sessions, median 5 sessions later)

From the next open to the close before the news the stock does not run: median -0.3%, mean +1.0% (n 1,303). The news session itself moves median 0.0%, mean +0.5%, up in 48%. Entering at the open after the news session, net: T5 -1.1 mean / -1.7 median; T10 -0.9 / -3.0; T20 +0.4 / -3.1 (win 40%, worst -99); trail20 +4.9 / -10.9. All are at or below random news-day entries in the same month and tier (p(med) 0.998 to 1.000). The same episodes entered at the signal made T20 +1.8 / -3.4. By the class of the first filing, n 74 to 926: board meeting notices (n 948) T20 -0.1 / -3.6; material_info (n 165) -0.2 / -2.7; insider_trade (n 215) +0.9 / -1.7; dividend_or_bonus (n 74) +4.0 / -1.5, the one cell with p(mean) 0.03 against placebo. The news is neither the top nor a launch.

### 4. Mirror: news-less falls (long only)

Buying a fall does better than a random entry: F1f at T20 mean +2.9, median -0.4, win 49% (n 5,000; placebo -1.4 / +1.1, p(med) 0.000); F3f (ret_10d < -12%) +4.1 / +0.7, win 52% (n 2,413). The edge sits in the thin names: tier A F1f T20 is +0.0 / +0.1 (placebo -1.1 / 0.0), tier B -0.3 / -2.7. Out-of-sample F1f T20 (n 50): -1.1 / -4.7. A mild reversal effect, not informed capital, with a median about zero before CGT.

### 5. Repeaters

"3+ times" covers 350 names and 5,880 of 5,935 episodes, so it does not select. Most frequent: DAAG 55 episodes, JATM 52, LEUL 51, DWSM 48, PIM 48. In the top 40, T20 median is positive for four names only (FEM +5.5, NCML +3.1, ASTM +1.5, FRCL +1.1); followed-by-news shares run from 5% (FFLM) to 34% (FANM). Point-in-time: the 3rd or later episode of a name has T20 mean +1.7, median -2.4, win 41% (n 5,180) against +0.3 / -3.5 for the first two; a repeat flag (2+ episodes in the prior 252 sessions) gives +1.7 / -2.7 (n 3,824) against +1.0 / -2.1, p(med) 1.000 versus placebo, tier A repeats +0.7 / -3.8 (n 215). Names whose earlier episodes were followed by news at 50% or more saw news again 38.1% of the time against 24.6%: propensity is a property of the name, mostly board notices. The repeats did not pay.

### 6. Case lists

Full lists (dates, titles, outcomes) are in the raw output. The 30 largest R1f rises followed by a five-class filing within 10 sessions are mostly sub-Rs1m names (KHYT +427% in 5 days, SERF, SLCL), 16 of 30 headed "Board Meeting"; entries made T20 median +1.3, mean +5.6, win 50%, largely unfillable. The 30 largest followed by nothing in any class made T20 median -11.5, mean +2.7, win 28%, driven by outliers (DMTM +266%, JUBS +72%, KSTM -74%, KHYT -62%). At Rs5m or more: followed T20 median -4.1, mean +2.4, win 37%; nothing -5.5 / -2.0, win 37%. Liquid examples with a filing: BECO 2025-09-24 (T20 +45.7), TELE 2021-04 (+96.5), KPUS 2026-07-14 (-59.5). Across all R1f episodes: followed by a five-class filing T20 +1.6 / -3.6 (n 1,574); no filing of any class +0.9 / -2.3 (n 3,765).

## Robustness

- Year: R1f T20 median is negative every year (-0.3 in 2020 to -5.3 in 2017); the mean is +5.9 to +6.5 in 2024 and 2025 and -3.0 and -2.0 in 2017 and 2022.
- What distinguishes the ones that paid (in-sample, exploratory, many cuts): almost nothing. Paid and unpaid episodes have the same median ret_5d (11.1% vs 11.2%), volume ratio, distance from the high and traded value; followed by news makes no difference (median T20 -3.5 vs -2.2). Fewer upper locks in the last 5 sessions is better (0 locks T20 median -1.5, trail20 -5.9, n 1,543; 3 or 4 locks -5.8 to -6.4, trail20 about -12 to -13); the top ret_5d quartile (above 15%) is worse (median -3.5, trail20 -11.4). Positive means come from sub-Rs5m names, non-KMI names (T20 mean +4.1 vs +1.8), and the easing regime. What pays is a rare tail (3.4% of entries above +50% at T20), not a typical case.
- The filing result is the same at all three strictness levels, with and without the sector filter.

## Verdict

1. Does a news-less rise predict news more than chance? Against the base of the same names and months, yes by 13% (26.6% vs 23.4%). Against the same names in the same silent state, no (26.7%), and a news-less fall behaves the same. The signal is silence, not the rise; there is no sign of the non-calendar classes (material_info, insider_trade) being pulled forward.
2. Does joining pay after costs with the tested exits? No. Median net return is negative at every exit (T20 -2.5%, trail20 -9.8%), below random same-date entries (p(med) 1.000), and the mean equals random. Above Rs5m, T5 to trail20, the mean is -1.4% to +1.3% and the median -2.3% to -11.7%. Out-of-sample is 40 episodes and says nothing.
3. What distinguishes the ones that paid? Nothing measured at entry. The tail winners are small non-KMI names in easing regimes.

## Caveats

- No mining test file existed; exits are as stated in Method.
- 83% of episodes are under Rs5m, where spreads and fills are unverified (`costs.md`); 17.8% enter on a limit-up close. The table does not model fill.
- Delisting losses after the last print are not captured; sector baskets are survivor-heavy hindsight; a few extreme ret_5d values in cheap names (KHYT, DKL) may be data breaks.
- Filings: the five classes plus agm, credit_rating and other; "other" (96k filings) counts as a filing in the lookback. The 15:30 cutoff is a simplification.
- Out-of-sample is 40 episodes. The "what paid" cuts are exploratory, with no multiple-testing correction.
- 15% CGT on gains is not deducted anywhere.
