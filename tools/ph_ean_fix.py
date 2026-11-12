# -*- coding: utf-8 -*-
"""Haalt prijsmetingen weg die bij een eerdere EAN van dezelfde plek in de gids horen (12 nov 2026).
Wie een product of variant wisselt zonder 'synced' weg te halen, neemt de geschiedenis van de oude listing mee
en krijgt een nepdaling op /aanbiedingen/, in de dealvideo en in de Black Friday-cijfers.
Toets: een meting van vóór de eerste dag waarop deze EAN in de git-geschiedenis van data/ gemeten is, hoort er niet bij.
Zet ook ph_ean (bij welke EAN de geschiedenis hoort), zodat bol_sync.py een latere wissel zelf ziet.
Gebruik: python3 tools/ph_ean_fix.py [--droog]"""
import os, sys, json, glob, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROOG = "--droog" in sys.argv
commits = subprocess.check_output(["git", "-C", ROOT, "log", "--format=%H", "--", "data"]).decode().split()
blobs = set()
for c in commits:
    for line in subprocess.check_output(["git", "-C", ROOT, "ls-tree", c, "data/"]).decode().splitlines():
        meta, f = line.split("\t")
        if f.endswith(".json"): blobs.add(meta.split()[2])
out = subprocess.run(["git", "-C", ROOT, "cat-file", "--batch"], input="\n".join(blobs).encode(), capture_output=True).stdout
i = 0; first = {}
while i < len(out):
    j = out.index(b"\n", i); size = int(out[i:j].split()[2]); raw = out[j + 1:j + 1 + size]; i = j + 2 + size
    try: g = json.loads(raw)
    except Exception: continue
    for p in g.get("products", []):
        if p.get("ean") and p.get("synced") and p.get("price"):
            k = str(p["ean"]); first[k] = min(first.get(k, "9"), p["synced"])
n = weg = 0
for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
    g = json.load(open(f, encoding="utf-8")); ch = False
    for nr, p in enumerate(g["products"], 1):
        ph = p.get("ph") or {}
        if not ph or not p.get("ean"): continue
        k = str(p["ean"]); f0 = first.get(k) or p.get("synced") or "9"
        vreemd = [d for d in ph if d < f0]
        if vreemd:
            print("  %s #%d %s %s: %d van %d metingen van een eerdere listing (EAN sinds %s)" % (g["slug"], nr, p["brand"], p["name"], len(vreemd), len(ph), f0))
            p["ph"] = {d: v for d, v in sorted(ph.items()) if d >= f0}
            for x in ("prev_price", "prev_date", "low_price"): p.pop(x, None)
            if p["ph"]:
                p["low_price"] = min(p["ph"].values())
                ds = sorted(d for d, v in p["ph"].items() if abs(v - p["price"]) >= 0.01)
                if ds: p["prev_price"] = p["ph"][ds[-1]]; p["prev_date"] = ds[-1]
            n += 1; weg += len(vreemd); ch = True
        if p.get("ph_ean") != k: p["ph_ean"] = k; ch = True
    if ch and not DROOG:
        json.dump(g, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ph_ean_fix: %d producten, %d metingen van een eerdere listing weggehaald%s" % (n, weg, " (droog, niets geschreven)" if DROOG else ""))
