"""informed_capital: do news-less rises on PSX precede filings, and does joining them pay?

Run: .venv/Scripts/python.exe scripts/tests/informed_capital.py > tests/out/informed_capital.txt
Input: data/daily_table.parquet (features at close of t, outcomes from next open), data/announcements.parquet.
Net return = gross minus 0.5% round trip, minus another 0.5% when the 60-session median traded value is under Rs20m.
Exits: time exits T5, T10, T20, T60 (table ret_fwd_k) and a 20% trailing stop on closes (trail20, cap 120 sessions)
rebuilt from the table's own returns. Placebo: random rows from the same date and liquidity tier, same exit.
"""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
R = r"C:\Users\JazibWaqas\Documents\GitHub\Investing-Research"
rng = np.random.default_rng(7)
B = 500
SPLIT = pd.Timestamp("2026-09-01")
C5 = ["financial_result", "material_info", "dividend_or_bonus", "insider_trade", "board_meeting_notice"]
EXITS = ["T5", "T10", "T20", "T60", "trail20"]

d = pd.read_parquet(R + r"\data\daily_table.parquet")
d["year"] = d["year"].astype(int)
d = d.sort_values(["symbol", "session_idx"]).reset_index(drop=True)
N = len(d)
code = d.symbol.astype("category").cat.codes.values.astype(np.int64)
sess = d.session_idx.values.astype(np.int64)
key = code * 100000 + sess
date = d.date.values
dcode = pd.factorize(d.date)[0]
ym = (d.date.dt.year * 12 + d.date.dt.month).values
tvm = d.traded_value_median_60.values.astype(float)
tier = np.where(np.isnan(tvm), -1, np.where(tvm >= 20e6, 0, np.where(tvm >= 5e6, 1, 2)))  # 0 >20m, 1 5-20m, 2 <5m
TN = {0: "A >Rs20m", 1: "B Rs5-20m", 2: "C <Rs5m"}
cost = np.where(tier < 0, np.nan, 0.005 + 0.005 * (tvm < 20e6))
print("=== 0. SETUP AND VALIDATION ===")
print(f"rows {N}, symbols {code.max()+1}, dates {d.date.nunique()}, {d.date.min().date()} to {d.date.max().date()}")

# adjusted price index from ret_1d (consecutive traded rows), used for ret_10d, the trailing stop and news paths
lr = np.log1p(np.clip(d.ret_1d.fillna(0).values.astype(float), -0.999, None))
pidx = np.exp(pd.Series(lr).groupby(code).cumsum().values)


def back(k):
    q = code * 100000 + sess - k
    pos = np.searchsorted(key, q, "right") - 1
    ok = (pos >= 0) & (code[np.clip(pos, 0, N - 1)] == code)
    return pos, ok


def retk(k):
    pos, ok = back(k)
    return np.where(ok, pidx / pidx[np.clip(pos, 0, N - 1)] - 1, np.nan)


r5 = retk(5)
m = ~np.isnan(r5) & d.ret_5d.notna().values
dif = np.abs(r5[m] - d.ret_5d.values[m])
print(f"ret_5d rebuilt from ret_1d chain vs table: median abs diff {np.median(dif):.5f}, share within 0.5pt {np.mean(dif<0.005):.4f}, n {m.sum()}")
r10 = retk(10)
d["ret_10d"] = r10
rr20 = retk(20)
m = ~np.isnan(rr20) & d.ret_20d.notna().values
dif = np.abs(rr20[m] - d.ret_20d.values[m])
print(f"ret_20d rebuilt vs table: median abs diff {np.median(dif):.5f}, share within 0.5pt {np.mean(dif<0.005):.4f}")

# entry row and entry-open on the pidx scale
nx = np.arange(N) + 1
has_next = np.zeros(N, bool)
has_next[:-1] = code[1:] == code[:-1]
nxc = np.minimum(nx, N - 1)
ooc = d.ret_open_to_close.values.astype(float)
open_e = np.where(has_next, pidx[nxc] / (1 + ooc[nxc]), np.nan)
ul = d.upper_lock.values.astype(bool)
entry_locked = np.where(has_next, ul[nxc], False)

# trailing stop: first close <= 80% of highest close since entry; cap 120 sessions
alive = has_next & ~np.isnan(open_e)
peak = np.full(N, -np.inf)
exit_v = np.full(N, np.nan)
last = np.full(N, np.nan)
for j in range(1, 121):
    rrow = np.arange(N) + j
    valid = rrow < N
    rc = np.minimum(rrow, N - 1)
    valid &= (code[rc] == code) & (sess[rc] - sess <= 120)
    c = np.where(valid, pidx[rc], np.nan)
    upd = alive & valid
    peak = np.where(upd, np.maximum(peak, c), peak)
    hit = upd & (c <= 0.8 * peak)
    exit_v[hit] = c[hit]
    alive = alive & ~hit
    last = np.where(upd, c, last)
