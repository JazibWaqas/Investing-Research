# Playbook: priced deals on PSX (takeovers, delistings, buybacks)

Written 2026-10-17. Sources:
- PSX announcements: the repo archive to Oct 2025, plus Nov 2025 to Aug 2026 fetched this session with `scripts/fetch_announcements.py` into the scratchpad. Documents are cited by PSX doc id (dps.psx.com.pk/download/document/ID.pdf).
- PSX daily closes via `scripts/psx_api.py`, and the press as cited.

Every price is the 16 Oct 2026 PSX close unless stated otherwise. Costs are 0.5% round trip.

**Bottom line.** Only one pending, priced deal is KMI-eligible: **EPCL**. Its headline spread is 21.5% (Rs31.77 against Rs38.60), but only about 53% of a minority holding is likely to be bought at the offer price. With 70% completion odds, the expected return is about +3% net over about four months (9% annualised), rising to about 18% annualised if acceptance reaches 70%. Every other live situation is either unpriced (SBL, AMBL, BML, NICL, MFL), not KMI, already trading at the exit price (SCL, GLPL), or suspended (ASC).

The base rate (n = 11, 2021 to 2026) is sobering:
- the median spread on the day before the public offer was 14.7%
- the median time from intention to payment was 302 days
- the median price one month after completion was 13% *below* the offer price.

## 1. How PSX takeovers price (observed)

- **Offer price rule.** Under the Takeover Regulations 2017, the public-offer price is the highest of four figures: the negotiated SPA price, the highest price the acquirer paid in the look-back period, the VWAP before the PAO, and the 28-day VWAP before the PAI. This is quoted in the PIOC offer (doc 267426, Dec 2025).
- **The offer can beat the SPA price.** That has happened often: Shell Rs118 SPA vs Rs155.11 offer; Tri-Pack 154.62 vs 245.20; Sanofi 940 vs 1,704; Mitchells 180 vs 232.75.
- **Offer size.** At least half of the shares outside the buyer group: PIOC's 11.72% was half of 23.44% (doc 267426). Oversubscription means pro rata acceptance: PIOC took 61.64% of tendered shares (doc 270524).
- **Timeline.** PAO within 180 days of the PAI, extendable by 90 (Reg. 7(1), doc 282317). The 7-day acceptance window opens about 7 to 8 weeks after the PAO, and payment follows in about 3 days (PIOC: PAO 18 Dec 2025, window 8 to 14 Feb, paid 17 Feb).

**Worked example of the trap (PIOC, KMI).** Someone who bought at Rs415.94 on the day before the PAO got 61.64% filled at Rs478.43, and the rest was worth Rs330.22 on payment day. The blended exit was Rs421.6, a gain of **+1.4%**, against a 15% headline spread.

## 2. Pending and recent deals

