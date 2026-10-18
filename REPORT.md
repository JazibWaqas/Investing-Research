# REPORT.md — How money is made on the PSX, and what the evidence actually supports

Written 18 Oct 2026 by Claude Fable 5.1 after a research session of about 20 hours, 60-odd subagents (Haiku, Sonnet, Opus, Codex gpt-6) and about 15 million tokens. Data to 16 Oct 2026. Everything here is reproducible from `scripts/` and `data/`; every number is quoted from a file in `tests/` (see `tests/FACTS.md` for the index). Read `PICKS.md` for the positions. Read `knowledge/lessons.md` before analysing anything.

## 1. The answer in one page

**What was tested.** Twelve quantitative tests on 456 names of daily prices (Oct 2016 to Oct 2026), 225,594 timestamped PSX announcements (2005 to 2026), quarterly EPS for 129 names, NCCPL flows by investor type and sector, index membership history, 84 MPC decisions, and commodity and PKR series. Each test had an Opus design review for lookahead and survivorship, a placebo of random entries, and a verdict rule fixed before the run. Five strategies were pre-registered and then walk-forward tested with Rs50,000 monthly deposits from Jan 2018. Twelve stocks were underwritten by Opus and red-teamed by Sonnet. A Codex critic reviewed the whole program.

**What works, in order of strength:**
1. **Being invested.** Rs50k a month into the KMI All Share index from Jan 2018 (Rs5.30m deposited) was worth Rs14.10m on 16 Oct 2026, 14% a year total return. Every month spent waiting in cash cost money. February was the only reliably weak month (negative in 9 of 10 years, mean −4%), and even that is an exploratory screen, not a rule.
2. **Regime-aware sector rotation with in-sector value (strategy S3).** Rs17.6m frozen, Rs18.6m to Rs20.4m with dividends accrued, 1.25x to 1.44x the index. But its sector lists were read off the same history, two stocks (SAZEW, LUCK) made 88% of the profit, and it is down 25% in 2026. It is a hypothesis with one good decade behind it, not a system.
3. **Sector momentum, long-short only.** Top-3 minus bottom-3 sectors by 6-month return earned +2.7% net per 3 months, 65% of windows, t 1.7. Retail cannot short, and long-only top-3 lost 0.4% a quarter to the KMI All Share after costs.
4. **The first rate cut of an easing cycle.** KSE100 +40% and +49% in the 120 days after the first cut in 2020 and 2024, against a placebo median of +8%. Two episodes. The Dec 2025 cut gave +1%. Useful as a regime marker, useless as a bet size.
5. **Quality within sector.** Top third minus bottom third on ROE, cash conversion and EPS stability: median +5.8% over 12 months, 69% win, placebo p 0.054, three independent years. Weak and unproven.

