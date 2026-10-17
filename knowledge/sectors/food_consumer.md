# Food, beverages and consumer staples sector note

As of 2026-10-17. Prices, P/E and dividend yield come from `seed/data/fundamentals/screener_20261016.csv` (16 Oct close). Web search quota ran out early in this session, so there is no sell-side research, no OGRA or APCMA data, and no edible oil, ghee, milk or sugar-mill price series. Those gaps are marked "unverified" or "not found" below. KMI check: NATF, SHEZ and PAKT are not in KMI All Share (screener `listed_in`; NATF and SHEZ also absent from `data/kmi_allshare_2026-06-05.csv`), so they are out of the investable universe. NATF is covered only as a read-across.

## 1. How this sector makes money

1. **Gross margin spread over raw materials.** Milk, palm and soy oil, wheat, sugar, tinplate and PET are the inputs. The spread decides profit. FCEPL gross margin went 12.0% (Dec 2025 quarter) to 21.0% (Mar 2026) to 23.2% (Jun 2026), taking quarterly profit from Rs0.6bn to Rs2.5bn on flat sales. Nestle sits near 39% and Colgate near 35%, both stable.
2. **Pricing power against consumer squeeze.** CPI is about 11% and wheat flour is up 35% YoY, so volumes are the risk. Nestle's June quarter sales rose 4% YoY but profit fell 19.5%. Multinationals pass on price; small names cannot.
3. **PKR and imported inputs.** Palm oil is priced in USD, and Nestle and Colgate import inputs and pay royalties. PKR has been flat near 277 for two years, which removes the 2018-19 and 2022-23 margin shock.
4. **Tax and regulation.** FED on beverages, sales tax, super tax, and now a possible PET bottle ban in Islamabad. A proposed 20% FED on low-sugar beverages was scrapped in the FY27 budget.
5. **Governance and balance sheet.** Working capital heavy names (edible oil, rice, dairy) live on short-term financing at an 11.5% policy rate. In small caps, filings, auditors and probes drive price more than margins.

## 2. Where each lever stands today

| Lever | Latest datapoint | Date | Source |
|---|---|---|---|
| Input cost: palm oil | US$1,180/t in September, 1,037 a year earlier (+14%) | Sep 2026 | repo `data/macro/palm_oil.csv` |
| Input cost: wheat flour, sugar | Flour +35.1% YoY, +3.4% WoW. Sugar -23.2% YoY. Tea +8.4% YoY. Eggs -19.8% | week to 15 Oct | https://www.dawn.com/news/2037605/short-term-inflation-surges-to-1138pc-due-to-costly-food |
| Weekly SPI headline | 11.38% YoY | 16 Oct | same |
| Cooking oil, ghee, milk prices | not found | n/a | unverified |
| Inflation and rates | CPI 11.1% (Aug). Policy rate 11.5%, held 14 Sep, majority 7 of 10, citing Middle East conflict and commodity prices | Sep 2026 | https://www.sbp.org.pk/assets/documents/press-release/PR-14-Sep-2026.pdf |
| PKR | about 277 per USD (a 268 print on 8 to 13 Oct looks like a data glitch) | 12 Oct | repo `data/macro/usdpkr.csv` |
| Margins | FCEPL 23.2% (Jun qtr), Nestle 39.0%, Colgate FY26 35.0% | Jun 2026 | https://stockanalysis.com/quote/psx/FCEPL/financials/?p=quarterly and NESTLE, COLG equivalents |
| Regulation | Govt and Nestle, Coca-Cola, PepsiCo, Metro in deadlock over Islamabad PET ban; Pak-EPA says no legal basis; talks continue next week | 17 Oct | https://tribune.com.pk/story/2635300/govt-mncs-in-deadlock-over-pet-bottle-ban |
| Budget | 20% FED on low-sugar water and drinks dropped | 24 Jun | https://www.dawn.com/news/2010463/budget-2026-27-finance-bill-sails-through-na |

## 3. What changes in the next 1 to 3 months

Q3 (September quarter) results season, mostly in the next two weeks. Dates from PSX board notices:

