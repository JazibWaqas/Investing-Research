import re,time,sys,os,json
sys.path.insert(0,'scripts')
from cf import get
t=open('data/raw/macro/mps_list.html',encoding='utf8',errors='ignore').read()
t=re.sub(r'<script.*?</script>','',t,flags=re.S)
out=[]
for h,s in re.findall(r'<a[^>]*href="([^"]+\.pdf)"[^>]*>(.*?)</a>',t,flags=re.S):
    s=re.sub(r'\s+',' ',re.sub('<[^>]+>','',s)).strip()
    if not s or s=='Download' or 'Compendium' in s or 'Information' in s: continue
    m=re.search(r'(20\d\d)',s)
    if m and int(m.group(1))>=2014 and (h,s) not in out: out.append((h,s))
json.dump(out,open('data/raw/macro/mps/index.json','w'))
for h,s in out:
    f='data/raw/macro/mps/'+h.split('/')[-1]
    if os.path.exists(f): continue
    try: open(f,'wb').write(get(h,timeout=60).content)
    except Exception as e: print('ERR',h,e)
    time.sleep(1)
print(len(out))
