#!/usr/bin/env python3
"""Site prototype builder (called by tools/build_pages.py).
Mirrors the WordPress plan: shared template parts (head, header, footer) + one template per page.
Writes site/*.html from design/data/menu.json. Paths are rewritten for GitHub Pages by build_pages.py.
"""
import json, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
os.makedirs(SITE, exist_ok=True)
data = json.load(open(os.path.join(ROOT, "design", "data", "menu.json")))
MENU, ORDER = data["menu"], data["order"]
TOAST_GIFT = "https://www.toasttab.com/osharesushibar/giftcards"
MAPS = "https://www.google.com/maps/search/?api=1&query=Oshare+Sushi+%2B+Bar%2C+350+Market+Street%2C+Lowell%2C+MA+01852"
DIRS = "https://www.google.com/maps/dir/?api=1&destination=350+Market+Street%2C+Lowell%2C+MA+01852"
PHONE, PHONE_TEL = "(978) 677-2636", "+19786772636"
e = html.escape

def item_url(it):
    return ORDER + "/" + it["id"] if it.get("id") else ORDER

ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M7 17 17 7M9 7h8v8"/></symbol>
<symbol id="i-bag" viewBox="0 0 24 24"><path d="M5 8h14l-1.2 12H6.2L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1Z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h10"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></symbol>
<symbol id="i-gift" viewBox="0 0 24 24"><path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13"/><path d="M12 7c-1.5-3-5-3.5-5-1.5S10 7 12 7Zm0 0c1.5-3 5-3.5 5-1.5S14 7 12 7Z"/></symbol>
<symbol id="i-car" viewBox="0 0 24 24"><path d="M5 16V11l2-5h10l2 5v5M3.5 16h17M7 19v-3m10 3v-3"/><circle cx="8" cy="13" r=".6"/><circle cx="16" cy="13" r=".6"/></symbol>
<symbol id="i-glass" viewBox="0 0 24 24"><path d="M5 4h14l-7 8-7-8ZM12 12v7M8 20h8"/></symbol>
<symbol id="i-chili" viewBox="0 0 24 24"><path fill="currentColor" stroke="none" d="M14.6 7.2c2.6.2 4.6 2.5 4 5.4-.9 4.7-6.6 8.4-12.8 8.4-.9 0-1.1-1.2-.3-1.5 3.9-1.6 6-4.2 6.6-7.4.4-2.6 1.1-4.8 2.5-4.9ZM15.4 6.3c.1-1.7 1.1-3 2.6-3.4.5-.1.8.5.4.8-.9.7-1.4 1.6-1.5 2.8-.5-.2-1-.2-1.5-.2Z"/></symbol>
</svg>"""

def ico(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

def hot_mark(n):
    if not n: return ""
    label = "Very spicy" if n > 1 else "Spicy"
    return f'<span class="mark mark--hot" role="img" aria-label="{label}">' + "".join(f'<svg aria-hidden="true"><use href="#i-chili"/></svg>' for _ in range(n)) + "</span>"

def raw_mark(r):
    return '<span class="mark mark--raw" title="Served raw or undercooked">RAW<span class="sr-only"> — served raw or undercooked</span></span>' if r else ""

HOURS_ROWS = [("Sunday", 0, "11:30 AM – 9 PM"), ("Monday", 1, "Closed"), ("Tuesday", 2, "4 – 9 PM"), ("Wednesday", 3, "4 – 9 PM"),
              ("Thursday", 4, "4 – 9 PM"), ("Friday", 5, "11:30 AM – 10 PM"), ("Saturday", 6, "11:30 AM – 10 PM")]

LD_RESTAURANT = {
    "@context": "https://schema.org", "@type": "Restaurant", "@id": "https://osharesushi.com/#restaurant",
    "name": "Oshare Sushi + Bar", "url": "https://osharesushi.com/", "telephone": "+1-978-677-2636",
    "image": "https://osharesushi.com/img/spread.jpg", "logo": "https://osharesushi.com/assets/lockup-color.svg",
    "servesCuisine": ["Sushi", "Japanese", "Korean"], "priceRange": "$$", "acceptsReservations": False,
    "hasMenu": "https://osharesushi.com/menu/",
    "address": {"@type": "PostalAddress", "streetAddress": "350 Market Street", "addressLocality": "Lowell", "addressRegion": "MA", "postalCode": "01852", "addressCountry": "US"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "16:00", "closes": "21:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday", "Saturday"], "opens": "11:30", "closes": "22:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "11:30", "closes": "21:00"}],
    "potentialAction": {"@type": "OrderAction", "target": ORDER, "deliveryMethod": ["http://purl.org/goodrelations/v1#DeliveryModePickUp", "http://purl.org/goodrelations/v1#DeliveryModeOwnFleet"]},
}

NAV = [("./", "Home", "home"), ("menu.html", "Menu", "menu"), ("story.html", "Our story", "story"), ("gallery.html", "Gallery", "gallery"), ("visit.html", "Visit", "visit")]

def head(title, desc, path, extra_ld=None):
    lds = [LD_RESTAURANT] + ([extra_ld] if extra_ld else [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, separators=(",", ":"))}</script>' for x in lds)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="https://osharesushi.com/{path}">
<meta property="og:type" content="restaurant">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://osharesushi.com/img/spread.jpg">
<meta name="theme-color" content="#1F3F80">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@500;700;800&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/oshare.css">
{ld}
</head>
<body>
{ICONS}
<a class="skip" href="#main">Skip to content</a>"""

