"""Fetch PSX portal daily history for KSE100 members with no price file in data/prices_*/.

Uses psx_api.historical_full (same source as the repo's price panels). Output: data/raw/macro/psx_hist/{SYM}.csv.
Old tickers map to the portal code (ENGRO to ENGROH, ICI to LCI, BYCO to CNERGY).
"""
import glob
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import psx_api

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/raw/macro/psx_hist"
SLUG = {"ENGRO": "ENGROH", "ICI": "LCI", "BYCO": "CNERGY"}

members = set()
for f in glob.glob(str(ROOT / "data/index_members/KSE100_*.csv")):
    members |= set(pd.read_csv(f).symbol.astype(str).str.strip())


def have(s):
    return any((ROOT / "data" / f / f"{n}.csv").exists() for f in ("prices_raw", "prices_listed_missing", "prices_delisted") for n in (s, SLUG.get(s, s)))


OUT.mkdir(parents=True, exist_ok=True)
todo = sorted(s for s in members if not have(s))
print(len(todo), "to fetch", flush=True)
for s in todo:
    try:
        df = psx_api.historical_full(SLUG.get(s, s))
        df.to_csv(OUT / f"{s}.csv", index=False)
        print(s, len(df), df.date.min(), df.date.max(), flush=True)
    except Exception as e:
        print(s, "FAIL", repr(e)[:120], flush=True)
    time.sleep(1.0)
