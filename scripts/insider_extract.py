"""Parse the text of a PSX insider-disclosure PDF (Form-29 style, many layouts) into trade rows.
parse(text, filed, symbol) -> list of dicts. Heuristic, row-based: a row is a line (plus the next line) holding a date, a direction word and
share/price numbers. Name and role come from the row's neighbourhood. Price is checked against the stock's raw high/low around the date.
"""
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MON = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
MONRE = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*"
D_NUM = re.compile(r"(?<!\d)(\d{1,2})\s*[./-]\s*(\d{1,2})\s*[./-]\s*(\d{2,4})(?!\d)")
D_DMY = re.compile(rf"(?<!\d)(\d{{1,2}})(?:st|nd|rd|th)?[\s,-]*{MONRE}[\s,.-]*(\d{{4}})", re.I)
D_MDY = re.compile(rf"\b{MONRE}[\s.]*(\d{{1,2}})(?:st|nd|rd|th)?[\s,-]+(\d{{4}})", re.I)
NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])")
BUYW = re.compile(r"purchas|bought|\bbuy|acqui|\bgift\s*in|\bpurch", re.I)
SELLW = re.compile(r"\bsale|\bsold|\bsell|dispos|\bgift\s*out", re.I)
NAMESKIP = re.compile(r"name|person|descri|detail|relevant|shares?\b|transaction|date|nature|form|market|cumulative|holding|certificate|number|percent|rate|sr\b|no\.|total|subject|dear|yours|the general|pakistan|exchange|regulation|company|limited|ltd|director|executive|secretary|officer|spouse|substantial|disclosure|interest|cdc|physical|ready|through", re.I)


def dates_in(s):
    out = []
    for m in D_NUM.finditer(s):
        d, mo, y = int(m[1]), int(m[2]), int(m[3])
        y += 2000 if y < 100 else 0
        out.append((m.start(), m.end(), d, mo, y))
    for m in D_DMY.finditer(s):
        out.append((m.start(), m.end(), int(m[1]), MON[m[2].lower()[:3]], int(m[3])))
    for m in D_MDY.finditer(s):
        out.append((m.start(), m.end(), int(m[2]), MON[m[1].lower()[:3]], int(m[3])))
    ok = []
    for a, b, d, mo, y in sorted(out):
        try:
            ok.append((a, b, pd.Timestamp(y, mo, d)))
        except ValueError:
            pass
    return ok


@lru_cache(None)
def px(sym):
    f = ROOT / "data/prices_raw" / f"{sym}.csv"
    return pd.read_csv(f, parse_dates=["date"]).set_index("date") if f.exists() else None


def price_ok(sym, d, p):
    """price inside the raw low..high of the symbol within +-3 sessions of d, with 12% slack"""
    df = px(sym)
    if df is None or p is None:
        return None
    i = df.index.searchsorted(d)
    w = df.iloc[max(0, i - 3): i + 4]
    if w.empty or abs((w.index[0] - d).days) > 15:
        return None
    return bool(w.low.min() * 0.88 <= p <= w.high.max() * 1.12)


def num(t):
    try:
        return float(t.replace(",", ""))
    except ValueError:
        return None


def nature(w, doc):
    for k, rx in (("gift", r"gift|inherit|succession|donat|hiba|transmission"), ("rights", r"\bright"), ("esop", r"esop|employee (stock|share)|stock option|option scheme|\bvest"),
                  ("ipo", r"\bipo\b|initial public|public offer|book.?build"), ("buyback", r"buy.?back|tender|repurchase|takeover"), ("bonus", r"bonus"),
                  ("transfer", r"transfer|\bndm\b|negotiable|block|physical|off.?market|inter.?se|pledge|ssl|lien|margin|mutual")):
        if re.search(rx, w, re.I):
            return k
    if re.search(r"ready|\bcdc\b|market|normal|broker|\btre\b|through", w, re.I):
        return "open_market"
    return "unstated"


def roles(w):
    t = w.lower()
    if re.search(r"spouse|wife|husband|minor|\bson\b|daughter|father|mother|brother|sister|dependent|relative", t):
        return "associate"
    if re.search(r"sponsor|promoter", t):
        return "sponsor"
    if re.search(r"substantial|associated (company|undertaking)|10\s*%|more than 10|holding company|major shareholder|shareholder", t):
        return "substantial_shareholder"
    if re.search(r"\bceo\b|chief executive|managing director|\bmd\b", t):
        return "ceo"
    if re.search(r"director|chairman|chairperson", t):
        return "director"
    if re.search(r"secretary|\bcfo\b|chief|executive|\bhead\b|manager|president|\bvp\b|controller|senior|officer|\bgm\b", t):
        return "executive"
    return ""