def header(cur):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k == cur else ""}>{t}</a>' for h, t, k in NAV if k != "home")
    return f"""<header class="hdr" data-open="false">
  <div class="wrap hdr__in">
    <a class="brand" href="./" aria-label="Oshare Sushi + Bar, home"><span class="enso" aria-hidden="true"></span><span class="wordmark" aria-hidden="true"></span></a>
    <nav class="nav" id="site-nav" aria-label="Main">{links}</nav>
    <div class="hdr__act">
      <span class="status" data-status><span class="status__dot" aria-hidden="true"></span><span><b>Hours</b> <span data-status-detail></span></span></span>
      <a class="btn btn--sm" href="{ORDER}" rel="noopener" target="_blank">{ico("bag")}<span class="long">Order pickup</span><span class="short">Order</span></a>
      <button class="menu-btn" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu">{ico("menu")}</button>
    </div>
  </div>
</header>"""

def footer():
    return f"""<footer class="ftr field on-cobalt">
  <div class="wrap">
    <div class="ftr__top">
      <div class="ftr__mark"><span class="enso" aria-hidden="true"></span><div><span class="wordmark" role="img" aria-label="Oshare Sushi + Bar"></span><p class="muted" style="margin-top:.9rem;max-width:30ch">350 Market Street, Lowell, MA 01852<br><span class="tnum">{PHONE}</span></p></div></div>
      <div class="ftr__cols">
        <div><h2>Eat</h2><ul><li><a href="{ORDER}" target="_blank" rel="noopener">Order pickup or delivery</a></li><li><a href="menu.html">Full menu</a></li><li><a href="menu.html#lunch">Lunch</a></li><li><a href="{TOAST_GIFT}" target="_blank" rel="noopener">Gift cards</a></li></ul></div>
        <div><h2>Visit</h2><ul><li><a href="visit.html">Hours &amp; directions</a></li><li><a href="{DIRS}" target="_blank" rel="noopener">Get directions</a></li><li><a href="story.html">Our story</a></li><li><a href="gallery.html">Gallery</a></li></ul></div>
        <div><h2>Follow</h2><ul><li><a href="https://www.instagram.com/osharesushibar/" target="_blank" rel="noopener">Instagram</a> <span class="note">Confirm handle</span></li><li><a href="https://www.facebook.com/OshareSushiBar/" target="_blank" rel="noopener">Facebook</a> <span class="note">Confirm page</span></li><li>#OshareSushiBar</li></ul></div>
      </div>
    </div>
    <hr class="rim" style="margin-top:3rem">
    <div class="ftr__base">
      <span>© 2026 Oshare Sushi + Bar · Menu, prices and availability from our Toast ordering menu.</span>
      <span>Design prototype by jeremyanderson.tech · <button type="button" data-notes-toggle aria-pressed="true">Hide pitch notes</button></span>
    </div>
  </div>
</footer>
<nav class="orderbar" aria-label="Quick actions">
  <a href="{ORDER}" target="_blank" rel="noopener">{ico("bag")}Order pickup</a>
  <a href="tel:{PHONE_TEL}">{ico("phone")}Call</a>
  <a href="{DIRS}" target="_blank" rel="noopener">{ico("pin")}Directions</a>
</nav>
<script src="assets/oshare.js"></script>
</body>
</html>"""

def hours_list():
    return "".join(f'<span data-day="{d}">{n[:3]} {h}</span>' for n, d, h in HOURS_ROWS)

