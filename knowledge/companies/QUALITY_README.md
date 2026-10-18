# Quality scores

Dated 2026-10-18. `quality_scores.csv` ranks 20 PSX-listed companies by overall score, highest first.

## What the scores mean

The four component scores are whole numbers (observed 2 to 4, higher is better):

- **promises_vs_delivery**: how far past guidance, timelines and targets were met.
- **capital_allocation**: how well profits and cash are used, including payouts, buybacks, acquisitions and investments.
- **minority_treatment**: how fairly non-controlling holders are treated, including related-party dealings and dilution.
- **disclosure_quality**: how complete, timely and consistent filings and briefings are.

`overall` is the sum of the four (maximum 16). `growth_engine` is a text view of what could drive growth and what would break it. `key_people` summarises management and control. `red_flags` lists specific concerns joined by " | ".

## Judgments, not ratings

These are judgments written by a language model from public records: annual reports, PSX filings, briefing slides, press and market data. Items marked unverified were not confirmed. They are not audited ratings and not investment advice.

## How to update

1. Add the new evidence to the company card in `knowledge/companies/` (`SYMBOL_quality.md`).
2. Edit that company's row in `quality_scores.csv`: change the scores, keep text fields quoted, and set `overall` to the sum.
3. Re-sort by `overall`, highest first.
4. Change the date at the top of this file.
