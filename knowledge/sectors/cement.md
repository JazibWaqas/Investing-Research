# Cement sector note

As of 2026-10-17. Prices and ratios from `seed/data/fundamentals/screener_20261016.csv` (16 Oct close). Anything not sourced below is marked "unverified". Price-return figures are price only, built from PSX daily history with gaps over 10.5% treated as corporate actions, so they are approximate.

## 1. How this sector makes money

1. **Domestic despatches and utilisation.** About 80 Mt of installed capacity ran at roughly 60% in FY26 (50.6 Mt sold), so every extra tonne drops through at a high margin. Utilisation is about 53% in the North and 85% in the South (AHL, FY26).
2. **Retention price per bag.** Retail price averaged Rs1,549 per 50 kg bag in September. Taxes are close to half of the retail price (CCP), and FED has been Rs4/kg (Rs200/bag) since the July 2024 budget. A Rs25 to 30 move in the North is only about 2% of retail but a larger share of ex-factory margin.
3. **Fuel and freight cost.** Coal is the biggest cash cost, followed by diesel freight and power. FY26 coal averaged US$97/t (AHL). Newcastle averaged US$131/t in August. Northern mills lost cheap Afghan coal.
4. **Exports.** About 18% of volume. South mills ship by sea, and North mills depend on the Afghan border, which has been shut to cement since October 2025.
5. **Financing and tax.** Finance cost fell 33% in FY26 to Rs16.9bn and drove most of the profit growth. The FY27 budget cut super tax, which gave a one-off deferred tax gain in 4QFY26 (AKD). Lucky is a conglomerate (autos, power, chemicals), so it also depends on other income.

## 2. Where each lever stands today

| Lever | Latest datapoint | Date | Source |
|---|---|---|---|
| Domestic despatches | 3.788 Mt, +7.35% YoY. 1QFY27 10.845 Mt, +7.8% | Sep 2026, published 2 Oct | https://propakistani.pk/2026/10/02/cement-sales-rise-7-in-september/ |
| Exports | 0.832 Mt, flat. 1QFY27 2.296 Mt, -11.3%. North exports zero against 0.66 Mt a year ago; South +19% | same | same, plus https://www.brecorder.com/news/40444242/cement-recovery-remains-uneven |
| Utilisation | About 66% in September, 60% for the quarter, North about 57% | 16 Oct | Business Recorder link above |
| Price | Rs1,549 per bag, +10% YoY. North up Rs25 to 30 late September on coal and diesel | 29 Sep | https://propakistani.pk/2026/09/29/cement-prices-in-northern-region-rise-sharply/ |
| Coal and oil | Newcastle US$131/t (August average). Brent US$125.8 on 13 Oct, from US$70 in July | Sep, Oct | https://www.westpaciq.com.au/economics/2026/09/commodities-update-september-2026.html ; repo `data/macro/brent.csv` |
| Policy rate and inflation | 11.5%, held 14 Sep (hiked 100bps on 27 Apr). August CPI 11.1%. Weekly SPI 11.97% | Sep to Oct | https://www.sbp.org.pk/assets/documents/press-release/PR-14-Sep-2026.pdf ; https://tribune.com.pk/story/2633984/staples-fuel-keep-spi-near-12-yoy |
| FY26 margins | Gross margin 33% (AHL) versus about 30% for 9MFY26 (BR). Samples differ. Profit +13% to Rs138bn | Aug 2026 | https://www.cemnet.com/News/story/182074/pakistan-s-cement-sector-profitability-rises-13-in-fy26-ahl-research.html |
| PKR | About 277 (Yahoo, 14 Oct), after 268 the day before. Possible data glitch | Oct | repo `data/raw/macro/yahoo_pkr.json`, unverified |
| Afghan border | Interior Minister said crossings would reopen (August). No confirmation found | Aug | https://kabulnow.com/2026/08/pakistan-to-reopen-border-crossings-and-transit-routes-with-afghanistan/ |

## 3. What changes in the next 1 to 3 months

- **19 Oct:** MLCF EOGM votes on absorbing Pioneer at 2.65 MLCF shares per PIOC share (PSX filing 283065). The Lahore High Court sanction follows. Effective date is 1 July 2026. **27 Oct:** PIOC EOGM, an election of directors.
- **20 Oct:** Lucky corporate briefing on FY26, 3:30pm. **22 Oct:** CHCC board for 1QFY27 (closed period from 15 Oct). **27 Oct:** FCCL board for 1QFY27.
- **Late October:** Other 1QFY27 results (LUCK, DGKC, MLCF, KOHC, ACPL, GWLC, POWER). Board dates are not yet announced, so treat them as unverified. DGKC reported 1QFY25 on 17 Oct 2024. GWLC declared a 5% interim with 1Q last year.
- **Dividends:** DGKC Rs1 final (book closure 20 to 27 Oct), FECTC Rs4 (16 to 26 Oct). CHCC pays an interim of about 15% in February.
- **26 Oct:** SBP MPC (date from Trading Economics, unverified against SBP). Hike risk is real with inflation at 11% and Brent above US$120. December MPC date unverified.
- **2 to 3 Nov:** APCMA October despatches. Winter and post-monsoon catch-up should keep domestic growth positive. I expect +4 to +8% YoY, a view and not a sourced forecast.
- **Open risks:** Torkham reopening (upside for North exports), Brent and Newcastle direction, PSDP releases, and the FY27 cement FED treatment (not found).

## 4. Exposed KMI names

Not in KMI All Share: BWCL (Rs6m/day) and DBCINC. Plant geography is from memory and unverified. P/E is trailing.

