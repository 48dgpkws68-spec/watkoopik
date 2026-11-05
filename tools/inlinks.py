# Telt interne links per gids in de gebouwde html. Gebruik: python3 tools/inlinks.py .  (groeimotor N4, 5 nov 2026)
import os,re,glob,collections,sys
root=sys.argv[1]
pages=[p for p in glob.glob(root+'/**/*.html',recursive=True) if '/_src' not in p and '/stats' not in p]
guides={os.path.relpath(p,root) for p in glob.glob(root+'/beste/*.html')}
inl=collections.defaultdict(set); ctx=collections.defaultdict(set)
for p in pages:
    src=os.path.relpath(p,root); d=os.path.dirname(src)
    s=open(p,encoding='utf-8').read()
    for h in set(re.findall(r'href="([^"#?]+\.html)',s)):
        if h.startswith('http'): 
            if 'watkoopik.nl/' in h: t=h.split('watkoopik.nl/')[1]
            else: continue
        else: t=os.path.normpath(os.path.join(d,h))
        if t in guides and t!=src: inl[t].add(src)
srcs=lambda t:[x for x in inl[t] if x not in ('gidsen.html',)]
rows=sorted(guides,key=lambda t:len(srcs(t)))
from collections import Counter
c=Counter(min(len(srcs(t)),10) for t in guides)
print('verdeling (inlinks excl gidsen.html):',sorted(c.items()))
print('gidsen <3 guide-inlinks (alleen van andere gidsen):')
n=0
for t in guides:
    g=[x for x in inl[t] if x.startswith('beste/')]
    if len(g)<3: n+=1; print(' ',t,len(g),len(srcs(t)))
print('totaal',n,'van',len(guides))
