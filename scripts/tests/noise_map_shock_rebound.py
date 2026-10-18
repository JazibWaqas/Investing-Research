"""Noise map and shock-rebound playbook. Run: .venv/Scripts/python.exe scripts/tests/noise_map_shock_rebound.py
Writes data/events_shocks.csv, data/events_shocks_metrics.csv and tests/out/noise_map_shock_rebound.txt. See tests/noise_map_shock_rebound.md.
Reuses scripts/prices.py (panel, adjusted returns, liquidity) and the sector baskets in scripts/sector_momentum.py (dict read, script not run)."""
import sys
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s)
def table(h, rows):
    say("| " + " | ".join(h) + " |"); say("|" + "---|" * len(h))
    for r in rows: say("| " + " | ".join(str(c) for c in r) + " |")
    say("")
def pc(v, d=1): return "n/a" if v != v else f"{v*100:+.{d}f}%"
def pp(v): return "n/a" if v != v else f"{v*100:.0f}%"
def nf(v, d=1): return "n/a" if v != v else f"{v:.{d}f}"

H20, H60, FALLWIN = 20, 60, 20      # windows in sessions
SHOCK = -0.05                      # task definition: fall of 5%+ within 20 sessions
FELL = -0.03                       # placeholder (unsourced): a fall counts as one to revert from if >= 3%
BAND = 0.5                         # placeholder: T-bill 6M minus policy rate beyond +-0.5pt = hike/cut expected
NPLAC, SEED = 2000, 17102026
rng = np.random.default_rng(SEED)

# ------------------------------------------------------------------ events (see events block in part 2)
SRC = {
 "pol": "data/macro/policy_rate_decisions.csv",
 "fx": "fxempire.com/credit-ratings/pakistan (rating history table, fetched 2026-10-18; aggregator, not the agencies)",
 "ians": "ianslive.in/pakistans-benchmark-index-plunges-nearly-10-pc-amid-us-iran-war-afghan-tensions--20260302163714",
 "mar9": "profit.pakistantoday.com.pk/2026/03/09/psx-plunges-over-7-as-oil-price-shock-triggers-market-halt/",
 "apr13": "timesofislamabad.com/13-04-2026/psx-kse-100-crashes-by-6600-points-as-us-iran-talks-collapse/",
 "afg": "theweek.in/news/world/2026/02/27/open-war-between-pakistan-and-afghanistan...; thenews.pk/story/1404311",
 "oct25": "en.dailypakistan.com.pk/13-Oct-2025/kse-100-tanks-nearly-3000-points-as-pak-afghan-clashes-shake-market-sentiment",
 "msci": "profit.pakistantoday.com.pk/2021/09/08/msci-downgrades-pakistan-to-frontier-markets; businesswire.com/news/home/20210907005911/en",
 "dec25": "pkrevenue.com/sbp-surprises-markets-cuts-policy-rate-by-50-basis-points-to-10-5/",
 "bud26": "app.com.pk/?p=1224991 (Rs18.771tn FY27 budget presented 12 Jun 2026)",
 "imf22": "dawn.com/news/amp/1762368; arynews.tv/pakistan-imf-reach-staff-level-agreement-sources/",
 "imf25": "Stratfor sitrep citing Reuters, 9 Dec 2025 (paywalled)",
 "imff": "seed/data/macro/imf_events.csv",
 "hz": "knowledge/sectors/exploration_production.md (cites en.wikipedia.org/wiki/2026_Strait_of_Hormuz_campaign)",
 "rec": "public record; date recalled, not re-verified in this run (Dawn, Business Recorder, Wikipedia timelines carry it)",
}
# Hand-curated events live in noise_map_events.psv. status: F repo file, W web-checked this run, R date recalled and not re-verified.
# rule: S = first session that can react is the event date itself (news before the 15:30 close), N = the next session.
ev = pd.read_csv(Path(__file__).with_name("noise_map_events.psv"), sep="|")
ev["source"] = ev.pop("src").map(SRC)
# SBP: every rate change since the first index day, from the repo file. Surprise flagged only where a source says so.
pol = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"])
rows = []
for r in pol[(pol.date >= "2016-10-17") & (pol.change_bp != 0)].itertuples():
    note, st, src = f"MPC {r.change_bp:+d}bp to {r.rate}%", "F", SRC["pol"]
    if r.date == pd.Timestamp("2025-12-15"): note += " SURPRISE (all 12 in a Reuters poll expected a hold)"; st = "W"; src = SRC["dec25"]
    if r.date in (pd.Timestamp("2020-03-17"), pd.Timestamp("2020-03-24"), pd.Timestamp("2022-04-07")): note += " off-cycle/emergency (recalled)"
    rows.append((r.date.strftime("%Y-%m-%d"), "SBP", "hike" if r.change_bp > 0 else "cut", "N", "announcement time not collected, treated as after close", note, st, src))
