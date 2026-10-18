"""Situation engine: "what happened next in the past in situations like this".

    python scripts/engine.py SYMBOL DATE                 # a (symbol, date) in the daily table
    python scripts/engine.py --scan DATE                 # every liquid KMI name with an interesting signature at DATE, tagged with its
                                                         # catalogue type and that type's odds, plus a "missed movers" section
    python scripts/engine.py --query ret_1d=0.06 ret_5d=0.12 cause=results liq=hi [asof=2026-10-16]   # free query

Point in time: for a query at the close of t, only rows strictly before t are candidates, and an analogue's return at
horizon k is used only if that outcome was already known at the close of t (idx_analogue + k <= idx_t).
Returns are from the next open, gross, on the adjusted scale of data/daily_table.parquet (see data/DAILY_TABLE_NOTES.md).
Method and weaknesses: knowledge/playbooks/situation_engine.md.
"""
import argparse
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data" / "daily_table.parquet"
HORIZONS = [1, 3, 5, 10, 20, 60]
MIN_N = 30
LIB = ROOT / "data" / "winners_library.csv"
WIN, MOVER = 60, 0.20  # filing look-back (sessions); missed mover = ret_20d at least this
WAVE20, WAVE60 = 0.10, 0.20  # sector_wave: median liquid peer ret_20d >= WAVE20 or ret_60d >= WAVE60
COST_HI, COST_OTHER = 0.005, 0.010  # round trip, data/costs.md: ~0.5%, plus 0.5% slippage under Rs20m median traded value

# numeric features and bucket edges (searchsorted side="right": value < edges[0] -> bucket 0)
EDGES = {
    "ret_1d": [-0.05, -0.02, -0.005, 0.005, 0.02, 0.05, 0.09],
    "ret_5d": [-0.10, -0.05, -0.02, 0.02, 0.05, 0.10, 0.20],
    "ret_20d": [-0.20, -0.10, -0.03, 0.03, 0.10, 0.20, 0.40],
    "ret_60d": [-0.30, -0.15, -0.05, 0.05, 0.15, 0.30, 0.60],
    "dist_252_high": [-0.50, -0.30, -0.15, -0.05, -0.005],
    "consecutive_up_days": [1, 2, 3, 4, 6],
    "locks_up_5d": [1, 2, 3],
    "vol_ratio_20_120": [0.5, 0.8, 1.25, 2.0, 3.5],
}
NUM = list(EDGES)
TIERS = ["lo", "mid", "hi"]  # <Rs5m, Rs5m-20m, >Rs20m median traded value (60 sessions)
LADDER = ([(d, True, 0) for d in (0, 1, 2, 3, 4)] + [(d, False, 0) for d in (0, 1, 2, 3, 4)]
          + [(d, False, 1) for d in (2, 3, 4, 6, 8, 12)])  # (L1 bucket tolerance, regime kept, tier tolerance)


def bucket(name, x):
    x = np.asarray(x, dtype="float64")
    b = np.searchsorted(EDGES[name], x, side="right").astype("int8")
    return np.where(np.isnan(x), -1, b).astype("int8")


def blabel(name, b):
    e = EDGES[name]
    if b <= 0:
        return f"<{e[0]:g}"
    if b >= len(e):
        return f">={e[-1]:g}"
    return f"{e[b - 1]:g}..{e[b]:g}"


