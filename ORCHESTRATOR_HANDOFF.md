# ORCHESTRATOR_HANDOFF.md — what this session established, for the orchestrator

Written 19 Oct 2026 by Claude Fable 5.1 at the end of a 30-hour research session (about 50 million subagent tokens across Haiku, Sonnet, Opus and Codex gpt-6). Every claim cites a repo file. Read PLAYBOOK.md and knowledge/HOW_TO_THINK.md with this. Data runs to the 16 Oct 2026 close; no results have landed since (EFERT and ATRL report 19 Oct).

## 1. The model: how money is made on PSX, ranked

Ranking is by effect size, then reliability, then how early it is knowable. "Knowable" means from public data before the move. All tests are point in time, placebo-controlled, with costs of 0.5% a round trip (data/costs.md); verdicts and numbers are in tests/FACTS.md.

| Rank | Mechanism | Effect | Reliability | Knowable | Key numbers and file |
|---|---|---|---|---|---|
| 1 | **Regime turns** (hike cycle ends, cut cycle begins, within ~3 months of a market low) | Largest: all 34 runs of 5x+ since 2016 were multi-year and 23 began within 3 months of a market low; KSE100 +40% and +49% in 120 sessions after the 2020 and 2024 first cuts | 4 real turns, 4 false bottoms; a 4-signal checklist separated them (3 to 4 present at real lows, 1 to 2 at false ones) | Weeks after the low, not before | tests/winners_population.md; tests/rate_cycle_episodes.md (first cut 120d median +39.8% vs placebo +7.9%, n_eff 3); knowledge/REGIME_TURN_PLAYBOOK.md |
| 2 | **Staying invested in liquid KMI names** | KMI All Share total return 11.4%/yr 2017 to 2026, 2.66x on Rs50k/month deposits 2018 to 2026 (Rs14.1m on Rs5.3m) | High; drawdowns 40 to 60% | Always | data/macro/INDEX_NOTES.md; tests/system_walkforward.md |
| 3 | **Confirmed trend with a sized exit** (buy at a 252-session high, trailing stop) | 2.5x to 3.3x on a fixed Rs50k in each of the three bull windows (2020-22, 2022-24, 2024-26); 0.8x to 1.1x in the two hike windows; 0.82x in the year to Oct 2026 | Held on two independent implementations, but one or two trades carry each window and a fixed 20% stop kept over half the gain in only 15 to 23% of winning runs | At the breakout, with about half the eventual gain still ahead (median, on winners only) | tests/oracle_and_good_case.md, tests/active_trading_codex.md, tests/rs50k_last_year.md, tests/winners_population.md |
| 4 | **Sector and policy waves** (refiners 2026, OMC 2024, cement 2016-17) | 142 of 382 liquid big runs; the leader of a wave runs 2x to 5x | Visible in filings and prices; implementation of announced policy only 42% (62% with partial) | Weeks into the wave; the first signal was a strong quarter the price ignored (PRL 29 Apr 2026) | knowledge/CATALOGUE.md type 2; knowledge/playbooks/actors_and_incentives.md; knowledge/playbooks/catalyst_trade.md |
| 5 | **Shock rebound** (geopolitical crash) | Index 5%+ below a shock's pre-event close: +4.2% median at 20 sessions, 78% win (random close +1.1%, 57%); geopolitical falls of 5%+ rebounded a median +27.8% at 60 sessions, 9 of 9 regained | 10 geopolitical events; day-1 repricing is the only headline type the market reprices | On the day | tests/noise_map_shock_rebound.md |
| 6 | **Results jump with cash behind it, price confirming** | Gap up 5%+ on 2x volume with EPS +30%: 60-session median +16.6%, win 81%, n 37, but same-year random entries +10% (p 0.11) | Weak, 14 entry quarters | On the filing day | tests/results_gap_and_policy.md; knowledge/winners/_results_jumps.md |
| 7 | **Deals, after the public offer** | 25 of 28 that reached an offer completed; buy after the offer median +1.1%; buy after the intention notice median −1.2% (48% complete) | Thin edge, partial offers pay on only part of the holding | At the offer document | knowledge/playbooks/deals.md; data/deals_history.csv |
| 8 | **Quality within sector** | Top minus bottom third median +5.8% over 12 months, 69% win, p 0.054 | 3 independent years | Quarterly | tests/quality_within_sector.md |
| 9 | **Sector momentum, long-short** | +2.66% net per 3 months, 65% win, t 1.7; long-only top-3 vs KMI −0.41% | Mostly the short leg; retail cannot short | Monthly | tests/sector_momentum_regime.md |

