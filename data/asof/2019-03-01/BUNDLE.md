# Replay bundle, close of 2019-03-01

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
# Market as of 2019-03-01 close (public information only)

- KSE100: 39,539 on 2019-03-01; 1m -2.6%, 3m -2.4%, 6m -5.6%, 12m -7.9%
- KMI All Share: 19,297 on 2019-03-01; 1m -1.5%, 3m -2.0%, 6m -6.6%, 12m -9.2%
- Policy rate 10.25%; last MPC decision 2019-01-31: hike (+25bp)
- 6M T-bill cutoff 10.60% (auction 2019-02-13); 3M 10.55%, 12M nan%
- CPI YoY 7.2% for 2019-01 (published by 2019-02-03); three months earlier (2018-10) 6.78%
- Brent: 63.71 USD/bbl on 2019-03-01; 3-month change +10.4%
- USD/PKR: 138.47  on 2019-03-01; 3-month change +0.2%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.35pp (market near policy rate); CPI rising over 3 months (+0.4pp)
- Next MPC: see SBP calendar

Session date used: 2019-03-01. Liquid KMI names: 45 (membership KMI_ALL_derived_2019-01-28.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.135,-0.2469,-0.3807,0,0
E&P,3,-0.0007,0.0327,-0.0317,0,0
OMC,4,-0.0721,-0.1008,-0.2281,0,0
Power,5,-0.0032,0.0293,0.0164,0,0
Fertilizer,4,-0.019,-0.009,0.0302,0,1
Cement,16,-0.0289,-0.1023,-0.1542,0,0
Steel & engineering,10,-0.0692,-0.1215,-0.3289,0,0
Autos,12,-0.0792,-0.1617,-0.3111,0,0
Tech & telecom,6,-0.05,-0.1232,-0.2251,0,0
Islamic banks & fin.,8,-0.0095,-0.0617,-0.1241,0,1
Pharma,11,-0.0148,-0.0153,-0.1944,0,0
Textiles,16,-0.0476,-0.0353,0.0038,0,1
Food & staples,11,-0.0373,-0.0819,-0.2246,0,0
Chemicals,17,-0.0469,-0.0857,-0.1347,0,1
"Glass, packaging, paper",12,-0.0411,-0.0406,-0.1446,0,0
Gas utilities & misc,10,-0.0152,-0.0335,-0.1235,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,n_results,n_material,n_insider_buy,n_insider_sell
AGP,88.26,-0.015,0.129,-0.052,,-0.176,0.527,0,0,0,0,0
ASTL,43.41,-0.138,-0.251,-0.429,-0.539,-0.551,1.175,0,2,0,0,0
ATRL,120.32,-0.143,-0.382,-0.314,-0.423,-0.466,1.216,0,1,0,0,0
CHCC,70.54,0.037,-0.103,-0.185,-0.44,-0.492,0.779,0,2,0,0,0
DCL,11.87,-0.202,-0.152,-0.235,-0.553,-0.584,0.737,0,2,0,0,0
DGKC,92.39,0.1,-0.049,-0.203,-0.345,-0.462,1.07,0,2,0,0,0
EFERT,74.3,-0.018,-0.027,-0.045,0.095,-0.104,1.049,0,1,0,0,0
EPCL,37.09,-0.071,-0.029,0.077,0.294,-0.114,0.613,0,1,0,0,0
FCCL,21.2,0.007,-0.066,-0.152,-0.162,-0.335,1.292,0,2,0,0,0
FCEPL,75.28,-0.104,-0.132,-0.155,-0.138,-0.288,2.688,0,0,0,0,0
FEROZ,181.98,0.01,0.077,-0.134,-0.232,-0.304,2.088,0,2,0,0,0
FML,106.39,0.18,0.288,0.504,0.716,-0.139,0.56,0,2,0,0,0
GAL,89.85,-0.074,-0.181,-0.412,-0.52,-0.668,1.372,0,0,0,0,0
GHNI,206.74,-0.12,-0.304,-0.386,-0.381,-0.519,3.06,0,2,0,0,0
HUBC,87.5,-0.059,-0.077,-0.074,-0.09,-0.166,0.954,0,2,0,0,0
INIL,140.94,-0.03,-0.119,-0.367,-0.518,-0.542,1.185,0,1,0,0,0
ISL,66.74,-0.034,-0.149,-0.38,-0.423,-0.473,1.174,0,1,0,0,0
KEL,6.09,-0.042,0.08,0.138,-0.026,-0.144,0.913,0,0,0,0,0
KOHC,90.76,0.078,-0.043,0.016,-0.133,-0.242,1.542,0,3,0,0,0
LOTCHEM,14.54,-0.134,-0.229,-0.01,0.647,-0.272,0.783,0,1,0,0,0
LUCK,469.61,0.004,-0.049,-0.148,-0.207,-0.351,0.952,0,2,0,0,0
MARI,1333.5,-0.006,-0.042,-0.134,-0.135,-0.163,0.738,0,2,0,0,0
MEBL,99.01,0.1,0.028,0.171,0.451,-0.006,1.139,0,1,0,0,0
MLCF,41.65,-0.054,-0.14,-0.23,-0.343,-0.473,0.945,0,3,0,0,0
NETSOL,82.44,-0.052,-0.224,-0.47,0.176,-0.5,0.984,0,2,0,0,0
NML,139.57,-0.014,-0.056,0.032,-0.118,-0.142,0.567,0,2,0,0,0
NRL,198.31,-0.186,-0.323,-0.463,-0.545,-0.559,0.612,0,1,0,0,0
OGDC,153.25,0.02,0.039,-0.001,-0.064,-0.136,1.333,0,2,0,0,0
PAEL,24.26,-0.1,-0.148,-0.309,-0.556,-0.559,0.816,0,0,0,0,0
PIBTL,10.73,-0.086,-0.081,-0.154,-0.393,-0.438,1.185,0,2,0,0,0
PIOC,41.03,-0.06,-0.167,-0.135,-0.368,-0.438,0.537,0,2,0,0,0
PKGS,370.98,0.02,-0.048,-0.199,-0.306,-0.372,1.438,0,0,0,0,0
POWER,7.87,-0.009,0.004,-0.08,-0.146,-0.234,0.841,0,2,0,0,0
PPL,186.0,-0.018,0.099,0.034,0.085,-0.04,1.195,0,1,0,0,0
PRL,22.1,-0.131,-0.183,-0.458,-0.418,-0.503,0.516,0,1,0,0,0
PSO,229.42,-0.06,-0.146,-0.172,-0.04,-0.191,1.07,0,3,0,0,0
SEARL,255.57,0.008,-0.01,-0.206,-0.296,-0.311,1.778,0,1,0,0,0
SNGP,74.58,-0.107,-0.064,-0.226,-0.339,-0.37,1.072,0,1,0,0,0
SPL,22.9,-0.153,-0.334,-0.154,0.316,-0.431,0.334,0,2,0,0,0
SSGC,21.65,-0.125,-0.106,-0.269,-0.384,-0.435,0.731,0,1,0,0,0
STCL,13.72,-0.172,-0.263,-0.461,-0.064,-0.502,0.433,0,2,0,0,0
TGL,105.36,0.082,0.166,0.035,0.003,-0.119,1.606,0,2,0,0,0
UNITY,18.84,-0.222,-0.382,-0.554,-0.232,-0.58,0.661,0,1,1,0,0
WAFI,299.72,-0.015,0.125,-0.013,-0.105,-0.234,1.128,0,0,0,0,0
WAVES,25.74,-0.05,-0.145,-0.284,-0.284,-0.375,0.64,0,0,0,0,0

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2019-01-30,ARCTM,material_info,DISCLOSURE OF MATERIAL INFORMATION
2019-01-30,PRL,financial_result,Financial Results For Six Months Period Ended 31st December 2018
2019-01-31,ANL,material_info,Material Information - Approval of Creditors' Led Scheme of Arrangement
2019-01-31,LUCK,financial_result,"Financial Results for the quarter ended December 31, 2018"
2019-01-31,EPCL,financial_result,"Financial Results for the Year Ended December 31, 2018 Consolidated And Sta"
2019-01-31,ECOP,insider_trade,Insider trade disclosure
2019-01-31,ECOP,insider_trade,Insider trade disclosure
2019-01-31,KOSM,insider_trade,Insider trade disclosure
2019-01-31,MARI,other,Transfer Notice for Divestment of GoP Shares in MPCL
2019-01-31,POWER,other,"PROJECT PROGRESS REPORT FOR THE QUARTER ENDED DECEMBER 31, 2018"
2019-02-01,ABL,insider_trade,Insider trade disclosure
2019-02-01,HINOON,insider_trade,Insider trade disclosure
2019-02-01,ECOP,insider_trade,Insider trade disclosure
2019-02-01,FCCL,insider_trade,Insider trade disclosure
2019-02-01,STPL,insider_trade,Insider trade disclosure
2019-02-01,STPL,insider_trade,Insider trade disclosure
2019-02-01,BAFL,insider_trade,Insider trade disclosure
2019-02-04,MUREB,insider_trade,Insider trade disclosure
2019-02-04,ECOP,insider_trade,Insider trade disclosure
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
2019-02-06,EFERT,other,Analyst Briefing for 4 Quarter 2018 Business Results of Engro Fertilizers L
2019-02-06,UNITY,agm,Certified Resolutions Passed by the Shareholders of Unity Foods Limited in 
2019-02-07,HINOON,insider_trade,Insider trade disclosure
2019-02-07,HINOON,insider_trade,Insider trade disclosure
2019-02-07,SALT,insider_trade,Insider trade disclosure
2019-02-07,ILTM,insider_trade,Insider trade disclosure
2019-02-08,EFERT,financial_result,"Financial Results for the Year Ended December 31, 2018"
2019-02-08,LUCK,financial_result,"Transmission of half yearly report for the half year ended December 31, 201"
2019-02-08,PKGS,insider_trade,Insider trade disclosure
2019-02-08,PKGS,insider_trade,Insider trade disclosure
2019-02-08,HINOON,insider_trade,Insider trade disclosure
2019-02-08,HINOON,insider_trade,Insider trade disclosure
2019-02-08,BAFL,insider_trade,Insider trade disclosure
2019-02-08,IGIHL,insider_trade,Insider trade disclosure
2019-02-08,BWCL,insider_trade,Insider trade disclosure
2019-02-08,KEL,other,Issue of rated and listed SUKUK of up to PKR 25 billion
2019-02-08,KEL,other,Resignation by Directors
2019-02-11,PKGS,insider_trade,Insider trade disclosure
2019-02-11,BFMOD,insider_trade,Insider trade disclosure
2019-02-11,HINOON,insider_trade,Insider trade disclosure
2019-02-12,UNITY,material_info,Material Information
2019-02-12,LOADS,material_info,Material Information
2019-02-12,HINOON,insider_trade,Insider trade disclosure
2019-02-12,PKGS,insider_trade,Insider trade disclosure
2019-02-12,HINOON,insider_trade,Insider trade disclosure
2019-02-12,LOTCHEM,other,Change of Director / Chairman
2019-02-12,NETSOL,other,"""MEETING IN PROGRESS"" BOARD MEETING DATED FEBRUARY 12, 2019"
2019-02-13,NETSOL,financial_result,Financial Results for the Quarter Ended 2018-12-31
2019-02-13,SSGC,financial_result,"FINANCIAL RESULTS FOR THE QUARTER ENDED 30 SEPTEMBER, 2016, HALF YEAR ENDED"
2019-02-13,NRL,financial_result,"Transmission of Quarterly Reportsfor the Period ended December 31, 2018"
2019-02-13,PKGS,insider_trade,Insider trade disclosure
2019-02-13,NCL,insider_trade,Insider trade disclosure
2019-02-13,CHCC,other,MEETING IN PROGRESS
2019-02-14,AGL,material_info,Material Information
2019-02-14,CHCC,financial_result,"FINANCIAL RESULTS FOR THE HALF YEAR ENDED DECEMBER 31, 2018"
2019-02-14,ATRL,financial_result,TRANSMISSION OF QUARTERLY REPORT FOR THE PERIOD ENDED 2018-12-31
2019-02-14,LOTCHEM,financial_result,Financial Results For the Year Ended 31 December 2018
2019-02-14,PKGS,insider_trade,Insider trade disclosure
2019-02-14,PKGS,insider_trade,Insider trade disclosure
2019-02-14,ANL,insider_trade,Insider trade disclosure
2019-02-14,NCL,insider_trade,Insider trade disclosure
2019-02-14,PSO,other,Change in the Venue of the Board Meeting
2019-02-15,SERF,material_info,Material Information
2019-02-15,BOP,insider_trade,Insider trade disclosure
2019-02-15,HINOON,insider_trade,Insider trade disclosure
2019-02-15,BOP,insider_trade,Insider trade disclosure
2019-02-18,GASF,material_info,Material Information
2019-02-18,PSO,financial_result,"Financial Results for the half year ended December 31, 2018 REVOKED"
2019-02-18,GHNI,financial_result,"Financial Results for the Half Year ended December 31, 2018"
2019-02-18,ISL,financial_result,TRANSMISSION OF HALF YEARLY FINANCIAL STATEMENTS FOR THE PERIOD ENDED 31-12
2019-02-18,STCL,financial_result,Financial Results for the 2nd Quarter and Half Year Ended 2018-12-31
2019-02-18,FCCL,financial_result,Financial Result for the quarter ended 2018-12-31
2019-02-18,MTL,insider_trade,Insider trade disclosure
2019-02-18,MTL,insider_trade,Insider trade disclosure
2019-02-18,PKGS,insider_trade,Insider trade disclosure
2019-02-18,HINOON,insider_trade,Insider trade disclosure
2019-02-18,AVN,insider_trade,Insider trade disclosure
2019-02-18,ZIL,insider_trade,Disclosure of interest by a Director under clause 5.6.1 (d) of PSX Rule Boo
2019-02-19,HSM,material_info,Material Information REVOKED
2019-02-19,HSM,material_info,Material Information
2019-02-19,SJTM,material_info,"Material Information - Land, Building and Other Assets Sale"
2019-02-19,PSO,financial_result,"Financial Results for the half year ended December 31, 2018"
2019-02-19,UNITY,dividend_or_bonus,Declaration of Right Shares
2019-02-19,MTL,insider_trade,Insider trade disclosure
2019-02-19,MTL,insider_trade,Insider trade disclosure
2019-02-19,HINOON,insider_trade,Insider trade disclosure
2019-02-19,SSGC,other,Appointment of Director
2019-02-19,PIBTL,other,"PIBT BOD MEETING IN PROGRESS FRBRUARY 19, 2019"
2019-02-19,SSGC,agm,CERTIFIED RESOLUTIONS PASSED IN THE 63RD ANNUAL GENERAL MEETING (AGM) OF SU
2019-02-19,SSGC,agm,CERTIFIED RESOLUTIONS PASSED IN THE 63RD ANNUAL GENERAL MEETING (AGM) OF SU
2019-02-20,PIBTL,financial_result,"FINANCIAL RESULTS FOR THE PERIOD ENDED DECEMBER 31, 2018"
2019-02-20,SNGP,financial_result,APPLICATION FOR EXTENSION IN THE PERIOD FOR SUBMISSION OF HALF YEARLY ACCOU
2019-02-20,MLCF,financial_result,Financial Results for the Quarter Ended 31.12.2018
2019-02-20,MARI,financial_result,"Financial results for the six months ended December 31, 2018"
2019-02-20,SPL,financial_result,Financial results for the Quarter Ended 31-12-2018
2019-02-20,PKGS,insider_trade,Insider trade disclosure
2019-02-20,MTL,insider_trade,Insider trade disclosure
2019-02-20,NCL,insider_trade,Insider trade disclosure
2019-02-20,ASTL,other,Board of Directors' Meeting
2019-02-20,MARI,other,Acquisition of Two New Exploration Blocks
2019-02-20,PIBTL,other,CHANGE OF COMPANY SECRETARY OF PAKISTAN INTERNATIONAL BULK TERMINAL LIMITED
2019-02-21,SAZEW,material_info,Material Information
2019-02-21,MEBL,financial_result,"Financial Results For the Year Ended December 31, 2018"
2019-02-21,KOHC,financial_result,"Financial Results for the Quarter Ended December 31, 2018"
2019-02-21,HUBC,financial_result,"FINANCIAL RESULTS FOR THE HALF YEAR ENDED DECEMBER 31, 2018"
2019-02-21,UNITY,dividend_or_bonus,Right Issue -Copy of Advertisement
2019-02-21,ARCTM,insider_trade,BOOK CLOSURE REQUIRED UNDER THE LISTED COMPANIES (SUBSTANTIAL ACQUISITION O
2019-02-21,PSEL,insider_trade,Insider trade disclosure
2019-02-21,MTL,insider_trade,Insider trade disclosure
2019-02-21,ENGRO,insider_trade,Insider trade disclosure
2019-02-21,INIL,other,APPOINTMENT OF DIRECTOR TO FILL THE CASUAL VACANCY
2019-02-21,EFERT,other,CO-OPTION OF NEW DIRECTOR ON THE BOARD OF ENGRO FERTILIZERS LIMITED
2019-02-21,EPCL,agm,NOTICE OF ANNUAL GENERAL MEETING
2019-02-22,BHAT,material_info,Material Information
2019-02-22,FASM,material_info,Material Information
2019-02-22,BTL,material_info,Material Information
2019-02-22,OGDC,financial_result,"FINANCIAL RESULTS FOR THE FINANCIAL FOR THE QUARTER ENDED DECEMBER 31, 2018"
2019-02-22,UBL,insider_trade,Insider trade disclosure
2019-02-22,RAVT,insider_trade,Insider trade disclosure
2019-02-22,GHNI,insider_trade,Insider trade disclosure
2019-02-22,DAWH,insider_trade,Insider trade disclosure
2019-02-22,HTL,insider_trade,Insider trade disclosure
2019-02-22,PSO,other,Restructuring of the Board of Management of Pakistan State Oil Company Limi
2019-02-22,GHNI,other,Appointment of Director
2019-02-25,INDU,material_info,Material Information - Change of Director
2019-02-25,FML,financial_result,"Financial Results for the Quarter/Half Year Ended December 31, 2018"
2019-02-25,FEROZ,financial_result,Financial Result Results for the Quarter Ended 2018-12-31
2019-02-25,STCL,financial_result,Transmission of Quarterly Report for the Period Ended 2018-12-31
2019-02-25,NETSOL,financial_result,Transmission of Quarterly Report for the Period Ended 2018-12-31
2019-02-25,FCCL,dividend_or_bonus,Announcement of Interim Cash Dividend Notice in the Newspapers
2019-02-25,UBL,insider_trade,Insider trade disclosure
2019-02-25,HUBC,other,Resignation of Director
2019-02-25,SSGC,other,MANAGING DIRECTOR/ CHIEF EXECUTIVE OFFICER
2019-02-25,AGP,other,"Annual Board Meeting for the year ended December 31, 2018"
2019-02-26,SBL,material_info,Material Information
2019-02-26,RAVT,material_info,Material Information
2019-02-26,SFLL,material_info,Material Information
2019-02-26,DCL,financial_result,"Financial Results for the Quarter Ended December 31,2018"
2019-02-26,INIL,financial_result,FINANCIAL RESULTS FOR THE HALF YEAR ENDED 31-12-2018
2019-02-26,DGKC,financial_result,"FINANCIAL RESULTS FOR THE HALF YEAR ENDED DECEMBER 31, 2018 (UN-AUDITED)"
2019-02-26,PIOC,financial_result,Financial results for quarter ended
2019-02-26,NML,financial_result,"FINANCIAL RESULTS FOR THE HALF YEAR ENDED DECEMBER 31, 2018 (UN-AUDITED)"
2019-02-26,FML,financial_result,Transmission of Quarterly Report for the Period Ended December 31 2018
2019-02-26,DINT,insider_trade,Insider trade disclosure
2019-02-26,FEROZ,insider_trade,Insider trade disclosure
2019-02-27,SFL,material_info,Material Information
2019-02-27,HSM,material_info,Material Information
2019-02-27,AKZO,material_info,Material Information
2019-02-27,GHNI,financial_result,"Transmission of Quarterly Report for the period ended December 31, 2018"
2019-02-27,SPL,financial_result,Transmission of Half yearly Report for the period ended 31.12.2018
2019-02-27,CHCC,financial_result,"Transmission of Quarterly Report for the period ended December 31, 2018"
2019-02-27,TGL,financial_result,Financial Results for the 2nd Quarter and Six Months ended 31-12-2018
2019-02-27,UNITY,financial_result,"Financial Results for the Half Year Ended December 31, 2018"
2019-02-27,MLCF,financial_result,Transmission of Quarterly Report for the Period Ended 31.12.2018 REVOKED
2019-02-27,BAFL,insider_trade,Insider trade disclosure
2019-02-27,HINOON,insider_trade,Insider trade disclosure
2019-02-27,PKGS,insider_trade,Insider trade disclosure
2019-02-27,DINT,insider_trade,"DISCLOSURE OF INTEREST BY A DIRECTOR CEO, OR EXECUTIVE OF A LISTED COMPANY "
2019-02-27,NICL,insider_trade,Insider trade disclosure
2019-02-27,NRL,insider_trade,Insider trade disclosure
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
2019-02-28,ABL,insider_trade,Insider trade disclosure
2019-02-28,FEROZ,insider_trade,Insider trade disclosure
2019-02-28,CCM,insider_trade,Insider trade disclosure
2019-02-28,MACFL,insider_trade,Insider trade disclosure
2019-02-28,HUMNL,insider_trade,Insider trade disclosure
2019-02-28,INDU,insider_trade,Insider trade disclosure
2019-03-01,AASM,material_info,Material Information
2019-03-01,ICIBL,material_info,MATERIAL INFORMATION - RESIGNATION BY DIRECTOR
2019-03-01,PIOC,financial_result,Transmission of Quarterly Accounts for the period ended 31 December 2018
2019-03-01,GASF,insider_trade,Insider trade disclosure
2019-03-01,HINOON,insider_trade,Insider trade disclosure
2019-03-01,FML,insider_trade,Insider trade disclosure
2019-03-01,JSML,insider_trade,Insider trade disclosure
2019-03-01,EFERT,agm,NOTICE OF THE 10TH ANNUAL GENERAL MEETING OF ENGRO FERTILIZERS LIMITED

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,6.112,2019-02-28
investor_type,last_5_sessions,broker proprietary trading,-4.152,2019-02-28
investor_type,last_5_sessions,companies,3.145,2019-02-28
investor_type,last_5_sessions,foreign corporates,-0.72,2019-02-28
investor_type,last_5_sessions,foreign individual,0.018,2019-02-28
investor_type,last_5_sessions,individuals,-10.148,2019-02-28
investor_type,last_5_sessions,insurance companies,12.308,2019-02-28
investor_type,last_5_sessions,mutual funds,-9.56,2019-02-28
investor_type,last_5_sessions,nbfc,0.776,2019-02-28
investor_type,last_5_sessions,other organization,2.202,2019-02-28
investor_type,last_5_sessions,overseas pakistani,0.019,2019-02-28
sector,last_5_sessions,fipi | All other Sectors,1.025,2019-02-28
sector,last_5_sessions,fipi | Cement,0.719,2019-02-28
sector,last_5_sessions,fipi | Commercial Banks,-1.514,2019-02-28
sector,last_5_sessions,fipi | Fertilizer,-0.514,2019-02-28
sector,last_5_sessions,fipi | Food and Personal Care Products,-0.322,2019-02-28
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-0.253,2019-02-28
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,0.247,2019-02-28
sector,last_5_sessions,fipi | Power Generation and Distribution,-0.291,2019-02-28
sector,last_5_sessions,fipi | Technology and Communication,0.227,2019-02-28
sector,last_5_sessions,fipi | Textile Composite,-0.008,2019-02-28
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-0.924,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Cement,0.179,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,1.083,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Fertilizer,0.852,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,0.363,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,3.86,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.55,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.051,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,0.25,2019-02-28
sector,last_5_sessions,lipi banks / dfi | Textile Composite,-0.153,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-0.663,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Cement,-0.344,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,-0.222,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,-0.167,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.123,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-1.631,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.056,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.11,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,-0.445,2019-02-28
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.969,2019-02-28
sector,last_5_sessions,lipi companies | All other Sectors,-0.206,2019-02-28
sector,last_5_sessions,lipi companies | Cement,1.065,2019-02-28
sector,last_5_sessions,lipi companies | Commercial Banks,1.171,2019-02-28
sector,last_5_sessions,lipi companies | Fertilizer,0.91,2019-02-28
sector,last_5_sessions,lipi companies | Food and Personal Care Products,0.079,2019-02-28
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,-0.42,2019-02-28
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,0.751,2019-02-28
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.266,2019-02-28
sector,last_5_sessions,lipi companies | Technology and Communication,-0.12,2019-02-28
sector,last_5_sessions,lipi companies | Textile Composite,0.18,2019-02-28
sector,last_5_sessions,lipi individuals | All other Sectors,-3.017,2019-02-28
sector,last_5_sessions,lipi individuals | Cement,-0.12,2019-02-28
sector,last_5_sessions,lipi individuals | Commercial Banks,-1.926,2019-02-28
sector,last_5_sessions,lipi individuals | Fertilizer,-1.125,2019-02-28
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,-0.877,2019-02-28
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,-1.425,2019-02-28
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-1.701,2019-02-28
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.246,2019-02-28
sector,last_5_sessions,lipi individuals | Technology and Communication,0.084,2019-02-28
sector,last_5_sessions,lipi individuals | Textile Composite,-0.288,2019-02-28
sector,last_5_sessions,lipi insurance companies | All other Sectors,7.117,2019-02-28
sector,last_5_sessions,lipi insurance companies | Cement,0.255,2019-02-28
sector,last_5_sessions,lipi insurance companies | Commercial Banks,2.497,2019-02-28
sector,last_5_sessions,lipi insurance companies | Fertilizer,0.45,2019-02-28
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.729,2019-02-28
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,0.014,2019-02-28
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.268,2019-02-28
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,0.406,2019-02-28
sector,last_5_sessions,lipi insurance companies | Technology and Communication,-0.051,2019-02-28
sector,last_5_sessions,lipi insurance companies | Textile Composite,0.623,2019-02-28
sector,last_5_sessions,lipi mutual funds | All other Sectors,-4.333,2019-02-28
sector,last_5_sessions,lipi mutual funds | Cement,-2.432,2019-02-28
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-1.056,2019-02-28
sector,last_5_sessions,lipi mutual funds | Fertilizer,-1.1,2019-02-28
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,-0.095,2019-02-28
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-0.705,2019-02-28
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.298,2019-02-28
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.199,2019-02-28
sector,last_5_sessions,lipi mutual funds | Technology and Communication,0.046,2019-02-28
sector,last_5_sessions,lipi mutual funds | Textile Composite,0.611,2019-02-28
sector,last_5_sessions,lipi nbfc | All other Sectors,0.186,2019-02-28
sector,last_5_sessions,lipi nbfc | Cement,0.24,2019-02-28
sector,last_5_sessions,lipi nbfc | Commercial Banks,0.197,2019-02-28
sector,last_5_sessions,lipi nbfc | Fertilizer,0.035,2019-02-28
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,-0.001,2019-02-28
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.078,2019-02-28
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.01,2019-02-28
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,0.016,2019-02-28
sector,last_5_sessions,lipi nbfc | Textile Composite,0.014,2019-02-28
sector,last_5_sessions,lipi other organization | All other Sectors,0.815,2019-02-28
sector,last_5_sessions,lipi other organization | Cement,0.436,2019-02-28
sector,last_5_sessions,lipi other organization | Commercial Banks,-0.23,2019-02-28
sector,last_5_sessions,lipi other organization | Fertilizer,0.659,2019-02-28
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,0.001,2019-02-28
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,0.481,2019-02-28
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.116,2019-02-28
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,-0.075,2019-02-28
sector,last_5_sessions,lipi other organization | Technology and Communication,0.008,2019-02-28
sector,last_5_sessions,lipi other organization | Textile Composite,-0.009,2019-02-28
investor_type,last_20_sessions,banks / dfi,8.098,2019-02-28
investor_type,last_20_sessions,broker proprietary trading,-9.268,2019-02-28
investor_type,last_20_sessions,companies,-5.096,2019-02-28
investor_type,last_20_sessions,foreign corporates,33.453,2019-02-28
investor_type,last_20_sessions,foreign individual,0.267,2019-02-28
investor_type,last_20_sessions,individuals,-2.014,2019-02-28
investor_type,last_20_sessions,insurance companies,10.494,2019-02-28
investor_type,last_20_sessions,mutual funds,-37.886,2019-02-28
investor_type,last_20_sessions,nbfc,0.481,2019-02-28
investor_type,last_20_sessions,other organization,-0.529,2019-02-28
investor_type,last_20_sessions,overseas pakistani,2.001,2019-02-28
sector,last_20_sessions,fipi | All other Sectors,4.829,2019-02-28
sector,last_20_sessions,fipi | Cement,11.642,2019-02-28
sector,last_20_sessions,fipi | Commercial Banks,11.289,2019-02-28
sector,last_20_sessions,fipi | Fertilizer,3.923,2019-02-28
sector,last_20_sessions,fipi | Food and Personal Care Products,-0.477,2019-02-28
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,2.773,2019-02-28
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,0.279,2019-02-28
sector,last_20_sessions,fipi | Power Generation and Distribution,-0.776,2019-02-28
sector,last_20_sessions,fipi | Technology and Communication,0.595,2019-02-28
sector,last_20_sessions,fipi | Textile Composite,1.645,2019-02-28
sector,last_20_sessions,lipi banks / dfi | All other Sectors,1.098,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Cement,-0.876,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,1.464,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Fertilizer,2.078,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.227,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,4.31,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.449,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-1.224,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,0.242,2019-02-28
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.329,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-0.696,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Cement,-2.386,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,-2.84,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-0.133,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.19,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-2.718,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.125,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.174,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-0.215,2019-02-28
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.388,2019-02-28
sector,last_20_sessions,lipi companies | All other Sectors,-2.526,2019-02-28
sector,last_20_sessions,lipi companies | Cement,-0.034,2019-02-28
sector,last_20_sessions,lipi companies | Commercial Banks,0.655,2019-02-28
sector,last_20_sessions,lipi companies | Fertilizer,0.417,2019-02-28
sector,last_20_sessions,lipi companies | Food and Personal Care Products,0.382,2019-02-28
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,-1.549,2019-02-28
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,0.245,2019-02-28
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-0.605,2019-02-28
sector,last_20_sessions,lipi companies | Technology and Communication,-0.11,2019-02-28
sector,last_20_sessions,lipi companies | Textile Composite,-1.97,2019-02-28
sector,last_20_sessions,lipi individuals | All other Sectors,6.598,2019-02-28
sector,last_20_sessions,lipi individuals | Cement,-6.336,2019-02-28
sector,last_20_sessions,lipi individuals | Commercial Banks,-4.294,2019-02-28
sector,last_20_sessions,lipi individuals | Fertilizer,-2.128,2019-02-28
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,-0.907,2019-02-28
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,-1.73,2019-02-28
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,0.394,2019-02-28
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,3.008,2019-02-28
sector,last_20_sessions,lipi individuals | Technology and Communication,-0.174,2019-02-28
sector,last_20_sessions,lipi individuals | Textile Composite,3.556,2019-02-28
sector,last_20_sessions,lipi insurance companies | All other Sectors,3.956,2019-02-28
sector,last_20_sessions,lipi insurance companies | Cement,5.549,2019-02-28
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-1.759,2019-02-28
sector,last_20_sessions,lipi insurance companies | Fertilizer,1.0,2019-02-28
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,1.531,2019-02-28
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-2.176,2019-02-28
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.903,2019-02-28
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,1.435,2019-02-28
sector,last_20_sessions,lipi insurance companies | Technology and Communication,0.101,2019-02-28
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.047,2019-02-28
sector,last_20_sessions,lipi mutual funds | All other Sectors,-13.033,2019-02-28
sector,last_20_sessions,lipi mutual funds | Cement,-5.966,2019-02-28
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-3.026,2019-02-28
sector,last_20_sessions,lipi mutual funds | Fertilizer,-5.981,2019-02-28
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,-0.51,2019-02-28
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-1.481,2019-02-28
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-2.082,2019-02-28
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-1.985,2019-02-28
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-0.682,2019-02-28
sector,last_20_sessions,lipi mutual funds | Textile Composite,-3.14,2019-02-28
sector,last_20_sessions,lipi nbfc | All other Sectors,0.545,2019-02-28
sector,last_20_sessions,lipi nbfc | Cement,-0.482,2019-02-28
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.435,2019-02-28
sector,last_20_sessions,lipi nbfc | Fertilizer,0.021,2019-02-28
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.026,2019-02-28
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.246,2019-02-28
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.373,2019-02-28
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.0,2019-02-28
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.178,2019-02-28
sector,last_20_sessions,lipi nbfc | Textile Composite,0.008,2019-02-28
sector,last_20_sessions,lipi other organization | All other Sectors,-0.772,2019-02-28
sector,last_20_sessions,lipi other organization | Cement,-1.111,2019-02-28
sector,last_20_sessions,lipi other organization | Commercial Banks,-1.053,2019-02-28
sector,last_20_sessions,lipi other organization | Fertilizer,0.804,2019-02-28
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-0.082,2019-02-28
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,2.325,2019-02-28
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.685,2019-02-28
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,-0.027,2019-02-28
sector,last_20_sessions,lipi other organization | Technology and Communication,0.065,2019-02-28
sector,last_20_sessions,lipi other organization | Textile Composite,0.007,2019-02-28

=== FILE: calendar.md ===
# Calendar as of 2019-03-01

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2019-02-01 STCL: Board Meeting
- 2019-02-01 NETSOL: Board Meeting
- 2019-02-04 CHCC: NOTICE OF BOARD OF DIRECTORS MEETING & NOTICE OF CLOSED PERIOD
- 2019-02-06 LOTCHEM: Board Meeting / Closed Period
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
- 2019-02-19 PKGS: BOARD MEETING
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
type,as_of_cutoff,n,hit_rate,median,p50plus,source
none,,,,,,no base rates available
=== END ===
