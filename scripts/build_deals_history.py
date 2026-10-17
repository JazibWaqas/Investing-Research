"""Build data/deals_history.csv: every PSX takeover PAI (plus sponsor delistings) 2018 to Oct 2026.
Deal facts are hand-keyed from PSX filings and press (see source_urls); prices and returns are computed.
Run: .venv/Scripts/python.exe -I scripts/build_deals_history.py
"""
import os, glob
import pandas as pd, numpy as np

D = "https://dps.psx.com.pk/download/document/{}.pdf"
def docs(*ids): return " ".join(D.format(i) for i in ids)

T = "takeover"; L = "delisting"
R = []
def add(*a): R.append(a)
# type, sym, target, acquirer, pai_date, pai_hhmm, offer, pao_date, acc, acc_note, status, end, src, note
# ---- 2018 ----
add(T,"DCL","Dewan Cement","Mega Conglomerate (BMA Capital manager)","2018-01-31",None,None,None,None,"","withdrawn","2018-07-02","PSX archive BMA Capital titles","Withdrawal title names Dewan Cement")
add(T,"","Khurshid Spinning Mills","Beacon Impex (BMA Capital manager)","2018-05-07",None,None,None,None,"","withdrawn","2018-07-03","PSX archive BMA titles","Withdrawal of 3 Jul 2018 by BMA does not name the target; matched by elimination (asserted). Symbol not on the PSX API")
add(T,"DATM","Data Textiles","Pearl Securities client (acquirer not read)","2018-05-22",None,None,None,None,"","unknown",None,docs(114786,124604,134661),"Earlier PAI withdrawn 16 May 2018; re-filed 22 May; extension requested 14 Dec 2018; no PAO or withdrawal found")
add(T,"GLOT","Globe Textile Mills","AKD Securities client (SPA for 81.98%)","2018-07-17",None,None,None,None,"","unknown",None,docs(116394,122488),"No PAO or withdrawal found")
add(T,"FFL","Fauji Foods","Inner Mongolia Yili (Citibank manager)","2018-07-31",None,None,None,None,"","withdrawn","2019-04-29","https://propakistani.pk/2018/07/31/inner-mongolia-yili-to-acquire-51-stake-in-fauji-foods/ https://yicaiglobal.com/news/chinese-dairy-giant-yili-ends-bid-for-pakistani-food-firm","Extended once; Yili withdrew 29 Apr 2019 as the offer period lapsed (press)")
add(T,"KEL","K-Electric","Shanghai Electric Power","2018-03-27",None,None,None,None,"","withdrawn","2018-12-20",docs(111974,123645,123737,164037,229592),"Chain of 180-day PAIs renewed 2018 to 2023 and finally withdrawn 22 Apr 2024. Return is measured on the first leg only (to 20 Dec 2018)")
add(T,"DNCC","Dandot Cement","Calicom Industries (Pervez Ahmed Capital manager)","2018-11-05",None,None,"2018-11-30",None,"Offer for 16.5%; buyer reported holding the 67% SPA block 30 Apr 2019","completed","2019-04-30",docs(122210,123055,129735)+" https://mettisglobal.news/calicom-industries-to-acquire-16-5-share-capital-of-dandot-cement-ltd","Completion date is the company disclosure that Calicom acquired the shares; payment date of the tender not found")
add(T,"JOPP","Johnson & Phillips (Pakistan)","Next Capital client","2018-11-27",None,66.30,"2019-07-30",None,"Fulfilment filing for 1,097,718 shares","completed","2019-10-03",docs(122967,133138,135863),"Offer price from offer letter (doc 133138). Delisted 2024")
# ---- 2019-2020 ----
add(T,"COLG","Colgate-Palmolive (Pakistan)","Colgate-Palmolive Company (AHL manager)","2019-05-07",None,None,None,None,"","withdrawn","2020-01-30","https://profit.pakistantoday.com.pk/?p=81373 https://mettisglobal.news/arif-habib-withdraws-poi-made-by-colgate-palmolive-to-acquire-21-shares-of-colgate-pakistan","PAI date from press (Dawn 7 May 2019); not in the archive. Up to 21%; parties could not agree terms")
add(T,"MFFL","Mitchells Fruit Farms","Waves Singer Pakistan (Next Capital manager)","2019-08-07",None,None,None,None,"","withdrawn","2020-01-31",docs(133253,142144),"Up to 30% plus control; withdrawn")
add(T,"NEXT","Next Capital","JS Global Capital (45.03%)","2019-12-11",None,None,None,None,"","withdrawn","2020-06-09",docs(140347,140370,148781),"")
add(T,"","Mian Textile Industries","Mr Ali Arif (Next Capital manager)","2020-03-06",None,None,None,None,"","unknown",None,docs(144407),"74.15%; symbol not found on the PSX API; no outcome found")
add(T,"SMBL","Summit Bank","Potential acquirer (Reg 6(3) notice); Lootah consortium made the 2022 offer","2020-03-30",None,None,"2022-03-18",None,"Tender offer announced 18 Mar 2022 (Business Recorder)","unknown",None,docs(145258,177451,183870)+" https://www.brecorder.com/news/amp/40162478","Extended Nov 2021; offer announced Mar 2022; completion not found")
add(T,"BIPLS","BIPL Securities","JS Global Capital (77.12%)","2020-08-11",None,None,None,None,"","withdrawn","2020-11-04",docs(150809,156875),"")
add(T,"WTL","Worldcall Telecom","Acquirer not read (more than 51%)","2020-08-07",None,None,None,None,"","unknown",None,docs(150734,161791,177817),"Extended Feb 2021 and again Nov 2021 after a second Reg 5 disclosure (May 2021); no PAO found")
add(T,"BIPLS","BIPL Securities","Acquirer not read","2020-11-25",None,None,None,None,"Book closure notice 30 Apr 2021 implies a PAO","completed","2021-06-15",docs(157756,164386,166472),"Low confidence: inferred from a Reg 9 book closure notice; completion date approximate")
add(T,"UDPL","United Distributors Pakistan","Acquirer not read","2020-12-09",None,None,"2021-01-27",None,"","completed","2021-03-05",docs(158320,160217,161550),"Completion date approximate: book closure notice 19 Feb 2021 then offer window; payment not filed in archive")
add(T,"SMTM","Samin Textiles","Acquirer not read","2021-01-18",None,None,"2021-01-27",None,"","completed","2021-03-05",docs(159737,160451),"Completion inferred from the proposed offer letter of 1 Feb 2021; date approximate")
add(T,"TRIPF","Tri-Pack Films","Packages Ltd","2021-02-18","10:35",245.20,"2021-10-28","filled","Buyer reached 69.26% (deals.md)","completed","2021-12-29",docs(161361,175576,179346),"deals.md used 17 Feb 2021 as the PAI date; the archive timestamp is 18 Feb 10:35")
add(T,"HCL","Hallmark Company","Acquirers not read (more than 50%)","2021-06-08",None,73.305,"2021-08-06",None,"Offer for 82,890 shares","completed","2021-09-15",docs(167866,169768,170131,170831),"Completion date approximate (book closure 26 Aug 2021)")
# ---- 2021-2023 ----
add(T,"HUMNL","Hum Network","Duraid Qureshi","2021-10-25",None,7.00,"2021-12-24",None,"Results filed 23 Feb 2022","completed","2022-02-23",docs(175157,179163,182136,179396),"Offer price from the offer letter (doc 179396); 28-day VWAP was 6.67")
add(T,"KCL","Karam Ceramics","Swat Ceramics","2021-11-12",None,None,"2022-05-13",None,"Results filed 14 Jul 2022","completed","2022-07-14",docs(177264,187288,189564),"Offer price is in a scanned filing, not read")
add(T,"SBL","Samba Bank","Fatima consortium (AHL manager)","2021-12-21",None,None,None,None,"","withdrawn","2022-05-20",docs(178977,187584),"84.51%")
add(T,"SAPL","Sanofi-Aventis Pakistan","Packages consortium","2021-12-27",None,1704.0,"2022-06-28","filled","6.07% acquired (deals.md)","completed","2022-09-02",docs(189091,191216,191592),"")
add(T,"SBL","Samba Bank","United Bank Ltd (AKD manager)","2022-02-04",None,None,None,None,"","withdrawn","2022-05-24",docs(180931,187706),"84.51%, competing with the Fatima consortium")
add(T,"ESBL","Escorts Investment Bank","Acquirer not read (more than 50%)","2022-03-11",None,None,None,None,"","unknown",None,docs(183574),"No PAO or withdrawal found")
add(T,"SPLC","Saudi Pak Leasing","Ansari Bros / ICON Global / Adam Securities client (competing PAIs)","2021-06-10",None,None,None,None,"","withdrawn","2022-03-08",docs(167959,167973,183402,183406),"Withdrawn 8 Mar 2022")
add(T,"SPLC","Saudi Pak Leasing","Progressive Group International (35%)","2022-03-07",None,None,None,None,"","unknown",None,docs(183308),"No PAO or withdrawal found")
add(T,"SPLC","Saudi Pak Leasing","Ansari Bros Pvt Ltd","2022-03-09",None,None,None,None,"","withdrawn","2022-12-07",docs(183461,198870),"")
add(T,"SPLC","Saudi Pak Leasing","Ansari Bros Pvt Ltd (re-filed)","2022-12-08",None,None,None,None,"","unknown",None,docs(198904),"Company moved to delisting in 2023; no PAO found")
add(T,"SILK","Silkbank","Park View Enclave (51%)","2022-05-31",None,None,None,None,"","withdrawn","2022-10-31",docs(188026,196721),"")
add(T,"LOTCHEM","Lotte Chemical Pakistan","Novatex / ICI Pakistan (75.01%)","2022-07-07",None,None,None,None,"","withdrawn","2023-01-06",docs(189439,200260),"")
add(T,"ZIL","ZIL Limited","New Future Consumer International","2022-07-14",None,None,"2023-03-16",None,"Acquisition completed per NFCI, Jun 2023","completed","2023-06-01",docs(189525,204290,209659)+" https://www.brecorder.com/news/amp/40246119","This is a re-filed PAI; the original date was not found. Public offer for 19.32% (ProPakistani)")
add(T,"BIPL","BankIslami Pakistan","JS Bank Ltd","2022-11-15",None,23.99,"2023-06-27",None,"Buyer reached 75.12% (deals.md)","completed","2023-08-23",docs(197893,211357,211581,213875),"")
add(T,"BGL","Balochistan Glass","Tariq Glass Industries (via MMM Holding)","2023-03-21",None,None,"2023-08-10",None,"Dispatch Sep 2023","completed","2023-10-09",docs(204474,213116,215754,217391),"Completion date approximate (information filing 9 Oct 2023)")
add(T,"HCL","Hallmark Company","Supernet Infrastructure","2023-03-03",None,47.74,"2023-07-19",None,"","completed","2023-08-16",docs(203654,212152,213343),"Offer price from the offer letter; completion approximate (Material Information 16 Aug 2023)")
add(T,"LOTCHEM","Lotte Chemical Pakistan","Lucky Core Ventures (re-filed chain)","2023-05-02",None,None,None,None,"","withdrawn","2024-01-16",docs(207800,215419,219224,223916),"Re-filed after a Jan 2023 withdrawal; amended Sep 2023; extended Oct 2023; withdrawn 16 Jan 2024. First filing date of this chain not in archive")
add(T,"HASCOL","Hascol Petroleum","Taj Gasoline (41%)","2023-06-14",None,None,None,None,"","withdrawn","2024-01-16",docs(210420,223872),"")
add(T,"SHEL","Shell Pakistan","Pakistan Refinery + Air Link","2023-07-17","09:15",None,None,None,"","unknown",None,docs(212035),"deals.md counted this date as the Wafi PAI. Wafi PAI was 31 Oct 2023. No PAO for this bid found")
add(T,"BWHL","Balochistan Wheels","RMS (Pvt) Ltd (63.56%)","2023-08-07",None,None,None,None,"","withdrawn","2024-05-06",docs(212955,231295),"")
add(T,"ESBL","Escorts Investment Bank","RMS (Pvt) Ltd (87.96%)","2023-08-11",None,None,None,None,"","withdrawn","2024-05-13",docs(213199,231600),"")
add(T,"SHEL","Shell Pakistan","Prax Overseas Holdings (77.42%)","2023-10-16",None,None,None,None,"","withdrawn","2023-11-08",docs(217792,220903),"Competing bid, withdrawn after 3 weeks")
add(T,"SHEL","Shell Pakistan","Wafi Energy","2023-10-31",None,155.11,"2024-07-25","filled","70% to 100% accepted (deals.md)","completed","2024-10-08",docs(219964,234459,239185),"deals.md dated this deal 17 Jul 2023 (449 days); from this PAI it is 343 days")
add(T,"HASCOL","Hascol Petroleum","Millat Global Holdings (76%)","2023-12-19",None,None,None,None,"","withdrawn","2024-06-20",docs(222687,233048),"")
add(T,"CASH","Calcorp","JS Global Capital (83.96%)","2024-02-20",None,None,None,None,"","withdrawn","2024-11-15",docs(225572,242868),"")
add(T,"EPQL","Engro Powergen Qadirpur","Liberty Power Holding / Soorty / Procon (68.89%)","2024-02-26",None,None,None,None,"","withdrawn","2024-11-22",docs(226010,243263),"Re-filed 3 Dec 2024")
add(T,"UNITY","Unity Foods","Wilmar group","2024-03-19",None,27.34,"2024-04-17",None,"","completed","2024-06-25",docs(227664,229179,233296),"Offer raised from 24.89 to 27.34 (deals.md)")
add(T,"SBL","Samba Bank","Bank Alfalah (84.51%)","2024-04-09",None,None,None,None,"","withdrawn","2024-11-13",docs(228881,240418,242747),"")
add(T,"BELA","Bela Automotives","Amir Noman (Adam Securities)","2024-06-11",None,None,"2025-05-16",None,"","unknown",None,"https://mettisglobal.news/amir-noman-extends-deadline-to-acquire-50-stake-in-bela-automotives/","Re-filed 19 Mar 2025; PAO 16 May 2025; result not found; company is in the defaulter segment")
add(T,"AGL","Agritech","Maple Leaf Cement (competing offer from FFC, Dec 2024)","2024-07-25",None,39.00,None,None,"MLCF fulfilment filing 8 Jan 2025; FFC offer drew 5% (Profit, asserted)","completed","2025-01-08",docs(234428,242724,244170,245644),"Offer 39.00 from the comparative statement (doc 242724); which bidder it belongs to is not certain")
add(T,"PKGI","Pakistan General Insurance","Muhammad Shahzad Habib group (SECP-directed mandatory offer)","2024-10-14",None,13.44,"2025-05-20",None,"Result filed 16 Jul 2025","completed","2025-07-16",docs(239494,254114,256520),"")
add(T,"MFFL","Mitchells Fruit Farms","CCL Holding","2024-11-13",None,232.75,"2025-07-28","filled","Filled (deals.md)","completed","2025-09-30",docs(242717,257013,257273),"")
add(T,"CASH","Calcorp","Asif Ali Shaikh and associates","2024-12-03",None,32.98,"2025-03-03",None,"Offer for 8.02%","completed","2025-04-30",docs(243829,249034,253225),"")
add(T,"EPQL","Engro Powergen Qadirpur","Liberty Power Holding / Soorty / Procon (re-filed)","2024-12-03",None,None,None,None,"","withdrawn","2025-04-03",docs(243823,250395),"")
add(T,"NRSL","Nimir Resins","Acquirer not read (AKD manager)","2024-12-20",None,25.00,"2024-12-31",None,"Offer for 21.42%","completed","2025-02-27",docs(244722,245215,248486),"")
add(T,"TRG","TRG Pakistan","Greentree Holdings (35.147%)","2024-12-23",None,75.00,"2025-01-15",None,"Tender window ran to 25 Apr 2025; no acceptance count found","lapsed","2025-06-18",docs(244799,245907,254844)+" https://profit.pakistantoday.com.pk/?p=200077 https://profit.pakistantoday.com.pk/?p=202843","Offer unwound: SECP let holders reclaim tendered shares until 18 Jun 2025, and the Sindh High Court later voided the offer (Profit)")
# ---- 2025 ----
add(T,"LOTCHEM","Lotte Chemical Pakistan","PTA Global Holding consortium","2025-02-13",None,22.37,"2025-07-10",29.8,"56.4m of 189.2m (deals.md)","completed","2025-09-08",docs(247304,256280,258989),"")
add(T,"ESBL","Escorts Investment Bank","Kamran Malik and Sheikh Ali Baakza (AKD manager; 6.02% plus control)","2025-04-17","14:58",None,None,None,"","pending",None,docs(251327,251346,261957,268980,280614,280673)+" https://propakistani.pk/2026/01/21/two-investors-submit-offer-to-take-over-escorts-investment-bank/amp/","Renewed Oct 2025, Jan 2026 and Jul 2026; timeline extended 90 days on 31 Jul 2026")
add(T,"PGLC","Pak-Gulf Leasing","IWT Investments (Rafi Securities)","2025-04-17",None,None,None,None,"","withdrawn","2025-07-07",docs(251356)+" https://profit.pakistantoday.com.pk/2025/07/07/iwt-investments-withdraws-intent-to-acquire-majority-stake-in-pak-gulf-leasing","Voluntary withdrawal; consultant approval pending")
add(T,"RMPL","Rafhan Maize Products","Cherat Cement (CHCC), 75.69%","2025-05-08",None,None,None,None,"","withdrawn","2025-09-26",docs(253581,260212),"Competing with Nishat and Sapphire")
add(T,"RMPL","Rafhan Maize Products","Nishat Hotels and Properties (Nishat group)","2025-05-14","13:54",9800.0,"2026-03-26",73.0,"Doc 277722","completed","2026-05-22",docs(253826,270035,273038,273287,277722),"Withdrawn and re-filed 6 and 11 Feb 2026; treated as one campaign")
add(T,"RMPL","Rafhan Maize Products","SFL (Sapphire)","2025-05-19",None,None,None,None,"","withdrawn","2025-12-31",docs(254043,268041),"")
add(T,"ZIL","ZIL Limited","TWF Holding (Alpha Beta manager)","2025-05-15",None,297.50,None,None,"","unknown",None,"https://profit.pakistantoday.com.pk/2025/05/15/twf-holding-acquires-majority-stake-in-zil-limited-in-major-share-purchase-deal/ https://mettisglobal.news/alpha-beta-submits-pai-on-clients-behalf-to-acquire-over-51-stake-in-zil-limited/","Intra-group sale (same owner); SPA price shown; PAI date from press; no PAO found")
add(T,"ACPL","Attock Cement Pakistan","FCCL (Alpha Cement) + KAPCO","2025-06-03",None,330.41,"2026-02-16","filled","Buyers reached 92.03% (deals.md)","completed","2026-04-20",docs(254711,261920,265324,270187),"Withdrawn and re-filed Oct to Nov 2025; treated as one campaign")
add(T,"ACPL","Attock Cement Pakistan","Cherat Cement (CHCC)","2025-06-04",None,None,None,None,"","withdrawn","2025-10-30",docs(254782,264460),"")
add(T,"BAPL","Bawany Air Products","Mohabat Khan and others (Intermarket Securities)","2025-07-08",None,None,"2025-12-19",None,"Offer for 2,146,228 shares; expired 25 Mar 2026","completed","2026-03-25",docs(256199,268673,272960),"PAI date is the first Reg disclosure (doc 256199); offer price not read")
add(T,"TPLI","TPL Insurance","Jazz International (VEON)","2025-09-04","15:19",30.00,"2026-04-20",None,"Filled (deals.md)","completed","2026-06-30",docs(258862,274456,275097,279482),"")
add(T,"SLGL","Secure Logistics-Trax Group","Acquirer not read","2025-10-03",None,None,None,None,"","unknown",None,docs(260890),"Scanned; no outcome found")
add(T,"PIOC","Pioneer Cement","Maple Leaf Cement (MLCF)","2025-11-13","13:22",478.43,"2025-12-18",162.0,"Tendered 162% of offer; pro rata 61.64% (doc 270524)","completed","2026-02-17",docs(265618,267426,270524),"")
# ---- 2026 pending ----
add(T,"SBL","Samba Bank","Najd Gateway Holding (SNB)","2026-02-18",None,None,None,None,"Price undisclosed","pending",None,docs(270513,281278),"PAO deadline extended 18 Aug 2026")
add(T,"EPCL","Engro Polymer & Chemicals","Noventra (formerly Lotte Chemical Pakistan)","2026-03-10",None,38.60,None,None,"Offer price is the SPA price; PAO not yet made","pending",None,docs(272303,282064,282317),"PAO deadline extended to 7 Dec 2026")
add(T,"AMBL","Apna Microfinance Bank","Mobilink Microfinance Bank","2026-03-10",None,None,None,None,"","pending",None,docs(272351,282316),"Extended 7 Sep 2026")
add(T,"BML","Bank Makramah","DM Holdings","2026-06-12",None,None,None,None,"","pending",None,docs(278478),"Terms not read")
add(T,"ASC","Al Shaheer Corporation","Farrukh/Amin group (AKD manager)","2026-06-30",None,None,None,None,"","pending",None,docs(279260,281148),"SECP suspended the acquisition by order of 10 Aug 2026")
add(T,"NICL","Nimir Industrial Chemicals","Cherat Cement (KTrade manager)","2026-09-10",None,None,None,None,"","pending",None,docs(282506),"At least 30%; price not disclosed")
# ---- sponsor delistings with a buy-back at a PSX-set price (separate base rate) ----
add(L,"PGCL","Pakistan Gum & Chemicals","Sponsors","2019-06-19",None,300.0,None,None,"","delisting_completed","2020-01-10",docs(131875),"Buy-back Rs300 (title 20 Sep 2019). Announcement date is the first delisting filing in the archive")
add(L,"AYTM","Ayesha Textile Mills","Sponsors","2019-09-20",None,200.0,None,None,"","delisting_completed","2019-11-01","PSX archive titles AYTM 20 Sep and 1 Nov 2019","Buy-back Rs200")
add(L,"AKZO","Akzo Nobel Pakistan","Sponsors","2020-03-04",None,270.0,None,None,"","delisting_completed","2020-07-10","PSX archive titles AKZO 4 Mar and 10 Jul 2020","Buy-back Rs270")
add(L,"WYETH","Wyeth Pakistan","Wyeth LLC","2021-08-16",None,2000.0,None,None,"","delisting_completed","2022-04-04","https://mettisglobal.news/wyeth-pakistan-delisted-at-buy-back-price-of-rs2000-per-share","PSX-approved minimum Rs2,000 (initial proposal Rs1,284). Delisted 4 Apr 2022")
add(L,"ADOS","Ados Pakistan","Sponsors","2021-12-28",None,29.0,None,None,"","delisting_completed","2022-08-11","PSX archive titles ADOS","Buy-back Rs29")
add(L,"PSMC","Pak Suzuki Motor","Suzuki Motor Corp","2023-10-19",None,609.0,None,None,"","delisting_completed","2024-04-23","https://carspiritpk.com/pak-suzuki-buyback-price-fixed-at-rs-609/","PSX-set minimum Rs609 (sponsor proposed Rs406). Completion date approximate (newspaper clipping on delisting)")
add(L,"PMPK","Philip Morris (Pakistan)","Philip Morris Investments","2025-03-26",None,1300.0,None,None,"","delisting_completed","2025-10-06","https://profit.pakistantoday.com.pk/2025/06/27/philip-morris-pakistan-accepts-voluntary-delisting-from-psx-at-rs1300-per-share/","PSX-set Rs1,300 (sponsor proposed Rs664)")
add(L,"GLPL","Gillette Pakistan","Sponsors","2025-10-02",None,700.0,None,None,"","delisting_completed","2026-05-19","https://www.techjuice.pk/tag/psx-delisting/","PSX-set Rs700 (initial proposal Rs216.49 per deals.md)")
add(L,"SCL","Shield Corporation","Sponsors","2025-11-19",None,750.0,None,None,"","delisting_completed","2026-07-24",docs(273979),"PSX-set Rs750; last trade 24 Jul 2026")

