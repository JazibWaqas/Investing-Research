"""update_prices.py: append new sessions to every data/prices_raw/{SYM}.csv and to the index files in data/macro/.

    .venv\\Scripts\\python.exe -I -X utf8 scripts\\update_prices.py            # everything older than today
    .venv\\Scripts\\python.exe -I -X utf8 scripts\\update_prices.py MEBL LUCK  # only these

refresh_prices.py writes a file only if it is missing; this script is the incremental step for the weekly loop.
It refetches the full history from the portal (one POST per symbol, about a second each) and keeps the rows
after the file's last date, so a corrected close in the portal's last days is not overwritten. Index files
(KSE100, KSE100PR, KMI30, KMIALLSHR, KSE30) are updated the same way; their `value` column mirrors `close`.
"""
import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import psx_api

ROOT = Path(__file__).resolve().parents[1]
INDEX = {"KSE100": "kse100.csv", "KSE100PR": "kse100pr.csv", "KMI30": "kmi30.csv", "KMIALLSHR": "kmiallshr.csv", "KSE30": "kse30.csv"}


def update(path, sym):
    old = pd.read_csv(path, parse_dates=["date"])
    last = old["date"].max()
    if last.date() >= date.today():
        return 0
    new = psx_api.historical_full(sym)
    if new.empty:
        return 0
    new = new[new["date"] > last].sort_values("date")
    if new.empty:
        return 0
    if "value" in old.columns:
        new = new.assign(value=new["close"])
    out = pd.concat([old, new[old.columns]], ignore_index=True)
    out.to_csv(path, index=False)
    return len(new)


def main(only):
    files = [(ROOT / "data/prices_raw" / f"{s}.csv", s) for s in only] if only else \
            [(p, p.stem) for p in sorted((ROOT / "data/prices_raw").glob("*.csv"))]
    if not only:
        files += [(ROOT / "data/macro" / f, s) for s, f in INDEX.items()]
    added, failed = 0, []
    for path, sym in files:
        try:
            n = update(path, sym)
            added += n
        except Exception as e:  # keep going; report at the end
            failed.append(f"{sym}: {e!r}"[:120])
        time.sleep(0.6)
    print(f"{len(files)} files, {added} rows added, {len(failed)} failed")
    for f in failed:
        print(" ", f)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
