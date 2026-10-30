# Scorecard — how good are the calls?

Every call and forecast is frozen in ledger/calls.csv with a probability before its event. Outcomes go in ledger/scores.csv (1 if the prediction held, 0 if not, void if withdrawn before entry, not_triggered if a conditional call never fired). Rows are never edited.

Brier score per row = (probability minus outcome) squared; lower is better, and 0.25 is a coin flip. Void and not-triggered rows are listed but not scored. Calibration means something at about 20 rows per kind; until then read the numbers as a first look.

## The record (built from the ledger; do not edit)

<!-- ledger:scores -->
| rows | n | Brier | held | mean stated odds |
|---|---|---|---|---|
| all | 24 | 0.164 | 15 of 24 | 0.60 |
| call | 1 | 0.040 | 0 of 1 | 0.20 |
| forecast | 23 | 0.170 | 15 of 23 | 0.62 |

| id | scored | ticker | prediction | odds | outcome | note |
|---|---|---|---|---|---|---|
| C0001 | 2026-10-21 | EFERT | Consolidated EPS between Rs4.80 and Rs7.50 (above the frozen bull of 4.74) | 0.62 | 1 | Consolidated Q3 EPS 7.07 (standalone 6.83), Q3-25 4.07; filing PSX doc 286023... |
| C0002 | 2026-10-21 | EFERT | Consolidated EPS above Rs4.74 | 0.8 | 1 | Consolidated Q3 EPS 7.07; the orchestrator band (-1.06/1.66/4.74) was too low. |
| C0003 | 2026-10-21 | EFERT | Interim DPS of Rs3.50 or more | 0.75 | 1 | Interim DPS Rs5.50 (book closure 2-3 Nov; 9M dividends Rs9.25). |
| C0005 | 2026-10-21 | PRL | Standalone EPS of Rs13.00 or more | 0.58 | 1 | Q1 FY27 EPS Rs22.17 (PAT Rs13.97bn) vs Rs1.61; filing doc 286225, 21 Oct 08:00. |
| C0007 | 2026-10-21 | PRL | No cash dividend declared with Q1 results | 0.93 | 1 | Board recommended nil dividend. |
| C0025 | 2026-10-21 | MLCF | Shareholders approve the scheme (resolution passes) | 0.92 | 1 | Special resolutions adopted at the 19 Oct EOGM (doc 286112); PIOC certified r... |
| C0026 | 2026-10-21 | ATRL | EPS of Rs100 or more | 0.68 | 1 | Q1 FY27 EPS Rs174.89 (PAT Rs18.65bn) vs Rs13.62; filing doc 286077, 20 Oct 08... |
| C0027 | 2026-10-21 | EPCL | EPS below Rs1.04 (the Q2 CY26 EPS) | 0.55 | 1 | Q3 EPS loss Rs1.45 basic (doc 286227, 21 Oct 08:01). |
| C0041 | 2026-10-21 | ATRL | If entered, trade closes with a net gain (stop at Rs975 on a closing basis) | 0.5 | not_triggered | Result was published 20 Oct 08:41, not before the Monday close; ATRL then clo... |
| C0037 | 2026-10-21 | LUCK | Total return incl. net dividends positive over 12 months from fill | 0.55 | void | No position taken; the 19 Oct LUCK row is void (never entered). Compliance: t... |
| C0004 | 2026-10-30 | EFERT | Price rule: close of 5th trading session after the release day (release day =... | 0.45 | 0 | EFERT 26 Oct close 190.41 vs ref 194.82 (lower) |
| C0006 | 2026-10-30 | PRL | EPS >= Rs13 AND stock flat-to-down over 5 sessions. Price rule: close of 5th ... | 0.28 | 1 | PRL EPS 22.17 and 28 Oct close 94.16 vs 101.44: both legs held; the orchestra... |
| C0008 | 2026-10-30 | PRL | Price rule: close of 5th trading session after the release day (release day =... | 0.42 | 0 | PRL 28 Oct close 94.16 vs 101.44 (lower) |
| C0009 | 2026-10-30 | MEBL | Standalone EPS between Rs12.50 and Rs15.00 (the frozen bull is 12.74) | 0.65 | 1 | Q3 standalone EPS 14.36 (consolidated 14.34), PSX doc 286477, 22 Oct 12:04 |
| C0010 | 2026-10-30 | MEBL | Standalone EPS inside the frozen 7.02-12.74 band | 0.22 | 0 | EPS 14.36 above the orchestrator band 7.02-12.74 (band too low) |
| C0011 | 2026-10-30 | MEBL | Interim DPS of Rs8.00 or more | 0.6 | 1 | Interim DPS Rs8.00, book closure notice doc 286843 |
| C0012 | 2026-10-30 | MEBL | Price rule: close of 5th trading session after the release day (release day =... | 0.48 | 0 | MEBL 29 Oct close 526.08 vs 21 Oct 546.95 (lower, despite the beat) |
| C0013 | 2026-10-30 | FCCL | EPS between Rs1.45 and Rs2.00 | 0.55 | 0 | FCCL 1QFY27 EPS 2.02, just above the 1.45-2.00 band; doc 287026 |
| C0014 | 2026-10-30 | FCCL | No interim cash dividend declared with Q1 results | 0.93 | 1 | No interim dividend with FCCL Q1 |
| C0016 | 2026-10-30 | FFC | Consolidated EPS between Rs14.00 and Rs18.00 | 0.65 | 0 | FFC Q3 consolidated EPS 19.72 (standalone 15.51), above the 14-18 band; doc 2... |
| C0017 | 2026-10-30 | FFC | Interim DPS between Rs9.50 and Rs14.50 inclusive | 0.65 | 0 | FFC interim DPS 18.50, above the 9.50-14.50 band |
| C0019 | 2026-10-30 | OGDC | Standalone EPS between Rs11.00 and Rs14.50 (frozen band is 8.08-9.94) | 0.62 | 1 | OGDC Q1 EPS 13.60 vs 8.91; basis per press (consolidated quoted), inside 11-1... |
| C0020 | 2026-10-30 | OGDC | Standalone EPS above Rs9.94 | 0.82 | 1 | OGDC EPS 13.60 above 9.94; orchestrator band 8.08-9.94 too low |
| C0021 | 2026-10-30 | OGDC | Interim DPS between Rs4.00 and Rs6.00 | 0.65 | 1 | OGDC interim DPS Rs5.00 |
| C0023 | 2026-10-30 | Policy rate | Policy rate held at 11.5% | 0.5 | 0 | MPC raised 50bp to 12% on 26 Oct (9-1 vote); we had hold 0.50, +50bp 0.38 |
| C0047 | 2026-10-30 | SAZEW | The trigger fires: Q1 FY27 EPS of Rs60 or more AND no hike on 26 Oct | 0.20 | 0 | SAZEW Q1 EPS 66.77 met the EPS leg (doc 27 Oct), but the MPC hiked, so the tr... |
<!-- /ledger:scores -->

## Notes that are not in the tables

- 19 to 21 Oct: 8 of 8 at a mean stated probability of 0.73 hints the probabilities were slightly cautious; several rows were easy (0.92, 0.93), so this says little yet.
- Orchestrator register (seed/FORECAST_REGISTER.md), scored 21 Oct: EFERT Q3 consolidated EPS band -1.06/1.66/4.74, actual 7.07, above the bull case (miss, too low). PRL "EPS >= Rs13" leg: actual 22.17 (hit); the "flat to down over 5 sessions" leg is scored with C0006 (test close about 28 Oct against the 20 Oct close Rs101.44).
- Price rows use the close of the fifth session after the release day against the last close before it.
