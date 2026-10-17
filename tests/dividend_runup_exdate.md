# Dividend run-ups, ex-date behaviour, cut drift and the dividend calendar

Run 17 Oct 2026. Script `scripts/tests/dividend_runup_exdate.py`; raw output `tests/out/dividend_runup_exdate.txt` (source of every number); calendar `catalysts/dividend_calendar.csv`. Nothing is committed.

## Hypothesis

- **H1** Names with trailing yield above 8% rise in the 20 sessions before their results and dividend announcement.
- **H2** Around the ex-date: (a) run-up ex-10 to ex-1, (b) the ex-day drop equals the dividend, (c) dividend capture survives 15% tax and 0.5% cost, (d) buying at the ex-date pays over 10 sessions.
- **H3** December and June are dividend seasons with positive excess returns for high yielders.
- **H4** A dividend cut or omission is followed by negative drift.

## Data

- Test window: cash rows with ex_date 2024-11-01 to 2026-10-16. Of 473 cash rows, 94 precede the window (a chosen sample, not complete) and 34 have a future ex-date (calendar only); 1 payouts duplicate of a seed row was dropped. 344 rows remain (314 payouts, 30 seed). Source and same-day bonus/split/right filters removed 0 (no approx, gap_inferred or same-day rows are in the window).
- Effective windows: H2 Nov 2024 to Oct 2026; H1, H3, H4 from 2025-11-01, when a full year of cash coverage exists for trailing yield (point in time, past ex-dates only, current share terms).
- Ex-month of the 378 cash rows from Nov 2024 (34 future included): Oct 133 (99 in the test window), Apr 46, Mar 42, Sep 40, May 30, Feb 26, Aug 17, Nov 17, Jan 13, Jul 8, **Jun 4, Dec 2**.
- Declaration time (spec 0.3): 207 of 315 stamped rows are raw after 15:30 PKT; rule (b) moves most to an earlier results or dividend row, leaving 15 of 344 shifted to the next session. 29 seed rows have no announce_dt; their time is the latest results announcement in the prior 75 days (my deviation).
- Universe: Rs5m liquid and in the KMI_ALL_derived snapshot in force. Returns: `prices.returns(close, 'adjusted')`, dividend counted once; net of tax scales cash by 0.85 in the actions table. Excess is vs `ew_market` (Rs5m); pre-ex windows are identical on either panel.

## Method

Per-symbol overlapping windows are dropped; events are then merged into clusters (independent episodes) when calendar windows overlap, and headline columns use the cluster mean. Placebo: 20 random entries per event in the same symbol, same window length and filters, excluding +-5 sessions around its declaration, ex-date and results; p = share of 1,000 one-per-event draws whose median is at least the observed (at most for H4). Fewer than 5 clusters is "n/t" (not testable). Dozens of rows were computed, so several p below 0.05 are expected by chance.

## Results

Columns: event-level n, symbols, clusters; event mean, median, win; cluster mean, median, win; placebo (event level) mean, median; p_event, p_cluster. "Net" is after 0.5% round trip.

| Row | n | sym | clu | mean | median | win | cl. mean | cl. med | cl. win | pl. mean | pl. med | p_ev | p_cl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H1a high yield, 20s to pre-news (descriptive) | 23 | 13 | 4 | +2.2% | +1.5% | 65% | +3.6% | +3.5% | 75% | -0.1% | -0.5% | 0.070 | n/t |
| H1a eligible at or below 8% | 345 | 144 | 2 | +1.8% | +0.2% | 50% | +1.8% | +1.8% | 100% | +1.1% | -1.1% | 0.001 | n/t |
| H1b high yield, notice to pre-news, net | 24 | 11 | 9 | +1.9% | +1.4% | 62% | +1.9% | +1.1% | 78% | -0.6% | -0.7% | 0.004 | 0.029 |
| H1b at or below 8%, net | 334 | 144 | 8 | -0.7% | -1.1% | 37% | -2.3% | -0.9% | 0% | -0.4% | -1.0% | 0.764 | 0.835 |
| H2a ex-10 to ex-1, net | 106 | 71 | 12 | +0.5% | 0.0% | 50% | +0.8% | +0.8% | 67% | -0.6% | -1.3% | 0.015 | 0.010 |
| H2a gross (descriptive) | 106 | 71 | 12 | +1.0% | +0.5% | 53% | +1.3% | +1.3% | 67% | +0.1% | -0.6% | 0.016 | 0.015 |
| H2a dividend/close at or above 2%, net | 63 | 47 | 10 | +0.6% | +0.1% | 51% | +0.7% | +1.5% | 60% | -0.6% | -1.2% | 0.063 | 0.007 |
| H2a below 2%, net | 43 | 34 | 10 | +0.2% | -0.1% | 49% | +0.5% | +0.4% | 60% | -0.1% | -1.0% | 0.116 | 0.151 |
| H2d buy ex close, hold 10, net | 185 | 76 | 13 | -1.0% | -1.7% | 32% | -3.6% | -2.6% | 15% | -0.2% | -0.9% | 0.969 | 0.994 |

