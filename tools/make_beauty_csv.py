"""Mightypreneur ADVANCED bulk CSVs for the Oct 10 round (perfume, makeup, hair, wardrobe).
Usage: python tools/make_beauty_csv.py   -> pins-beauty-lll.csv (Looks Like Luxe), pins-beauty-personal.csv (@PrettyGirlsLoveJess)
LLL gets blog pin v1 + choc collage (direct to Amazon list) + blog pin v2 per topic; the personal account gets DIFFERENT art
(blog pin v3 + cream collage) with different titles, a few days later (Pinterest dislikes identical duplicate pins).
Times are Eastern; the importer reads CSV times as Pacific so subtract 3h. Board is chosen on the review screen."""
import csv, sys, datetime as dt
sys.path.insert(0, 'tools')
from make_pin_csv import ROW1, ROW2

IMG = "https://raw.githubusercontent.com/jessicajsantiago/lookslikeluxe/main/pins"
BLOG = "lookslikeluxe.netlify.app/blog"
AMZ = "www.amazon.com/shop/influencer-bb664b2f/list/{id}?linkCode=spc&tag=lookslikeluxe-20&domainId=influencer"
D = " As an Amazon Associate I earn from qualifying purchases."

T = {
 'perfume': dict(id='1L4ZS0OCH8V2Z', slug='perfume-layering-combos', col='perfume-layering'),
 'makeup':  dict(id='BKAGDPVS1KN8', slug='dark-romantic-fall-makeup', col='fall-makeup'),
 'hair':    dict(id='18KAB1CTOA2DH', slug='hair-scalp-care', col='hair-scalp'),
 'wardrobe': dict(id='2R7FT7BWKFT95', slug='fall-winter-wardrobe-staples', col='fall-wardrobe'),
}

