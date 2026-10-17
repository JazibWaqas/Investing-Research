# PICKS.md — positions, limits and triggers (frozen 18 Oct 2026, 02:30 PKT, prices are 16 Oct closes)

Rests on: Phase 1 sector map, Phase 2 tests, Phase 3 walk-forward, twelve underwriting cards with red team (knowledge/companies/), the deals playbook. Not yet in: the full insider-trade extraction, the deal-failure base rate, delisted names. Those will change the satellite section, not the core.

Capital: Rs50,000 now, Rs50,000 in about 15 days, then Rs50,000 a month. Finqalab, stocks only, KMI All Share only. All twelve names below are in the 5 June 2026 KMI All Share list. All trade more than Rs8m a day, so Rs10k orders fill at the quote.

## How the book is built

Sixty percent core, forty percent satellite. The core is bought now and every month. The satellite is bought only on the triggers below; if nothing triggers within four weeks of a deposit, that deposit goes into the core. Never more than 30% of the account in cash for more than four weeks. Never more than 25% in one name at full size. No stop-losses: on this market a 25% trailing stop cut the best backtested strategy's final value by a sixth because it sold the winners. A position is sold on its written breaker, on a KMI deletion notice, or when a regime change removes its sector.

Confidence scale, from the walk-forward trade log (tests/system_walkforward.md, post-mortem): a value pick inside a sector favoured by the rate regime has won 61 to 66% of the time over 12 months with a median gain of 4 to 9%; a dated catalyst trade has no measured base rate yet, so each one below carries the card's probabilities and the red team's correction, and each is frozen in catalysts/frozen_predictions.csv when it is bought.

Where the odds come from: bear, base and bull values are the underwriting cards' probability-weighted scenarios, cut by the red team. Dividends are the next four expected payments from last year's pattern (catalysts/dividend_calendar.csv), net of 15% withholding tax.

## The core: buy now, Rs30,000, three names

The rate regime is TIGHT (6-month T-bill 12.40% above the 11.5% policy rate, CPI 10.3% and flat, MPC 26 Oct). In that regime the walk-forward's best strategy holds Islamic banks, E&P and fertilizer and buys the cheapest sound name in each. Its mechanical picks today are FABL, ENGROH and OGDC. I override two of them for quality: MEBL over FABL (ROE 34% vs 17%, lesson 6) and FFC over ENGROH (FFC owns the fertilizer cash flow directly; ENGROH is a holdco with a 9% discount on market multiples and a buyback ending 25 Oct). That is a judgment call, logged here so it can be scored against the mechanical choice.

