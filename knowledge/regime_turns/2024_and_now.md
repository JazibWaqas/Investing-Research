---
type: "regime turn (first rate cut inside an uptrend), the 2025 to 2026 regime, and the present"
low_date: 2024-06-11
written: 2026-10-18
evidence: "data/macro/* (kse100, kmiallshr, policy_rate_decisions, tbill_auctions, cpi, fx_reserves, import_cover, current_account, usdpkr, brent, fipi_lipi, fipi_lipi_by_sector, kse100_pe), seed/data/macro/imf_events.csv, data/events_shocks.csv, data/daily_table.parquet, data/winners_library.csv, data/announcements.parquet, data/fundamentals/quarterly_eps.csv, SBP monetary policy statements in data/raw/macro/mps, catalysts/catalyst_calendar.csv"
---

# The June 2024 first cut as a mid-cycle turn, what followed, and where October 2026 stands

Written 18 Oct 2026, data to 16 Oct 2026 (USD/PKR to 30 Sep). **Knowable** means dated on or before the row (CPI from the 2nd of the next month); **hindsight** means it needed later prices. KSE100 and KMI All Share are total-return series. A *252-high* is an adjusted close above the prior 251 sessions' closes. *Liquid* is the daily table's flag (60-session median traded value over Rs5m): 90 names on 11 Jun 2024, 127 on 16 Oct 2026. The table holds no conventional banks (HBL, MCB, UBL), so "banks" below are BIPL, FABL and MEBL. `CATALOGUE.md` calls its entry rules hypotheses; so does this note.

## 1. Short answer

- **The cut was a policy turn, not a market low.** The decision (10 Jun; time not collected, treated as after the close) was followed by a KSE100 close of 72,589 on 11 Jun: 4.5% under its 24 May high, 0.6% over its 50-session average, 18.9% over its 200-session average, 81% over its 23 Jun 2023 level (40,065). Half of 90 liquid names were above their 50-day average. It is "the low" only because no close under it followed.
- **It held and paid.** KSE100 +7.3% at eight weeks, +57.5% at six months, **+60.0% at twelve** (to 116,168 on 23 Jun 2025); KMI All Share +5.5%, +54.6%, +48.7%.
- **Turn versus bounce was not visible in price or breadth.** Troughs later undercut and troughs that held both sat at 1 to 80% of names above the 50-day average (section 4). The 11 Jun reader had direction: the first cut after seven holds, the 6M bill 1.0 pt under policy, CPI down 11.3 pt in three months, reserves up $1.2bn, a flat rupee. The three false bottoms of Dec 2024 to Apr 2025 had similar macro and were undercut by shocks.
- **The first fortnight's leaders were last cycle's winners:** 13 of the first 15 liquid 252-highs had a library run begin Sep 2022 to May 2023; runs that began at the turn printed first 252-highs a median 122 sessions later.
- **Joining at +1, +4 or +8 weeks** made +59%, +73% and +92% on the index over 12 months; the leaders did no better than other liquid names.
- **Today** (section 9): of 22 signals the earlier lows showed, 15 are present and 7 absent; four more need a low not yet identified. No conclusion is drawn.

## 2. Week by week, 15 Mar to 9 Aug 2024 (knowable)

The MPC held at 22% on 18 Mar and 29 Apr with "continuity" wording, then changed on 10 Jun when May CPI fell to 11.74%. The 6M bill had been 0.6 to 1.6 pt under policy since February, so the cut was priced; the index was 15.6% over its 11 Mar close by 24 May. In the 20 sessions to and including the low, insurers (+27), foreigners (+8) and banks/DFI (+6) were net buyers; individuals (-17), companies (-9), broker proprietary desks (-9) and mutual funds (-6) were net sellers (USD m). Foreigners then bought $27m in sessions 10 to 29 and sold $196m in sessions 41 to 126, while mutual funds bought $234m.

**Table A. Price, breadth, rates and external account.** The bill gap uses the policy rate on the auction date.

