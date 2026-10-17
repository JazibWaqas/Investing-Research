# PLAN.md — PSX research program (written 17 Oct 2026, 16:20 PKT, by Claude Fable 5.1)

## 1. What the user wants (my understanding)

Jazib, 22, Karachi, first job, Rs50k now and about Rs50k a month, Finqalab, KMI All Share stocks only.
He is not chasing a number. He wants two things:

1. **A learned, written model of how money is actually made on PSX** that lives in this repo, not in any chat's memory, so Claude, GPT and future sessions can use it. The model must say what a 50-year veteran looks at, which of those things are objectively testable, and how well each works (n, median, win rate, worst case).
2. **A strategy he can run** with that model: roughly half in solid, growing, high-quality names and the other half in concentrated high-upside bets, with rules for when to buy, when to wait and when to sell. He explicitly does not want a process that waits forever for perfect prices. Margin of safety, yes. Greed for a better entry, no.

Success in one line: a repo that makes a fresh model a competent PSX investor in one read, plus a scored track record proving which parts of the model work.

The orchestrator's brief (seed/CLAUDE.md) is a starting point. Its seven phases are kept but reordered by expected payoff and I add things it missed (below).

## 2. What is already established (from seed docs, to challenge not redo)

- Works: deep value (E/P + DY), rate-cycle turns (first cut), sector momentum (6m).
- Fails: stock momentum, volume footprints, pump chasing, IMF SLA timing.
- Caveat on value: 2022 to 2025 was a market-wide rerating from 3.5x to 9x. Must retest holding market P/E constant.
- 13 lessons in seed/LESSONS.md apply. The ones that bite most: consolidated EPS, no future-window exclusions, adjust raw prices, report medians, waiting has a cost.
- Frozen forecasts exist for EFERT (19 Oct), PRL (20 Oct), MEBL (22 Oct), FCCL (27 Oct), OGDC (29 Oct). Score them as they land; never edit them.

## 3. Things the brief missed or got wrong (course changes, with reasons)

1. **No practitioner layer.** The brief tests only price data. A veteran's edge is partly reading policy and commodity signals early. I add a qualitative sweep of broker research, veteran commentary and local forums to extract what practitioners actually watch, then test those signals.
2. **No system-level backtest.** Individual factor tests do not tell you how a *strategy* would have done. I add a walk-forward backtest of the whole decision model (regime + sector + value + catalyst filters) with the model's calls at each past month, so we can see when it was wrong and why.
3. **No calibration.** Picks must carry probabilities, and the repo must track Brier-style accuracy over time. Added as catalysts/scorecard.md.
4. **Phases 5 and 6 (dividend seasonality, insider buying) likely have small n.** They run, but after the high-payoff work, and are cut if n < 30 clean events.
5. **Monday is not a deadline.** The user said so. Provisional picks ship when the catalyst layer is good enough to defend them, with phases marked.
6. **PSX API works from this machine** once `X-Req-Id` (the `window.__ps._k` value on any company page) is sent. The brief's header list was incomplete. EOD endpoint gives 5 years; `POST /historical` with `month=0&year=0` gives full OHLCV from Oct 2016. Seed prices are therefore as deep as the API; the API adds freshness, announcements, payouts and filings.

## 4. Phases, order, and who does the work

