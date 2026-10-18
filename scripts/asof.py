"""Point-in-time information pack for blind replays.
    .venv/Scripts/python.exe -I scripts/asof.py 2024-06-14 [--check]
Writes data/asof/<T>/{market.md, sectors.csv, screens.csv, announcements_30d.csv, flows.csv, calendar.md}
holding only what was public by T 15:30 PKT. Months are sessions (21/63/126/252). NCCPL flows use sessions strictly
before T (published after the close). A policy decision dated T is treated as not yet known. Known leaks are listed
in the report that came with this script; the main ones: sector baskets are today's names, KMI lists before
2026-06-05 are derived, EPS/ratio vendor data may be restated, panel excludes names delisted before 2026.
"""
import ast, re, sys, argparse, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

M = ROOT / "data" / "macro"
OFF = {"1m": 21, "3m": 63, "6m": 126, "12m": 252}
KLASS = {"financial_result": "n_results", "dividend_or_bonus": "n_div_bonus", "material_info": "n_material",
         "board_meeting_notice": "n_board_notice"}


def sectors():
    """The S dict of sector_momentum.py (parsed, not run: that file is a script)."""
    tree = ast.parse((ROOT / "scripts" / "sector_momentum.py").read_text(encoding="utf-8"))
    d = next(n.value for n in tree.body if isinstance(n, ast.Assign) and n.targets[0].id == "S")
    return {k: v.split() for k, v in ast.literal_eval(d).items()}


def members(T):
    fs = [(f.stem.split("_")[-1], "derived" in f.stem, f) for f in (ROOT / "data" / "index_members").glob("KMI_ALL*.csv")]
    ok = sorted((d, dv, f) for d, dv, f in fs if d <= T)   # at equal date the real list (dv False) sorts first, take it last
    ok.sort(key=lambda x: (x[0], not x[1]))
    d, dv, f = ok[-1]
    return set(pd.read_csv(f).symbol), f"{f.name}"


def series(name, T, col="close"):
    s = pd.read_csv(M / f"{name}.csv", parse_dates=["date"]).set_index("date")[col]
    return s[s.index <= T]


def ret(s, n):
    return s.iloc[-1] / s.iloc[-1 - n] - 1 if len(s) > n else np.nan


def asof_val(s, d):
    s = s[s.index <= d]
    return s.iloc[-1] if len(s) else np.nan