**What does not work, on this data:** stock momentum, volume footprints and pump chasing (no different from random entry); earnings-yield value (four cohorts, net spread −1%, and the orchestrator's +28 pts was a sector effect plus a bug that dropped 29 names); post-earnings drift (positive surprise 60-day net median −2.3% vs placebo −2.2%); pre-result run-ups; dividend run-ups and ex-date games (the price falls by exactly the dividend); investor flows by type or sector (every pre-registered series fails); commodity and PKR moves as a lead (same-month betas only); index recompositions (nothing after costs); IMF events; calendar effects other than February.

**What active trading could have done (added 18 Oct after the user's challenge; tests/fixed_capital_runs.md, oracle_and_good_case.md, winners_case_control.md, active_trading_codex.md).** A fixed Rs50,000 on 1 Oct 2024 made 1.36x in our regime strategy, 1.81x in the KMI index, 2.03x in the KSE100, and 5.4x in the best single name (8 of 87 liquid names made 3x). Perfect foresight would have made 45x to 265x in every window, so the opportunities exist; predicting them is the problem. Of 15 pre-listed simple active systems in two independent implementations, exactly one held up: buy names breaking to 52-week highs, hold with a 20% trailing stop, at most three positions. It made 2.5x to 3.3x in the three bull windows (2020 to 2022, 2022 to 2024, 2024 to 2026) and 0.8x to 1.1x in the two hike-regime windows, with 18 to 44% drawdowns, one or two trades carrying each window. Nothing reached 3x in 2024 to 2026. Every other system was a one-window fluke. A case-control study of all 129 six-month doublers since 2017 found them unpredictable from public data at the start (out-of-sample precision 5.8% against a 4.5% base rate, equal to a shuffled placebo); the only knowable thing was timing, since doublers were 2.5 to 2.8 times more common when the 6-month T-bill sat below the policy rate. Consequence: the 25% satellite is now the breakout rule, run mechanically, and the discretionary catalyst triggers are paper.

**What is untested or half-tested, and matters:** disclosed sponsor buying (the ASL 2026 case was flaggable from public filings on 9 Apr, but the full extraction of 4,617 insider trades 2019 to 2026 found no cluster effect: 37 clusters, 63-session median −0.4%, p 0.47; only director buys out of sample, n 16, and single insider sales as a negative, median −3.1% at 21 sessions, p 0.006, remain as leads); the "ignored strong quarter" setup (the PRL 2026 case; +6.4% median at 120 days, n 42, but the edge sits in 2024 to 2026 and in low P/E, and it fails its own placebo inside the walk-forward); deal arbitrage (75 takeover intentions 2018 to 2026: only 48% completed, every withdrawal came before the public offer, 25 of 28 that reached an offer completed; buying after the intention notice had a median −1.2% and lost 14% to the index, buying after the offer announcement a median +1.1%; so the only tradable moment is after the offer is published, and the edge is thin).

**The updated model.** Money on PSX is made in three ways a retail investor can actually access. First, by staying invested through the cycle in liquid Shariah names, which compounds at 11 to 14% a year with 40 to 60% drawdowns. Second, by holding the right sectors for the rate regime (banks, E&P, fertilizer while the curve prices hikes; cyclicals once CPI turns and the 6-month T-bill drops below the policy rate) and the cheapest sound name in each, which history says adds 3 to 8 points a year but with no proof it will again. Third, by a small number of stock-specific situations where public information is ignored by the market for weeks: a sponsor buying in the open market, a quarter that changes the earnings base, a tender offer with a wide spread. These are rare, the base rates are thin, and each one needs underwriting. Everything else that looks like an edge on PSX, including the "chaotic small caps" idea, is noise or someone else's exit.

**What this means for Rs50k a month.** Keep 75% in a concentrated core of three large, liquid, cheap, dividend-paying KMI names, chosen by the walk-forward's mechanical rule (cheapest sound name in each of the sectors that fit the rate regime), bought every month, held through 40 to 50% drawdowns, sold only on a thesis breaker or a KMI deletion. The regime label is context, not the reason to own them: the regime tilt has no measured edge, and the core's honest expectation is the index's 11 to 14% a year. Keep 25% for one dated catalyst bet a month, only with a written card, a red team, a frozen prediction and a price you will not chase; if nothing qualifies within four weeks, that money goes into the core. The satellite grows only when the frozen-prediction scorecard shows a hit rate above its pool after ten or more trades. Expect 40 to 60% in a good year and a −30% year every four or five; in hike years the index has lost to T-bills, and the one hike year that broke the pattern (2023, +53%) is the reason not to wait. Ten to fifteen percent a month is not available from any tested strategy; a single position can do it, a portfolio cannot. Two independent reviews (knowledge/playbooks/picks_redteam_codex.md, consultant_review.md) shaped this: both cut the satellite and rejected unmeasured overrides of the mechanical core; they split on whether to buy Monday, and the deposit-habit argument won.

## 2. What was established before this session, and what survived

The orchestrator's seed findings (seed/CLAUDE.md section 3) were reproduced and audited (tests/seed_audit.md):

| Seed claim | Status after audit |
|---|---|
| Deep value +28 pts/yr, 6 of 7 cohorts | Reproduces as coded, but 29 of 108 names were dropped by an ex-dividend suffix bug, dividends were double counted, and the spread is −1.3 pts within sector. With publication dates and four cohorts: nothing. |
| Rate cuts +33% at 120 days | +37% corrected for pre-data cuts; 13 cuts are 3 cycles; first cuts +40% and +49%, Dec 2025 +1%. Weak, directionally right. |
| Sector rotation at turns (banks and power lag) | Two episodes; power's lag is −22 instead of −42 if the base is one month earlier. Anecdote. |
| Sector momentum +3.3%/3m, 67% | Reproduces; overlapping windows, t 1.3 to 1.7; the short leg carries it. |
| Stock momentum and pumps fail | They equal random entries (20-day median −1.5%, 43% win for both). "Fails" was overstated; "no edge" is right. |
| IMF agreements no effect | Not detectable, n 12, confidence interval ±5.7%. |
| CPI turn +44% | 33 months in 10 runs, one run supplies 21; earlier runs were followed by −10 to −15%. Weak. |

New lessons 14 to 21 in knowledge/lessons.md record the traps found: strip XD/XB suffixes, always run a placebo, count episodes not events, PSX's KSE100 is a total-return index, and a conclusion reached by eliminating alternatives is a hypothesis until tested.

## 3. The tests, with numbers

| Test | Verdict | Headline | n or episodes |
|---|---|---|---|
| Sector momentum and regime | long-short works modestly; long-only no; regime tilt no edge | +2.66% net per 3m, 65% win, t 1.73; long-only vs KMI −0.41% | 32 windows per offset |
| Commodity and PKR sensitivity | no predictive lead | E&P on Brent same-month beta +0.94 pts per 10%, t 4.0; refiners after Brent +20%: 7 episodes, fails once 2020 is removed | 7 and 5 episodes |
| Investor flows | fails | best pre-registered IC +0.045 (insurance), t 1.3; all top-3 spreads negative | 120 periods |
| Rate-cycle episodes | weak | first cut 120d median +39.8% vs placebo +7.9%; 60d coin flip | 2 cycles |
| Index recompositions | nothing | KMI30 additions +1.9% mean announcement to effective, too thin after costs | 617 events |
| Calendar | nothing | February −3.95% mean, 9 of 10 years negative; nothing else | 10 years |
| Size and liquidity | weak, reversed | least liquid tercile +8.4%/yr vs most liquid +3.1%, t −1.2 | 10 years |
| Value with publication dates | nothing | net spread −1.2 pts, 2 of 4 cohorts | 4 cohorts |
| Results surprise and drift | nothing | positive surprise 60d net median −2.3% vs placebo −2.2%; ignored-quarter +6.4% at 120d, n 42, not robust | 12 seasons |
| Insider cluster buying | insufficient | 7 clean clusters; out-of-sample 4 of 4 up, median +8% | 22 symbols sampled |
| Dividends | nothing | ex-day drop ratio 1.01; run-up into notice +1.1% vs −0.7% placebo on 9 clusters | 378 ex-dates, mostly 2025 to 2026 |
| Quality within sector | weak | top minus bottom third median +5.8%, 69% win, p 0.054 | 3 years |

The equal-weight liquid basket returned +44% price-only since 2017 against +245% for the KSE100. That gap is not a large-cap premium: about 6 points a year is dividends (KSE100 is total return; its implied yield 2020 to 2026 was 6.2% a year), about 24 points of the gap is daily rebalancing noise, and the rest is cap-weighting toward a few winners. Inside the investable set, less liquid names beat more liquid ones weakly. The KMI All Share total-return index compounded at 11.4% a year, KMI30 at 11.6%, KSE100 at 13.5%.

## 4. The walk-forward (tests/system_walkforward.md)

Five strategies were frozen in knowledge/playbooks/strategy_candidates.md before any backtest. Rs50,000 on the first trading day of every month, Jan 2018 to Oct 2026, 0.5% round trip, KMI membership point in time, survivors only.

| Strategy | Final value, frozen | With dividends accrued (estimate) | Ratio to KMI All Share TR (Rs14.10m) | Max drawdown |
|---|---|---|---|---|
| B0 equal-weight liquid KMI | Rs12.42m | Rs12.9m to 13.7m | 0.88 to 0.97 | −61% |
| B1 orchestrator's value plus regime | Rs13.11m | Rs14.1m to 14.8m | 0.93 to 1.05 | |
| S2 momentum sectors plus value | Rs14.17m | Rs15.3m to 16.2m | 1.01 to 1.15 | |
| S3 regime sectors plus value | Rs17.63m | Rs18.6m to 20.4m | 1.25 to 1.44 | −50% |
| S4 S3 plus earnings satellite | Rs16.54m | Rs17.9m to 19.5m | abandoned: below S3 | |
| B2 12 largest liquid names, traded-value weighted | Rs11.55m | Rs12.2m to 13.0m | 0.82 to 0.92 | −64% |
| 70% B2 plus 30% S3 | Rs13.39m | Rs14.1m to 15.2m | 0.95 to 1.08 | −59% |

Opus audit findings: the engine's timing is clean; the 132 names with fundamentals were chosen on 2026 liquidity and beat the rest by 2.3% a month, which inflates every fundamentals-based strategy (S3 falls to 1.35x B0 against a B0 restricted to the same names); the earnings satellite fails its placebo when drawn from its own pool, so it is abandoned; SAZEW and LUCK made 88% of S3's profit; three S3 sales on 1 Apr 2026 lost Rs5.15m on a regime turn. Calibration from the trade log: a value pick inside a favoured sector won 61 to 66% of the time with a median of +4 to +9%; an ignored-quarter pick won 56 to 58% with a median of +2 to +3%, no better than its pool.

Conclusion: no passive basket a retail investor can hold matched the index, and the only strategy that beat it is in-sample and concentrated. The honest reading is that regime-aware sector choice plus in-sector value is the best available core, held with the knowledge that its historical edge may be luck.

## 5. The catalyst layer (knowledge/playbooks/catalyst_trade.md, sector notes, catalyst calendar)

The 2026 refiner rally could have been flagged twice: on 29 Apr, when PRL's March-quarter result put it at about 2x trailing earnings and the market treated it as a one-off (the stock lagged for ten weeks), and on 8 to 9 Jul, when the US-Iran truce collapsed and PRL rose on 9x volume while the market fell; the refinery policy was approved 28 Jul. Buying at the 9 Jul close returned +155% by 16 Oct. There was no steel rally: ASL doubled because its sponsor bought in the open market on 7 Apr, 21 May and 3 to 4 Aug, each purchase public within two days. The size of both moves was luck.

Sixteen sector notes (knowledge/sectors/) give each sector's profit levers, where they stand with dated sources, what changes in the next 3 months, the exposed KMI names, and past 30%+ episodes. The synthesis (sector_map.md) ranks E&P, fertilizer (FFC), Islamic banks (MEBL), OMC (PSO) and tech (NETSOL) as the sectors to be in while the curve prices hikes, and chemicals, textiles, pharma and steel as the ones to avoid. No sector today has all three parts of the refiner setup (earnings already turned, spread widening, policy pending). The catalyst calendar (catalysts/catalyst_calendar.csv, 126 rows) and the ten weekly watch signals are the operating layer; the Codex critic is right that the signal list is a watch design, not a tested model.

Twelve underwriting cards (knowledge/companies/) all came back WATCH or AVOID after red team. Expected 12-month returns after the red team: GHGL +8 to 10%, PSO +4%, PPL +4%, MEBL +3%, OGDC +2 to 3%, FFC +3%, LUCK +3%, NETSOL +2%, ATRL +0.5%, SNGP +2%, EPCL about 0% at the market price (the public offer covers 17.5% of shares), SAZEW about −9%. These are probability-weighted price targets with wide error bars; the market sits near its high with the curve pricing a hike. At 16 Oct prices there is no 30% bet the evidence supports. PICKS.md therefore gives entry limits and result-dependent triggers rather than buys at any price, while the core gets bought now.

## 6. Where the program is wrong or thin (from the Codex critic and the audits)

- Survivorship: the main panel holds only the 456 names listed on 16 Oct 2026. Recovery of 169 delistings since 2016 (data/delistings.csv, 151 with prices from the portal) shows the effect on the liquid equal-weight basket is about zero (+44.1% vs +44.5% with the delisted names), because only 38 delisted names ever passed the Rs5m liquidity filter. The bias remains in any screen that reaches into illiquid or low-priced names, and 55 still-listed non-panel names (POL, APL, HASCOL among them) are in data/prices_listed_missing/ and not yet merged.
- Dividends: complete only from Nov 2024. Pre-2024 strategy returns are price-only or accrued from fiscal-year yields.
- S3's sector lists were chosen with knowledge of 2018 to 2026. Its 1.25x to 1.44x is an upper bound.
- Quality and catalyst definitions were written after seeing the 2026 winners. Their tests are weak or failed; the strategy keeps them only as watch screens.
- The sponsor-buying signal is now tested on the full universe and not supported (extraction recall about 60%, so the test is a floor, not a ceiling).
- Deal base rates now include lapsed and withdrawn offers (data/deals_history.csv, 75 intentions); offer prices are missing for 53 of them because the filings are scans.
- Nothing here is out of sample. The frozen-prediction register (catalysts/frozen_predictions.csv, 27 rows for 19 to 29 Oct) is the start of the out-of-sample record; the scorecard will show within a month whether our probabilities mean anything.

## 7. How to use this repo

CLAUDE.md is the entry point. RUNBOOK.md is the weekly loop. DECISIONS.md says why conclusions changed. knowledge/ is the model: sectors, playbooks (strategy, catalyst trade, deals, holdco discounts, practitioner signals, sector rotation, critic review), company cards, lessons. tests/ holds one markdown per test with n, median, win rate, worst case and placebo; tests/FACTS.md indexes them. catalysts/ holds the calendar, the dividend calendar, the frozen predictions and the scorecard. scripts/prices.py is the shared loader; scripts/walkforward.py the strategy engine; scripts/psx_api.py the PSX portal client.


## 8. The judgment exam (added 18 Oct 2026, evening)

After the user reframed the goal as building judgment that transfers (knowledge/HOW_TO_THINK.md), the program added a question list (knowledge/QUESTIONS.md), a situation library of twelve dated cases (knowledge/situations/), a noise map of 157 events (geopolitical shocks reprice on day one and revert; SBP, budgets, ratings, politics and IMF headlines are ignored on day one; buying the index 5% below a shock's pre-event close won 78% of the time at 20 sessions), an actor and incentive map (announced policies implemented as stated 42% of the time, 62% with partial; IMF-backed revenue measures 8 of 12, industry-paid items 3 of 14), external-account and valuation series (reserves, current account, import cover, KSE100 P/E 7.9x against a 12.4% bill), four more opportunity-type tests (volume with upper locks: nothing; corporate events: nothing except a nine-trade split lead; results-day gaps: watch; policy windows: only the first rate cut), a compounders study (3x in five years for 2 to 5% of names from 2017 to 2018 starts and 16 to 23% from 2019 to 2021 starts; a growth rule has too little history to test), business-quality scores for 20 growth candidates (knowledge/companies/*_quality.md), and a blind replay exam (knowledge/playbooks/replay_exam.md, scripts/asof.py, replay_bundle.py, score_replay.py).

The exam's result, in full in tests/replay_pilot_postmortem.md and HOW_TO_THINK.md section 10: the replay model remembers every date in our data, so judgment cannot be validated on history; the method documents as first written made the agent hide in cash; with the investor's posture stated, the agent behaved sensibly (exposure 50 to 75%, growth core, 4 entries, 75% hit, +2.8% vs +1.2% for the index at 60 sessions on 15 dates in 2026) but did not beat the plain breakout rule at 120 sessions and did not cut exposure before falls. Verdict by the pre-registered rules: adds nothing distinguishable from zero, sample too small and in one regime. The live weekly scorecard, run with the same pack, brief and scorer (see .claude/skills/psx-weekly/SKILL.md), is the exam from here; the breakout rule runs alongside as the challenger.

What a fair reader should conclude: the repo now holds the data, the base rates, the case library, the question list and an auditable weekly process that produces frozen, scoreable calls. It does not yet hold proof that the judgment layer adds value, and it holds evidence that the mechanical trend rule is hard to beat. Neither the investor's return target nor transfer across regimes is established. Future frozen decisions have to earn those claims.


## 9. The short-term study (added 18 Oct 2026, night)

Built: a daily decision table (577,794 stock-days, 101 columns, point in time, forward paths with locks, excursions and filings), forty pre-registered short-horizon rules with six exits and matched random placebos, a direct test of the informed-capital hypothesis, and a situation engine (scripts/engine.py) that returns analogue outcome distributions for any stock-day and scans a date for live situations. Costs from data/costs.md (about 0.5% round trip in liquid names, 15% CGT separately).

Result: no short-horizon mechanical edge on PSX after costs. 37 of 40 rules lose at the next close; 18 of 240 rule-exit tests reach p 0.01 against about 2.4 expected by chance, and none holds out of sample. The best fully reinvested Rs50,000 book (new 252-day high, 20% trailing stop) has a median six-week multiple of 1.00 and makes money in 49% of windows, against 0.98 and 43% for random names with the same exit; the "buy the day's top gainer" rule turned Rs50,000 into Rs15,050 over the last three months. News-less rises are followed by a filing 26.6% of the time against 26.7% for quiet names in the same state; joining them has a negative median at every exit. The engine's analogues for SSGC (Oct 2024) and PRL (Jul 2026) had negative medians; both winners were outliers. Monday's scan (16 Oct close) shows eight live situations, none with a positive analogue median at five sessions. Full write-up: knowledge/playbooks/short_term.md; tests/pattern_mining_daily.md, informed_capital.md; knowledge/playbooks/situation_engine.md.
