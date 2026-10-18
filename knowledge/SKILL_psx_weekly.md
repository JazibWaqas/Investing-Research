---
name: psx-weekly
description: Run the weekly PSX judgment loop for Jazib: build the as-of pack, make the frozen call, score last weeks' calls
---

# psx-weekly

Run from the repo root. Never commit or push unless Jazib says so. Never print credentials.

## 1. What this is

This is the method in `knowledge\HOW_TO_THINK.md` run as a weekly loop. Each run builds the same point-in-time pack and brief (v2) that the replay exam used, makes one frozen call, and scores the calls that have matured. The output is the live exam.

The live scorecard is the only valid test. A model that read the internet up to its cutoff cannot be replayed on past dates without memory leaking in (lesson 22; replay post-mortem section 1). Frozen calls on dates after the model's cutoff cannot be contaminated. Nothing before the scorecard matures proves skill. Say so to Jazib when he asks whether the method works.

## 2. Before the call

Read, in this order:
1. `knowledge\HOW_TO_THINK.md` sections 2 (the investor) and 6 (thinking rules).
2. `knowledge\QUESTIONS.md` (A regime, B business, C situation, D self-check).
3. The last two `data\asof\<date>\REPLY.json` files.
4. `catalysts\frozen_predictions.csv`, open rows only (blank `outcome`).
5. `knowledge\companies\quality_scores.csv`, if it exists.

Then build the pack. `<today>` is the session date, a trading day, as YYYY-MM-DD:

```
.venv\Scripts\python.exe -I scripts\asof.py <today> --check
.venv\Scripts\python.exe -I scripts\replay_bundle.py <today>
```

Refresh data first if stale (RUNBOOK.md step 1). Read `data\asof\<today>\BUNDLE.md` in full. It holds the brief v2, the schema and the method documents. If `--check` fails, stop and fix the data before calling.

## 3. The call

Follow the brief v2 in the bundle exactly: its forbidden list, the [P] risk budget (per entry size x (entry - stop) / entry <= 5, sum <= 10), the posture block, the schema and the citation rule. Every fact cites the pack; every mechanism cites a method file. Live, there is no future to leak, but still report anything you "remember" from outside the pack in `contamination_note`.

Additions from the Astra review (`knowledge\playbooks\astra_peer_review.md`, section c):

- **State the investible default portfolio.** The current core at about 75% exposure. Cash is a competitor, not a refuge: any deviation from the default, cash included, must beat the next-best eligible use of capital on payoff, horizon and stressed loss. Do not force trades and do not invent precision to fit the posture.
- **Cite base rates in three separate bins:** "not tested" (no measurement), "imprecisely estimated" (small n or wide interval; give n and median), and "evidence against" (measured and unfavourable). None means automatic cash, and none licenses an invented edge. Signals that share one cause count once.
- **Every situation card has:** mechanism; what the price already implies; base-rate limits; confirming evidence; falsifier; entry valuation; execution constraint (liquidity, locks, gap risk); exit; and a decision (buy, add, hold, reduce, exit, pass) with an amount in rupees or percent and a reason.
- **Every watch item names the observation** that converts it to an order (a print, a notification, a close above a level, a volume threshold).
- **Size against stressed portfolio loss and correlated exposure** (same sector, same macro driver, same sponsor), not stop distance alone. Stops fail on gaps and upper or lower locks. State the stressed loss in percent of book.
- **Exits differ by type.** Compounders: exit on a broken thesis or a better use of capital, not on price noise. Shocks: exit into the rebound on a time and distance target. Deals: exit on the deal's terms, falsified by a regulatory or financing break. Momentum: trailing stop on closes.

Record the call:
1. Write `data\asof\<today>\REPLY.json` (one JSON object, brief schema, nothing else).
2. Append one row per decision to `catalysts\frozen_predictions.csv`, same columns as existing rows: ticker, event, prediction, probability, reasoning (plus `frozen_at`, `event_date`; leave outcome fields blank). Put the full model ID and the brief and bundler commit hashes in the first row's reasoning for the week.
3. Add a prospectively defined candidate set: every screened name with any signal this week (screens.csv signals, insider clusters, ignored-quarter setups, upper-lock volume), each with a pass or act decision and a probability. This lets omissions be scored later against a list fixed in advance.

Never edit `prediction`, `probability` or `reasoning` after freezing.

## 4. The conversation with Jazib

Present the call as a broker would, not as JSON:
- the story in two lines and the mispricing;
- catalysts with dates;
- bear, base and bull outcomes in rupees on his actual share count, with probabilities;
- dividends net of 15% tax;
- the killers (what makes it wrong) and the stressed portfolio loss.

State the default portfolio first and what you propose to change from it. Then let him set sizes. He decides; you do not lobby. Ask for what you do not know (his current cash, deposits, holdings). Log his final sizes in the frozen file (an added row marked "Jazib final") before any order is placed. Where his size differs from yours, both are scored: his as the actual, yours as the method.

## 5. Scoring

Every week:

```
.venv\Scripts\python.exe -I scripts\score_replay.py --dates <comma list of every date older than 60 sessions>
```

Also fill `outcome`, `scored_at`, `score_note` on matured rows (RUNBOOK.md step 2). Then update `catalysts\scorecard.md` with:
- Brier score and hit rate, by category, with n;
- judgment-add: the book against the plain S3 rule and against KMI TR, at 20, 60 and 120 sessions;
- sit-out gap: return given up (or loss avoided) by holding less than the default exposure;
- omissions: returns of candidate-set names the method passed on.

State the sample thresholds from `tests\replay_pilot_postmortem.md` section 5 before any claim:
- calibration is readable at about 40 probabilities (about 20 weeks);
- the 20-session comparison needs 15 closed dates (about 5 months);
- the 60-session comparison is not before about 12 months.

All claims are single-regime until a different regime appears. Apply the pre-registered verdicts in `knowledge\playbooks\replay_exam.md` section 7 (adds value, adds nothing, unreliable, invalid) only when the minimum sample is met. Before that, report "no verdict". A prediction class with Brier above 0.25 after 20 rows is stopped.

## 6. Maintenance

- Monthly: re-run the screens (RUNBOOK.md step 3) and refresh quality scores for held names. Update base-rate tables and version them by month, since the bundler filters base rates by date.
- When a conclusion changes, add a dated entry to `DECISIONS.md`.
- When a mistake is found, add it to `knowledge\lessons.md` with the date and the question that would have caught it.
- Freeze the brief, bundler, scorer and risk numbers. Changing them mid-run starts a new scorecard version.

## 7. Checklist before each call

From HOW_TO_THINK.md section 6. Answer each in writing.

1. What exact question is Jazib asking, in his words, and what number answers it?
2. What was the ceiling and the reference class, before I call anything good?
3. Does the metric fit the horizon (no multi-year compounder graded on twelve months)?
4. Is the result skill, or contributions, or luck?
5. Does every number have a source, or is it labelled a placeholder?
6. Did I judge the people, strategy and incentives, from their record?
7. What would an experienced person call obvious that I skipped, and what does the data not contain?
8. What regime is this evidence from, and is it like the present?
9. What is the price reaction telling me about what informed money knows, and is a shock here an opportunity?
10. Am I following his risk posture, not an institution's, and did I stop to discuss before any large spend?
