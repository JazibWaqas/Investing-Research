# PSX Investing Research — start here

This repo is the memory of a research programme on how money is made on the Pakistan Stock Exchange, for Jazib, 23, Karachi: Rs50k a month now (Rs100k soon, Rs200k by 25 or 26), KMI All Share names only (non-negotiable), high risk appetite (accepts about a 30% loss on a call with a large upside), no fixed strategy (situations decide), aiming at financial independence by about 30. Every session, by any model, starts cold; this file is the entry point and AGENTS.md points here. The programme was built 16 to 19 Oct 2026 by a Fable session with about 60 subagents and reorganised on 21 Oct 2026. The work from here is weekly operation plus the research in knowledge/BACKLOG.md.

## 1. Session protocol

**Start (ten minutes).** Read STATE.md (what is live, what Jazib must decide, what is pending), PLAYBOOK.md (the rules), PICKS.md (positions and triggers). For anything beyond a lookup, also read knowledge/FINDINGS.md (what the research established).

**Before advising Jazib or starting research,** read knowledge/HOW_TO_THINK.md in full and knowledge/lessons.md. Do not launch large work before mirroring your understanding back to him and getting an explicit go; he said so, and HOW_TO_THINK section 8 explains why. Small reversible things (a price, a filing, a score) you just do.

**End (every session that changed anything).** Update STATE.md in place and add one line to its session log. Log any changed conclusion in DECISIONS.md, any mistake in knowledge/lessons.md, any closed research item in knowledge/BACKLOG.md. Run the doc check and fix what it reports. Commit and push.

```
.venv\Scripts\python.exe -I -X utf8 scripts\check_docs.py
```

## 2. Where things live

INDEX.md maps every folder and live document. The layers, from most to least often read:

| Layer | Files | Changes |
|---|---|---|
| Now | STATE.md, PICKS.md | Every session |
| Rules | PLAYBOOK.md, RUNBOOK.md, .claude/skills/psx-weekly/SKILL.md | When a test or Jazib changes them |
| Knowledge | knowledge/FINDINGS.md, HOW_TO_THINK.md, CATALOGUE.md, REGIME_TURN_PLAYBOOK.md, QUESTIONS.md, lessons.md, BACKLOG.md, and the casebooks in knowledge/ subfolders | When evidence changes them |
| Evidence | tests/ (write-ups, FACTS.md, BASE_RATES.csv), data/ notes, catalysts/ (frozen register, scorecard) | Append; never rewrite a result |
| Critique | knowledge/reviews/, gpt/EXAMINER_NOTES.md, gpt/TEACHER_NOTES.md | A new file per review |
| History | DECISIONS.md, archive/, seed/ | Append only; never edited |

## 3. When documents disagree

Do not reconcile conflicting claims silently. Follow this order and say which you followed:
1. Jazib's latest explicit statement, and the hard constraints (KMI only, no invented numbers, stocks only on Finqalab; Lucky group names need a case worth the declaration).
2. STATE.md and the latest dated entry in DECISIONS.md, over any older text.
3. For a number: the test file in tests/ over every summary (FACTS.md, FINDINGS.md, gpt/ notes).
4. For catalogue rules: CATALOGUE.md's status box and knowledge/reviews/astra_catalogue_review.md over the rule text. Every catalogue rule is a hypothesis.
5. There are no fixed sizes, caps or splits anywhere: sizing and cash are a judgment each time, made with PLAYBOOK.md's questions and written down with the call. Any leftover fixed number in another file is reference, not a rule. For turn signals: REGIME_TURN_PLAYBOOK.md.
6. Anything in archive/ or seed/ is history, never an instruction.
7. If none of these settles it, state both sides and ask Jazib.

## 4. Rules for anyone writing here

