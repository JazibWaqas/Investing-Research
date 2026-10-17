"""Disclosed insider trading on PSX: cluster buying (H1), role (H2), round trips (H3), selling (H4).
Run: .venv/Scripts/python.exe -I scripts/tests/insider_cluster_buying.py
Reads data/insider_pdf_reads.txt (a hand transcription of the 497 sampled PDFs; see data/INSIDER_TRADES_NOTES.md),
writes data/insider_trades.csv and tests/out/insider_cluster_buying.txt. Write-up: tests/insider_cluster_buying.md.
Point in time: an event is the announcement timestamp; entry is the close of the first tradable session; costs 0.5% round trip.
"""
import sys, io, re, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
def fp(x, d=1):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:+.{d}%}"
def fq(x, d=1):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}%}"
def fn(x, d=2):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}"

COST, SEED, LAST = 0.005, 20261017, pd.Timestamp("2026-10-16")
HZ = (21, 63, 126)
IS = (pd.Timestamp("2019-01-01"), pd.Timestamp("2023-12-31"))
OOS = (pd.Timestamp("2024-01-01"), LAST)
D30, D180 = pd.Timedelta(days=30), pd.Timedelta(days=180)
READS = ROOT / "data" / "insider_pdf_reads.txt"
ROLE = {"S": "sponsor_substantial", "D": "director_ceo", "E": "executive", "O": "other", "U": "unknown"}
DIRN = {"B": "buy", "S": "sell", "U": "unknown"}
MODE = {"m": "market", "r": "rights", "b": "bonus", "e": "esop", "g": "gift_inherit_transfer", "x": "off_market_block",
        "t": "tender", "p": "pledge", "o": "other", "u": "unstated"}

# ================================================================= 1. sample, parse, trades table
smp = pd.read_csv(ROOT / "data" / "insider_sample.csv", dtype={"doc": str})
smp["ann"] = pd.to_datetime(smp.datetime, utc=True).dt.tz_convert("Asia/Karachi").dt.tz_localize(None)
annd = dict(zip(smp.doc, smp.ann)); symd = dict(zip(smp.doc, smp.symbol)); blockd = dict(zip(smp.doc, smp.block))
drawn = list(pd.read_csv(ROOT / "data" / "insider_drawn_symbols.csv").symbol)

TITLES = {"MR", "MRS", "MS", "DR", "MISS"}
ALIAS = {"BOO ALI": "BOO ALI SIDDIQUI", "MUHAMMAD NAUMAN": "MUHAMMAD NAUMAN ALI", "MR ZEESHAN KHAWAR": "ZEESHAN KHAWAR"}
def norm(h):
    s = re.sub(r"[^A-Z0-9 ]", " ", h.upper().replace("-", " "))
    s = " ".join(t for t in s.split() if t not in TITLES)
    return ALIAS.get(s, s)

raw_lines, docs_notrade = [], []
for ln in READS.read_text(encoding="utf-8").splitlines():
    if not ln or ln[0] == "#":
        continue
    f = ln.split("|")
    doc, meth, holder, role, d, mode, trades = f[:7]; note = "|".join(f[7:])
    raw_lines.append(dict(doc=doc, meth=meth, holder=holder, role=role, d=d, mode=mode, trades=trades, note=note))
RL = pd.DataFrame(raw_lines)
assert set(RL.doc) == set(smp.doc), "every sampled PDF must have a transcription"
byfirst = RL.drop_duplicates("doc").set_index("doc").trades.to_dict()
rows = []
for r in RL.itertuples():
    if r.holder == "NONE":
        docs_notrade.append((r.doc, r.note)); continue
    tr = r.trades
    if tr.startswith("="):
        tr = byfirst[tr[1:]]
    for k, t in enumerate(tr.split(",")):
        m = re.match(r"(\?|\d{8}):(\?|\d+)@(\?|[\d.]+)", t)
        assert m, (r.doc, t)
        td = pd.NaT if m[1] == "?" else pd.Timestamp(m[1])
        sh = np.nan if m[2] == "?" else float(m[2]); px = np.nan if m[3] == "?" else float(m[3])
        rows.append(dict(doc_id=r.doc, line=k, ann_datetime=annd[r.doc], symbol=symd[r.doc], holder_name=r.holder, holder_norm=norm(r.holder),
                         role=ROLE[r.role], direction=DIRN[r.d], mode=MODE[r.mode], trade_date=td, shares=sh,
                         price=px if px != 0 else np.nan, source="pdf_text" if r.meth == "T" else "pdf_eye", note=r.note))
T = pd.DataFrame(rows).sort_values(["ann_datetime", "doc_id", "line"]).reset_index(drop=True)
T["value_rs"] = T.shares * T.price

