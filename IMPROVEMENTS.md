# Verbeterlogboek watkoopik.nl

Elke avond kiest de verbeterronde 1 tot 3 verbeteringen op basis van Umami, Search Console en bol en voert ze door.

## 2026-10-13
- Gedaan: lancering met 26 gidsen, bol-partnerlinks, Pinterest/IG/TikTok-routines, Search Console, Umami-analytics met bol-klik-events.

## 2026-10-13 (verbeterronde 21:15)
- Signalen: Umami 0 bezoekers in de laatste 24 uur (site vandaag live), dus nog geen bol-klik-events of bronnen.
- Signalen: Search Console verwerkt nog ("over enkele dagen opnieuw"), dus nog geen zoekopdrachten of indexeringsfouten.
- Signalen: bol partner niet ingelogd in Browser 1 (overgeslagen); build OK 26 gidsen; steekproef matras + airfryer: geen streepjes of ", en" in zichtbare tekst (alleen in interne bol_title-velden).
- Gedaan: per gids een eigen deelafbeelding 1200x630 (og/<slug>.jpg met titel, categorie en product nr. 1) + og:image en twitter summary_large_image; waarom: social-routines en WhatsApp-deelacties toonden geen beeld; verwacht effect: hogere CTR op gedeelde links en Pinterest/IG-bio-kliks.
- Gedaan: Article-structured data met dateModified, auteur en uitgever op elke gids; waarom: versheidssignaal voor "beste X 2026"-zoekopdrachten; verwacht effect: snellere indexering en betere snippet-kans.
- Idee voor later: zodra Search Console data heeft, titels/meta's herschrijven voor queries met vertoningen maar CTR onder 2%.
- Idee voor later: Umami-events vergelijken (tabel versus winnaarsblok versus sticky knop) om knopplaatsing bij te sturen.
- Voor Nick: inloggen op partner.bol.com in Chrome-profiel Browser 1, zodat de ronde kliks en commissie kan lezen.

## 2026-10-14
- Signalen: Umami laatste 24 uur ongeveer 21 bezoekers, 34 weergaven, bounce 21%, vooral homepage; grotendeels VS (bots), 4 uit NL, referrers watkoopik.com en bing.com.
- Signalen: 0 bol-klik-events (tracking in HTML gecontroleerd en in orde, er komen nog bijna geen gidsbezoekers); Search Console verwerkt nog, sitemap op 13 okt gelezen met 39 pagina's (nu 58 URL's).
- Signalen: bol partner niet ingelogd in Browser 1 (overgeslagen); build OK 44 gidsen; steekproef koelkast, robotmaaier, stoomreiniger: geen streepjes of ", en", ruim 3.400 woorden per gids.
- Gedaan: alle homelinks (logo, menu, kruimelpad, bedankt) wijzen nu naar / in plaats van index.html; waarom: Umami telde /index.html los en interne links gingen naar een niet-canonieke URL; verwacht effect: alle linkwaarde op de canonieke homepage, schonere statistiek.
- Gedaan: IndexNow-aanmelding (key-bestand 9a7bd066b1ef421bb698f3e20a840a06.txt, tools/indexnow.py, automatisch na elke deploy); 58 URL's gemeld, status 202; waarom: Bing stuurde al verkeer en Bing voedt ook DuckDuckGo en Ecosia; verwacht effect: nieuwe gidsen binnen dagen in Bing in plaats van weken.
- Idee voor later: Bing Webmaster Tools koppelen via import uit Search Console voor zoekdata naast Google.
- Idee voor later: zodra Search Console data heeft, titels en meta's herschrijven voor queries met CTR onder 2%.
- Idee voor later: categorie kind en sport hebben oude losse pagina's zonder gidsen; vullen via BACKLOG (sport staat er al in).
- Voor Nick: inloggen op partner.bol.com in Chrome-profiel Browser 1 (staat nog open sinds 13 okt).

