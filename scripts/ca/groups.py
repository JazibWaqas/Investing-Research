"""Group bonus / split / right announcements into events and pick the filing PDF most likely to state ratio and book closure."""
import re

import numpy as np
import pandas as pd

from common import ROOT


def tier_sets():
    u = pd.read_csv(ROOT / "seed/data/fundamentals/universe_scored.csv").t.tolist()
    kmi = pd.read_csv(ROOT / "data/kmi_allshare_2026-06-05.csv").symbol.tolist()
    return u, kmi


def tier_of(s, u, kmi):
    return 1 if s in u else 2 if s in kmi else 3


def group_events(e, kind, gap_days=100):
    b = e[e.kind == kind].copy()
    b["grp"] = (b.groupby("symbol").dt.diff().dt.days.fillna(999) > gap_days).cumsum()
    return b


def results_docs():
    a = pd.read_parquet(ROOT / "data/announcements.parquet")
    fr = a[(a.klass == "financial_result") & (a.document_ids.fillna("") != "")].copy()
    fr = fr[fr.title.str.contains("financial result|financial statement|results of", case=False)
            & ~fr.title.str.contains("transmission|progress|quarterly report|annual report|fund", case=False)]
    fr["dt"] = fr.datetime.dt.tz_localize(None)
    fr["doc"] = fr.document_ids.str.split(",").str[0].str.strip()
    return fr


def pick_doc(q, fr):
    """q: announcements of one event group. Prefer the earliest 'pre' (declaration / board resolution / book closure) PDF;
    else the annual-results PDF in the 110 days before the first notice; else the first notice with a PDF."""
    pre = q[(q.phase == "pre") & (q.doc != "")]
    if len(pre):
        r = pre.iloc[0]
        return r.doc, "declaration", r["dt"], r.title
    first = q.dt.min()
    c = fr[(fr.symbol == q.symbol.iloc[0]) & (fr.dt < first - pd.Timedelta(days=5)) & (fr.dt > first - pd.Timedelta(days=110))]
    if len(c):
        y = c[c.title.str.contains("year|annual", case=False)]
        r = (y if len(y) else c).iloc[-1]
        return r.doc, "results", r["dt"], r.title
    post = q[q.doc != ""]
    if len(post):
        r = post.iloc[0]
        return r.doc, "credit", r["dt"], r.title
    return None, None, None, None