Worst/best (event level): H1a high -11.8%/+12.4%; H1b high -7.5%/+14.5%; H2a -16.1%/+24.2%; H2d -14.6%/+21.2%. H1a high after tax: mean +2.3%, median +1.5%.

**H1 clusters** (equal-weight mean per episode; H1a is gross excess, H1b is net):

| Row | Cluster (first to last exposure) | n | mean |
|---|---|---|---|
| H1a high | Jan-Feb 2026 | 7 | +4.5% |
| H1a high | Mar-Apr 2026 | 10 | -0.0% |
| H1a high | Jun-Aug 2026 | 5 | +2.5% |
| H1a high | Sep-Oct 2026 (LOTCHEM) | 1 | +7.3% |
| H1b high | SNGP Nov 2025 | 1 | +3.6% |
| H1b high | EPQL, FFC Jan-Feb 2026 | 2 | +6.8% |
| H1b high | Feb-Mar 2026 | 7 | +3.0% |
| H1b high | Apr 2026 | 8 | +0.4% |
| H1b high | LOTCHEM Jul 2026 | 1 | +4.0% |
| H1b high | EPQL Jul 2026 | 1 | -0.7% |
| H1b high | BIPL Aug 2026 | 1 | +0.8% |
| H1b high | GHGL, HUBC Aug 2026 | 2 | +1.1% |
| H1b high | LOTCHEM Oct 2026 | 1 | -2.3% |

High minus low in the same two episodes: +0.8%. For H1b, 8 events were dropped for a notice under 2 sessions before results; for H1a high, 19 of 42 were illiquid.

**H2a clusters** (mean, net): 

| Cluster | n | mean | Cluster | n | mean |
|---|---|---|---|---|---|
| Feb-Apr 2025 | 12 | +0.5% | Nov 2025 SNGP | 1 | -2.7% |
| May 2025 SNGP | 1 | +4.0% | Feb-Mar 2026 | 6 | +4.4% |
| Jun 2025 HCAR | 1 | -4.7% | Mar-Apr 2026 | 11 | +1.0% |
| Jul 2025 EXIDE | 1 | +2.1% | May 2026 AVN | 1 | +5.6% |
| Sep-Oct 2025 | 43 | -0.8% | Jun 2026 HCAR | 1 | -1.7% |
| Jun-Jul 2026 GWLC | 1 | +0.6% | Sep-Oct 2026 | 27 | +1.3% |

Of 344 rows, 168 had the ex-date public after ex-10 and were dropped; liquidity removed 61 and the KMI snapshot 9.

**H2b, ex-day drop ratio** = (raw close ex-1 minus raw close ex) / gross dividend. Placebo ratios are noise around zero, so p of 0.000 only says the ratio is far from zero.

