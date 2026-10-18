# PLAYBOOK.md — the operating rules on one page (19 Oct 2026)

What to do, in order, every week and whenever a stock moves. Evidence and reasoning are in knowledge/HOW_TO_THINK.md, knowledge/CATALOGUE.md and knowledge/REGIME_TURN_PLAYBOOK.md; this page is the procedure. Every number here is a policy choice unless a test file is cited.

## A. The book

- **Core, about 80% of each deposit:** three to five growing businesses chosen on the business record (knowledge/companies/quality_scores.csv), earnings growth and price paid, not yield. Currently LUCK, MEBL, MARI (PICKS.md v4). Bought every month, the name furthest below target gets the most. Held through falls while the business grows. Sold only on its written killer, a KMI All Share deletion notice, or a regime change that removes its sector (banks after the first cut).
- **Reserve, about 20% of each deposit,** accumulated as cash for the regime turn (section C). Not deployed on anything else, with one release rule so it never becomes a standing cash drag: **if the turn checklist has not scored 3 of 4 within 12 months of the reserve's first deposit (i.e. by 19 Oct 2027), half of the accumulated reserve goes into the core on the next deposit day, and the reserve share of deposits drops from 20% to 10% until the checklist scores 2 or more; the remaining half keeps waiting. At no point may cash exceed 25% of the book.** Evidence for 12 months: the gap from the last false bottom to the real low was about 10 months in 2018 to 2019 (16 Oct 2018 to 16 Aug 2019) and 11 months in 2022 to 2023 (21 Jul 2022 to 23 Jun 2023), five weeks in 2020, and none in 2024; hike regimes themselves ran 24 months (2018 to 2019) and 27 months (2021 to 2023) (knowledge/regime_turns/, scripts/walkforward.py regime episodes). The current hike regime began Mar 2026, so a turn inside 12 months is the base case but not certain; half-release caps the cost of being wrong at about 10% of a year's deposits in cash.
- **Opportunity, at most one position at a time,** entered only on a trigger from section B, with the exit and size written before the order.

## B. The reflex, when a name starts moving (six checks, in order)

1. **Can I own it and get out?** KMI All Share member (data/kmi_allshare_2026-06-05.csv); median traded value above Rs5m a day; no pending deletion.
2. **What is the regime?** 6-month T-bill vs policy rate, CPI direction, reserves, rupee (data/macro/). Hike regime: few names rise, expect idiosyncratic winners only. Cut regime: cyclicals and small caps run.
3. **What is the cause, and which catalogue type?** Results jump with cash behind it; policy or sector wave; deal after the offer is published; regime turn; shock rebound; sponsor buying. "No visible cause" is an exclusion (knowledge/CATALOGUE.md, type 9). Run `scripts/engine.py --scan <date>` for the tag and the stage odds.
4. **Where is the price in the move?** Below about 2x its 52-week low with a confirmed breakout: joinable. Above 4x: late; of 18 comparable runs only 2 went further (tests/out/engine_scan_tagged_2026-10-16.txt).
5. **Can the profit become cash?** Receivables trend, operating cash flow vs profit, debt maturities, pending rights issues. Regulatory entitlement is not collection.
6. **Write the exit and the size before buying.** Stop sized to the name's own worst pullback (25% for names that dip 15 to 23%, 30 to 40% for names that dip a third), or the type's event exit (offer document, deletion notice, exchange letter after a doubling, third limit-down after a blow-off). Loss at the stop at most 5% of the book; at most 15% of the book at risk across correlated positions; stops never widened; re-entry is a new decision. Size from stressed exit capacity (two locked sessions, a third of normal volume).

## C. The regime turn (where every 5x run began)

Checklist from knowledge/REGIME_TURN_PLAYBOOK.md, scored live: A oil calm (Brent not up 10%+ in 13 weeks); B drain (under 10% of liquid names at a 20-session low two sessions after the low); C rupee flat in the following four weeks; D reserves up in the following four weeks. Three of four present at every real low (2019, 2020, 2023, 2024) and at no false bottom. Confirmation within ten sessions: more than half of names above their 200-day average and about 13 liquid names at one-year highs. On a score of 3: a third of the reserve into the leaders (cement, autos, the largest names), a third at four weeks, a third at eight; 25% trailing stop on index-led names, 30 to 40% on stock-specific ones, re-entry on the first close above the old high.

## D. The exits that kept the money (tests/winners_population.md, knowledge/CATALOGUE.md)

A fixed 20% trailing stop kept more than half the gain in only 15 to 23% of winning runs. Stops matched to the name's own dips, and event exits, kept far more. Take a third off at +50% and +100% only on names whose type has a history of round-tripping (results jumps, thin names); let index-led and compounder runs ride on their wide stop.

## E. The weekly loop (RUNBOOK.md; .claude/skills/psx-weekly/SKILL.md)

Refresh data; score every frozen row whose event has passed (catalysts/frozen_predictions.csv, scorecard.md); rebuild the daily table and run the tagged scan; apply the reflex to each tagged name; freeze the week's call with probabilities; log Jazib's sizes; list every 20%+ mover the scan missed and diagnose. After 20 weeks, read the scorecard: calibration first, then the 20-session comparison against the plain breakout rule and the KMI All Share; the 60-session comparison needs about a year.

## F. What not to do (tests/FACTS.md)

No value screens, no stock momentum, no volume-spike or lock chasing, no flow signals, no dividend games, no index-inclusion trades, no daily trading (costs 0.5 to 1% a round trip eat every edge of that size), no buying a results filing before the price reacts, no thin names, no fixed 20% stops, no cash above the reserve without a reason that beats the core.
