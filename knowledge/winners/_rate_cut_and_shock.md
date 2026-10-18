---
title: "Eight biggest liquid winners that started at a shock low: what they share"
written: 2026-10-18
cases: "TRG_201906, SYS_201906, NRL_201907, UBL_202301, MEBL_202212, GHNI_202301, LUCK_202301, FFBL_202212"
evidence: "data/winners_library.csv (liquid, not suspect, shock or rate-cut flag, largest multiple) and the eight case files"
---

# Rate-cut and shock winners: synthesis

None of the eight starts within 60 sessions of a first rate cut; all carry the shock flag. They start at two index lows only: June to July 2019 (TRG, SYS, NRL) and December 2022 to January 2023 (UBL, MEBL, GHNI, LUCK, FFBL). That is two regime episodes, not eight observations (L16). The largest rate-cut-flagged starts, EPCL (Mar 2020, 4.8x) and CSIL (Aug 2024, 4.9x), rank below.

**Shared signature.** The library start is a market low, but the stock is not the market: the median name needed 140 sessions to reach 1.5x (range 86 to 227). What they share is a first 252-day high on rising value. In the 2023 group it came within five weeks of the IMF agreement (LUCK 30 May, UBL 6 Jul, MEBL 21 Jul), later for GHNI and FFBL; in the 2019 group it came after a crash reclaim. At the 2x close, 3.2x (FFBL) to 6.4x (TRG) was still ahead, but that is conditioned on winning: only 25.6% of liquid first 252-highs gained another 50% within 126 sessions (`tests/winners_population.md`).

**Early or late.** Early entries worked in the 2023 group and lost in the 2019 group, because a second shock followed: TRG at its 3 Jan 2020 high lost 21% to 43% on stops under 40%; SYS bought on 13 Jan 2020 returned 0.77x to 0.87x. Entries at 2x to 3x paid in every case with a wide enough stop; above 5x they stopped paying (TRG 1.3x to 1.9x, GHNI 1.3x to 1.5x, UBL 1.4x to 1.7x, NRL 0.8x to 1.15x).

**Exits that kept the move.** For the index-led banks and cement a 25% closing stop did not fire until the March 2026 shock (UBL 5.8x, LUCK 3.7x) or never (MEBL 6.5x; worst closing drawdown 19.7%). For stock-specific runs the same stop sold the winner repeatedly (TRG at 1.5x, NRL at 0.9x to 1.0x, GHNI at 0.96x). There, 30% to 40% worked (TRG 3.3x, NRL 2.4x, GHNI 4.2x), as did a 100-day-average rule (TRG file) or a 25% stop with re-entry on a new high (TRG 3.1x, GHNI 2.3x). FFBL ended by merger.

**Failures.** Five months of nothing after the low (GHNI 0.79x, MEBL 0.89x, FFBL 0.75x, UBL -16%); entering after the third leg; the fall after the peak (TRG -69%, NRL -78%, UBL -39%, LUCK -33%); KMI status (SYS out for months of the run, TRG and UBL never in).

**Is there one rule?** No. The five 2023 cases share a regime rule: IMF trigger, the sector leader's first 252-high, a 25% stop until the index itself falls 20%. The rest need their own: TRG, buy the reclaim of the pre-crash high with a 30%-plus stop and add nothing above 5x; NRL, size an unexplained mover small; SYS, check the KMI list at each add; FFBL, once the swap ratio is fixed, you hold the acquirer.
