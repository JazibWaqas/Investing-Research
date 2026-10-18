---
type: "volume ignition with upper locks, on a regulated utility with late accounts"
knowable_date: 2024-10-23
outcome_end: 2024-12-30
summary: "Volume ignition with upper locks on a regulated utility with late accounts: SSGC rose from 9.95 to 49.52 by the December 2024 peak with no filing explaining it. Lesson: instinct paid, but the repo cannot yet say when."
---

# Situation 09: SSGC, the 2024 volume run (the investor's own call)

Written 2026-10-18. Type: volume ignition with upper locks, on a regulated utility with late accounts. Sources: `data/prices_raw/SSGC.csv` (no corporate action in the window), `data/announcements.parquet`, PSX documents 236238, 242268, 242895, 244612 (downloaded and read this session), `knowledge/sectors/gas_utilities_misc.md`, PACRA rating report and Business Recorder summaries of the OGRA decision (asserted via search; the Business Recorder pages returned 403 and were not opened). His actual entry and exit dates are not in the repo; "+120%" below is his stated figure, unverified.

## Dates and regime

- 12 Sep 2024: policy rate 17.5% (cut again 4 Nov to 15.0% and 16 Dec to 13.0%). CPI 6.9% (Sep), 4.9% (Nov). USD/PKR 278. 3-month bill 15.3% on 23 Oct.
- KSE 83,532 on 4 Oct, 115,259 on 30 Dec: +38%.
- SSGC: a regulated-return utility with accounts about a year and a half late, a qualified audit, and an acting MD (the MD resigned 2 Sep, doc 236238) and CFO.

## What was knowable, and when

1. 1 Oct: OGRA issued the final revenue requirement for FY2022-23, nearly a year late. SSGC was allowed a 23.45% return on average net operating assets (16.60% the prior year), Rs23.5bn, plus Rs1.85bn of prior-period claims (PACRA, asserted). When it became public is not established (first volume day 7 Oct). No consumer gas-tariff event was found for the window.
2. 5 Nov: FY2022-23 results (doc 242268): unconsolidated loss per share Rs1.82, qualified opinion, on Rs26.3bn owed by K-Electric and Rs22.3bn by Pakistan Steel Mills that the auditors could not confirm as recoverable. The profit was not in these accounts.
3. 13 to 15 Nov: PSX queried the price and volume; SSGC replied that it knew of no undisclosed information (doc 242895). SNGPL later challenged the ruling as biased (Business Recorder, asserted).
4. 13 and 18 Dec: PACRA upgraded SSGC from A+ to AA- (doc 244612). 17 Dec: management briefing; the plan assumed a 20.05% return on Rs155.6bn of assets for FY26 (doc 244576).
5. 13 May 2025: FY2023-24 accounts, 18 months after year-end (doc 253788). The sector file says FY24 EPS was 7.76; that figure was not public in November 2024, and the sector file's remark that the price was "1.1x FY24 EPS before release" is hindsight.

## What the market did

| Date | Close | Volume (m) | Note |
|---|---|---|---|
| 4 Oct | 8.58 | 0.2 | the base: median 0.65m a day since July |
| 7 Oct | 8.84 | 3.4 | first ignition, +3.0% |
| 23 Oct | 9.95 | 17.0 | +11.2%, volume 26x the base |
| 5 Nov | 16.68 | 52.0 | +10%, the FY23 loss day |
| 15 Nov | 26.40 | 36.3 | unusual-movement reply |
| 30 Dec | 49.52 | 30.3 | peak close; high 50.87 |
| 7 Jan 2025 | 39.24 | 33.4 | first close 20% below peak |
| 13 May 2025 | 32.79 | | FY24 accounts |
| 16 Oct 2026 | 22.91 | | low 19.43 on 30 Mar 2026 |

From 23 Oct to 31 Jan there were 12 closes at +10% and 3 at -10%, with average volume 32m a day against 1.2m before. The run lasted nine weeks.

## The right move

Entry that existed: the 23 Oct close (9.95, the first 10x volume day), or 25 Oct (11.98, volume 38m) once the pattern repeated. Exit: a 20% trailing stop on closes triggers on 7 Jan 2025 at 39.24, which is +294% from 23 Oct, +227% from 25 Oct, +135% from 5 Nov and +49% from 15 Nov. A +120% result (his figure) corresponds, for instance, to 11.98 to 26.40, entry 25 Oct and exit 15 Nov. The stop is a placeholder, not a tested rule.

## The trap

Staying on the fundamentals. Nothing public in the filings explained the price: the one dated fact (OGRA, 1 Oct) pre-dated the run, the earnings were hidden, and the audit was qualified. Entering late: a buyer on 6 Dec (38.25) saw -10% on 10 Dec. Holding: SSGC reported about -Rs4.6 a share for the June 2025 quarter (stockanalysis; a true-up that erased three profitable quarters), and the price was Rs22.91 on 16 Oct 2026.

## Situation type and lesson

Volume ignition on a regulated name with a regulatory fact nobody could price. The repo's tested volume rule (10-day over 120-day volume above 2.5x with a 20-day return above +15%, n = 788) has median -3.4% at 60 days and a win rate of 45%, only a weak edge. SSGC was in the right tail (6.1% of cases above +50%). Instinct was right here; the repo cannot yet say when it is right. What differed from a typical pump: a real regulator decision, a rating upgrade, repeated 10% closes on rising volume, and a regime of falling rates that favoured a leveraged utility.

## Questions that would have caught it

- Q2 Type and base rate: volume ignition, n = 788, median -3.4%.
- Q3 Actors: OGRA ruling for SSGC and against SNGPL; the government owns both. Who gains, who is the counterparty (consumers, KE)?
- Q4 Price: confirmation on 23 Oct (17m shares, 26x base) rather than extension at 36.
- Q5 Exit: 20% off the peak. Written before entry.
- Q6 Traps: qualified audit, receivables from KE and PSML, a Q4 true-up, a company reply of "no news".