# rupee: first day of each run of >=1.5% one-day rises in the SBP bank-average USD rate (10-session de-duplication)
u = pd.read_csv(ROOT / "data/macro/usdpkr.csv", index_col=0, parse_dates=True)["value"]; u = u[u.index >= "2016-10-17"]
last = None
for d, v in u.pct_change()[lambda s: s >= 0.015].items():
    if last is None or (u.index.get_loc(d) - last) > 10:
        rows.append((d.strftime("%Y-%m-%d"), "rupee", "devaluation", "S", "SBP daily bank-average rate for that day", f"USD/PKR {v*100:+.1f}% in one day", "F", "data/macro/usdpkr.csv"))
    last = u.index.get_loc(d)
ev = pd.concat([ev, pd.DataFrame(rows, columns=["date", "type", "subtype", "rule", "first_public", "event", "status", "source"])])
ev["date"] = pd.to_datetime(ev["date"])
ev = ev[ev.date >= "2016-10-18"].sort_values(["date", "type"]).reset_index(drop=True)
ev.insert(0, "id", range(1, len(ev) + 1))

# ------------------------------------------------------------------ data
kse = pd.read_csv(ROOT / "data/macro/kse100.csv", index_col=0, parse_dates=True)["close"]
cal, n = kse.index, len(kse)
kmi = pd.read_csv(ROOT / "data/macro/kmiallshr.csv", index_col=0, parse_dates=True)["close"].reindex(cal).ffill()
K, M = kse.values, kmi.values
close, vol, tv = [x.reindex(cal) for x in P.load_panel()]
cols = list(close.columns)
acts = P.provisional_actions()
ret_a = P.returns(close, "adjusted", vol=vol, actions=acts)
CA = (1 + ret_a.fillna(0)).cumprod().values
LIQ = (P._med_tv(tv) > 5e6).values
loc = {}
exec("S = " + (ROOT / "scripts/sector_momentum.py").read_text().split("END =")[0].split("S = ", 1)[1], {}, loc)
SEC = {k: [cols.index(t) for t in v.split() if t in cols] for k, v in loc["S"].items()}
fl = pd.read_csv(ROOT / "data/macro/fipi_lipi.csv", parse_dates=["date"])
FL = fl.pivot_table(index="date", columns="investor_type", values="net_usd_mn", aggfunc="sum").reindex(cal)
FLX = FL.fillna(0).values; FLT = list(FL.columns); FL_OK = FL.notna().any(axis=1).values
tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"]).set_index("date")
tb["y"] = tb.y6m.fillna(tb.y3m)
def regime(d):
    p = pol[pol.date <= d]; t = tb[tb.index <= d]
    if p.empty or t.empty: return "n/a", "n/a"
    sp = t.y.iloc[-1] - p.rate.iloc[-1]
    imp = "hike-expected" if sp > BAND else "cut-expected" if sp < -BAND else "neutral"
    ch = p[p.date > d - pd.Timedelta(days=180)].change_bp.sum()
    return imp, ("hike cycle" if ch > 0 else "cut cycle" if ch < 0 else "flat")

# ------------------------------------------------------------------ index metrics
def metr(px, i0):
    """Event metrics for reaction session i0 (day 1) on series px. Base = close of i0-1."""
    out = dict.fromkeys(["d1", "fall", "sess_bottom", "rise", "ret20", "reb5", "reb10", "reb20", "reb60", "rev_sess", "rev60", "bot"], np.nan)
    if i0 < 1 or i0 >= n or not np.isfinite(px[i0 - 1]): return out
    base = px[i0 - 1]; out["d1"] = px[i0] / base - 1
    if i0 + FALLWIN - 1 >= n: return out
    w = px[i0:i0 + FALLWIN]; k = int(np.argmin(w)); b = i0 + k
    out.update(fall=w[k] / base - 1, sess_bottom=k + 1, rise=w.max() / base - 1, ret20=w[-1] / base - 1, bot=b)
    for h in (5, 10, 20, 60):
        if b + h < n: out[f"reb{h}"] = px[b + h] / px[b] - 1
    if b + 60 < n:
        hit = np.where(px[b + 1:b + 61] >= base)[0]
        out["rev_sess"] = hit[0] + 1 if len(hit) else np.nan
        out["rev60"] = float(len(hit) > 0)
    return out