cols = ["type","sym","target","acquirer","pai_date","pai_hhmm","offer","pao_date","acc","acc_note","status","end","src","note"]
df = pd.DataFrame(R, columns=cols)
for c in ["pai_date","pao_date","end"]: df[c] = pd.to_datetime(df[c])

def load_raw(sym):
    if not sym: return None
    for p in (f"data/prices_raw/{sym}.csv", f"seed/data/prices/{sym}.csv", f"data/raw/deals_prices/{sym}.csv"):
        if os.path.exists(p):
            s = pd.read_csv(p); s.columns = [c.lower() for c in s.columns]
            if len(s) == 0: continue
            s["date"] = pd.to_datetime(s["date"]); s = s.dropna(subset=["close"]).sort_values("date")
            return s.drop_duplicates("date").set_index("date")["close"]
    return None
ADJ = pd.read_parquet("data/panel_close_adj_pricereturn.parquet")

def tday_after(s, d):
    i = s.index.searchsorted(d, side="right"); return s.index[i] if i < len(s) else None
def tday_on_before(s, d):
    i = s.index.searchsorted(d, side="right") - 1; return s.index[i] if i >= 0 else None
def tday_before(s, d):
    i = s.index.searchsorted(d, side="left") - 1; return s.index[i] if i >= 0 else None

