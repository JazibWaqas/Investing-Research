"""Live screen for the breakout sleeve. Run: .venv/Scripts/python.exe -I scripts/screen_breakout.py [--date YYYY-MM-DD]
Universe: KMI All Share (data/kmi_allshare_2026-06-05.csv), trailing 60-session median traded value > Rs5m (as prices._med_tv).
(a) S3 entry: close above the prior 252-session high.  (b) HIGH52 entry: close within 2% of that high (below it), 63-session return > 0,
ranked by 63-session return.  Prices: bonus/split adjusted panel (partial dividends), as the backtests. Stop = 80% of the highest close in the
last 252 sessions (for (b) this is the stop if it were bought now; a name already above the high may have broken out earlier, the stop is the same).
"""
import re, sys, argparse, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prices as P

ap = argparse.ArgumentParser()
ap.add_argument("--date", default=None, help="run as of this date (last session on or before it)")
args = ap.parse_args()

raw, vol, tv = P.load_panel()
adj = pd.read_parquet(ROOT / "data" / "panel_close_adj.parquet").reindex(index=raw.index, columns=raw.columns)
print(f"raw panel last date {raw.index[-1].date()}; adjusted panel last date {adj.dropna(how='all').index[-1].date()}")
last_adj = adj.dropna(how="all").index[-1]
if last_adj < raw.index[-1]:   # stale adjusted panel: extend with raw closes scaled by the last adjustment factor
    g = (adj.loc[last_adj] / raw.loc[:last_adj].ffill().iloc[-1])
    tail = raw.index > last_adj
    adj.loc[tail] = raw.loc[tail].mul(g, axis=1).values
    print(f"adjusted panel stale: filled {tail.sum()} session(s) after {last_adj.date()} from raw closes")

members = {re.sub(r"(XD|XB|XR)$", "", s) for s in pd.read_csv(ROOT / "data" / "kmi_allshare_2026-06-05.csv").symbol}
mem = np.array([c in members for c in adj.columns])

traded = adj.notna()
px = adj.ffill()
hi = adj.shift(1).rolling(252, min_periods=150).max()          # prior 252-session high (excludes today)
hc = adj.rolling(252, min_periods=150).max()                    # highest close in the last 252 sessions incl. today
r63, r126 = px / px.shift(63) - 1, px / px.shift(126) - 1
mtv = tv.rolling(60, min_periods=40).median().shift(1)
elig = traded & (mtv > 5e6) & mem & hi.notna()
s3 = elig & (adj > hi)
h52 = elig & (adj >= 0.98 * hi) & (r63 > 0)                     # includes names already above (they also fire S3)

i = raw.index.searchsorted(pd.Timestamp(args.date), side="right") - 1 if args.date else len(raw) - 1
t = raw.index[i]
print(f"As of {t.date()}  (eligible names: {int(elig.iloc[i].sum())})\n")

def table(mask, sort):
    s = mask.iloc[i]; s = s[s].index
    d = pd.DataFrame({"close": adj.loc[t, s], "high252": hi.loc[t, s], "r63": r63.loc[t, s], "r126": r126.loc[t, s],
                      "medTV_Rs_m": mtv.loc[t, s] / 1e6, "stop20": 0.8 * hc.loc[t, s]})
    d["above"] = np.where(d.close > d.high252, "yes", "")
    return d.sort_values(sort, ascending=False)
fmt = lambda d: d.to_string(float_format=lambda x: f"{x:.3f}" if abs(x) < 5 else f"{x:.1f}") if len(d) else "  (none)"
print("(a) S3 entry: close above prior 252-session high (ranked by 63-session return)")
print(fmt(table(s3, "r63")))
print("\n(b) HIGH52 entry: within 2% of the 252-session high (or above), 63-session return > 0, ranked by 63-session return")
print(fmt(table(h52, "r63")))

print("\nNames fired per session (S3 / HIGH52 candidates), last 20 sessions")
for d in raw.index[max(i - 19, 0):i + 1]:
    print(f"  {d.date()}  S3 {int(s3.loc[d].sum()):3d}  HIGH52 {int(h52.loc[d].sum()):3d}")
print("\nFor scale")
for d in ("2024-10-01", "2025-07-01", "2026-03-01"):
    d = raw.index[raw.index.searchsorted(pd.Timestamp(d))]
    print(f"  {d.date()}  S3 {int(s3.loc[d].sum()):3d}  HIGH52 {int(h52.loc[d].sum()):3d}  eligible {int(elig.loc[d].sum())}")
