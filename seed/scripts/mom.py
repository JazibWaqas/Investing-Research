import pandas as pd, numpy as np, glob
P={};V={}
for f in glob.glob('eod/*.csv'):
    t=f.split('/')[-1][:-4]
    d=pd.read_csv(f,parse_dates=['date']).drop_duplicates('date').set_index('date').sort_index()
    P[t]=d.close.astype(float); V[t]=d.volume.astype(float)
P=pd.DataFrame(P); V=pd.DataFrame(V)
R=P.pct_change()
ca=(R<-0.105)&(P.shift(1)>10)   # corporate action gaps (beyond circuit)
R=R.mask(ca,0).clip(upper=0.105)
I=(1+R.fillna(0)).cumprod().where(P.notna())
mkt=(1+R.mean(axis=1).fillna(0)).cumprod()
medv=V.rolling(20).median().shift(1); adv=(P*V).rolling(20).median().shift(1)
sig=((R>=0.07)|((R>=0.03)&(V>=5*medv)))&(P>=5)&(adv>=5e6)
prior20=I/I.shift(20)-1
rows=[]
for t in I.columns:
    s=sig[t].fillna(False).values; last=-999; idx=I.index
    for k in np.where(s)[0]:
        if k-last<20 or k+61>=len(idx): continue
        last=k; e=k+1  # enter next close
        pe=I[t].iloc[e]; me=mkt.iloc[e]
        if np.isnan(pe): continue
        r={'t':t,'date':idx[k],'prior20':prior20[t].iloc[k],'day':R[t].iloc[k]}
        for h in (5,10,20,60):
            r[f'r{h}']=I[t].iloc[e+h]/pe-1; r[f'x{h}']=r[f'r{h}']-(mkt.iloc[e+h]/me-1)
        path=I[t].iloc[e:e+21]/pe-1
        r['mfe20']=path.max(); r['mae20']=path.min()
        rows.append(r)
E=pd.DataFrame(rows); E.to_csv('momentum_events.csv',index=False)
def summ(d,lab):
    print(f"{lab:28s} n={len(d):4d} | x5 {d.x5.mean()*100:5.1f} x10 {d.x10.mean()*100:5.1f} x20 {d.x20.mean()*100:5.1f} x60 {d.x60.mean()*100:5.1f} | win20 {(d.x20>0).mean()*100:3.0f}% | med x20 {d.x20.median()*100:5.1f} | mae20 {d.mae20.mean()*100:5.1f}")
summ(E,'all signals')
summ(E[E.prior20>0.20],'prior20 >20%')
summ(E[(E.prior20>0)&(E.prior20<=0.20)],'prior20 0..20%')
summ(E[E.prior20<=0],'prior20 <=0')
E['yr']=E.date.dt.year
for y,g in E[E.prior20>0.20].groupby('yr'): summ(g,f'  >20% {y}')