## 2026-10-16
- Signalen: Umami laatste 24 uur ongeveer 24 bezoekers, bounce 19%, 71% blijft op de homepage; bronnen watkoopik.com (7) en github.io (1), 2 bol-klik-events.
- Signalen: Search Console 7 dagen 0 klikken, 1 vertoning (positie 27); indexering 0 geindexeerd, 8 "gecrawld, momenteel niet geindexeerd", 1 alternatieve pagina met canonical.
- Signalen: bol partner uitgelogd in Browser 1 (overgeslagen, genoteerd in login-nodig.md); build OK 96 gidsen / 960 producten, check_links 0 fouten en 10/10 doorverwijzingen goed, 0 producten zonder foto; steekproef iphone + vriezer: geen streepjes of ", en", ruim 3.900 woorden.
- Gedaan: elke bol-knop meet nu ook de plek (podium, tabel, kaart, eindoordeel, sticky) als Umami-eigenschap "plek"; waarom: tot nu toe niet te zien welke knopplaatsing werkt; verwacht effect: over een week onderbouwd knoppen verplaatsen of schrappen.
- Gedaan: "Ook interessant" onder elke gids toont 6 in plaats van 3 gidsen (max 4 uit dezelfde categorie, aangevuld met verschoven gidsen uit andere categorieen), alle 96 gidsen krijgen zo inlinks vanuit andere gidsen; waarom: 8 pagina's gecrawld maar niet geindexeerd, sterkere interne links helpen Google de waarde te zien; verwacht effect: snellere indexering en meer pagina's per bezoek.
- Gedaan: sitemap-lastmod volgt nu de nieuwste gidsdatum (per categorie) en vaste data voor statische pagina's in plaats van elke bouw "vandaag"; waarom: Google negeert lastmod als die altijd verandert; verwacht effect: betrouwbaarder hercrawlsignaal bij echte updates. IndexNow: 114 URL's gemeld.
- Idee voor later: over 5 tot 7 dagen in Umami de eigenschap "plek" van bol-klik vergelijken en de zwakste knopplek aanpassen.
- Idee voor later: overlap tussen smartphonegidsen (smartphone, iphone, samsung, onder 300) controleren op dubbele inhoud zodra Search Console per URL meldt welke niet geindexeerd worden.
- Voor Nick: inloggen op partner.bol.com in Chrome-profiel Browser 1 (open sinds 13 okt); optioneel in Search Console voor 5 tot 10 topgidsen "Indexering aanvragen" klikken.

## 2026-10-17
- Signalen: Umami laatste 24 uur ongeveer 14 bezoekers (teller laadt traag in de share-weergave), vooral homepage, bronnen watkoopik.com, bounce 25%; bol-klik-events laag (enkele per week), eigenschap "plek" nog te weinig data.
- Signalen: Search Console ongewijzigd (data t/m 14 okt): 0 klikken, 1 vertoning, 0 geindexeerd, 8 "gecrawld, momenteel niet geindexeerd", 1 alternatieve canonical.
- Signalen: bol partner uitgelogd in Browser 1 (overgeslagen, genoteerd in login-nodig.md); build OK 108 gidsen / 1080 producten, check_links 0 fouten en 10/10 goed, 0 producten zonder foto; steekproef stille-stofzuiger + wanddroogrek-zonder-boren: 0 streepjes, 0 ", en", geen "getest", 3.900 tot 4.200 woorden.
- Gedaan: elke gids heeft weer een eigen deelkaart 1200x630 (og/<slug>.jpg met titel, categorie en huidig nr. 1), plus og:image:width/height/alt en als eerste beeld in Article-structured data; waarom: sinds de nieuwe build.py werd de kaart niet meer gebruikt en toonde 78 gidsen een staand bol-plaatje van 550 px als deelbeeld (Pinterest, WhatsApp, Facebook snijden dat bij); generator staat nu in tools/og.py en maakt alleen ontbrekende kaarten (oude 29 kaarten opnieuw gemaakt omdat ze een verouderde nr. 1 toonden); verwacht effect: hogere CTR op gedeelde links en pins, nette Discover-kandidaat (max-image-preview large).
- Gedaan: gidsen hebben og:type article in plaats van website; waarom: juiste type voor artikelen met datum; verwacht effect: correcte weergave in sociale previews.
- Idee voor later: verander een gids van nr. 1 dan blijft de oude kaart staan; kaart opnieuw maken als de winnaar wisselt (bijv. nr. 1-naam in bestandshash).
- Idee voor later: zodra Search Console per URL toont welke 8 niet geindexeerd zijn, die gidsen extra versterken (unieke intro, meer inlinks vanaf homepage).
- Voor Nick: inloggen op partner.bol.com in Chrome-profiel Browser 1 (open sinds 13 okt); optioneel in Search Console "Indexering aanvragen" voor 5 tot 10 topgidsen.