# (topic, kind, image, title, description). kind: 'blog' -> link to post, 'amz' -> link to the Idea List
LLL = [
 ('perfume', 'blog', 'perfume-layering-combos-v1-grid.png', 'Perfume Layering Combos: 8 Scents That Smell Expensive Together',
  'Perfume layering is the fall 2026 beauty trend. Warm vanilla, sweet gourmand and floral scents plus a body cream to stack them on. Eight Amazon finds with great reviews. Tap for the full guide.' + D + ' #perfumelayering #fragrance #amazonbeauty'),
 ('perfume', 'amz', 'collage-perfume-layering-choc.png', 'Amazon Perfume Layering Combos That Smell Expensive',
  'Amazon perfume layering combos for fall: Ariana Grande Cloud, Lattafa Khamrah, Sol de Janeiro Cheirosa 62 and more. All on my Amazon storefront. Tap the pin for the full list.' + D + ' #perfumelayering #amazonfinds #fragrancetok'),
 ('perfume', 'blog', 'perfume-layering-combos-v2-hero.png', 'Best Perfume Layering Combos for Fall 2026 (Vanilla, Warm and Sweet)',
  'The best perfume layering combos for fall 2026: start with a body cream, add a vanilla base and finish with one bold note. Eight Amazon picks rated 4.4 stars or higher.' + D + ' #fallperfume #vanillaperfume #scentlayering'),
 ('makeup', 'blog', 'dark-romantic-fall-makeup-v1-grid.png', 'Dark Romantic Fall Makeup: Cream Blush, Berry Lips and More',
  'Dark romantic makeup is the look of fall 2026: soft cream blush, berry lips, black nails and a setting spray to lock it in. Eight Amazon finds with great reviews. Tap for the guide.' + D + ' #darkromantic #fallmakeup #amazonbeauty'),
 ('makeup', 'amz', 'collage-fall-makeup-choc.png', 'Amazon Dark Romantic Makeup Finds for Fall 2026',
  'Amazon dark romantic makeup finds: Rare Beauty liquid blush, Fenty Gloss Bomb Heat, Maybelline Matte Ink, black nail polish and more. All on my Amazon storefront. Tap the pin for the list.' + D + ' #fallmakeup #amazonfinds #makeupmusthaves'),
 ('makeup', 'blog', 'dark-romantic-fall-makeup-v2-hero.png', 'Fall Makeup Trends 2026: The Dark Romantic Look on a Budget',
  'Fall makeup trends 2026 are moody and pretty: cream blush, deep berry lips and a little smudge. Recreate the dark romantic look with eight Amazon finds. See all 8.' + D + ' #makeuptrends #berrylips #creamblush'),
 ('hair', 'blog', 'hair-scalp-care-v1-grid.png', 'Best Hair Care Products on Amazon: Scalp Care, Shine and Repair',
  'Scalp care is the new skincare. A simple hair routine from Amazon: scalp massager, rosemary oil, bond repair, shine oil and a blowout tool. Eight picks rated 4.5 stars or higher. Tap for the guide.' + D + ' #haircare #scalpcare #amazonfinds'),
 ('hair', 'amz', 'collage-hair-scalp-choc.png', 'Amazon Hair Care Finds: Scalp, Shine and Repair',
  'Amazon hair care finds: Olaplex, Moroccanoil, a Revlon dryer brush, a scalp massager and more. All on my Amazon storefront. Tap the pin for the full list.' + D + ' #haircareroutine #amazonhaircare #scalpmassage'),
 ('hair', 'blog', 'hair-scalp-care-v2-hero.png', 'Scalp Care Is the New Skincare: 8 Hair Finds on Amazon',
  'Scalp care is trending. These eight Amazon hair finds cover the scalp, repair and shine, from a silicone massager to a salon-style oil. See the full list.' + D + ' #scalpmassage #hairoil #haircare'),
 ('wardrobe', 'blog', 'fall-winter-wardrobe-staples-v1-grid.png', 'Fall and Winter Wardrobe Staples From Amazon (Look Expensive for Less)',
  'Dark romance is the mood of fall and winter 2026. Eight Amazon wardrobe staples: a puffer, a faux leather jacket, boots, a turtleneck, a gold belt and more. Tap for the guide.' + D + ' #fallfashion #wardrobestaples #amazonfashion'),
 ('wardrobe', 'amz', 'collage-fall-wardrobe-choc.png', 'Amazon Fall Wardrobe Staples: Coats, Boots and Belts',
  'Amazon fall wardrobe staples for a capsule that looks expensive: outerwear, boots, a turtleneck and accessories. All on my Amazon storefront. Tap the pin for the list.' + D + ' #amazonfashion #fallcapsule #fallwardrobe'),
 ('wardrobe', 'blog', 'fall-winter-wardrobe-staples-v2-hero.png', 'Fall Outfit Essentials 2026: 8 Amazon Wardrobe Staples',
  'Fall outfit essentials for 2026, all from Amazon: coats, boots, a classic turtleneck and the accessories that finish a look. See all 8 picks.' + D + ' #falloutfits #winterwardrobe #amazonfinds'),
]
PERSONAL = [
 ('perfume', 'blog', 'perfume-layering-combos-v3-list.png', 'Perfume Layering Ideas: Vanilla, Gourmand and Floral Combos',
  'Perfume layering ideas for fall: build a signature scent from a body cream, a sweet vanilla base and a floral top note. Eight Amazon finds with great reviews. Tap to browse.' + D + ' #perfumeideas #layeringperfume #beautyfinds'),
 ('perfume', 'amz', 'collage-perfume-layering-cream.png', 'Amazon Perfume Finds for Layering (Sweet, Warm and Floral)',
  'Sweet, warm and floral perfumes from Amazon that are made for layering. Tap the pin to shop the list on my Amazon storefront.' + D + ' #amazonperfume #fragrance #giftideasforher'),
 ('makeup', 'blog', 'dark-romantic-fall-makeup-v3-list.png', 'Dark Romantic Makeup Ideas for Fall: Berry Lips and Soft Blush',
  'Dark romantic makeup ideas for fall: soft blush, berry lips, black nails and a long-wear setting spray. Eight beauty finds from Amazon. Tap to browse.' + D + ' #makeupideas #fallbeauty #berrylips'),
 ('makeup', 'amz', 'collage-fall-makeup-cream.png', 'Fall Makeup Must Haves From Amazon',
  'Fall makeup must haves from Amazon, from cream blush to long-wear lips. Tap the pin to shop the list on my Amazon storefront.' + D + ' #makeupmusthaves #amazonmakeup #fallmakeuplook'),
 ('hair', 'blog', 'hair-scalp-care-v3-list.png', 'Hair Care Routine Ideas: Scalp, Repair and Shine From Amazon',
  'Hair care routine ideas from Amazon: a scalp massager, rosemary oil, bond repair, shine oil and a blowout tool. Eight picks with great reviews. Tap to browse.' + D + ' #hairroutine #hairproducts #amazonbeauty'),
 ('hair', 'amz', 'collage-hair-scalp-cream.png', 'Amazon Hair Care Must Haves for Healthy-Looking Hair',
  'Amazon hair care must haves for shine, softness and a happy scalp. Tap the pin to shop the list on my Amazon storefront.' + D + ' #hairproducts #amazonfinds #hairtok'),
 ('wardrobe', 'blog', 'fall-winter-wardrobe-staples-v3-list.png', 'Fall Capsule Wardrobe Ideas From Amazon',
  'Fall capsule wardrobe ideas from Amazon: a puffer, a faux leather jacket, boots, a turtleneck and a gold belt. Eight pieces that look more expensive than they are. Tap to browse.' + D + ' #capsulewardrobe #fallfashion #amazonfashion'),
 ('wardrobe', 'amz', 'collage-fall-wardrobe-cream.png', 'Amazon Winter Outfit Essentials (Coats, Boots, Accessories)',
  'Winter outfit essentials from Amazon: warm outerwear, boots and accessories that finish a look. Tap the pin to shop the list on my Amazon storefront.' + D + ' #winteroutfits #amazonstyle #wardrobeessentials'),
]

