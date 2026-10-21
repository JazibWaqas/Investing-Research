# Sector map, 17 Oct 2026 (knowledge/sectors/README.md; formerly the root sector map)

Written 2026-10-17. Evidence: the sixteen notes in `knowledge/sectors/`, `knowledge/playbooks/catalyst_trade.md` and `practitioner_signals.md`, and `catalysts/catalyst_calendar.csv`. Momentum is computed here: equal-weight baskets of the KMI names each note lists, daily returns clipped at ±10% (this also neutralises most bonus gaps), 126 sessions from 13 Apr to 16 Oct 2026, against KMI All Share (+4.3% over the same window). Prices come from `seed/data/prices`, with `data/prices_raw` used where a seed file was missing (ATRL, OGDC, HUBC, ISL, BIPL and others). Script: `scripts/sector_momentum.py`. Price-only returns, so dividend payers (HUBC, PPL, FFC) are understated. Most notes ran out of web search, so broker research is largely absent. Treat the verdicts as judgment on documented evidence, not a backtested model.

**Regime today.** Policy rate 11.5% (hiked 100bp on 27 Apr, held since). 6M T-bill 12.40%, 12M 12.50% (14 Oct auction), so the curve prices a hike. Topline survey (17 Oct): 61% expect a hike on 26 Oct. September CPI 10.3% (unverified on PBS) after 11.1% in August; weekly SPI 11.38% and rising. Brent about $105-110 on futures. Base case here: a 26 Oct hike is about 55% likely.

## 1. Ranking

Momentum has two columns. "Full" is every KMI name in the note. "Core" is the liquid names a Rs50k account can actually trade. They differ a lot where pumped small caps dominate the full basket (textiles: ASTM +175% in a year; Islamic financials: FPJM).

| # | Sector | (a) Catalysts, next 3 months | (b) 6m rel. to KMI, full / core (pts) | (c) Valuation vs own history (from notes) | (d) Fit with a hike-pricing curve | Verdict |
|---|---|---|---|---|---|---|
| 1 | E&P | Mildly positive | -3.5 / -3.5 | P/E 5.3-6 on EPS flattered by a one-off tax reversal; lagged KSE by 32 pts in 2025. No 5-year P/E series given | Good. Outperformed in 3 of 3 first-hike windows (+4, +9, +1) | Overweight |
| 2 | Fertilizer | Neutral to mildly positive (FFC) | -4.4 / -4.4 | FFC 8.8x consolidated, 7.3% yield; no history given | Good. +12, +21, -2 in the three hike windows | Overweight, FFC only |
| 3 | Islamic banks | Mildly positive (lagged repricing) | +23.6 / -1.4 | MEBL P/B 3.3, fair (target +14%); BIPL P/B 0.56 | Best. High-CASA spreads widen on hikes; +22, +4, +1 | Overweight, MEBL core |
| 4 | OMC | Mildly positive, low conviction | +14.1 / +1.0 (3m +10) | PSO P/B 0.59 against 0.31 at the FY24 trough and Rs503 in Jan 2026: mid-range | Poor. 100bp costs PSO about Rs3.8bn pre-tax | Overweight, PSO satellite |
| 5 | Tech | Neutral to mildly positive | -13.5 / -14.3 | SYS 15x TTM, mid of 106-174 range; NETSOL P/B 0.8, 4.6x | Poor for SYS multiples; NETSOL too cheap to care | Overweight, NETSOL only |
| 6 | Gas utilities, misc | Event-driven, mildly positive SNGP | +1.6 / -13.1 | SNGP 3.9x near 12-month low; SSGC -56% from Jul 2025 | Poor. Heavy short-term borrowing | Neutral, small SNGP event bet |
| 7 | Power | Flat to mildly negative | +1.6 / -15.1 | HUBC 5.1x consolidated against 3.0x at the 2023 trough; 10% yield | Mixed. +21 in 2021, -2 in 2018, -17 now | Neutral, HUBC as ballast |
| 8 | Glass, packaging | Neutral to slightly negative | +15.0 / -1.2 | TGL, GHGL near book at 5-7x | Glass net cash is fine; levered paper is not | Neutral, GHGL the one long |
| 9 | Refineries | Mixed to mildly negative | +98.4 / +98.4 | Re-rated about 2x vs KSE since June; Topline targets only +28-29% | Neutral; cracks dominate | Neutral, hold, no new entry |
| 10 | Food, staples | Mixed, stock-specific | -0.6 / +11.4 | FCEPL +89% since March; no history given | Neutral (defensive) | Neutral |
| 11 | Autos | Mixed, negative skew | +6.1 / +13.0 (3m -7.6) | SAZEW 3.9x at a 52-week low, HCAR -34% in 12 months: cheap | Worst. Volumes swing 2x on financing cost | Neutral until 26 Oct |
| 12 | Cement | Neutral to mildly negative | -0.8 / -2.2 | 14-33% below 2-year highs, P/E 7-12 | Poor. Trades as an oil and rates proxy | Neutral |
| 13 | Steel | Neutral to mildly negative | +5.3 / +4.0 | Lagged the market 45 pts since May 2024; ISL 9x | Poor. Leveraged | Avoid |
| 14 | Pharma | Neutral to slightly negative | -10.1 / -11.3 | Sector -25% since Sep 2025, P/E 10-12 | Poor. -7, -5, -11 in the three hike windows | Avoid |
| 15 | Textiles | Negative | +40.6 / -1.4 | Ratio to KSE 0.68 against 1.18 in 2023 and the 0.55 low of Apr 2025: cheap | Poor. Leveraged, energy-squeezed | Avoid |
| 16 | Chemicals | Negative | +8.3 / -10.4 | Chem index 0.82 vs market against 1.56 in Jan 2024; cheap on weak earnings | Poor. EPCL net debt Rs40bn | Avoid |

