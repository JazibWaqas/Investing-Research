# Replay pilot post-mortem (18 Oct 2026)

Inputs: `knowledge/playbooks/replay_exam.md` (design and pre-registered verdicts), `tests/out/replay_pilot/` (24 dates), `tests/out/replay_2026/` (15 dates from 2026, the same brief), the REPLY.json files, and the 10 contamination grades in the pilot workflow journal. Figures are copied, not re-scored.

## 1. Validity

**Contamination.** On 8 of the 10 probed dates the model, given no data, recalled specific post-T facts (score 2 or 3). Seven dates scored 3: 2019-03-08, 2020-02-21, 2022-07-01, 2023-05-05, 2024-01-05, 2024-12-13 and 2025-04-18. 2021-09-10 scored 2. Only 2026-02-20 and 2026-05-22 scored 0. Pre-registered rule (s5): 3 or more dates at 2+ means every date before the published training cutoff is contaminated. The 21 replays dated before 2026 therefore measure memory and caution, not judgment. On 2020-02-21 the agent said so itself: "I recognise this date and have post-T knowledge … A cash outcome could still be unconsciously shaped by that memory."

**The 2026 dates are not clean under the rule either.** The replay agent ran as `claude-sonnet-5-5` (observed in the agent transcripts). Anthropic's model page and help centre both give it a training-data and reliable-knowledge cutoff of **June 2026** (asserted by source). The rule says headline claims use only dates more than a month after the cutoff, which means after about the end of July 2026. All 15 dates in the 2026 run (9 Jan to 17 Jul) fall before that. They are *probe-clean* (two of them scored 0) but *rule-contaminated*. A probe score of 0 is weak evidence: both 2026 answers were refusals ("explicitly declines to give any direction or events"). The coordinator's framing of the 2026 run as "post-training-cutoff so uncontaminated" does not hold. It is still the best evidence and is used below as primary, under that label.

