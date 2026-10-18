# Replay exam: does the judgment layer add anything the plain rule does not?

Design, 18 Oct 2026, not yet run. This file is for the orchestrator and the scorer. The replay agent never sees it, because the reasons for most dates are facts that come after T. Every threshold marked [P] is a pre-registered placeholder, not evidence. It can be argued before the run and is frozen once any outcome has been seen.

## 1. What this exam can and cannot show

The exam asks one question. Given only what was public at a date T, does the method (regime read, core, watch, entries, exposure) beat the plain breakout rule run from the same date? It cannot prove out-of-sample skill. The method and the breakout rule were both chosen in Oct 2026 with 2019 to 2026 in view, so every date is in-sample for the design. That makes the replay necessary but not sufficient. The real exam is the frozen weekly scorecard from Oct 2026 on.

## 2. Date set (48 dates)

Each date is a Friday close, or the session before it if the Friday was closed. No two dates are less than 28 days apart (checked).

**Regimes.** hike_flat (HF) covers Jan 2019 to 16 Mar 2020, Jan 2021 to Jun 2023, and Jul 2025 to Jul 2026. Bull (B) covers 17 Mar to Dec 2020 and Jul 2023 to Jun 2025. Assigning 2020 Q1 and 2023 H1 to HF is my call: in both periods the policy rate was held at or rising to its peak (`data/macro/policy_rate_decisions.csv`). The split is 29 HF (60%) and 19 B.

**Shock dates.** "Pre" is the last Friday at least 5 sessions before the shock. "Post" is the first Friday at least 5 sessions after the trough, and never less than 28 days after "pre". Troughs are taken from `data/macro/kmiallshr.csv`. Event dates marked (gk) are from general knowledge and must be verified before the post-mortem.

**Random dates.** Eight dates are drawn from weekly last sessions between 1 Feb 2019 (after the first real KMI list, 28 Jan 2019) and 31 Jul 2026. The 40 hand-picked dates are fixed first. Then 5 HF dates and 3 B dates are drawn one at a time, each kept at least 28 days from every date already chosen, using `numpy.random.default_rng(20261018)` and `ok[rng.integers(len(ok))]` with the pool in date order.

| # | Date | Reg | Role | Reason |
|---|---|---|---|---|
| 1 | 2019-02-08 | HF | pre | Pulwama 14 Feb (gk) |
| 2 | 2019-03-08 | HF | post | After Balakot 26 Feb (gk) |
| 3 | 2019-05-17 | HF | policy | Before +150bp on 20 May; IMF staff deal 12 May (gk) |
| 4 | 2019-07-26 | HF | pre | Before the 16 Aug 2019 low; Article 370 on 5 Aug (gk) |
| 5 | 2019-08-23 | HF | post | After the 16 Aug low |
| 6 | 2020-02-21 | HF | pre | COVID crash (gk); low 26 Mar |
| 7 | 2020-04-03 | B | post | After the 26 Mar low and the cuts of 17 and 24 Mar |
| 8 | 2020-06-05 | B | calm | Mid cutting cycle |
| 9 | 2020-07-03 | B | random | |
| 10 | 2020-08-21 | B | calm | Index back near its 2018 peak |
| 11 | 2020-10-29 | B | calm | Rate on hold at 7%; second wave (gk) |
| 12 | 2020-12-18 | B | calm | Late easing bull |
| 13 | 2021-03-19 | HF | random | |
| 14 | 2021-06-11 | HF | pre-top | Week before the 14 Jun 2021 peak, which began a 22% fall |
| 15 | 2021-09-10 | HF | policy | Before the first hike, 20 Sep |
| 16 | 2021-10-08 | HF | post | After the 29 Sep low |
| 17 | 2021-12-17 | HF | random | |
| 18 | 2022-03-25 | HF | pre | No-confidence and ouster, 10 Apr (gk); +250bp on 7 Apr |
| 19 | 2022-04-22 | HF | post | After the ouster |
| 20 | 2022-07-01 | HF | pre | Default scare; +125bp on 7 Jul; low 21 Jul |
| 21 | 2022-07-29 | HF | post | After the 21 Jul low |
| 22 | 2022-10-07 | HF | random | |
| 23 | 2023-01-06 | HF | pre | Before the 17 Jan low and the rupee cap removal (gk) |
| 24 | 2023-02-03 | HF | post | After the devaluation |
| 25 | 2023-03-10 | HF | random | |
| 26 | 2023-05-05 | HF | pre | 9 May riots (gk) |
| 27 | 2023-06-23 | HF | pre | Before the IMF SBA staff deal, 29 Jun (gk) |
| 28 | 2023-07-21 | B | post | After the IMF rally |
| 29 | 2023-09-28 | B | calm | Rate at 22% on hold |
| 30 | 2023-12-08 | B | pre | Before the 12 to 26 Dec fall of 10% |
| 31 | 2024-01-05 | B | post | After the 26 Dec low |
| 32 | 2024-02-02 | B | pre | 8 Feb election (gk) |
| 33 | 2024-03-01 | B | post | After the election |
| 34 | 2024-06-07 | B | policy | Before the first cut, 10 Jun |
| 35 | 2024-10-04 | B | calm | Mid cutting cycle |
| 36 | 2024-11-15 | B | random | |
| 37 | 2024-12-13 | B | pre-top | Before the 16 Dec peak, which began a 16% fall |
| 38 | 2025-01-17 | B | random | |
| 39 | 2025-04-18 | B | pre | Pahalgam 22 Apr (gk); low 8 May |
| 40 | 2025-05-16 | B | post | After the ceasefire of 10 May (gk) |
| 41 | 2025-08-01 | HF | random | |
| 42 | 2025-09-12 | HF | calm | Rate held at 11% |
| 43 | 2025-12-12 | HF | policy | Before the 16 Dec cut |
| 44 | 2026-02-20 | HF | pre | Hormuz closure, 28 Feb; low 9 Mar |
| 45 | 2026-03-27 | HF | post | After the 9 Mar low |
| 46 | 2026-04-24 | HF | policy | Before +100bp on 27 Apr |
| 47 | 2026-05-22 | HF | post | After the hike |
| 48 | 2026-07-03 | HF | pre-top | Before the 6 Jul peak and the current fall |

