# -*- coding: utf-8 -*-
"""Haalt via de bol Marketing Catalog API per product de EAN, productpagina, foto, dagprijs en beoordeling op
en schrijft ze in data/*.json (velden: ean, url, image, price, rating, reviews, synced).
Gebruik: python3 tools/bol_sync.py [--all]   (standaard alleen producten zonder ean of ouder dan 1 dag)
Credentials in tools/.bol_credentials (regel 1 client id, regel 2 client secret); staat in .gitignore."""
import os, re, sys, json, glob, time, base64, datetime, urllib.request, urllib.parse

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

_FRESH = {}  # bol-tokens verlopen na ~5 min: bij 401 automatisch vernieuwen

def get(tok, path, params):
    url = API + path + "?" + urllib.parse.urlencode(params, doseq=True)
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"Accept": "application/json", "Accept-Language": "nl-NL", "Authorization": "Bearer " + _FRESH.get("tok", tok)})
        try:
            return json.load(urllib.request.urlopen(req))
        except urllib.error.HTTPError as e:
            if e.code == 401: _FRESH["tok"] = token(); continue
            if e.code == 429: time.sleep(2 + attempt * 3); continue
            if e.code == 404: return None
            raise
    return None

def search(tok, term):
    r = get(tok, "/products/search", {"search-term": term, "country-code": "NL", "page-size": 10, "include-image": "true", "include-offer": "true", "include-rating": "true"})
    return (r or {}).get("results") or (r or {}).get("products") or []

BAD = ("filter", "geschikt voor", "compatibel", "hoes", "accessoire", "onderdeel", "vervang", "set van", "stuks", "zak", "borstel", "houder", "kabel", "oplader", "adapter", "cover", "bescherm", "mondstuk", "opzet", "reserve", "navul", "cartridge", "sticker", "standaard", "stand ")

BAD = ("filter", "geschikt voor", "compatibel", "hoes", "accessoire", "onderdeel", "vervang", "set van", "stuks", "stofzak", "houder", "kabel", "oplader", "adapter", "cover", "bescherm", "mondstuk", "opzet", "reserve", "navul", "cartridge", "sticker")
VARIANTS = ("pro", "plus", "max", "ultra", "lite", "mini", "dual", "complete", "premium", "xxl", "kids", "submarine")

def norm(t): return re.sub(r"[^a-z0-9]", "", t.lower())

def strict_ok(p, title):
    """Streng: elk modelnummer (token met cijfer) uit onze naam moet in de bol-titel staan; zonder modelnummer minstens 80% van de woorden."""
    t = norm(title); name = p["name"].replace("/", " ")
    toks = [w for w in re.split(r"[\s,()]+", name) if w]
    models = [norm(w) for w in toks if re.search(r"\d", w) and len(norm(w)) >= 2 and not re.fullmatch(r"\d{2,3}x\d{2,3}|\d+(cm|mm|l|w|kg|inch|liter|watt)", norm(w))]
    tl = re.split(r" [-|\u2013\u2014] ", title)[0].lower(); nl = p["name"].lower()  # alleen het naamdeel vóór het eerste streepje
    if p["brand"].lower().split()[0] not in title.lower(): return False
    if any(b in tl for b in BAD if b not in nl): return False
    # losse versienummers in de bol-naam die niet in onze naam staan (bv. "Curv 2", "Series 11") wijzen op een ander model
    clean = lambda x: re.sub(r"/\d+|\d+[.,]\d+|-\d", " ", x)
    name_nums = set(re.findall(r"\b\d{1,2}\b", clean(nl)))
    for n in re.findall(r"\b\d{1,2}\b", clean(tl)):
        if n not in name_nums and not re.search(r"\b%s\s*(mm|cm|l|liter|kg|w|inch|stuks|delig|jaar|x)\b" % n, tl): return False
    for v in VARIANTS:
        if re.search(r"\b%s\b" % v, tl) and not re.search(r"\b%s\b" % v, nl): return False
    if models: return all(m in t for m in models)
    words = [norm(w) for w in toks if len(w) > 2]
    return words and sum(1 for w in words if w in t) / len(words) >= 0.8

def pick(results, p):
    for r in results:
        if strict_ok(p, r.get("title") or ""):
            price = float((r.get("offer") or {}).get("price") or 0)
            if price and p.get("price") and not (0.4 * p["price"] <= price <= 2.5 * p["price"]): continue
            return r
    return None

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
            p["ean"] = r.get("ean", p.get("ean")); p["bol_title"] = r.get("title", p.get("bol_title"))
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
