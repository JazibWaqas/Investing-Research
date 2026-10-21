# EXAMINER_NOTES.md — the departing researcher's examination

> **Update, 21 Oct 2026 (later the same day):** two things in this snapshot are superseded. Lucky group names are allowed when worth the declaration, and there are no fixed rules: no 80/20 split, no standing reserve, no 5% loss budget, no cash cap. Situations decide; every call carries odds and an upside-against-downside case; Jazib accepts a loss of up to about 30% on a call with a large upside. See PLAYBOOK.md and PICKS.md version 6. Where this file argues about those rules, read it as the history of the reasoning.

From Claude (Opus 5.5, continuing the Fable 5.1 session), 21 Oct 2026, to GPT-6. You have read TEACHER_NOTES.md and the core documents. This file does not repeat them. It attacks the conclusions most likely to cost money, lists where the documents contradict each other and which to follow, tests your understanding with six scenarios, names what was never written down, and gives an audit verdict. Where I checked a file for this note I say so; where something is unknown I say that.

## 1. The five conclusions that would do the most damage if wrong

### 1.1 "Keep a reserve for the regime turn; the turn is recognisable within weeks."

What it drives: 20% of every deposit held as cash, and since LUCK was withdrawn on 21 Oct, effectively 35 to 45% of the first month's money (LUCK's slot plus the reserve). If the turn is not recognisable in time, this is the costliest instruction in the repo.

Strongest counterargument. The checklist (knowledge/REGIME_TURN_PLAYBOOK.md) was built after reading the four turns and four false bottoms it is scored on: eight dates, fitted, never scored live. Two of its four signals (rupee flat over the next four weeks, reserves up over the next four weeks) are by construction only knowable four weeks after the low, and confirmation needs breadth thrust within ten sessions after that. The money in a turn is made early: the 2020 rebound and the June 2024 leaders moved within days (knowledge/regime_turns/2020.md, 2024_and_now.md). A rule that says "deploy a third at week 1 if the score is 3" cannot have a score of 3 at week 1 unless the rupee and reserve signals are read on partial data. The low itself is also ambiguous: the 2022 to 2023 file uses 23 Jun 2023 as the reference low, but the lowest rupee close was 17 Jan 2023 and the lowest dollar close 5 Apr 2023 (checked, knowledge/regime_turns/2022_23.md line 17). Choose January and the "wait from the last false bottom" falls from 11 months to 6, which is one of the two numbers behind the 12-month reserve release rule. And the reserve earns nothing: he cannot hold T-bills.

Evidence against my position. Lesson 13 and the walk-forward: being invested beat waiting, and the index compounded at 11.4% a year 2017 to 2026 (data/macro/INDEX_NOTES.md). In hike years the index roughly matched or trailed bills, but he cannot own bills, so the comparison is index against zero.

What would change my mind. A 15%+ rally in the KSE100 from a low that the checklist does not reach 3 within six weeks; or the reserve sitting idle past the 12-month release with no turn. Either means the reserve is a cash drag dressed as patience. A cleaner design would be to put the reserve into the core now and fund turn purchases from new deposits; I did not choose it because it gives up the one measured source of 5x runs. That is a judgment, and you should be willing to overturn it.

### 1.2 "The core should be growing businesses, held through falls."

What it drives: MEBL and MARI as the core, no price stops on them, bought monthly.

Strongest counterargument. The only test of a growth rule had too little data to be meaningful and showed nothing: the two-year growth-core rule made 1.73x against the index's 1.81x, inside its placebo band (tests/compounders.md). The four-name growth core held for the last year made 0.95x against the index's 0.99x (tests/rs50k_last_year.md). The quality scores that pick the names are one model's reading of filings, never tested against returns, and they barely discriminate: nine of twenty names scored 14 of 20 or a point either side (checked, knowledge/companies/quality_scores.csv). The red teams put each core name's expected 12-month return at +2 to +6%. "Growth" is also partly a story: MEBL's growth is deposit share in a bank sector whose returns are set by the policy rate; MARI's growth is volumes priced by a formula the state controls (knowledge/companies/MARI.md). Neither is a compounder in the sense he imagines (a business that doubles earnings on its own reinvestment). And "no price stop on the core" was supported by one fact: a 25% trailing stop on the backtested S3 sold its best name. In 2021 to 2023 the median liquid stock fell 52% (knowledge/situations/03). A two-name core with no stop could do that.

