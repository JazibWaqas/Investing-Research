"""Extract trade rows from every downloaded insider PDF -> data/insider_trades.csv (+ data/insider_docs.csv, one status row per PDF).
Text is cached in data/raw/insider_text/. Usage: insider_run.py   (reads data/announcements.parquet, data/insider_universe.csv)"""
import json, re, sys
from pathlib import Path

import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from insider_text import pdf_text
from insider_extract import parse

PDFS = ROOT / "data/raw/filings/insider"

ann = pd.read_parquet(ROOT / "data/announcements.parquet")
U = set(pd.read_csv(ROOT / "data/insider_universe.csv").symbol)
a = ann[(ann.klass == "insider_trade") & (ann.datetime >= "2019-01-01") & ann.symbol.isin(U) & (ann.document_ids != "")].copy()
a["doc"] = a.document_ids.str.split(",")
a = a.explode("doc").drop_duplicates("doc")
a["filed"] = a.datetime.dt.tz_convert("Asia/Karachi").dt.tz_localize(None)
meta = a.set_index("doc")[["symbol", "filed", "title"]]

TXT = ROOT / "data/raw/insider_text"   # extracted text is cached so the parser can be re-run without re-OCR
TXT.mkdir(parents=True, exist_ok=True)
rows, docs = [], []
for k, d in enumerate(meta.index):
    if not (PDFS / f"{d}.pdf").exists():
        continue
    sym, filed = meta.loc[d, "symbol"], meta.loc[d, "filed"]
    f = TXT / f"{d}.txt"
    if f.exists():
        raw = f.read_text(encoding="utf-8"); method, txt = raw.split(chr(10), 1)
    else:
        txt, method = pdf_text(PDFS / f"{d}.pdf")
        if not method.startswith("error"):
            f.write_text(method + chr(10) + txt, encoding="utf-8")
    try:
        got, err = (parse(txt, filed, sym) if txt.strip() else []), ""
    except Exception as e:
        got, err = [], f"parse_error:{type(e).__name__}"
    err = err or (method if method.startswith("error") else "")
    docs.append(dict(document_id=d, symbol=sym, filing_datetime=filed, extraction_method=method, chars=len(txt), n_rows=len(got), error=err))
    for r in got:
        r["trade_date"] = r["trade_date"].strftime("%Y-%m-%d")
        r.update(document_id=d, symbol=sym, filing_datetime=filed, extraction_method=method)
        rows.append(r)
    if k % 200 == 0:
        print(k, d, method, len(got), flush=True)


def conf(r):
    ok = r["_price_ok"]
    full = bool(r["insider_name"]) and bool(r["role"]) and r["direction"] in ("buy", "sell")
    if r["shares"] is None or r["shares"] < 1 or r["shares"] > 2e9 or (r["value_rs"] or 0) > 5e9:
        return "low"
    if ok and full:
        return "high"
    if ok or (ok is None and r["price"] is not None and r["direction"] in ("buy", "sell") and r["insider_name"]):
        return "medium"
    return "low"


for r in rows:
    r["confidence"] = conf(r)
T = pd.DataFrame(rows).drop(columns="_price_ok")
cols = ["symbol", "filing_datetime", "trade_date", "insider_name", "role", "direction", "shares", "price", "value_rs", "nature", "document_id", "extraction_method", "confidence"]
T = T[cols].sort_values(["filing_datetime", "document_id"]).reset_index(drop=True)
# the same trade filed again in a later document (re-filings, copies) counts once; repeats inside one document are kept
T["_k"] = list(zip(T.symbol, T.insider_name.str.upper(), T.trade_date, T.direction, T.shares))
first = T.groupby("_k").document_id.transform("first")
dup = T.document_id != first
T["duplicate_of"] = np.where(dup, first, "")
print(len(T), "rows,", int(dup.sum()), "copies in later documents (kept, flagged duplicate_of)")
T.drop(columns="_k").to_csv(ROOT / "data/insider_trades.csv", index=False)
pd.DataFrame(docs).to_csv(ROOT / "data/insider_docs.csv", index=False)
