# Strategy candidates for the walk-forward backtest (pre-registered)

Frozen 2026-10-17, before any system backtest. Evidence: `tests/seed_audit.md`, `tests/out/sector_momentum_regime.txt`, `tests/calendar_effects.md`, the catalyst, rotation and practitioner playbooks, `sector_map.md`, `seed/PSX_STATE`. Implement exactly. Log any deviation in `DECISIONS.md` and report both the frozen and the deviating result. Nothing here changes after a result is seen.

## 0. Rules common to every strategy

**Calendar.** Form at the last close of month t using only data timestamped by then. Trade at the first close of month t+1, when the Rs50,000 deposit also arrives: Jan 2018 (formed 29 Dec 2017) to Oct 2026, 106 deposits, Rs5.30m. Value at the 16 Oct 2026 close. No calendar timing.

**Universe U(t).** A name must pass two tests:
1. It is a KMI All Share member at t. Start from the latest `data/index_members/KMI_ALL*.csv` list dated on or before t, then apply the `data/index_changes.csv` rows with `index=KMI_ALL` whose `effective_date` is on or before t. Before 28 Jan 2019, use `KMI_ALL_derived_2019-01-28.csv` (an approximation; flag it).
2. Its median daily traded value (close times volume) over the 60 sessions strictly before t is at least Rs5m, with 40 or more traded sessions. This is `scripts/prices.py: liquid_universe`.

Sector labels are the screener codes mapped as in `scripts/tests/sector_momentum_regime.py` (U3 table). A sector is eligible if it has 3 or more names in U(t).

**Returns.** Total return via `prices.returns(method="adjusted", actions=provisional_actions())`, dividends reinvested, net of 15% withholding where known. Never add DY on top (lesson 19). Fractional shares allowed.

**Costs.** 0.25% per side (0.5% round trip) on every rupee traded, including each deposit's investment. KSE100 benchmark: no costs.

**Shariah exit (all strategies).** A holding removed from KMI All Share is sold at the first trade date after its `effective_date`.

**No cash.** Every deposit is invested on arrival. An empty sleeve's money goes to the core, or to EW U(t) if the core is empty too.

**Deposit allocation.** Each deposit goes to the names furthest below target weight, minimum ticket Rs5,000. No selling to rebalance, except: a name above 35% of the book at a month end is trimmed to 25%.

**Value inputs.** `sa_ratios.csv` fiscal-year rows only. A row is usable from the first close after that year's `financial_result` announcement in `data/announcements.csv`, else fiscal year end plus 4 months (lesson 18). Drift-adjust: EY_t = (P_FYE / pe) / P_t, likewise DY. Names without a row cannot be value picks. Rows start at FY2020, so until the first month with 15 or more value-eligible names in U(t) (about Oct 2020), value selections fall back to EW of the chosen sectors' liquid names. Report the full period and from that month.

**Statistics**, per strategy, per sleeve, and for KSE100 (`data/macro/kse100.csv`, price only) and EW U(t) (monthly rebalanced, same deposits and costs):
1. CAGR of the time-weighted unit value, plus money-weighted IRR.
2. Max drawdown of the daily unit value.
3. Worst rolling 12 months (month-end values).
4. Hit rate per trade. A trade runs from first buy to full exit; return = (proceeds + dividends) / cost − 1, net. Open trades are marked at 16 Oct 2026 and reported separately.
5. Median trade, with n, mean and worst.
6. Rs value of the deposits at each 31 Dec 2018-2025 and at 16 Oct 2026: strategy, KSE100, EW KMI, and the gaps.
7. Splits 2018-2021 and 2022-2026 (the rerating, lesson 9).
8. Turnover and average names held.

**Satellite placebo.** 1,000 sets of random U(t) names on the same entry dates with the same exits. Report median trade minus placebo median (lesson 15). At 0 or below, the signal is abandoned whatever the strategy does.

## B0. Naive baseline: buy the market, never sell

(a) U(t). (b) No regime. (c) All sectors. (d) All of U(t). (e) Each deposit split equally across U(t), no minimum ticket. (f) Shariah exit only. (g, h) Common.

Abandon: never. B0 is the bar.

## B1. The orchestrator's model (value plus regime, as in PSX_STATE)

