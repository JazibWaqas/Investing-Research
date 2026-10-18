# Short-term trading on PSX: what ten years of daily data say (1 to 10 days)

Written 18 Oct 2026 for the investor. Evidence: `tests/pattern_mining_daily.md` (40 pre-registered rules, 6 exits, 240 tests), `tests/informed_capital.md` (news-less rises), `knowledge/playbooks/situation_engine.md` and `scripts/engine.py` (analogue lookups), `tests/out/engine_scan_2026-10-16.txt`, all built on `data/daily_table.parquet` (577,794 stock-days, 455 names including 142 delisted, 2 Jan 2017 to 16 Oct 2026). Costs are from `data/costs.md`: about 0.5% round trip in a liquid name, plus 0.5% slippage for names under Rs20m median daily traded value. The Finqalab brokerage rate is unverified. The 15% capital gains tax is not deducted anywhere below. In-sample means signals up to 31 Aug 2026; out-of-sample means 1 Sep to 16 Oct 2026, which was a falling market.

## The short answer

Over one to ten days, buying what has just moved (a top gainer, a 7% day, a lock, a news-less rise, three up days) lost money after costs in every version we tested. It did worse than buying a random stock of the same liquidity on the same day. The gross edge is roughly zero and the costs are 0.5% to 1% a trade, so frequent trading turns Rs50,000 into less. The only in-sample positives were buying the worst fallers on a market panic day (39 dates, never tested out of sample) and holding breakouts with a 20% trailing stop (positive average, negative typical trade, and it lost 13% to 15% a trade in Sep to Oct 2026). Neither is an edge yet. Your SSGC trade in 2024 was real, but in the data it looks like a rare right-tail outcome, not a repeatable pattern.

## 1. Rs50,000 traded actively: the one-month distribution, and recent months

Setup: Rs50,000, fully reinvested, up to three positions at a time, each rule's signals taken in order of that day's volume surge. Every rolling 30-session window from January 2017 (2,397 windows; 30 sessions is about six weeks) was simulated with costs inside each trade. "Random" is the same book filled with random names above Rs5m traded value, with the same exit, over five seeds.

| Book (rule / exit) | Worst 10% of windows | Typical (median) | Best 10% | Windows that made money | Worst window |
|---|---|---|---|---|---|
| Best: new 252-day high, 20% trailing stop (R17a) | Rs42,500 | Rs50,000 | Rs61,850 | 48.9% | Rs29,900 |
| Random names, 20% trailing stop | Rs42,100 | Rs49,050 | Rs58,000 | 43.5% | Rs26,950 |
| Day's top gainer, sell at next close (the "reel", R1a) | Rs26,650 | Rs34,650 | Rs44,200 | 2.8% | Rs14,450 |
| Random names, sell at next close | Rs33,300 | Rs37,850 | Rs43,150 | 0.7% | Rs25,250 |

Of 192 rule books that held something in at least 90% of windows, only two had a median window at or above break-even, and only 37% beat the matching random book. The best book is the random book with a slightly fatter right tail: half the time you lose money, and the worst six weeks cost 40%.

Recent months (multiples of the starting Rs50,000; 1.00 means flat):

| Book | 17 Aug to 15 Sep | 16 Sep to 16 Oct (last month) | 16 Jul to 16 Oct (last three months, 65 sessions) |
|---|---|---|---|
| R17a breakout, 20% trail | 1.00 | 0.90 | 0.63 (Rs31,450) |
| R17b breakout on 2x volume, 20% trail | 0.98 | 1.00 | 1.62 (Rs81,150) |
| R4 two locks in three sessions, 20% trail | 0.75 | 0.79 | 0.69 |
| R1a reel, sell next close | 0.60 | 1.10 | 0.30 (Rs15,050) |
| R1a reel, +10% target or 5 sessions | 1.02 | 1.08 | 1.03 |
| R13a news-less rise, 20% trail | 0.96 | 0.75 | 0.62 |
| Random, 20% trail | 0.88 | 0.97 | 0.91 |
| Random, sell next close | 0.72 | 0.78 | 0.45 |
| Books up, of 192 | 22 | 47 | 15 |
| Median book | 0.84 | 0.89 | 0.66 |

