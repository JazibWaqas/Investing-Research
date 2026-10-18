# Why the breakout system missed MACFL, QUICE, PRL, CRTM, JVDC and (mostly) TPLT, 16 Oct 2025 to 16 Oct 2026

Script `scripts/tests/winners_2026_postmortem.py`; outputs `tests/out/winners_2026_postmortem_part1.txt` (names), `_part2.txt` (S3 attribution), `_part3.txt` (fixes). Built 18 Oct 2026 on the oracle script's panel with dividends at 85% (as `rs50k_last_year.md`), so S3 here is 0.82x on 12 trades, identical to that test; the replica was asserted equal to `oracle_and_good_case.py`'s S3 to the rupee.

**Short answer.** The investor is half right. All six names closed above their prior 252-session high during the year (12, 21, 26, 21, 14 and 30 sessions), so a breakout rule did "notice" them. S3 failed to hold them for three reasons that have nothing to do with seeing the move late: its three slots were full on 214 of 250 sessions, mostly with weak breakouts that were bought first; two names were below its liquidity bar when they signalled; and the one it did hold (TPLT) was removed from the KMI All Share index four days later. Six pre-registered fixes did not repair this: the one that held all six (no cap) made 1.10x this year and 0.88x in the median of five other windows, against 2.44x for S3. The winners were a mix: one sector story that was public and liquid (PRL), one earnings jump (MACFL), one takeover approach (TPLT), and three moves with no readable cause (QUICE's December leg, CRTM, JVDC) that look like thin-float speculation.

## 1. The six paths

Adjusted (total return) close, 16 Oct 2025 = 1.00. Base = lowest close before the peak.

| | base (date, x) | peak (date, x) | 16 Oct x | peak to end | peak / base |
|---|---|---|---|---|---|
| MACFL | 9 Mar, 0.71 | 14 Oct, 4.46 | 3.61 | -19% | 6.3 |
| QUICE | 20 Oct, 0.98 | 8 Jan, 4.64 | 3.29 | -29% | 4.7 |
| PRL | 2 Mar, 0.70 | 16 Oct, 2.95 | 2.95 | 0% | 4.2 |
| CRTM | 24 Feb, 0.76 | 20 Apr, 3.68 | 2.43 | -34% | 4.9 |
| JVDC | 28 Oct, 0.93 | 30 Jan, 2.18 | 1.89 | -14% | 2.3 |
| TPLT | 26 Nov, 0.93 | 7 Sep, 4.56 | 4.09 | -10% | 4.9 |

Month-end multiples (Oct is 16 Oct):

| | Oct | Nov | Dec | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | 16 Oct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MACFL | 1.00 | 0.88 | 1.02 | 1.17 | 0.86 | 0.71 | 1.06 | 2.11 | 2.41 | 2.44 | 2.10 | 2.54 | 3.61 |
| QUICE | 1.00 | 1.04 | 2.62 | 3.23 | 3.29 | 2.43 | 2.42 | 3.20 | 3.77 | 3.74 | 3.37 | 3.27 | 3.29 |
| PRL | 1.00 | 0.97 | 1.01 | 1.02 | 0.77 | 0.78 | 0.99 | 0.96 | 0.99 | 1.66 | 2.88 | 2.57 | 2.95 |
| CRTM | 1.00 | 1.08 | 1.15 | 1.00 | 0.92 | 1.73 | 3.35 | 3.05 | 2.82 | 3.10 | 2.93 | 2.63 | 2.43 |
| JVDC | 1.00 | 1.00 | 1.49 | 2.18 | 1.75 | 1.38 | 1.62 | 1.82 | 2.00 | 1.95 | 1.96 | 1.98 | 1.88 |
| TPLT | 1.00 | 0.94 | 1.44 | 1.75 | 1.40 | 1.09 | 1.72 | 2.47 | 2.89 | 3.84 | 4.16 | 4.29 | 4.09 |

Liquidity (trailing 60-session median traded value, Rs m; H above 20, M 5 to 20, L 2 to 5, XL under 2): MACFL 22H (Oct), 7.8M (Dec), 11.9M (Mar), 27H (Jun), 53H (Sep). QUICE 12.5M, 29.7H, 45H, 48H, then 4.3L in Sep. PRL 251H to 2,165H all year. CRTM 8.0M, 5.3M, 6.7M, 10.6M, then 0.2XL in Sep. JVDC 35H, 15M, 97H, 125H, 68H. TPLT 2.3L (Oct), 1.6XL (Dec), 5.2M (Mar), 17.5M (Jun), 12.7M (Sep). TPLT was under Rs5m for 95 of 250 sessions and CRTM for 83.

### What was observable, and when

Dates are the session of the signal close. TPLT is in the price panel (seed data) but not in `daily_table.parquet`, so its locks and volume flags are rebuilt from closes (a lock is a close up 9.95% or more) and its engine run is not possible.

| | first 252-high (x) | first upper lock | first 3 locks in 10 | first volume 3x | results / material filings | sector peers vs name, base to peak |
|---|---|---|---|---|---|---|
| MACFL | 15 Jun (2.38) | 4 Nov | 20 Jan | 5 Nov | 10 / 1 | +34% vs +532% |
| QUICE | 28 Oct (1.12) | 28 Oct | 4 Nov | 22 Oct | 9 / 1 | +3% vs +374% |
| PRL | 9 Jul (1.16) | 5 Mar | 21 Aug | 30 Dec | 9 / 4 | +111% vs +324% (3 refiners) |
| CRTM | 26 Nov (1.12) | 30 Dec | 4 Mar | 19 Nov | 8 / 0 | -2% vs +385% |
| JVDC | 26 Dec (1.32) | 26 Dec | never | 9 Dec | 8 / 0 | +11% vs +134% |
| TPLT | 17 Dec (1.44) | about 10 Dec | about 17 Dec | about 21 Oct | 12 / 2 | -19% vs +392% |

KMI All Share moved +5% to +14% over the same base-to-peak spans. MACFL's first 252-high is late because it had crashed about 60% from its 2025 high into Nov 2025 and had to recover that first.

Filings, class by class (titles in `_part1.txt`): MACFL material_info on 2 Jan (16:12) with no retrievable text; QUICE material_info 15 May, merger with Indus Fruit Products at 13.66 new shares per IFPL share (375.8m new shares against about 109m existing; I read the PDF); PRL material_info 23 Dec (interim CEO), 25 Sep (Upgrade Agreement signed 24 Sep with the Government under the refinery policy amended in Aug 2026), 12 and 15 Oct (chairman); CRTM none, only board-meeting notices with no stated agenda; JVDC none; TPLT 24 Mar (early sukuk redemption) and 24 Jun at 08:15 ("an international investment group has expressed interest in acquiring majority shareholding stakes"). Insider-disclosure filings exist for all six but the direction field is "unknown" in the data, so I cannot say whether they were buys.

What the price had already done when each cause became public (share of the base-to-peak log gain already made at the event close):

| event | public | gain already made | next 5 / 20 sessions |
|---|---|---|---|
| MACFL Q3 EPS 1.83 against 1.03 | 29 Apr 08:47 | 17% | +61% / +118% |
| MACFL FY results (Q4 EPS 0.28) | 2 Sep | 63% | +10% / +13% |
| QUICE Q1 results, lock day | 28 Oct | 9% | +13% / -9% |
| PRL Q3 EPS 15.78 against -4.09 | 21 Apr | 30% | -2% / -10% |
| PRL cabinet approves amended policy (Topline, via web search) | 21 Jul | 46% | +20% / +69% |
| PRL Upgrade Agreement | 25 Sep | 90% | -3% / +15% |
| JVDC H1 EPS 4.08 against 0.82 | 27 Feb | after the 30 Jan peak | -20% / -21% |
| TPLT takeover interest | 24 Jun | 82% | -4% / +17% |

TPLT rose from Rs22.67 to Rs25.04 on 19 and 22 Jun (volume 2.6m shares on the 22nd) before the 24 Jun 08:15 filing, then fell to Rs21.50 by 30 Jun. That is a pattern, not proof of leakage.

### Share of the eventual gain still ahead

Anchor = first 252-high close; "ahead" = log gain from the day-k close to the peak over the log gain base to peak; the multiple is peak over the day-k close.

| | day 0 | day 5 | day 10 | day 20 | day 40 |
|---|---|---|---|---|---|
| MACFL (15 Jun) | 34%, 1.87x | 30%, 1.73x | 33%, 1.84x | 31%, 1.78x | 34%, 1.86x |
| QUICE (28 Oct) | 91%, 4.13x | 83%, 3.65x | 92%, 4.15x | 97%, 4.52x | 50%, 2.18x |
| PRL (9 Jul) | 65%, 2.56x | 65%, 2.57x | 49%, 2.04x | 36%, 1.68x | 13%, 1.20x |
| CRTM (26 Nov) | 75%, 3.28x | 75%, 3.26x | 73%, 3.18x | 75%, 3.29x | 82%, 3.63x |
| JVDC (26 Dec) | 59%, 1.65x | 34%, 1.33x | 34%, 1.33x | 15%, 1.13x | past peak |
| TPLT (17 Dec) | 72%, 3.17x | 77%, 3.40x | 66%, 2.87x | 60%, 2.61x | 69%, 3.02x |

Late entry was worth it for QUICE, CRTM, TPLT and early PRL; it was not for JVDC (15% left by day 20) or MACFL's 15 Jun signal (a third left). Figures above 70% at day 40 for CRTM and TPLT reflect multi-leg paths with a later base. The other anchors (first lock, first 3-lock cluster, first volume spike) are in `_part1.txt`; the volume spike gives the most ahead (MACFL 81%, QUICE 95%, CRTM 81%, JVDC 82%), because it comes earliest.

**The engine on the first-signal day** (`engine.py`, analogues before that date, from the next open): MACFL 15 Jun, n=44, median +2% at 20 sessions and +1% at 60, 7% gained over 50%; QUICE 28 Oct, n=56 to 61, +1.6% at 20 and +13.3% at 60, 14% over 50%; PRL 9 Jul, +4.4% at 20, +3.0% at 60, 0% over 50%; CRTM 26 Nov, +0.4% and +6.3%, 6% over 50%; JVDC 26 Dec, +1.6% and -1.5%, 13% over 50%. The engine saw ordinary situations, correctly: the realised moves (+87% for MACFL, +313% QUICE, +156% PRL, +228% CRTM) sit in the top few percent of analogue outcomes. It said nothing that should have made anyone chase.

## 2. Why S3 did not hold them

S3 signalled (closed above the prior 252-high, liquid, KMI member) with a free slot for MACFL, CRTM and TPLT only; the rest were refused every time.

| name | signal sessions | what S3 did |
|---|---|---|
| QUICE | 21 (28 Oct to 8 Jan, four episodes) | slots full every time: TELE, HALEON, then TRSM (27 Oct to 25 Nov) or PIOC. KEL was stopped on 27 Oct and TRSM took the slot the same day, one day before QUICE's first signal |
| PRL | 26 (9 Jul to 2 Sep, eight episodes) | slots full every time: MEBL (+9% over the year), IPAK (+6%), TPLT |
| JVDC | 14 (26 Dec to 30 Jan) | slots full except 26 Jan: ranked 2nd of 6 for one slot, SAZEW (-7%) taken |
| MACFL | 12 | 15 Jun to 19 Aug and 9 to 12 Oct: slots full (MEBL, IPAK, TPLT). Order 13 Oct, bought 14 Oct at the peak close; -19% in two sessions, still open |
| CRTM | 21 | 26 Nov to 30 Dec: full (TELE, HALEON, PIOC). 6 to 18 Mar (nine sessions): excluded, median traded value Rs4.8m. Bought 9 Apr at about 3.1x after the first leg; stopped 19 May, -5% |
| TPLT | 30 | 17 Dec to 6 Jan: excluded, Rs1.6m. 11 to 12 May: full. Bought 1 Jun, +63%, open, the only big winner |

Over the year S3 held three positions on 214 of 250 sessions and none on 20. Liquid KMI names at a new 252-high numbered 2.4 per session on average (maximum 13), and 40 distinct names did it in January alone; three slots cannot queue that. Slots are given first-come, ranked only by how far the close sits above the old high.

The 12 trades (`_part2.txt` has the entry extension, tier, run-up and what happened after each exit):

| trade | held | return | Rs |
|---|---|---|---|
| TPLT 1 Jun to open | 95 d | +63% | +6,998 |
| MEBL 9 Apr to open | 128 d | +9% | +1,035 |
| IPAK 17 Apr to 14 Oct | 120 d | +6% | +756 |
| SAZEW 27 Jan to 10 Mar | 29 d | -7% | -599 |
| CRTM 9 Apr to 19 May | 27 d | -5% | -631 |
| PIOC 25 Nov to 27 Jan | 44 d | -8% | -716 |
| TELE 17 Oct to 17 Feb | 85 d | -8% | -1,282 |
| MACFL 14 to 16 Oct | 2 d | -19% | -2,418 |
| BWHL 17 Feb to 10 Mar | 15 d | -18% | -2,483 |
| HALEON 17 Oct to 3 Mar | 95 d | -16% | -2,619 |
| KEL 17 Oct to 27 Oct | 6 d | -22% | -3,605 |
| TRSM 27 Oct to 25 Nov | 21 d | -28% | -3,616 |

Why the nine losers lost (Rs): the KMI index fell 21% from 23 Jan to 9 Mar. Five stops landed in that window (PIOC, TELE, HALEON, SAZEW, BWHL), Rs7,698; but TELE and PIOC had run up 21% and 24% first, so the shock took back gains, and only BWHL (+26% 60 sessions after exit) and SAZEW (+7%) recovered after the stop. Two failed within six weeks in Oct to Nov (KEL, TRSM), Rs7,221, both first-day breakouts that never ran (run-up 0% and 1%); TRSM fell another 57% after its exit. MACFL and CRTM, Rs3,049, are bad timing (peak-day entry) and a stop on a name that had already tripled. So about half the loss is the March shock hitting normal stops, a third is two bad entries in the first month, the rest is late entry. Thin names were not the cause: all nine losers had a median traded value of Rs8.3m or more at entry.

## 3. Six fixes, pre-registered, on the seen year and five 2-year windows

Rules are in the script docstring, written before any variant ran. F1 rotation (top 3 of names within 5% of the 252 high, by 63-session return, monthly, drop-out below rank 6), F2 no cap (weekly, equal weight capped at one third each, 20% stop), F3 stop 30%, F4 Rs2m threshold with size at most 2% of the 20-day mean traded value (F4s adds 1.5% a side under Rs5m), F5 pyramid one extra unit at +10% above entry and a new high, F6 = F1+F3+F4. Placebos: 100 random draws per window, same exits (breakout timing kept and names random for S3; random names from the eligible list each month for F1 and F6).

Each cell: multiple / max drawdown / trades / hit rate / median trade, Rs50,000 start, after costs. KMI index multiple in the header.

| | 1 yr to 16 Oct 26 (KMI 0.99) | 2016-12 (0.80) | 2018-10 (1.02) | 2020-10 (1.02) | 2022-10 (1.75) | 2024-10 (1.83) |
|---|---|---|---|---|---|---|
| S3 base | 0.82 / -35% / 12 / 25% / -8% | 0.82 / -20% / 7 / 43% / -9% | 1.02 / -43% / 11 / 36% / -11% | 2.54 / -18% / 8 / 75% / +36% | 2.88 / -20% / 11 / 64% / +2% | 2.44 / -26% / 12 / 58% / +11% |
| F1 | 0.65 / -44% / 25 / 36% / -3% | 1.19 / -23% / 20 / 40% / -1% | 0.70 / -56% / 40 / 22% / -5% | 2.17 / -27% / 43 / 44% / -1% | 1.00 / -43% / 45 / 33% / -4% | 1.55 / -44% / 48 / 44% / -1% |
| F2 | 1.10 / -24% / 102 / 31% / -6% | 0.82 / -27% / 41 / 44% / -5% | 0.74 / -55% / 86 / 40% / -4% | 0.88 / -26% / 91 / 27% / -8% | 1.75 / -15% / 126 / 53% / +3% | 2.35 / -17% / 228 / 48% / -1% |
| F3 | 0.60 / -43% / 9 / 33% / -24% | 0.75 / -29% / 7 / 14% / -13% | 0.85 / -44% / 7 / 43% / -21% | 1.43 / -16% / 5 / 60% / +32% | 1.75 / -17% / 3 / 67% / +65% | 2.50 / -25% / 6 / 83% / +73% |
| F4 | 0.76 / -32% / 16 / 31% / -8% | 0.75 / -27% / 8 / 38% / -14% | 0.89 / -41% / 16 / 31% / -7% | 2.54 / -18% / 8 / 75% / +36% | 3.36 / -17% / 9 / 78% / +21% | 2.62 / -31% / 15 / 60% / +7% |
| F4s | 0.75 / -32% / 16 / 25% / -8% | 0.75 / -27% / 8 / 38% / -14% | 0.86 / -44% / 16 / 31% / -9% | 2.54 / -18% / 8 / 75% / +36% | 3.35 / -17% / 9 / 78% / +20% | 2.56 / -32% / 15 / 60% / +4% |
| F5 | 0.82 / -35% / 12 / 25% / -8% | 0.77 / -23% / 6 / 33% / -16% | 1.02 / -43% / 11 / 36% / -11% | 2.81 / -19% / 8 / 75% / +33% | 2.88 / -20% / 11 / 64% / +2% | 2.44 / -26% / 12 / 58% / +11% |
| F6 | 0.65 / -42% / 25 / 32% / -3% | 0.99 / -33% / 24 / 33% / -3% | 0.72 / -54% / 41 / 32% / -5% | 1.04 / -42% / 49 / 35% / -2% | 1.07 / -38% / 48 / 31% / -3% | 1.38 / -45% / 48 / 38% / -1% |
| placebo, S3 exits | 0.87 (S3 beats 35% of draws) | 0.75 (75%) | 0.72 (93%) | 0.85 (100%) | 1.48 (97%) | 1.59 (95%) |
| placebo, F1 exits | 0.85 (F1 beats 10%) | 0.99 (92%) | 0.72 (40%) | 1.18 (98%) | 1.58 (3%) | 1.56 (49%) |
| placebo, F6 exits | 0.84 (F6 beats 7%) | 0.82 (87%) | 0.69 (57%) | 1.03 (52%) | 1.49 (9%) | 1.44 (43%) |

The small differences from `oracle_and_good_case.txt` (S3 2.54 against 2.59, 2.88 against 2.96, 2.44 against 2.46) come from 85% against 100% dividends. F5 equals the base in three windows because a pyramid needs cash and three full slots leave none. Across the five 2-year windows (median / geometric mean / worst / windows beating S3 / beating KMI): S3 2.44 / 1.72 / 0.82 / - / 4; F1 1.19 / 1.23 / 0.70 / 1 / 2; F2 0.88 / 1.17 / 0.74 / 0 / 2; F3 1.43 / 1.32 / 0.75 / 1 / 3; F4 2.54 / 1.72 / 0.75 / 2 / 3; F5 2.44 / 1.73 / 0.77 / 1 / 3; F6 1.04 / 1.02 / 0.72 / 1 / 2.

Did any hold the six? Seen year, sessions held and return: S3 MACFL 2 d (-19%), CRTM 27 d (-5%), TPLT 95 d (+63%). F1 QUICE 22 d (+23%), PRL 41 d (+43%), JVDC 41 d (0%), TPLT 20 d (+19%). F2 all six: MACFL 50 d (-12%), QUICE 46 d (+34%), PRL 43 d (+89%), CRTM 87 d (+38%), JVDC 42 d (+29%), TPLT 103 d (+39%); on the six it made Rs11,955 and on the other names it lost Rs6,990. F3 CRTM 119 d (-25%), JVDC 21 d (-30%). F4 and F4s CRTM only (+16%). F5 the same as S3. F6 as F1. F1 lost because its other picks lost Rs27,414 (worst TRSM -53% in a month, PPL -30%, SGF -26%), against Rs9,953 on the six.

**Multiple testing.** Six variants (seven with F4s) over six windows is 42 comparisons on a year whose winners I already knew. Only the seen year is in-sample; the 2024-10 window ends 1 Oct 2026, so it contains about 11.5 of the 12 seen months and is not independent, which leaves four independent windows. A sign test over five windows cannot go below p = 0.031, above the Bonferroni 5% bar of 0.0083. No variant clears even the loose bar: F4 beats S3 in two windows and loses in two, F5 beats it in one and loses in one. The only variant that improved the seen year, F2, loses to S3 in four of five other windows. S3 itself beats its random-name placebo in all five 2-year windows (75% to 100% of draws) but only 35% of draws in the seen year, so this year is statistically unremarkable for S3, not a failure of the signal. F1 and F6 beat their placebos in about half the windows, so ranking by 63-session return adds nothing reliable. I did not run a placebo for F2.

## 4. Verdict

Were they catchable late by a rule? Partly, and at a price. A cap-free breakout basket (F2) entered all six and earned +29% to +89% on five of them (MACFL lost 12%), well under half of each move (TPLT +39% of a 4.9x move), but it made 0.88x in the median of the five other windows, below the index in three of five, and 1.75x against 2.88x in 2022 to 2024. Its 1.10x this year is one in-sample observation. The cap, which crowds out names like PRL, is also what gives S3 its 2.4x to 2.9x in good years. No tested fix is a free repair, and the best across all windows (F4 and F5, geometric mean 1.72 and 1.73 against S3's 1.72) is indistinguishable from doing nothing.

By reading a cause: PRL, MACFL and TPLT only. By name:

- **PRL**: catchable by rule and by cause. A sector story (three refiners, peers +111%) tied to refinery policy and a Q3 profit turn; liquid all year (Rs165m to 2.2bn a day); 65% of the gain still ahead at the first 252-high on 9 Jul; policy approval 21 Jul (asserted by a Topline note found by web search, not checked at source) and the Upgrade Agreement filing 25 Sep were public. S3 was crowded out on all 26 signal days. The cleanest miss.
- **MACFL**: catchable by cause for the second leg. Q3 EPS 1.83 against 1.03 was public at 08:47 on 29 Apr with 83% of the gain ahead; the first 252-high on 15 Jun had only a third left. The last leg (Sep to Oct, on a weak Q4) was speculative, and S3's only fill was the peak, then -19% in two sessions.
- **TPLT**: S3 caught it on timing luck. The cause (takeover interest) was public 24 Jun with 82% of the gain done. It was under Rs5m a day until Jan, and it was deleted from the KMI All Share index effective 5 Jun (`data/index_changes.csv`), so a KMI-only investor who bought on 1 Jun had to sell within days. Not tradable by the investor's own rules.
- **QUICE**: rule-catchable only without a cap (F2 +100% on one leg). No filing explains the December doubling; there was a substantial-holder disclosure on 6 Jan, two days before the peak; 35 upper-lock closes; a dilutive merger in May; liquidity down to Rs3.8m a day by October. Operator-style.
- **CRTM**: thin-float move. Textile peers -2%, no material filing, 23 locks, Rs4.5m to 8m a day before the run and Rs0.2m a day now (Rs50k would be a quarter of a day's volume). FY26 profit Rs52.7m (FinHisaab summary, asserted by search). Rs50k could have bought it in March; getting out at size after the 20 Apr peak was the problem. Exit liquidity.
- **JVDC**: the price peaked 30 Jan, four weeks before the EPS jump was announced; buyers on the 27 Feb news lost 20% in five sessions. Pre-results run, no cause visible at the time.

Not verified: TPLT's engine analogues and exact locks (not in the daily table); the text of MACFL's 2 Jan material information; the cause of CRTM, JVDC and QUICE's December leg; the policy-approval date for PRL beyond the web note; insider direction. Participation was not enforced in these simulations; a Rs50k position in a Rs2m-a-day name is 2.5% of a day, so F4's 2% cap would bind only for positions above Rs40k.
