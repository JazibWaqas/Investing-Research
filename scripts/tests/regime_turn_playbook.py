"""regime_turn_playbook: arithmetic behind knowledge/REGIME_TURN_PLAYBOOK.md.
Run: .venv/Scripts/python.exe scripts/tests/regime_turn_playbook.py > tests/out/regime_turn_playbook.txt

DEFINITIONS (fixed before results were read).
 Real lows (the four turn files): 2019-08-16, 2020-03-25, 2023-06-23, 2024-06-11.
 False bottoms (a closing trough later undercut): 2018-10-16, 2020-03-19, 2022-07-21, 2026-09-14.
 Today: provisional trough 2026-10-13 (lowest close of the current pullback), data to 2026-10-16.
 Liquid = daily_table `liquid`. Breadth = share of liquid names (in panel_close_adj) above own 50/200-session average.
 Drain = share of liquid names at a 20-session closing low two sessions after the trough.
 252-high = daily_table dist_252_high == 0. Thrust = max share above 200d in sessions +1..+10.
 Policy: decision dated on or before the day. Bill gap = latest 6M cutoff minus policy rate in force at that auction.
 CPI public on the 3rd of the following month. Flows: fipi_lipi.csv; foreign = foreign corporates + foreign individual + overseas pakistani.
 Group returns from adjusted closes (panel_close_adj), groups fixed on the low date: large = top 20 liquid by 60-day median value,
 mid = other liquid, small = not liquid with 60-day median value Rs0.5m to 5m; sector groups from daily_table `sector`.
 Index stops on KMI All Share (TR) closes; cash out of the market earns the latest 3M bill cutoff, accrued daily. No costs or tax.
"""
import warnings
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.max_rows", 400)
ROOT = Path(__file__).resolve().parents[2]; R = ROOT / "data"
macro = lambda n: pd.read_csv(R / f"macro/{n}.csv", parse_dates=["date"]).set_index("date")
kse, kmi = macro("kse100"), macro("kmiallshr"); c = kse.close; ck = kmi.close; sess = c.index
P = pd.read_parquet(R / "panel_close_adj.parquet")
D = pd.read_parquet(R / "daily_table.parquet", columns=["date", "symbol", "dist_252_high", "liquid", "sector", "traded_value_median_60"])
D = D[D.date >= "2017-06-01"]
usd = macro("usdpkr").value; brent = macro("brent").value
pol = macro("policy_rate_decisions"); tb = macro("tbill_auctions"); fx = macro("fx_reserves").sbp_reserves_usd_mn
cpi = pd.read_csv(R / "macro/cpi.csv"); cpi["pub"] = pd.to_datetime(cpi.month + "-01") + pd.offsets.MonthBegin(1) + pd.Timedelta(days=2)
cpi = cpi.set_index("pub").yoy
pe = pd.read_csv(R / "macro/kse100_pe.csv"); pe = pe[pe.month.str.len() == 7].set_index("month").pe
imf = pd.read_csv(ROOT / "seed/data/macro/imf_events.csv", parse_dates=["date"])
# events missing from the seed file, dated in the turn files: 2020 second-review SLA noted in the 17 Mar 2020 MPS; 13 Jul 2022 SLA (situation 03)
imf = pd.concat([imf, pd.DataFrame({"date": pd.to_datetime(["2020-03-17", "2022-07-13"]), "event": ["SLA", "SLA"], "program": ["2019 EFF r2", "2019 EFF 7-8"]})])
at = lambda s, d: s[:d].iloc[-1] if len(s[:d]) else np.nan
ma50, ma200, hi252 = c.rolling(50).mean(), c.rolling(200).mean(), c.rolling(252, min_periods=120).max()
vol60 = kse.volume.rolling(60).mean().shift(1)

m50, m200, lo20 = P.rolling(50, min_periods=50).mean(), P.rolling(200, min_periods=200).mean(), P.rolling(20, min_periods=20).min()
Lq = D[D.liquid].pivot_table(index="date", columns="symbol", values="liquid", aggfunc="any").reindex(index=P.index, columns=P.columns).fillna(False).astype(bool)
share = lambda cond, ok: (cond & ok).sum(axis=1) / ok.sum(axis=1)
ok50, ok200, ok20 = Lq & m50.notna() & P.notna(), Lq & m200.notna() & P.notna(), Lq & lo20.notna() & P.notna()
B50, B200, LOW20 = share(P > m50, ok50), share(P > m200, ok200), share(P <= lo20 + 1e-9, ok20)
H = D[D.liquid & (D.dist_252_high >= -1e-6)]; Hs = H.groupby("date").symbol.apply(set); nliq = D[D.liquid].groupby("date").symbol.nunique()
fl = pd.read_csv(R / "macro/fipi_lipi.csv", parse_dates=["date"])
G = lambda x: "foreign" if x in ("foreign corporates", "foreign individual", "overseas pakistani") else x
flow = fl.assign(g=fl.investor_type.map(G)).pivot_table(index="date", columns="g", values="net_usd_mn", aggfunc="sum").fillna(0)
pos = lambda d: sess.get_indexer([pd.Timestamp(d)])[0]


