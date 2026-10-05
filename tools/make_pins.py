"""Make 3 Pinterest pin designs (1000x1500) for a post.
Usage:  python tools/make_pins.py gifts-for-5-year-old-girls [more-slugs ...]
Reads posts/<slug>.json (needs a "pin" block) and the product photos referenced by each product's "image".
Writes pins/<slug>-v1-grid.png, -v2-hero.png, -v3-list.png
"pin" block fields: kicker, h1 (list of 2 lines), sub (italic subtitle for v3), hero_kicker, hero_lines (list of 3),
  hero_tag (small line under hero), cta (button text), hero_index (which product is the hero, default 0),
  small_idx (4 product indexes for the strip in v2, default [1,2,3,4])"""
import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

W, H = 1000, 1500
GOLD = (201, 162, 94); CHOC = (43, 26, 18); CREAM = (250, 244, 234); LIGHT = (236, 214, 170); BLUSH = (248, 228, 226); RUST = (155, 91, 47)
F = 'C:/Windows/Fonts/'
font = lambda n, s: ImageFont.truetype(F + n, s)

src = Image.open('brand/profile-monogram.png').convert('RGB')
P = 235
tile = Image.new('RGB', (P, P)); tile.paste(src.crop((0, 100, 190, 100 + P)), (0, 0)); tile.paste(src.crop((895, 100, 940, 100 + P)), (190, 0))


def patbg():
    bg = Image.new('RGB', (W, H))
    for x in range(0, W, P):
        for y in range(0, H, P): bg.paste(tile, (x, y))
    return ImageEnhance.Brightness(bg).enhance(0.8)


def card(path, size, pad=10):
    im = Image.open(path).convert('RGB')
    c = Image.new('RGB', size, (255, 255, 255)); inner = ImageOps.contain(im, (size[0] - 2 * pad, size[1] - 2 * pad))
    c.paste(inner, ((size[0] - inner.width) // 2, (size[1] - inner.height) // 2))
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=26, fill=255)
    return c, m


def center(d, t, y, f, fill): d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)


def badge(d, x, y, n, fill=GOLD, txt=CHOC):
    d.ellipse((x, y, x + 54, y + 54), fill=fill); f = font('BOD_B.TTF', 30)
    d.text((x + 27 - d.textlength(str(n), font=f) / 2, y + 7), str(n), font=f, fill=txt)


def cta(d, y, fill, txtfill, label):
    f = font('BOD_R.TTF', 38); tw = d.textlength(label, font=f); full = tw + 60; ax = (W - full) / 2; bw = full + 90
    d.rounded_rectangle(((W - bw) / 2, y, (W + bw) / 2, y + 86), radius=43, fill=fill)
    d.text((ax, y + 20), label, font=f, fill=txtfill); x0 = ax + tw + 18; cy = y + 43
    for a, b in [((x0, cy), (x0 + 34, cy)), ((x0 + 22, cy - 12), (x0 + 36, cy)), ((x0 + 22, cy + 12), (x0 + 36, cy))]: d.line((a, b), fill=txtfill, width=4)


def fit(d, text, name, size, maxw):
    while d.textlength(text, font=font(name, size)) > maxw and size > 40: size -= 4
    return font(name, size)


