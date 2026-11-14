# -*- coding: utf-8 -*-
"""watkoopik.nl: top 10-koopgidsen met bewegende vormgeving (GSAP + Lenis + WebGL-achtergrond).
Inhoud komt uit data/*.json. Gebruik: python3 build.py (of ./deploy.sh "bericht").
Vorige versie van de bouwmotor: build_v1.py (niet meer gebruikt).
Copyregel: geen em/en-dashes, geen ", en"."""
import os, re, sys, json, subprocess, hashlib, glob, html, datetime, urllib.parse

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
# versie van css/js = inhoudshash (12 nov 2026): verandert alleen als de bestanden echt wijzigen, zodat Googlebot ze niet bij elke deploy opnieuw ophaalt
ASSET_V = hashlib.md5(b"".join(open(os.path.join(ROOT, "_src", n), "rb").read() for n in ("style.css", "light.css", "green.css", "app.js"))).hexdigest()[:10]
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
# A/B-test N5 (hefboom C1, sinds 5 nov 2026): op de helft van de gidsen staat de actuele prijs in de bol-knop.
# Verdeling vast op slug (md5 even = "prijs", oneven = "controle"); alleen op gidspagina-plekken, Umami-eigenschap "variant".
AB_PLEKKEN = ("kaart", "podium", "tabel", "eindoordeel", "sticky")
def ab_variant(slug):
    return "prijs" if int(hashlib.md5(slug.encode()).hexdigest(), 16) % 2 == 0 else "controle"
def shop_a(p, g, cls="btn btn-buy magnet", plek="kaart"):
    label = "Bekijk actuele prijs bij bol" if plek == "kaart" else "Bekijk bij bol"
    var_attr = ""
    if plek in AB_PLEKKEN:
        var = ab_variant(g["slug"])
        var_attr = ' data-umami-event-variant="%s"' % var
        pr = p.get("price")
        if var == "prijs" and isinstance(pr, (int, float)) and pr > 0:
            label = "Bekijk bij bol · %s" % eur(pr)
    return '<a class="%s" href="%s" rel="sponsored nofollow noopener" target="_blank" data-umami-event="bol-klik" data-umami-event-gids="%s" data-umami-event-product="%s" data-umami-event-positie="%s" data-umami-event-plek="%s" data-umami-event-tekst="%s"%s>%s <span class="arr">→</span></a>' % (
        cls, shop_link(p), g["slug"], e("%s %s" % (p["brand"], p["name"])), p.get("rank", ""), plek, "prijs" if plek == "kaart" else "standaard", var_attr, label)

# Amazon als tweede winkel (sinds 30 okt 2026): amazon.com-zoeklink met tag watkoopik-20; Amazon Global Earning stuurt
# Nederlandse bezoekers automatisch door naar amazon.nl met dezelfde tag. Bol blijft de hoofdknop.
AMZ_TAG = "watkoopik-20"
def amazon_link(p):
    q = p.get("search") or "%s %s" % (p["brand"], p["name"])
    return "https://www.amazon.com/s?k=%s&tag=%s" % (urllib.parse.quote_plus(q), AMZ_TAG)
def amazon_a(p, g, plek="kaart"):
    return '<a class="amz-link" href="%s" rel="sponsored nofollow noopener" target="_blank" data-umami-event="amazon-klik" data-umami-event-gids="%s" data-umami-event-product="%s" data-umami-event-positie="%s" data-umami-event-plek="%s">of bekijk bij Amazon</a>' % (
        e(amazon_link(p)), g["slug"], e("%s %s" % (p["brand"], p["name"])), p.get("rank", ""), plek)

STAR = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.7.8-4.9 4.6 1.3 6.6L12 17.3l-6 3.3 1.3-6.6L2.4 9.4l6.7-.8z" fill="%s"/></svg>'
def own_block(g):
    """Optioneel blok "Ons eigen merk" boven het podium (veld eigen_merk in de gidsdata). Staat los van de top 10 en is altijd als eigen merk gemarkeerd."""
    o = g.get("eigen_merk")
    if not o: return ""
    pts = "".join("<li>%s</li>" % e(x) for x in o.get("punten", []))
    return '''<div class="own"><img src="%s" alt="%s" loading="lazy"><div class="own-body"><span class="own-lbl">Ons eigen merk</span><h2>%s</h2><p>%s</p><ul>%s</ul><div class="own-buy"><b>%s</b><a class="btn btn-buy" href="%s" target="_blank" rel="noopener" data-umami-event="eigen-merk-klik" data-umami-event-gids="%s">%s <span class="arr">→</span></a></div><p class="own-disc">%s is het eigen merk van de makers van watkoopik. Dit blok staat los van de onafhankelijke top 10 hieronder en daar verdienen wij direct aan.</p></div></div>''' % (
        e(o["image"]), e(o["name"]), e(o["name"]), e(o["text"]), pts, eur(o["price"]), e(o["url"]), e(g["slug"]), e(o.get("knop", "Bekijk bij " + o["merk"])), e(o["merk"]))
def own_compact(g):
    """Compacte variant (eigen_merk.compact): 1 regel met foto, 1 voordeel, prijs en knop; staat onder het podium als eigen_merk.plek = onder."""
    o = g["eigen_merk"]
    return '<div class="own own-c"><img src="%s" alt="%s" loading="lazy"><div class="own-body"><span class="own-lbl">Ons eigen merk</span> <b class="own-n">%s</b><p>%s</p><p class="own-disc">Eigen merk van de makers van watkoopik, los van de onafhankelijke top 10.</p></div><a class="btn btn-buy" href="%s" target="_blank" rel="noopener" data-umami-event="eigen-merk-klik" data-umami-event-gids="%s" data-umami-event-variant="compact">%s · %s <span class="arr">→</span></a></div>' % (
        e(o["image"]), e(o["name"]), e(o["name"]), e(o.get("kort") or o["text"]), e(o["url"]), e(g["slug"]), e(o.get("knop", "Bekijk " + o["merk"])), eur_n(o["price"]))
def own_pos(g, plek):
    o = g.get("eigen_merk")
    # eigen_merk.pauze (tekst met datum en reden, bijv. uitverkocht): blok niet tonen, de waarde blijft in de data staan
    if not o or o.get("pauze") or o.get("plek", "boven") != plek: return ""
    return own_compact(g) if o.get("compact") else own_block(g)


def chk_date(p, g):
    """Datum van de laatste prijscontrole: synced uit bol_sync, anders de gidsdatum."""
    return nldate(p.get("synced") or g.get("updated", TODAY.isoformat()))
def chk_html(p, g, short=False):
    d = chk_date(p, g)
    if short: d = " ".join(d.split()[:2])[:6].rstrip()
    return '<small class="chk">%s %s</small>' % ("gecontroleerd" if short else "Prijs gecontroleerd op", e(d))

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
    "cadeaus": ("Cadeaus", "Cadeau-ideeën voor Sinterklaas, Kerst en verjaardagen"),
}
# Intro per categoriehub (80 tot 120 woorden, sinds 24 okt 2026) voor betere indexering van de hubpagina's
CAT_INTRO = {
"elektronica": "Een nieuwe tv, koptelefoon of smartwatch koop je niet elk jaar, dus wil je in een keer goed kiezen. In deze categorie vind je onze top 10's voor televisies in elk formaat, van 32 tot 75 inch, plus OLED en QLED naast elkaar. Daarnaast vergelijken we oordopjes, koptelefoons, soundbars, tablets, e-readers, dashcams en videodeurbellen. Per gids zie je meteen welk model de beste keuze is, welke de slimste koop is en welke premium optie het geld waard is. Specificaties zoals helderheid, accuduur en ruisonderdrukking zetten we in een tabel, zodat je in een paar minuten ziet waar de echte verschillen zitten.",
"keuken": "In de keuken bepaalt een goed apparaat hoeveel plezier je elke dag hebt van koken, bakken en koffie zetten. Hier staan al onze top 10's voor keukenapparaten: airfryers in elk formaat, volautomatische koffiemachines, espressomachines, blenders, keukenmachines, magnetrons en meer. We vergelijken inhoud, vermogen, bediening, schoonmaakgemak en wat duizenden kopers na maanden gebruik melden. Zo zie je snel of een duurder model echt beter is of vooral mooier oogt. Elke gids heeft een duidelijke winnaar, een slimste koop voor een kleiner budget en een koopgids met de vragen die je jezelf vooraf moet stellen.",
"wonen": "Comfort in huis draait om warmte, frisse lucht en een fijne sfeer. In deze categorie vergelijken we elektrische kachels, infraroodpanelen, luchtreinigers voor allergie, luchtontvochtigers, ventilatoren, slimme thermostaten, banken, bureaustoelen en zit-sta-bureaus. Juist nu het stookseizoen begint, letten we extra op verbruik in watt, geluid in decibel en de kosten per maand. Bij luchtreinigers kijken we naar het HEPA-filter, de CADR-waarde en de prijs van vervangfilters. Elke top 10 begint met drie winnaars en eindigt met een koopgids, zodat je weet welk apparaat bij jouw ruimte en budget past.",
"huishouden": "Huishoudelijke apparaten moeten vooral doen wat ze beloven, jaar na jaar. Hier vind je onze top 10's voor stofzuigers met en zonder zak, steelstofzuigers, robotstofzuigers, modellen voor huisdierhaar, wasmachines, drogers, strijkijzers en stoomreinigers. We vergelijken zuigkracht, accuduur, filter, geluid en onderhoudskosten. Ook lezen we wat kopers na maanden gebruik melden over storingen en service. Heb je een hond of kat, dan zie je meteen welke modellen haar uit tapijt en banken halen zonder te verstoppen. Per gids staan de beste keuze, de slimste koop en de premium optie bovenaan.",
"slapen": "Een derde van je leven lig je in bed, dus een goed matras, kussen of dekbed maakt echt verschil. In deze categorie vergelijken we matrassen, ook voor rugklachten, hoofdkussens voor nekklachten, dekbedden voor elk seizoen, boxsprings, elektrische dekens, verzwaringsdekens en oordopjes om te slapen. We kijken naar hardheid, materiaal, ventilatie, proefslaapperiode en wat duizenden slapers na een paar weken melden. Zo zie je of een duur matras echt beter ligt of vooral een sterk merk heeft. Elke gids sluit af met een koopgids en antwoorden op de vragen die mensen het vaakst stellen.",
"verzorging": "Voor verzorgingsproducten tellen kleine details: hoe glad een scheerapparaat scheert, hoe lang de accu meegaat en hoe makkelijk je hem schoonmaakt. In deze categorie vergelijken we föhns, stijltangen, krultangen, elektrische tandenborstels, scheerapparaten, baardtrimmers, tondeuses, ladyshaves en epilators. Per product zetten we de specificaties naast elkaar en vatten we samen wat kopers na weken gebruik vertellen over huidirritatie, geluid en levensduur. Zo zie je snel welk model past bij jouw haar, huid en budget. Elke top 10 heeft een duidelijke winnaar, een slimste koop en een premium keuze.",
"klussen": "Goed gereedschap scheelt tijd, frustratie en soms een bezoek aan de huisarts. In deze categorie vind je onze top 10's voor accuboormachines, ook voor beginners, hogedrukreinigers, grasmaaiers, robotmaaiers, heggenscharen, bladblazers, barbecues en terrasverwarmers. We vergelijken accuplatform, vermogen, gewicht, geluid en de prijs van extra accu's, want dat bepaalt vaak de echte kosten. Heb je al accu's van een merk, dan zie je meteen welke machines daarop passen. Per gids staan de beste keuze, de slimste koop en de premium optie bovenaan, gevolgd door een koopgids voor klussers en tuinliefhebbers.",
"sport": "Thuis sporten werkt alleen als het apparaat stevig staat, stil genoeg is en past in je ruimte. In deze categorie vergelijken we hometrainers, ook compacte modellen, loopbanden, loopbanden voor onder het bureau, massageguns, sporthorloges, sportoordopjes en elektrische fietsen. We letten op maximale belasting, weerstandsniveaus, geluid, inklapbaarheid en wat sporters na maanden gebruik melden. Zo voorkom je dat een dure aankoop als kapstok in de hoek eindigt. Elke top 10 begint met drie winnaars en eindigt met een koopgids die helpt kiezen op basis van jouw doel en budget.",
"computer": "Een laptop of monitor gebruik je elke dag, dus de juiste keuze scheelt jarenlang ergernis. Hier staan onze top 10's voor laptops voor studenten, thuiswerken en ouderen, MacBooks, gaming laptops, all-in-one pc's en monitoren voor werk en ontspanning. We vergelijken processor, werkgeheugen, opslag, schermkwaliteit, gewicht en accuduur. Die cijfers vertalen we naar wat jij er in de praktijk aan hebt. Zo zie je of je voor jouw gebruik echt een duurder model nodig hebt. Elke gids heeft een duidelijke winnaar, een slimste koop en een premium keuze, plus een koopgids zonder vakjargon.",
"telefoon": "Een smartphone gaat al snel drie tot vijf jaar mee, dus updates en accuduur wegen zwaar. In deze categorie vergelijken we smartphones in elke prijsklasse, iPhones, Samsung-toestellen, smartwatches voor ouderen en bluetooth-trackers. We kijken naar camera, schermkwaliteit, opslag, accuduur en hoe lang de fabrikant software-updates belooft. Zo zie je of een toptoestel het meerbedrag waard is of dat een middenklasser voor jou genoeg is. Elke top 10 begint met de beste keuze, de slimste koop en de premium optie, gevolgd door een vergelijkingstabel en een koopgids.",
"gaming": "Bij gaming bepalen details als verversingssnelheid, reactietijd en comfort hoe goed een spelsessie voelt. In deze categorie vergelijken we gaming monitoren, gaming headsets, gaming stoelen, gaming pc's en de PlayStation 5. We zetten specificaties zoals hertz, paneeltype, latency en verstelbaarheid naast elkaar en vatten samen wat gamers na weken gebruik melden. Zo zie je of je het verschil van een duurder model echt merkt of vooral betaalt voor verlichting. Elke top 10 begint met drie duidelijke winnaars en eindigt met een koopgids, zodat je de juiste keuze maakt voor jouw console of pc.",
"cadeaus": "Een cadeau zoeken voor Sinterklaas, Kerst of een verjaardag kost vaak meer tijd dan je wilt. Daarom maken we cadeaugidsen op dezelfde manier als onze andere top 10's: per lijst tien echte producten die je nu bij bol kunt bestellen, met prijs, plus- en minpunten en voor wie het cadeau geschikt is. Je vindt lijsten per budget, zoals cadeaus voor hem of haar onder 50 euro. Ook zijn er lijsten per type ontvanger, zoals thuiswerkers, koks en ouders. Rond Black Friday op 27 november houden we de prijzen extra scherp in de gaten. Echte prijsdalingen zie je op onze pagina met aanbiedingen.",
"kind": "Voor je kind wil je spullen die veilig zijn, lang meegaan en het dagelijks leven makkelijker maken. In deze categorie vergelijken we kinderwagens, autostoelen, babyfoons en flessenwarmers. We letten op veiligheidsnormen zoals i-Size, gewicht, inklapmaat, bereik en hoe makkelijk je iets schoonmaakt. Ook lezen we wat ouders na maanden gebruik melden. Zo zie je snel welk model past bij jouw auto, woning en budget. Elke top 10 begint met de beste keuze, de slimste koop en de premium optie, gevolgd door een vergelijkingstabel en een koopgids met de vragen die nieuwe ouders het vaakst stellen.",
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
    "cadeaus": '<rect x="3" y="8" width="18" height="13" rx="1.5"/><path d="M3 12h18"/><path d="M12 8v13"/><path d="M12 8c-2-4-6-4-6-1s6 1 6 1c2-4 6-4 6-1s-6 1-6 1"/>',
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
# Snoeien (N32, 13 nov 2026): gidsen met "noindex": true in de data krijgen noindex,follow en staan niet in sitemap.xml; ze blijven gewoon bestaan en gelinkt (tools/snoei.py)
NOINDEX = {g["url"] for g in guides if g.get("noindex")}
# AI1 (14 nov 2026): gesnoeide gidsen zijn alleen voor Google noindex (meta googlebot). Bing en daarmee ChatGPT
# (78% van het bezoek) mogen ze blijven opnemen; ze blijven wel uit sitemap.xml. Google volgt de strengste van robots + googlebot.
def robots_meta(path):
    if PREVIEW: return "noindex,follow"
    if path in NOINDEX: return 'index,follow,max-image-preview:large"><meta name="googlebot" content="noindex,follow'
    return "index,follow,max-image-preview:large"
N_PROD = sum(len(g["products"]) for g in guides)
N_REV = sum(int(re.sub(r"\D", "", str(g.get("reviews_total", "0"))) or 0) for g in guides)
def win(g): return g["products"][0]
def img_of(p, cls=""):
    return ('<img src="%s" alt="%s %s" loading="lazy"%s>' % (e(p["image"]), e(p["brand"]), e(p["name"]), (' class="%s"' % cls) if cls else "")) if p.get("image") else '<span class="ph" aria-hidden="true">%s</span>' % e(p.get("_ico", "🛒"))
for g in guides:
    for p in g["products"]: p["_ico"] = g["ico"]

# ---------- prijsdalingen (sinds 24 okt 2026) ----------
# Alleen echt gemeten bol-prijzen uit bol_sync (veld ph = dagprijzen). Referentie = de LAAGSTE gemeten prijs
# van de 30 dagen voordat de huidige prijs inging (sinds 12 nov 2026, groeimotor N28; was de mediaan). Met de mediaan
# telden jojoprijzen mee (Eufy Omni C20 "34% lager" terwijl hij een week eerder al goedkoper was). Zelfde maat als
# watkoopik-social/deals.py en de Europese regel voor van-prijzen. Deal = minstens 10% lager. Dalingen van meer dan 60% zijn
# vrijwel altijd een andere verkoper of een onderdeel en tellen niet mee.
def deal_of(p):
    ph = p.get("ph") or {}
    if len(ph) < 3 or not p.get("price"): return None
    days = sorted(ph); cur = p["price"]
    i = len(days)
    while i > 0 and abs(ph[days[i - 1]] - cur) < 0.01: i -= 1
    since = days[i] if i < len(days) else days[-1]
    start = (datetime.date.fromisoformat(since) - datetime.timedelta(days=30)).isoformat()
    prev = sorted(ph[d] for d in days[:i] if d >= start)
    if len(prev) < 2: return None
    ref = prev[0]
    drop = 1 - cur / ref
    if drop < 0.10 or drop > 0.60: return None
    if since < (TODAY - datetime.timedelta(days=21)).isoformat(): return None  # na drie weken is het de gewone prijs
    return {"ref": ref, "drop": drop, "since": since, "low": min(ph.values()), "first": days[0]}
# ---------- prijsverloop per product (sinds 4 nov 2026, groeimotor A2) ----------
# Eigen dagelijkse bol-metingen (ph) zichtbaar maken: sparkline + laagste/hoogste/gemiddelde per product, een tabel per gids
# en een FAQ over de nr. 1. Alleen bij minstens 5 meetdagen; niets geschat of aangevuld.
def hist_of(p):
    ph = p.get("ph") or {}
    if len(ph) < 5 or not p.get("price"): return None
    days = sorted(ph); vals = [ph[d] for d in days]
    if days[-1] != TODAY.isoformat() and abs(vals[-1] - p["price"]) >= 0.01: days.append(TODAY.isoformat()); vals.append(p["price"])
    avg = sum(vals) / len(vals)
    return {"days": days, "vals": vals, "low": min(vals), "high": max(vals), "avg": avg, "n": len(vals), "first": days[0], "rel": p["price"] / avg - 1,
            "low_day": days[max(i for i, v in enumerate(vals) if v == min(vals))]}
def gmod(g):  # echte wijzigingsdatum: gidsdatum of de laatste dag dat een podiumprijs (top 3) 3%+ veranderde (zichtbaar op de pagina)
    d = g.get("updated", TODAY.isoformat())
    for p in sorted(g["products"], key=lambda p: p.get("rank", 99))[:3]:
        ph = p.get("ph") or {}; days = sorted(ph)
        for a, b in zip(days, days[1:]):
            if ph[a] and abs(ph[b] - ph[a]) / ph[a] >= 0.03: d = max(d, b)
    return min(d, TODAY.isoformat())
def spark(h, w=132, ht=34):
    lo, hi = h["low"], h["high"]; rng = (hi - lo) or 1
    d0 = datetime.date.fromisoformat(h["first"]); span = max(1, (datetime.date.fromisoformat(h["days"][-1]) - d0).days)
    pts = ["%.1f,%.1f" % (3 + (w - 6) * (datetime.date.fromisoformat(d) - d0).days / span, 4 + (ht - 8) * (1 - (v - lo) / rng)) for d, v in zip(h["days"], h["vals"])]
    return '<svg class="spark" viewBox="0 0 %d %d" width="%d" height="%d" aria-hidden="true"><polyline points="%s" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/><circle cx="%s" cy="%s" r="3" fill="currentColor"/></svg>' % (w, ht, w, ht, " ".join(pts), pts[-1].split(",")[0], pts[-1].split(",")[1])
def rel_txt(r):
    if abs(r) < 0.015: return "rond het gemiddelde"
    return "%d%% %s het gemiddelde" % (round(abs(r) * 100), "onder" if r < 0 else "boven")
def hist_box(p):
    h = hist_of(p)
    if not h: return ""
    if h["high"] - h["low"] < 0.01: txt = "Op alle %d meetdagen sinds %s kostte hij %s bij bol: de prijs is stabiel." % (h["n"], nldate(h["first"]), eur(p["price"]))
    else: txt = "Gemeten op %d dagen sinds %s: laagste %s, hoogste %s, gemiddeld %s. Nu %s, dat is %s." % (h["n"], nldate(h["first"]), eur(h["low"]), eur(h["high"]), eur(round(h["avg"], 2)), eur(p["price"]), rel_txt(h["rel"]))
    tag = ' <span class="ph-tag">laagste gemeten prijs</span>' if p["price"] <= h["low"] + 0.01 and h["high"] - h["low"] >= 0.01 else ""
    pu = prijs_url(p)
    more = (' <a href="../%s" data-umami-event="prijspagina-link">Alle gemeten prijzen</a>' % pu) if pu else ""
    return '<div class="ph-box%s">%s<div><b>Prijsverloop bij bol</b>%s<p>%s%s</p></div></div>' % (" low" if tag else "", spark(h), tag, e(txt), more)
_HS = {}
def hist_section(g):
    if g["slug"] in _HS: return _HS[g["slug"]]
    rows, hs = [], []
    for p in g["products"]:
        h = hist_of(p)
        if not h: continue
        hs.append((p, h))
        rows.append('<tr><td><span class="rk">%d</span></td><td class="nm">%s %s</td><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td class="sp">%s</td></tr>' % (
            p["rank"], e(p["brand"]), e(p["name"]), eur(p["price"]), eur(h["low"]), eur(h["high"]), e(rel_txt(h["rel"])), spark(h, 96, 26)))
    if len(hs) < 3: _HS[g["slug"]] = ""; return ""
    first = min(h["first"] for p, h in hs)
    under = [p for p, h in hs if h["rel"] <= -0.015]
    lowest = [p for p, h in hs if p["price"] <= h["low"] + 0.01 and h["high"] - h["low"] >= 0.01]
    big = max(hs, key=lambda x: (x[1]["high"] - x[1]["low"]) / x[1]["high"])
    s = "Wij noteren elke dag de bol-prijs van deze %d modellen, sinds %s. " % (len(hs), nldate(first))
    s += ("%d van de %d staan nu onder hun gemiddelde prijs" % (len(under), len(hs))) if under else "Geen enkel model staat nu duidelijk onder zijn gemiddelde prijs"
    s += (" en %d kost%s nu het minst sinds we meten. " % (len(lowest), "" if len(lowest) == 1 else "en")) if lowest else ". "
    sw = (big[1]["high"] - big[1]["low"]) / big[1]["high"]
    if sw >= 0.05: s += "De grootste schommeling zagen we bij de %s %s: tussen %s en %s." % (big[0]["brand"], big[0]["name"], eur(big[1]["low"]), eur(big[1]["high"]))
    else: s += "De prijzen in deze gids zijn rustig: geen enkel model schommelde meer dan 5%."
    html = ('<div class="phist rv" id="prijsverloop"><h2>Prijsverloop: zo bewogen de prijzen bij bol</h2><p>%s Geen adviesprijzen: alleen wat wij zelf hebben gemeten. '
            'Echte prijsdalingen van 10%% of meer staan op <a href="../aanbiedingen/">onze aanbiedingenpagina</a>.' + BF_HINT + '</p>\n'
            '<div class="tbl"><table><thead><tr><th>#</th><th>Model</th><th>Nu</th><th>Laagste</th><th>Hoogste</th><th>Nu t.o.v. gemiddeld</th><th class="sp"><span class="sr">Verloop</span></th></tr></thead><tbody>%s</tbody></table></div></div>\n') % (e(s), "".join(rows))
    _HS[g["slug"]] = html
    return html
# Black Friday-check in elke prijsverlooptabel tot en met 1 dec (groeimotor E22): interne links naar de datapagina voor de pers
BF_HINT = (' Op Black Friday (27 november) zie je hier meteen of een korting echt is. <a href="../black-friday/echte-kortingen-2026.html" data-umami-event="bf-link">Zoveel kortingen zijn nu al echt: onze eigen metingen</a>.') if TODAY <= datetime.date(2026, 12, 1) else ""
def hist_faq(g):
    p = g["products"][0]; h = hist_of(p)
    if not h or h["n"] < 7: return None
    q = "Is de %s %s nu goedkoop?" % (p["brand"], p["name"])
    if h["high"] - h["low"] < 0.01: a = "De prijs is stabiel: op alle %d dagen dat wij hem sinds %s bij bol maten kostte hij %s. Wachten op een lagere prijs levert bij dit model tot nu toe niets op." % (h["n"], nldate(h["first"]), eur(p["price"]))
    else: a = "Hij kost nu %s bij bol. Sinds %s maten wij op %d dagen een laagste prijs van %s (op %s) en een hoogste van %s. De huidige prijs ligt %s van %s." % (eur(p["price"]), nldate(h["first"]), h["n"], eur(h["low"]), nldate(h["low_day"]), eur(h["high"]), rel_txt(h["rel"]), eur(round(h["avg"], 2)))
    return {"q": q, "a": a}

# ---------- logboek per gids (groeimotor N32 stap 3, 13 nov 2026) ----------
# Wat er sinds de start in de lijst veranderde (tools/logboek.py leest de git-geschiedenis van data/<slug>.json, _src/logboek.json)
# en hoe de prijs van de top 3 bewoog (ph). Alleen feiten uit eigen administratie en metingen; een reden staat er alleen bij
# als die vastligt. Eerst op de 20 best verdienende indexeerbare gidsen (_src/logboek_gidsen.json).
try:
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "logboek.py"), "--stil"], timeout=180)
    LOGBOEK = json.load(open(os.path.join(ROOT, "_src", "logboek.json"), encoding="utf-8"))
