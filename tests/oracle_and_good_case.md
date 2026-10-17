# Oracle and good case: what Rs50,000 could have become

Run 18 Oct 2026. Script `scripts/tests/oracle_and_good_case.py`; raw output `tests/out/oracle_and_good_case.txt` (price-return rerun `oracle_and_good_case_pr.txt`); every trade `tests/out/oracle_trades.csv`. Prices to 16 Oct 2026.

## Short answer

- **The program's own picks cannot be replayed.** PICKS.md is judgment, not point-in-time rules, so it is not tested here. For scale only: FFC, OGDC and FABL (the current core, chosen in Oct 2026 with hindsight) multiplied 2.54x, 2.02x and 2.15x from 17 Oct 2024 to 16 Oct 2026, about 2.24x equal weight before costs. That describes winners, not evidence.
- **Fixed menu of eight mechanical systems, 17 Oct 2024 to 16 Oct 2026:** S4 (cheapest name in the three strongest sectors) 2.38x, S3 (52-week-high breakout, 20% trailing stop) 2.12x, equal-weight top-10 liquid 1.82x, KMI All Share buy and hold 1.74x (Rs86,860). **Nothing reached 3x.** Measured 1 Oct 2024 to 1 Oct 2026: S3 2.46x, S4 2.33x.
- **Perfect foresight** (unattainable): monthly rotation into the best three names with a 1% participation cap would have made 265x; without the cap, 2,099x. These only set the scale of hindsight.
- **Is a 3x floor a fair test?** Over two years 3x needs +73% a year. In 2024 to 2026, 8% of liquid KMI names did it by buy and hold. Of 200 random monthly-rotation paths, 1.0% to 1.5% reached 3x. In the three older windows no random path and no simple system reached 2x, except S3 once.

## Method (fixed before looking)

Five 2-year windows plus the literal one (17 Oct 2024 to 16 Oct 2026, marked *). Rs50,000 at the start close, all costs paid: 0.25% a side, plus 0.25% a side when the name's 60-session median traded value is under Rs20m (0.5% or 1.0% a round trip). Signal at one close, trade at the next. Universe: median traded value over Rs5m, rolling and point in time; KMI All Share members only from 2019-01-28 (first membership list), so the first two windows use all liquid names. The eight systems are defined in the script header and were not tuned: S1 top-3 by 3-month return; S2 top-3 by 6-month return skipping the last month; S3 52-week-high breakout with a 20% trailing stop; S4 cheapest P/E name in each top-3 sector; S5 buy a 20% dip below the 60-session high in an uptrend; S6 buy after a 50%+ EPS jump; S7 KMI All Share; S8 equal-weight 10 most liquid.

Placebo: 200 random monthly rotations into 3 random liquid names, same dates and costs, full turnover each month (so it pays more cost than S1 or S2; for S3 and the other non-rotation systems the percentile is a rough yardstick).

## A. What buy and hold looked like (no costs, names liquid at the window start)

| Window | Names | 2x | 3x | 5x | Median | Lost money | KMI TR | Top three (sector) |
|---|---|---|---|---|---|---|---|---|
| 2016-12-30 to 2018-12-28 | 122 | 3.3% (4) | 0.8% (1) | 0 | 0.63x | 84% | 0.80x | AVN 3.1x (tech), SAZEW 2.8x (autos), LOTCHEM 2.0x (chemicals) |
| 2018-10-01 to 2020-10-01 | 86 | 3.5% (3) | 0 | 0 | 0.86x | 69% | 1.02x | SYS 2.5x (tech), FEROZ 2.4x (pharma), PIOC 2.1x (cement) |
| 2020-10-01 to 2022-09-30 | 74 | 4.1% (3) | 1.4% (1) | 0 | 0.76x | 69% | 1.02x | SYS 3.1x (tech), LOTCHEM 2.4x (chemicals), MTL 2.1x (autos) |
| 2022-10-03 to 2024-10-01 | 47 | 21% (10) | 2.1% (1) | 0 | 1.25x | 32% | 1.75x | GAL 3.8x (autos), HUBC 2.9x (power), PIOC 2.8x (cement) |
| 2024-10-01 to 2026-10-01 | 87 | 32% (28) | 8.0% (7) | 1.1% (1) | 1.51x | 16% | 1.83x | QUICE 5.1x (food), THCCL 4.0x (cement), POWER 4.0x (cement) |
| 2024-10-17* to 2026-10-16 | 89 | 26% (23) | 8% (7) | 0 | 1.48x | 17% | 1.75x | QUICE 4.9x (food), POWER 4.3x (cement), PRL 4.0x (refineries) |

