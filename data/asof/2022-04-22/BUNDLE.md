# Replay bundle, close of 2022-04-22

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
# Market as of 2022-04-22 close (public information only)

- KSE100: 45,553 on 2022-04-22; 1m +4.7%, 3m +1.4%, 6m -0.5%, 12m +0.5%
- KMI All Share: 22,566 on 2022-04-22; 1m +4.9%, 3m +1.8%, 6m +1.2%, 12m +2.1%
- Policy rate 12.25%; last MPC decision 2022-04-07: hike (+250bp)
- 6M T-bill cutoff 13.85% (auction 2022-04-20); 3M 13.50%, 12M 13.85%
- CPI YoY 12.71% for 2022-03 (published by 2022-04-03); three months earlier (2021-12) 12.29%
- Brent: 105.15 USD/bbl on 2022-04-22; 3-month change +17.2%
- USD/PKR: 186.95  on 2022-04-22; 3-month change +6.1%
- FX reserves, current account: not available in this repository (no data file)
- Regime: 6M T-bill minus policy rate +1.60pp (market pricing hikes); CPI rising over 3 months (+0.4pp)
- Next MPC: see SBP calendar

Session date used: 2022-04-22. Liquid KMI names: 55 (membership KMI_ALL_derived_2022-01-03.csv).

=== FILE: sectors.csv ===
sector,n_names,r1m,r3m,r6m,n_at_252_high,n_within_2pct_of_high
Oil refineries,4,0.3471,0.09,-0.0426,0,0
E&P,3,0.0193,-0.0179,0.0182,0,0
OMC,3,0.0759,-0.0512,-0.13,0,0
Power,5,0.0214,-0.0155,0.0971,0,0
Fertilizer,4,0.0628,0.1491,0.2374,0,2
Cement,16,-0.0055,-0.0679,-0.1323,0,0
Steel & engineering,11,0.035,-0.0993,-0.2055,0,0
Autos,11,0.122,0.0044,-0.0817,0,2
Tech & telecom,8,0.1289,-0.0815,-0.0565,0,0
Islamic banks & fin.,8,0.0741,0.032,0.0076,0,1
Pharma,12,0.0308,-0.0385,-0.0666,0,0
Textiles,20,0.0367,-0.0249,-0.0378,0,0
Food & staples,14,-0.0019,-0.0642,-0.1406,0,0
Chemicals,16,0.0991,0.0629,-0.033,0,1
"Glass, packaging, paper",13,0.0904,-0.0133,-0.0839,0,1
Gas utilities & misc,10,0.0628,-0.023,-0.0925,1,1

