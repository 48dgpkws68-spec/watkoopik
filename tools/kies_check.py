"""Controle veld 'kies' + extra faq (groeimotor N6). Gebruik: python3 tools/kies_check.py beste-x [beste-y ...]"""
import json, re, sys, os
D = os.path.join(os.path.dirname(__file__), "..", "data")
bad = 0
for slug in sys.argv[1:]:
    g = json.load(open(os.path.join(D, slug + ".json"), encoding="utf-8"))
    k = g.get("kies") or {}; err = []
    ks, ws = k.get("keuzes", []), k.get("wanneer", [])
    if not 3 <= len(ks) <= 5: err.append("keuzes moet 3-5 zijn (%d)" % len(ks))
    if sorted(w.get("rank") for w in ws) != [2, 3]: err.append("wanneer moet rank 2 en 3 hebben")
    txt = json.dumps(k, ensure_ascii=False) + json.dumps(g["faq"], ensure_ascii=False)
    if "—" in txt or "–" in txt: err.append("streepje")
    if re.search(r", en\b", txt): err.append("', en'")
    if re.search(r"getest|testsieger|wij testten|zelf geprobeerd", txt, re.I): err.append("getest-claim")
    for x in ks:
        if set(x) != {"h", "p"} or not 25 <= len(x["p"].split()) <= 90: err.append("keuze %r: velden h,p en 25-90 woorden" % x.get("h"))
    for w in ws:
        if not 30 <= len(w.get("p", "").split()) <= 90: err.append("wanneer nr %s: 30-90 woorden" % w.get("rank"))
    if len(g["faq"]) > 10: err.append("te veel faq (%d)" % len(g["faq"]))
    qs = [q["q"] for q in g["faq"]]
    if len(qs) != len(set(qs)): err.append("dubbele faq")
    print(slug, "OK" if not err else "FOUT: " + "; ".join(err)); bad += bool(err)
sys.exit(1 if bad else 0)