def signals(L, today=False):
    L = pd.Timestamp(L); i = pos(L); after = sess[i + 1:i + 11]; s = {}
    s["KSE100 close"] = round(c[L]); s["below 252-high %"] = 100 * (c[L] / hi252[L] - 1); s["vs 200d avg %"] = 100 * (c[L] / ma200[L] - 1)
    s["names >50d %"] = 100 * B50[L]; s["names >200d %"] = 100 * B200[L]
    s["volume vs 60d"] = kse.volume[L] / vol60[L]
    s["drain: at 20d low +2 sessions %"] = 100 * LOW20[sess[i + 2]] if i + 2 < len(sess) else np.nan
    last = pol[:L].iloc[-1]; nxt = pol[L + pd.Timedelta(days=1):]
    s["last MPC move bp (date)"] = f"{int(last.change_bp)} ({last.name.date()})"
    s["next MPC move bp (date)"] = f"{int(nxt.iloc[0].change_bp)} ({nxt.index[0].date()})" if len(nxt) else "pending"
    a = tb[:L].iloc[-1]; s["6M bill minus policy"] = a.y6m - at(pol.rate, a.name)
    cp = cpi[:L]; s["CPI latest"] = cp.iloc[-1]; s["CPI 3m change pt"] = cp.iloc[-1] - cp.iloc[-4]
    s["real rate pt"] = at(pol.rate, L) - cp.iloc[-1]
    s["USD/PKR 4w before %"] = 100 * (at(usd, L) / at(usd, L - pd.Timedelta(days=28)) - 1)
    s["USD/PKR 4w after %"] = 100 * (at(usd, L + pd.Timedelta(days=28)) / at(usd, L) - 1) if not today else np.nan
    s["SBP res 13w chg $m"] = at(fx, L) - at(fx, L - pd.Timedelta(days=91))
    s["SBP res 4w after chg $m"] = at(fx, L + pd.Timedelta(days=28)) - at(fx, L) if not today else np.nan
    s["Brent 13w %"] = 100 * (at(brent, L) / at(brent, L - pd.Timedelta(days=91)) - 1)
    ev = imf[(imf.date >= L - pd.Timedelta(days=60)) & (imf.date <= L + pd.Timedelta(days=30))]
    s["IMF SLA/Board -60d..+30d"] = "; ".join(f"{e.event} {e.date.date()}" for e in ev.itertuples()) or "none"
    s["P/E"] = pe.get(L.strftime("%Y-%m"), np.nan)
    w = sess[max(0, i - 19):i + 1]; fw = flow.reindex(w).sum()
    s["foreign 20s $m"] = fw.get("foreign", np.nan); s["mutual funds 20s $m"] = fw.get("mutual funds", np.nan)
    s["thrust: max >200d in +1..+10 %"] = 100 * B200.reindex(after).max() if len(after) else np.nan
    hs = set().union(*[Hs.get(x, set()) for x in sess[i:i + 11]]) if len(after) else set()
    s["252-highs +0..+10, % of list"] = 100 * len(hs) / nliq.get(L, np.nan); s["252-highs n"] = len(hs)
    up = c[sess[i + 1:i + 31]]; up = up[up > ma50[up.index]]
    s["first close >50d (sessions)"] = (sess.get_loc(up.index[0]) - i) if len(up) else "none in 30"
    if not today:
        nx = c[sess[i + 1:i + 121]]; s["undercut in 120s"] = f"yes {nx.idxmin().date()}" if nx.min() < c[L] else "no"
        s["index 12 weeks %"] = 100 * (c[sess[min(i + 60, len(sess) - 1)]] / c[L] - 1)
    return s


