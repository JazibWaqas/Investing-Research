"""ledger.py: the system of record (ledger/) and the pages built from it.

    .venv\\Scripts\\python.exe -I -X utf8 scripts\\ledger.py build      # rebuild PICKS.md, the generated blocks in STATE.md and ledger/scorecard.md, ledger/book_daily.csv
    .venv\\Scripts\\python.exe -I -X utf8 scripts\\ledger.py check      # validate the tables; fail if a built page is stale
    .venv\\Scripts\\python.exe -I -X utf8 scripts\\ledger.py trade 2026-10-22 MEBL buy 23 548.50 --fees 30 --call C0043
    .venv\\Scripts\\python.exe -I -X utf8 scripts\\ledger.py deposit 2026-11-01 50000
    .venv\\Scripts\\python.exe -I -X utf8 scripts\\ledger.py score C0009 1 --note "standalone EPS 13.10, PSX doc id"
trade, deposit and score validate, refuse a bad row, and rebuild the pages.

Tables (append only; never edit or delete a row):
  calls.csv     every call and forecast, with odds. To change a view, add a row naming the old id in `supersedes`
                (supersede the open row that PICKS.md shows). For buy_if and watch rows the condition is the `event` text.
  scores.csv    outcomes: call_id, scored_at, outcome (1, 0, void, not_triggered), note.
  trades.csv    what Jazib actually bought and sold (he reports them in chat).
  deposits.csv  money in, when he reports it.
A call is open until it is scored or superseded. Built pages carry a "do not edit" note; change the tables and rebuild.
Prices are the repo's raw closes (data/prices_raw/); the book ignores dividends while the KMI All Share benchmark is total return.
"""
import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
L = ROOT / "ledger"
COLS = {
    "calls": ["id", "made_at", "made_by", "kind", "ticker", "action", "event", "event_date", "prediction", "probability",
              "price_at_call", "size_rs", "upside_rs", "downside_rs", "proves_wrong", "reasoning", "journal", "supersedes"],
    "scores": ["call_id", "scored_at", "outcome", "note"],
    "trades": ["date", "ticker", "side", "qty", "price", "fees", "call_id", "note"],
    "deposits": ["date", "amount", "note"],
}
KINDS = {"forecast", "call"}
ACTIONS = {"buy", "buy_if", "add", "hold", "trim", "sell", "watch", "pass", "paper", "forecast"}
OUTCOMES = {"1", "0", "void", "not_triggered"}


def load(name):
    p = L / f"{name}.csv"
    if not p.exists():
        return pd.DataFrame(columns=COLS[name])
    return pd.read_csv(p, dtype=str, keep_default_na=False)


def append(name, row):
    p = L / f"{name}.csv"
    new = not p.exists()
    with p.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS[name])
        if new:
            w.writeheader()
        w.writerow(row)


def status(calls, scores):
    scored = set(scores["call_id"])
    superseded = set(calls["supersedes"]) - {""}
    return calls["id"].map(lambda i: "scored" if i in scored else "superseded" if i in superseded else "open")


def close_series(sym):
    for folder in ("prices_raw", "prices_listed_missing", "prices_delisted"):
        p = ROOT / "data" / folder / f"{sym}.csv"
        if p.exists():
            d = pd.read_csv(p, usecols=["date", "close"], parse_dates=["date"])
            return d.set_index("date")["close"]
    return None


