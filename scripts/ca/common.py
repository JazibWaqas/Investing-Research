"""Shared pieces for the corporate-actions build (see data/CORPORATE_ACTIONS_NOTES.md)."""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices  # noqa: E402

T1_SWITCH = pd.Timestamp("2026-03-09")   # book-closure starts on/after this: ex = start - 1 trading day; before: start - 2
LAST_PX = None


def panel():
    close, vol, tv = prices.load_panel()
    return close, vol, tv


def ex_from_start(start, idx, n=None):
    """Ex-date from the first day of book closure, on the trading calendar idx.
    PSX settles T+2 until Mar 2026 (dip falls two trading days before closure start, checked on 99 high-yield
    payouts) and T+1 afterwards, so n = 2 before T1_SWITCH, else 1. start on a non-trading day counts from the next
    trading day."""
    start = pd.Timestamp(start).normalize()
    n = (2 if start < T1_SWITCH else 1) if n is None else n
    if start > idx[-1]:
        return start - pd.offsets.BDay(n)
    k = idx.searchsorted(start)
    return idx[max(k - n, 0)]


def pct_str(s):
    m = re.search(r"(\d+(?:\.\d+)?)", str(s))
    return float(m.group(1)) if m else np.nan