=== FILE: screens.csv ===
symbol,close,r1m,r3m,r6m,r12m,dist_from_252_high,vol20_over_vol120,upper_locks_10d,eps_qtr_end,eps_yoy,n_results,n_material,n_insider_buy,n_insider_sell,pe,dy
AGHA,17.51,-0.039,-0.268,-0.389,-0.437,-0.514,1.146,0,,,0,0,0,0,,
ANL,13.41,0.192,0.073,-0.134,-0.623,-0.621,1.032,1,,,0,0,0,0,,
ASC,10.86,0.054,-0.263,-0.198,-0.255,-0.478,0.794,0,2021-12-31,,0,0,0,0,,
ASL,13.2,0.051,-0.133,-0.276,-0.491,-0.528,0.511,0,,,0,0,0,0,,
ATRL,162.09,0.359,0.132,-0.059,-0.379,-0.42,1.4,2,2022-03-31,,1,0,0,0,,
AVN,83.33,0.207,-0.019,-0.073,0.398,-0.255,0.999,1,2021-12-31,,2,0,0,0,,
CHCC,132.01,-0.054,-0.064,-0.08,-0.232,-0.314,0.972,0,2021-12-31,,0,0,0,0,,
CNERGY,6.66,0.308,0.078,-0.071,-0.335,-0.488,1.788,0,,,0,0,0,0,,
DGKC,68.86,0.037,-0.099,-0.172,-0.438,-0.475,1.336,1,2021-12-31,,0,0,0,0,,
EFERT,96.04,0.065,0.191,0.335,0.507,-0.01,1.103,0,2022-03-31,,1,0,0,0,,
EPCL,85.46,0.381,0.655,0.551,0.939,-0.02,1.81,2,2022-03-31,,1,2,0,0,,
FCCL,17.0,-0.05,-0.021,-0.05,-0.286,-0.307,1.503,0,2021-09-30,,0,0,0,0,,
FCEPL,80.0,-0.001,-0.133,-0.112,0.111,-0.356,0.573,0,2021-09-30,,3,0,0,0,,
FLYNG,9.2,-0.078,-0.187,-0.31,-0.324,-0.62,3.424,0,,,0,0,0,0,,
GAL,75.35,0.266,0.012,0.004,-0.263,-0.474,1.006,1,,,0,0,0,0,,
GGGL,14.78,0.436,0.129,-0.169,-0.147,-0.504,1.896,1,,,1,1,0,0,,
GGL,20.7,0.432,0.025,-0.341,-0.294,-0.537,1.585,3,2021-12-31,,0,2,0,0,,
GHNI,181.13,0.199,0.083,0.106,-0.311,-0.429,1.061,1,2021-12-31,,0,0,0,0,,
HCAR,198.7,0.039,-0.075,-0.119,-0.34,-0.494,0.704,0,2021-12-31,,0,0,0,0,,
HTL,44.66,0.117,-0.038,-0.163,-0.261,-0.38,0.746,0,,,0,0,0,0,,
HUBC,70.64,0.024,-0.044,-0.016,0.036,-0.08,0.738,0,2021-12-31,,0,0,0,0,,
ILP,71.3,-0.03,-0.051,-0.051,0.064,-0.112,0.713,0,2021-12-31,,0,0,0,0,,
IMAGE,17.54,0.073,0.219,-0.085,0.222,-0.423,1.276,0,2021-12-31,,0,0,0,0,,
INIL,120.22,0.062,-0.11,-0.318,-0.46,-0.472,1.295,1,2021-12-31,,0,0,0,0,,
ISL,62.54,0.059,-0.106,-0.243,-0.32,-0.377,1.349,1,2022-03-31,,1,0,0,0,,
KEL,2.94,0.007,-0.048,-0.16,-0.222,-0.373,1.845,0,2021-12-31,-0.952,0,0,0,0,9.635,
KOHC,164.4,-0.002,-0.061,-0.087,-0.188,-0.299,0.731,0,2021-12-31,,0,0,0,0,,
KTML,67.22,0.118,0.12,-0.11,0.013,-0.242,1.647,0,2021-12-31,,1,0,0,0,,
LUCK,584.59,-0.001,-0.121,-0.182,-0.321,-0.379,0.81,0,2021-12-31,,0,0,0,0,,
MARI,1700.5,-0.014,-0.0,-0.01,0.083,-0.055,0.594,0,2021-12-31,,0,2,0,0,,
MEBL,141.03,0.112,0.04,0.043,0.555,-0.071,1.711,0,2021-12-31,,0,0,0,0,,
MLCF,35.42,0.023,0.063,-0.001,-0.231,-0.281,1.722,1,,,1,0,0,0,,
MTL,905.7,0.142,0.325,0.312,0.35,-0.012,0.818,0,2021-12-31,,0,0,0,0,,
MUGHAL,83.0,-0.03,-0.185,-0.077,0.016,-0.265,1.188,0,2021-12-31,,0,0,0,0,,
NETSOL,102.6,0.224,0.046,-0.051,-0.414,-0.468,0.666,3,2021-12-31,,0,1,0,0,,
NML,84.78,0.06,0.041,-0.014,-0.074,-0.193,0.787,0,2021-12-31,,0,0,0,0,,
NRL,259.53,0.334,0.026,-0.032,-0.556,-0.569,1.691,2,2022-03-31,,1,0,0,0,,
OGDC,85.44,0.026,-0.008,0.059,-0.066,-0.094,0.908,0,2021-12-31,,0,0,0,0,,
PAEL,18.58,0.222,-0.093,-0.293,-0.479,-0.494,2.059,2,2021-12-31,,2,0,0,0,,
PIBTL,6.68,0.108,-0.07,-0.204,-0.35,-0.444,1.391,1,2021-12-31,,0,0,0,0,,
PIOC,69.99,-0.029,-0.159,-0.194,-0.476,-0.486,0.869,1,2021-12-31,,0,0,0,0,,
PPL,76.14,0.045,-0.053,-0.01,-0.114,-0.197,0.838,1,2021-12-31,,0,0,0,0,,
PSO,167.16,0.061,-0.097,-0.103,-0.243,-0.313,1.151,0,2021-12-31,,0,0,0,0,,
PTC,7.7,0.023,-0.105,-0.146,-0.225,-0.444,0.731,0,,,2,0,0,0,,
SAZEW,80.81,0.115,-0.104,-0.316,-0.436,-0.477,1.363,2,2021-12-31,,0,0,0,0,,
SEARL,115.41,0.015,-0.153,-0.349,-0.381,-0.419,1.126,0,2021-12-31,,0,0,0,0,,
SGF,47.03,0.022,-0.03,0.063,,-0.263,1.192,0,2021-12-31,,2,0,0,0,,
SNGP,31.88,0.06,-0.048,-0.214,-0.234,-0.433,0.732,1,2021-12-31,,0,0,0,0,2.805,0.144
SYS,392.01,0.105,0.024,0.143,0.703,-0.05,1.699,0,2021-12-31,,1,1,0,0,,
TELE,15.29,0.472,-0.122,-0.091,0.212,-0.372,1.34,1,2021-06-30,,0,3,0,0,8.369,
TGL,127.35,0.028,0.034,0.416,0.662,-0.068,0.763,0,2021-12-31,,0,1,0,0,,
TREET,35.84,0.16,-0.086,-0.166,0.306,-0.418,1.386,1,2021-12-31,,0,2,0,0,,
UNITY,25.17,0.025,-0.076,-0.154,-0.173,-0.49,0.917,1,2021-12-31,0.094,0,0,0,0,13.56,
WAFI,117.08,0.048,-0.026,-0.147,-0.286,-0.369,0.827,0,,,0,0,0,0,,
WAVES,15.68,0.172,0.047,-0.122,-0.258,-0.425,1.246,1,2021-09-30,,0,2,0,0,,

