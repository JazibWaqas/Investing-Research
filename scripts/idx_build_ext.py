# Executed inside idx_build.py (shares rows, log, sym, U, D, pd, re, pdfplumber). Notices added after the first pass.
# Names/tickers were read from the PDFs (text, or page images for scans); scanned notices are marked in the note column.
P = 'https://www.psx.com.pk/psx/themes/psx/uploads/'

def add(ix, ann, eff, ins, outs, url, note='', raw=False, full=False):
    f = (lambda x: x) if raw else sym
    for n in ins: rows.append((ix, ann, eff, f(n), 'add', url, note or n))
    for n in outs: rows.append((ix, ann, eff, f(n), 'delete', url, note or n))
    log.append((ix, ann, eff, url, 'yes' if full else 'no'))

def lst30(f, n=30):
    """first n 'No SYMBOL Name' rows after a header line containing Symbol and Compan"""
    out, on = [], False
    for pg in pdfplumber.open(D + f).pages:
        for l in (pg.extract_text() or '').split('\n'):
            if re.search(r'symbol.*compan', l, re.I): on = True; continue
            m = re.match(r'^\d+ ([A-Z][A-Z0-9]+) (.+)$', l)
            if on and m:
                out.append((m.group(1), m.group(2)))
                if len(out) == n: return out
    return out

def members(ix, eff, f, n=30):
    m = lst30(f, n)
    if len(m) == n:
        pd.DataFrame(m, columns=['symbol', 'company']).to_csv(f'data/index_members/{ix}_{eff}.csv', index=False); return True
    return False

def setfull(ix, eff):
    for i, r in enumerate(log):
        if r[0] == ix and r[2] == eff: log[i] = r[:4] + ('yes',)

# ---- KSE-100 additions
add('KSE100', '2022-03-15', '2022-04-01', ['Pak-Gulf Leasing Company', 'Tariq Glass Industries Limited', 'Javedan Corporation Limited'],
    ['Orix Leasing Pakistan Limited', 'Feroze1888 Mills Limited', 'Jahangir Siddiqui & Company Limited'], P + 'Notice_251_date_MArch_15_2022_KSE-100_Recomposition-28-Feb-22.pdf')
add('KSE100', '2024-09-13', '2024-10-01', ['Kohinoor Spinning Mills Limited', 'JDW Sugar Mills Limited', 'Sazgar Engineering Works Limited', 'Air Link Communication Limited', 'Mehmood Textile Mills Limited', 'Atlas Honda Limited', 'Honda Atlas Cars (Pakistan) Limited'],
    ['Gadoon Textile Mills Limited', 'Habib Sugar Mills Limited', 'BankIslami Pakistan Limited', 'Century Paper & Board Mills Limited', 'Kohinoor Textile Mills Limited', 'Shifa International Hospitals Limited', 'Saif Power Limited'], P + 'KSE-100-notice-13-Sept-24.pdf')
for f, eff in [('Notice_251_date_MArch_15_2022_KSE-100_Recomposition-28-Feb-22.pdf', '2022-04-01'), ('KSE-100-notice-13-Sept-24.pdf', '2024-10-01')]:
    a = [(n, nm) for n, nm in annex(D + f) if n <= 100 and nm[:1].isalpha()]
    assert len(a) == 100 and len({n for n, _ in a}) == 100, (f, len(a))
    pd.DataFrame([(sym(nm), nm) for _, nm in a], columns=['symbol', 'company']).to_csv(f'data/index_members/KSE100_{eff}.csv', index=False)
    setfull('KSE100', eff)

