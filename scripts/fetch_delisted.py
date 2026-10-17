"""Fetch full portal history for symbols missing from the price panel (delisted names the portal still serves).
Writes data/prices_delisted/{SYM}.csv and data/prices_delisted_log.csv (symbol, rows, first, last, status)."""
import re, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import psx_api

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "prices_delisted"
sym = pd.read_csv(ROOT / "data/symbols.csv")
panel = set(pd.read_parquet(ROOT / "data/panel_close.parquet").columns)
cand = set(sym[~sym.isDebt & ~sym.isETF].symbol) - panel
ann = pd.read_csv(ROOT / "data/_ann_gone.csv")
cand |= {s for s in ann.symbol.dropna().astype(str) if not re.search(r"(OEF|FUNDS|TFC|SC\d*$|ETF|NSB|PMTFC)", s) and s not in panel and str(s) != "nan"}
cand = sorted(c for c in cand if not re.search(r"(XD|XB|XR)$", c))
log = []
for i, s in enumerate(cand):
    try:
        h = psx_api.historical_full(s)
        st = "ok" if len(h) else "empty"
        if len(h):
            h.to_csv(OUT / f"{s}.csv", index=False)
    except Exception as e:
        h, st = pd.DataFrame(), "err " + str(e)[:60]
    log.append((s, len(h), h.date.min() if len(h) else None, h.date.max() if len(h) else None, st))
    if i % 25 == 0:
        print(i, len(cand), flush=True)
        pd.DataFrame(log, columns=["symbol", "rows", "first", "last", "status"]).to_csv(ROOT / "data/prices_delisted_log.csv", index=False)
pd.DataFrame(log, columns=["symbol", "rows", "first", "last", "status"]).to_csv(ROOT / "data/prices_delisted_log.csv", index=False)
print("done")
