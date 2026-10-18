"""regime_turn_2022_23: arithmetic behind knowledge/regime_turns/2022_23.md (the June 2023 turn).
Run: .venv/Scripts/python.exe scripts/tests/regime_turn_2022_23.py  -> tests/out/regime_turn_2022_23.txt

DEFINITIONS (fixed before the results were read).
 Reference low T0 = 2023-06-23 (KSE100 close 40,065). Liquid = daily_table `liquid` (median 60-day traded value above Rs5m).
 Breadth = share of liquid names (in panel_close_adj) above their own 50 / 200-session average of adjusted closes.
 252-high = daily_table dist_252_high == 0. Fire date = first KSE100 close above its 50-session average after 15+ sessions below it
 (the 2023-06-26 and 2023-07-03 columns are the real turn, which had only 5 sessions below).
 Entries: signal at the close, entry at the NEXT open (index: index open; stocks: daily_table next_open, adjusted scale), hold 252 sessions.
 Stock stop: 25% closing trail from the entry price, exit at the next open. Index placeholder stop: 10% closing trail.
 Flows: fipi_lipi.csv daily net USD million by investor type; 2023-06-05 / 01-19 / 08-28 filled from fipi_lipi_by_sector.csv (Debt Market excluded).
 Not modelled: costs, tax, fills, locks. All 12-month results are in-sample hindsight.
"""
import warnings
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.max_rows", 400)
ROOT = Path(__file__).resolve().parents[2]; R = ROOT / "data"


def macro(n): return pd.read_csv(R / f"macro/{n}.csv", parse_dates=["date"]).set_index("date")


kse, kmi = macro("kse100"), macro("kmiallshr"); c = kse.close; sess = c.index
P = pd.read_parquet(R / "panel_close_adj.parquet")
D = pd.read_parquet(R / "daily_table.parquet", columns=["date", "symbol", "close", "ret_20d", "dist_252_high", "liquid", "sector", "kmi_member",
                    "traded_value_median_60", "vol_ratio_1_20", "next_open"])
D = D[D.date >= "2018-01-01"]
T0 = pd.Timestamp("2023-06-23")
usd = macro("usdpkr").value; pol = macro("policy_rate_decisions")["rate"]; tb = macro("tbill_auctions"); fx = macro("fx_reserves")
cpi = pd.read_csv(R / "macro/cpi.csv"); cpi["pub"] = pd.to_datetime(cpi.month + "-01") + pd.offsets.MonthBegin(1) + pd.Timedelta(days=2)
ic = pd.read_csv(R / "macro/import_cover.csv"); ic["m"] = pd.to_datetime(ic.month + "-01")
ma50, ma200, hi252 = c.rolling(50).mean(), c.rolling(200).mean(), c.rolling(252, min_periods=100).max()
at = lambda s, d: s[:d].iloc[-1]

# breadth ---------------------------------------------------------------
m50, m200 = P.rolling(50, min_periods=50).mean(), P.rolling(200, min_periods=200).mean()
Lq = D[D.liquid].pivot(index="date", columns="symbol", values="close").notna().reindex(index=P.index, columns=P.columns, fill_value=False)
ok50, ok200 = Lq & m50.notna() & P.notna(), Lq & m200.notna() & P.notna()
B = pd.DataFrame({"b50": ((P > m50) & ok50).sum(axis=1) / ok50.sum(axis=1), "b200": ((P > m200) & ok200).sum(axis=1) / ok200.sum(axis=1)})
H = D[D.liquid & (D.dist_252_high >= -1e-6)]
Hs = H.groupby("date").symbol.apply(set); nliq = D[D.liquid].groupby("date").symbol.nunique()

# flows -----------------------------------------------------------------
fl = pd.read_csv(R / "macro/fipi_lipi.csv", parse_dates=["date"]); fs = pd.read_csv(R / "macro/fipi_lipi_by_sector.csv", parse_dates=["date"])
G = lambda x: "FIPI" if x in ("foreign corporates", "foreign individual", "overseas pakistani") else x
flow = fl.assign(g=fl.investor_type.map(G)).pivot_table(index="date", columns="g", values="net_usd_mn", aggfunc="sum").fillna(0)
for d in ["2023-06-05", "2023-01-19", "2023-08-28"]:
    x = fs[(fs.date == d) & (fs.sector != "Debt Market")]
    s = x.groupby(x.investor_group.map(lambda g: "FIPI" if g == "fipi" else g.replace("lipi ", ""))).net_usd_mn.sum()
    flow.loc[pd.Timestamp(d)] = s.reindex(flow.columns).fillna(0)