exit_v[alive] = last[alive]
maxs = sess.max()
sym_last = pd.Series(sess).groupby(code).transform("max").values
censored = alive & (sess + 120 > maxs) & (sym_last >= maxs - 20)
tr20 = exit_v / open_e - 1
tr20[censored] = np.nan
print(f"trail20: capped/ended-without-stop {int(alive.sum())}, censored at end of data (set null) {int(censored.sum())}")
# check: pidx path against table ret_fwd_5 (close t+5 over next open) on rows whose t+5 row exists
pos5 = np.searchsorted(key, key + 5, "right") - 1
okk = (pos5 > np.arange(N)) & (code[np.clip(pos5, 0, N - 1)] == code) & (sess[np.clip(pos5, 0, N - 1)] == sess + 5) & ~np.isnan(open_e)
mine = pidx[np.clip(pos5, 0, N - 1)] / open_e - 1
tb = d.ret_fwd_5.values.astype(float)
mm = okk & ~np.isnan(tb)
print(f"entry-open scale check, ret_fwd_5 vs rebuilt: median abs diff {np.median(np.abs(mine[mm]-tb[mm])):.5f}, share within 0.5pt {np.mean(np.abs(mine[mm]-tb[mm])<0.005):.4f}, n {mm.sum()}")

GROSS = {f"T{k}": d[f"ret_fwd_{k}"].values.astype(float) for k in (5, 10, 20, 60)}
GROSS["trail20"] = tr20
NET = {k: v - cost for k, v in GROSS.items()}
tier_ok = tier >= 0

# ---------------- signal definitions ----------------
dsl = d.days_since_last_filing.values.astype(float)
sref = d.sector_ret_5d.fillna(d.index_ret_5d).values.astype(float)
r5t = d.ret_5d.values.astype(float)
r10t = r10
VAR = {}
for sec in (False, True):
    sfx = "f" if sec else ""
    VAR[f"R1{sfx}"] = ((r5t > 0.08) & (dsl > 10) & ((sref < 0.03) if sec else True), 10, "rise: ret_5d>8%, no filing in 10")
    VAR[f"R2{sfx}"] = ((r5t > 0.08) & (dsl > 5) & ((sref < 0.03) if sec else True), 5, "rise: ret_5d>8%, no filing in 5")
    VAR[f"R3{sfx}"] = ((r10t > 0.12) & (dsl > 20) & ((sref < 0.03) if sec else True), 20, "rise: ret_10d>12%, no filing in 20")
    VAR[f"F1{sfx}"] = ((r5t < -0.08) & (dsl > 10) & ((sref > -0.03) if sec else True), 10, "fall: ret_5d<-8%, no filing in 10")
    VAR[f"F2{sfx}"] = ((r5t < -0.08) & (dsl > 5) & ((sref > -0.03) if sec else True), 5, "fall: ret_5d<-8%, no filing in 5")
    VAR[f"F3{sfx}"] = ((r10t < -0.12) & (dsl > 20) & ((sref > -0.03) if sec else True), 20, "fall: ret_10d<-12%, no filing in 20")
VAR = {k: (np.asarray(v[0], bool) & ~np.isnan(dsl), v[1], v[2]) for k, v in VAR.items()}
chk = VAR["R1f"][0]
tab = d.is_newsless_rise.fillna(False).values.astype(bool)
print(f"R1f vs table is_newsless_rise: mine {chk.sum()}, table {tab.sum()}, both {(chk&tab).sum()}")


def episodes(mask, gap=20):
    out = []
    idx = np.where(mask)[0]
    cur_c, cur_s = -1, -10**9
    for i in idx:
        if code[i] != cur_c or sess[i] - cur_s >= gap:
            out.append(i)
            cur_c, cur_s = code[i], sess[i]
    return np.array(out, dtype=int)


EP = {k: episodes(v[0]) for k, v in VAR.items()}

# announcements -> filing sessions
a = pd.read_parquet(R + r"\data\announcements.parquet")
a = a[a.klass.isin(C5 + ["agm", "credit_rating", "other"])].copy()
a["dt"] = pd.to_datetime(a.datetime, utc=True).dt.tz_convert("Asia/Karachi")
a["dd"] = a.dt.dt.tz_localize(None).dt.normalize()
a["late"] = (a.dt.dt.hour * 60 + a.dt.dt.minute) > 15 * 60 + 30
cal = d[["date", "session_idx"]].drop_duplicates().sort_values("date")
cald = cal.date.values
cals = cal.session_idx.values
pl = np.searchsorted(cald, a.dd.values, "left")
pr = np.searchsorted(cald, a.dd.values, "right")
pp = np.where(a.late.values, pr, pl)
okp = pp < len(cald)
a = a[okp].copy()
a["sess"] = cals[pp[okp]]
a["fdate"] = cald[pp[okp]]
sc = {s: i for i, s in enumerate(d.symbol.astype("category").cat.categories)}
a = a[a.symbol.isin(sc)].copy()
a["code"] = a.symbol.map(sc)
a5 = a[a.klass.isin(C5)].sort_values(["code", "sess", "dt"]).reset_index(drop=True)
akey = a5.code.values.astype(np.int64) * 100000 + a5.sess.values.astype(np.int64)


