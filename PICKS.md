# PICKS.md — the open calls (built from ledger/calls.csv by scripts/ledger.py; do not edit by hand)

Built 2026-10-30. Each call's reasoning is in the journal entry it links; the latest letter to Jazib is journal/2026-10-30-picks-v7.md. To change a call, add a row to ledger/calls.csv that supersedes it, then run `scripts/ledger.py build`. Odds are the probability the call's prediction holds. Upside and downside are rupees on the suggested size.

## Live calls

| id | made | ticker | action | the call | odds that | odds | size Rs | upside Rs | downside Rs | proves it wrong | reasoning |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C0046 | 2026-10-21 | MARI | buy_if | PICKS v6: add at or below Rs540 | Total return incl. net dividends positive over 12 months from a fil... | 0.70 | 10000 | +5200 (bull Rs819) | -1300 (bear Rs468) | Same as C0045 | journal/2026-10-21-picks-v6.md |
| C0048 | 2026-10-21 | SYS | watch | PICKS v6: buy at or below Rs100, or on its first close above the 50-day average after its quarterly result | SYS closes at or below Rs100 on some day by 31 Dec 2026 | 0.25 |  |  |  | A result that settles the AI-pricing fear and a run away from Rs100 (then re-judge the ... | journal/2026-10-21-picks-v6.md |
| C0049 | 2026-10-30 | MEBL | buy | Tranche 1, Mon 2 Nov: Rs15,000, 28 shares, limit Rs535 | Total return incl. net dividends positive over 12 months from fill | 0.60 | 15000 | +3400 (good year, Rs650) | -2500 (cuts start, Rs440) | First rate cut of a cycle (Islamic banks lagged 48 pts in 6 months after both previous ... | journal/2026-10-30-picks-v7.md |
| C0050 | 2026-10-30 | LUCK | buy_if | Tranche 1, Mon 2 Nov: Rs10,000, 25 shares, limit Rs400, only if the declaration through his father's employ... | Total return incl. net dividends positive over 12 months from fill | 0.55 | 10000 | +4200 (turn year, Rs560) | -2300 (hikes persist, Rs300) | A binding DISCO cheque (GEPCO or IESCO) above about Rs35bn for LUCK's share; cement dem... | journal/2026-10-30-picks-v7.md |
| C0051 | 2026-10-30 | MARI | buy | Tranche 1, Mon 2 Nov: Rs10,000, 15 shares, limit Rs640 | Total return incl. net dividends positive over 12 months from fill | 0.55 | 10000 | +2500 (good, Rs800) | -2000 (oil to $75 and curtailments, Rs500) | Curtailments (50 MMscfd is about Rs10 of annual EPS); the Rs86bn trade debts (provision... | journal/2026-10-30-picks-v7.md |
| C0052 | 2026-10-30 | ILP | buy | Tranche 1, Mon 2 Nov: Rs10,000, 100 shares, limit Rs99 | Total return incl. net dividends positive over 12 months from fill | 0.55 | 10000 | +3900 (good, Rs135) | -2600 (bad, Rs70) | Next quarter's profit falls back under Rs2.50 a share; apparel capex slips; a rupee app... | journal/2026-10-30-picks-v7.md |
| C0053 | 2026-10-30 | SAZEW | buy_if | Tranche 3 (around 14 Dec): buy about Rs15,000 if the MPC holds or cuts on 14 Dec and Brent is below $105 | The trigger fires: MPC does not hike on 14 Dec AND Brent below $105... | 0.35 | 15000 | +10500 at the card's bull Rs2,100 | -5400 at the card's bear Rs900 | Another hike; Brent above $125; unit sales falling; gross margin under 18% | journal/2026-10-30-picks-v7.md |

## Open forecasts, soonest first

| id | event date | ticker | event | prediction | odds |
|---|---|---|---|---|---|
| C0024 | 2026-10-26 | KSE100 | Market direction after MPC | KSE100 closes higher on the 5th session after 26 Oct (about 2 Nov) than on the last close before ... | 0.52 |
| C0015 | 2026-10-27 | FCCL | Price reaction to Q1 FY27 results | Price rule: close of 5th trading session after the release day (release day = session containing ... | 0.47 |
| C0018 | 2026-10-27 | FFC | Price reaction to Q3 CY26 results | Price rule: close of 5th trading session after the release day (release day = session containing ... | 0.45 |
| C0022 | 2026-10-29 | OGDC | Price reaction to Q1 FY27 results | Price rule: close of 5th trading session after the release day (release day = session containing ... | 0.45 |
| C0054 | 2026-11-03 | CPI | October 2026 CPI (PBS, due 3 Nov) | Headline CPI year on year below 10.0% | 0.60 |
| C0042 | 2026-11-10 | REGIME | Regime-turn checklist (REGIME_TURN_PLAYBOOK.md) as of 19 Oct | Checklist does NOT reach a score of 3 by 10 Nov 2026 (no turn) | 0.75 |
| C0056 | 2026-12-01 | KSE100 | Index level on 1 Dec 2026 against the 23 Oct low | KSE100 closes on 1 Dec above 162,375 | 0.70 |
| C0057 | 2026-12-01 | TRANCHE2 | Tranche 2 released by signal (a) CPI under 10% with Brent... | Signal (a) or (b) fires before 1 Dec | 0.45 |
| C0055 | 2026-12-14 | Policy rate | SBP MPC decision 14 Dec 2026 | Policy rate unchanged at 12% | 0.55 |
| C0029 | 2027-10-19 | FABL | Core buy vs paper MEBL | FABL total return beats MEBL total return over 12 months | 0.5 |
| C0033 | 2027-10-19 | PORTFOLIO | Core 3 names vs KMI All Share TR | Equal-weight FABL+OGDC+FFC total return within +-5 pts of KMI All Share TR over 12 months | 0.5 |
| C0035 | 2027-10-19 | SLEEVE | Breakout sleeve vs KMI All Share TR, first 12 months | Sleeve time-weighted return beats the KMI All Share total-return index over 12 months | 0.4 |
| C0036 | 2027-10-19 | CORE | Core vs sleeve, first 12 months | Equal-weight core (FABL, OGDC, FFC) total return beats the breakout sleeve over 12 months | 0.55 |
| C0040 | 2027-10-19 | CORE_V4 | PICKS v4 core (LUCK/MEBL/MARI equal) vs KMI All Share TR,... | Core total return beats KMI All Share TR over 12 months | 0.5 |

## Paper calls (never acted on; kept open so they are scored)

C0028 FABL, C0030 OGDC, C0031 FFC, C0032 MEBL, C0034 PRL, C0058 PORTFOLIO