Data ends on 16 Oct 2026. Every date has 60 forward sessions. Dates 46, 47 and 48 have only 117, 98 and 73, so their 120-session scores wait for more data. The pilot is the odd-numbered dates: 24 of them, 15 HF.

## 3. Replay agent brief (give it this section only, verbatim, with the bundle)

You are at the close of T. You get only `data/asof/<T>/` (market.md, sectors.csv, screens.csv, announcements_30d.csv, flows.csv, calendar.md; prices as traded at T) and `data/asof/<T>/method/`.

Forbidden:
- web access;
- any other repo file, or any earlier replay output;
- reasoning from anything after T.

If you remember what happened after T from your training, that memory is contamination. Do not use it, and report it in `contamination_note`. Every fact you state cites the pack. Every mechanism you rely on cites a method file. An uncited claim is a violation.

Risk budget [P]: for each entry, size_pct × (entry − stop) / entry ≤ 5 (percent of book); the sum over entries ≤ 10. Concentration up to all-in is allowed within that.

Return one JSON object and nothing else:

```json
{"date": "YYYY-MM-DD",
 "regime": {"rates_phase": "hiking|holding|cutting", "stance": "risk_on|neutral|risk_off",
            "p_kmi_up_60": 0.0, "summary": "<=80 words", "evidence": [CITE]},
 "core": [{"symbol": "", "weight_pct": 0, "thesis": "<=60 words", "evidence": [CITE]}],
 "watch": [{"type": "TYPE", "subject": "", "trigger": "", "evidence": [CITE]}],
 "entries": [{"symbol": "", "type": "TYPE", "entry_price": 0.0, "stop_price": 0.0,
              "stop_type": "fixed|trailing", "size_pct": 0, "horizon_sessions": 60,
              "p_gain": 0.0, "reason": "<=80 words", "evidence": [CITE]}],
 "exposure_pct": 0, "not_known": "<=60 words", "contamination_note": ""}
```

The fields:
- **CITE** is `{"file", "row", "field", "quote"}`. For CSVs, row is the symbol and field is the column. For .md files, row and field are null and quote is an exact substring.
- **TYPE** is one of policy_or_price_decision_pending, earnings_inflection_ignored, shock_and_rebound, deal_after_offer, buyback_or_sponsor_move, volume_with_upper_locks, other.
- **Counts:** core 0 to 3, watch 0 to 10, entries 0 to 3.
- **horizon_sessions** is 20, 60 or 120.
- **exposure_pct** is the core weights plus the entry sizes, from 0 to 100.
- **Symbols** must appear in screens.csv.
- **A trailing stop** keeps the distance (entry − stop) / entry, trailed on closes.
- **p_gain** is the probability that the net return is above 0 at horizon_sessions.

