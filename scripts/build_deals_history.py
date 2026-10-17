"""Build data/deals_history.csv: every PSX takeover PAI (plus sponsor delistings) 2018 to Oct 2026.
Deal facts are hand-keyed from PSX filings and press (see source_urls); prices and returns are computed.
Run: .venv/Scripts/python.exe -I scripts/build_deals_history.py
"""
import os, glob
import pandas as pd, numpy as np

D = "https://dps.psx.com.pk/download/document/{}.pdf"
def docs(*ids): return " ".join(D.format(i) for i in ids)

T = "takeover"; L = "delisting"
R = []
def add(*a): R.append(a)
# type, sym, target, acquirer, pai_date, pai_hhmm, offer, pao_date, acc, acc_note, status, end, src, note
