"""Daily FIPI/LIPI by sector x investor group (USD mn) from scstrade.com FIPILIPI.aspx/loadfipiInvestor.
Writes data/macro/fipi_lipi_by_sector.csv. Resumable: dates already in the file are skipped."""
import os, pandas as pd, curl_cffi.requests as cr
from concurrent.futures import ThreadPoolExecutor
URL = "https://scstrade.com/FIPILIPI.aspx/loadfipiInvestor"
OUT = "data/macro/fipi_lipi_by_sector.csv"
COLS = ["date", "investor_group", "sector", "buy_usd_mn", "sell_usd_mn", "net_usd_mn", "source_url"]

def day(d):
    for _ in range(4):
        try:
            r = cr.post(URL, json={"date1": d, "date2": d}, impersonate="chrome", timeout=40)
            return d, r.json()["d"]
        except Exception:
            pass
    return d, None

done = set(pd.read_csv(OUT).date) if os.path.exists(OUT) else set()
days = [d.strftime("%Y-%m-%d") for d in pd.bdate_range("2017-01-01", pd.Timestamp.today())]
days = [d for d in days if d not in done]
for i in range(0, len(days), 200):  # chunked so an interruption keeps progress
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(day, days[i:i + 200]))
    rows = [(d, ("fipi" if x["FLTypeNew"] == "FIPI" else "lipi " + x["FLTypeNew"].strip().lower()),
             x["FLSectorName"].replace(" (mn$)", "").strip(), x["FLBuyValue"], -x["FLSellValue"], x["FLNetValueUSD"], URL)
            for d, xs in res for x in (xs or [])]
    pd.DataFrame(rows, columns=COLS).to_csv(OUT, mode="a", header=not os.path.exists(OUT), index=False)
    print(i, len(rows), "failed:", [d for d, xs in res if xs is None], flush=True)