Tested and not usable (all no better than random after costs): earnings-yield value (−1.2 pts net, 4 cohorts, tests/value_timestamped.md); stock momentum, volume ignition and upper locks (median −11% with a stop, worse than random, tests/volume_ignition_upper_locks.md); news-less "informed capital" rises (followed by a filing 26.6% vs 26.7% for quiet names, tests/informed_capital.md); investor flows by type or sector (tests/flows_predict_sectors.md); commodity and PKR leads (tests/commodity_pkr_sensitivity.md); index recompositions (tests/index_recomposition_events.md); insider cluster buying (37 clusters, median −0.4%, tests/insider_cluster_buying.md); dividend run-ups (ex-day drop ratio 1.01, tests/dividend_runup_exdate.md); corporate events except a 9-trade split lead (tests/corporate_events.md); calendar effects except February (−3.95% mean, 9 of 10 years, tests/calendar_effects.md); every 1-to-10-day mechanical rule, 40 tested (tests/pattern_mining_daily.md, knowledge/playbooks/short_term.md).

## 2. The 2026 refiner and steel retrospective

From knowledge/playbooks/catalyst_trade.md, tests/refiner_steel_retrospective.md, knowledge/situations/07_2026_refiners.md and 08_2026_asl_sponsor_buying.md, tests/winners_2026_postmortem.md.

Refiners: flaggable as a "loaded spring" on 29 Apr 2026, when PRL's March-quarter result (EPS 15.78 after a loss) put it at about 2x trailing earnings and the market treated it as a one-off; the stock lagged the market for ten weeks. Flaggable as a trade on 8 to 9 Jul: the US-Iran truce collapsed (Brent +6%), PRL rose on 9x normal volume while the market fell, and made its first 252-session high on 9 Jul at Rs41.85; the refinery policy was approved on 21 or 28 Jul (sources disagree, unverified). Buying at the 9 Jul close returned +155% to 16 Oct (PRL), +70% NRL, +34% ATRL, +37% CNERGY. Steel: there was no sector rally (ISL and MUGHAL fell); ASL doubled because Arif Habib Corp bought in the open market on 7 Apr, 21 May and 3 to 4 Aug, each public within two days; flaggable from 9 Apr.

Signals and their record elsewhere: (a) the "ignored strong quarter" (EPS more than 10% of price or trailing P/E under 4x, muted 20-day reaction): +6.4% median at 120 sessions, n 42, but the edge sits in 2024 to 2026 and low P/E, and it failed its own-pool placebo inside the walk-forward (tests/results_surprise_drift.md, tests/system_walkforward.md); (b) the 252-session breakout: 25.6% of 1,558 breakouts later touched +50% within 126 sessions, year rates 6% to 38% (tests/winners_population.md); (c) the volume-breakout reaction rule used in the retrospective: 60-day median −3.4% vs placebo −6.9%, win 45% vs 36%, n 788, 6.1% of signals above +50% (weak); (d) sponsor open-market buying: ASL is one case; across 4,617 extracted insider trades the cluster signal is not supported (median −0.4%, p 0.47), director buys out of sample are the only lead (n 16, median +8.3%). False positives: the breakout rule's nine losing trades in the year to Oct 2026 (five stopped in the March war crash) and the 59 "no visible cause" ignitions in the library with a negative base rate (knowledge/CATALOGUE.md type 9).

## 3. Calibration

