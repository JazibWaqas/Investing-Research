# Corporate events as trades, 18 October 2026

## Hypothesis

Announcements that change who owns, runs or funds a company, or that the exchange itself flags, leave a measurable edge when bought on the next session. Seven families, thirteen sub-types: buy-backs (E1a board approval, E1b first purchase report), bonus shares and splits (E2a, E2b), people and control (E3a CEO or chairman appointed, E3b resigns, E3c generic role-change form, E3d takeover disclosure or change of management), PSX unusual-movement letter (E4a) and company reply (E4b), credit-rating upgrade (E5), rights issue (E6, expected negative), KMI All Share addition (E7, cross-check of the index test).

## Data

`data/announcements.parquet` (225,594 rows, titles only, no PDF bodies), `data/corporate_actions.csv`, `data/corporate_actions_unplaced.csv` (rights), `data/index_changes.csv`, prices from the adjusted panel plus 315 delisted names on a crude return path (delisted names stay in: 141 of the 1,103 E3a events, 49 of the 743 E4a). KMI membership is the latest derived All Share snapshot on or before the event. Prices run 17 Oct 2016 to 16 Oct 2026. Script `scripts/tests/corporate_events.py`, raw output `tests/out/corporate_events.txt`.

## Method

Events come from title patterns, de-duplicated so one symbol cannot repeat inside 20 to 180 days (programs for buy-backs). Reaction day R is the announcement session if stamped by 15:30, otherwise the next session. The signal is the close of R. The fill is the next close that is not upper-locked (close within 0.5% of +10%). Exits: 20, 60, 120 sessions after the fill (rolled past lower locks), or a 20% close-to-close trailing stop filled at the next close, capped at 250 sessions. Costs: 0.5% round trip plus 0.5% slippage when the 60-day median traded value is under Rs20m. Trades that run past the last price date are dropped, except for delisted names, which exit at their last print.

Two placebos, 200 draws per event, same exits and costs. P1: same symbol, random day within 250 sessions. P1 is biased for explosive events (the window contains the run), so P2 is the main one: a random symbol-day from the whole panel in the same calendar year, with the same KMI status, liquidity bucket and 20-session run-up bucket. A p(median) near 1.00 means the events did worse than matched random entries; near 0 means better. Independence is shown as distinct symbols and distinct calendar months. Sleeve: Rs50k, every signal, at most 3 positions at one third of equity each.

E2 dates: the explicit title (declaration, board resolution, book-closure notice) for 46 of 149 bonuses and 17 of 19 splits; for the rest the last "Financial Results" announcement before the ex date, so those bonuses are confounded with an earnings release. E7 notices carry no clock time and are treated as after the close.

## Results

Counts: events / symbols / KMI members at the time / calendar months with an event.

| Type | Events | Symbols | KMI | Months |
|---|---|---|---|---|
| E1a buy-back approval | 23 | 19 | 13 | 17 |
| E1b first purchase | 28 | 22 | 17 | 23 |
| E2a bonus | 149 | 85 | 91 | 55 |
| E2b split | 19 | 19 | 10 | 11 |
| E3a CEO or chairman appointed | 1,103 | 403 | 552 | 120 |
| E3b resigns | 76 | 59 | 29 | 49 |
| E3c generic form | 8 | 7 | 6 | 8 |
| E3d takeover or change of mgmt | 168 | 85 | 76 | 91 |
| E4a PSX letter | 743 | 314 | 424 | 57 |
| E4b company reply | 63 | 43 | 30 | 33 |
| E5 rating upgrade | 12 | 11 | 7 | 9 |
| E6 rights issue | 149 | 111 | 79 | 81 |
| E7 KMI addition | 420 | 256 | 420 | 17 notices |

n is small (under 30 KMI events) for E1a, E1b, E2b, E3b, E3c, E5 and E4b: read those as anecdotes with a direction, not odds.

