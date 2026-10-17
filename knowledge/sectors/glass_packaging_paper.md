# Glass, packaging and paper sector note

As of 2026-10-17. Prices, P/E and dividend yield come from `seed/data/fundamentals/screener_20261016.csv` (16 Oct close). Results come from stockanalysis.com quarterly tables and PSX filings (June year-end except PKGS, which is December). Anything not sourced is marked "unverified". The web search tool hit its budget during this run, so news-based levers (gas tariff, resin, pulp, waste paper, anti-dumping) are mostly not found. Price returns are price only, with gaps over 10.5% treated as corporate actions.

## 1. How this sector makes money

1. **Selling price minus energy and raw-material cost.** Glass (TGL, GHGL, GGGL, GVGL) burns gas in furnaces and imports soda ash. Paper and board (CEPB, PKGS) buy waste paper, pulp, coal and gas. Films and flexibles (IPAK, MACFL, CPPL, SPEL, ECOP) buy polypropylene, PET and aluminium, which follow Brent. TGL's gross margin fell to 28.9% in FY26 from 31.0% in FY25 on lower selling prices. GHGL's rose to 28.9% from 27.1%. CEPB's was only 6.6%.
2. **Capacity and imports.** Glass has excess capacity. TGL's FY26 report says this "may continue to exert pressure on selling prices and margins". It has a rebuilt 550 t/day float furnace sitting idle and a Lucky Core JV (1,000 t/day) on hold. Whether the idle furnace restarts decides float glass pricing.
3. **Interest rate and leverage.** Packages (PKGS) has about Rs138bn of consolidated debt and Rs7.3bn of half-year finance cost. CEPB's interest cover is 1.42x, against 11.5x in FY21 (annual report ratios). TGL and GHGL are net cash. Rate moves hit the levered paper names and barely touch glass.
4. **End-market volume.** Float glass follows construction and autos, containers follow pharma and beverages, and packaging follows FMCG. Large-scale manufacturing grew only 0.67% in August.
5. **Tax and payout.** TGL's effective tax rate is about 40%. Payout is the other lever. GHGL paid Rs4 over the last 12 months, while TGL paid only the Rs5 interim for FY26.

## 2. Where each lever stands today

| Lever | Latest datapoint | Date | Source |
|---|---|---|---|
| Brent (film resin proxy, glass energy) | US$126.6 on 14 Oct. Spiked to 126.7 in March, fell to 70.5 in June, back above 120 | 14 Oct | repo `data/macro/brent.csv` |
| Policy rate, inflation | 11.5% held. August CPI 11.15% | 14 Sep | https://www.sbp.org.pk/assets/document/publications/MPS-Sep-2026-Eng.pdf ; https://tradingeconomics.com/pakistan/interest-rate |
| Glass margins | TGL FY26 gross profit Rs8.9bn, down 15% on sales down 8.5%. TGL 4Q EPS 6.19 against 5.14 in 1Q | 24 Sep | https://dps.psx.com.pk/download/document/283378.pdf |
| Glass demand | TGL says construction revival is gradual. GHGL cites the Iran conflict raising gas, energy and raw-material cost | Oct | PSX annual reports 284469 and 285037 |
| Industry volume | August LSM +0.67% YoY, 2MFY27 +1.85%, non-metallic minerals +0.20%. Paper and board not reported | 17 Oct | https://www.dawn.com/news/2037724/big-industry-output-posts-meagre-rise |
| Power cost | Power Division projects Rs2.56/unit rise in November bills | Oct | https://www.dawn.com/news/2037388/ |
| Chinese competition | Glassware imports from China are about US$200m a year or less. Paper and packaging not covered | 12 Oct | https://www.dawn.com/news/2036527/reality-of-chinese-imports |
| Industrial gas tariff, resin, pulp, waste paper, PKR | Not found. OGRA notices are scanned images. PKR about 268 to 277, unverified | n/a | https://www.ogra.org.pk/consumer-gas-prices |
| FY27 budget items for glass, paper, packaging | None found | Jun | https://propakistani.pk/budget-2026-live/ |

## 3. What changes in the next 1 to 3 months

