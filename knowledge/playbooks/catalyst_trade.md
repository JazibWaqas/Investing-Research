# Playbook: the catalyst trade (spread + policy + ignored earnings)

Written 2026-10-17. Evidence: `tests/refiner_steel_retrospective.md` (prices, PSX filings, ProPakistani and Dawn), plus the sector files in `knowledge/sectors/`. Status: one fully traced episode (refiners 2026), one partial analog (refiners 2020, from `knowledge/sectors/refineries.md`), and one different mechanism (ASL 2026, sponsor buying). The web search budget ran out before this session started, so broker notes and Business Recorder were not read. Treat the signal list as a watch design, not a tested model.

## 1. What happened in 2026

**Refiners.** The four March-quarter results came out between 21 and 29 Apr 2026, and every one swung from loss to large profit:

| Name | March-quarter EPS | Year earlier | Price on result date |
|---|---|---|---|
| PRL | Rs15.78 | −4.09 | Rs38.8 |
| ATRL | Rs106.41 | 15.97 | Rs940 |
| NRL | about Rs91 (profit Rs7.30bn) | loss | Rs382 |
| CNERGY | Rs3.22 | | Rs8.4 |

Sources are PSX docs 274659, 275863, 275684 and 275538. PRL traded at about 2x trailing EPS. The market ignored this for ten weeks, and the refiners lost 16 to 22 points against the market between 29 Apr and 6 Jul. It was right to be wary, because the profit came from the March oil spike: Brent went from $71 to $128 after Hormuz closed on 28 Feb, then fell back to $68.5 by 2 Jul (FRED). A windfall tax was also being discussed (26 May, `knowledge/sectors/omc.md`).

Three things then turned at once:

1. **Spread.** On 8 Jul the US-Iran truce collapsed and Brent rose 6% (ProPakistani, 8 Jul). The crude low was in, and cracks widened. The July GRM was $36.7 against $5.4 a year earlier (ProPakistani, 2 Sep).
2. **Policy.** The refining policy was "fast-tracked" on 13 Jul (unverified). The Cabinet Committee on Energy approved it on 28 Jul after seven years of deadlock (Dawn, 25 Sep).
3. **Earnings visibility.** The April results had already shown that the plants could earn in a high-crack regime.

PRL's volume went from 1.7m shares on 6 Jul to 15.6m on 7 Jul and 48m on 8 Jul. On 8 Jul PRL rose while the KSE-100 fell 2.5%. From 9 Jul to 16 Oct, PRL returned +155%, NRL +70%, ATRL +34% and CNERGY +37% (+64% at its peak).

**Steel.** There was no sector move. ISL and MUGHAL are 31% and 37% below their January highs. ASL alone doubled, from Rs9.00 on 19 Mar to Rs17.83 on 9 Sep. Its sponsor, Arif Habib Corp, bought in the open market on 7 Apr at Rs9.78, on 21 May at Rs12.27 and on 3-4 Aug at about Rs13.6 (docs 273850, 277816, 280799). It had also injected Rs6.9bn of equity by March (doc 275493). Each purchase was public within two days. ASTL's one-week +34% after its 16 Sep results is unexplained (unverified).

**Verdict.** The refiners were flaggable as a "loaded spring" from 29 Apr and as a trade from 8-9 Jul. Their size was luck: a war restarted. ASL was flaggable on 9 Apr from public sponsor filings. We missed both because we had no watch for ignored earnings or for sponsor buying, and because a sector-momentum filter puts a sector on the radar only after the move.

## 2. The pattern

A catalyst trade needs three legs, in this order:

1. **A visible earnings inflection that the price ignores.** The latest quarter's EPS is large against price (one quarter above 10% of price, or trailing P/E under 4x). It swings from a loss or doubles year on year. The stock does nothing for weeks afterwards because the market calls it a one-off. This is the loaded spring.
2. **The spread turns in the company's favour.** The commodity margin that drives earnings widens again: crude crack, urea against gas, PVC against ethylene, rebar against scrap, or crude for E&P. Or a regulated price is reset (OGRA, NEPRA, ECC). This tells you the "one-off" is repeating.
3. **The policy overhang lifts.** A long-pending approval passes (ECC, cabinet, CCoE, NTC final duty, IMF sign-off). This turns a trade into a rerating.

Price and volume confirm. The first day of more than 5x volume, rising on a down-market day, is the latest sensible entry. The first leg alone is a value trap. In 2026 it cost 20 relative points while the earnings sat there. All three legs together explain the 2020 refiner move as well: an oil low, the OPEC+ deal of 6 Jan 2021, and lubes earnings (`knowledge/sectors/refineries.md`).

The sponsor variant is simpler. A controlling shareholder buys in the open market more than once while injecting equity into the company. That is the strongest public insider signal on PSX. Lesson 11 still applies: one sale by an executive means little.

## 3. Signals to check every week