Hike-window figures are 6-month excess returns of the seed sector series (`seed/data/macro/sector_monthly_ret.csv`) after the first hikes of Jan 2018 and Sep 2021 and the Apr 2026 hike. n=3, and the 2026 window is dominated by the oil war. See `knowledge/playbooks/sector_rotation.md`.

**How this maps to the 50/50 plan.** Core (about half): FFC, MEBL, OGDC or PPL, with HUBC for yield. High-risk sleeve: NETSOL, PSO, a small SNGP event position, GHGL, and SAZEW only after its 23 Oct print and the 26 Oct MPC. KEL is a lottery ticket at most.

## 2. Sector blocks

**E&P (OGDC, PPL, MARI)**
- Levers: oil times PKR, wellhead gas price, curtailment, tax, circular-debt cash.
- State: Brent about $106, Hormuz shut; wellhead +8-10%; 1QFY27 profit +44% YoY expected; Rs1.49tr debt plan unapproved.
- Next: PPL ex about 19 Oct; results late Oct (OGDC about 29 Oct); debt plan, no date.
- Up: PPL, OGDC. Down: MARI (curtailment); all three on a Hormuz deal.
- Verdict: overweight. Cheapest hike-regime earners, but core, not lottery.

**Fertilizer (FFC, EFERT, FATIMA, ENGROH)**
- Levers: gas allocation and price, inventory, retail urea price, DAP margin, payout.
- State: inventory 645k t against 1.15 Mt a year ago, 519k t of it at EFERT; Qatar force majeure to 6 Nov; FFC Q2 EPS +39%.
- Next: EFERT 19 Oct, FFC about 23 Oct, FATIMA about 27 Oct, Qatar 6 Nov.
- Up: FFC. Down: FATIMA (RLNG plants, no dividend), EFERT (inventory).
- Verdict: overweight via FFC only.

**Islamic banks (MEBL, FABL, BIPL)**
- Levers: sukuk spread over CASA funding, 52% tax, fees against costs.
- State: H1 spread +2% on lower average rates; the April hike reprices with a lag.
- Next: MEBL, FABL 22 Oct; BIPL 23 Oct; MPC 26 Oct; ex-dividends about 3 Nov.
- Up: MEBL on a hike. Down: BIPL (illiquid, unexplained 2025 profit halving); avoid FPJM.
- Verdict: overweight MEBL as the hike hedge; expect +10-15% plus dividends.

**OMC (PSO)**
- Levers: Rs7.87 margin, inventory gains, Rs415bn receivables on Rs384bn short-term debt, government claims.
- State: Q4 implied loss about Rs30/share; daily pricing since 21 Jul; Rs1.22 margin rise not notified.
- Next: ex about 20 Oct, Q1 22-30 Oct, margin and windfall decisions undated.
- Up and down: PSO either way (margin vs clawback or hike).
- Verdict: overweight, satellite size. The 2024 re-rating shape; rates are the risk.

**Tech (SYS, NETSOL, AIRLINK)**
- Levers: USD exports, PKR against rupee costs, tax, Gulf collections, handset policy.
- State: exports +18% in September; tax regime fixed to TY2029; rupee strength squeezes SYS.
- Next: NETSOL ex 21 Oct, SYS about 27 Oct, NETSOL about 30 Oct.
- Up: NETSOL (4.6x, net cash a third of market cap). Down: SYS on a hike; AIRLINK.
- Verdict: overweight NETSOL only; the sector multiple is hike-exposed.

