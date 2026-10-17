# -*- coding: utf-8 -*-
"""watkoopik.nl: top 10-koopgidsen met bewegende vormgeving (GSAP + Lenis + WebGL-achtergrond).
Inhoud komt uit data/*.json. Gebruik: python3 build.py (of ./deploy.sh "bericht").
Vorige versie van de bouwmotor: build_v1.py (niet meer gebruikt).
Copyregel: geen em/en-dashes, geen ", en"."""
import os, re, json, glob, html, datetime, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
# Varianten: WK_THEME=light|dark (standaard dark), WK_OUT=<map> voor een preview elders (dan noindex + canonical naar .nl)
THEME = os.environ.get("WK_THEME", "green")  # standaard sinds 15 okt 2026: licht met groen en goud
OUT = os.environ.get("WK_OUT", ROOT)
PREVIEW = os.path.abspath(OUT) != ROOT
THEME_CSS = {"dark": [], "light": ["light"], "green": ["light", "green"]}.get(THEME, [])
BODY_CLASS = {"dark": "theme-dark", "light": "theme-light", "green": "theme-light theme-green"}.get(THEME, "theme-dark")
DATA = os.path.join(ROOT, "data")
SITE = "https://watkoopik.nl"
CANON = "https://watkoopik.nl"
BOL_SITE_ID = "1549706"
TODAY = datetime.date.today()
YEAR = TODAY.year
BUILD = datetime.datetime.now().strftime("%Y%m%d%H%M")
MONTHS = ["", "januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"]
e = html.escape
rd = lambda n: open(os.path.join(ROOT, "_src", n), encoding="utf-8").read()
def wr(path, s):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

def check(s, where):
    if "—" in s or "–" in s: raise SystemExit("streepje in " + where)
    if re.search(r", en\b", re.sub(r"<script.*?</script>", "", s, flags=re.S)): raise SystemExit("', en' in " + where)

def eur(v):
    s = ("%.2f" % v).replace(".", ","); return "€ " + (s[:-3] if s.endswith(",00") else s)
def eur_n(v):
    s = ("%.2f" % v).replace(".", ","); return s[:-3] if s.endswith(",00") else s
def nldate(iso):
    try:
        y, m, d = [int(x) for x in str(iso)[:10].split("-")]; return "%d %s %d" % (d, MONTHS[m], y)
    except Exception: return str(iso)

def shop_link(p):
    q = p.get("search") or "%s %s" % (p["brand"], p["name"])
    target = p.get("url") or "https://www.bol.com/nl/nl/s/?searchtext=" + urllib.parse.quote_plus(q)
    name = re.sub(r"[^A-Za-z0-9 ]", "", "%s %s" % (p["brand"], p["name"]))[:60]
    return "https://partner.bol.com/click/click?p=2&t=url&s=%s&f=TXL&url=%s&name=%s" % (BOL_SITE_ID, urllib.parse.quote(target, safe=""), urllib.parse.quote_plus(name))
def shop_a(p, g, cls="btn btn-buy magnet", plek="kaart"):
    return '<a class="%s" href="%s" rel="sponsored nofollow noopener" target="_blank" data-umami-event="bol-klik" data-umami-event-gids="%s" data-umami-event-product="%s" data-umami-event-positie="%s" data-umami-event-plek="%s">Bekijk bij bol <span class="arr">→</span></a>' % (
        cls, shop_link(p), g["slug"], e("%s %s" % (p["brand"], p["name"])), p.get("rank", ""), plek)

STAR = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.7.8-4.9 4.6 1.3 6.6L12 17.3l-6 3.3 1.3-6.6L2.4 9.4l6.7-.8z" fill="%s"/></svg>'
def stars(score):
    full = int(round(score / 2)); return '<span class="stars" aria-label="%s van 10">%s</span>' % (score, "".join(STAR % ("#f5b324" if i < full else "#e3dff0") for i in range(5)))

LOGO = ('<svg width="34" height="34" viewBox="0 0 100 100" aria-hidden="true"><path d="M14 10h40l32 32-40 40L14 50z" fill="#5b3fd6"/>'
        '<circle cx="30" cy="26" r="6" fill="#fff"/><path d="M34 56l10 10 20-22" fill="none" stroke="#ff7a3d" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#5b3fd6"/>'
           '<path d="M22 20h34l26 26-34 34L22 54z" fill="#fff"/><circle cx="35" cy="33" r="5" fill="#5b3fd6"/>'
           '<path d="M38 58l9 9 17-19" fill="none" stroke="#ff7a3d" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>')

