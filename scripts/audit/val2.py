import pandas as pd, numpy as np
exec(open('valaudit.py').read().split('X=build()')[0])
Xf=pd.read_csv('val_panel_audit.csv',parse_dates=['form'])
test(Xf,'s_val','ret','dyfill lag3',quiet=False)
X4=build(4,True); test(X4,'s_val','ret','dyfill lag4',quiet=False)
print(Xf.sort_values('pret').tail(8)[['t','form','ey','dy','pret','cohort']].round(2).to_string())
print(Xf.sort_values('pret').head(5)[['t','form','ey','dy','pret','cohort']].round(2).to_string())
# winsorized at 1/99 within cohort, and trimmed top 2 per cohort
Xw=Xf.copy(); Xw['retw']=Xw.groupby('cohort').ret.transform(lambda s:s.clip(s.quantile(.05),s.quantile(.95)))
test(Xw,'s_val','retw','winsor 5/95')
# drop 2023H2 cohort and 2024H2 (rerating years) to see dependence
test(Xf[~Xf.cohort.isin(['2023H2','2024H1','2024H2'])],'s_val','ret','excluding 2023H2-2024H2 rerating')
