# Insider trades table (run 2, full universe) and run 1 notes

Built 2026-10-18 for `tests/insider_cluster_buying.md`. Not committed.

## Run 2: files and pipeline

- `data/insider_trades.csv`: 4,617 rows, one per parsed trade line. Columns: symbol, filing_datetime (Asia/Karachi, naive), trade_date, insider_name, role (sponsor, substantial_shareholder, ceo, director, executive, associate, or blank), direction (buy, sell, unknown), shares, price, value_rs, nature (open_market, unstated, rights, esop, gift, transfer, ipo, buyback, bonus), document_id, extraction_method (pdf_text or ocr), confidence (high, medium, low), duplicate_of (document that filed the same trade first; blank if first). The table also keeps copies flagged by duplicate_of; the test excludes them.
- `data/insider_docs.csv`: one row per PDF read (2,548): method, characters extracted, rows parsed, error.
- `data/insider_universe.csv`: the 195 symbols (129 in `quarterly_eps.csv` plus KMI names ever above Rs5m trailing 60-session median traded value since 2019-01-01; a name that was liquid only in earlier years is included).
- `data/insider_trades_run1.csv`: the run-1 hand-read table (22 random symbols), unchanged.
- `scripts/fetch_announcements.py` (regex fixed), `scripts/refetch_ids.py` (one-off re-fetch of every month 2019-01 to 2026-10), `scripts/fetch_insider_pdfs.py` (downloads to `data/raw/filings/insider/`, 1 request per second per process, resumes, falls back to `.PDF`), `scripts/insider_text.py` (pdfplumber, else Windows OCR via `winocr` at 200 dpi), `scripts/insider_extract.py` (row parser), `scripts/insider_run.py` (builds the two CSVs; extracted text is cached in `data/raw/insider_text/`). OCR: tesseract is not installed; `rapidocr-onnxruntime` was installed first and worked but took 12 to 20 seconds a page on this machine, so Windows' built-in OCR (0.4 seconds a page) is used. Poppler is absent; pages are rendered with pdfplumber. The rapidocr and pdf2image packages stay installed in the venv, unused.

## Coverage by year (universe, insider_trade announcements since 2019-01-01)

| Year | Rows | With PDF | PDFs read | PDFs with at least one trade row | Table rows | Buy | Sell | Direction unknown |
|---|---|---|---|---|---|---|---|---|
| 2019 | 582 | 200 | 200 | 58% | 310 | 227 | 30 | 53 |
| 2020 | 682 | 313 | 313 | 50% | 514 | 212 | 287 | 15 |
| 2021 | 759 | 347 | 347 | 67% | 1,015 | 250 | 705 | 60 |
| 2022 | 585 | 268 | 268 | 49% | 236 | 140 | 69 | 27 |
| 2023 | 611 | 236 | 236 | 53% | 788 | 365 | 375 | 48 |
| 2024 | 613 | 368 | 368 | 74% | 671 | 326 | 324 | 21 |
| 2025 | 899 | 537 | 536 | 72% | 775 | 418 | 331 | 26 |
| 2026 | 714 | 280 | 280 | 66% | 308 | 181 | 108 | 19 |

Years are announcement years. Totals: 5,445 rows, 2,549 with a PDF, 2,548 read, 4,617 table rows (2,119 buy, 2,229 sell, 269 unknown). The 231 document ids gained from the regex fix (119 in the universe) are included. Rows without a PDF (53%) are title-only on the portal.

## Extraction rate

- By method, PDFs with at least one trade row: OCR 58% of 1,817, text layer 76% of 730; overall 63% (1,602 of 2,548). One PDF cannot be opened.
- Confidence: high = price inside the stock's raw high/low range (12% slack) and name, role and direction all present; medium = price checked but name or role missing, or price unverifiable (gift, rights); low = price outside the range, no price, or implausible size. 1,482 high, 2,129 medium, 1,006 low.
- Accuracy against the 497 hand-read PDFs of run 1 (match on trade date and share count): 479 of 840 hand-read lines recovered (57%), 406 of 672 open-market lines (60%); 50-PDF random sample: 46 of 80 lines, 26 of 48 PDFs complete. Parsed rows that match a hand-read line: high 93% (201 of 215), medium 85% (197 of 233), low 48% (81 of 169).
- The 497 PDFs are in the table's input, so this accuracy is a floor check on the parser used to build the table, not a held-out test; the parser was tuned on these.

## Known failure modes

- Dates split over two or three lines ("29" / "June" / "2026" or "November" / "10, 2020"): only the "dd-mm-" / "yyyy" and "dd-mm- ... / yyyy" wraps are repaired.
- Tables where the date cell is on a different line from the share and rate cells; the parser pulls numbers from the next or previous line, which can shift columns (shares read as a rate, a cumulative holding read as shares).
- Garbled text layers (a dozen CRTM and similar PDFs) and OCR noise in names and years ("202s"); a name misread by a letter splits one person in two.
- REIT-unit and futures-market notices (TPLRF1), rights certificates, auditor letters and broker statements: units or a different structure, mostly produce no rows or low-confidence rows.
- Role is blank for 1,043 of 1,496 qualifying sells; boilerplate in the cover letter lists every role, so only the row's own neighbourhood is used.
- Names in the test are matched order-free and merged when one is a token subset of another within a symbol; the table itself keeps the name as read.
- Only the first six pages of each PDF are read.
- The 497 run-1 hand reads also caught lines the parser misses; for the current screen (2026-07-18 on) the SHFA July cluster of run 1 is not recovered.

# Run 1 notes (22 random symbols, hand-read) - kept for provenance

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
