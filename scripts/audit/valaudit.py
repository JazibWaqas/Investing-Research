import pandas as pd, numpy as np, statsmodels.formula.api as smf
I=pd.read_parquet('I.parquet'); R=pd.read_parquet('R.parquet'); P=pd.read_parquet('P.parquet')
D0=pd.read_csv('sa_ratios.csv'); D0=D0[D0.date!='TTM'].copy(); D0['date']=pd.to_datetime(D0.date)
print('dy NaN share among pe-valid rows', D0[(D0.pe>0)&(D0.pe<60)].dividendyield.isna().mean().round(2))
D0=D0[D0.pe.notna()&(D0.pe>0)&(D0.pe<60)].sort_values(['t','date'])
sec=pd.read_csv('screener_20261016.csv'); sec['t']=sec.symbol.str.replace(r'X[DB]$','',regex=True); sec=sec.drop_duplicates('t').set_index('t').sector
def px(t,d):
    s=I[t].dropna(); i=s.index.searchsorted(d); return s.iloc[i] if i<len(s) else np.nan
def build(lag=3, dyfill=False):
    out=[]
    for _,r in D0.iterrows():
        form=r.date+pd.DateOffset(months=lag); end=form+pd.DateOffset(months=12)
        if end>I.index[-1] or r.t not in I.columns: continue
        p0,p1,p2=px(r.t,r.date),px(r.t,form),px(r.t,end)
        if np.isnan([p0,p1,p2]).any(): continue
        adj=p0/p1; dyr=r.dividendyield
        if dyfill and pd.isna(dyr): dyr=0
        dy=dyr*adj if pd.notna(dyr) else np.nan
        out.append({'t':r.t,'form':form,'ey':adj/r.pe,'dy':dy,'pb':r.pb,'roe':r.roe,'pret':p2/p1-1,'ret':p2/p1-1+(dy if pd.notna(dy) else 0) if dyfill else p2/p1-1+dy})
    X=pd.DataFrame(out); X['cohort']=X.form.dt.year.astype(str)+np.where(X.form.dt.month<=6,'H1','H2')
    X['s_val']=X.ey+X.dy; X['s_roe_pb']=X.roe/X.pb; X['sector']=X.t.map(sec); return X
def test(X,score,ret='ret',lab='',quiet=True):
    res=[]
    for c,g in X.dropna(subset=[score,ret]).groupby('cohort'):
        if len(g)<12: continue
        g=g.copy(); g['q']=pd.qcut(g[score].rank(method='first'),3,labels=['low','mid','high'])
        m=g.groupby('q',observed=True)[ret].mean(); md=g.groupby('q',observed=True)[ret].median()
        res.append({'cohort':c,'n':len(g),'spread':m['high']-m['low'],'medspread':md['high']-md['low'],'ew':g[ret].mean(),'ic':g[score].corr(g[ret],method='spearman')})
    T=pd.DataFrame(res)
    print(f"{lab:38s} {score:9s} {ret:5s} cohorts={len(T)} N={T.n.sum():4d} meanSpread {T.spread.mean()*100:6.1f} medianOfSpreads {T.spread.median()*100:6.1f} spreadOfMedians {T.medspread.mean()*100:6.1f} pos {(T.spread>0).sum()}/{len(T)} worst {T.spread.min()*100:6.1f} IC {T.ic.mean():.2f}")
    if not quiet: print(T.round(3).to_string(index=False))
    return T
X=build()
print('rows',len(X),'tickers',X.t.nunique(),'per cohort', X.groupby('cohort').size().to_dict())
T=test(X,'s_val',lab='BASELINE',quiet=False); test(X,'s_roe_pb',lab='BASELINE')
print('corr(spread, cohort EW return) s_val:', round(T.spread.corr(T.ew),2))
test(X,'s_val','pret','price only (no dy added)'); test(X,'ey','ret','EY alone, drift-adj, ret incl dy'); test(X,'ey','pret','EY alone, price only')
test(X,'s_roe_pb','pret','ROE/PB price only')
Xf=build(dyfill=True); test(Xf,'s_val',lab='DY NaN->0 (non-payers kept)'); test(Xf,'s_val','pret','DY NaN->0, price only'); test(Xf,'ey','pret','DY NaN->0 sample, EY price only')
for lag in (4,5): Xl=build(lag,dyfill=True); test(Xl,'s_val',lab=f'lag {lag}m, dy fill'); test(Xl,'ey','pret',f'lag {lag}m, EY price only')
# non-overlapping: H2 only (June FY, Sep->Sep) and H1 only
for h in ('H1','H2'): test(Xf[Xf.cohort.str.endswith(h)],'s_val',lab=f'only {h} cohorts dy fill')
# panel regression with cohort fixed effects: ret on within-cohort pct rank
for sc in ('s_val','ey','s_roe_pb'):
    Z=Xf.dropna(subset=[sc]).copy(); Z['rk']=Z.groupby('cohort')[sc].rank(pct=True)-0.5
    Z=Z[Z.groupby('cohort').t.transform('size')>=12]
    for y in ('ret','pret'):
        m=smf.ols(f'{y} ~ rk + C(cohort)',Z).fit(cov_type='cluster',cov_kwds={'groups':pd.factorize(Z.t)[0]})
        m2=smf.ols(f'{y} ~ rk + C(cohort)',Z).fit(cov_type='cluster',cov_kwds={'groups':pd.factorize(Z.cohort)[0]})
        print(f'FE reg {sc:8s} {y:4s} n={int(m.nobs)} slope(top-bottom rank)={m.params.rk*100:6.1f}pts t(cl ticker)={m.tvalues.rk:5.2f} t(cl cohort)={m2.tvalues.rk:5.2f}')
    # sector-neutral: rank within cohort x sector, demeaned return by cohort x sector
    Z=Z.dropna(subset=['sector']); Z['g']=Z.cohort+Z.sector.astype(str)
    Z=Z[Z.groupby('g').t.transform('size')>=3]
    Z['rks']=Z.groupby('g')[sc].rank(pct=True)-0.5
    m=smf.ols('pret ~ rks + C(g)',Z).fit(cov_type='cluster',cov_kwds={'groups':pd.factorize(Z.t)[0]})
    print(f'  sector-neutral {sc:8s} pret n={int(m.nobs)} slope={m.params.rks*100:6.1f}pts t={m.tvalues.rks:5.2f}')
# beta control: 250d beta vs EW market before formation
mk=R.mean(axis=1)
def beta(t,d):
    r=R[t].loc[:d].tail(250); m=mk.loc[r.index]; ok=r.notna()
    return np.cov(r[ok],m[ok])[0,1]/m[ok].var() if ok.sum()>100 else np.nan
Xf['beta']=[beta(t,d) for t,d in zip(Xf.t,Xf.form)]
Z=Xf.dropna(subset=['s_val','beta']).copy(); Z['rk']=Z.groupby('cohort').s_val.rank(pct=True)-0.5
print('corr(rank value, beta)',round(Z.rk.corr(Z.beta),2))
m=smf.ols('pret ~ rk + beta + C(cohort)',Z).fit(cov_type='cluster',cov_kwds={'groups':pd.factorize(Z.t)[0]}); print(f'with beta control slope={m.params.rk*100:.1f} t={m.tvalues.rk:.2f} beta coef={m.params.beta*100:.1f}')
Xf.to_csv('val_panel_audit.csv',index=False)
