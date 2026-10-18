# Replay bundle, close of 2019-03-08

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
# Market as of 2019-03-08 close (public information only)

- KSE100: 38,950 on 2019-03-08; 1m -5.8%, 3m +1.0%, 6m -5.6%, 12m -9.9%
- KMI All Share: 18,919 on 2019-03-08; 1m -5.5%, 3m +0.6%, 6m -7.0%, 12m -10.8%
- Policy rate 10.25%; last MPC decision 2019-01-31: hike (+25bp)
- 6M T-bill cutoff 10.60% (auction 2019-02-13); 3M 10.55%, 12M nan%
- CPI YoY 8.22% for 2019-02 (published by 2019-03-03); three months earlier (2018-11) 6.5%
- Brent: 65.66 USD/bbl on 2019-03-08; 3-month change +6.4%
- USD/PKR: 138.53  on 2019-03-08; 3-month change +0.1%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.35pp (market near policy rate); CPI rising over 3 months (+1.7pp)
- Next MPC: see SBP calendar

Session date used: 2019-03-08. Liquid KMI names: 43 (membership KMI_ALL_derived_2019-01-28.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.1483,-0.1909,-0.344,0,0
E&P,3,-0.0339,0.0379,-0.0657,0,0
OMC,4,-0.1225,-0.0415,-0.2375,0,0
Power,4,-0.0267,0.0156,-0.0357,0,0
Fertilizer,4,-0.0288,0.0206,0.0438,0,0
Cement,16,-0.0958,-0.0809,-0.1474,0,0
Steel & engineering,10,-0.1201,-0.0658,-0.3038,0,0
Autos,11,-0.1121,-0.108,-0.3119,0,0
Tech & telecom,6,-0.093,-0.0894,-0.223,0,0
Islamic banks & fin.,7,-0.0051,-0.0144,-0.0943,1,1
Pharma,11,-0.0533,0.0222,-0.1627,0,0
Textiles,16,-0.0739,-0.0392,-0.0174,0,0
Food & staples,12,-0.0498,-0.0455,-0.1693,0,0
Chemicals,16,-0.0913,-0.0648,-0.0659,0,0
"Glass, packaging, paper",12,-0.0769,-0.0033,-0.1152,0,0
Gas utilities & misc,10,-0.0389,0.0176,-0.108,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,n_results,n_material,n_insider_buy,n_insider_sell
AGP,81.27,-0.093,0.029,-0.086,,-0.242,0.517,0,2,0,0,0
ASTL,41.08,-0.242,-0.21,-0.44,-0.554,-0.575,0.934,0,2,0,0,0
ATRL,117.77,-0.152,-0.29,-0.286,-0.405,-0.478,1.036,0,1,0,0,0
CHCC,67.56,-0.077,-0.063,-0.164,-0.465,-0.514,0.617,0,2,0,0,0
DCL,11.67,-0.161,-0.123,-0.185,-0.545,-0.59,0.485,0,2,0,0,0
DGKC,89.67,-0.03,-0.001,-0.163,-0.376,-0.477,0.838,0,2,0,0,0
EFERT,73.99,-0.054,-0.003,-0.047,0.07,-0.108,0.613,0,2,0,0,0
EPCL,36.75,-0.056,-0.001,0.103,0.246,-0.122,0.495,0,0,0,0,0
FCCL,21.06,-0.065,-0.071,-0.131,-0.156,-0.339,1.019,0,2,0,0,0
FCEPL,73.26,-0.167,-0.106,-0.147,-0.165,-0.307,1.894,0,0,0,0,0
FEROZ,200.47,-0.071,0.251,-0.008,-0.123,-0.233,2.035,0,2,0,0,0
FML,103.33,0.101,0.195,0.506,0.751,-0.164,0.596,0,2,0,0,0
GAL,87.49,-0.145,-0.185,-0.4,-0.551,-0.676,1.192,0,0,0,0,0
GHNI,202.03,-0.144,-0.191,-0.382,-0.462,-0.53,2.729,0,2,0,0,0
HUBC,83.27,-0.118,-0.077,-0.079,-0.151,-0.206,0.769,0,2,0,0,0
INIL,138.03,-0.15,-0.087,-0.372,-0.551,-0.549,0.555,0,1,0,0,0
ISL,64.9,-0.159,-0.097,-0.369,-0.461,-0.488,0.778,0,1,0,0,0
KEL,6.01,-0.074,0.087,0.101,-0.032,-0.155,0.765,0,0,0,0,0
KOHC,87.26,-0.003,-0.01,0.012,-0.154,-0.271,1.084,0,3,0,0,0
LOTCHEM,14.78,-0.154,-0.198,0.106,0.672,-0.26,0.648,0,1,0,0,0
LUCK,459.95,-0.074,-0.02,-0.123,-0.234,-0.364,0.757,0,1,0,0,0
MARI,1298.32,-0.011,-0.02,-0.146,-0.118,-0.186,0.594,0,2,0,0,0
MEBL,101.58,0.061,0.065,0.202,0.49,0.0,0.951,0,2,0,0,0
MLCF,40.84,-0.13,-0.076,-0.244,-0.395,-0.483,0.816,0,3,0,0,0
NETSOL,81.62,-0.097,-0.145,-0.481,-0.009,-0.505,0.783,0,2,0,0,0
NML,137.98,-0.055,0.01,0.026,-0.135,-0.152,0.517,0,2,0,0,0
NRL,189.2,-0.216,-0.274,-0.473,-0.557,-0.58,0.827,0,1,0,0,0
OGDC,145.08,-0.031,0.034,-0.047,-0.111,-0.182,1.312,0,2,0,0,0
PAEL,23.58,-0.166,-0.05,-0.283,-0.518,-0.525,0.58,0,0,0,0,0
PIBTL,10.41,-0.155,-0.061,-0.14,-0.365,-0.455,0.892,0,2,0,0,0
PIOC,39.08,-0.156,-0.088,-0.094,-0.402,-0.465,0.454,0,2,0,0,0
POWER,7.84,-0.051,0.043,-0.043,-0.136,-0.237,0.546,0,2,0,0,0
PPL,178.1,-0.06,0.096,-0.012,0.012,-0.081,1.076,0,2,0,0,0
PRL,22.59,-0.088,-0.091,-0.392,-0.396,-0.492,0.547,0,1,1,0,0
PSO,221.26,-0.087,-0.059,-0.178,-0.071,-0.22,0.903,0,3,1,0,0
SEARL,247.27,-0.103,0.015,-0.212,-0.316,-0.333,1.644,0,2,0,0,0
SNGP,73.59,-0.148,-0.05,-0.224,-0.361,-0.378,0.851,0,1,0,0,0
SPL,22.5,-0.18,-0.305,-0.047,0.4,-0.441,0.274,0,2,0,0,0
SSGC,22.6,-0.102,-0.013,-0.227,-0.367,-0.41,0.733,0,1,0,0,0
STCL,13.86,-0.165,-0.187,-0.345,-0.075,-0.497,0.426,0,2,0,0,0
TGL,100.67,-0.023,0.189,0.044,-0.069,-0.159,1.474,0,2,0,0,0
UNITY,17.06,-0.313,-0.418,-0.568,-0.287,-0.62,0.676,0,2,1,0,0
WAFI,258.52,-0.169,0.073,-0.147,-0.192,-0.339,0.371,0,0,0,0,0

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2019-02-12,UNITY,material_info,Material Information
2019-02-12,LOADS,material_info,Material Information
2019-02-14,AGL,material_info,Material Information
2019-02-15,SERF,material_info,Material Information
2019-02-18,GASF,material_info,Material Information
2019-02-19,HSM,material_info,Material Information REVOKED
2019-02-19,HSM,material_info,Material Information
2019-02-19,SJTM,material_info,"Material Information - Land, Building and Other Assets Sale"
2019-02-21,SAZEW,material_info,Material Information
2019-02-22,BHAT,material_info,Material Information
2019-02-22,FASM,material_info,Material Information
2019-02-22,BTL,material_info,Material Information
2019-02-25,INDU,material_info,Material Information - Change of Director
2019-02-26,SBL,material_info,Material Information
2019-02-26,RAVT,material_info,Material Information
2019-02-26,SFLL,material_info,Material Information
2019-02-26,DCL,financial_result,"Financial Results for the Quarter Ended December 31,2018"
2019-02-26,INIL,financial_result,FINANCIAL RESULTS FOR THE HALF YEAR ENDED 31-12-2018
2019-02-26,DGKC,financial_result,"FINANCIAL RESULTS FOR THE HALF YEAR ENDED DECEMBER 31, 2018 (UN-AUDITED)"
2019-02-26,PIOC,financial_result,Financial results for quarter ended
2019-02-27,SFL,material_info,Material Information
2019-02-27,HSM,material_info,Material Information
2019-02-27,AKZO,material_info,Material Information
2019-02-27,GHNI,financial_result,"Transmission of Quarterly Report for the period ended December 31, 2018"
2019-02-27,SPL,financial_result,Transmission of Half yearly Report for the period ended 31.12.2018
2019-02-27,CHCC,financial_result,"Transmission of Quarterly Report for the period ended December 31, 2018"
2019-02-27,TGL,financial_result,Financial Results for the 2nd Quarter and Six Months ended 31-12-2018
2019-02-27,UNITY,financial_result,"Financial Results for the Half Year Ended December 31, 2018"
2019-02-27,MLCF,financial_result,Transmission of Quarterly Report for the Period Ended 31.12.2018 REVOKED
2019-02-28,ASTL,financial_result,Financial Results for the Half Year Ended 31 December 2018
2019-02-28,DCL,financial_result,"Transimission of Quarterly Report for the Period Ended December 31,2018"
2019-02-28,MLCF,financial_result,Transmission of Quarterly Report for the Period Ended 31.12.2018
2019-02-28,KOHC,financial_result,"Transmission of Quarterly Report for the Period Ended December 21, 2018 REV"
2019-02-28,HUBC,financial_result,"Dispatch of Quarterly Accounts for the period Ended Dec 31, 2018"
2019-02-28,NML,financial_result,"TRANSMISSION OF FINNACIAL STATEMENTS FOR THE HALF YEAR ENDED DECEMBER 31, 2"
2019-02-28,KOHC,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2018"
2019-02-28,DGKC,financial_result,"TRANSMISSION OF FINANCIAL STATEMENT FOR THE HALF YEAR ENDED DECEMBER 31, 20"
2019-02-28,MARI,financial_result,Transmission of Interim Financial Statements for the Six Months Ended Decem
2019-02-28,OGDC,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2018"
2019-02-28,PPL,financial_result,Financial Results for the half year ended 31 December 2018
2019-02-28,FCCL,financial_result,Transmission of Half Yearly Report for the Period Ended 31st December 2018
2019-02-28,TGL,financial_result,Transmission of Quarterly Report for the Period Ended 31 December 2018
2019-02-28,PSO,financial_result,"Transmission of Half Yearly Report for the period ended December 31, 2018"
2019-02-28,POWER,financial_result,FINANCIAL RESULTS FOR THE SIX MONTHS PERIOD AND QUARTER ENDED 31 DECEMBER 2
2019-02-28,PIBTL,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2018"
2019-02-28,SEARL,financial_result,Financial Results for the Quarter Ended 2018-12-31
2019-02-28,FEROZ,financial_result,Transmission of Quarterly Report for the Period Ended 2018-12-31
2019-02-28,POWER,financial_result,TRANSMISSION OF QUARTERLY REPORT FOR THE SIX MONTHS PERIOD ENDED 31 DECEMBE
2019-02-28,ASTL,financial_result,Transmission of Half Yearly Report for the Period Ended 31 December 2018
2019-03-01,AASM,material_info,Material Information
2019-03-01,ICIBL,material_info,MATERIAL INFORMATION - RESIGNATION BY DIRECTOR
2019-03-01,PRL,material_info,Material Information - Project
2019-03-01,PIOC,financial_result,Transmission of Quarterly Accounts for the period ended 31 December 2018
2019-03-01,PPL,financial_result,Half Yearly Report for 31 December 2018
2019-03-01,SEARL,financial_result,Transmission of Quarterly Report for the Period Ended 2018-12-31
2019-03-01,UNITY,financial_result,"Transmission of Half Yearly Report for the Period Ended December 31, 2018"
2019-03-04,PMPK,material_info,Material Information
2019-03-04,PSO,material_info,Material Information
2019-03-05,BAFL,material_info,Material Information - Update on Sale of Afghanistan Operations
2019-03-05,GGL,material_info,Material Information - Ghani Gases Limited
2019-03-05,HASCOL,material_info,Material Information
2019-03-05,PRL,financial_result,Transmission of Quarterly Report(Half Year) - 31 December 2018
2019-03-05,AGP,financial_result,"Financial Results for the year ending December 31, 2018 REVOKED"
2019-03-06,AGP,financial_result,"Financial Results for the year ended December 31, 2018"
2019-03-06,MEBL,financial_result,Annual report 2018-12-31
2019-03-06,EFERT,financial_result,Transmission of Annual Report for the Year Ended 2018
2019-03-08,HASCOL,material_info,Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-1.599,2019-03-07
investor_type,last_5_sessions,broker proprietary trading,1.571,2019-03-07
investor_type,last_5_sessions,companies,4.418,2019-03-07
investor_type,last_5_sessions,foreign corporates,-5.579,2019-03-07
investor_type,last_5_sessions,foreign individual,0.339,2019-03-07
investor_type,last_5_sessions,individuals,5.881,2019-03-07
investor_type,last_5_sessions,insurance companies,6.553,2019-03-07
investor_type,last_5_sessions,mutual funds,-10.877,2019-03-07
investor_type,last_5_sessions,nbfc,0.027,2019-03-07
investor_type,last_5_sessions,other organization,-0.037,2019-03-07
investor_type,last_5_sessions,overseas pakistani,-0.698,2019-03-07
sector,last_5_sessions,fipi | All other Sectors,0.521,2019-03-07
sector,last_5_sessions,fipi | Cement,0.15,2019-03-07
sector,last_5_sessions,fipi | Commercial Banks,-3.398,2019-03-07
sector,last_5_sessions,fipi | Fertilizer,0.318,2019-03-07
sector,last_5_sessions,fipi | Food and Personal Care Products,-0.056,2019-03-07
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-3.141,2019-03-07
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,-0.18,2019-03-07
sector,last_5_sessions,fipi | Power Generation and Distribution,0.087,2019-03-07
sector,last_5_sessions,fipi | Technology and Communication,0.097,2019-03-07
sector,last_5_sessions,fipi | Textile Composite,-0.334,2019-03-07
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-0.744,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Cement,-0.562,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,0.517,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-0.294,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-0.104,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.567,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-0.299,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.08,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,-0.027,2019-03-07
sector,last_5_sessions,lipi banks / dfi | Textile Composite,-0.731,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-0.34,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.247,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.137,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,-0.013,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.163,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,1.149,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.017,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.097,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,0.131,2019-03-07
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,0.176,2019-03-07
sector,last_5_sessions,lipi companies | All other Sectors,-0.375,2019-03-07
sector,last_5_sessions,lipi companies | Cement,-0.449,2019-03-07
sector,last_5_sessions,lipi companies | Commercial Banks,6.418,2019-03-07
sector,last_5_sessions,lipi companies | Fertilizer,0.05,2019-03-07
sector,last_5_sessions,lipi companies | Food and Personal Care Products,-0.169,2019-03-07
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,-0.055,2019-03-07
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,0.222,2019-03-07
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.153,2019-03-07
sector,last_5_sessions,lipi companies | Technology and Communication,-0.053,2019-03-07
sector,last_5_sessions,lipi companies | Textile Composite,-1.018,2019-03-07
sector,last_5_sessions,lipi individuals | All other Sectors,0.586,2019-03-07
sector,last_5_sessions,lipi individuals | Cement,2.169,2019-03-07
sector,last_5_sessions,lipi individuals | Commercial Banks,-1.739,2019-03-07
sector,last_5_sessions,lipi individuals | Fertilizer,-0.309,2019-03-07
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,-0.22,2019-03-07
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,4.386,2019-03-07
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,0.24,2019-03-07
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.534,2019-03-07
sector,last_5_sessions,lipi individuals | Technology and Communication,-0.429,2019-03-07
sector,last_5_sessions,lipi individuals | Textile Composite,0.662,2019-03-07
sector,last_5_sessions,lipi insurance companies | All other Sectors,5.619,2019-03-07
sector,last_5_sessions,lipi insurance companies | Cement,0.686,2019-03-07
sector,last_5_sessions,lipi insurance companies | Commercial Banks,0.998,2019-03-07
sector,last_5_sessions,lipi insurance companies | Fertilizer,0.282,2019-03-07
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.455,2019-03-07
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-2.114,2019-03-07
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-0.083,2019-03-07
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,-0.34,2019-03-07
sector,last_5_sessions,lipi insurance companies | Technology and Communication,0.02,2019-03-07
sector,last_5_sessions,lipi insurance companies | Textile Composite,1.03,2019-03-07
sector,last_5_sessions,lipi mutual funds | All other Sectors,-5.837,2019-03-07
sector,last_5_sessions,lipi mutual funds | Cement,-1.527,2019-03-07
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-2.132,2019-03-07
sector,last_5_sessions,lipi mutual funds | Fertilizer,-0.189,2019-03-07
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,-0.072,2019-03-07
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-1.12,2019-03-07
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.25,2019-03-07
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.159,2019-03-07
sector,last_5_sessions,lipi mutual funds | Technology and Communication,0.305,2019-03-07
sector,last_5_sessions,lipi mutual funds | Textile Composite,0.105,2019-03-07
sector,last_5_sessions,lipi nbfc | All other Sectors,0.168,2019-03-07
sector,last_5_sessions,lipi nbfc | Cement,-0.176,2019-03-07
sector,last_5_sessions,lipi nbfc | Commercial Banks,-0.237,2019-03-07
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.008,2019-03-07
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,-0.0,2019-03-07
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.0,2019-03-07
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.285,2019-03-07
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.001,2019-03-07
sector,last_5_sessions,lipi nbfc | Textile Composite,-0.003,2019-03-07
sector,last_5_sessions,lipi other organization | All other Sectors,0.402,2019-03-07
sector,last_5_sessions,lipi other organization | Cement,-0.539,2019-03-07
sector,last_5_sessions,lipi other organization | Commercial Banks,-0.564,2019-03-07
sector,last_5_sessions,lipi other organization | Fertilizer,0.162,2019-03-07
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,0.003,2019-03-07
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,0.328,2019-03-07
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.048,2019-03-07
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.05,2019-03-07
sector,last_5_sessions,lipi other organization | Technology and Communication,-0.043,2019-03-07
sector,last_5_sessions,lipi other organization | Textile Composite,0.114,2019-03-07
investor_type,last_20_sessions,banks / dfi,9.692,2019-03-07
investor_type,last_20_sessions,broker proprietary trading,-9.964,2019-03-07
investor_type,last_20_sessions,companies,1.457,2019-03-07
investor_type,last_20_sessions,foreign corporates,12.809,2019-03-07
investor_type,last_20_sessions,foreign individual,0.373,2019-03-07
investor_type,last_20_sessions,individuals,4.365,2019-03-07
investor_type,last_20_sessions,insurance companies,17.611,2019-03-07
investor_type,last_20_sessions,mutual funds,-36.13,2019-03-07
investor_type,last_20_sessions,nbfc,-0.402,2019-03-07
investor_type,last_20_sessions,other organization,-0.529,2019-03-07
investor_type,last_20_sessions,overseas pakistani,0.719,2019-03-07
sector,last_20_sessions,fipi | All other Sectors,3.694,2019-03-07
sector,last_20_sessions,fipi | Cement,9.978,2019-03-07
sector,last_20_sessions,fipi | Commercial Banks,-0.241,2019-03-07
sector,last_20_sessions,fipi | Fertilizer,1.843,2019-03-07
sector,last_20_sessions,fipi | Food and Personal Care Products,-0.38,2019-03-07
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-1.014,2019-03-07
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,0.48,2019-03-07
sector,last_20_sessions,fipi | Power Generation and Distribution,-0.917,2019-03-07
sector,last_20_sessions,fipi | Technology and Communication,0.647,2019-03-07
sector,last_20_sessions,fipi | Textile Composite,-0.189,2019-03-07
sector,last_20_sessions,lipi banks / dfi | All other Sectors,1.043,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Cement,-0.302,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,2.7,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Fertilizer,2.36,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.142,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,4.772,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.518,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-1.306,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,0.242,2019-03-07
sector,last_20_sessions,lipi banks / dfi | Textile Composite,-0.478,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-1.641,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Cement,-2.622,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,-3.264,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-0.2,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.321,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-1.597,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.215,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.295,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-0.22,2019-03-07
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.821,2019-03-07
sector,last_20_sessions,lipi companies | All other Sectors,-2.779,2019-03-07
sector,last_20_sessions,lipi companies | Cement,0.768,2019-03-07
sector,last_20_sessions,lipi companies | Commercial Banks,6.517,2019-03-07
sector,last_20_sessions,lipi companies | Fertilizer,0.598,2019-03-07
sector,last_20_sessions,lipi companies | Food and Personal Care Products,-0.068,2019-03-07
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,-1.206,2019-03-07
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,0.179,2019-03-07
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-0.394,2019-03-07
sector,last_20_sessions,lipi companies | Technology and Communication,0.006,2019-03-07
sector,last_20_sessions,lipi companies | Textile Composite,-2.163,2019-03-07
sector,last_20_sessions,lipi individuals | All other Sectors,7.187,2019-03-07
sector,last_20_sessions,lipi individuals | Cement,-2.338,2019-03-07
sector,last_20_sessions,lipi individuals | Commercial Banks,-3.831,2019-03-07
sector,last_20_sessions,lipi individuals | Fertilizer,-2.15,2019-03-07
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,-1.715,2019-03-07
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,2.278,2019-03-07
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.09,2019-03-07
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,3.236,2019-03-07
sector,last_20_sessions,lipi individuals | Technology and Communication,-0.918,2019-03-07
sector,last_20_sessions,lipi individuals | Textile Composite,2.706,2019-03-07
sector,last_20_sessions,lipi insurance companies | All other Sectors,10.637,2019-03-07
sector,last_20_sessions,lipi insurance companies | Cement,1.182,2019-03-07
sector,last_20_sessions,lipi insurance companies | Commercial Banks,1.285,2019-03-07
sector,last_20_sessions,lipi insurance companies | Fertilizer,1.789,2019-03-07
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,2.004,2019-03-07
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-3.214,2019-03-07
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,1.105,2019-03-07
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,1.116,2019-03-07
sector,last_20_sessions,lipi insurance companies | Technology and Communication,0.172,2019-03-07
sector,last_20_sessions,lipi insurance companies | Textile Composite,1.534,2019-03-07
sector,last_20_sessions,lipi mutual funds | All other Sectors,-18.361,2019-03-07
sector,last_20_sessions,lipi mutual funds | Cement,-5.259,2019-03-07
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-1.628,2019-03-07
sector,last_20_sessions,lipi mutual funds | Fertilizer,-5.13,2019-03-07
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,-0.307,2019-03-07
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-1.28,2019-03-07
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-1.607,2019-03-07
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-1.645,2019-03-07
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-0.124,2019-03-07
sector,last_20_sessions,lipi mutual funds | Textile Composite,-0.79,2019-03-07
sector,last_20_sessions,lipi nbfc | All other Sectors,0.172,2019-03-07
sector,last_20_sessions,lipi nbfc | Cement,-0.652,2019-03-07
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.641,2019-03-07
sector,last_20_sessions,lipi nbfc | Fertilizer,0.025,2019-03-07
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.025,2019-03-07
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.118,2019-03-07
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.347,2019-03-07
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.014,2019-03-07
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.178,2019-03-07
sector,last_20_sessions,lipi nbfc | Textile Composite,0.011,2019-03-07
sector,last_20_sessions,lipi other organization | All other Sectors,0.048,2019-03-07
sector,last_20_sessions,lipi other organization | Cement,-0.755,2019-03-07
sector,last_20_sessions,lipi other organization | Commercial Banks,-0.896,2019-03-07
sector,last_20_sessions,lipi other organization | Fertilizer,0.864,2019-03-07
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-0.023,2019-03-07
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,1.142,2019-03-07
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.719,2019-03-07
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,-0.399,2019-03-07
sector,last_20_sessions,lipi other organization | Technology and Communication,0.017,2019-03-07
sector,last_20_sessions,lipi other organization | Textile Composite,0.191,2019-03-07

=== FILE: calendar.md ===
# Calendar as of 2019-03-08

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2019-02-08 SSGC: BOARD MEETING
- 2019-02-08 HUBC: Board Meeting
- 2019-02-08 PSO: Board Meeting
- 2019-02-08 GHNI: Board Meeting
- 2019-02-11 MARI: Notice of Board of Directors Meeting
- 2019-02-12 MLCF: Board Meeting
- 2019-02-12 UNITY: Board Meeting
- 2019-02-12 PIBTL: NOTICE OF PIBT BOARD MEETING - FEBRUARY 19, 2019
- 2019-02-13 MEBL: Notice of Board Meeting and Closed Period
- 2019-02-13 FML: Board Meeting
- 2019-02-13 SPL: Board Meeting
- 2019-02-14 OGDC: Board meeting and close period
- 2019-02-14 KOHC: Board Meeting
- 2019-02-15 FEROZ: Board Meeting
- 2019-02-18 DGKC: BOARD MEETING
- 2019-02-18 DCL: Board Meeting
- 2019-02-19 NML: BOARD MEETING
- 2019-02-19 PPL: Meeting of the Board of Directors and Closed Period
- 2019-02-19 PIOC: Board Meeting
- 2019-02-20 UNITY: Board Meeting
- 2019-02-21 POWER: BOARD MEETING
- 2019-02-21 TGL: Board Meeting
- 2019-02-21 FCCL: Presentation of Trades Executed by Directors in the Board of Directors Meeting
- 2019-02-21 SEARL: Board Meeting

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