def hours_table():
    rows = "".join(f'<tr data-day="{d}"><th scope="row">{n}</th><td>{h}</td></tr>' for n, d, h in HOURS_ROWS)
    return f'<table class="hours"><caption class="sr-only">Opening hours</caption><tbody>{rows}</tbody></table>'

def find(name):
    for s in MENU:
        for it in s["items"]:
            if it["n"] == name: return it
    raise KeyError(name)

def money(p):
    return f"${p:.2f}".replace(".00", "") if p >= 1 else f"${p:.2f}"

def write(name, body):
    open(os.path.join(SITE, name), "w").write(body)
    print("wrote", name, len(body))

# ------------------------------------------------------------------ HOME
def plate(name, img, cls, alt):
    it = find(name)
    return f"""<article class="plate {cls}">
  <div class="plate__img"><img src="img/{img}.jpg" alt="{e(alt)}" loading="lazy" width="720" height="576"><span class="enso plate__ring" aria-hidden="true"></span></div>
  <div class="plate__row"><h3>{e(it['n'])}</h3><span class="price">{money(it['p'])}</span></div>
  <p>{e(it['d'])} {raw_mark(it.get('raw'))} {hot_mark(it.get('spicy'))}</p>
  <a class="link-arrow" href="{item_url(it)}" target="_blank" rel="noopener">Add to pickup order{ico('arrow')}</a>
</article>"""

def named(name, why):
    it = find(name)
    return f"""<article><h3>{e(it['n'])}</h3><span class="price">{money(it['p'])}</span><p>{e(it['d'])}</p><p class="why">{why}</p><a class="link-arrow" href="{item_url(it)}" target="_blank" rel="noopener">Order {e(it['n'])}{ico('arrow')}</a></article>"""

def counter_list(names):
    return "".join(f'<li><span>{e(n)}</span><span>{money(find(n)["p"])}</span></li>' for n in names)

