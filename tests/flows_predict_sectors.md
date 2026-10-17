# Do investor flows predict sector returns?

Run 17 Oct 2026. Script `scripts/tests/flows_predict_sectors.py`, raw output `tests/out/flows_predict_sectors.txt`. The 60-day table has no eligible years (0/0), 120 formation dates at 20 days (insurance 118), 40 at 60 days. Tables are copied verbatim from that output.

## Hypothesis

NCCPL net flows by investor group, scaled by the sector's gross traded value, rank the next 20 and 60 trading days of sector excess returns across 9 PSX sectors. Pre-registered signs: FIPI +, mutual funds +, insurance +, banks/DFI + (H1, H2); individuals -, broker proprietary - (H3). Companies, nbfc, other organization are exploratory. The groups split one zero-sum flow, so H1 to H3 are not independent. H4: heavy foreign selling at market level marks bottoms.

## Data

- `data/macro/fipi_lipi_by_sector.csv`: 2,415 flow dates, 2017-01-02 to 2026-10-16, 9 groups, 9 of 11 sectors used. `fipi_lipi.csv`, `kse100.csv`, `kmiallshr.csv` for H4.
- `scripts/prices.py` panel: 2,480 dates x 456 symbols (names listed on 2026-10-16). Baskets use `liquid_universe(E, 5e6)`; sizes are in the basket table.
- Returns: `returns(method="crude")`, plus 0 on every (symbol, date) in `data/suspected_corporate_actions.csv`.

suspected_corporate_actions.csv rows used: 801
git state of data/suspected_corporate_actions.csv at run time: status 'clean', uncommitted diff 'none', last commit touching it: b1e0b42 Codex: index recomposition and calendar tests; practitioner signals rewrite; gap resolutions in all sector notes

## Method

- Basket = equal-weight buy-and-hold from the close on E to the close on E+h, members fixed at E, at least 2 names. A name drops only if it has no observation on E or none in the 5 rows ending at X. Excess return = basket minus the mean of the available baskets (not `ew_market`).
- Signal S = 20-flow-day net USD of group g in sector s divided by the 20-day buy USD of all 9 groups in that sector. T is the last flow date before E and entry is the close on E. A missing sector row on a date the group reports counts 0; at least 18 of 20 days required.
- Non-overlapping windows, h = 20 or 60 rows, first E with 20 full flow days (2017-01-30). Headline is offset 0, fixed before the run.
- Spread: long top 3 sectors by S (bottom 3 for individuals and broker prop) minus the mean of all sectors, net of 0.5% per period. Top3 minus bottom3 is gross only, not tradable for retail.
- Rank IC = Spearman across sectors (at least 6); momentum control = IC of the residual of rank(S) on rank(trailing 20-day excess return). t = mean / (sd / sqrt n).
- Placebo: 1,000 permutations (seed 0) of period labels, signal vector kept intact. Also run on the residual IC and the net spread.
- Clip: daily net clipped at 5x its past 250-day median absolute value. Sensitivity: `method="adjusted"` with `provisional_actions()`.

## Results

| sector | liquid names min | median | max | basket names (after data rule) min | median | max | sector-periods dropped (<2 names) |
|---|---|---|---|---|---|---|---|
| Cement | 6 | 10 | 16 | 6 | 10 | 16 | 0 |
| Banks | 8 | 11 | 17 | 8 | 10 | 17 | 0 |
| Fertilizer | 2 | 3 | 5 | 2 | 3 | 5 | 0 |
| Food | 2 | 7 | 16 | 2 | 7 | 16 | 0 |
| E&P | 3 | 3 | 3 | 3 | 3 | 3 | 0 |
| OMC | 3 | 5 | 8 | 3 | 5 | 8 | 0 |
| Power | 3 | 3 | 9 | 3 | 3 | 9 | 0 |
| Tech | 2 | 8 | 18 | 2 | 8 | 18 | 0 |
| Textile | 1 | 4 | 10 | 1 | 4 | 10 | 1 |
60-day periods: sector-periods dropped for <2 names: Cement 0, Banks 0, Fertilizer 0, Food 0, E&P 0, OMC 0, Power 0, Tech 0, Textile 1
20-day total dropped sector-periods: 1 of 1080

