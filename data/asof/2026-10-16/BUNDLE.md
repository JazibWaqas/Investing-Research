# Replay bundle, close of 2026-10-16 (brief v2)

=== FILE: BRIEF ===
You are at the close of T. You get only `data/asof/<T>/` (market.md, sectors.csv, screens.csv, announcements_30d.csv, flows.csv, calendar.md; prices as traded at T) and `data/asof/<T>/method/`.

Forbidden:
- web access;
- any other repo file, or any earlier replay output;
- reasoning from anything after T.

If you remember what happened after T from your training, that memory is contamination. Do not use it, and report it in `contamination_note`. Every fact you state cites the pack. Every mechanism you rely on cites a method file. An uncited claim is a violation.

Risk budget [P]: for each entry, size_pct × (entry − stop) / entry ≤ 5 (percent of book); the sum over entries ≤ 10. Concentration up to all-in is allowed within that.

## The investor's posture

- Capital compounds. Nothing is withdrawn; dividends and profits are reinvested.
- The aim is capital gains, not yield. Yield names are the wrong core.
- Growth businesses are the resting place for capital: a business that grows, run by a builder with a sponsor who has done it before, judged on the business first and the numbers second.
- He accepts drawdowns of 40 to 60% in holdings; a falling price alone is not a reason to leave a business that is intact.
- He cuts a loser when a live opportunity needs the capital. Capital is never stuck.
- Concentration is allowed; the limits are on how much can be lost, not on how many names are held.
- Sitting out is allowed, but it must be argued against the default of holding the core (about 75% exposure). Say why this exposure rather than the default.
- "No measured edge" for a situation type does not mean hold cash. It means that type gives no timing signal; the core rests on business questions, not on timing base rates.

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
 "exposure_pct": 0, "exposure_reason": "", "core_default_considered": true, "not_known": "<=60 words", "contamination_note": ""}
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
- **exposure_reason** (required string) is why this exposure rather than the core default of about 75%.
- **core_default_considered** (required boolean) is true only if you weighed holding the core default against this exposure.

=== FILE: market.md ===
# Market as of 2026-10-16 close (public information only)

- KSE100: 166,420 on 2026-10-16; 1m -1.6%, 3m -5.3%, 6m +3.6%, 12m +5.0%
- KMI All Share: 65,474 on 2026-10-16; 1m -1.3%, 3m -4.2%, 6m +4.3%, 12m +2.9%
- Policy rate 11.5%; last MPC decision 2026-09-14: hold (+0bp)
- 6M T-bill cutoff 12.40% (auction 2026-10-14); 3M 12.00%, 12M 12.50%
- CPI YoY 10.3% for 2026-09 (published by 2026-10-03); three months earlier (2026-06) 11.08%
- Brent: 126.55 USD/bbl on 2026-10-14; 3-month change +51.2%
- USD/PKR: 277.42  on 2026-09-30; 3-month change -0.4%
- SBP reserves 21,470 USD mn, total 26,863 USD mn, week to 2026-10-09; 3-month change SBP +16.2%, total +12.0%
- Current account 2026-08: -73 USD mn (published 2026-09-20); trailing 12 months -21 USD mn
- Import cover (SBP only) 3.13 months at 2026-08 (reserves as of 2026-08-28; usable from 2026-09-20)
- KSE100 trailing P/E 8.09 at 2026-09 month-end; earnings yield minus 6M T-bill -0.09pp
- Regime: 6M T-bill minus policy rate +0.90pp (market pricing hikes); CPI falling over 3 months (-0.8pp)
- Next MPC: see SBP calendar

