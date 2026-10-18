---
type: "policy decision (first cut of an easing cycle)"
knowable_date: 2024-06-10
outcome_end: 2024-12-16
summary: "First-cut policy decision in an easing cycle: KSE +59% by December 2024; fertilizer, E&P and pharma led while banks lagged. Lesson: favour sectors with their own catalyst over rate-sensitive ones."
---

# Situation 05: the June 2024 first cut and the sector leaders

Written 2026-10-18. Type: policy decision (first cut of an easing cycle). Sources: `data/macro/`, `data/panel_close_adj_pricereturn.parquet` (94 liquid survivors, sector from `data/symbols.csv`), `tests/rate_cycle_episodes.md` (H1 table and placebo), `knowledge/playbooks/sector_rotation.md`. News: Profit and Geo, 10 Jun 2024; the SBP statement as reported (asserted from search snippets, not opened in full).

## Dates and regime

- 10 Jun 2024: the SBP cut 150bp to 20.5% (effective 11 Jun), the first cut in four years (asserted). Seven decisions at 22%, from Jun 2023 to Apr 2024, preceded it (observed).
- CPI 11.74% in May 2024, down from 37.97% in May 2023 (observed). The real policy rate was about +9 points. 3-month T-bill 21.0%.
- USD/PKR 278.3, flat for a year. IMF: the 2023 standby ended in spring 2024; a 37-month EFF of about $7bn was agreed later in the summer and approved by the Board on 25 Sep 2024 (IMF PR 25/137 background, asserted).
- KSE 73,253 on cut day, already +83% from 40,065 on 23 Jun 2023 (case 04).

## What was knowable, and when

1. Mar to May 2024: CPI fell to 20.7% (Mar), then 17.3% (Apr), then 11.7% (May). What analysts expected was not checked.
2. 10 Jun: the cut itself. The MPC also warned inflation would jump in July on base effects, before trending down.
3. 12 to 13 Jun: the FY25 budget was presented; KSE +4.7% on 13 Jun (76,208). The cause of that jump was not verified.
4. 29 Jul, 12 Sep, 4 Nov, 16 Dec: further cuts of 100, 200, 250 and 200bp, to 13.0%. Total 900bp in six months, 1,000bp by Jan 2025.

## What the market did

| Date | KSE | Note |
|---|---|---|
| 10 Jun 2024 | 73,253 | cut day |
| 11 Jun | 72,589 | -0.9% next day |
| 12 Sep | 79,018 | third cut |
| 16 Dec | 116,169 | +58.6% from cut day |
| 21 Apr 2025 | 118,383 | +61.6% |

The repo test (`tests/rate_cycle_episodes.md`) shows, for the first cut of each of the three easing clusters (2020, 2024, 2025-12) taken as n_eff = 3: KSE 20-day mean +6.7%, 60-day median +8.4% with one loser (-9.4%), 120-day median +39.8%, with a worst case of +1.1%. The 2024 cut alone: +10.1% at 20 days, +8.4% at 60, +49.1% at 120. With three episodes, percentiles are descriptive only.

Median liquid name from the cut to 16 Dec 2024: +42.6%, below the index (+58.6%): the gain was concentrated in the heavyweights.

Sector medians to 16 Dec 2024 (sectors with at least 2 names): pharma +96%, E&P +90% (2 names), fertilizer +85%, OMC +76%, refiners +65%, food +47%, autos +44%, cement +38%, banks +31% (11), technology +28% (10), textile composite +24%, power +14%, engineering +4%. Stock leaders: FLYNG +243%, FFC +206%, SYM +206%, AIRLINK +153%, CPHL +146%, PSO +136%, ATRL +108%.

## The right move

Entry: the 10 Jun close (73,253) or 11 Jun (72,589). Exit: a 10% trailing stop on closes triggers on 8 May 2025 at 103,527, +41.3% (+42.6% from 11 Jun), which is the low of the India conflict (case 06), followed by a 13% rebound in two sessions. The stop is a placeholder and its whipsaw is part of the lesson: a trailing stop on a 12-month trend trade can sell the low.

The more important choice was where to hold. The textbook rate beneficiaries (banks, cement, autos) delivered +31% to +44%. The leaders were sectors with their own catalyst: fertilizer (gas and dividends), E&P and OMC (circular-debt relief), and pharma. Power, the other textbook rate play, returned +14%.

## The trap

Two. First, the headline: the cut came after an 83% rally, and a buyer expecting a first-cut pop got -0.9% the next day. Second, assuming the rate-sensitive sectors lead. Banks look cheap and fall in yield when rates fall; leveraged cement and autos recover earnings late. Testing this requires per-sector evidence, not a story.

## Situation type and lesson

Policy decision priced in advance, in a regime that then supplied 1,000bp of cuts. The cut was a regime confirmation, not an information event. What it teaches: for a first cut, the right questions are how much more is coming (here, a lot, because the real rate was nine points) and which sectors carry their own catalyst, not whether the market reacts on the day. In 2025-12 the same signal produced +7.1% at 20 days and -9.4% at 60 (a war), so the signal is conditional on the external account.

## Questions that would have caught it

- Q1 Regime: the real policy rate (about +9 points), the trajectory of CPI, the IMF programme, the rupee flat for twelve months. Together: room for many cuts.
- Q2 Situation type and base rate: first cut of a cluster; n_eff = 3; median 120-day return +39.8%, worst +1.1%.
- Q3 Who gains: sectors with their own catalyst (gas, dividends, circular debt), not by default the most leveraged.
- Q4 Price: +83% already. Was this confirmation or extension? It was confirmation, because the earnings base was 2023 crisis earnings.
- Q5 Exit: the stop hit at 103,527 and the rebound followed.