| group | flow dates missing for group | sector-day rows absent on dates the group reports (filled 0) |
|---|---|---|
| fipi | 0 | 2 |
| mutual funds | 0 | 127 |
| insurance companies | 27 | 1256 |
| banks / dfi | 0 | 1619 |
| individuals | 0 | 0 |
| broker proprietary trading | 0 | 0 |
| companies | 0 | 23 |
| nbfc | 4 | 8770 |
| other organization | 0 | 1523 |
provisional_actions rows (sensitivity run): 462

### Headline rank IC, 20-day

| group | sign | n periods | mean IC | median IC | t | win rate | worst IC | IC 2017-21 | IC 2022-26 | years w/ sign (eligible) | placebo p5 | p50 | p95 | actual pctile |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fipi | + | 120 | -0.001 | +0.000 | -0.03 | 49% | -0.867 | +0.047 | -0.051 | 5/10 | -0.056 | -0.004 | +0.047 | 53.5 |
| mutual funds | + | 120 | +0.028 | -0.017 | +0.90 | 47% | -0.733 | +0.044 | +0.012 | 7/10 | -0.063 | -0.002 | +0.053 | 80.1 |
| insurance companies | + | 118 | +0.045 | +0.042 | +1.34 | 55% | -0.850 | +0.015 | +0.076 | 7/10 | -0.046 | +0.008 | +0.060 | 89.1 |
| banks / dfi | + | 120 | -0.037 | -0.050 | -1.00 | 41% | -0.850 | +0.007 | -0.081 | 3/10 | -0.052 | +0.004 | +0.062 | 11.0 |
| individuals | - | 120 | +0.018 | +0.033 | +0.51 | 45% | +0.850 | -0.063 | +0.101 | 4/10 | -0.051 | +0.001 | +0.055 | 68.9 |
| broker proprietary trading | - | 120 | -0.035 | -0.025 | -1.13 | 52% | +0.767 | -0.042 | -0.029 | 5/10 | -0.053 | -0.002 | +0.050 | 14.1 |
| companies | expl. | 120 | +0.004 | -0.025 | +0.13 | 47% | -0.750 | +0.015 | -0.007 | 6/10 | -0.045 | +0.008 | +0.060 | 43.6 |
| nbfc | expl. | 119 | +0.071 | +0.067 | +2.32 | 58% | -0.667 | +0.014 | +0.130 | 7/10 | -0.043 | +0.008 | +0.061 | 97.7 |
| other organization | expl. | 120 | +0.004 | +0.000 | +0.13 | 48% | -0.817 | +0.018 | -0.010 | 5/10 | -0.052 | +0.000 | +0.056 | 55.3 |
win rate = share of periods with IC in the hypothesised direction (IC>0 for exploratory); worst = worst period IC in the hypothesised direction; years: calendar years with >=6 periods whose mean IC has the hypothesised sign.

### Headline rank IC, 60-day

| group | sign | n periods | mean IC | median IC | t | win rate | worst IC | IC 2017-21 | IC 2022-26 | years w/ sign (eligible) | placebo p5 | p50 | p95 | actual pctile |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fipi | + | 40 | -0.002 | +0.075 | -0.04 | 60% | -0.700 | +0.010 | -0.017 | 0/0 | -0.089 | -0.002 | +0.092 | 49.3 |
| mutual funds | + | 40 | +0.037 | +0.049 | +0.66 | 55% | -0.683 | +0.018 | +0.058 | 0/0 | -0.094 | +0.009 | +0.098 | 69.1 |
| insurance companies | + | 39 | +0.014 | +0.117 | +0.20 | 51% | -0.883 | -0.066 | +0.098 | 0/0 | -0.081 | +0.013 | +0.113 | 50.8 |
| banks / dfi | + | 40 | -0.053 | -0.083 | -0.87 | 40% | -0.733 | -0.037 | -0.071 | 0/0 | -0.090 | +0.001 | +0.090 | 16.3 |
| individuals | - | 40 | -0.018 | -0.025 | -0.32 | 55% | +0.767 | -0.068 | +0.037 | 0/0 | -0.100 | -0.007 | +0.084 | 39.7 |
| broker proprietary trading | - | 40 | +0.006 | +0.050 | +0.10 | 45% | +0.883 | -0.016 | +0.029 | 0/0 | -0.076 | +0.012 | +0.104 | 44.9 |
| companies | expl. | 40 | +0.101 | +0.050 | +1.70 | 52% | -0.533 | +0.147 | +0.050 | 0/0 | -0.094 | -0.007 | +0.096 | 95.6 |
| nbfc | expl. | 40 | +0.052 | +0.100 | +0.96 | 60% | -0.933 | +0.065 | +0.038 | 0/0 | -0.069 | +0.021 | +0.106 | 70.1 |
| other organization | expl. | 40 | -0.053 | -0.083 | -0.89 | 40% | -0.783 | -0.102 | +0.000 | 0/0 | -0.087 | +0.003 | +0.101 | 15.4 |