# role fill: a person's role is a fact about the person; fill 'unknown' from the same holder's stated role in the same symbol
known = T[T.role != "unknown"].groupby(["symbol", "holder_norm"]).role.agg(lambda s: s.value_counts().index[0])
fill = [(s, h) in known.index for s, h in zip(T.symbol, T.holder_norm)]
isu = (T.role == "unknown") & np.array(fill)
nfilled = int(isu.sum())
T.loc[isu, "role"] = [known[(s, h)] for s, h in zip(T.symbol[isu], T.holder_norm[isu])]
T.loc[isu, "note"] = T.note[isu] + " | role filled from the same holder's other filings"

# dedupe: key (symbol, holder_norm, trade_date, direction, shares); the earliest document keeps the trade, later documents' copies get dup_of
T["dup_of"] = ""
T["_k"] = list(zip(T.symbol, T.holder_norm, T.trade_date, T.direction, T.shares))
ok = T.trade_date.notna() & T.shares.notna()
for k, g in T[ok].groupby("_k", sort=False):
    docs = list(dict.fromkeys(g.doc_id))
    if len(docs) < 2:
        continue
    n0 = (g.doc_id == docs[0]).sum()
    for dd in docs[1:]:
        idx = g.index[g.doc_id == dd][:n0]
        T.loc[idx, "dup_of"] = docs[0]
T["revoked"] = 0
T.loc[T.doc_id.isin(["181996"]), "note"] += " | corrected re-filing of 181992 (share count 100,000 vs 10,000 at 10.40); both kept, different key"
T["qual_mode"] = T["mode"].isin(["market", "unstated"])
T["qual"] = T.qual_mode & T.direction.isin(["buy", "sell"]) & (T.dup_of == "")
T.drop(columns=["_k", "qual_mode"]).to_csv(ROOT / "data" / "insider_trades.csv", index=False)

# ================================================================= 2. prices, returns, engine
close, vol, tv = P.load_panel()
dates, N = close.index, len(close.index)
cols = list(close.columns); cidx = {s: i for i, s in enumerate(cols)}
acts_nc = P.load_actions().query("type!='cash'")
ret = P.returns(close, "adjusted", actions=acts_nc)
mkt = P.ew_market(ret)
liq = (P._med_tv(tv) > 5e6).reindex(index=dates, columns=cols, fill_value=False).values
traded = close.notna().values
cum = (1 + ret.fillna(0)).cumprod().where(close.notna().cummax()).values
cnt = close.notna().cumsum().values
cm = (1 + mkt.reindex(dates).fillna(0)).cumprod().values

def win(sym, ia, ib):
    """excess return close(ia)->close(ib) over the market; code 0 ok, 1 window outside the panel, 2 no observation in the window"""
    ia, ib, sym = np.asarray(ia), np.asarray(ib), np.asarray(sym)
    inc = (ia < 0) | (ib >= N) | (ia >= ib)
    a, b = np.clip(ia, 0, N - 1), np.clip(ib, 0, N - 1)
    nobs = cnt[b, sym] - cnt[a, sym]
    v = (cum[b, sym] / cum[a, sym] - 1) - (cm[b] / cm[a] - 1)
    code = np.where(inc, 1, np.where((nobs <= 0) | np.isnan(v), 2, 0))
    return np.where(code == 0, v, np.nan), code

# sanity: vectorised liquidity screen equals prices.liquid_universe on three dates
for dt_ in ("2021-06-15", "2024-03-01", "2026-10-16"):
    k = dates.searchsorted(pd.Timestamp(dt_))
    a_ = set(P.liquid_universe(dates[k])); b_ = {cols[j] for j in np.where(liq[k])[0]}
    assert a_ == b_, dt_
out(f"== INSIDER CLUSTER BUYING (PSX). Panel {close.shape} {dates[0].date()} to {dates[-1].date()}; last date {LAST.date()}; returns = bonus/split-only price returns, "
    f"benchmark = equal-weight market (Rs5m); cost {COST:.1%} round trip charged to the stock leg. Seed {SEED}.")
assert dates[-1] == LAST

def first_obs(sym, start):
    """first panel row >= start where the symbol has a close; None if none within 5 rows after start"""
    j = cidx[sym]
    for i in range(start, min(start + 6, N)):
        if traded[i, j]:
            return i
    return None

def entry_row(sym, ts, plus1=False):
    """(row, reason). Stamped before 15:30 PKT on a panel day -> that day; after 15:30 -> next day; weekends/holidays roll forward."""
    if sym not in cidx:
        return None, "no_price_series"
    d = ts.normalize(); p = dates.searchsorted(d)
    after = (ts.hour * 60 + ts.minute) >= 15 * 60 + 30
    start = p + 1 if (after and p < N and dates[p] == d) else p
    if start >= N:
        return None, "after_panel"
    e = first_obs(sym, start)
    if e is None:
        return None, "no_obs_5d"
    if plus1:
        e = first_obs(sym, e + 1)
        if e is None:
            return None, "no_obs_5d"
    return e, "ok"