| Deal (KMI?) | Terms | Timeline | Price 16 Oct | Status |
|---|---|---|---|---|
| **EPCL** ← Noventra (formerly Lotte Chemical Pakistan, LOTCHEM) (KMI) | SPA for 510,733,455 shares (56.19%) from Engro Corp at Rs38.60 (doc 282064). Public offer for 17.5% (ProPakistani, 1 Sep 2026, asserted) = 159.1m shares | PAI 10 Mar 2026 (doc 272329); SPA 31 Aug; PAO deadline extended to 7 Dec 2026 (doc 282317). Payment likely Feb 2027 (inferred from the PIOC timeline) | 31.77 | Approvals pending |
| **NICL** ← CHCC (NICL not KMI; CHCC KMI) | At least 30% (33,177,164 shares); no price disclosed. About Rs8.9bn, roughly Rs268 a share (MarketScreener, unverified) | PAI 10 Sep 2026 (doc 282506). PAO due within 180 days | 265.70 (fell from 270.68 pre-PAI) | Due diligence. No spread at the implied price |
| **MFL**: sale of Matco Corn Products (KMI) | Non-binding IGI Investments offer for 100% of the subsidiary; no price (ProPakistani, 15 Oct 2026) | Board authorised talks 15 Oct | 47.33 (+8.5% on day 1, then gave it back) | Not a minority exit. Catalyst only |
| **SBL** ← Najd Gateway (not KMI) | SPA for 852.0m shares (84.51%) from SNB; price undisclosed (doc 270513). Mandatory offer for about 78.1m shares (Profit, asserted) | PAI 18 Feb 2026; PAO deadline extended 18 Aug (doc 281278) | 13.32 (pre-PAI 14.39) | Awaiting SBP and SECP |
| **AMBL** ← Mobilink MFB (not KMI) | Terms not in readable filings | PAI 10 Mar 2026; extended 7 Sep (doc 282316) | 19.50 (pre-PAI 24.65) | Pending |
| **BML** ← DM Holdings (not KMI) | "Significant shareholding"; terms unread (scanned) | PAI 12 Jun 2026 (doc 278478) | 60.16 | Pending; capital reduction in Jan 2026 |
| **ASC** ← Farrukh/Amin group (KMI) | SPA for 53.50% plus offer for 17.25% (64.69m shares) (doc 279260); price not stated | PAI 30 Jun 2026. **SECP suspended the acquisition by order of 10 Aug 2026** (doc 281148) | 7.95 (pre-PAI 13.42) | Suspended |
| **SCL** delisting (KMI) | Sponsors buy at the PSX-set Rs750 (doc 273979) | EGM 11 May 2026; last trade 24 Jul 2026 | 750.07 (last trade) | Done; no spread |
| **GLPL** delisting (not KMI) | Sponsor buys at the PSX-set Rs700, up from a Rs216.49 proposal (Mettis, pkrevenue) | Delisted 19 May 2026; buyback valid to 10 May 2027 | 700 | Done |
| **ENGROH** market buyback (KMI) | Up to 45m shares (3.73%) at market (doc 275940) | 7 May to 25 Oct 2026; about 36.0m done by 15 Oct (my sum of filings) | 260.65 | Support, not an exit price |
| **CHCC** market buyback (KMI) | Up to 7,771,800 shares (4%) at market (doc 278417) | 12 Jun to 1 Dec 2026; progress filings are scanned | 271.23 | Support |
| **AGP** market buyback (KMI) | Up to 5.6m shares (about 2%) at market (Mettis, asserted) | 22 Apr to 18 Oct 2026; daily filings to 16 Oct | 168.38 | Support; ends 18 Oct |
| **PIA** (PIAHCLA not KMI) | AHCL-led consortium (FFC 33.99% of SPV) paid Rs135bn for 75%; 25% call option (Rs45bn) exercised (doc 281738) | Closed 29 Jun 2026; Lucky consortium lost at Rs134bn (Aaj) | 22.45 | No minority offer |
| **GEPCO / FESCO / IESCO** | 51-100%; Lucky/Hub/Kohat/Metro among 9 prequalified for GEPCO (Tribune, 6 Oct) | FESCO Jan, GEPCO Feb, IESCO Mar 2027 (asserted) | – | Unlisted; risk to LUCK, HUBC, KOHC |
| **PRL** rights | **None found** in 2026 filings; upgrade agreement signed 24 Sep (doc 283398) | – | 106.95 | Future dilution risk (inference) |
| **Noventra** funding (KMI) | Authorised capital doubled to Rs40bn (22 Sep); Rs2.2bn cash vs about Rs26bn needed | EGMs 22 Jun, 22 Sep (not read) | 25.41 | Rights issue likely (inference) |

Completed in the last 12 months: PIOC, ACPL, RMPL and TPLI (all in section 5), plus tender buybacks at LPL (100m shares cancelled, doc 267879) and PKGP (doc 277400; price unread).

## 3. EPCL in detail (the only live KMI arbitrage)

**Who can tender.** EPCL has 908.92m shares.
- Engro Corp sells 56.19% to Noventra.
- Mitsubishi agreed to sell its 11.007% (100.05m shares) to Liberty Daharki Power (doc 270336, Feb 2026). Liberty was a member of the PTA Global consortium that bought control of LOTCHEM in 2025 (Profit, asserted), so it is probably acting in concert with Noventra and will not tender (inference).
- That leaves a free float of 32.80% (298.2m shares) chasing an offer for 17.5% (159.1m shares).
- If every free-float holder tenders, acceptance is **53.4%**. If Liberty also tenders, it is 39.9%. It reaches 70% only if about a quarter of the free float does not tender. Retail inertia makes that possible but not something to count on.

**Offer price.** The floor is Rs38.60. The 28-day VWAP before the PAI was Rs35.22 (30 Jan to 11 Mar 2026, my calculation), which is below the SPA price. So Rs38.60 is the likely offer unless EPCL trades above it before the PAO.