CATS = {
    "huishouden": ("Huishouden", "Stofzuigers, wasmachines, drogers en strijkijzers"),
    "keuken": ("Keuken", "Airfryers, koffiemachines, blenders en keukenhulpen"),
    "verzorging": ("Verzorging", "Föhns, tandenborstels, scheerapparaten en trimmers"),
    "slapen": ("Slapen", "Matrassen, kussens en dekbedden"),
    "elektronica": ("Elektronica", "Oordopjes, koptelefoons, speakers, smartwatches en tv's"),
    "wonen": ("Wonen", "Luchtreinigers, ventilatoren en comfort in huis"),
    "sport": ("Sport en buiten", "Fitness, fietsen en buitenleven"),
    "kind": ("Baby en kind", "Kinderwagens, babyfoons en speelgoed"),
    "klussen": ("Klussen en tuin", "Gereedschap en tuinmachines"),
    "computer": ("Computer", "Laptops, monitoren, printers en randapparatuur"),
    "telefoon": ("Telefoon en tablet", "Smartphones, tablets en opladers"),
    "audio": ("Audio", "Speakers, koptelefoons en hifi"),
    "gaming": ("Gaming", "Consoles, controllers en gaming-accessoires"),
    "foto": ("Foto en video", "Camera's, drones en actioncams"),
    "gezondheid": ("Gezondheid", "Bloeddrukmeters, massage en welzijn"),
    "huisdieren": ("Huisdieren", "Alles voor hond en kat"),
    "speelgoed": ("Speelgoed", "Speelgoed en spellen voor elke leeftijd"),
    "kantoor": ("Kantoor", "Thuiswerken en kantoorspullen"),
    "outdoor": ("Kamperen en outdoor", "Tenten, slaapzakken en buitengear"),
    "auto": ("Auto en fiets", "Accessoires voor onderweg"),
    "reizen": ("Reizen en mode", "Koffers, tassen en horloges"),
    "hobby": ("Hobby en muziek", "Creatief, muziekinstrumenten en vrije tijd"),
}
ICONS = {
    "huishouden": '<path d="M9 3h6l1 9H8z"/><path d="M8 12h8v3a4 4 0 0 1-8 0z"/>',
    "keuken": '<path d="M4 12h16"/><path d="M6 12v6a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-6"/><path d="M8 12V8a4 4 0 0 1 8 0v4"/>',
    "verzorging": '<path d="M6 4h8a5 5 0 0 1 0 10H9"/><path d="M9 14v6"/><path d="M14 9h4"/>',
    "slapen": '<path d="M3 18V9a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v9"/><path d="M3 14h18"/><path d="M7 7V5h4v2"/>',
    "elektronica": '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/>',
    "wonen": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "sport": '<circle cx="12" cy="12" r="9"/><path d="M12 3v18"/><path d="M3 12h18"/>',
    "kind": '<circle cx="12" cy="8" r="4"/><path d="M5 21a7 7 0 0 1 14 0"/>',
    "klussen": '<path d="M14 4l6 6-9 9H5v-6z"/><path d="M12 6l6 6"/>',
    "computer": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "telefoon": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    "audio": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1"/><rect x="17" y="14" width="4" height="6" rx="1"/>',
    "gaming": '<rect x="2" y="7" width="20" height="11" rx="5"/><path d="M7 11v3M5.5 12.5h3"/><circle cx="16" cy="11.5" r="1"/><circle cx="18" cy="13.5" r="1"/>',
    "foto": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "gezondheid": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "huisdieren": '<circle cx="7" cy="9" r="2"/><circle cx="17" cy="9" r="2"/><circle cx="10" cy="5" r="2"/><circle cx="14" cy="5" r="2"/><path d="M8 17a4 4 0 0 1 8 0c0 2-8 2-8 0z"/>',
    "speelgoed": '<circle cx="12" cy="12" r="9"/><path d="M12 3l3 6-3 3-3-3z"/>',
    "kantoor": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    "outdoor": '<path d="M3 20l9-15 9 15z"/><path d="M12 5v15"/>',
    "auto": '<path d="M5 16l1.5-5h11L19 16"/><rect x="3" y="16" width="18" height="3" rx="1"/><circle cx="7" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>',
    "reizen": '<rect x="5" y="7" width="14" height="13" rx="2"/><path d="M9 7V4h6v3"/>',
    "hobby": '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
}
def icon(cat, size=24):
    return '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, ICONS.get(cat, ICONS["huishouden"]))

# ---------- data ----------
guides = []
for f in sorted(glob.glob(os.path.join(DATA, "*.json"))):
    g = json.load(open(f, encoding="utf-8"))
    g["url"] = "beste/%s.html" % g["slug"]
    for i, p in enumerate(g["products"]):
        p["rank"] = i + 1
        if i == 0 and not p.get("label"): p["label"] = "Beste keuze"
    guides.append(g)
guides.sort(key=lambda g: (g.get("prio", 50), g["slug"]))
by_cat = {}
for g in guides: by_cat.setdefault(g["cat"], []).append(g)
N_PROD = sum(len(g["products"]) for g in guides)
N_REV = sum(int(re.sub(r"\D", "", str(g.get("reviews_total", "0"))) or 0) for g in guides)
def win(g): return g["products"][0]
def img_of(p, cls=""):
    return ('<img src="%s" alt="%s %s" loading="lazy"%s>' % (e(p["image"]), e(p["brand"]), e(p["name"]), (' class="%s"' % cls) if cls else "")) if p.get("image") else '<span class="ph" aria-hidden="true">%s</span>' % e(p.get("_ico", "🛒"))
for g in guides:
    for p in g["products"]: p["_ico"] = g["ico"]

# ---------- chrome ----------
NAV = [("gidsen.html", "Alle gidsen"), ("keuzehulp.html", "Keuzehulp"), ("slimste-koop.html", "Slimste koop"), ("zo-kiezen-wij.html", "Zo kiezen wij")]

def head(title, desc, path, root, extra="", img=""):
    canon = CANON + "/" + path
    return '''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="%s">
<link rel="canonical" href="%s">
<link rel="alternate" hreflang="nl-NL" href="%s">
<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:type" content="website"><meta property="og:locale" content="nl_NL"><meta property="og:site_name" content="watkoopik"><meta property="og:url" content="%s">%s
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#07060f">
<link rel="icon" href="%sfavicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%sstyle.css?v=%s">%s
<script>window.ROOT=%s</script>
<script defer src="https://cloud.umami.is/script.js" data-website-id="47030ca7-838e-4840-9d90-0c8b315ba5e8"></script>
%s
</head>
<body class="%s">
<div class="fx-fallback" aria-hidden="true"></div><canvas id="fx" aria-hidden="true"></canvas><div class="fx-veil" aria-hidden="true"></div><div class="fx-grain" aria-hidden="true"></div><div class="cursor-glow" aria-hidden="true"></div>
<div class="progress" aria-hidden="true"></div>''' % (e(title), e(desc), "noindex,follow" if PREVIEW else "index,follow,max-image-preview:large", canon, canon, e(title), e(desc), canon, ('<meta property="og:image" content="%s">' % e(img)) if img else '', root, root, BUILD, "".join('<link rel="stylesheet" href="%s%s.css?v=%s">' % (root, n, BUILD) for n in THEME_CSS), json.dumps(root), extra, BODY_CLASS)

def searchbox(cls="", ph="Zoek een product of merk", btn=True):
    return '''<div class="search-wrap"><form class="search %s" data-search role="search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><input type="search" placeholder="%s" aria-label="Zoek een gids" autocomplete="off">%s</form><div class="results"></div></div>''' % (cls, ph, '<button class="sbtn" type="submit">Zoek</button>' if btn else "")

def chrome(active, root):
    links = "".join('<li><a href="%s%s"%s>%s</a></li>' % (root, h, ' class="active"' if h == active else "", t) for h, t in NAV)
    drawer = "".join('<a class="dl" href="%s%s">%s</a>' % (root or ("./" if h == "" else ""), h, t) for h, t in [("", "Home")] + NAV + [("categorie/%s.html" % k, v[0]) for k, v in CATS.items() if by_cat.get(k)] + [("over-ons.html", "Over ons"), ("contact.html", "Contact")])
    return '''<header class="nav"><div class="nav-in">
<a class="logo" href="%s" aria-label="watkoopik, naar home">%s<span class="logo-word">wat<b>koop</b>ik</span></a>
<ul class="nav-links">%s</ul>
%s
<a class="btn btn-purple btn-sm nav-cta magnet" href="%skeuzehulp.html">Help mij kiezen</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<nav class="drawer" aria-label="Menu">%s%s</nav>
''' % (root or "./", LOGO, links, searchbox("search-nav", "Zoek…", False), root, searchbox(), drawer)

