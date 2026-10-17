import pandas as pd, openpyxl
ws=openpyxl.load_workbook("data/raw/macro/tb.xlsx",data_only=True)["New Detailed Format"]
rows=[(r[1],r[3],r[14],r[15],r[16]) for r in ws.iter_rows(min_row=7,values_only=True) if r[3] is not None and r[1]]
d=pd.DataFrame(rows,columns=["tenor","date","price","cutoff","wavg"])
print(d.tenor.value_counts())
d["date"]=pd.to_datetime(d.date,errors="coerce"); d["cutoff"]=pd.to_numeric(d.cutoff,errors="coerce")*100
d["tenor"]=d.tenor.str.extract(r"(\d+)")[0]+"m"
d=d[d.date>="2015-01-01"]
p=d.pivot_table(index="date",columns="tenor",values="cutoff",aggfunc="first").reset_index()
p=p.rename(columns={"3m":"y3m","6m":"y6m","12m":"y12m"})[["date","y3m","y6m","y12m"]].round(4)
p.to_csv("data/macro/tbill_auctions.csv",index=False)
print(len(p),p.date.min(),p.date.max()); print(p.tail(4)); print(p.isna().sum())