Top 10 for the literal window: QUICE 4.9x, POWER 4.3x, PRL 4.0x, THCCL 3.5x, CNERGY 3.4x, ATRL 3.3x, NRL 3.1x, GHNI 2.9x, MEBL 2.7x, SSGC 2.7x (refineries and cement supply six). In the three older windows the median name lost 14% to 37% and 2x names were 3 to 4 in 100.

Survivorship check: 22, 9, 10, 6, 5 and 6 delisted names were liquid at the window starts and are not in the panel. In the first three windows most lost money; in 2022 to 2024 two were big winners (PSMC 3.41x, FFBL 2.59x), so that window's 2x share is 12 of 53, not 10 of 47.

## B. Perfect-foresight upper bound (multiple of Rs50,000; unattainable)

At each month-end buy the names with the best next-month net return, after costs. "Cap" limits a position to 1% of the name's trailing median daily traded value (my reading of the participation rule); leftover money sits in cash except in the last two columns.

| Window | Best 1 name, no cap | Best 3, no cap | Best 3, capped | Best names in order, capped, fully invested | Same, weekly |
|---|---|---|---|---|---|
| 2016-12-30 | 8,581x | 918x | 45x | 136x | 1,042x |
| 2018-10-01 | 1,114x | 333x | 63x | 191x | 1,458x |
| 2020-10-01 | 945x | 172x | 45x | 148x | 841x |
| 2022-10-03 | 2,499x | 306x | 99x | 254x | 948x |
| 2024-10-01 | 20,079x | 1,921x | 248x | 702x | 3,744x |
| 2024-10-17* | 22,587x | 2,099x | 265x | 792x | 3,804x |

These are not targets: they assume knowing which stock jumps next month and ignore circuit-limit lockups. Even with the liquidity cap the best case is tens to hundreds of times the stake in every window, bad ones included. The opportunity set was never the constraint. Prediction was.

## C. The good case: eight simple systems (multiple, then percentile among 200 random paths)

| System | 2016-12-30 | 2018-10-01 | 2020-10-01 | 2022-10-03 | 2024-10-01 | 2024-10-17* |
|---|---|---|---|---|---|---|
| S1 | 0.77x (88%) | 0.49x (4%) | 0.95x (84%) | 2.37x (98%) | 1.84x (84%) | 1.36x (64%) |
| S2 | 0.63x (67%) | 0.61x (19%) | 0.53x (16%) | 3.21x (100%) | 1.34x (52%) | 0.90x (16%) |
| S3 | 0.81x (90%) | 1.02x (75%) | 2.59x (100%) | 2.96x (100%) | 2.46x (96%) | 2.12x (94%) |
| S4 | n/a | n/a | 1.03x (90%) | 1.38x (70%) | 2.33x (94%) | 2.38x (96%) |
| S5 | 0.38x (8%) | 0.59x (16%) | 0.89x (78%) | 1.56x (80%) | 1.57x (70%) | 1.43x (70%) |
| S6 | n/a | n/a | 0.97x (86%) | 2.98x (100%) | 1.43x (58%) | 1.38x (66%) |
| S7 KMI | 0.80x (90%) | 1.01x (75%) | 1.02x (90%) | 1.74x (88%) | 1.82x (82%) | 1.74x (85%) |
| S8 top-10 | 0.53x (44%) | 0.90x (66%) | 0.71x (52%) | 1.82x (90%) | 1.85x (84%) | 1.82x (88%) |
| Random median | 0.56x | 0.78x | 0.70x | 1.16x | 1.32x | 1.18x |

CAGR, drawdown, trade count, hit rate and median trade for every cell are in the appendix. S4 and S6 need announced quarterly EPS, which exists here only from 2021 (S4 first traded 1 Aug 2022 in the 2020 window, S6 on 29 Apr 2021), so they are n/a earlier.

**Rank stability.** S3 won four of five windows (S2 won 2022 to 2024). S3's ranks in the five windows: 1, 1, 1, 3, 1. S2: 4, 4, 8, 1, 8. S6, where it runs: 4, 2, 7. Mean Spearman rank correlation between windows is +0.33 (8 of 10 pairs positive). S3 beat the KMI index in 5 of 5 windows, but in the first two it merely tied (0.81x vs 0.80x, 1.02x vs 1.01x); it won clearly in 3 of 3 decided windows.

**Is S3 robust?** Partly, and only relatively. For: top three in every window, never behind the index by more than a hair, maximum drawdown 18% to 26% in the three good windows. Against: it is one system picked from eight after the results, which weakens "3 of 3" (a single pre-named system has a 12.5% chance of that by luck; the chance that at least one of seven does is above 50%, treating windows as independent, which they are not). It makes 7 to 12 trades a window and one or two carry the result: NETSOL +236%, SAZEW +293%, FATIMA +165%. Without the two best trades S3 ends at 1.63x, 1.18x and 1.48x in the last three windows, and it lost or tied in two of five. Shifting the last window by 16 days moves S3 from 2.46x to 2.12x, S1 from 1.84x to 1.36x, S2 from 1.34x to 0.90x, so differences under about 0.5x are noise.

