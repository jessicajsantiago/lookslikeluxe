"""Faceless 9:16 'list scroll' videos for Reels / Shorts / TikTok in Looks Like Luxe chocolate + gold.
Hook card -> 8 product cards (Ken Burns zoom, number badge, one-liner) -> end card. No prices (Amazon rule).
Usage: python tools/make_list_videos.py gifts-mom [gifts-teacher christmas-decor]
Writes videos/<key>.mp4 (1080x1920, ~25s, silent AAC track so every platform accepts it; add trending audio in-app)."""
import sys, subprocess, os, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
GOLD = (201, 162, 94); CHOC = (43, 26, 18); CREAM = (250, 244, 234); GOLD2 = (236, 214, 170)
F = 'C:/Windows/Fonts/'
font = lambda n, s: ImageFont.truetype(F + n, s)
DISC = 'As an Amazon Associate I earn from qualifying purchases.'

VIDEOS = {
    'gifts-mom': dict(
        folder='images/blog/gifts-mom', kicker='AMAZON FINDS', hook=['Christmas Gifts', 'for Mom'], hook_sub="that aren't a candle",
        items=[('Revlon One-Step Styler', 'Salon blowout. Zero salon appointment.'),
               ('Frameo Digital Picture Frame', 'Every grandkid photo, on rotation.'),
               ('Click & Grow Smart Garden', 'Fresh herbs. No green thumb required.'),
               ('Ninja CREAMi', "Homemade ice cream. You're her favorite now."),
               ('Lodge Enamel Dutch Oven', "The pot she'll hand down someday."),
               ('KitchenAid Stand Mixer', 'The forever mixer.'),
               ('Ultrasonic Jewelry Cleaner', 'Old rings, suddenly sparkly.'),
               ('Heated Sherpa Throw', 'Warm, plaid, practically a hug.')]),
    'gifts-teacher': dict(
        folder='images/blog/gifts-teacher', kicker='AMAZON FINDS', hook=['Teacher Gifts', "That Aren't Mugs"], hook_sub='she will actually use these',
        items=[('YETI Rambler Tumbler', 'For the coffee she never finishes hot.'),
               ('Owala FreeSip Bottle', 'Sip or swig. Her call.'),
               ('UGG Tasman Slippers', 'A little luxury under the desk.'),
               ('Leather Laptop Tote', 'Carries the grading and the glam.'),
               ('13-Piece Spa Basket', 'Self-care, already gift-wrapped.'),
               ('Rechargeable Hand Warmers', 'For that freezing classroom.'),
               ('Candle Warmer Lamp', 'The scent without the flame.'),
               ('Kindle Paperwhite', 'Summer reading, sorted.')]),
    'christmas-decor': dict(
        folder='images/blog/christmas-decor', kicker='AMAZON HOME FINDS', hook=['Christmas Decor', 'That Looks Designer'], hook_sub='rich-girl taste. real-girl budget.',
        items=[('Pre-Lit 7.5ft Tree', 'The magazine-cover tree. Remote included.'),
               ('Gingerbread Nutcracker', 'One very dramatic mantel guard.'),
               ('Candy Soldier Nutcracker', 'A little sweetness, a lot of drama.'),
               ('Lighted Ceramic Village', 'A glowing little town for your sideboard.'),
               ('Gold Mercury Ornaments', 'Shimmer that looks pricier than it is.'),
               ('Flameless Taper Candles', 'Candlelight, zero fire risk.'),
               ('Burgundy Velvet Bows', 'Your tree, wearing velvet.'),
               ('Gold Reindeer Pair', 'A little brass in the lineup.')]),
}

# monogram background tile (same trick as the collage pins)
src = Image.open('brand/profile-monogram.png').convert('RGB')
P = 235
tile = Image.new('RGB', (P, P)); tile.paste(src.crop((0, 100, 190, 100 + P)), (0, 0)); tile.paste(src.crop((895, 100, 940, 100 + P)), (190, 0))


def background():
    bg = Image.new('RGB', (W, H))
    for x in range(0, W, P):
        for y in range(0, H, P): bg.paste(tile, (x, y))
    bg = ImageEnhance.Brightness(bg).enhance(0.55)
    # vignette toward solid chocolate so text stays readable
    base = Image.new('RGB', (W, H), CHOC)
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse((-300, 200, W + 300, H - 200), fill=210)
    mask = mask.filter(ImageFilter.GaussianBlur(180))
    return Image.composite(bg, base, mask)


BG = None


def center(d, t, y, f, fill, track=0):
    if track:
        tw = sum(d.textlength(ch, font=f) + track for ch in t) - track; x = (W - tw) / 2
        for ch in t: d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track
    else: d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)


