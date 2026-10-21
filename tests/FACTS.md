# FACTS.md — headline numbers from every test (compiled 18 Oct 2026, verbatim quotes from the test files)

## Test table

| Test | Verdict | Key number | n or episodes |
|---|---|---|---|
| seed_audit | mixed: value "unproven"; sector momentum "weak"; stock and operator momentum "fails"; CPI turn "High" severity | Deep value E/P+DY "21.4 pts, 5/8" after fixes (claimed 27.9) | 71 names, 128 obs; CPI 33 months in 10 runs |
| refiner_steel_retrospective | weak | All-stock reaction rule, 60d median "-3.4%" vs placebo "-6.9%" | n=788 signals; 1 episode per named refiner and ASL |
| sector_momentum_regime | works (H1, "modestly"); H2 fails; regime tilt "no edge" | H1 primary net mean "+2.66%", net placebo p "0.001" | n=31.7 windows per offset; 6 cut episodes |
| commodity_pkr_sensitivity | fails (H1, H2); weak (H3) | Refinery 1m median "+5.92" (net "5.42") vs placebo p95 "4.03" | 7 Brent episodes; 11 H2 triggers, 5 macro episodes |
| flows_predict_sectors | fails ("final weekly-watch list: none") | Insurance rank IC "+0.045", t "+1.34" (best pre-registered) | 120 20-day periods; 40 60-day; H4 2 episodes |
| rate_cycle_episodes | weak | First cut, KSE100 120d median "+39.8%" vs placebo "+7.9%" | 2 cut cycles, 3 clusters, 3 hike cycles; H4 10 runs |
| index_recomposition_events | nothing | KMI30 additions ANN median "0.98" (mean "1.88") | 617 stock events; KMI30 adds 13 notices |
| calendar_effects | nothing (February "exploratory" only) | February EW mean "-3.95", median "-2.99" | 10 years per month; 72 MPC announcements |
| size_liquidity | weak | Most-liquid tercile "+3.1%" a year vs least "+8.4%"; t "-1.2" | 118 months; 10 years |
| value_timestamped | nothing | T1 net mean "-1.2" (2 of 4 positive, p "0.51") | 4 cohorts (Oct 2022 to Oct 2025) |

## Per-test facts

### 1. seed_audit
- Hypothesis: re-run of the orchestrator's seed findings (value, sector and stock momentum, operator footprints, IMF, CPI turn).
- Headline: value E/P+DY "21.4 pts, 5/8" after fixes (original "27.9 pts, 6/7, IC 0.30"); price only "13.4 pts, t=0.64"; sector-neutral "-1.3 pts". ROE/PB "47.5 pts, 7/8", corrected "45.9 pts, t=2.22 (ticker), 1.28 (cohort)". Sector momentum "3.31%, 67%, n=111". Stock momentum "n=1,239, median -1.3%, win 43%" vs placebo "median -1.5%, win 43%". Operator pump "n=675, 60d median -8.5%, win 35%" vs random days "60d median -2.9%". CPI falling "mean +45.6%, median 52.5%, n=33 months" vs flat "-3.6%".
- Verdict: value "goes from works to unproven" and "cannot be told apart from zero"; sector momentum "weak"; stock and operator momentum "no edge over random entry"; IMF "not detectable"; CPI turn "High" severity.
- Biggest caveat: data bugs (29 of 108 fundamentals names had no prices; no-trade-day zeroing; the corporate-action fix "cuts both ways") plus survivorship.

### 2. refiner_steel_retrospective
- Hypothesis: could a weekly catalyst watch have flagged the 2026 refiner and steel moves in advance.
- Headline: reaction rule, 60d, all stocks: "n = 788 (219 names), median -3.4%, mean +3.6%, win rate 45%, worst -64%", 6.1% above +50%. Placebo: "4,588 ... median -6.9%, mean -3.6%, win rate 36%, worst -80%", 3.5% above +50%. Entry 9 Jul to 16 Oct: PRL "+155%", NRL "+70%", ATRL "+34%", CNERGY "+37%".
- Verdict: weak ("Alone, the rule is a weak edge").
- Biggest caveat: one episode per name; the blowout-quarter leg has no measured odds (the "about 1 in 3" is labelled "My judgment, not a measured figure").