**KMI members, exit at 60 sessions, net of costs.** "Matched" is the P2 median.

| Type | n | Mean | Median | Win | >+50% | <-30% | Worst | Matched | p(med) |
|---|---|---|---|---|---|---|---|---|---|
| E1a | 13 | +1.2% | +0.7% | 54% | 0% | 0% | -19% | -1.2% | 0.40 |
| E1b | 15 | +0.1% | -2.4% | 47% | 0% | 0% | -17% | +0.6% | 0.74 |
| E2a | 89 | -1.6% | -6.0% | 39% | 2% | 4% | -35% | -3.9% | 0.84 |
| E2b | 9 | +14.8% | +13.9% | 89% | 0% | 0% | -13% | -3.4% | 0.04 |
| E3a | 526 | +2.9% | -0.5% | 49% | 5% | 6% | -97% | -1.6% | 0.14 |
| E3b | 27 | -2.5% | -4.9% | 48% | 4% | 4% | -66% | +0.1% | 0.90 |
| E3d | 74 | +1.4% | +0.0% | 50% | 5% | 7% | -66% | -1.4% | 0.24 |
| E4a | 373 | +4.6% | -3.7% | 43% | 8% | 10% | -82% | -0.6% | 1.00 |
| E4b | 29 | +20.4% | +4.0% | 59% | 14% | 10% | -58% | -0.2% | 0.22 |
| E5 | 7 | +3.1% | +8.5% | 57% | 0% | 0% | -28% | +0.2% | 0.15 |
| E6 | 76 | -4.6% | -9.1% | 33% | 7% | 14% | -66% | -3.8% | 0.99 |
| E7 | 388 | +0.7% | -4.9% | 36% | 3% | 4% | -62% | -0.2% | 1.00 |

**Other exits, KMI members** (median / win; for the stop also the mean and share above +50%).

| Type | 20 sessions | 120 sessions | 20% trailing stop | Stop >+50% | Stop worst |
|---|---|---|---|---|---|
| E1a | +0.7% / 54% | n 11, +4.8% / 64% | n 12, -3.5% / 42% / mean +46.3% | 17% | -23% |
| E1b | -1.8% / 33% | n 13, +5.7% / 62% | n 14, -6.5% / 36% / mean +62.0% | 14% | -23% |
| E2a | -2.9% / 42% | n 88, -7.4% / 39% | n 89, -12.8% / 31% / mean +0.5% | 8% | -28% |
| E2b | +2.0% / 50% | n 8, +12.9% / 62% | n 9, +11.3% / 67% / mean +20.1% | 11% | -23% |
| E3a | -1.5% / 42% | n 496, -2.1% / 47% | n 511, -8.5% / 36% / mean +6.1% | 10% | -90% |
| E3b | -1.5% / 48% | n 26, -6.9% / 35% | n 25, -13.0% / 20% / mean -3.2% | 12% | -30% |
| E3d | -2.1% / 35% | n 71, -0.6% / 49% | n 72, -7.8% / 40% / mean +4.4% | 8% | -53% |
| E4a | -4.0% / 41% | n 318, +0.7% / 52% | n 394, -12.6% / 34% / mean +9.3% | 11% | -80% |
| E4b | -3.9% / 43% | n 25, +4.7% / 56% | n 29, -7.7% / 41% / mean +11.2% | 7% | -26% |
| E5 | +2.1% / 57% | n 6, -5.7% / 33% | n 7, -8.4% / 43% / mean +4.6% | 14% | -21% |
| E6 | -4.5% / 34% | n 72, -15.4% / 28% | n 75, -15.2% / 25% / mean -6.9% | 4% | -37% |
| E7 | +0.2% / 51% | n 352, -5.1% / 41% | n 378, -10.3% / 33% / mean +5.5% | 10% | -42% |

Against the 60-session exit the trailing stop lowers the median in every family, by 3 to 17 points, and lifts the mean only through a few runners (E1a +545% and E1b +897%, both THCCL). A 20% stop is inside PSX noise.