| Week ending | KSE100 | 5-session % | vs 252-high % | vs 50d avg % | Liquid names above 50d / 200d % (n) | Policy % / 6M bill minus policy, pt | CPI y/y % (month) | SBP reserves $bn / import cover, months | USD/PKR | Brent $ |
|---|---|---|---|---|---|---|---|---|---|---|
| 15 Mar | 64,816 | -1.5 | -2.4 | +1.9 | 45 / 80 (74) | 22.0 / -1.61 | 23.1 (02) | 8.0 / 3.18 | 278.8 | 85 |
| 22 Mar | 65,152 | +0.5 | -1.9 | +2.3 | 42 / 79 (72) | 22.0 / -1.61 | 23.1 (02) | 8.0 / 3.18 | 278.4 | 85 |
| 29 Mar | 67,005 | +2.8 | -0.2 | +4.8 | 52 / 76 (71) | 22.0 / -1.61 | 23.1 (02) | 8.0 / 3.09 | 278.0 | 86 |
| 5 Apr | 68,417 | +1.9 | 0.0 | +6.6 | 64 / 84 (69) | 22.0 / -0.60 | 20.7 (03) | 8.0 / 3.09 | 277.9 | 90 |
| 12 Apr | 70,315 | +5.3 | 0.0 | +9.1 | 83 / 84 (70) | 22.0 / -0.60 | 20.7 (03) | 8.0 / 3.09 | 277.9 | 92 |
| 19 Apr | 70,910 | +0.8 | 0.0 | +8.7 | 86 / 90 (70) | 22.0 / -0.61 | 20.7 (03) | 8.0 / 3.09 | 278.3 | 88 |
| 26 Apr | 72,743 | +2.6 | 0.0 | +10.0 | 85 / 88 (73) | 22.0 / -0.61 | 20.7 (03) | 8.0 / 3.17 | 278.4 | 90 |
| 3 May | 71,902 | -0.1 | -1.2 | +7.4 | 69 / 86 (74) | 22.0 / -0.62 | 17.4 (04) | 9.1 / 3.17 | 278.3 | 84 |
| 10 May | 73,086 | +1.6 | 0.0 | +7.4 | 81 / 91 (78) | 22.0 / -0.62 | 17.4 (04) | 9.1 / 3.17 | 278.1 | 83 |
| 17 May | 75,342 | +3.1 | 0.0 | +9.0 | 85 / 93 (84) | 22.0 / -0.71 | 17.4 (04) | 9.2 / 3.17 | 278.3 | 82 |
| 24 May | 75,983 | +0.9 | 0.0 | +8.4 | 80 / 92 (86) | 22.0 / -0.71 | 17.4 (04) | 9.1 / 3.17 | 278.2 | 79 |
| 31 May | 75,878 | +1.0 | -0.1 | +7.0 | 75 / 91 (87) | 22.0 / -1.00 | 17.4 (04) | 9.1 / 3.17 | 278.4 | 79 |
| 7 Jun | 73,754 | -2.8 | -2.9 | +2.7 | 64 / 86 (90) | 22.0 / -1.00 | 11.7 (05) | 9.1 / 3.17 | 278.3 | 78 |
| 14 Jun **(low 11 Jun)** | 76,707 | +4.0 | 0.0 | +5.6 | 68 / 85 (91) | 20.5 / -0.53 | 11.7 (05) | 9.1 / 3.17 | 278.5 | 81 |
| 21 Jun | 78,810 | +8.6 | 0.0 | +7.8 | 66 / 85 (92) | 20.5 / -0.53 | 11.7 (05) | 8.9 / 3.17 | 278.5 | 86 |
| 28 Jun | 78,445 | -0.5 | -0.5 | +5.9 | 48 / 77 (94) | 20.5 / -0.54 | 11.7 (05) | 9.4 / 3.16 | 278.3 | 87 |
| 5 Jul | 80,213 | +2.3 | -0.1 | +6.9 | 54 / 76 (98) | 20.5 / -0.54 | 12.6 (06) | 9.4 / 3.16 | 278.4 | 89 |
| 12 Jul | 79,944 | -0.3 | -0.9 | +5.4 | 51 / 71 (98) | 20.5 / -0.72 | 12.6 (06) | 9.4 / 3.16 | 278.5 | 87 |
| 19 Jul | 80,118 | +0.3 | -2.1 | +4.8 | 49 / 71 (98) | 20.5 / -0.72 | 12.6 (06) | 9.0 / 3.16 | 278.2 | 85 |
| 26 Jul | 78,030 | -2.6 | -4.7 | +1.3 | 34 / 66 (97) | 20.5 / -1.21 | 12.6 (06) | 9.1 / 3.21 | 278.3 | 81 |
| 2 Aug | 78,226 | +0.3 | -4.4 | +1.0 | 34 / 65 (94) | 19.5 / -1.21 | 11.1 (07) | 9.2 / 3.21 | 278.5 | 78 |
| 9 Aug | 78,570 | +0.4 | -4.0 | +1.1 | 43 / 68 (92) | 19.5 / -0.75 | 11.1 (07) | 9.3 / 3.21 | 278.5 | 81 |

**Table B. Net buying by investor type, USD million, week to Friday** (scstrade.com; foreign is the three foreign types combined).

