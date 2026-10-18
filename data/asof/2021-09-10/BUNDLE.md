# Replay bundle, close of 2021-09-10

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
# Market as of 2021-09-10 close (public information only)

- KSE100: 47,198 on 2021-09-10; 1m +0.1%, 3m -2.0%, 6m +2.7%, 12m +12.8%
- KMI All Share: 23,382 on 2021-09-10; 1m +1.1%, 3m -1.3%, 6m +2.2%, 12m +12.4%
- Policy rate 7.0%; last MPC decision 2021-07-27: hold (+0bp)
- 6M T-bill cutoff 7.49% (auction 2021-09-08); 3M 7.23%, 12M 7.60%
- CPI YoY 8.34% for 2021-08 (published by 2021-09-03); three months earlier (2021-05) 10.84%
- Brent: 72.44 USD/bbl on 2021-09-10; 3-month change +1.1%
- USD/PKR: 167.58  on 2021-09-10; 3-month change +7.8%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.49pp (market near policy rate); CPI falling over 3 months (-2.5pp)
- Next MPC: see SBP calendar

Session date used: 2021-09-10. Liquid KMI names: 68 (membership KMI_ALL_derived_2021-07-05.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.0182,-0.1291,-0.1183,0,0
E&P,3,-0.0105,-0.0772,-0.0915,0,0
OMC,4,-0.0512,-0.0795,-0.0967,0,0
Power,5,0.0229,-0.0578,-0.0346,0,1
Fertilizer,4,0.0029,0.0031,0.0238,0,0
Cement,16,-0.0321,-0.096,-0.0178,0,0
Steel & engineering,11,0.0009,0.0244,0.0572,0,0
Autos,12,-0.058,-0.0041,0.0369,0,0
Tech & telecom,6,0.168,0.2029,0.224,2,3
Islamic banks & fin.,8,0.0517,0.0942,0.0646,2,2
Pharma,12,-0.032,-0.0057,0.0543,0,1
Textiles,22,-0.011,0.1416,0.1327,0,2
Food & staples,14,0.018,0.1667,0.3352,1,1
Chemicals,17,0.0939,0.1615,0.3301,1,1
"Glass, packaging, paper",12,-0.0263,-0.0332,0.0839,0,1
Gas utilities & misc,10,0.0379,0.0269,0.172,1,1

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ABOT,792.33,0.036,0.027,0.063,0.029,-0.01,1.58,0,,,2,0,0,0,,
AGHA,29.77,-0.077,-0.128,-0.149,,-0.282,0.447,0,,,0,1,0,0,,
AGP,133.06,0.082,0.27,0.086,0.112,-0.136,0.984,1,,,2,0,0,0,,
ASC,17.57,-0.067,0.059,0.228,0.318,-0.155,0.689,0,,,0,0,0,0,,
ASL,24.29,0.01,-0.106,-0.046,0.613,-0.132,0.539,0,,,0,0,0,0,,
ATBA,333.92,0.008,0.223,0.21,0.459,-0.187,0.8,0,,,2,0,0,0,,
ATRL,235.85,0.041,-0.048,0.018,0.418,-0.156,0.33,0,,,1,0,0,0,,
AVN,138.72,0.146,0.586,0.742,1.695,-0.008,1.22,1,,,2,4,0,0,,
BGL,15.58,-0.03,0.02,0.835,1.21,-0.114,0.734,0,,,0,0,0,0,,
CEPB,113.48,-0.004,-0.061,0.008,0.266,-0.135,0.835,0,,,1,0,0,0,,
CHCC,162.48,-0.019,-0.139,-0.083,0.156,-0.155,0.902,0,,,1,0,0,0,,
DCL,11.08,0.072,-0.03,-0.109,0.02,-0.191,0.855,0,,,0,0,0,0,,
DGKC,101.6,-0.045,-0.223,-0.249,-0.128,-0.282,0.711,0,,,0,1,0,0,,
DOL,24.07,-0.063,-0.197,-0.134,-0.236,-0.403,0.533,0,,,1,0,0,0,,
EFERT,74.06,-0.042,0.076,0.133,0.124,-0.049,0.76,0,,,1,0,0,0,,
EPCL,56.11,0.116,0.295,0.281,0.674,-0.024,1.044,0,,,1,0,0,0,,
FCCL,19.04,-0.117,-0.204,-0.228,-0.143,-0.3,0.56,0,,,2,0,0,0,,
FCEPL,108.23,-0.012,0.257,0.524,0.215,-0.129,1.12,0,,,2,0,0,0,,
FEROZ,390.53,-0.047,0.036,0.16,0.152,-0.06,0.674,0,,,2,0,0,0,,
FLYNG,18.09,-0.09,-0.101,0.554,0.876,-0.253,0.887,0,,,0,0,0,0,,
GAL,116.81,-0.063,0.051,0.025,0.007,-0.185,0.493,0,,,0,0,0,0,,
GGL,44.74,0.054,0.001,1.708,2.054,-0.13,1.379,2,,,1,0,0,0,,
GHGL,50.06,0.04,-0.056,0.031,0.575,-0.118,1.239,0,,,1,0,0,0,,
GHNI,249.55,-0.102,-0.112,-0.139,-0.228,-0.265,0.29,0,,,0,0,0,0,,
GLAXO,153.63,-0.036,-0.068,-0.162,-0.162,-0.222,0.507,0,,,2,0,0,0,,
HCAR,293.6,-0.18,-0.245,0.001,-0.105,-0.252,0.525,0,,,0,0,0,0,,
HTL,77.88,-0.018,0.023,-0.022,0.92,-0.184,0.597,0,,,0,0,0,0,,
HUBC,79.23,0.063,-0.008,-0.048,-0.04,-0.1,1.092,0,,,1,0,0,0,,
ILP,75.71,0.023,0.068,-0.011,0.178,-0.011,0.428,0,,,0,0,0,0,,
IMAGE,25.76,0.028,0.299,,,,1.313,0,,,0,0,0,0,,
INIL,192.35,-0.099,-0.131,-0.057,0.305,-0.201,0.767,0,,,2,0,0,0,,
ISL,97.07,0.033,0.064,0.052,0.267,-0.033,0.947,0,,,2,0,0,0,,
JVDC,62.62,0.289,0.333,1.199,1.485,0.0,0.596,1,,,0,0,0,0,,
KEL,3.65,-0.042,-0.12,-0.114,-0.151,-0.222,0.319,0,2021-03-31,2.0,0,0,0,0,,
KOHC,191.43,-0.106,-0.102,-0.158,0.057,-0.224,0.223,0,,,1,0,0,0,,
LCI,809.92,-0.083,-0.105,-0.024,0.049,-0.12,0.86,0,,,0,0,0,0,,
LUCK,785.42,-0.092,-0.143,-0.106,0.276,-0.165,0.828,0,,,1,0,0,0,,
MARI,1550.94,0.039,-0.01,-0.013,0.052,-0.084,0.653,0,,,1,1,0,0,,
MEBL,146.69,0.262,0.507,0.597,1.139,0.0,1.702,1,,,2,1,0,0,,
MLCF,40.25,-0.082,-0.15,-0.139,0.07,-0.183,0.932,0,,,2,0,0,0,,
MTL,1089.22,-0.001,-0.007,0.021,0.496,-0.04,1.245,0,,,0,1,0,0,,
MUGHAL,114.8,0.082,0.013,-0.041,0.663,-0.041,0.683,0,,,0,0,0,0,,
NETSOL,165.87,0.094,-0.103,-0.437,1.517,-0.447,0.292,1,,,0,0,0,0,,
NML,95.99,-0.008,-0.045,-0.118,-0.137,-0.22,0.719,0,,,0,0,0,0,,
NRL,419.32,0.045,-0.23,-0.341,1.186,-0.346,0.3,0,,,0,0,0,0,,
OGDC,88.99,-0.034,-0.06,-0.125,-0.189,-0.204,0.397,0,,,0,0,0,0,,
PAEL,32.74,0.023,-0.071,-0.121,-0.126,-0.228,1.224,0,,,2,0,0,0,,
PIBTL,9.98,-0.073,-0.096,-0.158,-0.223,-0.286,0.329,0,,,2,0,0,0,,
POWER,8.48,-0.04,-0.166,-0.19,-0.131,-0.281,0.623,0,,,0,0,0,0,,
PPL,78.16,-0.035,-0.16,-0.142,-0.227,-0.242,0.817,0,,,0,0,0,0,,
PREMA,29.88,-0.021,0.366,0.654,0.61,-0.04,0.888,1,,,0,0,0,0,,
PSO,214.17,-0.017,-0.092,-0.109,0.092,-0.174,0.785,0,,,1,0,0,0,,
SAZEW,161.78,-0.003,-0.105,-0.174,-0.13,-0.209,0.382,0,,,1,1,0,0,,
SEARL,227.12,-0.049,-0.097,-0.168,-0.152,-0.195,0.698,0,,,0,1,0,0,,
SNGP,44.86,-0.116,-0.023,0.092,-0.309,-0.34,0.408,0,,,0,2,0,0,,
STCL,32.82,-0.021,-0.028,0.215,1.471,-0.121,1.018,0,,,1,0,0,0,,
SYS,818.45,0.319,0.647,0.836,2.95,0.0,1.161,0,,,2,0,0,0,,
TGL,104.22,-0.036,-0.108,0.099,0.288,-0.118,0.341,0,,,0,0,0,0,,
THCCL,28.82,0.352,0.326,0.55,1.372,-0.12,2.479,0,,,0,1,0,0,,
TOMCL,40.67,0.058,0.148,0.185,0.697,-0.035,0.64,0,,,0,0,0,0,,
TRIPF,218.02,0.009,0.152,0.275,0.28,-0.056,1.1,0,,,1,0,0,0,,
UNITY,37.11,-0.038,-0.194,0.228,1.467,-0.248,0.319,0,2021-03-31,,0,0,0,0,,
WAFI,149.45,-0.087,-0.194,-0.237,-0.25,-0.3,0.401,0,,,0,0,0,0,,
WAVES,23.12,-0.088,-0.057,-0.06,-0.21,-0.258,0.772,0,,,2,0,0,0,,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2021-08-26,AVN,material_info,Material Information
2021-08-26,GTYR,material_info,Material Information
2021-08-26,IBFL,material_info,Material Information / Appointment of Director
2021-08-27,SAZEW,material_info,Material Information
2021-08-27,SNGP,material_info,Material Information
2021-08-27,SSGC,material_info,Material Information
2021-08-30,ANL,material_info,Material Information
2021-08-30,GTYR,material_info,Material Information
2021-08-30,SEARL,material_info,Material Information
2021-08-30,JSIL,material_info,Material Information
2021-08-31,MARI,material_info,Material Information
2021-08-31,BYCO,material_info,Disclosure of Material Information
2021-09-01,OTSU,material_info,Material Information
2021-09-01,AVN,material_info,Material Information
2021-09-01,DYNO,material_info,"Material Information in respect of Resignation of Mr. Murtaza Lalan, Direct"
2021-09-02,KTML,material_info,Material Information
2021-09-02,SSOM,material_info,Material Information
2021-09-02,FTMM,material_info,Material Information
2021-09-03,DMTX,material_info,Material Informaiton
2021-09-03,PAKRI,material_info,Material Information.
2021-09-03,THCCL,material_info,Material Information
2021-09-03,MTL,material_info,Material Information
2021-09-03,JSIL,material_info,Material Information REVOKED
2021-09-06,FFL,material_info,Material Information
2021-09-06,JSIL,material_info,Material Information REVISED
2021-09-06,GTYR,material_info,Disclosure of Material Information
2021-09-06,AVN,material_info,Material Information
2021-09-06,RPL,material_info,Material Information
2021-09-07,AGTL,material_info,Disclosure of material information
2021-09-07,DYNO,material_info,Material Information in respect of Change of Director
2021-09-07,ICIBL,material_info,MATERIAL INFORMATION
2021-09-08,AGHA,material_info,Material Info - Appointment of Directors
2021-09-08,CLVL,material_info,Material Information
2021-09-08,INDU,material_info,Material information
2021-09-10,DGKC,material_info,Material Information
2021-09-10,BIPL,material_info,Material Information: Press Release by US Department of Justice on Cyber At

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-2.622,2021-09-09
investor_type,last_5_sessions,broker proprietary trading,1.85,2021-09-09
investor_type,last_5_sessions,companies,0.837,2021-09-09
investor_type,last_5_sessions,foreign corporates,-13.511,2021-09-09
investor_type,last_5_sessions,foreign individual,0.052,2021-09-09
investor_type,last_5_sessions,individuals,6.282,2021-09-09
investor_type,last_5_sessions,insurance companies,7.081,2021-09-09
investor_type,last_5_sessions,mutual funds,-3.665,2021-09-09
investor_type,last_5_sessions,nbfc,0.163,2021-09-09
investor_type,last_5_sessions,other organization,3.209,2021-09-09
investor_type,last_5_sessions,overseas pakistani,0.324,2021-09-09
sector,last_5_sessions,fipi | All other Sectors,0.117,2021-09-09
sector,last_5_sessions,fipi | Cement,-2.061,2021-09-09
sector,last_5_sessions,fipi | Commercial Banks,-10.87,2021-09-09
sector,last_5_sessions,fipi | Fertilizer,-0.165,2021-09-09
sector,last_5_sessions,fipi | Food and Personal Care Products,0.283,2021-09-09
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-0.662,2021-09-09
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,0.04,2021-09-09
sector,last_5_sessions,fipi | Power Generation and Distribution,-0.109,2021-09-09
sector,last_5_sessions,fipi | Technology and Communication,0.252,2021-09-09
sector,last_5_sessions,fipi | Textile Composite,0.039,2021-09-09
sector,last_5_sessions,lipi banks / dfi | All other Sectors,0.447,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Cement,1.28,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,-0.502,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-0.1,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,0.09,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,-0.302,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.097,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,-1.105,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,-2.91,2021-09-09
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.383,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,0.117,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.026,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,-0.24,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Debt Market,-0.001,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,-0.042,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.1,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.151,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.005,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.016,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,1.666,2021-09-09
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,0.251,2021-09-09
sector,last_5_sessions,lipi companies | All other Sectors,0.774,2021-09-09
sector,last_5_sessions,lipi companies | Cement,-1.624,2021-09-09
sector,last_5_sessions,lipi companies | Commercial Banks,3.759,2021-09-09
sector,last_5_sessions,lipi companies | Debt Market,0.062,2021-09-09
sector,last_5_sessions,lipi companies | Fertilizer,-0.868,2021-09-09
sector,last_5_sessions,lipi companies | Food and Personal Care Products,-0.843,2021-09-09
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,0.266,2021-09-09
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,0.049,2021-09-09
sector,last_5_sessions,lipi companies | Power Generation and Distribution,0.222,2021-09-09
sector,last_5_sessions,lipi companies | Technology and Communication,-0.496,2021-09-09
sector,last_5_sessions,lipi companies | Textile Composite,-0.462,2021-09-09
sector,last_5_sessions,lipi individuals | All other Sectors,2.067,2021-09-09
sector,last_5_sessions,lipi individuals | Cement,3.694,2021-09-09
sector,last_5_sessions,lipi individuals | Commercial Banks,1.909,2021-09-09
sector,last_5_sessions,lipi individuals | Fertilizer,1.325,2021-09-09
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,0.32,2021-09-09
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,0.915,2021-09-09
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.398,2021-09-09
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.321,2021-09-09
sector,last_5_sessions,lipi individuals | Technology and Communication,-3.137,2021-09-09
sector,last_5_sessions,lipi individuals | Textile Composite,-0.734,2021-09-09
sector,last_5_sessions,lipi insurance companies | All other Sectors,0.4,2021-09-09
sector,last_5_sessions,lipi insurance companies | Cement,0.486,2021-09-09
sector,last_5_sessions,lipi insurance companies | Commercial Banks,3.414,2021-09-09
sector,last_5_sessions,lipi insurance companies | Fertilizer,-0.079,2021-09-09
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.143,2021-09-09
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-0.027,2021-09-09
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.789,2021-09-09
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,0.023,2021-09-09
sector,last_5_sessions,lipi insurance companies | Technology and Communication,1.808,2021-09-09
sector,last_5_sessions,lipi insurance companies | Textile Composite,0.124,2021-09-09
sector,last_5_sessions,lipi mutual funds | All other Sectors,-4.254,2021-09-09
sector,last_5_sessions,lipi mutual funds | Cement,-1.662,2021-09-09
sector,last_5_sessions,lipi mutual funds | Commercial Banks,0.827,2021-09-09
sector,last_5_sessions,lipi mutual funds | Debt Market,-0.061,2021-09-09
sector,last_5_sessions,lipi mutual funds | Fertilizer,-0.103,2021-09-09
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,0.059,2021-09-09
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-0.208,2021-09-09
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.598,2021-09-09
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.062,2021-09-09
sector,last_5_sessions,lipi mutual funds | Technology and Communication,2.123,2021-09-09
sector,last_5_sessions,lipi mutual funds | Textile Composite,0.275,2021-09-09
sector,last_5_sessions,lipi nbfc | All other Sectors,0.021,2021-09-09
sector,last_5_sessions,lipi nbfc | Cement,0.006,2021-09-09
sector,last_5_sessions,lipi nbfc | Commercial Banks,0.054,2021-09-09
sector,last_5_sessions,lipi nbfc | Fertilizer,0.05,2021-09-09
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,0.002,2021-09-09
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.01,2021-09-09
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.001,2021-09-09
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,0.01,2021-09-09
sector,last_5_sessions,lipi nbfc | Technology and Communication,-0.012,2021-09-09
sector,last_5_sessions,lipi nbfc | Textile Composite,0.021,2021-09-09
sector,last_5_sessions,lipi other organization | All other Sectors,0.311,2021-09-09
sector,last_5_sessions,lipi other organization | Cement,-0.145,2021-09-09
sector,last_5_sessions,lipi other organization | Commercial Banks,1.649,2021-09-09
sector,last_5_sessions,lipi other organization | Fertilizer,-0.016,2021-09-09
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,0.046,2021-09-09
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.144,2021-09-09
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.015,2021-09-09
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.683,2021-09-09
sector,last_5_sessions,lipi other organization | Technology and Communication,0.705,2021-09-09
sector,last_5_sessions,lipi other organization | Textile Composite,0.104,2021-09-09
investor_type,last_20_sessions,banks / dfi,-6.221,2021-09-09
investor_type,last_20_sessions,broker proprietary trading,1.607,2021-09-09
investor_type,last_20_sessions,companies,8.858,2021-09-09
investor_type,last_20_sessions,foreign corporates,-35.406,2021-09-09
investor_type,last_20_sessions,foreign individual,0.069,2021-09-09
investor_type,last_20_sessions,individuals,11.875,2021-09-09
investor_type,last_20_sessions,insurance companies,3.515,2021-09-09
investor_type,last_20_sessions,mutual funds,1.323,2021-09-09
investor_type,last_20_sessions,nbfc,0.641,2021-09-09
investor_type,last_20_sessions,other organization,10.167,2021-09-09
investor_type,last_20_sessions,overseas pakistani,3.572,2021-09-09
sector,last_20_sessions,fipi | All other Sectors,-12.078,2021-09-09
sector,last_20_sessions,fipi | Cement,-9.962,2021-09-09
sector,last_20_sessions,fipi | Commercial Banks,-17.166,2021-09-09
sector,last_20_sessions,fipi | Fertilizer,-0.242,2021-09-09
sector,last_20_sessions,fipi | Food and Personal Care Products,-0.018,2021-09-09
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-1.991,2021-09-09
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,-0.069,2021-09-09
sector,last_20_sessions,fipi | Power Generation and Distribution,0.113,2021-09-09
sector,last_20_sessions,fipi | Technology and Communication,8.122,2021-09-09
sector,last_20_sessions,fipi | Textile Composite,1.526,2021-09-09
sector,last_20_sessions,lipi banks / dfi | All other Sectors,0.376,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Cement,5.906,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-2.134,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-1.008,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.288,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.364,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.348,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-7.924,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,-3.395,2021-09-09
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.956,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,0.008,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Cement,0.262,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,0.077,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.001,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,0.195,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-1.668,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.356,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.185,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.147,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,2.463,2021-09-09
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,0.247,2021-09-09
sector,last_20_sessions,lipi companies | All other Sectors,8.257,2021-09-09
sector,last_20_sessions,lipi companies | Cement,-5.418,2021-09-09
sector,last_20_sessions,lipi companies | Commercial Banks,4.201,2021-09-09
sector,last_20_sessions,lipi companies | Debt Market,0.062,2021-09-09
sector,last_20_sessions,lipi companies | Fertilizer,-0.534,2021-09-09
sector,last_20_sessions,lipi companies | Food and Personal Care Products,-0.491,2021-09-09
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,0.283,2021-09-09
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,0.092,2021-09-09
sector,last_20_sessions,lipi companies | Power Generation and Distribution,2.595,2021-09-09
sector,last_20_sessions,lipi companies | Technology and Communication,-0.141,2021-09-09
sector,last_20_sessions,lipi companies | Textile Composite,-0.048,2021-09-09
sector,last_20_sessions,lipi individuals | All other Sectors,5.162,2021-09-09
sector,last_20_sessions,lipi individuals | Cement,9.528,2021-09-09
sector,last_20_sessions,lipi individuals | Commercial Banks,5.069,2021-09-09
sector,last_20_sessions,lipi individuals | Debt Market,-0.0,2021-09-09
sector,last_20_sessions,lipi individuals | Fertilizer,3.306,2021-09-09
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,0.559,2021-09-09
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,2.113,2021-09-09
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,1.852,2021-09-09
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,0.062,2021-09-09
sector,last_20_sessions,lipi individuals | Technology and Communication,-12.42,2021-09-09
sector,last_20_sessions,lipi individuals | Textile Composite,-3.356,2021-09-09
sector,last_20_sessions,lipi insurance companies | All other Sectors,-1.432,2021-09-09
sector,last_20_sessions,lipi insurance companies | Cement,4.301,2021-09-09
sector,last_20_sessions,lipi insurance companies | Commercial Banks,4.749,2021-09-09
sector,last_20_sessions,lipi insurance companies | Fertilizer,-1.739,2021-09-09
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,0.065,2021-09-09
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-1.232,2021-09-09
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-1.166,2021-09-09
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,0.106,2021-09-09
sector,last_20_sessions,lipi insurance companies | Technology and Communication,0.497,2021-09-09
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.634,2021-09-09
sector,last_20_sessions,lipi mutual funds | All other Sectors,-4.689,2021-09-09
sector,last_20_sessions,lipi mutual funds | Cement,-5.252,2021-09-09
sector,last_20_sessions,lipi mutual funds | Commercial Banks,2.642,2021-09-09
sector,last_20_sessions,lipi mutual funds | Debt Market,-0.477,2021-09-09
sector,last_20_sessions,lipi mutual funds | Fertilizer,-0.005,2021-09-09
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,1.124,2021-09-09
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,0.109,2021-09-09
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.509,2021-09-09
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,3.217,2021-09-09
sector,last_20_sessions,lipi mutual funds | Technology and Communication,4.162,2021-09-09
sector,last_20_sessions,lipi mutual funds | Textile Composite,1.0,2021-09-09
sector,last_20_sessions,lipi nbfc | All other Sectors,-0.132,2021-09-09
sector,last_20_sessions,lipi nbfc | Cement,0.016,2021-09-09
sector,last_20_sessions,lipi nbfc | Commercial Banks,0.394,2021-09-09
sector,last_20_sessions,lipi nbfc | Fertilizer,0.233,2021-09-09
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.011,2021-09-09
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.014,2021-09-09
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.065,2021-09-09
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.01,2021-09-09
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.006,2021-09-09
sector,last_20_sessions,lipi nbfc | Textile Composite,0.024,2021-09-09
sector,last_20_sessions,lipi other organization | All other Sectors,4.528,2021-09-09
sector,last_20_sessions,lipi other organization | Cement,0.618,2021-09-09
sector,last_20_sessions,lipi other organization | Commercial Banks,2.166,2021-09-09
sector,last_20_sessions,lipi other organization | Debt Market,0.416,2021-09-09
sector,last_20_sessions,lipi other organization | Fertilizer,-0.206,2021-09-09
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,0.131,2021-09-09
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.017,2021-09-09
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.428,2021-09-09
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,1.967,2021-09-09
sector,last_20_sessions,lipi other organization | Technology and Communication,0.706,2021-09-09
sector,last_20_sessions,lipi other organization | Textile Composite,0.286,2021-09-09

=== FILE: calendar.md ===
# Calendar as of 2021-09-10

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2021-08-13 WAVES: Board Meeting for the Quater Ended June 30, 2021
- 2021-08-13 ISL: Board Meeting Rescheduled
- 2021-08-16 PSO: Board Meeting
- 2021-08-16 GLAXO: Board of Directors Meeting
- 2021-08-16 CHCC: NOTICE OF BOARD OF DIRECTORS MEETING & CLOSED PERIOD
- 2021-08-17 PIBTL: NOTICE OF PIBT BOARD MEETING AUGUST 24, 2021
- 2021-08-17 HUBC: Board Meeting REVOKED
- 2021-08-17 ABOT: Board Meeting
- 2021-08-17 HUBC: Board Meeting
- 2021-08-17 AGP: Board Meeting
- 2021-08-17 SYS: Board Meeting
- 2021-08-17 PAEL: Board Meeting for the 2nd Quarter (Half Year) Ended June 30, 2021 (Un-Audited)
- 2021-08-17 MARI: Notice of Board of Directors Meeting
- 2021-08-20 GLAXO: Board Meeting Reschedule
- 2021-08-20 AVN: Board Meeting
- 2021-08-20 FEROZ: Board Meeting
- 2021-08-24 KOHC: Board Meeting
- 2021-08-26 STCL: Board Meeting
- 2021-08-30 MARI: Board Meeting Other Than Financials
- 2021-08-31 GGL: Meeting of the Board Of Directors - Ghani Global Holdings Limited
- 2021-08-31 IMAGE: Board Meeting Other Than Financial Results
- 2021-09-03 HTL: Board Meeting
- 2021-09-03 KEL: Board Meeting
- 2021-09-06 DGKC: BOARD MEETING
- 2021-09-07 ILP: Notice of Board Meeting for the Year Ended June 30, 2021 / Closed Period
- 2021-09-08 SEARL: Board Meeting Other Than Financial Results
- 2021-09-09 PPL: Meeting of the Board of Directors and Closed Period
- 2021-09-09 SPL: Board Meeting Other Than Financial Results
- 2021-09-10 MUGHAL: Notice of Board Meeting - FY 2021
- 2021-09-10 TGL: Board Meeting
- 2021-09-10 MTL: Board Meeting

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
