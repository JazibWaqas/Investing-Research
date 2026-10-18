# PSX Investing Research — knowledge base

This repo is the memory of a research program on how money is made on the Pakistan Stock Exchange, for a 22-year-old Karachi investor with Rs50k now and Rs50k a month, KMI All Share names only, high risk appetite. Any model (Claude, GPT, other) starting a fresh session should read, in order (and should not launch work before mirroring its understanding back to the user and getting an explicit go):

0. `knowledge/HOW_TO_THINK.md` — how this investor thinks, how the research went wrong and was corrected, the thinking rules, and the questions to ask him. Read it first and whole; it is the lens for everything below.
1. `REPORT.md` — the model of how money is made on PSX, with evidence. If it does not exist yet, read `PLAN.md`.
2. `PICKS.md` — current positions and watchlist, frozen with probabilities.
3. `knowledge/lessons.md` — mistakes already made. Do not repeat them.
4. `catalysts/catalyst_calendar.csv` and `catalysts/frozen_predictions.csv` — what is coming, what we predicted.
5. `RUNBOOK.md` — the weekly loop.

Deeper material: `knowledge/sectors/` (one file per sector: levers, current state, exposed names), `knowledge/playbooks/` (one file per way money is made), `tests/` (one file per backtest, with n, median, win rate, worst case), `DECISIONS.md` (why the plan changed), `seed/` (the original orchestrator brief and data, read-only).

## Rules for anyone writing here

- Point in time only. No lookahead. Results count after their announcement timestamp.
- Report n, mean, median, win rate, worst case. Never mean alone.
- Never invent numbers. Write "unverified" or "not found". Cite source and date.
- Freeze predictions before events in `catalysts/frozen_predictions.csv`. Append only.
- Use consolidated EPS for groups. Adjust prices for bonus and split before returns.
- Every knowledge file states its evidence and its date. Update in place; log the change in `DECISIONS.md` if it reverses a conclusion.
- Write normal prose in files. Files are read by humans and other models.

## Environment

- Python: `.venv/Scripts/python.exe` (3.12, uv-managed). Packages: pandas, numpy, requests, curl_cffi, psxdata, lxml, bs4, pdfplumber, openpyxl, scipy, statsmodels, matplotlib, pyarrow.
- PSX data portal API works from this machine. See `scripts/psx_api.py`. The trick: send header `X-Req-Id` with the value of `window.__ps._k` found in any `https://dps.psx.com.pk/company/{SYMBOL}` page, plus `X-Requested-With: XMLHttpRequest` and a Chrome User-Agent. Endpoints: `GET /timeseries/eod/{SYM}` (5 years), `GET /timeseries/int/{SYM}`, `POST /historical` with `month=0&year=0&symbol=SYM` (full daily OHLCV from Oct 2016, HTML table), `POST /company/payouts`, `GET /announcements/companies`, `GET /symbols`, `GET /download/document/{id}.pdf`. About 1 request per second.