def first_filing(i_rows, W):
    q = code[i_rows] * 100000 + sess[i_rows]
    pos = np.searchsorted(akey, q, "right")
    posc = np.minimum(pos, len(akey) - 1)
    ok = (pos < len(akey)) & (akey[posc] <= q + W)
    return np.where(ok, posc, -1)


# ---------------- 1. counts ----------------
print("\n=== 1. SIGNAL COUNTS (episode = first signal day, then 20-session re-arm per name) ===")
print(f"{'variant':7}{'definition':44}{'signal-days':>12}{'episodes':>9}{'names':>7}{'dates':>7}{'tierOK':>8}{'IS':>7}{'OOS':>5}")
for k, (m_, thr, desc) in VAR.items():
    e = EP[k]
    print(f"{k:7}{desc:44}{m_.sum():12d}{len(e):9d}{len(set(code[e])):7d}{len(set(dcode[e])):7d}{int(tier_ok[e].sum()):8d}{int((d.date.values[e]<np.datetime64(SPLIT)).sum()):7d}{int((d.date.values[e]>=np.datetime64(SPLIT)).sum()):5d}")

# ---------------- 2. filing shares vs base ----------------
print("\n=== 2. SHARE FOLLOWED BY A FILING vs BASE (same symbol-month) ===")
print("obs = share of episodes with a filing in sessions t+1..t+w; baseA = mean over the same symbols' rows in the same months of the same indicator (unconditional);")
print("baseB = same but only rows that also had no filing in the variant's lookback (days_since_last_filing above the same threshold); expA/expB expected count under each base; z against the base (Poisson-binomial).")
gkey = code * 10000 + (ym - 2017 * 12)
IND = {}
for w in (5, 10, 20):
    for c in C5 + ["total"]:
        IND[(w, c)] = (d[f"filing_within_{w}_{c}"] > 0).astype(float).where(d[f"filing_within_{w}_{c}"].notna())
    s5 = sum(d[f"filing_within_{w}_{c}"] for c in C5)
    IND[(w, "any of 5")] = (s5 > 0).astype(float).where(s5.notna())
indf = pd.DataFrame({f"{w}|{c}": v for (w, c), v in IND.items()})
indf["g"] = gkey
BASE_ALL = indf.groupby("g").mean()
BASE_ST = {}
for thr in (5, 10, 20):
    msk = (dsl > thr)
    BASE_ST[thr] = indf[msk].groupby("g").mean()


def share_table(vk):
    m_, thr, desc = VAR[vk]
    e = EP[vk]
    print(f"\n-- {vk}: {desc}; episodes {len(e)}")
    for w in (5, 10, 20):
        print(f" window {w} sessions" + " " * 12 + f"{'n':>6}{'obs%':>7}{'baseA%':>8}{'liftA':>7}{'zA':>7}{'baseB%':>8}{'liftB':>7}{'zB':>7}")
        for c in C5 + ["total", "any of 5"]:
            col = f"{w}|{c}"
            obs = indf[col].values[e]
            bA = BASE_ALL[col].reindex(gkey[e]).values
            bB = BASE_ST[thr][col].reindex(gkey[e]).values
            ok = ~np.isnan(obs) & ~np.isnan(bA) & ~np.isnan(bB)
            if ok.sum() == 0:
                continue
            o = obs[ok]
            A, Bb = bA[ok], bB[ok]
            zA = (o.sum() - A.sum()) / np.sqrt((A * (1 - A)).sum()) if (A * (1 - A)).sum() > 0 else np.nan
            zB = (o.sum() - Bb.sum()) / np.sqrt((Bb * (1 - Bb)).sum()) if (Bb * (1 - Bb)).sum() > 0 else np.nan
            print(f"   {c:26}{ok.sum():6d}{o.mean()*100:7.1f}{A.mean()*100:8.1f}{o.mean()/A.mean() if A.mean()>0 else np.nan:7.2f}{zA:7.1f}{Bb.mean()*100:8.1f}{o.mean()/Bb.mean() if Bb.mean()>0 else np.nan:7.2f}{zB:7.1f}")


for vk in VAR:
    share_table(vk)

# ---------------- 3. return paths with placebo ----------------
def mkpool(keyarr, net, extra=None):
    ok = ~np.isnan(net) & tier_ok
    if extra is not None:
        ok &= extra
    s = pd.Series(net[ok]).groupby(keyarr[ok]).apply(np.asarray)
    return s.to_dict()


DK = dcode * 4 + tier
POOL = {x: mkpool(DK, NET[x]) for x in EXITS}
POOLD = {x: mkpool(dcode, NET[x]) for x in EXITS}