**Exit value per share held** (price after completion assumed at Rs31.0, close to the pre-PAI Rs30.18 to 33.20 range; the base-rate median of 13% below the offer would be Rs33.6):

| Acceptance | Blended exit | Gross vs 31.77 | With a post-deal price of 33.6 |
|---|---|---|---|
| 50% | 34.80 | +9.5% | +13.6% |
| 53.4% (all free float tenders) | 35.06 | +10.4% | +14.2% |
| 70% | 36.32 | +14.3% | +16.8% |
| 100% | 38.60 | +21.5% | +21.5% |

**Odds and expected value.**
- If the deal fails, I assume EPCL falls to Rs28.0. That is the 52-week low of 27.30 plus a little: Q3 is likely weak, with results on 20 Oct (`knowledge/sectors/chemicals.md`).
- At the 53.4% acceptance case, the market-implied completion probability is 53%.
- I assign **70%**. Reasons for: the SPA is signed, Noventra's shareholders held two EGMs, the buyer has industrial logic, and in the archive a signed SPA has usually closed (Shell, Sanofi, Tri-Pack, PIOC, ACPL, RMPL, TPLI all completed). Reasons against:
  1. Funding: about Rs26bn needed against Rs2.2bn of cash, so a rights issue or debt is needed while Noventra's Q3 gross profit fell to Rs0.50bn (doc 285750).
  2. CCP and other approvals.
  3. One timeline extension has already happened.
  4. The PVC anti-dumping duty lapses about 23 Nov unless finalised.
- **Expected value at 70%:**
  - 53.4% acceptance: Rs32.94, which is +3.2% net, or about **9% annualised** over 0.35 years.
  - 70% acceptance: Rs33.82, which is +6.0% net, or about 18% annualised.
- At 60% odds the 53.4% case falls to +1.0% net (about 3% annualised), below the roughly 12% T-bill yield.
- **What kills it:** a Noventra funding failure, a failed rights issue, CCP objection, Engro walking away, or Noventra's controlling group changing its mind.
- **Trigger to act:** the PAO itself, due by 7 Dec 2026. It fixes the price and size and removes most approval risk. Buying before the PAO collects about 3 points more spread but takes the funding risk.

## 4. Ranked opportunities (expected annualised return after 0.5% costs)

| Rank | Deal | KMI | Expected exit | Odds | Horizon | Expected annualised | Note |
|---|---|---|---|---|---|---|---|
| 1 | EPCL tender | Yes | 32.9 to 33.8 | 70% | about 4 months | **about 9% (range 3% to 18%)** | Best case needs 70% acceptance |
| 2 | NICL (CHCC bid) | No | about 268 (implied, unverified) | 60% | 6 to 9 months | about 0% | No spread at the implied price |
| 3 | SBL (Najd) | No | unknown | 60% | 3 to 6 months | n/a | SPA price undisclosed; stock fell after the PAI |
| 4 | AMBL, BML | No | unknown | ? | ? | n/a | Terms unread |
| 5 | ASC | Yes | unknown | low | ? | n/a | Suspended by SECP |
| – | SCL, GLPL | Yes / No | 750 / 700 | done | – | 0% | Trade at the exit price |

None beats the 12% T-bill on expected value except EPCL in its 70%-acceptance case. **Do not enter EPCL before the PAO** unless a Noventra funding filing (rights issue or loan) appears first.

## 5. Base rate: 11 completed PSX tender offers, 2021 to 2026

Columns: pre-PAI close (day before the first PAI); spread = offer vs close the day before the PAO; days from PAI to payment; price 21 and 126 trading days after completion vs the offer; "rel" = 6-month return from completion vs the KSE-100. Raw PSX closes; no gap beyond ±11% in any window.

