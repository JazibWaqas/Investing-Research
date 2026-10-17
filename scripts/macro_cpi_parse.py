import glob,re,pdfplumber,pandas as pd
rows={}
for f in glob.glob('data/raw/macro/pbs/*.pdf'):
    with pdfplumber.open(f) as p: t=" ".join((pg.extract_text() or "") for pg in p.pages[:4])
    t=re.sub(r'\s+',' ',t)
    i=t.find('Table 1.a General'); 
    if i<0: print('no table',f); continue
    j=t.find('Table 1.b',i); seg=t[i:j if j>0 else i+4000]
    for m in re.finditer(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*-(\d\d) (-?\d+\.\d) (-?\d+\.\d)',seg):
        mo=pd.to_datetime(f"20{m.group(2)}-{m.group(1)}-01").strftime('%Y-%m')
        rows.setdefault(mo,[]).append((float(m.group(3)),float(m.group(4)),f))
out=[]
for mo,v in sorted(rows.items()):
    vals={(a,b) for a,b,_ in v}
    out.append((mo,v[-1][0],v[-1][1],len(vals)))
d=pd.DataFrame(out,columns=['month','yoy','mom','n_distinct'])
print(len(d),d.month.min(),d.month.max()); print(d[d.n_distinct>1])
d.to_csv('data/raw/macro/cpi_pbs_parsed.csv',index=False)
s=pd.read_csv('seed/data/macro/cpi_yoy_2015_2026.csv')
m=d.merge(s,on='month',how='outer')
m['diff']=m.yoy-m.cpi_yoy_pct
print(m[m['diff'].abs()>0.06])
print(m[m.yoy.isna()].month.tolist()[:5], m[m.yoy.isna()].month.max())
