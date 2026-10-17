import json,re,glob,pdfplumber,os
idx=json.load(open('data/raw/macro/mps/index.json'))
res=[]
for h,s in idx:
    f='data/raw/macro/mps/'+h.split('/')[-1]
    try:
        with pdfplumber.open(f) as p: t=" ".join((p.pages[i].extract_text() or "") for i in range(min(2,len(p.pages))))
    except Exception as e: t="ERR "+str(e)
    t=re.sub(r'\s+',' ',t)
    rates=re.findall(r'(?:policy rate|discount rate|target rate)[^.]{0,160}?(\d+(?:\.\d+)?) ?(?:percent|%|per cent)',t,flags=re.I)
    res.append((s,t[:50],rates[:3],t[:700] if not rates else ""))
for r in res: print(r[0],'|',r[2],r[3][:300] if r[3] else "")
