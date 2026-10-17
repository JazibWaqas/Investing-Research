# Playbook: sector rotation by rate regime

Written 2026-10-17. Evidence: the seed finding (`seed/PSX_STATE`, item l; audited in `tests/seed_audit.md`), a re-run of the same series for the three first-hike windows (`seed/data/macro/sector_monthly_ret.csv` against `ew_mkt_ret.csv`: 6-month excess return starting the month after the decision), the sixteen sector notes, and `practitioner_signals.md`. Status: two cutting cycles and three hiking windows. That is case studies, not statistics. The baskets are the seed's equal-weight survivor sets, chosen with hindsight.

## 1. What the data says

6-month excess return against the equal-weight market, in points:

| Sector | First cut Mar 2020 | First cut Jun 2024 | Hike Jan 2018 | Hike Sep 2021 | Hike Apr 2026 |
|---|---|---|---|---|---|
| Islamic banks | -48 | -49 | +22 | +4 | +1 |
| Conventional banks | -48 | -18 | +2 | +10 | -6 |
| Power | -42 | -46 | -2 | +21 | -17 |
| Chemicals | -28 | -41 | +14 | +11 | -12 |
| E&P | -23 | +30 | +4 | +9 | +1 |
| Fertilizer | -44 | +42 | +12 | +21 | -2 |
| Pharma | -36 | +37 | -7 | -5 | -11 |
| OMC and gas | -11 | +107 | -5 | -8 | -7 |
| Refineries | +33 | +14 | -3 | -23 | +83 |
| Cement | +27 | +1 | -22 | +1 | +3 |
| Steel | +28 | -52 | -12 | +1 | +3 |
| Textiles | +17 | -22 | -13 | +1 | -7 |
| Autos | +4 | -38 | -27 | +7 | -10 |
| Tech | +126 | -5 | +50 | -19 | -10 |
| Food | -1 | +17 | +51 | -13 | -20 |

What repeats:

- **After a first cut, Islamic banks and power lag in both cycles** (about -48 and -42 to -46), as the seed found. Chemicals and conventional banks lag in both too.
- **The leaders differ by cycle.** 2020 rewarded leveraged cyclicals and tech (a global tech boom too). 2024 rewarded OMC, fertilizer, pharma and E&P, the sectors whose earnings were inflecting. Only refineries led both times.
- **In hike windows, Islamic banks (3 of 3) and E&P (3 of 3) beat the market; pharma (0 of 3) and OMC and gas (0 of 3) lag.** Fertilizer led 2 of 3. Power is not a reliable hike-regime leader: +21 in 2021, -2 in 2018, -17 now. The power note's "power led in hike regimes" rests on the 2021 window alone.

## 2. What the sector notes add

The mechanisms behind the numbers:

- **Islamic banks:** high-CASA banks reprice assets faster than funding, so hikes widen spreads (MEBL +60 points relative, 2018-19). The 2020 fall came before the cuts.
- **Cyclicals at a rate peak:** cement bottomed on 26 Mar 2020, before the data turned. Levered paper (CEPB +450%) bottomed in Aug 2019, seven months before the first cut. Textiles rallied in May 2020 and May 2025 on cuts. So entry comes at or just before the first cut, not after the data.
- **Autos:** volumes swing 2x on financing cost. In 2023 the sequential turn in sales came only after T-bills started falling.
- **OMC:** "falls on rates and leverage, rallies on cuts and receivables" (PSO +176% from Oct 2024).
- **Tech:** the 2020 rate collapse produced the largest move. The 2021 turn in T-bills ended it.
- **Steel:** month-to-month rate changes do not time it (0.05 correlation). The end of tightening in 2019 did (+49 points relative).

The practitioner sweep ranks the rate path as the second most-cited driver after oil. It found no tested practitioner rotation rule. The 6M T-bill minus the policy rate is the market's own vote on the next move (`islamic_banks_financials.md`).

## 3. The rotation rule

**Trigger: "pre-cut" state.** Both conditions must hold:

1. CPI YoY falls for two consecutive monthly PBS prints, and the weekly SPI trend is down.
2. The 6M T-bill cut-off is below the policy rate at two consecutive auctions.

**Actions at the trigger:**

1. Stop adding hike-regime names (MEBL, FABL, HUBC). Cut Islamic bank and power weights by half. Cut the other half at the first actual cut. The seed measured the lag from the end of the cut month, but in 2020 the fall started before the cut, so do not wait for the cut to begin.
2. Move that money into leveraged, rate-sensitive cyclicals whose latest quarter already shows earnings holding up. Candidates now: autos (SAZEW, GAL, HCAR), cement (MLCF, DGKC, FCCL), steel (ISL), levered packaging (PKGS), textile composites (NML, ILP), PSO, and SYS. Rank them with leg 1 of `catalyst_trade.md`. Do not reuse the 2020 or 2024 leader lists.
3. Treat E&P and fertilizer as undecided (-23/+30, -44/+42). Hold them on their own catalysts, not on the regime.
4. Exit the rotation if the 6M bill climbs back 50bp above the policy rate, or CPI turns up for two prints.

**Size.** n=2. Rotate the regime part of the book in two steps, not all at once. The core yield names (FFC, OGDC) stay.

## 4. State on 17 Oct 2026

The 6M T-bill is 12.40% against a policy rate of 11.5%, so it is 90bp above. CPI fell to about 10.3% in September from 11.1% (one print, unverified on PBS), and the SPI is rising (11.38%). The rule has not fired. We are in a hike-pricing regime: favour Islamic banks, E&P and FFC for the core, and keep the cyclical sleeve small until the trigger. Re-check after each fortnightly T-bill auction and each CPI release (next CPI about 2 Nov).
