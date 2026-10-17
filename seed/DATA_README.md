# Seed data (collected 16 Oct 2026 by the orchestrator)

Re-download fresher data where you can. The PSX API should work from this machine.

## data/prices/  (528 CSVs)
- One file per ticker: `date,open,high,low,close,volume`, daily, from Oct 2016 (psxdata caps at about 10 years) to 16 Oct 2026.
- Universe: every ticker in ALLSHR as of 16 Oct 2026, so delisted names are **missing** (survivorship bias).
- **Raw, unadjusted.** `scripts/load_all.py` applies a crude fix (moves beyond the ±10.5% circuit treated as corporate actions). Replace it with proper bonus/split adjustment if possible.

## data/fundamentals/
- `sa_ratios.csv`: StockAnalysis fiscal year (and TTM) P/E, forward P/E, P/B, ROE, dividend yield and payout for 115 liquid KMI names, FY2021 to FY2026. Don't use `peForward` historically.
- `universe_scored.csv`: the current ranking of 92 liquid KMI names on 45% value (E/P + DY), 30% ROE and 25% 3 year EPS CAGR.
- `screener_20261016.csv`: PSX screener snapshot (750 symbols; `listed_in` shows KMIALLSHR membership; symbols with `XD` are ex dividend; `market_cap` is empty).

## data/macro/
- `tbill6m.csv`: monthly 6M T-bill cutoff yield, 1998 to Oct 2026, from SBP tb.xlsx.
- `pr.csv`: SBP policy rate changes, May 2015 to Apr 2026 (holds not listed; pre 2015 missing).
- `cpi_yoy_2015_2026.csv`: monthly national CPI YoY (derived from UN index to Aug 2026; Sep 2026 is official PBS, 10.3%).
- `imf_events.csv`: IMF staff level agreements and board approvals, 2019 to 2026 (incomplete; stalls missing).
- `sector_monthly_ret.csv`, `ew_mkt_ret.csv`: equal weight monthly sector and market returns from the original 60 ticker set.

## scripts/
- `load_all.py`: loads prices, applies the corporate action fix, builds a return index
- `valtest.py`: value factor test (the 28 pts/yr result)
- `ops.py`: operator footprint tests (accumulation, breakout, pump)
- `mom.py`: stock momentum event study
- `macro_ev.py`: IMF and MPC event studies
- `sect.py`: regime vs sector excess returns
- `sa_parse.py`, `universe.py`: StockAnalysis parsing and universe scoring
- `fetch_all.py`: bulk price download via psxdata

## Not included (download from the user's Drive if needed)
- `corporate_actions.csv`: dividends, bonuses and splits for MEBL, FFC, HUBC, OGDC, SYS and EPCL, 2021 to 2026.
- Prospective Forecast Register: frozen earnings forecasts for EFERT, MEBL, OGDC and FCCL.
