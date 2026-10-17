import pandas as pd, numpy as np, glob, os
def load():
    P={};V={}
    for f in glob.glob('eod_all/*.csv'):
        t=os.path.basename(f)[:-4]
        try: d=pd.read_csv(f,parse_dates=['date'])
        except: continue
        if len(d)<120: continue
        d=d.drop_duplicates('date').set_index('date').sort_index()
        P[t]=pd.to_numeric(d.close,errors='coerce'); V[t]=pd.to_numeric(d.volume,errors='coerce')
    P=pd.DataFrame(P).sort_index(); V=pd.DataFrame(V).reindex(P.index)
    R=P.pct_change(fill_method=None)
    prev=P.shift(1)
    ca=(R<-0.105)&(prev>10)            # moves beyond lower circuit on normal priced stocks = corporate action
    up=(R>0.105)&(prev>10)
    R=R.mask(ca,0).mask(up,0.10)
    R=R.clip(-0.5,0.5)
    I=(1+R.fillna(0)).cumprod().where(P.notna())
    return P,V,R,I
