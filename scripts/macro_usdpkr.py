import openpyxl,pandas as pd
ws=openpyxl.load_workbook('data/raw/macro/bfer.xlsx',data_only=True,read_only=True)['Sheet2']
rows=list(ws.iter_rows(values_only=True))
r=[x for x in rows if x[1] and 'U.S. Dollar' in str(x[1])][0]
d=pd.DataFrame({'date':pd.to_datetime(rows[6][2:],errors='coerce'),'value':pd.to_numeric(r[2:],errors='coerce')}).dropna()
d=d[d.date>='2015-01-01'].sort_values('date')
print(len(d),d.date.min(),d.date.max(),d.value.min(),d.value.max(),d.date.diff().dt.days.max())
print(d.iloc[::500].to_string())
d.to_csv('data/macro/usdpkr.csv',index=False)
