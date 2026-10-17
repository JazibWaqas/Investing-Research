"""Row loaders: each returns a DataFrame with symbol, ex_date, type, value, announce_dt, ex_date_source, source_doc, sub_price."""
import re

import numpy as np
import pandas as pd

from common import ROOT, ex_from_start

COLS = ["symbol", "ex_date", "type", "value", "announce_dt", "ex_date_source", "source_doc", "sub_price"]


def load_seed():
    s = pd.read_csv(ROOT / "seed/data/corporate_actions.csv", comment="#", parse_dates=["ex_date"])
    ty = {"cash_div": "cash", "bonus": "bonus", "split": "split"}
    def val(v):
        v = str(v)
        return float(v[:-1]) / 100 if v.endswith("%") else float(v.split(":")[0]) if ":" in v else float(v)
    out = pd.DataFrame({"symbol": s.ticker, "ex_date": s.ex_date, "type": s.type.map(ty), "value": s.amount_pkr_or_ratio.map(val),
                        "announce_dt": pd.NaT, "ex_date_source": "seed", "source_doc": "seed:" + s.source, "sub_price": np.nan})
    return out[COLS]


def load_payouts(par_at, idx):
    """data/payouts_raw.csv (PSX portal, about 2 years). par_at(symbol, date) -> par value in Rs.
    cash = pct/100*par; bonus = pct/100; right = pct/100 (sub_price parsed if stated). ex = book-closure start minus
    2 (before Mar 2026) or 1 trading day. Rows without a book closure range have no ex-date and are returned in `unplaced`."""
    p = pd.read_csv(ROOT / "data/payouts_raw.csv")
    rows, unplaced = [], []
    for r in p.itertuples():
        det = str(r.Details)
        adt = pd.to_datetime(r.Date, format="%B %d, %Y %I:%M %p", errors="coerce")
        m = re.match(r"\s*(\d\d/\d\d/\d{4})", str(r[4]))
        kind = "right" if "(R)" in det else "bonus" if "(B)" in det else "cash"
        pcts = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", det)]
        if not pcts:   # '80(ii) (D)', '12.1433 AT A PREMIUM ...(R)': bare number is a percent
            pcts = [float(x) for x in re.findall(r"^[\s=]*(\d+(?:\.\d+)?)", det)]
        if "(F) (D) - " in det:   # DOL: the same 20% printed twice for two closure ranges
            pcts = pcts[:1]
        if not pcts:
            continue
        pct = pcts[0]
        sp = re.search(r"(?:PREMIUM|DISCOUNT)(?: OF)? RS\.?\s*(\d+(?:\.\d+)?)", det, re.I)
        sub = float(sp.group(1)) if sp else np.nan
        sub = -sub if sp and "DISCOUNT" in det.upper() else sub
        base = dict(symbol=r.symbol, type=kind, announce_dt=adt, source_doc="payouts_raw", sub_price=sub)
        if not m:
            unplaced.append({**base, "ex_date": pd.NaT, "value": pct / 100, "ex_date_source": "none"})
            continue
        start = pd.to_datetime(m.group(1), dayfirst=True)
        ex = ex_from_start(start, idx)
        v = pct / 100 * par_at(r.symbol, ex) if kind == "cash" else pct / 100
        rows.append({**base, "ex_date": ex, "value": v, "ex_date_source": "payouts_book_closure"})
    return pd.DataFrame(rows)[COLS], pd.DataFrame(unplaced, columns=COLS)