PREF_BTN = '<a class="pref-src" href="https://google.com/preferences/source?q=watkoopik.nl" target="_blank" rel="noopener" data-umami-event="preferred-source"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="#4285F4" d="M22.5 12.3c0-.8-.1-1.5-.2-2.3H12v4.3h5.9a5 5 0 0 1-2.2 3.3v2.7h3.6c2.1-1.9 3.2-4.8 3.2-8z"/><path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.6-2.7c-1 .7-2.2 1-3.7 1-2.9 0-5.3-1.9-6.2-4.5H2.1v2.8A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.8 14.1a6.6 6.6 0 0 1 0-4.2V7.1H2.1a11 11 0 0 0 0 9.8z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3 .6 4.2 1.6l3.1-3.1A11 11 0 0 0 2.1 7.1l3.7 2.8C6.7 7.3 9.1 5.4 12 5.4z"/></svg>Voeg watkoopik toe als voorkeursbron in Google</a>'

def footer(root):
    pop = "".join('<li><a href="%s%s">%s</a></li>' % (root, g["url"], e(g["short"])) for g in guides[:7])
    cats = "".join('<li><a href="%scategorie/%s.html">%s</a></li>' % (root, k, v[0]) for k, v in CATS.items() if by_cat.get(k))
    return '''<footer><div class="wrap"><div class="cols">
<div><a class="logo" href="%s">%s<span class="logo-word">wat<b>koop</b>ik</span></a><p style="margin-top:12px;font-size:.92rem">Onafhankelijke top 10-gidsen. Wij vergelijken prijs, specificaties en reviews zodat jij in vijf minuten de juiste keuze maakt.</p></div>
<div><h4>Populair</h4><ul>%s</ul></div>
<div><h4>Categorieën</h4><ul>%s</ul></div>
<div><h4>watkoopik</h4><ul><li><a href="%skeuzehulp.html">Keuzehulp</a></li><li><a href="%sslimste-koop.html">Slimste koop</a></li><li><a href="%szo-kiezen-wij.html">Zo kiezen wij</a></li><li><a href="%sover-ons.html">Over ons</a></li><li><a href="%scontact.html">Contact</a></li><li><a href="%sprivacy.html">Privacy</a></li><li><a href="%sdisclaimer.html">Affiliate-disclaimer</a></li></ul></div>
</div><div class="pref-wrap"><a class="pref-src" href="https://google.com/preferences/source?q=watkoopik.nl" target="_blank" rel="noopener" data-umami-event="preferred-source"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="#4285F4" d="M22.5 12.3c0-.8-.1-1.5-.2-2.3H12v4.3h5.9a5 5 0 0 1-2.2 3.3v2.7h3.6c2.1-1.9 3.2-4.8 3.2-8z"/><path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.6-2.7c-1 .7-2.2 1-3.7 1-2.9 0-5.3-1.9-6.2-4.5H2.1v2.8A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.8 14.1a6.6 6.6 0 0 1 0-4.2V7.1H2.1a11 11 0 0 0 0 9.8z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3 .6 4.2 1.6l3.1-3.1A11 11 0 0 0 2.1 7.1l3.7 2.8C6.7 7.3 9.1 5.4 12 5.4z"/></svg>Voeg watkoopik toe als voorkeursbron in Google</a></div><div class="fine">© %d watkoopik · Wij ontvangen mogelijk een vergoeding als je via onze links iets koopt. Dit kost jou niets extra en beïnvloedt de rangschikking niet. Prijzen zijn indicatief.</div></div></footer>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="%sapp.js?v=%s" defer></script>
</body></html>''' % (root or "./", LOGO, pop, cats, root, root, root, root, root, root, root, YEAR, root, BUILD)

def page(path, title, desc, body, active=None, extra="", root=None, img=""):
    if root is None: root = "../" * path.count("/")
    out = head(title, desc, path if path != "index.html" else "", root, extra, img) + chrome(active, root) + "<main>" + body + "</main>" + footer(root)
    check(out, path); wr(path, out)

# ---------- bouwstenen ----------
def gcard(g, root=""):
    p = win(g)
    return '''<a class="gc ring tilt rv" href="%s%s" data-cat-item="%s"><div class="gc-img"><span class="tag">Top 10</span>%s</div><div class="gc-body"><h3>%s</h3><p>%s</p><div class="gc-win"><span>Winnaar: <b>%s %s</b></span><span class="pr">%s</span></div></div></a>''' % (
        root, g["url"], g["cat"], img_of(p), e(g["title"]), e(g["intro"][:130].rsplit(" ", 1)[0] + "…"), e(p["brand"]), e(p["name"]), eur(p["price"]))

def mq_items(root=""):
    items = []
    for g in guides:
        p = next((x for x in g["products"][:3] if x.get("image")), None)
        if p: items.append('<a class="mq-item" href="%s%s"><img src="%s" alt="" loading="lazy">%s</a>' % (root, g["url"], e(p["image"]), e(g["short"])))
    return items

def marquee(items, rev=False, light=False):
    return '<div class="mq%s%s" aria-hidden="true"><div class="mq-track">%s</div></div>' % (" rev" if rev else "", " mq-light" if light else "", "".join(items) * 2)

# ---------- home ----------
items = mq_items()
half = len(items) // 2
chips = "".join('<a href="%s">%s</a>' % (g["url"], e(g["short"])) for g in guides[:9])
PALET = {"huishouden": ("#7c5cff", "#38e1ff"), "keuken": ("#ff7a3d", "#ff4fd8"), "verzorging": ("#ff4fd8", "#7c5cff"), "slapen": ("#3b5bff", "#38e1ff"),
         "elektronica": ("#00c2ff", "#7c5cff"), "wonen": ("#3ee08f", "#38e1ff"), "sport": ("#ffc65c", "#ff7a3d"), "kind": ("#ff8fb1", "#ffc65c"), "klussen": ("#ffc65c", "#3ee08f"),
         "computer": ("#38e1ff", "#3b5bff"), "telefoon": ("#7c5cff", "#ff4fd8")}
for _k in CATS: PALET.setdefault(_k, ("#7c5cff", "#38e1ff"))
cat_keys = [k for k in CATS if by_cat.get(k)]
sizes = ["big", "", "", "wide", "", ""]
cat_cards = "".join('''<a class="cat ring tilt rv %s" href="categorie/%s.html" style="--c1:%s;--c2:%s"><span class="ic">%s</span><span class="thumbs">%s</span><b>%s</b><small>%d gidsen · %s</small></a>''' % (
    sizes[i] if i < len(sizes) else "", k, PALET[k][0], PALET[k][1], icon(k), "".join('<img src="%s" alt="" loading="lazy">' % e(win(x)["image"]) for x in by_cat[k][:4] if win(x).get("image")),
    CATS[k][0], len(by_cat[k]), CATS[k][1].split(",")[0]) for i, k in enumerate(cat_keys))