except Exception: LOGBOEK = {}
def dagmaand(iso):
    d = datetime.date.fromisoformat(iso); return "%d %s" % (d.day, MONTHS[d.month])
def _opsom(xs): return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " en " + xs[-1]
def logboek_html(g):
    lb = LOGBOEK.get(g["slug"])
    if not lb or g.get("noindex"): return ""
    pr = []
    for p in sorted(g["products"], key=lambda p: p["rank"])[:3]:
        h = hist_of(p)
        if not h: continue
        nm = "<b>Nr. %d · %s %s</b>" % (p["rank"], e(p["brand"]), e(p["name"]))
        if h["high"] - h["low"] < 0.01:
            pr.append("<li>%s: op alle %d meetdagen sinds %s kostte hij %s.</li>" % (nm, h["n"], dagmaand(h["first"]), eur(p["price"])))
            continue
        hi_day = h["days"][max(i for i, v in enumerate(h["vals"]) if v == h["high"])]
        n_ch = sum(1 for a, b in zip(h["vals"], h["vals"][1:]) if abs(a - b) >= 0.01)
        pr.append("<li>%s: eerste meting %s op %s, laagste %s op %s, hoogste %s op %s, nu %s. De prijs veranderde %d keer in %d meetdagen.</li>" % (
            nm, eur(h["vals"][0]), dagmaand(h["first"]), eur(h["low"]), dagmaand(h["low_day"]), eur(h["high"]), dagmaand(hi_day), eur(p["price"]), n_ch, h["n"]))
    days = {}
    for ev in lb.get("events", []): days.setdefault(ev["d"], []).append(ev)
    ch = []
    for d in sorted(days, reverse=True):
        evs = days[d]
        if all(ev.get("paar") for ev in evs):
            zinnen = ["%s ging eruit, %s kwam erin op plek %d.%s" % (e(ev["uit"]), e(ev["in"]), ev["plek"], (" Reden: %s." % e(ev["waarom"])) if ev.get("waarom") else "") for ev in evs]
        else:
            w = sorted({ev["waarom"] for ev in evs if ev.get("waarom")})
            zinnen = ["Uit de lijst: %s. Nieuw in de lijst: %s.%s" % (e(_opsom([ev["uit"] for ev in evs])), e(_opsom([ev["in"] for ev in evs])), (" Reden: %s." % e(w[0])) if len(w) == 1 and all(ev.get("waarom") for ev in evs) else "")]
        ch.append("<li><b>%s</b>: %s</li>" % (dagmaand(d), " ".join(zinnen)))
    n_ev = len(lb.get("events", []))
    if ch: wis = "<p>Sinds de start wisselden wij %d keer een product in deze top %d. De nieuwste wijziging staat bovenaan.</p><ul>%s</ul>" % (n_ev, lb.get("n", 10), "".join(ch))
    else: wis = "<p>Sinds de start op %s staan dezelfde %d producten in de lijst. De prijzen meten wij elke dag opnieuw.</p>" % (nldate(lb["start"]), lb.get("n", 10))
    prijs = ("<h3>De prijs van de top 3 bij bol</h3><ul>%s</ul>" % "".join(pr)) if pr else ""
    return ('<div class="guide logb rv" id="logboek"><h2>Logboek van deze gids</h2><p>Deze gids staat sinds %s online. Hier lees je wat wij sindsdien in de lijst hebben aangepast en hoe de prijs van de top 3 bewoog. '
            'Het komt uit onze eigen administratie en onze dagelijkse prijsmetingen bij bol, niet van een fabrikant of winkel.</p>%s<h3>Wijzigingen in de lijst</h3>%s</div>\n') % (nldate(lb["start"]), prijs, wis)

# ---------- populair bij bol (groeimotor S5, 9 nov 2026) ----------
# Plek van onze keuzes in bol's eigen sortering 'populariteit' op de bol-zoekterm van de gids (tools/bol_populair.py,
# _src/bolpopulair.json). Alleen echte plekken uit de top 100; geen data = geen blok.
try: BOLPOP = json.load(open(os.path.join(ROOT, "_src", "bolpopulair.json"), encoding="utf-8"))
except Exception: BOLPOP = {}
def pop_of(g):
    x = BOLPOP.get(g["slug"]) or {}
    if x.get("query") != g["query"]: return None, []
    pl = x.get("plek", {})
    return x, sorted([p for p in g["products"] if str(p.get("ean")) in pl], key=lambda p: pl[str(p["ean"])])
def pop_html(g):
    x, ps = pop_of(g)
    if not ps: return ""
    pl = x["plek"]
    rows = "".join('<li><span class="pop-n">%d</span><div><b>%s %s</b><small>Nr. %d in onze top 10 · %s</small></div>%s</li>' % (
        pl[str(p["ean"])], e(p["brand"]), e(p["name"]), p["rank"], eur(p["price"]), shop_a(p, g, "btn btn-buy btn-sm", "populair")) for p in ps[:3])
    return '<div class="pop rv" id="populair"><h2>Populair bij bol</h2><p>Zoek je op bol naar &ldquo;%s&rdquo; en sorteer je op populariteit, dan %s van onze top 10 bij de eerste 100. %s (gemeten op %s).</p><ol>%s</ol><p class="pop-note">Populariteit is de eigen sortering van bol. Dat zegt iets over wat veel mensen kiezen, niet automatisch over wat het beste is: daarvoor is onze ranglijst.</p></div>' % (
        e(x["query"]), "staat 1" if len(ps) == 1 else "staan alle %d" % len(ps) if len(ps) == len(g["products"]) else "staan %d" % len(ps),
        "Dit is het model, met zijn plek in die lijst" if len(ps) == 1 else "Dit zijn ze, met hun plek in die lijst" if len(ps) < 4 else "Dit zijn de hoogste, met hun plek in die lijst", e(nldate(x["datum"])), rows)
def pop_faq(g):
    x, ps = pop_of(g)
    if not ps: return None
    p = ps[0]; pl = x["plek"]
    q = "Welke %s is het populairst bij bol?" % g["query"]
    a = "Van onze top 10 staat de %s %s het hoogst als je op bol zoekt naar \"%s\" en sorteert op populariteit: plek %d (gemeten op %s)." % (p["brand"], p["name"], x["query"], pl[str(p["ean"])], nldate(x["datum"]))
    if len(ps) > 1: a += " Daarna volgt de %s %s op plek %d." % (ps[1]["brand"], ps[1]["name"], pl[str(ps[1]["ean"])])
    a += " In onze eigen ranglijst is de %s %s nr. %d." % (p["brand"], p["name"], p["rank"]) if p["rank"] != 1 else " Dat is ook onze nr. 1."
    return {"q": q, "a": a}

# ---------- prijsverloop-pagina per model (sinds 8 nov 2026, groeimotor N13) ----------
# Pilot: alleen de EAN's in _src/prijspaginas.json (top 3 van de best bezochte gidsen). Pagina = eigen dagmetingen bij bol
# (grafiek + tabel), plek in onze top 10's, kenmerken. Geen meting = geen pagina; niets geschat.
def pslug(p): return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", ("%s %s" % (p["brand"], p["name"])).lower())).strip("-")[:70]
try: _pp_eans = json.load(open(os.path.join(ROOT, "_src", "prijspaginas.json"), encoding="utf-8"))["eans"]
except Exception: _pp_eans = []
PRIJS = {}  # ean -> {"p": product (hoogste plek), "in": [(gids, product)], "slug": ...}
for g in guides:
    for p in g["products"]:
        k = str(p.get("ean") or "")
        if k not in _pp_eans: continue
        x = PRIJS.setdefault(k, {"p": p, "in": []}); x["in"].append((g, p))
        if p["rank"] < x["p"]["rank"]: x["p"] = p
_used = set()
for k in list(PRIJS):
    x = PRIJS[k]
    if not hist_of(x["p"]): del PRIJS[k]; continue
    s = pslug(x["p"]); s = s if s not in _used else "%s-%s" % (s, k[-4:]); _used.add(s); x["slug"] = s
def prijs_url(p):
    x = PRIJS.get(str(p.get("ean") or ""))
    return "prijs/%s.html" % x["slug"] if x else None

DEALS = []
_seen = set()
for g in guides:
    for p in g["products"]:
        d = deal_of(p)
        key = str(p.get("ean") or p["brand"] + p["name"])
        if d and key not in _seen:
            _seen.add(key); DEALS.append((g, p, d))
DEALS.sort(key=lambda x: (-x[2]["drop"], x[1]["rank"]))
# ---------- vergelijkingen X vs Y (sinds 24 okt 2026, vsdata/vs.json) ----------
# Producten worden op EAN gekoppeld: verdwijnt een van beide uit de gids, dan valt de pagina weg in plaats van verouderd te raken.
VS_PAGES = []
_gs = {g["slug"]: g for g in guides}
try: _vs = json.load(open(os.path.join(ROOT, "vsdata", "vs.json"), encoding="utf-8"))
except Exception: _vs = []
for v in _vs:
    g = _gs.get(v["gids"])
    if not g: continue
    pa = next((p for p in g["products"] if str(p.get("ean")) == v["a"]), None)
    pb = next((p for p in g["products"] if str(p.get("ean")) == v["b"]), None)
    if pa and pb:
        VS_PAGES.append(dict(v, g=g, pa=pa, pb=pb, updated=max(g.get("updated", ""), "2026-10-24")))
