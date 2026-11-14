#!/usr/bin/env python3
"""Snoeilijst (N32 stap 2, indexatie-onderzoek O1/O5): welke gidsen krijgen noindex,follow en gaan uit sitemap.xml?

Een gids komt alleen op de lijst als hij aan alles voldoet:
 (a) 0 bol-kliks en minder dan 5 bezoekers in 28 dagen (Umami share-API)
 (b) niet met naam in een lopend experiment (groeimotor/experimenten.json, veld paginas; sitebrede A/B's met 'beste/*' tellen niet),
     niet in de huidige seizoensfase (seizoen.py: cadeau/speelgoed, in de Black Friday-week dure gidsen),
     niet in de video-wachtrij van de komende 14 dagen, niet jonger dan 14 dagen (nog geen kans gehad),
     geen hoofdgids van een familie
 (d) minder dan 2 weergaven via ChatGPT in 28 dagen (adres met ?utm_source=chatgpt.com; sinds 14 nov 2026: ChatGPT brengt
     driekwart van het bezoek en een gids die het aanhaalt hoort vindbaar te blijven)
 (c) er blijft een zustergids in dezelfde familie (_src/clusters.json) of anders in dezelfde categorie

Gebruik:
  python3 tools/snoei.py            -> schrijft het voorstel naar _src/snoei.json (niets aan de site)
  python3 tools/snoei.py --toepassen -> zet "noindex": true in data/<slug>.json voor de lijst in _src/snoei.json
  python3 tools/snoei.py --terug     -> haalt "noindex" weer uit alle data/*.json
Niets wordt verwijderd of doorverwezen; build.py leest het veld (robots-meta, sitemap, llms.txt)."""
import datetime, glob, importlib.util, json, os, re, statistics, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import umami
GM = os.path.join(ROOT, "..", "groeimotor"); SOC = os.path.join(ROOT, "..", "watkoopik-social")
DOEL = 100      # ongeveer zoveel indexeerbare gidsen houden we over
DAGEN = 28
OUT = os.environ.get("SNOEI_OUT") or os.path.join(ROOT, "_src", "snoei.json")
CHATGPT_MIN = 2  # vanaf zoveel weergaven via ChatGPT in 28 dagen blijft een gids indexeerbaar

def load(p, d=None):
    try: return json.load(open(p, encoding="utf-8"))
    except Exception: return d

def guides():
    gs = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
        g = load(f); g["_f"] = f; gs.append(g)
    return gs

def cijfers():
    share = umami.get("/share/%s" % umami.SHARE); tok, wid = share["token"], share["websiteId"]
    now = int(time.time() * 1000); rng = dict(startAt=now - DAGEN * 86400000, endAt=now)
    bez, kl, ai = {}, {}, {}
    for r in umami.get("/websites/%s/metrics" % wid, tok, type="path", limit=1000, **rng):
        x = (r.get("x") or "").split("?")[0]
        if x.startswith("/beste/") and x.endswith(".html"): bez[x[7:-5]] = bez.get(x[7:-5], 0) + r["y"]
    for r in umami.get("/websites/%s/event-data/values" % wid, tok, event="bol-klik", propertyName="gids", **rng):
        kl[r.get("value")] = kl.get(r.get("value"), 0) + r.get("total", 0)
    try:
        for r in umami.get("/websites/%s/metrics" % wid, tok, type="path", limit=1000, query="utm_source=chatgpt.com", **rng):
            x = (r.get("x") or "").split("?")[0]
            if x.startswith("/beste/") and x.endswith(".html"): ai[x[7:-5]] = ai.get(x[7:-5], 0) + r["y"]
    except Exception as ex:
        print("LET OP: ChatGPT-bezoek niet gelezen (%s); regel (d) telt deze run niet mee" % ex)
    return bez, kl, ai

def in_experiment():
    e = load(os.path.join(GM, "experimenten.json"), [])
    e = e if isinstance(e, list) else e.get("experimenten", [])
    out = {}
    for x in e:
        if x.get("status") != "loopt": continue
        for p in x.get("paginas") or []:
            if "*" in p: continue
            m = re.search(r"(beste-[a-z0-9-]+)", p)
            if m and "watkoopik" in str(x.get("site", "")) + p or (m and p.startswith(("beste", "/beste"))):
                out.setdefault(m.group(1), []).append(x["id"])
    return out

def in_wachtrij():
    out = set()
    for plat, n in (("reel", 42), ("tt", 42), ("yt", 56), ("pin", 42)):
        q = load(os.path.join(SOC, "queue_%s.json" % plat)) or load(os.path.join(SOC, "queue_reel.json"), [])
        st = load(os.path.join(SOC, "state_%s.json" % plat), {})
        i = st.get("next", 0)
        out |= {x.get("slug") for x in q[i:i + n]}
    return out

def waarde(g):
    ps = [p["price"] for p in g["products"][:5] if p.get("price")]
    return statistics.mean(ps) if ps else 0

