# STATE.md — what is live right now

The only file that says what is true today. Update it at the end of every session: change what changed, add one line to the session log, delete what is finished. Durable knowledge does not go here (it goes to knowledge/, tests/ or DECISIONS.md); this file stays under about two pages. Older state logs: archive/HANDOFF_2026-10-19.md.

**As of 21 Oct 2026, 20 Oct closes. Last session: Claude Opus 5.5 (continuing the Fable 5.1 programme).**

## 1. The book

- **Holdings: unknown.** No order from PICKS v4 or v5 is confirmed placed. Ask Jazib what he holds and at what prices before the next call; record it here.
- **Calls:** PICKS.md version 6. MEBL after the 22 Oct result (EPS Rs11 or more); LUCK if the declaration is acceptable (the strongest turn name); MARI small now, more at or below Rs540; SAZEW on its result if no hike on 26 Oct. A suggested Rs50,000 book is in PICKS section 3; sizes are his call.
- **How calls are made:** no fixed rules or splits (PLAYBOOK.md, rewritten 21 Oct). Situations decide; every call has odds and an upside-against-downside case in rupees. He accepts a loss of up to about 30% on a call with a large upside.
- **Regime:** hike cycle, not a turn. Checklist: one signal present (drain), one absent (oil calm), two unknown until about 10 Nov (knowledge/REGIME_TURN_PLAYBOOK.md section 6).

## 2. Decisions only Jazib can make

1. **LUCK and the declaration.** Lucky group names are allowed when worth it (21 Oct). Is the declaration acceptable for a position of about Rs15,000, the size suggested in PICKS? If yes, re-freeze a LUCK row before buying (the 19 Oct row was voided).
2. **The next deposit.** PICKS section 3 suggests MEBL, LUCK, MARI and Rs10,000 held to 26 Oct for SAZEW. His sizes go here once he decides.
3. **Score the non-Lucky cement names and ILP?** knowledge/BACKLOG.md item 3; offered 21 Oct, waiting for his yes.
4. **What the 30% means.** Taken as: he accepts losing up to about 30% of the money in a call when the upside is large. If he meant the whole book in a bad year, the suggested book already fits (about 22 to 25% in its bad case).
5. **Finqalab's commission rate.** Unverified (data/costs.md); he can read it in the app.

## 3. Pending events and frozen rows

| Date | Event | Frozen row or action |
|---|---|---|
| 22 Oct 11:00 | MEBL Q3 result | EPS Rs12.50 to 15 (0.65); DPS Rs8 or more (0.60); orchestrator band 7.02 to 12.74. EPS of Rs11 or more is the buy condition |
| 26 Oct | EFERT five-session price row | Test close vs reference 194.82 |
| 26 Oct | MPC decision | Hold 0.50, +50bp 0.38, +100bp 0.10, cut 0.02. Re-run the turn checklist that evening |
| 27 Oct | FCCL result | Frozen EPS row; orchestrator band too |
| 27 to 29 Oct | FFC, OGDC, MARI, LUCK results | Frozen EPS rows; the MARI and LUCK results check their killers |
| 28 Oct | PRL five-session price row | Test close vs 20 Oct close 101.44; settles the orchestrator's "flat to down" leg |
| 1 Nov | Deposit day | Sizes per section 2, item 2 |
| 2 Nov | October CPI | Frozen row; a second monthly fall starts the rotation rule |
| About 10 Nov | Rupee and reserves signals | Frozen "no turn by 10 Nov" at 0.75 |
| 19 Oct 2027 | Core v4 12-month rows (MEBL, MARI) | The LUCK row was voided on 21 Oct; re-freeze if he buys |

Scored so far: 8 of 8, Brier 0.092, mostly easy rows (catalysts/scorecard.md). The ATRL conditional entry did not trigger.

## 4. Data freshness

- data/prices_raw/ ends **16 Oct 2026**. The 19 and 20 Oct closes were fetched for scoring but not written. Run scripts/refresh_prices.py before any computation.
- Announcements, corporate actions, the daily table and the engine scan are also as of 16 Oct; rebuild in the order in CLAUDE.md.
- The results poller (scripts/poll_results.py) is not running and its page fetch returns only the HTML shell; poll the announcements endpoint instead.
- Result PDFs read so far are in data/raw/filings/results/ (gitignored).

## 5. Known gaps in the documents

- gpt/TEACHER_NOTES.md and gpt/EXAMINER_NOTES.md are dated snapshots (21 Oct). Their section on contradictions was resolved by the 21 Oct cleanup except where STATE.md section 2 still lists a decision.
- The quarterly EPS file (data/fundamentals/quarterly_eps.csv) does not flag standalone vs consolidated.
- Unresolved research disagreements (Islamic banks at the turn; which sectors lead) are listed in gpt/EXAMINER_NOTES.md section 2 and stay open until the evidence changes.

## 6. Session log (newest first; one line each)

- 2026-10-21 | Opus 5.5 | Fixed rules removed at Jazib's request: PLAYBOOK rewritten as a decision guide (situations decide, odds on every call, upside against downside, about 30% downside accepted); PICKS v6 as calls with odds; Lucky group allowed when worth the declaration; caps and splits removed from the regime playbook, catalogue, skill and GPT pack.
- 2026-10-21 | Opus 5.5 | Repo cleanup: root cut to the files every session needs; STATE.md, INDEX.md, knowledge/BACKLOG.md and scripts/check_docs.py added; ORCHESTRATOR_HANDOFF became knowledge/FINDINGS.md; superseded files to archive/; PICKS v5 without LUCK; stale LUCK and sizing conflicts fixed. See DECISIONS.md.
- 2026-10-21 | Opus 5.5 | gpt/ pack: PROJECT_INSTRUCTIONS, ALERT_TASKS, TEACHER_NOTES, EXAMINER_NOTES.
- 2026-10-21 | Opus 5.5 | LUCK and the Lucky group removed from eligibility; 19 to 21 Oct results scored.
- 2026-10-19 | Fable 5.1 | Programme built; final state in archive/HANDOFF_2026-10-19.md.