VS_BY_GUIDE = {}
for v in VS_PAGES: VS_BY_GUIDE.setdefault(v["gids"], []).append(v)
def vs_title(v): return "%s %s vs %s %s" % (v["pa"]["brand"], v["pa"]["name"], v["pb"]["brand"], v["pb"]["name"])

# ---------- productfamilies (sinds 4 nov 2026, _src/clusters.json) ----------
# Gidsen over hetzelfde product linken allemaal naar elkaar: balk onder de kruimels plus een alinea in de koopgids.
# Families met minstens drie gidsen krijgen een overzicht op welke/<key>-kopen.html. Een nieuwe gids valt vanzelf in een
# familie als de slug (zonder "beste-") op het patroon past; de volgorde in clusters.json bepaalt de hoofdfamilie.
CLUSTERS = []
CL_OF = {}  # slug -> families waar de gids in valt, hoofdfamilie eerst
for c in json.load(open(os.path.join(ROOT, "_src", "clusters.json"), encoding="utf-8")):
    rx = re.compile(c["match"])
    ms = [g for g in guides if rx.match(g["slug"][6:])]
    main = next((g for g in ms if g["slug"] == c.get("main")), None)
    c["members"] = ([main] + [g for g in ms if g is not main]) if main else ms
    if len(ms) < 2: continue
    c["hub"] = "welke/%s-kopen.html" % c["key"] if len(ms) >= 3 else None
    CLUSTERS.append(c)
    for g in ms: CL_OF.setdefault(g["slug"], []).append(c)
HUBS = [c for c in CLUSTERS if c["hub"]]
# Zoekterm netjes in een zin (groeimotor 10 nov 2026): 'beste' vooraan en 'kopen' achteraan eraf, het-woorden en meervoud herkennen.
HET_KOP = ("cadeau", "dekbed", "dekbedovertrek", "matras", "bedframe", "droogrek", "fornuis", "hoofdkussen", "scheerapparaat", "strijkijzer", "bureau", "warmtekussen", "massagepistool", "autostoeltje", "paneel", "sporthorloge", "bruiswatertoestel")
def zoekterm(g):
    t = (g.get("seo") or g["query"]).strip()
    if t.lower().startswith("beste "): t = t[6:]
    if t.lower().endswith(" kopen"): t = t[:-6]
    return t
def zoekterm_vorm(t):
    """('Het', 'het', 'is') voor het-woorden, ('De', 'de', 'zijn') voor meervoud, anders ('De', 'de', 'is'). Kijkt naar de woorden voor het eerste voorzetsel."""
    kop = re.split(r" (?:voor|onder|bij|met|zonder|om|of) ", " " + t.lower() + " ")[0].split()
    if any(w.endswith("oordopjes") for w in kop): return "De", "de", "zijn"
    if any(w.endswith(HET_KOP) for w in kop): return "Het", "het", "is"
    return "De", "de", "is"

def cap1(s): return s[:1].upper() + s[1:]
def low1(s):
    w = s.split(" ")[0]
    return s[:1].lower() + s[1:] if w[1:] == w[1:].lower() else s
def welk(c): return "Welk" if c.get("welk") else "Welke"
def hub_q(c): return "%s %s kopen?" % (welk(c), c["enkel"])
def cl_nav(g, root="../"):
    """Balk met alle gidsen uit de hoofdfamilie, de huidige gids gemarkeerd."""
    cs = CL_OF.get(g["slug"])
    if not cs: return ""
    c = cs[0]
    first = ('<a class="cl-all" href="%s%s">Alle %d %s</a>' % (root, c["hub"], len(c["members"]), e(c["meervoud"]))) if c["hub"] else '<span class="cl-all">%s</span>' % e(cap1(c["meervoud"]))
    items = []
    for x in c["members"]:
        if x is g: items.append('<span class="on" aria-current="page">%s</span>' % e(x["short"]))
        else: items.append('<a href="%s%s">%s</a>' % (root, x["url"], e(x["short"])))
    return '<nav class="clnav" aria-label="Alle %s">%s%s</nav>' % (e(c["meervoud"]), first, "".join(items))
def cl_more(g, root="../"):
    """Alinea onder de koopgids met tekstlinks naar de andere gidsen uit de hoofdfamilie."""
    cs = CL_OF.get(g["slug"])
    if not cs: return ""
    c = cs[0]
    links = ['<a href="%s%s">%s</a>' % (root, x["url"], e(low1(x["short"]))) for x in c["members"] if x is not g]
    lst = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " en " + links[-1]
    s = "Verder vergelijken? We hebben ook gidsen voor %s." % lst
    if c["hub"]: s += ' Of bekijk <a href="%s%s">alle %s op een rij</a>.' % (root, c["hub"], e(c["meervoud"]))
    return '<p class="cl-more">%s</p>' % s
def hub_chips(cs, root=""):
    return '<nav class="clnav cl-hubs" aria-label="Overzichten">%s</nav>' % "".join('<a href="%s%s">%s</a>' % (root, c["hub"], e(hub_q(c))) for c in cs) if cs else ""

def deal_row(g, p, d, root):
    return '''<div class="deal rv"><a class="deal-img" href="%s%s#p%d">%s</a><div class="deal-bd"><span class="deal-pct">%d%% lager</span><h3><a href="%s%s#p%d">%s %s</a></h3><small>Nr. %d in <a href="%s%s">%s</a></small>
<div class="deal-pr"><b>%s</b><span>laagste 30 dagen ervoor %s</span></div><small class="chk">Gezakt op %s · laagste gemeten prijs %s sinds %s</small></div><div class="deal-buy">%s</div></div>''' % (
        root, g["url"], p["rank"], img_of(p), round(d["drop"] * 100), root, g["url"], p["rank"], e(p["brand"]), e(p["name"]), p["rank"], root, g["url"], e(g["short"].lower()),
        eur(p["price"]), eur(round(d["ref"], 2)), e(nldate(d["since"])), eur(d["low"]), e(nldate(d["first"])), shop_a(p, g, "btn btn-buy btn-sm", "deals"))

# ---------- chrome ----------
NAV = [("gidsen.html", "Alle gidsen"), ("aanbiedingen/", "Aanbiedingen"), ("cadeaus/", "Cadeaus"), ("keuzehulp.html", "Keuzehulp"), ("slimste-koop.html", "Slimste koop"), ("zo-kiezen-wij.html", "Zo kiezen wij")]

sys.path.insert(0, os.path.join(ROOT, "tools"))
try:
    import og as OG
except Exception:
    OG = None
OG_META_FILE = os.path.join(ROOT, "og", "_meta.json")
try: OG_META = json.load(open(OG_META_FILE))
except Exception: OG_META = {}

def og_img(g, top):
    """Eigen 1200x630 deelkaart per gids; valt terug op de productfoto als PIL ontbreekt.
    Wisselt de nr. 1 (andere foto), dan wordt de kaart opnieuw gemaakt en krijgt de URL een nieuwe ?v= zodat deelplatforms niet het oude beeld tonen."""
    rel = "og/%s.jpg" % g["slug"]
    path = os.path.join(ROOT, rel)
    sig = hashlib.md5((g["title"] + "|" + (top.get("image") or "")).encode("utf-8")).hexdigest()[:8]
    if OG:
        if OG_META.get(g["slug"]) != sig and os.path.exists(path) and g["slug"] in OG_META:
            os.remove(path)
        if not os.path.exists(path):
            try: OG.card(path, g["title"], "Top 10 · %s" % CATS[g["cat"]][0], g.get("color"), top.get("image"))
            except Exception: pass
        if os.path.exists(path) and OG_META.get(g["slug"]) != sig:
            OG_META[g["slug"]] = sig; OG_META["_dirty"] = 1
    return SITE + "/" + rel + "?v=" + OG_META.get(g["slug"], sig) if os.path.exists(path) else top.get("image", "")

def head(title, desc, path, root, extra="", img=""):
    canon = CANON + "/" + path
    return '''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="p:domain_verify" content="08507cf92b51261ab340ae79077e9383">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="%s">
<link rel="canonical" href="%s">
<link rel="alternate" hreflang="nl-NL" href="%s">
<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:type" content="%s"><meta property="og:locale" content="nl_NL"><meta property="og:site_name" content="watkoopik"><meta property="og:url" content="%s">%s
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#07060f">
<link rel="icon" href="%sfavicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%sstyle.css?v=%s">%s
<script>window.ROOT=%s</script>
<script defer src="https://cloud.umami.is/script.js" data-website-id="47030ca7-838e-4840-9d90-0c8b315ba5e8"></script>
<script defer src="https://stats.1v1battles.com/nv.js" data-website-id="03f16402-b724-4d0e-9b85-421af8108d65"></script>
%s
</head>
<body class="%s">
<div class="fx-fallback" aria-hidden="true"></div><canvas id="fx" aria-hidden="true"></canvas><div class="fx-veil" aria-hidden="true"></div><div class="fx-grain" aria-hidden="true"></div><div class="cursor-glow" aria-hidden="true"></div>
<div class="progress" aria-hidden="true"></div>''' % (e(title), e(desc), robots_meta(path), canon, canon, e(title), e(desc), "article" if "/beste/" in canon else "website", canon, (('<meta property="og:image" content="%s">' % e(img)) + ('<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="%s">' % e(title) if "/og/" in img else '')) if img else '', root, root, ASSET_V, "".join('<link rel="stylesheet" href="%s%s.css?v=%s">' % (root, n, ASSET_V) for n in THEME_CSS), json.dumps(root), extra, BODY_CLASS)

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

# Zustersites per land (groeimotor 11 nov 2026, E39): vaste regel onderaan elke pagina, eigen land zonder link.
LANDEN = [("watkoopik.nl", "Nederland", "nl"), ("derkauftipp.de", "Deutschland", "de"), ("lequelprendre.fr", "France", "fr"), ("getthatone.com", "United States", "en-US"), ("getthatone.co.uk", "United Kingdom", "en-GB"), ("checomprare.it", "Italia", "it"), ("cualelijo.es", "España", "es"), ("ktorykupic.pl", "Polska", "pl"), ("qualcompro.com", "Portugal", "pt")]
def landen_regel(eigen):
    return '<div class="fine" style="border-top:0;margin-top:8px;padding-top:0">🌍 ' + " · ".join(n if d == eigen else '<a href="https://%s/" hreflang="%s">%s</a>' % (d, h, n) for d, n, h in LANDEN) + '</div>'

def footer(root):
    pop = "".join('<li><a href="%s%s">%s</a></li>' % (root, g["url"], e(g["short"])) for g in guides[:5])
    pop += '</ul><h4 style="margin-top:18px">Overzichten</h4><ul>' + "".join('<li><a href="%s%s">%s</a></li>' % (root, c["hub"], e(hub_q(c))) for c in sorted(HUBS, key=lambda c: -len(c["members"]))[:8])
    cats = "".join('<li><a href="%scategorie/%s.html">%s</a></li>' % (root, k, v[0]) for k, v in CATS.items() if by_cat.get(k))
    return '''<footer><div class="wrap"><div class="cols">
<div><a class="logo" href="%s">%s<span class="logo-word">wat<b>koop</b>ik</span></a><p style="margin-top:12px;font-size:.92rem">Onafhankelijke top 10-gidsen. Wij vergelijken prijs, specificaties en reviews zodat jij in vijf minuten de juiste keuze maakt.</p></div>
<div><h4>Populair</h4><ul>%s</ul></div>
<div><h4>Categorieën</h4><ul>%s</ul></div>
<div><h4>watkoopik</h4><ul><li><a href="%skeuzehulp.html">Keuzehulp</a></li><li><a href="%sslimste-koop.html">Slimste koop</a></li><li><a href="%szo-kiezen-wij.html">Zo kiezen wij</a></li><li><a href="%sover-ons.html">Over ons</a></li><li><a href="%scontact.html">Contact</a></li><li><a href="%sprivacy.html">Privacy</a></li><li><a href="%sdisclaimer.html">Affiliate-disclaimer</a></li></ul></div>
</div><div class="pref-wrap"><a class="pref-src" href="https://google.com/preferences/source?q=watkoopik.nl" target="_blank" rel="noopener" data-umami-event="preferred-source"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="#4285F4" d="M22.5 12.3c0-.8-.1-1.5-.2-2.3H12v4.3h5.9a5 5 0 0 1-2.2 3.3v2.7h3.6c2.1-1.9 3.2-4.8 3.2-8z"/><path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.6-2.7c-1 .7-2.2 1-3.7 1-2.9 0-5.3-1.9-6.2-4.5H2.1v2.8A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.8 14.1a6.6 6.6 0 0 1 0-4.2V7.1H2.1a11 11 0 0 0 0 9.8z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3 .6 4.2 1.6l3.1-3.1A11 11 0 0 0 2.1 7.1l3.7 2.8C6.7 7.3 9.1 5.4 12 5.4z"/></svg>Voeg watkoopik toe als voorkeursbron in Google</a></div><div class="fine">© %d watkoopik · Wij ontvangen mogelijk een vergoeding als je via onze links iets koopt. Dit kost jou niets extra en beïnvloedt de rangschikking niet. Prijzen zijn indicatief. Als Amazon-partner verdienen wij aan kwalificerende aankopen.</div>%s</div></footer>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="%sapp.js?v=%s" defer></script>
</body></html>''' % (root or "./", LOGO, pop, cats, root, root, root, root, root, root, root, YEAR, landen_regel("watkoopik.nl"), root, ASSET_V)

def page(path, title, desc, body, active=None, extra="", root=None, img=""):
    if root is None: root = "../" * path.count("/")
    out = head(title, desc, path if path != "index.html" else "", root, extra, img) + chrome(active, root) + "<main>" + body + "</main>" + footer(root)
    out = out.replace("categorie/cadeaus.html", "cadeaus/")  # cadeau-hub woont op /cadeaus/
    check(out, path); wr(path, out)

# ---------- bouwstenen ----------
def gcard(g, root=""):
    p = win(g)
    return '''<a class="gc ring tilt rv" href="%s%s" data-cat-item="%s"><div class="gc-img"><span class="tag">Top 10</span>%s</div><div class="gc-body"><h3>%s</h3><p>%s</p><div class="gc-win"><span>Winnaar: <b>%s %s</b></span><span class="pr">%s</span></div></div></a>''' % (
        root, g["url"], g["cat"], img_of(p), e(g["title"]), e(g["intro"][:130].rsplit(" ", 1)[0] + "…"), e(p["brand"]), e(p["name"]), eur(p["price"]))

def mq_items(root="", gl=None):
    items = []
    for g in (gl or guides):
        p = next((x for x in g["products"][:3] if x.get("image")), None)
        if p: items.append('<a class="mq-item" href="%s%s"><img src="%s" alt="" loading="lazy">%s</a>' % (root, g["url"], e(p["image"]), e(g["short"])))
    return items

def marquee(items, rev=False, light=False):
    return '<div class="mq%s%s" aria-hidden="true"><div class="mq-track">%s</div></div>' % (" rev" if rev else "", " mq-light" if light else "", "".join(items) * 2)

# ---------- home ----------
# populair = gidsen gesorteerd op Umami-weergaven + bol-kliks van de laatste 7 dagen (tools/umami.py --save)
try:
    _pop = json.load(open(os.path.join(ROOT, "stats", "populair.json"), encoding="utf-8"))["gidsen"]
except Exception:
    _pop = []
_by_slug = {g["slug"]: g for g in guides}
popular = [_by_slug[s] for s in _pop if s in _by_slug]
popular += [g for g in guides if g not in popular]
# hero-band en winnaarsband: alleen de 60 / 48 populairste gidsen (was alle gidsen x2, ruim 700 afbeeldingen met blur op mobiel)
items = mq_items(gl=popular)[:60]
half = len(items) // 2
chips = "".join('<a href="%s">%s</a>' % (g["url"], e(g["short"])) for g in popular[:9])
# top 3 deze week direct in de hero (bounce homepage 63-65%, populair-blok stond pas onder de vouw); klik meten via event home-top3
def top3card(i, g):
    p = win(g)
    return '<a class="t3" href="%s" data-umami-event="home-top3" data-umami-event-gids="%s" data-umami-event-positie="%d">%s<span><small>Nr. 1 %s</small><b>%s %s</b><em>%s</em></span></a>' % (
        g["url"], g["slug"], i + 1, ('<img src="%s" alt="" width="56" height="56">' % e(p["image"])) if p.get("image") else "", e(g["short"].lower()), e(p["brand"]), e(p["name"]), eur(p["price"]))
top3 = '<div class="hero-top3"><span class="t3-lbl">Populair deze week</span><div class="t3-row">%s</div></div>' % "".join(top3card(i, g) for i, g in enumerate([g for g in popular if win(g).get("image")][:3]))
# N24 (groeimotor 11 nov): wie na een video het domein intypt landt op home; toon daar de gidsen van de laatst geplaatste video's
# (Instagram, TikTok, YouTube; laatste 3 dagen) in plaats van 'Populair deze week' (1 klik op 44 weergaven in 7 dagen).
def _video_gidsen(n=6, dagen=3):
    rows = []
    for f in ("state_reel.json", "state_tt.json", "state_yt.json"):
        try:
            rows += json.load(open(os.path.join(ROOT, "..", "watkoopik-social", f), encoding="utf-8")).get("log", [])
        except Exception:
            pass
    grens = (TODAY - datetime.timedelta(days=dagen)).isoformat()
    out = []
    for r in sorted(rows, key=lambda r: r.get("at", ""), reverse=True):
        s = r.get("slug")
        if not s or r.get("skip") or r.get("at", "") < grens or s not in _by_slug or _by_slug[s] in out: continue
        if win(_by_slug[s]).get("image"): out.append(_by_slug[s])
    return out[:n]
