"""Make 'Amazon finds' style collage pins (cut-out products scattered on a monogram background).
Pattern copied from the top Pinterest Amazon-storefront pages: product cut-outs, small 'AMAZON FINDS' tag,
big serif title, 'all on my storefront' line, soft CTA. Styled in Looks Like Luxe chocolate / gold / cream.
Usage: python tools/make_collage_pins.py gifts-for-her [cozy-fall ...]
Writes pins/collage-<key>-choc.png and pins/collage-<key>-cream.png (1000x1500)."""
import sys, glob, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps

W, H = 1000, 1500
GOLD = (201, 162, 94); CHOC = (43, 26, 18); CREAM = (250, 244, 234)
F = 'C:/Windows/Fonts/'
font = lambda n, s: ImageFont.truetype(F + n, s)

# key -> (image folder, kicker, title lines, sub line, cta)
SETS = {
    'gifts-for-her': ('images/gifts-for-her', 'AMAZON FINDS', ['Gifts for Her'], 'rich-girl taste. real-girl budget.', 'SHOP THE LIST'),
    'clean-girl': ('images/blog/clean-girl', 'AMAZON BEAUTY FINDS', ['Clean Girl', 'Beauty Finds'], '', 'SHOP THE LIST'),
    'host-hostess': ('images/blog/host-hostess', 'AMAZON FINDS', ['Host & Hostess', 'Gifts'], '', 'SHOP THE LIST'),
    'gifts-5yo': ('images/blog/gifts-5yo', 'AMAZON TOY FINDS', ['Gifts for 5 Year', 'Old Girls'], '', 'SHOP THE LIST'),
    'gifts-8-10': ('images/blog/gifts-8-10', 'AMAZON TWEEN FINDS', ['Gifts for 8-10', 'Year Old Girls'], '', 'SHOP THE LIST'),
    'gifts-20s': ('images/blog/gifts-20s', 'AMAZON GIFT FINDS', ['Gifts for Women', 'in Their 20s'], '', 'SHOP THE LIST'),
    'christmas-decor': ('images/blog/christmas-decor', 'AMAZON HOME FINDS', ['Christmas Decor', 'That Looks Designer'], '', 'SHOP THE LIST'),
    'gifts-teacher': ('images/blog/gifts-teacher', 'AMAZON GIFT FINDS', ['Teacher Gifts', "That Aren't Mugs"], '', 'SHOP THE LIST'),
    'gifts-mom': ('images/blog/gifts-mom', 'AMAZON GIFT FINDS', ['Christmas Gifts', 'for Mom'], '', 'SHOP THE LIST'),
    'cozy-fall': ('images/cozy-fall', 'AMAZON HOME FINDS', ['Cozy Fall', 'Home Decor'], 'looks designer. isn\'t.', 'SHOP THE LIST'),
}

src = Image.open('brand/profile-monogram.png').convert('RGB')
P = 235
tile = Image.new('RGB', (P, P)); tile.paste(src.crop((0, 100, 190, 100 + P)), (0, 0)); tile.paste(src.crop((895, 100, 940, 100 + P)), (190, 0))


def patbg(cream):
    bg = Image.new('RGB', (W, H))
    for x in range(0, W, P):
        for y in range(0, H, P): bg.paste(tile, (x, y))
    if cream:   # faint gold-on-cream version of the monogram
        return Image.blend(Image.new('RGB', (W, H), CREAM), bg, 0.20)
    return ImageEnhance.Brightness(bg).enhance(0.8)


def is_clean(im):
    # product-on-white shots have an (almost) all-white border; lifestyle photos do not
    w, h = im.size; px = im.load(); pts = [(x, 0) for x in range(0, w, 6)] + [(x, h - 1) for x in range(0, w, 6)] + [(0, y) for y in range(0, h, 6)] + [(w - 1, y) for y in range(0, h, 6)]
    return sum(1 for p in pts if min(px[p]) > 238) / len(pts) >= 0.95


def photo_card(im, size=620):
    im = ImageOps.contain(im, (size, size)); pad = 12
    c = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (255, 255, 255, 255)); c.paste(im, (pad, pad))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=22, fill=255)
    c.putalpha(m); return c