| Bucket / group | n | sym | clu | mean | median | p25 | p75 | share at or above 1 |
|---|---|---|---|---|---|---|---|---|
| Yield at or above 2%, all (headline) | 93 | 52 | 73 | 0.99 | **1.01** | 0.58 | 1.41 | 51% |
| ... payouts rows | 84 | 49 | 64 | 0.96 | 1.00 | 0.56 | 1.42 | 50% |
| ... seed rows (no pdf rows in window) | 9 | 3 | 9 | 1.20 | 1.33 | 0.76 | 1.38 | 56% |
| Below 2% | 107 | 49 | 80 | 0.84 | 1.12 | 0.27 | 1.98 | 51% |
| 2 to 5% | 75 | 46 | 64 | 0.97 | 0.92 | 0.58 | 1.36 | 48% |
| Above 5% (payouts only) | 18 | 13 | 15 | 1.05 | 1.17 | 0.95 | 1.43 | 61% |

Ex-day total-return excess vs market (yield at or above 2%, n=93, 73 clusters): gross mean +0.2%, median -0.1%, win 46%, placebo median -0.2%, p_ev 0.252; net of tax median -0.7%, win 34%.

| H2c capture (raw return, net of 0.5%) | n | clu | mean | median | win | pl. median | p_ev | p_cl |
|---|---|---|---|---|---|---|---|---|
| Gross dividend D | 200 | 125 | -0.4% | -0.6% | 36% | -0.6% | 0.562 | 0.517 |
| After tax, 0.85 D | 200 | 125 | -0.8% | -1.0% | 30% | -0.5% | 1.000 | 0.998 |
| Yield at or above 2%, after tax | 93 | 73 | -1.0% | -1.0% | 29% | -0.6% | 0.995 | 0.994 |
| Above 5%, after tax | 18 | 15 | -1.7% | -2.8% | 22% | -0.7% | 1.000 | 1.000 |

H2d windows contain no second ex-date (0 of 185), so gross and after-tax match. Seasonal H2d clusters: Feb-May 2025 n=41 -0.3%, Aug-Dec 2025 n=63 -1.3%, Feb-Apr 2026 n=27 +0.9%, Apr-Jun 2026 n=25 -2.0%, Aug-Oct 2026 n=19 -0.5%; eight small ones run -11.5% to +2.7%.

**H3, high-yield bucket (trailing yield above 8%) EW excess in the month after formation.**

| Month | eligible | high | excess gross | net of tax | median | win | worst / best | p (random names) |
|---|---|---|---|---|---|---|---|---|
| **Dec 2025** | 121 | 8 | +0.3% | +0.3% | -0.3% | 38% | -5.8% / +7.5% | 0.503 |
| Jan 2026 | 127 | 8 | -1.9% | -1.9% | -3.9% | 38% | -7.0% / +5.8% | 0.617 |
| Feb 2026 | 129 | 7 | +5.7% | +5.7% | +8.6% | 86% | -5.5% / +13.6% | 0.056 |
| Mar 2026 | 129 | 11 | +7.5% | +7.2% | +5.1% | 100% | +1.3% / +20.5% | 0.028 |
| Apr 2026 | 123 | 13 | -3.0% | -2.9% | -2.4% | 31% | -19.0% / +24.0% | 0.747 |
| May 2026 | 116 | 7 | -0.6% | -0.6% | -0.2% | 43% | -6.0% / +3.5% | 0.705 |
| **Jun 2026** | 116 | 5 | -6.0% | -6.0% | -4.6% | 20% | -13.2% / 0.0% | 0.942 |
| Jul 2026 | 135 | 5 | +1.4% | +1.3% | +2.8% | 60% | -4.2% / +6.6% | 0.237 |
| Aug 2026 | 140 | 5 | +2.6% | +2.5% | +2.4% | 60% | -2.8% / +8.7% | 0.283 |
| Sep 2026 | 141 | 5 | +1.3% | +1.4% | +1.3% | 80% | -0.1% / +3.0% | 0.187 |
| Oct 2026 (to 16th) | 128 | 5 | +0.5% | +0.5% | +1.1% | 80% | -1.4% / +1.4% | 0.433 |

Nov 2025 is not computable (formation before 2025-11-01). The nine other valid months average +0.8% (median +1.3%) excluding Dec, and +1.5% (median +1.3%) excluding Jun.

