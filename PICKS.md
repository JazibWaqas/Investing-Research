# PICKS.md — the open calls (built from ledger/calls.csv by scripts/ledger.py; do not edit by hand)

Built 2026-11-10. Each call's reasoning is in the journal entry it links; the latest letter to Jazib is journal/2026-11-10-picks-v8.md. To change a call, add a row to ledger/calls.csv that supersedes it, then run `scripts/ledger.py build`. Odds are the probability the call's prediction holds. Upside and downside are rupees on the suggested size.

## Live calls

| id | made | ticker | action | the call | odds that | odds | size Rs | upside Rs | downside Rs | proves it wrong | reasoning |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C0046 | 2026-10-21 | MARI | buy_if | PICKS v6: add at or below Rs540 | Total return incl. net dividends positive over 12 months from a fil... | 0.70 | 10000 | +5200 (bull Rs819) | -1300 (bear Rs468) | Same as C0045 | journal/2026-10-21-picks-v6.md |
| C0048 | 2026-10-21 | SYS | watch | PICKS v6: buy at or below Rs100, or on its first close above the 50-day average after its quarterly result | SYS closes at or below Rs100 on some day by 31 Dec 2026 | 0.25 |  |  |  | A result that settles the AI-pricing fear and a run away from Rs100 (then re-judge the ... | journal/2026-10-21-picks-v6.md |
| C0053 | 2026-10-30 | SAZEW | buy_if | Tranche 3 (around 14 Dec): buy about Rs15,000 if the MPC holds or cuts on 14 Dec and Brent is below $105 | The trigger fires: MPC does not hike on 14 Dec AND Brent below $105... | 0.35 | 15000 | +10500 at the card's bull Rs2,100 | -5400 at the card's bear Rs900 | Another hike; Brent above $125; unit sales falling; gross margin under 18% | journal/2026-10-30-picks-v7.md |
| C0059 | 2026-11-10 | MEBL | buy | Buy now (10 or 11 Nov): Rs15,000, 27 shares, limit Rs570 | Total return incl. net dividends positive over 12 months from fill | 0.60 | 15000 | +3000 (Rs680) | -2500 (Rs470) | First cut of a cycle arriving fast (Islamic banks lagged after both previous first cuts... | journal/2026-11-10-picks-v8.md |
| C0060 | 2026-11-10 | ILP | buy | Buy now: Rs15,000, 145 shares, limit Rs105 | Total return incl. net dividends positive over 12 months from fill | 0.60 | 15000 | +5000 (Rs140) | -3500 (Rs78) | Q2 EPS (due about late Feb) under Rs2.50; apparel capex slips; rupee appreciation squee... | journal/2026-11-10-picks-v8.md |
| C0061 | 2026-11-10 | MARI | buy | Buy now: Rs10,000, 15 shares, limit Rs670 | Total return incl. net dividends positive over 12 months from fill | 0.55 | 10000 | +2500 (Rs830) | -2000 (Rs525) | Curtailments; the Rs86bn trade debts (provisioning exemption ends 31 Dec 2026); oil und... | journal/2026-11-10-picks-v8.md |
| C0062 | 2026-11-10 | LUCK | buy_if | Buy now only if the declaration through his father's employer is acceptable: Rs10,000, 22 shares, limit Rs450 | Total return incl. net dividends positive over 12 months from fill | 0.60 | 10000 | +4000 (Rs620) | -2500 (Rs330) | A binding DISCO cheque (GEPCO or IESCO) above about Rs35bn for LUCK's share; cement des... | journal/2026-11-10-picks-v8.md |
| C0063 | 2026-11-10 | MLCF | buy | Buy now: Rs10,000, 95 shares, limit Rs106 (the non-Lucky cement; if LUCK is also bought, both are held) | Total return incl. net dividends positive over 12 months from fill | 0.55 | 10000 | +4000 (Rs150) | -3000 (Rs75) | Cement despatches falling two months running; a December hike; coal above $150; Brent b... | journal/2026-11-10-picks-v8.md |
| C0064 | 2026-11-10 | FCCL | buy | Optional opportunity position: Rs10,000, 160 shares, limit Rs62. Exit on a close 25% below its highest clos... | Total return positive at the written exit (close 25% below the high... | 0.55 | 10000 | +3500 (Rs82) | -2500 (the stop) | A close 25% below the high; despatches falling; a December hike | journal/2026-11-10-picks-v8.md |

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

C0028 FABL, C0030 OGDC, C0031 FFC, C0032 MEBL, C0034 PRL, C0067 PORTFOLIO
