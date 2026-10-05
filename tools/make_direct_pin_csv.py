"""Mightypreneur ADVANCED bulk CSV for the collage pins that link straight to the Amazon storefront Idea Lists.
Usage: python tools/make_direct_pin_csv.py pins-direct.csv
Times are Eastern; the importer reads CSV times as Pacific, so subtract 3 hours. Board is chosen on the review screen."""
import csv, sys, datetime as dt
sys.path.insert(0, 'tools')
from make_pin_csv import ROW1, ROW2

SITE = "https://lookslikeluxe.netlify.app"
LINK = "www.amazon.com/shop/influencer-bb664b2f/list/{id}?linkCode=spc&tag=lookslikeluxe-20&domainId=influencer"   # importer adds https://
DISC = " As an Amazon Associate I earn from qualifying purchases."

# key -> (list id, board hint, [(variant, title, description)])
LISTS = {
    'gifts-for-her': ('2XD9NH9XRDOU1', 'Luxe Gifts for Her', [
        ('choc', 'Amazon Gifts for Her That Look Expensive: Storefront Finds',
         'Amazon gifts for her that look way more expensive than they are: a silky sleep set, a Nest candle, a Sol de Janeiro mist set and more. Everything is on my Amazon storefront. Tap the pin for the full list.' + DISC + ' #amazonfinds #giftsforher #giftguide'),
        ('cream', 'Amazon Gift Guide for Her (Rich-Girl Taste, Real-Girl Budget)',
         'My Amazon gift guide for her: luxe-looking picks for birthdays, Christmas and just because. All linked on my Amazon storefront. Tap the pin to shop the list.' + DISC + ' #amazongiftguide #giftideasforher #amazonfinds')]),
    'cozy-fall': ('2E722XRJ37DX0', 'Cozy Fall Home Decor', [
        ('choc', 'Amazon Cozy Fall Home Decor Finds That Look Designer',
         'Amazon fall home decor that looks designer: a chunky knit throw, a cordless lamp, a tall vase, pampas grass and velvet pumpkins. All on my Amazon storefront. Tap the pin for the full list.' + DISC + ' #amazonhome #falldecor #cozyhome'),
        ('cream', 'Amazon Home Finds: Cozy Fall Living Room Decor',
         'Warm neutral Amazon home finds for a cozy fall living room. Everything is linked on my Amazon storefront. Tap the pin to shop the list.' + DISC + ' #amazonhomefinds #falldecor #livingroomdecor')]),
    'clean-girl': ('12LN3GTZLAFHZ', 'Glow-Up Beauty Finds', [
        ('choc', 'Amazon Clean Girl Beauty Finds for Dewy Skin and Glossy Hair',
         'Amazon clean girl beauty finds: Tatcha, Laneige, Olaplex, Sol de Janeiro and more. Glowy, polished and gift-ready, all on my Amazon storefront. Tap the pin for the list.' + DISC + ' #amazonbeauty #cleangirl #skincare'),
        ('cream', 'Clean Girl Aesthetic Amazon Beauty Must Haves',
         'The Amazon beauty must haves for the clean girl aesthetic. Skincare, hair oil, gold hoops and a matcha set, linked on my Amazon storefront. Tap the pin to shop.' + DISC + ' #cleangirlaesthetic #amazonfinds #beautyfinds')]),
    'host-hostess': ('2JZR6TTWD0ATF', 'Holiday Gift Guides', [
        ('choc', 'Amazon Host and Hostess Gifts She Will Actually Remember',
         'Amazon host and hostess gifts that go way beyond wine: a cocktail smoker kit, a champagne saber, a charcuterie set, truffle oil and more. All on my Amazon storefront. Tap the pin for the list.' + DISC + ' #hostessgift #amazonfinds #giftguide'),
        ('cream', 'Hostess Gift Ideas from Amazon (Elegant and Not Boring)',
         'Elegant hostess gift ideas for dinner parties, housewarmings and the holidays, all linked on my Amazon storefront. Tap the pin to shop the list.' + DISC + ' #hostessgifts #amazongiftideas #dinnerparty')]),
}

# (key, variant index) in posting order and Eastern times: 9 AM slot, choc versions first (Oct 6-9), cream versions next (Oct 12-15)
SLOTS = [('gifts-for-her', 0, dt.datetime(2026, 10, 6, 9)), ('host-hostess', 0, dt.datetime(2026, 10, 7, 9)),
         ('clean-girl', 0, dt.datetime(2026, 10, 8, 9)), ('cozy-fall', 0, dt.datetime(2026, 10, 9, 9)),
         ('gifts-for-her', 1, dt.datetime(2026, 10, 12, 9)), ('host-hostess', 1, dt.datetime(2026, 10, 13, 9)),
         ('clean-girl', 1, dt.datetime(2026, 10, 14, 9)), ('cozy-fall', 1, dt.datetime(2026, 10, 15, 9))]


def main(path):
    rows = [ROW1, ROW2]
    for key, v, et in SLOTS:
        lid, board, variants = LISTS[key]
        variant, title, desc = variants[v]
        pt = et - dt.timedelta(hours=3)
        row = [""] * 40
        row[0] = pt.strftime("%Y-%m-%d %H:%M:%S"); row[1] = desc
        row[3] = f"{SITE}/pins/collage-{key}-{variant}.png"
        row[7] = "false"; row[8] = "false"; row[38] = title; row[39] = LINK.format(id=lid)
        rows.append(row)
        print(et.strftime("%a %b %d %I:%M %p ET"), "|", key, variant, "| board:", board, "| len(desc)", len(desc))
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pins-direct.csv")
