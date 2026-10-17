"""Independent fixed-capital PSX rotation study. See active_trading_spec.md."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "tests" / "out" / "active_trading_codex.txt"
WINDOWS = ["2016-12-30", "2018-10-01", "2020-10-01", "2022-10-01", "2024-10-01"]
SYSTEMS = ["MOM63", "MOM252", "HIGH52", "DIP200", "SECTOR63", "VOL20", "EPS_YOY"]


def load():
    price = pd.read_parquet(DATA / "panel_close_adj.parquet").sort_index()
    volume = pd.read_parquet(DATA / "panel_volume.parquet").reindex_like(price)
    raw_close = pd.DataFrame(index=price.index, columns=price.columns, dtype=float)
    for sym in price.columns:
        path = DATA / "prices_raw" / f"{sym}.csv"
        if path.exists():
            raw = pd.read_csv(path, usecols=["date", "close"])
            raw.index = pd.to_datetime(raw.pop("date"))
            raw_close[sym] = raw["close"].reindex(price.index)
    traded = raw_close * volume
    sector = pd.read_csv(DATA / "symbols.csv").drop_duplicates("symbol").set_index("symbol")["sectorName"]
    eps = pd.read_csv(DATA / "fundamentals" / "quarterly_eps.csv")
    eps["fiscal_quarter_end"] = pd.to_datetime(eps["fiscal_quarter_end"])
    eps["first_tradable_date"] = pd.to_datetime(eps["first_tradable_date"], errors="coerce")
    eps = eps.sort_values(["symbol", "fiscal_quarter_end"])
    eps["eps_prior"] = eps.groupby("symbol")["eps_basic"].shift(4)
    eps["prior_end"] = eps.groupby("symbol")["fiscal_quarter_end"].shift(4)
    eps = eps[(eps["fiscal_quarter_end"] - eps["prior_end"]).dt.days.between(360, 370)]
    eps["eps_change"] = eps["eps_basic"] - eps["eps_prior"]
    eps = eps.dropna(subset=["first_tradable_date", "eps_change"])
    indices = {}
    for name in ["kmiallshr", "kse100"]:
        x = pd.read_csv(DATA / "macro" / f"{name}.csv", usecols=["date", "value"])
        indices[name] = x.set_index(pd.to_datetime(x["date"]))["value"].sort_index()
    return price, volume, traded, sector, eps, indices


def membership(start):
    files = sorted((DATA / "index_members").glob("KMI_ALL_derived_*.csv"))
    available = [(p.stem.split("_")[-1], p) for p in files if p.stem.split("_")[-1] <= start[:10]]
    if not available:
        return None, "broad_liquid_proxy"
    stamp, path = available[-1]
    return set(pd.read_csv(path)["symbol"].astype(str)), f"derived_KMI_{stamp}"


def row_signal(system, k, universe, price, volume, traded, sector, eps):
    """Signals at k, execution at k+1 or later. No future series read."""
    p = price.iloc[k]
    tv = traded.iloc[max(0, k-19):k+1].median()
    eligible = pd.Index(universe).intersection(price.columns)
    eligible = eligible[(p.reindex(eligible) > 0).fillna(False) & (tv.reindex(eligible) >= 5e6).fillna(False)]
    if len(eligible) == 0:
        return []
    r21 = p / price.iloc[max(0, k-21)] - 1 if k >= 21 else p * np.nan
    r63 = p / price.iloc[max(0, k-63)] - 1 if k >= 63 else p * np.nan
    r252 = p / price.iloc[max(0, k-252)] - 1 if k >= 252 else p * np.nan
    if system == "MOM63":
        score = r63.reindex(eligible).where(lambda x: x > 0)
    elif system == "MOM252":
        score = r252.reindex(eligible).where(lambda x: x > 0)
    elif system == "HIGH52":
        high = price.iloc[k-251:k+1].max() if k >= 251 else p * np.nan
        score = r63.reindex(eligible).where((p / high).reindex(eligible) >= .98).where(lambda x: x > 0)
    elif system == "DIP200":
        ma = price.iloc[k-199:k+1].mean() if k >= 199 else p * np.nan
        score = (-r21).reindex(eligible).where((p > ma).reindex(eligible) & (r21 < -.05).reindex(eligible))
    elif system == "SECTOR63":
        frame = pd.DataFrame({"ret": r63.reindex(eligible), "sector": sector.reindex(eligible)})
        frame = frame[(frame.ret > 0) & frame.sector.notna()]
        ranked = frame.groupby("sector").ret.median().sort_values(ascending=False).head(3).index
        return [frame[frame.sector == s].ret.idxmax() for s in ranked]
    elif system == "VOL20":
        if k < 140:
            return []
        recent = volume.iloc[k-19:k+1].mean()
        earlier = volume.iloc[k-139:k-19].mean()
        score = (recent / earlier).reindex(eligible).where(lambda x: x >= 2).where((r21 > 0).reindex(eligible))
    elif system == "EPS_YOY":
        date = price.index[k]
        events = eps[(eps.first_tradable_date <= date) & (eps.first_tradable_date >= date - pd.Timedelta(days=60))]
        events = events.sort_values("first_tradable_date").drop_duplicates("symbol", keep="last")
        score = events.set_index("symbol").eps_change.reindex(eligible).where(lambda x: x > 0)
    else:
        raise ValueError(system)
    return score.replace([np.inf, -np.inf], np.nan).dropna().sort_values(ascending=False).head(3).index.tolist()


def simulate(price, px, tv20, col, schedule, start_i, end_i):
    """Daily marked NAV; weights drift until a scheduled rebalance."""
    nav = 50000.0
    weights = {}
    entries = {}
    trades = []
    curve = [nav]
    changes = 0
    for i in range(start_i, end_i + 1):
        if i > start_i:
            invested = {}
            for s, w in weights.items():
                ratio = px[i, col[s]] / px[i-1, col[s]]
                if np.isfinite(ratio) and ratio > 0:
                    invested[s] = w * ratio
            total = sum(invested.values()) + max(0, 1-sum(weights.values()))
            nav *= total
            weights = {s: v / total for s, v in invested.items()}
        if i in schedule:
            picks = schedule[i]
            target = {s: 1 / len(picks) for s in picks} if picks else {}
            signal_tv = tv20[i-1]
            charge = 0.0
            for s in set(weights) | set(target):
                old, new = weights.get(s, 0), target.get(s, 0)
                if abs(old-new) < 1e-9:
                    continue
                side_cost = .0025 + (.0025 if signal_tv[col[s]] < 20e6 else 0)
                charge += abs(new-old) * side_cost
                if old == 0 and new > 0:
                    entries[s] = (float(px[i, col[s]]), side_cost)
                if old > 0 and new == 0 and s in entries:
                    entry_price, entry_cost = entries.pop(s)
                    trades.append(float(px[i, col[s]]) / entry_price * (1-entry_cost) * (1-side_cost) - 1)
                changes += 1
            nav *= 1-charge
            weights = target
        curve.append(nav)
    signal_tv = tv20[end_i]
    closing_cost = sum(w*(.0025 + (.0025 if signal_tv[col[s]] < 20e6 else 0)) for s,w in weights.items())
    nav *= 1-closing_cost
    for s in weights:
        if s in entries:
            ep, ec = entries[s]
            xc = .0025 + (.0025 if signal_tv[col[s]] < 20e6 else 0)
            trades.append(float(px[end_i, col[s]])/ep*(1-ec)*(1-xc)-1)
    curve[-1] = nav
    a = np.asarray(curve)
    dd = float(np.min(a / np.maximum.accumulate(a) - 1))
    years = (price.index[end_i] - price.index[start_i]).days / 365.25
    return {"multiple": nav/50000, "rupees": nav, "cagr": (nav/50000)**(1/years)-1,
            "max_drawdown": dd, "trades": len(trades), "hit_rate": float(np.mean(np.asarray(trades)>0)) if trades else None,
            "median_trade": float(np.median(trades)) if trades else None, "changes": changes}


def run():
    price, volume, traded, sector, eps, indices = load()
    # A non-trading day for one symbol has no realizable zero-price exit.
    # Carry its last observed close until another print appears.
    px = price.ffill().to_numpy(dtype=float)
    tv20 = traded.rolling(20, min_periods=1).median().to_numpy(dtype=float)
    col = {s: i for i, s in enumerate(price.columns)}
    rng = np.random.default_rng(104729)
    output = {"method": "scripts/codex/active_trading_spec.md", "windows": {}}
    for start in WINDOWS:
        target = pd.Timestamp("2026-10-16") if start == "2024-10-01" else pd.Timestamp(start) + pd.DateOffset(years=2) - pd.Timedelta(days=1)
        start_i = int(price.index.searchsorted(pd.Timestamp(start)))
        end_i = int(price.index.searchsorted(target, side="right")-1)
        start_dt, end_dt = price.index[start_i], price.index[end_i]
        members, membership_note = membership(start)
        past = traded.iloc[max(0, start_i-60):start_i]
        observations = past.notna().sum()
        liquid = set(past.median()[(past.median() >= 5e6) & (observations >= 40)].index)
        universe = sorted(liquid if members is None else liquid & members)
        universe = [s for s in universe if pd.notna(price.iloc[start_i][s]) and price.iloc[start_i][s] > 0]
        months = pd.Series(range(start_i, end_i), index=price.index[start_i:end_i]).groupby(price.index[start_i:end_i].to_period("M")).first().tolist()
        if months[0] != start_i:
            months.insert(0, start_i)
        schedules = {s: {} for s in SYSTEMS}
        eligible_by_month = {}
        for i in months:
            k = i-1
            if k < 0:
                continue
            tv = traded.iloc[max(0,k-19):k+1].median()
            eligible_by_month[i] = [s for s in universe if tv.get(s, 0) >= 5e6 and pd.notna(price.iloc[i][s]) and price.iloc[i][s]>0]
            for system in SYSTEMS:
                picks = row_signal(system, k, universe, price, volume, traded, sector, eps)
                schedules[system][i] = [s for s in picks if pd.notna(price.iloc[i][s]) and price.iloc[i][s] > 0]
        systems = {s: simulate(price, px, tv20, col, schedules[s], start_i, end_i) for s in SYSTEMS}
        random_values = []
        for _ in range(200):
            schedule = {i: rng.choice(pool, size=min(3,len(pool)), replace=False).tolist() if pool else [] for i,pool in eligible_by_month.items()}
            random_values.append(simulate(price, px, tv20, col, schedule, start_i, end_i)["multiple"])
        for system in SYSTEMS:
            systems[system]["random_percentile"] = float(np.mean(np.asarray(random_values) <= systems[system]["multiple"])*100)
        # The hindsight path sees next month's return and thus cannot be traded.
        oracle_schedule = {}
        for mi, i in enumerate(months):
            stop = months[mi+1] if mi+1 < len(months) else end_i
            pool = eligible_by_month.get(i, [])
            if pool:
                future = (price.iloc[stop][pool]/price.iloc[i][pool]).replace([np.inf,-np.inf], np.nan).dropna()
                oracle_schedule[i] = [future.idxmax()] if not future.empty else []
        oracle = simulate(price, px, tv20, col, oracle_schedule, start_i, end_i)
        bh = (price.iloc[end_i][universe] / price.iloc[start_i][universe]).replace([np.inf,-np.inf],np.nan).dropna()
        bh = bh[bh > 0]
        # One entry and exit, with liquidity-dependent costs.
        tv_start = traded.iloc[max(0,start_i-20):start_i].median()
        tv_end = traded.iloc[max(0,end_i-19):end_i+1].median()
        bh = bh * (1-.0025-(tv_start.reindex(bh.index)<20e6).astype(float)*.0025) * (1-.0025-(tv_end.reindex(bh.index)<20e6).astype(float)*.0025)
        winners = [{"symbol": s, "sector": str(sector.get(s, "unknown")), "multiple": float(v)} for s,v in bh.sort_values(ascending=False).head(10).items()]
        benchmarks = {}
        for name, series in indices.items():
            a = series.loc[:start_dt].iloc[-1] if len(series.loc[:start_dt]) else np.nan
            b = series.loc[:end_dt].iloc[-1]
            benchmarks[name] = float(b/a)
        output["windows"][start] = {"start": str(start_dt.date()), "end": str(end_dt.date()), "membership": membership_note,
             "universe_n": len(universe), "buy_hold": {"n": len(bh), "mean": float(bh.mean()), "median": float(bh.median()),
                 "win_rate": float((bh>1).mean()), "worst": float(bh.min()), "share_2x": float((bh>=2).mean()),
                 "share_3x": float((bh>=3).mean()), "share_5x": float((bh>=5).mean()), "top10": winners},
             "oracle": oracle, "oracle_picks": {str(price.index[i].date()): oracle_schedule.get(i, []) for i in months},
             "system_picks": {s: {str(price.index[i].date()): schedules[s].get(i, []) for i in months} for s in SYSTEMS},
             "benchmarks": benchmarks, "random": {"n": 200, "mean": float(np.mean(random_values)),
                 "median": float(np.median(random_values)), "worst": float(np.min(random_values)),
                 "win_rate": float(np.mean(np.asarray(random_values)>1)), "p10": float(np.percentile(random_values,10)),
                 "p90": float(np.percentile(random_values,90))}, "systems": systems}
        print(f"{start}: n={len(universe)}, oracle={oracle['multiple']:.2f}, best={max(v['multiple'] for v in systems.values()):.2f}", flush=True)
    rank = {}
    for s in SYSTEMS:
        multiples = np.array([w["systems"][s]["multiple"] for w in output["windows"].values()])
        percentiles = np.array([w["systems"][s]["random_percentile"] for w in output["windows"].values()])
        rank[s] = {"median_multiple": float(np.median(multiples)), "worst_multiple": float(np.min(multiples)),
                   "windows_over_random_median": int(np.sum(percentiles > 50)), "median_random_percentile": float(np.median(percentiles))}
    output["stability"] = dict(sorted(rank.items(), key=lambda kv: (-kv[1]["windows_over_random_median"], -kv[1]["median_random_percentile"])))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2, allow_nan=False), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    run()
