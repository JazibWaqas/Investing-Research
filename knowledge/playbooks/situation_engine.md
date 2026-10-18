# Situation engine: what happened next in situations like this

Built 18 Oct 2026. Code: `scripts/engine.py`. Data: `data/daily_table.parquet` (577,794 stock-days, 2017 to 16 Oct 2026; see `data/DAILY_TABLE_NOTES.md`). Outputs: `tests/out/engine_examples.txt`, `tests/out/engine_scan_2026-10-16.txt`.

For any (symbol, date) or free query, the engine reports what a buyer at the next open got over 1, 3, 5, 10, 20 and 60 sessions in past situations with a similar signature. It is a base-rate lookup, not a forecast, and it says nothing about why a stock moved.

```
python scripts/engine.py SSGC 2024-10-23
python scripts/engine.py --scan 2026-10-16
python scripts/engine.py --query ret_1d=0.06 ret_5d=0.12 cause=results liq=hi [asof=2026-10-16]
```

## Signature (all known at the close of t)

- **Cause**, first match: a filing since the prior close (results, material information, dividend or bonus, insider buy, insider sell, other insider, board-meeting notice, other filing), else sector peers up or down 2% or more, else the KMI index up or down 1.5% or more, else none. Always matched exactly.
- **Move so far**: ret_1d, ret_5d, ret_20d, ret_60d in eight buckets each.
- **Position**: dist_252_high (six buckets, top one is "at the high"), consecutive_up_days (0, 1, 2, 3, 4 to 5, 6+), locks_up_5d (0, 1, 2, 3+).
- **Volume**: vol_ratio_20_120 in six buckets.
- **Liquidity tier** (60-session median traded value): above Rs20m, Rs5m to 20m, under Rs5m. **Regime**: 6M T-bill above or at or below the policy rate.

## Analogues

1. Candidates are rows strictly before t with the same cause. For a past date the engine sees only what existed then.
2. Distance is the sum of absolute bucket differences over the eight numeric features. A fixed ladder stops at the first step with at least 30 analogues whose 5-session outcome is known: distance 0 to 4 with regime and tier exact; then 0 to 4 with regime dropped; then 2 to 12 with regime dropped and tier allowed one step. The report prints the step and flags THIN if even the last gives under 30.
3. An analogue counts at horizon k only if its k-session return was realised by the close of t, so n differs by horizon.
4. Consecutive days of one stock are not independent, so the report shows distinct name-months ("ep") and a median of name-month medians. Trust ep, not n.

Each report gives n, ep, p10, p25, median, p75, p90, mean, win rate, share above +10% and +50%, worst, a placebo (median of all rows on the same dates and liquidity tier: a random entry with the same exit), and the median after round-trip cost (0.5% above Rs20m, 1.0% below, per `data/costs.md`; 15% CGT not deducted). Then the share that locked up within 5 sessions, the median first red day and the share red next session, median max adverse and favourable excursion, and one plain sentence per horizon.

## Scan, 16 Oct 2026

Liquid (above Rs5m) KMI names with a move above 5%, a lock, a news-less rise, a results filing or a sector lead: 8 of 125. Sorted by the 5-session analogue median: STL +0.0%, POWER -0.2%, SYM -0.4%, SLGL -1.4%, WASL -1.6%, then KEL -1.7%, AGP -1.7%, PRL -2.6%. Against the date-matched random entry the analogue median was better for STL, POWER and SYM, level for SLGL, worse for the other four. Today's interesting names carry no consistent 5-session base-rate edge.

## Four examples

**SSGC, 23 Oct 2024** (no filing, +11.2%, a lock, median traded value Rs6.5m so tier "mid"). 36 analogues, 35 name-months, found at distance 4 with regime dropped. Medians: -0.3% at 5 sessions, -4.8% at 20, -6.3% at 60; 29% up at 60, none above +50%; placebo at 60 was -5.0%. SSGC itself returned +23%, +144% and +303% at 5, 20 and 60. The instinct that spotted it was, by this signature, a below-even bet with a fat left tail, and SSGC lay outside the analogue distribution. Whatever drove it (a re-rating the features cannot see) is what to look for.

**PRL, 8 Jul 2026** (no filing, index down 1.5% or more while PRL rose 3.2%, four up days, near its high, tier "hi"). 77 analogues needed distance 8, regime dropped, tier one step. Median -0.8% at 5, -1.9% at 60; 44% up at 60, 25% above +10%, 3% above +50%. PRL then returned +8%, +66% and +135% at 5, 20 and 60. A strong day on a weak tape has a thin base rate; PRL was the right tail.

**ATRL, 16 Oct 2026** (no cause, +0.8%, +35% in 60 sessions, at its 252-day high, volume ratio 0.5, tier "hi"). 41 analogues at distance 2 with regime kept. Medians -0.4% at 5, -0.9% at 20, -0.5% at 60 against placebos of -1.2%, -3.7%, -6.2%; at 60, 35% gained over 10%, 5% over 50%, worst -40%. Quiet new highs after a run have a wide, near-zero-median outcome that beats the average stock. Nothing here argues for or against ATRL.

**PRL, 16 Oct 2026** (board-meeting notice, +3.1%, +14.9% in 5 sessions, +110% in 60, at its high, volume ratio 1.6). Only 30 analogues, 29 name-months, after widening to distance 4, regime dropped, tier one step. Medians -2.6% at 5, -3.1% at 20, -1.6% at 60; 37% up at 5; 7% above +50% at 60. Stocks this extended into a board meeting tended to give back a little first. With 29 episodes this is a weak reading, and the July example shows the right tail exists.

## Known weaknesses

- **Hindsight sector baskets.** Sector moves and leaders use today's survivor-heavy lists from `scripts/sector_momentum.py`.
- **Survivors and delisters.** Forward returns of delisted names stop at the last trade, so losses after it are missing, which flatters every set slightly.
- **Small sets for rare signatures.** Rare causes (insider, board meeting, rating) or extreme moves force the ladder to widen, and a widened set is a looser situation. Read the widening line and ep first; THIN means anecdote.
- **Regimes and overlap.** The 5% limit era and sub-Rs20 stocks inflate lock rates, and name-months in one sector move together.
- **The story is missing.** Valuation, earnings revisions, ownership and commodities are not in the signature.
- **Untested as a predictor.** Bucket edges and the ladder were set by hand once, after seeing the columns; there is no in-sample/out-of-sample split of the engine's own calls.
- **Gross of tax and fills.** Locked opens cannot be bought, and CGT is not deducted.
