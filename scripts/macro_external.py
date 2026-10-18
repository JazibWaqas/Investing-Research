"""External account series: SBP weekly FX reserves, monthly current account, import cover.

Inputs (raw, read-only): data/raw/macro/forex_arch.xlsx (Week-end sheet, SBP Forex_Arch) and
data/raw/macro/BPM6_Ach_M.xlsx (SBP summary balance of payments, BPM6, USD mn, monthly).
Outputs: data/macro/fx_reserves.csv, current_account.csv, import_cover.csv.
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/macro"
OUT = ROOT / "data/macro"

# Weekly reserves: the sheet has footnote and revision tags on some dates ("29-Jun-12 (R)", "24-Jun-26 21/").
w = pd.read_excel(RAW / "forex_arch.xlsx", sheet_name="Week-end", header=None).iloc[6:, [1, 2, 4]]
w.columns = ["end", "sbp", "total"]


def parse_date(v):
    if isinstance(v, pd.Timestamp) or hasattr(v, "year"):
        return pd.Timestamp(v)
    s = re.sub(r"\s*(\(R\)|R|\d+/)\s*$", "", str(v).strip())
    return pd.to_datetime(s, format="%d-%b-%y", errors="coerce") if re.match(r"\d{2}-", s) else pd.to_datetime(s, errors="coerce")


w["date"] = w.end.map(parse_date)
w = w.dropna(subset=["date"]).copy()
w["sbp"] = pd.to_numeric(w.sbp, errors="coerce")
w["total"] = pd.to_numeric(w.total, errors="coerce")
w = w.dropna(subset=["sbp", "total"]).sort_values("date")
assert w.date.is_unique, "duplicate week"
fx = w[["date", "sbp", "total"]].rename(columns={"sbp": "sbp_reserves_usd_mn", "total": "total_reserves_usd_mn"})
fx.assign(date=fx.date.dt.strftime("%Y-%m-%d")).round(1).to_csv(OUT / "fx_reserves.csv", index=False)
print("fx_reserves", len(fx), fx.date.min().date(), fx.date.max().date(), flush=True)

# Balance of payments: header row 3 holds month-end dates. Dates after Mar 2026 are stored with day 26 (a
# parse of "Apr-26" labels), so only the year and month are used.
bop = pd.read_excel(RAW / "BPM6_Ach_M.xlsx", header=None)
hdr = bop.iloc[3, 1:].tolist()
months = [pd.Timestamp(h).to_period("M") for h in hdr if hasattr(h, "year")]
assert len(months) == len(hdr) and len(set(months)) == len(months), "BoP months not unique"
assert all((b - a).n == 1 for a, b in zip(months, months[1:])), "BoP months not consecutive"
rows = bop.set_index(0)
cab = pd.Series(rows.loc["Current account balance"].iloc[0:].values[: len(months)], index=months, dtype=float)
imp = pd.Series(rows.loc["Imports of goods FOB"].iloc[0:].values[: len(months)], index=months, dtype=float)
ca = cab[cab.index >= pd.Period("2015-01", "M")]
ca.rename("cab_usd_mn").rename_axis("month").reset_index().assign(month=lambda d: d.month.astype(str)).to_csv(
    OUT / "current_account.csv", index=False)
print("current_account", len(ca), ca.index.min(), ca.index.max(), flush=True)

# Import cover: reserves at the last weekly print in each month, over trailing 12-month goods imports (BoP, FOB).
w["m"] = w.date.dt.to_period("M")
last = w.groupby("m").tail(1).set_index("m")
t12 = imp.rolling(12).sum()
rows_out = []
for m in ca.index:
    if m not in last.index or m not in t12.index or pd.isna(t12[m]):
        continue
    r = last.loc[m]
    rows_out.append({
        "month": str(m), "reserves_asof": r.date.strftime("%Y-%m-%d"),
        "sbp_reserves_usd_mn": r.sbp, "total_reserves_usd_mn": r.total,
        "imports_12m_usd_mn": t12[m],
        "import_cover_total_months": round(r.total / (t12[m] / 12), 2),
        "import_cover_sbp_months": round(r.sbp / (t12[m] / 12), 2),
    })
ic = pd.DataFrame(rows_out)
ic.to_csv(OUT / "import_cover.csv", index=False)
print("import_cover", len(ic), ic.month.min(), ic.month.max(), flush=True)