Evidence against my position. Concentrated holding of the right names is where the walk-forward's excess came from (SAZEW and LUCK made 88% of S3's profit, tests/system_walkforward.md), and turnover cost the equal-weight basket about 24 points (tests/size_liquidity.md). But "the right names" was known with hindsight.

What would change my mind. The core underperforming the KMI All Share by more than 10 points over 12 months (the frozen CORE_V4 row is at 0.50), or a core name's thesis killer firing while the scores still said 14+. The defensible fallback is a broader core: six to eight large KMI names near index weight, which costs little relative to the index and removes the single-name risk. The rebench showed a traded-value-weighted 12-name core lagged (0.86x the index, tests/system_walkforward.md like-for-like section), so even that fallback is not free.

### 1.3 "A reader choosing among breakouts beats a mechanical rule."

What it drives: PICKS v4 dropped the breakout sleeve and replaced it with "one discretionary opportunity at a time, chosen by the reflex".

Strongest counterargument. There is no evidence for it and some against. The only clean judgment test (the 2026 replays) found the judgment book lost to the plain breakout rule at 120 sessions under both briefs (tests/out/replay_2026/, replay_2026_v2/). Two model families on the same information produced 70% and 15% exposure (data/asof/2026-10-16/REPLY.json and REPLY_astra.json): the "reader" is not a stable instrument. The 2026 post-mortem says the rule failed because its slots were full, not because it chose badly; a fix that removed the cap was worse across windows (tests/winners_2026_postmortem.md). So the conclusion "the decision process should choose" is an inference from one year.

What would change my mind. The live register at 20 weeks: if the discretionary calls do not beat the S3 arm and the random arm on hit rate and median, go back to a mechanical sleeve and let judgment only veto (KMI, liquidity, cause), not select.

### 1.4 "Confirmed trend (the 252-day breakout) is the one robust active edge."

What it drives: the stage check, the "joinable below 2x, late above 4x" rule, the never-ignore-a-mover posture.

Strongest counterargument. It is the best of 15 pre-listed rules in two implementations, which is a multiple-testing win, not an independent confirmation: both implementations shared the data, the windows and the designer's priors. One or two trades carry each window. The three bull windows overlap one long easing cycle (2020 to 2025). The daily-resolution version is indistinguishable from random (median six-week multiple 1.00 vs 0.98, tests/pattern_mining_daily.md), and it lost 18% in the only fully out-of-sample year (tests/rs50k_last_year.md). TEACHER_NOTES says "2.5x to 3.3x in bull windows"; the correct range across both implementations is 2.1x to 3.3x (HIGH52 made 2.09x in 2022 to 2024, tests/active_trading_codex.md). A smaller point, but a sign that summaries drift toward the flattering end.

What would change my mind. The breakout arm in the live register beating random entries after costs over 12 months, in a non-bull regime.

### 1.5 "Stops should be sized to each stock's own dips, and never fixed."

What it drives: every exit in the catalogue and the regime playbook.

Strongest counterargument. Every stop size in the catalogue was chosen after seeing the path ("1.3 times the deepest pullback since the base, at most 40%", knowledge/CATALOGUE.md reflex step 6). It has never been run on losing breakouts, which are three quarters of all breakouts. On finished winners a 20% stop gave a median 1.01x with 49% losing (tests/winners_population.md, as quoted in knowledge/reviews/astra_catalogue_review.md); wider stops on losers would lose more per trade. PSX price limits mean a stop can gap through two locked sessions. A wide stop plus the 5% loss budget means small positions, which conflicts with his wish to concentrate.

What would change my mind. The pre-registered exit test on the full breakout population (TEACHER_NOTES section 8, item 2). Until it runs, any stop size is a guess with a reason.

## 2. Contradictions in the documents, and which to follow

I checked these against the files on 21 Oct. **Status after the 21 Oct cleanup:** the outdated wording below is fixed (LUCK removed from PLAYBOOK, PICKS v5, REGIME_TURN_PLAYBOOK; the handoff became knowledge/FINDINGS.md); leader sizing now defers to PLAYBOOK; the bill-income caveat is on the stop table; the breakout range is corrected. Still open: the cash cap after LUCK (a decision for Jazib, STATE.md section 2) and the research disagreements. The list is kept as written, so the reasoning stays visible.

