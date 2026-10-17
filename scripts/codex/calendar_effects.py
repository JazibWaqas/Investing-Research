"""Calendar tests on liquid equal-weight PSX and KSE100, 2017-2026."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prices_codex import ROOT, load_prices, compound, stats

RNG = np.random.default_rng(55104)
BUDGET = {2017:"2017-05-26", 2018:"2018-04-27", 2019:"2019-06-11",
          2020:"2020-06-12", 2021:"2021-06-11", 2022:"2022-06-10",
          2023:"2023-06-09", 2024:"2024-06-12", 2025:"2025-06-10",
          2026:"2026-06-12"}
RAMADAN = {2017:"2017-05-28", 2018:"2018-05-17", 2019:"2019-05-07",
           2020:"2020-04-25", 2021:"2021-04-14", 2022:"2022-04-04",
           2023:"2023-03-23", 2024:"2024-03-12", 2025:"2025-03-02",
           2026:"2026-02-19"}


def pct(v):
    return "NA" if not np.isfinite(v) else f"{100*v:.2f}"


def add(rows, effect, episode, dates, series, calendar):
    dates = pd.DatetimeIndex(dates)
    if not len(dates) or dates.min() < pd.Timestamp("2017-01-01") or dates.max() > pd.Timestamp("2026-10-16"):
        return
    for name, s in series.items():
        x = s.reindex(dates)
        if x.isna().any():
            continue
        year_days = calendar[calendar.year == dates[0].year]
        if len(year_days) < len(dates):
            continue
        placebo = []
        for _ in range(100):
            start = int(RNG.integers(0, len(year_days)-len(dates)+1))
            v = s.reindex(year_days[start:start+len(dates)]).dropna()
            if len(v) == len(dates):
                placebo.append(compound(v))
        rows.append(dict(effect=effect, episode=episode, year=dates[0].year,
                         market=name, days=len(dates), ret=compound(x),
                         placebo=float(np.mean(placebo)) if placebo else np.nan))


def main():
    p = load_prices()
    series = {"EW liquid":p["ew"], "KSE100":p["kse100"]}
    calendar = p["kse100"].loc["2017-01-01":"2026-10-16"].dropna().index
    rows = []
    for year in range(2017, 2027):
        yd = calendar[calendar.year == year]
        for month in range(1, 13):
            md = yd[yd.month == month]
            if len(md) and md[-1].month == month and (year < 2026 or month <= 9):
                add(rows, f"month_{month:02d}", f"{year}-{month:02d}", md, series, calendar)
        bd = pd.Timestamp(BUDGET[year])
        pos = calendar.searchsorted(bd, side="left")
        if pos >= 5 and pos + 6 <= len(calendar):
            add(rows, "budget_pre_5", str(year), calendar[pos-5:pos], series, calendar)
            # Tradeable after the announcement date, excluding its same-day return.
            post_start = calendar.searchsorted(bd, side="right")
            add(rows, "budget_post_5", str(year), calendar[post_start:post_start+5], series, calendar)
        rd = pd.Timestamp(RAMADAN[year])
        # Fixed 30 calendar days from local first-fast date, end is approximate.
        ram = calendar[(calendar >= rd) & (calendar < rd + pd.Timedelta(days=30))]
        add(rows, "ramadan_30_calendar_days", str(year), ram, series, calendar)
        for quarter, (start, end) in enumerate([(f"{year}-01-20",f"{year}-02-28"),
                                                  (f"{year}-04-20",f"{year}-05-31"),
                                                  (f"{year}-07-20",f"{year}-08-31"),
                                                  (f"{year}-10-20",f"{year}-11-30")], 1):
            if pd.Timestamp(end) > pd.Timestamp("2026-10-16"):
                continue
            season = calendar[(calendar >= start) & (calendar <= end)]
            add(rows, "results_season", f"{year}Q{quarter}", season, series, calendar)
        months = sorted(set(yd.to_period("M")))
        for period in months[1:]:
            prev = calendar[calendar.to_period("M") == period-1]
            curr = calendar[calendar.to_period("M") == period]
            if len(prev) and len(curr) >= 3:
                add(rows, "turn_of_month_4", str(period), prev[-1:].append(curr[:3]), series, calendar)
    decisions = pd.read_csv(ROOT / "data/macro/policy_rate_decisions.csv", parse_dates=["date"])
    decisions = decisions[(decisions.date >= "2017-01-01") & (decisions.date <= "2026-10-16")]
    for date in decisions.date.drop_duplicates().sort_values():
        pre = calendar.searchsorted(date, side="left")
        post = calendar.searchsorted(date, side="right")
        if pre >= 10 and post + 10 <= len(calendar):
            add(rows, "mpc_pre_10", str(date.date()), calendar[pre-10:pre], series, calendar)
            add(rows, "mpc_post_10", str(date.date()), calendar[post:post+10], series, calendar)
    out = pd.DataFrame(rows)
    print(f"price_symbols={p['ret'].shape[1]} neutralized_gaps={len(p['actions'])} "
          f"calendar_days={len(calendar)} mpc_dates={decisions.date.nunique()}")
    print("Budget dates (verified where cited in report):", ", ".join(BUDGET.values()))
    print("Ramadan first-fast dates:", ", ".join(RAMADAN.values()))
    print("\neffect | market | n episodes | n years | mean% | median% | hit% | best% | worst% | placebo_mean% | cost_adj_mean%")
    for (effect, market), g in out.groupby(["effect", "market"], sort=True):
        s = stats(g.ret)
        print(f"{effect} | {market} | {s['n']} | {g.year.nunique()} | {pct(s['mean'])} | "
              f"{pct(s['median'])} | {pct(s['hit'])} | {pct(s['best'])} | {pct(s['worst'])} | "
              f"{pct(g.placebo.mean())} | {pct(s['mean']-.005)}")
    print("\nMPC independent 20-trading-day clusters:")
    mdates = pd.DatetimeIndex(decisions.date.drop_duplicates().sort_values())
    groups = []
    for d in mdates:
        if not groups or (d-groups[-1][-1]).days > 28:
            groups.append([d])
        else:
            groups[-1].append(d)
    print(f"{len(groups)} clusters from {len(mdates)} MPC announcements")
    print("\nPer-episode raw returns:")
    print("effect,episode,year,market,trading_days,return_pct,placebo_mean_pct")
    for r in out.itertuples(index=False):
        print(f"{r.effect},{r.episode},{r.year},{r.market},{r.days},{pct(r.ret)},{pct(r.placebo)}")
    print("\nNeutralized corporate-action-like raw returns:")
    print(p["actions"].to_csv(index=False), end="")


if __name__ == "__main__":
    main()
