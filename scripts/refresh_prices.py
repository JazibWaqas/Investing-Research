"""Write data/prices_raw/{SYM}.csv for every KMIALLSHR symbol in the screener snapshot."""
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import psx_api

ROOT = Path(__file__).parent.parent


def base(sym, known):
    """Strip ex-rights (XD/XB/XR/XA/XE) and NC suffixes if the base is a real symbol."""
    m = re.fullmatch(r"(.+?)(?:XD|XB|XR|XA|XE|NC)+", sym)
    return m.group(1) if m and m.group(1) in known else sym


def symbol_set():
    """Returns (base symbols to fetch, {suffixed: base} mapping that was collapsed)."""
    df = pd.read_csv(ROOT / "seed/data/fundamentals/screener_20261016.csv")
    known = set(pd.read_csv(ROOT / "data/symbols.csv").symbol)
    syms = set(df[df.listed_in.fillna("").str.contains("KMIALLSHR")].symbol.astype(str))
    mapped = {s: base(s, known) for s in syms}
    return sorted(set(mapped.values())), {s: b for s, b in mapped.items() if s != b}


if __name__ == "__main__":
    syms, dups = symbol_set()
    print("collapsed to base:", dups)
    out = ROOT / "data/prices_raw"
    out.mkdir(parents=True, exist_ok=True)
    ok, failed = 0, []
    for s in syms:
        if (out / f"{s}.csv").exists():  # resume: skip files already written
            ok += 1
            continue
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
