"""winners_population: every price run of +50% in 21-63 sessions or +100% in 126-252 sessions, 2016-10 to 2026-10, merged into episodes.
Run: .venv/Scripts/python.exe scripts/tests/winners_population.py build   -> data/winners_library.csv, data/winners_library_thin.csv (+ tests/out/winners_population_build.txt)
     .venv/Scripts/python.exe scripts/tests/winners_population.py engine  -> adds engine analogue columns for a sample of 60 episodes
     .venv/Scripts/python.exe scripts/tests/winners_population.py tables  -> tests/out/winners_population_tables.txt (numbers used in tests/winners_population.md)

DEFINITIONS (fixed before any result was looked at; tests/winners_population.md repeats them).
 Prices: adjusted (bonus, split, partial cash) closes from data/panel_close_adj.parquet for the 456 panel names (prices_raw + seed), crude-chain level for delisted names
 (as scripts/daily_table.py), forward-filled between a name's first and last trade. Sessions are the 2,480 market sessions of prices.load_panel.
 Qualifying window: [s, e] with e-s in 21..63 and close_e/close_s >= 1.5, or e-s in 126..252 and close_e/close_s >= 2.0. Overlapping windows merge into one episode.
 Start = lowest close in the 20 sessions up to the first qualifying window's start (not before the previous episode's peak). Peak = highest close from the start to 21 sessions
 after the merged windows end (capped before the next episode's first window and at the last trade). Multiple = peak / start.
 Liquid list: median traded value (close x volume, 60 sessions ending the day before the start, >= 40 listed sessions) above Rs2m; everything else is the thin list.
 First 252-high: first traded session from the start whose close exceeds the max close of the previous 252 sessions (>= 126 sessions of history needed).
 Fraction still ahead at session X = 1 - ln(P_X/P_start)/ln(P_peak/P_start) (log share of the gain), 0 if X is at or after the peak. Linear version: (P_peak - P_X)/(P_peak - P_start).
 Upper lock: close at the daily limit (5% to 27 Mar 2020, 7.5% to 5 Jul 2024, 10% after), same rule as data/DAILY_TABLE_NOTES.md, on raw closes, sessions start+1..peak.
 Filings: assigned to sessions as daily_table.py (after 15:30 -> next session). pre = sessions start-20..start; run = start+1..peak.
 Cause flags (an episode can carry several; the type is the first that applies in the order below):
  deal     material_info filing whose title matches acqui|merger|amalgam|takeover|offer (rights, public offer, offer for sale excluded) in start-20 .. min(peak, start+63)
  results  a financial_result filing in pre whose quarter EPS (data/fundamentals/quarterly_eps.csv, matched by the period in the title) is >= 1.5x the same quarter a year earlier, or loss to profit
  sponsor  insider_trade filing with direction buy, or a title matching buy-back|buyback|repurchase, in start-20 .. min(peak, start+63)
  policy   median liquid peer in the same sector (sector_momentum.py dict, self excluded, >= 3 peers) rose >= 30% from start to peak
  shock    KMI All Share closed >= 8% below its 20-session high on some session in start-20 .. start
  ratecut  start within 0..60 sessions after the first policy-rate cut after a hike (policy_rate_decisions.csv)
  other    none of the above but a material_info filing in start-20 .. start+63
  operator none of the above and no material_info filing
 Trailing stop: close <= 80% of the running maximum close since entry; exit at that close; if never hit, mark at the last close.
"""
import ast, re, sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
D = ROOT / "data"
OUT = ROOT / "tests" / "out"
LIB, THIN = D / "winners_library.csv", D / "winners_library_thin.csv"
MODE = sys.argv[1] if len(sys.argv) > 1 else "build"
LOGL = []


def log(*a):
    s = " ".join(str(x) for x in a)
    LOGL.append(s)
    print(s)