ev["i0"] = [cal.searchsorted(d, "left" if r == "S" else "right") for d, r in zip(ev.date, ev.rule)]
ev = ev[ev.i0 < n].copy()
ev["react_date"] = [cal[i].date() for i in ev.i0]
reg = [regime(cal[i]) for i in ev.i0]; ev["regime_tbill"] = [r[0] for r in reg]; ev["regime_cycle"] = [r[1] for r in reg]
for nm, px in (("kse", K), ("kmi", M)):
    ev = ev.join(pd.DataFrame([metr(px, i) for i in ev.i0], index=ev.index).add_prefix(nm + "_"))
ev["bot"] = ev.kse_bot

# ------------------------------------------------------------------ breadth, names, sectors, flows (around the KSE100 bottom)
def secret(i_from, i_to, liq_row):
    r = {}
    for s, m in SEC.items():
        mm = [j for j in m if liq_row[j] and np.isfinite(CA[i_from, j])]
        if len(mm) >= 2: r[s] = float(np.mean(CA[i_to, mm] / CA[i_from, mm] - 1))
    return r
def secbreadth(i_from, i_to, liq_row):
    r = {}
    for s, m in SEC.items():
        mm = [j for j in m if liq_row[j]]
        if len(mm) >= 2: r[s] = float(np.mean(CA[i_to, mm] / CA[i_from, mm] - 1 > 0))
    return r
extra = []
for r in ev.itertuples():
    o = {}
    i0 = r.i0; b = int(r.bot) if r.bot == r.bot else None
    if b is not None:
        ix = np.where(LIQ[i0])[0]; o["n_liquid"] = len(ix)
        fall_r = CA[b, ix] / CA[i0 - 1, ix] - 1; o["breadth_fall_down"] = float(np.mean(fall_r < 0)); o["med_name_fall"] = float(np.median(fall_r))
        if b + 20 < n:
            rr = CA[b + 20, ix] / CA[b, ix] - 1; o["breadth_reb_up"] = float(np.mean(rr > 0)); o["med_name_reb20"] = float(np.median(rr))
            top = np.argsort(-rr)[:10]
            o["top10"] = " ".join(f"{cols[ix[t]]}({rr[t]*100:+.0f}%)" for t in top); o["top10_syms"] = " ".join(cols[ix[t]] for t in top)
            sr = secret(b, b + 20, LIQ[i0]); sb = secbreadth(b, b + 20, LIQ[i0])
            o["top_sectors_reb"] = "; ".join(f"{s} {v*100:+.0f}%" for s, v in sorted(sr.items(), key=lambda x: -x[1])[:3])
            o["top_sectors_breadth"] = "; ".join(f"{s} {sb[s]*100:.0f}%" for s in sorted(sb, key=lambda s: (-sb[s], -sr.get(s, 0)))[:3])
            for s, v in sr.items(): o["secreb_" + s] = v
        if FL_OK[i0:b + 21].any():
            for j, t in enumerate(FLT):
                o["fall_" + t] = FLX[i0:b + 1, j].sum()
                if b + 20 < n: o["reb_" + t] = FLX[b + 1:b + 21, j].sum()
    extra.append(o)
ev = ev.join(pd.DataFrame(extra, index=ev.index))

# ------------------------------------------------------------------ placebo: every session as day 1
pl = pd.DataFrame([metr(K, i) for i in range(1, n)]); pl["i0"] = range(1, n)
plk = pl[pl.fall.notna()]
def band(nn, col, q=(5, 95)):
    v = plk[col].dropna().values
    return np.percentile([np.median(rng.choice(v, nn)) for _ in range(NPLAC)], q)

# ------------------------------------------------------------------ report
say("NOISE MAP AND SHOCK REBOUND. Data to", cal[-1].date(), "| KSE100 = total return index (INDEX_NOTES.md), KMIALLSHR total return. Panel: survivors only (flatters name and sector results).")
say(f"{len(ev)} events 2016-10-18 to 2026-10-16; day 1 = first session that can price the news; base = close the session before; fall/bottom = lowest close in the first {FALLWIN} sessions (day 1 = 1).")
say("Status: F repo file, W web-verified this run, R date recalled and not re-verified:", ev.status.value_counts().to_dict())
say("")
say("## Events by type"); say(ev.groupby("type").size().to_string()); say("")
say("## Event table (KSE100; reb = rise from the bottom; rev = sessions from bottom to regain the pre-event close; n/a where the window runs past 16 Oct 2026)")
table(["id", "date", "react", "type/sub", "event", "d1", "fall20", "sess", "reb5", "reb10", "reb20", "reb60", "rev", "KMI d1", "KMI fall", "breadth up", "st"],
      [(r.id, r.date.date(), r.react_date, f"{r.type}/{r.subtype}", r.event[:48], pc(r.kse_d1), pc(r.kse_fall), nf(r.kse_sess_bottom, 0), pc(r.kse_reb5), pc(r.kse_reb10), pc(r.kse_reb20), pc(r.kse_reb60),
        nf(r.kse_rev_sess, 0), pc(r.kmi_d1), pc(r.kmi_fall), pp(getattr(r, "breadth_reb_up", np.nan)), r.status) for r in ev.itertuples()])

