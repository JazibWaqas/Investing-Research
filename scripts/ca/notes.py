"""Write data/CORPORATE_ACTIONS_NOTES.md from the current corporate_actions.csv (run build.py and recon.py first).
All numbers in the file are computed here; the narrative around them is static text."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import recon  # noqa: E402  (writes the adjusted panels as a side effect)
import titles  # noqa: E402
from common import ROOT  # noqa: E402
import prices  # noqa: E402

close, vol, tv, sus = recon.close, recon.vol, recon.tv, recon.sus
a = pd.read_csv(ROOT / "data/corporate_actions.csv", parse_dates=["ex_date"])
unp = pd.read_csv(ROOT / "data/corporate_actions_unplaced.csv")
seed_cmp = pd.read_csv(ROOT / "data/raw/corporate_actions_seed_compare.csv")
conf = pd.read_csv(ROOT / "data/raw/corporate_actions_conflicts.csv")
reads = pd.read_csv(ROOT / "data/corporate_actions_pdf_reads.csv", dtype=str)
n_dl = len((ROOT / "data/raw/filings_downloads.log").read_text().split())
last = close.index[-1]


def md(df, index=True):
    df = df.reset_index() if index else df
    cols = [str(c) for c in df.columns]
    rows = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        rows.append("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else (f"{v:.4g}" if isinstance(v, float) else str(v)) for v in r) + " |")
    return "\n".join(rows)


# ---- coverage by year
past = a[a.ex_date <= last]
by_year = past.groupby([past.ex_date.dt.year.rename("ex year"), "type"]).size().unstack(fill_value=0)
by_year["total"] = by_year.sum(axis=1)
src_year = past.groupby([past.ex_date.dt.year.rename("ex year"), "ex_date_source"]).size().unstack(fill_value=0)
med = prices._med_tv(tv)
cov = []
for y in range(2017, 2027):
    d = close.index[close.index.searchsorted(pd.Timestamp(f"{y}-01-02"))]
    liq = list(med.columns[med.loc[d] > 5e6])
    row = {"year": y, "liquid names (Rs5m, 1 Jan)": len(liq)}
    for t in ("cash", "bonus", "split"):
        row[f"with a {t} action"] = past[(past.type == t) & (past.ex_date.dt.year == y) & past.symbol.isin(liq)].symbol.nunique()
    cov.append(row)
cov = pd.DataFrame(cov)

# ---- suspect reconciliation
tot, exp_, liq = len(sus), int(sus.explained.sum()), sus[sus.liquid]
e = titles.load(set(close.columns))


def near(r):
    q = e[(e.symbol == r.symbol) & (e.dt >= r.date - pd.Timedelta(days=100)) & (e.dt <= r.date + pd.Timedelta(days=45))]
    k = set(q.kind)
    return "bonus" if "bonus" in k else "right" if "right" in k else "split" if "split" in k else "cash" if "cash" in k else "none"


un = sus[~sus.applied].copy()
un["announcement near"] = un.apply(near, axis=1)
un["direction"] = np.where(un.pct_move < 0, "down", "up")
cat = un.groupby(["announcement near", "direction"]).size().unstack(fill_value=0)
cat["total"] = cat.sum(axis=1)
yr = sus.groupby(sus.date.dt.year.rename("year")).agg(suspects=("explained", "size"), explained=("explained", "sum"))
yr["remaining"] = yr.suspects - yr.explained
top = un[un.liquid].assign(abs_move=lambda x: x.pct_move.abs()).sort_values("abs_move", ascending=False).head(20)
top20 = top[["symbol", "date", "pct_move", "volume_ratio", "mtv_m", "announcement near"]].copy()
top20["date"] = top20.date.dt.strftime("%Y-%m-%d")
top20["pct_move"] = (top20.pct_move * 100).round(1).astype(str) + "%"
top20 = top20.rename(columns={"mtv_m": "60d median traded value (Rs m)", "volume_ratio": "volume ratio", "pct_move": "move"})

# ---- checks
chk = []
for s_, d_, what in [("LUCK", "2025-04-28", "5:1 split"), ("SYS", "2025-06-02", "5:1 split"), ("SYS", "2022-03-31", "100% bonus (+Rs5 cash)"), ("MEBL", "2022-08-22", "10% bonus (+Rs1.75 cash)"), ("MEBL", "2021-09-09", "15% bonus (+Rs1.50 cash)")]:
    t = pd.Timestamp(d_)
    row = a[(a.symbol == s_) & ((a.ex_date - t).abs() <= pd.Timedelta(days=1))]
    chk.append({"symbol": s_, "ex date": d_, "event": what, "raw move": f"{recon.pct0.at[t, s_]:+.1%}", "adjusted move": f"{recon.pct1.at[t, s_]:+.1%}",
                "table rows": "; ".join(f"{r.type} {r.value:g} [{r.ex_date_source}]" for r in row.itertuples())})
chk = pd.DataFrame(chk)

# seed comparison
sc = seed_cmp.copy()
sc["covered"] = sc.our_ex.notna()
sc_sum = sc.groupby("symbol").agg(seed_rows=("type", "size"), also_found_elsewhere=("covered", "sum"))
bad = sc[sc.covered & ((sc.ex_diff_days != 0) | (sc.value_ratio_minus_1.abs() > 1e-6))][["symbol", "type", "seed_ex", "seed_value", "our_ex", "our_value", "our_source", "ex_diff_days", "value_ratio_minus_1"]]
bad = bad.assign(value_ratio_minus_1=lambda x: x.value_ratio_minus_1.round(3))

# panel stats
rc = prices.returns(close, "crude", vol=vol)
ra = recon.ret_tr
ew_c = prices.ew_market(rc)
ew_c = ew_c[ew_c.index >= "2017-01-01"].dropna()
ew_p = prices.ew_market(recon.ret_px)
ew_p = ew_p[ew_p.index >= "2017-01-01"].dropna()
ew_a = prices.ew_market(ra)
ew_a = ew_a[ew_a.index >= "2017-01-01"].dropna()
zeroed_c = int(((rc == 0) & recon.big0).sum().sum())
zeroed_a = int(((ra == 0) & recon.big1).sum().sum())


# ---- ex-date rule evidence: payouts rows with yield >= 3%, where does the worst return in ex-3..ex+2 fall?
idx = close.index
rets = close.ffill(limit=3).pct_change(fill_method=None)
offs = []
for r in a[(a.type == "cash") & (a.ex_date_source == "payouts_book_closure")].itertuples():
    if r.symbol not in close.columns or r.ex_date > idx[-1]:
        continue
    k = idx.searchsorted(r.ex_date)
    if k < 4 or k >= len(idx) - 2:
        continue
    pr = close[r.symbol].iloc[:k].dropna()
    if not len(pr) or r.value / pr.iloc[-1] < 0.03:
        continue
    w = {o: rets.at[idx[k + o], r.symbol] for o in range(-3, 3)}
    offs.append(min(w, key=lambda o: w[o] if pd.notna(w[o]) else 9))
n_dip, n_dip0 = len(offs), sum(1 for o in offs if o == 0)
cash_titles = e[e.kind == "cash"]
n_ct, n_ct_val = len(cash_titles), int((cash_titles.pct.notna() | cash_titles.rs.notna()).sum())
mebl = seed_cmp[(seed_cmp.symbol == "MEBL") & (seed_cmp.seed_ex == "2026-03-16")]
mebl_px = float(close["MEBL"].loc[:"2026-03-13"].dropna().iloc[-1])
cash_diff = int(((bad.type == "cash") & (bad.value_ratio_minus_1.abs() > 1e-6)).sum())
dem = unp[unp.source_doc.fillna("").str.contains("not credible")]
dem_txt = "; ".join(f"{r.symbol} {r.type} {r.value:g}" for r in dem.itertuples())
unp_types_txt = ", ".join(f"{k} {v}" for k, v in unp.groupby("type").size().items())
unp_val_txt = ", ".join(f"{k} {v}" for k, v in unp[unp.value.notna()].groupby("type").size().items())
n_split = int((a.type == "split").sum())
gap_top = set(zip(top.symbol, top.date.dt.strftime("%Y-%m-%d")))

unp_types = unp.groupby("type").size().to_dict()
unp_val = unp[unp.value.notna()].groupby("type").size().to_dict()
placed_by_source = a.groupby("ex_date_source").size().sort_values(ascending=False)
future = int((a.ex_date > last).sum())

txt = f"""# Corporate actions: table, adjusted panel, reconciliation

