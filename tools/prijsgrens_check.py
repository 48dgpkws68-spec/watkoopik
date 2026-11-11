# -*- coding: utf-8 -*-
"""Controleert 'onder X euro'-gidsen: staat elk product met zijn dagprijs echt onder de grens uit de slug?
Gebruik: python3 tools/prijsgrens_check.py [--stil]
Schrijft _src/prijsgrens.json (overtreders per gids) en toont ze. Exitcode 0, ook bij overtreders (de build mag doorgaan)."""
import os, re, sys, json, glob, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def grens(slug):
    m = re.search(r"-onder-(\d+)(?:-euro)?$", slug)
    return int(m.group(1)) if m else None


def check():
    uit = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
        g = json.load(open(f, encoding="utf-8"))
        slug = g.get("slug") or os.path.basename(f)[:-5]
        gr = grens(slug)
        if not gr:
            continue
        for i, p in enumerate(g.get("products") or [], 1):
            pr = p.get("price")
            if pr is None:
                uit.append({"slug": slug, "grens": gr, "plek": i, "product": "%s %s" % (p.get("brand", ""), p.get("name", "")), "prijs": None, "ean": p.get("ean"), "reden": "geen prijs"})
            elif float(pr) >= gr:
                ph = p.get("ph") or {}
                uit.append({"slug": slug, "grens": gr, "plek": i, "product": "%s %s" % (p.get("brand", ""), p.get("name", "")), "prijs": float(pr), "ean": p.get("ean"),
                            "laagste_30d": min(ph.values()) if ph else None, "dagen_boven": sum(1 for v in ph.values() if v >= gr), "dagen_gemeten": len(ph), "reden": "boven grens"})
    return uit


if __name__ == "__main__":
    uit = check()
    json.dump({"datum": datetime.date.today().isoformat(), "overtreders": uit}, open(os.path.join(ROOT, "_src", "prijsgrens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--stil" not in sys.argv:
        for x in uit:
            print("%-45s #%-2d %-50s %s (grens %d, %s/%s dagen boven)" % (x["slug"], x["plek"], x["product"][:50], x["prijs"], x["grens"], x.get("dagen_boven", "-"), x.get("dagen_gemeten", "-")))
    print("Prijsgrens: %d product(en) boven de grens in %d gids(en)" % (len(uit), len({x["slug"] for x in uit})))
