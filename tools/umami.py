#!/usr/bin/env python3
"""Umami-cijfers via de publieke share-API (geen login nodig).
Gebruik: python3 tools/umami.py [dagen]   (standaard 7)
          python3 tools/umami.py --save   (stats/populair.json voor de homepage)"""
import json, sys, time, urllib.request, urllib.parse

BASE = "https://cloud.umami.is/analytics/eu/api"
SHARE = "sSKhb6j4KMk4E28R"

def get(path, token=None, **params):
    url = BASE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"User-Agent": "watkoopik-umami"})
    if token:
        req.add_header("x-umami-share-token", token)
        req.add_header("x-umami-share-context", "1")
    return json.load(urllib.request.urlopen(req, timeout=30))

def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
    share = get(f"/share/{SHARE}")
    tok, wid = share["token"], share["websiteId"]
    now = int(time.time() * 1000)
    rng = dict(startAt=now - days * 86400000, endAt=now)
    s = get(f"/websites/{wid}/stats", tok, **rng)
    bounce = round(100 * s["bounces"] / s["visits"]) if s.get("visits") else 0
    print(f"{days} dagen: {s['visitors']} bezoekers, {s['visits']} bezoeken, {s['pageviews']} weergaven, bounce {bounce}%")
    for t in ("path", "referrer", "event", "country"):
        try:
            rows = get(f"/websites/{wid}/metrics", tok, type=t, limit=15, **rng)
        except Exception as e:
            print(f"== {t}: fout {e}"); continue
        print(f"== {t}: " + ", ".join(f"{r.get('x') or '(direct)'} {r['y']}" for r in rows))
    for prop in ("plek", "positie", "product", "gids"):
        try:
            rows = get(f"/websites/{wid}/event-data/values", tok, event="bol-klik", propertyName=prop, **rng)
            print(f"== bol-klik {prop}: " + ", ".join(f"{r.get('value')} {r.get('total')}" for r in rows))
        except Exception as e:
            print(f"== bol-klik {prop}: fout {e}")

def save_popular(days=7, path=None):
    """Schrijft stats/populair.json: gidsslugs gesorteerd op weergaven + 3x bol-kliks."""
    import os
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stats", "populair.json")
    share = get(f"/share/{SHARE}")
    tok, wid = share["token"], share["websiteId"]
    now = int(time.time() * 1000)
    rng = dict(startAt=now - days * 86400000, endAt=now)
    score = {}
    for r in get(f"/websites/{wid}/metrics", tok, type="path", limit=200, **rng):
        x = r.get("x") or ""
        if x.startswith("/beste/") and x.endswith(".html"):
            slug = x[7:-5]; score[slug] = score.get(slug, 0) + r["y"]
    for r in get(f"/websites/{wid}/event-data/values", tok, event="bol-klik", propertyName="gids", **rng):
        slug = r.get("value"); score[slug] = score.get(slug, 0) + 3 * r.get("total", 0)
    ranked = sorted(score, key=lambda k: -score[k])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump({"dagen": days, "bijgewerkt": time.strftime("%Y-%m-%d"), "gidsen": ranked}, open(path, "w"), indent=1)
    print(f"populair.json: {len(ranked)} gidsen, top: {', '.join(ranked[:6])}")

if __name__ == "__main__":
    if "--save" in sys.argv:
        save_popular()
    else:
        main()
