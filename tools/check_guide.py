# -*- coding: utf-8 -*-
"""Controleert een of meer gids-JSON's op schema en taalregels zonder de site te bouwen.
Gebruik: python3 tools/check_guide.py data/beste-x.json [data/beste-y.json ...]"""
import sys, json, re

def check(path):
    errs = []
    try:
        g = json.load(open(path, encoding="utf-8"))
    except Exception as ex:
        return ["ongeldige JSON: %s" % ex]
    for k in ("slug", "cat", "prio", "title", "short", "query", "keywords", "ico", "updated", "reviews_total", "intro", "verdict", "products", "guide", "faq"):
        if k not in g: errs.append("veld ontbreekt: " + k)
    if g.get("cat") not in ("huishouden", "keuken", "verzorging", "slapen", "elektronica", "wonen", "sport", "kind", "klussen", "computer", "telefoon", "audio", "gaming", "foto", "gezondheid", "huisdieren", "speelgoed", "kantoor", "outdoor", "auto", "reizen", "hobby", "cadeaus"): errs.append("onbekende cat")
    ps = g.get("products", [])
    if len(ps) != 10: errs.append("aantal producten is %d, moet 10 zijn" % len(ps))
    labs = [p.get("label") for p in ps]
    for l in ("Beste keuze", "Beste prijs-kwaliteit", "Beste premium"):
        if labs.count(l) != 1: errs.append("label '%s' komt %d keer voor" % (l, labs.count(l)))
    if ps and labs[0] != "Beste keuze": errs.append("product 1 moet Beste keuze zijn")
    if ps and max(p.get("score", 0) for p in ps) != ps[0].get("score"): errs.append("product 1 moet de hoogste score hebben")
    keys = {tuple(p.get("specs", {}).keys()) for p in ps}
    if len(keys) > 1: errs.append("spec-sleutels verschillen tussen producten")
    for i, p in enumerate(ps):
        for k in ("brand", "name", "price", "score", "reviews", "oneliner", "specs", "pros", "cons", "ideal", "text"):
            if k not in p: errs.append("product %d mist %s" % (i + 1, k))
        n = len(p.get("text", "").split())
        if not 100 <= n <= 200: errs.append("product %d tekst is %d woorden" % (i + 1, n))
    vis = json.loads(json.dumps(g))
    for p in vis.get("products", []):
        for k in ("bol_title", "url", "image", "ean", "synced", "search", "ph", "prev_price", "prev_date", "low_price"): p.pop(k, None)
    blob = json.dumps(vis, ensure_ascii=False)  # alleen zichtbare tekst
    if "—" in blob or "–" in blob: errs.append("bevat een em- of en-dash")
    for m in re.finditer(r".{30}, en\b.{10}", blob): errs.append("komma voor 'en': ..." + m.group(0) + "...")
    if re.search(r"\b(wij|we) (hebben )?(ge)?test", blob, re.I): errs.append("claimt zelf getest te hebben")
    return errs

bad = 0
for p in sys.argv[1:]:
    e = check(p)
    print(("OK   " if not e else "FOUT ") + p)
    for x in e: print("     - " + x)
    bad += bool(e)
sys.exit(1 if bad else 0)
