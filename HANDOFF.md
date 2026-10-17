# HANDOFF.md — state of the program (18 Oct 2026, 13:30 PKT)

Deliverables are complete: REPORT.md, PICKS.md (v2), RUNBOOK.md, sector_map.md, catalysts/ (calendar, dividend calendar, 33 frozen predictions, scorecard), knowledge/ (16 sector notes, 13 company cards with red teams, 10 playbooks incl. strategy, deals, holdco discounts, catalyst trade, practitioner signals, critic and consultant reviews), tests/ (14 test write-ups plus FACTS.md), data/ and scripts/ as documented in CLAUDE.md. Everything is committed and pushed to origin main.

## Still running when this was written
- Active trading study (workflow wf_f22862e1-2dc): tests/fixed_capital_runs.md, oracle_and_good_case.md, winners_case_control.md, then knowledge/playbooks/active_trading.md and a DECISIONS.md entry. Plus a Codex replication (knowledge/playbooks/active_trading_codex.md). When they land: revise PICKS.md satellite rules and strategy.md if an active sleeve is supported; update REPORT.md section 1.
- Full insider-trade extraction 2019 to 2026 (fixes the .PDF case bug in the scraper, OCRs scanned filings, rebuilds data/insider_trades.csv, re-runs tests/insider_cluster_buying.md as "run 2"). When it lands: commit it, update the sponsor-buying trigger line in PICKS.md with the measured base rate, and add a DECISIONS.md line.

## What to do next, in order
1. Monday 19 Oct: place the three core orders in PICKS.md. Score EFERT, ATRL and MLCF rows in catalysts/frozen_predictions.csv after the close (RUNBOOK step 2). Tuesday: PRL (after 15:00 board), EPCL. Wednesday: MEBL, FABL. 26 Oct: MPC. 27 to 29 Oct: FCCL, FFC, OGDC.
2. After each result, check the killers in the company cards; a fired killer means the next deposit's add limit tightens (PICKS.md, second deposit).
3. Weekly: RUNBOOK.md. Monthly: the Rs50k split 75/25 per PICKS.md.
4. Open research, by payoff: (a) the TIGHT-sector-list check the consultant describes (one hour with tests/out/walkforward_trades.csv); (b) the "investable KMI contest" the Codex critic asked for, now partly done in the rebenchmark (B2 failed); (c) dividend carry vs T-bills once pre-2024 dividends are reconstructed from announcements; (d) true size with historical share counts; (e) merge data/prices_listed_missing/ (55 listed non-panel names, incl. POL, APL, HASCOL) into the panel.
5. Every reversal of a conclusion goes to DECISIONS.md; every mistake to knowledge/lessons.md.

## Environment
- Python: .venv/Scripts/python.exe. Print with -X utf8.
- Commits: no Co-Authored-By trailer; push to origin main freely.
- PSX portal: X-Req-Id trick in CLAUDE.md. Codex: `codex exec -c 'tools.web_search=true' -C <repo> -s workspace-write -c 'approval_policy="never"' - < prompt.md`.
