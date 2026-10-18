"""Results-day gaps (R) and sector policy windows (P), PSX KMI names.
Run: .venv/Scripts/python.exe -I scripts/tests/results_gap_and_policy.py [R|P]   (no argument = both)
Raw output: tests/out/results_gap_and_policy.txt. Write-up: tests/results_gap_and_policy.md.
Event timestamp cleaning is copied from results_surprise_drift.py (announce_dt re-searched in the announcements file).
"""
import sys, io, re, calendar, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

WHICH = sys.argv[1] if len(sys.argv) > 1 else "RP"
buf = io.StringIO()
def out(*a):
    s = " ".join(str(x) for x in a); print(s); buf.write(s + "\n")
def pct(x, d=1):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:+.{d}%}"

COST, SLIP, SLIP_BELOW, LAST = 0.005, 0.005, 20e6, pd.Timestamp("2026-10-16")
LOCK = 0.0945                  # close within 0.5% of the +-10% limit
MAXWAIT, TRAIL, TRAIL_CAP = 10, 0.20, 250
RULES = ["h20", "h60", "h120", "trail"]
SEED, NDRAW = 20261018, 300
rng = np.random.default_rng(SEED)

close, vol, tv = P.load_panel()
dates, N = close.index, len(close.index)
cols = list(close.columns); cidx = {s: i for i, s in enumerate(cols)}
adj = pd.read_parquet(ROOT / "data" / "panel_close_adj.parquet").reindex(index=dates, columns=cols)
# repair: the corporate-actions table misses some splits (STL 2026-03, BNL 2025-12, BECO 2025-11 fall ~89% in one session).
# A one-day fall of 35% or more, beyond what the 10% daily limit allows over the sessions elapsed, is a corporate action, not a trade: set it to zero.
_ix = pd.DataFrame(np.arange(N)[:, None] + 0.0 * adj.values, dates, cols).where(adj.notna())
_gap = (_ix - _ix.ffill().shift(1)).clip(lower=1)
_r = adj / adj.ffill().shift(1) - 1
REPAIRED = (_r < 0.9 ** _gap * 0.99 - 1) & (_r <= -0.35) & (_gap <= 3)
_lvl = (1 + _r.mask(REPAIRED, 0.0).fillna(0.0)).cumprod().where(adj.notna())
adj = _lvl
Aadj = adj.values
Aff = adj.ffill().values
MED = P._med_tv(tv).reindex(index=dates, columns=cols).values      # trailing 60 sessions up to the PREVIOUS day

# regime: 6M T-bill above / below policy rate, as of each panel date
tb = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"]).set_index("date").y6m
pr = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"]).set_index("date").rate
tbd = tb.reindex(tb.index.union(dates)).ffill().reindex(dates)
prd = pr.reindex(pr.index.union(dates)).ffill().reindex(dates)
REG = np.where(tbd.isna() | prd.isna(), "NA", np.where(tbd > prd, "tb>pr", "tb<=pr"))

def stats(x):
    x = np.asarray(x, float)
    if len(x) == 0: return None
    return dict(n=len(x), mean=x.mean(), med=np.median(x), win=(x > 0).mean(), p50=(x > .5).mean(), m30=(x < -.3).mean(), worst=x.min())
def fmt(s):
    if s is None: return "n 0"
    return f"n {s['n']}, mean {pct(s['mean'])}, median {pct(s['med'])}, win {s['win']:.0%}, >+50% {s['p50']:.0%}, <-30% {s['m30']:.0%}, worst {pct(s['worst'])}"

