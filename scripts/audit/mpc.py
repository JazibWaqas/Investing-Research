import pandas as pd, numpy as np
P,V,R,I=[pd.read_parquet(n+'.parquet') for n in 'PVRI']
adv=(P*V).rolling(20).median().shift(1)
ew=(1+R.where(adv>=5e6).mean(axis=1).fillna(0)).cumprod()
k=pd.read_csv('kse.csv',parse_dates=['date']).set_index('date').close
pr=pd.read_csv('pr.csv',parse_dates=['date']); pr['chg']=pr.rate.diff(); pr=pr.dropna()
def fwd(s,d,h):
    i=s.index.searchsorted(pd.Timestamp(d)); return s.iloc[i+h]/s.iloc[i]-1 if i+h<len(s) else np.nan
for name,s in [('EW',ew),('KSE100',k)]:
    D=pr.copy(); D['insample']=D.date>=s.index[0]
    for h in (20,60,120): D[f'f{h}']=[fwd(s,d,h)*100 for d in D.date]
    D['type']=np.where(D.chg>0,'hike','cut')
    for lab,Z in [('as coded',D),('in-sample only',D[D.insample])]:
        g=Z.groupby('type')[['f20','f60','f120']].agg(['mean','median','count']).round(1)
        print(name,lab); print(g.to_string())
    # unconditional
    u={h:(s.shift(-h)/s-1).mean()*100 for h in (20,60,120)}; print(name,'unconditional mean', {h:round(v,1) for h,v in u.items()})
    Z=D[D.insample&(D.type=='cut')].copy(); Z['episode']=(Z.date.diff().dt.days>180).cumsum()
    print(Z.groupby('episode').agg(start=('date','min'),n=('date','size'),f120_first=('f120','first'),f120_mean=('f120','mean')).round(1).to_string())
