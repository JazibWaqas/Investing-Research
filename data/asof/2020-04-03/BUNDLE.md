# Replay bundle, close of 2020-04-03

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
# Market as of 2020-04-03 close (public information only)

- KSE100: 31,622 on 2020-04-03; 1m -18.7%, 3m -25.3%, 6m -6.0%, 12m -18.8%
- KMI All Share: 15,005 on 2020-04-03; 1m -16.7%, 3m -25.1%, 6m -4.6%, 12m -20.2%
- Policy rate 11.0%; last MPC decision 2020-03-24: cut (-150bp)
- 6M T-bill cutoff 11.30% (auction 2020-03-25); 3M 11.30%, 12M 10.87%
- CPI YoY 11.38% for 2020-03 (published by 2020-04-03); three months earlier (2019-12) 13.74%
- Brent: 24.33 USD/bbl on 2020-04-03; 3-month change -64.8%
- USD/PKR: 166.46  on 2020-04-03; 3-month change +7.5%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.30pp (market near policy rate); CPI falling over 3 months (-2.4pp)
- Next MPC: see SBP calendar

Session date used: 2020-04-03. Liquid KMI names: 54 (membership KMI_ALL_derived_2020-01-13.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.1535,-0.2778,-0.0795,0,0
E&P,3,-0.2203,-0.3371,-0.1676,0,0
OMC,4,-0.1639,-0.2897,-0.0339,0,0
Power,4,-0.0951,-0.2527,-0.1182,0,0
Fertilizer,4,-0.1178,-0.1954,-0.0839,0,0
Cement,16,-0.044,-0.0605,0.1948,0,0
Steel & engineering,10,-0.0621,-0.1901,0.0395,0,0
Autos,12,-0.1866,-0.3019,0.0721,0,0
Tech & telecom,6,-0.1945,-0.2777,-0.0958,0,0
Islamic banks & fin.,8,-0.0852,-0.1049,-0.0027,0,0
Pharma,11,-0.0542,-0.0983,0.3973,0,0
Textiles,21,-0.1285,-0.1306,-0.0257,0,0
Food & staples,11,-0.1079,-0.2363,0.0257,0,0
Chemicals,17,-0.1234,-0.2055,-0.0098,0,0
"Glass, packaging, paper",12,-0.1445,-0.2433,0.1081,0,0
Gas utilities & misc,9,-0.1325,-0.2722,-0.0545,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,n_results,n_material,n_insider_buy,n_insider_sell
AGP,84.78,-0.164,-0.169,0.148,0.002,-0.22,0.525,0,1,0,0,0
ASC,10.0,-0.213,-0.212,-0.038,-0.375,-0.373,1.264,1,0,0,0,0
ASTL,31.82,-0.137,-0.19,0.222,-0.235,-0.261,0.791,2,0,1,0,0
ATRL,77.7,-0.165,-0.347,-0.134,-0.314,-0.433,0.638,1,0,2,0,0
BIPL,9.42,-0.264,-0.216,-0.144,-0.181,-0.372,0.902,0,0,0,0,0
CHCC,67.09,0.001,0.236,1.114,0.202,-0.219,1.464,3,0,0,0,0
DCL,7.52,-0.054,-0.053,0.056,-0.387,-0.347,1.196,1,0,0,0,0
DGKC,67.82,-0.112,-0.126,0.122,-0.223,-0.228,1.195,1,0,1,0,0
EFERT,57.39,-0.092,-0.22,-0.164,-0.204,-0.27,1.069,0,1,0,0,0
ENGROH,109.45,-0.226,-0.34,-0.088,-0.15,-0.377,0.486,0,0,0,0,0
EPCL,27.45,-0.143,-0.17,0.065,-0.242,-0.266,0.669,0,3,5,0,0
FCCL,16.72,-0.002,0.021,0.071,-0.164,-0.169,1.513,2,0,0,0,0
FCEPL,61.58,-0.051,-0.225,-0.061,-0.126,-0.284,0.419,0,1,0,0,0
FEROZ,178.68,-0.118,-0.172,0.171,-0.118,-0.225,0.995,1,0,0,0,0
GAL,48.6,-0.212,-0.359,-0.049,-0.349,-0.44,0.543,3,0,0,0,0
GGL,9.34,-0.333,-0.472,0.162,-0.206,-0.496,0.425,0,0,0,0,0
GHNI,76.84,-0.297,-0.43,-0.028,-0.56,-0.556,0.808,3,0,0,0,0
GLAXO,171.48,-0.009,0.019,0.631,0.175,-0.087,1.157,0,1,0,0,0
HCAR,149.96,-0.228,-0.307,0.03,-0.4,-0.383,0.725,2,0,0,0,0
HTL,27.74,-0.076,-0.121,-0.028,-0.425,-0.426,1.134,3,0,0,0,0
HUBC,76.38,-0.151,-0.224,0.04,0.008,-0.26,1.542,2,0,0,0,0
ILP,42.8,-0.247,-0.274,-0.056,,-0.297,0.319,3,1,1,0,0
INIL,87.49,-0.141,-0.248,0.038,-0.292,-0.295,0.865,1,0,0,0,0
ISL,41.93,-0.207,-0.294,-0.126,-0.355,-0.345,0.744,2,0,0,0,1
KEL,2.99,-0.221,-0.353,-0.272,-0.468,-0.465,1.408,0,0,0,0,0
KOHC,107.81,-0.033,0.375,0.915,0.241,-0.15,2.008,4,0,0,0,0
KTML,31.77,-0.216,-0.197,0.177,-0.293,-0.294,0.276,2,0,0,0,0
LCI,591.63,-0.144,-0.143,0.183,-0.092,-0.188,0.364,0,0,0,0,0
LOTCHEM,10.53,-0.165,-0.258,-0.288,-0.276,-0.387,0.674,0,1,0,0,0
LUCK,410.73,-0.187,-0.114,0.091,-0.058,-0.275,1.752,1,0,0,0,0
MARI,1085.98,-0.096,-0.171,0.095,-0.142,-0.253,1.55,1,0,0,0,0
MEBL,65.88,-0.318,-0.318,-0.138,-0.255,-0.38,1.616,0,0,0,0,0
MLCF,24.01,-0.098,-0.01,0.312,-0.381,-0.362,1.571,3,0,0,0,0
MTL,574.44,-0.124,-0.192,-0.033,-0.196,-0.237,0.53,1,0,1,0,0
MUGHAL,38.09,-0.132,-0.174,0.13,-0.021,-0.239,1.092,3,0,1,0,0
NETSOL,36.18,-0.324,-0.482,-0.406,-0.557,-0.556,1.05,3,0,0,0,0
NML,65.36,-0.391,-0.394,-0.281,-0.509,-0.514,1.335,0,0,1,0,0
NRL,101.31,-0.116,-0.322,-0.181,-0.404,-0.406,0.548,2,0,1,0,0
OGDC,88.17,-0.282,-0.41,-0.299,-0.411,-0.428,1.85,3,0,0,0,0
PAEL,21.18,-0.119,-0.269,0.127,-0.117,-0.282,0.655,1,1,2,0,0
PKGS,244.74,-0.333,-0.404,-0.172,-0.342,-0.453,1.009,0,1,1,0,0
POWER,6.55,-0.005,0.025,0.213,-0.189,-0.181,1.181,0,0,0,0,0
PPL,83.78,-0.278,-0.415,-0.272,-0.467,-0.451,1.911,1,0,0,0,0
PSO,138.4,-0.179,-0.332,-0.063,-0.231,-0.362,0.727,1,0,1,0,0
SEARL,174.81,-0.02,-0.102,0.053,-0.27,-0.268,0.818,1,0,1,0,0
SNGP,45.04,-0.338,-0.43,-0.32,-0.298,-0.459,0.713,1,0,0,0,0
SPEL,34.92,-0.065,-0.025,0.93,0.099,-0.128,0.39,0,0,0,0,0
SSGC,13.56,-0.18,-0.393,-0.259,-0.377,-0.452,0.504,0,0,0,0,0
STPL,7.91,-0.132,-0.314,-0.278,-0.572,-0.584,0.455,0,0,0,0,0
SYS,122.03,-0.201,-0.008,0.442,0.299,-0.223,0.835,2,1,1,0,0
TGL,55.62,-0.185,-0.272,0.086,-0.238,-0.344,1.31,1,0,0,0,0
TREET,14.03,-0.268,-0.394,-0.124,-0.34,-0.412,0.758,1,0,1,0,0
UNITY,10.51,-0.252,-0.366,0.03,-0.185,-0.391,0.771,0,0,0,0,0
WAFI,131.49,-0.242,-0.464,-0.106,-0.465,-0.505,0.492,0,0,0,0,0

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2020-03-13,GSKCH,material_info,Material Information REVOKED
2020-03-16,GHGL,material_info,Material Information
2020-03-16,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-16,SILK,material_info,Material Information
2020-03-16,GSKCH,material_info,Material Information
2020-03-17,CSAP,material_info,Material Information
2020-03-17,GSKCH,material_info,Material Information
2020-03-18,ASTL,material_info,Material Information
2020-03-20,FFC,material_info,Material Information
2020-03-20,FATIMA,material_info,Material Information
2020-03-24,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-24,786,material_info,Material Information
2020-03-24,SAZEW,material_info,Material Information
2020-03-25,SYS,material_info,Material Information
2020-03-25,CSAP,material_info,Material Information
2020-03-25,AKZO,material_info,Material Information
2020-03-25,ACPL,material_info,MATERIAL INFORMATION
2020-03-25,DSML,material_info,Material Information
2020-03-26,NRL,material_info,Material Information
2020-03-26,ACPL,material_info,Material Information
2020-03-26,GHGL,material_info,Material Information
2020-03-26,DGKC,material_info,Disclosure of Material Information - Temporary Suspension of Plant Operatio
2020-03-26,LOADS,material_info,Material Information
2020-03-26,TATM,material_info,Disclosure of Material Information
2020-03-26,SALT,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-26,ILTM,material_info,Disclosure of Material Information
2020-03-26,KOIL,material_info,Material Information - Appointment of Directors
2020-03-26,KOIL,material_info,Material Information - Appointment of Chief Executive Officer
2020-03-27,ELCM,material_info,Material Information
2020-03-27,MTIL,material_info,Material Information
2020-03-27,ATRL,material_info,MATERIAL INFORMATION
2020-03-27,GATM,material_info,Disclosure of Material Information
2020-03-27,BERG,material_info,Material Information
2020-03-27,ILP,material_info,Material Information
2020-03-27,HCL,material_info,Material Information for change in shareholding of directors and Chief Exec
2020-03-27,PAEL,material_info,Material Information
2020-03-27,AGTL,material_info,Material Information
2020-03-27,INDU,material_info,Material Information - Disclosure
2020-03-27,CTM,material_info,Material Information - Closure of Production
2020-03-27,BWCL,material_info,Material Information
2020-03-27,GADT,material_info,Material Information Regarding COVID-19
2020-03-27,MUGHAL,material_info,Material information
2020-03-27,BUXL,material_info,Material Information
2020-03-30,MTL,material_info,Material Information
2020-03-30,SAZEW,material_info,Material Information
2020-03-30,SMBL,material_info,"Disclosure of Material Information under Section 96 of the Securities Act, "
2020-03-30,NML,material_info,Disclosure of Material Information
2020-03-30,BYCO,material_info,Disclosure of Material Information
2020-03-30,AGIL,material_info,Material Information
2020-03-30,REDCO,material_info,Material Information - Suspension of Company's Operations due to COVID-19
2020-03-30,FZCM,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-30,KOHTM,material_info,Material Information
2020-03-30,DINT,material_info,Disclosure of Material Information
2020-03-30,CFL,material_info,MATERIAL INFORMATION.
2020-03-30,SAIF,material_info,Material Information
2020-03-30,QUET,material_info,Material Information
2020-03-30,DCR,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-30,SAPT,material_info,Material Information
2020-03-30,KML,material_info,Material Information
2020-03-30,SCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-30,BCL,material_info,Material Information
2020-03-30,PSEL,material_info,Material Information
2020-03-30,MSOT,material_info,Material Information
2020-03-31,NRSL,material_info,MATERIAL INFORMATION - NRsL
2020-03-31,EMCO,material_info,Material Information
2020-03-31,SMBL,material_info,"Disclosure of Material Information under section 96 of the Securities Act, "
2020-03-31,ATRL,material_info,MATERIAL INFORMATION
2020-03-31,ARUJ,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-31,PAEL,material_info,Material Information - SUSPENSION OF OPERATIONS DUE TO COVID-19
2020-03-31,ADMM,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-03-31,SSML,material_info,Material Information - SUSPENSION OF OPERATIONS DUE TO COVID-19
2020-03-31,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-04-01,ANL,material_info,Material Information - Temporary Suspension of Production Facilities
2020-04-01,AHTM,material_info,Material Information
2020-04-01,DCR,material_info,DISCLOSURE OF MATERIAL INFORMATION
2020-04-01,SILK,material_info,Material Information
2020-04-02,ICI,material_info,Material Information : COVID-19
2020-04-02,ILTM,material_info,Material Information Merger
2020-04-02,TATM,material_info,Material Information Merger
2020-04-02,SALT,material_info,Material Information Merger
2020-04-02,FFL,material_info,Disclosure of Material Information
2020-04-02,DEL,material_info,Material Information
2020-04-02,KSBP,material_info,Material Information
2020-04-03,BWHL,material_info,Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,2.072,2020-04-02
investor_type,last_5_sessions,broker proprietary trading,-0.196,2020-04-02
investor_type,last_5_sessions,companies,-0.095,2020-04-02
investor_type,last_5_sessions,foreign corporates,-30.549,2020-04-02
investor_type,last_5_sessions,foreign individual,0.286,2020-04-02
investor_type,last_5_sessions,individuals,14.018,2020-04-02
investor_type,last_5_sessions,insurance companies,5.954,2020-04-02
investor_type,last_5_sessions,mutual funds,7.4,2020-04-02
investor_type,last_5_sessions,nbfc,-0.007,2020-04-02
investor_type,last_5_sessions,other organization,0.763,2020-04-02
investor_type,last_5_sessions,overseas pakistani,0.353,2020-04-02
sector,last_5_sessions,fipi | All other Sectors,-3.642,2020-04-02
sector,last_5_sessions,fipi | Cement,-7.814,2020-04-02
sector,last_5_sessions,fipi | Commercial Banks,-6.908,2020-04-02
sector,last_5_sessions,fipi | Fertilizer,-0.482,2020-04-02
sector,last_5_sessions,fipi | Food and Personal Care Products,-0.059,2020-04-02
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-9.777,2020-04-02
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,-0.195,2020-04-02
sector,last_5_sessions,fipi | Power Generation and Distribution,-0.04,2020-04-02
sector,last_5_sessions,fipi | Technology and Communication,0.259,2020-04-02
sector,last_5_sessions,fipi | Textile Composite,-1.252,2020-04-02
sector,last_5_sessions,lipi banks / dfi | All other Sectors,-0.254,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Cement,-0.009,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,0.797,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Fertilizer,0.682,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,0.002,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.581,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-0.026,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,0.077,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,0.166,2020-04-02
sector,last_5_sessions,lipi banks / dfi | Textile Composite,0.057,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,-0.268,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.104,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.327,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,0.08,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.061,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.328,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,-0.042,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.44,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,-0.098,2020-04-02
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.126,2020-04-02
sector,last_5_sessions,lipi companies | All other Sectors,-0.115,2020-04-02
sector,last_5_sessions,lipi companies | Cement,1.259,2020-04-02
sector,last_5_sessions,lipi companies | Commercial Banks,-1.242,2020-04-02
sector,last_5_sessions,lipi companies | Fertilizer,-0.274,2020-04-02
sector,last_5_sessions,lipi companies | Food and Personal Care Products,-0.294,2020-04-02
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,1.075,2020-04-02
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,-0.065,2020-04-02
sector,last_5_sessions,lipi companies | Power Generation and Distribution,-0.284,2020-04-02
sector,last_5_sessions,lipi companies | Technology and Communication,-0.032,2020-04-02
sector,last_5_sessions,lipi companies | Textile Composite,-0.124,2020-04-02
sector,last_5_sessions,lipi individuals | All other Sectors,1.474,2020-04-02
sector,last_5_sessions,lipi individuals | Cement,5.802,2020-04-02
sector,last_5_sessions,lipi individuals | Commercial Banks,1.36,2020-04-02
sector,last_5_sessions,lipi individuals | Fertilizer,-0.746,2020-04-02
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,0.106,2020-04-02
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,4.774,2020-04-02
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.081,2020-04-02
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,0.536,2020-04-02
sector,last_5_sessions,lipi individuals | Technology and Communication,-0.281,2020-04-02
sector,last_5_sessions,lipi individuals | Textile Composite,1.075,2020-04-02
sector,last_5_sessions,lipi insurance companies | All other Sectors,0.611,2020-04-02
sector,last_5_sessions,lipi insurance companies | Cement,-0.152,2020-04-02
sector,last_5_sessions,lipi insurance companies | Commercial Banks,2.194,2020-04-02
sector,last_5_sessions,lipi insurance companies | Fertilizer,0.474,2020-04-02
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.0,2020-04-02
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,1.493,2020-04-02
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.468,2020-04-02
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,0.722,2020-04-02
sector,last_5_sessions,lipi insurance companies | Technology and Communication,0.055,2020-04-02
sector,last_5_sessions,lipi insurance companies | Textile Composite,0.089,2020-04-02
sector,last_5_sessions,lipi mutual funds | All other Sectors,2.337,2020-04-02
sector,last_5_sessions,lipi mutual funds | Cement,0.44,2020-04-02
sector,last_5_sessions,lipi mutual funds | Commercial Banks,3.207,2020-04-02
sector,last_5_sessions,lipi mutual funds | Fertilizer,0.173,2020-04-02
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,0.306,2020-04-02
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,1.414,2020-04-02
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-0.034,2020-04-02
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,-0.423,2020-04-02
sector,last_5_sessions,lipi mutual funds | Technology and Communication,-0.043,2020-04-02
sector,last_5_sessions,lipi mutual funds | Textile Composite,0.023,2020-04-02
sector,last_5_sessions,lipi nbfc | All other Sectors,0.016,2020-04-02
sector,last_5_sessions,lipi nbfc | Cement,-0.018,2020-04-02
sector,last_5_sessions,lipi nbfc | Commercial Banks,0.001,2020-04-02
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.003,2020-04-02
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.002,2020-04-02
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.0,2020-04-02
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.009,2020-04-02
sector,last_5_sessions,lipi nbfc | Textile Composite,0.007,2020-04-02
sector,last_5_sessions,lipi other organization | All other Sectors,-0.158,2020-04-02
sector,last_5_sessions,lipi other organization | Cement,0.389,2020-04-02
sector,last_5_sessions,lipi other organization | Commercial Banks,0.264,2020-04-02
sector,last_5_sessions,lipi other organization | Fertilizer,0.096,2020-04-02
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,0.113,2020-04-02
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.026,2020-04-02
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,-0.138,2020-04-02
sector,last_5_sessions,lipi other organization | Technology and Communication,-0.026,2020-04-02
sector,last_5_sessions,lipi other organization | Textile Composite,0.25,2020-04-02
investor_type,last_20_sessions,banks / dfi,22.215,2020-04-02
investor_type,last_20_sessions,broker proprietary trading,-0.389,2020-04-02
investor_type,last_20_sessions,companies,-4.474,2020-04-02
investor_type,last_20_sessions,foreign corporates,-89.397,2020-04-02
investor_type,last_20_sessions,foreign individual,0.158,2020-04-02
investor_type,last_20_sessions,individuals,32.639,2020-04-02
investor_type,last_20_sessions,insurance companies,58.229,2020-04-02
investor_type,last_20_sessions,mutual funds,-19.251,2020-04-02
investor_type,last_20_sessions,nbfc,-1.204,2020-04-02
investor_type,last_20_sessions,other organization,1.413,2020-04-02
investor_type,last_20_sessions,overseas pakistani,0.062,2020-04-02
sector,last_20_sessions,fipi | All other Sectors,-11.765,2020-04-02
sector,last_20_sessions,fipi | Cement,-23.007,2020-04-02
sector,last_20_sessions,fipi | Commercial Banks,-17.33,2020-04-02
sector,last_20_sessions,fipi | Fertilizer,-8.535,2020-04-02
sector,last_20_sessions,fipi | Food and Personal Care Products,0.001,2020-04-02
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-22.775,2020-04-02
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,-1.072,2020-04-02
sector,last_20_sessions,fipi | Power Generation and Distribution,-3.368,2020-04-02
sector,last_20_sessions,fipi | Technology and Communication,-0.041,2020-04-02
sector,last_20_sessions,fipi | Textile Composite,-1.285,2020-04-02
sector,last_20_sessions,lipi banks / dfi | All other Sectors,0.6,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Cement,2.126,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,5.245,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Fertilizer,7.303,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,0.097,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,5.208,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,0.879,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,0.475,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,0.227,2020-04-02
sector,last_20_sessions,lipi banks / dfi | Textile Composite,0.055,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-0.634,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Cement,-0.935,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,2.243,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-0.904,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.049,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.81,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.167,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.289,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-0.318,2020-04-02
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,-0.577,2020-04-02
sector,last_20_sessions,lipi companies | All other Sectors,4.001,2020-04-02
sector,last_20_sessions,lipi companies | Cement,1.629,2020-04-02
sector,last_20_sessions,lipi companies | Commercial Banks,-13.364,2020-04-02
sector,last_20_sessions,lipi companies | Fertilizer,-0.322,2020-04-02
sector,last_20_sessions,lipi companies | Food and Personal Care Products,-0.263,2020-04-02
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,-0.114,2020-04-02
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,1.507,2020-04-02
sector,last_20_sessions,lipi companies | Power Generation and Distribution,0.419,2020-04-02
sector,last_20_sessions,lipi companies | Technology and Communication,1.353,2020-04-02
sector,last_20_sessions,lipi companies | Textile Composite,0.679,2020-04-02
sector,last_20_sessions,lipi individuals | All other Sectors,-12.932,2020-04-02
sector,last_20_sessions,lipi individuals | Cement,0.067,2020-04-02
sector,last_20_sessions,lipi individuals | Commercial Banks,12.149,2020-04-02
sector,last_20_sessions,lipi individuals | Fertilizer,5.698,2020-04-02
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,-0.216,2020-04-02
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,24.81,2020-04-02
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,0.046,2020-04-02
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,2.147,2020-04-02
sector,last_20_sessions,lipi individuals | Technology and Communication,-1.549,2020-04-02
sector,last_20_sessions,lipi individuals | Textile Composite,2.419,2020-04-02
sector,last_20_sessions,lipi insurance companies | All other Sectors,13.06,2020-04-02
sector,last_20_sessions,lipi insurance companies | Cement,11.366,2020-04-02
sector,last_20_sessions,lipi insurance companies | Commercial Banks,13.872,2020-04-02
sector,last_20_sessions,lipi insurance companies | Fertilizer,4.96,2020-04-02
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,0.083,2020-04-02
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,9.458,2020-04-02
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,1.639,2020-04-02
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,3.984,2020-04-02
sector,last_20_sessions,lipi insurance companies | Technology and Communication,0.262,2020-04-02
sector,last_20_sessions,lipi insurance companies | Textile Composite,-0.455,2020-04-02
sector,last_20_sessions,lipi mutual funds | All other Sectors,8.247,2020-04-02
sector,last_20_sessions,lipi mutual funds | Cement,9.022,2020-04-02
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-3.247,2020-04-02
sector,last_20_sessions,lipi mutual funds | Fertilizer,-8.501,2020-04-02
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,0.301,2020-04-02
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-17.613,2020-04-02
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-2.97,2020-04-02
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-3.277,2020-04-02
sector,last_20_sessions,lipi mutual funds | Technology and Communication,0.112,2020-04-02
sector,last_20_sessions,lipi mutual funds | Textile Composite,-1.326,2020-04-02
sector,last_20_sessions,lipi nbfc | All other Sectors,0.055,2020-04-02
sector,last_20_sessions,lipi nbfc | Cement,-0.748,2020-04-02
sector,last_20_sessions,lipi nbfc | Commercial Banks,0.081,2020-04-02
sector,last_20_sessions,lipi nbfc | Fertilizer,0.052,2020-04-02
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.283,2020-04-02
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.186,2020-04-02
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,0.002,2020-04-02
sector,last_20_sessions,lipi nbfc | Technology and Communication,0.044,2020-04-02
sector,last_20_sessions,lipi nbfc | Textile Composite,-0.222,2020-04-02
sector,last_20_sessions,lipi other organization | All other Sectors,-0.633,2020-04-02
sector,last_20_sessions,lipi other organization | Cement,0.48,2020-04-02
sector,last_20_sessions,lipi other organization | Commercial Banks,0.352,2020-04-02
sector,last_20_sessions,lipi other organization | Fertilizer,0.247,2020-04-02
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-0.051,2020-04-02
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,0.499,2020-04-02
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,-0.011,2020-04-02
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,-0.092,2020-04-02
sector,last_20_sessions,lipi other organization | Technology and Communication,-0.09,2020-04-02
sector,last_20_sessions,lipi other organization | Textile Composite,0.711,2020-04-02

=== FILE: calendar.md ===
# Calendar as of 2020-04-03

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2020-03-10 SSGC: Board Meeting Other Than Financial Results
- 2020-03-11 GLAXO: Board Meeting - Number of Directors
- 2020-03-18 SYS: Board Meeting
- 2020-03-19 KEL: Board Meeting.
- 2020-03-20 ISL: BOARD MEETING TO REVIEW BUSINESS STRATEGY
- 2020-03-25 KEL: KEL | K-Electric Limited-Postponement of KE Board of Directors Meeting
- 2020-03-30 FCCL: Notice of the Board Meeting
- 2020-04-02 KEL: Board Meeting to consider financial statements
- 2020-04-03 ISL: BOARD MEETING TO REVIEW QUARTERLY FINANCIAL RESULTS FOR THE PERIOD ENDED 31-03-2020

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
| 12 | Six SOEs sold in FY20 | 29 Jan 2020 | outcome not shown |

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
