# PSX index series: total return vs price return

Sources: PSX brochures downloaded 2026-10-17 to `data/raw/macro/` (text extracted with pdfplumber to the matching `.txt`), linked from https://www.psx.com.pk/psx/product-and-services/indices. Series fetched from the PSX data portal via `scripts/psx_api.py` `historical_full(sym)` (raw copies `data/raw/macro/psx_<SYM>_hist.csv`).

## Table

| Series (csv) | Return type | Base date / value | Weighting | Re-composition |
|---|---|---|---|---|
| KSE100 (`kse100.csv`) | Total return (cash dividends adjusted) | Nov 1991 / 1,000 | Free-float market cap, top 100 (one per sector for 34 sectors, rest by cap) | Semi-annual: data Feb-end and Aug-end, effective 1st working day of April and October |
| KSE100PR (`kse100pr.csv`) | Price return (gross cash dividends not adjusted) | 1 Apr 2009 / 6,931 | Same as KSE100 | Same as KSE100 |
| ALLSHR (`allshr.csv`) | Total return (same methodology as KSE100, per KSE100 brochure) | not stated in the brochures read | All listed companies except open-end funds | not stated |
| KSE30 (`kse30.csv`) | Price return (see below; this contradicts the working assumption that it is total return) | Jun 2005 / 10,000 | Free-float market cap, 30 companies, rank 50% free-float cap / 50% impact cost | Semi-annual: 30 Jun to 15 Sep, 31 Dec to 15 Mar |
| KMI30 (`kmi30.csv`) | Total return | 30 Jun 2008 / 15,000 | Free-float cap, constituents capped at 12% of Islamic index cap (surplus redistributed) | Semi-annual: 30 Jun to 15 Nov, 31 Dec to 15 May |
| KMIALLSHR (`kmiallshr.csv`) | Total return (cash dividend adjusted via divisor) | 31 Dec 2014 / 15,000 | Brochure says full market cap (total shares x price); all Shariah-compliant stocks | Semi-annual: 31 Dec to 15 May, 30 Jun to 15 Nov |
| PSXDIV20 (`psxdiv20.csv`) | Total return | 29 Oct 2020 / 10,000 | Trailing-12-month dividend yield, max 12% per name | Semi-annual: last working day of Apr and Oct, effective first working day of Jun and Dec |

Other portal index series saved with the same layout (return type not checked in a brochure unless stated): `bkti, ogti, jsmfi, jsgbkti, aci, upp9, nitpgi, nbppgi, mznpi, mii30` (thematic/ETF-tracking indices).

## Quotes

- KSE100 brochure: "The KSE100 index is a total return index i.e. dividend, bonus, rights and any other corporate actions are adjusted in the constituents of the index, whereas, the KSE100PR Index is a price return index where gross cash dividends are not adjusted in the constituents of the index." Also: "The price variant only reflects the capital appreciation of index constituents and does not account for the impact of reinvestment of gross cash dividends." Base: "The base period of KSE100PR index is April 01, 2009 and the base value is 6,931 index points." "The Price Return version of the index began from 01 April 2009 (back dated)."
- KSE-30 brochure, section 10.1 Adjustment for Cash Dividend: "No adjustment of cash dividend will be made contrary to the practice applicable in KSE-100 Index." So KSE-30 is a price index. (The "total return index" sentence near the top of that PDF is the KSE-100 description, not KSE-30's.) Empirical support: KSE30/KSE100 ratio falls every year, 0.541 (end 2016) to 0.296 (Oct 2026).
- KMI30 brochure: "KMI 30 Index is a total return index; therefore, adjustment of cash dividend shall be made."
- All Shares Islamic brochure (3 Jun 2026), 1.7.1: the divisor is adjusted for cash dividend (ex-dividend price = market price minus dividend); maintenance covers "cash dividends, additions and deletions, share changes, stock splits, stock dividends".
- KSE-100 brochure on All Share: "The same methodology is applicable in the case of All Share Index, which includes all the listed companies, (except Open-End Mutual Funds)."
- PSXDIV20 brochure: "PSXDIV20 Index is a total-return Index; therefore, adjustment for cash dividend shall be made."

## Fetching

- `/symbols` does not list indices. Index codes work as symbols in `historical_full` and `eod`. `/indices/{code}` returns only the constituents table (HTML), not prices.
- KSE100PR is served by the portal but only from 2020-04-01 (1,621 rows), not from 2009 as the brochure implies. Earlier history not found; investing.com and the PSX historical-data page were not tried. `eod` only gives 5 years, so `historical_full` is the source.
- Not served (empty): KMIALL, ALLSHRPR, KSE30PR, KMI30PR.

## Files written (data/macro, columns date,value,open,high,low,close,volume; value = close)

kse100pr 2020-04-01 to 2026-10-16 (1,621); psxdiv20 2022-09-05 (1,023); bkti 2021-10-25 (856); ogti 2021-10-25 (856); jsmfi 2022-01-07 (1,183); jsgbkti 2023-09-11 (770); aci 2022-01-17 (1,177); upp9 2020-03-17 (1,632); nitpgi 2020-01-31 (1,663); nbppgi 2020-10-06 (1,495); mznpi 2020-10-05 (1,496); mii30 2024-03-11 (644). All end 2026-10-16. Already present: kse100, kse30, kmi30, kmiallshr, allshr (2016-10-17 or 2016-10-24 to 2026-10-16).

## Annualised returns, 2017-01-02 to 2026-10-16 (or from first date where the series starts later)

| Series | Type | From | CAGR |
|---|---|---|---|
| KSE100 | TR | 2017-01-02 | 13.49% |
| ALLSHR | TR | 2017-01-02 | 12.05% |
| KMI30 | TR | 2017-01-02 | 11.59% |
| KMIALLSHR | TR | 2017-01-02 | 11.37% |
| KSE30 | PR | 2017-01-02 | 6.70% |
| KSE100PR | PR | 2020-04-01 | 22.68% (KSE100 TR over the same window: 30.3%) |
| PSXDIV20 | TR | 2022-09-05 | 51.42% |

## Implied KSE100 dividend yield (KSE100 TR growth / KSE100PR growth - 1, calendar year, year-end to year-end)

| Year | Implied yield |
|---|---|
| 2020 (1 Apr to 31 Dec only) | 3.39% |
| 2021 | 7.13% |
| 2022 | 5.58% |
| 2023 | 6.97% |
| 2024 | 5.04% |
| 2025 | 7.61% |
| 2026 (to 16 Oct) | 4.77% |

Whole window 2020-04-01 to 2026-10-16: 6.19% a year. Pre-2020 not computable (no KSE100PR). Plain subtraction of the two annual returns overstates the yield in the high-return years (2023 to 2025, 8.9 to 10.7 points) because of compounding; the ratio above is the proper measure.
