# Replay bundle, close of 2020-02-21

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
# Market as of 2020-02-21 close (public information only)

- KSE100: 40,249 on 2020-02-21; 1m -5.4%, 3m +6.1%, 6m +28.4%, 12m -0.6%
- KMI All Share: 18,513 on 2020-02-21; 1m -6.9%, 3m +3.4%, 6m +25.7%, 12m -6.2%
- Policy rate 13.25%; last MPC decision 2020-01-28: hold (+0bp)
- 6M T-bill cutoff 13.30% (auction 2020-02-12); 3M 13.41%, 12M 13.52%
- CPI YoY 14.89% for 2020-01 (published by 2020-02-03); three months earlier (2019-10) 12.22%
- Brent: 58.60 USD/bbl on 2020-02-21; 3-month change -9.8%
- USD/PKR: 154.18  on 2020-02-21; 3-month change -0.7%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.05pp (market near policy rate); CPI rising over 3 months (+2.7pp)
- Next MPC: see SBP calendar

Session date used: 2020-02-21. Liquid KMI names: 55 (membership KMI_ALL_derived_2020-01-13.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.1303,-0.0114,0.3102,0,0
E&P,3,-0.1164,0.0153,0.2619,0,0
OMC,4,-0.1142,0.0091,0.3785,0,0
Power,4,-0.0802,-0.0445,0.166,0,0
Fertilizer,4,-0.0434,-0.0155,0.1243,0,1
Cement,16,-0.0535,-0.0089,0.2621,0,1
Steel & engineering,10,-0.065,-0.0939,0.2765,0,0
Autos,12,-0.103,0.0057,0.372,0,0
Tech & telecom,6,-0.0651,0.0274,0.2773,0,0
Islamic banks & fin.,7,-0.0592,0.0847,0.1545,0,0
Pharma,11,-0.0371,0.1112,0.678,0,0
Textiles,18,0.0122,0.1292,0.2328,0,0
Food & staples,11,-0.091,0.0701,0.2627,0,0
Chemicals,17,-0.0362,0.063,0.2161,0,0
"Glass, packaging, paper",12,-0.0649,-0.005,0.3561,0,0
Gas utilities & misc,9,-0.0916,-0.0759,0.1551,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,n_results,n_material,n_insider_buy,n_insider_sell
ACPL,101.65,-0.018,0.059,0.263,-0.105,,0.47,0,0,0,0,0
AGP,101.64,-0.051,0.217,0.746,0.156,-0.065,0.432,0,0,0,0,0
ASC,13.23,0.007,0.016,0.185,-0.371,-0.401,1.149,0,0,0,0,0
ASTL,33.51,-0.05,-0.139,0.724,-0.384,-0.377,0.206,0,0,0,0,0
ATRL,96.5,-0.162,-0.076,0.242,-0.232,-0.296,0.582,0,1,0,0,0
BIPL,13.12,-0.015,0.194,0.015,0.161,-0.125,0.958,0,0,0,0,0
CHCC,54.45,0.034,0.138,1.147,-0.189,-0.195,1.383,0,1,0,0,0
DCL,7.8,-0.13,-0.052,0.145,-0.427,-0.426,0.634,0,0,0,0,0
DGKC,68.54,-0.105,-0.027,0.262,-0.288,-0.298,1.411,0,1,0,0,0
EFERT,65.51,-0.046,-0.071,-0.012,-0.13,-0.166,0.917,0,1,0,0,0
ENGROH,150.1,-0.089,0.012,0.328,0.251,-0.145,0.369,0,0,0,0,0
EPCL,31.73,-0.04,0.041,0.37,-0.154,-0.157,0.54,0,2,1,0,0
FCCL,15.33,-0.072,-0.035,-0.004,-0.319,-0.323,0.56,0,1,0,0,0
FCEPL,68.54,-0.093,0.001,0.401,-0.196,-0.205,0.351,0,1,0,0,0
FEROZ,196.15,-0.133,-0.004,0.946,0.003,-0.149,0.384,0,0,0,0,0
GAL,61.49,-0.116,-0.028,0.36,-0.359,-0.356,0.478,0,0,0,0,0
GGL,15.38,-0.142,0.354,0.92,0.226,-0.171,0.465,0,0,0,0,0
GHNI,113.38,-0.074,0.189,0.606,-0.44,-0.478,0.65,0,1,0,0,0
GLAXO,168.66,0.048,0.089,0.79,0.157,-0.102,0.815,0,0,2,0,0
HCAR,199.61,-0.056,0.139,0.334,-0.144,-0.266,0.745,0,2,0,0,0
HTL,30.35,-0.089,-0.021,0.463,-0.445,-0.453,0.577,0,0,0,0,0
HUBC,98.3,-0.034,0.107,0.439,0.053,-0.048,0.583,0,0,1,0,0
ILP,56.57,-0.021,0.11,0.384,,-0.071,0.43,0,1,0,0,0
INIL,99.83,-0.089,0.06,0.199,-0.339,-0.321,0.497,0,2,0,0,0
ISL,49.03,-0.11,-0.078,0.232,-0.307,-0.305,0.714,0,1,0,0,0
KEL,4.07,-0.058,-0.007,0.143,-0.375,-0.377,0.349,0,0,0,0,0
KOHC,91.26,0.15,0.137,0.9,0.037,-0.024,0.854,0,0,1,0,0
KTML,41.4,-0.022,0.197,0.656,-0.044,-0.079,1.036,0,0,0,0,0
LCI,704.36,0.038,0.312,0.517,-0.034,-0.034,1.015,0,0,0,0,0
LOTCHEM,13.62,-0.056,-0.075,-0.164,-0.182,-0.207,0.629,0,1,0,0,0
LUCK,489.99,-0.012,0.225,0.333,0.005,-0.017,0.625,0,2,0,0,0
MARI,1253.5,-0.138,0.008,0.397,-0.035,-0.138,0.32,0,1,0,0,0
MEBL,99.15,-0.064,0.191,0.275,0.161,-0.066,0.732,0,1,0,0,0
MLCF,23.67,0.064,0.224,0.185,-0.499,-0.501,1.165,0,0,0,0,0
MTL,691.81,-0.05,0.001,0.24,-0.027,-0.081,0.275,0,1,0,0,0
MUGHAL,40.03,-0.08,-0.054,0.589,-0.085,-0.139,0.246,0,0,0,0,0
NETSOL,58.25,-0.15,-0.125,0.015,-0.31,-0.327,0.91,0,1,0,0,0
NML,105.14,-0.065,0.034,0.376,-0.265,-0.261,0.472,0,1,0,0,0
NRL,118.13,-0.178,-0.035,0.155,-0.472,-0.451,0.65,0,1,0,0,0
OGDC,131.39,-0.087,-0.017,0.074,-0.125,-0.148,0.623,0,0,0,0,0
PAEL,24.62,-0.085,0.048,0.433,-0.071,-0.165,0.369,0,0,0,0,0
PKGS,382.5,-0.011,0.111,0.355,-0.015,-0.146,0.777,0,0,0,0,0
POWER,6.35,-0.056,0.076,0.134,-0.227,-0.232,0.467,0,0,0,0,0
PPL,128.45,-0.125,0.044,0.309,-0.174,-0.183,0.563,0,0,0,0,0
PSO,181.97,-0.148,-0.006,0.548,-0.043,-0.161,0.679,0,1,0,0,0
PTC,8.93,-0.068,0.007,0.227,-0.112,-0.136,0.468,0,1,0,0,0
SEARL,172.25,-0.093,-0.059,0.152,-0.358,-0.36,0.404,0,0,0,0,0
SNGP,73.1,-0.075,-0.04,0.227,-0.002,-0.122,0.323,0,1,0,0,0
SSGC,17.89,-0.132,-0.084,0.022,-0.271,-0.277,0.475,0,0,0,0,0
STPL,9.55,-0.049,-0.35,-0.064,-0.568,-0.57,0.445,0,0,0,0,0
SYS,148.83,0.191,0.597,0.757,0.662,-0.052,1.712,0,0,2,0,0
TGL,113.0,-0.017,0.492,0.626,0.097,-0.047,0.451,0,0,0,0,0
TREET,19.66,-0.127,0.008,0.348,-0.22,-0.217,0.503,0,0,0,0,0
UNITY,14.27,-0.016,0.287,0.53,-0.194,-0.209,0.883,0,0,0,0,0
WAFI,189.62,-0.14,0.043,0.296,-0.368,-0.377,0.413,0,0,0,0,0

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2020-01-24,SLCL,material_info,Material Information
2020-01-24,GHGL,material_info,Disclosure of Material Information under Regulation 5.6.1(d) of PSX Rule Bo
2020-01-24,PIAA,material_info,MATERIAL INFORMATION
2020-01-27,KOHC,material_info,Material Information
2020-01-27,AVN,material_info,Material Information
2020-01-28,PASM,material_info,Material Information
2020-01-28,IMSL,material_info,Material Information
2020-01-30,SYS,material_info,Material Information
2020-01-30,SILK,material_info,Material Information
2020-01-31,HUBC,material_info,Material Information
2020-01-31,SYS,material_info,Material Information
2020-01-31,FFC,material_info,Disclosure of Material Information by Fauji Fertilizer Company Limited
2020-02-03,SRVI,material_info,Material Information
2020-02-03,KOHTM,material_info,Material Information
2020-02-03,PMI,material_info,Material Information
2020-02-03,PAKMI,material_info,Material Information
2020-02-03,MFFL,material_info,Material Information
2020-02-04,EPCL,financial_result,"FINANCIAL RESULTS FOR THE YEAR ENDED DECEMBER 31, 2019"
2020-02-06,AVN,material_info,Material Information
2020-02-06,LUCK,financial_result,"Transmission of Quarterly Report for the period ended December 31, 2019"
2020-02-07,FCEPL,financial_result,Financial Results for the Year Ended 2019
2020-02-11,SMTM,material_info,Material Information
2020-02-11,PTC,financial_result,"Financial results for the year ended December 31, 2019"
2020-02-12,MEBL,financial_result,"FINANCIAL RESULTS FOR THE YEAR ENDED DECEMBER 31, 2019"
2020-02-12,CHCC,financial_result,"Financial Results for the Quarter Ended December 31, 2019"
2020-02-12,ATRL,financial_result,Transmission of Quarterly Report for the Period Ended 2019-12-31
2020-02-13,JSCL,material_info,Material Information
2020-02-13,AKBL,material_info,Material Information
2020-02-13,DGKC,financial_result,"Financial Results for the Half Year ended December 31, 2019(Un-Audited)"
2020-02-14,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-02-14,EXIDE,material_info,Material Information
2020-02-14,LOTCHEM,financial_result,Financial Results For the Year Ended 31 December 2019
2020-02-14,NML,financial_result,"FINANCIAL RESULTS FOR THE HALF YEAR ENDED DECEMBER 31,2019"
2020-02-14,ILP,financial_result,"Financial Results for the Half Year Ended December 31, 2019"
2020-02-14,SNGP,financial_result,Application for Extension in the Period for Submission of Half Yearly Accou
2020-02-17,FML,material_info,Disclosure of Material Information
2020-02-17,JVDC,material_info,Material Information
2020-02-17,HBL,material_info,"Material Information Habib Bank Limited, New York Branch"
2020-02-17,PAKOXY,material_info,MATERIAL INFORMATION
2020-02-17,EFERT,financial_result,"FINANCIAL RESULTS FOR THE YEAR ENDED DECEMBER 31, 2019"
2020-02-18,PSO,financial_result,"Financial Results for the Half Year ended December 31, 2019"
2020-02-19,AVN,material_info,Material Information
2020-02-19,INDU,material_info,Material Information - Change of Director
2020-02-19,GSPM,material_info,Material Information
2020-02-19,MTL,financial_result,"Financial Results for the 2nd Quarter Ended December 31, 2019"
2020-02-19,GHNI,financial_result,"Financial Results for the Half Year ended December 31, 2019"
2020-02-20,GLAXO,material_info,Material Information - GSK Pakistan Limited REVOKED
2020-02-20,GLAXO,material_info,Material Information - GlaxoSmithKline Pakistan Limited
2020-02-21,JSGCL,material_info,Material Information
2020-02-21,INIL,financial_result,FINANCIAL RESULTS FOR THE HALF YEAR ENDED 31-12-2019
2020-02-21,FCCL,financial_result,Financial Results for the Half Year Ended 31st December 2019
2020-02-21,NETSOL,financial_result,Transmission of Quarterly Report for the Period Ended 2019-12-31

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,0.453,2020-02-20
investor_type,last_5_sessions,broker proprietary trading,-0.302,2020-02-20
investor_type,last_5_sessions,companies,4.57,2020-02-20
investor_type,last_5_sessions,foreign corporates,-8.909,2020-02-20
investor_type,last_5_sessions,foreign individual,-0.014,2020-02-20
investor_type,last_5_sessions,individuals,-2.168,2020-02-20
investor_type,last_5_sessions,insurance companies,7.344,2020-02-20
investor_type,last_5_sessions,mutual funds,-2.389,2020-02-20
investor_type,last_5_sessions,nbfc,-0.577,2020-02-20
investor_type,last_5_sessions,other organization,2.974,2020-02-20
investor_type,last_5_sessions,overseas pakistani,-0.982,2020-02-20
sector,last_5_sessions,fipi | All other Sectors,-0.644,2020-02-20
sector,last_5_sessions,fipi | Cement,-3.764,2020-02-20
sector,last_5_sessions,fipi | Commercial Banks,-1.266,2020-02-20
sector,last_5_sessions,fipi | Fertilizer,-0.76,2020-02-20
sector,last_5_sessions,fipi | Food and Personal Care Products,-0.018,2020-02-20
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-3.503,2020-02-20
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,0.108,2020-02-20
sector,last_5_sessions,fipi | Power Generation and Distribution,-0.114,2020-02-20
sector,last_5_sessions,fipi | Technology and Communication,0.726,2020-02-20
sector,last_5_sessions,fipi | Textile Composite,-0.671,2020-02-20
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-1.255,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Cement,0.299,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,0.136,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-0.286,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-0.08,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.29,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.625,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.005,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,0.303,2020-02-20
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.417,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,0.334,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.21,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,-1.039,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.036,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.019,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.504,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.064,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.152,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,0.128,2020-02-20
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.239,2020-02-20
sector,last_5_sessions,lipi companies | All other Sectors,0.632,2020-02-20
sector,last_5_sessions,lipi companies | Cement,0.785,2020-02-20
sector,last_5_sessions,lipi companies | Commercial Banks,1.151,2020-02-20
sector,last_5_sessions,lipi companies | Fertilizer,0.356,2020-02-20
sector,last_5_sessions,lipi companies | Food and Personal Care Products,0.032,2020-02-20
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,1.446,2020-02-20
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,-0.638,2020-02-20
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.187,2020-02-20
sector,last_5_sessions,lipi companies | Technology and Communication,0.578,2020-02-20
sector,last_5_sessions,lipi companies | Textile Composite,0.416,2020-02-20
sector,last_5_sessions,lipi individuals | All other Sectors,-1.836,2020-02-20
sector,last_5_sessions,lipi individuals | Cement,0.622,2020-02-20
sector,last_5_sessions,lipi individuals | Commercial Banks,-0.689,2020-02-20
sector,last_5_sessions,lipi individuals | Fertilizer,0.099,2020-02-20
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,0.1,2020-02-20
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,0.82,2020-02-20
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,0.656,2020-02-20
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.309,2020-02-20
sector,last_5_sessions,lipi individuals | Technology and Communication,-1.646,2020-02-20
sector,last_5_sessions,lipi individuals | Textile Composite,-0.602,2020-02-20
sector,last_5_sessions,lipi insurance companies | All other Sectors,0.116,2020-02-20
sector,last_5_sessions,lipi insurance companies | Cement,0.955,2020-02-20
sector,last_5_sessions,lipi insurance companies | Commercial Banks,3.44,2020-02-20
sector,last_5_sessions,lipi insurance companies | Fertilizer,0.704,2020-02-20
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.036,2020-02-20
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,1.054,2020-02-20
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.361,2020-02-20
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,0.479,2020-02-20
sector,last_5_sessions,lipi insurance companies | Technology and Communication,-0.065,2020-02-20
sector,last_5_sessions,lipi insurance companies | Textile Composite,0.264,2020-02-20
sector,last_5_sessions,lipi mutual funds | All other Sectors,-0.31,2020-02-20
sector,last_5_sessions,lipi mutual funds | Cement,0.731,2020-02-20
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-0.848,2020-02-20
sector,last_5_sessions,lipi mutual funds | Fertilizer,-0.005,2020-02-20
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,-0.051,2020-02-20
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-0.863,2020-02-20
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.624,2020-02-20
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.353,2020-02-20
sector,last_5_sessions,lipi mutual funds | Technology and Communication,-0.04,2020-02-20
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.027,2020-02-20
sector,last_5_sessions,lipi nbfc | All other Sectors,0.405,2020-02-20
sector,last_5_sessions,lipi nbfc | Cement,0.002,2020-02-20
sector,last_5_sessions,lipi nbfc | Commercial Banks,-0.602,2020-02-20
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.008,2020-02-20
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,-0.0,2020-02-20
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.001,2020-02-20
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.37,2020-02-20
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.0,2020-02-20
sector,last_5_sessions,lipi nbfc | Technology and Communication,-0.001,2020-02-20
sector,last_5_sessions,lipi nbfc | Textile Composite,-0.002,2020-02-20
sector,last_5_sessions,lipi other organization | All other Sectors,2.559,2020-02-20
sector,last_5_sessions,lipi other organization | Cement,0.16,2020-02-20
sector,last_5_sessions,lipi other organization | Commercial Banks,-0.283,2020-02-20
sector,last_5_sessions,lipi other organization | Fertilizer,-0.137,2020-02-20
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,0.001,2020-02-20
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,0.252,2020-02-20
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.052,2020-02-20
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.013,2020-02-20
sector,last_5_sessions,lipi other organization | Technology and Communication,0.017,2020-02-20
sector,last_5_sessions,lipi other organization | Textile Composite,0.445,2020-02-20
investor_type,last_20_sessions,banks / dfi,1.403,2020-02-20
investor_type,last_20_sessions,broker proprietary trading,1.549,2020-02-20
investor_type,last_20_sessions,companies,3.821,2020-02-20
investor_type,last_20_sessions,foreign corporates,-33.511,2020-02-20
investor_type,last_20_sessions,foreign individual,-0.143,2020-02-20
investor_type,last_20_sessions,individuals,-1.32,2020-02-20
investor_type,last_20_sessions,insurance companies,28.951,2020-02-20
investor_type,last_20_sessions,mutual funds,-10.949,2020-02-20
investor_type,last_20_sessions,nbfc,-0.216,2020-02-20
investor_type,last_20_sessions,other organization,10.324,2020-02-20
investor_type,last_20_sessions,overseas pakistani,0.092,2020-02-20
sector,last_20_sessions,fipi | All other Sectors,-6.863,2020-02-20
sector,last_20_sessions,fipi | Cement,-18.314,2020-02-20
sector,last_20_sessions,fipi | Commercial Banks,-7.009,2020-02-20
sector,last_20_sessions,fipi | Fertilizer,5.782,2020-02-20
sector,last_20_sessions,fipi | Food and Personal Care Products,0.299,2020-02-20
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-11.685,2020-02-20
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,6.949,2020-02-20
sector,last_20_sessions,fipi | Power Generation and Distribution,-0.493,2020-02-20
sector,last_20_sessions,fipi | Technology and Communication,2.224,2020-02-20
sector,last_20_sessions,fipi | Textile Composite,-4.453,2020-02-20
sector,last_20_sessions,lipi banks / dfi | All other Sectors,-0.01,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Cement,0.513,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-0.349,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-3.829,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.099,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.763,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,1.97,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-0.373,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,1.416,2020-02-20
sector,last_20_sessions,lipi banks / dfi | Textile Composite,1.203,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,1.358,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Cement,1.454,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,-1.891,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-0.05,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.088,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.816,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.23,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.126,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,0.502,2020-02-20
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.195,2020-02-20
sector,last_20_sessions,lipi companies | All other Sectors,-0.262,2020-02-20
sector,last_20_sessions,lipi companies | Cement,-0.234,2020-02-20
sector,last_20_sessions,lipi companies | Commercial Banks,1.317,2020-02-20
sector,last_20_sessions,lipi companies | Fertilizer,-2.608,2020-02-20
sector,last_20_sessions,lipi companies | Food and Personal Care Products,-1.014,2020-02-20
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,2.126,2020-02-20
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,-1.774,2020-02-20
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-1.044,2020-02-20
sector,last_20_sessions,lipi companies | Technology and Communication,0.167,2020-02-20
sector,last_20_sessions,lipi companies | Textile Composite,7.148,2020-02-20
sector,last_20_sessions,lipi individuals | All other Sectors,-5.651,2020-02-20
sector,last_20_sessions,lipi individuals | Cement,1.648,2020-02-20
sector,last_20_sessions,lipi individuals | Commercial Banks,5.347,2020-02-20
sector,last_20_sessions,lipi individuals | Fertilizer,1.571,2020-02-20
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,0.746,2020-02-20
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,8.677,2020-02-20
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,-7.108,2020-02-20
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,0.582,2020-02-20
sector,last_20_sessions,lipi individuals | Technology and Communication,-3.088,2020-02-20
sector,last_20_sessions,lipi individuals | Textile Composite,-4.045,2020-02-20
sector,last_20_sessions,lipi insurance companies | All other Sectors,0.632,2020-02-20
sector,last_20_sessions,lipi insurance companies | Cement,9.558,2020-02-20
sector,last_20_sessions,lipi insurance companies | Commercial Banks,3.494,2020-02-20
sector,last_20_sessions,lipi insurance companies | Fertilizer,8.25,2020-02-20
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,0.06,2020-02-20
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,3.28,2020-02-20
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,1.676,2020-02-20
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,2.671,2020-02-20
sector,last_20_sessions,lipi insurance companies | Technology and Communication,-0.133,2020-02-20
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.538,2020-02-20
sector,last_20_sessions,lipi mutual funds | All other Sectors,5.33,2020-02-20
sector,last_20_sessions,lipi mutual funds | Cement,5.897,2020-02-20
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-1.158,2020-02-20
sector,last_20_sessions,lipi mutual funds | Fertilizer,-10.74,2020-02-20
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,-0.056,2020-02-20
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-7.706,2020-02-20
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-1.298,2020-02-20
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-0.933,2020-02-20
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-0.786,2020-02-20
sector,last_20_sessions,lipi mutual funds | Textile Composite,0.5,2020-02-20
sector,last_20_sessions,lipi nbfc | All other Sectors,0.69,2020-02-20
sector,last_20_sessions,lipi nbfc | Cement,0.033,2020-02-20
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.938,2020-02-20
sector,last_20_sessions,lipi nbfc | Fertilizer,0.019,2020-02-20
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.001,2020-02-20
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.039,2020-02-20
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.106,2020-02-20
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,-0.031,2020-02-20
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.035,2020-02-20
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.17,2020-02-20
sector,last_20_sessions,lipi other organization | All other Sectors,4.775,2020-02-20
sector,last_20_sessions,lipi other organization | Cement,-0.554,2020-02-20
sector,last_20_sessions,lipi other organization | Commercial Banks,1.186,2020-02-20
sector,last_20_sessions,lipi other organization | Fertilizer,1.605,2020-02-20
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-0.046,2020-02-20
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,3.69,2020-02-20
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.291,2020-02-20
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,-0.254,2020-02-20
sector,last_20_sessions,lipi other organization | Technology and Communication,-0.337,2020-02-20
sector,last_20_sessions,lipi other organization | Textile Composite,0.55,2020-02-20

=== FILE: calendar.md ===
# Calendar as of 2020-02-21

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2020-01-23 SSGC: BOARD MEETING OTHER THAN FINANCIAL RESULTS - RESCHEDULED
- 2020-01-23 EPCL: Board Meeting - - ENGRO POLYMER & CHEMICALS LIMITED
- 2020-01-27 SSGC: BOARD MEETING OTHER THAN FINANCIAL RESULTS
- 2020-01-28 ILP: BOARD MEETING OTHER THAN FINANCIAL RESULTS
- 2020-01-30 MEBL: NOTICE OF BOARD MEETING AND CLOSED PERIOD
- 2020-01-31 FCCL: Board Meeting
- 2020-02-03 PTC: Board Meeting
- 2020-02-03 NETSOL: Board Meeting
- 2020-02-03 CHCC: NOTICE OF BOARD OF DIRECTORS MEETING AND NOTICE OF CLOSED PERIOD
- 2020-02-04 DGKC: Board Meeting
- 2020-02-06 SSGC: Board Meeting Other Than Financial Results
- 2020-02-06 EFERT: Board Meeting - Engro Fertilizers Limited
- 2020-02-06 LOTCHEM: Board Meeting / Closed Period
- 2020-02-06 NML: Board Meeting
- 2020-02-07 ILP: Notice of Board Meeting for the Half Year Ended December 31, 2019 / Closed Period
- 2020-02-07 PTC: Board Meeting Rescheduled
- 2020-02-07 SEARL: Board Meeting Other Than Financial Results
- 2020-02-11 PSO: Board Meeting
- 2020-02-12 MTL: Board Meeting
- 2020-02-12 GHNI: Board Meeting
- 2020-02-13 SEARL: NOTICE OF POSTPONEMENT OF BOARD MEETING
- 2020-02-13 MUGHAL: Notice of Board Meeting - QII 2020
- 2020-02-14 PPL: Meeting of the Board of Directors and Closed Period
- 2020-02-14 HTL: Board Meeting
- 2020-02-17 HUBC: Board Meeting/ Closed Period
- 2020-02-17 DCL: Board Meeting
- 2020-02-18 MLCF: Board Meeting
- 2020-02-18 MTL: Board Meeting Rescheduled
- 2020-02-18 ASTL: Board Meeting
- 2020-02-18 OGDC: Board meeting and close period
- 2020-02-19 KOHC: Board Meeting
- 2020-02-19 KTML: Board Meeting
- 2020-02-19 UNITY: Board Meeting
- 2020-02-19 TREET: Board Meeting
- 2020-02-20 POWER: BOARD MEETING
- 2020-02-20 ASC: Board Meeting
- 2020-02-20 SEARL: Board Meeting
- 2020-02-20 BIPL: Board Meeting - BankIslami Pakistan Limited
- 2020-02-20 STPL: 79th Board of Directors Meeting
- 2020-02-21 FEROZ: Board Meeting
- 2020-02-21 TGL: Board Meeting

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
| 12 | Six SOEs sold in FY20 | 29 Jan 2020 | outcome not shown |

=== FILE: situations.md ===
2020-01-13 (outcome_end) | 01_2019_bottom_imf_programme.md | Regime bottom: the IMF approval was not the low. The second signal (Sep 2019 rate hold, stable rupee) returned +35% to the January 2020 peak. Lesson: wait for it, not the headline.
2019-08-16 (outcome_end) | 12_2017_19_bear_and_the_2018_election.md | Balance-of-payments squeeze and hike cycle: the index fell 46% to the August 2019 low and 3 of 75 liquid names rose. Lesson: read the rate and the rupee, not the politics.

=== FILE: base_rates.csv ===
# WARNING: measured on data through 2026-10-16, partly AFTER this replay date. Use only as rough odds for a situation TYPE; infer nothing about specific names or dates.
type,horizon,n,hit_rate,median,p50plus,worst,placebo_median,verdict
shock_index5_buy,20 sessions,9,78%,+4.2%,,-7.7%,+1.1%,no word given (Verdict 3: buy only on a known trigger)
shock_index5_buy,60 sessions,9,67%,+3.5%,,-14.0%,+2.2%,no word given (Verdict 3: buy only on a known trigger)
shock_index3_buy,20 sessions,20,70%,+3.7%,,-10.9%,+1.1%,no word given
shock_index3_buy,60 sessions,20,50%,+0.7%,,-18.3%,+2.2%,no word given
shock_3day_fall5_buy,20 sessions,14,79%,+5.3%,,,,no word given (file labels this row a placebo arm)
shock_3day_fall5_buy,60 sessions,14,79%,+7.0%,,-15.5%,,no word given (file labels this row a placebo arm)
shock_fall5_hindsight_day1,20 sessions,25,12%,-4.4%,,,,biased downward (hindsight selection)
shock_fall5_hindsight_day1,60 sessions,25,38%,-4.2%,,,,biased downward (hindsight selection)
shock_fall5_hindsight_day3,20 sessions,25,16%,-3.9%,,,,biased downward (hindsight selection)
shock_fall5_hindsight_day3,60 sessions,25,46%,-2.4%,,,,biased downward (hindsight selection)
shock_fall5_hindsight_firstup_after_day1,20 sessions,25,24%,-4.4%,,,,biased downward (hindsight selection)
shock_fall5_hindsight_firstup_after_day1,60 sessions,25,46%,-2.0%,,,,biased downward (hindsight selection)
shock_fall5_hindsight_firstup_after_bottom,20 sessions,25,76%,+3.1%,,,,needs hindsight (file)
shock_fall5_hindsight_firstup_after_bottom,60 sessions,25,70%,+4.7%,,,,needs hindsight (file)
oracle_top3_3m_mom_S1,24 months (window; rotation exits),41,46%,-3%,,,,no verdict word (file: nothing reached 3x)
oracle_top3_6m_mom_skip1_S2,24 months (window; rotation exits),36,39%,-9%,,,,no verdict word (file: nothing reached 3x)
breakout_252high_S3,24 months (window; rotation exits),12,58%,+17%,,,,a hypothesis from five windows (file)
oracle_cheapest_pe_top_sector_S4,24 months (window; rotation exits),34,53%,+2%,,,,no verdict word (file: nothing reached 3x)
oracle_dip20_uptrend_S5,24 months (window; rotation exits),56,54%,+1%,,,,no verdict word (file: nothing reached 3x)
oracle_eps_jump50_S6,24 months (window; rotation exits),25,48%,-3%,,,,no verdict word (file: nothing reached 3x)
oracle_top10_liquid_ew_S8,24 months (window; rotation exits),49,63%,+4%,,,,no verdict word (file: nothing reached 3x)
codex_mom63,24 months (cohort 2024-26; rotation exits),44,55%,+2.5%,,,,suggestive (file-level)
codex_mom252,24 months (cohort 2024-26; rotation exits),30,37%,-1.7%,,,,suggestive (file-level)
breakout_252high_codex,24 months (cohort 2024-26; rotation exits),53,62%,+4.6%,,,,suggestive (file-level)
codex_dip200,24 months (cohort 2024-26; rotation exits),58,47%,-0.6%,,,,suggestive (file-level)
codex_sector63,24 months (cohort 2024-26; rotation exits),55,38%,-1.7%,,,,suggestive (file-level)
codex_vol20,24 months (cohort 2024-26; rotation exits),51,33%,-2.0%,,,,suggestive (file-level)
codex_eps_yoy,24 months (cohort 2024-26; rotation exits),39,44%,-2.2%,,,,suggestive (file-level)
insider_cluster,63 sessions,37,46%,-0.4%,,-33.2%,-0.6%,not supported
insider_cluster,21 sessions,44,,-0.9%,,,,not supported
insider_cluster,126 sessions,33,,-5.3%,,,,not supported
insider_cluster_net_sales,63 sessions,28,43%,-2.2%,,-33.2%,-0.1%,not supported
insider_singles,63 sessions,97,57%,+2.3%,,-33.2%,-1.6%,not supported
insider_singles,21 sessions,117,,-0.5%,,,,not supported
insider_singles,126 sessions,83,,-0.0%,,,,not supported
insider_sponsor_substantial,63 sessions,5,20%,-8.7%,,-13.3%,-2.2%,not supported (n too small)
insider_sponsor_substantial,21 sessions,7,,-3.2%,,,,not supported (n too small)
insider_sponsor_substantial,126 sessions,4,,-12.8%,,,,not supported (n too small)
insider_director_ceo,63 sessions,42,57%,+2.5%,,-33.2%,-1.3%,not supported
insider_director_ceo,21 sessions,51,,-1.4%,,,,not supported
insider_director_ceo,126 sessions,33,,+2.7%,,,,not supported
insider_executive,63 sessions,59,54%,+1.8%,,-22.7%,+0.9%,not supported
insider_executive,21 sessions,81,,+0.4%,,,,not supported
insider_executive,126 sessions,45,,+2.5%,,,,not supported
insider_roundtrip,63 sessions,23,48%,-0.6%,,-22.7%,+1.2%,not supported
insider_roundtrip,21 sessions,34,,-1.1%,,,,not supported
insider_roundtrip,126 sessions,18,,-1.8%,,,,not supported
insider_clean_buy,63 sessions,113,55%,+1.8%,,-33.2%,-1.5%,not supported
insider_clean_buy,21 sessions,149,,-0.5%,,,,not supported
insider_clean_buy,126 sessions,92,,-0.3%,,,,not supported
insider_sell_single,63 sessions,102,46%,-2.7%,,-63.6%,-0.8%,not supported
insider_sell_single,21 sessions,137,,-3.1%,,,,not supported
insider_sell_single,126 sessions,83,,-4.2%,,,,not supported
insider_sell_cluster,63 sessions,33,39%,-3.4%,,-45.5%,-0.5%,not supported
insider_sell_cluster,21 sessions,40,,-2.4%,,,,not supported
insider_sell_cluster,126 sessions,27,,-2.6%,,,,not supported
results_yoy_POS,5 sessions,378,48%,-0.2%,,,,no tradable drift (H1)
results_yoy_POS,20 sessions,366,38%,-2.0%,,,,no tradable drift (H1)
results_yoy_POS,60 sessions,338,43%,-2.3%,,,,no tradable drift (H1)
results_yoy_LTP,5 sessions,96,32%,-1.8%,,,,no tradable drift (H1)
results_yoy_LTP,20 sessions,92,48%,-0.4%,,,,no tradable drift (H1)
results_yoy_LTP,60 sessions,88,45%,-2.5%,,,,no tradable drift (H1)
results_yoy_NEG,5 sessions,188,46%,-0.5%,,,,no tradable drift (H1)
results_yoy_NEG,20 sessions,186,46%,-1.5%,,,,no tradable drift (H1)
results_yoy_NEG,60 sessions,181,39%,-5.3%,,,,no tradable drift (H1)
results_yoy_PTL,5 sessions,81,36%,-1.1%,,,,no tradable drift (H1)
results_yoy_PTL,20 sessions,79,34%,-2.4%,,,,no tradable drift (H1)
results_yoy_PTL,60 sessions,78,44%,-2.6%,,,,no tradable drift (H1)
results_yoy_MID,5 sessions,318,37%,-1.1%,,,,no tradable drift (H1)
results_yoy_MID,20 sessions,315,35%,-2.3%,,,,no tradable drift (H1)
results_yoy_MID,60 sessions,291,36%,-4.9%,,,,no tradable drift (H1)
results_yoy_positive,5 sessions,474,45%,-0.7%,,-22.2%,,no tradable drift (H1)
results_yoy_positive,20 sessions,458,40%,-1.6%,,-39.1%,,no tradable drift (H1)
results_yoy_positive,60 sessions,426,44%,-2.3%,,-91.6%,,no tradable drift (H1)
results_yoy_negative,5 sessions,269,43%,-0.8%,,,,no tradable drift (H1)
results_yoy_negative,20 sessions,265,42%,-2.1%,,,,no tradable drift (H1)
results_yoy_negative,60 sessions,259,40%,-4.4%,,,,no tradable drift (H1)
results_yoy_all,5 sessions,1061,42%,-0.8%,,,,no tradable drift (H1)
results_yoy_all,20 sessions,1038,39%,-2.0%,,,,no tradable drift (H1)
results_yoy_all,60 sessions,976,41%,-3.3%,,,,no tradable drift (H1)
results_muted_pe_main_H3,60 sessions,47,57%,+2.4%,,-26.0%,-0.3%,not confirmed (worst mapped to horizon by position)
results_muted_pe_main_H3,120 sessions,42,67%,+6.4%,,-47.4%,+1.4%,not confirmed (worst mapped to horizon by position)
results_muted_pe_tercile_H3,60 sessions,47,47%,-2.0%,,,,not confirmed
results_muted_pe_tercile_H3,120 sessions,40,55%,+1.0%,,,,not confirmed
results_pe_below6_any_reaction_H3,60 sessions,88,56%,+2.4%,,,,not confirmed
results_pe_below6_any_reaction_H3,120 sessions,80,61%,+7.2%,,,,not confirmed
results_muted_pe_above6_H3,60 sessions,84,32%,-4.4%,,,,not confirmed
results_muted_pe_above6_H3,120 sessions,78,41%,-4.3%,,,,not confirmed
results_positive_reference_H3,60 sessions,425,42%,-2.6%,,,,reference (no verdict word)
results_positive_reference_H3,120 sessions,389,47%,-2.4%,,,,reference (no verdict word)
results_board_notice_leg,about 5 sessions (median leg),2688,41%,-0.9%,,,-1.0%,nothing (indistinguishable from placebo)
first_rate_cut_kse100,20 sessions,3,100%,+7.1%,,+3.0%,+1.3%,weak (H1)
first_rate_cut_kse100,60 sessions,3,67%,+8.4%,,-9.4%,+3.7%,weak (H1)
first_rate_cut_kse100,120 sessions,3,100%,+39.8%,,+1.1%,+7.9%,weak (H1)
first_rate_cut_ew,20 sessions,3,100%,+3.9%,,+3.3%,+0.8%,weak (H1)
first_rate_cut_ew,60 sessions,3,67%,+11.9%,,-21.5%,+1.9%,weak (H1)
first_rate_cut_ew,120 sessions,3,67%,+49.2%,,-7.0%,+5.1%,weak (H1)
cpi_fall1pt_kse100,120 sessions,10,60%,+12.6%,,-18.7%,+8.1%,weak as a 12-month rule (H4)
cpi_fall1pt_kse100,250 sessions,10,70%,+52.3%,,-21.1%,+19.8%,weak as a 12-month rule (H4)
cpi_fall1pt_ew,250 sessions,10,60%,+53.1%,,-33.8%,+14.1%,weak as a 12-month rule (H4)
first_rate_hike_kse100,120 sessions,2,,-5.6%,,,,weak (H3)
first_rate_hike_ew,120 sessions,2,,-15.6%,,,,weak (H3)
mpc_hold_kse100,20 sessions,39,54%,+0.3%,,,,no verdict given (in sample; overlapping)
mpc_hold_kse100,60 sessions,37,62%,+5.5%,,,,no verdict given (in sample; overlapping)
mpc_hold_kse100,120 sessions,36,61%,+4.4%,,,,no verdict given (in sample; overlapping)
sector_momentum_ls,3 months,31.7,65%,+2.65%,,-21.64%,+0.03%,works modestly (H1; primary 6/0/3m)
sector_regime_tilt_RT_net_minus_B,3 months,31.7,51%,+0.21%,,-16.02%,,no edge (placebo p 0.255 is not a median)
sector_momentum_top3_net_minus_B,3 months,31.7,54%,+0.95%,,-15.91%,,fails offset and half checks (file)
sector_regime_tilt_RT_net_abs,3 months,31.7,46%,-1.20%,,-28.10%,,no edge
quality_top_third,12 months,26,92%,+57.7%,,-7.6%,,Weak not proven
quality_bottom_third,12 months,26,92%,+37.8%,,-14.1%,,Weak not proven
quality_top_minus_bottom,12 months,26,69%,+5.8%,,-33.2%,,Weak not proven (file placebo p 0.054 is not a median)
quality_qarp_minus_ew_kmi,12 months,26,54%,+2.4%,,-22.2%,,Weak not proven
quality_qarp_minus_kmi30,12 months,26,54%,+0.7%,,-14.5%,,Weak not proven
quality_qarp_minus_all_scored,12 months,26,46%,-0.3%,,-26.3%,,Weak not proven
quality_top_minus_bottom_ext_ab,12 months,36,67%,+8.2%,,-18.4%,,Weak not proven (extended a and b only)
quality_qarp_minus_ew_kmi_ext_ab,12 months,36,72%,+7.3%,,-18.0%,,Weak not proven (extended a and b only)
quality_qarp_minus_kmi30_ext_ab,12 months,36,69%,+9.6%,,-13.9%,,Weak not proven (extended a and b only)
winners_model_top_decile,6 months,550,57%,+7.1%,,-94.8%,+8.7%,does not support fast rotation
winners_rule_screen,6 months,229,62%,+7.6%,,-93.1%,+8.7%,does not support fast rotation
winners_all_liquid_placebo,6 months,5299,62%,+8.7%,,-94.8%,,placebo baseline (no verdict word)
winners_random_name_per_month_placebo,6 months,500,,+12.6%,,,,placebo (median of medians; 500 draws)
deal_post_intention,to completion or withdrawal (completion median 207 days),54,48%,-1.2%,,-64.3%,,no verdict word (see What this changes)
deal_post_intention_kmi,to completion or withdrawal (completion median 207 days),19,58%,+5.3%,,-25.9%,,no verdict word
deal_post_intention_vs_kse100,to completion or withdrawal (completion median 207 days),46,39%,-14.3%,,-88.2%,,lagged the index (file)
deal_post_intention_full_tender_upper_bound,to completion or withdrawal (completion median 207 days),19,84%,+12.5%,,-58.5%,,upper bound only (file)
deal_post_offer,to completion (duration not stated),24,54%,+1.1%,,-35.8%,,no verdict word
deal_post_offer_kmi,to completion (duration not stated),11,,+1.4%,,,,no verdict word
deal_sponsor_delisting,about 205 days (median),8,75%,+64%,,-15%,,no verdict word
volume_locks_V1_liq5,trail20 stop (variable),248,27%,-13.0%,7.7%,-46%,-6.9%,nothing
volume_locks_V2_liq5,trail20 stop (variable),215,28%,-14.2%,6.5%,-46%,-7.0%,nothing
volume_locks_V3_liq5,trail20 stop (variable),471,32%,-11.7%,7.4%,-46%,-5.0%,nothing
volume_locks_V4_liq5,trail20 stop (variable),440,35%,-9.6%,11.6%,-32%,-8.3%,watch not tradable
volume_locks_V1_liq5,60 sessions,237,38%,-10.3%,10.5%,-71%,+1.0%,nothing
volume_locks_V2_liq5,60 sessions,208,39%,-11.0%,10.6%,-71%,+0.3%,nothing
volume_locks_V3_liq5,60 sessions,465,42%,-7.1%,7.5%,-71%,+1.5%,nothing
volume_locks_V4_liq5,60 sessions,445,44%,-2.3%,4.0%,-60%,-0.8%,watch not tradable
volume_locks_V1_liq1,trail20 stop (variable),456,30%,-10.9%,9.2%,-43%,-6.2%,nothing
volume_locks_V2_liq1,trail20 stop (variable),413,31%,-12.8%,9.0%,-43%,-7.2%,nothing
volume_locks_V3_liq1,trail20 stop (variable),748,34%,-10.5%,8.7%,-43%,-4.5%,nothing
volume_locks_V4_liq1,trail20 stop (variable),738,36%,-9.1%,12.3%,-32%,-7.3%,watch not tradable
volume_locks_V1_liq1,60 sessions,446,39%,-6.8%,8.5%,-71%,+1.0%,nothing
volume_locks_V2_liq1,60 sessions,406,41%,-8.7%,9.1%,-71%,+0.0%,nothing
volume_locks_V3_liq1,60 sessions,736,43%,-5.2%,7.3%,-71%,+2.0%,nothing
volume_locks_V4_liq1,60 sessions,734,46%,-1.7%,4.6%,-60%,-0.5%,watch not tradable
volume_locks_V1_strict10_liq5,trail20 stop (variable),129,29%,-11.7%,,,,same conclusion (literal +10% sensitivity)
volume_locks_V4_strict10_liq1,trail20 stop (variable),377,,-6.6%,,,,same conclusion (literal +10% sensitivity)
results_gap_up,20 sessions,41,51%,+0.7%,5%,-23.7%,+1.7%,watch (20-day exit has no edge)
results_gap_up,60 sessions,37,81%,+16.6%,14%,-44.1%,+10.0%,watch (p 0.11 vs same-year random)
results_gap_up,120 sessions,37,78%,+18.4%,22%,-38.2%,+21.0%,watch (gone at 120d per file)
results_gap_up_trail20,trail20 stop (variable),38,68%,+14.5%,26%,-20.9%,+9.6%,watch (exit that worked per file)
results_upper_lock_results_day,60 sessions,31,61%,+5.8%,10%,-21.9%,+3.4%,nothing
results_upper_lock_results_day,120 sessions,29,62%,+6.5%,21%,-48.8%,+10.2%,nothing
results_upper_lock_results_day_trail20,trail20 stop (variable),33,48%,-2.0%,12%,-23.1%,-0.7%,nothing
results_loss_to_profit,60 sessions,49,59%,+5.7%,12%,-32.5%,+4.0%,nothing as an entry rule
results_loss_to_profit,120 sessions,47,60%,+8.8%,17%,-70.6%,+12.0%,nothing as an entry rule
results_loss_to_profit_trail20,trail20 stop (variable),47,43%,-2.9%,19%,-24.0%,-1.3%,nothing as an entry rule
results_all_liquid_baseline,60 sessions,1223,59%,+4.7%,7%,-72.1%,,baseline (no verdict word)
results_all_liquid_baseline_trail20,trail20 stop (variable),1169,46%,-2.5%,16%,-38.5%,,baseline (no verdict word)
=== END ===
