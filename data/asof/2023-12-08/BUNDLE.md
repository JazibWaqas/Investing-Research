# Replay bundle, close of 2023-12-08

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
# Market as of 2023-12-08 close (public information only)

- KSE100: 66,224 on 2023-12-08; 1m +22.0%, 3m +43.9%, 6m +58.0%, 12m +57.1%
- KMI All Share: 32,123 on 2023-12-08; 1m +21.2%, 3m +44.6%, 6m +57.3%, 12m +55.4%
- Policy rate 22.0%; last MPC decision 2023-10-30: hold (+0bp)
- 6M T-bill cutoff 21.43% (auction 2023-11-29); 3M 21.45%, 12M 21.43%
- CPI YoY 29.24% for 2023-11 (published by 2023-12-03); three months earlier (2023-08) 27.39%
- Brent: 75.94 USD/bbl on 2023-12-08; 3-month change -17.3%
- USD/PKR: 283.88  on 2023-12-08; 3-month change -6.4%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate -0.57pp (market pricing cuts); CPI rising over 3 months (+1.8pp)
- Next MPC: see SBP calendar

Session date used: 2023-12-08. Liquid KMI names: 85 (membership KMI_ALL_derived_2023-07-10.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.3141,0.8154,0.9652,2,4
E&P,3,0.3042,0.4097,0.6168,3,3
OMC,4,0.2825,0.4722,0.6923,1,3
Power,5,0.1958,0.726,0.7721,2,3
Fertilizer,4,0.1308,0.2924,0.2464,3,3
Cement,16,0.2253,0.5512,0.5114,5,11
Steel & engineering,11,0.1659,0.4653,0.3989,3,4
Autos,12,0.2384,0.6546,1.0213,1,3
Tech & telecom,9,0.2606,0.4291,0.4597,3,5
Islamic banks & fin.,8,0.1115,0.2813,0.3428,5,5
Pharma,13,0.1926,0.4418,0.3819,1,3
Textiles,23,0.1028,0.2618,0.302,2,5
Food & staples,14,0.2756,0.4193,0.5215,3,3
Chemicals,18,0.1588,0.3864,0.3368,3,6
"Glass, packaging, paper",12,0.2289,0.4299,0.3609,2,4
Gas utilities & misc,10,0.2701,0.4496,0.2812,2,4

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AGHA,15.87,0.054,0.708,0.522,0.231,-0.018,2.539,1,,,0,1,0,0,,
AIRLINK,71.13,0.627,2.106,2.288,1.591,0.0,2.5,1,2023-09-30,1.168,0,0,0,0,8.16,0.121
ASC,12.35,0.532,0.202,0.6,0.096,0.0,2.203,1,2023-09-30,-8.532,5,0,0,0,,
ATBA,263.76,0.102,0.088,0.194,0.689,-0.104,1.319,1,,,0,0,0,0,,
ATRL,360.0,0.242,0.517,1.048,1.172,-0.008,1.146,1,2023-09-30,0.636,1,0,0,0,0.597,0.073
AVN,64.71,0.24,0.342,0.342,-0.032,-0.029,2.065,0,2023-09-30,-0.376,0,1,0,0,,
BERG,90.05,0.285,0.698,0.857,0.438,-0.027,2.623,1,2023-09-30,,0,0,0,0,5.17,
BIPL,22.9,0.012,0.618,0.479,0.747,0.0,0.806,0,2023-09-30,1.359,0,0,0,0,,
CEPB,38.18,0.245,0.598,0.236,0.145,-0.02,2.783,1,2023-09-30,0.271,0,0,0,0,,
CHCC,164.34,0.077,0.306,0.332,0.467,-0.004,1.652,0,2023-09-30,0.034,0,0,0,0,5.307,0.037
CPHL,27.11,0.119,0.356,0.171,0.059,-0.051,2.062,0,2023-09-30,-0.359,0,0,0,0,7.41,0.117
CSAP,47.93,0.276,0.997,0.809,0.287,-0.035,2.882,2,2023-09-30,,0,1,0,0,2.826,
DCL,7.93,0.353,1.002,0.754,0.455,-0.0,2.592,1,,,0,0,0,0,,
DGKC,80.54,0.294,0.888,0.525,0.609,0.0,2.054,1,2023-09-30,0.656,0,0,0,0,,
DOL,25.71,0.15,0.031,0.008,0.265,-0.09,2.206,0,,,0,0,0,0,,
EFERT,108.78,0.191,0.412,0.259,0.338,0.0,2.067,0,2023-09-30,1.291,0,0,0,0,6.416,0.176
EPCL,49.44,0.208,0.3,0.26,0.17,0.0,2.392,1,2023-09-30,0.161,0,1,0,0,3.422,0.295
FABL,33.11,0.32,0.505,0.539,0.206,0.0,1.578,0,2023-09-30,0.342,1,0,0,0,3.427,0.271
FCCL,20.25,0.312,0.872,0.629,0.539,-0.013,2.36,1,2023-06-30,-0.681,0,1,0,0,3.877,
FCEPL,92.94,0.46,0.634,0.404,0.357,0.0,3.67,1,2023-09-30,-0.694,0,0,0,0,20.427,
FEROZ,229.35,0.167,0.686,0.584,0.308,-0.024,1.698,0,,,0,0,0,0,,
GAL,76.58,0.652,1.038,1.371,0.505,-0.057,2.474,0,2023-09-30,,0,0,0,0,11.951,
GGL,13.61,0.278,0.465,0.316,-0.065,-0.085,2.131,0,2023-09-30,0.483,0,0,0,0,9.587,
GHGL,33.73,0.319,0.309,0.139,0.039,-0.036,3.985,0,2023-09-30,0.094,0,0,0,0,,
GHNI,186.01,0.32,0.922,1.334,0.445,-0.03,1.744,0,2023-09-30,-0.229,0,0,0,0,19.126,
HCAR,229.78,0.285,1.098,1.411,0.518,-0.01,1.998,1,2023-09-30,,1,0,0,0,64.681,
HTL,30.73,0.248,0.329,0.312,-0.011,-0.001,2.398,0,,,0,0,0,0,,
HUBC,123.38,0.154,0.7,1.009,1.312,-0.002,1.347,0,2023-09-30,0.879,0,0,0,0,1.568,0.431
IBLHL,41.38,0.17,0.235,0.292,-0.044,-0.031,2.928,1,,,0,0,0,0,,
ILP,75.25,0.344,0.806,1.404,1.114,0.0,1.412,0,2023-09-30,0.218,0,1,0,0,2.45,0.113
IMAGE,18.97,0.15,0.556,0.981,0.826,-0.012,2.441,0,2023-09-30,0.944,0,0,0,0,,
INIL,137.26,0.213,0.545,0.716,0.577,0.0,1.96,0,2023-09-30,-0.433,0,0,0,0,3.136,0.102
ISL,74.99,0.223,0.704,0.696,0.639,0.0,1.611,0,2023-09-30,1.495,0,0,0,0,5.01,0.136
KEL,4.43,0.406,1.307,1.421,0.684,0.0,2.156,0,2023-06-30,0.033,0,0,0,0,,
LPL,23.36,0.386,0.576,2.341,2.239,0.0,1.027,0,,,0,0,0,0,,
LUCK,794.1,0.105,0.46,0.542,0.734,-0.03,1.693,0,2023-09-30,2.43,0,0,0,0,3.356,0.034
MARI,2067.41,0.253,0.284,0.326,0.242,0.0,1.725,0,2023-09-30,0.505,0,1,0,0,3.6,0.097
MEBL,175.04,0.201,0.514,1.117,0.83,0.0,1.427,0,2023-09-30,1.234,0,0,0,0,3.964,0.082
MFFL,200.77,0.6,1.697,1.571,1.092,-0.239,2.729,4,,,1,1,0,0,,
MLCF,42.71,0.166,0.488,0.488,0.744,0.0,1.907,0,,,0,0,0,0,5.269,
MTL,619.83,0.311,0.398,0.848,0.69,-0.055,1.67,2,2023-09-30,3.476,0,1,0,0,22.731,0.054
MUGHAL,73.27,0.208,0.489,0.482,0.333,-0.01,1.816,0,2023-09-30,-0.412,0,0,0,0,4.671,0.066
NETSOL,119.13,0.382,0.436,0.584,0.123,-0.005,2.233,0,2023-09-30,0.432,0,0,0,0,6.329,
NML,82.34,0.177,0.385,0.337,0.414,-0.009,1.769,0,2023-09-30,-0.138,0,0,0,0,1.767,0.088
NRL,368.56,0.437,0.894,1.262,0.802,-0.003,1.461,2,2023-09-30,,0,0,0,0,,
OGDC,125.38,0.245,0.365,0.669,0.896,0.0,1.424,0,2023-09-30,-0.08,0,0,0,0,1.494,0.11
PABC,77.49,0.262,0.514,0.572,0.769,-0.021,1.812,1,,,0,0,0,0,,
PAEL,21.33,0.601,1.238,1.19,0.389,0.0,2.692,0,2023-09-30,0.044,0,0,0,0,10.818,
PIBTL,6.11,0.18,0.66,0.434,0.222,0.0,2.034,0,2023-09-30,,2,0,0,0,,
PICT,57.9,0.204,-0.219,-0.519,-0.585,-0.587,1.814,0,2023-09-30,-0.699,0,0,0,0,6.38,0.132
PIOC,118.47,0.105,0.443,0.364,0.971,0.0,1.754,0,2023-09-30,0.593,0,0,0,0,7.536,
PPL,113.85,0.412,0.581,0.858,1.038,0.0,1.628,0,2023-09-30,0.13,0,0,0,0,1.655,0.042
PRL,31.8,0.402,1.177,1.112,0.975,0.0,1.649,2,2023-09-30,3.362,0,2,0,0,4.681,
PSO,217.22,0.549,0.852,0.928,0.449,0.0,1.887,0,2023-09-30,12.737,0,0,0,0,5.593,0.068
PTL,50.25,0.307,1.232,1.662,1.352,0.0,1.725,1,2023-09-30,,0,0,0,0,7.826,0.099
RPL,16.24,0.094,0.509,0.667,0.159,0.0,1.33,1,,,0,0,0,0,,
SAZEW,220.89,0.266,1.837,3.426,2.667,-0.008,1.868,2,2023-09-30,59.5,0,0,0,0,3.089,0.079
SEARL,62.57,0.338,0.812,0.452,-0.088,-0.059,2.609,0,2023-09-30,-0.542,0,0,0,0,47.647,
SGF,53.87,0.266,0.738,0.749,0.482,0.0,1.394,1,2023-09-30,2.204,0,0,0,0,,
SNGP,69.44,0.311,0.622,0.629,0.835,-0.009,1.742,0,2023-09-30,0.438,8,0,0,0,2.364,0.114
SSGC,13.76,0.354,0.532,0.452,0.362,-0.001,3.232,0,2021-06-30,,2,1,0,0,,
SYS,462.92,0.099,0.066,0.144,-0.058,-0.09,1.449,0,2023-09-30,-0.175,0,0,0,0,20.325,0.011
TELE,9.16,0.276,0.309,0.318,0.002,-0.002,1.915,0,2023-09-30,0.875,0,3,0,0,7.795,
TGL,108.88,0.23,0.336,0.5,0.315,-0.005,1.877,0,2023-09-30,1.151,0,0,0,0,4.654,0.088
TOMCL,24.3,0.115,0.155,0.132,0.059,-0.051,1.752,0,2023-09-30,-0.529,0,0,0,0,3.884,
TOWL,203.57,0.227,0.293,0.199,0.432,-0.353,1.237,0,2023-09-30,-0.329,1,0,0,0,1.141,0.081
TPLP,14.79,0.178,0.163,0.449,-0.068,-0.119,1.461,1,,,0,0,0,0,,
TREET,18.69,0.172,0.327,0.277,-0.013,-0.034,1.651,0,2023-09-30,,0,0,0,0,,
UNITY,27.47,0.126,0.185,1.036,0.627,-0.028,1.708,0,2023-09-30,,0,0,0,0,27.645,
WAFI,175.93,0.182,0.257,1.146,0.396,-0.005,1.054,0,,,0,0,0,0,,0.028

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2023-11-16,PHDL,material_info,Material Information
2023-11-16,SYM,material_info,Material Information - Change of Registered Address
2023-11-16,PRL,material_info,Material Information
2023-11-16,MTL,material_info,Material Information
2023-11-17,AHCL,material_info,Material Information Disclosure
2023-11-17,AHL,material_info,Material Information Disclosure - Arif Habib Limited
2023-11-20,KOSM,material_info,Material Information
2023-11-21,PRL,material_info,Material Information
2023-11-21,FFL,material_info,Material Information
2023-11-21,WTL,material_info,Material Information
2023-11-22,EFGH,material_info,Material Information
2023-11-22,EFGH,material_info,Material Information
2023-11-23,AGHA,material_info,Material Information
2023-11-23,SZTM,material_info,Disclosure of Material Information
2023-11-24,TELE,material_info,Material Information
2023-11-24,HCL,material_info,Material Information
2023-11-24,SAIF,material_info,Material Information
2023-11-27,LSEPL,material_info,Material Information
2023-11-29,AVN,material_info,Material Information
2023-11-29,OCTOPUS,material_info,Material Information
2023-11-29,LSEPL,material_info,Material Information
2023-11-29,TPL,material_info,Disclosure of Material Information
2023-11-29,MODAM,material_info,Material Information-Swap Ratio
2023-11-29,CSAP,material_info,Material Information
2023-11-30,FCCL,material_info,Disclosure of Material Information
2023-12-01,ILP,material_info,"Material Information, Acquisition of Top Circle Hosiery Mills Co., Inc., US"
2023-12-01,TELE,material_info,Material Information - Acquisition of 62.84% shares of Hallmark Company Lim
2023-12-01,HCL,material_info,Material Information - Material Change in Ownership of the Company
2023-12-04,MFL,material_info,Material Information
2023-12-04,BOK,material_info,Bank of Khyber-Material Information
2023-12-05,FUDLM,material_info,Material Information
2023-12-05,GCIL,material_info,DISCLOSURE OF MATERIAL INFORMATION - GHANI CHEMICAL INDUSTRIES LIMITED
2023-12-06,CPPL,material_info,Material Information
2023-12-06,SSGC,material_info,Material Information
2023-12-07,EPCL,material_info,Material Information
2023-12-08,HBL,material_info,Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-11.209,2023-12-07
investor_type,last_5_sessions,broker proprietary trading,-2.089,2023-12-07
investor_type,last_5_sessions,companies,1.124,2023-12-07
investor_type,last_5_sessions,foreign corporates,11.278,2023-12-07
investor_type,last_5_sessions,foreign individual,-0.021,2023-12-07
investor_type,last_5_sessions,individuals,-5.923,2023-12-07
investor_type,last_5_sessions,insurance companies,-2.538,2023-12-07
investor_type,last_5_sessions,mutual funds,6.772,2023-12-07
investor_type,last_5_sessions,nbfc,0.039,2023-12-07
investor_type,last_5_sessions,other organization,2.318,2023-12-07
investor_type,last_5_sessions,overseas pakistani,0.249,2023-12-07
sector,last_5_sessions,fipi | All other Sectors,3.156,2023-12-07
sector,last_5_sessions,fipi | Cement,1.502,2023-12-07
sector,last_5_sessions,fipi | Commercial Banks,3.628,2023-12-07
sector,last_5_sessions,fipi | Fertilizer,2.103,2023-12-07
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-2.558,2023-12-07
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,-3.353,2023-12-07
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,-2.505,2023-12-07
sector,last_5_sessions,lipi companies | All other Sectors,1.678,2023-12-07
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,4.45,2023-12-07
sector,last_5_sessions,lipi individuals | All other Sectors,-1.844,2023-12-07
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,-3.42,2023-12-07
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,2.885,2023-12-07
investor_type,last_20_sessions,banks / dfi,-42.063,2023-12-07
investor_type,last_20_sessions,broker proprietary trading,-7.793,2023-12-07
investor_type,last_20_sessions,companies,5.305,2023-12-07
investor_type,last_20_sessions,foreign corporates,49.403,2023-12-07
investor_type,last_20_sessions,foreign individual,-0.263,2023-12-07
investor_type,last_20_sessions,individuals,-3.478,2023-12-07
investor_type,last_20_sessions,insurance companies,-5.195,2023-12-07
investor_type,last_20_sessions,mutual funds,5.253,2023-12-07
investor_type,last_20_sessions,nbfc,-0.086,2023-12-07
investor_type,last_20_sessions,other organization,-1.997,2023-12-07
investor_type,last_20_sessions,overseas pakistani,0.914,2023-12-07
sector,last_20_sessions,fipi | All other Sectors,7.041,2023-12-07
sector,last_20_sessions,fipi | Cement,9.896,2023-12-07
sector,last_20_sessions,fipi | Commercial Banks,13.282,2023-12-07
sector,last_20_sessions,fipi | Fertilizer,7.833,2023-12-07
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,6.652,2023-12-07
sector,last_20_sessions,fipi | Power Generation and Distribution,9.244,2023-12-07
sector,last_20_sessions,lipi banks / dfi | All other Sectors,-8.429,2023-12-07
sector,last_20_sessions,lipi banks / dfi | Cement,-6.489,2023-12-07
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-11.354,2023-12-07
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-5.699,2023-12-07
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,4.813,2023-12-07
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,4.703,2023-12-07

=== FILE: calendar.md ===
# Calendar as of 2023-12-08

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2023-11-10 SNGP: ADJOURNMENT OF BOARD OF DIRECTORS MEETING
- 2023-11-10 MFFL: Board Meeting to consider the Quarterly accounts for the period year ended June 30, 2023 REVOKED
- 2023-11-13 SSGC: Board Meeting
- 2023-11-13 NRL: Board Meeting other than Financial Results - Concluded
- 2023-11-13 EPCL: Board Meeting other than Financial Results
- 2023-11-13 HCAR: Board Meeting
- 2023-11-15 EFERT: Board Meeting other than financial Results
- 2023-11-17 PIBTL: PIBT BOARD MEETING WILL BE HELD ON NOVEMBER 24, 2023
- 2023-11-21 SYS: Board Meeting Other Than Financial Results
- 2023-11-21 EPCL: Board Meeting other than financial Results
- 2023-11-22 ASC: Board Meeting
- 2023-11-23 MFFL: Board Meeting of the First Quarter
- 2023-11-27 FABL: Board Meeting other than Financial Results of Faysal Bank Limited
- 2023-11-27 AVN: Board Meeting Other Than Financial Results
- 2023-11-30 BIPL: Board Meeting Other Than Financial Results
- 2023-11-30 PNSC: Board Meeting Other Than Financial Results REVOKED
- 2023-12-01 AGP: Board Meeting other than financial Results - December 8, 2023

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
| 1 | Brownfield refinery policy | 17 Aug 2023 | outcome not shown |
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