# ================================================================= 3. coverage tables
ann = pd.read_parquet(ROOT / "data" / "announcements.parquet")
ins = ann[ann.klass == "insider_trade"].copy()
ins["has_doc"] = ins.document_ids.fillna("") != ""
out("\n== 1. COVERAGE")
out(f"insider_trade rows in announcements.parquet: {len(ins):,}; with a document id {ins.has_doc.sum():,} ({ins.has_doc.mean():.1%}). tags: " + str(ins.direction.value_counts().to_dict()))
insd = ins[ins.symbol.isin(drawn)]
out(f"in the {len(drawn)} drawn symbols: {len(insd):,} rows, with a document {insd.has_doc.sum():,} ({insd.has_doc.mean():.1%}); since 2019-01-01: {(insd.datetime >= '2019-01-01').sum():,} rows, with a document {(insd.has_doc & (insd.datetime >= '2019-01-01')).sum():,}")
out("drawn symbols in draw order (numpy default_rng 20261017 permutation of the liquid-KMI candidates, whole symbols added until the 500 cap would break): " + ", ".join(drawn))
bk = smp.block.value_counts().to_dict()
out(f"PDFs downloaded and read: {len(smp)} (block a, current: {bk['a_current']}; block b, backtest: {bk['b_backtest']}). parse_method pdf_text {int((RL.drop_duplicates('doc').meth == 'T').sum())}, pdf_eye {int((RL.drop_duplicates('doc').meth == 'E').sum())}")
out("  pdf_text = a usable text layer was read (113); pdf_eye = the page image was read by eye: 373 files have no text layer and 11 have a garbled one (3 of the 373 have a broken page tree that pdfplumber cannot open; their embedded JPEG was extracted and read).")
out(f"  unreadable files: 0. Files with no trade lines (logged with reason): {len(docs_notrade)}")
for d_, n_ in docs_notrade:
    out(f"    {d_} {symd[d_]} {annd[d_]:%Y-%m-%d}: {n_}")
yrs = smp.assign(y=smp.ann.dt.year).groupby("y").size()
meth = RL.drop_duplicates("doc").set_index("doc").meth
ey = smp.assign(y=smp.ann.dt.year, eye=smp.doc.map(meth) == "E").groupby("y").eye.mean()
out("PDF read method by announcement year (share read by eye): " + ", ".join(f"{y}: {ey[y]:.0%} of {yrs[y]}" for y in yrs.index))
nl = len(T); nd_ = int((T.dup_of != "").sum())
out(f"trade lines: {nl}; duplicates removed (same symbol, holder, trade date, direction and shares as an earlier document): {nd_}; unique lines {nl - nd_}; "
    f"revoked or revised: 0 filings carry an explicit revocation notice; 1 filing (181996) is a corrected re-filing of 181992 (kept, different key); roles filled from the holder's other filings: {nfilled} lines")
U = T[T.dup_of == ""]
out("unique lines by mode: " + ", ".join(f"{k} {v}" for k, v in U["mode"].value_counts().items()))
out("unique lines by direction: " + ", ".join(f"{k} {v}" for k, v in U.direction.value_counts().items()))
excl = U[U.direction.isin(["buy", "sell"]) & ~U["mode"].isin(["market", "unstated"])]
out("excluded lines (not market/unstated) by reason and direction: " + "; ".join(f"{m}: buy {int(((excl['mode']==m)&(excl.direction=='buy')).sum())}, sell {int(((excl['mode']==m)&(excl.direction=='sell')).sum())}" for m in excl["mode"].unique()))
Q = T[T.qual].copy()
out(f"qualifying lines (market or unstated, unique): buys {int((Q.direction=='buy').sum())}, sells {int((Q.direction=='sell').sum())}; distinct qualifying buyers (symbol, holder) {Q[Q.direction=='buy'].groupby(['symbol','holder_norm']).ngroups}, sellers {Q[Q.direction=='sell'].groupby(['symbol','holder_norm']).ngroups}; market-only buys {int(((Q['mode']=='market')&(Q.direction=='buy')).sum())}, sells {int(((Q['mode']=='market')&(Q.direction=='sell')).sum())}")
out("qualifying lines by role (buy/sell): " + ", ".join(f"{r}: {int(((Q.role==r)&(Q.direction=='buy')).sum())}/{int(((Q.role==r)&(Q.direction=='sell')).sum())}" for r in ROLE.values()))
# title tags vs the PDF read
tag = ins.assign(doc=ins.document_ids.fillna("").str.split(",").str[0]).query("doc in @smp.doc")
tag = tag[tag.direction.isin(["buy", "sell"])]
t174 = ins[ins.direction.isin(["buy", "sell"])]
out(f"title-tagged directions: {len(t174)} rows (buy {int((t174.direction=='buy').sum())}, sell {int((t174.direction=='sell').sum())}); {int((t174.document_ids.fillna('')!='').sum())} have a document; {int(((t174.datetime>='2019-01-01')&(t174.document_ids.fillna('')!='')).sum())} are dated 2019 on. "
    f"Only {len(tag)} falls on a sampled document ({', '.join(tag.symbol + ' ' + tag.datetime.dt.strftime('%Y-%m-%d') + ' tagged ' + tag.direction)}): a takeover book-closure notice with no trade lines, so agreement with the PDF reads cannot be assessed (0 comparable). Most tags are on 2015-2018 takeover-regulation or 'Purchase/Sale of Shares by Director' titles, outside the sample.")
