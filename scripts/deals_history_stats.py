"""Summary statistics for data/deals_history.csv (printed; copy into knowledge/playbooks/deals.md)."""
import pandas as pd, numpy as np
df = pd.read_csv("data/deals_history.csv")
tk = df[df.type == "takeover"]
def st(x, label):
    x = x.dropna()
    if len(x) == 0: print(f"{label}: n=0"); return
    print(f"{label}: n={len(x)} mean={x.mean():+.1%} median={x.median():+.1%} win={ (x>0).mean():.0%} worst={x.min():+.1%} best={x.max():+.1%}")
print("takeover PAIs", len(tk)); print(tk.status.value_counts().to_string())
print("by year of PAI:"); print(pd.to_datetime(tk.pai_date).dt.year.value_counts().sort_index().to_string())
res = tk[tk.status.isin(["completed", "withdrawn", "lapsed"])]
print("resolved", len(res), "completed share of resolved", (res.status == "completed").mean())
nonpend = tk[tk.status != "pending"]
print("completed share of non-pending (unknown counted as not completed)", (nonpend.status == "completed").mean(), len(nonpend))
c = tk[tk.status == "completed"]
print("days PAI->completion: n", c.days_pai_to_end.notna().sum(), "median", c.days_pai_to_end.median(), "range", c.days_pai_to_end.min(), c.days_pai_to_end.max())
nc = tk[tk.status.isin(["withdrawn", "lapsed"])]
print("days PAI->withdrawal/lapse: median", nc.days_pai_to_end.median(), "n", len(nc))
pr = tk[(tk.status.isin(["completed", "lapsed"])) & tk.premium_to_pre_pai.notna()]
st(pr.premium_to_pre_pai, "premium of offer to pre-PAI close (completed+lapsed, offer known)")
pc = c[c.premium_to_pre_pai.notna()]
st(pc.premium_to_pre_pai, "premium, completed only")
print("--- returns, buy close day after PAI, hold to completion/withdrawal/lapse (price return, bonus-adjusted when in panel)")
r = res.copy()
st(r.ret_pai_entry_to_end, "ALL resolved")
st(r[r.status == "completed"].ret_pai_entry_to_end, "completed")
st(r[r.status != "completed"].ret_pai_entry_to_end, "withdrawn/lapsed")
st(r[r.kmi_at_time.isin(["KMI30", "KMI All Share"])].ret_pai_entry_to_end, "KMI (30 or All Share) at the time, all resolved")
st(r[r.kmi_at_time.isin(["KMI30", "KMI All Share"]) & (r.status == "completed")].ret_pai_entry_to_end, "KMI, completed")
st(r[r.gap_flag == 0].ret_pai_entry_to_end, "no >12% daily gap in window")
r2 = r[r.bench_kse100pr_ret.notna()]
st(r2.ret_pai_entry_to_end - r2.bench_kse100pr_ret, "excess vs KSE100PR (same window; 2020-04 on)")
st(r2.bench_kse100pr_ret, "KSE100PR itself over the same windows")
cc = c[c.bench_kse100pr_ret.notna()]
st(cc.ret_pai_entry_to_end - cc.bench_kse100pr_ret, "excess vs KSE100PR, completed")
print("--- PAO day-after entry")
st(c.ret_pao_entry_to_end, "completed, buy day after PAO")
st(c[c.kmi_at_time.isin(["KMI30", "KMI All Share"])].ret_pao_entry_to_end, "completed, KMI, buy day after PAO")
cp = c[c.ret_pao_entry_to_end.notna() & c.bench_kse100pr_ret.notna()]
print("PAO-entry deals with no PAO date or missing:", c.ret_pao_entry_to_end.isna().sum(), "of", len(c))
print("--- full-tender upper bound (offer / day-after-PAI close - 1), completed with offer")
st(c.ret_offer_if_tendered_full, "tendered fully at offer")
print("--- after completion")
c = c.copy()
c["m1"] = c.price_1m_after_completion / c.offer_price - 1; c["m6"] = c.price_6m_after / c.offer_price - 1
st(c.m1, "price 1m after completion vs offer"); st(c.m6, "price 6m after completion vs offer")
print("--- delistings")
dl = df[df.type == "delisting"]
st(dl.ret_pai_entry_to_end, "delisting: buy day after first filing, tender at PSX-set price")
dl2 = dl.copy(); dl2["pre_to_exit"] = dl2.offer_price / dl2.pre_pai_close - 1
st(dl2.pre_to_exit, "delisting: pre-filing close to buy-back price")
print("days", dl.days_pai_to_end.median())
print("--- by PAI year, resolved returns")
r = r.assign(y=pd.to_datetime(r.pai_date).dt.year)
print(r.groupby("y").ret_pai_entry_to_end.agg(["count", "median", "mean"]).round(3).to_string())
print("--- status among 2018-2020 vs 2021+")
tk2 = tk.assign(era=np.where(pd.to_datetime(tk.pai_date) < "2021-01-01", "2018-20", "2021+"))
print(pd.crosstab(tk2.era, tk2.status).to_string())
print("--- KMI mix of PAIs"); print(tk.kmi_at_time.value_counts().to_string())
print(c[["target","pai_date","offer_price","entry_pai_close","ret_pai_entry_to_end","ret_offer_if_tendered_full","ret_pao_entry_to_end"]].to_string())