home = head("Oshare Sushi + Bar | Sushi, Maki & Cocktails on Market Street, Lowell MA",
            "Specialty maki, nigiri, sashimi and a Korean-leaning kitchen from Chefs Bryan and Son at 350 Market Street in downtown Lowell, MA. Order pickup or delivery online.", "") + header("home") + f"""
<main id="main">
  <section class="hero field" aria-labelledby="hero-h">
    <div class="hero__copy">
      <h1 id="hero-h"><span class="nowrap">Dressed-up</span> sushi on <em class="nowrap">Market Street.</em></h1>
      <p class="hero__lead">Specialty maki, nigiri and a Korean-leaning kitchen from Chefs Bryan and Son, in downtown Lowell.</p>
      <div class="hero__cta">
        <a class="btn" href="{ORDER}" target="_blank" rel="noopener">{ico('bag')}Order pickup</a>
        <a class="btn btn--ghost" href="menu.html">See the menu</a>
      </div>
      <div class="hero__meta">
        <span class="status" data-status><span class="status__dot" aria-hidden="true"></span><span><b>Hours</b> · <span data-status-detail></span></span></span>
        <span>350 Market St, Lowell</span>
      </div>
    </div>
    <figure class="hero__photo">
      <img src="img/night.jpg" alt="Overhead view of Oshare's table: nigiri and a salmon roll on a red-rimmed lacquer tray, surrounded by blue-and-white porcelain bowls of salmon, katsu, spicy chicken and edamame on dark wood" width="1372" height="984" fetchpriority="high">
      <span class="enso paint" aria-hidden="true"></span>
      <figcaption>Nigiri Deluxe, center</figcaption>
    </figure>
  </section>

  <section class="tonight" aria-label="Today">
    <div class="wrap tonight__in">
      <p class="tonight__state status" data-status><span class="status__dot" aria-hidden="true"></span><span><b>Hours</b> <span class="muted" data-status-detail style="font-family:var(--sans);font-size:var(--fs-sm);font-weight:400"></span></span></p>
      <div class="tonight__hours tnum">{hours_list()}</div>
      <div class="tonight__acts"><a class="btn btn--sm" href="{ORDER}" target="_blank" rel="noopener">{ico('bag')}Order pickup</a><a class="btn btn--sm btn--ghost" href="{DIRS}" target="_blank" rel="noopener">{ico('pin')}Directions</a></div>
    </div>
  </section>

  <section class="sec field" aria-labelledby="named-h">
    <div class="wrap">
      <div class="sec-head"><h2 id="named-h">Three rolls named for home.</h2><p>Some of our specialty maki carry Lowell's own names. Start here.</p></div>
      <div class="named">
        {named("The Acre", 'The Acre is Lowell\'s historic immigrant neighborhood, just outside downtown. <span class="note">Confirm the chefs\' naming story</span>')}
        {named("Red Sox Maki", 'For game nights. Green apple and honey aioli keep it bright.')}
        {named("Celtic Roll Maki", 'The Acre was home to Lowell\'s first Irish community. Smoked salmon, apple and cream cheese inside. <span class="note">Confirm intent</span>')}
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="plates-h">
    <div class="wrap">
      <div class="sec-head sec-head--split"><div style="display:grid;gap:1rem"><h2 id="plates-h">On the table tonight.</h2><p>Every photo here is a real plate from our kitchen. Tap one to add it to a pickup order.</p></div><a class="btn btn--ghost" href="menu.html">Full menu, {sum(len(s['items']) for s in MENU)} dishes</a></div>
      <div class="plates">
        {plate("Lobster Rangoon Maki", "lobster", "plate--wide", "Lobster Rangoon Maki: eight pieces topped with crispy wontons, avocado and plum sauce on a white plate")}
        {plate("Tuna Crispy Rice", "crispyRice", "", "Three pieces of tuna crispy rice with yuzu guacamole and pickled red onion")}
        {plate("Firebender Maki", "firebender", "", "Firebender Maki with spicy tuna, salmon and ghost pepper sate on a white plate")}
        {plate("Santaka Beef Noodle", "santaka", "", "Santaka Beef Noodle with spicy bulgogi beef in a blue-and-white porcelain bowl")}
        {plate("Fried Chicken Bao", "bao", "", "Two fried chicken bao with spicy slaw and pickled red onion")}
      </div>
    </div>
  </section>

  <section class="counters" aria-label="The sushi bar and the kitchen">
    <div class="counter">
      <figure><img src="img/tray.jpg" alt="Nigiri Deluxe on a red-rimmed black lacquer tray: ten nigiri and a spicy salmon roll on marble" loading="lazy" width="1600" height="1280"></figure>
      <div class="counter__body"><h3>The sushi bar</h3><p class="muted">Nigiri, sashimi and sets cut to order.</p><ul class="tnum">{counter_list(["Nigiri Deluxe", "Sashimi Deluxe", "Salmon Lover Set", "Party of 2"])}</ul><a class="link-arrow" href="menu.html#sets">All sushi sets{ico('arrow')}</a></div>
    </div>
    <div class="counter field">
      <figure><img src="img/udon.jpg" alt="Stir-fried noodles with shrimp, carrots and scallions in a blue-and-white porcelain bowl" loading="lazy" width="1600" height="1280"></figure>
      <div class="counter__body"><h3>The kitchen</h3><p class="muted">Noodles, bao and rice plates with Korean heat.</p><ul class="tnum">{counter_list(["Santaka Beef Noodle", "Spicy Beef Bao", "Chicken Karaage", "Kogi Beef Rice Bowl"])}</ul><a class="link-arrow" href="menu.html#noodles">Noodles &amp; udon{ico('arrow')}</a></div>
    </div>
  </section>

  <section class="sec" aria-labelledby="chefs-h">
    <div class="wrap chefs">
      <div style="display:grid;gap:1.5rem">
        <h2 id="chefs-h" class="sr-only">Our chefs</h2>
        <blockquote>Chefs Bryan and Son bring <span>more than 30 years</span> of combined experience to every roll and every noodle bowl.</blockquote>
        <p class="muted" style="max-width:52ch">Sushi and Asian cuisine made with care and precision, from the sushi bar to the wok. <span class="note">Chef portraits + interview needed for full bios</span></p>
        <a class="link-arrow" href="story.html">Read our story{ico('arrow')}</a>
      </div>
      <figure style="margin:0"><img src="img/spread.jpg" alt="A full Oshare spread on marble: bulgogi beef, shrimp noodles, a rice bowl with fried egg, edamame and crispy rice in blue-and-white porcelain" loading="lazy" width="1600" height="1280"></figure>
    </div>
  </section>

  <section class="sec sec--tight field field--band" aria-labelledby="bar-h">
    <div class="wrap barstack" style="display:grid;gap:2rem;align-items:center">
      <p aria-hidden="true" style="font-family:var(--display);font-weight:800;font-size:clamp(5rem,3rem + 10vw,12rem);line-height:.85;letter-spacing:-.04em;color:var(--on-cobalt)"><span style="color:var(--enso)">+</span>BAR</p>
      <div style="display:grid;gap:1.25rem">
        <h2 id="bar-h" style="font-size:var(--fs-h2)">A full bar and counter seats.</h2>
        <p class="muted" style="font-size:var(--fs-lead)">Come in for a solo dinner at the counter or a first round with friends before the show. <span class="note">Cocktail list + bar photography needed</span></p>
        <div><a class="btn btn--ghost" href="visit.html">Plan a visit</a></div>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="ratings-h">
    <div class="wrap">
      <div class="sec-head"><h2 id="ratings-h">What Lowell is saying.</h2><p>Guests keep coming back to the fish quality, the presentation and the people serving it.</p></div>
      <div class="ratings">
        <div class="rating"><span class="rating__n tnum">4.8<small> / 5</small></span><span class="rating__src">Restaurantji · 68 ratings</span></div>
        <div class="rating"><span class="rating__n tnum">4.8<small> / 5</small></span><span class="rating__src">OpenTable · 10 reviews</span></div>
        <div class="rating"><span class="rating__n tnum">4.9<small> / 5</small></span><span class="rating__src">Uber Eats · 27 ratings</span></div>
      </div>
      <p class="muted" style="font-size:var(--fs-xs);margin-top:1rem">Ratings as listed on each platform, October 8, 2026. <span class="note">Swap in Google rating once the Business Profile is confirmed. No review markup.</span></p>
    </div>
  </section>

  <section class="sec field" aria-labelledby="visit-h">
    <div class="wrap visit">
      <div style="display:grid;gap:1.5rem;align-content:start">
        <h2 id="visit-h" style="font-size:var(--fs-h2)">Find us on Market Street.</h2>
        <p class="addr">350 Market Street<br>Lowell, MA 01852</p>
        <div class="facts">
          <div class="fact">{ico('phone')}<div><span class="tnum">{PHONE}</span> <button class="chip" style="color:var(--on-cobalt);border-color:var(--on-cobalt-2)" type="button" data-copy="{PHONE}">Copy</button><br><span class="muted">No online reservations. Call us or walk in.</span></div></div>
          <div class="fact">{ico('car')}<div>Parking nearby <span class="note">Lot vs. street: listings disagree, confirm</span></div></div>
        </div>
        <div class="hero__cta"><a class="btn" href="{DIRS}" target="_blank" rel="noopener">{ico('pin')}Get directions</a><a class="btn btn--ghost" href="visit.html">Visiting details</a></div>
      </div>
      <div>{hours_table()}</div>
    </div>
  </section>
</main>
""" + footer()
write("index.html", home)

