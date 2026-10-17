import pandas as pd, numpy as np
from load_all import load
P,V,R,I=load()
D=pd.read_csv('sa_ratios.csv'); D=D[D.date!='TTM'].copy(); D['date']=pd.to_datetime(D.date)
D=D[D.pe.notna()&(D.pe>0)&(D.pe<60)]
D=D.sort_values(['t','date'])
D['med_pe_prior']=D.groupby('t').pe.transform(lambda s: s.expanding().median().shift(1))
def px(t,d):
    if t not in I.columns: return np.nan
    s=I[t].dropna(); i=s.index.searchsorted(d)
    return s.iloc[i] if i<len(s) else np.nan
out=[]
for _,r in D.iterrows():
    form=r.date+pd.DateOffset(months=3); end=form+pd.DateOffset(months=12)
    if end>I.index[-1] or r.t not in I.columns: continue
    p0=px(r.t,r.date); p1=px(r.t,form); p2=px(r.t,end)
    if np.isnan([p0,p1,p2]).any(): continue
    adj=p0/p1  # price drift since FY end
    ey=(1/r.pe)*adj; dy=(r.dividendyield or 0)*adj
    pe_now=r.pe/adj
    rer=np.log(r.med_pe_prior/pe_now)/2.5 if pd.notna(r.med_pe_prior) else np.nan
    out.append({'t':r.t,'fy':r.date,'form':form,'ey':ey,'dy':dy,'pb':r.pb,'roe':r.roe,'rer':rer,'ret':p2/p1-1+dy})
X=pd.DataFrame(out)
X['cohort']=X.form.dt.year.astype(str)+np.where(X.form.dt.month<=6,'H1','H2')
X['s_val']=X.ey+X.dy
X['s_er']=X.dy+X.rer        # our method sans growth term
X['s_roe_pb']=X.roe/X.pb
def test(score):
    res=[]
    for c,g in X.dropna(subset=[score]).groupby('cohort'):
        if len(g)<12: continue
        g=g.copy(); g['q']=pd.qcut(g[score].rank(method='first'),3,labels=['low','mid','high'])
        m=g.groupby('q',observed=True).ret.mean()
        res.append({'cohort':c,'n':len(g),'low':m['low'],'high':m['high'],'spread':m['high']-m['low'],'rankIC':g[score].corr(g.ret,method='spearman')})
    T=pd.DataFrame(res)
    print(f"\n== {score} ==\n", T.round(3).to_string(index=False))
    print(f" mean spread high-low {T.spread.mean()*100:.1f}pts, positive in {(T.spread>0).sum()}/{len(T)} cohorts, mean rankIC {T.rankIC.mean():.2f}")
for s in ['s_val','s_er','s_roe_pb','dy']: test(s)
X.to_csv('valtest_panel.csv',index=False)