def draw(rows, x):
    M = np.full((len(rows), B), np.nan)
    fb = 0
    for n, i in enumerate(rows):
        p = POOL[x].get(DK[i])
        if p is None or len(p) < 5:
            p = POOLD[x].get(dcode[i])
            fb += 1
        if p is None or len(p) == 0:
            continue
        M[n] = p[rng.integers(0, len(p), B)]
    return M, fb


def st(v):
    v = v[~np.isnan(v)]
    if len(v) == 0:
        return None
    return (len(v), v.mean() * 100, np.median(v) * 100, (v > 0).mean() * 100, (v > 0.10).mean() * 100, (v > 0.5).mean() * 100, v.min() * 100)


HDR = f"{'subset':26}{'n':>5}{'mean':>7}{'med':>7}{'win%':>6}{'>10%':>6}{'>50%':>6}{'worst':>7} | {'plac med':>9}{'plac mean':>10}{'p(med)':>8}{'p(mean)':>8}"


def line(label, v, M):
    s = st(v)
    if s is None or s[0] < 1:
        print(f"{label:26}{0:5d}")
        return
    pm = np.nanmedian(M, axis=0)
    pa = np.nanmean(M, axis=0)
    pmed_ = (pm >= s[2] / 100).mean()
    pmean_ = (pa >= s[1] / 100).mean()
    print(f"{label:26}{s[0]:5d}{s[1]:7.1f}{s[2]:7.1f}{s[3]:6.0f}{s[4]:6.1f}{s[5]:6.1f}{s[6]:7.0f} | {np.median(pm)*100:9.1f}{np.mean(pa)*100:10.1f}{pmed_:8.3f}{pmean_:8.3f}")


def subsets(rows):
    dts = d.date.values[rows]
    reg = d.regime.values[rows]
    t = tier[rows]
    out = [("ALL", np.ones(len(rows), bool)),
           ("in-sample to 2026-08", dts < np.datetime64(SPLIT)),
           ("out-of-sample 2026-09+", dts >= np.datetime64(SPLIT)),
           ("regime bill>policy", reg == "bill>policy"),
           ("regime bill<=policy", reg == "bill<=policy")]
    for tt in (0, 1, 2):
        out.append((f"tier {TN[tt]}", t == tt))
    return out


def path_block(vk, exits=EXITS):
    e = EP[vk]
    print(f"\n-- {vk}: {VAR[vk][2]}; episodes {len(e)}; net of costs, entry next open")
    for x in exits:
        net = NET[x][e]
        keep = ~np.isnan(net) & tier_ok[e]
        rows = e[keep]
        M, fb = draw(rows, x)
        print(f" exit {x}: episodes with outcome {len(rows)} (placebo pool fallback to date-only: {fb})")
        print(" " + HDR)
        for lab, sm in subsets(rows):
            line(" " + lab, NET[x][rows][sm], M[sm])
        # fill sensitivity: drop episodes whose entry session closes at the upper lock
        nl = ~entry_locked[rows]
        line(" excl. entry-day lock", NET[x][rows][nl], M[nl])
        print(f"   share of episodes whose entry session closed at the upper lock: {entry_locked[rows].mean()*100:.1f}%")


print("\n=== 3. RETURN PATHS FROM NEXT OPEN, NET, WITH PLACEBO (random same-date same-tier rows, same exit) ===")
print("p(med) = share of 500 placebo draws whose median is at or above the signal median (small = signal better than random). Mean/median/worst in %.")
for vk in ["R1", "R1f", "R2", "R2f", "R3", "R3f"]:
    path_block(vk)
print("\n=== 3b. MIRROR: NEWS-LESS FALLS (buying the fall, long only) ===")
for vk in ["F1", "F1f", "F2", "F2f", "F3", "F3f"]:
    path_block(vk, exits=["T5", "T10", "T20", "trail20"])

# MFE/MAE on the main variant
print("\n=== 3c. Excursions, R1f (adjusted, from next open) ===")
e = EP["R1f"]
for k in (5, 10, 20):
    mf = d[f"mfe_{k}"].values[e]
    ma = d[f"mae_{k}"].values[e]
    print(f" k={k}: median MFE {np.nanmedian(mf)*100:.1f}%, median MAE {np.nanmedian(ma)*100:.1f}%, share MAE<=-10% {np.nanmean(ma<=-0.10)*100:.1f}%, share MAE<=-20% {np.nanmean(ma<=-0.20)*100:.1f}%, share MFE>=+10% {np.nanmean(mf>=0.10)*100:.1f}%")

# ---------------- 4. from the news day onward ----------------
print("\n=== 4. FROM THE NEWS DAY ONWARD ===")
print("Episodes followed by a filing of the five classes in sessions t+1..t+10. News session N = first such filing. Row r = first traded row of the symbol at or after N.")
print("pre = entry open to the close before N (gross); news-day move = ret_1d at r; post = net return entering at the open after N, exit T5/T10/T20/trail20.")
print("placebo = random rows in the same month and tier that carry a filing of the five classes on that session, same exit.")
newsflag = (d[["f_" + c for c in C5]].sum(axis=1) > 0).values
NK = ym * 4 + tier
NPOOL = {x: mkpool(NK, NET[x], newsflag) for x in EXITS}


