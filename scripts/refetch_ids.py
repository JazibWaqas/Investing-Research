"""One-off: re-fetch announcement months 2019-01..2026-10 after the .PDF regex fix; rewrites the monthly caches."""
import sys; sys.path.insert(0, "scripts")
import fetch_announcements as F, pandas as pd
F.refresh_key()
for y in range(2019, 2027):
    for m in range(1, 13):
        if (y, m) > (2026, 10): break
        rows = F.fetch_month(y, m)
        pd.DataFrame(rows, columns=["datetime", "symbol", "company", "title", "category", "document_ids", "url"]).to_csv(F.CACHE / f"{y}-{m:02d}.csv", index=False)
        print(y, m, len(rows), flush=True)
