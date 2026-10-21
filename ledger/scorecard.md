# Scorecard — how good are the calls?

Every call and forecast is frozen in ledger/calls.csv with a probability before its event. Outcomes go in ledger/scores.csv (1 if the prediction held, 0 if not, void if withdrawn before entry, not_triggered if a conditional call never fired). Rows are never edited.

Brier score per row = (probability minus outcome) squared; lower is better, and 0.25 is a coin flip. Void and not-triggered rows are listed but not scored. Calibration means something at about 20 rows per kind; until then read the numbers as a first look.

## The record (built from the ledger; do not edit)

<!-- ledger:scores -->
| rows | n | Brier | held | mean stated odds |
|---|---|---|---|---|
| all | 8 | 0.092 | 8 of 8 | 0.73 |
| forecast | 8 | 0.092 | 8 of 8 | 0.73 |

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
<!-- /ledger:scores -->

## Notes that are not in the tables

- 19 to 21 Oct: 8 of 8 at a mean stated probability of 0.73 hints the probabilities were slightly cautious; several rows were easy (0.92, 0.93), so this says little yet.
- Orchestrator register (seed/FORECAST_REGISTER.md), scored 21 Oct: EFERT Q3 consolidated EPS band -1.06/1.66/4.74, actual 7.07, above the bull case (miss, too low). PRL "EPS >= Rs13" leg: actual 22.17 (hit); the "flat to down over 5 sessions" leg is scored with C0006 (test close about 28 Oct against the 20 Oct close Rs101.44).
- Price rows use the close of the fifth session after the release day against the last close before it.
