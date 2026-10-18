---
title: "Regime turn playbook: recognise the turn, join it, ride it, leave it"
written: 2026-10-19
status: "research hypothesis. The checklist is fitted to four real lows and four false bottoms; it has never been scored live."
evidence: "knowledge/regime_turns/ (2019.md, 2020.md, 2022_23.md, 2024_and_now.md), knowledge/CATALOGUE.md section 1, knowledge/winners/_life_changing.md and _rate_cut_and_shock.md, knowledge/situations/01 to 06 and 12, data/macro/*, seed/data/macro/imf_events.csv, data/daily_table.parquet, data/panel_close_adj.parquet. New arithmetic: scripts/tests/regime_turn_playbook.py, output tests/out/regime_turn_playbook.txt (data to 16 Oct 2026)."
---

# Regime turn playbook

Written 19 Oct 2026, prices to the 16 Oct close. **Knowable** means the number was public on the date. **Hindsight** means it needed later data. Not modelled anywhere here: costs, tax, fills or limit locks.

**Terms used below.**
- **50-day / 200-day average:** the average close of the last 50 or 200 sessions. Price above the 200-day means the long trend is up.
- **Breadth:** the share of liquid stocks (over Rs5m traded a day) closing above their own average.
- **252-high:** a close above every close of the past year (252 sessions).
- **Policy rate / MPC:** the State Bank's rate, set by its Monetary Policy Committee.
- **6M bill gap:** the 6-month T-bill auction yield minus the policy rate. Above zero, the market expects hikes. Below zero, it expects cuts.
- **Real rate:** the policy rate minus inflation (CPI).
- **SLA:** the IMF staff-level agreement. The **Board** approval comes after it and releases the money.
- **Reserves:** SBP's dollar holdings, published weekly.
- **Drawdown:** a fall from a peak.
- **Trailing stop:** sell when the price closes X% below its highest close since you bought.
- **P/E:** price divided by a year's earnings.

## 1. What a regime turn is

A regime turn is the point where the PSX goes from most stocks falling to most stocks rising for a year or more. It happens when what was crushing the market stops getting worse: a hike cycle with a dollar shortage (2019, 2023) or a shock that policy backstopped (2020). The index turns first; the rest follows over weeks to months.

It matters because it is where fortunes start. 33 of the library's 34 liquid runs of 5x or more began in April to August 2019 or October 2022 to November 2023, the two hike-cycle bottoms. The one exception is CLOV in 2017 (`_life_changing.md`). A turn comes every two to four years. In between, in the 2017 to 2019 and 2021 to 2022 bears, 4% of liquid names rose over two years (CATALOGUE section 1).

| | Aug 2019 | Mar 2020 | Jun 2023 | Jun 2024 |
|---|---|---|---|---|
| Low (KSE100 close) | 16 Aug, 28,765 | 25 Mar, 27,229 | 23 Jun, 40,065 | 11 Jun, 72,589 |
| Cause of the fall | Hikes to 13.25%, rupee devaluation, reserves at $7bn | Covid crash | Default scare, CPI 38%, policy rate 22%, reserves $3.5bn | None. A pullback inside a bull market |
| What turned it | Rupee flat for 7 weeks, reserves rising, IMF Board done, then a rate hold on 16 Sep | 625bp of cuts, IMF review agreed, oil at $22 | IMF SLA on 29 Jun with $3bn of bilateral money; reserves nearly doubled in 3 weeks | First rate cut, CPI down 11 points in 3 months |
| Fall from the prior 252-high | -33% | -37% | -8% (the January low was -18%) | -4.5% |
| KSE100, 12 months after the low | +40% | +63% | +101% | +60% |
| Where the run ended | 13 Jan 2020 (+50%), then Covid | 14 Jun 2021 (+79%), then the 2021 to 2022 hikes | 23 Jan 2026 (4.7x), then the Iran war oil shock | Same run as 2023 |

Sources: the four files in `knowledge/regime_turns/`. The KSE100 and KMI All Share used here are total-return series (`data/macro/INDEX_NOTES.md`).

## 2. The live checklist: signals at real lows against false bottoms

