# Replay bundle, close of 2026-04-24

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
# Market as of 2026-04-24 close (public information only)

- KSE100: 170,672 on 2026-04-24; 1m +11.6%, 3m -9.1%, 6m +4.5%, 12m +48.4%
- KMI All Share: 66,124 on 2026-04-24; 1m +10.2%, 3m -8.9%, 6m +0.8%, 12m +31.7%
- Policy rate 10.5%; last MPC decision 2026-03-09: hold (+0bp)
- 6M T-bill cutoff 11.15% (auction 2026-04-15); 3M 11.44%, 12M 11.89%
- CPI YoY 7.29% for 2026-03 (published by 2026-04-03); three months earlier (2025-12) 5.6%
- Brent: 111.86 USD/bbl on 2026-04-24; 3-month change +64.1%
- USD/PKR: 279.07  on 2026-04-24; 3-month change -0.4%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.65pp (market pricing hikes); CPI rising over 3 months (+1.7pp)
- Next MPC: see SBP calendar

Session date used: 2026-04-24. Liquid KMI names: 117 (membership KMI_ALL_derived_2025-12-02.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.2228,0.0057,0.189,1,1
E&P,3,0.1105,-0.0832,0.1194,0,1
OMC,4,0.2261,-0.133,-0.0567,0,0
Power,6,0.0575,-0.0835,0.1169,0,0
Fertilizer,4,0.0427,-0.1073,0.0864,0,0
Cement,16,0.0856,-0.2172,-0.0721,0,0
Steel & engineering,11,0.1451,-0.0888,-0.057,1,1
Autos,12,0.1789,-0.136,-0.1159,0,0
Tech & telecom,12,0.0075,-0.1039,-0.0437,0,0
Islamic banks & fin.,10,0.09,-0.0702,-0.1944,0,1
Pharma,14,0.1028,-0.127,-0.081,0,0
Textiles,23,0.2508,-0.0004,0.0689,0,1
Food & staples,15,0.1558,-0.1434,-0.0211,0,0
Chemicals,19,0.1519,-0.0871,0.0444,0,0
"Glass, packaging, paper",14,0.1427,-0.1674,-0.0924,0,0
Gas utilities & misc,13,0.1307,-0.1616,-0.084,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ABOT,920.2,0.038,-0.198,-0.2,-0.078,-0.262,2.333,0,2025-12-31,1.024,1,0,0,0,,
ACPL,230.7,-0.137,-0.166,-0.204,-0.1,-0.261,1.186,0,2025-06-30,-0.687,1,1,0,0,23.229,0.027
AGP,186.87,0.072,-0.134,-0.04,-0.062,-0.206,1.229,0,2025-12-31,0.035,1,0,0,0,17.84,0.024
AGTL,370.6,0.154,-0.13,-0.097,-0.232,-0.215,0.806,0,2025-12-31,0.339,2,0,0,0,9.191,
AIRLINK,142.87,0.054,-0.235,-0.146,-0.118,-0.255,0.731,0,2025-12-31,-0.005,0,0,0,0,12.707,0.046
ATRL,972.78,0.219,0.103,0.531,0.705,0.0,1.174,0,2025-12-31,0.032,0,1,0,0,8.095,0.015
AVN,32.01,0.05,-0.248,-0.333,-0.342,-0.393,0.701,0,2026-03-31,-0.794,2,0,0,0,,
BFBIO,148.25,0.103,-0.079,-0.044,-0.032,-0.214,0.529,0,2025-12-31,0.954,1,0,0,0,33.326,
BIFO,111.58,0.176,-0.319,-0.238,-0.25,-0.335,2.985,3,2026-03-31,-0.428,1,0,0,0,,
CHCC,280.53,0.102,-0.151,-0.152,0.053,-0.235,1.102,0,2025-12-31,-0.113,0,0,0,0,6.497,0.019
CLOV,8.09,0.285,0.462,0.9,0.97,-0.09,4.24,2,2025-12-31,-0.059,0,0,0,0,,
CNERGY,8.08,0.185,0.011,0.036,0.011,-0.109,1.6,0,2024-06-30,,0,0,0,0,,
CPHL,80.02,0.098,-0.116,-0.099,-0.055,-0.183,1.363,0,2025-12-31,0.58,0,0,0,0,21.506,0.042
CRTM,78.73,0.585,2.255,2.297,4.933,-0.105,1.442,2,,,0,0,0,0,,
CSAP,93.36,0.001,-0.295,-0.009,-0.21,-0.314,1.31,0,2026-03-31,-1.217,1,0,0,0,,0.065
DGKC,183.83,0.13,-0.222,-0.215,0.512,-0.317,1.648,0,2025-12-31,0.314,0,0,0,0,7.851,0.012
EFERT,199.12,-0.004,-0.172,-0.054,0.217,-0.204,0.931,0,2026-03-31,0.148,2,0,0,0,9.648,0.105
ENGROH,281.51,0.036,0.029,0.185,0.706,-0.055,0.953,0,2025-12-31,-0.166,1,1,0,0,9.7,0.04
EPCL,32.87,0.077,0.006,0.154,0.061,-0.148,0.639,0,2026-03-31,,2,0,0,0,,
EPQL,23.6,-0.041,-0.215,-0.147,-0.11,-0.281,0.997,0,2026-03-31,-0.605,1,0,0,0,,
FABL,88.52,0.051,-0.084,0.034,1.019,-0.129,1.108,0,2026-03-31,-0.014,1,0,0,0,3.08,0.144
FATIMA,140.21,0.083,-0.19,0.034,0.866,-0.239,1.248,0,2026-03-31,-0.614,2,0,0,0,4.517,0.089
FCCL,50.31,0.241,-0.148,-0.095,0.17,-0.176,1.234,0,2025-12-31,0.0,1,0,0,0,8.222,0.028
FCEPL,85.87,0.223,0.022,0.042,-0.046,-0.181,1.053,1,2024-09-30,2.03,2,0,0,0,31.055,0.031
FCL,22.2,0.063,-0.134,-0.051,-0.051,-0.2,0.56,0,2025-12-31,-0.163,1,0,0,0,12.305,0.021
FFC,524.75,0.052,-0.109,0.139,0.608,-0.208,0.669,0,2025-12-31,-0.021,0,0,0,0,5.523,0.112
FFL,18.0,0.192,-0.221,-0.064,0.16,-0.223,0.83,0,2025-12-31,1.0,0,0,0,0,68.835,
GAL,453.66,0.322,-0.158,-0.18,-0.028,-0.257,1.64,2,2026-03-31,0.611,1,0,0,0,5.252,0.026
GCIL,30.47,0.155,-0.129,-0.046,0.805,-0.208,0.675,0,,,0,0,0,0,,
GHNI,827.86,0.267,-0.101,-0.044,0.137,-0.181,1.442,0,2026-03-31,0.541,2,0,0,0,6.046,0.015
GLAXO,364.73,0.14,-0.125,-0.057,-0.144,-0.168,1.7,0,2025-12-31,0.283,2,1,0,0,19.339,0.025
HALEON,764.61,0.091,-0.189,-0.13,0.03,-0.212,1.502,0,2025-12-31,0.3,1,0,0,0,20.65,0.025
HCAR,182.68,0.113,-0.3,-0.371,-0.354,-0.413,1.111,1,2025-12-31,0.156,0,0,0,0,15.254,0.028
HINOON,955.52,0.158,-0.046,-0.127,0.099,-0.183,2.031,0,2025-12-31,0.458,2,0,0,0,,
HTL,51.13,0.459,-0.161,-0.14,0.261,-0.19,1.268,2,,,0,0,0,0,,
HUBC,227.47,0.152,-0.027,0.118,0.805,-0.046,0.925,0,2026-03-31,-0.021,2,0,0,0,3.875,0.109
ILP,80.13,0.02,-0.018,0.071,0.476,-0.135,0.887,0,2025-12-31,1.842,0,0,0,0,17.114,0.015
INIL,165.31,0.118,-0.108,-0.211,0.127,-0.302,1.058,0,2026-03-31,-0.172,1,0,0,0,25.968,0.023
IPAK,29.8,0.189,-0.001,0.15,0.421,-0.08,0.979,0,2026-03-31,1.015,1,0,0,0,13.394,0.027
ISL,82.02,0.123,-0.24,-0.196,0.16,-0.346,1.261,0,2026-03-31,0.896,1,0,0,0,25.861,0.027
JVDC,134.71,0.314,-0.04,0.92,1.333,-0.159,0.946,0,2025-12-31,3.976,0,0,0,0,14.977,0.078
KEL,7.8,0.105,0.099,0.388,0.84,-0.172,0.755,0,2024-06-30,-0.871,0,2,0,0,30.127,
KOHC,88.93,0.093,-0.231,-0.085,0.181,-0.273,1.038,0,2026-03-31,-0.151,1,0,0,0,6.026,
KSBP,192.77,-0.039,-0.009,-0.066,0.131,-0.261,1.376,0,2026-03-31,0.169,3,0,0,0,,
KTML,49.91,0.114,-0.232,-0.223,0.486,-0.321,0.386,0,2024-12-31,1.398,1,0,0,0,3.207,0.01
LOADS,13.29,0.09,-0.256,-0.262,-0.204,-0.359,1.656,0,2026-03-31,1.714,1,0,0,0,13.777,
LOTCHEM,28.8,0.228,0.035,0.248,0.9,-0.037,1.224,1,2026-03-31,1.204,2,0,0,0,11.982,0.239
LUCK,430.25,0.174,-0.131,-0.049,0.238,-0.161,1.385,0,2025-12-31,0.055,0,1,0,0,6.763,0.011
MARI,655.21,0.045,-0.098,-0.103,0.094,-0.159,0.9,0,2026-03-31,0.311,1,1,0,0,11.514,0.035
MEBL,494.48,0.09,0.062,0.172,1.042,-0.047,0.933,0,2026-03-31,0.006,1,0,0,0,4.229,0.116
MLCF,87.57,0.086,-0.283,-0.102,0.352,-0.328,1.296,0,2024-12-31,0.708,1,0,0,0,7.675,
MTL,511.89,0.038,-0.004,0.038,-0.091,-0.088,0.637,0,2025-12-31,-0.241,0,0,0,0,17.531,0.107
MUGHAL,76.39,0.08,-0.241,-0.095,0.16,-0.309,0.906,0,2025-12-31,1.333,0,0,0,0,28.337,
NETSOL,118.55,0.168,-0.084,-0.158,-0.081,-0.271,1.773,0,2025-12-31,,0,0,0,0,8.173,
NML,156.9,0.158,-0.203,0.044,0.454,-0.235,1.031,0,2025-12-31,,0,0,0,0,8.671,0.016
NRL,382.61,0.208,-0.14,0.089,0.674,-0.174,0.999,0,2025-12-31,,0,0,0,0,,
OCTOPUS,31.7,-0.027,-0.242,-0.349,-0.392,-0.466,1.282,0,,,2,0,0,0,,
OGDC,325.9,0.189,-0.005,0.27,0.642,-0.009,1.161,0,2025-12-31,-0.162,0,1,0,0,5.583,0.068
PAEL,42.27,0.154,-0.316,-0.226,-0.061,-0.33,1.498,0,2025-12-31,0.246,1,0,0,0,16.997,
PAKQATAR,17.96,0.053,-0.197,,,,0.318,0,,,2,0,0,0,,
PIBTL,16.19,0.112,-0.259,0.037,0.754,-0.283,0.8,0,2026-03-31,,1,0,0,0,,
PIOC,227.05,-0.0,-0.43,0.017,0.102,-0.461,0.191,0,2026-03-31,0.562,1,0,0,0,10.627,0.044
POWER,19.36,0.159,-0.048,0.057,0.34,-0.104,0.614,0,2026-03-31,2.0,1,0,0,0,31.257,
PPL,232.0,0.1,-0.149,0.213,0.452,-0.168,0.854,0,2025-12-31,-0.262,0,0,0,0,5.148,0.044
PQGTL,13.37,0.272,,,,,0.68,0,,,2,0,0,0,,
PREMA,35.93,0.379,-0.078,-0.1,-0.544,-0.586,0.977,4,2025-12-31,0.444,0,1,0,0,16.658,
PRL,37.42,0.27,-0.017,0.047,0.221,-0.067,1.635,0,2026-03-31,,2,0,0,0,,
PSO,393.07,0.092,-0.206,-0.155,0.082,-0.219,1.146,0,2025-12-31,-0.336,0,0,0,0,10.778,0.026
QUICE,24.14,0.067,-0.327,1.659,2.307,-0.424,0.416,0,,,0,0,0,0,,
SAZEW,2098.86,0.24,0.071,0.133,0.667,-0.145,1.779,0,2026-03-31,0.034,2,1,0,0,4.217,0.046
SEARL,93.88,0.124,-0.255,-0.162,0.193,-0.305,0.733,0,2025-12-31,,0,0,0,0,,
SGF,102.87,0.212,-0.121,0.196,0.31,-0.203,0.524,1,2025-12-31,-0.128,1,1,0,0,,
SGPL,48.42,2.379,0.737,3.022,5.725,0.0,1.447,5,2025-12-31,,0,0,0,0,,
SLGL,15.15,0.015,-0.28,-0.3,-0.039,-0.397,0.478,0,2025-12-31,-0.728,2,0,0,0,7.077,
SNGP,101.37,0.122,-0.149,-0.227,-0.099,-0.259,1.389,0,2025-12-31,-0.166,0,1,0,0,5.073,0.026
SPEL,43.11,0.216,-0.242,-0.249,0.095,-0.439,0.691,0,2026-03-31,-0.084,1,0,0,0,,
SSGC,28.4,0.322,-0.17,-0.276,-0.298,-0.381,2.036,1,2025-12-31,-0.725,0,0,0,0,10.954,0.012
SYS,152.35,0.107,-0.024,-0.026,0.575,-0.111,0.83,0,2025-12-31,0.5,2,0,0,0,24.356,0.01
TATM,144.19,0.591,-0.199,0.012,2.237,-0.509,0.454,1,2025-12-31,-0.944,0,0,0,0,6.525,
TELE,8.69,0.187,-0.284,-0.31,0.176,-0.345,0.839,0,2025-12-31,-0.75,0,0,0,0,18.478,
TOMCL,36.76,0.181,-0.301,-0.408,0.164,-0.445,0.574,0,2025-12-31,-0.04,0,0,0,0,13.655,
TPLP,8.79,0.295,-0.293,-0.191,-0.062,-0.32,0.848,0,,,0,0,0,0,,
TREET,25.12,0.13,-0.278,-0.222,0.264,-0.306,0.778,0,2025-12-31,0.111,0,0,0,0,17.461,
TRSM,17.24,-0.047,-0.035,-0.744,2.732,-0.748,0.528,1,2025-12-31,-0.345,0,0,0,0,,
WAFI,205.99,0.172,-0.13,0.132,0.268,-0.157,0.993,0,2025-12-31,-0.801,2,0,0,0,13.796,0.024
WAVES,10.38,0.069,-0.304,-0.147,0.375,-0.369,0.61,0,2025-09-30,-0.189,2,0,0,0,2.445,
ZAL,56.22,0.437,-0.188,0.402,2.82,-0.222,0.672,1,2025-12-31,2.354,0,0,0,0,6.31,0.062

=== FILE: announcements_30d.csv ===
date,symbol,klass,title

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-31.949,2026-04-23
investor_type,last_5_sessions,broker proprietary trading,-2.456,2026-04-23
investor_type,last_5_sessions,companies,1.993,2026-04-23
investor_type,last_5_sessions,foreign corporates,-2.125,2026-04-23
investor_type,last_5_sessions,foreign individual,0.049,2026-04-23
investor_type,last_5_sessions,individuals,16.52,2026-04-23
investor_type,last_5_sessions,insurance companies,14.159,2026-04-23
investor_type,last_5_sessions,mutual funds,10.998,2026-04-23
investor_type,last_5_sessions,nbfc,-0.006,2026-04-23
investor_type,last_5_sessions,other organization,-8.458,2026-04-23
investor_type,last_5_sessions,overseas pakistani,1.275,2026-04-23
sector,last_5_sessions,lipi banks / dfi | Debt Market,-29.423,2026-04-23
sector,last_5_sessions,lipi individuals | All other Sectors,6.517,2026-04-23
sector,last_5_sessions,lipi individuals | Cement,5.092,2026-04-23
sector,last_5_sessions,lipi individuals | Commercial Banks,9.731,2026-04-23
sector,last_5_sessions,lipi individuals | Fertilizer,4.683,2026-04-23
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,-4.386,2026-04-23
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,-3.147,2026-04-23
sector,last_5_sessions,lipi insurance companies | All other Sectors,-10.83,2026-04-23
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-4.561,2026-04-23
sector,last_5_sessions,lipi insurance companies | Debt Market,30.803,2026-04-23
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,8.633,2026-04-23
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,-3.277,2026-04-23
investor_type,last_20_sessions,banks / dfi,-7.746,2026-04-23
investor_type,last_20_sessions,broker proprietary trading,-2.62,2026-04-23
investor_type,last_20_sessions,companies,7.353,2026-04-23
investor_type,last_20_sessions,foreign corporates,-13.675,2026-04-23
investor_type,last_20_sessions,foreign individual,0.078,2026-04-23
investor_type,last_20_sessions,individuals,46.075,2026-04-23
investor_type,last_20_sessions,insurance companies,-37.874,2026-04-23
investor_type,last_20_sessions,mutual funds,6.206,2026-04-23
investor_type,last_20_sessions,nbfc,-0.287,2026-04-23
investor_type,last_20_sessions,other organization,-8.256,2026-04-23
investor_type,last_20_sessions,overseas pakistani,10.746,2026-04-23
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-16.505,2026-04-23
sector,last_20_sessions,lipi banks / dfi | Debt Market,44.139,2026-04-23
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,-10.082,2026-04-23
sector,last_20_sessions,lipi companies | Commercial Banks,11.345,2026-04-23
sector,last_20_sessions,lipi individuals | All other Sectors,18.732,2026-04-23
sector,last_20_sessions,lipi individuals | Commercial Banks,19.308,2026-04-23
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,-10.982,2026-04-23
sector,last_20_sessions,lipi insurance companies | All other Sectors,-14.792,2026-04-23
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-11.825,2026-04-23
sector,last_20_sessions,lipi mutual funds | Debt Market,-45.595,2026-04-23
sector,last_20_sessions,lipi mutual funds | Fertilizer,10.609,2026-04-23
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,19.163,2026-04-23

=== FILE: calendar.md ===
# Calendar as of 2026-04-24

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2026-03-26 PSO: Board Meeting Other Than Financial Results
- 2026-03-27 SYS: Board Meeting for the Year Ended December 31, 2025
- 2026-03-27 WAVES: Board Meeting-Annual Accounts for the year Ended 31Dec25
- 2026-03-30 HINOON: Board Meeting
- 2026-03-31 GCWL: MEETING OF THE BOARD OF DIRECTORS OTHER THAN FINANCIAL RESULTS - GHANI CHEMWORLD LIMITED
- 2026-04-01 ACPL: Board Meeting
- 2026-04-01 SGPL: Board Meeting Other Than Financial Results
- 2026-04-01 PAKQATAR: Board Meeting
- 2026-04-01 PQGTL: Board Meeting
- 2026-04-02 NRL: Board Meeting
- 2026-04-03 SYS: Board Meeting Rescheduled for the Year Ended December 31, 2025
- 2026-04-03 CRTM: Board Meeting Other Than Financial Results
- 2026-04-06 GCWL: DECISIONS OF THE BOARD OF DIRECTORS MEETING - GHANI CHEMWORLD LIMITED
- 2026-04-07 NRL: Board Meeting Rescheduled
- 2026-04-07 EFERT: Board Meeting for the announcement of the financial results for the first quarter ended March 31, 2026
- 2026-04-08 INIL: Board Meeting
- 2026-04-08 EPQL: Board Meeting for the announcement of the financial results for the three months ended March 31, 2026
- 2026-04-08 KEL: Board Meeting Other Than Financial Results
- 2026-04-08 IPAK: Board Meeting for the Third Quarter ended 31st March 2026
- 2026-04-09 SGPL: Board Meeting Other Than Financial Results
- 2026-04-10 PSO: Board Meeting Other Than Financial Results
- 2026-04-10 SPEL: Board Meeting
- 2026-04-10 MEBL: NOTICE OF BOARD MEETING AND CLOSED PERIOD - MEEZAN BANK LIMITED
- 2026-04-10 SAZEW: Board Meeting
- 2026-04-10 EPCL: Board Meeting - Q1 2026 - Engro Polymer & Chemicals Limited
- 2026-04-10 GHNI: Board Meeting
- 2026-04-10 LOTCHEM: Board Meeting
- 2026-04-10 ISL: Board Meeting
- 2026-04-10 GAL: Board Meeting
- 2026-04-10 CRTM: Board Meeting Other Than Financial Results
- 2026-04-13 PRL: Board Meeting
- 2026-04-13 POWER: Board Meeting
- 2026-04-13 FABL: Board of Directors Meeting of Faysal Bank Limited
- 2026-04-13 PIOC: Board Meeting
- 2026-04-14 PIBTL: Board Meeting -PIBTL
- 2026-04-14 KSBP: Board Meeting
- 2026-04-14 MLCF: MLCF-Notice of Board Meeting 21.04.2026
- 2026-04-14 HUBC: Board Meeting for the Third Quarter Ended March 31, 2026 - The Hub Power Company Limited
- 2026-04-14 CSAP: Notice of 204th Board Meeting for the Third Quarter Ended March 31, 2026
- 2026-04-15 LOADS: Board Meeting of Loads Limited
- 2026-04-15 KTML: KTML Notice of Board Meeting 22.04.2026
- 2026-04-15 KEL: Board Meeting Other Than Financial Results
- 2026-04-16 MARI: Notice of Board of Directors Meeting
- 2026-04-16 FCEPL: Board Meeting 1st Quarter 2026
- 2026-04-16 BIFO: Meeting of the Board of Directors
- 2026-04-16 ENGROH: Board Meeting for the Announcement of Financial Results for the Three Months Ended March 31, 2026
- 2026-04-16 KOHC: Board Meeting
- 2026-04-16 SGPL: Board Meeting Material Information
- 2026-04-16 FATIMA: Board meeting and closed period
- 2026-04-17 SAZEW: Board Meeting Rescheduled
- 2026-04-17 GWLC: Board Meeting
- 2026-04-17 LCI: Board Meeting / Closed Period
- 2026-04-17 BIPL: Board Meeting - BankIslami Pakistan Limited
- 2026-04-17 BBFL: Board Meeting
- 2026-04-17 CHCC: Board Meeting
- 2026-04-20 DCL: Board Meeting
- 2026-04-20 GLAXO: Board Meeting Quarter 1- 2026
- 2026-04-20 ITTEFAQ: BOARD MEETING
- 2026-04-20 BFBIO: Board Meeting
- 2026-04-20 ICL: Board Meeting
- 2026-04-20 CNERGY: Board Meeting and Closed Period
- 2026-04-20 BFAGRO: Board Meeting
- 2026-04-20 ABOT: Board Meeting
- 2026-04-20 ZAL: Board Meeting
- 2026-04-20 FCL: Notice of Board Meeting/closed period of FCL
- 2026-04-20 OGDC: Board Meeting and Closed Period
- 2026-04-20 GCWL: Meeting of the Board of Directors - GHANI CHEMWORLD LIMITED
- 2026-04-20 GCIL: Meeting of the Board of Directors - GHANI CHEMICAL INDUSTRIES LIMITED
- 2026-04-20 PPL: Meeting of the Board of Directors and Closed Period
- 2026-04-20 GGL: Meeting of the Board of Directors - GHANI GLOBAL HOLDINGS LIMITED
- 2026-04-20 FFL: Board Meeting
- 2026-04-20 FECTC: Board Meeting for the Quarter Ended March 31, 2026 & Annoucement of Closed Period
- 2026-04-20 HTL: Board Meeting
- 2026-04-20 ASL: BOARD MEETING / CLOSED PERIOD
- 2026-04-21 PREMA: Board Meeting
- 2026-04-21 QUICE: BOARD MEETING
- 2026-04-21 MACFL: Board meeting
- 2026-04-21 HALEON: Notice of Board of Directors Meeting - (Q1-2026)
- 2026-04-21 SSOM: Board Meeting
- 2026-04-21 IBLHL: Board Meeting
- 2026-04-21 TPLP: Board Meeting
- 2026-04-21 SGF: Board Meeting
- 2026-04-21 TGL: Board Meeting
- 2026-04-21 CEPB: BOARD MEETING
- 2026-04-21 SNGP: Board Meeting
- 2026-04-21 TRSM: Board of Directors Meeting for the Quarter ended March 31, 2026.
- 2026-04-21 GHGL: BOARD MEETING
- 2026-04-21 CLOV: Board of Directors Meeting and Closed Period
- 2026-04-21 SYM: Board Meeting
- 2026-04-21 WAFI: Board Meeting
- 2026-04-21 TBL: Notice of Board Meeting Q3 FY 25-26
- 2026-04-21 DGKC: Board Meeting
- 2026-04-21 GTYR: Board Meeting
- 2026-04-21 MTL: BOARD MEETING FOR QUARTERLY RESULTS
- 2026-04-21 TOMCL: Board Meeting
- 2026-04-21 OCTOPUS: Board Meeting
- 2026-04-21 LUCK: Board Meeting
- 2026-04-22 PSO: Board Meeting
- 2026-04-22 ILP: Notice of Board Meeting for the Third Quarter ended March 31, 2026 / Closed Period
- 2026-04-22 MUGHAL: Notice of Board Meeting - QIII - 2026
- 2026-04-22 MARI: Board of Directors Meeting - Change of Place
- 2026-04-22 ANL: Board Meeting
- 2026-04-22 IMAGE: Board Meeting
- 2026-04-22 OBOY: NOTICE OF BOARD MEETING
- 2026-04-22 AGTL: Board Meeting
- 2026-04-22 CRTM: Board Meeting
- 2026-04-22 SSGC: Board Meeting
- 2026-04-22 HINOON: Board Meeting
- 2026-04-22 GDL: Board Meeting
- 2026-04-22 PAEL: Board Meeting for the 1st Quarter ended 31-03-2026 (Un-Audited)
- 2026-04-22 SEARL: Board Meeting
- 2026-04-22 NETSOL: Board Meeting
- 2026-04-22 GATM: BOARD MEETING AND CLOSED PERIOD
- 2026-04-22 TATM: Meeting of the Board of Directors
- 2026-04-22 BECO: Board Meeting
- 2026-04-22 FFC: Board Meeting
- 2026-04-22 FEROZ: Board Meeting
- 2026-04-22 SGPL: BOARD MEETING TO CONSIDER AND APPROVE QUARTERLY FINANCIAL STATEMENTS
- 2026-04-22 AGP: Board Meeting
- 2026-04-22 TREET: Notice of Board Meeting for the Third Quarter ended March 31, 2026 / Closed Period
- 2026-04-22 NML: Board Meeting
- 2026-04-22 AVN: Board Meeting
- 2026-04-22 DCR: BOARD MEETING / CLOSED PERIOD
- 2026-04-23 CPHL: Board Meeting
- 2026-04-23 FFL: Board Meeting Rescheduled
- 2026-04-23 TELE: Board Meeting
- 2026-04-23 BNL: Board Meeting
- 2026-04-23 WAVES: Board Meeting for the Quarter ended 31Mar26
- 2026-04-23 PAKQATAR: Board Meetings
- 2026-04-23 PQGTL: Board Meetings

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
**Establishment and SIFC.** The SIFC (created mid-2023, army chief a member, agriculture, mining and IT focus, IMF asked about its powers) was described by a government adviser to mining.com (date not shown). Reuters in 2020 reported the military as the most influential voice on Reko Diq. Establishment-linked capital is visible in listed names: Fauji Foundation owns 44.32% of FFC (FFC H1-26 report), FFC holds 33.99% of the PIA buyer (repo), a Fauji Foundation and KAPCO group bought Attock Cement
| 1 | Brownfield refinery policy | 17 Aug 2023 | outcome not shown |
| 3 | OMC margin +Rs1.22 | OCAC ask Apr 2025 | outcome not shown |
| 6 | Rs1.225tn power bank facility | 2025 | outcome not shown |
| 7 | IPP terminations | 2024 (unverified) | 5 PPAs ended Oct 2024; Rs1tn savings claimed 29 Dec. Y |

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
corp_E1a_buyback_approval,20 sessions (KMI members),,54%,+0.7%,,,,nothing
corp_E1a_buyback_approval,60 sessions (KMI members),13,54%,+0.7%,0%,-19%,-1.2%,nothing; mean +1.2%; <-30% 0%; p(med) 0.40; placebo is matched P2 median
corp_E1a_buyback_approval,120 sessions (KMI members),11,64%,+4.8%,,,,nothing
corp_E1a_buyback_approval,20% trailing stop (KMI members),12,42%,-3.5%,17%,-23%,,nothing; stop mean +46.3%
corp_E1b_first_purchase,20 sessions (KMI members),,33%,-1.8%,,,,nothing
corp_E1b_first_purchase,60 sessions (KMI members),15,47%,-2.4%,0%,-17%,+0.6%,nothing; mean +0.1%; <-30% 0%; p(med) 0.74; placebo is matched P2 median
corp_E1b_first_purchase,120 sessions (KMI members),13,62%,+5.7%,,,,nothing
corp_E1b_first_purchase,20% trailing stop (KMI members),14,36%,-6.5%,14%,-23%,,nothing; stop mean +62.0% (THCCL runner)
corp_E2a_bonus,20 sessions (KMI members),,42%,-2.9%,,,,nothing
corp_E2a_bonus,60 sessions (KMI members),89,39%,-6.0%,2%,-35%,-3.9%,nothing; mean -1.6%; <-30% 4%; p(med) 0.84; placebo is matched P2 median
corp_E2a_bonus,120 sessions (KMI members),88,39%,-7.4%,,,,nothing
corp_E2a_bonus,20% trailing stop (KMI members),89,31%,-12.8%,8%,-28%,,nothing; stop mean +0.5%
corp_E2b_split,20 sessions (KMI members),,50%,+2.0%,,,,watch
corp_E2b_split,60 sessions (KMI members),9,89%,+13.9%,0%,-13%,-3.4%,watch (thin tail); mean +14.8%; <-30% 0%; p(med) 0.04; placebo is matched P2 median
corp_E2b_split,120 sessions (KMI members),8,62%,+12.9%,,,,watch
corp_E2b_split,20% trailing stop (KMI members),9,67%,+11.3%,11%,-23%,,watch; stop mean +20.1%
corp_E3a_ceo_chairman_appointed,20 sessions (KMI members),,42%,-1.5%,,,,nothing
corp_E3a_ceo_chairman_appointed,60 sessions (KMI members),526,49%,-0.5%,5%,-97%,-1.6%,nothing; mean +2.9%; <-30% 6%; p(med) 0.14; placebo is matched P2 median
corp_E3a_ceo_chairman_appointed,120 sessions (KMI members),496,47%,-2.1%,,,,nothing
corp_E3a_ceo_chairman_appointed,20% trailing stop (KMI members),511,36%,-8.5%,10%,-90%,,nothing; stop mean +6.1%
corp_E3b_resigns,20 sessions (KMI members),,48%,-1.5%,,,,nothing (lean avoid)
corp_E3b_resigns,60 sessions (KMI members),27,48%,-4.9%,4%,-66%,+0.1%,nothing (lean avoid); mean -2.5%; <-30% 4%; p(med) 0.90; placebo is matched P2 median
corp_E3b_resigns,120 sessions (KMI members),26,35%,-6.9%,,,,nothing (lean avoid)
corp_E3b_resigns,20% trailing stop (KMI members),25,20%,-13.0%,12%,-30%,,nothing (lean avoid); stop mean -3.2%
corp_E3d_takeover_or_mgmt_change,20 sessions (KMI members),,35%,-2.1%,,,,nothing
corp_E3d_takeover_or_mgmt_change,60 sessions (KMI members),74,50%,+0.0%,5%,-66%,-1.4%,nothing; mean +1.4%; <-30% 7%; p(med) 0.24; placebo is matched P2 median
corp_E3d_takeover_or_mgmt_change,120 sessions (KMI members),71,49%,-0.6%,,,,nothing
corp_E3d_takeover_or_mgmt_change,20% trailing stop (KMI members),72,40%,-7.8%,8%,-53%,,nothing; stop mean +4.4%
corp_E4a_psx_letter,20 sessions (KMI members),,41%,-4.0%,,,,nothing as a buy; avoid after a run-up
corp_E4a_psx_letter,60 sessions (KMI members),373,43%,-3.7%,8%,-82%,-0.6%,nothing as a buy; avoid after a run-up; mean +4.6%; <-30% 10%; p(med) 1.00; placebo is matched P2 median
corp_E4a_psx_letter,120 sessions (KMI members),318,52%,+0.7%,,,,nothing as a buy; avoid after a run-up
corp_E4a_psx_letter,20% trailing stop (KMI members),394,34%,-12.6%,11%,-80%,,nothing as a buy; stop mean +9.3%
corp_E4b_company_reply,20 sessions (KMI members),,43%,-3.9%,,,,nothing
corp_E4b_company_reply,60 sessions (KMI members),29,59%,+4.0%,14%,-58%,-0.2%,nothing (n 29); mean +20.4%; <-30% 10%; p(med) 0.22; placebo is matched P2 median
corp_E4b_company_reply,120 sessions (KMI members),25,56%,+4.7%,,,,nothing
corp_E4b_company_reply,20% trailing stop (KMI members),29,41%,-7.7%,7%,-26%,,nothing; stop mean +11.2%
corp_E5_rating_upgrade,20 sessions (KMI members),,57%,+2.1%,,,,nothing (anecdote)
corp_E5_rating_upgrade,60 sessions (KMI members),7,57%,+8.5%,0%,-28%,+0.2%,nothing (anecdote); mean +3.1%; <-30% 0%; p(med) 0.15; placebo is matched P2 median
corp_E5_rating_upgrade,120 sessions (KMI members),6,33%,-5.7%,,,,nothing (anecdote)
corp_E5_rating_upgrade,20% trailing stop (KMI members),7,43%,-8.4%,14%,-21%,,nothing (anecdote); stop mean +4.6%
corp_E6_rights_issue,20 sessions (KMI members),,34%,-4.5%,,,,avoid
corp_E6_rights_issue,60 sessions (KMI members),76,33%,-9.1%,7%,-66%,-3.8%,avoid; mean -4.6%; <-30% 14%; p(med) 0.99; placebo is matched P2 median
corp_E6_rights_issue,120 sessions (KMI members),72,28%,-15.4%,,,,avoid
corp_E6_rights_issue,20% trailing stop (KMI members),75,25%,-15.2%,4%,-37%,,avoid; stop mean -6.9%
corp_E7_kmi_addition,20 sessions (KMI members),,51%,+0.2%,,,,nothing (avoid chasing)
corp_E7_kmi_addition,60 sessions (KMI members),388,36%,-4.9%,3%,-62%,-0.2%,nothing (avoid chasing); mean +0.7%; <-30% 4%; p(med) 1.00; placebo is matched P2 median
corp_E7_kmi_addition,120 sessions (KMI members),352,41%,-5.1%,,,,nothing (avoid chasing)
corp_E7_kmi_addition,20% trailing stop (KMI members),378,33%,-10.3%,10%,-42%,,nothing; stop mean +5.5%
compounders_3x_share_5y,5 years (start 2016-12-30),155,3.2%,,,,,watch (population; 5 names with 3x)
compounders_3x_share_5y,5 years (start 2017-12-29),85,2.4%,,,,,watch (population; 2 names with 3x)
compounders_3x_share_5y,5 years (start 2018-12-31),97,5.2%,,,,,watch (population; 5 names with 3x)
compounders_3x_share_5y,5 years (start 2019-12-31),111,16.2%,,,,,watch (population; 18 names with 3x)
compounders_3x_share_5y,5 years (start 2020-12-31),124,23.4%,,,,,watch (population; 29 names with 3x)
compounders_3x_share_5y,5 years (start 2021-09-30),137,21.2%,,,,,watch (population; 29 names with 3x)
compounders_3x_share_5y,5 years (pooled over 58 starts; n is the average),108,12.1%,,,,,watch (population; 75 names had a 3x window)
compounders_3x_share_decade,9.8 years (2016-12-30 to 2026-10-16),155,20.0%,,,,,watch (population; 31 names with 3x)
compounders_growth_core_1y_position,1 year rule variant (start 2023-09-28; position level; file label 1y variant),39,51%,+6.6%,26%,-35.3%,,nothing; mean +26.3%; 8% below -30%
compounders_growth_core_2y_position,2 year rule variant (start 2024-09-30; position level; file label 2y variant),23,61%,+10.1%,26%,-52.6%,,nothing; mean +24.6%; 4% below -30%
compounders_growth_core_3y_position,3 year rule variant (position level; file label 3y variant),17,24%,-8.0%,,,,nothing; mean -4.7%
compounders_growth_core_3y_fixed,1.04 years (start 2025-09-30),,,,,,,nothing; fixed 0.88x (-11.7%) vs KMI TR 0.96x; EW liquid KMI 0.88x; placebo median 0.93x (pctile 30); max DD -27.9 / -21.3; numeric columns blank because outcome is a multiple
compounders_growth_core_3y_quality_fixed,1.04 years (start 2025-09-30),,,,,,,nothing; fixed 0.82x vs KMI TR 0.96x; EW 0.88x; placebo median 0.86x (pctile 35); numeric columns blank because outcome is a multiple
compounders_growth_core_2y_fixed,2.04 years (start 2024-09-30),,,,,,,nothing; fixed 1.73x (+30.6%) vs KMI TR 1.81x (+33.6%); EW 1.50x; placebo median 1.88x (pctile 30); numeric columns blank because outcome is a multiple
compounders_growth_core_2y_quality_fixed,2.04 years (start 2024-09-30),,,,,,,nothing; fixed 1.71x vs KMI TR 1.81x; EW 1.50x; placebo median 1.91x (pctile 24); numeric columns blank because outcome is a multiple
compounders_growth_core_1y_fixed,3.05 years (start 2023-09-28),,,,,,,nothing; fixed 2.80x (+40.2%) vs KMI TR 2.87x (+41.2%); EW 2.19x; placebo median 2.80x (pctile 51); numeric columns blank because outcome is a multiple
compounders_growth_core_1y_quality_fixed,3.05 years (start 2023-09-28),,,,,,,nothing; fixed 2.82x vs KMI TR 2.87x; EW 2.19x; placebo median 2.69x (pctile 56); numeric columns blank because outcome is a multiple
=== END ===
