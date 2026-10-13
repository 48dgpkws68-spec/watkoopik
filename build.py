# -*- coding: utf-8 -*-
"""Bouwt watkoopik.nl: statische top 10-gidsen uit data/*.json.
Gebruik: python3 build.py   (schrijft HTML in deze map + sitemap, search.json)
Regels: Nederlands, geen em/en-dashes, geen ", en" in zichtbare tekst."""
import os, re, sys, json, glob, html, datetime, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_src"))
import logo as LOGO
import og as OG

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://watkoopik.nl"
NAME = "watkoopik"
TODAY = datetime.date.today()
BUILD_ID = datetime.datetime.now().strftime('%Y%m%d%H%M')
YEAR = TODAY.year
rd = lambda n: open(os.path.join(ROOT, "_src", n), encoding="utf-8").read()
def wr(path, s):
    p = os.path.join(ROOT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)
e = html.escape
OG.card(os.path.join(ROOT, "og/default.jpg"), "Wat koop ik? Onafhankelijke top 10-lijsten van %d" % YEAR, "Koopgidsen", "#5b3fd6")

ICONS = {
    "huishouden": '<path d="M9 3h6l1 9H8z"/><path d="M8 12h8v3a4 4 0 0 1-8 0z"/><path d="M12 3V1"/>',
    "keuken": '<path d="M4 12h16"/><path d="M6 12v6a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-6"/><path d="M8 12V8a4 4 0 0 1 8 0v4"/>',
    "verzorging": '<path d="M6 4h8a5 5 0 0 1 0 10H9"/><path d="M9 14v6"/><path d="M14 9h4"/>',
    "slapen": '<path d="M3 18V9a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v9"/><path d="M3 14h18"/><path d="M7 7V5h4v2"/>',
    "elektronica": '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/>',
    "wonen": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "sport": '<circle cx="12" cy="12" r="9"/><path d="M12 3v18"/><path d="M3 12h18"/>',
    "kind": '<circle cx="12" cy="8" r="4"/><path d="M5 21a7 7 0 0 1 14 0"/>',
    "klussen": '<path d="M14 4l6 6-9 9H5v-6z"/><path d="M12 6l6 6"/>',
}
def icon(cat, size=28):
    return '<svg class="ico-line" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, ICONS.get(cat, ICONS["huishouden"]))

CATS = {
    "huishouden": ("Huishouden", "🧹", "Stofzuigers, wasmachines, strijkijzers en alles wat het huis schoon houdt"),
    "keuken":     ("Keuken", "🍳", "Airfryers, koffiemachines, blenders en keukenhulpen"),
    "verzorging": ("Verzorging", "💇", "Föhns, tandenborstels, trimmers en huidverzorging"),
    "slapen":     ("Slapen", "🛏️", "Matrassen, kussens, dekbedden en alles voor een betere nacht"),
    "elektronica":("Elektronica", "🎧", "Oordopjes, speakers, tv's en slimme gadgets"),
    "wonen":      ("Wonen", "🛋️", "Verlichting, klimaat en comfort in huis"),
    "sport":      ("Sport & buiten", "🚴", "Fitness, fietsen en buitenleven"),
    "kind":       ("Baby & kind", "🧸", "Kinderwagens, babyfoons en speelgoed"),
    "klussen":    ("Klussen & tuin", "🔧", "Gereedschap, tuinmachines en doe-het-zelf"),
}
COLORS = ["#1b3fb3","#0f766e","#b4531b","#6d28d9","#be185d","#0e7490","#4d7c0f","#9a3412","#1e3a8a","#7c2d12"]

BOL_SITE_ID = "1549706"  # watkoopik.nl in het bol Partnerprogramma

def shop_attrs(p, g):
    """data-attributen zodat Umami elke klik op een bol-knop meet (gids, product, positie)."""
    return ' data-umami-event="bol-klik" data-umami-event-gids="%s" data-umami-event-product="%s" data-umami-event-positie="%s"' % (
        g["slug"], e("%s %s" % (p["brand"], p["name"])), p.get("rank", ""))

def shop_a(p, g):
    """Volledige attributen voor een bol-knop: partnerlink + Umami-event."""
    return 'href="%s" rel="sponsored nofollow noopener" target="_blank" data-shop%s' % (shop_link(p, g), shop_attrs(p, g))

def shop_link(p, g):
    """Centrale plek voor de winkel-link: bol-partnerlink (deeplink naar product-URL of zoekresultaat)."""
    q = p.get("search") or ("%s %s" % (p["brand"], p["name"]))
    target = p.get("url") or ("https://www.bol.com/nl/nl/s/?searchtext=" + urllib.parse.quote_plus(q))
    name = re.sub(r"[^A-Za-z0-9 ]", "", "%s %s" % (p["brand"], p["name"]))[:60]
    return "https://partner.bol.com/click/click?p=2&t=url&s=%s&f=TXL&url=%s&name=%s" % (BOL_SITE_ID, urllib.parse.quote(target, safe=""), urllib.parse.quote_plus(name))

def nldate(iso):
    try:
        y, m, d = [int(x) for x in str(iso)[:10].split("-")]
        return "%d %s %d" % (d, MONTHS[m], y)
    except Exception:
        return str(iso)

def eur(v):
    s = ("%.2f" % v).replace(".", ",")
    return "€ " + (s[:-3] if s.endswith(",00") else s)

