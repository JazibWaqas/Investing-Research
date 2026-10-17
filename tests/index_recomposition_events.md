# Index recomposition events, 17 October 2026

## Hypothesis

Additions outperform the liquid equal-weight (EW) market after a public announcement, deletions underperform, and an inclusion pop may reverse. A pre-announcement move is anticipation, not a trade triggered by the notice.

## Data

`data/index_changes.csv`, 1,301 rows, 1,214 eligible after excluding 36 `derived` rows and 51 other rows with incomplete or missing dates. Raw OHLCV from `data/prices_raw` and `seed/data/prices`, through 16 October 2026, yields 456 usable symbols and 617 measured announcement-to-effective stock events. KSE100 is not the benchmark for this stock test. See [index data notes](../data/INDEX_DATA_NOTES.md). The script and [full output](out/index_recomposition_events.txt) include every measured event and neutralized gap.

## Method

Prior 20 trading days end before announcement (PRE). Announcement-to-effective (ANN) starts on the next trading day after the announcement and includes the effective close. Effective day (EFF) is reported separately. POST is the next 20 trading days. Each stock return is compounded and divided by compounded daily EW returns. EW includes names whose *prior* 60-session median close times volume exceeds Rs5m. A prior close above Rs10 followed by an absolute daily move above 10.5% is treated as a corporate action: zero that day's return and log it. There are 466 such gaps. The placebo draws 20 random symbol-date windows per event in the same year, within a factor of two of prior traded value. Returns below are excess percentages; win means excess above zero. ANN and EFF overlap, so do not sum them. A round trip costs 0.5%.

## Results

`n/ep` is stock events and distinct index notices. `Pbo` is mean matched placebo. All other columns are percentages.

| Index | Side | Phase | n/ep | Mean | Median | Win | Worst | Pbo |
|---|---|---|---:|---:|---:|---:|---:|---:|
| FTSE_PK | add | ANN | 5/1 | 0.49 | 0.10 | 60.00 | -1.79 | 0.26 |
| FTSE_PK | add | PRE | 5/1 | 2.15 | 2.73 | 60.00 | -4.76 | 0.54 |
| FTSE_PK | add | EFF | 5/1 | 0.81 | 0.09 | 60.00 | -0.72 | 0.14 |
| FTSE_PK | add | POST | 5/1 | -2.58 | -6.42 | 20.00 | -9.53 | -0.84 |
| KMI30 | add | ANN | 60/13 | 1.88 | 0.98 | 60.00 | -15.77 | -0.19 |
| KMI30 | add | PRE | 60/13 | -0.41 | -1.95 | 43.33 | -18.92 | -0.23 |
| KMI30 | add | EFF | 60/13 | 0.13 | 0.04 | 51.67 | -5.10 | 0.03 |
| KMI30 | add | POST | 60/13 | -1.73 | -3.01 | 35.00 | -21.72 | -0.35 |
| KMI30 | delete | ANN | 56/13 | 1.33 | -1.89 | 37.50 | -14.41 | -0.32 |
| KMI30 | delete | PRE | 56/13 | 1.32 | -1.00 | 41.07 | -16.32 | -0.72 |
| KMI30 | delete | EFF | 56/13 | 0.62 | 0.19 | 53.57 | -4.90 | 0.03 |
| KMI30 | delete | POST | 55/13 | -2.63 | -3.15 | 30.91 | -15.07 | -0.08 |
| KMI_ALL | add | ANN | 152/17 | 0.07 | -0.53 | 45.39 | -23.95 | 0.21 |
| KMI_ALL | add | PRE | 144/17 | 2.88 | -0.11 | 48.61 | -26.80 | 0.97 |
| KMI_ALL | add | EFF | 152/17 | -0.10 | -0.38 | 44.08 | -9.88 | 0.00 |
| KMI_ALL | add | POST | 148/17 | 1.99 | -1.64 | 41.89 | -37.55 | 0.75 |
| KMI_ALL | delete | ANN | 105/16 | 0.79 | -0.19 | 47.62 | -11.07 | -0.01 |
| KMI_ALL | delete | PRE | 103/16 | 0.06 | -0.29 | 48.54 | -19.57 | 1.29 |
| KMI_ALL | delete | EFF | 107/16 | 0.51 | 0.06 | 54.21 | -5.56 | 0.03 |
| KMI_ALL | delete | POST | 105/16 | -1.49 | -3.04 | 34.29 | -18.29 | 1.06 |
| KSE100 | add | ANN | 24/7 | 0.64 | 0.57 | 50.00 | -15.20 | -0.50 |
| KSE100 | add | PRE | 24/7 | -1.12 | -4.96 | 29.17 | -24.30 | 0.10 |
| KSE100 | add | EFF | 24/7 | 0.32 | -0.01 | 50.00 | -3.62 | -0.12 |
| KSE100 | add | POST | 24/7 | -1.62 | -2.57 | 45.83 | -19.08 | 0.32 |
| KSE100 | delete | ANN | 20/8 | 0.95 | 0.32 | 50.00 | -9.33 | 0.70 |
| KSE100 | delete | PRE | 20/8 | -6.59 | -6.74 | 15.00 | -40.41 | -0.22 |
| KSE100 | delete | EFF | 20/8 | 0.41 | 0.18 | 65.00 | -5.72 | -0.05 |
| KSE100 | delete | POST | 20/8 | -0.77 | -3.91 | 40.00 | -37.37 | 0.97 |
| KSE30 | add | ANN | 44/11 | 0.51 | -1.16 | 43.18 | -13.54 | 1.20 |
| KSE30 | add | PRE | 44/11 | 0.72 | -2.84 | 36.36 | -23.06 | 0.06 |
| KSE30 | add | EFF | 44/11 | 0.86 | 0.51 | 59.09 | -2.36 | 0.04 |
| KSE30 | add | POST | 44/11 | 1.02 | -0.04 | 50.00 | -23.41 | 0.25 |
| KSE30 | delete | ANN | 45/11 | -0.07 | -0.81 | 40.00 | -16.28 | 0.78 |
| KSE30 | delete | PRE | 45/11 | 0.52 | -1.24 | 44.44 | -16.14 | 0.42 |
| KSE30 | delete | EFF | 45/11 | -0.06 | -0.13 | 48.89 | -4.47 | -0.00 |
| KSE30 | delete | POST | 45/11 | -1.01 | -0.58 | 42.22 | -18.62 | 0.20 |
| MSCI_PK | add | ANN | 22/9 | -4.93 | -4.72 | 22.73 | -15.09 | 0.09 |
| MSCI_PK | add | PRE | 22/9 | 4.98 | 5.10 | 81.82 | -15.95 | 0.26 |
| MSCI_PK | add | EFF | 22/9 | -0.97 | -0.92 | 18.18 | -5.75 | -0.07 |
| MSCI_PK | add | POST | 22/9 | 1.05 | 0.20 | 54.55 | -11.09 | -0.13 |
| MSCI_PK | delete | ANN | 6/5 | 5.48 | 5.84 | 100.00 | 0.23 | -0.08 |
| MSCI_PK | delete | PRE | 6/5 | -5.82 | -6.19 | 16.67 | -16.39 | -2.15 |
| MSCI_PK | delete | EFF | 6/5 | -1.03 | -1.20 | 33.33 | -2.46 | -0.25 |
| MSCI_PK | delete | POST | 6/5 | -1.65 | -1.72 | 33.33 | -10.16 | -0.57 |
| MSCI_PK_SC | add | ANN | 55/12 | -0.89 | -0.74 | 43.64 | -25.84 | 0.65 |
| MSCI_PK_SC | add | PRE | 54/12 | 2.30 | -2.60 | 42.59 | -16.39 | -0.38 |
| MSCI_PK_SC | add | EFF | 55/12 | -0.11 | -0.12 | 45.45 | -5.09 | -0.05 |
| MSCI_PK_SC | add | POST | 55/12 | -1.41 | -3.04 | 30.91 | -28.02 | 0.43 |
| MSCI_PK_SC | delete | ANN | 23/11 | -2.52 | -3.00 | 26.09 | -13.86 | -0.17 |
| MSCI_PK_SC | delete | PRE | 23/11 | 0.94 | 3.12 | 56.52 | -22.77 | -0.05 |
| MSCI_PK_SC | delete | EFF | 23/11 | -0.06 | -0.29 | 39.13 | -5.75 | 0.06 |
| MSCI_PK_SC | delete | POST | 23/11 | -1.63 | -4.41 | 26.09 | -13.96 | -0.40 |

