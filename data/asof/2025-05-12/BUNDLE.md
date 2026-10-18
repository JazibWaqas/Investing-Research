# Replay bundle, close of 2025-05-12

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
# Market as of 2025-05-12 close (public information only)

- KSE100: 117,298 on 2025-05-12; 1m +1.0%, 3m +4.8%, 6m +27.5%, 12m +66.0%
- KMI All Share: 49,823 on 2025-05-12; 1m -1.7%, 3m +4.6%, 6m +23.2%, 12m +50.8%
- Policy rate 11.0%; last MPC decision 2025-05-05: cut (-100bp)
- 6M T-bill cutoff 12.00% (auction 2025-04-30); 3M 12.01%, 12M 12.01%
- CPI YoY 0.26% for 2025-04 (published by 2025-05-03); three months earlier (2025-01) 2.42%
- Brent: 65.28 USD/bbl on 2025-05-12; 3-month change -13.4%
- USD/PKR: 281.58  on 2025-05-12; 3-month change +0.9%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +1.00pp (market pricing hikes); CPI falling over 3 months (-2.2pp)
- Next MPC: see SBP calendar

Session date used: 2025-05-12. Liquid KMI names: 100 (membership KMI_ALL_derived_2025-01-03.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.2026,-0.1503,0.113,0,0
E&P,3,-0.0847,0.0217,0.2657,0,0
OMC,4,-0.0957,-0.0888,0.159,0,0
Power,5,-0.0171,-0.0197,0.0644,0,0
Fertilizer,4,-0.009,-0.0525,0.2428,0,1
Cement,16,0.0247,0.1271,0.2775,3,3
Steel & engineering,11,0.0402,0.012,0.1559,0,0
Autos,12,-0.0525,-0.0831,0.1429,0,0
Tech & telecom,11,-0.024,-0.132,0.0457,0,0
Islamic banks & fin.,8,0.0246,0.0687,0.156,1,2
Pharma,14,-0.1052,-0.1216,0.4268,1,1
Textiles,23,-0.0171,-0.092,0.0093,1,1
Food & staples,15,-0.0307,-0.0239,0.1831,0,1
Chemicals,18,0.0054,0.0414,0.2347,0,1
"Glass, packaging, paper",14,0.0164,0.0542,0.1546,1,1
Gas utilities & misc,12,-0.0274,0.0191,0.2909,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ABOT,925.84,-0.119,-0.258,0.029,0.67,-0.281,0.599,1,2025-03-31,0.054,2,0,0,0,,
ACPL,273.13,0.03,0.231,0.734,1.985,-0.088,0.818,0,2024-12-31,,2,0,0,0,3.743,0.067
AGP,175.29,-0.09,0.061,0.257,1.251,-0.175,1.327,1,2025-03-31,1.126,2,0,0,0,17.84,0.024
AGTL,410.22,-0.178,-0.334,-0.038,0.121,-0.408,0.738,0,2025-03-31,-1.119,2,0,0,0,9.191,
AIRLINK,150.25,-0.132,-0.207,0.194,1.221,-0.316,0.515,1,2025-03-31,-0.485,2,0,0,0,7.591,0.068
ATBA,255.13,-0.191,-0.311,-0.288,-0.013,-0.491,1.194,1,,,2,0,0,0,,
ATLH,1192.89,0.3,0.353,0.344,1.487,0.0,1.58,0,,,1,0,0,0,,
ATRL,526.52,-0.135,-0.097,0.167,0.383,-0.283,0.428,1,2025-03-31,-1.176,2,0,0,0,1.496,0.043
AVN,45.38,-0.09,-0.198,-0.121,-0.22,-0.33,0.561,1,2025-03-31,,4,0,0,0,,
BBFL,48.8,0.002,0.05,-0.301,,-0.416,1.535,1,,,2,0,0,0,,
BFAGRO,29.06,0.173,,,,,1.048,1,,,2,1,0,0,,
BFBIO,142.22,-0.072,-0.32,0.522,,,0.561,3,2025-03-31,-0.374,2,0,0,0,,
BIPL,20.06,-0.037,-0.11,-0.032,-0.025,-0.181,1.319,0,2025-03-31,-0.183,2,1,0,0,,
BNL,25.52,0.208,0.841,0.883,0.823,-0.253,2.91,1,,,2,0,0,0,,
BWCL,417.34,0.053,0.172,0.389,1.016,-0.035,0.832,0,,,2,0,0,0,,
CEPB,22.72,-0.069,-0.221,-0.127,-0.175,-0.363,0.784,0,2025-03-31,-1.423,2,0,0,0,,
CHCC,279.07,0.071,0.088,-0.047,0.763,-0.09,0.78,1,2025-03-31,0.355,2,0,0,0,5.763,0.034
CLOV,37.93,-0.14,-0.012,0.135,0.202,-0.203,0.845,0,2024-12-31,,2,2,0,0,,
CNERGY,7.42,-0.129,-0.009,0.805,0.762,-0.141,0.618,1,2024-06-30,,2,0,0,0,114.054,
CPHL,71.13,-0.27,-0.259,0.58,1.777,-0.332,0.52,1,2025-03-31,0.032,2,1,0,0,7.812,0.114
CSAP,116.41,0.211,0.126,0.069,1.02,-0.122,0.911,1,2025-03-31,0.298,2,0,0,0,3.297,0.102
DCL,9.94,0.146,0.153,0.183,0.386,-0.101,2.445,1,,,2,0,0,0,,
DCR,26.26,0.023,0.193,0.4,0.922,0.0,0.905,0,2025-03-31,0.16,2,0,0,0,4.494,0.122
DGKC,140.39,0.072,0.33,0.603,0.813,0.0,0.816,1,2025-03-31,0.64,2,0,0,0,63.696,
DOL,25.9,0.024,0.147,0.365,0.405,-0.011,0.601,0,,,2,0,0,0,,
EFERT,178.9,-0.055,-0.137,-0.036,0.212,-0.215,1.216,1,2025-03-31,-0.626,2,0,0,0,9.648,0.105
ENGROH,166.55,-0.027,-0.203,0.125,0.149,-0.395,1.473,1,2025-03-31,-0.626,2,0,0,0,9.7,0.04
EPCL,30.75,-0.159,-0.095,-0.187,-0.269,-0.36,0.726,0,2025-03-31,,1,1,0,0,,
FABL,47.97,0.041,0.035,0.088,0.362,-0.091,0.911,0,2025-03-31,-0.182,2,1,0,0,3.08,0.144
FATIMA,85.58,-0.005,0.095,0.396,0.726,-0.005,0.734,1,2025-03-31,-0.002,2,0,0,0,4.517,0.089
FCCL,45.71,-0.033,0.214,0.343,1.267,-0.038,0.629,1,2025-03-31,0.208,2,0,0,0,6.834,0.044
FCEPL,86.8,0.059,0.167,-0.055,0.21,-0.133,1.496,1,2024-09-30,2.03,2,0,0,0,31.055,0.031
FCL,22.0,-0.061,-0.109,0.011,,-0.223,0.399,0,2025-03-31,-0.37,2,1,0,0,7.966,0.052
FEROZ,288.26,-0.067,-0.135,-0.043,0.32,-0.252,0.33,1,,,2,0,0,0,,
FFL,14.34,-0.07,-0.043,0.36,0.572,-0.258,0.52,1,2025-03-31,2.25,2,0,0,0,68.835,
FLYNG,37.15,0.321,0.478,0.292,3.57,0.0,0.401,3,,,2,0,0,0,,
GAL,453.63,-0.073,0.056,0.815,2.778,-0.102,0.642,1,2025-03-31,6.437,2,0,0,0,27.284,
GATM,22.31,-0.09,-0.097,0.156,0.108,-0.186,0.335,1,2025-03-31,0.1,2,0,0,0,3.218,
GGGL,8.41,-0.023,0.098,0.318,0.435,-0.183,0.397,1,,,2,0,0,0,,
GGL,12.07,-0.085,-0.125,0.145,0.228,-0.278,0.247,1,2025-03-31,1.024,2,0,0,0,6.416,
GHGL,31.3,-0.059,0.098,0.276,0.26,-0.144,0.511,1,2025-03-31,-0.035,2,0,0,0,,
GHNI,703.03,0.018,0.207,0.755,1.837,-0.08,0.827,1,2025-03-31,3.032,2,0,0,0,14.907,
GLAXO,359.81,-0.116,-0.071,0.314,2.752,-0.23,1.495,1,2025-03-31,2.753,2,0,0,0,19.339,0.025
GTYR,36.97,-0.048,-0.193,0.004,-0.022,-0.33,0.382,1,2025-03-31,-0.2,2,0,0,0,,
GWLC,38.56,-0.016,-0.158,-0.063,0.682,-0.318,0.414,1,2025-03-31,-0.158,2,0,0,0,,
HALEON,747.53,-0.06,-0.068,0.133,2.166,-0.19,0.79,0,2025-03-31,1.074,2,1,0,0,20.65,0.025
HCAR,263.05,-0.098,-0.102,-0.084,-0.148,-0.233,0.777,1,2024-12-31,2.97,0,0,0,0,13.638,0.029
HINOON,905.36,0.008,0.068,0.136,0.655,-0.043,1.344,1,2025-03-31,0.217,2,0,0,0,,
HTL,37.16,-0.111,-0.201,-0.037,0.485,-0.386,0.184,1,,,2,0,0,0,,
HUBC,138.35,-0.004,0.13,0.324,0.165,-0.088,0.76,1,2025-03-31,-0.358,2,0,0,0,3.021,0.123
ILP,55.04,-0.115,-0.104,-0.144,-0.256,-0.345,0.523,1,2025-03-31,-0.627,2,0,0,0,6.013,0.064
IMAGE,21.62,-0.074,0.148,0.455,0.591,-0.146,0.808,1,2025-03-31,-0.497,2,0,0,0,,
INIL,144.58,-0.098,-0.113,-0.019,-0.031,-0.336,0.579,1,2025-03-31,0.925,2,1,0,0,11.902,0.028
ISL,74.81,-0.038,-0.07,-0.012,0.114,-0.294,0.306,1,2025-03-31,-0.407,3,1,0,0,10.063,0.065
KEL,4.56,0.004,0.029,-0.017,0.078,-0.288,0.684,0,2024-06-30,-0.871,0,0,0,0,30.127,
KOHC,385.35,-0.02,0.041,-0.136,0.765,-0.136,0.42,1,2025-03-31,0.138,2,0,0,0,5.515,
KSBP,171.1,0.014,0.175,0.315,0.46,-0.072,1.816,0,2025-03-31,,3,0,0,0,,
LCI,1460.02,0.075,0.288,0.261,0.892,-0.026,1.08,0,2025-03-31,-0.099,2,0,0,0,7.699,0.065
LOTCHEM,18.76,0.027,-0.094,0.089,0.084,-0.194,0.162,1,2025-03-31,-0.254,2,0,0,0,11.982,0.239
LPL,24.39,-0.095,-0.04,0.214,0.029,-0.207,1.168,2,,,2,0,0,0,,
LUCK,337.78,0.054,0.412,0.686,1.018,-0.059,3.567,1,2025-03-31,0.151,2,0,0,0,4.053,0.016
MARI,636.06,-0.1,0.11,0.543,1.124,-0.293,0.78,1,2025-03-31,0.137,2,0,0,0,4.682,0.086
MEBL,281.84,0.125,0.24,0.28,0.492,0.0,0.936,0,2025-03-31,-0.116,2,0,0,0,4.229,0.116
MFFL,179.73,-0.113,-0.422,0.141,0.182,-0.435,0.432,1,,,2,0,0,0,,
MLCF,69.65,0.119,0.574,0.635,0.908,-0.027,1.172,1,2024-12-31,0.708,2,1,0,0,5.919,
MTL,593.55,-0.02,-0.004,0.118,0.064,-0.129,0.752,0,2025-03-31,-0.513,2,0,0,0,11.845,0.039
MUGHAL,65.52,-0.093,-0.154,-0.128,0.018,-0.333,0.579,1,2025-03-31,1.194,2,0,0,0,16.363,
NETSOL,128.28,-0.069,-0.169,0.004,0.141,-0.243,0.477,1,2025-03-31,15.667,2,0,0,0,9.912,0.022
NML,115.41,0.047,0.255,0.61,0.696,-0.085,1.038,1,2025-03-31,-0.5,2,0,0,0,3.166,0.042
NRL,184.06,-0.263,-0.247,-0.207,-0.374,-0.44,0.405,1,2025-03-31,,2,0,0,0,,
OCTOPUS,43.73,-0.174,-0.298,-0.383,-0.274,-0.626,0.554,1,,,4,0,0,0,,
OGDC,203.01,-0.039,0.052,0.177,0.676,-0.121,0.714,1,2025-03-31,-0.014,2,0,0,0,2.786,0.075
PABC,111.44,-0.055,-0.009,0.321,0.747,-0.191,0.624,1,,,2,0,0,0,,
PAEL,44.24,-0.014,0.13,0.719,0.908,-0.083,0.646,1,2025-03-31,0.392,2,1,0,0,16.997,
PIBTL,8.62,-0.197,0.104,0.425,0.347,-0.22,0.873,1,2025-03-31,-2.368,2,0,0,0,6.244,
PIOC,212.19,-0.037,0.206,0.094,0.52,-0.066,0.68,1,2025-03-31,-0.189,2,0,0,0,7.401,0.089
POWER,14.98,0.222,0.559,1.081,2.008,0.0,1.522,0,2025-03-31,,2,0,0,0,,
PPL,152.75,-0.115,-0.097,0.066,0.334,-0.264,0.854,1,2025-03-31,-0.213,2,0,0,0,2.759,0.051
PREMA,44.01,0.053,0.828,1.667,2.294,-0.493,1.963,0,2025-03-31,0.5,2,2,0,0,8.672,
PRL,27.02,-0.254,-0.219,0.102,0.05,-0.39,0.54,1,2025-03-31,,2,0,0,0,3.599,0.086
PSO,362.8,-0.083,0.036,0.53,1.078,-0.185,0.919,1,2025-03-31,-0.287,2,0,0,0,4.258,0.06
SAZEW,1315.47,0.154,0.174,0.196,0.913,-0.031,1.702,0,2025-03-31,1.053,2,0,0,0,6.341,0.024
SEARL,75.06,-0.212,-0.27,0.074,0.442,-0.399,0.49,1,2025-03-31,,2,0,0,0,,
SHFA,438.64,-0.004,0.032,0.19,2.401,-0.141,0.245,1,,,3,1,0,0,,
SLGL,14.43,0.051,-0.051,-0.051,0.329,-0.257,1.613,1,2024-12-31,1.776,2,0,0,0,7.077,
SNGP,122.63,0.084,0.358,0.512,0.809,-0.03,1.368,1,2024-12-31,0.346,2,0,0,0,2.121,0.118
SPEL,38.18,-0.035,-0.064,-0.012,2.05,-0.286,0.739,1,2025-03-31,1.387,2,0,0,0,,
SSGC,30.46,-0.222,-0.187,0.786,1.89,-0.385,0.98,1,2024-06-30,-0.97,0,0,0,0,1.007,
SYM,13.95,-0.005,-0.224,0.459,2.822,-0.342,0.5,1,2025-03-31,0.154,2,0,0,0,,
SYS,538.43,0.084,-0.063,0.025,0.436,-0.137,1.357,1,2025-03-31,0.583,2,0,0,0,24.356,0.01
TELE,6.91,-0.044,-0.158,-0.042,-0.164,-0.343,0.565,0,2025-03-31,,2,0,0,0,210.275,
TGL,200.02,0.025,0.544,0.678,0.858,-0.054,0.597,1,2025-03-31,0.637,2,0,0,0,4.587,
THCCL,182.09,-0.134,-0.086,0.621,5.473,-0.201,0.496,1,2025-03-31,0.017,2,1,0,0,2.244,0.028
TOMCL,28.17,-0.163,-0.154,-0.22,-0.167,-0.391,1.738,1,2025-03-31,-0.253,2,0,0,0,10.506,
TPLP,8.0,-0.222,-0.309,0.026,-0.265,-0.488,0.608,1,,,2,2,0,0,,
TREET,18.25,-0.153,-0.115,0.171,0.155,-0.35,0.411,1,2025-03-31,-0.109,2,0,0,0,,
UNITY,25.78,-0.033,-0.158,-0.044,0.025,-0.339,0.524,1,2025-03-31,,2,0,0,0,,
WAFI,153.05,-0.173,-0.104,0.04,0.067,-0.376,0.388,1,2025-03-31,1.776,2,0,0,0,13.796,0.024
WAVES,7.79,0.012,-0.046,0.163,0.064,-0.159,0.522,0,2025-03-31,3.364,3,0,0,0,2.445,
ZAL,16.26,0.12,,,,,1.504,0,2025-03-31,0.645,2,1,0,0,,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2025-04-14,MACFL,material_info,Material Information
2025-04-14,PREMA,material_info,Material Information
2025-04-14,KOSM,material_info,Material Information---Credit of Shares By CDC
2025-04-15,FCL,material_info,Disclosure of Material Information - Fast Cables Limited
2025-04-16,SFL,material_info,Material Information
2025-04-16,FABL,material_info,Disclosure of Material Information - Termination of Acquisition Discussions
2025-04-16,TPLRF1,material_info,Material Information
2025-04-16,TPLP,material_info,Material Information
2025-04-16,CPHL,material_info,Material Information
2025-04-16,CWSM,material_info,Material Information
2025-04-17,HALEON,material_info,Material Information - Change of CEO
2025-04-17,PACE,material_info,Material Information
2025-04-21,DYNO,material_info,Material information
2025-04-21,PAEL,material_info,Material Information
2025-04-21,GATI,material_info,Material Information
2025-04-21,CLOV,material_info,Material Information
2025-04-21,PAKOXY,material_info,Material Information
2025-04-21,FNEL,material_info,Material Information
2025-04-21,ARPL,material_info,Disclosure Form & Material Information
2025-04-22,GCIL,material_info,DISCLOSURE OF MATERIAL INFORMATION - GHANI CHEMICAL INDUSTRIES LIMITED
2025-04-23,PGLC,material_info,Material Information
2025-04-23,CTM,material_info,Material Information
2025-04-23,EPCL,material_info,Material Information - Engro Polymer & Chemicals Limited
2025-04-23,BFAGRO,material_info,Material Information
2025-04-24,BIFO,material_info,Disclosure of Material Information
2025-04-25,APL,material_info,Material Information
2025-04-25,TPLRF1,material_info,Material Information
2025-04-25,TPLP,material_info,Material Information
2025-04-25,BCL,material_info,Material Information
2025-04-25,LSECL,material_info,MATERIAL INFORMATION
2025-04-28,SBL,material_info,Material Information - Resignation of President & CEO
2025-04-28,GEMSPNL,material_info,Material Information (Reko Diq Contract)
2025-04-28,FNEL,material_info,Material Information
2025-04-28,PAKL,material_info,MATERIAL INFORMATION
2025-04-29,SCBPL,material_info,Material Information
2025-04-30,CSIL,material_info,Material Information
2025-04-30,OGDC,financial_result,"Financial Results for the Quarter Ended March 31, 2025"
2025-04-30,TOMCL,financial_result,"Financial Results for the Quarter Ended MARCH 31, 2025"
2025-04-30,AGP,financial_result,"Financial Results for the Quarter Ended March 31, 2025"
2025-04-30,FLYNG,financial_result,Transmission of Quarterly Report for the Period Ended 2025-03-31
2025-04-30,SYM,financial_result,Financial Results for the Quarter Ended 31 March 2025
2025-04-30,THCCL,financial_result,"Transmission of Quarterly Report For The Period Ended March 31, 2025"
2025-04-30,AVN,financial_result,Transmission of Annual Report for the Year Ended 31 December 2024
2025-04-30,KSBP,financial_result,Transmission of Quarterly Report for the Period Ended 2025-03-31
2025-04-30,DCR,financial_result,"FINANCIAL RESULTS OF DOLMEN CITY REIT FOR THE QUARTER ENDED MARCH 31, 2025"
2025-04-30,ATRL,financial_result,TRANSMISSION OF FINANCIAL STATEMENTS FOR THE THIRD QUARTER AND NINE MONTHS 
2025-04-30,DGKC,financial_result,"TRANSMISSION OF QUARTERLY REPORT FOR THE 3RD QUARTER ENDED MARCH 31, 2025"
2025-04-30,PRL,financial_result,"Transmission of Quarterly Report for the Period ended March 31, 2025"
2025-04-30,LPL,financial_result,"TRANSMISSION OF QUARTERLY REPORT FOR THE 1ST QUARTER ENDED MARCH 31, 2025"
2025-04-30,ABOT,financial_result,"Transmission of Quarterly Report for the Period Ended March 31, 2025"
2025-04-30,AIRLINK,financial_result,"Transmission of Quarterly Report for the Period Ended March 31, 2025"
2025-04-30,HALEON,financial_result,Transmission of Quarterly Report for the Period Ended 31 March 2025
2025-04-30,FATIMA,financial_result,"Transmission of Quarterly Report for the Period Ended March 31, 2025"
2025-04-30,FFL,financial_result,"Transmission of Quarterly Accounts for the period ended March 31, 2025"
2025-04-30,FCCL,financial_result,Transmission of 3rd Quarterly Accounts for the Period Ended 31st March 2025
2025-04-30,ATLH,financial_result,Financial Results for the Year Ended 2025-03-31
2025-04-30,TGL,financial_result,"Transmission of Quarterly Report for the Period Ended March 31, 2025"
2025-04-30,SHFA,financial_result,"Transmission of Quarterly Report for the Period Ended March 31, 2025."
2025-04-30,HUBC,financial_result,"Transmission of Quarterly Report for the Period Ended March 31, 2025"
2025-04-30,IMAGE,financial_result,Transmission of Quarterly Report for the Period Ended 2025-03-31
2025-04-30,ILP,financial_result,"Transmission of 3rd Quarterly Report for the Period Ended March 31, 2025"
2025-04-30,PIOC,financial_result,Financial Results for the quarter ended 31 March 2025
2025-04-30,WAFI,financial_result,"FINANCIAL RESULTS FOR THE QUARTER ENDED March 31, 2025"
2025-04-30,GTYR,financial_result,"Transmission of Quarterly Report for the Period Ended March 31, 2025"
2025-04-30,PAEL,financial_result,Transmission of 1st Quarterly Report for the Period Ended 31-03-2025 (Un-Au
2025-04-30,UNITY,financial_result,Transmission of Quarterly Report for the Period Ended 2025-03-31
2025-04-30,HINOON,financial_result,Financial Results for the Quarter Ended 2025-03-31
2025-04-30,SYM,financial_result,Transmission of Quarterly Report for the Period Ended 31 March 2025
2025-04-30,KOHC,financial_result,Transmission of Quarterly Report for the Period Ended 31-03-2025
2025-04-30,GGGL,financial_result,"Transmission of 3rd Quarterly accounts for the period ended March 31, 2025 "
2025-04-30,SNGP,financial_result,"Transmission of Annual Report for the Year Ended June 30, 2024"
2025-04-30,BNL,financial_result,Financial Results for the Quarter Ended
2025-05-02,RMPL,material_info,Material Information
2025-05-02,THCCL,material_info,Material Information
2025-05-02,BAFL,material_info,Material Information - Completion of Divestiture of Shareholding in Alfalah
2025-05-02,MERIT,material_info,DISCLOSURE OF MATERIAL INFORMATION
2025-05-02,FNEL,material_info,Material Information
2025-05-02,OCTOPUS,financial_result,Financial Results for the Quarter Ended 31 March 2025
2025-05-02,AVN,financial_result,Financial Results for the Quarter Ended 31 March 2025
2025-05-02,WAVES,financial_result,Financial Results for the Quarter Ended 31 March 2025
2025-05-02,SEARL,financial_result,Transmission of Quarterly Report for the Period Ended 2025-03-31
2025-05-02,CPHL,financial_result,Transmission of financial statements for the Nine Months period ended 31 Ma
2025-05-02,AVN,financial_result,Transmission of Quarterly Report for the Period Ended 31 March 2025
2025-05-02,WAVES,financial_result,Transmission of Quarterly Report for the Period Ended 31 March 2025
2025-05-02,OCTOPUS,financial_result,OCTOPUS | Octopus Digital Limited Transmission of Quarterly Report for the 
2025-05-05,HASCOL,material_info,Material Information - Hascol welcomes the new Chief Executive Officer
2025-05-05,SLGL,financial_result,Financial Results for the Quarter Ended
2025-05-05,SLGL,financial_result,Transmission of Quarterly Report for the Period Ended
2025-05-06,BIPL,material_info,Disclosure of Material Information
2025-05-06,ZAL,material_info,Material Information
2025-05-06,BAHL,material_info,BAHL - Disclosure of Material Information
2025-05-06,PREMA,material_info,Material Information - Unusual Movement in Share Price
2025-05-06,TELE,financial_result,Transmission of Quarterly Accounts for the period ended 31 March 2025
2025-05-07,INIL,material_info,"MATERIAL INFORMATION INCORPORATION OF ""INIL EUROPE LIMITED"""
2025-05-07,HAEL,material_info,Material Information
2025-05-07,STPL,material_info,Material Information- Appointment of new auditor
2025-05-07,SHFA,financial_result,EMERGENT BOARD MEETING (OTHER THAN FINANCIAL RESULTS)
2025-05-08,OML,material_info,Material Information
2025-05-08,CASH,material_info,Material Information
2025-05-08,FFC,material_info,Material Information
2025-05-09,MLCF,material_info,MLCF-Disclosure of Material Information
2025-05-09,ISL,material_info,Material Information
2025-05-09,BCL,material_info,Material Information
2025-05-09,MFL,material_info,Material Information
2025-05-12,SHFA,material_info,Discloser of Material Information
2025-05-12,GFIL,material_info,Material Information
2025-05-12,CLOV,material_info,Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,17.274,2025-05-09
investor_type,last_5_sessions,broker proprietary trading,1.348,2025-05-09
investor_type,last_5_sessions,companies,8.01,2025-05-09
investor_type,last_5_sessions,foreign corporates,-0.872,2025-05-09
investor_type,last_5_sessions,foreign individual,0.022,2025-05-09
investor_type,last_5_sessions,individuals,-11.27,2025-05-09
investor_type,last_5_sessions,insurance companies,1.414,2025-05-09
investor_type,last_5_sessions,mutual funds,-26.393,2025-05-09
investor_type,last_5_sessions,nbfc,0.134,2025-05-09
investor_type,last_5_sessions,other organization,7.963,2025-05-09
investor_type,last_5_sessions,overseas pakistani,2.369,2025-05-09
sector,last_5_sessions,fipi | All other Sectors,1.503,2025-05-09
sector,last_5_sessions,fipi | Cement,4.856,2025-05-09
sector,last_5_sessions,fipi | Commercial Banks,-7.001,2025-05-09
sector,last_5_sessions,fipi | Fertilizer,0.509,2025-05-09
sector,last_5_sessions,fipi | Food and Personal Care Products,0.273,2025-05-09
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-1.417,2025-05-09
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,1.959,2025-05-09
sector,last_5_sessions,fipi | Power Generation and Distribution,0.746,2025-05-09
sector,last_5_sessions,fipi | Technology and Communication,-0.002,2025-05-09
sector,last_5_sessions,fipi | Textile Composite,0.094,2025-05-09
sector,last_5_sessions,lipi banks / dfi | All other Sectors,1.972,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Cement,-1.094,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,4.754,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Debt Market,2.038,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Fertilizer,1.793,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,0.316,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,2.231,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,3.344,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,1.31,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,0.5,2025-05-09
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.11,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,1.009,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.35,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.345,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,-0.396,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.902,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.014,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.51,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.146,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,0.244,2025-05-09
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,0.058,2025-05-09
sector,last_5_sessions,lipi companies | All other Sectors,1.563,2025-05-09
sector,last_5_sessions,lipi companies | Cement,-0.45,2025-05-09
sector,last_5_sessions,lipi companies | Commercial Banks,2.562,2025-05-09
sector,last_5_sessions,lipi companies | Fertilizer,0.837,2025-05-09
sector,last_5_sessions,lipi companies | Food and Personal Care Products,0.12,2025-05-09
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,3.246,2025-05-09
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,0.148,2025-05-09
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.395,2025-05-09
sector,last_5_sessions,lipi companies | Technology and Communication,0.485,2025-05-09
sector,last_5_sessions,lipi companies | Textile Composite,-0.107,2025-05-09
sector,last_5_sessions,lipi individuals | All other Sectors,-7.057,2025-05-09
sector,last_5_sessions,lipi individuals | Cement,-1.108,2025-05-09
sector,last_5_sessions,lipi individuals | Commercial Banks,-0.52,2025-05-09
sector,last_5_sessions,lipi individuals | Debt Market,-0.021,2025-05-09
sector,last_5_sessions,lipi individuals | Fertilizer,-0.011,2025-05-09
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,0.188,2025-05-09
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,0.716,2025-05-09
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-1.114,2025-05-09
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,-1.012,2025-05-09
sector,last_5_sessions,lipi individuals | Technology and Communication,-1.337,2025-05-09
sector,last_5_sessions,lipi individuals | Textile Composite,0.007,2025-05-09
sector,last_5_sessions,lipi insurance companies | All other Sectors,0.67,2025-05-09
sector,last_5_sessions,lipi insurance companies | Cement,0.099,2025-05-09
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-0.456,2025-05-09
sector,last_5_sessions,lipi insurance companies | Debt Market,0.623,2025-05-09
sector,last_5_sessions,lipi insurance companies | Fertilizer,-0.091,2025-05-09
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,-0.099,2025-05-09
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,0.384,2025-05-09
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.139,2025-05-09
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,-0.024,2025-05-09
sector,last_5_sessions,lipi insurance companies | Technology and Communication,0.017,2025-05-09
sector,last_5_sessions,lipi insurance companies | Textile Composite,0.151,2025-05-09
sector,last_5_sessions,lipi mutual funds | All other Sectors,-2.002,2025-05-09
sector,last_5_sessions,lipi mutual funds | Cement,-2.596,2025-05-09
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-2.968,2025-05-09
sector,last_5_sessions,lipi mutual funds | Debt Market,-2.785,2025-05-09
sector,last_5_sessions,lipi mutual funds | Fertilizer,-3.805,2025-05-09
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,0.084,2025-05-09
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-5.682,2025-05-09
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-5.028,2025-05-09
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.906,2025-05-09
sector,last_5_sessions,lipi mutual funds | Technology and Communication,-0.316,2025-05-09
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.39,2025-05-09
sector,last_5_sessions,lipi nbfc | All other Sectors,0.104,2025-05-09
sector,last_5_sessions,lipi nbfc | Cement,0.009,2025-05-09
sector,last_5_sessions,lipi nbfc | Commercial Banks,-0.007,2025-05-09
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.037,2025-05-09
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,-0.001,2025-05-09
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.043,2025-05-09
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.009,2025-05-09
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,0.011,2025-05-09
sector,last_5_sessions,lipi nbfc | Technology and Communication,0.002,2025-05-09
sector,last_5_sessions,lipi other organization | All other Sectors,2.237,2025-05-09
sector,last_5_sessions,lipi other organization | Cement,-0.067,2025-05-09
sector,last_5_sessions,lipi other organization | Commercial Banks,3.292,2025-05-09
sector,last_5_sessions,lipi other organization | Debt Market,0.145,2025-05-09
sector,last_5_sessions,lipi other organization | Fertilizer,1.201,2025-05-09
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,0.02,2025-05-09
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,0.493,2025-05-09
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.033,2025-05-09
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.123,2025-05-09
sector,last_5_sessions,lipi other organization | Technology and Communication,0.408,2025-05-09
sector,last_5_sessions,lipi other organization | Textile Composite,0.077,2025-05-09
investor_type,last_20_sessions,banks / dfi,125.315,2025-05-09
investor_type,last_20_sessions,broker proprietary trading,-6.65,2025-05-09
investor_type,last_20_sessions,companies,26.605,2025-05-09
investor_type,last_20_sessions,foreign corporates,-12.035,2025-05-09
investor_type,last_20_sessions,foreign individual,0.071,2025-05-09
investor_type,last_20_sessions,individuals,7.138,2025-05-09
investor_type,last_20_sessions,insurance companies,-33.166,2025-05-09
investor_type,last_20_sessions,mutual funds,-140.49,2025-05-09
investor_type,last_20_sessions,nbfc,0.409,2025-05-09
investor_type,last_20_sessions,other organization,28.318,2025-05-09
investor_type,last_20_sessions,overseas pakistani,4.485,2025-05-09
sector,last_20_sessions,fipi | All other Sectors,-5.427,2025-05-09
sector,last_20_sessions,fipi | Cement,9.09,2025-05-09
sector,last_20_sessions,fipi | Commercial Banks,-16.08,2025-05-09
sector,last_20_sessions,fipi | Fertilizer,-0.406,2025-05-09
sector,last_20_sessions,fipi | Food and Personal Care Products,-1.372,2025-05-09
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-1.427,2025-05-09
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,7.207,2025-05-09
sector,last_20_sessions,fipi | Power Generation and Distribution,1.488,2025-05-09
sector,last_20_sessions,fipi | Technology and Communication,-0.193,2025-05-09
sector,last_20_sessions,fipi | Textile Composite,-0.36,2025-05-09
sector,last_20_sessions,lipi banks / dfi | All other Sectors,-1.047,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Cement,-11.405,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,8.895,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Debt Market,119.138,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Fertilizer,1.617,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.316,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,3.318,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,2.756,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,1.409,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,0.126,2025-05-09
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.191,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-2.455,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Cement,0.032,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,-0.775,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.013,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-0.075,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.803,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-2.379,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.294,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.006,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,0.033,2025-05-09
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,0.084,2025-05-09
sector,last_20_sessions,lipi companies | All other Sectors,5.464,2025-05-09
sector,last_20_sessions,lipi companies | Cement,12.731,2025-05-09
sector,last_20_sessions,lipi companies | Commercial Banks,4.989,2025-05-09
sector,last_20_sessions,lipi companies | Debt Market,-0.35,2025-05-09
sector,last_20_sessions,lipi companies | Fertilizer,1.101,2025-05-09
sector,last_20_sessions,lipi companies | Food and Personal Care Products,-0.09,2025-05-09
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,2.687,2025-05-09
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,0.082,2025-05-09
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-0.709,2025-05-09
sector,last_20_sessions,lipi companies | Technology and Communication,0.831,2025-05-09
sector,last_20_sessions,lipi companies | Textile Composite,-0.131,2025-05-09
sector,last_20_sessions,lipi individuals | All other Sectors,-12.873,2025-05-09
sector,last_20_sessions,lipi individuals | Cement,-0.6,2025-05-09
sector,last_20_sessions,lipi individuals | Commercial Banks,5.166,2025-05-09
sector,last_20_sessions,lipi individuals | Debt Market,1.83,2025-05-09
sector,last_20_sessions,lipi individuals | Fertilizer,-4.264,2025-05-09
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,1.871,2025-05-09
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,14.166,2025-05-09
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,4.796,2025-05-09
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,-1.045,2025-05-09
sector,last_20_sessions,lipi individuals | Technology and Communication,-1.431,2025-05-09
sector,last_20_sessions,lipi individuals | Textile Composite,-0.478,2025-05-09
sector,last_20_sessions,lipi insurance companies | All other Sectors,4.165,2025-05-09
sector,last_20_sessions,lipi insurance companies | Cement,0.04,2025-05-09
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-19.347,2025-05-09
sector,last_20_sessions,lipi insurance companies | Debt Market,0.554,2025-05-09
sector,last_20_sessions,lipi insurance companies | Fertilizer,2.718,2025-05-09
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,-0.087,2025-05-09
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-7.981,2025-05-09
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-13.788,2025-05-09
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,-0.168,2025-05-09
sector,last_20_sessions,lipi insurance companies | Technology and Communication,0.504,2025-05-09
sector,last_20_sessions,lipi insurance companies | Textile Composite,0.224,2025-05-09
sector,last_20_sessions,lipi mutual funds | All other Sectors,4.782,2025-05-09
sector,last_20_sessions,lipi mutual funds | Cement,-11.162,2025-05-09
sector,last_20_sessions,lipi mutual funds | Commercial Banks,2.559,2025-05-09
sector,last_20_sessions,lipi mutual funds | Debt Market,-121.404,2025-05-09
sector,last_20_sessions,lipi mutual funds | Fertilizer,-3.117,2025-05-09
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,0.139,2025-05-09
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-9.938,2025-05-09
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.536,2025-05-09
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-1.41,2025-05-09
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-0.773,2025-05-09
sector,last_20_sessions,lipi mutual funds | Textile Composite,0.37,2025-05-09
sector,last_20_sessions,lipi nbfc | All other Sectors,0.174,2025-05-09
sector,last_20_sessions,lipi nbfc | Cement,0.029,2025-05-09
sector,last_20_sessions,lipi nbfc | Commercial Banks,0.152,2025-05-09
sector,last_20_sessions,lipi nbfc | Fertilizer,-0.012,2025-05-09
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,-0.007,2025-05-09
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.05,2025-05-09
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.03,2025-05-09
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,-0.0,2025-05-09
sector,last_20_sessions,lipi nbfc | Technology and Communication,-0.007,2025-05-09
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.001,2025-05-09
sector,last_20_sessions,lipi other organization | All other Sectors,7.218,2025-05-09
sector,last_20_sessions,lipi other organization | Cement,1.245,2025-05-09
sector,last_20_sessions,lipi other organization | Commercial Banks,14.441,2025-05-09
sector,last_20_sessions,lipi other organization | Debt Market,0.244,2025-05-09
sector,last_20_sessions,lipi other organization | Fertilizer,2.438,2025-05-09
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,0.033,2025-05-09
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,1.504,2025-05-09
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.254,2025-05-09
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,0.439,2025-05-09
sector,last_20_sessions,lipi other organization | Technology and Communication,0.909,2025-05-09
sector,last_20_sessions,lipi other organization | Textile Composite,0.1,2025-05-09

=== FILE: calendar.md ===
# Calendar as of 2025-05-12

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2025-04-14 FABL: Board of Directors Meeting of Faysal Bank Limited
- 2025-04-14 LCI: BOARD MEETING / CLOSED PERIOD
- 2025-04-14 FCEPL: Board Meeting 1st Quarter 2025
- 2025-04-14 HCAR: Board Meeting Other Than Financial Results
- 2025-04-14 CLOV: Board of Directors Meeting and Closed Period
- 2025-04-14 GTYR: Board Meeting
- 2025-04-15 INIL: Board Meeting
- 2025-04-15 PRL: Board Meeting
- 2025-04-15 SAZEW: Board Meeting Rescheduled
- 2025-04-15 BIPL: Board Meeting - BankIslami Pakistan Limited
- 2025-04-15 MLCF: MLCF-Notice of Board Meeting 22.04.2025
- 2025-04-15 KSBP: Board Meeting
- 2025-04-15 PIBTL: Board Meeting - Tuesday, April 22, 2025
- 2025-04-16 INIL: BOARD MEETING - OTHER THAN FINANCIAL RESULTS
- 2025-04-16 FFL: Board Meeting
- 2025-04-16 AGTL: Board Meeting
- 2025-04-16 LUCK: Board Meeting
- 2025-04-16 BFAGRO: Board Meeting & Closed Period Q3 2025
- 2025-04-16 ENGROH: Board Meeting for the Announcement of the Financial Results for the First Quarter ended March 31, 2025
- 2025-04-17 TPLP: Board Meeting
- 2025-04-17 MARI: Notice of Board of Directors Meeting
- 2025-04-17 GATM: BOARD MEETING
- 2025-04-17 POWER: Board Meeting
- 2025-04-17 FATIMA: Board Meeting and Closed Period
- 2025-04-17 GLAXO: Board Meeting Quarter ended March 31, 2025
- 2025-04-17 ACPL: Board Meeting
- 2025-04-17 ATBA: BOARD MEETING
- 2025-04-17 WAFI: Board Meeting
- 2025-04-17 SHFA: Board Meeting
- 2025-04-17 TREET: Notice of Board Meeting for the 3rd Quarter ended March 31, 2025 / Closed Period
- 2025-04-18 MTL: Board Meeting
- 2025-04-18 CEPB: BOARD MEETING
- 2025-04-18 SPEL: Board Meeting
- 2025-04-18 THCCL: Board Meeting for the quarter ended March 31, 2025
- 2025-04-18 NRL: Board Meeting
- 2025-04-18 TGL: Board Meeting
- 2025-04-18 GWLC: Notice of Board Meeting
- 2025-04-18 HALEON: Notice of Board of Directors Meeting - (Q1-2025)
- 2025-04-18 CHCC: Board Meeting REVOKED
- 2025-04-18 OGDC: Board Meeting
- 2025-04-18 FLYNG: Board Meeting
- 2025-04-18 PPL: Meeting of the Board of Directors and Closed Period
- 2025-04-18 SYS: Board Meeting
- 2025-04-18 SNGP: Board Meeting
- 2025-04-18 DGKC: BOARD MEETING
- 2025-04-21 OGDC: Board Meeting Rescheduled
- 2025-04-21 UNITY: Board Meeting
- 2025-04-21 ABOT: Board Meeting
- 2025-04-21 DCL: Board Meeting
- 2025-04-21 GGGL: MEETING OF THE BOARD OF DIRECTORS - GHANI GLOBAL GLASS LIMITED
- 2025-04-21 GGL: MEETING OF THE BOARD OF DIRECTORS - GHANI GLOBAL HOLDINGS LIMITED
- 2025-04-21 TOMCL: Board Meeting
- 2025-04-21 PAEL: Board Meeting for the 1st Quarter ended 31-03-2025
- 2025-04-21 IMAGE: Board Meeting
- 2025-04-21 BFBIO: Board Meeting
- 2025-04-21 BBFL: Board Meeting
- 2025-04-21 KOHC: Board Meeting
- 2025-04-21 PREMA: Board Meeting
- 2025-04-21 ZAL: Board Meeting
- 2025-04-21 HTL: Board Meeting REVOKED
- 2025-04-21 HUBC: Board Meeting - The Hub Power Company Limited
- 2025-04-21 LPL: BOARD MEETING
- 2025-04-21 HTL: Board Meeting
- 2025-04-22 AGP: Board Meeting
- 2025-04-22 ILP: Notice of Board Meeting for the Third Quarter ended March 31, 2025 / Closed Period
- 2025-04-22 PSO: Board Meeting
- 2025-04-22 MUGHAL: Notice of Board Meeting - QIII - FY 2025
- 2025-04-22 CSAP: Board Meetings
- 2025-04-22 SYM: Board Meeting
- 2025-04-22 FEROZ: Board Meeting
- 2025-04-22 DCR: BOARD MEETING / CLOSED PERIOD
- 2025-04-22 PABC: Board Meeting For 1st Quarter 2025 Financial Results and Other Matters
- 2025-04-22 OCTOPUS: Board Meeting
- 2025-04-22 AVN: Board Meeting
- 2025-04-22 FCL: Notice of the Board Meeting
- 2025-04-22 PIOC: Board Meeting
- 2025-04-22 NML: BOARD MEETING
- 2025-04-22 GHGL: Board Meeting
- 2025-04-23 CPHL: Board Meeting
- 2025-04-23 ATLH: Board Meeting
- 2025-04-23 NETSOL: Board Meeting
- 2025-04-23 TELE: Board Meeting to Consider Quarterly Accounts for the period ended 31 March 2025
- 2025-04-23 DOL: Board Meetings
- 2025-04-23 HINOON: Board Meeting
- 2025-04-23 SEARL: Board Meeting
- 2025-04-23 BNL: Board Meeting
- 2025-04-23 CNERGY: Board Meeting and Closed Period
- 2025-04-23 WAVES: Board Meeting for the Quarter ended 31Mar25
- 2025-04-30 FLYNG: Board Meeting Other Than Financial Results
- 2025-05-02 SSGC: Board Meeting

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
(no situation-library entry has an outcome that closed before this date, or the library has no INDEX.md)

=== FILE: base_rates.csv ===
type,as_of_cutoff,n,hit_rate,median,p50plus,source
none,,,,,,no base rates available
=== END ===
