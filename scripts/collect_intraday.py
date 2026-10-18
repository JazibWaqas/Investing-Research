"""Archive intraday trades to data/intraday/{session date}/{SYM}.csv (columns ts, price, volume).

Universe: every symbol in data/kmi_allshare_2026-06-05.csv, plus any data/prices_raw symbol whose
median close*volume over its last 60 sessions is above Rs5m (a proxy: the portal gives no traded value).
The portal serves only the current session, so run after the close every trading day. The session is the
latest PKT date in this run's responses; quiet names can return older trades, which are dropped. ts is unix
seconds (UTC); PKT is UTC+5. Idempotent: a symbol whose file for that session exists is not rewritten.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import psx_api

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data/intraday"
MIN_MEDIAN_VALUE = 5_000_000  # Rs


def universe():
    kmi = set(pd.read_csv(ROOT / "data/kmi_allshare_2026-06-05.csv").symbol.astype(str))
    liquid = set()
    for f in (ROOT / "data/prices_raw").glob("*.csv"):
        p = pd.read_csv(f).tail(60)
        if (p.close * p.volume).median() > MIN_MEDIAN_VALUE:
            liquid.add(f.stem)
    return sorted(kmi | liquid)


def pkt_date(ts):
    return pd.to_datetime(ts, unit="s", utc=True).dt.tz_convert("Asia/Karachi").dt.strftime("%Y-%m-%d")


if __name__ == "__main__":
    syms = universe()
    print("universe", len(syms), flush=True)
    got, failed, empty = {}, [], []
    for s in syms:
        try:
            df = psx_api.intraday(s)
        except Exception as e:
            failed.append(s)
            print("FAIL", s, repr(e)[:120], flush=True)
            continue
        if df.empty:
            empty.append(s)
        else:
            got[s] = df
    session = max(pkt_date(df.ts).max() for df in got.values())  # latest session the portal served
    saved, skipped = {}, []
    for s, df in got.items():
        path = OUT / session / f"{s}.csv"
        if path.exists():  # idempotent: already saved for this session
            skipped.append(s)
            continue
        today = df[pkt_date(df.ts) == session]
        if today.empty:
            empty.append(s)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        today.sort_values("ts").to_csv(path, index=False)
        saved[s] = len(today)
    print(f"session {session}: saved {len(saved)} symbols, {sum(saved.values())} rows; "
          f"skipped {len(skipped)}; no session trades {len(empty)}; failed {len(failed)} {failed}", flush=True)