winners = [g for g in guides if win(g).get("image")]
def wincard(g):
    p = win(g)
    return '''<a class="wincard" href="%s"><div class="im"><span class="crown">Nr. 1 %s</span><img src="%s" alt="%s %s" loading="lazy"></div><div class="bd"><small>%s · winnaar</small><h3>%s %s</h3><div class="pr">%s</div></div></a>''' % (
        g["url"], e(g["short"].lower()), e(p["image"]), e(p["brand"]), e(p["name"]), e(g["short"]), e(p["brand"]), e(p["name"]), eur(p["price"]))
wh = len(winners) // 2
winband = '<div class="mq winband">%s</div><div class="mq winband rev" style="margin-top:14px">%s</div>' % (
    '<div class="mq-track">%s</div>' % ("".join(wincard(g) for g in winners[:wh]) * 2),
    '<div class="mq-track">%s</div>' % ("".join(wincard(g) for g in winners[wh:]) * 2))
fl_imgs = [win(g)["image"] for g in winners[:6]]
floaters = '<div class="floaters" aria-hidden="true">%s</div>' % "".join('<div class="fl f%d" data-depth="%s"><div class="in"><img src="%s" alt=""></div></div>' % (i + 1, [.6, 1, .4, .8, .3, .5][i], e(im)) for i, im in enumerate(fl_imgs))

home = '''
<section class="hero" data-hue="0">%s
<div class="hero-in">
<span class="badge"><i></i> Elke dag nieuwe top 10's · prijzen dagelijks gecheckt</span>
<h1 class="split">Wat koop ik? <span class="grad">Wij zochten het uit.</span></h1>
<p class="lead">Onafhankelijke top 10-lijsten van de beste producten van %d. Vergeleken op prijs, specificaties en duizenden reviews, zodat jij in vijf minuten de juiste keuze maakt.</p>
%s
<div class="hero-chips">%s</div>
<div class="hero-stats"><div><b class="grad" data-count="%d">%d</b><span>top 10-gidsen</span></div><div><b class="grad" data-count="%d">%d</b><span>producten vergeleken</span></div><div><b class="grad" data-count="%d">%s</b><span>reviews meegewogen</span></div></div>
</div>
<div class="hero-band">%s%s</div>
</section>

<section data-hue="1"><div class="wrap">
<div class="sec-head rv"><div><span class="kick">Categorieën</span><h2>Waar ben je naar <span class="grad">op zoek?</span></h2></div><p>Kies een categorie en zie meteen de winnaars per productsoort.</p></div>
<div class="bento">%s</div>
</div></section>

<section data-hue="2" style="padding-left:0;padding-right:0"><div class="wrap"><div class="sec-head rv"><div><span class="kick">De winnaars</span><h2>Nummer 1 in <span class="grad">elke top 10</span></h2></div><a class="more" href="gidsen.html">Alle gidsen →</a></div></div>
%s
</section>

<section data-hue="3"><div class="wrap">
<div class="sec-head rv"><div><span class="kick">Nieuw</span><h2>De nieuwste <span class="grad">gidsen</span></h2></div><a class="more" href="gidsen.html">Alle %d gidsen →</a></div>
<div class="gl">%s</div>
</div></section>

<section data-hue="4"><div class="wrap">
<div class="sec-head rv"><div><span class="kick">Zo werkt het</span><h2>In drie stappen <span class="grad">de juiste keuze</span></h2></div></div>
<div class="steps">
<div class="step ring tilt rv"><div class="n">1</div><h3>Zoek of kies</h3><p>Typ een product in de zoekbalk of kies een categorie. Weet je het nog niet? Gebruik de <a href="keuzehulp.html">keuzehulp</a>.</p></div>
<div class="step ring tilt rv"><div class="n">2</div><h3>Vergelijk de top 10</h3><p>Bovenaan staan de beste keuze, de slimste koop en de beste premium optie. Daaronder alle tien modellen naast elkaar.</p></div>
<div class="step ring tilt rv"><div class="n">3</div><h3>Koop met een gerust hart</h3><p>Klik door naar bol. Prijzen controleren we dagelijks, plus- en minpunten staan er eerlijk bij.</p></div>
</div>
<div class="numbers" style="margin-top:18px">
<div class="rv"><b class="grad" data-count="%d">%d</b><span>gidsen</span></div><div class="rv"><b class="grad" data-count="%d">%d</b><span>producten</span></div><div class="rv"><b class="grad">4</b><span>criteria per product</span></div><div class="rv"><b class="grad">0</b><span>betaalde plekken</span></div>
</div>
</div></section>

<section data-hue="5"><div class="wrap">
<div class="cta-band rv"><div><h2>Twijfel je nog?</h2><p>Beantwoord drie vragen en wij kiezen het product dat het beste bij jou past.</p></div><div><a class="btn btn-dark magnet" href="keuzehulp.html" style="width:100%%">Start de keuzehulp <span class="arr">→</span></a></div></div>
</div></section>

<section data-hue="6" style="padding-top:20px"><div class="wrap narrow rv">
<h2 style="font-size:1.7rem">Onafhankelijk koopadvies voor %d</h2>
<p class="muted">watkoopik vergelijkt per productsoort de tien beste modellen die je nu in Nederland kunt kopen. Of je nu de <a href="beste/beste-airfryer.html">beste airfryer</a>, een <a href="beste/beste-stofzuiger.html">stille stofzuiger</a> of <a href="beste/beste-draadloze-oordopjes.html">draadloze oordopjes met noise cancelling</a> zoekt: elke gids begint met drie duidelijke winnaars, gevolgd door een vergelijkingstabel, uitleg per product met plus- en minpunten, een koopgids en antwoorden op veelgestelde vragen. Merken kunnen geen plek kopen. <a href="zo-kiezen-wij.html">Lees hoe wij kiezen</a>.</p>
</div></section>
''' % (floaters, YEAR, searchbox(), chips, len(guides), len(guides), N_PROD, N_PROD, N_REV, format(N_REV, ",").replace(",", "."),
       marquee(items[:half]), marquee(items[half:], rev=True), cat_cards, winband, len(guides), "".join(gcard(g) for g in guides[:9]),
       len(guides), len(guides), N_PROD, N_PROD, YEAR)
