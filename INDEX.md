# INDEX.md — map of the repo

Every live document or folder, what it holds and when to open it. Start with CLAUDE.md, which gives the session protocol and the precedence rules. scripts/check_docs.py fails if a live document is missing from this map. Updated 21 Oct 2026.

## Root: read every session

| Path | What it is | Open when |
|---|---|---|
| CLAUDE.md | Entry point: session protocol, layer map, precedence, writing rules, self-improvement loop, models, environment, the investor | Always first (auto-loaded by Claude Code) |
| AGENTS.md | Pointer to CLAUDE.md for non-Claude agents | Never needed by Claude |
| INDEX.md | This map | Looking for anything |
| STATE.md | What is live now: holdings (built), Jazib's open decisions, pending events (built), data freshness | Every session, start and end |
| PLAYBOOK.md | How to decide: what does not change, his stance on risk, the questions for every decision, reference points from the evidence, what tends to go wrong. No fixed rules | Before any call |
| PICKS.md | The open calls and forecasts, built from ledger/calls.csv (do not edit) | Before any call |
| DECISIONS.md | Dated log of every course change, with reason and author; append only | When asking why something is the way it is |
| RUNBOOK.md | The weekly loop step by step | Running the weekly loop by hand |

## knowledge/: what we know

| Path | What it is | Open when |
|---|---|---|
| knowledge/FINDINGS.md | The canonical synthesis: mechanisms ranked by effect, the 2026 retrospective, calibration, the regime, corrections to the seed, the machine, the models | Catching up; any "what works" question |
| knowledge/HOW_TO_THINK.md | How Jazib thinks, how the research went wrong and was corrected, thinking rules, alignment questions, what each phase taught | Before advising him or starting research |
| knowledge/lessons.md | 26 mistakes, each with the rule it produced | Before any analysis |
| knowledge/CATALOGUE.md | The if-then casebook of situation types: recognise, join, milk, leave; read its status box first (hypotheses, not a validated system) | Judging a moving stock |
| knowledge/REGIME_TURN_PLAYBOOK.md | Four turns vs four false bottoms, the checklist, leader sequence, entry in thirds, exits, today's reading | Any rate decision, crash or rally |
| knowledge/QUESTIONS.md | 42 questions an experienced investor asks before a call; scripts/replay_bundle.py reads it | Underwriting a name |
| knowledge/BACKLOG.md | The ranked research backlog, its protocol, the do-not-repeat list, done items | Choosing research; closing a test |
| knowledge/companies/ | Underwriting cards with red teams (`SYM.md`), business-quality records (`SYM_quality.md`), quality_scores.csv, QUALITY_README.md. LUCK is allowed when worth the declaration | Any single name |
| knowledge/sectors/ | README.md (the 16-sector ranking and verdicts, 17 Oct) and one note per sector: levers, state, catalysts, names, past episodes; _unresolved_gaps.md | Any sector question |
| knowledge/situations/ | 12 dated point-in-time cases (2017 bear to the 2026 EPCL takeover) and INDEX.md with machine rows | Comparing a live situation with the past |
| knowledge/winners/ | 49 hindsight case studies of big runs and 6 syntheses (`_*.md`) by type | Studying what a winner looked like before it moved |
| knowledge/regime_turns/ | The 2019, 2020, 2022-23 and 2024 turns week by week, with the present read | Deep dive behind the turn playbook |
| knowledge/playbooks/ | Situation playbooks (deals, holdco discounts, catalyst trade, sector rotation, actors and incentives, practitioner signals, active trading, short term), the situation engine guide, the pre-registered strategy rules (strategy_candidates.md) and the replay exam design (replay_exam.md, read by scripts) | A situation of that kind; understanding a test design |
| knowledge/reviews/ | Independent critiques that changed decisions: critic_review (Codex), consultant_review (Fable), astra_peer_review and astra_catalogue_review (GPT-6 Astra), picks_redteam_codex | Before trusting a conclusion they challenged; template for new reviews |

## tests/: the evidence

| Path | What it is | Open when |
|---|---|---|
| tests/FACTS.md | Headline numbers from every test, verbatim, with verdict words | First stop for any number |
| tests/BASE_RATES.csv | 395 rows of measured odds by situation type and horizon (full-sample, so hindsight-exposed) | Odds for a situation |
| tests/ | One write-up per test (30), each naming its script in scripts/tests/ and raw output in tests/out/ | Checking a number or method at the source |
| tests/out/ | Raw run outputs, replay packs, engine scans | Reproducing a write-up |

## ledger/ and journal/: the record

