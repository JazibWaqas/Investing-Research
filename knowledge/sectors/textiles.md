# Textiles sector note (spinning, weaving, composite)

As of 2026-10-17. Prices, P/E and DY come from `seed/data/fundamentals/screener_20261016.csv` (16 Oct close). Screener P/E is trailing and often standalone. Anything not sourced is marked "unverified". Return figures are price only from PSX daily history (gaps over 10.5% treated as corporate actions), so they are approximate. The WebSearch budget ran out, so I read Business Recorder (BR) pages with `curl_cffi` and PSX filings directly.

## 1. How this sector makes money

1. **Export volume and conversion margin.** Textiles are about 60% of exports. FY26 textile exports were US$17.93bn (+0.26%), and over 80% is value-added (APTMA). Composites (ILP, NML, GATM, KTML, SAPT) earn the margin between cost and a US or EU order price set months ahead. Spinners sell yarn into that chain.
2. **Energy cost.** Grid power for exporters costs about 11 US cents/kWh against about 6 in rival countries (APTMA chairman, 1 Oct). Other energy items are RLNG at US$14 to 15/MMBtu, the 20% off-grid levy on captive gas, monthly fuel adjustments, and winter gas curtailment.
3. **Cotton and polyester against yarn price.** Mills win or lose on the spread, and on inventory gains when cotton rises.
4. **Policy and tax support.** Items are the Export Facilitation Scheme (EFS, duty-free inputs), export finance at 4.5%, DLTL drawback (now being requested), sales tax refunds, provincial cesses, EU GSP+ (expires 2027) and the US tariff (19%).
5. **Financing cost, PKR and freight.** Policy rate is 11.5%. A stronger rupee cuts PKR margins. Ocean freight is 1.5 to 2.5 times normal.
6. **Other income.** NML (associates) and SFL (investments) report more from investments than from spinning.

## 2. Where each lever stands today

| Lever | Latest datapoint | Date | Source |
|---|---|---|---|
| Exports | 1QFY27 US$5.026bn, +5.26% YoY. Yarn +24%, garments +16%, cloth -5%. PTEA warns of a "steep" 2QFY27 decline | 12 to 16 Oct | https://www.brecorder.com/news/40444478 ; https://www.brecorder.com/news/40443744 |
| Power tariff | Exporters want 9 US cents. DISCOs seek +5 to 10% and fixed charges up from 8% to about 20%. B3/B4 cross-subsidy Rs56bn alleged, Rs26bn acknowledged by PPMC. Power Division meeting 16 Oct, outcome not found | 13 to 15 Oct | https://www.brecorder.com/news/40444115 ; https://www.brecorder.com/news/40444301 |
| Gas | SNGPL RLNG US$15.20/MMBtu (September, cut about 20%). Winter plan Nov to Feb may curtail industry and captive. QatarEnergy force majeure since March | 25 Sep, 13 Oct | https://www.brecorder.com/news/40441163 ; https://www.brecorder.com/news/40443943 |
| Cotton | KCA spot Rs18,300/maund. Arrivals 3.208m bales. Kharif estimate 6.7m bales against a 9.64m target. Pest damage reported. World price US$2.10/kg in September, up from US$1.63 in February | 15 Oct, 8 Oct | https://www.brecorder.com/news/40444449 ; https://www.brecorder.com/news/40443215 ; repo `data/macro/cotton.csv` |
| Policy support | EFS window 18 months, export finance 4.5% until Jun 2027 but banks charge 5.5 to 8.5%. Exporters ask 6 to 8% DLTL tied to +10% exports. Punjab 0.9% import cess challenged. FBR can seal spinning units off its monitoring system | Mar to Oct | https://www.brecorder.com/news/40412398 ; https://www.brecorder.com/news/40443616 ; https://www.brecorder.com/news/40442278 |
| Trade access | EU GSP+ renewal talks opened (expires 2027). US tariff 19% (Aug 2025). Current US rate unverified | 19 Sep | https://www.brecorder.com/news/40440240 |
| Rates and PKR | Policy rate 11.5%, held 14 Sep. PKR about 268, but the Yahoo series flips to 277 on some days, so treat as unreliable | Sep to Oct | repo `data/macro/policy_rate_decisions.csv`, `usdpkr.csv` |
| Freight and demand | Freight up 1.5 to 2.5 times. Weak Western demand. Faisalabad weaving units cutting shifts | 8 to 12 Oct | https://www.brecorder.com/news/40443204 ; https://www.brecorder.com/news/40443714 |

