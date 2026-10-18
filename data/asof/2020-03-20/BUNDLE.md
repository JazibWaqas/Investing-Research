# Replay bundle, close of 2020-03-20

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
# Market as of 2020-03-20 close (public information only)

- KSE100: 30,667 on 2020-03-20; 1m -24.2%, 3m -24.9%, 6m -3.7%, 12m -21.0%
- KMI All Share: 14,433 on 2020-03-20; 1m -22.5%, 3m -25.4%, 6m -2.5%, 12m -23.0%
- Policy rate 12.5%; last MPC decision 2020-03-17: cut (-75bp)
- 6M T-bill cutoff 12.51% (auction 2020-03-11); 3M 12.73%, 12M 12.00%
- CPI YoY 12.94% for 2020-02 (published by 2020-03-03); three months earlier (2019-11) 13.68%
- Brent: 25.55 USD/bbl on 2020-03-20; 3-month change -62.8%
- USD/PKR: 158.29  on 2020-03-20; 3-month change +2.3%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.01pp (market near policy rate); CPI falling over 3 months (-0.7pp)
- Next MPC: see SBP calendar

Session date used: 2020-03-20. Liquid KMI names: 55 (membership KMI_ALL_derived_2020-01-13.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.2729,-0.3186,-0.0287,0,0
E&P,3,-0.2997,-0.3436,-0.1239,0,0
OMC,4,-0.2375,-0.3033,0.0211,0,0
Power,5,-0.2028,-0.2321,-0.1418,0,0
Fertilizer,4,-0.1801,-0.2086,-0.1031,0,0
Cement,16,-0.1352,-0.1658,0.2249,0,0
Steel & engineering,10,-0.1507,-0.2163,0.1121,0,0
Autos,12,-0.2298,-0.3296,0.0776,0,0
Tech & telecom,6,-0.3164,-0.3184,-0.0884,0,0
Islamic banks & fin.,6,-0.2051,-0.1736,-0.0515,0,0
Pharma,10,-0.0706,-0.0791,0.5161,0,0
Textiles,20,-0.2076,-0.1459,-0.0225,0,0
Food & staples,11,-0.2198,-0.2756,0.0085,0,0
Chemicals,17,-0.1957,-0.2198,0.027,0,0
"Glass, packaging, paper",12,-0.2392,-0.2882,0.1049,0,0
Gas utilities & misc,9,-0.1756,-0.2838,0.0114,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,n_results,n_material,n_insider_buy,n_insider_sell
ACPL,90.61,-0.109,-0.094,0.218,-0.057,-0.274,1.588,0,1,0,0,0
AGP,84.98,-0.167,-0.092,0.371,0.036,-0.218,0.62,0,1,0,0,0
ASC,8.05,-0.365,-0.365,-0.137,-0.542,-0.518,0.989,0,2,0,0,0
ASTL,26.81,-0.199,-0.237,0.255,-0.334,-0.378,0.916,0,2,1,0,0
ATRL,73.73,-0.248,-0.361,-0.033,-0.348,-0.462,0.742,0,0,0,0,0
BIPL,8.37,-0.362,-0.285,-0.23,-0.242,-0.442,0.858,0,2,1,0,0
CHCC,57.51,0.086,0.036,1.448,-0.037,-0.331,1.595,0,1,0,0,0
DCL,5.36,-0.322,-0.313,-0.095,-0.555,-0.563,1.132,0,2,0,0,0
DGKC,63.07,-0.076,-0.138,0.419,-0.291,-0.282,1.475,0,1,0,0,0
EFERT,56.31,-0.151,-0.227,-0.176,-0.24,-0.283,0.99,0,1,0,0,0
ENGROH,110.92,-0.284,-0.319,-0.067,-0.113,-0.368,0.428,0,0,0,0,0
EPCL,27.13,-0.156,-0.177,0.049,-0.268,-0.275,0.808,0,0,3,0,0
FCCL,13.65,-0.126,-0.127,0.081,-0.334,-0.335,1.678,0,2,0,0,0
FCEPL,49.89,-0.287,-0.387,-0.124,-0.311,-0.42,0.382,0,0,0,0,0
FEROZ,196.86,-0.006,-0.077,0.602,-0.023,-0.146,0.998,0,2,0,0,0
GAL,45.11,-0.283,-0.434,-0.149,-0.467,-0.481,0.745,0,0,0,0,0
GGL,8.7,-0.429,-0.367,0.158,-0.279,-0.531,0.664,0,2,0,0,0
GHNI,71.53,-0.385,-0.485,-0.166,-0.616,-0.616,1.012,0,1,0,0,0
GLAXO,160.97,-0.047,-0.059,0.672,0.103,-0.142,1.268,0,1,2,0,0
HCAR,164.13,-0.18,-0.223,0.223,-0.329,-0.343,0.715,0,0,0,0,0
HTL,24.89,-0.195,-0.233,-0.001,-0.488,-0.485,1.521,0,2,1,0,0
HUBC,67.05,-0.31,-0.25,-0.078,-0.195,-0.35,1.555,0,2,0,0,0
ILP,39.42,-0.31,-0.312,-0.06,,-0.352,0.47,0,2,0,0,0
INIL,80.09,-0.205,-0.196,0.133,-0.392,-0.386,1.126,0,1,0,0,0
ISL,37.64,-0.24,-0.31,-0.074,-0.414,-0.421,0.834,0,1,0,0,0
KEL,2.99,-0.271,-0.274,-0.083,-0.493,-0.485,0.814,0,0,0,0,0
KOHC,91.78,0.014,0.18,0.994,0.055,-0.277,2.173,0,2,0,0,0
KTML,28.9,-0.294,-0.238,0.329,-0.325,-0.358,0.492,0,2,0,0,0
LCI,554.44,-0.218,-0.144,0.244,-0.183,-0.238,0.253,0,0,0,0,0
LOTCHEM,9.23,-0.336,-0.35,-0.363,-0.353,-0.463,0.562,0,0,0,0,0
LUCK,372.7,-0.229,-0.107,0.085,-0.179,-0.342,1.518,0,0,0,0,0
MARI,990.84,-0.215,-0.26,0.134,-0.234,-0.319,1.348,0,1,0,0,0
MEBL,64.85,-0.345,-0.313,-0.114,-0.26,-0.389,1.253,0,1,0,0,0
MLCF,20.21,-0.135,-0.112,0.428,-0.506,-0.501,1.674,0,2,0,0,0
MTL,544.0,-0.225,-0.221,-0.061,-0.202,-0.277,1.203,0,1,0,0,0
MUGHAL,32.32,-0.231,-0.184,0.191,-0.168,-0.354,1.004,0,2,0,0,0
NETSOL,31.74,-0.461,-0.52,-0.433,-0.627,-0.62,0.858,0,1,0,0,0
NML,66.03,-0.369,-0.364,-0.185,-0.521,-0.511,0.936,0,1,0,0,0
NRL,90.7,-0.255,-0.371,-0.193,-0.495,-0.469,0.675,0,0,0,0,0
OGDC,91.81,-0.313,-0.348,-0.241,-0.358,-0.405,1.512,1,2,0,0,0
PAEL,19.33,-0.227,-0.262,0.21,-0.186,-0.345,0.699,0,0,0,0,0
PKGS,249.45,-0.355,-0.389,-0.117,-0.267,-0.443,0.939,0,1,1,0,0
POWER,5.01,-0.206,-0.188,0.055,-0.352,-0.38,1.157,0,2,0,0,0
PPL,81.25,-0.369,-0.423,-0.24,-0.446,-0.484,1.713,1,2,0,0,0
PSO,135.83,-0.252,-0.27,0.045,-0.256,-0.374,0.897,0,1,1,0,0
SEARL,172.39,-0.017,-0.082,0.198,-0.313,-0.294,0.85,0,2,1,0,0
SNGP,42.32,-0.426,-0.437,-0.297,-0.335,-0.491,0.674,0,1,0,0,0
SPEL,29.36,-0.249,-0.194,0.716,-0.084,-0.267,1.064,0,1,0,0,0
SSGC,12.02,-0.33,-0.464,-0.249,-0.458,-0.514,0.479,0,0,0,0,0
STPL,7.02,-0.276,-0.302,-0.216,-0.648,-0.645,0.55,0,2,0,0,0
SYS,107.01,-0.303,-0.1,0.289,0.212,-0.318,0.829,0,0,0,0,0
TGL,52.98,-0.355,-0.329,-0.019,-0.262,-0.375,1.515,0,2,0,0,0
TREET,13.64,-0.312,-0.367,0.014,-0.385,-0.428,0.732,0,2,1,0,0
UNITY,8.71,-0.396,-0.411,0.022,-0.385,-0.495,0.947,0,2,0,0,0
WAFI,127.41,-0.32,-0.436,-0.008,-0.515,-0.52,0.459,0,0,0,0,0

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2020-02-19,GSPM,material_info,Material Information
2020-02-19,PMRS,insider_trade,Insider trade disclosure
2020-02-19,CHAS,insider_trade,Insider trade disclosure
2020-02-20,GLAXO,material_info,Material Information - GSK Pakistan Limited REVOKED
2020-02-20,GLAXO,material_info,Material Information - GlaxoSmithKline Pakistan Limited
2020-02-20,ARPAK,insider_trade,Insider trade disclosure
2020-02-20,IGIHL,insider_trade,Insider trade disclosure
2020-02-20,BAFL,insider_trade,Insider trade disclosure
2020-02-20,GGL,other,Meeting of Board of Directors - Ghani Global Holdings Limited
2020-02-21,JSGCL,material_info,Material Information
2020-02-21,INIL,financial_result,FINANCIAL RESULTS FOR THE HALF YEAR ENDED 31-12-2019
2020-02-21,FCCL,financial_result,Financial Results for the Half Year Ended 31st December 2019
2020-02-21,NETSOL,financial_result,Transmission of Quarterly Report for the Period Ended 2019-12-31
2020-02-21,MUGHAL,financial_result,"Financial Results for the Half Year ended December 31, 2019"
2020-02-21,MUGHAL,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2019"
2020-02-21,UBL,insider_trade,Insider trade disclosure
2020-02-21,HASCOL,insider_trade,Insider trade disclosure
2020-02-21,GGL,other,ALTERATION IN SPECIAL RESOLUTION PASSED BY THE SHAREHOLDERS- GHANI GLOBAL H
2020-02-24,JSIL,material_info,Material Information
2020-02-24,SHFA,material_info,Material Information
2020-02-24,HTL,financial_result,"Financial Results for the Quarter Ended December 31, 2019"
2020-02-24,DGKC,financial_result,"Submission of Half Yearly Accounts for the period ended December 31,2019"
2020-02-24,ISL,financial_result,TRANSMISSION OF HALF YEARLY REPORT FOR THE PERIOD ENDED 31-12-2019
2020-02-24,GHNI,financial_result,"Transmission of Quarterly Report for the period ended December 31, 2019"
2020-02-24,MARI,dividend_or_bonus,Payment of First Interim Cash Dividend for the Year 2019-20
2020-02-24,RAVT,insider_trade,Insider trade disclosure
2020-02-24,HSM,insider_trade,Insider trade disclosure
2020-02-25,SERF,material_info,Material Information
2020-02-25,MTIL,material_info,Material Information
2020-02-25,SLCL,material_info,Material Information
2020-02-25,HTL,material_info,MATERIAL INFORMATION: PERMISSION BY OGRA TO PROCEED TO APPLY FOR NOCs to SE
2020-02-25,SLCL,material_info,Material Information - Revised
2020-02-25,DCL,financial_result,"Financial Results for the Quarter Ended December 31,2019"
2020-02-25,MTL,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2019"
2020-02-25,HUBC,financial_result,Financial Results for the 2nd Quarter/ Half Year Ended December 31 2019
2020-02-25,PPL,financial_result,Financial Results for the Half Year Ended 31 December 2019
2020-02-25,CHCC,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2019"
2020-02-26,GATM,material_info,MATERIAL INFORMATION
2020-02-26,SNGP,financial_result,APPLICATION FOR EXTENSION IN THE PERIOD FOR SUBMISSION OF HALF YEARLY ACCOU
2020-02-26,MLCF,financial_result,Financial Results for the Quarter Ended 31.12.2019
2020-02-26,OGDC,financial_result,"Financial Results for the Quarter Ended December 31, 2019"
2020-02-26,FCCL,financial_result,Transmission of Half Yearly Accounts for the Period Ended 31st Dec 2019
2020-02-26,ASTL,financial_result,Financial Results for the Half Year Ended 31 December 2019
2020-02-26,UNITY,financial_result,"Financial Results for the Half year Ended December 31, 2019"
2020-02-26,NML,financial_result,"SUBMISSION OF HALF YEARLY ACCOUNTS FOR THE PERIOD ENDED DECEMBER 31,2019"
2020-02-26,PPL,financial_result,Transmission of Half Year Report for the period ended 31 December 2019
2020-02-26,ASC,dividend_or_bonus,Board Resolution for Unsubscribed Shares Against Right Issue
2020-02-26,ENGRO,insider_trade,Insider trade disclosure
2020-02-26,BAFL,insider_trade,Insider trade disclosure
2020-02-26,PSO,other,Appointment of Chief Executive Officer / Managing Director
2020-02-27,KOHC,financial_result,"Financial Results for the Quarter Ended December 31, 2019"
2020-02-27,TREET,financial_result,Financial Results for the Quarter Ended
2020-02-27,KTML,financial_result,Financial Results for the Quarter Ended 31.12.2019
2020-02-27,MARI,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2019"
2020-02-27,HUBC,financial_result,Transmission of Half Yearly/ 2nd Quarter Report for the Period Ended Dec 31
2020-02-27,ILP,financial_result,"Transmission of Half Year Report for the Period Ended December 31, 2019"
2020-02-27,TGL,financial_result,Financial Results for the Quarter Ended 31 December 2019
2020-02-27,ASC,financial_result,Financial Result for the Quarter Ended 2019-12-31
2020-02-27,ASC,dividend_or_bonus,Auditor's Certificate on Subscription of Right Issue
2020-02-27,ENGRO,insider_trade,Insider trade disclosure
2020-02-27,ENGRO,insider_trade,Insider trade disclosure
2020-02-27,PMPK,insider_trade,Insider trade disclosure
2020-02-27,ICI,insider_trade,Insider trade disclosure
2020-02-27,HBL,insider_trade,Insider trade disclosure
2020-02-27,JSIL,insider_trade,Insider trade disclosure
2020-02-27,MARI,other,Appointment of Director
2020-02-27,BIPL,other,BankIslami Pakistan Limited-Board Meeting in Progress
2020-02-27,POWER,other,MEETING IN PROGRESS
2020-02-28,BIPL,material_info,Disclosure of Material Information
2020-02-28,HUMNL,material_info,Material Information
2020-02-28,LOADS,material_info,Disclosure of Material Information
2020-02-28,POWER,financial_result,"FINANCIAL RESULTS FOR THE SIX MONTHS PERIOD ENDED DECEMBER 31, 2019"
2020-02-28,HTL,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2019"
2020-02-28,SEARL,financial_result,Financial Results for the Quarter Ended 2019-12-31
2020-02-28,BIPL,financial_result,"Financial Results for the year ended December 31, 2019"
2020-02-28,SPEL,financial_result,Transmission of Quarterly Report for the Period Ended 31-Dec-2019
2020-02-28,TREET,financial_result,Transmission of Quarterly Report for the Period Ended
2020-02-28,KOHC,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2019"
2020-02-28,DCL,financial_result,"Transmission of Quarterly Report for the Period Ended December 31,2019"
2020-02-28,ACPL,financial_result,Transmission of Half Yearly Accounts
2020-02-28,FEROZ,financial_result,Financial Results for the Quarter Ended 2019-12-31
2020-02-28,KTML,financial_result,Transmission of Quarterly Report for the Period Ended 31.12.2019
2020-02-28,PSO,financial_result,"Transmission of Half Yearly Report for the period ended December 31, 2019"
2020-02-28,TGL,financial_result,Transmission of Quarterly Report for the Period Ended 31 December 2019
2020-02-28,UNITY,financial_result,"Transmission of Half yearly report for the period ended December 31, 2019"
2020-02-28,ASTL,financial_result,Transmission of Half Yearly Report for the Period Ended 31 December 2019
2020-02-28,POWER,financial_result,TRANSMISSION OF HALF YEARLY ACCOUNTS FOR THE SIX MONTHS PERIOD 31 DECEMBER 
2020-02-28,FEROZ,financial_result,Transmission of Quarterly Report for the Period Ended 2019-12-31
2020-02-28,STPL,financial_result,"Financial Results for the 2nd Quarter half year period Ended December 31, 2"
2020-02-28,OGDC,financial_result,Transmission of quarterly report for the quarter ended 2019-12-31
2020-02-28,SEARL,financial_result,Transmission of Quarterly Report for the Period Ended 2019-12-31
2020-02-28,ASTL,dividend_or_bonus,Final Notice to the Shareholders for Unclaimed Dividend (D-1) - Published i
2020-02-28,KTML,dividend_or_bonus,KTML- Notice of Book Closure for 10% Interim Cash Dividend 31.12.2019
2020-02-28,UNITY,insider_trade,Insider trade disclosure
2020-02-28,DAWH,insider_trade,Insider trade disclosure
2020-02-28,STJT,insider_trade,Insider trade disclosure
2020-02-28,HSM,insider_trade,Insider trade disclosure
2020-02-28,GGL,other,Meeting in Progress - Ghani Global Holdings Limited
2020-03-02,DLL,material_info,Material Information
2020-03-02,ICI,material_info,Disclosure of Material Information
2020-03-02,CEPB,material_info,MATERIAL INFORMATION
2020-03-02,GGL,financial_result,"Financial Results for the half year ended December 31, 2019 - Ghani Global "
2020-03-02,GGL,financial_result,"Transmission of Half Yearly Accounts for the period ended December 31, 2019"
2020-03-02,MLCF,financial_result,Transmission of Quarterly Report for the Period Ended 31.12.2019
2020-03-02,ASC,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2019"
2020-03-02,MTL,insider_trade,Insider trade disclosure
2020-03-02,KEL,other,Incorporation of a private limited wholly owned KE subsidiary company to un
2020-03-02,GLAXO,other,Change of Chief Executive/Director
2020-03-02,HTL,other,Miscellaneous Information
2020-03-02,TREET,other,Company Secretary
2020-03-02,BIPL,agm,BankIslami Pakistan Limited - Annual General Meeting
2020-03-03,CSAP,material_info,Material Information
2020-03-03,MEBL,financial_result,"Transmission of Annual Report for the Year Ended December 31, 2019"
2020-03-03,STPL,financial_result,Transmission of half yearly
2020-03-03,MTL,insider_trade,Insider trade disclosure
2020-03-03,BAFL,insider_trade,Insider trade disclosure
2020-03-03,PKGS,insider_trade,Insider trade disclosure
2020-03-03,SNGP,other,CLARIFICATION OF SUI NORTHERN GAS PIPELINES LIMITED AS PER CLAUSE 5.6.1(B) 
2020-03-03,CHCC,other,MATERAIL INFORMATION - SUPPLY OF GAS
2020-03-03,MEBL,agm,Notice of 24th Annual General Meeting Prior to Publication
2020-03-03,NML,agm,NOTICE OF EXTRA ORDINARY GENERAL MEETING
2020-03-04,BIPL,financial_result,BankIslami Pakistan Limited - Annual Report 2019
2020-03-04,JKSM,insider_trade,Insider trade disclosure
2020-03-04,FEROZ,insider_trade,Insider trade disclosure
2020-03-04,MUREB,insider_trade,Insider trade disclosure
2020-03-04,EFERT,other,Resignation of Director
2020-03-04,MEBL,agm,Notice of 24th Annual General Meeting (AGM) of Meezan Bank Limited
2020-03-04,BIPL,agm,BankIslami Pakistan Limited-Notice of 16th Annual General Meeting
2020-03-05,POL,material_info,MATERIAL INFORMATION
2020-03-05,PSO,material_info,Material Information
2020-03-05,KOHC,insider_trade,Insider trade disclosure
2020-03-05,JSBL,insider_trade,Insider trade disclosure
2020-03-05,ICI,insider_trade,Insider trade disclosure
2020-03-05,MTL,insider_trade,Insider trade disclosure
2020-03-05,MTL,insider_trade,Insider trade disclosure
2020-03-05,SRVI,insider_trade,Insider trade disclosure
2020-03-05,MTL,insider_trade,Insider trade disclosure
2020-03-05,SERT,insider_trade,Insider trade disclosure
2020-03-05,EFERT,agm,NOTICE OF THE 11TH ANNUAL GENERAL MEETING OF ENGRO FERTILIZERS LIMITED
2020-03-06,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-06,AVN,material_info,Material Information
2020-03-06,SEARL,material_info,Material Information
2020-03-06,AKBL,insider_trade,Insider trade disclosure
2020-03-06,MCB,insider_trade,Insider trade disclosure
2020-03-06,UBL,insider_trade,Insider trade disclosure
2020-03-06,UBL,insider_trade,Insider trade disclosure
2020-03-06,GOC,insider_trade,Insider trade disclosure
2020-03-06,POL,insider_trade,Insider trade disclosure
2020-03-06,MARI,other,Disclosure of Material Price Sensitive Information
2020-03-06,HUBC,agm,Notice of Extraordinary General Meeting The Hub Power Company Limited
2020-03-06,TGL,agm,Notice of Extra Ordinary General Meeting
2020-03-06,POWER,agm,NOTICE OF EXTRAORDINARY GENERAL MEETING
2020-03-09,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-09,MTIL,material_info,Material Information
2020-03-09,SJTM,material_info,Material Information - Delisting from PSX
2020-03-09,BYCO,material_info,Disclosure of Material Information
2020-03-09,SHEL,insider_trade,Insider trade disclosure
2020-03-10,EFERT,financial_result,Annual Report for the Year Ended 2019
2020-03-10,HSM,insider_trade,Insider trade disclosure
2020-03-10,INIL,insider_trade,Insider trade disclosure
2020-03-10,OGDC,other,Resignation of Director
2020-03-11,TREET,material_info,Material Information
2020-03-11,GLAXO,financial_result,"financial Results for the Year Ended December 31, 2019"
2020-03-11,POL,insider_trade,Insider trade disclosure
2020-03-11,SHJS,insider_trade,Insider trade disclosure
2020-03-11,POL,insider_trade,Insider trade disclosure
2020-03-11,SNGP,other,CASUAL VACANCY ON THE BOARD OF SNGPL
2020-03-12,CSAP,material_info,Material Information
2020-03-12,ASC,dividend_or_bonus,Credit / Delivery of Shares - Right Issue
2020-03-12,HUBC,insider_trade,Insider trade disclosure
2020-03-12,POL,insider_trade,Insider trade disclosure
2020-03-13,GSKCH,material_info,Material Information REVOKED
2020-03-13,PKGS,material_info,Material Information
2020-03-13,AGP,financial_result,"Financial Results for the Year Ended December 31, 2019"
2020-03-13,PKGS,financial_result,FINANCIAL RESULTS FOR THE YEAR ENDED 31 DECEMBER 2019
2020-03-13,ENGRO,insider_trade,Insider trade disclosure
2020-03-13,NRL,insider_trade,Insider trade disclosure
2020-03-13,HASCOL,insider_trade,Insider trade disclosure
2020-03-13,MARI,other,COVID-19 Preventive Measures Taken by MPCL
2020-03-16,GHGL,material_info,Material Information
2020-03-16,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-16,SILK,material_info,Material Information
2020-03-16,GSKCH,material_info,Material Information
2020-03-16,ILP,financial_result,"Credit of Interim Cash Dividend for the half year ended December 31, 2019 a"
2020-03-16,UBL,insider_trade,Insider trade disclosure
2020-03-16,HSM,insider_trade,Insider trade disclosure
2020-03-16,POL,insider_trade,Insider trade disclosure
2020-03-16,DINT,insider_trade,Insider trade disclosure
2020-03-16,DINT,insider_trade,"DISCLOSURE OF INTEREST BY A DIRECTOR CEO, OR EXECUTIVE OF A LISTED COMPANY "
2020-03-16,DAWH,insider_trade,Insider trade disclosure
2020-03-16,SSGC,agm,APPLICATION FOR EXTENSION IN PERIOD OF HOLDING ANNUAL GENERAL MEETING (AGM)
2020-03-16,EPCL,agm,Notice of the Twenty Second Annual General Meeting - EPCL
2020-03-17,CSAP,material_info,Material Information
2020-03-17,GSKCH,material_info,Material Information
2020-03-17,PKGS,insider_trade,Insider trade disclosure
2020-03-17,OML,insider_trade,Insider trade disclosure
2020-03-17,ENGRO,insider_trade,Insider trade disclosure
2020-03-17,ASTL,insider_trade,Insider trade disclosure
2020-03-17,HSM,insider_trade,Insider trade disclosure
2020-03-17,SNGP,other,SNGPL INITIATIVES FOR NOVEL CORONA VIRUS (COVID-19) OUTBREAK
2020-03-17,FCCL,other,Commissioning of 2.5 Mega Watt Captive Power Plant
2020-03-18,ASTL,material_info,Material Information
2020-03-18,PKGS,insider_trade,Insider trade disclosure
2020-03-18,TGL,insider_trade,Insider trade disclosure
2020-03-18,LUCK,insider_trade,Disclosure of Interest by an Associated Company u/s 5.6.1 of PSX Regulation
2020-03-19,UBL,insider_trade,Insider trade disclosure
2020-03-19,DAWH,insider_trade,Insider trade disclosure
2020-03-19,PKGS,insider_trade,Insider trade disclosure
2020-03-19,PKGS,insider_trade,Insider trade disclosure
2020-03-19,EFUL,insider_trade,Insider trade disclosure
2020-03-19,NML,agm,ADDENDUM TO THE NOTICE OF EXTRA ORDINARY GENERAL MEETING OF NISHAT MILLS LI
2020-03-19,NML,agm,ELECTION OF DIRECTORS
2020-03-20,FFC,material_info,Material Information
2020-03-20,FATIMA,material_info,Material Information
2020-03-20,SEPL,insider_trade,Insider trade disclosure
2020-03-20,MEBL,insider_trade,Insider trade disclosure
2020-03-20,FFC,insider_trade,Insider trade disclosure
2020-03-20,SRVI,insider_trade,Insider trade disclosure
2020-03-20,MTL,insider_trade,Insider trade disclosure
2020-03-20,OML,insider_trade,Insider trade disclosure
2020-03-20,PKGS,insider_trade,Insider trade disclosure
2020-03-20,MFL,insider_trade,Insider trade disclosure
2020-03-20,EFUL,insider_trade,Insider trade disclosure
2020-03-20,PAEL,other,"PEL - Board Meeting for the Year Ended December 31, 2019"
2020-03-20,FCCL,other,Resignation of Director/Chairman - Fauji Cement Company Limited (FCCL)
2020-03-20,FCCL,other,Resignation of Director/Chairman - Fauji Cement Company Limited (FCCL)
2020-03-20,PKGS,other,RESIGNATION OF DIRECTOR
2020-03-20,MARI,other,Resignation of Director/Chairman of the Board
2020-03-20,HUBC,agm,CORONA VIRUS CONTINGENCY PLANNING FOR EXTRAORDINARY GENERAL MEETING OF THE 
2020-03-20,BIPL,agm,Annual General Meeting (AGM) of BankIslami Pakistan Limited (BIPL) - Revise

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,16.454,2020-03-19
investor_type,last_5_sessions,broker proprietary trading,-0.214,2020-03-19
investor_type,last_5_sessions,companies,-13.807,2020-03-19
investor_type,last_5_sessions,foreign corporates,-25.314,2020-03-19
investor_type,last_5_sessions,foreign individual,0.098,2020-03-19
investor_type,last_5_sessions,individuals,17.279,2020-03-19
investor_type,last_5_sessions,insurance companies,25.254,2020-03-19
investor_type,last_5_sessions,mutual funds,-18.899,2020-03-19
investor_type,last_5_sessions,nbfc,-1.167,2020-03-19
investor_type,last_5_sessions,other organization,0.386,2020-03-19
investor_type,last_5_sessions,overseas pakistani,-0.069,2020-03-19
sector,last_5_sessions,fipi | All other Sectors,-3.034,2020-03-19
sector,last_5_sessions,fipi | Cement,-9.786,2020-03-19
sector,last_5_sessions,fipi | Commercial Banks,-6.669,2020-03-19
sector,last_5_sessions,fipi | Fertilizer,-1.792,2020-03-19
sector,last_5_sessions,fipi | Food and Personal Care Products,0.021,2020-03-19
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-3.194,2020-03-19
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,-0.473,2020-03-19
sector,last_5_sessions,fipi | Power Generation and Distribution,-0.471,2020-03-19
sector,last_5_sessions,fipi | Technology and Communication,-0.002,2020-03-19
sector,last_5_sessions,fipi | Textile Composite,0.116,2020-03-19
sector,last_5_sessions,lipi banks / dfi | All other Sectors,1.891,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Cement,4.862,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,1.499,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Fertilizer,3.192,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-0.004,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,3.081,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.447,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,1.202,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,0.328,2020-03-19
sector,last_5_sessions,lipi banks / dfi | Textile Composite,-0.044,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-0.263,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.038,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,1.14,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,-0.671,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.046,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.499,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.106,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.142,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,-0.008,2020-03-19
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.245,2020-03-19
sector,last_5_sessions,lipi companies | All other Sectors,-0.879,2020-03-19
sector,last_5_sessions,lipi companies | Cement,-10.14,2020-03-19
sector,last_5_sessions,lipi companies | Commercial Banks,-6.928,2020-03-19
sector,last_5_sessions,lipi companies | Fertilizer,0.596,2020-03-19
sector,last_5_sessions,lipi companies | Food and Personal Care Products,-0.012,2020-03-19
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,0.304,2020-03-19
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,2.478,2020-03-19
sector,last_5_sessions,lipi companies | Power Generation and Distribution,0.525,2020-03-19
sector,last_5_sessions,lipi companies | Technology and Communication,0.13,2020-03-19
sector,last_5_sessions,lipi companies | Textile Composite,0.119,2020-03-19
sector,last_5_sessions,lipi individuals | All other Sectors,-0.957,2020-03-19
sector,last_5_sessions,lipi individuals | Cement,6.387,2020-03-19
sector,last_5_sessions,lipi individuals | Commercial Banks,5.351,2020-03-19
sector,last_5_sessions,lipi individuals | Fertilizer,2.976,2020-03-19
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,-0.044,2020-03-19
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,4.133,2020-03-19
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-1.116,2020-03-19
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,-0.274,2020-03-19
sector,last_5_sessions,lipi individuals | Technology and Communication,-0.082,2020-03-19
sector,last_5_sessions,lipi individuals | Textile Composite,0.905,2020-03-19
sector,last_5_sessions,lipi insurance companies | All other Sectors,3.457,2020-03-19
sector,last_5_sessions,lipi insurance companies | Cement,6.44,2020-03-19
sector,last_5_sessions,lipi insurance companies | Commercial Banks,6.206,2020-03-19
sector,last_5_sessions,lipi insurance companies | Fertilizer,1.712,2020-03-19
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.029,2020-03-19
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,3.95,2020-03-19
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,1.825,2020-03-19
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,1.205,2020-03-19
sector,last_5_sessions,lipi insurance companies | Technology and Communication,0.113,2020-03-19
sector,last_5_sessions,lipi insurance companies | Textile Composite,0.316,2020-03-19
sector,last_5_sessions,lipi mutual funds | All other Sectors,-0.742,2020-03-19
sector,last_5_sessions,lipi mutual funds | Cement,2.873,2020-03-19
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-0.991,2020-03-19
sector,last_5_sessions,lipi mutual funds | Fertilizer,-6.165,2020-03-19
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,-0.013,2020-03-19
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-7.708,2020-03-19
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-3.115,2020-03-19
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-2.322,2020-03-19
sector,last_5_sessions,lipi mutual funds | Technology and Communication,-0.104,2020-03-19
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.611,2020-03-19
sector,last_5_sessions,lipi nbfc | All other Sectors,-0.142,2020-03-19
sector,last_5_sessions,lipi nbfc | Cement,0.026,2020-03-19
sector,last_5_sessions,lipi nbfc | Commercial Banks,0.044,2020-03-19
sector,last_5_sessions,lipi nbfc | Fertilizer,0.008,2020-03-19
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.33,2020-03-19
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.186,2020-03-19
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,0.015,2020-03-19
sector,last_5_sessions,lipi nbfc | Technology and Communication,-0.369,2020-03-19
sector,last_5_sessions,lipi nbfc | Textile Composite,-0.234,2020-03-19
sector,last_5_sessions,lipi other organization | All other Sectors,0.67,2020-03-19
sector,last_5_sessions,lipi other organization | Cement,-0.699,2020-03-19
sector,last_5_sessions,lipi other organization | Commercial Banks,0.348,2020-03-19
sector,last_5_sessions,lipi other organization | Fertilizer,0.144,2020-03-19
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,-0.023,2020-03-19
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,0.262,2020-03-19
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.034,2020-03-19
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,-0.023,2020-03-19
sector,last_5_sessions,lipi other organization | Technology and Communication,-0.006,2020-03-19
sector,last_5_sessions,lipi other organization | Textile Composite,-0.321,2020-03-19
investor_type,last_20_sessions,banks / dfi,25.657,2020-03-19
investor_type,last_20_sessions,broker proprietary trading,-2.759,2020-03-19
investor_type,last_20_sessions,companies,-3.152,2020-03-19
investor_type,last_20_sessions,foreign corporates,-72.499,2020-03-19
investor_type,last_20_sessions,foreign individual,-0.005,2020-03-19
investor_type,last_20_sessions,individuals,6.688,2020-03-19
investor_type,last_20_sessions,insurance companies,75.336,2020-03-19
investor_type,last_20_sessions,mutual funds,-26.741,2020-03-19
investor_type,last_20_sessions,nbfc,-1.244,2020-03-19
investor_type,last_20_sessions,other organization,2.938,2020-03-19
investor_type,last_20_sessions,overseas pakistani,-4.217,2020-03-19
sector,last_20_sessions,fipi | All other Sectors,-11.231,2020-03-19
sector,last_20_sessions,fipi | Cement,-20.555,2020-03-19
sector,last_20_sessions,fipi | Commercial Banks,-12.387,2020-03-19
sector,last_20_sessions,fipi | Fertilizer,-8.583,2020-03-19
sector,last_20_sessions,fipi | Food and Personal Care Products,0.015,2020-03-19
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-16.403,2020-03-19
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,-2.287,2020-03-19
sector,last_20_sessions,fipi | Power Generation and Distribution,-4.925,2020-03-19
sector,last_20_sessions,fipi | Technology and Communication,-0.057,2020-03-19
sector,last_20_sessions,fipi | Textile Composite,-0.308,2020-03-19
sector,last_20_sessions,lipi banks / dfi | All other Sectors,2.904,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Cement,0.02,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,4.854,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Fertilizer,8.789,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.383,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,2.907,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,4.161,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-0.083,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,1.405,2020-03-19
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.317,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-0.75,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Cement,-1.94,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,0.914,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-1.098,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.03,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.5,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.074,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.16,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-0.225,2020-03-19
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.425,2020-03-19
sector,last_20_sessions,lipi companies | All other Sectors,4.213,2020-03-19
sector,last_20_sessions,lipi companies | Cement,3.459,2020-03-19
sector,last_20_sessions,lipi companies | Commercial Banks,-10.539,2020-03-19
sector,last_20_sessions,lipi companies | Fertilizer,-5.399,2020-03-19
sector,last_20_sessions,lipi companies | Food and Personal Care Products,0.073,2020-03-19
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,0.331,2020-03-19
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,1.903,2020-03-19
sector,last_20_sessions,lipi companies | Power Generation and Distribution,0.814,2020-03-19
sector,last_20_sessions,lipi companies | Technology and Communication,1.564,2020-03-19
sector,last_20_sessions,lipi companies | Textile Composite,0.428,2020-03-19
sector,last_20_sessions,lipi individuals | All other Sectors,-16.622,2020-03-19
sector,last_20_sessions,lipi individuals | Cement,-19.707,2020-03-19
sector,last_20_sessions,lipi individuals | Commercial Banks,10.317,2020-03-19
sector,last_20_sessions,lipi individuals | Fertilizer,8.603,2020-03-19
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,-1.046,2020-03-19
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,26.174,2020-03-19
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,0.386,2020-03-19
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,1.013,2020-03-19
sector,last_20_sessions,lipi individuals | Technology and Communication,-2.441,2020-03-19
sector,last_20_sessions,lipi individuals | Textile Composite,0.012,2020-03-19
sector,last_20_sessions,lipi insurance companies | All other Sectors,14.964,2020-03-19
sector,last_20_sessions,lipi insurance companies | Cement,19.476,2020-03-19
sector,last_20_sessions,lipi insurance companies | Commercial Banks,16.828,2020-03-19
sector,last_20_sessions,lipi insurance companies | Fertilizer,7.712,2020-03-19
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,0.165,2020-03-19
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,9.466,2020-03-19
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,1.68,2020-03-19
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,4.477,2020-03-19
sector,last_20_sessions,lipi insurance companies | Technology and Communication,-0.03,2020-03-19
sector,last_20_sessions,lipi insurance companies | Textile Composite,0.597,2020-03-19
sector,last_20_sessions,lipi mutual funds | All other Sectors,8.075,2020-03-19
sector,last_20_sessions,lipi mutual funds | Cement,17.956,2020-03-19
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-9.919,2020-03-19
sector,last_20_sessions,lipi mutual funds | Fertilizer,-10.766,2020-03-19
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,0.416,2020-03-19
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-23.751,2020-03-19
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-5.754,2020-03-19
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-1.755,2020-03-19
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-0.179,2020-03-19
sector,last_20_sessions,lipi mutual funds | Textile Composite,-1.064,2020-03-19
sector,last_20_sessions,lipi nbfc | All other Sectors,0.228,2020-03-19
sector,last_20_sessions,lipi nbfc | Cement,-0.628,2020-03-19
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.412,2020-03-19
sector,last_20_sessions,lipi nbfc | Fertilizer,0.065,2020-03-19
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.001,2020-03-19
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.223,2020-03-19
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.16,2020-03-19
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.029,2020-03-19
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.048,2020-03-19
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.191,2020-03-19
sector,last_20_sessions,lipi other organization | All other Sectors,-1.78,2020-03-19
sector,last_20_sessions,lipi other organization | Cement,1.919,2020-03-19
sector,last_20_sessions,lipi other organization | Commercial Banks,0.345,2020-03-19
sector,last_20_sessions,lipi other organization | Fertilizer,0.677,2020-03-19
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-0.037,2020-03-19
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,0.999,2020-03-19
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.003,2020-03-19
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,0.269,2020-03-19
sector,last_20_sessions,lipi other organization | Technology and Communication,-0.086,2020-03-19
sector,last_20_sessions,lipi other organization | Textile Composite,0.635,2020-03-19

=== FILE: calendar.md ===
# Calendar as of 2020-03-20

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2020-02-19 TREET: Board Meeting
- 2020-02-20 POWER: BOARD MEETING
- 2020-02-20 ASC: Board Meeting
- 2020-02-20 SEARL: Board Meeting
- 2020-02-20 BIPL: Board Meeting - BankIslami Pakistan Limited
- 2020-02-20 STPL: 79th Board of Directors Meeting
- 2020-02-21 FEROZ: Board Meeting
- 2020-02-21 TGL: Board Meeting
- 2020-02-21 ASC: Board Meeting
- 2020-02-21 KEL: Board Meeting other than financial results
- 2020-02-24 SPEL: Board Meeting
- 2020-02-24 SSGC: Board Meeting Other Than Financial Results
- 2020-02-26 SSGC: BOARD MEETING OTHER THAN FINANCIAL RESULTS - POSTPONED
- 2020-02-28 SEARL: Board Meeting Other Than Financial Results
- 2020-03-02 PKGS: BOARD MEETING
- 2020-03-03 AGP: Board Meeting
- 2020-03-03 TREET: Board Meeting Other Than Financial Results
- 2020-03-04 GLAXO: Board of Directors Meeting GSK Pakistan Limited
- 2020-03-10 SSGC: Board Meeting Other Than Financial Results
- 2020-03-11 GLAXO: Board Meeting - Number of Directors
- 2020-03-18 SYS: Board Meeting
- 2020-03-19 KEL: Board Meeting.

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
(no situation-library entry has an outcome that closed before this date, or the library has no INDEX.md)

=== FILE: base_rates.csv ===
type,as_of_cutoff,n,hit_rate,median,p50plus,source
none,,,,,,no base rates available
=== END ===
