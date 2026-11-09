# -*- coding: utf-8 -*-
"""D3-toets (groeimotor, 9 nov 2026): bol's top 10 op populariteit voor gidsen waarvan geen enkel product in bol's top 100 staat.
Leest _src/bolpopulair.json, slaat cadeaugidsen over (brede zoektermen) en schrijft _src/d3_kandidaten.json
{slug: {"datum", "query", "top": [{"plek", "ean", "titel", "soort", "url"}]}}. Zoeken geeft geen prijs; die haalt de verbeterronde zelf. Alleen input voor de verbeterronde; build.py gebruikt het niet.
Gebruik: python3 tools/bol_top_d3.py [slug ...]"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bol_sync as b

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POP = json.load(open(os.path.join(ROOT, "_src", "bolpopulair.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "_src", "d3_kandidaten.json")
SKIP = ("cadeau", "sinterklaas", "kerst")
want = set(sys.argv[1:]) or {s for s, v in POP.items() if not v.get("plek") and not any(k in s for k in SKIP)}

def soort(x):
    return next((c["name"] for c in x.get("gpc", []) if c.get("level") == "CHUNK"), None)

tok = b.token(); res = {}
for slug in sorted(want):
    q = POP[slug]["query"]
    r = b.get(tok, "/products/search", {"search-term": q, "country-code": "NL", "page-size": 10, "page": 1, "sort": "POPULARITY"})
    xs = (r or {}).get("results", [])
    res[slug] = {"datum": datetime.date.today().isoformat(), "query": q,
                 "top": [{"plek": i + 1, "ean": str(x.get("ean")), "titel": x.get("title"), "soort": soort(x), "url": x.get("url")} for i, x in enumerate(xs)]}
    print("%-45s %s" % (slug, " | ".join((t["titel"] or "?")[:40] for t in res[slug]["top"][:3])))
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
print("klaar: %d gidsen -> %s" % (len(res), OUT))