- (a) Universe: U(t).
- (b) Regime. Take the latest 6M cut-off on or before t (`data/macro/tbill_auctions.csv`, `y6m`, auction `date`) and the latest policy rate on or before t (`policy_rate_decisions.csv`, `rate`, announcement `date`).
  - HIKE-PRICING: 6M at least 50bp above policy.
  - CUT-PRICING: 6M at least 50bp below policy.
  - NEUTRAL: anything in between.
- (c) Sectors. HIKE: Autos, Islamic banks, Power. CUT: Fertilizer, Pharma, Cement, OMC. NEUTRAL: all eligible sectors. (PSX_STATE item b; `sector_momentum_regime.py` `HIKE`, `CUT`.)
- (d) Stocks: the top 5 by EY + DY (drift-adjusted, ranked across the allowed sectors, not within sector, as the orchestrator did).
- (e) Sizing: 5 names, 20% target each, 25% cap. Deposits go to the name furthest below target.
- (f) Exits. Quarterly review at the end of Mar, Jun, Sep and Dec. Sell a name if it falls out of the top 10 by EY + DY, or if a regime change removes its sector. No price stops.
- (g, h) As common.

Abandon B1 if its rupee value at 16 Oct 2026 is below B0's (ratio under 1.00).

## S2. Momentum core plus ignored-quarter satellite (no regime)

- (a) Universe: U(t).
- (b) Regime: deliberately none. This isolates what S3 and S4 gain from regime.
- (c) Sectors: the top 3 eligible sectors by 6-month (126-session) EW total return to t. The 6/0/3 variant is LS-supported in `sector_momentum_regime.txt`, but long-only top 3 vs KMIALLSHR had no edge (net median −2.2%); this tests whether in-sector value fixes that. No catalyst veto: `catalysts/catalyst_calendar.csv` starts in 2026, so no point-in-time flag exists for 2018-2025.
- (d) Stocks.
  - Core: in each chosen sector, the top name by drift-adjusted EY, among names with lagged ROE of at least 15%. That gives 3 names. For banks, rank by ROE/PB instead (lesson 6).
  - Satellite, "ignored blowout quarter":
    - Quarterly EPS comes from `financial_result` filings in `data/announcements.csv`. Use consolidated figures where reported. Single-quarter EPS is cumulative EPS minus the prior cumulative.
    - A signal requires EPS_q / EPS_q−4 − 1 of at least +50% with EPS_q−4 > 0, or a swing from loss to profit with EPS_q > 0.
    - In the 20 sessions after the first close following the filing datetime, the stock must be within ±5% of the EW U(t) return ("flat vs market").
    - The signal is live from session 20. Enter at the next trade date. If several signals are live, rank by 4 × EPS_q / P.
    - Prerequisite: these EPS series must be parsed from the filing PDFs. In any year where fewer than 70% of liquid KMI name-quarters are parsed, report the satellite for that year as "uncovered". Do not substitute another signal.
- (e) Sizing: core 3 names × 16.7%; satellite up to 4 names × 12.5%.
- (f) Exits.
  - Core: reviewed quarterly. Sell a name when its sector leaves the top 3, or when a new annual result drops its EY into the bottom half of its sector.
  - Satellite: time stop at 120 sessions. Thesis breaker: the next quarterly filing shows EPS YoY below 0. Trailing stop: close 25% below the highest close since entry, sold at the next trade date. No profit target.
- (g, h) As common.

Abandon S2 if its 16 Oct 2026 rupee value is under 1.05 × B0.

## S3. Regime rotation core plus sponsor-buying satellite

- (a) Universe: U(t).
- (b) Regime, from `sector_rotation.md`, without SPI (there is no SPI series). CPI is usable only once released: at the month end t, the latest usable print is month t−1 (`cpi.csv` `month`, `yoy`).
  - EASING if either (i) CPI YoY fell in each of the last two usable prints and `y6m` was below the policy rate at each of the last two auctions, or (ii) the last decision was a cut and the latest `y6m` is no more than the policy rate + 50bp.
  - Leave EASING if `y6m` reaches policy + 50bp or more, or CPI YoY rises for two prints.
  - TIGHT if the latest `y6m` is at least policy + 50bp, or there was a hike within the last 6 months.
  - NEUTRAL otherwise. If EASING and TIGHT both hold, EASING wins (the pre-cut trigger is meant to fire before the cut).
