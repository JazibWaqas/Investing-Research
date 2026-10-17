from load_all import load
P,V,R,I=load()
for n,x in zip('PVRI',(P,V,R,I)): x.to_parquet(f'{n}.parquet')