| Week ending | Foreign | Mutual funds | Individuals | Banks / DFI | Companies | Broker prop. | Insurers |
|---|---|---|---|---|---|---|---|
| 15 Mar | +2.7 | +0.6 | -0.1 | -0.7 | -2.5 | -1.7 | +1.1 |
| 22 Mar | +2.0 | -4.4 | -4.1 | -5.0 | -9.0 | -2.2 | +24.1 |
| 29 Mar | +3.6 | +1.0 | +0.3 | -5.2 | -7.6 | +2.1 | +9.0 |
| 5 Apr | +3.9 | -0.2 | +2.8 | +0.3 | +0.6 | -1.7 | -5.6 |
| 12 Apr | +4.2 | +2.5 | -3.2 | -4.9 | +0.4 | +2.6 | -1.3 |
| 19 Apr | +33.9 | -0.9 | -14.4 | -11.0 | -5.6 | +1.2 | -1.4 |
| 26 Apr | +3.0 | +6.0 | -0.1 | +1.3 | +0.1 | +2.4 | -13.1 |
| 3 May | +8.0 | -0.5 | -1.8 | -1.7 | +0.9 | -0.6 | +1.5 |
| 10 May | +2.7 | +1.6 | +0.1 | -0.4 | +0.5 | -1.9 | +2.0 |
| 17 May | +14.9 | +0.2 | -2.5 | -9.9 | -2.2 | +0.4 | -1.1 |
| 24 May | -12.1 | +2.0 | -6.7 | +10.4 | +5.2 | -2.8 | +5.3 |
| 31 May | +5.5 | -8.9 | -1.1 | -2.4 | -8.0 | +1.2 | +13.1 |
| 7 Jun | +4.4 | +1.6 | -10.3 | +7.5 | -4.8 | -7.3 | +7.3 |
| 14 Jun | -5.8 | +11.1 | -8.9 | -5.5 | +7.9 | +1.7 | -0.0 |
| 21 Jun | +0.6 | -0.8 | +0.7 | -10.0 | +8.0 | +3.5 | -1.3 |
| 28 Jun | +2.5 | -5.8 | +0.3 | -1.8 | +1.5 | +4.9 | +0.4 |
| 5 Jul | +7.7 | -13.6 | +5.4 | +5.6 | -4.6 | -0.1 | -0.6 |
| 12 Jul | +4.0 | -2.5 | -2.6 | +1.8 | -0.2 | -1.4 | +1.1 |
| 19 Jul | +9.3 | +4.1 | +3.3 | -0.8 | -4.4 | -1.9 | -7.7 |
| 26 Jul | +4.6 | -5.0 | -1.7 | -1.3 | +0.5 | -1.5 | +4.4 |
| 2 Aug | -2.2 | +1.4 | +1.5 | +0.0 | -1.2 | +0.5 | +1.8 |
| 9 Aug | +1.4 | -6.0 | +5.5 | -3.9 | -2.7 | +1.4 | +2.7 |

**Table C. Dated items.** Status R in `events_shocks.csv` means the date was recalled and not re-verified; W a web page.

| Date | What was knowable | Source |
|---|---|---|
| 18 Mar | MPC holds 22%: inflation "has begun to decline noticeably"; "requires continuity of the current monetary stance". 6M bill 20.39% on 20 Mar, 1.6 pt under policy | MPS 18 Mar; tbill_auctions |
| 21 Mar | IMF Board completes the final review of the 2023 standby | events_shocks (R) |
| 2 Apr | March CPI 20.67% (February 23.07%) | cpi.csv |
| 13 Apr | Iran missile and drone attack on Israel; Brent $92 on 9 Apr, $79 by 24 May | events_shocks (R); brent.csv |
| 18 to 30 Apr | March-quarter results: MEBL, SAZEW, FFC, HUBC up sharply; OGDC and PPL down (table D) | quarterly_eps.csv |
| 29 Apr | MPC holds 22%: inflation "still high"; budget measures a risk to the near-term outlook | MPS 29 Apr |
| 2 May / 2 Jun | April CPI 17.35%; May CPI 11.74% (month on month -3.2%) | cpi.csv |
| 29 May | 6M and 3M bills both 21.00%, 1.0 pt under the 22% policy rate: the cut is priced | tbill_auctions |
| **10 Jun** | **Cut 150bp to 20.5%, effective 11 Jun.** May inflation "better than anticipated"; reserves "around US$9 billion"; government "has approached the IMF for an Extended Fund Facility"; "now an appropriate time to reduce"; real rate "still significantly positive"; upside risks from the budget and energy prices | MPS 10 Jun |
| 11 Jun | KSE100 72,589 (-0.9%): the low. 12 Jun: FY25 budget presented; 6M bill 19.97% | kse100.csv; events_shocks (R) |
| 13 Jun | KSE100 +4.69% to 76,208 on 1.66x normal volume; 12 liquid names close at 252-highs. Cause not verified | kse100.csv; daily table |
| 2 Jul | June CPI 12.55% (up from 11.74%, the base-effect risk the 10 Jun statement named) | cpi.csv |
| 12 Jul | IMF staff-level agreement on a 37-month, about US$7bn EFF (31 days after the low; Board 25 Sep) | imf_events.csv; MPS 29 Jul |
| 29 Jul | Cut 100bp to 19.5%: "room to further reduce... in a calibrated manner"; SBP reserves "above $9.0 billion" from $4.4bn at end-June 2023. Fitch CCC to CCC+ | MPS 29 Jul; events_shocks (W) |
| 5 Aug | KSE100 77,084, 5.8% under its 60-session high; it stayed above the 13 Jun close | kse100.csv |

**Table D. Largest results filings of liquid names, by profit** (StockAnalysis, not checked against PSX filings). Most of the 299 material-information filings are untitled; titled: OGDC 27 Jun, Rs82bn Term Finance Certificates by Power Holding Limited; PPL 22 Apr, production enhancement. PDFs not opened.

