# Actors and incentives on PSX: who decides, what they want, and whether an announced thing will happen

Written 18 Oct 2026. Evidence: repo files (`data/macro/policy_rate_decisions.csv`, `data/macro/cpi.csv`, MPS texts in `data/raw/macro/mps`, `data/deals_history.csv`, `knowledge/sectors/`, `knowledge/playbooks/deals.md` and `holdco_discounts.md`) plus web searches run 18 Oct 2026. Most web pages were read as search summaries, not full text, so sourced dates are as reported by Profit, ProPakistani, Dawn, Tribune, Business Recorder and PSX filings. "Unverified" means I could not confirm it. The outcome coding in section 2 is my judgment on a small, non-random list.

## 1. The actors

**The decision chain.** The Cabinet Committee on Energy (chaired by the PM) approved the revamped refinery policy on 28 Jul 2026 (Dawn 2019159) and received the gas-debt plan on 19 Aug 2026 (ProPakistani). The ECC approves prices and margins. The Petroleum Division signs and monitors; OGRA notifies gas, fuel and FRR numbers; NEPRA sets tariffs. Approval is not implementation. The OMC margin rise of Rs1.22 a litre is ECC-approved but still un-notified (OCAC letter, Business Recorder 25 Aug 2026; nothing later found). The step that matters is the notification, which needs the Finance Division and, if there is a fiscal cost, the IMF.

**Finance ministry and IMF.** The ministry wants the primary surplus, clean reviews and market access (a Eurobond was issued before Apr 2026 per the MPS). The IMF enforces numbers and cost recovery: the captive-gas levy was a structural benchmark and the IMF refused to revise it (Profit, 28 Mar 2025); fertilizer subsidies were refused in 2023 (Tribune). It lets slide dates and stocks. DISCO sales promised for Jan 2025 (Profit, 12 Oct 2024) had reached only expressions of interest by May 2026. FBR missed the IMF FY26 target by Rs975bn (Tribune, 1 Jul 2026) and the gap was covered by a higher petroleum levy and development cuts. Board dates follow financing assurances: staff agreement 12 Jul 2024, Board 25 Sep 2024 (75 days). Circular debt sat at Rs1.835tn, above the ceiling (`sector_map.md`). The IMF queried the FY27 super-tax cut, which passed with banks, E&P and fertilizer excluded (Nukta, Daily Pakistan, Jun 2026).

**SBP reaction function** (computed here from the 84 decisions of Jan 2015 to Sep 2026: 45 holds, 21 hikes, 18 cuts; real rate = policy rate before the meeting minus prior-month CPI). Hikes came at a median real rate of -1.1% (range -17.0 to +3.9). Waves: 2018-19, 750bp to 13.25%, with MPS reasons the rupee, current account and reserves, running into the IMF programme (Jul 2019 MPS cites depreciation); Sep 2021 to Jul 2022, 7% to 15%; Nov 2022 to Jun 2023, 15% to 22%, real -8 to -17 as SBP chased inflation. Cuts came at a median real +5.2. Excluding the five Covid cuts of 2020 (real about zero; growth and oil shock), every cut came with real above +4.7: the 2024-25 cycle started in Jun 2024 at real +10.3 and ended with the 50bp cut of 15 Dec 2025 at +4.8. It reacts to shocks within two weeks to two months. The 12 Jun 2023 MPS said "barring unexpected shocks", then it hiked 100bp on 26 Jun after budget taxes and withdrawal of import guidance. The 8 Mar 2022 MPS said it was "prepared to meet earlier"; it hiked 250bp on 7 Apr. After the Middle East war began it held on 9 Mar 2026, then hiked 100bp on 27 Apr (CPI 7.3%, real +3.2). On 14 Sep 2026 it held, 7 votes of 10, with CPI near 11.1% (real about +0.3), because core was lower than expected and the external account was calm. So it tolerates near-zero real rates under a supply shock while the external account is quiet. The 26 Oct meeting tests that.

**Establishment and SIFC.** The SIFC (created mid-2023, army chief a member, agriculture, mining and IT focus, IMF asked about its powers) was described by a government adviser to mining.com (date not shown). Reuters in 2020 reported the military as the most influential voice on Reko Diq. Establishment-linked capital is visible in listed names: Fauji Foundation owns 44.32% of FFC (FFC H1-26 report), FFC holds 33.99% of the PIA buyer (repo), a Fauji Foundation and KAPCO group bought Attock Cement (completed 20 Apr 2026, `deals_history.csv`), and Fauji Foundation held 8.5% of HUBC (2021 deck). Where this capital is the buyer, the deal closes. I found no source naming the sectors it favours beyond these deals.

