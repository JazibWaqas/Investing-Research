# What PSX practitioners watch (signals to test)

Written 2026-10-17. Status: hypotheses, not findings. Nothing here has been backtested.

**Coverage warning.** The web search budget was exhausted before any search ran. Direct fetches of Business Recorder, SECP, MUFAP, SBP, Reddit and the broker sites returned 403, were blocked, or did not resolve. The Topline, AHL, JS Global, Optimus and Taurus strategy reports, the CFA Society and MUFAP material, and the forum threads were not read. What follows rests on Dawn, Tribune and Profit articles from 2025 to 2026, Wikipedia, and this repo's own data. Items marked "unverified" are author background with no retrievable source. A later session with search access should fill the gaps listed at the end.

## 1. What local institutions say drives PSX (ranked by how often cited, Oct 2026 sample)

The ranking comes from only about eight daily wrap articles (Aug to Oct 2026), so it describes the current regime and not PSX in general.

1. **Oil (Brent) and the Middle East.** Topline, 17 Oct 2026: "a lack of triggers and elevated crude oil prices" explain the range (Dawn 2037721; Tribune 2635305). KASB KTrade: elevated oil is "a key risk to market sentiment" (Tribune 2635095, 16 Oct). Brent was about $105 to 106. The Iran war began in Feb 2026, and the KSE-100 fell 9.57% on 2 Mar 2026 (Wikipedia KSE-100 page; secondary source).
2. **Policy rate path.** Tribune (17 Oct 2026) lists "expectations of a possible SBP policy rate hike" among drivers. Dawn (4 Jul 2026) listed "hopes of monetary easing" and flagged the SBP decision as a near-term risk. SBP raised 100bp to 11.5% on 27 Apr 2026 and has held since (`data/macro/policy_rate_decisions.csv`).
3. **Inflation and external account.** Dawn, 25 Aug 2026: August CPI expected near 11.1% against 3% a year earlier. Dawn, 17 Oct 2026: September current account deficit $356m, real effective exchange rate 108.93, the highest since May 2018.
4. **Earnings and results season.** KTrade said focus was shifting to September-quarter results (Tribune, 16 Oct). Dawn (17 Oct) blamed weak bank results, led by UBL (3Q profit down 13% YoY). Dawn (1 Aug) cited the ongoing earnings season.
5. **Institutional and foreign flows.** Tribune quotes NCCPL daily: foreigners net sold Rs194.4m on 16 Oct and Rs120m on 17 Oct. Dawn (16 Oct) names "institutional fund flows" with no figures. Brokers use these as sentiment colour, not as the cause of moves.
6. **IMF and ratings.** Staff-level agreement on the fourth EFF review reached early Oct 2026, about $1.2bn pending board approval (Profit, 17 Oct). Moody's upgrade to B3 around 25 Aug 2026 did not lift the index (Dawn, "PSX falls despite rating upgrade"). Rating news looks priced in.
7. **Geopolitics and politics.** AHL's Ali Najib: "geopolitical uncertainty and position-squaring ahead of the weekend" (Dawn, 17 Oct). Profit, 7 Oct 2025: profit-taking amid India tensions and flood-related GDP cuts (IMF discussed 3.5% growth).
8. **Index heavyweights.** Ten stocks added about 560 points on 16 Oct (Dawn). Points-contribution lists appear in every wrap, so index moves are often a handful of names.
9. **Budget, MTS leverage, fund inflows and redemptions, index rebalancing, MSCI.** Cited only in passing or not found. Profit (18 May 2026) quotes AKD Securities that Pakistan could re-enter MSCI EM if at least three stocks pass size and liquidity tests by 2027. MTS and MUFAP flows: no retrievable practitioner commentary.

Brokers' wrap language ("value-hunting", "profit-taking", "position-squaring", "lack of triggers") describes price action after the fact. Treat it as description, not prediction.

## 2. How informed capital is described (public record only)

Little of this is documented in sources I could read. What is on the record:

