# Noise map and shock-rebound playbook

Run 18 Oct 2026. Script `scripts/tests/noise_map_shock_rebound.py` (events in `scripts/tests/noise_map_events.psv`), output `tests/out/noise_map_shock_rebound.txt` (full 157-row event table, leaders, flows), data `data/events_shocks.csv` and `data/events_shocks_metrics.csv`.

## Question

Which event types does PSX ignore, which does it reprice, and what does a shock and rebound look like, so that "what to disregard" and "when to buy the crash" are measured rather than felt.

## Data and method

- **Events:** 157 from 18 Oct 2016 to 16 Oct 2026. Counts: SBP rate changes 34, geopolitical 27, political 20, IMF 19, rating actions 19, rupee 13, budget 12, external policy (FATF, US sanctions, tariffs) 6, Covid 4, MSCI 3. Date status: 59 from repo files, 31 web-checked in this run, 67 recalled and not re-verified (`status` column).
- **Day 1** is the first session that can price the news (same day if before the 15:30 close, else next session; weekends roll to Monday). Base is the previous close. Fall and bottom are the lowest KSE100 total-return close in the first 20 sessions. Rebounds are measured from that bottom. "Regained" means a close at or above the pre-event close within 60 sessions of the bottom.
- **First public time** is filled where known; for SBP, IMF, rating and budget releases it was not collected and they are treated as after the close (an assumption).
- **Placebo:** every session as day 1 (2,460 sessions), and 2,000 draws of the same number of random dates for each type. Verdict rule fixed before the run: a type REPRICES if its median day-1 move or median 20-session return lies outside the 5th to 95th percentile of random-date medians.
- **Panel results:** `prices.py` adjusted returns, names above Rs5m 60-day median traded value, survivors only (rebounds flattered).

## The shocks (fall of 5% or more within 20 sessions)

49 events qualified; 25 remain after keeping the first event of any cluster (the rest fall inside the same 20 sessions). Selecting by the realised fall is hindsight: this describes the pattern, it is not a trade test. Ten of the 25 are shown.

| first event | fall | bottom | reb20 | reb60 | breadth up (20s) |
|---|---|---|---|---|---|
| Covid first case, 26 Feb 2020 | -29.9% | 25 Mar 2020 | +19.2% | +25.0% | 100% |
| Pahalgam, 22 Apr 2025 (Sindoor 7 May) | -12.6% | 8 May 2025 | +17.9% | +38.2% | 99% |
| Israel strikes Iran, 13 Jun 2025 | -6.4% | 23 Jun 2025 | +19.0% | +34.4% | 99% |
| Afghan war 27 Feb 2026, Iran war 2 Mar | -13.3% | 9 Mar 2026 | +13.2% | +16.3% | 95% |
| Article 370, 5 Aug 2019 (with SBP +100bp) | -12.8% | 16 Aug 2019 | +10.9% | +27.8% | 93% |
| Pakistan strikes Iran, 18 Jan 2024 | -5.8% | 16 Feb 2024 | +8.3% | +25.8% | 83% |
| US-Iran truce collapses, 8 Jul 2026 | -8.2% | 24 Jul 2026 | +3.5% | n/a | 60% |
| Munir named, 24 Nov 2022 | -8.3% | 21 Dec 2022 | -1.4% | +6.4% | 19% |
| Rupee +1.9%, 17 Jun 2019 | -5.3% | 12 Jul 2019 | -12.6% | +1.5% | 0% |
| SBP +50bp, 29 Mar 2019 | -5.8% | 23 Apr 2019 | -4.9% | -11.0% | 18% |

Across the 25: day 1 median -0.5% (the fall is rarely a one-day event); max fall median -8.2%; sessions to the bottom median 17 (range 3 to 20); rebound from the bottom median +1.9% at 5 sessions, +3.2% at 10, +5.6% at 20 (range -12.6% to +19.2%), +6.6% at 60 (mean +11.1%, range -11.0% to +38.2%); the pre-event close was regained within 60 sessions of the bottom in 14 of 23 (median 17 sessions). Breadth: 95% of liquid names were down at the bottom and 78% were up in the next 20 sessions (medians). Where breadth was 20% or less there was no rebound (2019 rupee and rate hikes, Dec 2022).

## Per-type noise map

