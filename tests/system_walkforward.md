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

## Post-mortem and audit (Opus, 2026-10-17)

Evidence: `scripts/walkforward.py` (patched, audit sections 7E, 7F and 8), the unpatched engine kept as `scripts/walkforward_v0.py`, `scripts/tests/walkforward_audit.py` with output `tests/out/walkforward_audit.txt`, and `tests/out/walkforward_trades_pool.csv` (the trades of the same-pool re-run). The headline (sections 1 to 6 of `system_walkforward.txt`) is unchanged by the patch: every frozen number above still holds. Only new lines were added.

### 1. Lookahead audit

The engine's own timing is clean. Every decision at the month-end close F uses data stamped by F and trades at the next month's first close. Liquidity uses the 60 sessions strictly before F. Value rows are gated on the result filing. Satellite signals go live 20 sessions after the filing (minimum checked: 20). Stops are tested at F and executed at D, which is late, not early. The leaks are in the data, and one of them is material.

| # | Source | Finding | Severity | Bias | Fix |
|---|---|---|---|---|---|
| 1 | `sa_ratios.csv` `pe`, `date`, `TTM`, `peForward` | Clean. `TTM` and `peForward` are never read. Each row is gated on the annual-result filing (464 of 530 matched; 66 use FYE + 4 months). `pe` is on the FYE price: implied EPS matches the sum of the four quarterly EPS within 5% for 79% of 374 rows (median error 0.1%), against 25% at the filing-date price and 7% at today's price. The drift adjustment is therefore right. 13 rows are usable under 30 days after FYE (e.g. ARPL), which looks like genuinely early filers but was not checked against the PDFs. | none | none | none |
| 2 | **Pick pool chosen on 2026 liquidity** (`sa_ratios` 108 names, `quarterly_eps` 129; 132 together) | **Leak.** Every value pick and every earnings signal comes from names that were liquid in 2026, while B0 holds all of U(t). Inside U(t), pool names beat the rest by +2.28% a month from Aug 2022 to Sep 2026 (median +3.04%, t 3.85, 3.01x compounded) and by +0.03% before (t 0.04). The pool is 82% to 85% of U(t). | **material** for the satellite verdicts; moderate for the strategy ratios | favours every value or earnings strategy against B0, and favours the satellite against a placebo drawn from all of U(t) | Use a same-pool bar and a same-pool placebo. Results below. |
| 3 | `cpi.csv` `month` | Clean. At month-end t the regime reads print t-1. The unverified 2026-09 print is never read (the last formation reads August). | none | none | none |
| 4 | Index membership | Mostly clean. Derived rows are dropped and renames mapped. Across the 16 lists, no name's next KMI_ALL change is an add, so the rollback holds together. Left over: the 13 formations before 28 Jan 2019 use the 2019 list (an approximation), and 14.3 members a month (max 26) have no price series because they were delisted or renamed. Exits use the effective date, although the deletion notice comes out about a week earlier. That is conservative, not a leak. | low | survivorship: flatters EW and B0; unclear against the strategies | Flag only. Possible honest refinement: skip names with a pending deletion notice (CSAP, below). |
| 5 | Sector labels and snapshot data | `universe_scored`, `sector_monthly_ret`, `ew_mkt_ret`, `symbols.csv` and `listed_in` are never read. Sector returns are built from U(t). The labels themselves are the 16 Oct 2026 screener codes applied backwards (ENGROH and DAWH as Fertilizer, SNGP as OMC). | low | unknown, small | Flag only. No dated sector history exists. |
| 6 | Announcement `datetime` and EPS dates | Clean. Timestamps are Asia/Karachi wall time. 50 of 1,946 EPS filings came after 15:30 and move to the next session; Friday-afternoon filings are treated as after the close, which is conservative. Filing lag runs 10 to 148 days, median 31. 170 dates were re-joined to the result filing, 144 of them earlier than the file's own stamp, which had sometimes caught transmission or extension notices. EPS values are StockAnalysis's, possibly restated, with consolidation unverified (lesson 1). | low | unknown | Flag. ENGROH's ROE of 0.40 for a holding company is the case to check. |
| 7 | Book closure, ex dates, corporate actions | These affect return measurement, not signals. Ex date is book closure minus 2 trading days (minus 1 from Mar 2026), checked on price gaps. 107 bonus rows are `gap_inferred` (size off by a few points), and the loader zeroes unexplained circuit-breaking days. S3's two drivers are real: SAZEW had no bonus or split in its Jan 2024 to Jan 2025 window (raw Rs189.7 to Rs1,131.7). LUCK's 5:1 split on 28 Apr 2025 is in the table (raw 889.4 to 389.6, times 5, so +119%; total-return index +121%). | low | mixed | none |
| 8 | Panel survivorship (456 names listed on 16 Oct 2026) | Known; cannot be fixed with this data. | moderate for levels | flatters every EW figure, B0 included | Flag. |
| 9 | S3 sector lists read off 2018-2026 | Known in-sample. | moderate | flatters S3 and S4 | Treat as an upper bound. |
| 10 | Variant B (FYE + 3 months) | For the 66 rows with no matched filing, it uses FYE + 3 months, which can come before the real filing: a small lookahead, inside a post-hoc variant only. B1's 1.461 there is not evidence. | low | flatters variant B | Read the frozen FYE + 4 months result. |
| 11 | `data/insider_trades.csv` | Appeared at 23:44, after the builder's run. Per `tests/insider_cluster_buying.md` it holds 22 random symbols plus 2026 filings, not the full universe, so it cannot drive a point-in-time sponsor satellite for 2018-2026. S3 and S4 stay "no sponsor satellite". | n/a | n/a | Re-run once the full extraction lands. |
| 12 | **Benchmark labels** (found 18 Oct; lesson 20, `data/macro/INDEX_NOTES.md`) | `kse100.csv` and `kmiallshr.csv` are **total-return** indices, per the PSX brochures. The builder's "KSE100 price index" label is wrong, and so is the caveat above that KSE100 comparisons favour the strategies: they favour the index. The strategies carry cash dividends only from Nov 2024. KSE100's implied yield was 5.0% to 7.6% a year in 2021-25. | **material** for every "vs KSE100" or "vs index" claim; none for ratios to B0 (same basis) | against the strategies | Labels corrected in the script. The numbers cannot be fixed until cash dividends before Nov 2024 are in `corporate_actions.csv`. |

