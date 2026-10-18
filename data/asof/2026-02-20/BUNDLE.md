# Replay bundle, close of 2026-02-20

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
# Market as of 2026-02-20 close (public information only)

- KSE100: 173,170 on 2026-02-20; 1m -7.4%, 3m +6.8%, 6m +16.7%, 12m +53.1%
- KMI All Share: 66,507 on 2026-02-20; 1m -8.0%, 3m +3.9%, 6m +9.6%, 12m +38.1%
- Policy rate 10.5%; last MPC decision 2026-01-26: hold (+0bp)
- 6M T-bill cutoff 10.44% (auction 2026-02-18); 3M 10.29%, 12M 10.60%
- CPI YoY 5.79% for 2026-01 (published by 2026-02-03); three months earlier (2025-10) 6.25%
- Brent: 72.75 USD/bbl on 2026-02-20; 3-month change +14.3%
- USD/PKR: 279.75  on 2026-02-20; 3-month change -0.4%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate -0.06pp (market near policy rate); CPI falling over 3 months (-0.5pp)
- Next MPC: see SBP calendar

Session date used: 2026-02-20. Liquid KMI names: 131 (membership KMI_ALL_derived_2025-12-02.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.146,-0.0963,0.0915,0,0
E&P,3,-0.1249,0.0745,0.1922,0,0
OMC,4,-0.1342,-0.0256,0.0475,0,0
Power,6,-0.0709,0.1029,0.2362,0,0
Fertilizer,4,-0.0613,0.1088,0.2439,0,0
Cement,16,-0.1269,-0.0741,0.1596,0,0
Steel & engineering,11,-0.0673,-0.0251,0.0485,0,0
Autos,12,-0.0938,-0.0452,-0.0633,0,0
Tech & telecom,11,-0.1422,-0.1143,0.041,0,0
Islamic banks & fin.,9,-0.128,-0.1743,-0.0153,0,0
Pharma,14,-0.0568,-0.0208,-0.0042,0,0
Textiles,23,-0.1264,-0.0745,-0.152,0,0
Food & staples,15,-0.1404,-0.0201,0.0333,0,0
Chemicals,19,-0.0964,-0.044,0.1324,0,0
"Glass, packaging, paper",13,-0.1391,-0.0423,-0.1017,0,0
Gas utilities & misc,13,-0.0879,-0.0232,0.1128,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AGP,225.38,0.006,0.225,0.115,0.378,-0.074,2.401,1,2025-09-30,0.333,0,0,0,0,17.84,0.024
AIRLINK,162.43,-0.119,-0.065,0.12,-0.092,-0.153,0.402,0,2025-09-30,0.883,0,1,0,0,12.707,0.046
ARPL,439.11,0.021,0.02,-0.012,-0.023,-0.094,0.91,0,2025-12-31,0.242,2,0,0,0,13.647,0.065
ATRL,752.72,-0.09,0.115,0.144,0.208,-0.151,0.956,0,2025-09-30,-0.353,0,1,0,0,8.095,0.015
BERG,102.79,0.004,0.018,-0.035,0.1,-0.148,2.622,0,2025-12-31,0.173,1,0,0,0,9.087,0.045
BFAGRO,39.52,-0.075,-0.002,-0.049,,-0.177,0.327,1,,,0,0,0,0,,
BFBIO,158.26,-0.036,0.026,-0.07,-0.192,-0.214,1.577,0,2025-09-30,-0.006,0,0,0,0,33.326,
BIFO,143.37,-0.208,-0.146,-0.216,-0.228,-0.257,0.818,0,2025-12-31,1.653,1,0,0,0,,
BIPL,28.64,-0.135,-0.07,-0.169,0.254,-0.332,0.382,0,2025-12-31,-0.44,1,0,0,0,,
BNL,9.77,-0.151,-0.929,-0.9,-0.332,-0.939,0.607,0,2025-06-30,,0,0,0,0,,
BWHL,205.51,-0.054,0.21,0.209,0.634,-0.111,1.267,0,,,2,0,0,0,,
CEPB,32.87,-0.238,0.01,0.191,0.214,-0.269,0.518,0,2025-12-31,-6.462,1,0,0,0,,
CHCC,303.38,-0.087,-0.062,-0.078,0.164,-0.177,0.715,0,2025-12-31,-0.113,1,0,0,0,6.497,0.019
CNERGY,7.01,-0.106,-0.106,-0.01,-0.034,-0.227,1.0,0,2024-06-30,,0,0,0,0,,
CPHL,85.98,-0.039,0.054,-0.003,-0.105,-0.139,0.826,0,2025-12-31,0.58,2,0,0,0,21.506,0.042
CPPL,80.51,-0.184,-0.2,-0.267,-0.285,-0.402,0.298,0,,,1,0,0,0,,
CSAP,109.68,-0.088,0.138,0.103,0.052,-0.195,2.174,0,2025-09-30,0.694,1,2,0,0,,0.065
DGKC,214.44,-0.073,-0.024,0.145,0.965,-0.203,0.604,0,2025-09-30,1.672,0,0,0,0,7.851,0.012
ECOP,47.04,-0.193,-0.18,-0.328,0.948,-0.467,0.391,0,2025-12-31,-1.411,1,0,0,0,9.418,0.03
EFERT,212.89,-0.114,-0.011,0.066,0.034,-0.165,1.371,0,2025-12-31,-0.186,2,0,0,0,9.648,0.105
ENGROH,276.62,0.043,0.31,0.306,0.367,-0.072,1.439,0,2025-09-30,0.043,0,1,0,0,9.7,0.04
EPCL,33.75,0.038,0.147,0.188,-0.057,-0.147,1.59,1,2025-12-31,-1.288,1,1,0,0,,
EPQL,23.71,-0.25,-0.209,-0.165,0.266,-0.312,3.476,0,2025-12-31,,1,0,0,0,,
FABL,93.09,-0.064,0.14,0.211,1.148,-0.105,0.692,0,2025-12-31,0.953,1,0,0,0,3.08,0.144
FATIMA,156.75,-0.108,0.138,0.269,1.043,-0.164,1.358,0,2025-09-30,0.301,0,0,0,0,4.517,0.089
FCCL,52.8,-0.102,0.008,0.042,0.394,-0.135,0.702,0,2025-06-30,2.312,0,5,0,0,8.222,0.028
FCEPL,83.02,-0.076,-0.014,-0.026,0.038,-0.241,0.756,0,2024-09-30,2.03,1,0,0,0,31.055,0.031
FCL,24.93,-0.027,0.042,-0.024,0.01,-0.101,0.803,0,2025-12-31,-0.163,1,1,0,0,12.305,0.021
FECTC,109.49,-0.221,-0.308,0.242,-0.04,-0.424,0.693,0,2025-12-31,0.979,1,0,0,0,,
FFC,555.74,-0.072,-0.003,0.282,0.598,-0.174,1.589,0,2025-09-30,-0.027,1,1,0,0,5.523,0.112
FFL,18.28,-0.211,-0.019,0.082,0.232,-0.211,0.517,0,2025-12-31,1.0,2,0,0,0,68.835,
GAL,479.36,-0.107,-0.136,-0.11,0.078,-0.215,1.04,0,2025-12-31,1.662,1,0,0,0,5.252,0.026
GCIL,27.05,-0.232,-0.232,-0.035,0.74,-0.297,0.586,0,,,0,0,0,0,,
GCWL,19.55,-0.009,0.024,0.488,,-0.2,1.247,0,,,0,0,0,0,,
GHNI,879.5,-0.039,0.114,0.102,0.323,-0.13,1.186,0,2025-12-31,0.778,1,0,0,0,6.046,0.015
GLAXO,395.0,-0.092,0.014,-0.014,0.006,-0.144,0.737,0,2025-09-30,0.058,0,0,0,0,19.339,0.025
GTYR,31.91,-0.232,-0.15,-0.312,-0.304,-0.358,1.631,0,2025-12-31,-53.333,1,0,0,0,,
HCAR,211.55,-0.187,-0.253,-0.275,-0.262,-0.32,0.722,0,2025-12-31,0.156,2,0,0,0,15.254,0.028
HUBC,219.98,-0.068,0.019,0.43,0.816,-0.099,0.781,0,2025-12-31,1.592,1,0,0,0,3.875,0.109
ICL,145.38,-0.098,-0.046,0.639,1.032,-0.133,0.284,0,,,1,0,0,0,,
ILP,82.48,-0.003,0.122,0.192,0.412,-0.11,1.697,0,2025-12-31,1.842,1,0,0,0,17.114,0.015
INIL,184.39,-0.004,-0.007,-0.027,0.162,-0.221,1.001,0,2025-12-31,4.885,3,0,0,0,25.968,0.023
IPAK,29.37,-0.003,0.213,0.301,0.449,-0.085,1.016,0,2025-09-30,2.303,1,0,0,0,13.394,0.027
ISL,91.15,-0.129,0.006,-0.096,0.153,-0.274,0.511,0,2025-12-31,1.793,1,0,0,0,25.861,0.027
ITTEFAQ,7.58,-0.249,-0.185,-0.162,0.024,-0.375,0.283,0,,,1,0,0,0,,
JSML,62.28,-0.22,0.125,0.188,1.02,-0.227,0.315,0,,,2,0,0,0,,
JVDC,143.22,0.017,0.948,0.882,1.486,-0.106,2.405,0,2025-09-30,-0.214,0,0,0,0,14.977,0.078
KEL,8.03,0.146,0.429,0.606,0.898,-0.148,1.41,0,2024-06-30,-0.871,1,4,0,0,30.127,
KOHC,102.02,-0.106,0.004,-0.025,0.335,-0.166,0.491,0,2025-09-30,-0.088,0,0,0,0,6.026,
LCI,259.39,-0.115,-0.136,-0.2,0.157,-0.303,0.683,0,2025-12-31,-0.346,1,0,0,0,12.485,0.041
LOADS,13.79,-0.238,-0.254,-0.124,-0.285,-0.335,0.231,0,2025-12-31,0.044,1,0,0,0,13.777,
LOTCHEM,22.74,-0.191,-0.017,0.26,0.345,-0.191,0.913,0,2025-09-30,-0.818,0,0,0,0,11.982,0.239
LUCK,436.5,-0.113,0.019,0.059,0.508,-0.149,1.408,0,2025-12-31,0.055,1,0,0,0,6.763,0.011
MACFL,26.02,-0.302,0.03,-0.234,0.71,-0.599,1.922,1,2025-12-31,5.0,1,0,0,0,34.336,0.01
MACTER,319.76,-0.046,-0.076,-0.197,0.255,-0.486,0.72,0,,,1,1,0,0,,
MARI,664.63,-0.089,-0.052,0.104,0.217,-0.147,0.635,0,2025-12-31,0.144,1,1,0,0,11.514,0.035
MEBL,482.21,0.007,0.154,0.252,1.243,-0.062,0.864,0,2025-12-31,-0.143,1,1,0,0,4.229,0.116
MFL,54.13,-0.276,-0.239,0.002,0.065,-0.323,0.286,0,2025-12-31,0.269,1,0,0,0,14.487,
MLCF,108.43,-0.101,0.055,0.127,1.312,-0.168,0.61,0,2024-12-31,0.708,0,1,0,0,7.675,
MTL,537.67,0.001,0.056,-0.036,-0.074,-0.123,2.015,0,2025-12-31,-0.241,1,0,0,0,17.531,0.107
MUGHAL,84.12,-0.136,0.026,0.112,0.139,-0.239,0.68,0,2025-09-30,134.0,0,0,0,0,28.337,
NETSOL,115.21,-0.107,-0.089,-0.198,-0.173,-0.292,0.774,0,2025-12-31,,2,0,0,0,8.173,
NML,170.37,-0.134,0.216,0.19,0.886,-0.169,0.999,0,2025-09-30,-0.398,0,0,0,0,8.671,0.016
NRL,336.51,-0.228,-0.209,0.234,0.35,-0.274,0.866,0,2025-09-30,,0,0,0,0,,
OBOY,10.01,-0.248,0.064,0.116,0.031,-0.332,0.913,0,,,2,0,0,0,,
OGDC,290.41,-0.123,0.143,0.152,0.51,-0.13,1.112,0,2025-09-30,-0.066,0,0,0,0,5.583,0.068
PAEL,48.88,-0.202,-0.06,0.118,0.251,-0.225,0.35,0,2025-09-30,0.542,0,0,0,0,16.997,
PIBTL,18.68,-0.143,0.214,0.669,1.383,-0.173,0.672,0,2025-12-31,0.238,1,0,0,0,,
PIOC,274.7,-0.313,-0.159,0.134,0.548,-0.348,0.241,0,2025-09-30,0.247,1,0,0,0,10.627,0.044
POWER,18.87,-0.047,0.033,0.226,0.762,-0.126,1.06,0,2025-12-31,0.568,2,0,0,0,31.257,
PPL,229.02,-0.163,0.136,0.313,0.368,-0.186,0.98,0,2025-12-31,-0.262,2,0,0,0,5.148,0.044
PRL,30.97,-0.161,-0.169,-0.01,-0.08,-0.228,0.486,0,2025-12-31,2.296,1,0,0,0,,
PSO,400.65,-0.191,-0.107,0.012,0.228,-0.204,0.538,0,2025-12-31,-0.336,1,0,0,0,10.778,0.026
QUICE,26.99,-0.274,1.829,2.202,3.089,-0.355,0.585,0,,,0,0,0,0,,
SAZEW,2232.34,0.147,0.322,0.558,1.121,-0.091,2.346,0,2025-12-31,0.671,2,0,0,0,4.217,0.046
SEARL,104.99,-0.174,0.02,0.094,0.226,-0.223,0.437,0,2025-09-30,1.232,0,0,0,0,,
SGF,113.3,-0.048,0.192,0.337,0.255,-0.139,1.125,0,2025-09-30,0.356,0,1,0,0,,
SLGL,20.36,-0.037,0.056,0.144,0.387,-0.19,0.323,0,2025-03-31,0.146,0,1,0,0,7.077,
SNGP,102.09,-0.145,-0.128,-0.102,0.274,-0.254,0.807,0,2025-09-30,0.048,0,0,0,0,5.073,0.026
SPEL,46.29,-0.196,-0.141,-0.284,0.133,-0.405,0.272,0,2025-09-30,-0.08,1,0,0,0,,
SSGC,30.62,-0.114,-0.083,-0.28,-0.013,-0.332,0.574,1,2025-09-30,-0.849,0,0,0,0,10.954,0.012
SYS,140.16,-0.105,-0.05,0.02,0.295,-0.182,0.986,0,2025-09-30,0.267,0,0,0,0,24.356,0.01
TELE,9.45,-0.223,-0.194,0.189,0.172,-0.287,0.279,0,2025-09-30,0.667,0,0,0,0,18.478,
TOMCL,41.35,-0.216,-0.213,0.11,0.413,-0.376,0.304,0,2025-12-31,-0.04,1,0,0,0,13.655,
TPLP,9.55,-0.224,-0.145,-0.067,-0.217,-0.261,0.513,0,,,3,0,0,0,,
TREET,25.97,-0.255,-0.188,0.046,0.233,-0.282,0.409,0,2025-09-30,1.111,0,0,0,0,17.461,
TRSM,11.12,-0.404,-0.8,-0.736,1.746,-0.837,0.679,0,2025-12-31,-0.345,1,0,0,0,,
ZAL,59.92,-0.161,0.227,1.116,,-0.171,1.477,0,2025-09-30,2.926,0,0,0,0,6.31,0.062

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2026-02-11,SYM,material_info,Material Information
2026-02-11,BECO,material_info,Material Information
2026-02-12,BLUEX,material_info,Disclosure of Material Information
2026-02-12,ORM,material_info,Material Information
2026-02-12,NATF,material_info,"Disclosure of Material Information under Section 96 of the Securities Act, "
2026-02-13,HMB,material_info,Material Information
2026-02-13,CLOV,material_info,Material Information
2026-02-13,KEL,material_info,KEL | K-Electric Limited Material Information
2026-02-16,FCCL,material_info,Material Information - Public Announcement of Offer to Acquire Shares and J
2026-02-16,FCSC,material_info,Material Information
2026-02-16,SRVI,material_info,Material Information
2026-02-16,KAPCO,material_info,Disclosure of Material Information
2026-02-16,SGF,material_info,Material Information
2026-02-16,FIBLM,material_info,Material Information - Change of Management Control
2026-02-16,BECO,material_info,Material Information
2026-02-16,ACPL,material_info,Material Information
2026-02-16,PNSC,material_info,Disclosure of Material Information
2026-02-17,KAPCO,material_info,Material Information - Newspapers Publication of Public Announcement of Off
2026-02-17,FCCL,material_info,Material Information - Newspapers Publication of Public Announcement of Off
2026-02-17,FCCL,material_info,Material Information - Newspapers Publication of Public Announcement of Off
2026-02-17,ENGROH,material_info,Material Information
2026-02-17,EPCL,material_info,Material Information - Engro Polymer & Chemicals Limited
2026-02-18,FCL,material_info,Disclosure of material Information
2026-02-18,KAPCO,material_info,Disclosure of Material Information
2026-02-18,FCCL,material_info,Disclosure of Material Information
2026-02-19,BML,material_info,Material Information
2026-02-19,DHPL,material_info,Disclosure of Material Information
2026-02-19,CYAN,material_info,Disclosure of Material Information
2026-02-19,DLL,material_info,Disclosure of Material Information
2026-02-19,PREMA,material_info,Material Information
2026-02-19,SBL,material_info,Disclosure of Material Information REVOKED
2026-02-20,MLCF,material_info,Disclosure of Material Information
2026-02-20,ACPL,material_info,Material Information
2026-02-20,AGL,material_info,Material Information - Resumption of Urea Operations
2026-02-20,SBL,material_info,Disclosure of Material Information
2026-02-20,DADX,material_info,Disclosure of Material Information
2026-02-20,PHDL,material_info,Material Information
2026-02-20,BML,material_info,Material Information
2026-02-20,PAKL,material_info,Disclosure of Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,22.433,2026-02-19
investor_type,last_5_sessions,broker proprietary trading,-6.871,2026-02-19
investor_type,last_5_sessions,companies,2.584,2026-02-19
investor_type,last_5_sessions,foreign corporates,-41.653,2026-02-19
investor_type,last_5_sessions,foreign individual,-0.003,2026-02-19
investor_type,last_5_sessions,individuals,23.365,2026-02-19
investor_type,last_5_sessions,insurance companies,1.511,2026-02-19
investor_type,last_5_sessions,mutual funds,-2.47,2026-02-19
investor_type,last_5_sessions,nbfc,0.117,2026-02-19
investor_type,last_5_sessions,other organization,0.854,2026-02-19
investor_type,last_5_sessions,overseas pakistani,0.132,2026-02-19
sector,last_5_sessions,fipi | Cement,-12.659,2026-02-19
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-10.754,2026-02-19
sector,last_5_sessions,fipi | Technology and Communication,-10.26,2026-02-19
sector,last_5_sessions,lipi banks / dfi | Debt Market,9.803,2026-02-19
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,6.324,2026-02-19
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,7.489,2026-02-19
sector,last_5_sessions,lipi individuals | Technology and Communication,6.884,2026-02-19
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-7.227,2026-02-19
sector,last_5_sessions,lipi mutual funds | Cement,5.444,2026-02-19
sector,last_5_sessions,lipi mutual funds | Debt Market,-10.886,2026-02-19
sector,last_5_sessions,lipi mutual funds | Fertilizer,-5.422,2026-02-19
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,6.264,2026-02-19
investor_type,last_20_sessions,banks / dfi,12.128,2026-02-19
investor_type,last_20_sessions,broker proprietary trading,-20.513,2026-02-19
investor_type,last_20_sessions,companies,11.274,2026-02-19
investor_type,last_20_sessions,foreign corporates,-72.333,2026-02-19
investor_type,last_20_sessions,foreign individual,-0.25,2026-02-19
investor_type,last_20_sessions,individuals,57.138,2026-02-19
investor_type,last_20_sessions,insurance companies,-2.16,2026-02-19
investor_type,last_20_sessions,mutual funds,0.054,2026-02-19
investor_type,last_20_sessions,nbfc,0.156,2026-02-19
investor_type,last_20_sessions,other organization,-1.792,2026-02-19
investor_type,last_20_sessions,overseas pakistani,16.297,2026-02-19
sector,last_20_sessions,fipi | Cement,-20.293,2026-02-19
sector,last_20_sessions,fipi | Technology and Communication,-13.984,2026-02-19
sector,last_20_sessions,lipi banks / dfi | Debt Market,21.755,2026-02-19
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-6.885,2026-02-19
sector,last_20_sessions,lipi companies | Commercial Banks,11.851,2026-02-19
sector,last_20_sessions,lipi individuals | Cement,12.98,2026-02-19
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,17.393,2026-02-19
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,9.197,2026-02-19
sector,last_20_sessions,lipi insurance companies | Debt Market,8.672,2026-02-19
sector,last_20_sessions,lipi mutual funds | All other Sectors,13.91,2026-02-19
sector,last_20_sessions,lipi mutual funds | Debt Market,-31.14,2026-02-19
sector,last_20_sessions,lipi mutual funds | Technology and Communication,8.095,2026-02-19

=== FILE: calendar.md ===
# Calendar as of 2026-02-20

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2026-01-22 FFC: Board Meeting
- 2026-01-22 ARPL: Board Meeting
- 2026-01-22 JSML: Board Meeting
- 2026-01-23 PRL: Board Meeting
- 2026-01-26 EPQL: Board Meeting for the announcement of the financial results for the year ended December 31, 2025
- 2026-01-26 GATI: Board Meeting Other Than Financial Results
- 2026-01-26 HINOON: Board Meeting Other Then Financial Results
- 2026-01-27 ILP: Notice of Board Meeting for the Half Year ended December 31, 2025 / Closed Period
- 2026-01-28 MEBL: NOTICE OF BOARD MEETING AND CLOSED PERIOD
- 2026-01-28 CSAP: NOTICE OF 203rd BOARD MEETING
- 2026-01-30 WAFI: Board Meeting other than Financial Results
- 2026-02-02 EFERT: Board Meeting for the announcement of the financial results for the year ended December 31, 2025
- 2026-02-03 MACFL: Board Meeting
- 2026-02-03 CPHL: Board Meeting REVOKED
- 2026-02-03 CPHL: Board meeting
- 2026-02-03 BWHL: Board Meeting
- 2026-02-03 EPCL: Board Meeting for the announcement of the financial results for the year ended December 31, 2025 - Engro Polymer & Chemicals Ltd
- 2026-02-03 PPL: Meeting of the Board of Directors and Closed Period
- 2026-02-04 SGPL: Board Meeting Other Than Financial Results
- 2026-02-04 POWER: Board Meeting
- 2026-02-04 PIOC: Board Meeting
- 2026-02-06 NETSOL: Board Meeting
- 2026-02-06 SSGC: Board Meeting Other Than Financial Results
- 2026-02-06 MACTER: Board Meeting
- 2026-02-06 CLOV: Board Meeting Other Than Financial Results
- 2026-02-06 ECOP: Intimation of the 150th Meeting of the Board of ECOP
- 2026-02-06 FCL: Notice of Board Meeting/closed period of FCL
- 2026-02-06 IPAK: Board Meeting for the Half Year ended 31st December 2025
- 2026-02-09 FABL: Board of Directors Meeting of Faysal Bank Limited
- 2026-02-09 BERG: Board Meetings
- 2026-02-09 PIBTL: Board Meeting will be Held on February 16, 2026
- 2026-02-09 LCI: Board Meeting Other Than Financial Results
- 2026-02-10 PSO: Board Meeting
- 2026-02-10 SPEL: Board Meeting
- 2026-02-10 ICL: Board Meeting
- 2026-02-10 TOMCL: Board Meeting
- 2026-02-10 TRSM: Board of Directors Meeting for Half Year ended December 31, 2025.
- 2026-02-10 FECTC: Board Meeting
- 2026-02-10 GTYR: Board Meeting
- 2026-02-10 MTL: Board meeting
- 2026-02-10 LOADS: Board Meeting of Loads Limited
- 2026-02-10 MFL: Board Meeting
- 2026-02-10 CHCC: Board Meeting
- 2026-02-10 CPPL: Board Meeting
- 2026-02-11 PRL: Board Meeting other than Financial Results
- 2026-02-11 GHNI: Board Meeting
- 2026-02-11 GAL: Board Meeting
- 2026-02-11 BIPL: Board Meeting - BankIslami Pakistan Limited
- 2026-02-11 ACPL: Board Meeting
- 2026-02-12 CEPB: BOARD MEETING
- 2026-02-12 NRL: Board Meeting
- 2026-02-12 KEL: Board Meeting Other Than Financial Results
- 2026-02-12 SHFA: Board Meeting
- 2026-02-12 PPL: Change in Time of the Meeting of the Board of Directors
- 2026-02-13 OGDC: Board Meeting
- 2026-02-13 EFERT: Board Meeting other than Financial Results (Shorter Notice)
- 2026-02-13 BBFL: Board Meeting
- 2026-02-16 DGKC: Board Meeting
- 2026-02-16 SGPL: Board Meeting Other Than Financial Results held on February 16, 2026
- 2026-02-16 BFAGRO: Board Meeting
- 2026-02-16 TGL: Board Meeting
- 2026-02-16 DOL: Board Meeting
- 2026-02-16 TPLT: Board Meeting
- 2026-02-16 HUBC: Board Meeting for the Half Year Ended December 31, 2025 - The Hub Power Company Limited
- 2026-02-16 CNERGY: Board Meeting and Closed Period
- 2026-02-17 MLCF: MLCF-Notice of Board Meeting 24.02.2026
- 2026-02-17 ENGROH: Board Meeting for the Announcement of the Financial Results for the year ended December 31, 2025
- 2026-02-17 IBLHL: Board Meeting
- 2026-02-17 FLYNG: Board Meeting
- 2026-02-17 LCI: Board Meeting Other Than Financial Results
- 2026-02-18 EFERT: Board Meeting other than Financial Results-Shorter Notice
- 2026-02-18 KOHC: Board Meeting
- 2026-02-18 TPLP: Board Meeting
- 2026-02-18 BFBIO: Board Meeting
- 2026-02-18 GHGL: BOARD MEETING
- 2026-02-18 ZAL: Board Meeting
- 2026-02-18 ASL: BOARD MEETING / CLOSED PERIOD
- 2026-02-18 KTML: KTML-Notice of Board Meeting 25.02.2026
- 2026-02-18 TATM: Board of Directors Meeting - December 2025
- 2026-02-18 QUICE: BOARD MEETING
- 2026-02-18 WASL: Board Meeting
- 2026-02-18 TBL: Notice of Board Meeting [Q2 FY 25-26]
- 2026-02-18 DCL: Board Meeting
- 2026-02-18 SSGC: Board Meeting
- 2026-02-18 DCR: BOARD MEETING / CLOSED PERIOD
- 2026-02-18 HTL: Board Meeting
- 2026-02-19 PREMA: Board Meeting
- 2026-02-19 IMAGE: Board Meeting
- 2026-02-19 GATM: BOARD MEETING AND CLOSED PERIOD
- 2026-02-19 FEROZ: Board Meeting
- 2026-02-19 LIVEN: Board Meeting for Accounts for the Period Ended 31st December 2025
- 2026-02-19 CLOV: Board of Directors Meeting and Closed Period
- 2026-02-19 SNGP: Board Meeting
- 2026-02-19 GGGL: Meeting of the Board of Directors - GHANI GLOBAL GLASS LIMITED
- 2026-02-19 GCIL: Meeting of the Board of Directors - GHANI CHEMICAL INDUSTRIES LIMITED
- 2026-02-19 GGL: Meeting of the Board of Directors - GHANI GLOBAL HOLDINGS LIMITED
- 2026-02-19 GCWL: Meeting of the Board of Directors - GHANI CHEMWORLD LIMITED
- 2026-02-19 SEARL: Board Meeting
- 2026-02-19 CRTM: Board Meeting
- 2026-02-19 DNCC: Board Meeting
- 2026-02-19 TREET: Treet Corporation Limited - Notice of Board Meeting/ Closed Period
- 2026-02-20 SYM: Board Meeting
- 2026-02-20 OBOY: NOTICE OF BOARD MEETING
- 2026-02-20 GATI: BOARD MEETING
- 2026-02-20 MUGHAL: Notice of Board Meeting - HY 2026
- 2026-02-20 NML: Board Meeting
- 2026-02-20 SGPL: Board Meeting
- 2026-02-20 GWLC: Board Meeting
- 2026-02-20 ANL: Board Meeting
- 2026-02-20 BECO: Board Meeting
- 2026-02-20 TELE: Board Meeting to Review Half Yearly Accounts
- 2026-02-20 BNL: Board Meeting

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
| 6 | Rs1.225tn power bank facility | 2025 | outcome not shown |
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
| 22 | Net-metering reform | Draft Dec 2025 | Notified 9 Feb 2026; partly reversed. Y |
| 23 | IMF EFF Board | Staff deal 12 Jul 2024 | 25 Sep 2024. Y |
**"No plan to raise prices or taxes."** I found no dated denial followed by a reversal, so the base rate is unmeasured. Dated facts only: Rs170bn of taxes announced 10 Feb 2023; a November 2024 denial of mini-budget rumours after an IMF visit (Aaj), with no mini-budget found since (unverified); a pledge of contingency tax measures from Jan 2026 if revenue lagged (Tribune) with no verified outcome.

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