**Leakage** (all events): the 20-session run-up before R, and the reaction-day return.

| Type | Run-up median | Share above +20% | Reaction day median |
|---|---|---|---|
| E1a / E1b | +3.1% / +0.3% | 17% / 0% | +0.5% / 0.0% |
| E2a / E2b | +2.4% / +3.4% | 7% / 5% | +2.0% / +0.9% |
| E3a / E3b / E3d | 0.0% / -2.0% / +0.3% | 10% / 4% / 15% | 0.0% / -0.1% / 0.0% |
| E4a / E4b | +34.5% / +38.1% | 63% / 65% | 0.0% / 0.0% |
| E5 / E6 / E7 | +4.2% / 0.0% / 0.0% | 0% / 18% / 12% | +1.0% / 0.0% / 0.0% |

Only the PSX letter is a late signal: 63% of letters follow a rise of more than 20% in 20 sessions (median +34.5%). Nothing else is front-run.

**Sleeve (KMI members, Rs50k, 3 slots).** Final multiple, max drawdown, and the median multiple of the matched placebo sleeve (40 draws). Spans differ by type, so compare within a row only.

| Type | 60s multiple / maxDD / placebo | Stop multiple / maxDD / placebo |
|---|---|---|
| E1a | 1.04 / -21% / 1.10 | 0.97 / -28% / 1.28 |
| E1b | 0.99 / -20% / 1.06 | 3.42 / -30% / 1.20 (one trade) |
| E2a | 1.31 / -35% / 0.77 | 1.19 / -56% / 0.94 |
| E2b | 1.50 / -18% / 0.98 | 1.57 / -21% / 0.90 |
| E3a | 1.52 / -67% / 1.68 | 0.82 / -71% / 1.64 |
| E3b | 0.62 / -48% / 1.21 | 0.72 / -53% / 1.02 |
| E3d | 1.66 / -54% / 1.65 | 0.89 / -73% / 1.15 |
| E4a | 4.15 / -49% / 2.25 | 1.44 / -59% / 2.21 |
| E4b | 4.42 / -34% / 1.28 | 2.33 / -34% / 1.33 |
| E5 | 1.06 / -21% / 1.00 | 1.09 / -20% / 1.18 |
| E6 | 0.42 / -66% / 0.91 | 0.18 / -88% / 0.92 |
| E7 | 1.03 / -51% / 2.90 | 0.59 / -54% / 2.92 |

The E4a and E4b sleeve multiples come from a handful of tail winners; their median trade is negative or flat.

## Robustness

**Liquid KMI only (median traded value at least Rs5m), 60 sessions.** E1a n 10 median +0.1%; E1b n 12 +0.9%; E2a n 44 -5.1%; E2b n 7 +18.3% with all seven positive (matched -3.7%, p 0.03); E3a n 206 -2.4%; E3d n 26 -4.5%; E4a n 106 -3.9%; E4b n 15 +4.0%; E6 n 38 -6.9% (120 sessions -10.4%); E7 n 99 -9.8%, win 30%, against a matched median of -0.2%. The conclusions do not change.

**Years.** E6 had a negative 60-session median in 8 of 11 years; the three positive years are 2023 to 2025. E7 was negative in 7 of 8 years (2026 +0.7%). E4a was negative in 5 of 7 years (the two positive years hold 1 and 6 events). E2b has three years: 2021 (n 2) +13.7%, 2025 (n 11) +18.3%, 2026 (n 5) +0.4%. E3a swings between +8% and -11% by year and averages to nothing.

**Regime (6M bill above or below the policy rate).** The bill sat above the policy rate for most events (E2a 130 of 146), so the split has little power. E6 is worse when the bill is above the policy rate (60-session median -11.3% against +0.5%); E3b is worse when it is below (-6.7% against -0.6%). E2b is positive in both.

