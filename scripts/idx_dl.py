"""Download URLs (stdin lines) into data/raw/index_pdfs/. Never executes anything."""
import sys, os, requests, urllib.parse
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
D='data/raw/index_pdfs'
for u in [l.strip() for l in sys.stdin if l.strip()]:
    n=urllib.parse.unquote(u.rstrip('/').split('/')[-1].split('?file=')[-1])
    if 'dps.psx.com.pk' in u or '?file=' in u: n='psx_'+n
    p=os.path.join(D,n)
    if os.path.exists(p): continue
    try:
        r=requests.get(u,headers={"User-Agent":UA},timeout=60)
        ok=r.content[:4]==b'%PDF'
        if ok: open(p,'wb').write(r.content)
        print(r.status_code,ok,n)
    except Exception as e: print('ERR',u,e)