flow = flow.sort_index()

# 1. weekly tables --------------------------------------------------------
print("== TABLE 1/2: weekly, week ending Friday (last session in brackets)")
rows = []
for w in pd.date_range("2023-03-24", "2023-08-18", freq="W-FRI"):
    ws = w - pd.Timedelta(days=6); d = c[:w].index[-1]
    u = set().union(*[Hs.get(x, set()) for x in c[ws:w].index])
    f = flow[ws:w].sum(); cp = cpi[cpi.pub <= w].iloc[-1]
    rows.append(dict(week=w.date(), last=d.day, KSE=round(c[d]), vsT0=c[d] / c[T0] - 1, dd12m=c[d] / hi252[d] - 1, KMI=round(kmi.close[d]), b50=B.b50[d], b200=B.b200[d],
                     n252=len(u), volx=(kse.volume[ws:w] / kse.volume.rolling(50).mean()[ws:w]).mean(), pol=at(pol, w), bill6=at(tb.y6m.dropna(), w),
                     cpi=cp.yoy, res_pit=fx[:w - pd.Timedelta(days=7)].sbp_reserves_usd_mn.iloc[-1] / 1000, pkr=at(usd, w), brent=at(macro("brent").value, w),
                     FIPI=f.FIPI, Cos=f.get("companies", np.nan), Ind=f.get("individuals", np.nan), MF=f.get("mutual funds", np.nan)))
print(pd.DataFrame(rows).round(3).to_string())

# 2. price structure ------------------------------------------------------
print("\n== PRICE STRUCTURE")
z = c["2022-12-01":"2023-06-23"]
print("closes <= 40,100 since 1 Dec:", int((z <= 40100).sum()))
print("swing lows (lowest close within +-8 sessions, below 40,500):",
      [(z.index[i].date(), round(z.iloc[i])) for i in range(8, len(z) - 8) if z.iloc[i] == z.iloc[i - 8:i + 9].min() and z.iloc[i] < 40500])
print("min close after T0:", c[T0 + pd.Timedelta(days=1):].min(), c[T0 + pd.Timedelta(days=1):].idxmin().date())
u = (c / usd.reindex(sess).ffill())["2021-06-01":"2024-06-30"]; print("KSE per USD min:", u.idxmin().date(), round(u.min(), 1), "23 Jun:", round(u[T0], 1))
for d in ["2023-06-26", "2023-06-27", "2023-07-03", "2023-07-04"]:
    print(d, "index volume m", round(kse.volume[d] / 1e6), "x50d", round(kse.volume[d] / kse.volume.rolling(50).mean()[d], 2))
prior = c.rolling(252).max().shift(1)
print("first KSE close above prior 252-high:", c[T0:][c[T0:] > prior[T0:]].index[0].date())

# 3. false bottoms vs real ------------------------------------------------
print("\n== FALSE BOTTOMS vs REAL (signals at the 50-day reclaim)")


def sig(d, label):
    d = pd.Timestamp(d); i = sess.get_loc(d); r = {"label": label, "KSE": round(c[d]), "vs200": c[d] / ma200[d] - 1, "dd12m": c[d] / hi252[d] - 1,
                                                  "vol_x": kse.volume[d] / kse.volume.rolling(50).mean()[d], "b50": B.b50[d], "b200": B.b200[d],
                                                  "b50_p5": B.b50.iloc[B.index.get_loc(d) + 5], "b200_p5": B.b200.iloc[B.index.get_loc(d) + 5]}
    r["n252_win"] = len(set().union(*[Hs.get(x, set()) for x in sess[i - 5:i + 11]])); r["n252_30"] = len(set().union(*[Hs.get(x, set()) for x in sess[i:i + 31]]))
    r["policy"] = at(pol, d); r["bill6_minus_pol"] = at(tb.y6m.dropna(), d) - r["policy"]
    p = cpi[cpi.pub <= d]; r["cpi"], r["cpi_3m"] = p.yoy.iloc[-1], p.yoy.iloc[-4]
    fw = fx[:d - pd.Timedelta(days=7)].sbp_reserves_usd_mn; r["res_bn"], r["res_8w"] = fw.iloc[-1] / 1000, fw.iloc[-1] / fw.iloc[-9] - 1
    r["cover"] = ic[ic.m < d.to_period("M").to_timestamp()].import_cover_sbp_months.iloc[-1]
    r["pkr_before"] = at(usd, d) / at(usd, d - pd.Timedelta(days=28)) - 1; r["pkr_after"] = at(usd, d + pd.Timedelta(days=28)) / at(usd, d) - 1
    r["fipi_before"] = flow[d - pd.Timedelta(days=28):d].FIPI.sum(); r["fipi_after"] = flow[d + pd.Timedelta(days=1):d + pd.Timedelta(days=28)].FIPI.sum()
    for n, k in [("4w", 20), ("12w", 60), ("26w", 126), ("52w", 252)]: r["ret_" + n] = c.iloc[i + k] / c[d] - 1
    r["worst12w"] = c.iloc[i + 1:i + 61].min() / c[d] - 1
    return r


