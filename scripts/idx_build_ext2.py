# Executed from idx_build_ext.py. MSCI / FTSE Pakistan changes read from Pakistani press coverage (Profit by Pakistan Today, Business Recorder, Mettis Global, ProPakistani).
# index MSCI_PK = MSCI Pakistan Index (standard: Emerging Markets constituents until Nov-2021, Frontier Markets Index afterwards); MSCI_PK_SC = MSCI Pakistan Small Cap.
# announce_date is the date the article states for the MSCI announcement, else the article's publication date (so it can be a day late). Blank effective = not stated in the article.
PR = 'https://profit.pakistantoday.com.pk/'
def ms(ann, eff, url, std_add=(), std_del=(), sc_add=(), sc_del=()):
    for ix, a, d in (('MSCI_PK', std_add, std_del), ('MSCI_PK_SC', sc_add, sc_del)):
        for n in a: rows.append((ix, ann, eff, sym(n), 'add', url, n))
        for n in d: rows.append((ix, ann, eff, sym(n), 'delete', url, n))
    log.append(('MSCI_PK', ann, eff, url, 'no'))

ms('2017-05-15', '2017-06-01', PR + '2017/05/16/morgan-stanley-upgrades-pakistan-to-emerging-market-status', std_add=['Oil & Gas Development Company Limited', 'Habib Bank Limited', 'United Bank Limited', 'Lucky Cement Limited', 'MCB Bank Limited', 'Engro Corporation Limited'])
ms('2018-05-15', '2018-05-31', PR + '2018/05/16/pakistan-averts-msci-downgrade-weight-in-em-index-to-slightly-fall-post-china-a-shares', sc_del=['Pak Elektron Limited', 'National Refinery Limited', 'IGI Holdings Limited'])
ms('2018-11-14', '2018-11-30', PR + '2018/11/14/pakistan-avoids-demotion-to-frontier-by-msci-ubl-lucky-cement-stocks-demoted', std_del=['United Bank Limited', 'Lucky Cement Limited'], sc_add=['United Bank Limited', 'Lucky Cement Limited'], sc_del=['Honda Atlas Cars (Pakistan) Limited', 'Maple Leaf Cement Factory Limited'])
ms('2019-05-14', '2019-05-28', PR + '2019/05/14/pakistan-retains-upgraded-status-in-msci-emerging-market-index', sc_del=['Fauji Cement Company Limited', 'Fauji Fertilizer Bin Qasim Limited', 'International Steels Limited'])
ms('2019-11-09', '', PR + '2019/11/09/pakistan-maintains-its-msci-emerging-markets-status', sc_del=['D.G. Khan Cement Company Limited', 'Kot Addu Power Company Limited', 'Thal Limited'])
ms('2020-05-13', '2020-05-29', PR + '2020/05/13/pakistan-retains-its-place-in-msci-emerging-markets-index', sc_add=['Mari Petroleum Company Limited', 'Pakistan Petroleum Limited'], sc_del=['Nishat Mills Limited', 'Sui Northern Gas Pipelines Limited'])
ms('2021-05-12', '', 'https://propakistani.pk/2021/05/12/msci-releases-results-of-may-2021-semi-annual-index-review/', std_add=['Lucky Cement Limited'], std_del=['Oil & Gas Development Company Limited'], sc_add=['TRG Pakistan Limited'], sc_del=['Indus Motor Company Limited', 'Lucky Cement Limited', 'National Bank of Pakistan', 'Packages Limited'])
ms('2021-11-11', '2021-11-30', PR + '2021/11/12/msci-adds-three-pakistani-securities-to-frontier-markets-index', std_add=['Habib Bank Limited', 'Lucky Cement Limited', 'MCB Bank Limited'])  # reclassification EM->FM; 14 small-cap additions not named in the source
ms('2022-05', '', PR + '2022/11/14/mcb-out-of-the-msci-frontier-market-pakistan-index-moved-into-small-cap-index', std_add=['Oil & Gas Development Company Limited'], std_del=['Habib Bank Limited'])
ms('2022-11-14', '2022-11-30', PR + '2022/11/14/mcb-out-of-the-msci-frontier-market-pakistan-index-moved-into-small-cap-index', std_del=['MCB Bank Limited'], sc_add=['MCB Bank Limited'])
ms('2023-08-11', '', PR + '2023/08/11/psx-gains-momentum-amid-rising-msci-integration', std_add=['Bank Alfalah Limited', 'Engro Fertilizers Limited', 'Fauji Fertilizer Company Limited', 'Habib Bank Limited', 'The Hub Power Company Limited', 'Lucky Cement Limited', 'Mari Petroleum Company Limited', 'MCB Bank Limited', 'Millat Tractors Limited', 'Pakistan Oilfields Limited', 'Pakistan Petroleum Limited', 'Pakistan State Oil Company Limited', 'Systems Limited', 'TRG Pakistan Limited', 'United Bank Limited'])  # 41 small-cap additions (Business Recorder 40257458) not captured
ms('2024-02-13', '2024-02-29', PR + '2024/02/13/22-pakistani-listed-companies-added-to-msci-indices', std_add=['Bank AL Habib Limited', 'Interloop Limited', 'Sui Northern Gas Pipelines Limited'],
   sc_add=['Adamjee Insurance Company Limited', 'Attock Gen Limited', 'Aisha Steel Mills Limited', 'Askari Bank Limited', 'Century Paper & Board Mills Limited', 'Ferozsons Laboratories Limited', 'Ghandhara Industries Limited', 'Ghani Global Glass Limited', 'Hascol Petroleum Limited', 'IGI Holdings Limited', 'JS Bank Limited', 'Murree Brewery Company Limited', 'Nishat Chunian Limited', 'Pioneer Cement Limited', 'Pakistan Stock Exchange Limited', 'S.G. Fibre Limited', 'Sui Southern Gas Company Limited', 'Treet Corporation Limited', 'Worldcall Telecom Limited'],
   sc_del=['BankIslami Pakistan Limited', 'Fauji Cement Company Limited', 'Pak Suzuki Motor Company Limited', 'Sui Northern Gas Pipelines Limited'])
