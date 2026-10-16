"""TikTok photo-mode carousels (1080x1920) in Looks Like Luxe chocolate/gold. No prices. Outfit/room 'looks' with cut-outs.
Usage: py tools/make_tiktok_carousels.py   -> tiktok/<set>/slide-1..N.png"""
import os, sys
sys.path.insert(0, 'tools')
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from make_collage_pins import cutout, shadow, tile, P, font, GOLD, CHOC, CREAM

W, H = 1080, 1920
GOLD2 = (236, 214, 170)
DISC = 'As an Amazon Associate I earn from qualifying purchases.'


def bg():
    b = Image.new('RGB', (W, H))
    for x in range(0, W, P):
        for y in range(0, H, P): b.paste(tile, (x, y))
    b = ImageEnhance.Brightness(b).enhance(0.55)
    base = Image.new('RGB', (W, H), CHOC)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse((-300, 250, W + 300, H - 250), fill=200)
    return Image.composite(b, base, m.filter(ImageFilter.GaussianBlur(180))).convert('RGBA')


def center(d, t, y, f, fill, track=0):
    if track:
        tw = sum(d.textlength(c, font=f) + track for c in t) - track; x = (W - tw) / 2
        for c in t: d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + track
    else: d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)


def place(im, path, cx, cy, size, rot, card=False):
    c = cutout(path, card); c.thumbnail((size, size)); c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh, pad = shadow(c, False)
    im.alpha_composite(sh, (int(cx - sh.width / 2), int(cy - sh.height / 2))); im.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2)))


def header(d, kicker, lines, y=110, size=120):
    center(d, kicker, y, font('BOD_B.TTF', 38), GOLD2, track=10)
    y += 80
    for ln in lines:
        s = size
        while d.textlength(ln, font=font('BOD_I.TTF', s)) > W - 120: s -= 4
        center(d, ln, y, font('BOD_I.TTF', s), GOLD); y += s + 10
    return y


def footer(d, text='swipe for the looks  >>'):
    center(d, text, 1760, font('BOD_I.TTF', 48), CREAM)
    center(d, 'LOOKS LIKE LUXE', 1840, font('BOD_B.TTF', 30), GOLD2, track=9)


def build(name, cover, looks, end_lines, kicker, folder):
    os.makedirs(f'tiktok/{name}', exist_ok=True)
    # cover: 8 cut-outs scattered
    im = bg(); d = ImageDraw.Draw(im)
    y = header(d, kicker, cover['title'])
    slots = [(250, 740, 380, -4), (830, 760, 380, 3), (300, 1120, 430, 3), (790, 1150, 420, -3), (230, 1530, 340, -3), (560, 1540, 300, 2), (860, 1530, 330, 4)]
    for f, (cx, cy, sz, rot) in zip(cover['imgs'], slots): place(im, f'{folder}/{f}', cx, cy, sz, rot)
    d = ImageDraw.Draw(im); center(d, cover['sub'], 1745, font('BOD_I.TTF', 50), CREAM); center(d, 'LOOKS LIKE LUXE', 1840, font('BOD_B.TTF', 30), GOLD2, track=9)
    im.convert('RGB').save(f'tiktok/{name}/slide-1.png')
    # looks
    for n, lk in enumerate(looks, 2):
        im = bg(); d = ImageDraw.Draw(im)
        center(d, kicker, 110, font('BOD_B.TTF', 38), GOLD2, track=10)
        d.ellipse((W / 2 - 55, 190, W / 2 + 55, 300), fill=GOLD)
        nf = font('BOD_B.TTF', 64); t = str(n - 1); d.text((W / 2 - d.textlength(t, font=nf) / 2, 212), t, font=nf, fill=CHOC)
        s = 110
        while d.textlength(lk['title'], font=font('BOD_I.TTF', s)) > W - 120: s -= 4
        center(d, lk['title'], 330, font('BOD_I.TTF', s), GOLD)
        for f, (cx, cy, sz, rot) in zip(lk['imgs'], lk['slots']): place(im, f'{folder}/{f}', cx, cy, sz, rot)
        d = ImageDraw.Draw(im)
        yy = 1550
        for ln in lk['names']:
            center(d, ln, yy, font('BOD_R.TTF', 44), CREAM); yy += 62
        footer(d)
        im.convert('RGB').save(f'tiktok/{name}/slide-{n}.png')
    # end
    im = bg(); d = ImageDraw.Draw(im)
    y = 520
    for ln in end_lines:
        center(d, ln, y, font('BOD_I.TTF', 110), GOLD); y += 130
    d.line((W / 2 - 90, y + 30, W / 2 + 90, y + 30), fill=GOLD, width=3)
    center(d, 'Every piece is on my', y + 90, font('BOD_I.TTF', 62), CREAM); center(d, 'Amazon storefront', y + 170, font('BOD_I.TTF', 62), CREAM)
    bw = 640; d.rounded_rectangle(((W - bw) / 2, y + 330, (W + bw) / 2, y + 440), radius=55, fill=GOLD)
    center(d, 'LINK IN BIO', y + 359, font('BOD_B.TTF', 52), CHOC, track=6)
    center(d, DISC, 1780, font('BOD_R.TTF', 28), (190, 170, 140))
    im.convert('RGB').save(f'tiktok/{name}/slide-{len(looks) + 2}.png')
    print('wrote', name)


