# -*- coding: utf-8 -*-
"""Haal alleen de bol-score (gemiddelde 1-5) op per product met EAN, zonder prijzen te raken.
Schrijft rating + reviews ('bol-score 4,6 van 5' of leeg) via bol_sync.set_rating. Groeimotor 17 nov 2026.
Gebruik: python3 tools/bol_rating.py [--droog]"""
import os, sys, json, glob, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bol_sync as b
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROOG = "--droog" in sys.argv
tok = b.token()

def fetch(ean):
    for _ in range(3):
        try:
            r = b.get(tok, "/products/%s" % ean, {"country-code": "NL", "include-rating": "true"})
            return ean, (r or {}).get("rating"), bool(r)
        except Exception:
            time.sleep(2)
    return ean, None, False

files = sorted(glob.glob(os.path.join(ROOT, "data", "*.json")))
eans = sorted({p["ean"] for f in files for p in json.load(open(f, encoding="utf-8"))["products"] if p.get("ean")})
res = {}
with ThreadPoolExecutor(4) as ex:
    for ean, rt, ok in ex.map(fetch, eans):
        if ok: res[ean] = rt
print("EAN's: %d, antwoord: %d, met score: %d" % (len(eans), len(res), sum(1 for v in res.values() if v)))
gezet = leeg = onbekend = 0
for f in files:
    g = json.load(open(f, encoding="utf-8")); ch = False
    for p in g["products"]:
        old = (p.get("reviews"), p.get("rating"))
        if p.get("ean") in res: b.set_rating(p, res[p["ean"]])
        else: onbekend += 1; p["reviews"] = p["reviews"] if str(p.get("reviews", "")).startswith("bol-score ") else ""
        if p.get("rating"): gezet += 1
        else: leeg += 1
        ch |= old != (p.get("reviews"), p.get("rating"))
    if ch and not DROOG: json.dump(g, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("producten met bol-score: %d, zonder: %d (waarvan geen EAN/antwoord: %d)%s" % (gezet, leeg, onbekend, " [droog]" if DROOG else ""))