### Momentum-residual IC, 20-day

| group | sign | n | raw mean IC | residual mean IC | residual t | placebo p5 | p50 | p95 | residual actual pctile | avg rank corr of S with trailing 20d excess return |
|---|---|---|---|---|---|---|---|---|---|---|
| fipi | + | 120 | -0.001 | +0.002 | +0.07 | -0.056 | -0.002 | +0.049 | 56.2 | +0.033 |
| mutual funds | + | 120 | +0.028 | +0.031 | +0.99 | -0.063 | -0.002 | +0.052 | 83.2 | +0.176 |
| insurance companies | + | 118 | +0.045 | +0.044 | +1.33 | -0.045 | +0.008 | +0.059 | 87.6 | -0.061 |
| banks / dfi | + | 120 | -0.037 | -0.034 | -0.96 | -0.049 | +0.005 | +0.062 | 11.1 | -0.119 |
| individuals | - | 120 | +0.018 | +0.002 | +0.07 | -0.054 | +0.000 | +0.053 | 52.4 | -0.128 |
| broker proprietary trading | - | 120 | -0.035 | -0.030 | -0.97 | -0.056 | -0.004 | +0.046 | 21.0 | +0.047 |
| companies | expl. | 120 | +0.004 | +0.019 | +0.57 | -0.046 | +0.007 | +0.058 | 63.5 | +0.026 |
| nbfc | expl. | 119 | +0.071 | +0.057 | +1.75 | -0.047 | +0.008 | +0.062 | 94.0 | -0.011 |
| other organization | expl. | 120 | +0.004 | +0.012 | +0.38 | -0.051 | +0.001 | +0.057 | 63.7 | -0.047 |

### Top-3 long-only spread, 20-day

| group (leg chosen) | n | gross mean | gross median | gross win | gross worst | net mean | net median | net win | net worst | top3 minus bottom3 gross mean (not tradable) | L-S gross median | pick runs total/len>=2/longest |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fipi | 120 | +0.2% | +0.3% | 54% | -8.1% | -0.3% | -0.2% | 45% | -8.6% | +0.3% | +0.3% | 191/72/13 |
| mutual funds | 120 | +0.1% | +0.3% | 52% | -6.9% | -0.4% | -0.2% | 43% | -7.4% | +0.5% | +0.5% | 204/83/10 |
| insurance companies | 118 | +0.2% | +0.2% | 54% | -10.5% | -0.3% | -0.3% | 46% | -11.0% | +0.3% | -0.0% | 201/69/14 |
| banks / dfi | 120 | -0.3% | -0.4% | 46% | -10.7% | -0.8% | -0.9% | 41% | -11.2% | -0.5% | -1.5% | 199/84/8 |
| individuals (bottom 3) | 120 | +0.3% | +0.1% | 54% | -7.6% | -0.2% | -0.4% | 48% | -8.1% | +0.4% | -0.2% | 207/89/7 |
| broker proprietary trading (bottom 3) | 120 | +0.3% | +0.2% | 57% | -7.3% | -0.2% | -0.3% | 44% | -7.8% | +0.6% | +0.3% | 262/69/6 |
| companies (top 3) | 120 | -0.1% | -0.2% | 47% | -7.9% | -0.6% | -0.7% | 41% | -8.4% | -0.1% | -0.4% | 209/75/9 |
| nbfc (top 3) | 119 | +0.4% | -0.0% | 50% | -6.2% | -0.1% | -0.5% | 42% | -6.7% | +1.1% | +0.4% | 219/74/11 |
| other organization (top 3) | 120 | +0.1% | -0.1% | 48% | -11.1% | -0.4% | -0.6% | 40% | -11.6% | +0.1% | +0.2% | 186/88/11 |
net = gross minus 0.5% round trip charged once per period on the long leg; contrarian series (individuals, broker prop) pick the bottom 3 by S.

