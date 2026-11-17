# PICKS.md — the open calls (built from ledger/calls.csv by scripts/ledger.py; do not edit by hand)

Built 2026-11-17. Each call's reasoning is in the journal entry it links; the latest letter to Jazib is journal/2026-11-17-picks-v9.md. To change a call, add a row to ledger/calls.csv that supersedes it, then run `scripts/ledger.py build`. Odds are the probability the call's prediction holds. Upside and downside are rupees on the suggested size.

## Live calls

| id | made | ticker | action | the call | odds that | odds | size Rs | upside Rs | downside Rs | proves it wrong | reasoning |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C0046 | 2026-10-21 | MARI | buy_if | PICKS v6: add at or below Rs540 | Total return incl. net dividends positive over 12 months from a fil... | 0.70 | 10000 | +5200 (bull Rs819) | -1300 (bear Rs468) | Same as C0045 | journal/2026-10-21-picks-v6.md |
| C0048 | 2026-10-21 | SYS | watch | PICKS v6: buy at or below Rs100, or on its first close above the 50-day average after its quarterly result | SYS closes at or below Rs100 on some day by 31 Dec 2026 | 0.25 |  |  |  | A result that settles the AI-pricing fear and a run away from Rs100 (then re-judge the ... | journal/2026-10-21-picks-v6.md |
| C0076 | 2026-11-17 | MEBL | pass | Not in the swing book |  |  |  |  |  |  | journal/2026-11-17-picks-v9.md |
| C0077 | 2026-11-17 | ILP | pass | Not in the swing book |  |  |  |  |  |  | journal/2026-11-17-picks-v9.md |
| C0078 | 2026-11-17 | MLCF | pass | Not in the swing book |  |  |  |  |  |  | journal/2026-11-17-picks-v9.md |
| C0083 | 2026-11-17 | MARI | pass | Out of the swing book after the deeper check |  |  |  |  |  |  | journal/2026-11-17.md |
| C0088 | 2026-11-18 | SAZEW | buy_if | Buy 10 shares (about Rs12,000 to Rs15,000) only if one of: (a) a monthly sales filing shows four-wheelers a... | If bought: total return positive 6 months after the fill | 0.55 | 15000 | +6000 (Rs2,100, the card's bull case) | -4500 (Rs1,050, the card's cut level) | Gross margin under 20% in Q2; four-wheeler sales under 1,200 a month; the auto policy n... | journal/2026-11-17.md |
| C0089 | 2026-11-18 | LUCK | buy | Long-term holding: Rs25,000, 56 shares, limit Rs442. No price target; sell only if the case breaks or on a ... | Total return incl. net dividends positive over 12 months from fill | 0.60 | 24752 | +9968 (Rs620) | -6272 (Rs330) | A binding DISCO cheque above about Rs35bn for LUCK's share; cement despatches falling t... | journal/2026-11-17.md |
| C0090 | 2026-11-18 | FCCL | buy | The second Rs25,000: 417 shares, limit Rs60. Target Rs68, stop a close below Rs54, time exit 18 Dec | Swing exit at a profit: touches Rs68 (sell) before any close below ... | 0.55 | 25020 | +3336 (Rs68) | -2502 (Rs54) | A close below Rs54; a December hike; north cement despatches falling again in November | journal/2026-11-17.md |
| C0091 | 2026-11-18 | PAEL | buy | High-reward slot: Rs25,000, 700 shares, limit Rs35.80. No fixed target: exit on a close below Rs31.50 until... | Sold (or valued on 18 May 2027) above the fill | 0.50 | 25060 | +10000 (Rs50, about +40%, a first-cut rerating); +19000 at the old Rs63 high | -3000 (Rs31.50) plus gap risk | A close below Rs31.50; a December hike; Q4 (Dec) gross margin falling further | journal/2026-11-17.md |

## Open forecasts, soonest first

| id | event date | ticker | event | prediction | odds |
|---|---|---|---|---|---|
| C0065 | 2026-12-01 | KSE100 | Index level on 1 Dec 2026 against the 23 Oct low | KSE100 closes on 1 Dec above 162,375 | 0.92 |
| C0066 | 2026-12-14 | Policy rate | SBP MPC decision 14 Dec 2026 | Policy rate unchanged at 12% | 0.55 |
| C0029 | 2027-10-19 | FABL | Core buy vs paper MEBL | FABL total return beats MEBL total return over 12 months | 0.5 |
| C0033 | 2027-10-19 | PORTFOLIO | Core 3 names vs KMI All Share TR | Equal-weight FABL+OGDC+FFC total return within +-5 pts of KMI All Share TR over 12 months | 0.5 |
| C0035 | 2027-10-19 | SLEEVE | Breakout sleeve vs KMI All Share TR, first 12 months | Sleeve time-weighted return beats the KMI All Share total-return index over 12 months | 0.4 |
| C0036 | 2027-10-19 | CORE | Core vs sleeve, first 12 months | Equal-weight core (FABL, OGDC, FFC) total return beats the breakout sleeve over 12 months | 0.55 |
| C0040 | 2027-10-19 | CORE_V4 | PICKS v4 core (LUCK/MEBL/MARI equal) vs KMI All Share TR,... | Core total return beats KMI All Share TR over 12 months | 0.5 |

## Paper calls (never acted on; kept open so they are scored)

C0028 FABL, C0030 OGDC, C0031 FFC, C0032 MEBL, C0034 PRL, C0092 PORTFOLIO
