"""Monthly walk-forward engine for the pre-registered strategies B0, B1, S2, S3, S4 (knowledge/playbooks/strategy_candidates.md).
Run: .venv/Scripts/python.exe -I scripts/walkforward.py      Writes tests/out/system_walkforward.txt, walkforward_trades.csv, walkforward_holdings.csv.
Point in time: every decision at month-end F_k uses data stamped by F_k; trades execute at the first close D_k of the next month, when the Rs50,000 deposit arrives.
Frozen rules are implemented as written. Anything added after seeing results is labelled POST-HOC and kept out of the headline.
"""
import sys, io, re, ast, glob, calendar, collections, warnings
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import brentq

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
def pc(x, d=1): return "-" if x is None or not np.isfinite(x) else f"{x:+.{d}%}"
def rs(x): return "-" if x is None or not np.isfinite(x) else f"{x:,.0f}"

C, DEP, MINT, SATW, NSAT, SEED = 0.0025, 50000.0, 5000.0, 0.125, 4, 20261017
LAST_TXT = "2026-10-16"
rng = np.random.default_rng(SEED)

# ================================================================ panel and returns
close, vol, tv = P.load_panel()
dates, N, cols = close.index, len(close), list(close.columns)
cidx = {s: i for i, s in enumerate(cols)}
LAST = dates[-1]
assert LAST == pd.Timestamp(LAST_TXT)
closeV, rawF = close.values, close.ffill().values
prF = pd.read_parquet(ROOT / "data/panel_close_adj_pricereturn.parquet").reindex(index=dates, columns=cols).ffill().values
oc = np.cumsum(np.isfinite(closeV), axis=0)
ACTS = P.load_actions()
A_NET = ACTS.copy(); A_NET.loc[A_NET.type == "cash", "value"] *= 0.85          # 15% withholding on cash dividends
A_PR = ACTS[ACTS.type != "cash"]                                               # POST-HOC variant: bonus and split only
def make_tri(actions):
    r = P.returns(close, "adjusted", actions=actions)
    return r, (1 + r.fillna(0)).cumprod().values
RET = {}; TRI = {}
for b, a in (("TR", A_NET), ("PR", A_PR)):
    RET[b], TRI[b] = make_tri(a)

# ================================================================ calendar: trade date D_k, formation date F_k
MI = pd.period_range("2018-01", "2026-10", freq="M")
ID = [int(dates.searchsorted(m.start_time)) for m in MI]
IF = [i - 1 for i in ID]
K = len(ID)
assert dates[IF[0]] == pd.Timestamp("2017-12-29") and K == 106
KOF = {i: k for k, i in enumerate(ID)}

# ================================================================ membership (KMI All Share), point in time
RENAME = {"ENGRO": "ENGROH", "BYCO": "CNERGY", "ICI": "LCI"}
def norm(s):
    s = RENAME.get(s, s)
    if s not in cidx:
        s = re.sub(r"(XD|XB|XR)$", "", s); s = RENAME.get(s, s)
    return s
LISTS = {}
for f in sorted(glob.glob(str(ROOT / "data/index_members/KMI_ALL_derived_*.csv"))):
    LISTS[pd.Timestamp(re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1))] = {norm(s) for s in pd.read_csv(f).symbol}
LISTS[pd.Timestamp("2026-06-05")] = {norm(s) for s in pd.read_csv(ROOT / "data/index_members/KMI_ALL_2026-06-05.csv").symbol}  # exact list wins
_ic = pd.read_csv(ROOT / "data/index_changes.csv"); _ic["effective_date"] = pd.to_datetime(_ic.effective_date, errors="coerce")
CH = _ic[(_ic["index"] == "KMI_ALL") & ~_ic.source_url.astype(str).str.contains("derived")].copy()
CH["symbol"] = CH.symbol.map(norm)
LDATES = sorted(LISTS)
def members_at(t):
    ds = [d for d in LDATES if d <= t]
    d0 = ds[-1] if ds else LDATES[0]
    m = set(LISTS[d0])
    for r in CH[(CH.effective_date > d0) & (CH.effective_date <= t)].sort_values("effective_date").itertuples():
        (m.add if r.action == "add" else m.discard)(r.symbol)
    return m

# ================================================================ sector labels (screener codes mapped as in sector_momentum_regime.py U3)
scr = pd.read_csv(ROOT / "seed/data/fundamentals/screener_20261016.csv")
CODE = {}
for r in scr.itertuples():
    sym = r.symbol if r.symbol in cidx else re.sub(r"(XD|XB|XR)$", "", r.symbol)
    if pd.notna(r.sector) and (sym not in CODE or r.symbol == sym):
        CODE[sym] = str(int(r.sector))
_tree = ast.parse((ROOT / "scripts/sector_momentum.py").read_text(encoding="utf-8"))
S_DICT = [ast.literal_eval(n.value) for n in _tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "S"][0]
votes = collections.defaultdict(collections.Counter)
for lab, names in S_DICT.items():
    for nm in names.split():
        if nm in CODE: votes[CODE[nm]][lab] += 1
BANK_CODE, MOD_CODES = CODE["MEBL"], {CODE["FHAM"], CODE["PAKQATAR"]}
SHORT = {"Oil refineries": "Refineries", "Steel & engineering": "Steel & eng", "Glass, packaging, paper": "Glass/pack/paper", "Gas utilities & misc": "Gas utils & misc"}
LABEL = {}
for code in sorted(set(CODE.values())):
    lab = "Islamic banks" if code == BANK_CODE else "Modarabas & takaful" if code in MOD_CODES else votes[code].most_common(1)[0][0] if votes[code] else f"code{code}"
    LABEL[code] = SHORT.get(lab, lab)
SEC = {s: LABEL[c] for s, c in CODE.items()}
BANK = "Islamic banks"
HIKE_L = ["Autos", "Islamic banks", "Power"]
CUT_L = ["Fertilizer", "Pharma", "Cement", "OMC"]
TIGHT_L = ["Islamic banks", "E&P", "Fertilizer"]
EASE_L = ["Autos", "Cement", "Steel & eng", "Glass/pack/paper", "Textiles", "OMC", "Tech & telecom"]

# ================================================================ macro inputs
pol = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"]).sort_values("date").reset_index(drop=True)
tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"]).sort_values("date")
tb6 = tb[tb.y6m.notna()].reset_index(drop=True)
cpi = pd.read_csv(ROOT / "data/macro/cpi.csv").set_index("month").yoy
def rate_at(t): return float(pol[pol.date <= t].iloc[-1].rate)
def regimes(F, prev_easing):
    """-> (b1 regime, s3 regime, detail). Strictly data on or before F; CPI month t-1 is the latest usable print."""
    rate = rate_at(F)
    a = tb6[tb6.date <= F].tail(2)
    y6 = float(a.iloc[-1].y6m)
    spread = y6 - rate
    b1 = "HIKE" if spread >= 0.5 else "CUT" if spread <= -0.5 else "NEUTRAL"
    u = F.to_period("M") - 1
    c0, c1, c2 = (float(cpi[str(u - j)]) for j in range(3))
    cpi_fall, cpi_rise = (c0 < c1 < c2), (c0 > c1 > c2)
    below2 = len(a) == 2 and all(r.y6m < rate_at(r.date) for r in a.itertuples())
    cond_i = cpi_fall and below2
    last = pol[pol.date <= F].iloc[-1]
    cond_ii = last.decision == "cut" and y6 <= rate + 0.5
    leave = (y6 >= rate + 0.5) or cpi_rise
    easing = (prev_easing or cond_i or cond_ii) and not leave
    hike6 = ((pol.decision == "hike") & (pol.date <= F) & (pol.date > F - pd.DateOffset(months=6))).any()
    tight = (y6 >= rate + 0.5) or hike6
    s3 = "EASING" if easing else "TIGHT" if tight else "NEUTRAL"
    return b1, s3, dict(rate=rate, y6=y6, spread=spread, cpi=c0)

