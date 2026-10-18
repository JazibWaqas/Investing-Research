"""Fetch StockAnalysis quarterly income pages for KSE100 members not yet in data/raw/stockanalysis/.

Old tickers map to the current StockAnalysis slug (ENGRO to ENGROH, ICI to LCI, BYCO to CNERGY).
Raw HTML is saved as {SYM}_income.html with the membership symbol, so the parser finds it by name.
"""
import glob
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from cf import get

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/stockanalysis"
SLUG = {"ENGRO": "ENGROH", "ICI": "LCI", "BYCO": "CNERGY"}
URL = "https://stockanalysis.com/quote/psx/{}/financials/income-statement/?p=quarterly"

members = set()
for f in glob.glob(str(ROOT / "data/index_members/KSE100_*.csv")):
    members |= set(pd.read_csv(f).symbol.astype(str).str.strip())
todo = sorted(s for s in members if not (RAW / f"{s}_income.html").exists())
print(len(todo), "to fetch", flush=True)
for s in todo:
    r = get(URL.format(SLUG.get(s, s)))
    ok = r.status_code == 200 and "quarterly" in r.text.lower()
    print(s, r.status_code, "ok" if ok else "NO", flush=True)
    if ok:
        (RAW / f"{s}_income.html").write_text(r.text, encoding="utf-8")
    time.sleep(1.5)