**Outdated wording (follow the newer statement):**
- LUCK still appears as a core name in PLAYBOOK.md section A ("Currently LUCK, MEBL, MARI"), in PICKS.md's body (the LUCK pitch, and the Monday order line "LUCK 31 shares at limit Rs410"), in knowledge/REGIME_TURN_PLAYBOOK.md line 97, and in knowledge/FINDINGS.md section 5's table. The 21 Oct amendment at the top of PICKS.md, DECISIONS.md (21 Oct), CLAUDE.md and PROJECT_INSTRUCTIONS.md all exclude LUCK and the Lucky group. **Follow the exclusion.**
- knowledge/FINDINGS.md section 5 still shows MARI at 16 shares and Rs10,000; PICKS.md (body) and the MARI card say a Rs5,000 starter with the rest at or below Rs540. **Follow PICKS.md and the card.**
- PICKS.md section 5 says "Monday 19 October"; Monday has passed, no trade is confirmed, and the chat on 21 Oct moved MEBL to "after the 22 Oct result if EPS is Rs11 or more". **Follow the latest dated instruction.**

**Proposed policy choices that conflict with each other (unresolved; surface them to Jazib):**
- **Cash cap versus the reserve after LUCK.** PLAYBOOK section A says cash may never exceed 25% of the book. With LUCK's 35% slot moved to the reserve, the first month's plan holds roughly 35 to 45% cash. One of these has to give: either fill the LUCK slot (MEBL and MARI larger, or a replacement), or accept a temporary breach. My recommendation: do not let the slot sit; split it between a larger MEBL position after the result and the reserve, keeping cash under 25%.
- **Leader sizing versus the loss budget.** REGIME_TURN_PLAYBOOK says hold up to three leaders "each at most 25% of the book" with 25% stops (6.25% of the book each at the stop). PLAYBOOK section B says at most 5% at the stop per idea and 15% across correlated positions. Three turn leaders share one macro driver, so the regime playbook allows about 19% correlated risk. **Follow PLAYBOOK's limits** unless Jazib explicitly chooses more risk at the turn; it was written later and deliberately.
- **Stops on the core.** PLAYBOOK says the core has no price stop. REGIME_TURN_PLAYBOOK's stop table recommends a 25% trailing stop with buy-back above the 200-day average on the KMI All Share. They describe different things (single names versus the index), but a reader will conflate them. Neither has been tested on a two-name core.
- **Profit-taking.** PLAYBOOK section D says take a third off at +50% and +100% on round-tripping types. The rotation and profit-taking test that would have measured this was cancelled when Jazib paused the session; it never ran. **Treat as untested policy.**

**Genuine factual errors in the documents:**
- REGIME_TURN_PLAYBOOK's index stop table credits "cash earning the 3-month bill when out" (line 138). He cannot hold bills; out of the market his cash earns nothing in the brokerage account. The stop variants are flattered by bill income. **Do not cite that table's numbers as achievable for him.**
- TEACHER_NOTES section 3 item 3 says 2.5x to 3.3x; the two implementations give 2.1x to 3.3x (above).

**Unresolved research disagreements:**
- **Islamic banks at the turn.** The seed finding (two episodes) says Islamic banks lagged the market by about 48 points in the six months after the 2020 and 2024 first cuts, which is why MEBL is to be shrunk at the first cut. The regime-turn study lists MEBL in the 2023 index-led group whose first 252-high still had 3x to 5x ahead (knowledge/regime_turns/2022_23.md). These are not contradictory (relative lag over six months versus absolute multi-year gains from a different kind of low), but they point to different actions. Shrinking MEBL at the first cut is a relative-return rule; it may cost absolute return. Unresolved.
- **Who leads at a turn.** The playbook names cement and autos. The first fifteen 252-highs after each low were textiles, pharma and gas utilities in 2019; chemicals, cement, pharma and fertilizer in 2020; cement, power and refining in 2023; autos, cement and power in 2024 (the turn files). Cement is common; the rest differs by cycle, which matches the orchestrator's original finding that leaders differ. Do not pre-commit to sectors; use the first 252-highs after the low.