## 3. What changes in the next 1 to 3 months

- **20 Oct:** NML final dividend Rs2, book closure 21 to 28 Oct, AGM 28 Oct (PSX 283949).
- **22 Oct:** ILP 1QFY27 board (PSX 285686). **24 Oct:** GATM board (PSX 285796). **27 Oct:** NCL board (not in KMI).
- **By about 30 Oct:** other 1Q results. Last year KTML reported 20 Oct, KOHTM, SAPT and NCL 29 Oct, and NML, SFL, FML and FZCM 30 Oct. This year's dates are unannounced.
- **26 Oct:** SBP MPC (date from another note, unverified). Hike risk exists with Brent above US$120.
- **29 Oct:** NEPRA hearing on DISCO tariffs (Tribune).
- **Early to mid Nov:** a Prime Minister decision on the B3/B4 anomaly and DLTL is possible but unscheduled. Also the CCoE vote on the winter gas plan, OGRA's monthly RLNG price, and PBS October exports (September data came 15 Oct, August data 19 Sep).
- **Mid Dec:** SBP MPC (date unverified). Final dividends fall in Oct to Nov, interims in Feb to Mar.

## 4. Exposed KMI names

Not in KMI: NCL, SFL, KOSM (screener `listed_in`). BWHL is an auto-parts company, not textiles. Liquidity is price times 30-day average volume, in Rs m per day. FY26 EPS is from PSX filings (SFL, NML) or stockanalysis.com (others).

| Symbol | P/E | DY % | Liq | Levers and view |
|---|---|---|---|---|
| NML | 8.1 (standalone EPS 15.59). Consolidated EPS 41.08 gives 3.1 | 1.3 | 114 | Energy, export price, associates. Consolidated profit is flattered by Rs7.5bn from associates, and standalone operating profit fell. Standalone equity Rs156bn against a Rs44bn market cap. Cheap but a chronic discount. |
| ILP | 10.1 | 3.7 | 53 | Knitwear and hosiery exports, quality. EPS Rs9.06 against 3.96. Dividend Rs4. Price 94 against a 68 to 110 range. |
| TOWL | 14.0 | 0 | 29 | Towels, energy-exposed, expensive. |
| ASTM | 82 | 0 | 29 | Spinner up 175% in a year. PSX flagged unusual price movement on 25 Sep. Operator-type risk. |
| KOHTM, ARCTM, DFSM, TATM | 7.4, 11.8, loss, 2.3 | 0.9, 0, 0, 3.6 | 17, 17, 15, 14 | Small spinners, up 2% to 153% in a year. TATM is the cheap one. |
| GATM | loss (EPS -0.46) | 0 | 12 | Retail plus composite, down 45%. Needs margin repair. |
| KTML | 10.9. Stockanalysis shows 2.7 (EPS 14.77) | 0 | 10 | The two EPS figures disagree. Verify against the PSX filing before use. |
| MEHT | 5.1 | 0 | 8 | Down 57% in a year. Thin. |
| SAPT, FML, FZCM, CRTM | 4.9, 22.7, 5.7, 106 | 1.3, 0, 5.8, 0 | 0.2, 0.5, 2.5, 0.2 | Illiquid. Skip for a Rs50k account. |

## 5. Past big moves, 2017 to 2026

Basket is an equal-weight price index of 16 names against KSE-100. It is small-cap heavy, so medians are lower than the headlines.

