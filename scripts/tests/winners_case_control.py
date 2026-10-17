"""Big winners case-control: what did 100%-in-6-months names look like at the start, and could a screen see it?
See tests/winners_case_control.md. Run: .venv/Scripts/python.exe scripts/tests/winners_case_control.py
Raw output: tests/out/winners_case_control.txt (+ winners_case_control_events.csv, _features.csv).
"""
import re, sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from prices import load_panel, returns  # noqa: E402

LIQ, H, EV, CT, SLIP_TV = 5e6, 6, 1.0, 0.5, 20e6
RNG = np.random.default_rng(20261018)
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


# ============================================================ prices: survivors (adjusted TR) + delisted (crude)
close, vol, tv = load_panel()
adj = pd.read_parquet(ROOT / "data/panel_close_adj.parquet").reindex(index=close.index, columns=close.columns)
adjpr = pd.read_parquet(ROOT / "data/panel_close_adj_pricereturn.parquet").reindex(index=close.index, columns=close.columns)
dl = {}
for f in (ROOT / "data/prices_delisted").glob("*.csv"):
    if f.stem in close.columns:
        continue
    x = pd.read_csv(f, usecols=["date", "close", "volume"], parse_dates=["date"], index_col="date")
    x = x[~x.index.duplicated(keep="last")].sort_index()
    if len(x):
        dl[f.stem] = x
dc = pd.DataFrame({s: x.close for s, x in dl.items()}).reindex(close.index)
dv = pd.DataFrame({s: x.volume for s, x in dl.items()}).reindex(close.index)
inside = dv.notna().cummax() & dv[::-1].notna().cummax()[::-1]
dv = dv.where(~(inside & dv.isna()), 0.0)
ok = (dv > 0) & (dc > 0)
dc = dc.where(ok)
dup = []                                             # renamed symbols (CLOUD/CWSM = QTECH): same history under two codes
for col in dc.columns:
    ref = pd.concat([close, dc[[c for c in dc.columns if c < col]]], axis=1)
    both = ref.notna() & dc[[col]].notna().values
    same = (ref.values == dc[[col]].values) & both.values
    n = both.values.sum(0)
    if ((same.sum(0) >= 0.9 * n) & (n >= 100)).any():
        dup.append(col)
dc, dv = dc.drop(columns=dup), dv.drop(columns=dup)
dret = returns(dc, "crude", vol=dv)
dlev = (1 + dret.fillna(0)).cumprod().where(dc.notna())
dlev = dlev / dlev.ffill().iloc[-1] * dc.ffill().iloc[-1]          # scale so last level = last raw close
CL = pd.concat([close, dc], axis=1)
ADJ = pd.concat([adj, dlev], axis=1)
ADJPR = pd.concat([adjpr, dlev], axis=1)
TV = pd.concat([tv, (dc * dv).fillna(0).where(dv.notna())], axis=1)
SYMS = list(CL.columns)
days = CL.index
P(f"Panel {len(days)} days {days[0].date()} to {days[-1].date()}; survivors {close.shape[1]} (adjusted TR panel), "
  f"delisted added {dc.shape[1]} (crude returns); dropped as duplicate histories of another code: {' '.join(dup)}")

Af, Cf = ADJ.ffill(), CL.ffill()
last_obs_row = pd.DataFrame(np.arange(len(days))[:, None] + 0 * CL.values, days, SYMS).where(CL.notna()).ffill()
med60 = TV.rolling(60, min_periods=40).median()
mean60, mean250 = TV.rolling(60, min_periods=40).mean(), TV.rolling(250, min_periods=150).mean()
hi252, lo252 = Af.rolling(252, min_periods=150).max(), Af.rolling(252, min_periods=150).min()

# month-end rows
me = pd.Series(np.arange(len(days)), index=days).groupby([days.year, days.month]).last()
ME = [r for r in me.values if days[r] >= pd.Timestamp("2017-01-01")]
END = len(days) - 1
START = [r for r in ME if days[r] <= pd.Timestamp("2026-04-30")]          # last start with ~6m forward
fwd_row = {r: (ME[ME.index(r) + H] if ME.index(r) + H < len(ME) else END) for r in START}

# ============================================================ sectors
sym = pd.read_csv(ROOT / "data/symbols.csv").drop_duplicates("symbol").set_index("symbol").sectorName
SECT = pd.Series({s: sym.get(re.sub(r"(XD|XB|XR)$", "", s), "UNKNOWN") for s in SYMS}).fillna("UNKNOWN")

