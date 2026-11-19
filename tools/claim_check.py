#!/usr/bin/env python3
"""Toetst reviewclaims in de vrije tekst van de gidsen aan echte bol-data (N42, 17 nov 2026).

- Scoreclaims ("4,7 sterren", "gemiddeld 4,6 van 5", "op bol krijgt hij een 4,2") moeten
  binnen 0,1 van product["rating"] (bol-gemiddelde uit bol_sync.set_rating) liggen.
- Aantallen reviews ("ruim 7.000 reviews") zijn nooit gemeten: bol geeft geen aantal.
- Menigteclaims ("wat duizenden gebruikers melden", "honderden reviews") ook niet (18 nov 2026),
  in alle tekstvelden van de gids (intro, guide, faq, producten).
Uitvoer: _src/claims.json en een samenvatting. --kort = alleen de tellerregel (voor build.py).
"""
import json, glob, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = r'([1-5][,.]\d)'
SCORE = [
    re.compile(NUM + r'\s*(?:sterren|ster\b|uit 5|van (?:de )?5)', re.I),
    re.compile(r'(?:gemiddeld(?:e)?(?: van)?|scoort(?: het| hij| ze)?(?: gemiddeld)?|staat (?:hij|het|ze|de set) op|krijgt (?:hij|het|ze|de set)(?: gemiddeld)?|geven (?:hem|het|haar)(?: gemiddeld)?|beoordeeld met)\s+(?:een\s+)?' + NUM + r'(?!\d)', re.I),
]
MENIGTE = re.compile(r'\b(?:tien)?(?:duizenden|honderden)\s+(?:positieve\s+|nederlandse\s+|tevreden\s+)?(?:gebruikers\w*|kopers\w*|reviews|beoordelingen|recensies|ervaringen|klanten|eigenaren)|\b(?:best\s?verkochte|meest\s+(?:verkochte|gekochte))\s+[\w-]+\s+van\s+(?:Nederland|Belgi)', re.I)  # 19 nov: verkoopclaims zonder bron
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
        def alle(o, pad):
            if isinstance(o, dict):
                for k, v in o.items(): yield from alle(v, pad + '.' + k)
            elif isinstance(o, list):
                for i, v in enumerate(o): yield from alle(v, f'{pad}[{i}]')
            elif isinstance(o, str):
                yield pad, o
        for pad, s in alle(d, ''):
            for m in MENIGTE.finditer(s):
                uit.append({'gids': slug, 'p': None, 'naam': None, 'veld': pad, 'soort': 'menigte',
                            'claim': m.group(0), 'bol': None, 'zin': s[max(0, m.start()-80):m.end()+40]})
    return uit

VERGELIJK = re.compile(r'\b(?:hoogste|laagste|hoger|lager|beter|slechter|dan de|tegen|net als|evenveel|beste score|gelijk)\b', re.I)

def fix():
    """--fix (19 nov 2026): zet verschoven bol-scores in de tekst gelijk aan product.rating.
    Alleen als de zin geen vergelijking bevat; die worden getoond en blijven handwerk."""
    gedaan, hand = 0, []
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json'))):
        raw = open(f).read(); d = json.loads(raw); nieuw = raw
        for pi, p in enumerate(d.get('products', [])):
            r = p.get('rating')
            if r is None: continue
            for veld, s in velden(p):
                if not isinstance(s, str): continue
                spans = {}
                for rx in SCORE:
                    for m in rx.finditer(s):
                        v = float(m.group(1).replace(',', '.'))
                        if abs(v - float(r)) > 0.1: spans[m.start(1)] = m.end(1)
                if not spans: continue
                zinnen_ok = True
                for a in spans:
                    b0 = max(s.rfind('.', 0, a), s.rfind('\n', 0, a)) + 1
                    e0 = s.find('.', a + 4); e0 = len(s) if e0 < 0 else e0
                    if VERGELIJK.search(s[b0:e0]): zinnen_ok = False
                if not zinnen_ok:
                    hand.append(f'{os.path.basename(f)[:-5]} p{pi} {veld}: {s[:90]}'); continue
                t = s
                for a in sorted(spans, reverse=True):
                    t = t[:a] + f'{float(r):.1f}'.replace('.', ',') + t[spans[a]:]
                oud = json.dumps(s, ensure_ascii=False)[1:-1]; nw = json.dumps(t, ensure_ascii=False)[1:-1]
                if nieuw.count(oud) >= 1:
                    nieuw = nieuw.replace(oud, nw, 1); gedaan += len(spans)
                else:
                    hand.append(f'{os.path.basename(f)[:-5]} p{pi} {veld}: niet terug te vinden in het bestand')
        if nieuw != raw:
            json.loads(nieuw); open(f, 'w').write(nieuw)
    print(f'claim_check --fix: {gedaan} score(s) gelijkgezet, {len(hand)} met de hand')
    for h in hand: print('  HAND', h)

if __name__ == '__main__':
    if '--fix' in sys.argv: fix()
    uit = scan()
    json.dump(uit, open(os.path.join(ROOT, '_src', 'claims.json'), 'w'), ensure_ascii=False, indent=1)
    sc = sum(1 for x in uit if x['soort'] == 'score'); mg = sum(1 for x in uit if x['soort'] == 'menigte'); an = len(uit) - sc - mg
    gidsen = len({x['gids'] for x in uit})
    print(f'Reviewclaims: {sc} score(s) wijken af van bol, {an} aantal(len) reviews, {mg} menigteclaim(s), in {gidsen} gids(en)' if uit else 'Reviewclaims: 0')
    if '--kort' not in sys.argv:
        for x in uit[:400]: print(x['soort'], x['gids'], x['p'], x['veld'], x['claim'], 'bol', x['bol'], '|', x['zin'].replace('\n', ' '))