# ================================================================ announcements (annual results, quarterly results)
ann = pd.read_parquet(ROOT / "data/announcements.parquet")
_sym = ann.symbol.str.replace(r"(XD|XB|XR)$", "", regex=True)
ann["symbol"] = _sym.where(_sym.isin(cidx) & ~ann.symbol.isin(cidx), ann.symbol)
ann["dt"] = ann.datetime.dt.tz_localize(None)
fr = ann[ann.klass == "financial_result"].copy()
low = fr.title.str.lower()
fr["is_trans"] = low.str.contains("transmission|annual report")
NOTRES = r"extension|extend|application|applied|briefing|commentary|placement|progress report|approval of|board of director|issuance of direction"
fr["bad"] = low.str.contains("revoked|other than|board meeting|conclusion|transmission|annual report|" + NOTRES) | ~low.str.contains("result")
MON = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
MON.update({m.lower(): i for i, m in enumerate(calendar.month_abbr) if m}); MON["sept"] = 9
def parse_period(t):
    t = t.lower()
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", t)
    try:
        if m: return pd.Timestamp(int(m[1]), int(m[2]), int(m[3]))
        m = re.search(r"(\d{1,2})[-./](\d{1,2})[-./](\d{4})", t)
        if m: return pd.Timestamp(int(m[3]), int(m[2]), int(m[1]))
        for m in re.finditer(r"([a-z]{3,9})\.?\s*(\d{1,2})\s*,?\s*(\d{4})", t):
            if m[1] in MON: return pd.Timestamp(int(m[3]), MON[m[1]], int(m[2]))
        for m in re.finditer(r"(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]{3,9})\.?,?\s*(\d{4})", t):
            if m[2] in MON: return pd.Timestamp(int(m[3]), MON[m[2]], int(m[1]))
    except ValueError:
        pass
    return pd.NaT
def kind(l):
    if "half" in l: return "H"
    if re.search(r"year|annual", l): return "Y"
    if re.search(r"quarter|quater|period", l): return "Q"
    return "U"
fr["pdate"] = [parse_period(t) for t in fr.title]
fr["kind"] = [kind(t.lower()) for t in fr.title]
FR = {s: g.sort_values("dt") for s, g in fr[~fr.bad].groupby("symbol")}

def t0_idx(ts):
    """Index of the first panel close at or after the filing (15:30 PKT rule), -1 if none."""
    if pd.isna(ts): return -1
    after = ts.hour * 60 + ts.minute > 15 * 60 + 30
    i = dates.searchsorted(ts.normalize(), side="right" if after else "left")
    return int(i) if i < N else -1

# ---- annual results -> value rows
sa = pd.read_csv(ROOT / "seed/data/fundamentals/sa_ratios.csv")
fy = sa[(sa.date != "TTM") & sa.t.isin(cidx)].copy()
fy["fye"] = pd.to_datetime(fy.date)
def annual_ts(sym, fye):
    g = FR.get(sym)
    if g is None: return pd.NaT
    Y = g[g.kind == "Y"]
    lag = (Y.dt.dt.normalize() - fye).dt.days
    c = Y[Y.pdate.eq(fye) & lag.between(0, 150)]
    if not len(c): c = Y[Y.pdate.isna() & lag.between(7, 150)]
    return c.dt.min() if len(c) else pd.NaT
fy["pub"] = [annual_ts(s, f) for s, f in zip(fy.t, fy.fye)]
fy["i_ann"] = [t0_idx(p) for p in fy.pub]
fy["i_fb4"] = [int(dates.searchsorted(f + pd.DateOffset(months=4))) for f in fy.fye]   # frozen fallback: FYE + 4 months
fy["i_fb3"] = [int(dates.searchsorted(f + pd.DateOffset(months=3))) for f in fy.fye]   # task wording: 3 months after FYE
fy["use_frozen"] = np.where(fy.i_ann >= 0, fy.i_ann, fy.i_fb4)
fy["use_task"] = np.where(fy.i_ann >= 0, np.maximum(fy.i_ann, fy.i_fb3), fy.i_fb3)       # POST-HOC variant: later of announcement and FYE+3m
fy["pfye"] = [prF[max(int(dates.searchsorted(f, side="right")) - 1, 0), cidx[s]] for s, f in zip(fy.t, fy.fye)]
VROWS = {s: g.sort_values("fye") for s, g in fy.groupby("t")}

# ---- quarterly EPS, with announcement re-join (as results_surprise_drift.py)
e = pd.read_csv(ROOT / "data/fundamentals/quarterly_eps.csv", parse_dates=["fiscal_quarter_end"]).rename(columns={"fiscal_quarter_end": "qe"})
e["cur"] = pd.to_datetime(e.announce_dt.str.slice(0, 19), errors="coerce")
e["cur_trans"] = e.announce_title.fillna("").str.lower().str.contains("transmission|annual report")
_t = e.announce_title.fillna("").str.lower()
e["cur_bad"] = e.announce_dt.notna() & ~e.cur_trans & (_t.str.contains("revoked|other than|board meeting|conclusion|" + NOTRES) | ~_t.str.contains("result"))
ME = pd.offsets.MonthEnd(0)
ix = e.set_index(["symbol", "qe"])
def look(col, shift):
    k = list(zip(e.symbol, [q + pd.DateOffset(months=shift) + ME for q in e.qe]))
    return ix[col].reindex(pd.MultiIndex.from_tuples(k, names=["symbol", "qe"])).values
e["eps"] = e.eps_basic.fillna(e.eps_diluted)
e["eps_ly"] = look("eps_basic", -12)
e["eps_ly"] = np.where(np.isnan(e.eps_ly), look("eps_diluted", -12), e.eps_ly)
fym = {}
for s, g in fr[(fr.kind == "Y") & ~fr.is_trans & ~fr.bad & fr.pdate.notna()].groupby("symbol"): fym[s] = int(g.pdate.dt.month.mode().iloc[0])
for s, g in e[e.announce_title.fillna("").str.lower().str.contains("year ended") & ~e.cur_trans].groupby("symbol"):
    if s not in fym: fym[s] = int(g.qe.dt.month.mode().iloc[0])
def qtype(s, qe):
    if s not in fym: return "NA"
    return {0: "Q4", 3: "Q1", 6: "Q2", 9: "Q3"}.get((qe.month - fym[s]) % 12, "NA")
e["qtype"] = [qtype(s, q) for s, q in zip(e.symbol, e.qe)]
new = []
for r in e.itertuples():
    if pd.isna(r.cur): new.append(pd.NaT); continue
    g = FR.get(r.symbol); pick = None
    if g is not None:
        ok = (g.dt >= r.qe + pd.Timedelta(days=7)) & (g.dt <= (r.qe + pd.Timedelta(days=150) if r.cur_bad else r.cur))
        pd_ok = g.pdate.notna() & ((g.pdate - r.qe).abs() <= pd.Timedelta(days=4))
        und = g.pdate.isna()
        kind_ok = ((g.kind == "Y") & (r.qtype in ("Q4", "NA"))) | ((g.kind == "H") & (r.qtype in ("Q2", "NA"))) | ((g.kind == "Q") & (r.qtype != "Q4")) | (g.kind == "U")
        c = g[ok & (pd_ok | (und & kind_ok))]
        if len(c): pick = c.iloc[0]
    if pick is not None: new.append(pick["dt"])
    elif r.cur_trans or r.cur_bad: new.append(pd.NaT)
    else: new.append(r.cur)
e["ann"] = new
e["i0"] = [t0_idx(t) for t in e.ann]
e = e.sort_values(["symbol", "qe"]).reset_index(drop=True)
e["dated"] = (e.i0 >= 0) & e.eps.notna()
e["yoy_ok"] = e.dated & e.eps_ly.notna()
e["neg_yoy"] = e.yoy_ok & (e.eps < e.eps_ly)
e["blow"] = e.yoy_ok & (((e.eps_ly > 0) & (e.eps / e.eps_ly - 1 >= 0.5)) | ((e.eps_ly < 0) & (e.eps > 0)))
e["next_i0"] = N + 10 ** 6
for s, g in e[e.dated].sort_values("i0").groupby("symbol"):
    e.loc[g.index, "next_i0"] = list(g.i0.values[1:]) + [N + 10 ** 6]
FILINGS = {s: list(zip(g.i0, g.neg_yoy)) for s, g in e[e.dated].groupby("symbol")}