STAR = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.7.8-4.9 4.6 1.3 6.6L12 17.3l-6 3.3 1.3-6.6L2.4 9.4l6.7-.8z" fill="%s"/></svg>'
def stars(score):
    full = int(round(score / 2))
    return '<span class="stars" aria-label="%s van 10">%s</span>' % (score, "".join(STAR % ("#f5b324" if i < full else "#dfe3ee") for i in range(5)))

def check_copy(s, where):
    bad = []
    if "—" in s or "–" in s: bad.append("streepje")
    if re.search(r", en\b", s): bad.append("', en'")
    if bad: raise SystemExit("Copy-fout in %s: %s" % (where, ", ".join(bad)))

# ---------- chrome ----------
NAV = [("gidsen.html", "Alle gidsen"), ("categorie/huishouden.html", "Huishouden"), ("categorie/keuken.html", "Keuken"),
       ("categorie/verzorging.html", "Verzorging"), ("categorie/elektronica.html", "Elektronica"), ("zo-kiezen-wij.html", "Zo kiezen wij")]

def head(title, desc, canon, root, extra="", img=None):
    img = img or SITE + "/og/default.jpg"
    return '''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:type" content="article"><meta property="og:site_name" content="watkoopik.nl"><meta property="og:locale" content="nl_NL"><meta property="og:image" content="%s"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%s">
<link rel="icon" href="%sfavicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%sstyle.css?v=%s">
<script>window.ROOT=%s</script>
<script defer src="https://cloud.umami.is/script.js" data-website-id="47030ca7-838e-4840-9d90-0c8b315ba5e8"></script>
%s
</head>
<body>''' % (e(title), e(desc), canon, e(title), e(desc), canon, e(img), e(img), root, root, BUILD_ID, json.dumps(root), extra)

def chrome(active, root):
    links = "".join('<li><a href="%s%s"%s>%s</a></li>' % (root, h, ' class="active"' if h == active else "", t) for h, t in NAV)
    mm = "".join('<a href="%s%s">%s</a>' % (root, h, t) for h, t in NAV + [("over-ons.html", "Over ons"), ("contact.html", "Contact")])
    return '''<div class="topbar">Onafhankelijke top 10-gidsen<span class="tb-x"> · <strong>Elke dag nieuwe vergelijkingen</strong> · prijzen gecheckt in %s %s</span></div>
<header class="nav"><div class="nav-in">
<a class="brand" href="%sindex.html" aria-label="watkoopik, naar de homepage">%s</a>
<ul class="nav-links">%s</ul>
<div class="search-wrap"><label class="search"><span aria-hidden="true">🔍</span><input type="search" placeholder="Zoek een product…" data-search aria-label="Zoek een gids"></label><div class="search-results"></div></div>
<button class="burger" id="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="mobile-menu" id="mobileMenu"><div class="search-wrap"><label class="search"><span aria-hidden="true">🔍</span><input type="search" placeholder="Zoek een product…" data-search aria-label="Zoek een gids"></label><div class="search-results"></div></div>%s</div>
''' % (MONTHS[TODAY.month], YEAR, root, LOGO.lockup(38), links, mm)

MONTHS = ["", "januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"]

def footer(root, guides):
    pop = "".join('<li><a href="%s%s">%s</a></li>' % (root, g["url"], e(g["short"])) for g in guides[:8])
    cats = "".join('<li><a href="%scategorie/%s.html">%s</a></li>' % (root, k, v[0]) for k, v in CATS.items())
    return '''<footer><div class="wrap"><div class="cols">
<div><h4>watkoopik.nl</h4><p style="font-size:.92rem">Wij vergelijken producten op specificaties, prijs en duizenden gebruikersreviews. Zo weet jij in vijf minuten wat je het beste kunt kopen.</p></div>
<div><h4>Populaire gidsen</h4><ul>%s</ul></div>
<div><h4>Categorieën</h4><ul>%s</ul></div>
<div><h4>Over</h4><ul><li><a href="%szo-kiezen-wij.html">Zo kiezen wij</a></li><li><a href="%sover-ons.html">Over ons</a></li><li><a href="%scontact.html">Contact</a></li><li><a href="%sprivacy.html">Privacy &amp; cookies</a></li><li><a href="%sdisclaimer.html">Affiliate-disclaimer</a></li></ul></div>
</div>
<div class="fine">© %s watkoopik.nl · Wij ontvangen mogelijk een vergoeding als je via onze links iets koopt. Dit kost jou niets extra en beïnvloedt onze rangschikking niet. Prijzen zijn indicatief en kunnen afwijken van de actuele winkelprijs.</div>
</div></footer>
<script src="%sapp.js?v=%s" defer></script>
</body></html>''' % (pop, cats, root, root, root, root, root, YEAR, root, BUILD_ID)

# ---------- data ----------
guides = []
for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
    g = json.load(open(f, encoding="utf-8"))
    g["url"] = "beste/%s.html" % g["slug"]
    g["color"] = g.get("color") or COLORS[len(guides) % len(COLORS)]
    ps = g["products"]
    for i, p in enumerate(ps):
        p["rank"] = i + 1
        if i == 0 and not p.get("label"): p["label"] = "Beste keuze"
    guides.append(g)
