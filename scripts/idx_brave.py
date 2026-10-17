import sys, re, requests, html, time
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
for q in sys.argv[1:]:
    time.sleep(20)
    r=requests.get("https://search.brave.com/search",params={"q":q},headers={"User-Agent":UA},timeout=30)
    print("##",q,r.status_code)
    seen=set()
    for m in re.finditer(r'<a href="(https?://[^"]+)"[^>]*>(.*?)</a>',r.text,re.S):
        u=html.unescape(m.group(1))
        if 'brave.com' in u or u in seen or 'cdn' in u: continue
        seen.add(u)
        t=re.sub(r'<[^>]+>',' ',html.unescape(m.group(2)));t=re.sub(r'\s+',' ',t)[:140]
        print(u,'|',t)
