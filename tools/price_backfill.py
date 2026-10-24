# -*- coding: utf-8 -*-
"""Eenmalig (24 okt 2026): vult de prijsgeschiedenis (ph, low_price, prev_price) per product uit eerdere commits van data/*.json.
Alleen prijzen met een synced-datum tellen: dat zijn echt gemeten bol-prijzen. Koppeling op EAN, zodat een vervangen product geen 'korting' krijgt."""
import os, json, glob, subprocess, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cut = (datetime.date.today() - datetime.timedelta(days=60)).isoformat()
hist = {}
commits = subprocess.check_output(["git", "-C", ROOT, "log", "--format=%H", "--", "data"]).decode().split()
# alle unieke blobs van data/*.json in een keer via git cat-file --batch (snel)
blobs = set()
for c in commits:
    for line in subprocess.check_output(["git", "-C", ROOT, "ls-tree", c, "data/"]).decode().splitlines():
        meta, f = line.split("\t")
        if f.endswith(".json"): blobs.add(meta.split()[2])
out = subprocess.run(["git", "-C", ROOT, "cat-file", "--batch"], input="\n".join(blobs).encode(), capture_output=True).stdout
i = 0; docs = []
while i < len(out):
    j = out.index(b"\n", i); size = int(out[i:j].split()[2]); docs.append(out[j + 1:j + 1 + size]); i = j + 2 + size
for raw in docs:
        try: g = json.loads(raw)
        except Exception: continue
        for p in g.get("products", []):
            if p.get("ean") and p.get("synced") and p.get("price") and p["synced"] >= cut:
                hist.setdefault(str(p["ean"]), {}).setdefault(p["synced"], float(p["price"]))
n = 0
for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
    g = json.load(open(f, encoding="utf-8")); ch = False
    for p in g["products"]:
        h = dict(hist.get(str(p.get("ean")), {}))
        if not h: continue
        h.update(p.get("ph") or {})
        if p.get("synced"): h[p["synced"]] = p["price"]
        p["ph"] = dict(sorted(h.items()))
        p["low_price"] = min(p["ph"].values())
        ds = sorted(d for d, v in p["ph"].items() if abs(v - p["price"]) >= 0.01 and d < (p.get("synced") or "9"))
        if ds: p["prev_price"] = p["ph"][ds[-1]]; p["prev_date"] = ds[-1]
        ch = True; n += 1
    if ch: json.dump(g, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("backfill: %d producten met geschiedenis uit %d commits" % (n, len(commits)))