# ------------------------------------------------------------------ MENU
def menu_item(it):
    img = it.get("img")
    text = (it["n"] + " " + it.get("d", "")).lower()
    cls = "mitem mitem--photo" if img else "mitem"
    pic = f'<img class="mitem__img" src="img/{img}.jpg" alt="" loading="lazy" width="720" height="576">' if img else ""
    marks = raw_mark(it.get("raw")) + hot_mark(it.get("spicy"))
    oos = '<span class="oos">Sold out today</span>' if it.get("oos") else ""
    act = (f'<div class="mitem__act"><a href="{item_url(it)}" target="_blank" rel="noopener">Add to order{ico("arrow")}</a>{oos}</div>'
           if it.get("id") else f'<div class="mitem__act"><a href="{ORDER}" target="_blank" rel="noopener">Order online{ico("arrow")}</a>{oos}</div>')
    desc = f'<p class="mitem__desc">{e(it["d"])}</p>' if it.get("d") else ""
    return f"""<li class="{cls}" data-text="{e(text)}" data-raw="{str(bool(it.get('raw'))).lower()}" data-hot="{it.get('spicy', 0)}" data-oos="{str(bool(it.get('oos'))).lower()}">{pic}<h3>{e(it['n'])} {marks}</h3><span class="mitem__price">{money(it['p'])}</span>{desc}{act}</li>"""

def menu_ld():
    return {"@context": "https://schema.org", "@type": "Menu", "name": "Oshare Sushi + Bar menu", "url": "https://osharesushi.com/menu/", "inLanguage": "en",
            "hasMenuSection": [{"@type": "MenuSection", "name": s["title"], "hasMenuItem": [
                {"@type": "MenuItem", "name": it["n"], **({"description": it["d"]} if it.get("d") else {}),
                 "offers": {"@type": "Offer", "price": f"{it['p']:.2f}", "priceCurrency": "USD"}} for it in s["items"]]} for s in MENU]}

