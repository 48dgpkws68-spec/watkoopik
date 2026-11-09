# -*- coding: utf-8 -*-
"""Plek van onze producten in bol's eigen sortering 'populariteit' (groeimotor S5, 9 nov 2026).
Per gids: zoek op g["query"] met sort=POPULARITY (2 pagina's van 50) en noteer op welke plek onze EAN's staan.
Schrijft _src/bolpopulair.json {slug: {"datum", "query", "plek": {ean: plek}}}; build.py toont het blok "Populair bij bol".
Gebruik: python3 tools/bol_populair.py [slug ...]   (standaard alle gidsen; wekelijks draaien is genoeg)"""
import os, sys, json, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bol_sync as b

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_src", "bolpopulair.json")
TODAY = datetime.date.today().isoformat()
want = set(sys.argv[1:])

try: res = json.load(open(OUT, encoding="utf-8"))
except Exception: res = {}
tok = b.token(); n = 0
for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
    g = json.load(open(f, encoding="utf-8"))
    if want and g["slug"] not in want: continue
    ours = {str(p.get("ean")) for p in g["products"] if p.get("ean")}
    plek, pos = {}, 0
    for pg in (1, 2):
        r = b.get(tok, "/products/search", {"search-term": g["query"], "country-code": "NL", "page-size": 50, "page": pg, "sort": "POPULARITY"})
        xs = (r or {}).get("results", [])
        for x in xs:
            pos += 1
            ean = str(x.get("ean"))
            if ean in ours and ean not in plek: plek[ean] = pos
        if len(xs) < 50: break
    res[g["slug"]] = {"datum": TODAY, "query": g["query"], "plek": plek}
    n += 1
    print("%-50s %2d van %d in top %d" % (g["slug"], len(plek), len(ours), pos))
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
print("klaar: %d gidsen -> %s" % (n, OUT))