**Leak 2, both numbers** (ratio to B0; `system_walkforward.txt` section 8):

| | Frozen vs B0 (headline) | Frozen vs same-pool B0' | Same-pool re-run vs B0' (all strategies on the 132 names) |
|---|---|---|---|
| B0' / B0 | 1.000 | 1.050 (Rs13.04m) | 1.000 |
| B1 | 1.056 | **1.006** | 1.137 |
| S2 | 1.141 | **1.087** | 1.271 |
| S3 | 1.420 | **1.353** | 1.324 |
| S4 | 1.332 (0.938 of S3: abandon) | 1.269 | 1.461 (1.103 of S3) |
| S2 satellite, placebo from its own pool | +0.42 pt | **-0.12 pt (fails)** | -1.88 pt (fails) |
| S4 satellite, placebo from its own pool | -0.20 pt | **-1.10 pt (fails)** | -1.18 pt (fails) |

At the frozen thresholds no strategy verdict changes: B1 passes by 0.6%, S2 by 3.5%, S3 by 23%. The satellite verdict does change. The "ignored blowout quarter" fails its placebo in both strategies once the placebo comes from the same 129 names, so **the signal is abandoned**. S4 passes only in the same-pool re-run, which is post-hoc, so the frozen abandon stands.

**A better bar for this investor.** The KMI All Share index is total return. Bought with each deposit, it ends at Rs14.10m with no costs (Rs14.03m at 0.25% per side): TWR +14.2% a year, max drawdown -44.1%, worst 12 months -33.2%. Ratios to it: B0 0.88, B1 0.93, S2 1.01, S3 1.25, S4 1.17.

These ratios **understate every strategy**. The index has dividends throughout, while the strategies have them only from Nov 2024; on KSE100 the implied yield was 5 to 8 points a year. On a like-for-like basis, B0 and B1 are probably close to the index, and S2, S3 and S4 above it. That is an inference; it was not computed. Likewise, "only S3 beats KSE100" above is a total-return index against near-price-return strategies, not a fair test.

### 2. Post-mortem of S3, the best surviving strategy

S3 made Rs12.29m on Rs5.30m deposited. SAZEW made Rs6.32m of it and LUCK Rs4.48m (88% together). The ten worst trades lost Rs6.25m, and three of them (ECOP, CHCC, TGL, all sold on 1 Apr 2026) account for Rs5.15m.

**10 worst** (model at entry → outcome):

