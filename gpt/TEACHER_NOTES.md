# TEACHER_NOTES.md — what the documents do not tell you

> **Update, 21 Oct 2026 (later the same day):** two things in this snapshot are superseded. Lucky group names are allowed when worth the declaration, and there are no fixed rules: no 80/20 split, no standing reserve, no 5% loss budget, no cash cap. Situations decide; every call carries odds and an upside-against-downside case; Jazib accepts a loss of up to about 30% on a call with a large upside. See PLAYBOOK.md and PICKS.md version 6. Where this file argues about those rules, read it as the history of the reasoning.

From the Claude session that ran the research (Fable 5.1, then Opus 5.5), 21 Oct 2026, to the assistant that will advise Jazib next. You have read ORCHESTRATOR_HANDOFF, PLAYBOOK, PICKS, HOW_TO_THINK, CATALOGUE, REGIME_TURN_PLAYBOOK, lessons, FACTS and PROJECT_INSTRUCTIONS. This file is the layer underneath them: why things came out the way they did, where the documents are weaker than they read, and how to reason when you meet something new. Where I cite a number, the file is named; where something is my interpretation, I say so.

## 1. What we were actually trying to do

The brief the research started from (seed/CLAUDE.md, written by an earlier "orchestrator" chat) asked for 30%+ upside picks for Rs50k now and Rs50k a month, a catalyst layer, and seven research phases. The orchestrator had already built a value-and-macro model and had missed the 2026 refiner rally. That framing, "find 30% picks and a catalyst calendar", is what I executed for the first day, and it was the wrong reading of the person.

What Jazib actually asked, in order, as he clarified it over two days:

1. "Figure out how money is really made on the PSX." He meant a learnable model of the market, not a list.
2. "I don't know anything about the market; what would a 50-year veteran look at?" He wanted the judgment that produces picks, written down so other models and he himself could use it.
3. "50 to 75% in solid blue chips that actually grow, 25% risky to win big." I heard "solid" and built a yield core (FFC, OGDC, HUBC, then FABL). He meant growing businesses (his example was LUCK, which keeps expanding). Dividends are inconsequential at his size; he said so twice before it registered.
4. "If I'd given you Rs50k two years ago, what would it be worth?" and "what was the best case?" These were not requests for a backtest; they were tests of whether my method was any good. My walk-forward had reported Rs17.6m on Rs5.3m of deposits and I had treated that as a result. It was mostly deposits. On a fixed Rs50k the best strategy made 1.36x while the index made 1.81x (tests/fixed_capital_runs.md).
5. "Short term is where prediction should work." He then built this out: a stock up 7% today, a ceasefire on a Sunday, "join, milk it, leave". I tested 40 short-horizon rules; none survived (tests/pattern_mining_daily.md). He did not accept "nothing works" as the end, and he was right not to: the next reframing was the useful one.
6. "Study the actual winners with hindsight, case by case, so we never ignore a move that has started." This produced the winners library and the catalogue. He was explicit that each case can have its own rule; generalisation is optional; what is not acceptable is absence.

Stated objectives versus my interpretations, so you can keep them apart:

- Stated: financial independence by about 30; capital gains over dividends; growth businesses for the core; an opportunity sleeve hunting large moves; accepts big drawdowns; cuts losers to fund live situations; takes some profit on big winners; KMI only; "money in" is not a fixed Rs50k; no master strategy; never ignore a move; be told no with evidence.
- My interpretations, not his words: the 80/20 core-reserve split, the 5% loss budget per idea, the 12-month reserve release rule, the three-name core, "one opportunity at a time". These are policy choices I made to turn his posture into rules. He has not objected to them, but he has not chosen them either. Present them as proposals.
- New constraint (21 Oct): LUCK and any Lucky group company are off-limits because his father works at Lucky Cement and a holding needs a declaration. I knew his father worked there from 18 Oct and still put LUCK at the top of the core; I should have asked. Ask about conflicts before recommending a name connected to anything he has told you about his life.

What changed my understanding was not more data. It was his questions. Every reframing above came from a plain question that the method should already have been able to answer and could not. Treat his questions that way.

## 2. How PSX works, causally

This section is interpretation built on the measurements; I mark where it is measured.

