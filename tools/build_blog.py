"""Build the Looks Like Luxe blog: posts/*.json -> blog/<slug>.html, blog/index.html, sitemap.xml.
Run from the project root:  python tools/build_blog.py
Add a post by dropping a JSON file in posts/ (see gifts-for-5-year-old-girls.json for the shape)."""
import glob, html, json, os

SITE = "https://lookslikeluxe.netlify.app"
TAG = "lookslikeluxe-20"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@500;600&family=Playfair+Display:ital,wght@0,500;1,500&display=swap" rel="stylesheet">')
GHL_FORM = ('<iframe src="https://api.leadconnectorhq.com/widget/form/gsRUZDDIsJEpAF1ZlzP9" style="width:100%;height:100%;border:none;border-radius:8px" '
            'id="inline-gsRUZDDIsJEpAF1ZlzP9" data-layout="{\'id\':\'INLINE\'}" data-trigger-type="alwaysShow" data-trigger-value="" '
            'data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value="" '
            'data-form-name="Gift Guide Signup Form" data-height="434" data-layout-iframe-id="inline-gsRUZDDIsJEpAF1ZlzP9" '
            'data-form-id="gsRUZDDIsJEpAF1ZlzP9" data-cookie-consent="true" data-cookie-consent-provider="auto" title="Gift Guide Signup Form"></iframe>'
            '<script src="https://link.msgsndr.com/js/form_embed.js"></script>')
e = html.escape


def nav():
    return ('<div class="b-disc">As an Amazon Associate I earn from qualifying purchases.</div>'
            '<header class="b-nav"><a class="b-brand" href="/">Looks Like <em>Luxe</em></a>'
            '<nav><a href="/blog/">The Edit</a><a href="/l/gifts-for-her">Gifts</a><a href="/index.html#signup">Free Guide</a></nav></header>')


def footer():
    return ('<footer class="b-foot">&copy; Looks Like Luxe &middot; Rich-girl taste, real-girl budget.<br>'
            'As an Amazon Associate I earn from qualifying purchases. Prices and availability are shown on Amazon. '
            'Product names are trademarks of their owners.<br><a href="/privacy.html">Privacy &amp; disclosure</a></footer>')


def page(title, desc, body, canonical, og_image=None):
    og = f'<meta property="og:image" content="{SITE}/{og_image}">' if og_image else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{SITE}{canonical}">'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="article">{og}'
            f'{FONTS}<link rel="stylesheet" href="/blog.css"></head><body class="blog">{body}</body></html>')


def build_post(p):
    prods = []
    for i, pr in enumerate(p["products"], 1):
        link = f'https://www.amazon.com/dp/{pr["asin"]}?tag={TAG}'
        copy = "".join(f"<p>{e(t)}</p>" for t in pr["copy"])
        prods.append(
            f'<article class="b-prod"><p class="b-num">{i:02d}</p><h2>{e(pr["name"])}</h2>'
            f'<span class="b-best">Best for: {e(pr["best_for"])}</span>'
            f'<a class="b-photo" href="{link}" target="_blank" rel="sponsored nofollow noopener"><img src="/{pr["image"]}" alt="{e(pr["name"])}" loading="lazy"></a>'
            f'{copy}<a class="b-btn" href="{link}" target="_blank" rel="sponsored nofollow noopener">Shop on Amazon</a></article>')
        q = p.get("interludes", {}).get(str(i))
        if q:
            prods.append(f'<div class="b-quote"><p>&ldquo;{e(q)}&rdquo;</p></div>')
    intro = "".join(f"<p>{e(t)}</p>" for t in p["intro"])
    outro = "".join(f"<p>{e(t)}</p>" for t in p["outro"])
    related = "".join(f'<a href="{e(r["url"])}">{e(r["title"])}</a>' for r in p.get("related", []))
    body = (nav() +
            f'<section class="b-hero"><div class="b-kicker">{e(p["kicker"])}</div><h1>{e(p["headline"])}</h1><div class="b-rule"></div>'
            f'<div class="b-by">By Looks Like Luxe &nbsp;&middot;&nbsp; {e(p["date"])} &nbsp;&middot;&nbsp; {e(p["read_time"])}</div></section>'
            f'<main class="b-wrap"><div class="b-note"><strong>Affiliate disclosure:</strong> {e(p["disclosure"])}</div>'
            f'<div class="b-intro">{intro}</div><div class="b-sep">&#9830; &#9830; &#9830;</div>{"".join(prods)}'
            f'<div class="b-sep">&#9830; &#9830; &#9830;</div><div class="b-outro">{outro}<div class="b-sign">xx, Looks Like Luxe</div></div>'
            f'<section class="b-signup"><h2>Get the Luxe Holiday Gift Guide, free</h2><p>25 gifts that look like you spent way more, plus one fun email a week with the prettiest finds. Zero spam. Zero sad candles.</p><div class="form">{GHL_FORM}</div></section>'
            f'<section class="b-related"><h3>Keep reading</h3>{related}</section></main>' + footer())
    return page(p["seo_title"], p["description"], body, f'/blog/{p["slug"]}.html', p.get("pin_image"))


def build_index(posts):
    cards = []
    for p in posts:
        cards.append(f'<a class="bi-card" href="/blog/{p["slug"]}.html"><div class="im"><img src="/{p["products"][0]["image"]}" alt="{e(p["title"])}" loading="lazy"></div>'
                     f'<div class="tx"><div class="k">{e(p["kicker"])}</div><h2>{e(p["headline"])}</h2><p>{e(p["description"])}</p></div></a>')
    body = (nav() + '<section class="b-hero"><div class="b-kicker">The Edit</div><h1>Looks like luxe. Isn\'t.</h1><div class="b-rule"></div>'
            '<div class="b-by">Gift guides, room refreshes, and finds with a flair for the dramatic</div></section>'
            f'<div class="bi-grid">{"".join(cards)}</div>' + footer())
    return page("The Edit | Looks Like Luxe", "Gift guides, room refreshes and luxe-looking finds, curated with drama and a budget.", body, "/blog/")


def main():
    os.makedirs("blog", exist_ok=True)
    posts = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob("posts/*.json"))]
    for p in posts:
        open(f'blog/{p["slug"]}.html', "w", encoding="utf-8").write(build_post(p))
    open("blog/index.html", "w", encoding="utf-8").write(build_index(posts))
    feed = [{"slug": p["slug"], "headline": p["headline"], "kicker": p["kicker"], "description": p["description"], "image": p["products"][0]["image"], "date": p["date"]} for p in posts]
    json.dump(feed, open("blog/posts.json", "w", encoding="utf-8"), indent=1)
    urls = ["/", "/blog/", "/l/gifts-for-her", "/l/cozy-fall-living-room"] + [f'/blog/{p["slug"]}.html' for p in posts]
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls) + "</urlset>"
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print(f"built {len(posts)} post(s)")


if __name__ == "__main__":
    main()
