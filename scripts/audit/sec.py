import pandas as pd, numpy as np
S=pd.read_csv('sector_monthly_ret.csv',index_col=0); S.index=pd.PeriodIndex(S.index,freq='M')
M=pd.read_csv('ew_mkt_ret.csv',index_col=0).iloc[:,0]; M.index=pd.PeriodIndex(M.index,freq='M')
print('sectors',S.shape[1], 'mkt==mean of sectors?', round((S.mean(axis=1)-M).abs().max(),3))
def run(S,L=6,H=3,k=3,skip=0,step=1):
    idx=(1+S.fillna(0)).cumprod().where(S.notna().cumsum()>0)
    past=idx.shift(skip)/idx.shift(L+skip)-1; fut=idx.shift(-H)/idx-1
    rows=[]
    for i,d in enumerate(S.index):
        if i%step: continue
        p=past.loc[d].dropna(); f=fut.loc[d]
        if len(p)<2*k or f[p.index].isna().any(): continue
        r=p.rank(); top=r.nlargest(k).index; bot=r.nsmallest(k).index
        rows.append({'d':d,'spr':f[top].mean()-f[bot].mean()})
    T=pd.DataFrame(rows)
    return f"L{L} H{H} k{k} skip{skip} step{step}: n={len(T)} mean {T.spr.mean()*100:.2f}% median {T.spr.median()*100:.2f}% win {(T.spr>0).mean()*100:.0f}% worst {T.spr.min()*100:.1f}% t(naive) {T.spr.mean()/T.spr.std()*np.sqrt(len(T)):.2f} t(nonoverlap~/sqrt(H)) {T.spr.mean()/T.spr.std()*np.sqrt(len(T)/H):.2f}"
print(run(S)); print(run(S.drop(columns='conv_bank')))
print(run(S,step=3)); 
for o in range(3): print(' offset',o, run(S.iloc[o:],step=3))
print(run(S,L=12)); print(run(S,L=3)); print(run(S,H=1)); print(run(S,H=6)); print(run(S,k=2)); print(run(S,skip=1))
# first half / second half
print('2017-2021', run(S.loc[:'2021-06'])); print('2021-2026', run(S.loc['2021-07':]))
# rotation after first cut: 6m sector excess vs EW mkt
idx=(1+S.fillna(0)).cumprod(); mi=(1+M.fillna(0)).cumprod()
for base in ['2020-02','2020-03','2024-05','2024-06','2021-08','2021-09']:
    b=pd.Period(base,'M'); e=b+6
    ex=((idx.loc[e]/idx.loc[b]-1)-(mi.loc[e]/mi.loc[b]-1))*100
    print('base',base,'6m mkt',round((mi.loc[e]/mi.loc[b]-1)*100,1),'excess:',ex.round(0).sort_values().to_dict())
# current 6m momentum at last month
print('last 6m (to',S.index[-1],')',((idx.iloc[-1]/idx.iloc[-7]-1)*100).round(0).sort_values(ascending=False).to_dict())