def write(path, pins, start, slots):
    rows = [ROW1, ROW2]; i = 0
    for topic, kind, img, title, desc in pins:
        day = start + dt.timedelta(days=i // len(slots)); h, m = slots[i % len(slots)]
        et = dt.datetime(day.year, day.month, day.day, h, m); pt = et - dt.timedelta(hours=3); i += 1
        t = T[topic]; link = AMZ.format(id=t['id']) if kind == 'amz' else f"{BLOG}/{t['slug']}.html"
        assert len(title) <= 100 and len(desc) <= 500, (title, len(title), len(desc))
        r = [""] * 40
        r[0] = pt.strftime("%Y-%m-%d %H:%M:%S"); r[1] = desc; r[3] = f"{IMG}/{img}"; r[7] = "false"; r[8] = "false"; r[38] = title; r[39] = link
        rows.append(r); print(path, et.strftime("%a %b %d %I:%M %p ET"), topic, kind, img)
    with open(path, "w", newline="", encoding="utf-8") as f: csv.writer(f).writerows(rows)

if __name__ == '__main__':
    write('pins-beauty-lll.csv', LLL, dt.date(2026, 10, 11), [(11, 30), (21, 0)])
    write('pins-beauty-personal.csv', PERSONAL, dt.date(2026, 10, 13), [(12, 30)])


# ---- Round 3: gifts under $100 + holiday gift guide ----
T['gifts100'] = dict(id='693H5MH6IX80', slug='gifts-under-100-for-her', col='gifts-100')
T['holiday'] = dict(id='12ZPTJW3RR36H', slug='holiday-gift-guide-for-her', col='holiday-her')
LLL3 = [
 ('gifts100', 'blog', 'gifts-under-100-for-her-v1-grid.png', 'Amazon Gifts Under $100 for Her That Look Expensive',
  'Eight Amazon gifts under $100 that look like a splurge: Sol de Janeiro, Tatcha, an Instax camera, a Stanley tumbler, a NEST candle and more. Prices change, so check before you buy. Tap for the full guide.' + D + ' #giftsforher #giftsunder100 #amazongifts'),
 ('gifts100', 'amz', 'collage-gifts-100-choc.png', 'Amazon Gifts Under $100 That Look Way More Expensive',
  'Luxe-looking Amazon gift ideas for her, all under $100 when I checked. All on my Amazon storefront. Tap the pin for the full list.' + D + ' #giftguide #amazonfinds #christmasgiftideas'),
 ('gifts100', 'blog', 'gifts-under-100-for-her-v2-hero.png', 'Best Gifts Under $100 for Her: 8 Luxe-Looking Ideas',
  'The best gifts under $100 for her this holiday season, from skincare and perfume to a mini lamp and a cozy throw. Eight well-reviewed Amazon picks. See the guide.' + D + ' #bestgifts #giftideasforher #holidaygifts'),
 ('holiday', 'blog', 'holiday-gift-guide-for-her-v1-grid.png', 'Holiday Gift Guide for Her 2026: Stocking Stuffers to Splurges',
  'The holiday gift guide for her: stocking stuffers, cozy treats and a few splurges, from Laneige and satin pillowcases to UGG slippers and a Kindle. Eight Amazon picks rated 4.4 stars or higher.' + D + ' #holidaygiftguide #giftsforher #stockingstuffers'),
 ('holiday', 'amz', 'collage-holiday-her-choc.png', 'Amazon Holiday Gift Guide for Her: 8 Gift Ideas',
  'Amazon holiday gift ideas for her in three tiers: stocking stuffers, treats and splurges. All on my Amazon storefront. Tap the pin for the full list.' + D + ' #christmasgifts #amazonfinds #giftguide'),
 ('holiday', 'blog', 'holiday-gift-guide-for-her-v2-hero.png', 'Christmas Gift Ideas for Her 2026: Cozy, Beauty and Splurge Picks',
  'Christmas gift ideas for her that feel thoughtful: a satin robe, UGG slippers, a Kindle, a massage gun and more. Eight Amazon picks with real reviews. See all 8.' + D + ' #christmasgiftideas #giftsforwomen #holidaygifts'),
]
PERSONAL3 = [
 ('gifts100', 'blog', 'gifts-under-100-for-her-v3-list.png', 'Gift Ideas for Her Under $100 (Luxe-Looking Picks From Amazon)',
  'Gift ideas for her under $100: skincare, perfume, a camera, a tumbler and cozy home finds. Eight Amazon picks with great reviews. Tap to browse.' + D + ' #giftideasforher #affordablegifts #holidaygifts'),
 ('gifts100', 'amz', 'collage-gifts-100-cream.png', 'Amazon Gift Ideas for Her That Look Expensive',
  'Amazon gift ideas for her that look way more expensive than they are. Tap the pin to shop the list on my Amazon storefront.' + D + ' #amazongiftideas #giftsforher #luxegifts'),
 ('holiday', 'blog', 'holiday-gift-guide-for-her-v3-list.png', 'Holiday Gift Ideas for Her: Stocking Stuffers to Splurges',
  'Holiday gift ideas for her in three budgets: stocking stuffers, treats and splurges. Eight Amazon picks with real reviews. Tap to browse.' + D + ' #holidaygiftideas #stockingstuffers #giftsforwomen'),
 ('holiday', 'amz', 'collage-holiday-her-cream.png', 'Amazon Christmas Gifts for Her 2026',
  'Amazon Christmas gifts for her, from lip balm to a Kindle. Tap the pin to shop the list on my Amazon storefront.' + D + ' #christmasgiftsforher #amazonfinds #giftguide'),
]

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'round3':
    write('pins-gifts-lll.csv', LLL3, dt.date(2026, 10, 17), [(11, 30), (21, 0)])
    write('pins-gifts-personal.csv', PERSONAL3, dt.date(2026, 10, 21), [(12, 30)])


# ---- Round 4: teen gifts, best friend gifts, luxe finds for less ----
T['teen'] = dict(id=None, slug='gifts-for-teen-girls', col='gifts-teen')
T['bff'] = dict(id=None, slug='gifts-for-best-friend', col='gifts-bff')
T['dupes'] = dict(id=None, slug='luxe-looking-amazon-finds-for-less', col='dupes')
LLL4 = [
 ('teen', 'blog', 'gifts-for-teen-girls-v1-grid.png', 'Gifts for Teen Girls 2026: 8 Amazon Ideas She Will Actually Use',
  'Gifts for teen girls that are not cringe: LED lights, a Laneige lip mask, a heart waffle maker, an instant camera, Crocs and more. Eight Amazon picks with great reviews. Tap for the guide.' + D + ' #giftsforteengirls #teengifts #christmasgiftideas'),
 ('bff', 'blog', 'gifts-for-best-friend-v1-grid.png', 'Gifts for Your Best Friend: 8 Amazon Ideas She Will Love',
  'Gifts for your best friend: a jewelry tray, pearl hair clips, a NEST candle, a mini lamp, a Sol de Janeiro mist and more. Eight Amazon picks with real reviews. Tap for the full guide.' + D + ' #giftsforbestfriend #bestfriendgifts #giftideas'),
 ('dupes', 'blog', 'luxe-looking-amazon-finds-for-less-v1-grid.png', 'Luxe-Looking Beauty Finds for Less: 8 Budget Picks on Amazon',
  'Rich-girl taste, real-girl budget. Eight affordable beauty and hair finds with a designer vibe: a glow filter, a viral mascara, a warm vanilla perfume and more. Tap for the guide.' + D + ' #beautyfinds #budgetbeauty #amazonbeauty'),
 ('teen', 'blog', 'gifts-for-teen-girls-v2-hero.png', 'Best Gifts for Teenage Girls: Cozy, Cute and Not Cringe',
  'The best gifts for teenage girls this Christmas, from room upgrades to small beauty treats. Eight Amazon picks rated 4.4 stars or higher. See all 8.' + D + ' #giftsforteens #teengiftideas #holidaygifts'),
 ('bff', 'blog', 'gifts-for-best-friend-v2-hero.png', 'Best Friend Gift Ideas: Pretty, Cozy and a Little Dramatic',
  'Best friend gift ideas that feel personal without being weird. Eight Amazon picks, from jewelry trays to cozy lamps. See the full guide.' + D + ' #bestfriendgiftideas #giftsforher #christmasgifts'),
 ('dupes', 'blog', 'luxe-looking-amazon-finds-for-less-v2-hero.png', 'Budget Beauty Finds That Look Expensive (Amazon Edition)',
  'Budget beauty and hair finds that give a luxe feel for less. Eight well-reviewed Amazon picks. See the guide.' + D + ' #dupes #drugstoremakeup #beautyhacks'),
]
PERSONAL4 = [
 ('teen', 'blog', 'gifts-for-teen-girls-v3-list.png', 'Gift Ideas for Teen Girls (Cozy, Cute, Not Cringe)',
  'Gift ideas for teen girls: LED lights, Laneige, Crocs, an instant camera and more. Eight Amazon picks with great reviews. Tap to browse.' + D + ' #teengiftideas #giftsforgirls #christmasgifts'),
 ('bff', 'blog', 'gifts-for-best-friend-v3-list.png', 'Gift Ideas for Your Bestie: Eight Amazon Picks',
  'Gift ideas for your bestie, from a jewelry tray to a cozy mini lamp. Eight Amazon picks with real reviews. Tap to browse.' + D + ' #bestiegifts #giftideasforher #holidaygifts'),
 ('dupes', 'blog', 'luxe-looking-amazon-finds-for-less-v3-list.png', 'Luxe-Looking Beauty Finds on a Budget',
  'Luxe-looking beauty and hair finds on a budget, all with great Amazon reviews. Tap to browse the list.' + D + ' #budgetbeauty #beautyfinds #amazonfinds'),
]

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'round4':
    write('pins-round4-lll.csv', LLL4, dt.date(2026, 10, 20), [(11, 30), (21, 0)])
    write('pins-round4-personal.csv', PERSONAL4, dt.date(2026, 10, 25), [(12, 30)])
