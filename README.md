# watkoopik.nl

Statische affiliate-site met top 10-koopgidsen. Gebouwd met `build.py` uit `data/*.json`.

- `data/` : één JSON per gids (schema: zie `data/beste-stofzuiger.json` en `SCHRIJFREGELS.md`)
- `_src/` : stylesheet en script
- `build.py` : genereert alle HTML, sitemap.xml, search.json; breekt af bij streepjes of ", en" in copy
- `deploy.sh` : build + commit + push naar GitHub Pages (CNAME watkoopik.nl)
- `shop_link()` in build.py : centrale plek voor winkel-links; na goedkeuring bol Partner vervangen door partnerlinks

Nieuwe gids toevoegen: JSON in `data/`, dan `./deploy.sh "Nieuwe gids: X"`.

SEO-techniek (audit 24 nov 2026): `page()` zet titles op max 60 tekens (eerst "| watkoopik" eraf, dan de staart na de dubbele punt) en descriptions op 120-160 (`fit_title`/`fit_desc`: hele zinnen, inkorten op een zinsdeel, aanvullen met `FILL`). Pagina's zonder eigen kaart krijgen `og/default.jpg`. Offer-availability komt uit eigen metingen (`beschikbaar()`: bol-prijs van de laatste 2 dagen = InStock, check_stock/sync zonder aanbieding = OutOfStock, anders weglaten). vs/ (overzicht en vergelijkingen) is alleen voor Google noindex.
