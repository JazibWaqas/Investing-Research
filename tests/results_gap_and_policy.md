# Results-day gaps and sector policy windows (PSX, KMI names)

Run 2026-10-18. Script `scripts/tests/results_gap_and_policy.py`, raw output `tests/out/results_gap_and_policy.txt`, trade lists `tests/out/results_gap_R_*.csv`, event table `tests/out/results_gap_P_events.csv`.

## Hypothesis
R: a results day that the market rewards hard (a big gap-up on volume with EPS up 30%+, an upper lock, or a loss turning to profit) keeps drifting, so buying the next close is a tradable situation. P: a sector-wide policy or regulated-price event leaves a window between its first public date and the price fully moving, and the window differs by event type.

## Data
- R: `quarterly_eps.csv` (129 KMI names, EPS basic), result timestamps re-cleaned the same way as `results_surprise_drift.py`, raw OHLCV for locks and volume, `panel_close_adj.parquet` for returns. 1,946 events had a clean timestamp; 1,325 were traded and liquid (Rs5m, point in time), 2020 to 2026, but 81% fall in 2023 to 2026. Names are today's survivors; no delisted name has EPS rows.
- Repair: three splits missing from the actions table (BECO Nov 2025, BNL Dec 2025, STL Mar 2026, each about -89% in one day) were neutralised, otherwise they showed as -91% trades.
- P: 22 dated events, 12 from the repo's sector files, playbooks and rate file, 10 dated by web search (Dawn, ProPakistani, Profit, KPMG, MSCI via Profit; sources in the script). Baskets are the `sector_momentum.py` names, equal weight, total return, against KMI All Share total return.

## Method
Signal at the reaction-session close, fill at the next close that is traded and not locked (upper or lower, within 0.5% of 10%), within 10 sessions. Cost 0.5% round trip plus 0.5% slippage when 60-session median traded value is under Rs20m. Exits: 20, 60, 120 sessions, or a 20% trailing stop on closes (cap 250 sessions); an exit waits for the next session that is not locked down. Reaction session = announcement day, or the next session if announced after 15:30. 75% of results are intraday, so the "gap" is the day's close over the prior close; a strict opening-gap variant is in Robustness. Placebos, 300 draws each, same exits and costs: (1) random entry within 60 sessions after a result of the same symbol, (2) random liquid entry in the same symbol and year. Baseline: every liquid result event. Sleeve: Rs50k, every signal in date order, at most 3 positions, each 1/3 of equity. P entries are the close after the first session on or after the date, net of 1.0% for a basket.

## Results: R
Signal counts before fills: (a) gap 5%+, 2x volume, EPS +30%: 43 (14 entry quarters, 35 symbols); (b) upper lock: 38 (8 quarters, 34 symbols); (c) loss to profit with a positive reaction: 55 (18 quarters, 38 symbols). (a) and (c) never coincide; 18 of the 38 locks are also (a).

Net of cost. "Placebo" is the same-year random median (p = share of draws at or above the event median).

| Signal, exit | n | Median | Mean | Win | >+50% | <-30% | Worst | Placebo (p) | Sleeve, max DD |
|---|---|---|---|---|---|---|---|---|---|
| a, 20d | 41 | +0.7% | +5.9% | 51% | 5% | 0% | -23.7% | +1.7% (0.68) | 1.86x, -21% |
| a, 60d | 37 | +16.6% | +25.3% | 81% | 14% | 3% | -44.1% | +10.0% (0.11) | 5.17x, -23% |
| a, 120d | 37 | +18.4% | +37.4% | 78% | 22% | 8% | -38.2% | +21.0% (0.63) | 11.35x, -31% |
| a, trail 20% | 38 | +14.5% | +40.4% | 68% | 26% | 0% | -20.9% | +9.6% (0.19) | 11.22x, -23% |
| b, 60d | 31 | +5.8% | +14.0% | 61% | 10% | 0% | -21.9% | +3.4% (0.30) | 1.30x, -24% |
| b, 120d | 29 | +6.5% | +14.0% | 62% | 21% | 17% | -48.8% | +10.2% (0.69) | 1.73x, -28% |
| b, trail | 33 | -2.0% | +11.9% | 48% | 12% | 0% | -23.1% | -0.7% (0.59) | 1.56x, -24% |
| c, 60d | 49 | +5.7% | +17.3% | 59% | 12% | 2% | -32.5% | +4.0% (0.28) | 2.76x, -23% |
| c, 120d | 47 | +8.8% | +23.8% | 60% | 17% | 6% | -70.6% | +12.0% (0.78) | 3.07x, -31% |
| c, trail | 47 | -2.9% | +16.1% | 43% | 19% | 0% | -24.0% | -1.3% (0.62) | 3.87x, -25% |
| All results, 60d | 1,223 | +4.7% | +9.0% | 59% | 7% | 2% | -72.1% | | |
| All results, trail | 1,169 | -2.5% | +13.6% | 46% | 16% | 0% | -38.5% | | |

