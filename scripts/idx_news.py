"""Google News RSS search. Usage: idx_news.py "query" ... ; prints pubDate | title | source | link"""
import sys, re, requests, html, time, urllib.parse
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
for q in sys.argv[1:]:
    r=requests.get("https://news.google.com/rss/search",params={"q":q,"hl":"en-PK","gl":"PK","ceid":"PK:en"},headers={"User-Agent":UA},timeout=30)
    print("##",q,r.status_code)
    for it in re.findall(r'<item>(.*?)</item>',r.text,re.S):
        g=lambda t:(re.search(rf'<{t}[^>]*>(.*?)</{t}>',it,re.S) or [None,''])[1]
        print(g('pubDate')[5:16],'|',html.unescape(g('title')),'|',g('link'))
    time.sleep(2)
