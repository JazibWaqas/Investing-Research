# Big winners case-control: what did the doublers look like before they moved?

Run 18 Oct 2026. Script `scripts/tests/winners_case_control.py`. Output `tests/out/winners_case_control.txt`, `_events.csv` and `_features.csv` (every liquid name-month with its features and score). Not committed.

## Question

Could the 6-month doublers of 2017 to 2026 be seen at the start? And would a screen trained on 2017 to 2022 have found the ones in 2023 to 2026? If yes, fast rotation into big movers is worth building. If not, any best-case number is hindsight.

## Method

- **Universe.** Month-end starts Jan 2017 to Apr 2026, liquid (60-day median traded value above Rs5m, traded in the last 5 days): 12,021 name-months, 286 names. Prices come from `panel_close_adj.parquet` (cash complete only from Nov 2024), plus 284 delisted names on crude returns. 31 delisted files were dropped because they duplicate another code's history (renamings such as CLOUD/CWSM = QTECH, BYCO = CNERGY, EFOODS = FCEPL). Five events are delisted names.
- **Event.** A month-end to month-end 6-month return of +100% or more. A new event needs no qualifying start for that name in the previous 6 months. Peak and time to peak run to 6 months after the run's last qualifying start. The Apr 2026 window is cut at 16 Oct.
- **Controls.** 3 per event, 378 in total: same month, 6-month return under +50%, same sector where possible (62% were), nearest log traded value (median gap 0.16 log10), no name reused within a month.
- **Features at the start.**
  - Price: trailing 1/3/6/12-month return; distance from the 52-week high and low; 60/250-day traded-value ratio; log price; log traded value; sector 6-month momentum rank.
  - Filings: 90-day announcement counts by class (counted the same day if posted by 15:30); insider buys and sells; unusual-movement letters; index additions in the prior 6 months (major: KSE100/30, KMI30, MSCI, FTSE; also KMI All Share).
  - Macro: 6m T-bill minus policy rate; Brent 3-month change.
  - Fundamentals: EPS change YoY and QoQ and the loss-to-profit turn, at the first tradable date (quarter end + 90 days if missing). Earnings and dividend yield from `sa_ratios.csv` at the FYE quarter's first tradable date (else FYE + 120 days), rescaled to the current price.
- **Classifier.** Ridge logistic regression on all liquid name-months. The label is a 6-month return of +100% or more. Trained on starts up to Jun 2022, so every label is realised before the test period. Tested on Jan 2023 to Apr 2026, ranking names within each month. Fundamentals were left out because they cover 0 to 1% of training rows.
- **Costs.** 0.5% round trip, plus 0.5% slippage under Rs20m traded value.
- **Placebos.** Random names against random controls in the event months (200 draws); labels shuffled within month (20 refits); all liquid names and random picks for returns.

## 1. The events

129 events in 102 names, forming 83 independent sector episodes (same-sector starts within 3 months). The median 6-month return is +122% (mean +144%). The median peak is 2.71x, reached after 127 trading days. The largest is SAZEW from Mar 2023: 25.8x after 329 days.

| Start year | Events | Liquid name-months | Rate | Sector episodes |
|---|---|---|---|---|
| 2017 | 3 | 1,285 | 0.23% | 3 |
| 2018 | 1 | 1,070 | 0.09% | 1 |
| 2019 | 7 | 799 | 0.88% | 4 |
| 2020 | 30 | 1,210 | 2.48% | 19 |
| 2021 | 2 | 1,411 | 0.14% | 2 |
| 2022 | 0 | 947 | 0 | 0 |
| 2023 | 20 | 978 | 2.05% | 14 |
| 2024 | 33 | 1,508 | 2.19% | 22 |
| 2025 | 25 | 2,083 | 1.20% | 14 |
| 2026 (to Apr) | 8 | 730 | 1.10% | 5 |