| Trade | Model saw | What happened | Class |
|---|---|---|---|
| ECOP 1 Oct 25 → 1 Apr 26, -43%, -Rs2.33m | EASING; Glass/pack/paper 6M +44%; EY 10.9%, ROE 23% | The Dec 2025 quarter swung to EPS -0.23 from +0.56. Price 69 → 55 (Dec) → 45 (Feb) → 35 (Mar). Sector EW -31%, KSE100 -6%. Sold after the regime flipped to TIGHT. | thesis wrong (earnings), then regime shock |
| CHCC 1 Sep 25 → 1 Apr 26, -27%, -Rs1.45m | EASING; Cement +52%; EY 13.0%, ROE 30% | Cement EW -21% while KSE100 rose 4%. Dec quarter EPS -11% YoY. | regime shock (sector reversal) |
| TGL 3 Mar 25 → 1 Apr 26, -17%, -Rs1.37m | EASING; Glass +42%; EY 14.6%, ROE 26% | Rose to 271 (Aug 2025), then fell to 194 (Oct) and 135 (Mar). KSE100 +39% over the hold. Dec quarter EPS -39% YoY. | thesis wrong (stock-specific) |
| ENGROH 1 Apr 26 → open, -4% | TIGHT; Fertilizer (frozen list); EY 17.4%, ROE 40% | -4% while KSE100 rose 7%. ROE 40% for a holding company suggests standalone and consolidated figures are mixed. | too early; possible data error (unverified) |
| OGDC 1 Oct 26 → open, -3% | TIGHT; E&P; EY 17.8% | 11 sessions | noise |
| OGDC 1 Feb 18 → 1 Apr 20, -40% | TIGHT; E&P; no value data (EW fallback) | Price 165 → 76. E&P EW -48%, KSE100 -33%. The 2018-19 bear market, then Covid and the oil crash. Sold at the trough when the regime flipped to EASING. | regime shock |
| PPL 1 Jan 18 → 1 Apr 20, -32% | NEUTRAL, then TIGHT; E&P | As OGDC. The 2018-19 bonuses in the window are gap-sized, error a few points at most. | regime shock |
| CSAP 2 Jun 25 → 1 Jul 25, -5% | EASING; Steel; EY 13.9% | The KMI deletion notice came out on 2 Jun 2025, the day of the buy; Shariah exit followed. | bad luck (rule interaction) |
| MARI 1 Feb 18 → 1 Apr 20, -17% | TIGHT; E&P | As OGDC | regime shock |
| MARI 1 Apr 26 → 1 Oct 26, -1% | TIGHT; E&P; EY 8.7% | Sold when a new annual result put its EY in the bottom half of the sector | noise |

No loss traces to a corporate-action artefact, and none to a confirmed data error.

**10 best:** SAZEW (1 Jan 24 → 1 Jan 25, +136% over four buys, price +496% from the first buy; NEUTRAL, Autos 6M +104%, EY 9.3%, ROE 41%. EPS went from 12.5 to 50.2 to 69.8 a quarter). LUCK (1 Oct 24 → 1 Apr 26, +85%, index +121%; EASING, Cement, EY 25.3%). SYS (+43%). OGDC 2021-24 (trade +6%, price +44%; the gap is the trim churn of 29 buys). ILP (+9%). FABL 2026 (open, +10%). PPL 2021-24 (+44%). LUCK 2024 (+18%). SNGP (+9%; index +37%). FABL 2023 (+13%). All ten are either the 2023-25 easing and rerating, or TIGHT-list E&P and banks during 2021-23. The two that matter are a car maker with a fourfold earnings jump and a cement leader through a 1,100bp cut cycle.

**What rule would have avoided the losses, and is it honest?**

- *A 25% trailing stop on core names.* Honest: it is S2's own pre-registered satellite rule. Variant 7E: S3 falls to Rs14.45m (1.164 vs 1.420) because the stop also cuts LUCK (a 33% dip mid-hold). **Rejected.**
- *Sell a core name when a new quarter shows EPS down YoY.* Honest: also S2's rule, and knowable at the filing. Variant 7F: S3 rises to Rs20.42m (1.644), but S4 falls to Rs15.81m and S2 moves from 14.17m to 15.10m. The sign flips between sister strategies, so it is not dependable. Keep it as a judgement flag, not a rule.
- *Skip names with a pending KMI deletion notice.* Honest and knowable, but worth about Rs0.1m.
- *Leave EASING on the first CPI uptick.* **Hindsight.** It is fit to the single 2026 episode and was not tested.
- *Hold 5 core names instead of 3.* Honest risk control, untested, and it would halve SAZEW too.

The large losses were sector reversals at a regime turn. Only a regime forecast avoids those, and the regime rule already reacted, a month after the damage. The concentration that caused them is the same concentration that produced SAZEW.

### 3. Calibration (headline trade log, closed trades; `walkforward_audit.txt` section E)

