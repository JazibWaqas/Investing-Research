"""Draw the fixed PDF sample for the insider-trading test (spec 1). Writes data/insider_sample.csv and prints coverage."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

a = pd.read_parquet(ROOT / "data/announcements.parquet")
i = a[a.klass == "insider_trade"].copy()
i["doc"] = i.document_ids.fillna("").str.split(",").str[0].str.strip()
i["has_doc"] = i.doc != ""
kmi = set(pd.read_csv(ROOT / "data/kmi_allshare_2026-06-05.csv").symbol)
close, vol, tv = P.load_panel()
med = P._med_tv(tv)
def liq(r):
    d = r.datetime.tz_localize(None).normalize()
    k = med.index.searchsorted(d)           # first row >= d; med is already shifted by 1 row
    if k >= len(med) or r.symbol not in med.columns: return False
    v = med.iloc[k][r.symbol]
    return bool(v > 5e6)
i["d"] = i.datetime.dt.tz_localize(None).dt.normalize()
i["liquid"] = [liq(r) for r in i.itertuples()]
i["kmi"] = i.symbol.isin(kmi)
print("rows", len(i), "with doc", i.has_doc.sum(), "multi-doc rows", (i.document_ids.fillna("").str.contains(",")).sum())
print("direction", i.direction.value_counts().to_dict())
s19 = i[(i.d >= "2019-01-01") & i.has_doc]
print("since 2019 with doc", len(s19), "liquid", s19.liquid.sum(), "liquid&kmi", (s19.liquid & s19.kmi).sum())
A = i[i.kmi & i.has_doc & (i.d >= "2026-06-18") & (i.d <= "2026-10-16")]
print("block a", len(A))
B = i[i.kmi & i.has_doc & (i.d >= "2019-01-01") & (i.d <= "2026-06-17")]
cand = sorted(B[B.liquid].symbol.unique())
print("candidate symbols", len(cand))
rng = np.random.default_rng(20261017)
order = list(rng.permutation(cand))
cnt = B.groupby("symbol").size()
drawn, tot = [], 0
for s in order:
    if tot + cnt[s] > 500 - len(A): break
    drawn.append(s); tot += cnt[s]
print("drawn", len(drawn), "backtest filings", tot, "next symbol", order[len(drawn)], cnt[order[len(drawn)]])
print("order", drawn)
Bd = B[B.symbol.isin(drawn)]
S = pd.concat([A.assign(block="a_current"), Bd.assign(block="b_backtest")])
S = S.drop_duplicates("doc")
S[["doc", "datetime", "symbol", "block", "liquid", "direction", "title"]].to_csv(ROOT / "data/insider_sample.csv", index=False)
pd.Series(drawn).to_csv(ROOT / "data/insider_drawn_symbols.csv", index=False, header=["symbol"])
print("sample docs", len(S), "(dup docs dropped:", len(A) + len(Bd) - len(S), ")")
print("drawn: rows in all years, doc share:", i[i.symbol.isin(drawn)].has_doc.mean(), "overall", i.has_doc.mean())
