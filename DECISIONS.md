# DECISIONS.md — dated log of course changes

Format: date | decision | reason | who.

- 2026-10-17 | Take the orchestrator's brief as a starting point, not a cage. Reorder phases by expected payoff, add a practitioner sweep, a walk-forward system backtest and a calibration scorecard. | The user wants a learned model that improves itself, not a one-off pick list. Individual factor tests do not show how a strategy would have done. | Fable
- 2026-10-17 | Monday 19 Oct is not a deadline. | User said so; a provisional pick list ships when it can be defended. | Fable
- 2026-10-17 | Strategy frame: roughly half solid growing quality, half concentrated high-upside, with a cash rule so waiting never becomes the strategy. | User's own framing, plus lesson 13 (cash drag). | Fable
- 2026-10-17 | Use the PSX data portal directly (X-Req-Id header) instead of psxdata for refresh, announcements and payouts. | psxdata caps at 10 years and has no announcements; the portal's historical endpoint gives the same depth plus timestamps. | Fable
- 2026-10-17 | Downgrade the seed "deep value works" finding to "weak, mostly a sector effect, not distinguishable from zero". Keep rate-cycle turns (3 episodes, directionally strong) and sector momentum (t about 1.3, overlapping windows) as hypotheses to confirm in the walk-forward test, not as established facts. Momentum and operator "fails" are re-read as "no better than random entry", not "worse than random". | Opus audit in tests/seed_audit.md reproduced every number and found the value test lost 29 names to the XD-suffix bug, double-counted dividends, and collapses within sector. | Fable
