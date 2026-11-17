#!/usr/bin/env python3
"""Toetst reviewclaims in de vrije tekst van de gidsen aan echte bol-data (N42, 17 nov 2026).

- Scoreclaims ("4,7 sterren", "gemiddeld 4,6 van 5", "op bol krijgt hij een 4,2") moeten
  binnen 0,1 van product["rating"] (bol-gemiddelde uit bol_sync.set_rating) liggen.
- Aantallen reviews ("ruim 7.000 reviews") zijn nooit gemeten: bol geeft geen aantal.
Uitvoer: _src/claims.json en een samenvatting. --kort = alleen de tellerregel (voor build.py).
"""
import json, glob, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = r'([1-5][,.]\d)'
SCORE = [
    re.compile(NUM + r'\s*(?:sterren|ster\b|uit 5|van (?:de )?5)', re.I),
    re.compile(r'(?:gemiddeld(?:e)?(?: van)?|scoort(?: het| hij| ze)?(?: gemiddeld)?|staat (?:hij|het|ze|de set) op|krijgt (?:hij|het|ze|de set)(?: gemiddeld)?|geven (?:hem|het|haar)(?: gemiddeld)?|beoordeeld met)\s+(?:een\s+)?' + NUM + r'(?!\d)', re.I),
]
COUNT = re.compile(r'\d[\d.]*\+?\s*(?:reviews|beoordelingen|recensies|klantbeoordelingen|reacties van kopers)', re.I)

def velden(p):
    yield 'text', p.get('text', '')
    for i, s in enumerate(p.get('pros', []) or []): yield f'pros[{i}]', s
    for i, s in enumerate(p.get('cons', []) or []): yield f'cons[{i}]', s

def scan():
    uit = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json'))):
        slug = os.path.basename(f)[:-5]
        d = json.load(open(f))
        for pi, p in enumerate(d.get('products', [])):
            r = p.get('rating')
            for veld, s in velden(p):
                if not isinstance(s, str): continue
                gezien = set()
                for rx in SCORE:
                    for m in rx.finditer(s):
                        if m.start(1) in gezien: continue
                        gezien.add(m.start(1))
                        v = float(m.group(1).replace(',', '.'))
                        if r is None or abs(v - float(r)) > 0.1:
                            uit.append({'gids': slug, 'p': pi, 'naam': p.get('name'), 'veld': veld, 'soort': 'score',
                                        'claim': v, 'bol': r, 'zin': s[max(0, m.start()-80):m.end()+40]})
                for m in COUNT.finditer(s):
                    uit.append({'gids': slug, 'p': pi, 'naam': p.get('name'), 'veld': veld, 'soort': 'aantal',
                                'claim': m.group(0), 'bol': r, 'zin': s[max(0, m.start()-80):m.end()+40]})
    return uit

if __name__ == '__main__':
    uit = scan()
    json.dump(uit, open(os.path.join(ROOT, '_src', 'claims.json'), 'w'), ensure_ascii=False, indent=1)
    sc = sum(1 for x in uit if x['soort'] == 'score'); an = len(uit) - sc
    gidsen = len({x['gids'] for x in uit})
    print(f'Reviewclaims: {sc} score(s) wijken af van bol, {an} aantal(len) reviews, in {gidsen} gids(en)' if uit else 'Reviewclaims: 0')
    if '--kort' not in sys.argv:
        for x in uit[:400]: print(x['soort'], x['gids'], x['p'], x['veld'], x['claim'], 'bol', x['bol'], '|', x['zin'].replace('\n', ' '))