- **21 Oct, 11:00:** RMPL board, Q3 results. Last year's Q3 interim was Rs130 per share, announced 30 Oct 2025.
- **Nestle:** board notice filed 13 Oct, meeting date not found. Last year Q3 results came 16 Oct with Rs78 interim, book closure 27 to 29 Oct. Expect results and an interim dividend within days.
- **23 Oct, 14:30:** UPFL board, Q3. Closed period to 24 Oct.
- **23 Oct, 15:30:** FCEPL board, Q3 accounts. New CEO Usman Zaheer Ahmad joins 16 Nov.
- **26 Oct:** NATF AGM (5-for-1 split) and Q1 board. Not KMI.
- **About 28 Oct:** MFL AGM (date read from a garbled notice, unverified).
- **22 to 28 Oct:** ISIL book closure, final dividend 50%.
- **Matco Foods:** IGI Investments made a non-binding offer for 100% of subsidiary Matco Corn Products on 15 Oct. Arif Habib is sell-side advisor. No price disclosed.
- **UNITY:** FY26 annual accounts are not on the PSX page, and no board notice exists. Statutory deadline is about end October (unverified).
- **PET ban:** follow-up meetings in the week of 19 Oct.
- **Weekly:** PBS SPI every Thursday. Monthly CPI early November. Next SBP MPC date not found; the last four gaps were about 6 to 7 weeks, so a November meeting is likely.
- **Seasonal:** Ramadan starts about 8 Feb 2027, so dairy and beverage restocking shows in Dec to Feb quarters.

## 4. Exposed KMI names

Liquidity is volume_avg_30d x price. P/E is from the screener (may be standalone; see notes).

| Symbol | Levers (+ helps, - hurts) | P/E | DY % | Liquidity Rs m/day | View |
|---|---|---|---|---|---|
| FCEPL | Milk and sugar cost (-), margin recovery (+), CEO change (-) | 19.8 | 3.07 | 90.5 | Trailing EPS 7.53 vs 3.51 in FY25, stock +57%. Priced for the margin to hold; 23 Oct print decides. |
| MFL | Rice export, IGI offer for corn unit (+) | 22.0 | 0 | 82.7 | Screener P/E is standalone. Consolidated FY26 EPS is about 4.62, so about 10x (lesson 1). Event driven. |
| PREMA | Dairy input cost, financing (-) | 8.6 | 0 | 56.5 | FY26 EPS about 3.75 vs 2.48, down 24% in a year. Cheap but small and volatile. |
| UNITY | Palm oil (-), governance (-) | 6.5 | 0 | 36.2 | FIR on current and former officers, CFO and secretary resigned. Not investable until filings are clean. |
| TOMCL | Meat export, margins (-) | 41.4 | 0 | 34.7 | Q4 FY26 loss. FY26 EPS about 0.56. Expensive. |
| TREET | Consumer goods, PKR (-) | 8.1 | 0 | 99.6 | Q4 profit Rs0.53bn, nine-month loss near zero. Not classic staples. |
| COLG | Pricing power (+), flat volumes | 14.4 | 5.14 | 16.7 | Steady, EPS 76.7 FY26, Rs35 final. Thin liquidity. |
| NESTLE | Pricing (+), PET ban (-), input cost | 18.8 | 7.14 | 3.4 | Profit down 19.5% in June quarter, payout near 97% of H1 EPS. Illiquid. |
| UPFL | Pricing, wheat, edible oil (-) | 22.5 | 5.32 | 1.9 | June half profit Rs4.3bn. Illiquid. |
| RMPL | Corn price, PKR (+) | 11.6 | 4.56 | 0.5 | Q2 EPS Rs225. Illiquid, around 59 shares a day. |
| QUICE | n/a | n/a | 0 | 12.9 | Up 229% in a year, P/E 42,457 is meaningless. Avoid. |
| ISIL, MFFL, SOYASUPXD, ASCNC, BBFL, GDL | not assessed | | | ISIL 0.05, MFFL 3.8, SOYASUP 20.3, ASCNC 7.5, BBFL 20.8, GDL 22.4 | Listed for completeness. |

## 5. Past big moves, 2017 to 2026

Relative to KMI All Share (`data/macro/kmiallshr.csv`), raw closes from `seed/data/prices`.