- **21 Oct:** GHGL goes ex-dividend for the Rs1 final (book closure 22 to 28 Oct; ex-date is my inference). **19 to 26 Oct:** IPAK closure for the Rs2 final, and it already trades XD. ECOP (Rs3, closure 15 to 28 Oct) is also XD.
- **26 Oct:** SBP MPC (date from Trading Economics, not confirmed on SBP). With CPI at 11% and Brent above US$120 a hike is possible. That hurts PKGS, CEPB and IPAK most. IPAK AGM is the same day, TGL AGM 28 Oct (no dividend).
- **Late October:** 1QFY27 results for the June-year names, and PKGS nine-month results. GHGL announced 1QFY26 on 28 Oct last year, so expect about the same. Board dates are unconfirmed. GHGL's base is easy: 1QFY26 EPS was 0.71 against 2.29 and 2.54 in the next two quarters.
- **November:** electricity bills rise by Rs2.56/unit. No industry volume series for glass or paper was found, so watch the September LSM release (mid-November, cadence assumed).
- **Dec to Feb:** the next MPC (December date unverified), then half-year results and interim dividends in February (TGL 50% on 24 Feb 2026, GHGL 10%, CPPL 10%, SPEL 10%).
- **Unscheduled:** TGL restarting its idle float furnace (negative for float prices), Brent direction, any anti-dumping notice.

## 4. Exposed KMI names

KMI All Share members: TGL, GHGL, GGGL, GVGL, PKGS, CPPL, IPAK, ECOP, CEPB, MERIT, SPEL, MACFL, RPL (this is the ROSHAN you meant), GEMPAPL. Not in KMI: TRIPF (All Share only), BGL. Liquidity is price times 30-day average volume.

| Symbol | P/E | DY % | Rs m/day | Exposure | View |
|---|---|---|---|---|---|
| TGL | 6.8 | 5.2 | 21.2 | Float and tableware price, gas. Net cash Rs2.2bn, P/B 1.0 | Cheap but FY26 EPS fell 16%. Idle furnace caps upside |
| GHGL | 5.4 | 8.8 | 8.2 | Containers, tableware, gas. Net cash Rs5.9bn, P/B 0.93 | Best quality here. EPS 7.23, up 22% |
| GGGL | 13.3 | 0 | 2.4 | Glass, small | Illiquid, thin margins |
| GVGL | 7.8 | 3.5 | 1.0 | Glass | Too illiquid |
| PKGS | 20.5 | 2.0 | 3.5 | Paper, flexibles, rates. P/B 0.69, heavy debt | Earnings lumpy: 4Q25 loss Rs1.6bn. Rate hike is the risk |
| CEPB | n/a (loss) | 0 | 9.2 | Board price, waste paper, rates. Net debt Rs11.7bn | Turned profitable only in 4Q (Rs277m). Not yet proven |
| CPPL | 7.0 | 4.1 | 4.3 | Packaging, rates. P/B 0.47 | FY26 EPS 13.3 is mostly one quarter (4Q Rs536m). Treat as unproven |
| IPAK | 17.6 screener, 4.7 on filings | 5.7 | 42.3 | BOPP/BOPET films, resin, oil. Net debt Rs12.8bn | Screener P/E looks stale. 4Q margin 31% against about 19%, so inventory gain risk |
| ECOP | 5.2 | 5.1 | 10.3 | Packaging | Went ex-dividend. Small |
| MERIT | 14.9 | 0 | 1.4 | Packaging | Loss-making gross margin. Avoid |
| SPEL | 6.6 | 1.9 | 5.3 | Flexible and pharma packaging | FY26 EPS 5.99 against 6.60 |
| MACFL | 45.6 | 0 | 141.7 | BOPP films | Up 261% in a year, down 10% (limit) on 16 Oct. Momentum name, not valuation |
| RPL | 15.0 | 6.1 | 5.8 | Packaging | Fully priced |

## 5. Past big moves, 2017 to 2026 (versus KMI All Share, price only)