# ---- KSE-30
K30 = [
 ('Notice-KSE-30-index-June-30-2020.pdf', '2020-07-30', '2020-09-15', ['The Bank of Punjab', 'Cherat Cement Company Limited', 'Hascol Petroleum Limited', 'Unity Foods Limited'], ['Attock Refinery Limited', 'Millat Tractors Limited', 'Engro Polymer & Chemicals Limited', 'Lotte Chemical Pakistan Limited']),
 ('Notice_137_KSE_30_index_Dec_31_2020.pdf', '2021-01-29', '2021-03-15', ['Attock Refinery Limited', 'Systems Limited', 'Ghandhara Industries Limited', 'Pioneer Cement Limited', 'Kot Addu Power Company Limited', 'Dawood Hercules Corporation Limited'], ['Fauji Cement Company Limited', 'Hascol Petroleum Limited', 'Sui Northern Gas Pipelines Limited', 'National Bank of Pakistan', 'Bank Alfalah Limited', 'The Bank of Punjab']),
 ('Notice-no-946-date-August-3_2021-for-KSE30-index-Recomposition-30-June-2.pdf', '2021-08-03', '2021-09-15', ['Pakistan Refinery Limited', 'National Refinery Limited', 'International Industries Limited', 'Engro Polymer & Chemicals Limited', 'Avanceon Limited'], ['Cherat Cement Company Limited', 'Nishat Mills Limited', 'Pak Elektron Limited', 'Ghandhara Industries Limited', 'Dawood Hercules Corporation Limited']),
 ('Notice_KSE-30_index_726_Recomposition-30-June-22.pdf', '2022-07-29', '2022-09-15', ['Treet Corporation Limited', 'TPL Properties Limited', 'Telecard Limited'], ['Cnergyico PK Limited', 'The Searle Company Limited', 'NetSol Technologies Limited']),
 ('Notice_99_KSE-30_Recomposition-31-Jan_2023.pdf', '2023-01-31', '2023-03-15', ['Pakistan Refinery Limited', 'NetSol Technologies Limited', 'Sui Northern Gas Pipe Line Limited', 'Pak Elektron Limited'], ['Ghani Global Holdings Limited', 'Maple Leaf Cement Factory Limited', 'Telecard Limited', 'Treet Corporation Limited']),
 ('Notice-784_KSE-30_Recomposition-June-23.pdf', '2023-07-31', '2023-09-15', ['APL', 'BAFL', 'CHCC', 'FCCL', 'MLCF', 'PIOC'], ['NETSOL', 'NRL', 'PAEL', 'PRL', 'TPLP', 'UNITY']),
 ('Notice_KSE-30_Index_Recomposition-_Dec_2023.pdf', '2024-01-31', '2024-03-15', ['NRL', 'SHEL', 'PRL', 'COLG', 'SEARL', 'TPLP'], ['APL', 'AVN', 'EPCL', 'FCCL', 'KAPCO', 'PIOC']),
 ('Notice-PSXN-145-KSE30-Recomposition-Dec-2024.pdf', '2025-01-31', '2025-03-17', ['Ghandhara Industries Limited', 'Ghandhara Automobiles Limited', 'NetSol Technologies Limited', 'National Bank of Pakistan', 'Dewan Farooque Motors Limited'], ['Bank Alfalah Limited', 'National Refinery Limited', 'Pioneer Cement Limited', 'Pakistan Refinery Limited', 'Sui Northern Gas Pipelines Limited']),
 ('Notice-KSE-30-Index-Recomposition-June-2025.pdf', '2025-07-31', '2025-09-15', ['Sui Northern Gas Pipelines Limited', 'Pakistan Refinery Limited', 'The Bank of Punjab', 'Sui Southern Gas Company Limited'], ['Air Link Communication Limited', 'Dewan Farooque Motors Limited', 'Millat Tractors Limited', 'NetSol Technologies Limited']),
 ('Notice-KSE-30-Index-Recomposition-December2025.pdf', '2026-01-30', '2026-03-16', ['Air Link Communication Limited', 'National Refinery Limited'], ['Bank AL Habib Limited', 'Pakistan Refinery Limited']),
]
for f, ann, eff, ins, outs in K30:
    add('KSE30', ann, eff, ins, outs, P + f, raw=all(re.fullmatch(r'[A-Z0-9]+', x) for x in ins + outs), full=members('KSE30', eff, f))