say("## Noise map per type. Verdict rule fixed before the run: a type REPRICES if its median day-1 move or median 20-session return from base lies outside the 5th-95th percentile of medians of the same number of random dates; otherwise IGNORED.")
types = list(ev.groupby("type").size().sort_values(ascending=False).index)
hdr = ["group", "n", "med d1", "med max fall", "med sess to bottom", "med ret20 from base", "med reb20", "med reb60", "fall>=3% regained base <=60s of bottom", "placebo d1 5-95", "placebo ret20 5-95", "verdict"]
def typerow(label, g):
    nn = len(g); kk = g.dropna(subset=["kse_fall"])
    d1, fall, sb, r20, b20, b60 = g.kse_d1.median(), g.kse_fall.median(), g.kse_sess_bottom.median(), g.kse_ret20.median(), g.kse_reb20.median(), g.kse_reb60.median()
    rv = kk[kk.kse_fall <= FELL].kse_rev60.dropna()
    bd, br = band(nn, "d1"), band(nn, "ret20")
    out = d1 < bd[0] or d1 > bd[1] or r20 < br[0] or r20 > br[1]
    rs = (pp(rv.mean()) if len(rv) else "n/a") + f" ({int(rv.sum())}/{len(rv)})"
    return [label, nn, pc(d1), pc(fall), nf(sb), pc(r20), pc(b20), pc(b60), rs, f"{bd[0]*100:+.1f}..{bd[1]*100:+.1f}", f"{br[0]*100:+.1f}..{br[1]*100:+.1f}", "REPRICES" if out else "ignored"]
table(hdr, [typerow(t, ev[ev.type == t]) for t in types])
def prow(lab, g):
    return [lab, len(g), pc(g.d1.median()), pc(g.fall.median()), nf(g.sess_bottom.median()), pc(g.ret20.median()), pc(g.reb20.median()), pc(g.reb60.median()), pp(g[g.fall <= FELL].rev60.mean())]
say("Placebo reference classes (KSE100, every session as day 1; windows overlap):")
table(hdr[:9], [prow("all random sessions", plk), prow("random sessions with d1 <= -3%", plk[plk.d1 <= -0.03]), prow("random sessions with d1 <= -5%", plk[plk.d1 <= -0.05])])
say("Subtypes with n>=4:")
sub = ev.groupby(["type", "subtype"]).filter(lambda g: len(g) >= 4)
table(hdr, [typerow(f"{t}/{s}", g) for (t, s), g in sub.groupby(["type", "subtype"])])
say("Same on KMIALLSHR by type:")
table(["type", "n", "KMI med d1", "KMI med fall", "KMI med reb20", "KMI med reb60"],
      [[t, len(g), pc(g.kmi_d1.median()), pc(g.kmi_fall.median()), pc(g.kmi_reb20.median()), pc(g.kmi_reb60.median())] for t, g in ev.groupby("type")])
say("Direction check: day-1 move for good-news vs bad-news subtypes")
table(["group", "n", "med d1", "mean d1", "share d1>0"],
      [[lab, len(g), pc(g.kse_d1.median()), pc(g.kse_d1.mean()), pp((g.kse_d1 > 0).mean())] for lab, g in
       [("IMF SLA/board", ev[(ev.type == "IMF") & ev.subtype.isin(["SLA", "board"])]), ("IMF stall/decision", ev[(ev.type == "IMF") & ev.subtype.isin(["stall", "decision"])]),
        ("rating upgrade", ev[ev.subtype == "upgrade"]), ("rating downgrade", ev[ev.subtype == "downgrade"]), ("SBP cut", ev[ev.subtype == "cut"]), ("SBP hike", ev[ev.subtype == "hike"]),
        ("ceasefire events", ev[ev.event.str.contains("ceasefire")])]])
