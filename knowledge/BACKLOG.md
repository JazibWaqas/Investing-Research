# BACKLOG.md — the ranked research backlog

The one list of open research. Merged on 21 Oct 2026 from FINDINGS.md section 10, gpt/TEACHER_NOTES.md section 8, gpt/EXAMINER_NOTES.md and the old handoff log (archive/HANDOFF_2026-10-19.md). Ranked by how much the answer could change real decisions for Jazib. Nothing here starts without his explicit go (CLAUDE.md, "Do not launch work before mirroring").

## How an item moves

1. **Pick** the highest item that is unblocked. Mirror it back to Jazib in two or three sentences (question, method, cost) and wait for his go.
2. **Pre-register** the hypothesis, the rule, the placebo and the pass mark in the script header before running. Get an Opus design review for any backtest.
3. **Run** it. The write-up goes to tests/<name>.md with n, mean, median, win rate, worst case, independent episodes and the placebo.
4. **Propagate**: one line in tests/FACTS.md; change FINDINGS.md, PLAYBOOK.md or CATALOGUE.md only if the verdict changes them; a dated line in DECISIONS.md for any reversal; a lesson in knowledge/lessons.md if a mistake surfaced.
5. **Close** the item here: move it to "Done" with the date and the file that holds the answer.

## Open, ranked

1. **The live scorecard (running, no work to start).** Every weekly call is frozen and scored (catalysts/). Calibration is readable at about 20 weeks; the 20-session comparison against the plain breakout rule and random entries at about 5 months; the 60-session comparison at about a year. It is the only test of whether judgment adds anything (tests/replay_pilot_postmortem.md explains why history cannot test it).
2. **Exits on the full breakout population.** Test the named exits (stops sized to prior dips, event exits, re-entry on a new high, the third-off-at-+50%-and-+100% rule in PLAYBOOK.md section D) on every 252-session breakout, including the roughly three quarters that failed, pre-registered, with a placebo. Every exit in PLAYBOOK, CATALOGUE and REGIME_TURN_PLAYBOOK depends on it; today they were sized after seeing the winners' paths (knowledge/reviews/astra_catalogue_review.md).
3. **Filling the open core slot (LUCK withdrawn, not eligible).** Score FCCL, MLCF (after the PIOC merger), DGKC, KOHC and ILP on the business record (knowledge/companies/QUALITY_README.md method), so the core has a candidate and the turn has a non-Lucky cement name. Offered to Jazib on 21 Oct; waiting for his yes.
4. **Is the turn checklist real?** Fitted to 8 dates. Score it live: readings on 26 Oct (MPC), 2 Nov (CPI) and about 10 Nov (rupee and reserves). Also decide which low the 2022-23 turn is measured from (23 Jun 2023 reference vs 17 Jan 2023 lowest rupee close), because the reserve release rule's 11-month figure depends on it (knowledge/regime_turns/2022_23.md).
5. **Business quality against returns.** Score more liquid KMI names, freeze the scores at each year end from 2021, and test top against bottom third. Until then knowledge/companies/quality_scores.csv is a model's opinion.
6. **A regime gate for the breakout rule** (6-month bill vs policy rate), tested as a pre-registered variant; not applied live until tested.
7. **Policy implementation odds, systematically.** The 42% (62% with partial) figure rests on 26 hand-picked cases (knowledge/playbooks/actors_and_incentives.md). Build the full list from ECC and cabinet decisions with outcomes.
8. **More regime turns.** Extend index and macro history before 2016 from other sources so the checklist meets more than eight dates.
9. **Survivorship in thin names.** Merge data/prices_listed_missing/ (55 listed names, incl. POL, APL, HASCOL) into the panel (data/DELISTINGS_NOTES.md). No effect on the liquid basket; unknown for screens that reach thin names.
10. **Dividends before Nov 2024,** reconstructed from announcements, so dividend carry and the walk-forward's total returns can be compared with the total-return indices properly.
11. **Same-day questions,** only once the intraday archive (scripts/collect_intraday.py) has months of sessions.

## Do not repeat

Tested adequately, with placebos; the answers are in tests/FACTS.md: value screens, stock momentum, volume and upper-lock rules, investor-flow signals, index recomposition trades, dividend run-ups, calendar effects, insider cluster tests on the same data, the 40 daily rules, and any historical replay of a current model's judgment.

## Done

- 2026-10-19 | LUCK GEPCO exposure, MARI Brent sensitivity, reserve release rule | knowledge/companies/LUCK_gepco.md, knowledge/companies/MARI.md, PLAYBOOK.md section A
- 2026-10-21 | First results scored (8 of 8, Brier 0.092) | catalysts/scorecard.md
