# Replay bundle, close of 2022-07-01

=== FILE: BRIEF ===
You are at the close of T. You get only `data/asof/<T>/` (market.md, sectors.csv, screens.csv, announcements_30d.csv, flows.csv, calendar.md; prices as traded at T) and `data/asof/<T>/method/`.

Forbidden:
- web access;
- any other repo file, or any earlier replay output;
- reasoning from anything after T.

If you remember what happened after T from your training, that memory is contamination. Do not use it, and report it in `contamination_note`. Every fact you state cites the pack. Every mechanism you rely on cites a method file. An uncited claim is a violation.

Risk budget [P]: for each entry, size_pct × (entry − stop) / entry ≤ 5 (percent of book); the sum over entries ≤ 10. Concentration up to all-in is allowed within that.

Return one JSON object and nothing else:

```json
{"date": "YYYY-MM-DD",
 "regime": {"rates_phase": "hiking|holding|cutting", "stance": "risk_on|neutral|risk_off",
            "p_kmi_up_60": 0.0, "summary": "<=80 words", "evidence": [CITE]},
 "core": [{"symbol": "", "weight_pct": 0, "thesis": "<=60 words", "evidence": [CITE]}],
 "watch": [{"type": "TYPE", "subject": "", "trigger": "", "evidence": [CITE]}],
 "entries": [{"symbol": "", "type": "TYPE", "entry_price": 0.0, "stop_price": 0.0,
              "stop_type": "fixed|trailing", "size_pct": 0, "horizon_sessions": 60,
              "p_gain": 0.0, "reason": "<=80 words", "evidence": [CITE]}],
 "exposure_pct": 0, "not_known": "<=60 words", "contamination_note": ""}
```

The fields:
- **CITE** is `{"file", "row", "field", "quote"}`. For CSVs, row is the symbol and field is the column. For .md files, row and field are null and quote is an exact substring.
- **TYPE** is one of policy_or_price_decision_pending, earnings_inflection_ignored, shock_and_rebound, deal_after_offer, buyback_or_sponsor_move, volume_with_upper_locks, other.
- **Counts:** core 0 to 3, watch 0 to 10, entries 0 to 3.
- **horizon_sessions** is 20, 60 or 120.
- **exposure_pct** is the core weights plus the entry sizes, from 0 to 100.
- **Symbols** must appear in screens.csv.
- **A trailing stop** keeps the distance (entry − stop) / entry, trailed on closes.
- **p_gain** is the probability that the net return is above 0 at horizon_sessions.

=== FILE: market.md ===
# Market as of 2022-07-01 close (public information only)

- KSE100: 41,630 on 2022-07-01; 1m -1.4%, 3m -6.3%, 6m -5.9%, 12m -11.4%
- KMI All Share: 20,874 on 2022-07-01; 1m +0.4%, 3m -5.3%, 6m -4.6%, 12m -9.3%
- Policy rate 13.75%; last MPC decision 2022-05-23: hike (+150bp)
- 6M T-bill cutoff 14.80% (auction 2022-06-29); 3M 15.23%, 12M 14.95%
- CPI YoY 13.78% for 2022-05 (published by 2022-06-03); three months earlier (2022-02) 12.24%
- Brent: 119.21 USD/bbl on 2022-07-01; 3-month change +12.3%
- USD/PKR: 204.62  on 2022-06-30; 3-month change +12.2%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +1.05pp (market pricing hikes); CPI rising over 3 months (+1.5pp)
- Next MPC: see SBP calendar