### 3. sector_momentum_regime
- Hypothesis: H1 top-3 sectors by 6m return beat bottom-3 over next 3m. H2 regime changes sector leadership. RT tilt rule.
- Headline: H1 primary 6/0/3m: "n 31.7", mean "+3.26%", median "+2.65%", win "65%", worst "-21.64%", net mean "+2.66%", net placebo "p 0.001", t "1.73". Offsets "+4.79%, +2.12%, +2.88%". H2 "D = +3.60%, p = 0.097". RT net minus benchmark: mean "+1.09%", median "+0.21%", win "51%", placebo p "0.255".
- Verdict: H1 "works, modestly"; H2 "not supported"; RT tilt "no edge".
- Biggest caveat: "about 2.25 of the 3.26 points come from the loser leg, which retail cannot short." Long-only top-3 minus benchmark nets "+0.70%"; net minus KMIALLSHR "-0.41%".

### 4. commodity_pkr_sensitivity
- Hypothesis: H1 after a Brent 3m rise of 20%+, refiners and E&P beat the market at 1/2/3m. H2 after PKR devaluation, exporters beat importers. H3 sector betas.
- Headline: H1 refinery 1m "n 7, median 5.92, net median 5.42, placebo p95 4.03, pctile 97"; E&P 1m "n 7, median -4.35, win 29". H2 spread 20d "n 11 (5 eps), median 1.22, net 0.22"; 60d "median -1.09, net -2.09". H3 passes: E&P on Brent "+0.94 pts, t 4.04, p 0.008"; Autos on PKR "-1.70 pts, t -3.32, p 0.008".
- Verdict: H1 "not supported"; H2 "not supported"; H3 weak.
- Biggest caveat: 7 episodes; refinery 1m median falls to "0.44" (pctile 72) when 2020-06 is also removed; the 2026-09 episode is "PENDING".

### 5. flows_predict_sectors
- Hypothesis: NCCPL net flows by investor group, scaled by sector traded value, rank the next 20/60 days of sector excess returns across 9 sectors.
- Headline: 20d rank IC: fipi "-0.001, t -0.03"; mutual funds "+0.028, t +0.90"; insurance "+0.045, t +1.34, placebo pctile 89.1"; banks/dfi "-0.037, t -1.00"; individuals "+0.018, t +0.51"; broker prop "-0.035, t -1.13". "All nine net top-3 spreads are negative (-0.78% to -0.08%)". H4: "2 episodes" ("ANECDOTE").
- Verdict: fails ("final weekly watch list: none").
- Biggest caveat: nine sectors make each IC noisy; survivorship and today's sector labels.

### 6. rate_cycle_episodes
- Hypothesis: H1 market rises after cuts. H2 first cut strongest. H3 first hike weak. H4 CPI fall of 1pt+ over 3m followed by +44% in 12m. H5 6M T-bill anticipates cuts. H6 sector returns after first cut persist.
- Headline: H1 first cut per cluster (n_eff = 3), KSE100 120d "mean +30.0%, median +39.8%, win 100%", placebo "+7.9% (-7.8 to +26.7)"; 60d "median +8.4%, win 67%, worst -9.4%". Dec 2025 cut 120d "+1.1%". H4 KSE100 250d "10 runs, mean +37.1%, median +52.3%" vs placebo median "+19.8%".
- Verdict: weak (H1 "weak"; H2 "anecdote"; H3 "weak"; H4 "weak as a 12-month rule"; H5 "weak as a lead"; H6 "not persistent at 120d").
- Biggest caveat: n=2 cut cycles, 3 clusters, 3 hikes ("no statistical power"); six of ten H4 runs sit in about two episodes.

### 7. index_recomposition_events
- Headline: KMI_ALL add ANN "152/17, mean 0.07, median -0.53, win 45.39, Pbo 0.21". KMI30 add ANN "60/13, mean 1.88, median 0.98, win 60.00, worst -15.77, Pbo -0.19". KMI_ALL delete POST "105/16, mean -1.49, median -3.04, win 34.29". MSCI_PK add PRE "22/9, mean 4.98" with ANN "-4.93".
- Verdict: nothing ("No dependable recomposition trade after 0.5% cost").
- Biggest caveat: price-gap zeroing is "not a verified split, bonus, or cash-dividend adjustment"; coverage patchy.

