"""Poll the PSX announcements page for financial-result filings of given symbols on a given date.

Usage: python -I scripts/poll_results.py EFERT,ATRL 2026-10-19 [--start 16:00] [--every 20]
Polls the portal (X-Req-Id trick, see scripts/psx_api.py) from --start local time every --every minutes
until every symbol has a 'financial result' or 'quarterly' announcement dated that day, then writes
data/results_landed_<date>.txt with the titles and exits. Meant to be run with nohup in the background.
"""
import sys, time, re, datetime as dt, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import psx_api  # noqa: E402

def main():
    syms = sys.argv[1].split(",")
    day = sys.argv[2]
    start = "16:00"; every = 20
    if "--start" in sys.argv: start = sys.argv[sys.argv.index("--start") + 1]
    if "--every" in sys.argv: every = int(sys.argv[sys.argv.index("--every") + 1])
    out = pathlib.Path(__file__).resolve().parent.parent / "data" / f"results_landed_{day}.txt"
    hh, mm = map(int, start.split(":"))
    target = dt.datetime.strptime(day, "%Y-%m-%d").replace(hour=hh, minute=mm)
    while dt.datetime.now() < target:
        time.sleep(min(600, (target - dt.datetime.now()).total_seconds()))
    found = {}
    while len(found) < len(syms):
        try:
            html = psx_api._req("GET", "/announcements/companies").text
        except Exception as e:  # noqa: BLE001
            html = ""; print("fetch error", e, flush=True)
        for s in syms:
            if s in found:
                continue
            pat = re.compile(rf">{s}<.*?</tr>", re.S)
            for row in pat.findall(html):
                if re.search(r"financial result|quarter|period ended", row, re.I) and day.replace("-", "") in re.sub(r"\D", "", row)[:16] or (re.search(r"financial result|period ended", row, re.I)):
                    title = re.sub(r"<[^>]+>", " ", row); title = re.sub(r"\s+", " ", title).strip()[:300]
                    found[s] = title
                    break
        if len(found) < len(syms):
            time.sleep(every * 60)
    out.write_text("\n".join(f"{s}: {t}" for s, t in found.items()), encoding="utf-8")
    print("landed", found, flush=True)

if __name__ == "__main__":
    main()