| Filed | Name | Quarter | Profit, Rs m | y/y |
|---|---|---|---|---|
| 18 Apr | MEBL | Mar | 24,956 | +62% |
| 19 Apr | SAZEW | Mar | 3,034 | +582% |
| 29 Apr | OGDC | Mar | 47,808 | -26% |
| 29 Apr | PPL | Mar | 27,837 | -15% |
| 29 Apr | HUBC | Mar | 17,186 | +53% |
| 29 Apr | LUCK | Mar | 15,587 | -26% |
| 29 Apr | FFC | Mar | 12,560 | +52% |
| 30 Apr | AIRLINK | Mar | 1,036 | +534% |
| 30 Jul | FFC | Jun | 24,591 | +104% |
| 8 Aug | MEBL | Jun | 26,843 | +55% |
| 8 Aug | MARI | Jun | 25,659 | +62% |

## 3. The price structure of the low

| Item | Value |
|---|---|
| Low | Close 72,589.49 on Tue 11 Jun 2024 (intraday low 72,476.05). The 10 Jun close, before the decision reached the market, was 73,252.56 |
| Context | 4.47% under the 24 May high (75,983.04, 11 sessions earlier); the lowest close since 3 May (26 sessions); +0.64% over its 50-session average, +18.86% over its 200-session average; never closed under the 50-session average in the prior 60 sessions |
| Tests of the low | One. On 12 Jun the index traded to 72,464, 0.02% under the 11 Jun intraday low, and closed 72,797 (+0.29% over the 11 Jun close). No later close was under 72,589; the lowest close in the next 12 months was 76,208 (13 Jun) |
| First week that held | The low week (to 14 Jun) closed +4.0%; the first full week entirely above the low was the week to 21 Jun (weekly low 76,897, close 78,810) |
| First close above the 50-session average | Not applicable: it never closed below it. A new 252-high in the index came on 13 Jun (76,208 over 75,983), 2 sessions after the low |
| First 252-high in a liquid name | 13 Jun: 12 names (SAZEW, DGKC, HUBC, LUCK, FCCL, PIOC, FABL, MUGHAL, MTL, HINOON, GLAXO, HALEON). Their day volume was 0.5x to 7.5x the prior 20-day mean (median about 3x) |
| Index volume (60-session mean 209.8m shares) | 11 Jun 142.3m (0.68x); 12 Jun 106.6m (0.51x); 13 Jun 345.0m (1.66x); 14 Jun 212.7m (1.01x); 20 Jun 211.7m (1.00x) |

## 4. Pullbacks, false bottoms and the real lows

Every pullback of 4% or more from Aug 2023 to Aug 2024 held, so no false bottom preceded 11 Jun. False bottoms came later: 19 Dec 2024, 6 Feb and 9 Apr 2025 were undercut by 8 May 2025 (US tariffs 2 Apr, India strikes 7 May); 13 and 30 Oct 2025 by 2 Mar 2026 (war on Iran from 28 Feb). Of 18 troughs since Aug 2023 with a 120-session verdict, 8 were undercut. Breadth overlapped (median 30% of names above the 50-day average, range 12 to 80%, against 21%, range 1 to 52%), and foreign selling, mutual-fund selling and bank buying were as large at false bottoms (mutual funds -$269m before 9 Apr 2025). Only depth separated them: the two deepest troughs held (8 May 2025, -13.0%, 7% above their 50-day; 9 Mar 2026, -22.6%, 1%). The 13 Oct 2026 trough (164,776, -9.4%) is untested.

| Trough | KSE100 | Drop from 60-session high % | vs 200d avg % | Names above 50d / 200d % | Policy %, last move | 6M minus policy, pt | CPI % (3-month change, pt) | SBP reserves, 13-week change $bn | Foreign / mutual funds, 20 sessions, USD m | Outcome (120 sessions) |
|---|---|---|---|---|---|---|---|---|---|---|
| 26 Dec 2023 | 59,171 | -10.9 | +25.3 | 43 / 85 | 22.0, hold +0bp | -0.6 | 29.2 (+1.8) | +0.1 | +46 / -13 | held |
| 16 Feb 2024 | 59,873 | -9.9 | +16.8 | 11 / 67 | 22.0, hold +0bp | -1.6 | 28.4 (+1.4) | +0.8 | -21 / -6 | held |
| 11 Jun 2024 **(this turn)** | 72,589 | -4.5 | +18.9 | 50 / 80 | 20.5, cut -150bp | -1.0 | 11.7 (-11.3) | +1.2 | +8 / -6 | held |
| 5 Aug 2024 | 77,084 | -5.8 | +15.8 | 29 / 63 | 19.5, cut -100bp | -1.2 | 11.1 (-6.3) | +0.0 | +19 / -8 | held |
| 19 Dec 2024 | 106,275 | -8.5 | +31.9 | 80 / 89 | 13.0, cut -200bp | -3.0 | 4.9 (-4.8) | +2.6 | -55 / +56 | undercut 8 May |
| 6 Feb 2025 | 110,301 | -6.2 | +24.8 | 25 / 85 | 12.0, cut -100bp | -0.5 | 2.4 (-4.7) | +0.2 | -14 / -24 | undercut 7 May |
| 9 Apr 2025 | 114,153 | -4.0 | +18.2 | 34 / 71 | 12.0, hold +0bp | -0.0 | 0.7 (-3.4) | -1.0 | -9 / -269 | undercut 28 Apr |
| 8 May 2025 (real low) | 103,527 | -13.0 | +3.4 | 7 / 40 | 11.0, cut -100bp | -0.0 | 0.3 (-2.2) | -1.1 | -8 / -141 | held |
| 13 Oct 2025 | 158,443 | -6.2 | +23.7 | 35 / 75 | 11.0, hold +0bp | +0.0 | 5.6 (+2.3) | -0.1 | -44 / -85 | undercut 30 Oct |
| 30 Oct 2025 | 156,733 | -7.3 | +19.4 | 22 / 67 | 11.0, hold +0bp | +0.0 | 5.6 (+2.3) | +0.2 | -26 / -260 | undercut 2 Mar |
| 9 Mar 2026 (real low) | 146,480 | -22.6 | -6.7 | 1 / 9 | 10.5, hold +0bp | +0.2 | 7.0 (+0.8) | +1.8 | -289 / -50 | held |
| 30 Apr 2026 | 162,994 | -13.2 | -0.1 | 54 / 26 | 11.5, hike +100bp | +0.5 | 7.3 (+1.7) | -0.3 | -2 / +14 | undercut 18 May |
| 24 Jul 2026 | 171,021 | -8.8 | +0.8 | 26 / 36 | 11.5, hold +0bp | +0.3 | 11.1 (+3.8) | +1.2 | +32 / -66 | undercut 10 Sep |
| 14 Sep 2026 | 167,971 | -10.4 | -2.4 | 12 / 26 | 11.5, hold +0bp | +0.4 | 11.2 (-0.4) | +4.2 | -26 / -74 | undercut 5 Oct |