guides.sort(key=lambda g: (g.get("prio", 50), g["slug"]))
by_cat = {}
for g in guides: by_cat.setdefault(g["cat"], []).append(g)
by_slug = {g["slug"]: g for g in guides}

# ---------- guide page ----------
def pimg(p, g):
    if p.get("image"):
        return '<div class="pimg photo"><span class="rk">%d</span><img src="%s" alt="%s %s" loading="lazy" width="400" height="400"></div>' % (p["rank"], e(p["image"]), e(p["brand"]), e(p["name"]))
    return '<div class="pimg" style="background:linear-gradient(135deg,%s,%s99)"><span class="rk">%d</span><span class="ico" aria-hidden="true">%s</span><span class="br">%s</span></div>' % (g["color"], g["color"], p["rank"], g["ico"], e(p["brand"]))

def guide_page(g):
    root = "../"; ps = g["products"]; url = SITE + "/" + g["url"]
    title = "%s (%s) | watkoopik.nl" % (g["title"], YEAR) if str(YEAR) not in g["title"] else g["title"] + " | watkoopik.nl"
    desc = g.get("desc") or ("Op zoek naar de beste %s? Wij vergeleken prijs, specificaties en reviews. Bekijk de top 10 van %s met voor- en nadelen per model." % (g["query"], YEAR))

    # winnaars
    labs = [p for p in ps if p.get("label")][:3]
    wins = "".join('''<div class="win%s">%s%s<span class="tag">%s</span><h3>%s %s</h3><div class="price">%s</div><p>%s</p><a class="btn btn-shop btn-sm" %s>Bekijk bij bol</a></div>''' % (
        " first" if i == 0 else "", '<span class="ribbon">Onze keuze</span>' if i == 0 else "", ('<img class="win-img" src="%s" alt="" loading="lazy">' % e(p["image"])) if p.get("image") else ('<div class="win-img ph" style="background:linear-gradient(135deg,%s,%s99)">%s</div>' % (g["color"], g["color"], g["ico"])), e(p["label"]), e(p["brand"]), e(p["name"]), eur(p["price"]), e(p["oneliner"]), shop_a(p, g)) for i, p in enumerate(labs))

    # tabel
    spec_keys = list(ps[0]["specs"].keys())[:3]
    rows = "".join('<tr><td><span class="rank%s">%d</span></td><td class="name">%s%s<small>%s</small></td>%s<td>%s</td><td><span class="score%s">%s</span></td><td><a class="btn btn-shop btn-sm" %s>Bekijk</a></td></tr>' % (
        " r1" if p["rank"] == 1 else "", p["rank"], ('<img class="tbl-img" src="%s" alt="" loading="lazy">' % e(p["image"])) if p.get("image") else "", e(p["brand"]), e(p["name"]),
        "".join("<td>%s</td>" % e(str(p["specs"].get(k, "-"))) for k in spec_keys), eur(p["price"]),
        " hi" if p["score"] >= 9 else "", p["score"], shop_a(p, g)) for p in ps)
    table = '<div class="tbl-wrap"><table class="cmp"><thead><tr><th>#</th><th>Model</th>%s<th>Prijs</th><th>Score</th><th></th></tr></thead><tbody>%s</tbody></table></div>' % ("".join("<th>%s</th>" % e(k) for k in spec_keys), rows)

    # producten
    blocks = []
    for p in ps:
        specs = "".join("<span><b>%s:</b> %s</span>" % (e(k), e(str(v))) for k, v in p["specs"].items())
        pros = "".join("<li>%s</li>" % e(x) for x in p["pros"]); cons = "".join("<li>%s</li>" % e(x) for x in p["cons"])
        lab = '<span class="label%s">%s</span>' % (" gold" if p["rank"] == 1 else "", e(p["label"])) if p.get("label") else ""
        blocks.append('''<article class="prod%s" id="p%d">
<div class="prod-head">
%s
<div>%s<h2>%d. %s %s</h2>
<div class="meta"><span class="price">%s</span><span>%s <b>%s</b>/10</span><span>%s</span></div>
<div class="specs">%s</div>
</div></div>
<div class="txt">%s</div>
<div class="pc"><div class="pros"><h4>Pluspunten</h4><ul>%s</ul></div><div class="cons"><h4>Minpunten</h4><ul>%s</ul></div></div>
<div class="ideal"><b>Ideaal voor:</b> %s</div>
<div class="prod-cta"><a class="btn btn-shop" %s>Bekijk prijs bij bol <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a><small>Prijs gecheckt op %s</small></div>
</article>''' % (" top" if p["rank"] == 1 else "", p["rank"], pimg(p, g), lab, p["rank"], e(p["brand"]), e(p["name"]),
            eur(p["price"]), stars(p["score"]), p["score"], e(p.get("reviews", "")), specs,
            "".join("<p>%s</p>" % e(t) for t in p["text"].split("\n\n")), pros, cons, e(p["ideal"]), shop_a(p, g), e(nldate(nldate(g.get("updated", TODAY.isoformat()))))))

    toc = "".join('<li><a href="#p%d">%s %s</a></li>' % (p["rank"], e(p["brand"]), e(p["name"])) for p in ps)
    guide_html = "".join("<h3>%s</h3>%s" % (e(s["h"]), "".join("<p>%s</p>" % e(t) for t in s["p"].split("\n\n"))) for s in g["guide"])
    faq_html = "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q["q"]), e(q["a"])) for q in g["faq"])
    rel = [x for x in by_cat[g["cat"]] if x["slug"] != g["slug"]][:4] or [x for x in guides if x["slug"] != g["slug"]][:4]
    related = "".join(feature(x, root) for x in rel[:3])

    ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": g["title"], "url": url, "numberOfItems": len(ps),
           "itemListElement": [{"@type": "ListItem", "position": p["rank"], "name": "%s %s" % (p["brand"], p["name"])} for p in ps]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in g["faq"]]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": CATS[g["cat"]][0], "item": SITE + "/categorie/%s.html" % g["cat"]},
              {"@type": "ListItem", "position": 3, "name": g["title"], "item": url}]}]
    top = ps[0]
    og_rel = "og/%s.jpg" % g["slug"]
    OG.card(os.path.join(ROOT, og_rel), g["title"], "Top 10 · %s" % CATS[g["cat"]][0], g.get("color"), top.get("image"))
    upd = g.get("updated", TODAY.isoformat())
    ld.append({"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": desc, "image": SITE + "/" + og_rel,
               "datePublished": g.get("published", upd), "dateModified": upd, "inLanguage": "nl-NL", "mainEntityOfPage": url,
               "author": {"@type": "Organization", "name": "redactie watkoopik.nl", "url": SITE + "/over-ons.html"},
               "publisher": {"@type": "Organization", "name": "watkoopik.nl", "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/og/default.jpg"}}})
    extra = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    page = head(title, desc, url, root, extra, SITE + "/" + og_rel) + chrome(None, root) + '''
<main class="wrap">
<nav class="crumbs" aria-label="Kruimelpad"><a href="../index.html">Home</a> › <a href="../categorie/%s.html">%s</a> › %s</nav>
<div class="art-head"><div class="kicker">Top 10 · %s</div><h1>%s</h1><p class="intro">%s</p>
<div class="byline"><span>Door <b>de redactie van watkoopik</b></span><span>Bijgewerkt op <b>%s</b></span><span><b>%d modellen</b> vergeleken</span><span><b>%s</b> reviews meegewogen</span></div>
<div class="disc">Wij ontvangen mogelijk een vergoeding als je via onze links iets koopt. Dat kost jou niets extra en bepaalt niet welke producten in de lijst staan. <a href="../zo-kiezen-wij.html">Lees hoe wij kiezen</a>.</div></div>

<div class="winners">%s</div>

<div class="layout">
<div>
<h2 id="vergelijk">Alle %d in één overzicht</h2>%s
<h2 id="top10">De top 10 in detail</h2>
%s
<div class="verdict"><h2>Ons eindoordeel</h2><p>%s</p><a class="btn btn-shop" %s>Bekijk %s %s bij bol</a></div>
<div class="guide" id="koopgids"><h2>Koopgids: zo kies je de juiste %s</h2>%s</div>
<div class="faq" id="faq"><h2>Veelgestelde vragen</h2>%s</div>
</div>
<aside class="side"><details class="toc" id="toc"><summary><h4>In deze gids</h4></summary><ol><li><a href="#vergelijk">Vergelijkingstabel</a></li>%s<li><a href="#koopgids">Koopgids</a></li><li><a href="#faq">Veelgestelde vragen</a></li></ol></details>
<div class="box"><h4>Zo kwamen wij tot deze lijst</h4><ul><li>Specificaties van de fabrikant vergeleken</li><li>Gebruikersreviews bij bol en andere winkels geanalyseerd</li><li>Prijs afgezet tegen prestaties</li><li>Elke maand opnieuw gecheckt</li></ul></div></aside>
</div>
<section class="related"><div class="sec-head"><h2>Ook interessant</h2></div><div class="feat-grid">%s</div></section>
</main>
<div class="sticky-cta" id="stickyCta"><div class="in"><div><b>Onze nummer 1: %s %s</b>%s</div><a class="btn btn-shop btn-sm" %s>Bekijk bij bol</a></div></div>
''' % (g["cat"], CATS[g["cat"]][0], e(g["short"]), CATS[g["cat"]][0], e(g["title"]), e(g["intro"]), e(nldate(nldate(g.get("updated", TODAY.isoformat())))), len(ps), e(g.get("reviews_total", "duizenden")),
       wins, len(ps), table, "".join(blocks), e(g["verdict"]), shop_a(top, g), e(top["brand"]), e(top["name"]), e(g["query"]), guide_html, faq_html, toc, related,
       e(top["brand"]), e(top["name"]), eur(top["price"]), shop_a(top, g)) + footer(root, guides)
    check_copy(page, g["slug"])
    wr(g["url"], page)