# ================================================================= R
def run_R():
    syms_all = sorted(pd.read_csv(ROOT / 'data/fundamentals/quarterly_eps.csv').symbol.unique())
    out("== R. RESULTS-DAY GAPS. Panel", close.shape, dates[0].date(), "to", dates[-1].date())
    rp = REPAIRED[syms_all].stack(); rp = rp[rp]
    out(f"Corporate-action repair on the adjusted series (one-day fall of 35%+, beyond the limit): {len(rp)} name-days in the EPS symbols: " + ", ".join(f"{a.date()} {b} {_r.at[a, b]:+.0%}" for a, b in rp.index))
    out("Entry: close of the first session after the reaction session that is traded and not locked (upper or lower, within 0.5% of 10%), within", MAXWAIT, "sessions, else no trade. Exits: fixed 20/60/120 sessions, or 20% trailing stop on closes (cap 250 sessions); an exit waits for the next session that is not lower-locked.")
    out(f"Cost {COST:.1%} round trip, plus {SLIP:.1%} slippage when trailing-60-session median traded value < Rs{SLIP_BELOW/1e6:.0f}m. Universe: Rs5m median traded value (point in time). Returns: panel_close_adj (total return where the cash table has it).")
    ann = pd.read_parquet(ROOT / "data/announcements.parquet")
    ann["dt"] = ann.datetime.dt.tz_localize(None)
    e = pd.read_csv(ROOT / "data/fundamentals/quarterly_eps.csv", parse_dates=["fiscal_quarter_end"]).rename(columns={"fiscal_quarter_end": "qe"})
    syms = sorted(e.symbol.unique())
    O = np.full((N, len(cols)), np.nan); C = O.copy(); V = O.copy()
    for s in syms:
        x = pd.read_csv(ROOT / "data/prices_raw" / f"{s}.csv", parse_dates=["date"]).drop_duplicates("date", keep="last").set_index("date").reindex(dates)
        j = cidx[s]
        O[:, j], C[:, j], V[:, j] = x.open, x.close, x.volume
    obs = (V > 0) & (C > 0)
    Cprev = pd.DataFrame(np.where(obs, C, np.nan)).ffill().shift(1).values
    rr = C / Cprev - 1
    acts = pd.read_csv(ROOT / "data/corporate_actions.csv", parse_dates=["ex_date"])
    ca = np.zeros(obs.shape, bool)
    for r in acts.itertuples():
        if r.symbol in cidx:
            k = dates.searchsorted(r.ex_date)
            if k < N: ca[k, cidx[r.symbol]] = True
    lockUp = obs & (rr >= LOCK) & (rr <= 0.1055) & ~ca
    lockDn = obs & (rr <= -LOCK) & (rr >= -0.1055) & ~ca
    volmed = pd.DataFrame(np.where(obs, V, np.nan)).rolling(20, min_periods=5).median().shift(1).values
    vratio = np.where(obs, V / volmed, np.nan)
    sj = [cidx[s] for s in syms]
    out(f"Upper-lock days among the {len(syms)} EPS symbols: {int(lockUp[:, sj].sum())}; lower-lock days: {int(lockDn[:, sj].sum())} (corporate-action ex-dates are not flagged as locks)")

    # ---- events (cleaning copied from results_surprise_drift.py)
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
    e["cur"] = pd.to_datetime(e.announce_dt.str.slice(0, 19), errors="coerce")
    e["cur_trans"] = e.announce_title.fillna("").str.lower().str.contains("transmission|annual report")
    _t = e.announce_title.fillna("").str.lower()
    e["cur_bad"] = e.announce_dt.notna() & ~e.cur_trans & (_t.str.contains("revoked|other than|board meeting|conclusion|" + NOTRES) | ~_t.str.contains("result"))
    ME = pd.offsets.MonthEnd(0)
    ix = e.set_index(["symbol", "qe"])
    k_ly = list(zip(e.symbol, [q + pd.DateOffset(months=-12) + ME for q in e.qe]))
    e["eps_ly"] = ix["eps_basic"].reindex(pd.MultiIndex.from_tuples(k_ly, names=["symbol", "qe"])).values
    fym = {}
    y = fr[(fr.kind == "Y") & ~fr.is_trans & ~fr.bad & fr.pdate.notna()]
    for s, g in y.groupby("symbol"): fym[s] = int(g.pdate.dt.month.mode().iloc[0])
    yt = e[e.announce_title.fillna("").str.lower().str.contains("year ended") & ~e.cur_trans]
    for s, g in yt.groupby("symbol"):
        if s not in fym: fym[s] = int(g.qe.dt.month.mode().iloc[0])
    def qtype(s, qe):
        if s not in fym: return "NA"
        return {0: "Q4", 3: "Q1", 6: "Q2", 9: "Q3"}.get((qe.month - fym[s]) % 12, "NA")
    e["qtype"] = [qtype(s, q) for s, q in zip(e.symbol, e.qe)]
    new = []
    for r in e.itertuples():
        if pd.isna(r.cur):
            new.append(pd.NaT); continue
        g = FR.get(r.symbol); pick = None
        if g is not None:
            ok = (g.dt >= r.qe + pd.Timedelta(days=7)) & (g.dt <= (r.qe + pd.Timedelta(days=150) if r.cur_bad else r.cur))
            pd_ok = g.pdate.notna() & ((g.pdate - r.qe).abs() <= pd.Timedelta(days=4))
            und = g.pdate.isna()
            kind_ok = ((g.kind == "Y") & (r.qtype in ("Q4", "NA"))) | ((g.kind == "H") & (r.qtype in ("Q2", "NA"))) | \
                      ((g.kind == "Q") & (r.qtype != "Q4")) | (g.kind == "U")
            c = g[ok & (pd_ok | (und & kind_ok))]
            if len(c): pick = c.iloc[0]
        new.append(pick["dt"] if pick is not None else (pd.NaT if (r.cur_trans or r.cur_bad) else r.cur))
    e["ann"] = new
    def t0_idx(ts):
        if pd.isna(ts): return -1
        after = ts.hour * 60 + ts.minute > 15 * 60 + 30
        i = dates.searchsorted(ts.normalize(), side="right" if after else "left")
        return int(i) if i < N else -1
    e["i0"] = [t0_idx(t) for t in e.ann]
    e["pre_open"] = [(t.hour * 60 + t.minute) < 9 * 60 + 15 if pd.notna(t) else False for t in e.ann]
    e["post_close"] = [(t.hour * 60 + t.minute) > 15 * 60 + 30 if pd.notna(t) else False for t in e.ann]
    e["s"] = e.symbol.map(cidx)
    out(f"EPS rows {len(e)}, symbols {e.symbol.nunique()}; with a cleaned result timestamp and a reaction session on the panel: {int((e.i0 >= 0).sum())}")
    ev = e[e.i0 >= 0].copy()
    ev["liq"] = [bool(MED[i, j] > 5e6) if np.isfinite(MED[i, j]) else False for i, j in zip(ev.i0, ev.s)]
    ev["day_ret"] = [rr[i, j] if obs[i, j] else np.nan for i, j in zip(ev.i0, ev.s)]
    ev["vr"] = [vratio[i, j] for i, j in zip(ev.i0, ev.s)]
    ev["up_lock"] = [bool(lockUp[i, j]) for i, j in zip(ev.i0, ev.s)]
    ev["traded"] = [bool(obs[i, j]) for i, j in zip(ev.i0, ev.s)]
    ev["eps_g"] = np.where(ev.eps_ly > 0, ev.eps_basic / ev.eps_ly - 1, np.nan)
    ev["i_gap"] = np.where(ev.pre_open | ev.post_close, ev.i0, ev.i0 + 1).clip(max=N - 1)
    ev["strict_gap"] = [O[i, j] / Cprev[i, j] - 1 if obs[i, j] else np.nan for i, j in zip(ev.i_gap, ev.s)]
    ev["strict_vr"] = [vratio[i, j] for i, j in zip(ev.i_gap, ev.s)]
    nliq = ev[ev.liq & ev.traded].copy()
    out(f"Events with the reaction session traded and the name liquid (Rs5m): {len(nliq)} in {nliq.symbol.nunique()} symbols; by year {nliq.groupby(nliq.i0.map(lambda i: dates[i].year)).size().to_dict()}")
    pre_share = (nliq.pre_open | nliq.post_close).mean()
    out(f"Share of results announced before 09:15 or after 15:30 (pure opening-gap news): {pre_share:.1%}; the other {1-pre_share:.1%} is intraday news (reaction session = announcement day, so a '5% gap' is the day's close over the prior close)")
    A_ = nliq[(nliq.day_ret >= 0.05) & (nliq.vr >= 2) & (nliq.eps_g >= 0.30)]
    B_ = nliq[nliq.up_lock]
    C_ = nliq[(nliq.eps_basic > 0) & (nliq.eps_ly <= 0) & (nliq.day_ret > 0)]
    A2 = nliq[(nliq.strict_gap >= 0.05) & (nliq.strict_vr >= 2) & (nliq.eps_g >= 0.30)]
    SIG = {"a_gap_eps30": A_, "b_upperlock": B_, "c_loss_to_profit": C_}
    out(f"Signals before fills: (a) reaction-day return >=5% on 2x volume and EPS YoY >=30%: {len(A_)}; (a-strict) opening gap >=5% on the first session that opens after the news, 2x volume, EPS >=30%: {len(A2)}; (b) upper lock on the reaction session: {len(B_)}; (c) EPS loss to profit with a positive reaction: {len(C_)}")
    out("Overlaps: a&b", len(set(A_.index) & set(B_.index)), " a&c", len(set(A_.index) & set(C_.index)), " b&c", len(set(B_.index) & set(C_.index)))
    out("Context, all liquid events: share with day return >=5% on 2x volume", f"{((nliq.day_ret >= .05) & (nliq.vr >= 2)).mean():.1%}", " share upper-locked", f"{nliq.up_lock.mean():.1%}", " share with EPS up >=30% YoY", f"{(nliq.eps_g >= .3).mean():.1%}")

    # ---- trade machinery
    def first_ok(j, i):
        for k in range(i + 1, min(i + 1 + MAXWAIT, N)):
            if obs[k, j] and not lockUp[k, j] and not lockDn[k, j]: return k
        return -1
    def cost_at(j, k):
        m = MED[k, j]
        return COST + (SLIP if (not np.isfinite(m) or m < SLIP_BELOW) else 0.0)
    def exit_idx(j, k, rule):
        a = Aadj[:, j]
        if rule.startswith("h"):
            x = k + int(rule[1:])
            if x >= N: return N - 1, True
        else:
            end = min(k + TRAIL_CAP, N - 1)
            seg, ok = a[k:end + 1], obs[k:end + 1, j]
            pk = np.fmax.accumulate(np.where(ok, seg, np.nan))
            hit = np.where(ok & (seg <= (1 - TRAIL) * pk))[0]
            if len(hit): x = k + hit[0]
            else:
                x = k + TRAIL_CAP
                if x >= N: return N - 1, True
        while x < N and not (obs[x, j] and not lockDn[x, j]): x += 1
        if x >= N: return N - 1, True
        return x, False
    def trade(j, k, rule):
        x, cens = exit_idx(j, k, rule)
        a0, a1 = Aadj[k, j], Aff[x, j]
        if not (np.isfinite(a0) and np.isfinite(a1)): return None
        c = cost_at(j, k)
        return dict(k=k, x=x, cens=cens, gross=a1 / a0 - 1, net=a1 / a0 - 1 - c, cost=c)

    def run_signal(df, col="i0"):
        rows = []
        for r in df.itertuples():
            i0 = getattr(r, col)
            k = first_ok(r.s, i0)
            if k < 0: rows.append(dict(sym=r.symbol, j=r.s, i0=i0, fill=False)); continue
            for rule in RULES:
                t = trade(r.s, k, rule)
                if t: rows.append(dict(sym=r.symbol, j=r.s, i0=i0, fill=True, rule=rule, season=f"{dates[k].year}Q{dates[k].quarter}", year=dates[k].year, reg=REG[k], delay=k - i0, **t))
        return pd.DataFrame(rows)

    def sleeve(tr):
        """Rs50k, up to 3 positions, every signal in entry order, each sized at 1/3 of equity (or cash if less). Cost half at entry, half at exit."""
        tr = tr[~tr.cens].sort_values(["k", "sym"])
        if tr.empty: return None
        cash, pos, taken, inv = 50000.0, [], 0, 0
        d0, d1 = int(tr.k.min()), int(tr.x.max())
        events = list(tr.itertuples()); ei = 0; eq = []
        def val(p, d): return p["size"] * (1 - p["c"] / 2) * Aff[min(d, p["x"]), p["j"]] / p["a0"]
        for d in range(d0, d1 + 1):
            for p in list(pos):
                if p["x"] <= d:
                    cash += val(p, p["x"]) * (1 - p["c"] / 2); pos.remove(p)
            while ei < len(events) and int(events[ei].k) == d:
                r = events[ei]; ei += 1
                if len(pos) >= 3: continue
                tot = cash + sum(val(p, d) for p in pos)
                size = min(cash, tot / 3)
                if size <= 0: continue
                cash -= size
                pos.append(dict(x=int(r.x), j=int(r.j), c=r.cost, a0=Aadj[int(r.k), int(r.j)], size=size)); taken += 1
            eq.append(cash + sum(val(p, d) for p in pos)); inv += bool(pos)
        eq = np.array(eq)
        return dict(mult=eq[-1] / 50000, mdd=(eq / np.maximum.accumulate(eq) - 1).min(), inv=inv / len(eq), taken=taken)

    # ---- placebo
    cand_post = {}
    for j, g in nliq.groupby("s"):
        c = set()
        for i0 in g.i0:
            for k in range(i0 + 1, min(i0 + 61, N)):
                if obs[k, j] and not lockUp[k, j] and not lockDn[k, j] and np.isfinite(MED[k, j]) and MED[k, j] > 5e6: c.add(k)
        cand_post[j] = np.array(sorted(c))
    yr = np.array([d.year for d in dates])
    def cand_year(j, y):
        m = obs[:, j] & ~lockUp[:, j] & ~lockDn[:, j] & (yr == y) & (np.nan_to_num(MED[:, j]) > 5e6)
        return np.where(m)[0]
    cache = {}
    def tcache(j, k, rule):
        key = (j, k, rule)
        if key not in cache: cache[key] = trade(j, k, rule)
        return cache[key]
    def placebo(df, kind):
        base = [(int(r.s), int(r.i0)) for r in df.itertuples()]
        pools = [cand_post.get(j, np.array([], int)) if kind == "post" else cand_year(j, dates[min(i0 + 1, N - 1)].year) for j, i0 in base]
        res = {}
        for rule in RULES:
            draws = []
            for _ in range(NDRAW):
                v = []
                for (j, i0), c in zip(base, pools):
                    if len(c) == 0: continue
                    t = tcache(j, int(rng.choice(c)), rule)
                    if t and not t["cens"]: v.append(t["net"])
                draws.append(stats(v))
            res[rule] = [d for d in draws if d]
        return res

    for name, df in SIG.items():
        out(f"\n---------------- SIGNAL {name}: {len(df)} reaction-session events, {df.symbol.nunique()} symbols")
        tr = run_signal(df)
        if "fill" not in tr or tr.empty: out("no trades"); continue
        filled = tr[tr.fill == True].copy(); nf = tr[tr.fill == False]; filled["cens"] = filled.cens.astype(bool)
        ev_f = filled.drop_duplicates(["sym", "i0"])
        out(f"unfillable within {MAXWAIT} sessions: {len(nf)}; filled {len(ev_f)}; delay from signal day: {ev_f.delay.value_counts().sort_index().to_dict()}")
        out(f"independent episodes: {ev_f.season.nunique()} entry quarters, {ev_f.sym.nunique()} symbols; entry years {ev_f.year.value_counts().sort_index().to_dict()}; regime {ev_f.reg.value_counts().to_dict()}")
        pl = (placebo(df, "post"), placebo(df, "year"))
        for rule in RULES:
            t = filled[filled.rule == rule]; tc = t[~t.cens]; s = stats(tc.net)
            out(f"\n[{name} | exit {rule}] censored (window past data end, excluded) {int(t.cens.sum())}. NET: {fmt(s)}; gross median {pct(np.median(tc.gross)) if len(tc) else '-'}")
            for lab, d in (("post-result placebo", pl[0]), ("same-year placebo", pl[1])):
                dr = d[rule]
                if not dr or s is None: continue
                med = np.array([x["med"] for x in dr]); mean = np.array([x["mean"] for x in dr]); win = np.array([x["win"] for x in dr]); p50 = np.array([x["p50"] for x in dr])
                out(f"   {lab}: median of medians {pct(np.median(med))} (5-95%: {pct(np.quantile(med,.05))} to {pct(np.quantile(med,.95))}), mean {pct(mean.mean())}, win {win.mean():.0%}, >+50% {p50.mean():.1%}; event median minus placebo {pct(s['med']-np.median(med))}; p(placebo median >= event) {(med >= s['med']).mean():.3f}; p(placebo mean >= event) {(mean >= s['mean']).mean():.3f}")
            sl = sleeve(t)
            out("   sleeve Rs50k, <=3 positions: " + ("none" if sl is None else f"final {sl['mult']:.2f}x, max drawdown {sl['mdd']:.0%}, invested {sl['inv']:.0%} of days, trades taken {sl['taken']} of {len(tc)}"))
            if rule in ("h60", "trail"):
                out("   by entry year: " + "; ".join(f"{y}: {fmt(stats(g.net))}" for y, g in tc.groupby("year")))
                out("   by regime:     " + "; ".join(f"{r}: {fmt(stats(g.net))}" for r, g in tc.groupby("reg")))
        for rule in ("h60", "trail"):
            t6 = filled[(filled.rule == rule) & (~filled.cens)].sort_values("net")
            out(f"   [{rule}] worst 3: " + ", ".join(f"{r.sym} {dates[int(r.k)].date()} {pct(r.net)}" for r in t6.head(3).itertuples()) + " | best 3: " + ", ".join(f"{r.sym} {dates[int(r.k)].date()} {pct(r.net)}" for r in t6.tail(3).itertuples()) + f" | top-3 share of summed net return: {t6.net.nlargest(3).sum() / t6.net.sum():.0%}; median without the top 3: {pct(t6.net.iloc[:-3].median())}")
        filled.to_csv(ROOT / "tests/out" / f"results_gap_R_{name}.csv", index=False)

    out("\n---------------- ROBUSTNESS: (a) with the strict opening-gap definition, events", len(A2))
    f2 = run_signal(A2, "i_gap"); f2 = f2[f2.fill == True].copy(); f2["cens"] = f2.cens.astype(bool)
    for rule in RULES:
        t = f2[(f2.rule == rule) & (~f2.cens)]
        out(f"[strict a | {rule}] NET: {fmt(stats(t.net))}")
    out("\n---------------- BASELINE: every liquid result event, same entry and exits")
    fb = run_signal(nliq); fb = fb[fb.fill == True].copy(); fb["cens"] = fb.cens.astype(bool)
    for rule in RULES:
        t = fb[(fb.rule == rule) & (~fb.cens)]
        out(f"[all results | {rule}] NET: {fmt(stats(t.net))}")

    # ---- live screen
    out("\n---------------- LIVE SCREEN: reaction sessions in the last 20 sessions to", dates[-1].date())
    lv = ev[ev.i0 >= N - 20].copy()
    out(f"result events with a reaction session in the window: {len(lv)} ({int((lv.liq & lv.traded).sum())} liquid); symbols with the latest EPS row in the file: {lv.symbol.nunique()}")
    for r in lv.sort_values("i0").itertuples():
        fa = bool(r.day_ret >= .05 and r.vr >= 2 and r.eps_g >= .30); fb_ = bool(r.up_lock); fc = bool(r.eps_basic > 0 and r.eps_ly <= 0 and r.day_ret > 0)
        if fa or fb_ or fc:
            out(f"  {r.symbol} reaction {dates[r.i0].date()} day return {pct(r.day_ret)}, volume x{r.vr:.1f}, EPS {r.eps_basic} vs {r.eps_ly}, upper lock {fb_}, liquid {bool(r.liq)} -> a {fa}, b {fb_}, c {fc}; total return since the reaction-day close {pct(Aff[-1, int(r.s)] / Aff[r.i0, int(r.s)] - 1)}")