dd = pd.Series(np.r_[np.nan, K[1:] / K[:-1] - 1], cal)
cov = set()
for i in ev.i0: cov.update(range(i - 1, i + 2))
un = dd[(dd <= -0.035) & np.array([i not in cov for i in range(n)])]
say(f"Coverage check: {int((dd<=-0.035).sum())} sessions fell 3.5% or more; {len(un)} are not within a session of any event above (candidate misses, unexplained):")
say(", ".join(f"{d.date()} {v*100:+.1f}%" for d, v in un.items())); say("")

# ------------------------------------------------------------------ shocks, leaders, flows
sh = ev[ev.kse_fall <= SHOCK].copy()
cl, lasti = [], -999
for r in sh.sort_values("i0").itertuples():
    if r.i0 > lasti + 20: cl.append(r.Index); lasti = r.i0
shc = sh.loc[cl]
say(f"## Shocks with a 20-session fall of 5%+: {len(sh)} events, {len(shc)} after keeping the first event of any cluster (events within 20 sessions of an included one dropped)")
table(["id", "date", "type", "event", "fall", "bottom date", "reb20", "reb60", "cluster kept"],
      [(r.id, r.date.date(), r.type, r.event[:50], pc(r.kse_fall), cal[int(r.bot)].date(), pc(r.kse_reb20), pc(r.kse_reb60), "yes" if r.Index in cl else "") for r in sh.itertuples()])
say("Rebound pattern across the clustered shocks (KSE100):")
for c, lab in [("kse_d1", "day 1"), ("kse_fall", "max fall"), ("kse_sess_bottom", "sessions to bottom"), ("kse_reb5", "reb5"), ("kse_reb10", "reb10"), ("kse_reb20", "reb20"), ("kse_reb60", "reb60")]:
    v = shc[c].dropna(); say(f"  {lab}: n={len(v)} median {v.median():.3f} mean {v.mean():.3f} min {v.min():.3f} max {v.max():.3f}")
rv = shc.kse_rev60.dropna(); say(f"  regained pre-event close within 60 sessions of the bottom: {int(rv.sum())}/{len(rv)}; median sessions {shc.kse_rev_sess.median()}")
say(f"  breadth: share of liquid names up in the 20 sessions after the bottom, median {shc.breadth_reb_up.median():.2f}; share down at the bottom vs base, median {shc.breadth_fall_down.median():.2f}")
say("")
say("Leaders: top-10 liquid names by 20-session return from the bottom, clustered shocks")
table(["id", "event", "bottom", "top-10 names (20-session return from bottom)", "top sectors (return)", "top sectors (breadth)", "breadth up"],
      [(r.id, r.event[:32], cal[int(r.bot)].date(), r.top10 if isinstance(r.top10, str) else "n/a", r.top_sectors_reb if isinstance(r.top_sectors_reb, str) else "",
        r.top_sectors_breadth if isinstance(r.top_sectors_breadth, str) else "", pp(r.breadth_reb_up)) for r in shc.itertuples()])
cnt = Counter(s for t in shc.top10_syms.dropna() for s in t.split())
say("Names most often in the top 10 (of %d clustered shocks): %s" % (shc.top10_syms.notna().sum(), ", ".join(f"{k} {v}" for k, v in cnt.most_common(15)))); say("")
sc = [c for c in shc.columns if c.startswith("secreb_")]
sm = pd.DataFrame({"med": shc[sc].median(), "beat": (shc[sc].sub(shc[sc].median(axis=1), axis=0) > 0).sum() / shc[sc].notna().sum(), "n": shc[sc].notna().sum()}).sort_values("med", ascending=False)
say("Sector baskets, 20-session return from the bottom, clustered shocks (liquid members, equal-weight buy-and-hold); beat = share of shocks where the sector beat that shock median sector:")
table(["sector", "n shocks", "median reb20", "beat"], [(i[7:], int(r["n"]), pc(r["med"]), pp(r["beat"])) for i, r in sm.iterrows()])
sy = [t.split() for t in shc.top10_syms.dropna()]
hits = [len(set(sy[k][:3]) & set(sy[k + 1])) for k in range(len(sy) - 1)]
say(f"Does the leader repeat? mean overlap of one shock top 3 names with the next shock top 10: {np.mean(hits):.2f} of 3 (random expectation about {3*10/np.mean([LIQ[int(i)].sum() for i in shc.i0]):.2f})"); say("")

say("## Who sold and who bought: net USD mn by investor type, clustered shocks since 2017-01 (fall = day 1 to bottom; rebound = 20 sessions after bottom).")
fs = shc[shc.date >= "2017-01-02"]
fr = []
for t in FLT:
    a, b2 = fs["fall_" + t].dropna(), fs["reb_" + t].dropna()
    fr.append((t, len(a), nf(a.median(), 1), f"{int((a>0).sum())}/{len(a)}", nf(a.sum(), 0), nf(b2.median(), 1), f"{int((b2>0).sum())}/{len(b2)}", nf(b2.sum(), 0)))
