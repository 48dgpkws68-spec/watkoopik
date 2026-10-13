# -*- coding: utf-8 -*-
"""Logo A (vergrootglas met vraagteken) als SVG-onderdelen voor build.py, plus favicon en profielfoto."""

def mark(size=40, blue="#1b3fb3", orange="#ff7a3d"):
    """Beeldmerk: afgerond vierkant met verloop en wit vraagteken (het eerste logo)."""
    return ('<svg class="logo-mark" width="%d" height="%d" viewBox="0 0 64 64" aria-hidden="true">'
            '<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
            '<rect width="64" height="64" rx="16" fill="url(#lg)"/>'
            '<text x="32" y="45" text-anchor="middle" font-family="Sora,Inter,Arial,sans-serif" font-weight="800" font-size="38" fill="#fff">?</text>'
            '</svg>') % (size, size, blue, orange)

def lockup(size=40):
    return '<span class="logo">%s<span class="logo-word">wat<b>koop</b>ik</span></span>' % mark(size)

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
           '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#1b3fb3"/><stop offset="1" stop-color="#ff7a3d"/></linearGradient></defs>'
           '<rect width="64" height="64" rx="16" fill="url(#g)"/>'
           '<text x="32" y="46" font-family="Arial,sans-serif" font-weight="900" font-size="40" fill="#fff" text-anchor="middle">?</text></svg>')
