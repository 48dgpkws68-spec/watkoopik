# -*- coding: utf-8 -*-
"""Zoek in de bol-catalogus (Marketing Catalog API). Gebruik: python3 tools/bol_search.py "zoekterm" [aantal]
Toont per resultaat: EAN, prijs, beoordeling, titel. Handig om de juiste EAN voor een product te vinden."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bol_sync as b
q = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
tok = b.token()
r = b.get(tok, "/products/search", {"search-term": q, "country-code": "NL", "page-size": min(50, n), "include-image": "true", "include-offer": "true", "include-rating": "true"})
for x in (r or {}).get("results", [])[:n]:
    off = x.get("offer") or {}; rt = x.get("rating") or {}
    print("%s | %s | %s | %s" % (x.get("ean"), ("€ %s" % off["price"]) if off.get("price") else "geen aanbod", rt.get("average", "-") if isinstance(rt, dict) else rt, (x.get("title") or "")[:110]))
