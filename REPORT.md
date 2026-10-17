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

**What is untested or half-tested, and matters:** disclosed sponsor buying (the ASL 2026 case was flaggable from public filings on 9 Apr; our sample had 7 clean clusters, out-of-sample 4 of 4 winners, median +8%; a full extraction of 2019 to 2026 filings is running); the "ignored strong quarter" setup (the PRL 2026 case; +6.4% median at 120 days, n 42, but the edge sits in 2024 to 2026 and in low P/E, and it fails its own placebo inside the walk-forward); deal arbitrage (11 completed offers 2021 to 2026, median premium +40% to the pre-announcement price, median spread 15% the day before the offer, median price 13% below the offer a month after completion; failures not yet counted).

**The updated model.** Money on PSX is made in three ways a retail investor can actually access. First, by staying invested through the cycle in liquid Shariah names, which compounds at 11 to 14% a year with 40 to 60% drawdowns. Second, by holding the right sectors for the rate regime (banks, E&P, fertilizer while the curve prices hikes; cyclicals once CPI turns and the 6-month T-bill drops below the policy rate) and the cheapest sound name in each, which history says adds 3 to 8 points a year but with no proof it will again. Third, by a small number of stock-specific situations where public information is ignored by the market for weeks: a sponsor buying in the open market, a quarter that changes the earnings base, a tender offer with a wide spread. These are rare, the base rates are thin, and each one needs underwriting. Everything else that looks like an edge on PSX, including the "chaotic small caps" idea, is noise or someone else's exit.

**What this means for Rs50k a month.** Keep at least 60% in a concentrated core of 4 to 6 liquid KMI names chosen by regime sector and in-sector value and quality, bought every month, sold only on a thesis breaker or a KMI deletion. Keep up to 40% for dated catalyst bets, but only with a written card, a red team, a frozen prediction and a measured base rate. If no bet qualifies within four weeks, the money goes into the core. Expect 40 to 60% in a good year and a −30% year every four or five. Ten to fifteen percent a month is not available from any tested strategy; a single position can do it, a portfolio cannot.

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
- The sponsor-buying signal, the one with a clean recent case, is undertested because half the insider filings had no PDF id in the scrape. A full extraction is running and will update tests/insider_cluster_buying.md.
- Deal base rates exclude lapsed and withdrawn offers until data/deals_history.csv lands.
- Nothing here is out of sample. The frozen-prediction register (catalysts/frozen_predictions.csv, 27 rows for 19 to 29 Oct) is the start of the out-of-sample record; the scorecard will show within a month whether our probabilities mean anything.

## 7. How to use this repo

CLAUDE.md is the entry point. RUNBOOK.md is the weekly loop. DECISIONS.md says why conclusions changed. knowledge/ is the model: sectors, playbooks (strategy, catalyst trade, deals, holdco discounts, practitioner signals, sector rotation, critic review), company cards, lessons. tests/ holds one markdown per test with n, median, win rate, worst case and placebo; tests/FACTS.md indexes them. catalysts/ holds the calendar, the dividend calendar, the frozen predictions and the scorecard. scripts/prices.py is the shared loader; scripts/walkforward.py the strategy engine; scripts/psx_api.py the PSX portal client.