Point-in-time replays (knowledge/playbooks/replay_exam.md, tests/replay_pilot_postmortem.md, tests/out/replay_pilot/, replay_2026/, replay_2026_v2/): invalid as a judgment test. The replay model (Sonnet 5.5, training cutoff June 2026) recalled the six months after 8 of 10 probe dates in detail (7 scored 3 of 3), so every date in our data is contaminated. Within that caveat: brief v1 (no investor posture stated) produced 20% average exposure, two entries in 15 dates of 2026, judgment-add +1.1% at 60 sessions and −5.4% at 120 (CI below zero), Brier 0.287 vs 0.250 for a coin. Brief v2 (posture stated, exposure reason required) produced 50 to 75% exposure, growth names in the core, four entries at 75% hit, book +2.8% vs KMI +1.2% and placebo +1.4% at 60 sessions, but the plain breakout rule won at 120 (+11.7% vs +4.4%) by holding the refiners, and exposure was higher before falls than otherwise. Lesson 23 in knowledge/lessons.md: given documents that say "no measured edge", a model holds cash; the brief shapes behaviour more than the data.

Scored predictions: none yet. 42 rows are frozen in catalysts/frozen_predictions.csv: 27 on 19 to 29 Oct results and the MPC (frozen 17 Oct), 6 on the core buys and the breakout sleeve (18 Oct), 6 on PICKS v4 and the regime checklist (19 Oct), plus the orchestrator's register in seed/FORECAST_REGISTER.md. Three calibration rows bet the orchestrator's bands are too low: EFERT EPS above 4.74 (0.80), MEBL EPS above 12.74 (0.78 implied), OGDC EPS above 9.94 (0.82). Trust the probabilities as a reader's considered odds, not as calibrated frequencies, until catalysts/scorecard.md has 20 rows per class.

## 4. The current regime

Policy rate 11.5% (hiked 27 Apr 2026; held 14 Sep, 7 of 10 votes); 6-month T-bill 12.40% on 14 Oct, 0.9 points above policy, down 5bp from 30 Sep; Sep CPI 10.3% from 11.1% (seed series, unverified); SBP reserves $21.5bn (+$4.2bn in 13 weeks), import cover 3.1 to 3.9 months, current account about balanced over 12 months; KSE100 trailing P/E 7.9 to 8.1, earnings yield about equal to the bill (data/macro/earnings_yield_vs_tbill.csv); Brent about $105 to $126 depending on series, +50% in 13 weeks; KSE100 13% below its 23 Jan peak, 16% of liquid names above their 50-day average; IMF 4th-review staff agreement 8 Oct, board undated (data/macro/, knowledge/REGIME_TURN_PLAYBOOK.md section 6).

Regime label: TIGHT. The turn checklist reads 1 present (drain), 1 absent (oil), 2 unknown until about 10 Nov; the setup resembles the 14 Sep false bottom, not any of the four real lows.

MPC 26 Oct call (frozen 17 Oct): hold 0.50, +50bp 0.38, +100bp 0.10, cut 0.02. Evidence each way: hold, because CPI fell and real rates are about +0.3; hike, because the bill prices it and 61% of brokers expect it (Topline survey, 17 Oct, cited in knowledge/playbooks/picks_redteam_codex.md); SBP's reaction function from 84 decisions: it hiked at a median real rate of −1.1% and never cut outside Covid with real rates under +4.7% (knowledge/playbooks/actors_and_incentives.md).

Sector implication (sector_map.md, knowledge/playbooks/sector_rotation.md, tests/sector_momentum_regime.md): in hike windows E&P, fertilizer and Islamic banks held up best (regime tilt itself has no measured edge, placebo p 0.26); cement, autos, steel, textiles, pharma and chemicals lag; only about 4% of liquid names rose in the two previous hike bears (knowledge/situations/03 and 12). The rotation rule fires when CPI falls two prints and the 6-month bill sits below the policy rate at two auctions; it has not fired.

## 5. Current picks and the comparison with the orchestrator's calls

PICKS.md v4 (19 Oct), for Rs50,000 now and the monthly deposits:

