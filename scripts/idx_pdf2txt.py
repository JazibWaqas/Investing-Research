import pdfplumber, glob, os
for f in glob.glob('data/raw/index_pdfs/*.pdf'):
    o='C:/Users/JAZIBW~1/AppData/Local/Temp/claude/c--Users-JazibWaqas-Documents-GitHub-Investing-Research/5316537c-aaaf-4ab3-8e6d-fb307ab5b1ed/scratchpad/txt/'+os.path.basename(f)[:-4]+'.txt'
    if os.path.exists(o): continue
    try:
        with pdfplumber.open(f) as p: t='\n'.join((pg.extract_text() or '') for pg in p.pages)
    except Exception as e: t='ERR '+str(e)
    open(o,'w',encoding='utf8').write(t)