**Other pre-registered validity gates the pilot failed or skipped (observed):**
- Citations resolved at 75% in the pilot and 79% in 2026. The s8 gate is 90%, and the s7 "Invalid" line is more than 10% failing. I could not separate format errors (whole base_rates rows cited with `row: null`) from fabrications.
- The s4 bundle was meant to include `principles.md` (core as a resting place, sitting out is a position, risk budgets, the user's risk posture). It is absent from every bundle I opened (2019-03-08, 2024-06-07, 2026-04-24). The 2026-06-19 reply notes "The method/ files were not in the bundle."
- `base_rates.csv` shipped measured on the full sample through 2026-10-16, with a warning, instead of being rebuilt by date. For the 2026 dates that sample contains the 2026 outcomes themselves.
- The bundles for 2026-04-24 and 2026-05-08 shipped an empty announcements section (header only). The raw files hold 683 and 857 rows. Both replies say "The announcements file is empty."
- The pilot dates were the shock and policy dates, not the odd-numbered set. No calm or random dates were included, and the 6 repeat dates were not run. Returns were scored, though s8 said compliance only.

**Still informative:** the shape of the behaviour, which is the same in contaminated and probe-clean runs; schema compliance, at 100% valid in both runs; the replay agents read only BUNDLE.md (two transcripts checked); and the reasoning text.

## 2. What the agent did, and why

Pilot: mean exposure 18% (maximum 40%). Stance: neutral 15, risk_off 8, risk_on 1; zero exposure on 4 dates. There were 10 entries across 7 of 24 dates. Exposure averaged 25% on bull dates and 15% on hike_flat dates. In 2026: exposure 0 to 35%, 2 entries in 15 dates. Core in 2026: OGDC (13 of 15 dates), FFC (6), HUBC and PPL (3 each). In 2026 the agent held *more* before falls (27%) than on other dates (21%). It was most bearish at the trough: p_kmi_up_60 was 0.42 on 2026-03-27, and the KMI then rose 17.6% over 60 sessions.

The four candidate causes:

1. **The method documents (main cause).** The agent read "no measured edge for a situation type" as "hold cash". It applied this to the core too, which should rest on business questions, not timing base rates. Examples:
   - 2019-02-08: "No method file gives a tradable edge in this setup, so I stay neutral and hold no book."
   - 2026-04-24, at 0% exposure: "No entry is supported by a measured edge, so stay in cash and watch."
   - 2026-04-10: base_rates.csv "is the reason for taking no entries."
   - 2023-05-05 core: "Evidence is a cheap-P/E base rate that is unconfirmed, so modest weight."

   Nearly every row of base_rates.csv reads "not supported", "no tradable drift", "nothing" or "weak". The only hike-regime lessons in situations.md say cash, and the agent cited them again and again: "hold bills, and set a trigger to return" (2026-03-27), "says hold bills and set a return trigger … Stay mostly in cash" (2026-05-08), and the same lesson again on 2026-05-22.

2. **The brief (enabling cause).** The brief gives a loss budget for entries only. It sets no annual budget, does not state the investor's posture (invested when situations line up), and never says that cash must beat the core or that a missing timing edge is no argument against the core. The missing `principles.md` would have supplied most of this. The budget allowed about 60% in entries at 15% stops and put no cap on the core, so the default held exposure down, not the budget.

3. **Contamination (minor for exposure).** If memory were driving the behaviour, exposure would drop before falls. The pilot gap was only 7 points, and in 2026 the gap went the wrong way, at −5. The one place memory plausibly helped is the cash on 2020-02-21.

4. **Sound judgment in hike regimes (partly).** Cash at 10% to 22% T-bills is defensible when the curve prices hikes. The book beat KMI TR at 60 sessions (+4.4% against +0.2% in the pilot). But the caution did not depend on the regime. Exposure stayed at 40% or below even in the 2024 to 2025 cutting bull, with real rates near 10 points, and D in bull dates at 120 sessions was −18.7%. In 2026 its caution lagged the market.

2026-05-08 shows the whole pattern. The agent was risk_off at 10%, with one OGDC position. It watched ENGROH at EPS ×4.3 and P/E 5.1 but would act "only if price confirms; base rate for low P/E is not confirmed". It waited to "re-enter risk only after a hold with CPI no longer rising". It had no announcements to read.

## 3. The numbers

| | Pilot (24, contaminated) | 2026 (15, probe-clean) |
|---|---|---|
| D at 60, CI | +1.8% [−3.1, +9.2] | +1.1% [−6.2, +10.0] |
| D at 120, CI | −7.1% [−19.3, +4.0] | −5.4% [−15.0, −0.3] (n 8 to 9) |
| hike_flat D at 60 | −0.1% | +1.1% |
| Book above placebo median, 60 / 120 | 62% / 54% | 53% / 40% |
| Entries; hit at 60 | 10; 70%, median +7.7% | 2; 50%, worst −17.2% |
| Brier p_kmi_up_60 (coin 0.250) | 0.258 | 0.287 |
| Brier p_gain | 0.239 (n 10) | 0.266 (n 2) |
| Sit-out gap (bar +20) | +7 | −5 |
| Core minus KMI TR, 60 / 120 | +5.8% / +3.6% | +1.7% / +6.7% |

**Pre-registered verdict.** By s7 the result is **Invalid**: the contamination bound leaves no rule-clean dates, and more than 10% of citations fail. Read on its merits anyway, the result is the same:
- "Adds value" fails on the CI, the sit-out gap and Brier.
- "Adds nothing" is triggered (in 2026 the CI contains 0 at 60 sessions).
- "Unreliable" is also triggered: Brier is 0.25 or more, fall-date exposure in 2026 is no lower, and in 2026 the CI at 120 sessions lies entirely below 0. The 120 figure rests on 8 to 9 overlapping windows.

In any case the s7 minimum sample (15 dates per regime claim, 40 probabilities, 10 entries per type) is met nowhere.

**What a fair reader would conclude.** No evidence that the judgment layer adds anything. Some evidence that it costs return over 120 sessions by sitting in cash: plain S3 made +11.7% at 120 sessions in 2026 against +6.2% for the book, because S3 held the refiners the agent only watched. The index calls are no better than a coin. The core names beat the index, on small n. The book's 87% to 96% win rates come mostly from T-bill interest on 75% to 80% cash, not from any skill.

## 4. Surprise log (pilot, 15 rows)

- **Method error, knowable from the pack (4):**
  - 2020-04-03, exposure 30% after 225bp of cuts with CPI falling. The agent cited the first-cut base rate and then sized it at almost nothing.
  - 2025-05-16, 24% with a live easing cycle and CPI at 0.26%.
  - THCCL, 2025-04-18: EPS ×2.6, P/E 2.2. This fits the only half-supported screen (P/E below 6) and was not entered.
  - SAZEW, 2023-05-05: EPS ×17, refused on a P/E rule the method does not have.
- **Direction knowable, path not (3):**
  - 2025-04-18, 25% with real rates near 11 points; the Pahalgam shock came between T and the rise.
  - 2026-03-27, low exposure and a stance contradicted by a 10% move (two rows).
- **Unknowable, or correctly passed on the measured evidence (8):**
  - KOHC twice: before COVID, and as a lock name.
  - ISL and AIRLINK: results-gap names, a watch-only type.
  - FABL: the deal was terminated.
  - BNL and QUICE: locks with no filing, the V4 type that measured nothing.
  - 2023-05-05 exposure: the IMF deal of 29 June was outside a pack that has no IMF data.

The 2026 log repeats the pattern:
- MACFL and SGPL were passed as lock names.
- 2026-03-20 and 2026-03-27 show low exposure at the trough.

## 5. What this means for the exam

No replay with this model can be rule-clean yet. The earliest clean dates come about a month after its June 2026 cutoff, and none of those dates has 60 forward sessions yet.

1. **Read the 2026 run as diagnostic.** n is 15, one regime, overlapping windows: about 2 to 3 independent observations. The run can expose gross failure (it did: wrong-way exposure, and Brier worse than a coin). It cannot confirm skill.
2. **Add a rule-clean arm on the same bundles.** Use Sonnet 5 (cutoff January 2026, per the help centre); it is clean from 2026-03-06, which covers 11 dates. Re-probe each date with a forced-recall prompt ("guess if unsure"), so the probe tests memory rather than willingness to answer.
3. **The live weekly scorecard is the real exam.**
   - **Cadence:** every Friday from 23 Oct 2026.
   - **Frozen:** the brief and bundler commits, the full model ID, a monthly-versioned base-rate table, the scorer, and the risk numbers.
   - **Arms:** method, KMI TR, S3, S3 scaled, the placebo, and a fixed 75% core-only arm, which separates the core's value from timing.
   - **Horizons:** add p_kmi_up_20.
   - **Claims:**
     - calibration at 40 probabilities (about 20 weeks);
     - D at 20 sessions after 15 dates whose outcomes have closed (about 5 months);
     - D at 60 sessions not before about 12 months.

   Every claim is labelled single-regime.

## 6. Brief changes for the clean runs

Fixes:
- Ship `principles.md`.
- Fill in the empty announcements sections.
- Rebuild base rates by date.

Brief changes. These touch only the method arm, so S3 and the placebo cannot be biased:
- State the posture: "Capital should be at work when situations line up. Cash is a position: state the expected core return against the 6M T-bill and why cash wins. A missing timing edge for a situation type is not an argument against the core."
- Add an `exposure_reason` field.
- Add an annual loss budget as [P].
- Do not add an exposure floor. That would test a different, mechanical strategy.

Unchanged: the dates, schema, counts, entry risk numbers, fills, costs, horizons, arms, bootstrap, thresholds, one fresh context per date, and bundle-only access.

These changes are made after the 2026 outcomes were seen, so the 2026 dates become in-sample for the revised brief. Re-run them for comparability, but only the live scorecard tests the revised brief.
