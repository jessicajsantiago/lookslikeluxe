"""Make a Mightypreneur Social Planner ADVANCED bulk CSV for Pinterest pins.
Usage: python tools/make_pin_csv.py out.csv
Times below are Eastern; the importer reads CSV times as Pacific, so we subtract 3 hours when writing.
Board is chosen on the review screen (not in the CSV)."""
import csv, sys, datetime as dt

SITE = "https://lookslikeluxe.netlify.app"
ROW1 = (["All Social"] * 12 + ["Facebook", "Instagram", "LinkedIn", "LinkedIn"] + ["Google (GBP)"] * 10 + ["YouTube"] * 3 + ["TikTok"] * 7 + ["Community"] * 2 + ["Pinterest"] * 2)
ROW2 = ["postAtSpecificTime (YYYY-MM-DD HH:mm:ss)", "content", "OGmetaUrl (url)", "imageUrls (comma-separated)", "gifUrl", "videoUrls (comma-separated)", "thumbnailUrl",
        "mediaOptimization (true/false)", "applyWatermark (true/false)", "tags (comma-separated)", "category", "followUpComment", "type (post/story/reel)", "type (post/story/reel)",
        "pdfTitle", "postAsPdf (true/false)", "eventType (call_to_action/event/offer)", "actionType (none/order/book/shop/learn_more/call/sign_up)", "title", "offerTitle",
        "startDate (YYYY-MM-DD HH:mm:ss)", "endDate (YYYY-MM-DD HH:mm:ss)", "termsConditions", "couponCode", "redeemOnlineUrl", "actionUrl", "title",
        "privacyLevel (private/public/unlisted)", "type (video/short)", "privacyLevel (everyone/friends/only_me)", "promoteOtherBrand (true/false)", "enableComment (true/false)",
        "enableDuet (true/false)", "enableStitch (true/false)", "videoDisclosure (true/false)", "promoteYourBrand (true/false)", "title", "notifyAllGroupMembers (true/false)", "title", "link"]
assert len(ROW1) == len(ROW2) == 40

# slug -> (post url path, [(variant file suffix, pinterest title, description) x3])
COPY = {
    "gifts-for-8-10-year-old-girls": [
        ("v1-grid", "Gifts for 8-10 Year Old Girls: 8 Picks She Won't Call Cringe",
         "Gifts for 8 to 10 year old girls that are not babyish: an American Girl doll, a Tamagotchi Uni, an instant camera, a blanket hoodie and more. Tween-approved birthday and Christmas gift ideas, all on Amazon. Tap through for the full list."),
        ("v2-hero", "Gift Ideas for 9 Year Old Girls She Will Actually Use",
         "Birthday and Christmas gift ideas for girls age 8, 9 and 10 that make you the cool aunt, mom or friend. Instant camera, Squishmallows, a Stanley and a charm bracelet kit. See all 8 picks."),
        ("v3-list", "Best Gifts for Tween Girls Ages 8-10 (Zero Cringe)",
         "The best gifts for tween girls ages 8 to 10, from nostalgic Tamagotchis to cozy blanket hoodies and roller skates. Eight ideas, all with great reviews. Tap to see the whole list."),
    ],
    "clean-girl-gift-guide": [
        ("v1-grid", "Clean Girl Gift Guide: 8 Gifts for the Dewy, Gold-Hoop Girl",
         "A clean girl gift guide for the glowy, slicked-back, matcha-sipping girl on your list. Skincare, lip mask, hair oil, gold hoops and more. Aesthetic gift ideas for her, all on Amazon. Tap through for all 8."),
        ("v2-hero", "Clean Girl Aesthetic Gift Ideas She Will Love",
         "Gift ideas for the clean girl aesthetic: Tatcha, Laneige, Sol de Janeiro, Olaplex and a gold hoop. Polished, simple and a little expensive-looking. See the full guide."),
        ("v3-list", "Gifts for Girls Who Love Skincare and Clean Girl Aesthetic",
         "Gifts for the girl who loves skincare, matcha and gold jewelry. Eight clean girl aesthetic gift ideas that look luxe, all with great reviews. Tap to shop the list."),
    ],
    "gifts-for-women-in-their-20s": [
        ("v1-grid", "Gifts for Women in Their 20s: 8 Ideas She'll Actually Use",
         "Gifts for women in their 20s who say they don't need anything but absolutely do: a cozy throw, an instant camera, a Kindle, a sunrise alarm and more. Chic, useful gift ideas for her. Tap for all 8."),
        ("v2-hero", "Gift Ideas for 25 Year Old Women (Not Another Candle)",
         "Gift ideas for women in their twenties that feel like a treat, from a Barefoot Dreams throw to an AirTag 4 pack and a Theragun Mini. See the full list of 8."),
        ("v3-list", "Best Gifts for Her in Her 20s: Chic, Useful and Not Boring",
         "The best gifts for her in her 20s: eight ideas that make adult life a little softer and more organized. Birthday and Christmas gift ideas, all on Amazon. Tap to browse."),
    ],
    "host-hostess-gifts": [
        ("v1-grid", "Host & Hostess Gifts: 8 Ideas Better Than Wine",
         "Host and hostess gifts that go way beyond a bottle of wine: a cocktail smoker kit, a champagne saber, a truffle oil duo, a bitters trio and more. Elegant dinner party gift ideas, all on Amazon. Tap for all 8."),
        ("v2-hero", "Hostess Gift Ideas She Will Actually Remember",
         "Hostess gift ideas for the woman who has everything and throws great parties. A charcuterie board, a bartender kit, a Nest candle and more. See the full list of 8."),
        ("v3-list", "Unique Host Gifts for Dinner Parties and Housewarmings",
         "Unique host gifts for dinner parties, housewarmings and the holidays. Eight giftable ideas that say thank you and make you the guest everyone invites back. Tap to browse."),
    ],
}

# (slug, variant index) in posting order, with Eastern datetime
def schedule(start=dt.datetime(2026, 10, 11, 12, 0)):
    order = []
    for v in range(3):
        for slug in COPY:
            order.append((slug, v))
    t = start
    out = []
    for item in order:
        out.append((item, t))
        t = t + dt.timedelta(hours=6) if t.hour == 12 else (t.replace(hour=12) + dt.timedelta(days=1))
    return out


def main(path):
    rows = [ROW1, ROW2]
    for (slug, v), et in schedule():
        suffix, title, desc = COPY[slug][v]
        pt = et - dt.timedelta(hours=3)   # importer reads Pacific
        row = [""] * 40
        row[0] = pt.strftime("%Y-%m-%d %H:%M:%S")
        row[1] = desc
        row[3] = f"{SITE}/pins/{slug}-{suffix}.png"
        row[7] = "false"; row[8] = "false"
        row[38] = title
        row[39] = f"{SITE.replace('https://', '')}/blog/{slug}.html"   # the UI field adds https:// itself
        rows.append(row)
        print(et.strftime("%a %b %d %I:%M %p ET"), "|", slug, suffix)
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pins-batch1.csv")
