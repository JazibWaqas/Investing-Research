"""Usage: idx_newsfetch.py "query" "title-regex" maxchars [maxitems]. Searches Google News RSS, decodes matching items, prints article text."""
import sys, re, requests, html, time
sys.path.insert(0,'scripts')
from idx_gdecode import decode, text
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
q,rx,mx=sys.argv[1],sys.argv[2],int(sys.argv[3]); mi=int(sys.argv[4]) if len(sys.argv)>4 else 2
r=requests.get("https://news.google.com/rss/search",params={"q":q,"hl":"en-PK","gl":"PK","ceid":"PK:en"},headers={"User-Agent":UA},timeout=30)
n=0
for it in re.findall(r'<item>(.*?)</item>',r.text,re.S):
    g=lambda t:(re.search(rf'<{t}[^>]*>(.*?)</{t}>',it,re.S) or [None,''])[1]
    ti=html.unescape(g('title'))
    if not re.search(rx,ti,re.I): continue
    print('=====',g('pubDate')[5:16],ti)
    try:
        u=decode(html.unescape(g('link'))); print('URL',u)
        if u: print(text(u)[:mx])
    except Exception as e: print('ERR',e)
    n+=1; time.sleep(2)
    if n>=mi: break
