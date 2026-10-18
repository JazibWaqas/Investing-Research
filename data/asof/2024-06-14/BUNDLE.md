# Replay bundle, close of 2024-06-14

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
# Market as of 2024-06-14 close (public information only)

- KSE100: 76,707 on 2024-06-14; 1m +2.7%, 3m +16.7%, 6m +15.8%, 12m +83.0%
- KMI All Share: 34,609 on 2024-06-14; 1m -0.2%, 3m +9.6%, 6m +7.7%, 12m +69.4%
- Policy rate 20.5%; last MPC decision 2024-06-10: cut (-150bp)
- 6M T-bill cutoff 19.97% (auction 2024-06-12); 3M 20.15%, 12M 18.95%
- CPI YoY 11.74% for 2024-05 (published by 2024-06-03); three months earlier (2024-02) 23.07%
- Brent: 81.49 USD/bbl on 2024-06-14; 3-month change -5.4%
- USD/PKR: 278.54  on 2024-06-14; 3-month change -0.1%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate -0.53pp (market pricing cuts); CPI falling over 3 months (-11.3pp)
- Next MPC: see SBP calendar

Session date used: 2024-06-14. Liquid KMI names: 87 (membership KMI_ALL_derived_2023-12-26.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,-0.0919,-0.1323,-0.1789,0,0
E&P,3,-0.0405,0.0681,0.1603,0,0
OMC,4,0.0215,0.1908,0.0048,0,0
Power,5,0.0108,0.071,0.0168,1,1
Fertilizer,4,0.0179,0.2457,0.3998,0,0
Cement,16,0.0001,0.2172,0.1377,0,2
Steel & engineering,11,0.037,0.16,0.0905,0,2
Autos,12,-0.0078,0.2984,0.3406,2,3
Tech & telecom,10,0.0633,0.1205,0.4942,1,3
Islamic banks & fin.,8,0.0104,0.0975,0.0947,1,3
Pharma,13,0.0165,0.1898,0.131,2,4
Textiles,23,-0.0285,0.0096,-0.0327,0,0
Food & staples,14,-0.0301,0.0017,-0.1264,0,0
Chemicals,18,-0.0175,0.0371,-0.0935,2,3
"Glass, packaging, paper",13,-0.0271,0.0353,-0.0755,0,0
Gas utilities & misc,11,-0.0635,-0.0698,-0.1584,0,0

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AIRLINK,80.37,0.078,0.222,0.13,2.716,-0.007,0.825,0,2024-03-31,5.238,0,1,0,0,8.16,0.121
ATRL,361.47,-0.071,-0.026,0.004,1.056,-0.137,0.494,0,2024-03-31,-0.4,0,0,0,0,0.597,0.073
AVN,56.35,-0.012,0.134,-0.042,0.286,-0.071,1.337,0,2024-03-31,-1.064,1,0,0,0,,
BCL,140.07,-0.11,0.943,1.504,3.214,-0.183,1.166,0,,,0,0,0,0,,
BGL,14.52,-0.112,0.62,0.282,0.37,-0.112,1.411,2,,,0,1,0,0,,
BIPL,21.4,-0.044,-0.059,-0.066,0.382,-0.186,0.576,0,2024-03-31,0.784,0,0,0,0,,
CEPB,31.07,-0.054,0.083,-0.186,0.006,-0.203,0.69,0,2024-03-31,-0.426,0,0,0,0,,
CHCC,164.14,-0.023,0.058,-0.001,0.33,-0.03,0.916,0,2024-03-31,-0.023,0,0,0,0,5.307,0.037
CLOV,45.8,-0.045,0.567,0.604,2.207,-0.125,0.626,0,2023-12-31,,0,0,0,0,,
CNERGY,4.1,-0.085,-0.198,-0.199,0.231,-0.305,0.401,0,2024-03-31,,0,1,0,0,,
CPHL,28.66,-0.08,0.158,0.057,0.238,-0.13,0.974,0,2023-12-31,0.271,0,0,0,0,7.41,0.117
DCL,9.04,0.05,0.25,0.14,1.0,-0.183,2.989,0,,,0,0,0,0,,
DGKC,92.73,0.04,0.306,0.151,0.756,-0.027,1.429,0,2024-03-31,0.054,0,0,0,0,,
EFERT,165.47,0.073,0.121,0.521,0.915,-0.054,0.619,0,2024-03-31,0.761,0,0,0,0,5.722,0.183
EPCL,43.62,0.02,0.012,-0.098,0.137,-0.13,0.414,0,2024-03-31,-1.977,0,1,0,0,5.11,0.129
FABL,44.41,0.134,0.435,0.341,1.065,0.0,1.571,0,2024-03-31,0.995,1,1,0,0,2.442,0.123
FATIMA,48.77,-0.02,0.29,0.462,0.772,-0.078,0.355,0,2024-03-31,1.083,0,0,0,0,3.239,0.127
FCCL,23.91,0.058,0.325,0.181,0.924,-0.01,1.769,0,2023-06-30,-0.681,0,0,0,0,3.877,
FCEPL,72.83,0.004,-0.007,-0.216,0.1,-0.275,1.474,0,2024-03-31,-0.326,0,0,0,0,41.597,
FFL,9.21,-0.063,-0.036,-0.121,0.53,-0.197,0.368,0,2024-03-31,,0,0,0,0,46.392,
GAL,175.76,-0.021,1.077,1.295,4.442,-0.111,1.322,0,2024-03-31,-0.484,0,0,0,0,11.951,
GGL,10.02,-0.081,-0.038,-0.264,-0.031,-0.281,0.991,0,2024-03-31,0.2,0,0,0,0,9.587,
GHNI,277.54,-0.072,0.612,0.492,2.483,-0.107,0.834,1,2024-03-31,1.615,0,0,0,0,19.126,
GLAXO,140.24,0.064,0.615,0.469,0.763,-0.006,0.816,1,2024-03-31,0.318,0,0,0,0,49.498,
GTYR,43.82,-0.082,0.202,0.054,0.964,-0.082,0.937,0,2024-03-31,,0,0,0,0,,
GWLC,33.47,-0.002,0.334,0.26,1.128,-0.04,2.638,2,2024-03-31,0.015,0,0,0,0,,
HCAR,297.13,-0.044,0.194,0.293,2.118,-0.115,0.732,0,2024-03-31,,2,0,0,0,64.681,
HTL,34.12,0.003,0.37,0.11,0.456,-0.092,2.54,2,,,0,0,0,0,,
HUBC,145.46,0.064,0.258,0.244,1.498,0.0,0.948,0,2024-03-31,0.528,0,0,0,0,1.568,0.431
ILP,69.12,-0.165,-0.035,-0.082,1.208,-0.178,1.616,0,2024-03-31,-0.569,0,0,0,0,2.45,0.113
INIL,192.07,0.172,0.428,0.399,1.401,-0.023,2.472,0,2024-03-31,-0.772,0,0,0,0,3.136,0.102
ISL,86.88,0.139,0.249,0.159,0.964,-0.012,1.906,0,2024-03-31,-0.534,0,0,0,0,5.01,0.136
KEL,4.62,0.002,-0.019,0.043,1.525,-0.245,0.854,0,2023-06-30,0.033,1,1,0,0,,
KOHC,235.38,0.068,0.07,0.036,0.399,-0.055,1.014,1,2024-03-31,0.296,0,0,0,0,5.986,
LOTCHEM,17.9,-0.021,-0.072,-0.361,-0.4,-0.395,0.991,0,2024-03-31,-0.649,0,0,0,0,8.049,0.111
LPL,24.99,0.075,0.238,0.07,2.574,-0.128,2.44,0,,,0,0,0,0,,
LUCK,946.44,0.06,0.24,0.192,0.838,-0.011,1.193,0,2024-03-31,-0.199,0,0,0,0,3.356,0.034
MARI,2719.58,-0.038,0.111,0.316,0.744,-0.042,1.036,0,2024-03-31,-0.14,0,0,0,0,3.6,0.097
MEBL,242.49,0.092,0.394,0.489,2.152,-0.014,1.063,0,2024-03-31,0.614,0,0,0,0,3.383,0.124
MLCF,38.31,-0.037,0.009,-0.103,0.335,-0.103,1.133,0,,,0,1,0,0,5.269,
MTL,658.41,0.082,0.092,0.062,0.963,-0.005,1.131,0,2024-03-31,0.693,0,0,0,0,22.731,0.054
MUGHAL,96.91,0.291,0.436,0.323,0.96,-0.013,3.027,0,2024-03-31,-0.92,0,0,0,0,4.671,0.066
NETSOL,142.53,0.27,0.051,0.196,0.895,-0.013,2.087,1,2024-03-31,-0.99,1,1,0,0,6.329,
NML,72.46,0.027,0.048,-0.12,0.176,-0.134,1.893,0,2024-03-31,-0.673,0,0,0,0,1.767,0.088
NRL,272.02,-0.095,-0.124,-0.262,0.67,-0.264,0.546,0,2024-03-31,,0,1,0,0,,
OGDC,131.21,-0.058,0.042,0.083,0.807,-0.127,0.592,1,2024-03-31,-0.26,0,1,0,0,1.494,0.11
PABC,73.0,0.063,0.013,-0.058,0.481,-0.077,0.905,0,,,0,1,0,0,,
PAEL,24.89,-0.077,0.04,0.167,1.555,-0.141,0.798,1,2024-03-31,16.0,0,0,0,0,15.073,
PIBTL,6.24,-0.08,0.036,0.021,0.465,-0.214,0.34,0,2024-03-31,,0,0,0,0,,
PIOC,163.39,0.006,0.218,0.379,0.881,-0.029,1.117,1,2024-03-31,0.266,0,0,0,0,7.536,
PPL,119.76,-0.027,0.045,0.052,0.954,-0.105,0.552,0,2024-03-31,-0.152,0,0,0,0,1.655,0.042
PREMA,15.09,0.029,0.125,-0.133,-0.089,-0.213,2.368,1,2024-03-31,-0.832,0,0,0,0,2.884,
PRL,23.86,-0.119,-0.188,-0.25,0.584,-0.32,0.53,0,2024-03-31,-1.701,0,1,0,0,4.681,
PSO,171.67,-0.049,-0.006,-0.21,0.524,-0.21,0.47,0,2024-03-31,-0.657,0,0,0,0,5.593,0.068
SAZEW,802.06,0.093,0.853,2.631,15.07,-0.059,0.799,1,2024-03-31,5.821,1,1,0,0,3.089,0.079
SEARL,59.86,0.008,0.09,-0.043,0.389,-0.054,1.012,0,2024-03-31,-3.239,0,0,0,0,47.647,
SNGP,65.52,-0.081,-0.001,-0.056,0.537,-0.171,0.594,0,2024-03-31,0.619,0,0,0,0,2.364,0.114
SSGC,10.07,-0.034,-0.089,-0.268,0.062,-0.274,0.247,0,2021-06-30,,3,0,0,0,,
SYS,437.81,0.123,0.088,-0.04,0.099,-0.058,1.771,0,2024-03-31,-0.596,0,0,0,0,14.2,0.014
TELE,7.9,-0.086,-0.13,-0.138,0.137,-0.241,0.38,0,2024-03-31,-1.225,1,1,0,0,7.795,
TGL,113.64,0.003,0.108,0.044,0.566,-0.088,1.066,1,2024-03-31,-0.158,0,1,0,0,4.654,0.088
THCCL,36.2,-0.004,0.868,0.977,2.175,-0.087,0.947,1,2024-03-31,4.667,0,1,0,0,11.468,
TOMCL,34.03,0.044,0.403,0.4,0.586,-0.14,1.229,1,2024-03-31,-0.716,0,0,0,0,3.884,
TPLP,9.82,-0.147,-0.136,-0.336,-0.038,-0.357,0.696,0,,,0,0,0,0,,
TREET,15.67,-0.072,-0.103,-0.162,0.07,-0.274,0.416,0,2024-03-31,0.486,0,1,0,0,,
UNITY,26.92,0.044,0.139,-0.02,0.996,-0.047,0.705,0,2024-03-31,,0,2,0,0,27.645,
WAFI,138.55,-0.05,-0.139,-0.212,0.69,-0.217,0.657,0,,,0,0,0,0,5.504,0.033

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2024-05-16,HINOON,material_info,Material Information
2024-05-16,NATF,insider_trade,Insider trade disclosure
2024-05-16,SNBL,insider_trade,Insider trade disclosure
2024-05-16,NICL,insider_trade,Insider trade disclosure
2024-05-16,SMCPL,insider_trade,Insider trade disclosure
2024-05-16,LSEVL,insider_trade,Insider trade disclosure
2024-05-17,THCCL,material_info,Material Information - Wind Power Project
2024-05-17,BAFL,material_info,MATERIAL INFORMATION - STATE BANK OF PAKISTAN IN-PRINCIPLE APPROVAL FOR DUE
2024-05-17,UNITY,material_info,Material Information
2024-05-17,DAWH,material_info,Material Information
2024-05-17,LOADS,material_info,Material Information
2024-05-17,ENGRO,material_info,Disclosure of Material Information
2024-05-17,LCI,material_info,Material Information
2024-05-17,FABL,financial_result,"Credit of 10% Interim Cash Dividend for the First Quarter ended March 31, 2"
2024-05-17,NETSOL,financial_result,Emergent Board Meeting Other Than Financial Results
2024-05-17,AVN,financial_result,AVN | Avanceon Limited Transmission of Quarterly Report for the period ende
2024-05-17,PCAL,insider_trade,Insider trade disclosure
2024-05-17,PCAL,insider_trade,Insider trade disclosure
2024-05-17,SNBL,insider_trade,Insider trade disclosure
2024-05-17,HCAR,insider_trade,Insider trade disclosure
2024-05-17,ANTM,insider_trade,Insider trade disclosure
2024-05-17,LSEVL,insider_trade,Insider trade disclosure
2024-05-17,SEARL,insider_trade,Insider trade disclosure
2024-05-17,BIFO,insider_trade,Insider trade disclosure
2024-05-17,EMCO,insider_trade,Insider trade disclosure
2024-05-17,WAVES,insider_trade,Insider trade disclosure
2024-05-17,INIL,insider_trade,Insider trade disclosure
2024-05-17,INIL,insider_trade,Insider trade disclosure
2024-05-17,INIL,insider_trade,Insider trade disclosure
2024-05-17,WAVESAPP,insider_trade,Insider trade disclosure
2024-05-17,ILP,insider_trade,Insider trade disclosure
2024-05-17,PCAL,insider_trade,Insider trade disclosure
2024-05-17,PCAL,insider_trade,Insider trade disclosure
2024-05-17,PKGS,insider_trade,Insider trade disclosure
2024-05-17,IGIHL,insider_trade,Insider trade disclosure
2024-05-20,SYM,material_info,Material Information
2024-05-20,SYM,material_info,Material Information
2024-05-20,KEL,material_info,Disclosure of Material Information.
2024-05-20,KEL,financial_result,Emergent Board Meeting Other Than Financial Results
2024-05-20,SNBL,insider_trade,Insider trade disclosure
2024-05-20,INIL,insider_trade,Insider trade disclosure
2024-05-20,SHFA,insider_trade,Insider trade disclosure
2024-05-20,LSEVL,insider_trade,Insider trade disclosure
2024-05-20,TBL,insider_trade,Insider trade disclosure
2024-05-20,SYS,insider_trade,Insider trade disclosure
2024-05-20,SYS,insider_trade,Insider trade disclosure
2024-05-20,SYS,insider_trade,Insider trade disclosure
2024-05-20,SYS,insider_trade,Insider trade disclosure
2024-05-21,SYM,material_info,Material Information
2024-05-21,TELE,financial_result,Transmission of Quarterly Report for the Period Ended
2024-05-21,LPL,dividend_or_bonus,CREDIT OF 20% INTERIM CASH DIVIDEND
2024-05-21,SGF,insider_trade,Insider trade disclosure
2024-05-21,FPRM,insider_trade,Insider trade disclosure
2024-05-21,NATF,insider_trade,Insider trade disclosure
2024-05-21,UBL,insider_trade,"DISCLOSURE OF INTEREST BY THE DIRECTORS, CEO, EXECUTIVES, THEIR SPOUSES AND"
2024-05-21,UBL,insider_trade,Insider trade disclosure
2024-05-22,PRL,material_info,PRL | Pakistan Refinery Limited Material Information
2024-05-22,NETSOL,material_info,Material Information
2024-05-22,PABC,material_info,Material Information
2024-05-22,CLVL,material_info,Material Information
2024-05-22,CSIL,material_info,Material Information
2024-05-22,OGDC,dividend_or_bonus,Credit of Third Interim Cash Dividend (D-90)
2024-05-22,SITC,insider_trade,Insider trade disclosure
2024-05-22,PCAL,insider_trade,Insider trade disclosure
2024-05-22,KCL,insider_trade,Insider trade disclosure
2024-05-22,FEROZ,insider_trade,Insider trade disclosure
2024-05-22,SHFA,insider_trade,Insider trade disclosure
2024-05-23,MERIT,material_info,MATERIAL INFORMATION
2024-05-23,LSEPL,material_info,Material Information
2024-05-23,MODAM,material_info,Material Information-Dissulotion of Modaraba Al-Mali
2024-05-23,GCIL,insider_trade,Insider trade disclosure
2024-05-23,LSEVL,insider_trade,Insider trade disclosure
2024-05-23,NICL,insider_trade,Insider trade disclosure
2024-05-23,NONS,insider_trade,Insider trade disclosure
2024-05-23,UBL,insider_trade,"DISCLOSURE OF INTEREST BY THE DIRECTORS, CEO, EXECUTIVES, THEIR SPOUSES AND"
2024-05-23,WAVES,insider_trade,Insider trade disclosure
2024-05-23,WAVES,insider_trade,Insider trade disclosure
2024-05-24,TPLT,material_info,Material Information
2024-05-24,AGTL,material_info,Material Information: GO-LIVE SAP S/4 HANA
2024-05-24,FECM,material_info,Material Information
2024-05-24,CNERGY,material_info,Material Information
2024-05-24,RPL,material_info,Disclosure of Material Information
2024-05-24,PPL,dividend_or_bonus,Credit of 2nd Interim Dividend 2023-24
2024-05-24,HUBC,dividend_or_bonus,Credit of Interim Cash Dividend
2024-05-24,BAFL,insider_trade,Insider trade disclosure
2024-05-24,KOSM,insider_trade,Insider trade disclosure
2024-05-24,LSEVL,insider_trade,Insider trade disclosure
2024-05-24,HBL,insider_trade,Insider trade disclosure
2024-05-24,PKGI,insider_trade,Pakistan General Insurance Company Limited - Right Issue - Directors' and S
2024-05-24,TBL,insider_trade,Insider trade disclosure
2024-05-24,PPL,insider_trade,Insider trade disclosure
2024-05-24,JSCLPSA,insider_trade,Insider trade disclosure
2024-05-24,PKGI,insider_trade,Pakistan General Insurance Company Limited - Right Issue - Directors' and S
2024-05-24,DNCC,insider_trade,Insider trade disclosure
2024-05-27,NRL,material_info,Material Information
2024-05-27,FTSM,material_info,Material Information
2024-05-27,HCAR,financial_result,"Financial Results for the year ended March 31, 2024"
2024-05-27,SSGC,financial_result,"Transmission of Quarterly Report for the Period Ended 30th September, 2022"
2024-05-27,SSGC,financial_result,Transmission of Quarterly Report for the Period Ende 31st December 2022
2024-05-27,ALTN,insider_trade,Insider trade disclosure
2024-05-27,FECM,insider_trade,Insider trade disclosure
2024-05-27,SITC,insider_trade,Insider trade disclosure
2024-05-27,BAFL,insider_trade,Insider trade disclosure
2024-05-27,SYS,insider_trade,Insider trade disclosure
2024-05-27,PPL,insider_trade,Insider trade disclosure
2024-05-29,DFML,material_info,Material Information
2024-05-29,EPCL,material_info,Disclosure of Material Information
2024-05-29,LSECL,material_info,Material Information-Merger Effect Statement
2024-05-29,FUDLM,material_info,Material Information - UDL International Ltd
2024-05-29,MEBL,insider_trade,Insider trade disclosure
2024-05-29,HBL,insider_trade,Insider trade disclosure
2024-05-29,SHFA,insider_trade,Insider trade disclosure
2024-05-29,ILP,insider_trade,Insider trade disclosure
2024-05-29,BHAT,insider_trade,Insider trade disclosure
2024-05-29,FASM,insider_trade,Insider trade disclosure
2024-05-29,BTL,insider_trade,Insider trade disclosure
2024-05-29,EPCL,insider_trade,Insider trade disclosure
2024-05-29,MIRKS,insider_trade,Insider trade disclosure
2024-05-30,TGL,material_info,Material Information
2024-05-30,LCI,material_info,Material Information
2024-05-30,SHEL,material_info,Material Information
2024-05-30,PCAL,material_info,Material Information
2024-05-30,DFML,material_info,Material Information
2024-05-30,HBL,insider_trade,Insider trade disclosure
2024-05-30,BAHL,insider_trade,Insider trade disclosure
2024-05-30,TBL,insider_trade,Insider trade disclosure
2024-05-30,MEHT,insider_trade,Insider trade disclosure
2024-05-31,FABL,material_info,Material Information - Faysal Bank limited
2024-05-31,NATF,insider_trade,Insider trade disclosure
2024-05-31,MFL,insider_trade,Insider trade disclosure
2024-05-31,FCEPL,insider_trade,Insider trade disclosure
2024-05-31,FECM,insider_trade,Insider trade disclosure
2024-05-31,BIFO,insider_trade,Insider trade disclosure
2024-06-03,MFL,material_info,Material Information
2024-06-03,OGDC,material_info,Material Information
2024-06-03,SLCL,material_info,Material Information
2024-06-03,UBL,insider_trade,Insider trade disclosure
2024-06-03,FECM,insider_trade,Insider trade disclosure
2024-06-03,NONS,insider_trade,Insider trade disclosure
2024-06-03,BAFL,insider_trade,Insider trade disclosure
2024-06-04,BGL,material_info,MATERIAL INFORMATION REGARDING COMMENCEMENT OF COMMERCIAL OPERATIONS
2024-06-04,UBL,insider_trade,Insider trade disclosure
2024-06-04,ATRL,insider_trade,Insider trade disclosure
2024-06-04,ANTM,insider_trade,Insider trade disclosure
2024-06-04,SYM,insider_trade,Insider trade disclosure
2024-06-05,AIRLINK,material_info,Material Information
2024-06-05,SAZEW,financial_result,Emergent Board Meeting Other Than Financial Results
2024-06-05,PPL,dividend_or_bonus,Notice to Shareholders - Unclaimed Shares and Dividends
2024-06-05,NRL,insider_trade,Insider trade disclosure
2024-06-05,BIFO,insider_trade,Insider trade disclosure
2024-06-05,JSCLPSA,insider_trade,Insider trade disclosure
2024-06-05,PABC,insider_trade,Insider trade disclosure
2024-06-05,EFUG,insider_trade,Insider trade disclosure
2024-06-05,TBL,insider_trade,Insider trade disclosure
2024-06-05,HBL,insider_trade,Insider trade disclosure
2024-06-05,HRPL,insider_trade,Insider trade disclosure
2024-06-05,HBL,insider_trade,Insider trade disclosure
2024-06-05,FCEPL,insider_trade,Insider trade disclosure
2024-06-06,TREET,material_info,Material Information
2024-06-06,GEMBLUEX,material_info,Material Information
2024-06-06,TELE,material_info,Material information - Equity Investment in Hallmark Company Limited
2024-06-06,HCAR,financial_result,"Transmission of Annual Report for the year ended March 31, 2024"
2024-06-06,SERT,insider_trade,Insider trade disclosure
2024-06-06,SERT,insider_trade,Insider trade disclosure
2024-06-06,TPLP,insider_trade,Insider trade disclosure
2024-06-06,SANSM,insider_trade,Insider trade disclosure
2024-06-06,SANSM,insider_trade,Insider trade disclosure
2024-06-07,LSECL,material_info,Material Information-Initial offer to the accredited investor-Mughal Energy
2024-06-07,SAZEW,material_info,Material Information
2024-06-07,LSECL,material_info,Material Information-Initial offer to the accredited investors-Mughal Energ
2024-06-07,KCL,insider_trade,Insider trade disclosure
2024-06-07,SHFA,insider_trade,Insider trade disclosure
2024-06-07,JSCLPSA,insider_trade,Insider trade disclosure
2024-06-07,EMCO,insider_trade,Insider trade disclosure
2024-06-07,UNIC,insider_trade,Insider trade disclosure
2024-06-07,WAVES,insider_trade,Insider trade disclosure
2024-06-07,NONS,insider_trade,Correction of Disclosure of Information by a substantial shareholder
2024-06-07,ILP,insider_trade,Insider trade disclosure
2024-06-07,FPRM,insider_trade,FPRM | First Paramount Modaraba Disclosure of Interest by a Director CEO or
2024-06-10,SAPT,material_info,Material Information
2024-06-10,SFL,material_info,Material Information
2024-06-10,RCML,material_info,Material Information
2024-06-10,SSGC,financial_result,Emergent Board Meeting Other Than Financial Results
2024-06-10,UNITY,insider_trade,Insider trade disclosure
2024-06-10,UNITY,insider_trade,Insider trade disclosure
2024-06-10,UBL,insider_trade,Insider trade disclosure
2024-06-10,SHFA,insider_trade,Insider trade disclosure
2024-06-11,HPL,material_info,Material Information
2024-06-11,RCML,insider_trade,Insider trade disclosure
2024-06-11,PKGS,insider_trade,Insider trade disclosure
2024-06-11,WAVES,insider_trade,Insider trade disclosure
2024-06-12,MWMP,material_info,Material Information
2024-06-12,BNL,material_info,Material Information
2024-06-12,MLCF,material_info,Material Information
2024-06-12,HALEON,dividend_or_bonus,Prior Publication of Reminder for Conversion of Physical Shares to Book Ent
2024-06-12,FECM,insider_trade,Insider trade disclosure
2024-06-12,NICL,insider_trade,Insider trade disclosure
2024-06-12,JSCLPSA,insider_trade,Insider trade disclosure
2024-06-12,DEL,insider_trade,Insider trade disclosure
2024-06-12,ALAC,insider_trade,Insider trade disclosure
2024-06-12,PKGS,insider_trade,Insider trade disclosure
2024-06-12,MUGHAL,other,Listing of Mughal Energy Limited
2024-06-13,UNITY,material_info,Material Information
2024-06-13,TPL,material_info,Material Information
2024-06-13,DSML,material_info,Material Information Regarding Merger
2024-06-13,KTML,material_info,KTML-Material Information
2024-06-13,HALEON,dividend_or_bonus,Reminder for Conversion of Physical Shares to Book Entry Form & Unclaimed D
2024-06-13,SHFA,insider_trade,Insider trade disclosure
2024-06-13,UBL,insider_trade,Insider trade disclosure
2024-06-13,UBL,insider_trade,Insider trade disclosure
2024-06-13,CRTM,insider_trade,Insider trade disclosure
2024-06-13,MARI,other,Cancellation of Board Meeting
2024-06-14,FAYSAL-FUNDS,material_info,Material Information
2024-06-14,LSECL,material_info,Material Information-Appointment of Directors
2024-06-14,MUGHAL,dividend_or_bonus,NOTICE OF BOOK CLOSURE SUKUK-II (2nd PROFIT PAYMENT)
2024-06-14,ILP,insider_trade,Insider trade disclosure
2024-06-14,JSCLPSA,insider_trade,Insider trade disclosure
2024-06-14,TBL,insider_trade,Insider trade disclosure
2024-06-14,ATRL,other,NOTICE OF 22ND EXTRA ORDINARY GENERLA MEETING (EOGM)
2024-06-14,PSO,other,Corporate Briefing Session

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-1.465,2024-06-13
investor_type,last_5_sessions,broker proprietary trading,1.591,2024-06-13
investor_type,last_5_sessions,companies,7.399,2024-06-13
investor_type,last_5_sessions,foreign corporates,-5.829,2024-06-13
investor_type,last_5_sessions,foreign individual,0.017,2024-06-13
investor_type,last_5_sessions,individuals,-11.322,2024-06-13
investor_type,last_5_sessions,insurance companies,1.722,2024-06-13
investor_type,last_5_sessions,mutual funds,10.888,2024-06-13
investor_type,last_5_sessions,nbfc,-0.166,2024-06-13
investor_type,last_5_sessions,other organization,-1.122,2024-06-13
investor_type,last_5_sessions,overseas pakistani,-1.714,2024-06-13
sector,last_5_sessions,fipi | All other Sectors,-2.46,2024-06-13
sector,last_5_sessions,fipi | Cement,-0.524,2024-06-13
sector,last_5_sessions,fipi | Commercial Banks,0.771,2024-06-13
sector,last_5_sessions,fipi | Fertilizer,-1.76,2024-06-13
sector,last_5_sessions,fipi | Food and Personal Care Products,0.206,2024-06-13
sector,last_5_sessions,fipi | Oil and Gas Exploration Companies,-2.664,2024-06-13
sector,last_5_sessions,fipi | Oil and Gas Marketing Companies,-0.555,2024-06-13
sector,last_5_sessions,fipi | Power Generation and Distribution,-0.907,2024-06-13
sector,last_5_sessions,fipi | Technology and Communication,0.355,2024-06-13
sector,last_5_sessions,fipi | Textile Composite,0.012,2024-06-13
sector,last_5_sessions,lipi banks / dfi | All other Sectors,2.033,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Cement,-1.811,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,-0.894,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Fertilizer,0.064,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Food and Personal Care Products,-0.037,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,0.781,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-0.291,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Power Generation and Distribution,-1.085,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Technology and Communication,-0.223,2024-06-13
sector,last_5_sessions,lipi banks / dfi | Textile Composite,-0.0,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | All other Sectors,0.287,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Cement,0.926,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Commercial Banks,0.434,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Debt Market,-0.061,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Fertilizer,-0.014,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Food and Personal Care Products,0.093,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,0.206,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.138,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Power Generation and Distribution,0.128,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Technology and Communication,-0.507,2024-06-13
sector,last_5_sessions,lipi broker proprietary trading | Textile Composite,-0.039,2024-06-13
sector,last_5_sessions,lipi companies | All other Sectors,1.62,2024-06-13
sector,last_5_sessions,lipi companies | Cement,2.675,2024-06-13
sector,last_5_sessions,lipi companies | Commercial Banks,0.426,2024-06-13
sector,last_5_sessions,lipi companies | Debt Market,-0.664,2024-06-13
sector,last_5_sessions,lipi companies | Fertilizer,0.353,2024-06-13
sector,last_5_sessions,lipi companies | Food and Personal Care Products,0.006,2024-06-13
sector,last_5_sessions,lipi companies | Oil and Gas Exploration Companies,2.518,2024-06-13
sector,last_5_sessions,lipi companies | Oil and Gas Marketing Companies,-0.032,2024-06-13
sector,last_5_sessions,lipi companies | Power Generation and Distribution,0.078,2024-06-13
sector,last_5_sessions,lipi companies | Technology and Communication,0.06,2024-06-13
sector,last_5_sessions,lipi companies | Textile Composite,0.359,2024-06-13
sector,last_5_sessions,lipi individuals | All other Sectors,-2.918,2024-06-13
sector,last_5_sessions,lipi individuals | Cement,-3.018,2024-06-13
sector,last_5_sessions,lipi individuals | Commercial Banks,-2.261,2024-06-13
sector,last_5_sessions,lipi individuals | Debt Market,0.001,2024-06-13
sector,last_5_sessions,lipi individuals | Fertilizer,-2.038,2024-06-13
sector,last_5_sessions,lipi individuals | Food and Personal Care Products,-0.108,2024-06-13
sector,last_5_sessions,lipi individuals | Oil and Gas Exploration Companies,1.126,2024-06-13
sector,last_5_sessions,lipi individuals | Oil and Gas Marketing Companies,-0.499,2024-06-13
sector,last_5_sessions,lipi individuals | Power Generation and Distribution,-0.321,2024-06-13
sector,last_5_sessions,lipi individuals | Technology and Communication,-0.809,2024-06-13
sector,last_5_sessions,lipi individuals | Textile Composite,-0.478,2024-06-13
sector,last_5_sessions,lipi insurance companies | All other Sectors,-0.066,2024-06-13
sector,last_5_sessions,lipi insurance companies | Cement,-0.286,2024-06-13
sector,last_5_sessions,lipi insurance companies | Commercial Banks,-0.076,2024-06-13
sector,last_5_sessions,lipi insurance companies | Debt Market,-0.0,2024-06-13
sector,last_5_sessions,lipi insurance companies | Fertilizer,2.084,2024-06-13
sector,last_5_sessions,lipi insurance companies | Food and Personal Care Products,0.072,2024-06-13
sector,last_5_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-0.632,2024-06-13
sector,last_5_sessions,lipi insurance companies | Oil and Gas Marketing Companies,-0.028,2024-06-13
sector,last_5_sessions,lipi insurance companies | Power Generation and Distribution,0.548,2024-06-13
sector,last_5_sessions,lipi insurance companies | Technology and Communication,-0.176,2024-06-13
sector,last_5_sessions,lipi insurance companies | Textile Composite,0.283,2024-06-13
sector,last_5_sessions,lipi mutual funds | All other Sectors,1.723,2024-06-13
sector,last_5_sessions,lipi mutual funds | Cement,2.512,2024-06-13
sector,last_5_sessions,lipi mutual funds | Commercial Banks,1.82,2024-06-13
sector,last_5_sessions,lipi mutual funds | Debt Market,0.015,2024-06-13
sector,last_5_sessions,lipi mutual funds | Fertilizer,1.276,2024-06-13
sector,last_5_sessions,lipi mutual funds | Food and Personal Care Products,-0.231,2024-06-13
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,0.129,2024-06-13
sector,last_5_sessions,lipi mutual funds | Oil and Gas Marketing Companies,1.217,2024-06-13
sector,last_5_sessions,lipi mutual funds | Power Generation and Distribution,1.468,2024-06-13
sector,last_5_sessions,lipi mutual funds | Technology and Communication,1.122,2024-06-13
sector,last_5_sessions,lipi mutual funds | Textile Composite,-0.164,2024-06-13
sector,last_5_sessions,lipi nbfc | All other Sectors,-0.0,2024-06-13
sector,last_5_sessions,lipi nbfc | Cement,-0.057,2024-06-13
sector,last_5_sessions,lipi nbfc | Commercial Banks,-0.03,2024-06-13
sector,last_5_sessions,lipi nbfc | Fertilizer,-0.046,2024-06-13
sector,last_5_sessions,lipi nbfc | Food and Personal Care Products,-0.001,2024-06-13
sector,last_5_sessions,lipi nbfc | Oil and Gas Exploration Companies,-0.01,2024-06-13
sector,last_5_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.007,2024-06-13
sector,last_5_sessions,lipi nbfc | Power Generation and Distribution,-0.002,2024-06-13
sector,last_5_sessions,lipi nbfc | Technology and Communication,-0.002,2024-06-13
sector,last_5_sessions,lipi nbfc | Textile Composite,-0.011,2024-06-13
sector,last_5_sessions,lipi other organization | All other Sectors,-0.219,2024-06-13
sector,last_5_sessions,lipi other organization | Cement,-0.418,2024-06-13
sector,last_5_sessions,lipi other organization | Commercial Banks,-0.191,2024-06-13
sector,last_5_sessions,lipi other organization | Debt Market,0.709,2024-06-13
sector,last_5_sessions,lipi other organization | Fertilizer,0.082,2024-06-13
sector,last_5_sessions,lipi other organization | Food and Personal Care Products,0.001,2024-06-13
sector,last_5_sessions,lipi other organization | Oil and Gas Exploration Companies,-1.454,2024-06-13
sector,last_5_sessions,lipi other organization | Oil and Gas Marketing Companies,0.057,2024-06-13
sector,last_5_sessions,lipi other organization | Power Generation and Distribution,0.094,2024-06-13
sector,last_5_sessions,lipi other organization | Technology and Communication,0.181,2024-06-13
sector,last_5_sessions,lipi other organization | Textile Composite,0.038,2024-06-13
investor_type,last_20_sessions,banks / dfi,5.57,2024-06-13
investor_type,last_20_sessions,broker proprietary trading,-7.63,2024-06-13
investor_type,last_20_sessions,companies,-2.007,2024-06-13
investor_type,last_20_sessions,foreign corporates,0.251,2024-06-13
investor_type,last_20_sessions,foreign individual,-0.094,2024-06-13
investor_type,last_20_sessions,individuals,-21.964,2024-06-13
investor_type,last_20_sessions,insurance companies,26.06,2024-06-13
investor_type,last_20_sessions,mutual funds,3.763,2024-06-13
investor_type,last_20_sessions,nbfc,-0.225,2024-06-13
investor_type,last_20_sessions,other organization,-1.606,2024-06-13
investor_type,last_20_sessions,overseas pakistani,-4.692,2024-06-13
sector,last_20_sessions,fipi | All other Sectors,1.251,2024-06-13
sector,last_20_sessions,fipi | Cement,1.603,2024-06-13
sector,last_20_sessions,fipi | Commercial Banks,12.587,2024-06-13
sector,last_20_sessions,fipi | Debt Market,-16.551,2024-06-13
sector,last_20_sessions,fipi | Fertilizer,-0.161,2024-06-13
sector,last_20_sessions,fipi | Food and Personal Care Products,-0.395,2024-06-13
sector,last_20_sessions,fipi | Oil and Gas Exploration Companies,-3.516,2024-06-13
sector,last_20_sessions,fipi | Oil and Gas Marketing Companies,-0.494,2024-06-13
sector,last_20_sessions,fipi | Power Generation and Distribution,1.607,2024-06-13
sector,last_20_sessions,fipi | Technology and Communication,-0.683,2024-06-13
sector,last_20_sessions,fipi | Textile Composite,0.217,2024-06-13
sector,last_20_sessions,lipi banks / dfi | All other Sectors,3.315,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Cement,-1.123,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,-14.504,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Debt Market,16.586,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-1.438,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Food and Personal Care Products,-0.192,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Exploration Companies,10.815,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Oil and Gas Marketing Companies,-0.421,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Power Generation and Distribution,-4.878,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Technology and Communication,-2.298,2024-06-13
sector,last_20_sessions,lipi banks / dfi | Textile Composite,-0.291,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | All other Sectors,-3.097,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Cement,0.059,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Commercial Banks,-1.73,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Debt Market,-0.21,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Fertilizer,-0.562,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Food and Personal Care Products,-0.21,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Exploration Companies,-1.809,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Oil and Gas Marketing Companies,0.117,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Power Generation and Distribution,-0.042,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Technology and Communication,-0.157,2024-06-13
sector,last_20_sessions,lipi broker proprietary trading | Textile Composite,0.011,2024-06-13
sector,last_20_sessions,lipi companies | All other Sectors,-3.209,2024-06-13
sector,last_20_sessions,lipi companies | Cement,-1.216,2024-06-13
sector,last_20_sessions,lipi companies | Commercial Banks,5.197,2024-06-13
sector,last_20_sessions,lipi companies | Debt Market,-0.965,2024-06-13
sector,last_20_sessions,lipi companies | Fertilizer,1.291,2024-06-13
sector,last_20_sessions,lipi companies | Food and Personal Care Products,0.161,2024-06-13
sector,last_20_sessions,lipi companies | Oil and Gas Exploration Companies,-5.673,2024-06-13
sector,last_20_sessions,lipi companies | Oil and Gas Marketing Companies,-1.257,2024-06-13
sector,last_20_sessions,lipi companies | Power Generation and Distribution,-1.583,2024-06-13
sector,last_20_sessions,lipi companies | Technology and Communication,4.487,2024-06-13
sector,last_20_sessions,lipi companies | Textile Composite,0.76,2024-06-13
sector,last_20_sessions,lipi individuals | All other Sectors,-1.396,2024-06-13
sector,last_20_sessions,lipi individuals | Cement,-5.581,2024-06-13
sector,last_20_sessions,lipi individuals | Commercial Banks,-7.475,2024-06-13
sector,last_20_sessions,lipi individuals | Debt Market,0.007,2024-06-13
sector,last_20_sessions,lipi individuals | Fertilizer,-4.637,2024-06-13
sector,last_20_sessions,lipi individuals | Food and Personal Care Products,0.886,2024-06-13
sector,last_20_sessions,lipi individuals | Oil and Gas Exploration Companies,0.128,2024-06-13
sector,last_20_sessions,lipi individuals | Oil and Gas Marketing Companies,0.425,2024-06-13
sector,last_20_sessions,lipi individuals | Power Generation and Distribution,-0.855,2024-06-13
sector,last_20_sessions,lipi individuals | Technology and Communication,-4.003,2024-06-13
sector,last_20_sessions,lipi individuals | Textile Composite,0.536,2024-06-13
sector,last_20_sessions,lipi insurance companies | All other Sectors,1.36,2024-06-13
sector,last_20_sessions,lipi insurance companies | Cement,1.885,2024-06-13
sector,last_20_sessions,lipi insurance companies | Commercial Banks,8.95,2024-06-13
sector,last_20_sessions,lipi insurance companies | Debt Market,-0.0,2024-06-13
sector,last_20_sessions,lipi insurance companies | Fertilizer,6.146,2024-06-13
sector,last_20_sessions,lipi insurance companies | Food and Personal Care Products,0.032,2024-06-13
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,3.802,2024-06-13
sector,last_20_sessions,lipi insurance companies | Oil and Gas Marketing Companies,0.561,2024-06-13
sector,last_20_sessions,lipi insurance companies | Power Generation and Distribution,4.973,2024-06-13
sector,last_20_sessions,lipi insurance companies | Technology and Communication,-0.204,2024-06-13
sector,last_20_sessions,lipi insurance companies | Textile Composite,-1.445,2024-06-13
sector,last_20_sessions,lipi mutual funds | All other Sectors,0.837,2024-06-13
sector,last_20_sessions,lipi mutual funds | Cement,4.292,2024-06-13
sector,last_20_sessions,lipi mutual funds | Commercial Banks,-2.264,2024-06-13
sector,last_20_sessions,lipi mutual funds | Debt Market,-0.269,2024-06-13
sector,last_20_sessions,lipi mutual funds | Fertilizer,-0.278,2024-06-13
sector,last_20_sessions,lipi mutual funds | Food and Personal Care Products,-0.09,2024-06-13
sector,last_20_sessions,lipi mutual funds | Oil and Gas Exploration Companies,-2.521,2024-06-13
sector,last_20_sessions,lipi mutual funds | Oil and Gas Marketing Companies,0.992,2024-06-13
sector,last_20_sessions,lipi mutual funds | Power Generation and Distribution,1.446,2024-06-13
sector,last_20_sessions,lipi mutual funds | Technology and Communication,1.457,2024-06-13
sector,last_20_sessions,lipi mutual funds | Textile Composite,0.159,2024-06-13
sector,last_20_sessions,lipi nbfc | All other Sectors,-0.033,2024-06-13
sector,last_20_sessions,lipi nbfc | Cement,-0.031,2024-06-13
sector,last_20_sessions,lipi nbfc | Commercial Banks,-0.258,2024-06-13
sector,last_20_sessions,lipi nbfc | Fertilizer,0.149,2024-06-13
sector,last_20_sessions,lipi nbfc | Food and Personal Care Products,-0.001,2024-06-13
sector,last_20_sessions,lipi nbfc | Oil and Gas Exploration Companies,0.042,2024-06-13
sector,last_20_sessions,lipi nbfc | Oil and Gas Marketing Companies,-0.037,2024-06-13
sector,last_20_sessions,lipi nbfc | Power Generation and Distribution,-0.027,2024-06-13
sector,last_20_sessions,lipi nbfc | Technology and Communication,-0.032,2024-06-13
sector,last_20_sessions,lipi nbfc | Textile Composite,0.002,2024-06-13
sector,last_20_sessions,lipi other organization | All other Sectors,0.122,2024-06-13
sector,last_20_sessions,lipi other organization | Cement,-0.25,2024-06-13
sector,last_20_sessions,lipi other organization | Commercial Banks,-1.119,2024-06-13
sector,last_20_sessions,lipi other organization | Debt Market,1.402,2024-06-13
sector,last_20_sessions,lipi other organization | Fertilizer,-0.567,2024-06-13
sector,last_20_sessions,lipi other organization | Food and Personal Care Products,-0.147,2024-06-13
sector,last_20_sessions,lipi other organization | Oil and Gas Exploration Companies,-1.672,2024-06-13
sector,last_20_sessions,lipi other organization | Oil and Gas Marketing Companies,0.049,2024-06-13
sector,last_20_sessions,lipi other organization | Power Generation and Distribution,-0.68,2024-06-13
sector,last_20_sessions,lipi other organization | Technology and Communication,1.135,2024-06-13
sector,last_20_sessions,lipi other organization | Textile Composite,0.123,2024-06-13

=== FILE: calendar.md ===
# Calendar as of 2024-06-14

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2024-05-17 HCAR: Board of Directors Meeting & Close Period
- 2024-05-22 KEL: Board Meeting Other Than Financial Results
- 2024-05-23 GTYR: Board Meeting Other than Financial Results
- 2024-05-24 KEL: Board Meeting Other Than Financial Results
- 2024-05-27 PRL: Board Meeting other than Financial Results
- 2024-05-31 PRL: Board Meeting Rescheduled
- 2024-05-31 KEL: Board Meeting Other Than Financial Results
- 2024-06-03 TOMCL: Board Meeting Other Than Financial Results
- 2024-06-06 FCCL: Board Meeting Other Than Financial Results
- 2024-06-07 BGL: Board Meeting Other Than Financial Results
- 2024-06-12 NRL: Board Meeting Other Than Financial Results
- 2024-06-13 ATRL: BOARD MEETING OTHER THAN FINANCIAL RESULTS
- 2024-06-14 ACPL: Board Meeting other than Financial Results.
- 2024-06-14 INIL: Board Meeting Other Than Financial Results
- 2024-06-14 CHCC: Board Meeting Other Than Financial Results
- 2024-06-14 TPLP: Board Meeting Other Than Financial Results

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
| 10 | K-Electric to Shanghai Electric | PAI 27 Mar 2018 | outcome not shown |
| 11 | OGDC 7%, PPL 10% sale | CCoP 21 Aug 2020 | outcome not shown |
| 12 | Six SOEs sold in FY20 | 29 Jan 2020 | outcome not shown |
| 15 | Rs170bn mini-budget | 10 Feb 2023 | outcome not shown |
| 17 | GIDC recovery | SC Aug 2020 | outcome not shown |
| 18 | End subsidised RLNG to fertilizer | 2023 | outcome not shown |
| 19 | Exporter power tariff Rs19.99 | 6 Oct 2022 | outcome not shown |

=== FILE: situations.md ===
(no situation-library entry has an outcome that closed before this date, or the library has no INDEX.md)

=== FILE: base_rates.csv ===
type,as_of_cutoff,n,hit_rate,median,p50plus,source
none,,,,,,no base rates available
=== END ===
