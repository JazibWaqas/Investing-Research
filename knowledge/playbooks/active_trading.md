# Active trading: what Rs50,000 could have become, and what we change

Written 18 Oct 2026, prices to 16 Oct 2026. This file answers the user's challenge ("you stayed too long; constant buying and selling should have tripled Rs50k in two years") from four studies: `tests/fixed_capital_runs.md`, `tests/oracle_and_good_case.md`, `tests/winners_case_control.md` and the independent Codex replication `tests/active_trading_codex.md`. Raw numbers are in `tests/out/`. No new backtest was run; the blends in section 5 are arithmetic on those files' rupee values.

Naming warning: two rules are called "S3". In `fixed_capital_runs` it is the **regime strategy** behind the PICKS core (sector by rate regime, cheapest sound name, quarterly review). In `oracle_and_good_case` it is a **52-week-high breakout with a 20% trailing stop**. Here they are "regime S3" and "breakout".

## 1. Rs50,000 on 1 Oct 2024, marked on 16 Oct 2026

| Path | Value | Multiple | Max DD | Source |
|---|---|---|---|---|
| Regime S3 (our mechanical strategy) | Rs67,855 | 1.36x | -41.7% | fixed_capital_runs |
| Random quarterly rotation, median of 1,000 | about Rs72,000 | 1.44x | | fixed_capital_runs |
| KMI All Share TR | Rs90,375 | 1.81x | -21.3% | fixed_capital_runs |
| KSE100 TR | Rs101,718 | 2.03x | -22.6% | fixed_capital_runs |
| Good case: breakout | Rs122,927 | 2.46x | -26% | oracle_and_good_case |
| Good case: HIGH52 (Codex's version of the same idea) | Rs130,953 | 2.62x | -35% | active_trading_codex |
| Best single name, hindsight (QUICE) | Rs268,834 | 5.38x | -49.6% | fixed_capital_runs |
| Oracle, best 3 names a month, 1% participation cap | about Rs12.4m | 248x | | oracle_and_good_case |
| Oracle, best 3 a month, no cap | about Rs96m | 1,921x | | oracle_and_good_case |

The honest answer to "what would my Rs50k be worth" is Rs67,855. That is below the index and close to the random median: regime S3 beat only 41% of the random draws. It rose to Rs101,226 on 1 Oct 2025 and then gave a third of it back. ECOP (-43%) and CHCC (-27%) were held through the 2026 reversal because the rule reviews quarterly and uses no stops. On that point the user is right: this strategy stayed too long.

PICKS.md v2 is judgement and cannot be replayed. Its core names made about 2.24x from 17 Oct 2024, but they were chosen in Oct 2026, so that describes winners, not evidence.

## 2. What a well-informed constant trader could have made

The oracle ceiling (perfect foresight, monthly) was tens to hundreds of times the stake in **every** window, bad ones included. With the 1% participation cap, best-3 monthly made 45x (2016-18), 63x (2018-20), 45x (2020-22), 99x (2022-24) and 248x (2024-26). The opportunity set was never the constraint. Prediction was.

The Codex file logs the oracle's monthly best single name, so we can see what those paths were made of:

| Window | Monthly picks | Distinct names | Position runs | Median gain per run | Names that recur |
|---|---|---|---|---|---|
| 2016-18 | 25 | 19 | 21 | +33% | NETSOL x3, PRL, ANL, DCL, FFL |
| 2018-20 | 24 | 18 | 24 | +23% | LOTCHEM x3, GHNI x3, SYS, CHCC |
| 2020-22 | 24 | 17 | 20 | +25% | NETSOL, GGL, MEBL, SYS, LOTCHEM, CHCC, UNITY |
| 2022-24 | 24 | 17 | 23 | +28% | ATRL, MLCF, KEL, MFFL, GAL, FLYNG |
| 2024-26 | 25 | 18 | 21 | +44% | SSGC x3, PRL x3, PREMA, QUICE, GAL |

The perfect path is a different stock almost every month (17 to 19 distinct names in 24 or 25 months), usually held for one month. Nothing stable sits behind it: no name kept winning, and the recurring names change from window to window. "Join quickly and leave" is exactly what the ceiling does, and it depends on predicting next month's best name, which section 4 shows we cannot.

The realistic "good case" is a simple rule from a pre-listed menu: eight systems in `oracle_and_good_case`, seven in the Codex file, fifteen in all. In 2024-26 four reached 2x: the breakout (2.46x), cheapest name in the three strongest sectors (2.33x), HIGH52 (2.62x) and the volume-surge rule VOL20 (2.02x). **None reached 3x.** Random monthly rotation reached 3x in 1.0% to 1.5% of 200 paths, and 8 of 87 liquid names did it by buy and hold, visible only afterwards.

## 3. Which systems reached 2x, and were they robust?

These systems reached 2x in at least one two-year window. The table gives the multiple in each window:

| System | 2016-18 | 2018-20 | 2020-22 | 2022-24 | 2024-26 |
|---|---|---|---|---|---|
| KMI All Share TR (cost 0.25% a side) | 0.80 | 1.01 | 1.02 | 1.74 | 1.82 |
| Random rotation median | 0.56 | 0.78 | 0.70 | 1.16 | 1.32 |
| **Breakout, 20% trailing stop** | 0.81 | 1.02 | **2.59** | **2.96** | **2.46** |
| **HIGH52 (Codex)** | 0.89 | 1.08 | **3.34** | **2.09** | **2.62** |
| Top-3 6-month momentum (S2) | 0.63 | 0.61 | 0.53 | **3.21** | 1.34 |
| Strongest stock in top-3 sectors (SECTOR63) | 0.71 | 0.91 | 1.69 | **3.46** | 0.78 |
| Results-day EPS jump (S6) | n/a | n/a | 0.97 | **2.98** | 1.43 |
| Volume surge (VOL20) | 1.02 | 0.45 | 1.03 | 0.80 | **2.02** |
| Cheapest in strong sectors (S4) | n/a | n/a | 1.03 | 1.38 | **2.33** |
| 3-month momentum (MOM63) | 0.99 | 1.23 | 1.84 | **2.04** | 1.50 |

Most of these were **one-window flukes**. SECTOR63 made 3.46x and then lost 22%. S2 made 3.21x and has lost money in three other windows. VOL20 made 2.02x after a 0.45x. The monthly momentum rotations S1 and S2 carried drawdowns of 59% to 68% in 2024-26. Of the two dip-buying rules, S5 never beat the index, and DIP200 beat it only in 2016-18 (0.83x against 0.80x).

Only one idea survived across windows: **buy on a new 52-week high and get out on a trailing stop.** Two independent implementations agree on its pattern, even though they differ in mechanics. HIGH52 has no stop: it rebalances monthly into names within 2% of their high. So the common element is buying strength near the high, more than the exit. The breakout ranked 1, 1, 1, 3, 1 in its menu, and HIGH52 sat above the random median in 5 of 5 windows (median placebo percentile 96th). Both made 2.1x to 3.3x in the three windows with a trend (2020-22, 2022-24, 2024-26). Both were flat in the two hike-cycle windows (0.81x to 1.08x), where they roughly tied the index. In 2020-22 the breakout made 2.59x while the index made 1.02x. That is the strongest single piece of evidence, because a flat market cannot explain it.

Drawdowns: breakout -20%, -43%, -18%, -19%, -26%; HIGH52 -25%, -44%, -19%, -27%, -35%.

Trade counts were low. The breakout made 7 to 12 trades a window, HIGH52 15 to 53. This is not constant buying and selling. In falling markets few names make new highs, so the breakout held fewer positions and was partly in cash. In 2018-20, five of its seven losers were banks, stopped out in the 2019 hike cycle and the March 2020 crash. Its 2016-18 result is weaker evidence, because the panel starts in Oct 2016 and the rule could not signal until Aug 2017.

The case against it is real:

- It was picked as the best of fifteen after the results were in.
- One or two trades carry each window: NETSOL +236% (2020-22), SAZEW +293% and HUBC +178% (2022-24, 91% of profit), FATIMA +165% and TPLT +71% (2024-26). Without its two best trades the breakout ends at 1.63x, 1.18x and 1.48x in the three good windows.
- Shifting the 2024 start by 16 days moved it from 2.46x to 2.12x.
- On the price-return panel, where ex-dividend drops trigger stops, it fell to 1.39x in the literal window, below the index.
- The windows overlap and the panel holds survivors only.

Treat the result as a weak, replicated edge, not a proven one.

## 4. What the winners had in common, and how much was knowable

`winners_case_control` found 129 cases of +100% in six months (2017 to 2026), in 83 sector episodes but only about six market phases. Before they moved, the winners were cheap-priced (median Rs24 against Rs57), thinner, further below their 52-week high, less often recent index additions, and showing slightly rising volume. Momentum, sector strength, insider buys, earnings changes and unusual-movement letters were all within noise.

Out of sample, that knowledge was nearly worthless at stock level:

- Top-decile precision was 5.82% against a 4.51% base rate, the same as a model trained on shuffled labels (5.91%).
- A rule screen had 94% false positives.
- Rs50,000 rotated into the screen from Oct 2024 became Rs58,299, against Rs83,284 for all liquid names and 1.68x for the index, with a -44% drawdown. The features that predict doublers also predict collapses.

What was knowable is **timing**. Doublers were 2.5 to 2.8 times more common when the 6-month T-bill sat below the policy rate, and 35% of them had 300bp or more of cuts in the next six months. Today the T-bill (12.40%) is above the policy rate (11.5%). That is the state with the low base rate, about 1.6%.

An inference, not a test: the breakout does not try to see the winner early. It buys once the stock has proved itself at a new high, and the median winner peaked at 2.71x after 127 sessions, which leaves room for a late entry.

## 5. The revised model

The evidence supports a **small trend-following sleeve that exits on stops**. It does not support fast rotation into predicted winners, and it does not support constant trading for its own sake. Random rotation did no better than holding the median name, and the frequent rotators had the worst drawdowns.

**Size: 25% of the book**, taken from the current satellite. No larger, because of the selection bias, the two flat windows, the two-trade concentration and drawdowns up to -44%.

**Rules, frozen as tested** (breakout system in `scripts/tests/oracle_and_good_case.py`, not tuned):

1. **Universe.** KMI All Share names with a 60-session median traded value above Rs5m.
2. **Entry.** A close above the highest close of the prior 252 sessions, on dividend- and split-adjusted prices. Buy at the next session's close. If there are more candidates than free slots, take the one furthest above its old high.
3. **Positions.** Three slots, each one third of the sleeve's value at entry (about 8% of the book). Never add to an open position.
4. **Exit.** Sell at the next close after a close 20% or more below the highest close since entry. The stop is measured on adjusted prices, so an ex-dividend drop does not fire it. There is no profit target, no time stop and no rotation.
5. **Cash.** Empty slots stay in cash. That cash is the rule's bear-market defence, so the four-week rule does not apply to it. Each month's deposit tops the sleeve up to 25% of the book, never above, and the rest goes to the core.
6. **Review.** Every six months, compare the sleeve with the KMI All Share TR and the random-rotation placebo. If it trails the index by more than 10 points after 24 months, fold it into the core.

**What it would have returned on Rs50k.** The sleeves are held unrebalanced, so the value is 0.75 x core + 0.25 x sleeve:

- From 1 Oct 2024, with the regime S3 core: 0.75 x 67,855 + 0.25 x 122,927 = **Rs81,623 (1.63x)**. That is Rs13,768 more than regime S3 alone, and still below the index.
- With an index-like core (KMI TR, S7): **Rs98,857 (1.98x)**.
- Same blend across the windows: 0.80x, 1.01x, 1.41x, 2.04x, 1.98x. On the price-return sleeve: 0.80x, 1.01x, 1.32x, 1.95x, 1.95x.

In this sample the blend never fell meaningfully behind the index, and it added up to 0.39x in trend windows. The one exception is the literal 17 Oct window on the price-return sleeve, where the blend made 1.65x against the index's 1.74x.

**The most likely outcome from here.** The current regime is TIGHT, a hike is expected on 26 Oct, and the market is coming out of a reversal. The comparable windows are 2016-18 and 2018-20. There every rule in both menus made 0.38x to 1.23x, and the blend made 0.80x to 1.01x. Expect the sleeve to sit partly in cash and roughly track the index until a cut cycle starts. In those two windows, no tested rule made 2x in two years. Rs150,000 from Rs50,000 needs +73% a year, and no pre-registered rule delivered it in any window.

Unverified: Finqalab's minimum commission on Rs4,000 tickets; a fixed fee could exceed the 0.25% a side assumed. Check before the first order.

## 6. What changes in PICKS.md and strategy.md

**PICKS.md: changes**

- The 25% satellite becomes the breakout sleeve, with the rules above.
- The four catalyst triggers (GHGL, NETSOL, PSO, EPCL post-offer) become frozen paper trades in `catalysts/frozen_predictions.csv`. They earn a sleeve slot only after ten scored calls beat their pool. They have no measured edge; the breakout has a weak, replicated one.
- "No price stop-losses" becomes "no price stop-losses on the core". The Rs17.6m to Rs14.5m result was a stop on the value core, a different rule.
- The decision in five lines states that the active quarter follows strength with stops and does not predict.

**PICKS.md: stays**

- The 75% core (FABL, OGDC, FFC) bought Monday and every month.
- Event stops, the 25% and 35% name caps, the MEBL paper position and all frozen calls.
- The expectation that the whole book earns about the index.

**strategy.md: changes**

- Rule 3: the satellite is the breakout sleeve at 25%, not regime S3.
- Rule 4: no-stop applies to the core only.
- "Expected range" gains the fixed-capital table above.
- One flag. Fixed-capital regime S3 lost to the index over the last two years (1.36x against 1.81x) and beat it only from starts in Oct 2022 or earlier. That is a strike against the three-name core. The backtest of an index-like hand-built core moves up the "what would change this" list. The core is not changed today.

**strategy.md: stays**

- Deposit monthly, never wait in cash.
- Plan for a 40 to 50% drawdown.
- No stock-level predictive signal has passed a placebo, and this work confirms it.