### 8. calendar_effects
- Headline: Month 02 EW "10/10, mean -3.95, median -2.99, win 10.00, worst -11.81, Pbo 0.66"; "February EW loses in nine of ten years". TOM EW "108/10, mean 0.90, median 1.03, win 62.96, Pbo 0.16". MPC POST EW "72/10, mean 0.84, median 0.72, win 58.33, Pbo 0.41".
- Verdict: nothing. February is "an exploratory calendar screen across twelve months, not a validated rule"; "No other calendar effect justifies delaying a Rs50k deposit."
- Biggest caveat: twelve-month screen raises false-discovery risk; TOM "gross advantage over same-year placebo is 0.74%, or about 0.24% after 0.5% cost."

### 9. size_liquidity
- Hypothesis: why the EW liquid basket (+44.1%) lagged KSE100 (+245.0%), 2017 to 2026; whether large liquid names beat small ones.
- Headline: traded-value terciles, per year "+3.1%" (most liquid) vs "+8.4%" (least liquid). "Top minus bottom: mean -0.45% a month ... t -1.2"; placebo 95% band "-0.51% to +0.52%". Quintile spread "-0.72% a month, t -1.7, placebo percentile 1.5%". "Top beat bottom in 3 of 10 years." KSE100 beat the EW basket in 8 of 10 years. Daily rebalancing costs about 24 points; monthly EW +68.1%, annual +79.0%, buy-and-hold +86.6%. KMI30 members EW from Jul 2020: +139.3% (+15.0% a year) vs liquid KMI All EW +99.2% (+11.6% a year), ahead in 5 of 7 years, t 0.9.
- Verdict: weak ("a weak effect (t about -1.2 to -1.9), not a proven small-cap premium").
- Biggest caveat: survivors only; sort is by traded value, not market cap, so "a true mega-cap premium is untested."

### 10. value_timestamped
- Headline: cohorts Oct 2022 to Oct 2025 (4). T1 net mean "-1.2", median "-2.2", "2 of 4" positive, p "0.51". T2 (within sector) net mean "+13.0", median "+2.4", "2 of 4", p "0.17". T4 (within top-half momentum sectors) net mean "+21.7", "4 of 4", p "0.10" (outside the verdict rule, flips negative in both sensitivities).
- Verdict: nothing ("Nothing.").
- Biggest caveat: 4 episodes; 108 names chosen on today's liquidity; the T2 mean "comes mostly from Oct 2023 (+58.4)".

## Sector ranking (knowledge/sectors/README.md, 17 Oct 2026)