def book_daily(trades, deposits):
    """Daily value of the actual book against the same money put into the KMI All Share."""
    cols = ["date", "market_value", "cash", "book_value", "kmi_benchmark"]
    if trades.empty:
        return pd.DataFrame(columns=cols)
    t = trades.assign(date=pd.to_datetime(trades["date"]), qty=trades["qty"].astype(float),
                      price=trades["price"].astype(float), fees=pd.to_numeric(trades["fees"], errors="coerce").fillna(0))
    t["signed"] = t["qty"].where(t["side"] == "buy", -t["qty"])
    t["cash_out"] = (t["signed"] * t["price"]) + t["fees"]
    kmi = pd.read_csv(ROOT / "data/macro/kmiallshr.csv", usecols=["date", "close"], parse_dates=["date"]).set_index("date")["close"]
    start = t["date"].min()
    days = kmi[kmi.index >= start].index
    qty = t.pivot_table(index="date", columns="ticker", values="signed", aggfunc="sum").reindex(days, fill_value=0).fillna(0).cumsum()
    px = pd.DataFrame({s: close_series(s) for s in qty.columns}).reindex(days).ffill()
    mv = (qty * px).sum(axis=1)
    if deposits.empty:  # no deposits reported: each buy is funded from outside, each sale goes back out
        flows = t.groupby("date")["cash_out"].sum()
    else:
        flows = deposits.assign(date=pd.to_datetime(deposits["date"]), amount=deposits["amount"].astype(float)).groupby("date")["amount"].sum()
    flows = flows.reindex(days, fill_value=0)
    cash = flows.cumsum() - t.groupby("date")["cash_out"].sum().reindex(days, fill_value=0).cumsum()
    units = (flows / kmi.reindex(days)).cumsum()
    out = pd.DataFrame({"market_value": mv, "cash": cash, "book_value": mv + cash, "kmi_benchmark": units * kmi.reindex(days)})
    return out.round(0).reset_index(names="date").assign(date=lambda d: d["date"].dt.date.astype(str))[cols]


def short(s, n=110):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 3] + "..."


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows]
    return "\n".join(out)


def latest_letter():
    letters = sorted((ROOT / "journal").glob("*-picks-v*.md"), key=lambda p: (p.name[:10], int(re.search(r"v(\d+)", p.name).group(1))))
    return f"journal/{letters[-1].name}" if letters else "none yet"


def render_picks(calls, st, today):
    c = calls.assign(status=st)
    live = c[(c.status == "open") & (c.kind == "call") & (c.action != "paper")]
    fc = c[(c.status == "open") & (c.kind == "forecast")].sort_values("event_date")
    paper = c[(c.status == "open") & (c.action == "paper")]
    parts = [
        "# PICKS.md — the open calls (built from ledger/calls.csv by scripts/ledger.py; do not edit by hand)",
        "",
        f"Built {today}. Each call's reasoning is in the journal entry it links; the latest letter to Jazib is {latest_letter()}. "
        "To change a call, add a row to ledger/calls.csv that supersedes it, then run `scripts/ledger.py build`. "
        "Odds are the probability the call's prediction holds. Upside and downside are rupees on the suggested size.",
        "",
        "## Live calls",
        "",
        md_table(["id", "made", "ticker", "action", "the call", "odds that", "odds", "size Rs", "upside Rs", "downside Rs", "proves it wrong", "reasoning"],
                 [[r.id, r.made_at[:10], r.ticker, r.action, short(r.event, 110), short(r.prediction, 70), r.probability, r.size_rs, r.upside_rs, r.downside_rs,
                   short(r.proves_wrong, 90), r.journal] for r in live.itertuples()]) if len(live) else "None.",
        "",
        "## Open forecasts, soonest first",
        "",
        md_table(["id", "event date", "ticker", "event", "prediction", "odds"],
                 [[r.id, r.event_date, r.ticker, short(r.event, 60), short(r.prediction, 100), r.probability] for r in fc.itertuples()]) if len(fc) else "None.",
        "",
        "## Paper calls (never acted on; kept open so they are scored)",
        "",
        ", ".join(f"{r.id} {r.ticker}" for r in paper.itertuples()) or "None.",
        "",
    ]
    return "\n".join(parts)


def render_holdings(trades, book):
    if trades.empty:
        return ("No trades recorded. When Jazib reports a buy or sell, record it with "
                "`scripts/ledger.py trade DATE SYMBOL buy|sell QTY PRICE --fees F --call ID`, then rebuild.")
    t = trades.assign(qty=trades["qty"].astype(float), price=trades["price"].astype(float))
    rows = []
    for sym, g in t.groupby("ticker"):
        buys = g[g.side == "buy"]
        net = buys.qty.sum() - g[g.side == "sell"].qty.sum()
        if net <= 0:
            continue
        cost = (buys.qty * buys.price).sum() / buys.qty.sum()
        s = close_series(sym)
        last, asof = (s.iloc[-1], s.index[-1].date()) if s is not None else (float("nan"), "n/a")
        rows.append([sym, f"{net:g}", f"{cost:,.2f}", f"{last:,.2f} ({asof})", f"{net * last:,.0f}", f"{(last / cost - 1) * 100:+.1f}%"])
    text = md_table(["ticker", "shares", "average cost", "last close", "value Rs", "gain"], rows) if rows else "No open positions."
    if not book.empty:
        b = book.iloc[-1]
        text += (f"\n\nBook on {b.date}: value Rs{float(b.book_value):,.0f} (holdings Rs{float(b.market_value):,.0f}, cash Rs{float(b.cash):,.0f}); "
                 f"the same money in the KMI All Share: Rs{float(b.kmi_benchmark):,.0f}. Daily history: ledger/book_daily.csv.")
    return text


