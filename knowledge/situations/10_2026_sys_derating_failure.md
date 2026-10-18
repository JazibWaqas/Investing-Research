# Situation 10: a popular story that did not pay, SYS (and NETSOL) 2025 to 2026

Written 2026-10-18. Type: failure case, a derating while earnings rose. Sources: `data/panel_close_adj_pricereturn.parquet` (SYS had a 5-for-1 split on 2 Jun 2025, `data/corporate_actions.csv`), `data/fundamentals/quarterly_eps.csv` (stockanalysis figures; SYS shares restated for the split), `data/macro/`, `knowledge/sectors/tech.md`, `knowledge/companies/NETSOL.md`. I did not find a pumped small cap in `tests/out/` (no volume_ignition file exists), so this is the chosen failure. The causes of the 2026 sell-off are my reading from the repo, not sourced.

## Dates and regime

- 7 Jan 2026: SYS 171.3 (adjusted), the high; KSE 186,519. Policy rate 10.5% (cut 50bp on 15 Dec 2025). 3-month bill 10.0% (21 Jan 9.9%). CPI 5.6% (Dec). USD/PKR 280.3.
- Then: the war (Hormuz closed 28 Feb), a 100bp hike to 11.5% on 27 Apr, CPI 10.9% (Apr) to 11.6% (May), the 6-month bill 12.5% (20 May), and a rupee that strengthened 257 days in a row to 277.0 (8 Oct).

## What was knowable, and when

1. 30 Jun to 31 Dec 2025: SYS rose 59.6% (107.1 to 170.9), KSE +38.5% (125,627 to 174,054). The story: Pakistan's IT exports up 20% (tech.md, FY26 $4.6bn), SYS as the sector's quality name.
2. 27 Oct 2025: Q3 result, EPS 1.90. Trailing four quarters through Q3 2025: 1.40 + 1.71 + 1.81 + 1.90 = 6.82. At 171.3 on 7 Jan that is 25.1x trailing earnings, against a bill yielding 10%. Earnings yield 4.0% against 10% cash.
3. Structural facts already public: 94% of SYS revenue in foreign currency, but about 56% of its costs in rupees, so a stronger rupee compresses the margin (tech.md); 57% of revenue from the Middle East and Africa.
4. 27 Apr: the hike. 29 May and 27 Aug: results with revenue +35% for 1H26 and profit +17%, and management warning that more rupee strength hurts (tech.md, Business Recorder 4 Sep, asserted).

## What the market did

| Date | SYS (adj) | KSE | Note |
|---|---|---|---|
| 30 Jun 2025 | 107.1 | 125,627 | after the split |
| 7 Jan 2026 | 171.3 | 186,519 | high |
| 19 Feb | 136.4 | | first close 20% below the high |
| 9 Mar | 106.7 | 146,480 | the war low, -37.7% |
| 27 Aug | 123.1 | 177,323 | 1H26 results |
| 16 Oct | 118.4 | 166,420 | |

From 7 Jan to 16 Oct, SYS fell 30.9% and KSE 10.8%. Over that time trailing earnings (Q3 2025 to Q2 2026: 1.90 + 2.10 + 2.05 + 1.98 = 8.03) rose 17.8%, so the trailing P/E fell from 25.1x to 14.7x. All of the price fall was the multiple.

NETSOL showed the second face of the same trap: reported FY26 EPS Rs27.25 (+71%) and a trailing P/E of 4.5x, yet the stock fell from 134.1 on 7 Jan to 89.4 on 9 Mar and sat at 122.7 on 16 Oct (-8.5%). Its P/E was low because the earnings were lumpy (a one-off Mercedes licence, about Rs7.7 a share per the repo's estimate) and receivables were 200 days.

## The right move

For a holder: no add at 25x with a risk-free rate of 10% and a hike cycle possible; take a third off at a large gain (the method in HOW_TO_THINK section 5), and exit on a 20% trailing stop. That stop (a placeholder) triggered on 19 Feb at 136.4: +27.3% from a 30 Jun 2025 entry, -20.4% from 7 Jan. For a buyer on 7 Jan: nothing, or a small starter and a stop. A buyer who entered on 27 Oct at 154.1 and used the same stop lost 11.5% instead of 23.2% by 16 Oct.

## The trap

The story was true and the stock still fell. IT exports grew and SYS earnings grew. Four things were wrong: price already contained two years of growth, valuation was set against a 10% bill, cost structure faced a rupee that was about to strengthen, and a Gulf exposure met a war. "Good company" did not protect against a 41% multiple contraction.

## Situation type and lesson

Popular story with valuation risk, in a regime that moved against long-duration assets (rates up 100bp, CPI doubling). Lesson: when a rally is a re-rating, not an earnings change, the exit is the multiple, not the news. Check price to earnings against the bill yield and the earnings yield spread before buying a "quality" story, and write the exit before the entry. Tech's own record (tech.md) shows the same pattern in 2021 to 2022: NETSOL -68% from its March 2021 high.

## Questions that would have caught it

- Q1 Regime: rates at the bottom of a cycle (10.5%), CPI doubling as a risk, the rupee about to move.
- Q3 Actors: whose costs are in rupees and whose revenue in dollars? What does a stronger rupee do to margin?
- Q4 Price: +60% in six months, 25x earnings: extension, not confirmation.
- Q5 Exit: a stop at the entry, and a limit on the loss if the multiple goes to 15x (-41%).
- Q6 Traps: a low P/E that is a lumpy one-off (NETSOL); a high one that is a rerating (SYS).
