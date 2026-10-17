import re,sys,os,time
sys.path.insert(0,'scripts')
from cf import get
t=open('data/raw/macro/pbs_ps.html',encoding='utf8',errors='ignore').read()
i=t.find('cpidata1'); j=t.find('// Pagination',i)
for mo,u in re.findall(r'month:\s*"([^"]+)"\s*,\s*review:\s*"([^"]+)"',t[i:j]):
    f='data/raw/macro/pbs/'+mo.replace(' ','_')+'.'+u.rsplit('.',1)[1]
    if os.path.exists(f): continue
    try: open(f,'wb').write(get(u,timeout=40).content)
    except Exception as e: print('ERR',mo,str(e)[:60])
    time.sleep(1)
print(len(os.listdir('data/raw/macro/pbs')))
