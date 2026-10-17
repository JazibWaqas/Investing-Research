import pandas as pd, numpy as np
import pandas as pd
class _L: pass
def load(): return [pd.read_parquet(n+'.parquet') for n in 'PVRI']
P,V,R,I=load()
adv=(P*V).rolling(20).median().shift(1)
ew=(1+R.where(adv>=5e6).mean(axis=1).fillna(0)).cumprod()
k=pd.read_csv('kse.csv',parse_dates=['date']).set_index('date').close
def fwd(series,d,hs=(5,20,60,120)):
    i=series.index.searchsorted(pd.Timestamp(d))
    if i+1>=len(series): return None
    b=series.iloc[i]   # close on/after event day
    pre=series.iloc[max(i-20,0)]
    out={'pre20':b/pre-1}
    for h in hs: out[f'f{h}']=series.iloc[i+h]/b-1 if i+h<len(series) else np.nan
    return out
imf=[('2019-05-12','SLA 2019 EFF'),('2019-07-03','Board 2019'),('2021-02-16','SLA resume'),('2022-08-29','Review 7-8'),('2023-06-30','SLA SBA'),('2023-07-12','Board SBA'),('2023-11-15','SLA SBA r1'),('2024-07-12','SLA EFF'),('2024-09-25','Board EFF'),('2025-03-25','SLA r1'),('2025-10-14','SLA r2'),('2026-03-27','SLA r3'),('2026-10-08','SLA r4')]
print('IMF events, EW liquid market:')
rows=[]
for d,l in imf:
    o=fwd(ew,d); 
    if o: rows.append({'date':d,'event':l,**{k_:round(v*100,1) for k_,v in o.items()}})
print(pd.DataFrame(rows).to_string(index=False))
pr=pd.read_csv('pr.csv',parse_dates=['date'])
pr['chg']=pr.rate.diff()
print('\nMPC rate changes (effective date) vs EW market:')
rows=[]
for _,r in pr.dropna().iterrows():
    o=fwd(ew,r.date)
    if o: rows.append({'date':r.date.date(),'chg':r.chg,**{k_:round(v*100,1) for k_,v in o.items()}})
D=pd.DataFrame(rows)
D['type']=np.where(D.chg>0,'hike','cut')
print(D.groupby('type')[['pre20','f5','f20','f60','f120']].mean().round(1)); print(D.groupby('type').size())
# first hike / first cut of a cycle
D['first']=D.type!=D.type.shift(1)
print('\nfirst move of a new cycle:'); print(D[D['first']][['date','chg','type','f20','f60','f120']].to_string(index=False))
