# PLAYBOOK.md — how to decide (rewritten 21 Oct 2026)

There is no fixed strategy. No allocation split, no standing reserve, no loss cap, no "one position at a time". The situation decides, the way an owner decides about his own money. Sometimes the right answer is everything in one name, sometimes everything out, sometimes spread across many. This page is the way of thinking that makes that call well. It is not a rulebook. Every number on it is evidence from the past to weigh, never a limit. The version with fixed rules (19 Oct) is in git history and was dropped because Jazib said fixed rules are the one thing he did not want (DECISIONS.md, 21 Oct).

## What does not change

- **KMI All Share names only.** His religious line. Check membership on the date (data/kmi_allshare_2026-06-05.csv; recompositions in June and December).
- **Lucky group names are allowed when they are worth it.** Holding LUCK, LCI or another Lucky company means a declaration through his father's employer. That is a real cost, so a Lucky name has to beat the best non-Lucky alternative clearly. His inside view of LUCK is information with a bias; name the bias when you use it.
- **Every call carries odds,** frozen before the event in catalysts/frozen_predictions.csv and scored after. This is how the judgment earns trust. It is not a limit on what he buys.
- **No invented numbers, no lookahead.** "Unverified" is an answer.

## His stance on risk (stated 21 Oct 2026)

Advice weighs upside against downside. He accepts a loss of up to about 30% on a call when the upside is large, and the upside he is after is open-ended. He wants to maximise upside even if that means taking the occasional real risk. He will put in more than the monthly deposit when the odds are good, and he takes some profit on big winners. Dividends do not matter at his size. Cash earns nothing in his account (stocks only on Finqalab), so cash is a position with a cost, held only when it beats every alternative.

## The questions, for every decision

Buy, add, hold, trim, sell everything, go to cash, go all in: the same questions.

1. **What is the situation?** What is moving and why: the dated cause (a result, a policy, a deal, a sponsor buying, a shock, a regime change), or none. Which type in knowledge/CATALOGUE.md it resembles. What regime we are in (policy rate against CPI, the 6-month bill against policy, reserves, rupee, oil; knowledge/REGIME_TURN_PLAYBOOK.md).
2. **What did situations like this do before?** `scripts/engine.py SYMBOL DATE` for analogues, tests/BASE_RATES.csv, knowledge/winners/ and knowledge/situations/. Say how many independent episodes stand behind the odds, and whether they are measured, casebook (winners only) or judgment.
3. **What is the upside and the downside, in rupees, on the size you are proposing?** A bad, normal and good case with a probability each. The question is the asymmetry: how much he can make against how much he can lose. A downside of up to about 30% is acceptable to him when the upside is several times larger.
4. **How sure are you?** A probability, and why. What the price already assumes (if everyone expects it, it is in the price).
5. **What would prove you wrong?** The observation, ideally dated: a result, a notification, a close below a level that breaks the story. Decide the exit now, for this case. A compounder exits on a broken business, a trade on a broken story or price, a deal on its terms, a shock rebound on time and distance.
6. **Can he get in and out?** Traded value against the size; upper and lower locks; gaps through a stop. Thin names need a smaller size or a longer exit.
7. **Compared with what?** Every rupee has an alternative: the best other call on the list, the existing holdings, the index, cash at zero. A new idea has to beat the weakest thing it would replace.
8. **So how much?** Anywhere from nothing to everything. Size grows with the odds, the asymmetry and the quality of the evidence, and shrinks with correlation to what he already holds (same sector, same macro driver, same sponsor). Say the size, the rupees at risk if the downside happens, and that loss as a share of his whole book.

Write the answers down. The call, its probability and its exit go in the register before money moves.

## Reference points from the evidence (weigh them, do not obey them)

- **Where the big money came from.** Every run of 5x or more since 2016 began at or near a regime turn, when a hike cycle ended and cuts began, usually within three months of a market low (tests/winners_population.md). The turn checklist that separated four real lows from four false bottoms is in knowledge/REGIME_TURN_PLAYBOOK.md; it is fitted to eight dates.
- **Being invested.** The KMI All Share compounded at about 11.4% a year 2017 to 2026 with falls of 40 to 60% along the way (data/macro/INDEX_NOTES.md). In the two hike-cycle bears only about 4% of liquid stocks rose, and in 2021 to 2023 the median stock fell 52% (knowledge/situations/03).
- **How far along a move is.** Below about 2x its 52-week low with a confirmed breakout, most of the run was still ahead for the winners; above 4x, 2 of 18 comparable runs went further (tests/out/engine_scan_tagged_2026-10-16.txt). Odds measured on winners only.
- **Exits.** A fixed 20% trailing stop kept more than half the gain in only 15 to 23% of winning runs; wider stops matched to the stock's own dips kept far more, but that was measured on winners only (tests/winners_population.md). Price limits mean a stop can gap through locked sessions.
- **Concentration and turnover.** Two names made 88% of the walk-forward's profit (tests/system_walkforward.md); turnover cost the equal-weight basket about 24 points (tests/size_liquidity.md).
- **What has not worked** after costs, against random entries: value screens, stock momentum, volume spikes and lock chasing, flow signals, dividend run-ups, index-inclusion trades, insider clusters, calendar effects, and every 1-to-10-day trading rule (tests/FACTS.md). A rise on heavy volume with no visible cause had a negative base rate. Buying a result before the price reacts did not pay.
- **Shock rebounds.** Geopolitical falls of 5% or more rebounded a median +27.8% at 60 sessions, 9 of 9 regained (tests/noise_map_shock_rebound.md).
- **Costs.** About 0.5% a round trip in liquid names, 1% under Rs20m a day (data/costs.md).

## What tends to go wrong (knowledge/lessons.md)

Hiding in cash because the documents are full of "no edge"; answering a different question than the one he asked; hardening a preference into a rule; quoting a summary instead of the test file; trusting a story without cash behind the profit; using memory of 2019 to 2026 as if it were knowable then; staying silent about a move he can see.

## The weekly loop

RUNBOOK.md and `.claude/skills/psx-weekly/SKILL.md`: refresh data, score every frozen row whose event has passed, rebuild the daily table, run the tagged scan, put the questions above to every name that is moving and every holding, freeze the calls, update STATE.md, list every 20%+ mover the scan missed and say why.
