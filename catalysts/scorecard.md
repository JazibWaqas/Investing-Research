# Scorecard — how good are our predictions?

Rules: every prediction is frozen in `frozen_predictions.csv` before the event with a probability. When the outcome lands, the `outcome` and `score_note` columns are filled in. Nothing else in a frozen row is ever edited. This file summarises the record.

Scoring: Brier score per prediction = (probability − outcome)², outcome 1 if the prediction held, 0 if not. Lower is better. A coin flip at 50% scores 0.25. Report by category (results, macro events, price-direction calls, catalyst calls) with n.

| Period | n | Brier | Hit rate | Notes |
|---|---|---|---|---|
| (none scored yet) | 0 | — | — | Register opened 17 Oct 2026 |

Inherited from the orchestrator's register (seed/FORECAST_REGISTER.md): frozen EPS ranges for EFERT (19 Oct), PRL (20 Oct), MEBL (22 Oct), FCCL (27 Oct), OGDC (29 Oct). Those are scored here too when results land, labelled "orchestrator".
