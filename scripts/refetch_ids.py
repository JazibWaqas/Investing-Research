"""One-off: re-fetch announcement months START..2026-10 after the .PDF regex fix; rewrites the monthly caches.
Usage: refetch_ids.py [START=2019-01]. On a portal block (403) it waits 5 minutes and retries the month."""
import sys, time; sys.path.insert(0, "scripts")
import fetch_announcements as F, pandas as pd
sy, sm = map(int, (sys.argv[1] if len(sys.argv) > 1 else "2019-01").split("-"))
for y in range(sy, 2027):
    for m in range(1, 13):
        if (y, m) < (sy, sm) or (y, m) > (2026, 10): continue
        while True:
            try:
                F.refresh_key(); rows = F.fetch_month(y, m); break
            except Exception as e:
                print("blocked, waiting", y, m, flush=True); time.sleep(300)
        pd.DataFrame(rows, columns=["datetime", "symbol", "company", "title", "category", "document_ids", "url"]).to_csv(F.CACHE / f"{y}-{m:02d}.csv", index=False)
        print(y, m, len(rows), flush=True)
