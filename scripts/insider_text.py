"""PDF -> (text, method). Text layer via pdfplumber; no text layer -> Windows built-in OCR (winocr) on a 200dpi render, words regrouped into rows by y.
(rapidocr-onnxruntime was tried first: 12-20 s a page on this machine, vs 0.4 s for winocr.)"""
import pdfplumber, winocr


def ocr_lines(img):
    r = winocr.recognize_pil_sync(img.convert("RGB"), "en")
    ws = sorted(((w["bounding_rect"]["y"] + w["bounding_rect"]["height"] / 2, w["bounding_rect"]["x"], w["bounding_rect"]["height"], w["text"])
                 for l in r["lines"] for w in l["words"]))
    lines, cur, cy, ch = [], [], None, 0
    for y, x, h, t in ws:
        if cy is not None and abs(y - cy) > max(ch, h) * 0.55:
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
            return "\n".join(ocr_lines(pg.to_image(resolution=200).original) for pg in pages), "ocr"
    except Exception as e:
        return "", f"error:{type(e).__name__}"
