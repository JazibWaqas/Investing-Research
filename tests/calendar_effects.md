# PSX calendar effects, 17 October 2026

## Hypothesis

Month, federal budget, SBP Monetary Policy Committee (MPC), Ramadan, company results season, and turn-of-month timing may alter returns enough to change when a monthly Rs50k deposit is invested.

## Data

Daily liquid equal-weight (EW) stock returns and KSE100 closes from 2017 through 16 October 2026. EW uses each stock's *prior* 60-session median traded value above Rs5m. Raw OHLCV yields 456 usable symbols; 466 moves above 10.5% with prior close above Rs10 are zeroed and logged. [Script](../scripts/codex/calendar_effects.py) and [full output](out/calendar_effects.txt) include every episode. The October 2026 month and Q4 results season are incomplete and excluded.

## Method

Monthly rows compound each month's trading days. Budget PRE is five trading days strictly before presentation; POST is five strictly after. MPC PRE/POST use ten days, excluding announcement day. Ramadan uses 30 calendar days beginning with the locally observed first fast, an approximate end. Results season windows are 20 Jan to 28 Feb, 20 Apr to 31 May, 20 Jul to 31 Aug, and 20 Oct to 30 Nov; the adjoining periods are off-season. Turn-of-month (TOM) is prior month's last session plus the next month's first three. Each event is compared with 100 random same-length windows from its year. `n` counts windows, `yr` independent years; MPC has 72 announcements but only 68 clusters separated by more than 28 calendar days. All table values except `n/yr` are percentages. A hypothetical timing round trip costs 0.5%; compare mean minus 0.5 with placebo, not just zero.