ev = [("2022-08-05", "FB1"), ("2022-10-06", "FB2"), ("2023-02-02", "FB3"), ("2023-04-20", "FB4"), ("2023-06-26", "REAL 26Jun"), ("2023-07-03", "REAL 3Jul")]
print(pd.DataFrame([sig(d, l) for d, l in ev]).set_index("label").T.round(3).to_string())
bill = tb["2021-01-01":].dropna(subset=["y6m"]).copy(); bill["sp"] = bill.y6m - [at(pol, d) for d in bill.index]
print("6M bill minus policy, lowest at an auction 2022-07-13..2023-10-04:", round(bill["2022-07-13":"2023-10-04"].sp.min(), 2),
      "| first auction at/under policy after 2023-10-04:", bill["2023-10-05":][bill["2023-10-05":].sp <= 0].index[0].date())

# 4. leaders ---------------------------------------------------------------
print("\n== FIRST 15 LIQUID 252-HIGHS AFTER T0")
h = H[H.date > T0].sort_values(["date", "traded_value_median_60"], ascending=[True, False]).drop_duplicates("symbol").head(15)
rs = (P.loc[T0] / P.loc["2023-01-17"] - 1); liq0 = [s for s in D[(D.date == T0) & D.liquid].symbol if s in P.columns]
dates = P.index; out = []
for _, r in h.iterrows():
    s = r.symbol; i = dates.get_loc(r.date); e = r.next_open; path = P[s].iloc[i + 1:i + 1 + 252]
    out.append((r.date.date(), s, r.sector, bool(r.kmi_member), round(P[s][r.date] / P[s][T0] - 1, 3), round(rs.get(s, np.nan), 3), round(r.vol_ratio_1_20, 1),
                round(path.iloc[-1] / e - 1, 3), round((path / path.cummax() - 1).min(), 3)))
print(pd.DataFrame(out, columns=["date", "sym", "sector", "kmi", "gain_from_T0", "ret_17Jan_23Jun", "own_vol_x", "bh_12m", "max_dd"]).to_string())
print("liquid-list median 17Jan-23Jun return:", round(rs.reindex(liq0).median(), 3))
x0 = D[(D.date == T0) & D.liquid].set_index("symbol")
for lab, e in [("8w", "2023-08-18"), ("6m", "2023-12-22"), ("12m", "2024-06-21")]:
    t = (P.loc[e] / P.loc[T0] - 1).reindex(x0.index).dropna(); sec = x0.sector.reindex(t.index)
    print(lab, "sector medians:", t.groupby(sec).median().sort_values(ascending=False).round(2).to_dict(), "| all liquid", round(t.median(), 3), "n", len(t))

