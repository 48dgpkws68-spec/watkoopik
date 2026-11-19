# Schrijfregels voor gidsen (data/*.json)

Voorbeeld en schema: data/beste-stofzuiger.json. Kopieer de structuur exact.

Verplichte velden: slug, cat (huishouden|keuken|verzorging|slapen|elektronica|wonen|sport|kind|klussen), prio (volgorde op de site, 1 = bovenaan),
title ("De 10 beste X van 2026"), short, query (enkelvoud, bv "föhn"), keywords (4-6 zoektermen), ico (1 emoji), updated ("2026-10-13"),
reviews_total ("" laten: een geschat totaal is een verzonnen cijfer en wordt sinds 17 nov 2026 niet meer getoond), intro (70-100 woorden), verdict (60-90 woorden), products (precies 10), guide (5-6 secties {h,p}), faq (5-6 {q,a}).

Per product: brand, name (zonder merk), price (getal in euro, realistische NL-winkelprijs oktober 2026), score (7.8 t/m 9.5, product 1 heeft de hoogste),
label (product 1 = "Beste keuze"; precies één ander product "Beste prijs-kwaliteit"; precies één "Beste premium"; de rest null),
reviews ("" laten: tools/bol_sync.py vult het met de echte bol-score, "bol-score 4,6 van 5"; nooit een geschat aantal reviews, sinds 17 nov 2026), oneliner (max 12 woorden), specs (4 tot 5 sleutels, DEZELFDE sleutels bij alle 10 producten, korte waarden),
pros (3-4), cons (2-3), ideal (1 zin), text (2 alinea's gescheiden door \n\n, samen 130-180 woorden, concreet: cijfers, functies, wat gebruikers zeggen).

Taalregels (de build breekt af bij overtreding):
- Nederlands, je-vorm, concreet en nuchter. Geen reclametaal.
- NOOIT een em-dash of en-dash (— of –). Gebruik een punt, komma of dubbele punt.
- NOOIT een komma direct voor "en" (", en"). Splits de zin of laat de komma weg.
- Nooit "getest" of "wij hebben getest": wij vergelijken op specificaties en reviews.
- Reviewcijfers in de tekst (sinds 17 nov 2026): noem nooit een aantal reviews ("ruim 4.000 reviews"), bol geeft geen aantal. Een score ("4,6 van 5") alleen als die gelijk is aan de echte bol-score in het veld rating (bol_sync); bij twijfel weglaten. Ook geen "best verkochte" of "meest beoordeelde" zonder bron. De build telt afwijkingen: "Reviewclaims: N" (tools/claim_check.py).
- Geen menigteclaims (sinds 18 nov 2026): nooit "wat duizenden gebruikers melden", "honderden reviews", "de ervaringen van tienduizenden kopers". Niemand heeft die gelezen en bol geeft geen aantal. Schrijf "de score bij bol" of noem de echte bol-score. tools/claim_check.py telt ze als menigteclaim; de build moet "Reviewclaims: 0" geven.
- Geen verkoop- of testclaims zonder bron (sinds 19 nov 2026): nooit "de bestverkochte/meest verkochte X van Nederland", "wij zetten 34 machines naast elkaar op smaak". Wij hebben geen verkoopcijfers en testen niets zelf. Schrijf wat waar is: "een bekende/vertrouwde X", "de modellen die nu bij bol te koop zijn". claim_check.py telt ze als menigteclaim. Verschoven bol-scores zet `python3 tools/claim_check.py --fix` gelijk (zinnen met een vergelijking blijven handwerk).
- Geen aantal vergeleken modellen (sinds 18 nov 2026): nooit "wij vergeleken tientallen modellen" of "ruim dertig modellen". Schrijf "wij vergeleken de modellen die nu bij bol te koop zijn". Het aantal in de lijst (top 10) mag wel.
- Alleen echte, bestaande producten met echte modelnamen die in Nederland (bol) te koop zijn. Geen verzonnen modellen.
- Prijzen afronden op hele euro's of ,95/,99 zoals winkels doen.
- Geen "2025" in titels, alleen 2026.

Extra regel (13 okt 2026): nooit producten van Pegasus Depot of G&C Systems opnemen (eigen bol-verkoopaccount van Nick; affiliate-commissie op eigen producten is niet toegestaan).

Extra regel (24 okt 2026): eigen merken van Nick mogen alleen in het aparte, gemarkeerde blok "eigen_merk" boven het podium, nooit in de top 10 zelf.

## Auteur (sinds 4 nov 2026)
- Auteur van alle gidsen is Nick van Straaten (oprichter en eindredacteur); hij leest de gidsen na. Byline en Article-schema staan in build.py, bio op over-ons.html#nick.
- Schrijf nooit dat Nick of watkoopik producten zelf getest heeft; wij vergelijken specificaties, prijzen en ervaringen van kopers. Geen verzonnen persoonlijke ervaringen in zijn naam.