| type | n | med day 1 | med max fall | med sessions to bottom | med 20s from base | med reb20 | med reb60 | share with 5%+ fall | verdict |
|---|---|---|---|---|---|---|---|---|---|
| geopolitical | 27 | -1.0% | -4.3% | 7 | -1.3% | +7.2% | +20.7% | 37% | REPRICES |
| Covid | 4 | -5.6% | -26.1% | 8 | -14.7% | +19.2% | +25.0% | 100% | REPRICES |
| SBP | 34 | -0.2% | -2.7% | 7 | +0.0% | +7.0% | +6.5% | 32% | ignored |
| political | 20 | +0.0% | -2.8% | 8.5 | +0.3% | +2.7% | +0.8% | 30% | ignored |
| IMF | 19 | -0.2% | -3.4% | 5.5 | +3.8% | +6.6% | +9.4% | 21% | ignored |
| rating | 19 | -0.2% | -2.0% | 6 | +1.2% | +4.0% | +3.7% | 16% | ignored |
| rupee | 13 | +0.0% | -3.3% | 6 | +2.6% | +5.9% | +2.6% | 23% | ignored |
| budget | 12 | +0.3% | -3.0% | 11 | +0.1% | +3.6% | +2.3% | 25% | ignored |
| external policy | 6 | -0.1% | -3.4% | 3 | +3.2% | +7.1% | +4.5% | 33% | ignored |
| MSCI | 3 | -0.7% | -5.4% | 16 | -4.4% | +3.6% | -0.2% | 100% | ignored (n too small) |
| random sessions | 2,460 | +0.1% | -2.3% | 8 | +1.1% | +5.0% | +6.5% | 24% | |

The placebo band for median day 1 is roughly -0.3% to +0.5% for n of 20 to 34. Reading it:

- **Reprices on the day:** geopolitical (a third of the 27 had a day-1 move of -2% or worse, against 4% of random days) and Covid. Middle East events: median day 1 -2.0%, median rebound +11.5% at 20 and +22.9% at 60 sessions, regained in 5 of 5. India-Pakistan: day 1 -1.0%, rebound +5.8% and +24.2%. Ceasefires are the positive twin: +9.4% (10 May 2025) and +5.2% (24 Jun 2025).
- **Ignored on the day:** SBP hikes (median 0.0%), budgets, rating actions in both directions (downgrade -0.3%, upgrade +0.1%), rupee devaluations (0.0% on the day, including moves above 5% such as Jan 2023), political events (0.0%), IMF staff-level agreements (+0.6%) and board approvals (-0.5%). SBP hikes did grind lower (median max fall -3.7%, bottom 16 sessions later).
- **Drift, not reaction:** SBP cuts had a median day 1 of -0.5% but +10.1% at 20 sessions after the bottom and +23.0% at 60 (the 2020 and 2024 cut cycles). Cuts and IMF boards "reprice" on the 20-session test only because they sit inside bull legs.
- **Political:** 6 of 20 events had a 5%+ fall within 20 sessions (Panama July 2017, Munir and the rate hike Nov 2022, Imran conviction Aug 2023, election Feb 2024); the Imran arrest of 9 May 2023 cost only 1.1% on the day (and the index was +16.4% 60 sessions after its bottom), and the vote that ousted him on 10 Apr 2022 coincided with a +3.8% day, while the preceding dissolution day was -2.8%. The Feb 2024 election fell 6.7% from base and recovered 25.8% in 60 sessions.
- **Not explained:** 8 sessions with falls of 3.5% or more lie outside every event (12 and 20 Jun and 3 Jul 2017, 2 Dec 2021, 24 Jun 2022, 19 and 26 Dec 2023, 19 Feb 2026).

## Who sold and who bought (NCCPL, USD mn, 25 clustered shocks since 2017)

| investor | fall: median | net buyer in fall | rebound: median | net buyer in rebound |
|---|---|---|---|---|
| mutual funds | -25.6 | 0/25 | -4.3 | 10/25 |
| foreign corporates | -23.5 | 7/25 | -20.0 | 6/25 |
| banks / DFI | +11.3 | 20/25 | +0.7 | 14/25 |
| companies | +9.4 | 20/25 | +3.1 | 15/25 |
| individuals | +7.9 | 20/25 | +13.9 | 20/25 |
| insurers | +5.8 | 18/25 | +6.2 | 18/25 |

Fall = day 1 to the bottom; rebound = the 20 sessions after it. Mutual funds and foreign corporates sell the fall (totals -787 and -655); foreigners keep selling through the rebound (-563). Banks/DFI, companies, individuals and insurers buy the fall; individuals and insurers keep buying the rebound (+304 and +258) while banks take profit (-191). The bottoms are bought by domestic non-fund money from funds and foreigners.

## Leaders of the rebound

Names most often in the top 10 liquid names by 20-session return from the bottom (of 25 shocks): ATRL 8, NRL 7, GAL 6, TRG 6, LOTCHEM 6, PIAHCLA 5, FEROZ 5. Sector baskets by median 20-session rebound: oil refineries +11.2% (above the median sector in 72% of shocks), food +9.3%, textiles +8.9%, steel +7.2%; weakest Islamic banks +4.7% and power +5.1%. Leaders repeat only weakly: one shock top 3 appears in the next shock top 10 on average 0.38 times of 3, against 0.26 by chance.

## Rebound playbook: buying the crash

Entries on the KSE100 total-return index, clustered shocks, return from the entry close.

