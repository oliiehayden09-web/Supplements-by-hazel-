#!/usr/bin/env python3
"""Builds supplementsbyhazel.com into public/.

    python3 build.py

- src/pages/*.html are page bodies. Each starts with a <!--meta {...} --> JSON block (title,
  description, nav, scripts, ...). The shared header, footer, basket and newsletter wrap them.
- The shop page and every product page are generated from data/catalog.py.
- Also writes sitemap.xml, robots.txt and redirects.json (old Wix URLs -> new pages).

Only the standard library is used. Everything in public/ except css/, js/ and assets/ is generated:
edit src/ and data/, then rebuild.
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "data"))
import catalog as C  # noqa: E402

PUBLIC = ROOT / "public"
SITE = "https://www.supplementsbyhazel.com"
TODAY = date.today().isoformat()
EMAIL = "hello@supplementsbyhazel.com"
PHONE = "0117 462 3935"
PHONE_TEL = "+441174623935"

# The thin bar above the header. Change it for each promotion, or set it to "" to hide it.
ANNOUNCE = 'Free delivery on every order · <strong>50% off Rosy</strong>, taken off in your basket'

e = html.escape
W = "https://static.wixstatic.com/media/"


def img(url, w, h, mode="fill"):
    """A sized Wix media URL (Wix resizes on the fly)."""
    if "static.wixstatic.com/media/" in url and "/v1/" not in url:
        name = re.sub(r"[^a-z0-9.]+", "-", url.rsplit("/", 1)[-1].lower())
        name = re.sub(r"\.(png|jpe?g|webp)$", "", name)[:40] or "image"
        return f"{url}/v1/{mode}/w_{w},h_{h},al_c,q_85,enc_auto/{name}.webp"
    return url


ICONS = {
    "bag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "user": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14z"/><path d="M5 19l7-7"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V4M5 4h11l-2 4 2 4H5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/></svg>',
    "repeat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11V9a3 3 0 0 1 3-3h12l-3-3M20 13v2a3 3 0 0 1-3 3H5l3 3"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/></svg>',
    "mind": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M8.5 14.5c1.8 2 5.2 2 7 0M9 9.5h.01M15 9.5h.01"/></svg>',
    "sparkle": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/></svg>',
    "bone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.5 4.5a2.5 2.5 0 0 0-3.4 3.4 2.5 2.5 0 0 0 2.4 3.6l7 7a2.5 2.5 0 0 0 3.6 2.4 2.5 2.5 0 0 0 3.4-3.4 2.5 2.5 0 0 0-2.4-3.6l-7-7A2.5 2.5 0 0 0 7.5 4.5z"/></svg>',
    "moon": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>',
    "flower": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="10" r="2.5"/><path d="M12 7.5C12 4 9 3 9 3s-1 3 3 4.5zM14.5 10c3.5 0 4.5-3 4.5-3s-3-1-4.5 3zM12 12.5c0 3.5 3 4.5 3 4.5s1-3-3-4.5zM9.5 10C6 10 5 13 5 13s3 1 4.5-3zM12 13v8"/></svg>',
    "sun": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "quiz": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="8" width="18" height="4"/><path d="M5 12v9h14v-9M12 8v13M12 8S10.5 3 8 4.5 9.5 8 12 8zM12 8s1.5-5 4-3.5S14.5 8 12 8z"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4V5z"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
    "steth": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3v6a4 4 0 0 0 8 0V3"/><path d="M10 13v2a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="11" r="2"/></svg>',
}

SOCIAL = [
    ("Facebook", "https://www.facebook.com/supplementsbyhazel", '<path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/>'),
    ("Instagram", "https://www.instagram.com/supplementsbyhazel", '<path d="M12 7.2A4.8 4.8 0 1 0 12 16.8 4.8 4.8 0 0 0 12 7.2zm0 7.9a3.1 3.1 0 1 1 0-6.2 3.1 3.1 0 0 1 0 6.2zm5-8.1a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM12 3.6c2.7 0 3 0 4.1.1 1 0 1.5.2 1.9.3.5.2.8.4 1.1.7.3.3.6.7.7 1.1.1.4.3.9.3 1.9.1 1.1.1 1.4.1 4.1s0 3-.1 4.1c0 1-.2 1.5-.3 1.9-.2.5-.4.8-.7 1.1-.3.3-.7.6-1.1.7-.4.1-.9.3-1.9.3-1.1.1-1.4.1-4.1.1s-3 0-4.1-.1c-1 0-1.5-.2-1.9-.3-.5-.2-.8-.4-1.1-.7-.3-.3-.6-.7-.7-1.1-.1-.4-.3-.9-.3-1.9C3.6 15 3.6 14.7 3.6 12s0-3 .1-4.1c0-1 .2-1.5.3-1.9.2-.5.4-.8.7-1.1.3-.3.7-.6 1.1-.7.4-.1.9-.3 1.9-.3C9 3.6 9.3 3.6 12 3.6zM12 2c-2.7 0-3.1 0-4.1.1-1.1 0-1.8.2-2.4.5-.7.3-1.2.6-1.8 1.2S2.9 4.9 2.6 5.5c-.3.6-.4 1.4-.5 2.4C2 8.9 2 9.3 2 12s0 3.1.1 4.1c0 1.1.2 1.8.5 2.4.3.7.6 1.2 1.2 1.8.6.6 1.1.9 1.8 1.2.6.2 1.4.4 2.4.5 1 .1 1.4.1 4.1.1s3.1 0 4.1-.1c1.1 0 1.8-.2 2.4-.5.7-.3 1.2-.6 1.8-1.2.6-.6.9-1.1 1.2-1.8.2-.6.4-1.4.5-2.4.1-1 .1-1.4.1-4.1s0-3.1-.1-4.1c0-1.1-.2-1.8-.5-2.4-.3-.7-.6-1.2-1.2-1.8-.6-.6-1.1-.9-1.8-1.2-.6-.2-1.4-.4-2.4-.5C15.1 2 14.7 2 12 2z"/>'),
    ("TikTok", "https://www.tiktok.com/@supplementsbyhazel_", '<path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.7 5.7 0 1 0 4.9 5.7V9.1a7.3 7.3 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6z"/>'),
    ("LinkedIn", "https://www.linkedin.com/company/supplementsbyhazel", '<path d="M6.9 8.8H3.6V20h3.3V8.8zM5.2 3.5a1.9 1.9 0 1 0 0 3.9 1.9 1.9 0 0 0 0-3.9zM20.4 13.6c0-3-1.6-5-4.3-5-1.5 0-2.6.8-3 1.6V8.8H9.9V20h3.3v-5.6c0-1.5.3-2.9 2.1-2.9s1.8 1.7 1.8 3V20h3.3v-6.4z"/>'),
]


def menu_item(key):
    p = C.PRODUCTS[key]
    return (f'<li><a href="/{p["file"]}" data-acc="{p["acc"]}"><span class="dot"></span>'
            f'<span>{e(p.get("short", p["name"]))}<small>{e(p["menu_note"])}</small></span></a></li>')


def header(nav):
    def cur(k):
        return ' aria-current="page"' if nav == k else ""
    shop_menu = "".join(menu_item(k) for k in C.SINGLES) + "<li><hr></li>" + "".join(menu_item(k) for k in C.BUNDLES) + \
        '<li><hr></li><li><a href="/shop.html#goals"><span>Shop by health goal<small>Energy, mood, hair and skin, bones</small></span></a></li>' + \
        '<li><a href="/shop.html"><span>Shop all<small>All products and bundles</small></span></a></li>'
    announce = f'<div class="announce">{ANNOUNCE}</div>\n' if ANNOUNCE else ""
    return f'''<a class="skip-link" href="#main">Skip to content</a>
{announce}<header class="site">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="/" aria-label="Supplements by Hazel, home"><img src="/assets/wordmark-navy.png" alt="Supplements by Hazel" width="197" height="40"></a>
    <ul class="nav-links" id="nav-links">
      <li class="has-menu"><button type="button" class="drop" aria-expanded="false" aria-controls="menu-shop">Shop</button>
        <ul class="menu" id="menu-shop">{shop_menu}</ul></li>
      <li><a href="/quiz.html"{cur("quiz")}>Take the quiz</a></li>
      <li><a href="/about.html"{cur("about")}>Our story</a></li>
      <li><a href="/blog.html"{cur("blog")}>Journal</a></li>
      <li><a href="/help.html"{cur("help")}>Help</a></li>
    </ul>
    <div class="nav-actions">
      <a class="icon-btn account-link" href="/account.html" aria-label="Your account">{ICONS["user"]}<span>Account</span></a>
      <button type="button" class="icon-btn" data-cart-open aria-label="Open basket">{ICONS["bag"]}<span class="cart-count" data-cart-count></span></button>
      <button type="button" class="icon-btn menu-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">{ICONS["menu"]}</button>
    </div>
  </nav>
</header>'''


def footer():
    socials = "".join(f'<li><a href="{u}" target="_blank" rel="noopener" aria-label="Supplements by Hazel on {n}"><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg></a></li>' for n, u, p in SOCIAL)
    shop = "".join(f'<li><a href="/{C.PRODUCTS[k]["file"]}">{e(C.PRODUCTS[k].get("short", C.PRODUCTS[k]["name"]))}</a></li>' for k in C.SINGLES + C.BUNDLES)
    return f'''<section class="newsletter" aria-labelledby="nl-title">
  <div class="wrap nl-grid">
    <div class="nl-copy">
      <h2 id="nl-title">Join our mailing list</h2>
      <p>Offers, new products and Hazel's latest articles. Unsubscribe at any time.</p>
      <p class="nl-note">We use your details as set out in our <a href="/privacy.html">Privacy Policy</a>.</p>
    </div>
    <div id="newsletter-form" class="nl-form"></div>
  </div>
</section>

<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img src="/assets/wordmark-cream.png" alt="Supplements by Hazel" width="187" height="38" loading="lazy">
        <p>Food supplements formulated by Hazel Hayden, Consultant Nurse and British Menopause Society Registered Specialist. Made in the UK.</p>
        <ul class="foot-badges"><li>Free delivery</li><li>30-day money-back guarantee</li><li>Made in the UK</li><li>Biodegradable packaging</li></ul>
        <ul class="socials" aria-label="Supplements by Hazel on social media">{socials}</ul>
      </div>
      <div>
        <h4>Shop</h4>
        <ul>{shop}<li><a href="/shop.html">Shop all</a></li></ul>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="/about.html">Our story</a></li>
          <li><a href="/about.html#hazel">Meet Hazel</a></li>
          <li><a href="/about.html#team">Meet the team</a></li>
          <li><a href="/blog.html">Journal</a></li>
          <li><a href="/help.html">Help &amp; FAQs</a></li>
          <li><a href="/account.html">Your account</a></li>
        </ul>
        <h4 style="margin-top:22px">Our clinics</h4>
        <ul>
          <li><a href="https://www.bristolmenopause.com" target="_blank" rel="noopener">Bristol Menopause &amp; Wellwoman Clinic</a></li>
          <li><a href="https://www.bristolhealthhub.com" target="_blank" rel="noopener">Bristol Health Hub</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="/help.html#contact">Contact us</a></li>
        </ul>
      </div>
    </div>
    <p class="legal">Food supplements should not be used as a substitute for a varied, balanced diet and a healthy lifestyle. They are not medicines and are not intended to diagnose, treat, cure or prevent any condition. If you are pregnant, breastfeeding, taking medication or have a medical condition, speak to a healthcare professional before use.<br><a href="/terms.html">Terms &amp; Conditions</a> · <a href="/privacy.html">Privacy Policy</a> · <a href="/cookies.html">Cookie Policy</a><br>© {date.today().year} Supplements by Hazel Limited. Registered in England and Wales, company number 13478359. Registered office: 4 King Square, Bridgwater, Somerset, TA6 3YF, United Kingdom.</p>
    <img class="foot-giant" src="/assets/wordmark-cream.png" alt="" width="900" height="183">
  </div>
</footer>

<div id="cart" class="cart" hidden>
  <div class="cart-scrim" data-cart-close></div>
  <aside id="cart-panel" class="cart-panel" role="dialog" aria-modal="true" aria-labelledby="cart-title">
    <div class="cart-head">
      <h2 id="cart-title">Your basket</h2>
      <button type="button" id="cart-close" class="linkbtn" data-cart-close aria-label="Close basket">Close</button>
    </div>
    <div id="cart-body" class="cart-body"></div>
    <div id="cart-foot" class="cart-foot" hidden>
      <div id="cart-sums"></div>
      <button type="button" id="cart-checkout" class="btn wide">Checkout</button>
    </div>
  </aside>
</div>'''


ORG = {
    "@context": "https://schema.org", "@type": "Organization", "@id": f"{SITE}/#org",
    "name": "Supplements by Hazel Limited", "alternateName": "Supplements by Hazel", "url": f"{SITE}/",
    "logo": f"{SITE}/assets/roundel.png", "email": EMAIL, "telephone": "+44 117 462 3935",
    "founder": {"@type": "Person", "@id": f"{SITE}/about.html#hazel", "name": "Hazel Hayden", "jobTitle": "Consultant Nurse"},
    "sameAs": [u for _, u, _ in SOCIAL],
}


def page(meta, body):
    path = meta["path"]
    url = f"{SITE}/" if path == "index.html" else f"{SITE}/{path}"
    title, desc = meta["title"], meta["description"]
    og_img = meta.get("image") or img(W + "f6f1f2_b18172219e194152b95ec0dc1a4557c6~mv2.png", 1200, 1200)
    ld = [ORG] + meta.get("ld", [])
    scripts = meta.get("scripts", [])
    robots = '<meta name="robots" content="noindex">\n' if meta.get("noindex") else ""
    redirect = ('<script>if(/[?&]orderId=/.test(location.search))location.replace("/thank-you.html"+location.search)</script>\n'
                if path == "index.html" else "")
    tags = "\n".join(f'<script type="module" src="/js/{s}.js"></script>' for s in ["shop", "newsletter"] + scripts)
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{redirect}<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="{meta.get("og_type", "website")}">
<meta property="og:site_name" content="Supplements by Hazel">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{e(og_img)}">
<meta name="twitter:card" content="summary_large_image">
{"".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://static.wixstatic.com">
<link rel="stylesheet" href="/css/hazel.css">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0B3F5F">
</head>
<body>
{header(meta.get("nav"))}

<main id="main">
{body.strip()}
</main>

{footer()}

<script src="/js/site.js" defer></script>
{tags}
</body>
</html>
'''


# ---------- shared fragments ----------

def price_slot(key):
    """Live 'from' price: filled by shop.js from Wix (1-tub product)."""
    return f'<span class="card-price" data-price-slug="{C.PRODUCTS[key]["packs"][0][0]}">&nbsp;</span>'


def product_card(key, lazy=True):
    p = C.PRODUCTS[key]
    name = p.get("short", p["name"])
    badges = "".join(f'<span class="badge soft">{e(x)}</span>' for x in p.get("badges", []))
    ticks = "".join(f"<li>{e(t)}</li>" for t in p.get("benefits", []))
    return f'''<article class="card reveal" data-acc="{p["acc"]}" data-goals="{" ".join(p.get("goals", []))}">
  <a class="card-link" href="/{p["file"]}">
    <div class="card-media">
      <span class="badges"><span class="badge" data-badge-slug="{p["packs"][0][0]}" hidden></span>{badges}</span>
      <img src="{img(p["image"], 640, 640)}" alt="{e(p["alt"])}" width="640" height="640"{' loading="lazy"' if lazy else ''}>
    </div>
    <div class="card-body">
      <span class="stage">{e(p["stage"])}</span>
      <h3>{e(name)}</h3>
      <ul class="card-ticks">{ticks}</ul>
    </div>
  </a>
  <div class="card-foot">{price_slot(key)}<button type="button" class="quick-add" data-quick-add="{p["packs"][0][0]}" aria-label="Add {e(name)} to basket">{ICONS["bag"]}<span>Add</span></button></div>
</article>'''


def goal_tiles(href_prefix="/shop.html?goal="):
    icon = {"energy": "bolt", "mood": "mind", "hair-skin": "sparkle", "bones": "bone", "immunity": "shield",
            "perimenopause": "moon", "menopause": "flower", "post": "sun"}
    return "".join(f'<li><a href="{href_prefix}{k}#products">{ICONS[icon[k]]}<strong>{e(label)}</strong><span>{e(sub)}</span></a></li>'
                   for k, label, sub in C.GOALS)


def faq_html(items):
    out = []
    for q, ans in items:
        out.append(f'<details><summary>{e(q)}</summary><div class="answer">{"".join(f"<p>{e(a)}</p>" for a in ans)}</div></details>')
    return '<div class="faq">' + "".join(out) + "</div>"


def stars():
    return '<p class="review-stars" role="img" aria-label="5 out of 5 stars">★★★★★</p>'


def fragments():
    return {
        "products_singles": "\n".join(product_card(k, i > 1) for i, k in enumerate(C.SINGLES)),
        "products_bundles": "\n".join(product_card(k) for k in C.BUNDLES),
        "products_extras": "\n".join(product_card(k) for k in C.EXTRAS),
        "team": "\n".join(f'<li class="reveal"><span class="role">{e(r)}</span><h3>{e(n)}</h3><p>{e(t)}</p></li>' for r, n, t in C.TEAM),
        "posts_fallback": posts_html(json.loads((ROOT / "data" / C.POSTS_FILE).read_text())),
        "posts_latest": posts_html(json.loads((ROOT / "data" / C.POSTS_FILE).read_text())[:3]),
        "goal_tiles": goal_tiles(),
        "hero_fan": "".join(
            f'<a class="fan-card" href="/{C.PRODUCTS[k]["file"]}" data-acc="{C.PRODUCTS[k]["acc"]}" style="--i:{i}">'
            f'<img src="{img(C.PRODUCTS[k]["image"], 520, 520)}" alt="{e(C.PRODUCTS[k]["alt"])}" width="520" height="520">'
            f'<span><strong>{e(C.PRODUCTS[k]["name"])}</strong>{e(C.PRODUCTS[k]["stage"])}</span></a>'
            for i, k in enumerate(C.SINGLES)),
        "why_subscribe": why_subscribe(),
        "quiz_data": json.dumps({k: {"name": v.get("short", v["name"]), "file": v["file"], "image": img(v["image"], 640, 640),
                                     "acc": v["acc"], "stage": v["stage"], "card": v["card"], "benefits": v.get("benefits", []),
                                     "slug": v["packs"][0][0]} for k, v in C.PRODUCTS.items()}, ensure_ascii=False).replace("</", "<\\/"),
        "email": EMAIL, "phone": PHONE, "phone_tel": PHONE_TEL,
        "icon_leaf": ICONS["leaf"], "icon_flag": ICONS["flag"], "icon_shield": ICONS["shield"], "icon_heart": ICONS["heart"],
        "icon_truck": ICONS["truck"], "icon_repeat": ICONS["repeat"], "icon_steth": ICONS["steth"], "icon_quiz": ICONS["quiz"], "icon_gift": ICONS["gift"], "icon_calendar": ICONS["calendar"], "icon_chat": ICONS["chat"],
    }


def fmt_date(d):
    y, m, dd = d.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{int(dd)} {months[int(m) - 1]} {y}"


def posts_html(posts):
    return "\n".join(f'''<li><a class="post-card" href="/post.html?slug={e(p["slug"])}">
  <img src="{img(p["image"], 640, 400)}" alt="" width="640" height="400" loading="lazy">
  <div><span class="post-meta">{fmt_date(p["date"])} · {p["minutes"]} min read</span><h3>{e(p["title"])}</h3><p>{e(p["excerpt"])}</p></div>
</a></li>''' for p in posts)


# ---------- product pages ----------

def faqs_for(key):
    p = C.PRODUCTS[key]
    faqs = list(p.get("faqs", []))
    if p.get("how") and not any(q.lower().startswith("how") for q, _ in faqs):
        faqs.insert(0, ("How do I take it?", [p["how"]]))
    if key in C.BUNDLES:
        faqs = [
            ("How do I take the bundle?", ["Take each product as directed on its own label. " + " ".join(f'{C.PRODUCTS[k]["name"]}: {C.PRODUCTS[k]["how"]}' for k in p["includes"])]),
            ("What is the free gift?", ["Your first order with us includes a complimentary supplement, chosen to help you explore more of the range."]),
            ("Can I subscribe?", ["Yes. Choose Subscribe & save for a further 5% off, delivered every 1, 3 or 6 months depending on the supply you pick. There's no minimum term."]),
        ]
    faqs.append(("Is this a medicine?", [C.FOOD_SUPPLEMENT]))
    return faqs


def accordions(key):
    """The collapsible sections beside the buy box: why, how, what's inside, FAQs, delivery."""
    p = C.PRODUCTS[key]
    items = []
    if key in C.BUNDLES:
        why = "".join(f"<p>{e(t)}</p>" for t in p["intro"])
        inside = "<ul>" + "".join(f'<li><a class="textlink" href="/{C.PRODUCTS[k]["file"]}">{e(C.PRODUCTS[k]["name"])}</a>: {e(p["includes_notes"][k])}</li>' for k in p["includes"]) + "</ul>"
        how = "<ul>" + "".join(f'<li>{e(C.PRODUCTS[k]["name"])}: {e(C.PRODUCTS[k]["how"])}</li>' for k in p["includes"]) + "</ul>"
    elif p.get("simple"):
        why = "".join(f"<p>{e(t)}</p>" for t in p["intro"])
        inside = "<p>50mg of elemental iron in a vegetable cellulose capsule.</p>"
        how = f"<p>{e(p['how'])}</p>"
    else:
        why = "".join(f"<p>{e(t)}</p>" for t in p["intro"][1:]) + "<ul>" + "".join(f"<li><strong>{e(t)}.</strong> {e(d)}</li>" for t, d in p["why"]) + "</ul>"
        inside = "<ul>" + "".join(f"<li><strong>{e(n)}</strong>: {e(r)}</li>" for n, r, _ in p["ingredients"]) + '</ul><p><a class="textlink" href="#formula">See the full formula and claims</a></p>'
        how = f"<p>{e(p['how'])}</p>"
    items.append(("Why take it", why, True))
    items.append(("How to take", how + f"<p class=\"hint\">{e(C.FOOD_SUPPLEMENT)}</p>", False))
    items.append(("What's inside", inside, False))
    items.append(("FAQs", "".join(f"<p><strong>{e(q)}</strong><br>{' '.join(e(x) for x in a)}</p>" for q, a in faqs_for(key)[:-1]), False))
    items.append(("Delivery &amp; returns", '<p>Delivery is free on every order to the UK and Jersey.</p><p>If you\'re not happy, contact us within 30 days of delivery and we\'ll give you your money back. <a class="textlink" href="/help.html#delivery">Delivery and returns</a></p>', False))
    return '<div class="acc-list">' + "".join(
        f'<details class="acc"{" open" if op else ""}><summary>{t}</summary><div class="acc-body prose">{b}</div></details>' for t, b, op in items) + "</div>"


