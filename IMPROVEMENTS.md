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

## 2026-10-23
- Signalen: Umami 7 dagen 172 bezoekers, 238 weergaven, bounce 55%; homepage 50 weergaven, best gelezen tv 65 inch (12), tv 55 inch (9), dekbed en kachel (6); bronnen watkoopik.com 41, chatgpt.com 5; 73 bol-klik-events (podium 46, tabel 24, kaart 2, sticky 1), top gidsen stofzuiger huisdieren, tv 65 inch, kachel.
- Signalen: Search Console 7 dagen 0 klikken, 32 vertoningen, positie 59,6; eerste echte zoekopdrachten, allemaal luchtreiniger bij allergie (allergie, pollen, kattenallergie, formaldehyde, slaapkamer, astma, huisstofmijt); indexering nu 16 geindexeerd, 26 gevonden niet geindexeerd, 3 gecrawld niet geindexeerd, 1 canonical.
- Signalen: bol-cijfers: niet automatisch beschikbaar; build OK 162 gidsen / 1620 producten, check_links 1561 links 0 fouten en 10/10 goed; 20 producten zonder foto (tv 32 inch, ultrawide monitor) nu 0; steekproef tv 32 inch + ultrawide: 0 streepjes, 0 ", en", geen "getest".
- Gedaan: nieuw optioneel veld "seo" in de gidsdata voor titel, meta description en koopgids-kop, los van "query" (bol-zoekterm); ingevuld voor 20 subgidsen; waarom: titels droegen de bol-zoekterm, bijv. "Beste luchtreiniger hepa 2026" voor de allergiegids, "Beste volautomaat goedkoop" voor bonenmachines onder 500 euro, "Beste espressomachine pistonmachine" voor beginners; verwacht effect: titel en snippet sluiten aan op wat mensen echt zoeken, hogere positie en CTR. Nieuwe subgidsen van de dagroutine krijgen nog geen seo-veld (fallback query).
- Gedaan: allergiegids kreeg 4 FAQ's (slaapkamer, astma, formaldehyde, pollen) en 5 extra keywords, precies de zoekvragen uit Search Console; waarom: eerste echte vertoningen maar positie rond 60; verwacht effect: betere positie op die long tail en FAQ-structured data voor die vragen.
- Gedaan: 20 producten zonder foto gekoppeld via exacte EAN (alle 20 hetzelfde model op bol), bol_sync gedraaid; verwacht effect: foto's, dagprijs en werkende affiliatelinks op twee nieuwe gidsen. IndexNow: 181 URL's gemeld.
- Idee voor later: de dagroutine laten zorgen dat nieuwe subgidsen direct een "seo"-veld krijgen (zoekterm zoals in de titel).
- Idee voor later: 26 pagina's "gevonden, niet geindexeerd" (crawlbudget); homepage "meest bekeken" uitbreiden met een blok nieuwste gidsen voor snellere ontdekking.
- Idee voor later: kaart (2) en sticky (1) blijven zwak na de knoptekstwijziging; sticky-balk eventueel pas na het podium tonen.
- Voor Nick: niets (optioneel in Search Console "Indexering aanvragen" voor de allergiegids).

## 2026-10-24 (handmatig met Nick)
- Gedaan: tools/check_stock.py (bol-API) vond 106 producten zonder aanbieding of met afwijkende prijs, waaronder 8 nummers 1. Alle opgelost: 34 via leverbare variant, 73 vervangen met nieuwe tekst. Nu 1620/1620 leverbaar.
- Gedaan: bol_sync vernieuwt het token bij 401 (tokens verlopen na ~5 min). check_stock staat als STAP 2c in VERBETER_PROMPT.md.
- Voor Nick: niets.

