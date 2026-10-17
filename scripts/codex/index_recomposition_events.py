"""Index recomposition event study. Run from repository root."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prices_codex import ROOT, load_prices, stats, compound

RNG = np.random.default_rng(9917)
COST = .005


def fmt(x):
    return "NA" if not np.isfinite(x) else f"{100*x:.2f}"


def window_return(ret, ew, symbol, dates):
    if len(dates) == 0 or symbol not in ret:
        return np.nan
    s = ret.loc[dates, symbol]
    m = ew.loc[dates]
    if len(s) != len(dates) or s.isna().any() or m.isna().any():
        return np.nan
    return (1 + compound(s)) / (1 + compound(m)) - 1


def main():
    p = load_prices()
    ret, ew, liq = p["ret"], p["ew"], p["liquidity"]
    calendar = ew.dropna().index
    changes = pd.read_csv(ROOT / "data/index_changes.csv", parse_dates=["announce_date", "effective_date"])
    source_n = len(changes)
    changes = changes[changes.announce_date.notna() & changes.effective_date.notna()
                      & changes.source_url.fillna("").ne("derived")].copy()
    changes = changes.drop_duplicates(["index", "announce_date", "effective_date", "symbol", "action"])
    print(f"source_rows={source_n} eligible_rows={len(changes)} price_symbols={ret.shape[1]} "
          f"neutralized_gaps={len(p['actions'])}")
    records = []
    for row in changes.itertuples(index=False):
        a = calendar.searchsorted(row.announce_date, side="right")
        pre_end = calendar.searchsorted(row.announce_date, side="left")
        e = calendar.searchsorted(row.effective_date, side="right") - 1
        if pre_end < 20 or e < a or e + 20 >= len(calendar) or row.symbol not in ret:
            continue
        spans = {"anticipation": calendar[pre_end-20:pre_end],
                 "announce_to_effective": calendar[a:e+1],
                 "post_effective_20d": calendar[e+1:e+21]}
        for phase, dates in spans.items():
            actual = window_return(ret, ew, row.symbol, dates)
            if not np.isfinite(actual):
                continue
            anchor = dates[0]
            lv = liq.at[anchor, row.symbol]
            if not np.isfinite(lv) or lv <= 0:
                continue
            # Random symbol AND date, same year and same window length.
            year_dates = calendar[(calendar.year == anchor.year)]
            controls = []
            for _ in range(20):
                if len(year_dates) <= len(dates) + 1:
                    break
                start = int(RNG.integers(0, len(year_dates)-len(dates)))
                cd = year_dates[start:start+len(dates)]
                eligible = liq.loc[cd[0]].dropna()
                eligible = eligible[(eligible > 0) & (np.abs(np.log(eligible/lv)) <= np.log(2))]
                eligible = eligible.index.difference([row.symbol])
                if len(eligible):
                    sym = str(RNG.choice(eligible))
                    v = window_return(ret, ew, sym, cd)
                    if np.isfinite(v):
                        controls.append(v)
            records.append(dict(index=row.index, action=row.action, phase=phase, symbol=row.symbol,
                                announce=row.announce_date.date(), effective=row.effective_date.date(),
                                excess=actual, placebo=float(np.mean(controls)) if controls else np.nan,
                                controls=len(controls)))
    out = pd.DataFrame(records)
    if out.empty:
        print("No eligible events")
        return
    print("\nIndex | action | phase | n | episodes | mean% | median% | win% | worst% | placebo_mean% | net_mean%")
    for (idx, action, phase), g in out.groupby(["index", "action", "phase"], sort=True):
        s = stats(g.excess)
        episodes = g[["announce", "effective"]].drop_duplicates().shape[0]
        print(f"{idx} | {action} | {phase} | {s['n']} | {episodes} | {fmt(s['mean'])} | "
              f"{fmt(s['median'])} | {fmt(s['hit'])} | {fmt(s['worst'])} | "
              f"{fmt(g.placebo.mean())} | {fmt(s['mean']-COST)}")
    print("\nPooled notice-level results: equal-weight each independent index notice")
    for (action, phase), g in out.groupby(["action", "phase"]):
        episodes = g.groupby(["index", "announce", "effective"]).excess.mean()
        s = stats(episodes)
        print(f"{action} {phase}: episodes={s['n']} mean={fmt(s['mean'])}% median={fmt(s['median'])}% "
              f"hit={fmt(s['hit'])}% worst={fmt(s['worst'])}%")
    print("\nEvent rows and matched control means (percentage points):")
    print("index,action,phase,symbol,announce,effective,excess_pct,placebo_pct,control_draws")
    for r in out.itertuples(index=False):
        print(f"{r.index},{r.action},{r.phase},{r.symbol},{r.announce},{r.effective},"
              f"{fmt(r.excess)},{fmt(r.placebo)},{r.controls}")
    print("\nNeutralized corporate-action-like raw returns:")
    print(p["actions"].to_csv(index=False), end="")


if __name__ == "__main__":
    main()
