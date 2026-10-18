# Results-jump winners: what eight cases teach

Written 2026-10-18 from the eight case files beside this one (ATRL, FABL, ILP, NETSOL, TELE, INIL, FCEPL, MACFL): seven of the eight largest of the 18 liquid `results_jump` episodes in `data/winners_library.csv` (7.6x to 2.0x), with MACFL 2026 in place of MUGHAL 2023, which shares NETSOL's start date and wave. Four are 2022 to 2023, two May 2025, two 2026. Hindsight picks. Evidence: `tests/out/winners_results_jumps_sims.txt` and `_twins.txt`.

## Is there a shared signature?

Not in the filings. The label means a recent quarter had EPS at least 1.5x a year earlier; 16 of the 18 library episodes also carry a sector or shock flag, and the eight sit in three market events: the July 2023 IMF rally (ATRL, FABL, ILP, NETSOL), the May 2025 shock (TELE, INIL) and the March 2026 shock (FCEPL, MACFL). In six of eight the filing did not start the run. Three patterns, one rule each:

- **Ignored jump, then a trigger** (ATRL, FABL, ILP): the price waited one to eight months. Buy the first 252-day high after the trigger, not the filing (95%, 83% and 66% of the log gain still ahead).
- **Not really earnings** (NETSOL: other income; INIL: one quarter inside a year of 59% lower profit; TELE: Rs0.28 of EPS). Ignore the filing; the run was the market or a theme, and the late entries lost. At the first 252-day high only 37%, 28% and 18% was left.
- **A real operating jump with a fast price reply** (FCEPL, MACFL): join within two or three sessions with a 25% trail; the filing had 66% to 83% of the gain ahead, the first 252-day high 34%. Only these two were readable from the filing.

## Failures, and the base rate

Entering on the filing lost more than 13% within 20 sessions in four of eight (NETSOL 14%, INIL 19%, TELE 22%, FCEPL 25%), three of them in a market shock that the filing did not protect against; ATRL was 26% under cost within 60 sessions. Across 408 EPS-jump events since 2021 (123 liquid names) the 20-session median was plus 0.9%, win rate 52%; 10% fell 15% or more within 20 sessions (21% of the 103 events of 2026); 31.6% reached plus 50% within 126 sessions against 27.0% for other results releases. `tests/results_surprise_drift.md` has a median of minus 1.6% at 20 sessions. The jump adds little; the eight are survivors.

## Exits that kept the move

A 25% trail from the first 252-day high kept 3.3x of FABL's 5.5x; stop-out and re-entry kept about 5.3x of ATRL's 7.6x; a 25% trail made 2.0x in ILP (right: it later lost 45%) and 2.6x in MACFL (which then rose another 1.8x). A stop under 25% was hit before the real run in ATRL, FCEPL and TELE, and mid-run in NETSOL. Hypothesis: sit just outside the largest pullback so far, but no wider than 25% where earnings give no support (ILP, TELE, MACFL).

## Caveat

The library's EPS pairs were wrong against the filings in ATRL, NETSOL and FCEPL, and the EPS file was 3% to 5% off in ATRL and NETSOL. Eight cases, no placebo.