## 5. The leaders

Order is date, then 60-session traded value; 12 names printed on 13 Jun, the budget-reaction day. Common to the 15: all within 13% of their high on 11 Jun (median 4%) and all had printed a 252-high in the prior 30 sessions, so they continued rather than broke out of a base; 14 were KMI members and 12 traded over Rs20m a day; 13 had a library run starting Sep 2022 to May 2023; profit was up y/y in 10 of 14 with data, down in LUCK, FCCL, MUGHAL and NETSOL. The 18 liquid library runs that began 12 May to 9 Sep 2024 (median 2.5x; hindsight starts) share no name with the 15: gas utilities (SNGP, PIBTL, WAVES), textiles (NML), chemicals (GGL, DOL), HBL, CSIL, with first 252-highs mostly in Oct to Dec 2024. Returns are total return from the 11 Jun close, before costs.

| # | First 252-high | Name | Sector | Day volume vs prior 20-day mean | Below its high on 11 Jun | Latest quarter profit y/y | To +8w % | To +6m % | To +12m % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 13 Jun 2024 | SAZEW | Auto assembler | 1.4x | 7% | +582% | +43 | +41 | +39 |
| 2 | 13 Jun 2024 | DGKC | Cement | 3.0x | 4% | +5% | -11 | +22 | +65 |
| 3 | 13 Jun 2024 | HUBC | Power | 1.7x | 4% | +53% | +6 | -6 | +5 |
| 4 | 13 Jun 2024 | LUCK | Cement | 4.0x | 2% | -26% | -3 | +40 | +77 |
| 5 | 13 Jun 2024 | FCCL | Cement | 2.7x | 7% | -6% | -9 | +72 | +84 |
| 6 | 13 Jun 2024 | PIOC | Cement | 4.0x | 7% | +27% | +0 | +43 | +31 |
| 7 | 13 Jun 2024 | FABL | Bank | 0.8x | 4% | +100% | +15 | +12 | +52 |
| 8 | 13 Jun 2024 | MUGHAL | Engineering | 2.9x | 2% | -92% | -16 | -4 | -34 |
| 9 | 13 Jun 2024 | MTL | Auto assembler | 3.5x | 2% | +111% | -8 | -3 | -12 |
| 10 | 13 Jun 2024 | HINOON | Pharma | 0.5x | 3% | +28% | -5 | +33 | +39 |
| 11 | 13 Jun 2024 | GLAXO | Pharma | 7.5x | 7% | +31% | +7 | +227 | +174 |
| 12 | 13 Jun 2024 | HALEON | Pharma | 4.2x | 4% | +114% | +23 | +237 | +156 |
| 13 | 14 Jun 2024 | OCTOPUS | Tech | 0.7x | 13% | n/a | +70 | +8 | -30 |
| 14 | 20 Jun 2024 | AIRLINK | Tech | 2.6x | 9% | +534% | +80 | +158 | +81 |
| 15 | 20 Jun 2024 | NETSOL | Tech | 0.7x | 10% | -99% | +4 | +24 | -9 |

**Sector order, median total return from the 11 Jun close** (groups of 3 to 4 are a handful of stocks). Over eight weeks: auto assemblers (SAZEW, GAL, GHNI), technology (QTECH, AIRLINK, OCTOPUS), E&P; cement 15th of 16. Over six months: pharma, E&P, OMC (SSGC +293%), cement, fertilizer.

