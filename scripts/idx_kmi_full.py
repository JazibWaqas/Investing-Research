"""Full KMI All Share compliant lists from the ratio tables in recomposition notices -> data/index_members/."""
import pdfplumber, re, sys, pandas as pd
D='data/raw/index_pdfs/'
files={ # file: (effective_date, stated total)
 'Notice_1412_of_Recomposition_of_KMI_ALL_Shares_Dec_22_2020.pdf':('2020-12-31',209),
 'Notice-_KMI-All-Index-Re-composition-Jun-30-2023-Final.pdf':('2023-12-26',258),
 'KMI-ALL-Share-Recomposition-Notice-june-12-2024.pdf':('2024-06-25',255),
 'Notice-KMIALLshare-Notice-as-of-June-2024.pdf':('2025-01-03',264),
 'KMI-All-share-Notice-Recomposition-as-of-Dec-_2024-Final.pdf':('2025-06-10',258),
 'Merged_KMIALL_Notice_and_FinalList_June2025.pdf':(None,281),
 'Notice-to-KMIALL-re-composition-as-of-Dec-2025-Revised.pdf':('2026-06-05',309),
}
for f,(eff,tot) in files.items():
    rows={}
    for pg in pdfplumber.open(D+f).pages:
        for t in pg.extract_tables():
            for r in t:
                if r and r[0] and r[0].replace(' ','').isdigit() and len(r)>=8:
                    st=[c for c in r[3:] if c and re.search(r'ompliant|ature',c)]
                    fin=(r[-1] or '').strip()
                    rows[(r[1] or '').strip()]=(r[2] or '').replace('*','').strip(), fin, r[3] if len(r)>3 else ''
    ok=[k for k,(n,fin,o) in rows.items() if fin.startswith('Compliant') or (fin=='' )]
    ok2=[k for k,(n,fin,o) in rows.items() if fin.startswith('Compliant')]
    print(f[:50],eff,tot,'rows',len(rows),'compliant',len(ok2),'incl blank',len(ok))