def videocard(i, g):
    return '<a class="t3" href="%s" data-umami-event="home-video" data-umami-event-gids="%s" data-umami-event-positie="%d"><img src="%s" alt="" width="56" height="56"><span><small>Uit onze video</small><b>%s</b><em>Bekijk de top 10 →</em></span></a>' % (
        g["url"], g["slug"], i + 1, e(win(g)["image"]), e(g["short"]))
_vg = _video_gidsen()
if len(_vg) >= 3:
    _vg = _vg[:6] if len(_vg) >= 6 else _vg[:3]
    top3 = '<div class="hero-top3"><span class="t3-lbl">Net in onze video\'s</span><div class="t3-row t3-vid">%s</div></div>' % "".join(videocard(i, g) for i, g in enumerate(_vg))
PALET = {"huishouden": ("#7c5cff", "#38e1ff"), "keuken": ("#ff7a3d", "#ff4fd8"), "verzorging": ("#ff4fd8", "#7c5cff"), "slapen": ("#3b5bff", "#38e1ff"),
         "elektronica": ("#00c2ff", "#7c5cff"), "wonen": ("#3ee08f", "#38e1ff"), "sport": ("#ffc65c", "#ff7a3d"), "kind": ("#ff8fb1", "#ffc65c"), "klussen": ("#ffc65c", "#3ee08f"),
         "computer": ("#38e1ff", "#3b5bff"), "telefoon": ("#7c5cff", "#ff4fd8")}
for _k in CATS: PALET.setdefault(_k, ("#7c5cff", "#38e1ff"))
cat_keys = [k for k in CATS if by_cat.get(k)]
sizes = ["big", "", "", "wide", "", ""]
cat_cards = "".join('''<a class="cat ring tilt rv %s" href="categorie/%s.html" style="--c1:%s;--c2:%s"><span class="ic">%s</span><span class="thumbs">%s</span><b>%s</b><small>%d gidsen · %s</small></a>''' % (
    sizes[i] if i < len(sizes) else "", k, PALET[k][0], PALET[k][1], icon(k), "".join('<img src="%s" alt="" loading="lazy">' % e(win(x)["image"]) for x in by_cat[k][:4] if win(x).get("image")),
    CATS[k][0], len(by_cat[k]), CATS[k][1].split(",")[0]) for i, k in enumerate(cat_keys))
winners = [g for g in popular if win(g).get("image")]
def wincard(g):
    p = win(g)
    return '''<a class="wincard" href="%s"><div class="im"><span class="crown">Nr. 1 %s</span><img src="%s" alt="%s %s" loading="lazy"></div><div class="bd"><small>%s · winnaar</small><h3>%s %s</h3><div class="pr">%s</div></div></a>''' % (
        g["url"], e(g["short"].lower()), e(p["image"]), e(p["brand"]), e(p["name"]), e(g["short"]), e(p["brand"]), e(p["name"]), eur(p["price"]))
wh = 24
winband = '<div class="mq winband">%s</div><div class="mq winband rev" style="margin-top:14px">%s</div>' % (
    '<div class="mq-track">%s</div>' % ("".join(wincard(g) for g in winners[:wh]) * 2),
    '<div class="mq-track">%s</div>' % ("".join(wincard(g) for g in winners[wh:2 * wh]) * 2))
fl_imgs = [win(g)["image"] for g in winners[:6]]
floaters = '<div class="floaters" aria-hidden="true">%s</div>' % "".join('<div class="fl f%d" data-depth="%s"><div class="in"><img src="%s" alt=""></div></div>' % (i + 1, [.6, 1, .4, .8, .3, .5][i], e(im)) for i, im in enumerate(fl_imgs))

newest = sorted(guides, key=lambda g: (g.get("published", g.get("updated", "")), g["slug"]), reverse=True)
# seizoensblok Sinterklaas en kerst (directeur 2 nov): tv-gidsen eerst (grootste commissie eind okt), dan cadeaugidsen; t/m 25 december
SEIZOEN_SLUGS = ["beste-tv-55-inch", "beste-tv-65-inch", "beste-tv-onder-500-euro", "beste-sinterklaascadeau-onder-25-euro", "beste-cadeau-voor-hem-onder-50-euro",
                 "beste-cadeau-voor-haar-onder-50-euro", "beste-kerstcadeau-voor-ouders", "beste-tech-cadeau-onder-100-euro", "beste-cadeau-voor-thuiswerkers", "beste-adventskalender"]
seizoen = [_by_slug[s] for s in SEIZOEN_SLUGS if s in _by_slug]
def seizoen_sec(root=""):
    if not seizoen or TODAY > datetime.date(2026, 12, 25): return ""
    return '''<section data-hue="1" style="padding-bottom:0"><div class="wrap">
<div class="sec-head rv"><div><span class="kick">Sinterklaas · Kerst · Black Friday</span><h2>Cadeaus en tv's <span class="grad">voor december</span></h2></div><a class="more" href="%scadeaus/">Alle cadeaugidsen →</a></div>
<div class="gl">%s</div></div></section>''' % (root, "".join(gcard(g, root) for g in seizoen[:8]))
home_deals = ('''<section data-hue="1" style="padding-bottom:0"><div class="wrap">
<div class="sec-head rv"><div><span class="kick">Prijsdalingen</span><h2>Nu <span class="grad">echt goedkoper</span></h2></div><a class="more" href="aanbiedingen/">Alle %d aanbiedingen →</a></div>
<div class="deals">%s</div><p class="muted" style="font-size:.9rem;margin-top:14px"><a href="black-friday/echte-kortingen-2026.html">Black Friday 2026: zoveel kortingen zijn echt</a> · onze eigen dagelijkse prijsmetingen bij bol</p></div></section>''' % (len(DEALS), "".join(deal_row(g, p, d, "") for g, p, d in DEALS[:4]))) if DEALS else '''<section data-hue="1" style="padding-bottom:0"><div class="wrap"><p class="muted"><a href="aanbiedingen/">Aanbiedingen</a>: hier verschijnen producten uit onze top 10's die minstens 10%% goedkoper zijn dan eerder gemeten.</p></div></section>'''
home = '''
<section class="hero" data-hue="0">%s
<div class="hero-in">
<span class="badge"><i></i> Elke dag nieuwe top 10's · prijzen dagelijks gecheckt</span>
<h1 class="split">Wat koop ik? <span class="grad">Wij zochten het uit.</span></h1>
<p class="lead">Onafhankelijke top 10-lijsten van de beste producten van %d. Vergeleken op prijs, specificaties en duizenden reviews, zodat jij in vijf minuten de juiste keuze maakt.</p>
%s
%s
<div class="hero-chips">%s</div>
<div class="hero-stats"><div><b class="grad" data-count="%d">%d</b><span>top 10-gidsen</span></div><div><b class="grad" data-count="%d">%d</b><span>producten vergeleken</span></div><div><b class="grad" data-count="%d">%s</b><span>reviews meegewogen</span></div></div>
</div>
<div class="hero-band">%s%s</div>
</section>

<section data-hue="1" style="padding-bottom:0"><div class="wrap">
<div class="sec-head rv"><div><span class="kick">Populair</span><h2>Deze week <span class="grad">het meest bekeken</span></h2></div><a class="more" href="gidsen.html">Alle gidsen →</a></div>
<div class="gl">%s</div>
</div></section>

%s
%s
<section data-hue="1"><div class="wrap">
<div class="sec-head rv"><div><span class="kick">Categorieën</span><h2>Waar ben je naar <span class="grad">op zoek?</span></h2></div><p>Kies een categorie en zie meteen de winnaars per productsoort.</p></div>
<div class="bento">%s</div>
</div></section>

<section data-hue="2" style="padding-left:0;padding-right:0"><div class="wrap"><div class="sec-head rv"><div><span class="kick">De winnaars</span><h2>Nummer 1 in <span class="grad">elke top 10</span></h2></div><a class="more" href="gidsen.html">Alle gidsen →</a></div></div>
%s
</section>

<section data-hue="3"><div class="wrap">
<div class="sec-head rv"><div><span class="kick">Nieuw</span><h2>Nieuwste <span class="grad">gidsen</span></h2></div><a class="more" href="gidsen.html">Alle %d gidsen →</a></div>
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
''' % (floaters, YEAR, searchbox(), top3, chips, len(guides), len(guides), N_PROD, N_PROD, N_REV, format(N_REV, ",").replace(",", "."),
       marquee(items[:half]), marquee(items[half:], rev=True), "".join(gcard(g) for g in popular[:6]), seizoen_sec(), home_deals, cat_cards, winband, len(guides), "".join(gcard(g) for g in newest[:12]),
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
     '<section data-hue="1" style="padding-top:34px"><div class="wrap"><span class="kick">Overzicht</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">Alle %d top 10-gidsen</h1><p class="muted" style="max-width:620px">Filter op categorie of zoek direct op product of merk.</p><div style="max-width:560px;margin:14px 0 18px">%s</div>%s%s<div class="gl">%s</div></div></section>' % (
         len(guides), searchbox(), hub_chips(sorted(HUBS, key=lambda c: -len(c["members"]))), filt, "".join(gcard(g) for g in guides)), "gidsen.html")

# ---------- categorieën ----------
for k, v in CATS.items():
    gs = by_cat.get(k, [])
    if not gs or k == "cadeaus": continue
    body = '''<section style="padding-top:20px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a> › %s</nav>
<span class="kick" style="margin-top:14px">Categorie</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">De beste %s van %d</h1>
<p class="muted" style="max-width:760px">%s</p>%s<p class="muted" style="max-width:760px;font-size:.9rem">%d gidsen in deze categorie · %s</p>
<div class="gl" style="margin-top:22px">%s</div></div></section>''' % (v[0], v[0].lower(), YEAR, e(CAT_INTRO.get(k) or (v[1] + ". In deze gidsen vergelijken we per productsoort de tien beste modellen op prijs, specificaties en gebruikersreviews.")),
        hub_chips([c for c in HUBS if c["cat"] == k or any(x["cat"] == k for x in c["members"])], "../"), len(gs),
        " · ".join('<a href="../%s">%s</a>' % (x["url"], e(x["short"])) for x in sorted(gs, key=lambda x: x["short"].lower())), "".join(gcard(g, "../") for g in gs))
    cld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": v[0], "item": SITE + "/categorie/%s.html" % k}]},
           {"@context": "https://schema.org", "@type": "ItemList", "name": "Beste %s van %d" % (v[0].lower(), YEAR), "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/" + x["url"], "name": x["title"]} for i, x in enumerate(gs)]}]
    page("categorie/%s.html" % k, "Beste %s %d: alle top 10's | watkoopik" % (v[0].lower(), YEAR), "%s. Vergelijk per productsoort de tien beste modellen van %d op prijs, specificaties en reviews." % (v[1], YEAR), body,
         extra="".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in cld))

# ---------- gidspagina's ----------
# A/B-test C4 (groeimotor, 7 nov 2026): upgrade-tip onder de kaart van nr. 1 naar het premiummodel (hogere orderwaarde).
# Verdeling los van C1 (md5 van "c4:" + slug even = tip), alleen als premium minstens 30% duurder is dan nr. 1.
def c4_variant(slug):
    return "tip" if int(hashlib.md5(("c4:" + slug).encode()).hexdigest(), 16) % 2 == 0 else "controle"
