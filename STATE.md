# STATE.md — what is live right now

The one page that says what is true today. Sections marked "built" are generated from ledger/ by `scripts/ledger.py build` and must not be edited by hand; change the tables and rebuild. The other sections are written by the session and kept short: change what changed, delete what is finished. History never lives here: calls and outcomes are in ledger/, the reasoning of each day in journal/, course changes in DECISIONS.md.

**Updated 10 Nov 2026 by Claude Fable 5.1. Prices and announcements are current to the 10 Nov morning session (market open; 10 Nov rows partial). Regime: oil about $92 (from $116), October CPI 9.6%, KSE100 about 177,500 and 3.7% above its 200-day, breadth 43% above the 200-day; a shock-reversal turn (lesson 27), not a checklist turn.**

## 1. The book (built)

<!-- ledger:holdings -->
No trades recorded. When Jazib reports a buy or sell, record it with `scripts/ledger.py trade DATE SYMBOL buy|sell QTY PRICE --fees F --call ID`, then rebuild.
<!-- /ledger:holdings -->

How calls are made: no fixed rules or splits (PLAYBOOK.md). Situations decide; every call has odds and an upside-against-downside case in rupees; he accepts a loss of up to about 30% on a call with a large upside. The open calls are in PICKS.md; the latest letter to Jazib is journal/2026-10-30-picks-v7.md (three tranches tied to events; tranche 1 on Mon 2 Nov).

Regime: hike cycle, deeper after the 26 Oct hike to 12% (next MPC 14 Dec). Brent about $116, reserves $21.5bn rising, rupee 276.8, 6-month bill 12.65%. Turn checklist 2 of 4 (rupee flat, reserves up; oil not calm, drain 15 to 19%): the September false-bottom reading, not a turn. Breadth on 30 Oct: 24% of liquid KMI names above the 200-day, 14% above the 50-day, none at a one-year high.

## 2. Decisions only Jazib can make

1. **Buy now, 10 or 11 Nov** (journal/2026-11-10-picks-v8.md): MEBL 27 at 570, ILP 145 at 105, MARI 15 at 670, LUCK 22 at 450 if the declaration is acceptable or MLCF 95 at 106, FCCL 160 at 62 as an optional swing with its exit written (C0064). About Rs60,000; hold about Rs50,000 for 14 Dec. The 2 Nov plan was never executed. Report fills (name, shares, price, fees) for `scripts/ledger.py trade`.
2. **LUCK and the declaration.** Still unanswered. If no, MLCF is the cement.
3. **FCCL swing or not.** Optional; only if he will act on the written exit.
4. **Cards for MLCF and ILP** (knowledge/BACKLOG.md item 3): both now carry position calls without full underwriting; first research item when he says go.
5. **Finqalab's commission rate.** Unverified (data/costs.md); he can read it in the app.

## 3. Pending events (built)

<!-- ledger:pending -->
| event date | id | ticker | event | odds |
|---|---|---|---|---|
| 2026-12-01 | C0065 | KSE100 | Index level on 1 Dec 2026 against the 23 Oct low | 0.92 |
| 2026-12-14 | C0053 | SAZEW | Tranche 3 (around 14 Dec): buy about Rs15,000 if the MPC holds or cuts on 14 ... | 0.35 |
| 2026-12-14 | C0066 | Policy rate | SBP MPC decision 14 Dec 2026 | 0.55 |
<!-- /ledger:pending -->

Also watch: October CPI on 3 Nov (tranche 2 signal a, with Brent under $105); any oil collapse (accelerate); a KSE100 close below 162,375 or Brent above $125 (pause the remaining tranches); the 14 Dec MPC (tranche 3); the December KMI recomposition notice (late Nov). The record is in ledger/scorecard.md: 24 graded, 15 held, Brier 0.164.

## 4. Data freshness

- Prices (data/prices_raw/ and the index files in data/macro/) end **10 Nov 2026, morning session** (partial day). Weekly: `scripts/update_prices.py` (incremental; refresh_prices.py only writes missing files), then fetch_announcements, daily_table, engine --scan, ledger build. Non-KMI files (HBL, UBL, MCB, INDU, POL, TRG) end 16 Oct: the updater reads the KMI list.
- Announcements end 10 Nov. The daily table and scan for 10 Nov were started in the background on 10 Nov; rerun if STATE and the scan disagree.
- Filing PDFs read this session: data/raw/filings/nov26/ (gitignored).
- Oil, CPI and the rupee are from web sources on 10 Nov (journal/2026-11-10.md); reserves and USD/PKR for November are unverified.

## 5. Known gaps

- gpt/TEACHER_NOTES.md and gpt/EXAMINER_NOTES.md are 21 Oct snapshots; their notes at the top say what was superseded later that day.
- ILP has no underwriting card (only knowledge/companies/ILP_quality.md); the 30 Oct call rests on the result, the capex filing and the price reaction.
- data/fundamentals/quarterly_eps.csv has not been extended with the October 2026 results; trailing P/Es quoted on 30 Oct use the prior four quarters.
- The quarterly EPS file (data/fundamentals/quarterly_eps.csv) does not flag standalone vs consolidated.
- Unresolved research disagreements (Islamic banks at the turn; which sectors lead) are in gpt/EXAMINER_NOTES.md section 2.
