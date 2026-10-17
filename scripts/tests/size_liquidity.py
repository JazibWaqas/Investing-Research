"""Size/liquidity effect on PSX, 2017-2026. Run: .venv/Scripts/python.exe scripts/tests/size_liquidity.py
Prints and saves tests/out/size_liquidity.txt. Reuses scripts/prices.py. See tests/size_liquidity.md."""
import sys, io, re, glob
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
def pct(x): return f"{x:+.1%}"
def ann(cum, yrs): return (1 + cum) ** (1 / yrs) - 1

close, vol, tv = P.load_panel()
START, END = pd.Timestamp("2017-01-02"), close.index[-1]
YRS = (END - START).days / 365.25
ret = P.returns(close, "crude")
ret = ret[ret.index >= START]
med = P._med_tv(tv).reindex(ret.index)
liquid = med > 5e6
out(f"Panel {close.shape}, window {START.date()} to {END.date()} ({YRS:.2f} yrs). Liquid names per day, mean: {liquid.sum(axis=1).mean():.0f}")

def idx(name):
    return pd.read_csv(ROOT / "data/macro" / f"{name}.csv", index_col=0, parse_dates=True)["close"]
def idx_ret(name, a=START, b=END):
    s = idx(name); s = s[(s.index >= a) & (s.index <= b)]
    return s.iloc[-1] / s.iloc[0] - 1
out("\n== Index price returns")
for n in ["kse100", "kmi30", "kmiallshr"]:
    s = idx(n); a = max(START, s.index[0])
    c = idx_ret(n, a)
    out(f"{n:10s} {a.date()} to {END.date()}: {pct(c)}  ({pct(ann(c, (END-a).days/365.25))} a year)")

daily = ret.where(liquid).mean(axis=1).dropna()
daily_cum = (1 + daily).prod() - 1
out(f"\n== (b) rebalancing: daily-rebalanced EW liquid (crude): {pct(daily_cum)} ({pct(ann(daily_cum, YRS))} a yr); mean daily {daily.mean():.4%}, median {daily.median():.4%}")

month = ret.index.to_period("M")
first = pd.Series(ret.index, ret.index).groupby(month).first()
L = np.log1p(ret.clip(lower=-0.999))
mr = np.expm1(L.groupby(month).sum(min_count=1))   # month x name compounded return
cnt = ret.notna().groupby(month).sum()
mr = mr.where(cnt >= 1)
med_m = med.loc[first.values]; med_m.index = first.index   # trailing 60d median TV known on day 1
liq_m = med_m > 5e6
mon_ew = mr.where(liq_m).mean(axis=1).dropna()
mon_cum = (1 + mon_ew).prod() - 1
out(f"monthly-rebalanced EW liquid (buy-and-hold within month): {pct(mon_cum)} ({pct(ann(mon_cum, YRS))} a yr); n months {len(mon_ew)}")
bh_names = liq_m.iloc[0][liq_m.iloc[0]].index
cumn = np.expm1(L[bh_names].sum())
out(f"buy-and-hold EW of the {len(bh_names)} names liquid in Jan 2017 (no rebalance): mean cum {pct(cumn.mean())}, median name {pct(cumn.median())}")
ann_ew = []
for y in range(2017, 2027):
    ps = [p for p in mr.index if p.year == y]
    names = liq_m.loc[ps[0]]; names = names[names].index
    ann_ew.append(np.expm1(L.loc[L.index.year == y, names].sum()).mean())
a_cum = np.prod([1 + x for x in ann_ew]) - 1
out(f"annual-rebalanced EW (names liquid each Jan, held the year, no rebalance): {pct(a_cum)}")
sk = ret.where(liquid).stack().dropna()
out(f"liquid name-days {len(sk)}; mean daily name return {sk.mean():.4%}, median {sk.median():.4%}")
out(f"daily EW arithmetic mean {daily.mean():.4%} vs log mean {np.log1p(daily).mean():.4%}: drag {(daily.mean()-np.log1p(daily).mean())*252:.1%} a year")

