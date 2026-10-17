# HANDOFF.md — continue point (written 17 Oct 2026, about 21:30 PKT, session paused at the usage limit)

Read this first when resuming. Then CLAUDE.md, PLAN.md, DECISIONS.md.

## Where the program stands

Done and committed:
- Infrastructure: PSX portal API client (`scripts/psx_api.py`, X-Req-Id trick in CLAUDE.md), 313 KMI price files to 16 Oct (`data/prices_raw/`), shared loader `scripts/prices.py` (crude and adjusted modes), announcements archive 2005 to 2026 with timestamps and classes (`data/announcements.parquet`, 225k rows), index membership history (`data/index_changes.csv`, `data/index_members/`, notes in `data/INDEX_DATA_NOTES.md`), macro and commodity series (`data/macro/`, README there), NCCPL flows daily by investor type and by sector 2017 to 2026 (`data/macro/fipi_lipi*.csv`).
- Phase 1: 16 sector notes (`knowledge/sectors/`, each with a Codex gap-resolution section), `sector_map.md`, `catalysts/catalyst_calendar.csv` (126 rows), `knowledge/playbooks/catalyst_trade.md` (refiner and steel retrospective; verdict: refiners were flaggable 29 Apr as a loaded spring and 8-9 Jul as a trade; ASL doubled on disclosed sponsor buying), `practitioner_signals.md`, `sector_rotation.md`.
- Audit of the orchestrator's tests (`tests/seed_audit.md`): value finding downgraded, placebo baseline established, lessons 14 to 19 in `knowledge/lessons.md`.
- Phase 2a tests (`tests/`): sector momentum and regime, commodity and PKR sensitivity, flows, rate-cycle episodes. Verdicts in DECISIONS.md (17 Oct, last entry): sector and macro signals are context, not triggers.
- Codex tests: index recompositions (no tradable edge), calendar effects (February weak, November strong, not a rule).
- 27 frozen predictions for 19 to 29 Oct results and the 26 Oct MPC (`catalysts/frozen_predictions.csv`). Score them as results land; never edit the frozen columns.
- Pre-registered strategies for the walk-forward test (`knowledge/playbooks/strategy_candidates.md`): B0 naive EW, B1 orchestrator model, S2 momentum plus value plus ignored-quarter satellite, S3 regime rotation plus sponsor buying, S4 full model. Fixed before any backtest.

Running when the session paused (outputs land in the repo; commit whatever exists):
1. Phase 2b workflow (run id wf_3c960b7d-0e4): corporate-actions table (`data/corporate_actions.csv`, written; notes expected in `data/CORPORATE_ACTIONS_NOTES.md`), adjusted panel (`data/panel_close_adj.parquet`, written), quarterly EPS (`data/fundamentals/quarterly_eps.csv`, written), then four Opus-reviewed tests: results_surprise_drift, insider_cluster_buying (builds `data/insider_trades.csv`), dividend_runup_exdate (writes `catalysts/dividend_calendar.csv`), value_timestamped. Check `tests/` for which `.md` files exist.
2. Underwriting workflow (run id wf_709f39a7-b1b): `knowledge/companies/<SYM>.md` for NETSOL, PSO, GHGL, OGDC, PPL, MEBL, SAZEW, FFC, EPCL, ATRL, SNGP, LUCK, each followed by a Sonnet red-team section ending UPHELD / WEAKENED / BROKEN. Eleven cards exist; SNGP and the red-team sections may be incomplete.
3. Opus agent on holdco discounts and deals: `knowledge/playbooks/holdco_discounts.md` and `deals.md` (not yet written when paused).
4. Size and liquidity test: `tests/size_liquidity.md` (script and raw output exist; write-up pending). Question: did large liquid names beat small ones 2017 to 2026 (EW liquid basket +44% vs KSE100 +245% price-only).