def news_block(vk, W=10):
    e = EP[vk]
    ff = first_filing(e, W)
    has = ff >= 0
    ee = e[has]
    f = ff[has]
    Nsess = a5.sess.values[f]
    cls = a5.klass.values[f]
    r = np.searchsorted(key, code[ee] * 100000 + Nsess, "left")
    rc = np.minimum(r, N - 1)
    okr = (r < N) & (code[rc] == code[ee])
    ee, f, cls, r = ee[okr], f[okr], cls[okr], r[okr]
    print(f"\n-- {vk}: {VAR[vk][2]}: episodes {len(e)}, followed within {W}: {int(has.sum())} ({has.mean()*100:.1f}%), with a traded row at/after news: {len(ee)}")
    e_row = ee + 1
    pre = np.where(r > e_row, pidx[np.maximum(r - 1, 0)] / open_e[ee] - 1, np.nan)
    react = d.ret_1d.values[r].astype(float)
    print(f"  pre-news run-up from entry open: n {np.sum(~np.isnan(pre))}, median {np.nanmedian(pre)*100:.1f}%, mean {np.nanmean(pre)*100:.1f}%; news-session move: median {np.nanmedian(react)*100:.1f}%, mean {np.nanmean(react)*100:.1f}%, share>0 {np.nanmean(react>0)*100:.0f}%")
    print(f"  sessions from t to news: median {np.median(sess[r]-sess[ee]):.0f}")
    for x in ["T5", "T10", "T20", "trail20"]:
        net = NET[x][r]
        keep = ~np.isnan(net) & tier_ok[r]
        rows = r[keep]
        M = np.full((len(rows), B), np.nan)
        for n_, i in enumerate(rows):
            p = NPOOL[x].get(NK[i])
            if p is not None and len(p) >= 5:
                M[n_] = p[rng.integers(0, len(p), B)]
        okM = ~np.isnan(M[:, 0])
        print(f"  post-news exit {x}: n {len(rows)} (placebo pool found for {okM.sum()})")
        print("  " + HDR)
        line("  all first-filing classes", NET[x][rows], M)
        for c in C5:
            sel = (cls[keep] == c)
            if sel.sum() >= 5:
                line(f"  first filing = {c[:12]}", NET[x][rows][sel], M[sel])
        # versus joining at the original signal on the same episodes
        sig = NET[x][ee][keep]
        print(f"   same episodes, original entry at the signal's next open: n {np.sum(~np.isnan(sig))}, mean {np.nanmean(sig)*100:.1f}, median {np.nanmedian(sig)*100:.1f}, win {np.nanmean(sig>0)*100:.0f}%")


for vk in ["R1", "R1f", "R2f", "R3f", "F1", "F1f"]:
    news_block(vk)

# ---------------- 5. repeaters ----------------
print("\n=== 5. NAMES THAT REPEAT (R1f episodes) ===")
e = EP["R1f"]
ee_df = pd.DataFrame({"row": e, "sym": d.symbol.values[e], "date": d.date.values[e]})
ee_df["k"] = ee_df.groupby("sym").cumcount() + 1
ee_df["cnt"] = ee_df.groupby("sym").row.transform("size")
ff = first_filing(e, 10)
ee_df["news10"] = ff >= 0
ee_df["T20"] = NET["T20"][e]
ee_df["T10"] = NET["T10"][e]
ee_df["tr"] = NET["trail20"][e]
ee_df["tier"] = tier[e]
ee_df["tvm_m"] = tvm[e] / 1e6
rep = ee_df[ee_df.cnt >= 3]
print(f"names with 3+ episodes: {rep.sym.nunique()}, episodes in them {len(rep)} of {len(ee_df)}")
g = rep.groupby("sym").agg(eps=("row", "size"), news10=("news10", "mean"), T10med=("T10", "median"), T20mean=("T20", "mean"), T20med=("T20", "median"), T20win=("T20", lambda s: (s.dropna() > 0).mean()), trmed=("tr", "median"), trmean=("tr", "mean"), tvm=("tvm_m", "median"), first=("date", "min"), last=("date", "max")).sort_values("eps", ascending=False)
print("per-name table (net %, T20 = 20-session time exit, tr = trail20):")
print(f"{'sym':8}{'eps':>4}{'news10%':>8}{'T10med':>8}{'T20mean':>9}{'T20med':>8}{'T20win%':>8}{'tr med':>8}{'tr mean':>8}{'tv Rs m':>9}  first..last")
for s, r_ in g.head(40).iterrows():
    print(f"{s:8}{int(r_.eps):4d}{r_.news10*100:8.0f}{r_.T10med*100:8.1f}{r_.T20mean*100:9.1f}{r_.T20med*100:8.1f}{r_.T20win*100:8.0f}{r_.trmed*100:8.1f}{r_.trmean*100:8.1f}{r_.tvm:9.2f}  {str(r_['first'])[:10]}..{str(r_['last'])[:10]}")
