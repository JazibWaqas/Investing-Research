"""Build data/delistings.csv from announcements keyword hits + the portal price log (data/prices_delisted_log.csv).
Reason is a keyword classification of the symbol's announcement titles (strongest signal wins); if none, the row is
'suspension/unknown (no trades since last_date)'. Date = best dated keyword announcement, else last portal trade date."""
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
a = pd.read_parquet(ROOT / "data/announcements.parquet")
a["d"] = pd.to_datetime(a.datetime, utc=True).dt.tz_convert(None).dt.normalize()
sym = pd.read_csv(ROOT / "data/symbols.csv").set_index("symbol")
log = pd.read_csv(ROOT / "data/prices_delisted_log.csv", parse_dates=["first", "last"])
panel = set(pd.read_parquet(ROOT / "data/panel_close.parquet").columns)
RULES = [  # (reason, regex) in priority order
    ("merger", r"merger|amalgamat|scheme of arrangement|scheme of amalg"),
    ("voluntary delisting", r"delist|de-list|buy.?back"),
    ("default/compulsory", r"defaulter|compulsory"),
    ("liquidation/winding up", r"winding|liquidat"),
]
rows = []
for s in sorted(set(log.symbol) | set(a[a.title.str.contains("delist", case=False, na=False)].symbol.dropna())):
    if not isinstance(s, str) or s in panel or re.search(r"(TFC|SC\d*$|OEF|FUNDS)", s):
        continue
    if re.search(r"Right|Pref|Convt|\(R\)", str(sym.name.get(s, ""))):  # instruments, not companies
        continue
    x = a[a.symbol == s]
    hits = {}
    for r, rx in RULES:
        h = x[x.title.str.contains(rx, case=False, na=False)]
        if len(h):
            hits[r] = h
    lg = log[log.symbol == s]
    last = lg["last"].iloc[0] if len(lg) and pd.notna(lg["last"].iloc[0]) else pd.NaT
    if len(lg) and lg.rows.iloc[0] > 0:  # last date with real volume, not the last portal row
        p = pd.read_csv(ROOT / f"data/prices_delisted/{s}.csv", parse_dates=["date"])
        p = p[p.volume > 0]
        last = p.date.iloc[-1] if len(p) else pd.NaT
    # voluntary delisting wins over merger if both appear and delist notice is present
    reason = "voluntary delisting" if "voluntary delisting" in hits else (next(iter(hits), None))
    if reason is None and "default/compulsory" in hits:
        reason = "default/compulsory"
    if reason is None:
        if pd.isna(last) or last > pd.Timestamp("2026-09-01"):
            continue  # still trading or no evidence
        reason = "suspension/unknown"
    h = hits.get(reason)
    ev = h.sort_values("d").iloc[-1] if h is not None else None
    lp = None
    if len(lg) and lg.rows.iloc[0] > 0:
        p = pd.read_csv(ROOT / f"data/prices_delisted/{s}.csv")
        p = p[p.volume > 0]
        lp = p.close.iloc[-1] if len(p) else None
    rows.append(dict(symbol=s, company=sym.name.get(s, x.company.dropna().iloc[-1] if len(x) else ""),
                     delisting_or_suspension_date=(last if pd.notna(last) else ev.d).date() if (pd.notna(last) or ev is not None) else None,
                     date_basis="last portal trade" if pd.notna(last) else "announcement",
                     reason=reason, last_price=lp,
                     source=("announcements.parquet: " + str(ev.title)[:100] + f" ({ev.d.date()})") if ev is not None else "portal price history ends; no delisting notice in announcements",
                     price_file=bool(len(lg) and lg.rows.iloc[0] > 0)))
out = pd.DataFrame(rows)
out.loc[out.symbol == "ENGRO", "reason"] = "merger"  # DH/Engro/EHL scheme of arrangement, keyword hit said delisting
# still trading on 2026-10-16 (pending or failed delisting) and rights/odd-lot letters are not delistings
out = out[out.delisting_or_suspension_date.astype(str) < "2026-09-01"]
out = out[~out.symbol.str.contains(r"R\d$|GTECHBR|FFLNV", regex=True)]
out.to_csv(ROOT / "data/delistings.csv", index=False)
print(len(out)); print(out.reason.value_counts()); print(out.price_file.sum())