**Precedence when documents disagree:**
1. Jazib's latest explicit statement in conversation, and the hard constraints (KMI only, no Lucky group, no invented numbers, Finqalab stocks only).
2. The latest dated amendment in PICKS.md, then DECISIONS.md's latest entry, over any undated or older text.
3. For a number: the test file in tests/ over any summary (FACTS.md, TEACHER_NOTES.md, knowledge/FINDINGS.md, this file).
4. For catalogue rules: the status box and the Astra review over the rule text; every catalogue rule is a hypothesis.
5. For operating rules (sizing, loss limits): PLAYBOOK.md over REGIME_TURN_PLAYBOOK.md and CATALOGUE.md.
6. For turn signals only: REGIME_TURN_PLAYBOOK.md.
7. When none of these settles it: say the documents disagree, state both, and ask him.

## 3. Six scenarios to test your understanding

Each states only what was knowable at the decision time.

### 3.1 Regime turn: 11 June 2024

Known that evening: the State Bank cut 150bp to 20.5% on 10 Jun 2024 (announced after the close), the first cut after holding at 22% for a year; CPI had fallen from 38% (May 2023) to about 12% (May 2024); an IMF programme was in place; reserves had been rebuilt through 2023; the KSE100 was far above its June 2023 low and close to its highs (check the exact levels in data/prices_raw/ before quoting them); it was a pause inside an uptrend, not a crash low.

Reasoning: this is a first cut, which in the data was followed by +49% at 120 sessions (tests/rate_cycle_episodes.md). But the checklist is about lows after crises; this is a mid-cycle turn after a year-long rally. Breadth and 252-highs were already present. The rate-sensitive cyclicals (autos, cement, power) are the expected leaders; MEBL-type banks lag relatively.

Defensible decision: deploy the reserve into the first names to make new 252-highs on the cut (on 13 Jun these were SAZEW, DGKC, HUBC, LUCK, FCCL, PIOC; for Jazib, not LUCK), in thirds, with wide stops, and shift new deposits toward cyclicals.

Most tempting wrong decision: waiting because "the index is already up 80% from the low, it's late". The library says first cuts after long holds are where the multi-year runs start.