class Engine:
    def __init__(self):
        cols = ["date", "symbol", "session_idx", "sector", "regime", "kmi_member", "liquid", "traded_value_median_60",
                "upper_lock", "f_financial_result", "f_dividend_or_bonus", "f_material_info", "f_insider_trade",
                "f_insider_buy", "f_insider_sell", "f_board_meeting_notice", "f_agm", "f_credit_rating", "f_other",
                "sector_ret_1d", "index_ret_1d", "is_newsless_rise", "first_upper_lock_within_5", "first_red_day",
                "mae_5", "mae_20", "mfe_5", "dist_252_low"] + NUM + [f"ret_fwd_{k}" for k in HORIZONS]
        d = pd.read_parquet(TABLE, columns=cols)
        self.max_idx = int(d["session_idx"].max())
        d["cause"] = self.cause_of(d)
        tv = d["traded_value_median_60"]
        d["tier"] = np.select([tv > 20e6, tv > 5e6, tv.notna()], [2, 1, 0], -1).astype("int8")
        d["cost"] = np.where(d["tier"] == 2, COST_HI, COST_OTHER)
        d["ep"] = d["symbol"] + d["date"].dt.strftime("%Y%m")
        self.regime_code = d["regime"].astype("string").fillna("?").to_numpy()
        for k in HORIZONS:  # date x liquidity-tier cohort median: the placebo (random entry, same date, same tier, same exit)
            d[f"pl_{k}"] = d.groupby(["date", "tier"])[f"ret_fwd_{k}"].transform("median")
        self.B = np.stack([bucket(n, d[n].to_numpy()) for n in NUM], axis=1)
        self.d = d
        self.idx = d["session_idx"].to_numpy()
        self.cause = d["cause"].to_numpy()
        self.tier = d["tier"].to_numpy()

    @staticmethod
    def cause_of(d):
        """Filing class since the prior close (priority order) else sector move, else index move, else none."""
        sr, ir = d["sector_ret_1d"], d["index_ret_1d"]
        conds = [d["f_financial_result"] > 0, d["f_material_info"] > 0, d["f_dividend_or_bonus"] > 0,
                 d["f_insider_buy"] > 0, d["f_insider_sell"] > 0, d["f_insider_trade"] > 0,
                 d["f_board_meeting_notice"] > 0, (d["f_agm"] + d["f_credit_rating"] + d["f_other"]) > 0,
                 sr >= 0.02, sr <= -0.02, ir >= 0.015, ir <= -0.015]
        names = ["results", "material", "dividend", "insider_buy", "insider_sell", "insider", "board_meeting",
                 "other_filing", "sector_up", "sector_down", "index_up", "index_down"]
        return np.select(conds, names, "none")

    def signature(self, i):
        r = self.d.iloc[i]
        return {"symbol": r.symbol, "date": r.date, "idx": int(r.session_idx), "sector": r.sector, "cause": r.cause,
                "tier": TIERS[r.tier] if r.tier >= 0 else None, "regime": r.regime if isinstance(r.regime, str) else None,
                **{n: (None if pd.isna(r[n]) else float(r[n])) for n in NUM}}

    # ---- retrieval -------------------------------------------------------------------------------------------
    def analogues(self, sig):
        """Return (row positions, widening info). Cause exact; numeric buckets by L1 tolerance; widen until >= MIN_N."""
        t_idx = sig["idx"]
        base = self.idx < t_idx
        if sig.get("cause"):
            base &= self.cause == sig["cause"]
        used = [j for j, n in enumerate(NUM) if sig.get(n) is not None]
        qb = {j: int(bucket(NUM[j], [sig[NUM[j]]])[0]) for j in used}
        for j in used:
            base &= self.B[:, j] >= 0
        base &= self.tier >= 0
        pos = np.flatnonzero(base)
        dist = np.zeros(len(pos), dtype="int16")
        for j in used:
            dist += np.abs(self.B[pos, j].astype("int16") - qb[j])
        resolved5 = (self.idx[pos] + 5 <= t_idx) & self.d["ret_fwd_5"].notna().to_numpy()[pos]
        qt = TIERS.index(sig["tier"]) if sig.get("tier") else None
        best = None
        for D, keep_reg, ttol in LADDER:
            m = dist <= D
            if keep_reg and sig.get("regime"):
                m &= self.regime_code[pos] == sig["regime"]
            if qt is not None:
                m &= np.abs(self.tier[pos].astype(int) - qt) <= ttol
            n5 = int((m & resolved5).sum())
            best = (pos[m], dict(D=D, regime_kept=bool(keep_reg and sig.get("regime")), tier_tol=ttol, n5=n5,
                                 steps=LADDER.index((D, keep_reg, ttol)), used=[NUM[j] for j in used]))
            if n5 >= MIN_N:
                break
        best[1]["thin"] = best[1]["n5"] < MIN_N
        return best

    # ---- outcome report --------------------------------------------------------------------------------------
    def outcomes(self, sig, rows):
        d, t_idx = self.d, sig["idx"]
        sub = d.iloc[rows]
        out = {"h": {}}
        for k in HORIZONS:
            s = sub[(sub["session_idx"] + k <= t_idx) & sub[f"ret_fwd_{k}"].notna()]
            r = s[f"ret_fwd_{k}"].astype(float)
            if len(r) == 0:
                out["h"][k] = None
                continue
            q = r.quantile([.1, .25, .5, .75, .9]).to_numpy()
            epm = r.groupby(s["ep"]).median()
            out["h"][k] = dict(n=len(r), ep=s["ep"].nunique(), p10=q[0], p25=q[1], med=q[2], p75=q[3], p90=q[4],
                               mean=r.mean(), win=(r > 0).mean(), gt10=(r > .10).mean(), gt50=(r > .50).mean(),
                               worst=r.min(), plc=s[f"pl_{k}"].median(), net=(r - s["cost"]).median(),
                               epmed=epm.median())
        s5 = sub[(sub["session_idx"] + 5 <= t_idx) & sub["ret_fwd_5"].notna()]
        out["lock5"] = (s5["first_upper_lock_within_5"].notna().mean(), len(s5)) if len(s5) else None
        s20 = sub[(sub["session_idx"] + 20 <= t_idx) & sub["mae_20"].notna()]
        s60 = sub[(sub["session_idx"] + 60 <= t_idx) & sub["ret_fwd_60"].notna()]
        out["red"] = (s60["first_red_day"].fillna(61).median(), (s60["first_red_day"] == 1).mean(), len(s60)) if len(s60) else None
        out["mae5"] = (s5["mae_5"].median(), len(s5)) if len(s5) else None
        out["mfe5"] = s5["mfe_5"].median() if len(s5) else None
        out["mae20"] = (s20["mae_20"].median(), len(s20)) if len(s20) else None
        return out

    def run(self, sig):
        rows, info = self.analogues(sig)
        return rows, info, self.outcomes(sig, rows)


