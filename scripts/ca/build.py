"""Build data/corporate_actions.csv (+ unplaced rows) from seed, payouts_raw, PDF reads, announcement titles and price gaps.
Run:  .venv/Scripts/python.exe -I scripts/ca/build.py      (see data/CORPORATE_ACTIONS_NOTES.md for method and coverage)"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import common  # noqa: E402
from common import ROOT, ex_from_start  # noqa: E402
import gapmatch, groups, sources, titles  # noqa: E402
from sources import COLS  # noqa: E402

PRIO = {"seed": 1, "payouts_book_closure": 2, "pdf_book_closure": 3, "pdf_resume_date": 3, "credit_notice": 4,
        "approx": 5, "approx_wide": 6, "gap_inferred": 7}
INIT_PAR = {"NRSL": 5.0}   # par values that are not Rs10 before the first split we know of (doc 169604: NRSL Rs5 -> Rs10 in Aug 2021)

close, vol, tv = common.panel()
idx = close.index
G = gapmatch.Gaps(close, vol)
ann = pd.read_parquet(ROOT / "data/announcements.parquet")
ann["dt"] = ann.datetime.dt.tz_localize(None)
doc_meta = {}
for r in ann[ann.document_ids.fillna("") != ""].itertuples():
    for d in str(r.document_ids).split(","):
        doc_meta.setdefault(d.strip(), (r.symbol, r.dt))


def row(sym, ex, typ, val, adt, src, doc, sub=np.nan):
    return dict(symbol=sym, ex_date=pd.Timestamp(ex) if pd.notna(ex) else pd.NaT, type=typ, value=val, announce_dt=adt,
                ex_date_source=src, source_doc=doc, sub_price=sub)


def round_split(r):
    if r > 1:
        return float(min([2, 3, 4, 5, 10, 20], key=lambda k: abs(k - r)))
    return 1 / float(min([2, 3, 4, 5, 10], key=lambda k: abs(k - 1 / r)))


# ---------------- 1. splits ----------------
reads = pd.read_csv(ROOT / "data/corporate_actions_pdf_reads.csv", dtype={"doc_id": str})
for c in ("book_start", "ex_date"):
    reads[c] = pd.to_datetime(reads[c])
split_rows = []
for r in reads[reads.type == "split"].itertuples():
    sym_dt = doc_meta.get(r.doc_id)
    split_rows.append(row(r.symbol, r.ex_date, "split", r.value, sym_dt[1] if sym_dt else pd.NaT, "pdf_resume_date", f"pdf:{r.doc_id}"))
spl = titles.load(set(close.columns))
spl = spl[spl.kind == "split"].copy()
spl["grp"] = (spl.groupby("symbol").dt.diff().dt.days.fillna(999) > 60).cumsum()
for gi, q in spl.groupby("grp"):
    s = q.symbol.iloc[0]
    lo, hi = q.dt.min() - pd.Timedelta(days=3), q.dt.max() + pd.Timedelta(days=5)
    p = G.pct[s].loc[lo.normalize():hi.normalize()].dropna()
    cand = [(d, 1 / (1 + x)) for d, x in p.items() if x <= -0.35 or x >= 0.6]
    if not cand or any(x["symbol"] == s and abs((x["ex_date"] - d).days) <= 5 for x in split_rows for d, _ in cand):
        continue
    d, ratio = max(cand, key=lambda c: abs(np.log(c[1])))
    k = round_split(ratio)
    if abs(np.log(ratio / k)) > 0.25:
        continue
    cred = q[q.phase == "post"]
    on_day = len(cred) > 0 and ((cred.dt.dt.normalize() - d).abs().dt.days <= 1).any()
    src = "credit_notice" if on_day else ("approx" if G.td_after(q.dt.min().normalize(), 15) >= d else "approx_wide")
    split_rows.append(row(s, d, "split", k, q.dt.min(), src, "title:" + ",".join(q.doc[q.doc != ""].head(2)) + f" ratio from price gap {ratio:.2f}"))
splits = pd.DataFrame(split_rows)


def par_at(sym, date):
    p = INIT_PAR.get(sym, 10.0)
    for r in splits[(splits.symbol == sym) & (splits.ex_date <= pd.Timestamp(date))].sort_values("ex_date").itertuples():
        p /= r.value
    return p


# ---------------- 2. seed, payouts ----------------
seed = sources.load_seed()
pay, pay_unplaced = sources.load_payouts(par_at, idx)

# ---------------- 3. PDF reads (non-split) ----------------
pdf_rows, pdf_open = [], []
for r in reads[reads.type != "split"].itertuples():
    meta = doc_meta.get(r.doc_id, (r.symbol, pd.NaT))
    adt = meta[1]
    if pd.notna(r.ex_date):
        pdf_rows.append(row(r.symbol, r.ex_date, r.type, r.value, adt, "pdf_book_closure", f"pdf:{r.doc_id}", r.sub_price))
    elif pd.notna(r.book_start):
        pdf_rows.append(row(r.symbol, ex_from_start(r.book_start, idx), r.type, r.value, adt, "pdf_book_closure", f"pdf:{r.doc_id}", r.sub_price))
    else:
        pdf_open.append((r, adt))
pdf_rows = pd.DataFrame(pdf_rows)

# gap-match PDF rows that have a value but no dates: window = announcement .. +60 trading days
approx_rows, unplaced = [], []
for r, adt in pdf_open:
    if pd.isna(r.value) or pd.isna(adt):
        unplaced.append(row(r.symbol, pd.NaT, r.type, r.value, adt, "none", f"pdf:{r.doc_id}", r.sub_price))
        continue
    lo = adt.normalize() - pd.Timedelta(days=2)
    hi = G.td_after(adt.normalize(), 60)
    d = G.find(r.symbol, r.type, r.value, lo, hi)
    if d is None:
        unplaced.append(row(r.symbol, pd.NaT, r.type, r.value, adt, "none", f"pdf:{r.doc_id} {r.note}", r.sub_price))
    else:
        src = "approx" if d <= G.td_after(adt.normalize(), 15) else "approx_wide"
        approx_rows.append(row(r.symbol, d, r.type, r.value, adt, src, f"pdf:{r.doc_id} value; date by price gap"))
approx_rows = pd.DataFrame(approx_rows)

# ---------------- 4. bonus event groups from titles (no PDF read covers them) ----------------
e = titles.load(set(close.columns))
sus = pd.read_csv(ROOT / "data/suspected_corporate_actions.csv", parse_dates=["date"])
bonus = groups.group_events(e, "bonus")
read_docs = set(reads.doc_id)
placed_pdf = pd.concat([x for x in (pdf_rows, approx_rows) if len(x)], ignore_index=True)
read_syms_dates = reads.merge(pd.DataFrame([(d, m[1]) for d, m in doc_meta.items() if d in read_docs], columns=["doc_id", "adt"]), on="doc_id", how="left")
grp_rows = []
for gi, q in bonus.groupby("grp"):
    s = q.symbol.iloc[0]
    first, last = q.dt.min(), q.dt.max()
    if any(d in read_docs for d in q.doc):
        continue
    rr = read_syms_dates[(read_syms_dates.symbol == s) & (read_syms_dates.type == "bonus") & read_syms_dates.adt.between(first - pd.Timedelta(days=100), last + pd.Timedelta(days=60))]
    if len(rr):
        continue
    pc = q.pct.dropna()
    val = float(pc.mode().iloc[0]) / 100 if len(pc) and pc.nunique() == 1 else np.nan
    lo, hi = first.normalize() - pd.Timedelta(days=80), last.normalize() + pd.Timedelta(days=3)
    docs = ",".join(q.doc[q.doc != ""].head(2))
    if pd.notna(val):
        d = G.find(s, "bonus", val, lo, hi)
        if d is not None:
            grp_rows.append(row(s, d, "bonus", val, first, "approx_wide", f"title:{docs} value; date by price gap"))
        else:
            unplaced.append(row(s, pd.NaT, "bonus", val, first, "none", f"title:{docs}"))
        continue
    cs = sus[(sus.symbol == s) & sus.date.between(lo, hi) & (sus.pct_move < 0)]
    if len(cs) == 1:
        d, pm = cs.date.iloc[0], cs.pct_move.iloc[0]
        imp = 1 / (1 + pm) - 1
        v = round(imp / 0.05) * 0.05 if imp < 1.5 else round(imp)
        grp_rows.append(row(s, d, "bonus", round(v, 4), first, "gap_inferred", f"title:{docs} value inferred from gap {imp:.3f}, rounded to 5%"))
    else:
        unplaced.append(row(s, pd.NaT, "bonus", np.nan, first, "none", f"title:{docs} ambiguous: {len(cs)} gaps"))
grp_rows = pd.DataFrame(grp_rows)

# ---------------- 5. cash dividends in titles that state a percentage or Rs per share ----------------
cash_rows = []
ct = e[(e.kind == "cash") & (e.pct.notna() | e.rs.notna())]
for r in ct.itertuples():
    v = r.rs if pd.notna(r.rs) else r.pct / 100 * par_at(r.symbol, r.dt)
    if r.phase == "post":
        lo, hi = r.dt.normalize() - pd.Timedelta(days=75), r.dt.normalize() + pd.Timedelta(days=3)
    else:
        lo, hi = r.dt.normalize() - pd.Timedelta(days=3), G.td_after(r.dt.normalize(), 45)
    d = G.find(r.symbol, "cash", v, lo, hi, min_exp=0.10)
    if d is None:
        unplaced.append(row(r.symbol, pd.NaT, "cash", v, r.dt, "none", f"title:{r.doc} {r.title[:60]}"))
    else:
        src = "approx" if (r.phase == "pre" and d <= G.td_after(r.dt.normalize(), 15)) else "approx_wide"
        cash_rows.append(row(r.symbol, d, "cash", v, r.dt, src, f"title:{r.doc} value; date by price gap"))
cash_rows = pd.DataFrame(cash_rows)

# rights stated in titles: ratio and price only, no ex-date -> unplaced
for r in e[(e.kind == "right") & (e.phase == "pre") & e.pct.notna()].itertuples():
    sp = re.search(r"(?:premium|discount)[^\d]{0,12}(\d+(?:\.\d+)?)", r.title, re.I)
    unplaced.append(row(r.symbol, pd.NaT, "right", r.pct / 100, r.dt, "none", f"title:{r.doc} {r.title[:70]}", float(sp.group(1)) if sp else np.nan))

# ---------------- 6. merge ----------------
parts = [seed, pay, pdf_rows, splits, approx_rows, grp_rows, cash_rows]
allrows = pd.concat([p for p in parts if len(p)], ignore_index=True)
allrows["ex_date"] = pd.to_datetime(allrows.ex_date)
allrows["prio"] = allrows.ex_date_source.map(PRIO).fillna(9)
allrows = allrows.dropna(subset=["ex_date"]).sort_values(["symbol", "type", "prio", "ex_date"]).reset_index(drop=True)
keep = []
for (s, t), g in allrows.groupby(["symbol", "type"], sort=False):
    taken = []
    for r in g.itertuples():
        dup = [k for k in taken if abs((k.ex_date - r.ex_date).days) <= 4 and (t == "split" or abs(k.value - r.value) <= 0.35 * max(abs(k.value), 1e-9))]
        if not dup:
            taken.append(r)
    keep += [t_.Index for t_ in taken]
acts = allrows.loc[keep].sort_values(["symbol", "ex_date", "type"]).reset_index(drop=True)

# ---------------- 7. cross-check against seed ----------------
dis = []
for r in seed.itertuples():
    o = allrows[(allrows.symbol == r.symbol) & (allrows.type == r.type) & (allrows.ex_date_source != "seed") & ((allrows.ex_date - r.ex_date).abs() <= pd.Timedelta(days=10))]
    if len(o):
        o = o.iloc[(o.ex_date - r.ex_date).abs().argsort().iloc[0]]
        dis.append((r.symbol, r.type, r.ex_date.date(), r.value, o.ex_date.date(), o.value, o.ex_date_source, (o.ex_date - r.ex_date).days, o.value / r.value - 1 if r.value else np.nan))
    else:
        dis.append((r.symbol, r.type, r.ex_date.date(), r.value, None, None, None, None, None))
seed_cmp = pd.DataFrame(dis, columns=["symbol", "type", "seed_ex", "seed_value", "our_ex", "our_value", "our_source", "ex_diff_days", "value_ratio_minus_1"])

out = acts[COLS].copy()
out["ex_date"] = out.ex_date.dt.strftime("%Y-%m-%d")
out["announce_dt"] = pd.to_datetime(out.announce_dt).dt.strftime("%Y-%m-%d %H:%M")
out["value"] = out.value.round(6)
out.to_csv(ROOT / "data/corporate_actions.csv", index=False)
unp = pd.concat([pay_unplaced, pd.DataFrame(unplaced, columns=COLS)], ignore_index=True)
unp = unp.assign(announce_dt=pd.to_datetime(unp.announce_dt).dt.strftime("%Y-%m-%d %H:%M")).drop(columns="ex_date")
unp.drop_duplicates().to_csv(ROOT / "data/corporate_actions_unplaced.csv", index=False)
seed_cmp.to_csv(ROOT / "data/raw/corporate_actions_seed_compare.csv", index=False)
acts.to_pickle(Path(__file__).with_name("_acts.pkl"))
print(len(out), out.type.value_counts().to_dict(), out.ex_date_source.value_counts().to_dict(), "unplaced", len(unp))