## 2026-10-24 (pakket conversie, deals, indexering, seizoen)
- Gedaan: podium eerst. Op mobiel een kortere kop (2 regels intro, 1 meta-label, korte affiliatemelding), volledige disclaimer direct onder het podium, voorkeursbron-knop naar onder de FAQ. Sticky balk verscheen al pas na het podium (app.js), ongewijzigd. Waarom: podium levert 46 van 73 kliks. Verwacht: meer podiumkliks, lagere bounce; meten via plek=podium.
- Gedaan: "Prijs gecontroleerd op <datum>" bij podium, tabel en kaart, uit het synced-veld (terugval gidsdatum). Verwacht: meer vertrouwen en CTR op de koopknoppen.
- Gedaan: /aanbiedingen/ met alleen echt gemeten prijsdalingen: bol_sync bewaart nu ph (dagprijzen 60 dagen), prev_price, prev_date en low_price; geschiedenis teruggevuld uit git (tools/price_backfill.py). Deal = minstens 10% onder de mediaan van de 30 dagen voor de daling, dalingen boven 60% of ouder dan 21 dagen tellen niet. Eerlijke lege staat. Link in menu en homepageblok. Plek "deals". Vandaag 48 deals.
- Gedaan: indexering: unieke intro van 86 tot 101 woorden per categoriehub plus lijst van alle gidsen, homepageblok "Nieuwste gidsen" (8, op nieuw veld published), per gids 4 verwante gidsen uit dezelfde categorie (op woordoverlap), sitemap met lastmod inclusief nieuwe pagina's. Waarom: 26 URL's gevonden maar niet geindexeerd. Verwacht: meer geindexeerde gidsen binnen 2 weken.
- Gedaan: seizoen: categorie cadeaus met hub /cadeaus/ en 6 cadeaugidsen (hem en haar onder 50, tech onder 100, thuiswerkers, keuken, kerst voor ouders), alle 60 producten met bol-aanbod (check_stock 1680/1680 te koop). bol-API gaf geen reviewaantallen, dus daar staat "reviews op bol" zonder getal en geen reviews_total. Dubbele producten tussen hem en haar vervangen. /black-friday/ bundelt de 12 best bekeken gidsen en toont van 27 t/m 30 november automatisch de dealpagina bovenaan.
- Gedaan: /vs/ met 6 vergelijkingen (nr. 1 tegen nr. 2: tv 65, tv 55, stofzuiger huisdieren, kachel, luchtreiniger allergie, bureaustoel), specificatietabel, winnaar per situatie, koopknoppen (plek vs en vs-oordeel), link vanuit de gids onder het podium. Koppeling op EAN: wisselt een product, dan valt de pagina weg.
- Gedaan: dagroutine watkoopik-dagelijkse-gidsen: seo- en published-veld verplicht, voorrang seizoen en categorieën met kliks, tempo 3 per dag tot 70% geindexeerd, daarna 5 (backup SKILL.md.bak-20261024).
- Idee voor later: na 7 dagen kliks per plek vergelijken (podium, deals, vs); vs-pagina's toevoegen voor gidsen met veel tabelkliks.
- Voor Nick: niets.

## 2026-10-24 (avondronde)
- Signalen: Umami 7 dagen 206 bezoekers, 293 weergaven, bounce 51%; best gelezen tv 65 inch (16), tv 55 inch (9), tv onder 500 euro en kachel (7); bronnen watkoopik.com 47, chatgpt.com 5.
- Signalen: 87 bol-klik-events (podium 58, tabel 26, kaart 2, sticky 1); top producten TCL 65T69C en Shark PowerDetect (7), Roborock Qrevo Edge 2 en Philips CX5120 (5); gidsen tv 65 inch 8, kachel, tv onder 500, dweilrobot, stofzuiger huisdieren 7.
- Signalen: Search Console (t/m 22 okt) 50 vertoningen, positie 61,6, 0 klikken, alleen luchtreiniger-allergie-zoekopdrachten; indexering ongewijzigd 16 geindexeerd, 26 gevonden niet geindexeerd, 3 gecrawld, 1 canonical; bol-cijfers: niet automatisch beschikbaar; check_links 0 fouten, 0 zonder foto.
- Gedaan: check_stock vond 20 kapotte koopknoppen (sinds de ochtend weer uit aanbod), 9 opgelost via leverbare variant (o.a. Ninja Double Stack wit, Soundcore Sleep A30, Vultec P800T zwart), 11 vervangen (Vultec M450 door Komodo 450 W in 3 gidsen, Miele Guard M1 Cat & Dog door Guard L1 Cat & Dog Flex en Guard M1 Flex, Rowenta RO4933 door Electrolux Pure D8, Philips BT5502 door BT5775, Dell U2725QE door U2723QE, PS5-bundel door Digital 1 TB, Winbot W1 Pro door Winbot Mini, Tefal RK8121 door Reishunger, Philips HF3519 door UPLY); reviews bij vervangers als echte "bol-score x van 5" i.p.v. geschatte aantallen; nu 1680/1680 te koop. Verwacht: geen dode knoppen, o.a. op de best klikkende gidsen stofzuiger huisdieren en kachel.
- Gedaan: 2 nieuwe vs-pagina's: LG 55QNED84 vs TCL 65T69C (tv onder 500, de twee meest geklikte tv-producten) en Roborock Qrevo Edge 2 vs Dreame L40s Pro Ultra (dweilrobot, 7 kliks); waarom: idee "vs voor gidsen met veel kliks"; verwacht: meer kliks van twijfelaars, meten via plek vs / vs-oordeel en event vs-link.
- Idee voor later: check_stock elke ronde draaien blijft nodig, bol-aanbod wisselt binnen een dag; overweeg een dagelijkse automatische check met melding.
- Idee voor later: beste-playstation-5 heeft #2 en #9 met dezelfde EAN (Slim Digital) en een rommelige volgorde; gids opschonen.
- Voor Nick: niets.