A **false bottom** is a trough that looked like a low, bounced, and was then broken. Four of them are set against the four real lows. Every value comes from `tests/out/regime_turn_playbook.txt`, section 1.

| Signal | Aug 2019 | Mar 2020 | Jun 2023 | Jun 2024 | False: 16 Oct 2018 | False: 19 Mar 2020 | False: 21 Jul 2022 | False: 14 Sep 2026 |
|---|---|---|---|---|---|---|---|---|
| **A. Oil calm:** Brent not up more than 10% in 13 weeks (knowable on the day) | ✔ -20% | ✔ -63% | ✔ 0% | ✔ -4% | ✘ +14% | ✔ -66% | ✔ +5% | ✘ +44% |
| **B. Drain:** two sessions later, under 10% of liquid names are at a 20-session low (knowable 2 days later) | ✔ 0% | ✔ 8% | ✔ 2% | ✔ 3% | ✔ 2% | ✘ 99% | ✘ 14% | ✘ 37% |
| **C. Rupee flat:** USD/PKR moves less than 2% in the 4 weeks after (knowable after 4 weeks) | ✔ -1.6% | ✔ +0.1% | ✔ -0.5% | ✔ 0.0% | ✔ +0.5% | ✘ +5.2% | ✘ -4.9% | ✔ -0.1% |
| **D. Reserves up:** SBP reserves higher 4 weeks after (knowable after 4 weeks) | ✔ +$0.3bn | ✘ -$1.1bn | ✔ +$4.1bn | ✔ +$0.3bn | ✘ -$0.6bn | ✘ -$1.7bn | ✘ -$1.4bn | ✔ +$0.1bn |
| **Score A to D** | **4** | **3** | **4** | **4** | **2** | **1** | **1** | **2** |
| E. Thrust: over 50% of names above their 200-day within 10 sessions | ✘ 3% | ✘ 32% | ✔ 74% | ✔ 86% | ✘ 34% | ✘ 32% | ✘ 22% | ✘ 36% |
| F. New highs: at least 10% of liquid names make a 252-high within 10 sessions | ✘ 0% | ✘ 0% | ✔ 17% | ✔ 22% | ✘ 7% | ✘ 0% | ✘ 2% | ✘ 1% |
| *Not separators:* | | | | | | | | |
| Index below its 252-high | -33% | -37% | -8% | -5% | -21% | -30% | -17% | -11% |
| Names above their 50-day | 0% | 0% | 20% | 49% | 4% | 3% | 14% | 12% |
| Next MPC move | hold | -200bp | +100bp, named as the last IMF condition | -100bp | +150bp | -150bp | hold, then hikes | pending |
| 6M bill gap | +0.7 | +0.3 | +1.0 | -1.0 | +0.3 | -0.7 | +0.8 | +0.4 |
| IMF SLA or Board within 60 days before to 30 days after | Board | SLA | SLA and Board | none (SLA came 31 days later) | none | SLA | SLA | SLA (8 Oct) |
| Outcome | held | held | held | held | broken Apr 2019 | broken 25 Mar | broken Dec 2022 | broken 13 Oct |

**How to read it.**
- **Real lows scored 3 or 4 on A to D. False bottoms scored 1 or 2.** The rule is to treat a low as real only at 3 or more.
- A and B are knowable within two days. C and D need four weeks, so the full score is never available at the low itself.
- E and F confirm a turn when they are present. Their absence proves nothing: the two deepest lows, 2019 and 2020, had neither.
- Depth, a breadth washout, the rate decision, the bill gap and an IMF headline did not separate them. The bill sat above policy at three of four real lows, and an SLA came near three of four false bottoms. Waiting for a cut would have missed 2019 and 2023.
- The checklist is fitted to these eight dates, so it is a hypothesis (section 7).

## 3. The sequence: what moves first

Groups are fixed on the low date; adjusted closes. Large = the 20 most-traded liquid names, mid = other liquid names, small = Rs0.5m to 5m a day. Source: output file, section 2.

