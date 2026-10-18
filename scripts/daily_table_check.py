"""Checks for data/daily_table.parquet.
Run: .venv/Scripts/python.exe scripts/daily_table_check.py [truncated_table.parquet]
Leak test: rebuild with history cut at 2023-12-29 (DT_TRUNC=2023-12-29 DT_OUT=<path> daily_table.py) and pass that path here.
Every FEATURE column on rows dated <= the cut must be identical to the full build; if any used data after t, it would differ.
Outcome columns are expected to differ near the cut (the window is censored) and are not compared.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parents[1] / "data"
T = pd.read_parquet(D / "daily_table.parquet").sort_values(["symbol", "date"]).reset_index(drop=True)
OUT = ("ret_fwd_", "kmi_ret_fwd_", "mfe_", "mae_", "first_", "filing_within_", "next_open")
FEAT = [c for c in T.columns if not c.startswith(OUT) and c not in ("year",)]
print(f"{len(T):,} rows, {T.symbol.nunique()} symbols, {T.memory_usage(deep=True).sum() / 1e6:.0f} MB in memory, "
      f"{len(FEAT)} feature columns, {T.shape[1] - len(FEAT)} outcome/other columns")

if len(sys.argv) > 1:
    X = pd.read_parquet(sys.argv[1])
    cut = X.date.max()
    m = T[T.date <= cut].merge(X, on=["symbol", "date"], suffixes=("", "_x"), how="outer", indicator=True)
    print(f"leak test (cut {cut.date()}): rows only in full {int((m._merge == 'left_only').sum())}, only in truncated {int((m._merge == 'right_only').sum())}")
    m = m[m._merge == "both"]
    bad = {}
    for c in FEAT:
        if c in ("symbol", "date"):
            continue
        a, b = m[c], m[c + "_x"]
        if c == "kmi_member":
            a, b = a.astype(object).where(a.notna(), "na"), b.astype(object).where(b.notna(), "na")
        if a.dtype.kind == "f":
            diff = ~((a - b).abs() <= 1e-4 * (1 + a.abs())) & ~(a.isna() & b.isna())
        else:
            diff = a.astype(str) != b.astype(str)
            if c == "is_newsless_rise":   # float noise at the 8% threshold between two builds is not a leak
                diff &= (m.ret_5d - 0.08).abs() > 1e-5
        if diff.sum():
            bad[c] = int(diff.sum())
    print("feature columns that differ between full and truncated build:", bad or "none")
    assert not bad, bad

# forward columns must be NaN where the window is not complete (last session of each symbol)
last = T.groupby("symbol").tail(1)
assert last.ret_fwd_1.isna().all() and last.next_open.isna().all()
print("last row of every symbol has no forward outcomes: ok")

pd.set_option("display.width", 250, "display.max_columns", 40)
KEY = ["date", "close", "ret_1d", "gap_open", "ret_5d", "vol_ratio_20_120", "upper_lock", "locks_up_5d", "consecutive_up_days",
       "f_total", "days_since_last_filing", "sector_ret_5d", "is_newsless_rise", "next_open", "ret_fwd_5", "ret_fwd_20", "mfe_5", "mae_5",
       "first_upper_lock_within_5", "first_red_day", "filing_within_10_total"]
for sym, a, b in (("SSGC", "2024-10-23", "2024-11-15"), ("PRL", "2026-04-29", "2026-05-06"), ("PRL", "2026-07-06", "2026-07-14")):
    print(f"\n{sym} {a} .. {b}")
    print(T[(T.symbol == sym) & (T.date >= a) & (T.date <= b)][KEY].round(3).to_string(index=False))

print("\nshare of rows with at least one filing of each class (that session), and of rows with one in the 5 sessions to come:")
for k in ["financial_result", "dividend_or_bonus", "material_info", "insider_trade", "board_meeting_notice", "agm", "credit_rating", "other", "total"]:
    print(f"  {k:22s} today {(T['f_' + k] > 0).mean():6.2%}   next 5 sessions {(T['filing_within_5_' + k] > 0).mean():6.2%}")
print(f"  insider buy {(T.f_insider_buy > 0).mean():.2%}, sell {(T.f_insider_sell > 0).mean():.2%}")
print(f"\nupper_lock {T.upper_lock.mean():.2%}, lower_lock {T.lower_lock.mean():.2%}, liquid {T.liquid.mean():.1%}, newsless rise {T.is_newsless_rise.mean():.2%}, "
      f"kmi_member true {T.kmi_member.eq(True).mean():.1%} / null {T.kmi_member.isna().mean():.1%}")
print("null share of selected columns:")
print(T[["ret_126d", "dist_252_high", "vol_ratio_20_120", "sector_ret_5d", "days_since_last_filing", "regime", "next_open", "ret_fwd_60", "mfe_20", "first_red_day"]].isna().mean().round(3).to_string())