# price check of the transcription against the raw close around the trade date
Tc = T[(T.dup_of == "") & T.price.notna() & T.trade_date.notna() & T["mode"].isin(["market", "unstated"])]
badpx = []
for r in Tc.itertuples():
    if r.symbol not in cidx:
        continue
    k = dates.searchsorted(r.trade_date); w_ = close.iloc[max(0, k - 3):k + 4, cidx[r.symbol]].dropna()
    if w_.empty:
        badpx.append(f"{r.doc_id} {r.symbol} {r.trade_date:%Y-%m-%d} price {r.price:g} (no price in window)")
    elif not (w_.min() * 0.9 <= r.price <= w_.max() * 1.1):
        badpx.append(f"{r.doc_id} {r.symbol} {r.trade_date:%Y-%m-%d} price {r.price:g} vs raw close {w_.min():g}-{w_.max():g}")
out(f"transcription check: {len(Tc)} unique qualifying lines with a price and trade date compared with the raw close within +-3 trading days (+-10%): {len(Tc) - len(badpx)} inside, {len(badpx)} outside" + ("" if not badpx else ": " + "; ".join(badpx)))
out("5-row spot check of insider rows with no document id (seed 20261017, drawn symbols, 2019 on): PSX portal day pages queried 2026-10-17. FFC 2025-01-09 14:48: row has no PDF; FFC 2024-11-19 09:08: no PDF; FFC 2021-06-30 09:53: no PDF; GGL 2021-03-26 10:40: no PDF (3 rows that day, none with a PDF); CEPB 2019-07-31 14:33: a PDF exists at /download/document/133076.PDF.")
out("  The CEPB hit is a scraper bug: fetch_announcements.py matches '.pdf' case-sensitively, so documents linked as '.PDF' were stored as 'no document'. Re-fetching every announcement of the 22 drawn symbols (data/raw/insider_refetch_drawn.csv) finds 23 insider rows stored as no-document that do have a PDF (ISL 18, CNERGY 2, CEPB 2, SSGC 1; 2019: 4, 2020: 14, 2021: 3, 2025: 2), i.e. 23 of 224 no-document rows in the drawn symbols. The 2026-06-18 to 2026-10-16 window has none (data/raw/insider_refetch_2026.csv). These 23 are NOT in the 500-PDF sample, which was fixed in advance; ISL 2020 is the most affected.")

# timing / lag
Tu = T[T.dup_of == ""].copy()
lag = (Tu.ann_datetime.dt.normalize() - Tu.trade_date).dt.days.dropna()
lag = lag[(lag >= 0)]
out(f"\nFiling lag (announcement date minus trade date, days; unique lines with a trade date, n={len(lag)}): median {lag.median():.0f}, 90th percentile {lag.quantile(.9):.0f}, share filed same day {(lag==0).mean():.0%}, share lag over 5 days {(lag>5).mean():.0%}")
fm = smp.ann.dt.hour * 60 + smp.ann.dt.minute
out(f"Sample filings stamped at or after 15:30 PKT: {(fm >= 930).mean():.1%} ({int((fm >= 930).sum())} of {len(smp)}); stamped before 09:15: {(fm < 555).mean():.1%}")
a19 = ins[(ins.datetime >= "2019-01-01") & ins.has_doc]
am = a19.datetime.dt.hour * 60 + a19.datetime.dt.minute
out(f"All insider filings with a document since 2019 (n={len(a19):,}): at or after 15:30 {(am >= 930).mean():.1%}, before 09:15 {(am < 555).mean():.1%}")

# ================================================================= 4. events
smk = Q.copy()
smk["bq"] = smk.direction == "buy"
def build_L(trades, buy_modes=None):
    """announcement list per symbol: [(t, doc, buyers, sellers)] from qualifying unique lines (optional mode filter)"""
    L = {}
    t = trades if buy_modes is None else trades[trades["mode"].isin(buy_modes)]
    for (sym, tt, doc), g in t.groupby(["symbol", "ann_datetime", "doc_id"], sort=True):
        L.setdefault(sym, []).append((tt, doc, set(g[g.direction == "buy"].holder_norm), set(g[g.direction == "sell"].holder_norm), g))
    return L