print("\npoint-in-time test: the k-th episode of a name (k known at the time), net %, tier-OK only")
print(f"{'group':22}{'n':>5}{'news10%':>9}{'T10 mean':>9}{'T10 med':>8}{'T20 mean':>9}{'T20 med':>8}{'T20 win%':>9}{'tr mean':>8}{'tr med':>8}")
for lab, sel in [("1st episode", ee_df.k == 1), ("2nd episode", ee_df.k == 2), ("3rd+ episode", ee_df.k >= 3), ("3rd+ in 3+ names", (ee_df.k >= 3)), ("4th+ episode", ee_df.k >= 4), ("all", ee_df.k >= 1)]:
    s_ = ee_df[sel & (ee_df.tier >= 0)]
    print(f"{lab:22}{len(s_):5d}{s_.news10.mean()*100:9.1f}{s_.T10.mean()*100:9.1f}{s_.T10.median()*100:8.1f}{s_.T20.mean()*100:9.1f}{s_.T20.median()*100:8.1f}{(s_.T20.dropna()>0).mean()*100:9.0f}{s_.tr.mean()*100:8.1f}{s_.tr.median()*100:8.1f}")
# did a name's earlier episodes being followed by news predict the next being followed by news?
ee_df = ee_df.sort_values(["sym", "k"])
ee_df["prev_news"] = ee_df.groupby("sym").news10.shift(1)
ee_df["prev_news_rate"] = ee_df.groupby("sym").news10.transform(lambda s: s.shift(1).expanding().mean())
x_ = ee_df[ee_df.k >= 3]
print("episodes k>=3: news within 10 after the signal, by the name's earlier episodes' rate (point in time):")
for lab, sel in [("earlier rate >=50%", x_.prev_news_rate >= 0.5), ("earlier rate <50%", x_.prev_news_rate < 0.5)]:
    s_ = x_[sel]
    print(f"  {lab}: n {len(s_)}, news10 {s_.news10.mean()*100:.1f}%, T20 mean {s_.T20.mean()*100:.1f}, median {s_.T20.median()*100:.1f}")


print("\npoint-in-time repeat flag: episode where the same name already had 2+ episodes in the previous 252 sessions (known at the time)")
for vk in ["R1f", "R3f"]:
    ev = EP[vk]
    cs, ss = code[ev], sess[ev]
    prior = np.zeros(len(ev), int)
    for n_ in range(len(ev)):
        j = n_ - 1
        c_ = 0
        while j >= 0 and cs[j] == cs[n_] and ss[n_] - ss[j] <= 252:
            c_ += 1
            j -= 1
        prior[n_] = c_
    for lab, sel in [("repeat (2+ prior in 252)", prior >= 2), ("not repeat", prior < 2)]:
        for x in ["T10", "T20", "trail20"]:
            net = NET[x][ev]
            keep = sel & ~np.isnan(net) & tier_ok[ev]
            rows = ev[keep]
            M, fb = draw(rows, x)
            line(f"{vk} {lab[:12]} {x}", NET[x][rows], M)
    for tt in (0, 1):
        sel = (prior >= 2) & (tier[ev] == tt)
        for x in ["T20"]:
            net = NET[x][ev]
            keep = sel & ~np.isnan(net)
            rows = ev[keep]
            M, fb = draw(rows, x)
            line(f"{vk} repeat tier {TN[tt][:1]} {x}", NET[x][rows], M)

# ---------------- 6. case lists ----------------
print("\n=== 6. CASE LISTS (R1f episodes, ranked by ret_5d at the signal close) ===")
e = EP["R1f"]
ff10 = first_filing(e, 10)
tot10 = d.filing_within_10_total.values[e]
cases = pd.DataFrame({"row": e, "sym": d.symbol.values[e], "date": pd.to_datetime(d.date.values[e]).strftime("%Y-%m-%d"),
                      "r5": r5t[e] * 100, "tvm_m": tvm[e] / 1e6, "px": d.close.values[e], "T5": NET["T5"][e] * 100, "T10": NET["T10"][e] * 100, "T20": NET["T20"][e] * 100, "tr": NET["trail20"][e] * 100,
                      "ff": ff10, "tot10": tot10})
