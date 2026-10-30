# STATE.md — what is live right now

The one page that says what is true today. Sections marked "built" are generated from ledger/ by `scripts/ledger.py build` and must not be edited by hand; change the tables and rebuild. The other sections are written by the session and kept short: change what changed, delete what is finished. History never lives here: calls and outcomes are in ledger/, the reasoning of each day in journal/, course changes in DECISIONS.md.

**Updated 30 Oct 2026 by Claude Fable 5.1. Prices, announcements, the daily table and the scan are current to the 30 Oct close.**

## 1. The book (built)

<!-- ledger:holdings -->
No trades recorded. When Jazib reports a buy or sell, record it with `scripts/ledger.py trade DATE SYMBOL buy|sell QTY PRICE --fees F --call ID`, then rebuild.
<!-- /ledger:holdings -->

How calls are made: no fixed rules or splits (PLAYBOOK.md). Situations decide; every call has odds and an upside-against-downside case in rupees; he accepts a loss of up to about 30% on a call with a large upside. The open calls are in PICKS.md; the latest letter to Jazib is journal/2026-10-30-picks-v7.md (three tranches tied to events; tranche 1 on Mon 2 Nov).

Regime: hike cycle, deeper after the 26 Oct hike to 12% (next MPC 14 Dec). Brent about $116, reserves $21.5bn rising, rupee 276.8, 6-month bill 12.65%. Turn checklist 2 of 4 (rupee flat, reserves up; oil not calm, drain 15 to 19%): the September false-bottom reading, not a turn. Breadth on 30 Oct: 24% of liquid KMI names above the 200-day, 14% above the 50-day, none at a one-year high.

## 2. Decisions only Jazib can make

1. **Tranche 1 on Monday 2 Nov** (journal/2026-10-30-picks-v7.md): MEBL 28, MARI 15, ILP 100, and LUCK 25 if the declaration is acceptable. Report fills (name, shares, price, fees) for `scripts/ledger.py trade`.
2. **LUCK and the declaration.** Still unanswered. If no, LUCK's Rs10,000 goes to MEBL.
3. **What the 30% means.** Taken as per call. Tranche 1's bad case is about 21% of its Rs45,000.
4. **Score the non-Lucky cement names and ILP?** knowledge/BACKLOG.md item 3. ILP now has a position call without a full card; writing its card is the first research item when he says go.
5. **Finqalab's commission rate.** Unverified (data/costs.md); he can read it in the app.

## 3. Pending events (built)

<!-- ledger:pending -->
| event date | id | ticker | event | odds |
|---|---|---|---|---|
| 2026-11-03 | C0054 | CPI | October 2026 CPI (PBS, due 3 Nov) | 0.60 |
| 2026-11-10 | C0042 | REGIME | Regime-turn checklist (REGIME_TURN_PLAYBOOK.md) as of 19 Oct | 0.75 |
| 2026-12-01 | C0056 | KSE100 | Index level on 1 Dec 2026 against the 23 Oct low | 0.70 |
| 2026-12-01 | C0057 | TRANCHE2 | Tranche 2 released by signal (a) CPI under 10% with Brent under $105, or (b) ... | 0.45 |
| 2026-12-14 | C0053 | SAZEW | Tranche 3 (around 14 Dec): buy about Rs15,000 if the MPC holds or cuts on 14 ... | 0.35 |
| 2026-12-14 | C0055 | Policy rate | SBP MPC decision 14 Dec 2026 | 0.55 |

**Past their event date and not yet scored** (price-reaction rows score five sessions after the release): C0024 KSE100 (2026-10-26), C0015 FCCL (2026-10-27), C0018 FFC (2026-10-27), C0022 OGDC (2026-10-29)
<!-- /ledger:pending -->

Also watch: October CPI on 3 Nov (tranche 2 signal a, with Brent under $105); any oil collapse (accelerate); a KSE100 close below 162,375 or Brent above $125 (pause the remaining tranches); the 14 Dec MPC (tranche 3); the December KMI recomposition notice (late Nov). The record is in ledger/scorecard.md: 24 graded, 15 held, Brier 0.164.

## 4. Data freshness

- Prices (data/prices_raw/ and the index files in data/macro/) end **30 Oct 2026**. Weekly: `scripts/update_prices.py` (incremental; refresh_prices.py only writes missing files), then fetch_announcements, daily_table, engine --scan, ledger build.
- Announcements end 30 Oct 16:29. Daily table and the 30 Oct scan rebuilt the same day.
- Result PDFs read this session are in data/raw/filings/oct26/ (gitignored).
- The results poller (scripts/poll_results.py) is not running; poll the announcements endpoint instead.

## 5. Known gaps

- gpt/TEACHER_NOTES.md and gpt/EXAMINER_NOTES.md are 21 Oct snapshots; their notes at the top say what was superseded later that day.
- ILP has no underwriting card (only knowledge/companies/ILP_quality.md); the 30 Oct call rests on the result, the capex filing and the price reaction.
- data/fundamentals/quarterly_eps.csv has not been extended with the October 2026 results; trailing P/Es quoted on 30 Oct use the prior four quarters.
- The quarterly EPS file (data/fundamentals/quarterly_eps.csv) does not flag standalone vs consolidated.
- Unresolved research disagreements (Islamic banks at the turn; which sectors lead) are in gpt/EXAMINER_NOTES.md section 2.
