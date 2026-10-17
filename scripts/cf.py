from curl_cffi import requests as cr
def get(url, **kw):
    kw.setdefault("timeout", 25)
    return cr.get(url, impersonate="chrome", **kw)
