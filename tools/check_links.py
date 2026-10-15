# -*- coding: utf-8 -*-
"""Controleert alle bol-links in de gebouwde site.
- elke bol-link moet via partner.bol.com/click met site-code 1549706 lopen
- steekproef: de partnerlink moet doorsturen naar bol met de trackingcode
Gebruik: python3 tools/check_links.py [aantal-steekproeven]"""
import os, re, sys, glob, random, urllib.parse, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ID = "1549706"
n_sample = int(sys.argv[1]) if len(sys.argv) > 1 else 10
links, bad, direct = set(), [], []
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(("_src", "brand", "build_v1")): continue
    h = open(f, encoding="utf-8").read()
    for u in re.findall(r'href="([^"]+)"', h):
        u = u.replace("&amp;", "&")
        if "partner.bol.com/click" in u:
            q = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
            if q.get("s") != [SITE_ID] or not q.get("url", [""])[0].startswith("https://www.bol.com/"): bad.append((rel, u[:90]))
            else: links.add(u)
        elif "bol.com" in u: direct.append((rel, u[:90]))
print("unieke partnerlinks: %d | fout: %d | bol-links zonder code: %d" % (len(links), len(bad), len(direct)))
for x in (bad + direct)[:10]: print("  ", x)
random.seed()
fails = 0
for u in random.sample(sorted(links), min(n_sample, len(links))):
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{redirect_url}", u], capture_output=True, text=True).stdout
    code, _, loc = r.partition(" ")
    ok = code in ("301", "302") and SITE_ID in loc and "bol.com" in loc
    fails += not ok
    if not ok: print("  STEEKPROEF FOUT:", code, loc[:90])
print("steekproef: %d van %d doorverwijzingen correct" % (min(n_sample, len(links)) - fails, min(n_sample, len(links))))
sys.exit(1 if (bad or direct or fails) else 0)