# ---------- listing helpers ----------
def card(g, root):
    imgs = [p["image"] for p in g["products"] if p.get("image")][:3]
    if imgs:
        thumb = '<div class="thumb collage"><span class="n">Top %d</span>%s</div>' % (len(g["products"]), "".join('<img src="%s" alt="" loading="lazy">' % e(i) for i in imgs))
    else:
        thumb = '<div class="thumb" style="background:linear-gradient(135deg,%s,%s99)"><span class="n">Top %d</span>%s</div>' % (g["color"], g["color"], len(g["products"]), g["ico"])
    return '<a class="card" href="%s%s">%s<div class="body"><h3>%s</h3><p>%s</p><div class="meta">%s · bijgewerkt %s</div></div></a>' % (
        root, g["url"], thumb, e(g["title"]), e(g["intro"][:120].rsplit(" ", 1)[0] + "…"), CATS[g["cat"]][0], e(nldate(g.get("updated", TODAY.isoformat()))))

def simple(fn, title, body, desc, active=None):
    root = ""
    page = head(title + " | watkoopik.nl", desc, SITE + "/" + fn, root) + chrome(active, root) + '<main class="wrap">%s</main>' % body + footer(root, guides)
    check_copy(page, fn); wr(fn, page)

# ---------- home ----------
cat_cards = "".join('<a class="cat" href="categorie/%s.html"><span class="ico">%s</span>%s<small>%d gidsen</small></a>' % (k, icon(k, 30), v[0], len(by_cat.get(k, []))) for k, v in CATS.items() if by_cat.get(k))
chips = "".join('<a class="chip" href="%s">%s</a>' % (g["url"], e(g["short"])) for g in guides[:8])
def winner_of(g):
    return g["products"][0]

