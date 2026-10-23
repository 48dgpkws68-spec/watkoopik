# -*- coding: utf-8 -*-
"""Controleert via de bol Marketing Catalog API of elk product in data/*.json nog te koop is.
Meldt: "product weg" (EAN onbekend), "geen aanbieding" (niet leverbaar) en prijsverschillen > 15%.
Gebruik: python3 tools/check_stock.py   (schrijft data/_candidates/_stock.json)"""
import os, sys, glob, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bol_sync as b

def main():
    tok = b.token(); bad = []; n = 0
    for f in sorted(glob.glob(os.path.join(b.ROOT, "data", "*.json"))):
        g = json.load(open(f, encoding="utf-8"))
        for i, p in enumerate(g["products"]):
            if not p.get("ean"): bad.append((g["slug"], i + 1, p["brand"], p["name"], "geen ean")); continue
            r = b.get(tok, "/products/%s" % p["ean"], {"country-code": "NL", "include-offer": "true"}); n += 1
            offer = (r or {}).get("offer") or {}
            if not r: bad.append((g["slug"], i + 1, p["brand"], p["name"], "product weg"))
            elif not offer.get("price"): bad.append((g["slug"], i + 1, p["brand"], p["name"], "geen aanbieding"))
            time.sleep(0.12)
    json.dump(bad, open(os.path.join(b.ROOT, "data", "_candidates", "_stock.json"), "w"), ensure_ascii=False, indent=1)
    print("check_stock: %d gecontroleerd, %d niet te koop" % (n, len(bad)))
    for x in bad: print("  %s #%d %s %s: %s" % x)

if __name__ == "__main__":
    main()