# ============================================================ base rows: liquid name-months
rows = []
for r in START:
    t = days[r]
    liq = (med60.iloc[r] > LIQ) & (r - last_obs_row.iloc[r] <= 5)
    for s in liq.index[liq.fillna(False).values]:
        p0, p1 = Af.at[t, s], Af.iloc[fwd_row[r]][s]
        rows.append((r, t, s, p0, p1 / p0 - 1, med60.at[t, s]))
D = pd.DataFrame(rows, columns=["row", "date", "sym", "p0", "fwd6", "medtv"])
D["sector"] = D.sym.map(SECT)
D["y"] = (D.fwd6 >= EV).astype(int)
P(f"Liquid name-months (start month-ends 2017-01 to 2026-04): {len(D)}, names {D.sym.nunique()}, "
  f"months {D.row.nunique()}; with 6m forward >= +100%: {D.y.sum()} ({D.y.mean():.2%})")


# ============================================================ features
si = {s: i for i, s in enumerate(SYMS)}
R, Si = D.row.values, D.sym.map(si).values
A = Af.values
for k, n in (("r1", 21), ("r3", 63), ("r6", 126), ("r12", 252)):
    prev = np.where(R - n >= 0, A[np.maximum(R - n, 0), Si], np.nan)
    D[k] = A[R, Si] / prev - 1
D["dist52h"] = A[R, Si] / hi252.values[R, Si] - 1
D["dist52l"] = A[R, Si] / lo252.values[R, Si] - 1
D["vratio"] = mean60.values[R, Si] / mean250.values[R, Si]
D["logtv"] = np.log10(D.medtv)
D["logprice"] = np.log10(Cf.values[R, Si])

# sector 6m momentum rank (1 = best) among liquid names, sectors with >= 2 names
sm6 = D[D.sector != "UNKNOWN"].groupby(["row", "sector"]).r6.agg(["mean", "size"]).reset_index()
sm6 = sm6[sm6["size"] >= 2]
sm6["sect_rank"] = sm6.groupby("row")["mean"].rank(pct=True)
D = D.merge(sm6[["row", "sector", "sect_rank"]], on=["row", "sector"], how="left")

# macro: regime and Brent
tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"]).set_index("date").y6m
pr = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"]).set_index("date").rate
br = pd.read_csv(ROOT / "data/macro/brent.csv", parse_dates=["date"]).set_index("date").value
asof = lambda s, t: s[s.index <= t].iloc[-1]
mac = pd.DataFrame({"date": sorted(D.date.unique())})
mac["regime"] = [asof(tb, t) - asof(pr, t) for t in mac.date]
mac["brent3m"] = [asof(br, t) / asof(br, t - pd.Timedelta(days=91)) - 1 for t in mac.date]
D = D.merge(mac, on="date")

# index additions in prior 6 months (announcement date)
ic = pd.read_csv(ROOT / "data/index_changes.csv")
ad = ic.announce_date.astype(str)
ic["announce_date"] = pd.to_datetime(ad.where(ad.str.len() == 10), errors="coerce").fillna(        # month-only -> month end
    pd.to_datetime(ad.where(ad.str.len() == 7), format="%Y-%m", errors="coerce") + pd.offsets.MonthEnd(0)).fillna(
    pd.to_datetime(ic.effective_date, errors="coerce"))
ic = ic[ic.action == "add"]
MAJOR = {"KSE100", "KSE30", "KMI30", "MSCI_PK", "MSCI_PK_SC", "FTSE_PK"}
for name, sub in (("idx_add_major", ic[ic["index"].isin(MAJOR)]), ("idx_add_kmiall", ic[ic["index"] == "KMI_ALL"])):
    g = {s: v.announce_date.values for s, v in sub.groupby("symbol")}
    D[name] = [int(((g.get(s, np.array([], "datetime64[ns]")) > np.datetime64(t - pd.Timedelta(days=183))) &
                    (g.get(s, np.array([], "datetime64[ns]")) <= np.datetime64(t))).any()) for s, t in zip(D.sym, D.date)]