def feature(g, root=""):
    p = winner_of(g)
    img = ('<img src="%s" alt="%s %s" loading="lazy">' % (e(p["image"]), e(p["brand"]), e(p["name"]))) if p.get("image") else ('<div class="ph" style="background:linear-gradient(135deg,%s,%s99)">%s</div>' % (g["color"], g["color"], g["ico"]))
    return '''<a class="feat" href="%s%s"><div class="feat-img">%s</div><div class="feat-body"><span class="kick">%s · Top 10</span><h3>%s</h3><p>%s</p><div class="feat-win"><span class="dot"></span>Winnaar: <b>%s %s</b> · %s</div></div></a>''' % (
        root, g["url"], img, CATS[g["cat"]][0], e(g["title"]), e(g["intro"][:150].rsplit(" ", 1)[0] + "…"), e(p["brand"]), e(p["name"]), eur(p["price"]))

def row(g, root=""):
    p = winner_of(g)
    img = ('<img src="%s" alt="" loading="lazy">' % e(p["image"])) if p.get("image") else ('<div class="ph" style="background:linear-gradient(135deg,%s,%s99)">%s</div>' % (g["color"], g["color"], g["ico"]))
    return '''<a class="row" href="%s%s"><div class="row-img">%s</div><div><h3>%s</h3><div class="row-win">Winnaar: <b>%s %s</b> · %s</div></div><span class="row-arrow">→</span></a>''' % (root, g["url"], img, e(g["title"]), e(p["brand"]), e(p["name"]), eur(p["price"]))

top = guides[0]; tp = winner_of(top)
hero_card = '''<a class="hero-card" href="%s"><span class="hero-tag">Winnaar van de week</span><div class="hero-card-img">%s</div><div class="hero-card-body"><small>%s</small><h3>%s %s</h3><div class="hero-price">%s <span>bij bol</span></div><span class="btn btn-shop btn-sm">Bekijk de top 10</span></div></a>''' % (
    top["url"], ('<img src="%s" alt="">' % e(tp["image"])) if tp.get("image") else "", e(top["title"]), e(tp["brand"]), e(tp["name"]), eur(tp["price"]))
cat_pills = "".join('<a class="pill" href="categorie/%s.html">%s<span>%s</span></a>' % (k, icon(k, 20), v[0]) for k, v in CATS.items() if by_cat.get(k))
feat_html = "".join(feature(g) for g in guides[:3])
rows_html = "".join(row(g) for g in guides[3:11])
cat_sections = "".join('''<section class="catsec"><div class="wrap"><div class="sec-head"><div><span class="kick">%s</span><h2>De beste %s</h2></div><a class="more" href="categorie/%s.html">Alle %d gidsen →</a></div><div class="feat-grid">%s</div></div></section>''' % (
    v[2], v[0].lower(), k, len(by_cat[k]), "".join(feature(g) for g in by_cat[k][:3])) for k, v in CATS.items() if by_cat.get(k) and k in ("keuken", "verzorging", "elektronica", "slapen"))
mq_items = []
for g in guides:
    pr = next((p for p in g["products"][:3] if p.get("image")), None)
    if pr: mq_items.append('<a class="mq-item" href="%s" title="%s"><img src="%s" alt="" loading="lazy"><span>%s</span></a>' % (g["url"], e(g["title"]), e(pr["image"]), e(g["short"])))