**Courts and regulators.** Of the 26 policy cases in section 2, three were materially held up by courts: GIDC (2020), the captive levy (IHC suspended it 28 Mar 2025 and recalled the stay 11 Apr; SHC ruled retroactive bills unlawful in Jan 2026), and NEPRA’s cut to K-Electric (Appellate Tribunal 23 Sep, notified 27 Sep, SHC stay 7 Oct 2026). Interim stays arrive within days and rarely kill a fiscal levy; they cut retrospective claims. In deals: SECP and the SHC unwound the TRG offer; SECP suspended the ASC acquisition on 10 Aug 2026 (`deals.md`). PSX itself protects minorities: Philip Morris Pakistan’s delisting price went from the sponsor’s Rs664 to Rs1,300 after the PSX committee (Profit, 27 Jun 2025).

**Sponsor groups.** Evidence per group is two to five dated items. Alignment is what sources show, not rumour.

| Group | Listed holdings | Minority record (sourced) | Alignment |
|---|---|---|---|
| Fauji | FFC (Foundation 44.32%), Askari Bank 64.72%, Fauji Foods ~82-85%, AGL 37.36%, FCCL; 8.5% of HUBC | FFBL merged into FFC at 4.29:1 (court-approved 4 Dec 2024) against 3.92 estimated earlier, so FFBL holders got about 9% fewer shares than that estimate (Profit). Fauji Foods: Rs7.8bn rights issue 2021, then a Rs11.7bn issue to related entities (FFBL Power, FFC Energy, the Foundation) in 2022. FFC pays Rs41 a share (76% payout) but has Rs61bn going into PIA | Military foundation; in the PIA consortium |
| Nishat (Mansha) | MCB, NML, DGKC, Adamjee, NCL, NPL/NCPL (cross-holdings unverified) | Won Rafhan control at Rs9,800 a share (51%), about market (Rs9,915 the day before), reaching 73.9% via a public offer; beat Cherat and Sapphire. No rights-issue record found | MCB bought in Sharif’s first term; Mansha: "never met Nawaz Sharif" (Euromoney). Unproven |
| Lucky (Tabba) | LUCK, LCI 55%; Lucky Electric, Lucky Motor (unlisted) | No rights issues found; Rs77.6bn net cash against one Rs5 annual dividend; Rs319bn capex in ten years (Profit). Bid Rs134bn for PIA (lost by Rs1bn) and GEPCO with Hub, Kohat, Metro. LOTCHEM chase withdrawn Jan 2024 | Bids on state assets; no alignment shown |
| Engro/Dawood | ENGROH (ex-Dawood Hercules), EFERT 56.27%, EPCL 56.19% (being sold) | Swap at 2.2441 preserved economics (done Jan 2025); 36m-share buyback by 15 Oct at Rs263-282. EPQL sale: PAI 26 Feb 2024, withdrawn twice. EPCL control sold at Rs38.60 with an offer for 17.5%, so minorities fill about 50% | None shown |
| Attock/Pharaon | ATRL (Attock Oil 61.06%), APL, POL, NRL 25% | ATRL pays from Rs116bn cash; Attock Cement control sold to Fauji/KAPCO in 10 months; offer to sell Attock Hospital to its chairman (Jun 2026, immaterial) | None shown |
| Arif Habib | AHCL, AHL, FATIMA, ASL (sponsors 66%) | ASL: Rs6.9bn equity and open-market buys at Rs9.78, 12.27, 13.6 in 2026 (`catalyst_trade.md`). Led the PIA win with Fatima (Rs135bn, 23 Dec 2025). Dual role: adviser on the OGDC/PPL sales in 2020, MFL sell-side 2026 | Government-facing; no ties stated |
| JS (Siddiqui) | JSCL (not KMI), JS Bank 71.21%, BIPL 53.5% look-through | BIPL bid first offered minorities JS Bank paper, then cash after pushback (Profit, Apr 2023). JSCL trades 41.6% below NAV. Bids for Next Capital, BIPLS, Calcorp all withdrawn | None shown |
| Hub Power | HUBC: Mega Conglomerate 19.5%, Fauji 8.5%, ABL 4.4% (2021); CPHGC 47.5%, ThalNova 38.3% | Dividend Rs20 against Rs15; investee dividend income Rs29.3bn, above the payout (ProPakistani, 28 Sep 2026). In 2024 the state ended its 1,292MW PPA for Rs36.5bn | Chinese partners; Fauji holder |
| Habib, Lakson, PARCO, Chinese IPPs | INDU/Thal/Agriauto (Habib); PARCO unlisted (60% state, 40% Abu Dhabi); CPEC IPPs unlisted | Too little sourced evidence for Habib or Lakson. PARCO upgrade signing due before 24 Oct. Chinese lenders refused to waive Rs170bn of late-payment charges on Rs423bn dues (ProPakistani, 12 Jul 2026) | Chinese creditors resist the IMF line |