# announcements in prior 90 days: effective date = same day if at or before 15:30 else next day
an = pd.read_parquet(ROOT / "data/announcements.parquet")
an["symbol"] = an.symbol.str.replace(r"(XD|XB|XR)$", "", regex=True)
lt = an.datetime.dt.tz_convert("Asia/Karachi").dt.tz_localize(None)
an["eff"] = lt.dt.normalize() + pd.to_timedelta(((lt.dt.hour * 60 + lt.dt.minute) > 930).astype(int), unit="D")
it = pd.read_csv(ROOT / "data/insider_trades.csv")
it = it[it.duplicate_of.isna() & it.direction.isin(["buy", "sell"])]
doc_dir = it.groupby("document_id").direction.agg(lambda x: x.value_counts().index[0])
first_doc = pd.to_numeric(an.document_ids.str.split(",").str[0], errors="coerce")
an["dir2"] = an.direction.where(an.direction.isin(["buy", "sell"]), first_doc.map(doc_dir))
an["unusual"] = an.title.str.contains(r"unusual", case=False, na=False)
groups = {
    "a_insider": an.klass == "insider_trade",
    "a_ins_buy": (an.klass == "insider_trade") & (an.dir2 == "buy"),
    "a_ins_sell": (an.klass == "insider_trade") & (an.dir2 == "sell"),
    "a_divbonus": an.klass == "dividend_or_bonus",
    "a_material": an.klass == "material_info",
    "a_board": an.klass == "board_meeting_notice",
    "a_rating": an.klass == "credit_rating",
    "a_unusual": an.unusual,
}
cal = pd.date_range("2015-01-01", days[-1] + pd.Timedelta(days=2))
for name, m in groups.items():
    c = an[m].groupby(["eff", "symbol"]).size().unstack(fill_value=0).reindex(cal, fill_value=0).cumsum()
    c = c.reindex(columns=sorted(set(c.columns) | set(SYMS)), fill_value=0)
    v1 = c.reindex(D.date.values).values
    v0 = c.reindex((D.date - pd.Timedelta(days=90)).values).values
    ci = {s: i for i, s in enumerate(c.columns)}
    j = D.sym.map(ci).values
    D[name] = v1[np.arange(len(D)), j] - v0[np.arange(len(D)), j]
D["a_unusual"] = (D.a_unusual > 0).astype(int)

# quarterly EPS, point in time (first tradable date; missing -> quarter end + 90 days)
q = pd.read_csv(ROOT / "data/fundamentals/quarterly_eps.csv", parse_dates=["fiscal_quarter_end", "first_tradable_date"])
q["avail"] = q.first_tradable_date.fillna(q.fiscal_quarter_end + pd.Timedelta(days=90))
q = q.sort_values(["symbol", "fiscal_quarter_end"]).drop_duplicates(["symbol", "fiscal_quarter_end"])
q["e_prev"] = q.groupby("symbol").eps_basic.shift(1)
q4 = q[["symbol", "fiscal_quarter_end", "eps_basic"]].rename(columns={"eps_basic": "e_yoy"})
q4["fiscal_quarter_end"] = q4.fiscal_quarter_end + pd.DateOffset(years=1)
q4["fiscal_quarter_end"] = q4.fiscal_quarter_end + pd.offsets.MonthEnd(0)
q = q.merge(q4, on=["symbol", "fiscal_quarter_end"], how="left")
chg = lambda a, b: ((a - b) / b.abs()).clip(-5, 5)
q["eps_yoy"], q["eps_qoq"] = chg(q.eps_basic, q.e_yoy), chg(q.eps_basic, q.e_prev)
q["eps_turn"] = ((q.eps_basic > 0) & ((q.e_prev < 0) | (q.e_yoy < 0))).astype(float)
q = q.sort_values("avail")
D = D.sort_values("date")
D = pd.merge_asof(D, q[["symbol", "avail", "eps_yoy", "eps_qoq", "eps_turn"]].rename(columns={"symbol": "sym"}),
                  left_on="date", right_on="avail", by="sym", direction="backward")
stale = (D.date - D.avail).dt.days > 200                     # last result older than ~2 quarters: treat as missing
D.loc[stale, ["eps_yoy", "eps_qoq", "eps_turn"]] = np.nan

# trailing P/E and dividend yield (sa_ratios FY rows; available at the FYE quarter's first tradable date, else FYE+120d)
sa = pd.read_csv(ROOT / "seed/data/fundamentals/sa_ratios.csv")
sa = sa[sa.date != "TTM"].copy()
sa["fye"] = pd.to_datetime(sa.date)
qa = q.set_index(["symbol", "fiscal_quarter_end"]).first_tradable_date
sa["avail"] = [qa.get((s, f), pd.NaT) for s, f in zip(sa.t, sa.fye)]
sa["avail"] = sa.avail.fillna(sa.fye + pd.Timedelta(days=120))
sa = sa[sa.t.isin(SYMS)].sort_values("avail")
APf = ADJPR.ffill()
sa["pfye"] = [APf[s].asof(f) if s in APf else np.nan for s, f in zip(sa.t, sa.fye)]
D = pd.merge_asof(D.sort_values("date"), sa[["t", "avail", "pe", "dividendyield", "pfye"]].rename(columns={"t": "sym", "avail": "avail_sa"}),
                  left_on="date", right_on="avail_sa", by="sym", direction="backward")
