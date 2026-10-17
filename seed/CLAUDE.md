# PSX Research Program: Brief for Claude Code

You are running a long, autonomous research session for a private investor in Karachi. Another Claude instance (the "orchestrator") has been working with him for several days and wrote this brief. You have no other context. Everything you need is here. When you finish, the user will carry your output files back to the orchestrator, so the deliverables in section 7 matter more than anything you say in chat.

Today is Saturday 17 October 2026. PSX reopens Monday 19 October.

**Repo contents to read first:** `LESSONS.md` (mistakes already made, don't repeat them), `DATA_README.md` (seed data: 528 tickers of daily prices, fundamentals for 115 KMI names, macro series, and the scripts behind every result in section 3), plus anything else the user drops in, such as `PSX_STATE.md` (the orchestrator's living state doc). Reuse the seed data to move fast, but refresh and adjust it where the brief says to.

Work autonomously. Use subagents freely and in parallel (one per sector works well). Don't stop to ask questions. Where something is ambiguous, make a sensible call, write the assumption down, and keep going.

---

## 1. The investor and the goal

- Pakistani retail investor, 22, CS graduate, sharp, high risk appetite. He owns his decisions and wants direct, confident advice with reasoning, not hedging.
- **Capital:** Rs50,000 now, another Rs50,000 in about 15 days, then about Rs50,000 a month.
- **Broker:** Finqalab app. Stocks only. No mutual funds, ETFs or money market funds. Idle cash sits in the brokerage account.
- **Mandate:** only stocks in the PSX KMI All Share Index (Shariah compliant). The current list is the 29 May 2026 recomposition, effective 5 June 2026: https://www.psx.com.pk/psx/files/?file=277899-1.pdf
- **Goal:** make real money fast. 10 to 15% a year is not worth it to him. He wants concentrated positions with 30%+ upside, holding periods that vary by trade (days to months), and he accepts big drawdowns. He aspires to 10 to 15% a month. The orchestrator's view: single trades can do that, a portfolio can't sustain it, and chasing that number leads to buying what's already flying, which tested badly (see 3). Don't flatter the aspiration and don't lecture him about it. Find the real high upside opportunities.
- **Evaluation horizon:** 1 year.
- **How he wants picks delivered:** like a broker talking to a client. For each stock: the story, why it's mispriced, what's coming and when (catalysts with dates), how much it could move, the odds, what kills it, and rupee outcomes on the actual share count. Include dividends expected in the next 12 months (ex dates usually fall in predictable months), net of 15% withholding tax.

## 2. Why this session exists

The orchestrator built a solid valuation and macro layer, but the user correctly called out that it doesn't yet understand how money is actually made on PSX. In particular, it missed the 2026 refiner rally (PRL roughly +149% in 3 months, ATRL and steel names like ASL also ran). That was a catalyst story (oil spike, widening refining margins, refinery policy approval) that a good local broker would have flagged in advance.

Your job is to build the missing understanding comprehensively, test what can be tested, and produce actionable picks for Monday onward.

## 3. What's already established (don't redo; challenge if you find errors)

Tests run by the orchestrator on 549 PSX tickers (daily prices from Oct 2016) and fundamentals for 115 liquid KMI names:

