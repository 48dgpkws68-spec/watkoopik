# -*- coding: utf-8 -*-
"""Deelafbeeldingen (1200x630) voor og:image. Maakt alleen ontbrekende bestanden aan."""
import os, io, urllib.request
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "brand", "Sora.ttf")
FONT2 = os.path.join(HERE, "..", "brand", "Manrope.ttf")

def _font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    return f

def _hex(c):
    c = c.lstrip("#"); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))

def _wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def _fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=15).read())).convert("RGB")
    except Exception:
        return None

def card(path, title, kicker, color, image_url=None):
    if os.path.exists(path): return False
    col = _hex(color or "#1f6feb")
    im = Image.new("RGB", (W, H), (250, 248, 244))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 18, H], fill=col)
    text_w = 640
    prod = _fetch(image_url) if image_url else None
    if prod:
        box = Image.new("RGB", (440, 470), (255, 255, 255))
        prod.thumbnail((400, 430))
        box.paste(prod, ((440 - prod.width) // 2, (470 - prod.height) // 2))
        im.paste(box, (W - 440 - 60, 80))
        d.rounded_rectangle([W - 440 - 60, 80, W - 60, 550], radius=24, outline=(230, 226, 218), width=3)
    else:
        text_w = 1020
    fk = _font(FONT2, 30, 700)
    d.text((80, 80), kicker.upper(), font=fk, fill=col)
    size = 76
    while True:
        ft = _font(FONT, size, 800)
        lines = _wrap(d, title, ft, text_w)
        if (len(lines) <= 4 and max(d.textlength(l, font=ft) for l in lines) <= text_w) or size <= 48: break
        size -= 6
    y = 140
    for ln in lines:
        d.text((80, y), ln, font=ft, fill=(18, 26, 51)); y += int(size * 1.18)
    fb = _font(FONT2, 32, 700)
    d.rounded_rectangle([80, 500, 80 + d.textlength("watkoopik.nl", font=fb) + 48, 560], radius=30, fill=(18, 26, 51))
    d.text((104, 510), "watkoopik.nl", font=fb, fill=(255, 255, 255))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "JPEG", quality=84, optimize=True, progressive=True)
    return True