Workflow resume: `Workflow({scriptPath: "<session workflows dir>/psx-phase2b-announcement-tests-wf_3c960b7d-0e4.js", resumeFromRunId: "wf_3c960b7d-0e4"})` replays completed agents from cache. Scripts live under `C:\Users\JazibWaqas\.claude\projects\c--Users-JazibWaqas-Documents-GitHub-Investing-Research\<session>\workflows\scripts\`. If the session is gone, rerun the missing pieces as plain agents from the file outputs that exist.

## Next steps, in order

1. Commit and push anything the running agents wrote. Read the four Phase 2b test verdicts and the size test; add a DECISIONS.md entry.
2. Phase 3: walk-forward backtest of the pre-registered strategies in `strategy_candidates.md` (Sonnet build, Opus post-mortem of the worst calls) using `data/panel_close_adj.parquet`, `quarterly_eps.csv`, `insider_trades.csv`. Output `tests/system_walkforward.md`. Rules in the candidates file must not be changed after seeing results; add new variants only as clearly labelled post-hoc.
3. Read the 12 underwriting cards and their red-team lines. Pick 3 to 6 names: roughly half core quality, half high-upside with a dated catalyst. Red-team the top 3 with Codex (`codex exec -c 'tools.web_search=true' -C <repo> -s workspace-write -c 'approval_policy="never"' - < prompt.md`) and one Fable consultant pass.
4. Write REPORT.md (the model of how money is made on PSX, with the test numbers; max 5 pages), PICKS.md (broker-style pitches, share counts for Rs50k, dividends net of 15% tax, probabilities, killers, ranked watchlist with entry triggers), RUNBOOK.md (weekly loop for the orchestrator and GPT: refresh prices and announcements, score frozen predictions, update catalyst calendar, re-screen the ignored-quarter and sponsor-buying signals, update the scorecard).
5. Score the frozen predictions as EFERT (19 Oct), ATRL (19 Oct), PRL (20 Oct after close), EPCL (20 Oct), MEBL (22 Oct), MPC (26 Oct), FCCL and FFC (about 27 Oct), OGDC (about 29 Oct) land. Fill `outcome`, `scored_at`, `score_note`; update `catalysts/scorecard.md`.

## Emerging model (provisional, for whoever writes REPORT.md)

- Sector and macro timing signals exist in the data but are too weak or too few to trade for a long-only retail investor. Being invested matters more than timing: cash drag is the biggest documented cost.
- The KSE100 beat the equal-weight liquid basket by a wide margin 2017 to 2026, but tests/size_liquidity.md shows this is NOT a large-cap premium: daily rebalancing noise costs about 24 points, dropped dividends about 10, and the rest is cap-weighting toward a few large winners. Inside the investable set, the least liquid third beat the most liquid third by about 5 points a year (weak, t about -1.5, led in 3 of 10 years). Practical reading: concentrated positions in a few winners beat broad equal-weight baskets; churn is expensive.
- Stock-level edges still open for testing in Phase 2b: a strong quarter the market ignores (the 2026 refiner setup: PRL at 2x trailing earnings after its March-quarter result), disclosed sponsor buying (ASL), partial-offer deal math (EPCL).
- The orchestrator's deep-value result is mostly a sector effect and not statistically distinguishable from zero. Value is a tiebreaker inside a sector view.

## Environment notes

- Python: `.venv/Scripts/python.exe`. Use `-X utf8` when printing agent outputs (cp1252 console).
- Commits: no Co-Authored-By trailer. Push to origin main freely (user instruction 17 Oct).
- Raw downloads under `data/raw/` and `data/announcements.csv` are gitignored.
- Codex CLI: `codex exec` works; web search needs `-c 'tools.web_search=true'` (the `--search` flag is not accepted by `exec`).

## Addendum (about 22:00 PKT): underwriting result

All 12 cards are in `knowledge/companies/` with red-team sections. Every one came back WATCH or AVOID. Expected 12-month returns after the red team: NETSOL +2%, PSO +4%, GHGL +8 to 10%, OGDC +2 to 3%, PPL +4%, MEBL +3%, FFC +3%, ATRL +0.5%, LUCK +3%, SAZEW about -9% (avoid), EPCL about 0% (avoid, partial offer), SNGP +2% (avoid). All below the 12.5% T-bill. The red teams mostly cut the base case for one-offs treated as recurring and for re-ratings assumed without a driver.

What this means for PICKS.md: at 16 Oct prices, with the market near its high and the curve pricing hikes, none of the obvious candidates clears a 30% bar, and most do not clear the risk-free rate. The honest provisional pick list is therefore small and conditional: entry limits from the cards (OGDC about Rs265, MEBL Rs485, PSO Rs345, GHGL after the 28 Oct print, NETSOL after the 30 Oct print) plus whatever the Phase 2b live screens produce (ignored-quarter setups, sponsor-buying clusters). Do not manufacture 30% upside that the cards do not support; say so in PICKS.md and give the triggers. The cash rule in PLAN.md section 6 still applies: deploy into the best available names at their limits, not into the T-bill.

Also landed: `knowledge/playbooks/deals.md`, `holdco_discounts.md`, `tests/size_liquidity.md` (read its verdict before writing REPORT.md).