home_ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": "watkoopik", "url": SITE + "/", "inLanguage": "nl-NL",
            "potentialAction": {"@type": "SearchAction", "target": SITE + "/gidsen.html?q={search_term_string}", "query-input": "required name=search_term_string"}},
           {"@context": "https://schema.org", "@type": "Organization", "name": "watkoopik", "url": SITE + "/", "logo": SITE + "/favicon.svg",
            "sameAs": ["https://www.instagram.com/watkoopik/", "https://www.tiktok.com/@watkoopik", "https://www.pinterest.com/watkoopik/"]}]
page("index.html", "watkoopik · De beste producten van %d vergeleken" % YEAR, "Onafhankelijke top 10-gidsen: de beste stofzuigers, airfryers, föhns en meer van %d. Vergeleken op prijs, specificaties en reviews." % YEAR, home,
     extra="".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in home_ld), img=(win(guides[0]).get("image") or ""))

# ---------- alle gidsen met filter ----------
filt = '<div class="filters"><button class="on" data-cat="alle">Alle</button>%s</div>' % "".join('<button data-cat="%s">%s</button>' % (k, v[0]) for k, v in CATS.items() if by_cat.get(k))
page("gidsen.html", "Alle top 10-gidsen | watkoopik", "Overzicht van alle top 10-gidsen van watkoopik, te filteren per categorie.",
     '<section data-hue="1" style="padding-top:34px"><div class="wrap"><span class="kick">Overzicht</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">Alle %d top 10-gidsen</h1><p class="muted" style="max-width:620px">Filter op categorie of zoek direct op product of merk.</p><div style="max-width:560px;margin:14px 0 18px">%s</div>%s<div class="gl">%s</div></div></section>' % (
         len(guides), searchbox(), filt, "".join(gcard(g) for g in guides)), "gidsen.html")

# ---------- categorieën ----------
for k, v in CATS.items():
    gs = by_cat.get(k, [])
    if not gs: continue
    body = '''<section style="padding-top:20px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a> › %s</nav>
<span class="kick" style="margin-top:14px">Categorie</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">De beste %s van %d</h1>
<p class="muted" style="max-width:700px">%s. In deze %d gidsen vergelijken we per productsoort de tien beste modellen op prijs, specificaties en gebruikersreviews, met een duidelijke winnaar, de slimste koop en de beste premium keuze.</p>
<div class="gl" style="margin-top:22px">%s</div></div></section>''' % (v[0], v[0].lower(), YEAR, v[1], len(gs), "".join(gcard(g, "../") for g in gs))
    cld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": v[0], "item": SITE + "/categorie/%s.html" % k}]},
           {"@context": "https://schema.org", "@type": "ItemList", "name": "Beste %s van %d" % (v[0].lower(), YEAR), "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/" + x["url"], "name": x["title"]} for i, x in enumerate(gs)]}]
    page("categorie/%s.html" % k, "Beste %s %d: alle top 10's | watkoopik" % (v[0].lower(), YEAR), "%s. Vergelijk per productsoort de tien beste modellen van %d op prijs, specificaties en reviews." % (v[1], YEAR), body,
         extra="".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in cld))

# ---------- gidspagina's ----------
def bars(p, g):
    """Deelscores afgeleid van totaalscore en prijspositie binnen de gids (voor visuele vergelijking)."""
    prices = sorted(x["price"] for x in g["products"]); pos = prices.index(p["price"]) / max(1, len(prices) - 1)
    perf = min(10, round(p["score"] + (0.3 if p["rank"] <= 3 else 0), 1))
    val = round(max(5, min(10, p["score"] - 1.2 * pos + 0.8)), 1)
    rel = round(max(5, min(10, p["score"] - 0.2)), 1)
    rows = [("Prestaties", perf), ("Prijs-kwaliteit", val), ("Betrouwbaarheid", rel)]
    return '<div class="bars">%s</div>' % "".join('<div class="bar"><span>%s</span><i><em style="--w:%d%%"></em></i><b>%s</b></div>' % (n, int(s * 10), ("%.1f" % s).replace(".", ",")) for n, s in rows)

