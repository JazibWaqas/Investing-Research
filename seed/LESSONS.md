# Lessons learned so far (read before analysing anything)

Mistakes already made in this project. Don't repeat them.

1. **Standalone vs consolidated EPS.** MFL looked like 24x P/E on standalone EPS (Rs2.13). Consolidated EPS was Rs4.61, about 11x. For any holding company or group with subsidiaries, use consolidated EPS. Same trap for HUBC (standalone Rs18.86 vs consolidated Rs38.26) and FFC.
2. **Absolute historical P/E medians mislead.** PSX traded at 3 to 4x P/E in 2022 and 2023, so a stock's 5 year median P/E is dragged down by the crisis years. Using it as the exit multiple made MEBL and FFC look like −25% a year stocks. Use relative P/E (stock vs market at the same date) or a regime aware multiple.
3. **Future window exclusions are lookahead.** An earlier momentum study excluded events with a >35% jump in the following 60 days, which deletes the biggest outcomes. Never condition the sample on future data.
4. **StockAnalysis `peForward` may contain lookahead** when read historically. Use trailing P/E, P/B, ROE and dividend yield, lagged 3 months after fiscal year end.
5. **Raw prices contain corporate action gaps.** `psxdata` and the PSX API return unadjusted prices. Bonus issues and splits show as fake crashes (LUCK −79.5% on 28 Apr 2025 was the 5:1 split). Adjust before computing returns. A move beyond the circuit limit (±10%) is a corporate action, not a trade.
6. **For banks, P/E alone is a value trap.** FABL at 7x looked cheaper than MEBL at 10.8x, but FABL's ROE is ~17.5% vs MEBL's 34%. Compare P/B against ROE (justified P/B = (ROE − g) / (CoE − g)).
7. **Means lie on PSX.** Momentum and pump signals have positive means and negative medians: a few 5x winners hide a majority of losers. Always report median and win rate.
8. **Generic web page footers aren't company warnings.** The PSX "Risk Warning Alert" text appears on every company page. Verify any regulatory flag with a dated, company-specific notice.
9. **Market wide rerating flatters value.** 2022 to 2025 was a rerating from about 3.5x to 9x market P/E. Any value backtest over this period carries a tailwind. The latest cohort (Oct 2025 to Oct 2026) was flat to negative for value.
10. **Narrow takeover offers.** EPCL's control block sells at Rs38.60, but the public offer covers only 17.5% of shares, so minorities get the offer price on only about 50 to 70% of their holding. Always do the pro rata math before calling a takeover spread "free money."
11. **Insider sales are weak signals, but context matters.** A senior manager at SYS selling Rs138m while cash conversion sat at 60% was worth acting on (we deferred the buy). One small executive sale at MEBL was not.
12. **Don't recommend before mapping the sector.** The orchestrator pitched NETSOL before checking sector momentum. Tech was third worst. Check the sector backdrop first.
13. **Waiting has a cost.** An earlier ChatGPT strategy that sat in cash waiting for "validated" entries ended at Rs2.86m versus Rs4.26m for simply staying invested (same deposits). Don't let rigor turn into paralysis.
