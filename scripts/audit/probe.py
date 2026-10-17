import pandas as pd, numpy as np
from load_all import load
P,V,R,I=load()
print('tickers',P.shape)
Rraw=P.pct_change(fill_method=None)
prev=P.shift(1)
ca=(Rraw<-0.105)&(prev>10); up=(Rraw>0.105)&(prev>10)
print('ca down flags',int(ca.sum().sum()),'up flags',int(up.sum().sum()))
# NaN gaps inside life
inside=P.notna().cumsum()>0
inside&=P[::-1].notna().cumsum()[::-1]>0
gaps=(P.isna()&inside)
print('missing days inside life',int(gaps.sum().sum()),'of',int(inside.sum().sum()))
# returns lost: day after a gap where R is NaN but P notna
lost=Rraw.isna()&P.notna()&prev.isna()&inside.shift(1,fill_value=False)
# true move across gap
Pf=P.ffill(); Rtrue=P/Pf.shift(1)-1
lostmoves=Rtrue.where(lost)
print('returns dropped after gaps',int(lost.sum().sum()),'mean abs',float(lostmoves.abs().stack().mean()))
# compare total log return: index vs ffilled raw (no CA fix) for each ticker, share of difference due to gaps
lg=np.log1p(Rtrue.where(lost)).sum()
print('top tickers by dropped log-return:'); print(lg.sort_values().head(8).round(2)); print(lg.sort_values().tail(8).round(2))
liq=['OGDC','HUBC','MEBL','FFC','LUCK','SYS','ENGRO','PPL','MCB','UBL']
print('liquid names dropped logret', lg.reindex(liq).round(3).to_dict())
# corporate actions check
ca_df=pd.read_csv('corporate_actions.csv',comment='#')
print(ca_df.type.value_counts())
for _,r in ca_df[ca_df.type!='cash_div'].iterrows():
    t=r.ticker; d=pd.Timestamp(r.ex_date)
    if t not in P: continue
    s=Rraw[t].dropna(); i=s.index.searchsorted(d)
    w=s.iloc[max(i-1,0):i+2]
    print(t,r.ex_date,r.type,r.amount_pkr_or_ratio,'raw rets',[round(x,3) for x in w.values],'fixed',[round(x,3) for x in R[t].reindex(w.index).values])
# distribution of flagged down moves: how many look like small bonuses (-8.5..-10.5 not flagged)
band=((Rraw<-0.085)&(Rraw>=-0.105)&(prev>10)).sum().sum()
print('moves in -8.5%..-10.5% band (kept, includes limit downs and 10% bonus gaps):',int(band))