The three-month column comes from a rerun of the same pre-registered script with one window added. It reproduced every original number exactly, and the output is in `tests/out/pattern_mining_daily_books_3m.csv`. Look at R17a and R17b. They are nearly the same rule, yet over the same three months one book lost 37% and the other gained 62%, because one or two trades decide a small book. That is path luck, not skill, and it is why a three-month result proves nothing either way. Trading daily at the next close lost more than half the money in three months, mostly to costs: about 65 round trips at 0.5% to 1% each.

## 2. Which situations pay over 1 to 10 days after costs

All figures are in-sample, net of costs, per trade. "Episodes" counts a name's signals within ten sessions once. "Random" is a random same-day, same-liquidity entry with the same exit.

| Situation (rule) | Episodes | Exit | Mean | Median | Win | Worst | vs random | Out of sample |
|---|---|---|---|---|---|---|---|---|
| Day's top gainer (R1a) | 1,595 | next close | -1.24% | -1.32% | 36% | -17.7% | worse by 0.26% | 33 trades, -0.51% |
| Same, sell next morning's open | 1,595 | next open | -0.67% | -1.22% | 39% | -24.5% | +0.05% (p 0.09) | 32 trades, +0.77% |
| A 5%+ day without results (R8b, nearest to "a 7% day") | 5,761 | next close | -1.23% | -1.47% | 35% | -18.7% | worse | 243 trades, -2.04% |
| 5%+ day on 3x volume (R19) | 3,435 | next close | -1.53% | -1.86% | 32% | -18.5% | worse | 105 trades, -2.54% |
| First upper lock after a quiet base (R3a) | 1,533 | next close | -1.30% | -1.44% | 34% | -12.7% | worse | 20 trades, -4.44% |
| Two locks in three sessions (R4) | 1,850 | next close | -1.28% | -0.85% | 41% | -18.7% | worse | 51 trades, -1.64% |
| News-less rise, +8% in 5 days (R13a) | 1,832 | next close | -1.36% | -1.67% | 32% | -16.0% | worse | 66 trades, -1.78% |
| Three up days in a row (R5a) | 10,069 | next close | -0.83% | -1.00% | 32% | -17.8% | level | 237 trades, -1.12% |
| Lower-lock close (R21) | 3,216 | next close | -0.40% | -0.80% | 41% | -19.3% | level | 80 trades, +1.33% |
| Fell 10% in 3 days (R22) | 2,902 | next close | -0.46% | -0.69% | 42% | -17.7% | better by 0.18% | 177 trades, -0.27% |
| Index -3% day, buy the 3 worst fallers (R11a) | 108 (39 dates) | next close | +1.08% | +0.83% | 61% | -12.5% | better by 1.10% (p 0.005) | none: no -3% day since |
| Index -2% Friday, buy 3 big names Monday (R16) | 22 | next close | +0.97% | +1.11% | 67% | -7.0% | level (p 0.50) | none |

The rule is simple: chasing strength loses after costs and loses relative to random. Buying weakness after a fall is roughly break-even, and better than random only by fractions of a percent. The one striking cell, buying panic-day fallers, rests on 39 market crash days, which amounts to one story told 39 times.

**A ceasefire-type rebound** (the market crashes, then a sudden all-clear) was never tested directly. The nearest proxies are R11a and R16 above: buying into the panic paid in sample, but R16 did no better than any random big name on the same day, so the gain was the market bouncing, not stock picking. To check the other side, I asked the engine what happened after a liquid stock jumped 9% on a strong sector or index day, having fallen about 8% over the prior month (exploratory, one query each, not pre-registered). The 91 sector-day analogues had a 5-session median of -1.0% (43% up, -1.5% after costs). The 71 index-day analogues had -0.6% (42% up). Buying the rebound day itself, after the jump, did not pay. If anything was in it, you had to be in before.

**Exits.** None of these exits turned a losing entry into a winning one over 1 to 10 days:

- **Sell into the first lock (else day 5)** was the worst exit for most rules: top gainer -1.77% mean, two locks -1.79%, news-less rise -1.80%. Only 3% to 5% of trades locked their way above +10%. The rest were held for five days and drifted down.
- **Fixed targets (+5% within 3 sessions, +10% within 5)** raise the win rate but not the average. Two locks with a +5% target: median +2.6%, 54% wins, mean -1.06%, worst -34%. Fell 10% in 3 days with a +5% target: median +4.0%, 60% wins, mean -0.41%. Many small wins are paid for by a few large losses.
- **First red day (else 20 sessions)** and the **20% trailing stop** hold longer than ten days and lift the average (two locks, trail: mean +2.06%, median -3.30%, 25% of trades above +10%). They are lottery tickets: random entries with the same trail made +0.5% to +1.0% because the market drifted up. Out of sample, for the top-gainer, two-lock and breakout rules, both exits lost 11% to 20% a trade.