def voorstel():
    spec = importlib.util.spec_from_file_location("seizoen", os.path.join(GM, "seizoen.py")); sz = importlib.util.module_from_spec(spec); spec.loader.exec_module(sz)
    gs = guides(); by = {g["slug"]: g for g in gs}
    bez, kl, ai = cijfers(); exp = in_experiment(); wq = in_wachtrij()
    vandaag = datetime.date.today(); fase = sz.fase("nl")
    # families zoals build.py ze maakt
    fam, mains = {}, set()
    for c in load(os.path.join(ROOT, "_src", "clusters.json"), []):
        rx = re.compile(c["match"]); ms = [g["slug"] for g in gs if rx.match(g["slug"][6:])]
        if len(ms) < 2: continue
        if c.get("main") in ms: mains.add(c["main"])
        for s in ms: fam.setdefault(s, ms)   # eerste = hoofdfamilie
    rows = []
    for g in gs:
        s = g["slug"]; waarom = []
        b, k = bez.get(s, 0), kl.get(s, 0)
        if k > 0: waarom.append("%d bol-kliks" % k)
        if b >= 5: waarom.append("%d bezoekers" % b)
        if ai.get(s, 0) >= CHATGPT_MIN: waarom.append("%d weergaven via ChatGPT" % ai[s])
        if s in exp: waarom.append("experiment " + "/".join(exp[s]))
        if sz.is_cadeau(s, g.get("cat", "")) and not sz.voorbij(s) and fase in ("cadeau", "kerst"): waarom.append("seizoensfase " + fase)
        if fase == "blackfriday" and waarde(g) >= sz.DUUR: waarom.append("seizoensfase blackfriday")
        if s in wq: waarom.append("video-wachtrij 14 dagen")
        pub = g.get("published") or g.get("updated") or "2026-10-01"
        if (vandaag - datetime.date.fromisoformat(pub[:10])).days < 14: waarom.append("jonger dan 14 dagen")
        if s in mains: waarom.append("hoofdgids familie")
        rows.append({"slug": s, "cat": g["cat"], "bezoekers_28d": b, "kliks_28d": k, "chatgpt_28d": ai.get(s, 0), "waarde": round(waarde(g)), "blijft_omdat": waarom, "familie": fam.get(s)})
    kan = [r for r in rows if not r["blijft_omdat"]]
    # zwakste eerst: minste bezoek, dan laagste gemiddelde prijs top 5
    kan.sort(key=lambda r: (r["bezoekers_28d"], r["waarde"]))
    weg, ruimte = [], max(0, len(rows) - DOEL)
    wegset = set()
    for r in kan:
        if len(weg) >= ruimte: break
        zus_fam = [x for x in (r["familie"] or []) if x != r["slug"] and x not in wegset]
        zus_cat = [x["slug"] for x in rows if x["cat"] == r["cat"] and x["slug"] != r["slug"] and x["slug"] not in wegset]
        # (c) er moet een zuster blijven; kandidaten die nog niet beoordeeld zijn kunnen later ook wegvallen, daarom tellen alleen blijvers
        blijvers = {x["slug"] for x in rows if x["blijft_omdat"]}
        zus = [x for x in zus_fam if x in blijvers] or [x for x in zus_cat if x in blijvers]
        if not zus: continue
        r["zuster"] = zus[0]; weg.append(r); wegset.add(r["slug"])
    out = {"datum": str(vandaag), "dagen": DAGEN, "fase": fase, "gidsen_totaal": len(rows), "noindex": len(weg), "indexeerbaar": len(rows) - len(weg),
           "kandidaten_zonder_reden_om_te_blijven": len(kan),
           "lijst": [{k: r[k] for k in ("slug", "cat", "bezoekers_28d", "kliks_28d", "chatgpt_28d", "waarde", "zuster")} for r in weg],
           "blijft": {r["slug"]: r["blijft_omdat"] or ["doel %d bereikt of geen zuster" % DOEL] for r in rows if r["slug"] not in wegset}}
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("snoei.json: %d gidsen, %d kandidaten, %d noindex, %d indexeerbaar (fase %s)" % (len(rows), len(kan), len(weg), len(rows) - len(weg), fase))

def zet(aan):
    lijst = {x["slug"] for x in load(OUT, {}).get("lijst", [])} if aan else set()
    n = 0
    for g in guides():
        f = g.pop("_f"); had = g.get("noindex")
        if g["slug"] in lijst: g["noindex"] = True
        else: g.pop("noindex", None)
        if g.get("noindex") != had:
            json.dump(g, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2); n += 1
    print("%d databestanden gewijzigd, %d gidsen noindex" % (n, len(lijst)))

if __name__ == "__main__":
    if "--toepassen" in sys.argv: zet(True)
    elif "--terug" in sys.argv: zet(False)
    else: voorstel()