**Gas utilities (SNGP, SSGC, PIBTL, PAEL)**
- Levers: FRR true-up, UFG disallowance, Rs3.61tn gas circular debt, rates.
- State: FY26 FRRs undecided; accounts delayed to 27 Nov; SNGP 3.9x.
- Next: PIBTL about 22 Oct, FRR by about 6 Nov, results by 27 Nov.
- Up: SNGP on a benign FRR. Down: SSGC (qualified audit), PIBTL (lumpy).
- Verdict: neutral, small SNGP event position.

**Power (HUBC, KEL)**
- Levers: PPA terms, circular-debt cash, dispatch, associate dividends, NEPRA and rates.
- State: circular debt Rs1.835tn above the IMF ceiling; Chinese IPPs unsigned; KEL -29% since June, SHC stay 7 Oct.
- Next: HUBC AGM 20 Oct, results late Oct, KE hearings, DISCO bids.
- Up: KEL on a settlement (+40%, about 25% odds). Down: HUBC on a big GEPCO cheque.
- Verdict: neutral; HUBC is ballast.

**Glass, packaging (GHGL, TGL, PKGS, IPAK)**
- Levers: price minus energy and resin, glass overcapacity, leverage.
- State: spot Brent above $120; TGL's idle furnace caps float prices; GHGL EPS +22%.
- Next: GHGL ex about 21 Oct, results about 28 Oct; PKGS about 30 Oct.
- Up: GHGL (easy 0.71 base). Down: PKGS, CEPB, IPAK on a hike.
- Verdict: neutral; GHGL the one long.

**Refineries (ATRL, PRL, NRL, CNERGY)**
- Levers: diesel crack against the $41.89 cap, GRM, upgrade policy, inventory, utilisation.
- State: re-rated about 2x since June; GRM $36.7 July, $28.8 August.
- Next: ATRL, NRL 19 Oct; cap review about 20 Oct; PRL briefing 26 Oct; deemed duty 15 Nov.
- Up: ATRL. Down: PRL (rights), CNERGY; all on a $30 cap.
- Verdict: neutral; hold, no new entries. Every veto signal is live.

**Food (FCEPL, MFL, NESTLE, UNITY)**
- Levers: raw-material spread, pricing power, PKR, PET rules, governance.
- State: FCEPL margin 12% to 23%; Nestle profit -19.5%; UNITY FIR and missing filings.
- Next: FCEPL 23 Oct, MFL offer news about 28 Oct, UNITY accounts about 31 Oct.
- Up: MFL. Down: UNITY (avoid), FCEPL if the margin slips.
- Verdict: neutral; stock events only.

**Autos (SAZEW, HCAR, GAL)**
- Levers: financing cost, 2026-31 policy, PKR, tractor schemes, Chinese share.
- State: 1Q cars +43%, September -20% MoM; policy promised about 21 Oct.
- Next: policy about 21 Oct, SAZEW about 23 Oct, MPC 26 Oct, PAMA about 13 Nov.
- Up: SAZEW (3.9x), HCAR. Down: everyone on a hike.
- Verdict: neutral until 26 Oct; first buy when the rotation rule fires.

**Cement (LUCK, DGKC, MLCF, FCCL)**
- Levers: despatches, retail price, coal and freight, exports, finance cost.
- State: September +7.4%, price +10% YoY; coal and oil up; North exports zero.
- Next: MLCF EOGM 19 Oct, CHCC 22 Oct, FCCL 27 Oct, APCMA about 3 Nov.
- Up: North names on Torkham. Down: all on a hike or Brent above $120.
- Verdict: neutral; overweight on Brent below $90 plus an SBP pause.

**Steel (ISL, ASL, MUGHAL)**
- Levers: construction demand, scrap spread, power, anti-dumping, finance cost.
- State: FY26 recovery unrewarded; Mughal Q4 EPS -29%.
- Next: ISL 20 Oct, INIL 27 Oct, NTC final about Mar 2027.
- Up: ISL. Down: MUGHAL (debt +36%).
- Verdict: avoid; watch for a fourth ASL sponsor buy.

**Pharma (ABOT, GLAXO, SEARL)**
- Levers: regulated prices against dollar inputs, PKR, volume, refunds.
- State: PKR flat three years, margin recovery already in earnings; hardship cases undated.
- Next: HALEON about 27 Oct, others late Oct.
- Up: ABOT. Down: SEARL (geared).
- Verdict: avoid; no dated catalyst, rate-exposed multiple.

**Textiles (NML, ILP)**
- Levers: exports, energy cost, cotton spread, policy support, freight.
- State: 1Q exports +5.3%, steep 2Q drop warned; power 11 US cents.
- Next: ILP 22 Oct, NEPRA 29 Oct, DLTL decision undated.
- Up: NML on DLTL. Down: leveraged spinners.
- Verdict: avoid; upside needs an IMF-constrained decision.