two = [(300, 880, 520, -3), (790, 1100, 440, 3)]
three = [(270, 800, 470, -3), (800, 830, 470, 3), (540, 1280, 420, 0)]

# fall outfits: images in images/blog/choc-style-v2 (01 halter 02 trench 03 moto 04 ruched shirt 05 jorts 06 flannel 07 gladiator boot 08 fleece 09 tote 10 bomber 11 knee boot)
build('fall-fits-carousel',
      dict(title=['Chocolate Brown', 'Fall Fits'], sub='a little edgy. all Amazon.', imgs=['02.jpg', '03.jpg', '05.jpg', '10.jpg', '11.jpg', '09.jpg', '08.jpg']),
      [dict(title='The Moto Moment', imgs=['03.jpg', '05.jpg', '11.jpg'], slots=three, names=['Faux leather moto jacket', 'Baggy low-rise jorts', 'Knee-high block heel boots']),
       dict(title='Brown on Brown', imgs=['02.jpg', '04.jpg', '09.jpg'], slots=three, names=['Long faux leather trench', 'Ruched button-up top', 'Slouchy hobo bag']),
       dict(title='Night Out Edit', imgs=['01.jpg', '10.jpg', '07.jpg'], slots=three, names=['Lace-up leather halter', 'Oversized leather bomber', 'Studded gladiator heels']),
       dict(title='Cozy but Cool', imgs=['08.jpg', '06.jpg', '05.jpg'], slots=three, names=['Cropped fleece jacket', 'Plaid flannel crop top', 'Baggy denim jorts'])],
      ['Chocolate Brown', 'Fall Fits'], 'AMAZON FALL STYLE', 'images/blog/choc-style-v2')

# home decor: images/blog/choc-home 01..08
build('home-decor-carousel',
      dict(title=['Looks Like Ralph', 'Lauren. Is Amazon.'], sub='chocolate brown home edit', imgs=['01-chunky-knit-throw.jpg', '04-faux-fur-rug.jpg', '02-velvet-pillow-covers.jpg', '05-cordless-lamp.jpg', '06-woven-baskets.jpg', '07-wood-candle-holders.jpg', '03-boucle-pillow-covers.jpg']),
      [dict(title='The Living Room', imgs=['01-chunky-knit-throw.jpg', '02-velvet-pillow-covers.jpg', '03-boucle-pillow-covers.jpg'], slots=three, names=['Chunky knit throw', 'Velvet pillow covers', 'Boucle pillow covers']),
       dict(title='The Bedroom', imgs=['04-faux-fur-rug.jpg', '08-sherpa-pillow-covers.jpg', '05-cordless-lamp.jpg'], slots=three, names=['Faux fur rug', 'Sherpa pillow covers', 'Cordless lamp']),
       dict(title='The Finishing Touches', imgs=['06-woven-baskets.jpg', '07-wood-candle-holders.jpg'], slots=two, names=['Woven baskets', 'Wood candle holders'])],
      ['Looks Like Ralph', 'Lauren. Is Amazon.'], 'AMAZON HOME FINDS', 'images/blog/choc-home')