- **Broker proprietary books are large.** AKD Securities FY26 (to June) profit was Rs5.77bn, up 83%. Over half came in April to June 2026, from "booming trading activity" and a "substantial investment portfolio of its own" (Profit, 5 Oct 2026). Broker proprietary trading is a separate investor type in the NCCPL-derived data (`data/macro/fipi_lipi.csv`), so its net flow is measurable.
- **Opaque control changes.** Private Stock Holding bought 25.42% of Asia Insurance (PSX notice 9 Oct 2026). The notice said little about the buyer, and Profit (12 Oct) suggests the controlling family is behind it. Disclosure is thin and post-trade.
- **Structured IPOs.** Profit (12 Oct 2026, Khaadi): a partial sale lets owners cut risk while keeping upside. SECP (16 Oct 2026) halted the SE Fruits IPO over prospectus discrepancies and cited Securities Act 2015 sections 134 and 136 (false statements).
- **2008 precedent.** KSE-100 fell about 48% in two months; a price floor ran 28 Aug to 15 Dec 2008; broker clients defaulted (Wikipedia, KSE-100 and Arif Habib pages).
- **Hascol.** Price fell from over Rs300 (2018) to about Rs5 (2021) amid alleged falsified books and an FIA probe; NCCPL excluded it from eligible securities on 28 Jun 2021 (Wikipedia; allegations, not findings).
- **Not found:** documented cases of leaked results, pre-board-meeting positioning, or group-company support. These are widely believed locally (unverified). The testable part is price drift between a board-meeting notice and the result (`data/announcements.csv` holds notices with timestamps).

## 3. Calendar practitioners trade around

- **Budget (June).** Profit headlines show a run-up on "budget hopes" (29 May 2025, KSE-100 near 119,000; record 120,450 on 3 Jun 2025). The FY27 budget article (11 Jun 2026) mentions no investor tax measures, so no verified budget-reaction claim exists.
- **MPC.** 2026 decisions: 26 Jan, 9 Mar, 27 Apr, 15 Jun, 27 Jul, 14 Sep. Next date not found.
- **Results.** Q4 FY (June) results land late Jul to Sep (MLCF, Askari, reported 1 Aug 2026). September-quarter results: Oct to Nov. UBL reports on a calendar-year basis.
- **Dividends and book closures.** Data in `data/payouts_raw.csv`. A December season: unverified.
- **Index recompositions.** KMI30 notices in this repo cluster in June and December (`data/index_recomp_log.csv`; effective about 10 days later). The MSCI semi-annual review ran in May 2026 (HMBL added to Frontier); a November review is unverified.
- **Ramadan, Muharram, fiscal-year-end window dressing.** Unverified. Test from index data. AKD's April to June 2026 rebound is one data point, not evidence.
- **Settlement.** T+1 adopted 9 Feb 2026 (Wikipedia). Earlier return studies ran under T+2.

## 4. Technical conventions (hypotheses only)

- Named levels in wraps: resistance 167,000 to 168,000 (AHL via Tribune, 16 Oct 2026); range 164,000 to 168,000 (Dawn, 17 Oct); support 175,000 (Dawn, 25 Aug); record above 189,000 on 23 Jan 2026 (Dawn, 4 Jul).
- Round numbers: record 120,450 on 3 Jun 2025; on 2 Jun the index surged past 120,000 intraday then closed down 813 (Profit headlines). Rejection at round numbers is a recurring story. Test it.
- Volume confirmation: wraps compare volume with the previous day only. No standard.
- The daily price limit is plus or minus 10% (PSX snapshot 16 Oct 2026: DSIL +10.00%, MACFL -10.00%). Index halts occurred at -5.29% (8 Apr 2025) and on 2 Mar 2026 (Wikipedia).

## 5. Red flags for stocks to avoid

- **Penny-stock volume leaders.** On 16 Oct 2026 volume was led by Cnergyico (Rs12.80, 62.8m shares), WorldCall (Rs0.98, 19.5m) and K-Electric (Rs6.09, 28m on 17 Oct) (Tribune). Volume at low prices is retail speculation, not information. Hypothesis.
- **Opaque ownership or buyers** (Asia Insurance above). MSCI's proposed Indonesia downgrade cites "market transparency, ownership structures and trading practices" (Profit, 16 Oct 2026).
- **Partial-sale IPOs and weak audits** (Khaadi, SE Fruits).
- **Falsified books and default-list history** (Hascol).
- **Operator stocks, renamed shells, sponsor pledges, low free float:** no retrievable public source. Unverified.