| # | Sector | Catalysts next 3 months | 6m rel. to KMI, full / core (pts) | Valuation vs own history | Fit with a hike-pricing curve | Verdict |
|---|---|---|---|---|---|---|
| 1 | E&P | Mildly positive | -3.5 / -3.5 | P/E 5.3-6 on EPS flattered by a one-off tax reversal; lagged KSE by 32 pts in 2025 | Good. Outperformed in 3 of 3 first-hike windows (+4, +9, +1) | Overweight |
| 2 | Fertilizer | Neutral to mildly positive (FFC) | -4.4 / -4.4 | FFC 8.8x consolidated, 7.3% yield | Good. +12, +21, -2 in the three hike windows | Overweight, FFC only |
| 3 | Islamic banks | Mildly positive | +23.6 / -1.4 | MEBL P/B 3.3, fair; BIPL P/B 0.56 | Best. +22, +4, +1 | Overweight, MEBL core |
| 4 | OMC | Mildly positive, low conviction | +14.1 / +1.0 | PSO P/B 0.59 vs 0.31 at the FY24 trough | Poor. 100bp costs PSO about Rs3.8bn pre-tax | Overweight, PSO satellite |
| 5 | Tech | Neutral to mildly positive | -13.5 / -14.3 | SYS 15x TTM; NETSOL P/B 0.8, 4.6x | Poor for SYS; NETSOL too cheap to care | Overweight, NETSOL only |
| 6 | Gas utilities, misc | Event-driven (SNGP) | +1.6 / -13.1 | SNGP 3.9x near 12-month low | Poor | Neutral, small SNGP event bet |
| 7 | Power | Flat to mildly negative | +1.6 / -15.1 | HUBC 5.1x vs 3.0x at the 2023 trough; 10% yield | Mixed | Neutral, HUBC as ballast |
| 8 | Glass, packaging | Neutral to slightly negative | +15.0 / -1.2 | TGL, GHGL near book at 5-7x | Glass net cash fine | Neutral, GHGL the one long |
| 9 | Refineries | Mixed to mildly negative | +98.4 / +98.4 | Re-rated about 2x vs KSE since June | Neutral; cracks dominate | Neutral, hold, no new entry |
| 10 | Food, staples | Mixed, stock-specific | -0.6 / +11.4 | FCEPL +89% since March | Neutral | Neutral |
| 11 | Autos | Mixed, negative skew | +6.1 / +13.0 | SAZEW 3.9x at a 52-week low, HCAR -34% | Worst. Volumes swing 2x on financing cost | Neutral until 26 Oct |
| 12 | Cement | Neutral to mildly negative | -0.8 / -2.2 | 14-33% below 2-year highs, P/E 7-12 | Poor | Neutral |
| 13 | Steel | Neutral to mildly negative | +5.3 / +4.0 | Lagged the market 45 pts since May 2024 | Poor. Leveraged | Avoid |
| 14 | Pharma | Neutral to slightly negative | -10.1 / -11.3 | Sector -25% since Sep 2025, P/E 10-12 | Poor. -7, -5, -11 in the three hike windows | Avoid |
| 15 | Textiles | Negative | +40.6 / -1.4 | Ratio to KSE 0.68 vs 1.18 in 2023 | Poor. Leveraged, energy-squeezed | Avoid |
| 16 | Chemicals | Negative | +8.3 / -10.4 | Chem index 0.82 vs market against 1.56 in Jan 2024 | Poor. EPCL net debt Rs40bn | Avoid |

## Deals (knowledge/playbooks/deals.md)

| Rank | Deal | KMI | Expected exit | Odds | Horizon | Expected annualised | Note |
|---|---|---|---|---|---|---|---|
| 1 | EPCL tender | Yes | 32.9 to 33.8 | 70% | about 4 months | about 9% (range 3% to 18%) | Best case needs 70% acceptance |
| 2 | NICL (CHCC bid) | No | about 268 (unverified) | 60% | 6 to 9 months | about 0% | No spread at the implied price |
| 3 | SBL (Najd) | No | unknown | 60% | 3 to 6 months | n/a | SPA price undisclosed |
| 5 | ASC | Yes | unknown | low | ? | n/a | Suspended by SECP |

Base rate, 11 completed offers 2021 to 2026: premium to pre-announcement price median +40% (4% to 125%); spread the day before the public offer median 14.7%; days from intention to payment median 302 (96 to 449); price 1 month after completion vs offer median -13% (3 of 11 above); 6 months -14%; 6-month return relative to KSE100 -12% (2 of 11 positive); offers filled or oversubscribed in 6 of 9, undersubscribed in 3 (LOTCHEM 30%, RMPL 73%, SHEL 70 to 100%).

## Holdco discounts (knowledge/playbooks/holdco_discounts.md, 16 Oct 2026)

1. JSCL 41.6%, not KMI. 2. ENGROH 48% on Topline's DCF but 9% on market multiples, KMI. 3. ATRL about 21%, KMI, multiple-based. 4. OGDC about 19%, KMI, multiple-based. 5. POL 8%. 6. FFC 3%. 7. LUCK about 0. PSO and HUBC unranked.

## Catalyst-trade verdict (knowledge/playbooks/catalyst_trade.md)

"The refiners were flaggable as a 'loaded spring' from 29 Apr and as a trade from 8-9 Jul. Their size was luck: a war restarted. ASL was flaggable on 9 Apr from public sponsor filings. We missed both because we had no watch for ignored earnings or for sponsor buying, and because a sector-momentum filter puts a sector on the radar only after the move." Signals to watch: ignored blowout quarter; crude and inventory direction; product cracks and GRM; other sector spreads; policy pipeline (ECC, cabinet, CCoE); regulated-price resets (OGRA, NEPRA); trade protection (NTC); sponsor and insider buys; volume ignition; PSX unusual-movement letters. "Treat the signal list as a watch design, not a tested model."


