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
