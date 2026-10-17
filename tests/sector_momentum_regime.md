# Sector momentum and rate regime on KMI sector baskets

Run 17 Oct 2026. Script `scripts/tests/sector_momentum_regime.py`; raw output `tests/out/sector_momentum_regime.txt` (every number below comes from it). Seed 42, 2000 placebo draws.

## Hypothesis

- **H1.** Top 3 sectors by trailing return beat the bottom 3 over the next 1 and 3 months. Pre-registered primary: 6-month lookback, no skip, 3-month hold, non-overlapping. The other 11 grid variants are robustness only.
- **H2.** The regime changes which sectors lead. Frozen lists: HIKE = Autos, Islamic banks, Power; CUT = Fertilizer, Pharma, Cement, OMC. They came from the 2020 and 2024 episodes inside the sample, so H2 is an in-sample check.
- **Strategy question.** Does "overweight top-momentum sectors, tilted by regime" (rule RT) have an edge for a long-only KMI investor?


## Data

- Prices via `scripts/prices.py`: 456 symbols, 2016-10-17 to 2026-10-16. KMI lists: 15 derived files from 2019-01-28. Sector codes: `screener_20261016.csv`. Macro: policy rate, T-bill auctions, CPI, `kmiallshr.csv`. Flags: `suspected_corporate_actions.csv`.
- 107 formation months, 2017-11-30 to 2026-09-30; 104 have a 3m exit, and 95 of those are ranked (2019-03 to 2019-11 has fewer than 8 eligible sectors).
- Liquid KMI names per month: median 60, minimum 32. Eligible sectors (3 or more names): median 11, minimum 4. KMI members with no price file: median 14, maximum 26 of about 250.
- Of 7121 name-windows at 3m, 4 had a stale exit-day close and 0 a series ending inside. T-bill fallback to y3m: 6 of 107 months.


## Method (exact rules)

- Formation t = last trading day of the month. Entry = next day's close. Exit = close after the formation date that ends the hold. Windows chain with no gap or overlap.
- Names: latest KMI list on or before t (renames applied, XD/XB/XR stripped), median value above Rs5m over the 60 rows before entry, trading on the entry day. Sector = PSX code from the screener, labelled by majority note sector; the commercial-banks code is "Islamic banks". Names with no code are dropped (median 1 per month, maximum 3).
- Returns: crude, zeroed on every flagged (symbol, date); no window dropped; no dividend add-back. Signal: compounded lookback return (60% of rows observed), averaged over members. B = mean of all sectors with 3 or more names.
- Costs: 0.5% round trip times the fraction of slots replaced; first window 0.25%; conservative net charges 0.5% per leg every window; LS pays both legs.
- Regime: curve spread = 6M T-bill yield minus policy rate; at or below -50bp cuts priced, at or above +50bp hikes priced. CPI from months M-1 and M-4. G3 = last non-hold decision in 12 months.
- RT: in hikes or cuts months take the top 3 by momentum among eligible HIKE or CUT sectors, filling from the overall ranking; otherwise the plain top 3.
- 3m holds use three start-offset series; n is windows in ONE offset and results are averaged over offsets.


## Results

### T1: H1 grid (long-short spread LS, gross unless noted; n = windows per offset)