## 3. Do news-less rises come before news, and does joining them pay?

Your hypothesis was that a rise with no public information means insiders know. We tested 5,935 episodes: a stock up more than 8% in five days, with no filing in ten sessions and its sector not up.

- **News does follow, but no more often than silence alone predicts.** 26.6% were followed by a filing (results, material information, dividend, insider trade or board notice) within ten sessions, against 23.4% for the same names in the same months. Compared with the same names in the same quiet state, the rate is 26.7%, which is exactly chance. A news-less fall is followed by news 25.0% of the time. The "signal" is that a quiet company is nearer its next scheduled notice, whichever way the price moved. The unscheduled kinds (material information, insider trades) are not pulled forward.
- **Joining does not pay.** Net median is -1.3% at 5 sessions, -2.5% at 20 and -9.8% with the 20% trailing stop. The median is below random same-day entries at every exit, and the mean equals random. Above Rs5m traded value the median is -2.3% to -11.7%. 83% of these episodes are in names under Rs5m a day, where fills are doubtful.
- **Waiting for the news does not help either.** The stock does not run into the filing (median -0.3%), the news day moves about 0%, and buying after the news is at or below random news-day entries.
- **The winners look like the losers at entry.** Same size of rise, same volume, same liquidity. Fewer locks in the last five days was slightly better, and the top quarter of rises (above 15%) was worse. The positive averages come from rare +50% jumps in small non-KMI names in easing years.

## 4. How to read the situation engine, and what the 16 Oct scan says for Monday

The engine answers one question: "when stocks were in a situation like this before, what did a buyer at the next open get?" It matches the cause exactly (results filing, other filing, insider filing, board notice, sector move, index move, or nothing), then finds past days with similar 1, 5, 20 and 60-day moves, distance from the yearly high, up-day streak, recent locks and volume. It uses only data known at that close.

Read the output in this order:

1. **ep (distinct name-months), not n.** Below 30 name-months is anecdote. A "THIN" flag means even less.
2. **The widening line.** "Regime dropped" or "tier +/-1" means the matches are looser.
3. **Median against placebo** (a random stock on the same dates). If the median is no better than placebo, the situation adds nothing.
4. **Net** (median after costs) and the **p10 to p90 range.** That range is your realistic outcome band.
5. **Red next session and MAE** (the typical worst dip before exit), so you know what holding feels like.

The scan for 16 Oct covered liquid (above Rs5m) KMI names with a move above 5%, a lock, a news-less rise, a results filing or a sector lead. Eight of 125 qualified. Returns are gross, from Monday's open; costs take a further 0.5% (hi tier) or 1.0% (mid tier).

| Name | Why flagged | ep | Median 1 / 3 / 5 days | 5-day middle half | 5-day 10%-90% | Up at 5 days | Random at 5 | Note |
|---|---|---|---|---|---|---|---|---|
| STL | results filing, +1.2% | 66 | -0.3 / -0.5 / 0.0% | -3.8 to +2.6% | -8.7 to +6.9% | 48% | -0.1% | Signature shows -98.9% from the yearly high and -40% over 60 days: an unadjusted corporate action (STL was one of the four data-break names). Ignore this read. |
| POWER | cement sector leader, +2.8% | 98 | -0.2 / -0.6 / -0.2% | -3.5 to +2.2% | -6.1 to +5.7% | 48% | -0.9% | Slightly better than random, still a coin flip before costs. |
| SYM | +8.7%, sector leader | 72 | -0.6 / -1.2 / -0.4% | -4.2 to +3.9% | -7.9 to +7.6% | 47% | -1.4% | Volume is low (0.2x). A 7%+ day with no news gives back a little. |
| SLGL | news-less rise (+12.9% in 5 days), -3.7% Friday | 78 | -0.4 / -0.7 / -1.4% | -4.4 to +3.0% | -8.3 to +6.4% | 40% | -1.3% | Level with random; 66% red on the next session. |
| WASL | +6.0% | 27 | 0.0 / -0.3 / -1.6% | -5.5 to +4.2% | -7.8 to +9.2% | 45% | +0.4% | Below 30 name-months; worse than random. |
| KEL | insider filing, +3.0% | 33 | -0.2 / -0.5 / -1.7% | -3.3 to +2.6% | -7.2 to +7.7% | 35% | -1.4% | The 20-day median is +4.5% (68% up), the only positive horizon, on 30 name-months. Watch it; it is not a trade. |
| AGP | other filing, +4.1%, 4 up days | 34 | -0.2 / -0.6 / -1.7% | -4.7 to +0.3% | -7.3 to +5.6% | 28% | -0.7% | Regime dropped. Weak. |
| PRL | board meeting (results Tue 20 Oct), +14.9% in 5 days, +110% in 60, at its high | 29 | -2.1 / -2.5 / -2.6% | -5.5 to +1.7% | -9.2 to +2.9% | 37% | -0.4% | Worst read: 69% red the next session, typical dip -6.9% within 5 days. Loosest match (regime dropped, tier widened). |