table(["investor type", "n", "fall median", "net buyer in fall", "fall total", "rebound median", "net buyer in rebound", "rebound total"], fr)
fo = ["foreign corporates", "foreign individual"]
ff = fs[["fall_" + t for t in fo]].sum(axis=1, min_count=1); fb = fs[["reb_" + t for t in fo]].sum(axis=1, min_count=1)
say(f"Foreign (corporates + individual): fall median {ff.median():.1f}, rebound median {fb.median():.1f}; net sellers in the fall in {int((ff<0).sum())}/{ff.notna().sum()} shocks, net buyers in the rebound in {int((fb>0).sum())}/{fb.notna().sum()}.")
say(f"Check: daily sum of net flows across types, median abs {FL.sum(axis=1).abs().median():.2f} USD mn (should be near 0)"); say("")
say("Per shock (fall/rebound, USD mn):")
GR = ("foreign corporates", "mutual funds", "individuals", "banks / dfi", "companies", "insurance companies", "broker proprietary trading")
for r in shc.itertuples():
    g = ev.loc[r.Index]
    if not np.isfinite(g.get("fall_individuals", np.nan)): continue
    say(f"  {r.id} {r.date.date()} {r.event[:34]:34s} " + " | ".join(f"{t[:9]} {g.get('fall_'+t, np.nan):+.0f}/{g.get('reb_'+t, np.nan):+.0f}" for t in GR))
say("")

# ------------------------------------------------------------------ trading test
def summ(v):
    v = np.array([x for x in v if x == x])
    return (len(v), v.mean(), np.median(v), (v > 0).mean(), v.min()) if len(v) else (0, np.nan, np.nan, np.nan, np.nan)
def fwd(px, e, h):
    if e is None or e + h >= n: return np.nan, np.nan
    return px[e + h] / px[e] - 1, px[e:e + h + 1].min() / px[e] - 1
def entries(px, i0, b):
    ec = next((j for j in range(b + 1, min(b + 30, n)) if px[j] > px[j - 1]), None)
    ed = next((j for j in range(i0 + 1, min(i0 + 30, n)) if px[j] > px[j - 1]), None)
    return {"a day-1 close": i0, "b day-3 close": i0 + 2, "c first up-day after bottom (hindsight)": ec, "d first up-day after day 1 (tradable)": ed}
def sec_trade(e, i0, b, h, how):
    if e is None or e + h >= n: return np.nan, np.nan
    liq = LIQ[e]
    if how == "pit":
        sr = secret(i0 - 1, e, liq); pick = sorted(sr, key=lambda s: -sr[s])[:3]      # least-fallen sectors at the entry date
    else:
        if b + 20 >= n: return np.nan, np.nan
        sb = secbreadth(b, b + 20, liq); sr = secret(b, b + 20, liq)
        pick = sorted(sb, key=lambda s: (-sb[s], -sr.get(s, 0)))[:3]                   # hindsight: broadest rebound
    paths = []
    for s in pick:
        m = [j for j in SEC[s] if liq[j] and np.isfinite(CA[e, j])]
        if len(m) >= 2: paths.append((CA[e:e + h + 1, m] / CA[e, m]).mean(axis=1))
    if not paths: return np.nan, np.nan
    p = np.mean(paths, axis=0); return p[-1] - 1, p.min() - 1
def trade_block(evs, px, sectors):
    R = {}
    for r in evs.itertuples():
        b = int(r.bot)
        for ek, e in entries(px, r.i0, b).items():
            for h in (H20, H60):
                R.setdefault((ek, "index", h), []).append((r.Index,) + fwd(px, e, h))
                if sectors:
                    R.setdefault((ek, "pit sectors", h), []).append((r.Index,) + sec_trade(e, r.i0, b, h, "pit"))
                    R.setdefault((ek, "hindsight sectors", h), []).append((r.Index,) + sec_trade(e, r.i0, b, h, "hind"))
    return R
def report_trades(R, title, sel=None):
    if title: say(title)
    rows = []
    for ek, what in sorted({(k[0], k[1]) for k in R}):
        a = [x for x in R[(ek, what, H20)] if sel is None or x[0] in sel]; b2 = [x for x in R[(ek, what, H60)] if sel is None or x[0] in sel]
        s20, s60 = summ([x[1] for x in a]), summ([x[1] for x in b2])
        dw = [x[2] for x in b2 if x[2] == x[2]]
        rows.append((ek, what, s20[0], pc(s20[2]), pp(s20[3]), pc(s20[4]), s60[0], pc(s60[1]), pc(s60[2]), pp(s60[3]), pc(s60[4]), pc(np.median(dw)) if dw else "n/a", pc(min(dw)) if dw else "n/a"))
    table(["entry", "buy", "n20", "med 20", "win 20", "worst 20", "n60", "mean 60", "med 60", "win 60", "worst 60", "med worst drawdown in 60", "worst drawdown in 60"], rows)
