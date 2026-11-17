# STATE.md — what is live right now

The one page that says what is true today. Sections marked "built" are generated from ledger/ by `scripts/ledger.py build` and must not be edited by hand; change the tables and rebuild. The other sections are written by the session and kept short: change what changed, delete what is finished. History never lives here: calls and outcomes are in ledger/, the reasoning of each day in journal/, course changes in DECISIONS.md.

**Updated 17 Nov 2026 by Claude Opus 5.5. Prices and announcements are current to the 17 Nov close. Regime: Brent about $91 to $93, October CPI 9.6%, KSE100 177,518 and 3.9% above its 200-day, breadth 45% above the 200-day and 61% above the 50-day; a shock-reversal turn (lesson 27) consolidating for a week. Jazib's Finqalab account is active; the Lucky restriction is off (17 Nov).**

## 1. The book (built)

<!-- ledger:holdings -->
No trades recorded. When Jazib reports a buy or sell, record it with `scripts/ledger.py trade DATE SYMBOL buy|sell QTY PRICE --fees F --call ID`, then rebuild.
<!-- /ledger:holdings -->

How calls are made: no fixed rules or splits (PLAYBOOK.md). Situations decide; every call has odds and an upside-against-downside case in rupees; he accepts a loss of up to about 30% on a call with a large upside. The open calls are in PICKS.md; the latest letter to Jazib is journal/2026-11-17-picks-v9.md (a four-week swing book into the 14 Dec MPC, with targets, stops and an 18 Dec time exit).

Regime: policy rate 12% (next MPC 14 Dec; C0066 hold 0.55, cut 0.30, hike 0.15). The market turned on the oil reversal, not on the checklist (journal/2026-11-10.md). Jazib wants a weeks-long swing book, not year-long holds (17 Nov).

## 2. Decisions only Jazib can make

1. **The core (18 Nov, journal/2026-11-18.md):** FCCL Rs15,000 (C0093), OGDC Rs15,000 (C0094), FFC Rs20,000 (C0101), held through dips, exit only if a case breaks; ILP dropped after its report (C0100). High reward Rs25,000, three re-rating stories: GHNI Rs10,000 (C0107), NETSOL Rs7,500 (C0112, replacing MLCF to cut cement weight), LUCK Rs7,500 (C0109), each with a 25% trailing exit; GAL and PPL passed. Report fills for `scripts/ledger.py trade`.
2. **Run the exits.** Sell at a target (all, or half with the stop moved to cost); sell the morning after a close below a stop. Message on Brent above $105.
3. **SAZEW only on company evidence** (C0088): four-wheeler sales above 1,600 a month, a hybrid concession in the auto policy, or Rs1,200 or below. The 1QFY27 report confirmed the Avoid (knowledge/companies/SAZEW.md).
4. **Finqalab's commission rate.** Unverified (data/costs.md); he can read it on his first contract note.

## 3. Pending events (built)

<!-- ledger:pending -->
| event date | id | ticker | event | odds |
|---|---|---|---|---|
| 2026-12-01 | C0065 | KSE100 | Index level on 1 Dec 2026 against the 23 Oct low | 0.92 |
| 2026-12-14 | C0066 | Policy rate | SBP MPC decision 14 Dec 2026 | 0.55 |
| 2026-12-18 | C0076 | MEBL | Not in the swing book |  |
| 2026-12-18 | C0083 | MARI | Out of the swing book after the deeper check |  |
| 2026-12-31 | C0048 | SYS | PICKS v6: buy at or below Rs100, or on its first close above the 50-day avera... | 0.25 |
<!-- /ledger:pending -->

Also watch: November CPI (early Dec; SAZEW trigger); Brent above $105 (the swing setup failing); the 14 Dec MPC; the December KMI recomposition notice (late Nov). The record is in ledger/scorecard.md: 24 graded, 15 held, Brier 0.164.

## 4. Data freshness

- Prices (data/prices_raw/ and the index files in data/macro/) end **17 Nov 2026** (close). Weekly: `scripts/update_prices.py` (incremental; refresh_prices.py only writes missing files), then fetch_announcements, daily_table, engine --scan, ledger build. Non-KMI files (HBL, UBL, MCB, INDU, POL, TRG) end 16 Oct: the updater reads the KMI list.
- Announcements end 17 Nov. The daily table and engine scan were last built on 10 Nov (partial session); rebuild before the next scan.
- Filing PDFs read this session: data/raw/filings/nov26/ (gitignored).
- Brent and the week's KSE100 closes are from web reports on 17 Nov (journal/2026-11-17.md); reserves and USD/PKR for November are unverified.

## 5. Known gaps

- gpt/TEACHER_NOTES.md and gpt/EXAMINER_NOTES.md are 21 Oct snapshots; their notes at the top say what was superseded later that day.
- ILP has no underwriting card (only knowledge/companies/ILP_quality.md); the 30 Oct call rests on the result, the capex filing and the price reaction.
- data/fundamentals/quarterly_eps.csv has not been extended with the October 2026 results; trailing P/Es quoted on 30 Oct use the prior four quarters.
- The quarterly EPS file (data/fundamentals/quarterly_eps.csv) does not flag standalone vs consolidated.
- Unresolved research disagreements (Islamic banks at the turn; which sectors lead) are in gpt/EXAMINER_NOTES.md section 2.
