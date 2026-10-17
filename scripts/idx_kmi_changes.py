"""Extract incoming/outgoing tickers from PSX KMI All Share recomposition notices (tables on first pages)."""
import pdfplumber, re, json, sys
D='data/raw/index_pdfs/'
files={
 'Notice_1412_of_Recomposition_of_KMI_ALL_Shares_Dec_22_2020.pdf':3,
 'Notice-_KMI_All_Shares_Index_Recomposition_30-June-22_(M).pdf':3,
 'Notice-_KMI-All-Index-Re-composition-Jun-30-2023-Final.pdf':3,
 'KMI-ALL-Share-Recomposition-Notice-june-12-2024.pdf':3,
 'Notice-KMIALLshare-Notice-as-of-June-2024.pdf':3,
 'KMI-All-share-Notice-Recomposition-as-of-Dec-_2024-Final.pdf':2,
 'Merged_KMIALL_Notice_and_FinalList_June2025.pdf':2,
 'Notice-to-KMIALL-re-composition-as-of-Dec-2025-Revised.pdf':2,
 'Notice-with-List-incoming-outgoing-KMI-ALL-Shares-July-01-2019-Dec-31-2019.pdf':3,
 'sharia_KMI_All_Share_list_June_2021_Final_27122021.pdf':3,
 'Copy_of_KMI_All_Share_June_-22_23122022.pdf':3,
 'Notice-666_KMI_All_Share_Index_re-composition_for_Dec-22.pdf':3,
}
tk=re.compile(r'^[A-Z][A-Z0-9]{1,9}$')
out={}
for f,n in files.items():
    p=pdfplumber.open(D+f); inc=[];outg=[]
    for pg in p.pages[:n]:
        for t in pg.extract_tables():
            hdr=' '.join(str(c) for r in t[:3] for c in r if c)
            if 'ncoming' not in hdr and 'Outgoing' not in hdr and 'ncoming' not in (pg.extract_text() or '')[:900]: continue
            # find column of 'Outgoing'
            for r in t:
                cells=[(i,(c or '').strip()) for i,c in enumerate(r)]
                tks=[(i,c) for i,c in cells if tk.match(c.replace('\n',''))]
                for i,c in tks: (inc if len(tks)==2 and i==tks[0][0] or len(tks)==1 and i<len(r)//2 else outg).append(c)
    out[f]=(inc,outg); print(f,len(inc),len(outg))
json.dump(out,open('scripts/_tmp_kmi.json','w'))