scale = D.pfye / APf.values[D.row.values, D.sym.map(si).values]
D["ey"] = (1 / D.pe.where(D.pe > 0)) * scale
D["dy"] = D.dividendyield * scale
D = D.sort_values(["row", "sym"]).reset_index(drop=True)

FEATS = ["r1", "r3", "r6", "r12", "dist52h", "dist52l", "vratio", "logtv", "logprice", "sect_rank", "regime", "brent3m",
         "idx_add_major", "idx_add_kmiall", "a_insider", "a_ins_buy", "a_ins_sell", "a_divbonus", "a_material", "a_board",
         "a_rating", "a_unusual", "eps_yoy", "eps_qoq", "eps_turn", "ey", "dy"]

# ============================================================ events (first start of each run) and peaks
D["qual"] = D.y == 1
ev, chain_end = [], {}
for s, g in D[D.qual].groupby("sym"):
    mi = sorted(ME.index(r) for r in g.row)
    first = prev = mi[0]
    for m in mi[1:] + [None]:
        if m is None or m - prev > H:                       # a new move: no qualifying start in the previous 6 months
            ev.append((s, ME[first])); chain_end[(s, ME[first])] = ME[prev]
            first = m
        prev = m
EVK = set(ev)
D["event"] = [int((s, r) in EVK) for s, r in zip(D.sym, D.row)]
E = D[D.event == 1].copy()
pk, ttp = [], []
for s, r in zip(E.sym, E.row):
    path = Af[s].iloc[r:fwd_row[chain_end[(s, r)]] + 1]
    pk.append(path.max() / path.iloc[0]); ttp.append(int(np.argmax(path.values)))
E["peak_mult"], E["days_to_peak"] = pk, ttp
E["year"] = E.date.dt.year

# independent episodes: same sector, start months chained within 3 months
E = E.sort_values(["sector", "row"])
epi, k = [], 0
for sct, g in E.groupby("sector", sort=False):
    prev = None
    for r in g.row:
        if prev is None or ME.index(r) - ME.index(prev) > 3:
            k += 1
        epi.append(k); prev = r
E["episode"] = epi
E["wave"] = E.groupby("episode").sym.transform("size") >= 3
E = E.sort_values("row")

P("\n== 1. Events: liquid at start, 6-month point-to-point return >= +100%, first start of each run")
P(f"events {len(E)}, distinct names {E.sym.nunique()}, independent sector-time episodes {E.episode.nunique()}, "
  f"events in sector waves (episode of 3+ names) {E.wave.sum()} ({E.wave.mean():.0%})")
P(f"fwd6 median {E.fwd6.median():+.0%} mean {E.fwd6.mean():+.0%}; peak multiple median {E.peak_mult.median():.2f}x "
  f"mean {E.peak_mult.mean():.2f}x max {E.peak_mult.max():.2f}x; trading days to peak median {E.days_to_peak.median():.0f}")
P(f"delisted names among events: {E.sym.isin(dc.columns).sum()}")
P("\nEvents by year (n events / liquid name-months / rate):")
yy = pd.DataFrame({"events": E.groupby("year").size(), "name_months": D.groupby(D.date.dt.year).size()}).fillna(0)
yy["episodes"] = E.groupby("year").episode.nunique()
yy["rate"] = yy.events / yy.name_months
P(yy.to_string())
P("\nEvents by sector:")
P(E.groupby("sector").agg(events=("sym", "size"), names=("sym", "nunique"), episodes=("episode", "nunique"),
                          med_fwd6=("fwd6", "median")).sort_values("events", ascending=False).to_string())
P("\nEpisodes with 3+ names (sector waves):")
for e, g in E[E.wave].groupby("episode"):
    P(f"  {g.sector.iloc[0]:<40} {g.date.min().date()} to {g.date.max().date()}  n={len(g)}  {' '.join(g.sym)}")

# ============================================================ matched controls
C = []
for (r, s, sct, ltv) in E[["row", "sym", "sector", "logtv"]].itertuples(index=False):
    pool = D[(D.row == r) & (D.fwd6 < CT) & ~D.sym.isin([x[1] for x in C if x[0] == r])].copy()
    pool["d"] = (pool.logtv - ltv).abs()
    same = pool[pool.sector == sct].nsmallest(3, "d")
    pick = pd.concat([same, pool[~pool.index.isin(same.index)].nsmallest(3 - len(same), "d")]) if len(same) < 3 else same
    for x in pick.itertuples():
        C.append((r, x.sym, s, int(x.sector == sct)))
