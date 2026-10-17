# What Rs50,000 could have become through active PSX trading

**Evidence date: 18 October 2026. Price and index data end 16 October 2026.** This is an independent fixed-capital experiment, not a monthly-deposit simulation. Its executable rules were saved in [the preregistration](../scripts/codex/active_trading_spec.md) before the first run; [the independent loader and engine](../scripts/codex/active_trading.py) produce [all raw figures and monthly selections](out/active_trading_codex.txt). No result below assumes that the investor knew the later winning stocks.

## Design and limits

Each cohort starts with **Rs50,000 once**, on the stated start session, and ends at the last session of its two-year interval. I freeze names with at least 40 quotes in the preceding 60 sessions and median *raw* close times volume of Rs5m or more. The universe has 47 to 86 names. From 2019 I intersect that list with the latest available KMI All Share membership list. Those older lists were **derived retrospectively** from later membership, so their reconstruction can contain survivorship or classification errors. No KMI All Share membership list exists here before 2019. The 2016 and 2018 cohorts therefore use liquid PSX-panel names as a broader proxy, not a verified Shariah universe. All five cohorts also inherit the adjusted panel's exclusion of firms delisted before October 2026.

The panel adjusts bonuses and splits. Its cash dividend coverage becomes reasonably complete only in November 2024. Thus earlier stock returns mostly omit distributions; 2024–26 stock returns include recorded dividends. The KMI All Share and KSE100 columns are **total-return** indices throughout. I neither add a trailing yield to the adjusted panel nor pretend that older stock and index figures are perfectly comparable. A stock missing an occasional daily quote retains its last close for mark-to-market, but it cannot be newly bought at a missing close. Stale prices and later delistings remain execution risks. All amounts are nominal PKR, with no tax or USD conversion.

The seven systems choose up to three equally weighted names at the first trading close of each month, using information available by the preceding session's close. Holdings drift between rebalances; an empty screen holds cash. Entry and exit each cost 0.25%, for 0.5% round trip. Each side costs a further 0.25% if the preceding 20-session median traded value is below Rs20m. The engine permits fractional shares and close-price fills; real Rs50,000 orders may have additional rounding and execution loss. Completed position episodes supply trade hit rate and median trade return; daily marked NAV supplies maximum drawdown. For each cohort, 200 seeded paths rotate among three randomly chosen eligible names every month under identical costs. Their percentile is a **within-window placebo**, not an out-of-sample probability or a statistical confidence level.

## The opportunity set

Buy and hold means buying each start-liquid name once and selling it at the end, including the same costs. `n` is the number with valid terminal prices; mean, median, win rate, worst and threshold shares refer to that cross-section. The hindsight column chooses the subsequent best-performing name **every month**, then compounds those choices with costs. It uses future prices and is an unattainable ceiling, not an estimate of trading skill. The 2024–26 oracle's 25 monthly selections had a 1.47x median monthly gross return, which explains why its compound multiple becomes absurdly large.

| Start to end | Universe / n | Buy-hold mean / median | Win / worst | Share ≥2x / ≥3x / ≥5x | KMI TR / KSE100 TR | Hindsight ceiling |
|---|---:|---:|---:|---:|---:|---:|
| 30 Dec 2016–28 Dec 2018 | 86 / 83 | 0.76x / 0.63x | 17% / 0.19x | 4.8% / 1.2% / 0% | 0.80x / 0.78x | 621x |
| 1 Oct 2018–30 Sep 2020 | 69 / 69 | 0.98x / 0.89x | 36% / 0.46x | 4.3% / 0% / 0% | 1.02x / 0.99x | 440x |
| 1 Oct 2020–30 Sep 2022 | 69 / 68 | 0.93x / 0.78x | 31% / 0.23x | 4.4% / 1.5% / 0% | 1.02x / 1.01x | 801x |
| 3 Oct 2022–30 Sep 2024 | 47 / 47 | 1.44x / 1.20x | 68% / 0.52x | 21.3% / 2.1% / 0% | 1.73x / 1.97x | 2,111x |
| 1 Oct 2024–16 Oct 2026 | 84 / 84 | 1.74x / 1.53x | 81% / 0.27x | 31.0% / 9.5% / 1.2% | 1.81x / 2.03x | 25,906x |

The top ten buy-and-hold names expose how much the result depended on sector and stock selection. These are **terminal winners**, never a proposed entry list. Multiples include one entry and exit charge.

