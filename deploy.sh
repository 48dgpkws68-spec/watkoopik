#!/bin/zsh
# Bouwt de site en pusht naar GitHub Pages. Gebruik: ./deploy.sh "commit-bericht"
set -e
cd "$(dirname "$0")"
python3 tools/umami.py --save || echo "populair.json niet bijgewerkt"
python3 build.py
git add -A
git commit -m "${1:-Update gidsen}" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" || echo "niets te committen"
git push origin main
# Nieuwe en gewijzigde pagina's direct aanmelden bij Bing/DuckDuckGo/Ecosia (key-bestand moet live zijn, dus even wachten)
(sleep 90; python3 tools/indexnow.py) || true