| Weeks for the group median to reach +20% | 2019 | 2020 | 2023 | 2024 |
|---|---|---|---|---|
| KSE100 | 10.8 | 3.4 | 4.6 | 17.8 |
| Large caps | 6.6 | 1.4 | 4.4 | 18.4 |
| Mid caps | 6.0 | 1.2 | 3.0 | 23.2 |
| Small caps | 6.8 | 1.4 | 15.0 | 23.4 |
| Cyclicals (cement, steel, autos) | 6.2 | 1.2 | 14.8 | 19.8 |
| Tech | 7.4 (1 name) | 1.0 | 1.4 | 5.2 |
| Banks (Islamic only; the table lacks HBL, MCB and UBL) | 14.8 (1 name) | 1.4 | 3.0 | 3.0 |
| E&P and fertilizer | 7.8 | 3.4 | 18.8 | 13.8 |
| First liquid 252-high, sessions after the low | 63 | 16 | 2 | 2 |
| Index first close above its 50-day, sessions after | 19 | 26 | 1 | never below it |
| **Best group at 26 weeks** | cyclicals +57%, mid +57% | tech +184%, cyclicals +109% | banks +69%, index +61% | pharma +91%, E&P and fertilizer +70% |

**The order, in plain words.**
1. **Weeks 0 to 4: the index and the large caps move first.** After a shock they move within days (2020: large caps +20% in 1.4 weeks). After a slow grind they take 4 to 7 weeks.
2. **Weeks 1 to 5: tech and banks sprint early.** Tech reached +20% first in three of four turns (2020, 2023, 2024). Banks did the same in 2023 and 2024. Tech kept leading only in 2020, when the rupee fell 5% in three days and dollar earners gained. By 26 weeks in 2023 and 2024 tech had fallen behind the index (+36% against +61%, +10% against +46%).
3. **Weeks 4 to 26: cyclicals and sector leaders take over.** After the deep lows (2019, 2020) cement, steel and autos were the big 13 to 26 week winners. After the shallow lows (2023, 2024) they lagged for three months, and pharma, power, refiners and E&P led at six months.
4. **Small caps come last or tie.** They were never ahead of large caps at 8 weeks. In 2023 and 2024 they needed 15 to 23 weeks to make +20%.
5. **The future 5x runs show themselves late.** The first 15 names at a 252-high are mostly last cycle's winners (13 of 15 in 2024, 12 of 15 in 2023); runs that began at the turn made their first 252-high a median 68 to 226 sessions after the low (`2024_and_now.md`, section 8).

## 4. The entry plan for a person with monthly deposits

The `PICKS.md` rule stands: Rs50,000 a month, 75% core (three large KMI names), 25% breakout sleeve; stopping deposits is the one thing that reliably loses. A turn changes only what you do with uninvested money, **C**: the month's deposit plus anything held back while the regime was hostile.

| When | Test | Action | Why |
|---|---|---|---|
| **Week 1** after a trough | A and B present (oil calm, drain under 10%) | Put **one third of C** into the core names. | All 15 index entries at +1, +4 and +8 weeks in five finished turns were up 16% to 80% a year later (`2022_23.md` rule 4); in 2020 and 2023 week 1 beat week 8 by 16 to 17 points. |
| **Week 4** | Score 3 or more, and the MPC has not hiked (an IMF-named final hike, as on 26 Jun 2023, is the one exception) | Put **another third of C** into the core. From this month, the sleeve's Rs12,500 ticket buys a KMI liquid name at its first 252-high in the leading sector. | 2019: the 4-week entry beat week 1 (+35% against +26%); the hold came on 16 Sep. |
| **Week 8** | Score still 3 or more; the index is above its 50-day | Put **the rest of C** in. Hold up to three leaders, each at most 25% of the book. | Week 8 was best in 2024 (+92%) and worst in 2019 (+18%, Covid); thirds average the spread. |
| **Leaders** | Each leader at its own first 252-high | Stop: 25% below the high close for index-led names (banks, cement). 30 to 40% for stock-specific names. | On the 34 five-baggers a 20% stop left a median +28%, 30% left +167%, 40% left +231% (`_life_changing.md`). |

**What makes you wrong. Stop adding the remaining thirds if any of these happens:**
- The index closes below the suspected low. In the 2017 to 2019 bear, three bounces of 8% to 15% failed this way.
- The MPC hikes, other than an IMF-named final hike.
- USD/PKR moves more than 3% in four weeks, or reserves fall by more than $1bn.
- Brent rises more than 10% over 13 weeks.

