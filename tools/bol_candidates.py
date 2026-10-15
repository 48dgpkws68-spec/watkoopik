# -*- coding: utf-8 -*-
"""Zoekt voor producten zonder bol-koppeling de beste kandidaten in de bol-catalogus.
Schrijft data/_candidates/<slug>.json: per productnummer (rank) een lijst kandidaten met titel, ean, prijs, url, image.
Gebruik: python3 tools/bol_candidates.py [slug ...]   (zonder slugs: alle gidsen)
Daarna kiest een mens of agent per product de juiste EAN en zet die in data/<slug>.json als "ean"; tools/bol_sync.py haalt dan foto, prijs en link op."""
import os, sys, json, glob, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bol_sync as b

ROOT = b.ROOT
OUT = os.path.join(ROOT, "data", "_candidates")
os.makedirs(OUT, exist_ok=True)

def queries(p):
    name = p["name"]
    qs = [p.get("search") or "%s %s" % (p["brand"], name)]
    codes = [w for w in re.split(r"[\s,()]+", name) if re.search(r"\d", w) and len(w) >= 4]
    for c in codes: qs.append("%s %s" % (p["brand"], c.split("/")[0]))
    words = [w for w in name.split() if not re.search(r"\d", w)]
    if words: qs.append("%s %s" % (p["brand"], " ".join(words[:4])))
    seen, out = set(), []
    for q in qs:
        if q.lower() not in seen: seen.add(q.lower()); out.append(q)
    return out[:3]

def main(slugs):
    tok = b.token()
    files = [os.path.join(ROOT, "data", s + ".json") for s in slugs] if slugs else sorted(glob.glob(os.path.join(ROOT, "data", "*.json")))
    n = 0
    for f in files:
        g = json.load(open(f, encoding="utf-8")); res = {}
        for i, p in enumerate(g["products"]):
            if p.get("image"): continue
            cands, seen = [], set()
            for q in queries(p):
                for r in b.search(tok, q)[:8]:
                    e = r.get("ean")
                    if not e or e in seen: continue
                    seen.add(e)
                    cands.append({"ean": e, "title": (r.get("title") or "")[:140], "price": (r.get("offer") or {}).get("price"),
                                  "url": r.get("url"), "image": (r.get("image") or {}).get("url"), "query": q})
                time.sleep(.25)
            res[str(i + 1)] = {"product": "%s %s" % (p["brand"], p["name"]), "our_price": p["price"], "candidates": cands[:10]}
            n += 1
        if res:
            json.dump({"slug": g["slug"], "missing": res}, open(os.path.join(OUT, g["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("kandidaten opgehaald voor %d producten in %s" % (n, OUT))

if __name__ == "__main__":
    main(sys.argv[1:])
