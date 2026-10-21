# Scorecard — how good are our predictions?

Rules: every prediction is frozen in `frozen_predictions.csv` before the event with a probability. When the outcome lands, the `outcome` and `score_note` columns are filled in. Nothing else in a frozen row is ever edited. This file summarises the record.

Scoring: Brier score per prediction = (probability − outcome)², outcome 1 if the prediction held, 0 if not. Lower is better. A coin flip at 50% scores 0.25. Report by category (results, macro events, price-direction calls, catalyst calls) with n.

| Period | n | Brier | Hit rate | Notes |
|---|---|---|---|---|
| 19 to 21 Oct 2026, results and corporate events | 8 | 0.092 | 8 of 8 (mean stated p 0.73) | EFERT EPS 7.07 consol., DPS 5.5; PRL EPS 22.17, nil DPS; ATRL EPS 174.89; EPCL EPS -1.45; MLCF EOGM passed. Too few rows to judge calibration; 8 of 8 at an average 0.73 hints the probabilities were slightly cautious. |
| Price-reaction rows | pending | | | EFERT test close 26 Oct (ref 194.82); PRL test close 28 Oct (ref 20 Oct close 101.44); orchestrator PRL conjunction scored with it |
| Conditional ATRL entry | n/a | | not triggered | Closed 1,190.74 on 20 Oct after the result, below the 1,200 trigger |

Inherited from the orchestrator's register (seed/FORECAST_REGISTER.md): frozen EPS ranges for EFERT (19 Oct), PRL (20 Oct), MEBL (22 Oct), FCCL (27 Oct), OGDC (29 Oct). Those are scored here too when results land, labelled "orchestrator".


Orchestrator register (seed/FORECAST_REGISTER.md), scored 21 Oct: EFERT Q3 consolidated EPS band -1.06/1.66/4.74, actual 7.07, above the bull case (miss, too low). PRL 'EPS >= Rs13' leg: actual 22.17 (hit); the 'flat to down over 5 sessions' leg is pending (test close about 28 Oct against the 20 Oct close Rs101.44).