| L/skip/hold | n | mean | median | win | worst | best | t | p gross | p net | net mean | net cons. | turnover |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3/0/3m | 31.7 | +1.81% | +2.88% | 61% | -21.53% | +36.43% | 1.05 | 0.045 | 0.044 | +1.05% | +0.81% | 0.78 |
| **6/0/3m (primary)** | 31.7 | +3.26% | +2.65% | 65% | -21.64% | +57.32% | 1.73 | 0.002 | 0.001 | +2.66% | +2.26% | 0.62 |
| 12/0/3m | 31.7 | +2.49% | +3.19% | 64% | -49.82% | +33.38% | 1.28 | 0.013 | 0.009 | +1.98% | +1.49% | 0.52 |
| 3/1/3m | 31.7 | +0.87% | +1.08% | 53% | -59.59% | +34.01% | 0.45 | 0.225 | 0.221 | +0.10% | -0.13% | 0.78 |
| 6/1/3m | 31.7 | +3.52% | +3.12% | 67% | -51.31% | +36.76% | 1.88 | 0.001 | 0.001 | +2.92% | +2.52% | 0.61 |
| 12/1/3m | 31.7 | +1.05% | +1.57% | 60% | -49.82% | +27.13% | 0.52 | 0.191 | 0.143 | +0.51% | +0.05% | 0.54 |
| 3/0/1m | 97 | +0.91% | +0.76% | 59% | -11.34% | +16.72% | 1.58 | 0.056 | 0.022 | +0.41% | -0.09% | 0.49 |
| 6/0/1m | 97 | +0.89% | +0.79% | 57% | -11.20% | +27.37% | 1.47 | 0.060 | 0.011 | +0.51% | -0.11% | 0.38 |
| 12/0/1m | 97 | +0.79% | +0.81% | 59% | -17.56% | +18.67% | 1.21 | 0.080 | 0.015 | +0.48% | -0.21% | 0.31 |
| 3/1/1m | 97 | -0.03% | +0.37% | 53% | -12.58% | +16.62% | -0.06 | 0.506 | 0.331 | -0.53% | -1.03% | 0.50 |
| 6/1/1m | 97 | +0.63% | +0.69% | 58% | -14.90% | +14.61% | 1.08 | 0.130 | 0.035 | +0.26% | -0.37% | 0.37 |
| 12/1/1m | 97 | +0.22% | +0.81% | 54% | -17.56% | +18.67% | 0.33 | 0.345 | 0.117 | -0.10% | -0.78% | 0.32 |

Primary, by start offset (3m windows): offset 0 (Nov/Feb/May/Aug) n=32, mean +4.79%, median +3.11%, win 69%, t 2.21. Offset 1 n=32, +2.12%, +2.73%, 66%, t 1.29. Offset 2 n=31, +2.88%, +2.11%, 61%, t 1.68. Overlapping monthly series (labelled overlapping): n=95, +3.27%, median +2.71%, win 65%, Newey-West t 2.58.

Primary placebo (random sector ranks, same months): median of placebo means +0.03%, 5th percentile -1.87%, 95th +1.81%. Median-statistic p=0.006, win-rate-statistic p=0.002.

Long-only primary (top 3 minus B): gross +1.01%, net +0.70% (median +0.95%, win 54%, worst -15.91%, t 0.50). Net minus KMIALLSHR: -0.41% (median -2.20%, win 38%). Mean B window return +3.12%; mean KMIALLSHR +4.22%. About 2.25 of the 3.26 points come from the loser leg, which retail cannot short.

### Splits (primary, LS gross; n per offset)

| split | n | mean | median | win | net |
|---|---|---|---|---|---|
| 2017 / 2018 / 2019 | 1.0 / 4.0 / 1.0 | +0.12% / +5.58% / +5.80% | | | -0.38% / +5.04% / +5.30% |
| 2020 / 2021 / 2022 | 4.0 each | +9.51% / +1.10% / -0.93% | | | +8.95% / +0.48% / -1.51% |
| 2023 / 2024 / 2025 / 2026 | 4.0 / 4.0 / 4.0 / 2.0 | +3.57% / +5.80% / -1.02% / +1.63% | | | +2.91% / +5.13% / -1.63% / +0.88% |
| 2017-11 to 2021-12 | 13.7 | +5.19% | +3.77% | 73% | +4.63% |
| 2022-01 to 2026-06 | 18.0 | +1.83% | +1.33% | 59% | +1.19% |
| pre-2019 (2017-11 to 2018-12) | 4.7 | +4.65% | +3.67% | 77% | +4.12% |

Eight of ten calendar years have a positive mean. Effective n is the 32 windows per offset (sector returns within a window are cross-correlated).

### T2: regime x sector, next-3m excess vs B (mean/median/win; n = windows per offset; e = episodes)

Frozen-list sectors only; the full table and the 1m, CPI, last-MPS and +-25/+-100bp versions are in the raw output. Bonus payers (cement, fertilizer, banks) are biased down (R3).