| Setup | n | Hit | Median | Middle 50% | Worst | Median hold | Versus a placebo |
|---|---|---|---|---|---|---|---|
| Random liquid KMI name, bought and held (B0) | 89 (+185 open) | 48% | -0.9% | -23% to +19% | -71% | 377 sessions | the base rate |
| Ignored blowout quarter (S2 satellite) | 38 | 58% | +2.6% | -8% to +21% | -43% | 107 | -0.12 pt vs own pool: **no edge** |
| Ignored blowout quarter (S4 satellite) | 41 | 56% | +2.0% | -9% to +27% | -43% | 101 | -1.10 pt: **no edge** |
| Top-EY name, ROE ≥15%, in a top-3 momentum sector (S2 value pick) | 38 | 66% | +5.6% | -7% to +22% | -54% | 65 | +1.8 pt vs same sector (70th pct): not significant |
| Same, in the regime sector set (S3 value pick) | 25 (+3 open) | 64% | +6.2% | -3% to +13% | -43% | 65 | +5.5 pt vs same sector (98th pct, lump sum, n 28) |
| Top-2 per regime sector (S4 value pick) | 33 (+4 open) | 61% | +3.8% | -3% to +19% | -41% | 65 | +0.1 pt (51st pct): no edge |
| Top-5 EY+DY across regime sectors (B1 value pick) | 77 | 66% | +8.5% | -9% to +40% | -54% | 65 | -2.2 pt vs same sector (8th pct): the gain is the sector, not the stock |
| EW of a momentum sector (S2, before value data) | 223 | 36% | -7.1% | -20% to +8% | -58% | 83 | worse than the base rate |
| EW of the EASING sector set, 2020 (S3) | 21 | 81% | +20.5% | +11% to +46% | -12% | 106 | **one episode** (Mar to Jul 2020) |

For PICKS.md: "An ignored-quarter setup paid off 56-58% of the time with a median of +2 to +3% over about five months. A random name from the same pool did as well. Treat it as a coin flip." "A cheap, high-ROE leader in a sector the regime or momentum favours paid off about 60-65% of the time, with a median of +4 to +9% over three to four months. Most of that is the sector. The stock pick adds 0 to 5 points, significant only in the 28-trade S3 sample, and contradicted by S4." Size every pick as at most a 60/40 bet.

### 4. Honest verdict

Yes, after costs and on the same survivor pool: S3 beats B0 by 35% and S2 by 9%. B1 ties (1.006), and S4 is abandoned under its frozen rule. Three qualifications:

1. The bar that matters to this investor is the cap-weighted KMI All Share index (total return), not B0. Against it, S3 is 1.25x and S2 1.01x. Both ratios are understated, because the strategies lack dividends before Nov 2024. On a like-for-like basis, S3 very likely beats the index by more than 25%, and S2 and S4 probably beat it too. B0 and B1 are about even with it (unverified until the dividend history is filled).
2. S3's margin is fragile. Its sector lists are in-sample, 88% of its profit is two stocks, and honest one-rule changes move it anywhere from 1.16x to 1.64x B0. It gave back most of its lead in 2026: 1.61x the KMI index on 31 Dec 2025, 1.25x on 16 Oct 2026, a -24.6% year so far against -3.5%.
3. No stock-level signal survives a fair placebo. The ignored quarter fails; value picks add nothing reliable inside a sector; sponsor buying is untested.

Would I bet the user's Rs50k a month on S3 as a system? **No.** I would bet it on staying fully invested in cap-weighted KMI exposure every month. That needs no skill and roughly matched B0 like for like. Lesson 13 says waiting costs more than any signal here earned. S3-style rotation would get at most a capped satellite, with a pre-registered review. That is what `knowledge/playbooks/strategy.md` sets out.

### Audit housekeeping

- Patch: `set_pool` and `POOL` (same-pool runs); `placebo(..., names=, rg=)` (own-pool placebo on its own random stream, so the headline placebo is unchanged); variants 7E and 7F (`cstop`); section 8 (pool bar, pool re-run, KMI All Share bar). Every number in sections 1 to 6 matches the builder's run. Text changes: two AUDIT placebo lines in section 5; the `insider_trades.csv` line ("EXISTS but this script does not parse it"); and the KSE100 label, now "total return", with the dividend note in the header line corrected.
- Another session committed an intermediate state of these files in `0220f06` (23:47): `walkforward.py` with section 8 but without variant F or the KMI bar, `walkforward_v0.py`, and an earlier `walkforward_trades_pool.csv`. The working tree holds the final versions. This audit committed nothing.
