# -*- coding: utf-8 -*-
"""Haalt via de bol Marketing Catalog API per product de EAN, productpagina, foto, dagprijs en beoordeling op
en schrijft ze in data/*.json (velden: ean, url, image, price, rating, reviews, synced).
Gebruik: python3 tools/bol_sync.py [--all]   (standaard alleen producten zonder ean of ouder dan 1 dag)
Credentials in tools/.bol_credentials (regel 1 client id, regel 2 client secret); staat in .gitignore."""
import os, sys, json, glob, time, base64, datetime, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED = os.path.join(ROOT, "tools", ".bol_credentials")
API = "https://api.bol.com/marketing/catalog/v1"
TODAY = datetime.date.today().isoformat()
FORCE = "--all" in sys.argv

def token():
    cid, sec = [l.strip() for l in open(CRED).read().splitlines()[:2]]
    req = urllib.request.Request("https://login.bol.com/token?grant_type=client_credentials", method="POST",
                                 headers={"Accept": "application/json", "Authorization": "Basic " + base64.b64encode(("%s:%s" % (cid, sec)).encode()).decode()})
    return json.load(urllib.request.urlopen(req))["access_token"]

def get(tok, path, params):
    url = API + path + "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"Accept": "application/json", "Accept-Language": "nl-NL", "Authorization": "Bearer " + tok})
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(req))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(2 + attempt * 3); continue
            if e.code == 404: return None
            raise
    return None

def search(tok, term):
    r = get(tok, "/products/search", {"search-term": term, "country-code": "NL", "page-size": 5, "include-image": "true", "include-offer": "true", "include-rating": "true"})
    return (r or {}).get("results") or (r or {}).get("products") or []

def pick(results, p):
    """Kies het resultaat waarvan de titel merk en modelnaam bevat; anders het eerste."""
    want = [w.lower() for w in (p["brand"] + " " + p["name"]).replace("/", " ").split() if len(w) > 2]
    best, score = None, -1
    for r in results:
        t = (r.get("title") or "").lower()
        s = sum(1 for w in want if w in t)
        if s > score: best, score = r, s
    return best if score >= max(1, len(want) // 2) else None

def main():
    tok = token(); t0 = time.time(); done = skipped = miss = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
        g = json.load(open(f, encoding="utf-8")); changed = False
        for p in g["products"]:
            if not FORCE and p.get("synced") == TODAY: skipped += 1; continue
            if time.time() - t0 > 3000: tok = token(); t0 = time.time()
            r = None
            if p.get("ean"):
                r = get(tok, "/products/%s" % p["ean"], {"country-code": "NL", "include-image": "true", "include-offer": "true", "include-rating": "true"})
            if not r:
                r = pick(search(tok, p.get("search") or "%s %s" % (p["brand"], p["name"])), p)
            if not r: miss += 1; print("  geen match:", g["slug"], p["brand"], p["name"]); continue
            p["ean"] = r.get("ean", p.get("ean"))
            if r.get("url"): p["url"] = r["url"]
            if r.get("image", {}).get("url"): p["image"] = r["image"]["url"]
            offer = r.get("offer") or {}
            if offer.get("price"): p["price"] = float(offer["price"])
            rating = r.get("rating")
            if isinstance(rating, dict):
                if rating.get("count"): p["reviews"] = "%s reviews" % format(int(rating["count"]), ",").replace(",", ".")
            p["synced"] = TODAY; changed = True; done += 1
            time.sleep(0.25)
        if changed:
            json.dump(g, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("bol_sync: %d bijgewerkt, %d overgeslagen, %d zonder match" % (done, skipped, miss))

if __name__ == "__main__":
    if not os.path.exists(CRED): sys.exit("geen credentials in " + CRED)
    main()
