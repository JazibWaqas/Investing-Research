# Replay bundle, close of 2019-02-08

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
# Market as of 2019-02-08 close (public information only)

- KSE100: 40,887 on 2019-02-08; 1m +5.1%, 3m -1.2%, 6m -3.8%, 12m -7.6%
- KMI All Share: 19,777 on 2019-02-08; 1m +4.3%, 3m -3.0%, 6m -4.5%, 12m -9.3%
- Policy rate 10.25%; last MPC decision 2019-01-31: hike (+25bp)
- 6M T-bill cutoff 10.35% (auction 2018-12-05); 3M 10.30%, 12M nan%
- CPI YoY 7.2% for 2019-01 (published by 2019-02-03); three months earlier (2018-10) 6.78%
- Brent: 61.37 USD/bbl on 2019-02-08; 3-month change -11.4%
- USD/PKR: 138.14  on 2019-02-08; 3-month change +4.2%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.10pp (market near policy rate); CPI rising over 3 months (+0.4pp)
- Next MPC: see SBP calendar

Session date used: 2019-02-08. Liquid KMI names: 47 (membership KMI_ALL_derived_2019-01-28.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.0171,-0.212,-0.3353,0,0
E&P,3,0.0378,-0.0231,-0.0393,0,0
OMC,4,0.037,-0.0701,-0.205,0,0
Power,5,0.035,-0.0053,-0.0101,0,0
Fertilizer,4,0.0366,-0.0213,-0.0096,1,1
Cement,16,0.0223,-0.0674,-0.1186,0,0
Steel & engineering,10,0.0656,-0.1054,-0.2973,0,0
Autos,12,0.0472,-0.1505,-0.2586,0,0
Tech & telecom,6,0.0703,-0.0604,-0.1288,0,0
Islamic banks & fin.,7,0.0161,-0.0558,-0.0825,0,0
Pharma,11,0.0882,-0.0274,-0.1395,0,0
Textiles,17,0.0277,0.0251,0.0737,1,1
Food & staples,12,0.0382,-0.0387,-0.138,0,0
Chemicals,16,0.0336,-0.018,-0.0442,0,0
"Glass, packaging, paper",12,0.0285,-0.0034,-0.089,0,0
Gas utilities & misc,9,0.0252,-0.0337,-0.1257,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,n_results,n_material,n_insider_buy,n_insider_sell
AGP,89.05,0.03,-0.032,-0.035,,-0.169,1.211,0,0,0,0,0
ASTL,53.46,0.103,-0.192,-0.32,-0.453,-0.45,0.983,0,0,0,0,0
ATRL,137.09,-0.007,-0.344,-0.242,-0.332,-0.392,1.294,0,1,0,0,0
CHCC,72.62,-0.011,-0.039,-0.195,-0.462,-0.477,0.591,0,0,1,0,0
DCL,13.86,0.041,-0.107,-0.198,-0.459,-0.522,1.203,2,0,0,0,0
DGKC,92.94,0.084,-0.124,-0.21,-0.416,-0.458,0.763,0,0,0,0,0
EFERT,76.27,0.015,-0.08,-0.056,0.108,-0.08,1.179,0,1,0,0,0
EPCL,38.73,-0.021,0.024,0.1,0.467,-0.074,0.648,0,2,0,0,0
FCCL,22.65,0.041,-0.102,-0.082,-0.217,-0.289,0.77,0,0,0,0,0
FCEPL,87.95,0.102,0.014,-0.049,-0.068,-0.168,2.212,0,0,0,0,0
FEROZ,209.62,0.389,0.15,0.027,-0.28,-0.323,2.115,0,0,0,0,0
FML,92.76,-0.022,0.359,0.388,0.49,-0.249,0.354,0,0,0,0,0
GAL,102.81,0.118,-0.16,-0.388,-0.391,-0.62,1.686,0,0,0,0,0
GHNI,232.42,-0.078,-0.38,-0.327,-0.194,-0.46,2.564,0,0,0,0,0
HUBC,92.66,0.022,-0.024,-0.054,-0.069,-0.116,1.017,0,0,0,0,0
INIL,160.55,0.079,-0.09,-0.314,-0.475,-0.483,1.256,0,1,0,0,0
ISL,74.69,0.078,-0.156,-0.331,-0.398,-0.41,1.151,0,1,0,0,0
KEL,6.38,0.036,0.074,0.156,-0.056,-0.103,1.208,0,0,0,0,0
KOHC,87.85,0.007,-0.129,-0.009,-0.249,-0.266,1.105,0,0,0,0,0
LCI,732.2,-0.068,0.181,-0.011,-0.092,-0.204,0.243,0,0,0,0,0
LOTCHEM,17.25,-0.042,-0.08,0.256,0.971,-0.136,0.565,0,0,0,0,0
LUCK,491.18,0.063,0.013,-0.078,-0.223,-0.321,0.679,0,1,0,0,0
MARI,1289.27,-0.069,-0.087,-0.128,-0.169,-0.192,0.732,0,0,0,0,0
MEBL,94.45,0.049,-0.003,0.144,0.345,-0.052,0.679,0,0,0,0,0
MLCF,46.81,0.026,-0.075,-0.141,-0.432,-0.428,0.575,0,0,0,0,0
NETSOL,91.57,0.24,-0.216,-0.343,0.463,-0.445,1.298,0,0,0,0,0
NML,143.36,0.049,-0.05,0.032,-0.139,-0.16,1.028,0,0,0,0,0
NRL,236.19,-0.094,-0.182,-0.435,-0.458,-0.478,0.604,0,1,0,0,0
OGDC,147.4,0.056,-0.041,-0.036,-0.119,-0.169,1.31,0,0,0,0,0
PAEL,27.29,-0.009,-0.137,-0.31,-0.554,-0.551,1.143,0,0,0,0,0
PIBTL,12.61,0.123,0.051,-0.022,-0.322,-0.339,1.6,0,0,0,0,0
PIOC,45.21,-0.017,-0.082,-0.08,-0.396,-0.429,0.378,0,0,0,0,0
PKGS,394.07,0.063,0.042,-0.193,-0.307,-0.333,1.625,0,0,1,0,0
POWER,8.26,0.004,0.022,-0.066,-0.175,-0.206,0.703,0,0,0,0,0
PPL,187.92,0.134,0.057,0.041,0.052,-0.03,1.93,0,0,0,0,0
PRL,24.45,-0.015,-0.203,-0.435,-0.421,-0.45,0.711,0,1,0,0,0
PSO,239.3,0.013,-0.113,-0.111,-0.051,-0.156,0.907,0,0,0,0,0
SEARL,269.84,0.101,-0.157,-0.185,-0.289,-0.307,2.069,0,0,0,0,0
SNGP,84.86,0.002,-0.049,-0.13,-0.289,-0.314,1.037,0,0,0,0,0
SPL,27.16,-0.121,-0.257,0.459,0.479,-0.326,0.364,0,0,0,0,0
SSGC,24.97,-0.015,-0.024,-0.226,-0.297,-0.348,1.345,0,1,0,0,0
STCL,16.53,0.092,-0.128,-0.266,0.035,-0.4,0.626,0,0,0,0,0
TGL,101.76,0.084,0.116,0.107,-0.018,-0.15,1.05,0,0,0,0,0
TREET,25.76,0.071,0.006,-0.26,-0.45,-0.446,1.024,0,0,0,0,0
UNITY,24.23,-0.068,-0.272,-0.284,0.012,-0.46,0.708,0,0,1,0,0
WAFI,309.31,0.202,0.124,-0.074,-0.09,-0.21,2.804,0,0,0,0,0
WAVES,27.83,0.01,-0.086,-0.208,-0.302,-0.324,0.71,0,0,0,0,0

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2019-01-10,TPLP,material_info,Disclosure of Material Information
2019-01-10,PKGS,material_info,MATERIAL INFORMATION
2019-01-11,GHNL,material_info,Material Information
2019-01-11,MTL,material_info,MATERIAL INFORMATION REVOKED
2019-01-11,MTL,material_info,MATERIAL INFORMATION
2019-01-11,ECOP,material_info,Disclosure of Material Information
2019-01-14,UNITY,material_info,Material Information
2019-01-14,EPCL,financial_result,Right Issue of Engro Polymer & Chemicals Limited - Quarterly progress repor
2019-01-15,LOADS,material_info,Material Information
2019-01-17,BAFS,material_info,Material Information
2019-01-17,MFFL,material_info,Material Information
2019-01-17,DINT,material_info,Material Information
2019-01-17,DINT,material_info,Material Information
2019-01-17,DINT,material_info,Material Information
2019-01-17,DINT,material_info,Material Information
2019-01-17,DINT,material_info,Material Information
2019-01-17,DINT,material_info,Material Information
2019-01-17,DINT,material_info,Material Information
2019-01-21,DYNO,material_info,Material Information
2019-01-21,GSKCH,material_info,Material Information Increase of Paid Up Capital and Shareholding
2019-01-21,ACPL,material_info,Material Information
2019-01-21,NRL,financial_result,"Financial Results for the Half Year Ended December 31, 2018"
2019-01-21,ATRL,financial_result,FINANCIAL RESULTS FOR THE QUARTER ENDED 2018-12-31
2019-01-24,AHTM,material_info,Material Information
2019-01-24,BHAT,material_info,Material Information
2019-01-24,SSGC,financial_result,"Transmission of Annual Report for the Year Ended June 30, 2017"
2019-01-25,CHCC,material_info,MATERIAL INFORMATION - COMMISSIONING OF CEMENT LINE 3
2019-01-25,AICL,material_info,Material Information
2019-01-25,ISL,financial_result,FINANCIAL RESULTS FOR THE HALF YEAR ENDED 31-12-2018
2019-01-28,AABS,material_info,Material Information
2019-01-28,AABS,material_info,Material Information
2019-01-28,IMSL,material_info,Material Information
2019-01-28,KEL,dividend_or_bonus,Final Book Closure of KE AZM SUKUK-3
2019-01-28,KEL,dividend_or_bonus,Book Closure of KE SUKUK-4 (Sukuk-ul-Shirkah)
2019-01-28,HTL,insider_trade,Insider trade disclosure
2019-01-28,BAFL,insider_trade,Insider trade disclosure
2019-01-29,ARCTM,material_info,DISCLOSURE OF MATERIAL INFORMATION
2019-01-29,ARPL,material_info,Material Information
2019-01-29,FFL,material_info,Disclosure of Material Information by Fauji Foods Limited
2019-01-29,AHTM,insider_trade,Insider trade disclosure
2019-01-29,OLPL,insider_trade,Insider trade disclosure
2019-01-29,SNAI,insider_trade,Insider trade disclosure
2019-01-30,FFBL,material_info,Material Information by Fauji Fertilizer Bin Qasim Limited
2019-01-30,ARCTM,material_info,DISCLOSURE OF MATERIAL INFORMATION
2019-01-30,INIL,financial_result,FINANCIAL RESULTS FOR THE HALF YEAR ENDED 31-12-2018
2019-01-30,PRL,financial_result,Financial Results For Six Months Period Ended 31st December 2018
2019-01-30,GASF,insider_trade,Insider trade disclosure
2019-01-30,BAFL,insider_trade,Insider trade disclosure
2019-01-31,ANL,material_info,Material Information - Approval of Creditors' Led Scheme of Arrangement
2019-01-31,LUCK,financial_result,"Financial Results for the quarter ended December 31, 2018"
2019-01-31,EPCL,financial_result,"Financial Results for the Year Ended December 31, 2018 Consolidated And Sta"
2019-01-31,ECOP,insider_trade,Insider trade disclosure
2019-01-31,ECOP,insider_trade,Insider trade disclosure
2019-01-31,KOSM,insider_trade,Insider trade disclosure
2019-02-01,ABL,insider_trade,Insider trade disclosure
2019-02-01,HINOON,insider_trade,Insider trade disclosure
2019-02-01,ECOP,insider_trade,Insider trade disclosure
2019-02-01,FCCL,insider_trade,Insider trade disclosure
2019-02-01,STPL,insider_trade,Insider trade disclosure
2019-02-01,STPL,insider_trade,Insider trade disclosure
2019-02-01,BAFL,insider_trade,Insider trade disclosure
2019-02-04,ECOP,insider_trade,Insider trade disclosure
2019-02-04,MUREB,insider_trade,Insider trade disclosure
2019-02-04,IGIHL,insider_trade,Insider trade disclosure
2019-02-04,PKGS,insider_trade,Insider trade disclosure
2019-02-04,HINOON,insider_trade,Insider trade disclosure
2019-02-04,BAFL,insider_trade,Insider trade disclosure
2019-02-04,IGIHL,insider_trade,Insider trade disclosure
2019-02-04,PSMC,insider_trade,Insider trade disclosure
2019-02-06,CLOV,material_info,Material Information
2019-02-06,FFBL,material_info,Disclosure of Material Information by Fauji Fertilizer Bin Qasim Limited
2019-02-06,FFL,material_info,Material Information
2019-02-06,OLPL,material_info,THE DISCLOSURE OF MATERIAL INFORMATION
2019-02-06,PKGS,insider_trade,Insider trade disclosure
2019-02-06,HINOON,insider_trade,Insider trade disclosure
2019-02-06,JVDC,insider_trade,Insider trade disclosure
2019-02-06,IGIHL,insider_trade,Insider trade disclosure
2019-02-06,BAFL,insider_trade,Insider trade disclosure
2019-02-06,PSMC,insider_trade,Insider trade disclosure
2019-02-07,HINOON,insider_trade,Insider trade disclosure
2019-02-07,HINOON,insider_trade,Insider trade disclosure
2019-02-07,SALT,insider_trade,Insider trade disclosure
2019-02-07,ILTM,insider_trade,Insider trade disclosure
2019-02-08,EFERT,financial_result,"Financial Results for the Year Ended December 31, 2018"
2019-02-08,PKGS,insider_trade,Insider trade disclosure
2019-02-08,PKGS,insider_trade,Insider trade disclosure
2019-02-08,HINOON,insider_trade,Insider trade disclosure
2019-02-08,HINOON,insider_trade,Insider trade disclosure
2019-02-08,BAFL,insider_trade,Insider trade disclosure

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-3.194,2019-02-07
investor_type,last_5_sessions,broker proprietary trading,2.267,2019-02-07
investor_type,last_5_sessions,companies,-2.135,2019-02-07
investor_type,last_5_sessions,foreign corporates,15.066,2019-02-07
investor_type,last_5_sessions,foreign individual,0.234,2019-02-07
investor_type,last_5_sessions,individuals,-0.498,2019-02-07
investor_type,last_5_sessions,insurance companies,-0.564,2019-02-07
investor_type,last_5_sessions,mutual funds,-12.633,2019-02-07
investor_type,last_5_sessions,nbfc,0.91,2019-02-07
investor_type,last_5_sessions,other organization,-0.037,2019-02-07
investor_type,last_5_sessions,overseas pakistani,0.584,2019-02-07
sector,last_5_sessions,fipi | All other Sectors,1.656,2019-02-07
sector,last_5_sessions,fipi | Cement,1.814,2019-02-07
sector,last_5_sessions,fipi | Commercial Banks,8.131,2019-02-07
sector,last_5_sessions,fipi | Fertilizer,2.397,2019-02-07
sector,last_5_sessions,fipi | Food and Personal Care Products,-0.153,2019-02-07
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,0.646,2019-02-07
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,-0.381,2019-02-07
sector,last_5_sessions,fipi | Power Generation and Distribution,0.228,2019-02-07
sector,last_5_sessions,fipi | Technology and Communication,0.045,2019-02-07
sector,last_5_sessions,fipi | Textile Composite,1.5,2019-02-07
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-0.689,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Cement,-1.136,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,-0.719,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-0.577,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-0.02,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.105,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-0.369,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.163,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,-0.027,2019-02-07
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.075,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,0.605,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.483,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.561,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.055,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.348,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.028,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.357,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.218,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,0.136,2019-02-07
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,0.608,2019-02-07
sector,last_5_sessions,lipi companies | All other Sectors,-0.122,2019-02-07
sector,last_5_sessions,lipi companies | Cement,-1.251,2019-02-07
sector,last_5_sessions,lipi companies | Commercial Banks,0.556,2019-02-07
sector,last_5_sessions,lipi companies | Fertilizer,-0.13,2019-02-07
sector,last_5_sessions,lipi companies | Food and Personal Care Products,0.281,2019-02-07
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,-0.398,2019-02-07
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,0.288,2019-02-07
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.364,2019-02-07
sector,last_5_sessions,lipi companies | Technology and Communication,-0.17,2019-02-07
sector,last_5_sessions,lipi companies | Textile Composite,-0.825,2019-02-07
sector,last_5_sessions,lipi individuals | All other Sectors,-0.003,2019-02-07
sector,last_5_sessions,lipi individuals | Cement,-1.828,2019-02-07
sector,last_5_sessions,lipi individuals | Commercial Banks,-2.203,2019-02-07
sector,last_5_sessions,lipi individuals | Fertilizer,-0.287,2019-02-07
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,0.588,2019-02-07
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,0.378,2019-02-07
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,0.723,2019-02-07
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.306,2019-02-07
sector,last_5_sessions,lipi individuals | Technology and Communication,0.315,2019-02-07
sector,last_5_sessions,lipi individuals | Textile Composite,1.512,2019-02-07
sector,last_5_sessions,lipi insurance companies | All other Sectors,-1.062,2019-02-07
sector,last_5_sessions,lipi insurance companies | Cement,5.053,2019-02-07
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-2.046,2019-02-07
sector,last_5_sessions,lipi insurance companies | Fertilizer,-0.508,2019-02-07
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,-0.018,2019-02-07
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-1.076,2019-02-07
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-0.285,2019-02-07
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,-0.021,2019-02-07
sector,last_5_sessions,lipi insurance companies | Technology and Communication,-0.052,2019-02-07
sector,last_5_sessions,lipi insurance companies | Textile Composite,-0.55,2019-02-07
sector,last_5_sessions,lipi mutual funds | All other Sectors,-0.508,2019-02-07
sector,last_5_sessions,lipi mutual funds | Cement,-2.233,2019-02-07
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-3.529,2019-02-07
sector,last_5_sessions,lipi mutual funds | Fertilizer,-1.04,2019-02-07
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,-0.276,2019-02-07
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-1.322,2019-02-07
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.726,2019-02-07
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.5,2019-02-07
sector,last_5_sessions,lipi mutual funds | Technology and Communication,-0.253,2019-02-07
sector,last_5_sessions,lipi mutual funds | Textile Composite,-2.246,2019-02-07
sector,last_5_sessions,lipi nbfc | All other Sectors,0.542,2019-02-07
sector,last_5_sessions,lipi nbfc | Cement,-0.006,2019-02-07
sector,last_5_sessions,lipi nbfc | Commercial Banks,-0.031,2019-02-07
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.012,2019-02-07
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,0.0,2019-02-07
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.128,2019-02-07
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.311,2019-02-07
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.016,2019-02-07
sector,last_5_sessions,lipi nbfc | Technology and Communication,-0.0,2019-02-07
sector,last_5_sessions,lipi nbfc | Textile Composite,-0.005,2019-02-07
sector,last_5_sessions,lipi other organization | All other Sectors,-0.418,2019-02-07
sector,last_5_sessions,lipi other organization | Cement,-0.896,2019-02-07
sector,last_5_sessions,lipi other organization | Commercial Banks,-0.721,2019-02-07
sector,last_5_sessions,lipi other organization | Fertilizer,0.102,2019-02-07
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,-0.055,2019-02-07
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,1.511,2019-02-07
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.082,2019-02-07
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.422,2019-02-07
sector,last_5_sessions,lipi other organization | Technology and Communication,0.005,2019-02-07
sector,last_5_sessions,lipi other organization | Textile Composite,-0.07,2019-02-07
investor_type,last_20_sessions,banks / dfi,-9.395,2019-02-07
investor_type,last_20_sessions,broker proprietary trading,7.027,2019-02-07
investor_type,last_20_sessions,companies,-8.102,2019-02-07
investor_type,last_20_sessions,foreign corporates,29.329,2019-02-07
investor_type,last_20_sessions,foreign individual,0.234,2019-02-07
investor_type,last_20_sessions,individuals,-1.512,2019-02-07
investor_type,last_20_sessions,insurance companies,-0.99,2019-02-07
investor_type,last_20_sessions,mutual funds,-15.538,2019-02-07
investor_type,last_20_sessions,nbfc,-1.029,2019-02-07
investor_type,last_20_sessions,other organization,-0.211,2019-02-07
investor_type,last_20_sessions,overseas pakistani,0.186,2019-02-07
sector,last_20_sessions,fipi | All other Sectors,1.006,2019-02-07
sector,last_20_sessions,fipi | Cement,0.564,2019-02-07
sector,last_20_sessions,fipi | Commercial Banks,26.329,2019-02-07
sector,last_20_sessions,fipi | Fertilizer,4.722,2019-02-07
sector,last_20_sessions,fipi | Food and Personal Care Products,-0.09,2019-02-07
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,0.364,2019-02-07
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,-2.034,2019-02-07
sector,last_20_sessions,fipi | Power Generation and Distribution,-1.468,2019-02-07
sector,last_20_sessions,fipi | Technology and Communication,-0.023,2019-02-07
sector,last_20_sessions,fipi | Textile Composite,0.381,2019-02-07
sector,last_20_sessions,lipi banks / dfi | All other Sectors,-0.906,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Cement,-0.838,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-3.72,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-2.811,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.022,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,-0.909,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-0.377,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,0.07,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,-0.199,2019-02-07
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.275,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,2.167,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Cement,0.363,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,3.389,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,0.189,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.35,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,1.895,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-2.594,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.192,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,1.01,2019-02-07
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,0.765,2019-02-07
sector,last_20_sessions,lipi companies | All other Sectors,-4.894,2019-02-07
sector,last_20_sessions,lipi companies | Cement,-2.305,2019-02-07
sector,last_20_sessions,lipi companies | Commercial Banks,-1.491,2019-02-07
sector,last_20_sessions,lipi companies | Fertilizer,0.752,2019-02-07
sector,last_20_sessions,lipi companies | Food and Personal Care Products,0.268,2019-02-07
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,0.775,2019-02-07
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,0.506,2019-02-07
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-0.499,2019-02-07
sector,last_20_sessions,lipi companies | Technology and Communication,-0.231,2019-02-07
sector,last_20_sessions,lipi companies | Textile Composite,-0.982,2019-02-07
sector,last_20_sessions,lipi individuals | All other Sectors,0.057,2019-02-07
sector,last_20_sessions,lipi individuals | Cement,-0.729,2019-02-07
sector,last_20_sessions,lipi individuals | Commercial Banks,-7.616,2019-02-07
sector,last_20_sessions,lipi individuals | Fertilizer,-2.375,2019-02-07
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,-0.716,2019-02-07
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,5.392,2019-02-07
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,2.424,2019-02-07
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,0.181,2019-02-07
sector,last_20_sessions,lipi individuals | Technology and Communication,-0.172,2019-02-07
sector,last_20_sessions,lipi individuals | Textile Composite,2.041,2019-02-07
sector,last_20_sessions,lipi insurance companies | All other Sectors,3.862,2019-02-07
sector,last_20_sessions,lipi insurance companies | Cement,4.837,2019-02-07
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-3.986,2019-02-07
sector,last_20_sessions,lipi insurance companies | Fertilizer,0.604,2019-02-07
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,-0.051,2019-02-07
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-7.971,2019-02-07
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,1.974,2019-02-07
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,1.167,2019-02-07
sector,last_20_sessions,lipi insurance companies | Technology and Communication,-0.496,2019-02-07
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.928,2019-02-07
sector,last_20_sessions,lipi mutual funds | All other Sectors,-2.433,2019-02-07
sector,last_20_sessions,lipi mutual funds | Cement,0.023,2019-02-07
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-9.847,2019-02-07
sector,last_20_sessions,lipi mutual funds | Fertilizer,-2.003,2019-02-07
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,-0.568,2019-02-07
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-0.955,2019-02-07
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,1.431,2019-02-07
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,0.202,2019-02-07
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-0.074,2019-02-07
sector,last_20_sessions,lipi mutual funds | Textile Composite,-1.314,2019-02-07
sector,last_20_sessions,lipi nbfc | All other Sectors,1.001,2019-02-07
sector,last_20_sessions,lipi nbfc | Cement,-0.731,2019-02-07
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.749,2019-02-07
sector,last_20_sessions,lipi nbfc | Fertilizer,0.039,2019-02-07
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.0,2019-02-07
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.114,2019-02-07
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.448,2019-02-07
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,-0.015,2019-02-07
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.026,2019-02-07
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.264,2019-02-07
sector,last_20_sessions,lipi other organization | All other Sectors,0.141,2019-02-07
sector,last_20_sessions,lipi other organization | Cement,-1.183,2019-02-07
sector,last_20_sessions,lipi other organization | Commercial Banks,-2.308,2019-02-07
sector,last_20_sessions,lipi other organization | Fertilizer,0.883,2019-02-07
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,1.485,2019-02-07
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,1.295,2019-02-07
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.882,2019-02-07
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,0.169,2019-02-07
sector,last_20_sessions,lipi other organization | Technology and Communication,0.16,2019-02-07
sector,last_20_sessions,lipi other organization | Textile Composite,0.028,2019-02-07

=== FILE: calendar.md ===
# Calendar as of 2019-02-08

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2019-01-10 NRL: Board Meeting
- 2019-01-14 ISL: BOARD MEETING FOR THE PERIOD ENDED 31-12-2018
- 2019-01-15 TREET: Board Meeting
- 2019-01-17 INIL: BOARD MEETING FOR THE PERIOD ENDED 31-12-2018
- 2019-01-21 LUCK: BOARD MEETING
- 2019-01-22 TREET: Board Meeting
- 2019-01-22 EPCL: Board Meeting & Closed Period
- 2019-01-28 FCCL: Notice for Board Meeting
- 2019-01-28 EFERT: BOARD MEETING & CLOSED PERIOD
- 2019-02-01 STCL: Board Meeting
- 2019-02-01 NETSOL: Board Meeting
- 2019-02-04 CHCC: NOTICE OF BOARD OF DIRECTORS MEETING & NOTICE OF CLOSED PERIOD
- 2019-02-06 LOTCHEM: Board Meeting / Closed Period
- 2019-02-08 SSGC: BOARD MEETING
- 2019-02-08 HUBC: Board Meeting
- 2019-02-08 PSO: Board Meeting
- 2019-02-08 GHNI: Board Meeting

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

=== FILE: situations.md ===
(no situation-library entry has an outcome that closed before this date, or the library has no INDEX.md)

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