Against the post-result placebo (a weaker comparator than same-year random: median +3.0% against +10.0% at 60d) (a) wins at p 0.000; against same-year random it is +6.5 points at 60d (p 0.11) and nothing at 120d.

**By year and regime, (a) at 60d:** 2022 n1 -26.4%; 2023 n6 median +23.9%; 2024 n16 +27.9% (94% win); 2025 n12 +2.0%; 2026 n2 +21.4%. With the trailing stop the 2025 median is +0.6%. Bill above policy rate (n11) median +26.0%, win 91%; at or below (n26) +13.1%, win 77%. (b) 60d: 2024 +32.0% (n12), 2025 -5.2% (n15), 2026 +0.9% (n4). (c) 60d: 2023 +19.5%, 2024 +12.8%, 2025 -0.6%, 2026 +15.3%.

**Tail of (a):** best three trades are 44% of summed 60d return (SAZEW Feb 2024 +267%, HALEON +83%, FFC +66%); without them the median is +16.1%. Trailing: top three are 54%, median without them +9.3%. Worst: TATM Aug 2025 -44.1%, FABL Oct 2022 -26.4%.

## Results: P
Excess return of the sector basket over KMI TR from the entry after the first public date (market rows: KMI TR itself). "Lag" is sessions from first public date to decision; zero means only one date was found. Pctile = rank of the +60 excess among all start dates of the same basket.

| Event | Sector | First public / decision | Lag | +20 | +60 | +120 | Pctile@60 |
|---|---|---|---|---|---|---|---|
| Refinery policy 2026 (+) | Refineries | 13 Jul / 28 Jul 2026 | 11 | +31.3% | +61.0% | open | 98% |
| Circular-debt Rs1.225tr signed (+) | Power | 24 Sep 2025 | 0 | -2.1% | +15.7% | +17.5% | 97% |
| Construction package (+) | Cement | 3 Apr / 14 Apr 2020 | 7 | +5.3% | +3.1% | +27.7% | 56% |
| IMF SBA (+) | Islamic banks | 30 Jun / 12 Jul 2023 | 7 | +1.4% | +6.1% | +9.6% | 64% |
| OMC margin Rs1.87 (+) | OMC | 7 / 15 Sep 2023 | 6 | -0.2% | -2.7% | -21.0% | 51% |
| Super tax ruling (+) | E&P | 27 Jan 2026 | 0 | -5.3% | -0.2% | -4.7% | 47% |
| Auto policy AIDEP (+) | Autos | 17 Dec 2021 | 0 | -0.6% | -10.3% | -4.4% | 17% |
| Wellhead gas +8-10% (+) | E&P | 4 Sep 2026 | 0 | +2.1% | open | open | |
| Gas circular-debt plan (+) | Gas utilities | 19 Aug 2026, pending | | -2.2% | open | open | |
| IPP probe report (-) | Power | 21 Apr 2020 | 0 | -4.1% | -8.6% | -18.2% | 17% |
| IPP PPA terminations (-) | Power | 10 Oct 2024 | 0 | -2.1% | -21.2% | -22.8% | 1% |
| Super tax 10% (-) | Cement | 24 / 29 Jun 2022 | 3 | -0.7% | +13.3% | +2.3% | 88% |
| Cement FED (-) | Cement | 12 / 28 Jun 2024 | 9 | -4.3% | +0.6% | +34.7% | 47% |
| GIDC verdict (-) | Fertilizer | 13 Aug 2020 | 0 | -0.9% | +0.7% | -10.2% | 43% |
| Feed gas price rise (-) | Fertilizer | 14 Feb 2024 | 0 | +5.4% | +20.8% | +28.8% | 99% |
| Diesel crack cap (-) | Refineries | 20 Aug 2026 | 0 | +0.7% | open | open | |
| Diesel cut Rs135 (-) | OMC | 11 Apr 2026 | 0 | +29.5% | +19.7% | +19.0% | 96% |
| Auto policy 2026-31 (?) | Autos | 14 Sep 2026, pending | | -3.9% | open | open | |
| First cut 2020 (+) | KMI TR | 17 Mar 2020 | 0 | +4.5% | +16.2% | +46.5% | 84% |
| First cut 2024 (+) | KMI TR | 10 Jun 2024 | 0 | +6.5% | +6.8% | +41.8% | 69% |
| Cut after a pause (+) | KMI TR | 15 Dec 2025 | 0 | +4.2% | -10.8% | +0.5% | 7% |
| MSCI to Frontier (-) | KMI TR | 7 Sep / 30 Nov 2021 | 59 | -5.7% | -8.2% | -5.4% | 12% |