## 4. Harness, bundle and leak control

**Harness.** `scripts/replay_run.py` makes one API call per date. The call has no tools, has the brief and bundle inlined, starts from a fresh context, and logs the model ID. Output goes to `data/replay/<T>.json`, append only. The fallback is a subagent allowed to read only `data/asof/<T>/`. If it reads anything else, the date is void and is re-run once.

**Bundle filter** (`scripts/replay_bundle.py`). Today's method files are full of outcomes from 2024 to 2026, so:
- **`questions.md`**: from QUESTIONS.md, the item ID and the bold question only. Parentheticals naming a year or month are deleted. (B10 has "Feb 2026", and the why, data and [M] lines hold full-sample results.)
- **`base_rates.csv`**: each type is recomputed from events whose outcome window closed before T. With n<5 it shows the definition only. If the table cannot be rebuilt by date, it ships definitions without numbers.
- **`actors.md`**: only lines tagged `as_of:` before T. Undated lines are dropped.
- **Situation library**: a file is included only if its front-matter `outcome_end`, its latest fact, is before T. A file with no front matter is excluded. The event start date is not enough, because entries record what happened next.
- **`principles.md`**: HOW_TO_THINK s5 items 2 to 6 and the s6 bullets, with parentheticals stripped. Nothing from FACTS, tests/, sectors/, companies/, lessons, PICKS or REPORT.

**Leak lint** (it must pass before a date runs):
- no date after T in the bundle, except the "Next scheduled MPC" line;
- no post-T event term, from a list built from the reasons column (Hormuz, Pahalgam, COVID, no-confidence, SBA and so on);
- symbols as they were at T (BYCO, not CNERGY, before the rename);
- `asof.py <T> --check` passes.

**Leaks logged, not fixed:**
- **Sector baskets** use 2026 names.
- **KMI lists** before Jun 2026 are derived.
- **Survivorship**: the panel lacks names delisted before 2026. It flatters levels, but the method, S3 and the placebo all share it.
- **Vendor EPS** may be restated.
- **next_mpc** reads real decision dates, so the emergency meeting of 7 Apr 2022 shows as "scheduled".
- **Dividends** in the adjusted panel are complete only from Nov 2024. That biases book against KMI TR before then, but not method against S3.

**Validation.** The output must parse and its symbols must exist. Exposure must equal the sum of weights within ±1. The risk budget must hold. Every citation must resolve: the quote matches to 4 significant figures, or as a substring. A failed output is re-run once. A second failure is scored and flagged.

## 5. Contamination check

Dates 1, 4, 6, 14, 18, 23, 27, 34, 39 and 44 get a fresh call with no pack: "It is the close of T. Without data, what do you expect over the next 6 months for the KSE-100, the SBP policy rate, the rupee and any major political or security event in Pakistan? If you remember what actually happened, say so and state it." A second agent scores each answer against a scripted fact sheet: the KMI 120-session return, the rate path, USD/PKR, and the reasons column.

Scores:
- 0: nothing specific;
- 1: generic direction;
- 2: one specific correct post-T fact (a named event, a rate within 100bp, or the index within 10 points);
- 3: several.

Bound:
- If 3 or more dates score 2 or higher [P], every date before the model's published training cutoff (recorded from Anthropic's documentation, not assumed) counts as contaminated, and headline claims use only dates more than a month after it.
- A second agent also flags any post-T fact in each replay output.
- Results are always split before and after the cutoff.

## 6. Scoring (`scripts/score_replay.py`)

The book is Rs100k at T.

**Fills:**
- at the T+1 close;
- an entry is unfilled if that close is more than 3% above entry_price [P];
- an entry_price below the T close fills at the first close at or below it within 10 sessions.

**Costs.** As in `tests/oracle_and_good_case.md`: 0.25% a side, plus 0.25% under Rs20m median traded value.

**Prices.** Returns come from `panel_close_adj.parquet`. Stops are rescaled by the adjusted-to-raw ratio at T. A close at or below the stop exits at the next close. Core has no stop. Cash earns the 6M T-bill rate at T. A delisted name is marked at its last print.