**Chemicals (EPCL, LOTCHEM, LCI)**
- Levers: feedstock spread, anti-dumping, gas levy, rates.
- State: EPCL delta -18%; Noventra Q3 gross profit Rs0.5bn against Rs2.7bn; EPCL sale at Rs38.60.
- Next: EPCL 20 Oct, LCI 26 Oct, offer terms November, PVC duty lapse about 23 Nov.
- Up: EPCL on a generous offer. Down: LOTCHEM (rights).
- Verdict: avoid; fails leg 1.

## 3. Where the 2026 refiner-type setup exists today

The three legs from `catalyst_trade.md`: (1) the last quarter's earnings already inflected and the price ignored it; (2) a spread widening; (3) a policy decision pending.

| Sector, name | Leg 1, earnings | Leg 2, spread | Leg 3, policy | Read |
|---|---|---|---|---|
| E&P: OGDC, PPL | Partial. FY26 strong but tax-flattered; 1QFY27 +44% YoY is the real test | Yes. Brent about $106 against $70 in June; wellhead +8-10% | Debt plan pending | Closest match. 1Q prints decide leg 1. Veto: a Hormuz deal |
| OMC: PSO | Not yet. Q4 was a loss; Q1 is the test | Yes while crude rises (inventory gains) | Rs1.22 margin pending | Two legs, waiting on Q1. Veto: windfall clawback |
| Autos: SAZEW | Yes. 3.9x trailing, FY26 profit +44%, at a 52-week low | No. Financing cost is rising | Auto policy pending | Legs 1 and 3. Leg 2 points the wrong way until rates turn |
| Gas: SNGP | Hidden. Accounts delayed to 27 Nov | Regulated return | FRR plus debt plan | SSGC-2024 shape, binary |
| Tech: NETSOL | Yes. EPS +72%, 4.6x | No. Rupee strength narrows it | Tax extension already passed | A loaded spring without a trigger, except the 30 Oct print |
| Steel: ISL | Yes. Record Q4 EPS 2.90 | No. Scrap spread narrowed | Colour-coated duty, final about Mar 2027 | Too early |

No sector has all three legs today. E&P is nearest. The refiners had all three on 8-9 Jul and are now in the veto phase.

## 4. Conflicts between notes, and resolutions

1. **Brent.** Cement, chemicals, glass, pharma and the playbook use FRED spot $126.6 (14 Oct); refiners, E&P and OMC use futures at $104-109. FRED DCOILBRENTEU is dated physical Brent, which can sit well above front-month futures in a supply shock; Profit (17 Oct) has futures touching $110. Use $105-110 for earnings; the spot premium is unverified.
2. **PKR.** Autos and textiles cite about 268 from `data/macro/usdpkr.csv`; others use 277. Use 277.01 (ProPakistani, 8 Oct). The repo series has bad ticks and needs cleaning.
3. **MPC.** Food guessed November; the rest say 26 Oct. Use 26 Oct, 14 Dec (not 15 Dec, which pharma and textiles inferred from 2025) and 25 Jan. OMC and tech expect a hold, but their source previewed the September meeting; the 17 Oct survey and the curve point to a hike. The April hike was 27 Apr, not 28 Apr (`policy_rate_decisions.csv`).
4. **CPI.** "11%" in cement and glass is August; September is about 10.3%. One lower print is not a turn while SPI rises.
5. **Does power lead in hikes?** Only after the 2021 hike (+21). It was -2 in 2018 and -17 since 27 Apr 2026; HUBC is -14 price-only (the Rs5 ex-dividend on 12 Oct counts against it). Islamic banks and E&P are the reliable hike-regime sectors.
6. **E&P "best fit" vs "no idea".** Both hold: the three-leg structure is there, but upside is about 15-25%. Core, not lottery.
7. **Group EPS.** PSO, ATRL, HUBC, MLCF, MFL, FATIMA and ENGROH screener figures are standalone or stale. Use consolidated per repo rules, except NML, whose consolidated profit is mostly associates.
8. **KMI eligibility.** The playbook lists INDU and POL; neither is KMI, nor are PNSC, APL, KAPCO, NPL, NCPL, PTC or TRG.
9. **Full vs core momentum.** Textiles (+41) and Islamic financials (+24) are lifted by pumps (ASTM, FPJM). Use the core figure.
10. **Steel and rates.** 0.05 monthly correlation (steel note) and "cyclicals lead after a first cut" (seed) are compatible: rates matter at turns, not month to month.