**H4.** 189 declarations with T0 from 2025-11-01. Prior-year match: period 114, ex-month 24, none 47, before coverage 4. Classes: 37 cuts (30 symbols), 65 increases, 36 flat, 51 unmatched. Omissions: 44 (38 symbols), among 182 results with a prior-year dividend (1,174 of 1,356 had none); 10 results after 2026-09-15 unclassified (feed lag). Pooled 81; controls 101.

| Row (excess, before cost) | n | sym | clu | mean | median | win | cl. mean | cl. median | pl. median | p_ev | p_cl |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cuts, T0 reaction | 20 | 16 | 16 | -0.4% | -0.6% | 45% | -0.9% | -0.9% | -0.1% | 0.045 | 0.003 |
| Omissions, T0 | 26 | 22 | 20 | 0.0% | -0.7% | 35% | 0.0% | -0.9% | -0.2% | 0.031 | 0.014 |
| Pooled, T0 | 46 | 32 | 33 | -0.1% | -0.7% | 39% | -0.4% | -0.9% | 0.0% | 0.003 | 0.000 |
| Controls, T0 | 64 | 47 | 47 | +0.3% | 0.0% | 50% | +0.4% | +0.2% | -0.1% | 0.678 | 0.936 |
| Cuts, +5 | 20 | 16 | 9 | -0.5% | -0.8% | 45% | -1.1% | -2.0% | -0.2% | 0.152 | 0.019 |
| Omissions, +5 | 26 | 22 | 8 | +0.5% | -0.9% | 42% | -1.1% | -1.6% | -0.1% | 0.164 | 0.054 |
| Pooled, +5 | 46 | 32 | 9 | 0.0% | -0.9% | 43% | -1.7% | -1.8% | -0.3% | 0.097 | 0.024 |
| Controls, +5 | 64 | 47 | 8 | -0.1% | 0.0% | 50% | +1.6% | +0.6% | -0.2% | 0.593 | 0.845 |
| Cuts, +20 | 19 | 15 | 3 | +2.8% | +1.7% | 53% | +2.3% | +2.6% | -0.4% | n/t | n/t |
| Pooled, +20 | 45 | 32 | 4 | +2.0% | -0.2% | 49% | +0.7% | +1.2% | -0.7% | n/t | n/t |
| Cuts, +60 | 11 | 11 | 1 | +3.8% | +2.1% | 73% | +3.8% | +3.8% | +7.4% | n/t | n/t |
| Pooled, +60 | 24 | 23 | 1 | +0.6% | +0.2% | 50% | +0.6% | +0.6% | -0.2% | n/t | n/t |
| Exit rule (sell at T0 close, after cost), pooled +5 | 46 | 32 | 9 | -0.5% | +0.4% | 54% | +1.2% | +1.3% | -0.2% | 0.090 | 0.014 |

Worst/best: cuts T0 -7.6%/+4.6%; pooled T0 -7.6%/+11.2%; cuts +20 -6.1%/+15.6%; cuts +60 -13.3%/+20.5%. After tax, +20 cuts mean +2.7%, +60 cuts +3.5%. T0 clusters are single announcement days (16 cuts, 20 omissions, 33 pooled; each listed in the printout).

**Calendar.** `catalysts/dividend_calendar.csv`: 69 rows, 30 names; 2 declared (CSAP, GHGL, both ex 2026-10-21), 67 projected; 6 one-off rows (AGP, CPHL, FCL, IPAK, LOTCHEM, NRSL). Universe 309 KMI names, 174 liquid, 125 in both. Three projections were skipped because the payment already went ex by 2026-10-16 (SYM, BERG, OGDC).

| Top 30 by trailing yield, 2026-10-16 | | | | |
|---|---|---|---|---|
| LOTCHEM 25.58% | SYM 12.40% | EPQL 11.67% | BIPL 11.27% | HUBC 10.34% |
| GHGL 10.20% | BERG 8.87% | FFC 7.62% | OGDC 7.36% | FABL 7.10% |
| DCR 6.48% | ISL 6.32% | IPAK 6.31% | EFERT 6.29% | GLAXO 6.08% |
| FCL 6.07% | COLG 5.74% | CPHL 5.68% | MEBL 5.40% | LCI 5.40% |
| HINOON 5.36% | CSAP 5.04% | AGP 4.75% | BIFO 4.71% | WAFI 4.55% |
| NRSL 4.53% | JVDC 4.50% | INIL 4.49% | HCAR 4.46% | HALEON 4.38% |

