# Replay bundle, close of 2023-05-05

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
# Market as of 2023-05-05 close (public information only)

- KSE100: 42,242 on 2023-05-05; 1m +6.0%, 3m +5.9%, 6m +1.0%, 12m -8.3%
- KMI All Share: 20,209 on 2023-05-05; 1m +6.3%, 3m +4.5%, 6m -3.4%, 12m -11.2%
- Policy rate 21.0%; last MPC decision 2023-04-04: hike (+100bp)
- 6M T-bill cutoff 21.96% (auction 2023-05-03); 3M 22.00%, 12M 22.00%
- CPI YoY 36.42% for 2023-04 (published by 2023-05-03); three months earlier (2023-01) 27.56%
- Brent: 75.85 USD/bbl on 2023-05-05; 3-month change -3.8%
- USD/PKR: 283.71  on 2023-05-05; 3-month change +3.9%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.96pp (market pricing hikes); CPI rising over 3 months (+8.9pp)
- Next MPC: see SBP calendar

Session date used: 2023-05-05. Liquid KMI names: 45 (membership KMI_ALL_derived_2023-01-12.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.0492,-0.0252,-0.1841,0,0
E&P,3,0.0316,-0.0184,0.1513,0,0
OMC,4,-0.0025,-0.1322,-0.2453,0,0
Power,5,-0.0037,-0.0379,-0.0838,1,1
Fertilizer,4,0.048,0.0408,0.0069,0,0
Cement,16,0.0985,0.1689,-0.064,0,1
Steel & engineering,10,0.0218,0.0884,-0.1595,0,0
Autos,12,0.0106,0.022,-0.1465,0,1
Tech & telecom,8,0.0458,0.0439,-0.1723,1,1
Islamic banks & fin.,8,0.0919,0.0383,-0.057,0,0
Pharma,13,0.0046,0.0311,-0.1819,0,0
Textiles,23,-0.0004,0.0705,-0.0043,0,0
Food & staples,13,0.1065,0.0618,-0.0736,0,0
Chemicals,18,0.0184,0.0404,-0.081,0,0
"Glass, packaging, paper",12,0.053,0.1309,-0.1214,0,0
Gas utilities & misc,10,0.0253,-0.072,-0.0914,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ATRL,170.0,0.006,-0.015,-0.024,0.064,-0.052,0.741,0,2023-03-31,2.222,2,1,0,0,1.447,0.057
AVN,64.44,-0.004,0.008,-0.194,-0.235,-0.257,0.64,0,2023-03-31,-0.049,3,2,0,0,,
BIPL,15.66,0.623,0.41,0.603,0.342,-0.021,1.095,5,2023-03-31,2.447,2,1,0,0,,
CHCC,121.92,0.09,0.292,-0.024,-0.07,-0.066,0.949,0,2023-03-31,0.195,2,0,0,0,4.057,0.032
CNERGY,3.48,-0.0,-0.103,-0.267,-0.455,-0.488,0.656,0,,,2,0,0,0,5.945,
CPHL,25.41,-0.01,0.136,-0.108,-0.234,-0.267,0.874,0,2023-03-31,-0.554,5,0,0,0,11.407,
DGKC,49.53,0.167,0.219,-0.09,-0.287,-0.277,1.164,0,2023-03-31,-0.222,2,0,0,0,8.664,0.016
DOL,26.25,-0.013,0.309,0.262,0.658,-0.071,1.712,0,,,2,1,0,0,,
EFERT,86.95,0.048,0.101,0.076,-0.122,-0.139,0.793,0,2023-03-31,-0.201,2,0,0,0,6.416,0.176
EPCL,45.59,0.066,0.047,-0.08,-0.375,-0.4,1.074,0,2023-03-31,-0.75,2,0,0,0,3.422,0.295
FCCL,12.28,0.017,0.117,-0.154,-0.281,-0.28,0.757,0,2023-03-31,0.203,2,0,0,0,2.749,
GGL,11.07,0.041,0.132,-0.305,-0.448,-0.452,0.63,0,2023-03-31,0.207,2,0,0,0,8.853,
HCAR,109.51,-0.052,-0.161,-0.334,-0.453,-0.438,0.289,0,2022-12-31,0.82,0,2,0,0,11.79,0.034
ILP,50.31,0.043,-0.036,-0.16,-0.3,-0.3,0.968,0,2023-03-31,3.196,2,0,0,0,4.434,0.066
INIL,78.5,0.063,0.241,-0.19,-0.344,-0.335,0.545,0,2023-03-31,1.241,2,0,0,0,5.642,0.077
ISL,44.19,0.049,0.119,-0.153,-0.31,-0.302,1.573,0,2023-03-31,0.338,2,0,0,0,4.771,0.11
KEL,1.99,-0.039,-0.07,-0.297,-0.328,-0.466,0.669,0,2023-03-31,,2,0,0,0,9.912,
KOHC,151.87,0.092,0.147,-0.064,-0.076,-0.092,0.834,0,2023-03-31,-0.012,2,0,0,0,5.202,
LUCK,455.4,0.144,0.152,-0.075,-0.223,-0.212,0.843,1,2023-03-31,1.84,2,1,0,0,5.032,
MARI,1574.47,0.048,0.072,-0.063,-0.091,-0.121,0.836,0,2022-12-31,0.492,2,1,0,0,7.019,0.071
MEBL,98.33,0.079,0.141,-0.011,-0.151,-0.154,0.972,0,2023-03-31,0.682,2,0,0,0,3.964,0.082
MLCF,28.62,0.107,0.377,0.041,-0.179,-0.171,1.146,0,,,2,0,0,0,6.598,
MTL,518.0,-0.048,0.112,-0.122,-0.264,-0.363,0.527,0,2023-03-31,-0.092,4,0,0,0,15.755,0.074
MUGHAL,52.06,0.067,0.155,-0.174,-0.378,-0.364,0.931,0,2023-03-31,0.556,3,0,0,0,3.575,0.052
NETSOL,77.65,0.049,-0.067,-0.291,-0.255,-0.358,0.471,0,2023-03-31,8.261,2,0,0,0,10.272,
NML,56.53,0.07,0.078,-0.086,-0.337,-0.322,0.706,0,2023-03-31,-0.115,2,0,0,0,2.112,0.054
NRL,157.09,0.051,-0.012,-0.258,-0.393,-0.426,0.624,0,2023-03-31,-1.481,2,0,0,0,2.225,0.059
OGDC,86.17,0.028,0.025,0.278,0.1,-0.166,0.604,0,2023-03-31,0.497,2,0,0,0,2.529,0.092
PAEL,10.67,0.008,-0.01,-0.323,-0.429,-0.416,0.695,0,2023-03-31,-0.951,3,0,0,0,10.818,
PIOC,79.86,0.16,0.592,0.119,0.137,-0.004,0.926,1,2023-03-31,0.953,2,0,0,0,13.048,
PPL,64.77,0.016,-0.151,0.236,-0.153,-0.228,0.62,0,2023-03-31,0.609,2,0,0,0,3.38,0.03
PRL,14.0,0.142,0.025,-0.184,-0.17,-0.297,1.023,0,2023-03-31,-0.68,2,0,0,0,0.896,
PSO,113.96,-0.009,-0.125,-0.213,-0.333,-0.409,0.426,0,2023-03-31,-0.653,2,0,0,0,0.884,0.058
SAZEW,51.31,0.135,0.069,-0.073,-0.368,-0.351,1.297,1,2023-03-31,16.951,2,0,0,0,31.865,
SEARL,52.41,0.002,0.01,-0.306,-0.439,-0.432,0.749,0,2023-03-31,-0.664,2,1,0,0,14.467,
SNGP,43.42,0.111,0.063,0.247,0.556,-0.084,0.669,0,2023-03-31,-0.104,1,0,0,0,2.093,0.117
SSGC,10.88,0.126,0.028,0.169,0.186,-0.106,0.498,0,2021-06-30,,1,0,0,0,,
SYS,442.26,-0.043,-0.022,-0.02,0.09,-0.141,0.913,0,2023-03-31,2.069,4,0,0,0,20.325,0.011
TELE,7.64,0.001,0.302,-0.247,-0.462,-0.47,1.232,0,2021-06-30,,2,1,0,0,8.192,
TGL,74.06,0.064,0.281,-0.089,-0.297,-0.318,0.698,0,2023-03-31,-0.258,2,2,0,0,3.453,0.019
TPLP,14.06,-0.008,-0.099,-0.21,-0.351,-0.364,0.744,0,,,2,0,0,0,,
TREET,17.85,0.047,0.113,-0.198,-0.5,-0.49,1.066,0,2023-03-31,,2,0,0,0,,
UNITY,13.25,0.013,-0.04,-0.355,-0.474,-0.462,0.52,0,2023-03-31,-1.133,2,0,0,0,10.986,
WAFI,74.42,-0.059,-0.291,-0.439,-0.37,-0.459,1.035,0,,,0,0,0,0,,0.028
WAVES,7.72,0.08,0.039,-0.278,-0.501,-0.488,0.848,0,2022-12-31,,3,0,0,0,13.769,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2023-04-27,DADX,material_info,Material Information
2023-04-27,BIPL,material_info,Disclosure of Material Information
2023-04-27,ARPL,material_info,Material Information
2023-04-27,JSCL,material_info,Material Information
2023-04-27,JSGCL,material_info,Material Information
2023-04-27,SAPT,material_info,Material Information
2023-04-27,JSIL,material_info,Material Information
2023-04-28,HCAR,material_info,Material Information
2023-04-28,CLVL,material_info,Material Information
2023-04-28,LOADS,material_info,Material Information
2023-04-28,INDU,material_info,Disclosure of material information
2023-04-28,DATM,material_info,Material Information-Approval of the Scheme REVOKED
2023-04-28,SEARL,material_info,Material Information
2023-04-28,DATM,material_info,Material Information-Approval of the Scheme
2023-04-28,PKGS,material_info,Disclosure of Material Information - Acquisition of Substantial Shareholdin
2023-04-28,AHCL,material_info,Price Sensitive / Material Information Disclosure
2023-04-28,AHL,material_info,Price Sensitive / Material Information Disclosure
2023-04-28,SMBL,material_info,Disclosure of Material Information
2023-04-28,SAPL,material_info,Disclosure of Material Information
2023-04-28,LCI,material_info,Material Information
2023-05-02,UDPL,material_info,Material Information
2023-05-02,LUCK,material_info,Material Information - 2nd Buy-Back of Shares
2023-05-02,HBL,material_info,Material Information
2023-05-02,IGIHL,material_info,Material Information
2023-05-02,SILK,material_info,Material Information
2023-05-02,LOTCHEM,material_info,Material Information Resumption of Plant Operations
2023-05-02,DOL,material_info,Material Information
2023-05-02,MCBAH,material_info,Material Information
2023-05-02,AGIL,material_info,Material Information
2023-05-02,DATM,material_info,Material Information-Decision of Board Meeting
2023-05-02,ZIL,material_info,Material Information
2023-05-03,ATRL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2023-05-03,BRR,material_info,MATERIAL INFORMATION
2023-05-04,GHNL,material_info,Material Information
2023-05-04,ELCM,material_info,Material Information
2023-05-04,SIBL,material_info,Material Information
2023-05-04,BNWM,material_info,DISCLOSURE OF MATERIAL INFORMATION FOR EXTENSION OF PRODUCTION PROCESS CLOS

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,1.708,2023-05-04
investor_type,last_5_sessions,broker proprietary trading,-0.1,2023-05-04
investor_type,last_5_sessions,companies,15.624,2023-05-04
investor_type,last_5_sessions,foreign corporates,-21.938,2023-05-04
investor_type,last_5_sessions,foreign individual,-0.023,2023-05-04
investor_type,last_5_sessions,individuals,7.445,2023-05-04
investor_type,last_5_sessions,insurance companies,-0.913,2023-05-04
investor_type,last_5_sessions,mutual funds,-2.881,2023-05-04
investor_type,last_5_sessions,nbfc,1.499,2023-05-04
investor_type,last_5_sessions,other organization,-1.415,2023-05-04
investor_type,last_5_sessions,overseas pakistani,0.994,2023-05-04
sector,last_5_sessions,fipi | All other Sectors,-17.109,2023-05-04
sector,last_5_sessions,fipi | Cement,-0.204,2023-05-04
sector,last_5_sessions,fipi | Commercial Banks,4.595,2023-05-04
sector,last_5_sessions,fipi | Fertilizer,0.294,2023-05-04
sector,last_5_sessions,fipi | Food and Personal Care Products,-8.999,2023-05-04
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,0.048,2023-05-04
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,0.036,2023-05-04
sector,last_5_sessions,fipi | Power Generation and Distribution,0.382,2023-05-04
sector,last_5_sessions,fipi | Technology and Communication,0.026,2023-05-04
sector,last_5_sessions,fipi | Textile Composite,-0.035,2023-05-04
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-0.07,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Cement,-0.165,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,-0.854,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Fertilizer,0.77,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,1.921,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.146,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.114,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,-0.232,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,0.151,2023-05-04
sector,last_5_sessions,lipi banks / dfi | Textile Composite,-0.073,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,0.421,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Cement,-0.402,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,-0.702,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.019,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.545,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.041,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.05,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.032,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,0.025,2023-05-04
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,0.016,2023-05-04
sector,last_5_sessions,lipi companies | All other Sectors,15.084,2023-05-04
sector,last_5_sessions,lipi companies | Cement,4.022,2023-05-04
sector,last_5_sessions,lipi companies | Commercial Banks,-1.932,2023-05-04
sector,last_5_sessions,lipi companies | Fertilizer,-0.851,2023-05-04
sector,last_5_sessions,lipi companies | Food and Personal Care Products,0.318,2023-05-04
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,0.572,2023-05-04
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,-0.055,2023-05-04
sector,last_5_sessions,lipi companies | Power Generation and Distribution,0.175,2023-05-04
sector,last_5_sessions,lipi companies | Technology and Communication,-1.996,2023-05-04
sector,last_5_sessions,lipi companies | Textile Composite,0.287,2023-05-04
sector,last_5_sessions,lipi individuals | All other Sectors,2.835,2023-05-04
sector,last_5_sessions,lipi individuals | Cement,-2.225,2023-05-04
sector,last_5_sessions,lipi individuals | Commercial Banks,0.965,2023-05-04
sector,last_5_sessions,lipi individuals | Fertilizer,-0.115,2023-05-04
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,1.422,2023-05-04
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,1.376,2023-05-04
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,0.125,2023-05-04
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.237,2023-05-04
sector,last_5_sessions,lipi individuals | Technology and Communication,2.813,2023-05-04
sector,last_5_sessions,lipi individuals | Textile Composite,0.011,2023-05-04
sector,last_5_sessions,lipi insurance companies | All other Sectors,-0.178,2023-05-04
sector,last_5_sessions,lipi insurance companies | Cement,-0.955,2023-05-04
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-0.252,2023-05-04
sector,last_5_sessions,lipi insurance companies | Fertilizer,-0.241,2023-05-04
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.789,2023-05-04
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-0.199,2023-05-04
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.072,2023-05-04
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,-0.021,2023-05-04
sector,last_5_sessions,lipi insurance companies | Technology and Communication,0.078,2023-05-04
sector,last_5_sessions,lipi insurance companies | Textile Composite,-0.007,2023-05-04
sector,last_5_sessions,lipi mutual funds | All other Sectors,-0.819,2023-05-04
sector,last_5_sessions,lipi mutual funds | Cement,0.065,2023-05-04
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-1.501,2023-05-04
sector,last_5_sessions,lipi mutual funds | Fertilizer,0.287,2023-05-04
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,2.465,2023-05-04
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-1.816,2023-05-04
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.162,2023-05-04
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.549,2023-05-04
sector,last_5_sessions,lipi mutual funds | Technology and Communication,-0.977,2023-05-04
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.198,2023-05-04
sector,last_5_sessions,lipi nbfc | All other Sectors,0.003,2023-05-04
sector,last_5_sessions,lipi nbfc | Cement,0.001,2023-05-04
sector,last_5_sessions,lipi nbfc | Commercial Banks,0.012,2023-05-04
sector,last_5_sessions,lipi nbfc | Fertilizer,0.01,2023-05-04
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,1.507,2023-05-04
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.014,2023-05-04
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.001,2023-05-04
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.016,2023-05-04
sector,last_5_sessions,lipi nbfc | Technology and Communication,-0.003,2023-05-04
sector,last_5_sessions,lipi nbfc | Textile Composite,0.0,2023-05-04
sector,last_5_sessions,lipi other organization | All other Sectors,-0.167,2023-05-04
sector,last_5_sessions,lipi other organization | Cement,-0.137,2023-05-04
sector,last_5_sessions,lipi other organization | Commercial Banks,-0.331,2023-05-04
sector,last_5_sessions,lipi other organization | Fertilizer,-0.172,2023-05-04
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,0.032,2023-05-04
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.072,2023-05-04
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.505,2023-05-04
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.055,2023-05-04
sector,last_5_sessions,lipi other organization | Technology and Communication,-0.117,2023-05-04
sector,last_5_sessions,lipi other organization | Textile Composite,-0.001,2023-05-04
investor_type,last_20_sessions,banks / dfi,10.628,2023-05-04
investor_type,last_20_sessions,broker proprietary trading,-1.631,2023-05-04
investor_type,last_20_sessions,companies,9.994,2023-05-04
investor_type,last_20_sessions,foreign corporates,-16.649,2023-05-04
investor_type,last_20_sessions,foreign individual,0.058,2023-05-04
investor_type,last_20_sessions,individuals,13.006,2023-05-04
investor_type,last_20_sessions,insurance companies,-10.243,2023-05-04
investor_type,last_20_sessions,mutual funds,-9.893,2023-05-04
investor_type,last_20_sessions,nbfc,1.436,2023-05-04
investor_type,last_20_sessions,other organization,1.166,2023-05-04
investor_type,last_20_sessions,overseas pakistani,2.127,2023-05-04
sector,last_20_sessions,fipi | All other Sectors,-16.595,2023-05-04
sector,last_20_sessions,fipi | Cement,1.047,2023-05-04
sector,last_20_sessions,fipi | Commercial Banks,6.092,2023-05-04
sector,last_20_sessions,fipi | Fertilizer,-0.331,2023-05-04
sector,last_20_sessions,fipi | Food and Personal Care Products,-8.896,2023-05-04
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,3.805,2023-05-04
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,-0.061,2023-05-04
sector,last_20_sessions,fipi | Power Generation and Distribution,0.275,2023-05-04
sector,last_20_sessions,fipi | Technology and Communication,0.088,2023-05-04
sector,last_20_sessions,fipi | Textile Composite,0.112,2023-05-04
sector,last_20_sessions,lipi banks / dfi | All other Sectors,1.544,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Cement,0.19,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,1.974,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Debt Market,0.835,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Fertilizer,2.212,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,1.968,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.762,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.823,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-0.343,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,0.613,2023-05-04
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.05,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,0.164,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Cement,-0.265,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,-0.73,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.189,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-0.271,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.712,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.762,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.062,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.236,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,0.002,2023-05-04
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,0.006,2023-05-04
sector,last_20_sessions,lipi companies | All other Sectors,12.777,2023-05-04
sector,last_20_sessions,lipi companies | Cement,3.518,2023-05-04
sector,last_20_sessions,lipi companies | Commercial Banks,-1.995,2023-05-04
sector,last_20_sessions,lipi companies | Debt Market,-1.008,2023-05-04
sector,last_20_sessions,lipi companies | Fertilizer,-1.393,2023-05-04
sector,last_20_sessions,lipi companies | Food and Personal Care Products,0.439,2023-05-04
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,-0.11,2023-05-04
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,-0.341,2023-05-04
sector,last_20_sessions,lipi companies | Power Generation and Distribution,0.277,2023-05-04
sector,last_20_sessions,lipi companies | Technology and Communication,-2.366,2023-05-04
sector,last_20_sessions,lipi companies | Textile Composite,0.198,2023-05-04
sector,last_20_sessions,lipi individuals | All other Sectors,3.986,2023-05-04
sector,last_20_sessions,lipi individuals | Cement,-1.961,2023-05-04
sector,last_20_sessions,lipi individuals | Commercial Banks,2.026,2023-05-04
sector,last_20_sessions,lipi individuals | Debt Market,-0.004,2023-05-04
sector,last_20_sessions,lipi individuals | Fertilizer,0.926,2023-05-04
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,1.745,2023-05-04
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,1.931,2023-05-04
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.201,2023-05-04
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,0.9,2023-05-04
sector,last_20_sessions,lipi individuals | Technology and Communication,3.046,2023-05-04
sector,last_20_sessions,lipi individuals | Textile Composite,0.612,2023-05-04
sector,last_20_sessions,lipi insurance companies | All other Sectors,-0.749,2023-05-04
sector,last_20_sessions,lipi insurance companies | Cement,-1.77,2023-05-04
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-3.115,2023-05-04
sector,last_20_sessions,lipi insurance companies | Debt Market,-0.157,2023-05-04
sector,last_20_sessions,lipi insurance companies | Fertilizer,-1.124,2023-05-04
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,-0.034,2023-05-04
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-2.889,2023-05-04
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.298,2023-05-04
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,-0.27,2023-05-04
sector,last_20_sessions,lipi insurance companies | Technology and Communication,0.041,2023-05-04
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.473,2023-05-04
sector,last_20_sessions,lipi mutual funds | All other Sectors,-0.99,2023-05-04
sector,last_20_sessions,lipi mutual funds | Cement,-0.886,2023-05-04
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-4.513,2023-05-04
sector,last_20_sessions,lipi mutual funds | Debt Market,-1.204,2023-05-04
sector,last_20_sessions,lipi mutual funds | Fertilizer,0.295,2023-05-04
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,2.452,2023-05-04
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-2.587,2023-05-04
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.056,2023-05-04
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-0.747,2023-05-04
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-1.266,2023-05-04
sector,last_20_sessions,lipi mutual funds | Textile Composite,-0.503,2023-05-04
sector,last_20_sessions,lipi nbfc | All other Sectors,-0.018,2023-05-04
sector,last_20_sessions,lipi nbfc | Cement,0.002,2023-05-04
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.007,2023-05-04
sector,last_20_sessions,lipi nbfc | Debt Market,-0.035,2023-05-04
sector,last_20_sessions,lipi nbfc | Fertilizer,0.02,2023-05-04
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,1.51,2023-05-04
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.014,2023-05-04
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.0,2023-05-04
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,-0.016,2023-05-04
sector,last_20_sessions,lipi nbfc | Technology and Communication,-0.003,2023-05-04
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.002,2023-05-04
sector,last_20_sessions,lipi other organization | All other Sectors,-0.12,2023-05-04
sector,last_20_sessions,lipi other organization | Cement,0.125,2023-05-04
sector,last_20_sessions,lipi other organization | Commercial Banks,0.268,2023-05-04
sector,last_20_sessions,lipi other organization | Debt Market,1.762,2023-05-04
sector,last_20_sessions,lipi other organization | Fertilizer,-0.333,2023-05-04
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,0.104,2023-05-04
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.136,2023-05-04
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.512,2023-05-04
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,0.161,2023-05-04
sector,last_20_sessions,lipi other organization | Technology and Communication,-0.154,2023-05-04
sector,last_20_sessions,lipi other organization | Textile Composite,0.001,2023-05-04

=== FILE: calendar.md ===
# Calendar as of 2023-05-05

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2023-04-06 SSGC: Board Meeting
- 2023-04-07 MEBL: NOTICE OF BOARD MEETING AND CLOSED PERIOD
- 2023-04-07 ISL: Board Meeting
- 2023-04-10 DOL: BOARD MEETING
- 2023-04-10 SAZEW: Board Meeting
- 2023-04-10 MLCF: Board Meeting 17.04.2023
- 2023-04-10 ILP: Notice of Board Meeting for the Third Quarter ended March 31, 2023 / Closed Period
- 2023-04-11 INIL: Board Meeting
- 2023-04-11 PRL: Board Meeting
- 2023-04-11 AVN: Board Meeting Other Than Financial Results REVOKED
- 2023-04-11 AVN: Board Meeting Other Than Financial Results
- 2023-04-11 DGKC: Board Meeting
- 2023-04-11 KEL: Board Meeting Other Than Financial Results
- 2023-04-13 NRL: Board Meeting
- 2023-04-13 MTL: Board Meeting
- 2023-04-17 OGDC: Board Meeting and Closed Period
- 2023-04-17 CHCC: Board Meeting
- 2023-04-18 PPL: Meeting of the Board of Directors and Closed Period
- 2023-04-18 MUGHAL: Notice of Board Meeting - QIII - FY 2023
- 2023-04-18 TELE: Board Meeting
- 2023-04-19 TPLP: Board Meeting
- 2023-04-19 NML: Board Meeting
- 2023-04-19 KOHC: Board Meeting
- 2023-04-19 GGL: Board Meeting - GHANI GLOBAL HOLDINGS LIMITED
- 2023-04-19 TGL: Board Meeting
- 2023-04-19 PSO: Board Meeting
- 2023-04-19 PIOC: Board Meeting
- 2023-04-19 NETSOL: Board Meeting
- 2023-04-19 BIPL: Board Meeting - BankIslami Pakistan Limited
- 2023-04-19 TREET: Board Meeting of Treet Corporation Limited
- 2023-04-19 AVN: Board Meeting
- 2023-04-20 UNITY: Board Meeting
- 2023-04-20 SEARL: Board Meeting
- 2023-04-20 SYS: Board Meeting
- 2023-04-20 MARI: Notice of Board of Directors Meeting
- 2023-04-20 CPHL: Board Meeting
- 2023-04-20 PAEL: Board Meeting for the 1st Quarter ended March 31, 2023 (Un-Audited)
- 2023-04-20 LUCK: BOARD MEETING
- 2023-04-20 KEL: Board Meeting
- 2023-04-20 CNERGY: Board Meeting and Closed Period
- 2023-04-27 WAVES: Board Meeting - Annual Accounts for the year ended 31 December 2022

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
| 15 | Rs170bn mini-budget | 10 Feb 2023 | outcome not shown |
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
