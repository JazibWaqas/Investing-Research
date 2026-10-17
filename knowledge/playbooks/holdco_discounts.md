# Playbook: holding-company discounts on PSX

Written 2026-10-17. Prices are PSX closes for 16 Oct 2026, taken from the PSX `/historical` endpoint, which matches `data/prices_raw`. The screener differs by up to about 1% on a few names. Share counts come from the PSX company pages, fetched 17 Oct. Year-end market caps for 2021 to 2025 come from stockanalysis.com/quote/psx/SYM/market-cap/. Stake data comes from company filings where I could read them (cited) and from rating reports or press otherwise (marked "asserted"). Work files are in the session scratchpad and are not committed.

**Bottom line.** Measured against market prices and stated peer multiples, most large KMI holding companies trade near their sum of the parts. The one wide, clearly measured discount is JSCL, at about 42% to NAV, and it is not KMI. ENGROH's discount depends on how you value its unlisted assets: about 9% on market multiples, about 48% on Topline's DCF. ATRL and OGDC look about 20% cheap, but that comes from peer multiples (a sector call), not from the value of their listed stakes. Lesson 17 applies: a low multiple inside a holdco is usually a sector discount.

## 1. Method

- **Listed stakes** are valued at the 16 Oct close times the shares held. EPCL is valued at the Rs38.60 deal price, because Engro has signed to sell it.
- **Holdco net cash** comes from the company's own (unconsolidated) balance sheet: cash and short-term investments minus all borrowings.
- **The stub** is the price minus listed stakes minus net cash. It is everything else: the operating business plus unlisted subsidiaries.
- **The stub P/E** is the stub divided by the holdco's own earnings once the listed subsidiaries' and the cash's earnings are removed.
- **NAV** adds the listed stakes, the net cash, and the stub earnings times a stated reference multiple. Discount = 1 − price/NAV. The reference multiples are trailing P/Es from the 16 Oct screener: cement median 7.26x (DGKC, FCCL, KOHC, CHCC, MLCF), HUBC consolidated 5.05x for power, E&P 6.0x (PPL 6.04, POL 5.96), refining median 6.57x (NRL, PRL, CNERGY), fertilizer 11.5x (EFERT 12.6, FATIMA 10.4). Changing the multiple changes the answer, so each row shows its multiple.
- **History** measures listed-stake coverage, which is listed-stake value divided by the holdco's market cap at each year end. It uses current stake percentages unless a change is noted. I could not rebuild stub earnings for every past year, so the history covers the listed layer only.

## 2. Current snapshot (16 Oct 2026)

| Holdco (KMI?) | Price | Listed stakes, Rs/share | Listed as % of price | Net cash, Rs/share | Stub P/E | Reference NAV | Discount |
|---|---|---|---|---|---|---|---|
| JSCL (no) | 23.32 | 30.1 | 129% | about −1 | n/a | 39.9 (unlisted at reported NAV) | **41.6%** |
| ENGROH (yes) | 260.65 | 137.9 | 53% | inside stub | 5.4x | 286 (mixed multiples) / 499 (Topline) | **9% / 48%** |
| ATRL (yes) | 1,219.10 | 261.4 | 21% | not split out | 4.9x | 1,536 at 6.57x | **~21%** |
| OGDC (yes) | 299.10 | 35.2 | 12% | not split out | 4.7x | 371 at 6.0x | **~19%** |
| POL (no) | 671.30 | 63.3 | 9% | not split out | 5.5x | 732 at 6.04x | ~8% |
| FFC (yes) | 537.87 | 100.5 | 19% | 52.3 (see caveat) | 12.5x | 553 | ~3% |
| LUCK (yes) | 400.56 | 33.7 | 8% | 53.0 | 6.0x | 393 | about −2% (a premium) |
| PSO (yes) | 368.04 | 91.2 | 25% | net debt, large | 8.6x | no usable OMC peer | n/a |
| HUBC (yes) | 193.43 | 0 (no listed stakes) | 0% | n/a | 5.06x consolidated | no market-based NAV | n/a |
| MARI, PPL (yes) | 630.73, 218.75 | no material listed stakes | – | – | – | – | n/a |
| DAWH | delisted | Renamed Engro Holdings (ENGROH) in Jan 2025; see ENGROH | | | | | |