def buy_section(key):
    p = C.PRODUCTS[key]
    name = p.get("short", p["name"])
    packs = json.dumps([{"slug": s, "label": l, "note": n} for s, l, n in p["packs"]])
    thumbs = ""
    if len(p["gallery"]) > 1:
        thumbs = '<ul class="thumbs">' + "".join(
            f'<li><button type="button" data-thumb="{img(g, 1000, 1000)}" aria-pressed="{str(i == 0).lower()}" aria-label="Show image {i + 1}"><img src="{img(g, 160, 160)}" alt="" width="74" height="74" loading="lazy"></button></li>'
            for i, g in enumerate(p["gallery"])) + "</ul>"
    badges = "".join(f'<span class="badge soft">{e(x)}</span>' for x in p.get("badges", []))
    ticks = "".join(f"<li>{e(t)}</li>" for t in p.get("benefits", []))
    unit = "bundle" if key in C.BUNDLES else "tub"
    return f'''<section class="product-top" data-acc="{p["acc"]}">
  <div class="wrap">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/shop.html">Shop</a><span aria-hidden="true">/</span>{e(name)}</nav>
    <div class="shop-grid" style="margin-top:22px">
      <div class="gallery">
        <div class="gallery-main"><span class="badges">{badges}</span><img id="shop-img" src="{img(p["gallery"][0], 1000, 1000)}" alt="{e(p["alt"])}" width="1000" height="1000" fetchpriority="high"></div>
        {thumbs}
      </div>
      <div class="shop-info">
        <span class="stage acc-bar">{e(p["stage"])}</span>
        <h1>{e(p["name"])}</h1>
        <p class="tagline">{e(p["tagline"])}</p>
        <ul class="pdp-ticks">{ticks}</ul>
        <p class="pdp-intro">{e(p["intro"][0])}</p>
        <div id="buy-panel" class="buy-panel" data-packs='{e(packs)}' data-name="{e(name)}" data-unit="{unit}" aria-live="polite">
          <div class="skeleton"></div><div class="skeleton short"></div>
        </div>
        <ul class="promise">
          <li>{ICONS["truck"]}<span><strong>Free delivery</strong>On every order, no minimum</span></li>
          <li>{ICONS["shield"]}<span><strong>30-day guarantee</strong>Not happy? Get your money back</span></li>
        </ul>
        {accordions(key)}
        <p class="footnote">{e(C.CLAIMS_NOTE)}</p>
      </div>
    </div>
  </div>
</section>
<div class="sticky-buy" id="sticky-buy" hidden>
  <div class="wrap sticky-inner">
    <img src="{img(p["image"], 96, 96)}" alt="" width="48" height="48">
    <div class="sticky-name"><strong>{e(name)}</strong><span data-sticky-note></span></div>
    <span class="sticky-price" data-sticky-price></span>
    <button type="button" class="btn" data-sticky-add>Add to basket</button>
  </div>
</div>'''