ms('2024-05-15', '2024-05-31', PR + '2024/05/15/national-bank-of-pakistan-added-to-msci-frontier-market-index', std_add=['National Bank of Pakistan'])
ms('2024-08-12', '2024-08-30', PR + '2024/08/13/six-pakistani-firms-added-to-msci-frontier-market-index-one-to-small-cap-index', std_add=['Sazgar Engineering Works Limited'],
   sc_add=['Atlas Battery Limited', 'Ghandhara Automobiles Limited', 'Habib Sugar Mills Limited', 'Lotte Chemical Pakistan Limited', 'Octopus Digital Limited', 'Soneri Bank Limited'], sc_del=['Hascol Petroleum Limited', 'Sazgar Engineering Works Limited'])
ms('2024-11-06', '2024-11-25', 'https://www.brecorder.com/news/40331223', std_del=['TRG Pakistan Limited'],
   sc_add=['Citi Pharma Limited', 'Crescent Steel & Allied Products Limited', 'Fast Cables Limited', 'Flying Cement Company Limited', 'Pakistan Oxygen Limited', 'Shifa International Hospitals Limited', 'Thatta Cement Company Limited', 'TRG Pakistan Limited'], sc_del=['Fauji Fertilizer Bin Qasim Limited'])
ms('2025-02-12', '2025-02-28', PR + '2025/02/12/two-pakistani-firms-added-to-msci-frontier-markets-index-three-to-small-cap-index', std_add=['Abbott Laboratories (Pakistan) Limited', 'The Searle Company Limited'],
   sc_add=['BF Biosciences Limited', 'Biafo Industries Limited', 'Power Cement Limited'], sc_del=['Air Link Communication Limited', 'Askari Bank Limited', 'Attock Refinery Limited', 'The Searle Company Limited'])
ms('2025-05-14', '2025-05-30', PR + '2025/05/14/msci-adds-7-pakistani-companies-in-may-2025-review-raises-countrys-frontier-market-weight', std_add=['Fauji Cement Company Limited', 'D.G. Khan Cement Company Limited', 'Maple Leaf Cement Factory Limited'],
   sc_add=['Archroma Pakistan Limited', 'At-Tahur Limited', 'Engro Polymer & Chemicals Limited', 'Pakistan Reinsurance Company Limited'], sc_del=['AGP Limited', 'Agritech Limited', 'D.G. Khan Cement Company Limited'])  # third small-cap deletion in the article is DGKC moving to the main index
ms('2025-11-06', '2025-11-24', PR + '2025/11/06/msci-adds-three-pakistani-banks-to-frontier-market-index-in-november-2025-review', std_add=['Askari Bank Limited', 'The Bank of Punjab', 'Meezan Bank Limited'],
   sc_add=['AGP Limited', 'Big Bird Foods Limited', 'Gatron (Industries) Limited', 'Ghani Chemical Industries Limited', 'Ghani Global Holdings Limited', 'International Packaging Films Limited', 'Ittehad Chemicals Limited', 'Javedan Corporation Limited', 'Sitara Chemical Industries Limited', 'SPEL Limited', 'The Organic Meat Company Limited'],
   sc_del=['Atlas Battery Limited', 'The Bank of Punjab'])
ms('2026-02-11', '2026-02-27', 'https://mettisglobal.news/MSCI-Index-Review-Abbott-exits-SEPL-ZAL-enter-MSCI-fold-58327', std_del=['Abbott Laboratories (Pakistan) Limited'], sc_add=['Security Papers Limited', 'Zarea Limited'], sc_del=['Lalpir Power Limited'])
ms('2026-05-13', '2026-05-29', 'https://mettisglobal.news/Habib-Metro-joins-MSCI-Frontier-Searle-demoted-Murree-dropped-60407', std_add=['Habib Metropolitan Bank Limited'], std_del=['The Searle Company Limited'],
   sc_add=['Crescent Textile Mills Limited', 'Highnoon Laboratories Limited', 'The Searle Company Limited'], sc_del=['Murree Brewery Company Limited'])
ms('2026-08-12', '2026-08-31', PR + '2026/08/13/msci-adds-air-link-removes-biafo-from-pakistans-fm-small-cap-index', sc_add=['Air Link Communication Limited'], sc_del=['Biafo Industries Limited'])

# FTSE: only one constituent event found
for n in ['Engro Corporation Limited', 'Habib Bank Limited', 'Nishat Mills Limited', 'Mari Petroleum Company Limited', 'Fauji Fertilizer Company Limited', 'The Searle Company Limited']:
    rows.append(('FTSE_PK', '2017-03-03', '2017-03-20', sym(n), 'add', PR + '2017/03/03/six-pakistani-companies-to-be-listed-on-ftse', n))
log.append(('FTSE_PK', '2017-03-03', '2017-03-20', PR + '2017/03/03/six-pakistani-companies-to-be-listed-on-ftse', 'no'))