=== FILE: announcements_30d.csv ===
date,symbol,klass,title
2022-04-01,TREET,material_info,Material Information
2022-04-04,TELE,material_info,Material Information
2022-04-04,IGIHL,material_info,Material Information
2022-04-04,KASBM,material_info,Material Information REVOKED
2022-04-04,KASBM,material_info,Material Information
2022-04-04,AWWAL,material_info,Material Information
2022-04-05,PMI,material_info,Material Information
2022-04-05,PAKMI,material_info,Material Information
2022-04-06,AASM,material_info,Material Information
2022-04-06,AABS,material_info,Material Information
2022-04-07,JSMFETF,material_info,Material Information
2022-04-07,NICL,material_info,Disclosure of Material Information
2022-04-08,GGGL,material_info,Material Information - GHANI GLOBAL GLASS LIMITED
2022-04-08,LOADS,material_info,Disclosure of Material Information
2022-04-08,JSMFETF,material_info,Material Information - Resumption of iNAV JSMFETF
2022-04-11,HINOON,material_info,Material Information
2022-04-11,POWER,material_info,MATERIAL INFORMATION
2022-04-11,NETSOL,material_info,Material Information
2022-04-11,UNIC,material_info,Material Information
2022-04-12,KML,material_info,Material Information
2022-04-14,LMSM,material_info,Disclosure of Material Information
2022-04-14,BRR,material_info,Material Information
2022-04-14,ARM,material_info,Material Information
2022-04-14,SZTM,material_info,Material Information
2022-04-14,TELE,material_info,Material Information
2022-04-14,MARI,material_info,Material Information
2022-04-14,GGL,material_info,MATERIAL INFORMATION - GHANI GLOBAL HOLDINGS LIMITED
2022-04-15,TPL,material_info,Material Information
2022-04-15,TPLI,material_info,Material Information
2022-04-15,PGLC,material_info,Material Information
2022-04-15,AWWAL,material_info,Material Information
2022-04-15,TREET,material_info,Material Information
2022-04-15,GGL,material_info,Material Information - GHANI GLOBAL HOLDINGS LIMITED
2022-04-18,WAVES,material_info,Material Information REVOKED
2022-04-18,WAVES,material_info,Material Information
2022-04-18,TGL,material_info,Material Information
2022-04-19,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2022-04-19,EPCL,material_info,DISCLOSURE OF MATERIAL INFORMATION
2022-04-20,SMBL,material_info,Disclosure of Material Information
2022-04-21,NICL,material_info,Disclosure of Material Information