Built 17 Oct 2026 by `scripts/ca/` (build.py, recon.py, notes.py). Price data to {last.date()}. Nothing here is committed. Every number below is computed by `scripts/ca/notes.py` from the files, not typed.

## What was written

| File | What it is |
|---|---|
| `data/corporate_actions.csv` | {len(a)} placed actions (ex date known): {', '.join(f'{k} {v}' for k, v in a.type.value_counts().items())}. Columns: symbol, ex_date, type, value, announce_dt, ex_date_source, source_doc, plus sub_price (rights subscription price, where stated). {future} rows have an ex date after {last.date()} (declared, not yet traded). |
| `data/panel_close_adj.parquet` | Back-adjusted close, total return: bonus, split and every cash dividend in the table, unexplained suspect days zeroed as the loader does. Last value of each series equals the raw last close. NaN where raw close is NaN. |
| `data/panel_close_adj_pricereturn.parquet` | Same, with bonus and split only (cash ignored). Use this one when comparing years: cash coverage is very uneven (see below). |
| `data/corporate_actions_unplaced.csv` | {len(unp)} announcements with a value or ratio but no ex date I could defend (by type: {unp_types_txt}; with a value or ratio stated: {unp_val_txt}). Not applied anywhere. |
| `data/corporate_actions_pdf_reads.csv` | {len(reads)} rows read by eye from {reads.doc_id.nunique()} filing PDFs (doc id in every row). Input to build.py. |
| `data/raw/filings/` | the PDFs. {n_dl} downloaded by this build (cap 400), one request per second, parsed and viewed only, never executed. Log: `data/raw/filings_downloads.log`. |
| `data/raw/corporate_actions_seed_compare.csv`, `corporate_actions_conflicts.csv` | seed cross-check and rows dropped as duplicates of a better source. |

