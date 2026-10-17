import pandas as pd, numpy as np, glob
sec={'cement':'LUCK DGKC MLCF FCCL CHCC KOHC PIOC ACPL','fert':'FFC EFERT FFBL','ep':'OGDC PPL POL MARI','omc_gas':'PSO APL SNGP SSGC',
'power':'HUBC KAPCO NCPL','isl_bank':'MEBL BIPL','conv_bank':'HBL UBL MCB BAHL','auto':'INDU HCAR PSMC MTL','tech':'SYS TRG AVN NETSOL AIRLINK',
'steel':'ISL ASTL MUGHAL','textile':'NML ILP GATM KTML','pharma':'SEARL AGP GLAXO HINOON','refinery':'ATRL NRL PRL CNERGY','chem':'LCI EPCL ENGRO','food':'FFL UNITY MFL'}
px={}
for s,ts in sec.items():
    for t in ts.split():
        try: d=pd.read_csv(f'eod/{t}.csv',parse_dates=['date']).drop_duplicates('date').set_index('date').close.astype(float)
        except: continue
        r=d.pct_change()
        # strip corporate-action gaps: single-day moves beyond circuit limits
        r[(r<-0.105)&(d.shift(1)>10)]=0; r[r>0.105]=r[r>0.105].clip(upper=0.105)
        px[t]=(r.fillna(0)+1).cumprod()
P=pd.DataFrame(px); M=P.resample('ME').last(); M.index=M.index.to_period('M')
R=M.pct_change()
mapping={t:s for s,ts in sec.items() for t in ts.split()}
S=R.T.groupby(mapping).mean().T  # equal weight sector monthly returns
mkt=R.mean(axis=1)
S.to_csv('sector_monthly_ret.csv'); mkt.to_csv('ew_mkt_ret.csv')
# regime vars
reg=pd.read_csv('regime_monthly.csv',index_col=0); reg.index=pd.PeriodIndex(reg.index,freq='M')
tb=pd.read_csv('tbill6m.csv',index_col=0).squeeze(); tb.index=pd.PeriodIndex(tb.index,freq='M')
df=pd.DataFrame({'cpi_chg3':reg.cpi_chg3,'real':reg.real,'rate':reg.rate}).join(tb.rename('tb6'))
df['curve']=df.tb6-df.rate
df=df.dropna()
idx=(1+S).cumprod(); mi=(1+mkt).cumprod()
fwd=lambda x,h:(x.shift(-h)/x-1)
F6=fwd(idx,6).sub(fwd(mi,6),axis=0)*100  # sector excess vs EW mkt, next 6m
F6m=fwd(mi,6)*100
D=df.join(F6).join(F6m.rename('mkt6'))
D['infl']=np.where(D.cpi_chg3<=-1,'cpi_falling',np.where(D.cpi_chg3>=1,'cpi_rising','cpi_flat'))
D['crv']=np.where(D.curve<=-0.75,'curve_cuts',np.where(D.curve>=0.5,'curve_hikes','curve_flat'))
pd.set_option('display.width',250)
for g in ['infl','crv']:
    t=D.groupby(g)[list(S.columns)+['mkt6']].mean().round(1); t['n']=D.groupby(g).size(); print(t.T)
print(df.tail(4).round(2))
