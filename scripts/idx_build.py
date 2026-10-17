"""Build data/index_changes.csv, data/index_recomp_log.csv, data/index_members/*.csv from PSX notices in data/raw/index_pdfs/.
Notice facts (dates, in/out names) were read from the PDFs by hand; ticker lists are parsed.
Run: .venv/Scripts/python.exe -I scripts/idx_build.py"""
import sys, re, json, os, shutil, pdfplumber, pandas as pd
sys.path.insert(0, 'scripts')
from idx_ksemap import annex, lookup
U = 'https://www.psx.com.pk/psx/themes/psx/uploads/'
D = 'data/raw/index_pdfs/'
# names the symbols.csv fuzzy match gets wrong or cannot find
MANUAL = {'Mari Petroleum Company Ltd': 'MARI', 'Mari Petroleum Company Ltd.': 'MARI', 'Orix Leasing Pakistan Ltd': 'OLPL',
          'I. C. I. Pakistan Ltd': 'ICI', 'Treet Corporation Limited': 'TREET'}
if os.path.exists('scripts/idx_manual_names.json'): MANUAL.update(json.load(open('scripts/idx_manual_names.json')))

# ---- KSE-100 notices: (file, announce, effective, in-names, out-names, full list parsed)
KSE100 = [
 ('Notice_of_Re-composition_of_KSE-100_Index_438.doc_(26-Feb-21)_.pdf', '2021-03-10', '2021-04-01',
  ['Yousaf Weaving Mills Limited', 'Ibrahim Fibres Limited', 'National Refinery Limited', 'Unity Foods Limited', 'Saif Power Limited'],
  ['Shahtaj Textile Limited', 'Gatron (Industries) Limited', 'Philip Morris (Pakistan) Limited', 'Glaxo SmithKline Consumer Healthcare Pakistan Limited', 'Century Paper & Board Mills Limited'], True),
 ('Notice-KSE-100-Recomposition-31-Aug-21.pdf', '2021-09-15', '2021-10-01',
  ['Shakarganj Limited', 'Aisha Steel Mills Limited', 'Avanceon Limited', 'Jahangir Siddiqui & Co. Limited', 'Mughal Iron & Steel Industries Limited'],
  ['JDW Sugar Mills Limited', 'Jubilee Life Insurance Company Limited', 'Agriautos Industries Limited', 'Sui Southern Gas Company Limited', 'Hascol Petroleum Limited'], True),
 ('Notice_KSE-100_Recomposition-31-Aug-22..pdf', '2022-09-15', '2022-10-03',
  ['Air Link Communication Ltd', 'Rafhan Maize Products Company Ltd', 'Unilever Pakistan Foods Ltd'],
  ['Azgard Nine Ltd', 'Aisha Steel Mills Ltd', 'IGI Holdings Ltd'], False),
 ('Notice-KSE-100_Recomposition-28-Feb-23.pdf', '2023-03-17', '2023-04-03',
  ['JDW Sugar Mills Ltd.', 'Pakistan Aluminum Beverage Cans Ltd.'], ['Shakarganj Ltd', 'Nishat Chunian Ltd'], True),
 ('Notice_KSE-100-29_Feb_2024.pdf', '2024-03-15', '2024-04-01',
  ['Nishat Chunian Power Limited', 'Nishat Power Limited', 'Habib Sugar Mills Limited'],
  ['Archroma Pakistan Limited', 'Gul Ahmed Textile Mills Limited', 'JDW Sugar Mills Limited'], True),
 ('KSE-100-notice-14-Mar-25.pdf', '2025-03-14', '2025-04',
  ['TPL REIT Fund I', 'Gadoon Textile Mills Limited', 'Agritech Limited', 'Hum Network Limited', 'Haleon Pakistan Limited'],
  ['BankIslami Pakistan Limited', 'Kohinoor Spinning Mills Limited', 'Nishat Chunian Power Limited', 'National Refinery Limited', 'Wafi Energy Pakistan Limited'], True),
 ('KSE-100-notice-PSXN-991-15-Sept-25.pdf', '2025-09-15', '2025-10-01',
  ['S.S.Oil Mills Limited', 'Shifa International Hospitals Limited', 'DH Partners Limited', 'Ghandhara Automobiles Limited', 'Sui Southern Gas Company Limited', 'Ghandhara Industries Limited', 'Citi Pharma Ltd.', 'Fauji Foods Limited'],
  ['Punjab Oil Mills', 'Avanceon Limited', 'EFU General Insurance Limited', 'Engro Polymer & Chemicals Limited', 'Frieslandcampina Engro Pakistan Limited', 'Mughal Iron & Steel Industries Limited', 'Nishat Power Limited', 'Agritech Limited'], True),
 ('KSE-100-Re-composition-notice-As-of-Feb-2026.pdf', '2026-03-13', '2026-04-01',
  ['Arif Habib Corporation Limited', 'Power Cement Limited'], ['Unity Foods Limited', 'Pakgen Power Limited'], True),
 ('KSE-100_--KSE100-PR-Index-re-composition-Notice-as-of-Aug-2026.pdf', '2026-09-15', '2026-10-01',
  ['Image Pakistan Limited', 'Thatta Cement Company Limited', 'Nishat Chunian Power Limited', 'Bank Makramah Limited'],
  ['Hum Network Limited', 'Mehmood Textile Mills Limited', 'Pakistan Aluminium Beverage Cans Limited', 'Rafhan Maize Products Company Limited'], True),
]
rows, log, unm = [], [], {}
def sym(name):
    if name.startswith('P. T. C. L.'): return 'PTC'
    s = lookup(name, MANUAL)
    if s is None or s.endswith('?'): unm[name] = s
    return (s or '').rstrip('?') or name