Best minority records, low confidence: Hub, Arif Habib (ASL), Engro. Worst: JS, Fauji (insider-subscribed issues, a less favourable ratio, cash steered to state projects), and Lucky on capital allocation to state sales, the weakest of the three.

## 2. Implementation base rate, 2018 to 2026

Y implemented as announced; P partial, diluted or reversed; N not done or pending. Lag is announcement to first effective step, in months.

| # | Policy | Announced | Outcome | Lag | Pushed / blocked |
|---|---|---|---|---|---|
| 1 | Brownfield refinery policy | 17 Aug 2023 | CCoE 28 Jul 2026; 4 of 5 signed 24 Sep; zero deemed duty unnotified. Y | 37 | PM / refiners, Finance |
| 2 | HSD crack cap | Aug 2026 | In force 20 Aug 2026. Y | 0 | PM, pump-price politics |
| 3 | OMC margin +Rs1.22 | OCAC ask Apr 2025 | ECC-approved, not notified. N | >10 | OMCs / Finance |
| 4 | Dealer margin Rs9.98 | Aug 2026 | In force 1 Sep 2026. Y | 0.5 | ECC |
| 5 | Gas debt plan Rs1.49tr | 19 Aug 2026 | No IMF approval found. N | pending | Petroleum Div. / IMF |
| 6 | Rs1.225tn power bank facility | 2025 | Signed 25 Sep 2025; debt then rose Rs223bn. P | n/a | Power Div., IMF |
| 7 | IPP terminations | 2024 (unverified) | 5 PPAs ended Oct 2024; Rs1tn savings claimed 29 Dec. Y | ~6 | PM, IMF / Chinese IPPs |
| 8 | PIA sale | Auction 31 Oct 2024 failed | Sold 23 Dec 2025, closed 29 Jun 2026. Y | 20 | IMF, PM, Arif Habib, FFC |
| 9 | DISCO sales | Oct 2024: two by Jan 2025 | EOIs 19 May 2026; none sold. N | 21+ | IMF / tariff doubts |
| 10 | K-Electric to Shanghai Electric | PAI 27 Mar 2018 | Withdrawn Apr 2024, ended 9 Sep 2025. N | never | approvals unmet |
| 11 | OGDC 7%, PPL 10% sale | CCoP 21 Aug 2020 | On hold May 2021; no sale found. N | never | ministry / weak prices |
| 12 | Six SOEs sold in FY20 | 29 Jan 2020 | None found completed (unverified). N | never | Privatisation minister |
| 13 | Super tax cut | Budget 12 Jun 2026 | Finance Act 27 Jun 2026. Y | 0.5 | Finance / IMF queried |
| 14 | Cement FED | Jun 2024 | Effective Jul 2024; no reversal. Y | 0.5 | Finance, IMF |
| 15 | Rs170bn mini-budget | 10 Feb 2023 | Passed that month. Y | 0.5 | IMF |
| 16 | Captive gas levy | Ordinance Jan 2025 | Levied from Feb 2025; stayed, eroded. P | 1.5 | IMF / IHC, SHC |
| 17 | GIDC recovery | SC Aug 2020 | Rs449bn due Dec 2022; Senate deferred 5 Sep 2026. P | 72 | SC / stays |
| 18 | End subsidised RLNG to fertilizer | 2023 | Mari gas swap, ECC Nov 2025. P | 28 | IMF / Finance Div. objected |
| 19 | Exporter power tariff Rs19.99 | 6 Oct 2022 | Dropped 2023 on IMF demand. P | n/a | PM / IMF |
| 20 | Panda bond | "this year" 2024 | Postponed 4th time 11 Feb 2026. N | >12 | Finance / multilaterals |
| 21 | Auto policy 2026-31 | Old one expired 30 Jun 2026 | PM office: not approved. N | pending | assemblers, IMF |
| 22 | Net-metering reform | Draft Dec 2025 | Notified 9 Feb 2026; partly reversed. Y | 2 | NEPRA, IMF |
| 23 | IMF EFF Board | Staff deal 12 Jul 2024 | 25 Sep 2024. Y | 2.5 | financing assurances |
| 24 | Windfall recovery Rs72bn | 26 May 2026 | No enactment found. N | pending | Finance |
| 25 | Hybrid tax concession sunset | Scheduled | Ended 30 Jun 2026. Y | 0 | Finance |
| 26 | NEPRA cut to KE tariff | Notified 27 Sep 2026 | SHC stay 7 Oct. N | stalled | NEPRA / KE |

