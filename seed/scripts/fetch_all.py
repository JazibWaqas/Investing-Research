import psxdata, pandas as pd, os, sys, time, warnings, logging
logging.disable(logging.WARNING); warnings.filterwarnings('ignore')
T=[l.strip() for l in open('universe.txt') if l.strip()]
t0=time.time(); n=0
for t in T:
    if os.path.exists(f'eod_all/{t}.csv') or os.path.exists(f'eod_all/{t}.err'): continue
    if time.time()-t0>265: break
    try:
        d=psxdata.stocks(t,start='2016-01-01',end='2026-10-16').sort_values('date')
        d[['date','open','high','low','close','volume']].to_csv(f'eod_all/{t}.csv',index=False)
    except Exception as e:
        open(f'eod_all/{t}.err','w').write(repr(e)[:200])
    n+=1
print('fetched',n,'total',len(os.listdir('eod_all')),'of',len(T))
