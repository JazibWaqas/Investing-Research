"""Scores the blind-replay exam (knowledge/playbooks/replay_exam.md s6).
    .venv/Scripts/python.exe -I scripts/score_replay.py [--fake] [--draws 500]
Reads data/asof/<T>/REPLY.json (+ BUNDLE.md), writes tests/out/replay_scores.csv, replay_entries.csv, replay_summary.txt and
data/replay/surprises.csv. --fake first writes a synthetic REPLY.json for dates that have none (marked "fake": true) so the
scorer can be tested end to end; a real REPLY.json is never overwritten.
Simplifications (ponytail): S3 uses the liquid KMI names of screens.csv at T as a fixed universe (membership over the next 120
sessions is not re-derived); KMI "TR" is the kmiallshr price index less 0.25% each way, as S7 of the oracle script; the entry
Brier uses the 60-session net return whatever horizon_sessions the entry stated; dividends are as complete as the adjusted panel.
"""
import argparse, json, re, sys, warnings, random, io
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

HS = (20, 60, 120)
TYPES = "policy_or_price_decision_pending earnings_inflection_ignored shock_and_rebound deal_after_offer buyback_or_sponsor_move volume_with_upper_locks other".split()
SEED = 20261018

raw, vol, tv = P.load_panel()
dates, N, cols = raw.index, len(raw), list(raw.columns)
cidx = {s: i for i, s in enumerate(cols)}
adj = pd.read_parquet(ROOT / "data" / "panel_close_adj.parquet").reindex(index=dates, columns=cols)
TRADED, PX, RAWF = adj.notna().values, adj.ffill().values, raw.ffill().values
MTV = tv.rolling(60, min_periods=40).median().shift(1).values
LIQ = MTV > 5e6
HI252 = adj.ffill().rolling(252, min_periods=200).max().shift(1).values
KM = pd.read_csv(ROOT / "data/macro/kmiallshr.csv", parse_dates=["date"]).set_index("date").close.reindex(dates, method="ffill").values
TB = pd.read_csv(ROOT / "data/macro/tbill_auctions.csv", parse_dates=["date"]).dropna(subset=["y6m"])


def side(i, c):
    m = MTV[i, c]
    return 0.0025 + (0.0025 if not (m >= 20e6) else 0.0)


def t_index(d):
    return int(dates.searchsorted(pd.Timestamp(d), side="right")) - 1


def rf(i0):
    return TB[TB.date <= dates[i0]].y6m.iloc[-1] / 100


# ---- one name: fill, stop, exit
def plan(i0, c, kind=None, d=None, stop_abs=None, limit=None):
    """-> (fill index, stop-exit index or None), or None if unfilled. kind None|fixed|trailing; d = (entry-stop)/entry; limit = adjusted entry price."""
    end = min(i0 + 120, N - 1)
    j = None
    if limit is not None and limit < PX[i0, c]:                      # resting buy below the T close: first close at or below it within 10 sessions
        j = next((k for k in range(i0 + 1, min(i0 + 10, end) + 1) if TRADED[k, c] and PX[k, c] <= limit), None)
    elif limit is not None:                                          # at or above: T+1 close, unless it gapped over 3% above
        j = i0 + 1 if i0 + 1 <= end and TRADED[i0 + 1, c] and PX[i0 + 1, c] <= 1.03 * limit else None
    else:
        j = next((k for k in range(i0 + 1, min(i0 + 5, end) + 1) if TRADED[k, c]), None)
    if j is None or not np.isfinite(PX[j, c]):
        return None
    cl = PX[j:end + 1, c]
    if kind == "fixed":
        hit = cl <= (stop_abs if stop_abs else cl[0] * (1 - d))
    elif kind == "trailing":
        hit = cl <= np.maximum.accumulate(cl) * (1 - d)
    else:
        return j, None
    e = j + int(np.argmax(hit)) + 1 if hit.any() else None            # close at or below the stop: exit at the next session's close
    return j, (e if e is not None and e <= end else None)


def ret(i0, c, pl, h):
    """net return at horizon h; None unfilled; nan data not there yet."""
    i1 = i0 + h
    if i1 > N - 1:
        return np.nan
    if pl is None or pl[0] > i1:
        return None
    j, e = pl
    x = e if e is not None and e <= i1 else i1
    return (1 - side(j, c)) * (1 - side(x, c)) * PX[x, c] / PX[j, c] - 1