def wrap_center(d, t, y, f, fill, width_px, gap=10):
    words, lines, cur = t.split(), [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if d.textlength(trial, font=f) <= width_px: cur = trial
        else: lines.append(cur); cur = w
    lines.append(cur)
    for ln in lines:
        center(d, ln, y, f, fill); y += f.size + gap
    return y


def photo_card(path, size=820):
    im = Image.open(path).convert('RGB'); im = ImageOps.contain(im, (size, size)); pad = 16
    c = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (255, 255, 255, 255)); c.paste(im, (pad, pad))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=34, fill=255)
    c.putalpha(m)
    sh = Image.new('RGBA', (c.width + 160, c.height + 160), (0, 0, 0, 0))
    al = Image.new('L', sh.size, 0); al.paste(c.split()[3], (80, 96)); al = al.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.6))
    sh.putalpha(al); sh.alpha_composite(c, (80, 80))
    return sh


def static_frame(kind, **k):
    """Background + all text for a segment (photo is composited per-frame for the zoom)."""
    im = BG.copy().convert('RGBA'); d = ImageDraw.Draw(im)
    if kind == 'hook':
        center(d, k['kicker'], 520, font('BOD_B.TTF', 44), GOLD2, track=12)
        y = 620
        hs = 150
        while max(d.textlength(ln, font=font('BOD_I.TTF', hs)) for ln in k['hook']) > W - 140: hs -= 4   # fit the widest line
        for ln in k['hook']:
            center(d, ln, y, font('BOD_I.TTF', hs), GOLD); y += hs + 15
        d.line(((W / 2 - 90), y + 40, (W / 2 + 90), y + 40), fill=GOLD, width=3)
        center(d, k['sub'], y + 90, font('BOD_I.TTF', 58), CREAM)
        center(d, 'LOOKS LIKE LUXE', 1640, font('BOD_B.TTF', 38), GOLD2, track=10)
    elif kind == 'item':
        # number badge top, name + one-liner under the photo
        center(d, k['kicker'], 120, font('BOD_B.TTF', 36), GOLD2, track=10)
        d.ellipse((W / 2 - 62, 190, W / 2 + 62, 314), fill=GOLD)
        nf = font('BOD_B.TTF', 70); t = str(k['n']); d.text((W / 2 - d.textlength(t, font=nf) / 2, 215), t, font=nf, fill=CHOC)
        y = 1330
        y = wrap_center(d, k['name'], y, font('BOD_I.TTF', 76), GOLD, W - 160) + 16
        wrap_center(d, k['line'], y, font('BOD_R.TTF', 52), CREAM, W - 200)
        # progress dots
        for i in range(8):
            cx = W / 2 + (i - 3.5) * 46
            d.ellipse((cx - 11, 1790 - 11, cx + 11, 1790 + 11), fill=GOLD if i < k['n'] else (96, 70, 52))
    else:  # end
        center(d, 'LOOKS LIKE', 560, font('BOD_I.TTF', 130), GOLD)
        center(d, 'LUXE. ISN\'T.', 700, font('BOD_I.TTF', 130), GOLD)
        d.line(((W / 2 - 90), 880, (W / 2 + 90), 880), fill=GOLD, width=3)
        center(d, 'Full list on my', 940, font('BOD_I.TTF', 70), CREAM)
        center(d, 'Amazon storefront', 1030, font('BOD_I.TTF', 70), CREAM)
        bw = 640; d.rounded_rectangle(((W - bw) / 2, 1190, (W + bw) / 2, 1300), radius=55, fill=GOLD)
        center(d, 'LINK IN BIO', 1219, font('BOD_B.TTF', 52), CHOC, track=6)
        wrap_center(d, DISC, 1690, font('BOD_R.TTF', 30), (190, 170, 140), W - 200)
    return im


def render(key):
    global BG
    BG = BG or background()
    v = VIDEOS[key]; os.makedirs('videos', exist_ok=True); out = f'videos/{key}.mp4'
    files = sorted(f for f in os.listdir(v['folder']) if f[:2].isdigit() and f.endswith('.jpg'))[:8]
    segs = [('hook', 2.6, static_frame('hook', kicker=v['kicker'], hook=v['hook'], sub=v['hook_sub']), None)]
    for i, ((name, line), f) in enumerate(zip(v['items'], files), 1):
        segs.append(('item', 2.4, static_frame('item', kicker=v['kicker'], n=i, name=name, line=line), photo_card(f"{v['folder']}/{f}")))
    segs.append(('end', 3.2, static_frame('end'), None))
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    prev = None; fade = 8
    for kind, dur, base, card in segs:
        n = int(dur * FPS)
        for i in range(n):
            fr = base.copy()
            if card is not None:
                s = 1.0 + 0.07 * i / n; cw, ch = int(card.width * s), int(card.height * s)
                c = card.resize((cw, ch), Image.BILINEAR)
                fr.alpha_composite(c, ((W - cw) // 2, 330 + (880 - ch) // 2 + 40))
            elif kind == 'hook':   # soft slow zoom-in feel via brightness ramp
                pass
            rgb = fr.convert('RGB')
            if prev is not None and i < fade:
                rgb = Image.blend(prev, rgb, (i + 1) / fade)
            ff.stdin.write(np.asarray(rgb).tobytes())
            last = rgb
        prev = last
    ff.stdin.close(); ff.wait(); print('wrote', out)


if __name__ == '__main__':
    for k in sys.argv[1:]: render(k)