## Added 18 Oct 2026

| Test | Verdict | Key number | n or episodes |
|---|---|---|---|
| quality_within_sector | weak ("Weak, not proven.") | Top minus bottom median "+5.8", placebo "p = 0.054" | 26 formations, 3 annual episodes |
| insider_cluster_buying (run 2) | not supported ("Still not supported.") | H1 cluster 63 sessions median "-0.4%", p "0.473" | 37 H1 cluster events, 17 symbols |
| fixed_capital_runs | no 3x ("no pre-registered rule set would have") | S3 "1.36x" vs B1 "2.00x" from 1 Oct 2024; KMI TR "1.81x" | 6 start dates; 14 S3 trades |
| oracle_and_good_case | nothing reached 3x; breakout "a hypothesis from five windows" | S4 "2.38x", S3 "2.12x" (literal window); oracle "265x" | 8 systems, 5 windows plus literal; 200 random paths |
| winners_case_control | not predictable ("does not support fast rotation") | Top-decile precision "5.82% (32 of 550)" vs base "4.51%"; placebo median "5.91%" | 129 events, 83 sector episodes |
| active_trading_codex | suggestive | HIGH52 "2.62x" (2024-26), "3.34x" (2020-22), "0.89x" (2016-18) | 7 rules, 5 cohorts, 200 random paths |
| system_walkforward post-mortem | "No" (S3 as a system); earnings signal "abandoned" | S3 "1.353" vs same-pool B0' | 132-name pool; 38 S2 satellite closed trades |
| system_walkforward like-for-like | "B2 does not beat B0 or the index." | B2 accrued ratio to KMI TR "0.86" | 106 deposits, Rs5.3m; 456 survivor names |
| deals.md base rate, complete set | about 50% at the PAI, "about 90% or better after the PAO" | Completion "27 of 56 resolved PAIs (48%)" | 75 PAIs (53 targets); 56 resolved |

### 11. quality_within_sector
- Hypothesis: within a sector, higher-quality names (ROE, cash conversion, EPS stability, dividend cover) earn higher 12-month returns; quality plus cheapness beats the EW liquid KMI basket.
- Headline: n = 26 formations. "Top minus bottom | +9.2 | +5.8 | 69% | -33.2" (mean, median, win, worst). "QARP minus EW liquid KMI | +4.1 | +2.4 | 54% | -22.2". Placebo "p = 0.054."
- Verdict: weak ("Weak, not proven.")
- Biggest caveat: "Three episodes. Everything is inside one rerating regime."

### 12. insider_cluster_buying (run 2, full universe)
- Hypothesis (H1): a second distinct insider buying in the open market within 30 days predicts outperformance over 21, 63 and 126 sessions.
- Headline: H1 cluster, 63 sessions, net: n 37, 17 symbols, mean "+2.6%", median "-0.4%", win "46%", p "0.473". Out of sample median "+5.0%", p "0.137". H4 single sales, 21 sessions: "137, -3.1%, 0.006".
- Verdict: not supported.
- Biggest caveat: "Extraction recall is about 60%, and 37% of PDFs give no row." "The top 3 events sum +192% against a total of +95%."

### 13. fixed_capital_runs
- Question: would Rs50,000 deposited once have tripled under the frozen rules, from six start dates.
- Headline, from 1 Oct 2024: "S3 regime | 67,855 | 1.36x"; "B1 orchestrator | 100,041 | 2.00x"; "KMI All Share TR | 90,375 | 1.81x"; placebo "median 1.44x". "No strategy reached 3x."
- Verdict: "over two years, no, and no pre-registered rule set would have."
- Biggest caveat: "Cash dividends are complete only from Nov 2024."