def clean_name(s):
    s = re.sub(r"\(.*?\)|\(.*$", " ", s)
    s = re.sub(r"\b(cdc|ready|physical|through|market|buy|sale|sold|purchase[d]?|rs\.?|s\.?no|sr\.?)\b", " ", s, flags=re.I)
    s = re.sub(r"^[\s\d.)\-:]+", "", s)
    s = re.sub(r"[^A-Za-z .'&-]", " ", s)
    return " ".join(s.split())


def name_for(lines, i, a):
    """name: letters before the date on the row line; else a name-like line up to 2 above (then 1 below)"""
    pre = clean_name(lines[i][:a])
    if len(pre.split()) >= 2 and not NAMESKIP.search(pre.replace("Mr", "")) or (len(pre.split()) >= 2 and re.match(r"(mr|mrs|ms|dr|syed|m/s)\b", pre, re.I)):
        return pre
    for j in (i - 1, i - 2, i + 1):
        if 0 <= j < len(lines):
            c = clean_name(lines[j])
            if 2 <= len(c.split()) <= 7 and not NAMESKIP.search(c) and not NUM.search(lines[j].replace("(", " ")) :
                return c
    return ""


def parse(text, filed, symbol):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    doc_roles = [roles(l) for l in lines if l.count("/") < 2 and re.search(r"\bby\b.*(mr|mrs|ms|dr)\b", l, re.I)]
    rows = []
    for i, ln in enumerate(lines):
        ds = dates_in(ln)
        if not ds:
            continue
        for a, b, d in ds[:1]:
            if d > filed + pd.Timedelta(days=3) or d < filed - pd.Timedelta(days=800):
                continue
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            prv = lines[i - 1] if i else ""
            row = ln[:a] + " " + ln[b:]
            # number tokens after the date on this line; wrap to the next line if short
            toks = [t for t in NUM.findall(row[len(ln[:a]):]) if num(t) is not None]
            win = ln
            if len(toks) < 2:
                row2 = row + " " + nxt
                toks = [t for t in NUM.findall(row2[len(ln[:a]):]) if num(t) is not None]
                win = ln + " " + nxt
            if len(toks) < 1:
                continue
            ctx = " ".join([prv, ln, nxt])
            sb, ss = BUYW.search(win), SELLW.search(win)
            if not (sb or ss):
                sb, ss = BUYW.search(ctx), SELLW.search(ctx)
            if not (sb or ss):
                continue
            direction = "buy" if sb and (not ss or sb.start() < ss.start()) else "sell"
            vals = [num(t) for t in toks]
            sh = pr = None
            cand = [v for v in vals if v is not None]
            # default layout: shares then price; try swapped if only that fits the market
            if len(cand) >= 2:
                s1, p1 = cand[0], cand[1]
                ok1 = price_ok(symbol, d, p1)
                ok2 = price_ok(symbol, d, s1)
                if ok1 is False and ok2:
                    sh, pr = p1, s1
                else:
                    sh, pr = s1, p1
                    if ok1 is False:   # look for any later token that fits
                        for v in cand[2:]:
                            if price_ok(symbol, d, v):
                                pr = v; break
            else:
                sh = cand[0]
            if sh is not None and (sh < 1 or sh != int(sh)):
                if pr is not None and pr == int(pr) and pr >= 1:
                    sh, pr = pr, sh
                else:
                    continue
            name = name_for(lines, i, a)
            rw = " ".join(l for l in (prv, ln, nxt) if l.count("/") < 3)
            role = roles(rw) or (doc_roles[0] if doc_roles else "")
            nat = nature(" ".join([ln, nxt]), text)
            if nat == "unstated":
                nat = nature(ctx, text)
            ok = price_ok(symbol, d, pr)
            rows.append(dict(trade_date=d, insider_name=name, role=role, direction=direction, shares=sh, price=pr,
                             value_rs=sh * pr if (pr is not None and sh is not None) else None, nature=nat, _price_ok=ok))
    return rows