def book(i0, items, h, r_f):
    """items: [(weight fraction, ret or None)]. Unfilled and unallocated money earns the T-bill rate."""
    if any(r is not None and np.isnan(r) for _, r in items):
        return np.nan
    inv = sum(w for w, r in items if r is not None)
    return sum(w * r for w, r in items if r is not None) + (1 - inv) * r_f * h / 252


# ---- S3 from T
def s3(i0, univ):
    end = min(i0 + 120, N - 1)
    cash, pos, ps, pb, eq = 1e5, {}, set(), [], {}
    for i in range(i0, end + 1):
        for c in list(ps):
            if TRADED[i, c]:
                cash += pos[c][0] * PX[i, c] * (1 - side(i, c)); del pos[c]; ps.discard(c)
        val = lambda: cash + sum(s * PX[i, c] * (1 - side(i, c)) for c, (s, _) in pos.items())
        for c in pb:
            amt = min(val() / 3, cash)
            if amt >= 1000 and TRADED[i, c] and c not in pos:
                pos[c] = [amt * (1 - side(i, c)) / PX[i, c], PX[i, c]]; cash -= amt
        pb = []
        eq[i] = val()
        for c, p in pos.items():
            p[1] = max(p[1], PX[i, c])
            if PX[i, c] <= 0.8 * p[1]:
                ps.add(c)
        free = 3 - len([c for c in pos if c not in ps])
        if free > 0:
            cand = np.where(univ & LIQ[i] & TRADED[i] & (PX[i] > HI252[i]))[0]
            cand = sorted((int(c) for c in cand if int(c) not in pos), key=lambda c: -PX[i, c] / HI252[i, c])
            pb = cand[:free]
    return {h: (eq[i0 + h] / 1e5 - 1 if i0 + h in eq else np.nan) for h in HS}


# ---- schema and citations
def sections(txt):
    return {m[1]: m[2] for m in re.finditer(r"=== FILE: (\S+) ===\n(.*?)(?=\n=== (?:FILE: \S+|END) ===)", txt, re.S)}


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def cite_ok(c, sec):
    try:
        f, q = c["file"], norm(c["quote"])
    except (KeyError, TypeError):
        return False
    t = sec.get(f)
    if t is None or not q:
        return False
    if not f.endswith(".csv"):
        return q in norm(t)
    df = pd.read_csv(io.StringIO(t), dtype=str)
    rows = df[df.iloc[:, 0 if f != "announcements_30d.csv" else 1].astype(str) == str(c.get("row"))] if c.get("row") is not None else df
    if c.get("field") in df.columns and len(rows):
        for v in rows[c["field"]].dropna():
            if q == norm(v) or q in norm(v):
                return True
            try:
                if f"{float(q):.4g}" == f"{float(v):.4g}":
                    return True
            except ValueError:
                pass
    return len(rows) > 0 and any(q in norm(" ".join(r.dropna())) for _, r in rows.iterrows())


def validate(r, syms):
    e = []
    g = lambda *k: r.get(k[0]) if len(k) == 1 else None
    reg = r.get("regime", {})
    if reg.get("rates_phase") not in ("hiking", "holding", "cutting"): e.append("rates_phase")
    if reg.get("stance") not in ("risk_on", "neutral", "risk_off"): e.append("stance")
    if not isinstance(reg.get("p_kmi_up_60"), (int, float)) or not 0 <= reg["p_kmi_up_60"] <= 1: e.append("p_kmi_up_60")
    core, watch, ents = r.get("core", []), r.get("watch", []), r.get("entries", [])
    if len(core) > 3 or len(watch) > 10 or len(ents) > 3: e.append("counts")
    for x in core + ents:
        if x.get("symbol") not in syms: e.append(f"symbol {x.get('symbol')}")
    for x in watch:
        if x.get("type") not in TYPES: e.append("watch type")
    risk = 0
    for x in ents:
        if x.get("type") not in TYPES: e.append("entry type")
        if x.get("horizon_sessions") not in HS: e.append("horizon")
        if x.get("stop_type") not in ("fixed", "trailing"): e.append("stop_type")
        if not 0 <= x.get("p_gain", -1) <= 1: e.append("p_gain")
        try:
            rk = x["size_pct"] * (x["entry_price"] - x["stop_price"]) / x["entry_price"]
            if not 0 < x["stop_price"] < x["entry_price"]: e.append("stop vs entry")
            if rk > 5: e.append(f"risk {x['symbol']} {rk:.1f}>5")
            risk += rk
        except (KeyError, TypeError, ZeroDivisionError):
            e.append("entry fields")
    if risk > 10: e.append(f"risk sum {risk:.1f}>10")
    try:
        if abs(r["exposure_pct"] - sum(x["weight_pct"] for x in core) - sum(x["size_pct"] for x in ents)) > 1 or not 0 <= r["exposure_pct"] <= 100: e.append("exposure")
    except (KeyError, TypeError):
        e.append("exposure fields")
    return e


