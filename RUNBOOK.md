# RUNBOOK.md — the weekly loop (written 17 Oct 2026; revised 21 Oct 2026)

Who runs it: the orchestrator (Claude chat) with network access runs steps 1 to 4. GPT (or any research chat) runs steps 5 to 7 from the files, and emails opportunities. Either can run step 8. Nothing here needs more than an hour a week.

## 1. Refresh data (Claude, needs this machine or any Pakistani IP)

```
.venv\Scripts\python.exe -I -X utf8 scripts\update_prices.py   # appends new sessions to every price file and the index files (refresh_prices.py only writes missing files)
.venv\Scripts\python.exe scripts\fetch_payouts.py          # dividends, bonus, rights for the last 2 years
.venv\Scripts\python.exe scripts\fetch_announcements.py    # resumes from the last date in data\announcements.parquet
.venv\Scripts\python.exe scripts\fetch_fipi_lipi.py        # NCCPL flows (via scstrade)
.venv\Scripts\python.exe scripts\macro_tbill.py            # SBP auctions; also policy rate after each MPC
collect_intraday.py          # after the close, every trading day: today's trades to data\intraday (portal keeps only the current session; see data\intraday\README.md)
```
The PSX portal needs the `X-Req-Id` header (CLAUDE.md, Environment). If every call returns 403, open https://dps.psx.com.pk/company/MEBL in a browser and read `window.__ps._k`; `scripts\psx_api.py` fetches it automatically.

## 2. Score what landed (Claude or GPT)

`scripts\ledger.py build` lists, in STATE.md, every open row past its `event_date`. For each: find the actual (PSX announcement PDF, or the close prices in `data\prices_raw`) and append a row to `ledger\scores.csv`: `call_id`, `scored_at`, `outcome` (1 or 0; `void` if withdrawn before entry; `not_triggered` if a conditional call never fired), and the actual number in `note`. Never edit a call row. Rebuild; `ledger\scorecard.md` recomputes the Brier table. A class of call whose Brier score stays above 0.25 after 20 rows is worse than a coin flip: say so and change how those calls are made.

## 3. Re-run the live screens (Claude)

```
.venv\Scripts\python.exe scripts\tests\results_surprise_drift.py --screen     # ignored-quarter setups in the last 2 quarters
.venv\Scripts\python.exe scripts\tests\insider_cluster_buying.py --screen     # sponsor and director buying clusters, last 90 days
.venv\Scripts\python.exe scripts\sector_momentum.py                           # 6-month sector ranks
.venv\Scripts\python.exe scripts\screen_breakout.py                           # names above their 252-session high, ranked; fire count (candidates for the reflex)
.venv\Scripts\python.exe scripts\daily_table.py && .venv\Scripts\python.exe scripts\engine.py --scan <today>   # rebuild the daily table (about 2 minutes) and list today's live situations with analogue odds
```
The standing breakout sleeve with its 20% trailing stop was dropped in PICKS v4 (DECISIONS.md, 19 Oct 2026). Breakout names are now candidates for the six-check reflex (PLAYBOOK.md section B); an opportunity position, once held, is exited only on the exit written at entry.
(If a script has no `--screen` flag yet, run it and read the "live screen" section of its output.) Paste the three screens into the week's note. Only names that pass the base rates in `tests\` (hit rate above 55% and median above costs for that signal class) go to step 5.

## 4. Update the catalyst calendar (Claude)

Append new dated events to `catalysts\catalyst_calendar.csv` with a source; mark passed events `done` in a new column rather than deleting them. Sources to check weekly, with the sector each feeds: SBP (MPC calendar, T-bill auctions: all), OGRA notifications (refiners, OMC, gas utilities), NEPRA and the Power Division (power, KEL), ECC and cabinet decisions (fertilizer gas price, refinery policy, duties), PBS CPI (regime), APCMA despatches (cement), PAMA sales (autos), NFDC offtake (fertilizer), PSX board-meeting notices (every results date), PSX "unusual movement" letters and insider disclosures (the sponsor-buying signal), SECP enforcement.

## 5. Underwrite anything new (GPT or Claude)

For each candidate from step 3 or from a catalyst in step 4, write `knowledge\companies\<SYM>.md` using the card format already in that folder: story, mispricing with consolidated numbers, dated catalysts, bear/base/bull with probabilities, killers, position plan for Rs10k to 12.5k, evidence. Then a red-team section by a different model, ending UPHELD, WEAKENED or BROKEN. A pick needs: expected 12-month return above the 12-month T-bill after 15% CGT and 0.5% costs, a dated catalyst inside 6 months, KMI All Share membership (`data\kmi_allshare_2026-06-05.csv`), median daily traded value above Rs5m.

## 6. Decide and freeze (whoever holds the pen that week)

Put PLAYBOOK.md's questions to every holding and every moving name. Each decision becomes a row in `ledger\calls.csv` before money moves (odds, rupee upside and downside on the size, what proves it wrong), with its reasoning in `journal\<today>.md`. When Jazib reports a trade, record it with `scripts\ledger.py trade`. Then `scripts\ledger.py build` rebuilds PICKS.md and the built parts of STATE.md; edit the rest of STATE.md by hand. There is no fixed split or cash limit: cash earns nothing in his account, so it has to beat the best alternative, and the reason goes in the journal.

## 7. Email format for opportunities (GPT)

Subject: PSX: <SYM> <verdict> at Rs<price>. Body, in this order: the story in two lines; the catalyst and its date; bear/base/bull with probabilities and the rupee outcome on the suggested share count; the killer; what to do (buy now, limit at Rs X, wait for the print). Under 200 words. Link the company card.

## 8. Monthly maintenance

- Re-run `scripts\tests\size_liquidity.py` and `scripts\sector_momentum.py` after month end; append a line to `DECISIONS.md` only if a verdict changes.
- After each results season, re-run `results_surprise_drift.py` and `insider_cluster_buying.py` in full and update the base-rate table in `tests\` and the confidence scale in `knowledge\playbooks\strategy.md`.
- After every MPC: update `data\macro\policy_rate_decisions.csv`, re-check the rotation rule (CPI down two prints and 6M T-bill below the policy rate at two auctions). If it fires, that is the one macro signal with a documented 120-day payoff in both prior cycles (two episodes, so size it as a tilt, not a bet).
- Semiannually (June, December): parse the new KMI All Share list into `data\` and drop any holding that leaves it.
- Add every mistake to `knowledge\lessons.md` with the date. Add every change of conclusion to `DECISIONS.md`.