def render_pending(calls, st, today):
    c = calls.assign(status=st)
    o = c[(c.status == "open") & (c.event_date != "")].sort_values("event_date")
    due = o[o.event_date < str(today)]
    soon = o[(o.event_date >= str(today)) & (o.event_date <= str(today + pd.Timedelta(days=45)))]
    text = md_table(["event date", "id", "ticker", "event", "odds"], [[r.event_date, r.id, r.ticker, short(r.event, 80), r.probability] for r in soon.itertuples()]) if len(soon) else "Nothing in the next 45 days."
    if len(due):
        text += "\n\n**Past their event date and not yet scored** (price-reaction rows score five sessions after the release): " + ", ".join(f"{r.id} {r.ticker} ({r.event_date})" for r in due.itertuples())
    return text


def render_scores(calls, scores):
    s = scores.merge(calls[["id", "kind", "ticker", "prediction", "probability"]], left_on="call_id", right_on="id", how="left")
    graded = s[s.outcome.isin(["0", "1"])].copy()
    graded["p"] = graded.probability.astype(float)
    graded["o"] = graded.outcome.astype(float)
    graded["brier"] = (graded.p - graded.o) ** 2
    lines = []
    for label, g in [("all", graded), *graded.groupby("kind")]:
        if len(g):
            lines.append([label, len(g), f"{g.brier.mean():.3f}", f"{int(g.o.sum())} of {len(g)}", f"{g.p.mean():.2f}"])
    text = md_table(["rows", "n", "Brier", "held", "mean stated odds"], lines) if lines else "Nothing scored yet."
    text += "\n\n" + md_table(["id", "scored", "ticker", "prediction", "odds", "outcome", "note"],
                              [[r.call_id, r.scored_at[:10], r.ticker, short(r.prediction, 80), r.probability, r.outcome, short(r.note, 80)] for r in s.itertuples()])
    return text


def splice(text, block, body):
    a, b = f"<!-- ledger:{block} -->", f"<!-- /ledger:{block} -->"
    if a not in text:
        raise SystemExit(f"missing marker {a}")
    i, j = text.index(a) + len(a), text.index(b)
    return text[:i] + "\n" + body + "\n" + text[j:]


def views(today=None):
    today = today or date.today()
    calls, scores, trades, deposits = (load(n) for n in COLS)
    st = status(calls, scores)
    book = book_daily(trades, deposits)
    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    state = splice(state, "holdings", render_holdings(trades, book))
    state = splice(state, "pending", render_pending(calls, st, pd.Timestamp(today)))
    card = (L / "scorecard.md").read_text(encoding="utf-8")
    card = splice(card, "scores", render_scores(calls, scores))
    return {ROOT / "PICKS.md": render_picks(calls, st, today), ROOT / "STATE.md": state, L / "scorecard.md": card,
            L / "book_daily.csv": book.to_csv(index=False, lineterminator="\n")}


