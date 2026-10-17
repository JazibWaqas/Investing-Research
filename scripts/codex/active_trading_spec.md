# Active trading rules frozen before first run, 18 October 2026

The starting capital is Rs50,000 once per window. All systems use the same
start-date universe: symbols in the adjusted panel with at least 40 observations
in the preceding 60 sessions and median raw close times raw volume of at least
Rs5m. The universe remains fixed within each window. For dates from 2019 onward,
also require membership in the latest available KMI All Share list as of the
window start. The 2016 and 2018 windows have no contemporary KMI list, so they
use the liquid panel as a broader proxy. Historical KMI lists are retrospectively
derived and this limitation must be disclosed.

Signals use only the close of the session before the first trading session of
each month. Orders fill at that first session's adjusted close, so the signal
has a full session of delay. Existing holdings stay until rebalanced. Equal
weights across up to three picks; empty screens hold cash. Signals never use
forward returns. Names must have a positive adjusted price and a preceding
20-session median raw traded value of at least Rs5m at each rebalance.

1. **MOM63**: top three 63-session adjusted price returns, requiring positive return.
2. **MOM252**: top three 252-session adjusted price returns, requiring positive return.
3. **HIGH52**: top three names within 2% of their preceding 252-session high, ranked by 63-session return, requiring that return positive.
4. **DIP200**: price above 200-session moving average, 21-session return below -5%; rank by most negative 21-session return.
5. **SECTOR63**: rank sectors by median 63-session return among eligible names; buy the strongest 63-session-return name from each of the top three sectors, requiring positive sector and stock return.
6. **VOL20**: 20-session mean raw volume at least twice its preceding 120-session mean, 21-session price return positive; rank by the volume ratio, take three.
7. **EPS_YOY**: quarterly EPS with an announcement timestamp at or before the signal close, within the last 60 calendar days. Compare with the same fiscal quarter a year earlier, require both values and positive year-on-year EPS change; rank by change, take three. Its source does not certify consolidated EPS, so this is a provisional screen.

The first six signals use fully adjusted close for returns. Raw close and
volume determine tradability and volume spikes. Costs are 0.25% at entry and
exit (0.5% round trip). Add 0.25% at each side when the preceding 20-session
median traded value is below Rs20m. This convention charges per position change.
The placebo consists of 200 seeded paths with three uniformly drawn eligible
names at each monthly rebalance, charged identically. The oracle chooses the
single highest *subsequent* monthly return, including costs, and is explicitly
untradable. Price-only individual stock outcomes are compared with the two
total-return indices, with the dividend mismatch disclosed.
