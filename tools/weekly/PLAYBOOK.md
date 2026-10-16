# Looks Like Luxe weekly playbook (runs Sunday evening)

Goal: research trends, propose 2-3 new Idea Lists, and BUILD all content as files. Nothing is posted, created on Amazon, or imported to Pinterest without Jessica's approval.

## Hard rules (always)
- No prices on pins/posts/videos. Amazon disclosure on everything: "As an Amazon Associate I earn from qualifying purchases."
- No "I use this" claims, no medical claims. Product rating must be 4.4+ unless Jessica picked it herself (then flag it). Check color + size options; note the chosen color/size.
- Voice: Carrie Bradshaw / sassy. Palette: chocolate, gold, cream. LLL = lookslikeluxe (Amazon). Personal @PrettyGirlsLoveJess = Pretty Girls Love Co (Etsy) ONLY. Never mix; never upload PGLC pins to LLL.
- Tracking ID lookslikeluxe-20. Minimal Netlify deploys: batch blog changes into ONE deploy, only after approval.
- Run python as `py`. Work from C:\Users\jessi\LooksLikeLuxe-repo.

## Weekly targets
- 2-3 new Idea Lists (+ refresh 1 older list) | ~15-20 fresh Pinterest pins (2-3/day) | 3-4 TikTok/Reels posts (mix of carousels and videos) | optional 1 blog post.
- Jessica's style: edgier, street style, younger demo for fashion; neutral black/white/tan/brown for home ("looks like Ralph Lauren, is Amazon").

## Steps
1. **Research** (Chrome TikTok search + Pinterest search + WebSearch): what is trending for fall/holiday fashion, home decor, beauty. Note top formats (video vs carousel), titles, view counts. Check the calendar: upcoming holidays/events in the next 2-4 weeks.
1b. **Validate demand on Pinterest Trends** (trends.pinterest.com) for each candidate list topic before building. Also check YouTube search for low-competition queries; the vertical list videos can also be posted as YouTube Shorts.
2. **Review last week's results** if numbers are provided (saves, link clicks, Creator Hub clicks). Keep what worked.
3. **Pick 2-3 list ideas** with reasons. For each list: 8-12 candidate products (name, ASIN, rating, color/size note). Product pages block WebFetch; use the Amazon tab in Chrome or ask Jessica for links. Save to `weekly/<date>/lists.md`.
4. **Build content** into `weekly/<date>/`:
   - Pin images via tools/make_collage_pins.py and tools/make_product_pins.py patterns; pins CSV for Mightypreneur (Advance format; board per post; LLL account separate from personal).
   - TikTok carousels via tools/make_tiktok_carousels.py; videos via tools/make_list_videos.py.
   - Captions file (no prices, disclosure, hashtags, bio-link reminder).
5. **Write `weekly/<date>/SUMMARY.md`**: what was found, the lists, what was built, and an APPROVAL CHECKLIST: (a) create the Idea Lists in Creator Hub (Jessica approves; Chrome often freezes, use browse-history + swatch flow), (b) import the CSV in Mightypreneur picking the right account, (c) post TikToks manually.
6. Tell Jessica where the folder is and keep the message short.

## Known gotchas
- Amazon "Add products" modal: use Browse history after visiting product pages; the arrow opens a product view with size/color swatches (clicking a swatch swaps the list item in place).
- Pinterest: scheduled pins page only shows for the logged-in account; account menu switches accounts.
- Chrome tabs freeze; refresh and call tabs_context_mcp for new tab IDs.