## 2026-10-25
- Signalen: Umami 7 dagen 195 bezoekers, 276 weergaven, bounce 51%; best gelezen homepage 48, tv 65 inch 10, tv onder 500 euro 8, tv 55 inch, dweilrobot en kachel 7; bronnen watkoopik.com 36, chatgpt.com 5.
- Signalen: 88 bol-klik-events (podium 64, tabel 21, kaart 2, sticky 1; positie 1: 41, positie 2: 25); top gidsen tv onder 500 en dweilrobot 8, kachel en stofzuiger huisdieren 7; top product Shark PowerDetect 7.
- Signalen: Search Console 7 dagen 0 klikken, 64 vertoningen, positie 66,2, nog steeds alleen luchtreiniger-allergie-zoekopdrachten; indexering 16 geindexeerd, 26 gevonden niet geindexeerd, 3 gecrawld, 1 canonical; bol-cijfers: niet automatisch beschikbaar; check_links 1646 links 0 fouten, live test (zondag) 2/2 goed; steekproef dweilrobot + kachel badkamer schoon.
- Gedaan: check_stock vond 17 kapotte koopknoppen, alle opgelost. Varianten: Ducky Dons 260x220, POCO M8 Pro 12/512 (laadsnelheid gecorrigeerd naar 100 W), Braun MQ55.254M, Xiaomi Rice Cooker 4L, Bosch EasyAquatak 120 (andere EAN). Vervangen: TCL 65T69C door TCL 65P71K (tv onder 500 #2, tv 65 #9), TCL 55P79L door TCL 55C69KS (tv onder 500 #9, tv 55 #10), Samsung QE65Q7FA door Hisense 65E7S, Philips HF3532 door HF3531 (nr. 1 kerstcadeau ouders) en HF3519 (wekker), XGIMI MoGo 3 Pro door MoGo 2 Pro, Vultec P800T door Komodo 800 W, SodaStream E-Terra door WMF Element One, KitchenAid Go door KitchenAid 5KHBV83, Xiaomi X20+ door X20 Max; verdicts en FAQ's mee aangepast. Waarom: TCL 65T69C was het meest geklikte tv-product, de knoppen gaven geen commissie meer. Verwacht: weer 1710/1710 te koop.
- Gedaan: PS5-gids opgeschoond: dubbele EAN op #9 vervangen door Slim Disc Edition met 2 DualSense (909 euro), onjuiste prijsclaims bij #2 weggehaald. Waarom: idee van 24 okt, twee dezelfde producten en "goedkoopste" klopte niet meer.
- Gedaan: Pinterest-wachtrij (watkoopik-social/queue_pin.json, backup .bak-20261025) herschikt: de eerstvolgende 16 pins zijn de 10 best klikkende gidsen plus de 6 cadeaugidsen, rest in de oude volgorde. Waarom: weekrapport-advies pins op tv/kachel/stofzuiger, en Pinterest heeft weken aanloop voor kerstzoekverkeer. Verwacht: meer verkeer naar gidsen die al converteren.
- Gedaan: verlopen vs-pagina LG 55QNED84 vs TCL 65T69C (build ruimt die niet op) vervangen door noindex-doorverwijzing naar de gids tv onder 500.
- Idee voor later: nieuwe vs-pagina voor tv onder 500 met de nieuwe nr. 2 (TCL 65P71K); build.py laten waarschuwen of opruimen als een vs-pagina vervalt.
- Idee voor later: bij WMF Element One staat "Stroom nodig: niet vermeld", nakijken; zuigkracht 8.000 Pa bij Xiaomi X20 Max komt niet uit de bol-data, verifiëren.
- Voor Nick: niets.
