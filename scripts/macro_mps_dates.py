import json,re,pdfplumber
idx=json.load(open('data/raw/macro/mps/index.json'))
M="January|February|March|April|May|June|July|August|September|October|November|December"
for h,s in idx:
    if not re.search(r'201[4-9]',s): continue
    f='data/raw/macro/mps/'+h.split('/')[-1]
    with pdfplumber.open(f) as p:
        t=" ".join((pg.extract_text() or "") for pg in p.pages[:6])
    t=re.sub(r'\s+',' ',t)
    d=re.findall(r'(?:%s) \d{1,2}, 20\d\d'%M,t)
    print(s,'|',d[:3])