# ---- KMI-30
K = [
 ('KMI-30_Notice_updatedon_Jul-18-19.pdf', '2019-06', '2019-07-15', ['Millat Tractors Limited', 'Attock Petroleum Limited', 'AGP Limited', 'Meezan Bank Limited', 'Honda Atlas Cars (Pakistan) Limited', 'Dawood Hercules Corporation Limited', 'Thal Limited'],
  ['International Industries Limited', 'National Refinery Limited', 'Engro Foods Limited', 'Shell Pakistan Limited', 'Pakistan State Oil Company Limited', 'Byco Petroleum Pakistan Limited', 'The Hub Power Company Limited'], 'scan; announce date only to month (image blurred)'),
 ('islamic-index-notice-Dec-20-2019-for-June-Reveiw-2019.pdf', '2019-12-20', '2019-12-31', ['The Hub Power Company Limited', 'Pakistan State Oil Company Limited', 'Frieslandcampina Engro Pakistan Limited', 'Pak Suzuki Motor Company Limited', 'NetSol Technologies Limited', 'Unity Foods Limited'],
  ['Attock Petroleum Limited', 'Hascol Petroleum Limited', 'Packages Limited', 'AGP Limited', 'Pakistan International Bulk Terminal Limited', 'Thal Limited'], 'scan PSX/N-1640'),
 ('KMI-30-index-notice-788-dated-July-3-2020.pdf', '2020-07-03', '2020-07-13', ['Cherat Cement Company Limited', 'Indus Motor Company Limited', 'Systems Limited', 'National Refinery Limited', 'Hascol Petroleum Limited'],
  ['The Hub Power Company Limited', 'Pak Suzuki Motor Company Limited', 'Dawood Hercules Corporation Limited', 'Sui Southern Gas Company Limited', 'Frieslandcampina Engro Pakistan Limited'], ''),
 ('Notice-December-4-2020-KMI-30-index-for-the-period-June-30-2020.pdf', '2020-12-04', '2020-12-21', ['GlaxoSmithKline Pakistan Limited', 'Kohat Cement Company Limited', 'ICI Pakistan Limited', 'Abbott Laboratories (Pakistan) Limited', 'Packages Limited', 'International Industries Limited'],
  ['Lotte Chemical Pakistan Limited', 'Hascol Petroleum Limited', 'Indus Motor Company Limited', 'Systems Limited', 'National Refinery Limited', 'NetSol Technologies Limited'], ''),
 ('Notice-746_of_KMI_30_Index_for_Recomposition-Dec-20.pdf', '2021-06-18', '2021-06-28', ['The Hub Power Company Limited', 'Systems Limited', 'Ghandhara Industries Limited', 'Avanceon Limited', 'Pakistan International Bulk Terminal Limited', 'National Refinery Limited'],
  ['Abbott Laboratories (Pakistan) Limited', 'Kohat Cement Company Limited', 'ICI Pakistan Limited', 'K-Electric Limited', 'Packages Limited', 'GlaxoSmithKline Pakistan Limited'], ''),
 ('Notice-1460-Dec-10-2021-KMI-30-index-re-composition-for-the-period-(June_30_2021).pdf', '2021-12-10', '2021-12-20', ['Pioneer Cement Limited', 'Byco Petroleum Pakistan Limited', 'Azgard Nine Limited'],
  ['Pakistan International Bulk Terminal Limited', 'Sui Northern Gas Pipelines Limited', 'Honda Atlas Cars (Pakistan) Limited'], ''),
 ('Notice_1302_Dec_23_2022_KMI_30_Index_Re-composition_for_the_period_June-22_1.pdf', '2022-12-23', '2022-12-30', ['TPL Properties Limited', 'Fauji Cement Company Limited', 'Pak Elektron Limited'],
  ['The Hub Power Company Limited', 'Sui Northern Gas Pipelines Limited', 'International Industries Limited'], ''),
 ('Notice_No._653_KMI_30_Index_Recomposition_-Dec-22_.pdf', '2023-06-23', '2023-07-07', ['The Hub Power Company Limited', 'Pakistan Refinery Limited', 'NetSol Technologies Limited', 'Sui Northern Gas Pipelines Limited', 'Attock Petroleum Limited', 'Lotte Chemical Pakistan Limited', 'Shell Pakistan Limited'],
  ['Cnergyico PK Limited', 'Ghani Global Holdings Limited', 'Nishat Mills Limited', 'Pakistan Oilfields Limited', 'The Searle Company Limited', 'Telecard Limited', 'Treet Corporation Limited'], ''),
 ('Notice-KMI_30_Index_Recomposition-30_Jun_2023.pdf', '2023-12-15', '2023-12-22', ['Colgate-Palmolive (Pakistan) Limited', 'The Searle Company Limited', 'Cnergyico PK Limited', 'Dolmen City REIT'],
  ['Dawood Hercules Corporation Limited', 'NetSol Technologies Limited', 'Pak Elektron Limited', 'Shell Pakistan Limited'], ''),
 ('Notice-KMI30_Re-compostion-_June_24(final).pdf', '2024-06-07', '2024-06-14', ['Shell Pakistan Limited', 'Nishat Mills Limited', 'Interloop Limited', 'NetSol Technologies Limited', 'Faysal Bank Limited', 'Air Link Communication Limited'],
  ['Attock Petroleum Limited', 'Avanceon Limited', 'Cnergyico PK Limited', 'Colgate-Palmolive (Pakistan) Limited', 'Lotte Chemical Pakistan Limited', 'Oil & Gas Development Company Limited'], ''),
 ('KMI30-Index-Re-composition-Notice-final1-12-23-24.pdf', '2024-12-20', '2024-12-30', ['Oil & Gas Development Company Limited', 'Sazgar Engineering Works Limited', 'Pak Elektron Limited', 'Honda Atlas Cars (Pakistan) Limited', 'Fauji Foods Limited', 'K-Electric Limited', 'Dawood Hercules Corporation Limited'],
  ['Cherat Cement Company Limited', 'Dolmen City REIT', 'Interloop Limited', 'NetSol Technologies Limited', 'Nishat Mills Limited', 'Shell Pakistan Limited', 'TPL Properties Limited'], ''),
 ('Combined-KMI30-Notice-and-List-Dec-2024-revised.pdf', '2025-05-23', '2025-06-02', ['Ghandhara Automobiles Limited', 'NetSol Technologies Limited', 'Octopus Digital Limited', 'The Organic Meat Company Limited', 'Avanceon Limited'],
  ['Air Link Communication Limited', 'Engro Polymer & Chemicals Limited', 'K-Electric Limited', 'National Refinery Limited', 'Unity Foods Limited'], ''),
]
for f, ann, eff, ins, outs, note in K:
    add('KMI30', ann, eff, ins, outs, P + f, note=note, full=members('KMI30', eff, f))
