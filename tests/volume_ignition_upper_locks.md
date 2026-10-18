# Volume ignition with upper locks (the SSGC 2024 call)

Run 18 Oct 2026. Script `scripts/tests/volume_ignition_upper_locks.py`. Raw output `tests/out/volume_ignition_upper_locks.txt` (all 40 rows per universe, splits, winner and loser lists); literal +10% run `..._strict10.txt`; episodes `..._trades.csv`.

## Hypothesis

Joining a stock once heavy volume and upper-lock closes show a rise is under way, then leaving on a 20% trailing stop, pays after costs and beats entering random names with the same exit. His case is SSGC in 2024 (about +120%).

## Data

Survivor panel (456 names, total-return adjusted) plus 284 delisted names (crude returns), 17 Oct 2016 to 16 Oct 2026. Volume is in share-equivalents, so a bonus cannot fake an ignition. Liquidity is the 60-session median traded value at signal, above Rs5m ("liq5") or Rs1m ("liq1", the small-cap tail). Regime is the 6M T-bill minus the policy rate at fill. KMI flag is the 5 Jun 2026 list (hindsight).

## Method

Pre-registered entries, unchanged: V1 20-session mean volume at least 3x the prior 120-session mean and at least 2 upper-lock closes in the last 5 sessions. V2 the same with 3 locks in 10. V3 volume 3x with a 20-session return above +25%, no lock needed. V4 the first upper lock after 60 sessions with no lock, with the prior 20-session close range under 15% (my reading of "60-session base").

Exits, each run separately: close at or below 80% of the highest close since entry ("trail20"); time stops of 20, 60 and 120 sessions; first lower-lock close. Signal at close t, fill at the next close that is not a lock day (within 10 sessions, else dropped), same rule for exits. Cost 0.5% round trip, plus 0.5% under Rs20m median traded value. A name re-arms after 60 sessions with the condition false. Unmatured time-stop trades are excluded. Placebo: 50,000 random liquid (name, day) entries per universe, same fill, exits and costs, resampled in the signals' fill-quarter mix, 1,000 draws; p(med) and p(mean) are the share of draws at or above the real median or mean (near 1 = worse than random). Sleeve: Rs50k, equal thirds of equity, up to 3 positions, every signal taken in date order.

