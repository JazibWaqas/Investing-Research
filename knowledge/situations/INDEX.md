# Situation library: index

Written 2026-10-18. Twelve dated cases from PSX history, each in its own file, in the format of `tests/refiner_steel_retrospective.md`: dates and regime, what was knowable and when, what the market did, the right move with entry, exit and return, the trap, the situation type, and the questions that would have caught it. These feed step 7 of `knowledge/HOW_TO_THINK.md` section 5 and the exam in step 9.

## The question list used in the files

- Q1 Regime: policy rate against CPI, rate direction, the curve, IMF status, reserves and the rupee, market valuation.
- Q2 Situation type and its base rate (n and median, never a mean alone).
- Q3 Actors and who gains; who is the counterparty.
- Q4 Price: confirmation or extension.
- Q5 Exit, and the loss if wrong.
- Q6 Traps: one-off earnings, standalone versus consolidated, operator float, rights issue, sponsor behaviour, stale multiples.

## Cases

| # | Case | Type | Regime | Knowable date | The move | Lesson |
|---|---|---|---|---|---|---|
| 01 | 2019 bottom and IMF | Regime bottom | Hikes to 13.25%, rupee 158, CPI 10 to 15% | 16 Sep 2019 (first hold) | KSE 31,929 to 43,219 (+35%); the low 28,765 was 6 weeks after Board approval | Buy the second signal (hold, stable rupee), not the IMF headline |
| 02 | March 2020 crash | Shock plus policy backstop | Rate 13.25% cut to 7% in 100 days | 17 to 25 Mar 2020 | Low 27,229, +61% to Dec; first cut was 12% above the low | Cuts precede the low; scale in; pick USD earners |
| 03 | 2021 to 2022 hikes and default scare | Tightening plus external stress | 7% to 15%, CPI 27%, rupee 168 to 240 | Nov 2021 (IMF stalls) | KSE -17% in PKR, -39% in USD; 4 of 95 liquid names up in 21 months | Sit out is a position; need a trigger to return |
| 04 | June 2023 IMF standby | Regime bottom, confirmed trigger | Policy peak 22%, CPI 38% to 29% | 29 Jun to 12 Jul 2023 | KSE 43,899 to 116,169 (+165%); low came 11 days before the Board | Do not wait for the cut or the Board |
| 05 | June 2024 first cut | Policy decision | 22% to 20.5%, CPI 11.7%, real rate +9 | 10 Jun 2024 | KSE +58.6% in 6 months; fertilizer, E&P, pharma led; banks and power lagged | The cut confirms; choose sectors with their own catalyst |
| 06 | May 2025 India conflict | Geopolitical shock and rebound | Rate 11%, CPI near 0, IMF intact | 9 May 2025 (IMF approval, Friday) | -12.6% to 103,527, then +13.3% in two sessions | The rebound was a weekend gap; hold the core, keep cash |
| 07 | 2026 refiners | Catalyst trade | Oil shock, hike to 11.5% | 29 Apr (watch), 8 to 9 Jul (trade) | PRL +155%, NRL +70%, ATRL +34% | Ignored earnings plus spread plus policy plus volume |
| 08 | ASL 2026 | Sponsor accumulation | Same as 07 | 9 Apr 2026 (disclosure) | Rs10.97 to 17.83 peak (+62%), +38% at 16 Oct | Sponsor signal is real but untested; the price moved the day before disclosure |
| 09 | SSGC 2024 | Volume ignition with locks | Cuts from 17.5% to 13% | 23 Oct 2024 (17m shares, 26x base) | Rs9.95 to 49.52 peak; stop exit 39.24 on 7 Jan | The instinct can pay, the regulator fact pre-dated the run, the earnings were hidden |
| 10 | SYS 2025 to 2026 | Failure: derating | Rate bottom 10.5%, then hike, war, strong rupee | 7 Jan 2026 (25x trailing, bill 10%) | SYS -31% while trailing EPS +18%; NETSOL's low P/E did not help | The story was true; the multiple was the risk |
| 11 | EPCL takeover | Deal, in progress | Rate 11.5%, hike risk 26 Oct | 10 Mar 2026 (PAI), 1 Sep (Rs38.60) | Rs31.77 on 16 Oct; every entry since 12 Feb is down | Narrow offer, pro rata; EPCL.md says avoid above Rs27 |
| 12 | 2017 to 2019 bear and the 2018 election | Regime bear | Rate 5.75% to 13.25%, rupee 105 to 159 | 11 Dec 2017 (devaluation), 29 Jan 2018 (hike) | KSE -45.6% (-64% in USD); 3 of 75 names up | Read the rate and the rupee, not the politics |

## Cross-case findings

- IMF Board approval was not the low in any of cases 01, 03 and 04. The low came six weeks later (2019), five months later (2022), and eleven days earlier (2023).
- In both hike-cycle bears (03 and 12), the breadth was almost unanimous: 4% of liquid names were up over 21 and 27 months respectively. The index hid it in 03.
- Entries that worked were confirmations (rate hold, SLA window, first 10x volume day, disclosure). The best entry was never the low.
- Shock cases (02, 06) show the rebound arriving as a gap or an acceleration inside two to three weeks. The reachable gain was smaller than the move.

## Caveats

- Index: `data/macro/kse100.csv` is the headline series. Its levels match the widely reported headline index (52,876 on 24 May 2017; 116,169 on 16 Dec 2024). `knowledge/lessons.md` item 20 says it is a total-return series; `tests/rate_cycle_episodes.md` says it is a price index. Not resolved here.
- Stock breadth uses the survivors-only panel (456 symbols listed on 16 Oct 2026): losses in cases 03 and 12 are understated, and leaders flattered. Liquidity filter: Rs20m a day over 60 sessions, from adjusted prices, so earlier dates are slightly under-filtered.
- Trailing stops (10% on the index, 20% on single names) are illustrative placeholders. They were not tested and not chosen from evidence.
- News items marked "asserted" came from search snippets (the Business Recorder and several others returned 403 or were not opened in full). The 2018 election date, the Panama verdict, the Kashmir date and the Pahalgam date are general knowledge.
- Cash returns are approximations from auction yields.
