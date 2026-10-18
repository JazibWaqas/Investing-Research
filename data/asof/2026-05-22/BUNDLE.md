# Replay bundle, close of 2026-05-22 (brief v2)

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
# Market as of 2026-05-22 close (public information only)

- KSE100: 167,844 on 2026-05-22; 1m -2.2%, 3m -2.5%, 6m +3.0%, 12m +40.9%
- KMI All Share: 65,769 on 2026-05-22; 1m -0.7%, 3m -0.3%, 6m +2.1%, 12m +28.3%
- Policy rate 11.5%; last MPC decision 2026-04-27: hike (+100bp)
- 6M T-bill cutoff 12.50% (auction 2026-05-20); 3M 12.49%, 12M 12.59%
- CPI YoY 10.91% for 2026-04 (published by 2026-05-03); three months earlier (2026-01) 5.79%
- Brent: 106.90 USD/bbl on 2026-05-22; 3-month change +46.9%
- USD/PKR: 278.75  on 2026-05-22; 3-month change -0.4%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +1.00pp (market pricing hikes); CPI rising over 3 months (+5.1pp)
- Next MPC: see SBP calendar

Session date used: 2026-05-22. Liquid KMI names: 116 (membership KMI_ALL_derived_2025-12-02.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.0298,0.1694,0.0558,0,0
E&P,3,-0.0002,0.0712,0.1229,0,0
OMC,4,0.145,0.1348,0.1062,0,0
Power,6,0.1064,0.0392,0.1357,0,0
Fertilizer,4,-0.0272,-0.0495,0.0526,0,0
Cement,16,-0.0072,-0.096,-0.1698,0,0
Steel & engineering,11,-0.0082,-0.0415,-0.0612,0,0
Autos,12,0.0057,-0.0422,-0.0784,0,0
Tech & telecom,12,-0.0337,-0.0349,-0.0932,0,0
Islamic banks & fin.,10,-0.027,0.0157,-0.1557,0,0
Pharma,14,-0.071,-0.1182,-0.135,0,0
Textiles,23,0.0112,0.1338,0.0492,1,1
Food & staples,15,0.0169,-0.0107,-0.0317,0,0
Chemicals,19,0.0065,0.0179,-0.0303,0,1
"Glass, packaging, paper",14,0.0628,0.0242,-0.0304,0,0
Gas utilities & misc,13,-0.012,-0.0806,-0.112,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
ABOT,871.15,-0.078,-0.204,-0.157,-0.061,-0.301,1.794,0,2026-03-31,0.213,2,0,0,0,,
ACPL,228.67,-0.041,-0.15,-0.185,-0.224,-0.256,0.704,0,2025-06-30,-0.687,1,3,0,0,23.229,0.027
AGP,188.24,-0.017,-0.08,0.048,0.054,-0.201,1.306,0,2026-03-31,0.007,4,8,0,0,15.229,0.039
AIRLINK,149.85,0.056,-0.067,-0.149,-0.054,-0.219,0.836,0,2026-03-31,0.111,3,0,0,0,12.707,0.046
ASL,12.0,0.034,-0.016,-0.076,0.134,-0.223,0.809,0,2026-03-31,-0.812,3,0,0,0,,
ATRL,889.53,-0.036,0.198,0.314,0.448,-0.086,0.669,0,2026-03-31,,2,1,0,0,8.095,0.015
AVN,34.01,0.085,-0.055,-0.194,-0.291,-0.337,1.416,0,2026-03-31,-0.794,4,1,0,0,,
BBFL,43.34,0.014,-0.036,-0.102,-0.163,-0.227,0.998,0,,,2,1,0,0,,
BECO,5.33,-0.052,-0.063,-0.3,-0.438,-0.925,0.998,0,2026-03-31,1.75,2,0,0,0,20.344,
BFAGRO,32.93,-0.096,-0.157,-0.188,0.144,-0.314,0.89,0,,,3,0,0,0,,
BFBIO,134.97,-0.088,-0.142,-0.114,-0.27,-0.285,0.384,0,2026-03-31,-0.164,2,0,0,0,33.326,
BIFO,134.47,0.172,0.042,-0.068,-0.132,-0.198,3.292,2,2026-03-31,-0.428,2,0,0,0,,
BIPL,25.06,-0.127,-0.116,-0.148,0.355,-0.386,0.851,0,2026-03-31,-0.657,2,0,0,0,,
BNL,7.14,-0.2,-0.286,-0.948,-0.815,-0.955,1.708,0,2025-06-30,,2,0,0,0,,
CEPB,28.03,-0.066,-0.193,-0.173,0.081,-0.377,0.473,0,2026-03-31,,2,0,0,0,,
CHCC,276.5,0.008,-0.072,-0.142,0.05,-0.246,0.699,0,2026-03-31,-0.165,3,0,0,0,6.497,0.019
CLOV,8.36,-0.06,0.224,1.23,1.123,-0.105,3.589,0,2026-03-31,1.333,2,1,0,0,,
CNERGY,8.4,0.021,0.175,0.059,0.102,-0.074,1.874,0,2024-06-30,,2,0,0,0,,
CPHL,77.4,-0.075,-0.082,-0.053,-0.062,-0.21,0.756,0,2026-03-31,0.26,2,2,0,0,21.506,0.042
CRTM,70.88,-0.052,2.54,1.944,3.792,-0.194,0.652,0,,,2,0,0,0,,
CSAP,90.83,-0.027,-0.164,-0.066,-0.24,-0.333,0.415,0,2026-03-31,-1.217,1,0,0,0,,0.065
DCL,9.39,0.022,-0.135,-0.264,-0.085,-0.408,1.665,0,,,2,0,0,0,,
DCR,35.88,-0.005,-0.048,0.148,0.421,-0.082,0.454,0,2026-03-31,0.121,3,0,0,0,7.515,0.083
DGKC,183.64,-0.018,-0.124,-0.174,0.219,-0.318,1.218,0,2026-03-31,0.288,2,0,0,0,7.851,0.012
DOL,32.65,0.108,0.113,0.046,0.1,-0.057,1.751,0,,,2,0,0,0,,
EFERT,201.97,-0.002,-0.026,-0.038,0.189,-0.184,0.489,0,2026-03-31,0.148,2,0,0,0,13.357,0.066
ENGROH,260.13,-0.083,-0.052,0.221,0.469,-0.127,1.083,0,2026-03-31,4.27,2,0,0,0,5.136,
EPCL,33.52,-0.042,-0.009,0.124,0.015,-0.131,0.42,0,2026-03-31,,1,2,0,0,,
EPQL,24.22,0.014,0.068,-0.147,0.017,-0.262,0.565,0,2026-03-31,-0.605,1,0,0,0,,
FABL,87.55,-0.024,-0.01,0.102,0.966,-0.124,0.464,0,2026-03-31,-0.014,4,0,0,0,6.266,0.07
FATIMA,136.39,-0.036,-0.126,0.028,0.633,-0.26,0.426,0,2026-03-31,-0.614,2,0,0,0,7.57,0.04
FCCL,50.29,0.003,-0.044,-0.052,0.106,-0.176,0.807,0,2025-12-31,0.0,3,1,0,0,8.222,0.028
FCEPL,109.29,0.395,0.379,0.349,0.104,-0.05,2.813,1,2024-09-30,2.03,2,0,0,0,24.633,0.04
FCL,23.82,0.07,-0.052,-0.008,0.039,-0.141,0.859,0,2026-03-31,0.086,3,1,0,0,12.305,0.021
FECTC,89.39,-0.095,-0.236,-0.466,0.268,-0.53,0.25,0,2026-03-31,-0.309,2,0,0,0,,
FEROZ,374.18,-0.064,-0.132,-0.062,0.164,-0.177,1.504,0,,,2,0,0,0,,
FFC,531.21,0.014,-0.008,-0.03,0.586,-0.185,0.44,0,2025-12-31,-0.021,2,0,0,0,10.107,0.063
FFL,17.69,0.002,-0.051,-0.056,0.14,-0.236,0.744,0,2026-03-31,-0.077,2,0,0,0,45.156,
GAL,434.51,-0.07,-0.085,-0.218,0.02,-0.288,0.686,0,2026-03-31,0.611,1,0,0,0,5.252,0.026
GATM,22.5,-0.087,-0.124,-0.196,-0.07,-0.437,0.52,0,2026-03-31,-1.131,2,0,0,0,4.564,
GCIL,27.23,-0.113,-0.037,-0.292,0.304,-0.292,0.535,0,,,2,0,0,0,,
GCWL,16.74,-0.051,-0.164,-0.182,0.61,-0.315,0.398,0,,,2,0,0,0,,
GDL,19.92,-0.061,-0.33,,,,0.783,0,2026-03-31,0.031,2,0,0,0,,
GGL,17.23,-0.065,-0.152,-0.386,0.031,-0.411,0.497,0,2026-03-31,0.247,2,0,0,0,2.013,
GHNI,829.3,-0.02,-0.055,0.05,0.277,-0.179,0.805,0,2026-03-31,0.541,2,0,0,0,6.046,0.015
GLAXO,335.3,-0.134,-0.101,-0.119,-0.088,-0.235,0.748,0,2026-03-31,0.228,2,0,0,0,12.382,0.044
GTYR,28.91,0.007,-0.184,-0.235,-0.265,-0.418,0.739,0,2026-03-31,-5.656,2,0,0,0,,
GWLC,47.51,-0.021,-0.078,-0.243,0.127,-0.367,0.709,0,2026-03-31,0.128,2,0,0,0,,
HALEON,761.92,-0.031,-0.131,-0.055,0.053,-0.215,1.068,0,2026-03-31,0.132,2,0,0,0,15.305,0.036
HCAR,222.69,0.215,0.036,-0.22,-0.233,-0.284,2.822,1,2026-03-31,-0.402,1,0,0,0,15.254,0.028
HINOON,949.99,-0.016,0.004,-0.109,0.072,-0.188,0.596,0,2025-12-31,0.458,2,0,0,0,,
HTL,41.35,-0.166,-0.161,-0.197,0.028,-0.345,1.1,0,,,2,0,0,0,,
HUBC,215.42,-0.033,0.029,0.046,0.724,-0.076,0.52,0,2026-03-31,-0.021,3,0,0,0,3.875,0.109
ICL,139.68,-0.087,-0.072,-0.085,0.925,-0.161,0.597,0,,,2,0,0,0,,
ILP,80.32,-0.009,-0.028,0.069,0.394,-0.133,0.683,0,2026-03-31,0.918,3,0,0,0,17.114,0.015
IMAGE,24.14,0.03,0.042,0.049,0.09,-0.31,1.011,0,2026-03-31,-0.033,2,0,0,0,,
INIL,156.76,-0.114,-0.147,-0.161,0.037,-0.338,0.55,0,2026-03-31,-0.172,3,1,0,0,25.968,0.023
IPAK,30.5,0.011,0.052,0.245,0.496,-0.058,0.318,0,2026-03-31,1.015,2,1,0,0,13.394,0.027
ISL,76.77,-0.106,-0.136,-0.142,-0.038,-0.388,0.413,0,2026-03-31,0.896,1,0,0,0,25.861,0.027
ITTEFAQ,8.01,-0.03,-0.002,-0.152,0.057,-0.34,0.934,0,,,2,0,0,0,,
JSML,68.61,-0.339,0.082,0.265,0.697,-0.512,2.813,2,,,0,0,0,0,,
JVDC,132.14,-0.02,-0.052,0.789,1.284,-0.175,0.658,0,2026-03-31,2.407,2,0,0,0,14.977,0.078
KEL,8.34,0.083,0.062,0.461,0.771,-0.115,0.725,0,2024-06-30,-0.871,0,0,0,0,30.127,
KOHC,83.23,-0.069,-0.175,-0.192,0.114,-0.32,0.483,0,2026-03-31,-0.151,2,0,0,0,6.026,
KSBP,198.17,0.03,0.104,-0.093,0.157,-0.24,0.681,1,2026-03-31,0.169,1,0,0,0,,
KTML,45.66,-0.063,-0.234,-0.258,0.465,-0.378,0.387,0,2024-12-31,1.398,2,0,0,0,3.207,0.01
LCI,223.24,-0.092,-0.145,-0.256,-0.248,-0.4,0.598,0,2026-03-31,-0.271,3,0,0,0,12.485,0.041
LOADS,13.16,-0.001,-0.056,-0.306,-0.101,-0.366,2.406,0,2026-03-31,1.714,1,0,0,0,13.777,
LOTCHEM,26.97,-0.028,0.164,0.135,0.571,-0.098,0.32,0,2026-03-31,1.204,1,1,0,0,39.488,0.171
LUCK,422.13,-0.021,-0.031,-0.018,0.31,-0.177,0.773,0,2026-03-31,0.063,2,0,0,0,6.763,0.011
MACFL,59.0,1.519,1.182,1.234,2.637,-0.092,2.366,4,2026-03-31,0.777,2,0,0,0,34.336,0.01
MARI,643.56,-0.034,-0.027,-0.084,0.086,-0.174,0.514,0,2026-03-31,0.311,1,0,0,0,11.514,0.035
MEBL,479.56,-0.005,0.051,0.198,0.816,-0.062,0.542,0,2026-03-31,0.006,2,0,0,0,8.82,0.063
MLCF,84.36,-0.051,-0.16,-0.202,0.134,-0.353,1.127,0,2024-12-31,0.708,1,0,0,0,7.675,
MTL,546.44,0.057,0.044,0.117,0.013,-0.052,1.438,0,2026-03-31,1.227,2,3,0,0,17.531,0.107
MUGHAL,73.05,-0.065,-0.115,-0.132,0.012,-0.339,0.393,0,2026-03-31,0.676,3,0,0,0,28.337,
NETSOL,127.96,0.082,0.105,-0.009,-0.079,-0.213,2.32,0,2026-03-31,3.392,3,3,0,0,8.173,
NML,141.5,-0.099,-0.162,-0.001,0.285,-0.31,0.513,0,2026-03-31,0.835,2,0,0,0,8.671,0.016
NRL,376.53,-0.016,0.13,-0.115,0.504,-0.188,0.835,0,2026-03-31,,3,0,0,0,,
NRSL,35.95,0.053,0.268,0.063,0.008,-0.078,1.222,0,2026-03-31,0.296,3,0,0,0,16.932,
OBOY,13.3,0.364,0.255,0.393,0.566,-0.113,1.564,4,,,2,0,0,0,,
OCTOPUS,31.68,-0.012,-0.091,-0.266,-0.393,-0.466,0.897,0,,,5,0,0,0,,
OGDC,323.51,0.018,0.17,0.299,0.618,-0.021,0.79,0,2026-03-31,-0.104,2,0,0,0,5.583,0.068
PAEL,39.07,-0.084,-0.205,-0.26,-0.113,-0.38,0.653,0,2026-03-31,0.324,2,0,0,0,13.768,
PIBTL,16.22,-0.011,-0.103,0.044,0.827,-0.282,0.666,0,2026-03-31,,1,0,0,0,,
PIOC,270.92,0.129,-0.019,-0.162,0.29,-0.357,0.292,0,2026-03-31,0.562,1,0,0,0,10.627,0.044
POWER,20.18,0.043,0.079,0.124,0.413,-0.066,0.799,0,2026-03-31,2.0,2,1,0,0,31.257,
PPL,235.26,0.014,0.071,0.171,0.441,-0.149,0.605,0,2026-03-31,-0.06,2,0,0,0,5.148,0.044
PREMA,35.29,0.034,0.028,-0.098,-0.255,-0.333,1.286,1,2026-03-31,-0.133,2,1,0,0,16.658,
PRL,34.75,-0.09,0.088,-0.082,0.054,-0.134,0.863,0,2026-03-31,,2,0,0,0,,
PSO,346.34,-0.114,-0.122,-0.236,-0.06,-0.312,0.793,0,2026-03-31,6.803,2,0,0,0,10.778,0.026
QUICE,28.33,0.178,0.045,1.927,2.632,-0.323,0.731,0,,,3,1,0,0,,
SAZEW,2156.01,0.022,-0.027,0.285,0.769,-0.113,0.911,0,2026-03-31,0.034,0,0,0,0,4.217,0.046
SEARL,88.16,-0.057,-0.158,-0.148,0.181,-0.347,0.566,0,2026-03-31,,2,2,0,0,,
SGF,124.53,0.221,0.111,0.329,0.658,-0.073,1.454,0,2026-03-31,3.0,2,0,0,0,,
SGPL,36.13,-0.097,0.469,1.149,3.804,-0.569,1.592,1,2026-03-31,,2,0,0,0,,
SLGL,14.91,-0.048,-0.254,-0.231,-0.007,-0.407,0.347,0,2026-03-31,0.064,2,0,0,0,11.307,
SNGP,100.65,-0.034,0.004,-0.148,-0.123,-0.264,0.997,0,2026-03-31,0.226,2,0,0,0,5.073,0.026
SPEL,43.45,0.008,-0.064,-0.195,0.025,-0.435,0.544,0,2026-03-31,-0.084,1,0,0,0,,
SSGC,26.22,-0.087,-0.139,-0.218,-0.227,-0.428,1.382,0,2026-03-31,-0.48,2,0,0,0,10.954,0.012
SSOM,408.77,-0.187,-0.279,-0.088,-0.509,-0.614,0.762,0,,,2,0,0,0,,
STL,53.12,-0.13,-0.96,-0.97,-0.936,-0.974,1.837,0,2026-03-31,2.043,2,1,0,0,9.853,
SYM,10.33,-0.051,-0.207,-0.223,-0.29,-0.353,1.794,0,2026-03-31,-0.8,2,3,0,0,,
SYS,150.0,-0.003,0.115,0.024,0.359,-0.112,0.457,0,2025-12-31,0.5,0,0,0,0,22.795,0.012
TATM,130.52,-0.071,-0.146,-0.236,1.82,-0.556,0.784,0,2026-03-31,,2,0,0,0,6.525,
TBL,9.72,0.003,-0.137,-0.194,-0.181,-0.341,1.988,0,,,2,0,0,0,,
TELE,8.17,-0.041,-0.173,-0.322,0.11,-0.384,0.644,0,2026-03-31,0.464,2,0,0,0,18.478,
TGL,165.46,-0.026,-0.142,-0.161,-0.193,-0.406,0.453,0,2026-03-31,-0.111,2,1,0,0,9.051,0.016
TOMCL,34.48,-0.056,-0.188,-0.366,0.196,-0.48,0.47,0,2026-03-31,-0.848,2,0,0,0,13.655,
TPLP,8.1,-0.056,-0.17,-0.271,-0.139,-0.373,0.84,0,,,2,0,0,0,,
TPLT,17.05,0.574,0.536,1.323,1.818,-0.051,1.174,0,,,1,0,0,0,,
TREET,23.95,-0.056,-0.111,-0.264,0.224,-0.338,0.751,0,2026-03-31,-1.0,2,0,0,0,17.461,
TRSM,16.13,0.111,0.367,-0.712,1.927,-0.764,0.804,0,2026-03-31,-2.0,2,0,0,0,,
WAFI,197.73,-0.048,-0.09,0.033,0.226,-0.191,0.726,0,2026-03-31,1.478,3,0,0,0,13.409,0.032
WAVES,9.88,-0.056,-0.212,-0.28,0.302,-0.399,0.448,0,2026-03-31,0.042,3,0,0,0,8.618,
ZAL,43.97,-0.265,-0.292,-0.1,1.785,-0.392,0.587,0,2026-03-31,-3.118,2,0,0,0,6.31,0.062

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2026-05-15,QUICE,material_info,Material Information
2026-05-15,HINOON,dividend_or_bonus,Credit of Final Cash Dividend
2026-05-15,SGPL,insider_trade,Insider trade disclosure
2026-05-18,AGP,financial_result,ADJOURNMENT OF BOARD MEETING OTHER THAN FINANCIAL RESULTS
2026-05-18,OCTOPUS,financial_result,Financial Results for the Quarter Ended 31 March 2026
2026-05-18,NETSOL,insider_trade,Insider trade disclosure
2026-05-18,MACFL,insider_trade,Insider trade disclosure
2026-05-19,PREMA,material_info,Material Information
2026-05-19,EPCL,material_info,Material Information - Engro Polymer & Chemicals Limited
2026-05-19,HCAR,financial_result,"Financial Results for the Year Ended March 31, 2026"
2026-05-19,MEBL,dividend_or_bonus,CREDIT OF INTERIM CASH DIVIDEND OF MEEZAN BANK LIMITED
2026-05-19,HUBC,dividend_or_bonus,Credit of Third Interim Cash Dividend (D-59)
2026-05-19,TPLT,insider_trade,Insider trade disclosure
2026-05-19,TPLP,insider_trade,Insider trade disclosure
2026-05-19,BNL,insider_trade,Insider trade disclosure
2026-05-19,ILP,insider_trade,Insider trade disclosure
2026-05-20,MEBL,dividend_or_bonus,PUBLICATION OF NOTICES FOR THE CREDIT OF INTERIM CASH DIVIDEND OF MEEZAN BA
2026-05-20,FFC,dividend_or_bonus,Credit of Interim Cash Dividend
2026-05-20,SGPL,dividend_or_bonus,Draft Offer Document - Right Issue.
2026-05-20,TPLT,insider_trade,Insider trade disclosure
2026-05-20,BNL,insider_trade,Insider trade disclosure
2026-05-21,IPAK,material_info,Material Information
2026-05-21,CPHL,material_info,Material Information
2026-05-21,SYM,material_info,Material Information - Acquisition
2026-05-21,TGL,material_info,Material Information
2026-05-21,AGP,financial_result,ADJOURNMENT OF BOARD MEETING OTHER THAN FINANCIAL RESULTS
2026-05-21,FATIMA,insider_trade,Insider trade disclosure
2026-05-21,BNL,insider_trade,Insider trade disclosure
2026-05-21,MACFL,insider_trade,Insider trade disclosure
2026-05-21,OGDC,insider_trade,Insider trade disclosure
2026-05-21,WAVES,insider_trade,Insider trade disclosure
2026-05-22,AGP,material_info,DISCLOSURE OF MATERIAL INFORMATION
2026-05-22,AVN,financial_result,Financial Results for the Quarter Ended 31 March 2026
2026-05-22,OCTOPUS,financial_result,Transmission of Annual Report for the Year Ended 31 December 2025
2026-05-22,OCTOPUS,financial_result,Transmission of Quarterly Report for the Period Ended 31 March 2026
2026-05-22,AVN,financial_result,Transmission of Annual Report for the Year Ended 31 December 2025
2026-05-22,OGDC,dividend_or_bonus,CREDIT OF THIRD INTERIM CASH DIVIDEND (D-98)
2026-05-22,MTL,insider_trade,Insider trade disclosure
2026-05-22,MTL,insider_trade,Insider trade disclosure
2026-05-22,GWLC,insider_trade,Insider trade disclosure

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,2.865,2026-05-21
investor_type,last_5_sessions,broker proprietary trading,-2.635,2026-05-21
investor_type,last_5_sessions,companies,-4.872,2026-05-21
investor_type,last_5_sessions,foreign corporates,-13.636,2026-05-21
investor_type,last_5_sessions,foreign individual,0.027,2026-05-21
investor_type,last_5_sessions,individuals,6.621,2026-05-21
investor_type,last_5_sessions,insurance companies,9.328,2026-05-21
investor_type,last_5_sessions,mutual funds,1.124,2026-05-21
investor_type,last_5_sessions,nbfc,0.214,2026-05-21
investor_type,last_5_sessions,other organization,-0.055,2026-05-21
investor_type,last_5_sessions,overseas pakistani,1.019,2026-05-21
sector,last_5_sessions,fipi | Cement,-4.263,2026-05-21
sector,last_5_sessions,fipi | Commercial Banks,-6.43,2026-05-21
sector,last_5_sessions,lipi banks / dfi | All other Sectors,5.541,2026-05-21
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-2.544,2026-05-21
sector,last_5_sessions,lipi companies | Commercial Banks,-3.785,2026-05-21
sector,last_5_sessions,lipi individuals | All other Sectors,5.553,2026-05-21
sector,last_5_sessions,lipi individuals | Cement,-2.806,2026-05-21
sector,last_5_sessions,lipi individuals | Commercial Banks,2.808,2026-05-21
sector,last_5_sessions,lipi insurance companies | All other Sectors,-8.669,2026-05-21
sector,last_5_sessions,lipi insurance companies | Commercial Banks,5.887,2026-05-21
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,5.521,2026-05-21
sector,last_5_sessions,lipi mutual funds | Cement,4.755,2026-05-21
investor_type,last_20_sessions,banks / dfi,6.923,2026-05-21
investor_type,last_20_sessions,broker proprietary trading,1.019,2026-05-21
investor_type,last_20_sessions,companies,-4.714,2026-05-21
investor_type,last_20_sessions,foreign corporates,-21.175,2026-05-21
investor_type,last_20_sessions,foreign individual,-0.052,2026-05-21
investor_type,last_20_sessions,individuals,51.486,2026-05-21
investor_type,last_20_sessions,insurance companies,-1.807,2026-05-21
investor_type,last_20_sessions,mutual funds,-47.123,2026-05-21
investor_type,last_20_sessions,nbfc,0.875,2026-05-21
investor_type,last_20_sessions,other organization,1.546,2026-05-21
investor_type,last_20_sessions,overseas pakistani,13.021,2026-05-21
sector,last_20_sessions,fipi | Commercial Banks,-12.245,2026-05-21
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,5.711,2026-05-21
sector,last_20_sessions,lipi banks / dfi | All other Sectors,10.279,2026-05-21
sector,last_20_sessions,lipi individuals | All other Sectors,10.031,2026-05-21
sector,last_20_sessions,lipi individuals | Commercial Banks,20.424,2026-05-21
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,5.529,2026-05-21
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,10.159,2026-05-21
sector,last_20_sessions,lipi insurance companies | All other Sectors,-18.585,2026-05-21
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-11.185,2026-05-21
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-8.215,2026-05-21
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,-9.915,2026-05-21
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,-7.623,2026-05-21

=== FILE: calendar.md ===
# Calendar as of 2026-05-22

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2026-04-23 CPHL: Board Meeting
- 2026-04-23 FFL: Board Meeting Rescheduled
- 2026-04-23 STL: Board Meeting
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
- 2026-05-08 AGP: Board Meeting Other Than Financial Results
- 2026-05-14 AVN: Board Meeting
- 2026-05-14 SGPL: Board Meeting Other Than Financial Results
- 2026-05-15 SYS: Board Meeting for the First Quarter ended 31 March 2026
- 2026-05-18 JSML: Board Meeting
- 2026-05-18 SGPL: Board Meeting Material Information
- 2026-05-18 CRTM: Board Meeting Other Than Financial Results
- 2026-05-21 CLOV: Notice of an Emergent Board Meeting other than Financial Matters
- 2026-05-22 BIFO: Board Meeting Other Than Financial Results

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
