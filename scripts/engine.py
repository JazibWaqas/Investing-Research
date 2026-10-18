"""Situation engine: "what happened next in the past in situations like this".

    python scripts/engine.py SYMBOL DATE                 # a (symbol, date) in the daily table
    python scripts/engine.py --scan DATE                 # every liquid KMI name with an interesting signature at DATE
    python scripts/engine.py --query ret_1d=0.06 ret_5d=0.12 cause=results liq=hi [asof=2026-10-16]   # free query

Point in time: for a query at the close of t, only rows strictly before t are candidates, and an analogue's return at
horizon k is used only if that outcome was already known at the close of t (idx_analogue + k <= idx_t).
Returns are from the next open, gross, on the adjusted scale of data/daily_table.parquet (see data/DAILY_TABLE_NOTES.md).
Method and weaknesses: knowledge/playbooks/situation_engine.md.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data" / "daily_table.parquet"
HORIZONS = [1, 3, 5, 10, 20, 60]
MIN_N = 30
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
                "mae_5", "mae_20", "mfe_5"] + NUM + [f"ret_fwd_{k}" for k in HORIZONS]
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


def scan(e, date):
    date = pd.Timestamp(date)
    t = interesting(e, date)
    if t.empty:
        return f"No interesting liquid KMI names on {date:%Y-%m-%d} (or the date is not in the table)."
    rows = []
    for i, r in t.iterrows():
        sig = e.signature(i)
        pos, info, out = e.run(sig)
        h = {k: out["h"][k] for k in HORIZONS}
        rows.append(dict(sym=r.symbol, fl=",".join(r.why), cause=r.cause, ret1=r.ret_1d, tier=sig["tier"], n5=h[5]["n"] if h[5] else 0,
                         ep=h[5]["ep"] if h[5] else 0, m1=h[1]["med"] if h[1] else np.nan, m5=h[5]["med"] if h[5] else np.nan,
                         m20=h[20]["med"] if h[20] else np.nan, w5=h[5]["win"] if h[5] else np.nan,
                         g10=h[5]["gt10"] if h[5] else np.nan, pl5=h[5]["plc"] if h[5] else np.nan,
                         lk=out["lock5"][0] if out["lock5"] else np.nan, mae=out["mae5"][0] if out["mae5"] else np.nan,
                         wd=f"L1<={info['D']}{'' if info['regime_kept'] else ',noreg'}{',tier+-1' if info['tier_tol'] else ''}{' THIN' if info['thin'] else ''}"))
    R = pd.DataFrame(rows).sort_values("m5", ascending=False, na_position="last")
    L = [f"=== SCAN {date:%Y-%m-%d}: liquid (>Rs5m median traded value) KMI names with an interesting signature, sorted by the median 5-session analogue return ===",
         f"{len(R)} names of {int(((e.d['date'] == date) & e.d['liquid'] & (e.d['kmi_member'] == True)).sum())} liquid KMI names traded. Returns are from the next open, gross; analogues use only data known at that close.",
         "n5/ep = analogues with a known 5-session outcome / distinct name-months. m1,m5,m20 = analogue median return at 1, 5, 20 sessions. pl5 = same-date, same-tier random-entry median at 5. "
         "w5 = share up at 5; g10 = share above +10% at 5; lk5 = share that locked up within 5; mae5 = median max adverse excursion in 5.", "",
         f"{'symbol':<8}{'flags':<24}{'cause':<13}{'ret1d':>7} {'tier':<4}{'n5':>6}{'ep':>5}{'m1':>8}{'m5':>8}{'m20':>8}{'pl5':>8}{'w5':>5}{'g10':>5}{'lk5':>5}{'mae5':>8}  widening"]
    for _, r in R.iterrows():
        L.append(f"{r.sym:<8}{r.fl[:23]:<24}{r.cause:<13}{pct(r.ret1):>7} {r.tier:<4}{r.n5:>6}{r.ep:>5}{pct(r.m1):>8}{pct(r.m5):>8}{pct(r.m20):>8}{pct(r.pl5):>8}"
                 f"{'' if pd.isna(r.w5) else format(r.w5, '.0%'):>5}{'' if pd.isna(r.g10) else format(r.g10, '.0%'):>5}{'' if pd.isna(r.lk) else format(r.lk, '.0%'):>5}{pct(r.mae):>8}  {r.wd}")
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
