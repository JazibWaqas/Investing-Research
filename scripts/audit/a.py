import pandas as pd, numpy as np
cpi_vals = """3.85 3.28 2.45 2.13 3.21 3.18 1.81 1.80 1.31 1.59 2.77 3.15
3.36 4.03 3.95 4.17 3.17 3.16 4.17 3.54 3.89 4.21 3.78 3.73
3.66 4.21 4.95 4.81 5.02 3.92 2.95 3.42 3.87 3.84 3.97 4.58
4.38 3.78 3.23 3.63 4.20 5.25 5.80 5.85 5.12 6.78 6.50 6.13
7.20 8.22 9.45 8.85 9.11 8.88 10.36 11.90 12.81 12.22 13.68 13.74
14.89 12.94 11.38 9.09 8.57 9.05 9.28 8.22 9.06 8.95 8.37 7.98
5.64 8.68 9.03 11.08 10.84 9.68 8.44 8.34 8.99 9.18 11.53 12.29
12.94 12.24 12.71 13.37 13.78 21.34 24.92 27.26 23.14 26.54 23.80 24.50
27.56 31.58 35.38 36.42 37.97 29.40 28.28 27.39 31.46 26.92 29.24 29.64
28.35 23.07 20.67 17.35 11.74 12.55 11.10 9.64 6.93 7.07 4.86 4.08
2.42 1.51 0.72 0.26 3.48 3.25 4.06 2.99 5.60 6.25 6.16 5.60
5.79 6.99 7.29 10.91 11.64 11.08 9.20 11.21 10.30""".split()
cpi = pd.Series([float(x) for x in cpi_vals], index=pd.period_range('2015-01', periods=len(cpi_vals), freq='M'))
pr = pd.read_csv('pr.csv', parse_dates=['date']).set_index('date')['rate']
k = pd.read_csv('kse.csv', parse_dates=['date']).set_index('date')['close']
km = k.resample('ME').last(); km.index = km.index.to_period('M')
rate_m = pr.resample('D').ffill().resample('ME').last(); rate_m.index=rate_m.index.to_period('M')
df = pd.DataFrame({'kse':km,'cpi':cpi,'rate':rate_m}).dropna()
df['real'] = df.rate - df.cpi
df['cpi_chg3'] = df.cpi - df.cpi.shift(3)
df['rate_chg6'] = df.rate - df.rate.shift(6)
for h in (6,12): df[f'f{h}'] = (df.kse.shift(-h)/df.kse - 1)*100
df['dd'] = (df.kse/df.kse.cummax()-1)*100
def b(x):
    return 'real>=5' if x>=5 else ('real 0..5' if x>=0 else 'real<0')
df['rb']=df.real.apply(b)
df['infl']=np.where(df.cpi_chg3<=-1,'cpi falling',np.where(df.cpi_chg3>=1,'cpi rising','cpi flat'))
print(df.groupby('rb')[['f6','f12']].agg(['mean','median','count']).round(1))
print(df.groupby('infl')[['f6','f12']].agg(['mean','median','count']).round(1))
print(df.groupby(['rb','infl'])['f12'].agg(['mean','count']).round(1))
df['cutting']=np.where(df.rate_chg6<0,'cutting',np.where(df.rate_chg6>0,'hiking','flat'))
print(df.groupby('cutting')[['f6','f12']].agg(['mean','count']).round(1))
print(df[['kse','cpi','rate','real','cpi_chg3','dd']].tail(6).round(1))
df.to_csv('regime_monthly.csv')