**The balance of payments is the master variable.** Pakistan's cycles run: reserves fall, the rupee weakens, inflation rises, the State Bank hikes, an IMF programme is negotiated, reserves are rebuilt, inflation falls, the bank cuts. Equities sit at the end of that chain. Both deep bears in the data (2017 to 2019 and 2021 to 2023) were balance-of-payments crises; both big bulls followed IMF programmes and reserve rebuilds (knowledge/situations/01, 03, 12; knowledge/regime_turns/). So the first question about the market is always where the external account is, not what the index did last week.

**Rates set the multiple; the multiple sets the market.** When the 6-month T-bill pays 12 to 22%, a stock on 8x earnings (12.5% earnings yield) competes with a risk-free bill, so the whole market derates. The current KSE100 earnings yield is about equal to the bill (data/macro/earnings_yield_vs_tbill.csv). In hike regimes this compresses almost everything: in the two previous hike bears only about 4% of liquid names rose at all, and the index hid the damage (2021 to 2023 the index fell 22% while the median stock fell 52%) (knowledge/situations/03, 12). When cuts begin the reverse happens fast and broadly, which is why every 5x run since 2016 started within a turn (tests/winners_population.md: all 34 runs of 5x or more were multi-year, 23 began within three months of a market low).

**Regulated sectors earn what the state lets them earn.** Refiners (crack caps, deemed duty, upgrade policy), E&P (wellhead gas formulas), OMCs (margins set by OGRA), fertilizer (gas price), power (tariffs, capacity payments). Their earnings move on policy decisions, and policy is a probability: 42% of announced decisions were implemented as stated, 62% with partial implementation, fast when the IMF wanted the revenue and slow when industry had to be paid (knowledge/playbooks/actors_and_incentives.md; 26 hand-picked cases, so suggestive). The refinery upgrade policy took 37 months. A "policy is coming" story is worth about a coin flip until you know who gains and who decides.

**Profit is not cash.** Circular debt means E&P and OMC profits sit as receivables: MARI has Rs86bn of trade debts, Rs62bn overdue, and an SECP provisioning exemption that expires 31 Dec 2026 (knowledge/companies/MARI.md). A sector can report record earnings and still need to borrow. This is why the cash-conversion check was added to the reflex after the Astra review.

**Markets learn slowly about earnings the crowd distrusts.** PRL's March 2026 quarter (EPS 15.78 after a loss) put it at about 2x earnings; the market treated it as a one-off for ten weeks and the stock lagged (knowledge/playbooks/catalyst_trade.md). That delay is real and it is where the 2026 refiner money was. My interpretation of why: in regulated sectors with a history of one-off inventory gains, investors wait for a second quarter or a policy decision before believing a jump. The edge is not seeing the quarter; everyone saw it. It is judging whether it is repeatable before the market does.

**Trends persist because information and conviction diffuse.** The breakout rule's results (2.1x to 3.3x on a fixed Rs50k in the three bull windows across the two implementations, tests/oracle_and_good_case.md, tests/active_trading_codex.md) are consistent with a market where funds, then retail, arrive in waves after a re-rating starts. It is also consistent with luck plus selection (best of 15 rules). Treat "the trend continues" as a tendency of confirmed moves with visible causes, not a law.

**Who is on the other side.** At the bottoms of 25 shocks, banks, DFIs, companies and individuals were net buyers; mutual funds sold at every one (tests/noise_map_shock_rebound.md). Foreign corporates sold the fall and kept selling the rebound. My interpretation: mutual funds face redemptions in panics and are forced sellers, which is exactly when patient money should buy. Flows do not predict sector returns in general (tests/flows_predict_sectors.md), but they tell you who is being forced.

**What the market ignores and what it reprices.** Geopolitical shocks are the one headline type the market reprices on the day and then gives back: ten geopolitical falls of 5%+ rebounded a median +27.8% in 60 sessions and nine of nine regained their level (tests/noise_map_shock_rebound.md). SBP decisions, budgets, ratings, IMF staff deals and domestic politics are ignored on the day. Jazib's father said the market was "used to" the Iran war headlines; the data agrees. My reading: Pakistani business has lived through so much political noise that it prices only what changes cash flows or the external account.

**Sponsors and minorities.** Control of most listed companies sits with a few groups (Fauji, Nishat, Lucky and Yunus, Engro and Dawood, Arif Habib, JS, Hub Power, Attock). Their behaviour matters more than in a dispersed market: partial tender offers that buy only part of a minority's shares (EPCL: about 53% of a holding at Rs38.60 at full tender, knowledge/playbooks/deals.md), rights issues at bad moments (rights issues lose a median 9% over 60 sessions, tests/corporate_events.md), and open-market sponsor buying that occasionally signals a real re-rating (ASL 2026). Systematically, insider cluster buying does not predict returns (37 clusters, median −0.4%, tests/insider_cluster_buying.md); individually, a sponsor repeatedly buying in the open market after injecting equity was the ASL case. Know the difference between a base rate and a case.