def windows(Ls):
    """for each announcement k: holders over the trailing 30 calendar days before (m<k) and including it"""
    res = []
    for k, (t, doc, B, S, g) in enumerate(Ls):
        bb, ss = set(), set()
        for m in range(k):
            if Ls[m][0] > t - D30:
                bb |= Ls[m][2]; ss |= Ls[m][3]
        res.append((bb, ss, bb | B, ss | S))
    return res

def cluster_events(L, side="buy", net=False):
    ev = []
    for sym, Ls in L.items():
        W = windows(Ls)
        for k, (t, doc, B, S, g) in enumerate(Ls):
            trig = B if side == "buy" else S
            if not trig:
                continue
            bb, ss, ba, sa = W[k]
            if side == "buy":
                a, b = (len(ba) - len(sa), len(bb) - len(ss)) if net else (len(ba), len(bb))
                members = ba
            else:
                a, b = len(sa), len(ss); members = sa
            if a >= 2 and b < 2:
                ev.append(dict(symbol=sym, ann=t, doc=doc, members=sorted(members), role=""))
    return ev

def units(trades, direction):
    ev = []
    t = trades[trades.direction == direction]
    for (sym, h), g in t.groupby(["symbol", "holder_norm"]):
        g = g.sort_values(["ann_datetime", "doc_id"]); start = None
        for r in g.itertuples():
            if start is None or r.ann_datetime > start + D30:
                ev.append(dict(symbol=sym, holder=h, ann=r.ann_datetime, doc=r.doc_id, role=r.role)); start = r.ann_datetime
    return ev

L_all = build_L(smk)
def after_count(sym, t, doc, L):
    Ls = L[sym]; W = windows(Ls)
    for k, x in enumerate(Ls):
        if x[0] == t and x[1] == doc:
            return len(W[k][2])
    return None

E = {}
E["H1 cluster"] = cluster_events(L_all, "buy")
E["H1 net-of-sales"] = cluster_events(L_all, "buy", net=True)
bu = units(smk, "buy"); su = units(smk, "sell")
Wc = {s: windows(L_all[s]) for s in L_all}
def nafter(sym, t, doc):
    for k, x in enumerate(L_all[sym]):
        if x[0] == t and x[1] == doc:
            return len(Wc[sym][k][2])
E["H1 singles"] = [u for u in bu if nafter(u["symbol"], u["ann"], u["doc"]) == 1]
for r_, nm in (("sponsor_substantial", "H2 sponsor_substantial"), ("director_ceo", "H2 director_ceo"), ("executive", "H2 executive")):
    E[nm] = [u for u in bu if u["role"] == r_]
sells_by = {}
for t_ in smk[smk.direction == "sell"].itertuples():
    sells_by.setdefault((t_.symbol, t_.holder_norm), []).append(t_.ann_datetime)
rt, cl = [], []
for u in bu:
    prior = [x for x in sells_by.get((u["symbol"], u["holder"]), []) if u["ann"] - D180 <= x < u["ann"]]
    (rt if prior else cl).append(u)
E["H3 round-trip"] = rt; E["H3 clean"] = cl
E["H4 single"] = su
E["H4 cluster"] = cluster_events(L_all, "sell")
ONE_SIDED_LOW = {"H4 single", "H4 cluster"}

# roles of H1 cluster members for the record
def in_backtest(ev):
    return [e for e in ev if e["symbol"] in drawn and e["ann"] >= pd.Timestamp("2019-01-01")]

# ================================================================= 5. engine for one event set
def prepare(ev, plus1=False, restrict=True, extra_drop=None):
    """map events to entry rows; returns DataFrame with entry row / date and drop reasons"""
    rows_ = []
    for e in (in_backtest(ev) if restrict else ev):
        r, why = entry_row(e["symbol"], e["ann"], plus1)
        rec = dict(e); rec["why"] = why
        if r is not None:
            rec["eidx"] = r; rec["edate"] = dates[r]; rec["sidx"] = cidx[e["symbol"]]
            if not liq[r, rec["sidx"]]:
                rec["why"] = "illiquid"
            elif extra_drop is not None and extra_drop(e["symbol"], r):
                rec["why"] = "post_results"
        rows_.append(rec)
    return pd.DataFrame(rows_)

def nonoverlap(df, h):
    keep, last = [], {}
    for r in df.sort_values(["symbol", "eidx"]).itertuples():
        if r.symbol in last and r.eidx <= last[r.symbol] + h:
            keep.append(False); continue
        keep.append(True); last[r.symbol] = r.eidx
    return pd.Series(keep, index=df.sort_values(["symbol", "eidx"]).index).reindex(df.index)

