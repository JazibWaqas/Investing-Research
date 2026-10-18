# Replay bundle, close of 2025-04-18

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
# Market as of 2025-04-18 close (public information only)

- KSE100: 117,316 on 2025-04-18; 1m +1.5%, 3m +2.2%, 6m +36.1%, 12m +71.5%
- KMI All Share: 50,991 on 2025-04-18; 1m +2.0%, 3m +2.1%, 6m +35.3%, 12m +59.1%
- Policy rate 12.0%; last MPC decision 2025-03-10: hold (+0bp)
- 6M T-bill cutoff 11.99% (auction 2025-04-16); 3M 12.01%, 12M 12.01%
- CPI YoY 0.72% for 2025-03 (published by 2025-04-03); three months earlier (2024-12) 4.08%
- Brent: 69.33 USD/bbl on 2025-04-17; 3-month change -16.5%
- USD/PKR: 280.65  on 2025-04-18; 3-month change +0.7%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate -0.01pp (market near policy rate); CPI falling over 3 months (-3.4pp)
- Next MPC: see SBP calendar

Session date used: 2025-04-18. Liquid KMI names: 96 (membership KMI_ALL_derived_2025-01-03.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.0015,-0.0624,0.4574,0,1
E&P,3,0.0004,-0.0582,0.4014,0,0
OMC,4,-0.0208,-0.1145,0.2756,0,0
Power,6,0.0661,0.0039,0.1353,0,0
Fertilizer,4,-0.0889,-0.0895,0.2721,0,0
Cement,16,0.0164,0.1308,0.7068,2,3
Steel & engineering,11,0.0263,-0.0636,0.1558,1,1
Autos,12,0.0454,-0.0001,0.3469,1,3
Tech & telecom,11,-0.0127,-0.1661,0.1678,0,0
Islamic banks & fin.,8,0.0082,0.0459,0.149,1,1
Pharma,14,0.0288,0.0225,0.8179,1,3
Textiles,23,-0.0105,-0.0903,0.0637,0,0
Food & staples,15,-0.0132,0.0134,0.3932,1,2
Chemicals,18,0.0493,0.0677,0.3393,2,3
"Glass, packaging, paper",14,0.0194,0.0021,0.1673,1,1
Gas utilities & misc,12,0.049,0.0466,0.5918,0,1

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ABOT,1056.74,0.008,-0.148,0.379,1.136,-0.179,0.29,0,2024-12-31,0.219,1,0,0,0,,
AGP,198.92,0.071,0.164,0.672,1.624,-0.007,0.462,0,2024-12-31,1.014,1,0,0,0,12.579,0.036
AGTL,476.39,-0.125,-0.275,0.153,0.4,-0.312,0.86,0,2024-12-31,0.415,2,0,0,0,8.123,
AIRLINK,181.39,0.007,-0.082,0.325,1.969,-0.175,0.381,1,2024-12-31,0.18,0,0,0,0,7.591,0.068
ATRL,596.88,-0.088,-0.101,0.518,0.517,-0.188,0.57,0,2024-12-31,-0.261,0,0,0,0,1.496,0.043
AVN,49.9,-0.062,-0.141,-0.062,0.051,-0.264,0.575,0,2024-12-31,0.63,1,0,0,0,,
BBFL,50.53,-0.017,-0.094,-0.276,,-0.395,0.778,0,,,0,0,0,0,,
BFBIO,155.77,-0.151,-0.259,,,,0.46,0,2024-12-31,0.313,1,0,0,0,,
BWCL,414.91,0.098,0.201,0.618,0.928,-0.007,0.564,0,,,1,0,0,0,,
CHCC,280.51,0.016,0.077,0.559,0.798,-0.085,0.827,0,2024-12-31,0.215,0,0,0,0,5.763,0.034
CNERGY,8.54,0.142,0.184,1.247,0.856,-0.012,1.009,0,2024-06-30,,0,0,0,0,114.054,
CPHL,94.26,0.027,0.415,1.121,2.876,-0.115,0.704,0,2024-12-31,-0.317,0,1,0,0,7.812,0.114
CSAP,116.99,0.101,0.098,0.204,0.705,-0.064,0.375,1,2024-12-31,-1.544,0,0,0,0,3.297,0.102
DGKC,125.0,-0.071,0.21,0.599,0.82,-0.076,0.698,0,2024-12-31,6.628,0,0,0,0,63.696,
EFERT,187.1,-0.146,-0.114,-0.019,0.275,-0.19,1.5,0,2024-12-31,-0.078,0,0,0,0,5.722,0.183
ENGROH,169.44,-0.1,-0.225,0.182,0.057,-0.384,1.49,0,2024-12-31,,1,1,0,0,5.206,0.167
EPCL,34.01,-0.08,-0.059,0.057,-0.249,-0.293,0.842,0,2025-03-31,,1,0,0,0,5.11,0.129
FABL,47.5,-0.032,-0.002,-0.037,0.359,-0.127,0.638,0,2024-12-31,-0.554,0,1,0,0,2.442,0.123
FATIMA,81.54,-0.024,0.042,0.414,1.128,-0.052,1.52,0,2024-12-31,0.361,1,1,0,0,3.239,0.127
FCCL,46.18,0.022,0.322,0.594,1.571,-0.028,0.778,0,2024-12-31,0.518,0,0,0,0,6.834,0.044
FCEPL,86.85,0.044,0.051,0.527,0.294,-0.084,0.4,0,2024-09-30,2.03,1,0,0,0,41.597,
FCL,24.26,-0.006,-0.063,-0.058,,-0.143,0.334,0,2024-12-31,-0.131,0,1,0,0,7.966,0.052
FFL,15.66,-0.025,-0.101,0.798,0.71,-0.189,0.415,0,2024-12-31,-0.9,0,0,0,0,46.392,
FLYNG,28.18,0.027,0.134,0.641,2.308,-0.094,0.463,0,,,1,0,0,0,,
GAL,501.01,0.114,0.294,1.601,3.447,-0.008,0.762,0,2024-12-31,90.444,0,0,0,0,27.284,
GHNI,764.04,0.131,0.284,1.062,3.337,-0.0,0.918,0,2024-12-31,,0,0,0,0,14.907,
GLAXO,440.02,0.142,0.16,1.057,4.041,-0.039,1.28,0,2024-12-31,2.189,2,0,0,0,49.498,
GWLC,40.62,-0.081,-0.276,0.577,0.753,-0.3,0.258,0,2024-12-31,-0.087,0,0,0,0,,
HALEON,809.5,0.019,-0.023,0.363,3.134,-0.122,2.213,0,2024-12-31,2.73,0,1,0,0,19.871,
HCAR,303.99,0.038,-0.03,0.157,0.312,-0.113,1.109,0,2024-12-31,2.97,0,1,0,0,13.638,0.029
HINOON,939.83,0.116,0.102,0.28,0.791,-0.006,1.972,0,2024-09-30,0.293,3,0,0,0,,
HUBC,142.77,0.072,0.159,0.457,0.312,-0.059,0.765,0,2024-12-31,-0.732,0,0,0,0,3.021,0.123
ILP,59.01,-0.033,-0.114,-0.181,-0.202,-0.298,0.747,0,2024-12-31,-0.698,0,0,0,0,6.013,0.064
KEL,4.53,0.018,-0.094,0.18,0.018,-0.292,0.509,0,2024-06-30,-0.871,0,0,0,0,30.127,
KSBP,167.64,0.062,0.092,0.318,0.386,-0.082,1.441,0,2024-12-31,1.42,2,0,0,0,,
LOTCHEM,17.82,-0.109,-0.161,0.032,-0.062,-0.234,0.122,0,2025-03-31,-0.254,2,1,0,0,8.049,0.111
LPL,27.2,0.02,0.167,0.619,0.361,-0.115,2.469,0,,,3,0,0,0,,
LUCK,1751.45,0.196,0.569,1.084,1.214,0.0,1.556,0,2024-12-31,0.232,0,1,0,0,4.053,0.016
MARI,662.8,0.094,-0.062,0.555,1.37,-0.263,1.212,0,2024-12-31,-0.386,1,3,0,0,4.682,0.086
MEBL,255.65,0.088,0.108,0.128,0.323,-0.036,0.731,0,2024-12-31,-0.075,0,0,0,0,3.383,0.124
MFFL,204.59,-0.088,-0.256,0.45,0.32,-0.356,0.3,0,,,1,0,0,0,,
MLCF,65.51,0.114,0.468,0.718,0.802,0.0,1.007,0,2024-12-31,0.708,0,0,0,0,5.919,
MTL,608.45,0.038,-0.079,0.201,0.112,-0.107,0.791,0,2024-12-31,0.015,0,0,0,0,11.845,0.039
NETSOL,135.56,-0.023,-0.143,0.031,0.123,-0.2,0.418,0,2024-12-31,-1.156,0,0,0,0,9.912,0.022
NML,115.92,0.138,0.147,0.598,0.726,-0.081,0.877,0,2024-12-31,-3.403,0,0,0,0,3.166,0.042
NRL,242.01,-0.011,-0.147,0.108,-0.163,-0.263,0.56,0,2024-12-31,,0,0,0,0,,
OCTOPUS,54.43,-0.11,-0.222,-0.358,0.286,-0.535,0.554,0,,,1,0,0,0,,
OGDC,212.88,-0.026,-0.024,0.301,0.829,-0.093,0.721,0,2024-12-31,-0.442,0,1,0,0,2.786,0.075
PABC,110.91,-0.113,-0.059,0.422,0.526,-0.195,0.665,0,,,2,0,0,0,,
PAEL,46.6,0.093,0.089,0.822,1.088,-0.034,0.962,1,2024-12-31,0.605,2,0,0,0,15.073,
PIBTL,10.61,0.07,0.247,0.622,0.804,-0.04,1.122,0,2024-12-31,0.556,0,0,0,0,6.244,
PIOC,219.41,0.028,0.153,0.117,0.69,-0.03,0.713,0,2024-12-31,0.034,0,0,0,0,7.401,0.089
POWER,12.31,0.03,0.345,1.395,1.28,-0.002,0.454,0,2024-12-31,,0,0,0,0,,
PPL,170.9,-0.066,-0.104,0.298,0.568,-0.183,0.836,0,2024-12-31,-0.319,0,1,0,0,2.759,0.051
PREMA,63.9,0.357,1.53,3.347,3.859,0.0,1.637,5,2024-12-31,0.853,0,3,0,0,8.672,
PRL,34.27,-0.03,-0.174,0.374,0.265,-0.227,0.777,0,2024-12-31,-0.832,0,0,0,0,3.599,0.086
PSO,389.83,-0.016,-0.032,0.911,1.286,-0.124,1.282,0,2024-12-31,,0,0,0,0,4.258,0.06
SAZEW,1316.34,0.209,0.209,0.366,2.046,0.0,0.884,0,2024-12-31,2.186,0,0,0,0,6.341,0.024
SEARL,94.95,-0.009,-0.062,0.5,0.644,-0.24,0.609,0,2024-12-31,,0,0,0,0,,
SLGL,15.86,0.079,0.036,-0.006,,-0.183,0.658,1,2024-12-31,1.776,4,0,0,0,,
SNGP,114.44,0.05,0.125,0.521,0.847,-0.013,0.803,0,2024-12-31,0.346,0,0,0,0,2.121,0.118
SPEL,39.78,0.004,-0.1,-0.022,2.056,-0.262,0.632,0,2024-12-31,0.603,0,1,0,0,,
SSGC,42.47,0.138,-0.032,3.843,2.984,-0.142,0.85,1,2024-06-30,-0.97,1,0,0,0,1.007,
SYM,14.19,-0.118,-0.244,0.463,2.888,-0.33,0.298,0,2024-06-30,-0.706,0,0,0,0,,
SYS,499.1,-0.035,-0.122,0.22,0.281,-0.2,1.266,0,2024-12-31,0.321,2,0,0,0,14.2,0.014
TGL,206.59,0.124,0.413,0.854,0.93,-0.034,0.626,0,2024-12-31,-0.204,0,0,0,0,4.587,
THCCL,207.9,0.017,0.002,1.161,8.925,-0.087,0.514,0,2024-12-31,2.581,0,1,0,0,2.244,0.028
TOMCL,34.18,-0.011,-0.026,-0.071,0.132,-0.262,0.944,0,2024-12-31,0.22,0,0,0,0,10.506,
TPLP,9.91,-0.086,-0.242,0.294,-0.103,-0.366,0.575,0,,,0,3,0,0,,
TREET,20.93,-0.06,-0.112,0.495,0.294,-0.255,0.635,0,2024-12-31,,0,0,0,0,,
WAFI,175.77,-0.064,-0.165,0.12,0.157,-0.283,0.219,0,2024-12-31,,3,0,0,0,5.504,0.033
WAVES,7.71,-0.023,-0.058,0.23,0.035,-0.167,0.228,0,2024-09-30,1.467,4,0,0,0,9.819,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2025-04-03,TPLRF1,material_info,Material Information
2025-04-03,TPLP,material_info,Material Information
2025-04-03,PKGP,material_info,Material Information
2025-04-03,NPL,material_info,Material Information
2025-04-03,LOTCHEM,material_info,Material Information
2025-04-03,NCPL,material_info,Material Information
2025-04-04,PKGI,material_info,Material Information REVOKED
2025-04-04,THCCL,material_info,Material Information - Wind Power Project
2025-04-04,CSIL,material_info,Material Information
2025-04-04,BAFL,material_info,Disclosure of Material Information
2025-04-04,ZHCM,material_info,Material Information
2025-04-07,EPQL,material_info,Disclosure of Material Information
2025-04-07,ENGROH,material_info,Disclosure of Material Information
2025-04-07,PREMA,material_info,Material Information
2025-04-08,PREMA,material_info,Material Information - Privately Placed Islamic Sukuk
2025-04-08,MARI,material_info,Material Information
2025-04-08,LUCK,material_info,DISCLOSURE OF MATERIAL INFORMATION
2025-04-08,FATIMA,material_info,Disclosure of Material Information
2025-04-08,IGIHL,material_info,Material Information
2025-04-09,TPLRF1,material_info,Material Information
2025-04-09,TPLP,material_info,Material Information
2025-04-09,ATLH,material_info,Material Information
2025-04-09,SITC,material_info,Material Information
2025-04-10,PPL,material_info,Material Information
2025-04-10,KAPCO,material_info,Disclosure of Material Information
2025-04-11,HCAR,material_info,Material Information
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

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,45.176,2025-04-17
investor_type,last_5_sessions,broker proprietary trading,-5.815,2025-04-17
investor_type,last_5_sessions,companies,13.998,2025-04-17
investor_type,last_5_sessions,foreign corporates,-5.375,2025-04-17
investor_type,last_5_sessions,foreign individual,0.009,2025-04-17
investor_type,last_5_sessions,individuals,20.828,2025-04-17
investor_type,last_5_sessions,insurance companies,-33.747,2025-04-17
investor_type,last_5_sessions,mutual funds,-46.77,2025-04-17
investor_type,last_5_sessions,nbfc,0.078,2025-04-17
investor_type,last_5_sessions,other organization,10.021,2025-04-17
investor_type,last_5_sessions,overseas pakistani,1.597,2025-04-17
sector,last_5_sessions,fipi | All other Sectors,-5.789,2025-04-17
sector,last_5_sessions,lipi banks / dfi | Cement,-6.255,2025-04-17
sector,last_5_sessions,lipi banks / dfi | Debt Market,47.104,2025-04-17
sector,last_5_sessions,lipi companies | All other Sectors,4.112,2025-04-17
sector,last_5_sessions,lipi companies | Cement,8.943,2025-04-17
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,11.303,2025-04-17
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-18.112,2025-04-17
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-6.799,2025-04-17
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-13.456,2025-04-17
sector,last_5_sessions,lipi mutual funds | Cement,-4.687,2025-04-17
sector,last_5_sessions,lipi mutual funds | Debt Market,-48.725,2025-04-17
sector,last_5_sessions,lipi other organization | Commercial Banks,9.103,2025-04-17
investor_type,last_20_sessions,banks / dfi,242.85,2025-04-17
investor_type,last_20_sessions,broker proprietary trading,-11.659,2025-04-17
investor_type,last_20_sessions,companies,14.102,2025-04-17
investor_type,last_20_sessions,foreign corporates,-25.18,2025-04-17
investor_type,last_20_sessions,foreign individual,0.098,2025-04-17
investor_type,last_20_sessions,individuals,15.629,2025-04-17
investor_type,last_20_sessions,insurance companies,-58.058,2025-04-17
investor_type,last_20_sessions,mutual funds,-210.109,2025-04-17
investor_type,last_20_sessions,nbfc,0.952,2025-04-17
investor_type,last_20_sessions,other organization,16.347,2025-04-17
investor_type,last_20_sessions,overseas pakistani,15.028,2025-04-17
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,9.076,2025-04-17
sector,last_20_sessions,lipi banks / dfi | Debt Market,228.699,2025-04-17
sector,last_20_sessions,lipi companies | Cement,16.633,2025-04-17
sector,last_20_sessions,lipi companies | Fertilizer,-13.92,2025-04-17
sector,last_20_sessions,lipi individuals | Commercial Banks,9.132,2025-04-17
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-32.796,2025-04-17
sector,last_20_sessions,lipi insurance companies | Fertilizer,11.725,2025-04-17
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-9.88,2025-04-17
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-29.711,2025-04-17
sector,last_20_sessions,lipi mutual funds | Cement,-9.966,2025-04-17
sector,last_20_sessions,lipi mutual funds | Debt Market,-229.071,2025-04-17
sector,last_20_sessions,lipi other organization | Commercial Banks,14.459,2025-04-17

=== FILE: calendar.md ===
# Calendar as of 2025-04-18

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2025-03-20 MFFL: Board Meeting other than Financial Results
- 2025-03-20 OCTOPUS: Board Meeting
- 2025-03-20 ATLH: Board Meeting - Approval of Annual Budget
- 2025-03-21 LPL: BOARD MEETING
- 2025-03-27 WAVES: Board Meeting- Annual Accounts for the Year Ended 31Dec24
- 2025-04-03 SLGL: Short Notice of Board Meeting
- 2025-04-03 INIL: Board Meeting Other Than Financial Results
- 2025-04-04 EFERT: Board Meeting for the announcement of the financial results for the three months ended March 31, 2025
- 2025-04-08 EPCL: Board Meeting for the announcement of the financial results - Engro Polymer & Chemicals Limited
- 2025-04-09 BWCL: Board Meeting
- 2025-04-10 LOTCHEM: Board Meeting
- 2025-04-10 MEBL: NOTICE OF BOARD MEETING AND CLOSED PERIOD - MEEZAN BANK LIMITED
- 2025-04-10 ISL: BOARD MEETING
- 2025-04-11 GHNI: Board Meeting
- 2025-04-11 GAL: Board Meeting
- 2025-04-11 SAZEW: Board Meeting
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
- 2025-04-16 ENGROH: Board Meeting for the Announcement of the Financial Results for the First Quarter ended March 31, 2025
- 2025-04-17 TPLP: Board Meeting
- 2025-04-17 MARI: Notice of Board of Directors Meeting
- 2025-04-17 GATM: BOARD MEETING
- 2025-04-17 POWER: Board Meeting
- 2025-04-17 FATIMA: Board Meeting and Closed Period
- 2025-04-17 GLAXO: Board Meeting Quarter ended March 31, 2025
- 2025-04-17 ACPL: Board Meeting
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