Session date used: 2022-07-01. Liquid KMI names: 50 (membership KMI_ALL_derived_2022-01-03.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.0027,0.2006,-0.0108,0,0
E&P,3,0.0211,-0.0525,-0.0465,0,0
OMC,4,0.0332,0.0256,-0.056,0,0
Power,5,0.0589,-0.0535,0.0006,0,0
Fertilizer,4,0.0135,-0.0294,0.111,0,0
Cement,16,-0.0284,-0.2384,-0.2852,0,0
Steel & engineering,11,0.0405,-0.096,-0.1813,0,0
Autos,12,-0.0057,-0.0308,-0.101,0,0
Tech & telecom,8,0.0428,-0.0552,-0.1233,0,0
Islamic banks & fin.,7,-0.0187,-0.0235,-0.0408,0,0
Pharma,12,0.093,-0.04,-0.08,0,1
Textiles,21,-0.0022,-0.0779,-0.0545,0,0
Food & staples,11,-0.0103,-0.1402,-0.2266,0,0
Chemicals,17,0.0035,0.0078,-0.0103,0,0
"Glass, packaging, paper",13,-0.0227,-0.0797,-0.1281,0,0
Gas utilities & misc,9,0.012,-0.0138,-0.0773,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AGHA,15.35,-0.019,-0.203,-0.43,-0.54,-0.551,1.365,0,,,0,0,0,0,,
ANL,10.8,0.012,-0.093,-0.181,-0.688,-0.686,0.691,0,,,0,0,0,0,,
ASL,11.12,-0.058,-0.197,-0.245,-0.548,-0.567,0.836,0,,,0,0,0,0,,
ATRL,168.42,0.026,0.339,0.152,-0.333,-0.349,1.157,0,2022-03-31,,2,0,0,0,,
AVN,77.34,0.028,0.102,0.044,0.049,-0.308,1.011,1,2022-03-31,,0,0,0,0,,
CHCC,91.08,-0.115,-0.355,-0.362,-0.497,-0.499,1.97,0,2022-03-31,,0,0,0,0,,
CNERGY,5.33,-0.013,0.002,-0.226,-0.532,-0.544,0.863,0,,,0,0,0,0,,
DGKC,61.16,0.028,-0.161,-0.244,-0.481,-0.492,1.759,0,2022-03-31,,0,1,0,0,,
EFERT,90.71,0.022,-0.004,0.195,0.288,-0.102,0.649,0,2022-03-31,,0,0,0,0,4.817,0.217
EPCL,79.11,-0.045,0.324,0.706,1.296,-0.112,0.54,0,2022-03-31,,0,0,0,0,3.33,0.301
FCCL,14.2,-0.043,-0.209,-0.219,-0.381,-0.39,0.708,0,2021-09-30,,0,0,0,0,,
FLYNG,7.17,0.001,-0.289,-0.389,-0.654,-0.676,0.946,0,,,0,0,0,0,,
GAL,59.17,0.0,-0.105,-0.246,-0.448,-0.587,1.229,1,,,0,0,0,0,,
GGGL,11.13,-0.04,-0.082,-0.228,-0.547,-0.627,0.564,0,,,0,0,0,0,,
GGL,16.55,-0.003,0.041,-0.314,-0.612,-0.617,0.581,0,2022-03-31,,0,1,0,0,,
GHNI,155.9,0.051,-0.043,-0.104,-0.429,-0.508,0.98,1,2022-03-31,,0,0,0,0,,
HCAR,187.24,0.054,-0.108,-0.191,-0.441,-0.518,1.25,0,2022-03-31,,1,0,0,0,,
HTL,39.85,0.026,-0.027,-0.074,-0.357,-0.447,0.836,0,,,0,0,0,0,,
HUBC,68.52,0.063,-0.041,0.039,-0.016,-0.107,0.94,0,2022-03-31,,0,0,0,0,,
ILP,60.6,-0.076,-0.176,-0.165,-0.115,-0.246,0.438,0,2022-03-31,,0,0,0,0,,
IMAGE,14.14,-0.008,-0.199,-0.202,-0.348,-0.535,0.241,0,2022-03-31,,0,0,0,0,,
INIL,102.13,0.044,-0.105,-0.275,-0.512,-0.529,0.593,0,2022-03-31,,0,0,0,0,,
ISL,58.75,0.004,-0.053,-0.12,-0.367,-0.414,0.554,0,2022-03-31,,0,1,0,0,,
KEL,2.91,0.106,-0.064,-0.149,-0.28,-0.304,1.367,0,2022-03-31,-1.778,0,1,0,0,9.635,
KOHC,128.89,-0.03,-0.245,-0.297,-0.376,-0.45,0.912,0,2022-03-31,,0,1,0,0,,
LUCK,452.69,0.002,-0.281,-0.335,-0.474,-0.503,1.758,0,2022-03-31,,0,1,0,0,,
MARI,1746.82,0.045,-0.005,0.068,0.157,-0.03,1.888,0,2022-03-31,,0,0,0,0,,
MEBL,114.94,-0.116,-0.114,-0.129,0.238,-0.233,0.962,0,2022-03-31,,0,0,0,0,7.73,0.042
MFFL,91.69,0.222,-0.436,-0.709,-0.753,-0.783,2.232,3,,,0,0,0,0,,
MLCF,26.98,0.046,-0.256,-0.21,-0.41,-0.432,1.016,0,,,0,0,0,0,,
MTL,877.28,-0.031,0.161,0.542,0.504,-0.037,1.156,0,2022-03-31,,0,0,0,0,,
MUGHAL,56.72,-0.054,-0.372,-0.441,-0.351,-0.497,1.074,0,2022-03-31,,0,0,0,0,,
NETSOL,100.01,0.096,0.183,0.06,-0.383,-0.435,0.774,1,2022-03-31,,0,1,0,0,,
NML,73.41,0.026,-0.102,-0.083,-0.226,-0.264,1.057,0,2022-03-31,,0,0,0,0,,
NRL,248.73,0.022,0.211,-0.112,-0.515,-0.526,1.06,0,2022-03-31,,0,0,0,0,,
OGDC,78.05,0.002,-0.066,-0.059,-0.133,-0.15,0.984,0,2022-03-31,,0,1,0,0,,
PAEL,15.87,-0.028,-0.025,-0.288,-0.553,-0.551,0.95,0,2022-03-31,,0,0,0,0,7.238,
PIBTL,6.01,-0.064,-0.049,-0.181,-0.48,-0.491,0.784,0,2022-03-31,,0,1,0,0,,
PIOC,59.17,-0.005,-0.242,-0.296,-0.534,-0.551,0.996,0,2022-03-31,,0,0,0,0,,
PPL,67.02,0.014,-0.092,-0.15,-0.238,-0.245,1.286,0,2022-03-31,,0,0,0,0,,
PSO,172.42,0.065,0.039,-0.057,-0.219,-0.255,1.468,0,2022-03-31,,1,0,0,0,,
SEARL,107.35,0.063,-0.09,-0.246,-0.419,-0.43,1.716,0,2022-03-31,,0,0,0,0,,
SNGP,35.47,0.261,0.138,0.057,-0.26,-0.369,1.969,0,2021-12-31,,0,1,0,0,2.805,0.144
SYS,328.49,-0.004,-0.074,-0.119,0.187,-0.204,1.107,0,2022-03-31,,1,0,0,0,23.513,0.007
TELE,10.8,-0.01,-0.113,-0.326,-0.264,-0.557,0.476,0,2021-06-30,,0,0,0,0,8.369,
TGL,103.55,0.022,-0.162,-0.031,0.131,-0.242,0.597,0,2022-03-31,,0,0,0,0,,
TREET,29.08,-0.005,-0.076,-0.293,-0.406,-0.528,0.503,0,2022-03-31,,0,2,0,0,,
UNITY,20.02,-0.084,-0.232,-0.236,-0.525,-0.562,1.521,0,2022-03-31,-0.395,0,3,0,0,13.56,
WAFI,119.27,0.061,0.037,-0.0,-0.311,-0.348,0.796,0,,,0,0,0,0,5.807,
WAVES,12.83,-0.042,-0.11,-0.193,-0.523,-0.529,0.645,0,2022-03-31,,1,1,0,0,13.769,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2022-06-02,OGDC,material_info,Material Information
2022-06-02,CLVL,material_info,Material Information
2022-06-02,STPL,insider_trade,Insider trade disclosure
2022-06-02,UNITY,insider_trade,Insider trade disclosure
2022-06-02,PTL,insider_trade,Insider trade disclosure
2022-06-02,MFFL,insider_trade,Insider trade disclosure
2022-06-02,PPL,other,Continuation of Production from the Sui Mining Lease
2022-06-02,MUGHAL,other,Credit of 5th Profit and 1st Principal Payment to Sukuk Certificate-1 Holde
2022-06-02,MTL,other,Increase in Authorized Capital
2022-06-02,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-03,TREET,material_info,Material Information
2022-06-03,CRTM,insider_trade,Insider trade disclosure
2022-06-03,STPL,insider_trade,Insider trade disclosure
2022-06-03,YOUW,insider_trade,Insider trade disclosure
2022-06-03,STPL,insider_trade,Insider trade disclosure
2022-06-03,SAPT,insider_trade,Insider trade disclosure
2022-06-03,NEXT,insider_trade,Insider trade disclosure
2022-06-03,MFFL,insider_trade,Insider trade disclosure
2022-06-03,LUCK,insider_trade,Insider trade disclosure
2022-06-03,LUCK,insider_trade,Insider trade disclosure
2022-06-03,MFFL,insider_trade,Insider trade disclosure
2022-06-03,IBFL,insider_trade,Insider trade disclosure
2022-06-03,MLCF,other,MLCFL-Report of buy back of shares 03.06.2022
2022-06-03,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-03,MTL,agm,Notice of Extraordinary General Meeting
2022-06-06,GEMUNSL,material_info,Material Information
2022-06-06,HMM,material_info,Material Information
2022-06-06,FRSM,material_info,Material Information
2022-06-06,UNITY,material_info,Material Information
2022-06-06,BIPLS,material_info,Material Information
2022-06-06,STPL,insider_trade,Insider trade disclosure
2022-06-06,GATM,insider_trade,Insider trade disclosure
2022-06-06,ASHT,insider_trade,Insider trade disclosure
2022-06-06,BECO,insider_trade,Insider trade disclosure
2022-06-06,MFFL,insider_trade,Insider trade disclosure
2022-06-06,GHNL,insider_trade,Insider trade disclosure
2022-06-06,ILP,credit_rating,Material Information - VIS Reaffirms Entity Ratings of Interloop Limited
2022-06-06,GHNI,other,Appointment of Director
2022-06-06,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-06,KOHC,agm,Notice of Extraordinary General Meeting
2022-06-07,MRNS,material_info,Material Information
2022-06-07,HCAR,financial_result,Transmission of Annual Report for the Year Ended 2022-03-31
2022-06-07,SPEL,insider_trade,Insider trade disclosure
2022-06-07,AVN,insider_trade,Insider trade disclosure
2022-06-07,IBFL,insider_trade,Insider trade disclosure
2022-06-07,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-07,MLCF,other,MLCFL-Report of buy back of shares 07.06.2022
2022-06-07,TREET,agm,Notice of Extra Ordinary general Meeting of Treet Corporation Limited REVOK
2022-06-07,TREET,agm,Notice of Extraordinary General Meeting of the Company
2022-06-07,HCAR,agm,Notice of Annual General Meeting
2022-06-08,UNITY,material_info,Material Information
2022-06-08,JSMFETF,material_info,Material Information - Resumption of iNAV JSMFETF
2022-06-08,GLAXO,material_info,Material Information
2022-06-08,HABSM,material_info,Material Information
2022-06-08,UNITY,insider_trade,Insider trade disclosure
2022-06-08,UNITY,insider_trade,Insider trade disclosure
2022-06-08,OCTOPUS,insider_trade,Insider trade disclosure
2022-06-08,PKGS,insider_trade,Insider trade disclosure
2022-06-08,ASHT,insider_trade,Insider trade disclosure
2022-06-08,TRG,insider_trade,Insider trade disclosure
2022-06-08,MUREB,insider_trade,Insider trade disclosure
2022-06-08,INIL,insider_trade,Insider trade disclosure
2022-06-08,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-09,AWWAL,material_info,Material Information
2022-06-09,COLG,insider_trade,Insider trade disclosure
2022-06-09,ENGRO,insider_trade,Insider trade disclosure
2022-06-09,STPL,insider_trade,Insider trade disclosure
2022-06-09,SPWL,insider_trade,Insider trade disclosure
2022-06-09,IGIHL,insider_trade,Insider trade disclosure
2022-06-09,IGIHL,insider_trade,Insider trade disclosure
2022-06-09,ASL,insider_trade,Insider trade disclosure
2022-06-09,BIFO,insider_trade,Insider trade disclosure
2022-06-09,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-10,EPQL,material_info,Material Information
2022-06-10,GTECH,material_info,MATERIAL INFORMATION
2022-06-10,GGL,material_info,Material Information - On behalf of Ghani Chemical Industries (one of the S
2022-06-10,BHAT,material_info,Material Information - Scheme of Arrangement
2022-06-10,LOTCHEM,material_info,Material Information
2022-06-10,SRVI,material_info,Material Information
2022-06-10,SYS,financial_result,Extracts of resolutions in the Board of Director Meeting for other than Fin
2022-06-10,CRTM,insider_trade,Insider trade disclosure
2022-06-10,OCTOPUS,insider_trade,Insider trade disclosure
2022-06-10,TPLI,insider_trade,Insider trade disclosure
2022-06-10,PTL,insider_trade,Insider trade disclosure
2022-06-10,PKGS,insider_trade,Insider trade disclosure
2022-06-10,PSEL,insider_trade,Insider trade disclosure
2022-06-10,INIL,insider_trade,Insider trade disclosure
2022-06-10,UBL,insider_trade,Insider trade disclosure
2022-06-10,SPWL,insider_trade,Insider trade disclosure
2022-06-10,IGIHL,insider_trade,Insider trade disclosure
2022-06-10,IGIHL,insider_trade,Insider trade disclosure
2022-06-10,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-10,SYS,agm,Notice of Extraordinary General Meeting
2022-06-10,WAVES,agm,Extension in time for holding the Annual General Meeting
2022-06-13,LUCK,material_info,MATERIAL INFORMATION
2022-06-13,ICI,material_info,Material Information
2022-06-13,ATRL,financial_result,ARL BOARD MEETING OTHER THAN FINANCIAL RESULTS
2022-06-13,PKGI,insider_trade,Insider trade disclosure
2022-06-13,DGKC,insider_trade,Insider trade disclosure
2022-06-13,CLVL,insider_trade,Insider trade disclosure
2022-06-13,ENGRO,insider_trade,Insider trade disclosure
2022-06-13,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-14,TPLT,material_info,Material Information
2022-06-14,TPLT,material_info,Material Information
2022-06-14,ENGRO,insider_trade,Insider trade disclosure
2022-06-14,MEBL,insider_trade,Insider trade disclosure
2022-06-14,THALL,insider_trade,Insider trade disclosure
2022-06-14,OBOY,insider_trade,Insider trade disclosure
2022-06-14,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-14,MLCF,other,MLCF-Report of buy back of shares 14.06.2022
2022-06-14,MARI,agm,Election of Directors
2022-06-15,AGP,material_info,Material Information Disclosure
2022-06-15,UNITY,insider_trade,Insider trade disclosure
2022-06-15,TRG,insider_trade,Insider trade disclosure
2022-06-15,HINOON,insider_trade,Insider trade disclosure
2022-06-15,IBFL,insider_trade,Insider trade disclosure
2022-06-15,DSIL,insider_trade,Insider trade disclosure
2022-06-15,MFFL,insider_trade,Insider trade disclosure
2022-06-15,OGDC,other,"GAS DISCOVERY AT UMAIR SOUTH EAST-1 WELL IN GUDDU BLOCK, SINDH, PROVINCE, P"
2022-06-15,MLCF,other,MLCF-Report of buy back of shares 15.06.2022
2022-06-16,UDPL,material_info,Material Information
2022-06-16,MODAM,material_info,MATERIAL INFORMATION REVOKED
2022-06-16,MODAM,material_info,MATERIAL INFORMATION REVOKED
2022-06-16,SBL,material_info,Material Information
2022-06-16,ENGRO,insider_trade,Insider trade disclosure
2022-06-16,OCTOPUS,insider_trade,Insider trade disclosure
2022-06-16,MFFL,insider_trade,Insider trade disclosure
2022-06-16,HINOON,insider_trade,Insider trade disclosure
2022-06-16,FRSM,insider_trade,Insider trade disclosure
2022-06-16,MLCF,other,MLCF-Report of buy back of shares 16.06.2022
2022-06-17,SNGP,material_info,DISCLOSURE OF MATERIAL INFORMATION
2022-06-17,UNITY,material_info,Material Information
2022-06-17,PSX,material_info,Disclosure of Material Information
2022-06-17,FATIMA,insider_trade,Insider trade disclosure
2022-06-17,HMM,insider_trade,Insider trade disclosure
2022-06-17,JVDC,insider_trade,Insider trade disclosure
2022-06-17,TGL,insider_trade,Insider trade disclosure
2022-06-17,ENGRO,insider_trade,Insider trade disclosure
2022-06-17,TRG,insider_trade,Insider trade disclosure
2022-06-17,MFFL,insider_trade,Insider trade disclosure
2022-06-17,ASHT,insider_trade,Insider trade disclosure
2022-06-17,UBL,insider_trade,Insider trade disclosure
2022-06-17,UBL,insider_trade,Insider trade disclosure
2022-06-17,UBL,insider_trade,Insider trade disclosure
2022-06-17,MARI,other,Corporate Briefing Session
2022-06-17,MLCF,other,MLCF-Report of buy back of shares 17.06.2022
2022-06-17,NETSOL,other,NETSOL | NetSol Technologies Limited - Purchase Repot of Buy Back of NetSol
2022-06-20,TRG,material_info,Material Information
2022-06-20,MODAM,material_info,Material Information
2022-06-20,PIBTL,material_info,Disclosure of Material Information of Pakistan International Bulk Terminal 
2022-06-20,ENGRO,insider_trade,Insider trade disclosure
2022-06-20,KOSM,insider_trade,Insider trade disclosure
2022-06-20,SPEL,insider_trade,Insider trade disclosure
2022-06-20,TRG,insider_trade,Insider trade disclosure
2022-06-20,IBFL,insider_trade,Insider trade disclosure
2022-06-20,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-20,MLCF,other,MLCF-Report of buy back of shares 20.06.2022
2022-06-20,UNITY,other,Miscellaneous Information
2022-06-21,DGKC,material_info,Material Information
2022-06-21,PSO,financial_result,Corporate Briefing Session on Business Results for the period ended March 3
2022-06-21,JVDC,insider_trade,Insider trade disclosure
2022-06-21,FATIMA,insider_trade,Insider trade disclosure
2022-06-21,NETSOL,other,Purchase (Buy Back) by NetSol Technologies Limited of its own shares pursua
2022-06-21,NETSOL,other,Public Announcement for Buy Back of Shares under regulation 10(g) of the Th
2022-06-21,KOHC,agm,List of Persons intended to contest Election of Directors to be held on 29-
2022-06-22,TPL,material_info,Disclosure of Material Information
2022-06-22,KSTM,material_info,Material Information REVOKED
2022-06-22,PAKL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2022-06-22,WAVES,financial_result,Emergent Board Meeting (Other Than Financial Results)
2022-06-22,ATRL,financial_result,ARL BOARD MEETING OTHER THAN FINANCIAL RESULTS
2022-06-22,GSKCH,insider_trade,Insider trade disclosure
2022-06-22,HMM,insider_trade,Insider trade disclosure
2022-06-22,SYS,insider_trade,Insider trade disclosure
2022-06-22,UBL,insider_trade,Insider trade disclosure
2022-06-22,SBL,insider_trade,Insider trade disclosure
2022-06-22,OGDC,other,OIL AND GAS DISCOVERY AT NIM EAST 1 EXPLORATORY WELL IN NIM BLOCK DISTRICT 
2022-06-22,OGDC,other,GAS DISCOVERY AT KALERI SHUM 01 IN KALCHAS BLOCK PUNJAB PROVINCE PAKISTAN
2022-06-22,WAVES,other,Scheme of Arrangement sanctioned by the High Court
2022-06-22,NETSOL,other,Newspapers Published copies of Public Announcement for Buy Back of Shares u
2022-06-22,NRL,other,Approval of Company's Budget for the year 2022-23
2022-06-22,MARI,agm,Certified true copy of resolution adopted at Extraordinary General Meeting 
2022-06-23,KSTM,material_info,Material Information
2022-06-23,ASTL,material_info,Material Information
2022-06-23,AVN,insider_trade,Insider trade disclosure
2022-06-23,UBL,insider_trade,Insider trade disclosure
2022-06-23,UBL,insider_trade,Insider trade disclosure
2022-06-23,INIL,insider_trade,Insider trade disclosure
2022-06-23,SKRS,insider_trade,Insider trade disclosure
2022-06-23,WAVES,other,Certified Copy of the Court Order (Waves & SMTM)
2022-06-24,KML,material_info,Material Information
2022-06-24,PSEL,material_info,Material Information
2022-06-24,KASBM,material_info,Material Information
2022-06-24,PAKMI,material_info,Material Information
2022-06-24,PMI,material_info,Material Information
2022-06-24,IBFL,insider_trade,Insider trade disclosure
2022-06-24,LUCK,insider_trade,Insider trade disclosure
2022-06-24,ASHT,insider_trade,Insider trade disclosure
2022-06-24,MLCF,other,MLCF Report of Buy-Back of Shares 24.06.2022
2022-06-27,TPLP,material_info,Disclosure of Material Information
2022-06-27,ISL,material_info,DISCLOSURE OF MATERIAL INFORMATION - COMMISSIONING OF REWINDING LINE
2022-06-27,ARM,material_info,Material Information
2022-06-27,SMTM,material_info,Material Information
2022-06-27,WAVES,material_info,Material Information
2022-06-27,UNITY,insider_trade,Insider trade disclosure
2022-06-27,TGL,insider_trade,Insider trade disclosure
2022-06-27,ENGRO,insider_trade,Insider trade disclosure
2022-06-27,TPL,insider_trade,Insider trade disclosure
2022-06-27,IBFL,insider_trade,Insider trade disclosure
2022-06-27,ISIL,insider_trade,Insider trade disclosure
2022-06-27,AGHA,insider_trade,Insider trade disclosure
2022-06-27,MTL,other,APPOINTMENT/CHANGE OF SHARE REGISTRAR / TRANSFER AGENT
2022-06-27,MARI,other,Discovery of Hvdrocarbons from Bannu West-l Well
2022-06-27,SNGP,other,CHANGE OF VENUE OF BOARD MEETING
2022-06-27,MLCF,other,MLCF-Report of Buy-Back of shares 27.06.2022
2022-06-28,TREET,material_info,Material information
2022-06-28,KEL,material_info,Material Information - Intimation for Extension in timeline for Public Anno
2022-06-28,SPEL,insider_trade,Insider trade disclosure
2022-06-28,CRTM,insider_trade,Insider trade disclosure
2022-06-28,MERIT,insider_trade,Insider trade disclosure
2022-06-28,STPL,insider_trade,Insider trade disclosure
2022-06-28,BNL,insider_trade,Insider trade disclosure
2022-06-28,BNL,insider_trade,Insider trade disclosure
2022-06-28,CHAS,insider_trade,Insider trade disclosure
2022-06-28,BNL,insider_trade,Insider trade disclosure
2022-06-28,BNL,insider_trade,Insider trade disclosure
2022-06-28,YOUW,insider_trade,Insider trade disclosure
2022-06-28,ARPAK,insider_trade,Insider trade disclosure
2022-06-28,PMRS,insider_trade,Insider trade disclosure
2022-06-28,FRSM,insider_trade,Insider trade disclosure
2022-06-28,JDWS,insider_trade,Insider trade disclosure
2022-06-28,AVN,insider_trade,Insider trade disclosure
2022-06-28,JDWS,insider_trade,Insider trade disclosure
2022-06-28,MLCF,other,MLCF- Report of Buy-Back of shares 28.06.2022
2022-06-28,TREET,agm,EXTRACTS OF RESOLUTION PASSED AT THE EXTRA ORDINARY GENERAL MEETING
2022-06-28,MTL,agm,Certified Copy of Special Resolution Passed in Extra Ordinary General Meeti
2022-06-29,SAPL,material_info,Material Information
2022-06-29,KOHC,material_info,Material Information
2022-06-29,NETSOL,material_info,Material Information
2022-06-29,AGHA,dividend_or_bonus,Book Closure Notice-Agha Steel Industries Limited-Sukuk Certificates-15th P
2022-06-29,MERIT,insider_trade,Insider trade disclosure
2022-06-29,EFUL,insider_trade,Insider trade disclosure
2022-06-29,FRSM,insider_trade,Insider trade disclosure
2022-06-29,CRTM,insider_trade,Insider trade disclosure
2022-06-29,UBL,insider_trade,Insider trade disclosure
2022-06-29,MLCF,other,MLCF- Report of Buy-Back of shares 29.06.2022
2022-06-30,GLAXO,material_info,Material Information - Resignation of Mark Dawson as Director w.e.f. 30 Jun
2022-06-30,POL,insider_trade,Insider trade disclosure
2022-06-30,EFUL,insider_trade,Insider trade disclosure
2022-06-30,TPL,insider_trade,Insider trade disclosure
2022-06-30,MODAM,insider_trade,Insider trade disclosure
2022-06-30,POL,insider_trade,Insider trade disclosure
2022-06-30,FCCL,other,FCCL | Fauji Cement Company Limited
2022-07-01,MEHT,material_info,Material Information
2022-07-01,ICI,material_info,Material Information
2022-07-01,SAZEW,material_info,Material Information
2022-07-01,PKGS,insider_trade,Insider trade disclosure
2022-07-01,OML,insider_trade,Insider trade disclosure
2022-07-01,MRNS,insider_trade,Insider trade disclosure
2022-07-01,INIL,insider_trade,Insider trade disclosure
2022-07-01,EFUL,insider_trade,Insider trade disclosure
2022-07-01,SURC,insider_trade,Insider trade disclosure
2022-07-01,EFERT,other,ASSUMPTION OF CHARGE AS NEW CHIEF EXECUTIVE OFFICER
2022-07-01,MUGHAL,other,Provisional Profit Payment and Musharakah Capital Repayment to Islamic Comm
2022-07-01,NETSOL,other,Final Report on The Purchase to be Submitted to the Commission and the Secu
2022-07-01,MARI,other,Nomination of Directors on MPCL Board
2022-07-01,SYS,agm,Extracts of resolutions adopted in the Extra Ordinary General Meeting

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,7.745,2022-06-30
investor_type,last_5_sessions,broker proprietary trading,3.47,2022-06-30
investor_type,last_5_sessions,companies,0.306,2022-06-30
investor_type,last_5_sessions,foreign corporates,0.995,2022-06-30
investor_type,last_5_sessions,foreign individual,0.018,2022-06-30
investor_type,last_5_sessions,individuals,4.589,2022-06-30
investor_type,last_5_sessions,insurance companies,-13.64,2022-06-30
investor_type,last_5_sessions,mutual funds,-6.539,2022-06-30
investor_type,last_5_sessions,nbfc,-0.28,2022-06-30
investor_type,last_5_sessions,other organization,0.973,2022-06-30
investor_type,last_5_sessions,overseas pakistani,2.361,2022-06-30
sector,last_5_sessions,fipi | All other Sectors,0.146,2022-06-30
sector,last_5_sessions,fipi | Cement,-0.143,2022-06-30
sector,last_5_sessions,fipi | Commercial Banks,0.15,2022-06-30
sector,last_5_sessions,fipi | Fertilizer,-0.137,2022-06-30
sector,last_5_sessions,fipi | Food and Personal Care Products,0.024,2022-06-30
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,0.48,2022-06-30
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,0.298,2022-06-30
sector,last_5_sessions,fipi | Power Generation and Distribution,-0.027,2022-06-30
sector,last_5_sessions,fipi | Technology and Communication,2.532,2022-06-30
sector,last_5_sessions,fipi | Textile Composite,0.051,2022-06-30
sector,last_5_sessions,lipi banks / dfi | All other Sectors,2.311,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Cement,7.916,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,-2.029,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Fertilizer,0.523,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,0.067,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.902,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-1.574,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.128,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,-0.816,2022-06-30
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.318,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,0.163,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.691,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.13,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.239,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.276,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.68,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,2.859,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.128,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,-0.805,2022-06-30
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.339,2022-06-30
sector,last_5_sessions,lipi companies | All other Sectors,-1.202,2022-06-30
sector,last_5_sessions,lipi companies | Cement,0.574,2022-06-30
sector,last_5_sessions,lipi companies | Commercial Banks,2.793,2022-06-30
sector,last_5_sessions,lipi companies | Fertilizer,0.025,2022-06-30
sector,last_5_sessions,lipi companies | Food and Personal Care Products,-1.137,2022-06-30
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,0.63,2022-06-30
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,-0.79,2022-06-30
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.266,2022-06-30
sector,last_5_sessions,lipi companies | Technology and Communication,-0.39,2022-06-30
sector,last_5_sessions,lipi companies | Textile Composite,0.068,2022-06-30
sector,last_5_sessions,lipi individuals | All other Sectors,1.315,2022-06-30
sector,last_5_sessions,lipi individuals | Cement,-1.122,2022-06-30
sector,last_5_sessions,lipi individuals | Commercial Banks,-0.592,2022-06-30
sector,last_5_sessions,lipi individuals | Fertilizer,0.688,2022-06-30
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,1.871,2022-06-30
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,0.538,2022-06-30
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.05,2022-06-30
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.318,2022-06-30
sector,last_5_sessions,lipi individuals | Technology and Communication,1.344,2022-06-30
sector,last_5_sessions,lipi individuals | Textile Composite,0.278,2022-06-30
sector,last_5_sessions,lipi insurance companies | All other Sectors,-1.373,2022-06-30
sector,last_5_sessions,lipi insurance companies | Cement,-5.901,2022-06-30
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-0.331,2022-06-30
sector,last_5_sessions,lipi insurance companies | Fertilizer,-0.543,2022-06-30
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,-0.537,2022-06-30
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-2.587,2022-06-30
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-1.135,2022-06-30
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,-0.023,2022-06-30
sector,last_5_sessions,lipi insurance companies | Technology and Communication,-1.135,2022-06-30
sector,last_5_sessions,lipi insurance companies | Textile Composite,-0.077,2022-06-30
sector,last_5_sessions,lipi mutual funds | All other Sectors,-1.546,2022-06-30
sector,last_5_sessions,lipi mutual funds | Cement,-1.961,2022-06-30
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-0.586,2022-06-30
sector,last_5_sessions,lipi mutual funds | Fertilizer,-0.874,2022-06-30
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,0.048,2022-06-30
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-0.929,2022-06-30
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.4,2022-06-30
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.283,2022-06-30
sector,last_5_sessions,lipi mutual funds | Technology and Communication,-0.523,2022-06-30
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.284,2022-06-30
sector,last_5_sessions,lipi nbfc | All other Sectors,-0.008,2022-06-30
sector,last_5_sessions,lipi nbfc | Cement,-0.006,2022-06-30
sector,last_5_sessions,lipi nbfc | Commercial Banks,-0.159,2022-06-30
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.091,2022-06-30
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.033,2022-06-30
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.0,2022-06-30
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,0.008,2022-06-30
sector,last_5_sessions,lipi nbfc | Technology and Communication,0.006,2022-06-30
sector,last_5_sessions,lipi nbfc | Textile Composite,0.003,2022-06-30
sector,last_5_sessions,lipi other organization | All other Sectors,0.195,2022-06-30
sector,last_5_sessions,lipi other organization | Cement,-0.05,2022-06-30
sector,last_5_sessions,lipi other organization | Commercial Banks,0.625,2022-06-30
sector,last_5_sessions,lipi other organization | Fertilizer,0.169,2022-06-30
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,-0.059,2022-06-30
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,0.319,2022-06-30
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.008,2022-06-30
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.017,2022-06-30
sector,last_5_sessions,lipi other organization | Technology and Communication,-0.214,2022-06-30
sector,last_5_sessions,lipi other organization | Textile Composite,-0.02,2022-06-30
investor_type,last_20_sessions,banks / dfi,10.166,2022-06-30
investor_type,last_20_sessions,broker proprietary trading,-3.639,2022-06-30
investor_type,last_20_sessions,companies,18.826,2022-06-30
investor_type,last_20_sessions,foreign corporates,-9.469,2022-06-30
investor_type,last_20_sessions,foreign individual,-0.129,2022-06-30
investor_type,last_20_sessions,individuals,17.853,2022-06-30
investor_type,last_20_sessions,insurance companies,-28.741,2022-06-30
investor_type,last_20_sessions,mutual funds,-8.845,2022-06-30
investor_type,last_20_sessions,nbfc,-1.553,2022-06-30
investor_type,last_20_sessions,other organization,4.413,2022-06-30
investor_type,last_20_sessions,overseas pakistani,1.118,2022-06-30
sector,last_20_sessions,fipi | All other Sectors,-4.595,2022-06-30
sector,last_20_sessions,fipi | Cement,-1.855,2022-06-30
sector,last_20_sessions,fipi | Commercial Banks,-5.418,2022-06-30
sector,last_20_sessions,fipi | Debt Market,-0.0,2022-06-30
sector,last_20_sessions,fipi | Fertilizer,-2.152,2022-06-30
sector,last_20_sessions,fipi | Food and Personal Care Products,0.369,2022-06-30
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,0.056,2022-06-30
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,0.627,2022-06-30
sector,last_20_sessions,fipi | Power Generation and Distribution,0.504,2022-06-30
sector,last_20_sessions,fipi | Technology and Communication,3.999,2022-06-30
sector,last_20_sessions,fipi | Textile Composite,-0.015,2022-06-30
sector,last_20_sessions,lipi banks / dfi | All other Sectors,4.024,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Cement,12.137,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-3.94,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-1.428,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,-0.726,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.442,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-1.618,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-0.619,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,0.121,2022-06-30
sector,last_20_sessions,lipi banks / dfi | Textile Composite,1.774,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-0.165,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Cement,0.809,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,0.624,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-1.176,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,2.189,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-1.159,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-3.538,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.141,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.039,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-0.779,2022-06-30
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.625,2022-06-30
sector,last_20_sessions,lipi companies | All other Sectors,5.628,2022-06-30
sector,last_20_sessions,lipi companies | Cement,2.159,2022-06-30
sector,last_20_sessions,lipi companies | Commercial Banks,6.607,2022-06-30
sector,last_20_sessions,lipi companies | Debt Market,-0.576,2022-06-30
sector,last_20_sessions,lipi companies | Fertilizer,0.7,2022-06-30
sector,last_20_sessions,lipi companies | Food and Personal Care Products,-0.997,2022-06-30
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,4.776,2022-06-30
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,1.985,2022-06-30
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-0.114,2022-06-30
sector,last_20_sessions,lipi companies | Technology and Communication,-1.207,2022-06-30
sector,last_20_sessions,lipi companies | Textile Composite,-0.135,2022-06-30
sector,last_20_sessions,lipi individuals | All other Sectors,1.301,2022-06-30
sector,last_20_sessions,lipi individuals | Cement,0.539,2022-06-30
sector,last_20_sessions,lipi individuals | Commercial Banks,3.609,2022-06-30
sector,last_20_sessions,lipi individuals | Fertilizer,2.169,2022-06-30
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,4.048,2022-06-30
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,2.915,2022-06-30
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.613,2022-06-30
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,1.05,2022-06-30
sector,last_20_sessions,lipi individuals | Technology and Communication,2.714,2022-06-30
sector,last_20_sessions,lipi individuals | Textile Composite,0.121,2022-06-30
sector,last_20_sessions,lipi insurance companies | All other Sectors,-3.075,2022-06-30
sector,last_20_sessions,lipi insurance companies | Cement,-10.214,2022-06-30
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-0.551,2022-06-30
sector,last_20_sessions,lipi insurance companies | Debt Market,-0.531,2022-06-30
sector,last_20_sessions,lipi insurance companies | Fertilizer,-1.632,2022-06-30
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,-0.704,2022-06-30
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-6.079,2022-06-30
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-2.523,2022-06-30
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,-0.525,2022-06-30
sector,last_20_sessions,lipi insurance companies | Technology and Communication,-2.708,2022-06-30
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.199,2022-06-30
sector,last_20_sessions,lipi mutual funds | All other Sectors,-3.441,2022-06-30
sector,last_20_sessions,lipi mutual funds | Cement,-3.822,2022-06-30
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-1.335,2022-06-30
sector,last_20_sessions,lipi mutual funds | Debt Market,0.569,2022-06-30
sector,last_20_sessions,lipi mutual funds | Fertilizer,-0.223,2022-06-30
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,0.584,2022-06-30
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,0.401,2022-06-30
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,1.517,2022-06-30
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-0.497,2022-06-30
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-1.758,2022-06-30
sector,last_20_sessions,lipi mutual funds | Textile Composite,-0.84,2022-06-30
sector,last_20_sessions,lipi nbfc | All other Sectors,-0.333,2022-06-30
sector,last_20_sessions,lipi nbfc | Cement,-0.009,2022-06-30
sector,last_20_sessions,lipi nbfc | Commercial Banks,-1.074,2022-06-30
sector,last_20_sessions,lipi nbfc | Fertilizer,-0.09,2022-06-30
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.001,2022-06-30
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.033,2022-06-30
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.0,2022-06-30
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.004,2022-06-30
sector,last_20_sessions,lipi nbfc | Technology and Communication,-0.006,2022-06-30
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.014,2022-06-30
sector,last_20_sessions,lipi other organization | All other Sectors,0.656,2022-06-30
sector,last_20_sessions,lipi other organization | Cement,0.256,2022-06-30
sector,last_20_sessions,lipi other organization | Commercial Banks,1.477,2022-06-30
sector,last_20_sessions,lipi other organization | Debt Market,1.714,2022-06-30
sector,last_20_sessions,lipi other organization | Fertilizer,0.467,2022-06-30
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-1.416,2022-06-30
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,1.059,2022-06-30
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,0.486,2022-06-30
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,0.157,2022-06-30
sector,last_20_sessions,lipi other organization | Technology and Communication,-0.376,2022-06-30
sector,last_20_sessions,lipi other organization | Textile Composite,-0.067,2022-06-30

=== FILE: calendar.md ===
# Calendar as of 2022-07-01

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2022-06-03 INIL: BOARD MEETING OTHER THAN FINANCIAL RESULTS
- 2022-06-03 INIL: Board Meeting Other Than Financial Results
- 2022-06-03 MFFL: Notice of Board Meeting
- 2022-06-06 LUCK: Board Meeting Other Than Financial Results
- 2022-06-07 SYS: Board Meeting Other Than Financial Results
- 2022-06-10 NRL: Board Meeting Other Than Financial Results
- 2022-06-13 MFFL: Board Meeting-Business Plan/Annual Budget 2022-2023
- 2022-06-13 CHCC: Board Meeting Other Than Financial Results
- 2022-06-13 ISL: BOARD MEETING OTHER THAN FINANCIAL RESULTS
- 2022-06-14 MARI: Notice of Board of Directors Meeting
- 2022-06-14 UNITY: Board Meeting Other than Financial Results
- 2022-06-15 INIL: BOARD MEETING - OTHER THAN FINANCIAL RESULTS
- 2022-06-16 CNERGY: Board Meeting Other Than Financial Results
- 2022-06-20 CHCC: Board Meeting Other Than Financial Results
- 2022-06-21 MARI: Notice of Postponement of the Board of Directors Meeting
- 2022-06-21 TREET: Board Meeting of Treet Corporation Limited
- 2022-06-21 ILP: Notice of Board Meeting Other Than Financial Results / Closed Period
- 2022-06-22 GHNI: Board Meeting Other than Financial Results
- 2022-06-23 FCCL: Board Meeting Other Than Financial Results
- 2022-06-24 ISL: BOARD MEETING - OTHER THAN FINANCIAL RESULTS
- 2022-06-24 SNGP: Board Meeting
- 2022-06-24 SNGP: Board Meeting
- 2022-06-24 CNERGY: Board Meeting other than Financial Results
- 2022-06-27 SEARL: Board Meeting Other Than Financial Results
- 2022-06-29 GHNI: Board Meeting Other Than Financial Results
- 2022-06-29 ILP: Board Meeting-Approval of Annual Budget FY 2022-23 amidst Other Items
- 2022-06-30 KOHC: Board Meeting Other Than Financial Results
- 2022-07-01 MARI: Emergent Board of Directors Meeting

=== FILE: questions.md ===

## A. Regime questions (what is the tide doing)
A1. Where is the policy rate against inflation, and which way is it likelier to move?
A2. Is the curve pricing a move the SBP has not made?
A3. Is inflation turning, and is this a run or a blip?
A4. IMF status: staff agreement, board approval or cash release, and which conditions bite?
A5. Balance of payments: reserves, current account, import cover, rupee direction?
A6. Is the market cheap or rerated against its own post-crisis range?
A7. Political stability as business reads it: is the government stable, buyable and pro-business?
A8. Oil: where is Brent, and which link do I actually hold?
A9. Is the market used to this noise? What did price do on the headline day, and what did the largest holders do?
A10. Which past regime does this resemble, and what did the method do there?
A11. If a shock, how far and how fast did past shocks fall, and who led the rebound?

## B. Business questions (the core)
B1. What is five-year earnings power on consolidated EPS, one-offs stripped?
B2. What are the sector real levers, and where do they stand?
B3. What does the business earn on new capital, and how much does it reinvest?
B4. Is the business trying to become big, with a builder culture?
B5. Who runs it, and did past promises meet delivery and past bets pay?
B6. How does the sponsor treat minorities?
B7. Can the balance sheet survive higher rates and a bad year?
B8. Is the cash real?
B9. Float and exit: can I leave at my size, and who holds the free float?
B10. Is it in KMI All Share, and near the debt threshold?
B11. What is priced in: P/E relative to market and own history, P/B against ROE for banks, and what must go right?
B12. Can I explain it in two minutes, and do I know it better than the price does?
B13. Is it growing, not merely stable?

## C. Situation questions (opportunity sleeve)
C1. What type is this: policy decision, ignored earnings inflection, shock and rebound, deal, sponsor or buyback move, volume ignition, or none?
C2. What is the measured base rate for this type, and how many independent episodes stand behind it?
C3. Who gains, who decides, and when?
C4. Is price confirming or extended?
C5. Am I picking a winner from start-of-move features?
C6. If a takeover: what fraction of my holding does the offer buy, and what is the stub worth?
C7. Is volume with upper locks demand or an operator?
C8. Is the sponsor or an insider buying, filed and public?
C9. What is the exit: stop, target, time, and the loss in rupees if wrong?
C10. What is the trap: one episode counted as many, a one-off, a corporate-action gap, lookahead in my sample?
C11. Is capital stuck in a position I would not buy today?

## D. Self-check questions
D1. What would an expert find obvious that I skipped?
D2. What does my data not contain?
D3. Am I intellectualizing a long causal chain? How strong is each link?
D4. Does the metric fit the goal and horizon?
D5. Did I use a placebo, the total-return index and a reference class, and separate deposits from skill?
D6. Did the market surprise me, and have I written why?
D7. Did I start work before the question was clear?

=== FILE: actors.md ===
| 10 | K-Electric to Shanghai Electric | PAI 27 Mar 2018 | outcome not shown |
| 11 | OGDC 7%, PPL 10% sale | CCoP 21 Aug 2020 | outcome not shown |
| 12 | Six SOEs sold in FY20 | 29 Jan 2020 | outcome not shown |
| 17 | GIDC recovery | SC Aug 2020 | outcome not shown |

=== FILE: situations.md ===
(no situation-library entry has an outcome that closed before this date, or the library has no INDEX.md)

=== FILE: base_rates.csv ===
type,as_of_cutoff,n,hit_rate,median,p50plus,source
none,,,,,,no base rates available
=== END ===
