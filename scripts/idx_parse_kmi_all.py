"""Parse the PSX KMI All Share recomposition PDF (N-659) into data/kmi_allshare_2026-06-05.csv.
Index = rows with final status Compliant, plus rows with ratios but a footnote-only status (AVN, OCTOPUS)."""
import pdfplumber, pandas as pd
pdf = pdfplumber.open('data/raw/index_pdfs/kmi_allshare_2026-06-05.pdf')
rows = []
for pg in pdf.pages[2:]:
    for t in pg.extract_tables():
        for r in t:
            if r[0] and r[0].replace(' ', '').isdigit() and len(r) >= 11:
                st = (r[10] or '').strip()
                ok = st.startswith('Compliant') or (st == '' and (r[4] or '').endswith('%'))
                if ok:
                    rows.append(((r[1] or '').strip(), (r[2] or '').replace('*', '').strip()))
d = pd.DataFrame(rows, columns=['symbol', 'company']).drop_duplicates('symbol')
d.to_csv('data/kmi_allshare_2026-06-05.csv', index=False)
print(len(d))
