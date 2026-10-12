"""Single-product Pinterest pins that link DIRECTLY to one Amazon product (tagged affiliate link).
Usage (from project root):  py tools/make_product_pins.py
Writes pins/product-<key>.png (1000x1500) and pins-products.csv (Mightypreneur ADVANCED bulk CSV).
Times are Eastern; the importer reads CSV times as Pacific so we subtract 3h. Board is chosen on the review screen.
Rules: no prices on pins, no 'I use' claims, disclosure in every description, keyword-first titles."""
import sys, csv, datetime as dt
sys.path.insert(0, 'tools')
from PIL import Image, ImageDraw
from make_pin_csv import ROW1, ROW2
import make_pins as mp

IMG = "https://raw.githubusercontent.com/jessicajsantiago/lookslikeluxe/main/pins"
TAG = "lookslikeluxe-20"
D = " As an Amazon Associate I earn from qualifying purchases."

# key, asin, image, kicker, headline lines, pin title (<=100), description, board hint
P = [
 ('stanley', 'B0CRMP3RQT', 'images/blog/gifts-100/03-stanley-quencher.jpg', 'AMAZON GIFT FIND', ['The Tumbler', 'With a Fan Club'],
  'Stanley Quencher 40 oz Tumbler: The Gift Everyone Wants', 'The Stanley Quencher 40 oz tumbler has over 200,000 reviews on Amazon and comes in giftable colors. A cozy, useful gift idea for her. Tap the pin to shop.', 'Luxe Gifts for Her'),
 ('tatcha', 'B09QBB8ZL4', 'images/blog/gifts-100/04-tatcha-dewy-skin-cream.jpg', 'AMAZON BEAUTY FIND', ['A Luxe-Looking', 'Moisturizer'],
  'TATCHA Dewy Skin Cream: A Gift That Looks Expensive', 'A luxe-looking moisturizer in a jar that belongs on a vanity. A beauty gift idea for her, rated 4.6 stars on Amazon. Tap the pin to shop.', 'Luxury Beauty Gift Sets'),
 ('sol-de-janeiro', 'B09X3HB2BR', 'images/blog/gifts-100/01-sol-de-janeiro-mist.jpg', 'AMAZON BEAUTY FIND', ['The Perfume Mist', 'Everyone Asks About'],
  'Sol de Janeiro Cheirosa 62 Perfume Mist: Sweet Fragrance Gift Idea', 'The Sol de Janeiro Cheirosa 62 hair and body mist, a sweet, warm fragrance with more than 50,000 reviews on Amazon. Great for perfume layering and gifting. Tap to shop.', 'Perfume & Fragrance Finds'),
 ('instax', 'B0BWNYPCT1', 'images/blog/gifts-100/02-instax-mini-12.jpg', 'AMAZON GIFT FIND', ['The Camera That', 'Prints Tiny Photos'],
  'Fujifilm Instax Mini 12 Instant Camera: Fun Gift Idea for Her', 'The Instax Mini 12 instant camera prints a tiny photo in seconds. A playful gift idea for friends, sisters and girls trips. Tap the pin to shop.', 'Luxe Gifts for Her'),
 ('nest', 'B00394USWE', 'images/blog/gifts-100/05-nest-candle.jpg', 'AMAZON HOME FIND', ['A Candle That', 'Looks Boutique'],
  'NEST New York Bamboo Scented Candle: Luxe Host and Hostess Gift', 'A designer-looking scented candle in a glass jar, a lovely host gift or girlfriend gift. Rated 4.6 stars on Amazon. Tap the pin to shop.', 'Holiday Gift Guides'),
 ('revlon', 'B01LSUQSB0', 'images/blog/gifts-100/08-revlon-one-step.jpg', 'AMAZON HAIR FIND', ['The Dryer Brush', 'With 350,000 Reviews'],
  'Revlon One-Step Hair Dryer and Volumizer: Blowout Tool Gift Idea', 'The Revlon One-Step dryer brush dries and styles in one pass and has more than 350,000 reviews on Amazon. A hair tool gift idea she will use. Tap to shop.', 'Hair Care Finds'),
 ('laneige', 'B0DVH22M8S', 'images/blog/holiday-her/01-laneige-lip-glowy-balm.jpg', 'AMAZON STOCKING STUFFER', ['A Stocking Stuffer', "She'll Actually Use"],
  'LANEIGE Lip Glowy Balm: Stocking Stuffer Idea for Her', 'A sheer-tinted lip balm from Laneige, a pretty and affordable stocking stuffer idea with more than 34,000 reviews on Amazon. Tap the pin to shop.', 'Holiday Gift Guides'),
 ('kindle', 'B0CFPJYX7P', 'images/blog/holiday-her/08-kindle-paperwhite.jpg', 'AMAZON GIFT FIND', ['The Gift for', 'the Bookworm'],
  'Kindle Paperwhite: Holiday Gift Idea for Book Lovers', 'The Kindle Paperwhite has a glare-free 7-inch display and weeks of battery life. A holiday gift idea for readers and travelers. Tap the pin to shop.', 'Holiday Gift Guides'),
 ('ugg', 'B0DPJJNHDW', 'images/blog/holiday-her/06-ugg-tasman-ii.jpg', 'AMAZON GIFT FIND', ['The Cozy', 'Splurge'],
  'UGG Tasman II Slippers: Cozy Christmas Gift Idea for Her', 'The UGG Tasman slipper, a cozy splurge gift idea with a 4.7-star rating on Amazon. Check sizing before you buy. Tap the pin to shop.', 'Luxe Gifts for Her'),
 ('khamrah', 'B0B92Y18GT', 'images/blog/perfume-layering/02-lattafa-khamrah.jpg', 'AMAZON PERFUME FIND', ['The Warm Vanilla', 'Perfume Going Viral'],
  'Lattafa Khamrah Eau de Parfum: Warm Vanilla Perfume for Fall', 'Lattafa Khamrah is a warm vanilla, spice and amber perfume with more than 39,000 reviews on Amazon. A fall fragrance to layer or wear alone. Tap to shop.', 'Perfume & Fragrance Finds'),
 ('rare-beauty', 'B08L79L91T', 'images/blog/fall-makeup/01-rare-beauty-blush.jpg', 'AMAZON MAKEUP FIND', ['The Liquid Blush', 'for Fall'],
  'Rare Beauty Soft Pinch Liquid Blush: Fall Makeup Must Have', 'Rare Beauty Soft Pinch Liquid Blush, a blendable cream blush for the soft, flushed fall makeup trend. Choose your shade on the page. Tap to shop.', 'Makeup Must-Haves'),
 ('orolay', 'B00HHOXY14', 'images/blog/fall-wardrobe/01-orolay-puffer.jpg', 'AMAZON STYLE FIND', ['The Winter Coat', 'That Got Famous'],
  'Orolay Thickened Down Jacket: Winter Coat Women Love', 'The Orolay thickened down jacket has nearly 30,000 reviews on Amazon and a 4.5-star rating. A warm winter coat idea. Check sizing before you buy.', 'Fall & Winter Outfit Finds'),
]

