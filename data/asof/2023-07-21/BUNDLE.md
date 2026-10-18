# Replay bundle, close of 2023-07-21

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
# Market as of 2023-07-21 close (public information only)

- KSE100: 45,921 on 2023-07-21; 1m +13.0%, 3m +14.2%, 6m +13.9%, 12m +11.0%
- KMI All Share: 22,421 on 2023-07-21; 1m +10.8%, 3m +16.5%, 6m +13.3%, 12m +7.4%
- Policy rate 22.0%; last MPC decision 2023-06-26: hike (+100bp)
- 6M T-bill cutoff 22.96% (auction 2023-07-12); 3M 22.80%, 12M 22.99%
- CPI YoY 29.4% for 2023-06 (published by 2023-07-03); three months earlier (2023-03) 35.38%
- Brent: 81.06 USD/bbl on 2023-07-21; 3-month change -2.8%
- USD/PKR: 285.11  on 2023-07-21; 3-month change +0.5%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.96pp (market pricing hikes); CPI falling over 3 months (-6.0pp)
- Next MPC: see SBP calendar

Session date used: 2023-07-21. Liquid KMI names: 57 (membership KMI_ALL_derived_2023-07-10.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.2433,0.2271,0.154,0,0
E&P,3,0.1415,0.0301,0.0176,0,0
OMC,4,0.1335,0.1561,-0.027,0,0
Power,5,0.1293,0.0299,0.029,1,1
Fertilizer,4,0.0066,-0.0036,0.0164,0,0
Cement,16,0.0815,0.1838,0.2349,0,1
Steel & engineering,10,0.1835,0.0875,0.0905,0,0
Autos,12,0.2202,0.1972,0.1678,0,1
Tech & telecom,8,0.161,0.0797,0.0412,0,0
Islamic banks & fin.,8,0.1231,0.1341,0.1091,1,2
Pharma,12,0.128,0.0817,0.0095,0,0
Textiles,22,0.0907,0.168,0.2619,0,0
Food & staples,13,0.147,0.2452,0.1913,1,1
Chemicals,18,0.0959,0.0701,0.057,0,0
"Glass, packaging, paper",13,0.0988,0.1326,0.1252,0,0
Gas utilities & misc,10,-0.0082,-0.0563,-0.1611,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ACPL,90.03,0.134,0.562,0.555,0.288,-0.074,0.597,0,2023-03-31,0.244,0,0,0,0,8.161,0.053
AGHA,10.68,0.074,-0.106,-0.154,-0.282,-0.355,1.158,0,,,0,2,0,0,,
AGP,59.19,0.172,0.105,-0.014,-0.249,-0.306,2.09,0,2023-03-31,-0.359,0,1,0,0,11.591,0.031
AIRLINK,25.31,0.291,0.398,0.021,-0.339,-0.36,2.077,1,2023-03-31,-0.533,0,1,0,0,10.434,0.025
ATBA,228.42,0.083,0.53,0.666,1.061,-0.006,1.486,0,,,0,0,0,0,,
ATRL,206.46,0.23,0.198,0.267,0.384,-0.033,1.737,0,2023-03-31,2.222,0,0,0,0,1.447,0.057
AVN,54.38,0.224,-0.04,-0.063,-0.174,-0.279,2.404,0,2023-03-31,-0.049,0,2,0,0,,
BIPL,18.49,0.081,0.744,0.481,0.856,-0.016,2.213,0,2023-03-31,2.447,0,4,1,0,,
CHCC,128.6,0.106,0.132,0.279,0.468,-0.056,0.916,0,2023-03-31,0.195,0,0,0,0,4.057,0.032
COLG,1475.5,0.146,1.096,1.171,0.953,-0.089,2.031,2,2023-03-31,0.751,0,0,0,0,27.87,0.023
CPHL,23.72,0.096,-0.086,0.011,-0.262,-0.316,1.328,0,2023-03-31,-0.554,0,0,0,0,11.407,
DGKC,54.93,0.098,0.22,0.198,-0.016,-0.154,1.027,0,2023-03-31,-0.222,0,0,0,0,8.664,0.016
DOL,26.51,0.153,-0.037,0.445,0.899,-0.062,1.291,1,,,0,0,0,0,,
EFERT,82.15,0.012,-0.052,0.052,-0.085,-0.096,1.302,0,2023-03-31,-0.201,0,0,0,0,6.416,0.176
EPCL,43.87,0.065,0.03,0.103,-0.324,-0.289,1.467,0,2023-03-31,-0.75,0,0,0,0,3.422,0.295
FABL,25.06,0.208,0.072,0.032,0.036,-0.206,1.316,0,2023-03-31,0.493,0,0,0,0,3.427,0.271
FCCL,12.35,0.048,0.04,0.093,-0.087,-0.226,1.362,0,2023-03-31,0.203,0,0,0,0,2.749,
GGL,11.33,0.154,0.025,0.029,-0.302,-0.37,1.662,0,2023-03-31,0.207,0,0,0,0,8.853,
HCAR,127.24,0.394,0.123,-0.07,-0.243,-0.344,2.515,5,2023-03-31,-5.181,0,0,0,0,11.79,0.034
HUBC,80.74,0.256,0.226,0.495,0.674,0.0,1.636,0,2023-03-31,0.218,0,1,0,0,3.106,0.095
ILP,37.38,0.124,0.232,0.109,-0.022,-0.124,1.474,0,2023-03-31,3.196,0,0,0,0,4.434,0.066
INIL,90.52,0.311,0.219,0.367,-0.117,-0.212,2.108,0,2023-03-31,1.241,0,0,0,0,5.642,0.077
ISL,47.37,0.205,0.109,0.144,-0.161,-0.234,1.255,0,2023-03-31,0.338,0,0,0,0,4.771,0.11
KEL,2.03,0.285,0.025,-0.117,-0.334,-0.456,2.244,0,2023-03-31,,0,1,0,0,9.912,
KOHC,176.45,0.076,0.222,0.316,0.354,-0.065,1.257,0,2023-03-31,-0.012,0,0,0,0,5.202,
LOTCHEM,27.94,0.046,0.136,0.014,0.12,-0.205,0.636,0,2023-03-31,-0.029,0,0,0,0,3.876,0.232
LUCK,583.02,0.14,0.45,0.362,0.337,-0.0,1.348,0,2023-03-31,1.84,0,0,0,0,5.032,
MARI,1546.3,0.033,0.029,0.029,-0.111,-0.102,1.12,0,2022-12-31,0.492,0,1,0,0,7.019,0.071
MEBL,118.34,0.426,0.232,0.348,0.161,0.0,1.676,0,2023-03-31,0.682,0,1,0,0,3.964,0.082
MLCF,31.22,0.135,0.177,0.49,0.172,-0.028,0.968,0,,,0,0,0,0,6.598,
MTL,396.44,0.051,0.141,0.27,-0.231,-0.263,2.041,0,2023-03-31,-0.092,0,0,0,0,15.755,0.074
MUGHAL,57.57,0.199,0.132,0.273,-0.018,-0.195,2.242,0,2023-03-31,0.556,0,0,0,0,3.575,0.052
NETSOL,89.63,0.18,0.196,0.05,-0.064,-0.259,1.81,0,2023-03-31,8.261,0,0,0,0,10.272,
NML,61.69,0.079,0.144,0.224,-0.134,-0.233,1.058,0,2023-03-31,-0.115,0,0,0,0,2.112,0.054
NRL,218.43,0.448,0.455,0.301,-0.02,-0.201,2.552,1,2023-03-31,-1.481,0,1,0,0,2.225,0.059
OGDC,85.21,0.156,0.015,0.089,0.17,-0.157,1.205,0,2023-03-31,0.497,0,0,0,0,2.529,0.092
PABC,46.8,-0.025,0.017,0.185,0.47,-0.128,0.663,0,,,0,0,0,0,,
PAEL,11.11,0.213,0.028,-0.062,-0.293,-0.363,2.468,1,2023-03-31,-0.951,0,0,0,0,10.818,
PIBTL,4.32,0.11,0.094,0.016,-0.242,-0.316,1.95,0,2023-03-31,,0,0,0,0,,
PIOC,90.66,0.08,0.28,0.819,0.534,-0.026,0.536,0,2023-03-31,0.953,0,0,0,0,13.048,
PNSC,132.44,0.052,0.301,0.159,1.606,-0.048,0.825,0,,,0,0,0,0,,
PPL,69.91,0.242,0.04,-0.082,0.009,-0.166,1.21,0,2023-03-31,0.609,0,0,0,0,3.38,0.03
PRL,16.5,0.184,0.337,0.222,-0.005,-0.171,2.123,0,2023-03-31,-0.68,0,1,0,0,0.896,
PSO,119.68,0.136,0.04,-0.159,-0.327,-0.379,2.172,0,2023-03-31,-0.653,0,0,0,0,0.884,0.058
SAZEW,66.55,0.425,0.479,0.365,0.038,-0.03,2.125,2,2023-03-31,16.951,0,0,0,0,31.865,
SEARL,46.44,0.224,-0.109,-0.157,-0.439,-0.482,1.736,1,2023-03-31,-0.664,0,1,0,0,14.467,
SNGP,44.89,0.06,0.088,0.115,0.327,-0.053,1.328,0,2023-03-31,-0.104,2,0,0,0,2.093,0.117
SSGC,9.63,0.094,-0.048,-0.095,-0.058,-0.209,0.896,0,2021-06-30,,1,0,0,0,,
SYS,439.72,0.102,-0.079,-0.1,0.306,-0.136,0.925,0,2023-03-31,2.069,0,0,0,0,20.325,0.011
TELE,8.11,0.225,0.018,0.24,-0.246,-0.344,1.759,0,2021-06-30,,0,0,0,0,8.192,
TGL,87.58,0.257,0.24,0.337,0.046,-0.173,1.483,2,2023-03-31,-0.258,0,0,0,0,3.453,0.019
TOMCL,22.11,0.027,-0.008,0.116,0.033,-0.166,1.246,0,2023-03-31,5.465,0,0,0,0,6.529,
TPLP,13.49,0.167,0.11,-0.064,-0.183,-0.285,1.633,0,,,1,0,0,0,,
TREET,22.02,0.387,0.254,0.288,-0.223,-0.203,2.602,3,2023-03-31,,0,0,0,0,,
UNITY,26.82,0.834,1.068,0.866,0.363,0.0,2.469,3,2023-03-31,-1.133,0,0,0,0,10.986,
WAFI,126.48,0.17,0.605,0.192,0.054,-0.081,2.862,2,,,0,0,0,0,,0.028
WAVES,7.64,0.207,0.02,-0.066,-0.399,-0.472,2.244,0,2023-03-31,-0.892,0,0,0,0,10.273,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2023-07-03,NRL,material_info,Material Information
2023-07-04,JOPP,material_info,Material Information
2023-07-04,LMSM,material_info,MATERIAL INFORMATION
2023-07-05,META,material_info,"Material information - Order Passed the Honorable Lahore High Court, Lahore"
2023-07-05,FPJM,material_info,Material Information
2023-07-05,AVN,material_info,Material Information
2023-07-05,AGHA,material_info,MATERIAL INFORMATION REVOKED
2023-07-06,LSEVL,material_info,Material Information-Acceptance of Shares of LSEVL as collateral for BMC
2023-07-06,AGHA,material_info,Material Information
2023-07-06,LSEPL,material_info,Material Information-Acceptance of Shares of LSEPL as collateral for BMC
2023-07-07,FATIMA,material_info,Disclosure of Material Information
2023-07-07,SIEM,material_info,Material Information
2023-07-07,HIRAT,material_info,Material Information
2023-07-07,SPL,material_info,Material Information
2023-07-10,SGF,material_info,Material Information
2023-07-10,SRVI,material_info,Material Information
2023-07-10,MEBL,material_info,Material Information - Meezan Bank Limited
2023-07-10,BIPL,material_info,BIPL | BankIslami Pakistan Limited - Material Information
2023-07-10,EFGH,material_info,Material Information
2023-07-10,JSGCL,material_info,JSGCL | JS Global Capital Limited - Material Information
2023-07-11,OTSU,material_info,Disclosure of Material Information
2023-07-11,ANL,material_info,Material Information
2023-07-11,BRR,material_info,Material Information
2023-07-12,SMBL,material_info,Disclosure of Material Information
2023-07-12,SEARL,material_info,Material Information
2023-07-14,FUDLM,material_info,Material Information
2023-07-17,AIRLINK,material_info,Material Information
2023-07-17,PRL,material_info,Material Information
2023-07-18,SMBL,material_info,Disclosure of Material Information
2023-07-18,ORM,material_info,Material Information
2023-07-18,AVN,material_info,Material Information
2023-07-19,OBOY,material_info,Material Information
2023-07-19,SMBL,material_info,Material Information for disclosure of EOGM
2023-07-20,ATLH,material_info,Material Information
2023-07-20,PICT,material_info,Disclosure of Material Information
2023-07-20,MARI,material_info,Material Information
2023-07-20,META,material_info,Material information - proposed resolutions from the shareholder of the Com
2023-07-20,INDU,material_info,Disclosure of Material Information
2023-07-21,JSBLTFC1,material_info,DISCLOSURE OF MATERIAL INFORMATION

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,1.612,2023-07-20
investor_type,last_5_sessions,broker proprietary trading,-0.135,2023-07-20
investor_type,last_5_sessions,companies,-0.294,2023-07-20
investor_type,last_5_sessions,foreign corporates,4.806,2023-07-20
investor_type,last_5_sessions,foreign individual,-0.005,2023-07-20
investor_type,last_5_sessions,individuals,0.977,2023-07-20
investor_type,last_5_sessions,insurance companies,1.295,2023-07-20
investor_type,last_5_sessions,mutual funds,-5.593,2023-07-20
investor_type,last_5_sessions,nbfc,-0.04,2023-07-20
investor_type,last_5_sessions,other organization,-2.676,2023-07-20
investor_type,last_5_sessions,overseas pakistani,0.052,2023-07-20
sector,last_5_sessions,fipi | Commercial Banks,1.965,2023-07-20
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,1.033,2023-07-20
sector,last_5_sessions,lipi companies | Cement,1.727,2023-07-20
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,-1.879,2023-07-20
sector,last_5_sessions,lipi individuals | Commercial Banks,-1.281,2023-07-20
sector,last_5_sessions,lipi individuals | Fertilizer,1.426,2023-07-20
sector,last_5_sessions,lipi insurance companies | Commercial Banks,1.03,2023-07-20
sector,last_5_sessions,lipi mutual funds | Cement,-1.345,2023-07-20
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-1.523,2023-07-20
sector,last_5_sessions,lipi mutual funds | Fertilizer,-1.746,2023-07-20
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,1.181,2023-07-20
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,-2.558,2023-07-20
investor_type,last_20_sessions,banks / dfi,-2.958,2023-07-20
investor_type,last_20_sessions,broker proprietary trading,-4.429,2023-07-20
investor_type,last_20_sessions,companies,7.847,2023-07-20
investor_type,last_20_sessions,foreign corporates,15.195,2023-07-20
investor_type,last_20_sessions,foreign individual,0.046,2023-07-20
investor_type,last_20_sessions,individuals,0.114,2023-07-20
investor_type,last_20_sessions,insurance companies,4.381,2023-07-20
investor_type,last_20_sessions,mutual funds,-12.779,2023-07-20
investor_type,last_20_sessions,nbfc,0.004,2023-07-20
investor_type,last_20_sessions,other organization,-6.696,2023-07-20
investor_type,last_20_sessions,overseas pakistani,-0.726,2023-07-20
sector,last_20_sessions,fipi | Commercial Banks,8.228,2023-07-20
sector,last_20_sessions,fipi | Technology and Communication,3.371,2023-07-20
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,3.807,2023-07-20
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-5.598,2023-07-20
sector,last_20_sessions,lipi companies | Cement,7.152,2023-07-20
sector,last_20_sessions,lipi companies | Commercial Banks,-3.462,2023-07-20
sector,last_20_sessions,lipi companies | Debt Market,5.311,2023-07-20
sector,last_20_sessions,lipi individuals | Cement,-3.586,2023-07-20
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-3.934,2023-07-20
sector,last_20_sessions,lipi mutual funds | Fertilizer,-5.812,2023-07-20
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-4.141,2023-07-20
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,-4.316,2023-07-20

=== FILE: calendar.md ===
# Calendar as of 2023-07-21

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2023-06-23 INIL: BOARD MEETING - OTHER THAN FINANCIAL RESULTS
- 2023-06-23 CHCC: Board Meeting Other Than Financial Results
- 2023-06-23 KEL: Board Meeting Other Than Financial Results
- 2023-06-26 ATBA: BOARD MEETING
- 2023-06-27 TREET: Board Meeting Other than the Financial Results
- 2023-07-05 ILP: Notice of Board Meeting Other Than Financial Results / Closed Period
- 2023-07-10 SEARL: Board Meeting Other Than Financial Results
- 2023-07-11 FABL: Board Meeting Other Than Financial Results
- 2023-07-13 ILP: Board Meeting other than Financial Results - Concluded
- 2023-07-14 HCAR: Board Meeting & Closed Period
- 2023-07-14 EFERT: Board Meeting for the announcement of the financial results for the half year ended June 30, 2023
- 2023-07-14 PRL: Board Meeting other than Financial Results
- 2023-07-14 NRL: Board Meeting Other Than Financial Results
- 2023-07-14 SSGC: Board Meeting Other Than Financial Results
- 2023-07-17 TGL: Board Meeting Other Than Financial Results
- 2023-07-18 NRL: Board Meeting other than Financial Results - Concluded
- 2023-07-18 BIPL: Board Meeting Other Than Financial Results

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
| 15 | Rs170bn mini-budget | 10 Feb 2023 | outcome not shown |
| 17 | GIDC recovery | SC Aug 2020 | outcome not shown |
| 19 | Exporter power tariff Rs19.99 | 6 Oct 2022 | outcome not shown |

=== FILE: situations.md ===
2020-01-13 (outcome_end) | 01_2019_bottom_imf_programme.md | Regime bottom: the IMF approval was not the low. The second signal (Sep 2019 rate hold, stable rupee) returned +35% to the January 2020 peak. Lesson: wait for it, not the headline.
2021-06-14 (outcome_end) | 02_2020_covid_crash_rate_cut_rebound.md | Shock with a policy backstop: the first rate cut came before the March 2020 low, the rebound was +79% from the low by June 2021. Lesson: enter a third, add on confirmation, favour USD earners.
2023-06-23 (outcome_end) | 03_2021_22_hike_cycle_and_default_scare.md | Tightening plus external stress: rate up 800bp in ten months with CPI above it. To June 2023 the median liquid stock fell 52% and 4 of 95 names rose. Lesson: hold bills, and set a trigger to return.
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