**Horizons.** 20, 60 and 120 sessions; 60 is primary.

Arms:
1. **Method book.**
2. **KMI All Share TR.**
3. **S3 from T:** Rs100k cash, the 52-week-high breakout, liquid KMI names (median traded value over Rs5m), up to 3 at 1/3 each, ranked by close over the prior 252-session high, 20% trailing stop, slots refilled daily. This reuses the S3 branch of `scripts/tests/oracle_and_good_case.py`.
4. **S3 scaled to the method's exposure.**
5. **Placebo:** 500 draws. Each core and entry name is replaced by a random screens.csv name, with the same weights, stops, fills and horizons.

Metrics, each reported as n, mean, median, win rate and worst, by regime and by role:
- **Entries.** Returns, hit rate at 60, share above +50% at 120, worst entry, placebo percentile.
- **Core.** Returns against KMI TR.
- **Calibration.** Brier on p_gain and on p_kmi_up_60, against the pooled placebo win rate and 0.5.
- **Judgment-add.** D = method − S3, at 60 and 120. It splits into selection (method − arm 4) and exposure (arm 4 − S3). The CI is a moving-block bootstrap over dates in order: blocks of 3, 10,000 draws, seed 20261018.
- **Sit-out.** A fall date is one where the KMI 60-session minimum is at least 10% below the T close. Compare exposure on fall dates with the other dates.
- **Surprise log** (`data/replay/surprises.csv`). A row is written for any of:
  - exposure of 60% or more on a fall date;
  - exposure of 30% or less before a KMI rise of 10% or more;
  - a stance contradicted by a 10% move;
  - p_gain of 0.65 or more with the stop hit;
  - a watched name that rose 50% or more and was not entered.

  Each row carries the reasoning verbatim and its citations. The post-mortem classes it as knowable, unknowable, model error or contamination suspect.

## 7. Verdicts, pre-registered [P]

- **Adds value:**
  - the 95% CI of D at 60 sessions is above 0;
  - hike_flat mean D is above 0;
  - entry Brier is below its reference;
  - the book is above the placebo median on at least 60% of dates;
  - fall-date exposure is at least 20 points lower.

  If only the exposure part is positive, the verdict is "timing call only".
- **Adds nothing:** the CI contains 0, or hike_flat D is 0 or below. The method becomes the plain rule plus the core, and the core is kept only if it beats KMI TR on mean and median at 120 sessions.
- **Unreliable:** any of:
  - the book is below KMI TR on mean and median at both 60 and 120;
  - the CI is entirely below 0;
  - Brier is 0.25 or more;
  - fall-date exposure is no lower;
  - on 3 or more of the 6 repeated pilot dates, exposure differs by more than 30 points or no core name is shared.
- **Invalid:** the contamination bound leaves too few clean dates, more than 10% of claims fail citation, or the leak lint fails.
- **Minimum sample:** no verdict from the pilot; at least 15 dates per regime claim; at least 40 probabilities for calibration; at least 10 entries per situation-type claim.

## 8. Order and cost

1. **Bundles and lint.**
2. **Pilot:** 24 dates, with dates 1, 9, 21, 29, 39 and 45 repeated. Only compliance is scored; returns stay unseen. Gate: at least 95% valid outputs, at least 90% of citations resolving, and the user's explicit go. If the brief changes, the pilot dates are re-run.
3. **Contamination check,** finished before step 4.
4. **Full run,** with the brief's commit hash frozen.
5. **Scoring,** plus a per-date leak review.
6. **Post-mortem:** one call per surprise, then a main-session review.

Estimate (Sonnet, no-tool harness). Packs measure 55 to 116 KB (17k to 35k tokens); the bundle is assumed at 10k and the output at 8k.

| Stage | Calls | Input | Output |
|---|---|---|---|
| Pilot | 30 | 1.3M | 0.25M |
| Contamination | 20 | 0.1M | 0.03M |
| Full run | 24 to 48 | 1.1M to 2.2M | 0.2M to 0.4M |
| Leak review | 48 | 0.8M | 0.1M |
| Post-mortem | ~20 | 1.0M | 0.1M |
| Total | 140 to 165 | 4.3M to 5.4M | 0.7M to 0.9M |

At $3 and $15 per million tokens (asserted; check the price) that is about $25 to $30, and the pilot about $8. A subagent tool loop costs 3 to 5 times the input. The pilot's measured usage replaces this estimate.
