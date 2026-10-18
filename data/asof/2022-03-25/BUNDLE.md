# Replay bundle, close of 2022-03-25

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
# Market as of 2022-03-25 close (public information only)

- KSE100: 43,551 on 2022-03-25; 1m -3.5%, 3m -0.8%, 6m -3.8%, 12m -2.6%
- KMI All Share: 21,518 on 2022-03-25; 1m -3.7%, 3m -0.9%, 6m -1.8%, 12m -2.5%
- Policy rate 9.75%; last MPC decision 2022-03-08: hold (+0bp)
- 6M T-bill cutoff 12.50% (auction 2022-03-22); 3M 12.00%, 12M 12.70%
- CPI YoY 12.24% for 2022-02 (published by 2022-03-03); three months earlier (2021-11) 11.53%
- Brent: 122.67 USD/bbl on 2022-03-25; 3-month change +63.0%
- USD/PKR: 181.64  on 2022-03-25; 3-month change +2.1%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +2.75pp (market pricing hikes); CPI rising over 3 months (+0.7pp)
- Next MPC: see SBP calendar

Session date used: 2022-03-25. Liquid KMI names: 53 (membership KMI_ALL_derived_2022-01-03.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.1163,-0.1356,-0.3309,0,0
E&P,3,-0.0589,-0.0068,0.0576,0,0
OMC,4,-0.1127,-0.0977,-0.2033,0,0
Power,5,-0.0747,0.0342,0.0848,0,0
Fertilizer,4,0.0451,0.1202,0.1775,3,3
Cement,16,-0.0553,-0.0928,-0.1269,0,0
Steel & engineering,11,-0.0645,-0.1217,-0.2492,0,0
Autos,11,-0.0846,-0.1115,-0.2244,1,1
Tech & telecom,8,-0.1246,-0.0921,-0.1563,0,0
Islamic banks & fin.,8,-0.0163,-0.0225,-0.0673,0,0
Pharma,10,-0.0568,-0.0638,-0.1581,0,0
Textiles,22,-0.0711,0.0291,-0.0336,0,0
Food & staples,13,-0.0755,-0.0689,-0.1651,0,0
Chemicals,16,-0.0811,-0.0315,-0.1445,1,2
"Glass, packaging, paper",13,-0.0755,-0.0711,-0.1759,0,0
Gas utilities & misc,9,-0.0854,-0.0823,-0.2263,0,1

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AGHA,18.16,-0.175,-0.288,-0.349,-0.43,-0.495,1.13,0,,,2,1,0,0,,
ANL,11.3,-0.114,-0.084,-0.425,-0.652,-0.704,0.291,0,,,3,0,0,0,,
ASC,10.21,-0.232,-0.266,-0.299,-0.344,-0.509,0.408,0,2021-12-31,,2,0,0,0,,
ASL,12.78,-0.089,-0.101,-0.426,-0.458,-0.543,0.634,0,,,2,0,0,0,,
ATRL,120.54,-0.137,-0.116,-0.348,-0.417,-0.569,0.59,0,2021-12-31,,0,0,0,0,,
AVN,86.93,-0.131,-0.023,-0.3,0.16,-0.378,0.645,0,2021-09-30,,0,0,0,0,,
CHCC,135.94,-0.045,-0.029,-0.029,-0.183,-0.293,0.855,0,2021-12-31,,1,0,0,0,,
CNERGY,5.25,-0.077,-0.169,-0.33,-0.477,-0.597,0.425,0,,,1,0,0,0,,
DGKC,66.02,-0.132,-0.148,-0.234,-0.469,-0.496,1.046,0,2021-12-31,,0,0,0,0,,
EFERT,91.0,0.051,0.208,0.261,0.358,0.0,1.094,0,2021-12-31,,1,0,0,0,,
EPCL,62.71,0.094,0.284,0.278,0.648,0.0,0.864,0,2021-12-31,,0,0,0,0,,
FCCL,17.62,-0.022,-0.026,0.017,-0.233,-0.282,1.077,0,2021-09-30,,1,0,0,0,,
FCEPL,80.59,-0.036,-0.011,-0.223,0.085,-0.351,0.94,0,2021-09-30,,0,0,0,0,,
FLYNG,9.97,-0.079,-0.145,-0.296,-0.278,-0.588,1.232,0,,,2,1,0,0,,
GAL,59.99,-0.168,-0.216,-0.36,-0.416,-0.582,0.402,0,,,0,0,0,0,,
GGGL,10.4,-0.207,-0.269,-0.404,-0.296,-0.651,1.016,0,,,2,0,0,0,,
GGL,14.26,-0.285,-0.39,-0.592,-0.229,-0.681,0.887,0,2021-12-31,,2,0,0,0,,
GHNI,150.76,-0.117,-0.102,-0.263,-0.403,-0.524,0.544,0,2021-12-31,,1,1,0,0,,
HCAR,190.28,-0.109,-0.179,-0.259,-0.271,-0.515,0.513,0,2021-12-31,,0,0,0,0,,
HTL,39.59,-0.15,-0.057,-0.307,-0.422,-0.46,0.406,0,,,1,0,0,0,,
HUBC,68.77,-0.042,0.042,-0.003,0.006,-0.104,0.831,0,2021-12-31,,0,0,0,0,,
ILP,72.8,-0.061,0.023,0.013,0.022,-0.094,0.646,0,2021-12-31,,0,0,0,0,,
IMAGE,16.21,-0.03,-0.022,-0.27,,-0.467,1.124,0,2021-12-31,,2,0,0,0,,
INIL,112.95,-0.084,-0.182,-0.335,-0.448,-0.504,0.66,0,2021-12-31,,1,0,0,0,,
ISL,59.38,-0.072,-0.083,-0.245,-0.3,-0.408,0.567,0,2021-12-31,,1,0,0,0,,
KEL,2.91,-0.107,-0.102,-0.147,-0.294,-0.38,0.88,0,2021-12-31,-0.952,2,3,0,0,9.635,
KOHC,161.22,-0.108,-0.154,-0.048,-0.265,-0.312,0.66,0,2021-12-31,,1,0,0,0,,
LUCK,597.67,-0.102,-0.117,-0.174,-0.289,-0.365,0.612,0,2021-12-31,,0,1,0,0,,
MARI,1721.82,-0.036,0.074,0.117,0.096,-0.044,0.453,0,2021-12-31,,0,0,0,0,,
MEBL,128.95,-0.039,-0.034,-0.015,0.374,-0.15,0.988,0,2021-12-31,,1,0,0,0,,
MLCF,34.03,0.002,-0.014,-0.02,-0.246,-0.309,0.887,0,,,1,0,0,0,,
MTL,806.25,0.049,0.209,0.19,0.204,0.0,0.947,0,2021-12-31,,1,2,0,0,,
MUGHAL,84.87,-0.157,-0.149,0.041,0.063,-0.248,0.888,0,2021-12-31,,0,0,0,0,,
NETSOL,82.67,-0.163,-0.095,-0.317,-0.674,-0.671,0.711,0,2021-12-31,,1,0,0,0,,
NML,79.2,-0.062,0.011,-0.124,-0.211,-0.246,0.597,0,2021-12-31,,1,0,0,0,,
NRL,195.56,-0.193,-0.252,-0.369,-0.642,-0.689,0.707,0,2021-12-31,,0,0,0,0,,
OGDC,82.62,-0.05,-0.013,0.052,-0.108,-0.153,1.245,0,2021-12-31,,1,1,0,0,,
PAEL,15.02,-0.264,-0.304,-0.482,-0.544,-0.591,1.195,0,2021-09-30,,0,0,0,0,,
PIBTL,6.04,-0.125,-0.172,-0.321,-0.439,-0.497,1.302,0,2021-12-31,,2,0,0,0,,
PIOC,71.72,-0.104,-0.123,-0.201,-0.435,-0.473,0.782,0,2021-12-31,,1,0,0,0,,
PPL,72.42,-0.092,-0.081,-0.014,-0.164,-0.237,1.115,0,2021-12-31,,2,1,0,0,,
PSO,156.65,-0.13,-0.119,-0.215,-0.31,-0.356,0.958,0,2021-12-31,,1,0,0,0,,
PTC,7.53,-0.06,-0.104,-0.237,-0.101,-0.456,0.659,0,,,0,0,0,0,,
SAZEW,71.91,-0.184,-0.265,-0.397,-0.51,-0.534,0.438,0,2021-12-31,,0,0,0,0,,
SEARL,113.04,-0.169,-0.182,-0.314,-0.411,-0.433,0.626,0,2021-12-31,,2,0,0,0,,
SNGP,29.81,-0.144,-0.115,-0.368,-0.238,-0.47,0.818,0,2021-12-31,,0,0,0,0,2.805,0.144
SYS,706.01,0.038,-0.078,-0.068,0.629,-0.137,1.599,0,2021-12-31,,5,1,0,0,,
TELE,10.45,-0.319,-0.317,-0.399,0.416,-0.571,0.749,0,2021-06-30,,2,1,0,0,8.369,
TGL,123.02,-0.016,0.161,0.364,0.557,-0.054,1.118,0,2021-12-31,,2,0,0,0,,
TREET,30.51,-0.185,-0.241,-0.259,0.092,-0.504,0.986,0,2021-12-31,,2,0,0,0,,
UNITY,25.02,-0.086,-0.045,-0.242,-0.15,-0.493,0.71,0,2021-12-31,0.094,2,1,0,0,13.56,
WAFI,111.08,-0.086,-0.05,-0.2,-0.312,-0.401,0.718,0,,,0,0,0,0,,
WAVES,13.5,-0.096,-0.136,-0.312,-0.387,-0.505,0.294,0,2021-09-30,,0,0,0,0,,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2022-03-03,AGHA,material_info,Material Information-Approved Vendor for Suki Kinari Dam Project
2022-03-03,FRCL,material_info,MATERIAL INFORMATION
2022-03-04,YOUW,material_info,Material Information
2022-03-04,MTL,material_info,Material Information
2022-03-07,DMTX,material_info,Material Information
2022-03-07,JSMFETF,material_info,Material Information - Suspension of iNAV
2022-03-08,TPLT,material_info,Material Information
2022-03-08,JSBL,material_info,Material Information
2022-03-08,SPWL,material_info,Material Information
2022-03-09,JSMFETF,material_info,Material Information- Resumption of iNAV
2022-03-09,BIPL,material_info,Disclosure of Material Information
2022-03-10,AHL,material_info,Material Information Selling of 100% shareholding of Arif Habib Limited in 
2022-03-10,SRVI,material_info,Material Information
2022-03-10,SGF,material_info,Material Information
2022-03-10,TELE,material_info,Material Information
2022-03-10,REDCO,material_info,Material Information
2022-03-10,FFC,material_info,Material Information - Resignation of Director
2022-03-11,PREMA,material_info,Material Information - Precautionary Measurement
2022-03-11,TRG,material_info,Material Information
2022-03-11,LOTCHEM,material_info,Material Information
2022-03-11,AHTM,material_info,Material Information REVOKED
2022-03-11,KASBM,material_info,Material Information
2022-03-11,UNITY,material_info,Material Information
2022-03-11,PMI,material_info,Material Information
2022-03-11,AWWAL,material_info,Material Information
2022-03-11,PAKMI,material_info,Material Information
2022-03-11,SPWL,material_info,Material Information
2022-03-11,KEL,material_info,Material Information - MYT Mid-Term Review Petition REVOKED
2022-03-14,KEL,material_info,Material Information - MYT Determination
2022-03-14,SPWL,material_info,Material Information
2022-03-15,OBOY,material_info,MATERIAL INFORMATION
2022-03-17,FPJM,material_info,Material Information
2022-03-17,THALL,material_info,Material Information - Resignation of Director
2022-03-18,KOSM,material_info,Material Information
2022-03-18,AHTM,material_info,Material Information
2022-03-21,PPL,material_info,Material Information - Reconstitution of the Reko Diq Project
2022-03-21,OGDC,material_info,Material Information
2022-03-21,LUCK,material_info,Material Information
2022-03-21,OBOY,material_info,MATERIAL INFORMATION
2022-03-21,SSGC,material_info,DISCLOSURE OF MATERIAL INFORMATION
2022-03-21,GHNI,material_info,Material Information - Intimation of Sad demise of Director
2022-03-21,NCL,material_info,Material Information
2022-03-21,KEL,material_info,Material Information - First Sync of Unit 1 of 900 MW BQPS-III
2022-03-21,JDMT,material_info,Material Information - Intimation of Sad Demise of the Chairman of the Boar
2022-03-21,BNWM,material_info,Material Information
2022-03-21,MTL,material_info,Material Information
2022-03-21,UVIC,material_info,Material Information - Intimation of Sad Demise of Chairman of the Board of
2022-03-22,FLYNG,material_info,Material information
2022-03-24,NICL,material_info,The expansion of Soap Noodle Plant - Material Information
2022-03-24,TPLP,material_info,Material Information
2022-03-25,SYS,material_info,Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,4.825,2022-03-24
investor_type,last_5_sessions,broker proprietary trading,-0.042,2022-03-24
investor_type,last_5_sessions,companies,-0.78,2022-03-24
investor_type,last_5_sessions,foreign corporates,-8.912,2022-03-24
investor_type,last_5_sessions,foreign individual,0.041,2022-03-24
investor_type,last_5_sessions,individuals,0.869,2022-03-24
investor_type,last_5_sessions,insurance companies,2.724,2022-03-24
investor_type,last_5_sessions,mutual funds,-0.741,2022-03-24
investor_type,last_5_sessions,nbfc,0.093,2022-03-24
investor_type,last_5_sessions,other organization,0.722,2022-03-24
investor_type,last_5_sessions,overseas pakistani,1.202,2022-03-24
sector,last_5_sessions,fipi | All other Sectors,0.433,2022-03-24
sector,last_5_sessions,fipi | Cement,-0.151,2022-03-24
sector,last_5_sessions,fipi | Commercial Banks,-8.474,2022-03-24
sector,last_5_sessions,fipi | Fertilizer,1.702,2022-03-24
sector,last_5_sessions,fipi | Food and Personal Care Products,-0.132,2022-03-24
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-0.859,2022-03-24
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,-0.9,2022-03-24
sector,last_5_sessions,fipi | Power Generation and Distribution,0.177,2022-03-24
sector,last_5_sessions,fipi | Technology and Communication,0.543,2022-03-24
sector,last_5_sessions,fipi | Textile Composite,-0.009,2022-03-24
sector,last_5_sessions,lipi banks / dfi | All other Sectors,0.857,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Cement,0.068,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,3.676,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Debt Market,1.14,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-3.479,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-0.122,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.081,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.252,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.227,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,1.95,2022-03-24
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.174,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-0.912,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Cement,1.3,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,-0.181,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.192,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.161,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.076,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.207,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.033,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,-0.199,2022-03-24
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.179,2022-03-24
sector,last_5_sessions,lipi companies | All other Sectors,0.503,2022-03-24
sector,last_5_sessions,lipi companies | Cement,-0.847,2022-03-24
sector,last_5_sessions,lipi companies | Commercial Banks,1.165,2022-03-24
sector,last_5_sessions,lipi companies | Fertilizer,0.948,2022-03-24
sector,last_5_sessions,lipi companies | Food and Personal Care Products,0.036,2022-03-24
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,0.312,2022-03-24
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,-0.023,2022-03-24
sector,last_5_sessions,lipi companies | Power Generation and Distribution,0.156,2022-03-24
sector,last_5_sessions,lipi companies | Technology and Communication,-3.041,2022-03-24
sector,last_5_sessions,lipi companies | Textile Composite,0.012,2022-03-24
sector,last_5_sessions,lipi individuals | All other Sectors,-1.52,2022-03-24
sector,last_5_sessions,lipi individuals | Cement,-1.212,2022-03-24
sector,last_5_sessions,lipi individuals | Commercial Banks,1.379,2022-03-24
sector,last_5_sessions,lipi individuals | Fertilizer,-1.339,2022-03-24
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,0.334,2022-03-24
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,1.411,2022-03-24
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,1.016,2022-03-24
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.199,2022-03-24
sector,last_5_sessions,lipi individuals | Technology and Communication,0.617,2022-03-24
sector,last_5_sessions,lipi individuals | Textile Composite,-0.017,2022-03-24
sector,last_5_sessions,lipi insurance companies | All other Sectors,0.531,2022-03-24
sector,last_5_sessions,lipi insurance companies | Cement,0.459,2022-03-24
sector,last_5_sessions,lipi insurance companies | Commercial Banks,1.023,2022-03-24
sector,last_5_sessions,lipi insurance companies | Fertilizer,1.034,2022-03-24
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,-0.224,2022-03-24
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,0.056,2022-03-24
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.005,2022-03-24
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,-0.183,2022-03-24
sector,last_5_sessions,lipi insurance companies | Technology and Communication,0.087,2022-03-24
sector,last_5_sessions,lipi insurance companies | Textile Composite,-0.063,2022-03-24
sector,last_5_sessions,lipi mutual funds | All other Sectors,-0.342,2022-03-24
sector,last_5_sessions,lipi mutual funds | Cement,0.407,2022-03-24
sector,last_5_sessions,lipi mutual funds | Commercial Banks,1.265,2022-03-24
sector,last_5_sessions,lipi mutual funds | Debt Market,-1.14,2022-03-24
sector,last_5_sessions,lipi mutual funds | Fertilizer,1.004,2022-03-24
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,-0.127,2022-03-24
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-0.866,2022-03-24
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.514,2022-03-24
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.518,2022-03-24
sector,last_5_sessions,lipi mutual funds | Technology and Communication,0.008,2022-03-24
sector,last_5_sessions,lipi mutual funds | Textile Composite,0.083,2022-03-24
sector,last_5_sessions,lipi nbfc | All other Sectors,0.004,2022-03-24
sector,last_5_sessions,lipi nbfc | Cement,-0.0,2022-03-24
sector,last_5_sessions,lipi nbfc | Commercial Banks,0.084,2022-03-24
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.001,2022-03-24
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.0,2022-03-24
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.005,2022-03-24
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,0.0,2022-03-24
sector,last_5_sessions,lipi nbfc | Textile Composite,0.0,2022-03-24
sector,last_5_sessions,lipi other organization | All other Sectors,0.446,2022-03-24
sector,last_5_sessions,lipi other organization | Cement,-0.024,2022-03-24
sector,last_5_sessions,lipi other organization | Commercial Banks,0.064,2022-03-24
sector,last_5_sessions,lipi other organization | Fertilizer,-0.062,2022-03-24
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,0.396,2022-03-24
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.06,2022-03-24
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.047,2022-03-24
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,-0.025,2022-03-24
sector,last_5_sessions,lipi other organization | Technology and Communication,0.035,2022-03-24
sector,last_5_sessions,lipi other organization | Textile Composite,-0.001,2022-03-24
investor_type,last_20_sessions,banks / dfi,11.722,2022-03-24
investor_type,last_20_sessions,broker proprietary trading,-1.189,2022-03-24
investor_type,last_20_sessions,companies,14.522,2022-03-24
investor_type,last_20_sessions,foreign corporates,-22.891,2022-03-24
investor_type,last_20_sessions,foreign individual,-0.053,2022-03-24
investor_type,last_20_sessions,individuals,3.493,2022-03-24
investor_type,last_20_sessions,insurance companies,4.29,2022-03-24
investor_type,last_20_sessions,mutual funds,-20.443,2022-03-24
investor_type,last_20_sessions,nbfc,0.16,2022-03-24
investor_type,last_20_sessions,other organization,5.093,2022-03-24
investor_type,last_20_sessions,overseas pakistani,5.297,2022-03-24
sector,last_20_sessions,fipi | All other Sectors,0.648,2022-03-24
sector,last_20_sessions,fipi | Cement,-3.052,2022-03-24
sector,last_20_sessions,fipi | Commercial Banks,-16.948,2022-03-24
sector,last_20_sessions,fipi | Fertilizer,1.076,2022-03-24
sector,last_20_sessions,fipi | Food and Personal Care Products,-0.142,2022-03-24
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-0.177,2022-03-24
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,-2.159,2022-03-24
sector,last_20_sessions,fipi | Power Generation and Distribution,0.299,2022-03-24
sector,last_20_sessions,fipi | Technology and Communication,1.339,2022-03-24
sector,last_20_sessions,fipi | Textile Composite,1.47,2022-03-24
sector,last_20_sessions,lipi banks / dfi | All other Sectors,1.897,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Cement,0.778,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,3.512,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Debt Market,2.578,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-3.554,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,-0.057,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,-0.347,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,1.498,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,0.639,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,2.925,2022-03-24
sector,last_20_sessions,lipi banks / dfi | Textile Composite,1.854,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-1.5,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Cement,1.993,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,-0.7,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.065,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-3.203,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,2.429,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,1.232,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.734,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.013,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-1.73,2022-03-24
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.392,2022-03-24
sector,last_20_sessions,lipi companies | All other Sectors,2.985,2022-03-24
sector,last_20_sessions,lipi companies | Cement,1.132,2022-03-24
sector,last_20_sessions,lipi companies | Commercial Banks,6.082,2022-03-24
sector,last_20_sessions,lipi companies | Debt Market,-0.943,2022-03-24
sector,last_20_sessions,lipi companies | Fertilizer,3.78,2022-03-24
sector,last_20_sessions,lipi companies | Food and Personal Care Products,0.309,2022-03-24
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,4.029,2022-03-24
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,0.75,2022-03-24
sector,last_20_sessions,lipi companies | Power Generation and Distribution,0.834,2022-03-24
sector,last_20_sessions,lipi companies | Technology and Communication,-4.07,2022-03-24
sector,last_20_sessions,lipi companies | Textile Composite,-0.366,2022-03-24
sector,last_20_sessions,lipi individuals | All other Sectors,1.758,2022-03-24
sector,last_20_sessions,lipi individuals | Cement,-0.479,2022-03-24
sector,last_20_sessions,lipi individuals | Commercial Banks,2.46,2022-03-24
sector,last_20_sessions,lipi individuals | Debt Market,-0.002,2022-03-24
sector,last_20_sessions,lipi individuals | Fertilizer,1.169,2022-03-24
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,-1.239,2022-03-24
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,-6.364,2022-03-24
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,4.222,2022-03-24
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,-0.388,2022-03-24
sector,last_20_sessions,lipi individuals | Technology and Communication,4.327,2022-03-24
sector,last_20_sessions,lipi individuals | Textile Composite,-1.969,2022-03-24
sector,last_20_sessions,lipi insurance companies | All other Sectors,0.329,2022-03-24
sector,last_20_sessions,lipi insurance companies | Cement,1.555,2022-03-24
sector,last_20_sessions,lipi insurance companies | Commercial Banks,1.075,2022-03-24
sector,last_20_sessions,lipi insurance companies | Debt Market,0.779,2022-03-24
sector,last_20_sessions,lipi insurance companies | Fertilizer,1.231,2022-03-24
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,-1.197,2022-03-24
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-0.761,2022-03-24
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-0.504,2022-03-24
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,-0.38,2022-03-24
sector,last_20_sessions,lipi insurance companies | Technology and Communication,1.712,2022-03-24
sector,last_20_sessions,lipi insurance companies | Textile Composite,0.452,2022-03-24
sector,last_20_sessions,lipi mutual funds | All other Sectors,-9.672,2022-03-24
sector,last_20_sessions,lipi mutual funds | Cement,-2.487,2022-03-24
sector,last_20_sessions,lipi mutual funds | Commercial Banks,3.68,2022-03-24
sector,last_20_sessions,lipi mutual funds | Debt Market,-2.623,2022-03-24
sector,last_20_sessions,lipi mutual funds | Fertilizer,-1.042,2022-03-24
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,0.014,2022-03-24
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,0.857,2022-03-24
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-4.189,2022-03-24
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-1.099,2022-03-24
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-3.471,2022-03-24
sector,last_20_sessions,lipi mutual funds | Textile Composite,-0.411,2022-03-24
sector,last_20_sessions,lipi nbfc | All other Sectors,0.007,2022-03-24
sector,last_20_sessions,lipi nbfc | Cement,-0.029,2022-03-24
sector,last_20_sessions,lipi nbfc | Commercial Banks,0.141,2022-03-24
sector,last_20_sessions,lipi nbfc | Fertilizer,0.021,2022-03-24
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,-0.007,2022-03-24
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.018,2022-03-24
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.001,2022-03-24
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,-0.012,2022-03-24
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.016,2022-03-24
sector,last_20_sessions,lipi nbfc | Textile Composite,0.003,2022-03-24
sector,last_20_sessions,lipi other organization | All other Sectors,3.549,2022-03-24
sector,last_20_sessions,lipi other organization | Cement,0.591,2022-03-24
sector,last_20_sessions,lipi other organization | Commercial Banks,0.7,2022-03-24
sector,last_20_sessions,lipi other organization | Debt Market,0.275,2022-03-24
sector,last_20_sessions,lipi other organization | Fertilizer,0.523,2022-03-24
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-0.111,2022-03-24
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,1.514,2022-03-24
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.353,2022-03-24
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,0.096,2022-03-24
sector,last_20_sessions,lipi other organization | Technology and Communication,-1.049,2022-03-24
sector,last_20_sessions,lipi other organization | Textile Composite,-0.641,2022-03-24

=== FILE: calendar.md ===
# Calendar as of 2022-03-25

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2022-02-28 CNERGY: Board Meeting Other Than Financial Results
- 2022-02-28 ASC: Board Meeting
- 2022-03-08 CNERGY: Board Meeting other than Financial Results
- 2022-03-09 CNERGY: Board Meeting other than Financial Results - Disclosure
- 2022-03-14 HCAR: Board Meeting Other Than Financial Results
- 2022-03-14 EFERT: Board Meeting Other Than Financial Results
- 2022-03-15 EPCL: BOARD MEETING (OTHER THAN FINANCIAL RESULTS)
- 2022-03-22 EFERT: Board Meeting other than financial Results
- 2022-03-22 HCAR: Board Meeting Other Than Financial Results
- 2022-03-22 PAEL: Board Meeting for the Year ended December 31, 2021
- 2022-03-24 EPCL: BOARD MEETING (OTHER THAN FINANCIAL RESULTS)
- 2022-03-24 AVN: Board Meeting
- 2022-03-25 NETSOL: Board Meeting Other Than Financial Results

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
