# Replay bundle, close of 2025-05-16

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
# Market as of 2025-05-16 close (public information only)

- KSE100: 119,649 on 2025-05-16; 1m +3.1%, 3m +5.9%, 6m +28.3%, 12m +64.8%
- KMI All Share: 51,415 on 2025-05-16; 1m +1.7%, 3m +6.4%, 6m +24.9%, 12m +52.5%
- Policy rate 11.0%; last MPC decision 2025-05-05: cut (-100bp)
- 6M T-bill cutoff 11.28% (auction 2025-05-14); 3M 11.24%, 12M 11.35%
- CPI YoY 0.26% for 2025-04 (published by 2025-05-03); three months earlier (2025-01) 2.42%
- Brent: 65.20 USD/bbl on 2025-05-16; 3-month change -13.3%
- USD/PKR: 281.61  on 2025-05-16; 3-month change +0.9%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.28pp (market near policy rate); CPI falling over 3 months (-2.2pp)
- Next MPC: see SBP calendar

Session date used: 2025-05-16. Liquid KMI names: 100 (membership KMI_ALL_derived_2025-01-03.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.0532,-0.0319,0.219,0,0
E&P,3,0.0057,0.042,0.2715,0,0
OMC,4,-0.0082,-0.0771,0.2233,0,0
Power,6,-0.0628,-0.0499,-0.0073,0,0
Fertilizer,4,0.027,-0.0364,0.2413,0,1
Cement,16,0.0842,0.1839,0.4041,2,3
Steel & engineering,11,0.0693,0.0562,0.1942,0,0
Autos,12,-0.0259,-0.0619,0.1532,0,0
Tech & telecom,11,0.0271,-0.0759,0.093,0,0
Islamic banks & fin.,8,0.0326,0.071,0.1562,1,1
Pharma,14,-0.035,-0.055,0.3905,1,1
Textiles,23,0.0285,-0.0401,0.0384,2,2
Food & staples,15,0.004,0.0197,0.2269,1,3
Chemicals,18,0.0376,0.0891,0.2871,3,3
"Glass, packaging, paper",14,0.0136,0.068,0.1066,0,2
Gas utilities & misc,12,-0.0015,0.0614,0.2706,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ABOT,979.75,-0.068,-0.192,-0.008,0.621,-0.239,0.708,1,2025-03-31,0.054,2,0,0,0,,
ACPL,321.85,0.139,0.297,0.859,2.466,0.0,0.873,0,2024-12-31,,2,0,0,0,3.743,0.067
AGP,185.29,-0.052,0.128,0.215,1.139,-0.128,1.446,1,2025-03-31,1.126,2,0,0,0,17.84,0.024
AGTL,427.44,-0.112,-0.292,0.006,0.162,-0.383,0.988,1,2025-03-31,-1.119,2,1,0,0,9.191,
AIRLINK,159.96,-0.099,-0.155,0.268,1.245,-0.272,0.501,1,2025-03-31,-0.485,2,0,0,0,7.591,0.068
ATBA,277.67,-0.203,-0.251,-0.244,0.056,-0.446,1.266,2,,,2,0,0,0,,
ATLH,1145.83,0.058,0.342,0.317,1.415,-0.04,1.296,0,,,1,0,0,0,,
ATRL,608.32,0.001,-0.047,0.3,0.577,-0.172,0.641,1,2025-03-31,-1.176,2,0,0,0,1.496,0.043
AVN,51.21,0.023,-0.087,-0.103,-0.079,-0.244,0.818,1,2025-03-31,,4,0,0,0,,
BBFL,50.57,0.072,0.057,-0.286,,-0.395,1.707,1,,,2,0,0,0,,
BFAGRO,28.64,0.072,,,,,1.081,1,,,2,1,0,0,,
BFBIO,168.03,0.081,-0.228,0.737,,,0.675,3,2025-03-31,-0.374,2,0,0,0,,
BIPL,20.08,-0.042,-0.11,-0.043,-0.026,-0.18,1.412,0,2025-03-31,-0.183,2,1,0,0,,
BNL,33.89,0.524,1.405,1.449,1.016,-0.008,3.204,4,,,2,0,0,0,,
BWCL,403.84,0.014,0.132,0.344,0.878,-0.066,0.886,0,,,2,0,0,0,,
CEPB,24.06,-0.048,-0.197,-0.197,-0.194,-0.326,0.622,0,2025-03-31,-1.423,2,0,0,0,,
CHCC,267.16,-0.013,0.016,-0.035,0.649,-0.128,0.771,1,2025-03-31,0.355,2,0,0,0,5.763,0.034
CLOV,37.65,-0.125,-0.041,0.122,-0.033,-0.209,0.911,0,2024-12-31,,2,2,0,0,,
CNERGY,7.68,-0.098,0.031,0.67,0.774,-0.111,0.596,1,2024-06-30,,2,0,0,0,114.054,
CPHL,87.45,-0.091,-0.179,0.849,1.768,-0.179,0.417,2,2025-03-31,0.032,2,0,0,0,7.812,0.114
CSAP,121.92,0.194,0.149,0.179,1.159,-0.08,0.825,1,2025-03-31,0.298,2,0,0,0,3.297,0.102
DCL,10.37,0.075,0.216,0.223,0.438,-0.062,2.198,1,,,2,0,0,0,,
DCR,26.24,0.015,0.183,0.41,0.881,-0.001,0.904,0,2025-03-31,0.16,2,0,0,0,4.494,0.122
DGKC,147.33,0.195,0.352,0.702,0.814,-0.026,1.021,1,2025-03-31,0.64,2,0,0,0,63.696,
DOL,28.97,0.159,0.248,0.53,0.5,0.0,1.124,1,,,2,0,0,0,,
EFERT,181.07,-0.04,-0.124,-0.045,0.259,-0.205,1.166,1,2025-03-31,-0.626,2,0,0,0,9.648,0.105
ENGROH,176.58,0.03,-0.16,0.122,0.06,-0.358,1.324,1,2025-03-31,-0.626,2,0,0,0,9.7,0.04
EPCL,33.14,-0.089,-0.1,-0.086,-0.224,-0.311,0.908,0,2025-03-31,,1,1,0,0,,
FABL,48.53,0.05,0.062,0.129,0.434,-0.08,0.95,0,2025-03-31,-0.182,3,0,0,0,3.08,0.144
FATIMA,86.53,0.05,0.126,0.414,0.805,-0.006,0.831,1,2025-03-31,-0.002,2,0,0,0,4.517,0.089
FCCL,47.94,0.066,0.239,0.492,1.234,-0.012,0.756,1,2025-03-31,0.208,2,0,0,0,6.834,0.044
FCEPL,104.52,0.217,0.391,0.204,0.5,0.0,1.736,2,2024-09-30,2.03,2,0,0,0,31.055,0.031
FCL,24.16,-0.017,-0.068,0.044,,-0.146,0.539,1,2025-03-31,-0.37,3,0,0,0,7.966,0.052
FEROZ,279.28,-0.094,-0.203,-0.133,0.199,-0.276,0.633,1,,,2,0,0,0,,
FFL,15.17,-0.046,0.028,0.48,0.537,-0.215,0.526,1,2025-03-31,2.25,2,0,0,0,68.835,
FLYNG,50.67,0.816,1.01,1.144,5.105,0.0,0.528,6,,,2,0,0,0,,
GAL,472.47,-0.008,0.036,0.86,2.595,-0.065,0.634,1,2025-03-31,6.437,2,0,0,0,27.284,
GATM,22.18,-0.063,-0.108,0.092,0.065,-0.191,0.431,1,2025-03-31,0.1,2,0,0,0,3.218,
GGGL,8.34,-0.072,0.056,0.322,0.212,-0.19,0.4,1,,,2,0,0,0,,
GGL,13.72,0.016,-0.012,0.304,0.31,-0.18,0.388,1,2025-03-31,1.024,2,0,0,0,6.416,
GHGL,32.83,-0.041,0.135,0.31,0.251,-0.102,0.549,1,2025-03-31,-0.035,2,0,0,0,,
GHNI,686.26,-0.004,0.091,0.695,1.469,-0.102,0.79,1,2025-03-31,3.032,2,0,0,0,14.907,
GLAXO,379.09,-0.129,-0.037,0.198,2.129,-0.188,1.437,1,2025-03-31,2.753,2,0,0,0,19.339,0.025
GTYR,37.81,-0.053,-0.175,-0.064,-0.155,-0.315,0.466,1,2025-03-31,-0.2,2,0,0,0,,
GWLC,41.07,0.052,-0.072,0.029,0.72,-0.274,0.463,1,2025-03-31,-0.158,2,0,0,0,,
HALEON,734.27,-0.095,-0.081,-0.053,1.806,-0.204,0.792,0,2025-03-31,1.074,2,1,0,0,20.65,0.025
HCAR,298.97,0.002,-0.04,-0.042,-0.05,-0.128,0.828,1,2024-12-31,2.97,0,0,0,0,13.638,0.029
HINOON,921.16,-0.011,0.104,0.089,0.478,-0.026,1.086,1,2025-03-31,0.217,2,0,0,0,,
HTL,41.33,-0.028,-0.147,0.068,0.56,-0.318,0.237,1,,,2,0,0,0,,
HUBC,140.73,-0.008,0.107,0.322,0.124,-0.073,0.907,1,2025-03-31,-0.358,2,1,0,0,3.021,0.123
ILP,57.02,-0.049,-0.073,-0.097,-0.274,-0.322,0.569,1,2025-03-31,-0.627,2,0,0,0,6.013,0.064
IMAGE,23.11,0.006,0.224,0.594,0.695,-0.088,0.889,1,2025-03-31,-0.497,2,0,0,0,,
INIL,153.29,0.0,-0.06,0.011,0.001,-0.296,0.675,1,2025-03-31,0.925,2,1,0,0,11.902,0.028
ISL,81.24,0.076,0.003,0.097,0.132,-0.233,0.368,1,2025-03-31,-0.407,3,1,0,0,10.063,0.065
KEL,4.4,-0.007,-0.02,-0.142,-0.06,-0.312,0.811,0,2024-06-30,-0.871,0,0,0,0,30.127,
KOHC,386.32,0.0,0.044,-0.082,0.775,-0.134,0.455,1,2025-03-31,0.138,2,0,0,0,5.515,
KSBP,166.73,-0.03,0.098,0.221,0.413,-0.096,1.135,0,2025-03-31,,3,0,0,0,,
LCI,1576.16,0.094,0.407,0.359,1.043,0.0,1.422,0,2025-03-31,-0.099,2,1,0,0,7.699,0.065
LOTCHEM,20.98,0.172,0.006,0.212,0.165,-0.098,0.399,1,2025-03-31,-0.254,2,0,0,0,11.982,0.239
LPL,23.75,-0.123,-0.138,0.106,0.08,-0.227,0.93,1,,,2,0,0,0,,
LUCK,342.37,-0.008,0.405,0.73,1.033,-0.046,3.764,1,2025-03-31,0.151,2,1,0,0,4.053,0.016
MARI,641.08,-0.024,0.091,0.504,1.132,-0.288,0.708,1,2025-03-31,0.137,2,0,0,0,4.682,0.086
MEBL,286.62,0.162,0.274,0.33,0.518,0.0,1.092,0,2025-03-31,-0.116,2,0,0,0,4.229,0.116
MFFL,196.36,-0.072,-0.318,0.079,0.261,-0.382,0.552,2,,,2,1,0,0,,
MLCF,74.78,0.231,0.659,0.795,0.994,-0.021,1.234,1,2024-12-31,0.708,2,1,0,0,5.919,
MTL,580.79,-0.038,-0.048,0.067,0.031,-0.148,0.677,0,2025-03-31,-0.513,2,0,0,0,11.845,0.039
MUGHAL,72.18,0.037,-0.043,0.051,0.021,-0.265,0.884,1,2025-03-31,1.194,2,0,0,0,16.363,
NETSOL,140.24,0.023,-0.089,0.073,0.234,-0.173,0.58,1,2025-03-31,15.667,2,0,0,0,9.912,0.022
NML,109.04,-0.03,0.172,0.422,0.566,-0.136,1.286,1,2025-03-31,-0.5,2,0,0,0,3.166,0.042
NRL,233.91,-0.062,-0.073,-0.014,-0.23,-0.288,0.681,2,2025-03-31,,2,0,0,0,,
OCTOPUS,54.1,-0.034,-0.116,-0.238,-0.157,-0.538,0.614,2,,,4,0,0,0,,
OGDC,211.5,0.015,0.052,0.125,0.705,-0.084,0.987,1,2025-03-31,-0.014,2,0,0,0,2.786,0.075
PABC,107.56,-0.022,-0.015,0.288,0.674,-0.219,0.577,1,,,2,0,0,0,,
PAEL,45.34,-0.025,0.119,0.622,0.764,-0.06,0.638,1,2025-03-31,0.392,2,1,0,0,16.997,
PIBTL,8.72,-0.169,0.054,0.09,0.35,-0.211,0.758,1,2025-03-31,-2.368,2,0,0,0,6.244,
PIOC,217.45,-0.012,0.188,0.168,0.474,-0.042,0.756,1,2025-03-31,-0.189,2,0,0,0,7.401,0.089
POWER,14.85,0.254,0.597,1.216,1.812,-0.022,1.672,0,2025-03-31,,2,0,0,0,,
PPL,172.39,0.023,-0.027,0.161,0.435,-0.17,1.059,2,2025-03-31,-0.213,2,1,0,0,2.759,0.051
PREMA,49.83,-0.056,0.881,1.818,2.413,-0.426,2.347,2,2025-03-31,0.5,2,1,0,0,8.672,
PRL,33.43,-0.031,-0.029,0.244,0.235,-0.246,0.772,1,2025-03-31,,2,0,0,0,3.599,0.086
PSO,379.95,-0.012,0.04,0.542,1.136,-0.147,0.804,1,2025-03-31,-0.287,2,0,0,0,4.258,0.06
SAZEW,1299.82,0.121,0.168,0.228,0.811,-0.043,1.586,0,2025-03-31,1.053,2,0,0,0,6.341,0.024
SEARL,86.36,-0.081,-0.18,0.104,0.537,-0.309,0.585,2,2025-03-31,,2,0,0,0,,
SHFA,458.85,0.049,0.072,0.232,2.49,-0.101,0.309,1,,,3,1,0,0,,
SLGL,15.96,0.026,0.05,-0.009,0.644,-0.178,1.387,1,2025-03-31,0.146,4,0,0,0,7.077,
SNGP,119.9,0.134,0.39,0.474,0.844,-0.025,1.446,1,2024-12-31,0.346,2,0,0,0,2.121,0.118
SPEL,39.78,0.027,-0.024,-0.057,1.768,-0.256,0.717,1,2025-03-31,1.387,2,0,0,0,,
SSGC,35.69,-0.103,-0.015,0.741,2.475,-0.279,1.063,2,2024-06-30,-0.97,1,0,0,0,1.007,
SYM,15.28,0.078,-0.17,0.491,3.108,-0.279,0.601,1,2025-03-31,0.154,2,0,0,0,,
SYS,543.79,0.114,-0.014,0.06,0.44,-0.129,1.406,1,2025-03-31,0.583,2,0,0,0,24.356,0.01
TELE,7.46,0.019,-0.125,0.01,-0.119,-0.291,0.749,0,2025-03-31,,2,0,0,0,210.275,
TGL,207.81,0.009,0.599,0.666,0.959,-0.017,0.652,1,2025-03-31,0.637,2,0,0,0,4.587,
THCCL,190.63,-0.079,-0.036,0.78,4.11,-0.163,0.718,1,2025-03-31,0.017,2,1,0,0,2.244,0.028
TOMCL,31.67,-0.069,-0.067,-0.112,-0.069,-0.316,1.682,1,2025-03-31,-0.253,2,0,0,0,10.506,
TPLP,8.92,-0.11,-0.278,0.128,-0.208,-0.43,0.564,1,,,2,1,0,0,,
TREET,19.91,-0.049,-0.059,0.253,0.181,-0.291,0.422,1,2025-03-31,-0.109,2,0,0,0,,
UNITY,27.12,-0.024,-0.102,0.022,0.077,-0.305,0.606,1,2025-03-31,,2,0,0,0,,
WAFI,167.2,-0.079,-0.15,0.11,0.146,-0.318,0.492,1,2025-03-31,1.776,2,0,0,0,13.796,0.024
WAVES,7.54,-0.012,-0.092,0.034,-0.022,-0.186,0.884,0,2025-03-31,3.364,2,0,0,0,2.445,
ZAL,15.89,0.104,,,,,1.656,0,2025-03-31,0.645,2,1,0,0,,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2025-04-30,CSIL,material_info,Material Information
2025-05-02,RMPL,material_info,Material Information
2025-05-02,THCCL,material_info,Material Information
2025-05-02,BAFL,material_info,Material Information - Completion of Divestiture of Shareholding in Alfalah
2025-05-02,MERIT,material_info,DISCLOSURE OF MATERIAL INFORMATION
2025-05-02,FNEL,material_info,Material Information
2025-05-05,HASCOL,material_info,Material Information - Hascol welcomes the new Chief Executive Officer
2025-05-06,BIPL,material_info,Disclosure of Material Information
2025-05-06,ZAL,material_info,Material Information
2025-05-06,BAHL,material_info,BAHL - Disclosure of Material Information
2025-05-06,PREMA,material_info,Material Information - Unusual Movement in Share Price
2025-05-07,INIL,material_info,"MATERIAL INFORMATION INCORPORATION OF ""INIL EUROPE LIMITED"""
2025-05-07,HAEL,material_info,Material Information
2025-05-07,STPL,material_info,Material Information- Appointment of new auditor
2025-05-08,OML,material_info,Material Information
2025-05-08,CASH,material_info,Material Information
2025-05-08,FFC,material_info,Material Information
2025-05-09,MLCF,material_info,MLCF-Disclosure of Material Information
2025-05-09,ISL,material_info,Material Information
2025-05-09,BCL,material_info,Material Information
2025-05-09,MFL,material_info,Material Information
2025-05-12,SHFA,material_info,Discloser of Material Information
2025-05-12,GFIL,material_info,Material Information
2025-05-12,CLOV,material_info,Material Information
2025-05-13,LCI,material_info,Material Information
2025-05-13,AMBL,material_info,Material Information
2025-05-13,AASM,material_info,Material information
2025-05-14,PPL,material_info,Material Information - Appointment of a Director - Mr. Zafar Abbas
2025-05-14,LUCK,material_info,Material Information
2025-05-14,AATM,material_info,MATERIAL INFORMATION
2025-05-14,AGTL,material_info,Disclosure of Material Information
2025-05-15,ZIL,material_info,Material Information
2025-05-15,MFFL,material_info,Disclosure of Material Information
2025-05-15,HUBC,material_info,Material Information
2025-05-16,TRG,material_info,Material Information
2025-05-16,BILF,material_info,MATERIAL INFORMATION

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-10.83,2025-05-15
investor_type,last_5_sessions,broker proprietary trading,7.159,2025-05-15
investor_type,last_5_sessions,companies,-6.66,2025-05-15
investor_type,last_5_sessions,foreign corporates,-8.123,2025-05-15
investor_type,last_5_sessions,foreign individual,-0.027,2025-05-15
investor_type,last_5_sessions,individuals,-16.316,2025-05-15
investor_type,last_5_sessions,insurance companies,5.964,2025-05-15
investor_type,last_5_sessions,mutual funds,35.017,2025-05-15
investor_type,last_5_sessions,nbfc,0.033,2025-05-15
investor_type,last_5_sessions,other organization,-3.554,2025-05-15
investor_type,last_5_sessions,overseas pakistani,-2.662,2025-05-15
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-6.825,2025-05-15
sector,last_5_sessions,lipi banks / dfi | Cement,-3.903,2025-05-15
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,4.081,2025-05-15
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,-5.72,2025-05-15
sector,last_5_sessions,lipi individuals | Commercial Banks,-4.782,2025-05-15
sector,last_5_sessions,lipi individuals | Fertilizer,-7.213,2025-05-15
sector,last_5_sessions,lipi insurance companies | Fertilizer,7.704,2025-05-15
sector,last_5_sessions,lipi mutual funds | All other Sectors,7.996,2025-05-15
sector,last_5_sessions,lipi mutual funds | Cement,5.573,2025-05-15
sector,last_5_sessions,lipi mutual funds | Commercial Banks,4.012,2025-05-15
sector,last_5_sessions,lipi mutual funds | Debt Market,-4.289,2025-05-15
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,10.071,2025-05-15
investor_type,last_20_sessions,banks / dfi,93.586,2025-05-15
investor_type,last_20_sessions,broker proprietary trading,4.341,2025-05-15
investor_type,last_20_sessions,companies,3.117,2025-05-15
investor_type,last_20_sessions,foreign corporates,-13.567,2025-05-15
investor_type,last_20_sessions,foreign individual,0.036,2025-05-15
investor_type,last_20_sessions,individuals,-20.407,2025-05-15
investor_type,last_20_sessions,insurance companies,-8.097,2025-05-15
investor_type,last_20_sessions,mutual funds,-83.543,2025-05-15
investor_type,last_20_sessions,nbfc,0.444,2025-05-15
investor_type,last_20_sessions,other organization,22.966,2025-05-15
investor_type,last_20_sessions,overseas pakistani,1.125,2025-05-15
sector,last_20_sessions,fipi | Cement,9.809,2025-05-15
sector,last_20_sessions,fipi | Commercial Banks,-10.87,2025-05-15
sector,last_20_sessions,lipi banks / dfi | Cement,-8.294,2025-05-15
sector,last_20_sessions,lipi banks / dfi | Debt Market,100.087,2025-05-15
sector,last_20_sessions,lipi individuals | All other Sectors,-13.842,2025-05-15
sector,last_20_sessions,lipi individuals | Fertilizer,-9.978,2025-05-15
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,7.428,2025-05-15
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-14.18,2025-05-15
sector,last_20_sessions,lipi insurance companies | Fertilizer,8.139,2025-05-15
sector,last_20_sessions,lipi mutual funds | All other Sectors,8.674,2025-05-15
sector,last_20_sessions,lipi mutual funds | Debt Market,-102.641,2025-05-15
sector,last_20_sessions,lipi other organization | Commercial Banks,13.605,2025-05-15

=== FILE: calendar.md ===
# Calendar as of 2025-05-16

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2025-04-17 TPLP: Board Meeting
- 2025-04-17 MARI: Notice of Board of Directors Meeting
- 2025-04-17 GATM: BOARD MEETING
- 2025-04-17 POWER: Board Meeting
- 2025-04-17 FATIMA: Board Meeting and Closed Period
- 2025-04-17 GLAXO: Board Meeting Quarter ended March 31, 2025
- 2025-04-17 ACPL: Board Meeting
- 2025-04-17 ATBA: BOARD MEETING
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
- 2025-04-18 DGKC: BOARD MEETING
- 2025-04-21 OGDC: Board Meeting Rescheduled
- 2025-04-21 UNITY: Board Meeting
- 2025-04-21 ABOT: Board Meeting
- 2025-04-21 DCL: Board Meeting
- 2025-04-21 GGGL: MEETING OF THE BOARD OF DIRECTORS - GHANI GLOBAL GLASS LIMITED
- 2025-04-21 GGL: MEETING OF THE BOARD OF DIRECTORS - GHANI GLOBAL HOLDINGS LIMITED
- 2025-04-21 TOMCL: Board Meeting
- 2025-04-21 PAEL: Board Meeting for the 1st Quarter ended 31-03-2025
- 2025-04-21 IMAGE: Board Meeting
- 2025-04-21 BFBIO: Board Meeting
- 2025-04-21 BBFL: Board Meeting
- 2025-04-21 KOHC: Board Meeting
- 2025-04-21 PREMA: Board Meeting
- 2025-04-21 ZAL: Board Meeting
- 2025-04-21 HTL: Board Meeting REVOKED
- 2025-04-21 HUBC: Board Meeting - The Hub Power Company Limited
- 2025-04-21 LPL: BOARD MEETING
- 2025-04-21 HTL: Board Meeting
- 2025-04-22 AGP: Board Meeting
- 2025-04-22 ILP: Notice of Board Meeting for the Third Quarter ended March 31, 2025 / Closed Period
- 2025-04-22 PSO: Board Meeting
- 2025-04-22 MUGHAL: Notice of Board Meeting - QIII - FY 2025
- 2025-04-22 CSAP: Board Meetings
- 2025-04-22 SYM: Board Meeting
- 2025-04-22 FEROZ: Board Meeting
- 2025-04-22 DCR: BOARD MEETING / CLOSED PERIOD
- 2025-04-22 PABC: Board Meeting For 1st Quarter 2025 Financial Results and Other Matters
- 2025-04-22 OCTOPUS: Board Meeting
- 2025-04-22 AVN: Board Meeting
- 2025-04-22 FCL: Notice of the Board Meeting
- 2025-04-22 PIOC: Board Meeting
- 2025-04-22 NML: BOARD MEETING
- 2025-04-22 GHGL: Board Meeting
- 2025-04-23 CPHL: Board Meeting
- 2025-04-23 ATLH: Board Meeting
- 2025-04-23 NETSOL: Board Meeting
- 2025-04-23 TELE: Board Meeting to Consider Quarterly Accounts for the period ended 31 March 2025
- 2025-04-23 DOL: Board Meetings
- 2025-04-23 HINOON: Board Meeting
- 2025-04-23 SEARL: Board Meeting
- 2025-04-23 BNL: Board Meeting
- 2025-04-23 CNERGY: Board Meeting and Closed Period
- 2025-04-23 WAVES: Board Meeting for the Quarter ended 31Mar25
- 2025-04-30 FLYNG: Board Meeting Other Than Financial Results
- 2025-05-02 SSGC: Board Meeting
- 2025-05-13 HCAR: Board Meeting
- 2025-05-14 BNL: Board Meeting Other Than Financial Results
- 2025-05-16 FEROZ: Holding of Emergent Board of Directors Meeting

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