half = max(1, len(mq_items) // 2)
def mq_row(items, cls):
    inner = "".join(items) * 2  # dubbel voor een naadloze lus
    return '<div class="mq %s" aria-hidden="true"><div class="mq-track">%s</div></div>' % (cls, inner)
marquee = '<section class="mq-wrap">%s%s</section>' % (mq_row(mq_items[:half], "mq-left"), mq_row(mq_items[half:], "mq-right"))
home = '''
<section class="hero"><div class="wrap hero-grid"><div>
<span class="kick">Onafhankelijke koopgidsen</span>
<h1>Wat koop ik?<br><em>Wij zochten het uit.</em></h1>
<p class="lead">Elke dag een nieuwe top 10 van de beste producten. Vergeleken op prijs, specificaties en duizenden reviews, zodat jij in vijf minuten de juiste keuze maakt.</p>
<div class="hero-search search-wrap"><label class="search"><span aria-hidden="true">🔍</span><input type="search" placeholder="Zoek een product, bijvoorbeeld airfryer…" data-search aria-label="Zoek een gids"></label><div class="search-results"></div></div>
<div class="pills">%s</div>
</div>%s</div></section>
%s
<section><div class="wrap"><div class="sec-head"><div><span class="kick">Nieuw deze week</span><h2>De nieuwste gidsen</h2></div><a class="more" href="gidsen.html">Alle %d gidsen →</a></div>
<div class="feat-grid">%s</div>
<div class="rows">%s</div></div></section>
%s
<section class="band"><div class="wrap band-grid">
<div><span class="kick kick-light">Zo werken wij</span><h2>Geen betaalde plekken. Wel duidelijke keuzes.</h2><p>Merken kunnen geen positie kopen. We wegen prestaties, prijs-kwaliteit, betrouwbaarheid en gebruiksgemak. Prijzen checken we dagelijks bij bol.</p><a class="btn btn-ghost" href="zo-kiezen-wij.html">Lees onze methode</a></div>
<div class="stats"><div><b>%d</b>top 10-gidsen</div><div><b>%d</b>producten vergeleken</div><div><b>4</b>criteria per product</div><div><b>Dagelijks</b>prijzen gecheckt</div></div>
</div></section>
<section class="seo"><div class="wrap narrow"><h2>Zo vind je snel wat je zoekt</h2><p>Typ een product in de zoekbalk, bijvoorbeeld <a href="beste/beste-airfryer.html">airfryer</a>, <a href="beste/beste-stofzuiger.html">stofzuiger</a> of <a href="beste/beste-koptelefoon.html">koptelefoon</a>, of kies een categorie. Elke gids begint met de drie winnaars (beste keuze, beste prijs-kwaliteit en beste premium), gevolgd door een vergelijkingstabel van alle tien modellen, een uitleg per product met plus- en minpunten, een koopgids en antwoorden op veelgestelde vragen. Prijzen worden dagelijks bij bol gecontroleerd.</p></div></section>
<section><div class="wrap"><div class="newsletter"><div><h3 style="margin:0 0 4px">Nieuwe top 10's in je mailbox</h3><p style="margin:0;color:var(--ink2)">Eén mail per week met de nieuwste vergelijkingen en prijsdalingen.</p></div><form action="https://formsubmit.co/hallo@watkoopik.nl" method="POST"><input type="hidden" name="_subject" value="Nieuwsbrief aanmelding watkoopik"><input type="hidden" name="_next" value="%s/bedankt.html"><input type="email" name="email" placeholder="je@email.nl" required><button class="btn btn-brand" type="submit">Aanmelden</button></form></div></div></section>
''' % (cat_pills, hero_card, marquee, len(guides), feat_html, rows_html, cat_sections, len(guides), sum(len(g["products"]) for g in guides), SITE)
page = head("De beste producten van %d vergeleken | watkoopik.nl" % YEAR, "Wat koop ik? Onafhankelijke top 10-lijsten met de beste stofzuigers, airfryers, föhns en meer. Specificaties, prijzen en reviews vergeleken.", SITE + "/", "",
            '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": "watkoopik.nl", "url": SITE + "/", "potentialAction": {"@type": "SearchAction", "target": SITE + "/gidsen.html?q={search_term_string}", "query-input": "required name=search_term_string"}}, ensure_ascii=False)) + chrome(None, "") + "<main>%s</main>" % home + footer("", guides)
check_copy(page, "index"); wr("index.html", page)

# ---------- gidsen + categorieën ----------
simple("gidsen.html", "Alle top 10-gidsen", '<div class="art-head"><h1>Alle top 10-gidsen</h1><p class="intro">%d vergelijkingen, elke dag komen er nieuwe bij.</p></div>%s' % (len(guides), "".join('<section><div class="sec-head"><h2>%s</h2></div><div class="feat-grid">%s</div></section>' % (v[0], "".join(feature(g, "") for g in by_cat[k])) for k, v in CATS.items() if by_cat.get(k))),
       "Overzicht van alle top 10-gidsen op watkoopik.nl, van stofzuigers tot koffiemachines.", "gidsen.html")
for k, v in CATS.items():
    gs = by_cat.get(k, [])
    root = "../"
    body = '<nav class="crumbs"><a href="../index.html">Home</a> › %s</nav><div class="art-head"><div class="kicker">Categorie</div><h1>De beste %s van %d</h1><p class="intro">%s. In deze %d gidsen vergelijken we per productsoort de tien beste modellen op prijs, specificaties en gebruikersreviews, met een duidelijke winnaar, de beste prijs-kwaliteit en de beste premium keuze.</p></div><div class="feat-grid">%s</div>' % (v[0], v[0].lower(), YEAR, v[2], len(gs), "".join(feature(g, root) for g in gs) or "<p>Binnenkort verschijnen hier de eerste gidsen.</p>")
    page = head("Beste %s van %d | watkoopik.nl" % (v[0].lower(), YEAR), v[2] + ". Vergelijk de beste producten in top 10-lijsten.", SITE + "/categorie/%s.html" % k, root) + chrome("categorie/%s.html" % k, root) + '<main class="wrap">%s</main>' % body + footer(root, guides)
    check_copy(page, k); wr("categorie/%s.html" % k, page)

for g in guides: guide_page(g)

# ---------- vaste pagina's ----------
simple("zo-kiezen-wij.html", "Zo kiezen wij", '''<div class="art-head prose"><div class="kicker">Onze methode</div><h1>Zo komen onze top 10's tot stand</h1><p class="intro">Een lijst is pas nuttig als je weet hoe hij gemaakt is. Daarom leggen we hier precies uit wat we wel en niet doen.</p></div>
<div class="prose">
<div class="bento"><div><b>4</b>criteria per product</div><div><b>1000+</b>reviews per gids</div><div><b>0</b>betaalde plekken</div><div><b>30 dagen</b>maximale leeftijd van prijzen</div></div>
<h2>Wat we wegen</h2>
<p>Elk product krijgt een score van 1 tot 10 op vier onderdelen. <b>Prestaties</b> (40%%): hoe goed doet het product waarvoor het gemaakt is, afgeleid uit specificaties, metingen van fabrikanten en terugkerende ervaringen in reviews. <b>Prijs-kwaliteit</b> (25%%): wat krijg je voor je geld vergeleken met de rest van de lijst. <b>Betrouwbaarheid</b> (20%%): garantie, merkreputatie en het aandeel klachten over defecten. <b>Gebruiksgemak</b> (15%%): bediening, onderhoud en hoe vaak gebruikers er ergernissen over melden.</p>
<h2>Waar onze informatie vandaan komt</h2>
<p>We gebruiken de officiële specificaties van fabrikanten, productpagina's en reviewscores van grote Nederlandse winkels zoals bol. Waar beschikbaar gebruiken we ook onafhankelijke tests van gespecialiseerde media. We testen producten niet zelf in een lab. We zeggen dus nooit dat we iets getest hebben, we zeggen dat we het vergeleken hebben.</p>
<h2>Hoe we aan geld komen</h2>
<p>Als je via een link op onze site iets koopt, ontvangen wij soms een kleine vergoeding van de winkel. Jij betaalt daardoor niets extra. Deze vergoeding heeft geen invloed op de volgorde van de lijst: een product op nummer 1 levert ons niet meer op dan een product op nummer 10. Merken kunnen geen plek kopen en wij schrijven geen betaalde reviews.</p>
<h2>Hoe actueel zijn de lijsten?</h2>
<p>Bij elke gids staat de datum waarop prijzen voor het laatst gecheckt zijn. Lijsten worden minimaal elke maand opnieuw bekeken. Komt er een belangrijk nieuw model uit of verdwijnt een product uit de handel, dan passen we de lijst eerder aan. Prijzen in winkels veranderen dagelijks, dus de prijs bij de winkel is altijd de juiste.</p>
<h2>Fout gezien?</h2>
<p>Klopt een specificatie niet of is een product niet meer leverbaar? <a href="contact.html">Laat het ons weten</a>. We passen het binnen een paar dagen aan.</p>
</div>''', "Lees hoe watkoopik.nl producten vergelijkt en rangschikt: criteria, bronnen en hoe wij geld verdienen.", "zo-kiezen-wij.html")

simple("over-ons.html", "Over ons", '''<div class="art-head prose"><h1>Over watkoopik</h1><p class="intro">Wij geloven dat een goede aankoop begint met een eerlijk overzicht.</p></div><div class="prose">
<p>watkoopik.nl is begonnen uit frustratie. Wie een stofzuiger of koffiemachine zoekt, verdrinkt in honderden modellen, tegenstrijdige reviews en webshops die vooral hun eigen aanbod aanprijzen. Wij wilden één plek waar je per productsoort in vijf minuten ziet wat de beste keuze is en waarom.</p>
<p>Daarom maken we top 10-lijsten. Niet eindeloos, maar precies tien modellen die er echt toe doen, met een eerlijke uitleg van voor- en nadelen. Voor elk product zoeken we uit voor wie het geschikt is, want de beste stofzuiger voor een appartement is een andere dan voor een gezin met twee honden.</p>
<p>watkoopik.nl is onderdeel van 4NEON, een Nederlands bedrijf dat meerdere online platforms ontwikkelt. We werken onafhankelijk van merken en winkels. <a href="zo-kiezen-wij.html">Lees hoe we onze lijsten samenstellen</a>.</p></div>''', "Over watkoopik.nl: onafhankelijke top 10-gidsen voor slimme aankopen.")

simple("contact.html", "Contact", '''<div class="art-head prose"><h1>Contact</h1><p class="intro">Een fout gezien, een product dat ontbreekt of een vraag? We horen het graag.</p></div><div class="prose">
<form action="https://formsubmit.co/hallo@watkoopik.nl" method="POST" style="display:grid;gap:12px;max-width:520px"><input type="hidden" name="_subject" value="Contact via watkoopik.nl"><input type="hidden" name="_next" value="%s/bedankt.html"><input type="text" name="_honey" style="display:none">
<input type="text" name="naam" placeholder="Je naam" required style="padding:12px;border:1px solid var(--line);border-radius:12px;font:inherit"><input type="email" name="email" placeholder="Je e-mailadres" required style="padding:12px;border:1px solid var(--line);border-radius:12px;font:inherit"><textarea name="bericht" rows="6" placeholder="Je bericht" required style="padding:12px;border:1px solid var(--line);border-radius:12px;font:inherit"></textarea><button class="btn btn-brand" type="submit">Versturen</button></form>
<p style="margin-top:20px">Mailen kan ook: <a href="mailto:hallo@watkoopik.nl">hallo@watkoopik.nl</a>. We reageren binnen twee werkdagen.</p></div>''' % SITE, "Neem contact op met de redactie van watkoopik.nl.")

simple("bedankt.html", "Bedankt", '<div class="art-head prose"><h1>Bedankt!</h1><p class="intro">We hebben je bericht ontvangen. <a href="index.html">Terug naar de homepage</a>.</p></div>', "Bedankt voor je bericht.")

simple("disclaimer.html", "Affiliate-disclaimer", '''<div class="art-head prose"><h1>Affiliate-disclaimer</h1></div><div class="prose">
<p>watkoopik.nl neemt deel aan partnerprogramma's van webwinkels, waaronder het bol Partnerprogramma. Dat betekent dat wij een vergoeding kunnen ontvangen wanneer je via een link op onze website een aankoop doet. De prijs die jij betaalt verandert hierdoor niet.</p>
<p>Links naar winkels zijn herkenbaar aan de knoppen "Bekijk bij bol" en "Bekijk prijs". Deze vergoeding financiert het onderhoud van de website en het bijwerken van onze gidsen. Ze heeft geen invloed op de volgorde van onze lijsten of op ons oordeel over producten. Merken en winkels kunnen geen plek in een lijst kopen.</p>
<p>Prijzen op onze site zijn indicatief en gebaseerd op de laatste controle, waarvan de datum bij elke gids staat. De actuele prijs in de winkel is leidend. Productnamen, merknamen en beeldmerken zijn eigendom van de betreffende fabrikanten.</p></div>''', "Hoe watkoopik.nl geld verdient met affiliate links en wat dat voor jou betekent.")

simple("privacy.html", "Privacy & cookies", '''<div class="art-head prose"><h1>Privacy &amp; cookies</h1></div><div class="prose">
<h2>Welke gegevens verwerken wij</h2><p>Bezoek je watkoopik.nl, dan verwerken wij alleen de gegevens die technisch nodig zijn om de site te tonen. Vul je het contactformulier of de nieuwsbriefaanmelding in, dan gebruiken wij je naam en e-mailadres uitsluitend om op je bericht te reageren of om je de nieuwsbrief te sturen. Je kunt je op elk moment afmelden via de link in elke mail.</p>
<h2>Cookies</h2><p>Wij plaatsen zelf geen volgcookies. Onze site gebruikt alleen functionele opslag in je browser, bijvoorbeeld om te onthouden welke onderdelen je hebt bekeken. Klik je door naar een winkel, dan kan die winkel een cookie plaatsen om de aankoop aan onze site te koppelen. Daarvoor geldt het privacybeleid van die winkel.</p>
<h2>Je rechten</h2><p>Je hebt het recht je gegevens in te zien, te laten corrigeren of te laten verwijderen. Stuur een mail naar <a href="mailto:hallo@watkoopik.nl">hallo@watkoopik.nl</a>.</p>
<h2>Verantwoordelijke</h2><p>watkoopik.nl is onderdeel van 4NEON, Nederland. Dit beleid is voor het laatst bijgewerkt op %s.</p></div>''' % TODAY.strftime("%d-%m-%Y"), "Privacy- en cookiebeleid van watkoopik.nl.")

simple("404.html", "Pagina niet gevonden", '<div class="art-head prose"><h1>Deze pagina bestaat niet (meer)</h1><p class="intro">Misschien is de gids verhuisd. <a href="gidsen.html">Bekijk alle gidsen</a> of zoek hieronder.</p><div class="search-wrap" style="max-width:520px"><label class="search"><span>🔍</span><input type="search" placeholder="Zoek een product…" data-search></label><div class="search-results"></div></div></div>', "Pagina niet gevonden.")

# ---------- assets ----------
wr("style.css", rd("style.css")); wr("app.js", rd("app.js"))
wr("favicon.svg", LOGO.FAVICON)
wr("stats.html", '<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=https://cloud.umami.is/share/sSKhb6j4KMk4E28R/watkoopik.nl"><title>Statistieken</title></head><body><a href="https://cloud.umami.is/share/sSKhb6j4KMk4E28R/watkoopik.nl">Naar het dashboard</a></body></html>')
wr("CNAME", "watkoopik.nl\n"); wr(".nojekyll", "")
wr("robots.txt", "User-agent: *\nAllow: /\nDisallow: /stats.html\nSitemap: %s/sitemap.xml\n" % SITE)
urls = ["", "gidsen.html", "zo-kiezen-wij.html", "over-ons.html", "contact.html", "disclaimer.html", "privacy.html"] + ["categorie/%s.html" % k for k in CATS if by_cat.get(k)] + [g["url"] for g in guides]
wr("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (SITE, u, TODAY.isoformat()) for u in urls) + "</urlset>\n")
wr("search.json", json.dumps([{"t": g["title"], "u": g["url"], "c": CATS[g["cat"]][0], "k": " ".join([g["query"], g["short"]] + g.get("keywords", []) + ["%s %s" % (p["brand"], p["name"]) for p in g["products"]])} for g in guides], ensure_ascii=False))
print("OK: %d gidsen, %d producten, %d pagina's" % (len(guides), sum(len(g["products"]) for g in guides), len(urls)))