| group | actual net mean | placebo p5 | p50 | p95 | actual pctile |
|---|---|---|---|---|---|
| fipi | -0.32% | -0.91% | -0.45% | -0.00% | 67.8 |
| mutual funds | -0.36% | -1.00% | -0.51% | -0.04% | 69.8 |
| insurance companies | -0.27% | -0.93% | -0.48% | +0.00% | 78.5 |
| banks / dfi | -0.78% | -0.99% | -0.49% | +0.00% | 14.5 |
| individuals | -0.17% | -0.94% | -0.49% | -0.00% | 86.3 |
| broker proprietary trading | -0.23% | -0.97% | -0.51% | -0.07% | 85.6 |
| companies | -0.65% | -0.94% | -0.48% | -0.06% | 27.2 |
| nbfc | -0.08% | -0.93% | -0.48% | -0.04% | 92.2 |
| other organization | -0.44% | -0.97% | -0.52% | -0.06% | 60.7 |

### By-year mean IC, 20-day

| group | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| fipi | -0.11 (12) | -0.09 (12) | +0.07 (13) | +0.23 (12) | +0.13 (12) | +0.02 (13) | -0.07 (12) | -0.12 (12) | -0.16 (13) | +0.13 (9) |
| mutual funds | +0.12 (12) | +0.00 (12) | +0.02 (13) | +0.07 (12) | +0.01 (12) | +0.16 (13) | -0.03 (12) | -0.04 (12) | -0.04 (13) | +0.01 (9) |
| insurance companies | +0.20 (10) | +0.06 (12) | -0.02 (13) | -0.16 (12) | +0.03 (12) | -0.01 (13) | +0.11 (12) | +0.08 (12) | +0.08 (13) | +0.15 (9) |
| banks / dfi | -0.02 (12) | +0.10 (12) | +0.05 (13) | -0.04 (12) | -0.06 (12) | -0.10 (13) | -0.08 (12) | -0.10 (12) | +0.03 (13) | -0.19 (9) |
| individuals | -0.11 (12) | +0.14 (12) | -0.11 (13) | -0.18 (12) | -0.05 (12) | +0.19 (13) | +0.05 (12) | +0.01 (12) | +0.09 (13) | +0.18 (9) |
| broker proprietary trading | -0.17 (12) | -0.05 (12) | -0.08 (13) | +0.07 (12) | +0.03 (12) | -0.20 (13) | +0.04 (12) | -0.14 (12) | +0.06 (13) | +0.14 (9) |

### Signal overlap

|  | fipi | mutual funds | insurance companies | banks / dfi | individuals | broker proprietary trading | companies | nbfc | other organization |
|---|---|---|---|---|---|---|---|---|---|
| fipi | +1.00 | -0.22 | -0.19 | -0.24 | -0.18 | -0.13 | -0.21 | -0.11 | -0.23 |
| mutual funds | -0.22 | +1.00 | -0.09 | -0.11 | -0.24 | +0.00 | -0.04 | +0.06 | +0.00 |
| insurance companies | -0.19 | -0.09 | +1.00 | -0.04 | -0.12 | -0.09 | -0.08 | -0.01 | +0.03 |
| banks / dfi | -0.24 | -0.11 | -0.04 | +1.00 | -0.03 | +0.02 | -0.02 | +0.04 | +0.06 |
| individuals | -0.18 | -0.24 | -0.12 | -0.03 | +1.00 | +0.03 | -0.09 | +0.03 | +0.04 |
| broker proprietary trading | -0.13 | +0.00 | -0.09 | +0.02 | +0.03 | +1.00 | -0.06 | +0.05 | -0.00 |
| companies | -0.21 | -0.04 | -0.08 | -0.02 | -0.09 | -0.06 | +1.00 | -0.00 | +0.01 |
| nbfc | -0.11 | +0.06 | -0.01 | +0.04 | +0.03 | +0.05 | -0.00 | +1.00 | +0.08 |
| other organization | -0.23 | +0.00 | +0.03 | +0.06 | +0.04 | -0.00 | +0.01 | +0.08 | +1.00 |
fipi vs individuals: -0.18
fipi vs mutual funds: -0.22
fipi vs banks / dfi: -0.24
fipi vs broker proprietary trading: -0.13