2018, 2021 and 2022 together gave 3 events in 3,428 name-months. 13 of 2020's 30 started in March 2020. By month the events fall into about six market phases (Jul 2019, Feb to Mar 2020, Mar to Jun 2023, Jan to Jul 2024, Mar to Jul 2025, Jan to Mar 2026), so the 83 episodes are not independent draws.

By sector: Tech 16 (8 episodes), Food 15 (9), Refinery 10 (4), Banks 9 (4), Autos 9 (6), Cement 8 (4), Chemical 7, and Pharma, OMC, Engineering and Inv. banks 6 each. Twelve sector waves of 3 or more names hold 31% of events. They include the refiners in 2020 (ATRL NRL PRL) and Feb to Mar 2026 (PRL CNERGY NRL), the banks in Mar to Apr 2025 (JSBL BML AKBL NBP HBL), and pharma and cement in 2024.

## 2. Events vs matched controls

Sorted by |standardised difference|. "Placebo 95%" is the noise level. Regime and Brent are 0 by construction, because events and controls share a month.

| Feature | n ev / ct | Mean ev | Mean ct | Median ev | Median ct | Std diff | Placebo 95% |
|---|---|---|---|---|---|---|---|
| log10 price | 129/378 | 1.44 | 1.78 | 1.39 | 1.76 | **-0.60** | 0.21 |
| log10 traded value | 129/378 | 7.26 | 7.44 | 7.10 | 7.33 | **-0.36** | 0.19 |
| dividend yield | 15/78 | 5.9% | 7.8% | 5.4% | 4.7% | -0.27 | 0.44 |
| major index add, 6m | 129/378 | 0.07 | 0.14 | 0 | 0 | **-0.22** | 0.19 |
| distance from 52w high | 125/372 | -28.7% | -25.0% | -26.4% | -22.7% | **-0.21** | 0.16 |
| earnings yield | 35/115 | 0.21 | 0.16 | 0.12 | 0.12 | 0.20 | 0.35 |
| volume ratio 60/250 | 125/372 | 1.37 | 1.23 | 1.14 | 1.10 | **0.18** | 0.17 |
| sector momentum rank | 125/361 | 0.52 | 0.56 | 0.52 | 0.57 | -0.15 | 0.19 |
| insider buys, 90d | 129/378 | 0.16 | 0.04 | 0 | 0 | 0.12 | 0.17 |
| EPS YoY | 49/160 | 0.11 | 0.34 | 0.27 | 0.16 | -0.12 | 0.30 |
| 6m return | 125/373 | 34% | 17% | 6.5% | 3.4% | 0.12 | 0.16 |
| loss-to-profit turn | 49/163 | 0.22 | 0.18 | 0 | 0 | 0.12 | 0.29 |
| unusual-movement letter | 129/378 | 0.09 | 0.07 | 0 | 0 | 0.10 | 0.16 |
| 3m return | 127/377 | 15% | 6% | -3.3% | -0.5% | 0.10 | 0.15 |
| 12m return | 124/366 | 52% | 49% | 15.5% | 14.2% | 0.01 | 0.17 |

Five features clear the placebo (in bold), and all of them describe a cheap, thin, beaten-down name. Winners had a median price of about Rs24 against Rs57 for controls. They were less liquid even after matching, sat further below their 52-week high, were less often a recent index addition, and had slightly rising volume. Momentum, sector strength, insider buying, earnings change and unusual-movement letters are within the noise. Fundamentals have data for only 15 to 49 events, all in 2023 to 2026, so they are neither confirmed nor ruled out.

Price, liquidity and distance from the high hold up in both halves. The filing features do not. From 2017-22 to 2023-26, board notices go from -0.32 to +0.28, dividend/bonus notices from +0.32 to -0.22, and insider buys from +0.22 to -0.02.

## 3. Classifier, out of sample

