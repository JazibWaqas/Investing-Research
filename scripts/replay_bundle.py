"""One markdown bundle per replay date, filtered to what was public before T.
    .venv/Scripts/python.exe -I scripts/replay_bundle.py 2024-06-14     (run scripts/asof.py T first)
Writes data/asof/<T>/BUNDLE.md: brief + schema (replay_exam.md s3, verbatim), the six asof files (trimmed), and the method
documents filtered by date (questions, actors, situation library, base rates). Sections start with '=== FILE: name ==='
so score_replay.py can resolve citations. Budget about 12,000 tokens (4 chars per token); the order of trimming is
announcements (low-value classes first), then flows, then actor lines.
"""
import re, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
BUDGET = 48000
MON = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}
MRE = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*"
SCOLS = ["symbol", "close", "r1m", "r3m", "r6m", "r12m", "dist_from_252_high", "vol20_over_vol120", "upper_locks_10d",
         "eps_qtr_end", "eps_yoy", "n_results", "n_material", "n_insider_buy", "n_insider_sell", "pe", "dy"]
PRIO = ["material_info", "financial_result", "dividend_or_bonus", "insider_trade", "other", "agm", "board_meeting_notice"]


def line_dates(l):
    """Every date a line mentions; a bare year or month is read as its end (conservative)."""
    d, l2 = [], l
    for m in re.finditer(rf"\b(\d{{1,2}}) {MRE},? ((?:19|20)\d\d)\b", l):
        d.append(pd.Timestamp(int(m[3]), MON[m[2].lower()], 1) + pd.offsets.MonthEnd(0) if not 1 <= int(m[1]) <= 28 else pd.Timestamp(int(m[3]), MON[m[2].lower()], int(m[1]))); l2 = l2.replace(m[0], " ")
    for m in re.finditer(rf"\b{MRE},? ((?:19|20)\d\d)\b", l2):
        d.append(pd.Timestamp(int(m[2]), MON[m[1].lower()], 1) + pd.offsets.MonthEnd(0)); l2 = l2.replace(m[0], " ")
    for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)\b", l2):
        d.append(pd.Timestamp(m[0])); l2 = l2.replace(m[0], " ")
    d += [pd.Timestamp(int(y), 12, 31) for y in re.findall(r"\b((?:19|20)\d\d)\b", l2)]
    return d


def questions():
    out = []
    for l in (ROOT / "knowledge" / "QUESTIONS.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-D]\d+)\. \*\*(.+?)\*\*", l)
        if m:
            q = re.sub(r"\s*\([^)]*\)", "", m[2])             # parentheticals carry dates and examples
            q = re.sub(r"\b\d[\d.,]*%\s*", "", q).replace("`", "")
            out.append(f"{m[1]}. {q}")
        elif re.match(r"^## [A-D]\. ", l):
            out.append("\n" + l)
    return "\n".join(out)


def actors(T):
    keep = []
    for l in (ROOT / "knowledge" / "playbooks" / "actors_and_incentives.md").read_text(encoding="utf-8").splitlines():
        if re.match(r"^\|[-| ]+\|$", l) or not l.strip():
            continue
        if l.startswith("|"):
            c = [x.strip() for x in l.strip("|").split("|")]
            if not c[0].isdigit():      # sponsor-group rows summarise 2018 to 2026 with undated facts
                continue
            # policy rows: announcement always (if before T); outcome only when it is a dated completion (ends Y) before T, never a "no"/pending state of 2026
            d = line_dates(c[1] + " " + c[2])
            if not d or max(d) >= T:
                continue
            o = line_dates(c[3])
            keep.append(f"| {c[0]} | {c[1]} | {c[2]} | " + (c[3] if o and max(o) < T and c[3].endswith(" Y") else "outcome not shown") + " |")
            continue
        d = line_dates(l)
        if d and max(d) < T:
            keep.append(l[:500])
    return "\n".join(keep) or "(no actor-map line is dated entirely before this date)"


def situations(T):
    """INDEX.md lines hold an outcome_end date (YYYY-MM-DD) and a summary; else front matter 'outcome_end:' in each file. None found -> none shipped."""
    d = ROOT / "knowledge" / "situations"
    idx, out = d / "INDEX.md", []
    if idx.exists():
        for l in idx.read_text(encoding="utf-8").splitlines():
            ds = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", l)
            if ds and pd.Timestamp(max(ds)) < T:
                out.append(l[:400])
    else:
        for f in sorted(d.glob("*.md")):
            fm = re.match(r"^---\n(.*?)\n---", f.read_text(encoding="utf-8"), re.S)
            e = re.search(r"outcome_end:\s*(\d{4}-\d{2}-\d{2})", fm[1]) if fm else None
            if e and pd.Timestamp(e[1]) < T:
                s = re.search(r"summary:\s*(.+)", fm[1])
                out.append(f"{f.stem}: {s[1] if s else ''}"[:400])
    return "\n".join(out) or "(no situation-library entry has an outcome that closed before this date, or the library has no INDEX.md)"