ALL = sorted((pd.Timestamp(f.split("_")[-1][:-4]), f) for f in glob.glob("data/index_members/KMI_ALL_derived_*.csv"))
K30 = sorted((pd.Timestamp(f.split("_")[-1][:-4]), f) for f in glob.glob("data/index_members/KMI30_*.csv"))
def kmi_flag(sym, d):
    if not sym: return "n/a"
    s = [x for x in ALL if x[0] <= d]
    if not s: return "n/a (before Jan 2019)"
    a = set(pd.read_csv(s[-1][1])["symbol"])
    k = [x for x in K30 if x[0] <= d]
    k30 = set(pd.read_csv(k[-1][1])["symbol"]) if k else set()
    return "KMI30" if sym in k30 else ("KMI All Share" if sym in a else "not KMI")

NEW = ["pre_pai_close","entry_pai_date","entry_pai_close","entry_pao_date","entry_pao_close","exit_date","exit_close",
       "ret_pai_to_end","ret_pao_to_end","px_1m_after","px_6m_after","gap_flag"]
out = []
for r in df.itertuples():
    raw = load_raw(r.sym)
    adj = ADJ[r.sym].dropna() if r.sym in ADJ.columns else None
    o = r._asdict(); o.pop("Index")
    o.update({k: np.nan for k in NEW})
    if raw is not None:
        hh = int(r.pai_hhmm[:2]) + int(r.pai_hhmm[3:]) / 60 if isinstance(r.pai_hhmm, str) else None
        pre = tday_on_before(raw, r.pai_date) if (hh is not None and hh >= 15.5) else tday_before(raw, r.pai_date)
        if pre is not None and (r.pai_date - pre).days < 45: o["pre_pai_close"] = raw[pre]
        ent = tday_after(raw, r.pai_date)
        end = tday_on_before(raw, r.end) if pd.notna(r.end) else None
        if ent is not None and (ent - r.pai_date).days < 45:
            o["entry_pai_date"] = ent; o["entry_pai_close"] = raw[ent]
            if end is not None and end >= ent and (r.end - end).days < 45:
                o["exit_date"] = end; o["exit_close"] = raw[end]
                ser = adj if (adj is not None and ent in adj.index and end in adj.index) else raw
                o["ret_pai_to_end"] = ser[end] / ser[ent] - 1
                o["gap_flag"] = int((raw[ent:end].pct_change().abs() > 0.12).any())
                if r.status == "completed":
                    i = raw.index.get_loc(end)
                    if i + 21 < len(raw): o["px_1m_after"] = raw.iloc[i + 21]
                    if i + 126 < len(raw): o["px_6m_after"] = raw.iloc[i + 126]
        if pd.notna(r.pao_date):
            pent = tday_after(raw, r.pao_date)
            if pent is not None and (pent - r.pao_date).days < 45:
                o["entry_pao_date"] = pent; o["entry_pao_close"] = raw[pent]
                if end is not None and end >= pent and (r.end - end).days < 45:
                    ser = adj if (adj is not None and pent in adj.index and end in adj.index) else raw
                    o["ret_pao_to_end"] = ser[end] / ser[pent] - 1
    if r.type == "delisting" and pd.notna(o["entry_pai_close"]):
        o["exit_date"] = r.end; o["exit_close"] = r.offer   # holder tenders at the PSX-set buy-back price
        o["ret_pai_to_end"] = r.offer / o["entry_pai_close"] - 1
    o["premium_to_pre_pai"] = (r.offer / o["pre_pai_close"] - 1) if (pd.notna(r.offer) and pd.notna(o["pre_pai_close"])) else np.nan
    o["kmi_at_time"] = kmi_flag(r.sym, r.pai_date)
    o["days_pai_to_end"] = (r.end - r.pai_date).days if pd.notna(r.end) else np.nan
    out.append(o)