# ================================================================ month records: universe, regime, value
M = []
prev_easing = False
for k in range(K):
    iF, iD = IF[k], ID[k]
    F = dates[iF]
    mem = members_at(F)
    liq = set(P.liquid_universe(F))
    U = sorted(s for s in liq & mem if s in cidx)
    b1, s3, det = regimes(F, prev_easing)
    prev_easing = s3 == "EASING"
    bysec = collections.defaultdict(list)
    for s in U:
        if s in SEC: bysec[SEC[s]].append(s)
    M.append(dict(k=k, iF=iF, iD=iD, F=F, D=dates[iD], mem_exit=members_at(dates[iD] - pd.Timedelta(days=1)), U=U, Uset=set(U), bysec=dict(bysec),
                  elig={sec for sec, v in bysec.items() if len(v) >= 3}, b1=b1, s3=s3, det=det, nmem=len(mem), U_all=U))

# AUDIT 2026-10-17 (Opus): sa_ratios (108 names) and quarterly_eps (129) were chosen on 2026 liquidity, so every value or
# earnings pick comes from ex-post survivors, while B0 holds all of U(t). POOL = the names a strategy could ever pick.
POOL = set(VROWS) | set(e.symbol)
EPSSET = set(e.symbol)
def set_pool(keep=None):
    """Restrict U(t) to `keep` for every month (None = the frozen full U(t))."""
    for m in M:
        U = [s for s in m["U_all"] if keep is None or s in keep]
        bysec = collections.defaultdict(list)
        for s in U:
            if s in SEC: bysec[SEC[s]].append(s)
        m.update(U=U, Uset=set(U), bysec=dict(bysec), elig={sec for sec, v in bysec.items() if len(v) >= 3})

def build_val(mode):
    """Value metrics per month, drift-adjusted. mode 'frozen' (announcement else FYE+4m) or 'task' (later of announcement, FYE+3m)."""
    col = "use_frozen" if mode == "frozen" else "use_task"
    for m in M:
        iF, v = m["iF"], {}
        for s in m["U"]:
            g = VROWS.get(s)
            if g is None: continue
            g = g[g[col] <= iF]
            if not len(g): continue
            r = g.iloc[-1]; c = cidx[s]
            pt = prF[iF, c]
            if not (np.isfinite(pt) and pt > 0 and np.isfinite(r.pfye) and r.pfye > 0): continue
            ey = (r.pfye / r.pe) / pt if (np.isfinite(r.pe) and r.pe > 0) else np.nan
            dy = (r.dividendyield if np.isfinite(r.dividendyield) else 0.0) * r.pfye / pt
            pbt = r.pb * pt / r.pfye if (np.isfinite(r.pb) and r.pb > 0) else np.nan
            bm = r.roe / pbt if np.isfinite(pbt) and np.isfinite(r.roe) else np.nan
            v[s] = dict(ey=ey, dy=dy, roe=r.roe, bm=bm, fye=r.fye, metric=bm if SEC.get(s) == BANK else ey)
        m["val"] = v
        m["nval"] = sum(np.isfinite(x["ey"]) for x in v.values())
        rk = {}
        for sec, names in m["bysec"].items():
            ms = sorted([(v[s]["metric"], s) for s in names if s in v and np.isfinite(v[s]["metric"])], reverse=True)
            for i, (_, s) in enumerate(ms): rk[s] = i / len(ms)
        m["rank"] = rk
    first = next(m["k"] for m in M if m["nval"] >= 15)
    for m in M: m["value_mode"] = m["k"] >= first
    return first

# ================================================================ features that depend on the return basis
def build_feat(basis):
    T, ret = TRI[basis], RET[basis].values
    for m in M:
        iF = m["iF"]; sec6 = {}
        if iF - 126 >= 0:
            for sec, names in m["bysec"].items():
                x = []
                for s in names:
                    c = cidx[s]
                    if (oc[iF, c] - oc[iF - 126, c]) / 126 >= 0.6: x.append(T[iF, c] / T[iF - 126, c] - 1)
                if x: sec6[sec] = float(np.mean(x))
        m["sec6"] = sec6
    ew = np.full(N, np.nan)
    for k in range(K):
        lo, hi = ID[k] + 1, (ID[k + 1] if k + 1 < K else N - 1)
        cs = [cidx[s] for s in M[k]["U"]]
        ew[lo:hi + 1] = np.nanmean(ret[lo:hi + 1][:, cs], axis=1)
    cum = np.cumprod(1 + np.nan_to_num(ew))
    sigs = []
    for r in e[e.blow & e.dated].itertuples():
        i0, b, c = r.i0, r.i0 + 20, cidx[r.symbol]
        if b >= N: continue
        rs_, rm_ = T[b, c] / T[i0, c] - 1, cum[b] / cum[i0] - 1
        sigs.append(dict(sym=r.symbol, c=c, i0=i0, live=b, exp=r.next_i0, flat=abs(rs_ - rm_) <= 0.05, eps=r.eps, af0=prF[i0, c] / rawF[i0, c], qe=r.qe, rs=rs_, rm=rm_))
    return ew, cum, sigs

# ================================================================ allocation
def waterfill(pool, s, minimum):
    s = {k: v for k, v in s.items() if v > 0}
    while s:
        tot = sum(s.values())
        if tot <= pool:
            a = {k: v + (pool - tot) * v / tot for k, v in s.items()}
        else:
            lo, hi = 0.0, max(s.values())
            for _ in range(60):
                lam = (lo + hi) / 2
                if sum(max(0.0, v - lam) for v in s.values()) > pool: lo = lam
                else: hi = lam
            a = {k: max(0.0, v - hi) for k, v in s.items()}
            t = sum(a.values()); a = {k: v * pool / t for k, v in a.items()}
        a = {k: v for k, v in a.items() if v > 1e-9}
        if len(a) <= 1 or all(v >= minimum for v in a.values()): return a
        del s[min(a, key=a.get)]
    return {}

class Run:
    def __init__(s, name, basis, mode, sat=True, excl=False, cstop=False):
        s.name, s.basis, s.mode, s.sat, s.excl, s.cstop, s.block = name, basis, mode, sat, excl, cstop, {}
        s.T = TRI[basis]; s.pos = {}; s.log = []; s.ev = []; s.used = set()
        s.fees = np.zeros(K); s.nav_pre = np.zeros(K); s.buy_amt = np.zeros(K); s.sell_val = np.zeros(K); s.nhold = np.zeros(K); s.hold_rows = []
        s.reason_n = collections.Counter()

    def buy(s, k, sym, amt, sleeve, **meta):
        iD, c = ID[k], cidx[sym]
        x = amt / (1 + C); u = x / s.T[iD, c]
        p = s.pos.get(sym)
        if p is None:
            p = s.pos[sym] = dict(u=0.0, c=c, sleeve=sleeve, ie=iD, ke=k, cost=0.0, proc=0.0, nb=0, **meta)
        p["u"] += u; p["cost"] += amt; p["nb"] += 1
        s.ev.append((iD, c, u, sleeve)); s.fees[k] += amt - x; s.buy_amt[k] += amt

    def sell(s, k, sym, frac, reason):
        iD, p = ID[k], s.pos[sym]
        u = p["u"] * frac; val = u * s.T[iD, p["c"]]
        p["u"] -= u; p["proc"] += val * (1 - C)
        s.ev.append((iD, p["c"], -u, p["sleeve"])); s.fees[k] += val * C; s.sell_val[k] += val
        if frac >= 0.999999:
            s.log.append(dict(strategy=s.name, sleeve=p["sleeve"], symbol=sym, entry=dates[p["ie"]], exit=dates[iD], ie=p["ie"], ix=iD, cost=p["cost"], proceeds=p["proc"],
                              ret=p["proc"] / p["cost"] - 1, sessions=iD - p["ie"], nbuys=p["nb"], status="closed", reason=reason, k_entry=p["ke"], sig=p.get("sig")))
            del s.pos[sym]
        s.reason_n[reason] += 1
        return val * (1 - C)

