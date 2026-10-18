# RUNBOOK.md — the weekly loop (written 17 Oct 2026; revise as tests change)

Who runs it: the orchestrator (Claude chat) with network access runs steps 1 to 4. GPT (or any research chat) runs steps 5 to 7 from the files, and emails opportunities. Either can run step 8. Nothing here needs more than an hour a week.

## 1. Refresh data (Claude, needs this machine or any Pakistani IP)

```
.venv\Scripts\python.exe scripts\refresh_prices.py        # KMI prices; delete data\prices_raw\<SYM>.csv first to force a refetch
.venv\Scripts\python.exe scripts\fetch_payouts.py          # dividends, bonus, rights for the last 2 years
.venv\Scripts\python.exe scripts\fetch_announcements.py    # resumes from the last date in data\announcements.parquet
.venv\Scripts\python.exe scripts\fetch_fipi_lipi.py        # NCCPL flows (via scstrade)
.venv\Scripts\python.exe scripts\macro_tbill.py            # SBP auctions; also policy rate after each MPC
collect_intraday.py          # after the close, every trading day: today's trades to data\intraday (portal keeps only the current session; see data\intraday\README.md)
```
The PSX portal needs the `X-Req-Id` header (CLAUDE.md, Environment). If every call returns 403, open https://dps.psx.com.pk/company/MEBL in a browser and read `window.__ps._k`; `scripts\psx_api.py` fetches it automatically.

## 2. Score what landed (Claude or GPT)

Open `catalysts\frozen_predictions.csv`. For every row whose `event_date` has passed and `outcome` is blank: find the actual (PSX announcement PDF, or the close prices in `data\prices_raw`), write 1 or 0 in `outcome`, the date in `scored_at`, and the actual number in `score_note`. Never edit `prediction`, `probability` or `reasoning`. Then update the Brier table in `catalysts\scorecard.md`. A prediction class whose Brier score stays above 0.25 after 20 rows is worse than a coin flip: stop making that class of call.

## 3. Re-run the live screens (Claude)

```
.venv\Scripts\python.exe scripts\tests\results_surprise_drift.py --screen     # ignored-quarter setups in the last 2 quarters
.venv\Scripts\python.exe scripts\tests\insider_cluster_buying.py --screen     # sponsor and director buying clusters, last 90 days
.venv\Scripts\python.exe scripts\sector_momentum.py                           # 6-month sector ranks
.venv\Scripts\python.exe scripts\screen_breakout.py                           # the breakout sleeve: names above their 252-session high, ranked; fire count
```
Sleeve maintenance, every trading day or at least weekly: for each sleeve holding, compare the last close with 80% of the highest close since entry (adjusted closes); a close below it is a sell at the next session, no exceptions. On the deposit day, buy the top-ranked breakout name not already held (max 3), else send the ticket to the core.
(If a script has no `--screen` flag yet, run it and read the "live screen" section of its output.) Paste the three screens into the week's note. Only names that pass the base rates in `tests\` (hit rate above 55% and median above costs for that signal class) go to step 5.

## 4. Update the catalyst calendar (Claude)

Append new dated events to `catalysts\catalyst_calendar.csv` with a source; mark passed events `done` in a new column rather than deleting them. Sources to check weekly, with the sector each feeds: SBP (MPC calendar, T-bill auctions: all), OGRA notifications (refiners, OMC, gas utilities), NEPRA and the Power Division (power, KEL), ECC and cabinet decisions (fertilizer gas price, refinery policy, duties), PBS CPI (regime), APCMA despatches (cement), PAMA sales (autos), NFDC offtake (fertilizer), PSX board-meeting notices (every results date), PSX "unusual movement" letters and insider disclosures (the sponsor-buying signal), SECP enforcement.

## 5. Underwrite anything new (GPT or Claude)

For each candidate from step 3 or from a catalyst in step 4, write `knowledge\companies\<SYM>.md` using the card format already in that folder: story, mispricing with consolidated numbers, dated catalysts, bear/base/bull with probabilities, killers, position plan for Rs10k to 12.5k, evidence. Then a red-team section by a different model, ending UPHELD, WEAKENED or BROKEN. A pick needs: expected 12-month return above the 12-month T-bill after 15% CGT and 0.5% costs, a dated catalyst inside 6 months, KMI All Share membership (`data\kmi_allshare_2026-06-05.csv`), median daily traded value above Rs5m.

## 6. Decide and freeze (whoever holds the pen that week)

Update `PICKS.md`: current positions, entry limits, the ranked watchlist with triggers. Every new buy, sell, or entry limit gets a row in `catalysts\frozen_predictions.csv` before the money moves (ticker, the price or EPS it depends on, the probability, the reasoning). The monthly Rs50k goes, on the same day each month, into the pick furthest below its target weight that still qualifies. Cash above 30% of the account for more than 4 weeks is a failure of the process, not prudence (lesson 13), unless the regime rule in `knowledge\playbooks\sector_rotation.md` says the market is in a hike-regime drawdown.

## 7. Email format for opportunities (GPT)

Subject: PSX: <SYM> <verdict> at Rs<price>. Body, in this order: the story in two lines; the catalyst and its date; bear/base/bull with probabilities and the rupee outcome on the suggested share count; the killer; what to do (buy now, limit at Rs X, wait for the print). Under 200 words. Link the company card.

## 8. Monthly maintenance

- Re-run `scripts\tests\size_liquidity.py` and `scripts\sector_momentum.py` after month end; append a line to `DECISIONS.md` only if a verdict changes.
- After each results season, re-run `results_surprise_drift.py` and `insider_cluster_buying.py` in full and update the base-rate table in `tests\` and the confidence scale in `knowledge\playbooks\strategy.md`.
- After every MPC: update `data\macro\policy_rate_decisions.csv`, re-check the rotation rule (CPI down two prints and 6M T-bill below the policy rate at two auctions). If it fires, that is the one macro signal with a documented 120-day payoff in both prior cycles (two episodes, so size it as a tilt, not a bet).
- Semiannually (June, December): parse the new KMI All Share list into `data\` and drop any holding that leaves it.
- Add every mistake to `knowledge\lessons.md` with the date. Add every change of conclusion to `DECISIONS.md`.