| Position | Size now | Entry | Exit | Catalysts | Probability |
|---|---|---|---|---|---|
| LUCK core | Rs12,500, 31 sh, limit Rs410 | Monday open | Written killer (PIA or GEPCO cheque, cement demand falling), KMI deletion; no price stop | Result late Oct; first rate cut (leader at both prior turns) | 12m total return positive 0.55; turn year +50% |
| MEBL core | Rs12,500, 23 sh, limit Rs552 | Monday open | Shrink on the first rate cut of a cycle | Q3 result 22 Oct 11:00 (EPS 12.5 to 15 at 0.65, DPS 8+ at 0.60); MPC 26 Oct | 12m positive 0.55 |
| MARI core | Rs10,000, 16 sh, limit Rs640 | Monday open | Oil collapse or higher state take | Q1 result late Oct (EPS about Rs17); gas circular-debt plan | 12m positive 0.55 |
| Reserve | Rs10,000 now, 20% of each deposit | Only on a turn score of 3 of 4 | n/a | Checklist signals resolve about 10 Nov | No turn by 10 Nov: 0.75 |
| ATRL opportunity | Rs5,000 to 10,000, conditional | Tue 20 Oct only if Mon close > Rs1,200 after result and diesel-cap decision | Close below Rs975 or first lower lock | Result 19 Oct 16:00; cap decision about 19 to 20 Oct | If entered, net gain 0.50 |
| SAZEW trigger | up to Rs12,500 | Q1 EPS at or above Rs60 and no hike on 26 Oct | Stop 30% below entry | Result date not noticed yet | — |

Versus the orchestrator's calls (seed/PSX_STATE, seed/FORECAST_REGISTER.md):
- **HUBC, OGDC, FFC (yield core):** disagree as the core for this investor. Sound businesses with no engine to double earnings (knowledge/companies/quality_scores.csv: FFC 14, OGDC and HUBC not scored higher; cards and red teams gave +2 to +3% expected returns, knowledge/companies/OGDC.md, FFC.md). Kept as paper positions for scoring. The orchestrator's OGDC entry at Rs285 and HUBC at Rs170 remain reasonable value entries; they are not growth.
- **MEBL:** agree on the business (best record of 20), disagree on the valuation gate. The orchestrator's Rs490 trigger and its frozen Q3 band (7.02 to 12.74) look too low; we expect 12.5 to 15. We buy now as a core name because a hike regime favours it; the sell signal is the first cut, which the orchestrator also identified (rotation rule).
- **SYS:** agree with the deferral. 23x earnings, cash conversion unresolved, a derating case study in knowledge/situations/10. Watch at or below Rs100.
- **SAZEW:** agree on the business (capacity 3x sales, 4x earnings), disagree on timing. Red team expected −9% in a hike regime (knowledge/companies/SAZEW.md). It is the first cyclical to own at the turn; trigger as above.
- **NETSOL:** disagree with the buy. Half of FY26 EPS was a one-off, treasury shares sold at a 40% discount, revoked filings; red team +2% (knowledge/companies/NETSOL.md).
- **EPCL:** agree with the pass at the market price; the arithmetic is in knowledge/playbooks/deals.md (about 53% of a holding bought at Rs38.60 at full tender; complete-set base rate: buy after the offer, not the intention).
- **PRL avoid:** agreed on fundamentals, and the frozen "EPS at or above Rs13 and flat-to-down over 5 sessions" call stands (we put 0.28 on the conjunction). But the retrospective shows PRL was the cleanest catchable move of 2026 on 9 Jul at Rs41.85, and the breakout rule held it; the avoid was right about value and wrong about the trade. At 4.2x its low it is late now.

## 6. Results scored so far

None. The first events are 19 Oct (EFERT 09:30, ATRL 16:00, MLCF EOGM), 20 Oct (PRL 15:00 board, first reaction session 21 Oct; EPCL), 22 Oct (MEBL 11:00, FABL 09:30), 26 Oct (MPC), 27 Oct (FCCL), 27 to 29 Oct (FFC, OGDC, MARI, LUCK, unconfirmed). Score per RUNBOOK.md step 2; the price-direction rows use the close of the fifth session after the release against the last close before it. The orchestrator's PRL conjunction and its EPS bands are in the same register, labelled "orchestrator", and will be scored alongside.

## 7. Corrections to the orchestrator's findings