def sat_candidates(R, m, sigs, exclude):
    iF, iD = m["iF"], m["iD"]
    out_ = []
    for g in sigs:
        key = (g["sym"], g["i0"])
        if key in R.used or not g["flat"] or not (g["live"] <= iF < g["exp"]): continue
        s = g["sym"]
        if s not in m["Uset"] or s in exclude or not np.isfinite(closeV[iD, g["c"]]): continue
        pt = rawF[iF, g["c"]]
        if not (pt > 0): continue
        eps_t = g["eps"] * g["af0"] / (prF[iF, g["c"]] / rawF[iF, g["c"]])
        out_.append((4 * eps_t / pt, key, g))
    out_.sort(key=lambda x: -x[0])
    return out_

def step(R, strat, k, sigs):
    m, iF, iD, T = M[k], IF[k], ID[k], R.T
    pos = R.pos
    R.nav_pre[k] = sum(p["u"] * T[iD, p["c"]] for p in pos.values())
    tradable = lambda s: np.isfinite(closeV[iD, cidx[s]])
    sells = {s: "shariah" for s in pos if s not in m["mem_exit"]}
    quarter = m["F"].month in (3, 6, 9, 12)
    core_t, sat_keep, sat_new = [], [], []
    elig = m["elig"]; sec6 = m["sec6"]; val = m["val"]
    top3 = lambda secs: [x for x in sorted((x for x in secs if x in sec6), key=lambda x: -sec6[x])][:3]

    def core_pick(secs, per):
        picks = []
        if not m["value_mode"]:                                   # fallback: EW of the chosen sectors' liquid names
            return [(s, None) for sec in secs for s in m["bysec"][sec]]
        for rnk in range(per):
            for sec in secs:
                cand = sorted([(val[s]["metric"], s) for s in m["bysec"][sec] if s in val and np.isfinite(val[s]["metric"]) and val[s]["roe"] >= 0.15], reverse=True)
                if len(cand) > rnk: picks.append((cand[rnk][1], val[cand[rnk][1]]["fye"]))
        return picks

    def core_review(chosen):
        for s, p in pos.items():
            if p["sleeve"] != "core" or s in sells: continue
            if SEC.get(s) not in chosen: sells[s] = "review_sector"; continue
            v = val.get(s)
            if m["value_mode"] and v is not None and (p.get("fye") is None or v["fye"] > p["fye"]) and m["rank"].get(s, 0) >= 0.5:
                sells[s] = "review_ey_bottom_half"

    if strat == "B0":
        pass
    elif strat == "B1":
        allowed_l = {"HIKE": HIKE_L, "CUT": CUT_L}.get(m["b1"])
        allowed = [x for x in (allowed_l or sorted(elig)) if x in elig]
        names = [s for sec in allowed for s in m["bysec"][sec]]
        if m["value_mode"]:
            rk = sorted([(val[s]["ey"] + val[s]["dy"], s) for s in names if s in val and np.isfinite(val[s]["ey"])], reverse=True)
            core_t = [(s, None) for _, s in rk[:5]]; top10 = {s for _, s in rk[:10]}
        else:
            core_t = [(s, None) for s in names]; top10 = None
        if quarter:
            for s, p in pos.items():
                if s in sells: continue
                if allowed_l is not None and SEC.get(s) not in allowed_l: sells[s] = "review_regime"
                elif top10 is not None and s not in top10: sells[s] = "review_rank"
    else:
        if strat == "S2":
            chosen = top3(elig); per = 1
        else:
            per = 1 if strat == "S3" else 2
            if m["s3"] == "TIGHT": chosen, rset = [x for x in TIGHT_L if x in elig], set(TIGHT_L)
            elif m["s3"] == "EASING": chosen, rset = top3([x for x in EASE_L if x in elig]), set(EASE_L)
            else: chosen, rset = top3(elig), None
            prev = M[k - 1]["s3"] if k else None
            if rset is not None and prev is not None and prev != m["s3"]:
                for s, p in pos.items():
                    if p["sleeve"] == "core" and s not in sells and SEC.get(s) not in rset: sells[s] = "regime_set"
        core_t = core_pick(chosen, per)
        if strat == "S4" and m["value_mode"]: core_t = core_t[:4]
        if quarter: core_review(set(chosen))
        if R.cstop:   # POST-HOC variant E (audit): S2's 25% trailing stop applied to core names; a stopped name is not re-bought for 3 months
            for s, p in pos.items():
                if p["sleeve"] == "core" and s not in sells:
                    path = T[p["ie"]:iF + 1, p["c"]]
                    if (path / np.maximum.accumulate(path)).min() <= 0.75: sells[s] = "core_trail"; R.block[s] = k + 3
            core_t = [(s, f) for s, f in core_t if k >= R.block.get(s, -1)]
        if R.sat and strat in ("S2", "S4"):
            for s, p in pos.items():
                if p["sleeve"] != "sat" or s in sells: continue
                path = T[p["ie"]:iF + 1, p["c"]]
                if iF - p["ie"] >= 120: sells[s] = "sat_time"
                elif any(p["ie"] < i0 <= iF and ng for i0, ng in FILINGS.get(s, [])): sells[s] = "sat_breaker"
                elif (path / np.maximum.accumulate(path)).min() <= 0.75: sells[s] = "sat_trail"
        if quarter and core_t:
            for s, p in pos.items():
                if p["sleeve"] == "ew": sells[s] = "review_ew_flush"

    # ---- execute sells; trim names above 35% at month end F down to 25%
    wF = {s: p["u"] * T[iF, p["c"]] for s, p in pos.items()}
    totF = sum(wF.values())
    trims = [s for s in pos if strat != "B0" and totF > 0 and wF[s] / totF > 0.35 and s not in sells]
    V0 = sum(p["u"] * T[iD, p["c"]] for p in pos.values())
    pool = DEP
    for s, why in list(sells.items()):
        if not tradable(s): continue                                # suspended: defer to next month
        pool += R.sell(k, s, 1.0, why)
    trimmed = set()
    for s in trims:
        if s in pos and tradable(s):
            v = pos[s]["u"] * T[iD, pos[s]["c"]]
            if v > 0.25 * V0:                                       # a trimmed name gets no new money this month
                pool += R.sell(k, s, 1 - 0.25 * V0 / v, "trim"); trimmed.add(s)
    # ---- targets
    held_sat = [s for s, p in pos.items() if p["sleeve"] == "sat" and tradable(s)]
    core_t = [(s, f) for s, f in core_t if tradable(s)]
    if R.excl and trimmed:     # POST-HOC variant D: a trimmed name gets no new money this month, unless nothing else is left to buy
        c2, h2 = [(s, f) for s, f in core_t if s not in trimmed], [s for s in held_sat if s not in trimmed]
        if c2 or h2: core_t, held_sat = c2, h2
    new_sat = []
    if R.sat and strat in ("S2", "S4"):
        coreset = {s for s, _ in core_t}
        cands = sat_candidates(R, m, sigs, set(pos) | set(sells) | coreset)
        for _, key, g in cands:
            if len(held_sat) + len(new_sat) >= NSAT: break
            new_sat.append((g["sym"], key))
    n_sat = len(held_sat) + len(new_sat)
    Vh = sum(p["u"] * T[iD, p["c"]] for p in pos.values())
    Vtot = Vh + pool
    wts = {}
    if strat == "B0":
        U = [s for s in m["U"] if tradable(s)]
        for s in U: R.buy(k, s, pool / len(U), "core")
    else:
        share = 1 - SATW * n_sat
        if core_t:
            for s, f in core_t: wts[s] = (share / len(core_t), "core", dict(fye=f))
        else:
            U = [s for s in m["U"] if tradable(s)]
            for s in U: wts[s] = (share / len(U), "ew", {})
        for s in held_sat: wts[s] = (SATW, "sat", {})
        for s, key in new_sat: wts[s] = (SATW, "sat", dict(sig=key))
        short = {s: w * Vtot - (pos[s]["u"] * T[iD, pos[s]["c"]] if s in pos else 0.0) for s, (w, _, _) in wts.items()}
        alloc = waterfill(pool, short, MINT)
        if not alloc:
            alloc = {s: pool * w for s, (w, _, _) in wts.items()}   # nothing below target: split by target weight
        for s, amt in alloc.items():
            sl = wts[s][1]
            if s in pos: sl = pos[s]["sleeve"]
            R.buy(k, s, amt, sl, **(wts[s][2] if s not in pos else {}))
            if "sig" in wts[s][2]: R.used.add(wts[s][2]["sig"])
    R.nhold[k] = len(pos)
    for s, p in pos.items():
        R.hold_rows.append((R.name, dates[iD], s, p["sleeve"], p["u"], p["u"] * T[iD, p["c"]]))

