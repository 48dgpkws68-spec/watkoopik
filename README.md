# watkoopik.nl

Statische affiliate-site met top 10-koopgidsen. Gebouwd met `build.py` uit `data/*.json`.

- `data/` : één JSON per gids (schema: zie `data/beste-stofzuiger.json` en `SCHRIJFREGELS.md`)
- `_src/` : stylesheet en script
- `build.py` : genereert alle HTML, sitemap.xml, search.json; breekt af bij streepjes of ", en" in copy
- `deploy.sh` : build + commit + push naar GitHub Pages (CNAME watkoopik.nl)
- `shop_link()` in build.py : centrale plek voor winkel-links; na goedkeuring bol Partner vervangen door partnerlinks

Nieuwe gids toevoegen: JSON in `data/`, dan `./deploy.sh "Nieuwe gids: X"`.
