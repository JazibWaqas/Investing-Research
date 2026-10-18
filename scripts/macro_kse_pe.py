"""KSE100 trailing P/E from members, and earnings yield against the 6-month T-bill.

P/E for a month-end = sum(market cap) / sum(trailing-4-quarter net income to common) over the KSE100 members
in force at that date. Market cap = last close on or before the date x basic shares from the latest quarter
available by then, scaled by bonus and split events after that quarter (data/corporate_actions.csv).
Negative earnings stay in the sum (aggregate ratio). Inputs: data/raw/stockanalysis/{SYM}_income.html
(quarterly block: netinccmn, sharesBasic, period-end headers), data/fundamentals/quarterly_eps.csv
(announce_dt where joined), data/index_members/KSE100_*.csv, data/prices_*/{SYM}.csv or data/raw/macro/psx_hist/{SYM}.csv, data/macro/tbill_auctions.csv.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).resolve().parents[1]
SLUG = {"ENGRO": "ENGROH", "ICI": "LCI", "BYCO": "CNERGY"}
LAG_DAYS = 90  # availability when no announce_dt is joined
START, END = pd.Timestamp("2021-04-30"), pd.Timestamp("2026-10-31")


def parse_income(path):
    """Quarterly block of a StockAnalysis income page: list of (period_end, net income, basic shares)."""
    t = path.read_text(encoding="utf-8")
    i = t.find("fiscalYear:[")
    j = t.find("fiscalYear:[", i + 1)
    seg = t[i:j] if j > 0 else t[i:]

    def arr(key):
        m = re.search(key + r":\[([^\]]*)\]", seg)
        if not m:
            return None
        return [np.nan if x.strip() in ("null", "") else float(x) for x in m.group(1).split(",")]

    ni = arr("netinccmn") or arr("netinc")
    sh = arr("sharesBasic") or arr("sharesDiluted")
    ids = re.findall(r'<th id="(\d{4}-\d{2}-\d{2})"', t)[: len(ni)]
    assert len(ids) == len(ni) == len(sh), path.name
    return pd.DataFrame({"period_end": pd.to_datetime(ids), "ni": ni, "shares": sh}).sort_values("period_end")


def price_series(sym):
    for name in (sym, SLUG.get(sym, sym)):
        for folder in ("prices_raw", "prices_listed_missing", "prices_delisted", "raw/macro/psx_hist"):
            p = ROOT / "data" / folder / f"{name}.csv"
            if p.exists():
                s = pd.read_csv(p, parse_dates=["date"]).set_index("date")["close"].dropna()
                return s.sort_index()
    return None


members = {}
for f in sorted((ROOT / "data/index_members").glob("KSE100_*.csv")):
    tag = f.stem.split("KSE100_")[1]
    eff = pd.Timestamp(tag if len(tag) == 10 else tag + "-01")
    members[eff] = set(pd.read_csv(f).symbol.astype(str).str.strip())
effs = sorted(members)
print("snapshots", [str(e.date()) for e in effs], flush=True)

fin, prices = {}, {}
for s in set().union(*members.values()):
    p = ROOT / "data/raw/stockanalysis" / f"{s}_income.html"
    if p.exists():
        fin[s] = parse_income(p)
    ps = price_series(s)
    if ps is not None:
        prices[s] = ps

eps = pd.read_csv(ROOT / "data/fundamentals/quarterly_eps.csv", usecols=["symbol", "fiscal_quarter_end", "announce_dt"])
eps["period_end"] = pd.to_datetime(eps.fiscal_quarter_end)
eps["ann"] = pd.to_datetime(eps.announce_dt.str[:10], errors="coerce")
ann = {(r.symbol, r.period_end): r.ann for r in eps.dropna(subset=["ann"]).itertuples()}

ca = pd.read_csv(ROOT / "data/corporate_actions.csv", parse_dates=["ex_date"])
ca = ca[ca.type.isin(["bonus", "split"])]
factor_events = {s: g for s, g in ca.groupby("symbol")}


def share_factor(sym, after, upto):
    g = factor_events.get(sym)
    if g is None:
        return 1.0
    g = g[(g.ex_date > after) & (g.ex_date <= upto)]
    f = 1.0
    for r in g.itertuples():
        f *= (1 + r.value) if r.type == "bonus" else r.value
    return f


def member_cap_and_ni(sym, d):
    """Market cap and TTM net income for one member at date d, or None."""
    if sym not in fin or sym not in prices:
        return None
    q = fin[sym].copy()
    q["avail"] = [ann.get((sym, pe), pe + pd.Timedelta(days=LAG_DAYS)) for pe in q.period_end]
    q = q[q.avail <= d].reset_index(drop=True)
    for k in range(len(q) - 1, 2, -1):
        w = q.iloc[k - 3: k + 1]
        if w.ni.notna().all() and w.shares.notna().all() and all(
                (b.to_period("M") - a.to_period("M")).n == 3 for a, b in zip(w.period_end, w.period_end[1:])):
            last = w.iloc[-1]
            px = prices[sym][:d]
            if px.empty or (d - px.index[-1]).days > 10:
                return None
            shares = last.shares * share_factor(sym, last.period_end, d)
            return px.iloc[-1] * shares, w.ni.sum()
    return None


rows, cover = [], []
for m_end in pd.date_range("2021-04-30", "2026-10-31", freq="ME"):
    d = min(m_end, pd.Timestamp("2026-10-16"))
    if d < pd.Timestamp("2021-04-01") or m_end > END:
        continue
    eff = [e for e in effs if e <= d]
    if not eff:
        continue
    mem = members[eff[-1]]
    cap = ni = 0.0
    n = 0
    for s in sorted(mem):
        r = member_cap_and_ni(s, d)
        if r is not None:
            cap += r[0]
            ni += r[1]
            n += 1
    if n >= 60 and ni > 0:
        rows.append({"month": m_end.strftime("%Y-%m"), "pe": round(cap / ni, 2), "source": "computed_kse100_members"})
    cover.append((m_end.strftime("%Y-%m"), len(mem), n))
    print(m_end.strftime("%Y-%m"), "members", len(mem), "with P/E inputs", n, flush=True)

pe = pd.DataFrame(rows)
pe.to_csv(ROOT / "data/macro/kse100_pe.csv", index=False)
print("kse100_pe", len(pe), pe.month.min(), pe.month.max(), flush=True)

tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"])
out = []
for r in pe.itertuples():
    me = pd.Timestamp(r.month + "-01") + pd.offsets.MonthEnd(0)
    t = tb[tb.date <= me].tail(1)
    tbill = float(t.y6m.iloc[0])
    ey = 100.0 / r.pe
    out.append({"month": r.month, "kse100_earnings_yield_pct": round(ey, 3), "tbill_6m_cutoff_pct": tbill,
                "gap_pct_points": round(ey - tbill, 3), "tbill_auction_date": t.date.iloc[0].strftime("%Y-%m-%d")})
pd.DataFrame(out).to_csv(ROOT / "data/macro/earnings_yield_vs_tbill.csv", index=False)
print("earnings_yield_vs_tbill", len(out), flush=True)
