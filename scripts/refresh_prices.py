"""Write data/prices_raw/{SYM}.csv for every KMIALLSHR symbol in the screener snapshot."""
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import psx_api

ROOT = Path(__file__).parent.parent


def symbol_set():
    df = pd.read_csv(ROOT / "seed/data/fundamentals/screener_20261016.csv")
    syms = set(df[df.listed_in.fillna("").str.contains("KMIALLSHR")].symbol.astype(str))
    # ex-dividend/bonus/right duplicates (e.g. LUCKXD) are skipped when the base is present
    dups = {s for s in syms if re.fullmatch(r"(.+?)(XD|XB|XR|XA|XE)", s) and re.fullmatch(r"(.+?)(XD|XB|XR|XA|XE)", s).group(1) in syms}
    return sorted(syms - dups), sorted(dups)


if __name__ == "__main__":
    syms, dups = symbol_set()
    print("skipped ex-duplicates:", dups)
    out = ROOT / "data/prices_raw"
    out.mkdir(parents=True, exist_ok=True)
    ok, failed = 0, []
    for s in syms:
        try:
            df = psx_api.historical_full(s)
            if df.empty:
                raise ValueError("no history")
            df.to_csv(out / f"{s}.csv", index=False)
            ok += 1
        except Exception as e:
            failed.append(s)
            print("FAIL", s, repr(e)[:120], flush=True)
    print(f"written {ok}, failed {len(failed)}: {failed}")
