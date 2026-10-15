# Opdracht: producten zonder bol-koppeling oplossen

Werkmap: /Users/nickvanstraaten/Desktop/4neon /fable5/watkoopik (pad bevat een spatie, gebruik aanhalingstekens).

Doel: elk product in een gids moet bij bol te koop zijn en een EAN hebben, zodat de site een echte productfoto, de dagprijs en een directe link met de affiliatecode kan tonen. Een product zonder bol-artikel levert geen commissie op.

Voor elke gids die aan jou is toegewezen:
1. Open data/_candidates/<slug>.json. Onder "missing" staan per productnummer (rank, 1 = eerste product in data/<slug>.json) de producten zonder koppeling plus kandidaten uit de bol-catalogus.
2. Kies per product:
   a. Staat er een kandidaat bij die HETZELFDE model is (een ander kleurcode-achtervoegsel zoals /10 vs /20, of een andere kleurvariant mag), met een prijs? Zet dan in data/<slug>.json bij dat product: "ean": "<de EAN als tekst>".
   b. Zo niet: zoek zelf met python3 tools/bol_search.py "<zoekterm>" 15 (probeer merk + typenummer, merk + serie + productsoort, productsoort + merk). Gevonden en met prijs? Zet de EAN.
   c. Verkoopt bol het model echt niet (niet gevonden of "geen aanbod")? Vervang het product door een vergelijkbaar model dat bol WEL verkoopt (zelfde rol en prijsklasse, zelfde positie in de lijst). Herschrijf dan voor dat product: brand, name, price (de bol-prijs, afgerond), score (logisch binnen de lijst), reviews, oneliner, specs (exact dezelfde sleutels als de andere producten), pros, cons, ideal en text (2 alinea's, samen 130 tot 180 woorden, concreet). Zet "ean". Verwijder bij een vervangen product de velden url, image, bol_title en synced als die er staan.
3. Regels die altijd blijven gelden: product 1 houdt het label "Beste keuze" en de hoogste score; precies één "Beste prijs-kwaliteit" en één "Beste premium". Nederlands, je-vorm, NOOIT een em-dash of en-dash, NOOIT een komma direct voor "en", nooit claimen dat wij iets getest hebben. Geen producten van Pegasus Depot of G&C Systems. Kies alleen bol-artikelen met een prijs en liefst een goede beoordeling; geen tweedehands, geen accessoires, geen onderdelen.
4. Controleer elke aangepaste gids: python3 tools/check_guide.py data/<slug>.json (moet OK geven).
5. Draai NIET tools/bol_sync.py en NIET build.py (dat doet de coördinator daarna in één keer). Raak alleen de jou toegewezen gidsen aan.

Rapporteer aan het eind kort per gids: hoeveel producten gekoppeld via EAN, hoeveel vervangen (welke door welke), en wat onoplosbaar bleef.
