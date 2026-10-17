import pandas as pd, numpy as np
from load_all import load
P,V,R,I=load()
print('tickers',P.shape[1],'days',P.shape[0])
s=pd.read_csv('screener_20261016.csv').set_index('symbol')
mcap=pd.to_numeric(s.market_cap,errors='coerce'); ff=pd.to_numeric(s.free_float,errors='coerce')
kmi=s.listed_in.astype(str).str.contains('KMIALLSHR')
adv=(P*V).rolling(20).median().shift(1)
medv=V.rolling(20).median().shift(1)
mkt=(1+R.where(adv>=5e6).mean(axis=1).fillna(0)).cumprod()   # liquid EW market
def study(sig,lab,cool=20,hs=(5,10,20,60)):
    rows=[]; idx=I.index; M=mkt.values
    for t in sig.columns:
        s_=np.where(sig[t].fillna(False).values)[0]; last=-999; It=I[t].values
        for k in s_:
            if k-last<cool or k+max(hs)+1>=len(idx): continue
            last=k; e=k+1
            if np.isnan(It[e]): continue
            r={'t':t,'k':k,'date':idx[k]}
            for h in hs:
                if np.isnan(It[e+h]): break
                r[f'x{h}']=It[e+h]/It[e]-M[e+h]/M[e]
            else:
                pth=It[e:e+21]/It[e]-1; r['mae20']=np.nanmin(pth); rows.append(r)
    E=pd.DataFrame(rows)
    if len(E)==0: print(lab,'none'); return E
    E['mcap']=E.t.map(mcap); E['kmi']=E.t.map(kmi)
    print(f"{lab:34s} n={len(E):5d} x5 {E.x5.mean()*100:5.1f} x20 {E.x20.mean()*100:5.1f} x60 {E.x60.mean()*100:5.1f} | med20 {E.x20.median()*100:5.1f} win20 {(E.x20>0).mean()*100:3.0f}% mae {E.mae20.mean()*100:5.1f}")
    return E
liq2=adv>=2e6
prior20=I/I.shift(20)-1
r5=I/I.shift(5)-1
# 1 accumulation footprint: volume >=3x 20d median on 3+ of last 5 days, price change over 5d within +-4%
hv=(V>=3*medv).astype(float).rolling(5).sum()
acc=(hv>=3)&(r5.abs()<=0.04)&liq2&(P>=5)
E1=study(acc,'ACCUMULATION (vol up, price flat)')
# 2 breakout after accumulation: accumulation in prior 10d then +5% day
accp=acc.rolling(10).max().shift(1).fillna(0).astype(bool)
brk=accp&(R>=0.05)&liq2
E2=study(brk,'BREAKOUT after accumulation')
# 3 extended pump: up 50%+ in 20d
pump=(prior20>=0.5)&liq2&(P>=5)
E3=study(pump,'PUMP +50% in 20d (fade?)')
# 4 big momentum on small caps
big=((R>=0.07)|((R>=0.03)&(V>=5*medv)))&liq2&(P>=5)
E4=study(big,'MOMENTUM signal all caps')
for E,lab in [(E1,'ACC'),(E4,'MOM')]:
    if len(E):
        E['size']=pd.cut(E.mcap,[0,5e9,25e9,1e15],labels=['small<5bn','mid5-25bn','large>25bn'])
        for g,d in E.groupby('size',observed=True):
            print(f"   {lab} {g:12s} n={len(d):4d} x20 {d.x20.mean()*100:5.1f} med {d.x20.median()*100:5.1f} win {(d.x20>0).mean()*100:3.0f}% x60 {d.x60.mean()*100:5.1f}")
for E,n in [(E1,'acc'),(E2,'brk'),(E3,'pump'),(E4,'mom')]: E.to_csv(f'ev_{n}.csv',index=False)