W, H = mp.W, mp.H
GOLD, CHOC, CREAM, BLUSH, RUST = mp.GOLD, mp.CHOC, mp.CREAM, mp.BLUSH, mp.RUST


def build(i, key, asin, img, kicker, lines, title, desc, board):
    dark = (i % 2 == 0)
    if dark:
        bg = mp.patbg(); d = ImageDraw.Draw(bg, 'RGBA'); d.rectangle((0, 0, W, H), fill=(43, 26, 18, 120)); ink, ink2 = GOLD, (236, 214, 170)
    else:
        bg = Image.new('RGB', (W, H), BLUSH); d = ImageDraw.Draw(bg); d.rectangle((24, 24, W - 24, H - 24), outline=GOLD, width=3); ink, ink2 = CHOC, RUST
    mp.center(d, kicker, 70, mp.font('BOD_R.TTF', 34), ink2)
    for k, l in enumerate(lines): mp.center(d, l, 130 + k * 118, mp.fit(d, l, 'BOD_I.TTF', 112, 880), ink)
    c, m = mp.card(img, (840, 840), pad=14); x = (W - 840) // 2; y = 430
    bg.paste(c, (x, y), m); d.rounded_rectangle((x, y, x + 840, y + 840), radius=26, outline=GOLD, width=4)
    mp.cta(d, 1330, GOLD if dark else CHOC, CHOC if dark else GOLD, 'TAP TO SHOP')
    out = f'pins/product-{key}.png'; bg.save(out); return out


def main():
    rows = [ROW1, ROW2]; start = dt.date(2026, 10, 14)
    for i, (key, asin, img, kicker, lines, title, desc, board) in enumerate(P):
        build(i, key, asin, img, kicker, lines, title, desc, board)
        day = start + dt.timedelta(days=i); et = dt.datetime(day.year, day.month, day.day, 15, 30); pt = et - dt.timedelta(hours=3)
        assert len(title) <= 100 and len(desc) + len(D) + 40 <= 500, (key, len(title), len(desc))
        r = [""] * 40
        r[0] = pt.strftime("%Y-%m-%d %H:%M:%S"); r[1] = desc + D + ' #amazonfinds #giftideas'; r[3] = f"{IMG}/product-{key}.png"
        r[7] = "false"; r[8] = "false"; r[38] = title; r[39] = f"www.amazon.com/dp/{asin}?tag={TAG}"
        rows.append(r); print(et.strftime('%a %b %d %I:%M %p ET'), key, '| board:', board)
    with open('pins-products.csv', 'w', newline='', encoding='utf-8') as f: csv.writer(f).writerows(rows)


if __name__ == '__main__':
    main()