If one fires, keep the monthly core deposits going. Do not sell the core: from the knowable entries, the KMI All Share's worst fall was 37% in Covid and 22% from 2021 to 2023 (section 5). The leaders are sold only on their own stops.

## 5. The exit plan: where runs ended and what came before

Source: the output file, sections 3 and 4.

| Peak (KSE100) | 13 Jan 2020 | 14 Jun 2021 | 3 Jan 2025 | 23 Jan 2026 | 6 Jul 2026 |
|---|---|---|---|---|---|
| Index above its 200-day | +22% | +11% | +42% | +28% | +11% |
| Names above 50-day (highest in the prior 60 sessions) | 90% (100%) | 95% (95%) | 94% (98%) | 66% (86%) | 87% (94%) |
| P/E (series starts 2022) | n/a | n/a | 9.8 | 10.4, the series high | 9.3 |
| CPI, change over 3 months | 13.7%, +0.9 | 10.8%, +2.2 | 4.1%, -2.8 | 5.6%, 0.0 | 11.1%, +3.8 |
| Real rate | -0.5 | -3.8 | +8.9 | +4.9 | +0.4 |
| 6M bill gap | 0.0 | +0.6 | -1.0 | -0.6 | +0.2 |
| Foreign net buying, last 60 sessions | +$2m | -$75m | -$122m | -$176m | -$199m |
| Next hike | Sep 2021 | 20 Sep 2021 (98 days later) | Apr 2026 | 27 Apr 2026 | none yet |
| What followed | Covid, -37% by 25 Mar | -21% by Jan 2023. The median stock fell 52% and only 4 of 95 names rose (situation 03) | -6%, a pause. New high by 19 Mar 2025 | Iran war from 28 Feb, -23% by 9 Mar | -12% by 13 Oct, still open |

**What preceded the tops.**
- **2021** was the textbook regime end: CPI rising, a negative real rate, and the bill above policy three months before the first hike. That combination is the exit signal (bill gap positive, CPI up over three months, real rate near or below zero). It was also present at the July 2026 high.
- **January 2026** had the series-high P/E (10.4), narrowing breadth (66% against 86% weeks earlier) and foreign selling, but sound macro. The oil shock ended it, and nobody could forecast that.
- **January 2025 looked like a top on stretch** (42% above the 200-day) but was a pause. Being stretched alone is not an exit.
- **January 2020 gave no warning** before Covid.

Two of five endings were unsignalled shocks: hence a stop as well as a regime test.

**Stops on the index core** (KMI All Share total return, cash earning the 3-month bill when out, values at 16 Oct 2026):

| Entry | Buy and hold (worst fall) | 10% trail | 20% trail | 20% trail, buy back above the 200-day | 25% trail, buy back above the 200-day | In above the 200-day, out below |
|---|---|---|---|---|---|---|
| 16 Sep 2019 | 4.41x (-37%) | 3.01x | 2.59x | 3.90x | 3.85x | 3.99x |
| 3 Apr 2020 | 4.36x (-22%) | 3.09x | 2.35x | 4.02x | 4.36x, never fired | 3.92x |
| 3 Jul 2023 | 3.04x (-21%) | 1.99x | 2.86x | 2.71x | 3.04x, never fired | 2.57x |
| 21 Jun 2024 | 1.87x (-21%) | 1.65x | 1.76x | 1.67x | 1.87x, never fired | 1.58x |

**What the stop table says.**
- On the index, no stop beat holding. A **25% trailing stop with a buy-back on the first close above the 200-day average** kept 87% to 100% of the buy-and-hold result and fired only once, in Covid.
- The 10% placeholder in the catalogue kept 65% to 88% and should be dropped.
- The index hides damage: from 2021 to 2023 it fell 22% in rupees while the median stock fell 52% (situation 03). So when the exit signal fires, the leaders and the sleeve move into the core; the index stop is only for shocks.
- For leaders, per-name stops (section 4) with a buy-back on a reclaim of the old high left +179% on the five-baggers, nothing worse than +2% (`_life_changing.md`).

