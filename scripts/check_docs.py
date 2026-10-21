"""check_docs.py: keeps the documentation navigable. Run at the end of every session that edits docs.

    .venv\\Scripts\\python.exe -I -X utf8 scripts\\check_docs.py

Checks, on live docs (tracked .md files outside archive/, seed/, data/asof/, tests/out/):
  1. every repo path a doc mentions (folder/file.ext, ../file.md, or a root doc name) exists;
  2. no live doc names a retired file (see RETIRED) without its new path;
  3. AGENTS.md points to CLAUDE.md, and the two psx-weekly skill copies are identical;
  4. PICKS.md and STATE.md mention a Lucky group name only on lines that exclude it;
  5. every live doc is listed in INDEX.md, by its path or by its folder.
Exit code 1 if anything fails. Fix the doc, not the check, unless the check is wrong.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = ("archive/", "seed/", "data/asof/", "tests/out/")
RETIRED = {  # old name -> where its content went
    "ORCHESTRATOR_HANDOFF.md": "knowledge/FINDINGS.md",
    "HANDOFF.md": "STATE.md",
    "REPORT.md": "archive/REPORT_2026-10-18.md",
    "PLAN.md": "archive/PLAN_2026-10-17.md",
    "sector_map.md": "knowledge/sectors/README.md",
    "SKILL_psx_weekly.md": ".claude/skills/psx-weekly/SKILL.md",
}
PATH_RE = re.compile(r"(?<![\w/.\-=])((?:\.\./|\./)*[\w.\-]+(?:/[\w.\-]+)+/?|[A-Z][A-Z_]+\.md)")
# Paths named on purpose although they do not exist (a bug's missing file, a name a spec used).
ALLOW = {"data/prices_raw/HUBCXD.csv", "tests/value_pubdates.md", "scripts/replay_run.py"}
EXT_OK = (".md", ".csv", ".py", ".json", ".parquet", ".txt", ".pdf")
LUCKY = re.compile(r"\b(LUCK|LCI|Lucky)\b")
EXCLUDES = re.compile(r"off-limits|exclud|withdrawn|not eligible|never|no Lucky|cannot|restriction|voided|removed|without", re.I)


def tracked():
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True).stdout
    return [p for p in out.splitlines() if p]


def live_docs(files):
    return [p for p in files if p.endswith(".md") and not p.startswith(SKIP)]


def exists(token, doc, files, names):
    """True if the token names something in the repo. Accepts shorthand: a bare file name that exists
    somewhere, a path relative to the doc, a path suffix (prices_raw/X.csv), or a truncated prefix
    (knowledge/situations/03)."""
    t = token.rstrip("/.,;:)")
    first = t.split("/")[0]
    if t in ALLOW or any(c in t for c in "<>*{}") or t.startswith(("http", "www.", "data/raw/")):
        return True
    if "." in first and first not in (".", "..") and not (ROOT / first).exists():
        return True  # a web domain, not a repo path
    if "/" in t and not (ROOT / first).exists() and first not in (".", ".."):
        if not any(f.endswith("/" + t) for f in files):
            return not t.endswith(EXT_OK)  # prose like "and/or" is not a path
    for base in (ROOT, (ROOT / doc).parent):
        if (base / t).exists():
            return True
    if "/" not in t:
        return t in names
    return any(f.startswith(t) or f.endswith("/" + t) for f in files)


def main():
    files = tracked()
    names = {f.rsplit("/", 1)[-1] for f in files}
    docs = live_docs(files)
    problems = []

    for doc in docs:
        text = (ROOT / doc).read_text(encoding="utf-8", errors="replace")
        for n, line in enumerate(text.splitlines(), 1):
            for old, new in RETIRED.items():
                if re.search(r"(?<![\w/])" + re.escape(old), line) and doc != "DECISIONS.md":  # the log records old names on purpose
                    problems.append(f"{doc}:{n}: names retired {old}; now {new}")
            for m in PATH_RE.finditer(line):
                tok = m.group(1)
                if tok in RETIRED:
                    continue
                if "/" not in tok and not tok.endswith(".md"):
                    continue
                if not exists(tok, doc, files, names):
                    problems.append(f"{doc}:{n}: missing path {tok}")

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "CLAUDE.md" not in agents:
        problems.append("AGENTS.md: must point to CLAUDE.md")
    a, b = ROOT / ".claude/skills/psx-weekly/SKILL.md", ROOT / ".agents/skills/psx-weekly/SKILL.md"
    if a.exists() and b.exists() and a.read_bytes() != b.read_bytes():
        problems.append("skill copies differ: copy .claude/skills/psx-weekly/SKILL.md over .agents/skills/psx-weekly/SKILL.md")

    for doc in ("PICKS.md", "STATE.md"):
        if not (ROOT / doc).exists():
            problems.append(f"{doc}: missing")
            continue
        for n, line in enumerate((ROOT / doc).read_text(encoding="utf-8").splitlines(), 1):
            if LUCKY.search(line) and not EXCLUDES.search(line):
                problems.append(f"{doc}:{n}: Lucky group name on a line that does not exclude it")

    index = (ROOT / "INDEX.md").read_text(encoding="utf-8") if (ROOT / "INDEX.md").exists() else ""
    for doc in docs:
        parent = doc.rsplit("/", 1)[0] + "/" if "/" in doc else ""
        # root and knowledge/ top-level files need their own line; deeper files may be covered by their folder
        listed = doc in index or (parent not in ("", "knowledge/") and parent in index)
        if not listed:
            problems.append(f"INDEX.md: does not list {doc} or its folder")

    for p in problems:
        print(p)
    print(f"{len(docs)} live docs checked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