| Target (acquirer) | PAI | Offer (SPA) | Pre-PAI | Premium | Spread before PAO | Acceptance (tendered vs offer size) | Days | 1m vs offer | 6m vs offer | 6m rel |
|---|---|---|---|---|---|---|---|---|---|---|
| TRIPF (Packages) | 17 Feb 2021 | 245.20 (154.62) | 170.19 | +44% | 11.5% | Filled; buyer reached 69.26% | 315 | −23% | −37% | −21% |
| SAPL (Packages consortium) | 27 Dec 2021 | 1,704 (940) | 758.82 | +125% | 98.1% | Filled (6.07% acquired) | 249 | −38% | −56% | −43% |
| BIPL (JSBL) | 15 Nov 2022 | 23.99 | 12.22 | +96% | 45.2% | Not found; buyer reached 75.12% | 281 | −34% | +4% | +14% |
| SHEL (Wafi) | 17 Jul 2023 | 155.11 (118) | 110.50 | +40% | 5.5% | 70% to 100%, all accepted | 449 | −5% | +19% | −5% |
| UNITY (Wilmar group) | 19 Mar 2024 | 27.34 (raised from 24.89) | 24.04 | +14% | 16.6% | Not found | 98 | +14% | +26% | −19% |
| MFFL (CCL) | 13 Nov 2024 | 232.75 (180) | 181.91 | +28% | 11.1% | Filled (doc 260732 title) | 322 | −13% | −31% | −19% |
| LOTCHEM (PTA Global consortium) | 13 Feb 2025 | 22.37 | 21.56 | +4% | 5.7% | **30%** (56.4m of 189.2m) | 207 | +23% | −6% | −7% |
| PIOC (MLCF) | 13 Nov 2025 | 478.43 (USD-linked SPA) | 221.98 | +116% | 15.0% | **162%; pro rata 61.64%** | 96 | −52% | −44% | −22% |
| ACPL (FCCL + KAPCO) | 3 Jun 2025 | 330.41 (same) | 310.54 | +6% | 14.7% | About filled (buyers reached 92.03%) | 321 | −32% | −29% | −1% |
| RMPL (Nishat group) | 14 May 2025 | 9,800 (same) | 8,911 | +10% | 9.2% | **73%**, all accepted (doc 277722) | 373 | −2% | −14% | −12% |
| TPLI (Jazz) | 4 Sep 2025 | 30.00 (same) | 19.51 | +54% | 24.9% | Filled (doc 279482 title) | 302 | +138% | +70% | +69% |

**Summary** (n = 11; 9 have a known acceptance):

| Measure | Median | Range or count |
|---|---|---|
| Premium to pre-PAI price | +40% | 4% to 125% |
| Spread on the day before the PAO | 14.7% | 5.5% to 98% |
| Days from PAI to payment | 302 | 96 to 449 |
| Price 1 month after completion vs offer | −13% | 3 of 11 above the offer |
| Price 6 months after completion vs offer | −14% | |
| 6-month return relative to KSE-100 | −12% | 2 of 11 positive |
| Acceptance | | Offer oversubscribed or filled in 6 of 9; undersubscribed in 3 (LOTCHEM 30%, RMPL 73%, SHEL 70% to 100%) |

Also outside the table: FFC's offer for Agritech (Dec 2024) drew only 7.85m of 151.05m shares (5%), because the price was near the market (Profit, asserted).

**Lessons for the next deal:**
1. **Oversubscription follows the spread.** When the spread is above about 10%, retail tenders and you get pro rata. When the offer sits near the market (LOTCHEM, AGL), few tender. With EPCL's 21.5% spread, expect the free float to tender fully, so about 53% acceptance.
2. **The stub sags after completion.** The unaccepted remainder usually trades below the pre-offer price within 1 to 6 months (median −13% vs offer at 1 month). Value it below the offer, never at it.
3. **Most of the return comes at the PAI, not after.** The median premium to the pre-PAI price was 40%, while the median spread left on the day before the PAO was 14.7%. Capturing it means spotting sale processes early (multinational exits: Shell, Sanofi, Gillette, Rafhan).
4. **Delistings at PSX-set prices** (GLPL Rs700 vs a Rs216 proposal; SCL Rs750) gave large uplifts to holders on the day the price was set. Watch for "voluntary delisting application" notices; that is where minority value appeared in 2026.
5. **Withdrawals are common among competing bidders.** In 2025-26, PAIs for ACPL (AHL, CHCC), RMPL (CHCC, SFL), SGPL and Escorts were withdrawn, and ASC was suspended by SECP. Signed-SPA deals rarely failed in this sample.

## 6. Could not verify

- The EPCL public-offer size and price from a primary filing. The PAI attachment was not retrievable; 17.5% is from ProPakistani.
- The NICL, SBL, AMBL and BML deal prices.
- CHCC and AGP buyback progress.
- Whether Liberty Daharki is acting in concert with Noventra.
- PKGP and LPL buyback prices.
- BIPL and UNITY acceptance figures.
- PRL rights: none found, and the absence is itself unconfirmed for filings that are scanned images.