**Thin floats are someone else's exit.** Volume spikes with upper locks and no filing lose money after a stop (median −11% to −14%, worse than random, tests/volume_ignition_upper_locks.md). The library's "no visible cause" type has a negative base rate. QUICE and CRTM in 2026 made multiples but were thin enough that a small account would have been the liquidity for the people leaving (tests/winners_2026_postmortem.md).

What I understand now that I did not at the start: the PSX is not a market where clever screens find mispriced stocks; it is a market where the macro cycle decides the size of the opportunity set, regulated earnings decide which sectors move, and the edge for a retail investor is mostly in being invested in the right sectors at the turn, recognising confirmed situations early enough, and not being the exit liquidity for operators.

## 3. The discoveries that changed my thinking

Graded: **demonstrated** (reproduced, placebo-controlled, out of sample or on two implementations), **suggestive** (consistent but small n or in-sample), **hypothesis** (plausible, untested).

1. **The value factor was a bug and a sector bet.** Believed: cheap stocks beat expensive by about 28 points a year (the orchestrator's finding). Evidence: 29 of 108 names had been dropped by an ex-dividend symbol suffix (HUBCXD), dividends were double counted, the spread is −1.3 points within sector, and with true publication dates over four cohorts the net spread is −1.2 points (tests/seed_audit.md, tests/value_timestamped.md). Conclusion: value is at most a tiebreaker inside a sector view. Demonstrated. Decision change: never rank stocks on P/E alone; banks on ROE against price-to-book (lesson 6) still stands.

2. **"This signal fails" usually meant "this signal equals random".** Believed: momentum and operator footprints lose money. Evidence: random liquid entry days give a 20-day median of −1.5% and a 43% win rate, the same as the signals (tests/seed_audit.md). Demonstrated. Decision change: every claim, positive or negative, is compared against random entries in the same names and period. PSX's skew makes the median trade negative even at random.

3. **Confirmed trend is the only active rule that held up.** Believed (after the tests): nothing mechanical works. Evidence: buying at a 252-session high with a trailing stop ranked first in four of five windows across two independent implementations, 2.1x to 3.3x in bull windows, 0.8x to 1.1x in hike windows (tests/oracle_and_good_case.md, tests/active_trading_codex.md). Then it lost 18% in the year to Oct 2026 (tests/rs50k_last_year.md) and its short-horizon version is indistinguishable from random (tests/pattern_mining_daily.md: R17a median six-week multiple 1.00 vs random 0.98). Suggestive, regime-dependent, chosen as the best of 15. Decision change: a breakout is a reason to look and a timing tool, not a buy signal on its own; expect it to fail in hike regimes.

4. **The fortunes are made at regime turns.** Evidence: 34 runs of 5x+, all multi-year, 23 starting within three months of a market low (tests/winners_population.md); first rate cuts were followed by +40% and +49% in 120 sessions, but the Dec 2025 cut by +1% (tests/rate_cycle_episodes.md). Descriptively strong, but only four turns and four false bottoms; the checklist that separates them is fitted to those eight dates. Suggestive. Decision change: keep powder for the turn and know the checklist; do not size on a checklist that has never been scored live.

5. **Being late is less costly than being absent, on winners.** Evidence: at the first 252-session high the median winner still had about half its gain ahead (tests/winners_population.md). But this is computed only on runs that went on to 1.5x or 2x; among all breakouts, 25.6% later touched +50% within 126 sessions, with year rates from 6% to 38%. Suggestive and biased (the Astra review, knowledge/reviews/astra_catalogue_review.md, is right). Decision change: "it has already moved 30%" is not by itself a reason to skip a stock with a confirmed, visible cause; but a breakout is a one-in-four shot at +50%, not a likely winner.

6. **Exits decide more than entries.** Evidence: a live 20% trailing stop kept more than half the gain in only 15 to 23% of winning runs; stops sized to the stock's own dips and event exits kept far more. Astra's counter: across all finished winners the 20% stop gave a median 1.01x with 49% losing; wide stops help long runs and hurt short ones, and none of the named exits was tested on losers. Hypothesis, with good reason behind it. Decision change: write the exit for the situation type (wide for index-led compounders, event exits for deals, tight for results blow-offs), freeze it, and never widen it; do not claim it is optimal.

7. **Short-horizon mechanical trading loses to costs.** Evidence: 40 pre-registered rules, six exits each, 37 lose at the next close; 18 of 240 tests reached p ≤ 0.01 against about 2.4 expected by chance, none held out of sample; "buy the day's top gainer" turned Rs50,000 into Rs15,050 in three months (tests/pattern_mining_daily.md). Demonstrated for public price-and-filing rules. Decision change: do not build daily trading for him; short-term calls are judgment on a cause, frozen and scored.

8. **News-less rises do not predict news.** Believed (his hypothesis, and mine): in a small market, a stock rising without news means someone knows. Evidence: 26.6% of such rises were followed by a filing within ten sessions against 26.7% for quiet names in the same state, and joining them lost at every exit (tests/informed_capital.md). Demonstrated for the definitions tested; the definitions could miss the specific case of leaks before results, which the results-drift test also found weak. Decision change: a rise without news is a reason to find the news, not a reason to buy.

9. **A model cannot be tested on history it remembers.** Evidence: the replay model recalled the six months after 8 of 10 probe dates in detail, 7 at the highest grade (tests/replay_pilot_postmortem.md). Demonstrated. Decision change: judgment is scored forward only; do not cite a model's "backtested" calls as evidence; and do not use your own memory of 2019 to 2026 events as if it were knowable at the time.

10. **The instructions shape the agent more than the data.** Evidence: the same bundle and model produced 20% average exposure and watch lists under brief v1, and 50 to 75% exposure with growth names under brief v2, which stated the investor's posture; Astra on the same bundle held 85% cash (data/asof/2026-10-16/REPLY_astra.json). Suggestive (15 dates, one regime). Decision change: you will be tempted to hide in cash because the documents are full of "no edge". The default is the core; cash must beat the next-best use of the money.

11. **The KSE100 is a total-return index.** I had compared price-only baskets against it as if it were a price index, which understated the baskets by about six points a year (data/macro/INDEX_NOTES.md; the implied KSE100 dividend yield 2020 to 2026 is about 6.2% a year). Demonstrated. Decision change: compare total return with total return; KSE30 and KSE100PR are the price indices.

12. **The equal-weight basket lagged the index for mechanical reasons, not because big stocks win.** Evidence: +44% vs +245% from 2017; daily rebalancing cost about 24 points, missing dividends about 10, and the rest is cap-weighting toward a few large winners; inside the investable set the least liquid third beat the most liquid third weakly (tests/size_liquidity.md). Suggestive. Decision change: turnover is expensive; concentrated holds of the right names beat broad baskets.

13. **Announced deals complete about half the time, but almost always once an offer is published.** Evidence: 75 intentions 2018 to 2026, 48% of 56 resolved completed; 25 of 28 that reached a public offer completed; buying after the intention notice had a median −1.2%, after the offer +1.1% (knowledge/playbooks/deals.md, data/deals_history.csv). Suggestive. Decision change: never trade a deal on the intention notice; at the offer, do the pro-rata arithmetic for a partial offer.

14. **On the last full year, nothing I built beat doing nothing.** Rs50,000 from 16 Oct 2025 would have been about Rs45,000 on my rules against Rs49,500 for the KMI All Share; the hindsight best five made 2.8x (tests/rs50k_last_year.md). Of 2026's six big winners, all broke out early in their move, two (PRL, MACFL) were catchable with visible causes, and the breakout rule missed them because its three slots were full on 214 of 250 sessions (tests/winners_2026_postmortem.md). Demonstrated for that year. Decision change: the failure mode is not "the screen did not see it" but "the decision process did not choose it"; a reader comparing candidates beats a slot count, if the reader is any good, which the scorecard will show.

15. **Only a few PSX businesses have an engine to double earnings.** Of 20 scored on promises versus delivery, capital allocation, minority treatment and disclosure, MEBL, LUCK, SYS, ILP and SAZEW's capacity had visible engines; FFC, EFERT, PSO and most others are sound businesses at a ceiling (knowledge/companies/quality_scores.csv). Hypothesis: these are model judgments from filings, never tested against returns.

## 4. Mistakes, and what now prevents them

Most are in lessons.md; these are the consequential ones, including some that are not.

- **Data-handling bugs that silently changed conclusions.** The XD suffix dropped 29 names (lesson 14). The announcements scraper matched ".pdf" case-sensitively, so half the insider filings had no document id and the first insider test ran on seven clusters (DECISIONS.md, 18 Oct). The bundler's budget loop shipped empty announcement sections on two exam dates. The as-of pack first leaked the next MPC date. What prevents them: spot checks on known cases (SSGC Oct 2024, PRL Jul 2026 were printed from the daily table), leak assertions (`scripts/asof.py --check`), and an Opus design review before every Sonnet test.
- **Measuring the wrong thing and reporting it confidently.** The deposit-dominated walk-forward; grading a growth core on a twelve-month target against the T-bill (which made every card look like +2 to +3% and pushed me to yield names); comparing against the total-return KSE100 as if it were price. Prevention: state the question in his words and the number that answers it before running anything; separate skill from contributions; state the horizon the metric fits.
- **False precision.** 60/40, 75/25, three names, four-week rules, 25% stops, a "1 in 3 chance of +50%" that was labelled as measured in a summary and was a judgment in the source. Prevention: every number carries its file or the word "placeholder"; risk limits are labelled policy.
- **Building rules from winners and then "validating" them on the same winners.** The catalogue's reflex "catches" PRL and MACFL in 2026, but those cases were used to write it. The stage odds in the tagged scan are computed on runs that succeeded. Prevention: the catalogue's status box; every rule labelled hypothesis until scored live; Astra's review appended.
- **Pitching a stock's story without reading its earnings mechanics.** I pitched MARI as an oil bet. Its gas is priced by a formula that caps the benefit above $110 and resets half-yearly on past oil, so FY27 EPS moves only from Rs64 to Rs67 across $75 to $125 Brent (knowledge/companies/MARI.md). Not in lessons.md. Prevention: before calling a regulated company "sensitive to X", find the pricing formula and the lag.
- **Recommending LUCK without asking about the obvious conflict.** Not in lessons.md. Prevention: before recommending any name tied to the user's family, employer or circle, ask.
- **A trigger that could not fire as written.** The ATRL condition required Monday's close to hold above Rs1,200 "after the result", but the result was published Tuesday 08:41. Prevention: check the announcement timing against the trigger window when writing a conditional order.
- **Standalone versus consolidated, nearly again.** EFERT's filing shows 6.83 standalone on one page and 7.07 consolidated on another; the frozen call was consolidated. Lesson 1 exists for a reason; read the page headers of every annexure.
- **Proactivity before alignment.** Twice the session launched large workflows on an understanding that sounded aligned and was not (knowledge/HOW_TO_THINK.md section 8). Prevention: mirror his request in his words, ask, wait for an explicit go before any large spend.
- **Background work that does not survive the session.** The Monday results poller died with the session and nothing was scored until the next session noticed. Prevention: anything scheduled must be re-armed or done by a person; the scorecard is checked at the start of every session.
- **Small technical traps that cost time.** The Windows console is cp1252 (use `-X utf8`); bash heredocs with backticks or apostrophes break; the OCR helper returns a string, and iterating it character by character silently produced nothing; Claude subagents' web search budgets run out. These are in CLAUDE.md now.

## 5. How to think when something lands

Here is the order I actually use, with the cases that taught each step.

**First: can he own it and get out?** KMI membership on the date (TPLT was deleted from the KMI All Share on 5 Jun 2026 four days after the breakout rule bought it, tests/winners_2026_postmortem.md), no Lucky group link, median traded value above about Rs5m a day, no pending deletion. If this fails, stop; nothing else matters.

**Second: what regime is it?** Policy rate against CPI, the 6-month bill against the policy rate, reserves, the rupee, Brent, the index's breadth. In a hike regime, assume most stocks will not work and only stock-specific causes will; in a turn, assume most rate-sensitive names will. MEBL is in the core partly because a hike widens its spread; that is a regime judgment, and the regime tilt as a general rule had no measured edge (tests/sector_momentum_regime.md). Know when you are using judgment.

**Third: what is the cause, who decides it, and which type is it?** Find the filing on dps.psx.com.pk or the news. A results jump (MACFL, April 2026: EPS 1.83 vs 1.03, operating profit more than doubled, 12x volume the day before) is a different animal from a policy wave (refiners 2026), a deal (EPCL), a shock rebound (May 2025), sponsor buying (ASL), or no visible cause (QUICE). For policy, ask who gains, whether the IMF wants it, and how long similar decisions took. For deals, has the offer been published, and what fraction of a holding does it buy?

**Fourth: what is priced?** Four checks. The price reaction to the news: ATRL, PRL and NRL fell 4 to 9% on the day after blowout results on 20 Oct 2026; a stock that sells off on great news is telling you the news was expected. The stage of the move from its low: PRL at 4.2x its low on 16 Oct had only 2 of 18 comparable runs go further (tests/out/engine_scan_tagged_2026-10-16.txt; conditional on winners, so read it as "late", not as a probability). The valuation against its own history and against the bill. And the brokers' previews: when Topline already expects the beat, beating Topline is the bar.

**Fifth: is the business sound and will the profit become cash?** Promises against delivery in the last few annual reports, the return on the big capital decisions, how minorities were treated, receivables and operating cash flow against profit, pending rights issues. LUCK's GEPCO bid illustrates the judgment: the same cheque that threatened HUBC's dividend thesis was only an allocation test for LUCK, because LUCK has about Rs96bn of standalone cash against a Rs12.5bn central-case cheque (knowledge/companies/LUCK_gepco.md, estimates marked as such). The breaker is the size of the cheque, not its existence.

**Sixth: what is the exit, and what does it cost if wrong?** Write the stop or the event exit before the order, size so the loss at the stop is a bounded share of the book, and assume the stop can gap (two locked sessions). If you cannot name the exit, you do not understand the trade.

**Then compare it with what he already owns.** A new idea has to beat adding to the core name furthest below target, on expected payoff, horizon and stressed loss. Most ideas do not. SAZEW at 4x earnings is a better business at the turn than now; MARI at Rs631 is a fair price for a volume story with an expected return of about +4%, so buy a starter and wait for Rs540 (knowledge/companies/MARI.md).

**When to act despite uncertainty.** When the cause is visible and dated, the price is confirming, the exit is clear, and the loss at the exit is small relative to the book. Give a probability anyway; 55% is a real number. The first deposit is a small share of what he will invest over years, so waiting for a dated event (a result tomorrow, a rate decision on Sunday) is cheap and waiting for months is expensive.

**When the evidence is insufficient.** One case; no filing; a thin name; a rule that only worked in one window; a number you cannot source; a model that "remembers" what happened. Say so plainly and say what would settle it.

## 6. The infrastructure (what the repo can and cannot answer)

All in the Claude repo session; the GPT project does not have these tools. Commands use `.venv\Scripts\python.exe -I -X utf8`.

- **PSX portal client** `scripts/psx_api.py`: prices (`eod`, `historical_full`, `intraday`), payouts, symbols, filings. The portal needs the `X-Req-Id` header from any company page; the client handles it.
- **Prices and corporate actions**: `data/prices_raw/` (313 KMI names), `data/prices_delisted/` (142 traded delisted names), `data/corporate_actions.csv` and `scripts/prices.py` (`returns(close, 'adjusted')`). Cash dividends are complete only from Nov 2024; bonus and split coverage is much better. Survivorship was measured and is about zero for the liquid basket (data/DELISTINGS_NOTES.md), not for thin names.
- **Announcements**: `data/announcements.parquet`, 225,594 timestamped filings 2005 to 2026 with classes; `scripts/fetch_announcements.py` resumes. Titles only; the numbers are in PDFs, many scanned (`scripts/insider_text.py` has a Windows OCR helper).
- **Fundamentals**: `data/fundamentals/quarterly_eps.csv` (129 names, 2019Q3 onward, consolidation unflagged); `seed/data/fundamentals/sa_ratios.csv` (fiscal-year ratios from FY2020).
- **Macro**: `data/macro/` (policy rate decisions with holds, T-bill auctions, CPI, reserves, current account, import cover, KSE100 P/E from 2022, Brent, USD/PKR, Pink Sheet commodities, NCCPL flows by type and sector via scstrade).
- **Daily decision table** `data/daily_table.parquet` (`scripts/daily_table.py` rebuilds it in about two minutes): 577,794 stock-days with features at the close and forward paths from the next open, including best and worst points, locks and later filings. Answers "what usually happened next after X" with exact timing. Its sector baskets are today's lists (hindsight) and delisted names' paths stop at their last trade.
- **Situation engine** `scripts/engine.py SYMBOL DATE` (analogue outcomes) and `--scan DATE` (the day's movers tagged by catalogue type, with stage odds and missed movers). Reliable for base odds of a signature; unreliable for rare signatures (thin analogue sets) and blind to causes not in the filings tape (SSGC's 2024 move was tagged "none" because the OGRA decision is not a company filing).
- **Backtests**: `scripts/walkforward.py` (monthly strategy engine, deposit schedule parameter), `scripts/tests/*.py` (one per test, pre-registration in each header), `scripts/codex/` (independent replication).
- **Winners library**: `data/winners_library.csv` (382 liquid runs), `knowledge/winners/` (cases), `tests/winners_population.md`.
- **Exam harness**: `scripts/asof.py DATE --check` (point-in-time pack), `scripts/replay_bundle.py DATE`, `scripts/score_replay.py --dates ...`. Only useful for dates after the model's training cutoff.
- **Scorecard**: `catalysts/frozen_predictions.csv` (append-only) and `catalysts/scorecard.md`.
- **Intraday archive** `scripts/collect_intraday.py`: started 16 Oct 2026; same-day rules cannot be tested until months have accumulated.

What these tools cannot answer: whether a specific move will continue (they give base rates, not forecasts), whether a policy will be implemented, anything needing intraday history before Oct 2026, anything about management quality beyond what filings say, and any judgment test on dates the model remembers.

Which tool for which question: a past situation's typical path, the daily table or engine; a new rule, a pre-registered test in `scripts/tests/` with an Opus design review and a placebo; a company, its filings plus a card in `knowledge/companies/`; the regime, `data/macro/` plus the checklist; a live call, the scan plus the reflex, frozen in the register.

## 7. Where the framework is strong and where it is weak

**Supported by convincing evidence:** the list of things not to do (value screens, momentum, flows, dividend games, index events, insider clusters, daily trading); costs eat short-horizon edges; staying invested beats waiting in cash over years (the KMI All Share compounded at 11.4% a year 2017 to 2026); partial offers and rights issues are traps; geopolitical shocks rebound; the KSE100 is total return.

**Reasonable judgment calls:** the growth core and its names; the 80/20 core-reserve split; the 5% loss budget; stops sized to each stock; the reserve release rule at 12 months (based on two waits of 10 and 11 months); buying a starter and waiting for a price.

**Possibly overfitted or wrong:** the turn checklist (fitted to eight dates); the catalogue's entry and exit rules (built from winners); the stage odds (conditional on success); the business-quality scores (never tested against returns); the breakout rule's bull-window results (best of 15, one or two trades per window).

**Contradictions you should hold, not resolve by pretending:**
- The only robust active rule in the research is the confirmed breakout, and PICKS v4 dropped the breakout sleeve in favour of one discretionary opportunity at a time. The reason (the rule failed last year, its fixed stop is poor, the reader should choose among breakouts) is defensible; the reader's skill is unproven.
- The regime tilt had no measured edge, and the core is chosen partly by regime (MEBL because hikes help banks).
- The card red teams put the core names' expected 12-month returns at about +2 to +6%, below the T-bill, and the plan buys them anyway, on the argument that the deposit habit and the turn asymmetry matter more than one year's expected return. That is a judgment, and a reasonable person could disagree.
- "Never ignore a move" sits beside "short-term rules lose to costs". The reconciliation is that a move should always be classified and answered, not that it should always be traded.
- The reserve holds cash while lesson 13 says cash drag is the costliest mistake; the release rule is the bridge, and it is a policy choice.
- Concentration is his preference, and a 5% loss budget with wide stops implies small positions. Watch for this when he wants to go all in.

## 8. What to investigate next, and what not to repeat

Ranked by usefulness to real decisions:

1. **The live scorecard.** Calibration is readable at about 20 weeks, the 20-session comparison with the breakout rule at about 5 months, the 60-session comparison at about a year. Nothing else answers whether the judgment layer adds value.
2. **Exits on the full breakout population.** Test the named exits (stops sized to prior dips, event exits, re-entry on a new high) on every breakout, including the 74% that failed, pre-registered, with a placebo. This is the experiment that tells you whether the catalogue's exits are real. Worth its cost.
3. **The LUCK replacement.** Score FCCL, MLCF (after the PIOC merger), DGKC, KOHC and ILP on the business record, so the cement exposure at the turn has a candidate.
4. **Business quality against returns.** Score more liquid KMI names, freeze the scores at each year end from 2021, and test top versus bottom third. Without this the quality scores are opinions.
5. **More regime turns.** Extend index and macro history before 2016 from other sources, so the checklist can be tested on more than eight dates.
6. **Policy implementation, systematically.** A full list of ECC and cabinet decisions with outcomes, not 26 hand-picked ones.
7. **Same-day questions,** only once the intraday archive has months.

Do not repeat: value screens, stock momentum, volume and lock rules, flow signals, index recomposition trades, dividend run-ups, calendar effects, insider cluster tests on the same data, the 40 daily rules, and any historical replay of a current model's judgment. These were tested adequately, with placebos, and the answers are in FACTS.md.

## 9. Where things stand on 21 Oct 2026

- **No trade has been confirmed.** Do not assume he executed anything.
- **Current recommendation (PICKS.md v4 with the 21 Oct amendment):** MEBL after its 22 Oct 11:00 result if EPS is Rs11 or more (we froze Rs12.50 to 15 at 65% and a dividend of Rs8 or more at 60%); a MARI starter of about 8 shares now, the rest at Rs540 or below; LUCK withdrawn and its slot in the reserve; about 20% of each deposit as the turn reserve, with the release rule; triggers for SAZEW (EPS Rs60+ and no hike) and SYS (Rs100 or below); skip the refiners (late in stage, sold off on blowout results on 20 Oct, cause unverified).
- **Scored so far (catalysts/scorecard.md):** 8 of 8 result and event calls held, Brier 0.092: EFERT consolidated EPS 7.07 and Rs5.50 dividend; ATRL EPS 174.89; PRL EPS 22.17, nil dividend; EPCL a loss of Rs1.45; MLCF's merger approved. The orchestrator's EFERT band (top case 4.74) was too low. The conditional ATRL entry did not trigger.
- **Pending:** EFERT's price reaction (26 Oct close against Rs194.82), PRL's (28 Oct against Rs101.44, which also settles the orchestrator's "flat to down" call), MEBL 22 Oct, the MPC 26 Oct (we froze hold 0.50, +50bp 0.38, +100bp 0.10, cut 0.02), FFC, FCCL, OGDC 27 to 29 Oct, October CPI 2 Nov, the checklist's rupee and reserves signals about 10 Nov, the regime call "no turn by 10 Nov" at 75%.
- **Still to verify:** Finqalab's commission; the refinery policy approval date (21 or 28 Jul); Sep CPI 10.3%; every GEPCO figure; why refiners fell on 20 Oct.
- **Next actions:** score as events land; decide the MEBL buy after its result; after the MPC, re-run the regime read; score the cement names for the LUCK slot when Jazib asks.

## 10. Advice to you

You will probably make these mistakes, because I made them or nearly did:

- **Treating the catalogue as a rulebook.** It is a casebook. Its rules are hypotheses; its odds are conditional on success.
- **Hiding in cash** because the documents are full of negative findings. A negative finding about a signal is not a negative finding about owning good businesses.
- **Recommending yield names as the core** because they look safe and cheap. He has said three times that dividends do not matter to him.
- **Answering a different question than the one he asked.** When he asks what Rs50k would have become, compute exactly that, on a fixed sum, against the index and the hindsight best.
- **Using your own memory of 2019 to 2026 as if it were knowable at the time.** It will make every past call look easier than it was.
- **Quoting a number from a summary instead of its source.** Several summaries in this project rounded or relabelled; the test files are the record.
- **Over-precision.** Give a probability and a range, not three decimal places.
- **Forgetting the constraints:** KMI membership on the date, no Lucky group, Finqalab stocks only, no T-bills as income.

Challenge rather than accept: my core names; the 80/20 split; the turn checklist; the exit sizes; the business-quality scores; any claim that the breakout rule or the catalogue is validated; and my framing of what he wants, if he tells you something new. He has changed this framework five times in three days by asking good questions, and each time he was right.

How to balance it: on small reversible things (a filing check, a price, a score), act; on anything large (new research, a new rule, a change to the plan), mirror his request back, ask, and wait for his go. Give him a decision and a probability rather than a survey of options. Say "no, because..." when the evidence says no; never say nothing about a move he can see. Explain every technical term the first time. Freeze every call and score it, especially the ones you get wrong, and tell him what the miss changes.

Mental models that held up: the balance of payments sets the cycle; rates set the multiple; regulated earnings follow policy, and policy is a probability; profit is not cash until collected; price reaction tells you what was expected; a confirmed cause plus a confirming price beats either alone; turnover and thin floats are the retail investor's main enemies; the size of the opportunity set depends on the regime; and a forecast you have not frozen is a story, not evidence.