| Phase | What | Model | Output |
|---|---|---|---|
| 0 Infrastructure | PSX API client, adjusted price panel (dividends, bonus, split from payouts endpoint), KMI All Share list, announcements scraper (history as far back as the site allows), filings downloader, refresh to today | Haiku scrape, Sonnet build, Opus review of adjustment logic | scripts/psx_api.py, data/prices_adj.parquet, data/kmi_allshare.csv, data/announcements.parquet |
| 1 Sector driver map + catalyst calendar | One agent per sector (15): levers, where they stand today with dated sources, what changes in 1 to 3 months, most exposed KMI names. Plus the refiner and steel retrospective: what was knowable, when. Plus the practitioner sweep. | Sonnet per sector, Opus for the retrospective and synthesis | knowledge/sectors/*.md, sector_map.md, catalyst_calendar.csv, knowledge/playbooks/catalyst_trade.md |
| 2 Quant tests (ranked by payoff) | a) value with market P/E held constant, out of sample; b) sector momentum plus regime combined; c) results surprise and post-earnings drift, pre-result run-up; d) commodity and PKR sensitivity by sector (Brent, coal, urea, PKR); e) index recompositions (KSE100, KMI30, KMI All Share, MSCI/FTSE); f) NCCPL flows; g) dividend run-up and ex-date; h) insider cluster buying; i) calendar effects | Sonnet writes and runs; Opus reviews every design for lookahead and survivorship before it runs | tests/*.md, one per test, with n, mean, median, win rate, worst case |
| 3 System backtest and calibration | Walk-forward: at each month-end 2017 to 2026, what would the full model have bought, held, sold? Returns, drawdowns, and a post-mortem of the worst calls. Defines the confidence scale used in picks. | Sonnet build, Opus post-mortem | tests/system_walkforward.md, knowledge/playbooks/strategy.md |
| 4 Corporate value gaps | SOTP for listed holdcos (LUCK, ENGROH, DAWH, JSCL, HUBC, FFC stakes); pending deals with pro rata math and odds (EPCL, MFL, CHCC/NICL, privatizations) | Opus | knowledge/playbooks/deals.md, tests/sotp.md |
| 5 Dividends, seasonality, insiders | As in brief, cut if n too small | Sonnet | tests/*.md |
| 6 Synthesis | Underwrite candidates, freeze picks with probabilities and rupee outcomes, red team each top pick (Codex gpt-6 and a Fable consultant), write REPORT.md, PICKS.md, RUNBOOK.md, update knowledge/ | Fable (me), Codex red team | REPORT.md, PICKS.md, RUNBOOK.md |

Live tests during the session: EFERT 19 Oct, PRL 20 Oct, MEBL 22 Oct, MPC 26 Oct, FFC and FCCL about 27 Oct, OGDC 29 Oct. Predictions are frozen in catalysts/frozen_predictions.csv before each.

## 5. Token discipline

Fable (me) plans, reads summaries, integrates, judges, writes REPORT.md, PICKS.md and knowledge/ files. Everything else is delegated:
- Haiku 5.5: downloads, scraping, PDF parsing, cleaning, file housekeeping.
- Sonnet 5.5: sector research, news, standard backtests and their write-ups.
- Opus 5.5: reviewing test designs for bias, SOTP valuation, synthesising conflicting evidence, post-mortems.
- Codex (gpt-6-sol): independent red team of the top picks and of the model.
Workflows run sector agents and tests in parallel. Each agent returns a compact structured report; raw material goes to files, not to my context.

## 6. Open questions and working assumptions (user is away)

1. Averaging into a loser allowed? Assume yes while the thesis is intact and no dated breaker has fired.
2. Position cap? Assume 25% per name at full size, 4 to 6 names, Rs10k to 12.5k starters.
3. Are the orchestrator's conditional buys (SAZEW, NETSOL) open orders? Assume no. They are candidates to re-underwrite.
4. Cash rule? Assume: never hold more than 30% cash for more than 4 weeks unless the model says the market is in a hike-regime drawdown. Waiting has a cost (lesson 13).
5. Delisted names? Assume I reconstruct what I can from index recomposition PDFs and the symbols endpoint, and flag survivorship wherever it remains.
6. Weekly loop owner? Assume the orchestrator (Claude chat) plus GPT. RUNBOOK.md is written for both.

## 7. Repo as knowledge base (layout)

```
CLAUDE.md             entry point for any model: what this is, how to use it, rules
PLAN.md               this file
DECISIONS.md          dated log of course changes and why
REPORT.md             the model of how money is made on PSX, with evidence (final)
PICKS.md              current picks, frozen, with probabilities (final)
RUNBOOK.md            the weekly loop for the orchestrator and GPT
knowledge/            the durable model: one file per sector, per playbook, plus lessons
tests/                one markdown per test: hypothesis, data, method, n, results, verdict
catalysts/            catalyst_calendar.csv, frozen_predictions.csv, scorecard.md
scripts/              everything reproducible (.venv at repo root, Python 3.12)
data/                 cleaned datasets
seed/                 the orchestrator's original brief and data, untouched
```