| Sector (symbols.csv, liquid names on 11 Jun) | n | Median to +8w % | Rank | Median to +6m % | Rank | Median to +12m % |
|---|---|---|---|---|---|---|
| Pharmaceuticals | 7 | +8 | 5 | +107 | 1 | +109 |
| Oil & Gas Exploration Companies | 3 | +13 | 3 | +95 | 2 | +85 |
| Oil & Gas Marketing Companies | 5 | +4 | 9 | +91 | 3 | +90 |
| Cement | 12 | -8 | 15 | +69 | 4 | +76 |
| Fertilizer | 3 | +7 | 7 | +69 | 5 | +88 |
| Refinery | 4 | -3 | 11 | +62 | 6 | +49 |
| Automobile Assembler | 5 | +43 | 1 | +41 | 7 | +39 |
| Glass & Ceramics | 3 | -2 | 10 | +35 | 8 | +33 |
| Food & Personal Care Products | 9 | -3 | 12 | +35 | 9 | +17 |
| Power Generation & Distribution | 3 | +6 | 8 | +34 | 10 | +9 |
| Automobile Parts & Accessories | 3 | +9 | 4 | +33 | 11 | +2 |
| Chemical | 4 | -6 | 14 | +31 | 12 | +25 |
| Textile Composite | 3 | -9 | 16 | +28 | 13 | +3 |
| Technology & Communication | 7 | +25 | 2 | +28 | 14 | -8 |
| Commercial Banks | 3 | +8 | 6 | +12 | 15 | +52 |
| Engineering | 6 | -5 | 13 | +4 | 16 | -8 |

## 6. What a reader applying the reflex would have done

The reflex for a regime turn (`CATALOGUE.md`) is to join on the second signal, then take the sector leaders' first 252-highs with a 25% stop and a 32% size cap. At each checkpoint I give the index and the leaders printed so far (point in time), bought at the checkpoint close and held 12 months. The leader label added nothing distinguishable: the leaders' medians (+53%, +55%, +67%) match the other liquid names (+46%, +56%, +69%). The 25% trail fired in 7, 18 and 25 names and lowered the mean by 2, 14 and 26 points. FFBL (merged into FFC) is held flat after 20 Dec 2024, which understates it.

| Entry (close) | KSE100 over next 12m (worst close; max drawdown) | KMI All Share TR | Leaders so far: mean / median / win / worst | Leaders with 25% closing trail: mean / median (stops fired) | Other liquid names: mean / median / win | All liquid: median |
|---|---|---|---|---|---|---|
| +1 week, 21 Jun 2024 | +59.4% (-2.2%; -13.0%) | +53.8% | 18 names: +61% / +53% / 72% / -39% | +59% / +53% (7) | 74 names: +70% / +46% / 85% | +47% |
| +4 weeks, 12 Jul 2024 | +72.9% (-3.6%; -13.0%) | +57.8% | 31 names: +59% / +55% / 81% / -43% | +45% / +26% (18) | 68 names: +77% / +56% / 88% | +55% |
| +8 weeks, 13 Aug 2024 | +92.3% (-0.2%; -13.0%) | +74.8% | 40 names: +81% / +67% / 82% / -72% | +55% / +48% (25) | 55 names: +71% / +69% / 93% | +65% |

## 7. After the turn: the peak, the cuts and the hike regime

The first leg ran from 72,589 to 117,587 on 3 Jan 2025 (+62.0% in 6.8 months) with 1,000bp of cuts by 27 Jan and CPI falling from 11.7% to 4.1%. At that peak 94% of liquid names were above their 50-day average, the KSE100 P/E was 10.1 (7.1 to 8.7 at the 2023 and 2024 lows) and the real policy rate was +8.9. The index then ranged between 110,300 and 118,900 for four months while cuts paused, fell 13.0% to the 8 May 2025 low, and reached 189,167 on 23 Jan 2026 (+160.6% from 11 Jun 2024). The 15 Dec 2025 cut surprised (all 12 in a Reuters poll expected a hold). The 28 Feb 2026 war on Iran took Brent from $71 to $121 by late March ($138 on 7 Apr) and the KSE100 down 9.6% on 2 Mar to a 9 Mar low, 22.6% under the peak; the 6M bill was 1.0 pt over policy at the 16 Mar auction, six weeks before the hike. The 27 Apr hike to 11.5% came with "inflation is likely to increase and remain above the target range in the next few quarters"; CPI went 7.3% (Mar), 10.9% (Apr), 10.3% (Sep, seed only). The MPC held on 15 Jun, 27 Jul and 14 Sep. The 6M bill has been over policy at 12 of 13 auctions since the hike (12.40% on 14 Oct).

