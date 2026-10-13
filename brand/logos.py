# -*- coding: utf-8 -*-
"""Vier logoconcepten voor watkoopik, gerenderd op één overzichtsblad (logo-concepten.png) en los als png."""
from PIL import Image, ImageDraw, ImageFont
import os
H = os.path.dirname(os.path.abspath(__file__))
NAVY = (20, 26, 43); BLUE = (27, 63, 179); ORANGE = (255, 122, 61); GOLD = (245, 179, 36); WHITE = (255, 255, 255); BG = (246, 247, 251)
def F(name, size): return ImageFont.truetype(os.path.join(H, name), size)

def word(d, x, y, size, font="Sora.ttf", dark=NAVY, accent=BLUE):
    f = F(font, size)
    parts = [("wat", dark), ("koop", accent), ("ik", dark)]
    for t, c in parts:
        d.text((x, y), t, font=f, fill=c); x += d.textlength(t, font=f)
    return x

def concept_a(W=900, H_=300):
    """A. Vergrootglas met vraagteken + wordmark."""
    im = Image.new("RGB", (W, H_), WHITE); d = ImageDraw.Draw(im)
    cx, cy, r = 150, 140, 78
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=BLUE)
    d.ellipse((cx-r+14, cy-r+14, cx+r-14, cy+r-14), fill=WHITE)
    d.line((cx+52, cy+52, cx+112, cy+112), fill=BLUE, width=30)
    d.ellipse((cx+96, cy+96, cx+128, cy+128), fill=ORANGE)
    f = F("Sora.ttf", 96); t = "?"; w = d.textlength(t, font=f)
    d.text((cx-w/2, cy-66), t, font=f, fill=ORANGE)
    word(d, 290, 90, 100)
    return im

def concept_b(W=900, H_=300):
    """B. Tekstballon met vraagteken (vraag) die overgaat in een vinkje (antwoord)."""
    im = Image.new("RGB", (W, H_), WHITE); d = ImageDraw.Draw(im)
    x0, y0 = 60, 55
    d.rounded_rectangle((x0, y0, x0+190, y0+150), 40, fill=NAVY)
    d.polygon([(x0+40, y0+148), (x0+40, y0+195), (x0+95, y0+148)], fill=NAVY)
    f = F("Sora.ttf", 110); t = "?"; w = d.textlength(t, font=f)
    d.text((x0+95-w/2-22, y0+8), t, font=f, fill=WHITE)
    d.line((x0+118, y0+90, x0+140, y0+112, x0+178, y0+60), fill=ORANGE, width=16, joint="curve")
    word(d, 300, 90, 100, "Manrope.ttf", NAVY, ORANGE)
    return im

def concept_c(W=900, H_=300):
    """C. Boodschappentas met vinkje, warme stijl."""
    im = Image.new("RGB", (W, H_), WHITE); d = ImageDraw.Draw(im)
    x0, y0 = 70, 70
    d.rounded_rectangle((x0, y0+40, x0+170, y0+190), 28, fill=ORANGE)
    d.arc((x0+40, y0-10, x0+130, y0+90), 180, 360, fill=NAVY, width=18)
    d.line((x0+40, y0+40, x0+40, y0+60), fill=NAVY, width=18); d.line((x0+130, y0+40, x0+130, y0+60), fill=NAVY, width=18)
    d.line((x0+50, y0+115, x0+78, y0+145, x0+128, y0+85), fill=WHITE, width=18, joint="curve")
    word(d, 300, 90, 100, "Outfit.ttf", NAVY, ORANGE)
    return im

def concept_d(W=900, H_=300):
    """D. Puur typografisch: 'wat koop ik' gestapeld met oranje vraagteken als accent."""
    im = Image.new("RGB", (W, H_), NAVY); d = ImageDraw.Draw(im)
    f1 = F("PlusJakartaSans.ttf", 92); f2 = F("PlusJakartaSans.ttf", 92)
    d.text((70, 40), "wat koop", font=f1, fill=WHITE)
    d.text((70, 150), "ik", font=f2, fill=WHITE)
    x = 70 + d.textlength("ik", font=f2) + 18
    d.text((x, 136), "?", font=F("PlusJakartaSans.ttf", 110), fill=ORANGE)
    d.rounded_rectangle((x+120, 196, x+330, 212), 8, fill=GOLD)
    f3 = F("Manrope.ttf", 26); d.text((x+120, 222), "onafhankelijke top 10-gidsen", font=f3, fill=(199, 203, 224))
    return im

ims = [("A · Vergrootglas", concept_a()), ("B · Vraag wordt antwoord", concept_b()), ("C · Boodschappentas", concept_c()), ("D · Typografisch", concept_d())]
sheet = Image.new("RGB", (1860, 760), BG); d = ImageDraw.Draw(sheet); lab = F("Manrope.ttf", 28)
for i, (name, im) in enumerate(ims):
    x, y = 30 + (i % 2) * 920, 30 + (i // 2) * 370
    d.text((x, y), name, font=lab, fill=NAVY)
    sheet.paste(im, (x, y+40)); d.rectangle((x, y+40, x+899, y+339), outline=(228, 231, 239), width=2)
    im.save(os.path.join(H, "logo-%s.png" % name[0]))
sheet.save(os.path.join(H, "logo-concepten.png")); print("ok")