def product_page(key):
    p = C.PRODUCTS[key]
    parts = [buy_section(key)]
    name = p.get("short", p["name"])

    if key in C.BUNDLES:
        items = "".join(f'''<li data-acc="{C.PRODUCTS[k]["acc"]}"><img src="{img(C.PRODUCTS[k]["image"], 128, 128)}" alt="" width="64" height="64" loading="lazy"><div><strong><a class="textlink" href="/{C.PRODUCTS[k]["file"]}">{e(C.PRODUCTS[k]["name"])}</a></strong><span>{e(p["includes_notes"][k])}</span></div></li>''' for k in p["includes"])
        parts.append(f'''<section class="alt">
  <div class="wrap why-grid">
    <div class="reveal"><span class="eyebrow">What's in the bundle</span><h2>Three products in one order</h2><div class="prose" style="margin-top:16px">{"".join(f"<p>{e(t)}</p>" for t in p["intro"])}</div></div>
    <ul class="bundle-list reveal">{items}</ul>
  </div>
</section>''')
    elif not p.get("simple"):
        parts.append(f'''<section data-acc="{p["acc"]}">
  <div class="wrap">
    <figure class="note reveal">
      <span class="eyebrow">A note from Hazel</span>
      <blockquote><p>“{e(p["note"])}”</p></blockquote>
      <figcaption class="sig">Hazel Hayden, Consultant Nurse and founder</figcaption>
    </figure>
  </div>
</section>''')
        ings = "".join(f'<article class="ingredient reveal"><h3>{e(n)}</h3><p class="role">{e(r)}</p><ul>{"".join(f"<li>{e(c)}</li>" for c in cl)}</ul></article>' for n, r, cl in p["ingredients"])
        parts.append(f'''<section class="alt" id="formula" data-acc="{p["acc"]}">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Ingredients</span><h2>What's inside {e(name)}</h2><p class="lead">{e(p["formula_intro"])}</p></div>
    <div class="formula-grid">{ings}</div>
    <p class="footnote">{e(C.CLAIMS_NOTE)}</p>
  </div>
</section>''')

    parts.append(why_subscribe())

    if p.get("review"):
        txt, by = p["review"]
        parts.append(f'''<section class="quote-band">
  <div class="wrap reveal">{stars()}<blockquote><p>“{e(txt)}”</p></blockquote><p class="review-by">{e(by)}</p>
  <p style="margin-top:22px"><a class="textlink arrow" href="https://www.trustpilot.com/review/www.menopausebyhazel.com" target="_blank" rel="noopener">Read our Trustpilot reviews</a></p></div>
</section>''')

    rel = "\n".join(product_card(k) for k in p["related"])
    parts.append(f'''<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Also in the range</span><h2>Works well with</h2></div>
    <div class="product-grid">{rel}</div>
  </div>
</section>''')

    if p.get("blog"):
        post = next((x for x in json.loads((ROOT / "data" / C.POSTS_FILE).read_text()) if x["slug"] == p["blog"]), None)
        if post:
            parts.append(f'''<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">From the journal</span><h2>Read more about {e(name)}</h2></div>
    <a class="post-feature reveal" href="/post.html?slug={post["slug"]}" style="margin:0"><img src="{img(post["image"], 900, 560)}" alt="" width="900" height="560" loading="lazy"><div><span class="post-meta">{fmt_date(post["date"])} · {post["minutes"]} min read</span><h3 style="font-size:1.6rem">{e(post["title"])}</h3><p class="hint">{e(post["excerpt"])}</p><span class="card-cta">Read the article</span></div></a>
  </div>
</section>''')

    faqs = faqs_for(key)
    ld = [{
        "@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["description"],
        "image": [img(g, 1200, 1200) for g in p["gallery"]], "brand": {"@type": "Brand", "name": "Supplements by Hazel"},
        "url": f'{SITE}/{p["file"]}', "manufacturer": {"@id": f"{SITE}/#org"},
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Shop", "item": f"{SITE}/shop.html"},
            {"@type": "ListItem", "position": 3, "name": p["name"], "item": f'{SITE}/{p["file"]}'}]
    }, {
        "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faqs]
    }]
    meta = {"path": p["file"], "title": p["title"], "description": p["description"], "nav": "shop",
            "image": img(p["image"], 1200, 1200), "og_type": "product", "ld": ld, "scripts": []}
    return page(meta, "\n\n".join(parts))