cats_nav = "".join(f'<a href="#{s["key"]}">{e(s["title"])}</a>' for s in MENU) + '<a href="#bar">Bar</a>'
sections = []
for s in MENU:
    note = f'<p>{e(s["note"])}</p>' if s.get("note") else "<p></p>"
    extra = ""
    if s["key"] == "nigiri":
        extra = """<div class="sushi-guide"><div><b>Nigiri</b><p>Two pieces of sliced fish over sushi rice, with wasabi.</p></div><div><b>Sashimi</b><p>Three to four slices, fish only. Add $2 to any nigiri order.</p></div><div><b>Hand roll</b><p>One cone-shaped roll. Add $1.50 to any classic maki.</p></div></div>"""
    if s["key"] == "lunch":
        note = '<p>Lunch combos as published on our menu. <span class="note">Confirm lunch days + hours</span></p>'
    sections.append(f"""<section class="mcat" id="{s['key']}" aria-labelledby="h-{s['key']}">
  <div class="mcat__head"><h2 id="h-{s['key']}">{e(s['title'])}</h2>{note}</div>
  <hr class="rim">
  <ul class="mlist" role="list">{''.join(menu_item(it) for it in s['items'])}</ul>{extra}
</section>""")
sections.append("""<section class="mcat" id="bar" aria-labelledby="h-bar">
  <div class="mcat__head"><h2 id="h-bar">Bar</h2><p>A full bar with cocktails. Ask your server for tonight's list.</p></div>
  <hr class="rim">
  <p class="mempty">The drinks list goes here once the bar team shares it. <span class="note">Cocktail, beer, sake + wine list needed from client</span></p>
</section>""")

menu = head("Menu | Oshare Sushi + Bar, Lowell MA — Specialty Maki, Nigiri, Noodles",
            "The full Oshare Sushi + Bar menu with prices: specialty maki like The Acre and Lobster Rangoon, nigiri and sashimi, sushi sets, Santaka noodles, udon, bao and lunch. Order pickup online.",
            "menu/", menu_ld()) + header("menu") + f"""
<main id="main">
  <section class="phead field" aria-labelledby="menu-h">
    <span class="enso paint" aria-hidden="true"></span>
    <div class="wrap phead__in"><h1 id="menu-h">The menu</h1><p>Every roll, plate and price from our ordering menu. Tap a dish to add it to a pickup order. <span class="note">Captured from Toast Oct 8, 2026. Live site syncs automatically.</span></p></div>
  </section>
  <div class="mtools" data-filters="closed">
    <div class="wrap mtools__in">
      <nav class="cats" aria-label="Menu sections">{cats_nav}</nav>
      <button class="ftoggle" type="button" aria-expanded="false" aria-controls="menu-filters">{ico('search')}<span>Search &amp; filter</span><span class="ftoggle__dot" hidden></span></button>
      <div class="filters" id="menu-filters" role="group" aria-label="Filter dishes">
        <label class="search"><span class="sr-only">Search the menu</span>{ico('search')}<input id="menu-search" type="search" placeholder="Search dishes" autocomplete="off"></label>
        <button class="chip" id="f-noraw" type="button" aria-pressed="false">No raw fish</button>
        <button class="chip" id="f-hot" type="button" aria-pressed="false"><span class="mark mark--hot" aria-hidden="true"><svg><use href="#i-chili"/></svg></span>Spicy</button>
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="legend"><span><span class="mark mark--raw" aria-hidden="true">RAW</span> Served raw or undercooked</span><span>{hot_mark(1)} Spicy</span><span>{hot_mark(2)} Very spicy</span><span id="menu-live" role="status" aria-live="polite"></span></div>
    <p class="mempty" id="menu-empty" hidden>No dishes match. <button class="chip" type="button" id="menu-clear">Clear filters</button></p>
    {''.join(sections)}
    <p class="muted" style="font-size:var(--fs-sm);padding-block:3rem 4rem;max-width:70ch">Consuming raw or undercooked meats, poultry, seafood, shellfish or eggs may increase your risk of foodborne illness, especially if you have certain medical conditions. Before placing your order, please tell your server if anyone in your party has a food allergy. Prices and availability can change; our online ordering menu is always current. <span class="note">Confirm advisory wording with owner</span></p>
  </div>
</main>
""" + footer()
write("menu.html", menu)

