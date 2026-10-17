# Size and liquidity on PSX, 2017 to 2026

Script: `scripts/tests/size_liquidity.py`. Raw output: `tests/out/size_liquidity.txt`. Run 17 Oct 2026.

## Hypothesis
The equal-weight (EW) liquid basket made +44.1% (2017-01-02 to 2026-10-16) while KSE100 made +245.0%. Candidate causes: (a) dividends, (b) daily-rebalancing drag, (c) a large-cap premium, (d) the crude corporate-action fix, (e) a few mega-caps carrying the index.

## Data
Panel from `scripts/prices.py` (456 symbols, survivors only, raw prices, crude returns). Liquid = trailing 60-day median traded value above Rs5m (about 108 names a day on average). Size proxy = that same traded value, known the day before. It measures liquidity, not market cap. The repo has no share counts, so a true cap sort was not possible. Index returns are price-only closes from `data/macro`. KMI30 and KMI All membership: `data/index_members`. The KMI All lists are "derived" (rolled back from the 2026 list, survivor-biased, see `data/INDEX_DATA_NOTES.md`).

## Method
Monthly: universe fixed on the first trading day of each month, per-name compounded return over the month, EW across names. Buckets: rank by traded value, split into 3 or 5 groups, next-month EW return per group (118 months). Placebo: 200 random bucket assignments with the same sizes. Yearly: compounded monthly returns.

## Results

Index price returns, same window:

| Index | Cum | Per year |
|---|---|---|
| KSE100 | +245.0% | +13.5% |
| KMI30 | +192.4% | +11.6% |
| KMI All Share | +186.8% | +11.4% |

(b) Rebalancing, liquid names EW (measured):

| Method | Cum |
|---|---|
| Daily rebalanced (baseline) | +44.1% |
| Monthly rebalanced | +68.1% |
| Annual, held a year | +79.0% |
| Buy and hold, 122 names liquid Jan 2017 (median name +14.5%) | +86.6% mean |

Daily EW volatility drag is 3.4% a year (arithmetic minus log mean), about 24 points of the gap to monthly. Even the best EW variant is far below KSE100.

(c) Terciles by traded value, liquid universe (1 = least liquid):

| Bucket | Mean month | Median month | Months up | Cum | Per year | Name-months | Name median | Name win |
|---|---|---|---|---|---|---|---|---|
| 1 least liquid | +1.1% | -0.1% | 48.3% | +120% | +8.4% | 4,263 | -1.1% | 45.4% |
| 2 | +0.7% | -0.4% | 49.2% | +48% | +4.0% | 4,182 | -1.1% | 45.1% |
| 3 most liquid | +0.6% | -0.1% | 48.3% | +35% | +3.1% | 4,228 | -0.7% | 47.1% |

Top minus bottom: mean -0.45% a month (about -5.4% a year), t -1.2, top ahead in 44% of months. Placebo spread: mean -0.02%, 95% band -0.51% to +0.52%. The real spread is at or below only 4.0% of placebo draws. Quintiles: top +2.4% a year, bottom +11.2% a year, spread -0.72% a month, t -1.7, placebo percentile 1.5%. Wider universe (above Rs1m, about 162 names): spread -0.56% a month, t -1.9.

Yearly (terciles, compounded monthly; 2026 to 16 Oct):

| Year | Bottom | Middle | Top | Top minus bottom | EW all liquid | KSE100 |
|---|---|---|---|---|---|---|
| 2017 | -19.3% | -27.4% | -20.8% | -1.5% | -22.4% | -16.1% |
| 2018 | -8.4% | -7.9% | -16.7% | -8.3% | -10.9% | -9.0% |
| 2019 | -0.1% | -1.0% | -13.3% | -13.2% | -4.6% | +9.9% |
| 2020 | +39.7% | +29.4% | +42.9% | +3.2% | +37.6% | +7.4% |
| 2021 | -0.1% | -1.6% | -21.1% | -20.9% | -8.0% | +1.9% |
| 2022 | -31.3% | -31.2% | -23.9% | +7.4% | -28.8% | -9.4% |
| 2023 | +36.0% | +58.2% | +47.7% | +11.8% | +47.3% | +53.0% |
| 2024 | +103.5% | +53.9% | +84.3% | -19.1% | +80.4% | +78.0% |
| 2025 | +22.3% | +30.6% | +18.4% | -3.8% | +23.9% | +51.2% |
| 2026 | -8.1% | -20.0% | -14.4% | -6.4% | -14.2% | -4.4% |