def why_subscribe():
    return f'''<section class="why-sub">
  <div class="wrap">
    <div class="section-head reveal" style="display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:16px;max-width:none">
      <div style="max-width:620px"><span class="eyebrow">Subscribe &amp; save</span><h2>Why subscribe?</h2><p class="lead">Your supplements arrive when you need them, for less.</p></div>
      <a class="btn" href="/shop.html">Find your formula</a>
    </div>
    <ul class="sub-tiles">
      <li class="reveal"><span class="big">5%<small>off</small></span><strong>Off every delivery</strong><span>On top of the 10% and 15% multi-buy savings</span></li>
      <li class="reveal">{ICONS["calendar"]}<strong>Free delivery</strong><span>Monthly, every 3 months or every 6 months</span></li>
      <li class="reveal">{ICONS["repeat"]}<strong>No minimum term</strong><span>Change or cancel by email or phone</span></li>
      <li class="reveal">{ICONS["gift"]}<strong>Free gift with bundles</strong><span>Your first bundle order comes with a free supplement</span></li>
    </ul>
  </div>
</section>'''


def shop_page():
    f = fragments()
    chips = '<a class="chip" href="/shop.html#products" data-goal="">All</a>' + "".join(
        f'<a class="chip" href="/shop.html?goal={k}#products" data-goal="{k}">{e(label)}</a>' for k, label, _ in C.GOALS)
    body = f'''<section class="page-head">
  <div class="wrap">
    <nav class="crumb" aria-label="Breadcrumb" style="padding-top:0;margin-bottom:22px"><a href="/">Home</a><span aria-hidden="true">/</span>Shop</nav>
    <h1>Shop the range</h1>
    <p class="lead">Every formula is made in the UK to Hazel Hayden\'s recipe. Save 10% on 3 tubs and 15% on 6, plus 5% when you subscribe. Delivery is free.</p>
    <div class="actions" style="margin-top:22px"><a class="btn line" href="/quiz.html">{ICONS["quiz"]} Not sure? Take the quiz</a></div>
  </div>
</section>
<section id="goals" class="goal-band">
  <div class="wrap">
    <h2>Shop by health goal</h2>
    <ul class="goal-tiles">{f["goal_tiles"]}</ul>
  </div>
</section>
<section id="products" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="chips" role="navigation" aria-label="Filter by health goal">{chips}</div>
    <p class="hint" data-goal-note hidden></p>
    <div class="product-grid" data-filterable>{f["products_singles"]}
{f["products_bundles"]}
{f["products_extras"]}</div>
  </div>
</section>
{why_subscribe()}'''
    items = [C.PRODUCTS[k] for k in C.SINGLES + C.BUNDLES + C.EXTRAS]
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f'{SITE}/{p["file"]}', "name": p["name"]} for i, p in enumerate(items)]}]
    meta = {"path": "shop.html", "title": "Shop | Supplements by Hazel", "nav": "shop", "ld": ld,
            "description": "Shop Clarity, Peri, Rosy and Hair & Skin, plus the Wellbeing and Hormone Health bundles, by life stage or health goal. Formulated by Hazel Hayden, made in the UK."}
    return page(meta, body)