From tests/seed_audit.md (Opus reproduction of every seed script) and the later tests:
- **Value factor (+28 pts/yr, 6 of 7):** reproduces as coded but is wrong. 29 of 108 names were dropped by an ex-dividend suffix bug (HUBCXD), dividends were double counted, the spread is −1.3 pts within sector and 24.8 pts with year fixed effects at t 1.2; with publication dates and four cohorts, net −1.2 pts (tests/value_timestamped.md). Qualify to: value is at most a tiebreaker inside a sector view. ROE/PB for banks (lesson 6) stands.
- **Sector momentum (+3.3%/3m, 67%):** holds as a long-short spread (+2.66% net, t 1.7) and fails long-only (−0.41% vs KMI). Qualify to: a ranking input, not a trade.
- **Operator footprints and pump chasing "fail":** overstated; they equal random entries (20-day median −1.5%, 43% win for both). The pump 60-day median reproduced at −8.5%, not −14.9%. Correct to: no edge, not negative edge. Volume-and-lock entries with a stop are worse than random (tests/volume_ignition_upper_locks.md).
- **Rate-cycle events (+33% at 120d after cuts):** +37% corrected for two cuts before the data; 13 cuts are 3 cycles; the first-cut result holds (+40%, +49%) but Dec 2025 gave +1%. Keep as a regime marker, not a bet size.
- **Rotation at turns (banks −48, power −42 to −46):** two episodes; power is −22 if the base is one month earlier. Keep as an anecdote and a watch rule.
- **IMF events, no effect:** correct, better phrased as not detectable (n 12, CI ±5.7%).
- **CPI turn +44%:** 33 months in 10 runs, one run supplies 21; earlier runs were followed by −10 to −15%. Weak.
- **LESSONS.md 1 to 13:** all held; 1, 3, 5, 7 and 13 were decisive. Lesson 13's citation (a ChatGPT comparison) was weak and is rewritten to cite the walk-forward. Lessons 14 to 25 added (knowledge/lessons.md): XD suffixes, placebos, episodes not events, value as sector effect, formation lag, KSE100 is total return (lesson 20, caught by the Codex critic), conclusions by elimination, model memory invalidates historical judgment tests, "no edge" is not "hold cash", watching is not entering, short-horizon trading loses to costs.
- **New since the brief:** the KSE100 series the orchestrator used is total return; KSE100PR is the price index (data/macro/INDEX_NOTES.md). Any "price-only basket vs KSE100" comparison in the seed understated the basket by about 6 points a year.

## 8. The machine

Pipeline (CLAUDE.md, scripts/): PSX portal client with the X-Req-Id trick (scripts/psx_api.py); 313 KMI price files plus 142 delisted (data/prices_raw/, prices_delisted/); 225,594 timestamped announcements 2005 to 2026 with classes (data/announcements.parquet, scripts/fetch_announcements.py); corporate actions and an adjusted panel (data/corporate_actions.csv, scripts/prices.py); quarterly EPS for 129 names (data/fundamentals/quarterly_eps.csv); NCCPL flows by type and sector (data/macro/fipi_lipi*.csv); index membership history (data/index_changes.csv); macro and external-account series (data/macro/); 4,617 extracted insider trades (data/insider_trades.csv); the daily decision table of 577,794 stock-days with forward paths (data/daily_table.parquet, scripts/daily_table.py); the situation engine and tagged scan (scripts/engine.py); the point-in-time pack builder and replay scorer (scripts/asof.py, replay_bundle.py, score_replay.py); the walk-forward engine (scripts/walkforward.py); an intraday archive started 16 Oct (scripts/collect_intraday.py).

Weekly loop: RUNBOOK.md, run by .claude/skills/psx-weekly/SKILL.md: refresh, score frozen rows, rebuild the daily table, tagged scan, apply the reflex (PLAYBOOK.md section B), freeze the call, log sizes, list missed movers.

From a chat with web search only: reading PLAYBOOK.md, CATALOGUE.md, REGIME_TURN_PLAYBOOK.md and the quality scores; checking the regime checklist from SBP, PBS and PSX pages; reading a filing and applying the six checks; scoring a frozen row from a published result and the closing prices; writing a card in the knowledge/companies format. Needs this repo: anything with the daily table or engine (scan, analogue odds, stage), the as-of packs, the scorer, any backtest, the base-rate table recomputation, corporate-action adjusted returns.

## 9. Models

