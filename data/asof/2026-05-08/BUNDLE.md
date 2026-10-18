# Replay bundle, close of 2026-05-08 (brief v2)

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
# Market as of 2026-05-08 close (public information only)

- KSE100: 171,116 on 2026-05-08; 1m +3.2%, 3m -8.9%, 6m +7.6%, 12m +65.3%
- KMI All Share: 66,650 on 2026-05-08; 1m +2.8%, 3m -8.0%, 6m +6.0%, 12m +51.2%
- Policy rate 11.5%; last MPC decision 2026-04-27: hike (+100bp)
- 6M T-bill cutoff 11.98% (auction 2026-04-29); 3M 11.84%, 12M 12.10%
- CPI YoY 10.91% for 2026-04 (published by 2026-05-03); three months earlier (2026-01) 5.79%
- Brent: 103.48 USD/bbl on 2026-05-08; 3-month change +46.9%
- USD/PKR: 278.91  on 2026-05-08; 3-month change -0.3%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.48pp (market near policy rate); CPI rising over 3 months (+5.1pp)
- Next MPC: see SBP calendar

Session date used: 2026-05-08. Liquid KMI names: 116 (membership KMI_ALL_derived_2025-12-02.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.043,0.0023,0.1663,0,0
E&P,3,0.0135,-0.072,0.196,0,1
OMC,4,0.2489,-0.0647,0.0739,1,1
Power,6,0.0562,-0.0593,0.1914,0,0
Fertilizer,4,-0.0258,-0.1178,0.1252,0,0
Cement,16,0.0591,-0.1526,-0.0542,0,0
Steel & engineering,11,0.1091,-0.0838,-0.0438,0,0
Autos,12,0.177,-0.0847,-0.0456,1,1
Tech & telecom,12,0.0105,-0.0577,-0.0548,0,0
Islamic banks & fin.,10,0.0381,-0.064,-0.1653,0,0
Pharma,14,0.0225,-0.1432,-0.0603,0,0
Textiles,23,0.2166,0.031,0.1082,0,1
Food & staples,15,0.0994,-0.1225,-0.0122,0,1
Chemicals,19,0.1148,-0.0378,0.1071,0,0
"Glass, packaging, paper",14,0.1397,-0.0772,0.0366,0,0
Gas utilities & misc,13,0.093,-0.1381,-0.0739,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ABOT,891.67,-0.055,-0.211,-0.154,0.141,-0.285,1.849,0,2026-03-31,0.213,2,0,0,0,,
ACPL,231.86,-0.164,-0.184,-0.191,-0.009,-0.258,1.619,0,2025-06-30,-0.687,2,3,0,0,23.229,0.027
AGP,187.38,0.02,-0.1,0.006,0.305,-0.204,1.198,0,2026-03-31,0.007,2,6,0,0,15.229,0.039
AGTL,370.39,0.077,-0.112,-0.105,-0.044,-0.215,1.026,0,2026-03-31,,2,0,0,0,17.853,
AIRLINK,142.61,0.035,-0.231,-0.215,0.166,-0.256,0.772,0,2026-03-31,0.111,3,0,0,0,12.707,0.046
ANL,10.62,0.083,-0.1,-0.069,0.578,-0.192,1.269,0,,,3,0,0,0,,
ASL,12.11,0.119,-0.132,-0.083,0.313,-0.216,0.811,0,2026-03-31,-0.812,3,0,0,0,,
ATRL,903.72,0.034,0.032,0.406,1.025,-0.071,1.014,0,2026-03-31,,2,2,0,0,8.095,0.015
AVN,37.17,0.131,-0.086,-0.155,-0.088,-0.296,1.137,0,2026-03-31,-0.794,3,1,0,0,,
BBFL,45.0,0.121,-0.078,-0.062,0.022,-0.198,1.113,0,,,2,0,0,0,,
BECO,5.66,0.139,-0.024,-0.919,-0.267,-0.921,0.971,0,2026-03-31,1.75,2,0,0,0,20.344,
BFAGRO,33.69,-0.045,-0.182,-0.117,0.348,-0.299,1.355,0,,,3,0,0,0,,
BFBIO,139.93,-0.024,-0.173,-0.088,0.143,-0.258,0.445,0,2026-03-31,-0.164,3,0,0,0,33.326,
BIFO,140.35,0.549,-0.058,-0.006,0.083,-0.163,3.456,3,2026-03-31,-0.428,2,0,0,0,,
BIPL,25.95,-0.045,-0.179,-0.122,0.568,-0.364,1.381,0,2026-03-31,-0.657,2,1,0,0,,
BNL,8.38,-0.028,-0.257,-0.929,-0.631,-0.948,0.596,0,2025-06-30,,2,0,0,0,,
CEPB,29.97,0.058,-0.287,-0.023,0.441,-0.334,0.591,0,2026-03-31,,2,0,0,0,,
CHCC,289.3,0.079,-0.116,-0.089,0.213,-0.211,1.053,0,2026-03-31,-0.165,3,0,0,0,6.497,0.019
CLOV,8.89,0.337,0.147,1.286,1.632,-0.048,5.114,0,2026-03-31,1.333,2,1,0,0,,
CNERGY,8.53,0.087,0.112,0.101,0.491,-0.06,1.916,0,2024-06-30,,2,0,0,0,,
CPHL,80.64,0.01,-0.097,-0.016,0.249,-0.177,1.413,0,2026-03-31,0.26,2,1,0,0,21.506,0.042
CRTM,73.02,0.078,2.042,2.172,5.193,-0.17,1.389,2,,,2,0,0,0,,
CSAP,92.61,-0.093,-0.301,-0.047,-0.025,-0.32,0.978,0,2026-03-31,-1.217,2,0,0,0,,0.065
DCL,10.72,0.249,-0.126,-0.159,0.186,-0.324,1.72,0,,,2,0,0,0,,
DCR,36.27,-0.006,-0.058,0.173,0.508,-0.072,0.794,0,2026-03-31,0.121,3,0,0,0,7.515,0.083
DGKC,190.31,0.118,-0.162,-0.112,0.605,-0.293,1.774,0,2026-03-31,0.288,2,0,0,0,7.851,0.012
EFERT,197.91,-0.066,-0.144,0.001,0.364,-0.201,0.674,0,2026-03-31,0.148,3,0,0,0,13.357,0.066
ENGROH,279.5,-0.032,0.009,0.281,0.903,-0.062,1.068,0,2026-03-31,4.27,2,0,0,0,5.136,
EPCL,34.8,-0.055,0.111,0.239,0.308,-0.098,0.514,0,2026-03-31,,2,1,0,0,,
EPQL,23.44,-0.083,-0.227,-0.151,0.06,-0.286,0.928,0,2026-03-31,-0.605,2,0,0,0,,
FABL,89.25,0.01,-0.061,0.077,1.262,-0.107,0.772,0,2026-03-31,-0.014,3,0,0,0,6.266,0.07
FATIMA,137.43,0.007,-0.254,0.082,0.886,-0.254,0.975,0,2026-03-31,-0.614,2,0,0,0,7.57,0.04
FCCL,51.85,0.107,-0.095,0.005,0.329,-0.151,1.121,0,2025-12-31,0.0,3,1,0,0,8.222,0.028
FCEPL,104.59,0.364,0.22,0.253,0.45,-0.002,2.3,2,2024-09-30,2.03,2,0,0,0,24.633,0.04
FCL,23.4,0.02,-0.111,0.006,0.21,-0.156,0.811,0,2026-03-31,0.086,3,1,0,0,12.305,0.021
FECTC,92.88,-0.016,-0.398,-0.366,0.556,-0.512,0.393,0,2026-03-31,-0.309,2,0,0,0,,
FEROZ,400.91,0.075,-0.108,-0.003,0.647,-0.118,1.828,0,,,2,0,0,0,,
FFC,532.94,-0.016,-0.082,0.098,0.711,-0.195,0.57,0,2025-12-31,-0.021,2,0,0,0,10.107,0.063
FFL,17.45,0.065,-0.196,-0.065,0.429,-0.247,0.888,0,2026-03-31,-0.077,2,0,0,0,45.156,
GAL,454.64,0.361,-0.133,-0.182,0.141,-0.255,1.592,0,2026-03-31,0.611,2,0,0,0,5.252,0.026
GATM,23.02,0.167,-0.244,-0.129,0.171,-0.424,1.199,0,2026-03-31,-1.131,2,0,0,0,4.564,
GCIL,29.09,-0.031,-0.142,-0.079,1.047,-0.244,0.652,0,,,2,0,0,0,,
GCWL,17.16,-0.085,-0.298,-0.06,2.07,-0.298,0.441,0,,,2,0,0,0,,
GDL,21.54,0.096,,,,,1.266,0,2026-03-31,0.031,2,0,0,0,,
GGL,18.96,0.106,-0.218,-0.205,0.848,-0.352,0.709,0,2026-03-31,0.247,2,2,0,0,2.013,
GHGL,37.16,0.039,0.026,0.186,0.494,-0.21,0.705,0,2026-03-31,0.388,3,0,0,0,,
GHNI,857.55,0.258,-0.11,0.078,0.341,-0.151,1.417,0,2026-03-31,0.541,2,0,0,0,6.046,0.015
GLAXO,364.64,0.054,-0.121,-0.033,0.202,-0.168,1.093,0,2026-03-31,0.228,3,0,0,0,12.382,0.044
GTYR,30.11,0.102,-0.251,-0.182,-0.061,-0.394,0.85,0,2026-03-31,-5.656,2,0,0,0,,
GWLC,52.29,0.059,-0.133,0.007,0.524,-0.303,0.75,1,2026-03-31,0.128,2,0,0,0,,
HALEON,787.08,0.1,-0.139,-0.036,0.203,-0.189,1.38,0,2026-03-31,0.132,2,0,0,0,15.305,0.036
HCAR,234.02,0.344,-0.054,-0.19,0.025,-0.248,2.701,3,2025-12-31,0.156,0,0,0,0,15.254,0.028
HINOON,978.0,0.118,-0.011,-0.07,0.252,-0.164,1.24,0,2025-12-31,0.458,3,0,0,0,,
HTL,43.84,0.139,-0.248,-0.149,0.312,-0.305,1.687,0,,,2,0,0,0,,
HUBC,216.53,0.014,-0.033,0.066,1.038,-0.071,0.826,0,2026-03-31,-0.021,4,0,0,0,3.875,0.109
IBLHL,48.05,0.062,-0.206,0.081,0.827,-0.402,0.444,0,,,2,0,0,0,,
ICL,150.14,0.151,-0.019,0.163,1.36,-0.098,0.617,0,,,2,0,0,0,,
ILP,83.64,0.013,-0.065,0.076,0.868,-0.097,0.96,0,2026-03-31,0.918,3,0,0,0,17.114,0.015
IMAGE,24.13,0.09,-0.044,0.008,0.381,-0.31,1.059,0,2026-03-31,-0.033,2,0,0,0,,
INIL,159.2,0.013,-0.09,-0.166,0.363,-0.327,0.93,0,2026-03-31,-0.172,2,0,0,0,25.968,0.023
IPAK,30.19,0.077,-0.06,0.208,0.567,-0.068,0.936,0,2026-03-31,1.015,3,0,0,0,13.394,0.027
ISL,79.54,0.086,-0.233,-0.129,0.291,-0.366,0.89,0,2026-03-31,0.896,2,0,0,0,25.861,0.027
ITTEFAQ,7.94,-0.033,-0.177,-0.126,0.444,-0.345,0.828,0,,,2,0,0,0,,
JVDC,138.3,0.219,-0.09,0.912,1.738,-0.136,1.057,0,2026-03-31,2.407,2,0,0,0,14.977,0.078
KEL,8.12,0.02,-0.023,0.544,1.071,-0.138,0.668,0,2024-06-30,-0.871,0,1,0,0,30.127,
KOHC,88.06,0.045,-0.189,-0.062,0.304,-0.28,0.608,0,2026-03-31,-0.151,2,0,0,0,6.026,
KSBP,193.48,-0.056,0.03,-0.018,0.24,-0.258,0.338,0,2026-03-31,0.169,2,0,0,0,,
KTML,49.12,0.115,-0.24,-0.036,0.944,-0.331,0.404,0,2024-12-31,1.398,2,0,0,0,3.207,0.01
LCI,233.71,-0.058,-0.141,-0.216,-0.065,-0.372,0.458,0,2026-03-31,-0.271,2,0,0,0,12.485,0.041
LOADS,13.68,0.112,-0.21,-0.23,0.057,-0.34,3.228,1,2026-03-31,1.714,2,0,0,0,13.777,
LOTCHEM,27.4,0.085,0.094,0.219,0.96,-0.084,1.285,0,2026-03-31,1.204,2,1,0,0,39.488,0.171
LUCK,445.73,0.06,-0.065,0.014,0.562,-0.131,1.134,0,2026-03-31,0.063,2,0,0,0,6.763,0.011
MACFL,47.29,1.076,0.453,0.877,2.61,-0.272,1.651,7,2026-03-31,0.777,2,0,0,0,34.336,0.01
MARI,650.81,-0.055,-0.078,-0.038,0.248,-0.165,0.656,0,2026-03-31,0.311,2,0,0,0,11.514,0.035
MEBL,485.95,-0.049,-0.008,0.208,1.082,-0.049,0.639,0,2026-03-31,0.006,2,0,0,0,8.82,0.063
MLCF,88.96,0.07,-0.222,-0.031,0.462,-0.318,1.438,0,2024-12-31,0.708,2,0,0,0,7.675,
MTL,569.71,0.078,0.033,0.129,0.147,0.0,1.072,0,2026-03-31,1.227,2,2,0,0,17.531,0.107
MUGHAL,76.23,0.119,-0.189,-0.113,0.386,-0.31,0.74,0,2026-03-31,0.676,3,0,0,0,28.337,
NETSOL,140.34,0.247,0.118,0.045,0.225,-0.137,2.478,1,2026-03-31,3.392,3,2,0,0,8.173,
NML,152.39,0.048,-0.228,0.055,0.523,-0.257,0.884,1,2026-03-31,0.835,2,0,0,0,8.671,0.016
NRL,382.68,0.045,-0.148,0.054,1.256,-0.174,1.028,0,2026-03-31,,3,0,0,0,,
OBOY,9.76,0.089,-0.288,0.11,0.228,-0.349,0.687,0,,,2,0,0,0,,
OCTOPUS,33.18,-0.032,-0.156,-0.246,-0.195,-0.441,0.913,0,,,3,0,0,0,,
OGDC,329.68,0.088,0.018,0.367,0.96,-0.012,1.156,0,2026-03-31,-0.104,2,0,0,0,5.583,0.068
PAEL,40.85,0.103,-0.287,-0.246,0.104,-0.352,1.584,0,2026-03-31,0.324,2,0,0,0,13.768,
PIBTL,17.13,0.076,-0.172,0.124,1.413,-0.242,0.942,0,2026-03-31,,2,0,0,0,,
PIOC,278.38,0.211,-0.19,0.328,0.622,-0.339,0.251,2,2026-03-31,0.562,2,0,0,0,10.627,0.044
POWER,19.66,0.014,-0.086,0.132,0.466,-0.09,0.775,0,2026-03-31,2.0,3,0,0,0,31.257,
PPL,229.93,0.009,-0.157,0.28,0.815,-0.176,0.778,0,2026-03-31,-0.06,2,0,0,0,5.148,0.044
PREMA,34.66,0.279,-0.174,-0.149,-0.267,-0.345,1.566,1,2026-03-31,-0.133,2,1,0,0,16.658,
PRL,36.16,0.0,-0.049,0.026,0.49,-0.098,1.55,0,2026-03-31,,3,0,0,0,,
PSO,364.97,-0.014,-0.246,-0.162,0.196,-0.275,1.157,0,2026-03-31,6.803,2,0,0,0,10.778,0.026
QUICE,26.7,0.071,-0.197,1.675,3.82,-0.362,0.686,2,,,2,0,0,0,,
SAZEW,2181.66,0.23,-0.024,0.248,1.016,-0.103,1.449,0,2026-03-31,0.034,2,0,0,0,4.217,0.046
SEARL,93.42,0.018,-0.257,-0.153,0.612,-0.308,0.757,0,2026-03-31,,2,1,0,0,,
SGF,118.99,0.365,-0.072,0.332,0.778,-0.078,1.037,1,2026-03-31,3.0,2,1,0,0,,
SGPL,71.98,1.93,1.534,5.09,10.074,0.0,1.767,7,2026-03-31,,2,0,0,0,,
SLGL,15.35,0.008,-0.276,-0.215,0.16,-0.389,0.506,0,2026-03-31,0.064,2,0,0,0,11.307,
SNGP,99.63,0.023,-0.111,-0.137,0.025,-0.272,1.323,0,2026-03-31,0.226,2,1,0,0,5.073,0.026
SPEL,44.92,0.078,-0.184,-0.158,0.327,-0.416,0.68,1,2026-03-31,-0.084,2,0,0,0,,
SSGC,27.91,0.169,-0.175,-0.173,-0.031,-0.391,2.462,0,2026-03-31,-0.48,2,0,0,0,10.954,0.012
SSOM,423.49,-0.034,-0.002,-0.085,-0.174,-0.6,0.994,0,,,2,0,0,0,,
SYM,10.65,-0.051,-0.242,-0.205,-0.094,-0.333,1.752,0,2026-03-31,-0.8,2,1,0,0,,
SYS,153.89,0.011,-0.029,0.052,0.626,-0.089,0.622,0,2025-12-31,0.5,1,0,0,0,22.795,0.012
TATM,146.4,0.503,-0.121,0.07,2.836,-0.502,0.873,2,2026-03-31,,2,0,0,0,6.525,
TBL,9.49,-0.06,-0.235,-0.181,-0.05,-0.356,2.324,0,,,2,0,0,0,,
TELE,8.69,0.036,-0.276,-0.24,0.552,-0.345,0.947,0,2026-03-31,0.464,2,0,0,0,18.478,
TGL,167.0,0.093,-0.199,-0.064,-0.008,-0.4,0.895,0,2026-03-31,-0.111,2,0,0,0,9.051,0.016
TOMCL,34.85,-0.002,-0.327,-0.404,0.48,-0.474,0.537,0,2026-03-31,-0.848,2,0,0,0,13.655,
TPLP,8.65,0.178,-0.288,-0.152,0.282,-0.33,1.158,0,,,2,0,0,0,,
TPLT,15.5,0.694,0.174,1.144,2.222,-0.015,1.982,1,,,2,0,0,0,,
TREET,25.02,0.043,-0.263,-0.224,0.524,-0.308,0.912,0,2026-03-31,-1.0,2,0,0,0,17.461,
TRSM,17.06,0.086,0.072,-0.742,2.607,-0.751,0.81,3,2026-03-31,-2.0,2,0,0,0,,
WAFI,199.5,0.046,-0.176,0.086,0.528,-0.184,1.006,0,2026-03-31,1.478,3,0,0,0,13.409,0.032
WAVES,10.69,-0.002,-0.35,-0.302,0.61,-0.35,0.774,0,2026-03-31,0.042,4,0,0,0,8.618,
ZAL,48.01,0.148,-0.303,-0.031,2.518,-0.336,0.985,0,2026-03-31,-3.118,2,0,0,0,6.31,0.062

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2026-05-04,NETSOL,material_info,Material Information REVOKED
2026-05-04,AGP,material_info,Material Information
2026-05-04,AGP,material_info,Material Information
2026-05-04,NETSOL,material_info,Material Information (Revise) REVISED
2026-05-04,ATRL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2026-05-04,NETSOL,financial_result,Financial Results for the Quarter Ended 2026-03-31
2026-05-04,WAVES,financial_result,Transmission of Quarterly Report for the Period Ended 31 March 2026
2026-05-04,TATM,financial_result,"Transmission of Quarterly Report for the Nine Month Period Ended March 31, "
2026-05-04,NETSOL,financial_result,Transmission of Quarterly Financial Statements for the Period Ended March 3
2026-05-04,SGPL,financial_result,Transmission of Quarterly Financial Statements for the Period Ended March 3
2026-05-04,FATIMA,insider_trade,Insider trade disclosure
2026-05-04,SGPL,insider_trade,Insider trade disclosure
2026-05-05,TELE,financial_result,Financial Results for the Quarter Ended 31 March 2026
2026-05-05,POWER,financial_result,"Mandatory Shariah Disclosure for the Half Year Ended December 31, 2025"
2026-05-05,SYM,insider_trade,Insider trade disclosure
2026-05-05,KSBP,insider_trade,Insider trade disclosure
2026-05-06,FCL,material_info,Disclosure of Material Information - Consolidation of Manufacturing Units
2026-05-06,CPHL,material_info,Material Information
2026-05-06,CLOV,financial_result,"Transmission of Quarterly Report for the Period Ended March 31, 2026"
2026-05-06,KSBP,dividend_or_bonus,Credit of Final Cash Dividend
2026-05-06,GLAXO,dividend_or_bonus,Credit of Final Cash Dividend
2026-05-06,CEPB,insider_trade,Insider trade disclosure
2026-05-06,SGPL,insider_trade,Insider trade disclosure
2026-05-06,WAVES,insider_trade,Insider trade disclosure
2026-05-07,MTL,material_info,Material Information
2026-05-07,AVN,material_info,Material Information
2026-05-07,TELE,financial_result,Transmission of Quarterly Report for the Period Ended 31 March 2026
2026-05-07,HALEON,dividend_or_bonus,Prior Publication of Notice of Credit of Final Cash Dividend
2026-05-07,EPCL,insider_trade,Insider trade disclosure
2026-05-07,KEL,insider_trade,Insider trade disclosure
2026-05-08,CLOV,material_info,Disclosure Of Material Information
2026-05-08,AIRLINK,financial_result,Shariah Disclosure for the Half Year Ended 31st December 2025
2026-05-08,FCEPL,dividend_or_bonus,Credit of Final Cash Dividend
2026-05-08,SGF,dividend_or_bonus,Credit of Final Cash Dividend
2026-05-08,HALEON,dividend_or_bonus,Credit of Final Cash Dividend
2026-05-08,SGF,insider_trade,Insider trade disclosure
2026-05-08,SGPL,insider_trade,Insider trade disclosure
2026-05-08,TBL,insider_trade,Insider trade disclosure
2026-05-08,FATIMA,insider_trade,Insider trade disclosure
2026-05-08,MEBL,insider_trade,Insider trade disclosure

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-4.5,2026-05-07
investor_type,last_5_sessions,broker proprietary trading,9.931,2026-05-07
investor_type,last_5_sessions,companies,-0.288,2026-05-07
investor_type,last_5_sessions,foreign corporates,-1.806,2026-05-07
investor_type,last_5_sessions,foreign individual,0.002,2026-05-07
investor_type,last_5_sessions,individuals,-1.229,2026-05-07
investor_type,last_5_sessions,insurance companies,-10.265,2026-05-07
investor_type,last_5_sessions,mutual funds,3.005,2026-05-07
investor_type,last_5_sessions,nbfc,0.281,2026-05-07
investor_type,last_5_sessions,other organization,2.478,2026-05-07
investor_type,last_5_sessions,overseas pakistani,2.389,2026-05-07
sector,last_5_sessions,fipi | Commercial Banks,-2.114,2026-05-07
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,3.573,2026-05-07
sector,last_5_sessions,lipi banks / dfi | Debt Market,-2.805,2026-05-07
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,3.705,2026-05-07
sector,last_5_sessions,lipi companies | All other Sectors,3.231,2026-05-07
sector,last_5_sessions,lipi companies | Debt Market,-2.754,2026-05-07
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,2.405,2026-05-07
sector,last_5_sessions,lipi insurance companies | All other Sectors,-7.222,2026-05-07
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-2.345,2026-05-07
sector,last_5_sessions,lipi mutual funds | All other Sectors,4.413,2026-05-07
sector,last_5_sessions,lipi mutual funds | Debt Market,3.445,2026-05-07
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-2.358,2026-05-07
investor_type,last_20_sessions,banks / dfi,-23.314,2026-05-07
investor_type,last_20_sessions,broker proprietary trading,4.833,2026-05-07
investor_type,last_20_sessions,companies,7.244,2026-05-07
investor_type,last_20_sessions,foreign corporates,-10.072,2026-05-07
investor_type,last_20_sessions,foreign individual,0.055,2026-05-07
investor_type,last_20_sessions,individuals,40.882,2026-05-07
investor_type,last_20_sessions,insurance companies,-38.844,2026-05-07
investor_type,last_20_sessions,mutual funds,10.239,2026-05-07
investor_type,last_20_sessions,nbfc,0.746,2026-05-07
investor_type,last_20_sessions,other organization,-6.174,2026-05-07
investor_type,last_20_sessions,overseas pakistani,14.404,2026-05-07
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-7.705,2026-05-07
sector,last_20_sessions,lipi banks / dfi | Debt Market,8.638,2026-05-07
sector,last_20_sessions,lipi companies | Commercial Banks,8.624,2026-05-07
sector,last_20_sessions,lipi individuals | All other Sectors,13.092,2026-05-07
sector,last_20_sessions,lipi individuals | Commercial Banks,18.771,2026-05-07
sector,last_20_sessions,lipi individuals | Fertilizer,8.406,2026-05-07
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,-8.512,2026-05-07
sector,last_20_sessions,lipi insurance companies | All other Sectors,-19.696,2026-05-07
sector,last_20_sessions,lipi insurance companies | Commercial Banks,-11.251,2026-05-07
sector,last_20_sessions,lipi mutual funds | Cement,7.342,2026-05-07
sector,last_20_sessions,lipi mutual funds | Debt Market,-7.672,2026-05-07
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,11.248,2026-05-07

=== FILE: calendar.md ===
# Calendar as of 2026-05-08

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2026-04-09 SGPL: Board Meeting Other Than Financial Results
- 2026-04-10 PSO: Board Meeting Other Than Financial Results
- 2026-04-10 SPEL: Board Meeting
- 2026-04-10 MEBL: NOTICE OF BOARD MEETING AND CLOSED PERIOD - MEEZAN BANK LIMITED
- 2026-04-10 SAZEW: Board Meeting
- 2026-04-10 EPCL: Board Meeting - Q1 2026 - Engro Polymer & Chemicals Limited
- 2026-04-10 GHNI: Board Meeting
- 2026-04-10 LOTCHEM: Board Meeting
- 2026-04-10 ISL: Board Meeting
- 2026-04-10 GAL: Board Meeting
- 2026-04-10 CRTM: Board Meeting Other Than Financial Results
- 2026-04-13 PRL: Board Meeting
- 2026-04-13 POWER: Board Meeting
- 2026-04-13 FABL: Board of Directors Meeting of Faysal Bank Limited
- 2026-04-13 PIOC: Board Meeting
- 2026-04-14 PIBTL: Board Meeting -PIBTL
- 2026-04-14 KSBP: Board Meeting
- 2026-04-14 TPLT: Board Meeting
- 2026-04-14 MLCF: MLCF-Notice of Board Meeting 21.04.2026
- 2026-04-14 HUBC: Board Meeting for the Third Quarter Ended March 31, 2026 - The Hub Power Company Limited
- 2026-04-14 CSAP: Notice of 204th Board Meeting for the Third Quarter Ended March 31, 2026
- 2026-04-15 LOADS: Board Meeting of Loads Limited
- 2026-04-15 KTML: KTML Notice of Board Meeting 22.04.2026
- 2026-04-15 KEL: Board Meeting Other Than Financial Results
- 2026-04-16 MARI: Notice of Board of Directors Meeting
- 2026-04-16 FCEPL: Board Meeting 1st Quarter 2026
- 2026-04-16 BIFO: Meeting of the Board of Directors
- 2026-04-16 ENGROH: Board Meeting for the Announcement of Financial Results for the Three Months Ended March 31, 2026
- 2026-04-16 KOHC: Board Meeting
- 2026-04-16 SGPL: Board Meeting Material Information
- 2026-04-16 FATIMA: Board meeting and closed period
- 2026-04-17 SAZEW: Board Meeting Rescheduled
- 2026-04-17 GWLC: Board Meeting
- 2026-04-17 LCI: Board Meeting / Closed Period
- 2026-04-17 BIPL: Board Meeting - BankIslami Pakistan Limited
- 2026-04-17 BBFL: Board Meeting
- 2026-04-17 CHCC: Board Meeting
- 2026-04-20 DCL: Board Meeting
- 2026-04-20 GLAXO: Board Meeting Quarter 1- 2026
- 2026-04-20 ITTEFAQ: BOARD MEETING
- 2026-04-20 BFBIO: Board Meeting
- 2026-04-20 ICL: Board Meeting
- 2026-04-20 CNERGY: Board Meeting and Closed Period
- 2026-04-20 BFAGRO: Board Meeting
- 2026-04-20 ABOT: Board Meeting
- 2026-04-20 ZAL: Board Meeting
- 2026-04-20 FCL: Notice of Board Meeting/closed period of FCL
- 2026-04-20 OGDC: Board Meeting and Closed Period
- 2026-04-20 GCWL: Meeting of the Board of Directors - GHANI CHEMWORLD LIMITED
- 2026-04-20 GCIL: Meeting of the Board of Directors - GHANI CHEMICAL INDUSTRIES LIMITED
- 2026-04-20 PPL: Meeting of the Board of Directors and Closed Period
- 2026-04-20 GGL: Meeting of the Board of Directors - GHANI GLOBAL HOLDINGS LIMITED
- 2026-04-20 FFL: Board Meeting
- 2026-04-20 FECTC: Board Meeting for the Quarter Ended March 31, 2026 & Annoucement of Closed Period
- 2026-04-20 HTL: Board Meeting
- 2026-04-20 ASL: BOARD MEETING / CLOSED PERIOD
- 2026-04-21 PREMA: Board Meeting
- 2026-04-21 QUICE: BOARD MEETING
- 2026-04-21 MACFL: Board meeting
- 2026-04-21 HALEON: Notice of Board of Directors Meeting - (Q1-2026)
- 2026-04-21 SSOM: Board Meeting
- 2026-04-21 IBLHL: Board Meeting
- 2026-04-21 TPLP: Board Meeting
- 2026-04-21 SGF: Board Meeting
- 2026-04-21 TGL: Board Meeting
- 2026-04-21 CEPB: BOARD MEETING
- 2026-04-21 SNGP: Board Meeting
- 2026-04-21 TRSM: Board of Directors Meeting for the Quarter ended March 31, 2026.
- 2026-04-21 GHGL: BOARD MEETING
- 2026-04-21 CLOV: Board of Directors Meeting and Closed Period
- 2026-04-21 SYM: Board Meeting
- 2026-04-21 WAFI: Board Meeting
- 2026-04-21 TBL: Notice of Board Meeting Q3 FY 25-26
- 2026-04-21 DGKC: Board Meeting
- 2026-04-21 GTYR: Board Meeting
- 2026-04-21 MTL: BOARD MEETING FOR QUARTERLY RESULTS
- 2026-04-21 TOMCL: Board Meeting
- 2026-04-21 OCTOPUS: Board Meeting
- 2026-04-21 LUCK: Board Meeting
- 2026-04-22 PSO: Board Meeting
- 2026-04-22 MUGHAL: Notice of Board Meeting - QIII - 2026
- 2026-04-22 ILP: Notice of Board Meeting for the Third Quarter ended March 31, 2026 / Closed Period
- 2026-04-22 MARI: Board of Directors Meeting - Change of Place
- 2026-04-22 ANL: Board Meeting
- 2026-04-22 IMAGE: Board Meeting
- 2026-04-22 OBOY: NOTICE OF BOARD MEETING
- 2026-04-22 AGTL: Board Meeting
- 2026-04-22 CRTM: Board Meeting
- 2026-04-22 SSGC: Board Meeting
- 2026-04-22 HINOON: Board Meeting
- 2026-04-22 GDL: Board Meeting
- 2026-04-22 PAEL: Board Meeting for the 1st Quarter ended 31-03-2026 (Un-Audited)
- 2026-04-22 SEARL: Board Meeting
- 2026-04-22 NETSOL: Board Meeting
- 2026-04-22 GATM: BOARD MEETING AND CLOSED PERIOD
- 2026-04-22 TATM: Meeting of the Board of Directors
- 2026-04-22 BECO: Board Meeting
- 2026-04-22 FFC: Board Meeting
- 2026-04-22 FEROZ: Board Meeting
- 2026-04-22 SGPL: BOARD MEETING TO CONSIDER AND APPROVE QUARTERLY FINANCIAL STATEMENTS
- 2026-04-22 AGP: Board Meeting
- 2026-04-22 TREET: Notice of Board Meeting for the Third Quarter ended March 31, 2026 / Closed Period
- 2026-04-22 NML: Board Meeting
- 2026-04-22 AVN: Board Meeting
- 2026-04-22 DCR: BOARD MEETING / CLOSED PERIOD
- 2026-04-23 CPHL: Board Meeting
- 2026-04-23 FFL: Board Meeting Rescheduled
- 2026-04-23 TELE: Board Meeting
- 2026-04-23 BNL: Board Meeting
- 2026-04-23 WAVES: Board Meeting for the Quarter ended 31Mar26
- 2026-04-27 PRL: Board Meeting other than Financial Results
- 2026-04-27 SLGL: Board Meeting
- 2026-04-27 NETSOL: Board Meeting Rescheduled
- 2026-04-27 TATM: Board Meeting Rescheduled
- 2026-04-28 TBL: Board Meeting Rescheduled Q3 FY 25-26
- 2026-04-28 SYM: Board Meeting Rescheduled
- 2026-04-28 GCWL: DECISION OF THE BOARD OF DIRECTORS MEETING - GHANI CHEMWORLD LIMITED
- 2026-04-28 GGL: DECISIONS OF THE BOARD OF DIRECTORS MEETING - GHANI GLOBAL HOLDINGS LIMITED
- 2026-04-28 GCIL: DECISIONS OF THE BOARD OF DIRECTORS MEETING - GHANI CHEMICAL INDUSTRIES LIMITED
- 2026-04-30 WAVES: Board Meeting Rescheduled
- 2026-05-05 FABL: Board of Directors Meeting other than Financial Results
- 2026-05-07 HCAR: Board Meeting & Closed Period
- 2026-05-07 SEARL: SHORT NOTICE (EMERGENT) BOARD MEETING- OTHER THAN FINANCIAL RESULTS
- 2026-05-08 OCTOPUS: Board Meeting

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
**Establishment and SIFC.** The SIFC (created mid-2023, army chief a member, agriculture, mining and IT focus, IMF asked about its powers) was described by a government adviser to mining.com (date not shown). Reuters in 2020 reported the military as the most influential voice on Reko Diq. Establishment-linked capital is visible in listed names: Fauji Foundation owns 44.32% of FFC (FFC H1-26 report), FFC holds 33.99% of the PIA buyer (repo), a Fauji Foundation and KAPCO group bought Attock Cement
| 1 | Brownfield refinery policy | 17 Aug 2023 | outcome not shown |
| 3 | OMC margin +Rs1.22 | OCAC ask Apr 2025 | outcome not shown |
| 6 | Rs1.225tn power bank facility | 2025 | outcome not shown |
| 7 | IPP terminations | 2024 (unverified) | 5 PPAs ended Oct 2024; Rs1tn savings claimed 29 Dec. Y |

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