say("## Playbook: buy after a shock with a 5%+ fall (KSE100 total return as the index; sectors from the sector_momentum baskets)")
say("Selecting events by the realised 20-session fall uses hindsight; rule (a) is tradable only if you would have bought every shock. Entry (c) uses the hindsight bottom, (d) is the tradable stand-in. pit sectors = three least-fallen sectors from base to the entry date (known at entry). hindsight sectors = three broadest rebounds from bottom to bottom+20 (a ceiling, not tradable). Returns are from the entry close.")
Rk = trade_block(shc, K, True); report_trades(Rk, f"All clustered shocks (n={len(shc)}), KSE100:")
report_trades(trade_block(shc, M, False), "Same on KMIALLSHR (index only):")
shd = ev[ev.kse_d1 <= -0.03].copy()
cl2, lasti = [], -999
for r in shd.sort_values("i0").itertuples():
    if r.i0 > lasti + 20: cl2.append(r.Index); lasti = r.i0
report_trades(trade_block(ev.loc[cl2], K, False), f"Tradable trigger instead (day-1 return <= -3%, a placeholder; clustered n={len(cl2)}), KSE100 index only:")
p20 = np.array([K[i + H20] / K[i] - 1 for i in range(1, n - H20)]); p60 = np.array([K[i + H60] / K[i] - 1 for i in range(1, n - H60)])
say(f"Placebo, buy the KSE100 on any random close: 20-session median {np.median(p20)*100:+.1f}%, win {np.mean(p20>0)*100:.0f}%, worst {p20.min()*100:+.1f}%; 60-session median {np.median(p60)*100:+.1f}%, win {np.mean(p60>0)*100:.0f}%, worst {p60.min()*100:+.1f}%.")
d1c = [i for i in range(1, n - H60) if K[i] / K[i - 1] - 1 <= -0.03]
v20 = np.array([K[i + H20] / K[i] - 1 for i in d1c]); v60 = np.array([K[i + H60] / K[i] - 1 for i in d1c])
say(f"Placebo, buy the close of any day that fell 3%+ (n={len(d1c)}, overlapping): 20-session median {np.median(v20)*100:+.1f}%, win {np.mean(v20>0)*100:.0f}%; 60-session median {np.median(v60)*100:+.1f}%, win {np.mean(v60>0)*100:.0f}%, worst {v60.min()*100:+.1f}%.")
say("")
say("Sector picks minus the index, 20-session return, same entry (clustered shocks):")
for ek in ["a day-1 close", "b day-3 close", "d first up-day after day 1 (tradable)"]:
    di = {x[0]: x[1] for x in Rk[(ek, "index", H20)]}; dp = {x[0]: x[1] for x in Rk[(ek, "pit sectors", H20)]}; dh = {x[0]: x[1] for x in Rk[(ek, "hindsight sectors", H20)]}
    a = np.array([dp[k] - di[k] for k in di if dp[k] == dp[k] and di[k] == di[k]]); c = np.array([dh[k] - di[k] for k in di if dh[k] == dh[k] and di[k] == di[k]])
    say(f"  {ek}: pit sectors minus index median {np.median(a)*100:+.1f}%, beat index {np.mean(a>0)*100:.0f}% (n={len(a)}); hindsight sectors minus index median {np.median(c)*100:+.1f}%, beat {np.mean(c>0)*100:.0f}%")
say("")
say("## By regime (T-bill 6M minus policy rate; band +-%.1fpt is a placeholder). Index and pit sectors, clustered 5%%+ shocks" % BAND)
for rg in ["hike-expected", "neutral", "cut-expected"]:
    sel = set(shc.index[shc.regime_tbill == rg]); say(f"{rg}: n={len(sel)} shocks: " + ", ".join(str(shc.loc[i, "date"].date()) for i in sel))
    if sel: report_trades({k: v for k, v in Rk.items() if k[1] != "hindsight sectors"}, "", sel)