def pct(x, d=1):
    return "   n/a" if x is None or pd.isna(x) else f"{x * 100:+.{d}f}%"


def sentence(k, h):
    if h is None:
        return f"{k:>2} sessions: no analogue had a resolved {k}-session outcome by this date."
    thin = " (thin: fewer than 10 name-months, treat as anecdote)" if h["ep"] < 10 else ""
    s = "" if k == 1 else "s"
    return (f"Over {k} session{s} from the next open, {h['n']} analogues ({h['ep']} name-months) returned a median of "
            f"{pct(h['med'])} (middle half {pct(h['p25'], 0)} to {pct(h['p75'], 0)}, worst {pct(h['worst'], 0)}); "
            f"{h['win']:.0%} finished up, {h['gt10']:.0%} gained over 10%, {h['gt50']:.0%} over 50%. "
            f"Same-date same-liquidity random entries had a median of {pct(h['plc'])}; "
            f"after round-trip costs the analogue median is {pct(h['net'])}.{thin}")


def widen_text(info):
    if info["steps"] == 0:
        return "none (same signature on all used features, regime and liquidity tier exact)"
    parts = [f"numeric buckets within L1 distance {info['D']}"]
    parts.append("regime kept" if info["regime_kept"] else "regime dropped")
    parts.append("tier exact" if info["tier_tol"] == 0 else "tier +/-1")
    return "widened: " + ", ".join(parts) + f" (ladder step {info['steps'] + 1} of {len(LADDER)})"


def sig_text(sig):
    parts = [f"cause={sig.get('cause') or 'any'}"]
    for n in NUM:
        if sig.get(n) is not None:
            v = sig[n]
            parts.append(f"{n}={v:+.1%}" if n.startswith(("ret_", "dist")) else f"{n}={v:.2f}".rstrip("0").rstrip("."))
    parts.append(f"liq={sig.get('tier') or 'any'}")
    parts.append(f"regime={sig.get('regime') or 'any'}")
    return " | ".join(parts)