| | Train (2017-01 to 2022-06) | Test (2023-01 to 2026-04) |
|---|---|---|
| Name-months / label positives | 6,276 / 108 | 5,299 / 239 |
| Base rate | 1.72% | **4.51%** |
| Top-decile precision | 4.11% (in-sample) | **5.82%** (32 of 550) |
| Lift / recall | 2.4x | 1.29x / 13% |
| Shuffled-label placebo, top-decile precision | | median 5.91%, range 2.91% to 8.91% |

The largest coefficients (distance from 52w low +, 12m return -, log price -, distance from 52w high -) describe a volatile, low-priced name. Test hit rate by decile, bottom to top: 2.3, 1.9, 2.3, 3.5, 4.5, 4.4, 5.3, 5.7, 9.3 and 5.8%. There is a gradient: about 7% in the top three deciles against about 2% in the bottom three. But the top decile does no better than the shuffled-label placebo. Of the 86 test events, 10% were in the top decile, 40% in the top three and 38% in the bottom half.

A simpler rule screen flags a name when it meets at least 3 of the 5 strongest training discriminators, each cut at the monthly 70th or 30th percentile. The five are low price, far below the 52w high, few board notices, dividend/bonus notices and no index addition. It flags 4% of test name-months. Precision is 6.1% against a 4.5% base, so 94% of flags are false positives, and recall is 6%.

## 4. What the screens would have earned (6m hold, net of costs)

| | n | Mean | Median | Win | Worst |
|---|---|---|---|---|---|
| Model top decile, test | 550 | +15.3% | +7.1% | 57% | -94.8% |
| Rule screen, test | 229 | +21.1% | +7.6% | 62% | -93.1% |
| All liquid names (placebo) | 5,299 | +18.6% | +8.7% | 62% | -94.8% |
| Random name per month, 500 draws | | | median of medians +12.6% | | |

Rs50,000 rebalanced every 6 months into the equal-weight model top decile:

| Span | Model top decile | All liquid EW | KMI All Share TR |
|---|---|---|---|
| 31 Jan 2023 to 31 Jul 2026 | Rs88,770 (1.78x), MDD -51% | Rs186,034 (3.72x), MDD -31% | 3.47x, MDD -21% |
| 31 Oct 2024 to 16 Oct 2026 | Rs58,299 (1.17x), MDD -44% | Rs83,284 (1.67x), MDD -31% | 1.68x, MDD -21% |

The big-winner screen lost to the index in both spans, with twice the drawdown. The features that predict doublers also predict collapses.

## 5. Events from 2024 to 2026: what flagged them

66 events; a selection is below and the full table is in section 6 of the raw output. Model pct is the percentile of that month's score. Flags are the top-8 discriminators at the monthly 70th/30th percentile in the event direction.

| Name | Start | 6m | Peak | Model pct | Wave | Flags at start |
|---|---|---|---|---|---|---|
| PRL | 2026-02 | +273% | 3.82x | 0.31 | yes | none |
| CNERGY | 2026-02 | +118% | 2.18x | 0.69 | yes | logprice |
| NRL | 2026-03 | +105% | 2.05x | 0.81 | yes | vratio |
| FCEPL | 2026-03 | +103% | 2.31x | 0.22 | no | none |
| ATRL | 2024-06 | +102% | 2.11x | 0.06 | no | ey, sect_rank |
| CNERGY | 2024-06 | +104% | 2.15x | 0.49 | no | logprice, dist52h, sect_rank |
| SAZEW | 2023-03 (run through Mar 2024) | +104% | 25.8x | | yes (autos) | (2023 start) |
| ASL | none | max 6m +81% | | | | not an event on month-end windows |
| QTECH | 2024-02 | +369% | 5.40x | 0.98 | no | logtv, vratio |
| THCCL | 2025-04 | +141% | 2.63x | 1.00 | no | dy |
| SGPL | 2025-12 | +143% | 3.65x | 0.99 | no | vratio |
| BNL | 2025-05 | +280% | 4.54x | 0.96 | yes | vratio |
| ASC | 2025-04 | +141% | 3.43x | 0.95 | yes | logprice, logtv, dist52h |
| PACE | 2024-06 | +168% | 2.71x | 0.94 | no | logprice, logtv, dist52h, vratio, sect_rank |
| BOP | 2024-06 | +122% | 8.85x | 0.88 | no | logprice, dist52h |
| Banks wave | 2025-03/04 | +106 to +172% | 2.15 to 3.61x | 0.02 to 0.80 | yes | JSBL 4 flags, HBL none |
| MARI, PSO, PNSC, EXIDE, HBL | 2024-25 | +106 to +165% | | 0.02 to 0.07 | | none or one |