**Dividends.** The adjusted panel has cash dividends complete only from Nov 2024. The price-return rerun gives S3 2.22x, 2.57x, 2.34x and 1.39x in the last four windows (ex-dividend gaps now trigger stops) and S4 2.08x and 2.11x in the last two; S3 then falls below KMI in the literal window. S7 uses the complete total-return index, so before 2024 it is flattered relative to the others by roughly the dividend yield.

## D. 2024 to 2026: who reached 2x and what they traded

Reached 2x: S3 and S4, in both windows. Reached 3x: none. No other system passed 1.85x. Trade counts: S3 12, S4 34.

S3 (1 Oct 2024 to 1 Oct 2026), by rupee profit:

| Name | Entry | Exit | Return | Rs P&L | Exit reason |
|---|---|---|---|---|---|
| FATIMA | 2024-10-02 | 2026-02-25 | +165% | 27,405 | 20% trailing stop |
| TPLT | 2026-06-01 | 2026-10-01 | +71% | 21,457 | open at end |
| THCCL | 2024-10-02 | 2024-12-19 | +117% | 19,430 | 20% trailing stop |
| FCCL | 2024-10-02 | 2026-03-03 | +74% | 12,260 | 20% trailing stop |
| POWER | 2025-04-25 | 2026-03-03 | +20% | 3,825 | 20% trailing stop |
| MEBL | 2026-04-09 | 2026-10-01 | +11% | 3,499 | open at end |
| IPAK | 2026-04-17 | 2026-10-01 | +10% | 3,373 | open at end |
| CRTM | 2026-04-09 | 2026-05-19 | -5% | -1,732 | 20% trailing stop |
| SSGC | 2024-12-19 | 2025-01-08 | -11% | -2,688 | 20% trailing stop |
| GWLC | 2025-01-14 | 2025-02-04 | -17% | -4,253 | 20% trailing stop |

S4 (same window), exits by monthly rotation: TOMCL 2025-05-02 to 2025-10-01 +124% (Rs33,762); PRL 2026-08-03 to end +43% (open); CPHL 2024-10-02 to 2025-01-01 +86%; GWLC 2024-10-02 to 2024-11-01 +55%; MLCF 2024-11-01 to 2025-03-03 +36%; SNGP 2024-12-02 to 2025-04-03 +27%. Its win came from TOMCL, PRL and CPHL. Literal-window lists (S3 held MEBL +139% from 25 Nov 2024) are in the raw file.

S1 and S2 had the same best trade (BNL, +242% and +255%) but gave it back, with drawdowns of 59% and 63%. S5 (buy the dip) never beat the index. Monthly rotators had hit rates of 38% to 59% and medians near zero: the money was in the tail.

## What this does and does not say

1. A 3x in two years was reachable only by luck or hindsight in these windows. No simple rule delivered it. The best, S3, made 2.5x to 3.0x in the three windows that suited trend-following (2020 to 2022 and the last two) and about 1x in the other two.
2. The edge, if any, is cutting losers and letting winners run, which is what S3 does. That is a hypothesis from five windows.
3. In the three older windows the market returned 0.80x to 1.02x and the menu ranged 0.38x to 1.03x, apart from S3's 2.59x in 2020 to 2022. That fits lesson 13's finding that hike years lost to T-bills. A 2x two-year base case is not supported outside the last two windows.
4. Missing 3x does not show the model is unsharp: random paths had a 95th percentile of 2.2x to 2.3x in 2024 to 2026 and hit 3x in 1.0% to 1.5%.

## Caveats

- Survivors only; section A shows the delisted check. The bias is mixed and mostly flattering in the early windows.
- Price repair: 25 one-session drops of 25%+ (50%+ under Rs10) that the corporate-action table missed were treated as splits and earlier history rescaled (BECO, BNL, FNEL, KML, STL among them). The rule is mine and unverified against filings. Without it S1 and S2 took fake 90% losses in 2025.
- Quarterly EPS is StockAnalysis, consolidation unverified. Sector labels are a 2026 snapshot. Membership before 2019 is unknown. S3 cannot signal in the 2016 window before about Aug 2017 (panel starts Oct 2016).
- The windows overlap and the last two share one bull run: really five observations.
- Not tested: the real program (PICKS), monthly deposits, tax.

## Appendix: per-window detail (multiple, final Rs, CAGR, max drawdown, trades, hit rate, median trade, percentile)