def validate():
    calls, scores, trades, deposits = (load(n) for n in COLS)
    bad = []
    for n, df in [("calls", calls), ("scores", scores), ("trades", trades), ("deposits", deposits)]:
        if list(df.columns) != COLS[n]:
            bad.append(f"ledger/{n}.csv: columns must be {COLS[n]}")
    if bad:
        return bad
    ids = set(calls.id)
    if calls.id.duplicated().any():
        bad.append(f"calls: duplicate ids {sorted(calls.id[calls.id.duplicated()])}")
    st = status(calls, scores)
    for r, s in zip(calls.itertuples(), st):
        if not re.fullmatch(r"C\d{4}", r.id):
            bad.append(f"{r.id}: id must look like C0001")
        if r.kind not in KINDS or r.action not in ACTIONS:
            bad.append(f"{r.id}: kind {r.kind!r} or action {r.action!r} not allowed")
        if r.probability and not 0 <= float(r.probability) <= 1:
            bad.append(f"{r.id}: probability outside 0 to 1")
        if r.supersedes and r.supersedes not in ids:
            bad.append(f"{r.id}: supersedes unknown {r.supersedes}")
        if r.journal and not (ROOT / r.journal).exists():
            bad.append(f"{r.id}: journal {r.journal} not found")
        if s == "open" and r.kind == "call" and r.action not in ("paper", "pass") and not (r.probability and r.proves_wrong):
            bad.append(f"{r.id}: an open call needs odds and proves_wrong")
    for r in scores.itertuples():
        if r.call_id not in ids:
            bad.append(f"scores: unknown call {r.call_id}")
        if r.outcome not in OUTCOMES:
            bad.append(f"scores: {r.call_id} outcome {r.outcome!r} not in {sorted(OUTCOMES)}")
    if scores.call_id.duplicated().any():
        bad.append(f"scores: scored twice {sorted(scores.call_id[scores.call_id.duplicated()])}")
    held = {}
    for r in trades.itertuples():
        if r.side not in ("buy", "sell") or float(r.qty) <= 0 or float(r.price) <= 0:
            bad.append(f"trades: bad row {r.date} {r.ticker}")
            continue
        held[r.ticker] = held.get(r.ticker, 0) + (float(r.qty) if r.side == "buy" else -float(r.qty))
        if held[r.ticker] < 0:
            bad.append(f"trades: {r.ticker} sold more than held on {r.date}")
        if r.call_id and r.call_id not in ids:
            bad.append(f"trades: unknown call {r.call_id}")
        elif r.call_id and (calls[calls.supersedes == r.call_id].made_at.str[:10] <= r.date).any():
            bad.append(f"trades: {r.date} {r.ticker} is linked to {r.call_id}, already superseded; link the open call")
    return bad


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    sub.add_parser("check")
    t = sub.add_parser("trade")
    for a in ("date", "ticker", "side", "qty", "price"):
        t.add_argument(a)
    t.add_argument("--fees", default="")
    t.add_argument("--call", default="")
    t.add_argument("--note", default="")
    s = sub.add_parser("score")
    s.add_argument("call_id")
    s.add_argument("outcome")
    s.add_argument("--note", default="")
    d = sub.add_parser("deposit")
    d.add_argument("date")
    d.add_argument("amount")
    d.add_argument("--note", default="")
    a = ap.parse_args()
    target = L / {"trade": "trades.csv", "score": "scores.csv"}.get(a.cmd, "deposits.csv")
    before = target.read_bytes() if target.exists() else None
    if a.cmd == "trade":
        append("trades", {"date": a.date, "ticker": a.ticker.upper(), "side": a.side, "qty": a.qty, "price": a.price,
                          "fees": a.fees, "call_id": a.call, "note": a.note})
    elif a.cmd == "score":
        append("scores", {"call_id": a.call_id, "scored_at": date.today().isoformat(), "outcome": a.outcome, "note": a.note})
    elif a.cmd == "deposit":
        append("deposits", {"date": a.date, "amount": a.amount, "note": a.note})
    bad = validate()
    if bad:
        if a.cmd in ("trade", "deposit", "score"):  # roll back the row just added
            target.write_bytes(before) if before is not None else target.unlink()
            print("row not recorded:")
        print("\n".join(bad))
        return 1
    if a.cmd == "check":
        stale = [str(p.relative_to(ROOT)) for p, txt in views().items() if not p.exists() or p.read_text(encoding="utf-8") != txt]
        if stale:
            print("stale, run `scripts/ledger.py build`: " + ", ".join(stale))
            return 1
        print("ledger ok")
        return 0
    for p, txt in views().items():
        p.write_text(txt, encoding="utf-8", newline="\n")
    print("built PICKS.md, STATE.md blocks, ledger/scorecard.md, ledger/book_daily.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