res = pd.DataFrame(out)
res["ret_offer_if_tendered_full"] = np.where((res.status == "completed") & res.offer.notna() & res.entry_pai_close.notna(),
                                             res.offer / res.entry_pai_close - 1, np.nan)
B = pd.read_csv("data/macro/kse100pr.csv", parse_dates=["date"]).set_index("date")["close"].sort_index()
def bret(a, b):
    if pd.isna(a) or pd.isna(b) or a < B.index[0]: return np.nan
    ia = B.index.searchsorted(a, side="right") - 1; ib = B.index.searchsorted(b, side="right") - 1
    return B.iloc[ib] / B.iloc[ia] - 1
res["bench_kse100pr_ret"] = [bret(a, b) for a, b in zip(res.entry_pai_date, res.exit_date)]
d = lambda c: pd.to_datetime(res[c]).dt.date
final = pd.DataFrame({
    "type": res.type, "target": res.target, "symbol": res.sym, "acquirer": res.acquirer,
    "pai_date": d("pai_date"), "offer_price": res.offer, "pre_pai_close": res.pre_pai_close,
    "premium_to_pre_pai": res.premium_to_pre_pai, "pao_date": d("pao_date"),
    "acceptance_pct": res.acc, "acceptance_note": res.acc_note,
    "completion_date": np.where(res.status.isin(["completed", "delisting_completed"]), res.end.dt.strftime("%Y-%m-%d"), ""),
    "end_date": d("end"), "status": res.status, "days_pai_to_end": res.days_pai_to_end,
    "price_1m_after_completion": res.px_1m_after, "price_6m_after": res.px_6m_after,
    "kmi_at_time": res.kmi_at_time,
    "entry_pai_date": d("entry_pai_date"), "entry_pai_close": res.entry_pai_close,
    "exit_date": d("exit_date"), "exit_close": res.exit_close,
    "ret_pai_entry_to_end": res.ret_pai_to_end, "ret_offer_if_tendered_full": res.ret_offer_if_tendered_full,
    "entry_pao_date": d("entry_pao_date"), "entry_pao_close": res.entry_pao_close,
    "ret_pao_entry_to_end": res.ret_pao_to_end, "bench_kse100pr_ret": res.bench_kse100pr_ret, "gap_flag": res.gap_flag,
    "source_urls": res.src, "notes": res.note,
}).sort_values(["pai_date", "target"])
final.to_csv("data/deals_history.csv", index=False, float_format="%.4f")
pd.set_option("display.width", 250)
print(final[["type","symbol","pai_date","status","pre_pai_close","entry_pai_close","exit_close","ret_pai_entry_to_end","ret_pao_entry_to_end","gap_flag"]].to_string())
