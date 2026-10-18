---
type: "catalyst trade (ignored earnings, then spread and policy)"
knowable_date: 2026-04-29
outcome_end: 2026-10-16
summary: "Catalyst trade: refiners' windfall earnings were ignored for ten weeks, then a spread turn, volume and policy lifted them. PRL +155%, NRL +70% to 16 October 2026. Lesson: spread, volume and policy, in that order."
---

# Situation 07: the 2026 refiners (PRL, NRL, ATRL, CNERGY)

Written 2026-10-18. Type: catalyst trade (ignored earnings, then spread and policy). This is a condensed reuse of `tests/refiner_steel_retrospective.md` and `knowledge/playbooks/catalyst_trade.md`; read those for the full price tables and PSX document ids. Prices re-checked from `data/panel_close_adj_pricereturn.parquet` and `data/macro/`. News is as cited in the retrospective (ProPakistani 8 Jul and 2 Sep 2026, Dawn 25 Sep 2026); I did not re-open it.

## Dates and regime

- KSE 189,167 on 23 Jan 2026 (high), 146,480 on 9 Mar (low, -22.6%), 181,260 on 9 Jul (observed).
- The Strait of Hormuz closed on 28 Feb (retrospective). Brent $71.3 (27 Feb), $95.7 (6 Mar), $127.6 (weekly, 3 Apr), $68.5 (2 Jul).
- Policy rate 10.5% until a 100bp hike on 27 Apr to 11.5%, held through 14 Sep. CPI 5.8% (Jan), 7.3% (Mar), 11.1% (Jun). 3-month bill 11.8% (9 Apr). USD/PKR 279 to 278. IMF programme running.

## What was knowable, and when

1. 21 to 29 Apr: the four March-quarter results. PRL EPS Rs15.78 (year earlier -4.09) at a price of Rs38.8, about 1.9x trailing; NRL about Rs91 a share at Rs382; ATRL Rs106.41 at Rs940; CNERGY Rs3.22 at about Rs8 (PSX docs 274659, 275684, 275863, 275538). A flag from 29 Apr.
2. May to 2 Jul: Brent fell by 42% from about $118 to $68.5, and the stocks lost 16 to 22 points against the market over ten weeks. The market's reading, that the profit was an inventory gain, was partly correct.
3. 7 to 9 Jul: PRL volume 15.6m on 7 Jul against 1.7m the day before and 48m on 8 Jul; on 8 Jul the war resumed, Brent +6%, KSE -2.5%, PRL +3.2%. A trade signal.
4. 28 Jul: the Cabinet Committee on Energy approved the refining policy after seven years of deadlock (Dawn 25 Sep).
5. 2 Sep: July refining margin $36.7 against $5.4 a year earlier. From 20 Aug a diesel crack cap of $41.89 limited the upside.

## What the market did

| | 9 Jul close | 16 Oct close | Return | Peak (date) |
|---|---|---|---|---|
| PRL | 41.85 | 106.95 | +155% | 105.39 (2 Sep), new high 16 Oct |
| NRL | 391.52 | 665.73 | +70% | at the high |
| ATRL | 911.75 | 1,219.1 | +34% | at the high |
| CNERGY | 9.40 | 12.85 | +37% | 15.46 (31 Aug), +64% at peak |

A 20% trailing stop (a placeholder) exits PRL on 10 Sep at Rs80.93, +93%, against +155% held. KSE moved from 181,260 to 166,420 (-8.2%) over the same period.

## The right move

Watchlist entry: 29 Apr. It lost 16 to 22 relative points over ten weeks while the spring sat loaded, which is the cost of the first leg alone. Trade entry: the 8 to 9 Jul reaction (volume above 5x, refiners up on a down market day, Brent turning), with PRL at Rs41.85 on 9 Jul. Entry after the 28 Jul policy approval, at about Rs59, still returned +81% to 16 Oct. Size on the trade was luck: a war restarted. The signal was a spread, volume, and policy, in that order.

## The trap

Two. The value trap on the first leg: a P/E of 2x on windfall earnings was ignored for ten weeks because the market was right that it was windfall. And the extension trap: a buyer after 2 Sep (Rs105) faced a crack cap, a possible windfall tax, and a likely rights issue (PICKS.md). PRL's normalised EPS was about Rs10 on the repo's own estimate, which makes Rs107 about 10x, not 2x.

## Situation type and lesson

Catalyst trade: a visible earnings inflection the price ignores, plus a turn in the commodity spread, plus a policy overhang lifting, confirmed by volume. Odds: volume ignition alone (n = 788, 2017 to 2026, 60-day) has median -3.4%, win rate 45%, against a placebo median of -6.9% and win rate 36%. That is a weak edge. The fundamental filter leaves too few cases to measure; my judgement, not a figure, was about 1 in 3 for a move above +50% in six months once all three legs lined up.

## Questions that would have caught it

- Q1 Regime: oil shock, rupee stable, IMF intact, a hike on 27 Apr. Rates hurt multiples but not refiners with 2x P/E.
- Q2 Situation type and base rate: catalyst trade, n = 1 episode here, volume rule n = 788.
- Q3 Actors: refiners gain on spread and policy; a government considering a windfall tax is the loser's counterparty.
- Q4 Price: confirmation was 8 to 9 Jul; extension was after 2 Sep.
- Q5 Exit: trailing stop; veto signals are a crack cap, a windfall tax, a rights issue.
- Q6 Traps: one-off earnings, stale valuation, rights issue risk.
