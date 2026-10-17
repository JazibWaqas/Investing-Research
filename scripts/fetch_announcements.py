"""Scrape all PSX company announcements (global archive back to Jan 2005) and classify.

Archive: POST dps.psx.com.pk/announcements type=C, date_from/date_to, count<=100, offset.
Fetched month by month; each finished month is cached in data/raw/announcements/YYYY-MM.csv
(resume = skip existing; current and previous month always refetched). 1 request/second.
Usage: fetch_announcements.py [START=2005-01]   (use --classify-only to reclassify from cache)
"""
import calendar, re, sys, time
from datetime import date
from pathlib import Path

import pandas as pd
from curl_cffi import requests
from lxml import html

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data/raw/announcements"
BASE = "https://dps.psx.com.pk"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
S = requests.Session(impersonate="chrome")
H = {"User-Agent": UA, "X-Requested-With": "XMLHttpRequest"}


def refresh_key():
    page = S.get(f"{BASE}/company/MEBL", headers={"User-Agent": UA}).text
    H["X-Req-Id"] = re.search(r"_k\W+([\w-]+)", page).group(1)


def post(**d):
    for attempt in range(5):
        time.sleep(1)
        try:
            r = S.post(f"{BASE}/announcements", data=d, headers=H, timeout=60)
            if r.status_code == 200 and "tbl__body" in r.text or "0 of 0 entries" in r.text:
                return r.text
        except Exception as e:
            print("retry", e, flush=True)
        refresh_key()
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"failed {d}")


def parse(doc):
    out = []
    for tr in html.fromstring(doc).xpath('//table[@id="announcementsTable"]/tbody/tr'):
        td = tr.xpath("td")
        if len(td) < 6:
            continue
        ids = re.findall(r"/download/document/(\d+)\.pdf", html.tostring(td[5]).decode())
        out.append(dict(
            datetime=pd.to_datetime(f"{td[0].text_content().strip()} {td[1].text_content().strip()}", format="%b %d, %Y %I:%M %p"),
            symbol=td[2].text_content().strip(), company=td[3].text_content().strip(),
            title=" ".join(td[4].text_content().split()), category="Companies Announcements",
            document_ids=",".join(ids), url=f"{BASE}/download/document/{ids[0]}.pdf" if ids else ""))
    return out


def fetch_month(y, m):
    d1, d2 = f"{y}-{m:02d}-01", f"{y}-{m:02d}-{calendar.monthrange(y, m)[1]}"
    rows, off, total = [], 0, None
    while total is None or off < total:
        doc = post(type="C", symbol="", query="", count=100, offset=off, date_from=d1, date_to=d2, page="annc")
        total = int(re.search(r"of (\d+) entries", doc).group(1))
        got = parse(doc)
        if not got:
            break
        rows += got
        off += 100
    if len(rows) != total:
        print(f"WARN {d1}: got {len(rows)} of {total}", flush=True)
    return rows


# --- classification: first match wins ---
R = lambda p: re.compile(p, re.I)
RULES = [
    ("insider_trade", R(r"transaction of shares|disclosure of interest|disclosure of (sale|purchase)|(sale|purchase|acquisition|disposal) of (shares|securities).*(director|sponsor|ceo|officer|shareholder|executive)|(director|sponsor|ceo|substantial shareholder|executive)s?.*(sale|purchase|acquisition|disposal|bought|sold)|insider|sale of shares by|purchase of shares by|trading of shares|dealing in shares|substantial shareholder|acquisition of voting")),
    ("credit_rating", R(r"credit rating|rating (of|report)|entity rating|vis |pacra|rating assigned|maintains? .*rating")),
    ("board_meeting_notice", R(r"(notice|intimation|date|schedule).{0,40}board.{0,3}(of directors)? ?meeting|board meeting.{0,30}(to be held|will be held|on )|meeting of the board.{0,30}(to be held|will be held)|board of directors meeting|^board meeting|bbodb.{0,10}meeting|meeting of the board")),
    ("financial_result", R(r"financial results?|(quarterly|half[- ]?yearly|annual|interim|accounts?|condensed|un-?audited).{0,30}(report|accounts|financial|statements?)|financial statements?|results? (for|of) the|transmission of (quarterly|annual)|(1st|2nd|3rd|first|second|third|fourth|4th) quarter|annual report|half year")),
    ("dividend_or_bonus", R(r"dividend|bonus|right (shares?|issue)|rights? (issue|subscription)|book closure|entitlement|book closing")),
    ("agm", R(r"annual general meeting|\bagm\b|extra[- ]?ordinary general|\begm\b|general meeting|election of directors")),
    ("material_info", R(r"material information|material info")),
]
BUY = R(r"purchase|acquisition|acquired|acquire|bought|\bbuy\b|buying")
SELL = R(r"\bsale\b|\bsold\b|\bsell|disposal|disposed")


def classify(t):
    for k, rx in RULES:
        if rx.search(t):
            return k
    return "other"


def direction(t):
    b, s = bool(BUY.search(t)), bool(SELL.search(t))
    return "buy" if b and not s else "sell" if s and not b else "unknown"


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    if "--classify-only" not in sys.argv:
        args = [a for a in sys.argv[1:] if not a.startswith("--")]
        sy, sm = map(int, (args[0] if args else "2005-01").split("-"))
        today = date.today()
        refresh_key()
        y, m = sy, sm
        while (y, m) <= (today.year, today.month):
            f = CACHE / f"{y}-{m:02d}.csv"
            recent = (today.year * 12 + today.month) - (y * 12 + m) <= 1
            if recent or not f.exists():
                rows = fetch_month(y, m)
                pd.DataFrame(rows, columns=["datetime", "symbol", "company", "title", "category", "document_ids", "url"]).to_csv(f, index=False)
                print(y, m, len(rows), flush=True)
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    df = pd.concat([pd.read_csv(f, dtype=str, keep_default_na=False) for f in sorted(CACHE.glob("*.csv"))])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.drop_duplicates(["datetime", "symbol", "title", "document_ids"]).sort_values("datetime", ascending=False, kind="stable").reset_index(drop=True)
    df["klass"] = df["title"].map(classify)
    df["direction"] = [direction(t) if k == "insider_trade" else "" for t, k in zip(df["title"], df["klass"])]
    df["datetime"] = df["datetime"].dt.tz_localize("Asia/Karachi", ambiguous="NaT", nonexistent="NaT")
    df.to_parquet(ROOT / "data/announcements.parquet", index=False)
    df.to_csv(ROOT / "data/announcements.csv", index=False)
    print(len(df), "rows")


if __name__ == "__main__":
    main()