Session date used: 2026-10-16. Liquid KMI names: 125 (membership KMI_ALL_2026-06-05.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.1679,0.6526,1.0356,3,3
E&P,3,-0.0221,-0.0157,0.0308,0,0
OMC,4,-0.0212,-0.0401,0.2505,0,0
Power,6,-0.0555,-0.016,0.0849,0,0
Fertilizer,4,-0.0017,-0.0381,0.0132,0,0
Cement,16,-0.0203,-0.0733,0.0412,0,0
Steel & engineering,11,0.0114,-0.0537,0.1029,0,0
Autos,12,-0.0169,-0.1224,0.1314,0,0
Tech & telecom,13,-0.0207,-0.1175,-0.0611,0,0
Islamic banks & fin.,10,0.0046,0.0328,0.2371,0,0
Pharma,14,0.018,-0.0938,-0.0421,0,0
Textiles,23,0.0401,0.0301,0.4488,1,2
Food & staples,16,-0.0032,-0.0557,0.0384,0,0
Chemicals,19,-0.035,-0.0218,0.1482,1,2
"Glass, packaging, paper",14,-0.0096,-0.0528,0.2084,0,0
Gas utilities & misc,13,-0.0225,-0.1053,0.0596,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AGP,168.38,0.116,-0.13,-0.058,-0.08,-0.276,0.542,0,2026-06-30,-0.023,0,0,0,0,15.229,0.039
AIRLINK,118.54,-0.041,-0.15,-0.118,-0.203,-0.382,0.437,0,2026-06-30,0.361,2,0,0,0,12.707,0.046
ASL,15.09,-0.118,0.194,0.379,0.184,-0.154,0.724,0,2026-06-30,43.0,1,0,0,0,,
ASTM,64.57,-0.504,1.665,3.528,1.806,-0.6,2.088,0,2026-06-30,,2,0,0,0,11.813,
ATRL,1219.1,0.123,0.372,0.492,0.84,0.0,0.64,0,2026-06-30,2.019,1,1,0,0,8.095,0.015
BBFL,35.94,-0.098,-0.164,-0.058,-0.274,-0.335,0.77,0,,,2,0,0,0,,
BECO,4.29,-0.032,-0.175,-0.077,-0.93,-0.94,0.668,0,2026-06-30,,2,0,0,0,20.344,
BERG,112.68,-0.03,0.163,0.319,0.108,-0.324,0.322,0,2026-06-30,0.076,2,0,0,0,9.087,0.045
BFBIO,128.65,0.041,-0.023,-0.098,-0.134,-0.253,0.932,0,2026-06-30,0.312,2,0,0,0,33.326,
BIFO,106.09,-0.056,-0.1,0.248,-0.242,-0.34,0.13,0,2026-06-30,-0.438,2,0,0,0,,
BLUEX,5.94,-0.012,-0.2,0.007,,-0.352,0.32,0,2025-12-31,-0.143,1,0,0,0,,
BNL,5.14,-0.082,-0.227,-0.355,-0.957,-0.963,0.206,0,2025-06-30,,2,0,0,0,,
BUXL,336.47,-0.414,0.772,1.102,1.23,-0.706,2.421,0,2026-06-30,,2,0,0,0,,
CEPB,25.52,-0.042,-0.11,-0.129,0.028,-0.433,0.403,0,2026-06-30,,1,0,0,0,,
CHCC,271.23,0.017,-0.11,-0.017,-0.156,-0.243,0.982,0,2026-06-30,-0.06,1,0,0,0,6.497,0.019
CLOV,5.79,0.045,-0.117,0.052,0.63,-0.287,0.347,0,2026-06-30,2.0,2,0,0,0,,
CNERGY,12.85,-0.002,0.31,0.782,0.641,-0.169,0.709,0,2024-06-30,,2,2,0,0,,
CPHL,61.66,-0.166,-0.176,-0.202,-0.278,-0.332,0.47,0,2026-06-30,-1.441,2,0,0,0,21.506,0.042
CSAP,89.35,-0.01,-0.15,-0.073,-0.025,-0.344,0.23,0,2026-06-30,,1,0,0,0,,0.065
DCL,9.08,-0.044,-0.162,0.125,-0.349,-0.368,0.49,0,,,2,0,0,0,,
DCR,39.81,0.002,0.054,0.144,0.355,-0.036,0.663,0,2026-06-30,,1,0,0,0,7.515,0.083
DFSM,14.61,0.252,-0.15,1.368,1.515,-0.556,0.424,0,,,2,0,0,0,,
DGKC,182.0,-0.062,-0.124,0.029,-0.236,-0.271,0.435,0,2026-06-30,-0.084,1,1,0,0,7.851,0.012
EFERT,194.82,0.042,0.023,-0.031,-0.074,-0.206,0.496,0,2026-06-30,-0.316,0,1,0,0,13.357,0.066
ENGROH,260.65,-0.003,-0.055,-0.034,0.12,-0.125,0.398,0,2026-06-30,-0.698,0,0,0,0,5.136,
FABL,91.49,-0.016,-0.061,0.05,0.169,-0.108,0.298,0,2026-06-30,0.003,0,0,0,0,6.266,0.07
FATIMA,138.57,-0.057,-0.121,0.011,0.057,-0.248,0.636,0,2026-06-30,1.007,0,1,0,0,7.57,0.04
FCCL,51.77,-0.025,-0.006,0.112,-0.031,-0.112,0.427,0,2026-06-30,0.39,0,1,0,0,8.222,0.028
FCEPL,133.39,-0.042,0.304,0.753,0.686,-0.147,0.252,0,2024-09-30,2.03,0,0,0,0,24.633,0.04
FCL,24.71,-0.029,0.093,0.242,0.126,-0.09,0.495,0,2026-06-30,5.333,2,1,0,0,12.305,0.021
FECTC,91.86,0.022,-0.087,0.089,-0.049,-0.496,0.232,0,2026-06-30,-0.61,1,0,0,0,,
FFC,537.87,0.013,-0.0,0.091,0.225,-0.154,0.376,0,2026-06-30,0.116,0,0,0,0,10.107,0.063
FFL,14.03,-0.035,-0.159,-0.094,-0.3,-0.394,0.337,0,2026-06-30,-0.375,0,0,0,0,45.156,
FPJM,20.05,-0.108,0.816,2.916,2.133,-0.391,2.324,0,2026-06-30,,1,0,0,0,,
GAL,484.93,-0.092,-0.133,0.374,-0.087,-0.244,0.535,0,2026-06-30,-0.146,3,1,0,0,5.252,0.026
GATM,19.98,-0.072,-0.26,-0.122,-0.415,-0.46,0.419,0,2026-03-31,-1.131,2,0,0,0,4.564,
GCIL,32.74,0.053,-0.1,0.182,0.105,-0.171,0.961,0,,,3,1,0,0,,
GCWL,13.31,-0.05,-0.18,-0.2,-0.256,-0.455,0.595,1,,,2,0,0,0,,
GDL,18.53,0.036,-0.002,-0.013,,-0.376,0.852,0,2026-06-30,3.737,2,0,0,0,,
GGL,19.7,0.041,-0.164,0.143,-0.217,-0.298,0.473,0,2026-03-31,0.247,3,1,0,0,2.013,
GHGL,39.22,-0.025,0.011,0.126,0.054,-0.103,0.258,0,2026-06-30,0.682,1,0,0,0,,
GHNI,1029.07,-0.056,-0.08,0.475,0.214,-0.224,0.38,0,2026-06-30,0.006,2,0,0,0,6.046,0.015
GLAXO,312.45,-0.007,-0.108,-0.071,-0.201,-0.27,0.338,0,2026-06-30,-0.048,0,0,0,0,12.382,0.044
GTYR,26.49,0.072,-0.22,-0.038,-0.303,-0.396,0.639,1,2026-06-30,,1,0,0,0,,
GWLC,45.72,-0.082,-0.08,-0.046,-0.324,-0.385,0.158,0,2026-03-31,0.128,1,0,0,0,,
HCAR,201.8,-0.091,-0.156,0.235,-0.289,-0.313,0.176,0,2026-06-30,2.002,0,1,0,0,6.693,0.059
HUBC,193.43,-0.02,-0.09,-0.017,0.035,-0.158,0.443,0,2026-06-30,,1,1,0,0,3.875,0.109
ILP,94.03,-0.008,-0.041,0.21,0.448,-0.116,0.325,0,2026-06-30,0.562,1,0,0,0,17.114,0.015
IMAGE,23.91,-0.048,-0.101,0.041,-0.021,-0.146,0.317,0,2026-06-30,,2,0,0,0,,
IPAK,31.72,-0.061,-0.056,0.183,0.427,-0.208,0.937,0,2026-06-30,20.6,1,0,0,0,13.394,0.027
ITANZ,28.45,-0.165,-0.265,0.124,,-0.423,0.399,0,2026-06-30,-0.511,1,0,0,0,,
JDMT,113.49,-0.132,-0.196,0.112,0.116,-0.376,1.143,0,2026-06-30,,2,0,0,0,,
JVDC,133.29,-0.005,-0.039,0.178,0.883,-0.132,0.327,0,2026-06-30,,1,0,0,0,14.977,0.078
KEL,6.09,-0.081,-0.171,-0.161,-0.111,-0.354,0.786,0,2024-06-30,-0.871,3,2,0,0,30.127,
KOHC,83.32,-0.076,-0.144,-0.039,-0.165,-0.319,0.456,0,2026-06-30,0.411,2,1,0,0,6.026,
KOHTM,104.16,0.241,-0.231,1.12,0.915,-0.456,0.6,3,2026-03-31,-0.209,2,0,0,0,6.163,0.024
LOADS,11.88,-0.084,-0.128,0.007,-0.297,-0.427,0.143,0,2026-06-30,1.471,2,1,0,0,13.777,
LOTCHEM,25.41,0.033,-0.078,0.114,0.274,-0.152,0.49,0,2026-09-30,5.0,1,1,0,0,39.488,0.171
LUCK,400.56,-0.016,-0.09,-0.011,-0.06,-0.209,0.436,0,2026-06-30,0.291,0,1,0,0,6.763,0.011
MACFL,100.33,0.464,0.492,3.702,2.559,-0.19,0.965,6,2026-06-30,0.333,1,0,0,0,34.336,0.01
MARI,630.73,-0.002,-0.006,0.005,-0.066,-0.135,0.552,0,2026-06-30,0.971,0,0,0,0,11.514,0.035
MEBL,545.82,0.004,0.023,0.172,0.37,-0.077,0.308,0,2026-06-30,0.049,0,0,0,0,8.82,0.063
MEHT,127.6,-0.075,-0.348,-0.462,-0.576,-0.597,0.544,0,2026-03-31,0.188,3,0,0,0,,
MFL,47.33,0.098,0.122,-0.252,0.141,-0.408,2.339,0,2026-06-30,0.281,2,1,0,0,14.487,
MLCF,89.95,-0.036,-0.058,0.036,-0.105,-0.31,0.406,0,2026-06-30,0.173,0,0,0,0,7.675,
MTL,302.9,0.015,0.043,0.2,0.247,-0.035,0.416,0,2026-06-30,0.374,1,0,0,0,17.531,0.107
MUGHAL,65.82,-0.032,-0.199,-0.06,-0.142,-0.404,0.38,0,2026-06-30,-0.317,1,0,0,0,28.337,
MWMP,86.39,0.002,0.382,0.578,-0.339,-0.371,3.212,1,,,2,0,0,0,,
NETSOL,122.66,-0.016,0.013,0.016,-0.126,-0.176,0.828,0,2026-06-30,-0.393,2,1,0,0,8.173,
NML,126.26,-0.022,-0.126,-0.117,-0.122,-0.384,0.446,0,2026-06-30,0.513,2,1,0,0,8.671,0.016
NRL,665.73,0.282,0.679,0.963,0.703,0.0,1.022,0,2026-06-30,,0,1,0,0,,
NRSL,33.1,-0.059,0.028,0.156,0.08,-0.255,0.879,0,2026-06-30,3.868,1,0,0,0,16.932,
OGDC,299.1,-0.036,-0.041,0.049,0.278,-0.126,0.416,0,2026-06-30,2.154,1,0,0,0,5.583,0.068
PAEL,33.77,-0.053,-0.193,-0.095,-0.355,-0.464,0.351,0,2026-06-30,0.022,1,0,0,0,13.768,
PIBTL,13.65,-0.088,-0.173,-0.111,-0.015,-0.396,1.064,0,2026-06-30,,2,0,0,0,,
PICT,45.06,0.11,-0.124,0.441,0.109,-0.227,0.594,1,2026-06-30,,0,0,0,0,,
POWER,21.76,-0.003,0.047,0.174,0.311,-0.085,0.4,0,2026-06-30,6.538,1,0,0,0,31.257,
PPL,218.87,-0.029,-0.004,0.029,0.267,-0.208,0.579,0,2026-06-30,1.039,1,0,0,0,5.148,0.044
PREMA,32.21,0.003,0.022,0.234,-0.213,-0.245,0.682,0,2026-06-30,1.214,2,0,0,0,16.658,
PRL,106.95,0.287,1.398,2.145,1.988,0.0,1.381,0,2026-06-30,,0,3,0,0,,
PSO,368.04,0.076,0.059,0.051,-0.188,-0.269,0.727,0,2026-06-30,-4.368,2,1,0,0,10.778,0.026
QTECH,35.65,-0.036,-0.283,0.032,0.202,-0.352,1.034,0,2026-06-30,,3,2,0,0,,
SAZEW,1530.41,-0.127,-0.228,-0.172,-0.144,-0.37,0.792,0,2026-06-30,,0,2,0,0,4.217,0.046
SEARL,77.74,0.004,-0.14,-0.122,-0.21,-0.417,0.766,0,2026-06-30,,2,0,0,0,,
SGPL,23.58,-0.296,-0.404,1.068,3.921,-0.517,1.547,0,2026-06-30,,2,0,0,0,,
SLGL,14.88,0.074,-0.088,-0.022,-0.259,-0.358,0.768,1,2026-06-30,-0.259,0,0,0,0,11.307,
SNGP,90.23,-0.009,-0.161,-0.089,-0.236,-0.312,0.336,0,2026-03-31,0.226,1,0,0,0,5.073,0.026
SPEL,39.8,-0.027,-0.175,-0.025,-0.344,-0.428,0.119,0,2026-06-30,-0.21,1,0,0,0,,
SPSL,15.68,0.043,-0.128,,,,0.646,0,2026-06-30,0.206,2,0,0,0,,
SSGC,22.91,-0.03,-0.208,-0.089,-0.398,-0.46,0.319,0,2026-03-31,-0.48,0,0,0,0,10.954,0.012
STL,22.65,-0.004,-0.452,-0.649,-0.989,-0.988,2.056,0,2026-06-30,,4,0,0,0,9.853,
SYM,12.1,0.05,0.171,0.246,-0.04,-0.134,0.209,0,2026-06-30,1.222,3,0,0,0,,
SYS,118.37,-0.029,-0.137,-0.194,-0.2,-0.3,0.746,0,2026-06-30,0.094,0,0,0,0,22.795,0.012
TATM,149.5,-0.01,0.161,0.274,0.052,-0.319,0.466,1,2026-06-30,4.265,1,0,0,0,6.525,
TGL,159.72,-0.022,-0.159,-0.039,-0.265,-0.329,0.748,0,2026-06-30,-0.159,2,0,0,0,9.051,0.016
THCCL,66.14,-0.125,-0.022,0.179,-0.299,-0.335,0.342,0,2026-03-31,0.554,0,0,0,0,6.723,0.005
TOMCL,29.4,-0.078,-0.225,-0.139,-0.524,-0.549,0.517,1,2026-06-30,,2,0,0,0,13.655,
TOWL,124.23,-0.052,0.007,0.165,-0.239,-0.407,0.583,0,2026-06-30,0.913,2,1,0,0,10.955,
TPLRF1,8.79,-0.054,-0.129,0.116,-0.375,-0.378,0.324,0,,,0,2,0,0,,
TREET,23.38,0.097,0.025,0.012,-0.172,-0.354,1.553,1,2026-06-30,1.6,2,0,0,0,17.461,
TRSM,14.14,0.048,-0.087,-0.008,-0.764,-0.793,0.297,0,2026-06-30,5.333,2,0,0,0,,
UNITY,7.93,-0.031,-0.216,-0.031,-0.697,-0.696,0.41,1,2025-09-30,,0,0,0,0,18.228,
WASL,6.56,0.127,0.095,0.393,-0.254,-0.253,0.671,0,2026-06-30,0.3,2,0,0,0,,
WAVES,8.91,0.003,-0.159,-0.08,-0.162,-0.458,0.538,0,2026-06-30,0.619,1,0,0,0,8.618,
ZAL,37.93,-0.004,-0.056,-0.12,0.014,-0.475,0.682,0,2026-06-30,-0.084,2,0,0,0,6.31,0.062

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2026-10-07,LUCK,material_info,Material Information
2026-10-07,HUBC,material_info,Disclosure of Material Information
2026-10-07,KOHC,material_info,Material Information
2026-10-07,CNERGY,material_info,Disclosure of Material Information
2026-10-07,GGL,material_info,Disclosure of Material Information - GHANI GLOBAL HOLDINGS LIMITED
2026-10-07,TOMCL,financial_result,Transmission of Annual Report for the Year Ended 30-06-2026
2026-10-07,MEHT,financial_result,Financial Results for the year ended 30.6.2026 REVOKED
2026-10-08,KEL,material_info,Disclosure of Material Information
2026-10-08,QTECH,material_info,Material Information
2026-10-08,MEHT,financial_result,Transmission of Annual Report for the year Ended 30.06.2026
2026-10-08,ZAL,financial_result,"Transmission of Annual Report for the Year Ended June 30, 2026"
2026-10-08,BECO,financial_result,"Transmission of Annual Report for the FY ended June 30, 2026"
2026-10-08,SPSL,financial_result,"Transmission of Annual report for the year ended June 30, 2026"
2026-10-08,MWMP,financial_result,"Transmission of Annual Report for the Year Ended June 30, 2026"
2026-10-08,SGPL,financial_result,"Transmission of Annual Report for the Year Ended June 30, 2026."
2026-10-08,GCIL,financial_result,"Transmission of Annual Report for the Year Ended June 30, 2026"
2026-10-08,DCR,financial_result,"FINANCIAL RESULTS OF DOLMEN CITY REIT FOR THE YEAR ENDED JUNE 30, 2026"
2026-10-08,SAZEW,dividend_or_bonus,"Credit of final cash dividend for the year ended June 30, 2026"
2026-10-08,DCR,dividend_or_bonus,DECLARATION OF INTERIM DIVIDEND OF DOLMEN CITY REIT FOR THE YEAR ENDING JUN
2026-10-09,TPLRF1,material_info,Material Information
2026-10-09,PSO,material_info,Material Information
2026-10-09,SNGP,financial_result,APPLICATION FOR EXTENSION IN THE PERIOD FOR SUBMISSION OF 1ST QUARTER ACCOU
2026-10-09,BLUEX,financial_result,Application for Extension in the period for submission of 1st Quarter Accou
2026-10-09,LUCK,dividend_or_bonus,Credit of final cash dividend
2026-10-12,PRL,material_info,Material Information
2026-10-12,TPLRF1,material_info,Material Information
2026-10-12,SYM,financial_result,Transmission of Annual Report for the Year Ended 30 June 2026
2026-10-12,SNGP,dividend_or_bonus,Deposit of Unclaimed Dividend into the Federal Consolidated Fund
2026-10-13,MTL,insider_trade,Insider trade disclosure
2026-10-14,QTECH,material_info,Material Information
2026-10-14,CHCC,dividend_or_bonus,Credit of Final Cash Dividend
2026-10-14,CLOV,dividend_or_bonus,CREDIT OF BONUS SHARES IN CDS AND DISPATCH OF PHYSICAL SHARES
2026-10-14,SGPL,insider_trade,Insider trade disclosure
2026-10-15,PRL,material_info,Material Information
2026-10-15,MFL,material_info,Material Information
2026-10-15,LOTCHEM,financial_result,Financial Results for the quarter and nine months period ended 30 September
2026-10-15,MTL,insider_trade,Insider trade disclosure
2026-10-16,STL,financial_result,"Transmission of Annual Report for the Year Ended June 30, 2026"
2026-10-16,SPEL,dividend_or_bonus,Credit of Final Cash Dividend
2026-10-16,KEL,insider_trade,Insider trade disclosure

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,62.103,2026-10-15
investor_type,last_5_sessions,broker proprietary trading,-0.331,2026-10-15
investor_type,last_5_sessions,companies,6.851,2026-10-15
investor_type,last_5_sessions,foreign corporates,-5.338,2026-10-15
investor_type,last_5_sessions,foreign individual,-0.035,2026-10-15
investor_type,last_5_sessions,individuals,7.083,2026-10-15
investor_type,last_5_sessions,insurance companies,-33.243,2026-10-15
investor_type,last_5_sessions,mutual funds,-40.033,2026-10-15
investor_type,last_5_sessions,nbfc,0.092,2026-10-15
investor_type,last_5_sessions,other organization,2.606,2026-10-15
investor_type,last_5_sessions,overseas pakistani,0.245,2026-10-15
sector,last_5_sessions,fipi | Commercial Banks,-2.514,2026-10-15
sector,last_5_sessions,lipi banks / dfi | All other Sectors,3.11,2026-10-15
sector,last_5_sessions,lipi banks / dfi | Debt Market,53.755,2026-10-15
sector,last_5_sessions,lipi companies | All other Sectors,2.825,2026-10-15
sector,last_5_sessions,lipi companies | Cement,3.871,2026-10-15
sector,last_5_sessions,lipi individuals | Commercial Banks,3.249,2026-10-15
sector,last_5_sessions,lipi insurance companies | Debt Market,-31.817,2026-10-15
sector,last_5_sessions,lipi mutual funds | All other Sectors,-3.995,2026-10-15
sector,last_5_sessions,lipi mutual funds | Cement,-4.951,2026-10-15
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-2.527,2026-10-15
sector,last_5_sessions,lipi mutual funds | Debt Market,-23.942,2026-10-15
sector,last_5_sessions,lipi other organization | Debt Market,2.876,2026-10-15
investor_type,last_20_sessions,banks / dfi,-60.437,2026-10-15
investor_type,last_20_sessions,broker proprietary trading,-4.205,2026-10-15
investor_type,last_20_sessions,companies,20.845,2026-10-15
investor_type,last_20_sessions,foreign corporates,-13.696,2026-10-15
investor_type,last_20_sessions,foreign individual,-0.051,2026-10-15
investor_type,last_20_sessions,individuals,20.358,2026-10-15
investor_type,last_20_sessions,insurance companies,-27.407,2026-10-15
investor_type,last_20_sessions,mutual funds,34.228,2026-10-15
investor_type,last_20_sessions,nbfc,0.831,2026-10-15
investor_type,last_20_sessions,other organization,25.32,2026-10-15
investor_type,last_20_sessions,overseas pakistani,4.216,2026-10-15
sector,last_20_sessions,fipi | Commercial Banks,-8.842,2026-10-15
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,6.062,2026-10-15
sector,last_20_sessions,lipi banks / dfi | Debt Market,-72.525,2026-10-15
sector,last_20_sessions,lipi companies | All other Sectors,8.918,2026-10-15
sector,last_20_sessions,lipi companies | Cement,8.806,2026-10-15
sector,last_20_sessions,lipi individuals | Commercial Banks,5.751,2026-10-15
sector,last_20_sessions,lipi insurance companies | Debt Market,-22.752,2026-10-15
sector,last_20_sessions,lipi mutual funds | All other Sectors,-7.21,2026-10-15
sector,last_20_sessions,lipi mutual funds | Cement,-12.973,2026-10-15
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-7.035,2026-10-15
sector,last_20_sessions,lipi mutual funds | Debt Market,73.459,2026-10-15
sector,last_20_sessions,lipi other organization | Debt Market,22.139,2026-10-15

=== FILE: calendar.md ===
# Calendar as of 2026-10-16

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2026-09-17 BIFO: Meeting of the Board of Directors
- 2026-09-17 TRSM: Board of Directors Meeting for the year ended June 30, 2026.
- 2026-09-17 BBFL: Board Meeting
- 2026-09-18 PSO: Board Meeting
- 2026-09-18 SEARL: Board Meeting
- 2026-09-18 GATM: BOARD MEETING AND CLOSED PERIOD
- 2026-09-18 GCIL: Meeting of the Board of Directors - GHANI CHEMICAL INDUSTRIES LIMITED
- 2026-09-18 GCWL: Meeting of the Board of Directors - GHANI CHEMWORLD LIMITED
- 2026-09-21 DCL: Board Meeting
- 2026-09-21 DFSM: Board Meeting
- 2026-09-21 BFBIO: Board Meeting
- 2026-09-21 NETSOL: Board Meeting
- 2026-09-21 JDMT: Board Meeting Rescheduled
- 2026-09-22 PREMA: Board Meeting
- 2026-09-22 GGL: Meeting of the Board of Directors - GHANI GLOBAL HOLDINGS LIMITED
- 2026-09-22 GDL: Board Meeting
- 2026-09-23 SYM: Board Meeting
- 2026-09-23 SGPL: Board Meeting
- 2026-09-23 KOHTM: Board Meeting
- 2026-09-23 NML: Board Meeting
- 2026-09-23 TREET: Notice of Board Meeting of Treet Corporation Limited FY 25-26
- 2026-09-23 TOMCL: Board Meeting
- 2026-09-23 ZAL: Board Meeting
- 2026-09-24 CLOV: Board of Directors Meeting and Closed Period
- 2026-09-25 KEL: Board Meeting Other Than Financial Results REVOKED
- 2026-09-28 CPHL: Board Meeting
- 2026-09-28 WASL: Board Meeting
- 2026-09-28 QTECH: Board Meeting
- 2026-09-28 BNL: Board Meeting
- 2026-09-29 IMAGE: Board Meeting
- 2026-09-29 ASTM: Board Meeting
- 2026-09-29 MEHT: Board Meeting
- 2026-09-30 BECO: Board Meeting
- 2026-10-01 KEL: Board Meeting Other Than Financial Results
- 2026-10-01 MWMP: Board Meeting
- 2026-10-02 MARI: Notice of Emergent Board Meeting
- 2026-10-02 EFERT: BOARD MEETING FOR THE ANNOUNCEMENT OF THE FINANCIAL RESULTS FOR THE NINE MONTHS ENDED SEPTEMBER 30, 2026
- 2026-10-05 GCWL: EMERGENT (SHORT NOTICE) BOARD OF DIRECTORS MEETING OTHER THAN FINANCIAL RESULTS
- 2026-10-06 EPQL: Board Meeting for the announcement of the financial results for the nine months ended September 30, 2026
- 2026-10-07 EPCL: Board Meeting - Engro Polymer & Chemicals Limited
- 2026-10-08 ATRL: BOARD MEETING AND CLOSED PERIOD
- 2026-10-08 ACPL: Board Meeting
- 2026-10-08 LOTCHEM: Board Meeting / Closed Period
- 2026-10-09 NRL: Board Meeting
- 2026-10-12 MEBL: NOTICE OF BOARD MEETING AND CLOSED PERIOD - MEEZAN BANK LIMITED
- 2026-10-12 FABL: Board of Directors Meeting of Faysal Bank Limited
- 2026-10-12 PRL: Board Meeting
- 2026-10-12 KSBP: Board Meeting
- 2026-10-13 NRSL: Board Meeting and Closed Period
- 2026-10-13 ISL: Board Meeting
- 2026-10-14 POWER: Board Meeting
- 2026-10-14 ILP: Notice of Board Meeting for the First Quarter ended September 30, 2026 / Closed Period
- 2026-10-14 SEARL: Board Meeting
- 2026-10-15 FCEPL: Board Meeting 3rd Quarter 2026
- 2026-10-15 CHCC: Board Meeting
- 2026-10-15 BIFO: Meeting of the Board of Directors
- 2026-10-15 SPEL: Board Meeting
- 2026-10-15 INIL: Board Meeting
- 2026-10-15 MTL: Board Meeting
- 2026-10-15 ITANZ: Board Meeting
- 2026-10-16 GATM: BOARD MEETING AND CLOSED PERIOD
- 2026-10-16 SGF: Board Meeting
- 2026-10-16 SRVI: Board Meeting
- 2026-10-16 TOWL: BOARD MEETING
- 2026-10-16 PRL: Board Meeting Rescheduled
- 2026-10-16 PIOC: Notice of Board Meeting
- 2026-10-16 LCI: Board Meeting / Closed Period
- 2026-10-16 JDMT: Board Meeting
- 2026-10-16 BIPL: Board Meeting - BankIslami Pakistan Limited

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
**The decision chain.** The Cabinet Committee on Energy (chaired by the PM) approved the revamped refinery policy on 28 Jul 2026 (Dawn 2019159) and received the gas-debt plan on 19 Aug 2026 (ProPakistani). The ECC approves prices and margins. The Petroleum Division signs and monitors; OGRA notifies gas, fuel and FRR numbers; NEPRA sets tariffs. Approval is not implementation. The OMC margin rise of Rs1.22 a litre is ECC-approved but still un-notified (OCAC letter, Business Recorder 25 Aug 2026; 
**Finance ministry and IMF.** The ministry wants the primary surplus, clean reviews and market access (a Eurobond was issued before Apr 2026 per the MPS). The IMF enforces numbers and cost recovery: the captive-gas levy was a structural benchmark and the IMF refused to revise it (Profit, 28 Mar 2025); fertilizer subsidies were refused in 2023 (Tribune). It lets slide dates and stocks. DISCO sales promised for Jan 2025 (Profit, 12 Oct 2024) had reached only expressions of interest by May 2026. FB
**SBP reaction function** (computed here from the 84 decisions of Jan 2015 to Sep 2026: 45 holds, 21 hikes, 18 cuts; real rate = policy rate before the meeting minus prior-month CPI). Hikes came at a median real rate of -1.1% (range -17.0 to +3.9). Waves: 2018-19, 750bp to 13.25%, with MPS reasons the rupee, current account and reserves, running into the IMF programme (Jul 2019 MPS cites depreciation); Sep 2021 to Jul 2022, 7% to 15%; Nov 2022 to Jun 2023, 15% to 22%, real -8 to -17 as SBP chase
**Establishment and SIFC.** The SIFC (created mid-2023, army chief a member, agriculture, mining and IT focus, IMF asked about its powers) was described by a government adviser to mining.com (date not shown). Reuters in 2020 reported the military as the most influential voice on Reko Diq. Establishment-linked capital is visible in listed names: Fauji Foundation owns 44.32% of FFC (FFC H1-26 report), FFC holds 33.99% of the PIA buyer (repo), a Fauji Foundation and KAPCO group bought Attock Cement
**Courts and regulators.** Of the 26 policy cases in section 2, three were materially held up by courts: GIDC (2020), the captive levy (IHC suspended it 28 Mar 2025 and recalled the stay 11 Apr; SHC ruled retroactive bills unlawful in Jan 2026), and NEPRA’s cut to K-Electric (Appellate Tribunal 23 Sep, notified 27 Sep, SHC stay 7 Oct 2026). Interim stays arrive within days and rarely kill a fiscal levy; they cut retrospective claims. In deals: SECP and the SHC unwound the TRG offer; SECP suspend

=== FILE: situations.md ===
2020-01-13 (outcome_end) | 01_2019_bottom_imf_programme.md | Regime bottom: the IMF approval was not the low. The second signal (Sep 2019 rate hold, stable rupee) returned +35% to the January 2020 peak. Lesson: wait for it, not the headline.
2021-06-14 (outcome_end) | 02_2020_covid_crash_rate_cut_rebound.md | Shock with a policy backstop: the first rate cut came before the March 2020 low, the rebound was +79% from the low by June 2021. Lesson: enter a third, add on confirmation, favour USD earners.
2023-06-23 (outcome_end) | 03_2021_22_hike_cycle_and_default_scare.md | Tightening plus external stress: rate up 800bp in ten months with CPI above it. To June 2023 the median liquid stock fell 52% and 4 of 95 names rose. Lesson: hold bills, and set a trigger to return.
2024-12-16 (outcome_end) | 04_2023_imf_standby_and_the_rally.md | Regime bottom on an IMF trigger: the staff-level deal came before any rate cut. KSE rose 190% from the June 2023 low to December 2024. Lesson: enter in stages on the trigger, not on a cut.
2024-12-16 (outcome_end) | 05_2024_first_cut_and_the_sector_leaders.md | First-cut policy decision in an easing cycle: KSE +59% by December 2024; fertilizer, E&P and pharma led while banks lagged. Lesson: favour sectors with their own catalyst over rate-sensitive ones.
2025-07-01 (outcome_end) | 06_2025_may_india_conflict_crash_and_rebound.md | Geopolitical shock, intact IMF and rates: KSE fell 12.6%, rebounded 13% in two sessions and was 8% above its pre-shock level by July. Lesson: hold the core; keep cash ready for a weekend gap.
2026-09-09 (outcome_end) | 08_2026_asl_sponsor_buying.md | Sponsor accumulation: the controlling sponsor bought three times at rising prices, each disclosed within two days; ASL rose 62% to its September 2026 peak. Lesson: real but untested; the price moved a day before disclosure.
2024-12-30 (outcome_end) | 09_2024_ssgc_volume_run.md | Volume ignition with upper locks on a regulated utility with late accounts: SSGC rose from 9.95 to 49.52 by the December 2024 peak with no filing explaining it. Lesson: instinct paid, but the repo cannot yet say when.
2019-08-16 (outcome_end) | 12_2017_19_bear_and_the_2018_election.md | Balance-of-payments squeeze and hike cycle: the index fell 46% to the August 2019 low and 3 of 75 liquid names rose. Lesson: read the rate and the rupee, not the politics.

=== FILE: quality_scores.csv ===
business-quality scores from public records, judged by a model on 2026-10-18; not point in time
symbol,promises_vs_delivery,capital_allocation,minority_treatment,disclosure_quality,overall,growth_engine,key_people,red_flags
MEBL,4,4,4,4,16,"Deposits growing 20 to 25% a year on 100+ new branches a year (1,105 to 1,250 target by end-2026) with 91% CASA; at 33% ROE and 55% payout retention alone roughly doubles equity in 5 years, but earnings stay a policy-rate call (PAT Rs28bn 2021, Rs101bn 2024, Rs89bn 2025).","Founder CEO Irfan Siddiqui (1997 to 29 Dec 2025) built the largest Islamic bank; Dr Syed Amir Ali CEO since 30 Dec 2025 (Meezan from 2006, BankIslami CEO 2018 to 2023, named successor in AR2023), under 1 year so no CEO record; chairman Riyadh Edrees (Noor Financial) on the board since 2012.","Earnings are mostly a rate call: PAT 3.6x from 2021 to 2024 on the policy rate, then -12% in 2025; not management skill | Islamic credit card promised in AR2021 for 2022, still a 2027 rollout (five-year slip) | Apr 2025 'stronger H2' guidance missed: H1 PAT about Rs46.1bn vs H2 about Rs42.9bn | Rs30.0bn (Jan 2023) and Rs33.0bn (Jan 2024, about 18% of 2023 equity) financing to common-director entities, repaid in 2024; counterparty not identified (unverified) | Investments Rs2.6tn (Rs2.2tn government Ijarah sukuk), about 9x equity: sovereign and rate concentration | Annual report outlook is boilerplate with no numeric targets; promises only checkable via briefings and press | Several notices unread (scanned): CEO 30 Dec 2025, material info 9 Feb 2026, director cessation 17 Aug 2026, director change 8 Oct 2026; Q4 2025 EPS dip unexplained | Al Meezan AUM flat (Rs718bn to Rs724bn) in a year the index rose 51%; open HSBC bargain-purchase tax dispute Rs1.8bn | Three holders own about 74% (Noor 35.0%, PKIC 29.8%, IsDB 9.3%); free float 25.9%"
LUCK,4,4,3,4,15,"Doubling EPS in 5 years needs about 15% a year, against recent growth of +44%, +19%, +16%. Drivers are Congo plant 2 (1.31 to 2.91 Mtpa, due 2Q FY28), a full year of the Iraq clinker line and grinding mill, renewables cutting energy cost, Thar coal at LEPCL, and rate cuts. My unsourced estimate is 1.6x to 1.9x in 5 years. It breaks on a Gulf conflict hitting Iraq or coal prices, super tax and FED, an overpriced DISCO bid, solar eroding grid demand, and CPPA arrears.","Chairman Muhammad Sohail Tabba (since 30 Jan 2023, reappointed 14 Oct 2024). CEO Muhammad Ali Tabba (reappointed 2021 and 14 Oct 2024; off the board since 25 Apr 2025, still CEO). Family-controlled, with Hassan Tabba (next generation) added to the board in April 2025. Record: hard capacity and solar projects on time, EPS Rs14 (FY21) to Rs61 (FY26), two buybacks that returned 3x to 4.6x. Weak spot: the Thar-coal timeline, which the coal miner controls.","Thar coal for LEPCL promised Q2 CY2023 (Mar 2022), still in transition at Sep 2026 (three years late, set by the coal miner) | Consolidated payout 8% of EPS (Rs5 on Rs60.78) against ROE of about 23%, while cash funds PIA, DISCO, mining and Congo bids | Rs39.6bn put into associate-managed mutual funds in FY26 (Rs24.7bn redeemed); terms and fees unverified | Cement output at 49.7% of 15.6 Mtpa capacity in FY26 while Congo capacity is being added; Pezu 3.15 Mtpa line came online at a demand trough | LEPCL's CPPA-G receivable is Rs28.3bn, of which Rs17.5bn is overdue and Rs7.1bn is over 90 days | Directors, sponsors and associates hold about 70%, so float is about 30% | Guidance is qualitative only: no EPS, margin or return targets in briefing slides | Unverified: Lucky Motor earnings, Pezu line cost, CFO tenure, 20 Oct 2026 briefing content; no briefing transcripts exist, only slides"
SYS,4,3,3,4,14,"Export IT services sold through Microsoft, Temenos and SAP partnerships, with 91% of revenue in foreign currency. Growth comes from Saudi, UK and APAC expansion, the Confiz and BAT SAA acquisitions, and AI work. Earnings were Rs11.0bn in 2025, so doubling in five years needs about 15% a year. What would break it: rupee appreciation or wage inflation (57% of costs are in PKR), AI cutting billable hours, Confiz or BAT integration failing, and dependence on related-party customers.","Aezaz Hussain founded the company in 1977 and is non-executive Chairman; he also chairs Visionet, a related party. Asif Peer, CEO and MD, has 30+ years in the group and holds 7.06%. USD revenue grew from $94m in 2021 to $286m in 2025 (32% CAGR) under him. Arshad Masood, a non-executive director, holds 13.09%. CFO Roohi Khan joined from PepsiCo; COO is Asif Akram.","Two related-party customers were 48.1% of standalone revenue in 2025 (47.9% in 2024), and the note says this is not a concentration risk because they are related parties (AR25). Visionet Systems Inc alone paid Rs12.8bn. Arm's-length pricing is unverified. | CEO Asif Peer sold 10m shares at Rs172 (Rs1.72bn) on 8 Jan 2026, near the 52-week high of 174.40. The price was Rs118.37 on 16 Oct 2026 (insider_trades.csv, stockanalysis.com). | Start-up bets were written down (Jomo, Jugnu). The EP Systems loan is being converted to preference shares, and the three directors above sit on the EP B.V. side. | Said 'no new markets' in AR22 and AR24, then entered new ones: UK entity, Vietnam, Indonesia, two acquisitions. | Net margin fell from about 33% (H2 2021) to 11% in 2024 and 14% in 2025. Q2 2026 net margin was 11.8% against 14.2% a year earlier. | Filings were revoked repeatedly (H1 2019 report, Oct 2024 deck, four briefing notices and videos in May to Jul 2026). The FY25 briefing came on 3 Jun 2026, versus 10 Apr a year earlier, and there were AGM extensions in 2023 and 2026. | Shares outstanding rose about 4% (1,473m to 1,531m) by Q2 2026, probably from the Confiz share swap. I found no filing that confirms the link, so it is unverified."
FFC,4,3,3,4,14,"Nothing clearly doubles EPS in 5 years. Urea runs at about 112% of capacity and share is already 56-58%, so volume is capped by gas. Realistic 1.3 to 1.6x nominal (my estimate, unverified) from Port Qasim gas, PEF, Thar dividends, Agritech and Askari. PIA and coal-to-urea are options, not drivers.","Chairman Lt Gen Anwar Ali Hyder (since Apr 2024) is also CEO of sponsor Fauji Foundation (44.32%). MD and CEO Jahangir Piracha (since 1 Apr 2024) is an ex-Engro outsider who delivered the FFBL merger integration, KMI-30 entry and a 58% urea share. Predecessor Sarfaraz Ahmed Rehman served Oct 2021 to Mar 2024.","Rs61bn (Rs30.6bn paid plus Rs30.59bn committed) into a 33.99% PIA stake while GIDC of about Rs85bn sits unpaid under a stay | Sales-tax receivable provisions up to Rs39.6bn at end 2025 from Rs25.2bn in 2024, with GST refunds unresolved since at least 2021 | Repeated acquisitions from sponsor Fauji Foundation (wind Rs13.51bn 2021, FFBL merger 2024, FPCL 25% share swap Jan 2026); chairman is also Foundation CEO; fairness of pricing unverified | Food arm (Fauji Foods, FFF) about Rs18bn invested, first profit only in 2025; Fauji Foods impaired Rs2bn | Dividend and investment income about 38% of 2024 profit, part Askari Bank equity income that is not cash | PEF gas compression project about three years behind the 2022 plan; Agritech control goal of 2024 not reached (37.36%) | Insider dealings unverified: zero FFC rows in insider_trades.csv; Q4 2025 sales-tax charge size is a broker estimate only"
ILP,4,3,3,4,14,"Apparel and denim ramp-up (apparel 1.1m to 1.6m garments, 7 more denim lines, Plant 6) plus margin recovery from FY25's 3% toward FY24's 10% could roughly double EPS from Rs9.4 if revenue grows about 8% a year, but US tariffs, a stable rupee, taxes and 57% gearing can break it; no successor to Vision 2025 has been published.","Musadaq Zulqarnain (non-executive chairperson, founder), Navid Fazil (CEO, founder), Muhammad Maqsood (Group CFO, 24 years). The family bloc holds 69.6%. They hit most Vision 2025 targets, but returns on the capex-heavy build-out have fallen, and a CFO change on 27 Jul 2026 is unverified.","FY25 net profit fell 66% (Rs16bn to Rs5.4bn) after the Rs29bn apparel build; apparel is only 17% of FY26 sales | Top Circle (64% bought Nov 2023 for Rs1.73bn) lost Rs703m in FY26 and revenue fell 35% | Gearing 56 to 63% for five years; interest cover 2.0x in FY25 | Directors, CEO and spouses hold 69.57%; group of 23 sponsor-owned outside companies (dairy, logistics, IT) trading with ILP | Gearing definition differs between the 2023 and 2024 briefing decks (39.5% vs about 56% for FY23) | Bonnie Doon brand bought by an 'associate' (Textile Hub B.V.) and announced as ILP material information; ILP's stake unverified | No Vision 2030 or other successor strategy published; 'questions received in advance: Nil' at CBS 2026 | Unusual share-volume clarifications on 27 Sep 2024 and 19 Jun 2026 (scanned, content unverified)"
MARI,4,3,3,4,14,"Volumes can rise (Ghazij to 222 MMscfd for three fertilizer buyers, Shams, Spinwam, Pateji, Soho), but underlying EPS has been flat at about Rs54 for two years because the state takes more per unit. 2x EPS in 5 years is not visible; 1.3 to 1.5x is plausible (my estimate).","CEO Faheem Haider since Aug 2020, a petroleum engineer and not a Fauji officer, now reappointed to Aug 2027. Chairman Lt Gen Anwar Ali Hyder (Retd) is also CEO of the sponsor, Fauji Foundation (40%). Record: reserves and resources 568 to 1,029 MMBOE, capacity +31%, reported EPS 26 to 72.5, but dated project milestones keep slipping.","FY26 profit of Rs87.1bn includes Rs22.8bn of tax reversals (Rs17.2bn super tax after the 27 Jan 2026 court judgment, Rs5.7bn Rule 35 under a stay). Pre-tax profit fell 5.6% and underlying EPS is about 53.5, flat on FY25. | Trade debts of Rs86bn are 45% of sales, with Rs38bn over 90 days and no expected-credit-loss charge on government debt (SECP exemption). | Dated projects are late: Shewa about 15 months, the HRL compression fix still unfinished after three years, the data centre about seven months. | Payout fell from about 60% (FY21) to 37% (FY26) while cash goes to Abu Dhabi (US$100m, no revenue), minerals and data centres, none earning yet. | The sponsor chief chairs the board, state-linked holders own 80%, and the free float is only 20%."
FABL,4,3,3,4,14,"Balance sheet growing about 14% a year (CASA and current-account mix, remittances, CBSME) with book compounding about 9% a year gives roughly 1.5x EPS in 5 years. Doubling needs about 15% a year, so ROE would have to stay near 19% as rates fall. That is not the base case.","CEO Yousaf Hussain: CEO since 2017, at the bank since 2008, led the Islamic conversion, reappointed for 3 years from 15 Aug 2026. Ithmaar Bank holds 66.78% (ultimate parent Dar Al-Maal Al-Islami Trust); chair is Mian Muhammad Younis. CFO changed Dec 2025.","Sponsor wants out: Ithmaar approved a 75% stake sale to GFH in May 2024; talks ended 16 Apr 2025 with the door left open; minority exit terms were never stated | Maple Leaf Cement bought shares on market in 2025 and got CCP approval on 12 Mar 2026 to buy more; stake size unverified | Earnings are rate-driven: 2025 PAT -5.8% and net profit return -13%, with Rs7bn more capital gains and credit reversals propping the result | CASA mix fell in 2023 (80% to 75%) and in 2025 (85.5% to 81.9%); CAR about 14% and a Rs7bn Tier II sukuk issued May 2026 | Half-year result revoked the same day on 6 Aug 2026 over a cash-flow typo (reason taken from the existing card; notice not read) | Forward statements lost their numbers after 2023 ('strategic targets against KPIs'); the 2026 to 2030 plan has no published financial targets | Rs5.5 interim dividend in Nov 2022 took the 2022 payout to about 94%; cause unconfirmed (AGM record mentions Shariah cleansing of retained earnings) | CFO and chair turnover"
THCCL,4,3,4,3,14,"No visible doubling from the existing plant (1,800 TPD, 63% utilisation, perhaps +15% volume). EPS 2x in 5 years needs the unfunded 5,000 TPD line, hotel assets from a Pakistan Services (PC Hotels) settlement, or higher cement prices. FY25 profit leaned on intra-group dividends; FY26 nine-month operating cash flow was Rs0.54bn on Rs2.19bn profit.","CEO Kamran Munir Ansari (director since Oct 2021, CEO since Oct 2023). His record is strong: operational promises delivered (solar, wind, local coal), a Rs277m buyback at about Rs3.7 split-adjusted, and heavy personal buying. His prior career is unverified. Sponsors Sky Pak and Al-Miftah (about 54% with two other holdcos) took over from Arif Habib in 2012; the people behind them are not disclosed. Chair Khawaja Muhammad Salman Younis, a repeat buyer of the stock. CEO and CFO turnover has been high.","Rs6.47bn for 28% of Pakistan Services (PC Hotels): non-core, no board seat, frozen by the Islamabad High Court, and half funded by Rs5.5bn sukuk at 6M KIBOR+2.5% (PSX 13-14 Oct 2025, 4 Dec 2025) | FY26 nine-month operating cash flow Rs0.54bn against net income Rs2.19bn (stockanalysis, quarterly_eps.csv) | Six CFO changes between Jan 2020 and Sep 2026 and five CEO appointment notices since 2016 (PSX announcement titles) | Director Saleem Zamindar bought 1.25m shares at Rs50.18 on 9 Sep 2025, five weeks before the Pakistan Services deal, and sold 1.25m at Rs67.35 on 1 Jul 2026. His knowledge is unverified. The sukuk arranger AKD Securities shares a name with AKD Group, another Pakistan Services block holder; any link is unverified | FY25 unconsolidated profit inflated by Rs2.0bn of other income, mostly Thatta Power dividends (VIS 18 Sep 2025) | Annual report quality is poor: placeholders, a Rs10.030 million PPE valuation, image-only financial statements. FY24 report transmission was revoked. FY26 results are not out and an AGM extension was sought on 30 Sep 2026 | Treasury shares (75m, about Rs5bn) are pledged as sukuk backstop and were not cancelled | The 5,000 TPD expansion MoU of Feb 2025 shows no financing or construction in filings | KMI-All membership was deleted in Jun 2025 and re-added in Jun 2026, a debt-ratio risk after the sukuk | Opaque ultimate owners of the sponsor holdcos"
ISL,3,3,4,4,14,"Volume on an already-built 1.0m t cold-rolling plant (435 kt sold in FY26, about 45% utilisation), helped by anti-dumping enforcement, exports and lower rates. About 650 kt at FY26 unit profit gives EPS near 12.6 (1.5x); 2x needs about 870 kt or better margins (my estimate, unverified). It breaks if duty collection stays stayed or circumvented, if HRC prices swing, or if the Rs914m CCP penalty lands.","Kamal A. Chinoy has chaired since 2007 and also chairs sponsor IIL, which holds 56.33%. Samir M. Chinoy, a sponsor-family member at ISL since 2009 and COO before, has been CEO since Oct 2024, after Yousuf Mirza (CEO 2015 to Oct 2024). EPS went 17.16 (FY21), 12.44, 8.10, 8.40, 3.58, 8.44 (FY26), and the share price is about flat to down over six years.","Operating cash flow about -Rs4bn in FY26 against Rs3.67bn profit; short-term borrowings rose to Rs10.7bn from Rs4.5bn | CCP found price coordination among steel producers; Rs914m penalty (about Rs2.1 per share) under appeal with no provision made (AR2026 note 23.1.2) | Earnings swing with import protection and HRC prices: EPS 17.16 in FY21 and 3.58 in FY25 | Rs38.8bn of FY26 purchases from related parties, mostly Sumitomo (9.08% holder); price fairness unverified | Rs1.5bn bank guarantee and a joint Reko Diq performance guarantee for sponsor-group affiliate CECL; release on exit unverified | Hot-rolled strip mill feasibility (AR2022) dropped without explanation; no volume or earnings targets ever given | Jan 2025 half-year results revoked and reissued 9 days later, reason not stated; AR2025 PDF text layer unusable | SRO 565 HRC concession dispute: Rs5.7bn post-dated cheques, Rs1.65bn bank guarantee"
ENGROH,4,3,3,4,14,"Doubling needs Jazz tower profit to roughly double, fertiliser back to 2024 levels and Thar Phase III to hold. Plausible, not likely; buy-backs add only 3 to 4%.","Chairman Hussain Dawood (Engro chair since 2002) and CEO Abdul Samad Dawood (CEO since Jan 2025, ran the Hubco, Fatima and FrieslandCampina deals). The CEO's letters are candid and he delivered the 2025 restructure, the tower deal and the rice exit on time. The subsidiary benches rotate.","2025 EPS of 46.2 is inflated by a Rs26.6bn thermal write-down reversal; underlying is 24.1 | No dividend for 2025; buy-back instead, with 18 Jun 2026 buying at Rs287 near the high | Authority to lend up to Rs7bn to Dawood Lawrencepur, a 6.47% holder sharing three directors | Debt-funded US$562m tower bet: Rs96.4bn still owed to PMCL at Dec 2025, group liabilities Rs755bn against equity Rs319bn | Thermal sale collapse unexplained: the CEO says the board declined to extend, press says the buyer pulled out | Rice and the PDH project were value-destroying and admitted; EPCL sold at Rs19.7bn with cost basis unverified | Family control (directors and families 15.28%) and cash trapped below the holding company by inter-corporate dividend tax and minority leakage (Rs25.9bn to subsidiary minorities in 2025)"
EFERT,3,3,3,4,13,"Nothing identified that doubles EPS in 5 years: urea volume is capped near 2.3Mt and earnings are urea price minus gas cost. Best case is a recovery to the 2023/24 EPS of Rs20 to 21 from Rs15.9 TTM, if the Rs150/bag premium holds, 519kt inventory clears and the gas cost gap to FFC and Fatima narrows. Specialty, Markaz and UgAi are immaterial. The case breaks if the Mari pressure enhancement facility slips again, if the SNGPL contract for EnVen ends in 2027 without a good renewal (unverified), or if GIDC, NGDS cess or super tax rise.","Engro Corporation owns 56.27%, with Engro Holdings above it. CEO Imran Ahmed has served since 11 May 2026 after Ali Rathore resigned on 2 Mar 2026 with no reason given; before Rathore came Ahsan Zafar Syed (Jul 2022 to Apr 2024, now chairman). That is three CEO changes since April 2022, with the CFO also changing several times. The record is a professional sponsor-group bench with rotation, not a founder with a long tenure.","Three CEO changes since Apr 2022, plus CFO changes in Feb 2023, Aug 2023 and Apr/May 2024 | Gas pressure enhancement facility timeline slipped three times (end-2024, then Q2 2025, Q4 2026, Q3 2026) | Gas cost disadvantage (EnVen Rs1,597 vs Rs580/mmbtu for FFC and Fatima); 2026 share loss and 519kt inventory | Dividends of Rs94bn over 2022 to 2025 against Rs93bn profit and about Rs116bn operating cash flow; 2024 operating cash flow was negative (about -Rs4bn) while the payout was near 100% | Gross government subsidy receivable of Rs6.52bn, unchanged since 2018 | Annual reports for 2021 to 2024 are image scans, and no explicit payout policy was found | Parent royalty and reimbursements of about Rs3bn a year, and a Rs33bn short-term loan from the parent in 2025 | Holding company layers (Engro Holdings, Engro Corp); the NGDS cess of up to Rs700/bag and super tax are policy risks"
SAZEW,4,3,3,3,13,"Haval, Tank and NEV volume on a planned 54,000-unit plant (19,179 sold in FY26); doubling FY26 EPS by FY31 needs roughly 2x units at about a 24% gross margin while hybrid sales tax is higher, so I would not assume it. Three-wheelers and parts are small and flat; exports are tiny.","Mian Asad Hameed, CEO and founder-director since 1991, re-appointed for three years from 28 Mar 2026; wife Saira is chairperson and son Ali Hameed is COO cars. The family holds about 63%. Record: Rs4bn to Rs191.7bn revenue in five years by localising GWM Haval, but a thin record before FY22.","Capex plan went Rs4.5bn, Rs11.5bn, then Rs22bn paint shop plus Rs4bn and Rs1.1bn land, with no stated return target | Stock in trade tripled to Rs42.1bn; FY26 operating cash flow Rs9.6bn on Rs23.6bn profit | Payout only 15 to 19% while cash and land accumulate; CEO Asad Hameed's stake fell from 25.30m to 22.63m shares Jun 2024 to Jun 2026 (buyer and price unverified) | Single franchise dependence (GWM); chair, CEO and a COO are one family | Exports promised in every briefing since 2024; FY26 exports Rs78m of Rs191.7bn | Auditor Saeed Kamran & Co. removed June 2024 for Crowe Hussain Chaudhury, no reason found | Unprovided contingencies: stayed additional customs duty on CKD kits, section 5A case, sales tax demands (unquantified)"
GLAXO,3,3,3,4,13,"Nothing clearly doubles EPS: the 2024-25 jump (gross margin 25% to 37%) came from drug-price deregulation, not volume. Antibiotics were flat in 2025 and underlying H1 2026 sales rose only 4.4%. Realistic 1.3 to 1.6x over five years (my estimate, unverified) from price, dermatology, Shingrix and tenders. The Aug 2026 order to review DRAP pricing, hardship rules and margins could cut this.","CEO Erum Shakir Rahim, a GSK career manager, running GSK Pakistan since Apr 2020 and re-appointed 25 May 2026. EPS went from 10.6 (2020) to 31.5 (2025), but the 2022-23 trough and the 2024 recovery both followed regulation. Sponsor is GSK plc through GSK International Holding and Finance B.V., 82.59%. Chair Dmytro Oliinyk was re-appointed in May 2026 after the previous chair resigned in March 2026. The CFO resigned in June 2026 and a successor was named in September 2026.","Earnings depend on regulation: gross margin went 7% (2023) to 37% (2025), and a pricing review was ordered on 28 Aug 2026 | No dividend for 2022 and 2023 despite Rs8.5bn cash at end-2021 | 82.59% parent; Rs4.5bn of purchases from affiliates and Rs0.7bn royalty, transfer-price fairness unverified | Chair change (Mar and May 2026) and CFO resignation and replacement in mid-2026 | Antibiotics flat in 2025, underlying H1 2026 sales growth 4.4%, inventory days up to 105 from 91 | Operating cash flow was negative (-Rs3.2bn) in 2022 on a profitable year | Many tax appeals pending since 2009 | Insider dealings unverified (no rows in insider_trades.csv, director-interest filings not read)"
HALEON,3,3,3,4,13,"Panadol and CaC-1000 volume plus non-essential pricing, Sensodyne and Centrum, and 8bn-tablet Jamshoro capacity could carry roughly 15% a year EPS growth. Gross margin has already doubled to 39%, so most of the recovery is done. Q2 2026 EPS was only +3%.","CEO Qawi Naseer since 1 Jun 2025, a group-appointed consumer-goods executive with no record yet. Predecessor Farhan Haroon, now Chairperson, ran the margin recovery. CFO Babar Sharif since Sep 2025. Seconded executives rotate every 2 to 3 years. Sponsor is Haleon plc via Haleon Netherlands B.V., holding 85.79%.","85.79% parent and about 14% free float; a shareholder asked about maintaining the PSX listing at the Apr 2026 briefing and the answer is not in the filing (delisting risk unverified) | Export promise failed: exports were Rs1.0bn in 2022 and Rs29m in 2024 and Rs99m in 2025; tolling fell 54% in 2025 | Panadol insourcing plan targeted Q2 2025 completion, slipped; DRAP approval reportedly still pending in Jan 2026 (unverified) | No dividends for 2021 to 2023 despite profits; no buyback | Related-party goods purchases doubled to Rs2.2bn in 2025; OTC marketing authorisations still run through GSK Pakistan against a service fee since 2022 | Management rotation and internal-audit head churn (interim heads in 2025 and again in Aug 2026); chair is now a group nominee | Unprovided tax demands (Rs392m and Rs287m among others), mostly won at first appeal | Q2 2026 EPS growth only +3%; share price fell from 1,010 to 684, cause unverified"
IPAK,3,3,3,4,13,"No clear 2x. FY26 EPS of Rs6.73 already rests on a peak-margin year (Q4 was 48% of annual profit; Q1-Q3 run-rate is about Rs4.7). Levers are utilisation (about 75% to 90%), metallised and specialty mix, exports (25% of sales to 40%), PETPAK moving from breakeven to profit, and lower interest. Estimated 1.3 to 1.6x on the run-rate by FY31 (my estimate, unverified). Breakers are domestic BOPP overcapacity (the company's own slides show demand of about 78kt against saleable capacity of 158 to 196kt), tax holiday expiry, polymer and freight swings, and the Rs22bn of parent guarantees to subsidiaries.","Naveed Godil, founder-CEO since 2015 (13.14% holder), re-appointed for 3 years from 31 Oct 2025. Chairman Muhammed Amin, ex-CEO Gillette Pakistan and Mondelez Pakistan. Two BOPP/BOPET lines commissioned about on schedule in 2024, then two years of heavy finance cost and PETPAK losses, with a strong FY26. Sponsor-directors hold about 43%, float 29%, and 3 of 10 directors are independent.","Q4 FY26 net income Rs2.38bn was 48% of the year on revenue only 7% above Q3; cause unverified (one-offs or a price spike) | Operating cash flow Rs2.2bn against profit of Rs4.95bn; receivables up Rs1.8bn and inventory up Rs2.1bn | Domestic BOPP overcapacity shown in the company's own briefing slides | About Rs3.6bn a year of sales to associated packaging firms (common directors), Rs1.6bn receivable, 17% of trade receivables; ownership of those firms unverified | PETPAK 48% partner did not follow the Rs2.13bn rights (paid Rs141.6m); group took the rest at par; fairness unverified | Rs22bn cross-guarantees from the listed parent to subsidiaries | Prospectus EPS targets missed by over 50% in FY24 and FY25 (secondary source) | Quarterly report [264256] and AGM minutes [267566] each revoked once in late 2025; AR2026 text partly unreadable on extraction | Insider dealings unverified: 13 director-interest filings since 2025 not parsed, zero IPAK rows in insider_trades.csv | Float only 29%"
AIRLINK,3,3,3,3,12,"Local assembly of TVs, ACs and phones in the Sundar Green SEZ (10-year tax holiday), Hisense and Acer partnerships, retail and BNPL. Profit of Rs6.2bn needs about 15% a year to double in five years. It breaks on sales-tax or import-rule changes, Xiaomi dependence, higher rates on Rs29bn of short-term debt, SEZ delays and a gross margin (15% in FY26) that may be at a peak.","Muzzaffar Hayat Piracha, founder and CEO since 2010, holds 24.45%. Brother Yasir holds 24.23% and the chairman Aslam Hayat Piracha is family, so the sponsor family holds about 74%. He built sales from Rs6bn (FY15) to Rs130bn (FY24) and beat his Rs100bn FY24 target, but missed the 150-outlet IPO target and sold Rs1.0bn of stock in Oct 2024.","Consolidated operating cash flow was -Rs2.8bn (FY24) and -Rs8.7bn (FY25), and about -Rs5bn in FY26 (CSV, unverified), against about Rs15bn of reported profit. Short-term borrowings were Rs29.6bn at Jun 2025, finance cost Rs4.4bn in FY26. | CEO sold 7.5m shares at Rs135.25 (Rs1.01bn) on 3 Oct 2024. 30m sponsor shares (Rs2.145bn) were sold in the 2021 IPO. His holding fell from 100.16m to 96.66m with no matching filing in the CSV (unverified). | FY26 dividend cut to Rs2.0 on EPS 15.75 (13% payout); final nil, announced 29 Sep 2026. | Scope keeps widening: Zexo, AirFin BNPL (Rs500m), e-bikes, Hisense ACs, Acer laptops, Shell Pakistan bid (withdrawn Apr 2024). | Four revoked filings (Oct 2021, Oct 2022, Oct 2023, Sep 2024). Deck figures disagree: FY23 sales Rs36.9bn vs Rs21.5bn, and FY24 debt-to-equity shown as 19% against Rs13.7bn borrowings on about Rs15bn equity. | Q4 FY26 profit Rs2.58bn is 41% of the year and the cause is unverified. The Select IPO sold 10% of the best asset to outsiders."
FATIMA,3,2,3,4,12,"Core fertilizer is capped near 2.57Mt (111% utilisation in 2025), so 2x EPS in five years rests on unproven PIA (up to Rs50bn), E&P and mining, none of which management calls material today.","Arif Habib (chairman, Arif Habib Group) and Fawad Ahmed Mukhtar (CEO, Fatima Group), both re-appointed for 3 years from 22 Sep 2026; long builders of the plants (Sadiqabad, Pakarab, DH Fertilizers) with high continuity, but restructurings have taken years and been reversed.","Multan plant: Pakarab amalgamated into Fatima 27 Jun 2023, then Multan carved back into Pakarab as a subsidiary from 1 Jan 2025 (reversal in 18 months) | Sheikhupura carve-out proposed 2020, executed Jul 2024 (four years, deferred twice) | Interim dividend nil for H1 2026 citing capital commitments while funding sponsor-led PIA bid (up to Rs50bn, about 17% of market cap) | Related-party exposure: Rs15bn in REITs run by Arif Habib Dolmen, Arif Habib on both sides of the PIA deal, loans to Reliance Commodities | Operating cash flow about Rs5bn (2024) and Rs28bn (2025) vs profit Rs36bn and Rs42bn (quarterly file, not checked in statements) | Finance cost +56% in 2025 from borrowing for an 'arbitrage opportunity'; other income 38% of 2025 PAT while operating profit fell 1% | Gas pressure enhancement project still 'operational in 2026' per AR 2025 after a 2022 framework agreement | Q1 2026 EPS 1.54 then Q2 8.19, cause unverified | Samba Bank bid (Dec 2021) withdrawn May 2022, reason unverified (scanned)"
GHNI,3,3,2,3,11,"No clear 2x in 5 years: FY26 is a peak (record truck market of 8,424 units, 23% gross margin versus 12 to 14% in FY21 to FY22). Possible but unproven upside from Zhongtong buses, UD Trucks (from Q1 2027), D-Max and income on Rs15.4bn of cash and funds. Expect cyclical earnings.","Chairman Lt Gen (R) Ali Kuli Khan Khattak and CEO Ahmad Kuli Khan Khattak, Bibojee family (about 57% with sister company GAL). The record is market leadership every year with no numeric guidance. Share was lost in FY23 and FY26, and diversification was four years late. Deputy CEO Muhammad Kuli Khan is the next generation.","Dividend payout is 7 to 9% (Rs10 for FY25, Rs12 for FY26) and nil for FY24, on Rs15.4bn of cash and funds (AR 2026, 283092) | Assembly is outsourced to GAL, a 17.9% holder: Rs2.5bn of FY26 purchases, Rs4.7bn of stock held there. GAL also sells rival JAC trucks (AR 2026; CBS 265610) | Related-party property deal with Business Vision: Rs171m advance in FY24 for a floor, sold back in FY26 at Rs554m (AR 2026 note 6.8.4) | Rs18.4bn of customer advances fund the cash pile and would unwind if demand turns (AR 2026 note 24) | Essar Asset Management dividend and bonus withheld by Sindh High Court order since 16 Nov 2018 (AR 2026 note 25) | Peak-cycle earnings: record 8,424-unit market, rates tightening, inflation 11.07% in June 2026 | Share fell from 59% to 53% in FY26 while the market grew 61% | No Q&A, no guidance, Isuzu agreement terms undisclosed (unverified), material filings are scans, one insider filing revoked in 2022"
PSO,2,2,2,4,10,"Nothing organic doubles earnings. Upside is policy that PSO does not control: a circular-debt settlement (a Rs250bn paydown would save roughly Rs30bn of pre-tax finance cost, my arithmetic) or the Rs1.22/litre margin rise (about Rs9bn). The PRL upgrade is the only builder project and has no final investment decision.","CEO Jawwad Ahmed Cheema since 27 Apr 2026 (ex-CEO of Shell Pakistan and Karachi Hydrocarbon Terminal, PRL director) has six months in the role. Predecessor Syed Muhammad Taha (Feb 2020 to Mar 2026) left for K-Electric. The sponsor is the state: 22.47% direct and about 51% direct plus indirect. Chairman Asif Baigmohamed since May 2023.","State control: government-nominee board, windfall recovery (Section 99D) and a margin hike tied to digitisation hang over holders | Trade debts Rs414.8bn (about 1.5x equity), mostly SNGPL, GENCOs and PIA; LNG receivable Rs276bn; Rs371bn overdue at FY24 against a Rs347m specific provision | White oil share fell from 51.6% (FY24) to 45.7% (FY25) to 42.7% (FY26) despite a share-maintenance target | Strategy items disappear without explanation: the Aramco/Sinopec greenfield refinery is absent from the FY25 and FY26 reports, and the LNG tripartite agreement and the receivable-equity swap are dropped | PRL FEED slipped over a year, and there is still no final investment decision in Sep 2026 | CEO churn: seven CEO/MD notices from Mar 2019 to Feb 2020, then an interim CEO, a new CEO and a changed start date in Mar to Apr 2026; board resignations 15 Jun and 3 Sep 2026 with no reasons given | Earnings swing with inventory: standalone profit Rs86bn in FY22, Rs5.7bn in FY23, and a Q4FY26 loss | Return on equity is mostly 4 to 11%, below a cost of equity near 17% | Flat Rs10 dividend whatever the profit, with no stated payout policy"
GGL,2,2,3,3,10,"Hattar 275 TPD gas plant at tax-exempt margins, calcium carbide (management guided Rs8bn sales in FY27), and the Rs14bn Mari gas-capture JV could double earnings by FY31. This needs debt-funded capex and on-time execution, which the company has not delivered so far.",Masroor Ahmad Khan (CEO) and Atique Ahmad Khan (chairman). The sponsor family holds 47.2% with spouses and children. They have run the group since 2007 and built five gas plants. Every large project has slipped 1 to 2 years.,"1 to 2 year delays on every large project: Hattar gas plant promised Q2 2023, then Q1 2024, then Dec 2024, delivered Apr 2025; carbide promised Q1 2024, production began Dec 2025 | FY25 headline EPS 8.97 was inflated by a Rs1.93bn bargain purchase gain; FY26 EPS 4.15 (restated FY25: 8.94); FY25 restated for deferred tax | Receivables up 53% to Rs4.46bn on 8% sales growth (about 145 days); short-term borrowings up 57%; finance cost up 28%; capex above operating cash flow in FY25 and FY26 | Real-estate REIT scheme inside a gas and glass holdco: 75m shares to a GGL subsidiary and 60m to partners of G3 Homes LLP (sponsor real estate); asset valuation not verified | Class B tracking shares added to the articles at board discretion; no holdco cash dividend in any recorded year | High board churn (director changes Sep 2024 to Jul 2026) and two internal-audit head changes in 2024 | FY26 annual report and Jul 2026 briefing are scanned and were not read; carbide FY26 revenue against the Rs3.5 to 4bn guidance is unverified"

=== FILE: base_rates.csv ===
# WARNING: measured through 2026-10-16, partly AFTER this replay date. Use only as rough odds for a situation TYPE; infer nothing about specific names or dates. Note: the replay model may remember this period; cite only the bundle.
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
corp_E1a_buyback_approval,20 sessions (KMI members),,54%,+0.7%,,,,nothing
corp_E1a_buyback_approval,60 sessions (KMI members),13,54%,+0.7%,0%,-19%,-1.2%,nothing; mean +1.2%; <-30% 0%; p(med) 0.40; placebo is matched P2 median
corp_E1a_buyback_approval,120 sessions (KMI members),11,64%,+4.8%,,,,nothing
corp_E1a_buyback_approval,20% trailing stop (KMI members),12,42%,-3.5%,17%,-23%,,nothing; stop mean +46.3%
corp_E1b_first_purchase,20 sessions (KMI members),,33%,-1.8%,,,,nothing
corp_E1b_first_purchase,60 sessions (KMI members),15,47%,-2.4%,0%,-17%,+0.6%,nothing; mean +0.1%; <-30% 0%; p(med) 0.74; placebo is matched P2 median
corp_E1b_first_purchase,120 sessions (KMI members),13,62%,+5.7%,,,,nothing
corp_E1b_first_purchase,20% trailing stop (KMI members),14,36%,-6.5%,14%,-23%,,nothing; stop mean +62.0% (THCCL runner)
corp_E2a_bonus,20 sessions (KMI members),,42%,-2.9%,,,,nothing
corp_E2a_bonus,60 sessions (KMI members),89,39%,-6.0%,2%,-35%,-3.9%,nothing; mean -1.6%; <-30% 4%; p(med) 0.84; placebo is matched P2 median
corp_E2a_bonus,120 sessions (KMI members),88,39%,-7.4%,,,,nothing
corp_E2a_bonus,20% trailing stop (KMI members),89,31%,-12.8%,8%,-28%,,nothing; stop mean +0.5%
corp_E2b_split,20 sessions (KMI members),,50%,+2.0%,,,,watch
corp_E2b_split,60 sessions (KMI members),9,89%,+13.9%,0%,-13%,-3.4%,watch (thin tail); mean +14.8%; <-30% 0%; p(med) 0.04; placebo is matched P2 median
corp_E2b_split,120 sessions (KMI members),8,62%,+12.9%,,,,watch
corp_E2b_split,20% trailing stop (KMI members),9,67%,+11.3%,11%,-23%,,watch; stop mean +20.1%
corp_E3a_ceo_chairman_appointed,20 sessions (KMI members),,42%,-1.5%,,,,nothing
corp_E3a_ceo_chairman_appointed,60 sessions (KMI members),526,49%,-0.5%,5%,-97%,-1.6%,nothing; mean +2.9%; <-30% 6%; p(med) 0.14; placebo is matched P2 median
corp_E3a_ceo_chairman_appointed,120 sessions (KMI members),496,47%,-2.1%,,,,nothing
corp_E3a_ceo_chairman_appointed,20% trailing stop (KMI members),511,36%,-8.5%,10%,-90%,,nothing; stop mean +6.1%
corp_E3b_resigns,20 sessions (KMI members),,48%,-1.5%,,,,nothing (lean avoid)
corp_E3b_resigns,60 sessions (KMI members),27,48%,-4.9%,4%,-66%,+0.1%,nothing (lean avoid); mean -2.5%; <-30% 4%; p(med) 0.90; placebo is matched P2 median
corp_E3b_resigns,120 sessions (KMI members),26,35%,-6.9%,,,,nothing (lean avoid)
corp_E3b_resigns,20% trailing stop (KMI members),25,20%,-13.0%,12%,-30%,,nothing (lean avoid); stop mean -3.2%
corp_E3d_takeover_or_mgmt_change,20 sessions (KMI members),,35%,-2.1%,,,,nothing
corp_E3d_takeover_or_mgmt_change,60 sessions (KMI members),74,50%,+0.0%,5%,-66%,-1.4%,nothing; mean +1.4%; <-30% 7%; p(med) 0.24; placebo is matched P2 median
corp_E3d_takeover_or_mgmt_change,120 sessions (KMI members),71,49%,-0.6%,,,,nothing
corp_E3d_takeover_or_mgmt_change,20% trailing stop (KMI members),72,40%,-7.8%,8%,-53%,,nothing; stop mean +4.4%
corp_E4a_psx_letter,20 sessions (KMI members),,41%,-4.0%,,,,nothing as a buy; avoid after a run-up
corp_E4a_psx_letter,60 sessions (KMI members),373,43%,-3.7%,8%,-82%,-0.6%,nothing as a buy; avoid after a run-up; mean +4.6%; <-30% 10%; p(med) 1.00; placebo is matched P2 median
corp_E4a_psx_letter,120 sessions (KMI members),318,52%,+0.7%,,,,nothing as a buy; avoid after a run-up
corp_E4a_psx_letter,20% trailing stop (KMI members),394,34%,-12.6%,11%,-80%,,nothing as a buy; stop mean +9.3%
corp_E4b_company_reply,20 sessions (KMI members),,43%,-3.9%,,,,nothing
corp_E4b_company_reply,60 sessions (KMI members),29,59%,+4.0%,14%,-58%,-0.2%,nothing (n 29); mean +20.4%; <-30% 10%; p(med) 0.22; placebo is matched P2 median
corp_E4b_company_reply,120 sessions (KMI members),25,56%,+4.7%,,,,nothing
corp_E4b_company_reply,20% trailing stop (KMI members),29,41%,-7.7%,7%,-26%,,nothing; stop mean +11.2%
corp_E5_rating_upgrade,20 sessions (KMI members),,57%,+2.1%,,,,nothing (anecdote)
corp_E5_rating_upgrade,60 sessions (KMI members),7,57%,+8.5%,0%,-28%,+0.2%,nothing (anecdote); mean +3.1%; <-30% 0%; p(med) 0.15; placebo is matched P2 median
corp_E5_rating_upgrade,120 sessions (KMI members),6,33%,-5.7%,,,,nothing (anecdote)
corp_E5_rating_upgrade,20% trailing stop (KMI members),7,43%,-8.4%,14%,-21%,,nothing (anecdote); stop mean +4.6%
corp_E6_rights_issue,20 sessions (KMI members),,34%,-4.5%,,,,avoid
corp_E6_rights_issue,60 sessions (KMI members),76,33%,-9.1%,7%,-66%,-3.8%,avoid; mean -4.6%; <-30% 14%; p(med) 0.99; placebo is matched P2 median
corp_E6_rights_issue,120 sessions (KMI members),72,28%,-15.4%,,,,avoid
corp_E6_rights_issue,20% trailing stop (KMI members),75,25%,-15.2%,4%,-37%,,avoid; stop mean -6.9%
corp_E7_kmi_addition,20 sessions (KMI members),,51%,+0.2%,,,,nothing (avoid chasing)
corp_E7_kmi_addition,60 sessions (KMI members),388,36%,-4.9%,3%,-62%,-0.2%,nothing (avoid chasing); mean +0.7%; <-30% 4%; p(med) 1.00; placebo is matched P2 median
corp_E7_kmi_addition,120 sessions (KMI members),352,41%,-5.1%,,,,nothing (avoid chasing)
corp_E7_kmi_addition,20% trailing stop (KMI members),378,33%,-10.3%,10%,-42%,,nothing; stop mean +5.5%
compounders_3x_share_5y,5 years (start 2016-12-30),155,3.2%,,,,,watch (population; 5 names with 3x)
compounders_3x_share_5y,5 years (start 2017-12-29),85,2.4%,,,,,watch (population; 2 names with 3x)
compounders_3x_share_5y,5 years (start 2018-12-31),97,5.2%,,,,,watch (population; 5 names with 3x)
compounders_3x_share_5y,5 years (start 2019-12-31),111,16.2%,,,,,watch (population; 18 names with 3x)
compounders_3x_share_5y,5 years (start 2020-12-31),124,23.4%,,,,,watch (population; 29 names with 3x)
compounders_3x_share_5y,5 years (start 2021-09-30),137,21.2%,,,,,watch (population; 29 names with 3x)
compounders_3x_share_5y,5 years (pooled over 58 starts; n is the average),108,12.1%,,,,,watch (population; 75 names had a 3x window)
compounders_3x_share_decade,9.8 years (2016-12-30 to 2026-10-16),155,20.0%,,,,,watch (population; 31 names with 3x)
compounders_growth_core_1y_position,1 year rule variant (start 2023-09-28; position level; file label 1y variant),39,51%,+6.6%,26%,-35.3%,,nothing; mean +26.3%; 8% below -30%
compounders_growth_core_2y_position,2 year rule variant (start 2024-09-30; position level; file label 2y variant),23,61%,+10.1%,26%,-52.6%,,nothing; mean +24.6%; 4% below -30%
compounders_growth_core_3y_position,3 year rule variant (position level; file label 3y variant),17,24%,-8.0%,,,,nothing; mean -4.7%
compounders_growth_core_3y_fixed,1.04 years (start 2025-09-30),,,,,,,nothing; fixed 0.88x (-11.7%) vs KMI TR 0.96x; EW liquid KMI 0.88x; placebo median 0.93x (pctile 30); max DD -27.9 / -21.3; numeric columns blank because outcome is a multiple
compounders_growth_core_3y_quality_fixed,1.04 years (start 2025-09-30),,,,,,,nothing; fixed 0.82x vs KMI TR 0.96x; EW 0.88x; placebo median 0.86x (pctile 35); numeric columns blank because outcome is a multiple
compounders_growth_core_2y_fixed,2.04 years (start 2024-09-30),,,,,,,nothing; fixed 1.73x (+30.6%) vs KMI TR 1.81x (+33.6%); EW 1.50x; placebo median 1.88x (pctile 30); numeric columns blank because outcome is a multiple
compounders_growth_core_2y_quality_fixed,2.04 years (start 2024-09-30),,,,,,,nothing; fixed 1.71x vs KMI TR 1.81x; EW 1.50x; placebo median 1.91x (pctile 24); numeric columns blank because outcome is a multiple
compounders_growth_core_1y_fixed,3.05 years (start 2023-09-28),,,,,,,nothing; fixed 2.80x (+40.2%) vs KMI TR 2.87x (+41.2%); EW 2.19x; placebo median 2.80x (pctile 51); numeric columns blank because outcome is a multiple
compounders_growth_core_1y_quality_fixed,3.05 years (start 2023-09-28),,,,,,,nothing; fixed 2.82x vs KMI TR 2.87x; EW 2.19x; placebo median 2.69x (pctile 56); numeric columns blank because outcome is a multiple
=== END ===
