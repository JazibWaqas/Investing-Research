# Pattern mining on the daily table (18 Oct 2026)

Script `scripts/tests/pattern_mining_daily.py` (the 40 rules, six exits and the survivor criteria are in its header, written before the first run). Raw output `tests/out/pattern_mining_daily.txt`, plus `_results.csv` (every rule, exit and split) and `_books.csv`.

## Hypothesis

Short-horizon patterns visible at the daily close (the "reel" top gainer, upper-lock runs, gap-ups on volume with a filing, news-less rises, dips in uptrends, panic days, 252-day highs and so on) leave an edge of days to weeks that survives about 0.5% to 1.0% round-trip costs, and could compound a Rs50,000 book over 30 sessions.

## Data

`data/daily_table.parquet`: 577,794 stock-days, 455 names including 142 delisted, 2017-01-02 to 2026-10-16. Features are as of the close of t, entry is the open of t+1, forward paths come from the table (checked: my 20-session close path reproduces the table's ret_fwd_2/3/5/10/20 to 0.00000). 526,391 rows have a trade on t+1. I dropped 19,448 whose entry session opens at the limit up (cannot be bought) and 1,342 with a data break (a later |ret_1d| above 35%) in the next 20 sessions. Costs: 0.5% round trip, plus 0.5% under Rs20m median traded value. CGT is not in the numbers.

## Method

40 rules (R1 to R22 with variants), 6 exits each: sell at the next close, +5% or 3 sessions, +10% or 5 sessions, first upper lock else 5 sessions, first red day else 20 sessions, 20% trailing stop else 20 sessions. That is 240 tests, plus an exploratory "sell at the following open" for R1 and R2. Universe: names above Rs5m for the ranked rules (R1, R2, R10, R11, R12, R16), above Rs1m for the rest ("under Rs5m" below means Rs1m to 5m). In-sample is signal date to 2026-08-31, out of sample 2026-09-01 to 2026-10-16.

Placebo: each signal replaced by a random name on the same date and liquidity tier, same exit, same costs. "Excess" is the mean net minus the exact expected placebo mean. The p-value is from 400 placebo draws on the first signal of each episode (a symbol's signals within 10 sessions merged), one-sided. Survivor screen: S1 at least 100 IS episodes, IS mean net above 0, excess above 0, p at most 0.01; S2 the same sign in both regimes; S3 in both halves (to 2021, 2022 on); S4 out-of-sample n at least 10 with mean net and excess above 0.

Book: Rs50,000, fully reinvested, up to 3 positions, signals taken in order of vol_ratio_1_20, every rolling 30-session window from 2017-01-02 (2,397 windows), open positions marked at the window end. The placebo book fills free slots with random names above Rs5m each session, same exit and costs, 5 seeds.

## Results

**1. The headline: nothing beats costs at the next close.** Across the 40 rules, the in-sample mean net return with a sell at the next close is negative for 37, and the cross-rule average is -1.02%. Gross, the rules are near zero (R1a gross -0.49%, R5a -0.05%, R22 +0.33%). The cost drag alone is 0.5% to 1.0%.

Selected rules, exit "next close" (IS, net of costs; share above +50% is 0.0% for all but a handful):

| Rule | n | episodes | mean | median | win | >+10% | worst | excess vs placebo | p | OOS n / mean |
|---|---|---|---|---|---|---|---|---|---|---|
| R1a top gainer (reel) | 2,221 | 1,595 | -1.24% | -1.32% | 36.0% | 0.4% | -17.7% | -0.26% | 1.00 | 33 / -0.51% |
| R2a top 3 gainers | 6,761 | 3,754 | -1.12% | -1.17% | 35.8% | 0.3% | -17.7% | -0.18% | 1.00 | 95 / -1.76% |
| R3a first lock after base | 1,533 | 1,533 | -1.30% | -1.44% | 34.1% | 0.3% | -12.7% | -0.26% | 1.00 | 20 / -4.44% |
| R4 two locks in 3 sessions | 3,439 | 1,850 | -1.28% | -0.85% | 41.4% | 0.4% | -18.7% | -0.32% | 1.00 | 51 / -1.64% |
| R5a 3 up days | 15,307 | 10,069 | -0.83% | -1.00% | 32.4% | 0.2% | -17.8% | +0.03% | 0.017 | 237 / -1.12% |
| R6a gap-up, results filing | 223 | 220 | -1.75% | -1.96% | 27.4% | 0.0% | -14.9% | -0.60% | 1.00 | 3 / -3.17% |
| R7 gap-up, no filing | 2,952 | 2,296 | -1.63% | -1.86% | 30.9% | 0.5% | -18.5% | -0.54% | 1.00 | 48 / -1.80% |
| R8a +5% day with results | 524 | 499 | -1.27% | -1.56% | 34.5% | 0.4% | -14.9% | -0.26% | 0.98 | 14 / -3.58% |
| R9 dip in uptrend | 2,564 | 2,240 | -0.81% | -1.00% | 36.4% | 1.0% | -15.4% | +0.04% | 0.15 | 44 / -0.47% |
| R11a index -3%, fell most | 117 | 108 | +1.08% | +0.83% | 60.7% | 3.4% | -12.5% | +1.10% | 0.005 | 0 |
| R13a news-less rise | 4,363 | 1,832 | -1.36% | -1.67% | 31.9% | 0.6% | -16.0% | -0.27% | 1.00 | 66 / -1.78% |
| R17a 252-day high | 8,871 | 1,771 | -0.85% | -1.00% | 35.9% | 0.3% | -18.6% | +0.07% | 0.002 | 47 / -2.16% |
| R22 3-day fall of 10% | 6,506 | 2,902 | -0.46% | -0.69% | 42.1% | 1.6% | -17.7% | +0.18% | 0.002 | 177 / -0.27% |

The reel (R1a) loses at every exit: the top gainer is worse than a random same-day, same-tier name by 0.26% at the next close. Selling at the following open (exploratory) is -0.67% net, +0.05% over placebo (p 0.09, n 2,220); out of sample it is +0.77% on 32 trades, which is too few to count. It is a not-quite-losing rule before CGT, not an edge.

**2. The trailing stop turns the average positive, but through the exit, not the signal.** With the 20% trail the cross-rule mean is +1.24% and 31 of 40 rules are positive, yet the placebo with the same exit makes about +0.5% to +1.0% too (R17a placebo +0.69%). Medians are negative for most rules (R4: mean +2.06%, median -3.30%, 25% of trades above +10%, 3.9% above +50%). It is a lottery profile on a drifting market.

**3. Multiple testing.** Of 240 tests, 18 have p at most 0.01 (chance alone gives 2.4) and 18 pass Benjamini-Hochberg at 10%. At the rule level 7 of 40 rules have one exit at p at most 0.01 (expected by chance about 2.3 if exits were independent, 0.4 if perfectly correlated). So there is more than chance in the tail, but 107 of 240 tests are worse than random entries at p at least 0.99: chasing strength costs money. Note p-values on the mean are driven by large n of correlated episodes; treat them as upper bounds on significance.

**4. Survivor screen.**

| Rule / exit | IS ep | IS mean / median | excess | p | regimes (bill>policy / bill<=policy) | halves | OOS |
|---|---|---|---|---|---|---|---|
| R11a / next close | 108 | +1.08% / +0.83% | +1.10% | 0.005 | +0.77% / +1.48% | +1.09% / +1.08% | n 0 (index -3% days did not occur) |
| R17a 252-day high / trail20 | 1,771 | +1.94% / -0.81% | +1.28% | 0.002 | +0.30% / +3.41% | +0.13% / +2.92% | 27 / -15.42% (excess -7.73%) |
| R17b same + volume 2x / trail20 | 1,621 | +1.84% / -1.15% | +0.89% | 0.002 | +0.43% / +2.99% | +0.68% / +2.40% | 12 / -12.98% (excess -5.87%) |
| R4 two locks / trail20 | 1,850 | +2.06% / -3.30% | +1.59% | 0.002 | +0.79% / +6.69% | -0.18% / +7.40% | 32 / -13.87% |
| R4 two locks / red20 | 1,850 | +0.77% / -2.45% | +1.38% | 0.002 | -0.08% / +3.86% | -0.28% / +3.27% | 21 / -18.57% |
| R17a / red20 | 1,771 | +0.12% / -1.56% | +0.61% | 0.002 | -0.11% / +0.33% | -0.13% / +0.26% | 25 / -20.17% |

Six pass S1; R11a/close1, R17a/trail20 and R17b/trail20 also pass S2 and S3; none passes S4. **Survivors: none.** R17a and R17b (the trend rule at daily resolution, with a 20% trail) held in both regimes and both halves, then lost 13% to 15% per trade out of sample on 27 and 12 trades in a falling September to October (excess against placebo also negative). R11a has the cleanest in-sample record (60.7% win, both regimes, both halves, KMI members +0.99%) but it rests on 39 market-down days and cannot be tested out of sample; under the trail exit its excess is +3.3% (p 0.04), also with no out-of-sample trades. Treat it as a hypothesis, not an edge: 39 dates is one market-crash story told 39 times.

**5. Robustness.** Tier splits for R17a/trail20: above Rs20m +2.38%, Rs5-20m +1.44%, Rs1-5m +1.42%; KMI members +2.16%. For R11a, above Rs20m +1.80%, Rs5-20m +0.32%. Regime splits favour bill<=policy for the lock and breakout rules (R4 +6.69% against +0.79%), so the rule's edge, where it exists, lives in the easing regime. Early versions of this run contained four names (PHDL, BECO, BNL, STL) with a 99% drop inside 20 sessions from unadjusted corporate actions; I added the 35% forward-break filter after seeing worst cases of -100%, before looking at any book. That cleaning changed R17a/trail20 mean from +1.83% to +1.94% and no survivor decision.

## Books (Rs50,000, 30-session windows)

Placebo books (random liquid names, same exit): next close p10 0.67, median 0.76, p90 0.86, 0.7% of windows up; trail20 p10 0.84, median 0.98, p90 1.16, 43.5% up, worst 0.54. Specific windows: 14 Aug to 15 Sep, placebo 0.72 (close) to 0.88 (trail); 16 Sep to 16 Oct, 0.78 to 0.97.

Real books (192 that hold something in at least 90% of windows; multiples of Rs50,000):

| Book | p10 | median | p90 | share up | worst | mean | 14Aug-15Sep | 16Sep-16Oct |
|---|---|---|---|---|---|---|---|---|
| R1a reel / next close | 0.53 | 0.69 | 0.88 | 2.8% | 0.29 | 0.70 | 0.60 | 1.10 |
| R5a 3 up days / next close | 0.64 | 0.77 | 0.91 | 1.2% | 0.51 | 0.77 | 0.70 | 0.79 |
| R17a / trail20 | 0.85 | 1.00 | 1.24 | 48.9% | 0.60 | 1.03 | 1.00 | 0.90 |
| R17b / trail20 | 0.84 | 1.00 | 1.23 | 47.9% | 0.55 | 1.03 | 0.98 | 1.00 |
| R4 / trail20 | 0.75 | 0.96 | 1.41 | 44.0% | 0.49 | 1.05 | 0.75 | 0.79 |
| R1a / trail20 | 0.74 | 0.95 | 1.31 | 40.6% | 0.48 | 1.02 | 0.62 | 1.05 |
| R11a / next close (active in 30% of windows) | 1.00 | 1.00 | 1.03 | 21.3% | 0.91 | 1.005 | 1.00 | 1.00 |

Across the 192 always-on books, the median book multiple beats the matched placebo book in 37% of cases; only 2 have a median at or above 1.00; the median book at next close is 0.80 and at trail20 0.96. The multiples in the two named windows: 22 of 192 books were up in 14 Aug to 15 Sep and 47 of 192 in 16 Sep to 16 Oct (median 0.84 and 0.89). **The best achievable 30-day distribution from these rules** was about what the placebo trail book gives with a slightly better tail: p10 0.85, median 1.00, p90 1.24, 49% of windows up, worst 0.60 (R17a/trail20), against a placebo of 0.84 / 0.98 / 1.16 / 43.5% / 0.54. That is a lottery ticket with no cash cushion, not a method for a Rs50,000 book.

## Verdict

No rule has a short-horizon edge after costs that held out of sample and across regimes. At the next close every rule is negative after costs, because the signals carry roughly zero gross return against 0.5% to 1.0% of costs. Chasing the day's winners (R1, R2, R3, R4, R5, R19) is worse than random entries on the same date. Only two things stand out in sample: panic-day buying of the biggest fallers (R11a, 39 dates, no out-of-sample test) and 252-day-high or double-lock entries held with a 20% trail (positive mean, negative median, reversed hard in Sep to Oct 2026). The 30-day book is not a plausible compounding engine: in the best case it matches the matched random book plus a thicker right tail, with roughly half of all 30-session windows losing money and a worst window of -40% to -50%.

## Caveats

- Targets are booked at the target when the table's high touches it (a limit order), and the exit session is taken at the latest possible (3 or 5) for capital release; the trail is on closes. Entry is assumed filled at the open if it did not open at the limit; no queue or spread model. Rs1-5m names carry only the extra 0.5%, which is probably too little.
- Delisted names are held at the last print after their last trade; delisting losses beyond that are not captured (flatters the trail results slightly).
- Sector peers are a hindsight basket (today's sector lists); R12 and R13a use them.
- Interpretation choices: "above its 20-session high by less than 5%" read as the prior close within 5% of its 20-session close high; "reaction day" of R15 is the session the filing is assigned to; R16 buys the 3 most liquid names as an index proxy (the KMI index cannot be traded); R10, R11 and R16 have 22 to 40 dates each, so their numbers are one episode told many times.
- Out-of-sample is 33 sessions in a falling market, so S4 is a weak check; with n below 10 it is untestable, not a pass.
- p-values treat first signals of episodes as independent, ignoring cross-sectional correlation beyond the date match; the 400-draw floor is p of about 0.002.
- Frozen brokerage and slippage inputs are from `data/costs.md` and marked unverified there (Finqalab rate, spreads).
