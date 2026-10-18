# Replay bundle, close of 2026-07-10

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
# Market as of 2026-07-10 close (public information only)

- KSE100: 182,242 on 2026-07-10; 1m +7.0%, 3m +20.5%, 6m +1.8%, 12m +36.6%
- KMI All Share: 71,041 on 2026-07-10; 1m +6.6%, 3m +19.2%, 6m +2.3%, 12m +27.2%
- Policy rate 11.5%; last MPC decision 2026-06-15: hold (+0bp)
- 6M T-bill cutoff 11.44% (auction 2026-07-08); 3M 11.40%, 12M 11.49%
- CPI YoY 11.08% for 2026-06 (published by 2026-07-03); three months earlier (2026-03) 7.29%
- Brent: 74.34 USD/bbl on 2026-07-10; 3-month change -37.6%
- USD/PKR: 278.31  on 2026-07-10; 3-month change -0.3%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate -0.06pp (market near policy rate); CPI rising over 3 months (+3.8pp)
- Next MPC: see SBP calendar

Session date used: 2026-07-10. Liquid KMI names: 143 (membership KMI_ALL_2026-06-05.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.1318,0.1978,0.1842,2,2
E&P,3,0.0459,0.1485,0.0314,0,0
OMC,4,0.0313,0.456,0.0507,0,0
Power,6,0.041,0.1704,-0.0193,0,0
Fertilizer,4,0.057,0.1365,0.0021,0,0
Cement,16,0.0692,0.2773,-0.0731,0,0
Steel & engineering,11,0.054,0.2975,0.0049,0,0
Autos,12,0.0821,0.4176,0.0303,1,2
Tech & telecom,12,0.0238,0.145,-0.013,0,0
Islamic banks & fin.,10,0.0501,0.2696,0.0295,1,2
Pharma,14,0.0809,0.1883,-0.055,0,0
Textiles,23,0.1726,0.6642,0.2833,0,0
Food & staples,15,0.0056,0.2018,-0.098,0,0
Chemicals,19,0.0954,0.3325,0.0571,1,2
"Glass, packaging, paper",14,0.1472,0.4747,0.1151,0,2
Gas utilities & misc,13,0.115,0.3331,-0.0276,1,1

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AGP,211.2,0.123,0.275,0.03,0.111,-0.103,1.618,0,2026-03-31,0.007,0,0,0,0,15.229,0.039
AIRLINK,153.18,-0.017,0.23,-0.118,0.051,-0.201,1.246,0,2026-03-31,0.111,0,0,0,0,12.707,0.046
ASC,13.85,0.271,0.402,0.124,0.731,-0.361,2.259,2,2026-03-31,,0,0,0,0,,
ATRL,908.93,0.043,0.074,0.308,0.373,-0.066,0.614,0,2026-03-31,,0,2,0,0,8.095,0.015
BFAGRO,36.15,0.087,0.131,-0.17,-0.123,-0.247,1.922,1,,,0,0,0,0,,
BIFO,128.1,-0.033,0.557,-0.1,-0.157,-0.236,0.947,1,2026-03-31,-0.428,0,0,0,0,,
BPL,57.63,0.014,1.552,0.918,0.421,-0.219,2.174,1,,,0,0,0,0,,
CHCC,329.38,0.148,0.337,-0.004,0.151,-0.102,1.815,0,2026-03-31,-0.165,0,0,0,0,6.497,0.019
CNERGY,9.69,0.176,0.344,0.29,0.353,0.0,1.175,0,2024-06-30,,0,0,0,0,,
CPHL,79.02,0.02,0.082,-0.098,-0.071,-0.193,0.903,0,2026-03-31,0.26,0,1,0,0,21.506,0.042
CSAP,107.67,0.105,0.184,0.069,0.004,-0.21,1.415,0,2026-03-31,-1.217,0,0,0,0,,0.065
DFSM,21.56,0.152,2.534,2.857,2.242,-0.344,1.357,5,,,0,0,0,0,,
DGKC,224.49,0.146,0.468,0.001,0.346,-0.166,1.345,0,2026-03-31,0.288,0,0,0,0,7.851,0.012
EFERT,196.6,-0.017,0.012,-0.178,0.089,-0.206,0.892,0,2026-03-31,0.148,0,2,0,0,13.357,0.066
ENGROH,280.7,0.08,0.068,0.129,0.507,-0.058,1.341,0,2026-03-31,4.27,0,1,0,0,5.136,
FABL,101.63,0.144,0.27,0.102,0.383,-0.024,1.288,0,2026-03-31,-0.014,0,0,0,0,6.266,0.07
FATIMA,162.88,0.154,0.305,0.065,0.624,-0.116,1.157,0,2026-03-31,-0.614,0,0,0,0,7.57,0.04
FCCL,55.88,0.056,0.313,-0.012,0.226,-0.085,1.122,0,2025-12-31,0.0,0,0,0,0,8.222,0.028
FCEPL,106.53,0.004,0.506,0.28,0.249,-0.074,0.968,0,2024-09-30,2.03,0,0,0,0,24.633,0.04
FCL,24.19,-0.014,0.155,-0.124,-0.021,-0.128,1.29,0,2026-03-31,0.086,1,0,0,0,12.305,0.021
FFC,561.9,0.013,0.167,-0.026,0.495,-0.138,0.654,0,2025-12-31,-0.021,0,0,0,0,10.107,0.063
FFL,17.58,-0.012,0.183,-0.173,0.094,-0.241,0.819,0,2026-03-31,-0.077,0,0,0,0,45.156,
FML,63.04,0.2,0.614,-0.077,-0.244,-0.293,2.218,2,,,0,0,0,0,,
GAL,607.97,0.291,1.002,0.094,0.403,-0.004,2.512,0,2026-03-31,0.611,0,0,0,0,5.252,0.026
GCIL,37.46,0.257,0.392,0.022,0.344,-0.052,3.272,0,,,0,0,0,0,,
GHGL,40.21,0.171,0.262,0.129,0.056,-0.124,2.698,0,2026-03-31,0.388,1,0,0,0,,
GHNI,1168.32,0.264,0.916,0.448,0.596,0.0,1.124,1,2026-03-31,0.541,0,0,0,0,6.046,0.015
GLAXO,373.01,0.076,0.188,-0.063,-0.031,-0.149,1.461,0,2026-03-31,0.228,0,0,0,0,12.382,0.044
HCAR,245.56,-0.053,0.601,-0.085,-0.117,-0.184,1.466,0,2026-03-31,-0.402,0,0,0,0,15.254,0.028
HUBC,227.05,0.056,0.171,0.055,0.792,-0.036,1.025,0,2026-03-31,-0.021,0,0,0,0,3.875,0.109
IBLHL,55.14,0.118,0.346,-0.153,0.0,-0.313,2.325,1,,,0,0,0,0,,
ILP,103.92,0.255,0.395,0.358,0.512,-0.041,2.67,0,2026-03-31,0.918,0,0,0,0,17.114,0.015
INIL,176.25,0.118,0.218,-0.066,-0.048,-0.255,1.615,1,2026-03-31,-0.172,0,0,0,0,25.968,0.023
ITANZ,42.9,-0.114,0.434,,,,1.951,0,2026-03-31,-0.595,0,2,0,0,,
ITTEFAQ,8.96,0.042,0.226,-0.152,-0.007,-0.261,1.348,1,,,0,0,0,0,,
JVDC,155.37,0.035,0.484,0.292,1.566,-0.03,1.607,0,2026-03-31,2.407,0,0,0,0,14.977,0.078
KEL,8.1,0.016,0.139,0.276,0.579,-0.14,0.586,0,2024-06-30,-0.871,0,1,0,0,30.127,
KOHC,101.46,0.123,0.299,-0.107,0.259,-0.17,1.307,0,2026-03-31,-0.151,0,0,0,0,6.026,
KOHTM,152.39,0.366,2.176,1.62,0.915,-0.204,3.359,1,2026-03-31,-0.209,0,0,0,0,6.163,0.024
KPUS,2081.55,-0.148,5.373,8.723,14.576,-0.221,1.516,2,,,0,0,0,0,,
LOADS,14.56,0.073,0.279,-0.205,-0.11,-0.298,1.626,0,2026-03-31,1.714,0,1,0,0,13.777,
LOTCHEM,31.46,0.078,0.321,0.285,0.755,0.0,2.392,0,2026-03-31,1.204,0,1,0,0,39.488,0.171
LUCK,468.58,0.084,0.236,-0.021,0.331,-0.086,1.098,0,2026-03-31,0.063,0,1,0,0,6.763,0.011
MACFL,78.28,0.286,2.813,1.684,0.464,-0.01,0.333,1,2026-03-31,0.777,2,0,0,0,34.336,0.01
MARI,678.62,0.041,0.07,-0.06,0.112,-0.129,1.368,0,2026-03-31,0.311,0,0,0,0,11.514,0.035
MEBL,557.7,0.137,0.184,0.275,0.669,-0.016,1.37,0,2026-03-31,0.006,0,0,0,0,8.82,0.063
MLCF,104.24,0.212,0.391,-0.107,0.223,-0.2,1.942,0,2024-12-31,0.708,0,0,0,0,7.675,
MTL,298.67,0.069,0.197,0.163,0.145,-0.049,1.888,0,2026-03-31,1.227,0,0,0,0,17.531,0.107
MUGHAL,88.96,0.146,0.435,-0.152,0.257,-0.195,1.333,0,2026-03-31,0.676,1,0,0,0,28.337,
NETSOL,130.57,0.0,0.278,-0.022,-0.184,-0.172,0.609,0,2026-03-31,3.392,0,1,0,0,8.173,
NML,155.0,0.077,0.17,-0.119,0.1,-0.244,1.217,0,2026-03-31,0.835,0,0,0,0,8.671,0.016
NRL,397.63,0.089,0.161,-0.046,0.576,-0.142,0.876,0,2026-03-31,,0,0,0,0,,
OGDC,334.13,0.045,0.225,0.164,0.545,-0.042,0.968,0,2026-03-31,-0.104,0,0,0,0,5.583,0.068
PAEL,45.03,0.12,0.358,-0.217,0.05,-0.286,1.625,0,2026-03-31,0.324,0,0,0,0,13.768,
PIBTL,17.97,0.038,0.24,-0.108,0.981,-0.204,1.252,0,2026-03-31,,0,0,0,0,,
PICT,56.13,0.455,0.854,0.333,0.4,0.0,2.306,3,2026-03-31,0.158,0,0,0,0,,
PPL,236.55,0.05,0.149,-0.013,0.429,-0.144,0.824,0,2026-03-31,-0.06,0,0,0,0,5.148,0.044
PREMA,33.7,-0.002,0.391,-0.139,-0.231,-0.363,1.406,0,2026-03-31,-0.133,0,0,0,0,16.658,
PRL,42.07,0.224,0.21,0.109,0.262,0.0,1.362,0,2026-03-31,,0,0,0,0,,
PSO,354.3,0.014,0.05,-0.268,-0.079,-0.296,1.164,0,2026-03-31,6.803,0,0,0,0,10.778,0.026
QTECH,50.01,0.461,0.587,0.04,0.204,-0.09,3.583,1,2026-03-31,,0,0,0,0,,
QUICE,33.9,-0.112,0.46,0.186,3.021,-0.19,0.62,0,,,0,0,0,0,,
SAZEW,2019.97,-0.043,0.25,0.166,0.747,-0.169,0.4,0,2026-03-31,0.034,0,0,0,0,4.217,0.046
SEARL,95.48,0.055,0.142,-0.242,0.043,-0.293,1.287,0,2026-03-31,,0,1,0,0,,
SGF,118.92,-0.017,0.59,0.053,0.523,-0.115,0.816,0,2026-03-31,3.0,0,0,0,0,,
SGPL,113.61,1.142,4.465,2.654,14.088,-0.032,1.406,7,2026-03-31,,0,3,0,0,,
SHDT,64.27,0.194,0.646,0.188,0.033,-0.148,2.848,1,,,0,0,0,0,,
SNGP,112.4,0.113,0.268,-0.058,-0.045,-0.178,1.71,0,2026-03-31,0.226,0,0,0,0,5.073,0.026
SSGC,30.83,0.152,0.462,-0.149,-0.328,-0.323,1.898,0,2026-03-31,-0.48,0,0,0,0,10.954,0.012
SYM,11.61,0.116,0.13,-0.186,-0.189,-0.273,1.508,1,2026-03-31,-0.8,0,0,0,0,,
SYS,143.51,-0.028,0.052,-0.142,0.23,-0.151,0.879,0,2026-03-31,0.199,1,0,0,0,22.795,0.012
TELE,9.17,0.023,0.211,-0.225,0.096,-0.308,0.884,0,2026-03-31,0.464,0,0,0,0,18.478,
THCCL,72.84,0.049,0.381,-0.136,0.954,-0.267,1.734,0,2026-03-31,0.554,0,0,0,0,6.723,0.005
TOMCL,41.43,0.218,0.337,-0.19,0.322,-0.375,2.33,0,2026-03-31,-0.848,0,0,0,0,13.655,
TREET,24.73,0.007,0.16,-0.228,0.039,-0.316,1.024,0,2026-03-31,-1.0,3,0,0,0,17.461,
UNITY,10.26,-0.116,0.278,-0.514,-0.616,-0.666,0.374,0,2025-09-30,,0,0,0,0,18.228,
ZAL,43.47,-0.037,0.132,-0.081,0.874,-0.399,0.919,0,2026-03-31,-3.118,0,0,0,0,6.31,0.062

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2026-06-11,ARPL,material_info,Material Information
2026-06-11,MQTM,material_info,Material Information
2026-06-11,BML,material_info,Material Information
2026-06-11,SEARL,material_info,Material Information
2026-06-11,BML,material_info,Material Information
2026-06-11,SYS,financial_result,236th Emergent Board Meeting Other Than Financial Results
2026-06-11,HALEON,dividend_or_bonus,Reminder for Conversion of Physical Shares to Book Entry Form & Unclaimed D
2026-06-11,GCWL,dividend_or_bonus,GCWL | Ghani ChemWorld Limited Issuance of Right Shares 0.50% Right Issue o
2026-06-11,KEL,dividend_or_bonus,"Book Closure of Rated Unsecured & Retail Listed, Shirkat-ul-Aqd Sukuk"
2026-06-12,ITANZ,material_info,Material Information
2026-06-12,IDSM,material_info,MATERIAL INFORMATION
2026-06-12,MUGHAL,financial_result,Emergent Board Meeting - Other Than Financial Results
2026-06-12,MTL,dividend_or_bonus,Notice of book closure for sub division of shares
2026-06-12,HINOON,dividend_or_bonus,Mandatory Conversion of Physical Shares to Book-Entry Form Unclaimed Divide
2026-06-15,SHFA,material_info,Material Information
2026-06-15,WAVESAPP,material_info,Material Information
2026-06-15,PACE,material_info,Material Information
2026-06-15,PIOC,material_info,Material Information
2026-06-16,GCWL,dividend_or_bonus,SUBSCRIPTION OF RIGHT SHARES BY THE DIRECTORS - GHANI CHEMWORLD LIMITED
2026-06-17,ATRL,material_info,Disclosure of Material Information - Receipt of an offer to acquire 70% sha
2026-06-17,NETSOL,material_info,Material Information
2026-06-17,ITANZ,material_info,Material Information
2026-06-18,BAFL,material_info,Disclosure of Material Information - Bank Alfalah Limited
2026-06-18,ENGROH,material_info,Material Information
2026-06-19,AVN,material_info,Material Information
2026-06-19,ATRL,material_info,Material Information
2026-06-19,GEMPACRA,material_info,Material Information
2026-06-19,GHGL,financial_result,DECISION OF BOARD MEETING OTHER THAN FINANCIAL RESULTS
2026-06-22,LOADS,material_info,Material Information
2026-06-22,PINL,material_info,Material Information
2026-06-22,CPPL,material_info,MATERIAL INFORMATION
2026-06-22,FCL,financial_result,Approval of the Annual Budget for Financial Year 2026-27
2026-06-23,LSECL,material_info,Material Information
2026-06-23,PPVC,material_info,Material Information
2026-06-23,SKRS,material_info,Material Information - Revival Plan SKRS
2026-06-24,TPLT,material_info,Material Information
2026-06-24,TPL,material_info,Material Information
2026-06-24,AMBL,material_info,Material Information
2026-06-24,LIVEN,material_info,MATERIAL INFORMATION SIGNING OF MOU WITH TOFFLON THE TECH GIANT OF CHINA
2026-06-24,ZUMA,material_info,Material Information
2026-06-29,SGPL,material_info,Material Information
2026-06-29,SRVI,material_info,Material Information
2026-06-29,EFUL,material_info,Disclosure of Material Information
2026-06-29,SLM,material_info,Material Information
2026-06-29,EFUG,material_info,Disclosure of Material Information
2026-06-29,MACFL,financial_result,Emergent Board Meeting Other Than Financial Results
2026-06-29,TREET,financial_result,Conclusion of Board Meeting Other Than Financial Results (Appointment of Ch
2026-06-30,IPAK,material_info,Material Information
2026-06-30,HINOON,material_info,Material Information- Shariah Screening Compliance Confirmation REVOKED
2026-06-30,DEL,material_info,Material Information
2026-06-30,TREET,financial_result,Conclusion of Board Meeting Other Than Financial Results (Appointment of Ch
2026-07-01,PTC,material_info,Material Information
2026-07-01,RMPL,material_info,Material Information
2026-07-01,STL,material_info,Material Information - Award of Contract Valued at Approximately PKR 1 Bill
2026-07-01,SPCL,material_info,Material Informarion
2026-07-01,PTL,material_info,Material Information
2026-07-01,LUCK,material_info,Material Information
2026-07-01,KEL,material_info,Disclosure of Material Information
2026-07-01,MACFL,financial_result,Announcement - Board Meeting other than Financial Results
2026-07-01,GHGL,dividend_or_bonus,GHGL | Ghani Glass Limited Revision of Book Closure Date - Ghani Glass Limi
2026-07-02,ANL,material_info,Material Information
2026-07-02,PIAHCLA,material_info,Material Information
2026-07-02,PINL,material_info,Material Information - Appointment of Chairman and Chief Executive Officer
2026-07-03,ANSM,material_info,Material Information
2026-07-03,JSCL,material_info,Material Information
2026-07-03,EFERT,material_info,Material Information
2026-07-03,MUGHAL,dividend_or_bonus,Sukuk V - Notice of book closure
2026-07-06,TATM,material_info,Material Information Successful Completion and Commencement of Operations a
2026-07-06,PAKL,material_info,Material Information
2026-07-06,KOHC,insider_trade,Insider trade disclosure
2026-07-06,LSEVL,insider_trade,Insider trade disclosure
2026-07-06,LSECL,insider_trade,Insider trade disclosure
2026-07-06,IPAK,insider_trade,Insider trade disclosure
2026-07-06,ASC,insider_trade,Insider trade disclosure
2026-07-06,TPLP,insider_trade,Insider trade disclosure
2026-07-07,JSGCL,material_info,Material information
2026-07-07,SGPL,material_info,MATERIAL INFORMATION
2026-07-07,BAPL,insider_trade,Insider trade disclosure
2026-07-07,SHFA,insider_trade,Insider trade disclosure
2026-07-07,BAPL,insider_trade,Insider trade disclosure
2026-07-07,RMPL,insider_trade,Insider trade disclosure
2026-07-08,SGPL,material_info,MATERIAL INFORMATION
2026-07-08,CPHL,material_info,Material Information
2026-07-08,KHTC,material_info,Material Information
2026-07-08,ZUMA,material_info,Material Information
2026-07-08,LSEVL,insider_trade,Insider trade disclosure
2026-07-08,LSECL,insider_trade,Insider trade disclosure
2026-07-08,LSECL,insider_trade,Insider trade disclosure
2026-07-08,UBL,insider_trade,Insider trade disclosure
2026-07-08,GOC,insider_trade,Insider trade disclosure
2026-07-08,LEUL,insider_trade,Insider trade disclosure
2026-07-08,SHSML,insider_trade,DISCLOSURE OF INTEREST BY AN ASSOCIATED COMPANY
2026-07-08,PKGS,insider_trade,Insider trade disclosure
2026-07-08,HAEL,insider_trade,Insider trade disclosure
2026-07-08,ILP,insider_trade,Insider trade disclosure
2026-07-08,TCORP,insider_trade,Intimation of Subscription of Right Shares by Directors / Substantial Share
2026-07-08,ZUMA,insider_trade,Insider trade disclosure
2026-07-08,WAVES,insider_trade,Insider trade disclosure
2026-07-08,WAVESAPP,insider_trade,Insider trade disclosure
2026-07-09,GDL,material_info,Material Information
2026-07-09,BAFL,material_info,Disclosure of Material Information - Bank Alfalah Limited
2026-07-09,LOTCHEM,material_info,Disclosure of Material Information
2026-07-09,TREET,financial_result,CONCLUSION OF BOARD MEETING OTHER THAN FINANCIAL RESULTS
2026-07-09,HCAR,dividend_or_bonus,Credit of Final Cash Dividend
2026-07-09,AKBL,insider_trade,Insider trade disclosure
2026-07-09,SIEM,insider_trade,Insider trade disclosure
2026-07-09,UBL,insider_trade,Insider trade disclosure
2026-07-09,TCORP,insider_trade,Auditors Certificate Regarding Subscription of Right Shares by Directors / 
2026-07-09,LSECL,insider_trade,Insider trade disclosure
2026-07-09,KOHC,insider_trade,Insider trade disclosure
2026-07-09,IGIHL,insider_trade,Insider trade disclosure
2026-07-09,PKGS,insider_trade,Insider trade disclosure
2026-07-09,TPLRF1,insider_trade,Insider trade disclosure
2026-07-10,EFERT,material_info,DISCLOSURE OF MATERIAL INFORMATION
2026-07-10,SLCL,material_info,Material Information
2026-07-10,MQTM,material_info,MATERIAL INFORMATION
2026-07-10,PPL,dividend_or_bonus,Notice to Shareholders Unclaimed Dividends
2026-07-10,GCWL,dividend_or_bonus,STATUS OF 0.50% RIGHT SHARES SUBSCRIPTION - GHANI CHEMWORLD LIMITED
2026-07-10,ITANZ,dividend_or_bonus,Material Information - Increase in Paid-up Capital and declaration of inter
2026-07-10,ITANZ,dividend_or_bonus,Material Information - Increase in Authorized Capital and Declaration of In
2026-07-10,UBL,insider_trade,Insider trade disclosure
2026-07-10,TPLT,insider_trade,Insider trade disclosure
2026-07-10,TPL,insider_trade,Insider trade disclosure
2026-07-10,TPLI,insider_trade,Insider trade disclosure
2026-07-10,HAEL,insider_trade,Insider trade disclosure
2026-07-10,CRTM,insider_trade,Insider trade disclosure

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-10.066,2026-07-09
investor_type,last_5_sessions,broker proprietary trading,2.749,2026-07-09
investor_type,last_5_sessions,companies,-22.767,2026-07-09
investor_type,last_5_sessions,foreign corporates,9.267,2026-07-09
investor_type,last_5_sessions,foreign individual,0.005,2026-07-09
investor_type,last_5_sessions,individuals,12.657,2026-07-09
investor_type,last_5_sessions,insurance companies,15.598,2026-07-09
investor_type,last_5_sessions,mutual funds,-5.01,2026-07-09
investor_type,last_5_sessions,nbfc,0.524,2026-07-09
investor_type,last_5_sessions,other organization,-2.896,2026-07-09
investor_type,last_5_sessions,overseas pakistani,-0.061,2026-07-09
sector,last_5_sessions,fipi | All other Sectors,9.282,2026-07-09
sector,last_5_sessions,fipi | Cement,2.284,2026-07-09
sector,last_5_sessions,fipi | Commercial Banks,-0.038,2026-07-09
sector,last_5_sessions,fipi | Debt Market,-0.004,2026-07-09
sector,last_5_sessions,fipi | Fertilizer,0.128,2026-07-09
sector,last_5_sessions,fipi | Food and Personal Care Products,0.073,2026-07-09
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,0.612,2026-07-09
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,0.3,2026-07-09
sector,last_5_sessions,fipi | Power Generation and Distribution,-1.336,2026-07-09
sector,last_5_sessions,fipi | Technology and Communication,-0.827,2026-07-09
sector,last_5_sessions,fipi | Textile Composite,-1.263,2026-07-09
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-0.162,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Cement,4.406,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,1.216,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Debt Market,-17.848,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Fertilizer,0.515,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,0.087,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,-0.632,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,1.16,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.968,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,-0.698,2026-07-09
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.922,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-0.044,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.174,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.73,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Debt Market,-0.0,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.143,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.001,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,1.171,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.006,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.434,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,0.169,2026-07-09
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.024,2026-07-09
sector,last_5_sessions,lipi companies | All other Sectors,-15.106,2026-07-09
sector,last_5_sessions,lipi companies | Cement,-2.623,2026-07-09
sector,last_5_sessions,lipi companies | Commercial Banks,-2.529,2026-07-09
sector,last_5_sessions,lipi companies | Fertilizer,0.067,2026-07-09
sector,last_5_sessions,lipi companies | Food and Personal Care Products,-0.227,2026-07-09
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,1.127,2026-07-09
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,-3.577,2026-07-09
sector,last_5_sessions,lipi companies | Power Generation and Distribution,0.415,2026-07-09
sector,last_5_sessions,lipi companies | Technology and Communication,-0.762,2026-07-09
sector,last_5_sessions,lipi companies | Textile Composite,0.449,2026-07-09
sector,last_5_sessions,lipi individuals | All other Sectors,2.311,2026-07-09
sector,last_5_sessions,lipi individuals | Cement,-2.94,2026-07-09
sector,last_5_sessions,lipi individuals | Commercial Banks,-0.156,2026-07-09
sector,last_5_sessions,lipi individuals | Debt Market,-0.052,2026-07-09
sector,last_5_sessions,lipi individuals | Fertilizer,2.455,2026-07-09
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,0.449,2026-07-09
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,5.034,2026-07-09
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,1.458,2026-07-09
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,1.536,2026-07-09
sector,last_5_sessions,lipi individuals | Technology and Communication,1.68,2026-07-09
sector,last_5_sessions,lipi individuals | Textile Composite,0.883,2026-07-09
sector,last_5_sessions,lipi insurance companies | All other Sectors,-0.254,2026-07-09
sector,last_5_sessions,lipi insurance companies | Cement,0.918,2026-07-09
sector,last_5_sessions,lipi insurance companies | Commercial Banks,0.233,2026-07-09
sector,last_5_sessions,lipi insurance companies | Debt Market,14.445,2026-07-09
sector,last_5_sessions,lipi insurance companies | Fertilizer,0.32,2026-07-09
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,-0.077,2026-07-09
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-0.527,2026-07-09
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.526,2026-07-09
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,0.16,2026-07-09
sector,last_5_sessions,lipi insurance companies | Technology and Communication,-0.009,2026-07-09
sector,last_5_sessions,lipi insurance companies | Textile Composite,-0.138,2026-07-09
sector,last_5_sessions,lipi mutual funds | All other Sectors,5.362,2026-07-09
sector,last_5_sessions,lipi mutual funds | Cement,-3.635,2026-07-09
sector,last_5_sessions,lipi mutual funds | Commercial Banks,2.085,2026-07-09
sector,last_5_sessions,lipi mutual funds | Debt Market,2.501,2026-07-09
sector,last_5_sessions,lipi mutual funds | Fertilizer,-3.145,2026-07-09
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,0.279,2026-07-09
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-6.813,2026-07-09
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.206,2026-07-09
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-1.199,2026-07-09
sector,last_5_sessions,lipi mutual funds | Technology and Communication,0.226,2026-07-09
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.878,2026-07-09
sector,last_5_sessions,lipi nbfc | All other Sectors,0.176,2026-07-09
sector,last_5_sessions,lipi nbfc | Cement,0.037,2026-07-09
sector,last_5_sessions,lipi nbfc | Commercial Banks,0.112,2026-07-09
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.02,2026-07-09
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,0.052,2026-07-09
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.107,2026-07-09
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.009,2026-07-09
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.027,2026-07-09
sector,last_5_sessions,lipi nbfc | Technology and Communication,0.031,2026-07-09
sector,last_5_sessions,lipi nbfc | Textile Composite,0.048,2026-07-09
sector,last_5_sessions,lipi other organization | All other Sectors,-1.565,2026-07-09
sector,last_5_sessions,lipi other organization | Cement,1.378,2026-07-09
sector,last_5_sessions,lipi other organization | Commercial Banks,-1.653,2026-07-09
sector,last_5_sessions,lipi other organization | Debt Market,0.956,2026-07-09
sector,last_5_sessions,lipi other organization | Fertilizer,-0.464,2026-07-09
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,-0.635,2026-07-09
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.079,2026-07-09
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.077,2026-07-09
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,-0.951,2026-07-09
sector,last_5_sessions,lipi other organization | Technology and Communication,0.192,2026-07-09
sector,last_5_sessions,lipi other organization | Textile Composite,0.001,2026-07-09
investor_type,last_20_sessions,banks / dfi,24.668,2026-07-09
investor_type,last_20_sessions,broker proprietary trading,1.937,2026-07-09
investor_type,last_20_sessions,companies,206.193,2026-07-09
investor_type,last_20_sessions,foreign corporates,-178.32,2026-07-09
investor_type,last_20_sessions,foreign individual,0.031,2026-07-09
investor_type,last_20_sessions,individuals,-47.611,2026-07-09
investor_type,last_20_sessions,insurance companies,-64.638,2026-07-09
investor_type,last_20_sessions,mutual funds,45.296,2026-07-09
investor_type,last_20_sessions,nbfc,0.414,2026-07-09
investor_type,last_20_sessions,other organization,-4.114,2026-07-09
investor_type,last_20_sessions,overseas pakistani,16.143,2026-07-09
sector,last_20_sessions,fipi | All other Sectors,3.322,2026-07-09
sector,last_20_sessions,fipi | Cement,-9.132,2026-07-09
sector,last_20_sessions,fipi | Commercial Banks,12.649,2026-07-09
sector,last_20_sessions,fipi | Debt Market,-0.13,2026-07-09
sector,last_20_sessions,fipi | Fertilizer,-0.196,2026-07-09
sector,last_20_sessions,fipi | Food and Personal Care Products,-157.673,2026-07-09
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-1.817,2026-07-09
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,1.006,2026-07-09
sector,last_20_sessions,fipi | Power Generation and Distribution,-4.466,2026-07-09
sector,last_20_sessions,fipi | Technology and Communication,-2.787,2026-07-09
sector,last_20_sessions,fipi | Textile Composite,-2.922,2026-07-09
sector,last_20_sessions,lipi banks / dfi | All other Sectors,-1.342,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Cement,6.43,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,3.784,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Debt Market,20.209,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-1.713,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.082,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,1.873,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-0.798,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,0.202,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,-6.037,2026-07-09
sector,last_20_sessions,lipi banks / dfi | Textile Composite,1.978,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-4.832,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Cement,1.128,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,4.833,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.114,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,0.02,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.415,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.351,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.023,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.169,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-0.156,2026-07-09
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,0.102,2026-07-09
sector,last_20_sessions,lipi companies | All other Sectors,-3.318,2026-07-09
sector,last_20_sessions,lipi companies | Cement,-3.13,2026-07-09
sector,last_20_sessions,lipi companies | Commercial Banks,2.44,2026-07-09
sector,last_20_sessions,lipi companies | Debt Market,1.51,2026-07-09
sector,last_20_sessions,lipi companies | Fertilizer,0.183,2026-07-09
sector,last_20_sessions,lipi companies | Food and Personal Care Products,215.562,2026-07-09
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,0.4,2026-07-09
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,-5.433,2026-07-09
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-0.361,2026-07-09
sector,last_20_sessions,lipi companies | Technology and Communication,-0.957,2026-07-09
sector,last_20_sessions,lipi companies | Textile Composite,-0.704,2026-07-09
sector,last_20_sessions,lipi individuals | All other Sectors,6.416,2026-07-09
sector,last_20_sessions,lipi individuals | Cement,-15.903,2026-07-09
sector,last_20_sessions,lipi individuals | Commercial Banks,-1.798,2026-07-09
sector,last_20_sessions,lipi individuals | Debt Market,-0.649,2026-07-09
sector,last_20_sessions,lipi individuals | Fertilizer,4.245,2026-07-09
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,-61.068,2026-07-09
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,5.348,2026-07-09
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,10.06,2026-07-09
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,0.298,2026-07-09
sector,last_20_sessions,lipi individuals | Technology and Communication,2.636,2026-07-09
sector,last_20_sessions,lipi individuals | Textile Composite,2.803,2026-07-09
sector,last_20_sessions,lipi insurance companies | All other Sectors,-19.683,2026-07-09
sector,last_20_sessions,lipi insurance companies | Cement,0.037,2026-07-09
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-41.047,2026-07-09
sector,last_20_sessions,lipi insurance companies | Debt Market,6.837,2026-07-09
sector,last_20_sessions,lipi insurance companies | Fertilizer,0.195,2026-07-09
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,-0.871,2026-07-09
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-3.979,2026-07-09
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-0.407,2026-07-09
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,-3.766,2026-07-09
sector,last_20_sessions,lipi insurance companies | Technology and Communication,-0.285,2026-07-09
sector,last_20_sessions,lipi insurance companies | Textile Composite,-1.67,2026-07-09
sector,last_20_sessions,lipi mutual funds | All other Sectors,20.359,2026-07-09
sector,last_20_sessions,lipi mutual funds | Cement,18.978,2026-07-09
sector,last_20_sessions,lipi mutual funds | Commercial Banks,26.956,2026-07-09
sector,last_20_sessions,lipi mutual funds | Debt Market,-37.288,2026-07-09
sector,last_20_sessions,lipi mutual funds | Fertilizer,-1.827,2026-07-09
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,2.274,2026-07-09
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,3.847,2026-07-09
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-3.951,2026-07-09
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,9.264,2026-07-09
sector,last_20_sessions,lipi mutual funds | Technology and Communication,5.596,2026-07-09
sector,last_20_sessions,lipi mutual funds | Textile Composite,1.086,2026-07-09
sector,last_20_sessions,lipi nbfc | All other Sectors,0.255,2026-07-09
sector,last_20_sessions,lipi nbfc | Cement,-0.003,2026-07-09
sector,last_20_sessions,lipi nbfc | Commercial Banks,0.127,2026-07-09
sector,last_20_sessions,lipi nbfc | Fertilizer,-0.021,2026-07-09
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.03,2026-07-09
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.138,2026-07-09
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.059,2026-07-09
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,-0.16,2026-07-09
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.045,2026-07-09
sector,last_20_sessions,lipi nbfc | Textile Composite,0.063,2026-07-09
sector,last_20_sessions,lipi other organization | All other Sectors,-1.177,2026-07-09
sector,last_20_sessions,lipi other organization | Cement,1.594,2026-07-09
sector,last_20_sessions,lipi other organization | Commercial Banks,-7.944,2026-07-09
sector,last_20_sessions,lipi other organization | Debt Market,9.625,2026-07-09
sector,last_20_sessions,lipi other organization | Fertilizer,-0.886,2026-07-09
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,1.248,2026-07-09
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,-6.161,2026-07-09
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.442,2026-07-09
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,-1.18,2026-07-09
sector,last_20_sessions,lipi other organization | Technology and Communication,1.945,2026-07-09
sector,last_20_sessions,lipi other organization | Textile Composite,-0.736,2026-07-09

=== FILE: calendar.md ===
# Calendar as of 2026-07-10

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2026-06-11 ATRL: BOARD MEETING TO CONSODER CORPORATE BUDGET 2026-2027
- 2026-06-11 NRL: Board Meeting Other Than Financial Results
- 2026-06-12 LCI: Board Meeting Other Than Financial Results
- 2026-06-12 GCIL: MEETING OF THE BOARD OF DIRECTORS OTHER THAN FINANCIAL RESULTS - GHANI CHEMICAL INDUSTRIES LIMITED
- 2026-06-12 GGL: Board Meeting Other Than Financial Results - GHANI GLOBAL HOLDINGS LIMITED
- 2026-06-12 GHGL: Board Meeting Other Than Financial Results
- 2026-06-12 CRTM: Board Meeting Other Than Financial Results
- 2026-06-15 GADT: Board Meeting other than Financial Results
- 2026-06-15 FCL: Board Meeting other than Financial Results
- 2026-06-15 CHCC: Board Meeting Other Than Financial Result
- 2026-06-16 TPLRF1: Board Meeting Other Than Financial Results REVOKED
- 2026-06-16 GTYR: Board Meeting Other Than Financial Results
- 2026-06-17 GAL: Board Meeting Other Than Financial Results
- 2026-06-17 GHNI: Board Meeting Other Than Financial Results
- 2026-06-18 ISL: BOARD MEETING - OTHER THAN FINANCIAL RESULTS
- 2026-06-18 FCCL: Board Meeting Other Than Financial Results
- 2026-06-18 SKRS: Board Meeting Other Than Financial Results
- 2026-06-19 SHFA: Board Meeting Other Than Financial Results
- 2026-06-19 IPAK: Board Meeting Other Than Financial Results
- 2026-06-19 BBFL: Board Meeting for approval of Budget for the year 2026-27
- 2026-06-19 PRL: Board Meeting Other than Financial Results
- 2026-06-19 CRTM: Board Meeting Other Than Financial Results
- 2026-06-22 ILP: Notice of Board Meeting Other Than Financial Results / Closed Period
- 2026-06-22 TATM: Board Meeting Other Than Financial Results
- 2026-06-22 STCL: Board Meeting Other Than Financial Results
- 2026-06-22 LOADS: Board Meeting Other Than Financial Results
- 2026-06-22 SRVI: Board Meeting Other Than Financial Results
- 2026-06-22 TREET: Board Meeting Other Than Financial Results
- 2026-06-22 CSAP: Board Meeting for Company Strategy and Operating Budget
- 2026-06-22 PRL: Board Meeting Rescheduled
- 2026-06-23 KEL: Board Meeting Other Than Financial Results
- 2026-06-24 CHCC: BOARD MEETING OTHER THAN FINANCIAL RESULTS
- 2026-06-24 GAL: Board Meeting other than financial results
- 2026-06-29 SHFA: Board Meeting Other Than Financial Results
- 2026-06-29 GHNI: Board Meeting Other than Financial Results
- 2026-06-30 TATM: Board of Directors Meeting - Other than Financial Results Budget Approval 2026-27
- 2026-06-30 KEL: Board Meeting Other Than Financial Results
- 2026-07-01 CPHL: Board Meeting Other Than Financial Results
- 2026-07-02 FABL: Board Meeting Other Than Financial Results of Faysal Bank Limited
- 2026-07-02 TREET: Board Meeting Other Than Financial Results
- 2026-07-06 ACPL: Board Meeting Other Than Financial Results
- 2026-07-06 BFBIO: Board Meeting Other Than Financial Results
- 2026-07-07 FEROZ: Board Meeting Other Than Financial Results
- 2026-07-07 WAVES: Board Meeting other than Financial Results
- 2026-07-08 WAHDAT: Board Meeting Other Than Financial Results
- 2026-07-08 STL: Board Meeting Other Than Financial Results
- 2026-07-09 LOTCHEM: Board Meeting _ Closed Period
- 2026-07-09 GCWL: MEETING OF THE BOARD OF DIRECTORS OTHER THAN FINANCIAL RESULTS - GHANI CHEMWORLD LIMITED

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
**Finance ministry and IMF.** The ministry wants the primary surplus, clean reviews and market access (a Eurobond was issued before Apr 2026 per the MPS). The IMF enforces numbers and cost recovery: the captive-gas levy was a structural benchmark and the IMF refused to revise it (Profit, 28 Mar 2025); fertilizer subsidies were refused in 2023 (Tribune). It lets slide dates and stocks. DISCO sales promised for Jan 2025 (Profit, 12 Oct 2024) had reached only expressions of interest by May 2026. FB
**Establishment and SIFC.** The SIFC (created mid-2023, army chief a member, agriculture, mining and IT focus, IMF asked about its powers) was described by a government adviser to mining.com (date not shown). Reuters in 2020 reported the military as the most influential voice on Reko Diq. Establishment-linked capital is visible in listed names: Fauji Foundation owns 44.32% of FFC (FFC H1-26 report), FFC holds 33.99% of the PIA buyer (repo), a Fauji Foundation and KAPCO group bought Attock Cement
| 1 | Brownfield refinery policy | 17 Aug 2023 | outcome not shown |
| 3 | OMC margin +Rs1.22 | OCAC ask Apr 2025 | outcome not shown |
| 6 | Rs1.225tn power bank facility | 2025 | outcome not shown |
| 7 | IPP terminations | 2024 (unverified) | 5 PPAs ended Oct 2024; Rs1tn savings claimed 29 Dec. Y |
| 8 | PIA sale | Auction 31 Oct 2024 failed | Sold 23 Dec 2025, closed 29 Jun 2026. Y |
| 9 | DISCO sales | Oct 2024: two by Jan 2025 | outcome not shown |
| 10 | K-Electric to Shanghai Electric | PAI 27 Mar 2018 | outcome not shown |
| 11 | OGDC 7%, PPL 10% sale | CCoP 21 Aug 2020 | outcome not shown |
| 12 | Six SOEs sold in FY20 | 29 Jan 2020 | outcome not shown |
| 13 | Super tax cut | Budget 12 Jun 2026 | Finance Act 27 Jun 2026. Y |
| 14 | Cement FED | Jun 2024 | Effective Jul 2024; no reversal. Y |
| 15 | Rs170bn mini-budget | 10 Feb 2023 | outcome not shown |
| 16 | Captive gas levy | Ordinance Jan 2025 | outcome not shown |
| 17 | GIDC recovery | SC Aug 2020 | outcome not shown |
| 18 | End subsidised RLNG to fertilizer | 2023 | outcome not shown |
| 19 | Exporter power tariff Rs19.99 | 6 Oct 2022 | outcome not shown |
| 20 | Panda bond | "this year" 2024 | outcome not shown |
| 22 | Net-metering reform | Draft Dec 2025 | Notified 9 Feb 2026; partly reversed. Y |
| 23 | IMF EFF Board | Staff deal 12 Jul 2024 | 25 Sep 2024. Y |
| 24 | Windfall recovery Rs72bn | 26 May 2026 | outcome not shown |
**SBP guidance.** Conditional language ("barring shocks", "prepared to act") was followed by action within 2 to 7 weeks three times (Jun 2023, Mar-Apr 2022, Mar-Apr 2026). "Outlook broadly unchanged" with real above +4.7 preceded a cut (Dec 2025). Read the real rate and the external account, not the adjectives.
**A sponsor announces expansion.** Self-funded capex gets built: Lucky’s Karachi expansion to 15.6 Mtpa was filed 1 Jul 2026 and the group reports Rs319bn invested in ten years. Diversification into state-directed or loss-making assets costs minorities: FFC’s PIA Rs30.6bn paid plus Rs30.6bn due. An expansion alongside an authorised-capital increase means a rights issue: Noventra doubled authorised capital to Rs40bn on 22 Sep with Rs2.2bn cash against Rs25.8bn needed (`deals.md`), and PRL’s upgra
**"No plan to raise prices or taxes."** I found no dated denial followed by a reversal, so the base rate is unmeasured. Dated facts only: Rs170bn of taxes announced 10 Feb 2023; a November 2024 denial of mini-budget rumours after an IMF visit (Aaj), with no mini-budget found since (unverified); a pledge of contingency tax measures from Jan 2026 if revenue lagged (Tribune) with no verified outcome.

=== FILE: situations.md ===
(no situation-library entry has an outcome that closed before this date, or the library has no INDEX.md)

=== FILE: base_rates.csv ===
type,as_of_cutoff,n,hit_rate,median,p50plus,source
none,,,,,,no base rates available
=== END ===
