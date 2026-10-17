# Sector sensitivity to Brent, coal, urea, cotton, palm oil, PKR and KSE100

Run 17 Oct 2026, method `crude` (rerun with `--method adjusted` once `data/corporate_actions.csv` exists). Script `scripts/tests/commodity_pkr_sensitivity.py`; raw output `tests/out/commodity_pkr_sensitivity.txt`; map `tests/out/sensitivity_map.csv`. All numbers come from that output.

## Hypothesis

- **H1** (prior +): after Brent's 3-month rise is 20% or more, refiners and E&P each beat the market over the next 1, 2 and 3 months.
- **H2** (prior +): after a PKR devaluation, exporters (textiles, tech) beat importers (autos, pharma) over 20 and 60 trading days.
- **H3** (descriptive): sector excess-return betas on each factor, contemporaneous and 1-3 month leads. Twelve sign cells are pre-registered; every other cell is exploratory.

## Data

- Prices: `prices.py` panel, 456 symbols, 2016-10-17 to 2026-10-16, method `crude`; 801 suspect-flagged stock-days drive member-window drops. Sectors from `data/symbols.csv` (today's classification).
- Factors: `data/macro/` brent (to 2026-10-14), usdpkr (to 2026-09-30, so no October PKR signal), kse100 close; Pink Sheet monthly averages coal_rb, urea, cotton, palm_oil. Palm 2026-01 and urea 2022-03 changes set to NaN. Richards Bay coal has World Bank estimates for some 2022-24 months.
- Sample: factor months 2017-01 to 2026-09 (117); 116 monthly basket windows; market = all of `liquid_universe(F)`.

| basket | months with basket | median liquid n | min | dropped: flag / gap>5 / no obs |
|---|---|---|---|---|
| E&P | 116 | 3 | 3 | 3 / 0 / 0 |
| Refinery | 116 | 4 | 2 | 2 / 0 / 0 |
| OMC (ex SNGP, SSGC) | 106 | 3 | 1 | 5 / 0 / 0 |
| Gas utilities | 102 | 2 | 1 | 2 / 0 / 0 |
| Fertilizer | 116 | 3 | 2 | 0 / 0 / 0 |
| Cement | 116 | 10 | 6 | 3 / 1 / 0 |
| Power | 115 | 3 | 3 | 13 / 0 / 0 |
| Autos | 116 | 8 | 2 | 15 / 0 / 0 |
| Pharma | 112 | 4 | 1 | 6 / 0 / 0 |
| Textiles | 115 | 4 | 1 | 2 / 0 / 0 |
| Tech | 116 | 8 | 2 | 6 / 0 / 0 |
| Chemicals | 116 | 6 | 2 | 10 / 0 / 0 |
| Food | 116 | 7 | 2 | 8 / 0 / 0 |
| Banks | 116 | 10 | 7 | 14 / 0 / 0 |
| Steel/engineering | 116 | 7 | 3 | 2 / 0 / 0 |
| Glass/packaging | 100 | 5 | 0 | 10 / 0 / 0 |
| Exporters (textiles+tech) | 116 | 12 | 3 | 8 / 0 / 0 |
| Importers (autos+pharma) | 116 | 12 | 4 | 21 / 0 / 0 |

E&P (3 names), refinery (median 4), fertilizer and gas utilities are close to single-stock bets.

## Method

- Formation: Brent, PKR and KSE100 signals for month t trade at the first PSX day of t+1; Pink Sheet at the 5th PSX day of t+1 (release timing assumed). Pre-2017-02 events are dropped, never re-dated.
- Window return = equal-weight buy-and-hold over (F, end], members fixed at F. A member is dropped for a suspect-flagged day or a return spanning more than 5 panel rows; a basket needs 2 valid members. Excess = basket minus same-window market.
- H3: univariate OLS per sector x factor x spec, HAC maxlags 3, 448 cells. Contemporaneous = calendar-month excess on the month's factor change (KSE100: raw sector return); leads k=1-3 = non-overlapping one-month excess from F(t+k-1) to F(t+k). Units: pts of monthly excess per +10% log move (PKR per +5%). Placebo: 1000 circular shifts of all 7 factors by one offset (12 to 105 months).
- H1: onset = first signal month after 3 non-signal months; entry F(t); 1, 2, 3 months; net = excess minus 0.5.
- H2: trigger = 20-row log change of USDPKR crossing up through 4%, 60-day lockout, entry next PSX close; 20 and 60 days; spread net of 1.0, others 0.5. Lens = 5 largest monthly depreciations, 3 months apart.
- Section 7: 10 largest up and 10 largest down monthly Brent log changes, 3 months apart, 20 and 60 days, gross.
- Event placebos: 2000 draws of the same n random entries, same baskets, period and costs.

## Results

**Multiple testing (H3).** |t| >= 2 in 53 of 448 cells; placebo median 37, 95th percentile 51 (share of draws at least 53: 0.047). The excess is the KSE100 factor, whose contemporaneous cells are market betas. Excluding it: 35 of 384 against a placebo median of 33 and 95th percentile of 45. Leads alone: k=1 4 cells (placebo median 9), k=2 8 (10), k=3 10 (10).

**Supported pre-registered cells (placebo p < 0.05, sign matches):** E&P on Brent, contemporaneous, +0.94 pts per +10%, t 4.04, p 0.008, R2 0.060, n 115. Autos on PKR, contemporaneous, -1.70 pts per +5%, t -3.32, p 0.008, R2 0.028, n 115. No lead cell (k=1, 2, 3) is supported. The other ten pre-registered cells are not supported at any lag. Tech on PKR at k=1 is placebo-significant with the **opposite** sign (-1.60, t -3.24, p 0.010); with the name-picked Tech-lite basket it is -0.90, t -1.30, p 0.312, so it is not robust. E&P on Brent at k=1 is -0.36 (t -1.37): the oil link is same-month only.

Exploratory, needs out-of-sample check: cement on Brent contemporaneous (-1.08, t -4.88, p 0.000), tech on Brent (+1.04, t 2.70, p 0.031), OMC on PKR k=1 (-1.50, t -2.28, p 0.015). The CSV marks 25 sector-factor pairs exploratory, mostly KSE100 betas of 0.71 to 1.58.

**Sensitivity map** (beta, NW t in brackets, * = placebo p < 0.05; units as above; KSE100 contemporaneous = raw beta).

Contemporaneous:

| sector | brent | coal | urea | cotton | palm | pkr | kse100 |
|---|---|---|---|---|---|---|---|
| E&P | 0.94 (4.0)* | 0.23 (0.5) | -0.25 (-0.5) | 0.31 (0.3) | -0.02 (-0.0) | 1.16 (1.4) | 1.16 (10.8)* |
| Refinery | 0.74 (1.4) | 0.34 (0.5) | 0.90 (1.3) | 3.75 (1.6) | 1.14 (1.1) | -2.47 (-1.9) | 1.57 (8.5)* |
| OMC | 0.57 (2.1) | 0.78 (2.0) | -0.58 (-1.1) | 1.59 (1.4) | -0.39 (-0.3) | 0.15 (0.2) | 1.41 (10.3)* |
| Gas utilities | 0.01 (0.0) | -0.80 (-1.0) | -1.20 (-2.5)* | -0.83 (-0.4) | 1.47 (0.6) | 0.76 (0.4) | 1.58 (6.1)* |
| Fertilizer | -0.69 (-2.2) | -0.84 (-1.2) | 0.23 (0.5) | -2.52 (-2.3) | -0.81 (-0.7) | 1.65 (2.1)* | 0.71 (6.6)* |
| Cement | -1.08 (-4.9)* | -0.47 (-0.6) | -0.08 (-0.2) | -1.69 (-1.3) | -0.55 (-0.6) | -1.36 (-1.9) | 1.33 (9.3)* |
| Power | -0.24 (-1.0) | 0.37 (0.7) | 0.16 (0.3) | -0.50 (-0.4) | -1.48 (-2.1) | 0.52 (0.8) | 1.10 (11.7)* |
| Autos | 0.50 (2.4) | 0.55 (1.2) | 0.42 (1.2) | 0.32 (0.3) | 0.81 (1.0) | -1.70 (-3.3)* | 1.47 (9.7)* |
| Pharma | -0.41 (-1.0) | 0.60 (1.4) | 0.25 (0.9) | -1.19 (-1.1) | -0.13 (-0.1) | -0.11 (-0.2) | 1.11 (6.5)* |
| Textiles | 0.60 (1.9) | -0.17 (-0.3) | 0.12 (0.3) | 0.63 (0.6) | 0.69 (1.1) | -0.43 (-0.7) | 1.22 (11.0)* |
| Tech | 1.04 (2.7)* | 0.09 (0.2) | -0.40 (-0.9) | 0.03 (0.0) | 0.72 (0.8) | 0.26 (0.3) | 1.36 (14.2)* |
| Chemicals | -0.09 (-0.5) | -0.43 (-1.0) | 0.11 (0.4) | 1.44 (1.0) | -0.86 (-1.6) | 2.39 (2.9)* | 1.09 (12.4)* |
| Food | 0.09 (0.5) | 0.21 (0.5) | -0.05 (-0.2) | 1.99 (2.1) | 0.41 (0.7) | 0.53 (0.8) | 1.33 (9.8)* |
| Banks | 0.14 (0.5) | 0.38 (0.7) | 0.30 (0.9) | 0.46 (0.4) | 0.11 (0.1) | 0.85 (1.4) | 1.06 (14.1)* |
| Steel/eng. | -0.25 (-1.6) | 0.21 (0.5) | 0.06 (0.2) | -0.72 (-0.8) | 0.17 (0.2) | -1.62 (-2.9)* | 1.36 (11.0)* |
| Glass/pack. | -0.25 (-1.2) | -0.11 (-0.3) | -0.10 (-0.3) | 0.85 (0.8) | -0.22 (-0.4) | -0.55 (-0.8) | 1.18 (10.8)* |

k=1 lead (tradable timing):

| sector | brent | coal | urea | cotton | palm | pkr | kse100 |
|---|---|---|---|---|---|---|---|
| E&P | -0.36 (-1.4) | 0.30 (0.5) | -0.02 (-0.0) | -0.23 (-0.2) | 1.02 (1.3) | -0.78 (-1.0) | -0.63 (-0.8) |
| Refinery | 0.31 (0.7) | 0.19 (0.2) | -1.51 (-1.4) | 1.69 (0.9) | 1.19 (1.0) | -0.65 (-0.5) | -0.91 (-0.8) |
| OMC | -0.05 (-0.2) | 0.33 (0.5) | -0.11 (-0.3) | 0.10 (0.1) | 0.02 (0.0) | -1.50 (-2.3)* | 0.65 (0.8) |
| Gas utilities | -0.21 (-0.7) | -0.46 (-0.5) | 0.57 (1.0) | 1.02 (0.4) | -0.57 (-0.3) | 0.70 (0.8) | 0.41 (0.2) |
| Fertilizer | 0.10 (0.3) | 0.26 (0.4) | 0.02 (0.0) | -0.66 (-0.5) | 0.07 (0.1) | 0.25 (0.3) | -0.07 (-0.1) |
| Cement | -1.08 (-3.4) | -0.67 (-1.8) | -0.48 (-2.1)* | -0.56 (-0.6) | -0.08 (-0.1) | 1.60 (1.8) | -0.86 (-0.6) |
| Power | 0.63 (1.7) | 0.02 (0.0) | 1.12 (1.6) | 0.94 (0.7) | 1.33 (1.2) | 0.10 (0.1) | -0.87 (-0.7) |
| Autos | 0.54 (1.1) | 0.50 (1.1) | -0.04 (-0.1) | 0.55 (0.6) | 0.74 (0.8) | -1.00 (-1.3) | 0.18 (0.3) |
| Pharma | -0.00 (-0.0) | -0.02 (-0.1) | -0.17 (-0.6) | -0.13 (-0.2) | -0.59 (-0.8) | 0.72 (1.1) | -0.05 (-0.1) |
| Textiles | 0.28 (1.4) | 0.23 (0.7) | 0.35 (1.2) | -0.39 (-0.5) | -0.22 (-0.3) | -0.27 (-0.6) | -1.21 (-1.3) |
| Tech | 0.04 (0.2) | -0.20 (-0.3) | 0.30 (0.7) | -1.04 (-0.9) | 0.47 (0.6) | -1.60 (-3.2)* | 0.62 (0.9) |
| Chemicals | 0.17 (0.8) | 1.53 (1.5) | 0.12 (0.4) | 1.47 (1.6) | 0.74 (0.6) | 0.78 (0.6) | -1.16 (-2.0) |
| Food | -0.18 (-0.7) | -0.29 (-0.8) | -0.22 (-0.8) | -0.53 (-0.7) | -0.70 (-1.2) | 0.30 (0.4) | 0.03 (0.0) |
| Banks | 0.66 (1.5) | 0.60 (0.9) | 0.19 (0.4) | -0.07 (-0.1) | -0.18 (-0.2) | 0.04 (0.1) | 1.52 (1.4) |
| Steel/eng. | -0.47 (-1.9) | -0.51 (-1.2) | -0.06 (-0.3) | 1.52 (1.7) | -0.11 (-0.2) | 0.67 (0.8) | -1.04 (-1.4) |
| Glass/pack. | -0.11 (-0.5) | -0.13 (-0.3) | 0.76 (1.8) | -0.09 (-0.1) | -1.19 (-1.7) | 0.73 (0.9) | -0.74 (-0.8) |

**H1 per episode** (excess vs market, % points; net = gross minus 0.5; k = months). Pre-2017-02 onsets 2015-04 and 2016-04 dropped.

| onset | Brent 3m | Refinery k1 / k2 / k3 gross | E&P k1 / k2 / k3 gross |
|---|---|---|---|
| 2017-09 | 21.1% | -3.64 / -9.71 / -21.32 | 11.75 / 14.96 / 18.49 |
| 2019-03 | 34.3% | 0.94 / 0.39 / -8.02 | 3.57 / 5.75 / 4.40 |
| 2020-06 (COVID rebound) | 180.4% | 27.92 / 46.81 / 28.66 | -15.36 / -24.06 / -26.03 |
| 2020-12 | 27.1% | 8.80 / 24.44 / 28.21 | -8.95 / -3.85 / -0.42 |
| 2022-02 | 45.5% | -1.26 / 17.16 / 25.15 | -4.35 / -2.74 / -1.72 |
| 2023-08 | 21.3% | 8.49 / 18.51 / 13.16 | -1.34 / -14.21 / -25.91 |
| 2026-03 (in-sample) | 106.5% | 5.92 / 0.26 / -11.24 | -6.20 / -6.31 / -12.67 |
| 2026-09 | 64.5% | PENDING: 11 trading days, Refinery +9.30%, E&P +0.14% so far | |

Ex-dates found inside E&P and refinery windows are all cash (OGDC, PPL, ATRL; dates in the raw output); no bonus ex-date turned up in any small-basket window.

**H1 summary** (net of 0.5; n = episodes, so n events = n episodes; placebo = random month-start entries; pctile = actual median's rank among placebo medians):

| row | n | mean | median | win% | worst | net median | net win% | placebo med / p5..p95 | pctile |
|---|---|---|---|---|---|---|---|---|---|
| Refinery 1m full | 7 | 6.74 | 5.92 | 71 | -3.64 | 5.42 | 71 | -1.79 / -5.40..4.03 | 97 |
| Refinery 2m full | 7 | 13.98 | 17.16 | 86 | -9.71 | 16.66 | 57 | -1.42 / -8.42..4.83 | 100 |
| Refinery 3m full | 7 | 7.80 | 13.16 | 57 | -21.32 | 12.66 | 57 | -2.32 / -10.89..10.57 | 98 |
| E&P 1m full | 7 | -2.98 | -4.35 | 29 | -15.36 | -4.85 | 29 | 0.49 / -5.55..4.91 | 8 |
| E&P 2m full | 7 | -4.35 | -3.85 | 29 | -24.06 | -4.35 | 29 | 0.69 / -6.03..7.10 | 15 |
| E&P 3m full | 7 | -6.26 | -1.72 | 29 | -26.03 | -2.22 | 29 | 1.33 / -8.45..8.50 | 28 |
| Refinery 1m excl 2026 | 6 | 6.87 | 4.71 | 67 | -3.64 | 4.21 | 67 | -1.65 / -5.92..3.94 | 95 |
| Refinery 2m excl 2026 | 6 | 16.27 | 17.83 | 83 | -9.71 | 17.33 | 67 | -2.11 / -8.30..4.68 | 100 |
| Refinery 3m excl 2026 | 6 | 10.97 | 19.15 | 67 | -21.32 | 18.65 | 67 | -3.11 / -10.54..7.28 | 100 |
| Refinery 1m excl 2026 and 2020-06 | 5 | 2.66 | 0.94 | 60 | -3.64 | 0.44 | 60 | -1.83 / -6.27..4.03 | 72 |
| Refinery 2m excl 2026 and 2020-06 | 5 | 10.16 | 17.16 | 80 | -9.71 | 16.66 | 60 | -2.08 / -9.47..5.13 | 99 |
| E&P 1m excl 2026 | 6 | -2.45 | -2.85 | 33 | -15.36 | -3.35 | 33 | 0.51 / -5.74..5.00 | 14 |

Rule per cell: Refinery 1m passes (median net 5.42 above placebo p95 4.03; 5 of 7 episodes positive; survives excluding 2026) but not once 2020-06 is also removed (median net 0.44, pctile 72). Refinery 2m and 3m fail because only 4 of 7 episodes are positive net, despite large medians. E&P fails everywhere. Dummy regression on all 20 signal months: refinery +2.48 pts (NW t 0.89), E&P -3.29 pts (t -2.18). Versus KSE100, refinery medians are 8.59 / 10.58 / 16.27 and E&P -2.56 / -4.50 / -5.72.

**H2.** 11 triggers from 2017-12-13 to 2023-11-15 (20-day PKR change 4.08% to 7.49%; each listed in the raw output); 5 macro episodes (2017-19 cycle, 2020, 2022, 2023-01, 2023-08/11), against the spec guess of about 13 and 3-4. None pending.

| row | n | eps | mean | median | win% | worst | net median | net win% | placebo med / p5..p95 | pctile |
|---|---|---|---|---|---|---|---|---|---|---|
| spread 20d | 11 | 5 | 0.00 | 1.22 | 55 | -7.21 | 0.22 | 55 | 0.08 / -3.40..3.26 | 53 |
| spread 60d | 11 | 5 | -0.12 | -1.09 | 36 | -22.65 | -2.09 | 36 | 1.06 / -4.90..7.31 | 19 |
| exporters minus market 20d | 11 | 5 | -1.17 | -0.29 | 27 | -5.27 | -0.79 | 27 | -0.15 / -2.43..2.01 | 35 |
| exporters minus market 60d | 11 | 5 | 1.05 | -1.44 | 45 | -9.71 | -1.94 | 36 | -0.51 / -3.66..4.40 | 24 |
| lens spread 20d | 5 | 5 | 1.68 | 2.58 | 60 | -3.81 | 1.58 | 60 | -0.10 / -4.56..4.68 | 66 |
| lens spread 60d | 5 | 5 | 3.76 | 4.95 | 80 | -1.56 | 3.95 | 80 | 0.99 / -6.49..7.80 | 75 |
| lens spread 60d excl 2020-03 | 4 | 4 | 3.26 | 4.44 | 75 | -1.56 | 3.44 | 75 | 1.36 / -7.33..8.90 | 71 |

Net spread is positive in 2 of 5 macro episodes at 20d and 3 of 5 at 60d. Textiles 20d after triggers: median -3.66 (pctile 3). Lens picks match the spec: 2023-01, 2022-07, 2019-06, 2020-03 (COVID-confounded), 2018-10.

**Top Brent months.** 10 up and 10 down picks, 6 episodes, 6 of the 10 up picks flagged rebound. They share the 2020, 2022 and 2026 episodes with H1 and H3, so they are not independent confirmation. Up picks, median excess (placebo pctile): 20 days refinery 1.17 (78), E&P 2.38 (75), OMC 1.10 (86); 60 days E&P -1.22 (37), refinery -0.61 (56), OMC 0.41 (66). No oil basket reaches placebo p95. Exploratory: autos after up picks +3.41 at 20 days (win 100%, pctile 99), textiles +3.49 (99); among 64 rows some are expected by chance. Pending: the 2026-07 up pick, 52 days elapsed (refinery +48.46%, E&P +5.33%, gross).

## Robustness

KSE100-relative excess (H1 above; H2 exporters 60d median -2.20, importers -2.17); excluding 2026 and 2020-06 (H1); excluding 2020 entries (H2 spread net median 20d -1.24, 60d -2.21); Tech-lite excluding PTC, TELE, AIRLINK (name-picked); Brent up picks without rebounds (4 events: refinery 20d median 7.09, pctile 94; 60d -6.19, pctile 25). Sector-note name lists were not run.

## Verdict

- **H1: not supported.** E&P goes the wrong way (median net -4.85 at 1 month, win 29%). Refinery is the only positive result: strong medians, but it fails the 2/3 rule at 2 and 3 months, loses its edge at 1 month when the COVID rebound is dropped, and rests on 7 episodes (5 after the exclusions). Power is low. Treat refinery strength after Brent spikes as a prior, not a rule.
- **H2: not supported.** Triggers: median net spread +0.22 (20d) and -2.09 (60d), far below the placebo p95 (3.26, 7.31). The lens is better (60d median net +3.95, 4 of 5 positive) but pctile 75 and n = 5; inconclusive.
- **H3: weak.** Two pre-registered contemporaneous cells pass. No predictive cell passes, and leads show fewer significant cells than chance. For the strategy: commodity and PKR moves are priced in the same month; there is no tradable monthly lag here. Use the E&P-Brent and autos-PKR betas to describe risk, not to time entries.

## Caveats

Survivorship: only names listed on 2026-10-16 are in the panel (3 E&P symbols; symbols.csv lists 4), so delisted textile, refinery and auto names are missing. Sector labels are today's. Returns are price-only and crude zeroes large ex-dividend drops, so E&P, fertilizer, power and OMC are understated (no dividends added back, lesson 19). Sub-threshold bonuses stay in as fake losses; the provisional action table is thin before 2024 and one unflagged bonus can move a small-basket window by 3-5 pts. Pink Sheet timing is assumed. 2026 is in-sample for H1. H1, section 7 and H3 reuse the same episodes; top-N picks are ex post. Basket sizes grow after 2024 (nominal Rs5m threshold). Whether KSE100 is a total-return index is unverified.