# ================================================================ EW KMI benchmark (monthly rebalanced) and KSE100
class EWRun(Run):
    def step(s, k):
        m, iD, T = M[k], ID[k], s.T
        s.nav_pre[k] = sum(p["u"] * T[iD, p["c"]] for p in s.pos.values())
        U = [x for x in m["U"] if np.isfinite(closeV[iD, cidx[x]])]
        tot = s.nav_pre[k] + DEP
        tgt = tot / len(U)
        cur = {x: p["u"] * T[iD, p["c"]] for x, p in s.pos.items()}
        traded = sum(abs(tgt - cur.get(x, 0.0)) for x in U) + sum(v for x, v in cur.items() if x not in U)
        fee = C * traded
        for x in list(s.pos):
            if x not in U: s.ev.append((iD, s.pos[x]["c"], -s.pos[x]["u"], "core")); s.sell_val[k] += cur[x]; del s.pos[x]
        for x in U:
            new = (tgt - fee / len(U)) / T[iD, cidx[x]]
            old = s.pos[x]["u"] if x in s.pos else 0.0
            s.ev.append((iD, cidx[x], new - old, "core")); s.pos[x] = dict(u=new, c=cidx[x], sleeve="core")
            d = tgt - cur.get(x, 0.0)
            s.buy_amt[k] += max(d, 0); s.sell_val[k] += max(-d, 0)
        s.fees[k] = fee; s.nhold[k] = len(U)

def nav_from(R):
    Um = np.zeros((N, len(cols)))
    for i, c, u, _ in R.ev: Um[i, c] += u
    Um = np.cumsum(Um, axis=0)
    nav = (Um * R.T).sum(axis=1)
    return Um, nav

def unit_price(nav, nav_pre):
    """Unit value series from the first deposit: deposit buys units at the pre-flow unit price, so costs fall on performance."""
    uu, price = 0.0, np.full(N, np.nan)
    for k in range(K):
        iD = ID[k]
        Ppre = nav_pre[k] / uu if uu > 0 else 1.0
        uu += DEP / Ppre
        hi = ID[k + 1] if k + 1 < K else N
        price[iD:hi] = nav[iD:hi] / uu
    return price

kse = pd.read_csv(ROOT / "data/macro/kse100.csv", parse_dates=["date"]).set_index("date").close.reindex(dates).ffill().values
def kse_run():
    nav, nav_pre, units = np.full(N, np.nan), np.zeros(K), 0.0
    for k in range(K):
        iD = ID[k]
        nav_pre[k] = units * kse[iD]
        units += DEP / kse[iD]
        hi = ID[k + 1] if k + 1 < K else N
        nav[iD:hi] = units * kse[iD:hi]
    return nav, nav_pre

# ================================================================ statistics
def xirr(flows):
    d0 = flows[0][0]
    f = lambda r: sum(a / (1 + r) ** ((d - d0).days / 365.0) for d, a in flows)
    return brentq(f, -0.95, 20)

def stats(nav, nav_pre, fees=None, R=None, label=""):
    price = unit_price(nav, nav_pre)
    p0, yrs = price[ID[0]], (LAST - dates[ID[0]]).days / 365.25
    flows = [(dates[ID[k]], -DEP) for k in range(K)] + [(LAST, nav[-1])]
    pv = pd.Series(price, dates)
    me = pv.iloc[[IF[k] for k in range(K)]]                     # month-end unit values (F_k)
    r12 = (me / me.shift(12) - 1).dropna()
    dd = (pv.dropna() / pv.dropna().cummax() - 1)
    d = dict(label=label, nav=nav[-1], cagr=(price[-1] / p0) ** (1 / yrs) - 1, irr=xirr(flows), mdd=dd.min(), mdd_date=dd.idxmin(), w12=r12.min(), w12_end=r12.idxmin(), price=pv, yrs=yrs)
    d["twr_all"] = price[-1] / p0 - 1
    return d

def cagr_between(price, a, b):
    pa, pb = price.asof(a), price.asof(b)
    return (pb / pa) ** (365.25 / (b - a).days) - 1

def trades_df(R):
    rows = list(R.log)
    for s, p in R.pos.items():
        mark = p["u"] * R.T[-1, p["c"]] * (1 - C)
        rows.append(dict(strategy=R.name, sleeve=p["sleeve"], symbol=s, entry=dates[p["ie"]], exit=pd.NaT, ie=p["ie"], ix=N - 1, cost=p["cost"], proceeds=p["proc"] + mark,
                         ret=(p["proc"] + mark) / p["cost"] - 1, sessions=N - 1 - p["ie"], nbuys=p["nb"], status="open", reason="open", k_entry=p["ke"], sig=p.get("sig")))
    return pd.DataFrame(rows)

def tstat(x):
    x = np.asarray(x, float)
    if not len(x): return dict(n=0, hit=np.nan, med=np.nan, mean=np.nan, worst=np.nan)
    return dict(n=len(x), hit=(x > 0).mean(), med=np.median(x), mean=x.mean(), worst=x.min())

def placebo(tr, basis, n=1000, names=None, rg=None):
    """1,000 sets of random U(t) names on the same entry dates and the same exits (lump-sum, net of 0.5% round trip).
    names: AUDIT option, draw only from these (the signal's own survivor-selected pool)."""
    T = TRI[basis]
    if not len(tr): return None
    act = np.array([T[r.ix, cidx[r.symbol]] / T[r.ie, cidx[r.symbol]] * (1 - C) / (1 + C) - 1 for r in tr.itertuples()])
    R_ = np.zeros((len(tr), n))
    for j, r in enumerate(tr.itertuples()):
        pool_ = [s for s in M[r.k_entry]["U"] if s != r.symbol and np.isfinite(closeV[r.ie, cidx[s]]) and (names is None or s in names)]
        cs = (rng if rg is None else rg).choice([cidx[s] for s in pool_], n)
        R_[j] = T[r.ix, cs] / T[r.ie, cs] * (1 - C) / (1 + C) - 1
    sm = np.median(R_, axis=0)
    return dict(n=len(tr), actual=np.median(act), placebo=np.median(sm), diff=np.median(act) - np.median(sm), pct=(sm < np.median(act)).mean(), p5=np.percentile(sm, 5), p95=np.percentile(sm, 95),
                act_mean=act.mean(), pl_mean=R_.mean())

# ================================================================ driver
def run_all(basis, vmode, sat=True, excl=False, pool=None, cstop=False):
    set_pool(pool)
    first = build_val(vmode)
    ew, cum, sigs = build_feat(basis)
    res = {}
    for st in ("B0", "B1", "S2", "S3", "S4"):
        R = Run(st, basis, vmode, sat, excl, cstop)
        for k in range(K): step(R, st, k, sigs)
        Um, nav = nav_from(R)
        chk = [R.nav_pre[k] + DEP - R.fees[k] - (Um[ID[k]] * R.T[ID[k]]).sum() for k in range(K)]
        assert max(abs(x) for x in chk) < 1e-4 * DEP, max(abs(x) for x in chk)
        res[st] = dict(R=R, Um=Um, nav=nav, stats=stats(nav, R.nav_pre, label=st), trades=trades_df(R))
    E = EWRun("EW", basis, vmode)
    for k in range(K): E.step(k)
    Um, nav = nav_from(E)
    res["EW"] = dict(R=E, Um=Um, nav=nav, stats=stats(nav, E.nav_pre, label="EW KMI"), trades=pd.DataFrame())
    nav, npre = kse_run()
    res["KSE"] = dict(nav=nav, stats=stats(nav, npre, label="KSE100"), trades=pd.DataFrame(), R=None)
    res["_first"], res["_sigs"], res["_ew"] = first, sigs, (ew, cum)
    return res

