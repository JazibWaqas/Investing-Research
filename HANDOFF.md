# HANDOFF.md — state of the program (18 Oct 2026, evening)

> Status: PAUSED by the user for alignment. Read knowledge/HOW_TO_THINK.md first. The plan in its section 9 (thinking charter and question list, situation library, noise and actor maps, opportunity types incl. shock and rebound, blind replays across regimes, growth core, then names and sizing with him) starts only when he explicitly says go. A growth-and-opportunity workflow was launched and stopped on his request; do not resume it blindly, re-brief it from HOW_TO_THINK.md. PICKS.md v3 predates the alignment and is evidence, not the plan; do not place its orders without his say.

Deliverables are complete: REPORT.md, PICKS.md (v2), RUNBOOK.md, sector_map.md, catalysts/ (calendar, dividend calendar, 33 frozen predictions, scorecard), knowledge/ (16 sector notes, 13 company cards with red teams, 10 playbooks incl. strategy, deals, holdco discounts, catalyst trade, practitioner signals, critic and consultant reviews), tests/ (14 test write-ups plus FACTS.md), data/ and scripts/ as documented in CLAUDE.md. Everything is committed and pushed to origin main.

## Still running when this was written
Nothing. All agents and workflows have completed; every output is committed.

## What to do next, in order
1. Monday 19 Oct: place the three core orders and the PRL sleeve buy in PICKS.md v3 (stop Rs85.60 on a closing basis). Score EFERT, ATRL and MLCF rows in catalysts/frozen_predictions.csv after the close (RUNBOOK step 2). Tuesday: PRL (after 15:00 board), EPCL. Wednesday: MEBL, FABL. 26 Oct: MPC. 27 to 29 Oct: FCCL, FFC, OGDC.
2. After each result, check the killers in the company cards; a fired killer means the next deposit's add limit tightens (PICKS.md, second deposit).
3. Weekly: RUNBOOK.md. Monthly: the Rs50k split 75/25 per PICKS.md.
4. Open research, by payoff: (0) the breakout sleeve's own record: log every trade with the fire count and regime, score at 10 trades (tests/oracle_and_good_case.md placebo is the bar); (0b) a regime gate for the breakout rule (T-bill vs policy rate) tested as a pre-registered variant, not applied live until tested; (a) the TIGHT-sector-list check the consultant describes (one hour with tests/out/walkforward_trades.csv); (b) the "investable KMI contest" the Codex critic asked for, now partly done in the rebenchmark (B2 failed); (c) dividend carry vs T-bills once pre-2024 dividends are reconstructed from announcements; (d) true size with historical share counts; (e) merge data/prices_listed_missing/ (55 listed non-panel names, incl. POL, APL, HASCOL) into the panel.
5. Every reversal of a conclusion goes to DECISIONS.md; every mistake to knowledge/lessons.md.

## Environment
- Python: .venv/Scripts/python.exe. Print with -X utf8.
- Commits: no Co-Authored-By trailer; push to origin main freely.
- PSX portal: X-Req-Id trick in CLAUDE.md. Codex: `codex exec -c 'tools.web_search=true' -C <repo> -s workspace-write -c 'approval_policy="never"' - < prompt.md`.

## Update 18 Oct 2026, late evening
Method built and exam run; see REPORT.md section 8 and knowledge/HOW_TO_THINK.md section 10. Weekly loop packaged as .claude/skills/psx-weekly/SKILL.md (copy at knowledge/SKILL_psx_weekly.md). Business-quality scores for 20 growth candidates in knowledge/companies/quality_scores.csv (MEBL 16, LUCK 15, SYS/FFC/ILP/MARI/FABL/THCCL/ISL/ENGROH 14, ... PSO and GGL 10). First live calls for the 16 Oct close: data/asof/2026-10-16/REPLY.json (method: ATRL 25, MARI 20, LUCK 15, OGDC entry 10, exposure 70) and REPLY_astra.json (peer: ATRL trend entry 15, cash 85). Next: the names and sizing conversation with Jazib, then PICKS.md v4 and frozen rows before any order; then the weekly loop runs from the skill and the scorecard becomes the exam.

## Update 18 Oct 2026, night
Short-term study done and closed (REPORT.md section 9, HOW_TO_THINK.md section 11, lesson 25): no mechanical 1 to 10 day edge after costs; the situation engine (scripts/engine.py --scan DATE) and the daily table (data/daily_table.parquet, rebuild with scripts/daily_table.py) stay as reading tools. Intraday archive started (scripts/collect_intraday.py daily after the close). Costs in data/costs.md (Finqalab's own commission still unverified; ask Jazib). Open: Jazib's sizing decision for PICKS v4; Monday 19 Oct scoring of EFERT, ATRL, MLCF rows; the weekly loop per .claude/skills/psx-weekly/SKILL.md with the engine scan added to step 3.

## Update 19 Oct 2026, early
Winners library and catalogue done (knowledge/CATALOGUE.md, knowledge/winners/, data/winners_library.csv, tests/winners_population.md); tagged scan in scripts/engine.py; skill updated with the reflex. The method is complete as a knowledge base; what remains is operation: the Monday scoring of frozen calls, the daily or weekly tagged scan, PICKS v4 with Jazib's sizes. The catalogue's own stage odds say PRL (4.2x from its low) and MACFL (5.1x) are late now; see the 2026-10-16 tagged scan.