Top beat bottom in 3 of 10 years (2 of 10 in the wider universe). Mean yearly spread -5.1%, median -5.1%. KSE100 beat the EW liquid basket in 8 of 10 years.

(d) Corporate-action fix: crude zeroes 434 moves since 2017 (60 up, 374 down). Only 1 up-move is in a liquid name: BML, +1,627% on 2026-02-02 (4.86 to 83.91), a consolidation, correctly zeroed. Restoring up-moves below +100% changes nothing (+44.1%). `data/corporate_actions.csv` does not exist, so true adjusted returns could not be run. A provisional total-return table (462 actions from `provisional_actions()`, unverified) gives +54.5%, about +10 points. That mixes dividends added back with 10% bonuses fixed, so it is not a clean dividend number. With no fix at all the basket shows +21.0%, because of fake crashes.

(e) KSE100 members from 2021-04 (lists start then):

| Series | Cum |
|---|---|
| KSE100 index | +274.6% |
| EW of members, monthly | +104.0% |
| Traded-value-weighted members | +63.4% |
| Same, excluding top 10 by traded value | +82.6% |

Traded value is a poor stand-in for index weight: it does not reproduce the index (+63% against +275%). The exclusion test is therefore inconclusive. The top 10 by traded value hold 56% of that weight and add 40 of 69 points on a simple-sum basis.

KMI30 EW against the liquid KMI All Share EW, monthly rebalanced, from 2020-07-13 (first KMI30 list):

| | Cum | Per year |
|---|---|---|
| EW KMI30 members (about 28 names) | +139.3% | +15.0% |
| EW liquid KMI All members (about 81 names) | +99.2% | +11.6% |
| KMI30 index, same window | +307.1% | |

KMI30 EW was ahead in 5 of 7 years (differences +2.9, -1.2, +6.5, +6.4, -21.3, +5.3, +11.5 points, 2020 to 2026); monthly diff +0.23%, t 0.9, not significant. EW with no liquidity filter on the derived KMI All lists gives +335%. Do not use that: the lists are rolled back from 2026 membership, so it is survivor-biased.

## Robustness
Results hold with 3 or 5 buckets and with a Rs1m or Rs5m floor. A random-bucket placebo is centred on zero. The reversed sign sits in the 1.5% to 4% tail, which is suggestive, not conclusive. There are 118 months but few independent regimes (2020, 2023 and 2024 supply most of the gain).

## Verdict
For a Rs50k-a-month retail investor, large liquid names did not beat small ones on PSX 2017 to 2026 inside the investable (above Rs5m) set. The most liquid third returned +3.1% a year against +8.4% for the least liquid third, a gap of about 5 points a year against the large side. The large side led in only 3 of 10 years. That is a weak effect (t about -1.2 to -1.9), not a proven small-cap premium. The sort is by traded value, not market cap, so a true mega-cap premium is untested.

Gap decomposition: dividends do not explain it (both indices are price-only); the basket also drops most dividends, and the provisional adjustment suggests about 10 points. Daily rebalancing costs about 24 points (44% to 68%); annual rebalancing or buy and hold gives 79% to 87%. The crude fix is not a cause for liquid names. Most of the rest (best EW case about +87% against +245%) is the index being cap-weighted toward large winners, which this test could not isolate. Practical reading: an equal-weight basket of many liquid names, rebalanced daily, badly lagged the index; the cap-weighted index did better than any equal-weight variant.

## Caveats
Survivors only, so every EW figure is flattered, the small-name bucket most. Traded value is not market cap. Crude returns drop large dividends and leave some 10% bonuses as fake losses. Corporate actions file absent. Bottom-bucket names have wider spreads and thinner fills than the price series implies; no costs were charged. KSE100 weights were approximated badly. 2026 is a partial year.
