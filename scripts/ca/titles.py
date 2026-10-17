"""Corporate-action announcements -> one row each, with kind, phase and any numbers the title states."""
import re

import numpy as np
import pandas as pd

from common import ROOT

KINDS = ["dividend_or_bonus", "financial_result", "other", "material_info", "board_meeting_notice"]
KW = r"bonus|right|dividend|sub-?division|split|face value|consolidation"
BAD = (r"revok|withdraw|progress report|utili[sz]ation|auditor|winding|tfc|sukuk|certificate of|offer document|unclaimed|"
       r"fraction|nominee|withhold|withholding|236Z|abandon|clarification|transmission|quarterly report|half yearly|income tax|"
       r"annual report")
POST = r"credit|despatch|dispatch|disburse|payment|e-credit|allot|paid|remit"


def kind_of(t):
    t = t.lower()
    if re.search(r"sub-?division|split|consolidation|face value", t):
        return "split"
    if "bonus" in t:
        return "bonus"
    if re.search(r"\bright", t):
        return "right"
    if "dividend" in t:
        return "cash"
    return None


def load(syms):
    a = pd.read_parquet(ROOT / "data/announcements.parquet")
    a = a[a.symbol.isin(syms) & (a.datetime >= "2016-06-01")]
    a = a[a.klass.isin(KINDS) & a.title.str.contains(KW, case=False, na=False)]
    a = a[~a.title.str.contains(BAD, case=False, na=False)]
    a = a.assign(kind=a.title.map(kind_of)).dropna(subset=["kind"])
    # fund distributions and daily dividend noise are not equities
    a = a[~a.title.str.contains(r"daily dividend|distribution|fund|reit", case=False)]
    t = a.title
    a["phase"] = np.where(t.str.contains(POST, case=False), "post", "pre")
    a["pct"] = pd.to_numeric(t.str.extract(r"(\d+(?:\.\d+)?)\s*%")[0], errors="coerce")
    rs = t.str.extract(r"(?:Rs\.?|Re\.?)\s*(\d+(?:\.\d+)?)\s*/?-?\s*(?:per|/)\s*(?:ordinary\s+)?share", flags=re.I)[0]
    a["rs"] = pd.to_numeric(rs, errors="coerce")
    a["dt"] = a.datetime.dt.tz_localize(None)
    a["doc"] = a.document_ids.fillna("").str.split(",").str[0].str.strip()
    return a.sort_values(["symbol", "dt"]).reset_index(drop=True)