1. **Deep value works.** Ranking liquid KMI stocks by earnings yield plus dividend yield, measured 3 months after fiscal year end (to avoid lookahead), the cheapest third beat the most expensive third by about 28 pts/yr. Positive in 6 of 7 cohorts (2022 to 2025), rank IC 0.30. Earnings yield alone was stronger. Dividend yield alone was weak. Caveats: small cohorts (13 to 42 names), survivors only, 2022 to 2025 was a market wide rerating from 3 to 4x P/E, and the latest cohort (Oct 2025 to Oct 2026) was flat to negative.
2. **Rate cycle turns work.** After SBP rate cuts, the equal weight liquid market averaged +7% in 20 days, +17% in 60 and +33% in 120. After hikes, roughly 0. The first cut of a cycle was strongest (Mar 2020: +66% in 120 days; Jun 2024: +46%). The first hike was weak (2021: −22%).
3. **Sector rotation at turns.** After a first cut, Islamic banks lagged the market by about 48 pts and power by 42 to 46 pts over 6 months, both in 2020 and 2024. Leaders differed by cycle (2020: tech +126, cement, refiners, steel; 2024: OMC +107, fertilizer, pharma, E&P).
4. **Sector momentum works, stock momentum doesn't.** The top 3 of 14 sectors by trailing 6m return beat the bottom 3 by about 3.3% over the next 3 months, 67% of the time. Stock level momentum signals (big up days, volume spikes) showed a median 20 day excess return of −1.5% and a 43% win rate.
5. **Operator footprints and pump chasing fail.** Volume up 3x with flat price ("accumulation") gave a median 20 day excess of −1.8%. Breakouts after accumulation, −3.5%. Buying illiquid stocks after a +50% run in 20 days, a median 60 day excess of −14.9% with a 35% win rate. A few huge winners make it feel like a strategy. Most entrants lose.
6. **IMF staff level agreements:** no reliable short term market move.
7. **Current macro (16 Oct 2026):** policy rate 11.5% (hiked from 10.5% on 28 Apr 2026). 6M T-bill 12.40%, so the curve prices further hikes. CPI 10.3% (Sep), roughly flat. Next MPC is **26 Oct 2026**. IMF staff level agreement on the 4th EFF review was reached 8 Oct 2026, with board approval pending. KSE100 is around 166,000, near highs. Brent is about $104.
8. **Current 6m sector momentum:** refinery +129% (stretched), steel +17%, Islamic banks +8%, autos +3%, fertilizer 0, E&P 0, cement −1, OMC −4, power −6, chemicals −7, pharma −8, tech −8, textiles −13, food −17.

**Companies already underwritten.** Treat these as inputs to challenge, not gospel:
- **HUBC** (Rs193): about 5x consolidated earnings, FY27 DPS of about Rs17 (8.8% yield). Main risks: the CPHGC tariff true up dispute, and its consortium (with Lucky, Kohat, Metro) shortlisted for the GEPCO distribution privatization.
- **OGDC** (Rs302): normalized EPS about Rs47.5, DPS about Rs21, FY26 collections 107%, overdue circular debt Rs508bn.
- **FFC** (Rs538): consolidated EPS about Rs61 TTM, about Rs41 trailing DPS. Committed Rs30.6bn more to PIA. Gas repricing risk.
- **MEBL** (Rs548): ROE 34%, P/B 3.4x, justified value about Rs490. Q3 results 22 Oct.
- **SYS** (Rs116): revenue +35% but EPS +12% in 1H26, cash conversion about 60%, senior management sold Rs138m of stock in Sep.
- **PRL:** avoid at Rs104 (normalized EPS about Rs10, likely large rights issue). Q1 results 20 Oct.
- **SAZEW** (Rs1,541): record FY26 EPS Rs390.5, DPS Rs70, P/E 3.9, down 22% since July.
- **NETSOL** (Rs123): FY26 EPS Rs27.25, about half of it a one-time license fee. The US parent is "evaluating structural options" for the Pakistan minority stake.
- **EPCL:** takeover by Noventra at Rs38.60 vs a Rs31.85 market price, but the public offer is only 17.5% of shares. Offer announcement due by 7 Dec.
- **FABL:** pass (low ROE relative to P/B).
- **MFL:** subsidiary sale talk, avoid chasing.

No positions have been bought yet. Monday buys were withdrawn pending your work.

## 4. Data access (you're on a residential Pakistani connection, which is a big advantage)

