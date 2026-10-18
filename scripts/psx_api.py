"""Client for the PSX data portal (https://dps.psx.com.pk).

The JSON/HTML endpoints return 403 unless the request carries `X-Req-Id: <key>`,
where <key> is `_k` in the inline script `__ps = {...,"_k":"...",...};` served on
any page (we use /company/MEBL). The key rotates, so get_key() fetches it fresh;
on a non-200 we re-fetch it and retry once. 1s sleep between requests.
"""
import io
import re
import time

import pandas as pd
import requests

BASE = "https://dps.psx.com.pk"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
_s = requests.Session()
_s.headers["User-Agent"] = UA
_key = None


def get_key():
    r = _s.get(f"{BASE}/company/MEBL", timeout=30)
    r.raise_for_status()
    return re.search(r'"_k"\s*:\s*"([^"]+)"', r.text).group(1)


def _req(method, path, sym="MEBL", **kw):
    global _key
    for attempt in (0, 1):
        if _key is None:
            _key = get_key()
        h = {"X-Req-Id": _key, "X-Requested-With": "XMLHttpRequest",
             "Referer": f"{BASE}/company/{sym}",
             "Accept": "application/json, text/javascript, */*; q=0.01"}
        time.sleep(1.0)
        r = _s.request(method, BASE + path, headers=h, timeout=60, **kw)
        if r.status_code == 200:
            return r
        _key = None  # re-fetch key and retry once
    r.raise_for_status()


def eod(sym):
    d = _req("GET", f"/timeseries/eod/{sym}", sym).json()["data"]
    df = pd.DataFrame(d, columns=["ts", "close", "volume", "open"])
    df["date"] = pd.to_datetime(df.ts, unit="s").dt.normalize()
    return df.drop(columns="ts").sort_values("date").reset_index(drop=True)


def intraday(sym):
    """Today's trades, newest first: ts (unix seconds, UTC), price, volume. Portal serves only the current session."""
    d = _req("GET", f"/timeseries/int/{sym}", sym).json()["data"]
    return pd.DataFrame(d, columns=["ts", "price", "volume"])


def historical_full(sym):
    r = _req("POST", "/historical", sym, data={"month": 0, "year": 0, "symbol": sym})
    cols = ["date", "open", "high", "low", "close", "volume"]
    if "<tbody" not in r.text or "data-order" not in r.text:  # no history (e.g. DFSM, ZAHID)
        return pd.DataFrame(columns=cols)
    df = pd.read_html(io.StringIO(r.text))[0]
    ts = re.findall(r'<td[^>]*data-order="(\d+)"', r.text)
    df.columns = [c.lower() for c in df.columns]
    if len(ts) == len(df):  # data-order is the unix ts; more robust than text dates
        df["date"] = pd.to_datetime([int(t) for t in ts], unit="s").normalize()
    else:
        df["date"] = pd.to_datetime(df["date"])
    for c in cols[1:]:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="coerce")
    return df[cols].sort_values("date").reset_index(drop=True)


def payouts(sym):
    r = _req("POST", "/company/payouts", sym, data={"symbol": sym})
    try:
        return pd.read_html(io.StringIO(r.text))[0]
    except ValueError:  # no tables = no payouts
        return pd.DataFrame()


def symbols():
    return pd.DataFrame(_req("GET", "/symbols").json())


def download_document(doc_id, path):
    r = _req("GET", f"/download/document/{doc_id}.pdf")
    with open(path, "wb") as f:
        f.write(r.content)


if __name__ == "__main__":
    h = historical_full("MEBL")
    assert len(h) > 2000, len(h)
    p = payouts("MEBL")
    assert not p.empty
    print(len(h), h.tail(2), p.head(), sep="\n")
