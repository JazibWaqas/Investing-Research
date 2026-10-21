# STATE.md — what is live right now

The one page that says what is true today. Sections marked "built" are generated from ledger/ by `scripts/ledger.py build` and must not be edited by hand; change the tables and rebuild. The other sections are written by the session and kept short: change what changed, delete what is finished. History never lives here: calls and outcomes are in ledger/, the reasoning of each day in journal/, course changes in DECISIONS.md.

**Written 21 Oct 2026 by Claude Opus 5.5. Prices in the repo end 16 Oct (section 4).**

## 1. The book (built)

<!-- ledger:holdings -->
No trades recorded. When Jazib reports a buy or sell, record it with `scripts/ledger.py trade DATE SYMBOL buy|sell QTY PRICE --fees F --call ID`, then rebuild.
<!-- /ledger:holdings -->

How calls are made: no fixed rules or splits (PLAYBOOK.md). Situations decide; every call has odds and an upside-against-downside case in rupees; he accepts a loss of up to about 30% on a call with a large upside. The open calls are in PICKS.md; the latest letter to Jazib is journal/2026-10-21-picks-v6.md.

Regime: hike cycle, not a turn. Checklist: one signal present (drain), one absent (oil calm), two unknown until about 10 Nov (knowledge/REGIME_TURN_PLAYBOOK.md section 6).

## 2. Decisions only Jazib can make

1. **LUCK and the declaration.** Lucky group names are allowed when worth it. Is the declaration acceptable for about Rs15,000 of LUCK (call C0044)?
2. **The next deposit.** The v6 letter suggests MEBL, LUCK, MARI and Rs10,000 held to 26 Oct for SAZEW. When he buys or sells, record each trade with `scripts/ledger.py trade`.
3. **Score the non-Lucky cement names and ILP?** knowledge/BACKLOG.md item 3; offered 21 Oct, waiting for his yes.
4. **What the 30% means.** Taken as: he accepts losing up to about 30% of the money in a call when the upside is large. If he meant the whole book in a bad year, the suggested book already fits (about 22 to 25% in its bad case).
5. **Finqalab's commission rate.** Unverified (data/costs.md); he can read it in the app.

## 3. Pending events (built)

<!-- ledger:pending -->
| event date | id | ticker | event | odds |
|---|---|---|---|---|
| 2026-10-22 | C0009 | MEBL | Q3 CY26 standalone EPS (board 22 Oct 11:00, confirmed PSX 285467) | 0.65 |
| 2026-10-22 | C0010 | MEBL | Q3 CY26 EPS vs frozen band | 0.22 |
| 2026-10-22 | C0011 | MEBL | Q3 CY26 interim dividend | 0.6 |
| 2026-10-22 | C0012 | MEBL | Price reaction to Q3 CY26 results | 0.48 |
| 2026-10-26 | C0023 | Policy rate | SBP MPC decision | 0.5 |
| 2026-10-26 | C0024 | KSE100 | Market direction after MPC | 0.52 |
| 2026-10-27 | C0013 | FCCL | Q1 FY27 EPS (board 27 Oct 10:30, confirmed PSX 284522) | 0.55 |
| 2026-10-27 | C0014 | FCCL | Q1 FY27 entitlement | 0.93 |
| 2026-10-27 | C0015 | FCCL | Price reaction to Q1 FY27 results | 0.47 |
| 2026-10-27 | C0016 | FFC | Q3 CY26 consolidated EPS (board date NOT confirmed; no PSX notice as of 16 Oc... | 0.65 |
| 2026-10-27 | C0017 | FFC | Q3 CY26 third interim dividend | 0.65 |
| 2026-10-27 | C0018 | FFC | Price reaction to Q3 CY26 results | 0.45 |
| 2026-10-29 | C0019 | OGDC | Q1 FY27 standalone EPS (board about 29 Oct, NO PSX notice as of 16 Oct; last ... | 0.62 |
| 2026-10-29 | C0020 | OGDC | Q1 FY27 EPS vs frozen bull | 0.82 |
| 2026-10-29 | C0021 | OGDC | Q1 FY27 interim dividend | 0.65 |
| 2026-10-29 | C0022 | OGDC | Price reaction to Q1 FY27 results | 0.45 |
| 2026-10-30 | C0047 | SAZEW | PICKS v6: buy about Rs10,000 on its Q1 FY27 result if EPS is Rs60 or more and... | 0.20 |
| 2026-11-10 | C0042 | REGIME | Regime-turn checklist (REGIME_TURN_PLAYBOOK.md) as of 19 Oct | 0.75 |

**Past their event date and not yet scored** (price-reaction rows score five sessions after the release): C0004 EFERT (2026-10-19), C0006 PRL (2026-10-20), C0008 PRL (2026-10-20)
<!-- /ledger:pending -->

Also watch: the MPC on 26 Oct (re-run the turn checklist that evening), the 1 Nov deposit, October CPI on 2 Nov (a second monthly fall would be the first rotation signal). The record so far is in ledger/scorecard.md.

## 4. Data freshness

- data/prices_raw/ ends **16 Oct 2026**. The 19 and 20 Oct closes were fetched for scoring but not written. Run scripts/refresh_prices.py before any computation, then rebuild the ledger pages.
- Announcements, corporate actions, the daily table and the engine scan are also as of 16 Oct; rebuild in the order in CLAUDE.md.
- The results poller (scripts/poll_results.py) is not running and its page fetch returns only the HTML shell; poll the announcements endpoint instead.
- Result PDFs read so far are in data/raw/filings/results/ (gitignored).

## 5. Known gaps

- gpt/TEACHER_NOTES.md and gpt/EXAMINER_NOTES.md are 21 Oct snapshots; their notes at the top say what was superseded later that day.
- The quarterly EPS file (data/fundamentals/quarterly_eps.csv) does not flag standalone vs consolidated.
- Unresolved research disagreements (Islamic banks at the turn; which sectors lead) are in gpt/EXAMINER_NOTES.md section 2.
