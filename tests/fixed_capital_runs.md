# Fixed capital runs: Rs50,000 once, six start dates, to 16 Oct 2026

Run 18 Oct 2026. Script `scripts/tests/fixed_capital_runs.py`, raw output `tests/out/fixed_capital_runs.txt`. Engine: `scripts/walkforward.py`, frozen rules of `knowledge/playbooks/strategy_candidates.md` unchanged. The only change is a deposit schedule (`DEPS`, default Rs50,000 every month) and an optional calendar start (`WF_START`, default 2018-01). With the defaults the engine still gives S3 Rs17,630,566, the frozen headline.

## What was run

One deposit of Rs50,000 at the first close of the start month, nothing added afterwards. Decisions are monthly (quarterly reviews), sell proceeds are reinvested by the same rules, 0.5% round trip. Final values are marked at the 16 Oct 2026 close with no exit fee. Max drawdown is on the daily value path, with the Rs50,000 as the starting peak. Indices cost nothing. The "trades" column counts positions opened; hit, median and worst are over those trades, open ones marked.

## Headline: Rs50,000 from 1 Oct 2024 (two years)

| Row | Final Rs | Multiple | CAGR | Max DD | Trades |
|---|---|---|---|---|---|
| B0 buy the market | 83,936 | 1.68x | +28.9% | -31.2% | 169 |
| B1 orchestrator | 100,041 | 2.00x | +40.5% | -29.5% | 31 |
| S2 momentum + blowout | 82,384 | 1.65x | +27.7% | -29.4% | 42 |
| **S3 regime** | **67,855** | **1.36x** | +16.1% | -41.7% | 14 |
| S4 full | 74,929 | 1.50x | +21.9% | -36.8% | 42 |
| KMI All Share TR | 90,375 | 1.81x | +33.7% | -21.3% | |
| KSE100 TR | 101,718 | 2.03x | +41.6% | -22.6% | |
| KSE30 PR | 94,798 | 1.90x | +36.8% | -23.7% | |
| EW liquid KMI basket | 79,978 | 1.60x | +25.9% | -30.6% | |
| Best name, hindsight (QUICE) | 268,834 | 5.38x | +128% | -49.6% | |
| 10th best (SSGC) | 133,877 | 2.68x | +62% | -60.3% | |
| Worst (OCTOPUS, survivors only) | 13,582 | 0.27x | -47% | -77.5% | |

Of 87 liquid KMI names at entry: median buy-and-hold 1.50x, 82% ended above 1.0x, 24 reached 2x, 8 reached 3x, and only 33% beat the KMI All Share TR. No strategy reached 3x. Placebo (every quarter sell all, buy 4 random names, 1,000 draws): median 1.44x, 5th to 95th percentile 0.89x to 2.51x; S3 beat 41% of them.

S3's two-year path: 49,875 at entry, a peak of Rs101,226 on 1 Oct 2025 (1.08x the KMI index), then Rs87,468 in November, Rs69,018 in March 2026, Rs67,855 at the end. It led the index by up to 18% (May 2025) and trailed it by 25% by October 2026. Month by month:

| Date | S3 | KMI TR | KSE100 TR | EW KMI |
|---|---|---|---|---|
| 2024-10-01 | 49,875 | 50,000 | 50,000 | 49,875 |
| 2025-01-01 | 71,158 | 70,765 | 71,517 | 74,673 |
| 2025-04-03 | 73,888 | 71,663 | 72,696 | 72,049 |
| 2025-07-01 | 85,657 | 74,816 | 78,357 | 77,914 |
| 2025-10-01 | 101,226 | 93,957 | 101,241 | 91,969 |
| 2026-01-01 | 92,279 | 94,772 | 107,791 | 92,292 |
| 2026-03-02 | 69,018 | 80,586 | 92,888 | 71,467 |
| 2026-07-01 | 74,907 | 98,525 | 112,494 | 91,881 |
| 2026-10-16 | 67,855 | 90,375 | 101,718 | 79,978 |