# ---------- src pages ----------

META_RE = re.compile(r"^\s*<!--meta\s*(\{.*?\})\s*-->", re.S)


def src_page(path):
    raw = path.read_text()
    m = META_RE.match(raw)
    if not m:
        raise SystemExit(f"{path.name}: missing <!--meta {{...}} --> header")
    meta = json.loads(m.group(1))
    meta.setdefault("path", path.name)
    body = raw[m.end():]
    frags = fragments()
    body = re.sub(r"\{\{(\w+)\}\}", lambda x: frags[x.group(1)] if x.group(1) in frags else x.group(0), body)
    left = re.findall(r"\{\{\w+\}\}", body)
    if left:
        raise SystemExit(f"{path.name}: unknown placeholders {left}")
    return meta, page(meta, body)


# Old Wix URLs -> new pages (wired as 301s when the site is deployed).
REDIRECTS = {
    "/shop-all": "/shop.html", "/clarity": "/clarity.html", "/product-page/clarity": "/clarity.html",
    "/peri": "/peri.html", "/rosy": "/rosy.html", "/hair-skin": "/hair-skin.html",
    "/perform-for-men": "https://www.performformen.co.uk/", "/perform.html": "https://www.performformen.co.uk/", "/peri-bundle": "/wellbeing-bundle.html",
    "/hormone-health-support": "/hormone-health-bundle.html", "/abouthazel": "/about.html",
    "/meet-hazel": "/about.html#hazel", "/meet-the-team": "/about.html#team", "/blog": "/blog.html",
    "/faqs": "/help.html", "/contact": "/help.html#contact", "/terms": "/terms.html",
    "/post/:slug": "/post.html?slug=:slug", "/product-page/:slug": "/shop.html",
}


