# Retrospective: the 2026 refiner and steel moves

Written 2026-10-17. Question: when did PRL, ATRL, NRL, CNERGY and the steel names move, what public information existed before the move, and could a weekly catalyst watch have flagged it? The playbook drawn from this is `knowledge/playbooks/catalyst_trade.md`.

## Method

- Prices: `seed/data/prices/{SYM}.csv`, raw closes. ATRL, ISL and INIL come from `data/prices_raw/` because the seed files `ATRLXD`, `ISLXD`, `INILXD` are empty (lesson 14). A daily move beyond ±10.5% that is also more than Rs1 is treated as a corporate action and zeroed. None was found in any of these names since June 2025 (BECO had one on 2025-11-17).
- Market proxy: equal-weight mean of the daily returns of all 378 seed tickers that have prices, each clipped at ±10%, compounded. "Relative" means (1 + stock return) / (1 + market return) − 1 over the same window, unless the table says "minus" (simple difference, used for the 20 and 60-day grids).
- Filings: PSX announcement archive for each symbol, 2025-10-01 to 2026-09-10 (POST `/announcements` with `symbol=`, see `scripts/fetch_announcements.py`), PDFs read directly. Web: ProPakistani and Dawn pages fetched by URL. The web search budget was used up before this session's first search, so broker notes (Topline, AHL, JS, Intermarket, Optimus), Business Recorder (HTTP 403) and Mettis were not read. Anything sourced only from them is marked unverified.
- Scripts were run from the session scratchpad and are not saved in the repo. The logic is stated here so it can be rebuilt.

## 1. Price path

The market proxy fell 18.8% from 1 Jan to 2 Mar 2026 (Hormuz closed 28 Feb), rose 36.7% from 2 Mar to 6 Jul, and fell 6.8% from 6 Jul to 16 Oct.

### Refiners

| Name | 2026 low (date, Rs) | Base before launch | Launch | First peak (date, Rs) | 6 Jul to first peak, abs / rel | 6 Jul to 16 Oct, abs / rel | Max drawdown after 6 Jul |
|---|---|---|---|---|---|---|---|
| PRL | 2 Mar, 25.20 | Rs34-37 from 10 Apr to 6 Jul | 7 Jul (volume 15.6m vs 1.7m on 6 Jul, 48m on 8 Jul) | 2 Sep, 105.39 | +189% / +200% | +193% / +214% (new high 106.75 on 16 Oct) | −23.2% to 10 Sep |
| ATRL | 2 Mar, 679.73 | 875-975 from 24 Apr | 8 Jul | 31 Aug, 1,197.49 | +37% / +40% | +39% / +49% (high 1,219 on 16 Oct) | −10.4% to 7 Sep |
| NRL | 2-3 Mar, about 276-283 | 358-398 from 24 Apr | 9 Jul | 30 Sep, 596.18 | +60% / +71% | +79% / +92% (high 665 on 16 Oct) | −13.0% to 7 Sep |
| CNERGY | 2 Mar, 6.10 | 8.0-8.8 from 24 Apr | 9 Jul | 31 Aug, 15.46 | +82% / +86% | +51% / +62% (12.85, 17% off peak) | −21.0% to 5 Oct |

What the March-to-July leg looked like: PRL +44.6% from 2 Mar to 6 Jul against a market up 36.7%, so only +5.8% relative. From the day the last March-quarter result came out (29 Apr) to 6 Jul, the four refiners lost 16 to 22 points relative to the market. The record quarter was ignored for ten weeks.

The "+149% in 3 months" in the question matches PRL from 9 Jul (41.85) to 16 Oct (106.75): +155% absolute, +171% relative.

### Steel

There was no steel sector rally. Only Aisha Steel (ASL) and, briefly, Amreli (ASTL) moved.