Cdf = pd.DataFrame(C, columns=["row", "sym", "case", "same_sector"])
CC = Cdf.merge(D, on=["row", "sym"])
P(f"\n== 2. Matched controls: {len(CC)} for {len(E)} events (same sector {CC.same_sector.mean():.0%}); "
  f"|log10 TV gap| median {np.median(np.abs(CC.logtv.values - E.set_index(['row','sym']).loc[list(zip(CC.row, CC.case))].logtv.values)):.2f}")
P(f"control fwd6: median {CC.fwd6.median():+.1%}, mean {CC.fwd6.mean():+.1%}")


def sdiff(a, b):
    a, b = pd.Series(a).dropna(), pd.Series(b).dropna()
    s = np.sqrt((a.var() + b.var()) / 2)
    return (a.mean() - b.mean()) / s if s > 0 else np.nan


def table(Ev, Co, label):
    rows = []
    for f in FEATS:
        rows.append((f, Ev[f].notna().sum(), Co[f].notna().sum(), Ev[f].mean(), Co[f].mean(), Ev[f].median(), Co[f].median(), sdiff(Ev[f], Co[f])))
    t = pd.DataFrame(rows, columns=["feature", "n_ev", "n_ct", "mean_ev", "mean_ct", "med_ev", "med_ct", "std_diff"])
    t = t.reindex(t.std_diff.abs().sort_values(ascending=False).index)
    P(f"\n{label}")
    P(t.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return t


T_all = table(E, CC, "Feature table, all events vs matched controls (sorted by |standardised difference|)")
# placebo: random 'events' = random liquid names in the same months, with matched controls drawn the same way
pl = []
for _ in range(200):
    kk = E.groupby("row").size()
    seed = int(RNG.integers(1e9))
    fk = D[D.row.isin(kk.index)].sample(frac=1, random_state=seed)
    rk_, k_ = fk.groupby("row").cumcount(), fk.row.map(kk)
    fake = fk[rk_ < k_]

    ctl = fk[(rk_ >= k_) & (rk_ < 4 * k_)]
    pl.append([abs(sdiff(fake[f], ctl[f])) for f in FEATS])
pl = np.nanpercentile(np.array(pl), 95, axis=0)
P("\nPlacebo (200 draws, as many random liquid names as events in each event month vs 3x as many random names): 95th pct |std diff| per feature")
P("  " + "  ".join(f"{f}={v:.2f}" for f, v in zip(FEATS, pl)))
TR = E[E.date < "2023-01-01"]
T_tr = table(TR, CC[CC.row.isin(TR.row)], f"Training period only (starts 2017-01 to 2022-12), {len(TR)} events")
TE = E[E.date >= "2023-01-01"]
T_te = table(TE, CC[CC.row.isin(TE.row)], f"Test period only (starts 2023-01 to 2026-04), {len(TE)} events")

# ============================================================ classifier on the full liquid cross-section
P("\n== 3. Logistic classifier, all liquid name-months; label = 6m forward >= +100%")
train = (D.date <= "2022-06-30").values         # labels of train rows realise by 2022-12
test = (D.date >= "2023-01-01").values
MF = [f for f in FEATS if D.loc[train, f].notna().mean() >= 0.5]   # EPS, P/E, yield have ~0% train coverage: dropped
P("model features (>= 50% coverage in train): " + ", ".join(MF))
X = D[MF].copy()
MISS = [f for f in MF if D[f].isna().any()]


for f in MF:
    lo, hi = np.nanpercentile(X.loc[train, f], [1, 99]) if X.loc[train, f].notna().any() else (np.nan, np.nan)
    if np.isfinite(lo):
        X[f] = X[f].clip(lo, hi)
for f in MISS:
    X[f + "_na"] = X[f].isna().astype(int)
med = X[train].median()
X = X.fillna(med).fillna(0)
mu, sd = X[train].mean(), X[train].std().replace(0, 1)
Z = sm.add_constant((X - mu) / sd)
keep = [c for c in Z.columns if c == "const" or Z.loc[train, c].std() > 0]
Z = Z[keep]
P(f"train rows {train.sum()} (events {D.y[train].sum()}), test rows {test.sum()} (events {D.y[test].sum()})")
P("feature coverage in train (non-missing share): " + ", ".join(f"{f}={D.loc[train, f].notna().mean():.0%}" for f in ["eps_yoy", "ey", "dy", "r12", "a_unusual"]))
fit = lambda yv: sm.GLM(yv, Z[train], family=sm.families.Binomial()).fit_regularized(alpha=0.002, L1_wt=0.0)   # ridge
mdl = fit(D.y[train])
coef = mdl.params.drop("const")
P("largest coefficients (standardised, ridge alpha=0.002): " + ", ".join(f"{k}={v:+.2f}" for k, v in coef.reindex(coef.abs().sort_values(ascending=False).index).head(12).items()))
D["score"] = mdl.predict(Z)


def top_decile(score, mask):
    d = D[mask].assign(s=score[mask])
    d["dec"] = d.groupby("row").s.rank(pct=True, method="first")
    return d


Tt = top_decile(D.score.values, test)
picks = Tt[Tt.dec > 0.9]
base = Tt.y.mean()
P(f"TEST 2023-01 to 2026-04: base rate {base:.2%} ({Tt.y.sum()}/{len(Tt)}); top-decile precision {picks.y.mean():.2%} "
  f"({picks.y.sum()}/{len(picks)}); lift {picks.y.mean() / base:.2f}x; recall {picks.y.sum() / Tt.y.sum():.0%}")
P(f"   precision by test year: " + ", ".join(f"{y}: {g.y.mean():.1%} of {len(g)} (base {Tt[Tt.date.dt.year == y].y.mean():.1%})" for y, g in picks.groupby(picks.date.dt.year)))
dec = Tt.assign(d10=np.ceil(Tt.dec * 10).clip(1, 10)).groupby("d10").agg(n=("y", "size"), hit=("y", "mean"), med_fwd6=("fwd6", "median"))
P("test hit rate by score decile:\n" + dec.to_string(float_format=lambda x: f"{x:.3f}"))
tr_d = top_decile(D.score.values, train)
P(f"in-sample (train) top-decile precision {tr_d[tr_d.dec > 0.9].y.mean():.2%}, base {tr_d.y.mean():.2%}")
E_test = E[E.date >= "2023-01-01"].merge(Tt[["row", "sym", "dec"]], on=["row", "sym"], how="left")
P(f"test EVENTS (first starts, n={len(E_test)}): in top decile {np.mean(E_test.dec > 0.9):.0%}, top 3 deciles {np.mean(E_test.dec > 0.7):.0%}, "
  f"bottom half {np.mean(E_test.dec <= 0.5):.0%}")

# placebo: shuffle labels within month in train, refit, test precision
pp = []
for i in range(20):
    ys = D.y[train].groupby(D.row[train]).transform(lambda v: v.sample(frac=1, random_state=int(RNG.integers(1e9))).values)
    m2 = fit(ys)
    t2 = top_decile(m2.predict(Z).values, test)
    pp.append(t2[t2.dec > 0.9].y.mean())
P(f"placebo (labels shuffled within month in train, 20 refits): test top-decile precision median {np.median(pp):.2%}, "
  f"range {min(pp):.2%} to {max(pp):.2%}")

# ============================================================ returns of the screen, net of costs
cost = lambda tvv: 0.005 + np.where(tvv < SLIP_TV, 0.005, 0.0)
picks = picks.assign(net=(1 + picks.fwd6) * (1 - cost(picks.medtv)) - 1)
allt = Tt.assign(net=(1 + Tt.fwd6) * (1 - cost(Tt.medtv)) - 1)


def st(x):
    x = pd.Series(x).dropna()
    return f"n {len(x)}, mean {x.mean():+.1%}, median {x.median():+.1%}, win {np.mean(x > 0):.0%}, worst {x.min():+.1%}"


P("\n== 4. Screen returns (6m hold from each month-end, net 0.5% round trip + 0.5% slippage under Rs20m TV)")
P("model top decile:     " + st(picks.net))
P("all liquid (placebo): " + st(allt.net))
rp = [allt.groupby("row").sample(n=1, random_state=int(RNG.integers(1e9))).net.median() for _ in range(500)]
P(f"random one-name-per-month placebo, 500 draws: median of medians {np.median(rp):+.1%}, 95th pct {np.percentile(rp, 95):+.1%}")


def portfolio(start, sel, n_pick=None):
    """Semiannual rebalance from `start`, EW buy-and-hold of `sel(row)` names, net of costs. Daily value path."""
    rws = [r for r in START if days[r] >= pd.Timestamp(start)][::H]
    v, path = 1.0, []
    for r in rws:
        names = sel(r)
        e = fwd_row[r]
        seg = Af[names].iloc[r:e + 1].ffill()
        seg = seg / seg.iloc[0]
        c = cost(D[(D.row == r) & D.sym.isin(names)].set_index("sym").medtv.reindex(names).values)
        val = (seg * (1 - c)).mean(axis=1) * v
        path.append(val.iloc[1:] if path else val)
        v = val.iloc[-1]
    path = pd.concat(path)
    return path, path.iloc[-1], (path / path.cummax() - 1).min()


sel_model = lambda r: list(Tt[(Tt.row == r) & (Tt.dec > 0.9)].sym)
sel_all = lambda r: list(Tt[Tt.row == r].sym)
kmi = pd.read_csv(ROOT / "data/macro/kmiallshr.csv", parse_dates=["date"]).set_index("date").close
for start in ("2023-01-01", "2024-10-01"):
    for lab, sel in (("model top decile", sel_model), ("all liquid EW", sel_all)):
        path, end_v, mdd = portfolio(start, sel)
        P(f"Rs50,000 from {path.index[0].date()} to {path.index[-1].date()} in {lab:<17}: Rs{50000 * end_v:,.0f} ({end_v:.2f}x), max drawdown {mdd:.0%}")
    k = kmi[(kmi.index >= path.index[0]) & (kmi.index <= path.index[-1])]
    P(f"   KMI All Share (total return) same span: {k.iloc[-1] / k.iloc[0]:.2f}x, max drawdown {(k / k.cummax() - 1).min():.0%}")

# ============================================================ simple rule screen from training-period differences
P("\n== 5. Rule screen: top 5 training-period discriminators (by |std diff|, event vs control), cut at the monthly "
  "70th percentile in the event direction; flag = at least 3 of 5")
top5 = [f for f in T_tr.feature if f not in ("logtv",) and T_tr.set_index("feature").loc[f, "n_ev"] >= 0.5 * len(TR)][:5]
sign = T_tr.set_index("feature").std_diff.reindex(top5)
P("features: " + ", ".join(f"{f} ({'+' if sign[f] > 0 else '-'}{abs(sign[f]):.2f})" for f in top5))
fl = pd.DataFrame(index=D.index)
for f in top5:
    pr_ = D.groupby("row")[f].rank(pct=True)
    fl[f] = (pr_ > 0.7) if sign[f] > 0 else (pr_ < 0.3)
D["nflag"] = fl.sum(axis=1)
D["rule"] = D.nflag >= 3
for lab, msk in (("train", train), ("test", test)):
    d = D[msk]
    f_ = d[d.rule]
    P(f"{lab}: flagged {len(f_)} of {len(d)} name-months ({len(f_) / len(d):.0%}); precision {f_.y.mean():.2%} vs base {d.y.mean():.2%} "
      f"(lift {f_.y.mean() / d.y.mean():.2f}x); recall {f_.y.sum() / max(d.y.sum(), 1):.0%}; false-positive share of flags {1 - f_.y.mean():.0%}; "
      f"non-events flagged {d[d.y == 0].rule.mean():.0%}")
    P(f"   flagged 6m net: " + st((1 + f_.fwd6) * (1 - cost(f_.medtv)) - 1))

# ============================================================ 2024 to 2026 events
P("\n== 6. Events starting 2024-01 to 2026-04, features at start (flag = monthly 70th/30th pct in the event direction)")
top8 = list(T_all.feature[:8])
sg8 = T_all.set_index("feature").std_diff
rk = {f: D.groupby("row")[f].rank(pct=True) for f in top8}
D["dec_all"] = D.groupby("row").score.rank(pct=True)
L = E[E.date >= "2024-01-01"].copy()
lines = []
for x in L.itertuples():
    i = D[(D.row == x.row) & (D.sym == x.sym)].index[0]
    flags = [f for f in top8 if pd.notna(D.at[i, f]) and ((rk[f][i] > 0.7) if sg8[f] > 0 else (rk[f][i] < 0.3))]
    lines.append((x.sym, x.sector[:22], x.date.date(), f"{x.fwd6:+.0%}", f"{x.peak_mult:.2f}x", x.days_to_peak,
                  f"{D.at[i, 'dec_all']:.2f}", int(D.at[i, 'nflag']), "wave" if x.wave else "solo", ", ".join(flags)))
LL = pd.DataFrame(lines, columns=["sym", "sector", "start", "fwd6", "peak", "d2peak", "model_pct", "rule_flags", "episode", "top8_flags"])
P(LL.to_string(index=False))
P(f"\n2024-26 events: n {len(LL)}; model percentile >= 0.9: {(LL.model_pct.astype(float) >= 0.9).sum()}; rule screen (3+/5): {(LL.rule_flags >= 3).sum()}; "
  f"sector waves: {(LL.episode == 'wave').sum()}")
for s in ["PRL", "ATRL", "NRL", "CNERGY", "ASL", "SAZEW", "FCEPL"]:
    g = D[(D.sym == s) & (D.date >= "2024-01-01")]
    P(f"  {s}: qualifying start months 2024-26: {[str(d.date())[:7] for d in g[g.y == 1].date]}; max 6m fwd from any start {g.fwd6.max():+.0%}")

# predictable vs not
E2 = E.merge(D[["row", "sym", "dec_all", "nflag"]], on=["row", "sym"])
P("\n== 7. How much was visible at the start (all events, model trained on 2017-22, so pre-2023 rows are in-sample)")
for lab, g in (("all", E2), ("test 2023-26", E2[E2.date >= "2023-01-01"])):
    P(f"{lab}: n {len(g)}; model top decile {np.mean(g.dec_all > 0.9):.0%}; top 3 deciles {np.mean(g.dec_all > 0.7):.0%}; "
      f"rule 3+/5 {np.mean(g.nflag >= 3):.0%}; in sector waves {g.wave.mean():.0%}; "
      f"waves with sector rank >= 0.7 at start {np.mean(g[g.wave].sect_rank >= 0.7) if g.wave.any() else float('nan'):.0%}")
P("Events by regime at start (6m T-bill minus policy rate, pts): " +
  ", ".join(f"{k}: {v}" for k, v in pd.cut(E.regime, [-10, -1, -0.25, 0.25, 10]).value_counts().sort_index().items()))
P("Base rate by regime (all liquid name-months): " +
  ", ".join(f"{k}: {v:.2%}" for k, v in D.groupby(pd.cut(D.regime, [-10, -1, -0.25, 0.25, 10]), observed=True).y.mean().items()))

P("Base rate by Brent 3m change at start: " +
  ", ".join(f"{k}: {v:.2%} (n {n})" for (k, v), n in zip(D.groupby(pd.cut(D.brent3m, [-1, -0.1, 0.1, 5]), observed=True).y.mean().items(),
                                                     D.groupby(pd.cut(D.brent3m, [-1, -0.1, 0.1, 5]), observed=True).size())))

# news that arrived after the start: policy-rate change and Brent change inside the 6-month window
prd = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"])
mm = pd.DataFrame({"date": sorted(D.date.unique())})
mm["end"] = [days[fwd_row[ME[[days[r] for r in ME].index(t)]]] for t in mm.date]
mm["cut_fwd"] = [prd[(prd.date > a) & (prd.date <= b)].change_bp.sum() for a, b in zip(mm.date, mm.end)]
mm["brent_fwd"] = [asof(br, b) / asof(br, a) - 1 for a, b in zip(mm.date, mm.end)]
D = D.merge(mm[["date", "cut_fwd", "brent_fwd"]], on="date")
E = E.merge(mm[["date", "cut_fwd", "brent_fwd"]], on="date")
P("\nNews inside the window (known only after the start):")
for lab, m in (("policy rate cut >= 300bp in next 6m", D.cut_fwd <= -300), ("cut 1-299bp", (D.cut_fwd < 0) & (D.cut_fwd > -300)),
               ("no change or hike", D.cut_fwd >= 0)):
    P(f"  {lab:<38} name-months {m.sum():>5}, base rate {D[m].y.mean():.2%}, events {int(D[m].event.sum())}")
P(f"  Brent +20% or more in next 6m: name-months {(D.brent_fwd >= 0.2).sum()}, base rate {D[D.brent_fwd >= 0.2].y.mean():.2%}; "
  f"events {int(D[D.brent_fwd >= 0.2].event.sum())}")
big_cut = E.cut_fwd <= -300
P(f"Events: big cut ahead {big_cut.mean():.0%}; sector wave and no big cut {(E.wave & ~big_cut).mean():.0%}; "
  f"neither (idiosyncratic, no big cut) {(~E.wave & ~big_cut).mean():.0%}")
P(f"Events in 2024-26 that started in the Feb-Mar 2026 refinery wave (Hormuz closed 28 Feb 2026 per tests/refiner_steel_retrospective.md): "
  f"{' '.join(E[(E.sector == 'REFINERY') & (E.date >= '2026-01-01')].sym)}")
P("\nNamed names, all event starts any year:")
P(E[E.sym.isin(["PRL", "ATRL", "NRL", "CNERGY", "ASL", "SAZEW", "FCEPL"])][["sym", "date", "fwd6", "peak_mult", "days_to_peak", "wave", "cut_fwd"]].to_string(index=False))

out = ROOT / "tests/out"
E.to_csv(out / "winners_case_control_events.csv", index=False)
D[["date", "sym", "sector", "fwd6", "y", "event", "score", "dec_all", "nflag"] + FEATS].to_csv(out / "winners_case_control_features.csv", index=False)
(out / "winners_case_control.txt").write_text("\n".join(OUT), encoding="utf-8")
