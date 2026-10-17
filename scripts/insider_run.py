"""Extract trade rows from every downloaded insider PDF -> data/insider_trades.csv (+ data/insider_docs.csv, one status row per PDF).
Resumes from data/raw/insider_extract_cache.jsonl. Usage: insider_run.py   (reads data/announcements.parquet, data/insider_universe.csv)"""
import json, re, sys
from pathlib import Path

import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from insider_text import pdf_text
from insider_extract import parse

CACHE = ROOT / "data/raw/insider_extract_cache.jsonl"
PDFS = ROOT / "data/raw/filings/insider"

ann = pd.read_parquet(ROOT / "data/announcements.parquet")
U = set(pd.read_csv(ROOT / "data/insider_universe.csv").symbol)
a = ann[(ann.klass == "insider_trade") & (ann.datetime >= "2019-01-01") & ann.symbol.isin(U) & (ann.document_ids != "")].copy()
a["doc"] = a.document_ids.str.split(",")
a = a.explode("doc").drop_duplicates("doc")
a["filed"] = a.datetime.dt.tz_convert("Asia/Karachi").dt.tz_localize(None)
meta = a.set_index("doc")[["symbol", "filed", "title"]]

done = set()
if CACHE.exists():
    done = {json.loads(l)["doc"] for l in CACHE.open(encoding="utf-8")}
todo = [d for d in meta.index if d not in done and (PDFS / f"{d}.pdf").exists()]
print(len(meta), "docs in universe,", len(done), "done,", len(todo), "to do", flush=True)
with CACHE.open("a", encoding="utf-8") as out:
    for k, d in enumerate(todo):
        sym, filed = meta.loc[d, "symbol"], meta.loc[d, "filed"]
        txt, method = pdf_text(PDFS / f"{d}.pdf")
        try:
            rows = parse(txt, filed, sym) if txt.strip() else []
            err = ""
        except Exception as e:
            rows, err = [], f"parse_error:{type(e).__name__}"
        for r in rows:
            r["trade_date"] = r["trade_date"].strftime("%Y-%m-%d")
        out.write(json.dumps(dict(doc=d, method=method, err=err or (method if method.startswith("error") else ""), n=len(rows), chars=len(txt), rows=rows), default=str) + "\n")
        out.flush()
        if k % 100 == 0:
            print(k, d, method, len(rows), flush=True)


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


rows, docs = [], []
for l in CACHE.open(encoding="utf-8"):
    j = json.loads(l)
    docs.append(dict(document_id=j["doc"], symbol=meta.loc[j["doc"], "symbol"], filing_datetime=meta.loc[j["doc"], "filed"], extraction_method=j["method"],
                     chars=j["chars"], n_rows=j["n"], error=j["err"]))
    for r in j["rows"]:
        r.update(document_id=j["doc"], symbol=meta.loc[j["doc"], "symbol"], filing_datetime=meta.loc[j["doc"], "filed"], extraction_method=j["method"])
        r["confidence"] = conf(r)
        rows.append(r)
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