out("\n== (d) corporate-action handling")
out("data/corporate_actions.csv exists:", P.ACTIONS.exists())
pctm, _, _, _, big = P._moves(close, vol)
pctm, big = pctm.reindex(ret.index), big.reindex(ret.index)
zero_mask = (ret == 0) & big
z = pctm.where(zero_mask).stack().dropna()
out(f"crude zeroed {len(z)} moves since 2017: {int((z>0).sum())} up, {int((z<0).sum())} down")
zl = pctm.where(zero_mask & liquid).stack().dropna()
out(f"  in liquid names: {len(zl)} zeroed, {int((zl>0).sum())} up")
raw_ew = pctm.where(liquid).mean(axis=1).dropna()
out(f"EW daily, NO fix at all (fake crashes left in): {pct((1+raw_ew).prod()-1)}")
upfix = ret.mask(zero_mask & (pctm > 0) & (pctm < 1), pctm)  # moves above +100% are splits, BML 16x on 2026-02-02
out(f"EW daily, crude but zeroed up-moves below +100% restored: {pct((1+upfix.where(liquid).mean(axis=1).dropna()).prod()-1)}")
try:
    acts = P.provisional_actions()
    acts = acts[acts.type.isin(["cash", "bonus", "split"])]
    ra = P.returns(close, "adjusted", actions=acts)
    ra = ra[ra.index >= START]
    d2 = ra.where(liquid).mean(axis=1).dropna()
    out(f"EW daily, PROVISIONAL total-return adjustment ({len(acts)} actions, unverified table; includes cash dividends): {pct((1+d2).prod()-1)}")
except Exception as e:
    out("provisional adjustment failed:", repr(e))

def buckets(q, universe_mask, rng=None):
    rows, per = {}, []
    for p in mr.index:
        u = universe_mask.loc[p]; names = u[u].index
        r = mr.loc[p, names].dropna()
        if len(r) < q * 3: continue
        key = med_m.loc[p, r.index] if rng is None else pd.Series(rng.random(len(r)), r.index)
        b = pd.qcut(key.rank(method="first"), q, labels=False)
        rows[p] = r.groupby(b).mean()
        per.append(pd.DataFrame({"p": p, "b": b, "r": r}))
    return pd.DataFrame(rows).T, pd.concat(per)
def summ(B, per, q):
    t = []
    for k in range(q):
        s = B[k]; pr = per[per.b == k].r
        c = (1 + s).prod() - 1
        t.append(dict(bucket=k + 1, months=len(s), mean_m=s.mean(), median_m=s.median(), win_m=(s > 0).mean(),
                      cum=c, ann=ann(c, len(s) / 12), n_namemonths=len(pr), name_median=pr.median(), name_win=(pr > 0).mean()))
    return pd.DataFrame(t).set_index("bucket")
def fmt(df):
    f = df.copy()
    for c in ["mean_m", "median_m", "win_m", "cum", "ann", "name_median", "name_win"]:
        f[c] = f[c].map(lambda x: f"{x:.1%}" if c in ("win_m", "name_win") else f"{x:+.1%}")
    return f.to_string()
out("\n== (c) buckets by trailing 60d median traded value (1 = least liquid, top = most), liquid universe (>Rs5m)")
res = {}
for q in (3, 5):
    B, per = buckets(q, liq_m)
    res[q] = (B, per)
    out(f"\n{q} buckets, liquid universe, months {len(B)}, mean names/month {len(per)/len(B):.0f}")
    out(fmt(summ(B, per, q)))
    spr = B[q - 1] - B[0]
    out(f"spread top-bottom monthly: mean {spr.mean():+.2%}, median {spr.median():+.2%}, t {spr.mean()/(spr.std()/np.sqrt(len(spr))):.2f}, months top>bottom {(spr>0).mean():.1%}, mean x12 {spr.mean()*12:+.1%}")
    rng = np.random.default_rng(0)
    ps = np.array([(lambda Bp: (Bp[q - 1] - Bp[0]).mean())(buckets(q, liq_m, rng)[0]) for _ in range(200)])
    out(f"placebo (200 random bucket draws): spread mean {ps.mean():+.3%}, sd {ps.std():.3%}, 95% band [{np.percentile(ps,2.5):+.3%}, {np.percentile(ps,97.5):+.3%}]; real {spr.mean():+.3%}, share of placebos at or below real {(ps<=spr.mean()).mean():.1%}")