followed = cases[cases.ff >= 0].copy()
followed["fdate"] = pd.to_datetime(a5.fdate.values[followed.ff.values]).strftime("%Y-%m-%d")
followed["klass"] = a5.klass.values[followed.ff.values]
followed["title"] = a5.title.values[followed.ff.values]
followed["lag"] = a5.sess.values[followed.ff.values] - sess[followed.row.values]
rN = np.searchsorted(key, code[followed.row.values] * 100000 + a5.sess.values[followed.ff.values], "left")
rN = np.minimum(rN, N - 1)
followed["post10"] = NET["T10"][rN] * 100
followed["post20"] = NET["T20"][rN] * 100
nothing = cases[(cases.tot10 == 0)].copy()
print(f"R1f episodes {len(cases)}; followed by a five-class filing within 10: {len(followed)}; no filing of any class within 10: {len(nothing)}")
for nm, sub, cols in [("30 LARGEST FOLLOWED BY A FILING WITHIN 10 SESSIONS (all liquidity tiers)", followed, True), ("30 LARGEST FOLLOWED BY NOTHING WITHIN 10 SESSIONS (all liquidity tiers)", nothing, False)]:
    print(f"\n{nm}")
    print("T5/T10/T20/trail from the signal's next open, net %; post10/post20 = net return entering at the open after the news session")
    s_ = sub.sort_values("r5", ascending=False).head(30)
    for _, r_ in s_.iterrows():
        base = f"{r_['sym']:7}{r_['date']} r5 {r_.r5:5.1f}% px {r_.px:7.1f} tv {np.nan_to_num(r_.tvm_m,nan=-1):7.2f}m | T5 {r_.T5:6.1f} T10 {r_.T10:6.1f} T20 {r_.T20:6.1f} tr {r_.tr:6.1f}"
        if cols:
            base += f" | +{int(r_.lag)}s {r_.fdate} {r_.klass[:10]} post10 {r_.post10:6.1f} post20 {r_.post20:6.1f} | {str(r_.title)[:70]}"
        print(base)
liq = lambda df: df[df.tvm_m >= 5]
for nm, sub, cols in [("30 LARGEST FOLLOWED BY A FILING WITHIN 10 SESSIONS, median traded value >= Rs5m", followed, True), ("30 LARGEST FOLLOWED BY NOTHING WITHIN 10 SESSIONS, median traded value >= Rs5m", nothing, False)]:
    print(f"\n{nm}")
    s_ = liq(sub).sort_values("r5", ascending=False).head(30)
    for _, r_ in s_.iterrows():
        base = f"{r_['sym']:7}{r_['date']} r5 {r_.r5:5.1f}% px {r_.px:7.1f} tv {np.nan_to_num(r_.tvm_m,nan=-1):7.2f}m | T5 {r_.T5:6.1f} T10 {r_.T10:6.1f} T20 {r_.T20:6.1f} tr {r_.tr:6.1f}"
        if cols:
            base += f" | +{int(r_.lag)}s {r_.fdate} {r_.klass[:10]} post10 {r_.post10:6.1f} post20 {r_.post20:6.1f} | {str(r_.title)[:70]}"
        print(base)
for nm, sub in [("followed", followed), ("nothing", nothing)]:
    s_ = liq(sub).sort_values("r5", ascending=False).head(30)
    print(f"\n[{nm}, restricted to median traded value >= Rs5m: summary of these 30] T20 net median {s_.T20.median():.1f}, mean {s_.T20.mean():.1f}, win {(s_.T20.dropna()>0).mean()*100:.0f}%; trail20 median {s_.tr.median():.1f}, mean {s_.tr.mean():.1f}")
s_ = followed.sort_values("r5", ascending=False).head(30)
print(f"[followed top 30 all tiers] T20 median {s_.T20.median():.1f}, mean {s_.T20.mean():.1f}, win {(s_.T20.dropna()>0).mean()*100:.0f}%")
s_ = nothing.sort_values("r5", ascending=False).head(30)
print(f"[nothing top 30 all tiers] T20 median {s_.T20.median():.1f}, mean {s_.T20.mean():.1f}, win {(s_.T20.dropna()>0).mean()*100:.0f}%")
# followed vs nothing across all R1f episodes
print("\nAll R1f episodes: followed by a five-class filing within 10 vs not (hindsight split, descriptive only)")
for lab, sub in [("followed", followed), ("nothing (no filing of any class)", nothing), ("neither (only agm/credit/other)", cases[(cases.ff < 0) & (cases.tot10 > 0)])]:
    print(f"  {lab:34} n {len(sub):5d} | T10 mean {sub.T10.mean():5.1f} med {sub.T10.median():5.1f} | T20 mean {sub.T20.mean():5.1f} med {sub.T20.median():5.1f} win {(sub.T20.dropna()>0).mean()*100:3.0f}% | trail20 mean {sub.tr.mean():5.1f} med {sub.tr.median():5.1f}")

# ---------------- 7. what distinguishes the ones that paid ----------------
print("\n=== 7. WHAT DISTINGUISHES THE ONES THAT PAID (R1f, in-sample, tier-OK; exploratory, many cuts, not a signal) ===")
e = EP["R1f"]
e = e[(d.date.values[e] < np.datetime64(SPLIT)) & tier_ok[e]]
X = pd.DataFrame({"row": e})
for c_ in ["ret_5d", "ret_60d", "ret_126d", "vol_ratio_20_120", "vol_ratio_1_20", "locks_up_5d", "consecutive_up_days", "dist_252_high", "dist_252_low", "days_since_last_filing", "index_ret_5d", "ret_1d", "gap_open"]:
    X[c_] = d[c_].values[e].astype(float)