Budget dates used: 2017-05-26, 2018-04-27, 2019-06-11, 2020-06-12, 2021-06-11, 2022-06-10, 2023-06-09, 2024-06-12, 2025-06-10, 2026-06-12. Sources: [APP 2017](https://www.app.com.pk/national/budget-2017-18-at-a-glance/), [APP 2018](https://www.app.com.pk/budget/budget-2018-19/page/2/), [Finance Division archive 2019-2025](https://finance.gov.pk/downloads.html), [APP 2020](https://www.app.com.pk/national/text-of-federal-budget-2020-21-speech/), [APP 2021](https://www.app.com.pk/national/govt-presents-rs-8-487tr-federal-budget-with-19-increase-despite-covid/), [APP 2022](https://www.app.com.pk/budget/budget-2022-23/rs-9-502-trillion-federal-budget-2022-23-at-a-glance/), [APP 2023](https://www.app.com.pk/budget/federal-budget-2023-24/government-presents-finance-bill-2023-in-national-assembly/), [Finance Division 2024](https://www.finance.gov.pk/budget/Budget_2024_25/Budget_Speech_Urdu.pdf), [APP 2025](https://www.app.com.pk/national/finance-minister-aurangzeb-unveils-rs17-573-trillion-federal-budget/), [AP 2026](https://apnews.com/article/7489d3dcf439da0ad106c3a85884e480). No budget date is assumed.

Ramadan first-fast dates used: 2017-05-28, 2018-05-17, 2019-05-07, 2020-04-25, 2021-04-14, 2022-04-04, 2023-03-23, 2024-03-12, 2025-03-02, 2026-02-19. Sources: [Dawn 2017](https://www.dawn.com/news/1335573/moon-not-sighted-ramazan-to-begin-from-sunday), [Dawn 2018](https://www.dawn.com/news/1408056/), [Dawn 2019](https://www.dawn.com/news/amp/1480651), [timeanddate 2020-2026](https://www.timeanddate.com/holidays/pakistan/ramadan-begins), [Business Recorder 2023](https://www.brecorder.com/news/40232902), [APP 2024](https://www.app.com.pk/domestic/moon-sighted-ist-ramazan-tomorrow/), [APP 2026](https://www.app.com.pk/national/ramazan-moon-sighted-ist-fast-on-february-19-in-pakistan-khabeer-azad/). The 30-day *end* is assumed, since local Eid moon sighting varies.

## Results

`EW` is liquid equal-weight. `Pbo` is placebo mean. Win is fraction of positive windows. Best and worst are single windows.

| Effect | Market | n/yr | Mean | Median | Win | Best | Worst | Pbo |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Budget POST | EW | 10/10 | -0.51 | -0.11 | 40.00 | 3.87 | -7.00 | 0.13 |
| Budget POST | KSE100 | 10/10 | -0.37 | -0.09 | 40.00 | 7.47 | -7.75 | 0.19 |
| Budget PRE | EW | 10/10 | 0.30 | 1.50 | 60.00 | 5.13 | -6.05 | -0.03 |
| Budget PRE | KSE100 | 10/10 | 0.25 | 0.24 | 60.00 | 3.75 | -3.16 | 0.24 |
| Month 01 | EW | 9/9 | 2.96 | 2.02 | 66.67 | 15.86 | -4.65 | 0.98 |
| Month 01 | KSE100 | 10/10 | 3.58 | 2.09 | 80.00 | 10.07 | -0.76 | 0.99 |
| Month 02 | EW | 10/10 | -3.95 | -2.99 | 10.00 | 5.05 | -11.81 | 0.66 |
| Month 02 | KSE100 | 10/10 | -2.43 | -1.48 | 10.00 | 4.19 | -8.76 | 0.51 |
| Month 03 | EW | 10/10 | -3.31 | -0.18 | 50.00 | 5.31 | -22.97 | 0.36 |
| Month 03 | KSE100 | 10/10 | -2.62 | -0.91 | 40.00 | 5.37 | -23.04 | 1.07 |
| Month 04 | EW | 10/10 | 2.93 | 0.76 | 50.00 | 24.90 | -9.08 | 0.64 |
| Month 04 | KSE100 | 10/10 | 2.82 | 1.55 | 60.00 | 16.69 | -5.50 | 0.73 |
| Month 05 | EW | 10/10 | 1.90 | 3.28 | 60.00 | 14.34 | -7.16 | 0.84 |
| Month 05 | KSE100 | 10/10 | 1.78 | 1.04 | 50.00 | 8.21 | -5.81 | 0.99 |
| Month 06 | EW | 10/10 | -0.83 | -0.52 | 50.00 | 7.17 | -11.11 | 0.76 |
| Month 06 | KSE100 | 10/10 | -0.69 | -0.42 | 50.00 | 4.96 | -7.96 | 0.66 |
| Month 07 | EW | 10/10 | 2.72 | 1.01 | 60.00 | 20.43 | -13.17 | 1.08 |
| Month 07 | KSE100 | 10/10 | 2.88 | -0.67 | 40.00 | 15.88 | -5.79 | 1.01 |
| Month 08 | EW | 10/10 | 0.25 | 0.70 | 50.00 | 9.49 | -13.06 | 0.70 |
| Month 08 | KSE100 | 10/10 | -0.73 | 0.64 | 60.00 | 6.62 | -10.44 | 1.32 |
| Month 09 | EW | 10/10 | -1.01 | -2.68 | 40.00 | 10.46 | -12.92 | 0.60 |
| Month 09 | KSE100 | 10/10 | 1.32 | 0.71 | 50.00 | 11.36 | -5.31 | 0.67 |
| Month 10 | EW | 9/9 | 1.11 | -1.00 | 44.44 | 11.59 | -12.66 | 0.54 |
| Month 10 | KSE100 | 9/9 | 2.53 | 1.59 | 66.67 | 12.30 | -6.58 | 1.36 |
| Month 11 | EW | 9/9 | 6.60 | 1.73 | 77.78 | 24.03 | -3.28 | 0.97 |
| Month 11 | KSE100 | 9/9 | 5.54 | 2.96 | 77.78 | 16.59 | -2.77 | 1.26 |
| Month 12 | EW | 9/9 | 1.19 | -0.34 | 44.44 | 17.22 | -10.73 | 1.01 |
| Month 12 | KSE100 | 9/9 | 2.05 | 3.17 | 66.67 | 13.59 | -8.47 | 1.40 |
| MPC POST | EW | 72/10 | 0.84 | 0.72 | 58.33 | 15.86 | -14.39 | 0.41 |
| MPC POST | KSE100 | 72/10 | 0.88 | 1.11 | 56.94 | 10.07 | -9.54 | 0.55 |
| MPC PRE | EW | 72/10 | -0.90 | -0.87 | 45.83 | 15.92 | -23.63 | 0.37 |
| MPC PRE | KSE100 | 72/10 | -0.31 | -0.33 | 50.00 | 12.77 | -19.76 | 0.62 |
| Ramadan | EW | 10/10 | -2.66 | -0.07 | 50.00 | 7.64 | -20.28 | 0.63 |
| Ramadan | KSE100 | 10/10 | -0.74 | 0.92 | 70.00 | 6.93 | -14.60 | 1.20 |
| Off-season | EW | 39/10 | 1.06 | 2.42 | 56.41 | 18.95 | -16.58 | 1.12 |
| Off-season | KSE100 | 39/10 | 2.35 | 1.06 | 53.85 | 15.80 | -13.56 | 1.75 |
| Results | EW | 39/10 | 1.06 | -0.22 | 48.72 | 25.94 | -14.25 | 0.98 |
| Results | KSE100 | 39/10 | 1.30 | 0.29 | 53.85 | 20.18 | -12.01 | 1.37 |
| TOM | EW | 108/10 | 0.90 | 1.03 | 62.96 | 19.56 | -10.86 | 0.16 |
| TOM | KSE100 | 108/10 | 0.62 | 1.21 | 60.19 | 12.84 | -7.77 | 0.22 |

## Robustness

February EW loses in nine of ten years, averaging -5.43% in 2017-2021 and -2.47% in 2022-2026. KSE100 averages -3.29% and -1.57% in those halves. November EW averages +4.35% then +9.42%, but the median over nine years is only +1.73%, with large winners driving the mean. TOM EW is stable at +0.92% then +0.88%, but its gross advantage over same-year placebo is 0.74%, or about 0.24% after 0.5% cost. Results season has the same cumulative EW mean as the longer off-season windows, which gives no clear edge. June is weak, July positive on EW but has a negative KSE100 median, and December has a negative EW median. Budget and MPC windows lack a consistent edge after costs.

## Verdict

February is the only plausible deposit-timing candidate: the EW mean drop of 3.95% would be about Rs1,975 on Rs50k before costs, with 9 of 10 February windows negative. This is an exploratory calendar screen across twelve months, not a validated rule to hold a monthly deposit in cash. November is strong historically, but a deposit arriving in November can simply be invested promptly. No other calendar effect justifies delaying a Rs50k deposit.

## Caveats

The 30-day Ramadan proxy may include or omit a trading session. Budget dates were identified retrospectively; the PRE test assumes the planned presentation date was known then. Results seasons are fixed calendar proxies, not company announcement dates, and off-season windows differ in length, so cumulative returns are not directly comparable. MPC windows can overlap even when announcement clusters are counted separately. Returns exclude cash dividends and use a rough bonus/split filter, not verified corporate-action adjustments. KSE100 uses a raw price index, so EW and KSE dividend treatment differs. The sample spans one long rerating and ten years at most; month screening raises false-discovery risk. This tests aggregate market entry, not the exact KMI-compliant basket or deposit arrival day.