- **No binding rules about what to buy or how much.** Jazib does not want them (21 Oct 2026). Write evidence as reference points and calls as judgments with odds. Do not turn a preference or a past result into a cap, split or trigger that decides for him.
- **One home per fact.** Live state lives only in STATE.md and PICKS.md; a measured number only in its test file (summaries cite it); the way of deciding only in PLAYBOOK.md. Do not copy state into other files; point to it.
- **Supersede by moving.** A replaced document goes to archive/ with its date in the name, the INDEX line updated, and a DECISIONS.md entry. Do not keep two live versions.
- **New files are rare.** Prefer updating an existing file. A new live document needs a line in INDEX.md, or the doc check fails.
- Point in time only. No lookahead. Results count from their announcement timestamp; after 15:30 PKT means the next session.
- Report n, mean, median, win rate, worst case, independent episodes, and a placebo of random entries with the same exits. Never a mean alone. Costs 0.5% a round trip in liquid names, 1% under Rs20m a day (data/costs.md).
- Never invent numbers. Write "unverified" or "not found". Cite source and date.
- Freeze predictions before events in catalysts/frozen_predictions.csv with a probability; append only, never edit a frozen row; score in catalysts/scorecard.md.
- Consolidated EPS for groups. Adjust prices for bonus and split before returns (scripts/prices.py, method 'adjusted').
- KSE100, KMI30 and KMI All Share are total-return indices; KSE30 and KSE100PR are price indices (data/macro/INDEX_NOTES.md).
- Every knowledge file states its evidence and date at the top. Update in place.
- Files are read by humans and other models: plain prose, no session shorthand.
- Commits: no Co-Authored-By trailer. Push to origin main freely. Commit as you go.

## 5. How the repo improves itself