for g in guides:
    root = "../"; ps = g["products"]; top = ps[0]
    labs = [p for p in ps if p.get("label")][:3]
    podium = "".join('''<div class="pd%s"><span class="lbl">%s</span><div class="im">%s</div><h3>%s %s</h3><div class="pr">%s</div><p>%s</p>%s</div>''' % (
        " first" if i == 0 else "", e(p["label"]), img_of(p), e(p["brand"]), e(p["name"]), eur(p["price"]), e(p["oneliner"]), shop_a(p, g, "btn btn-buy btn-sm magnet", "podium")) for i, p in enumerate(labs))
    keys = list(ps[0]["specs"].keys())[:3]
    rows = "".join('<tr><td><span class="rk%s">%d</span></td><td class="nm"><span class="ti">%s<span>%s<small>%s</small></span></span></td>%s<td><b>%s</b></td><td><span class="sc%s">%s</span></td><td>%s</td></tr>' % (
        " r1" if p["rank"] == 1 else "", p["rank"], ('<img src="%s" alt="" loading="lazy">' % e(p["image"])) if p.get("image") else "", e(p["brand"]), e(p["name"]),
        "".join("<td>%s</td>" % e(str(p["specs"].get(k, "-"))) for k in keys), eur(p["price"]), " hi" if p["score"] >= 9 else "", p["score"], shop_a(p, g, "btn btn-buy btn-sm", "tabel")) for p in ps)
    table = '<div class="tbl rv"><table><thead><tr><th>#</th><th>Model</th>%s<th>Prijs</th><th>Score</th><th></th></tr></thead><tbody>%s</tbody></table></div>' % ("".join("<th>%s</th>" % e(k) for k in keys), rows)
    cards = "".join('''<article class="pr-card%s rv" id="p%d"><div class="pr-head"><div class="pr-img"><span class="n">%d</span>%s</div><div>%s<h2>%s %s</h2>
<div class="pr-meta"><span class="price">%s</span><span>%s <b>%s</b>/10</span><span>%s</span></div>%s<div class="specs">%s</div></div></div>
<div class="pr-txt">%s</div><div class="pc"><div class="pros"><h4>Pluspunten</h4><ul>%s</ul></div><div class="cons"><h4>Minpunten</h4><ul>%s</ul></div></div>
<div class="ideal"><b>Ideaal voor:</b> %s</div><div class="buy">%s<small>Prijs gecheckt op %s</small></div></article>''' % (
        " top" if p["rank"] == 1 else "", p["rank"], p["rank"], img_of(p), ('<span class="pr-lbl">%s</span>' % e(p["label"])) if p.get("label") else "", e(p["brand"]), e(p["name"]),
        eur(p["price"]), stars(p["score"]), p["score"], e(p.get("reviews", "")), bars(p, g), "".join("<span><b>%s:</b> %s</span>" % (e(k), e(str(v))) for k, v in p["specs"].items()),
        "".join("<p>%s</p>" % e(t) for t in p["text"].split("\n\n")), "".join("<li>%s</li>" % e(x) for x in p["pros"]), "".join("<li>%s</li>" % e(x) for x in p["cons"]),
        e(p["ideal"]), shop_a(p, g), e(nldate(g.get("updated", TODAY.isoformat())))) for p in ps)
    guide_html = "".join("<h3>%s</h3>%s" % (e(s["h"]), "".join("<p>%s</p>" % e(t) for t in s["p"].split("\n\n"))) for s in g["guide"])
    faq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q["q"]), e(q["a"])) for q in g["faq"])
    toc = "".join('<li><a href="#p%d">%s %s</a></li>' % (p["rank"], e(p["brand"]), e(p["name"])) for p in ps)
    rel = [x for x in by_cat[g["cat"]] if x["slug"] != g["slug"]][:4]
    gi = guides.index(g)  # aanvullen met gidsen uit andere categorieen, per gids verschoven zodat elke gids inlinks krijgt
    rel += [x for x in (guides[(gi + 7 * j + 3) % len(guides)] for j in range(len(guides))) if x["cat"] != g["cat"] and x not in rel][:6 - len(rel)]
    url_abs = SITE + "/" + g["url"]
    def prod_ld(p):
        d = {"@type": "Product", "name": "%s %s" % (p["brand"], p["name"]), "brand": {"@type": "Brand", "name": p["brand"]},
             "description": p["oneliner"],
             "review": {"@type": "Review", "author": {"@type": "Organization", "name": "watkoopik"}, "reviewRating": {"@type": "Rating", "ratingValue": p["score"], "bestRating": 10, "worstRating": 1},
                        "positiveNotes": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": x} for i, x in enumerate(p["pros"])]},
                        "negativeNotes": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": x} for i, x in enumerate(p["cons"])]}},
             "offers": {"@type": "Offer", "price": "%.2f" % p["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": p.get("url") or url_abs}}
        if p.get("image"): d["image"] = p["image"]
        if p.get("ean"): d["gtin13"] = str(p["ean"])
        return d
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": g["title"], "url": url_abs, "numberOfItems": len(ps),
           "itemListElement": [{"@type": "ListItem", "position": p["rank"], "url": url_abs + "#p%d" % p["rank"], "item": prod_ld(p)} for p in ps]},
          {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["intro"][:200], "dateModified": g.get("updated", TODAY.isoformat()),
           "datePublished": g.get("published", g.get("updated", TODAY.isoformat())), "author": {"@type": "Organization", "name": "redactie watkoopik", "url": SITE + "/over-ons.html"},
           "publisher": {"@type": "Organization", "name": "watkoopik", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.svg"}}, "mainEntityOfPage": url_abs,
           "image": [p["image"] for p in ps if p.get("image")][:3]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in g["faq"]]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": CATS[g["cat"]][0], "item": SITE + "/categorie/%s.html" % g["cat"]},
              {"@type": "ListItem", "position": 3, "name": g["title"], "item": url_abs}]}]
    extra = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    body = '''<div class="wrap"><nav class="crumbs"><a href="../">Home</a> › <a href="../categorie/%s.html">%s</a> › %s</nav>
<div class="ghero"><span class="kick">Top 10 · %s</span><h1 class="split">%s</h1><p class="intro">%s</p>
<div class="meta-line"><span>Bijgewerkt <b>%s</b></span><span><b>%d</b> modellen</span><span><b>%s</b> reviews</span><span>Door <b>de redactie</b></span></div><div class="pref-wrap"><a class="pref-src" href="https://google.com/preferences/source?q=watkoopik.nl" target="_blank" rel="noopener" data-umami-event="preferred-source"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="#4285F4" d="M22.5 12.3c0-.8-.1-1.5-.2-2.3H12v4.3h5.9a5 5 0 0 1-2.2 3.3v2.7h3.6c2.1-1.9 3.2-4.8 3.2-8z"/><path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.6-2.7c-1 .7-2.2 1-3.7 1-2.9 0-5.3-1.9-6.2-4.5H2.1v2.8A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.8 14.1a6.6 6.6 0 0 1 0-4.2V7.1H2.1a11 11 0 0 0 0 9.8z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3 .6 4.2 1.6l3.1-3.1A11 11 0 0 0 2.1 7.1l3.7 2.8C6.7 7.3 9.1 5.4 12 5.4z"/></svg>Voeg watkoopik toe als voorkeursbron in Google</a></div>
<p class="disc">Wij ontvangen mogelijk een vergoeding als je via onze links iets koopt. Dit kost jou niets extra en bepaalt niet welke producten in de lijst staan. <a href="../zo-kiezen-wij.html">Zo kiezen wij</a>.</p></div>
<div class="podium">%s</div>
<div class="layout"><div>
<h2 id="vergelijk" class="rv" style="margin-top:22px">Alle %d naast elkaar</h2>%s
<h2 id="top10" class="rv">De top 10 in detail</h2>%s
<div class="verdict rv"><span class="kick" style="color:#ffb48a">Eindoordeel</span><h2>Onze conclusie</h2><p>%s</p>%s</div>
<div class="guide rv" id="koopgids"><h2>Koopgids: zo kies je de juiste %s</h2>%s</div>
<div class="faq rv" id="faq"><h2>Veelgestelde vragen</h2>%s</div>
</div>
<aside class="side"><details class="toc"><summary>In deze gids</summary><ol><li><a href="#vergelijk">Vergelijkingstabel</a></li>%s<li><a href="#koopgids">Koopgids</a></li><li><a href="#faq">Veelgestelde vragen</a></li></ol></details></aside>
</div>
<section style="padding:40px 0"><div class="sec-head"><h2>Ook interessant</h2></div><div class="gl">%s</div></section>
</div>
<div class="sticky-buy">%s<div><b>Nr. 1: %s %s</b>%s</div>%s</div>''' % (
        g["cat"], CATS[g["cat"]][0], e(g["short"]), CATS[g["cat"]][0], e(g["title"]), e(g["intro"]), e(nldate(g.get("updated", TODAY.isoformat()))), len(ps), e(str(g.get("reviews_total", ""))),
        podium, len(ps), table, cards, e(g["verdict"]), shop_a(top, g, plek="eindoordeel"), e(g["query"]), guide_html, faq, toc, "".join(gcard(x, root) for x in rel),
        ('<img src="%s" alt="">' % e(top["image"])) if top.get("image") else "", e(top["brand"]), e(top["name"]), eur(top["price"]), shop_a(top, g, "btn btn-buy btn-sm", "sticky"))
    bv = next((p for p in ps if p.get("label") == "Beste prijs-kwaliteit"), ps[1])
    title = "Beste %s %d: top 10 vergeleken | watkoopik" % (g["query"], YEAR)
    if len(title) > 62: title = "%s | watkoopik" % g["title"]
    desc = "De beste %s van %d is de %s %s (%s). Slimste koop: %s %s voor %s. Bekijk de volledige top 10 met plus- en minpunten, koopgids en FAQ." % (
        g["query"], YEAR, top["brand"], top["name"], eur(top["price"]), bv["brand"], bv["name"], eur(bv["price"]))
    page(g["url"], title, desc, body, extra=extra, img=top.get("image", ""))