The full 26-row path is in the raw file. Only 14 S3 trades: LUCK (+48%), TGL (+36%), AIRLINK (+30%) were the wins; ECOP (-43%), CHCC (-27%), TGL second time (-13%) the losses. The drop from Feb to March 2026 (S3 -23%, KMI TR -18%) and the failure to recover with the index in mid-2026 account for the shortfall.

## Other start dates (final Rs, multiple; S3 and the benchmarks)

| Start | B0 | B1 | S2 | S3 | S4 | KMI TR | KSE100 TR | EW KMI | Best name | 10th | Worst |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-01 | 99k 1.99x | 112k 2.24x | 140k 2.80x | 122k 2.44x | 133k 2.66x | 103k 2.07x | 129k 2.57x | 90k 1.80x | THCCL 16.9x | 3.49x | 0.32x |
| 2022-10 | 129k 2.58x | 150k 3.00x | 186k 3.73x | 213k 4.26x | 220k 4.39x | 158k 3.16x | 202k 4.04x | 116k 2.31x | GAL 8.8x | 3.79x | 0.34x |
| 2020-10 | 123k 2.45x | 175k 3.50x | 141k 2.81x | 222k 4.44x | 208k 4.16x | 162k 3.24x | 205k 4.09x | 101k 2.01x | MEBL 13.3x | 3.81x | 0.34x |
| 2018-10 | 129k 2.57x | 104k 2.08x | 140k 2.79x | 235k 4.70x | 219k 4.39x | 165k 3.30x | 203k 4.07x | 98k 1.96x | MEBL 14.1x | 4.10x | 0.28x |
| 2016-12 | 117k 2.34x | 88k 1.75x | 137k 2.73x | 218k 4.35x | 204k 4.08x | 143k 2.87x | 172k 3.45x | 69k 1.38x | SAZEW 22.5x | 3.72x | 0.18x |

S3 CAGR and max drawdown: 2024-01 +37.7% / -41.7%; 2022-10 +43.2% / -41.7%; 2020-10 +28.0% / -41.7%; 2018-10 +21.2% / -48.5%; 2016-12 +16.2% / -64.7%. S3 median trade +2% to +6%, hit rate 50% to 67%, worst trade -43% to -46%. KSE30 PR and KSE100 PR (from April 2020 only) are in the raw file. Beat-the-index share of names stayed between 17% and 33% in every window.

## Reading it

1. The question "would it have tripled": over two years, no, and no pre-registered rule set would have. Rs150,000 in two years needs +73% a year. The best strategy (B1, 2.00x) did +40%. Only 8 of 87 names did 3x, and they are visible only afterwards.
2. S3 beat both TR indices only for starts of Oct 2022 or earlier, beat KMI TR but not KSE100 TR from Jan 2024, and lost to both in the last two years. The dependable edge is the long window, not the recent one. That fits lesson 9: 2022 to 2025 was a rerating.
3. Windows are nested, all ending 16 Oct 2026, so six starts are not six independent tests. The distinct market regimes inside them number about four: the 2017-19 fall, the 2020 crash and recovery, the 2022-25 boom, the 2026 reversal.
4. Rotation by itself is not an edge: the random quarterly-rotation placebo had a median of 1.44x to 2.12x in the four recent windows, close to the median buy-and-hold name. S3 beat 86% to 98% of placebo draws in the windows from 2024-01 back, but only 41% in the last two years.

## Caveats

- Cash dividends are complete only from Nov 2024. Before that the strategies and EW basket are near price return while KMI TR and KSE100 TR include dividends, so the table tilts against the strategies in every window except the first. Against the price-return KSE100 (from April 2020), S3 was 4.26x and 4.44x vs 3.14x and 2.81x.
- The panel holds survivors only; delisted names are missing. The worst-name row and the EW basket are flattered. The best-name rows are hindsight, not a strategy.
- Value inputs go live only in Aug 2022. Before then S3's core is the equal-weight of the chosen sectors' names (regime and momentum only).
- Membership before 28 Jan 2019 is the derived approximation; 2016-12 uses a separate 2017-01 calendar (118 months) with the regime state started cold, the others the frozen 2018-01 calendar.
- S3's sector lists were read off 2018 to 2026, so its longer-window numbers are an upper bound.
- Trade counts are small (14 to 77 for S3), so hit rates are noisy.