def sat_note(): return "no sponsor satellite (data/insider_trades.csv absent)"


# ================================================================ report
def df_out(df, **kw): out(df.to_string(index=False, **kw))

def episodes(labels):
    o, start = [], 0
    for k in range(1, K + 1):
        if k == K or labels[k] != labels[start]:
            o.append((labels[start], M[start]["F"].strftime("%Y-%m"), M[k - 1]["F"].strftime("%Y-%m"), k - start)); start = k
    return o

def cov_tables():
    rows = []
    insym = set(e.symbol)
    for Y in range(2018, 2027):
        den = dated = strict = infile = 0
        for m in M:
            F = m["F"]
            if F.year != Y or F.month not in (3, 6, 9, 12): continue
            qe = F.to_period("M").end_time.normalize()
            if qe >= pd.Timestamp("2026-09-30"): continue                    # September 2026 results are not yet due
            g = e[e.qe == qe]
            den += len(m["U"]); infile += sum(s in insym for s in m["U"])
            dated += len(set(m["U"]) & set(g[g.dated].symbol)); strict += len(set(m["U"]) & set(g[g.yoy_ok].symbol))
        rows.append(dict(year=Y, name_quarters=den, in_eps_file=infile, dated_rows=dated, with_yoy=strict, cov_dated=dated / den if den else np.nan, cov_yoy=strict / den if den else np.nan))
    d = pd.DataFrame(rows)
    d["flag"] = np.where(d.name_quarters == 0, "n/a", np.where(d.cov_dated < 0.7, "UNCOVERED", "covered"))
    return d

