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

1. **Buy on 18 Nov** (journal/2026-11-17-picks-v9.md): LUCK 56 at 442, MARI 28 at 715 (up to 730 after two sessions), FCCL 250 at 60, PAEL 420 at 35.80; about Rs75,000. Each has a target, a stop on the close and an 18 Dec time exit (C0071 to C0074). Report fills (name, shares, price, fees) for `scripts/ledger.py trade`.
2. **Run the exits.** Sell at a target (all, or half with the stop moved to cost); sell the morning after a close below a stop. Message on Brent above $105.
3. **SAZEW after the November CPI** (early Dec), if CPI is under 9% and Brent under $100 (C0075).
4. **Finqalab's commission rate.** Unverified (data/costs.md); he can read it on his first contract note.

## 3. Pending events (built)

<!-- ledger:pending -->
| event date | id | ticker | event | odds |
|---|---|---|---|---|
| 2026-12-01 | C0065 | KSE100 | Index level on 1 Dec 2026 against the 23 Oct low | 0.92 |
| 2026-12-14 | C0066 | Policy rate | SBP MPC decision 14 Dec 2026 | 0.55 |
| 2026-12-18 | C0071 | LUCK | Swing into the 14 Dec MPC: Rs25,000, 56 shares, limit Rs442. Target Rs490, st... | 0.55 |
| 2026-12-18 | C0072 | MARI | Swing: Rs20,000, 28 shares, limit Rs715 (pay up to Rs730 if unfilled in two s... | 0.50 |
| 2026-12-18 | C0073 | FCCL | Swing: Rs15,000, 250 shares, limit Rs60. Target Rs68, stop a close below Rs54... | 0.55 |
| 2026-12-18 | C0074 | PAEL | Swing: Rs15,000, 420 shares, limit Rs35.80. Target Rs42, stop a close below R... | 0.50 |
| 2026-12-18 | C0075 | SAZEW | Buy 10 shares (Rs15,000) after the November CPI release (early Dec) if CPI is... | 0.50 |
| 2026-12-18 | C0076 | MEBL | Not in the swing book |  |
| 2026-12-18 | C0077 | ILP | Not in the swing book |  |
| 2026-12-18 | C0078 | MLCF | Not in the swing book |  |
| 2026-12-18 | C0079 | PORTFOLIO | The 17 Nov swing book (LUCK 56, MARI 28, FCCL 250, PAEL 420 at the limits, ex... | 0.50 |
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