- **Haiku 5.5:** reliable for scraping, parsing, data builds and file maps; it stuck to scope and reported gaps honestly. Not for anything needing judgment.
- **Sonnet 5.5:** reliable for backtests, sector notes, case studies and engine builds; it flagged its own deviations and spec gaps. Its web search budget ran out in several Phase 1 agents (they fell back to direct fetches). It is the right default; the user said so and the record agrees.
- **Opus 5.5:** earned its cost on the seed audit (found the XD bug, the double counting, the placebo), the test-design reviews, the walk-forward post-mortem, the exam design and the syntheses. Over-wrote length limits routinely.
- **Fable (me) as orchestrator:** the failures were mine: wrong yardstick for the core, false precision, proactivity before alignment; the record is in knowledge/HOW_TO_THINK.md sections 3 and 6.
- **Codex gpt-6-sol:** good for independent replication (active_trading_codex matched the Claude result) and web research with `-c 'tools.web_search=true'`; `--search` is not accepted by `codex exec`.
- **GPT-6 Astra:** the best critic in the programme on two occasions (knowledge/playbooks/astra_peer_review.md, astra_catalogue_review.md); as a trader it hid in cash on the same bundle (data/asof/2026-10-16/REPLY_astra.json). Use it for critique, not calls. The user's plan limits make long Codex tasks risky.
- **All models:** pretraining memory of 2019 to mid-2026 contaminates any historical judgment test (tests/replay_pilot_postmortem.md). Mechanical rules can be backtested; judgment only scored forward.

## 10. Open questions, ranked by likely money impact