**MEBL, Meezan Bank, Rs545.82. Buy 18 shares, Rs9,825.**
The story: the largest Islamic bank, 34% return on equity, no interest-rate floor on deposits, so every rate hike widens its spread. Q3 result 22 Oct 11:00. Why it is not cheap: 3.3x book. Why own it anyway: it is the only bank that compounds book at 30%+, and in a hike regime Islamic banks led in all three past hike windows. Catalysts: 22 Oct result (we predict EPS Rs12.50 to 15.00, 65% odds, against the orchestrator's 7.02 to 12.74 band, which we think is too low), Rs8 interim (60%), MPC 26 Oct (a hike is good for MEBL). Dividends next 12 months: Nov Rs7, Mar Rs7, May Rs7.5, Aug Rs8, gross Rs29.5, net Rs25.1 per share, Rs452 on 18 shares. Outcomes on 18 shares at 12 months: bear Rs425 (25%) −Rs2,175; base Rs560 (55%) +Rs255; bull Rs680 (20%) +Rs2,415; plus Rs452 of dividends. Card expected return +5.9%, red team +3%. Killer: Q3 EPS below Rs11, or spread compression once cuts start (then rotate out). Add below Rs485.

**OGDC, Oil and Gas Development, Rs299.10. Buy 33 shares, Rs9,870.**
The story: the country's largest E&P at about 6x earnings with Brent near $105 and wellhead gas prices up 8 to 10% for the half. Q1 FY27 result expected about 29 Oct (not yet noticed); Topline expects EPS Rs12.9, +45% year on year; we predict Rs11 to 14.5 (62%) and a Rs4 to 6 interim (65%). Why it is cheap: Rs508bn of overdue circular debt, a one-off tax reversal in FY26 that flattered last year's EPS, and a government that can change the royalty and tax rules. Catalysts: Q1 result, the Rs1.49tr gas circular-debt plan (pending, not approved), IMF board approval of the 4th EFF review. Dividends: Nov Rs3.5, Mar Rs4.25, May Rs3.25, Oct Rs6, gross Rs17, net Rs14.45, Rs477 on 33 shares. Outcomes: bear Rs215 (25%) −Rs2,775; base Rs305 (50%) +Rs195; bull Rs390 (25%) +Rs3,000; plus Rs477. Card +7.2%, red team +2 to 3%. Killer: collections fall or gas curtailments resume; Brent below $75. Add below Rs265.

**FFC, Fauji Fertilizer, Rs537.87. Buy 18 shares, Rs9,682.**
The story: the urea duopoly's cash machine after absorbing FFBL, consolidated EPS about Rs61 trailing, Rs41 of dividends in the last four quarters, 7.6% yield. Q3 result about 27 Oct (no board notice yet; Topline EPS Rs16.1 consolidated; we predict Rs14 to 18 at 65% and a Rs9.5 to 14.5 interim). Why it is not more expensive: Rs30.6bn committed to the PIA consortium, gas repricing risk every budget, and a fertilizer sector that is 4 points behind the KMI over six months. Dividends: Nov Rs9.5, Mar Rs8.5, May Rs8.5, Aug Rs14.5, gross Rs41, net Rs34.85, Rs627 on 18 shares. Outcomes: bear Rs405 (25%) −Rs2,392; base Rs535 (50%) −Rs52; bull Rs646 (25%) +Rs1,946; plus Rs627. Card +5.1%, red team +3%. Killer: gas cost not passed into urea, DPS below Rs32, more PIA funding. Add below Rs510.

Core expectation: these three are index-like holdings in the sectors the regime favours. Expect roughly the KMI All Share's 11 to 14% a year with 6 to 7 points of it as cash dividends, not a 30% year. The red teams' point estimates (+2 to +3% price plus 5 to 7% yield) are below that; the gap is the market near its high. The core exists because waiting in cash has cost more than imperfect entries every time it was measured (lesson 13).

## The satellite: Rs20,000 now, deployed only on triggers

Four situations, each with a trigger, a limit and a size. Buy the first two that trigger. Freeze a row in catalysts/frozen_predictions.csv before each buy.

**1. GHGL, Ghani Glass, Rs39.22. Trigger: Q1 FY27 result about 28 Oct shows EPS at or above Rs1.60, and price at or below Rs40. Buy 250 shares, about Rs9,900.**
Net cash (about Rs3.9bn after declared dividends), 5.4x earnings, 10% trailing yield, the only glass name with no debt in a sector where peers fell 30% in a year. Red team: the base case is a re-rating to 6x without a driver, the final dividend was cut from Rs1.50 to Rs1.00, and the stock fell 15% in two days after last October's result. So: wait for the print. Dividends: Rs1 ex 21 Oct (declared; buying after the print misses it), Nov Rs0.5, Mar Rs1, Jul Rs1, net about Rs2.1 after the first. Outcomes on 250 shares: bear Rs29 (25%) −Rs2,550; base Rs44 (50%) +Rs1,200; bull Rs52 (25%) +Rs3,200. Card +15%, red team +8 to 10%. Killer: EPS below Rs1.3, or trade debts rising again.

**2. NETSOL, Rs122.66. Trigger: Q1 FY27 result (board 30 Oct per the sector note; confirm the notice) shows underlying quarterly EPS at or above Rs6 excluding one-offs, and price at or below Rs125. Buy 80 shares, about Rs10,000.**
USD revenue, 4.6x earnings, net cash about a third of market cap (half of it customer advances), and an easy year-earlier base. Red team: the whole case hangs on how much of FY26's EPS was the one-off licence fee (Rs3.5 to 15 per share by the card's own range), treasury shares were sold at a 40% discount in January, the Q2 result was revoked and reissued, and the CFO changed on results day. The US parent "evaluating structural options" is unverified secondary reporting. Outcomes on 80 shares: bear Rs88 (25%) −Rs2,770; base Rs132 (55%) +Rs750; bull Rs160 (20%) +Rs2,990. Dividends about Rs1.3 net. Card +4.3%, red team +2%. Killer: normalised EPS below Rs15 a year; parent moves work out of Pakistan.

**3. PSO, Rs368.04. Trigger: limit order at Rs345, or the OMC margin notification (Rs1.22 a litre, ECC-approved, not notified) is published. Buy 29 shares, about Rs10,000.**
0.59x book, 6.8x consolidated earnings, Rs415bn of receivables that the gas circular-debt plan would start to clear, and daily fuel pricing since July that caps inventory losses. Its PRL stake is a quarter of its market value. Red team: a PRL rights issue could take Rs10bn from PSO; the Rs72bn windfall-levy proposal is unresolved; CEO churn. Dividends about Rs10 gross, Rs8.5 net, ex about 20 Oct (inferred). Outcomes on 29 shares at Rs345: bear Rs270 (25%) −Rs2,175; base Rs380 (55%) +Rs1,015; bull Rs500 (20%) +Rs4,495. Card +4.6%, red team +3.8%. Killer: windfall levy enacted; a 100bp hike (costs about Rs3.8bn pre-tax); Brent collapse with inventory losses.