**What it says for Monday:** none of the eight has a positive 5-day median after costs, and none is a short-term buy on base rates. PRL is the breakout sleeve's first buy under PICKS.md v3. The engine reading does not override that rule, because the sleeve is a 20% trailing-stop position held for months, not a five-day trade. Expect a pullback into Tuesday's result, and do not read a 5% dip as the rule failing. That disagreement between rule and analogues is exactly what the live scorecard should score.

## 5. The honest limits

- **Survivors and delisters.** 142 delisted names are included, but losses after a name's last trade are not, which flatters every result slightly.
- **Hindsight sector baskets.** "Sector leader" and "sector not up" use today's sector lists, which hold the survivors.
- **Multiple testing.** 240 tests were run. 18 have p of 0.01 or less, where chance alone gives about 2.4, so there is something in the tail. But 107 tests were worse than random at p 0.99 or more, and nothing passed all four screens. Any single good-looking row may be luck.
- **No intraday data.** Entries are at the open and exits at the close or a target touched by the high. Spreads, queue position at a lock and partial fills are not modelled. A stock that opens at the upper limit was treated as unbuyable. The intraday archive only started on 16 Oct 2026.
- **Thin names.** Most of the striking cases trade under Rs5m a day, and the extra 0.5% slippage assumed there is probably too little.
- **Out-of-sample is short.** It covers seven weeks in one falling market: a weak check in both directions.
- **The engine is untested as a predictor.** Its buckets and widening ladder were set by hand once. Its calls have never been scored in-sample against out-of-sample.
- **Judgement is untested.** The model's own discretionary calls cannot be backtested, because it remembers 2026 (`knowledge/HOW_TO_THINK.md` section 10). Only forward scoring can test them.
- **Tax.** 15% CGT on gains comes on top of everything here.

## 6. The daily routine that follows

The base rates say not to trade these situations mechanically. They do not say your eye is worthless. SSGC and PRL in July were right-tail cases outside their analogue sets, and the only way to learn whether you can spot those is to score yourself forward, cheaply, before risking the core. So the short-term work becomes a measured paper habit, with money following only a proven record.

1. **At the close (after 15:30):** run `python scripts/engine.py --scan <date>`. Add any name you noticed yourself with `python scripts/engine.py SYMBOL <date>`.
2. **Read the analogues** in the order in section 4: ep, widening, median against random, net, range.
3. **Freeze a call before the next open** in `catalysts/frozen_predictions.csv`: name, direction, a 5-day range (start from the analogues' middle half and move it only with a written reason), your probability of being up at 5 days, and what you know that the engine does not.
4. **Score at 1, 3 and 5 sessions:** inside the range or not, sign right or not, and your probability against the analogue win rate.
5. **Weekly diagnosis (Saturday):** for every miss, write one cause: the data was wrong (as with STL), the situation had no analogue, news arrived, the market moved everything, or "unknown". Count how often your calls beat the engine's.
6. **The gate:** no real money on a short-term call until about 20 scored calls show your probabilities beating the analogue base rate, after costs. Until then the money stays in the core and the breakout sleeve.

## Verdict

Short-horizon trading on PSX from daily signals does not pay after costs: across 240 tests, nothing survived out of sample and across regimes, and the best Rs50,000 book is break-even over a typical six weeks with a 40% worst case. Chasing strength (top gainers, 7% days, locks, news-less rises) is worse than random. News-less rises do not predict news. Panic-day buying of the worst fallers is the one live hypothesis, and it waits for the next -3% day. Keep the core and the breakout sleeve, and run the scan and scored paper calls as the way to find out whether your instinct beats the base rates.
