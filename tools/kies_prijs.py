#!/usr/bin/env python3
"""Zet prijzen tussen haakjes in het veld 'kies' gelijk aan de actuele productprijs (verbeterronde 26 nov 2026).
De keuzehulp noemt producten als 'nr. 8 Hisense 55E8S (€ 549)'; na een prijswijziging via bol_sync liep die tekst achter.
Gebruik: python3 tools/kies_prijs.py          (alleen melden)
         python3 tools/kies_prijs.py --fix    (haakjesprijzen bijwerken; losse bedragen in zinnen alleen melden)"""
import json, glob, os, re, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FIX = "--fix" in sys.argv
def eur(v):
    return "{:,}".format(int(round(v))).replace(",", ".")
def num(s):
    return int(s.replace(".", ""))
tot_fix = tot_los = 0
for f in sorted(glob.glob(os.path.join(D, "beste-*.json"))):
    g = json.load(open(f, encoding="utf-8")); k = g.get("kies")
    if not k: continue
    prods = g["products"]; prices = {int(round(p.get("price") or 0)) for p in prods}
    changed = False; los = []
    def fixtext(t, rank=None):
        global tot_fix
        out = []; pos = 0
        for m in re.finditer(r"\(€ ([\d.]+)\)", t):
            old = num(m.group(1)); pre = t[max(0, m.start() - 90):m.start()]
            # dichtstbijzijnde 'nr. N' voor de prijs, anders de productnaam, anders de rank van het blok
            r = None
            nrs = list(re.finditer(r"[Nn]r\. (\d+)", pre))
            if nrs: r = int(nrs[-1].group(1))
            elif rank: r = rank
            else:
                # geen 'nr. N': alleen een token met een cijfer dat bij precies 1 product hoort
                best = -1
                for i, p in enumerate(prods, 1):
                    for key in p.get("name", "").split():
                        if len(key) >= 4 and re.search(r"\d", key) and sum(key in q.get("name", "") for q in prods) == 1:
                            j = pre.rfind(key)
                            if j > best: best = j; r = i
            new = int(round(prods[r - 1].get("price") or 0)) if r and r <= len(prods) else None
            out.append(t[pos:m.start()])
            if new and new != old:
                out.append("(€ %s)" % eur(new)); tot_fix += 1
                print("%s: nr. %d (€ %s) -> (€ %s)" % (g["slug"], r, m.group(1), eur(new)))
            else:
                out.append(m.group(0))
            pos = m.end()
        out.append(t[pos:])
        return "".join(out)
    for x in k.get("keuzes", []):
        n = fixtext(x["p"])
        if n != x["p"]: changed = True; x["p"] = n
    for w in k.get("wanneer", []):
        n = fixtext(w["p"], w.get("rank"))
        if n != w["p"]: changed = True; w["p"] = n
    for x in k.get("keuzes", []) + k.get("wanneer", []):
        for m in re.finditer(r"(?<!\()€ ([\d.]+)(?!\d)", x["p"]):
            if num(m.group(1)) not in prices:
                los.append("…" + x["p"][max(0, m.start() - 45):m.end() + 25] + "…")
    if los:
        tot_los += len(los)
        print("%s: %d los bedrag(en) nakijken" % (g["slug"], len(los)))
        for l in los: print("    " + l)
    if changed and FIX:
        json.dump(g, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("kies-prijzen: %d haakjesprijs(en) %s, %d los bedrag(en) nakijken" % (tot_fix, "bijgewerkt" if FIX else "wijken af", tot_los))