| Path | What it is | Open when |
|---|---|---|
| ledger/calls.csv | Every call and forecast ever made, with odds, rupee upside and downside, what proves it wrong, the journal link, and `supersedes`; append only | Making, changing or reading a call |
| ledger/scores.csv | Outcomes of calls (1, 0, void, not_triggered); append only | Scoring |
| ledger/trades.csv, ledger/deposits.csv | What Jazib actually bought, sold and put in, as he reports it | Recording a trade |
| ledger/scorecard.md | Brier score and hit rate built from the tables, plus notes | Judging how good the calls are |
| ledger/book_daily.csv | Built: the book's daily value against the same money in the KMI All Share | Asking how the money has done |
| journal/ | One entry per session (`<date>.md`) and every letter to Jazib (`<date>-picks-vN.md`, all versions since 18 Oct); never edited after its day | Asking why something was decided |
| scripts/ledger.py | Validates the tables, records trades and deposits, builds PICKS.md, the built sections of STATE.md, the scorecard and the daily book | Every session |

## catalysts/: dated events

| Path | What it is | Open when |
|---|---|---|
| catalysts/catalyst_calendar.csv, dividend_calendar.csv | Dated events by ticker | Planning the week |

## data/: datasets and their notes

| Path | What it is |
|---|---|
| data/CORPORATE_ACTIONS_NOTES.md | Corporate-actions table, adjusted panel, reconciliation, the T+2 to T+1 ex-date change |
| data/DAILY_TABLE_NOTES.md | The daily decision table: columns, definitions, gaps |
| data/DELISTINGS_NOTES.md | Delistings and survivorship |
| data/INDEX_DATA_NOTES.md | Index membership history and caveats |
| data/INSIDER_TRADES_NOTES.md | The insider trades table |
| data/costs.md | Trading costs via Finqalab (its own commission unverified) |
| data/macro/ | README.md (every macro and commodity series) and INDEX_NOTES.md (total return vs price indices) |
| data/fundamentals/ | quarterly_eps.csv (129 names; standalone vs consolidated not flagged) and QUARTERLY_EPS_NOTES.md |
| data/intraday/ | Tick archive by session, README.md |
| data/prices_raw/, prices_delisted/, prices_listed_missing/ | Daily OHLCV from the PSX portal (STATE.md says how fresh) |
| data/asof/ | Point-in-time packs and bundles by date; generated, never edited |

## scripts/

The pipeline (entry points in CLAUDE.md section 7), scripts/tests/ (one script per test), scripts/ca/ (corporate actions), scripts/codex/ (Codex's independent engines), scripts/audit/ (seed-era audits). scripts/check_docs.py is the documentation check run at the end of every session.

## gpt/: the GPT-6 project pack

| Path | What it is |
|---|---|
| gpt/README.md | How Jazib sets up the ChatGPT project and what to upload |
| gpt/PROJECT_INSTRUCTIONS.md | The project's instructions box |
| gpt/ALERT_TASKS.md | Five scheduled alert prompts |
| gpt/TEACHER_NOTES.md | Reasoning the documents do not carry: what was misunderstood, how PSX works causally, discoveries graded, mistakes, advice (21 Oct snapshot) |
| gpt/EXAMINER_NOTES.md | The five conclusions most likely to be wrong, document contradictions and precedence, six scenarios, tacit knowledge, audit verdict (21 Oct snapshot); the template for any future model's examination |

## .claude/ and .agents/

`.claude/skills/psx-weekly/SKILL.md` is the weekly loop as a skill (`/psx-weekly`); `.agents/skills/psx-weekly/SKILL.md` is an identical copy for other agents, kept in sync by the doc check.
`.claude/skills/psx-weekly/jazib-learning/SKILL.md` is how to teach Jazib when he asks to learn something (applied first, failure mode first, no quizzes); load it for any "teach me" session.

## archive/ and seed/: history, never instructions

| Path | What it is |
|---|---|
| archive/HANDOFF_2026-10-19.md | Session state log to 19 Oct (replaced by STATE.md) |
| archive/PLAN_2026-10-17.md | The original plan (replaced by HOW_TO_THINK.md and BACKLOG.md) |
| archive/REPORT_2026-10-18.md | The long-form account of what works (replaced by FINDINGS.md; some narrative detail only here) |
| archive/strategy_2026-10-18.md | The 18 Oct strategy note (replaced by PLAYBOOK.md) |
| journal/ | PICKS v3 and v4 |
| seed/ | The orchestrator's original brief, state, register (FORECAST_REGISTER.md, still scored), lessons, scripts and data (scripts read seed/data; do not move it) |