rng = np.random.default_rng(SEED)
def placebo_matrix(kept, h):
    """(n, 20) placebo nets, NaN row when the event has no eligible day"""
    M = np.full((len(kept), 20), np.nan)
    for i, r in enumerate(kept.itertuples()):
        j = r.sidx
        lo = dates.searchsorted(r.edate - pd.Timedelta(days=365)); hi = dates.searchsorted(r.edate + pd.Timedelta(days=365), side="right")
        cand = np.arange(lo, min(hi, N - h))
        cand = cand[traded[cand, j] & liq[cand, j] & (cand != r.eidx)]
        if len(cand) == 0:
            continue
        v, code = win(np.full(len(cand), j), cand, cand + h)
        v = v[code == 0] - COST
        if len(v) == 0:
            continue
        M[i] = rng.choice(v, 20, replace=len(v) < 20)
    return M

def month_stats(net, ed):
    mo = pd.Series(net).groupby(pd.Series(ed).dt.to_period("M").values).mean()
    return mo.median(), (mo > 0).mean(), len(mo)

def row_stats(df, M, one_low=False):
    n = len(df)
    if n == 0:
        return None
    net = df.net.values; med = np.median(net)
    w = df.loc[df.net.idxmin()]
    mm, mw, nm = month_stats(net, df.edate)
    ok = ~np.isnan(M).any(axis=1)
    pm = pw = pp = np.nan
    if ok.sum() >= 1:
        idx = rng.integers(0, 20, (1000, int(ok.sum())))
        vals = M[ok][np.arange(int(ok.sum())), idx]
        meds = np.median(vals, axis=1)
        pm, pw = np.median(meds), (vals > 0).mean()
        evm = np.median(net[ok])
        pp = (meds <= evm).mean() if one_low else (meds >= evm).mean()
    return dict(n=n, sym=df.symbol.nunique(), months=nm, mean=net.mean(), med=med, win=(net > 0).mean(), worst=net.min(), wsym=w.symbol, wdate=w.edate,
                mcmed=mm, mcwin=mw, pmed=pm, pwin=pw, p=pp, nplc=int(ok.sum()))

def fmt(label, h, split, s):
    if s is None:
        return f"{label:<24}| h={h:<3}| {split:<4}| n=0"
    lab = "  [insufficient to conclude]" if (s["n"] < 20 or s["months"] < 8) else ""
    return (f"{label:<24}| h={h:<3}| {split:<4}| n={s['n']:<3} sym={s['sym']:<2} mo={s['months']:<2} mean={fp(s['mean'])} med={fp(s['med'])} win={fq(s['win'],0)} "
            f"worst={fp(s['worst'])} ({s['wsym']} {s['wdate']:%Y-%m-%d}) | mc_med={fp(s['mcmed'])} mc_win={fq(s['mcwin'],0)} | plc_med={fp(s['pmed'])} plc_win={fq(s['pwin'],0)} p={fn(s['p'],3)} (placebo n={s['nplc']}){lab}")

def run(label, ev, plus1=False, extra_drop=None, splits=True, hz=HZ, restrict=True, store=None):
    """full pipeline for one hypothesis row; returns dict of tables"""
    pre = prepare(ev, plus1, restrict, extra_drop)
    res = {}
    if pre.empty:
        out(f"{label}: no events"); return res
    d1 = pre.why.value_counts().to_dict()
    ok_ = pre[pre.why == "ok"].copy()
    out(f"{label}: events built {len(pre)}; dropped no price series {d1.get('no_price_series',0)}, no observation within 5 rows {d1.get('no_obs_5d',0)}, illiquid at entry {d1.get('illiquid',0)}"
        + (f", post-results {d1.get('post_results',0)}" if 'post_results' in d1 else "") + f"; usable {len(ok_)}")
    for h in hz:
        v, code = win(ok_.sidx.values, ok_.eidx.values, ok_.eidx.values + h)
        d = ok_.copy(); d["net"] = v - COST; d["code"] = code
        inc = int((code == 1).sum()); noobs = int((code == 2).sum())
        d = d[d.code == 0]
        kp = nonoverlap(d, h); nov = int((~kp).sum()); d = d[kp]
        out(f"   h={h}: dropped horizon past {LAST.date()} {inc}, no obs in window {noobs}; overlapping events removed {nov}; kept {len(d)}")
        M = placebo_matrix(d, h)
        if store is not None:
            store[(label, h)] = (d, M)
        parts = [("all", d, M)]
        if splits:
            mi = (d.edate >= IS[0]) & (d.edate <= IS[1]); mo = (d.edate >= OOS[0]) & (d.edate <= OOS[1])
            parts += [("IS", d[mi], M[mi.values]), ("OOS", d[mo], M[mo.values])]
        for nm, dd, MM in parts:
            s = row_stats(dd, MM, label in ONE_SIDED_LOW)
            res[(h, nm)] = s
            out("   " + fmt(label, h, nm, s))
    return res

