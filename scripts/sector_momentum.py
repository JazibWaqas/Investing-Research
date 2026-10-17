# Equal-weight sector baskets, daily returns clipped at +/-10%, 6m (126 sessions) to 2026-10-16.
import pandas as pd, numpy as np, os, re
R = r"C:\Users\JazibWaqas\Documents\GitHub\Investing-Research"
S = {
 "Oil refineries": "ATRL PRL NRL CNERGY",
 "E&P": "OGDC PPL MARI",
 "OMC": "PSO WAFI HTL BPL",
 "Power": "HUBC KEL EPQL KOHE SEL GEMMEL",
 "Fertilizer": "FFC EFERT FATIMA ENGROH",
 "Cement": "LUCK DGKC MLCF FCCL KOHC CHCC PIOC ACPL POWER GWLC THCCL FLYNG FECTC DCL DNCC SMCPL",
 "Steel & engineering": "ASL ISL MUGHAL INIL CSAP ITTEFAQ DSL BECO BCL KSBP MSCL",
 "Autos": "SAZEW GAL GHNI HCAR MTL AGTL BWHL EXIDE LOADS GTYR ATBA HINO",
 "Tech & telecom": "SYS NETSOL AIRLINK AVN OCTOPUS TELE PAKD SELECT ITANZ QTECH STL ZAL SYM",
 "Islamic banks & fin.": "MEBL FABL BIPL FHAM OLPM ORM PQGTL PAKQATAR FPJM TRSM",
 "Pharma": "GLAXO HALEON ABOT HINOON SEARL AGP CPHL FEROZ BFBIO MACTER IBLHL OTSU LIVEN HPL",
 "Textiles": "NML ILP TOWL ASTM KOHTM ARCTM DFSM TATM GATM KTML JDMT MEHT JATM SHDT GADT FZCM SAPT FML CRTM ZAHID ANL PSYL GATI",
 "Food & staples": "NESTLE FCEPL MFL PREMA UNITY TOMCL TREET COLG UPFL RMPL ISIL QUICE MFFL FFL SOYASUP ASCNC BBFL",
 "Chemicals": "EPCL LOTCHEM LCI ICL SITC WAHN ARPL PAKOXY GCIL GCWL GGL NRSL BERG BIFO DYNO DOL BUXL SARC SPL",
 "Glass, packaging, paper": "TGL GHGL GGGL GVGL PKGS CPPL IPAK ECOP CEPB MERIT SPEL MACFL RPL GEMPAPL",
 "Gas utilities & misc": "SNGP SSGC PIBTL PAEL SIEM PSEL PICT BLUEX SLGL FCL EMCO WAVES JVDC",
}
END = pd.Timestamp("2026-10-16")
def load(t):
    for d in ("seed/data/prices", "data/prices_raw"):
        p = os.path.join(R, d, t + ".csv")
        if os.path.exists(p):
            df = pd.read_csv(p, parse_dates=["date"])
            if len(df) > 200 and df.date.max() >= END - pd.Timedelta(days=7):
                s = df.set_index("date")["close"]
                return s[s > 0], d.split("/")[0]
    return None, None
kmi = pd.read_csv(os.path.join(R, "data/macro/kmiallshr.csv"), parse_dates=["date"]).set_index("date")["close"]
cal = kmi.index[kmi.index <= END]
def basket(series):
    rets = pd.concat([s.reindex(cal).ffill().pct_change().clip(-0.10, 0.10) for s in series], axis=1)
    return (1 + rets.mean(axis=1, skipna=True).fillna(0)).cumprod()
rows = []
for sec, names in S.items():
    got, miss = [], []
    for t in names.split():
        s, src = load(t)
        (got.append(s) if s is not None else miss.append(t))
    idx = basket(got)
    k = kmi.reindex(cal)
    def ret(n, x): return x.iloc[-1] / x.iloc[-1 - n] - 1
    w5 = idx.iloc[-1260:]
    pct5 = (idx.iloc[-1] - w5.min()) / (w5.max() - w5.min())
    rows.append(dict(sector=sec, n=len(got), r6m=ret(126, idx), rel6m=ret(126, idx) - ret(126, k),
                     r3m=ret(63, idx), rel3m=ret(63, idx) - ret(63, k), r1m=ret(21, idx),
                     pos5y=pct5, missing=" ".join(miss)))
out = pd.DataFrame(rows).sort_values("rel6m", ascending=False)
print("KMI All Share 6m %.1f%% 3m %.1f%%" % (100 * (kmi.reindex(cal).iloc[-1] / kmi.reindex(cal).iloc[-127] - 1), 100 * (kmi.reindex(cal).iloc[-1] / kmi.reindex(cal).iloc[-64] - 1)))
pd.set_option("display.width", 200)
f = out.copy()
for c in ["r6m", "rel6m", "r3m", "rel3m", "r1m", "pos5y"]: f[c] = (100 * f[c]).round(1)
print(f.to_string(index=False))
print("6m start date:", cal[-127].date())

CORE = {"Oil refineries":"ATRL PRL NRL CNERGY","E&P":"OGDC PPL MARI","OMC":"PSO","Power":"HUBC KEL",
 "Fertilizer":"FFC EFERT FATIMA ENGROH","Cement":"LUCK DGKC MLCF FCCL CHCC","Steel & engineering":"ISL ASL MUGHAL INIL",
 "Autos":"SAZEW GAL GHNI HCAR MTL","Tech & telecom":"SYS NETSOL AIRLINK","Islamic banks & fin.":"MEBL FABL BIPL",
 "Pharma":"GLAXO ABOT SEARL AGP HALEON","Textiles":"NML ILP","Food & staples":"FCEPL MFL TREET PREMA",
 "Chemicals":"EPCL LOTCHEM LCI","Glass, packaging, paper":"TGL GHGL IPAK PKGS","Gas utilities & misc":"SNGP SSGC PIBTL PAEL"}
print("\nLIQUID CORE")
k = kmi.reindex(cal)
for sec, names in CORE.items():
    idx = basket([load(t)[0] for t in names.split()])
    r6 = idx.iloc[-1]/idx.iloc[-127]-1; r3 = idx.iloc[-1]/idx.iloc[-64]-1
    print(f"{sec:26s} 6m {100*r6:6.1f} rel {100*(r6-(k.iloc[-1]/k.iloc[-127]-1)):6.1f} | 3m {100*r3:6.1f} rel {100*(r3-(k.iloc[-1]/k.iloc[-64]-1)):6.1f}")
