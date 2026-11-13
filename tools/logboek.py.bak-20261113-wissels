#!/usr/bin/env python3
"""Logboek per gids (groeimotor N32 stap 3, 13 nov 2026): wat er sinds de start in de lijst veranderde.

Bron = de git-geschiedenis van data/<slug>.json. Per versie vergelijken we de 10 producten met de versie ervoor:
een product dat verdween en een dat erbij kwam = vervanging; een andere nummer 1 = wissel aan de top.
Een andere bol-aanbieding van hetzelfde model (zelfde naam, andere EAN, of bijna dezelfde naam) telt niet.
Een reden staat er alleen bij als de commit maar over één ding ging (leverbaarheid of prijsgrens); anders geen reden.
Niets wordt geschat of verzonnen.

Gebruik:
  python3 tools/logboek.py            -> werkt _src/logboek.json bij voor de gidsen in _src/logboek_gidsen.json
  python3 tools/logboek.py --kies 20  -> kiest eerst de 20 best verdienende indexeerbare gidsen
                                         (bol-kliks 28 dagen x mediaan prijs top 5) en schrijft _src/logboek_gidsen.json
  --stil                              -> geen uitvoer
build.py leest _src/logboek.json (logboek_html). Versies die al gelezen zijn staan in de cache (veld _tot)."""
import difflib, glob, json, os, re, statistics, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
LIJST = os.path.join(ROOT, "_src", "logboek_gidsen.json")
OUT = os.path.join(ROOT, "_src", "logboek.json")
STIL = "--stil" in sys.argv

def load(p, d=None):
    try: return json.load(open(p, encoding="utf-8"))
    except Exception: return d

def git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True, timeout=60).stdout

def norm(s): return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
def naam(p): return ("%s %s" % (p.get("brand", ""), p.get("name", ""))).strip()

def cijfers(n): return sorted(t for t in n.split() if re.search(r"\d", t))
def zelfde(a, b, ruim=False):
    """Zelfde model? Zelfde EAN of zelfde naam; ruim: ook zelfde merk met dezelfde typenummers en bijna dezelfde naam
    (andere kleur of uitvoering). Typenummers die verschillen = een ander model (TCL 55P79L en 55C69KS)."""
    if a.get("ean") and a.get("ean") == b.get("ean"): return True
    na, nb = norm(naam(a)), norm(naam(b))
    if na == nb: return True
    if ruim and norm(a.get("brand")) == norm(b.get("brand")) and cijfers(na) == cijfers(nb):
        return difflib.SequenceMatcher(None, na, nb).ratio() >= (0.6 if cijfers(na) else 0.75)
    return False

def koppel(prev, ps):
    """Een-op-een koppelen: eerst EAN of naam, daarna de ruime regel op wat overblijft. Geeft (weg, bij) met plek."""
    over_p = list(enumerate(prev)); over_q = list(enumerate(ps))
    for ruim in (False, True):
        for i, p in list(over_p):
            for j, q in over_q:
                if zelfde(p, q, ruim):
                    over_p.remove((i, p)); over_q.remove((j, q)); break
    return over_p, over_q

REDEN = [
    (re.compile(r"^Leverbaarheid:", re.I), "niet meer leverbaar of verkeerd geprijsd bij bol"),
    (re.compile(r"^\d+ niet-leverbare producten hersteld", re.I), "niet meer leverbaar bij bol"),
    (re.compile(r"^Prijsgrens:", re.I), "kwam boven de prijsgrens van deze gids"),
]
def reden(subject):
    for rx, t in REDEN:
        if rx.search(subject): return t
    return None

def versies(slug):
    out = []
    for line in git("log", "--reverse", "--format=%H|%ad|%s", "--date=short", "--", "data/%s.json" % slug).splitlines():
        h, d, s = line.split("|", 2)
        out.append((h, d, s))
    return out

def producten(h, slug):
    try: g = json.loads(git("show", "%s:data/%s.json" % (h, slug)))
    except Exception: return None
    return [{"brand": p.get("brand", ""), "name": p.get("name", ""), "ean": p.get("ean")} for p in g.get("products", [])]

def logboek(slug, oud=None):
    vs = versies(slug)
    if not vs: return None
    lb = oud if oud and oud.get("_tot") in [v[0] for v in vs] else {"start": vs[0][1], "n": 0, "events": [], "_tot": None, "_ps": None}
    begin = [v[0] for v in vs].index(lb["_tot"]) + 1 if lb["_tot"] else 0
    prev = lb["_ps"]
    for h, d, s in vs[begin:]:
        ps = producten(h, slug)
        if not ps: continue
        if prev is None:
            lb["start"] = d; lb["n"] = len(ps)
        else:
            weg, bij = koppel(prev, ps)
            r = reden(s)
            for (i, p), (j, q) in zip(weg, bij):
                ev = {"d": d, "t": "vervangen", "uit": naam(p), "in": naam(q), "plek": j + 1, "paar": len(weg) == 1 or i == j}
                if r: ev["waarom"] = r
                lb["events"].append(ev)
            for i, p in weg[len(bij):]: lb["events"].append({"d": d, "t": "weg", "uit": naam(p)})
            for j, q in bij[len(weg):]: lb["events"].append({"d": d, "t": "bij", "in": naam(q), "plek": j + 1})
            if not zelfde(prev[0], ps[0], True) and any(zelfde(prev[0], q, True) for q in ps) and any(zelfde(p, ps[0], True) for p in prev):
                lb["events"].append({"d": d, "t": "nr1", "van": naam(prev[0]), "naar": naam(ps[0])})
            lb["n"] = len(ps)
        prev = ps; lb["_tot"] = h
    lb["_ps"] = prev
    return lb

def kies(n):
    sys.path.insert(0, HERE)
    import snoei
    bez, kl = snoei.cijfers()
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
        g = load(f)
        if g.get("noindex"): continue
        pr = [p["price"] for p in g["products"][:5] if p.get("price")]
        if not pr: continue
        k = kl.get(g["slug"], 0)
        rows.append({"slug": g["slug"], "kliks_28d": k, "bezoekers_28d": bez.get(g["slug"], 0), "mediaan_prijs_top5": round(statistics.median(pr), 2),
                     "score": round(k * statistics.median(pr))})
    rows.sort(key=lambda r: (-r["score"], -r["bezoekers_28d"]))
    import datetime
    json.dump({"datum": datetime.date.today().isoformat(), "maat": "bol-kliks 28 dagen x mediaan prijs top 5 (alleen indexeerbare gidsen)", "gidsen": rows[:n]},
              open(LIJST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if not STIL:
        for r in rows[:n]: print("%-48s kliks %3d  mediaan %7.2f  score %6d" % (r["slug"], r["kliks_28d"], r["mediaan_prijs_top5"], r["score"]))

def main():
    if "--kies" in sys.argv: kies(int(sys.argv[sys.argv.index("--kies") + 1]))
    lijst = load(LIJST, {}).get("gidsen", [])
    cache = load(OUT, {})
    out = {}
    for r in lijst:
        lb = logboek(r["slug"], cache.get(r["slug"]))
        if lb: out[r["slug"]] = lb
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if not STIL:
        print("Logboek: %d gidsen, %d wijzigingen in de lijsten" % (len(out), sum(len(v["events"]) for v in out.values())))

if __name__ == "__main__":
    main()