# ================================================================= 6. results
out("\n== 2. EVENT COUNTS BEFORE RETURNS (all symbols with parsed filings; the backtest keeps the 22 drawn symbols only, from 2019-01-01)")
for k, ev in E.items():
    bt = in_backtest(ev)
    out(f"{k:<24}: all symbols {len(ev):>4}; drawn symbols {len(bt):>4}; announcements 2026-07-18 to 2026-10-16 (any symbol) {sum(1 for e in ev if e['ann'] >= pd.Timestamp('2026-07-18'))}")

out("\n== 3. RESULTS (net of 0.5% round trip, excess vs equal-weight market; non-overlap rule; placebo = 1,000 samples of one random same-symbol day within +-365 days per event). IS = entry 2019-01-01 to 2023-12-31, OOS = 2024-01-01 to 2026-10-16")
out("A buy can appear in both H1 and H2 (and H3); the hypotheses are never pooled.")
ST = {}
RES = {}
for k in E:
    out(f"\n-- {k}")
    RES[k] = run(k, E[k], store=ST)

out("\n-- event lists (all events in the 22 drawn symbols, before drops): H1 buy clusters and H4 sell clusters")
for k_ in ("H1 cluster", "H4 cluster"):
    for e in sorted(in_backtest(E[k_]), key=lambda x: (x["symbol"], x["ann"])):
        r_, why_ = entry_row(e["symbol"], e["ann"])
        out(f"  {k_}: {e['symbol']} completed {e['ann']:%Y-%m-%d %H:%M}; members {', '.join(e['members'])}; entry {('n/a (' + why_ + ')') if r_ is None else format(dates[r_], '%Y-%m-%d') + (' liquid' if liq[r_, cidx[e['symbol']]] else ' illiquid')}")

# ---------------- H2 permutation
out("\n== 4. H2: difference in medians, sponsor_substantial minus director_ceo (net, kept events); p = share of 1,000 label shuffles with a difference at least as large (one-sided)")
def perm(a, b, nshuf=1000, seed=SEED):
    r_ = np.random.default_rng(seed)
    obs = np.median(a) - np.median(b); pool = np.concatenate([a, b]); na = len(a); c = 0
    for _ in range(nshuf):
        r_.shuffle(pool)
        c += (np.median(pool[:na]) - np.median(pool[na:])) >= obs
    return obs, c / nshuf
for h in HZ:
    sa, sb = ST.get(("H2 sponsor_substantial", h)), ST.get(("H2 director_ceo", h))
    if sa is None or sb is None:
        out(f"h={h}: not available"); continue
    a, b = sa[0], sb[0]
    for tag_, f_ in (("all drawn events", lambda d: d), ("without ASL and AHCL", lambda d: d[~((d.symbol == "ASL") | d.holder.str.contains("ARIF HABIB CORPORATION"))])):
        x, y = f_(a), f_(b)
        if len(x) < 2 or len(y) < 2:
            out(f"h={h} {tag_}: sponsor n={len(x)}, director n={len(y)}; too few to test"); continue
        obs, p = perm(x.net.values, y.net.values)
        out(f"h={h} {tag_}: sponsor n={len(x)} median {fp(x.net.median())}, director n={len(y)} median {fp(y.net.median())}; difference {fp(obs)}; p={p:.3f}" + ("  [insufficient to conclude]" if min(len(x), len(y)) < 20 else ""))
out("ASL and AHCL: neither ASL (symbol) nor Arif Habib Corporation (holder) is in the 22 drawn backtest symbols, so the H2 rows above already exclude them; their 2026 filings sit in block a and are used only in the current list.")

# ---------------- concentration
out("\n== 5. CONCENTRATION (kept events, h=63, all periods)")
for k in ("H1 cluster", "H2 sponsor_substantial", "H2 director_ceo", "H2 executive", "H4 single", "H4 cluster"):
    d = ST.get((k, 63))
    if d is None or len(d[0]) == 0:
        out(f"{k}: no events"); continue
    d = d[0]
    yc = d.edate.dt.year.value_counts().sort_index()
    mc = d.edate.dt.to_period("M").value_counts()
    top3 = d.net.sort_values(ascending=False).head(3)
    tot = d.net.sum()
    out(f"{k:<24}: n={len(d)}; by year " + ", ".join(f"{y}:{c}" for y, c in yc.items()) + f"; largest single month {mc.index[0]} holds {mc.iloc[0] / len(d):.0%} of events; top 3 events sum {top3.sum():+.2%} vs total net {tot:+.2%}"
        + (f" (share {top3.sum() / tot:.0%})" if tot > 0 else " (total net not positive, share not meaningful)"))