## 2026-10-18
- Signalen: Umami laatste 24 uur 7 bezoekers, 9 weergaven, bounce 10%, vooral homepage, bron watkoopik.com; nog te weinig bol-klik-events voor een uitspraak over eigenschap "plek".
- Signalen: Search Console ongewijzigd: 0 geindexeerd, 8 "gecrawld, momenteel niet geindexeerd", 1 alternatieve canonical; geen nieuwe zoekdata.
- Signalen: bol partner uitgelogd in Browser 1 (overgeslagen, genoteerd in login-nodig.md); build OK 120 gidsen / 1200 producten, check_links 0 fouten en 10/10 goed, 0 producten zonder foto; steekproef laptop-thuiswerken + koffiemachine-bonen-onder-500: 0 streepjes, 0 ", en", geen "getest", 4.000 tot 4.550 woorden.
- Gedaan: deelkaart (og/<slug>.jpg) wordt automatisch opnieuw gemaakt als de nr. 1 of titel van een gids verandert (vingerafdruk per gids in og/_meta.json) en og:image krijgt een ?v=<vingerafdruk>; waarom: idee van 17 okt, na een productwissel bleef het oude winnaarsbeeld staan en Facebook/Pinterest/WhatsApp cachen op URL; verwacht effect: deelbeeld klopt altijd met de gids, geen verouderde productfoto in pins en previews. Getest door een vingerafdruk te wijzigen: kaart werd opnieuw gemaakt. IndexNow: 138 URL's gemeld.
- Idee voor later: zodra Search Console per URL toont welke 8 gidsen niet geindexeerd zijn, die versterken met unieke intro en homepage-link.
- Idee voor later: overlap smartphonegidsen en oordopjesgidsen (draadloos, slapen, sporten) controleren op dubbele inhoud.
- Voor Nick: inloggen op partner.bol.com in Chrome-profiel Browser 1 (open sinds 13 okt); optioneel in Search Console "Indexering aanvragen" voor 5 tot 10 topgidsen.

## 2026-10-19
- Signalen: Umami laatste 24 uur ongeveer 24 bezoekers (6 met een klik), voor het eerst vooral gidsbezoekers: tv 55 inch en tv 65 inch (3 elk), vriezer, elektrische kachel, smartphone onder 300 (2 elk); nieuwe bron chatgpt.com naast watkoopik.com.
- Signalen: 7 bol-klik-events, eigenschap "plek": tabel 5, podium 2, kaart/eindoordeel/sticky 0 (Dyson Airstrait 2x, Philips OLED, Polar Pacer, SIHOO, VONROC, Leifheit); Search Console 7 dagen 4 vertoningen, positie 10,5, 0 klikken; indexering ongewijzigd (0 geindexeerd, 8 gecrawld niet geindexeerd, 1 canonical), URL-lijst niet te openen in de share-weergave.
- Signalen: bol-cijfers: niet automatisch beschikbaar; build OK 132 gidsen / 1320 producten, check_links 0 fouten en 10/10 goed, 0 producten zonder foto.
- Gedaan: koopknop-kolom in de vergelijkingstabel blijft nu rechts vastgeplakt (position sticky, met schaduw) bij horizontaal scrollen, name-kolom op mobiel iets smaller; waarom: de tabel levert 5 van 7 kliks, maar op een telefoon (tabel min. 600 px breed) stond de knop buiten beeld; verwacht effect: meer tabelkliks op mobiel, meten via plek "tabel" komende week.
- Gedaan: BACKLOG herordend: tv 43 inch, tv onder 500 euro, tv 75 inch, QLED-tv, infraroodpaneel, elektrische openhaard en nieuw oliegevulde radiator bovenaan; waarom: tv-gidsen en kachel zijn nu de best gelezen gidsen en het stookseizoen begint; verwacht effect: de dagelijkse routine bouwt eerst op wat al bezoekers trekt.
- Idee voor later: kaart-knoppen (0 kliks) testen met een kortere knoptekst of prijs in de knop, zodra er meer data is.
- Idee voor later: llms.txt of duidelijke samenvatting bovenaan gidsen nu chatgpt.com als bron opduikt.
- Voor Nick: niets (optioneel in Search Console "Indexering aanvragen" voor de tv-gidsen).