Of the 66 events, 8 had a model percentile of 0.9 or more, 3 met the rule, and 24 were in sector waves. The 2026 refiners did not show up: PRL scored 0.31 with no flag, and CNERGY and NRL had one flag each. PRL's window opens on 27 Feb 2026, the day before the Hormuz closure. `tests/refiner_steel_retrospective.md` dates the launch to 7 Jul, ten weeks after a record quarter was ignored. Large caps scored lowest: ATRL, MARI, PSO and PNSC in Jun 2024 and HBL in Apr 2025, at 0.02 to 0.07. The Jun 2024 starts were followed by 750bp of rate cuts.

## 6. What was predictable and what was news

News after the start explains more than any stock feature, and the biggest piece is policy:

| Policy-rate change in the next 6 months | Name-months | Doubling base rate | Events |
|---|---|---|---|
| Cut of 300bp or more | 1,601 | 7.25% | 45 |
| Cut of 1 to 299bp | 2,104 | 3.47% | 27 |
| No change or a hike | 8,316 | 1.90% | 57 |

Part of this was visible in advance: the base rate was 4.0 to 4.5% when the 6m T-bill sat below the policy rate at the start, against 1.6% above. That times the market, not names. A prior 3-month Brent fall of more than 10% gave 5.0% (mostly Mar 2020); a Brent rise of 20% or more inside the window gave no lift (2.5%).

Of the 129 events, 35% had 300bp or more of cuts ahead (policy news), 17% were sector waves without such cuts (the 2026 war refiners, the 2025 banks), and 48% were idiosyncratic.

## Honest statement

- **Predictable from public data.** *When* the doublers come: in easing regimes, where a T-bill below the policy rate gave 2.5 to 2.8 times the base rate. And, weakly, *where*: low-priced, thinner names below their highs, which is a volatility tilt. Out-of-sample top-decile precision was 5.8% against a 4.5% base (1.29x), and at the top decile that is no better than the shuffled-label placebo.
- **News after the start.** This is most of it. A third of events had 300bp or more of cuts ahead of them. Another sixth were sector waves on dated shocks: war and the Hormuz closure for the 2026 refiners, rerating for the 2024 large caps.
- **Screen for the predictable part.** In an easing regime, take liquid names in the bottom 30% by price that are well below their 52-week high and have rising volume. Expect about 6 doublers per 100 flags (94% false positives), a median 6-month return below the market, and drawdowns of 40 to 50%. It does not pay as a strategy on its own. The regime signal is the piece worth testing as a timing rule. This test does not support fast rotation into big winners picked on start-of-move features.

## Caveats

- Survivorship is reduced, not removed: delisted names are on crude returns, and suspended names are carried at their last print.
- Cash dividends are complete only from Nov 2024.
- Fundamentals cover 108 to 129 names, from 2019 or 2022. EPS is basic, consolidation is unverified (lesson 1), and bonus issues distort EPS changes.
- Insider direction comes from the 22-symbol sample plus portal tags.
- Unusual-movement letters are mostly from 2021 onward.
- Sectors are the 2026 classification, held fixed.
- Month-end windows miss round trips within a month: ASL went +98% from low to peak in 2026 but never +100% month-end to month-end.
- There is no correction for testing 27 features.