| Start | Ten strongest start-liquid stocks, symbol (sector, multiple) |
|---|---|
| 2016 | AVN (technology, 3.07); SAZEW (auto, 2.81); LOTCHEM (chemical, 2.03); EPCL (chemical, 2.02); DOL (chemical, 1.74); MEBL (bank, 1.45); ANL (textile, 1.38); NETSOL (technology, 1.33); STCL (glass, 1.33); SYS (technology, 1.24) |
| 2018 | SYS (technology, 2.53); FEROZ (pharma, 2.38); PIOC (cement, 2.04); KOHC (cement, 1.90); CHCC (cement, 1.63); DOL (chemical, 1.51); TGL (glass, 1.36); ACPL (cement, 1.35); EPCL (chemical, 1.34); MUGHAL (engineering, 1.33) |
| 2020 | SYS (technology, 3.09); LOTCHEM (chemical, 2.39); MTL (auto, 2.10); EPCL (chemical, 1.90); MEBL (bank, 1.89); NETSOL (technology, 1.60); GGL (chemical, 1.53); NRL (refinery, 1.39); UNITY (food, 1.39); EFERT (fertilizer, 1.28) |
| 2022 | GAL (auto, 3.79); HUBC (power, 2.76); MEBL (bank, 2.66); PIOC (cement, 2.66); MARI (E&P, 2.43); FLYNG (cement, 2.43); EFERT (fertilizer, 2.43); OGDC (E&P, 2.28); ATRL (refinery, 2.18); GHNI (auto, 2.15) |
| 2024 | QUICE (food, 5.35); PRL (refinery, 4.46); POWER (cement, 3.95); ATRL (refinery, 3.81); THCCL (cement, 3.68); CNERGY (refinery, 3.34); NRL (refinery, 3.18); GHNI (auto, 3.17); MEBL (bank, 2.86); SSGC (gas marketing, 2.68) |

For the investor's amount, the 2024–26 KMI and KSE100 index multiples imply about **Rs90,375 and Rs101,718**. Buying the one best name at the start, QUICE, implies about **Rs267,500**, but selecting it from 84 names required knowing the finish. The ceiling implies roughly Rs1.30 billion from Rs50,000. That is a mathematical demonstration of selection hindsight, not a feasible best-case payoff. An investor trying to implement the oracle would also encounter circuit limits, thin order books, stale quotes and adverse fill prices beyond the simple slippage charge.

## Seven rules, frozen before the run

`MOM63` and `MOM252` buy the top positive 63- and 252-session price returns. `HIGH52` buys names within 2% of their trailing 252-session high, ranked by 63-session return. `DIP200` buys the deepest one-month falls below -5% while price stays above its 200-session average. `SECTOR63` takes the strongest stock from each of the three sectors with the highest median 63-session returns. `VOL20` requires recent average volume at least twice the earlier 120-session average and a positive one-month price return. `EPS_YOY` buys the strongest positive year-on-year quarterly EPS changes announced within the previous 60 days; the source does **not** certify whether group EPS is consolidated. No sector or event category was selected after inspecting this study's winners. Policy rates, T-bills and Brent were deliberately not turned into regime overrides: that would add unstated discretion to a frozen menu.

The next table gives every net capital multiple. The strongest tested rule in 2024–26 is marked in bold. A 2x system means Rs100,000 from the initial Rs50,000, before tax.

| System | 2016–18 | 2018–20 | 2020–22 | 2022–24 | 2024–26 |
|---|---:|---:|---:|---:|---:|
| MOM63 | 0.99x | 1.23x | 1.84x | 2.04x | 1.50x |
| MOM252 | 1.10x | 0.74x | 0.75x | 1.51x | 1.79x |
| HIGH52 | 0.89x | 1.08x | 3.34x | 2.09x | **2.62x** |
| DIP200 | 0.83x | 0.76x | 0.76x | 1.43x | 0.94x |
| SECTOR63 | 0.71x | 0.91x | 1.69x | 3.46x | 0.78x |
| VOL20 | 1.02x | 0.45x | 1.03x | 0.80x | 2.02x |
| EPS_YOY | 1.00x* | 1.00x* | 0.83x | 1.50x | 1.22x |

*No qualified EPS trade existed in the first two cohorts; the 1.00x entries are cash, not wins. In 2024–26 HIGH52 and VOL20 reached 2x; **none** reached 3x. HIGH52 had reached 3.34x in 2020–22 and 2.09x in 2022–24, but lost 11% in 2016–18. VOL20 lost 55% in 2018–20. SECTOR63 reached 3.46x in 2022–24 and then lost 22% in 2024–26. One spectacular window is insufficient proof of a reusable edge.*

| 2024–26 rule | End Rs | CAGR | Max drawdown | Completed trades | Hit rate | Median trade | Random percentile |
|---|---:|---:|---:|---:|---:|---:|---:|
| MOM63 | 75,041 | 22% | -49% | 44 | 55% | +2.5% | 57th |
| MOM252 | 89,270 | 33% | -39% | 30 | 37% | -1.7% | 77th |
| HIGH52 | 130,953 | 60% | -35% | 53 | 62% | +4.6% | 95th |
| DIP200 | 47,101 | -3% | -45% | 58 | 47% | -0.6% | 9th |
| SECTOR63 | 39,184 | -11% | -50% | 55 | 38% | -1.7% | 2nd |
| VOL20 | 100,781 | 41% | -39% | 51 | 33% | -2.0% | 86th |
| EPS_YOY | 61,069 | 10% | -42% | 39 | 44% | -2.2% | 30th |