def all_cites(r):
    out = list(r.get("regime", {}).get("evidence", []))
    for k in ("core", "watch", "entries"):
        for x in r.get(k, []):
            out += x.get("evidence", [])
    return out


# ---- regimes and roles from the exam table
EXAM = (ROOT / "knowledge/playbooks/replay_exam.md").read_text(encoding="utf-8")
TAB = {m[1]: (m[2], m[3]) for m in re.finditer(r"^\| \d+ \| (\d{4}-\d\d-\d\d) \| (HF|B) \| ([\w-]+) \|", EXAM, re.M)}


def regime_role(d):
    if d in TAB:
        return TAB[d]
    t = pd.Timestamp(d)
    b = (pd.Timestamp("2020-03-17") <= t <= pd.Timestamp("2020-12-31")) or (pd.Timestamp("2023-07-01") <= t <= pd.Timestamp("2025-06-30"))
    return ("B" if b else "HF"), "n/a"


# ---- fake replies
def fake(d):
    A = ROOT / "data/asof" / d
    f = A / "REPLY.json"
    if f.exists() and not json.loads(f.read_text(encoding="utf-8")).get("fake"):
        return
    rnd = random.Random(f"{SEED}{d}")
    sc = pd.read_csv(A / "screens.csv")
    pick = sc.sample(8, random_state=rnd.randint(0, 10**6)).itertuples()
    cite = lambda r: {"file": "screens.csv", "row": r.symbol, "field": "close", "quote": f"{r.close:g}"}
    mk = (A / "market.md").read_text(encoding="utf-8").splitlines()[2]
    bad = {"file": "market.md", "row": None, "field": None, "quote": "this sentence is not in the bundle"}
    core = [dict(symbol=r.symbol, weight_pct=w, thesis="fake", evidence=[cite(r)]) for r, w in zip([next(pick) for _ in range(rnd.randint(0, 3))], (20, 15, 10))]
    ents = []
    for r in [next(pick) for _ in range(rnd.randint(0, 3))]:
        dist = rnd.uniform(0.08, 0.2)
        ents.append(dict(symbol=r.symbol, type=rnd.choice(TYPES), entry_price=round(r.close * rnd.uniform(0.95, 1.01), 2), stop_price=0, stop_type=rnd.choice(["fixed", "trailing"]),
                         size_pct=rnd.choice([10, 15, 20]), horizon_sessions=60, p_gain=round(rnd.uniform(0.3, 0.8), 2), reason="fake", evidence=[cite(r), bad if rnd.random() < .2 else cite(r)]))
        ents[-1]["stop_price"] = round(ents[-1]["entry_price"] * (1 - dist), 2)
        ents[-1]["size_pct"] = min(ents[-1]["size_pct"], int(4.9 / dist))
    r = dict(date=d, fake=True, regime=dict(rates_phase=rnd.choice(["hiking", "holding", "cutting"]), stance=rnd.choice(["risk_on", "neutral", "risk_off"]),
             p_kmi_up_60=round(rnd.uniform(0.3, 0.7), 2), summary="fake", evidence=[{"file": "market.md", "row": None, "field": None, "quote": mk[:40]}]),
             core=core, watch=[dict(type="other", subject=r.symbol, trigger="fake", evidence=[cite(r)]) for r in [next(pick)]], entries=ents,
             exposure_pct=sum(x["weight_pct"] for x in core) + sum(x["size_pct"] for x in ents), not_known="fake", contamination_note="")
    f.write_text(json.dumps(r, indent=1), encoding="utf-8")


# ---- stats helpers
def st(x):
    x = np.asarray([v for v in x if v is not None and np.isfinite(v)], float)
    return "n=0" if not len(x) else f"n={len(x)} mean={x.mean():+.1%} median={np.median(x):+.1%} win={np.mean(x > 0):.0%} worst={x.min():+.1%}"