### 14. oracle_and_good_case
- Question: what Rs50,000 could have become, per 2-year window, under perfect foresight and under eight systems fixed before looking.
- Headline, 17 Oct 2024 to 16 Oct 2026: "S4 ... 2.38x, S3 ... 2.12x, equal-weight top-10 liquid 1.82x, KMI All Share buy and hold 1.74x (Rs86,860). Nothing reached 3x." Perfect foresight "265x" with a 1% cap, "2,099x" without.
- Verdict: the breakout rule S3 ranked 1, 1, 1, 3, 1 across windows; "a hypothesis from five windows."
- Biggest caveat: "The windows overlap and the last two share one bull run: really five observations."

### 15. winners_case_control
- Question: could the 129 six-month doublers of 2017 to 2026 be seen at the start from public data.
- Headline: "Base rate | 1.72% | 4.51%" (train, test). "Top-decile precision | 4.11% (in-sample) | 5.82% (32 of 550)". "Shuffled-label placebo, top-decile precision | median 5.91%". Doublers 2.5 to 2.8 times more common when the 6-month T-bill sat below the policy rate.
- Verdict: "This test does not support fast rotation into big winners picked on start-of-move features."
- Biggest caveat: "There is no correction for testing 27 features."

### 16. active_trading_codex (independent implementation)
- Method: seven frozen rules (MOM63, MOM252, HIGH52, DIP200, SECTOR63, VOL20, EPS_YOY), five two-year cohorts, 200 random rotation paths each.
- Headline: HIGH52 "0.89x | 1.08x | 3.34x | 2.09x | 2.62x" (2016-18 to 2024-26). 2024-26 HIGH52: "130,953", "-35%" drawdown, "53" trades, "62%" hit, "+4.6%" median trade, "95th" percentile. Random paths "mean 1.53x, median 1.42x".
- Verdict: suggestive.
- Biggest caveat: "the panel omits delistings, older dividends are missing and historical membership was reconstructed."