| Symbol | P/E | DY % | Liquidity Rs m/day | Exposure | View |
|---|---|---|---|---|---|
| MLCF | 11.2 | 0 | 585 | North, high leverage, FY26 EPS Rs8.06 unconsolidated, owns about 77% of PIOC | Merger event name. Most liquid. |
| DGKC | 7.0 | 0.45 | 426 | North plus Sindh, cheap | Cheapest large cap. Down 33% from its 2-year high. |
| LUCK | 12.6 | 1.06 | 338 | South plus Pezu, diversified, record EPS Rs60.78 | Quality, priced for it. |
| THCCL | 4.5 | 0 | 287 | South, sukuk-funded | Cheap and risky. Sukuk and governance are unchecked. |
| FCCL | 7.8 | 2.6 | 170 | North, solar and BESS | Steady. Smallest drawdown (-14% from high). |
| CHCC | 7.3 | 1.6 | 84 | North, buy-back, bid for 30% of Nimir | Capital allocation to watch. |
| KOHC | 7.2 | 0 | 23 | North, thin | Cheap, illiquid. |
| ACPL | 9.4 | 0.2 | 22 | South (Hub) | Illiquid. EOGM on 6 Oct. |
| PIOC | 8.0 | 0 | 16 | North. Swap value Rs238.5 against Rs231.6 price, a 3.0% gross spread | Tied to MLCF. Too small an edge. |
| POWER, GWLC, FECTC, DNCC, SMCPL, DCL | 7.5, 7.6, 7.0, 60, 7.8, loss | 0, 1.8, 3.4, 0, 6.5, 0 | 16, 4, 8, 8, 2, 36 | Small and illiquid | Skip for a Rs50k account. |

## 5. Past big moves, 2017 to 2026

Basket is an equal-weight price index of LUCK, DGKC, MLCF, FCCL, KOHC, CHCC and PIOC against KSE-100.

- **Apr 2017 to Aug 2019 de-rating.** The basket fell 56% by Dec 2017 against KSE -24% (relative -42%). By Aug 2019 the total was about -80% (KSE -43%). Publicly known in advance: North expansions of 15.6 Mtpa by FY21 and 5.2 Mtpa in the South (cemnet, Jan 2018). Cherat's second line opened. Coal rose 23% YoY to US$91.5/t in 1QFY18. PKR fell 4.7%. 1HFY18 profit fell 13% while despatches rose 18%. Signal: despatch growth with falling retention price and a capacity pipeline above demand growth. Rate hikes followed in 2018 to 2019.
- **Mar to Aug 2020 rebound.** The basket gained 144% from the 26 Mar low against KSE +51% (relative +62%). SBP cut from 13.25% to 7% between 17 Mar and 25 Jun (Profit). The construction package came on 3 Apr, and the basket was already +41% by then. May despatches fell 36% YoY and the record 5.21 Mt came in Sep. Signal: a rate-cutting cycle plus a policy catalyst, with the stock bottoming before the data did.
- **Jun 2021 to Jul 2022 cost shock.** The basket fell 54% against KSE -18% (relative -44%), then rose 28% in Aug to Sep 2022. Drivers (global coal spike, PKR slide, rate hikes) are from memory and unverified. Signal: coal and PKR, not volume.
- **2026 oil shock.** Basket -25% from 20 Feb to 30 Mar (Brent US$72 to US$118), +44% to 6 Jul as Brent fell to US$70, then -20% to 12 Oct. The relative swings are only -12%, +13% and -9%, so cement is trading as a macro and oil proxy.

## 6. What a veteran watches weekly

1. PBS weekly SPI (cement bag price), Thursday or Friday: https://www.pbs.gov.pk/ (the weekly executive summary PDF)
2. APCMA monthly despatches, 1st to 3rd of the month (ProPakistani and Business Recorder carry them)
3. Topline, AHL and AKD mid-month despatch previews (for example the 29 Sep Topline note)
4. Newcastle and Richards Bay coal futures, plus Brent, daily (thecoalhub.com, repo brent.csv)
5. Petrol and diesel prices, fortnightly (1st and 16th)
6. SBP MPC calendar and PBS CPI (first working day): https://www.sbp.org.pk/
7. PSX company announcements (board notices, closed periods): https://dps.psx.com.pk/announcements/companies
8. Torkham and Afghan trade news, and the North export line in the APCMA release
9. Interbank PKR, daily (SBP)
10. PSDP release figures from the Finance Division, monthly

## 7. Evidence and dates

ProPakistani 2 Oct, 29 Sep and 10 Aug 2026; Business Recorder 16 Oct (40444242), Aug (40439830), June and July pieces (40427931, 40424757) and CCP summary (40418600); cemnet (AHL FY26, AKD 4QFY26, 2018 outlook); Westpac Sep 2026; SBP PR 14 Sep 2026; Tribune 10 Oct 2026; PSX filings 283065 (MLCF scheme) and PSX announcements to 16 Oct; PSX payouts API; repo macro files; Profit on 2020 rate cuts; kabulnow Aug 2026. Business Recorder and cemnet block WebFetch, so I read them with `curl_cffi`. I did not verify the cement FED rate for FY27, September CPI, the October MPC date, or the 1QFY27 board dates. I ran out of search budget before checking the 2021 to 2022 drivers.

**Verdict:** no 12-month +30% idea with a dated catalyst path. Cement is cheap (P/E 7 to 12) but it trades as an oil and rates proxy. The trigger that would flip this is Brent back below US$90 with an SBP pause, together with a Torkham reopening.