**4. EPCL, Engro Polymer, Rs31.85. Trigger: only after the public offer announcement (due by 7 Dec) is published, and only if the net blended value exceeds the price by 10% or more. Buy 300 shares, about Rs9,000 at Rs30.**
Noventra is buying 56.19% at Rs38.60. The public offer covers only 17.5% of shares against a 32.8% free float, so about 53% of a holding is bought at Rs38.60 if everyone tenders; blended exit Rs32.9 to 33.8. At Rs29 the expected net return is about +12% in four months at 70% completion odds; at Rs31.85 it is about zero. Base rate from the complete set of 75 takeover intentions 2018 to 2026 (data/deals_history.csv): only 48% completed; all 28 withdrawals came before a public offer, and 25 of 28 that reached the offer stage completed. Buying the day after an intention notice had a median return of −1.2% and lost 14% to the index; buying the day after the offer announcement in completed deals returned a median +1.1%. So the trade is after the offer, not before. Median premium +21%, median 207 days to completion, median price 13% below the offer a month after completion. Killer: Liberty Daharki (11%) acts in concert and does not tender, cutting acceptance; the offer lapses; EPCL's own earnings (net debt Rs40bn, PVC margins) keep falling.

**Not taken, and why.** ATRL: refiners re-rated 2x since June, Q1 result 19 Oct 16:00 is expected to be huge and is priced, the diesel crack cap review about 20 Oct can cut 10 to 20%; red team expected return +0.5%. SAZEW: 4x earnings but margins compressing, volumes fall on every hike, red team −9%; revisit if Q1 EPS is at or above Rs60 and the MPC does not hike. PRL: avoid, normalised EPS about Rs10, a large rights issue likely; our frozen call is EPS at or above Rs13 on 20 Oct and flat-to-down after. SNGP and SSGC: the OGRA ruling (6 to 27 Nov) is a coin flip with a 10 to 40% swing; no edge in guessing. HUBC: 10% yield, 5x earnings, fine as ballast; the GEPCO consortium and the CPHGC true-up are unresolved, and power lagged in both easing cycles. LUCK: holdco discount about zero. Chemicals, textiles, pharma, steel: negative catalysts, bottom of the sector ranking.

## Orders for Monday 19 Oct and the next deposit

Now (Rs50,000): MEBL 18 at limit Rs552, OGDC 33 at limit Rs305, FFC 18 at limit Rs545. About Rs29,400. Keep about Rs20,600 for triggers 1 to 4; whatever has not triggered by 16 Nov goes into the core name furthest below one third.

Second Rs50,000 (about 1 Nov): if MEBL's 22 Oct result and the 26 Oct MPC are as predicted, add Rs10k to each core name and hold Rs20k for triggers. If the MPC cuts (2% odds), the regime rule flips: stop adding banks and power, start the EASING list (autos, cement, steel, glass, textiles, OMC, tech by 6-month momentum, cheapest sound name in each).

Monthly after that: Rs30k core (the name furthest below target), Rs20k satellite or core by the four-week rule.

## Watchlist with entry triggers

| Name | Sector | Trigger | Limit | Size | Note |
|---|---|---|---|---|---|
| PPL | E&P | OGDC-type result on Q1; price at or below Rs200 | Rs200 | Rs10k | 6x earnings, 5% yield, same circular-debt story; red team +3.6% |
| FABL | Islamic bank | the mechanical S3 pick; buy if MEBL's P/B exceeds 3.6x or FABL's 1H EPS growth turns positive | Rs88 | Rs10k | ROE 17%, P/B 1.2x; orchestrator passed on it |
| ENGROH | holdco | buyback completes 25 Oct and discount to market SOTP exceeds 15% | Rs245 | Rs10k | EFERT plus EPCL stakes are 53% of price |
| ISL | steel | HRC prices up 10% from the Oct low and Q1 EPS up year on year | Rs75 | Rs8k | sector lagged 45 pts since May 2024; quality screen top 10 |
| SAZEW | autos | Q1 FY27 EPS at or above Rs60 and no hike on 26 Oct | Rs1,450 | Rs10k | cheapest high-ROE name; margin squeeze is the risk |
| HUBC | power | GEPCO bid disclosed and HUBC's equity share below Rs20bn | Rs170 | Rs10k | 10% yield ballast |
| Any KMI name | any | a sponsor or substantial shareholder buys in the open market on two or more days within 30 days (PSX insider filings) | market | Rs8k | the ASL 2026 pattern; base rate being measured now |
| Any KMI name | any | quarterly EPS more than 10% of price and the stock within ±3% of the market 20 days after the result | market | Rs8k | the PRL 2026 pattern; weak base rate, needs a card |

## Live calls already frozen (catalysts/frozen_predictions.csv)

EFERT 19 Oct: EPS Rs4.80 to 7.50 (62%), above the orchestrator's 4.74 (80%), DPS Rs3.5+ (75%). ATRL 19 Oct: EPS Rs100+ (68%). PRL 20 Oct: EPS Rs13+ (58%), no dividend (93%), higher after 5 sessions only 42%. MEBL 22 Oct: EPS Rs12.5 to 15 (65%), DPS Rs8+ (60%). MPC 26 Oct: hold at 11.5% (50%). FCCL 27 Oct: EPS Rs1.45 to 2.00 (55%). FFC about 27 Oct: EPS Rs14 to 18 (65%). OGDC about 29 Oct: EPS Rs11 to 14.5 (62%), above the orchestrator's 9.94 (82%). Score each as it lands; the scorecard tells us within a month whether these probabilities mean anything.