def build():
    import prices as P
    close_raw, vol, tv = P.load_panel()
    CAL = close_raw.index
    N = len(CAL)
    adj = pd.read_parquet(D / "panel_close_adj.parquet").reindex(index=CAL)
    # ---- delisted names, duplicates of any other code dropped (90% equal closes test of daily_table.py)
    def rd(f):
        x = pd.read_csv(f, usecols=["date", "open", "high", "low", "close", "volume"], parse_dates=["date"], index_col="date")
        return x[~x.index.duplicated(keep="last")].sort_index()
    seen = close_raw.copy()
    dl = {}
    for f in sorted((D / "prices_delisted").glob("*.csv")):
        if f.stem in close_raw.columns:
            continue
        x = rd(f)
        if len(x) == 0:
            continue
        c = x.close.where((x.volume > 0) & (x.close > 0)).reindex(CAL)
        if c.notna().sum() < 5:
            continue
        both = seen.notna() & c.notna().values[:, None]
        n = both.sum().values
        same = ((seen.values == c.values[:, None]) & both.values).sum(0)
        if ((same >= 0.9 * n) & (n >= 100)).any():
            continue
        dl[f.stem] = x
        seen[f.stem] = c
    log(f"panel names {close_raw.shape[1]}, delisted kept {len(dl)}")

    def crude_level(x):
        c = x.close.where((x.volume > 0) & (x.close > 0))
        r = P.returns(c.to_frame("s"), "crude", vol=x.volume.to_frame("s"))["s"]
        lv = (1 + r.fillna(0)).cumprod().where(c.notna())
        return lv / lv.ffill().iloc[-1] * c.ffill().iloc[-1]

    A, RAW, TV, DEL = {}, {}, {}, {}
    for s in close_raw.columns:
        A[s] = adj[s].where(close_raw[s].notna())
        RAW[s] = close_raw[s]
        TV[s] = tv[s]
        DEL[s] = False
    for s, x0 in dl.items():
        x = x0.reindex(CAL)
        tr = (x.volume > 0) & (x.close > 0)
        first, last = np.flatnonzero(tr.values)[[0, -1]]
        lvl = crude_level(x0).reindex(CAL).where(tr)
        A[s] = lvl
        RAW[s] = x.close.where(tr)
        t = (x.close * x.volume).where(tr, 0.0)
        t.iloc[:first] = np.nan
        t.iloc[last + 1:] = np.nan
        TV[s] = t
        DEL[s] = True
    names = list(A)
    A = pd.DataFrame(A)[names]
    RAW = pd.DataFrame(RAW)[names]
    TV = pd.DataFrame(TV)[names]
    obs = A.notna().values
    first = np.array([np.flatnonzero(obs[:, j])[0] if obs[:, j].any() else -1 for j in range(len(names))])
    last = np.array([np.flatnonzero(obs[:, j])[-1] if obs[:, j].any() else -1 for j in range(len(names))])
    keep = first >= 0
    log(f"names with any trade {keep.sum()} of {len(names)}")
    Af = A.ffill()
    ar = np.arange(N)[:, None]
    Af = Af.where((ar >= first[None, :]) & (ar <= last[None, :]))
    Afv = Af.values
    RAWf = RAW.ffill()
    prevR = RAWf.shift(1)
    TVmed = TV.rolling(60, min_periods=40).median().shift(1).values
    pr252 = Af.rolling(252, min_periods=126).max().shift(1).values

    # ---- upper locks on raw closes
    LIM = np.where(CAL < pd.Timestamp("2020-03-30"), 0.05, np.where(CAL < pd.Timestamp("2024-07-08"), 0.075, 0.10))[:, None]
    up = RAW.values / prevR.values - 1
    pv = prevR.values
    LOCK = (up >= (1 + LIM) * 0.995 - 1) & np.where(pv >= 20, up <= (1 + LIM) * 1.015 - 1, up <= 0.30) & RAW.notna().values
    # agreement with the daily table
    dtb = pd.read_parquet(D / "daily_table.parquet", columns=["date", "symbol", "upper_lock"])
    jmap = {s: j for j, s in enumerate(names)}
    di = CAL.get_indexer(dtb.date)
    dj = dtb.symbol.map(jmap).values
    okk = (di >= 0) & ~pd.isna(dj)
    mine = LOCK[di[okk], dj[okk].astype(int)]
    theirs = dtb.upper_lock.values[okk].astype(bool)
    log(f"upper-lock agreement with daily_table on {okk.sum()} rows: both {int((mine & theirs).sum())}, mine only {int((mine & ~theirs).sum())}, table only {int((~mine & theirs).sum())}")
    del dtb

    # ---- qualifying windows -> per end the smallest start
    SMIN = np.full((N, len(names)), -1, dtype=np.int32)
    for L in list(range(21, 64)) + list(range(126, 253)):
        thr = 1.5 if L <= 63 else 2.0
        with np.errstate(invalid="ignore", divide="ignore"):
            ok = Afv[L:] / Afv[:-L] >= thr
        sl = SMIN[L:]
        sl[ok] = np.broadcast_to((np.arange(L, N) - L)[:, None], ok.shape)[ok]
    eps_ = []  # (j, s_first, e_last)
    for j in range(len(names)):
        if not keep[j]:
            continue
        ends = np.flatnonzero(SMIN[:, j] >= 0)
        if len(ends) == 0:
            continue
        iv = sorted(zip(SMIN[ends, j].tolist(), ends.tolist()))
        cs, ce = iv[0]
        for s, e in iv[1:]:
            if s <= ce:
                ce = max(ce, e)
            else:
                eps_.append((j, cs, ce))
                cs, ce = s, e
        eps_.append((j, cs, ce))
    log(f"merged windows {len(eps_)}")

    # ---- macro and reference series
    def ser(path, col):
        x = pd.read_csv(path, parse_dates=["date"]).set_index("date")[col]
        return x[~x.index.duplicated(keep="last")].sort_index().reindex(CAL.union(x.index)).ffill().reindex(CAL)
    kmi = ser(D / "macro/kmiallshr.csv", "close")
    kmi_v = kmi.values
    kmi_dd = (kmi / kmi.rolling(20, min_periods=20).max() - 1).values
    brent = ser(D / "macro/brent.csv", "value").values
    tb = pd.read_csv(D / "macro/tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"]).set_index("date").y6m
    prate = pd.read_csv(D / "macro/policy_rate_decisions.csv", parse_dates=["date"]).set_index("date")
    pr = prate.rate
    spread = tb.reindex(tb.index.union(CAL)).ffill().reindex(CAL) - pr.reindex(pr.index.union(CAL)).ffill().reindex(CAL)
    REG = np.where(spread.isna(), None, np.where(spread > 0, "bill>policy", "bill<=policy"))
    firstcut, state = [], False
    for r in prate.itertuples():
        if r.change_bp > 0:
            state = False
        elif r.change_bp < 0 and not state:
            firstcut.append(r.Index)
            state = True
    fc_idx = [int(CAL.searchsorted(d)) for d in firstcut]
    log("first cuts after a hike:", [str(d.date()) for d in firstcut])

    # ---- membership
    snaps = sorted(((pd.Timestamp(re.search(r"(\d{4}-\d{2}-\d{2})", f.name).group(1)), set(pd.read_csv(f).symbol))
                    for f in (D / "index_members").glob("KMI_ALL_*.csv") if "derived" in f.name or "2026-06-05" in f.name), key=lambda z: z[0])
    kmi_now = set(pd.read_csv(D / "kmi_allshare_2026-06-05.csv").symbol)

    def kmi_at(sym, d):
        k = max(np.searchsorted([z[0] for z in snaps], np.datetime64(d), "right") - 1, 0)
        return sym in snaps[k][1]

    # ---- sectors
    src = (ROOT / "scripts/sector_momentum.py").read_text()
    a0 = src.index("S = {") + 4
    SECT = ast.literal_eval(src[a0:src.index("\n}", a0) + 2])
    SEC = {t: sec for sec, nm in SECT.items() for t in nm.split()}
    NCC = {"Cement": "Cement", "Fertilizer": "Fertilizer", "E&P": "Oil and Gas Exploration Companies", "OMC": "Oil and Gas Marketing Companies",
           "Power": "Power Generation and Distribution", "Tech & telecom": "Technology and Communication", "Islamic banks & fin.": "Commercial Banks",
           "Food & staples": "Food and Personal Care Products"}
    fl = pd.read_csv(D / "macro/fipi_lipi_by_sector.csv", parse_dates=["date"])
    fl = fl[fl.investor_group.isin(["fipi", "lipi individuals"])]
    flp = fl.pivot_table(index="date", columns=["sector", "investor_group"], values="net_usd_mn", aggfunc="sum")

    # ---- filings
    an = pd.read_parquet(D / "announcements.parquet")
    dtm = an.datetime.dt.tz_convert("Asia/Karachi").dt.tz_localize(None)
    an["sess"] = CAL.searchsorted(((dtm - pd.Timedelta(hours=15, minutes=30)).dt.normalize() + pd.Timedelta(days=1)).values)
    an["dt"] = dtm
    an = an[(an.sess < N) & an.symbol.isin(names)]
    AN = {s: g.sort_values(["sess", "dt"]) for s, g in an.groupby("symbol")}
    KL = ["financial_result", "dividend_or_bonus", "material_info", "insider_trade", "board_meeting_notice", "agm", "credit_rating", "other"]
    eps = pd.read_csv(D / "fundamentals/quarterly_eps.csv", parse_dates=["fiscal_quarter_end"])
    eps["e"] = eps.eps_basic.fillna(eps.eps_diluted)
    EPS = {s: g.set_index("fiscal_quarter_end").e.dropna() for s, g in eps.groupby("symbol")}
    DEAL = re.compile(r"acqui|merger|amalgam|take[- ]?over|\boffer", re.I)
    NODEAL = re.compile(r"right|offer for sale|public offer|initial public|ipo", re.I)
    BUYB = re.compile(r"buy[- ]?back|repurchase", re.I)

    def period_of(title):
        m = re.search(r"(?:ended|ending)\s+(.*)$", str(title), re.I)
        if not m:
            return None
        s = re.sub(r"[.]+$", "", m.group(1)).strip()
        s = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", s)
        try:
            from dateutil import parser as dp
            return pd.Timestamp(dp.parse(s, fuzzy=True, default=pd.Timestamp("2000-01-01").to_pydatetime()))
        except Exception:
            return None

    def eps_jump(sym, g_pre):
        """-> (known, jump, eps_now, eps_prior) over the financial_result filings in the pre window"""
        e = EPS.get(sym)
        if e is None or len(g_pre) == 0:
            return False, False, np.nan, np.nan
        known, jump, bn, bp = False, False, np.nan, np.nan
        for r in g_pre.itertuples():
            q = period_of(r.title)
            if q is None:
                continue
            q = pd.Timestamp(q)
            k = np.argmin(np.abs((e.index - q).days)) if len(e) else None
            if k is None or abs((e.index[k] - q).days) > 10:
                continue
            qe = e.index[k]
            j = np.argmin(np.abs((e.index - (qe - pd.DateOffset(years=1))).days))
            if abs((e.index[j] - (qe - pd.DateOffset(years=1))).days) > 10:
                continue
            en, ep = float(e.iloc[k]), float(e.iloc[j])
            known = True
            jj = (ep > 0 and en >= 1.5 * ep) or (ep <= 0 and en > 0)
            if jj or np.isnan(bn):
                bn, bp = en, ep
            jump = jump or jj
        return known, jump, bn, bp

    # ---- episodes
    rows = []
    byname = {}
    for j, s_, e_ in eps_:
        byname.setdefault(j, []).append((s_, e_))
    for j, lst in byname.items():
        sym = names[j]
        prev_pk = -1
        for n_, (s_first, e_last) in enumerate(lst):
            nxt = lst[n_ + 1][0] if n_ + 1 < len(lst) else N
            lo = max(s_first - 20, prev_pk + 1, first[j])
            seg = Afv[lo:s_first + 1, j]
            st = lo + int(np.nanargmin(seg))
            ub = min(e_last + 21, nxt - 1, last[j])
            seg = Afv[st:ub + 1, j]
            pk = st + int(np.nanargmax(seg))
            prev_pk = pk
            rows.append(dict(j=j, symbol=sym, st=st, pk=pk, s_first=s_first, e_last=e_last))
    E = pd.DataFrame(rows)
    log(f"episodes {len(E)} in {E.symbol.nunique()} names")

    out = []
    for r in E.itertuples():
        j, st, pk, sym = r.j, r.st, r.pk, r.symbol
        a = Afv[:, j]
        P0, P1 = a[st], a[pk]
        d = dict(symbol=sym, kmi=bool(kmi_at(sym, CAL[st])), kmi_now=sym in kmi_now, delisted=bool(DEL[sym]),
                 start_date=CAL[st].date(), start_price=round(P0, 4), start_close_raw=RAW.values[st, j],
                 peak_date=CAL[pk].date(), peak_price=round(P1, 4), peak_close_raw=RAW.values[pk, j],
                 multiple=P1 / P0, sessions_to_peak=pk - st, first_window_start=CAL[r.s_first].date(), last_window_end=CAL[r.e_last].date())
        d["ongoing"] = bool(last[j] == N - 1 and pk >= N - 6)
        d["pre_2019"] = bool(CAL[st] < pd.Timestamp("2019-01-28"))
        # how it ended
        seg = a[pk + 1:min(pk + 61, last[j]) + 1]
        d["dd60_after_peak"] = float(np.nanmin(seg) / P1 - 1) if len(seg) else np.nan
        d["dd60_complete"] = bool(pk + 60 <= last[j])
        ex_, hit_ = a[last[j]], False   # 20% trailing stop measured from the peak: first close after the peak at or below 80% of it
        for t in range(pk + 1, last[j] + 1):
            if a[t] <= 0.8 * P1:
                ex_, hit_ = a[t], True
                break
        d["peak_stop_exit_mult"] = ex_ / P0
        d["peak_stop_kept_half"] = bool((ex_ / P0 - 1) > 0.5 * (P1 / P0 - 1))
        d["peak_stop_hit"] = hit_
        # first 252-high
        w = np.flatnonzero((a[st:pk + 1] > pr252[st:pk + 1, j]) & ~np.isnan(RAW.values[st:pk + 1, j]))
        f252i = st + int(w[0]) if len(w) else None
        d["f252_date"] = CAL[f252i].date() if f252i is not None else None
        d["f252_sessions_after_start"] = f252i - st if f252i is not None else np.nan
        d["has_history"] = bool(not np.isnan(pr252[st:pk + 1, j]).all())
        lg = np.log(P1 / P0)

        def ahead(i):
            if i is None:
                return np.nan, np.nan
            if i >= pk:
                return 0.0, 0.0
            if i > last[j]:
                return np.nan, np.nan
            return float(1 - np.log(a[i] / P0) / lg), float((P1 - a[i]) / (P1 - P0))
        d["f252_x"] = a[f252i] / P0 if f252i is not None else np.nan
        d["ahead_f252_log"], d["ahead_f252_lin"] = ahead(f252i)
        for k in (10, 20, 40):
            d[f"ahead_{k}_log"], d[f"ahead_{k}_lin"] = ahead(st + k)
        # locks, pullback, one-day jumps
        d["upper_locks"] = int(LOCK[st + 1:pk + 1, j].sum())
        arr = a[st:pk + 1]
        pb = 0.0
        for k in range(1, 21):
            if len(arr) > k:
                pb = min(pb, np.nanmin(arr[k:] / arr[:-k]) - 1)
        d["max_pullback_20"] = pb
        rm = np.fmax.accumulate(arr)
        d["max_dd_in_run"] = float(np.nanmin(arr / rm - 1))
        n25, armed = 0, False   # number of times the close fell 25% below the running high and later made a new high
        for v_, m_ in zip(arr, rm):
            if v_ <= 0.75 * m_:
                armed = True
            elif armed and v_ >= m_:
                n25, armed = n25 + 1, False
        d["n_dd25_recovered_in_run"] = n25
        trd = np.flatnonzero(~np.isnan(RAW.values[st:pk + 1, j]))
        if len(trd) > 1:
            v = arr[trd]
            r1 = v[1:] / v[:-1] - 1
            d["max_1d_ret"] = float(r1.max())
            d["max_gap_sessions"] = int(np.diff(trd).max())
            d["traded_days_in_run"] = int(len(trd))
        else:
            d["max_1d_ret"], d["max_gap_sessions"], d["traded_days_in_run"] = np.nan, np.nan, int(len(trd))
        pre_ret = Afv[max(st - 25, 1):st + 4, j] / Afv[max(st - 26, 0):st + 3, j] - 1
        d["min_1d_around_start"] = float(np.nanmin(pre_ret)) if np.isfinite(pre_ret).any() else np.nan
        d["frac_sessions_traded"] = d["traded_days_in_run"] / (pk - st + 1)
        tvm = TVmed[st, j]
        d["tv_median_60"] = tvm
        d["liq_tier"] = "thin" if not (tvm > 2e6) else "H" if tvm > 20e6 else "M" if tvm > 5e6 else "L"
        # filings
        g = AN.get(sym)
        deal_off = spon_off = None
        pre_titles, run_titles = [], []
        res_known, res_jump, en, ep = False, False, np.nan, np.nan
        mat_any = False
        for k in KL:
            d[f"pre_{k}"] = d[f"run_{k}"] = 0
        d["pre_insider_buy"] = d["run_insider_buy"] = 0
        if g is not None:
            gs = g[(g.sess >= st - 20) & (g.sess <= pk)]
            for x in gs.itertuples():
                per = "pre" if x.sess <= st else "run"
                kl = x.klass if x.klass in KL else "other"
                d[f"{per}_{kl}"] += 1
                if x.klass == "insider_trade" and x.direction == "buy":
                    d[f"{per}_insider_buy"] += 1
                if kl not in ("board_meeting_notice", "agm"):
                    lst2 = pre_titles if per == "pre" else run_titles
                    if len(lst2) < 2:
                        lst2.append(f"{x.dt:%Y-%m-%d} [{kl}] {str(x.title)[:90]}".replace("\n", " "))
                near = x.sess <= min(pk, st + 63)
                if near and x.klass == "material_info":
                    mat_any = True
                    if DEAL.search(str(x.title)) and not NODEAL.search(str(x.title)) and deal_off is None:
                        deal_off = int(x.sess - st)
                if near and spon_off is None and ((x.klass == "insider_trade" and x.direction == "buy") or BUYB.search(str(x.title))):
                    spon_off = int(x.sess - st)
            res_known, res_jump, en, ep = eps_jump(sym, gs[(gs.klass == "financial_result") & (gs.sess <= st)])
        d["pre_total"] = sum(d[f"pre_{k}"] for k in KL)
        d["run_total"] = sum(d[f"run_{k}"] for k in KL)
        d["pre_first2"] = " || ".join(pre_titles)
        d["run_first2"] = " || ".join(run_titles)
        d["eps_known"], d["eps_now"], d["eps_prior"] = res_known, en, ep
        # sector
        sec = SEC.get(sym)
        d["sector"] = sec or "other"
        sm, npeer = np.nan, 0
        if sec:
            pj = [q for q in (names.index(p) for p in SECT[sec].split() if p in names and p != sym)
                  if TVmed[st, q] > 2e6 and not np.isnan(Afv[st, q]) and not np.isnan(Afv[pk, q])]
            npeer = len(pj)
            if npeer >= 3:
                sm = float(np.median(Afv[pk, pj] / Afv[st, pj] - 1))
        d["sector_move"], d["n_peers"] = sm, npeer
        d["index_move"] = float(kmi_v[pk] / kmi_v[st] - 1) if not (np.isnan(kmi_v[st]) or np.isnan(kmi_v[pk])) else np.nan
        d["regime_start"] = REG[st]
        d["brent_change"] = float(brent[pk] / brent[st] - 1) if not (np.isnan(brent[st]) or np.isnan(brent[pk])) else np.nan
        fn, li = np.nan, np.nan
        if sec in NCC and (NCC[sec], "fipi") in flp.columns:
            sub = flp.loc[(flp.index > CAL[st]) & (flp.index <= CAL[pk])]
            fn = float(sub[(NCC[sec], "fipi")].sum())
            li = float(sub[(NCC[sec], "lipi individuals")].sum())
        d["fipi_net_usd_mn"], d["lipi_individuals_net_usd_mn"] = fn, li
        # flags
        d["flag_deal"] = deal_off is not None
        d["flag_results"] = bool(res_jump)
        d["flag_sponsor"] = spon_off is not None
        d["flag_policy"] = bool(sm >= 0.30) if not np.isnan(sm) else False
        w20 = kmi_dd[max(st - 20, 0):st + 1]
        d["flag_shock"] = bool(np.nanmin(w20) <= -0.08) if not np.isnan(w20).all() else False
        d["flag_ratecut"] = any(0 <= st - c <= 60 for c in fc_idx)
        d["deal_offset"], d["sponsor_offset"] = deal_off if deal_off is not None else np.nan, spon_off if spon_off is not None else np.nan
        d["has_material_info"] = mat_any
        typ = ("takeover_deal" if d["flag_deal"] else "results_jump" if d["flag_results"] else "sponsor_buyback" if d["flag_sponsor"] else
               "policy_sector_wave" if d["flag_policy"] else "shock_rebound" if d["flag_shock"] else "rate_cut_rotation" if d["flag_ratecut"] else
               "other" if mat_any else "operator_no_visible_cause")
        d["type"] = typ
        d["n_flags"] = sum(d[f] for f in ("flag_deal", "flag_results", "flag_sponsor", "flag_policy", "flag_shock", "flag_ratecut"))

        # trailing 20% stop from three entries
        def stop(i, w=0.2):
            if i is None or i >= pk:
                return np.nan, np.nan, False
            m = a[i]
            for t in range(i + 1, last[j] + 1):
                if np.isnan(a[t]):
                    continue
                m = max(m, a[t])
                if a[t] <= (1 - w) * m:
                    return a[t] / a[i], (a[t] / a[i] - 1) > 0.5 * (P1 / a[i] - 1), True
            return a[last[j]] / a[i], (a[last[j]] / a[i] - 1) > 0.5 * (P1 / a[i] - 1), False
        for tag, i in (("start", st), ("f252", f252i), ("s20", st + 20)):
            x, kh, hit = stop(i)
            d[f"stop_{tag}_exit_mult"], d[f"stop_{tag}_kept_half"], d[f"stop_{tag}_hit"] = x, kh, hit
            for w in (0.3, 0.4):
                d[f"stop{int(w * 100)}_{tag}_exit_mult"] = stop(i, w)[0]
        out.append(d)
    # ---- denominator: every first 252-high (no other 252-high of the name in the previous 20 sessions) of a liquid (>Rs2m) name, and how often it was followed by +50% in 126 / +100% in 252 sessions
    ev = []
    for j in range(len(names)):
        if not keep[j]:
            continue
        a = Afv[:, j]
        fl_ = np.flatnonzero((a > pr252[:, j]) & ~np.isnan(RAW.values[:, j]) & (TVmed[:, j] > 2e6))
        lastev = -999
        for t in fl_:
            if t - lastev > 20 and t + 126 <= N - 1:
                f126 = np.nanmax(a[t + 1:t + 127]) / a[t] if t + 1 <= last[j] else np.nan
                f252_ = np.nanmax(a[t + 1:t + 253]) / a[t] if (t + 252 <= N - 1 and t + 1 <= last[j]) else np.nan
                ev.append((names[j], int(t), CAL[t].year, kmi_at(names[j], CAL[t]), f126, f252_))
            lastev = t
    EV = pd.DataFrame(ev, columns=["symbol", "t", "year", "kmi", "fwd_max_126", "fwd_max_252"])
    EV.to_csv(OUT / "winners_population_breakout_events.csv", index=False)
    log(f"first 252-highs of liquid names: {len(EV)}; followed by +50% (max close) within 126 sessions: {(EV.fwd_max_126 >= 1.5).mean():.3f}; +100% within 252: {(EV.fwd_max_252 >= 2).mean():.3f} (n={EV.fwd_max_252.notna().sum()}); KMI-at-time only: {(EV[EV.kmi].fwd_max_126 >= 1.5).mean():.3f} / {(EV[EV.kmi].fwd_max_252 >= 2).mean():.3f}")
    L = pd.DataFrame(out)
    L["data_suspect"] = (L.max_1d_ret > 0.5) | (L.min_1d_around_start <= -0.5) | (L.frac_sessions_traded < 0.4)
    L = L.sort_values("multiple", ascending=False).reset_index(drop=True)
    for c in ("engine_n", "engine_median_5", "engine_median_20", "engine_median_60"):
        L[c] = np.nan
    main = L[L.liq_tier != "thin"]
    thin = L[L.liq_tier == "thin"]
    main.to_csv(LIB, index=False)
    thin.to_csv(THIN, index=False)
    log(f"episodes {len(L)}: liquid (>Rs2m) {len(main)}, thin {len(thin)}; data_suspect {int(L.data_suspect.sum())}")
    (OUT / "winners_population_build.txt").write_text("\n".join(LOGL) + "\n", encoding="utf-8")