**Since 1 Nov 2024** (cash dividends complete): conclusions hold. E2a n 8 median +5.0% (matched +1.6%, p 0.37): too few to call. E1a n 6 -13.6%, E1b n 7 -8.9%, both worse than matched.

**E4a split by the move in the 10 sessions before R.** After a rise of 15% or more (n 302): median -7.5%, 18% below -30%, matched -1.0%, p 1.00. After a fall of 15% or more (n 55): median +1.3%, mean +16.0%, matched +1.8%, p 0.55. Letters after falls are not distinguishable from chance.

**Cross-check against the index test.** `tests/index_recomposition_events.md` found KMI All Share additions flat to slightly negative from announcement to effective date (median -0.53% excess, 152 events, 17 notices). Here the 20-session median is +0.2% (388) and the 60 and 120-session medians are -4.9% and -5.1% against matched -0.2% and +3.4%; among liquid names n 99 median -9.8%. Same direction, same 17 notices, no tradable long.

## Verdict

| Sub-type | Verdict | Exit that worked | Note |
|---|---|---|---|
| E1a buy-back approval | nothing | none | n 13 KMI; median +0.7% is the market, not the news |
| E1b first purchase | nothing | none | n 15; the +897% stop trade is THCCL, one name |
| E2a bonus | nothing | none | median -6.0% at 60, -7.4% at 120, 18% below -30% at 120; same as matched entries |
| E2b split | **watch** | 60 sessions, or the 20% stop to keep a runner | 19 events in 3 years; 11 in 2025; 2026 fades |
| E3a CEO or chairman appointed | nothing | none | n 526 KMI, p(med) 0.14 |
| E3b resigns | nothing (lean avoid) | none | median -4.9%, stop median -13.0% |
| E3c generic form | nothing | none | n 8 |
| E3d takeover or change of mgmt | nothing | none | liquid KMI median -4.5% |
| E4a PSX letter | nothing as a buy; avoid after a run-up | not applicable | worse than matched entries (p 1.00) |
| E4b company reply | nothing | none | n 29; mean from 4 trades above +50% |
| E5 rating upgrade | nothing | none | n 12 total; anecdote |
| E6 rights issue | **avoid** | for a holder, 60 sessions of losses is the base case | median -9.1% at 60, -15.4% at 120, win 28% to 33% |
| E7 KMI addition | nothing (avoid chasing) | none | negative after 60 sessions in 7 of 8 years |

No corporate event is tradable on this evidence. The one lead is the split: median +13.9% at 60 sessions on 9 KMI events (89% win, worst -13%), +13.2% on all 18, matched entries about zero. The tail is thin (one trade above +50%), the sample is 19 names in three years, and eleven of them sit in the 2025 bull run.

## Caveats

Titles only, no document bodies: bonus and rights sizes, buy-back amounts and whether a CEO change is a new person or a re-election are not observed. Sixty-nine percent of bonus events are dated by the preceding results release, so they carry the earnings reaction, and cash dividends are missing from the adjusted prices before November 2024, which understates every event that sits near a payout (bonus most of all). The matched placebo cannot match on news content. The 2024 to 2026 letters (E4a) dominate that sample. Events from the last 120 sessions have no 120-session outcome yet. Crude return paths for delisted names may mis-handle bonuses.

## Today's screen (price data to 16 Oct 2026)

Live KMI events: E1b first purchase reports at CHCC (9 Oct) and AGP (15 Oct), both liquid; FATIMA chairman or CEO change (6 Oct); CLOV small bonus (2 Oct); SRVI split (notice 6 Aug, ex 24 Aug, no longer early); PSX letters at ASTM, BUXL, DWSM, NONS and GEMPACRA. None carries a measured edge. Of the five rights issues in the last 60 sessions, only GCIL (15 Sep) is a KMI name with Rs20m of daily value; the base rate says do not add to it.
