# PICKS.md — the open calls (built from ledger/calls.csv by scripts/ledger.py; do not edit by hand)

Built 2026-11-17. Each call's reasoning is in the journal entry it links; the latest letter to Jazib is journal/2026-11-17-picks-v9.md. To change a call, add a row to ledger/calls.csv that supersedes it, then run `scripts/ledger.py build`. Odds are the probability the call's prediction holds. Upside and downside are rupees on the suggested size.

## Live calls

| id | made | ticker | action | the call | odds that | odds | size Rs | upside Rs | downside Rs | proves it wrong | reasoning |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C0046 | 2026-10-21 | MARI | buy_if | PICKS v6: add at or below Rs540 | Total return incl. net dividends positive over 12 months from a fil... | 0.70 | 10000 | +5200 (bull Rs819) | -1300 (bear Rs468) | Same as C0045 | journal/2026-10-21-picks-v6.md |
| C0048 | 2026-10-21 | SYS | watch | PICKS v6: buy at or below Rs100, or on its first close above the 50-day average after its quarterly result | SYS closes at or below Rs100 on some day by 31 Dec 2026 | 0.25 |  |  |  | A result that settles the AI-pricing fear and a run away from Rs100 (then re-judge the ... | journal/2026-10-21-picks-v6.md |
| C0071 | 2026-11-17 | LUCK | buy | Swing into the 14 Dec MPC: Rs25,000, 56 shares, limit Rs442. Target Rs490, stop a close below Rs400, time e... | Swing exit at a profit: touches Rs490 (sell) before any close below... | 0.55 | 24752 | +2688 (Rs490) | -2352 (Rs400) | A December hike; Brent back above $105; cement despatches falling in the November data | journal/2026-11-17-picks-v9.md |
| C0072 | 2026-11-17 | MARI | buy | Swing: Rs20,000, 28 shares, limit Rs715 (pay up to Rs730 if unfilled in two sessions). Target Rs820, stop a... | Swing exit at a profit: touches Rs820 (sell) before any close below... | 0.50 | 20020 | +2940 (Rs820) | -1260 (Rs670) | The discovery spike fully retraced (close below Rs670); Phase 1B or a third party casti... | journal/2026-11-17-picks-v9.md |
| C0073 | 2026-11-17 | FCCL | buy | Swing: Rs15,000, 250 shares, limit Rs60. Target Rs68, stop a close below Rs54, time exit 18 Dec | Swing exit at a profit: touches Rs68 (sell) before any close below ... | 0.55 | 15000 | +2000 (Rs68) | -1500 (Rs54) | A close below Rs54 (the 10-day low); a December hike | journal/2026-11-17-picks-v9.md |
| C0074 | 2026-11-17 | PAEL | buy | Swing: Rs15,000, 420 shares, limit Rs35.80. Target Rs42, stop a close below Rs31.50, time exit 18 Dec | Swing exit at a profit: touches Rs42 (sell) before any close below ... | 0.50 | 15036 | +2604 (Rs42) | -1806 (Rs31.50) | A close below the 252-low (Rs31.81); a December hike | journal/2026-11-17-picks-v9.md |
| C0075 | 2026-11-17 | SAZEW | buy_if | Buy 10 shares (Rs15,000) after the November CPI release (early Dec) if CPI is under 9.0% and Brent is under... | If bought: total return positive at the 18 Dec close | 0.50 | 15000 | +1500 (Rs1,650 by 18 Dec) | -1500 (Rs1,350) | A December hike; monthly four-wheeler sales under 1,200 | journal/2026-11-17-picks-v9.md |
| C0076 | 2026-11-17 | MEBL | pass | Not in the swing book |  |  |  |  |  |  | journal/2026-11-17-picks-v9.md |
| C0077 | 2026-11-17 | ILP | pass | Not in the swing book |  |  |  |  |  |  | journal/2026-11-17-picks-v9.md |
| C0078 | 2026-11-17 | MLCF | pass | Not in the swing book |  |  |  |  |  |  | journal/2026-11-17-picks-v9.md |

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

C0028 FABL, C0030 OGDC, C0031 FFC, C0032 MEBL, C0034 PRL, C0079 PORTFOLIO