| sector | cuts priced | neutral | hikes priced |
|---|---|---|---|
| Autos (HIKE) | +14.5/+13.2/78%, n5.3 e6, insufficient | -2.8/-4.4/33%, n16.3 | +1.3/-2.3/40%, n10.0 e7 |
| Islamic banks (HIKE) | +0.1/+3.8/67%, n5.0 e5, insufficient | -0.2/+0.2/51%, n9.7 | +0.5/-1.2/51%, n4.7, insufficient |
| Power (HIKE) | -3.4/-2.6/36%, n5.3, insufficient | +0.9/-0.1/52%, n13.0 | +10.8/+7.2/85%, n7.0 e6 |
| Fertilizer (CUT) | +3.5/+0.7/72%, n4.3, insufficient | -0.6/+1.1/58%, n9.7 | -10.4/-10.4/25%, n1.5, insufficient |
| Pharma (CUT) | +8.9/+5.8/83%, n5.3, insufficient | -2.5/-2.6/31%, n16.3 | -7.4/-5.7/21%, n6.3 e7 |
| Cement (CUT) | +4.8/+3.3/69%, n5.3, insufficient | +1.7/+0.5/49%, n16.3 | +0.5/-0.9/46%, n10.0 |
| OMC (CUT) | -2.8/-5.2/17%, n5.3, insufficient | -0.6/-2.1/41%, n16.3 | +1.8/-0.4/53%, n10.0 |

Every cuts-priced cell fails the 6-window minimum. The month counts are 16 cuts, 55 neutral and 36 hikes.

### T3: episodes and the HIKE-minus-CUT spread S

30 episodes (9 hikes, 6 cuts, 15 neutral). S = mean excess of eligible HIKE sectors minus CUT sectors, next 3m. Mean S per episode (months), %:

- Hikes: 2021-02 to 07 -0.44 (6); 2021-09 to 10 +3.35 (2); 2021-12 to 2022-12 -0.51 (13); 2023-02 to 05 +8.73 (4); 2023-07 to 09 +19.49 (3); 2026-03 +22.97 (1); 2026-05 +5.64 (1); two others n/a.
- Cuts: 2018-11 -8.24 (1); 2020-04 +14.08 (1); 2023-11 to 2024-06 +6.92 (8); 2024-08 -49.96 (1); 2024-10 to 2025-01 -5.27 (4); 2026-01 +13.13 (1).

Observed D = +3.60%. Circular-shift null (72 shifts): median -1.73%, 5th percentile -6.12%, 95th +4.36%; observed percentile 90%, p = 0.097. Predicted sign: hikes episodes S>0 in 5 of 7; cuts episodes S<0 in 3 of 6. Sensitivities (not used to pick): +-25bp D +1.97% (p 0.236); +-100bp +3.58% (p 0.278); last-MPS labels +3.33% (p 0.306).


### T4: regime tilt RT vs momentum top 3 vs B vs KMIALLSHR (net, primary variant)

| series | n | mean | median | win | worst | max DD | placebo p | half 1 | half 2 |
|---|---|---|---|---|---|---|---|---|---|
| RT net (abs) | 31.7 | +4.20% | -1.20% | 46% | -28.10% | -54.96% | | +2.23% | +5.69% |
| Momentum top 3 net (abs) | 31.7 | +3.81% | -0.86% | 45% | -28.10% | -52.53% | | +2.38% | +4.90% |
| B net (abs) | 31.7 | +2.97% | +0.35% | 51% | -31.48% | -51.53% | | -0.02% | +5.24% |
| KMIALLSHR (abs) | 31.7 | +4.22% | +2.19% | 60% | -29.57% | -34.01% | | +0.49% | +7.04% |
| RT net - B | 31.7 | +1.09% | +0.21% | 51% | -16.02% | -24.58% | 0.255 | +2.09% | +0.33% |
| Momentum net - B | 31.7 | +0.70% | +0.95% | 54% | -15.91% | -22.46% | 0.059 | +2.23% | -0.46% |
| RT net - KMIALLSHR | 31.7 | -0.02% | -2.31% | 40% | -19.07% | -55.71% | 0.255 | +1.74% | -1.35% |
| RT net - momentum net | 31.7 | +0.39% | +0.00% | 23% | -12.50% | -16.83% | | -0.14% | +0.80% |

