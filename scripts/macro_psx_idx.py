import sys; sys.path.insert(0,'scripts')
import psx_api as p
for s in ["KSE100","KMI30","KMIALLSHR","KSE30","ALLSHR"]:
    try:
        e=p.eod(s); print(s,'eod',len(e),e.date.min(),e.date.max())
    except Exception as ex: print(s,'eod fail',ex)
    try:
        h=p.historical_full(s); print(s,'hist',len(h),h.date.min(),h.date.max())
        h.to_csv(f"data/raw/macro/psx_{s}_hist.csv",index=False)
    except Exception as ex: print(s,'hist fail',repr(ex)[:100])
