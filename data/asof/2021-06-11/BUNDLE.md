# Replay bundle, close of 2021-06-11

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
# Market as of 2021-06-11 close (public information only)

- KSE100: 48,305 on 2021-06-11; 1m +7.5%, 3m +5.4%, 6m +14.4%, 12m +39.0%
- KMI All Share: 23,671 on 2021-06-11; 1m +8.5%, 3m +3.7%, 6m +13.6%, 12m +37.0%
- Policy rate 7.0%; last MPC decision 2021-05-28: hold (+0bp)
- 6M T-bill cutoff 7.59% (auction 2021-06-02); 3M 7.35%, 12M 7.67%
- CPI YoY 10.84% for 2021-05 (published by 2021-06-03); three months earlier (2021-02) 8.68%
- Brent: 72.05 USD/bbl on 2021-06-11; 3-month change +3.9%
- USD/PKR: 155.63  on 2021-06-11; 3-month change -0.8%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.59pp (market pricing hikes); CPI rising over 3 months (+2.2pp)
- Next MPC: see SBP calendar

Session date used: 2021-06-11. Liquid KMI names: 57 (membership KMI_ALL_derived_2020-12-31.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.1602,0.0508,0.6335,0,1
E&P,3,0.0418,-0.0438,0.0114,0,0
OMC,4,0.1878,-0.0227,0.2104,0,0
Power,4,0.0693,0.0433,0.1651,1,1
Fertilizer,4,0.069,0.0463,0.0887,0,2
Cement,16,0.1931,0.098,0.3365,1,1
Steel & engineering,10,0.2123,0.062,0.2061,1,1
Autos,12,0.1609,0.0749,0.1299,1,2
Tech & telecom,6,0.2207,0.1139,0.7997,2,2
Islamic banks & fin.,8,0.0395,-0.0349,0.0254,0,1
Pharma,11,0.1088,0.0508,0.1247,0,1
Textiles,23,0.0967,0.0064,0.2779,1,1
Food & staples,13,0.1953,0.1847,0.249,3,4
Chemicals,17,0.1363,0.1446,0.2695,1,3
"Glass, packaging, paper",12,0.2258,0.1493,0.2722,1,2
Gas utilities & misc,9,0.2831,0.2033,0.1804,1,1

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ABOT,775.02,0.0,0.042,0.012,0.347,-0.01,0.565,0,,,0,0,0,0,,
ACPL,177.17,0.094,-0.027,0.235,0.384,-0.074,0.668,0,,,0,0,0,0,,
AGP,102.52,-0.083,-0.162,-0.059,-0.019,-0.247,0.694,0,,,0,0,0,0,,
ASC,18.7,0.403,0.263,0.24,0.767,-0.018,1.973,0,,,0,0,0,0,,
ATRL,267.33,0.208,0.13,0.675,1.849,-0.038,0.567,0,,,0,0,0,0,,
CEPB,126.57,0.292,0.182,0.17,1.377,-0.035,1.131,0,,,0,0,0,0,,
CHCC,186.73,0.127,0.062,0.378,1.107,-0.029,0.779,0,,,0,0,0,0,,
DCL,11.55,0.348,-0.019,0.19,0.442,-0.156,1.04,0,,,0,0,0,0,,
DGKC,126.09,0.14,-0.061,0.188,0.512,-0.109,1.122,0,,,0,0,0,0,,
DOL,28.66,0.147,0.031,-0.104,0.229,-0.289,0.992,0,,,0,0,0,0,,
EFERT,72.03,0.064,0.095,0.18,0.183,-0.005,1.187,0,,,0,0,0,0,,
EPCL,47.71,-0.045,-0.02,0.101,0.877,-0.165,0.667,0,,,0,0,0,0,,
FCCL,24.03,0.054,-0.025,0.123,0.427,-0.117,0.834,0,,,0,0,0,0,,
FEROZ,364.53,0.24,0.087,0.146,0.271,-0.048,0.844,2,,,0,0,0,0,,
FLYNG,22.36,0.97,0.548,1.708,2.097,0.0,3.657,3,,,0,0,0,0,,
GAL,113.02,0.193,0.021,0.247,0.713,-0.128,0.751,1,,,0,0,0,0,,
GGGL,23.87,0.574,0.476,1.462,1.867,0.0,2.865,1,,,0,0,0,0,,
GGL,46.66,0.226,1.338,2.567,3.475,-0.018,1.734,1,,,0,1,0,0,,
GHGL,51.15,0.102,0.09,0.25,1.005,-0.099,2.303,1,,,0,0,0,0,,
GHNI,285.08,0.152,0.015,0.048,1.484,-0.16,0.939,1,,,0,0,0,0,,
HCAR,377.32,0.262,0.308,0.18,0.952,-0.038,1.907,0,,,2,0,0,0,,
HTL,75.33,0.204,-0.061,0.814,1.435,-0.21,0.752,0,,,0,0,0,0,,
ILP,69.99,0.066,-0.043,0.112,0.604,-0.086,0.446,0,,,0,0,0,0,,
IMAGE,27.69,0.7,,,,,1.323,2,,,0,1,0,0,,
INIL,211.8,0.068,-0.016,0.416,1.183,-0.121,0.817,0,,,1,0,0,0,,
ISL,91.49,0.116,0.003,0.14,0.763,-0.067,0.635,0,,,0,0,0,0,,
KEL,4.19,0.139,0.048,0.126,0.347,-0.103,1.302,0,2021-03-31,2.0,0,0,0,0,,
KOHC,210.31,0.101,-0.049,-0.026,0.439,-0.147,0.899,0,,,0,0,0,0,,
LCI,905.88,0.075,0.058,0.23,0.294,-0.006,0.4,0,,,0,0,0,0,,
LUCK,911.6,0.066,0.048,0.353,0.991,-0.031,1.411,0,,,0,0,0,0,,
MARI,1550.05,0.02,-0.025,0.11,0.22,-0.084,0.777,0,,,0,0,0,0,,
MEBL,112.92,0.049,0.053,0.189,1.031,-0.017,0.827,0,,,0,0,0,0,,
MLCF,46.83,0.109,0.014,0.153,0.759,-0.029,0.657,0,,,0,0,0,0,,
MTL,1123.48,0.061,0.038,0.25,0.832,-0.01,1.11,0,,,0,0,0,0,,
MUGHAL,115.33,0.259,0.01,0.704,1.789,-0.037,0.636,0,,,0,0,0,0,,
NETSOL,183.27,0.331,-0.359,0.921,2.585,-0.389,1.408,0,,,0,0,0,0,,
NML,101.09,0.208,-0.056,0.09,0.32,-0.179,0.616,0,,,0,0,0,0,,
NRL,560.95,0.016,-0.113,1.427,4.203,-0.126,0.808,0,,,0,0,0,0,,
NRSL,19.95,0.533,0.701,1.451,2.376,-0.108,2.212,0,,,0,0,0,0,,
OGDC,92.72,0.022,-0.103,-0.065,-0.178,-0.187,2.77,0,,,0,0,0,0,,
PAEL,36.05,0.158,-0.03,0.025,0.503,-0.149,0.626,0,,,0,0,0,0,,
PICT,170.36,0.104,0.129,-0.057,0.013,-0.337,0.907,0,,,0,0,0,0,,
PKGS,535.0,0.106,0.081,-0.006,0.58,-0.114,2.015,0,,,0,1,0,0,,
POWER,10.09,0.196,-0.013,0.051,0.643,-0.145,0.853,0,,,0,0,0,0,,
PPL,90.07,0.082,-0.009,-0.023,-0.068,-0.141,1.011,0,,,0,0,0,0,,
PREMA,22.67,0.414,0.239,0.328,0.421,0.0,2.212,2,,,0,1,0,0,,
PSO,232.79,0.052,-0.025,0.142,0.467,-0.102,1.246,0,,,0,0,0,0,,
PTC,13.84,0.506,0.585,0.504,0.626,0.0,2.963,1,,,0,0,0,0,,
SAZEW,178.4,0.111,-0.046,0.103,0.484,-0.128,0.737,0,,,0,1,0,0,,
SEARL,256.98,0.116,-0.043,0.068,0.323,-0.089,0.936,0,,,0,1,0,0,,
SNGP,48.35,0.257,0.137,0.114,-0.153,-0.288,2.023,0,,,0,0,0,0,,
SSGC,14.81,0.226,0.067,0.02,0.083,-0.217,2.196,0,,,1,0,0,0,,
STCL,34.89,0.422,0.423,0.847,2.978,0.0,0.906,2,,,0,0,0,0,,
STPL,17.2,0.27,-0.024,0.055,0.788,-0.227,1.878,0,,,0,0,0,0,,
UNITY,49.36,0.411,0.642,0.813,2.765,0.0,1.185,0,2021-03-31,,0,2,0,0,,
WAFI,179.21,0.189,-0.054,-0.015,0.317,-0.16,1.145,0,,,0,0,0,0,,
WAVES,26.82,0.336,0.088,-0.029,0.385,-0.14,2.503,1,,,0,0,0,0,,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2021-05-17,RMPL,material_info,Material Information
2021-05-17,PKGS,material_info,Disclosure of Material Information
2021-05-17,BAHL,material_info,BAHL - Disclosure of Material Information
2021-05-17,TPLP,material_info,Disclosure of Material Information
2021-05-17,DNCC,material_info,Material Information
2021-05-17,ANL,material_info,Material Information
2021-05-18,SAZEW,material_info,Material Information
2021-05-18,WYETH,material_info,Disclosure of Material Information- De Listing of Wyeth Pakistan Limited
2021-05-18,MRNS,material_info,Material Information
2021-05-20,TREET,material_info,Material Information REVOKED
2021-05-20,FTMM,material_info,Material Information
2021-05-21,WYETH,material_info,Material Information
2021-05-21,RUPL,material_info,Disclosure of Material Information
2021-05-24,KAPCO,material_info,Disclosure of Material Information
2021-05-24,BIPL,material_info,Disclosure of Material Informaton
2021-05-25,TELE,material_info,Material Information
2021-05-25,HCAR,financial_result,"Financial Results for the year ended March 31, 2021"
2021-05-27,BWCL,material_info,Material Information
2021-05-27,AVN,material_info,Material Information
2021-05-28,BNL,material_info,Material Information
2021-05-28,HSM,material_info,Material Information
2021-05-31,SYS,material_info,Material Information
2021-05-31,SERF,material_info,MATERIAL INFORMATION
2021-05-31,PECO,material_info,PECO | Pakistan Engineering Company Limited - Material Information
2021-05-31,ADMM,material_info,Material Information
2021-05-31,FDIBL,material_info,Material Information
2021-05-31,TREET,material_info,Material Information
2021-06-02,MODAM,material_info,Material Information /Adoption of Strategic Business Plans
2021-06-02,SPWL,material_info,Material information REVOKED
2021-06-02,SPWL,material_info,Material information
2021-06-03,JSGCL,material_info,Material Information
2021-06-03,TREET,material_info,Material Information
2021-06-03,PINL,material_info,Material Information
2021-06-04,GGL,material_info,MATERIAL INFORMATION - GHANI GLOBAL HOLDINGS LIMITED
2021-06-04,PREMA,material_info,Material Information
2021-06-04,ICIBL,material_info,MATERIAL INFORMATION-CLARIFICATION
2021-06-04,SEARL,material_info,Material Information
2021-06-04,ANL,material_info,Material Information
2021-06-04,MTIL,material_info,Material Information
2021-06-07,KAPCO,material_info,Disclosure of Material Information
2021-06-07,SPEL,material_info,Material Information
2021-06-07,UNITY,material_info,Material Information
2021-06-07,JDWS,material_info,Material Information
2021-06-07,KOHE,material_info,Material Information
2021-06-07,EFGH,material_info,Material Information
2021-06-07,HCAR,financial_result,Transmission of Annual Report for the Year ended 2021-03-31
2021-06-08,LPL,material_info,MATERIAL INFORMATION
2021-06-08,PKGP,material_info,MATERIAL INFORMATION
2021-06-08,WTL,material_info,Material Information
2021-06-08,SGF,material_info,Material Information
2021-06-08,SRVI,material_info,Material Information
2021-06-08,DCR,material_info,DISCLOSURE OF MATERIAL INFORMATION
2021-06-08,SSGC,financial_result,DISCLOSURE - BOARD MEETING OTHER THAN FINANCIAL RESULTS
2021-06-09,SANSM,material_info,Material Information
2021-06-09,CPAL,material_info,Material Information
2021-06-10,IMAGE,material_info,Material Information
2021-06-10,RAVT,material_info,Material Information
2021-06-10,AKBL,material_info,Material Information
2021-06-11,DLL,material_info,Material Information
2021-06-11,JSBL,material_info,Material Information
2021-06-11,UNITY,material_info,Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-18.478,2021-06-10
investor_type,last_5_sessions,broker proprietary trading,-2.955,2021-06-10
investor_type,last_5_sessions,companies,5.038,2021-06-10
investor_type,last_5_sessions,foreign corporates,-7.03,2021-06-10
investor_type,last_5_sessions,foreign individual,0.04,2021-06-10
investor_type,last_5_sessions,individuals,18.761,2021-06-10
investor_type,last_5_sessions,insurance companies,-8.259,2021-06-10
investor_type,last_5_sessions,mutual funds,9.963,2021-06-10
investor_type,last_5_sessions,nbfc,-0.05,2021-06-10
investor_type,last_5_sessions,other organization,0.867,2021-06-10
investor_type,last_5_sessions,overseas pakistani,2.103,2021-06-10
sector,last_5_sessions,fipi | All other Sectors,0.888,2021-06-10
sector,last_5_sessions,fipi | Cement,3.321,2021-06-10
sector,last_5_sessions,fipi | Commercial Banks,-3.133,2021-06-10
sector,last_5_sessions,fipi | Fertilizer,0.318,2021-06-10
sector,last_5_sessions,fipi | Food and Personal Care Products,-0.349,2021-06-10
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-2.341,2021-06-10
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,-0.579,2021-06-10
sector,last_5_sessions,fipi | Power Generation and Distribution,-1.938,2021-06-10
sector,last_5_sessions,fipi | Technology and Communication,-0.253,2021-06-10
sector,last_5_sessions,fipi | Textile Composite,-0.821,2021-06-10
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-7.39,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Cement,-3.547,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,0.485,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-1.722,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-1.359,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.692,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.038,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,-5.593,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,-0.241,2021-06-10
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.159,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-4.132,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Cement,1.352,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,-0.134,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Debt Market,-0.0,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.271,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,2.344,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.218,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-1.127,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.113,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,-0.886,2021-06-10
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.539,2021-06-10
sector,last_5_sessions,lipi companies | All other Sectors,0.838,2021-06-10
sector,last_5_sessions,lipi companies | Cement,2.329,2021-06-10
sector,last_5_sessions,lipi companies | Commercial Banks,1.825,2021-06-10
sector,last_5_sessions,lipi companies | Fertilizer,-1.186,2021-06-10
sector,last_5_sessions,lipi companies | Food and Personal Care Products,-0.523,2021-06-10
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,1.61,2021-06-10
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,0.698,2021-06-10
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.84,2021-06-10
sector,last_5_sessions,lipi companies | Technology and Communication,0.536,2021-06-10
sector,last_5_sessions,lipi companies | Textile Composite,-0.249,2021-06-10
sector,last_5_sessions,lipi individuals | All other Sectors,1.573,2021-06-10
sector,last_5_sessions,lipi individuals | Cement,0.021,2021-06-10
sector,last_5_sessions,lipi individuals | Commercial Banks,-3.343,2021-06-10
sector,last_5_sessions,lipi individuals | Debt Market,0.174,2021-06-10
sector,last_5_sessions,lipi individuals | Fertilizer,1.646,2021-06-10
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,-1.435,2021-06-10
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,7.432,2021-06-10
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,4.407,2021-06-10
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,7.15,2021-06-10
sector,last_5_sessions,lipi individuals | Technology and Communication,-0.712,2021-06-10
sector,last_5_sessions,lipi individuals | Textile Composite,1.847,2021-06-10
sector,last_5_sessions,lipi insurance companies | All other Sectors,4.16,2021-06-10
sector,last_5_sessions,lipi insurance companies | Cement,-3.893,2021-06-10
sector,last_5_sessions,lipi insurance companies | Commercial Banks,2.382,2021-06-10
sector,last_5_sessions,lipi insurance companies | Fertilizer,0.567,2021-06-10
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,-0.104,2021-06-10
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-6.601,2021-06-10
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-3.215,2021-06-10
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,-0.391,2021-06-10
sector,last_5_sessions,lipi insurance companies | Technology and Communication,-0.268,2021-06-10
sector,last_5_sessions,lipi insurance companies | Textile Composite,-0.894,2021-06-10
sector,last_5_sessions,lipi mutual funds | All other Sectors,5.41,2021-06-10
sector,last_5_sessions,lipi mutual funds | Cement,0.821,2021-06-10
sector,last_5_sessions,lipi mutual funds | Commercial Banks,0.114,2021-06-10
sector,last_5_sessions,lipi mutual funds | Debt Market,0.233,2021-06-10
sector,last_5_sessions,lipi mutual funds | Fertilizer,0.139,2021-06-10
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,1.473,2021-06-10
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-0.505,2021-06-10
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.145,2021-06-10
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.332,2021-06-10
sector,last_5_sessions,lipi mutual funds | Technology and Communication,1.684,2021-06-10
sector,last_5_sessions,lipi mutual funds | Textile Composite,0.782,2021-06-10
sector,last_5_sessions,lipi nbfc | All other Sectors,-0.006,2021-06-10
sector,last_5_sessions,lipi nbfc | Cement,0.044,2021-06-10
sector,last_5_sessions,lipi nbfc | Commercial Banks,-0.018,2021-06-10
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,-0.006,2021-06-10
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.024,2021-06-10
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.004,2021-06-10
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.051,2021-06-10
sector,last_5_sessions,lipi nbfc | Technology and Communication,0.052,2021-06-10
sector,last_5_sessions,lipi nbfc | Textile Composite,-0.045,2021-06-10
sector,last_5_sessions,lipi other organization | All other Sectors,-1.34,2021-06-10
sector,last_5_sessions,lipi other organization | Cement,-0.449,2021-06-10
sector,last_5_sessions,lipi other organization | Commercial Banks,1.821,2021-06-10
sector,last_5_sessions,lipi other organization | Debt Market,-0.407,2021-06-10
sector,last_5_sessions,lipi other organization | Fertilizer,-0.032,2021-06-10
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,-0.039,2021-06-10
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.046,2021-06-10
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.371,2021-06-10
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,1.883,2021-06-10
sector,last_5_sessions,lipi other organization | Technology and Communication,0.089,2021-06-10
sector,last_5_sessions,lipi other organization | Textile Composite,-0.241,2021-06-10
investor_type,last_20_sessions,banks / dfi,-13.252,2021-06-10
investor_type,last_20_sessions,broker proprietary trading,1.813,2021-06-10
investor_type,last_20_sessions,companies,20.336,2021-06-10
investor_type,last_20_sessions,foreign corporates,-45.583,2021-06-10
investor_type,last_20_sessions,foreign individual,-2.146,2021-06-10
investor_type,last_20_sessions,individuals,47.969,2021-06-10
investor_type,last_20_sessions,insurance companies,-25.45,2021-06-10
investor_type,last_20_sessions,mutual funds,4.233,2021-06-10
investor_type,last_20_sessions,nbfc,0.131,2021-06-10
investor_type,last_20_sessions,other organization,17.54,2021-06-10
investor_type,last_20_sessions,overseas pakistani,-5.592,2021-06-10
sector,last_20_sessions,fipi | All other Sectors,-46.983,2021-06-10
sector,last_20_sessions,fipi | Cement,36.907,2021-06-10
sector,last_20_sessions,fipi | Commercial Banks,0.043,2021-06-10
sector,last_20_sessions,fipi | Fertilizer,-1.49,2021-06-10
sector,last_20_sessions,fipi | Food and Personal Care Products,0.624,2021-06-10
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-39.266,2021-06-10
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,-1.289,2021-06-10
sector,last_20_sessions,fipi | Power Generation and Distribution,-7.597,2021-06-10
sector,last_20_sessions,fipi | Technology and Communication,8.77,2021-06-10
sector,last_20_sessions,fipi | Textile Composite,-3.04,2021-06-10
sector,last_20_sessions,lipi banks / dfi | All other Sectors,-2.711,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Cement,-8.611,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,0.894,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Debt Market,-0.104,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-4.388,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,-2.222,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,6.769,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,1.379,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-5.202,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,1.5,2021-06-10
sector,last_20_sessions,lipi banks / dfi | Textile Composite,-0.555,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-8.229,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Cement,1.826,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,0.338,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.001,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,0.656,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,4.38,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,4.309,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,1.049,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.114,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-2.422,2021-06-10
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,0.022,2021-06-10
sector,last_20_sessions,lipi companies | All other Sectors,22.798,2021-06-10
sector,last_20_sessions,lipi companies | Cement,-3.224,2021-06-10
sector,last_20_sessions,lipi companies | Commercial Banks,-6.194,2021-06-10
sector,last_20_sessions,lipi companies | Fertilizer,1.292,2021-06-10
sector,last_20_sessions,lipi companies | Food and Personal Care Products,-3.045,2021-06-10
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,6.798,2021-06-10
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,0.599,2021-06-10
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-1.675,2021-06-10
sector,last_20_sessions,lipi companies | Technology and Communication,0.385,2021-06-10
sector,last_20_sessions,lipi companies | Textile Composite,2.603,2021-06-10
sector,last_20_sessions,lipi individuals | All other Sectors,6.57,2021-06-10
sector,last_20_sessions,lipi individuals | Cement,-6.148,2021-06-10
sector,last_20_sessions,lipi individuals | Commercial Banks,0.185,2021-06-10
sector,last_20_sessions,lipi individuals | Debt Market,0.386,2021-06-10
sector,last_20_sessions,lipi individuals | Fertilizer,6.968,2021-06-10
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,3.421,2021-06-10
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,21.872,2021-06-10
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,8.908,2021-06-10
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,13.935,2021-06-10
sector,last_20_sessions,lipi individuals | Technology and Communication,-8.915,2021-06-10
sector,last_20_sessions,lipi individuals | Textile Composite,0.787,2021-06-10
sector,last_20_sessions,lipi insurance companies | All other Sectors,16.863,2021-06-10
sector,last_20_sessions,lipi insurance companies | Cement,-18.956,2021-06-10
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-7.972,2021-06-10
sector,last_20_sessions,lipi insurance companies | Debt Market,0.007,2021-06-10
sector,last_20_sessions,lipi insurance companies | Fertilizer,0.924,2021-06-10
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,-0.284,2021-06-10
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-12.364,2021-06-10
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-6.754,2021-06-10
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,0.305,2021-06-10
sector,last_20_sessions,lipi insurance companies | Technology and Communication,2.439,2021-06-10
sector,last_20_sessions,lipi insurance companies | Textile Composite,0.341,2021-06-10
sector,last_20_sessions,lipi mutual funds | All other Sectors,11.352,2021-06-10
sector,last_20_sessions,lipi mutual funds | Cement,-1.287,2021-06-10
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-6.422,2021-06-10
sector,last_20_sessions,lipi mutual funds | Debt Market,-0.113,2021-06-10
sector,last_20_sessions,lipi mutual funds | Fertilizer,-3.849,2021-06-10
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,-2.372,2021-06-10
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,10.428,2021-06-10
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,1.832,2021-06-10
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-4.502,2021-06-10
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-1.79,2021-06-10
sector,last_20_sessions,lipi mutual funds | Textile Composite,0.956,2021-06-10
sector,last_20_sessions,lipi nbfc | All other Sectors,0.048,2021-06-10
sector,last_20_sessions,lipi nbfc | Cement,0.105,2021-06-10
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.079,2021-06-10
sector,last_20_sessions,lipi nbfc | Fertilizer,-0.003,2021-06-10
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,-0.014,2021-06-10
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.057,2021-06-10
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.029,2021-06-10
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.003,2021-06-10
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.039,2021-06-10
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.055,2021-06-10
sector,last_20_sessions,lipi other organization | All other Sectors,0.29,2021-06-10
sector,last_20_sessions,lipi other organization | Cement,-0.613,2021-06-10
sector,last_20_sessions,lipi other organization | Commercial Banks,19.208,2021-06-10
sector,last_20_sessions,lipi other organization | Debt Market,-0.174,2021-06-10
sector,last_20_sessions,lipi other organization | Fertilizer,-0.111,2021-06-10
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-0.487,2021-06-10
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,1.396,2021-06-10
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-5.753,2021-06-10
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,4.848,2021-06-10
sector,last_20_sessions,lipi other organization | Technology and Communication,-0.005,2021-06-10
sector,last_20_sessions,lipi other organization | Textile Composite,-1.06,2021-06-10

=== FILE: calendar.md ===
# Calendar as of 2021-06-11

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2021-05-17 HCAR: Board of Directors Meeting & Close Period
- 2021-05-19 FLYNG: Board Meeting other than Financial Results
- 2021-05-21 KEL: Board Meeting Other Than Financial Results
- 2021-05-24 PTC: Board Meeting other than Financial Results
- 2021-05-31 KEL: Board Meeting Other Than Financial Results
- 2021-05-31 SSGC: Board Meeting Other Than Financial Results
- 2021-05-31 SEARL: Board Meeting Other Than Financial Results
- 2021-06-01 IMAGE: Board Meeting Other Than Financial Results REVOKED
- 2021-06-01 IMAGE: Board Meeting Other Than Financial Results
- 2021-06-04 SSGC: Rescheduled - Board Meeting Other than Financial Results
- 2021-06-10 UNITY: Board Meeting Other than Financial Results
- 2021-06-10 SEARL: Short Notice (emergency) Board Meeting Other Than Financial Results

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