def engine():
    sys.path.insert(0, str(ROOT / "scripts"))
    import engine as EN
    L = pd.read_csv(LIB)
    e = EN.Engine()
    d = e.d
    key = pd.Series(d.index, index=pd.MultiIndex.from_arrays([d.symbol, d.date]))
    ok = L[(~L.data_suspect) & L.f252_date.notna() & ~L.ongoing]
    ok = ok[[(r.symbol, pd.Timestamp(r.f252_date)) in key.index for r in ok.itertuples()]]
    samp = ok.sample(60, random_state=20261018)
    print(f"eligible {len(ok)} of {len(L)}; sampled {len(samp)}")
    for i, r in samp.iterrows():
        pos = int(key[(r.symbol, pd.Timestamp(r.f252_date))])
        sig = e.signature(pos)
        rows, info, out = e.run(sig)
        for k, c in ((5, "engine_median_5"), (20, "engine_median_20"), (60, "engine_median_60")):
            h = out["h"][k]
            L.loc[i, c] = h["med"] if h else np.nan
        L.loc[i, "engine_n"] = out["h"][20]["n"] if out["h"][20] else 0
        L.loc[i, "engine_thin"] = bool(info["thin"])
    L.to_csv(LIB, index=False)
    s = L[L.engine_median_20.notna() | L.engine_n.notna()]
    print(f"engine sample {len(s)}: 20-session median positive in {int((s.engine_median_20 > 0).sum())} ({(s.engine_median_20 > 0).mean():.0%}); 5: {(s.engine_median_5 > 0).mean():.0%}; 60: {(s.engine_median_60 > 0).mean():.0%}; thin {int(s.engine_thin.sum())}")


