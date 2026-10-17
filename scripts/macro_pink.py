import pandas as pd, openpyxl
ws=openpyxl.load_workbook("data/raw/macro/pinksheet.xlsx",data_only=True,read_only=True)["Monthly Prices"]
rows=list(ws.iter_rows(values_only=True)); hdr=[str(c).strip() if c else "" for c in rows[4]]
hdr[0]="m"; d=pd.DataFrame(rows[6:],columns=hdr)
d["date"]=pd.to_datetime(d.m.astype(str).str.replace("M","-")+"-01",errors="coerce")
d=d[d.date>="2015-01-01"]
for col,n in [("Coal, South African **","coal_rb"),("Coal, Australian","coal_newcastle"),("Urea","urea"),("DAP","dap"),("Cotton, A Index","cotton"),("Palm oil","palm_oil"),("Iron ore, cfr spot","iron_ore")]:
    c=[h for h in hdr if h.startswith(col)][0]
    s=pd.DataFrame({"date":d.date,"value":pd.to_numeric(d[c],errors="coerce")}).dropna()
    s.to_csv(f"data/macro/{n}.csv",index=False); print(n,c,len(s),s.date.min().date(),s.date.max().date(),s.value.iloc[-1])
