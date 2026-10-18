# Replay bundle, close of 2022-07-29

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
# Market as of 2022-07-29 close (public information only)

- KSE100: 40,150 on 2022-07-29; 1m -4.1%, 3m -12.1%, 6m -10.8%, 12m -15.8%
- KMI All Share: 20,294 on 2022-07-29; 1m -3.0%, 3m -9.9%, 6m -8.6%, 12m -13.1%
- Policy rate 15.0%; last MPC decision 2022-07-07: hike (+125bp)
- 6M T-bill cutoff 15.80% (auction 2022-07-27); 3M 15.75%, 12M 15.94%
- CPI YoY 21.34% for 2022-06 (published by 2022-07-03); three months earlier (2022-03) 12.71%
- Brent: 111.51 USD/bbl on 2022-07-29; 3-month change +2.9%
- USD/PKR: 239.94  on 2022-07-29; 3-month change +29.3%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.80pp (market pricing hikes); CPI rising over 3 months (+8.6pp)
- Next MPC: see SBP calendar

Session date used: 2022-07-29. Liquid KMI names: 46 (membership KMI_ALL_derived_2022-07-15.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.1683,-0.1547,-0.1191,0,0
E&P,3,-0.0063,-0.0401,-0.066,0,0
OMC,4,-0.0211,-0.04,-0.1027,0,0
Power,5,-0.0568,-0.0951,-0.107,0,0
Fertilizer,4,-0.0621,-0.1229,0.0208,0,0
Cement,16,-0.0442,-0.23,-0.2862,0,0
Steel & engineering,11,-0.0281,-0.1386,-0.2293,0,0
Autos,12,-0.0851,-0.1514,-0.1627,0,0
Tech & telecom,8,-0.0358,-0.1278,-0.2168,0,0
Islamic banks & fin.,6,0.0061,-0.0842,-0.0781,0,0
Pharma,11,-0.0123,-0.0957,-0.1425,0,0
Textiles,18,-0.0222,-0.1244,-0.1618,0,0
Food & staples,13,-0.033,-0.1317,-0.2098,0,0
Chemicals,16,-0.0159,-0.0835,-0.0334,0,0
"Glass, packaging, paper",13,-0.0194,-0.1336,-0.1585,0,0
Gas utilities & misc,9,0.0022,-0.0301,-0.0785,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ANL,9.83,-0.066,-0.218,-0.222,-0.689,-0.691,0.981,0,,,0,0,0,0,,
ATRL,135.92,-0.229,-0.163,-0.066,-0.442,-0.439,1.056,0,2022-03-31,,0,0,0,0,,
AVN,79.06,-0.014,-0.049,-0.074,-0.115,-0.293,0.967,0,2022-03-31,,0,1,0,0,,
CHCC,77.88,-0.17,-0.426,-0.454,-0.532,-0.561,0.897,0,2022-03-31,,0,0,0,0,,
CNERGY,4.79,-0.128,-0.263,-0.248,-0.534,-0.536,0.515,0,,,0,0,0,0,,
DGKC,52.48,-0.12,-0.239,-0.318,-0.532,-0.54,1.02,0,2022-03-31,,0,0,0,0,,
EFERT,79.0,-0.113,-0.186,-0.002,0.066,-0.218,1.008,0,2022-06-30,,1,1,0,0,4.817,0.217
EPCL,66.34,-0.196,-0.18,0.365,0.784,-0.255,0.722,1,2022-03-31,,0,0,0,0,3.33,0.301
FCCL,12.93,-0.108,-0.241,-0.262,-0.428,-0.42,0.719,0,2021-09-30,,0,0,0,0,,
FLYNG,6.12,-0.162,-0.328,-0.476,-0.69,-0.704,0.289,0,,,0,0,0,0,,
GAL,52.98,-0.14,-0.302,-0.304,-0.63,-0.628,1.141,0,,,0,0,0,0,,
GGGL,10.01,-0.121,-0.284,-0.25,-0.643,-0.639,0.378,0,,,0,1,0,0,,
GGL,15.55,-0.078,-0.193,-0.251,-0.619,-0.634,0.363,0,2022-03-31,,0,0,0,0,,
GHNI,137.37,-0.14,-0.247,-0.181,-0.558,-0.545,0.884,0,2022-03-31,,0,0,0,0,,
HCAR,151.47,-0.175,-0.233,-0.3,-0.609,-0.606,0.554,0,2022-06-30,,2,0,0,0,,
HTL,37.8,-0.062,-0.143,-0.196,-0.409,-0.475,0.541,0,,,0,0,0,0,,
HUBC,64.42,-0.037,-0.089,-0.123,-0.045,-0.161,0.722,0,2022-03-31,,0,0,0,0,,
INIL,100.09,-0.012,-0.155,-0.268,-0.512,-0.539,0.387,0,2022-03-31,,0,0,0,0,,
ISL,54.6,-0.066,-0.126,-0.225,-0.393,-0.455,0.602,0,2022-03-31,,0,0,0,0,,
KEL,2.89,-0.065,-0.01,-0.068,-0.265,-0.278,0.871,0,2022-03-31,-1.778,0,0,0,0,9.635,
KOHC,127.22,-0.059,-0.216,-0.275,-0.394,-0.436,0.572,0,2022-03-31,,0,1,0,0,,
LUCK,411.93,-0.079,-0.298,-0.383,-0.543,-0.542,1.109,0,2022-03-31,,0,0,0,0,,
MARI,1695.88,-0.053,-0.003,-0.009,0.124,-0.058,0.748,0,2022-03-31,,0,0,0,0,,
MEBL,118.49,0.038,-0.15,-0.114,0.169,-0.21,0.799,0,2022-03-31,,0,0,0,0,7.73,0.042
MFFL,114.71,0.422,0.119,-0.618,-0.727,-0.728,2.979,2,,,0,0,0,0,,
MLCF,24.03,-0.104,-0.325,-0.285,-0.468,-0.48,0.558,0,,,0,0,0,0,,
MTL,820.02,-0.077,0.042,0.392,0.412,-0.1,0.472,0,2022-03-31,,0,0,0,0,,
MUGHAL,55.99,-0.056,-0.322,-0.457,-0.333,-0.504,0.838,0,2022-03-31,,0,0,0,0,,
NML,67.42,-0.077,-0.202,-0.157,-0.306,-0.324,0.498,0,2022-03-31,,0,0,0,0,,
NRL,219.83,-0.154,-0.155,-0.154,-0.509,-0.483,0.808,0,2022-03-31,,0,0,0,0,,
OCTOPUS,70.12,-0.022,-0.036,-0.368,,-0.368,0.944,0,,,0,1,0,0,,
OGDC,80.42,0.018,-0.036,-0.052,-0.084,-0.124,0.988,0,2022-03-31,,0,0,0,0,,
PAEL,14.86,-0.116,-0.14,-0.282,-0.573,-0.567,0.633,0,2022-03-31,,0,0,0,0,7.238,
PIBTL,5.46,-0.105,-0.173,-0.25,-0.518,-0.514,0.53,0,2022-03-31,,0,0,0,0,,
PIOC,55.26,-0.093,-0.218,-0.344,-0.545,-0.56,0.484,0,2022-03-31,,0,0,0,0,,
PPL,68.45,0.015,-0.088,-0.146,-0.178,-0.218,1.088,0,2022-03-31,,0,1,0,0,,
PSO,172.44,-0.008,0.042,-0.054,-0.236,-0.254,0.942,0,2022-03-31,,0,0,0,0,,
SEARL,98.08,-0.071,-0.152,-0.284,-0.468,-0.475,0.766,0,2022-03-31,,0,1,0,0,,
SNGP,31.5,0.068,0.147,0.081,-0.288,-0.311,2.045,0,2021-12-31,,4,0,0,0,2.805,0.144
SYS,347.64,0.027,-0.104,-0.102,0.114,-0.158,0.957,0,2022-03-31,,0,0,0,0,23.513,0.007
TELE,10.6,-0.071,-0.282,-0.404,-0.326,-0.565,0.349,0,2021-06-30,,0,0,0,0,8.369,
TGL,103.61,-0.012,-0.189,-0.172,0.121,-0.242,0.346,0,2022-03-31,,0,0,0,0,,
TREET,24.72,-0.179,-0.292,-0.371,-0.576,-0.576,0.2,0,2022-03-31,,0,0,0,0,,
UNITY,18.74,-0.085,-0.241,-0.319,-0.572,-0.564,0.893,0,2022-03-31,-0.395,0,0,0,0,13.56,
WAFI,118.91,0.024,0.012,-0.013,-0.309,-0.309,0.785,0,,,0,0,0,0,5.807,
WAVES,11.38,-0.119,-0.244,-0.25,-0.567,-0.581,0.423,0,2022-03-31,,0,0,0,0,13.769,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2022-06-30,GLAXO,material_info,Material Information - Resignation of Mark Dawson as Director w.e.f. 30 Jun
2022-07-01,MEHT,material_info,Material Information
2022-07-01,ICI,material_info,Material Information
2022-07-01,SAZEW,material_info,Material Information
2022-07-04,FFC,material_info,Material Information
2022-07-04,SMBL,material_info,Additional Disclosure of Material Information in the Matter of Acquisition 
2022-07-04,CSAP,material_info,Material Information
2022-07-04,SNGP,financial_result,FINANCIAL RESULTS FOR THE 1ST QUARTER ACCOUNTS FOR THE PERIOD ENDED SEPTEMB
2022-07-04,SNGP,financial_result,"FINANCIAL RESULTS FOR THE FINANCIAL YEAR ENDED JUNE 30, 2021"
2022-07-06,AGL,material_info,Disclosure of Material Information
2022-07-06,PPL,material_info,Material Information - Resignation of a Director
2022-07-06,ZIL,material_info,Material Information
2022-07-06,HCAR,dividend_or_bonus,HCAR | Honda Atlas Cars (Pakistan) Limited - Dispatch of Dividend warrants 
2022-07-07,SNGP,financial_result,"TRANSMISSION OF ANNUAL AUDITED ACCOUNTS FOR THE YEAR ENDED JUNE 30, 2021"
2022-07-07,SNGP,financial_result,TRANSMISSION OF 1ST QUARTER (UN-AUDITED) ACCOUNTS FOR THE PERIOD ENDED SEPT
2022-07-13,KOHC,material_info,Material Information
2022-07-13,GEMUNSL,material_info,Material Information
2022-07-14,ICI,material_info,Material Information
2022-07-14,SEARL,material_info,Material Information
2022-07-15,MODAM,material_info,Material Information
2022-07-15,TPLI,material_info,Material Information
2022-07-15,TPL,material_info,Category Material Information
2022-07-15,KEL,dividend_or_bonus,Book Closure of KE SUKUK-5.
2022-07-18,FNEL,material_info,Material Information
2022-07-18,EFGH,material_info,Material Information
2022-07-18,GGGL,material_info,Disclosure of Material Information - GHANI GLOBAL GLASS LIMITED
2022-07-18,FLYNG,dividend_or_bonus,PROGRESS REPORT OF RIGHT ISSUE - FLYING CEMENT COMPANY LTD
2022-07-19,MTL,dividend_or_bonus,Disposal of Bonus Shares Fraction-B25
2022-07-20,FFC,material_info,"Material Information - FFC Plant-III, MM"
2022-07-20,NCL,material_info,Material Information
2022-07-21,DATM,material_info,Material Information
2022-07-22,PSX,material_info,DISCLOSURE OF MATERIAL INFORMATION
2022-07-22,FFL,material_info,Material Information
2022-07-25,ICI,material_info,Material Information
2022-07-25,DAWH,material_info,Material information
2022-07-25,BHAT,material_info,Material Information - Chairman Report
2022-07-26,KAPCO,material_info,Material Information
2022-07-26,AVN,material_info,Material Information
2022-07-26,OCTOPUS,material_info,Material Information
2022-07-26,HCAR,financial_result,"Financial Results for the quarter ended June 30, 2022"
2022-07-27,SHFA,insider_trade,Insider trade disclosure
2022-07-28,EFERT,material_info,Material Information
2022-07-28,BIPLS,material_info,DISCLOSURE OF MATERIAL INFORMAITON OF OPERATIONAL MERGER
2022-07-28,BCL,material_info,Material Information
2022-07-28,CLVL,material_info,Material Information
2022-07-28,HCAR,financial_result,"Transmission of Quarterly Report for the period ended June 30, 2022"
2022-07-28,EFERT,financial_result,"ANNOUNCEMENT OF FINANCIAL RESULTS FOR THE SIX MONTHS ENDED JUNE 30, 2022"
2022-07-28,TRG,insider_trade,Insider trade disclosure
2022-07-28,PKGS,insider_trade,Insider trade disclosure
2022-07-28,STPL,insider_trade,Insider trade disclosure
2022-07-29,INDU,material_info,Material Information
2022-07-29,FML,insider_trade,Insider trade disclosure
2022-07-29,FML,insider_trade,Insider trade disclosure
2022-07-29,SHFA,insider_trade,Insider trade disclosure
2022-07-29,MCB,insider_trade,Insider trade disclosure
2022-07-29,MCB,insider_trade,Insider trade disclosure

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,3.478,2022-07-28
investor_type,last_5_sessions,broker proprietary trading,-0.09,2022-07-28
investor_type,last_5_sessions,companies,1.746,2022-07-28
investor_type,last_5_sessions,foreign corporates,-1.568,2022-07-28
investor_type,last_5_sessions,foreign individual,-0.001,2022-07-28
investor_type,last_5_sessions,individuals,-0.266,2022-07-28
investor_type,last_5_sessions,insurance companies,-0.575,2022-07-28
investor_type,last_5_sessions,mutual funds,-2.209,2022-07-28
investor_type,last_5_sessions,nbfc,-0.018,2022-07-28
investor_type,last_5_sessions,other organization,-1.025,2022-07-28
investor_type,last_5_sessions,overseas pakistani,0.527,2022-07-28
sector,last_5_sessions,fipi | All other Sectors,-1.229,2022-07-28
sector,last_5_sessions,fipi | Cement,-0.985,2022-07-28
sector,last_5_sessions,fipi | Commercial Banks,-1.479,2022-07-28
sector,last_5_sessions,fipi | Fertilizer,0.025,2022-07-28
sector,last_5_sessions,fipi | Food and Personal Care Products,-0.035,2022-07-28
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,0.423,2022-07-28
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,0.167,2022-07-28
sector,last_5_sessions,fipi | Power Generation and Distribution,-0.131,2022-07-28
sector,last_5_sessions,fipi | Technology and Communication,1.531,2022-07-28
sector,last_5_sessions,fipi | Textile Composite,0.672,2022-07-28
sector,last_5_sessions,lipi banks / dfi | All other Sectors,1.935,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Cement,-0.016,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,0.187,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Fertilizer,0.993,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-0.039,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,-0.129,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.302,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.116,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,-0.179,2022-07-28
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.308,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-0.081,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.126,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.057,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.093,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.073,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.142,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.048,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.024,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,0.273,2022-07-28
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.318,2022-07-28
sector,last_5_sessions,lipi companies | All other Sectors,-0.132,2022-07-28
sector,last_5_sessions,lipi companies | Cement,-0.013,2022-07-28
sector,last_5_sessions,lipi companies | Commercial Banks,1.344,2022-07-28
sector,last_5_sessions,lipi companies | Fertilizer,-0.122,2022-07-28
sector,last_5_sessions,lipi companies | Food and Personal Care Products,-0.117,2022-07-28
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,0.866,2022-07-28
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,0.137,2022-07-28
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.026,2022-07-28
sector,last_5_sessions,lipi companies | Technology and Communication,-0.45,2022-07-28
sector,last_5_sessions,lipi companies | Textile Composite,0.259,2022-07-28
sector,last_5_sessions,lipi individuals | All other Sectors,0.23,2022-07-28
sector,last_5_sessions,lipi individuals | Cement,0.842,2022-07-28
sector,last_5_sessions,lipi individuals | Commercial Banks,0.286,2022-07-28
sector,last_5_sessions,lipi individuals | Fertilizer,-0.336,2022-07-28
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,-0.006,2022-07-28
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,0.978,2022-07-28
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.158,2022-07-28
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.264,2022-07-28
sector,last_5_sessions,lipi individuals | Technology and Communication,-1.839,2022-07-28
sector,last_5_sessions,lipi individuals | Textile Composite,-0.526,2022-07-28
sector,last_5_sessions,lipi insurance companies | All other Sectors,-0.431,2022-07-28
sector,last_5_sessions,lipi insurance companies | Cement,0.186,2022-07-28
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-0.051,2022-07-28
sector,last_5_sessions,lipi insurance companies | Fertilizer,0.094,2022-07-28
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,-0.007,2022-07-28
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-0.341,2022-07-28
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-0.0,2022-07-28
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,0.006,2022-07-28
sector,last_5_sessions,lipi insurance companies | Technology and Communication,0.018,2022-07-28
sector,last_5_sessions,lipi insurance companies | Textile Composite,-0.049,2022-07-28
sector,last_5_sessions,lipi mutual funds | All other Sectors,-0.466,2022-07-28
sector,last_5_sessions,lipi mutual funds | Cement,-0.039,2022-07-28
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-0.17,2022-07-28
sector,last_5_sessions,lipi mutual funds | Fertilizer,-0.608,2022-07-28
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,0.296,2022-07-28
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-1.235,2022-07-28
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.402,2022-07-28
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.136,2022-07-28
sector,last_5_sessions,lipi mutual funds | Technology and Communication,0.753,2022-07-28
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.2,2022-07-28
sector,last_5_sessions,lipi nbfc | All other Sectors,-0.019,2022-07-28
sector,last_5_sessions,lipi nbfc | Cement,-0.001,2022-07-28
sector,last_5_sessions,lipi nbfc | Commercial Banks,-0.001,2022-07-28
sector,last_5_sessions,lipi nbfc | Fertilizer,0.011,2022-07-28
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,-0.0,2022-07-28
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.002,2022-07-28
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.001,2022-07-28
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.0,2022-07-28
sector,last_5_sessions,lipi nbfc | Technology and Communication,-0.001,2022-07-28
sector,last_5_sessions,lipi nbfc | Textile Composite,-0.006,2022-07-28
sector,last_5_sessions,lipi other organization | All other Sectors,0.194,2022-07-28
sector,last_5_sessions,lipi other organization | Cement,-0.1,2022-07-28
sector,last_5_sessions,lipi other organization | Commercial Banks,-0.172,2022-07-28
sector,last_5_sessions,lipi other organization | Fertilizer,-0.15,2022-07-28
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,-0.019,2022-07-28
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.419,2022-07-28
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.003,2022-07-28
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,-0.118,2022-07-28
sector,last_5_sessions,lipi other organization | Technology and Communication,-0.104,2022-07-28
sector,last_5_sessions,lipi other organization | Textile Composite,-0.14,2022-07-28
investor_type,last_20_sessions,banks / dfi,7.023,2022-07-28
investor_type,last_20_sessions,broker proprietary trading,-2.863,2022-07-28
investor_type,last_20_sessions,companies,3.512,2022-07-28
investor_type,last_20_sessions,foreign corporates,2.315,2022-07-28
investor_type,last_20_sessions,foreign individual,0.069,2022-07-28
investor_type,last_20_sessions,individuals,12.93,2022-07-28
investor_type,last_20_sessions,insurance companies,-15.339,2022-07-28
investor_type,last_20_sessions,mutual funds,-14.12,2022-07-28
investor_type,last_20_sessions,nbfc,0.084,2022-07-28
investor_type,last_20_sessions,other organization,2.627,2022-07-28
investor_type,last_20_sessions,overseas pakistani,3.762,2022-07-28
sector,last_20_sessions,fipi | All other Sectors,0.432,2022-07-28
sector,last_20_sessions,fipi | Cement,-0.571,2022-07-28
sector,last_20_sessions,fipi | Commercial Banks,-2.183,2022-07-28
sector,last_20_sessions,fipi | Fertilizer,-0.422,2022-07-28
sector,last_20_sessions,fipi | Food and Personal Care Products,0.741,2022-07-28
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,1.259,2022-07-28
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,0.363,2022-07-28
sector,last_20_sessions,fipi | Power Generation and Distribution,-0.049,2022-07-28
sector,last_20_sessions,fipi | Technology and Communication,5.686,2022-07-28
sector,last_20_sessions,fipi | Textile Composite,0.89,2022-07-28
sector,last_20_sessions,lipi banks / dfi | All other Sectors,3.717,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Cement,2.52,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-1.318,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Debt Market,-0.989,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Fertilizer,2.47,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,-0.291,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,1.64,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-1.467,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,0.016,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,-0.089,2022-07-28
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.815,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-2.668,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Cement,-0.029,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,0.677,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.008,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,0.008,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-1.442,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-0.025,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.623,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.143,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,0.622,2022-07-28
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.477,2022-07-28
sector,last_20_sessions,lipi companies | All other Sectors,3.529,2022-07-28
sector,last_20_sessions,lipi companies | Cement,1.124,2022-07-28
sector,last_20_sessions,lipi companies | Commercial Banks,2.531,2022-07-28
sector,last_20_sessions,lipi companies | Fertilizer,-1.309,2022-07-28
sector,last_20_sessions,lipi companies | Food and Personal Care Products,-1.324,2022-07-28
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,1.727,2022-07-28
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,-1.195,2022-07-28
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-0.423,2022-07-28
sector,last_20_sessions,lipi companies | Technology and Communication,-1.544,2022-07-28
sector,last_20_sessions,lipi companies | Textile Composite,0.397,2022-07-28
sector,last_20_sessions,lipi individuals | All other Sectors,5.072,2022-07-28
sector,last_20_sessions,lipi individuals | Cement,2.32,2022-07-28
sector,last_20_sessions,lipi individuals | Commercial Banks,1.587,2022-07-28
sector,last_20_sessions,lipi individuals | Debt Market,-0.001,2022-07-28
sector,last_20_sessions,lipi individuals | Fertilizer,1.406,2022-07-28
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,1.93,2022-07-28
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,0.296,2022-07-28
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,2.332,2022-07-28
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,0.862,2022-07-28
sector,last_20_sessions,lipi individuals | Technology and Communication,-3.646,2022-07-28
sector,last_20_sessions,lipi individuals | Textile Composite,0.774,2022-07-28
sector,last_20_sessions,lipi insurance companies | All other Sectors,-4.288,2022-07-28
sector,last_20_sessions,lipi insurance companies | Cement,-3.752,2022-07-28
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-2.038,2022-07-28
sector,last_20_sessions,lipi insurance companies | Fertilizer,-0.088,2022-07-28
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,-0.799,2022-07-28
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-2.23,2022-07-28
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-0.719,2022-07-28
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,-0.022,2022-07-28
sector,last_20_sessions,lipi insurance companies | Technology and Communication,-1.209,2022-07-28
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.193,2022-07-28
sector,last_20_sessions,lipi mutual funds | All other Sectors,-6.869,2022-07-28
sector,last_20_sessions,lipi mutual funds | Cement,-1.927,2022-07-28
sector,last_20_sessions,lipi mutual funds | Commercial Banks,0.395,2022-07-28
sector,last_20_sessions,lipi mutual funds | Fertilizer,-1.93,2022-07-28
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,0.43,2022-07-28
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-2.258,2022-07-28
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.002,2022-07-28
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-0.125,2022-07-28
sector,last_20_sessions,lipi mutual funds | Technology and Communication,0.248,2022-07-28
sector,last_20_sessions,lipi mutual funds | Textile Composite,-2.086,2022-07-28
sector,last_20_sessions,lipi nbfc | All other Sectors,-0.027,2022-07-28
sector,last_20_sessions,lipi nbfc | Cement,0.029,2022-07-28
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.013,2022-07-28
sector,last_20_sessions,lipi nbfc | Debt Market,0.169,2022-07-28
sector,last_20_sessions,lipi nbfc | Fertilizer,-0.043,2022-07-28
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,0.0,2022-07-28
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.024,2022-07-28
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,0.036,2022-07-28
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.0,2022-07-28
sector,last_20_sessions,lipi nbfc | Technology and Communication,-0.024,2022-07-28
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.021,2022-07-28
sector,last_20_sessions,lipi other organization | All other Sectors,1.103,2022-07-28
sector,last_20_sessions,lipi other organization | Cement,0.286,2022-07-28
sector,last_20_sessions,lipi other organization | Commercial Banks,0.361,2022-07-28
sector,last_20_sessions,lipi other organization | Debt Market,0.83,2022-07-28
sector,last_20_sessions,lipi other organization | Fertilizer,-0.094,2022-07-28
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,0.755,2022-07-28
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,-0.384,2022-07-28
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,0.027,2022-07-28
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,-0.116,2022-07-28
sector,last_20_sessions,lipi other organization | Technology and Communication,-0.043,2022-07-28
sector,last_20_sessions,lipi other organization | Textile Composite,-0.099,2022-07-28

=== FILE: calendar.md ===
# Calendar as of 2022-07-29

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2022-06-30 KOHC: Board Meeting Other Than Financial Results
- 2022-07-01 MARI: Emergent Board of Directors Meeting
- 2022-07-07 MARI: Notice of Board of Directors Meeting
- 2022-07-07 SEARL: Board Meeting Other Than Financial Results
- 2022-07-14 MFFL: Board Meeting to approve Business Plan 2023-2025
- 2022-07-18 EFERT: Board Meeting
- 2022-07-19 HCAR: Board Meeting
- 2022-07-25 LUCK: BOARD MEETING
- 2022-07-26 WAVES: Board Meeting for the Quarter Ended March 31, 2022
- 2022-07-26 WAVES: Board Meeting for Annual Financial Results Year Ended December 31, 2021
- 2022-07-28 EPCL: Board Meeting
- 2022-07-28 MARI: Notice of Board of Directors Meeting
- 2022-07-29 CNERGY: Board Meeting Other Than Financial Results

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
