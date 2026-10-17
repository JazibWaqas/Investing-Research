"""Daily FIPI/LIPI by investor type (USD mn) from scstrade.com FIPILIPI.aspx (mirrors NCCPL). Writes data/macro/fipi_lipi.csv."""
import pandas as pd, curl_cffi.requests as cr
from concurrent.futures import ThreadPoolExecutor
URL = "https://scstrade.com/FIPILIPI.aspx/loadmainsumdetails"

def day(d):
    for _ in range(4):
        try:
            r = cr.post(URL, json={"date1": d, "date2": d}, impersonate="chrome", timeout=40)
            return d, r.json()["d"]
        except Exception:
            pass
    return d, None

days = [d.strftime("%Y-%m-%d") for d in pd.bdate_range("2017-01-01", pd.Timestamp.today())]
with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(day, days))
rows = [(d, i["FLType"].strip().lower(), i["FLBuyValue"], -i["FLSellValue"], i["FLNetValueUSD"], URL)
        for d, x in res for i in (x or [])]
df = pd.DataFrame(rows, columns=["date", "investor_type", "buy_usd_mn", "sell_usd_mn", "net_usd_mn", "source_url"])
df.to_csv("data/macro/fipi_lipi.csv", index=False)
print(len(df), df.date.nunique(), "failed:", [d for d, x in res if x is None])
