"""Rate-cycle turns and inflation turns (redo of seed H1-H6). Run: .venv/Scripts/python.exe scripts/tests/rate_cycle_episodes.py
Output is printed and saved to tests/out/rate_cycle_episodes.txt. Reuses scripts/prices.py. See tests/rate_cycle_episodes.md."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s)
def table(headers, rows):
    say("| " + " | ".join(headers) + " |"); say("|" + "---|" * len(headers))
    for r in rows: say("| " + " | ".join(str(c) for c in r) + " |")
    say("")
def pc(v): return "n/a" if v != v else f"{v*100:+.1f}%"
def pp(v): return "n/a" if v != v else f"{v*100:.0f}%"

COST, HS, NDRAW = 0.005, (20, 60, 120, 250), 10000
rng = np.random.default_rng(17102026)
SURV = "EW survivorship: panel holds only symbols listed on 2026-10-16 (456 of 528 seed files non-empty), delisted losers missing, EW biased UP."

# ---------------------------------------------------------------- data
kse = pd.read_csv(ROOT / "data/macro/kse100.csv", index_col=0, parse_dates=True)["close"]
cal, n, K, CAL0 = kse.index, len(kse), kse.values, kse.index[0]
close, vol, tv = [x.reindex(cal) for x in P.load_panel()]
cols = list(close.columns); S = len(cols); colix = {c: j for j, c in enumerate(cols)}
ret_c = P.returns(close, "crude", vol=vol)
acts = P.provisional_actions()
ret_a = P.returns(close, "adjusted", vol=vol, actions=acts)
LIQ = (P._med_tv(tv) > 5e6).values
for d in ("2018-01-30", "2020-03-18", "2024-06-11", "2025-12-16"):   # vectorised mask must equal liquid_universe()
    assert set(np.array(cols)[LIQ[cal.searchsorted(d)]]) == set(P.liquid_universe(d)), d

def zeros(): return np.zeros((n, S), bool)
Fs, Fb, Fcash = zeros(), zeros(), zeros()
sus = pd.read_csv(P.SUSPECTS, parse_dates=["date"])
for r in sus.itertuples():
    j, i = colix.get(r.symbol), cal.searchsorted(r.date)
    if j is not None and i < n and cal[i] == r.date: Fs[i, j] = True
pct, prev, gap, vr, big = P._moves(close, vol)
Fc = ((pct <= -0.08) & (pct >= -0.105) & (vr <= 3) & (prev > 10)).values   # candidate undetected bonus
for r in acts.itertuples():
    j, i = colix.get(r.symbol), cal.searchsorted(r.ex_date)
    if j is not None and i < n: (Fb if r.type in ("bonus", "split") else Fcash)[i, j] = True
FB = Fs | Fc | Fb          # flag B: suspected log, candidate bonus, provisional bonus/split ex-date
FA = FB | Fcash            # flag A: B plus any provisional action incl. cash dividends (spec-literal)
CFB, CFA = np.cumsum(FB, 0), np.cumsum(FA, 0)
IDX = np.arange(n)
def endi(h): return np.minimum(IDX + h, n - 1)
COMPLETE = {h: IDX + h <= n - 1 for h in HS}
CC = (1 + ret_c.fillna(0)).cumprod().values
CA = (1 + ret_a.fillna(0)).cumprod().values
R_c = {h: CC[endi(h)] / CC - 1 for h in HS}
R_a = {h: CA[endi(h)] / CA - 1 for h in HS}
FLB = {h: (CFB[endi(h)] - CFB) > 0 for h in HS}
FLA = {h: (CFA[endi(h)] - CFA) > 0 for h in HS}
def bask(R, mask):
    c = mask.sum(1); s = np.where(mask, R, 0.0).sum(1)
    return np.where(c > 0, s / np.maximum(c, 1), np.nan), c
ser, cnt = {}, {}
for h in HS:
    ser[("KSE", h)] = K[endi(h)] / K - 1
    for nm, R, fl in (("EW", R_c, None), ("EWX", R_c, FLB[h]), ("EWA", R_a, None), ("EWAX", R_a, FLB[h])):
        ser[(nm, h)], cnt[(nm, h)] = bask(R[h], LIQ if fl is None else LIQ & ~fl)
MINC = {"KSE": 0, "EW": 10, "EWX": 5, "EWA": 10, "EWAX": 5}
def valid(name, h):
    ok = COMPLETE[h] & (IDX >= 1)                         # t0 from 2016-10-18 on
    if name != "KSE": ok = ok & (cnt[(name, h)] >= MINC[name])
    return np.where(ok)[0]

def stats(v):
    v = np.array([x for x in v if x == x])
    return None if len(v) == 0 else dict(n=len(v), mean=v.mean(), med=np.median(v), win=(v > 0).mean(), worst=v.min())
def plc(x, k, obs):
    x = x[x == x]; m = x[rng.integers(0, len(x), size=(NDRAW, k))].mean(1)
    return dict(med=np.median(m), lo=np.percentile(m, 5), hi=np.percentile(m, 95), pct=((m < obs).mean() + 0.5 * (m == obs).mean()) * 100,
                umed=np.median(x), uwin=(x > 0).mean(), nv=len(x))
HEAD = ["set", "series", "h", "n_episodes", "mean", "median", "win", "worst", "plc median of k-mean", "plc 5-95%", "obs pctile", "net mean (-0.5%)", "uncond median / win", "power"]
def hrow(label, name, h, idx, trade=True, vidx=None):
    v = [ser[(name, h)][i] for i in idx if COMPLETE[h][i]]
    s = stats(v)
    if s is None: return [label, name, h, 0, "not computable: no complete window"] + [""] * 9
    vi = valid(name, h) if vidx is None else vidx
    p = plc(ser[(name, h)][vi], s["n"], s["mean"])
    return [label, name, h, s["n"], pc(s["mean"]), pc(s["med"]), pp(s["win"]), pc(s["worst"]), pc(p["med"]), f"{pc(p['lo'])} to {pc(p['hi'])}",
            f"{p['pct']:.0f}", pc(s["mean"] - COST) if trade else "-", f"{pc(p['umed'])} / {pp(p['uwin'])}", "no statistical power" if s["n"] <= 3 else ""]
def cell(name, h, i):
    v = ser[(name, h)][i]
    return pc(v) if COMPLETE[h][i] else f"{pc(v)} (INCOMPLETE, {n-1-i}d)"
def pathdd(p): return (p / np.maximum.accumulate(p) - 1).min()
def mdd(name, i, h):
    e = min(i + h, n - 1)
    if name == "KSE": return pathdd(K[i:e + 1] / K[i])
    m = LIQ[i]; return pathdd((CC[i:e + 1][:, m] / CC[i][m]).mean(1))

# ---------------------------------------------------------------- macro tables
dec = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"]).sort_values("date").reset_index(drop=True)
dec["prev_rate"] = dec.rate - dec.change_bp / 100
mv = dec[dec.decision.isin(["cut", "hike"])].copy()
def tpos(d):
    d = pd.Timestamp(d)
    return int(cal.searchsorted(d)) if d >= CAL0 else -int(np.busday_count(d.date(), CAL0.date()))
cyc, clu, c0, k0, lastdir, lastpos = [], [], 0, 0, None, None
for r in mv.itertuples():
    if r.decision != lastdir: c0 += 1; k0 += 1
    elif tpos(r.date) - lastpos > 120: k0 += 1
    cyc.append(c0); clu.append(k0); lastdir, lastpos = r.decision, tpos(r.date)
mv["cycle"], mv["cluster"] = cyc, clu
mv["first_cycle"] = mv.cycle != mv.cycle.shift(); mv["first_cluster"] = mv.cluster != mv.cluster.shift()
mv["oos"] = mv.date < CAL0
mv["i0"] = [cal.searchsorted(d, "right") for d in mv.date]

cp = pd.read_csv(ROOT / "data/macro/cpi.csv"); cp["m"] = pd.PeriodIndex(cp.month, freq="M"); cp = cp.set_index("m")
cp["raw"] = cp.yoy_pbs_release.fillna(cp.yoy); cp["src"] = np.where(cp.yoy_pbs_release.notna(), "pbs", "seed")
cp["val"] = cp.raw.where(cp.index != pd.Period("2026-09"))      # 2026-09 unverified: out of any historical signal
cp["rel"] = [(m + 1).to_timestamp() + pd.Timedelta(days=4) for m in cp.index]   # 5th of month m+1
cp["d3"] = (cp.val - cp.val.shift(3)).round(6)
tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"])
def cpi_known(d):
    x = cp[cp.rel < pd.Timestamp(d)].dropna(subset=["val"]); return x.iloc[-1] if len(x) else None
def y6_before(d):
    x = tb[(tb.date < pd.Timestamp(d)) & tb.y6m.notna()]; return x.iloc[-1] if len(x) else None
first = dec.iloc[0]
def prevailing(d):
    j = int(dec.date.searchsorted(d)) - 1
    return dec.rate.iloc[j] if j >= 0 else first.rate - first.change_bp / 100
tb["pol"] = tb.date.map(prevailing); tb["spr"] = tb.y6m - tb.pol

# ================================================================ 0. DATA
say("# rate_cycle_episodes raw output (generated by scripts/tests/rate_cycle_episodes.py)\n")
say("## 0. DATA AND SETUP")
say(f"KSE100 data/macro/kse100.csv: {n} rows {CAL0.date()} to {cal[-1].date()}. Trading calendar = these dates. Last close {K[-1]:.2f}.")
say("KSE100 type: PSX KSE-100 is a free-float market-cap PRICE index (capital gains only, no dividends); the file has OHLCV only and no dividend column. Treated as a price index, no dividends added (lesson 19). [type from PSX index methodology, not verifiable inside the file]")
say(f"Price panel: prices.load_panel() {close.shape[0]} dates x {S} symbols. Liquid universe: trailing 60 sessions strictly before t0, median traded value > Rs5m, 40+ obs (vector mask checked equal to prices.liquid_universe on 4 dates).")
say(f"Flag matrices: suspected log rows {len(sus)} ({P.SUSPECTS.name}), candidate-bonus day count {int(Fc.sum())}, provisional actions {len(acts)} (bonus/split {int(acts.type.isin(['bonus','split']).sum())}, cash {int((acts.type=='cash').sum())}).")
say("Flag B = suspected log OR candidate bonus (-8% to -10.5%, vol ratio<=3, price>Rs10) OR provisional bonus/split ex-date inside the window. Flag A = B plus provisional CASH dividend ex-dates (spec-literal; flags most payers). EWX = EW excluding flag-B names; EWA = EW with method='adjusted', actions=provisional_actions() (TOTAL return incl. cash dividends, so not like-for-like with price-only KSE100); EWAX = EWA excluding flag-B names.")
say(SURV)
say(f"Cost: {COST*100:.1f}% round trip subtracted from every trade-framed row (net = gross - 0.5%). Placebo: {NDRAW} draws of k dates with replacement, fixed seed 17102026, t0 from {cal[1].date()}, complete windows only; EW placebos also need >=10 basket names (EWX/EWAX >=5).")
say("Entry t0 = close of the first trading day strictly after the announcement date. Return = close[t0+h]/close[t0]-1. Windows past 2026-10-16 are shown INCOMPLETE with the return to date and are never used in statistics.")
for h in (20, 60, 120, 250):
    for nm in ("KSE", "EW"):
        x = ser[(nm, h)][valid(nm, h)]
        say(f"placebo date pool {nm} h={h}: {len(x)} dates ({cal[valid(nm,h)[0]].date()} to {cal[valid(nm,h)[-1]].date()}), unconditional single-date median {pc(np.median(x))}, mean {pc(x.mean())}, win {pp((x>0).mean())}")
say("\n### MPC moves: cycle and cluster IDs (cycle = run of same-direction moves; cluster = same direction with no gap > 120 trading days)")
table(["date", "decision", "bp", "rate prev->new", "cycle", "cluster", "first of cycle", "first of cluster", "in sample?", "note"],
      [[r.date.date(), r.decision, r.change_bp, f"{r.prev_rate}->{r.rate}", f"cyc{r.cycle}", f"cl{r.cluster}", r.first_cycle, r.first_cluster,
        "OUT OF SAMPLE (not computable: before 2016-10-17 index start)" if r.oos else "yes",
        "approximate date flagged in source" if r.date == pd.Timestamp("2018-01-29") else ""] for r in mv.itertuples()])
ins = mv[~mv.oos]
cutins, hikeins = ins[ins.decision == "cut"], ins[ins.decision == "hike"]
say(f"In sample cuts: {len(cutins)}; cut cycles: {int(cutins.first_cycle.sum())} {[str(d.date()) for d in cutins[cutins.first_cycle].date]}; cut clusters: {cutins.cluster.nunique()} {[str(d.date()) for d in cutins[cutins.first_cluster].date]}")
say(f"In sample hikes: {len(hikeins)}; hike cycles: {int(hikeins.first_cycle.sum())} {[str(d.date()) for d in hikeins[hikeins.first_cycle].date]}; hike clusters: {hikeins.cluster.nunique()} {[str(d.date()) for d in hikeins[hikeins.first_cluster].date]}")
say(f"Out of sample, not computable: cuts {[str(d.date()) for d in mv[mv.oos & (mv.decision=='cut')].date]} (2015 cycle and 2016-05-21 predate the index; NOT measured from 2016-10-17).")
say("Liquid names at t0 of cluster-first moves: " + ", ".join(f"{r.date.date()}={int(LIQ[r.i0].sum())}" for r in ins[ins.first_cluster].itertuples()) + f"; range over all dates after day 60: {int(LIQ.sum(1)[60:].min())}-{int(LIQ.sum(1).max())}")

# ---------------------------------------------------------------- event frame
E = ins[ins.i0 < n].copy()
E["ia"] = E.i0 - 1
E["react"] = K[E.i0] / K[E.ia] - 1
E["drift"] = K[E.ia] / K[E.i0 - 20] - 1
out_, last_ = [], {}
for r in E.itertuples():
    out_.append(r.decision in last_ and r.i0 < last_[r.decision] + 120); last_[r.decision] = r.i0
E["overlap"] = out_
E["ex120"] = [mdd("KSE", i, 120) for i in E.i0]
E["ew120"] = [mdd("EW", i, 120) for i in E.i0]

def event_tables(sub, title):
    say(f"\n### {title}: identification and context (descriptive columns are not tradable)")
    rows = []
    for r in sub.itertuples():
        c_ = cpi_known(cal[r.i0]); y_ = y6_before(cal[r.i0])
        rows.append([r.date.date(), r.change_bp, f"cyc{r.cycle}", f"cl{r.cluster}", f"{r.prev_rate}->{r.rate}", f"{c_.val:.2f} ({c_.name}, {c_.src})", f"{y_.y6m:.2f} ({y_.date.date()})",
                     pc(r.react), pc(r.drift), "yes" if r.overlap else "no", cal[r.i0].date()])
    table(["date", "bp", "cycle", "cluster", "rate", "last CPI yoy known at t0", "last 6M T-bill before t0", "reaction day (ann close->t0)", "pre-event drift (t0-20 -> ann close)", "120d window overlaps prior same-direction move", "t0"], rows)
    say(f"{title}: returns from t0 close (gross; net = gross - 0.5% shown for 120d). EW = EW liquid buy-and-hold basket; EWX excludes flag-B names; gap = EW120 - KSE120. {SURV}")
    rows = []
    for r in sub.itertuples():
        i = r.i0
        rows.append([r.date.date()] + [cell("KSE", h, i) for h in (20, 60, 120)] + [cell("EW", h, i) for h in (20, 60, 120)] + [cell("EWX", 120, i),
                     pc(ser[("EW", 120)][i] - ser[("KSE", 120)][i]), pc(r.ex120), pc(r.ew120), pc(ser[("KSE", 120)][i] - COST), pc(ser[("EW", 120)][i] - COST),
                     f"{int(cnt[('EW',120)][i])}/{int(FLB[120][i][LIQ[i]].sum())}/{int(FLA[120][i][LIQ[i]].sum())}"])
    table(["date", "KSE 20", "KSE 60", "KSE 120", "EW 20", "EW 60", "EW 120", "EWX 120", "EW-KSE gap 120", "KSE max DD 120", "EW max DD 120", "KSE120 net", "EW120 net", "EW names/flagB/flagA (120d)"], rows)

# ================================================================ H1
say("\n## H1: after a cut, the market rises (20/60/120)")
C = E[E.decision == "cut"]
event_tables(C, "H1 Table A, every in-sample cut")
fc = C[C.first_cluster]
say(f"\n### H1 headline: first cut of each cluster (effective n = clusters = {len(fc)}); no statistical power (k<=3)")
table(HEAD, [hrow("cluster-first cuts", nm, h, fc.i0) for nm in ("KSE", "EW", "EWX", "EWA") for h in (20, 60, 120)])
say("Intra-window max drawdown (peak-to-trough from t0 over h days) of cluster-first cuts:")
table(["h", "KSE worst DD", "EW worst DD", "KSE mean DD", "EW mean DD"],
      [[h, pc(min(mdd("KSE", i, h) for i in fc.i0)), pc(min(mdd("EW", i, h) for i in fc.i0)), pc(np.mean([mdd("KSE", i, h) for i in fc.i0])), pc(np.mean([mdd("EW", i, h) for i in fc.i0]))] for h in (20, 60, 120)])
say("EW minus KSE100 gap, cluster-first cuts (survivorship-flattered):")
table(["cut", "h", "KSE", "EW", "EW-KSE"], [[r.date.date(), h, pc(ser[("KSE", h)][r.i0]), pc(ser[("EW", h)][r.i0]), pc(ser[("EW", h)][r.i0] - ser[("KSE", h)][r.i0])] for r in fc.itertuples() for h in (20, 60, 120)])
say("### H1 secondary: greedy non-overlapping cuts (keep a cut only if t0 >= h days after the last kept t0, per h)")
rows = []
for h in (20, 60, 120):
    kept, last = [], -10**9
    for i in C.i0:
        if i >= last + h: kept.append(i); last = i
    say(f"h={h}: kept {[str(cal[i].date()) for i in kept]}")
    for nm in ("KSE", "EW"): rows.append(hrow(f"greedy h={h}", nm, h, kept))
table(HEAD, rows)
say("### H1 pooled (OVERLAPPING, n_eff = 3, not a headline)")
table(HEAD, [hrow("pooled 13 cuts, overlapping, n_eff=3", nm, h, C.i0) for nm in ("KSE", "EW") for h in (20, 60, 120)])

# ================================================================ H2 / H3
def first_vs_later(sub, title, tag):
    say(f"\n### {title}")
    rows = []
    for cy in sub.cycle.unique():
        g = sub[sub.cycle == cy]; f = g.iloc[0]; later = g.iloc[1:]
        for nm in ("KSE", "EW"):
            for h in (60, 120):
                fv = ser[(nm, h)][f.i0]; allv = [ser[(nm, h)][i] for i in g.i0 if COMPLETE[h][i]]; lv = [ser[(nm, h)][i] for i in later.i0 if COMPLETE[h][i]]
                if not COMPLETE[h][f.i0]:
                    rows.append([f"cyc{cy}", f.date.date(), nm, h, f"{pc(fv)} INCOMPLETE ({n-1-f.i0}d)", "-", "-", "-"]); continue
                rows.append([f"cyc{cy}", f.date.date(), nm, h, pc(fv), f"{pc(np.median(lv)) if lv else 'n/a'} (n later complete={len(lv)} of {len(later)})",
                             f"{1+sum(x > fv for x in allv)} of {len(allv)}", pc(fv - np.median(lv)) if lv else "n/a"])
    table(["cycle", "first move", "series", "h", "first move return", "median of later moves in cycle", "rank of first (1=best)", "first minus later median"], rows)
    say(f"{tag}: anecdote, {sub.cycle.nunique()} cases, no statistical power.")
    rows = []
    for cy in sub.cycle.unique():
        f = sub[sub.cycle == cy].iloc[0]; e = min(f.i0 + 120, n - 1); path = K[f.i0:e + 1] / K[f.i0] - 1
        rows.append([f"cyc{cy}", f.date.date(), pc(path.min()), cal[f.i0 + int(path.argmin())].date(), pc(mdd("KSE", f.i0, 120)), pc(mdd("EW", f.i0, 120)), "yes" if e == f.i0 + 120 else f"INCOMPLETE ({e-f.i0}d)"])
    table(["cycle", "first move", "KSE lowest point vs t0 within 120d", "date of low", "KSE max DD 120", "EW max DD 120", "120d complete"], rows)
    return sub.groupby("cycle").head(1)
say("\n## H2: the first cut of a cycle is strongest")
fcy = first_vs_later(C, "H2: first cut vs later cuts in the same cycle (cycle = until the next hike)", "H2")
say("H2 first cuts of cycles vs placebo (k=2):")
table(HEAD, [hrow("first cut of each cut cycle", nm, h, fcy.i0) for nm in ("KSE", "EW") for h in (20, 60, 120)])
say("2020-03-17 note: mid-COVID crash; see 'KSE lowest point vs t0' above for the continued fall after t0.")

H = E[E.decision == "hike"]
hf = H[H.first_cluster]
say("\n## H3: the first hike is weak")
first_vs_later(H, "H3: first hike vs later hikes in the same cycle", "H3")
say("H3 individual first hikes (cluster-first, gross; 2026-04-27 120d INCOMPLETE shown with return to date):")
table(["first hike", "cycle", "KSE 20", "KSE 60", "KSE 120", "EW 20", "EW 60", "EW 120", "reaction", "pre-drift"],
      [[r.date.date(), f"cyc{r.cycle}"] + [cell("KSE", h, r.i0) for h in (20, 60, 120)] + [cell("EW", h, r.i0) for h in (20, 60, 120)] + [pc(r.react), pc(r.drift)] for r in hf.itertuples()])
rows = []
for nm in ("KSE", "EW"):
    for h in (20, 60, 120):
        v = [ser[(nm, h)][i] for i in hf.i0 if COMPLETE[h][i]]
        rows.append([nm, h, len(v), pc(np.median(v))])
table(["series", "h", "n complete first hikes", "median of the complete ones"], rows)
table(HEAD, [hrow("first hikes (cluster-first)", nm, h, hf.i0) for nm in ("KSE", "EW", "EWX") for h in (20, 60, 120)])
say("2018-01-29 approximate date: t0 shifted by -3..+3 trading days around the base t0, range of returns:")
b = hf[hf.date == pd.Timestamp("2018-01-29")].i0.iloc[0]; rows = []
for nm in ("KSE", "EW"):
    for h in (20, 60, 120):
        v = [ser[(nm, h)][b + o] for o in range(-3, 4)]
        rows.append([nm, h, pc(ser[(nm, h)][b]), pc(min(v)), pc(max(v)), ", ".join(pc(x) for x in v)])
table(["series", "h", "base t0", "min of shifts", "max of shifts", "offsets -3..+3"], rows)
say("Hike rows are descriptive (no hike trade is framed). Full hike table:")
event_tables(H, "H3 Table, every in-sample hike")

# ================================================================ P2 holds
say("\n## P2: returns after MPC holds (in sample, same windows, t0 = first trading day after the announcement)")
holds = dec[(dec.decision == "hold") & (dec.date >= CAL0)].copy(); holds["i0"] = [cal.searchsorted(d, "right") for d in holds.date]; holds = holds[holds.i0 < n]
rows = []
for nm in ("KSE", "EW"):
    for h in (20, 60, 120):
        s = stats([ser[(nm, h)][i] for i in holds.i0 if COMPLETE[h][i]])
        rows.append([nm, h, s["n"], pc(s["mean"]), pc(s["med"]), pp(s["win"]), pc(s["worst"]), "holds overlap at 60/120d (MPCs 6-8 weeks apart)"])
table(["series", "h", "n holds", "mean", "median", "win", "worst", "note"], rows)
hr = K[holds.i0.values] / K[holds.i0.values - 1] - 1
say(f"Holds: reaction day (ann close -> t0) mean {pc(np.mean(hr))}, median {pc(np.median(hr))}; all-day KSE daily median {pc(np.median(K[1:]/K[:-1]-1))}")
say(f"Moves (cuts+hikes, in sample): reaction mean {pc(E.react.mean())}, median {pc(E.react.median())}; cuts median {pc(C.react.median())}, hikes median {pc(H.react.median())}")

# ================================================================ H4
say("\n## H4: CPI fall of 1pt+ over 3 months leads to +44% over the next 12 months (and mirror: CPI rise)")
say("Signal at month m: yoy(m) - yoy(m-3) <= -1.0 (mirror >= +1.0). yoy = yoy_pbs_release where present else seed yoy (source printed). 2026-09 (10.3) excluded as unverified. Formation t0 = first trading day after the 5th of month m+1. VINTAGE CAVEAT: series is rebased to 2015-16 retroactively (PBS rebased in 2020) so pre-2020 values are not the real-time vintage; not fixed.")
def form(m):
    d5 = (m + 1).to_timestamp() + pd.Timedelta(days=4); return d5, int(cal.searchsorted(d5, "right"))
vform = {m: i for m, (d5, i) in ((m, form(m)) for m in cp.index) if d5 >= CAL0 and i < n}
def cpi_study(sign, label):
    ok = cp.index[(cp.d3 * sign >= 1.0 - 1e-9)]
    runs = []
    for m in ok:
        if runs and runs[-1][-1] + 1 == m: runs[-1].append(m)
        else: runs.append([m])
    say(f"\n### H4 {label}: signal months {len(ok)} in {len(runs)} runs (usable CPI 2015-04 to 2026-08); run lengths {[len(r) for r in runs]}")
    rows, idx = [], []
    for r in runs:
        m = r[0]; i = form(m)[1]; c_ = cp.loc[m]
        if m not in vform:
            rows.append([m, len(r), f"{c_.val:.2f}", f"{c_.d3:+.2f}", c_.src, "-", "not computable: formation date before 2016-10-18 (pre-sample run)", "", "", ""]); continue
        idx.append(i)
        rows.append([m, len(r), f"{c_.val:.2f}", f"{c_.d3:+.2f}", c_.src, cal[i].date(), cell("KSE", 120, i), cell("KSE", 250, i), cell("EW", 120, i), cell("EW", 250, i)])
    table(["start month", "length", "yoy at start", "3m change", "yoy source", "t0 (formation)", "KSE 120", "KSE 250", "EW 120", "EW 250"], rows)
    say(f"runs measurable after Oct 2016: {len(idx)} of {len(runs)}. Incomplete windows excluded from stats. {SURV}")
    allm = [m for r in runs for m in r]; bigr = max(runs, key=len)
    meas = [m for m in allm if m in vform]
    say(f"Largest run: {bigr[0]} to {bigr[-1]}, {len(bigr)} of {len(allm)} signal months = {len(bigr)/len(allm)*100:.0f}%. Measurable signal months (formation >= 2016-10-18): {len(meas)}; largest run supplies {len([m for m in bigr if m in vform])} of them")
    rows = []
    for nm in ("KSE", "EW"):
        for h in (120, 250):
            vi = np.array(sorted(i for i in vform.values() if COMPLETE[h][i] and (nm == "KSE" or cnt[(nm, h)][i] >= MINC[nm])))
            rows.append(hrow(f"{label} runs (one obs per run)", nm, h, idx, vidx=vi))
    table(HEAD, rows)
    rows = []
    for nm in ("KSE", "EW"):
        for h in (120, 250):
            s = stats([ser[(nm, h)][vform[m]] for m in meas if COMPLETE[h][vform[m]]])
            rows.append([nm, h, "OVERLAPPING all signal months", s["n"] if s else 0, pc(s["mean"]) if s else "n/a", pc(s["med"]) if s else "n/a", pp(s["win"]) if s else "n/a", pc(s["worst"]) if s else "n/a"])
    table(["series", "h", "set", "n months", "mean", "median", "win", "worst"], rows)
    v = [ser[("KSE", 250)][i] for i in idx if COMPLETE[250][i]]; ve = [ser[("EW", 250)][i] for i in idx if COMPLETE[250][i]]
    say(f"{label}: runs with 250d return >= +44%: KSE {sum(x>=0.44 for x in v)} of {len(v)}; EW {sum(x>=0.44 for x in ve)} of {len(ve)}")
cpi_study(-1, "CPI FALL")
cpi_study(+1, "CPI RISE (mirror)")

# ================================================================ H5
say("\n## H5: the market anticipates cuts through T-bills (6M cut-off yield vs prevailing policy rate)")
say(f"Prevailing rate = rate of the latest MPC announcement strictly before the auction. Auctions before 2015-01-31 use rate - change = {first.rate - first.change_bp/100} (derived from the first row; unverified). Auctions {len(tb)}, with blank y6m {int(tb.y6m.isna().sum())}.")
nb = tb[tb.y6m.notna()].reset_index(drop=True)
nb["base"] = nb.spr < 0; nb["b50"] = nb.spr <= -0.5; nb["b100"] = nb.spr <= -1.0; nb["two"] = nb.base & nb.base.shift(1, fill_value=False)
VAR = {"primary y6m<policy": "base", "50bp below": "b50", "100bp below": "b100", "2 consecutive auctions below": "two"}
cuts_all = dec[dec.decision == "cut"].date
def cut_within(a, b): return bool(((cuts_all > a) & (cuts_all <= b)).any())
say("Fixed in advance: primary threshold 0bp; sensitivities 50bp, 100bp, 2 consecutive auctions. No others.")
say("2015 cut cycle: not computable (first cut 2015-01-31 has no preceding hike cycle in the data and no earlier T-bill history; KSE100 also starts 2016-10-17).")
say("\n### H5 per cut cycle (first cut of cycle, in sample): signal = first auction after the last hike of the preceding hike cycle (and before the cut) that fires")
rows = []
for r in C[C.first_cycle].itertuples():
    lh = dec[(dec.decision == "hike") & (dec.date < r.date)].date.max()
    for vn, vc in VAR.items():
        sel = nb[(nb.date > lh) & (nb.date < r.date) & nb[vc]]
        if sel.empty: rows.append([r.date.date(), vn, lh.date(), "not fired before the cut"] + [""] * 7); continue
        s = sel.iloc[0]; N = (r.date - s.date).days / 7
        ie_ = int(cal.searchsorted(s.date, "right")); m1 = K[r.i0] / K[ie_] - 1 if (s.date >= CAL0 and ie_ < r.i0) else float("nan")
        lo = s.date - pd.Timedelta(weeks=26)
        if lo < CAL0: m2 = ["not computable: window starts before index data"] * 3
        else:
            w = kse[(kse.index >= lo) & (kse.index <= r.date)]; tr = w.idxmin()
            m2 = [tr.date(), f"{(s.date-tr).days/7:+.1f}", f"{(r.date-tr).days/7:+.1f}"]
        rows.append([r.date.date(), vn, lh.date(), s.date.date(), f"{s.y6m:.2f} vs {s.pol:.2f}", f"{N:.1f}", pc(m1), pc(m1 - COST)] + m2)
table(["first cut", "variant", "last hike before", "signal auction", "y6m vs policy", "N weeks to cut", "M1 KSE gross (close after signal -> t0 of cut)", "M1 net", "M2 trough date (HINDSIGHT)", "weeks trough->signal", "weeks trough->cut"], rows)
say("M2 uses hindsight (the minimum of KSE100 between 26 weeks before the signal and the cut); descriptive only, never a rule.")
say("Episode containing the last auction before each cluster-first cut (descriptive): start of the continuous firing run, N weeks from that start to the cut")
rows = []
for r in mv[(mv.decision == "cut") & mv.first_cluster].itertuples():
    pre = nb[nb.date < r.date]
    for vn, vc in VAR.items():
        j = pre.index[-1]
        if not nb.loc[j, vc]: rows.append([r.date.date(), "OOS(index)" if r.oos else "in", vn, "not firing at last auction before the cut", nb.loc[j, "date"].date(), f"{nb.loc[j,'spr']:+.2f}", ""]); continue
        s = j
        while s - 1 >= 0 and nb.loc[s - 1, vc]: s -= 1
        rows.append([r.date.date(), "OOS(index)" if r.oos else "in", vn, nb.loc[s, "date"].date(), nb.loc[j, "date"].date(), f"{nb.loc[j,'spr']:+.2f}", f"{(r.date-nb.loc[s,'date']).days/7:.1f}"])
table(["cluster-first cut", "sample", "variant", "episode start", "last auction before cut", "y6m-policy at that auction (pp)", "N weeks from episode start"], rows)
say("### H5 false positives (2015-2026, all auctions): episode = maximal run of consecutive firing non-blank auctions; hit if an MPC cut falls in (episode start, episode end + 26 weeks]")
rows = []
for vn, vc in VAR.items():
    f = nb[nb[vc]]; grp = (nb[vc] != nb[vc].shift()).cumsum()
    eps = [g for _, g in nb[nb[vc]].groupby(grp[nb[vc]])]
    LASTD = tb.date.iloc[-1]
    cens = lambda g: g.date.iloc[-1] + pd.Timedelta(weeks=26) > LASTD     # 26w window not yet over: unresolved, not a settled false positive
    fp = [g for g in eps if not cut_within(g.date.iloc[0], g.date.iloc[-1] + pd.Timedelta(weeks=26))]
    fpr, fpu = [g for g in fp if not cens(g)], [g for g in fp if cens(g)]
    fpa = [d for d in f.date if not cut_within(d, d + pd.Timedelta(weeks=26))]
    fpa_u = sum(d + pd.Timedelta(weeks=26) > LASTD for d in fpa)
    rows.append([vn, len(nb), len(f), len(eps), len(eps) - len(fp), len(fpr), len(fpu), len(fpa) - fpa_u, fpa_u, f"{(len(f)-len(fpa))/max(len(f),1)*100:.0f}% (unresolved counted as miss)"])
    say(f"False-positive episodes, {vn}: " + ("; ".join(f"{g.date.iloc[0].date()} to {g.date.iloc[-1].date()} ({len(g)} auctions, min spread {g.spr.min():+.2f}pp){' UNRESOLVED: 26w window runs past '+str(LASTD.date()) if cens(g) else ''}" for g in fp) or "none"))
table(["variant", "non-blank auctions", "firing auctions", "episodes", "episodes with a cut within 26w", "FALSE-POSITIVE episodes (settled)", "FP episodes unresolved (window past last auction)", "FP firing auctions (settled)", "FP firing auctions unresolved", "auction-level hit rate"], rows)
say("### H5 mirror: y6m ABOVE prevailing rate ahead of first hikes (N only)")
rows = []
for r in H[H.first_cycle].itertuples():
    lc = dec[(dec.decision == "cut") & (dec.date < r.date)].date.max()
    sel = nb[(nb.date > lc) & (nb.date < r.date) & (nb.spr > 0)]
    j = nb[nb.date < r.date].index[-1]; s = j
    while s - 1 >= 0 and nb.loc[s - 1, "spr"] > 0: s -= 1
    up = nb.loc[j, "spr"] > 0
    rows.append([r.date.date(), lc.date(), sel.iloc[0].date.date() if len(sel) else "none", f"{(r.date-sel.iloc[0].date).days/7:.1f}" if len(sel) else "-",
                 f"{nb.loc[j,'spr']:+.2f}", nb.loc[s, "date"].date() if up else "not above at last auction", f"{(r.date-nb.loc[s,'date']).days/7:.1f}" if up else "-"])
table(["first hike", "last cut before", "first auction after with y6m>policy", "N weeks", "spread at last auction before hike", "start of continuous above-run", "N weeks from run start"], rows)
say("H5 caveats: 2 usable cut cycles and 3 first hikes; thresholds fixed beforehand; no statistical power.")

# ================================================================ H6
say("\n## H6: sector returns after a first cut (cut-cluster starts)")
sy = pd.read_csv(ROOT / "data/symbols.csv")
okmask = ~sy.isETF.astype(bool) & ~sy.isDebt.astype(bool) & (sy.sectorName != "BILLS AND BONDS")
sec_of = dict(zip(sy.symbol[okmask], sy.sectorName[okmask]))
sectors = sorted(set(sec_of[c] for c in cols if c in sec_of))
smask = {s: np.array([sec_of.get(c) == s for c in cols]) for s in sectors}
say(f"Sectors = PSX sectorName (current classification) from data/symbols.csv, excluding ETFs, debt and BILLS AND BONDS: {len(sectors)} sectors with a panel name. Panel names that are ETF/debt (outside sector baskets): {sum(1 for c in cols if c not in sec_of)}. Baskets contain only currently listed names (survivorship).")
SEC, SECX = {}, {}
for h in (60, 120):
    for s in sectors:
        SEC[(s, h)] = bask(R_c[h], LIQ & smask[s]); SECX[(s, h)] = bask(R_c[h], LIQ & smask[s] & ~FLB[h])
EXC = {}
for s in sectors:
    for h in (60, 120):
        r_, c_ = SEC[(s, h)]; EXC[(s, h)] = np.where(c_ >= 3, r_ - ser[("EW", h)], np.nan)
evs = [(pd.Timestamp(d), int(cal.searchsorted(pd.Timestamp(d), "right"))) for d in ("2020-03-17", "2024-06-10", "2025-12-15")]
sec_tab = {}
for d, i in evs:
    say(f"\n### H6 {d.date()} (t0 {cal[i].date()}): EW liquid basket 60d {pc(ser[('EW',60)][i])}, 120d {pc(ser[('EW',120)][i])} (n={int(cnt[('EW',120)][i])}); KSE100 60d {pc(ser[('KSE',60)][i])}, 120d {pc(ser[('KSE',120)][i])}. Excess = sector - EW; net = excess - 0.5%.")
    rows, small = [], []
    for s in sectors:
        m = LIQ[i] & smask[s]; nm_ = int(m.sum())
        if nm_ == 0: continue
        if nm_ < 3: small.append([s, nm_, "n<3, not a basket", ",".join(cols[j] for j in np.where(m)[0])] + [""] * 6); continue
        nf = int((m & FLB[120][i]).sum()); r60, r120 = SEC[(s, 60)][0][i], SEC[(s, 120)][0][i]
        x120 = SECX[(s, 120)]
        xv = (pc(x120[0][i] - ser[("EW", 120)][i]) + f" (n={int(x120[1][i])})") if x120[1][i] >= 3 else "n<3 after exclusion"
        e60, e120 = r60 - ser[("EW", 60)][i], r120 - ser[("EW", 120)][i]
        sec_tab[(d, s)] = (e60, e120)
        rows.append((e120, [s, nm_, f"{nf} flagged", pc(r60), pc(r120), pc(e60), pc(e60 - COST), pc(e120), pc(e120 - COST), xv]))
    rows.sort(key=lambda t: -t[0])
    table(["sector", "n names", "flag-B in 120d window", "60d gross", "120d gross", "60d excess", "60d excess net", "120d excess", "120d excess net", "120d excess ex-flag"], [t[1] for t in rows] + small)
    say("Top 3 by 120d excess: " + "; ".join(f"{t[1][0]} {pc(t[0])}" for t in rows[:3])); say("Bottom 3 by 120d excess: " + "; ".join(f"{t[1][0]} {pc(t[0])}" for t in rows[-3:]))
for a, b in ((0, 1), (1, 2), (0, 2)):
    for j, h in ((0, 60), (1, 120)):
        common = [s for s in sectors if (evs[a][0], s) in sec_tab and (evs[b][0], s) in sec_tab]
        rho = spearmanr([sec_tab[(evs[a][0], s)][j] for s in common], [sec_tab[(evs[b][0], s)][j] for s in common])[0]
        say(f"Spearman persistence of sector {h}d excess, {evs[a][0].date()} vs {evs[b][0].date()}: rho {rho:+.2f} over {len(common)} sectors (descriptive, single number){'  <- the 2020 vs 2024 pair asked for' if (a, b) == (0, 1) else ''}")
say("\n### H6 per-sector placebo: observed = mean sector excess across the 3 cut-cluster episodes where the basket exists (k<=3, no statistical power); placebo = random dates with the basket rebuilt each date (needs >=3 names)")
rows = []
for s in sectors:
    for h in (60, 120):
        obs = [EXC[(s, h)][i] for _, i in evs if EXC[(s, h)][i] == EXC[(s, h)][i]]
        if not obs: continue
        v = IDX[(EXC[(s, h)] == EXC[(s, h)]) & COMPLETE[h] & (IDX >= 1) & (cnt[("EW", h)] >= 10)]
        if len(v) < 50: rows.append([s, h, len(obs), pc(np.mean(obs)), "not computable: <50 valid placebo dates", "", "", "", ""]); continue
        p = plc(EXC[(s, h)][v], len(obs), np.mean(obs))
        rows.append([s, h, len(obs), pc(np.mean(obs)), pc(np.mean(obs) - COST), pc(p["med"]), f"{pc(p['lo'])} to {pc(p['hi'])}", f"{p['pct']:.0f}", pc(p["umed"])])
table(["sector", "h", "episodes with basket", "obs mean excess", "net", "placebo median k-mean", "placebo 5-95%", "obs pctile", "uncond single-date median excess"], rows)
say("\n### H6 Islamic banks case study (FIXED LIST stated before running: MEBL, BIPL; symbols.csv has no other full-fledged Islamic bank). Not a sector. Stock-level: windows with a flagged day are marked FLAG.")
IB = ["MEBL", "BIPL"]; rows = []
for d, i in evs:
    for nm_ in IB:
        j = colix[nm_]; row = [d.date(), nm_, "liquid" if LIQ[i, j] else "NOT liquid at t0"]
        for h in (60, 120):
            fl = [str(cal[t].date()) for t in range(i + 1, min(i + h, n - 1) + 1) if FB[t, j]]
            row += [pc(R_c[h][i, j]) + (f" FLAG {fl}" if fl else ""), pc(R_c[h][i, j] - ser[("EW", h)][i])]
        rows.append(row)
table(["episode", "name", "liquidity", "60d", "60d excess vs EW", "120d", "120d excess vs EW"], rows)
ibm = LIQ[:, [colix[x] for x in IB]].all(1)
for h in (60, 120):
    r_ = np.where(ibm, R_c[h][:, [colix[x] for x in IB]].mean(1), np.nan) - ser[("EW", h)]
    obs = [r_[i] for _, i in evs if r_[i] == r_[i]]
    v = IDX[(r_ == r_) & COMPLETE[h] & (IDX >= 1) & (cnt[("EW", h)] >= 10)]
    p = plc(r_[v], len(obs), np.mean(obs)) if obs and len(v) > 50 else None
    say(f"Islamic 2-bank basket {h}d excess vs EW: episodes with both liquid {len(obs)}; values {[pc(x) for x in obs]}; mean {pc(np.mean(obs)) if obs else 'n/a'}; net {pc(np.mean(obs)-COST) if obs else 'n/a'}; placebo {('median '+pc(p['med'])+', 5-95 '+pc(p['lo'])+' to '+pc(p['hi'])+', obs pctile '+format(p['pct'],'.0f')+f', {p['nv']} dates') if p else 'not computable'}; no statistical power")
say("\n### Corporate-action handling: basket composition and sensitivity at the cluster-first cuts (120d)")
rows = []
for r in fc.itertuples():
    i = r.i0
    rows.append([r.date.date(), int(LIQ[i].sum()), int(FLB[120][i][LIQ[i]].sum()), int(FLA[120][i][LIQ[i]].sum()), pc(ser[("EW", 120)][i]), pc(ser[("EWX", 120)][i]), pc(ser[("EWA", 120)][i]), pc(ser[("EWAX", 120)][i]), pc(ser[("KSE", 120)][i])])
rows2 = []
for r in fc.itertuples():
    i = r.i0; e = min(i + 120, n - 1)
    rows2.append([r.date.date()] + [int((F[i + 1:e + 1].any(0) & LIQ[i]).sum()) for F in (Fs, Fc, Fb, Fcash)])
say("Flag components among the liquid names at t0 (names with at least one such day in the 120d window; a name can sit in several):")
table(["cut", "suspected-log days", "candidate-bonus days (loose rule, flags many ordinary -8..-10% days)", "provisional bonus/split ex-dates", "provisional cash-dividend ex-dates (flag A only)"], rows2)
table(["cut", "liquid names", "flag-B names", "flag-A names", "EW (crude)", "EWX (crude, ex flag B)", "EWA (adjusted, provisional actions, total return)", "EWAX (adjusted ex flag B)", "KSE100 price"], rows)
say("Baskets dilute but do not remove the bonus bias: one 10% bonus (about -9.1% fake loss) in an n-name basket costs 9.1/n pts, e.g. 1.8 pts in a 5-name basket. EW/EWX are price-only after crude zeroing; EWA adds cash dividends back (total return); lesson 19 respected (no extra yield added).")

# ================================================================ 5. CURRENT SETUP
say("\n## 5. CURRENT SETUP (computed from files)")
last = dec.iloc[-1]; lm = mv.iloc[-1]; la = tb.iloc[-1]
say(f"Latest policy rate {last.rate}% (decision {last.decision} on {last.date.date()}); last move: {lm.decision} {lm.change_bp}bp on {lm.date.date()}; rate unchanged since {lm.date.date()}.")
say(f"Latest 6M T-bill {la.y6m} on {la.date.date()} (3M {la.y3m}, 12M {la.y12m}); spread to policy {la.spr*100:+.0f}bp.")
nl = nb.iloc[-1]
say("H5 signal at latest auction: " + ", ".join(f"{vn}={'ON' if nl[vc] else 'OFF'}" for vn, vc in VAR.items()) + f". Auctions since the last move ({lm.date.date()}) that fired (primary): {[str(d.date()) for d in nb[(nb.date>lm.date)&nb.base].date]}")
say("CPI yoy (src; value): " + "; ".join(f"{m}={cp.loc[m,'raw']} ({cp.loc[m,'src']}{', UNVERIFIED' if m==pd.Period('2026-09') else ''})" for m in [pd.Period(x) for x in ("2026-05", "2026-06", "2026-07", "2026-08", "2026-09")]))
dj = cp.loc[pd.Period('2026-09'), 'raw'] - cp.loc[pd.Period('2026-06'), 'raw']
say(f"3-month change Jun->Sep 2026 (uses unverified Sep 10.3): {dj:+.2f} (trigger <= -1.0: {'MET' if dj <= -1 else 'NOT met'}). Last PBS-verified 3-month change May->Aug (rule value): {cp.loc[pd.Period('2026-08'),'val']-cp.loc[pd.Period('2026-05'),'val']:+.2f}.")
sd = cp.loc[pd.Period('2026-09'), 'yoy'] - cp.loc[pd.Period('2026-06'), 'yoy']
say(f"Seed-yoy-only values (2dp): 2026-06 {cp.loc[pd.Period('2026-06'),'yoy']}, 2026-07 {cp.loc[pd.Period('2026-07'),'yoy']}, 2026-08 {cp.loc[pd.Period('2026-08'),'yoy']}, 2026-09 {cp.loc[pd.Period('2026-09'),'yoy']}; Jun->Sep change on seed yoy {sd:+.2f} (also not <= -1.0).")
say(f"Real rate = policy - latest CPI yoy: verified Aug ({cp.loc[pd.Period('2026-08'),'val']}): {last.rate-cp.loc[pd.Period('2026-08'),'val']:+.2f}pp; with unverified Sep ({cp.loc[pd.Period('2026-09'),'raw']}): {last.rate-cp.loc[pd.Period('2026-09'),'raw']:+.2f}pp.")
cal_ = pd.read_csv(ROOT / "catalysts/catalyst_calendar.csv", parse_dates=["date"])
nm = cal_[cal_.event.str.contains("SBP MPC", na=False) & (cal_.date > pd.Timestamp("2026-10-17"))].sort_values("date")
say(f"Next MPC per catalysts/catalyst_calendar.csv: {nm.date.iloc[0].date()} (then {[str(d.date()) for d in nm.date.drop_duplicates().iloc[1:3]]}).")
say("y6m minus prevailing policy at the last auction before each cluster-first cut (what the curve said before the cut):")
table(["cut", "last auction before", "y6m", "policy then", "spread pp"], [[r.date.date(), y6_before(r.date).date.date(), y6_before(r.date).y6m, prevailing(r.date), f"{y6_before(r.date).y6m-prevailing(r.date):+.2f}"] for r in mv[(mv.decision == 'cut') & mv.first_cluster].itertuples()])
say("Conditions that would mark the next first cut (stated in advance): (1) y6m below the prevailing policy rate at an auction; confirmation: 50bp below and 2 consecutive auctions below; (2) a CPI 3-month change <= -1.0 on a PBS-verified print. Conditional history, not a forecast: n = 2 usable cut cycles.")
say("Proposed frozen-prediction row (NOT appended; orchestrator decides). An existing row already freezes the policy-rate outcome for 2026-10-26 with a cut probability of 0.02, so this is a duplicate-risk.")
say('2026-10-17,Policy rate,SBP MPC decision: no cut,2026-10-26,"SBP does not cut at the 26 Oct 2026 MPC (hold or hike)",0.97,"6M T-bill 12.3989 on 14 Oct is +90bp above the 11.5 policy rate (H5 signal OFF); see the table above for y6m minus policy before the 2020 and 2024 first cuts; CPI 3m change on the last PBS-verified print is not <= -1.0. n=2 cut cycles: conditional history, not a forecast.",,,')

Path(ROOT / "tests/out").mkdir(exist_ok=True)
(ROOT / "tests/out/rate_cycle_episodes.txt").write_text("\n".join(OUT), encoding="utf-8")