def main():
    out("== SYSTEM WALK-FORWARD (B0, B1, S2, S3, S4), run 2026-10-17. Pre-registered rules: knowledge/playbooks/strategy_candidates.md")
    out(f"Panel {close.shape[0]} days x {close.shape[1]} symbols, {dates[0].date()} to {LAST.date()}. Months K={K} (deposits {K} x Rs{DEP:,.0f} = Rs{K * DEP:,.0f}); first trade {dates[ID[0]].date()} (formed {dates[IF[0]].date()}), last trade {dates[ID[-1]].date()}; valued at {LAST.date()} close.")
    out(f"Costs {C:.2%} per side. Dividends: cash from data/corporate_actions.csv at 85% (15% withholding), reinvested through the total-return index. Cash dividends are complete only from Nov 2024: before that the strategies and EW KMI are close to price return, and KSE100 is price only.")
    res = run_all("TR", "frozen")
    first = res["_first"]
    sigs = res["_sigs"]
    # ---------------------------------------------------------------- data flags
    out("\n== 1. DATA AND COVERAGE FLAGS")
    nd = sum(m["F"] < pd.Timestamp("2019-01-28") for m in M)
    out(f"KMI membership: {len(LISTS)} lists ({LDATES[0].date()} to {LDATES[-1].date()}); the {nd} formations before 28 Jan 2019 use KMI_ALL_derived_2019-01-28.csv (APPROXIMATION: names that left earlier are missing); later ones use the latest derived list plus index_changes.csv (psx.com.pk rows only); 2026 uses the exact 2026-06-05 list. Derived lists sit 0 to 7 names from notice totals.")
    us = pd.Series([len(m["U"]) for m in M], [m["F"].year for m in M])
    out("U(t) size by formation year (min/mean/max): " + "; ".join(f"{y}: {g.min()}/{g.mean():.0f}/{g.max()}" for y, g in us.groupby(level=0)))
    nos = [sum(s not in SEC for s in m["U"]) for m in M]
    out(f"Names in U(t) with no sector code: mean {np.mean(nos):.1f}, max {max(nos)}. Eligible sectors (3+ names) per month: mean {np.mean([len(m['elig']) for m in M]):.1f}, min {min(len(m['elig']) for m in M)}, max {max(len(m['elig']) for m in M)}.")
    out("B1 regime (6M cut-off minus policy rate, +-50bp): months " + str(dict(collections.Counter(m["b1"] for m in M))))
    out("S3 regime: months " + str(dict(collections.Counter(m["s3"] for m in M))))
    out("S3 regime episodes: " + "; ".join(f"{a} {b}..{c} ({n}m)" for a, b, c, n in episodes([m["s3"] for m in M])))
    out("B1 regime episodes: " + "; ".join(f"{a} {b}..{c} ({n}m)" for a, b, c, n in episodes([m["b1"] for m in M])))
    out(f"Value inputs: sa_ratios fiscal-year rows {len(fy)} for {fy.t.nunique()} names (FY by year: {fy.fye.dt.year.value_counts().sort_index().to_dict()}); matched to an annual-result announcement {(fy.i_ann >= 0).sum()}, fallback FYE+4 months {(fy.i_ann < 0).sum()}.")
    nv = lambda d: next(m['nval'] for m in M if m['F'].strftime('%Y-%m') == d)
    out(f"First month with 15 or more value-eligible names in U(t): {M[first]['F'].strftime('%b %Y')} formation (frozen text said about Oct 2020; the data say later because sa_ratios holds only 2 FY2020 and 28 FY2021 rows). Value-eligible names in U(t) at Dec 2020 / Dec 2021 / Dec 2022 / Sep 2026: "
        + " / ".join(str(nv(d)) for d in ("2020-12", "2021-12", "2022-12", "2026-09")))
    out(f"Before that month, B1 and the S2/S3/S4 cores hold EW of the chosen sectors' liquid names (fallback rule). Lesson 9: the value half of the test covers only {K - first} months of a market that rerated 2022-25.")
    out(f"Quarterly EPS: {len(e)} rows, {e.symbol.nunique()} names; dated after re-join {int(e.dated.sum())}; with a year-ago comparator {int(e.yoy_ok.sum())}. Consolidation status UNVERIFIED (lesson 1). Blowout signals (>=+50% YoY or loss to profit) {len(sigs)}, of which flat vs market in the 20 sessions {sum(g['flat'] for g in sigs)}.")
    ct = cov_tables()
    out("Name-quarter coverage of the EPS series (liquid KMI name-quarters at calendar quarter-ends; September 2026 quarter excluded, not yet due). Under 70% = UNCOVERED:")
    df_out(ct.assign(cov_dated=ct.cov_dated.map(lambda x: f"{x:.0%}"), cov_yoy=ct.cov_yoy.map(lambda x: f"{x:.0%}")))
    unc = ct[ct.flag == "UNCOVERED"].year.tolist()
    out("Satellite (earnings-blowout) UNCOVERED years: " + str(unc) + ". Signals still trade where they exist (they are point-in-time); no other signal is substituted.")
    out("Sponsor-buying satellite: data/insider_trades.csv " + ("EXISTS but this script does not parse it" if (ROOT / "data/insider_trades.csv").exists() else "is ABSENT") + ". S3 and S4 therefore run as 'no sponsor satellite': S3 is core only; S4 satellite is the earnings-blowout signal only.")
    # ---------------------------------------------------------------- headline
    out("\n== 2. HEADLINE (frozen rules, total-return basis, 15% withholding on known cash dividends)")
    names = ["B0", "B1", "S2", "S3", "S4", "EW", "KSE"]
    lab = {"B0": "B0 buy market", "B1": "B1 orchestrator", "S2": "S2 momentum+blowout", "S3": "S3 regime (no sponsor sat)", "S4": "S4 full (no sponsor sat)", "EW": "EW liquid KMI (rebal.)", "KSE": "KSE100 price index, no costs"}
    b0 = res["B0"]["stats"]["nav"]
    rows = []
    for n in names:
        s = res[n]["stats"]
        rows.append(dict(strategy=lab[n], final_Rs=rs(s["nav"]), x_deposits=f"{s['nav'] / (K * DEP):.2f}", vs_B0=f"{s['nav'] / b0:.3f}", TWR_CAGR=pc(s["cagr"]), IRR=pc(s["irr"]), maxDD=pc(s["mdd"]), DD_trough=s["mdd_date"].strftime("%Y-%m-%d"),
                         worst12m=pc(s["w12"]), w12_end=s["w12_end"].strftime("%Y-%m")))
    df_out(pd.DataFrame(rows))
    out(f"Deposits total Rs{K * DEP:,.0f}. TWR CAGR is of the unit value from {dates[ID[0]].date()} (costs fall on performance). IRR is money-weighted. Worst 12m is the worst rolling 12 months of month-end unit values (F_k).")
    # trades
    out("\nTrade statistics (net of 0.5% round trip; trade = first buy to full exit; dividends reinvested inside the return; open trades marked at 16 Oct 2026, net of exit fee):")
    rows = []
    for n in ("B0", "B1", "S2", "S3", "S4"):
        tr = res[n]["trades"]; cl, op = tr[tr.status == "closed"], tr[tr.status == "open"]
        a, b_, c_ = tstat(cl.ret), tstat(op.ret), tstat(tr.ret)
        R = res[n]["R"]; yrs = res[n]["stats"]["yrs"]
        avgnav = np.mean([res[n]["nav"][ID[k]] for k in range(K)])
        rows.append(dict(strategy=n, closed_n=a["n"], closed_hit=pc(a["hit"], 0), closed_median=pc(a["med"]), closed_mean=pc(a["mean"]), closed_worst=pc(a["worst"]), open_n=b_["n"], open_hit=pc(b_["hit"], 0), open_median=pc(b_["med"]),
                         all_n=c_["n"], all_hit=pc(c_["hit"], 0), all_median=pc(c_["med"]), avg_names=f"{R.nhold.mean():.1f}", sell_turnover_pa=f"{R.sell_val.sum() / avgnav / yrs:.0%}", fees_Rs=rs(R.fees.sum())))
    df_out(pd.DataFrame(rows))
    out("Closed-trade exit reasons: " + "; ".join(f"{n}: {dict(collections.Counter(res[n]['trades'].reason))}" for n in ("B1", "S2", "S3", "S4")))
    out("\nBy sleeve (P&L = proceeds + open mark - cost, summed over trades; ret_on_cost = P&L / cost):")
    rows = []
    for n in ("B1", "S2", "S3", "S4"):
        tr = res[n]["trades"]
        for sl, g in tr.groupby("sleeve"):
            cl = g[g.status == "closed"]
            a = tstat(cl.ret)
            rows.append(dict(strategy=n, sleeve=sl, closed_n=a["n"], hit=pc(a["hit"], 0), median=pc(a["med"]), mean=pc(a["mean"]), worst=pc(a["worst"]), open_n=int((g.status == "open").sum()), cost_Rs=rs(g.cost.sum()), PnL_Rs=rs((g.proceeds - g.cost).sum()), ret_on_cost=pc((g.proceeds.sum() - g.cost.sum()) / g.cost.sum())))
    df_out(pd.DataFrame(rows))
    # year by year
    out("\n== 3. YEAR BY YEAR: Rs value of the Rs50k/month deposits at each 31 Dec (and 16 Oct 2026) vs KSE100 and EW KMI")
    ends = [dates[int(dates.searchsorted(pd.Timestamp(f"{y}-12-31"), side="right")) - 1] for y in range(2018, 2026)] + [LAST]
    kp, ep = res["KSE"]["stats"]["price"], res["EW"]["stats"]["price"]
    for n in ("B0", "B1", "S2", "S3", "S4"):
        rows, pp = [], res[n]["stats"]["price"]
        prev = None
        for d in ends:
            i = dates.get_loc(d); dep = sum(ID[k] <= i for k in range(K)) * DEP
            ps = pp.asof(d); yr = (ps / pp.asof(prev) - 1) if prev is not None else (ps / pp.iloc[ID[0]] - 1)
            ky = (kp.asof(d) / kp.asof(prev) - 1) if prev is not None else (kp.asof(d) / kp.iloc[ID[0]] - 1)
            rows.append(dict(date=d.strftime("%Y-%m-%d"), deposited=rs(dep), strategy=rs(res[n]["nav"][i]), KSE100=rs(res["KSE"]["nav"][i]), EW_KMI=rs(res["EW"]["nav"][i]), vs_KSE=f"{res[n]['nav'][i] / res['KSE']['nav'][i]:.2f}",
                             vs_EW=f"{res[n]['nav'][i] / res['EW']['nav'][i]:.2f}", year_TWR=pc(yr), KSE_yr=pc(ky)))
            prev = d
        out(f"-- {n}"); df_out(pd.DataFrame(rows))
    # splits
    out("\n== 4. SPLITS (time-weighted CAGR of unit value) and the value-data period")
    d21, d_first = pd.Timestamp("2021-12-31"), dates[ID[first]]
    rows = []
    for n in names:
        pp = res[n]["stats"]["price"]; p2 = pp[pp.index >= d_first].dropna()
        rows.append(dict(strategy=lab[n], CAGR_2018_2021=pc(cagr_between(pp, dates[ID[0]], d21)), CAGR_2022_2026=pc(cagr_between(pp, d21, LAST)), **{f"CAGR_from_{d_first:%Y-%m}": pc(cagr_between(pp, d_first, LAST)), f"maxDD_from_{d_first:%Y-%m}": pc((p2 / p2.cummax() - 1).min())}))
    df_out(pd.DataFrame(rows))
    out(f"From {d_first:%Y-%m} the value inputs are live (15+ eligible names); before it B1, S2 and the cores of S3/S4 run on the EW-of-chosen-sectors fallback. Lesson 9: 2022 to 2025 carries the rerating tailwind; the Oct 2025 to Oct 2026 cohort was flat to negative for value.")
    # satellite
    out("\n== 5. EARNINGS-BLOWOUT SATELLITE (S2 and S4) AND PLACEBO")
    plres = {}
    for n in ("S2", "S4"):
        tr = res[n]["trades"]; sat = tr[tr.sleeve == "sat"]
        out(f"-- {n}: satellite trades {len(sat)} (closed {int((sat.status == 'closed').sum())}, open {int((sat.status == 'open').sum())}); by entry year " + str(dict(collections.Counter(sat.entry.dt.year))) + "; in UNCOVERED years: " + str(int(sat.entry.dt.year.isin(unc).sum())))
        a = tstat(sat.ret); out(f"   trade return (net, as defined): n {a['n']}, hit {pc(a['hit'], 0)}, median {pc(a['med'])}, mean {pc(a['mean'])}, worst {pc(a['worst'])}")
        pl = placebo(sat, "TR"); plres[n] = pl
        if pl:
            out(f"   Placebo (1,000 sets, one random U(t) name per trade, same entry day and same exit, lump-sum, net of 0.5%): actual median {pc(pl['actual'])} vs placebo median {pc(pl['placebo'])} (5th-95th pct of set medians {pc(pl['p5'])} to {pc(pl['p95'])}); difference {pc(pl['diff'], 2)}; actual above {pl['pct']:.0%} of placebo sets; mean actual {pc(pl['act_mean'])} vs placebo {pc(pl['pl_mean'])}. Signal {'ABANDONED (<= 0)' if pl['diff'] <= 0 else 'survives the placebo test'}.")
        pf = placebo(sat, "TR", names=EPSSET, rg=np.random.default_rng(SEED + 1))   # own stream: headline placebo unchanged
        if pf: out(f"   AUDIT placebo drawn only from quarterly_eps names (the signal's own survivor pool): placebo median {pc(pf['placebo'])}, difference {pc(pf['diff'], 2)}, actual above {pf['pct']:.0%} of sets -> {'fails' if pf['diff'] <= 0 else 'passes'}")
        out("   by exit reason (count, median): " + str(sat.groupby('reason').ret.agg(['count', 'median']).round(3).to_dict('index')))
    out("-- Signal-level placebo not applicable to S3: no sponsor satellite.")
    # abandonment
    out("\n== 6. ABANDONMENT TESTS (value at 16 Oct 2026, frozen)")
    v = {n: res[n]["stats"]["nav"] for n in names}
    def verdict(n, thr, base, bname):
        r = v[n] / base
        out(f"{n}: Rs{v[n]:,.0f} / {bname} Rs{base:,.0f} = {r:.3f} (threshold {thr:.2f}) -> {'SURVIVES' if r >= thr else 'ABANDON'}")
    out("B0: bar, never abandoned.")
    verdict("B1", 1.00, v["B0"], "B0"); verdict("S2", 1.05, v["B0"], "B0"); verdict("S3", 1.10, v["B0"], "B0")
    verdict("S4", 1.00, max(v["S2"], v["S3"]), "better of S2 and S3")
    for n in ("S2", "S4"):
        if plres.get(n) and plres[n]["diff"] <= 0: out(f"{n}: satellite signal fails the placebo (median trade minus placebo <= 0) -> signal abandoned whatever the strategy does.")
    out("S3 sponsor-buying signal: not tested (no insider_trades.csv). S3 and S4 verdicts are for 'no sponsor satellite' versions; the S3 sector lists were read off 2018-2026 windows (partly in-sample), so S3 is an upper bound.")
    out(f"Also: B0 is {v['B0'] / v['KSE']:.2f}x KSE100 and {v['B0'] / v['EW']:.2f}x EW KMI; best strategy {max(names[:5], key=lambda n: v[n])} is {max(v[n] for n in names[:5]) / v['KSE']:.2f}x KSE100.")
    # variants
    out("\n== 7. VARIANTS (POST-HOC, not headline). Final Rs / TWR CAGR / ratio to that variant's B0")
    for tag, basis, vm, sat, ex, cs in (("A. price-return basis (no cash dividends at all)", "PR", "frozen", True, False, False), ("B. value lag = later of announcement and FYE+3m (task wording)", "TR", "task", True, False, False),
                                    ("C. satellite switched off (S2 and S4 core only)", "TR", "frozen", False, False, False), ("D. a trimmed name gets no new money in the month it is trimmed", "TR", "frozen", True, True, False),
                                    ("E. AUDIT: 25% trailing stop on core names (month-end check), stopped name blocked 3 months", "TR", "frozen", True, False, True)):
        rv = run_all(basis, vm, sat, ex, cstop=cs)
        out(f"-- {tag}; first value month {M[rv['_first']]['F']:%b %Y}")
        rows = []
        for n in names:
            s = rv[n]["stats"]
            rows.append(dict(strategy=n, final_Rs=rs(s["nav"]), TWR_CAGR=pc(s["cagr"]), vs_B0=f"{s['nav'] / rv['B0']['stats']['nav']:.3f}", maxDD=pc(s["mdd"])))
        df_out(pd.DataFrame(rows))
        vv = {n: rv[n]["stats"]["nav"] for n in names}
        out(f"   verdicts: B1 {vv['B1'] / vv['B0']:.3f} ({'ok' if vv['B1'] >= vv['B0'] else 'abandon'}); S2 {vv['S2'] / vv['B0']:.3f} ({'ok' if vv['S2'] >= 1.05 * vv['B0'] else 'abandon'}); S3 {vv['S3'] / vv['B0']:.3f} ({'ok' if vv['S3'] >= 1.10 * vv['B0'] else 'abandon'}); S4 vs best(S2,S3) {vv['S4'] / max(vv['S2'], vv['S3']):.3f} ({'ok' if vv['S4'] >= max(vv['S2'], vv['S3']) else 'abandon'})")
        if cs: out("   core_trail exits: " + "; ".join(f"{n} {int((rv[n]['trades'].reason == 'core_trail').sum())}" for n in ("S2", "S3", "S4")))
    # audit: same-pool comparison
    out("\n== 8. AUDIT (Opus, 2026-10-17): SURVIVOR-SELECTED PICK POOL. sa_ratios and quarterly_eps names were chosen on 2026 liquidity; B0 holds all of U(t).")
    rows = []
    for k in range(K - 1):
        a, b = ID[k], ID[k + 1]
        for s in M[k]["U"]:
            c = cidx[s]
            if TRI["TR"][a, c] > 0: rows.append((M[k]["F"], TRI["TR"][b, c] / TRI["TR"][a, c] - 1, s in POOL))
    dd_ = pd.DataFrame(rows, columns=["F", "r", "pool"])
    for lab_, g in (("2018-01 to 2022-07", dd_[dd_.F < "2022-08-01"]), ("2022-08 to 2026-09", dd_[dd_.F >= "2022-08-01"])):
        mm = g.groupby(["F", "pool"]).r.mean().unstack(); df_ = mm[True] - mm[False]
        out(f"   {lab_}: pool share of U(t) {g.pool.mean():.0%}; monthly EW(pool) - EW(rest) mean {pc(df_.mean(), 2)}, median {pc(df_.median(), 2)}, t {df_.mean() / df_.std() * np.sqrt(len(df_)):.2f}, compounded ratio {(1 + mm[True]).prod() / (1 + mm[False]).prod():.2f}")
    rp = run_all("TR", "frozen", pool=POOL)
    out(f"-- Every strategy re-run with U(t) restricted to the pick pool ({len(POOL)} names: sa_ratios or quarterly_eps); B0' and EW' hold the same pool. First value month {M[rp['_first']]['F']:%b %Y}.")
    rows = []
    for n in names:
        s, s0 = rp[n]["stats"], res[n]["stats"]
        rows.append(dict(strategy=n, frozen_Rs=rs(s0["nav"]), frozen_vs_B0=f"{s0['nav'] / b0:.3f}", frozen_vs_poolB0=f"{s0['nav'] / rp['B0']['stats']['nav']:.3f}", pool_Rs=rs(s["nav"]), pool_CAGR=pc(s["cagr"]), pool_vs_poolB0=f"{s['nav'] / rp['B0']['stats']['nav']:.3f}", pool_maxDD=pc(s["mdd"])))
    df_out(pd.DataFrame(rows))
    vv = {n: rp[n]["stats"]["nav"] for n in names}
    out(f"   pool verdicts: B1 {vv['B1'] / vv['B0']:.3f} ({'ok' if vv['B1'] >= vv['B0'] else 'abandon'}); S2 {vv['S2'] / vv['B0']:.3f} ({'ok' if vv['S2'] >= 1.05 * vv['B0'] else 'abandon'}); S3 {vv['S3'] / vv['B0']:.3f} ({'ok' if vv['S3'] >= 1.10 * vv['B0'] else 'abandon'}); S4 vs best(S2,S3) {vv['S4'] / max(vv['S2'], vv['S3']):.3f} ({'ok' if vv['S4'] >= max(vv['S2'], vv['S3']) else 'abandon'})")
    for n in ("S2", "S4"):
        sat = rp[n]["trades"][rp[n]["trades"].sleeve == "sat"]
        pl = placebo(sat, "TR", names=EPSSET, rg=np.random.default_rng(SEED + 2))
        if pl: out(f"   {n} satellite in pool run: n {pl['n']}, actual median {pc(pl['actual'])}, placebo (quarterly_eps names) {pc(pl['placebo'])}, difference {pc(pl['diff'], 2)} -> {'fails' if pl['diff'] <= 0 else 'passes'}")
    pd.concat([rp[n]["trades"] for n in ("B0", "B1", "S2", "S3", "S4")]).drop(columns=["ie", "ix", "k_entry"]).assign(sig=lambda x: x.sig.astype(str)).to_csv(ROOT / "tests/out/walkforward_trades_pool.csv", index=False)
    set_pool(None)
    # files
    allt = pd.concat([res[n]["trades"].drop(columns=["ie", "ix", "k_entry"]) for n in ("B0", "B1", "S2", "S3", "S4")])
    allt["sig"] = allt.sig.astype(str)
    allt.to_csv(ROOT / "tests/out/walkforward_trades.csv", index=False)
    h = pd.DataFrame([r for n in ("B0", "B1", "S2", "S3", "S4") for r in res[n]["R"].hold_rows], columns=["strategy", "trade_date", "symbol", "sleeve", "units", "value_Rs"])
    h["weight"] = h.value_Rs / h.groupby(["strategy", "trade_date"]).value_Rs.transform("sum")
    h.to_csv(ROOT / "tests/out/walkforward_holdings.csv", index=False)
    out(f"\nWrote tests/out/walkforward_trades.csv ({len(allt)} rows) and walkforward_holdings.csv ({len(h)} rows).")
    (ROOT / "tests/out/system_walkforward.txt").write_text(buf.getvalue(), encoding="utf-8")


if __name__ == "__main__":
    main()