# the Nov-2025 / May-2026 lists were set earlier in idx_build.py; Dec-2023/2024 lists are symbol tables too
# ---- KMI All Share: transcribed from scans / hand-read where table extraction failed
add('KMI_ALL', '2019-01-16', '2019-01-28', ['ADAMS', 'AGP', 'BGL', 'BAPL', 'COLG', 'DNCC', 'DWSM', 'EPQL', 'GGGL', 'GSKCH', 'HMM', 'HSPI', 'IDSM', 'JDWS', 'KCL', 'MSCL', 'MIRKS', 'PIBTL', 'PGCL', 'PSO', 'SANSM', 'SHCM', 'STJT', 'SASML', 'TATM', 'UBDL', 'UNITY', 'WAVES', 'WYETH'],
    ['ARUJ', 'ECOP', 'FANM', 'GTYR', 'IDRT', 'KASBM', 'LPL', 'MTL', 'MUGHAL', 'SYS', 'ZAHID'], P + 'PSX-KMI-ALL-SHARE-INDEX-NOTICE-JUNE-2018-min.pdf', 'scan PSX/N-48; total 246 (29 in, 11 out)', raw=True)
add('KMI_ALL', '2019-06-26', '2019-07-15', ['AGSML', 'ALNRS', 'PREMA', 'CHAS', 'CLOV', 'HCAR', 'MTL', 'MUGHAL', 'SHSML', 'STPL', 'THALL', 'WTL'],
    ['AEL', 'ALTN', 'BCML', 'BGL', 'BYCO', 'CPPL', 'DMTM', 'DWSM', 'EPQL', 'FASM', 'FEM', 'FPJM', 'GLPL', 'HUBC', 'IDSM', 'IDYM', 'JDWS', 'MRNS', 'MSCL', 'NPL', 'PRL', 'PSO', 'REDCO', 'SEL', 'SHCM', 'TATM', 'TRPOL', 'UNITY', 'WYETH'],
    P + 'KMI_All_notice_updatedon_Jul-18-19.pdf', 'scan; total 227 (12 in, 29 out); effective day read as 15', raw=True)
