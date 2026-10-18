# Replay bundle, close of 2025-12-12

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
# Market as of 2025-12-12 close (public information only)

- KSE100: 169,865 on 2025-12-12; 1m +5.7%, 3m +8.8%, 6m +41.0%, 12m +56.0%
- KMI All Share: 67,142 on 2025-12-12; 1m +6.0%, 3m +4.2%, 6m +30.0%, 12m +38.3%
- Policy rate 11.0%; last MPC decision 2025-10-27: hold (+0bp)
- 6M T-bill cutoff 11.00% (auction 2025-12-10); 3M 10.99%, 12M 11.27%
- CPI YoY 6.16% for 2025-11 (published by 2025-12-03); three months earlier (2025-08) 2.99%
- Brent: 62.11 USD/bbl on 2025-12-12; 3-month change -8.5%
- USD/PKR: 280.59  on 2025-12-12; 3-month change -0.4%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate -0.00pp (market near policy rate); CPI rising over 3 months (+3.2pp)
- Next MPC: see SBP calendar

Session date used: 2025-12-12. Liquid KMI names: 131 (membership KMI_ALL_derived_2025-12-02.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.057,0.0876,0.2341,0,0
E&P,3,0.1023,0.0965,0.3018,2,2
OMC,4,0.0738,0.0661,0.2394,0,1
Power,6,0.1974,0.2121,0.6106,0,0
Fertilizer,4,0.0594,0.1161,0.4685,0,1
Cement,16,0.0862,0.1979,0.5137,2,3
Steel & engineering,11,0.0266,0.0076,0.3446,0,0
Autos,12,0.0051,-0.019,0.1402,0,0
Tech & telecom,11,0.0693,0.185,0.2896,0,1
Islamic banks & fin.,8,-0.0009,0.1142,0.7624,0,0
Pharma,14,0.0241,-0.0152,0.1102,1,1
Textiles,23,0.0592,-0.0426,0.291,2,2
Food & staples,15,0.0625,0.0451,0.2424,1,1
Chemicals,19,0.1249,0.1011,0.546,1,1
"Glass, packaging, paper",14,0.0511,-0.0888,0.1194,1,2
Gas utilities & misc,12,0.0726,0.0607,0.3365,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ACPL,281.87,-0.028,0.026,0.024,0.255,-0.099,0.319,0,2025-06-30,-0.687,0,0,0,0,23.229,0.027
AIRLINK,173.19,-0.025,0.1,0.255,0.026,-0.18,0.678,0,2025-09-30,0.883,1,1,0,0,12.707,0.046
ATRL,660.17,-0.022,0.008,0.004,0.14,-0.098,0.641,0,2025-09-30,-0.353,0,0,0,0,8.095,0.015
BECO,6.85,-0.896,-0.711,-0.458,-0.192,-0.904,3.323,0,2025-09-30,-0.901,0,0,0,0,20.344,
BFAGRO,42.73,0.13,0.001,0.392,,-0.11,0.543,1,,,0,1,0,0,,
BFBIO,152.95,0.008,-0.089,-0.09,-0.207,-0.37,0.452,0,2025-09-30,-0.006,0,0,0,0,33.326,
BNL,13.3,-0.887,-0.914,-0.765,-0.193,-0.917,2.384,0,2025-06-30,,0,2,0,0,,
CHCC,359.8,0.063,0.036,0.325,0.203,-0.024,1.518,0,2025-09-30,-0.271,0,0,0,0,6.497,0.019
CNERGY,7.74,0.018,0.052,0.087,0.115,-0.147,0.427,0,2024-06-30,,0,0,0,0,,
CPHL,88.06,0.072,-0.07,0.106,0.53,-0.141,0.453,0,2025-03-31,0.032,0,0,0,0,21.506,0.042
DCL,13.38,0.08,-0.089,-0.135,0.326,-0.156,0.401,0,,,0,0,0,0,,
DGKC,242.04,0.061,0.008,0.56,1.283,-0.101,0.624,0,2025-09-30,1.672,0,0,0,0,7.851,0.012
EFERT,219.43,0.014,0.026,0.236,0.179,-0.042,0.792,0,2025-09-30,-0.321,0,0,0,0,9.648,0.105
ENGROH,216.41,-0.009,-0.08,0.257,0.082,-0.214,0.644,0,2025-09-30,0.043,0,0,0,0,9.7,0.04
FABL,89.68,0.054,0.178,0.571,1.095,-0.054,0.661,0,2025-09-30,-0.181,1,0,0,0,3.08,0.144
FATIMA,149.83,0.134,0.217,0.746,1.097,-0.03,0.82,0,2025-09-30,0.301,0,2,0,0,4.517,0.089
FCCL,57.47,0.05,0.012,0.302,0.505,-0.059,0.735,0,2025-06-30,2.312,0,1,0,0,8.222,0.028
FECTC,160.53,-0.097,0.702,0.774,0.669,-0.156,2.553,2,2025-09-30,-0.183,0,0,0,0,,
FFC,584.94,0.099,0.317,0.634,0.89,-0.014,1.391,0,2025-09-30,-0.027,0,0,0,0,5.523,0.112
FFL,19.75,0.072,0.002,0.28,0.442,-0.13,0.486,0,2025-09-30,-0.111,0,0,0,0,68.835,
GAL,551.06,-0.002,-0.035,0.374,0.984,-0.098,0.225,0,2025-09-30,1.78,0,0,0,0,5.252,0.026
GATI,121.17,0.126,-0.081,-0.143,-0.345,-0.348,0.4,1,,,0,0,0,0,,
GCIL,34.53,0.093,-0.007,0.754,1.82,-0.102,1.472,0,,,0,0,0,0,,
GCWL,20.16,0.141,0.052,1.28,,-0.098,0.657,0,,,0,0,0,0,,
GGL,26.25,0.101,-0.098,0.684,0.887,-0.103,0.575,0,2025-09-30,0.654,0,0,0,0,2.013,
GHNI,822.97,0.032,0.01,0.289,0.808,-0.069,0.404,0,2025-09-30,1.467,0,1,0,0,6.046,0.015
GLAXO,390.5,-0.009,-0.053,0.055,0.062,-0.154,0.325,0,2025-09-30,0.058,0,0,0,0,19.339,0.025
GWLC,63.1,0.069,0.172,0.256,0.543,-0.168,0.443,0,2025-09-30,-0.485,0,0,0,0,,
HCAR,281.02,-0.015,-0.043,0.025,-0.02,-0.158,0.394,0,2025-09-30,1.889,2,0,0,0,15.254,0.028
HUBC,224.57,0.065,0.214,0.792,1.089,-0.021,0.969,0,2025-09-30,-0.396,0,1,0,0,3.875,0.109
ISL,111.65,0.228,-0.124,0.348,0.377,-0.127,0.728,2,2025-09-30,2.488,0,0,0,0,25.861,0.027
KEL,5.62,0.12,0.005,0.077,-0.049,-0.27,0.565,0,2024-06-30,-0.871,0,4,0,0,30.127,
KML,15.66,-0.108,-0.826,-0.648,-0.566,-0.891,2.796,1,,,0,1,0,0,,
KOHC,104.76,0.06,0.028,0.372,0.231,-0.049,1.29,0,2025-09-30,-0.088,0,0,0,0,6.026,
KSBP,200.76,-0.04,-0.095,-0.058,0.275,-0.234,1.374,0,2025-09-30,2.115,1,0,0,0,,
LOADS,18.9,0.032,0.065,0.324,0.263,-0.089,0.443,0,2025-09-30,0.113,0,0,0,0,13.777,
LOTCHEM,29.78,0.073,0.185,0.491,0.451,0.0,1.006,0,2025-09-30,-0.818,0,0,0,0,11.982,0.239
LUCK,488.82,0.096,0.032,0.487,1.049,-0.017,0.819,0,2025-09-30,0.226,0,1,0,0,6.763,0.011
MARI,707.38,0.014,0.067,0.171,0.102,-0.188,0.542,0,2025-09-30,-0.178,0,1,0,0,11.514,0.035
MEBL,431.8,0.023,0.054,0.444,0.935,-0.094,1.198,0,2025-09-30,-0.129,0,0,0,0,4.229,0.116
MLCF,123.34,0.244,0.162,0.509,1.564,0.0,1.551,1,2024-12-31,0.708,0,1,0,0,7.675,
MUGHAL,88.39,0.065,0.035,0.221,0.102,-0.046,0.812,0,2025-09-30,134.0,0,0,0,0,28.337,
MWMP,80.35,-0.415,-0.314,3.386,4.184,-0.51,1.782,1,,,0,0,0,0,,
NETSOL,132.35,0.029,-0.126,0.016,-0.167,-0.213,0.333,0,2025-09-30,-0.453,0,1,0,0,8.173,
NML,186.26,0.302,0.201,0.522,0.693,0.0,1.721,1,2025-09-30,-0.398,0,0,0,0,8.671,0.016
NRL,422.73,0.203,0.172,0.755,0.585,-0.044,1.578,0,2025-09-30,,0,0,0,0,,
OGDC,275.11,0.131,0.044,0.346,0.519,0.0,0.714,0,2025-09-30,-0.066,0,0,0,0,5.583,0.068
PAEL,54.67,0.04,-0.019,0.35,0.7,-0.088,0.482,0,2025-09-30,0.542,0,0,0,0,16.997,
PIBTL,15.63,0.07,0.166,0.899,0.949,-0.05,0.689,0,2025-09-30,,0,0,0,0,,
PIOC,412.14,0.688,0.62,1.031,0.991,0.0,4.047,0,2025-09-30,0.247,0,1,0,0,10.627,0.044
PPL,220.27,0.166,0.175,0.381,0.32,0.0,1.115,0,2025-09-30,-0.118,0,1,0,0,5.148,0.044
PREMA,40.44,0.038,-0.049,-0.04,0.49,-0.534,0.497,0,2025-09-30,0.818,0,1,0,0,16.658,
PRL,36.71,0.032,0.126,0.182,0.126,-0.172,0.86,0,2025-09-30,,0,0,0,0,,
PSO,469.36,0.087,0.129,0.309,0.604,-0.019,0.683,0,2025-09-30,2.695,0,0,0,0,10.778,0.026
QUICE,14.27,0.482,0.566,0.908,1.03,0.0,0.966,4,,,0,0,0,0,,
SAZEW,1668.97,-0.041,0.003,0.512,0.587,-0.15,0.33,0,2025-09-30,0.047,0,0,0,0,4.217,0.046
SEARL,106.44,0.027,0.038,0.419,-0.02,-0.085,0.657,0,2025-09-30,1.232,0,0,0,0,,
SGPL,36.58,1.803,2.545,4.052,3.304,0.0,3.218,8,2025-09-30,,0,0,0,0,,
SLGL,21.22,0.117,0.047,0.259,0.329,-0.156,0.506,0,2025-03-31,0.146,0,0,0,0,7.077,
SNGP,120.09,0.06,-0.069,0.071,0.493,-0.122,0.78,0,2025-09-30,0.048,2,0,0,0,5.073,0.026
SSGC,41.39,0.298,-0.053,-0.051,0.251,-0.152,0.942,0,2025-06-30,-9.518,0,1,0,0,10.954,0.012
SYS,164.85,0.113,0.203,0.612,0.389,-0.001,0.631,0,2025-09-30,0.267,1,1,0,0,24.356,0.01
TATM,194.1,0.203,0.097,1.312,2.478,-0.34,1.56,3,2025-09-30,,0,1,0,0,6.525,
TELE,11.63,0.07,0.343,0.518,0.235,-0.123,0.832,0,2025-09-30,0.667,0,0,0,0,18.478,
TOMCL,53.77,0.004,0.038,0.95,0.671,-0.188,1.2,0,2025-09-30,0.227,0,3,0,0,13.655,
TPLP,12.5,0.211,0.137,0.29,0.076,-0.201,1.405,1,,,4,0,0,0,,
TREET,31.75,-0.013,0.169,0.567,0.724,-0.069,0.497,0,2025-09-30,1.111,0,1,0,0,17.461,
TRSM,40.21,-0.296,-0.157,5.047,9.471,-0.412,1.45,3,2025-09-30,-0.619,0,0,0,0,,
WAFI,212.91,0.135,0.12,0.235,0.029,-0.118,0.62,0,2025-09-30,,3,0,0,0,13.796,0.024
WAVES,13.51,-0.012,0.126,0.75,0.548,-0.134,0.466,0,2025-09-30,-0.189,0,0,0,0,2.445,
ZAL,48.89,0.063,0.744,2.243,,-0.05,0.826,0,2025-09-30,2.926,0,0,0,0,6.31,0.062

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2025-12-03,HALEON,material_info,Disclosure of Material Information
2025-12-03,KEL,material_info,Disclosure of Material Information.
2025-12-03,PREMA,material_info,Material Information
2025-12-04,PSEL,material_info,Material Information
2025-12-04,MEHT,material_info,Material Information
2025-12-04,BBFL,material_info,Material Information
2025-12-04,BAFL,material_info,Disclosure of Material Information
2025-12-04,PSEL,material_info,Material Information
2025-12-04,THCCL,material_info,Material Information-False Circulation of Information on Social Media
2025-12-04,JSCL,material_info,Material Information - Intimation about disposal of Suit No. 1696/2025 (old
2025-12-04,FATIMA,material_info,Disclosure of Material Information
2025-12-05,SBL,material_info,Disclosure of Material Information
2025-12-05,GEMBLUEX,material_info,Material Information
2025-12-05,SRVI,material_info,Material Information
2025-12-05,JSBL,material_info,Material Information
2025-12-05,SGF,material_info,Material Information
2025-12-05,JSGCL,material_info,Material Information
2025-12-08,ZUMA,material_info,MATERIAL INFORMATION
2025-12-08,PTC,material_info,Material Information
2025-12-08,OBOY,material_info,Material Information - Newspaper Advertisement for Ballot Paper
2025-12-08,ZUMA,material_info,MATERIAL INFORMATION
2025-12-08,CWSM,material_info,CWSM | Chakwal Spinning Mills Limited Material Information
2025-12-08,LIVEN,material_info,Disclosure of Material Information - Commissioning of Automatic Blistering 
2025-12-09,KEL,material_info,Disclosure of Material Information
2025-12-09,PRET,material_info,Disclosure of Material Information
2025-12-09,PABC,material_info,Material Information
2025-12-09,KEL,material_info,Disclosure of Material Information.
2025-12-09,KEL,material_info,Disclosure of Material Information
2025-12-09,DINT,material_info,Material Information - Solar Energy
2025-12-10,KAPCO,material_info,Disclosure of Material Information
2025-12-10,KML,material_info,Material Information
2025-12-11,SYS,material_info,Material Information
2025-12-11,PABC,material_info,Material Information -Conclusion of Sunset Review and Continuation of Anti-
2025-12-11,ASHT,material_info,Material information
2025-12-11,BAPL,material_info,Material Information
2025-12-12,TATM,material_info,Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-1347.408,2025-12-11
investor_type,last_5_sessions,broker proprietary trading,-0.6,2025-12-11
investor_type,last_5_sessions,companies,1451.163,2025-12-11
investor_type,last_5_sessions,foreign corporates,-4.278,2025-12-11
investor_type,last_5_sessions,foreign individual,-0.059,2025-12-11
investor_type,last_5_sessions,individuals,-9.402,2025-12-11
investor_type,last_5_sessions,insurance companies,-33.352,2025-12-11
investor_type,last_5_sessions,mutual funds,-40.615,2025-12-11
investor_type,last_5_sessions,nbfc,-0.156,2025-12-11
investor_type,last_5_sessions,other organization,-0.089,2025-12-11
investor_type,last_5_sessions,overseas pakistani,-15.204,2025-12-11
sector,last_5_sessions,fipi | Commercial Banks,-6.274,2025-12-11
sector,last_5_sessions,fipi | Power Generation and Distribution,-12.0,2025-12-11
sector,last_5_sessions,lipi banks / dfi | Debt Market,-1353.02,2025-12-11
sector,last_5_sessions,lipi companies | Cement,-5.009,2025-12-11
sector,last_5_sessions,lipi companies | Debt Market,1428.51,2025-12-11
sector,last_5_sessions,lipi companies | Power Generation and Distribution,23.989,2025-12-11
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,-17.498,2025-12-11
sector,last_5_sessions,lipi insurance companies | Debt Market,-7.582,2025-12-11
sector,last_5_sessions,lipi insurance companies | Fertilizer,-17.951,2025-12-11
sector,last_5_sessions,lipi mutual funds | Debt Market,-62.35,2025-12-11
sector,last_5_sessions,lipi mutual funds | Fertilizer,8.41,2025-12-11
sector,last_5_sessions,lipi other organization | Fertilizer,5.315,2025-12-11
investor_type,last_20_sessions,banks / dfi,-1236.655,2025-12-11
investor_type,last_20_sessions,broker proprietary trading,8.199,2025-12-11
investor_type,last_20_sessions,companies,1450.64,2025-12-11
investor_type,last_20_sessions,foreign corporates,-28.718,2025-12-11
investor_type,last_20_sessions,foreign individual,-0.299,2025-12-11
investor_type,last_20_sessions,individuals,2.207,2025-12-11
investor_type,last_20_sessions,insurance companies,-53.491,2025-12-11
investor_type,last_20_sessions,mutual funds,-112.814,2025-12-11
investor_type,last_20_sessions,nbfc,1.366,2025-12-11
investor_type,last_20_sessions,other organization,-9.343,2025-12-11
investor_type,last_20_sessions,overseas pakistani,-21.094,2025-12-11
sector,last_20_sessions,fipi | Commercial Banks,-17.944,2025-12-11
sector,last_20_sessions,fipi | Power Generation and Distribution,-16.193,2025-12-11
sector,last_20_sessions,lipi banks / dfi | Debt Market,-1269.587,2025-12-11
sector,last_20_sessions,lipi companies | Debt Market,1428.51,2025-12-11
sector,last_20_sessions,lipi companies | Power Generation and Distribution,30.221,2025-12-11
sector,last_20_sessions,lipi individuals | Commercial Banks,18.072,2025-12-11
sector,last_20_sessions,lipi insurance companies | Fertilizer,-21.971,2025-12-11
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,-16.906,2025-12-11
sector,last_20_sessions,lipi mutual funds | Cement,13.623,2025-12-11
sector,last_20_sessions,lipi mutual funds | Debt Market,-153.49,2025-12-11
sector,last_20_sessions,lipi mutual funds | Fertilizer,16.221,2025-12-11
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,13.391,2025-12-11

=== FILE: calendar.md ===
# Calendar as of 2025-12-12

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2025-11-13 KEL: Board Meeting Other Than Financial Results
- 2025-11-14 GCIL: MEETING OF THE BOARD OF DIRECTORS OTHER THAN FINANCIAL RESULTS - GHANI CHEMICAL INDUSTRIES LIMITED
- 2025-11-21 SNGP: Board Meeting
- 2025-11-21 SSGC: Board Meeting
- 2025-11-28 SYS: Board Meeting Other Than Financial Results
- 2025-12-01 SSGC: Disclosure for Board Meeting held on 29 November 2025
- 2025-12-01 FABL: Board Meeting other than Financial Results of Faysal Bank Limited
- 2025-12-08 FFL: Board Meeting Other Than Financial Results

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
| 3 | OMC margin +Rs1.22 | OCAC ask Apr 2025 | outcome not shown |
| 7 | IPP terminations | 2024 (unverified) | 5 PPAs ended Oct 2024; Rs1tn savings claimed 29 Dec. Y |
| 8 | PIA sale | Auction 31 Oct 2024 failed | outcome not shown |
| 9 | DISCO sales | Oct 2024: two by Jan 2025 | outcome not shown |
| 10 | K-Electric to Shanghai Electric | PAI 27 Mar 2018 | outcome not shown |
| 11 | OGDC 7%, PPL 10% sale | CCoP 21 Aug 2020 | outcome not shown |
| 12 | Six SOEs sold in FY20 | 29 Jan 2020 | outcome not shown |
| 14 | Cement FED | Jun 2024 | Effective Jul 2024; no reversal. Y |
| 15 | Rs170bn mini-budget | 10 Feb 2023 | outcome not shown |
| 16 | Captive gas levy | Ordinance Jan 2025 | outcome not shown |
| 17 | GIDC recovery | SC Aug 2020 | outcome not shown |
| 18 | End subsidised RLNG to fertilizer | 2023 | outcome not shown |
| 19 | Exporter power tariff Rs19.99 | 6 Oct 2022 | outcome not shown |
| 20 | Panda bond | "this year" 2024 | outcome not shown |
| 23 | IMF EFF Board | Staff deal 12 Jul 2024 | 25 Sep 2024. Y |

=== FILE: situations.md ===
2020-01-13 (outcome_end) | 01_2019_bottom_imf_programme.md | Regime bottom: the IMF approval was not the low. The second signal (Sep 2019 rate hold, stable rupee) returned +35% to the January 2020 peak. Lesson: wait for it, not the headline.
2021-06-14 (outcome_end) | 02_2020_covid_crash_rate_cut_rebound.md | Shock with a policy backstop: the first rate cut came before the March 2020 low, the rebound was +79% from the low by June 2021. Lesson: enter a third, add on confirmation, favour USD earners.
2023-06-23 (outcome_end) | 03_2021_22_hike_cycle_and_default_scare.md | Tightening plus external stress: rate up 800bp in ten months with CPI above it. To June 2023 the median liquid stock fell 52% and 4 of 95 names rose. Lesson: hold bills, and set a trigger to return.
2024-12-16 (outcome_end) | 04_2023_imf_standby_and_the_rally.md | Regime bottom on an IMF trigger: the staff-level deal came before any rate cut. KSE rose 190% from the June 2023 low to December 2024. Lesson: enter in stages on the trigger, not on a cut.
2024-12-16 (outcome_end) | 05_2024_first_cut_and_the_sector_leaders.md | First-cut policy decision in an easing cycle: KSE +59% by December 2024; fertilizer, E&P and pharma led while banks lagged. Lesson: favour sectors with their own catalyst over rate-sensitive ones.
2025-07-01 (outcome_end) | 06_2025_may_india_conflict_crash_and_rebound.md | Geopolitical shock, intact IMF and rates: KSE fell 12.6%, rebounded 13% in two sessions and was 8% above its pre-shock level by July. Lesson: hold the core; keep cash ready for a weekend gap.
2024-12-30 (outcome_end) | 09_2024_ssgc_volume_run.md | Volume ignition with upper locks on a regulated utility with late accounts: SSGC rose from 9.95 to 49.52 by the December 2024 peak with no filing explaining it. Lesson: instinct paid, but the repo cannot yet say when.
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
