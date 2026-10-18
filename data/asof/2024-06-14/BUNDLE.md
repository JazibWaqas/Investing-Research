# Replay bundle, close of 2024-06-14

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
# Market as of 2024-06-14 close (public information only)

- KSE100: 76,707 on 2024-06-14; 1m +2.7%, 3m +16.7%, 6m +15.8%, 12m +83.0%
- KMI All Share: 34,609 on 2024-06-14; 1m -0.2%, 3m +9.6%, 6m +7.7%, 12m +69.4%
- Policy rate 20.5%; last MPC decision 2024-06-10: cut (-150bp)
- 6M T-bill cutoff 19.97% (auction 2024-06-12); 3M 20.15%, 12M 18.95%
- CPI YoY 11.74% for 2024-05 (published by 2024-06-03); three months earlier (2024-02) 23.07%
- Brent: 81.49 USD/bbl on 2024-06-14; 3-month change -5.4%
- USD/PKR: 278.54  on 2024-06-14; 3-month change -0.1%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate -0.53pp (market pricing cuts); CPI falling over 3 months (-11.3pp)
- Next MPC: see SBP calendar

Session date used: 2024-06-14. Liquid KMI names: 87 (membership KMI_ALL_derived_2023-12-26.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.0919,-0.1323,-0.1789,0,0
E&P,3,-0.0405,0.0681,0.1603,0,0
OMC,4,0.0215,0.1908,0.0048,0,0
Power,5,0.0108,0.071,0.0168,1,1
Fertilizer,4,0.0179,0.2457,0.3998,0,0
Cement,16,0.0001,0.2172,0.1377,0,2
Steel & engineering,11,0.037,0.16,0.0905,0,2
Autos,12,-0.0078,0.2984,0.3406,2,3
Tech & telecom,10,0.0633,0.1205,0.4942,1,3
Islamic banks & fin.,8,0.0104,0.0975,0.0947,1,3
Pharma,13,0.0165,0.1898,0.131,2,4
Textiles,23,-0.0285,0.0096,-0.0327,0,0
Food & staples,14,-0.0301,0.0017,-0.1264,0,0
Chemicals,18,-0.0175,0.0371,-0.0935,2,3
"Glass, packaging, paper",13,-0.0271,0.0353,-0.0755,0,0
Gas utilities & misc,11,-0.0635,-0.0698,-0.1584,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AIRLINK,80.37,0.078,0.222,0.13,2.716,-0.007,0.825,0,2024-03-31,5.238,0,1,0,0,8.16,0.121
ATRL,361.47,-0.071,-0.026,0.004,1.056,-0.137,0.494,0,2024-03-31,-0.4,0,0,0,0,0.597,0.073
AVN,56.35,-0.012,0.134,-0.042,0.286,-0.071,1.337,0,2024-03-31,-1.064,1,0,0,0,,
BCL,140.07,-0.11,0.943,1.504,3.214,-0.183,1.166,0,,,0,0,0,0,,
BGL,14.52,-0.112,0.62,0.282,0.37,-0.112,1.411,2,,,0,1,0,0,,
BIPL,21.4,-0.044,-0.059,-0.066,0.382,-0.186,0.576,0,2024-03-31,0.784,0,0,0,0,,
CEPB,31.07,-0.054,0.083,-0.186,0.006,-0.203,0.69,0,2024-03-31,-0.426,0,0,0,0,,
CHCC,164.14,-0.023,0.058,-0.001,0.33,-0.03,0.916,0,2024-03-31,-0.023,0,0,0,0,5.307,0.037
CLOV,45.8,-0.045,0.567,0.604,2.207,-0.125,0.626,0,2023-12-31,,0,0,0,0,,
CNERGY,4.1,-0.085,-0.198,-0.199,0.231,-0.305,0.401,0,2024-03-31,,0,1,0,0,,
CPHL,28.66,-0.08,0.158,0.057,0.238,-0.13,0.974,0,2023-12-31,0.271,0,0,0,0,7.41,0.117
DCL,9.04,0.05,0.25,0.14,1.0,-0.183,2.989,0,,,0,0,0,0,,
DGKC,92.73,0.04,0.306,0.151,0.756,-0.027,1.429,0,2024-03-31,0.054,0,0,0,0,,
EFERT,165.47,0.073,0.121,0.521,0.915,-0.054,0.619,0,2024-03-31,0.761,0,0,0,0,5.722,0.183
EPCL,43.62,0.02,0.012,-0.098,0.137,-0.13,0.414,0,2024-03-31,-1.977,0,1,0,0,5.11,0.129
FABL,44.41,0.134,0.435,0.341,1.065,0.0,1.571,0,2024-03-31,0.995,1,1,0,0,2.442,0.123
FATIMA,48.77,-0.02,0.29,0.462,0.772,-0.078,0.355,0,2024-03-31,1.083,0,0,0,0,3.239,0.127
FCCL,23.91,0.058,0.325,0.181,0.924,-0.01,1.769,0,2023-06-30,-0.681,0,0,0,0,3.877,
FCEPL,72.83,0.004,-0.007,-0.216,0.1,-0.275,1.474,0,2024-03-31,-0.326,0,0,0,0,41.597,
FFL,9.21,-0.063,-0.036,-0.121,0.53,-0.197,0.368,0,2024-03-31,,0,0,0,0,46.392,
GAL,175.76,-0.021,1.077,1.295,4.442,-0.111,1.322,0,2024-03-31,-0.484,0,0,0,0,11.951,
GGL,10.02,-0.081,-0.038,-0.264,-0.031,-0.281,0.991,0,2024-03-31,0.2,0,0,0,0,9.587,
GHNI,277.54,-0.072,0.612,0.492,2.483,-0.107,0.834,1,2024-03-31,1.615,0,0,0,0,19.126,
GLAXO,140.24,0.064,0.615,0.469,0.763,-0.006,0.816,1,2024-03-31,0.318,0,0,0,0,49.498,
GTYR,43.82,-0.082,0.202,0.054,0.964,-0.082,0.937,0,2024-03-31,,0,0,0,0,,
GWLC,33.47,-0.002,0.334,0.26,1.128,-0.04,2.638,2,2024-03-31,0.015,0,0,0,0,,
HCAR,297.13,-0.044,0.194,0.293,2.118,-0.115,0.732,0,2024-03-31,,2,0,0,0,64.681,
HTL,34.12,0.003,0.37,0.11,0.456,-0.092,2.54,2,,,0,0,0,0,,
HUBC,145.46,0.064,0.258,0.244,1.498,0.0,0.948,0,2024-03-31,0.528,0,0,0,0,1.568,0.431
ILP,69.12,-0.165,-0.035,-0.082,1.208,-0.178,1.616,0,2024-03-31,-0.569,0,0,0,0,2.45,0.113
INIL,192.07,0.172,0.428,0.399,1.401,-0.023,2.472,0,2024-03-31,-0.772,0,0,0,0,3.136,0.102
ISL,86.88,0.139,0.249,0.159,0.964,-0.012,1.906,0,2024-03-31,-0.534,0,0,0,0,5.01,0.136
KEL,4.62,0.002,-0.019,0.043,1.525,-0.245,0.854,0,2023-06-30,0.033,1,1,0,0,,
KOHC,235.38,0.068,0.07,0.036,0.399,-0.055,1.014,1,2024-03-31,0.296,0,0,0,0,5.986,
LOTCHEM,17.9,-0.021,-0.072,-0.361,-0.4,-0.395,0.991,0,2024-03-31,-0.649,0,0,0,0,8.049,0.111
LPL,24.99,0.075,0.238,0.07,2.574,-0.128,2.44,0,,,0,0,0,0,,
LUCK,946.44,0.06,0.24,0.192,0.838,-0.011,1.193,0,2024-03-31,-0.199,0,0,0,0,3.356,0.034
MARI,2719.58,-0.038,0.111,0.316,0.744,-0.042,1.036,0,2024-03-31,-0.14,0,0,0,0,3.6,0.097
MEBL,242.49,0.092,0.394,0.489,2.152,-0.014,1.063,0,2024-03-31,0.614,0,0,0,0,3.383,0.124
MLCF,38.31,-0.037,0.009,-0.103,0.335,-0.103,1.133,0,,,0,1,0,0,5.269,
MTL,658.41,0.082,0.092,0.062,0.963,-0.005,1.131,0,2024-03-31,0.693,0,0,0,0,22.731,0.054
MUGHAL,96.91,0.291,0.436,0.323,0.96,-0.013,3.027,0,2024-03-31,-0.92,0,0,0,0,4.671,0.066
NETSOL,142.53,0.27,0.051,0.196,0.895,-0.013,2.087,1,2024-03-31,-0.99,1,1,0,0,6.329,
NML,72.46,0.027,0.048,-0.12,0.176,-0.134,1.893,0,2024-03-31,-0.673,0,0,0,0,1.767,0.088
NRL,272.02,-0.095,-0.124,-0.262,0.67,-0.264,0.546,0,2024-03-31,,0,1,0,0,,
OGDC,131.21,-0.058,0.042,0.083,0.807,-0.127,0.592,1,2024-03-31,-0.26,0,1,0,0,1.494,0.11
PABC,73.0,0.063,0.013,-0.058,0.481,-0.077,0.905,0,,,0,1,0,0,,
PAEL,24.89,-0.077,0.04,0.167,1.555,-0.141,0.798,1,2024-03-31,16.0,0,0,0,0,15.073,
PIBTL,6.24,-0.08,0.036,0.021,0.465,-0.214,0.34,0,2024-03-31,,0,0,0,0,,
PIOC,163.39,0.006,0.218,0.379,0.881,-0.029,1.117,1,2024-03-31,0.266,0,0,0,0,7.536,
PPL,119.76,-0.027,0.045,0.052,0.954,-0.105,0.552,0,2024-03-31,-0.152,0,0,0,0,1.655,0.042
PREMA,15.09,0.029,0.125,-0.133,-0.089,-0.213,2.368,1,2024-03-31,-0.832,0,0,0,0,2.884,
PRL,23.86,-0.119,-0.188,-0.25,0.584,-0.32,0.53,0,2024-03-31,-1.701,0,1,0,0,4.681,
PSO,171.67,-0.049,-0.006,-0.21,0.524,-0.21,0.47,0,2024-03-31,-0.657,0,0,0,0,5.593,0.068
SAZEW,802.06,0.093,0.853,2.631,15.07,-0.059,0.799,1,2024-03-31,5.821,1,1,0,0,3.089,0.079
SEARL,59.86,0.008,0.09,-0.043,0.389,-0.054,1.012,0,2024-03-31,-3.239,0,0,0,0,47.647,
SNGP,65.52,-0.081,-0.001,-0.056,0.537,-0.171,0.594,0,2024-03-31,0.619,0,0,0,0,2.364,0.114
SSGC,10.07,-0.034,-0.089,-0.268,0.062,-0.274,0.247,0,2021-06-30,,3,0,0,0,,
SYS,437.81,0.123,0.088,-0.04,0.099,-0.058,1.771,0,2024-03-31,-0.596,0,0,0,0,14.2,0.014
TELE,7.9,-0.086,-0.13,-0.138,0.137,-0.241,0.38,0,2024-03-31,-1.225,1,1,0,0,7.795,
TGL,113.64,0.003,0.108,0.044,0.566,-0.088,1.066,1,2024-03-31,-0.158,0,1,0,0,4.654,0.088
THCCL,36.2,-0.004,0.868,0.977,2.175,-0.087,0.947,1,2024-03-31,4.667,0,1,0,0,11.468,
TOMCL,34.03,0.044,0.403,0.4,0.586,-0.14,1.229,1,2024-03-31,-0.716,0,0,0,0,3.884,
TPLP,9.82,-0.147,-0.136,-0.336,-0.038,-0.357,0.696,0,,,0,0,0,0,,
TREET,15.67,-0.072,-0.103,-0.162,0.07,-0.274,0.416,0,2024-03-31,0.486,0,1,0,0,,
UNITY,26.92,0.044,0.139,-0.02,0.996,-0.047,0.705,0,2024-03-31,,0,2,0,0,27.645,
WAFI,138.55,-0.05,-0.139,-0.212,0.69,-0.217,0.657,0,,,0,0,0,0,5.504,0.033

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2024-05-24,TPLT,material_info,Material Information
2024-05-24,AGTL,material_info,Material Information: GO-LIVE SAP S/4 HANA
2024-05-24,FECM,material_info,Material Information
2024-05-24,CNERGY,material_info,Material Information
2024-05-27,NRL,material_info,Material Information
2024-05-27,FTSM,material_info,Material Information
2024-05-29,DFML,material_info,Material Information
2024-05-29,EPCL,material_info,Disclosure of Material Information
2024-05-29,LSECL,material_info,Material Information-Merger Effect Statement
2024-05-29,FUDLM,material_info,Material Information - UDL International Ltd
2024-05-30,TGL,material_info,Material Information
2024-05-30,LCI,material_info,Material Information
2024-05-30,SHEL,material_info,Material Information
2024-05-30,PCAL,material_info,Material Information
2024-05-30,DFML,material_info,Material Information
2024-05-31,FABL,material_info,Material Information - Faysal Bank limited
2024-06-03,MFL,material_info,Material Information
2024-06-03,OGDC,material_info,Material Information
2024-06-03,SLCL,material_info,Material Information
2024-06-04,BGL,material_info,MATERIAL INFORMATION REGARDING COMMENCEMENT OF COMMERCIAL OPERATIONS
2024-06-05,AIRLINK,material_info,Material Information
2024-06-06,TREET,material_info,Material Information
2024-06-06,GEMBLUEX,material_info,Material Information
2024-06-06,TELE,material_info,Material information - Equity Investment in Hallmark Company Limited
2024-06-07,LSECL,material_info,Material Information-Initial offer to the accredited investor-Mughal Energy
2024-06-07,SAZEW,material_info,Material Information
2024-06-07,LSECL,material_info,Material Information-Initial offer to the accredited investors-Mughal Energ
2024-06-10,SAPT,material_info,Material Information
2024-06-10,SFL,material_info,Material Information
2024-06-10,RCML,material_info,Material Information
2024-06-11,HPL,material_info,Material Information
2024-06-12,MWMP,material_info,Material Information
2024-06-12,BNL,material_info,Material Information
2024-06-12,MLCF,material_info,Material Information
2024-06-13,UNITY,material_info,Material Information
2024-06-13,TPL,material_info,Material Information
2024-06-13,DSML,material_info,Material Information Regarding Merger
2024-06-13,KTML,material_info,KTML-Material Information
2024-06-14,FAYSAL-FUNDS,material_info,Material Information
2024-06-14,LSECL,material_info,Material Information-Appointment of Directors

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-1.465,2024-06-13
investor_type,last_5_sessions,broker proprietary trading,1.591,2024-06-13
investor_type,last_5_sessions,companies,7.399,2024-06-13
investor_type,last_5_sessions,foreign corporates,-5.829,2024-06-13
investor_type,last_5_sessions,foreign individual,0.017,2024-06-13
investor_type,last_5_sessions,individuals,-11.322,2024-06-13
investor_type,last_5_sessions,insurance companies,1.722,2024-06-13
investor_type,last_5_sessions,mutual funds,10.888,2024-06-13
investor_type,last_5_sessions,nbfc,-0.166,2024-06-13
investor_type,last_5_sessions,other organization,-1.122,2024-06-13
investor_type,last_5_sessions,overseas pakistani,-1.714,2024-06-13
sector,last_5_sessions,fipi | All other Sectors,-2.46,2024-06-13
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-2.664,2024-06-13
sector,last_5_sessions,lipi banks / dfi | All other Sectors,2.033,2024-06-13
sector,last_5_sessions,lipi companies | Cement,2.675,2024-06-13
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,2.518,2024-06-13
sector,last_5_sessions,lipi individuals | All other Sectors,-2.918,2024-06-13
sector,last_5_sessions,lipi individuals | Cement,-3.018,2024-06-13
sector,last_5_sessions,lipi individuals | Commercial Banks,-2.261,2024-06-13
sector,last_5_sessions,lipi individuals | Fertilizer,-2.038,2024-06-13
sector,last_5_sessions,lipi insurance companies | Fertilizer,2.084,2024-06-13
sector,last_5_sessions,lipi mutual funds | Cement,2.512,2024-06-13
sector,last_5_sessions,lipi mutual funds | Commercial Banks,1.82,2024-06-13
investor_type,last_20_sessions,banks / dfi,5.57,2024-06-13
investor_type,last_20_sessions,broker proprietary trading,-7.63,2024-06-13
investor_type,last_20_sessions,companies,-2.007,2024-06-13
investor_type,last_20_sessions,foreign corporates,0.251,2024-06-13
investor_type,last_20_sessions,foreign individual,-0.094,2024-06-13
investor_type,last_20_sessions,individuals,-21.964,2024-06-13
investor_type,last_20_sessions,insurance companies,26.06,2024-06-13
investor_type,last_20_sessions,mutual funds,3.763,2024-06-13
investor_type,last_20_sessions,nbfc,-0.225,2024-06-13
investor_type,last_20_sessions,other organization,-1.606,2024-06-13
investor_type,last_20_sessions,overseas pakistani,-4.692,2024-06-13
sector,last_20_sessions,fipi | Commercial Banks,12.587,2024-06-13
sector,last_20_sessions,fipi | Debt Market,-16.551,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-14.504,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Debt Market,16.586,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,10.815,2024-06-13
sector,last_20_sessions,lipi companies | Commercial Banks,5.197,2024-06-13
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,-5.673,2024-06-13
sector,last_20_sessions,lipi individuals | Cement,-5.581,2024-06-13
sector,last_20_sessions,lipi individuals | Commercial Banks,-7.475,2024-06-13
sector,last_20_sessions,lipi insurance companies | Commercial Banks,8.95,2024-06-13
sector,last_20_sessions,lipi insurance companies | Fertilizer,6.146,2024-06-13
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,4.973,2024-06-13

=== FILE: calendar.md ===
# Calendar as of 2024-06-14

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2024-05-17 HCAR: Board of Directors Meeting & Close Period
- 2024-05-22 KEL: Board Meeting Other Than Financial Results
- 2024-05-23 GTYR: Board Meeting Other than Financial Results
- 2024-05-24 KEL: Board Meeting Other Than Financial Results
- 2024-05-27 PRL: Board Meeting other than Financial Results
- 2024-05-31 PRL: Board Meeting Rescheduled
- 2024-05-31 KEL: Board Meeting Other Than Financial Results
- 2024-06-03 TOMCL: Board Meeting Other Than Financial Results
- 2024-06-06 FCCL: Board Meeting Other Than Financial Results
- 2024-06-07 BGL: Board Meeting Other Than Financial Results
- 2024-06-12 NRL: Board Meeting Other Than Financial Results
- 2024-06-13 ATRL: BOARD MEETING OTHER THAN FINANCIAL RESULTS
- 2024-06-14 ACPL: Board Meeting other than Financial Results.
- 2024-06-14 INIL: Board Meeting Other Than Financial Results
- 2024-06-14 CHCC: Board Meeting Other Than Financial Results
- 2024-06-14 TPLP: Board Meeting Other Than Financial Results

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
| 18 | End subsidised RLNG to fertilizer | 2023 | outcome not shown |
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
