# -*- coding: utf-8 -*-
"""Logo A (vergrootglas met vraagteken) als SVG-onderdelen voor build.py, plus favicon en profielfoto."""

PURPLE = "#5b3fd6"; ORANGE = "#ff7a3d"

def mark(size=40, purple=PURPLE, orange=ORANGE):
    """Beeldmerk E: prijskaartje met vinkje, viewBox 0 0 100 100."""
    return ('<svg class="logo-mark" width="%d" height="%d" viewBox="0 0 100 100" aria-hidden="true">'
            '<path d="M14 10h40l32 32-40 40L14 50z" fill="%s"/>'
            '<circle cx="30" cy="26" r="6" fill="#fff"/>'
            '<path d="M34 56l10 10 20-22" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
            '</svg>') % (size, size, purple, orange)

def lockup(size=40):
    return '<span class="logo">%s<span class="logo-word">wat<b>koop</b>ik</span></span>' % mark(size)

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
           '<rect width="100" height="100" rx="22" fill="#5b3fd6"/>'
           '<path d="M22 20h34l26 26-34 34L22 54z" fill="#fff"/>'
           '<circle cx="35" cy="33" r="5" fill="#5b3fd6"/>'
           '<path d="M38 58l9 9 17-19" fill="none" stroke="#ff7a3d" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
