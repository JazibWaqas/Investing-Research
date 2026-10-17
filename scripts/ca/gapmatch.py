"""Place an action on the day whose price move matches it (used when no book-closure date is known)."""
import numpy as np
import pandas as pd


class Gaps:
    def __init__(self, close, vol):
        self.close = close
        prev = close.ffill().shift(1)
        self.prev = prev
        self.pct = close / prev - 1
        vo = vol.where(close.notna())
        self.vratio = vo / vo.rolling(20, min_periods=5).median().shift(1)
        self.idx = close.index

    @staticmethod
    def expected(kind, v, prev):
        if kind == "cash":
            return -v / prev
        if kind == "bonus":
            return 1 / (1 + v) - 1
        if kind == "split":
            return 1 / v - 1
        return np.nan

    def find(self, sym, kind, v, lo, hi, min_exp=0.08):
        """Matching observation date in [lo, hi] (inclusive), or None.
        match = |actual move - expected move| <= 0.015 + 0.06*|expected| (0.02 + 0.15*|expected| when the expected move is 12% or more: bigger events carry more cash-dividend and market noise). Expected moves smaller than min_exp (8%) are never
        matched: they do not stand out of daily noise. If more than one day matches, the best is returned only when its error is
        under 40% of the runner-up's, otherwise None (ambiguous)."""
        if sym not in self.close:
            return None
        p, pr = self.pct[sym].loc[lo:hi].dropna(), self.prev[sym]
        hits = []
        for d, x in p.items():
            e = self.expected(kind, v, pr.at[d])
            if not np.isfinite(e) or abs(e) < min_exp:
                continue
            err = abs(x - e)
            if err <= (0.02 + 0.15 * abs(e) if abs(e) >= 0.12 else 0.015 + 0.06 * abs(e)):
                hits.append((err, d))
        if not hits:
            return None
        hits.sort()
        if len(hits) > 1 and hits[0][0] >= 0.4 * hits[1][0]:
            return None
        return hits[0][1]

    def td_after(self, d, n):
        """Date n trading days after d (calendar index)."""
        k = min(self.idx.searchsorted(pd.Timestamp(d)) + n, len(self.idx) - 1)
        return self.idx[k]

    def implied(self, sym, d):
        """price ratio prev/close on d (for inferring bonus/split sizes from the gap)."""
        return self.prev.at[d, sym] / self.close.at[d, sym]