wide = med_m > 1e6
Bw, perw = buckets(3, wide)
out(f"\n3 buckets, wider universe (>Rs1m median traded value), mean names/month {len(perw)/len(Bw):.0f}")
out(fmt(summ(Bw, perw, 3)))
sw = Bw[2] - Bw[0]; out(f"spread top-bottom monthly {sw.mean():+.2%}, t {sw.mean()/(sw.std()/np.sqrt(len(sw))):.2f}, months top>bottom {(sw>0).mean():.1%}")

B3 = res[3][0]
Y = B3.groupby(B3.index.year).apply(lambda d: (1 + d).prod() - 1)
Y["spread"] = Y[2] - Y[0]
Y["EW_all_liquid"] = mon_ew.groupby(mon_ew.index.year).apply(lambda d: (1 + d).prod() - 1)
Y["KSE100"] = [idx_ret("kse100", START if y == 2017 else pd.Timestamp(f"{y-1}-12-31"), min(END, pd.Timestamp(f"{y}-12-31"))) for y in Y.index]
Yw = Bw.groupby(Bw.index.year).apply(lambda d: (1 + d).prod() - 1)
Y["wide_spread"] = Yw[2] - Yw[0]
Y.columns = ["bottom", "middle", "top", "top-bottom", "EW all liquid", "KSE100", "wide top-bottom"]
out("\nYearly tercile returns (liquid universe, compounded monthly; 2026 to 16 Oct)")
out(Y.map(lambda x: f"{x:+.1%}").to_string())
nyr = len(Y)
out(f"top beat bottom in {(Y['top-bottom']>0).sum()} of {nyr} years; wide universe {(Y['wide top-bottom']>0).sum()} of {nyr}; top beat EW-all in {(Y['top']>Y['EW all liquid']).sum()} of {nyr}; KSE100 beat EW liquid in {(Y['KSE100']>Y['EW all liquid']).sum()} of {nyr}")
Yt = Y["top-bottom"]; out(f"mean yearly spread {Yt.mean():+.1%}, median {Yt.median():+.1%}; ex-2026 partial {Yt.iloc[:-1].mean():+.1%}")
out("annualised compounded: " + ", ".join(f"{n} {np.expm1(np.log1p(B3[k]).sum() / (len(B3)/12)):+.1%}" for k, n in enumerate(["bottom", "middle", "top"])))
out("cumulative since 2017: " + ", ".join(f"{n} {pct((1+B3[k]).prod()-1)}" for k, n in enumerate(["bottom", "middle", "top"])))

def members(prefix, d):
    fs = sorted(glob.glob(str(ROOT / "data/index_members" / f"{prefix}_*.csv")))
    ok = [(pd.Timestamp(re.search(r"(\d{4}-\d{2}(?:-\d{2})?)", Path(f).stem).group(1)), f) for f in fs]
    ok = [x for x in ok if x[0] <= d]
    if not ok: return None
    return [s for s in pd.read_csv(max(ok)[1]).symbol]