def upgrade_tip(g):
    ps = g["products"]; top = ps[0]
    pr = next((p for p in ps[1:] if p.get("label") == "Beste premium"), None)
    if not pr or c4_variant(g["slug"]) != "tip" or not top.get("price") or pr["price"] < 1.3 * top["price"]: return ""
    h = hist_of(pr)
    extra = (" Nu %s van onze metingen." % rel_txt(h["rel"])) if h and h["rel"] <= -0.03 else ""
    return '<div class="upg"><span class="upg-lbl">Meer budget?</span><p>Onze premiumkeuze is nr. %d: de <b>%s %s</b> voor %s. %s%s</p>%s</div>' % (
        pr["rank"], e(pr["brand"]), e(pr["name"]), eur(pr["price"]), e(pr["oneliner"].rstrip(".") + "."), e(extra), shop_a(pr, g, "btn btn-buy btn-sm", "upgrade"))

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
    podium = "".join('''<div class="pd%s"><span class="lbl">%s</span><div class="im">%s</div><h3>%s %s</h3><div class="pr">%s</div>%s<p>%s</p>%s</div>''' % (
        " first" if i == 0 else "", e(p["label"]), img_of(p), e(p["brand"]), e(p["name"]), eur(p["price"]), chk_html(p, g), e(p["oneliner"]), shop_a(p, g, "btn btn-buy btn-sm magnet", "podium") + amazon_a(p, g, "podium")) for i, p in enumerate(labs))
    keys = list(ps[0]["specs"].keys())[:3]
    rows = "".join('<tr><td><span class="rk%s">%d</span></td><td class="nm"><span class="ti">%s<span>%s<small>%s</small></span></span></td>%s<td><b>%s</b>%s</td><td><span class="sc%s">%s</span></td><td class="bc">%s</td></tr>' % (
        " r1" if p["rank"] == 1 else "", p["rank"], ('<img src="%s" alt="" loading="lazy">' % e(p["image"])) if p.get("image") else "", e(p["brand"]), e(p["name"]),
        "".join("<td>%s</td>" % e(str(p["specs"].get(k, "-"))) for k in keys), eur(p["price"]), chk_html(p, g, True), " hi" if p["score"] >= 9 else "", p["score"], shop_a(p, g, "btn btn-buy btn-sm", "tabel")) for p in ps)
    table = '<div class="tbl rv"><table><thead><tr><th>#</th><th>Model</th>%s<th>Prijs</th><th>Score</th><th class="bc"><span class="sr">Kopen</span></th></tr></thead><tbody>%s</tbody></table></div>' % ("".join("<th>%s</th>" % e(k) for k in keys), rows)
    cards = "".join('''<article class="pr-card%s rv" id="p%d"><div class="pr-head"><div class="pr-img"><span class="n">%d</span>%s</div><div>%s<h2>%s %s</h2>
<div class="pr-meta"><span class="price">%s</span><span>%s <b>%s</b>/10</span><span>%s</span></div>%s<div class="specs">%s</div></div></div>
<div class="pr-txt">%s</div><div class="pc"><div class="pros"><h4>Pluspunten</h4><ul>%s</ul></div><div class="cons"><h4>Minpunten</h4><ul>%s</ul></div></div>
%s<div class="ideal"><b>Ideaal voor:</b> %s</div><div class="buy">%s%s<small>Prijs gecontroleerd op %s</small></div>%s</article>''' % (
        " top" if p["rank"] == 1 else "", p["rank"], p["rank"], img_of(p), ('<span class="pr-lbl">%s</span>' % e(p["label"])) if p.get("label") else "", e(p["brand"]), e(p["name"]),
        eur(p["price"]), stars(p["score"]), p["score"], e(p.get("reviews", "")), bars(p, g), "".join("<span><b>%s:</b> %s</span>" % (e(k), e(str(v))) for k, v in p["specs"].items()),
        "".join("<p>%s</p>" % e(t) for t in p["text"].split("\n\n")), "".join("<li>%s</li>" % e(x) for x in p["pros"]), "".join("<li>%s</li>" % e(x) for x in p["cons"]),
        hist_box(p), e(p["ideal"]), shop_a(p, g), amazon_a(p, g), e(chk_date(p, g)), upgrade_tip(g) if p["rank"] == 1 else "") for p in ps)
    guide_html = "".join("<h3>%s</h3>%s" % (e(s["h"]), "".join("<p>%s</p>" % e(t) for t in s["p"].split("\n\n"))) for s in g["guide"]) + cl_more(g)
    # optioneel veld "kies" (groeimotor N6, 6 nov 2026): beslispunten + wanneer nr. 2 of 3, met eigen koopknop
    kq = g.get("kies") or {}
    byr = {p["rank"]: p for p in ps}
    kies_html = ('<div class="guide rv" id="zo-kies-je"><h2>Zo kies je in %d vragen</h2>%s%s</div>' % (len(kq.get("keuzes", [])),
        "".join("<h3>%s</h3><p>%s</p>" % (e(k["h"]), e(k["p"])) for k in kq.get("keuzes", [])),
        ("<h2>Wanneer kies je nr. 2 of 3?</h2>" + "".join('<h3>Nr. %d: %s %s</h3><p>%s</p><p>%s</p>' % (w["rank"], e(byr[w["rank"]]["brand"]), e(byr[w["rank"]]["name"]), e(w["p"]), shop_a(byr[w["rank"]], g, "btn btn-buy btn-sm", "wanneer"))
            for w in kq.get("wanneer", []) if w.get("rank") in byr)) if kq.get("wanneer") else "")) if kq.get("keuzes") else ""
    hubc = next((c for c in CL_OF.get(g["slug"], []) if c["hub"]), None)  # familie-overzicht in kruimelpad en schema
    hf = hist_faq(g)  # FAQ uit eigen prijsmetingen (alleen in de pagina, niet in de bron-json)
    if hf and not any(q["q"] == hf["q"] for q in g["faq"]): g["faq"] = g["faq"] + [hf]
    pf = pop_faq(g); pop = pop_html(g)
    if pf and not any(q["q"] == pf["q"] for q in g["faq"]): g["faq"] = g["faq"] + [pf]
    faq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q["q"]), e(q["a"])) for q in g["faq"])
    toc = "".join('<li><a href="#p%d">%s %s</a></li>' % (p["rank"], e(p["brand"]), e(p["name"])) for p in ps)
    # varianten van hetzelfde product eerst (beste-airfryer <-> beste-airfryer-1-persoon), daarna dezelfde categorie
    stem = lambda sl: sl[6:].split("-")[0]
    fam, _ids = [], {id(g)}  # eerst de productfamilies, dan gidsen met dezelfde stam
    for x in [x for c in CL_OF.get(g["slug"], []) for x in c["members"]] + [x for x in guides if stem(x["slug"]) == stem(g["slug"])]:
        if id(x) not in _ids: _ids.add(id(x)); fam.append(x)
    words = lambda x: set(re.findall(r"[a-zà-ü]{4,}", " ".join([x["slug"], x["query"]] + x.get("keywords", [])).lower())) - {"beste", "goedkoop", "kopen", "2026", "review", "test"}
    gw = words(g)
    same = [x for x in fam if x["cat"] == g["cat"]] + sorted([x for x in by_cat[g["cat"]] if x["slug"] != g["slug"] and x not in fam], key=lambda x: -len(gw & words(x)))
    # optioneel veld "rel": vaste verwante gidsen vooraan (sinds 27 okt 2026, extra inlinks naar gidsen met zoekvertoningen)
    forced = [x for s in g.get("rel", []) for x in guides if x["slug"] == s]
    rel = forced + [x for x in same if x not in forced][:4 - min(len(forced), 2)] + [x for x in fam if x["cat"] != g["cat"] and x not in forced][:1]
    gi = guides.index(g)  # aanvullen met gidsen uit andere categorieen, per gids verschoven zodat elke gids inlinks krijgt
    _rot = []  # rotatie over andere categorieen, zonder dubbele (stap 7 liep rond als len(guides) deelbaar is door 7)
    for x in (guides[(gi + 7 * j + 3) % len(guides)] for j in range(len(guides))):
        if x["cat"] != g["cat"] and x not in rel and x not in _rot: _rot.append(x)
    rel = rel[:8] + _rot[:max(0, 6 - len(rel))]  # sinds 12 nov 2026: nooit meer dan 8 kaarten (indexatie-onderzoek)
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
          {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["intro"][:200], "dateModified": gmod(g),
           "datePublished": g.get("published", g.get("updated", TODAY.isoformat())), "author": {"@type": "Person", "name": "Nick van Straaten", "url": SITE + "/over-ons.html#nick", "jobTitle": "Oprichter en eindredacteur"},
           "publisher": {"@type": "Organization", "name": "watkoopik", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.svg"}}, "mainEntityOfPage": url_abs,
           "image": [SITE + "/og/%s.jpg" % g["slug"]] + [p["image"] for p in ps if p.get("image")][:2]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in g["faq"]]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": CATS[g["cat"]][0], "item": SITE + "/categorie/%s.html" % g["cat"]}] +
              ([{"@type": "ListItem", "position": 3, "name": cap1(hubc["meervoud"]), "item": SITE + "/" + hubc["hub"]}] if hubc else []) +
              [{"@type": "ListItem", "position": 4 if hubc else 3, "name": g["title"], "item": url_abs}]}]
    extra = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    body = '''<div class="wrap"><nav class="crumbs"><a href="../">Home</a> › <a href="../categorie/%s.html">%s</a> › %s</nav>%s
<div class="ghero"><span class="kick">Top 10 · %s</span><h1 class="split">%s</h1><p class="intro">%s</p>
<div class="meta-line"><span>Bijgewerkt <b>%s</b></span><span><b>%d</b> modellen</span>%s<span>Door <a href="../over-ons.html#nick"><b>Nick van Straaten</b></a></span></div>
<p class="disc disc-top">Bevat affiliatelinks, <a href="#disclaimer">zo verdienen wij</a>.</p></div>
%s<div class="podium">%s</div>
%s<p class="disc" id="disclaimer">Wij ontvangen mogelijk een vergoeding als je via onze links iets koopt. Dit kost jou niets extra en bepaalt niet welke producten in de lijst staan. <a href="../zo-kiezen-wij.html">Zo kiezen wij</a>.</p>
<div class="layout"><div>
<h2 id="vergelijk" class="rv" style="margin-top:22px">Alle %d naast elkaar</h2>%s%s
<h2 id="top10" class="rv">De top 10 in detail</h2>%s
%s%s<div class="verdict rv"><span class="kick" style="color:#ffb48a">Eindoordeel</span><h2>Onze conclusie</h2><p>%s</p>%s</div>
<div class="guide rv" id="koopgids"><h2>Koopgids: zo kies je %s juiste %s</h2>%s</div>
<div class="faq rv" id="faq"><h2>Veelgestelde vragen</h2>%s</div>
<div class="pref-wrap">%s</div>
</div>
<aside class="side"><details class="toc"><summary>In deze gids</summary><ol><li><a href="#vergelijk">Vergelijkingstabel</a></li>%s%s%s%s<li><a href="#koopgids">Koopgids</a></li><li><a href="#faq">Veelgestelde vragen</a></li></ol></details></aside>
</div>
<section style="padding:40px 0"><div class="sec-head"><h2>Meer gidsen in %s</h2><a class="more" href="../categorie/%s.html">Alle %d →</a></div><div class="gl">%s</div></section>
</div>
<div class="sticky-buy">%s<div><b>Nr. 1: %s %s</b>%s</div>%s</div>''' % (
        g["cat"], CATS[g["cat"]][0], (('<a href="../%s">%s</a> › ' % (hubc["hub"], e(cap1(hubc["meervoud"])))) if hubc else "") + e(g["short"]), cl_nav(g), CATS[g["cat"]][0], e(g["title"]), e(g["intro"]), e(nldate(gmod(g))), len(ps), ("<span><b>%s</b> reviews</span>" % e(str(g["reviews_total"]))) if str(g.get("reviews_total", "")).strip("0. ") else "",
        own_pos(g, "boven"), podium, own_pos(g, "onder") + "".join('<a class="vs-link" href="../vs/%s.html" data-umami-event="vs-link"><b>Twijfel je tussen nr. %d en nr. %d?</b> %s %s of %s %s: wie wint per situatie →</a>' % (v["slug"], v["pa"]["rank"], v["pb"]["rank"], e(v["pa"]["brand"]), e(v["pa"]["name"]), e(v["pb"]["brand"]), e(v["pb"]["name"])) for v in VS_BY_GUIDE.get(g["slug"], [])), len(ps), table, pop, cards, hist_section(g) + logboek_html(g), kies_html, e(g["verdict"]), shop_a(top, g, plek="eindoordeel"), zoekterm_vorm(zoekterm(g))[1], e(zoekterm(g)), guide_html, faq, PREF_BTN, toc, '<li><a href="#populair">Populair bij bol</a></li>' if pop else "", ('<li><a href="#prijsverloop">Prijsverloop</a></li>' if hist_section(g) else "") + ('<li><a href="#logboek">Logboek</a></li>' if logboek_html(g) else ""), '<li><a href="#zo-kies-je">Zo kies je</a></li>' if kies_html else "", CATS[g["cat"]][0].lower(), g["cat"], len(by_cat[g["cat"]]), "".join(gcard(x, root) for x in rel),
        ('<img src="%s" alt="">' % e(top["image"])) if top.get("image") else "", e(top["brand"]), e(top["name"]), "" if ab_variant(g["slug"]) == "prijs" else eur(top["price"]), shop_a(top, g, "btn btn-buy btn-sm", "sticky"))
    bv = next((p for p in ps if p.get("label") == "Beste prijs-kwaliteit"), ps[1])
    seo = zoekterm(g)  # zoekterm voor titel en meta; query blijft de bol-zoekterm
    lidw, _, ww = zoekterm_vorm(seo)
    title = "Beste %s %d: top 10 vergeleken | watkoopik" % (seo, YEAR)
    if len(title) > 62: title = "%s | watkoopik" % g["title"]
    desc = "%s beste %s van %d %s de %s %s (%s). Slimste koop: %s %s voor %s. Bekijk de volledige top 10 met plus- en minpunten, koopgids en FAQ." % (
        lidw, seo, YEAR, ww, top["brand"], top["name"], eur(top["price"]), bv["brand"], bv["name"], eur(bv["price"]))
    # optionele vaste titel/meta op echte Search Console-zoekvragen ({top} = huidige nr. 1)
    if g.get("meta_title"): title = g["meta_title"]
    if g.get("meta_desc"): desc = g["meta_desc"].replace("{top}", "%s %s" % (top["brand"], top["name"]))
    page(g["url"], title, desc, body, extra=extra, img=og_img(g, top))

# ---------- aanbiedingen ----------
def deals_body(root, kick="Aanbiedingen", h1="Echte prijsdalingen in onze top 10's", lead=None):
    lead = lead or "Wij controleren elke dag de bol-prijs van alle %d producten in onze gidsen. Hier staan de producten die nu minstens 10%% goedkoper zijn dan de laagste prijs die wij in de dertig dagen daarvoor maten. Een prijs die heen en weer springt tussen twee bedragen telt dus niet als daling. Geen adviesprijzen of verzonnen van-prijzen: alleen wat wij zelf hebben gemeten." % N_PROD
    if DEALS:
        lst = '<div class="deals">%s</div>' % "".join(deal_row(g, p, d, root) for g, p, d in DEALS)
    else:
        lst = '<div class="deal-empty"><h2>Nu even geen echte aanbiedingen</h2><p>Geen enkel product uit onze top 10\'s is op dit moment minstens 10%% goedkoper dan eerder gemeten. Dat gebeurt: prijzen bewegen per week. Kom later terug of bekijk <a href="%sslimste-koop.html">de slimste koop per productsoort</a>.</p></div>' % root
    return '''<section data-hue="1" style="padding-top:34px"><div class="wrap"><nav class="crumbs"><a href="%s">Home</a> › %s</nav><span class="kick" style="margin-top:14px">%s</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">%s</h1>
<p class="muted" style="max-width:720px">%s</p><p class="muted" style="font-size:.85rem">%d producten met een gemeten prijsdaling · bijgewerkt %s · <a href="%sblack-friday/echte-kortingen-2026.html">Zoveel Black Friday-kortingen zijn echt</a> · <a href="%sprijs/">prijsverloop per model</a> · wij ontvangen mogelijk een vergoeding als je via onze links koopt.</p>%s</div></section>''' % (
        root or "./", kick, kick, h1, lead, len(DEALS), nldate(TODAY.isoformat()), root, root, lst)
page("aanbiedingen/index.html", "Aanbiedingen: echte prijsdalingen bij bol | watkoopik", "Producten uit onze top 10-gidsen die nu minstens 10% goedkoper zijn dan hun laagste bol-prijs van de 30 dagen ervoor. Dagelijks bijgewerkt, alleen eigen metingen.",
     deals_body("../"), "aanbiedingen/", root="../")