- **Jun 2023 to Apr 2025: relative -53%** (basket +28%, KSE +174%). The ratio hit its low of 0.55 on 7 Apr 2025. Public before: the policy rate began falling in Jun 2024 and money went to banks and energy, while textile policy turned worse. BR (21 Jan 2025) documents the loss of zero-rating for local inputs under EFS. The FY25 budget tax change and the captive gas levy are from memory and unverified. Signal: a falling relative-strength line while exports rose, plus tax and levy announcements.
- **May to Jul 2025: relative +54%** (basket +76%, KSE +14%, led by small spinners such as KOHTM +200%). Public before: SBP cut to 11% on 5 May. The US tariff shock, pause and later 19% deal are from memory except the BR 4 Aug piece, where exporters said Pakistan was below Bangladesh and India. Signal: a record-low ratio, a rate cut and a relative tariff advantage.
- **May 2020 to Aug 2021: relative +52%** (basket +113%, KSE +40%). Public before: SBP cut from 13.25% to 7% between 17 Mar and 25 Jun 2020 (repo file). The stocks bottomed before export data turned (export numbers are from memory). Signal: a rate-cut cycle.
- **Sep 2017 to Nov 2019: relative -35%** (basket -40%, KSE -8%; SFL -59%, KTML -62%). Public before: the rate rose from 10.25% to 13.25% in 2019. Drivers beyond that are unverified.
- **Mar to Jun 2026: relative +31%** (basket +49%, KSE +14%) from a record-low ratio on 3 Mar. On 19 Mar the government extended the EFS window to 18 months and export finance fell to 4.5% (BR). Since 29 Jun the basket is -13% (KSE -7%) as energy cost, freight and the oil shock hit.

## 6. What a veteran watches weekly

1. PBS monthly exports, mid-month: https://www.pbs.gov.pk/
2. KCA spot rate and the weekly cotton review, daily and Monday: https://www.brecorder.com/trends/cotton
3. ICE cotton futures, daily
4. NEPRA fuel adjustments and tariff hearings, monthly: https://nepra.org.pk/
5. OGRA RLNG prices, monthly: https://www.ogra.org.pk/
6. APTMA and PTEA statements and Commerce Ministry meetings: https://www.brecorder.com/trends/aptma
7. SBP MPC dates and export-finance circulars: https://www.sbp.org.pk/
8. PSX announcements for board dates and results: https://dps.psx.com.pk/announcements/companies
9. PCGA cotton arrivals, fortnightly
10. Freight rates and the interbank PKR, weekly

## 7. Evidence and dates

BR articles 40444478, 40444115, 40444301, 40444470, 40443744, 40443616, 40443204, 40443714, 40443943, 40443215, 40442656, 40442278, 40442310, 40442089, 40441163, 40440240, 40440237, 40440581, 40444449, 40444486, 40436246, 40428467, 40412398, 40376113, 40343734 (Jul 2025 to Oct 2026); Tribune 17 Oct 2026; PSX filings 283949, 285686, 285796, 285736, 283405 (SFL), 282492 (ILP), 283782 (CRTM) and the PSX announcement archive; stockanalysis.com financial pages (ILP, NML, NCL, KTML, GATM, SAPT, FML, 16 Oct); repo macro files and PSX price history. Not found: Power Division outcome on 16 Oct, current US tariff rate, MPC dates, TOWL board date, KTML FY26 filing, a mill-level yarn spread series, 2017 to 2019 and 2024 policy details (memory only).

**Verdict:** the sector is cheap on a relative basis (ratio 0.68 against 1.18 in 2023) but the near-term path is down on energy, freight and 2QFY27 export warnings. Upside needs a DLTL or tariff decision, which is unscheduled and IMF-constrained. No high-conviction 12-month +30% idea. NML is a low-odds asset-discount case only.

## Gap resolution (17 Oct 2026, Codex)

- [SBP's published MPC calendar](https://www.sbp.org.pk/m_policy/mp-comm-semi.asp) confirms 26 October and 14 December 2026, resolving the two dates marked unverified in section 3.
- [TOWL's PSX page](https://dps.psx.com.pk/company/TOWL), checked 17 October, shows its FY26 result on 28 September and AGM notice on 1 October but no 1QFY27 board notice. Its next result date remains unverified. [PSX's 13 October notice list](https://dps.psx.com.pk/announcements?type=cdc) gives Hira Textile a company-specific non-compliance deadline of 28 October, a concrete governance flag rather than a generic textile-sector concern.
