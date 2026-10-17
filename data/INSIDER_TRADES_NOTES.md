# Insider trades table: sample, coverage, parse rates

Built 2026-10-17 for `tests/insider_cluster_buying.md` (script `scripts/tests/insider_cluster_buying.py`, raw output `tests/out/insider_cluster_buying.txt`). Not committed.

## Files

- `data/insider_trades.csv`: one row per trade line in a sampled filing (973 lines, 877 unique after removing 96 duplicate copies). Columns: doc_id, line, ann_datetime (Asia/Karachi, naive), symbol, holder_name, holder_norm, role, direction, mode, trade_date, shares, price, value_rs, source (pdf_text or pdf_eye), note, dup_of, revoked, qual (qualifying buy or sell, unique, mode market or unstated, direction buy or sell). value_rs is blank where the price is 0 or not stated.
- `data/insider_pdf_reads.txt`: the transcription the CSV is built from (one line per holder per filing; header explains the codes). The 124 PDFs with a text layer were transcribed from the pdfplumber text; the rest were read from page images.
- `data/insider_sample.csv`, `data/insider_drawn_symbols.csv`: the fixed sample and draw (both were committed in b99bb13 before any PDF was opened).
- `data/raw/insider_refetch_drawn.csv`, `data/raw/insider_refetch_2026.csv`: re-fetch of the portal announcement tables used to find hidden documents (see gaps).

## Sample draw (spec 1)

Block a (current): every KMI-list filing with a document dated 2026-06-18 to 2026-10-16, 144 filings. Block b (backtest): current-KMI symbols with at least one filing while point-in-time liquid since 2019-01-01, permuted with numpy default_rng(20261017), whole symbols added in that order until the next would break the 500 cap. Drawn symbols in draw order (22): HCAR, ISL, BIPL, CNERGY, FECTC, WASL, KOHC, GGL, CRTM, BFAGRO, SPL, TELE, EFERT, FFC, NETSOL, GLAXO, SSGC, WAVES, GCWL, RPL, CEPB, CPPL. Next symbol in the order would have broken the cap. 353 backtest filings + 144 current = 497 PDFs (cap 500). Nothing was hand-picked. ASL and AHCL were not drawn; they appear only in block a.

The backtest uses the 22 drawn symbols only (whole filing histories). Block a filings in other symbols are used only for the current list, because a partial history would make cluster dating wrong.

## Parse rates

- 497 PDFs downloaded and read, 0 unreadable. pdf_text 113 (usable text layer), pdf_eye 384 (373 with no text layer, 11 with a garbled one). Three of the 373 have a broken page tree that pdfplumber cannot open; their embedded JPEG was extracted and read.
- Share read by eye by announcement year: 2019 48% of 52, 2020 82% of 38, 2021 94% of 54, 2022 87% of 47, 2023 95% of 39, 2024 100% of 18, 2025 67% of 64, 2026 75% of 185.
- 9 filings have no trade lines (reasons logged in the test output): a 34-page broker statement (PQGTL), a nil return (TELE), board minutes (INKL), two material-information notices about a third-party acquisition (NML, DGKC), a takeover book-closure notice (BIPL 2023), a board-presentation notice (BIPL 2021), a holding list with no transaction (GLAXO), a scheme transfer to the company itself (GGL 2019).
- Transcription check: all 672 unique qualifying lines that carry a price and a trade date sit inside the raw close range (+-10%, +-3 trading days) of the symbol. Five lines in three filings (280203 SKRS, 282600 and 285317 AWTX) failed the first pass: physical-share transfers at prices away from the market, reclassified off_market_block before the final run.

## Conventions

- role: stated in the filing; spouses take the principal's role and holder_norm; sponsor group companies, associated companies and holders of 10% or more are sponsor_substantial. 85 lines with role unknown were filled from the same holder's role in other filings of the same symbol.
- mode: market (CDC ready market through a broker), unstated, rights, bonus, esop, gift_inherit_transfer, off_market_block (NDM, physical, block), tender, other (preference shares, REIT units traded through the futures market, court-scheme allotments). Only market and unstated qualify.
- Duplicates: same symbol, holder_norm, trade_date, direction and shares as a line in an earlier document; the earliest document keeps the trade. Same-document repeats are kept (separate trades). Five groups of byte-identical PDFs (13 files) were found; their trades count once.
- Revoked or revised: no filing carries a revocation notice; one is a corrected re-filing (181996 corrects 181992) and both are kept.

## Gaps

- 6,459 of 13,120 insider_trade rows (49.2%) have no document id. The portal check (5 rows) found one hidden PDF. Cause: `scripts/fetch_announcements.py` matches `\.pdf` case-sensitively, so links ending `.PDF` were stored as no-document. Re-fetching the 22 drawn symbols finds 23 insider rows that do have a PDF (ISL 18, CNERGY 2, CEPB 2, SSGC 1; 2019: 4, 2020: 14, 2021: 3, 2025: 2). The 2026-06-18 to 2026-10-16 window has none. These 23 are outside the fixed 500-PDF sample. The same bug affects every document_ids field in `data/announcements.parquet` for years before 2026; it has not been fixed here.
- Only filings with a document are visible. Clusters are undercounted and singles can be misclassified when a second insider's filing has no document.
- Survivorship: prices exist only for names listed on 2026-10-16.