KMI flags are from `data/kmi_allshare_2026-06-05.csv`.

## 3. Company detail

**JSCL (Jahangir Siddiqui & Co.). Not KMI.** Source: half-year report to 30 Jun 2026, PSX doc 281862, note 8 (observed).
- Listed holdings: 1,460.2m JSBL shares (71.21%) at Rs12.13 = Rs17.7bn; 42.19m EFUG at 120.72 = Rs5.1bn; 20.29m EFUL at 112.0 = Rs2.3bn; 121.2m ANL at 8.60 = Rs1.0bn; 2.19m SITC at 641.2 = Rs1.4bn. Total Rs27.5bn, or Rs30.1 per share on 915.9m shares.
- Unlisted, at reported net assets: Energy Infrastructure Holding Rs4.28bn, JS Infocom Rs2.12bn, Security General Rs0.97bn. Short-term investments are Rs2.66bn, including 4.94% of TRG.
- Liabilities are about Rs1.0bn. NAV is about Rs39.9 per share against a price of Rs23.32.
- Caveats: the JSBL shares are sponsor shares blocked by SBP. Deferred tax on gains is ignored. JSBL is itself a holdco: it owns 53.49% effective of BIPL (JSCL's look-through, observed).

**ENGROH (Engro Holdings, formerly Dawood Hercules). KMI.**
- Listed stakes: EFERT 56.27% (Topline via Mettis, 29 Jun 2026, asserted) is 751.4m shares × 194.82 = Rs146.4bn. EPCL is 510.73m shares × Rs38.60 = Rs19.7bn under the SPA of 31 Aug 2026 (PSX doc 282064, observed).
- Shares: 1,204.2m per the PSX page, before cancelling about 36m bought-back shares.
- H1 2026 owners' profit was Rs18.6bn (PSX doc 281897, observed): fertilizer 4.0bn, polymer 0.9bn, power and mining 8.8bn, towers 3.9bn, terminals 0.7bn, trading 0.9bn, other less eliminations −0.5bn. Excluding EFERT and EPCL and annualised, that is Rs27.4bn, or Rs22.8 per share. The stub of Rs122.8 per share is therefore 5.4x.
- Reference NAV: power at 5.05x, towers at an assumed 10x, terminals and trading at 6x gives Rs148 per share for the stub, so NAV is Rs286.
- Topline's SOTP is Rs499 per share, of which Engro Connect is Rs219 (Mettis, 29 Jun 2026, asserted). That implies a 48% discount at today's price.
- The holdco's own net debt is in scanned pages I could not read (unverified).

**ATRL. KMI.**
- Stakes: NRL 25% (20.0m shares) and APL 21.88% (27.2m shares) (PACRA Dec 2025, asserted). That is Rs27.9bn, or Rs261 per share.
- ATRL's 2025 share register (arl.com.pk, observed) shows Attock Oil Company at 61.06% and APL at 1.68% of ATRL.
- EPS of about Rs207 is derived from the screener P/E. About Rs15 of it is APL dividends. FY26 includes the war-driven refining windfall (see `knowledge/playbooks/catalyst_trade.md`).
- On 17 Jun 2026 ATRL received an offer for 70% of its unlisted Attock Hospital (doc 278694). That is immaterial.

**OGDC. KMI.** It owns 20% of MARI: 240.1m shares × 630.73 = Rs151.5bn (long-standing holding, asserted). EPS of Rs56 is derived from the screener.

**POL. Not KMI.** NRL 25% plus APL 7.02% (APL briefing 2025, asserted) is Rs18.0bn. EPS of Rs112.5 is derived from the screener.

**FFC. KMI.** Source: half-year report to 30 Jun 2026, PSX doc 281738 (observed).
- Listed associates and subsidiaries:
  - AKBL 64.72% (AKBL annual report via search, asserted): Rs100.2bn.
  - FFL about 82.2% (Simply Wall St, asserted; BR said 84.84% in 2024): Rs29.1bn.
  - AGL 223.83m shares, 37.36% (Profit, May 2025): Rs10.5bn.
  - FCCL about 93.6m shares (6.79% in 2015, so the count is an approximation): Rs4.8bn.
- Unlisted, at cost: PIA Equity Rs30.6bn (34% of the consortium SPV, 22.6% of PIACL), Thar Energy 6.0bn, wind 13.5bn, FFBL Power 6.6bn, Fauji Fresh n Freeze 5.2bn, others 4.6bn. Total Rs66.5bn, or Rs46 per share.
- Net cash: short-term investments 174.4bn plus cash 5.0bn minus borrowings 104.2bn = Rs75.2bn. Caveat: FFC also carries Rs213bn of trade and other payables, which include GIDC, so treating the investments as free cash flatters it.
- Core 2025 profit is Rs73.6bn less dividend and investment income after tax, about Rs44bn or Rs31 per share, valued at 11.5x.

**LUCK. KMI.** Source: FY26 annual report, PSX doc 282262, note 7 (observed).
- Listed: LCI 253.99m shares (55%) × 194.44 = Rs49.4bn.
- Unlisted, at cost: Lucky Electric Rs29.9bn (100%, pledged to lenders), Lucky Motor Rs12.9bn (71.14%), LCL Investment Holdings Rs4.6bn (100%, overseas cement), National Resources Rs1.7bn (33.3%), Yunus Energy Rs0.6bn (20%).
- Net cash: short-term investments 94.8bn plus cash 1.5bn minus borrowings 18.8bn = Rs77.6bn, or Rs53 per share.
- Earnings: standalone EPS 31.83 includes Rs15.8bn of subsidiary dividends and Rs9.1bn of mutual-fund dividends. Core cement is about Rs18.1 per share and unlisted subsidiaries contribute about Rs34.5 per share of the consolidated EPS of 60.78 (my split; tax rates assumed).
- No discount: cement at 7.26x plus subsidiaries at 5.05x gives Rs393.

**PSO. KMI.**
- It owns 63.56% of PRL, 400.4m shares × 106.95 = Rs42.8bn (PSO FY24 briefing and PACRA, asserted). The FY26 annual report says "63.6%" (doc 284943, observed).
- Standalone FY26 EPS was 32.10 (observed). Trade debts are Rs414.8bn and short-term borrowings Rs384.3bn, so no net-cash credit is given.

**HUBC. KMI.**
- All stakes are unlisted (FY26 annual report, doc 283369): CPHGC 47.5%, Thar Energy 60%, ThalNova, Prime International 50%, Mega Motor/BYD 50% via HPHL.
- Consolidated EPS was 38.26 and standalone 18.86. No broker SOTP was found, so a market-based discount cannot be computed.

## 4. History: listed-stake coverage at each year end (% of the holdco's market cap)

| Holdco | 2021 | 2022 | 2023 | 2024 | 2025 | 16 Oct 2026 | Reading |
|---|---|---|---|---|---|---|---|
| JSCL (JSBL+EFU+ANL+SITC) | 123 | 173 | 167 | 142 | 164 | 129 | The discount to listed value is 22% now, against 19%, 42%, 40%, 30% and 39% at past year ends. **Narrower than usual.** |
| PSO (PRL 63.56%) | 7 | 8 | 14 | 9 | 7 | **25** | A record share of the price. PSO's stub fell from Rs443 to Rs277 per share (−37%) while PRL tripled. |
| ENGROH (EFERT+EPCL at market) | – | – | – | – | 65 | 53 | Not comparable before 2025. The towers (Deodar) and thermal assets changed the base. |
| ENGRO layer (pre-2025) | 54 | 53 | 68 | 72 | – | – | The old Engro Corp traded at 1.4x to 1.9x its listed stakes. |
| DAWH → its ENGRO stake (214.5m shares, derived) | 127 | 124 | 122 | 76* | – | – | DH traded at an 18% to 21% discount to its ENGRO shares. *2024 was distorted by the swap. |
| ATRL (NRL+APL) | 82 | 75 | 48 | 28 | 32 | 21 | ATRL rerated much faster than its stakes. |
| LUCK (LCI 55%) | 18 | 23 | 16 | 17 | 11 | 8 | LCI fell 50% from Jul 2025, while LUCK held. |
| OGDC (MARI 20%) | 12 | 12 | 12 | 18 | 14 | 12 | Stable. |
| FFC (FFBL, AKBL, FCCL to 2024; AKBL, FFL, AGL, FCCL from 2025) | 23 | 18 | 26 | 19 | 19 | 19 | Stable. Stake percentages changed in 2025 with the FFBL merger. |
| POL (NRL+APL) | 8 | 5 | 8 | 6 | 8 | 9 | Stable. |

Approximations:
- PSO's 63.56% is applied to all years. In 2019 it was 52.68%, and the timing of the change is unverified.
- DH's 214.5m ENGRO shares are derived as 536.6m less 722.9m/2.24408. ENGRO's shares are taken as 576.16m (2021-22) and 536.63m (2023-24).
- FFC's pre-2025 stakes are FFBL 49.88% and AKBL 43.15% (VIS 2021 and 2013 filings, asserted).
- JSCL's holdings are held at June 2026 share counts.

**Unusually wide vs own history?** None of the KMI names is. PSO is the outlier in the other direction: the market gives PSO's own business its lowest value in two years, at the moment its listed stake is worth the most. That is a stub signal, not a classic holdco discount, and it sits on top of PSO's Rs415bn of circular-debt receivables.

## 5. Ranking

**By discount width** (stated multiples, 16 Oct 2026):
1. JSCL, 41.6%, not KMI.
2. ENGROH, 48% on Topline's DCF but 9% on market multiples, KMI.
3. ATRL, about 21%, KMI, multiple-based.
4. OGDC, about 19%, KMI, multiple-based.
5. POL, 8%.
6. FFC, 3%.
7. LUCK, about 0.

PSO and HUBC are unranked.

**By catalysts that could close the gap:**

| Holdco | Catalyst | Status and date | Strength |
|---|---|---|---|
| ENGROH | Buyback of up to 45m shares, 7 May to 25 Oct 2026 | About 36.0m bought by 15 Oct: 21.0m to 27 Jul at Rs281.68 (doc 281897) plus 15.0m at Rs263.7 average from 28 Jul to 15 Oct (my sum of daily filings) | Strong now; ends 25 Oct |
| ENGROH | EPCL sale cash of Rs19.7bn (about Rs16 per share) arrives at Engro Corp | Needs approvals; offer deadline 7 Dec 2026 | Medium. The cash stays in a subsidiary unless upstreamed, and inter-corporate dividend tax applies (ENGROH H1 report) |
| ENGROH | Listing or sale of a stake in Engro Connect (towers) | Not announced (unverified) | Speculative |
| PSO | PRL upgrade agreement signed 24 Sep 2026 (doc 283398) | Capex funding could mean a PRL rights issue, which PSO would fund at 63.56% (inference) | Could widen the gap before closing it |
| JSCL | Emergent board meeting on 13 Oct 2026, "other than financial results" (doc 285572) | Content unread | Unknown |
| FFC | PIA call option for the remaining 25% exercised (doc 281738) | More cash going into an unlisted, loss-making asset | Negative for any discount |
| LUCK, HUBC | GEPCO bid as part of the Lucky/Hub/Kohat/Metro consortium | Prequalified 5 Oct 2026; sale targeted for Feb 2027 (Tribune, Bol News) | Negative, as cash goes out |
| ATRL | Refinery upgrade policy; hospital sale | Hospital is immaterial | Weak |

## 6. How to use this

- A holdco discount pays only if something forces it closed: buybacks below NAV, dividends passed up from subsidiaries, listing a subsidiary, a merger, or a sale.
- ENGROH is the only KMI name where that mechanism is running now (buyback plus the EPCL sale), and its buyback window ends 25 Oct.
- After that, watch whether ENGROH announces a second buyback or passes the EPCL proceeds up to shareholders.
- Re-run sections 2 and 4 each quarter. The inputs are the PSX close, the stake share counts above, and the latest interim report.

## 7. Could not verify

- ENGROH's and OGDC's holdco net debt: the statements are scanned pages.
- Current FFL and FCCL stakes held by FFC.
- PSO's PRL percentage before 2024.
- HUBC broker SOTP.
- CHCC buyback progress: filings are scanned.
- OGDC and ATRL EPS are derived from screener P/Es, not read from filings.
- PKGS, AHCL and other holdcos were not covered.
