# Setting up the GPT project (for Jazib)

1. In ChatGPT, create a Project named "PSX Research".
2. Paste the whole of `gpt/PROJECT_INSTRUCTIONS.md` into the project's Instructions box.
3. Upload these files as project knowledge, in this order of importance (the first nine are the must-haves if there is a file limit):
   1. STATE.md — what is live now: holdings, open decisions, pending events
   2. PLAYBOOK.md — the rules on one page
   3. PICKS.md — version 5: positions, triggers, dates
   4. knowledge/FINDINGS.md — everything established, with sources
   5. gpt/TEACHER_NOTES.md — the reasoning behind the documents, the discoveries graded by evidence, mistakes, advice
   6. gpt/EXAMINER_NOTES.md — the conclusions most likely to be wrong, contradictions and which document to follow, six test scenarios
   7. knowledge/HOW_TO_THINK.md — how you think, how the research went wrong and was corrected
   8. knowledge/CATALOGUE.md — the casebook of situation types
   9. knowledge/REGIME_TURN_PLAYBOOK.md — the turn checklist
   10. knowledge/lessons.md — 26 mistakes and their rules
   11. tests/FACTS.md — every test's headline numbers
   12. knowledge/BACKLOG.md — open research, and what not to repeat
   13. knowledge/QUESTIONS.md — the question list
   14. knowledge/companies/quality_scores.csv — business-quality scores
   15. catalysts/frozen_predictions.csv and catalysts/scorecard.md — the live register and its record
   16. catalysts/catalyst_calendar.csv and catalysts/dividend_calendar.csv
   17. knowledge/companies/MEBL.md, MARI.md, SAZEW.md, FABL.md — cards for the names in play
4. Create the five scheduled tasks in `gpt/ALERT_TASKS.md` (copy each prompt into a new task, set the schedule it names).
5. Every week, re-upload STATE.md, PICKS.md, catalysts/frozen_predictions.csv and catalysts/scorecard.md so it has the current state. When the Claude session changes a knowledge file, re-upload that file too.
6. To pass questions between the two: paste GPT's question into the Claude repo session; paste Claude's answer back. Anything needing the data tools (backtests, the daily table, the situation engine) goes to Claude.