out("\n== (e) KSE100 concentration, members point-in-time from 2021-04-01")
K0 = pd.Timestamp("2021-04-01")
ms = [p for p in mr.index if first[p] >= K0]
ew_k, tvw, tvx, contrib, shares = {}, {}, {}, {}, []
for p in ms:
    names = [n for n in members("KSE100", first[p]) if n in mr.columns]
    r = mr.loc[p, names]; w = med_m.loc[p, names].where(r.notna()); r = r.dropna(); w = w.loc[r.index].fillna(0)
    ew_k[p] = r.mean(); tvw[p] = (r * w / w.sum()).sum()
    top = w.nlargest(10).index; r2, w2 = r.drop(top), w.drop(top)
    tvx[p] = (r2 * w2 / w2.sum()).sum()
    contrib[p] = (r[top] * w[top] / w.sum()).sum(); shares.append(w[top].sum() / w.sum())
cum = lambda d: (1 + pd.Series(d)).prod() - 1
out(f"KSE100 index price return {K0.date()} to {END.date()}: {pct(idx_ret('kse100', K0))}")
out(f"EW of KSE100 members (monthly rebal): {pct(cum(ew_k))}")
out(f"traded-value-weighted KSE100 members (proxy for cap weights, monthly): {pct(cum(tvw))}")
out(f"same, excluding the 10 largest by traded value each month: {pct(cum(tvx))}")
out(f"top-10 share of traded-value weight (mean) {np.mean(shares):.0%}; their monthly contributions sum to {sum(contrib.values()):+.1%} of {sum(tvw.values()):+.1%} total (simple sums)")
out("Caveat: real KSE100 weights are free-float market cap; the repo has no share counts, so traded value is a stand-in.")
lw = mon_ew[[p for p in mon_ew.index if first[p] >= K0]]
out(f"EW liquid (whole panel, monthly) over same window: {pct((1+lw).prod()-1)}")

out("\n== KMI30 members EW vs EW liquid KMI All Share (monthly rebal, point in time)")
def run(prefix, start, liquid_only):
    d, nn = {}, []
    for p in mr.index:
        if first[p] < start: continue
        names = members(prefix, first[p])
        if names is None: continue
        names = [n for n in names if n in mr.columns]
        if liquid_only: names = [n for n in names if liq_m.loc[p, n]]
        r = mr.loc[p, names].dropna(); d[p] = r.mean(); nn.append(len(r))
    return pd.Series(d), np.mean(nn)
for start in (pd.Timestamp("2020-07-13"), pd.Timestamp("2019-01-28")):
    sa, na = run("KMI_ALL_derived", start, True)
    sa_all, na_all = run("KMI_ALL_derived", start, False)
    ya = (END - start).days / 365.25
    out(f"from {start.date()}:")
    out(f"  EW KMI All members that are liquid ({na:.0f} names): {pct(cum(sa))} ({pct(ann(cum(sa), ya))} a yr)")
    out(f"  EW all KMI All members, no liquidity filter ({na_all:.0f} names): {pct(cum(sa_all))}; KMIALLSHR index {pct(idx_ret('kmiallshr', start))}")
    if start == pd.Timestamp("2020-07-13"):
        s30, n30 = run("KMI30", start, False)
        out(f"  EW KMI30 members ({n30:.0f} names): {pct(cum(s30))} ({pct(ann(cum(s30), ya))} a yr); KMI30 index {pct(idx_ret('kmi30', start))}")
        both = pd.concat([s30, sa], axis=1).dropna(); dd = both.iloc[:, 0] - both.iloc[:, 1]
        yy = both.groupby(both.index.year).apply(lambda d: (1 + d).prod() - 1)
        yy.columns = ["KMI30 EW", "KMIAll liquid EW"]; yy["diff"] = yy.iloc[:, 0] - yy.iloc[:, 1]
        out(yy.map(lambda x: f"{x:+.1%}").to_string())
        out(f"  KMI30 beat KMI-liquid in {(yy['diff']>0).sum()} of {len(yy)} years; monthly diff mean {dd.mean():+.2%}, t {dd.mean()/(dd.std()/np.sqrt(len(dd))):.2f}")

(ROOT / "tests/out/size_liquidity.txt").write_text(buf.getvalue(), encoding="utf-8")