RT excess vs B by offset: +2.98%, +0.63%, -0.35%. RT turnover 0.62 and momentum 0.64; RT differs from momentum in 37 of 95 months.

## Robustness

- **T1 grid:** seven of twelve variants have a gross placebo p below 0.10 (three 3m skip-0, 6/1/3m, three 1m skip-0). The 1m variants are weak: +0.8% to +0.9% gross, +0.4% to +0.5% net for skip 0, negative after conservative costs.
- **T5, return series:**

| series | LS gross | LS net | p net | D | D p | RT-B net | RT p | RT-KMI |
|---|---|---|---|---|---|---|---|---|
| headline | +3.26% | +2.66% | 0.000 | +3.60% | 0.097 | +1.09% | 0.265 | -0.02% |
| A crude only | +3.28% | +2.67% | 0.002 | +3.60% | 0.097 | +1.15% | 0.226 | +0.08% |
| B provisional adjusted | +3.27% | +2.66% | 0.000 | +3.56% | 0.097 | +1.16% | 0.234 | +0.34% |
| C (extra, not in spec) | +2.32% | +1.71% | 0.017 | +4.46% | 0.042 | +0.82% | 0.508 | -0.06% |

Signs are unchanged under A and B. C was added after inspection: the headline leaves 145 stock-days beyond the circuit limit unzeroed (high-volume ex-dates such as LUCK 5:1, KOHC, THCCL, LCI and the 2025-26 face-value splits show as -80% to -90% days, and `provisional_actions()` misses them). C zeroes them. D then becomes significant (p 0.042), so D is **not robust to price adjustment**. The LS spread shrinks but stays positive.


## Verdict

- **H1: works, modestly.** The primary passes every pre-specified check (net placebo p 0.001, positive in all 3 offsets and both halves, same sign under A and B). But the plain t is 1.73 (offsets 2.21, 1.29, 1.68), weaker than the placebo p implies, because momentum picks high-variance sectors and the placebo does not. Most of the spread is the short leg. 3m lookbacks and skip-month variants are weak; 1m holds fail conservative costs.
- **H2: not supported.** D = +3.60%, p = 0.097; predicted sign in 5 of 7 hikes episodes but only 3 of 6 cuts episodes; lists are in-sample.
- **Tilt rule: no edge.** RT net vs B: mean +1.09%, median +0.21%, win 51%, placebo p 0.255, negative in offset 2. Against KMIALLSHR it fails mean, median, win rate, placebo, offsets, halves and the A/B check. Plain momentum top 3 (+0.70% vs B, p 0.059) also fails the offset and half checks.
- **Meaning:** about 32 windows and 6 cuts episodes cannot support a regime tilt. Sector momentum is at most a tiebreaker inside a sector view. Long-only it does not beat the KMI All Share index (-0.41% net per 3 months, median -2.20%).


## Caveats

- Survivorship: only names listed on 2026-10-16 have prices (median 14 KMI members missing per month). EW baskets are flattered; the effect on the spread is unknown.
- KMI lists before 2019-01-28 are approximated by the 2019 list; derived lists sit 0 to 7 names above official totals. Pre-2019 (14 months) is shown separately.
- Sub-circuit bonuses stay as fake losses (R3), biasing cement, fertilizer and banks down. High-volume splits survive in the headline (see C).
- Labels: SNGP and SSGC sit in OMC (code 821 majority); Islamic banks has only 3 names (BIPL, FABL, MEBL); Textiles merges three codes.
- H2 lists are in-sample; all cuts-priced cells are insufficient.
- Rs5m is nominal (about 46 liquid names in 2017). KMIALLSHR is price-only and cap-weighted, so not like-for-like.
- Multiple testing: 12 grid variants, 3 regime thresholds, 2 regime definitions; only the primary was pre-registered.