# ---------- keuzehulp ----------
quiz = {}
for g in guides:
    prices = sorted(p["price"] for p in g["products"])
    lo, mid = prices[len(prices) // 3], prices[2 * len(prices) // 3]
    quiz[g["slug"]] = {"url": g["url"], "budgets": [
        {"max": lo, "label": "Tot %s" % eur(lo), "hint": "Zo voordelig mogelijk"},
        {"max": mid, "label": "Tot %s" % eur(mid), "hint": "Middenklasse"},
        {"max": 99999, "label": "Geen limiet", "hint": "Het beste is goed genoeg"}],
        "products": [{"name": "%s %s" % (p["brand"], p["name"]), "price": p["price"], "priceTxt": eur_n(p["price"]), "score": p["score"], "oneliner": p["oneliner"], "image": p.get("image", ""), "link": shop_link(p)} for p in g["products"]]}
q_opts = "".join('<button data-k="gids" data-v="%s"><b>%s</b><small>%s</small></button>' % (g["slug"], e(g["short"]), CATS[g["cat"]][0]) for g in guides)
qbody = '''<section data-hue="1" style="padding-top:34px"><div class="wrap">
<div style="text-align:center;max-width:680px;margin:0 auto 24px"><span class="kick">Keuzehulp</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">In drie vragen naar jouw beste keuze</h1><p class="muted">Kies een product, je budget en wat je het belangrijkst vindt. Wij rekenen de rest uit op basis van onze vergelijking.</p></div>
<div class="quiz"><div class="q-prog"><i></i></div>
<div class="q-step" data-i="0"><h3>1. Wat zoek je?</h3><div class="q-opts">%s</div></div>
<div class="q-step" data-i="1"><h3>2. Wat is je budget?</h3><div class="q-opts" id="q-budget"></div><button class="q-back">← Terug</button></div>
<div class="q-step" data-i="2"><h3>3. Wat vind je het belangrijkst?</h3><div class="q-opts">
<button data-k="prio" data-v="beste"><b>De allerbeste</b><small>Hoogste score in de vergelijking</small></button>
<button data-k="prio" data-v="prijs"><b>Slimste koop</b><small>Meeste kwaliteit per euro</small></button>
<button data-k="prio" data-v="premium"><b>Premium</b><small>Topmodel met alle extra's</small></button></div><button class="q-back">← Terug</button></div>
<div class="q-step" data-i="3"><div class="q-out"></div><button class="q-back">← Opnieuw kiezen</button></div>
</div></div></section>''' % q_opts
page("keuzehulp.html", "Keuzehulp: welk product past bij jou? | watkoopik", "Beantwoord drie vragen en ontdek welk product uit onze top 10-gidsen het beste bij jouw budget en wensen past.", qbody, "keuzehulp.html",
     extra="<script>window.QUIZ=%s</script>" % json.dumps(quiz, ensure_ascii=False))

# ---------- slimste koop ----------
def best_value(g):
    lab = next((p for p in g["products"] if p.get("label") == "Beste prijs-kwaliteit"), None)
    return lab or max(g["products"], key=lambda p: p["score"] / p["price"])
sv = "".join('<a class="rw rv" href="%s"><div class="rw-img">%s</div><div><h3>%s %s</h3><small>Slimste koop bij %s · score %s</small></div><b style="font-family:Sora">%s</b></a>' % (
    g["url"], img_of(best_value(g)), e(best_value(g)["brand"]), e(best_value(g)["name"]), e(g["short"].lower()), best_value(g)["score"], eur(best_value(g)["price"])) for g in guides)
page("slimste-koop.html", "De slimste koop per productsoort | watkoopik", "Per categorie het product met de beste prijs-kwaliteitverhouding uit onze top 10-gidsen.",
     '<section data-hue="1" style="padding-top:34px"><div class="wrap narrow"><span class="kick">Prijs-kwaliteit</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">De slimste koop per productsoort</h1><p class="muted">Niet het duurste, wel het verstandigste: per gids het model dat de meeste kwaliteit per euro biedt.</p><div class="rows" style="margin-top:20px">%s</div></div></section>' % sv, "slimste-koop.html")

# ---------- vaste pagina's ----------
def prose(path, title, desc, inner, active=None):
    page(path, title + " | watkoopik", desc, '<section data-hue="1" style="padding-top:34px"><div class="wrap prose">%s</div></section>' % inner, active)
prose("zo-kiezen-wij.html", "Zo kiezen wij", "Hoe watkoopik producten vergelijkt en rangschikt.", '''<span class="kick">Onze methode</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3rem)">Zo komen onze top 10's tot stand</h1>
<div class="numbers" style="margin:20px 0"><div class="rv"><b>4</b><span>criteria</span></div><div class="rv"><b>1000+</b><span>reviews per gids</span></div><div class="rv"><b>0</b><span>betaalde plekken</span></div><div class="rv"><b>Dagelijks</b><span>prijzen gecheckt</span></div></div>
<h2>Wat we wegen</h2><p>Elk product krijgt een score van 1 tot 10. <b>Prestaties</b> (40%): hoe goed doet het product zijn werk, op basis van specificaties en terugkerende ervaringen in reviews. <b>Prijs-kwaliteit</b> (25%): wat krijg je voor je geld vergeleken met de rest van de lijst. <b>Betrouwbaarheid</b> (20%): garantie, merkreputatie en klachten over defecten. <b>Gebruiksgemak</b> (15%): bediening, onderhoud en ergernissen.</p>
<h2>Onze bronnen</h2><p>Officiële specificaties van fabrikanten, productpagina's en reviewscores van grote Nederlandse winkels zoals bol. Waar beschikbaar gebruiken we ook onafhankelijke tests van gespecialiseerde media. Wij testen producten niet zelf in een lab. We zeggen dus nooit dat we iets getest hebben, wel dat we het vergeleken hebben.</p>
<h2>Hoe we geld verdienen</h2><p>Koop je via een link op onze site, dan ontvangen wij soms een kleine vergoeding van de winkel. Jij betaalt niets extra. Dit heeft geen invloed op de volgorde: merken kunnen geen plek kopen.</p>
<h2>Actualiteit</h2><p>Prijzen controleren we dagelijks bij bol. Lijsten bekijken we minimaal elke maand opnieuw. Verdwijnt een product of komt er een beter model, dan passen we de lijst eerder aan.</p>''', "zo-kiezen-wij.html")
prose("over-ons.html", "Over ons", "Over watkoopik: onafhankelijke koopgidsen.", '''<span class="kick">Over watkoopik</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3rem)">Een eerlijk overzicht, zodat jij slim koopt</h1>
<p>Wie een stofzuiger of koffiemachine zoekt, verdrinkt in honderden modellen en tegenstrijdige reviews. Wij wilden één plek waar je per productsoort in vijf minuten ziet wat de beste keuze is en waarom.</p>
<p>Daarom maken we top 10-lijsten: precies tien modellen die ertoe doen, met eerlijke plus- en minpunten en voor wie elk product geschikt is. watkoopik is onderdeel van 4NEON en werkt onafhankelijk van merken en winkels.</p>''')
prose("contact.html", "Contact", "Neem contact op met watkoopik.", '''<span class="kick">Contact</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3rem)">Vraag, tip of fout gezien?</h1>
<form action="https://formsubmit.co/hallo@watkoopik.nl" method="POST" style="display:grid;gap:12px;max-width:520px;margin-top:16px"><input type="hidden" name="_subject" value="Contact via watkoopik.nl"><input type="text" name="_honey" style="display:none">
<input name="naam" placeholder="Je naam" required style="padding:13px 16px;border:1.5px solid var(--line);border-radius:14px;font:inherit"><input type="email" name="email" placeholder="Je e-mailadres" required style="padding:13px 16px;border:1.5px solid var(--line);border-radius:14px;font:inherit"><textarea name="bericht" rows="6" placeholder="Je bericht" required style="padding:13px 16px;border:1.5px solid var(--line);border-radius:14px;font:inherit"></textarea><button class="btn btn-purple" type="submit">Versturen</button></form>''')
prose("disclaimer.html", "Affiliate-disclaimer", "Hoe watkoopik geld verdient.", '''<h1 style="font-size:2rem">Affiliate-disclaimer</h1><p>watkoopik neemt deel aan het bol Partnerprogramma. Koop je via een link op onze site, dan kunnen wij een vergoeding ontvangen. De prijs die jij betaalt verandert niet. Deze vergoeding heeft geen invloed op de volgorde van onze lijsten. Prijzen zijn indicatief; de actuele winkelprijs is leidend.</p>''')
prose("privacy.html", "Privacy", "Privacybeleid van watkoopik.", '''<h1 style="font-size:2rem">Privacy en cookies</h1><p>Wij plaatsen geen volgcookies. Bezoekersstatistieken meten we anoniem en zonder cookies. Gegevens uit het contactformulier gebruiken we alleen om te reageren. Klik je door naar een winkel, dan geldt het privacybeleid van die winkel. Vragen: <a href="mailto:hallo@watkoopik.nl">hallo@watkoopik.nl</a>.</p>''')
page("404.html", "Niet gevonden | watkoopik", "Pagina niet gevonden.", '<section style="padding-top:34px"><div class="wrap prose"><h1 style="font-size:2rem">Deze pagina bestaat niet</h1><p>Zoek hieronder of bekijk <a href="/gidsen.html">alle gidsen</a>.</p>' + searchbox() + '</div></section>', root="/")

prose("bedankt.html", "Bedankt", "Bedankt voor je bericht.", '<h1 style="font-size:2rem">Bedankt!</h1><p>We hebben je bericht ontvangen en reageren binnen twee werkdagen. <a href="./">Terug naar home</a>.</p>')
wr("stats.html", '<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=https://cloud.umami.is/share/sSKhb6j4KMk4E28R/watkoopik.nl"><title>Statistieken</title></head><body><a href="https://cloud.umami.is/share/sSKhb6j4KMk4E28R/watkoopik.nl">Naar het dashboard</a></body></html>')
# lastmod volgt echte wijzigingen (nieuwste gids), niet de bouwdatum, zodat Google het signaal blijft vertrouwen
LAST = max(g.get("updated", TODAY.isoformat()) for g in guides)
urls = [("", LAST, "1.0"), ("gidsen.html", LAST, "0.8"), ("keuzehulp.html", LAST, "0.7"), ("slimste-koop.html", LAST, "0.7"),
        ("zo-kiezen-wij.html", "2026-10-13", "0.4"), ("over-ons.html", "2026-10-13", "0.3"), ("contact.html", "2026-10-13", "0.3")]
urls += [("categorie/%s.html" % k, max(g.get("updated", TODAY.isoformat()) for g in by_cat[k]), "0.7") for k in CATS if by_cat.get(k)]
urls += [(g["url"], g.get("updated", TODAY.isoformat()), "0.9") for g in guides]
wr("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n" % (SITE, u, d, pr) for u, d, pr in urls) + "</urlset>\n")

# ---------- assets ----------
wr("style.css", rd("style.css")); wr("app.js", rd("app.js")); wr("favicon.svg", FAVICON)
for n in THEME_CSS: wr(n + ".css", rd(n + ".css"))
if THEME == "green": wr("favicon.svg", FAVICON.replace("#5b3fd6", "#0f5c4c"))
wr("CNAME", "watkoopik.com\n" if PREVIEW else "watkoopik.nl\n"); wr(".nojekyll", "")
wr("robots.txt", "User-agent: *\nDisallow: /\n" if PREVIEW else "User-agent: *\nAllow: /\nDisallow: /stats.html\nSitemap: %s/sitemap.xml\n" % SITE)
wr("search.json", json.dumps([{"t": g["title"], "u": g["url"], "c": CATS[g["cat"]][0], "w": "%s %s" % (win(g)["brand"], win(g)["name"]), "i": win(g).get("image", ""),
    "k": " ".join([g["query"], g["short"]] + g.get("keywords", []) + ["%s %s" % (p["brand"], p["name"]) for p in g["products"]])} for g in guides], ensure_ascii=False))
print("OK pro: %d gidsen, %d producten" % (len(guides), N_PROD))
