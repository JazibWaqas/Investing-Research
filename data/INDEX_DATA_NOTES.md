# Index membership data: coverage and caveats (built 17 Oct 2026)

Files: `index_changes.csv` (1301 add/delete rows), `index_recomp_log.csv` (79 notices), `index_members/` (50 constituent lists), `kmi_allshare_2026-06-05.csv` (309 names, exact). Rebuild with `.venv/Scripts/python.exe -I scripts/idx_build.py`.

Coverage by notice: KSE100 from 2021 (2017 to 2020 not found anywhere, including Wayback). KSE30 from 2020. KMI30 from mid 2019. KMI All Share from Jan 2019. MSCI Pakistan from Pakistani press only, with gaps (Nov 2017, Nov 2020, Feb and Aug 2022, most of 2023, Aug 2025). FTSE: one 2017 event only.

Caveats: four rows are derived from list differences (source_url = derived, no announce date). `KMI_ALL_derived_*.csv` lists are rolled back from the exact 2026 list and sit 0 to 7 names above each notice's stated total. Older KMI All Share PDFs hold a Shariah screening table, not the membership list. Ticker renames to watch: BYCO to CNERGY, ENGRO to ENGROH, ICI to LCI. Mapping of "Attock Gen (AGL)" to AGL (Feb 2024 MSCI small cap) is unconfirmed. Any index event test must use announce_date, and must drop derived rows.
