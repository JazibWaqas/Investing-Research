# PSX Investing Research — read this first

This repo is the memory of a research programme on how money is made on the Pakistan Stock Exchange, for Jazib, 23, Karachi, investing Rs50k a month now (Rs100k soon, Rs200k by 25 or 26), KMI All Share names only (non-negotiable), high risk appetite, aiming at financial independence by about 30. Every session, any model (Opus, Sonnet, GPT, Fable) starts cold; this file is the navigator. The programme was built 16 to 19 Oct 2026 by a Fable session with about 60 subagents; its state is final and the work from here is weekly operation plus the research listed in ORCHESTRATOR_HANDOFF.md section 10.

## Read by purpose

**Ten-minute catch-up (any session):** ORCHESTRATOR_HANDOFF.md (everything established, with every number's file), then PLAYBOOK.md (the rules on one page), then PICKS.md (current positions and triggers). That is enough to answer Jazib's questions and to run the weekly loop.

**Before giving Jazib any advice or starting any research:** knowledge/HOW_TO_THINK.md in full. It holds how he thinks and why, the ten ways the first session went wrong and the plain questions that caught each, the fourteen thinking rules, the alignment questions to ask him, and what each phase taught. Then knowledge/lessons.md (25 mistakes, each with the rule it produced). Do not launch work before mirroring your understanding back to him and getting an explicit go; he said so, and section 8 of HOW_TO_THINK explains why.

**To run the weekly or daily loop:** .claude/skills/psx-weekly/SKILL.md (invoke as /psx-weekly in Claude Code) and RUNBOOK.md. The loop: refresh data, score frozen rows, rebuild the daily table, run the tagged scan, apply the reflex (PLAYBOOK.md section B), freeze the call, log his sizes, list missed movers.

**To judge a situation or a stock:** knowledge/CATALOGUE.md (read its status box first: it is a casebook of hindsight-selected winners, not a validated system), knowledge/REGIME_TURN_PLAYBOOK.md (the one playbook worth knowing by heart), knowledge/winners/ (49 cases, 6 syntheses), knowledge/situations/ (12 dated cases), knowledge/companies/ (cards, red teams, quality scores), knowledge/sectors/ (16 notes). `scripts/engine.py SYMBOL DATE` gives the analogue odds; `scripts/engine.py --scan DATE` lists the day's movers tagged by type.

**To find a number or a verdict:** tests/FACTS.md (every test's headline numbers, verbatim), tests/BASE_RATES.csv (395 rows of odds by situation type and horizon), REPORT.md (the account of what works and what does not), then the test file itself in tests/.

**To understand why something changed:** DECISIONS.md (dated, with reasons). **To see what is pending:** HANDOFF.md.

## Rules for anyone writing here

- Point in time only. No lookahead. Results count from their announcement timestamp; after 15:30 PKT means the next session.
- Report n, mean, median, win rate, worst case, independent episodes, and a placebo of random entries with the same exits. Never a mean alone. Costs 0.5% a round trip in liquid names, 1% under Rs20m a day (data/costs.md).
- Never invent numbers. Write "unverified" or "not found". Cite source and date.
- Freeze predictions before events in catalysts/frozen_predictions.csv with a probability; append only; score in catalysts/scorecard.md.
- Consolidated EPS for groups. Adjust prices for bonus and split before returns (scripts/prices.py, method 'adjusted').
- KSE100, KMI30 and KMI All Share are total-return indices; KSE30 and KSE100PR are price indices (data/macro/INDEX_NOTES.md).
- Every knowledge file states its evidence and date. Update in place; log reversals in DECISIONS.md; add mistakes to knowledge/lessons.md.
- Files are read by humans and other models: plain prose, no session shorthand.
- Commits: no Co-Authored-By trailer. Push to origin main freely. Commit as you go.

## How to work (what the first session learned about models and orchestration)

- **Sonnet 5.5** is the default for research, tests, case studies and builds; it reports its own deviations. **Haiku 5.5** for scraping, parsing, data builds, file maps. **Opus 5.5** for audits of test designs (lookahead, survivorship, placebo), post-mortems, exam design, syntheses and anything where a wrong call is costly. **Codex gpt-6-sol** (`codex exec -m gpt-6-sol -C <repo> -s workspace-write -c 'approval_policy="never"' - < prompt.md`, add `-c 'tools.web_search=true'` for live search; `--search` is not accepted by `exec`) for independent replication and web research. **GPT-6 Astra** (`-m gpt-6-astra`) for blunt critique of a finished document; it is the best critic in the record and a cautious trader. Jazib's $20 plan limits Codex to short tasks; always have Codex write its output to a repo file so a cut-off leaves something.
- Every test gets an Opus design review before a Sonnet run, a pre-registered spec in the script header, and a placebo. Pattern mining breeds false positives; count how many of N rules would pass by chance.
- Historical replays cannot test a model's judgment: models remember 2019 to mid-2026 in detail (tests/replay_pilot_postmortem.md). Mechanical rules can be backtested; judgment is scored forward only.
- The brief shapes the agent more than the data: documents full of "no measured edge" make an agent hold cash; state the investor's posture and require a reason for any exposure below the core default (knowledge/lessons.md 23).
- Claude subagents' WebSearch has a per-agent budget that runs out; tell them to prefer WebFetch on known URLs, or use Codex for search-heavy work.
- Say in one line what is being delegated and to which model. Launch independent pieces in one message. Read summaries, not transcripts. Workflow scripts live under the session's `workflows/scripts/` folder and can be resumed with their run id.

## Environment and pipeline

- Python: `.venv\Scripts\python.exe` (3.12, uv-managed; pandas, numpy, scipy, statsmodels, pyarrow, requests, curl_cffi, lxml, bs4, pdfplumber, openpyxl, psxdata, winocr). Use `-I -X utf8` when printing (the console is cp1252; characters like the minus sign break it). Bash heredocs containing backticks or apostrophes break; write a .py file and run it.
- PSX data portal works from this machine. Every call needs header `X-Req-Id` = the `_k` value in the inline `__ps = {...}` script on any `https://dps.psx.com.pk/company/{SYM}` page, plus `X-Requested-With: XMLHttpRequest` and a Chrome User-Agent (scripts/psx_api.py does this). Endpoints: `GET /timeseries/eod/{SYM}` (5 years), `GET /timeseries/int/{SYM}` (current session ticks), `POST /historical` with `month=0&year=0&symbol=SYM` (full daily OHLCV from Oct 2016, also index codes KSE100, KSE100PR, KMI30, KMIALLSHR, KSE30), `POST /company/payouts` (about 2 years), `GET /announcements/companies` (archive to 2005), `GET /symbols`, `GET /download/document/{id}.pdf` (links can end in `.PDF`). About one request a second. Screener symbols carry XD/XB/NC suffixes; strip them.
- Blocked from this machine: nccpl.com.pk (use scstrade.com mirrors, scripts/fetch_fipi_lipi*.py), investing.com, stooq. Business Recorder sometimes returns 403. SBP and PBS need curl_cffi (scripts/cf.py).
- Rebuild order after new prices: `scripts/refresh_prices.py`, `scripts/fetch_announcements.py`, `scripts/ca/build.py` (corporate actions), `scripts/daily_table.py`, `scripts/engine.py --scan <date>`. Point-in-time packs: `scripts/asof.py <date> --check` then `scripts/replay_bundle.py <date>`; scoring: `scripts/score_replay.py --dates d1,d2`. Intraday archive: `scripts/collect_intraday.py` after each close.
- data/raw/ (filings, PDFs, macro downloads) is gitignored; data/announcements.csv too (the parquet is canonical).
- Finqalab's own commission is unverified (data/costs.md); ask Jazib.

## The investor, beyond the numbers (so no session has to re-learn it)

He wants to be taught, not told, and he wants the same for the models. He pushes back by asking plain questions ("what would Rs50k have become", "what was the best case"), not by instructing; take every such question as a test the method should already have answered. He accepts "no" with evidence; he does not accept absence, meaning a move on the screen that the system ignored. His formative trade was TRG from Rs16 on a tip from his father's friend, sold at about Rs70; his father works at Lucky Cement, so his inside view of LUCK is real information with a bias, and LUCK and other Lucky group companies (e.g. LCI) are effectively off-limits for him to buy: holding them requires a declaration through his father's employer (stated 21 Oct 2026). Never put a Lucky group name in his picks. "Money in" is not a fixed Rs50k: if a call has decent odds he will put more in. Capital gains matter, dividends do not at his scale; capital is never stuck; he takes some profit on big winners; he will go all-in on a confirmed situation within a loss budget. He does not want a master strategy; he wants an if-then library of situations, each judged on its own path, and a scorecard that says which parts work. He does not want to assign tasks endlessly: learn, then report what the learning yielded, how valuable it is, how it would be used for him, and what it now enables.
