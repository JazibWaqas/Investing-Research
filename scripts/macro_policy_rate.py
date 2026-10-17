"""Policy-rate decisions 2015+. Meeting/announcement dates: SBP MPS titles (2020+) or the date printed in the
MPS PDF (2015-19). Rates: seed pr.csv gives effective dates of changes; a change belongs to the meeting
announced within 7 days before it. Holds carry the prior rate."""
import json,re,pandas as pd,pdfplumber
M="January|February|March|April|May|June|July|August|September|October|November|December"
idx=json.load(open('data/raw/macro/mps/index.json'))
meet=[]  # (date, source)
for h,s in idx:
    u="https://www.sbp.org.pk/assets/document/publications/"+h.split('/')[-1]
    m=re.search(r'((?:%s|[A-Z][a-z]{2}) \d{1,2}, 20\d\d)'%M,s)
    if m: d=pd.to_datetime(m.group(1)); 
    else:
        if not re.search(r'201[5-9]',s): continue
        with pdfplumber.open('data/raw/macro/mps/'+h.split('/')[-1]) as p:
            t=re.sub(r'\s+',' '," ".join((pg.extract_text() or "") for pg in p.pages[:6]))
        f=re.findall(r'(?:%s) \d{1,2}, 20\d\d'%M,t); 
        mon=re.search(r'(%s|[A-Z][a-z]{2}[a-z]*) (20\d\d)'%M,s)
        cand=[pd.to_datetime(x) for x in f]
        cand=[c for c in cand if c.strftime('%b')==pd.to_datetime(mon.group(1)[:3]+' 2000').strftime('%b') and c.year==int(mon.group(2))]
        if cand: d=cand[0]
        else: d=None
    meet.append([d,u,s])
# month-only fallbacks (exact day not printed in the PDF): month end, flagged
fix={"Monetary Policy Statement - Jan 2018":"2018-01-29","Monetary Policy Statement - July 2015":"2015-07-31","Monetary Policy Statement - Jan 2015":"2015-01-31"}
for r in meet:
    if r[0] is None:
        r[0]=pd.to_datetime(fix[r[2]]); r[2]+=" [exact day not in PDF; date approximate]"
    elif "2015" in r[2] and "Mar" in r[2]: pass
meet=[r for r in meet if r[0]>=pd.Timestamp("2015-01-01")]
df=pd.DataFrame(meet,columns=["date","source","t"]).drop_duplicates("date").sort_values("date").reset_index(drop=True)
seed=pd.read_csv('seed/data/macro/pr.csv',parse_dates=['date'])
init=[(pd.Timestamp("2015-01-01"),9.5),(pd.Timestamp("2015-01-31"),8.5)]
# Mar 2015 PDF: -50bp from 8.5 to 8.0 (effective date not in seed, so key it to the meeting date)
chg=pd.concat([pd.DataFrame(init,columns=["date","rate"]),pd.DataFrame([(pd.Timestamp("2015-03-21"),8.0)],columns=["date","rate"]),seed]).sort_values("date")
rates=[];prev=9.5
used=set()
for _,r in df.iterrows():
    w=chg[(chg.date>=r.date-pd.Timedelta(days=1))&(chg.date<=r.date+pd.Timedelta(days=7))&(chg.date>pd.Timestamp("2015-01-01"))]
    if len(w): new=w.rate.iloc[-1]; used.update(w.index) if False else None
    else: new=prev
    rates.append((new,round((new-prev)*100)));prev=new
df["rate"]=[a for a,b in rates]; df["change_bp"]=[b for a,b in rates]
df["decision"]=df.change_bp.map(lambda x:"cut" if x<0 else "hike" if x>0 else "hold")
df["source"]=df.source
unm=[d.date() for d in seed.date if not ((df.date<=d)&(df.date>=d-pd.Timedelta(days=7))).any()]
print("seed changes with no meeting:",unm)
df[["date","rate","change_bp","decision","source"]].to_csv('data/macro/policy_rate_decisions.csv',index=False)
print(df[["date","rate","change_bp","decision"]].to_string())