```
Window 2016-12-30
sys   multiple   final Rs    CAGR   maxDD  trades   hit  median  plc pct
S1       0.77x     38,294    -13%    -58%      43   28%     -8%      88%
S2       0.63x     31,457    -21%    -42%      30   43%     -5%      67%
S3       0.81x     40,254    -10%    -20%       7   43%    -11%      90%
S4         n/a          -       -       -       0     -       -        -
S5       0.38x     18,969    -39%    -66%      36   22%    -18%       8%
S6         n/a          -       -       -       0     -       -        -
S7       0.80x     39,890    -11%    -29%       1    0%    -20%      90%
S8       0.53x     26,521    -27%    -57%      44   16%     -9%      44%
  best of menu: S3 0.81x; menu median 0.70x; placebo median 0.56x
Window 2018-10-01
sys   multiple   final Rs    CAGR   maxDD  trades   hit  median  plc pct
S1       0.49x     24,555    -30%    -70%      45   33%     -7%       4%
S2       0.61x     30,311    -22%    -66%      44   36%     -2%      19%
S3       1.02x     50,902     +1%    -43%      11   36%    -11%      75%
S4         n/a          -       -       -       0     -       -        -
S5       0.59x     29,401    -23%    -65%      39   36%    -11%      16%
S6         n/a          -       -       -       0     -       -        -
S7       1.01x     50,678     +1%    -37%       1  100%     +1%      75%
S8       0.90x     45,032     -5%    -50%      40   42%     -6%      66%
  best of menu: S3 1.02x; menu median 0.75x; placebo median 0.78x
Window 2020-10-01
sys   multiple   final Rs    CAGR   maxDD  trades   hit  median  plc pct
S1       0.95x     47,416     -3%    -50%      37   46%     -2%      84%
S2       0.53x     26,656    -27%    -58%      31   26%     -3%      16%
S3       2.59x    129,456    +61%    -18%       8   75%    +40%     100%
S4       1.03x     51,505     +1%    -12%       4   50%     +2%      90%
S5       0.89x     44,363     -6%    -44%      38   42%     -6%      78%
S6       0.97x     48,694     -1%     -9%       3   33%     -3%      86%
S7       1.02x     50,965     +1%    -16%       1  100%     +2%      90%
S8       0.71x     35,449    -16%    -54%      41   29%     -6%      52%
  best of menu: S3 2.59x; menu median 0.96x; placebo median 0.70x
Window 2022-10-03
sys   multiple   final Rs    CAGR   maxDD  trades   hit  median  plc pct
S1       2.37x    118,601    +54%    -33%      43   42%     -2%      98%
S2       3.21x    160,391    +79%    -27%      32   44%     -1%     100%
S3       2.96x    147,838    +72%    -19%      11   64%     +2%     100%
S4       1.38x     69,245    +18%    -24%      29   41%     -1%      70%
S5       1.56x     78,091    +25%    -21%      40   55%     +3%      80%
S6       2.98x    148,913    +73%    -15%      25   80%    +25%     100%
S7       1.74x     87,022    +32%    -12%       1  100%    +74%      88%
S8       1.82x     91,038    +35%    -22%      46   54%     +4%      90%
  best of menu: S2 3.21x; menu median 2.10x; placebo median 1.16x
Window 2024-10-01
sys   multiple   final Rs    CAGR   maxDD  trades   hit  median  plc pct
S1       1.84x     91,962    +36%    -59%      41   46%     -2%      84%
S2       1.34x     66,902    +16%    -63%      37   38%     -2%      52%
S3       2.46x    122,927    +57%    -26%      12   58%    +11%      96%
S4       2.33x    116,255    +53%    -32%      34   53%     +2%      94%
S5       1.57x     78,572    +25%    -50%      56   59%     +9%      70%
S6       1.43x     71,433    +20%    -31%      25   48%     -3%      58%
S7       1.82x     90,834    +35%    -21%       1  100%    +82%      82%
S8       1.85x     92,343    +36%    -24%      49   59%     +5%      84%
  best of menu: S3 2.46x; menu median 1.83x; placebo median 1.32x
Window 2024-10-17*
sys   multiple   final Rs    CAGR   maxDD  trades   hit  median  plc pct
S1       1.36x     68,173    +17%    -63%      41   46%     -3%      64%
S2       0.90x     44,786     -5%    -68%      36   39%     -9%      16%
S3       2.12x    106,092    +46%    -28%      12   58%    +17%      94%
S4       2.38x    118,904    +54%    -32%      34   53%     +2%      96%
S5       1.43x     71,661    +20%    -51%      56   54%     +1%      70%
S6       1.38x     69,237    +18%    -31%      25   48%     -3%      66%
S7       1.74x     86,860    +32%    -21%       1  100%    +74%      85%
S8       1.82x     91,015    +35%    -24%      49   63%     +4%      88%
  best of menu: S4 2.38x; menu median 1.59x; placebo median 1.18x
```
