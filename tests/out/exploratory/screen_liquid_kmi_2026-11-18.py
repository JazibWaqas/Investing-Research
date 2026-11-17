import re, os, glob
import numpy as np, pandas as pd
from pathlib import Path
ROOT = Path(r"c:\Users\JazibWaqas\Documents\GitHub\Investing-Research"); os.chdir(ROOT)
S = Path(r"C:\Users\JAZIBW~1\AppData\Local\Temp\claude\c48c7d45e4ac7dc7\5316537c-aaaf-4ab3-8e6d-fb307ab5b1ed\scratchpad")
def parse(path):
    t = path.read_text(encoding="utf-8")
    i = t.find("fiscalYear:["); j = t.find("fiscalYear:[", i + 1); seg = t[i:j] if j > 0 else t[i:]
    def arr(key):
        m = re.search(r"[,{]" + key + r":\[([^\]]*)\]", seg)
        return None if not m else [np.nan if x.strip() in ("null", "") else float(x) for x in m.group(1).split(",")]
    ni = arr("netinccmn") or arr("netinc"); rev = arr("revenue"); gp = arr("gp") or arr("grossProfit")
    ids = re.findall(r'<th id="(\d{4}-\d{2}-\d{2})"', t)[:len(ni)]
    d = pd.DataFrame({"pe": pd.to_datetime(ids), "ni": ni[:len(ids)]})
    if rev: d["rev"] = rev[:len(ids)]
    if gp: d["gp"] = gp[:len(ids)]
    return d.sort_values("pe").reset_index(drop=True)
t = pd.read_csv(S / "nov17_table.csv", index_col=0)
sym = pd.read_csv("data/symbols.csv") if os.path.exists("data/symbols.csv") else None
sec = {}
if sym is not None:
    sc = [c for c in sym.columns if "sector" in c.lower()][0]; kc = [c for c in sym.columns if "symbol" in c.lower()][0]
    sec = dict(zip(sym[kc], sym[sc]))
w = pd.read_csv("data/winners_library.csv")
last_mult = w[w.start_date >= "2022-06-01"].groupby("symbol").multiple.max()
k = pd.read_csv("data/macro/kse100.csv", parse_dates=["date"]).sort_values("date").set_index("date").close.pct_change()
rows = []
for f in sorted((ROOT / "data/raw/stockanalysis_nov26").glob("*_income.html")):
    s = f.name.split("_")[0]
    try: q = parse(f)
    except Exception as e: print(s, "parse fail", e); continue
    q = q.dropna(subset=["ni"])
    if len(q) < 5: continue
    last = q.iloc[-1]; ya = q[q.pe == last.pe - pd.DateOffset(years=1)]
    g = 100 * (last.ni / ya.ni.iloc[0] - 1) if len(ya) and ya.ni.iloc[0] > 0 else np.nan
    ttm = q.tail(4).ni.sum()
    c = pd.read_csv(f"data/prices_raw/{s}.csv", parse_dates=["date"]).sort_values("date").set_index("date")
    shares_m = None
    m = re.search(r"[,{]sharesBasic:\[([^\]]*)\]", f.read_text(encoding="utf-8"))
    if m:
        vals = [x for x in m.group(1).split(",") if x.strip() not in ("null", "")]
        shares_m = float(vals[0]) if vals else None   # newest first on the page
    px = c.close.iloc[-1]
    pe_ttm = px * shares_m / ttm if shares_m and ttm > 0 else np.nan
    pe_run = px * shares_m / (4 * last.ni) if shares_m and last.ni > 0 else np.nan
    gm = 100 * last.gp / last.rev if "gp" in q and "rev" in q and pd.notna(last.get("gp")) and last.rev else np.nan
    gm_ya = 100 * ya.gp.iloc[0] / ya.rev.iloc[0] if len(ya) and "gp" in q and pd.notna(ya.gp.iloc[0]) and ya.rev.iloc[0] else np.nan
    r = c.close.pct_change(); j = pd.concat([r, k], axis=1, sort=True).dropna().tail(500); j = j[j.iloc[:, 0].abs() < 0.3]
    beta = j.cov().iloc[0, 1] / j.iloc[:, 1].var()
    rows.append(dict(sym=s, sector=str(sec.get(s, ""))[:18], q=last.pe.date(), ni_g=g, gm=gm, gm_ya=gm_ya, pe_ttm=pe_ttm, pe_run=pe_run,
                     px=px, vshi=t.loc[s, "vshi"], v200=t.loc[s, "v200"], d20=t.loc[s, "d20"], beta=beta, last_turn=last_mult.get(s, np.nan), tv=t.loc[s, "tv"]))
R = pd.DataFrame(rows).set_index("sym")
R.to_csv(S / "screen_nov18.csv")
pd.set_option("display.width", 250)
print(R.sort_values("ni_g", ascending=False).round(1).to_string())