# ---------- vs-pagina's ----------
def vs_page(v):
    g, a, b = v["g"], v["pa"], v["pb"]; root = "../"
    keys = list(a["specs"].keys())
    rows = [("Plek in onze top 10", "Nr. %d" % a["rank"], "Nr. %d" % b["rank"]), ("Prijs bij bol", eur(a["price"]), eur(b["price"])), ("Onze score", "%s/10" % a["score"], "%s/10" % b["score"]), ("Reviews", a.get("reviews", ""), b.get("reviews", ""))]
    rows += [(k, str(a["specs"].get(k, "-")), str(b["specs"].get(k, "-"))) for k in keys]
    tbl = '<div class="tbl"><table><thead><tr><th>Specificatie</th><th>%s %s</th><th>%s %s</th></tr></thead><tbody>%s</tbody></table></div>' % (
        e(a["brand"]), e(a["name"]), e(b["brand"]), e(b["name"]), "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (e(r[0]), e(r[1]), e(r[2])) for r in rows))
    sit = "".join('<div class="vs-sit"><span>%s</span><b>%s %s</b><p>%s</p></div>' % (e(x[0]), e((a if x[1] == "a" else b)["brand"]), e((a if x[1] == "a" else b)["name"]), e(x[2])) for x in v["sit"])
    def side(p):
        return '<div class="pd%s"><span class="lbl">Nr. %d · %s</span><div class="im">%s</div><h3>%s %s</h3><div class="pr">%s</div>%s<p>%s</p><ul class="vs-pc">%s%s</ul>%s</div>' % (
            " first" if p["rank"] == 1 else "", p["rank"], e(p.get("label") or "Top 10"), img_of(p), e(p["brand"]), e(p["name"]), eur(p["price"]), chk_html(p, g), e(p["oneliner"]),
            "".join("<li>+ %s</li>" % e(x) for x in p["pros"][:3]), "".join("<li>- %s</li>" % e(x) for x in p["cons"][:2]), shop_a(p, g, "btn btn-buy btn-sm magnet", "vs"))
    t = vs_title(v)
    body = '''<div class="wrap"><nav class="crumbs"><a href="../">Home</a> › <a href="./">Vergelijkingen</a> › <a href="../%s">%s</a></nav>
<div class="ghero"><span class="kick">Vergelijking</span><h1 class="split">%s</h1><p class="intro">%s</p><p class="disc disc-top">Bevat affiliatelinks, <a href="../disclaimer.html">zo verdienen wij</a>.</p></div>
<div class="podium vs2">%s%s</div>
<h2 class="rv" style="margin-top:26px">Wie wint per situatie?</h2><div class="vs-sits">%s</div>
<h2 class="rv" style="margin-top:26px">Specificaties naast elkaar</h2>%s
<div class="verdict rv"><span class="kick" style="color:#ffb48a">Eindoordeel</span><h2>Onze conclusie</h2><p>%s</p><div style="display:flex;gap:10px;flex-wrap:wrap">%s%s</div></div>
<p class="muted" style="margin:24px 0 40px">Beide modellen staan in onze <a href="../%s">%s</a>. Daar vind je ook de acht andere modellen, een koopgids en veelgestelde vragen. Wij vergelijken op specificaties, prijs en kopersreviews.</p></div>''' % (
        g["url"], e(g["short"]), e(t), e(v["intro"]), side(a), side(b), sit, tbl, e(v["verdict"]), shop_a(a, g, "btn btn-buy", "vs-oordeel"), shop_a(b, g, "btn btn-buy", "vs-oordeel"), g["url"], e(g["title"].lower().replace("de 10 beste", "top 10 van de beste")))
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Vergelijkingen", "item": SITE + "/vs/"}, {"@type": "ListItem", "position": 3, "name": t, "item": SITE + "/vs/%s.html" % v["slug"]}]}]
    tt = "%s: welke kies je? | watkoopik" % t
    if len(tt) > 70: tt = "%s %s vs %s %s | watkoopik" % (a["brand"], a["name"].split()[0], b["brand"], b["name"].split()[0])
    page("vs/%s.html" % v["slug"], tt, "%s %s (%s) of %s %s (%s)? Specificaties naast elkaar en per situatie de winnaar. %s" % (a["brand"], a["name"], eur(a["price"]), b["brand"], b["name"], eur(b["price"]), v["verdict"][:90].rsplit(" ", 1)[0] + "."), body,
         extra='<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), img=a.get("image", ""))
for v in VS_PAGES: vs_page(v)
# Verlopen vergelijkingen (product niet meer in de gids): noindex-doorverwijzing naar de gids, zodat oude URL's niet 404'en of verouderd blijven (sinds 26 okt 2026)
_live = {v["slug"] for v in VS_PAGES}
for v in _vs:
    g = _gs.get(v["gids"])
    if v["slug"] in _live or not g: continue
    wr("vs/%s.html" % v["slug"], '''<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vergelijking verlopen | watkoopik</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="%s/%s">
<meta http-equiv="refresh" content="0; url=../%s">
</head><body><p>Een van beide modellen staat niet meer in onze top 10. Bekijk de actuele <a href="../%s">%s</a>.</p></body></html>''' % (SITE, g["url"], g["url"], g["url"], e(g["title"].lower().replace("de 10 beste", "top 10 van de beste"))))
    print("let op: vergelijking %s verlopen, doorverwijzing naar %s" % (v["slug"], g["url"]))
page("vs/index.html", "Vergelijkingen: X tegenover Y | watkoopik", "De populairste twijfelgevallen uit onze top 10's naast elkaar: specificaties, prijs en per situatie de winnaar.",
     '''<section style="padding-top:34px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a> › Vergelijkingen</nav><span class="kick" style="margin-top:14px">Vergelijkingen</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">Twijfel je tussen twee modellen?</h1>
<p class="muted" style="max-width:720px">Hier zetten we de modellen waar de meeste lezers tussen twijfelen naast elkaar, meestal de nummer 1 en 2 uit een gids. Per situatie zie je wie wint.</p><div class="rows" style="margin-top:18px">%s</div></div></section>''' % "".join(
         '<a class="rw rv" href="%s.html"><div class="rw-img">%s</div><div><h3>%s</h3><small>Uit %s</small></div><b>→</b></a>' % (v["slug"], img_of(v["pa"]), e(vs_title(v)), e(v["g"]["short"].lower())) for v in VS_PAGES), root="../")

# ---------- prijsverloop-pagina's per model (groeimotor N13, zie PRIJS hierboven) ----------
def big_chart(h, w=640, ht=220):
    lo, hi = h["low"], h["high"]; pad = (hi - lo) * 0.15 or max(1, lo * 0.03); lo2, hi2 = lo - pad, hi + pad
    d0 = datetime.date.fromisoformat(h["first"]); span = max(1, (datetime.date.fromisoformat(h["days"][-1]) - d0).days)
    X = lambda d: 64 + (w - 80) * (datetime.date.fromisoformat(d) - d0).days / span
    Y = lambda v: 14 + (ht - 44) * (1 - (v - lo2) / (hi2 - lo2))
    pts = " ".join("%.1f,%.1f" % (X(d), Y(v)) for d, v in zip(h["days"], h["vals"]))
    grid = "".join('<line x1="64" x2="%d" y1="%.1f" y2="%.1f" stroke="currentColor" stroke-opacity=".15"/><text x="58" y="%.1f" text-anchor="end" font-size="12" fill="currentColor" fill-opacity=".7">%s</text>' % (w - 16, Y(v), Y(v), Y(v) + 4, e(eur(round(v)))) for v in sorted({lo, hi, round(h["avg"], 2)}))
    xl = '<text x="64" y="%d" font-size="12" fill="currentColor" fill-opacity=".7">%s</text><text x="%d" y="%d" text-anchor="end" font-size="12" fill="currentColor" fill-opacity=".7">%s</text>' % (ht - 8, e(nldate(h["first"])), w - 16, ht - 8, e(nldate(h["days"][-1])))
    dots = "".join('<circle cx="%.1f" cy="%.1f" r="2.6" fill="currentColor"/>' % (X(d), Y(v)) for d, v in zip(h["days"], h["vals"]))
    return '<svg class="pp-chart" viewBox="0 0 %d %d" role="img" aria-label="Prijsverloop bij bol van %s tot %s">%s%s<polyline points="%s" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>%s</svg>' % (
        w, ht, e(nldate(h["first"])), e(nldate(h["days"][-1])), grid, xl, pts, dots)
def prijs_page(k, x):
    p, g = x["p"], x["in"][0][0]
    g = next(gg for gg, pp in x["in"] if pp is p); h = hist_of(p); nm = "%s %s" % (p["brand"], p["name"]); root = "../"
    if h["high"] - h["low"] < 0.01:
        intro = "Wij noteren elke dag de prijs van de %s bij bol. Op alle %d meetdagen sinds %s kostte hij %s: de prijs is stabiel." % (nm, h["n"], nldate(h["first"]), eur(p["price"]))
        moment = "Wachten op een lagere prijs heeft bij dit model tot nu toe niets opgeleverd. Zakt hij minstens 10%, dan staat hij meteen op onze aanbiedingenpagina."
    else:
        intro = "Wij noteren elke dag de prijs van de %s bij bol. Sinds %s maten we op %d dagen een laagste prijs van %s (op %s) en een hoogste van %s. Gemiddeld was het %s. Nu kost hij %s, dat is %s." % (
            nm, nldate(h["first"]), h["n"], eur(h["low"]), nldate(h["low_day"]), eur(h["high"]), eur(round(h["avg"], 2)), eur(p["price"]), rel_txt(h["rel"]))
        if p["price"] <= h["low"] + 0.01: moment = "Dit is de laagste prijs die wij voor dit model hebben gemeten."
        elif h["rel"] <= -0.03: moment = "Hij zit nu onder zijn gemiddelde prijs, maar niet op het laagste punt: dat was %s op %s." % (eur(h["low"]), nldate(h["low_day"]))
        elif h["rel"] >= 0.03: moment = "Hij is nu duurder dan gemiddeld. De laagste prijs die wij maten was %s op %s. Geen haast? Dan loont wachten op een daling misschien." % (eur(h["low"]), nldate(h["low_day"]))
        else: moment = "De prijs zit rond het gemiddelde van onze metingen. Een echte daling van 10% of meer zie je meteen op onze aanbiedingenpagina."
    if TODAY <= datetime.date(2026, 12, 1): moment += " Black Friday valt op 27 november: omdat wij elke dag meten, zie je hier dan of een korting echt lager is dan de weken ervoor."
    days = h["days"][::-1][:30]; vals = h["vals"][::-1][:30]
    trs = "".join("<tr><td>%s</td><td><b>%s</b></td><td>%s</td></tr>" % (e(nldate(d)), eur(v), ("" if i + 1 >= len(vals) or abs(v - vals[i + 1]) < 0.01 else ("%s %s" % ("omlaag" if v < vals[i + 1] else "omhoog", eur(round(abs(v - vals[i + 1]), 2)))))) for i, (d, v) in enumerate(zip(days, vals)))
    plekken = "".join('<li>Nr. %d in de <a href="../%s#p%d">%s</a>%s</li>' % (pp["rank"], gg["url"], pp["rank"], e(gg["title"].lower().replace("de 10 beste", "top 10 van de beste")), (" · %s" % e(pp["label"])) if pp.get("label") else "") for gg, pp in sorted(x["in"], key=lambda t: t[1]["rank"]))
    specs = "".join("<tr><td>%s</td><td>%s</td></tr>" % (e(kk), e(str(vv))) for kk, vv in p["specs"].items())
    alts = [q for q in g["products"][:4] if q is not p][:3]
    alt = "".join('<a class="rw rv" href="../%s"><div class="rw-img">%s</div><div><h3>%s %s</h3><small>Nr. %d · nu %s</small></div><b>→</b></a>' % (
        prijs_url(q) or "%s#p%d" % (g["url"], q["rank"]), img_of(q), e(q["brand"]), e(q["name"]), q["rank"], eur(q["price"])) for q in alts)
    body = '''<div class="wrap"><nav class="crumbs"><a href="../">Home</a> › <a href="./">Prijsverloop</a> › <a href="../%s">%s</a></nav>
<div class="ghero"><span class="kick">Prijsverloop bij bol</span><h1 class="split">%s: prijs en prijsverloop</h1><p class="intro">%s</p><p class="disc disc-top">Bevat affiliatelinks, <a href="../disclaimer.html">zo verdienen wij</a>. Alleen prijzen die wij zelf bij bol hebben gemeten, geen adviesprijzen.</p></div>
<div class="pp-top rv"><div class="pp-img">%s</div><div><div class="pp-now"><span>Nu bij bol</span><b>%s</b></div><p>%s</p><div style="display:flex;gap:10px;flex-wrap:wrap">%s</div><small class="muted">Prijs gecontroleerd op %s</small></div></div>
<h2 class="rv" style="margin-top:26px">Zo bewoog de prijs</h2><div class="pp-wrap rv">%s</div>
<h2 class="rv" style="margin-top:26px">In onze top 10's</h2><ul class="pp-in">%s</ul><p>%s</p>
<h2 class="rv" style="margin-top:26px">Alle metingen</h2><div class="tbl"><table><thead><tr><th>Datum</th><th>Prijs bij bol</th><th>Verandering</th></tr></thead><tbody>%s</tbody></table></div>
<h2 class="rv" style="margin-top:26px">Kenmerken</h2><div class="tbl"><table><tbody>%s</tbody></table></div>
<div class="pc" style="margin-top:18px"><div class="pros"><h4>Pluspunten</h4><ul>%s</ul></div><div class="cons"><h4>Minpunten</h4><ul>%s</ul></div></div><p><b>Ideaal voor:</b> %s</p>
<h2 class="rv" style="margin-top:26px">Andere modellen uit deze gids</h2><div class="rows">%s</div>
<p class="muted" style="margin:24px 0 40px">Hoe wij meten: elke dag halen wij de prijs van alle %d producten uit onze gidsen op bij bol. Een dag zonder meting vullen we niet aan. <a href="../zo-kiezen-wij.html">Zo kiezen wij</a> · <a href="../aanbiedingen/">echte prijsdalingen</a>.</p></div>''' % (
        g["url"], e(g["short"]), e(nm), e(intro), img_of(p), eur(p["price"]), e(moment), shop_a(p, g, "btn btn-buy magnet", "prijspagina") + amazon_a(p, g, "prijspagina"), e(chk_date(p, g)),
        big_chart(h), plekken, e(p["oneliner"]), trs, specs, "".join("<li>%s</li>" % e(t) for t in p["pros"]), "".join("<li>%s</li>" % e(t) for t in p["cons"]), e(p["ideal"]), alt, N_PROD)
    url = "prijs/%s.html" % x["slug"]
    prod = {"@context": "https://schema.org", "@type": "Product", "name": nm, "brand": {"@type": "Brand", "name": p["brand"]}, "description": p["oneliner"],
            "offers": {"@type": "Offer", "price": "%.2f" % p["price"], "priceCurrency": "EUR", "url": SITE + "/" + url, "seller": {"@type": "Organization", "name": "bol"}}}
    if p.get("image"): prod["image"] = p["image"]
    if re.fullmatch(r"\d{13}", k): prod["gtin13"] = k
    ld = [prod, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Prijsverloop", "item": SITE + "/prijs/"}, {"@type": "ListItem", "position": 3, "name": nm, "item": SITE + "/" + url}]}]
    tt = "%s prijs: verloop bij bol | watkoopik" % nm
    if len(tt) > 68: tt = "%s prijsverloop | watkoopik" % nm[:50].rsplit(" ", 1)[0]
    ds = ("Nu %s bij bol. Op %d dagen gemeten sinds %s: laagste %s, hoogste %s. Elke dag bijgewerkt met eigen metingen." % (eur(p["price"]), h["n"], nldate(h["first"]), eur(h["low"]), eur(h["high"])))
    page(url, tt, ds, body, extra='<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), img=p.get("image", ""))
for k, x in PRIJS.items(): prijs_page(k, x)
if PRIJS:
    _pl = sorted(PRIJS.values(), key=lambda x: (x["in"][0][0]["short"], x["p"]["rank"]))
    page("prijs/index.html", "Prijsverloop per model: eigen metingen bij bol | watkoopik", "Van %d populaire modellen uit onze top 10's zie je elke gemeten bol-prijs: laagste, hoogste en nu. Elke dag bijgewerkt." % len(PRIJS),
         '''<section style="padding-top:34px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a> › Prijsverloop</nav><span class="kick" style="margin-top:14px">Prijsverloop</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">Wat kostte dit model de afgelopen weken?</h1>
<p class="muted" style="max-width:720px">Wij meten elke dag de bol-prijs van alle producten in onze gidsen. Van de populairste modellen zie je hier elke meting: de laagste prijs, de hoogste en waar de prijs nu staat. Handig vlak voor Black Friday en de feestdagen.</p><div class="rows" style="margin-top:18px">%s</div></div></section>''' % "".join(
             '<a class="rw rv" href="%s.html"><div class="rw-img">%s</div><div><h3>%s %s</h3><small>Nu %s · %s</small></div><b>→</b></a>' % (x["slug"], img_of(x["p"]), e(x["p"]["brand"]), e(x["p"]["name"]), eur(x["p"]["price"]), e(rel_txt(hist_of(x["p"])["rel"]))) for x in _pl), root="../")

# ---------- cadeaus ----------
_cg = by_cat.get("cadeaus", [])
cad_body = '''<section style="padding-top:34px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a> › Cadeaus</nav><span class="kick" style="margin-top:14px">Sinterklaas · Kerst · Black Friday</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">De beste cadeaus van %d</h1>
<p class="muted" style="max-width:760px">%s</p><p class="muted" style="font-size:.9rem"><a href="../black-friday/">Black Friday 2026</a> · <a href="../aanbiedingen/">Echte prijsdalingen</a></p>
<div class="gl" style="margin-top:22px">%s</div>
<div class="sec-head" style="margin-top:40px"><h2>Ook vaak cadeau gegeven</h2></div><div class="gl">%s</div></div></section>''' % (
    YEAR, e(CAT_INTRO["cadeaus"]), "".join(gcard(g, "../") for g in _cg) or '<p class="muted">De cadeaugidsen verschijnen hier binnenkort.</p>', "".join(gcard(g, "../") for g in [x for x in popular if x["cat"] != "cadeaus"][:6]))
page("cadeaus/index.html", "Cadeau-ideeën %d: de beste cadeaus per budget | watkoopik" % YEAR, "Cadeaugidsen voor Sinterklaas en Kerst %d: cadeaus voor hem en haar onder 50 euro, tech-cadeaus, keukencadeaus en meer. Tien echte producten per lijst." % YEAR, cad_body, root="../",
     extra='<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "Cadeaugidsen %d" % YEAR, "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/" + x["url"], "name": x["title"]} for i, x in enumerate(_cg)]}, ensure_ascii=False))

# ---------- black friday ----------
# Toont tot en met Black Friday de best klikkende gidsen; van 27 november tot en met Cyber Monday (30 november 2026) staan de echte prijsdalingen bovenaan.
BF = datetime.date(2026, 11, 27); BF_END = datetime.date(2026, 11, 30)
bf_live = BF <= TODAY <= BF_END
bf_deals = deals_body("../", "Black Friday", "Black Friday 2026: echte prijsdalingen", "Het is Black Friday. Hieronder staan alle producten uit onze top 10's die nu minstens 10%% goedkoper zijn dan wij de dertig dagen ervoor maten. Geen adviesprijzen, alleen gemeten bol-prijzen.")
bf_body = '''<div id="bf-live"%s>%s</div><section style="padding-top:34px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a> › Black Friday</nav><span class="kick" style="margin-top:14px">Vrijdag 27 november 2026</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">Black Friday 2026: zo koop je slim</h1>
<p class="muted" style="max-width:760px">Black Friday valt dit jaar op vrijdag 27 november, Cyber Monday op 30 november. Veel kortingen zijn dan minder groot dan ze lijken, omdat de van-prijs een adviesprijs is. Wij meten elke dag de echte bol-prijs van alle %d producten in onze gidsen. Op Black Friday verschijnen op deze pagina automatisch de producten die echt goedkoper zijn geworden. Tot die tijd vind je hieronder de gidsen die nu het meest bekeken worden, zodat je vooraf weet welk model je zoekt.</p>
<p class="muted" style="font-size:.9rem"><a href="echte-kortingen-2026.html"><b>Zoveel kortingen zijn echt: onze eigen metingen</b></a> · <a href="../aanbiedingen/">Bekijk de prijsdalingen van vandaag</a> · <a href="../cadeaus/">Cadeaugidsen</a></p>
<div class="sec-head" style="margin-top:26px"><h2>Meest bekeken gidsen voor Black Friday</h2></div><div class="gl">%s</div>
<div class="sec-head" style="margin-top:34px"><h2>Cadeaus en tv's voor Sinterklaas en kerst</h2></div><div class="gl">%s</div>
<div class="guide" style="margin-top:34px"><h2>Drie tips voor Black Friday</h2><h3>Kies vooraf je model</h3><p>Lees de gids nu al en noteer je favoriet en de prijs van vandaag. Dan zie je op Black Friday meteen of een korting echt iets oplevert.</p><h3>Vergelijk met de prijs van de laatste weken</h3><p>Een korting ten opzichte van een adviesprijs zegt weinig. Op onze aanbiedingenpagina vergelijken we alleen met prijzen die wij zelf hebben gemeten.</p><h3>Let op levertijd en verkoper</h3><p>Bestel cadeaus voor Sinterklaas op tijd. Kijk op bol ook of een product door bol zelf of door een partner wordt verkocht.</p></div></div></section>
<script>(function(){var d=new Date(),s=new Date(2026,10,27),t=new Date(2026,11,1);var b=document.getElementById("bf-live");if(b&&d>=s&&d<t)b.hidden=false;})()</script>''' % (
    "" if bf_live else " hidden", bf_deals, N_PROD, "".join(gcard(g, "../") for g in popular[:12]), "".join(gcard(g, "../") for g in seizoen if g not in popular[:12]))
page("black-friday/index.html", "Black Friday 2026: echte aanbiedingen en de beste koop | watkoopik", "Black Friday 2026 valt op 27 november. Zie welke producten echt goedkoper zijn (gemeten met dagelijkse bol-prijzen) en welke gidsen het meest bekeken worden.", bf_body, root="../")

# ---------- Black Friday: zoveel kortingen zijn echt (sinds 5 nov 2026, groeimotor N1) ----------
# Alleen eigen dagelijkse bol-metingen (ph). Per uniek product (EAN): huidige prijs tegenover de mediaan van de metingen
# in de 30 dagen ervoor (de dag van de huidige meting telt niet mee). Minstens 10 meetdagen. Verschillen van meer dan
# 60% zijn vrijwel altijd een andere verkoper of een onderdeel en tellen niet mee. Dagelijks bijgewerkt tot 1 december.
def _med(v):
    v = sorted(v); n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
def bf_ref(ph, day, cur=None):
    """Mediaan van de metingen in de 30 dagen vóór day (day zelf niet meegeteld)."""
    start = (datetime.date.fromisoformat(day) - datetime.timedelta(days=30)).isoformat()
    prev = [ph[d] for d in ph if start <= d < day]
    return _med(prev) if len(prev) >= 5 else None
def bf_strict(p):
    """Strengste toets (N28): huidige prijs tegenover de laagste meting in de 30 dagen voordat de huidige prijs inging."""
    ph = p["ph"]; days = sorted(ph); cur = p["price"]; i = len(days)
    while i > 0 and abs(ph[days[i - 1]] - cur) < 0.01: i -= 1
    if i == 0: return None
    since = days[i] if i < len(days) else days[-1]
    start = (datetime.date.fromisoformat(since) - datetime.timedelta(days=30)).isoformat()
    prev = [ph[d] for d in days[:i] if d >= start]
    return cur / min(prev) - 1 if len(prev) >= 2 else None
BFX = []; _bfseen = set()
for g in guides:
    for p in g["products"]:
        ph = p.get("ph") or {}
        key = str(p.get("ean") or p["brand"] + p["name"])
        if key in _bfseen or len(ph) < 10 or not p.get("price"): continue
        _bfseen.add(key)
        last = max(ph); ref = bf_ref(ph, last)
        if not ref: continue
        ch = p["price"] / ref - 1
        if abs(ch) > 0.60: continue
        BFX.append({"g": g, "p": p, "ref": ref, "ch": ch, "n": len(ph), "first": min(ph), "st": bf_strict(p)})
def _bucket(ch): return "echt" if ch <= -0.10 else "iets" if ch <= -0.02 else "duur" if ch >= 0.02 else "gelijk"
BF_N = len(BFX)
BF_CNT = {k: sum(1 for x in BFX if _bucket(x["ch"]) == k) for k in ("echt", "iets", "gelijk", "duur")}
BF_AVG = sum(x["ch"] for x in BFX) / BF_N if BF_N else 0
BF_FIRST = min((x["first"] for x in BFX), default=TODAY.isoformat())
def pct(n, t=None): return "%d%%" % round(100.0 * n / (t or BF_N or 1))
# Verloop per dag: aandeel producten dat op die dag minstens 10% onder of 2% boven zijn mediaan van de 30 dagen ervoor stond
_alld = sorted({d for x in BFX for d in x["p"]["ph"]})
BF_DAYS = []
for day in _alld:
    lo = hi = n = 0
    for x in BFX:
        ph = x["p"]["ph"]
        if day not in ph: continue
        r = bf_ref(ph, day)
        if not r: continue
        c = ph[day] / r - 1
        if abs(c) > 0.60: continue
        n += 1; lo += c <= -0.10; hi += c >= 0.02
    if n >= 200: BF_DAYS.append((day, n, lo / n, hi / n))
def bf_chart():
    if len(BF_DAYS) < 3: return ""
    w, ht, pad = 640, 180, 28; top = max(max(a, b) for _, _, a, b in BF_DAYS) or 0.01; top = max(0.05, top * 1.15)
    bw = (w - pad) / len(BF_DAYS)
    bars = "".join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#0f5c4c"><title>%s: %s minstens 10%% goedkoper</title></rect><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#d4a52a"><title>%s: %s duurder</title></rect>' % (
        pad + i * bw + 1, ht - 20 - (ht - 30) * a / top, bw / 2 - 1.5, (ht - 30) * a / top, nldate(d), pct(round(a * 1000), 1000),
        pad + i * bw + bw / 2, ht - 20 - (ht - 30) * b / top, bw / 2 - 1.5, (ht - 30) * b / top, nldate(d), pct(round(b * 1000), 1000)) for i, (d, n, a, b) in enumerate(BF_DAYS))
    lbl = "".join('<text x="%.1f" y="%d" font-size="10" fill="currentColor" text-anchor="middle">%s</text>' % (pad + i * bw + bw / 2, ht - 6, d[8:10].lstrip("0") + "/" + d[5:7].lstrip("0")) for i, (d, n, a, b) in enumerate(BF_DAYS) if i % 3 == 0 or i == len(BF_DAYS) - 1)
    ax = '<text x="0" y="14" font-size="10" fill="currentColor">%s</text><text x="0" y="%d" font-size="10" fill="currentColor">0%%</text><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity=".25"/>' % (pct(round(top * 1000), 1000), ht - 20, pad, ht - 20, w, ht - 20)
    return '<figure class="bf-chart"><svg viewBox="0 0 %d %d" role="img" aria-label="Aandeel producten per dag dat echt goedkoper of duurder was">%s%s%s</svg><figcaption><span class="k1"></span>minstens 10%% goedkoper dan de 30 dagen ervoor <span class="k2"></span>duurder (2%% of meer)</figcaption></figure>' % (w, ht, ax, bars, lbl)
def bf_row(x, root="../"):
    g, p = x["g"], x["p"]
    return '<tr><td class="nm"><a href="%s%s#p%d">%s %s</a><small>%s</small></td><td>%s</td><td><b>%s</b></td><td>%s%d%%</td></tr>' % (
        root, g["url"], p["rank"], e(p["brand"]), e(p["name"]), e(g["short"]), eur(round(x["ref"], 2)), eur(p["price"]), "+" if x["ch"] > 0 else "", round(x["ch"] * 100))
def bf_table(rows, cap):
    return '<div class="tbl"><table><caption class="sr">%s</caption><thead><tr><th>Product</th><th>Mediaan 30 dagen</th><th>Nu</th><th>Verschil</th></tr></thead><tbody>%s</tbody></table></div>' % (e(cap), "".join(bf_row(x) for x in rows))
if BF_N:
    _drops = sorted([x for x in BFX if x["ch"] <= -0.10], key=lambda x: x["ch"])
    _rises = sorted([x for x in BFX if x["ch"] >= 0.05], key=lambda x: -x["ch"])
    _cats = []
    for c, (cn, _) in CATS.items():
        xs = [x for x in BFX if x["g"]["cat"] == c]
        if len(xs) < 20: continue
        _cats.append((cn, len(xs), sum(1 for x in xs if x["ch"] <= -0.10), sum(1 for x in xs if x["ch"] <= -0.02), sum(1 for x in xs if x["ch"] >= 0.02), sum(x["ch"] for x in xs) / len(xs), min(xs, key=lambda x: x["ch"])))
    _cats.sort(key=lambda c: c[5])
    cat_rows = "".join('<tr><td class="nm">%s</td><td>%d</td><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s%s%%</td><td>%s</td></tr>' % (
        e(cn), n, pct(echt, n), pct(goed, n), pct(duur, n), "+" if avg > 0.0005 else "", ("%.1f" % (avg * 100)).replace(".", ",").replace("-0,0", "0,0"), ('<a href="../%s#p%d">%s %s</a> (%d%%)' % (b["g"]["url"], b["p"]["rank"], e(b["p"]["brand"]), e(b["p"]["name"]), round(b["ch"] * 100))) if b["ch"] <= -0.05 else "geen daling van 5% of meer")
        for cn, n, echt, goed, duur, avg, b in _cats)
    _goed = BF_CNT["echt"] + BF_CNT["iets"]
    _streng = sorted([x for x in _drops if x["st"] is not None and x["st"] <= -0.10], key=lambda x: x["ch"])
    _jojo = [x for x in _drops if x["st"] is not None and x["st"] >= -0.001]
    _kern = "Van de %d producten die wij sinds %s elke dag bij bol meten, is %s nu minstens 10%% goedkoper dan in de dertig dagen ervoor. Nog eens %s is iets goedkoper (2 tot 10%%), %s kost ongeveer hetzelfde en %s is juist duurder geworden. Gemiddeld ligt de prijs %s%% %s de mediaan van de afgelopen maand. Leggen we de strengste lat aan, minstens 10%% onder de laagste prijs van de dertig dagen ervoor, dan blijft %s over." % (
        BF_N, nldate(BF_FIRST), pct(BF_CNT["echt"]), pct(BF_CNT["iets"]), pct(BF_CNT["gelijk"]), pct(BF_CNT["duur"]), ("%.1f" % (abs(BF_AVG) * 100)).replace(".", ","), "onder" if BF_AVG < 0 else "boven", pct(len(_streng)))
    tiles = "".join('<div class="bf-t"><b>%s</b><span>%s</span></div>' % (a, b) for a, b in [
        (pct(BF_CNT["echt"]), "minstens 10% goedkoper"), (pct(BF_CNT["iets"]), "2 tot 10% goedkoper"), (pct(BF_CNT["gelijk"]), "ongeveer gelijk"), (pct(BF_CNT["duur"]), "duurder geworden")])
    bfe_faq = [
        ("Hoeveel Black Friday-kortingen bij bol zijn echt?", "Wij vergelijken de prijs van vandaag met de mediaan van wat wij de dertig dagen ervoor zelf maten, niet met een adviesprijs. Op %s was %s van de %d gemeten producten minstens 10%% goedkoper dan die mediaan. Volgens de strengste toets, minstens 10%% onder de laagste prijs van de dertig dagen ervoor, was dat %s. Die cijfers werken we elke dag bij tot en met 1 december." % (nldate(TODAY.isoformat()), pct(BF_CNT["echt"]), BF_N, pct(len(_streng)))),
        ("Wat is een jojoprijs?", "Een prijs die heen en weer springt tussen twee bedragen, bijvoorbeeld doordat de verkoper wisselt. Zo'n product lijkt vandaag in de aanbieding, maar kostte kort geleden al hetzelfde of minder. Op %s gold dat voor %d van de %d producten die minstens 10%% onder hun mediaan stonden. Daarom tonen wij als aanbieding alleen producten die goedkoper zijn dan hun laagste prijs van de dertig dagen ervoor." % (nldate(TODAY.isoformat()), len(_jojo), len(_drops))),
        ("Worden prijzen vlak voor Black Friday verhoogd?", "Bij een deel van de producten wel. Op %s was %s van de producten minstens 2%% duurder dan de mediaan van de maand ervoor. Bij %d producten was dat zelfs 5%% of meer. Een korting op Black Friday vergelijk je daarom het best met de prijs van de weken ervoor." % (nldate(TODAY.isoformat()), pct(BF_CNT["duur"]), len(_rises))),
        ("Hoe meten jullie de prijzen?", "Elke dag halen wij via de officiële bol-koppeling de prijs op van alle producten in onze top 10-gidsen. Er wordt niets geschat of aangevuld. Een product telt mee bij minstens 10 meetdagen; verschillen van meer dan 60%% laten we weg, omdat dat bijna altijd een andere verkoper of een los onderdeel is."),
        ("Mag ik deze cijfers gebruiken?", "Ja. Gebruik de cijfers gerust in een artikel of op een forum met een bronvermelding en een link naar deze pagina. De volledige lijst per product staat in het CSV-bestand onderaan."),
    ]
    _csv = ["product;merk;gids;categorie;mediaan_30_dagen;prijs_nu;verschil_procent;meetdagen;meet_sinds;verschil_tov_laagste_30_dagen_procent"]
    for x in sorted(BFX, key=lambda x: x["ch"]):
        _csv.append(";".join([x["p"]["name"].replace(";", ","), x["p"]["brand"].replace(";", ","), SITE + "/" + x["g"]["url"], CATS.get(x["g"]["cat"], (x["g"]["cat"],))[0], ("%.2f" % x["ref"]).replace(".", ","), ("%.2f" % x["p"]["price"]).replace(".", ","), ("%.1f" % (x["ch"] * 100)).replace(".", ","), str(x["n"]), x["first"], ("%.1f" % (x["st"] * 100)).replace(".", ",") if x["st"] is not None else ""]))
    wr("black-friday/echte-kortingen-2026.csv", "﻿" + "\n".join(_csv) + "\n")
    bfe_body = '''<section style="padding-top:34px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a> › <a href="./">Black Friday</a> › Echte kortingen</nav><span class="kick" style="margin-top:14px">Eigen prijsmetingen · bijgewerkt %s</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">Black Friday 2026: zoveel kortingen zijn echt</h1>
<p class="lead" style="max-width:760px">%s</p>
<div class="bf-tiles">%s</div>
<div class="guide" style="margin-top:30px"><h2>Zo bewegen de prijzen per dag</h2><p>Per dag het aandeel producten dat minstens 10%% onder zijn mediaan van de dertig dagen ervoor stond (groen) en het aandeel dat juist duurder was (goud). Zo zie je of de kortingen richting Black Friday op 27 november echt toenemen.</p>%s
<h2>Per categorie</h2><p>Gesorteerd van de grootste gemiddelde daling naar de kleinste. Alleen categorieën met minstens 20 gemeten producten.</p>
<div class="tbl"><table><thead><tr><th>Categorie</th><th>Producten</th><th>10%%+ goedkoper</th><th>2%%+ goedkoper</th><th>Duurder</th><th>Gemiddeld</th><th>Grootste daling</th></tr></thead><tbody>%s</tbody></table></div>
<h2>De grootste echte prijsdalingen</h2><p>%s</p>%s
<h2>Nu duurder dan de weken ervoor</h2><p>%s</p>%s
<h2>Zo hebben we gemeten</h2><p>Elke dag halen wij via de officiële bol-koppeling de prijs op van alle %d producten in onze top 10-gidsen. Voor deze pagina telt elk product één keer mee, ook als het in meerdere gidsen staat. Het moet wel minstens 10 meetdagen hebben. De huidige prijs vergelijken we met de mediaan van onze eigen metingen in de dertig dagen ervoor. Een mediaan is minder gevoelig voor één uitschieter dan een gemiddelde. Daarnaast rekenen we de strengste toets uit: de huidige prijs tegenover de laagste meting in de dertig dagen voordat die prijs inging. Zo vallen prijzen die heen en weer springen af. Verschillen van meer dan 60%% laten we weg: dat is bijna altijd een andere verkoper of een los onderdeel. We gebruiken geen adviesprijzen of van-prijzen van winkels. We meten sinds %s, dus de eerste weken is de vergelijkingsperiode korter dan dertig dagen. Deze pagina wordt elke dag opnieuw berekend tot en met 1 december 2026.</p>
<p>Journalist of blogger? De cijfers zijn vrij te gebruiken met een bronvermelding en een link naar deze pagina. <a href="echte-kortingen-2026.csv" download>Download alle %d producten als CSV</a>.</p>
<h2>Veelgestelde vragen</h2>%s
<p class="muted" style="font-size:.9rem;margin-top:24px"><a href="../aanbiedingen/">Alle echte prijsdalingen van vandaag</a> · <a href="./">Black Friday 2026: zo koop je slim</a> · <a href="../cadeaus/">Cadeaugidsen</a> · Wij ontvangen mogelijk een vergoeding als je via onze links koopt.</p></div></div></section>''' % (
        nldate(TODAY.isoformat()), e(_kern), tiles, bf_chart(), cat_rows,
        "Producten die nu minstens 10%% goedkoper zijn dan hun mediaan van de dertig dagen ervoor: %d producten halen dat. Bij %d daarvan stond de prijs in die dertig dagen al eens even laag of lager. Dat zijn jojoprijzen die heen en weer springen tussen twee bedragen. %d producten zijn ook minstens 10%% goedkoper dan hun laagste prijs van de dertig dagen ervoor, dezelfde maat als de Europese regel voor van-prijzen. Hieronder de 15 grootste daarvan." % (len(_drops), len(_jojo), len(_streng)) if _drops else "Op dit moment is geen enkel product minstens 10% goedkoper dan de dertig dagen ervoor.",
        bf_table(_streng[:15], "Grootste prijsdalingen") if _streng else "",
        "Producten die nu minstens 5%% duurder zijn dan hun mediaan van de dertig dagen ervoor. Dat zijn er %d; hieronder de 10 grootste stijgers. Zie je die op Black Friday terug met korting, dan is die korting kleiner dan hij lijkt." % len(_rises) if _rises else "Op dit moment is geen enkel product 5% of meer duurder dan de dertig dagen ervoor.",
        bf_table(_rises[:10], "Grootste prijsstijgingen") if _rises else "",
        N_PROD, nldate(BF_FIRST), BF_N, "".join("<h3>%s</h3><p>%s</p>" % (e(q), e(a)) for q, a in bfe_faq))
    bfe_ld = [{"@context": "https://schema.org", "@type": "Dataset", "name": "Echte Black Friday-kortingen bij bol 2026", "description": "Dagelijkse bol-prijzen van %d producten uit de top 10-gidsen van watkoopik, vergeleken met de mediaan van de 30 dagen ervoor." % BF_N,
               "url": SITE + "/black-friday/echte-kortingen-2026.html", "creator": {"@type": "Organization", "name": "watkoopik", "url": SITE}, "license": "https://creativecommons.org/licenses/by/4.0/", "isAccessibleForFree": True,
               "temporalCoverage": "%s/%s" % (BF_FIRST, TODAY.isoformat()), "dateModified": TODAY.isoformat(), "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": SITE + "/black-friday/echte-kortingen-2026.csv"}]},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in bfe_faq]}]
    page("black-friday/echte-kortingen-2026.html", "Black Friday 2026: zoveel kortingen zijn echt (eigen metingen) | watkoopik",
         "%s van %d producten bij bol is nu echt 10%% of meer goedkoper dan de maand ervoor, %s werd juist duurder. Dagelijkse eigen prijsmetingen tot Black Friday." % (pct(BF_CNT["echt"]), BF_N, pct(BF_CNT["duur"])),
         bfe_body, root="../", extra="".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in bfe_ld))
    # Persbericht met de cijfers van vandaag (groeimotor N29, 12 nov 2026). Staat buiten de site (groeimotor/persbericht.md),
    # wordt bij elke build herschreven en nooit gepubliceerd of verstuurd: Nick verstuurt zelf.
    _pdir = os.path.join(ROOT, "..", "groeimotor")
    if os.path.isdir(_pdir) and TODAY <= datetime.date(2026, 12, 1):
        try:
            _pp = lambda n, t=None: pct(n, t).replace("%", " procent")
            _dbf = (datetime.date(2026, 11, 27) - TODAY).days
            _wanneer = ("%d dagen voor Black Friday" % _dbf) if _dbf > 1 else "een dag voor Black Friday" if _dbf == 1 else "op Black Friday" if _dbf == 0 else "in de dagen na Black Friday"
            _url = SITE + "/black-friday/echte-kortingen-2026.html"
            _cg = max(_cats, key=lambda c: c[3] / c[1]) if _cats else None
            _cd = max(_cats, key=lambda c: c[4] / c[1]) if _cats else None
            _catzin = ("De verschillen per categorie zijn groot. In %s is %s van de producten minstens 2 procent goedkoper geworden. In %s is %s juist duurder dan de maand ervoor.\n\n" % (
                _cg[0].lower(), _pp(_cg[3], _cg[1]), _cd[0].lower(), _pp(_cd[4], _cd[1]))) if _cg and _cd and _cg[0] != _cd[0] else ""
            _top = (" De grootste stijger staat nu %d procent boven zijn prijs van de weken ervoor." % round(_rises[0]["ch"] * 100)) if _rises else ""
            _jz = ("Opvallend zijn de jojoprijzen. Van de %d producten die minstens 10 procent onder hun mediaan staan, kostten er %d in de dertig dagen ervoor al eens hetzelfde of minder. Zo'n prijs springt heen en weer tussen twee bedragen, vaak doordat de verkoper wisselt, en lijkt daardoor telkens opnieuw een aanbieding.\n\n" % (len(_drops), len(_jojo))) if _jojo else ""
            _pers = """# Persbericht Black Friday (cijfers van %s)

Dit bestand wordt bij elke build van watkoopik herschreven met de cijfers van die dag. Niets is verstuurd. De pagina met dezelfde cijfers: %s

## Persbericht

**Maar %s van de producten bij bol is %s echt goedkoper**

Vergelijkingssite watkoopik.nl meet sinds %s elke dag de prijs van de producten in zijn top 10-gidsen bij bol. Uit die metingen blijkt dat %s maar %s van de %d gemeten producten echt goedkoper is: minstens 10 procent onder de laagste prijs van de dertig dagen ervoor. Vergeleken met de mediaanprijs van die dertig dagen haalt %s een daling van 10 procent of meer. Tegelijk is %s van de producten minstens 2 procent duurder geworden. Bij %d producten ligt de prijs nu 5 procent of meer boven die van de weken ervoor.%s

%s"Een korting op Black Friday zegt alleen iets als je weet wat een product de weken ervoor kostte", zegt Nick van Straaten van watkoopik. "Wie nu een model kiest en de prijs noteert, ziet op 27 november meteen of een aanbieding echt iets oplevert."

%swatkoopik vergelijkt de prijs van vandaag met de eigen metingen van de dertig dagen ervoor, niet met een adviesprijs. Verschillen van meer dan 60 procent, vaak een andere verkoper, tellen niet mee. De cijfers worden tot en met 1 december dagelijks bijgewerkt. De volledige dataset staat als CSV op de site en mag met bronvermelding worden gebruikt.

Meer informatie: %s · hallo@watkoopik.nl

## 5 korte pitches (zelf de contactweg zoeken)

- Tweakers (nieuwstips): "Eigen dagprijzen van %d producten bij bol: %s is %s echt goedkoper dan de laagste prijs van de maand ervoor, %s is duurder geworden. Dataset als CSV: %s"
- Radar (KRO-NCRV): "Kijkers vragen elk jaar of Black Friday-kortingen echt zijn. Wij meten sinds %s elke dag de bol-prijs van %d producten. Bij %d producten ging de prijs de afgelopen weken 5 procent of meer omhoog. Graag lever ik op 27 november de cijfers van die dag."
- RTL Nieuws (consument): "Nieuwe cijfers voor Black Friday: %s van de producten bij bol is nu echt 10 procent goedkoper dan de maand ervoor, %s is juist duurder. Dagelijks bijgewerkt, ook op de dag zelf."
- NU.nl (economie/tech): "Korte datastory voor de Black Friday-week: per categorie hoeveel producten echt goedkoper of duurder zijn, op basis van eigen dagelijkse prijsmetingen bij bol. Grafiek en CSV vrij te gebruiken."
- Bright: "Jojoprijzen bij bol: %d van de %d producten die nu in de aanbieding lijken, kostten de afgelopen maand al eens hetzelfde of minder. Lijst per model met prijs nu en laagste prijs: %s"
""" % (nldate(TODAY.isoformat()), _url, _pp(len(_streng)), _wanneer, nldate(BF_FIRST), _wanneer, _pp(len(_streng)), BF_N, _pp(BF_CNT["echt"]), _pp(BF_CNT["duur"]), len(_rises), _top,
       _jz, _catzin, _url, BF_N, _pp(len(_streng)), _wanneer, _pp(BF_CNT["duur"]), _url, nldate(BF_FIRST), BF_N, len(_rises), _pp(len(_streng)), _pp(BF_CNT["duur"]), len(_jojo), len(_drops), _url)
            open(os.path.join(_pdir, "persbericht.md"), "w", encoding="utf-8").write(_pers)
            print("Persbericht bijgewerkt: groeimotor/persbericht.md")
        except Exception as ex:
            print("Persbericht overgeslagen: %s" % ex)

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