def build(slug):
    post = json.load(open(f'posts/{slug}.json', encoding='utf-8'))
    pin = post['pin']; imgs = [p['image'] for p in post['products']]
    n = len(imgs)
    # v1 blush grid (3x3 with a final text tile)
    bg = Image.new('RGB', (W, H), BLUSH); d = ImageDraw.Draw(bg)
    d.rectangle((24, 24, W - 24, H - 24), outline=GOLD, width=3)
    center(d, pin['kicker'], 70, font('BOD_R.TTF', 34), RUST)
    for k, l in enumerate(pin['h1']): center(d, l, 112 + k * 106, fit(d, l, 'BOD_I.TTF', 104, 880), CHOC)
    cell, gap = 270, 20; x0 = (W - (3 * cell + 2 * gap)) // 2; y0 = 400
    for i in range(9):
        x = x0 + (i % 3) * (cell + gap); y = y0 + (i // 3) * (cell + gap)
        if i < min(n, 8):
            c, m = card(imgs[i], (cell, cell)); bg.paste(c, (x, y), m); d.rounded_rectangle((x, y, x + cell, y + cell), radius=26, outline=GOLD, width=3); badge(d, x + 10, y + 10, i + 1)
        else:
            d.rounded_rectangle((x, y, x + cell, y + cell), radius=26, fill=GOLD)
            a, b = pin.get('tile', ['zero', 'regrets'])
            fa = font('BOD_I.TTF', 44); fb = font('BOD_B.TTF', 44)
            d.text((x + cell / 2 - d.textlength(a, font=fa) / 2, y + 70), a, font=fa, fill=CHOC); d.text((x + cell / 2 - d.textlength(b, font=fb) / 2, y + 125), b, font=fb, fill=CHOC)
    cta(d, 1352, CHOC, GOLD, pin.get('cta1', 'READ THE GUIDE'))
    bg.save(f'pins/{slug}-v1-grid.png')
    # v2 chocolate hero
    bg = patbg(); d = ImageDraw.Draw(bg, 'RGBA'); d.rectangle((0, 0, W, H), fill=(43, 26, 18, 140))
    center(d, pin['hero_kicker'], 64, font('BOD_R.TTF', 34), LIGHT)
    for k, l in enumerate(pin['hero_lines']): center(d, l, 110 + k * 100, fit(d, l, 'BOD_I.TTF', 96, 900), GOLD)
    hi = pin.get('hero_index', 0)
    c, m = card(imgs[hi], (880, 480), 12); bg.paste(c, (60, 440), m); d.rounded_rectangle((60, 440, 940, 920), radius=26, outline=GOLD, width=4); badge(d, 76, 456, hi + 1)
    for k, idx in enumerate(pin.get('small_idx', [1, 2, 3, 4])):
        c, m = card(imgs[idx], (205, 205), 8); x = 60 + k * 225; bg.paste(c, (x, 950), m); d.rounded_rectangle((x, 950, x + 205, 1155), radius=26, outline=GOLD, width=3); badge(d, x + 8, 958, idx + 1)
    center(d, pin.get('hero_tag', ''), 1190, font('BOD_I.TTF', 46), LIGHT)
    cta(d, 1290, GOLD, CHOC, pin.get('cta2', 'GET THE LIST'))
    bg.save(f'pins/{slug}-v2-hero.png')
    # v3 cream list
    bg = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(bg)
    d.rectangle((24, 24, W - 24, H - 24), outline=GOLD, width=3)
    center(d, pin.get('kicker3', 'THE LUXE LIST'), 66, font('BOD_R.TTF', 34), RUST)
    for k, l in enumerate(pin['h1']): center(d, l, 106 + k * 104, fit(d, l, 'BOD_I.TTF', 100, 900), CHOC)
    center(d, pin['sub'], 330, font('BOD_I.TTF', 46), RUST)
    cw, ch = 430, 205; g = 20; x0 = (W - (2 * cw + g)) // 2; y0 = 430
    for i in range(min(n, 8)):
        c, m = card(imgs[i], (cw, ch), 8); x = x0 + (i % 2) * (cw + g); y = y0 + (i // 2) * (ch + g)
        bg.paste(c, (x, y), m); d.rounded_rectangle((x, y, x + cw, y + ch), radius=26, outline=GOLD, width=3); badge(d, x + 10, y + 10, i + 1)
    cta(d, 1340, CHOC, GOLD, pin.get('cta3', 'SHOP ALL 8'))
    bg.save(f'pins/{slug}-v3-list.png')
    print('pins made for', slug)


if __name__ == '__main__':
    for s in sys.argv[1:]: build(s)