REAL = ["2019-08-16", "2020-03-25", "2023-06-23", "2024-06-11"]; FALSE = ["2018-10-16", "2020-03-19", "2022-07-21", "2026-09-14"]
print("== 1. SIGNAL TABLE (real lows, false bottoms, today = provisional trough 2026-10-13)")
T = pd.DataFrame({**{f"REAL {d}": signals(d) for d in REAL}, **{f"FALSE {d}": signals(d) for d in FALSE}, "TODAY 2026-10-13": signals("2026-10-13", today=True)})
print(T.to_string(float_format=lambda x: f"{x:.1f}"))
print("\nToday at 16 Oct close:", {k: round(v, 1) for k, v in {"below 252-high %": 100 * (c.iloc[-1] / hi252.iloc[-1] - 1), "vs 200d %": 100 * (c.iloc[-1] / ma200.iloc[-1] - 1),
      "vs 50d %": 100 * (c.iloc[-1] / ma50.iloc[-1] - 1), ">50d %": 100 * B50.iloc[-1], ">200d %": 100 * B200.iloc[-1], "at 20d low %": 100 * LOW20.iloc[-1]}.items()},
      "| 252-highs 13-16 Oct:", sorted(set().union(*[Hs.get(x, set()) for x in sess[-4:]])), "| liquid n", nliq.iloc[-1])
print("Breadth last 10 sessions (>50d, >200d, at 20d low):"); print((100 * pd.DataFrame({"b50": B50, "b200": B200, "low20": LOW20}).iloc[-10:]).round(0).to_string())

# 2. sequence ------------------------------------------------------------------
print("\n== 2. SEQUENCE: median return of group from the low close, adjusted closes (n in brackets); weeks to median +20%")
CYC = {"Cement", "Steel & engineering", "Autos"}
for L in REAL:
    L = pd.Timestamp(L); i = pos(L); x = D[D.date == L].set_index("symbol"); x = x[x.index.isin(P.columns)]
    liq = x[x.liquid]; big = liq.nlargest(20, "traded_value_median_60").index
    grp = {"large (top 20 liquid)": big, "mid (other liquid)": liq.index.difference(big),
           "small (Rs0.5-5m/day)": x[(~x.liquid) & x.traded_value_median_60.between(5e5, 5e6)].index,
           "cyclicals (cement/steel/autos)": liq[liq.sector.isin(CYC)].index, "tech": liq[liq.sector.str.contains("Tech")].index,
           "banks (Islamic, in table)": liq[liq.sector.str.contains("bank")].index,
           "E&P + fertilizer": liq[liq.sector.isin({"E&P", "Fertilizer"})].index, "pharma": liq[liq.sector == "Pharma"].index}
    rows = []
    for k, syms in [("KSE100", None), ("KMI All Share", None)] + list(grp.items()):
        if syms is None:
            s = (c if k == "KSE100" else ck); path = (s.reindex(sess) / s[L] - 1).iloc[i:i + 131]; med = path
        else:
            pp = P.loc[sess[i:i + 131], list(syms)]; med = (pp / pp.iloc[0] - 1).median(axis=1)
        hit = med[med >= 0.2]; wk = round((sess.get_loc(hit.index[0]) - i) / 5, 1) if len(hit) else ">26"
        rows.append([k, 0 if syms is None else len(syms)] + [round(100 * med.iloc[min(h, len(med) - 1)], 1) for h in (10, 20, 40, 65, 130)] + [wk])
    print(f"\n-- low {L.date()}"); print(pd.DataFrame(rows, columns=["group", "n", "+2w", "+4w", "+8w", "+13w", "+26w", "wks to +20%"]).to_string(index=False))