SYM, BERG and OGDC hold the same seasonal payment twice in the 12-month window, inflating their rank. Projections are a one-year pattern repeat, not forecasts; history is two years at most; par-value errors below 4% yield are unverified (CORPORATE_ACTIONS_NOTES.md item 3). Live screen: seven names exceed 8% (LOTCHEM, SYM, EPQL, BIPL, HUBC, GHGL, BERG); GHGL's declared Rs1.00 is a cut from Rs1.50 (ratio 0.67).

## Robustness

- Leave-one-cluster-out cluster median: H1b high +1.0% to +2.1%; H2a +0.6% to +1.0%; H1a high +2.5% to +4.5%; H2d -3.6% to -2.3%; H4 pooled T0 -0.9% throughout.
- Tax changes nothing for pre-ex windows (H1, H2a), costs about 0.5 point on the ex-day return and H2c, and moves H4 +20 cuts by 0.1 point.
- H2a by size: dividend at or above 2% of price has cluster median +1.5% (p_cl 0.007); below 2%, +0.4% (p_cl 0.151).
- Event and cluster medians disagree for H2a (0.0% vs +0.8%): cluster medians lean on off-season singletons; large seasonal H2a clusters run -0.8% to +4.4%. Low yielders also beat placebo before results (H1a event p 0.001), so the run-up is not specific to high yield.

## Verdict

- **H1a:** not testable (4 clusters). **H1b:** weak evidence for: 9 clusters, net cluster median +1.1% vs placebo -0.7% (p_cl 0.029, p_ev 0.004), but 11 symbols, one year, survivor-biased. Paper-track this results season; not proven.
- **H2a:** marginal. Beats placebo (p_cl 0.010) but net event median is 0.0% and 168 of 344 dividends were not public by ex-10. Not tradable alone.
- **H2b:** the price falls by the dividend (median ratio 1.01, 73 clusters). Payouts rows are circular (ex-dates calibrated on dips); the independent seed rows (n=9, 3 names) show 1.33. No ex-day abnormal return (p_ev 0.252).
- **H2c:** rejected. Gross equals a random day (p 0.562); after tax it is worse (30% win). **H2d:** rejected as a long entry; lags placebo (p_cl 0.994).
- **H3:** 2 episodes, not testable. Dec 2025 +0.3%, Jun 2026 -6.0%. The premise also fails on the calendar: 2 December and 4 June ex-dates vs 99 in October.
- **H4:** announcement-day reaction is negative (cluster median -0.9% for cuts, omissions and pooled vs +0.2% for controls; p_cl 0.003, 0.014, 0.000) but happens at T0, so it cannot be traded. Drift at +5 is weak (cuts cluster median -2.0%, p_cl 0.019, p_ev 0.152); +20 and +60 not testable. The exit rule shows no value after cost.

## Caveats

- Survivorship: the panel and payouts feed hold only names listed on 2026-10-16. Delisted cutters are missing, so H4 drift is likely understated and high-yield buckets flattered.
- Par value: amounts are percent times par; names with Re1 or Rs5 par below 4% yield are unverified, which touches drop ratios, yields, cuts and calendar amounts. Large cuts (EPQL 1.25 vs 7.5, FFC 8.5 vs 21) rest on one prior-year amount.
- Coverage: a name with no cash row gets zero trailing yield (low bucket); the omission rule assumes the payouts feed is complete; 47 declarations had no prior-year match.
- Liquidity and KMI filters remove about half of events (H2b/c: 121 illiquid, 19 non-KMI of 340). October holds 133 of 378 ex-dates, so event counts overstate the evidence.
- The EW market is survivor-biased. Cuts arrive with earnings, so the T0 reaction mixes dividend and earnings surprise.
- The spec names the files `dividend_events`; this run used the names assigned (`dividend_runup_exdate`).