# ---------- familie-overzichten "Welke X kopen?" (sinds 4 nov 2026) ----------
# Per familie: snelkiezer met de nr. 1 en slimste koop van elke gids (dagprijzen), alle gidskaarten en een FAQ uit de data.
def lijst(xs): return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " en " + xs[-1]
def hub_page(c):
    ms = c["members"]; main = ms[0]; top = win(main); bv = best_value(main); n = len(ms)
    allp = [p for g in ms for p in g["products"]]
    prices = sorted(p["price"] for p in allp)
    good = sorted((p for p in allp if p["score"] >= 8), key=lambda p: p["price"])
    chk = max((p.get("synced") or g.get("updated", "")) for g in ms for p in g["products"])
    rows = "".join('<tr><td class="nm"><a href="../%s"><b>%s</b></a></td><td>%s %s</td><td><b>%s</b></td><td>%s %s</td><td><b>%s</b></td><td><a class="more" href="../%s">Top 10 →</a></td></tr>' % (
        g["url"], e(g["short"]), e(win(g)["brand"]), e(win(g)["name"]), eur(win(g)["price"]), e(best_value(g)["brand"]), e(best_value(g)["name"]), eur(best_value(g)["price"]), g["url"]) for g in ms)
    faq = []
    if c.get("faq", True):
        faq = [("Wat is de beste %s van %d?" % (c["enkel"], YEAR), "In onze vergelijking is dat de %s %s voor %s. Dat model staat op nummer 1 in onze gids %s. Zoek je iets specifieks, kies dan hierboven de gids die bij jouw situatie past." % (top["brand"], top["name"], eur(top["price"]), main["title"].lower())),
               ("%s %s is de slimste koop?" % (welk(c), c["enkel"]), "De %s %s voor %s biedt volgens onze vergelijking de meeste kwaliteit per euro. Je vindt hem in onze gids %s." % (bv["brand"], bv["name"], eur(bv["price"]), main["title"].lower()))]
        if good:
            faq.append(("Wat kost een goede %s?" % c["enkel"], "In onze %d gidsen kost de goedkoopste aanrader met een score van 8 of hoger %s, de %s %s. De helft van alle %d modellen die wij vergelijken kost tussen %s en %s. De duurste topmodellen kosten %s." % (
                n, eur(good[0]["price"]), good[0]["brand"], good[0]["name"], len(allp), eur(prices[len(prices) // 4]), eur(prices[3 * len(prices) // 4]), eur(prices[-1]))))
        faq.append(("Hoe kiezen jullie de beste %s?" % c["meervoud"], "Per gids vergelijken we tien modellen op prestaties, prijs-kwaliteit, betrouwbaarheid en gebruiksgemak, op basis van specificaties en duizenden kopersreviews. Merken kunnen geen plek kopen. De prijzen controleren we elke dag bij bol."))
    others = [x for x in HUBS if x is not c and (x["cat"] == c["cat"])] or [x for x in HUBS if x is not c][:8]
    h1 = (c.get("h1") or "").replace("{YEAR}", str(YEAR)) or '%s %s <span class="grad">kopen in %d?</span>' % (welk(c), e(c["enkel"]), YEAR)
    catk = c["cat"] if c["cat"] in CATS else main["cat"]
    body = '''<section data-hue="1" style="padding-top:20px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a> › <a href="../categorie/%s.html">%s</a> › %s</nav>
<span class="kick" style="margin-top:14px">Alle gidsen · %s</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3.2rem)">%s</h1>
<p class="muted" style="max-width:760px">%s</p><p class="muted" style="font-size:.9rem">%d gidsen · %d modellen vergeleken · prijzen gecontroleerd op %s</p>
<h2 class="rv" style="margin-top:26px">Snel kiezen: per situatie de winnaar</h2>
<div class="tbl hubtbl rv"><table><thead><tr><th>Je zoekt</th><th>Beste keuze</th><th>Prijs</th><th>Slimste koop</th><th>Prijs</th><th><span class="sr">Gids</span></th></tr></thead><tbody>%s</tbody></table></div>
<h2 class="rv">Alle %d gidsen voor %s</h2><div class="gl" style="margin-top:14px">%s</div>
%s
<div class="sec-head" style="margin-top:40px"><h2>Meer overzichten</h2><a class="more" href="../categorie/%s.html">Alle %s →</a></div>%s
</div></section>''' % (catk, CATS[catk][0], e(cap1(c["meervoud"])), e(c["meervoud"]), h1, e(c.get("intro") or "Hieronder staan al onze gidsen voor %s naast elkaar, met per gids de beste keuze en de slimste koop." % c["meervoud"]),
        n, len(allp), e(nldate(chk)), rows, n, e(c["meervoud"]), "".join(gcard(g, "../") for g in ms),
        ('<div class="faq rv" id="faq" style="margin-top:34px"><h2>Veelgestelde vragen</h2>%s</div>' % "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q), e(a)) for q, a in faq)) if faq else "",
        catk, CATS[catk][0].lower(), hub_chips(others, "../"))
    url_abs = SITE + "/" + c["hub"]
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": CATS[catk][0], "item": SITE + "/categorie/%s.html" % catk}, {"@type": "ListItem", "position": 3, "name": cap1(c["meervoud"]), "item": url_abs}]},
          {"@context": "https://schema.org", "@type": "ItemList", "name": hub_q(c), "url": url_abs, "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/" + g["url"], "name": g["title"]} for i, g in enumerate(ms)]}]
    if faq: ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    title = (c.get("title") or "%s %s kopen in {YEAR}? {n} gidsen op een rij | watkoopik" % (welk(c), c["enkel"])).replace("{YEAR}", str(YEAR)).replace("{n}", str(n))
    desc = "Onze nr. 1: %s %s (%s). Bekijk alle %d gidsen voor %s naast elkaar: %s. Met per gids de beste keuze en de slimste koop." % (top["brand"], top["name"], eur(top["price"]), n, c["meervoud"], lijst([low1(g["short"]) for g in ms[:4]]))
    page(c["hub"], title, desc, body, extra="".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld), img=og_img(main, top))
for c in HUBS: hub_page(c)

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
<p>Daarom maken we top 10-lijsten: precies tien modellen die ertoe doen, met eerlijke plus- en minpunten en voor wie elk product geschikt is. watkoopik is onderdeel van 4NEON en werkt onafhankelijk van merken en winkels.</p>
<h2 id="nick">Wie zit erachter</h2>
<p>watkoopik is opgezet door Nick van Straaten. Hij is de eindredacteur: hij leest de gidsen na en past ze aan als iets niet klopt of beter kan. Producten testen we niet zelf in een testlab. We zetten per productsoort tien modellen naast elkaar op specificaties, prijs en de ervaringen van kopers. De prijzen meten we elke dag bij bol, zodat je ziet welke korting echt is.</p>
<p>Zie je een fout of mis je een model? Laat het weten via het <a href="contact.html">contactformulier</a>.</p>''')
prose("contact.html", "Contact", "Neem contact op met watkoopik.", '''<span class="kick">Contact</span><h1 class="split" style="font-size:clamp(1.9rem,5vw,3rem)">Vraag, tip of fout gezien?</h1>
<form action="https://formsubmit.co/hallo@watkoopik.nl" method="POST" style="display:grid;gap:12px;max-width:520px;margin-top:16px"><input type="hidden" name="_subject" value="Contact via watkoopik.nl"><input type="text" name="_honey" style="display:none">
<input name="naam" placeholder="Je naam" required style="padding:13px 16px;border:1.5px solid var(--line);border-radius:14px;font:inherit"><input type="email" name="email" placeholder="Je e-mailadres" required style="padding:13px 16px;border:1.5px solid var(--line);border-radius:14px;font:inherit"><textarea name="bericht" rows="6" placeholder="Je bericht" required style="padding:13px 16px;border:1.5px solid var(--line);border-radius:14px;font:inherit"></textarea><button class="btn btn-purple" type="submit">Versturen</button></form>''')
prose("disclaimer.html", "Affiliate-disclaimer", "Hoe watkoopik geld verdient.", '''<h1 style="font-size:2rem">Affiliate-disclaimer</h1><p>watkoopik neemt deel aan het bol Partnerprogramma en aan het Amazon Associates-programma. Als Amazon-partner verdienen wij aan kwalificerende aankopen. Koop je via een link op onze site, dan kunnen wij een vergoeding ontvangen. De prijs die jij betaalt verandert niet. Deze vergoeding heeft geen invloed op de volgorde van onze lijsten. Prijzen zijn indicatief; de actuele winkelprijs is leidend.</p>''')
prose("privacy.html", "Privacy", "Privacybeleid van watkoopik.", '''<h1 style="font-size:2rem">Privacy en cookies</h1><p>Wij plaatsen geen volgcookies. Bezoekersstatistieken meten we anoniem en zonder cookies. Gegevens uit het contactformulier gebruiken we alleen om te reageren. Klik je door naar een winkel, dan geldt het privacybeleid van die winkel. Vragen: <a href="mailto:hallo@watkoopik.nl">hallo@watkoopik.nl</a>.</p>''')
page("404.html", "Niet gevonden | watkoopik", "Pagina niet gevonden.", '<section style="padding-top:34px"><div class="wrap prose"><h1 style="font-size:2rem">Deze pagina bestaat niet</h1><p>Zoek hieronder of bekijk <a href="/gidsen.html">alle gidsen</a>.</p>' + searchbox() + '</div></section>', root="/")

prose("bedankt.html", "Bedankt", "Bedankt voor je bericht.", '<h1 style="font-size:2rem">Bedankt!</h1><p>We hebben je bericht ontvangen en reageren binnen twee werkdagen. <a href="./">Terug naar home</a>.</p>')
wr("stats.html", '<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=https://cloud.umami.is/share/sSKhb6j4KMk4E28R/watkoopik.nl"><title>Statistieken</title></head><body><a href="https://cloud.umami.is/share/sSKhb6j4KMk4E28R/watkoopik.nl">Naar het dashboard</a></body></html>')
# lastmod volgt echte wijzigingen (nieuwste gids), niet de bouwdatum, zodat Google het signaal blijft vertrouwen
LAST = max(gmod(g) for g in guides)
urls = [("", LAST, "1.0"), ("gidsen.html", LAST, "0.8"), ("aanbiedingen/", TODAY.isoformat(), "0.8"), ("keuzehulp.html", LAST, "0.7"), ("slimste-koop.html", LAST, "0.7"),
        ("zo-kiezen-wij.html", "2026-10-13", "0.4"), ("over-ons.html", "2026-10-13", "0.3"), ("contact.html", "2026-10-13", "0.3")]
urls += [("categorie/%s.html" % k if k != "cadeaus" else "cadeaus/", max(gmod(g) for g in by_cat[k]), "0.7") for k in CATS if by_cat.get(k)]
urls += [("black-friday/", TODAY.isoformat(), "0.8")] + ([("black-friday/echte-kortingen-2026.html", TODAY.isoformat(), "0.8")] if BF_N else []) + [("vs/%s.html" % v["slug"], v["updated"], "0.6") for v in VS_PAGES]
urls += [(c["hub"], max(gmod(g) for g in c["members"]), "0.8") for c in HUBS]
urls += [(g["url"], gmod(g), "0.9") for g in guides if g["url"] not in NOINDEX]
def _pp_mod(x):  # lastmod = laatste dag dat de gemeten prijs veranderde (of de gids bijgewerkt werd)
    h = hist_of(x["p"]); d = h["first"]
    for i in range(1, len(h["vals"])):
        if abs(h["vals"][i] - h["vals"][i - 1]) >= 0.01: d = h["days"][i]
    return max(d, x["in"][0][0].get("updated", d))
urls += ([("prijs/", max(_pp_mod(x) for x in PRIJS.values()), "0.6")] + [("prijs/%s.html" % x["slug"], _pp_mod(x), "0.6") for x in PRIJS.values()]) if PRIJS else []
wr("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n" % (SITE, u, d, pr) for u, d, pr in urls) + "</urlset>\n")

# ---------- assets ----------
wr("style.css", rd("style.css")); wr("app.js", rd("app.js")); wr("favicon.svg", FAVICON)
for n in THEME_CSS: wr(n + ".css", rd(n + ".css"))
if THEME == "green": wr("favicon.svg", FAVICON.replace("#5b3fd6", "#0f5c4c"))
wr("CNAME", "watkoopik.com\n" if PREVIEW else "watkoopik.nl\n"); wr(".nojekyll", "")
wr("robots.txt", "User-agent: *\nDisallow: /\n" if PREVIEW else "User-agent: *\nAllow: /\nDisallow: /stats.html\nSitemap: %s/sitemap.xml\n" % SITE)
wr("search.json", json.dumps([{"t": g["title"], "u": g["url"], "c": CATS[g["cat"]][0], "w": "%s %s" % (win(g)["brand"], win(g)["name"]), "i": win(g).get("image", ""),
    "k": " ".join([g.get("seo", ""), g["query"], g["short"]] + g.get("keywords", []) + ["%s %s" % (p["brand"], p["name"]) for p in g["products"]])} for g in guides], ensure_ascii=False))
# llms.txt: compacte index voor AI-zoekmachines (chatgpt.com stuurt sinds 19 okt bezoekers), per categorie gids, nr. 1 en slimste koop
if not PREVIEW:
    L = ["# watkoopik.nl", "", "> Onafhankelijke Nederlandse top 10-koopgidsen. Per productsoort tien modellen vergeleken op specificaties, prijs en reviews, met plus- en minpunten, een koopgids en veelgestelde vragen. Prijzen zijn indicatief en worden dagelijks bij bol bijgewerkt.", "",
         "- [Alle gidsen](%s/gidsen.html)" % SITE, "- [Zo kiezen wij](%s/zo-kiezen-wij.html): werkwijze en hoe we geld verdienen" % SITE, "", "## Overzichten per productfamilie", ""]
    L += ["- [%s](%s/%s): %d gidsen, nr. 1 %s %s" % (hub_q(c), SITE, c["hub"], len(c["members"]), win(c["members"][0])["brand"], win(c["members"][0])["name"]) for c in HUBS] + [""]
    for k in CATS:
        if not by_cat.get(k): continue
        L += ["## %s" % CATS[k][0], ""]
        for g in sorted(by_cat[k], key=lambda x: x["title"]):
            t = win(g); bv = next((p for p in g["products"] if p.get("label") == "Beste prijs-kwaliteit"), None)
            s = "- [%s](%s/%s): nr. 1 %s %s (%s)" % (g["title"], SITE, g["url"], t["brand"], t["name"], eur(t["price"]))
            if bv and bv is not t: s += "; slimste koop %s %s (%s)" % (bv["brand"], bv["name"], eur(bv["price"]))
            L.append(s + "; bijgewerkt %s" % gmod(g))
        L.append("")
    txt = "\n".join(L); check(txt, "llms.txt"); wr("llms.txt", txt)
if OG_META.pop("_dirty", None):
    json.dump(OG_META, open(OG_META_FILE, "w"), indent=0, sort_keys=True)
print("OK pro: %d gidsen, %d producten" % (len(guides), N_PROD))
# Prijsgrens: 'onder X euro'-gidsen moeten hun titel waarmaken (tools/prijsgrens_check.py schrijft _src/prijsgrens.json)
try:
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "prijsgrens_check.py"), "--stil"], timeout=60)
except Exception as ex:
    print("Prijsgrens-controle overgeslagen: %s" % ex)