| entry (hindsight-selected 5%+ shocks, n=25) | 20s median | win | 60s median | win | median worst drawdown in 60 |
|---|---|---|---|---|---|
| (a) day-1 close | -4.4% | 12% | -4.2% | 38% | -9.7% |
| (b) day-3 close | -3.9% | 16% | -2.4% | 46% | -8.7% |
| (d) first up-day after day 1 | -4.4% | 24% | -2.0% | 46% | -8.9% |
| (c) first up-day after the bottom (needs hindsight) | +3.1% | 76% | +4.7% | 70% | -2.3% |

These rows are biased downward: choosing events because a 5% fall followed puts the entry before the fall. They show only that buying every shock blindly would have cost money. The clean test sets the trigger at entry:

| trigger known at entry | trades | 20s median | win | worst 20s | 60s median | win | worst 60s | worst drawdown in 60 |
|---|---|---|---|---|---|---|---|---|
| index 5%+ below pre-event close | 9 | +4.2% | 78% | -7.7% | +3.5% | 67% | -14.0% | -19.2% (Mar 2020) |
| index 3%+ below pre-event close | 20 | +3.7% | 70% | -10.9% | +0.7% | 50% | -18.3% | -24.3% |
| placebo: any random close | 2,400 | +1.1% | 57% | -29.9% | +2.2% | 59% | -34.0% | |
| placebo: after a 3-day 5%+ fall | 14 | +5.3% | 79% | | +7.0% | 79% | -15.5% | |

Buying a market already 5% below its pre-event close earned +4.2% at 20 sessions with a 78% win rate, against +1.1% and 57% for a random close. The direction is right and the sample is small, and it is not distinguishable from buying after any sharp 3-day drop. At 60 sessions it fades to +0.7% median for the 3% trigger.

Sector choice adds nothing at tradable entries. The three sectors that had fallen least by the entry date lost to the index by 1.5% (day 1) and 0.2% (day 3) and tied on the first up-day, beating it 40%, 48% and 56% of the time. Even the hindsight top-breadth sectors only tie the index at those entries (-0.6%, -0.2%, +0.6%); they win clearly only if the bottom is already known (+12.4% at 20 sessions against +3.1% for the index).

By regime (T-bill 6M minus policy rate; the 0.5-point band is a placeholder): of the 25 clustered shocks 3 were hike-expected, 19 neutral, 3 cut-expected. Across all 49 events, hike-expected shocks (n=7) rebounded +10.9% at 20 and +32.9% at 60 sessions; neutral (33) +5.6% and +4.3%; cut-expected (9) +9.0% and +9.3%. Day-1 entries in neutral shocks lost over 60 sessions (median -6.6%, win 22%). Cells are too small to act on.

## Verdict

1. PSX reprices geopolitical shocks on the day and then gives them back. Of 10 geopolitical events with a 5%+ fall, the median fall was -9.0%, the 20-session rebound +13.2% and the 60-session rebound +27.8%; the pre-event close was regained in all 9 with a full window. The rebound was strongest when the shock was bounded (Sindoor then ceasefire, Iran-Israel then ceasefire). Balakot and Abhinandan in 2019 never fell more than 4.5%: the market largely ignored them.
2. The market ignores the day-1 headline of rate decisions, budgets, rating changes, rupee devaluations, IMF agreements and most domestic politics. Their effects arrive as drift over weeks. "Disregard the headline" is supported on day 1; "nothing follows" is not.
3. Buy the crash only on a trigger known at the time (the index 5%+ below its pre-event close), expecting about +4% over 20 sessions and roughly a 1-in-5 chance of a loss, with 60-session outcomes from -14% to +38% and a worst drawdown of -19% (Mar 2020). Buying the first session of a shock before the fall is known lost money in this sample.
4. Domestic non-fund money (banks, companies, individuals, insurers) buys the bottoms; mutual funds and foreigners sell them.

## Caveats

- 67 of 157 dates are recalled, not re-verified. The 2026 rating entries (S&P 22 Jul, Moodys 24 Aug) come from an aggregator table (fxempire), not the agencies.
- Only one SBP decision was verified as a surprise (15 Dec 2025, all 12 analysts in a Reuters poll expected a hold). Consensus was not collected for the other 33, so "every surprise decision" is not done; the three off-cycle cuts are recalled.
- Events overlap (Mar 2020, Apr to Jun 2025, Feb to Mar 2026), so type statistics are not independent; Covid is one episode counted four times.
- 2024 to 2026 was a bull run and flatters rebounds; the 60-session rebound after Soleimani (Jan 2020) is contaminated by Covid.
- The panel holds only survivors, so name and sector results are biased upward. Sector baskets are the static lists in `sector_momentum.py`. In the early years the liquidity screen leaves about 70 names.
- A 20-session fall mixes the event with whatever else happened; a type-level fall is not proof the event caused it. Not tested: pre-event drift (whether IMF and rating news was priced before the date).