def base_rates(T):
    f = ROOT / "tests" / "BASE_RATES.csv"
    if not f.exists():
        return "type,n,hit_rate,median,p50plus,source
none,,,,,no base rates available"
    b = pd.read_csv(f)
    # Base rates were measured on the full sample (as_of_cutoff 2026-10-16 on every row); point-in-time recomputation
    # is not available. Ship a compact subset with an explicit look-ahead warning so the replay agent has the same
    # full-sample knowledge that the plain-rule comparison arm (S3) was chosen with. Logged as a known contamination.
    keep = ["type", "horizon", "n", "hit_rate", "median", "p50plus", "worst", "placebo_median", "verdict"]
    b = b[[c for c in keep if c in b.columns]]
    b = b[~b["type"].astype(str).str.startswith(("policy_", "regime_", "index_", "dividend_", "sector_momentum_ls_grid"))]
    head = ("# WARNING: measured on data through 2026-10-16, partly AFTER this replay date. Use only as rough odds for a "
            "situation TYPE; infer nothing about specific names or dates.
")
    return head + b.to_csv(index=False)


def brief():
    t = (ROOT / "knowledge" / "playbooks" / "replay_exam.md").read_text(encoding="utf-8")
    return t[t.index("## 3. ") : t.index("## 4. ")].split("\n", 1)[1].strip()


def main(date):
    from prices import load_panel
    A = ROOT / "data" / "asof" / date
    T = pd.Timestamp(date)
    raw, vol, tv = load_panel()
    mtv = tv.loc[:T].rolling(60, min_periods=40).median().iloc[-1]

    sc = pd.read_csv(A / "screens.csv")
    lock, res, ins = sc.upper_locks_10d.fillna(0) > 0, sc.n_results.fillna(0) > 0, (sc.n_insider_buy.fillna(0) + sc.n_insider_sell.fillna(0)) > 0
    top = set(sc.assign(v=sc.symbol.map(mtv)).nlargest(60, "v").symbol)
    sc = sc[sc.symbol.isin(top) | lock | res | ins]
    sc = sc[[c for c in SCOLS if c in sc]].round(3)
    sc_txt = sc.to_csv(index=False)

    an = pd.read_csv(A / "announcements_30d.csv")
    an["date"] = an.datetime.str[:10]
    an["title"] = an.title.str.replace(r"^Disclosure of Interest by a Director.*", "Insider trade disclosure", regex=True).str[:75]
    an["p"] = an.klass.map({k: i for i, k in enumerate(PRIO)}).fillna(4)
    an = an[an.klass != "board_meeting_notice"].sort_values(["p", "date"], ascending=[True, False])   # notices are in calendar.md

    fl = pd.read_csv(A / "flows.csv")
    fl_txt = fl.to_csv(index=False)
    act = actors(T).split("\n")

    def assemble(nan, nact, flows):
        a = an.head(nan)[["date", "symbol", "klass", "title"]].sort_values("date").to_csv(index=False)
        secs = [("BRIEF", brief()), ("market.md", (A / "market.md").read_text(encoding="utf-8")), ("sectors.csv", (A / "sectors.csv").read_text(encoding="utf-8")),
                ("screens.csv", sc_txt), ("announcements_30d.csv", a), ("flows.csv", flows), ("calendar.md", (A / "calendar.md").read_text(encoding="utf-8")),
                ("questions.md", questions()), ("actors.md", "\n".join(act[:nact])), ("situations.md", situations(T)), ("base_rates.csv", base_rates(T))]
        return f"# Replay bundle, close of {date}\n\n" + "\n\n".join(f"=== FILE: {n} ===\n{t.rstrip()}" for n, t in secs) + "\n=== END ===\n"

    nan, nact = len(an), len(act)
    flows = fl_txt
    while len(assemble(nan, nact, flows)) > BUDGET:
        if nan > 40:
            nan = int(nan * 0.85)
        elif flows is fl_txt:
            f2 = fl.assign(a=fl.net_usd_mn.abs()).sort_values("a", ascending=False).groupby(["kind", "window"]).head(12).drop(columns="a")
            flows = f2.sort_index().to_csv(index=False)
        elif nact > 6:
            nact = int(nact * 0.8)
        else:
            nan = max(nan - 10, 0)
            if nan == 0:
                break
    txt = assemble(nan, nact, flows)
    (A / "BUNDLE.md").write_text(txt, encoding="utf-8")
    print(f"{date}: {len(txt):,d} chars, ~{len(txt) // 4:,d} tokens; announcements {nan}/{len(an)}, screens {len(sc)}, actor lines {nact}/{len(act)}")


if __name__ == "__main__":
    main(sys.argv[1])
