import re, glob, pandas as pd, numpy as np
rows=[]
for f in glob.glob('sa/*.html'):
    t=f.split('/')[-1][:-5]; h=open(f,errors='ignore').read()
    def arr(k):
        m=re.search(k+r':\[([-0-9.,nul]*)\]',h)
        return [None if x in ('null','') else float(x) for x in m.group(1).split(',')] if m else []
    dk=re.search(r'datekey:\[([^\]]*)\]',h)
    if not dk: continue
    dates=[x.strip('"') for x in dk.group(1).split(',')]
    pe,pb,roe,dy,po,lc,mc=[arr(k) for k in ['pe','pb','roe','dividendyield','payoutratio','lastCloseRatios','marketcap']]
    g=lambda a,i: a[i] if i<len(a) else None
    eps=[ (g(lc,i)/g(pe,i)) if g(lc,i) and g(pe,i) and g(pe,i)>0 else None for i in range(len(dates))]
    fy=[(d,e) for d,e in zip(dates,eps) if d!='TTM']
    fy=[x for x in fy if x[1]]
    cagr=None
    if len(fy)>=3:
        e_new=fy[0][1]; e_old=fy[min(3,len(fy)-1)][1]; n=min(3,len(fy)-1)
        if e_old and e_old>0 and e_new>0: cagr=(e_new/e_old)**(1/n)-1
    rows.append({'t':t,'price':g(lc,0),'pe':g(pe,0),'pb':g(pb,0),'roe':g(roe,0),'dy':g(dy,0) or 0,'payout':g(po,0),'mcap_bn':(g(mc,0) or 0)/1e3,'eps_cagr3':cagr,
                 'med_pe':np.nanmedian([x for x in pe[1:] if x and 0<x<60]) if len(pe)>1 else None})
U=pd.DataFrame(rows)
s=pd.read_csv('screener_20261016.csv'); s['t']=s.symbol.str.replace(r'X[DB]$','',regex=True)
s['adv_m']=pd.to_numeric(s.price,errors='coerce')*pd.to_numeric(s.volume_avg_30d,errors='coerce')/1e6
s['chg1y']=pd.to_numeric(s.change_1y_pct,errors='coerce')
U=U.merge(s[['t','sector','adv_m','chg1y']],on='t',how='left')
U=U[(U.pe>0)&(U.pe<60)&U.roe.notna()].copy()
U['ey']=1/U.pe; U['val']=U.ey+U.dy
U['r_val']=U.val.rank(pct=True); U['r_q']=U.roe.rank(pct=True); U['r_g']=U.eps_cagr3.rank(pct=True)
U['score']=0.45*U.r_val+0.30*U.r_q+0.25*U.r_g.fillna(0.5)
U.to_csv('universe_scored.csv',index=False)
pd.set_option('display.width',220)
c=['t','price','pe','med_pe','pb','roe','dy','eps_cagr3','mcap_bn','adv_m','chg1y','score']
print(len(U)); print(U.sort_values('score',ascending=False)[c].head(30).round(2).to_string(index=False))