=== FILE: flows.csv ===
kind,window,key,net_usd_mn,through
investor_type,last_5_sessions,banks / dfi,-1.103,2022-04-21
investor_type,last_5_sessions,broker proprietary trading,-0.032,2022-04-21
investor_type,last_5_sessions,companies,1.101,2022-04-21
investor_type,last_5_sessions,foreign corporates,-1.144,2022-04-21
investor_type,last_5_sessions,foreign individual,0.07,2022-04-21
investor_type,last_5_sessions,individuals,5.043,2022-04-21
investor_type,last_5_sessions,insurance companies,-0.405,2022-04-21
investor_type,last_5_sessions,mutual funds,-5.099,2022-04-21
investor_type,last_5_sessions,nbfc,-0.095,2022-04-21
investor_type,last_5_sessions,other organization,0.477,2022-04-21
investor_type,last_5_sessions,overseas pakistani,1.187,2022-04-21
sector,last_5_sessions,fipi | Commercial Banks,-1.616,2022-04-21
sector,last_5_sessions,fipi | Technology and Communication,1.075,2022-04-21
sector,last_5_sessions,lipi banks / dfi | Commercial Banks,1.187,2022-04-21
sector,last_5_sessions,lipi banks / dfi | Fertilizer,-3.181,2022-04-21
sector,last_5_sessions,lipi companies | All other Sectors,1.679,2022-04-21
sector,last_5_sessions,lipi companies | Commercial Banks,-1.777,2022-04-21
sector,last_5_sessions,lipi companies | Fertilizer,1.617,2022-04-21
sector,last_5_sessions,lipi individuals | Commercial Banks,2.338,2022-04-21
sector,last_5_sessions,lipi individuals | Fertilizer,0.956,2022-04-21
sector,last_5_sessions,lipi mutual funds | All other Sectors,-2.832,2022-04-21
sector,last_5_sessions,lipi mutual funds | Cement,-1.413,2022-04-21
sector,last_5_sessions,lipi mutual funds | Oil and Gas Exploration Companies,1.383,2022-04-21
investor_type,last_20_sessions,banks / dfi,8.676,2022-04-21
investor_type,last_20_sessions,broker proprietary trading,-3.847,2022-04-21
investor_type,last_20_sessions,companies,2.151,2022-04-21
investor_type,last_20_sessions,foreign corporates,-23.985,2022-04-21
investor_type,last_20_sessions,foreign individual,-0.064,2022-04-21
investor_type,last_20_sessions,individuals,47.883,2022-04-21
investor_type,last_20_sessions,insurance companies,-14.274,2022-04-21
investor_type,last_20_sessions,mutual funds,-27.415,2022-04-21
investor_type,last_20_sessions,nbfc,0.747,2022-04-21
investor_type,last_20_sessions,other organization,3.782,2022-04-21
investor_type,last_20_sessions,overseas pakistani,6.346,2022-04-21
sector,last_20_sessions,fipi | Commercial Banks,-22.552,2022-04-21
sector,last_20_sessions,fipi | Technology and Communication,5.669,2022-04-21
sector,last_20_sessions,lipi banks / dfi | Commercial Banks,8.792,2022-04-21
sector,last_20_sessions,lipi banks / dfi | Fertilizer,-5.292,2022-04-21
sector,last_20_sessions,lipi individuals | All other Sectors,12.966,2022-04-21
sector,last_20_sessions,lipi individuals | Cement,10.14,2022-04-21
sector,last_20_sessions,lipi individuals | Commercial Banks,4.969,2022-04-21
sector,last_20_sessions,lipi individuals | Technology and Communication,6.793,2022-04-21
sector,last_20_sessions,lipi insurance companies | Oil and Gas Exploration Companies,-4.981,2022-04-21
sector,last_20_sessions,lipi mutual funds | All other Sectors,-11.134,2022-04-21
sector,last_20_sessions,lipi mutual funds | Cement,-5.731,2022-04-21
sector,last_20_sessions,lipi mutual funds | Technology and Communication,-7.083,2022-04-21