# 3. peaks ---------------------------------------------------------------------
print("\n== 3. PEAKS: conditions at the index top, and what followed")
PK = ["2020-01-13", "2021-06-14", "2025-01-03", "2026-01-23", "2026-07-06"]
rows = {}
for p in PK:
    p = pd.Timestamp(p); i = pos(p); s = {}
    s["KSE100"] = round(c[p]); s["vs 200d %"] = 100 * (c[p] / ma200[p] - 1); s["names >50d %"] = 100 * B50[p]; s["names >200d %"] = 100 * B200[p]
    s["max >50d in prior 60s %"] = 100 * B50[sess[i - 60:i + 1]].max()
    h1 = len(set().union(*[Hs.get(x, set()) for x in sess[i - 19:i + 1]])); h0 = len(set().union(*[Hs.get(x, set()) for x in sess[i - 79:i - 59]]))
    s["252-highs last 20s / 20s ending 60s earlier"] = f"{h1} / {h0}"
    s["P/E"] = pe.get(p.strftime("%Y-%m"), np.nan); last = pol[:p].iloc[-1]; nxt = pol[p + pd.Timedelta(days=1):]
    s["policy, last move"] = f"{last.rate} ({int(last.change_bp)} {last.name.date()})"; s["next move"] = f"{int(nxt.iloc[0].change_bp)} {nxt.index[0].date()}" if len(nxt) else ""
    hk = nxt[nxt.change_bp > 0]; s["next hike"] = str(hk.index[0].date()) if len(hk) else "none"
    a = tb[:p].iloc[-1]; s["6M bill minus policy"] = a.y6m - at(pol.rate, a.name)
    cp = cpi[:p]; s["CPI, 3m chg"] = f"{cp.iloc[-1]:.1f} ({cp.iloc[-1] - cp.iloc[-4]:+.1f})"; s["real rate"] = at(pol.rate, p) - cp.iloc[-1]
    s["Brent 13w %"] = 100 * (at(brent, p) / at(brent, p - pd.Timedelta(days=91)) - 1); s["USD/PKR 13w %"] = 100 * (at(usd, p) / at(usd, p - pd.Timedelta(days=91)) - 1)
    s["foreign 60s $m"] = flow.reindex(sess[i - 59:i + 1]).sum().get("foreign")
    nx = c[sess[i + 1:i + 500]]; tr = nx[:nx[nx > c[p]].index[0]] if (nx > c[p]).any() else nx
    s["worst close before reclaim %"] = 100 * (tr.min() / c[p] - 1); s["date"] = str(tr.idxmin().date())
    f10 = nx[nx <= 0.9 * c[p]]; s["first close -10% (sessions)"] = sess.get_loc(f10.index[0]) - i if len(f10) else "none"
    rc = nx[nx > c[p]]; s["reclaimed peak"] = str(rc.index[0].date()) if len(rc) else "not yet"
    rows[str(p.date())] = s
print(pd.DataFrame(rows).to_string(float_format=lambda x: f"{x:.1f}"))

# 4. stops ---------------------------------------------------------------------
print("\n== 4. INDEX EXIT RULES on KMI All Share TR from knowable entries to 2026-10-16; cash earns the 3M bill")
y3 = tb.y3m.reindex(pd.date_range(tb.index.min(), sess[-1])).ffill()
k200 = ck.rolling(200).mean()


def run(E, rule, X=None):
    E = pd.Timestamp(E); dates = sess[sess >= E]; val, inn, peak, ex_i, trades, exits = 1.0, True, ck[E], None, 0, []
    eq = []
    for j, d in enumerate(dates):
        if j:
            pd_ = dates[j - 1]
            val *= (ck[d] / ck[pd_]) if inn else (1 + y3[pd_] / 100 * (d - pd_).days / 365)
        if inn:
            peak = max(peak, ck[d])
            out = (rule in ("trail", "trail_re200") and ck[d] <= (1 - X) * peak) or (rule == "ma200" and ck[d] < k200[d])
            if out: inn, ex_i = False, j; exits.append(str(d.date())); trades += 1
        else:
            back = (rule == "trail_re200" and j - ex_i >= 10 and ck[d] > k200[d]) or (rule == "ma200" and ck[d] > k200[d])
            if back: inn, peak = True, ck[d]
        eq.append(val)
    eq = pd.Series(eq, index=dates); dd = (eq / eq.cummax() - 1).min()
    return eq, dd, trades, exits


ENT = ["2019-09-16", "2020-04-03", "2023-07-03", "2024-06-21"]
for E in ENT:
    rows = []
    bh, dd, _, _ = run(E, "bh"); pk = bh.idxmax()
    rows.append(["buy and hold", bh.iloc[-1], bh.max(), dd, 0, ""])
    for X in (0.10, 0.15, 0.20, 0.25, 0.30):
        for rule in ("trail", "trail_re200"):
            eq, dd, n, ex = run(E, rule, X); rows.append([f"{rule} {int(X * 100)}%", eq.iloc[-1], eq[:pk].iloc[-1], dd, n, ",".join(ex[:4]) + ("..." if len(ex) > 4 else "")])
    eq, dd, n, ex = run(E, "ma200"); rows.append(["200d in/out", eq.iloc[-1], eq[:pk].iloc[-1], dd, n, f"{n} switches"])
    print(f"\n-- entry {E} (KMI {ck[E]:.0f}); index peak in window {pk.date()} at {bh.max():.2f}x")
    print(pd.DataFrame(rows, columns=["rule", "x at 16 Oct 2026", "x at index peak date", "max drawdown", "exits", "exit dates"]).to_string(index=False, float_format=lambda x: f"{x:.2f}"))
