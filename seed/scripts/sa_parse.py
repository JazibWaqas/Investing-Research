import re, glob, pandas as pd, numpy as np
rows=[]
for f in glob.glob('sa/*.html'):
    t=f.split('/')[-1][:-5]; h=open(f,errors='ignore').read()
    def arr(k):
        m=re.search(k+r':\[([-0-9.,nul]*)\]',h)
        return [None if x in ('null','') else float(x) for x in m.group(1).split(',')] if m else None
    dk=re.search(r'datekey:\[([^\]]*)\]',h)
    if not dk: continue
    dates=[x.strip('"') for x in dk.group(1).split(',')]
    data={k:arr(k) for k in ['pe','peForward','pb','roe','dividendyield','payoutratio']}
    n=len(dates)
    for i in range(n):
        r={'t':t,'date':dates[i]}
        for k,v in data.items(): r[k]=v[i] if v and i<len(v) else None
        rows.append(r)
D=pd.DataFrame(rows); print(D.shape); print(D.date.value_counts().head(12)); print(D.head(8).to_string())
D.to_csv('sa_ratios.csv',index=False)
