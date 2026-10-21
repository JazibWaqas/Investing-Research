# Scheduled task prompts for the GPT project (paste each into a ChatGPT scheduled task)

Each task uses web search only. Keep each alert under 150 words, lead with the action ("Buy", "Watch", "No action"), and end with the one line that would change the call. All names must be KMI All Share members. Lucky group names are allowed when worth the declaration. There are no fixed rules: every call states upside against downside in rupees and a probability.

## 1. Daily close scan — every trading day, 16:30 PKT

Search today's PSX market close (Business Recorder market wrap, Mettis, dps.psx.com.pk). Report: KSE100 close and change; the five biggest liquid KMI gainers and losers with the reason given in news or filings (results, policy, sector move, no stated cause); any KMI stock that made a new 52-week high today. For each mover, classify it with CATALOGUE.md (results jump, sector or policy wave, deal, shock rebound, sponsor buying, or no visible cause) and say join, wait or skip, with the reason. "No visible cause" with heavy volume is skip. Then check the triggers in PICKS.md and say if any fired.

## 2. Results watch — every trading day, 09:00 and 15:45 PKT

Search dps.psx.com.pk announcements and the news for board meetings and financial results filed since the last check for: MEBL, LUCK, MARI, FABL, SAZEW, SYS, OGDC, FFC, PPL, ILP, FCCL, MLCF, DGKC, KOHC. For each result: EPS against the same quarter last year and against any frozen prediction in frozen_predictions.csv, the dividend, and whether it fires a killer or a trigger in PICKS.md. Score any frozen row that has landed.

## 3. Rate and regime check — Mondays 09:00 PKT, and the evening of every SBP rate decision

Search SBP for the latest policy rate decision and statement, the latest 6-month T-bill cutoff, the weekly SBP reserves, USD/PKR, the latest CPI (PBS), and Brent. Fill in the four-signal turn checklist from REGIME_TURN_PLAYBOOK.md (oil calm: Brent not up 10%+ in 13 weeks; drain; rupee flat over 4 weeks; reserves up over 4 weeks) and the confirmation signals. Say "turn" only at 3 of 4. If a turn is called, say which names lead, how much you would move into them (from cash, new money, or trimming names that lag), and the downside in rupees.

## 4. Price triggers — every trading day, 15:40 PKT

Check closing prices against the PICKS.md triggers: MARI at or below Rs540 (the real buy); SYS at or below Rs100; SAZEW result with EPS of Rs60 or more and no rate hike; any core holding down 20% from its purchase (re-check the thesis, do not auto-sell); any opportunity position closing below its written stop (sell next morning). Only send an alert if something fired.

## 5. Weekly review — Saturdays 10:00 PKT

Summarise the week: what was bought or sold, the portfolio's change against the KMI All Share index, every frozen prediction scored this week with the running Brier score, the movers the daily scan flagged and whether those calls were right, and the plan for next week's deposit (which core name is furthest below target). List one thing the method got wrong this week and what to change.