| Date | Event | KSE100 | vs 252-high % | Policy % | 6M minus policy | CPI % (month) | Real rate | SBP res. $bn | Brent $ | Above 50d / 200d % |
|---|---|---|---|---|---|---|---|---|---|---|
| 16 Dec 2024 | Cut 200bp to 13.0% | 116,169 | 0.0 | 13.0 | -3.00 | 4.9 (Nov) | +8.1 | 12.1 | 74 | 94 / 97 |
| 3 Jan 2025 | High of the first leg | 117,587 | 0.0 | 13.0 | -1.01 | 4.1 (Dec) | +8.9 | 11.7 | 77 | 94 / 96 |
| 27 Jan 2025 | Cut 100bp to 12.0%; last of 1,000bp | 113,520 | -3.5 | 12.0 | -1.60 | 4.1 (Dec) | +7.9 | 11.4 | 77 | 56 / 91 |
| 21 Apr 2025 | After the 10 Mar hold | 118,383 | -0.5 | 12.0 | -0.01 | 0.7 (Mar) | +11.3 | 10.2 | 69 | 57 / 76 |
| 8 May 2025 | Low: India strikes (7 May) | 103,527 | -13.0 | 11.0 | 0.00 | 0.3 (Apr) | +10.7 | 10.3 | 62 | 7 / 40 |
| 15 Dec 2025 | Surprise cut to 10.5% | 170,741 | 0.0 | 10.5 | 0.00 | 6.2 (Nov) | +4.3 | 15.9 | 62 | 66 / 79 |
| 23 Jan 2026 | All-time high | 189,167 | 0.0 | 10.5 | -0.55 | 5.6 (Dec) | +4.9 | 16.1 | 68 | 66 / 78 |
| 9 Mar 2026 | Low: Iran war, oil shock | 146,480 | -22.6 | 10.5 | +0.24 | 7.0 (Feb) | +3.5 | 16.3 | 94 | 1 / 9 |
| 27 Apr 2026 | Hike 100bp to 11.5% | 169,497 | -10.4 | 11.5 | +0.65 | 7.3 (Mar) | +4.2 | 15.8 | 114 | 82 / 31 |
| 3 Jul 2026 | Second high | 185,372 | -2.0 | 11.5 | +0.25 | 11.1 (Jun) | +0.4 | 18.5 | 69 | 86 / 63 |
| 16 Oct 2026 | Now | 166,420 | -12.0 | 11.5 | +0.90 | 10.3 (Sep) | +1.2 | 21.5 | 127 | 16 / 31 |

## 8. If-then rules this turn supports

Counts are of the seven lows in section 9, each the lowest close of its episode (hindsight). They are descriptions, not tested rules.

| If | Then (measured, not a forecast) | Lows sharing it | June 2024 |
|---|---|---|---|
| The index is 12% or more under its 252-high and under 10% of liquid names are above their 50-day average | It is a deep, washed-out low; the first liquid 252-highs took 2 to 63 sessions. Breadth that low occurred on 7% of 223 sampled dates | 5 of 7 (2019, 2020, Jan 2023, May 2025, Mar 2026) | No (-4.5%; 50%) |
| A policy or IMF trigger arrives with 20% or more of names above their 50-day average | The low is a pullback in an uptrend: first liquid 252-high within 2 sessions, no later undercut, 12-month index +101% and +60% | 2 of 7 (Jun 2023, Jun 2024) | Yes |
| The 6M bill cutoff is 0.7 pt or more under policy in the auction before a first cut | The cut was priced; in 2024 the index had risen 15.6% from 11 Mar to 24 May and fell 0.9% the day after the cut | 2 of 3 first cuts (Mar 2020 -0.74, Jun 2024 -1.00; not Dec 2025) | Yes |
| After any of the seven lows | The first 15 liquid 252-highs are mostly last cycle's winners (4 to 13 of 15 had a library run begin in the prior 24 months); runs that begin at the low print their first 252-high a median 68 to 226 sessions later | 7 of 7 (hindsight labels) | Yes (13 of 15; 122 sessions) |
| You join 8 weeks after the low | The index still beat the 12-month bill: +18%, +42%, +56%, +65%, +92%, +37% over 12 months (bills 14.2%, 10.9%, n/a, 22.0%, 20.1%, 12.0%) | 6 of 6 with 12 months of data | Yes (+92%) |
| Brent is flat or falling over the 13 weeks before the low | No oil shock in the low; the exception was the Mar 2026 low, which was the oil shock | 6 of 7 | Yes (-4%) |
| Import cover is at least 3 months | No default-risk low; the two lows under 2.1 months were Jan and Jun 2023 | 5 of 7 | Yes (3.2) |
| Mutual funds are net sellers and banks/DFI net buyers into the low | Weak: these held on 61% and 53% of all 20-session windows (both on 42%) | 7 of 7 | Yes (-6 / +6) |
| Six months on | Refiners or E&P were in the top four sectors (3 to 4 names each) in 6 of 7 turns; banks were in the top two in 3 (Jan 2023, Jun 2023, May 2025) and 15th of 16 in 2024 | 6 of 7; banks 3 of 7 | E&P 2nd, banks 15th |

## 9. The present, 16 Oct 2026

Each row is a signal earlier lows showed, measured the same way today. "Present" means the test passes; it does not say a low is in.

