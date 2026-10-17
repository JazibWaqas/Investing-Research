"""Download the sampled insider PDFs (data/insider_sample.csv) to data/raw/filings/insider/. 1 request/sec via psx_api. Never executes anything."""
import sys, time
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import psx_api
out = ROOT / "data/raw/filings/insider"; out.mkdir(parents=True, exist_ok=True)
S = pd.read_csv(ROOT / "data/insider_sample.csv", dtype={"doc": str})
log = open(ROOT / "data/raw/insider_downloads.log", "a")
for n, d in enumerate(S.doc):
    p = out / f"{d}.pdf"
    if p.exists() and p.stat().st_size > 500: continue
    try:
        psx_api.download_document(d, p)
        ok = p.read_bytes()[:5] == b"%PDF-"
        log.write(f"{d}\t{'ok' if ok else 'notpdf'}\t{p.stat().st_size}\n")
    except Exception as e:
        log.write(f"{d}\tERR\t{e}\n")
    log.flush()
    if n % 50 == 0: print(n, flush=True)
print("done")
