"""PDF -> (text, method). Text layer via pdfplumber; no text layer -> rapidocr on a 150dpi render, boxes regrouped into lines by y."""
import numpy as np, pdfplumber

_ocr = None


def ocr_lines(img):
    global _ocr
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr = RapidOCR()
    res, _ = _ocr(np.array(img.convert("RGB")))
    boxes = sorted(((np.mean([p[1] for p in b]), min(p[0] for p in b), max(p[1] for p in b) - min(p[1] for p in b), t) for b, t, c in (res or [])))
    lines, cur, cy, ch = [], [], None, 0
    for y, x, h, t in boxes:
        if cy is not None and abs(y - cy) > max(ch, h) * 0.6:
            lines.append(" ".join(t_ for _, t_ in sorted(cur))); cur = []
        if not cur:
            cy, ch = y, h
        cur.append((x, t))
    if cur:
        lines.append(" ".join(t_ for _, t_ in sorted(cur)))
    return "\n".join(lines)


def pdf_text(path, max_pages=6):
    try:
        with pdfplumber.open(path) as p:
            pages = p.pages[:max_pages]
            txt = "\n".join(pg.extract_text() or "" for pg in pages)
            if len(txt.strip()) >= 80:
                return txt, "pdf_text"
            return "\n".join(ocr_lines(pg.to_image(resolution=150).original) for pg in pages), "ocr"
    except Exception as e:
        return "", f"error:{type(e).__name__}"