| Name | Low | Peak | Low to peak, abs / rel | 16 Oct vs peak | 60-day rel at 16 Oct |
|---|---|---|---|---|---|
| ASL | 19 Mar, 9.00 | 9 Sep, 17.83 | +98% / +54% | −15.3% | +22.6 pts |
| ASTL | 15 Sep, 14.86 | 23 Sep, 19.98 | +34% / +31% (one week, after FY26 results on 16 Sep) | −10% | +17.8 pts |
| ISL | 2026 high 5 Jan (113.9) | best 3-month window 31 Mar to 6 Jul, +40% abs, +1.8% rel | | −30.6% | −0.5 pts |
| MUGHAL | 2026 high 2 Jan (104.9) | same window, +46% abs, +6% rel | | −37.3% | −14.9 pts |
| AGHA, ITTEFAQ, INIL, BECO, CSAP, DSL | 2026 highs in Jan or early July | | | −22% to −45% | −3 to −15 pts |

ASL ran in two legs: 19 Mar to 17 Apr (9.00 to 12.37, +37% abs, +20% rel) and 13 Aug to 9 Sep (13.90 to 17.83, +28% abs, +33% rel).

### 20-day and 60-day returns, stock minus market (percentage points)

| Date | PRL 20d | PRL 60d | ATRL 20d | ATRL 60d | NRL 20d | NRL 60d | CNERGY 20d | CNERGY 60d | ASL 20d | ASL 60d | Market 20d / 60d (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 Mar | +8.6 | −5.2 | +7.9 | +28.4 | +0.9 | −10.4 | +0.2 | +6.4 | −6.5 | −10.2 | −8.1 / −19.3 |
| 30 Apr | +9.4 | +4.5 | +1.6 | +14.5 | +3.8 | −5.5 | +7.6 | +16.9 | +15.3 | −4.5 | +10.7 / −9.4 |
| 29 May | −10.7 | +11.2 | −9.9 | +4.1 | −5.9 | +4.1 | +1.1 | +5.4 | +1.3 | +0.4 | +2.8 / +9.7 |
| 30 Jun | −7.4 | −3.9 | −14.6 | −19.0 | −13.1 | −5.2 | −12.7 | −5.9 | −3.8 | +9.5 | +10.4 / +33.7 |
| 10 Jul | +11.9 | −6.6 | −4.4 | −21.4 | +0.7 | −15.0 | +9.4 | +2.9 | −9.8 | −5.2 | +9.6 / +26.1 |
| 17 Jul | +17.7 | +11.3 | −4.1 | −12.1 | −0.1 | −3.4 | +13.2 | +15.3 | −5.1 | −11.4 | +2.2 / +15.8 |
| 31 Jul | +68.3 | +49.5 | +13.2 | −12.3 | +20.5 | +0.7 | +31.7 | +14.4 | +1.9 | −3.6 | −2.6 / +17.9 |
| 13 Aug | +82.6 | +102.3 | +14.2 | +2.5 | +28.1 | +19.7 | +40.6 | +40.2 | +9.2 | +0.9 | +1.6 / +15.3 |
| 31 Aug | +82.7 | +186.5 | +21.7 | +24.1 | +24.7 | +37.2 | +44.0 | +74.6 | +9.3 | +1.6 | +1.7 / +11.5 |
| 15 Sep | +5.4 | +125.5 | +6.0 | +23.6 | +5.0 | +36.7 | −7.7 | +52.7 | +17.0 | +28.1 | −7.0 / −2.0 |
| 30 Sep | −9.0 | +161.4 | +4.3 | +41.5 | +16.4 | +66.3 | −7.7 | +60.6 | +18.2 | +32.2 | −2.8 / −6.2 |
| 16 Oct | +29.5 | +112.1 | +12.2 | +35.6 | +29.1 | +64.4 | +0.3 | +32.3 | −10.4 | +22.6 | −0.9 / −2.2 |

Volume: PRL's 10-day over 120-day average volume first exceeded 2x on 27 Apr and peaked at 3.6x on 21 Jul. NRL first exceeded 2x on 21 Jul. ATRL never exceeded 1.5x. ASL first exceeded 2x on 13 Aug and peaked at 3.7x on 15 Sep.

## 2. Timeline: what was public, and when

Price is the adjusted close on that date. "Doc" is the PSX document id (`https://dps.psx.com.pk/download/document/{id}.pdf`).

| Date | Datapoint | Source | PRL | ASL |
|---|---|---|---|---|
| 28 Feb 2026 | Strait of Hormuz closed; Iran war | `knowledge/sectors/exploration_production.md` (Wikipedia, 2026 Strait of Hormuz campaign) | 28.0 | 10.9 |
| 27 Feb to 3 Apr | Brent $71.3 to $127.6 (weekly closes) | FRED DCOILBRENTEU, `data/macro/brent.csv` | | |
| 7 Apr | Arif Habib Corp (sponsor) buys 39.28m ASL at Rs9.78, taking it to 15.67% of ordinary shares. Letter dated 8 Apr, on PSX 9 Apr 10:24 | doc 273850 | | 9.82 → 10.82 on 8 Apr |
| 21 Apr | PRL March quarter: profit Rs9.94bn, EPS Rs15.78 vs −4.09; 9M EPS 19.17. Nil dividend | doc 274659 | 38.84 | |
| 22-23 Apr | ATRL shuts its 32,400 bpd main crude unit because tank lorry movement around Islamabad was suspended; resumes next day | docs 274758, 274961 | | |
| 27 Apr | SBP raises policy rate 100bp to 11.5% | `data/macro/policy_rate_decisions.csv` | | |
| 28 Apr | CNERGY March quarter: unconsolidated profit Rs17.7bn, EPS 3.22 (9M EPS 2.68 vs −0.50) at a price of about Rs8 | doc 275538 (text extraction, figures as printed) | | |
| 28 Apr | ASL 9M FY26: profit Rs99m vs loss Rs1.39bn; sponsor contributed a further Rs6.92bn of equity in 9M | doc 275493 | | 11.62 |
| 29 Apr | NRL March quarter: profit Rs7.30bn vs loss Rs2.76bn; 9M Rs9.07bn. About Rs91 a share on 79.97m shares (my arithmetic) at a price of Rs382 | doc 275684 | | |
| 29 Apr | ATRL March quarter EPS Rs106.41 vs 15.97 (refinery 102.68); 9M EPS 153.49 | doc 275863 | 37.23 | |
| May to 2 Jul | Brent falls from about $118 (1 May) to $68.5 (2 Jul): March-quarter inventory gains reverse in April to June | `data/macro/brent.csv` | 34-37 | |
| 21 May | Sponsor buys 27.0m ASL at Rs12.27, taking it to 18.44% (letter 25 May) | doc 277816 | | 12.18 |
| 26 May | Government considering a windfall tax on oil-sector profits (Rs72bn under section 99D); not enacted as of Oct | `knowledge/sectors/omc.md` (dailytimes.com.pk/1499116) | | |
| 2 Jul | Fuel levies recast | `knowledge/sectors/omc.md` (Profit, 2 Jul) | 36.08 | |
| 7 Jul | PRL volume 15.6m vs 1.7m the day before; Brent +3.2% to $71.8 | price file; FRED | 37.25 | |
| 8 Jul | Trump declares the Iran ceasefire over after new strikes; Brent +6% to $78.58; KSE-100 −2.48%, PRL +3.2% and CNERGY +2.7% on that day | propakistani.pk/2026/07/08/oil-gains-6-after-trump-violates-iran-truce-again/ ; propakistani.pk/2026/07/08/psx-plunges-below-182000-after-us-iran-war-returns/ | 38.43 | |
| 13 Jul | Refining policy "fast-tracked" | `knowledge/sectors/refineries.md`; primary source unverified | 42.73 | |
| 14-15 Jul | Hormuz blockade reinstated | `knowledge/sectors/exploration_production.md` | | |
| 21 Jul | Daily fuel pricing begins | `knowledge/sectors/omc.md` | 49.19 | |
| 28 Jul | Cabinet Committee on Energy (PM chairing) approves the Brownfield Petroleum Refining Policy 2026 after a seven-year deadlock | Dawn, 25 Sep 2026, dawn.com/news/2032467 | 59.15 | |
| 30 Jul | PRL replies to PSX that it knows of no undisclosed information behind the price move | doc 280561 | 57.4 | |
| 3-4 Aug | Sponsor buys 26.8m ASL at Rs13.53-13.78, taking it to 21.19% of ordinary shares (24.79% with preference shares). Letter 5 Aug | doc 280799 | | 13.60 |
| 13 Aug | PRL FY26 results (EPS 25.05, no dividend) | doc 281136 | 76.73 | |
| 19 Aug | ASL FY26 results; preference dividend arrears for Jul 2022 to Jun 2026 declared | doc 281323 | | 15.29 |
| 20 Aug | Diesel crack cap $41.89/bbl takes effect | propakistani.pk/2026/09/02/... | | |
| 2 Sep | July GRM $36.7, August $28.8 (first month above $20 was July, by the article's wording) | propakistani.pk/2026/09/02/pakistan-refineries-profit-margins-jump-more-than-fivefold-in-a-year/ | 105.39 | |
| 10 Sep / 24 Sep | Policy notified; four refiners sign upgrade agreements | `seed/FORECAST_REGISTER.md`; Dawn 2032467 | | |

**Not found (search budget):** Topline or AHL monthly GRM for April to June 2026, broker preview notes before July, any deemed duty change before August, refiner insider trades before September (PRL's insider filings are dated 22 and 24 Sep, after the move), and Pakistani HRC or scrap prices for March to September. Steel context from `knowledge/sectors/steel.md`: Chinese HRC $505-540/t CFR (25 Mar), CR coil anti-dumping duty extended five years from 13 Jan 2026, PKR drifting from 280.3 to 277.4 between Dec and Sep (SBP). None of these changed in the weeks before ASL's legs.

## 3. Verdict

**Refiners.** The setup could be flagged on 29 Apr 2026, when the last of the four March-quarter results came out. PRL at Rs37 was about 1.9x trailing EPS of Rs19.06 (9M 19.17 plus the June 2025 quarter's −0.11). ATRL's single quarter was 11% of its price, NRL's about 24%, and CNERGY's about 38%. The market discounted this as a one-off inventory gain from the March oil spike, and it was partly right: Brent then halved, and the stocks lost 16 to 22 points relative to the market over ten weeks. The trigger was renewed war (8 Jul), followed by policy approval (28 Jul). Neither was datable in advance. The policy had been stuck for seven years, so nobody could have counted on approval that month.

A watch would have caught most of the move on a reaction rule: Brent turning up more than 10% off its low, plus refiner volume above 5x, plus refiners rising on a day the market fell. That rule fired on 8-9 Jul. Entry at the 9 Jul close against 16 Oct: PRL +155%, NRL +70%, ATRL +34%, CNERGY +37% (+64% at its peak). Entry after the 28 Jul approval still gave PRL +81% and NRL +53%. So the move was flaggable without hindsight as a watchlist item from 29 Apr and as a trade from 9 Jul. Its size (PRL tripling) was only knowable with hindsight.

**ASL.** This was a sponsor-accumulation trade, not a steel-cycle trade, and it was knowable. The sponsor bought at Rs9.78 (7 Apr), Rs12.27 (21 May) and Rs13.5-13.8 (3-4 Aug), and had injected Rs6.9bn of equity by March. Each purchase was public within one to two days. Buying at the 9 Apr disclosure close (10.97) returned +62% to the peak and +38% to today. Buying on the 5 Aug disclosure (13.60) returned +31% to the 9 Sep peak, before the 19 Aug results. Steel prices, duties and PKR explain neither leg.

**Odds.** These are measured on one episode each, so they are thin.

- **Reaction rule, all stocks 2017-2026.** The signal was 10-day over 120-day volume above 2.5x, a 20-day return above +15%, and liquidity above Rs20m a day, with the first signal per name per 120 days. Over 60 days: n = 788 (219 names), median −3.4%, mean +3.6%, win rate 45%, worst −64%, and 6.1% of cases above +50%. The placebo was 4,588 random liquid days in the same names, with median −6.9%, mean −3.6%, win rate 36%, worst −80%, and 3.5% of cases above +50%. Against the market, the median was −8.3% (placebo −9.5%) and the win rate 33% (placebo 29%). Alone, the rule is a weak edge. PRL fired it on 14 Jul and went on to make +117% over the next 60 days.
- **With the fundamental filter.** Adding the requirement of a blowout quarter that the price ignored leaves too few cases to measure. My judgment, not a measured figure: about 1 in 3 for a move above +50% within six months, once the spread, policy and volume conditions all line up.
- **Sponsor buying.** A base rate has not been tested. The data exists: `data/announcements.csv` classifies insider trades, but the documents need parsing. This is the next test to run.