- (c) Sectors.
  - TIGHT: Islamic banks, E&P, Fertilizer.
  - EASING: Autos, Cement, Steel, Glass/pack/paper, Textiles, OMC, Tech. The top 3 of these by 6-month return are used.
  - NEUTRAL: the top 3 by 6-month return across all eligible sectors.
  - These lists were read off the 2018-2026 windows themselves, so S3 is partly in-sample. Treat its result as an upper bound.
- (d) Stocks.
  - Core: as in S2. One name per sector; in TIGHT, the three sectors give the three names.
  - Satellite, "sponsor buying": parse the `insider_trade` filings in `data/announcements.csv` (the `direction` column is mostly `unknown`, so the PDFs must be read). A signal is 2 or more distinct buy filings within 120 calendar days by a director, CEO, sponsor, substantial shareholder or associated company (executive-only buys do not count, lesson 11), with no insider sell filing in the same window. The signal date is the second filing's `datetime`; entry is at the next trade date.
- (e) Sizing: core 3 × 16.7%; satellite up to 4 × 12.5%.
- (f) Exits.
  - Core: reviewed quarterly. Also sell at the first month end after a regime change if the name's sector is no longer in the set.
  - Satellite: time stop at 250 sessions. Breaker: any insider sell filing in the name. Trailing stop: 30% below the high close.
- (g, h) As common.

Abandon S3 if its 16 Oct 2026 rupee value is under 1.10 × B0.

## S4. The full model: regime plus within-sector value plus both catalyst signals

- (a, b, c): as S3.
- (d) Core: the top 2 names per chosen sector by drift-adjusted EY, ROE of at least 15% (banks by ROE/PB), capped at 4 names. Satellite: the S2 and S3 signals pooled. When both fire on one name, it gets one position.
- (e) Core 4 × 12.5%; satellite up to 4 × 12.5%.
- (f) Core exits as S3; satellite exits as each signal's own rule.
- (g, h) As common.

Abandon S4 if its 16 Oct 2026 rupee value is below the better of S2 and S3 (ratio under 1.00).

## Five lookahead sources the implementer must avoid

1. **`seed/data/fundamentals/sa_ratios.csv`, columns `date`, `pe`, `pb`, `dividendyield`, `peForward`, and the `TTM` rows.** `date` is fiscal year end, not publication (a quarter of June-year-end names report in October, lesson 18). `pe` uses the FYE price, embedding 3+ months of later drift (seed audit). `TTM` is as of 2026; `peForward` leaks (lesson 4). Gate rows on the `financial_result` `datetime`. The 108 names were picked on 2026 liquidity (survivorship; flag it).
2. **`data/macro/cpi.csv`, column `month`.** Reference month; PBS publishes on the 1st or 2nd working day after. Month t CPI at the month-t close is lookahead (the seed audit's CPI-trigger flaw). Use t−1. Skip `mom` (starts 2021-06); 2026-09 `yoy` is unverified.
3. **Index membership: `data/kmi_allshare_2026-06-05.csv`, `seed/data/fundamentals/screener_20261016.csv` column `listed_in`, and `data/index_members/KMI_ALL_derived_*.csv`.** The first two are 2026 snapshots. Derived lists are rolled back from 2026, so names that left earlier are missing (lists sit 0 to 7 above notice totals). Switch on `index_changes.csv` `effective_date`, drop `source_url = derived`, map BYCO/CNERGY, ENGRO/ENGROH, ICI/LCI.
4. **Current-snapshot sector and screen data: `seed/data/macro/sector_monthly_ret.csv` and `ew_mkt_ret.csv` (all columns), `seed/data/fundamentals/universe_scored.csv` (`sector`, `adv_m`, `chg1y`, `score`), and `data/symbols.csv` `sectorName`.** Baskets are today's leaders picked with hindsight; `adv_m`, `score` are 16 Oct 2026 values. Build sector returns from U(t); never filter or rank on `universe_scored.csv`.
5. **`data/announcements.csv`, column `datetime`, and the dates inside the filing PDFs.** A filing after the 15:30 PKT close counts from the next session. Insider letters show a transaction date before the filing; signal on the filing `datetime`, never the PDF trade date. Quarterly EPS dates to the filing, not the period end.

Not lookahead, but report it: `data/panel_close.parquet` holds only the 456 symbols listed on 16 Oct 2026, so every EW figure, B0 included, is biased up.