## 2026-10-20
- Signalen: Umami laatste 24 uur ongeveer 9 bezoekers, 11 weergaven, bounce 19%; best gelezen tv 55 inch, baardtrimmer, elektrische kachel, oven; bronnen watkoopik.com en chatgpt.com; bol-klik-events 7 dagen laag (teller in de share-weergave laadt onbetrouwbaar), te weinig voor een uitspraak over "plek".
- Signalen: Search Console 7 dagen 6 vertoningen, positie 10,2, 0 klikken, nog geen zoekopdrachten zichtbaar; indexering ongewijzigd (0 geindexeerd, 8 gecrawld niet geindexeerd, 1 canonical).
- Signalen: bol-cijfers: niet automatisch beschikbaar; build OK 144 gidsen / 1440 producten, check_links 1385 links 0 fouten en 10/10 goed, 0 producten zonder foto; steekproef tv 55 inch + elektrische kachel: check_guide OK, 0 streepjes, 0 ", en", geen "getest", 3.600 tot 3.900 woorden.
- Gedaan: /llms.txt (automatisch per bouw) met alle 144 gidsen per categorie, nr. 1 en slimste koop met prijs en bijwerkdatum; waarom: idee van 19 okt, chatgpt.com is de tweede bron en AI-zoekmachines lezen llms.txt als compacte index; verwacht effect: vaker genoemd en gelinkt in ChatGPT/Perplexity-antwoorden, actuele productnamen in die antwoorden.
- Idee voor later: Umami-events via de API of de Properties-weergave per "plek" uitlezen, de share-tellers geven wisselende cijfers.
- Idee voor later: de 8 niet-geindexeerde URL's achterhalen (URL-inspectie per topgids) en die gidsen een unieke intro geven.
- Voor Nick: niets (optioneel in Search Console "Indexering aanvragen" voor tv 55 inch, elektrische kachel en baardtrimmer).

## 2026-10-21
- Signalen: Umami 7 dagen 171 bezoekers, 262 weergaven, bounce 64%; homepage 76 weergaven (29%), best gelezen tv 65 inch (12), tv 55 inch (8), kachel en dekbed (5); bronnen watkoopik.com 53, chatgpt.com 3; NL 97, US 48.
- Signalen: 51 bol-klik-events in 7 dagen (19 in 24 uur); plek podium 33, tabel 15, kaart 1, eindoordeel en sticky 0; positie 1 (24) en 2 (13) domineren; top gidsen in kliks tv 65 inch 8, stofzuiger huisdieren 7, kachel 6, stijltang 4.
- Signalen: Search Console 7 dagen 0 klikken, 7 vertoningen, positie 8,9, nog geen zoekopdrachten; indexering 0 geindexeerd, 8 gecrawld niet geindexeerd, 1 canonical; bol-cijfers: niet automatisch beschikbaar; build OK 156 gidsen / 1560 producten, check_links 0 fouten en 10/10 goed, 0 zonder foto; steekproef stijltang + dekbed schoon (0 streepjes, 0 ", en", geen "getest", 4.100 tot 4.200 woorden).
- Gedaan: tools/umami.py leest Umami via de publieke share-API (stats, pagina's, bronnen, bol-klik per plek/positie/product/gids) zonder browser; waarom: de share-weergave laadde onbetrouwbaar (idee 20 okt); verwacht effect: elke ronde exacte cijfers in seconden.
- Gedaan: homepage heeft een blok "Deze week het meest bekeken" (6 gidsen) en de hero-chips volgen dezelfde volgorde, uit stats/populair.json (weergaven + 3x bol-kliks, 7 dagen), automatisch ververst in deploy.sh; waarom: 29% van de weergaven en hoge bounce op de homepage, terwijl de chips alfabetisch de eerste 9 gidsen toonden; verwacht effect: lagere bounce en meer bezoekers op gidsen die al converteren.
- Gedaan: knop op de 10 productkaarten heet nu "Bekijk actuele prijs bij bol" (Umami-eigenschap tekst=prijs, andere plekken tekst=standaard); waarom: kaart leverde 1 van 49 kliks; verwacht effect: meer kaartkliks, over 7 dagen vergelijken met kaart=1.
- Idee voor later: eindoordeel en sticky gaven 0 kliks in 7 dagen; als dat zo blijft sticky-balk pas tonen na het podium of met prijs in de tekst.
- Idee voor later: tv 65 inch en stofzuiger huisdieren converteren het best; subgidsen ("beste OLED-tv 65 inch", "stofzuiger katten") bovenaan BACKLOG zetten.
- Voor Nick: niets (optioneel in Search Console "Indexering aanvragen" voor tv 65 inch, elektrische kachel en stofzuiger huisdieren).