What would change it: a cut announced alongside a weakening rupee or falling reserves (an emergency cut, like March 2020's first, which came before the low), or Brent spiking.

### 3.2 Unexpected earnings: PRL, 21 April 2026

Known: PRL's March quarter EPS was Rs15.78 against a loss of Rs4.09 a year earlier; annualised, one quarter's EPS was more than the share price (it was still below Rs42 ten weeks later); the gain came in a quarter when oil spiked, so part was inventory gains; the diesel crack was capped by the government; the refinery upgrade policy had been pending for years; PRL had no dividend and might need a rights issue.

Reasoning: a huge quarter in a regulated sector with a history of one-off inventory gains. The question is not "is it cheap" (obviously, on one quarter) but "is it repeatable, and what would make the market believe it". The market lagged for ten weeks (knowledge/playbooks/catalyst_trade.md).

Defensible decision: put it on the trigger list; do not buy on the result alone; buy when price confirms (a first 252-session high) or when a dated repeatable driver appears (the policy approval). In hindsight the confirmation came on 9 Jul at Rs41.85.

Most tempting wrong decisions: buying at once because the P/E on one quarter is under 1 (then sitting through ten weeks of underperformance and probably selling), or dismissing it as a one-off forever.

What would change it: the next quarter repeating without an oil spike (makes it repeatable), or a crack-cap cut or rights issue announcement (makes it worse).

### 3.3 Unexplained price movement: SSGC, 23 October 2024

Known: SSGC (a gas utility) closed +11.2% at the upper lock on 17m shares, about 26 times its base volume (knowledge/situations/INDEX.md, tests/out/engine_scan_tagged_2024-10-23.txt); the policy rate was being cut from 17.5%; the gas utilities' returns depend on OGRA decisions on revenue requirements and on the circular-debt settlement, neither of which appears as a company filing.

Reasoning: the reflex's third check fails at the filing level ("no visible cause" in the tape), but the cause may sit in a regulator's decision, not a company filing. The engine's analogues for this signature had flat to negative medians at every horizon (the same scan file). Liquidity was adequate. A thin-float operator move has a negative base rate.

Defensible decision: spend the evening finding the cause (OGRA, the Petroleum Division, the circular-debt plan, the news). If you find a dated regulatory decision that changes the earnings base, a small position with a wide stop is defensible; if not, skip.

Most tempting wrong decision: learning from hindsight. SSGC went from Rs9.95 to a Rs49.52 peak, and a stop exit came at Rs39.24 on 7 Jan 2025. Jazib's call on it worked, and he remembers it. Do not convert one remembered winner into a rule; the same signature lost money on average.

What would change it: a published regulatory decision (positive), or a substantial-shareholder filing showing who was buying.

### 3.4 Major policy announcement: the OMC margin, 2026

Known: the ECC approved a Rs1.22 a litre rise in OMC margins; OGRA had not notified it; PSO traded at about 0.59x book with Rs415bn of receivables; the windfall levy proposal on inventory gains was unresolved (knowledge/sectors/omc.md, knowledge/companies/PSO.md).

Reasoning: an approval is not an implementation. Of 26 coded policies, items paid by industry or consumers without an IMF revenue interest were implemented 3 times in 14 (knowledge/playbooks/actors_and_incentives.md). This one raises pump prices, which governments delay.

Defensible decision: price the margin at well under 50% odds; do not buy PSO on the ECC headline; if you own it for other reasons, hold; buy only on the OGRA notification and only if the price has not already moved on the approval.

Most tempting wrong decision: buying on the approval headline as if it were income.

What would change it: OGRA's notification, or an IMF document listing the margin as a structural benchmark.

### 3.5 Portfolio rotation: the first cut, with MEBL in the core

Suppose: the State Bank makes the first cut of a new cycle; MEBL is up 15% since purchase and is the largest holding; SAZEW's result shows EPS above Rs60; the reserve holds about Rs40,000; Brent is falling.

Reasoning: the rotation rule says Islamic banks lagged after the two previous first cuts; the turn file says MEBL still did well in absolute terms after the 2023 low; SAZEW is the cyclical with capacity three times its sales; the reserve exists for exactly this.

Defensible decision: buy SAZEW and the first cyclical 252-highs from the reserve first (that is what it is for), then trim MEBL toward a smaller core weight over the following deposits rather than selling it all on the day; keep total correlated risk within the PLAYBOOK limits.

Most tempting wrong decisions: selling all of MEBL to buy cyclicals (a relative-return rule applied as an absolute one, on two episodes), or doing nothing because "the core is held through everything".

What would change it: the cut accompanied by deposit-rate floors or a bank tax that hits MEBL's spread directly (sell more), or the cut followed by a weakening rupee (wait).

### 3.6 Misleading backtest: the walk-forward's S3

Shown: "S3 (regime sectors plus value) turned Rs50,000 a month from Jan 2018 into Rs17.63m against Rs14.10m for the KMI All Share, 1.25x the index after a survivorship fix" (tests/system_walkforward.md).

Reasoning: four problems. The result is mostly deposits; on a fixed Rs50k from Oct 2024 the same strategy made 1.36x against the index's 1.81x (tests/fixed_capital_runs.md). The sector lists in its regime rule were read from the same 2018 to 2026 history. Two stocks (SAZEW and LUCK) made 88% of the profit. Cash dividends are missing before Nov 2024, which cuts both ways against a total-return benchmark.

Defensible conclusion: an in-sample upper bound with concentrated luck; not evidence of an edge. The question to ask is what a fixed sum did, from several start dates, with the rule frozen before the period.

Most tempting wrong decision: adopting S3 because "it beat the index by 25%".

What would change it: S3 run frozen, out of sample, from 2027, beating the index on a fixed sum.

## 4. Tacit knowledge and gaps

**Practical knowledge I used repeatedly that is thin or absent in the documents:**
- **The repo's prices end on 16 Oct 2026.** I fetched 19 and 20 Oct prices for scoring on 21 Oct but did not write them into data/prices_raw/. Anything computed from the repo files is stale by those sessions until `scripts/refresh_prices.py` runs.
- **How result filings are laid out.** Page one is a cover letter with the dividend; the numbers are in annexures, often scanned; the standalone and consolidated statements are on different pages with similar headings (EFERT: 6.83 standalone on page 5, 7.07 consolidated on page 11). Boards often meet after the close and the filing appears at 08:00 to 09:00 the next morning, which matters for which session is the "reaction day".
- **Price limits changed over time** (5%, then 7.5%, then 10% from July 2024, inferred from the data, not from circulars). Any "upper lock" count across years must use the limit in force.
- **Settlement moved from T+2 to T+1 in early March 2026**, which changes the ex-date relative to book closure (data/CORPORATE_ACTIONS_NOTES.md).
- **KMI All Share lists change semiannually** (effective early June and December). The current list is the 5 Jun 2026 one; the December 2026 recomposition will be announced in late November. A name's eligibility must be checked on the date.
- **Screener symbols carry suffixes** (XD, XB, NC) on ex-dates; strip them before any lookup.
- **The portal's history begins in October 2016**; there is no older daily data in the repo.
- **Why refiners fell on 20 Oct 2026 is unknown.** Do not fill that gap with a story.

**Assumptions about Jazib that may still be wrong:**
- **His real risk tolerance.** He has not yet lived through a drawdown with real money in this plan. "Accepts 40 to 60% drawdowns" is stated, not observed.
- **Existing holdings.** Unknown. He may already own stocks (the TRG trade was years ago).
- **The extent of the Lucky restriction.** LUCK and LCI are clear. Whether it extends to the wider Yunus Brothers group (for example its listed textile companies) is unknown. Ask before recommending any group-linked name. KOHC (Kohat Cement) is not a Yunus Brothers company and is on the candidate list.
- **His tax status** (filer or not) affects capital gains tax and dividend withholding; assumed filer at 15%.
- **Time.** He is starting full-time work; daily trading or intraday monitoring may not be realistic. The alert design assumes he reads messages after the close.
- **What "money in" means in practice.** He said he would put more into a high-odds call; how much more, and from where, is unknown.
- **Whether the 20% reserve is acceptable to him.** He has not been asked directly.

**Research dependencies you could misunderstand:**
- The engine's stage odds and the catalogue's "fraction still ahead" are computed on winners only.
- tests/BASE_RATES.csv was measured on the full sample to Oct 2026; every row has hindsight.
- data/fundamentals/quarterly_eps.csv does not say whether EPS is standalone or consolidated.
- Sector baskets are today's lists applied backwards.
- "Liquid" means a 60-session median traded value above Rs5m.
- Announcement data is titles only; the numbers are in PDFs.
- The KSE100, KMI30 and KMI All Share are total-return indices.
- The quality scores are one model's reading, not data.

**Questions to bring to the Claude repo session when you need it:**
- "What did situations like this one look like in the past?" (the engine, with the symbol and date).
- "Rebuild the daily table and run the tagged scan for today."
- "Score these frozen rows" (with the result figures and the source).
- "Is this name KMI on this date, and what is its 60-session median traded value?"
- "Run the pre-registered exit test" or any new test; say the hypothesis in one sentence, and the repo session will pre-register it and run a placebo.
- "Read this filing" (give the PSX document id) when a result is scanned.

## 5. The audit verdict

**What I would trust.** The negative results (what does not work, with placebos, costs and episode counts). The data pipeline's core outputs (prices, announcements with timestamps, the daily table), with the stated caveats. The facts that the KSE100 is total return, that partial offers and rights issues are traps, that profit in regulated sectors is not cash. The scoring discipline.

**What I would distrust.** Every positive rule in the catalogue; the turn checklist; the exit sizes; the quality scores; the breakout rule's bull-window multiples; any summary number not traced to its test file; my own core picks, which rest on judgment and a red-team expected return below what the index has compounded.

**What I would change first.** Remove LUCK from the four documents that still name it, and resolve the cash-cap conflict so the first month does not hold 40% cash by accident. Then run the pre-registered exit test on the full breakout population, because every exit in the playbooks depends on it.

**What should remain untouched.** The append-only register and the scoring rules; the hard constraints; the "do not repeat" list; the requirement to compare every claim against random entries; the precedence that test files outrank summaries.

**The single biggest risk.** That a confident, well-documented framework is mistaken for a validated one. The documents are long, specific and internally argued, and almost none of their positive rules has been tested out of sample. The risk is that you, or Jazib, act on them with more conviction than the evidence supports, size up, and meet a hike-regime year like the last one with a concentrated book and no exit.

**The most important principle.** Judgment is scored forward, in the register, against the plain rule and against random entries. Until the scorecard says otherwise, every call is a hypothesis with a probability, and the right response to a miss is to say what it changes.

**Questions you should still ask me:**
1. Should the LUCK slot go to MEBL, to the reserve, or to a replacement now, given the 25% cash cap?
2. Does the Lucky restriction extend to the rest of the Yunus Brothers group?
3. Has Jazib bought anything yet, and at what prices?
4. When the exit test runs, which stop variants should be pre-registered?
5. When the December KMI recomposition is announced, which held or watched names are at risk of deletion?
6. Which turn-low definition should the checklist use when the rupee, dollar and reference lows disagree?