def md(df, idx=True):
    d = df.reset_index() if idx else df
    rows = ["| " + " | ".join(str(c) for c in d.columns) + " |", "|" + "|".join("---" for _ in d.columns) + "|"]
    rows += ["| " + " | ".join(str(v) for v in r) + " |" for r in d.itertuples(index=False)]
    return "\n".join(rows)


def tables():
    M = pd.read_csv(LIB, parse_dates=["start_date", "peak_date"])
    T = pd.read_csv(THIN, parse_dates=["start_date", "peak_date"])
    for X in (M, T):
        X["year"] = X.start_date.dt.year
        X["dur"] = pd.cut(X.sessions_to_peak, [0, 63, 252, 10000], labels=["sprint <=63", "run 64-252", "multi-year >252"])
        for c in [c for c in X.columns if (c.startswith("stop_") or c.startswith("peak_stop_")) and (c.endswith("kept_half") or c.endswith("hit"))]:
            X[c] = X[c].map({True: 1.0, False: 0.0, "True": 1.0, "False": 0.0})
    O = []

    def p(*a):
        O.append(" ".join(str(x) for x in a))
    Mo = M[~M.data_suspect]
    To = T[~T.data_suspect]
    p(f"liquid episodes {len(M)}, of which data-suspect {int(M.data_suspect.sum())}; analysed {len(Mo)}; thin {len(T)}, data-suspect {int(T.data_suspect.sum())}; names liquid {Mo.symbol.nunique()}")
    p(f"ongoing at 16 Oct 2026 (liquid, analysed): {int(Mo.ongoing.sum())}")
    p("\n== by start year (liquid analysed | thin non-suspect)")
    y = pd.DataFrame({"liquid": Mo.groupby("year").size(), "thin": To.groupby("year").size(), "liquid_5x+": Mo[Mo.multiple >= 5].groupby("year").size(),
                      "liquid_median_x": Mo.groupby("year").multiple.median().round(2), "kmi_at_start": Mo.groupby("year").kmi.sum()}).fillna(0)
    for c in ("liquid", "thin", "liquid_5x+", "kmi_at_start"):
        y[c] = y[c].astype(int)
    p(md(y))
    p(f"total liquid {y.liquid.sum()}, thin {y.thin.sum()}")
    p("\n== by type (liquid analysed)")
    ty = Mo.groupby("type").agg(n=("symbol", "size"), multi_flag=("n_flags", lambda s: int((s > 1).sum())), kmi=("kmi", "sum"))
    ty["share"] = (ty.n / len(Mo)).round(3)
    p(md(ty.sort_values("n", ascending=False)))
    p("\n== flags (not exclusive, liquid analysed)")
    p({f: int(Mo[f].sum()) for f in ["flag_deal", "flag_results", "flag_sponsor", "flag_policy", "flag_shock", "flag_ratecut", "has_material_info"]}, "eps_known", int(Mo.eps_known.sum()), "n_flags dist", Mo.n_flags.value_counts().sort_index().to_dict())
    p("\n== by KMI flag x liquidity tier (all non-suspect; tier by tv_median_60 at start: H>20m, M 5-20m, L 2-5m, thin <=2m or no history)")
    A = pd.concat([Mo, To], ignore_index=True)
    kt = pd.crosstab(A.kmi.map({True: "KMI at start", False: "not KMI"}), A.liq_tier)[["H", "M", "L", "thin"]]
    kt["total"] = kt.sum(axis=1)
    p(md(kt))
    kn = pd.crosstab(A.kmi_now.map({True: "in KMI list 5 Jun 2026", False: "not in it"}), A.liq_tier)[["H", "M", "L", "thin"]]
    p(md(kn))
    p("pre-2019 starts (KMI flag uses the Jan 2019 list):", int(A.pre_2019.sum()))
    p("liquid KMI-at-start median multiple", round(Mo[Mo.kmi].multiple.median(), 2), "non-KMI", round(Mo[~Mo.kmi].multiple.median(), 2), "; thin median", round(To.multiple.median(), 2))
    p("\n== by liquidity tier: n, median multiple, median sessions")
    p(md(A.groupby("liq_tier").agg(n=("symbol", "size"), med_x=("multiple", lambda s: round(s.median(), 2)), p90_x=("multiple", lambda s: round(s.quantile(.9), 2)),
                                    med_sess=("sessions_to_peak", "median"), x5=("multiple", lambda s: int((s >= 5).sum()))).loc[["H", "M", "L", "thin"]]))

    def prof(g):
        f252 = g.ahead_f252_log.dropna()
        r = dict(n=len(g), med_x=round(g.multiple.median(), 2), med_sess=int(g.sessions_to_peak.median()),
                 n_f252=len(f252), ahead_f252=round(f252.median(), 2) if len(f252) else np.nan,
                 ahead_f252_lin=round(g.ahead_f252_lin.dropna().median(), 2) if len(f252) else np.nan,
                 ahead_10=round(g.ahead_10_log.median(), 2), ahead_20=round(g.ahead_20_log.median(), 2), ahead_40=round(g.ahead_40_log.median(), 2))
        rem = g.multiple ** g.ahead_f252_log
        r["rem_x_f252"] = round(rem.median(), 2) if len(f252) else np.nan
        r["f252_rem>=1.5"] = round((rem.dropna() >= 1.5).mean(), 2) if len(f252) else np.nan
        r["rem>=1.5_at10"] = round(((g.multiple ** g.ahead_10_log).dropna() >= 1.5).mean(), 2)
        r["rem>=1.5_at20"] = round(((g.multiple ** g.ahead_20_log).dropna() >= 1.5).mean(), 2)
        e = g[~g.ongoing]
        r["dd60_med"] = round(e.dd60_after_peak.median(), 2)
        r["stop_peak"] = round(e.peak_stop_kept_half.dropna().mean(), 2)
        r["x>1.67"] = round((g.multiple > 5 / 3).mean(), 2)
        for t in ("start", "f252", "s20"):
            k = e[f"stop_{t}_kept_half"].dropna()
            r[f"stop_{t}"] = round(k.mean(), 2) if len(k) else np.nan
        return pd.Series(r)
    p("\n== profile by type (liquid analysed). ahead_* = median share of the log gain still ahead; stop_* = share of non-ongoing runs where a 20% trailing stop entered at start / first 252-high / start+20 keeps more than half the gain to the peak")
    p(md(Mo.groupby("type").apply(prof).sort_values("n", ascending=False)))
    p("ALL liquid:", prof(Mo).to_dict())
    p("\n== profile by duration class (liquid analysed)")
    p(md(Mo.groupby("dur").apply(prof)))
    p("\n== type x duration: n")
    p(md(pd.crosstab(Mo.type, Mo.dur)))
    p("\n== profile by liquidity (H, M, L)")
    p(md(Mo.groupby("liq_tier").apply(prof)))
    p("\n== profile, thin list (non-suspect) by type")
    p(md(To.groupby("type").apply(prof).sort_values("n", ascending=False)))
    p("thin ALL:", prof(To).to_dict())
    p("\n== other run features (liquid analysed), medians")
    r = Mo
    p("upper locks median", r.upper_locks.median(), "share with 0 locks", round((r.upper_locks == 0).mean(), 2), "share >=10", round((r.upper_locks >= 10).mean(), 2))
    p("max 20-session pullback median", round(r.max_pullback_20.median(), 3), "p10", round(r.max_pullback_20.quantile(.1), 3), "max dd in run median", round(r.max_dd_in_run.median(), 3),
      "episodes with a 25% drawdown recovered in run", round((r.n_dd25_recovered_in_run > 0).mean(), 2))
    p("sector move median (peers, where covered)", round(r.sector_move.median(), 2), "n", int(r.sector_move.notna().sum()), "; name beat peers in", round(((r.multiple - 1) > r.sector_move)[r.sector_move.notna()].mean(), 2), "of covered")
    p("index move over run median", round(r.index_move.median(), 2), "n", int(r.index_move.notna().sum()))
    p("brent change median", round(r.brent_change.median(), 2))
    p("regime at start:", r.regime_start.value_counts(dropna=False).to_dict())
    p("fipi net USD mn over run, covered n", int(r.fipi_net_usd_mn.notna().sum()), "median", round(r.fipi_net_usd_mn.median(), 1), "share positive", round((r.fipi_net_usd_mn.dropna() > 0).mean(), 2),
      "; lipi individuals median", round(r.lipi_individuals_net_usd_mn.median(), 1))
    for k in ("financial_result", "material_info", "insider_trade", "insider_buy", "dividend_or_bonus", "credit_rating"):
        p(f"filings: share with >=1 {k} in the 20 sessions up to start: {(r['pre_' + k] > 0).mean():.2f}; during run: {(r['run_' + k] > 0).mean():.2f}")
    p("median filings pre", r.pre_total.median(), "run", r.run_total.median(), "; zero filings pre share", round((r.pre_total == 0).mean(), 2))
    p("delisted among liquid", int(r.delisted.sum()), "; tv median Rs m", round(r.tv_median_60.median() / 1e6, 1))
    p("first 252-high: share of episodes with one in the run", round(r.f252_date.notna().mean(), 2), "; no history", int((~r.has_history).sum()), "; median sessions after start", r.f252_sessions_after_start.median())
    p("f252 multiple at that date median", round(r.f252_x.median(), 2))
    ne = r[~r.ongoing]
    p("dd60 after peak: median", round(ne.dd60_after_peak.median(), 3), "share worse than -20%", round((ne.dd60_after_peak < -0.2).mean(), 2), "-40%", round((ne.dd60_after_peak < -0.4).mean(), 2))
    p("\n== context: policy flag vs market wave, and filing base rates")
    pf = Mo[Mo.flag_policy]
    p(f"policy-flagged {len(pf)}; of them index itself up >=30% over the run: {int((pf.index_move >= 0.30).sum())} ({(pf.index_move >= 0.30).mean():.0%}); sector move minus index move median {(pf.sector_move - pf.index_move).median():.2f}; sector beat index by >=20 points: {int(((pf.sector_move - pf.index_move) >= 0.2).sum())}")
    p("5x+ liquid index move median", round(f5_idx := Mo[Mo.multiple >= 5].index_move.median(), 2), "; multiple/(1+index move) median", round((Mo[Mo.multiple >= 5].multiple / (1 + Mo[Mo.multiple >= 5].index_move)).median(), 2))
    p("5x+ liquid start months:", Mo[Mo.multiple >= 5].start_date.dt.strftime("%Y-%m").value_counts().sort_index().to_dict())
    dtb = pd.read_parquet(D / "daily_table.parquet", columns=["date", "symbol", "liquid", "f_financial_result", "f_material_info", "f_insider_trade", "f_dividend_or_bonus"])
    dtb = dtb.sort_values(["symbol", "date"])
    base = {}
    for c in ("f_financial_result", "f_material_info", "f_insider_trade", "f_dividend_or_bonus"):
        rs = dtb.groupby("symbol")[c].transform(lambda s: s.rolling(21, min_periods=1).sum())
        base[c] = round(float((rs[dtb.liquid.fillna(False).values] > 0).mean()), 2)
    p("baseline share of liquid stock-days with >=1 filing in the last 21 sessions (daily table, 2017-2026):", base)
    del dtb
    ev = pd.read_csv(OUT / "winners_population_breakout_events.csv")
    p("\n== denominator: first 252-highs of liquid names (>Rs2m), by year")
    evy = ev.groupby("year").agg(events=("symbol", "size"), hit50_126=("fwd_max_126", lambda s: round((s >= 1.5).mean(), 3)), hit100_252=("fwd_max_252", lambda s: round((s >= 2).mean(), 3) if s.notna().any() else np.nan))
    p(md(evy))
    p(f"all: events {len(ev)}, +50% within 126 sessions {(ev.fwd_max_126 >= 1.5).mean():.3f}, +100% within 252 {(ev.fwd_max_252 >= 2).mean():.3f}; KMI-at-time {len(ev[ev.kmi])}: {(ev[ev.kmi].fwd_max_126 >= 1.5).mean():.3f} / {(ev[ev.kmi].fwd_max_252 >= 2).mean():.3f}; fwd max 126 median {ev.fwd_max_126.median():.2f}")
    p("\n== engine sample")
    s = M[M.engine_n.notna()]
    s = s[s.engine_n > 0]
    p(f"n with an answer {len(s)}; 20-session median>0: {int((s.engine_median_20 > 0).sum())}; ==0: {int((s.engine_median_20 == 0).sum())}; 5: {int((s.engine_median_5 > 0).sum())}; 60: {int((s.engine_median_60 > 0).sum())}; thin {int(s.engine_thin.sum())}; median of medians 20: {s.engine_median_20.median():.3f}; max {s.engine_median_20.max():.3f}")
    s2 = s.copy()
    s2["pos"] = s2.engine_median_20 > 0
    p(md(s2.groupby("pos").agg(n=("symbol", "size"), med_x=("multiple", "median"), ahead_f252=("ahead_f252_log", "median"), med_sess=("sessions_to_peak", "median"))))
    p("\n== 30 largest liquid episodes (analysed)")
    t30 = Mo.nlargest(30, "multiple")[["symbol", "kmi", "start_date", "peak_date", "multiple", "sessions_to_peak", "liq_tier", "type", "upper_locks", "dd60_after_peak", "ahead_f252_log", "ongoing"]].copy()
    t30["start_date"], t30["peak_date"] = t30.start_date.dt.strftime("%Y-%m-%d"), t30.peak_date.dt.strftime("%Y-%m-%d")
    t30["multiple"] = t30.multiple.round(1)
    t30["dd60_after_peak"] = t30.dd60_after_peak.round(2)
    t30["ahead_f252_log"] = t30.ahead_f252_log.round(2)
    p(md(t30, idx=False))
    p("\n== 5x+ liquid (analysed), sorted by multiple; multi-year = more than 252 sessions to peak")
    f5 = Mo[Mo.multiple >= 5].sort_values("multiple", ascending=False)
    p(f"n {len(f5)}; multi-year {int((f5.sessions_to_peak > 252).sum())}; within 252 sessions {int((f5.sessions_to_peak <= 252).sum())}; ongoing {int(f5.ongoing.sum())}")
    f5t = f5[["symbol", "kmi", "start_date", "peak_date", "multiple", "sessions_to_peak", "type"]].copy()
    f5t["start_date"], f5t["peak_date"] = f5t.start_date.dt.strftime("%Y-%m-%d"), f5t.peak_date.dt.strftime("%Y-%m-%d")
    f5t["multiple"] = f5t.multiple.round(1)
    p(md(f5t, idx=False))
    p("5x+ thin non-suspect:", int((To.multiple >= 5).sum()), "; 10x+:", int((To.multiple >= 10).sum()))
    p("\n== 5x+ liquid: stop outcomes (non-ongoing)")
    e5 = f5[~f5.ongoing]
    p("n", len(e5), "stop from start keeps half:", round(e5.stop_start_kept_half.mean(), 2), "median exit multiple from start", round(e5.stop_start_exit_mult.median(), 2), "; from f252:", round(e5.stop_f252_kept_half.mean(), 2), "median exit mult", round(e5.stop_f252_exit_mult.median(), 2))
    ne = Mo[~Mo.ongoing]
    p("all liquid analysed non-ongoing: median stop exit mult from start", round(ne.stop_start_exit_mult.median(), 2), "from f252", round(ne.stop_f252_exit_mult.median(), 2), "from s20", round(ne.stop_s20_exit_mult.median(), 2))
    p("\n== exit multiple of a trailing stop of width w entered at the first 252-high / start+20 / start (liquid analysed, non-ongoing; hindsight: these are all winners)")
    rows_ = []
    for nm, g_ in (("all liquid", ne), ("multi-year", ne[ne.sessions_to_peak > 252]), ("sprint+run", ne[ne.sessions_to_peak <= 252]), ("5x+", e5)):
        for tag in ("f252", "s20", "start"):
            for w, col in ((20, f"stop_{tag}_exit_mult"), (30, f"stop30_{tag}_exit_mult"), (40, f"stop40_{tag}_exit_mult")):
                v = g_[col].dropna()
                rows_.append(dict(group=nm, entry=tag, stop=f"{w}%", n=len(v), median_x=round(v.median(), 2), mean_x=round(v.mean(), 2), p25=round(v.quantile(.25), 2),
                                  share_gt_1_25=round((v > 1.25).mean(), 2), share_gt_2=round((v > 2).mean(), 2), share_lt_1=round((v < 1).mean(), 2)))
    p(md(pd.DataFrame(rows_), idx=False))
    p("\n== pilot six names in the library (any list)")
    A2 = pd.concat([M.assign(L="liquid"), T.assign(L="thin")], ignore_index=True)
    z = A2[A2.symbol.isin(["PRL", "MACFL", "TPLT", "QUICE", "CRTM", "JVDC"]) & (A2.start_date >= "2024-01-01")][["symbol", "L", "start_date", "peak_date", "multiple", "sessions_to_peak", "tv_median_60", "type", "ahead_f252_log"]].copy()
    z["start_date"], z["peak_date"] = z.start_date.dt.strftime("%Y-%m-%d"), z.peak_date.dt.strftime("%Y-%m-%d")
    z["multiple"] = z.multiple.round(2)
    z["tv_median_60"] = (z.tv_median_60 / 1e6).round(2)
    p(md(z, idx=False))
    # ---- compact tables for the write-up
    def compact(g):
        q = prof(g)
        n_f = int(q.n_f252)
        return pd.Series({"n": int(q.n), "median x": f"{q.med_x:.2f}", "sessions to peak": int(q.med_sess), "ahead at 1st 252-high (n)": f"{q.ahead_f252:.2f} ({n_f})" if n_f else "none",
                          "ahead s10": f"{q.ahead_10:.2f}", "ahead s20": f"{q.ahead_20:.2f}", "ahead s40": f"{q.ahead_40:.2f}", "median 60-session drawdown after peak": f"{q.dd60_med:.0%}",
                          "stop from peak keeps >half": f"{q.stop_peak:.0%}", "live 20% stop from 1st 252-high keeps >half": "n/a" if np.isnan(q.stop_f252) else f"{q.stop_f252:.0%}"})
    SN = {}
    SN["type"] = md(Mo.groupby("type").apply(compact).loc[ty.sort_values("n", ascending=False).index])
    allrow = compact(Mo).to_frame("all liquid").T
    SN["all"] = md(allrow)
    SN["dur"] = md(Mo.groupby("dur").apply(compact))
    SN["year"] = md(y)
    SN["typecount"] = md(ty.sort_values("n", ascending=False)[["n", "share", "multi_flag", "kmi"]])
    SN["kmi"] = md(kt)
    SN["top30"] = md(t30[["symbol", "kmi", "start_date", "peak_date", "multiple", "sessions_to_peak", "liq_tier", "type", "upper_locks"]], idx=False)
    SN["x5"] = md(f5t, idx=False)
    SN["tier"] = md(A.groupby("liq_tier").agg(n=("symbol", "size"), median_x=("multiple", lambda s: round(s.median(), 2)), p90_x=("multiple", lambda s: round(s.quantile(.9), 2)),
                                              median_sessions=("sessions_to_peak", "median"), x5plus=("multiple", lambda s: int((s >= 5).sum()))).loc[["H", "M", "L", "thin"]])
    ex = pd.DataFrame(rows_)
    ex = ex[(ex.stop.isin(["20%", "30%", "40%"])) & (ex.entry == "f252")][["group", "stop", "n", "median_x", "mean_x", "share_gt_1_25", "share_gt_2", "share_lt_1"]]
    SN["exit"] = md(ex, idx=False)
    (OUT / "winners_population_snippets.md").write_text("\n\n".join(f"<<{k}>>\n{v}" for k, v in SN.items()) + "\n", encoding="utf-8")
    (OUT / "winners_population_tables.txt").write_text("\n".join(O) + "\n", encoding="utf-8")
    print("\n".join(O))


if MODE == "build":
    build()
elif MODE == "engine":
    engine()
elif MODE == "tables":
    tables()