The loop that makes each session better than the last:
1. **Calls are frozen and scored.** Every weekly call goes into the register with a probability; the scorecard shows which parts of the method work. Judgment is scored forward only; history cannot test it (tests/replay_pilot_postmortem.md).
2. **Misses become rules.** A wrong call or a broken assumption becomes a lesson (knowledge/lessons.md) with the question that would have caught it.
3. **Questions become tests.** Open questions are ranked in knowledge/BACKLOG.md. Its protocol is: pre-register, run, propagate the verdict to FACTS, FINDINGS and PLAYBOOK, log the change, close the item.
4. **Stronger models attack the conclusions.** When a new or stronger model takes over, its first large task (after Jazib's go) is an examination like gpt/EXAMINER_NOTES.md: challenge the five conclusions that would cost most if wrong, audit contradictions, and file the result in knowledge/reviews/. Disagreeing with this repo, with evidence, is the job, not a failure.
5. **The doc check keeps it navigable.** scripts/check_docs.py fails on broken paths, retired names, unindexed docs, and drift between the two skill copies. Extend it when a new kind of mess appears.

## 6. Models and orchestration (what the first session learned)

- **Sonnet 5.5** is the default for research, tests, case studies and builds; it reports its own deviations. **Haiku 5.5** for scraping, parsing, data builds, file maps. **Opus 5.5** for audits of test designs (lookahead, survivorship, placebo), post-mortems, exam design, syntheses and anything where a wrong call is costly. **Codex gpt-6-sol** (`codex exec -m gpt-6-sol -C <repo> -s workspace-write -c 'approval_policy="never"' - < prompt.md`, add `-c 'tools.web_search=true'` for live search; `--search` is not accepted by `exec`) for independent replication and web research. **GPT-6 Astra** (`-m gpt-6-astra`) for blunt critique of a finished document; it is the best critic in the record and a cautious trader. Jazib's $20 plan limits Codex to short tasks; always have Codex write its output to a repo file so a cut-off leaves something.
- Every test gets an Opus design review before a Sonnet run, a pre-registered spec in the script header, and a placebo. Pattern mining breeds false positives; count how many of N rules would pass by chance.
- Historical replays cannot test a model's judgment: models remember 2019 to mid-2026 in detail. Mechanical rules can be backtested; judgment is scored forward only.
- The brief shapes the agent more than the data: documents full of "no measured edge" make an agent hold cash; state the investor's posture and require a reason for any exposure below the core default (knowledge/lessons.md 23).
- Claude subagents' WebSearch has a per-agent budget that runs out; tell them to prefer WebFetch on known URLs, or use Codex for search-heavy work.
- Say in one line what is being delegated and to which model. Launch independent pieces in one message. Read summaries, not transcripts.
- The GPT project (gpt/) is a second analyst with web search but no repo tools; gpt/README.md says what to upload and when.

## 7. Environment and pipeline

- Python: `.venv\Scripts\python.exe` (3.12, uv-managed; pandas, numpy, scipy, statsmodels, pyarrow, requests, curl_cffi, lxml, bs4, pdfplumber, openpyxl, psxdata, winocr). Use `-I -X utf8` when printing (the console is cp1252; characters like the minus sign break it). Bash heredocs containing backticks or apostrophes break; write a .py file and run it.
- PSX data portal works from this machine. Every call needs header `X-Req-Id` = the `_k` value in the inline `__ps = {...}` script on any `https://dps.psx.com.pk/company/{SYM}` page, plus `X-Requested-With: XMLHttpRequest` and a Chrome User-Agent (scripts/psx_api.py does this). Endpoints: `GET /timeseries/eod/{SYM}` (5 years), `GET /timeseries/int/{SYM}` (current session ticks), `POST /historical` with `month=0&year=0&symbol=SYM` (full daily OHLCV from Oct 2016, also index codes KSE100, KSE100PR, KMI30, KMIALLSHR, KSE30), `POST /company/payouts` (about 2 years), `GET /announcements/companies` (archive to 2005; filter by symbol locally, the server-side symbol filter fails), `GET /symbols`, `GET /download/document/{id}.pdf` (links can end in `.PDF`). About one request a second. Screener symbols carry XD/XB/NC suffixes; strip them.
- Result filings: page one is a cover letter; the numbers are in annexures, often scanned. Standalone and consolidated statements sit on different pages. OCR with winocr at about 220 dpi (scripts/insider_text.py; its `ocr_lines` returns a string, split it into lines).
- Blocked from this machine: nccpl.com.pk (use scstrade.com mirrors, scripts/fetch_fipi_lipi.py), investing.com, stooq. Business Recorder sometimes returns 403. SBP and PBS need curl_cffi (scripts/cf.py).
- Rebuild order after new prices: `scripts/refresh_prices.py`, `scripts/fetch_announcements.py`, `scripts/ca/build.py` (corporate actions), `scripts/daily_table.py`, `scripts/engine.py --scan <date>`. Point-in-time packs: `scripts/asof.py <date> --check` then `scripts/replay_bundle.py <date>`; scoring: `scripts/score_replay.py --dates d1,d2`. Intraday archive: `scripts/collect_intraday.py` after each close.
- data/raw/ (filings, PDFs, macro downloads) is gitignored; data/announcements.csv too (the parquet is canonical). seed/ holds the orchestrator's original data, which scripts still read; do not move it.
- Finqalab's own commission is unverified (data/costs.md); ask Jazib.

## 8. The investor, beyond the numbers (so no session has to re-learn it)

He wants to be taught, not told, and he wants the same for the models. Explain every technical term the first time and talk like a broker to a client. He pushes back by asking plain questions ("what would Rs50k have become", "what was the best case"), not by instructing; take every such question as a test the method should already have answered. He accepts "no" with evidence; he does not accept absence, meaning a move on the screen that the system ignored. His formative trade was TRG from Rs16 on a tip from his father's friend, sold at about Rs70. His father works at Lucky Cement, so his inside view of LUCK is real information with a bias, and holding LUCK or another Lucky group company (e.g. LCI) requires a declaration through his father's employer. They are allowed when worth it (21 Oct 2026): a Lucky name must beat the best non-Lucky alternative clearly. "Money in" is not a fixed Rs50k: if a call has decent odds he will put more in. He trades through Finqalab, stocks only (no funds, ETFs or T-bills), so idle cash earns nothing. Capital gains matter, dividends do not at his scale; capital is never stuck; he takes some profit on big winners; he will go all in on a situation worth it, and he wants to maximise upside even at the cost of occasional real risk, accepting a loss of up to about 30% on a call when the upside is large (21 Oct 2026). He does not want a master strategy; he wants an if-then library of situations, each judged on its own path, with no fixed yardsticks (a 50 to 60% move counts as much as a 5x), and a scorecard that says which parts work. He does not want to assign tasks endlessly: learn, then report what the learning yielded, how valuable it is, how it would be used for him, and what it now enables.