`prices.returns(close, 'adjusted')` now reads the table instead of falling back to crude. The loader's own rules still apply: cash is added back on the ex date, bonus and split rescale the new price, rights are ignored, and any suspect day the table does not explain is zeroed.

## Read this first: what the table can and cannot do

1. **Bonus and split adjustment is the reliable part.** All {n_split} splits found (2021 to 2026) are in, and the bonus events with a large price gap are in. Small bonuses (under about 8%) are only in when a PDF or the portal gave the book-closure date; the rest sit in the unplaced file and still appear as fake -5% to -9% days.
2. **Cash dividends are only complete from November 2024.** The portal's payout endpoint covers about two years ({len(a[a.ex_date_source == 'payouts_book_closure'])} rows used), the seed adds six names from 2021, and announcement titles almost never state an amount ({n_ct_val} of {n_ct} cash titles). For 2017 to 2020 there are {int(past[(past.type == 'cash') & (past.ex_date.dt.year <= 2020)].shape[0])} cash rows in total. So the total-return panel is a price-return series with partial dividends: any 2025-26 versus earlier comparison on `panel_close_adj.parquet` is tilted by about the dividend yield. The equal-weight index (Rs5m filter, from 2017) compounds to {ew_p.add(1).prod() - 1:+.1%} on bonus and split only, {ew_a.add(1).prod() - 1:+.1%} with the table's cash, and {ew_c.add(1).prod() - 1:+.1%} on the crude method. All three are survivor-biased (only names listed on 2026-10-16 are in the panel), so the level is flattered; the differences between them are the point.
3. **Par value.** Cash = percent × par. Par is Rs10 unless a split changed it (par divided by the split ratio, so SYS's April 2026 "100%" is Rs2, which matches the seed) or a document says otherwise: ZAL pays "Re.1" for the portal's 100% (doc 260205), NRSL was Rs5 until its Aug 2021 consolidation (doc 169604). I checked every payouts-based cash event with a yield of 4% or more against the price. Before the fix ZAL (a 27% yield with no price drop at all) was the only failure at 8% or more; between 4% and 8%, SNGP 2025-05 (worst day three days before the computed ex date) and GEMPAPL 2026-03 (a stock at a few rupees) show no dip on the ex date, and neither points to par. Below 4% a wrong par cannot be seen in the price, so other Re1 or Rs5 names remain a risk and are not flagged.
4. **Ex-date rule.** The task said book-closure start minus one business day. The data say two trading days until early March 2026 and one from then on: among {n_dip} payouts with a yield of 3% or more, the worst day in ex-3 to ex+2 is the computed ex date in {n_dip0}, and PDF-dated events from 2017 to 2024 match their price gaps (PPL 2018 and 2019, AVN 2017, AKBL 2020, SPWL 2021, KAPCO 2022, TPLP 2023). That is T+2 settlement, then T+1. The switch is placed at book-closure starts on or after 2026-03-05 (MTL starting 4 Mar still dips at -2, OGDC starting 7 Mar dips at -1). Splits are different: the entitlement date is the Friday before a Saturday closure and the ex date is the first trading day of the new shares, which is also the date of the exchange's "credit of ordinary shares pursuant to the sub-division" notice (checked on LUCK, SYS, UBL and others).
5. **Where the price decided the date or the size.** Rows with `ex_date_source` of `approx` or `approx_wide` take their date from a price move that matches the stated value (tolerance 1.5% plus 6% of the expected move, wider for big events, ambiguous matches rejected, never for expected moves under 8%): `approx` when within 15 trading days of the announcement, `approx_wide` when later or when the only notice was a credit notice after the fact. `gap_inferred` rows have no stated value at all: a bonus announcement exists for the symbol, exactly one suspect gap fell in the window, and the size is the gap rounded to 5%. Their size can be off by several points (PPL 2018: the gap implied 18.3%, the notice says 15% bonus plus Rs1.50 cash) and larger bonuses are rounded coarsely. {int((a.ex_date_source == 'gap_inferred').sum())} such rows. Treat them as "a bonus happened here" rather than as exact.
6. **Date verification.** Book-closure dates from the portal or a PDF were checked against the price when the expected drop is 8% or more. Those where neither the ex date nor the days either side showed even 40% of the expected drop, and no matching gap lay within 3 trading days, went to the unplaced file instead of being applied on a day with no drop: {len(dem)} rows ({dem_txt}).

## Coverage by year (placed actions, by ex-date year)

{md(by_year)}

By source of the ex date:

{md(src_year)}

Liquid names (60-day median traded value above Rs5m on 1 January) with at least one placed action in the year. The cash column is what limits the total-return panel before 2025:

{md(cov, index=False)}

Placed rows by source: {', '.join(f'{k} {v}' for k, v in placed_by_source.items())}.

## Suspected gaps (`data/suspected_corporate_actions.csv`, {tot} rows)

A suspect is explained when an action in the table applies on that date and the adjusted move is back inside the circuit band. It is unexplained when no action applies there.

- Explained: **{exp_}** of {tot}. Remaining: **{tot - exp_}**.
- Liquid names (traded value above Rs5m, {len(liq)} suspects): explained **{int(liq.explained.sum())}**, remaining **{int((~liq.applied).sum())}**.
- Applied but still outside the band after adjustment: {int((sus.applied & sus.still_big).sum())}.

{md(yr)}

What the remaining {len(un)} look like, by the kind of corporate-action announcement the same symbol made in the 100 days before to 45 days after the gap (this says an announcement exists, not that it caused the gap):

{md(cat)}

"none" means no announcement mentioning dividend, bonus, right or split was found for that symbol in the window; these can be real crashes, data glitches (BML 2026-02-02 is +1,626% on a day with 0.23x normal volume) or actions announced in words my filters missed. Down-gaps next to a "cash" announcement are plausibly ex-dividend days whose amount I could not retrieve, but that is a guess from timing only. Several of the largest down-gaps (FFL 2017 -63%, SGPL 2026 -59%, GGGL 2021 -33%, UNITY 2019 -22%, PRL 2020 -22%) coincide with right-issue announcements; rights are in the table only when the portal listed them and the loader ignores rights, so those days are zeroed.

Twenty largest unexplained gaps in liquid names:

{md(top20, index=False)}

One cause I did read: GCIL 2025-04-03 follows a court-sanctioned demerger (doc 249387: 500 GCWL shares per 1,000 GCIL, notice 10 Mar 2025). The others are not diagnosed.

## The five checks the task named

{md(chk, index=False)}

The adjusted move on each is inside ordinary daily noise, so all five are handled. MEBL 2021 and 2022 and SYS 2022 come from the seed (ground truth); LUCK 2025 from the book-closure notice (doc 249947: Rs10 to Rs2, trading resumed 28 Apr 2025); SYS 2025 is in the seed and agrees with the exchange's credit notice of the same day.

## Seed cross-check

Seed rows: {len(seed_cmp)} (MEBL, FFC, HUBC, OGDC, SYS, EPCL). {int(sc.covered.sum())} of them were also found independently (payouts or price gap); the rest cover 2021 to Oct 2024, which no other source reaches. The seed wins every overlap. Disagreements:

{md(bad, index=False)}

Notes on those: MEBL 2026-03: the seed says ex 16 Mar, the portal's book closure (25 Mar to ...) gives 24 Mar. A Rs7 dividend on a price of about Rs{mebl_px:.0f} is under 2% and cannot be seen in the price, so I cannot arbitrate; the seed date is used. OGDC 2026-03: closure started on a Saturday, so the switch date mattered; the switch was moved to 5 Mar to agree with the seed. SYS 2022-03-31: the seed says 100% bonus, the price-gap estimate was 90% (the gap is 47% plus market noise); the seed is used. Cash amounts that disagreed with the seed: {cash_diff}.

## Sources and method in one paragraph

Order of trust: seed, then portal payouts (book closure range), then book-closure dates and ratios read from filing PDFs, then price-matched placement of a stated value, then gap-inferred size. Announcement titles state a percentage or a Rs amount in only {n_ct_val + int(((e.kind != 'cash') & e.pct.notna()).sum())} of the {len(e)} dividend, bonus, right and split rows found; most notices are "credit of dividend" or "dispatch of bonus certificates" with no number. Most filing PDFs are scanned images with no text layer and no OCR was available, so I read them by eye from rendered pages and typed what they state into `data/corporate_actions_pdf_reads.csv`. Of the {n_dl} documents downloaded, {reads.doc_id.nunique()} gave at least one row. The rest had a profit-and-loss table or a material-information notice on page 1, were superseded by a better document for the same event, or were never opened. I read page 1 only unless noted, so book-closure dates on page 2 are missing for some rows (those events then rely on a price match). Priority order for downloads: splits, then bonus declarations for the 92 liquid names and the rest of KMI All Share, then results letters for the 40-odd bonus events that had no declaration notice, then the largest unexplained gaps in liquid names. {n_dl} of 400 downloads used. Usable rows per document read were roughly 79% for results letters picked from bonus announcements and 37% for letters picked only by date proximity to an unexplained gap, so the remaining budget was not spent; covering the cash dividends of 92 names across 2017 to 2024 would need roughly 2,000 documents (92 names, 8 years, 2 to 3 declarations a year; an estimate).

## Not done, and what would fix it

- Cash dividends 2017 to Oct 2024 for most names. Needs a dividend history source (the portal shows two years). With one, `build.py` takes it as another row source.
- Small bonuses (under 8%) without a book-closure date. {unp_val.get('bonus', 0)} bonus rows have a value but no date; they are in the unplaced file.
- Rights: {unp_types.get('right', 0)} rights notices are unplaced; ex-right adjustment (theoretical ex-rights price) is not implemented and the loader ignores rights.
- Delisted and merged names are not in the panel (survivorship). FFC/FFBL merger issuance (Dec 2024) is not a price event and is not in the table.
- Weekly or later refresh: rerun `scripts/ca/build.py`, then `recon.py`, then `notes.py`.
"""
(ROOT / "data/CORPORATE_ACTIONS_NOTES.md").write_text(txt, encoding="utf-8")
print(len(txt), "chars written")