| # | Signal | Trigger | Source |
|---|---|---|---|
| 1 | Ignored blowout quarter | Latest quarterly EPS more than 10% of price, or trailing P/E under 4x, and 20-day relative return under +10% four weeks after the result | PSX announcements, `financial_result` class, via `scripts/fetch_announcements.py`; https://dps.psx.com.pk/announcements/companies |
| 2 | Crude and inventory direction | Brent more than 10% off its 20-day low, or quarter-to-date change above ±15%. Up means inventory gains for refiners and OMCs; down means losses | FRED DCOILBRENTEU (`data/macro/brent.csv`); https://fred.stlouisfed.org/series/DCOILBRENTEU |
| 3 | Product cracks and GRM | Monthly GRM above $20, diesel crack against the cap | OGRA price notices https://www.ogra.org.pk ; Topline monthly GRM via Business Recorder https://www.brecorder.com and ProPakistani |
| 4 | Other sector spreads | Urea (international vs local), PVC and PTA (China spot), scrap and HRC, coal vs cement price | World Bank Pink Sheet (`data/macro/`); https://www.sunsirs.com ; SteelOrbis; APCMA https://www.apcma.com |
| 5 | Policy pipeline | ECC, cabinet and CCoE agendas and decisions on any listed sector; how many months a policy has been pending | https://www.finance.gov.pk (ECC press releases); https://cabinet.gov.pk ; https://mopetroleum.gov.pk ; Dawn business |
| 6 | Regulated-price resets | OGRA wellhead gas, OMC and dealer margins, NEPRA tariffs | https://www.ogra.org.pk ; https://www.nepra.org.pk |
| 7 | Trade protection | NTC anti-dumping initiations, provisional and final duties | https://ntc.gov.pk/anti-dumping-investigation-conducted/ |
| 8 | Sponsor and insider buys | A substantial shareholder buys repeatedly in the open market, especially after injecting equity | PSX `insider_trade` class (rule 5.6.1(d) and 5.6.4 letters), `data/announcements.csv` |
| 9 | Volume ignition | 10-day over 120-day volume above 2.5x with a 20-day return above +15%; two or more names in the same sector firing within 10 days | `seed/data/prices`, `scripts/psx_api.py` |
| 10 | PSX "unusual movement" letters | PSX asks a company to explain a move, and it says it knows of no news | PSX announcements, by title |

Exit and veto signals: a price cap or crack cap (the diesel cap from 20 Aug 2026 took the GRM from $36.7 to $28.8), a windfall tax, a rights issue (the PRL risk now), and a reversal of the spread.

Odds for signal 9 alone, all stocks 2017-2026, 60 days, against a random-day placebo:

| | n | Median | Win rate | Worst | Above +50% |
|---|---|---|---|---|---|
| Signal 9 | 788 | −3.4% | 45% | −64% | 6.1% |
| Placebo | 4,588 | −6.9% | 36% | −80% | 3.5% |

So volume ignition is a weak edge on its own and is useful only as confirmation of legs 1 to 3. The combined odds are untested. My judgment is about 1 in 3 for a gain above 50%, so size positions as a high-risk sleeve and not as a core holding.

## 4. Which sectors have this structure now (16 Oct 2026)

Relative returns are against the equal-weight market, computed from `seed/data/prices`.

| Sector, names | Leg 1, ignored earnings | Leg 2, spread | Leg 3, policy | Price now | Read |
|---|---|---|---|---|---|
| E&P: OGDC, PPL, MARI | Partly. FY26 strong, but OGDC's 6% tax rate will not repeat | Strong. Brent $126.6 (14 Oct) against $70 in June; wellhead gas up 8-10% for Jul-Dec (OGRA, 4 Sep) | Pending. Gas circular-debt plan for Rs1.49tr presented, not approved (19 Aug) | 120-day relative −16 to −19 pts, volume 0.4x | Best fit now. Q1FY27 results late Oct are leg 1. Risk: a Hormuz deal |
| OMC: PSO | Yes. FY26 profit 22x (Mettis) | Inventory gains while Brent rises | Margin increase of Rs1.22 approved, not notified; windfall tax risk | 60-day +9 pts, 120-day −15 | Second. Watch the margin notification |
| Gas utilities: SNGP, SSGC | Hidden. Accounts and FY26 FRR delayed to 27 Nov | Regulated return | FRR determination plus the circular-debt plan | 120-day −25 and −33 pts | Same shape as SSGC in 2024 (+475%, `gas_utilities_misc.md`). Binary |
| Autos: SAZEW, HCAR, INDU | Sales 1Q +43% | None; PKR flat | Auto policy draft approved by the PM (Dawn, 14 Sep), still being finalised | SAZEW 120-day −41 pts | Policy leg only. Rate hike risk on 26 Oct |
| Refiners: PRL, ATRL, NRL, CNERGY | Q1FY27 results 20-26 Oct | Cracks high, capped | Cap renewal around 19-20 Oct; deemed duty to zero on 15 Nov | PRL 60-day +112 pts | Late stage. Not a new entry |
| Steel: ASL | Thin | Flat | Colour-coated anti-dumping duty, preliminary only | 15% off peak | Watch for a fourth sponsor filing |
| Chemicals: EPCL, LOTCHEM | No. Margins collapsing (doc 285750) | PVC flat | PVC anti-dumping duty provisional (23 Jul), final pending | 120-day −17 and −20 pts | Fails leg 1 |
| Fertilizer: FFC, EFERT | FFC Q2 +39% | International urea above local | GIDC cess of up to Rs700/bag deferred | flat | Policy risk points the wrong way |

## 5. How to use this

1. Each Monday, scan signals 1, 8 and 9 across the KMI universe. Read signals 2 to 7 for the sectors on the table above.
2. A name with leg 1 goes on the loaded-spring list. Freeze a prediction in `catalysts/frozen_predictions.csv` with the leg 2 or leg 3 event you expect.
3. Enter in a starter size when leg 2 or leg 3 fires. Add on volume ignition. Exit on a veto signal.
4. Score every call. Measured odds should replace the 1-in-3 judgment once there are 10 or more episodes. The next tests to build are the sponsor-buy base rate and the ignored-quarter screen, which needs quarterly EPS history.
