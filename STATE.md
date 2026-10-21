# STATE.md — what is live right now

The only file that says what is true today. Update it at the end of every session: change what changed, add one line to the session log, delete what is finished. Durable knowledge does not go here (it goes to knowledge/, tests/ or DECISIONS.md); this file stays under about two pages. Older state logs: archive/HANDOFF_2026-10-19.md.

**As of 21 Oct 2026, 20 Oct closes. Last session: Claude Opus 5.5 (continuing the Fable 5.1 programme).**

## 1. The book

- **Holdings: unknown.** No order from PICKS v4 or v5 is confirmed placed. Ask Jazib what he holds and at what prices before the next call; record it here.
- **Plan:** PICKS.md version 5. Core MEBL (after the 22 Oct result, if EPS is Rs11 or more) and MARI (Rs5,000 starter; rest at or below Rs540); a 20% reserve for the regime turn; no opportunity position qualifies today.
- **Regime:** hike cycle, not a turn. Checklist: one signal present (drain), one absent (oil calm), two unknown until about 10 Nov (knowledge/REGIME_TURN_PLAYBOOK.md section 6).

## 2. Decisions only Jazib can make

1. **The open core slot and the cash cap.** With LUCK withdrawn (not eligible), the first month would hold about 35 to 45% cash against PLAYBOOK's 25% cap. Options: put the slot into MEBL after its result; split it between MEBL and the reserve; or name a replacement first. Recommended: split between MEBL and the reserve so cash stays under 25%, then move it to a replacement once one is scored. Default if he does not answer by the 1 Nov deposit: the PICKS rule, at least half the money in the core.
2. **Scope of the Lucky restriction.** LUCK and LCI are clear. Does it cover the other listed Yunus Brothers companies, such as the group's textile companies? KOHC is not a Yunus Brothers company.
3. **Score the cement names and ILP for the open slot?** knowledge/BACKLOG.md item 3; offered 21 Oct, waiting for his yes.
4. **Is the 20% reserve acceptable to him?** Never asked directly. The argument against it is in gpt/EXAMINER_NOTES.md section 1.1.
5. **Finqalab's commission rate.** Unverified (data/costs.md); he can read it in the app.

## 3. Pending events and frozen rows

| Date | Event | Frozen row or action |
|---|---|---|
| 22 Oct 11:00 | MEBL Q3 result | EPS Rs12.50 to 15 (0.65); DPS Rs8 or more (0.60); orchestrator band 7.02 to 12.74. EPS of Rs11 or more is the buy condition |
| 26 Oct | EFERT five-session price row | Test close vs reference 194.82 |
| 26 Oct | MPC decision | Hold 0.50, +50bp 0.38, +100bp 0.10, cut 0.02. Re-run the turn checklist that evening |
| 27 Oct | FCCL result | Frozen EPS row; orchestrator band too |
| 27 to 29 Oct | FFC, OGDC, MARI results | Frozen EPS rows; MARI result checks its killers |
| 28 Oct | PRL five-session price row | Test close vs 20 Oct close 101.44; settles the orchestrator's "flat to down" leg |
| 1 Nov | Deposit day | Open-slot rule (section 2, item 1) |
| 2 Nov | October CPI | Frozen row; a second monthly fall starts the rotation rule |
| About 10 Nov | Rupee and reserves signals | Frozen "no turn by 10 Nov" at 0.75 |
| 19 Oct 2027 | Core v4 12-month rows | LUCK row voided 21 Oct by an appended row |

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

- 2026-10-21 | Opus 5.5 | Repo cleanup: root cut to the files every session needs; STATE.md, INDEX.md, knowledge/BACKLOG.md and scripts/check_docs.py added; ORCHESTRATOR_HANDOFF became knowledge/FINDINGS.md; superseded files to archive/; PICKS v5 without LUCK; stale LUCK and sizing conflicts fixed. See DECISIONS.md.
- 2026-10-21 | Opus 5.5 | gpt/ pack: PROJECT_INSTRUCTIONS, ALERT_TASKS, TEACHER_NOTES, EXAMINER_NOTES.
- 2026-10-21 | Opus 5.5 | LUCK and the Lucky group removed from eligibility; 19 to 21 Oct results scored.
- 2026-10-19 | Fable 5.1 | Programme built; final state in archive/HANDOFF_2026-10-19.md.
