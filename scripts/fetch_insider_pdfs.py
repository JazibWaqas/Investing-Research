"""Download every insider_trade PDF (2019-01-01 on) for the symbols in data/insider_universe.csv into data/raw/filings/insider/.
Resumes (skips files already there). 1 request/second. Files are only ever read as data, never executed.
Usage: fetch_insider_pdfs.py [rev|mid]   (rev walks the list oldest first, so a second copy can share the work at 2 requests/second in total)"""
import sys
import time
from pathlib import Path

import pandas as pd
from curl_cffi import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/raw/filings/insider"
LOG = ROOT / "data/raw/insider_downloads.log"
S = requests.Session(impersonate="chrome")
OUT.mkdir(parents=True, exist_ok=True)

ann = pd.read_parquet(ROOT / "data/announcements.parquet")
U = set(pd.read_csv(ROOT / "data/insider_universe.csv").symbol)
u = ann[(ann.klass == "insider_trade") & (ann.datetime >= "2019-01-01") & ann.symbol.isin(U) & (ann.document_ids != "")]
ids = sorted(set(u.document_ids.str.split(",").explode()), key=int, reverse=True)
todo = [i for i in ids if not (OUT / f"{i}.pdf").exists()]
print(len(ids), "ids,", len(todo), "to fetch", flush=True)
order = todo[::-1] if "rev" in sys.argv else todo[len(todo) // 2:] + todo[:len(todo) // 2] if "mid" in sys.argv else todo
for k, i in enumerate(order):
    if (OUT / f"{i}.pdf").exists():
        continue
    time.sleep(1)
    status = "fail"
    for attempt in range(3):
        try:
            r = S.get(f"https://dps.psx.com.pk/download/document/{i}.pdf", timeout=60)
            if r.status_code == 404:   # the portal is case-sensitive: links ending .PDF only resolve with the capital extension
                time.sleep(1)
                r = S.get(f"https://dps.psx.com.pk/download/document/{i}.PDF", timeout=60)
            if r.status_code == 200 and r.content[:5] == b"%PDF-":
                (OUT / f"{i}.pdf").write_bytes(r.content); status = f"ok\t{len(r.content)}"; break
            status = f"http{r.status_code}"
            if r.status_code == 404: break
        except Exception as e:
            status = type(e).__name__
        time.sleep(5)
    with LOG.open("a") as f:
        f.write(f"{i}\t{status}\n")
    if k % 100 == 0:
        print(k, i, status, flush=True)
print("done", flush=True)