os.makedirs('data/index_members', exist_ok=True)
for f, ann, eff, ins, outs, full in KSE100:
    url = U + f
    rows += [('KSE100', ann, eff, sym(n), 'add', url, n) for n in ins] + [('KSE100', ann, eff, sym(n), 'delete', url, n) for n in outs]
    if full:
        a = [(n, nm) for n, nm in annex(D + f) if n <= 100 and nm[:1].isalpha()]
        assert len(a) == 100 and len({n for n, _ in a}) == 100, (f, len(a))
        pd.DataFrame([(sym(nm), nm) for _, nm in a], columns=['symbol', 'company']).to_csv(f'data/index_members/KSE100_{eff}.csv', index=False)
    log.append(('KSE100', ann, eff, url, 'yes' if full else 'no'))

# ---- KMI All Share: tickers pulled from the incoming/outgoing tables by idx_kmi_changes.py
kmi = json.load(open('scripts/_tmp_kmi.json'))
KMIALL = [
 ('Notice_1412_of_Recomposition_of_KMI_ALL_Shares_Dec_22_2020.pdf', '2020-12-22', '2020-12-31'),
 ('Notice-_KMI_All_Shares_Index_Recomposition_30-June-22_(M).pdf', '2022-07-07', '2022-07-15'),
 ('Notice-_KMI-All-Index-Re-composition-Jun-30-2023-Final.pdf', '2023-12-18', '2023-12-26'),
 ('KMI-ALL-Share-Recomposition-Notice-june-12-2024.pdf', '2024-06-14', '2024-06-25'),
 ('Notice-KMIALLshare-Notice-as-of-June-2024.pdf', '2024-12-30', '2025-01-03'),
 ('KMI-All-share-Notice-Recomposition-as-of-Dec-_2024-Final.pdf', '2025-06-02', '2025-06-10'),
 ('Merged_KMIALL_Notice_and_FinalList_June2025.pdf', '2025-11-24', '2025-12-02'),
 ('Notice-to-KMIALL-re-composition-as-of-Dec-2025-Revised.pdf', '2026-05-29', '2026-06-05'),
]
for f, ann, eff in KMIALL:
    ins, outs = kmi[f]; url = U + f
    rows += [('KMI_ALL', ann, eff, s, 'add', url, '') for s in ins] + [('KMI_ALL', ann, eff, s, 'delete', url, '') for s in outs]
    log.append(('KMI_ALL', ann, eff, url, 'yes' if eff == '2026-06-05' else 'no'))