## 6. Today, 19 Oct 2026

The current trough is 13 Oct, KSE100 164,776: 12.9% under the 23 Jan peak of 189,167 and 1.9% under the 14 Sep false bottom. At the 16 Oct close the index was 166,420. That is 3.6% under its 50-day average (172,656) and 3.4% under its 200-day (172,197). Of 127 liquid names, 16% are above their 50-day and 31% above their 200-day.

| Signal | Reading | Status |
|---|---|---|
| A. Oil calm | Brent $126.55 on 14 Oct, +50% in 13 weeks ($84 in mid-July) | **absent** |
| B. Drain | 7.0% of names at a 20-session low on 15 Oct, 6.3% on 16 Oct (21% on the trough day) | **present** |
| C. Rupee flat over the 4 weeks after | Resolves about 10 Nov. The USD/PKR file ends 30 Sep, flat at 277.4 | **unknown** |
| D. Reserves up over the 4 weeks after | Resolves about 10 Nov. Latest print $21.47bn on 9 Oct, +$4.2bn in 13 weeks | **unknown** |
| Score so far | 1 present, 1 absent, 2 unknown. The best possible is 3 | |
| E. Thrust | 32% of names above their 200-day after 3 sessions. Needs over 50% | absent so far |
| F. New highs | 4 names (ATRL, MACFL, NRL, PRL), 3% of the list. Needs about 13 | absent so far |
| Context | MPC 26 Oct, 61% of brokers expect a hike (Topline, 17 Oct); 6M bill 12.40%, 0.9 over policy; Sep CPI 10.3% (unverified); IMF SLA 8 Oct, Board undated; P/E 7.9 (past lows 6.8 to 8.8); mutual funds bought $94m in 20 sessions (they sold at all four real lows) | mixed |

**What the playbook says to do now.**
- This is not a regime turn yet. The setup looks like the 14 Sep false bottom: a hike regime, an oil shock that is still running, and a bill pricing a hike. It does not look like any of the four real lows.
- Keep the `PICKS.md` deposits as written: Rs37,500 core and Rs12,500 sleeve.
- Do not commit any turn tranche (section 4) until the score reaches 3.
- Do not sell the core on this pullback. From past knowable entries, the 25% index leash has not been reached.

**What to watch, in date order.**
- **26 Oct MPC.** A hold removes a reason to wait. A hike keeps the regime hostile, unless the statement names it as a last condition, as in June 2023.
- **2 Nov October CPI.** A second monthly fall would start the rotation rule in `knowledge/playbooks/sector_rotation.md`.
- **Weekly reserves and USD/PKR to about 10 Nov.** These settle C and D.
- **Brent.** A turns present when the 13-week rise drops under 10%: Brent under about $92 now, or, if it holds near $125, around late December, when the comparison reaches late September ($116).
- **Price.** A close above about 172,700, the 50-day average. Within ten sessions of that, more than 50% of names should be above their 200-day and about 13 or more liquid names should make 252-highs. Those are E and F.
- **The IMF Board date for the fourth review.**

## 7. The honest limits

- **Four turns, fewer causes.** Two hike-cycle IMF bottoms, one shock, one policy turn inside a bull market. The rows were chosen after reading the turn files, so they are fitted to eight dates; another false bottom (Dec 2018, May 2019, Oct 2025) could break them.
- **Overlap.** Oil, rupee and reserves move together through the import bill; A, C and D may be one signal counted three times.
- **Survivors.** Delisted losers are thin in the price panel, so group medians and the 2021 to 2023 damage are understated. Breadth uses 41 to 127 names.
- **Hindsight.** A "real low" is real only because no lower close followed; live, you see a trough and a partial score.
- **Data gaps.** Indexes are rupee total return (dollar returns were far worse in 2022 to 2023). USD/PKR ends 30 Sep 2026; September 2026 CPI is unverified; the Mar 2020 and Jul 2022 SLAs were added from the turn files; conventional banks are missing from group returns.
- **Twelve-month results are in-sample.** The entry thirds and the 25% leash with a 200-day buy-back are hypotheses. They should be scored live in `catalysts/frozen_predictions.csv` before more money depends on them.