# ================================================================= P
SECT = {   # copied from scripts/sector_momentum.py
 "Oil refineries": "ATRL PRL NRL CNERGY", "E&P": "OGDC PPL MARI", "OMC": "PSO WAFI HTL BPL",
 "Power": "HUBC KEL EPQL KOHE SEL GEMMEL", "Fertilizer": "FFC EFERT FATIMA ENGROH",
 "Cement": "LUCK DGKC MLCF FCCL KOHC CHCC PIOC ACPL POWER GWLC THCCL FLYNG FECTC DCL DNCC SMCPL",
 "Autos": "SAZEW GAL GHNI HCAR MTL AGTL BWHL EXIDE LOADS GTYR ATBA HINO",
 "Islamic banks & fin.": "MEBL FABL BIPL FHAM OLPM ORM PQGTL PAKQATAR FPJM TRSM",
 "Gas utilities & misc": "SNGP SSGC PIBTL PAEL SIEM PSEL PICT BLUEX SLGL FCL EMCO WAVES JVDC"}
# id, type, basket ("MARKET" = KMI All Share TR itself), expected direction for the sector (+1/-1/0 mixed), first public, decision, note/source
EV = [
 ("REFPOL26", "policy approval", "Oil refineries", +1, "2026-07-13", "2026-07-28", "refinery policy fast-tracked 13 Jul (repo: unverified), CCoE approval 28 Jul (repo: Dawn 25 Sep)"),
 ("DIESELCAP26", "regulated price", "Oil refineries", -1, "2026-08-20", "2026-08-20", "HSD crack cap effective 20 Aug 2026 (refineries.md); announcement date not found, so no lead"),
 ("OMCDIESELCUT26", "regulated price", "OMC", -1, "2026-04-11", "2026-04-11", "diesel cut Rs135/l, OMC inventory loss est. Rs106bn (omc.md)"),
 ("OMCMARGIN23", "regulated price", "OMC", +1, "2023-09-07", "2023-09-15", "ECC margin rise Rs1.87/l: Geo article 7 Sep 2023 (meeting inferred 6 Sep), effective 15 Sep; later reported delayed"),
 ("SUPERTAXFCC26", "tax", "E&P", +1, "2026-01-27", "2026-01-27", "Federal Constitutional Court order on super tax, per-concession calculation (exploration_production.md)"),
 ("WELLHEAD26", "regulated price", "E&P", +1, "2026-09-04", "2026-09-04", "OGRA wellhead gas +8-10% Jul-Dec 2026, Nukta 4 Sep (exploration_production.md); some fields pending"),
 ("GIDC20", "tax", "Fertilizer", -1, "2020-08-13", "2020-08-13", "Supreme Court GIDC verdict Rs417bn, 13 Aug 2020 (ProPakistani, Profit)"),
 ("FEEDGAS24", "regulated price", "Fertilizer", -1, "2024-02-14", "2024-02-14", "ECC gas price rise incl. fertilizer feed/fuel gas, ProPakistani 14 Feb 2024; earlier proposal date not found"),
 ("CONSTRPKG20", "policy approval", "Cement", +1, "2020-04-03", "2020-04-14", "construction package announced 3 Apr 2020 (KPMG), ordinance 14 Apr (Pakistan Today; ProPakistani says 19 Apr)"),
 ("CEMFED24", "tax", "Cement", -1, "2024-06-12", "2024-06-28", "FY25 budget 12 Jun 2024 raises cement FED (to Rs4/kg; sources disagree on the old rate); NA passed Finance Bill 28 Jun"),
 ("SUPERTAX22", "tax", "Cement", -1, "2022-06-24", "2022-06-29", "10% super tax on 13 sectors incl. cement: announced 24 Jun 2022, NA approval 29 Jun (Dawn, Business Recorder)"),
 ("IPPPROBE20", "policy approval", "Power", -1, "2020-04-21", "2020-04-21", "cabinet decision to publish IPP inquiry report (power.md)"),
 ("IPPTERM24", "policy approval", "Power", -1, "2024-10-10", "2024-10-10", "cabinet/PM announce early termination of 5 IPP PPAs, Hub Power disclosure same day (Dawn 10 Oct 2024)"),
 ("CIRCDEBT25", "settlement", "Power", +1, "2025-09-24", "2025-09-24", "Rs1.225tr bank financing signed ~24 Sep 2025; term sheets reported Jun 2025 (day not found); ECC guarantee Nov 2025 (day not found)"),
 ("GASCD26", "settlement", "Gas utilities & misc", +1, "2026-08-19", None, "Rs1.495tr gas circular-debt plan unveiled 19 Aug 2026; decision pending at 16 Oct 2026"),
 ("AUTOPOL26", "policy approval", "Autos", 0, "2026-09-14", None, "2026-31 auto policy draft approved by PM 14 Sep 2026 (catalyst_trade.md); final approval pending"),
 ("AIDEP21", "policy approval", "Autos", +1, "2021-12-17", "2021-12-17", "AIDEP 2021-26 ECC approval, Business Recorder print 17 Dec 2021 (meeting a Thursday); approximate"),
 ("RATECUT20", "rate cut", "MARKET", +1, "2020-03-17", "2020-03-17", "first cut of the 2020 cycle (policy_rate_decisions.csv)"),
 ("RATECUT24", "rate cut", "MARKET", +1, "2024-06-10", "2024-06-10", "first cut of the 2024-25 cycle (policy_rate_decisions.csv)"),
 ("RATECUT25", "rate cut", "MARKET", +1, "2025-12-15", "2025-12-15", "cut after a pause, not a cycle start (policy_rate_decisions.csv)"),
 ("IMFSBA23", "macro deal", "Islamic banks & fin.", +1, "2023-06-30", "2023-07-12", "IMF SBA staff agreement 30 Jun 2023, board 12 Jul 2023 (islamic_banks_financials.md)"),
 ("MSCI21", "index", "MARKET", -1, "2021-09-07", "2021-11-30", "MSCI announces Pakistan EM to Frontier 7 Sep 2021, effective Nov 2021 review (Profit says 30 Nov, Pakistan Today 1 Dec)"),
]