- **PSX DPS API**, blocked for cloud IPs but should work for you. Confirm first thing:
  - `GET https://dps.psx.com.pk/timeseries/eod/{SYMBOL}` returns JSON `data: [[unix_ts, close, volume, open], ...]`, full daily history
  - `GET https://dps.psx.com.pk/timeseries/int/{SYMBOL}` returns intraday
  - `POST https://dps.psx.com.pk/historical` with `month, year, symbol` returns a monthly OHLCV table
  - Send browser headers: User-Agent, `X-Requested-With: XMLHttpRequest`, Referer `https://dps.psx.com.pk/company/{SYMBOL}`. Rate limit to about 1 request a second.
  - Company announcements (with timestamps): https://dps.psx.com.pk/announcements/companies
  - Filing PDFs: `https://dps.psx.com.pk/download/document/{id}.pdf`
- **`psxdata` Python package** (`pip install psxdata`): `psxdata.stocks(symbol, start, end)` returns raw, unadjusted OHLCV with about a 10 year cap. `psxdata.screener()` returns a live snapshot of all stocks (price, P/E, dividend yield, free float, `listed_in` showing KMIALLSHR membership).
- **StockAnalysis ratios pages**, e.g. https://stockanalysis.com/quote/psx/MEBL/financials/ratios/. The HTML embeds JS arrays: `datekey`, `pe`, `peForward`, `pb`, `roe`, `dividendyield`, `payoutratio`, `lastCloseRatios`, `marketcap` (TTM first, then fiscal years). Don't trust `peForward` historically, since it may contain lookahead. Income statement and dividend pages work similarly.
- **SBP:** T-bill auctions at https://www.sbp.org.pk/assets/document/tb.xlsx (sheets "Old Format" and "New Detailed Format"); monetary policy page; EasyData.
- **NCCPL market information** (FIPI/LIPI flows by investor type, MTS leverage): https://www.nccpl.com.pk/market-information
- **Sector data:** APCMA cement despatches (https://www.apcma.com/data_monthly.html), PAMA auto sales, OCAC fuel sales, NFDC fertilizer offtake, OGRA gas and fuel pricing notifications, PBS CPI.
- **News:** Business Recorder, Mettis Global, Profit (Pakistan Today), ProPakistani, Nukta, KSEAlert, Dawn business, broker research (Topline, AHL, JS, IGI, Intermarket, Optimus).

Prices from `psxdata` and the PSX API are raw. Adjust for bonus issues and splits before computing returns. Daily moves beyond the circuit limit (±10%, or Rs1 for very cheap stocks) are corporate actions, not trades.

## 5. The research program

### Phase 1 (the most important): sector driver map and catalyst calendar
For each major sector (refineries, E&P, OMC, power, fertilizer, cement, steel, autos and auto parts, tech, Islamic banks, pharma, textiles, food, chemicals, glass and packaging, plus anything else with liquid KMI names):
- The 3 to 5 levers that actually drive its profits. Be concrete: e.g. refiners = product cracks vs Arab Light, the government diesel crack cap, deemed duty, the upgrade policy; cement = local despatches, retention price per bag, coal cost (Richards Bay/Afghan), PKR, interest cost.
- **Where each lever stands today**, with the latest datapoint, date and source.
- **What's scheduled or likely to change in the next 1 to 3 months:** policy decisions, tariff or duty changes, gas price notifications, budget measures, privatizations, circular debt steps, commodity trends, results dates.
- Which listed KMI names are most exposed, and in which direction.
- The **retrospective test:** for the 2026 refiner and steel rallies, write down what a well informed broker could have known before the move, and when. Then define the signals that would have flagged it in advance. That defines what the catalyst layer must watch.

Deliverables: `sector_map.md` and `catalyst_calendar.csv` (date, sector, tickers, event, expected direction, magnitude guess, confidence, source).

### Phase 2: results season
Results for Sep quarters land 19 Oct to mid Nov 2026. Build a pipeline that pulls each result from PSX announcements (timestamped), compares it to a sensible expectation (last year's same quarter, broker previews where available), and measures the price reaction (1 and 5 days). Using whatever history you can reconstruct from announcement timestamps, test whether big positive surprises keep drifting up (post earnings drift) and whether stocks run up before announcements (leakage).

### Phase 3: money flows and index events
- Pull NCCPL FIPI/LIPI history. Test whether sustained foreign, mutual fund or insurance net buying in a sector predicts its next 1 to 3 months.
- Rebuild the history of KSE100, KMI30 and KMI All Share recompositions (semiannual), and MSCI/FTSE Pakistan changes. Test what happens to additions and deletions around announcement and effective dates.
- Pull MTS leverage by stock if available. Test whether rising leverage marks tops.

### Phase 4: corporate value gaps
- Holding company discounts: value each listed holding company's stakes at market (sum of the parts) against its own market cap (e.g. LUCK, ENGROH, DAWH, JSCL, FFC's stakes, HUBC). Flag discounts that are unusually wide by their own history.
- Deals: pending takeovers, tender offers, buyouts, delistings, mergers and privatizations. For each, give the spread, timeline, pro rata math and odds.

### Phase 5: dividends and seasonality
- Run ups before dividend announcements and price behavior around ex dates for high yielders.
- Calendar effects: results seasons, December, June budget, Ramadan, pre and post MPC.

### Phase 6: disclosed insider buying
Scrape director and substantial shareholder trade disclosures from PSX announcements (2022 onward). Net out sales against buys (round trips exist). Test cluster buying (several insiders buying at market prices) against the following 1 to 6 month returns.

### Phase 7: synthesis into picks
Combine everything into a ranked list of **current opportunities in KMI names with 30%+ upside within 12 months**. Each needs a real catalyst path and a defined downside. Also include a short list of high quality "anchor" names in case he wants ballast (he probably won't).

## 6. Method rules (non negotiable)

- **Point in time only.** No lookahead. Results count only after their announcement timestamp. Fundamentals count only after publication. Index lists count only from their effective date.
- Always report **n, mean, median, win rate and worst case**, not just the mean. Fat right tails fool people on PSX.
- Include costs: assume about 0.5% round trip (brokerage, CVT, CDC, spread) plus slippage for illiquid names. Require minimum liquidity (e.g. median daily traded value above Rs5m) for anything tradable.
- Separate in sample from out of sample. Don't tune a rule on the same period you report it on. Prefer simple rules.
- Flag survivorship bias wherever delisted names are missing.
- **Never invent numbers.** If something can't be verified, write "unverified" or "not found." Cite sources with dates.
- **Freeze predictions.** Before any result or event lands, write the prediction into `frozen_predictions.csv` (timestamp, ticker, event, prediction, reasoning). Never edit past rows.
- Check KMI All Share membership for every pick.

## 7. Deliverables (put everything in the repo; these are what come back to the orchestrator)

```
REPORT.md              <- executive summary, max ~5 pages, written for the orchestrator to absorb in one read:
                          what you tested, results with numbers, what works on PSX and what doesn't,
                          the updated model of "how money is made on PSX", and the pick list
PICKS.md               <- broker style pitches for the top 3 to 6 opportunities (story, mispricing, catalysts
                          with dates, rupee outcomes on suggested share counts for Rs50k, dividends in the next
                          12 months net of tax, odds, thesis killers), plus a ranked watchlist with entry triggers
sector_map.md
catalyst_calendar.csv
frozen_predictions.csv
tests/                 <- one short markdown per test: hypothesis, data, method, n, results table, verdict
data/                  <- cleaned datasets (adjusted prices, fundamentals panel, flows, announcements, index history)
scripts/               <- everything reproducible
```

Keep REPORT.md and PICKS.md tight. The orchestrator will read them in full. Everything else is supporting evidence.

## 8. Practical notes

- Start by confirming PSX API access from this machine and pulling adjusted daily history for all KMI All Share names (plus delisted names you can find, to limit survivorship bias).
- Parallelize: one subagent per sector for Phase 1, another for flows and index history, another for the announcements scraper.
- Monday 19 Oct matters: if you can produce a provisional PICKS.md early, before all phases are done, do it, and mark which phases it rests on.
- Results that land during your session (EFERT 19 Oct, PRL 20 Oct, MEBL 22 Oct, SBP MPC 26 Oct, FFC ~27 Oct, OGDC 29 Oct) are live tests. Freeze predictions first.
