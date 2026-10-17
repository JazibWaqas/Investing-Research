"""Fetch payout history for the KMIALLSHR symbol set into data/payouts_raw.csv."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import psx_api
from refresh_prices import ROOT, symbol_set

if __name__ == "__main__":
    syms, _ = symbol_set()
    frames, failed = [], []
    for s in syms:
        try:
            p = psx_api.payouts(s)
            if not p.empty:
                frames.append(p.assign(symbol=s))
        except Exception as e:
            failed.append(s)
            print("FAIL", s, repr(e)[:120], flush=True)
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(ROOT / "data/payouts_raw.csv", index=False)
    print(f"{len(df)} rows, {len(frames)} symbols with payouts, failed {len(failed)}: {failed}")
