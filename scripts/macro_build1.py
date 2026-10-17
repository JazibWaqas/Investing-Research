import pandas as pd
R="data/raw/macro/"; O="data/macro/"
for s,n in [("KSE100","kse100"),("KMI30","kmi30"),("KMIALLSHR","kmiallshr"),("KSE30","kse30"),("ALLSHR","allshr")]:
    d=pd.read_csv(R+f"psx_{s}_hist.csv")
    d=d.drop_duplicates("date").sort_values("date")
    d["value"]=d["close"]
    d[["date","value","open","high","low","close","volume"]].to_csv(O+n+".csv",index=False)
    print(n,len(d),d.date.min(),d.date.max(),d.close.isna().sum())
for id,n in [("DCOILBRENTEU","brent"),("DCOILWTICO","wti")]:
    d=pd.read_csv(R+f"fred_{id}.csv"); d.columns=["date","value"]
    d["value"]=pd.to_numeric(d.value,errors="coerce"); d=d.dropna()
    d.to_csv(O+n+".csv",index=False); print(n,len(d),d.date.min(),d.date.max())