## 6. Handoff table to the quant phase

Data: repo files under `data/` and `data/macro/`; endpoints in CLAUDE.md. Every test reports n, mean, median, win rate, worst case, uses point-in-time dates, and controls for the 2022 to 2025 rerating tailwind (lesson 9).

| Signal | Who cites | Measurable? | Data source | Proposed test |
|---|---|---|---|---|
| MPC decision (cut/hold/hike) | Dawn 4 Jul 2026; Tribune 17 Oct 2026 | Yes | https://www.sbp.org.pk/our-operations/publications/monetary-policy-statements/501 | KSE-100 and KMI30 returns, day -5 to +20 around the 84 announcements, by decision type |
| T-bill cut-off yield change | Implied by rate-path commentary | Yes | https://www.sbp.org.pk/assets/document/tb.xlsx | 4-week change in 6m yield vs next 20-day index return, by regime |
| Brent move | Topline, KTrade, AHL (Oct 2026) | Yes | FRED DCOILBRENTEU | Sector betas (E&P, OMC, refiners, banks, fertilizer) to 20-day Brent change; check asymmetry |
| PKR / REER | Dawn 17 Oct 2026 | Yes | SBP BFER archive (see data/macro/README.md) | Return after 3-month PKR depreciation vs not, per sector |
| FIPI net flow | Tribune daily (NCCPL) | Yes | https://scstrade.com/FIPILIPI.aspx (`fipi_lipi.csv`) | Decile of 5-day cumulative FIPI net vs next 5 and 20-day return; lead-lag with index |
| LIPI split: mutual funds, insurance, broker prop | Dawn "institutional fund flows"; Profit on AKD | Yes | same | Same test per type; does broker prop lead or fade? |
| Sector FIPI | Practitioner habit (unverified) | Yes | `fipi_lipi_by_sector.csv` | Sector excess return after 10-day foreign net buying |
| MTS leverage | Local belief (unverified) | Not yet; no history | scstrade MTS PDF (daily snapshot) | Log daily; test after 250 days |
| Pre-result drift | Local belief (unverified) | Yes | `data/announcements.csv`, PSX API | Return from board-meeting notice to result vs sector median |
| Results surprise | KTrade, Dawn | Partly; no consensus | PSX financial results | Use YoY and QoQ EPS change, lagged to announcement time |
| Dividend / book closure drift | Unverified | Yes | `data/payouts_raw.csv` | Run-up into book closure by yield bucket; December effect |
| Budget window (15 May to 30 Jun) | Profit 29 May 2025 | Yes | `data/macro/kse100.csv` | Window return across 10 years |
| Index adds/deletes | AKD on MSCI | Yes | `data/index_recomp_log.csv` | Announce-to-effective abnormal return, adds vs deletes |
| Calendar: Ramadan, Muharram, Dec | Unverified | Yes | `kse100.csv` plus Hijri calendar | Mean, median, win rate per period; n is small |
| Round-number rejection | Wraps (AHL) | Yes | `kse100.csv` | Return 10 days after first touch of each 5,000 multiple |
| Volume confirmation | Unverified | Yes | PSX API OHLCV | Breakouts with volume above 1.5x 20-day average vs not |
| Penny-stock volume leader | Tribune daily lists | Yes | PSX API | Top-5 volume names under Rs30: forward 5 and 20-day median return |
| Insider trades | KSEAlert feature; lesson 11 | Yes | https://ksealert.com (insider trades page) | Forward return after reported insider buys vs sells |
| Governance flags (SECP action, default list) | Profit, Wikipedia | Partly | PSX and SECP notices | Event study around NCCPL eligibility removal |

## Gaps for a later session

Read the Topline, AHL, JS Global, Optimus and Taurus strategy PDFs, MUFAP monthly flows, SECP market-manipulation orders, and the PSX rulebook (circuit breakers, MTS limits, index review rules). Search forums for "operator" and "pledge". Confirm December and MSCI November dates.