1. **Is the turn checklist real?** Fitted to 8 dates. It decides when the reserve (the money that made every 5x run) goes in. Score it live from now; the next readings are 26 Oct, 2 Nov and about 10 Nov (knowledge/REGIME_TURN_PLAYBOOK.md section 6).
2. **Does reading a cause add to the breakout rule?** The only question the live scorecard can answer; 20 weeks of frozen calls (catalysts/scorecard.md). Until then the plain rule is the challenger and it is hard to beat (tests/replay_2026_v2).
3. **Exits.** The library says stops sized to each name beat fixed stops, measured on winners only (Astra's objection). Test the named exit rules on the full breakout population including losers, pre-registered (tests/winners_population.md, knowledge/playbooks/astra_catalogue_review.md).
4. **Business-quality scores vs returns.** 20 names scored by a model from filings; untested against subsequent returns. Score the remaining liquid KMI names and test the top third vs bottom third over 2022 to 2026 with the records frozen at each year end.
5. **Policy implementation odds** (42% as stated, 62% partial): the single most useful number for the catalyst layer, on 26 cases chosen by hand. Extend to a systematic list from the announcements and ECC records (knowledge/playbooks/actors_and_incentives.md).
6. **Survivorship in the small-cap tail and the 55 listed names missing from the panel** (data/prices_listed_missing/, data/DELISTINGS_NOTES.md): zero effect on the liquid basket, unknown for any screen that reaches thin names.
7. **Finqalab's commission rate:** unverified; the user must read it in the app (data/costs.md). It moves the break-even of every short trade.

## 11. File map

See section 12 below, generated from `git ls-files` with one line per file or group and a tag. CORE files, the six that go into the orchestrator's project knowledge: PLAYBOOK.md, PICKS.md, knowledge/HOW_TO_THINK.md, knowledge/CATALOGUE.md, knowledge/REGIME_TURN_PLAYBOOK.md, and this file. REPORT.md and tests/FACTS.md are the first REFERENCE files to open when a number is needed.


## 12. File map (2,436 tracked files; `git ls-files`, 19 Oct 2026)

Tags: **CORE** goes into the orchestrator's project knowledge (six files); **REFERENCE** stays in the repo and is opened when needed; **ARCHIVE** is superseded, historical or raw output. data/raw/ (filings, PDFs) is gitignored and not in the repo.

### Root

| Path | What it is | Tag |
|---|---|---|
| PLAYBOOK.md | The operating rules on one page: the book, the six-check reflex, the regime-turn checklist, exits, the weekly loop, what not to do | CORE |
| PICKS.md | v4 buy report (19 Oct): core LUCK, MEBL, MARI; reserve for the turn; one conditional opportunity; triggers; dates; plain language | CORE |
| ORCHESTRATOR_HANDOFF.md | This file | CORE |
| REPORT.md | The evidence-backed account of how money is made on PSX, 11 sections, every number from a test file | REFERENCE, first to open for a number |
| knowledge/HOW_TO_THINK.md | How the investor thinks, how the research went wrong and was corrected, the thinking rules, the alignment questions, what each phase taught (13 sections) | CORE |
| knowledge/CATALOGUE.md | The if-then casebook of nine situation types with paths, entry and exit hypotheses, failure twins and cases; read its status box first | CORE |
| knowledge/REGIME_TURN_PLAYBOOK.md | Four real turns vs four false bottoms, the signal checklist, leader sequence, entry in thirds, exits, today's reading | CORE |
| CLAUDE.md | Entry point and reading order for any model; rules; environment and the PSX API trick | REFERENCE |
| AGENTS.md | Same brief for non-Claude agents | REFERENCE |
| HANDOFF.md | Session state and continue points, dated updates to 19 Oct | REFERENCE |
| RUNBOOK.md | The weekly loop step by step (refresh, score, scan, calendar, underwrite, freeze, email format, maintenance) | REFERENCE |
| DECISIONS.md | Dated log of every course change with reason | REFERENCE |
| sector_map.md | 16-sector ranking and verdicts, 17 Oct | REFERENCE |
| PLAN.md | The original plan (17 Oct), superseded by HOW_TO_THINK | ARCHIVE |
| .claude/skills/psx-weekly/SKILL.md; knowledge/SKILL_psx_weekly.md (identical copy) | The weekly judgment loop as a skill a chat can run | REFERENCE |

### knowledge/

| Path | What it is | Tag |
|---|---|---|
| knowledge/lessons.md | 25 lessons, each a mistake made and the rule it produced | REFERENCE, read before any analysis |
| knowledge/QUESTIONS.md | 42 questions an experienced investor asks before a call, with evidence weights | REFERENCE |
| knowledge/winners/ (49 cases + 6 syntheses `_*.md`) | Hindsight case studies of big runs by type; the syntheses hold each type's shared signature and rules | REFERENCE |
| knowledge/regime_turns/ (4) | The 2019, 2020, 2022-23 and 2024 turns week by week, with the present read | REFERENCE |
| knowledge/situations/ (12 cases + INDEX.md) | Dated point-in-time situation cases (2019 bottom to EPCL 2026) | REFERENCE |
| knowledge/companies/ (13 cards, 20 `*_quality.md`, quality_scores.csv, QUALITY_README.md) | Underwriting cards with red-team sections; business-quality records and scores | REFERENCE |
| knowledge/sectors/ (16 notes + _unresolved_gaps.md) | Sector levers, state, catalysts, exposed names, past episodes, with Codex gap resolutions | REFERENCE |
| knowledge/playbooks/ (17) | strategy.md, strategy_candidates.md (pre-registered rules), active_trading.md, short_term.md, deals.md, holdco_discounts.md, sector_rotation.md, catalyst_trade.md (refiner retrospective), situation_engine.md, replay_exam.md, practitioner_signals.md, actors_and_incentives.md; reviews: critic_review.md (Codex), consultant_review.md (Fable), astra_peer_review.md, astra_catalogue_review.md, picks_redteam_codex.md | REFERENCE (reviews: REFERENCE, they changed decisions) |

### tests/

| Path | What it is | Tag |
|---|---|---|
| tests/FACTS.md | Headline numbers from all 19+ tests, verbatim, with verdict words | REFERENCE, first to open for a number |
| tests/BASE_RATES.csv | 395 rows of measured odds by situation type and horizon | REFERENCE |
| tests/*.md (30 write-ups) | One per test: seed_audit, refiner_steel_retrospective, sector_momentum_regime, commodity_pkr_sensitivity, flows_predict_sectors, rate_cycle_episodes, index_recomposition_events, calendar_effects, size_liquidity, value_timestamped, results_surprise_drift, insider_cluster_buying, dividend_runup_exdate, quality_within_sector, compounders, corporate_events, results_gap_and_policy, volume_ignition_upper_locks, noise_map_shock_rebound, winners_case_control, winners_population, winners_2026_postmortem, system_walkforward (with audit and rebench), fixed_capital_runs, oracle_and_good_case, active_trading_codex, rs50k_last_year, pattern_mining_daily, informed_capital, replay_pilot_postmortem | REFERENCE |
| tests/out/ (103 raw outputs, incl. replay_pilot/, replay_2026/, replay_2026_v2/, engine scans) | Raw run output behind every write-up | ARCHIVE |

### catalysts/

| Path | What it is | Tag |
|---|---|---|
| catalysts/frozen_predictions.csv | 42 frozen calls with probabilities; append-only; outcome columns filled as events land | REFERENCE |
| catalysts/scorecard.md | Brier scoring rules and the (empty) record | REFERENCE |
| catalysts/catalyst_calendar.csv (126 rows), dividend_calendar.csv (69) | Dated events by sector and ticker; expected ex-dates and net amounts | REFERENCE |
| catalysts/draft_predictions.csv | Drafts before freezing | ARCHIVE |

### data/ and scripts/

| Path | What it is | Tag |
|---|---|---|
| data/prices_raw/ (313), prices_delisted/ (315), prices_listed_missing/ (55) | Daily OHLCV from the PSX portal | REFERENCE |
| data/panel_close*.parquet, panel_volume.parquet; data/corporate_actions.csv and notes | Price panels, raw and adjusted; the corporate-actions table | REFERENCE |
| data/announcements.parquet (225,594 rows) | Timestamped PSX announcements 2005 to 2026 with classes | REFERENCE |
| data/daily_table.parquet/ (10 partitions) + DAILY_TABLE_NOTES.md | 577,794 stock-days of features and forward paths | REFERENCE |
| data/fundamentals/ | quarterly_eps.csv (129 names) and notes | REFERENCE |
| data/macro/ (40 series + README, INDEX_NOTES) | Rates, bills, CPI, reserves, current account, FX, oil, commodities, indices (TR vs PR), NCCPL flows | REFERENCE |
| data/index_changes.csv, index_recomp_log.csv, index_members/ (50), kmi_allshare_2026-06-05.csv, INDEX_DATA_NOTES.md | Index membership history | REFERENCE |
| data/winners_library.csv (382 liquid runs), winners_library_thin.csv (1,376) | The winners population with path metrics | REFERENCE |
| data/deals_history.csv, delistings.csv, insider_trades.csv (+ docs, universe), events_shocks*.csv, costs.md, symbols.csv, payouts_raw.csv | Supporting datasets with their notes | REFERENCE |
| data/asof/ (42 date folders) | Point-in-time packs and bundles; REPLY*.json are replay outputs | REFERENCE (REPLY files ARCHIVE) |
| data/intraday/ | Tick archive from the 16 Oct 2026 session | REFERENCE |
| scripts/psx_api.py, prices.py, asof.py, replay_bundle.py, score_replay.py, daily_table.py, engine.py, walkforward.py, walkforward_rebench.py, screen_breakout.py, sector_momentum.py, collect_intraday.py, refresh_prices.py, fetch_*.py, macro_*.py, idx_*.py, build_*.py, survivorship.py | The pipeline (CLAUDE.md Environment lists the entry points) | REFERENCE |
| scripts/tests/ (28), scripts/ca/ (9), scripts/codex/ (5) | One script per test; the corporate-actions pipeline; Codex's independent engines | REFERENCE |
| scripts/audit/ (17), scripts/walkforward_v0.py, scripts/refetch_ids.py, scripts/insider_sample.py, insider_dl.py, _tmp_kmi.json, data/insider_trades_run1.csv, data/insider_pdf_reads.txt, picks/PICKS_v3.md | Seed-era audit scripts, earlier versions, one-off fixes | ARCHIVE |

### seed/

| Path | What it is | Tag |
|---|---|---|
| seed/CLAUDE.md, DATA_README.md, LESSONS.md, FORECAST_REGISTER.md, PSX_STATE (living state, read first).md, scripts/ (10), data/ (538) | The orchestrator's original brief, state, register, scripts and data, untouched | ARCHIVE (FORECAST_REGISTER.md stays referenced for scoring) |
