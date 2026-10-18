# Rs50,000 on 16 Oct 2025, valued 16 Oct 2026

Script `scripts/tests/rs50k_last_year.py`, full output `tests/out/rs50k_last_year.txt`. One deposit, fully reinvested, cash dividends at 85% where `data/corporate_actions.csv` has them (complete only from Nov 2024), costs 0.25% per side plus 0.25% under Rs20m traded value, values after exit costs. Index lines carry no costs.

| Line | Final Rs | Multiple | Max DD | Trades |
|---|---|---|---|---|
| KMI All Share TR | 49,494 | 0.99 | -21% | 0 |
| KSE100 TR | 50,601 | 1.01 | -23% | 0 |
| KMI30 TR | 50,110 | 1.00 | -22% | 0 |
| Walk-forward B0 | 48,519 | 0.97 | -29% | 163 |
| Walk-forward B1 | 43,549 | 0.87 | -30% | 17 |
| Walk-forward S2 | 41,153 | 0.82 | -31% | 20 |
| Walk-forward S3 | 41,955 | 0.84 | -34% | 10 |
| Walk-forward S4 | 41,191 | 0.82 | -40% | 16 |
| S1 (63-day momentum top 3) | 24,499 | 0.49 | -61% | 20 |
| S2 (6-1 momentum top 3) | 16,514 | 0.33 | -73% | 21 |
| S3 breakout, 20% trail | 40,820 | 0.82 | -35% | 12 |
| S4 cheapest in top 3 sectors | 47,409 | 0.95 | -32% | 21 |
| S5 dip buy | 50,248 | 1.00 | -39% | 29 |
| S6 earnings jump | 38,420 | 0.77 | -32% | 15 |
| S8 top-10 liquid, monthly equal weight | 49,614 | 0.99 | -23% | 30 |
| Placebo, 200 random rotations | p10 30,035, median 39,007, p90 52,792 | 0.60 / 0.78 / 1.06 | | |
| Growth core hold (LUCK MEBL SYS MARI) | 47,384 | 0.95 | -25% | 4 |
| 60% core + 40% S3 | 44,759 | 0.90 | -26% | 16 |
| 75% core + 25% S3 | 45,743 | 0.91 | -26% | 16 |
| CHEATING best 5 liquid names in hindsight (MACFL QUICE PRL CRTM JVDC) | 140,721 | 2.81 | -33% | 5 |
| CHEATING single best (MACFL) | 179,742 | 3.59 | -53% | 1 |

The walk-forward strategies trade only on the first session of a month, so their money entered on 3 Nov 2025 and sat in cash for the first two weeks. The oracle-script systems start on 16 Oct exactly.

## What drove each result

The year was a round trip for the market: KMI TR rose to about Rs54,000 by Feb 2026, fell about 18% in the March 2026 drawdown, recovered to Rs53,900 in July, and ended flat. Nothing that was tested beat the index after costs, and most lost money.

- Momentum (S1, S2) was the worst: both bought the leaders going into the March fall and rotated monthly through a reversal, with full turnover costs. S2 lost two thirds.
- The random-rotation placebo had a median of 0.78x, so churning is itself expensive here; S3, S6 and the walk-forward strategies sit near that median, not above it.
- S8 and S5 ended at about 1.0x, S4 at 0.95x: they roughly matched the index.
- The growth core was hurt by SYS (0.77x), LUCK (0.89x) and MARI (0.87x); MEBL (1.28x) was the only gain. It fell 21% in the March drawdown month and lost less than the active systems.
- Blends were worse than the core alone because S3 was worse than the core.
- Hindsight: the winners were small, thin names (MACFL, QUICE, PRL, CRTM, JVDC) that no rule picked in advance. Even the best five carried a 33% drawdown.

## Trades that decided S3

- TPLT, bought 1 Jun 2026, up 63%, +Rs6,998 and still open on 16 Oct. It is the only large winner; without it S3 would be near Rs34,000.
- TRSM (-28%, -Rs3,616) and KEL (-22%, -Rs3,605): breakouts bought on the first days that failed within weeks.
- HALEON (-16%), BWHL (-18%) and MACFL (-19% in two days, bought 14 Oct): trailing stops and a last-minute entry cost another Rs7,500.

Twelve trades, three winners (TPLT, MEBL, IPAK). The walk-forward S3 version, a different implementation with monthly rebalancing, had no large winner and ended at 0.84x.

## Caveats

- The strategy list, the growth core names (LUCK, MEBL, SYS, MARI) and S3 as the blend partner were chosen with the year in view. This is a description of one year, not a test. Treat the blends especially as illustration.
- One year, one start date, one path; the result is dominated by a handful of trades.
- Oracle-script systems use the Rs5m liquidity filter and 1% participation is not enforced; MACFL and QUICE may not have absorbed Rs50k per name cleanly.
- Dividends at 85% apply only where the corporate-actions table has them; the table is incomplete before Nov 2024 but covers this window. Capital gains tax (15%) is not deducted anywhere.
- Survivors only: the panel contains names still listed on 16 Oct 2026.
- Oracle-script systems here use a panel rebuilt with dividends at 85% (the script's own panel uses 100%), so numbers differ slightly from `oracle_and_good_case.txt`.