Three data findings changed the method. (1) The daily limit was 5% until Mar 2020, 7.5% until 5 Jul 2024 and 10% since 8 Jul 2024, so a literal +10% lock exists only from July 2024. The main run uses the limit in force; the literal version is the sensitivity run. (2) Stocks under Rs20 trade a wider band, so for them a lock is any close at or above the limit move (cap +30%). (3) 1,479 one-day drops beyond the limit were treated as unadjusted splits or capital reductions (KML's 10:1 split, PHDL) and zeroed; signals with such a break in the 140 sessions before fill or during the hold are dropped, about 10% of signals, which also drops some real winners (SYS in 2019).

## Results

Signals (liq1): V1 529, V2 483, V3 860, V4 823, from 230 to 307 names across 38 to 39 calendar quarters. About 90% are tradable. Fill is not the problem: the median move from signal close to fill close is -0.1% to +1.0%.

Net returns, %. Placebo = random entries, same stop or time exit. n in brackets is calendar quarters.

| Universe, exit, variant | n (qtrs) | Mean | Median | Win % | >+50% | <-30% | Worst | Placebo median / mean | Sleeve x / max DD |
|---|---|---|---|---|---|---|---|---|---|
| liq5 trail20 V1 | 248 (36) | 0.0 | -13.0 | 27 | 7.7 | 1.6 | -46 | -6.9 / +9.8 | 1.16x / -59% |
| liq5 trail20 V2 | 215 (32) | -2.9 | -14.2 | 28 | 6.5 | 2.3 | -46 | -7.0 / +8.9 | 0.53x / -77% |
| liq5 trail20 V3 | 471 (33) | +1.2 | -11.7 | 32 | 7.4 | 0.6 | -46 | -5.0 / +13.9 | 0.58x / -61% |
| liq5 trail20 V4 | 440 (37) | +9.4 | -9.6 | 35 | 11.6 | 0.9 | -32 | -8.3 / +13.9 | 1.45x / -71% |
| liq5 T60 V1 | 237 (35) | +4.2 | -10.3 | 38 | 10.5 | 13.5 | -71 | +1.0 / +6.0 | 1.89x / -55% |
| liq5 T60 V2 | 208 (32) | +2.3 | -11.0 | 39 | 10.6 | 13.9 | -71 | +0.3 / +5.3 | 1.67x / -69% |
| liq5 T60 V3 | 465 (33) | +2.3 | -7.1 | 42 | 7.5 | 8.2 | -71 | +1.5 / +7.4 | 1.85x / -59% |
| liq5 T60 V4 | 445 (37) | +1.3 | -2.3 | 44 | 4.0 | 4.5 | -60 | -0.8 / +4.2 | 0.44x / -76% |
| liq1 trail20 V1 | 456 (38) | +2.8 | -10.9 | 30 | 9.2 | 2.0 | -43 | -6.2 / +11.4 | 0.30x / -78% |
| liq1 trail20 V2 | 413 (38) | +0.6 | -12.8 | 31 | 9.0 | 2.7 | -43 | -7.2 / +9.6 | 1.04x / -65% |
| liq1 trail20 V3 | 748 (37) | +5.1 | -10.5 | 34 | 8.7 | 1.5 | -43 | -4.5 / +15.6 | 0.61x / -77% |
| liq1 trail20 V4 | 738 (38) | +12.9 | -9.1 | 36 | 12.3 | 0.7 | -32 | -7.3 / +16.0 | 0.74x / -81% |
| liq1 T60 V1 | 446 (37) | +4.8 | -6.8 | 39 | 8.5 | 11.4 | -71 | +1.0 / +6.4 | 1.03x / -76% |
| liq1 T60 V2 | 406 (37) | +4.4 | -8.7 | 41 | 9.1 | 12.3 | -71 | +0.0 / +5.4 | 0.51x / -76% |
| liq1 T60 V3 | 736 (37) | +4.2 | -5.2 | 43 | 7.3 | 7.3 | -71 | +2.0 / +7.9 | 0.85x / -79% |
| liq1 T60 V4 | 734 (38) | +2.4 | -1.7 | 46 | 4.6 | 4.8 | -60 | -0.5 / +4.7 | 0.89x / -78% |

Reading the table:

- The signal median is below the placebo median for V1, V2 and V3 in every one of the 10 universe-by-exit cells, with p(med) between 0.996 and 1.000 and p(mean) from 0.75 to 1.000. Buying after volume and locks is worse than buying a random liquid name on a random day, by about 5 to 7 points at the median under a stop and 7 to 11 points at 60 sessions.
- Random entries with a 20% trail made a mean of +9% to +16%. That reflects the 2023 to 2025 bull market, survivors and total-return prices; the stop is doing the work and the ignition entry adds nothing to it.
- V4 is indistinguishable from random: p(med) 0.89 to 0.98 under the stop, 0.55 to 0.77 at 20 sessions.
- The other exits (raw file): T20 medians -1% to -7%, means -2.4% to +1.2%. T120 is no better than T60 and has 19% to 27% of V1 and V2 trades below -30%. The first-lower-lock exit leaves 6% to 12% of trades open at the end of data, and V4's mean of +16% to +19% under it comes from those open winners (median -5% to -6%), so it is not an exit.
- The stop cuts the tail. Below -30%: 1.6% to 2.7% of V1 and V2 trades under trail20 against 11% to 14% at 60 sessions and 19% to 27% at 120 sessions. Random entries at 60 sessions fall below -30% 4.9% to 5.3% of the time, so V1 and V2 entries without a stop have two to three times the crash share (11% to 14%).
- Sleeve results (0.09x to 3.53x across the 40 cells, drawdowns -44% to -96%) are one path each, with 130 to 690 signals skipped for lack of a free slot: instability, not skill.

## Robustness

By fill year, liq1 trail20 (median, mean): V1 is negative at the median in every year (-8% to -20%); the mean is positive only in 2020 (+2), 2021 (+4), 2023 (+17), 2024 (+15) and 2025 (+5). V4 is -15% to -22% at the median in 2017, 2018, 2019, 2021 and 2022, then +17% (mean +60, 65% win, n 116) in 2023 and +8% (mean +41, n 134) in 2024, then -9% and -7% in 2025 and 2026. V4's mean is a two-year rally.

By regime (liq1 trail20, 6M T-bill below or at the policy rate against above): V1 median -8 / mean +10 / win 36% (n 174) against -13 / -2 / 27% (n 282). V4 -3 / +27 / 48% (n 279) against -12 / +4 / 29% (n 459). Signals do less badly in the easing regime, but the median is negative in both. Cluster check by fill quarter: mean of quarter means -2.5 (V1), +7.6 (V4); positive quarters 37% to 49%.

KMI (liq5 trail20): V1 KMI median -10.7, mean +3.4 against non-KMI -15.8 / -6.8; V4 KMI -9.7 / +9.9. The KMI list does not rescue the signal.

Literal +10% locks (strict run): V1 and V2 exist only from July 2024. V1 liq5 trail20 n 129, mean +3.4, median -11.7, win 29%, p(med) 1.000; V4 liq1 trail20 n 377, mean +5.9, median -6.6, p(med) 0.97. Same conclusion.

## SSGC and the pump question

SSGC fired three variants in the 2024 run: V4 on 23 Oct (first lock after a base; filled 25 Oct), V1 on 25 Oct (filled 28 Oct), V2 on 1 Nov (filled 6 Nov). Under trail20 all three exited 8 Jan 2025: +247%, +224% and +144% net. The stock had 15 upper-lock closes between 23 Oct and 11 Dec 2024. His +120% sits below that range, so the instinct was right on that name, and the stop would have held it. The same stock also fired four losers: V1 Nov 2023 -10%, V3 Dec 2023 -15%, V4 Nov 2025 -15%, V3 May 2026 -11%.

Round trips within 60 sessions of the fill: V1 16% closed at or below the pre-run price (V2 12% to 14%, V3 8% to 9%), and 10% to 13% for V1 and V2 fell 30% or more from the fill price (random 5%). A tighter pump test (rose 20% after fill, then gave back the whole run) gives only 0% to 2%, because the stop exits first.

Largest winners (liq1, any variant, trail20, 1,395 episodes, mean +8.1%, median -10.0%, win 34%), by signal date: THCCL 25 Sep 2023 +1,348% and 9 Apr 2024 +793%; MEBL 3 Jul 2023 +700% (open); FATIMA Dec 2023 +379%; LUCK May 2023 +364%; PNSC Sep 2023 +351%; GLAXO Feb 2024 +338%; SSGC Oct 2024 +247%. Most of the top 30 are V4 signals from the 2023 and 2024 rally (UBL, BAHL, MEBL, LUCK, FCCL), which is market beta, not ignition. Largest losers are small names stopped out in 8 to 24 sessions at -28% to -43% (QTECH Oct 2017 -43%, QTECH Jan 2024 -36%, CSIL Jan 2026 -35%, JSML Apr 2026 -35%). The top 5 winners hold 14% of all positive net returns; the mean without them is +5.5%.

## Verdict

- V1 and V2 (volume and locks): nothing. Median trade -11% to -14% under a stop, win rate 27% to 31%, worse than random entry in every cell. The only winning exit was the 20% trailing stop, and only because it kept the tail small. Paid only as a lottery ticket (6% to 9% of trades above +50%, while random entries with the same stop give 10% to 12%).
- V3 (volume and a 25% run, no locks): nothing. Same pattern, worse than random everywhere.
- V4 (first lock after a base): watch, not tradable. Net mean +9% to +13% under the stop with a 12% chance of a +50% trade, but the median is -9%, win rate 35%, indistinguishable from random entries with the same stop, and the mean sits in 2023 and 2024. It is a rally beta with a stop attached.
- Has "join a sustained volume-driven rise and leave on the stop" paid? Not as a selection rule. The stop paid; the volume signal did not. For whom: no one buying on the signal alone. The tail it gives: 6% to 12% of trades above +50%, 6 to 7 in 10 trades losing, median loss about -10% per stop-out, worst loss -43% to -46% with the stop and -71% without.

## Caveats

The 2023 to 2025 rally supplies most positive means, and signals cluster in rallies, so 32 to 38 quarters is closer to 3 or 4 regimes. The lock definition is my choice; the literal +10% run agrees on a smaller sample. The 10% of signals dropped for data breaks may include real winners. Delisted names use crude returns and the KMI flag is today's list. The test has no news content (a gas price decision or takeover behind the volume), which an experienced person would read first and which could separate SSGC from the 2017 to 2020 losers.