### 17. system_walkforward: post-mortem and audit (Opus)
- Headline: "S3 | 1.420 | 1.353 | 1.324" (frozen vs B0, vs same-pool B0', same-pool re-run). "S2 satellite, placebo from its own pool | +0.42 pt | -0.12 pt (fails)". "S4 satellite ... -1.10 pt (fails)".
- Verdict: "Would I bet the user's Rs50k a month on S3 as a system? No." The ignored-quarter signal "is abandoned."
- Biggest caveat: "Every value pick and every earnings signal comes from names that were liquid in 2026" (132-name pool).

### 18. system_walkforward: like-for-like benchmarks and cap-weighted core
- Headline, accrued dividends, 16 Oct 2026: "B2 | 12.15m", "B2-EW | 12.66m", "S3 | 18.60m", "KMI All Share TR | 14.10m". B2 to KMI TR "0.86".
- Verdict: "B2 does not beat B0 or the index."
- Biggest caveat: "The accrual is an estimate and is incomplete."

### 19. deals.md: base rate, complete set
- Headline: "Completion: 27 of 56 resolved PAIs (48%)." Buy the day after the PAI, all resolved: "54 | +7.2% | -1.2% | 48%". Completed only: "27 | +18.5% | +8.0% | 63%".
- Verdict: "the odds are about 50% at the PAI and about 90% or better after the PAO."
- Biggest caveat: unknown outcomes for 12 PAIs: "27 of 68 non-pending (40%)" if failures, "57%" if completions.

## Added 18 Oct 2026, evening

| Test | Verdict | Key number | n or episodes |
|---|---|---|---|
| noise_map_shock_rebound | REPRICES geopolitical on day 1 and gives it back; SBP, budget, rating, rupee, IMF and political headlines ignored on day 1; buy the crash only on a known trigger | index 5%+ below pre-event close: 20s median "+4.2%", win "78%", against random close "+1.1%" and "57%" | 9 trades (trigger); 25 clustered shocks; 157 events |
| volume_ignition_upper_locks | V1 and V2 nothing; V3 nothing; V4 watch, not tradable; the 20% stop paid, the volume signal did not | liq5 trail20 V1 median "-13.0", win "27", placebo median "-6.9" | 248 V1 trades (36 quarters) |
| corporate_events | nothing for most sub-types; E2b split watch; E6 rights issue avoid | E2b KMI 60 sessions median "+13.9%" (win "89%", worst "-13%"); E6 median "-9.1%" at 60 sessions | E2b 9 KMI (19 events in 3 years); E6 76; E3a 526 |
| results_gap_and_policy | R(a) watch; R(b) nothing; R(c) nothing as an entry rule; P none reliable | R(a) 60d median "+16.6%", win "81%", matched "+10.0%" (p 0.11) | 37 (14 entry quarters); P 22 events |
| compounders | population watch; picking the 3x name nothing; growth-core rule nothing | pooled 3x share "12.1%" (58 starts); 3y rule "0.88x (-11.7%)" vs KMI TR "0.96x" | 58 starts; 155 liquid names (decade); 1.04 years for the registered 3y rule |

### 20. noise_map_shock_rebound
- Hypothesis: which event types PSX ignores and which it reprices, and whether buying a shock and rebound is measurable at a trigger known at entry.
- Headline: "Buying a market already 5% below its pre-event close earned +4.2% at 20 sessions with a 78% win rate, against +1.1% and 57% for a random close." Geopolitical: "the median fall was -9.0%, the 20-session rebound +13.2% and the 60-session rebound +27.8%".
- Verdict: REPRICES for geopolitical and Covid; ignored for SBP, budget, rating, rupee, IMF and political on day 1. "The direction is right and the sample is small."
- Biggest caveat: "67 of 157 dates are recalled, not re-verified"; 9 trigger trades; event clusters overlap (Covid counted four times).

### 21. volume_ignition_upper_locks
- Hypothesis: joining a stock on heavy volume and upper-lock closes, then leaving on a 20% trailing stop, pays after costs and beats random entries with the same exit.
- Headline: liq5 trail20 V1 "248 (36) | 0.0 | -13.0 | 27" with placebo "-6.9 / +9.8". "Net mean +9% to +13% under the stop with a 12% chance of a +50% trade, but the median is -9%, win rate 35%" (V4).
- Verdict: V1 and V2 nothing; V3 nothing; V4 "watch, not tradable". "The stop paid; the volume signal did not."
- Biggest caveat: "The 2023 to 2025 rally supplies most positive means"; 32 to 38 quarters is "closer to 3 or 4 regimes"; no news content.

### 22. corporate_events
- Hypothesis: announcements that change ownership, management or funding, or that the exchange flags, leave a measurable edge when bought on the next session (E1a to E7).
- Headline: "median +13.9% at 60 sessions on 9 KMI events (89% win, worst -13%)" (E2b). "median -9.1% at 60, -15.4% at 120, win 28% to 33%" (E6). E4a "worse than matched entries (p 1.00)".
- Verdict: "No corporate event is tradable on this evidence." E2b watch; E6 avoid; the rest nothing.
- Biggest caveat: titles only, no document bodies; "the sample is 19 names in three years, and eleven of them sit in the 2025 bull run."

### 23. results_gap_and_policy
- Hypothesis: R, a results day the market rewards hard keeps drifting, so buying the next close is tradable; P, a sector policy or regulated-price event leaves a window after its first public date.
- Headline: "The 60d median (+16.6%, win 81%) is +11.9 points over any result and +6.5 over matched random entries, not significant (p 0.11), and gone at 120d."
- Verdict: R(a) watch; R(b) nothing; R(c) nothing as an entry rule; P "None reliable."
- Biggest caveat: "Fourteen quarters, one year doing most of the work, 2025 flat."

### 24. compounders
- Hypothesis: (A) a measurable base rate of 3x over five years among liquid PSX names; (B) start-of-window features separate winners; (C) a pre-registered growth-core rule beats KMI All Share TR and the EW liquid basket.
- Headline: "pooled, 58 starts | 108 avg | 24.7% | 12.1%" (3x share). "3y growth, 2025-09-30 | 1.04 | 0.88x (-11.7%) | 0.96x | 0.88x".
- Verdict: population Watch; picking the 3x name Nothing; growth-core rule "Nothing: 1.04 years, 0.88x vs 0.96x".
- Biggest caveat: "The pre-registered test is not runnable: five years of growth data do not exist in the repo"; every window sits in one 2020 to 2026 re-rating.