add('KMI_ALL', '2020-01-06', '2020-01-13', ['FANM', 'ARUJ', 'BAFS', 'BYCO', 'FASM', 'FEM', 'FPJM', 'HUBC', 'IDSM', 'IDYM', 'ILP', 'JDWS', 'KASBM', 'KOHTM', 'MQTM', 'PSO', 'REDCO', 'SFLL', 'SEL', 'SYS', 'TATM', 'TRPOL', 'UNITY', 'ZAHID'],
    ['ASTM', 'BATA', 'BAPL', 'CHAS', 'DMIL', 'PAKMI', 'FPRM', 'HINO', 'ISIL', 'JUBS', 'KHYT', 'KOHE', 'LMSM', 'PIBTL', 'PIOC', 'SHSML', 'THALL', 'UBDL', 'WAHN', 'DNCC', 'GAMON', 'PECO', 'HAEL', 'HSPI'],
    P + 'KMI_ALL_notices_updatedon_Jan6_2020.pdf', 'scan PSX/N-10/2020; 24 in, 24 out; FPRM ticker for First Prudential Modaraba not legible', raw=True)
add('KMI_ALL', '2021-06-30', '2021-07-05', ['BGL', 'FCEPL', 'PIBTL', 'PSMC', 'TOMCL', 'SHSML', 'TGL', 'THALL', 'TRIPF', 'CHAS', 'MRNS', 'AVN', 'ASL', 'HUBC', 'SYS', 'AGHA', 'ADOS', 'BAFS', 'BTL', 'GAMON', 'LEUL', 'MIRKS', 'MODAM', 'MQTM', 'PMRS', 'TICL', 'WAHN', 'BNL', 'UBDL', 'ADAMS', 'UCAPM'],
    ['COLG', 'DFSM', 'FANM', 'FIBLM', 'NRSL', 'FCONM', 'PSEL', 'PTC', 'SFL', 'GGGL', 'JDWS', 'SHDT', 'SHEZ', 'STPL'],
    P + 'notice_825_June_30_2021_KMI_All_Share_islamic_period_December_31_2020.pdf', 'scan PSX/N-825; total 226 (31 in, 14 out)', raw=True)
add('KMI_ALL', '2021-12-24', '2022-01-03', ['ANL', 'CNERGY', 'CLVL', 'DAWH', 'DFSM', 'FZCM', 'FANM', 'PAKM', 'PMI', 'GADT', 'GGGL', 'GFIL', 'HINO', 'IDRT', 'JKSM', 'KASBM', 'KOHE', 'MFFL', 'NATM', 'NRSL', 'OTSU', 'PSEL', 'PTC', 'PIOC', 'RCML', 'SGABL', 'SFL', 'SSML', 'SGF', 'SHDT', 'SHEZ', 'STPL', 'TATM', 'TELE', 'TREET', 'WYETH', 'ZTL']  ,
    ['AABS', 'ALNRS', 'ADMM', 'BAFS', 'CHAS', 'MRNS', 'MIRKS', 'SEPL', 'SHSML', 'SINDM', 'PMRS', 'TICL', 'CLOV'], P + 'sharia_KMI_All_Share_list_June_2021_Final_27122021.pdf', 'PSX/N-1504; total 250 (37 in, 13 out); incoming list hand-read from text', raw=True)