# ------------------------------------------------------------------ STORY
story = head("Our Story | Oshare Sushi + Bar, Lowell MA", "Chefs Bryan and Son bring more than 30 years of combined experience to Oshare Sushi + Bar, a neighborhood sushi bar and kitchen on Market Street in downtown Lowell.", "about/") + header("story") + f"""
<main id="main">
  <section class="phead field" aria-labelledby="story-h">
    <span class="enso paint" aria-hidden="true"></span>
    <div class="wrap phead__in"><h1 id="story-h">Your neighborhood sushi spot.</h1><p>Fresh sushi, a kitchen with heat, and a room for friends and family on Market Street.</p></div>
  </section>
  <section class="sec">
    <div class="wrap story-grid">
      <div class="prose">
        <h2>Two counters, one menu.</h2>
        <p class="lede">Chefs Bryan and Son bring more than 30 years of combined experience to Oshare, cooking sushi and Asian cuisine with care and precision.</p>
        <p>At the sushi bar that means nigiri, sashimi and specialty maki like the Passion Roll, finished with dragon fruit aioli. In the kitchen it means Santaka noodles tossed in Japanese chili pepper sauce, spicy bulgogi in bao and rice bowls, and udon in chicken broth with miso tare.</p>
        <p>Everything arrives the way you see it in our photos: on blue-and-white porcelain and red-rimmed lacquer.</p>
        <p><span class="note">Opening year, how the chefs met, and family details: interview needed</span></p>
      </div>
      <figure><img src="img/tray.jpg" alt="Nigiri Deluxe on a red-rimmed lacquer tray" loading="lazy" width="1600" height="1280"></figure>
    </div>
  </section>
  <section class="sec field" aria-labelledby="lowell-h">
    <div class="wrap story-grid">
      <figure><img src="img/spread.jpg" alt="Overhead spread of Oshare dishes in blue-and-white bowls on marble" loading="lazy" width="1600" height="1280"></figure>
      <div class="prose">
        <h2 id="lowell-h">Made in Lowell.</h2>
        <p class="lede">Our menu has The Acre, the Red Sox Maki and the Celtic Roll on it for a reason: this is a Lowell restaurant.</p>
        <p>We're downtown at 350 Market Street, a short walk from the mills and canals. Come in before a show, after class, or for a long dinner at the bar.</p>
        <a class="link-arrow" href="menu.html#signature">See the signature maki{ico('arrow')}</a>
      </div>
    </div>
  </section>
  <section class="sec field field--band note-block" aria-labelledby="gaps-h">
    <div class="wrap">
      <div class="sec-head"><h2 id="gaps-h">Still to write, together.</h2><p>These parts of the story belong to the owners. The layout is ready for them. <span class="note">Pitch note: visible in prototype only</span></p></div>
      <div class="gaps">
        <div class="gap"><h3>The chefs</h3><p>Portraits at the sushi bar and wok, full names, where they trained, and a short interview.</p></div>
        <div class="gap"><h3>The name</h3><p>"Oshare" means stylish or dressed-up in Japanese. We'd love the real story behind the choice before telling it.</p></div>
        <div class="gap"><h3>The room</h3><p>Photos of the dining room, the bar and the counter at dinner service, plus the cocktail list.</p></div>
      </div>
    </div>
  </section>
</main>
""" + footer()
write("story.html", story.replace('note-block"', 'note-block" data-note-block'))

# ------------------------------------------------------------------ GALLERY
G = [("night", "The full table on dark wood: Nigiri Deluxe in the lacquer tray, katsu, salmon and edamame in porcelain"),
     ("lobster", "Lobster Rangoon Maki"), ("spread", "Bulgogi beef, shrimp noodles, a rice bowl with fried egg and crispy rice on marble"),
     ("crispyRice", "Tuna Crispy Rice"), ("santaka", "Santaka Beef Noodle"), ("tray", "Nigiri Deluxe in a red-rimmed lacquer tray"),
     ("firebender", "Firebender Maki"), ("bao", "Fried Chicken Bao"), ("udon", "Stir-fried noodles with shrimp in a blue-and-white bowl"),
     ("karaage", "Chicken Karaage with watermelon radish"), ("beefTataki", "Beef Tataki"), ("katsu", "Chicken Katsu with tonkatsu sauce and slaw"),
     ("salmon", "Lemon Butter Salmon"), ("crabSalad", "Crab Avocado Salad"), ("spicyChicken", "Spicy Chicken with fried egg"),
     ("beefTeri", "Beef Teriyaki"), ("edamame", "Spicy Edamame"), ("stirfry", "Stir-Fried Noodles")]