# 5. entries --------------------------------------------------------------
print("\n== ENTRIES at +1w, +4w, +8w (signal close, next open, 252 sessions)")
Lh = h.assign(sym=h.symbol)
for k, days in [("+1w", 7), ("+4w", 28), ("+8w", 56)]:
    sd = sess[sess.searchsorted(T0 + pd.Timedelta(days=days))]; i = sess.get_loc(sd); e = i + 1
    for nm, df in [("KSE100", kse), ("KMI", kmi.reindex(sess).ffill())]:
        ent = df.open.iloc[e]; path = df.close.iloc[e:e + 252]; peak = ent; ex = None
        for j, (dd, cl) in enumerate(path.items()):
            peak = max(peak, cl)
            if cl <= 0.9 * peak: ex = df.open.iloc[e + j + 1]; exd = sess[e + j + 1]; break
        print(k, nm, "signal", sd.date(), "entry", sess[e].date(), round(ent), "12m %.3f" % (path.iloc[-1] / ent - 1), "worst close %.3f" % (path.min() / ent - 1),
              "maxdd %.3f" % (path / path.cummax() - 1).min(), "10%% trail %.3f" % (ex / ent - 1) if ex else "", exd.date() if ex else "")
    known = h[h.date <= sd]; res = []
    for s in known.symbol:
        row = D[(D.symbol == s) & (D.date == sd)]
        if s not in P.columns or not len(row) or np.isnan(row.next_open.iloc[0]): continue
        ent = row.next_open.iloc[0]; path = P[s].iloc[i + 1:i + 1 + 252]; peak = ent; ex = None
        for dd, cl in path.items():
            peak = max(peak, cl)
            if cl <= 0.75 * peak:
                nx = D[(D.symbol == s) & (D.date == dd)].next_open; ex = nx.iloc[0] if len(nx) and not np.isnan(nx.iloc[0]) else cl; break
        res.append((s, path.iloc[-1] / ent - 1, (ex / ent - 1) if ex is not None else path.iloc[-1] / ent - 1))
    r = pd.DataFrame(res, columns=["s", "bh", "tr25"])
    print(k, "leaders known n=%d" % len(r), "B&H median %.3f mean %.3f | trail25 median %.3f mean %.3f worst %.3f" % (r.bh.median(), r.bh.mean(), r.tr25.median(), r.tr25.mean(), r.tr25.min()))
    allr = []
    for s in D[(D.date == sd) & D.liquid].symbol:
        if s not in P.columns: continue
        ent = D[(D.symbol == s) & (D.date == sd)].next_open.iloc[0]; path = P[s].iloc[i + 1:i + 1 + 252]
        if not np.isnan(ent) and len(path) == 252: allr.append(path.iloc[-1] / ent - 1)
    print(k, "all liquid median %.3f n=%d" % (np.median(allr), len(allr)))

# 6. cross-turn -------------------------------------------------------------
print("\n== CROSS-TURN (same signals at six lows)")
turns = {"2019 Aug": "2019-08-16", "2020 Mar": "2020-03-25", "2023 Jun": "2023-06-23", "2024 Feb": "2024-02-16", "2025 May": "2025-05-08", "2026 Mar": "2026-03-09"}
rows = {}
for nm, T in turns.items():
    T = pd.Timestamp(T); i = sess.get_loc(T); a = c[T:]; r = {}
    f50 = a.index[(a > ma50[T:]).values & (np.arange(len(a)) > 0)][0]; j = sess.get_loc(f50)
    r["first_50d_sessions"] = j - i; r["b200_at_low"] = B.b200[T]; r["b200_5_after_reclaim"] = B.b200.iloc[B.index.get_loc(f50) + 5]
    u = set().union(*[Hs.get(x, set()) for x in sess[j - 5:j + 11]]); r["n252_near_reclaim"] = len(u); r["pct_list"] = len(u) / nliq.get(f50)
    r["first_252_sessions"] = next((sess.get_loc(x) - i for x in sess[i + 1:i + 120] if len(Hs.get(x, ())) > 0), None)
    for n, k in [("4w", 20), ("12w", 60), ("52w", 252)]: r["ret_" + n] = c.iloc[i + k] / c[T] - 1 if i + k < len(c) else np.nan
    r["bill_minus_policy"] = at(tb.y6m.dropna(), T) - at(pol, T)
    fb, fa = flow[T - pd.Timedelta(days=56):T], flow[T + pd.Timedelta(days=1):T + pd.Timedelta(days=28)]
    r["fipi_8w_before"], r["fipi_4w_after"], r["companies_8w_before"] = fb.FIPI.sum(), fa.FIPI.sum(), fb["companies"].sum()
    for lab, days in [("+1w", 7), ("+4w", 28), ("+8w", 56)]:
        e = sess.get_loc(sess[sess.searchsorted(T + pd.Timedelta(days=days))]) + 1; k = min(252, len(sess) - e)
        r["kse_entry_" + lab] = c.iloc[e + k - 1] / kse.open.iloc[e] - 1
    rows[nm] = r
print(pd.DataFrame(rows).round(3).to_string())

# 7. IMF dates -----------------------------------------------------------------
print("\n== IMF SLA/BOARD DATES: KSE100 12-week return from the close on or before the date")
ev = pd.read_csv(ROOT / "seed/data/macro/imf_events.csv", parse_dates=["date"])
ev = pd.concat([ev, pd.DataFrame([{"date": pd.Timestamp("2022-07-13"), "event": "SLA", "program": "7th-8th (events_shocks 73)"}])]).sort_values("date")
for _, r in ev.iterrows():
    d0 = c[:r.date].index[-1]; i = sess.get_loc(d0)
    print(r.date.date(), r.event, r.program, "12w %.3f" % (c.iloc[i + 60] / c[d0] - 1) if i + 60 < len(c) else "n/a")
