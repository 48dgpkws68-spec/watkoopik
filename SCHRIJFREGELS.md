# Schrijfregels voor gidsen (data/*.json)

Voorbeeld en schema: data/beste-stofzuiger.json. Kopieer de structuur exact.

Verplichte velden: slug, cat (huishouden|keuken|verzorging|slapen|elektronica|wonen|sport|kind|klussen), prio (volgorde op de site, 1 = bovenaan),
title ("De 10 beste X van 2026"), short, query (enkelvoud, bv "föhn"), keywords (4-6 zoektermen), ico (1 emoji), updated ("2026-10-13"),
reviews_total (bv "6.300"), intro (70-100 woorden), verdict (60-90 woorden), products (precies 10), guide (5-6 secties {h,p}), faq (5-6 {q,a}).

Per product: brand, name (zonder merk), price (getal in euro, realistische NL-winkelprijs oktober 2026), score (7.8 t/m 9.5, product 1 heeft de hoogste),
label (product 1 = "Beste keuze"; precies één ander product "Beste prijs-kwaliteit"; precies één "Beste premium"; de rest null),
reviews ("1.200+ reviews"), oneliner (max 12 woorden), specs (4 tot 5 sleutels, DEZELFDE sleutels bij alle 10 producten, korte waarden),
pros (3-4), cons (2-3), ideal (1 zin), text (2 alinea's gescheiden door \n\n, samen 130-180 woorden, concreet: cijfers, functies, wat gebruikers zeggen).

Taalregels (de build breekt af bij overtreding):
- Nederlands, je-vorm, concreet en nuchter. Geen reclametaal.
- NOOIT een em-dash of en-dash (— of –). Gebruik een punt, komma of dubbele punt.
- NOOIT een komma direct voor "en" (", en"). Splits de zin of laat de komma weg.
- Nooit "getest" of "wij hebben getest": wij vergelijken op specificaties en reviews.
- Alleen echte, bestaande producten met echte modelnamen die in Nederland (bol) te koop zijn. Geen verzonnen modellen.
- Prijzen afronden op hele euro's of ,95/,99 zoals winkels doen.
- Geen "2025" in titels, alleen 2026.

Extra regel (13 okt 2026): nooit producten van Pegasus Depot of G&C Systems opnemen (eigen bol-verkoopaccount van Nick; affiliate-commissie op eigen producten is niet toegestaan).
