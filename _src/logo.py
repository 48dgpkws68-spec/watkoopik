# -*- coding: utf-8 -*-
"""Logo A (vergrootglas met vraagteken) als SVG-onderdelen voor build.py, plus favicon en profielfoto."""

def mark(size=40, blue="#1b3fb3", orange="#ff7a3d"):
    """Beeldmerk: vergrootglas met vraagteken, viewBox 0 0 100 100."""
    return ('<svg class="logo-mark" width="%d" height="%d" viewBox="0 0 100 100" aria-hidden="true">'
            '<circle cx="42" cy="42" r="30" fill="none" stroke="%s" stroke-width="11"/>'
            '<line x1="64" y1="64" x2="86" y2="86" stroke="%s" stroke-width="13" stroke-linecap="round"/>'
            '<circle cx="88" cy="88" r="8" fill="%s"/>'
            '<text x="42" y="56" text-anchor="middle" font-family="Sora,Arial,sans-serif" font-weight="800" font-size="40" fill="%s">?</text>'
            '</svg>') % (size, size, blue, blue, orange, orange)

def lockup(size=40):
    return '<span class="logo">%s<span class="logo-word">wat<b>koop</b>ik</span></span>' % mark(size)

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
           '<rect width="100" height="100" rx="22" fill="#1b3fb3"/>'
           '<circle cx="44" cy="44" r="24" fill="none" stroke="#fff" stroke-width="9"/>'
           '<line x1="62" y1="62" x2="80" y2="80" stroke="#fff" stroke-width="11" stroke-linecap="round"/>'
           '<circle cx="82" cy="82" r="7" fill="#ff7a3d"/>'
           '<text x="44" y="55" text-anchor="middle" font-family="Arial,sans-serif" font-weight="900" font-size="32" fill="#ff7a3d">?</text>'
           '</svg>')
