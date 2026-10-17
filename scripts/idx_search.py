"""Web search via DDG html then Brave; prints url | snippet. Usage: idx_search.py q1 q2 ..."""
import sys, re, requests, urllib.parse, html, time
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
def ddg(q):
    r=requests.post("https://html.duckduckgo.com/html/",data={"q":q},headers={"User-Agent":UA},timeout=30)
    if r.status_code!=200: return r.status_code,[]
    res=[]
    for m in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',r.text,re.S):
        u=urllib.parse.unquote(re.search(r'uddg=([^&]+)',m.group(1)).group(1)) if 'uddg=' in m.group(1) else m.group(1)
        res.append((u,re.sub('<[^>]+>','',html.unescape(m.group(3)))[:240]))
    return 200,res
for q in sys.argv[1:]:
    for attempt in range(4):
        c,res=ddg(q)
        if c==200: break
        time.sleep(30)
    print("##",q,c,flush=True)
    for u,s in res: print(u,'|',s,flush=True)
    time.sleep(12)