### H4: foreign selling at market bottoms

fipi_lipi.csv: 2413 flow dates, 2017-01-02 to 2026-10-16; scaled 60-day FIPI net / gross buy, first valid 2017-03-27
KSE100 rows 2480, 2016-10-17 to 2026-10-16; KMI All Share rows 2473, KSE100 dates missing from KMI series (forward-filled): 7
first possible trigger date 2018-03-30; trigger days 155

| trigger date T | entry E (close) | scaled signal | KSE100 fwd 60d | KSE100 fwd 120d | KMI All Share fwd 60d | KMI fwd 120d | KSE100 worst drawdown within 120d | marked bottom (KSE100 min within 20 rows of E) |
|---|---|---|---|---|---|---|---|---|
| 2018-05-25 | 2018-05-28 | -0.0159 | -0.7% | -3.0% | -2.8% | -5.7% | -13.0% | no |
| 2020-04-07 | 2020-04-08 | -0.0389 | +15.3% | +29.4% | +20.2% | +34.3% | +0.0% | yes |
trigger clusters (episode first trigger -> last trigger in the same cluster, trigger days): 2018-05-25 -> 2018-12-26, 100 days; 2020-04-07 -> 2020-06-29, 55 days
episodes: 2. Where the rule fires: 2017-2019: 2018-05-25; 2021-2022: none

| series | sample | n | mean | median | win rate | worst |
|---|---|---|---|---|---|---|
| KSE100 fwd 60d | episodes | 2 | +7.3% | +7.3% | 50% | -0.7% |
| KSE100 fwd 60d | all non-overlapping 60-day windows, eligible period | 35 | +4.5% | +1.8% | 60% | -16.7% |
| KSE100 fwd 120d | episodes | 2 | +13.2% | +13.2% | 50% | -3.0% |
| KSE100 fwd 120d | all non-overlapping 120-day windows, eligible period | 17 | +9.9% | +9.2% | 65% | -17.4% |
| KMI All Share fwd 60d | episodes | 2 | +8.7% | +8.7% | 50% | -2.8% |
| KMI All Share fwd 60d | all non-overlapping 60-day windows, eligible period | 35 | +3.8% | +2.1% | 60% | -16.1% |
| KMI All Share fwd 120d | episodes | 2 | +14.3% | +14.3% | 50% | -5.7% |
| KMI All Share fwd 120d | all non-overlapping 120-day windows, eligible period | 17 | +8.3% | +8.3% | 65% | -20.1% |

random-entry placebo: 1000 draws of 2 entry dates (no replacement) from E rows 2018-04-02 to 2026-04-21 (full 120-day forward window), seed 0
| statistic | episodes (actual) | placebo p5 | p50 | p95 | actual pctile |
|---|---|---|---|---|---|
| KSE100 median fwd 60d | +7.3% | -7.5% | +4.7% | +20.0% | 60.1 |
| KSE100 median fwd 120d | +13.2% | -8.1% | +10.4% | +33.1% | 58.8 |
| KMI median fwd 60d | +8.7% | -8.0% | +3.7% | +19.5% | 69.6 |
| KMI median fwd 120d | +14.3% | -9.4% | +8.8% | +30.7% | 68.4 |
| bottom-hit rate (KSE100) | 50% | 0% | 0% | 50% | 98.3 |
bottom-hit rate among eligible entry rows (all rows): 14%
H4 verdict: 2 episodes; fewer than 5 episodes: ANECDOTE whatever the numbers say.

## Robustness