Sector events with expected-positive direction (n 9, 7, 6 at +20/+60/+120): median -0.2%, +3.1%, +2.6%. Net of 1.0% that is nothing. The direction label is mine, assigned from the nature of the event before looking.

## Robustness
- Strict opening-gap definition for (a) (news before 09:15 or after 15:30, or the next session): n 19, 60d median +9.3%, mean +17.4%, win 58%; trail median +7.3%, mean +32.8%. Smaller and weaker; same sign.
- Dropping the repair changes nothing for (a) but would have put two -91% trades in (b) and one in (c).
- The 2024 bull supplies 16 of the 42 (a) trades and the sleeve multiples. KMI All Share TR rose 3.17x from 28 Oct 2022, 2.87x from 26 Feb 2021 ((c) start) and 1.89x from 2 Aug 2024 ((b) start). The (a) sleeve beats the index at every exit except 20d (it sits in cash 32% of days at 60d); (b) never beats it; (c) beats it only at 120d (3.07x) and with the stop (3.87x).

## Verdict
- **R(a) gap + 2x volume + EPS +30%: watch.** The 60d median (+16.6%, win 81%) is +11.9 points over any result and +6.5 over matched random entries, not significant (p 0.11), and gone at 120d. Fourteen quarters, one year doing most of the work, 2025 flat. Exit that worked: the 20% trailing stop (worst -20.9%, 26% above +50%) or a 60-day hold; the 20-day exit has no edge (median +0.7%).
- **R(b) upper lock on results day: nothing.** Matches or trails random; trailing median -2.0%; 2025 negative. The part that works overlaps (a).
- **R(c) loss to profit: nothing as an entry rule.** 60d median equals the all-results baseline; with the stop the median is -2.9% and the mean (+16.1%) is three right-tail trades.
- **P, tradable windows after the first public date.** None reliable. Candidates, each thin: the first rate cut of a cycle (+41.8% and +46.5% at 120d, two cycles, and the third cut was nothing); a signed circular-debt settlement (nothing for 20 sessions, +15.7% at 60d, peak +20.9% at +64, one event); policy approvals with a lag (refinery policy, construction package: most of the first 5 to 15% came before the decision, the rest needed a confirming driver). Negative power-sector policy is worth exiting: both IPP events fell 18 to 23% at 120d, with only 2 to 4% gone in the first 20 sessions, so the exit window stayed open about a month. Tax and price announcements are not tradable in either direction: the cement tax hits recovered within 60 sessions, the fertilizer gas rise and the OMC diesel cut rose against the expected sign, and OMC margin approval (2023) lost 21%.

## Caveats
- Small n. (a) has 14 entry quarters; P has one event for most types; only 7 of 22 P events have a verified lag, because first public dates were not found for the rest (zero lag means unknown).
- Confounded windows: the OMC diesel cut came inside the post-war rebound; the refinery policy coincided with a collapsed ceasefire and a crack spike (13 Jul is unverified in the repo). AIDEP's date is approximate (press edition).
- Locks are inferred from closes, not order books; a lock is assumed buyable only after it breaks. A 10% bonus ex-day can look like a lower lock and delays an exit.
- EPS comes from StockAnalysis, consolidation unchecked, survivors only; cash dividends are complete only from Nov 2024, so older returns understate.
- Baskets are equal weight against a cap-weighted index; the percentile column is the guard, and the typical excess of these baskets is about +1%.
- I did not search for coal events or a separate cement FED 2023 date.

## Today's screen (16 Oct 2026)
R: of 36 results in the last 20 sessions, four pass a rule. PREMA (9/29: +10% lock, 7.9x volume, EPS 1.86 vs 0.84; both (a) and (b), now -8.6% from the reaction close, low-priced stock). Loss to profit: PIBTL (0.70 vs -0.14, -14.5% since), STL (1.14 vs -0.80, -9.5%), QTECH (1.06 vs -0.27, -1.3%). None is a fresh entry and (c) is a "nothing" rule.
P: pending decisions with a measured analogue are few. The gas circular-debt plan (19 Aug, -2.2% at +20) mirrors CIRCDEBT25, which paid only after signing. Other open items have no measured type: HSD crack cap term ends about 19 to 20 Oct, the Rs1.22 OMC margin notification, the 2026-31 auto policy, the windfall tax.
