"""Decode a news.google.com/rss/articles/... link to the publisher URL and fetch text. Usage: idx_gdecode.py LINK"""
import sys, re, json, requests, html
from bs4 import BeautifulSoup
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
def decode(link):
    gid=link.split('/articles/')[1].split('?')[0]
    r=requests.get(f"https://news.google.com/articles/{gid}",headers={"User-Agent":UA},timeout=30)
    sg=re.search(r'data-n-a-sg="([^"]+)"',r.text); ts=re.search(r'data-n-a-ts="([^"]+)"',r.text)
    if not sg: return None
    payload=["Fbv4je",json.dumps(["garturlreq",[["X","X",["X","X"],None,None,1,1,"US:en",None,1,None,None,None,None,None,0,1],"X","X",1,[1,1,1],1,1,None,0,0,None,0],gid,int(ts.group(1)),sg.group(1)]),None,"generic"]
    r2=requests.post("https://news.google.com/_/DotsSplashUi/data/batchexecute",data={"f.req":json.dumps([[payload]])},headers={"User-Agent":UA,"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"},timeout=30)
    m=re.search(r'"garturlres\\",\\"(.*?)\\"',r2.text)
    return m.group(1).replace('\\u003d','=').replace('\\u0026','&') if m else None
def text(u):
    r=requests.get(u,headers={"User-Agent":UA},timeout=40); s=BeautifulSoup(r.text,'html.parser')
    for t in s(['script','style','nav','footer','header']): t.decompose()
    return re.sub(r'\n\s*\n+','\n',s.get_text('\n'))
if __name__=='__main__':
    u=decode(sys.argv[1]); print('URL',u)
    if u and len(sys.argv)>2: print(text(u)[:int(sys.argv[2])])