20d periods per offset: 0:120, 1:120, 2:120, 3:120, 4:120, 5:120, 6:119, 7:119, 8:119, 9:119, 10:119, 11:119, 12:119, 13:119, 14:119, 15:119, 16:119, 17:119, 18:119, 19:119
60d periods per offset: 0:40, 20:39, 40:39
| horizon | group | sign | offsets | min mean IC | median | max | offsets with hypothesised sign |
|---|---|---|---|---|---|---|---|
| 20d | fipi | + | 20 | -0.036 | +0.003 | +0.040 | 11/20 |
| 20d | mutual funds | + | 20 | -0.005 | +0.032 | +0.085 | 19/20 |
| 20d | insurance companies | + | 20 | -0.030 | +0.007 | +0.045 | 14/20 |
| 20d | banks / dfi | + | 20 | -0.085 | -0.053 | -0.026 | 0/20 |
| 20d | individuals | - | 20 | -0.022 | +0.002 | +0.033 | 9/20 |
| 20d | broker proprietary trading | - | 20 | -0.052 | +0.007 | +0.082 | 8/20 |
| 20d | companies | expl. | 20 | -0.007 | +0.026 | +0.067 | 19/20 |
| 20d | nbfc | expl. | 20 | +0.012 | +0.040 | +0.071 | 20/20 |
| 20d | other organization | expl. | 20 | -0.027 | -0.010 | +0.018 | 7/20 |
| 60d | fipi | + | 3 | -0.036 | -0.006 | -0.002 | 0/3 |
| 60d | mutual funds | + | 3 | +0.029 | +0.035 | +0.037 | 3/3 |
| 60d | insurance companies | + | 3 | -0.099 | +0.014 | +0.017 | 2/3 |
| 60d | banks / dfi | + | 3 | -0.053 | -0.048 | +0.062 | 1/3 |
| 60d | individuals | - | 3 | -0.040 | -0.018 | +0.007 | 2/3 |
| 60d | broker proprietary trading | - | 3 | +0.006 | +0.019 | +0.046 | 0/3 |
| 60d | companies | expl. | 3 | -0.021 | +0.101 | +0.110 | 2/3 |
| 60d | nbfc | expl. | 3 | +0.052 | +0.097 | +0.098 | 3/3 |
| 60d | other organization | expl. | 3 | -0.053 | -0.033 | -0.008 | 0/3 |

| horizon | group | sign | headline mean IC | t | adjusted mean IC | t | adjusted vs headline | label | clipped mean IC | t | clip vs headline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20d | fipi | + | -0.001 | -0.03 | -0.002 | -0.06 | same sign | ok | +0.003 | +0.10 | SIGN FLIP |
| 20d | mutual funds | + | +0.028 | +0.90 | +0.032 | +1.01 | same sign | ok | +0.027 | +0.87 | same sign |
| 20d | insurance companies | + | +0.045 | +1.34 | +0.039 | +1.15 | same sign | ok | +0.033 | +0.92 | same sign |
| 20d | banks / dfi | + | -0.037 | -1.00 | -0.045 | -1.22 | same sign | ok | -0.043 | -1.16 | same sign |
| 20d | individuals | - | +0.018 | +0.51 | +0.025 | +0.73 | same sign | ok | +0.005 | +0.15 | same sign |
| 20d | broker proprietary trading | - | -0.035 | -1.13 | -0.029 | -0.92 | same sign | ok | -0.028 | -0.94 | same sign |
| 20d | companies | expl. | +0.004 | +0.13 | +0.002 | +0.05 | same sign | ok | -0.019 | -0.57 | SIGN FLIP |
| 20d | nbfc | expl. | +0.071 | +2.32 | +0.073 | +2.37 | same sign | ok | +0.049 | +1.49 | same sign |
| 20d | other organization | expl. | +0.004 | +0.13 | +0.002 | +0.06 | same sign | ok | -0.017 | -0.46 | SIGN FLIP |
| 60d | fipi | + | -0.002 | -0.04 | -0.005 | -0.08 | same sign | ok | +0.022 | +0.43 | SIGN FLIP |
| 60d | mutual funds | + | +0.037 | +0.66 | +0.028 | +0.50 | same sign | ok | +0.023 | +0.40 | same sign |
| 60d | insurance companies | + | +0.014 | +0.20 | +0.017 | +0.24 | same sign | ok | -0.035 | -0.54 | SIGN FLIP |
| 60d | banks / dfi | + | -0.053 | -0.87 | -0.057 | -0.91 | same sign | ok | -0.061 | -1.01 | same sign |
| 60d | individuals | - | -0.018 | -0.32 | -0.022 | -0.39 | same sign | ok | -0.040 | -0.69 | same sign |
| 60d | broker proprietary trading | - | +0.006 | +0.10 | -0.001 | -0.01 | SIGN FLIP | UNRESOLVED (needs data/corporate_actions.csv) | +0.013 | +0.24 | same sign |
| 60d | companies | expl. | +0.101 | +1.70 | +0.103 | +1.72 | same sign | ok | +0.066 | +1.15 | same sign |
| 60d | nbfc | expl. | +0.052 | +0.96 | +0.044 | +0.83 | same sign | ok | +0.056 | +1.00 | same sign |
| 60d | other organization | expl. | -0.053 | -0.89 | -0.055 | -0.91 | same sign | ok | -0.079 | -1.22 | same sign |

