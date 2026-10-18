# Replay bundle, close of 2023-01-06

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
# Market as of 2023-01-06 close (public information only)

- KSE100: 41,008 on 2023-01-06; 1m -1.5%, 3m -2.9%, 6m -0.4%, 12m -8.6%
- KMI All Share: 20,035 on 2023-01-06; 1m -1.2%, 3m -5.1%, 6m -3.1%, 12m -9.5%
- Policy rate 16.0%; last MPC decision 2022-11-25: hike (+100bp)
- 6M T-bill cutoff 16.83% (auction 2022-12-28); 3M 17.00%, 12M 16.85%
- CPI YoY 24.5% for 2022-12 (published by 2023-01-03); three months earlier (2022-09) 23.14%
- Brent: 76.41 USD/bbl on 2023-01-06; 3-month change -20.1%
- USD/PKR: 227.09  on 2023-01-06; 3-month change +2.2%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.83pp (market pricing hikes); CPI rising over 3 months (+1.4pp)
- Next MPC: see SBP calendar

Session date used: 2023-01-06. Liquid KMI names: 47 (membership KMI_ALL_derived_2022-07-15.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.0659,-0.1399,-0.168,0,0
E&P,3,0.1404,0.1244,0.0522,0,0
OMC,4,-0.0596,-0.1696,-0.1742,0,0
Power,4,-0.0448,-0.0084,0.0542,0,0
Fertilizer,4,-0.0135,0.0015,-0.0345,0,0
Cement,16,-0.0598,-0.1928,-0.0297,0,0
Steel & engineering,11,-0.0787,-0.1817,-0.2192,0,0
Autos,12,-0.1006,-0.1827,-0.1931,0,0
Tech & telecom,8,-0.0989,-0.1185,-0.0571,0,0
Islamic banks & fin.,8,-0.0846,-0.0731,-0.0579,0,0
Pharma,11,-0.0561,-0.1797,-0.2754,0,0
Textiles,21,-0.068,-0.0514,-0.0828,0,0
Food & staples,13,-0.0606,-0.1279,-0.0753,0,0
Chemicals,18,-0.0527,-0.1054,-0.119,0,0
"Glass, packaging, paper",13,-0.0942,-0.1684,-0.1598,0,0
Gas utilities & misc,10,0.0071,0.0011,-0.0011,0,1

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AIRLINK,25.99,-0.048,-0.275,-0.342,-0.561,-0.586,1.724,0,2022-09-30,-0.167,0,0,0,0,10.434,0.025
ATRL,161.87,0.022,0.052,-0.006,0.129,-0.098,0.673,0,2022-09-30,50.846,0,2,0,0,1.447,0.057
AVN,71.22,-0.06,-0.106,-0.08,-0.076,-0.208,0.588,0,2022-09-30,3.333,0,1,0,0,,
BIPL,13.21,-0.101,0.198,0.111,0.024,-0.146,1.129,0,2022-09-30,1.032,0,0,0,0,,
CHCC,99.99,-0.023,-0.206,0.136,-0.334,-0.354,0.588,0,2022-09-30,0.243,0,0,0,0,4.057,0.032
CNERGY,4.05,-0.084,-0.185,-0.232,-0.391,-0.446,0.742,0,,,0,1,0,0,5.945,
DCL,5.09,-0.118,-0.068,-0.049,-0.335,-0.347,1.0,1,,,0,0,0,0,,
DGKC,47.7,-0.016,-0.232,-0.172,-0.431,-0.438,0.988,0,2022-09-30,-0.588,0,0,0,0,8.664,0.016
EFERT,80.05,-0.018,-0.007,-0.097,0.047,-0.208,0.75,0,2022-09-30,-0.052,0,2,0,0,4.817,0.217
EPCL,44.73,-0.097,-0.214,-0.352,0.027,-0.455,0.693,0,2022-09-30,-0.272,0,0,0,0,3.33,0.301
FCCL,11.37,-0.103,-0.287,-0.171,-0.389,-0.404,0.815,0,2021-09-30,,0,1,0,0,2.749,
GGGL,7.06,-0.164,-0.308,-0.352,-0.522,-0.548,0.627,0,,,0,0,0,0,,
GGL,11.24,-0.188,-0.318,-0.32,-0.543,-0.55,0.591,0,2022-09-30,-0.58,0,0,0,0,8.853,
GHNI,100.38,-0.201,-0.336,-0.353,-0.437,-0.477,0.827,0,2022-09-30,-0.824,0,0,0,0,9.239,
HCAR,139.07,-0.069,-0.243,-0.236,-0.404,-0.425,2.162,0,2022-09-30,-1.41,0,0,0,0,11.79,0.034
HUBC,61.38,-0.068,-0.036,0.115,0.158,-0.123,1.052,0,2022-09-30,0.226,0,2,0,0,3.106,0.095
INIL,74.3,-0.105,-0.28,-0.263,-0.491,-0.503,1.644,0,2022-09-30,-0.592,0,0,0,0,5.642,0.077
ISL,44.15,0.004,-0.21,-0.218,-0.379,-0.399,1.04,0,2022-09-30,-0.832,0,0,0,0,4.771,0.11
KEL,2.36,-0.078,-0.205,-0.175,-0.289,-0.367,0.963,0,2022-09-30,-6.364,0,0,0,0,9.912,
KOHC,137.4,-0.124,-0.166,0.07,-0.27,-0.275,0.84,0,2022-09-30,0.281,0,0,0,0,5.202,
LUCK,433.11,-0.042,-0.158,-0.009,-0.372,-0.382,0.467,0,2022-09-30,-0.18,0,2,0,0,5.032,
MARI,1528.33,-0.079,-0.05,-0.119,-0.079,-0.151,0.985,0,2022-09-30,0.397,0,1,0,0,7.019,0.071
MEBL,96.43,-0.082,-0.092,-0.05,-0.165,-0.246,1.093,0,2022-09-30,0.648,0,0,0,0,7.73,0.042
MLCF,21.76,-0.084,-0.253,-0.155,-0.404,-0.434,0.903,0,,,0,0,0,0,6.598,
MTL,485.9,-0.179,-0.412,-0.444,-0.161,-0.466,1.294,0,2022-09-30,-0.622,0,4,0,0,15.755,0.074
MUGHAL,46.5,-0.149,-0.336,-0.177,-0.561,-0.588,0.743,0,2022-09-30,-0.483,0,0,0,0,3.575,0.052
NML,51.52,-0.094,-0.249,-0.286,-0.357,-0.468,1.326,0,2022-09-30,-0.025,0,0,0,0,2.112,0.054
NRL,184.85,-0.073,-0.203,-0.236,-0.355,-0.39,0.716,0,2022-09-30,-11.811,0,0,0,0,2.225,0.059
OCTOPUS,61.61,-0.072,-0.082,-0.12,-0.263,-0.444,0.5,0,,,0,0,0,0,,
OGDC,82.31,0.156,0.142,0.127,0.039,-0.05,1.377,0,2022-09-30,0.584,0,0,0,0,2.529,0.092
PABC,41.05,-0.009,-0.047,0.282,0.203,-0.115,0.53,0,,,0,0,0,0,,
PAEL,12.17,-0.197,-0.303,-0.22,-0.457,-0.494,0.9,0,2022-09-30,-0.27,0,0,0,0,7.238,
PIBTL,4.44,-0.088,-0.218,-0.252,-0.423,-0.434,1.226,0,2022-09-30,,0,0,0,0,,
PIOC,49.96,-0.082,-0.342,-0.16,-0.451,-0.461,0.526,0,2022-06-30,,0,0,0,0,13.048,
PPL,76.05,0.382,0.294,0.15,-0.037,-0.131,2.419,2,2022-09-30,0.561,0,1,0,0,3.38,0.03
PSO,145.03,-0.011,-0.13,-0.144,-0.206,-0.263,1.054,0,2022-09-30,-0.851,0,0,0,0,0.884,0.058
SEARL,56.53,-0.122,-0.319,-0.33,-0.506,-0.52,1.92,0,2022-09-30,-0.711,0,0,0,0,14.467,
SNGP,41.51,0.092,0.305,0.312,0.405,-0.002,1.244,1,2022-09-30,-0.151,0,0,0,0,2.093,0.117
SSGC,10.76,0.073,0.086,0.221,0.157,-0.08,1.568,1,2021-06-30,,1,0,0,0,,
SYS,496.83,0.024,0.184,0.498,0.288,-0.035,0.886,0,2022-09-30,1.053,1,0,0,0,23.513,0.007
TELE,6.76,-0.235,-0.419,-0.371,-0.583,-0.637,0.52,0,2021-06-30,,0,0,0,0,8.192,
TGL,67.22,-0.158,-0.263,-0.198,-0.269,-0.385,0.579,0,2022-09-30,-0.694,0,0,0,0,3.453,0.019
TOMCL,20.54,-0.091,-0.147,-0.058,-0.354,-0.379,0.462,0,2022-09-30,0.333,0,1,0,0,6.529,
TREET,17.17,-0.177,-0.278,-0.402,-0.593,-0.604,0.544,0,2022-09-30,-1.098,0,0,0,0,,
UNITY,14.14,-0.145,-0.408,-0.29,-0.467,-0.564,0.491,0,2022-03-31,-0.395,0,0,0,0,10.986,
WAFI,106.54,-0.119,-0.195,-0.119,-0.116,-0.24,0.283,0,,,0,0,0,0,5.807,
WAVES,8.73,-0.047,-0.274,-0.313,-0.445,-0.479,0.807,0,2022-09-30,-0.526,0,0,0,0,13.769,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2022-12-12,DLL,material_info,Material Information
2022-12-12,TPLP,material_info,Material Information
2022-12-12,FRCL,material_info,MATERIAL INFORMATION SHUT DOWN OF FLOOR TILE PRODUCTION PLANT
2022-12-12,SMBL,material_info,Disclosure of Material Information
2022-12-13,ATRL,material_info,Disclosure of Material Information
2022-12-13,SMBL,material_info,SMBL | Summit Bank Limited - Material Information Disclosure
2022-12-14,KOSM,material_info,Material Information
2022-12-15,ENGRO,material_info,Material Information
2022-12-15,WHALE,material_info,Material Information Upgradation/Assignment of Ratings Waves Home Appliance
2022-12-15,FATIMA,material_info,Disclosure of Material Information
2022-12-15,MTL,material_info,Material Information REVOKED
2022-12-15,MTL,material_info,Material Information
2022-12-16,PPL,material_info,Material Information - Signing of Definitive Agreements - Reko Diq Project
2022-12-19,AKDHL,material_info,Material Information
2022-12-19,TOMCL,material_info,Material Information
2022-12-19,RPL,material_info,Material Information
2022-12-19,INDU,material_info,Material Information
2022-12-20,TPLP,material_info,Material Information
2022-12-21,DOL,material_info,Material Information
2022-12-21,KSTM,material_info,Material Information
2022-12-21,DOL,material_info,Material Information
2022-12-21,MTL,material_info,Material Information
2022-12-21,MQTM,material_info,Material Information
2022-12-22,FFBL,material_info,Disclosure of Material Information
2022-12-22,LUCK,material_info,Material Information
2022-12-22,CLVL,material_info,Material Information
2022-12-23,HUBC,material_info,HUBC | The Hub Power Company Limited - Disclosure of Material Information
2022-12-23,BWHL,material_info,Material Information
2022-12-23,FCCL,material_info,Material Information
2022-12-23,ICI,material_info,Material Information
2022-12-26,ATRL,material_info,Disclosure of Material Information
2022-12-28,NCL,material_info,Material Information
2022-12-28,ZIL,material_info,Material Information
2022-12-29,EFERT,material_info,Material Information
2022-12-30,LUCK,material_info,Material Information
2022-12-30,BWHL,material_info,Material Information
2022-12-30,AGIC,material_info,Material Information
2022-12-30,SURC,material_info,Material Information
2022-12-30,HUBC,material_info,Disclosure of Material Information
2022-12-30,FABL,material_info,Disclosure of Material Information - Faysal Bank Limited
2022-12-30,SRVI,material_info,Material Information
2022-12-30,GRR,material_info,DISCLOSURE OF MATERIAL INFORMATION
2023-01-02,KSBP,material_info,Material Information
2023-01-02,NCPL,material_info,Material Information
2023-01-03,CFL,material_info,MATERIAL INFORMATION
2023-01-03,DAWH,material_info,Material Information
2023-01-03,AVN,material_info,Material Information
2023-01-04,PNSC,material_info,Material Information
2023-01-04,CNERGY,material_info,Disclosure of Material Information
2023-01-04,AGL,material_info,Disclosure of Material Information
2023-01-05,MTL,material_info,Material Information
2023-01-06,JKSM,material_info,Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,5.886,2023-01-05
investor_type,last_5_sessions,broker proprietary trading,0.547,2023-01-05
investor_type,last_5_sessions,companies,2.401,2023-01-05
investor_type,last_5_sessions,foreign corporates,0.147,2023-01-05
investor_type,last_5_sessions,foreign individual,0.026,2023-01-05
investor_type,last_5_sessions,individuals,-5.557,2023-01-05
investor_type,last_5_sessions,insurance companies,-1.098,2023-01-05
investor_type,last_5_sessions,mutual funds,-1.711,2023-01-05
investor_type,last_5_sessions,nbfc,0.013,2023-01-05
investor_type,last_5_sessions,other organization,0.317,2023-01-05
investor_type,last_5_sessions,overseas pakistani,-0.971,2023-01-05
sector,last_5_sessions,fipi | All other Sectors,-0.593,2023-01-05
sector,last_5_sessions,fipi | Cement,0.266,2023-01-05
sector,last_5_sessions,fipi | Commercial Banks,-0.954,2023-01-05
sector,last_5_sessions,fipi | Fertilizer,0.016,2023-01-05
sector,last_5_sessions,fipi | Food and Personal Care Products,0.077,2023-01-05
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,0.019,2023-01-05
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,0.087,2023-01-05
sector,last_5_sessions,fipi | Power Generation and Distribution,0.288,2023-01-05
sector,last_5_sessions,fipi | Technology and Communication,0.248,2023-01-05
sector,last_5_sessions,fipi | Textile Composite,-0.251,2023-01-05
sector,last_5_sessions,lipi banks / dfi | All other Sectors,1.981,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Cement,0.857,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,1.281,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-0.045,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-0.004,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.449,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.01,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.903,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,0.088,2023-01-05
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.365,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-0.204,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Cement,-0.159,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.078,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.398,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.033,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.668,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.062,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.152,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,-0.091,2023-01-05
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.021,2023-01-05
sector,last_5_sessions,lipi companies | All other Sectors,0.473,2023-01-05
sector,last_5_sessions,lipi companies | Cement,0.252,2023-01-05
sector,last_5_sessions,lipi companies | Commercial Banks,0.314,2023-01-05
sector,last_5_sessions,lipi companies | Fertilizer,-0.002,2023-01-05
sector,last_5_sessions,lipi companies | Food and Personal Care Products,0.069,2023-01-05
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,1.809,2023-01-05
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,-0.3,2023-01-05
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.058,2023-01-05
sector,last_5_sessions,lipi companies | Technology and Communication,-0.029,2023-01-05
sector,last_5_sessions,lipi companies | Textile Composite,-0.125,2023-01-05
sector,last_5_sessions,lipi individuals | All other Sectors,-0.518,2023-01-05
sector,last_5_sessions,lipi individuals | Cement,0.066,2023-01-05
sector,last_5_sessions,lipi individuals | Commercial Banks,-0.596,2023-01-05
sector,last_5_sessions,lipi individuals | Fertilizer,-0.819,2023-01-05
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,-0.116,2023-01-05
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,-3.472,2023-01-05
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.036,2023-01-05
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.331,2023-01-05
sector,last_5_sessions,lipi individuals | Technology and Communication,-0.454,2023-01-05
sector,last_5_sessions,lipi individuals | Textile Composite,0.057,2023-01-05
sector,last_5_sessions,lipi insurance companies | All other Sectors,0.087,2023-01-05
sector,last_5_sessions,lipi insurance companies | Cement,0.075,2023-01-05
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-0.069,2023-01-05
sector,last_5_sessions,lipi insurance companies | Fertilizer,-0.23,2023-01-05
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.031,2023-01-05
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-1.122,2023-01-05
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.021,2023-01-05
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,-0.002,2023-01-05
sector,last_5_sessions,lipi insurance companies | Technology and Communication,0.094,2023-01-05
sector,last_5_sessions,lipi insurance companies | Textile Composite,0.016,2023-01-05
sector,last_5_sessions,lipi mutual funds | All other Sectors,-1.26,2023-01-05
sector,last_5_sessions,lipi mutual funds | Cement,-1.285,2023-01-05
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-0.182,2023-01-05
sector,last_5_sessions,lipi mutual funds | Fertilizer,0.711,2023-01-05
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,-0.018,2023-01-05
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,1.494,2023-01-05
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.1,2023-01-05
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-1.368,2023-01-05
sector,last_5_sessions,lipi mutual funds | Technology and Communication,0.116,2023-01-05
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.019,2023-01-05
sector,last_5_sessions,lipi nbfc | All other Sectors,-0.0,2023-01-05
sector,last_5_sessions,lipi nbfc | Cement,-0.01,2023-01-05
sector,last_5_sessions,lipi nbfc | Commercial Banks,0.008,2023-01-05
sector,last_5_sessions,lipi nbfc | Fertilizer,0.002,2023-01-05
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,0.001,2023-01-05
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.003,2023-01-05
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.001,2023-01-05
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,0.002,2023-01-05
sector,last_5_sessions,lipi nbfc | Technology and Communication,0.009,2023-01-05
sector,last_5_sessions,lipi nbfc | Textile Composite,0.0,2023-01-05
sector,last_5_sessions,lipi other organization | All other Sectors,0.035,2023-01-05
sector,last_5_sessions,lipi other organization | Cement,-0.063,2023-01-05
sector,last_5_sessions,lipi other organization | Commercial Banks,0.12,2023-01-05
sector,last_5_sessions,lipi other organization | Fertilizer,-0.03,2023-01-05
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,-0.007,2023-01-05
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,0.152,2023-01-05
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.057,2023-01-05
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.057,2023-01-05
sector,last_5_sessions,lipi other organization | Technology and Communication,0.018,2023-01-05
sector,last_5_sessions,lipi other organization | Textile Composite,-0.022,2023-01-05
investor_type,last_20_sessions,banks / dfi,44.291,2023-01-05
investor_type,last_20_sessions,broker proprietary trading,-4.264,2023-01-05
investor_type,last_20_sessions,companies,16.429,2023-01-05
investor_type,last_20_sessions,foreign corporates,-59.694,2023-01-05
investor_type,last_20_sessions,foreign individual,0.205,2023-01-05
investor_type,last_20_sessions,individuals,-8.007,2023-01-05
investor_type,last_20_sessions,insurance companies,-4.671,2023-01-05
investor_type,last_20_sessions,mutual funds,-11.022,2023-01-05
investor_type,last_20_sessions,nbfc,-0.407,2023-01-05
investor_type,last_20_sessions,other organization,5.227,2023-01-05
investor_type,last_20_sessions,overseas pakistani,21.914,2023-01-05
sector,last_20_sessions,fipi | All other Sectors,0.565,2023-01-05
sector,last_20_sessions,fipi | Cement,-0.379,2023-01-05
sector,last_20_sessions,fipi | Commercial Banks,-40.671,2023-01-05
sector,last_20_sessions,fipi | Fertilizer,-0.864,2023-01-05
sector,last_20_sessions,fipi | Food and Personal Care Products,0.014,2023-01-05
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,0.21,2023-01-05
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,0.096,2023-01-05
sector,last_20_sessions,fipi | Power Generation and Distribution,0.902,2023-01-05
sector,last_20_sessions,fipi | Technology and Communication,1.882,2023-01-05
sector,last_20_sessions,fipi | Textile Composite,0.67,2023-01-05
sector,last_20_sessions,lipi banks / dfi | All other Sectors,5.527,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Cement,4.049,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,31.707,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Debt Market,-0.38,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Fertilizer,1.864,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.034,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,-0.488,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.266,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,1.454,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,0.154,2023-01-05
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.103,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,1.948,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Cement,-0.886,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,-0.056,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.51,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,1.422,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.142,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.531,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-3.872,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.516,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-1.099,2023-01-05
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.021,2023-01-05
sector,last_20_sessions,lipi companies | All other Sectors,-0.222,2023-01-05
sector,last_20_sessions,lipi companies | Cement,2.833,2023-01-05
sector,last_20_sessions,lipi companies | Commercial Banks,4.972,2023-01-05
sector,last_20_sessions,lipi companies | Debt Market,-0.999,2023-01-05
sector,last_20_sessions,lipi companies | Fertilizer,1.216,2023-01-05
sector,last_20_sessions,lipi companies | Food and Personal Care Products,0.239,2023-01-05
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,2.672,2023-01-05
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,3.589,2023-01-05
sector,last_20_sessions,lipi companies | Power Generation and Distribution,0.852,2023-01-05
sector,last_20_sessions,lipi companies | Technology and Communication,1.538,2023-01-05
sector,last_20_sessions,lipi companies | Textile Composite,-0.261,2023-01-05
sector,last_20_sessions,lipi individuals | All other Sectors,-2.951,2023-01-05
sector,last_20_sessions,lipi individuals | Cement,-2.134,2023-01-05
sector,last_20_sessions,lipi individuals | Commercial Banks,7.343,2023-01-05
sector,last_20_sessions,lipi individuals | Debt Market,-0.002,2023-01-05
sector,last_20_sessions,lipi individuals | Fertilizer,-2.174,2023-01-05
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,-2.151,2023-01-05
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,-5.235,2023-01-05
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.363,2023-01-05
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,1.287,2023-01-05
sector,last_20_sessions,lipi individuals | Technology and Communication,-2.339,2023-01-05
sector,last_20_sessions,lipi individuals | Textile Composite,0.711,2023-01-05
sector,last_20_sessions,lipi insurance companies | All other Sectors,-0.405,2023-01-05
sector,last_20_sessions,lipi insurance companies | Cement,-0.03,2023-01-05
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-0.599,2023-01-05
sector,last_20_sessions,lipi insurance companies | Debt Market,0.185,2023-01-05
sector,last_20_sessions,lipi insurance companies | Fertilizer,-1.181,2023-01-05
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,0.144,2023-01-05
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-2.35,2023-01-05
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-0.173,2023-01-05
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,-0.173,2023-01-05
sector,last_20_sessions,lipi insurance companies | Technology and Communication,0.127,2023-01-05
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.214,2023-01-05
sector,last_20_sessions,lipi mutual funds | All other Sectors,-3.592,2023-01-05
sector,last_20_sessions,lipi mutual funds | Cement,-3.75,2023-01-05
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-3.003,2023-01-05
sector,last_20_sessions,lipi mutual funds | Debt Market,-0.397,2023-01-05
sector,last_20_sessions,lipi mutual funds | Fertilizer,-0.289,2023-01-05
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,-0.345,2023-01-05
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,5.281,2023-01-05
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.449,2023-01-05
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-4.234,2023-01-05
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-0.269,2023-01-05
sector,last_20_sessions,lipi mutual funds | Textile Composite,-0.874,2023-01-05
sector,last_20_sessions,lipi nbfc | All other Sectors,-0.368,2023-01-05
sector,last_20_sessions,lipi nbfc | Cement,-0.007,2023-01-05
sector,last_20_sessions,lipi nbfc | Commercial Banks,0.012,2023-01-05
sector,last_20_sessions,lipi nbfc | Fertilizer,-0.041,2023-01-05
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.001,2023-01-05
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.029,2023-01-05
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.0,2023-01-05
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.021,2023-01-05
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.006,2023-01-05
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.002,2023-01-05
sector,last_20_sessions,lipi other organization | All other Sectors,-0.501,2023-01-05
sector,last_20_sessions,lipi other organization | Cement,0.304,2023-01-05
sector,last_20_sessions,lipi other organization | Commercial Banks,0.295,2023-01-05
sector,last_20_sessions,lipi other organization | Debt Market,2.102,2023-01-05
sector,last_20_sessions,lipi other organization | Fertilizer,0.045,2023-01-05
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,2.205,2023-01-05
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,0.47,2023-01-05
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,0.009,2023-01-05
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,0.406,2023-01-05
sector,last_20_sessions,lipi other organization | Technology and Communication,0.001,2023-01-05
sector,last_20_sessions,lipi other organization | Textile Composite,-0.111,2023-01-05

=== FILE: calendar.md ===
# Calendar as of 2023-01-06

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2022-12-14 BIPL: Board Meeting other than Financial Results
- 2022-12-15 SSGC: Board Meeting Other Than Financial Results
- 2022-12-22 KEL: Board Meeting Other Than Financial Results
- 2022-12-23 SSGC: BOARD MEETING OTHER THAN FINANCIAL RESULTS - POSTPONED
- 2022-12-23 SSGC: BOARD MEETING OTHER THAN FINANCIAL RESULTS (RESCHEDULED)
- 2022-12-26 KEL: Board Meeting Other Than Financial Results
- 2022-12-28 SSGC: BOARD MEETING OTHER THAN FINANCIAL RESULTS RESCHEDULED
- 2022-12-29 SSGC: Board Meeting
- 2023-01-05 SSGC: Board Meeting Rescheduled

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
| 17 | GIDC recovery | SC Aug 2020 | outcome not shown |
| 19 | Exporter power tariff Rs19.99 | 6 Oct 2022 | outcome not shown |

=== FILE: situations.md ===
2020-01-13 (outcome_end) | 01_2019_bottom_imf_programme.md | Regime bottom: the IMF approval was not the low. The second signal (Sep 2019 rate hold, stable rupee) returned +35% to the January 2020 peak. Lesson: wait for it, not the headline.
2021-06-14 (outcome_end) | 02_2020_covid_crash_rate_cut_rebound.md | Shock with a policy backstop: the first rate cut came before the March 2020 low, the rebound was +79% from the low by June 2021. Lesson: enter a third, add on confirmation, favour USD earners.
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
