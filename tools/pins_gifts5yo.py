from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
W, H = 1000, 1500
GOLD = (201, 162, 94); CHOC = (43, 26, 18); CREAM = (250, 244, 234); LIGHT = (236, 214, 170); BLUSH = (248, 228, 226)
F = 'C:/Windows/Fonts/'
font = lambda n, s: ImageFont.truetype(F + n, s)
IMGS = ['01-mixies.jpg', '02-hatchimals.jpg', '03-tent.jpg', '04-moonlite.jpg', '05-unicorn.jpg', '06-squishmallow.jpg', '07-toniebox.jpg', '08-barbie.jpg']

src = Image.open('brand/profile-monogram.png').convert('RGB')
P = 235
tile = Image.new('RGB', (P, P)); tile.paste(src.crop((0, 100, 190, 100 + P)), (0, 0)); tile.paste(src.crop((895, 100, 940, 100 + P)), (190, 0))


def patbg():
    bg = Image.new('RGB', (W, H))
    for x in range(0, W, P):
        for y in range(0, H, P): bg.paste(tile, (x, y))
    return ImageEnhance.Brightness(bg).enhance(0.8)


def card(name, size, pad=10):
    im = Image.open(f'images/blog/gifts-5yo/{name}').convert('RGB')
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


def grid(bg, d, cell, gap, x0, y0, ring, nfill=GOLD, ntxt=CHOC):
    for i, n in enumerate(IMGS):
        c, m = card(n, (cell, cell)); x = x0 + (i % 3) * (cell + gap); y = y0 + (i // 3) * (cell + gap)
        bg.paste(c, (x, y), m); d.rounded_rectangle((x, y, x + cell, y + cell), radius=26, outline=ring, width=3)
        badge(d, x + 10, y + 10, i + 1, nfill, ntxt)
    # 9th cell: "more inside"
    i = 8; x = x0 + (i % 3) * (cell + gap); y = y0 + (i // 3) * (cell + gap)
    d.rounded_rectangle((x, y, x + cell, y + cell), radius=26, fill=ring if ring != GOLD else GOLD)


# A: blush, chocolate type
bg = Image.new('RGB', (W, H), BLUSH); d = ImageDraw.Draw(bg)
d.rectangle((24, 24, W - 24, H - 24), outline=GOLD, width=3)
center(d, 'THE GIFT EDIT', 70, font('BOD_R.TTF', 34), (155, 91, 47))
f = font('BOD_I.TTF', 104); center(d, 'Gifts for', 112, f, CHOC); center(d, '5-Year-Old Girls', 218, f, CHOC)
cell, gap = 270, 20; x0 = (W - (3 * cell + 2 * gap)) // 2; y0 = 400
grid(bg, d, cell, gap, x0, y0, GOLD)
i = 8; x = x0 + 2 * (cell + gap); y = y0 + 2 * (cell + gap)
ft = font('BOD_I.TTF', 44); d.text((x + cell / 2 - d.textlength('zero', font=ft) / 2, y + 70), 'zero', font=ft, fill=CHOC)
fs = font('BOD_B.TTF', 44); t = 'crayons'; d.text((x + cell / 2 - d.textlength(t, font=fs) / 2, y + 125), t, font=fs, fill=CHOC)
cta(d, 1352, CHOC, GOLD, 'READ THE GUIDE')
bg.save('pins/gifts5yo-v1-blush-grid.png')

# B: chocolate pattern, hero barbie + row
bg = patbg(); d = ImageDraw.Draw(bg, 'RGBA'); d.rectangle((0, 0, W, H), fill=(43, 26, 18, 140))
center(d, 'WAIT, THEY MAKE THIS?!', 64, font('BOD_R.TTF', 34), LIGHT)
f = font('BOD_I.TTF', 96)
for k, l in enumerate(['8 Gifts for', '5-Year-Old Girls', "She'll Scream For"]): center(d, l, 110 + k * 100, f, GOLD)
c, m = card('01-mixies.jpg', (880, 480), 12); bg.paste(c, (60, 440), m); d.rounded_rectangle((60, 440, 940, 920), radius=26, outline=GOLD, width=4)
badge(d, 76, 456, 1)
sm = ['02-hatchimals.jpg', '03-tent.jpg', '04-moonlite.jpg', '05-unicorn.jpg']; nums = [2, 3, 4, 5]
for k, n in enumerate(sm):
    c, m = card(n, (205, 205), 8); x = 60 + k * 225; bg.paste(c, (x, 950), m); d.rounded_rectangle((x, 950, x + 205, 1155), radius=26, outline=GOLD, width=3); badge(d, x + 8, 958, nums[k])
center(d, 'zero crayons. zero regrets.', 1190, font('BOD_I.TTF', 46), LIGHT)
cta(d, 1290, GOLD, CHOC, 'GET THE LIST')
bg.save('pins/gifts5yo-v2-chocolate-hero.png')

# C: cream editorial, 2 columns x 4 rows
bg = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(bg)
d.rectangle((24, 24, W - 24, H - 24), outline=GOLD, width=3)
center(d, 'THE LUXE LIST', 66, font('BOD_R.TTF', 34), (155, 91, 47))
f = font('BOD_I.TTF', 100)
for k, l in enumerate(['Gifts for', '5-Year-Old Girls']): center(d, l, 106 + k * 104, f, CHOC)
center(d, "(wait, they make THIS?!)", 330, font('BOD_I.TTF', 46), (155, 91, 47))
cw, ch = 430, 205; g = 20; x0 = (W - (2 * cw + g)) // 2; y0 = 430
for i, n in enumerate(IMGS):
    c, m = card(n, (cw, ch), 8); x = x0 + (i % 2) * (cw + g); y = y0 + (i // 2) * (ch + g)
    bg.paste(c, (x, y), m); d.rounded_rectangle((x, y, x + cw, y + ch), radius=26, outline=GOLD, width=3); badge(d, x + 10, y + 10, i + 1)
cta(d, 1340, CHOC, GOLD, 'SHOP ALL 8')
bg.save('pins/gifts5yo-v3-cream-list.png')
print('ok')