| Signal at the low | Lows showing it | Values at the seven lows (Aug 2019 / Mar 2020 / Jan 2023 / Jun 2023 / Jun 2024 / May 2025 / Mar 2026) | Today, 16 Oct 2026 | Status |
|---|---|---|---|---|
| Index 12% or more under its 252-session high | 5 of 7 | -33.0 / -37.0 / -17.7 / -8.3 / -4.5 / -13.0 / -22.6 | -12.0 | present |
| Index under its 200-session average | 5 of 7 | -23 / -24 / -9 / -3 / +19 / +3 / -7 | -3 | present |
| Index under its 50-session average | 6 of 7 | -14 / -30 / -7 / -3 / +1 / -10 / -18 | -4 | present |
| Under 10% of liquid names above their 50-day average | 5 of 7 | 0 / 0 / 2 / 20 / 50 / 7 / 1 | 16 | absent |
| Under 10% of liquid names above their 200-day average | 4 of 7 | 0 / 6 / 9 / 26 / 80 / 40 / 9 | 31 | absent |
| Index volume on the day below its 60-session mean (x) | 5 of 7 | 0.64 / 0.80 / 1.50 / 0.89 / 0.68 / 1.25 / 0.89 | 0.52 | present |
| At least one policy cut in the prior 180 days | 4 of 7 | 0 / 2 / 0 / 0 / 1 / 3 / 1 | 0 | absent |
| No policy hike in the prior 60 days | 5 of 7 | 31d / 253d / 53d / 80d / 351d / 682d / 987d | 172d | present |
| 6M bill cutoff 0.25 pt or more under the policy rate then in force | 1 of 7 | +0.70 / +0.30 / +0.83 / +0.97 / -1.00 / -0.00 / +0.24 | +0.90 | absent |
| Real policy rate (policy minus latest CPI) above zero, pt | 4 of 7 | +2.9 / -1.9 / -8.5 / -17.0 / +8.8 / +10.7 / +3.5 | +1.2 | present |
| CPI y/y lower than three months earlier, pt | 3 of 7 | +1.5 / -0.7 / +1.4 / +6.4 / -11.3 / -2.2 / +0.8 | -0.8 | present |
| Import cover (total reserves) at least 3 months | 5 of 7 | 3.6 / 4.8 / 2.0 / 2.0 / 3.2 / 3.1 / 4.0 | 4.8 | present |
| SBP reserves above their level 13 weeks earlier, $bn | 3 of 7 | -0.6 / +1.1 / -3.0 / -0.2 / +1.2 / -1.1 / +1.8 | +4.2 | present |
| USD/PKR within 1.5% of its level 13 weeks earlier, % | 4 of 7 | +8.0 / +3.2 / +4.2 / +1.1 / -0.2 / +0.9 / -0.4 | -0.4 | present |
| Current account positive over the last 3 known months, $m | 3 of 7 | -3150 / -2115 / -1460 / +826 / +674 / +749 / -40 | -1354 | absent |
| Brent not up more than 20% in 13 weeks, % | 6 of 7 | -20 / -63 / -6 / -0 / -4 / -17 / +49 | +52 | absent |
| IMF staff-level or Board event from 60 days before to 45 days after | 5 of 7 | yes / no / no / yes / yes / yes / yes | yes | present |
| KSE100 P/E between 7.0 and 10.5 (from 2022 only) | 5 of 5 | n/a / n/a / 7.2 / 7.1 / 8.7 / 10.0 / 9.5 | 8.1 | present |
| Mutual funds net sellers over the prior 20 sessions, USD m | 7 of 7 | -50 / -26 / -15 / -16 / -6 / -141 / -50 | -35 | present |
| Banks / DFI net buyers over the prior 20 sessions, USD m | 7 of 7 | +6 / +26 / +21 / +3 / +6 / +121 / +89 | +21 | present |
| Foreign net sellers of USD 50m or more over the prior 20 sessions | 2 of 7 | +18 / -79 / -13 / +6 / +8 / -8 / -289 | -9 | absent |
| Individuals net buyers over the prior 20 sessions, USD m | 5 of 7 | +23 / +7 / -0 / +6 / -17 / +17 / +1 | +22 | present |
| No lower close in the 40 sessions after the low (known only afterwards) | 7 of 7 (by selection) | each low is the lowest close of its episode | no low identified | unknown |
| First liquid-name 252-high within 10 sessions of the low (afterwards) | 4 of 7 | 63 / 16 / 7 / 2 / 2 / 2 / 20 sessions | 3 names (ATRL, NRL, PRL) on 16 Oct; nothing to count from | unknown |
| Three or more liquid names at 252-highs in one session within 10 sessions (afterwards) | 3 of 7 | none / none / none / yes / yes / yes / none | no low identified | unknown |
| Index back above its 50-session average within 30 sessions of the low (afterwards) | 7 of 7 | 19 / 26 / 12 / 1 / 0 (never below) / 2 / 20 sessions | below it now (-3.6%) | unknown |

Not in the table: SBP MPC on 26 Oct (Topline survey of 17 Oct: 61% expect a hike; catalyst calendar), October CPI on 2 Nov, the 4th-review IMF Board (staff-level agreement 8 Oct; date not found), $3bn of Eurobonds (MPS 14 Sep), Moody's B3 and S&P B upgrades (Aug, Jul). The index is 12.0% under its 23 Jan peak and 13.6% over the 9 Mar low; on depth it sits between the 2024 pullback (-4.5%) and the two shock lows (-13.0%, -22.6%). The post-low rows cannot be filled in from here.

## 10. Limits

Seven lows in five regimes make every "x of 7" descriptive. The lows, library starts and run classes are hindsight; first-252-high lists and checkpoints are point in time. Leader returns omit costs, tax and fills. The 13 Jun jump has no verified cause. Quarterly profits and the September 2026 CPI are unverified against filings. Intraday index columns (about 99% consistent with closes) were used only for the 2024 retest.