The 2024–26 random paths had **n=200, mean 1.53x, median 1.42x, win rate 89%, worst 0.72x and 90th percentile 2.20x**. The placebo itself benefited from a broad bull market. HIGH52 beat 95% of those paths, but selecting the best of seven rules after seeing all seven outcomes weakens that comparison. The same rule ranked above the random median in five of five cohorts, with median placebo percentile 96th, median capital multiple 2.09x and worst 0.89x. MOM63 also ranked above the placebo median in all five, but its 2024–26 gain was only 1.50x with a 49% drawdown. SECTOR63 did so in four of five, yet its worst result was 0.71x. HIGH52 is the most stable **within this menu and sample**; five overlapping market regimes and retrospectively reconstructed membership do not establish a live edge. The raw file gives CAGR, drawdown, trade count, hit rate, median trade and placebo percentile for every rule in every window.

## What the contemporaneous story could actually identify

[AHL's 27 June 2025 FY25 review](https://arifhabibltd.com/api/research/open?path=178/685ee97b720f2c38da31add0.pdf) attributed the market rally to rate cuts, improved liquidity and valuation recovery. Its FY25 stock gainers included NBP, GLAXO and FFC, while its sector leaders included OMCs, fertilizer and cement. [Mettis on 2 July 2025](https://mettisglobal.news/PSX-in-FY25-From-Oof-to-Boom-53554) identified FFC, UBL, MARI, LUCK, OGDC and MEBL as the largest index-point contributors. These are contribution rankings, which favor large-cap names, rather than the highest percentage returns in this study's fixed liquid cohort. The publicly visible easing story could justify an invested cyclicals or yield basket, but it did not specify a monthly rule that picked the final top-ten names in advance. AHL also mentioned MSCI additions; an inclusion announcement is already public information, and this menu does not demonstrate a profitable post-announcement entry.

[Mettis's 1 July 2026 FY26 account](https://mettisglobal.news/PSX-in-FY26-Rides-Out-the-Storm-61507) named FFC, UBL, HUBC, ENGROH and MEBL among the largest positive index contributors, with banks, fertilizer and E&P leading by index points. It also recorded the sharp March decline and recovery. The 2024–26 *stock-multiple* list here is different: four refiners and three cement names occupy seven of ten places. That distinction matters for a Rs50,000 trader targeting multiples rather than index points. [Profit reported Sazgar's FY25 Haval sales growth on 12 June 2025](https://profit.pakistantoday.com.pk/2025/06/12/car-bike-sales-accelerate-in-may-11-month-volumes-up-39-yoy), and [its record March-quarter FY26 profit on 27 April 2026](https://profit.pakistantoday.com.pk/2026/04/27/as-haval-sales-soar-sazgar-posts-record-profits/). Those dated disclosures made an auto growth thesis observable, but they did not promise the later share multiple.

The refinery thesis offers the clearest timeline test. [Business Recorder reported on 8 July 2026](https://www.brecorder.com/news/40429000/) that an upgrade policy had been submitted to Cabinet; its [10 July account](https://www.brecorder.com/news/40429386/) described implementation hurdles. [Approval came on 28 July](https://www.brecorder.com/news/40432152/), when Topline explicitly favored PRL, NRL and ATRL. [Business Recorder on 26 September](https://www.brecorder.com/news/40441304/) reported that sector FY26 profit swung from loss to Rs54.8bn, driven by wider fuel margins and volumes. A rule to buy refiners on **8 July** could have acted before final approval, but had policy and earnings risk; a rule to buy on **28 July** could only capture the remaining move. Neither policy rule was preregistered or backtested here, so its realized gain is **unverified**. The rule that did reach 2x, HIGH52, correlated with sustained price leadership, not advance knowledge of the upgrade policy. `EPS_YOY` did not validate a mechanical results-day edge, and the announcement file's insider direction is too uncertain to assert that “follow sponsor buying” would have captured the winners. No MSCI/KMI inclusion or sponsor rule is credited with hypothetical profits.

## Verdict (about 250 words)

The answer is a **range with a named rule**. A random monthly-rotation path in 2024–26 ended at a median **Rs70,800**; the KMI total-return index reached **Rs90,400**. A good active outcome was the 252-session momentum rule's **Rs89,270**, or 1.79x, with a **39%** maximum drawdown. The best tested rule was the 52-week-high screen's **Rs130,953**, or 2.62x, with **53 trades**, a **62%** hit rate, a **4.6%** median trade and a **35%** drawdown. It was selected after comparing seven systems, so Rs131,000 is a historical good-luck outcome, not a forecast. The KSE100 total-return index reached Rs101,700, above six active systems.

The same 52-week-high rule turned Rs50,000 into **Rs166,806** in 2020–22 and **Rs104,472** in 2022–24, but only **Rs44,733** in 2016–18 and **Rs53,799** in 2018–20. The 2022–24 sector rule reached **Rs173,041**, then fell to **Rs39,184** in 2024–26. The edge is suggestive because the panel omits delistings, older dividends are missing and historical membership was reconstructed.

For a 22-year-old adding Rs50,000 monthly, I would allow an **active sleeve of at most 20–25% of deposits**, with a written signal, cost log and comparison to a liquid KMI core. I would start with the 52-week-high screen as a research candidate. The rest should stay systematically invested. This assumes a 35–50% sleeve drawdown would not interrupt the savings habit.