CARDS = {'clean-girl': {2, 6}, 'gifts-mom': {1, 2, 6, 7}, 'gifts-teacher': {2, 3, 4, 5, 6, 7}, 'christmas-decor': {3, 4, 5, 6, 7}}   # product shots with white parts that cut out badly -> rounded photo cards


def cutout(path, force_card=False):
    im = Image.open(path).convert('RGB')
    im.thumbnail((900, 900))
    if force_card or not is_clean(im): return photo_card(im)
    probe = im.copy()
    for xy in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]:
        ImageDraw.floodfill(probe, xy, (255, 0, 255), thresh=12)
    px = probe.load(); a = Image.new('L', im.size, 255); ap = a.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y] == (255, 0, 255): ap[x, y] = 0
    a = a.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.3))
    out = im.convert('RGBA'); out.putalpha(a)
    return out.crop(out.getbbox())


def shadow(img, cream):
    pad = 40
    sh = Image.new('RGBA', (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    al = Image.new('L', sh.size, 0); al.paste(img.split()[3], (pad, pad + 14))
    al = al.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * (0.22 if cream else 0.55)))
    sh.putalpha(al); return sh, pad


# 3-2-3 scattered layout: (cx, cy, max size, rotation)
SLOTS = [(190, 520, 320, -4), (500, 490, 300, 2), (815, 530, 320, 4),
         (330, 880, 380, 3), (675, 880, 380, -3),
         (190, 1205, 310, 3), (500, 1215, 310, -2), (815, 1205, 310, -4)]


def build(key, cream):
    folder, kicker, title, sub, cta = SETS[key]
    files = sorted(glob.glob(folder + '/0*.jpg'))[:7 if key == 'gifts-8-10' else 8]   # 8-10 list is missing the roller skates (#8)
    bg = patbg(cream).convert('RGBA')
    ink = CHOC if cream else GOLD; ink2 = (122, 84, 52) if cream else (236, 214, 170)
    for i, (f, (cx, cy, sz, rot)) in enumerate(zip(files, SLOTS)):
        c = cutout(f, i in CARDS.get(key, set())); c.thumbnail((sz, sz))
        c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
        sh, pad = shadow(c, cream)
        bg.alpha_composite(sh, (cx - sh.width // 2, cy - sh.height // 2))
        bg.alpha_composite(c, (cx - c.width // 2, cy - c.height // 2))
    d = ImageDraw.Draw(bg)
    def center(t, y, f, fill, track=0):
        if track:
            tw = sum(d.textlength(ch, font=f) + track for ch in t) - track; x = (W - tw) / 2
            for ch in t: d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track
        else: d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)
    center(kicker, 62, font('BOD_B.TTF', 34), ink2, track=9)
    y = 112
    ts = 128 if len(title) == 1 else 104
    for line in title:
        center(line, y, font('BOD_I.TTF', ts), ink); y += ts
    sy = y + 12
    if len(title) == 1: center(sub, sy, font('BOD_I.TTF', 40), ink2)   # two-line titles skip the tagline (no room)
    # cta pill
    f = font('BOD_B.TTF', 38); label = cta; tw = d.textlength(label, font=f); bw = tw + 150
    pill = CHOC if cream else GOLD; txt = GOLD if cream else CHOC
    d.rounded_rectangle(((W - bw) / 2, 1368, (W + bw) / 2, 1454), radius=43, fill=pill)
    d.text(((W - tw) / 2 - 22, 1388), label, font=f, fill=txt)
    x0 = (W + tw) / 2 - 2; cy = 1411
    for a, b in [((x0, cy), (x0 + 34, cy)), ((x0 + 22, cy - 12), (x0 + 36, cy)), ((x0 + 22, cy + 12), (x0 + 36, cy))]: d.line((a, b), fill=txt, width=4)
    out = f'pins/collage-{key}-{"cream" if cream else "choc"}.png'
    bg.convert('RGB').save(out); print('wrote', out)


if __name__ == '__main__':
    for k in sys.argv[1:]:
        build(k, False); build(k, True)