say("Cross-tab, realised policy-rate cycle over the previous 180 days (rows) vs T-bill label (columns), clustered shocks:")
say(pd.crosstab(shc.regime_cycle, shc.regime_tbill).to_string()); say("")
say("All 5%+ events by regime:")
table(["regime", "n", "med fall", "med sess", "med reb20", "med reb60"], [[rg, int((sh.regime_tbill == rg).sum()), pc(sh[sh.regime_tbill == rg].kse_fall.median()), nf(sh[sh.regime_tbill == rg].kse_sess_bottom.median()), pc(sh[sh.regime_tbill == rg].kse_reb20.median()), pc(sh[sh.regime_tbill == rg].kse_reb60.median())] for rg in ["hike-expected", "neutral", "cut-expected"]])
say("Regime at all events (count): " + str(ev.regime_tbill.value_counts().to_dict()))

# ------------------------------------------------------------------ point-in-time trigger: buy only if the index is already down 5%+ from the pre-event close at the entry close
say("")
say("## Clean version: trigger known at entry. Buy at the entry close only if the KSE100 is already 5%+ below the pre-event close at that moment (any event type; first trigger per 20 sessions). No hindsight in the selection.")
def pit_block(trig):
    R, used, seen = {}, [], -999
    cand = []
    for r in ev.itertuples():
        for ek, e in entries(K, r.i0, int(r.bot) if r.bot == r.bot else r.i0).items():
            if ek[0] in "abd" and e is not None and e < n and K[e] / K[r.i0 - 1] - 1 <= trig: cand.append((e, ek, r.Index))
    for e, ek, idx in sorted(cand):
        if e > seen + 20: seen = e; used.append((e, ek, idx))
    rows = []
    for e, ek, idx in used:
        r20, d20 = fwd(K, e, H20); r60, d60 = fwd(K, e, H60)
        rows.append((cal[e].date(), ek[:1], ev.loc[idx, "event"][:40], K[e] / K[ev.loc[idx, "i0"] - 1] - 1, r20, r60, d60, np.nan))
    return rows
for trig in (-0.05, -0.03):
    rows = pit_block(trig)
    r20 = [x[4] for x in rows if x[4] == x[4]]; r60 = [x[5] for x in rows if x[5] == x[5]]; dd60 = [x[6] for x in rows if x[6] == x[6]]
    say(f"Trigger: down {abs(trig)*100:.0f}%+ from the pre-event close at the entry close. {len(rows)} trades (20-session windows apart). 20-session: median {np.median(r20)*100:+.1f}%, mean {np.mean(r20)*100:+.1f}%, win {np.mean(np.array(r20)>0)*100:.0f}%, worst {min(r20)*100:+.1f}%. 60-session (n={len(r60)}): median {np.median(r60)*100:+.1f}%, mean {np.mean(r60)*100:+.1f}%, win {np.mean(np.array(r60)>0)*100:.0f}%, worst {min(r60)*100:+.1f}%; median worst drawdown inside 60 {np.median(dd60)*100:+.1f}%, worst {min(dd60)*100:+.1f}%.")
    if trig == -0.05:
        table(["entry date", "rule", "event", "down from base", "ret20", "ret60", "worst dd in 60"], [(x[0], x[1], x[2], pc(x[3]), pc(x[4]), pc(x[5]), pc(x[6])) for x in rows])
# placebo for the same trigger on any session: trailing 1-day or 3-day fall to 5%+ below the close 1 or 3 sessions earlier, first per 20 sessions
for lab, lag in (("1-day", 1), ("3-day", 3)):
    for trig in (-0.05, -0.03):
        idx, seen = [], -999
        for i in range(lag, n - H60):
            if K[i] / K[i - lag] - 1 <= trig and i > seen + 20: idx.append(i); seen = i
        a, b = np.array([K[i + H20] / K[i] - 1 for i in idx]), np.array([K[i + H60] / K[i] - 1 for i in idx])
        say(f"Placebo reference, any session after a {lab} fall of {abs(trig)*100:.0f}%+ (first per 20 sessions, n={len(idx)}): 20-session median {np.median(a)*100:+.1f}%, win {np.mean(a>0)*100:.0f}%; 60-session median {np.median(b)*100:+.1f}%, win {np.mean(b>0)*100:.0f}%, worst {b.min()*100:+.1f}%.")

# ------------------------------------------------------------------ write
ev.drop(columns=["i0", "bot"]).to_csv(ROOT / "data/events_shocks_metrics.csv", index=False)
ev[["id", "date", "type", "subtype", "event", "first_public", "react_date", "rule", "source", "status"]].to_csv(ROOT / "data/events_shocks.csv", index=False)
(ROOT / "tests/out/noise_map_shock_rebound.txt").write_text("\n".join(OUT), encoding="utf-8")