X["tvm_m"] = tvm[e] / 1e6
X["tier"] = [TN[t] for t in tier[e]]
X["regime"] = d.regime.values[e]
X["kmi"] = d.kmi_member.astype(object).values[e]
X["year"] = d.year.values[e]
X["board_known"] = d.next_board_meeting_known.values[e]
X["sector"] = d.sector.values[e]
X["news10"] = first_filing(e, 10) >= 0
X["T20"] = NET["T20"][e] * 100
X["tr"] = NET["trail20"][e] * 100
X["T10"] = NET["T10"][e] * 100
X = X[X.T20.notna()]
X["paid"] = X.T20 > 0
print(f"n {len(X)}; paid (T20 net>0) {X.paid.mean()*100:.1f}%; median T20 {X.T20.median():.1f}, mean {X.T20.mean():.1f}")
print("paid vs not paid, feature medians:")
for c_ in ["ret_5d", "ret_1d", "gap_open", "ret_60d", "vol_ratio_20_120", "vol_ratio_1_20", "locks_up_5d", "consecutive_up_days", "dist_252_high", "days_since_last_filing", "tvm_m"]:
    print(f"  {c_:24} paid {X[X.paid][c_].median():9.3f}   not paid {X[~X.paid][c_].median():9.3f}")


def bucket(col, qs=4, label=None):
    s_ = X[col]
    try:
        b = pd.qcut(s_, qs, duplicates="drop")
    except Exception:
        return
    print(f" by {label or col} (quantiles):")
    for k_, g_ in X.groupby(b):
        print(f"   {str(k_):28} n {len(g_):4d} | T20 med {g_.T20.median():6.1f} mean {g_.T20.mean():6.1f} win {g_.paid.mean()*100:3.0f}% | trail20 med {g_.tr.median():6.1f} | news10 {g_.news10.mean()*100:3.0f}%")


for c_ in ["ret_5d", "ret_1d", "vol_ratio_20_120", "vol_ratio_1_20", "dist_252_high", "ret_60d", "tvm_m"]:
    bucket(c_)
for c_ in ["tier", "regime", "kmi", "board_known", "news10", "year", "locks_up_5d", "sector"]:
    print(f" by {c_}:")
    for k_, g_ in X.groupby(X[c_].astype(str)):
        if len(g_) >= 15:
            print(f"   {k_:28} n {len(g_):4d} | T20 med {g_.T20.median():6.1f} mean {g_.T20.mean():6.1f} win {g_.paid.mean()*100:3.0f}% | trail20 med {g_.tr.median():6.1f} | news10 {g_.news10.mean()*100:3.0f}%")
print("\nepisodes by calendar year, all R1f with outcome (net T20 median / mean / n) and share followed by news10:")
for y_, g_ in X.groupby("year"):
    print(f"   {y_}: n {len(g_):4d} T20 med {g_.T20.median():6.1f} mean {g_.T20.mean():6.1f} news10 {g_.news10.mean()*100:3.0f}%")
print("\nDONE")

# ---------------- 2b. filing share by split (added) ----------------
print("\n=== 2b. SHARE FOLLOWED BY ANY OF THE 5 CLASSES WITHIN 10 SESSIONS, BY SPLIT (obs vs baseA vs baseB, %) ===")
for vk in ["R1f", "R3f", "F1f"]:
    e = EP[vk]
    thr = VAR[vk][1]
    col = "10|any of 5"
    obs = indf[col].values[e]
    bA = BASE_ALL[col].reindex(gkey[e]).values
    bB = BASE_ST[thr][col].reindex(gkey[e]).values
    dts = d.date.values[e]
    reg = d.regime.values[e]
    subs = [("ALL", np.ones(len(e), bool)), ("in-sample", dts < np.datetime64(SPLIT)), ("out-of-sample", dts >= np.datetime64(SPLIT)), ("bill>policy", reg == "bill>policy"), ("bill<=policy", reg == "bill<=policy")] + [(f"tier {TN[t]}", tier[e] == t) for t in (0, 1, 2)]
    print(f"-- {vk}")
    for lab, sm in subs:
        ok = sm & ~np.isnan(obs) & ~np.isnan(bA) & ~np.isnan(bB)
        if ok.sum() == 0:
            continue
        zB = (obs[ok].sum() - bB[ok].sum()) / np.sqrt((bB[ok] * (1 - bB[ok])).sum())
        print(f"   {lab:22} n {ok.sum():5d} obs {obs[ok].mean()*100:5.1f} baseA {bA[ok].mean()*100:5.1f} baseB {bB[ok].mean()*100:5.1f} zB {zB:6.1f}")
print("\nDONE2")
