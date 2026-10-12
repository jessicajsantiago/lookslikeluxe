import json
DISC = "As an Amazon Associate I earn from qualifying purchases, which means if you tap a link and buy, I may earn a small commission at no extra cost to you. Prices and availability live on Amazon and change often."


def P(asin, name, img, best, c1, c2, c3):
    return {"asin": asin, "name": name, "image": img, "best_for": best, "copy": [c1, c2, c3]}


def post(slug, title, headline, seo, desc, kicker, intro, products, inter, outro, pin, related):
    d = {"slug": slug, "title": title, "headline": headline, "seo_title": seo, "description": desc, "kicker": kicker,
         "date": "October 12, 2026", "read_time": "5 min read", "pin_image": f"pins/{slug}-v1-grid.png", "intro": intro,
         "disclosure": DISC, "products": products, "interludes": inter, "outro": outro, "pin": pin, "related": related}
    json.dump(d, open(f'posts/{slug}.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


rel = [{"title": "Holiday Gift Guide for Her", "url": "/blog/holiday-gift-guide-for-her.html"},
       {"title": "Gifts Under $100 That Look Expensive", "url": "/blog/gifts-under-100-for-her.html"},
       {"title": "The Luxe Gift Vault (free)", "url": "/index.html#signup"}]

g = 'images/blog/gifts-teen/'
post("gifts-for-teen-girls", "Gifts for Teen Girls",
     "Gifts for Teen Girls 2026: 8 Amazon Ideas She'll Actually Use (Not Cringe)",
     "Gifts for Teen Girls 2026: 8 Amazon Gift Ideas | Looks Like Luxe",
     "Gifts for teen girls on Amazon: LED lights, a Laneige lip mask, a heart waffle maker, an instant camera, Crocs and more. Eight best-reviewed gift ideas for Christmas.",
     "The Gift Edit",
     ["Buying for a teenager is the hardest gifting assignment there is. She has opinions, a group chat, and zero patience for anything that feels like a gift from an aunt.",
      "So I went looking for the stuff teens actually ask for: cozy-room upgrades, small beauty treats, and a couple of things that make good photos. Every pick has a 4.4-star rating or higher on Amazon, with thousands of reviews behind it.",
      "I haven't tested them. I'm telling you what's popular, well reviewed and very giftable. Prices move a lot before Christmas, so check before you buy.",
      "Let's make you the cool one."],
     [P("B0DFYBYPZM", "LED Strip Lights for Bedroom, 200 ft with Remote", g + "01-led-strip-lights.jpg", "The room makeover that costs less than a pizza night",
        "LED strip lights are the fastest way to give a bedroom a mood. This set comes with a remote and an app.", "It has a 4.5-star rating from nearly 2,000 reviewers.", "Verdict: the glow-up for her room."),
      P("B07XXPHQZK", "LANEIGE Lip Sleeping Mask", g + "02-laneige-lip-sleeping-mask.jpg", "The beauty treat every teen has on her wishlist",
        "A bedtime lip mask from a K-beauty brand people rave about, in a pretty jar.", "It rates 4.6 stars from more than 37,000 reviewers.", "Verdict: a small gift that gets a big reaction."),
      P("B01E8IZ4ZA", "ESARORA Ice Roller for Face and Eye", g + "03-ice-roller.jpg", "Skincare routines that feel like self-care",
        "A cooling face roller that has become a staple in beauty routines.", "It has a 4.6-star rating from more than 22,000 reviewers.", "Verdict: low-cost, high-fun."),
      P("B08BCSNCMW", "Dash Heart Mini Waffle Maker", g + "04-dash-heart-waffle.jpg", "Sleepovers and breakfast-for-dinner energy",
        "A tiny, heart-shaped waffle maker that makes a snack feel like an event.", "It rates 4.7 stars from more than 35,000 reviewers.", "Verdict: the cutest kitchen gift for a teen."),
      P("B0014C0LSY", "Crocs Classic Clog", g + "05-crocs-classic-clog.jpg", "The comfy shoe that never went out of style",
        "The classic clog in a huge range of colors, plus charms to personalize them. Check sizing before you buy.", "It has a 4.8-star rating from nearly 490,000 reviewers.", "Verdict: a safe bet in the right color."),
      P("B01MFGN8S5", "Bath Bombs Gift Set, 12 Pack", g + "06-bath-bomb-set.jpg", "Self-care night, already gift-wrapped",
        "A set of twelve fizzing bath bombs with shea and cocoa butter.", "It rates 4.8 stars from more than 46,000 reviewers.", "Verdict: the easy stocking stuffer."),
      P("B0BWNYPCT1", "Fujifilm Instax Mini 12 Instant Camera", g + "07-instax-mini-12.jpg", "The friend who documents everything",
        "A camera that prints a tiny photo in seconds. Film is sold separately, so tuck in a pack.", "It has a 4.6-star rating from more than 1,500 reviewers.", "Verdict: the most fun gift on the list."),
      P("B0CRMP3RQT", "STANLEY Quencher H2.0 FlowState Tumbler, 40 oz", g + "08-stanley-quencher.jpg", "The tumbler with its own fan club",
        "The 40 oz tumbler everyone has seen online, in giftable colors.", "It rates 4.7 stars from more than 200,000 reviewers.", "Verdict: the crowd-pleaser.")],
     {"3": "Rule one of teen gifting: skip the cringe, pick the cozy.", "6": "Rule two: add a handwritten note. Teens notice."},
     ["And that's the list: eight Amazon gifts for teen girls that won't end up in the back of a closet.",
      "If you take one thing from this guide, let it be this. Pick one 'room' gift and one 'treat' gift, and you're covered.",
      "Until the next gift emergency, darling."],
     {"kicker": "THE GIFT EDIT", "h1": ["Gifts for", "Teen Girls"], "sub": "(not cringe, we promise)", "tile": ["no", "cringe"], "cta1": "READ THE GUIDE",
      "hero_kicker": "CHRISTMAS 2026", "hero_lines": ["8 Gifts Teen Girls", "Actually Want", "(Not Cringe)"], "hero_tag": "cozy. cute. zero eye-rolls.",
      "cta2": "GET THE LIST", "cta3": "SHOP ALL 8", "hero_index": 6, "small_idx": [0, 1, 3, 4]}, rel)

g = 'images/blog/gifts-bff/'
post("gifts-for-best-friend", "Gifts for Best Friend",
     "Gifts for Your Best Friend: 8 Amazon Ideas That Say 'I Get You'",
     "Gifts for Best Friend 2026: 8 Amazon Gift Ideas She'll Love | Looks Like Luxe",
     "Gifts for your best friend on Amazon: a jewelry tray, pearl hair clips, a NEST candle, a mini lamp, a Sol de Janeiro mist and more. Eight best-reviewed ideas.",
     "The Gift Edit",
     ["Your best friend knows your coffee order, your worst date story and the exact moment you need a snack. The gift needs to match that level of intimacy.",
      "I went through Amazon for the gifts that feel personal without being weird: pretty things for her vanity, cozy things for her nightstand, and a couple of small luxuries.",
      "Everything here is rated 4.4 stars or higher with real review counts, and none of it is claimed as tested by me. Check prices before you buy, since they change around the holidays.",
      "Let's go make her squeal."],
     [P("B0FNW2TTZ9", "ProCase Stackable Jewelry Organizer Trays", g + "01-procase-jewelry-trays.jpg", "The friend with too many earrings",
        "Stackable trays that fit in a drawer and keep jewelry in order.", "It has a 4.5-star rating from nearly 2,500 reviewers.", "Verdict: pretty storage for pretty things."),
      P("B082Z7S4VJ", "Mehayi 20-Piece Pearl Hair Clips", g + "02-pearl-hair-clips.jpg", "The easiest way to dress up a messy bun",
        "A set of pearl hair clips in mixed sizes, a trend that never fully leaves.", "It rates 4.4 stars from more than 7,400 reviewers.", "Verdict: tiny, cute and very giftable."),
      P("B0BHQYS16C", "ADRIONE Satin Scrunchies, 60-Pack", g + "03-satin-scrunchies.jpg", "A stocking stuffer you can split with her",
        "A big pack of soft satin scrunchies in lots of colors.", "It has a 4.5-star rating from nearly 4,000 reviewers.", "Verdict: share the pack, or keep some."),
      P("B0009F3R7E", "Burt's Bees Hand Repair Gift Set", g + "04-burts-bees-hand-set.jpg", "Winter hands, solved",
        "A hand care gift set with four products in a pretty box.", "It rates 4.7 stars from nearly 14,000 reviewers.", "Verdict: practical and sweet."),
      P("B00394USWE", "NEST New York Scented Classic Candle, Bamboo", g + "05-nest-candle.jpg", "The girl whose home always smells amazing",
        "A designer-looking candle in a glass jar that looks right on any shelf.", "It has a 4.6-star rating from more than 1,100 reviewers.", "Verdict: the boutique-looking gift."),
      P("B0D92YB4RH", "O'Bright Seraph Mini Cordless LED Table Lamp", g + "06-obright-mini-lamp.jpg", "The aesthetic nightstand",
        "A small cordless lamp with a dimmer and a rechargeable battery.", "It rates 4.6 stars from more than 1,300 reviewers.", "Verdict: part decor, part gadget."),
      P("B09MDG5ZQ7", "Kitsch Satin Pillowcase with Zipper, 2-Pack", g + "07-kitsch-satin-pillowcase.jpg", "The beauty-sleep upgrade",
        "Satin pillowcases with a zipper closure, in colors that wrap well.", "It has a 4.6-star rating from more than 31,000 reviewers.", "Verdict: a spa moment for her bed."),
      P("B09X3HB2BR", "Sol de Janeiro Cheirosa Hair & Body Perfume Mist", g + "08-sol-de-janeiro-mist.jpg", "The scent she keeps asking about",
        "A hair and body mist from one of the most-gifted fragrance brands right now.", "It rates 4.7 stars from more than 53,000 reviewers. Choose a scent on the page.", "Verdict: the squeal-worthy splurge.")],
     {"3": "The best friend gift says 'I remember that thing you mentioned in May.'", "6": "A handwritten note makes any of these feel twice as expensive."},
     ["And that's the list: eight Amazon gifts for the friend who knows everything about you.",
      "If you take one thing from this guide, let it be this. Pair one pretty thing with one cozy thing and add a note.",
      "Until the next gift emergency, darling."],
     {"kicker": "THE GIFT EDIT", "h1": ["Gifts for Your", "Best Friend"], "sub": "(she'll know it's from you)", "tile": ["bestie", "approved"], "cta1": "READ THE GUIDE",
      "hero_kicker": "CHRISTMAS 2026", "hero_lines": ["8 Gifts Your", "Best Friend Will", "Actually Love"], "hero_tag": "pretty. cozy. a little dramatic.",
      "cta2": "GET THE LIST", "cta3": "SHOP ALL 8", "hero_index": 4, "small_idx": [0, 1, 5, 7]}, rel)

g = 'images/blog/dupes/'
post("luxe-looking-amazon-finds-for-less", "Luxe-Looking Finds for Less",
     "Luxe-Looking Beauty Finds for Less: 8 Budget Picks With a Designer Vibe",
     "Luxe-Looking Beauty Finds for Less: 8 Amazon Picks | Looks Like Luxe",
     "Luxe-looking beauty and hair finds for less on Amazon: a glow filter, a viral mascara, a gripping primer, a lip gloss, a warm vanilla perfume and more. Eight best-reviewed budget picks.",
     "The Beauty Edit",
     ["Rich-girl taste, real-girl budget. It's the whole brand, and it's the whole point of this list.",
      "These are the affordable beauty and hair picks that give a designer vibe without the designer price tag. To be clear, I'm not claiming any of them is identical to a luxury product. They're simply well-reviewed, budget-friendly finds with a luxe feel.",
      "Every pick has a 4.4-star rating or higher on Amazon. I haven't tested them, so read the reviews and check the shade or size for you.",
      "Let's save you some money, darling."],
     [P("B0B5MGBDHZ", "e.l.f. Halo Glow Liquid Filter", g + "01-elf-halo-glow.jpg", "A glow product with a loyal following",
        "A hydrating complexion booster you can wear alone or under foundation.", "It has a 4.5-star rating from more than 21,000 reviewers. Choose a shade on the page.", "Verdict: a lit-from-within look for about the price of lunch."),
      P("B08H3JPH74", "Maybelline Lash Sensational Sky High Mascara", g + "02-maybelline-sky-high.jpg", "The drugstore mascara everyone talks about",
        "A volumizing, lengthening mascara that has become a staple.", "It rates 4.5 stars from more than 190,000 reviewers.", "Verdict: big lashes, small price."),
      P("B09XMYFTB7", "e.l.f. Power Grip Primer", g + "03-elf-power-grip-primer.jpg", "Makeup that stays put",
        "A gel primer designed to help makeup grip and last.", "It has a 4.6-star rating from more than 44,000 reviewers.", "Verdict: a popular budget step."),
      P("B00ICT8JRC", "NYX Professional Makeup Butter Gloss", g + "04-nyx-butter-gloss.jpg", "Glossy, non-sticky lips for under ten dollars",
        "A creamy, non-sticky lip gloss in many shades.", "It rates 4.5 stars from more than 126,000 reviewers. Pick your shade on the page.", "Verdict: a very giftable stocking stuffer."),
      P("B0B92Y18GT", "Lattafa Khamrah Eau de Parfum", g + "05-lattafa-khamrah.jpg", "A warm vanilla and spice perfume with a luxe feel",
        "A warm, spicy gourmand perfume that has been going viral for its price.", "It has a 4.5-star rating from more than 39,000 reviewers.", "Verdict: a full bottle for the price of a mini."),
      P("B0FFLTC255", "Mythsight StyleVibe 6-in-1 Air Styler", g + "06-mythsight-air-styler.jpg", "Salon-style hair tools at a lower price",
        "A multi-attachment air styler with a dryer and auto-wrap curlers.", "It rates 4.5 stars from more than 1,600 reviewers, a smaller sample, so read the reviews.", "Verdict: the splurge-ish pick on this list."),
      P("B01LSUQSB0", "REVLON One-Step Volumizer Hair Dryer and Styler", g + "07-revlon-one-step.jpg", "The blowout shortcut",
        "A dryer-brush that dries and styles in one pass.", "It has a 4.6-star rating from more than 350,000 reviewers.", "Verdict: a salon-looking blowout without the salon."),
      P("B09MDG5ZQ7", "Kitsch Satin Pillowcase with Zipper, 2-Pack", g + "08-kitsch-satin-pillowcase.jpg", "The beauty-sleep luxe",
        "A pair of satin pillowcases with a zipper closure.", "It rates 4.6 stars from more than 31,000 reviewers.", "Verdict: a small luxury you use every night.")],
     {"3": "Luxe isn't the price tag. It's the feeling.", "6": "Always check shade, size and reviews before you buy beauty online."},
     ["And that's the list: eight budget-friendly beauty and hair finds with a designer vibe.",
      "If you take one thing from this guide, let it be this. Pick one glow product and one scent, and you've covered the look.",
      "Until the next beauty obsession, darling."],
     {"kicker": "THE BEAUTY EDIT", "h1": ["Luxe-Looking", "Finds for Less"], "sub": "(designer vibe, small price)", "tile": ["save", "more"], "cta1": "READ THE GUIDE",
      "hero_kicker": "RICH-GIRL TASTE", "hero_lines": ["8 Budget Beauty", "Finds That Look", "Expensive"], "hero_tag": "glowy. glossy. a little dramatic.",
      "cta2": "GET THE LIST", "cta3": "SHOP ALL 8", "hero_index": 4, "small_idx": [0, 1, 2, 3]},
     [{"title": "Perfume Layering Combos", "url": "/blog/perfume-layering-combos.html"}, {"title": "Hair and Scalp Care", "url": "/blog/hair-scalp-care.html"},
      {"title": "The Luxe Gift Vault (free)", "url": "/index.html#signup"}])

p = 'tools/make_collage_pins.py'
s = open(p, encoding='utf-8').read()
s = s.replace("    'vitamins':", "    'gifts-teen': ('images/blog/gifts-teen', 'AMAZON GIFT FINDS', ['Gifts for', 'Teen Girls'], '', 'SHOP THE LIST'),\n    'gifts-bff': ('images/blog/gifts-bff', 'AMAZON GIFT FINDS', ['Gifts for Your', 'Best Friend'], '', 'SHOP THE LIST'),\n    'dupes': ('images/blog/dupes', 'AMAZON BEAUTY FINDS', ['Luxe-Looking', 'Finds for Less'], '', 'SHOP THE LIST'),\n    'vitamins':", 1)
s = s.replace("CARDS = {", "CARDS = {'gifts-teen': {1, 5, 6}, 'gifts-bff': {0, 1, 3}, 'dupes': {0, 4}, ", 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