def report(sig, info, out, title):
    L = [f"=== {title} ===", "Signature: " + sig_text(sig),
         "Buckets: " + ", ".join(f"{n} [{blabel(n, int(bucket(n, [sig[n]])[0]))}]" for n in NUM if sig.get(n) is not None),
         f"Pool: rows before {sig['date']:%Y-%m-%d}" if sig.get("date") is not None else "Pool: all rows",
         f"Analogues with a 5-session outcome known: {info['n5']}" + ("  ** THIN: fewer than 30 even at the widest setting **" if info["thin"] else ""),
         "Widening: " + widen_text(info), "",
         f"{'h':>3} {'n':>6} {'ep':>5} {'p10':>8} {'p25':>8} {'med':>8} {'p75':>8} {'p90':>8} {'mean':>8} {'win':>5} {'>10%':>5} {'>50%':>5} {'worst':>8} {'plcbo':>8} {'net':>8} {'epmed':>8}"]
    for k in HORIZONS:
        h = out["h"][k]
        if h is None:
            L.append(f"{k:>3}   (no resolved analogues)")
            continue
        L.append(f"{k:>3} {h['n']:>6} {h['ep']:>5} " + " ".join(f"{pct(h[c], 1):>8}" for c in ["p10", "p25", "med", "p75", "p90", "mean"])
                 + f" {h['win']:>5.0%} {h['gt10']:>5.0%} {h['gt50']:>5.0%} {pct(h['worst'], 0):>8} {pct(h['plc']):>8} {pct(h['net']):>8} {pct(h['epmed']):>8}")
    L.append("  (plcbo = median return of all rows on the same dates and liquidity tiers; net = median after round-trip cost; epmed = median of name-month medians)")
    if out["lock5"]:
        L.append(f"Locked up (close at upper limit) within 5 sessions after entry: {out['lock5'][0]:.0%} (n={out['lock5'][1]})")
    if out["red"]:
        L.append(f"Median first red day (session offset from t, 61 = none in 60): {out['red'][0]:.0f}; red on the very next session: {out['red'][1]:.0%} (n={out['red'][2]})")
    if out["mae5"]:
        L.append(f"Max adverse excursion from the next open, median: 5 sessions {pct(out['mae5'][0])} (n={out['mae5'][1]}), "
                 f"20 sessions {pct(out['mae20'][0]) if out['mae20'] else 'n/a'}; median max favourable 5 sessions {pct(out['mfe5'])}")
    L.append("")
    L += [sentence(k, out["h"][k]) for k in HORIZONS]
    return "\n".join(L)


def interesting(e, date):
    """Rows on `date` that are liquid KMI names with a move above 5%, a lock, a news-less rise, results or a sector lead."""
    d = e.d
    t = d[(d["date"] == date) & d["liquid"] & (d["kmi_member"] == True)].copy()  # noqa: E712
    t["why"] = [[] for _ in range(len(t))]
    cnt = t.groupby("sector")["symbol"].transform("size")
    top = t.groupby("sector")["ret_1d"].transform("max")
    rules = {"move>5%": t["ret_1d"] > 0.05, "lock": t["upper_lock"], "newsless": t["is_newsless_rise"],
             "results": t["f_financial_result"] > 0,
             "sector_leader": (t["sector"] != "other") & (cnt >= 3) & (t["ret_1d"] == top) & (t["ret_1d"] >= 0.02)}
    for name, m in rules.items():
        for i in t.index[m.fillna(False)]:
            t.at[i, "why"].append(name)
    return t[t["why"].str.len() > 0]



# ---- catalogue tags (knowledge/CATALOGUE.md) -------------------------------------------------------------------------
# tag -> (label with catalogue section, winners_library types it is scored against). First tag that applies wins, in the
# library's own order (tests/winners_population.md section 2), so the odds below are for the same definition.
TAGS = {"deal": ("deal (cat 7)", ["takeover_deal"]),
        "results": ("results_jump (cat 4/5)", ["results_jump"]),
        "sponsor": ("sponsor (cat 8)", ["sponsor_buyback"]),
        "sector_wave": ("sector_wave (cat 2)", ["policy_sector_wave"]),
        "shock_rebound": ("shock_rebound (cat 3)", ["shock_rebound"]),
        "first_cut": ("first_cut (cat 1)", ["rate_cut_rotation"]),
        "none": ("none (cat 9 or other)", ["operator_no_visible_cause", "other"])}
DEAL = re.compile(r"acqui|merger|amalgam|take[- ]?over|\boffer", re.I)
NODEAL = re.compile(r"right|offer for sale|public offer|initial public|ipo", re.I)
BUYB = re.compile(r"buy[- ]?back|repurchase", re.I)