for f, ann, eff, note in [('Notice-with-List-incoming-outgoing-KMI-ALL-Shares-July-01-2019-Dec-31-2019.pdf', '2020-07-10', '2020-07-20', 'PSX/N-805; total 217'),
                          ('Copy_of_KMI_All_Share_June_-22_23122022.pdf', '2023-01-05', '2023-01-12', 'PSX/N-008; total 261'),
                          ('Notice-666_KMI_All_Share_Index_re-composition_for_Dec-22.pdf', '2023-06-26', '2023-07-10', 'PSX/N-666; total 251')]:
    ins, outs = kmi[f]
    add('KMI_ALL', ann, eff, ins, outs, P + f, note, raw=True)

# ---- gaps between consecutive full lists = one missing notice each (derived, flagged in source_url). Ticker renames are not changes.
def derived(ix, a, b, eff, rename=None):
    rename = rename or {}
    A = set(pd.read_csv(f'data/index_members/{ix}_{a}.csv').symbol); B = set(pd.read_csv(f'data/index_members/{ix}_{b}.csv').symbol)
    A = {rename.get(x, x) for x in A}
    B = (B - {r[3] for r in rows if r[0] == ix and r[2] == b and r[4] == 'add'}) | {r[3] for r in rows if r[0] == ix and r[2] == b and r[4] == 'delete'}  # undo the known notice at b
    note = f'derived: {ix} list {a} vs {b}; notice not found'
    for x in sorted(B - A): rows.append((ix, '', eff, x, 'add', 'derived', note))
    for x in sorted(A - B): rows.append((ix, '', eff, x, 'delete', 'derived', note))
    log.append((ix, '', eff, 'derived', 'no'))
derived('KSE100', '2023-04-03', '2024-04-01', '2023-10')
derived('KSE30', '2021-09-15', '2022-09-15', '2022-03')
derived('KSE30', '2024-03-15', '2025-03-17', '2024-09', {'ENGRO': 'ENGROH'})
derived('KMI30', '2021-12-20', '2022-12-30', '2022-06', {'BYCO': 'CNERGY'})

# ---- KMI All Share: approximate membership by rolling the exact 2026-06-05 list backwards through the notices (files named *_derived_*)
TOT = {'2019-01-28': 246, '2019-07-15': 227, '2020-01-13': 226, '2020-07-20': 217, '2020-12-31': 209, '2021-07-05': 226, '2022-01-03': 250, '2022-07-15': 252,
       '2023-01-12': 261, '2023-07-10': 251, '2023-12-26': 258, '2024-06-25': 255, '2025-01-03': 264, '2025-06-10': 258, '2025-12-02': 281, '2026-06-05': 309}
ev = sorted({r[2] for r in rows if r[0] == 'KMI_ALL' and r[2] <= '2026-06-05'})
cur = set(pd.read_csv('data/index_members/KMI_ALL_2026-06-05.csv').symbol); KMI_CHECK = []
for i in range(len(ev) - 1, -1, -1):
    e = ev[i]
    pd.DataFrame(sorted(cur), columns=['symbol']).to_csv(f'data/index_members/KMI_ALL_derived_{e}.csv', index=False)
    KMI_CHECK.append((e, len(cur), TOT.get(e)))
    cur = (cur - {r[3] for r in rows if r[0] == 'KMI_ALL' and r[2] == e and r[4] == 'add'}) | {r[3] for r in rows if r[0] == 'KMI_ALL' and r[2] == e and r[4] == 'delete'}

exec(open('scripts/idx_build_ext2.py').read())