def run_P():
    out("== P. SECTOR POLICY WINDOWS. Panel", dates[0].date(), "to", dates[-1].date())
    out("Baskets: equal-weight daily-rebalanced total-return (panel_close_adj, forward-filled, corporate-action repair) of the scripts/sector_momentum.py names present in the panel. Benchmark: KMI All Share total return (data/macro/kmiallshr.csv).")
    out("Entry = close of the session AFTER the first session on or after the date (signal at close t, fill next close). Net = excess minus 1.0% (0.5% round trip plus 0.5% slippage for a multi-name basket). MARKET rows use the KMI All Share TR itself (absolute).")
    kmi = pd.read_csv(ROOT / "data/macro/kmiallshr.csv", parse_dates=["date"]).set_index("date")["close"].reindex(dates).ffill()
    kr = kmi.pct_change()
    lv = pd.DataFrame(Aff, dates, cols)
    br = {}
    for sec, names in SECT.items():
        got = [n for n in names.split() if n in cidx]
        r = lv[got].pct_change(fill_method=None)
        br[sec] = r.mean(axis=1, skipna=True).fillna(0.0)
        miss = sorted(set(names.split()) - set(got))
        out(f"  basket {sec}: {len(got)} of {len(names.split())} names in panel" + (f" (missing {' '.join(miss)})" if miss else ""))
    lvl = {k: (1 + v).cumprod().values for k, v in br.items()}
    lvl["MARKET"] = (1 + kr.fillna(0.0)).cumprod().values
    kl = lvl["MARKET"]
    def eidx(date):
        i = int(dates.searchsorted(pd.Timestamp(date)))
        return i + 1 if i + 1 < N else None
    H = [5, 20, 60, 120]
    def exc(sec, e, h):
        if e is None or h <= 0 or e + h >= N: return np.nan
        b = lvl[sec][e + h] / lvl[sec][e] - 1
        return b if sec == "MARKET" else b - (kl[e + h] / kl[e] - 1)
    allx = {(sec, h): np.array([exc(sec, e, h) for e in range(1, N - h)]) for sec in lvl for h in H}
    def f(v): return "n/a" if not np.isfinite(v) else f"{v:+.1%}"
    rows = []
    for id_, typ, sec, dr, fp_, dec, note in EV:
        e1 = eidx(fp_); e2 = eidx(dec) if dec else None
        r1 = {h: exc(sec, e1, h) for h in H}; r2 = {h: exc(sec, e2, h) for h in H}
        lag = (e2 - e1) if (e2 is not None and e1 is not None) else None
        pre = exc(sec, e1, lag) if lag else np.nan
        rows.append(dict(id=id_, typ=typ, sec=sec, dr=dr, fp=fp_, dec=dec, lag=lag, pre=pre, r1=r1, r2=r2, note=note))
        out(f"\n{id_} [{typ}; {sec}; expected {'+' if dr > 0 else '-' if dr < 0 else 'mixed'}] first public {fp_}, decision {dec or 'PENDING'}, lag {lag if lag is not None else 'n/a'} sessions. {note}")
        out("   from first public, excess vs KMI TR (gross; net = gross - 1.0%; percentile among all start dates for the same basket and horizon): " + "  ".join(
            f"+{h}: {f(r1[h])} (net {f(r1[h]-0.01)}, pctile {np.nanmean(allx[(sec, h)] < r1[h]):.0%})" if np.isfinite(r1[h]) else f"+{h}: n/a (past data end)" for h in H))
        if e2 is not None and e2 != e1:
            out("   from decision date: " + "  ".join(f"+{h}: {f(r2[h])}" for h in H) + f"   | earned between first public and decision: {f(pre)}")
        if e1 is not None and e1 + 1 < N:
            hz = min(120, N - 1 - e1)
            sg = dr if dr else 1
            path = np.array([exc(sec, e1, k) for k in range(1, hz + 1)]) * sg
            pk = int(np.nanargmax(path)) + 1
            neg = np.where(path < 0)[0]
            out(f"   path to +{hz}: best in expected direction at +{pk} sessions = {f(path[pk-1] * sg)}; first session the excess is against the expected direction: {('+' + str(neg[0] + 1)) if len(neg) else 'never'}; excess at end {f(path[-1] * sg)}")
    out("\n---------------- SUMMARY BY EVENT TYPE (signed so that + means the expected direction was right; gross excess; events with data to +h only; mixed-direction events excluded)")
    out("   long-only note: for expected-negative events the useful action is to avoid or exit, not to short.")
    for t in sorted({r["typ"] for r in rows}):
        rs = [r for r in rows if r["typ"] == t and r["dr"]]
        for h in (20, 60, 120):
            v = np.array([r["r1"][h] * r["dr"] for r in rs if np.isfinite(r["r1"][h])])
            pos = np.array([r["r1"][h] for r in rs if np.isfinite(r["r1"][h]) and r["dr"] > 0])
            if len(v):
                out(f"   {t:16s} +{h:3d}: n {len(v)}, signed excess median {pct(np.median(v))}, mean {pct(v.mean())}, right direction {np.mean(v > 0):.0%}" + (f"; expected-positive only (n {len(pos)}): median {pct(np.median(pos))}, win {np.mean(pos > 0):.0%}, mean {pct(pos.mean())}" if len(pos) else ""))
    allp = [r for r in rows if r["dr"] > 0]
    for h in (20, 60, 120):
        v = np.array([r["r1"][h] for r in allp if np.isfinite(r["r1"][h])])
        out(f"   ALL expected-positive events, from first public +{h}: n {len(v)}, median {pct(np.median(v))}, mean {pct(v.mean())}, win {np.mean(v > 0):.0%}, net median {pct(np.median(v) - 0.01)}")
    allm = [r for r in rows if r["dr"] < 0]
    for h in (20, 60, 120):
        v = np.array([r["r1"][h] for r in allm if np.isfinite(r["r1"][h])])
        out(f"   ALL expected-negative events, from first public +{h}: n {len(v)}, median excess {pct(np.median(v))}, mean {pct(v.mean())}, fell (excess<0) {np.mean(v < 0):.0%}")
    for h in (20, 60, 120):
        pc = [np.nanmean(allx[(r["sec"], h)] < r["r1"][h]) for r in allp if np.isfinite(r["r1"][h])]
        mdn = [np.nanmedian(allx[(r["sec"], h)]) for r in allp if np.isfinite(r["r1"][h])]
        out(f"   expected-positive events +{h}: median percentile against all start dates of the same basket {np.median(pc):.0%}; share above the 75th {np.mean(np.array(pc) > .75):.0%}; typical (median over start dates) excess of these baskets {pct(np.median(mdn))}")
    out("\n---------------- EXPECTED-POSITIVE EVENTS WITH A LAG BETWEEN FIRST PUBLIC AND DECISION")
    for r in rows:
        if r["dr"] > 0 and r["lag"]:
            out(f"   {r['id']}: lag {r['lag']} sessions; excess earned in the lag {pct(r['pre'])}; from first public +60 {pct(r['r1'][60])}; from decision +60 {pct(r['r2'][60])}")
    flat = [dict(id=r["id"], typ=r["typ"], sec=r["sec"], dr=r["dr"], fp=r["fp"], dec=r["dec"], lag=r["lag"], pre=r["pre"], **{f"fp_{h}": r["r1"][h] for h in H}, **{f"dec_{h}": r["r2"][h] for h in H}) for r in rows]
    pd.DataFrame(flat).to_csv(ROOT / "tests/out/results_gap_P_events.csv", index=False)

if "R" in WHICH:
    run_R()
    (ROOT / "tests/out/results_gap_and_policy.txt").write_text(buf.getvalue(), encoding="utf-8")
if "P" in WHICH:
    buf = io.StringIO()
    run_P()
    open(ROOT / "tests/out/results_gap_and_policy.txt", "a", encoding="utf-8").write(buf.getvalue())