**Results.** Implemented as announced: 11 of 26 (42%); with partials, 16 (62%); not done or pending, 10. The median lag of the 11 is 0.5 months (range 0 to 37); only PIA (20) and the refinery policy (37) took over six months. Sponsorship split the list. Where the Finance Division or IMF sponsored a measure that raises revenue or cuts cost (n=12: items 6-9, 13-16, 18, 22, 23, 25), 8 were fully implemented and 11 at least partly (67%, 92%). Where only a line ministry, industry body or the PM backed it without an IMF number (n=14), 3 were implemented and 5 at least partly (21%, 36%); the three are the pump-price items (2, 4) and the refinery policy. Nine of those 14 never happened or are pending. The backing that matters most is the IMF/Finance Division, the PM through the CCoE and ECC (fast on pump-price politics, slow on paying industry), and establishment-linked buyers for asset sales. Private deals are separate: 27 of 56 resolved takeover announcements completed (48%); once a public offer is made about 90% do (`deals.md`). Caveat: n is small and the list was assembled from what surfaced, so contested items are over-represented.

## 3. Reading the game

**A minister promises a privatisation.** On 29 Jan 2020 the privatisation minister listed six entities for sale that fiscal year (Profit); I found no completed sale. DISCOs promised for Jan 2025 reached expressions of interest in May 2026. PIA was promised for November 2025 (Senate committee, 30 Oct 2025) and sold 23 Dec; a new owner "by April" closed 29 Jun. Deadlines slip 1 to 17 months. A sale closes when a named buyer with money and state-friendly standing is already at the table, and fails when the market must pay (OGDC/PPL, which are now asked for Rs540bn of extra dividends instead; ProPakistani, 19 Aug 2026).

**SBP guidance.** Conditional language ("barring shocks", "prepared to act") was followed by action within 2 to 7 weeks three times (Jun 2023, Mar-Apr 2022, Mar-Apr 2026). "Outlook broadly unchanged" with real above +4.7 preceded a cut (Dec 2025). Read the real rate and the external account, not the adjectives.

**IMF staff remarks.** Staff numbers are credible, staff dates are not: the Board followed staff agreement by 75 days in 2024, and the calendar cites past gaps of 12 to 75 days. The current agreement is dated 8 Oct 2026, Board unscheduled. The IMF flagged a Rs1tn FY26 tax gap in May 2025 (Profit); the miss was Rs975bn and was tolerated through levies. It delayed the petroleum debt plan on 24 May 2025 and PSO was dropped from it. The repo’s earlier test found staff-agreement timing weak for prices.

**A sponsor announces expansion.** Self-funded capex gets built: Lucky’s Karachi expansion to 15.6 Mtpa was filed 1 Jul 2026 and the group reports Rs319bn invested in ten years. Diversification into state-directed or loss-making assets costs minorities: FFC’s PIA Rs30.6bn paid plus Rs30.6bn due. An expansion alongside an authorised-capital increase means a rights issue: Noventra doubled authorised capital to Rs40bn on 22 Sep with Rs2.2bn cash against Rs25.8bn needed (`deals.md`), and PRL’s upgrade carries rights risk (Topline assumes 80%).

**"No plan to raise prices or taxes."** I found no dated denial followed by a reversal, so the base rate is unmeasured. Dated facts only: Rs170bn of taxes announced 10 Feb 2023; a November 2024 denial of mini-budget rumours after an IMF visit (Aaj), with no mini-budget found since (unverified); a pledge of contingency tax measures from Jan 2026 if revenue lagged (Tribune) with no verified outcome.
