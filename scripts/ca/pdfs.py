"""Download (capped, 1 req/s, logged) and read filing PDFs. Files land in data/raw/filings/ and are only ever parsed."""
import sys
from pathlib import Path

from common import ROOT

FIL = ROOT / "data" / "raw" / "filings"
LOG = ROOT / "data" / "raw" / "filings_downloads.log"
CAP = 400


def downloaded():
    return {p.stem for p in FIL.glob("*.pdf")}


def fetch(ids):
    """Download ids not yet on disk, stopping at the 400-file cap. Returns list of ids now on disk."""
    import psx_api
    FIL.mkdir(parents=True, exist_ok=True)
    have = downloaded()
    for i in ids:
        i = str(i).zfill(6)
        if i in have:
            continue
        if len(have) >= CAP:
            print("CAP reached", file=sys.stderr)
            break
        try:
            psx_api.download_document(i, FIL / f"{i}.pdf")
            have.add(i)
        except Exception as e:  # noqa: BLE001
            print("FAIL", i, repr(e)[:100], file=sys.stderr)
    return [str(i).zfill(6) for i in ids if str(i).zfill(6) in have]


def text(doc_id, maxpages=3):
    import pdfplumber
    try:
        with pdfplumber.open(FIL / f"{doc_id}.pdf") as p:
            return "\n".join((pg.extract_text() or "") for pg in p.pages[:maxpages])
    except Exception as e:  # noqa: BLE001
        return f"ERR {e!r}"
