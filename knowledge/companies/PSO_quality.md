# PSO quality score (Pakistan State Oil), 18 Oct 2026

Sources are PSX filings (document ids in brackets, under `data/raw/filings/quality/PSO/`): annual reports FY22 [193763], FY23 [216506], FY24 [238256], FY25 [260771], FY26 [284943], four corporate briefing decks [210513, 233128, 254990, 278695], CEO notices [273196, 273975, 275202]. Also `sa_ratios.csv` and press. The FY22 report is garbled, so FY22 claims are partial. `insider_trades.csv` has no PSO rows; `corporate_actions.csv` shows no rights issue.

## People
- **Sponsor is the state.** Government of Pakistan holds 22.47% directly and about 51% direct plus indirect [238256, p.19]. The board is ex-officio ministry nominees plus independents, run under the SOE Act 2023; CEOs are chosen by a Special Committee under CMU guidelines [284943].
- **CEO Jawwad Ahmed Cheema**, from 27 Apr 2026 (board approved 11 Apr, start date moved up from 18 May), three-year term [273975, 275202]. Ex-CEO Shell Pakistan, ex-CEO Karachi Hydrocarbon Terminal (VTTI), director of PRL and PAPCO. Six months in; no record at PSO.
- **Predecessor Syed Muhammad Taha**, Feb 2020 to Mar 2026. Standalone profit went from a Rs6.5bn loss (FY20) to Rs86bn (FY22) and Rs15bn (FY26) [238256, 284943]; the board says equity "more than doubled". He left for K-Electric (effective 15 Apr 2026, Profit, 16 Apr 2026). Interim CEO Abdus Sami served 31 Mar to 27 Apr [273196].
- Before Taha: the MD contract lapsed 31 Aug 2019, then seven CEO/MD notices in 11 months, including an acting MD from 30 Nov 2019 (announcements.parquet; Business Recorder). Chairman Asif Baigmohamed since May 2023.

## Promises against delivery
| Year | Promise | Outcome | Source |
|---|---|---|---|
| Aug 2022 | FEED for the PRL upgrade "by Q1 FY24" (garbled text) | Consultant engaged Aug 2023; FEED "by Dec 2024" (Aug 2024); PSO loan of Rs3.15bn approved 24 Oct 2024. Still no final investment decision in Sep 2026. Over a year late | [193763, 216506, 238256, 284943] |
| Aug 2023 | Hold MoGas and diesel share; volumes "to bounce back" | White oil share 51.6% FY24, 45.7% FY25, 42.7% FY26. Chairman blames trader-backed discounting. Re-promised in FY25 and FY26 | [238256, 260771, 284943] |
| Aug 2023 | LNG tripartite agreement with SNGPL and SSGC | FY24: "satisfactory resolution remains elusive". LNG receivable Rs276bn (Jun 2026) | [216506, 238256, 284943] |
| Aug 2023 | Storage to 1.23mt | 1.24mt by FY24. Kept | [216506, 238256] |
| 2023 to 2025 | Circular-debt "proposals under consideration"; receivable-equity swap (FY25) | Trade debts Rs496bn FY23, 488bn, 437bn, 415bn FY26. Falling slowly; no settlement. Swap wording dropped in FY26 | [216506, 260771, 284943] |
| Aug 2024 | Greenfield refinery (Aramco, Sinopec); white oil pipeline "FEED done, consortium next" | Greenfield absent from FY25 and FY26 reports (silent drop). Pipeline consortium "renewed", construction "planned FY2027" | [238256, 284943] |
| Sep 2025 | Borrowings Rs300 to 350bn in FY26 | Rs384bn at 30 Jun 2026, though finance cost fell 24% | [260771, 284943] |


## Capital decisions
- **PRL, 63.56%, cost Rs4.89bn** [238256]. At PRL's Rs107 (card, 17 Oct) the stake is about Rs43bn, but that is a 2025 to 26 crisis re-rating, not management skill. Upgrade (double to 100,000 bpd) has no FID; acquisition history unverified.
- Cerisma (fintech), PSO Renewable and PSO Venture Capital: about Rs2.6bn in by FY24, pilot stage, no earnings. APL (49%) and PAPCO (12%) are small.
- LNG import for SNGPL since 2015 piled up Rs276bn of receivables.
- ROE (sa_ratios): 52% FY22, 4% FY23, 8% FY24, 6% FY25, 11% FY26, below a cost of equity near 17%.

## Minorities
- Cash dividend every year but FY20. Standalone payout against EPS: FY22 Rs10 on Rs183.7 (5%, on a windfall year), FY23 Rs7.5 on 12.1, FY24 Rs10 on 33.8, FY25 Rs10 on 44.5, FY26 Rs10 on 32.1 [238256, 216506, 284943]. Flat Rs10 whatever the profit.
- No rights issue in the data, no dilution. PRL FEED loan was a related-party deal with a market-rate clause and equity-conversion option [238256, AGM 24 Oct 2024].
- Government risk sits on minorities: windfall recovery and margin tied to digitisation (card 17 Oct 2026).

## Disclosure
Annual report out 2 to 7 Oct every year, award-winning. Corporate briefing with deck each June, video since 2026. CEO exits filed same day. Interest on overdue debts is booked on receipt only, so surcharge is not in profit. Against: Rs371bn overdue with Rs347m specific provision [238256 audit matter]; resignation reasons withheld; FY22 report garbled.

## Growth engine
Nothing organic doubles earnings. Standalone profit is Rs15 to 21bn; a regulated Rs7.87/litre margin does not scale. Upside is policy: a Rs250bn receivable settlement saves roughly Rs30bn of pre-tax finance cost (my arithmetic, 12%), and the Rs1.22 margin adds about Rs9bn (card). Either could double standalone profit but PSO does not control either. The PRL upgrade is the only builder project, with no FID. What breaks it: windfall recovery, further share loss, a rate rise, the new CEO resetting strategy.

## Red flags
State control; receivables at 1.5 times equity; share down 9 points in two years; strategy items that quietly vanish; 2019 to 2020 and 2026 CEO churn; earnings swing from Rs86bn to Rs5.7bn on inventory (FY22 to FY23).

## Scores (0 to 5)
- Promises vs delivery 2: operations kept; share, LNG, FEED and borrowing promises missed.
- Capital allocation 2: PRL cheap but luck-driven; ROE below cost of equity; new ventures unproven.
- Minority treatment 2: steady but flat dividend, state priorities come first, policy risk lands on holders.
- Disclosure 4: timely, full reports, briefings; thin on reasons and what was dropped.
- **Overall 10 of 20.**