def boot(x, rng, b=3, n_draws=10000):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < b + 1:
        return np.nan, np.nan
    k = -(-len(x) // b)
    idx = (rng.integers(0, len(x) - b + 1, (n_draws, k))[:, :, None] + np.arange(b)).reshape(n_draws, -1)[:, :len(x)]
    m = x[idx].mean(axis=1)
    return tuple(np.percentile(m, [2.5, 97.5]))


def brier(p, o):
    p, o = np.asarray(p, float), np.asarray(o, float)
    return np.mean((p - o) ** 2) if len(p) else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fake", action="store_true")
    ap.add_argument("--draws", type=int, default=500)
    a = ap.parse_args()
    if a.fake:
        for d in ("2019-03-01", "2020-03-20", "2022-07-01", "2024-06-14", "2025-05-12", "2026-07-10"):
            fake(d)
    rng = np.random.default_rng(SEED)
    rows, ent_rows, surprises, pl_win, bp, bo, bkp, bko = [], [], [], [], [], [], [], []
    for f in sorted((ROOT / "data/asof").glob("*/REPLY.json")):
        d = f.parent.name
        r = json.loads(f.read_text(encoding="utf-8"))
        sc = pd.read_csv(f.parent / "screens.csv")
        syms = set(sc.symbol)
        sec = sections((f.parent / "BUNDLE.md").read_text(encoding="utf-8"))
        errs = validate(r, syms)
        cites = all_cites(r)
        ok = [cite_ok(c, sec) for c in cites]
        i0, r_f = t_index(d), rf(t_index(d))
        reg, role = regime_role(d)
        row = dict(date=d, regime=reg, role=role, valid=not errs, n_err=len(errs), errors="; ".join(errs), cites=len(cites), cite_rate=np.mean(ok) if ok else np.nan,
                   exposure=r["exposure_pct"], stance=r["regime"]["stance"], p_kmi_up_60=r["regime"]["p_kmi_up_60"], fake=bool(r.get("fake")))
        core = [x for x in r.get("core", []) if x.get("symbol") in cidx]
        ents = [x for x in r.get("entries", []) if x.get("symbol") in cidx]
        # method items
        cp = [(x, cidx[x["symbol"]]) for x in core]
        cpl = [plan(i0, c) for _, c in cp]
        epl = []
        for x, c in [(x, cidx[x["symbol"]]) for x in ents]:
            k = PX[i0, c] / RAWF[i0, c]
            epl.append((x, c, plan(i0, c, x["stop_type"], (x["entry_price"] - x["stop_price"]) / x["entry_price"], x["stop_price"] * k if x["stop_type"] == "fixed" else None, x["entry_price"] * k)))
        pool = [cidx[s] for s in syms if s in cidx and np.isfinite(PX[i0, cidx[s]])]
        univ = np.zeros(len(cols), bool); univ[pool] = True
        s3r = s3(i0, univ)
        exp = r["exposure_pct"] / 100
        # placebo
        pb = {h: [] for h in HS}
        for _ in range(a.draws):
            it = {h: [] for h in HS}
            for (x, c), p0 in zip(cp, cpl):
                c2 = int(rng.choice(pool)); p2 = plan(i0, c2)
                for h in HS: it[h].append((x["weight_pct"] / 100, ret(i0, c2, p2, h)))
            for x, c, p0 in epl:
                c2 = int(rng.choice(pool)); dd = (x["entry_price"] - x["stop_price"]) / x["entry_price"]; p2 = plan(i0, c2, x["stop_type"], dd)
                for h in HS:
                    it[h].append((x["size_pct"] / 100, ret(i0, c2, p2, h)))
                v = ret(i0, c2, p2, 60)
                if v is not None and np.isfinite(v): pl_win.append(v > 0)
            for h in HS: pb[h].append(book(i0, it[h], h, r_f))
        fall = np.nan
        if i0 + 60 <= N - 1:
            fall = bool(KM[i0 + 1:i0 + 61].min() <= 0.9 * KM[i0])
        row["fall"] = fall
        for h in HS:
            kr = KM[i0 + h] / KM[i0] * 0.9975 ** 2 - 1 if i0 + h <= N - 1 else np.nan
            cr = [ret(i0, c, p, h) for (_, c), p in zip(cp, cpl)]
            er = [ret(i0, c, p, h) for _, c, p in epl]
            items = [(x["weight_pct"] / 100, v) for (x, _), v in zip(cp, cr)] + [(x["size_pct"] / 100, v) for (x, _, _), v in zip(epl, er)]
            bk = book(i0, items, h, r_f)
            pbh = np.array(pb[h], float)
            row.update({f"core_{h}": np.nanmean([v for v in cr if v is not None]) if any(v is not None and np.isfinite(v) for v in cr) else np.nan,
                        f"entries_{h}": np.nanmean([v for v in er if v is not None]) if any(v is not None and np.isfinite(v) for v in er) else np.nan,
                        f"book_{h}": bk, f"kmi_{h}": kr, f"s3_{h}": s3r[h], f"s3x_{h}": s3r[h] * exp + (1 - exp) * r_f * h / 252 if np.isfinite(s3r[h]) else np.nan,
                        f"plac_med_{h}": np.nanmedian(pbh) if np.isfinite(pbh).any() else np.nan,
                        f"plac_pct_{h}": (np.mean(pbh < bk) + 0.5 * np.mean(pbh == bk)) if np.isfinite(bk) and np.isfinite(pbh).any() else np.nan})
            if h == 60:
                for (x, c, p0), v in zip(epl, er):
                    ent_rows.append(dict(date=d, regime=reg, symbol=x["symbol"], type=x["type"], p_gain=x["p_gain"], filled=v is not None, ret60=v, stopped=bool(p0 and p0[1] is not None and p0[1] <= i0 + 60),
                                         ret120=ret(i0, c, p0, 120)))
                    if v is not None and np.isfinite(v):
                        bp.append(x["p_gain"]); bo.append(v > 0)
        # regime probability vs KMI outcome
        if i0 + 60 <= N - 1:
            bkp.append(r["regime"]["p_kmi_up_60"]); bko.append(KM[i0 + 60] > KM[i0])
        # surprises
        k60 = row["kmi_60"]
        why = lambda t: surprises.append(dict(date=d, rule=t, exposure=row["exposure"], stance=row["stance"], reasoning=r["regime"]["summary"], citations=json.dumps(r["regime"]["evidence"])))
        if fall is True and row["exposure"] >= 60: why("exposure>=60 on a fall date")
        if np.isfinite(k60):
            if row["exposure"] <= 30 and k60 >= 0.10: why("exposure<=30 before a KMI rise of 10%+")
            if (row["stance"] == "risk_on" and k60 <= -0.10) or (row["stance"] == "risk_off" and k60 >= 0.10): why("stance contradicted by a 10% move")
        for x, c, p0 in epl:
            if x["p_gain"] >= 0.65 and p0 and p0[1] is not None and p0[1] <= i0 + 60:
                surprises.append(dict(date=d, rule="p_gain>=0.65 with the stop hit", exposure=row["exposure"], stance=row["stance"], reasoning=f"{x['symbol']}: {x['reason']}", citations=json.dumps(x["evidence"])))
        held = {x["symbol"] for x in core} | {x["symbol"] for x in ents}
        for w in r.get("watch", []):
            c = cidx.get(w.get("subject"))
            if c is not None and w["subject"] not in held and i0 + 120 <= N - 1 and PX[i0 + 120, c] / PX[i0, c] - 1 >= 0.5:
                surprises.append(dict(date=d, rule="watched name rose 50%+ in 120 sessions, not entered", exposure=row["exposure"], stance=row["stance"], reasoning=f"{w['subject']}: {w['trigger']}", citations=json.dumps(w["evidence"])))
        rows.append(row)
        print(f"{d}: valid={not errs} cite_rate={row['cite_rate']:.0%} exposure={row['exposure']} book60={row['book_60']:+.1%} s3_60={row['s3_60']:+.1%} kmi60={row['kmi_60']:+.1%}" if np.isfinite(row["book_60"]) else f"{d}: valid={not errs} (no 60-session data)")
    if not rows:
        sys.exit("no REPLY.json found")
    df = pd.DataFrame(rows).sort_values("date")
    out = ROOT / "tests/out"
    df.round(4).to_csv(out / "replay_scores.csv", index=False)
    en = pd.DataFrame(ent_rows)
    en.round(4).to_csv(out / "replay_entries.csv", index=False)
    (ROOT / "data/replay").mkdir(exist_ok=True)
    pd.DataFrame(surprises, columns=["date", "rule", "exposure", "stance", "reasoning", "citations"]).to_csv(ROOT / "data/replay/surprises.csv", index=False)

    L = [f"Replay summary: {len(df)} dates scored ({int(df.fake.sum())} fake). Pilot-size samples give no verdict (replay_exam s7 minimum sample).", ""]
    L.append(f"Validity: {df.valid.mean():.0%} of replies valid; citations resolving {np.nansum(df.cites * df.cite_rate) / max(df.cites.sum(), 1):.0%} ({int(df.cites.sum())} cited)")
    for _, x in df.iterrows():
        L.append(f"  {x.date} {x.regime} {x.role}: errors [{x.errors}] cite_rate {x.cite_rate:.0%}")
    L.append("")
    for h in HS:
        L.append(f"== {h} sessions ==")
        for nm, col in (("book", f"book_{h}"), ("KMI TR", f"kmi_{h}"), ("S3", f"s3_{h}"), ("S3 scaled", f"s3x_{h}"), ("placebo median", f"plac_med_{h}"), ("core", f"core_{h}"), ("entries", f"entries_{h}")):
            L.append(f"  {nm:15s} {st(df[col])}")
        D, sel, ex = df[f"book_{h}"] - df[f"s3_{h}"], df[f"book_{h}"] - df[f"s3x_{h}"], df[f"s3x_{h}"] - df[f"s3_{h}"]
        for nm, x in (("judgment-add D", D), ("  selection", sel), ("  exposure", ex)):
            lo, hi = boot(x, rng)
            L.append(f"  {nm:15s} mean {np.nanmean(x):+.1%}  95% block-bootstrap CI [{lo:+.1%}, {hi:+.1%}]" if np.isfinite(x).any() else f"  {nm:15s} n/a")
        for g, s in df.assign(D=D).groupby("regime"):
            L.append(f"  D in {g}: {st(s.D)}")
        for g, s in df.assign(D=D).groupby("role"):
            L.append(f"  D role {g}: {st(s.D)}")
        cd = df[f"core_{h}"] - df[f"kmi_{h}"]
        L.append(f"  core minus KMI TR: {st(cd)}")
        L.append(f"  book above placebo median on {np.nanmean(df[f'book_{h}'] > df[f'plac_med_{h}']):.0%} of dates; mean placebo percentile {np.nanmean(df[f'plac_pct_{h}']):.0%}")
    L += ["", "== entries =="]
    if len(en):
        f_ = en[en.filled]
        L.append(f"  filled {len(f_)} of {len(en)}; 60-session {st(f_.ret60)}; hit rate {np.mean(f_.ret60 > 0):.0%}" if len(f_) else f"  none filled of {len(en)}")
        if len(f_):
            L.append(f"  share above +50% at 120: {np.nanmean(f_.ret120 > 0.5):.0%}; worst entry {f_.ret60.min():+.1%}; stopped {f_.stopped.mean():.0%}")
            for g, s in f_.groupby("regime"):
                L.append(f"  regime {g}: {st(s.ret60)}")
    pw = np.mean(pl_win) if pl_win else np.nan
    if len(bp):
        L.append(f"  Brier p_gain {brier(bp, bo):.3f} (n={len(bp)}) vs pooled placebo win rate {pw:.0%} constant {brier([pw] * len(bo), bo):.3f}, vs 0.5 {brier([.5] * len(bo), bo):.3f}")
    if len(bkp):
        L.append(f"  Brier p_kmi_up_60 {brier(bkp, bko):.3f} (n={len(bkp)}) vs 0.5 {brier([.5] * len(bko), bko):.3f}")
    fl = df[df.fall.notna()]
    if len(fl):
        fe, ne = fl[fl.fall == True].exposure, fl[fl.fall == False].exposure
        L += ["", f"== sit-out == fall dates (KMI 60-session min at least 10% below T close): {len(fe)} of {len(fl)}; mean exposure {fe.mean():.0f}% on fall dates vs {ne.mean():.0f}% on others; gap {ne.mean() - fe.mean():+.0f} points (the exam wants 20+)"]
    L += ["", f"== surprise log == {len(surprises)} rows in data/replay/surprises.csv: " + "; ".join(f"{k} {v}" for k, v in pd.Series([s['rule'] for s in surprises]).value_counts().items())]
    (out / "replay_summary.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
