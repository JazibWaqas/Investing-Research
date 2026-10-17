# The strategy the evidence supports

Evidence date 17 Oct 2026, data to 16 Oct 2026. Sources: the "Post-mortem and audit" section of `tests/system_walkforward.md`; `tests/out/system_walkforward.txt`, sections 7 and 8; `tests/out/walkforward_audit.txt`. The pre-registered rules in `strategy_candidates.md` are unchanged. Review when the sponsor-buying data is complete or after 24 live months.

## Bottom line

Stay fully invested every month in cap-weighted KMI exposure. That is the only result that needs no skill and survives every check. Active rotation gets a capped satellite with a fixed review date.

106 monthly deposits of Rs50,000, Jan 2018 to Oct 2026 (Rs5.30m in total), were worth this on 16 Oct 2026:

| Plan | Value |
|---|---|
| KMI All Share index (total return, no costs) | Rs14.10m |
| B0, equal weight of liquid KMI names | Rs12.42m |
| B1, value plus regime | Rs13.11m |
| S2, momentum sector plus value | Rs14.17m |
| S3, regime sectors plus value | Rs17.63m |

The strategies include dividends only from Nov 2024, so they are understated against the index (KSE100's implied yield was 5 to 8 points a year). Like for like, B0 and B1 are probably level with the index and S2 and S3 above it. That is an inference, not computed.

S3 is the best surviving strategy, at 1.35x B0 after the survivorship fix. That edge is soft:

- Its sector lists were read off the test period.
- Two stocks, SAZEW and LUCK, made 88% of its profit.
- Honest one-rule changes move it from 1.16x to 1.64x B0.
- It fell 24.6% in 2026 to date, against -3.5% for the index.

No stock-level signal survived a fair placebo. The ignored blowout quarter fails, value picks track their sector, and sponsor buying is untested.

## Rules

1. **Deposit and invest on the first trading day of every month.** Never wait in cash for a setup (lesson 13).
2. **Core, at least 70%: cap-weighted KMI exposure.**
   - Option one: a fund or ETF that tracks a KMI index. Availability, fees and tracking error are unverified here; check them first.
   - Option two: hold the 10 to 15 largest liquid KMI All Share names near index weight. Not yet backtested.
   - Buy and hold. Send each deposit to the names furthest below target.
   - Sell a name only when a deletion notice shows it is leaving KMI All Share.
3. **Satellite, at most 30%: S3 as frozen.**
   - Regime comes from the 6-month T-bill against the policy rate, plus the last two CPI prints.
   - TIGHT: Islamic banks, E&P, Fertilizer.
   - EASING: the top 3 by six-month return of autos, cement, steel, glass/packaging, textiles, OMC and tech.
   - NEUTRAL: the top 3 eligible sectors.
   - In each sector, buy the highest drift-adjusted earnings yield with ROE of at least 15% (banks: ROE/PB).
   - Review quarterly. Sell when a regime change removes the sector.
   - At most 3 names, each at most 12% of the total book.
   - Skip names with a pending KMI deletion notice.
   - Treat a quarter with EPS down year on year as a prompt to re-check, not an automatic sale. As a rule it helped S3 and hurt S4.
   - Dated catalyst trades from `PICKS.md` count inside the 30%, each sized as at most a 60/40 bet.
4. **No stop-losses.** A 25% trailing stop on S3's core cut its final value from Rs17.6m to Rs14.5m, because it also stopped out LUCK.
5. **Fixed review.** Every six months, compare the satellite's time-weighted return with the KMI All Share index. If it trails by more than 10 points after 24 months, fold it into the core. Change no rule because of a result. Log every change in `DECISIONS.md`.

## Expected range of outcomes

History from 2018 to 2026, not a forecast:

| | Deposits multiplied | CAGR | Max drawdown | Worst 12 months |
|---|---|---|---|---|
| KMI All Share index | 2.66x | +14.2% | -44% | -33% |
| S3 | 3.33x | +19.2% | -50% | -42% |
| B0 | 2.34x | +10.1% | -61% | -51% |

The path was very uneven:

| | 2018 to 2021 | 2022 to 2026 |
|---|---|---|
| KMI All Share index | +2.0% a year | +25.5% a year |
| S3 | +5.2% a year | +32.4% a year |

The later years carry the rerating from about 3.5x to 9x earnings (lesson 9), which cannot be assumed to repeat.

Plan for:

- index-like returns, a few points a year either side from the satellite, which can lose badly in a single year (S3 trailed the index by 21 points in 2026);
- a multi-year flat stretch;
- at least one 40 to 50% drawdown.

At Rs50k a month, deposits dominate the first five years. The plan's main job is to keep them going through the drawdown.

## The three things most likely to break it

1. **A regime turn while the book is concentrated.** S3's three worst trades (ECOP, CHCC, TGL, Rs5.1m) were sector reversals as the 2026 easing ended. The regime rule exited a month after the damage. In 2018-20 the E&P names lost 17 to 40% and were sold at the Covid trough. The satellite cap limits this. Stopping deposits in a drawdown is the bigger risk, and no rule prevents it.
2. **History flattered every active result.**
   - The fundamentals files cover names picked for being liquid in 2026; from Aug 2022 those names beat the rest of the universe by 2.3% a month (t 3.85).
   - The price panel holds only survivors.
   - S3's sector lists are in-sample.

   Live picks lack these tailwinds; the true edge may be zero. Rule 5 tests that.
3. **No repeatable stock-level edge.** The satellite's record rests on catching one SAZEW, whose quarterly EPS quadrupled in 2024. Without another, expect the satellite to trail the index by its trading costs: S3 paid Rs0.62m in fees at 199% annual sell turnover. Consolidated EPS is also unverified (lesson 1); ENGROH shows a 40% ROE.

## What would change this

- **Full insider extraction:** run S3's frozen sponsor-buying satellite.
- **Dated KMI index weights:** backtest the hand-built core.
- **Cash dividends before Nov 2024:** a like-for-like comparison with the index.
- **Point-in-time fundamentals for names that were not liquid in 2026.**
- **24 months of live satellite results.**

