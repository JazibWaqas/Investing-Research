# Replay bundle, close of 2026-03-06 (brief v2)

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
# Market as of 2026-03-06 close (public information only)

- KSE100: 157,496 on 2026-03-06; 1m -16.2%, 3m -5.7%, 6m +0.6%, 12m +39.7%
- KMI All Share: 60,839 on 2026-03-06; 1m -16.0%, 3m -7.9%, 6m -5.1%, 12m +26.0%
- Policy rate 10.5%; last MPC decision 2026-01-26: hold (+0bp)
- 6M T-bill cutoff 10.74% (auction 2026-03-04); 3M 10.50%, 12M 10.99%
- CPI YoY 6.99% for 2026-02 (published by 2026-03-03); three months earlier (2025-11) 6.16%
- Brent: 95.74 USD/bbl on 2026-03-06; 3-month change +48.6%
- USD/PKR: 279.59  on 2026-03-06; 3-month change -0.4%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +0.24pp (market near policy rate); CPI rising over 3 months (+0.8pp)
- Next MPC: see SBP calendar

Session date used: 2026-03-06. Liquid KMI names: 127 (membership KMI_ALL_derived_2025-12-02.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.1932,-0.1281,-0.0336,0,0
E&P,3,-0.162,-0.0315,0.0513,0,0
OMC,4,-0.2574,-0.2007,-0.1198,0,0
Power,5,-0.1368,-0.0659,0.1096,0,0
Fertilizer,4,-0.135,0.0055,0.1002,0,0
Cement,16,-0.2222,-0.2221,-0.0973,0,0
Steel & engineering,11,-0.2267,-0.1663,-0.1687,0,0
Autos,12,-0.2224,-0.1967,-0.2079,0,0
Tech & telecom,11,-0.264,-0.2613,-0.1342,0,0
Islamic banks & fin.,9,-0.1842,-0.23,-0.152,0,0
Pharma,14,-0.2057,-0.144,-0.1582,0,0
Textiles,23,-0.2147,-0.1798,-0.2358,1,1
Food & staples,15,-0.2273,-0.144,-0.1191,0,0
Chemicals,19,-0.1755,-0.1777,-0.0608,0,0
"Glass, packaging, paper",13,-0.2355,-0.1598,-0.2419,0,0
Gas utilities & misc,13,-0.2259,-0.1782,-0.1263,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ACPL,268.79,-0.055,-0.073,-0.027,0.15,-0.141,0.746,0,2025-06-30,-0.687,2,2,0,0,23.229,0.027
AGP,191.04,-0.112,-0.001,0.009,0.02,-0.215,2.508,0,2025-09-30,0.333,0,0,0,0,17.84,0.024
AIRLINK,152.51,-0.177,-0.123,0.007,-0.1,-0.205,0.27,0,2025-12-31,-0.005,2,0,0,0,12.707,0.046
ANL,9.01,-0.236,-0.207,-0.258,0.161,-0.315,0.819,0,,,2,0,0,0,,
ASL,10.09,-0.277,-0.216,-0.283,-0.024,-0.347,0.472,0,2025-12-31,,2,0,0,0,,
ATRL,788.77,-0.099,0.196,0.21,0.293,-0.108,0.763,1,2025-12-31,0.032,2,1,0,0,8.095,0.015
BBFL,39.68,-0.187,-0.255,-0.171,-0.142,-0.293,0.424,0,,,2,0,0,0,,
BECO,4.83,-0.167,-0.284,-0.777,-0.447,-0.932,0.644,0,2025-09-30,-0.901,2,2,0,0,20.344,
BERG,89.51,-0.175,-0.101,-0.185,-0.044,-0.258,0.613,0,2025-12-31,0.173,3,0,0,0,9.087,0.045
BFAGRO,33.46,-0.188,-0.185,-0.244,,-0.303,0.613,0,,,2,0,0,0,,
BFBIO,138.86,-0.18,-0.088,-0.162,-0.2,-0.266,0.899,0,2025-12-31,0.954,2,0,0,0,33.326,
BIFO,120.54,-0.191,-0.156,-0.225,-0.174,-0.281,0.544,0,2025-12-31,1.653,2,0,0,0,,
BIPL,25.93,-0.22,-0.19,-0.303,0.246,-0.395,0.436,0,2025-12-31,-0.44,2,0,0,0,,
BNL,8.67,-0.231,-0.933,-0.93,-0.401,-0.946,0.417,1,2025-06-30,,2,0,0,0,,
BWHL,186.81,-0.09,0.062,0.05,0.493,-0.192,0.912,0,,,2,0,0,0,,
CEPB,30.5,-0.274,-0.016,0.118,0.168,-0.322,0.36,0,2025-12-31,-6.462,2,0,0,0,,
CHCC,259.03,-0.209,-0.226,-0.281,0.03,-0.294,0.868,0,2025-12-31,-0.113,2,0,0,0,6.497,0.019
CLOV,56.2,-0.275,0.428,0.303,0.286,-0.303,1.763,0,2025-12-31,-0.059,1,1,0,0,,
CNERGY,6.7,-0.126,-0.148,-0.063,-0.102,-0.261,1.115,0,2024-06-30,,2,1,0,0,,
CPHL,77.93,-0.127,-0.131,-0.153,-0.129,-0.204,0.899,0,2025-12-31,0.58,2,2,0,0,21.506,0.042
CSAP,88.3,-0.333,-0.074,-0.117,-0.109,-0.352,0.787,0,2025-09-30,0.694,1,0,0,0,,0.065
DCL,7.38,-0.398,-0.419,-0.487,-0.169,-0.535,0.342,0,,,2,0,0,0,,
DCR,36.71,-0.064,0.108,0.186,0.662,-0.077,1.125,0,2025-12-31,-0.578,2,0,0,0,7.515,0.083
DGKC,183.34,-0.193,-0.217,-0.23,0.55,-0.319,0.79,0,2025-12-31,0.314,2,0,0,0,7.851,0.012
DOL,32.52,-0.008,-0.049,-0.104,0.437,-0.124,0.558,0,,,2,0,0,0,,
ECOP,42.39,-0.255,-0.269,-0.304,0.815,-0.52,0.374,0,2025-12-31,-1.411,1,0,0,0,9.418,0.03
EFERT,211.6,-0.111,-0.03,0.007,0.032,-0.17,1.0,0,2025-12-31,-0.186,3,0,0,0,9.648,0.105
ENGROH,255.31,-0.078,0.184,0.029,0.422,-0.143,1.345,0,2025-12-31,-0.166,1,1,0,0,9.7,0.04
EPCL,32.43,0.035,0.024,0.073,-0.128,-0.181,1.7,0,2025-12-31,-1.288,1,1,0,0,,
EPQL,24.91,-0.218,-0.194,-0.143,0.348,-0.277,3.55,0,2025-12-31,,1,0,0,0,,
FABL,84.26,-0.149,-0.072,0.11,0.858,-0.19,0.611,0,2025-12-31,0.953,2,0,0,0,3.08,0.144
FATIMA,140.94,-0.248,-0.077,0.13,0.83,-0.248,0.971,0,2025-09-30,0.301,0,0,0,0,4.517,0.089
FCCL,43.84,-0.235,-0.198,-0.233,0.12,-0.282,0.599,0,2025-12-31,0.0,2,4,0,0,8.222,0.028
FCEPL,70.95,-0.207,-0.158,-0.186,-0.141,-0.352,0.489,0,2024-09-30,2.03,1,0,0,0,31.055,0.031
FCL,21.68,-0.176,-0.083,-0.062,-0.09,-0.218,0.438,0,2025-12-31,-0.163,3,1,0,0,12.305,0.021
FECTC,101.63,-0.341,-0.329,0.088,0.08,-0.466,0.411,0,2025-12-31,0.979,2,0,0,0,,
FEROZ,333.29,-0.259,-0.12,-0.19,0.056,-0.267,0.842,0,,,2,0,0,0,,
FFC,522.29,-0.1,-0.065,0.184,0.5,-0.212,0.648,0,2025-12-31,-0.021,1,0,0,0,5.523,0.112
FFL,15.75,-0.274,-0.146,-0.156,0.074,-0.32,0.413,0,2025-12-31,1.0,1,0,0,0,68.835,
FLYNG,47.34,-0.098,-0.139,-0.092,0.679,-0.211,0.644,0,,,2,0,0,0,,
GAL,398.02,-0.241,-0.286,-0.3,-0.078,-0.348,1.098,0,2025-12-31,1.662,2,0,0,0,5.252,0.026
GATM,19.0,-0.376,-0.312,-0.5,-0.186,-0.525,0.696,0,2025-12-31,-1.376,2,0,0,0,4.564,
GCIL,28.86,-0.149,-0.171,-0.097,0.611,-0.25,0.617,1,,,2,0,0,0,,
GCWL,18.0,-0.263,-0.086,0.188,,-0.263,0.549,0,,,3,0,0,0,,
GGGL,7.7,-0.285,-0.268,-0.396,-0.183,-0.429,0.859,0,,,2,0,0,0,,
GGL,16.65,-0.314,-0.359,-0.376,0.169,-0.431,0.98,0,2025-12-31,0.321,2,0,0,0,2.013,
GHGL,30.87,-0.176,-0.12,-0.323,0.027,-0.365,0.406,0,2025-12-31,-0.066,2,0,0,0,,
GHNI,759.73,-0.212,-0.09,-0.043,0.162,-0.248,1.076,0,2025-12-31,0.778,2,0,0,0,6.046,0.015
GLAXO,325.66,-0.238,-0.174,-0.198,-0.157,-0.294,0.716,0,2025-09-30,0.058,0,0,0,0,19.339,0.025
GTYR,24.15,-0.4,-0.35,-0.421,-0.382,-0.514,0.93,0,2025-12-31,-53.333,2,1,0,0,,
GWLC,46.32,-0.24,-0.278,-0.152,0.204,-0.389,0.194,0,2025-12-31,2.762,2,0,0,0,,
HALEON,776.84,-0.166,-0.068,-0.102,0.009,-0.214,0.65,0,2025-12-31,0.3,1,0,0,0,20.65,0.025
HCAR,169.3,-0.315,-0.394,-0.433,-0.385,-0.456,0.469,0,2025-12-31,0.156,0,0,0,0,15.254,0.028
HTL,37.84,-0.351,-0.302,-0.235,-0.075,-0.4,0.296,0,,,3,0,0,0,,
HUBC,207.33,-0.095,-0.05,0.161,0.759,-0.13,0.667,0,2025-12-31,1.592,6,0,0,0,3.875,0.109
IBLHL,40.46,-0.331,-0.304,-0.23,0.236,-0.496,0.129,0,,,2,0,0,0,,
ICL,128.55,-0.16,-0.213,0.053,0.853,-0.228,0.254,0,,,2,0,0,0,,
ILP,76.1,-0.149,0.015,0.116,0.317,-0.179,0.869,0,2025-12-31,1.842,2,0,0,0,17.114,0.015
IMAGE,21.56,-0.146,-0.12,-0.232,0.08,-0.384,0.361,0,2025-12-31,0.293,2,0,0,0,,
INIL,141.44,-0.192,-0.232,-0.359,-0.072,-0.402,1.031,0,2025-12-31,4.885,1,0,0,0,25.968,0.023
IPAK,24.83,-0.227,-0.004,0.094,0.184,-0.227,0.43,0,2025-09-30,2.303,4,0,0,0,13.394,0.027
ISL,75.78,-0.269,-0.194,-0.362,-0.014,-0.396,0.34,0,2025-12-31,1.793,1,0,0,0,25.861,0.027
ITTEFAQ,6.72,-0.304,-0.262,-0.34,-0.08,-0.446,0.303,0,,,3,0,0,0,,
JVDC,102.9,-0.323,0.354,0.288,0.915,-0.358,0.868,0,2025-12-31,3.976,2,0,0,0,14.977,0.078
KEL,7.81,-0.06,0.441,0.358,0.767,-0.171,0.859,0,2024-06-30,-0.871,1,2,0,0,30.127,
KOHC,83.71,-0.23,-0.192,-0.182,0.037,-0.316,0.524,0,2025-12-31,-0.199,2,0,0,0,6.026,
KSBP,192.74,0.021,-0.093,-0.154,0.304,-0.265,0.472,1,2025-09-30,2.115,0,0,0,0,,
KTML,48.92,-0.243,-0.249,-0.031,0.435,-0.334,0.179,0,2024-12-31,1.398,2,0,0,0,3.207,0.01
LCI,223.52,-0.178,-0.231,-0.236,-0.069,-0.4,0.59,0,2025-12-31,-0.346,1,0,0,0,12.485,0.041
LIVEN,32.68,-0.357,-0.383,-0.487,-0.664,-0.681,1.113,0,,,2,0,0,0,,
LOADS,12.54,-0.276,-0.303,-0.261,-0.299,-0.395,0.228,0,2025-12-31,0.044,2,0,0,0,13.777,
LOTCHEM,20.45,-0.183,-0.071,0.056,0.268,-0.273,0.456,0,2025-12-31,,1,0,0,0,11.982,0.239
LUCK,383.04,-0.196,-0.195,-0.197,0.352,-0.253,1.791,0,2025-12-31,0.055,1,0,0,0,6.763,0.011
MACFL,21.78,-0.331,-0.118,-0.279,0.45,-0.665,0.562,0,2025-12-31,5.0,2,0,0,0,34.336,0.01
MACTER,281.45,-0.162,-0.168,-0.277,-0.016,-0.547,0.542,0,,,2,0,0,0,,
MARI,617.05,-0.126,-0.114,-0.062,0.163,-0.208,0.746,0,2025-12-31,0.144,1,0,0,0,11.514,0.035
MEBL,444.9,-0.134,0.027,0.112,0.998,-0.134,0.828,0,2025-12-31,-0.143,2,1,0,0,4.229,0.116
MFL,48.16,-0.22,-0.304,-0.037,0.082,-0.398,0.124,0,2025-12-31,0.269,2,1,0,0,14.487,
MLCF,84.26,-0.263,-0.198,-0.213,0.594,-0.354,1.028,0,2024-12-31,0.708,2,2,0,0,7.675,
MTL,500.45,-0.093,0.025,-0.058,-0.12,-0.136,1.177,0,2025-12-31,-0.241,2,0,0,0,17.531,0.107
MUGHAL,71.9,-0.235,-0.144,-0.118,-0.018,-0.349,0.592,0,2025-12-31,1.333,2,0,0,0,28.337,
NETSOL,97.4,-0.224,-0.249,-0.323,-0.249,-0.401,0.788,0,2025-12-31,,3,1,0,0,8.173,
NML,149.05,-0.245,-0.012,-0.045,0.518,-0.273,0.641,0,2025-12-31,,3,0,0,0,8.671,0.016
NRL,303.26,-0.325,-0.302,-0.189,0.291,-0.346,0.629,0,2025-12-31,,2,0,0,0,,
OBOY,8.85,-0.354,-0.052,-0.02,-0.046,-0.41,0.379,0,,,2,0,0,0,,
OGDC,275.79,-0.148,0.02,0.06,0.405,-0.161,1.111,0,2025-12-31,-0.162,2,0,0,0,5.583,0.068
PAEL,39.98,-0.302,-0.246,-0.281,-0.045,-0.366,0.504,0,2025-09-30,0.542,0,0,0,0,16.997,
PIBTL,14.63,-0.293,-0.039,0.118,0.604,-0.352,0.569,0,2025-12-31,0.238,2,0,0,0,,
PIOC,240.08,-0.302,-0.379,-0.075,0.234,-0.43,0.298,0,2025-12-31,-0.086,3,0,0,0,10.627,0.044
POWER,16.34,-0.241,-0.11,-0.142,0.46,-0.244,0.664,0,2025-12-31,0.568,2,0,0,0,31.257,
PPL,214.75,-0.212,-0.003,0.153,0.309,-0.23,1.088,0,2025-12-31,-0.262,2,0,0,0,5.148,0.044
PREMA,27.59,-0.343,-0.299,-0.337,0.039,-0.682,0.72,0,2025-12-31,0.444,2,1,0,0,16.658,
PRL,28.46,-0.252,-0.245,-0.12,-0.168,-0.29,0.474,0,2025-12-31,2.296,1,0,0,0,,
PSO,383.97,-0.207,-0.174,-0.058,0.175,-0.237,0.567,0,2025-12-31,-0.336,2,0,0,0,10.778,0.026
QUICE,23.46,-0.295,1.456,1.651,2.465,-0.44,0.372,1,,,2,0,0,0,,
SAZEW,2132.19,-0.055,0.245,0.339,1.096,-0.132,1.138,0,2025-12-31,0.671,0,0,0,0,4.217,0.046
SEARL,84.86,-0.325,-0.199,-0.16,0.046,-0.372,0.609,0,2025-12-31,,2,0,0,0,,
SGF,98.73,-0.245,-0.162,0.057,0.092,-0.25,0.202,0,2025-09-30,0.356,0,1,0,0,,
SGPL,14.7,-0.483,-0.353,0.235,0.746,-0.608,0.391,0,2025-12-31,,2,0,0,0,,
SHFA,471.25,-0.191,-0.107,-0.145,0.061,-0.219,0.489,0,,,2,0,0,0,,
SNGP,95.89,-0.144,-0.177,-0.252,0.08,-0.299,1.107,0,2025-12-31,-0.166,2,0,0,0,5.073,0.026
SPEL,39.71,-0.278,-0.273,-0.422,0.053,-0.484,0.435,0,2025-12-31,0.172,2,0,0,0,,
SSGC,24.23,-0.284,-0.393,-0.418,-0.247,-0.472,0.593,1,2025-12-31,-0.725,2,0,0,0,10.954,0.012
SSOM,507.63,0.196,0.148,-0.226,4.86,-0.521,2.069,2,,,2,0,0,0,,
SYM,10.01,-0.288,-0.231,-0.358,-0.354,-0.373,0.786,0,2025-12-31,0.636,2,2,0,0,,
SYS,117.75,-0.267,-0.232,-0.142,0.099,-0.313,1.055,0,2025-09-30,0.267,0,0,0,0,24.356,0.01
TATM,105.97,-0.364,-0.387,-0.445,1.417,-0.64,0.164,0,2025-12-31,-0.944,2,0,0,0,6.525,
TBL,9.0,-0.274,-0.251,-0.296,-0.359,-0.389,0.333,0,,,2,0,0,0,,
TELE,7.17,-0.402,-0.408,-0.109,-0.102,-0.459,0.362,0,2025-12-31,-0.75,1,1,0,0,18.478,
TGL,145.93,-0.3,-0.258,-0.441,-0.174,-0.476,0.816,0,2025-12-31,-0.386,2,0,0,0,9.051,0.016
TOMCL,33.2,-0.359,-0.346,-0.322,0.175,-0.499,0.295,0,2025-12-31,-0.04,2,0,0,0,13.655,
TPLP,7.3,-0.399,-0.307,-0.297,-0.338,-0.435,0.503,0,,,2,0,0,0,,
TPLT,9.54,-0.277,0.381,0.247,0.359,-0.394,0.481,0,,,2,0,0,0,,
TREET,22.73,-0.33,-0.282,-0.072,0.089,-0.372,0.386,0,2025-12-31,0.111,2,0,0,0,17.461,
TRSM,9.08,-0.429,-0.751,-0.811,1.281,-0.867,0.393,1,2025-12-31,-0.345,2,0,0,0,,
WAFI,190.65,-0.228,-0.057,0.132,0.087,-0.235,0.431,0,2025-12-31,-0.801,1,2,0,0,13.796,0.024
ZAL,41.95,-0.391,-0.153,0.469,1.695,-0.42,0.617,0,2025-12-31,2.354,2,0,0,0,6.31,0.062

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2026-03-02,NRL,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2025"
2026-03-02,ANL,financial_result,Transmission of Quarterly Financial Statements for the Period Ended Decembe
2026-03-02,JVDC,financial_result,Transmission of Half Yearly financial statements for the period ended 31 De
2026-03-02,TOMCL,financial_result,Transmission of Quarterly Report for the Period Ended 31-12-2025
2026-03-02,KOHC,financial_result,Transmission of Quarterly Financial Statements for the Period Ended 31-12-2
2026-03-02,SSGC,financial_result,Transmission of Quarterly Report for the Period Ended 31 December 2025
2026-03-02,ZAL,financial_result,"Transmission of Quarterly Report for the Period Ended December 31, 2025"
2026-03-02,OBOY,financial_result,"Financial Results for the Half Year and Quarter Ended December 31, 2025"
2026-03-03,CPHL,material_info,Material Information
2026-03-03,HALEON,financial_result,Financial Results for the Year Ended 31 December 2025
2026-03-03,TELE,financial_result,Financial Results for the Half Year Ended 31 December 2025
2026-03-03,LOTCHEM,financial_result,Financial Results for the year ended 31 December 2025
2026-03-03,CSAP,dividend_or_bonus,"Credit of Interim Cash Dividend for the year ending June 30, 2026"
2026-03-03,KOHC,insider_trade,Insider trade disclosure
2026-03-04,EPQL,financial_result,"Transmission of Annual Report for the Year Ended December 31, 2025"
2026-03-04,FCL,financial_result,"Annual IPO Progress report of FCL June 30, 2025"
2026-03-04,OBOY,financial_result,"Financial Results for the Half Year Ended December 31, 2025"
2026-03-04,EFERT,financial_result,"Transmission of Annual Report for the Year Ended December 31, 2025"
2026-03-04,KOHC,insider_trade,Insider trade disclosure
2026-03-04,NETSOL,insider_trade,Insider trade disclosure
2026-03-04,SHFA,insider_trade,Insider trade disclosure
2026-03-04,CEPB,insider_trade,Insider trade disclosure
2026-03-05,FABL,financial_result,"Transmission of Annual Report for the year ended December 31, 2025 of Faysa"
2026-03-05,MEBL,financial_result,"Transmission of Annual Report for the Year Ended December 31, 2025 - Meezan"
2026-03-05,BIPL,dividend_or_bonus,BankIslami Pakistan Limited - Draft Notice of 22nd Annual General Meeting a
2026-03-05,NETSOL,insider_trade,Insider trade disclosure
2026-03-05,SHFA,insider_trade,Insider trade disclosure
2026-03-05,CEPB,insider_trade,Insider trade disclosure
2026-03-05,IPAK,insider_trade,Insider trade disclosure
2026-03-05,TPLP,insider_trade,Insider trade disclosure
2026-03-06,GTYR,material_info,Material Information
2026-03-06,NETSOL,material_info,Material Information
2026-03-06,BIPL,financial_result,"Transmission of Annual Report for the Year Ended December 31, 2025"
2026-03-06,ILP,insider_trade,Insider trade disclosure
2026-03-06,SHFA,insider_trade,Insider trade disclosure
2026-03-06,GWLC,insider_trade,Insider trade disclosure
2026-03-06,ENGROH,insider_trade,Insider trade disclosure
2026-03-06,TPLP,insider_trade,Insider trade disclosure
2026-03-06,TPLP,insider_trade,Insider trade disclosure
2026-03-06,BNL,insider_trade,Insider trade disclosure

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,50.765,2026-03-05
investor_type,last_5_sessions,broker proprietary trading,1.858,2026-03-05
investor_type,last_5_sessions,companies,10.274,2026-03-05
investor_type,last_5_sessions,foreign corporates,-30.811,2026-03-05
investor_type,last_5_sessions,foreign individual,0.006,2026-03-05
investor_type,last_5_sessions,individuals,-6.497,2026-03-05
investor_type,last_5_sessions,insurance companies,15.515,2026-03-05
investor_type,last_5_sessions,mutual funds,-55.0,2026-03-05
investor_type,last_5_sessions,nbfc,-0.184,2026-03-05
investor_type,last_5_sessions,other organization,8.719,2026-03-05
investor_type,last_5_sessions,overseas pakistani,5.356,2026-03-05
sector,last_5_sessions,fipi | Cement,-13.568,2026-03-05
sector,last_5_sessions,fipi | Commercial Banks,-7.562,2026-03-05
sector,last_5_sessions,lipi banks / dfi | Cement,9.299,2026-03-05
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,14.407,2026-03-05
sector,last_5_sessions,lipi banks / dfi | Fertilizer,6.796,2026-03-05
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,6.157,2026-03-05
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,6.526,2026-03-05
sector,last_5_sessions,lipi mutual funds | Cement,-5.274,2026-03-05
sector,last_5_sessions,lipi mutual funds | Commercial Banks,-10.8,2026-03-05
sector,last_5_sessions,lipi mutual funds | Fertilizer,-10.44,2026-03-05
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-13.479,2026-03-05
sector,last_5_sessions,lipi other organization | Commercial Banks,5.756,2026-03-05
investor_type,last_20_sessions,banks / dfi,106.247,2026-03-05
investor_type,last_20_sessions,broker proprietary trading,-19.818,2026-03-05
investor_type,last_20_sessions,companies,230.316,2026-03-05
investor_type,last_20_sessions,foreign corporates,-302.84,2026-03-05
investor_type,last_20_sessions,foreign individual,-0.158,2026-03-05
investor_type,last_20_sessions,individuals,21.114,2026-03-05
investor_type,last_20_sessions,insurance companies,4.479,2026-03-05
investor_type,last_20_sessions,mutual funds,-62.27,2026-03-05
investor_type,last_20_sessions,nbfc,0.274,2026-03-05
investor_type,last_20_sessions,other organization,14.828,2026-03-05
investor_type,last_20_sessions,overseas pakistani,7.828,2026-03-05
sector,last_20_sessions,fipi | Cement,-237.657,2026-03-05
sector,last_20_sessions,fipi | Technology and Communication,-13.796,2026-03-05
sector,last_20_sessions,lipi banks / dfi | Cement,15.982,2026-03-05
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,19.171,2026-03-05
sector,last_20_sessions,lipi banks / dfi | Debt Market,27.781,2026-03-05
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,16.737,2026-03-05
sector,last_20_sessions,lipi companies | Cement,203.554,2026-03-05
sector,last_20_sessions,lipi companies | Commercial Banks,13.949,2026-03-05
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-16.194,2026-03-05
sector,last_20_sessions,lipi mutual funds | Debt Market,-30.32,2026-03-05
sector,last_20_sessions,lipi mutual funds | Fertilizer,-16.537,2026-03-05
sector,last_20_sessions,lipi other organization | Commercial Banks,14.424,2026-03-05

=== FILE: calendar.md ===
# Calendar as of 2026-03-06

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

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
- 2026-02-19 SSOM: Board Meeting
- 2026-02-19 GGL: Meeting of the Board of Directors - GHANI GLOBAL HOLDINGS LIMITED
- 2026-02-19 GCWL: Meeting of the Board of Directors - GHANI CHEMWORLD LIMITED
- 2026-02-19 SEARL: Board Meeting
- 2026-02-19 TREET: Treet Corporation Limited - Notice of Board Meeting/ Closed Period
- 2026-02-20 SYM: Board Meeting
- 2026-02-20 OBOY: NOTICE OF BOARD MEETING
- 2026-02-20 MUGHAL: Notice of Board Meeting - HY 2026
- 2026-02-20 NML: Board Meeting
- 2026-02-20 SGPL: Board Meeting
- 2026-02-20 GWLC: Board Meeting
- 2026-02-20 ANL: Board Meeting
- 2026-02-20 BECO: Board Meeting
- 2026-02-20 TELE: Board Meeting to Review Half Yearly Accounts
- 2026-02-20 BNL: Board Meeting
- 2026-02-23 HALEON: Notice of Board of Directors Meeting - (Q4-2025)
- 2026-02-23 LOTCHEM: Board Meeting / Closed Period
- 2026-02-25 ZAL: Board Meeting In Process
- 2026-02-26 ITTEFAQ: BOARD MEETING IS PROGRESS
- 2026-02-27 FATIMA: Board meeting and closed period
- 2026-03-05 PRL: Board Meeting other than Financial Results
- 2026-03-06 HCAR: Board Meeting Other Than Financial Results REVOKED
- 2026-03-06 HCAR: Board Meeting Other than Financial Results
- 2026-03-06 GCWL: MEETING OF THE BOARD OF DIRECTORS OTHER THAN FINANCIAL RESULTS - GHANI CHEMWORLD LIMITED
- 2026-03-06 PAEL: Board Meeting for the Year ended 31-12-2025

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