No 20-day series flips sign under the corporate-action sensitivity. The clip flips FIPI at 20 days (-0.001 to +0.003), which is noise around zero. Only broker prop at 60 days is labelled unresolved. Across offsets banks/DFI has the hypothesised sign in 0 of 20, mutual funds in 19 of 20 (median +0.032), FIPI in 11 of 20. The exploratory nbfc series is positive at all 20 offsets, and offset 0 (+0.071) is its maximum, so its headline t of 2.32 is the best case.

## Verdict

| group | sign | (a) sign and t>=2 | (b) beyond placebo 95th | (c) halves and >=6 yrs | (d) net spread median>0, win>50% | (e) residual keeps sign, >=half | (f) sign holds under adj + clip | (g) 60d same sign | verdict |
|---|---|---|---|---|---|---|---|---|---|
| fipi | + | fail | fail | fail | fail | pass | fail | fail | no |
| mutual funds | + | fail | fail | pass | fail | pass | pass | pass | no |
| insurance companies | + | fail | fail | pass | fail | pass | pass | pass | no |
| banks / dfi | + | fail | fail | fail | fail | fail | pass | fail | no |
| individuals | - | fail | fail | fail | fail | fail | pass | pass | no |
| broker proprietary trading | - | fail | fail | fail | fail | pass | pass | fail | no |
| companies | expl. | - | - | - | - | - | - | - | exploratory: cannot enter the watch |
| nbfc | expl. | - | - | - | - | - | - | - | exploratory: cannot enter the watch |
| other organization | expl. | - | - | - | - | - | - | - | exploratory: cannot enter the watch |
final weekly-watch list: none
Multiple testing: 9 series x 2 horizons (x IC and spread statistics): 1 to 2 false passes at 5% are expected by chance alone.

**Fails.** No pre-registered series passes (a) to (c). The weekly watch is empty and no mirrored pair needed collapsing. The best series, insurance, has mean IC +0.045, t +1.34, placebo percentile 89.1; FIPI is -0.001. Individuals has the wrong sign (+0.018). Broker prop has the right sign (-0.035) but t -1.13 and percentile 14.1 (rule needs 5 or below). All nine net top-3 spreads are negative (-0.78% to -0.08%) and no net win rate exceeds 48%. The only nominal pass of (a) and (b) is exploratory nbfc (t +2.32, percentile 97.7), which cannot enter the watch, drops to t +1.49 with the clip, and is within the 1 to 2 false passes expected from 9 series x 2 horizons. Residual ICs are within 0.02 of raw, so sector momentum is not hiding anything.

For the strategy: NCCPL group flows are not a sector-rotation signal here. Do not use FIPI selling or retail buying as a sector call. The signals are only weakly related (fipi vs individuals -0.18, mutual funds -0.22, banks/DFI -0.24, broker prop -0.13), and all are empty. H4 is an anecdote with 2 episodes: 2018 (trigger cluster to 2018-12-26, no bottom, -13.0% drawdown) and April 2020 (bottom). The rule did not fire in 2021-2022; 2017 and 2019 had no trigger.

## Caveats

- Survivorship and classification: today's sectorName for all years; only names listed on 2026-10-16 (ENGRO missing), while NCCPL flows include delisted names. Fertilizer baskets have 2 to 5 names, E&P exactly 3.
- Price only: high payers (E&P, Fertilizer, Power, Banks) understated; no yield added back (lesson 19). Sub-threshold bonus drops (5 to 9%) remain and are weakly diluted in 2 to 3 name baskets.
- Nine sectors (8 in some periods) make each IC noisy; worst periods near -0.9 and +0.9. Flows are in USD.
- Gaps: insurance starts 2017-02-08; nbfc has 4 flow dates missing and most sector rows absent (0).
- The suspect-log file was uncommitted when the task was set and is committed in `b1e0b42` (first block).
- 9 series x 2 horizons: 1 to 2 nominal passes expected by chance.
- Not computed: dividend-adjusted returns, anything using `data/corporate_actions.csv` (absent).