u = 'https://dps.psx.com.pk/download/attachment/279989-1.pdf'  # corrigendum PSX/N-884: BRRG reinstated
rows.append(('KMI_ALL', '2026-07-15', '2026-07-16', 'BRRG', 'add', u, 'corrigendum PSX/N-884'))
log.append(('KMI_ALL', '2026-07-15', '2026-07-16', u, 'no'))
shutil.copy('data/kmi_allshare_2026-06-05.csv', 'data/index_members/KMI_ALL_2026-06-05.csv')

def tbl(f, start, stop):
    out, on = [], False
    for pg in pdfplumber.open(D + f).pages:
        for l in (pg.extract_text() or '').split('\n'):
            if start in l: on = True; continue
            if on and l.startswith(stop): return out
            m = re.match(r'^\d+ ([A-Z][A-Z0-9]+) (.+)$', l)
            if on and m: out.append((m.group(1), m.group(2)))
    return out
for f, ann, eff, ins, outs, url in [
 ('Notice-KMI30-Index-Nov-14-2025-merged.pdf', '2025-11-14', '2025-11-24',
  ['Sui Southern Gas Company Limited', 'Fauji Fertilizer Company Limited', 'GlaxoSmithKline Pakistan', 'National Refinery Limited', 'Air Link Communication Limited', 'Citi Pharma Limited', 'Cnergyico PK Limited'],
  ['Octopus Digital Limited', 'Pioneer Cement Limited', 'Honda Atlas Cars (Pakistan) Limited', 'NetSol Technologies Limited', 'Faysal Bank Limited', 'Avanceon Limited', 'The Organic Meat Company Limited'],
  U + 'Notice-KMI30-Index-Nov-14-2025-merged.pdf'),
 ('psx_277332-1.pdf', '2026-05-15', '2026-05-25', ['Nishat Mills Limited', 'Treet Corporation Limited', 'Honda Atlas Cars (Pakistan) Limited'],
  ['Cnergyico PK Limited', 'GlaxoSmithKline Pakistan Limited', 'Millat Tractors Limited'], 'https://dps.psx.com.pk/download/attachment/277332-1.pdf')]:
    rows += [('KMI30', ann, eff, sym(n), 'add', url, n) for n in ins] + [('KMI30', ann, eff, sym(n), 'delete', url, n) for n in outs]
    m = tbl(f, 'Constituent Companies', 'Note')
    assert len(m) == 30, (f, len(m))
    pd.DataFrame(m, columns=['symbol', 'company']).to_csv(f'data/index_members/KMI30_{eff}.csv', index=False)
    log.append(('KMI30', ann, eff, url, 'yes'))
f = 'Notice-KSE-30-Index-Recomposition-June-2026.pdf'; url = U + f
rows += [('KSE30', '2026-07-31', '2026-09-15', sym(n), 'add', url, n) for n in ['Pakistan Telecommunication Company Ltd', 'Bank Alfalah Limited', 'K-Electric Limited', 'Fatima Fertilizer Company Limited']]
rows += [('KSE30', '2026-07-31', '2026-09-15', sym(n), 'delete', url, n) for n in ['Air Link Communication Limited', 'Ghandhara Automobiles Limited', 'Ghandhara Industries Limited', 'Sui Southern Gas Company Limited']]
m = tbl(f, 'Constituent Companies', 'Strategy'); assert len(m) == 30
pd.DataFrame(m, columns=['symbol', 'company']).to_csv('data/index_members/KSE30_2026-09-15.csv', index=False)
log.append(('KSE30', '2026-07-31', '2026-09-15', url, 'yes'))

if os.path.exists('scripts/idx_build_ext.py'): exec(open('scripts/idx_build_ext.py').read())  # later-found notices, MSCI, FTSE

ch = pd.DataFrame(rows, columns=['index', 'announce_date', 'effective_date', 'symbol', 'action', 'source_url', 'note'])
ch.sort_values(['index', 'effective_date', 'action', 'symbol']).drop(columns='note').to_csv('data/index_changes.csv', index=False)
pd.DataFrame(log, columns=['index', 'announce_date', 'effective_date', 'source_url', 'full_list_available']).sort_values(['index', 'effective_date']).to_csv('data/index_recomp_log.csv', index=False)
print(len(ch), len(log)); print('UNMAPPED', unm)