## Robustness

Equal weighting the notices rather than stocks gives ANN addition mean -0.04%, median 0.14%, 51.43% positive across 70 add-bearing notices. POST deletions average -1.39%, median -1.48%, 35.94% positive across 64 delete-bearing notices. Restricting to prior Rs5m-plus stock liquidity gives ANN additions n=294, mean 0.33%, median -0.38%, versus 0.24% placebo. The apparent broad addition effect vanishes. KMI30 additions remain the strongest *post-notice* cell (ANN n=60, 13 notices, mean 1.88%, median 0.98%, 60% positive, -15.77% worst, -0.19% placebo), but its 1.38% mean after cost is too thin against downside and notice clustering.

## Verdict

No dependable recomposition trade after 0.5% cost. MSCI Pakistan additions show a 4.98% PRE excess and -4.93% ANN excess, consistent with anticipation followed by reversal, not a post-announcement buy. KSE100 deletion underperformance is also mostly PRE (-6.59%). The pooled EFF addition mean is only 0.05% per notice, so there is no broad inclusion-day pop. POST deletions average -1.39% per notice, a hypothetical short gains 0.89% after cost, but shortability is limited. MSCI Pakistan deletion longs show +5.48% ANN from only six stocks in five notices. KMI30 additions merit forward tracking, not an automatic order.

## Caveats

Price-gap zeroing is not a verified split, bonus, or cash-dividend adjustment. It can erase a genuine unusual move and does not reconstruct total returns. The index dataset misses older notices, MSCI coverage is patchy, FTSE has one notice, and some KMI All Share membership lists were reconstructed. Renames (BYCO/CNERGY, ENGRO/ENGROH, ICI/LCI) and an uncertain AGL mapping can lose events. Missing stock prices and incomplete 20-day windows are excluded, so results retain survivorship and coverage bias. Announcement timestamps are unavailable, hence next-day entry is deliberately conservative. Market impact, short-borrow cost, and taxes are beyond the 0.5% round trip.
