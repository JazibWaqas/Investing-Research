# Intraday trade archive

Written by `scripts\collect_intraday.py` from the PSX portal endpoint `GET /timeseries/int/{SYM}` (same X-Req-Id header as the EOD series, see `scripts\psx_api.py`).

- **Starts on the first run date.** Nothing before that exists; the portal does not keep past sessions here (the first run, on Sun 18 Oct 2026, returned the Fri 16 Oct session, so the archive begins with 16 Oct).
- **The portal serves only the current session.** A run after the close saves that session's trades; a missed day is lost for good. Run it after the close on every trading day (RUNBOOK.md step 1).
- **Session date:** the latest PKT trading date in the run's responses. Quiet names can return older trades; those rows are dropped, so a name with no trade that session gets no file.
- **Layout:** `data\intraday\{YYYY-MM-DD}\{SYM}.csv` where the date is the PKT session date of the trades. Columns: `ts,price,volume`. `ts` is unix seconds (UTC; add 5 hours for PKT), `price` is the trade price in Rs, `volume` is shares. Rows are in time order.
- **Universe:** the KMI All Share names in `data\kmi_allshare_2026-06-05.csv`, plus any `data\prices_raw` name whose median close times volume over its last 60 sessions exceeds Rs5m (a proxy for traded value, which the portal does not give).
- **Idempotent:** a symbol already saved for that session is not rewritten, so reruns are safe. Every run still makes one request per symbol (about 5 minutes), because the session date is only known from the responses.
- Portal response (verified 18 Oct 2026): JSON `{"status": 1, "message": "", "data": [[ts, price, volume], ...]}`, newest first. Three fields per row.