tiles = "".join(f'<button type="button" data-caption="{e(c)}"><img src="img/{k}.jpg" alt="{e(c)}" loading="lazy"><span>{e(c)}</span></button>' for k, c in G)
gallery = head("Gallery | Oshare Sushi + Bar, Lowell MA", "Photos of sushi, maki, noodles and plates from Oshare Sushi + Bar on Market Street in Lowell, MA.", "gallery/") + header("gallery") + f"""
<main id="main">
  <section class="phead field" aria-labelledby="gal-h">
    <span class="enso paint" aria-hidden="true"></span>
    <div class="wrap phead__in"><h1 id="gal-h">Gallery</h1><p>Real plates from our kitchen, on the porcelain they're served on. <span class="note">Dining room, bar and team photos needed</span></p></div>
  </section>
  <section class="sec"><div class="wrap"><div class="gallery">{tiles}</div></div></section>
  <dialog class="lightbox" aria-label="Photo viewer">
    <figure><img alt=""><figcaption class="lightbox__bar"><span></span><div><span data-count class="tnum" style="align-self:center;margin-right:.5rem"></span><button type="button" data-prev aria-label="Previous photo">Prev</button><button type="button" data-next aria-label="Next photo">Next</button><button type="button" data-close>Close</button></div></figcaption></figure>
  </dialog>
</main>
""" + footer()
write("gallery.html", gallery)

# ------------------------------------------------------------------ VISIT
visit = head("Hours & Directions | Oshare Sushi + Bar, 350 Market St, Lowell MA", "Oshare Sushi + Bar is at 350 Market Street, Lowell, MA 01852. Open Tuesday to Sunday. Call (978) 677-2636, order pickup or delivery online, or buy a gift card.", "visit/") + header("visit") + f"""
<main id="main">
  <section class="phead field" aria-labelledby="visit-h">
    <span class="enso paint" aria-hidden="true"></span>
    <div class="wrap phead__in"><h1 id="visit-h">Visit us</h1><p>350 Market Street in downtown Lowell. Open Tuesday through Sunday.</p></div>
  </section>
  <section class="sec">
    <div class="wrap visit">
      <div style="display:grid;gap:2rem;align-content:start">
        <div style="display:grid;gap:.75rem"><p class="addr">350 Market Street<br>Lowell, MA 01852</p><p class="status" data-status><span class="status__dot" aria-hidden="true"></span><span><b>Hours</b> · <span data-status-detail></span></span></p></div>
        {hours_table()}
        <div class="hero__cta"><a class="btn" href="{DIRS}" target="_blank" rel="noopener">{ico('pin')}Get directions</a><a class="btn btn--ghost" href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps</a></div>
      </div>
      <div style="display:grid;gap:1.5rem;align-content:start">
        <a class="mapcard" href="{MAPS}" target="_blank" rel="noopener" aria-label="Open 350 Market Street in Google Maps">
          <svg class="map" viewBox="0 0 400 300" aria-hidden="true"><g fill="none" stroke="var(--cobalt-2)" stroke-opacity=".5"><circle cx="200" cy="150" r="40"/><circle cx="200" cy="150" r="80"/><circle cx="200" cy="150" r="120" stroke-dasharray="2 6"/><circle cx="200" cy="150" r="160" stroke-dasharray="2 6"/></g><circle cx="200" cy="150" r="9" fill="var(--enso)"/><circle cx="200" cy="150" r="18" fill="none" stroke="var(--enso)" stroke-width="2"/></svg>
          <span class="mapcard__label">{ico('pin')}350 Market St · Open map</span>
        </a>
        <div class="facts">
          <div class="fact">{ico('phone')}<div><b class="tnum">{PHONE}</b> <button class="chip" type="button" data-copy="{PHONE}">Copy</button><br><span class="muted">We don't take online reservations. Call us, or walk in.</span></div></div>
          <div class="fact">{ico('bag')}<div><b>Pickup and delivery</b><br><span class="muted">Order directly through our online ordering. <a href="{ORDER}" target="_blank" rel="noopener">Start an order</a></span></div></div>
          <div class="fact">{ico('gift')}<div><b>Gift cards and rewards</b><br><span class="muted">Buy an <a href="{TOAST_GIFT}" target="_blank" rel="noopener">Oshare gift card</a>. Online orders earn rewards points with a free account.</span></div></div>
          <div class="fact">{ico('car')}<div><b>Parking</b><br><span class="muted">Street and nearby lot parking downtown.</span> <span class="note">Confirm: listings say both "street only" and "adjacent lot"</span></div></div>
          <div class="fact">{ico('glass')}<div><b>Groups and events</b><br><span class="muted">Planning something bigger? Call us to talk it through.</span> <span class="note">Private dining / catering: confirm before promoting</span></div></div>
        </div>
      </div>
    </div>
  </section>
</main>
""" + footer()
write("visit.html", visit)