# ---------------- robustness
out("\n== 6. H1 ROBUSTNESS at h=63 (all periods, IS, OOS)")
base = ST.get(("H1 cluster", 63))
fr = ann[ann.klass == "financial_result"].copy()
fr["dt"] = fr.datetime.dt.tz_localize(None)
res_rows = {}
for s_, g in fr.groupby("symbol"):
    if s_ in cidx:
        rr = [entry_row(s_, t)[0] for t in g.dt]
        res_rows[s_] = np.array(sorted({x for x in rr if x is not None}))
def post_res(sym, r):
    a = res_rows.get(sym)
    if a is None or len(a) == 0:
        return False
    return bool(((a <= r) & (r <= a + 10)).any())
rob = {}
rob["(a) entry at the D+1 close"] = run("H1 cluster D+1", E["H1 cluster"], plus1=True, hz=(63,))
mk = cluster_events(build_L(smk, buy_modes=["market"]), "buy")
rob["(b) mode == market only"] = run("H1 cluster market-only", mk, hz=(63,))
rob["(c) exclude within 10 trading days after a result"] = run("H1 cluster ex-results", E["H1 cluster"], extra_drop=post_res, hz=(63,))
pre = prepare(E["H1 cluster"]); pk = pre[pre.why == "ok"]
share = np.mean([post_res(r.symbol, r.eidx) for r in pk.itertuples()]) if len(pk) else float("nan")
nshare = int(sum(post_res(r.symbol, r.eidx) for r in pk.itertuples()))
out(f"(c) share of usable H1 cluster events entering within 10 trading days after a financial_result announcement in the same symbol: {nshare} of {len(pk)} ({share:.0%})")
if base is not None:
    kp_ = base[0]
    out(f"    among the kept 63-day H1 events: {int(sum(post_res(r.symbol, r.eidx) for r in kp_.itertuples()))} of {len(kp_)}")

# ---------------- current list
out("\n== 7. CURRENT LIST: H1 buy clusters and H4 sell clusters whose completing announcement falls 2026-07-18 to 2026-10-16 in KMI-list names")
kmi = set(pd.read_csv(ROOT / "data" / "kmi_allshare_2026-06-05.csv").symbol)
liq_now = set(P.liquid_universe(pd.Timestamp("2026-10-17")))
def show_current(name, ev):
    cur = [e for e in ev if e["ann"] >= pd.Timestamp("2026-07-18") and e["symbol"] in kmi]
    out(f"\n{name}: {len(cur)} clusters")
    for e in sorted(cur, key=lambda x: x["ann"]):
        sym, t = e["symbol"], e["ann"]
        r, why = entry_row(sym, t)
        status = "liquid (Rs5m, trailing 60 days)" if sym in liq_now else "NOT liquid at Rs5m"
        side = "buy" if name.startswith("H1") else "sell"
        if r is None:
            ret_ = "n/a (" + why + ")"
        else:
            v, code = win(np.array([cidx[sym]]), np.array([r]), np.array([N - 1]))
            ret_ = f"entry close {dates[r]:%Y-%m-%d}, net excess to {LAST:%Y-%m-%d} close {fp(float(v[0]) - COST) if code[0]==0 else 'n/a'}; liquid at entry: {bool(liq[r, cidx[sym]])}"
        out(f"  {sym}: completed {t:%Y-%m-%d %H:%M}; {status}; {ret_}")
        g = smk[(smk.symbol == sym) & (smk.ann_datetime > t - D30) & (smk.ann_datetime <= t) & (smk.direction == side)]
        for r_ in g.sort_values(["ann_datetime", "doc_id"]).itertuples():
            out(f"      {side}: ann {r_.ann_datetime:%Y-%m-%d %H:%M} doc {r_.doc_id}; {r_.holder_name} ({r_.role}); trade {r_.trade_date:%Y-%m-%d}; {r_.shares:,.0f} sh @ {r_.price:g} = Rs {r_.value_rs:,.0f}; mode {r_.mode}")
        o = smk[(smk.symbol == sym) & (smk.ann_datetime > t - D30) & (smk.ann_datetime <= t + pd.Timedelta(days=30)) & (smk.direction != side)]
        if len(o):
            for r_ in o.sort_values(["ann_datetime", "doc_id"]).itertuples():
                out(f"      opposite side ({r_.direction}) in the window: ann {r_.ann_datetime:%Y-%m-%d %H:%M}; {r_.holder_name} ({r_.role}); {r_.shares:,.0f} sh @ {r_.price:g}")
        else:
            out("      no qualifying opposite-side trades in the same 30 days")
show_current("H1 buy cluster", E["H1 cluster"])
show_current("H4 sell cluster", E["H4 cluster"])
out("\nOther qualifying single buys 2026-07-18 to 2026-10-16 in KMI names that did NOT form a cluster are not listed; see data/insider_trades.csv.")

open(ROOT / "tests" / "out" / "insider_cluster_buying.txt", "w", encoding="utf-8").write(buf.getvalue())
