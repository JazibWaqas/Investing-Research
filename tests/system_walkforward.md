# System walk-forward: B0, B1, S2, S3, S4 (pre-registered)

Run 17 Oct 2026. Script `scripts/walkforward.py`; raw output `tests/out/system_walkforward.txt`; trades `tests/out/walkforward_trades.csv`; monthly holdings `tests/out/walkforward_holdings.csv`. Rules: `knowledge/playbooks/strategy_candidates.md`, frozen before this run. Logged in `DECISIONS.md`.

## Hypothesis

Value, regime and catalyst signals, layered on a liquid KMI universe, beat buying the market and never selling (B0) after 0.5% round-trip costs. Each strategy carries its own abandonment rule: B1 below B0 (ratio under 1.00), S2 under 1.05 x B0, S3 under 1.10 x B0, S4 below the better of S2 and S3. A satellite whose median trade does not beat 1,000 random-name placebos is abandoned whatever the strategy does.

## Data

- Prices: `panel_close.parquet` with `prices.returns(..., 'adjusted')` on `data/corporate_actions.csv`, cash at 85% (15% withholding), dividends reinvested. Cash dividends are complete only from Nov 2024, so before that the strategies and the EW market are close to price return and **KSE100 is price only**. Comparisons with KSE100 are therefore tilted in the strategies' favour by roughly the missing dividend yield.
- Panel holds only the 456 names listed on 16 Oct 2026 (survivorship; every EW figure is flattered).
- KMI membership: derived lists plus `index_changes.csv`; the 13 formations before 28 Jan 2019 use the 2019-01-28 derived list (**approximation**). U(t) is small: 46 to 60 names in 2018, 32 to 75 in 2019-22, 70 to 141 in 2024-26.
- Sectors: screener codes mapped as in `sector_momentum_regime.py`; 2026 snapshot, static. 0.8 names per month have no code.
- Value: `sa_ratios.csv`, 108 names picked on 2026 liquidity, FY rows 2020 (2), 2021 (28), 2022 to 2026 (103 to 107 a year). 464 of 530 rows matched to an annual-result filing; the rest use FYE + 4 months.
- Quarterly EPS: StockAnalysis, 129 names, announcement dates re-joined to result filings (the file's own join sometimes stamped extension notices). Consolidation **unverified** (lesson 1).
- Sponsor satellite: `data/insider_trades.csv` **absent**. S3 and S4 are therefore "no sponsor satellite": S3 is core only, S4's satellite is the earnings-blowout signal only.

**Value period.** The frozen text said value selection starts "about Oct 2020". The data say **Aug 2022**: Dec 2020 has 0 value-eligible names in U(t), Dec 2021 has 4, Dec 2022 has 38. Before that, B1 and the S2/S3/S4 cores hold the equal-weight of the chosen sectors' liquid names (the frozen fallback). Value picks therefore run on 50 of 106 months, inside the 2022-25 rerating (lesson 9).

**EPS coverage** (liquid KMI name-quarters with a dated EPS row; under 70% is UNCOVERED):

| Year | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Dated rows / name-quarters | 0/219 | 0/170 | 4/245 | 94/250 | 142/199 | 186/252 | 243/346 | 309/453 | 180/258 |
| Coverage | 0% | 0% | 2% | 38% | 71% | 74% | 70% | 68% | 70% |
| Flag | uncovered | uncovered | uncovered | uncovered | covered | covered | covered | uncovered | uncovered |

2026 sits at 69.8% and 2025 at 68%, just under the line. Signals still trade where they exist (they are point in time) and no other signal is substituted. 20 of S2's 42 satellite trades entered in uncovered years.

## Method (exact point-in-time rules)

- Calendar: form at the last close F of month t, trade at the first close D of month t+1 when Rs50,000 arrives. 106 deposits, 1 Jan 2018 to 1 Oct 2026, Rs5.30m. Value at the 16 Oct 2026 close.
- U(t): KMI All Share member at F and median traded value over the 60 sessions before F of at least Rs5m with 40+ traded sessions. Sector eligible with 3+ names. Held names are sold at D if absent from the KMI list at D-1 (Shariah exit).
- Regime. B1: latest 6M cut-off minus latest policy rate, +-50bp. S3: EASING if CPI YoY (month t-1, the latest usable print) fell twice and the last two 6M auctions were below the policy rate, or the last decision was a cut and 6M is within 50bp of policy; once EASING it stays until 6M reaches policy + 50bp or CPI rises twice (my reading of "leave EASING"). TIGHT if 6M is 50bp+ above policy or a hike in the last 6 months. EASING wins a tie. No SPI.
- Sector momentum: 126-session EW total return of U(t) names. Sectors: S2 and NEUTRAL top 3; EASING top 3 of the seven listed; TIGHT the three listed.
- Core pick: highest drift-adjusted EY = (P at FYE / PE) / P now, among names with ROE of at least 15%; banks by ROE / (PB drift-adjusted). Prices for the drift are bonus/split-only. B1 ranks EY + drift-adjusted DY across allowed sectors. A value row is usable from the first close after the annual-result filing (15:30 rule), else FYE + 4 months.
- Satellite signal: EPS_q at least 1.5x EPS_q-4 (EPS_q-4 above 0) or loss to profit; a stock within +-5% of the EW U(t) return over the 20 sessions after the first close following the filing; live from session 20 until that name's next filing (my added expiry). Ranked by 4 x EPS_q / P.
- Sizing and allocation: sleeve targets as frozen (core 3 x 16.7% or 4 x 12.5%, satellite up to 4 x 12.5%; empty sleeve to core, empty core to EW U(t)). Deposits plus sale proceeds go to the names furthest below target, water-filled with a Rs5,000 minimum ticket. Names above 35% at F are trimmed to 25% at D; in the headline the shortfall rule may buy a trimmed name back.
- Exits as frozen. Satellite time stop, breaker and 25% trailing stop are tested at the month-end F and executed at D, so a stop can fire up to a month late.
- Costs 0.25% per side on every rupee traded, including each deposit. KSE100 has no costs. EW KMI: U(t) rebalanced monthly to equal weight with the same costs.

## Results (frozen rules, total return, headline)

| | Final Rs | x deposits | vs B0 | TWR CAGR | IRR | Max DD (trough) | Worst 12m |
|---|---|---|---|---|---|---|---|
| B0 buy market | 12,418,018 | 2.34 | 1.000 | +10.1% | +18.7% | -61.3% (Mar 2020) | -51.2% |
| B1 orchestrator | 13,110,944 | 2.47 | 1.056 | +10.1% | +19.9% | -66.3% (Jun 2023) | -52.9% |
| S2 momentum + blowout | 14,170,936 | 2.67 | 1.141 | +11.8% | +21.6% | -61.3% | -53.5% |
| S3 regime, no sponsor sat | 17,630,566 | 3.33 | 1.420 | +19.2% | +26.3% | -50.2% | -42.2% |
| S4 full, no sponsor sat | 16,541,384 | 3.12 | 1.332 | +18.0% | +24.9% | -50.2% | -42.2% |
| EW liquid KMI, rebalanced | 10,242,065 | 1.93 | 0.825 | +7.4% | +14.5% | -60.9% | -52.1% |
| KSE100 price index, no costs | 17,124,185 | 3.23 | 1.379 | +17.4% | +25.6% | -41.6% | -28.9% |

Only S3 finishes above KSE100 (1.03x); S4 is 0.97x, S2 0.83x, B1 0.77x, B0 0.73x.

Trades (net of 0.5%; trade = first buy to full exit; open trades marked at 16 Oct, shown separately):

| | Closed n | Hit | Median | Mean | Worst | Open n | Avg names | Sell turnover p.a. | Fees Rs |
|---|---|---|---|---|---|---|---|---|---|
| B0 | 89 | 48% | -0.9% | +14.5% | -70.5% | 185 | 99 | 6% | 23,701 |
| B1 | 277 | 43% | -6.1% | +5.4% | -72.3% | 5 | 24.8 | 178% | 364,150 |
| S2 | 299 | 43% | -4.9% | +2.9% | -58.0% | 6 | 13.7 | 247% | 562,582 |
| S3 | 121 | 57% | +5.4% | +14.6% | -43.0% | 3 | 5.6 | 199% | 616,733 |
| S4 | 160 | 60% | +5.0% | +17.5% | -42.7% | 8 | 7.6 | 195% | 534,912 |

By sleeve, return on cost: B1 core +10.4%; S2 core +10.3%, satellite +3.4% (38 closed, median +2.6%); S3 core +9.8%; S4 core +14.1%, satellite +5.7%. S3's profit is two stocks: SAZEW Rs6.3m and LUCK Rs4.5m of Rs12.3m total.

Rs value of the deposits (strategy / KSE100 / EW KMI):

| Date | B0 | B1 | S2 | S3 | S4 | KSE100 | EW KMI |
|---|---|---|---|---|---|---|---|
| 31 Dec 2018 | 476,874 | 474,668 | 511,181 | 510,603 | 510,603 | 524,015 | 480,974 |
| 31 Dec 2019 | 1,110,007 | 1,201,828 | 1,064,706 | 1,239,558 | 1,239,558 | 1,261,529 | 1,132,923 |
| 31 Dec 2020 | 2,491,266 | 2,935,478 | 2,595,585 | 2,525,151 | 2,525,151 | 2,053,357 | 2,462,256 |
| 31 Dec 2021 | 2,639,756 | 2,642,308 | 2,760,923 | 2,907,553 | 2,893,531 | 2,674,135 | 2,745,893 |
| 31 Dec 2022 | 2,416,113 | 2,112,405 | 2,258,320 | 3,413,222 | 3,247,730 | 2,986,859 | 2,355,127 |
| 31 Dec 2023 | 4,545,548 | 4,434,757 | 4,142,055 | 6,197,745 | 6,398,578 | 5,455,893 | 4,309,309 |
| 31 Dec 2024 | 9,212,574 | 8,856,624 | 11,015,798 | 17,952,247 | 15,642,638 | 10,981,075 | 8,421,190 |
| 31 Dec 2025 | 12,795,242 | 14,857,310 | 17,060,631 | 22,758,149 | 19,910,094 | 17,399,027 | 11,071,893 |
| 16 Oct 2026 | 12,418,018 | 13,110,944 | 14,170,936 | 17,630,566 | 16,541,384 | 17,124,185 | 10,242,065 |

Splits (time-weighted CAGR):

| | 2018-21 | 2022-26 | From Sep 2022 (value live) |
|---|---|---|---|
| B0 | -1.6% | +20.9% | +27.8% |
| B1 | -1.9% | +21.1% | +27.2% |
| S2 | -0.8% | +23.6% | +33.8% |
| S3 | +5.2% | +32.4% | +39.9% |
| S4 | +5.0% | +30.1% | +37.4% |
| EW KMI | -0.3% | +14.3% | +21.0% |
| KSE100 | +2.3% | +31.6% | +39.3% |

2026 to date: S3 -24.6%, S4 -19.3%, S2 -19.6%, B1 -14.7%, B0 -6.8%, KSE100 -4.4%.

**Satellite placebo** (1,000 sets, one random U(t) name per trade, same entry day and exit, lump sum, net of 0.5%):

| | Trades | Actual median | Placebo median | Difference | Actual above |
|---|---|---|---|---|---|
| S2 satellite | 42 | +1.5% | +1.1% | +0.42 pt | 57% of sets |
| S4 satellite | 45 | +0.4% | +0.6% | -0.20 pt | 48% of sets |

It is one signal, and 42 versus 45 trades give opposite signs: no detectable edge.

## Abandonment verdicts

| Strategy | Test | Result | Verdict |
|---|---|---|---|
| B0 | bar | n/a | bar |
| B1 | Rs13.11m / Rs12.42m = 1.056 vs 1.00 | passes by 5.6% | **survives** (barely) |
| S2 | 1.141 vs 1.05 | passes | **survives**; satellite passes the placebo by 0.42 pt (noise) |
| S3 | 1.420 vs 1.10 | passes | **survives**, as an upper bound (in-sample sector lists, two stocks, no sponsor test) |
| S4 | Rs16.54m / Rs17.63m = 0.938 vs 1.00 | fails | **abandon**; its satellite also fails the placebo |

**Post-hoc variants** (not headline), ratio to that variant's B0:

| Variant | B1 | S2 | S3 | S4 | S4 vs best(S2,S3) |
|---|---|---|---|---|---|
| A. price return only | 1.020 | 1.122 | 1.301 | 1.391 | 1.069 (passes) |
| B. value lag = later of filing and FYE+3m | 1.461 | 1.351 | 1.440 | 1.290 | 0.896 |
| C. satellite off | 1.056 | 1.099 | 1.420 | 1.292 | 0.910 |
| D. trimmed name not re-bought that month | 1.055 | 1.192 | 1.387 | 1.335 | 0.962 |

S4 fails in the headline and three of four variants and passes only on price return. B1, S2 and S3 pass in every variant. S2 without its satellite still passes (1.099).

## Caveats

1. **Fragile ranking.** B1 jumps from 1.056 to 1.461 under a one-month shift in value timing; S3 moves 1.30 to 1.44. The B1 book is five names. Do not read the ordering of B1, S2, S3 and S4 as stable; only the facts below hold across variants.
2. **Everything but S3 lags KSE100**, and B0 sits at 0.73x it. A cap-weighted index of large caps beat the equal-weight liquid-KMI market in 2024-26 even before the index's missing dividends. KSE100 includes non-KMI names, so it is a benchmark, not an investable alternative.
3. **S3 is the most flattering result.** Its sector lists were read off the same 2018-2026 windows; it earned Rs12.3m on a book dominated by SAZEW and LUCK; and it lost 24.6% in 2026 to date against KSE100 -4.4%.
4. **Value was tested for only 50 months** and only after the 2022 rerating began. The 2018-21 gains of S3 come from the sector rule on EW fallbacks, not from value.
5. **Satellite is thin**: 42 to 45 trades, 20 in uncovered years, EPS unverified for consolidation, signals expire at the next filing by my assumption, and stops act at month-end so a 25% stop can execute late.
6. **Cap rule.** A 3-name core drifts over the 35% cap often, and the literal rule can re-buy what it just trimmed (S3 trimmed 33 times). Variant D changes S3 by 2% and does not change any verdict.
7. **Survivorship and partial dividends** flatter all EW figures and tilt the dividend comparison; the 15% withholding applies only where cash dividends are known.
8. Costs are 0.25% per side only. No slippage on Rs1.7m satellite tickets, no tax, fractional shares allowed, and all suspended names are assumed sellable the next month.
9. Sponsor-buying was not tested, so S3 and S4 verdicts are for the versions without it.