1. **Unity Foods rally, Jun 2020 to Jun 2021: +299% vs index +35%.** Palm oil rose from US$577/t (May 2020) to 1,136 (May 2021), and Unity's price rose from 11.15 to 44.52. Knowable early: palm oil was already up 14% from May to June 2020 (577 to 656), and Unity went from 11 to 32 by December while palm was still 1,016. Signal: palm price momentum plus a large local refiner with operating leverage. FY21 EPS was Rs3.61, confirmed after the move.
2. **Unity collapse, Feb to Mar 2026: -59% vs index -18%.** Price held near Rs20 through 11 Feb, then fell to 7.89 by 30 Mar on volume spikes (9.5m shares 13 Feb, 117m on 4 Mar). The only PSX notice was an emergent board meeting on 10 Feb "not for financial results". The SECP referral (25 Aug) and FIR (29 Aug) came six months later. Signal: an unexplained emergent board meeting and a volume spike in a stock that has no dated filings after October 2025 on PSX. Whether the H1 and nine-month FY26 results were filed is not confirmed.
3. **Nestle, Mar 2018 to Sep 2019: -56% vs index -33%.** PKR went from 115 to 156 and the policy rate from 6.0% to 13.25%. Signal: a PKR devaluation and rate hike cycle that was visible monthly (SBP decisions). This was a macro bet, not a company one.
4. **FCEPL, Mar to Oct 2026: +89% vs index +12%.** Gross margin and profit inflected in the Dec 2025 quarter results (17 Feb). Price was 80 on 17 Apr, 94 on 27 Apr, 113 on 29 May, 156 on 1 Sep. The Q1 print on about 27 Apr was an entry with 65% still to run. Cause of the margin move: unverified.
5. **FCEPL 2017: -58% vs index -10%.** Cause not found; price series may contain an unflagged rights or bonus gap. Treat as unverified.

## 6. What a veteran watches weekly

| Item | URL | Cadence |
|---|---|---|
| PBS SPI (flour, sugar, tea, eggs, LPG) | https://www.pbs.gov.pk/ | Thursday |
| Monthly CPI, food and core | https://www.pbs.gov.pk/ | first days of month |
| SBP policy decisions and PKR | https://www.sbp.org.pk/m_policy/index.asp | about every 6 to 7 weeks |
| Palm oil, Brent | repo `data/macro/` refresh | weekly |
| PSX board notices and results | https://dps.psx.com.pk/announcements/companies | daily in results weeks |
| Payout and book closure dates | https://dps.psx.com.pk/company/NESTLE (and others) | per result |
| Governance flags: emergent board meetings, resignations, SECP referrals | PSX announcements | daily |
| PET ban talks, FED and sales tax | https://tribune.com.pk/business | weekly |

## 7. Evidence and dates

- PSX company pages, read 17 Oct 2026: https://dps.psx.com.pk/company/NESTLE, FCEPL, UPFL, RMPL, NATF, UNITY.
- PSX PDFs: Unity FIR https://dps.psx.com.pk/download/document/282080.pdf (1 Sep). Matco https://dps.psx.com.pk/download/document/285766.pdf (15 Oct). NATF split https://dps.psx.com.pk/download/document/282982.pdf (18 Sep). NATF board https://dps.psx.com.pk/download/document/285846.pdf (16 Oct). RMPL https://dps.psx.com.pk/download/document/285622.pdf. UPFL https://dps.psx.com.pk/download/document/283335.pdf. FCEPL https://dps.psx.com.pk/download/document/285710.pdf and 285754.pdf.
- Financials: https://stockanalysis.com/quote/psx/SYMBOL/financials/ for NESTLE, FCEPL, COLG, TREET, UNITY, TOMCL, PREMA, MFL.
- News: Dawn 16 Oct, Tribune 10 and 17 Oct, Dawn 24 Jun (links above). SBP statement 14 Sep.
- Repo data: `data/macro/*.csv`, `data/announcements.csv`, `seed/data/prices`.
- Not found: edible oil and ghee prices, milk price, sugar policy, tobacco FED, broker research, Nestle board date.

## Gap resolution (17 Oct 2026, Codex)

- The [PBS weekly SPI report for the week ended 15 October 2026](https://www.pbs.gov.pk/wp-content/uploads/2020/07/Executive-Summary-SPI-Report_15.10.2026.pdf), released 16 October, gives the national average refined-sugar retail price as Rs142.11/kg, down 23.20% YoY, and fresh milk as Rs218.92/litre, up 8.00% YoY. These are observable retail-price series for the note's sugar and milk gaps, although they do not establish a particular producer's margins or a policy decision.
- [Nestle's PSX page](https://dps.psx.com.pk/company/NESTLE), checked 17 October, had no accessible October 2026 Q3 board notice or result. The date and payout remain unverified; last year's 16 October print is not this year's announcement. The [SBP calendar](https://www.sbp.org.pk/m_policy/mp-comm-semi.asp) fixes the next MPC on 26 October, not an inferred November meeting.
