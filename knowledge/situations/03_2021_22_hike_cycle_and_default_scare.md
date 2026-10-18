# Situation 03: the 2021 to 2022 hike cycle and the 2022 default scare

Written 2026-10-18. Type: regime case (tightening plus external stress). Sources: `data/macro/` (kse100, policy_rate_decisions, cpi, usdpkr, tbill_auctions), `data/panel_close_adj_pricereturn.parquet` (95 liquid survivors; delisted names are missing, so losses are understated), `tests/rate_cycle_episodes.md`, `knowledge/lessons.md` items 9 and 13. News: Al Jazeera 25 May 2022, Bloomberg (via BNN) and ProPakistani 27 May 2022, Arab News 14 Jul 2022, ProPakistani 17 Aug 2022 (all asserted from search snippets, not opened in full).

## Dates and regime

- 14 Jun 2021: KSE 48,726, the high before the cycle (observed). Policy rate 7.0%, flat for 15 months. CPI 10.8% (May).
- 20 Sep 2021: first hike, +25bp to 7.25%; KSE 46,528; USD/PKR 168.1.
- Hikes to 9.75% (14 Dec 2021), 12.25% (7 Apr 2022), 13.75% (23 May), 15.0% (7 Jul), then 16.0% (25 Nov) and 17.0% (23 Jan 2023).
- CPI 12.9% (Jan 2022), 21.3% (Jun), 27.3% (Aug), 26.5% (Oct).
- USD/PKR 177 (Dec 2021), 185.5 (Apr 2022), 204.6 (Jun), 239.9 on 29 Jul 2022 (peak), then 220 to 228 until Jan 2023.

## What was knowable, and when

1. 20 Sep 2021: the first hike. The 3-month bill was 7.2% and the 12-month 7.6%. The tightening cycle was visible from the central bank, though CPI at 9% made it look early.
2. Nov 2021: the IMF review stalled and a tranche was held up (WION, asserted). Every month without the IMF cost reserves.
3. Mar to Apr 2022: Sri Lanka defaulted and a no-confidence vote removed the PM (both asserted, general knowledge). The hike on 7 Apr was 250bp. KSE rallied to 46,602 on 15 Apr: a relief bounce.
4. 25 to 27 May 2022: reserves $10.2bn, under two months of imports; Pakistan 2031 dollar bonds at 63 cents, down 14 in a month; Moody warned of default without an IMF deal (asserted).
5. 13 to 14 Jul 2022: staff-level agreement on the combined seventh and eighth reviews, about $1.17bn (Arab News, asserted). Board approval 29 Aug (ProPakistani and ARY, asserted).

## What the market did

KSE: 46,528 (20 Sep 2021), 46,602 (15 Apr 2022), 39,832 (21 Jul 2022), 42,504 (29 Aug), 38,342 (17 Jan 2023, the cycle low). In rupees the index fell only 17.6% from the cycle start to the low. In dollars (index divided by USD/PKR) it fell 39% from 20 Sep 2021 to 17 Jan 2023 and 49.5% to 23 Jun 2023.

The index hid the stock market. From 20 Sep 2021 to 21 Jul 2022, 95 liquid survivors had a median return of -39.9%. Worst: TPLP -70%, TPL -67%, FLYNG -63%, GGL -60%, TRG -55%. Winners were rare: LOTCHEM +64%, EPCL +19%, EFERT +14%. To 23 Jun 2023, only 4 of 95 were up (4.2%) and the median was -52%.

## The right move

There was no long trade in this window; the correct position was bills. The 3-month T-bill yield rose from 7.2% (Sep 2021) to 15.2% (Jul 2022) to 22% (Jun 2023). Cash returned roughly 25% over the 21 months (approximate: average yield about 14% times 1.75 years) while the median liquid stock lost 52%.

Narrow exceptions existed, none repeatable: SNGP +60% from the 7 Apr 2022 hike to 23 Jun 2023, and ATRL +33%, both survivors. A sensible action for a small account was to add to bills, keep dry powder, and wait for a trigger to return. Lesson 13 says the cost of waiting was low until 2023, when the market rose 53% in a year and anyone sitting in cash missed it.

## The trap

Buying the dip repeatedly because rupee prices looked cheap. KSE sat 10 to 17% off its high for most of 2022 while the median stock was down 40%. A second trap was reading "the IMF will approve" as the bottom: KSE fell 4.9% after the 14 Jul staff-level agreement (41,863 on 13 Jul to 39,832 on 21 Jul), because the rupee kept sliding to 240.

## Situation type and lesson

Tightening cycle plus balance-of-payments stress. Markers: the policy rate up 800bp in ten months with CPI above it, a falling rupee, reserves under two months of imports, an IMF programme stalled or conditional. In this regime the base rate for a long equity trade was negative (4 of 95 liquid names up over 21 months), the bill paid double digits, and sitting out was a position.

Do not over-generalise the sit-out. The regime flipped within weeks of the IMF Board in 2023 (case 04), and a sit-out that continues into the recovery is a cost. The rule needs a trigger to return: an SLA, a budget the IMF accepted, and a rupee that has stopped falling.

## Questions that would have caught it

- Q1 Regime: policy rate against CPI (real rate negative until mid-2023), rupee direction, reserves in months of imports, IMF status. All four were red from Nov 2021.
- Q2 Situation type: IMF approval pending, with negative drift. Base rate in this repo for "approval is the low": n = 3 (cases 01, 03, 04); the Board date was not the low in any of the three.
- Q4 Price: the index was flat while the median stock fell. A breadth check on the median stock, not the index, shows it.
- Q5 Exit and loss: no stop protects against a market that is down 40% in breadth.