def period_of(title):
    m = re.search(r"(?:ended|ending)\s+(.*)$", str(title), re.I)
    if not m:
        return None
    s = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", re.sub(r"[.]+$", "", m.group(1)).strip())
    try:
        from dateutil import parser as dp
        return pd.Timestamp(dp.parse(s, fuzzy=True, default=pd.Timestamp("2000-01-01").to_pydatetime()))
    except Exception:
        return None


class Tagger:
    """Point-in-time catalogue flags for (symbol, date), mirroring the winners_library definitions with a look-back instead of
    a hindsight run start: results = a financial_result filing in the last WIN sessions whose quarter EPS is >= 1.5x the same
    quarter a year earlier (or loss to profit); deal / sponsor = a matching filing title or a director buy in the last WIN
    sessions; sector_wave = median liquid peer (>= 3, self excluded) with ret_20d >= WAVE20 or ret_60d >= WAVE60 (fires on 27% of liquid sector-days; on 43%, 36% and 67% of the library's wave runs 20, 40 and 60 sessions after their start); shock_rebound = KMI All Share
    >= 8% below its 20-session high on some session in the last 40; first_cut = within 80 sessions of the first policy-rate cut
    after a hike. ponytail: look-backs are proxies for 'the run started at most ~20-60 sessions ago'; library flags are set at the
    run start with hindsight (sector_wave uses the peers' move to the peak), so the two definitions are close, not identical."""

    def __init__(self, d):
        self.CAL = np.sort(d["date"].unique())
        an = pd.read_parquet(ROOT / "data" / "announcements.parquet", columns=["datetime", "symbol", "title", "klass", "direction"])
        an = an[an["klass"].isin(["financial_result", "material_info", "insider_trade"]) | an["title"].str.contains(BUYB)].copy()
        dtm = an["datetime"].dt.tz_convert("Asia/Karachi").dt.tz_localize(None)
        an["dt"] = dtm
        an["sess"] = self.CAL.searchsorted(((dtm - pd.Timedelta(hours=15, minutes=30)).dt.normalize() + pd.Timedelta(days=1)).values)
        self.AN = {s: g for s, g in an.groupby("symbol")}
        q = pd.read_csv(ROOT / "data" / "fundamentals" / "quarterly_eps.csv", parse_dates=["fiscal_quarter_end"])
        q["e"] = q["eps_basic"].fillna(q["eps_diluted"])
        self.EPS = {s: g.set_index("fiscal_quarter_end")["e"].dropna() for s, g in q.groupby("symbol")}
        k = pd.read_csv(ROOT / "data" / "macro" / "kmiallshr.csv", parse_dates=["date"]).drop_duplicates("date").set_index("date")["close"].sort_index()
        self.kdd = k / k.rolling(20, min_periods=20).max() - 1
        pr = pd.read_csv(ROOT / "data" / "macro" / "policy_rate_decisions.csv", parse_dates=["date"])
        cuts, hiked = [], True  # first cut after a hike, as scripts/tests/winners_population.py
        for r in pr.itertuples():
            if r.change_bp > 0:
                hiked = True
            elif r.change_bp < 0 and hiked:
                cuts.append(int(self.CAL.searchsorted(np.datetime64(r.date))))
                hiked = False
        self.cuts = cuts

    def eps_jump(self, sym, w):
        e = self.EPS.get(sym)
        if e is None or not len(e):
            return None
        for r in w[w["klass"] == "financial_result"].sort_values("sess", ascending=False).itertuples():  # newest first
            qd = period_of(r.title)
            if qd is None:  # title cut off after "Quarter Ended" (MACFL 29 Apr 2026): the latest quarter end at least 15 days before the filing
                prev = e.index[e.index <= r.dt - pd.Timedelta(days=15)]
                if not len(prev):
                    continue
                qd = prev[-1]
            k = np.argmin(np.abs((e.index - qd).days))
            if abs((e.index[k] - qd).days) > 10:
                continue
            prior = e.index[k] - pd.DateOffset(years=1)
            j = np.argmin(np.abs((e.index - prior).days))
            if abs((e.index[j] - prior).days) > 10:
                continue
            en, ep = float(e.iloc[k]), float(e.iloc[j])
            if (ep > 0 and en >= 1.5 * ep) or (ep <= 0 < en):
                return f"EPS {en:g} vs {ep:g}"
        return None

    def tag(self, sym, date, peers):
        """-> (tag, [(flag, detail), ...] every flag that applies, in priority order)"""
        i = int(self.CAL.searchsorted(np.datetime64(date)))
        g = self.AN.get(sym)
        w = g[(g["sess"] > i - WIN) & (g["sess"] <= i)] if g is not None else pd.DataFrame(columns=["klass", "title", "direction", "sess", "dt"])
        fl = []
        dl = w[(w["klass"] == "material_info") & w["title"].str.contains(DEAL) & ~w["title"].str.contains(NODEAL)]
        if len(dl):
            fl.append(("deal", dl["title"].iloc[-1][:40]))
        ej = self.eps_jump(sym, w)
        if ej:
            fl.append(("results", ej))
        if ((w["klass"] == "insider_trade") & (w["direction"] == "buy")).any() or w["title"].str.contains(BUYB).any():
            fl.append(("sponsor", "director buy or buy-back title"))
        if peers is not None and (peers[0] >= WAVE20 or peers[1] >= WAVE60):
            fl.append(("sector_wave", f"peer median {peers[0]:+.0%} in 20d, {peers[1]:+.0%} in 60d"))
        kd = self.kdd[self.kdd.index <= pd.Timestamp(date)].iloc[-40:]
        if len(kd) and kd.min() <= -0.08:
            fl.append(("shock_rebound", f"KMI {kd.min():+.0%} off 20d high"))
        if any(0 <= i - c <= 80 for c in self.cuts):
            fl.append(("first_cut", "within 80 sessions of first cut"))
        return (fl[0][0] if fl else "none"), fl


