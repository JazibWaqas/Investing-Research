# Setting up the GPT project (for Jazib)

1. In ChatGPT, create a Project named "PSX Research".
2. Paste the whole of `gpt/PROJECT_INSTRUCTIONS.md` into the project's Instructions box.
3. Upload these files as project knowledge, in this order of importance (the first eight are the must-haves if there is a file limit):
   1. ORCHESTRATOR_HANDOFF.md — everything established, with sources
   2. PLAYBOOK.md — the rules on one page
   3. PICKS.md — current positions, triggers, the 21 Oct LUCK amendment
   4. knowledge/HOW_TO_THINK.md — how you think, how the research went wrong and was corrected
   5. knowledge/CATALOGUE.md — the casebook of situation types
   6. knowledge/REGIME_TURN_PLAYBOOK.md — the turn checklist
   7. knowledge/lessons.md — 25 mistakes and their rules
   8. tests/FACTS.md — every test's headline numbers
   9. knowledge/QUESTIONS.md — the question list
   10. knowledge/companies/quality_scores.csv — business-quality scores
   11. catalysts/frozen_predictions.csv — the live register
   12. catalysts/catalyst_calendar.csv and catalysts/dividend_calendar.csv
   13. knowledge/companies/MEBL.md, MARI.md, SAZEW.md, FABL.md — cards for the names in play
   14. REPORT.md — the full account, if there is room
4. Create the five scheduled tasks in `gpt/ALERT_TASKS.md` (copy each prompt into a new task, set the schedule it names).
5. Every week, re-upload PICKS.md, catalysts/frozen_predictions.csv and catalysts/scorecard.md so it has the current state. When the Claude session changes a knowledge file, re-upload that file too.
6. To pass questions between the two: paste GPT's question into the Claude repo session; paste Claude's answer back. Anything needing the data tools (backtests, the daily table, the situation engine) goes to Claude.