def main():
    written = []
    for f in sorted((ROOT / "src" / "pages").glob("*.html")):
        meta, out = src_page(f)
        (PUBLIC / meta["path"]).write_text(out)
        written.append(meta)
    (PUBLIC / "shop.html").write_text(shop_page())
    written.append({"path": "shop.html"})
    for k in C.PRODUCTS:
        (PUBLIC / C.PRODUCTS[k]["file"]).write_text(product_page(k))
        written.append({"path": C.PRODUCTS[k]["file"]})

    urls = [m["path"] for m in written if not m.get("noindex")]
    prio = {"index.html": "1.0", "shop.html": "0.9"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(urls, key=lambda x: (x != "index.html", x)):
        loc = f"{SITE}/" if u == "index.html" else f"{SITE}/{u}"
        p = prio.get(u, "0.8" if u in [C.PRODUCTS[k]["file"] for k in C.PRODUCTS] else "0.5")
        sm.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>")
    for post in json.loads((ROOT / "data" / C.POSTS_FILE).read_text()):
        sm.append(f'  <url><loc>{SITE}/post.html?slug={post["slug"]}</loc><lastmod>{post["date"]}</lastmod><priority>0.5</priority></url>')
    sm.append("</urlset>")
    (PUBLIC / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /account.html\nDisallow: /thank-you.html\n\nSitemap: {SITE}/sitemap.xml\n")
    (ROOT / "redirects.json").write_text(json.dumps(REDIRECTS, indent=2) + "\n")
    print(f"built {len(written)} pages into {PUBLIC.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