class Odds:
    """Measured odds per tag from data/winners_library.csv (tests/winners_population.md): liquid, non-suspect runs, all winners in
    hindsight, so every figure is conditional on the run having happened (the denominator is in the catalogue: 25.6% of first
    252-highs ran another 50%). For a historical scan only runs whose peak was at least 45 days before the scan date are used."""

    def __init__(self, date, last):
        lib = pd.read_csv(LIB, parse_dates=["peak_date"])
        lib = lib[lib["data_suspect"] == False]  # noqa: E712
        self.lib = lib if pd.Timestamp(date) >= last else lib[lib["peak_date"] <= pd.Timestamp(date) - pd.Timedelta(days=45)]

    def line(self, tag, x):
        lab, types = TAGS[tag]
        g = self.lib[self.lib["type"].isin(types)]
        if len(g) == 0:
            return f"{lab}: no library runs finished by this date"
        m = g["multiple"]
        s = f"{lab}: {len(g)} library runs, median peak {m.median():.2f}x"
        if x is not None and not np.isnan(x):
            far = m[m > x]
            rem = far / x
            if len(far):
                s += (f"; at {x:.2f}x from the 252d low {len(far)} of {len(g)} ({len(far) / len(g):.0%}) went further, "
                      f"median a further {rem.median():.2f}x, {int((rem >= 1.5).sum())} ({(rem >= 1.5).sum() / len(g):.0%}) another +50% or more")
            else:
                s += f"; at {x:.2f}x from the 252d low none went further"
        a = g["ahead_f252_log"].dropna()
        if len(a):
            s += f"; share of the gain still ahead at the first 252-high, median {a.median():.2f} (n={len(a)})"
        s20, s30 = g["stop_f252_exit_mult"].dropna(), g["stop30_f252_exit_mult"].dropna()
        if len(s20):
            s += (f"; late-entry rule (first 252-high, trail 20% / 30%): finished above 1.0x in {(s20 > 1).mean():.0%} / {(s30 > 1).mean():.0%}, "
                  f"median exit {s20.median():.2f}x / {s30.median():.2f}x (n={len(s20)})")
        else:
            s += "; late-entry rule: no library run with a first 252-high"
        return s + (" [thin: n<15]" if len(g) < 15 else "")

