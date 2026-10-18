# Situation 01: the 2019 bottom and the IMF programme

Written 2026-10-18. Type: regime bottom (IMF and rate peak). Prices: `data/macro/kse100.csv` (headline price index; "KSE" below), `data/panel_close_adj_pricereturn.parquet` (survivors only, 34 liquid names). Macro: `data/macro/policy_rate_decisions.csv`, `cpi.csv`, `usdpkr.csv`, `tbill_auctions.csv`. "Observed" means computed from those files; "asserted" means taken from a cited page or general knowledge that I did not re-open in full.

## Dates and regime

- Policy rate 10.75% (29 Mar 2019), 12.25% (20 May), 13.25% (16 Jul): 750bp of hikes since Jan 2018 (observed).
- CPI 8.9% (Jun 2019), 10.4% (Jul), 11.9% (Aug), peaking at 14.9% in Jan 2020 (observed).
- USD/PKR 141.2 on 13 May, 157.7 on 3 Jul, 158.6 on 16 Aug: the rupee was floated down 12% in the seven weeks around the IMF deal (observed).
- 3-month T-bill 13.75% on 16 Aug (observed). IMF: staff-level agreement 12 May 2019; Board approval of a 39-month, about $6bn Extended Fund Facility on 3 Jul 2019 (IMF press release 19/264, asserted via search; the 12 May date is asserted by Arab News and secondary reports).

## What was knowable, and when

1. 12 May: the programme was agreed in principle. The market did not rally (KSE 33,900 on 13 May; observed).
2. 20 May and 16 Jul: two more hikes, the second after the Board. The programme price was visible: tight money and a depreciated rupee.
3. 3 Jul: Board approval, immediate disbursement about $1bn. KSE 34,897 that day.
4. 5 Aug: India revoked Kashmir special status (asserted, general knowledge). KSE fell to 28,765 on 16 Aug.
5. 16 Sep: the MPC held at 13.25%, the first non-hike after nine moves. The rupee had been flat for ten weeks (156.1). KSE 31,929.
6. Nov 2019: second hold, while CPI was still rising (13.7%). The central bank was looking through the peak, which is why the hold mattered.

Nothing dated 16 Aug identified it as the low.

## What the market did

| Date | KSE | Note |
|---|---|---|
| 3 Jul 2019 | 34,897 | IMF Board approval |
| 16 Aug 2019 | 28,765 | low, 17.6% below the approval day |
| 16 Sep 2019 | 31,929 | first rate hold |
| 13 Jan 2020 | 43,219 | high, +50.2% from the low, +35.4% from 16 Sep |
| 25 Feb 2020 | 38,858 | first close 10% below that high |

From 16 Sep to 13 Jan the median of 34 liquid survivors rose 41%; TRG +118%, CHCC +104%, ASTL +90%, UNITY +81%, PSO +81%. Survivorship flatters this.

## The right move

Entry that existed: the 16 Sep close after the first hold (31,929). Exit: a 10% trailing stop on index closes triggers at 38,858 on 25 Feb 2020, +21.7%. That stop is a placeholder, not a tested rule; it is shown to size the move. Holding to the 13 Jan peak was +35%; holding on was 27,229 on 25 Mar 2020 (case 02). The low itself (+50% to the peak) needed foresight. An entry on the approval day (3 Jul) was down 17.6% within six weeks and would have hit a 10% stop on 5 Aug at 31,181 (-10.6%).

Cash alternative: the 3-month bill yielded about 13.7%, so the 16 Sep trade beat cash by roughly 16 points over five months (21.7% against about 5.7% pro-rated; approximate).

## The trap

Treating "IMF approved" as the bottom. The event was fully public, had been expected for weeks, and the market fell for six more weeks because the programme cost (rates, the rupee, CPI) was still landing. Second trap: reading rising CPI as a reason to stay out when the central bank had stopped hiking.

## Situation type and lesson

Regime bottom. The sequence that marked it: IMF programme in place, rupee adjustment done, rate path stops rising, index makes a higher low (31,929 against 28,765). Buy the second signal (rate hold with a stable currency), not the first (programme announcement). In this sample the wait cost 11% of the move from the low (28,765 to 31,929) and avoided the 17.6% fall that followed the approval.

## Questions that would have caught it

- Q1 Regime: is the rate path still rising? Has the rupee finished adjusting? Has the central bank stopped reacting to CPI?
- Q2 Situation type: policy or IMF decision pending. Base rate for "IMF approval = low" in this repo: n = 3 (2019, 2022, 2023); see cases 03 and 04.
- Q4 Price confirmation: wait for a higher low, not the headline.
- Q5 Exit: where is the stop, and what does a 17% fall after good news do to the position?

Related: `tests/rate_cycle_episodes.md`, `knowledge/lessons.md` item 13.
