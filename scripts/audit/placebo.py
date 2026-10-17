import pandas as pd, numpy as np
exec(open('ops.py').read().split('# 1 accumulation')[0].replace("print('tickers'","pass#"))
for n in ['acc','brk','pump','mom']:
    E=pd.read_csv(f'ev_{n}.csv'); print(n,'n',len(E),'tickers',E.t.nunique(),'med60',round(E.x60.median()*100,1),'win60',round((E.x60>0).mean()*100),'mean60',round(E.x60.mean()*100,1),'| med20',round(E.x20.median()*100,1),'mean20',round(E.x20.mean()*100,1))
# placebo: every eligible stock-day (liq2 & P>=5), cooldown 20, same study()
rng=np.random.default_rng(0)
base=liq2&(P>=5)
rand=base&pd.DataFrame(rng.random(base.shape)<0.05,index=base.index,columns=base.columns)
Ep=study(rand,'PLACEBO random liquid days')
print('placebo med60',round(Ep.x60.median()*100,1),'win60',round((Ep.x60>0).mean()*100))
# same placebo excluding pre-signal condition but restricted to stocks that ever pumped
pumped=pd.read_csv('ev_pump.csv').t.unique()
Ep2=study(rand[pumped],'PLACEBO random days, pump-prone names')
print('placebo2 med60',round(Ep2.x60.median()*100,1),'win60',round((Ep2.x60>0).mean()*100))