def market(T):
    L = [f"# Market as of {T.date()} close (public information only)\n"]
    for nm, f in (("KSE100", "kse100"), ("KMI All Share", "kmiallshr")):
        s = series(f, T)
        L.append(f"- {nm}: {s.iloc[-1]:,.0f} on {s.index[-1].date()}; " + ", ".join(f"{k} {ret(s, n):+.1%}" for k, n in OFF.items()))
    dec = pd.read_csv(M / "policy_rate_decisions.csv", parse_dates=["date"])
    past = dec[dec.date < T]
    last = past.iloc[-1]
    L.append(f"- Policy rate {last.rate}%; last MPC decision {last.date.date()}: {last.decision} ({int(last.change_bp):+d}bp)")
    tb = pd.read_csv(M / "tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"])
    tb = tb[tb.date <= T]
    L.append(f"- 6M T-bill cutoff {tb.y6m.iloc[-1]:.2f}% (auction {tb.date.iloc[-1].date()}); 3M {tb.y3m.iloc[-1]:.2f}%, 12M {tb.y12m.iloc[-1]:.2f}%")
    cpi = pd.read_csv(M / "cpi.csv")
    cpi["pub"] = pd.PeriodIndex(cpi.month, freq="M").to_timestamp() + pd.offsets.MonthBegin(1) + pd.Timedelta(days=2)
    cpi = cpi[cpi.pub <= T]   # published by the 3rd of the next month
    c, c3 = cpi.iloc[-1], cpi.iloc[-4]
    L.append(f"- CPI YoY {c.yoy}% for {c.month} (published by {c.pub.date()}); three months earlier ({c3.month}) {c3.yoy}%")
    for nm, f, unit in (("Brent", "brent", "USD/bbl"), ("USD/PKR", "usdpkr", "")):
        s = pd.read_csv(M / f"{f}.csv", parse_dates=["date"]).set_index("date")["value"]
        s = s[s.index <= T]
        prev = asof_val(s, s.index[-1] - pd.DateOffset(months=3))
        L.append(f"- {nm}: {s.iloc[-1]:,.2f} {unit} on {s.index[-1].date()}; 3-month change {s.iloc[-1] / prev - 1:+.1%}")
    L.append("- FX reserves, current account: not available in this repository (no data file)")
    sp = tb.y6m.iloc[-1] - last.rate
    ch = c.yoy - c3.yoy
    L.append(f"- Regime: 6M T-bill minus policy rate {sp:+.2f}pp ({'market pricing hikes' if sp > 0.5 else 'market pricing cuts' if sp < -0.5 else 'market near policy rate'}); "
             f"CPI {'rising' if ch > 0.3 else 'falling' if ch < -0.3 else 'flat'} over 3 months ({ch:+.1f}pp)")
    L.append("- Next MPC: see SBP calendar")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    raw, vol, tv = P.load_panel()
    adj = pd.read_parquet(ROOT / "data" / "panel_close_adj.parquet").reindex(index=raw.index, columns=raw.columns)
    T = raw.index[raw.index.searchsorted(pd.Timestamp(a.date), side="right") - 1]
    cut = pd.Timestamp(f"{a.date} 15:30", tz="Asia/Karachi")
    out = ROOT / "data" / "asof" / a.date
    out.mkdir(parents=True, exist_ok=True)
    raw, vol, tv, adj = (x.loc[:T] for x in (raw, vol, tv, adj))
    px = adj.ffill()

    # --- universe
    mem, memfile = members(a.date)
    mtv = tv.rolling(60, min_periods=40).median().iloc[-1]
    liquid = [s for s in raw.columns if s in mem and mtv[s] > 5e6 and adj[s].iloc[-60:].notna().any()]
    hi = adj.rolling(252, min_periods=150).max().iloc[-1]
    lo = adj.rolling(252, min_periods=150).min().iloc[-1]

    # --- sectors
    kmi = series("kmiallshr", T)
    rows = []
    for sec, names in sectors().items():
        got = [n for n in names if n in adj.columns and adj[n].iloc[-5:].notna().any() and adj[n].iloc[:-21].notna().any()]   # priced at T and already listed a month before
        r = px[got].iloc[-253:].pct_change().clip(-0.10, 0.10)
        idx = (1 + r.mean(axis=1).fillna(0)).cumprod()
        at_hi = int(sum(adj[n].iloc[-1] >= hi[n] for n in got if pd.notna(adj[n].iloc[-1]) and pd.notna(hi[n])))
        near = int(sum(adj[n].iloc[-1] >= 0.98 * hi[n] for n in got if pd.notna(adj[n].iloc[-1]) and pd.notna(hi[n])))
        rows.append(dict(sector=sec, n_names=len(got), r1m=ret(idx, 21), r3m=ret(idx, 63), r6m=ret(idx, 126), n_at_252_high=at_hi, n_within_2pct_of_high=near))
    pd.DataFrame(rows).round(4).to_csv(out / "sectors.csv", index=False)

    # --- announcements
    an = pd.read_csv(ROOT / "data" / "announcements.csv", low_memory=False, usecols=["datetime", "symbol", "title", "klass", "direction"])
    an["dt"] = pd.to_datetime(an.datetime, utc=True).dt.tz_convert("Asia/Karachi")
    an = an[an.dt <= cut]
    w30 = an[an.dt > cut - pd.Timedelta(days=30)]

    # --- screens
    q = pd.read_csv(ROOT / "data" / "fundamentals" / "quarterly_eps.csv", parse_dates=["fiscal_quarter_end"])
    q["ann"] = pd.to_datetime(q.announce_dt, utc=True, errors="coerce").dt.tz_convert("Asia/Karachi")
    sa = pd.read_csv(ROOT / "seed" / "data" / "fundamentals" / "sa_ratios.csv").rename(columns={"t": "symbol"})
    sa = sa[sa.date != "TTM"].assign(fy=lambda d: pd.to_datetime(d.date))
    ohlc = {}
    scr = []
    for s in liquid:
        c, p = raw[s].dropna(), px[s]
        d = dict(symbol=s, close=round(float(c.iloc[-1]), 2), last_trade=c.index[-1].date())
        for k, n in OFF.items():
            d["r" + k] = ret(p, n)
        d["dist_from_252_high"] = adj[s].iloc[-1] / hi[s] - 1 if pd.notna(adj[s].iloc[-1]) else np.nan
        d["dist_from_252_low"] = adj[s].iloc[-1] / lo[s] - 1 if pd.notna(adj[s].iloc[-1]) else np.nan
        v20, v120 = vol[s].iloc[-20:].mean(), vol[s].iloc[-120:].mean()
        d["vol20_over_vol120"] = v20 / v120 if v120 > 0 else np.nan
        f = next((ROOT / x / f"{s}.csv" for x in ("data/prices_raw", "seed/data/prices") if (ROOT / x / f"{s}.csv").exists()), None)
        o = pd.read_csv(f, parse_dates=["date"]).set_index("date")[["high", "close"]].loc[:T].tail(11)
        pc = o.close.pct_change().iloc[1:]
        d["upper_locks_10d"] = int(((o.close.iloc[1:] >= o.high.iloc[1:] - 0.005) & (pc >= 0.07)).sum())   # closed at day high, up 7%+
        e = q[(q.symbol == s) & (q.ann <= cut)].sort_values("fiscal_quarter_end")
        if len(e):
            l = e.iloc[-1]
            py = q[(q.symbol == s) & (q.fiscal_quarter_end == l.fiscal_quarter_end - pd.DateOffset(years=1))]
            d.update(eps_qtr_end=l.fiscal_quarter_end.date(), eps_announced=l.ann.date(), eps_basic=l.eps_basic)
            if len(py) and py.eps_basic.iloc[0] not in (0,) and pd.notna(py.eps_basic.iloc[0]):
                d["eps_yoy"] = l.eps_basic / py.eps_basic.iloc[0] - 1 if py.eps_basic.iloc[0] > 0 else np.nan
        r = sa[sa.symbol == s].copy()
        if len(r):
            ann = q[(q.symbol == s) & q.ann.notna()].set_index("fiscal_quarter_end").ann
            r["avail"] = [max(pd.Timestamp(y) + pd.DateOffset(months=4), ann.get(y, pd.NaT).tz_localize(None) if y in ann.index else pd.Timestamp(y)) for y in r.fy]
            r = r[r.avail <= pd.Timestamp(a.date)].sort_values("fy")
            if len(r):
                d.update(pe=r.pe.iloc[-1], dy=r.dividendyield.iloc[-1], ratios_fy=r.fy.iloc[-1].date())
        x = w30[w30.symbol == s]
        for k, col in KLASS.items():
            d[col] = int((x.klass == k).sum())
        ins = x[x.klass == "insider_trade"]
        d.update(n_insider_buy=int((ins.direction == "buy").sum()), n_insider_sell=int((ins.direction == "sell").sum()),
                 n_insider_unknown=int((~ins.direction.isin(["buy", "sell"])).sum()))
        scr.append(d)
    scr = pd.DataFrame(scr).sort_values("symbol")
    scr.round(4).to_csv(out / "screens.csv", index=False)

    keep = w30[(w30.symbol.isin(liquid)) | w30.klass.isin(["material_info", "insider_trade"])]
    keep.sort_values("dt").assign(datetime=lambda d: d.dt.dt.strftime("%Y-%m-%d %H:%M"))[["datetime", "symbol", "title", "klass"]].to_csv(out / "announcements_30d.csv", index=False)

    # --- flows (sessions strictly before T)
    fl = pd.read_csv(M / "fipi_lipi.csv", parse_dates=["date"])
    fs = pd.read_csv(M / "fipi_lipi_by_sector.csv", parse_dates=["date"])
    days = np.sort(fl.date[fl.date < T].unique())
    parts = []
    for n in (5, 20):
        dd = days[-n:]
        t = fl[fl.date.isin(dd)].groupby("investor_type").net_usd_mn.sum().reset_index().rename(columns={"investor_type": "key"})
        t2 = fs[fs.date.isin(dd)].groupby(["investor_group", "sector"]).net_usd_mn.sum().reset_index()
        t2["key"] = t2.investor_group + " | " + t2.sector
        parts += [t.assign(kind="investor_type", window=f"last_{n}_sessions", through=pd.Timestamp(dd[-1]).date()),
                  t2[["key", "net_usd_mn"]].assign(kind="sector", window=f"last_{n}_sessions", through=pd.Timestamp(dd[-1]).date())]
    pd.concat(parts)[["kind", "window", "key", "net_usd_mn", "through"]].round(3).to_csv(out / "flows.csv", index=False)

    # --- calendar and market
    b = w30[(w30.klass == "board_meeting_notice") & w30.symbol.isin(liquid) & ~w30.title.str.contains("in progress", case=False)]
    cal = [f"# Calendar as of {a.date}\n", "- Next MPC: see SBP calendar\n",
           "## Board meeting notices in the last 30 days, liquid KMI names (meeting dates are in the notice PDFs, not parsed; titles shown as published)\n"]
    cal += [f"- {r.dt:%Y-%m-%d} {r.symbol}: {r.title}" for r in b.sort_values("dt").itertuples()]
    (out / "calendar.md").write_text("\n".join(cal) + "\n", encoding="utf-8")
    (out / "market.md").write_text(market(T) + f"\nSession date used: {T.date()}. Liquid KMI names: {len(liquid)} (membership {memfile}).\n", encoding="utf-8")
    print(f"{a.date}: session {T.date()}, {len(liquid)} liquid names, list {memfile}")

    if a.check:
        lim = pd.Timestamp(a.date) + pd.Timedelta(days=1)
        for f in sorted(out.iterdir()):
            if f.suffix == ".md":
                txt = f.read_text(encoding="utf-8")
                mx = pd.to_datetime(pd.Series(re.findall(r"\d{4}-\d{2}-\d{2}", txt))).max()
            else:
                df = pd.read_csv(f)
                cols = [c for c in df.columns if c in ("datetime", "through", "last_trade", "eps_announced", "eps_qtr_end", "ratios_fy")]
                mx = max((pd.to_datetime(df[c]).max() for c in cols), default=pd.NaT)
            ok = pd.isna(mx) or mx < lim
            print(f"  {f.name:22s} {f.stat().st_size:>8,d} B  max date {mx.date() if pd.notna(mx) else '-'}  {'OK' if ok else 'LEAK'}")
            assert ok, f"{f.name} has a date after {a.date}"


main()