def scan(e, date):
    date = pd.Timestamp(date)
    t = interesting(e, date)
    if t.empty:
        return f"No interesting liquid KMI names on {date:%Y-%m-%d} (or the date is not in the table)."
    tg, odds = Tagger(e.d), Odds(date, e.d["date"].max())
    day = e.d[(e.d["date"] == date) & e.d["liquid"] & (e.d["sector"] != "other")]
    secs = {s: g.set_index("symbol")[["ret_20d", "ret_60d"]].dropna() for s, g in day.groupby("sector")}

    def peer_moves(sym, sector):  # median 20d and 60d move of the liquid sector peers, self excluded, >= 3 peers
        sr = secs.get(sector)
        p = sr.drop(sym, errors="ignore") if sr is not None else None
        return (float(p["ret_20d"].median()), float(p["ret_60d"].median())) if p is not None and len(p) >= 3 else None

    def tagged(r):
        tag, fl = tg.tag(r.symbol, date, peer_moves(r.symbol, r.sector))
        x = 1 + r.dist_252_low if pd.notna(r.dist_252_low) else np.nan
        return tag, fl, x

    rows = []
    for i, r in t.iterrows():
        sig = e.signature(i)
        pos, info, out = e.run(sig)
        h = {k: out["h"][k] for k in HORIZONS}
        tag, fl, x = tagged(r)
        rows.append(dict(sym=r.symbol, fl=",".join(r.why), tag=tag, allfl=", ".join(f"{a} [{b}]" for a, b in fl) or "no flag", x=x, ret20=r.ret_20d,
                         cause=r.cause, ret1=r.ret_1d, tier=sig["tier"], n5=h[5]["n"] if h[5] else 0,
                         ep=h[5]["ep"] if h[5] else 0, m1=h[1]["med"] if h[1] else np.nan, m5=h[5]["med"] if h[5] else np.nan,
                         m20=h[20]["med"] if h[20] else np.nan, w5=h[5]["win"] if h[5] else np.nan,
                         g10=h[5]["gt10"] if h[5] else np.nan, pl5=h[5]["plc"] if h[5] else np.nan,
                         lk=out["lock5"][0] if out["lock5"] else np.nan, mae=out["mae5"][0] if out["mae5"] else np.nan,
                         wd=f"L1<={info['D']}{'' if info['regime_kept'] else ',noreg'}{',tier+-1' if info['tier_tol'] else ''}{' THIN' if info['thin'] else ''}"))
    R = pd.DataFrame(rows).sort_values("m5", ascending=False, na_position="last")
    nliq = int(((e.d['date'] == date) & e.d['liquid'] & (e.d['kmi_member'] == True)).sum())  # noqa: E712
    L = [f"=== SCAN {date:%Y-%m-%d}: liquid (>Rs5m median traded value) KMI names with an interesting signature, sorted by the median 5-session analogue return ===",
         f"{len(R)} names of {nliq} liquid KMI names traded. Returns are from the next open, gross; analogues use only data known at that close.",
         "n5/ep = analogues with a known 5-session outcome / distinct name-months. m1,m5,m20 = analogue median return at 1, 5, 20 sessions. pl5 = same-date, same-tier random-entry median at 5. "
         "w5 = share up at 5; g10 = share above +10% at 5; lk5 = share that locked up within 5; mae5 = median max adverse excursion in 5.",
         f"type = catalogue type the name most resembles (knowledge/CATALOGUE.md), first flag that applies in the winners-library order deal, results, sponsor, sector_wave, shock_rebound, first_cut, else none. "
         f"Flags look back {WIN} sessions (filings) or, for sector_wave, the liquid peers' median move (20 days >= {WAVE20:.0%} or 60 days >= {WAVE60:.0%}, at least 3 peers); the line under each name lists every flag that applies and that type's measured odds "
         f"from data/winners_library.csv ({len(odds.lib)} liquid runs{'' if date >= e.d['date'].max() else ', only those whose peak was 45+ days before this date'}). x = close over the 252-session low.",
         "The odds are conditional on the run having happened (the library holds winners only, each at least 1.5x, so any x below 1.5 reads 100% went further). Unconditional: 25.6% of first 252-highs in liquid names gained another 50% in 126 sessions; EPS jumps alone, +0.9% median at 20 sessions.", "",
         f"{'symbol':<8}{'flags':<24}{'type':<14}{'cause':<13}{'ret1d':>7} {'tier':<4}{'n5':>6}{'ep':>5}{'m1':>8}{'m5':>8}{'m20':>8}{'pl5':>8}{'w5':>5}{'g10':>5}{'lk5':>5}{'mae5':>8}  widening"]
    for _, r in R.iterrows():
        L.append(f"{r.sym:<8}{r.fl[:23]:<24}{r.tag:<14}{r.cause:<13}{pct(r.ret1):>7} {r.tier:<4}{r.n5:>6}{r.ep:>5}{pct(r.m1):>8}{pct(r.m5):>8}{pct(r.m20):>8}{pct(r.pl5):>8}"
                 f"{'' if pd.isna(r.w5) else format(r.w5, '.0%'):>5}{'' if pd.isna(r.g10) else format(r.g10, '.0%'):>5}{'' if pd.isna(r.lk) else format(r.lk, '.0%'):>5}{pct(r.mae):>8}  {r.wd}")
        L.append(f"        flags: {r.allfl}; ret_20d {pct(r.ret20, 0)}")
        L.append(f"        odds: {odds.line(r.tag, r.x)}")

    # missed movers: every liquid name (KMI or not) up MOVER or more over 20 sessions that is not above
    d = e.d
    m = d[(d["date"] == date) & d["liquid"] & (d["ret_20d"] >= MOVER) & ~d["symbol"].isin(R["sym"])].sort_values("ret_20d", ascending=False)
    L += ["", f"=== MISSED MOVERS {date:%Y-%m-%d}: liquid names up {MOVER:.0%}+ over the last 20 sessions that are not in the scan above (KMI = member on this date) ===",
          f"{len(m)} names. Same tags and odds as above; ret_20d and ret_60d are adjusted closes; x = close over the 252-session low.", ""]
    for _, r in m.iterrows():
        tag, fl = tg.tag(r.symbol, date, peer_moves(r.symbol, r.sector))
        x = 1 + r.dist_252_low if pd.notna(r.dist_252_low) else np.nan
        L.append(f"{r.symbol:<8}{'KMI' if r.kmi_member == True else 'non-KMI':<8}{r.sector[:22]:<23}ret_20d {pct(r.ret_20d, 0):>6} ret_60d {pct(r.ret_60d, 0):>6} x {x:>5.2f}  type {tag}"  # noqa: E712
                 f" | flags: {', '.join(f'{a} [{b}]' for a, b in fl) or 'no flag'}")
        L.append(f"        odds: {odds.line(tag, x)}")
    if m.empty:
        L.append("(none)")
    return "\n".join(L)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("args", nargs="*", help="SYMBOL DATE | key=value pairs with --query")
    ap.add_argument("--scan", metavar="DATE")
    ap.add_argument("--query", action="store_true")
    a = ap.parse_args()
    e = Engine()
    if a.scan:
        print(scan(e, a.scan))
    elif a.query:
        kv = dict(x.split("=", 1) for x in a.args)
        asof = pd.Timestamp(kv.pop("asof")) if "asof" in kv else None
        t_idx = int(e.d.loc[e.d["date"] <= asof, "session_idx"].max()) + 1 if asof is not None else e.max_idx + 1
        sig = {"idx": t_idx, "date": None, "cause": kv.pop("cause", None), "tier": kv.pop("liq", None), "regime": kv.pop("regime", None)}
        bad = [k for k in kv if k not in NUM]
        if bad or (sig["tier"] and sig["tier"] not in TIERS):
            sys.exit(f"unknown keys {bad}; numeric keys: {NUM}; liq in {TIERS}")
        sig.update({n: float(kv[n]) for n in kv})
        rows, info, out = e.run(sig)
        print(report(sig, info, out, "FREE QUERY"))
    else:
        if len(a.args) != 2:
            sys.exit("usage: engine.py SYMBOL DATE | --scan DATE | --query key=value ...")
        sym, date = a.args[0].upper(), pd.Timestamp(a.args[1])
        m = e.d.index[(e.d["symbol"] == sym) & (e.d["date"] == date)]
        if len(m) == 0:
            sys.exit(f"{sym} has no row on {date:%Y-%m-%d} (did not trade, or not in the table)")
        sig = e.signature(m[0])
        rows, info, out = e.run(sig)
        print(report(sig, info, out, f"{sym} {date:%Y-%m-%d} ({sig['sector']})"))


if __name__ == "__main__":
    main()