=== FILE: calendar.md ===
# Calendar as of 2022-04-22

- Next MPC: see SBP calendar

## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)

- 2022-03-24 EPCL: BOARD MEETING (OTHER THAN FINANCIAL RESULTS)
- 2022-03-24 AVN: Board Meeting
- 2022-03-24 SGF: Board Meeting
- 2022-03-25 NETSOL: Board Meeting Other Than Financial Results
- 2022-03-29 KEL: Board Meeting Other Than Financial Results
- 2022-03-31 NETSOL: Board Meeting Rescheduled
- 2022-04-04 EFERT: Board Meeting for the announcement of the financial results for the first quarter ended March 31, 2022
- 2022-04-05 EFERT: Board Meeting Rescheduled
- 2022-04-05 PTC: Board Meeting
- 2022-04-05 KEL: Board Meeting Other Than Financial Results
- 2022-04-06 MARI: Notice of Board of Directors Meeting
- 2022-04-06 EPCL: Board Meeting for the announcement of the financial results for the first quarter ended March 31, 2022
- 2022-04-06 FLYNG: Board Meeting Other Than Financial Results REVOKED
- 2022-04-07 FLYNG: Board Meeting Other Than Financial Results
- 2022-04-07 FCEPL: Board Meeting 1st Quarter
- 2022-04-08 FLYNG: EXTRACT OF BOARD OF DIRECTORS MEETING
- 2022-04-11 ISL: BOARD MEETING
- 2022-04-12 MLCF: Board Meeting
- 2022-04-13 MEBL: NOTICE OF BOARD MEETING AND CLOSED PERIOD - MEEZAN BANK LIMITED
- 2022-04-13 INIL: Board Meeting
- 2022-04-13 KTML: Board Meeting
- 2022-04-14 NRL: Board Meeting
- 2022-04-15 CHCC: Board Meeting
- 2022-04-15 DGKC: BOARD MEETING
- 2022-04-15 HTL: Board Meeting
- 2022-04-18 PPL: Board Meeting and Closed Period
- 2022-04-18 SGF: Board Meeting
- 2022-04-18 MARI: Notice of Board of Directors Meeting
- 2022-04-18 TGL: Board Meeting
- 2022-04-18 LUCK: BOARD MEETING
- 2022-04-18 ILP: Notice of Board Meeting for the Third Quarter ended March 31, 2022 / Closed Period
- 2022-04-19 KOHC: Board Meeting
- 2022-04-19 IMAGE: Board Meeting
- 2022-04-19 SAZEW: Board Meeting
- 2022-04-19 TREET: Board Meeting
- 2022-04-19 HUBC: Intimation for Board Meeting - The Hub Power Company Limited
- 2022-04-20 GHNI: Board Meeting
- 2022-04-20 PPL: Board Meeting Rescheduled
- 2022-04-20 ANL: Board Meeting
- 2022-04-20 SYS: Board Meeting
- 2022-04-20 NML: BOARD MEETING
- 2022-04-20 UNITY: Board Meeting
- 2022-04-21 MTL: Board Meeting
- 2022-04-21 PSO: Board Meeting
- 2022-04-21 AVN: Board Meeting
- 2022-04-21 FLYNG: Board Meeting
- 2022-04-21 PIBTL: NOTICE OF PIBT BOARD MEETING - APRIL 28, 2022
- 2022-04-21 MUGHAL: Notice of Board Meeting - QIII - FY 2022
- 2022-04-21 SEARL: Board Meeting
- 2022-04-21 AGHA: Board Meeting
- 2022-04-21 ASL: BOARD MEETING / CLOSED PERIOD
- 2022-04-21 NETSOL: Board Meeting
- 2022-04-21 OGDC: Board meeting and closed period
- 2022-04-21 CNERGY: Board Meeting and Closed Period
- 2022-04-21 ASC: Board Meeting
- 2022-04-21 KEL: Board Meeting
- 2022-04-22 PIOC: Board Meeting
- 2022-04-22 PAEL: Board Meeting for the 1st Quarter ended March 31, 2022 (Un-Audited)
- 2022-04-22 TELE: Board Meeting

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