**Aug 2019 to Dec 2020: paper and packaging up 100 to 450%.** CEPB +450%, CPPL +357%, SPEL +183%, PKGS +101%, glass +86 to +133%, against KMI +46%. The trough was 16 to 19 Aug 2019. SBP raised to 13.25% on 16 Jul 2019, then cut 650bp between 17 Mar and 25 Jun 2020 (repo `policy_rate_decisions.csv`). CEPB's interest cover was 11.5x in FY21, against 1.4x now, which shows how much a low-rate year lifts a levered board maker. The product-price side is unverified. Signal: highly levered, low-P/B names at a rate peak, with the first cut on 17 Mar 2020. Honest caveat: the bottom came seven months before the first cut, so the rate cut alone did not time it.

**Sep 2022 to Mar 2024: glass and small packaging lagged by 50 to 120 points.** GGGL -66%, ECOP -46%, GHGL -26%, against KMI +52% (TGL +17% was the exception). The policy rate went from 15% to 22% and the market re-rated from low single-digit P/E. GHGL's EPS slid from 8.10 (FY23) to 6.75 (FY24) to 5.90 (FY25). Signal: falling EPS plus the TGL-reported excess capacity, visible in each annual report, while the market rallied elsewhere.

**Jan to Oct 2026: oil shock round trip.** Brent went from 71 to 127 in March. TGL fell 44% from 234.89 (16 Jan) to 131.08 (30 Mar) against KMI -20%, then rose 56% to 204.65 (7 Jul) against KMI +26%, and now sits at 159.7. Both reports cite the Iran conflict and energy costs. Signal: the Brent daily series crossing 100 in March. It flagged the fall but gave no entry, since the rebound began on the same trough.

Idiosyncratic spikes exist too: SPEL +130% (Jul to Sep 2024) and ECOP +143% (Apr to Jun 2025) against KMI +3% and +4%. SPEL's FY25 EPS then doubled to 6.60 from 3.36, so price led earnings. The ECOP cause is not found.

## 6. What a veteran watches weekly

1. Brent and resin: repo `data/macro/brent.csv`, daily. Spike means film inventory gains, then margin squeeze.
2. PSX company announcements: https://dps.psx.com.pk/announcements/companies, daily. Board dates, results, dividends.
3. SBP policy and PKR: https://www.sbp.org.pk, MPC about every 6 weeks, interbank daily.
4. Weekly SPI and monthly CPI: https://www.pbs.gov.pk, SPI on Fridays, CPI in the first days of the month.
5. LSM: https://www.pbs.gov.pk, mid-month. Check non-metallic minerals and paper.
6. OGRA gas and RLNG notices: https://www.ogra.org.pk, fortnightly and 1 July. Industrial gas tariff drives glass.
7. NEPRA fuel adjustment: https://www.nepra.org.pk, monthly.
8. NTC anti-dumping notices (unverified URL: https://ntc.gov.pk): irregular, for glass and board.
9. Idle TGL furnace and Lucky TG JV: TGL announcements.

## 7. Evidence and dates

- Screener `seed/data/fundamentals/screener_20261016.csv` (16 Oct 2026).
- stockanalysis.com quarterly, annual and statistics pages for TGL, GHGL, PKGS, CEPB, CPPL, IPAK, ECOP, SPEL, MERIT, GGGL (read 17 Oct 2026). PKGS and IPAK EPS columns conflict with net income, so I used net income and market cap.
- PSX filings: TGL results 283378 and annual report 284469, GHGL annual report 285037, IPAK results 282487, PKGS Shariah disclosure 282741, CEPB annual report 284308.
- Repo: `data/prices_raw`, `data/macro/kmiallshr.csv`, `brent.csv`, `policy_rate_decisions.csv`, `data/payouts_raw.csv`.
- Dawn (12 and 17 Oct), ProPakistani budget page, Trading Economics, OGRA site.

## Gap resolution (17 Oct 2026, Codex)

- [SBP's published calendar](https://www.sbp.org.pk/m_policy/mp-comm-semi.asp) confirms MPC meetings on 26 October and 14 December 2026. The earlier note's 26 October date was correct, while its unspecified December date can now be replaced with 14 December for monitoring.
- [GHGL's PSX page](https://dps.psx.com.pk/company/GHGL) records the 6 October AGM notice and 7 October FY26 annual report transmission. The note's 21 October ex-date is still an inference from book closure, not a separately verified exchange ex-date. [OGRA's decision index](https://www.ogra.org.pk/decisions-3) does not provide a current industrial gas tariff for these named mills; input-cost attribution remains unverified.
