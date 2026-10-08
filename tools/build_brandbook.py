#!/usr/bin/env python3
"""Brand book builder (called by tools/build_pages.py). Writes brand-book/index.html; build_pages.py adds the document shell and concept bar."""
import json, os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape
src = open(os.path.join(ROOT, "tools", "build_site.py")).read()
ICONS = re.search(r'ICONS = """(.*?)"""', src, re.S).group(1)
data = json.load(open(os.path.join(ROOT, "design", "data", "menu.json")))
MENU, ORDER = data["menu"], data["order"]
SITE_URL = os.environ.get("SITE_URL", "")
n_items = sum(len(s["items"]) for s in MENU)

def ico(n): return f'<svg class="ico" aria-hidden="true"><use href="#i-{n}"/></svg>'
V = '<span class="tag tag--v">Verified</span>'
R = '<span class="tag tag--r">Recommendation</span>'
C = lambda t="Confirm with owner": f'<span class="tag tag--c">{t}</span>'

# ---------- contrast (computed, not asserted) ----------
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def cr(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True); return (x + .05) / (y + .05)

COLORS = [
    ("Glaze", "#F3F5F9", "Porcelain white. The page ground; slightly cool so the marble in the photos reads warm.", "#0B1A36"),
    ("Cobalt", "#1F3F80", "Underglaze cobalt, sampled from the deepest strokes on Oshare's bowls. Owns whole regions.", "#F3F5F9"),
    ("Ensō Orange", "#F25A0A", "From the logo's brush ring. The only warm note: the ring, the order button, one word.", "#0B1A36"),
    ("Ink", "#0B1A36", "Blue-black for text. Never pure black.", "#F3F5F9"),
    ("Wash", "#D9E3F2", "Diluted cobalt for quiet fills and tables.", "#0B1A36"),
    ("Cobalt Line", "#2E58A6", "Links, icons and hairlines on glaze.", "#F3F5F9"),
    ("Orange Ink", "#B5420A", "Orange when it has to be small text on glaze.", "#F3F5F9"),
    ("Orange Light", "#FF8540", "Orange when it is large text on cobalt.", "#0B1A36"),
]
def rgb(h): return ", ".join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5))
swatches = "".join(f'''<div class="swatch"><div class="swatch__chip" style="background:{h};color:{fg};{'box-shadow:inset 0 0 0 1px var(--line)' if h=='#F3F5F9' else ''}">{n}</div><div class="swatch__meta"><b>{h}</b><span>RGB {rgb(h)}</span><span>{d}</span></div></div>''' for n, h, d, fg in COLORS)
PAIRS = [("Ink on Glaze", "#0B1A36", "#F3F5F9", "Body text"), ("Glaze on Cobalt", "#F3F5F9", "#1F3F80", "Text on cobalt fields"),
         ("Cobalt on Glaze", "#1F3F80", "#F3F5F9", "Headings, data"), ("Cobalt Line on Glaze", "#2E58A6", "#F3F5F9", "Links, icons"),
         ("Ink on Ensō Orange", "#0B1A36", "#F25A0A", "Primary button label"), ("Orange Ink on Glaze", "#B5420A", "#F3F5F9", "Small orange text"),
         ("Orange Light on Cobalt", "#FF8540", "#1F3F80", "Large orange words on cobalt"), ("Ensō Orange on Cobalt", "#F25A0A", "#1F3F80", "The ring on cobalt (graphic)"),
         ("White on Ensō Orange", "#FFFFFF", "#F25A0A", "Avoid for text")]
def verdict(r):
    if r >= 7: return '<span class="pass">AAA</span>'
    if r >= 4.5: return '<span class="pass">AA</span>'
    if r >= 3: return '<span class="pass pass--lg">Large text / graphics only</span>'
    return '<span class="pass pass--lg">Fail</span>'
pairs = "".join(f'<div class="cpair"><i style="background:{bg};color:{fg}">Aa</i><div><b>{n}</b><br><span class="muted" style="font-size:.88rem">{use}</span></div><div style="text-align:right"><b class="tnum">{cr(fg,bg):.2f}:1</b><br>{verdict(cr(fg,bg))}</div></div>' for n, fg, bg, use in PAIRS)

# ---------- TOC ----------
TOC = [
    ("I", "Discovery", [("research", "1.1", "What we found"), ("conflicts", "1.2", "Conflicts & open questions"), ("market", "1.3", "Lowell's sushi landscape"), ("audit", "1.4", "Current identity audit"), ("word", "1.5", "The word oshare")]),
    ("II", "Strategy", [("positioning", "2.1", "Positioning"), ("personality", "2.2", "Promise & personality"), ("audiences", "2.3", "Audiences & personas"), ("experience", "2.4", "The guest experience"), ("mission", "2.5", "Mission & vision"), ("voice", "2.6", "Voice & tone"), ("messaging", "2.7", "Story & messaging"), ("principles", "2.8", "Brand principles")]),
    ("III", "Identity", [("directions", "3.1", "Directions explored"), ("logo", "3.2", "Logo system"), ("color", "3.3", "Color"), ("type", "3.4", "Typography"), ("graphics", "3.5", "Graphic system"), ("icons", "3.6", "Icons & marks"), ("photo", "3.7", "Photography"), ("layout", "3.8", "Layout & spacing"), ("components", "3.9", "UI components"), ("motion", "3.10", "Motion")]),
    ("IV", "Applications", [("website", "4.1", "Website"), ("social", "4.2", "Social"), ("print", "4.3", "Printed menu"), ("packaging", "4.4", "Packaging & gift card")]),
    ("V", "Build plan", [("toast", "5.1", "Toast integration"), ("seo", "5.2", "SEO & local search"), ("wordpress", "5.3", "WordPress & hosting"), ("tokens", "5.4", "Design tokens"), ("assets", "5.5", "Asset inventory"), ("checklist", "5.6", "Owner approval checklist"), ("sources", "5.7", "Sources")]),
]
toc_html = "".join(f'<li class="part">{p} · {t}</li>' + "".join(f'<li><a href="#{i}"><span>{n}</span><span>{l}</span></a></li>' for i, n, l in ch) for p, t, ch in TOC)
toc_m = "".join(f'<a href="#{i}"><span class="tnum" style="color:var(--cobalt-2)">{n}</span><span>{l}</span></a>' for p, t, ch in TOC for i, n, l in ch)
def chead(cid, title, lede=""):
    n = next(n for p, t, ch in TOC for i, n, l in ch if i == cid)
    return f'<div class="ch__head"><h2><span class="n">{n}</span>{title}</h2>{f"<p>{lede}</p>" if lede else ""}</div>'
def part(num, title, lede):
    return f'<section class="part-open field" aria-label="Part {num}: {title}"><span class="part-open__n" aria-hidden="true">{num}</span><div><h2>{title}</h2><p>{lede}</p></div></section>'

LOCKUP = lambda cls="lockup--ink": f'<div class="lockup {cls}"><span class="enso"></span><span class="wordmark"></span></div>'
def item(name):
    for s in MENU:
        for it in s["items"]:
            if it["n"] == name: return it
def m(p): return f"${p:.0f}" if p == int(p) else f"${p:.2f}"

css_tokens = """:root {
  /* color */
  --glaze: #F3F5F9;   --glaze-2: #E9EDF4;  --wash: #D9E3F2;
  --ink: #0B1A36;     --ink-2: #3E4D6B;
  --cobalt: #1F3F80;  --cobalt-2: #2E58A6; --on-cobalt: #F3F5F9; --on-cobalt-2: #B9C9EA;
  --enso: #F25A0A;    --enso-ink: #B5420A; --enso-hi: #FF8540; --on-enso: #0B1A36;
  /* type */
  --display: "Shippori Mincho B1", "Yu Mincho", Georgia, serif;
  --sans: "Zen Kaku Gothic New", "Yu Gothic", system-ui, sans-serif;
  --fs-hero: clamp(2.5rem, 1.5rem + 3.6vw, 5rem);
  --fs-h2: clamp(2rem, 1.35rem + 2.4vw, 3.6rem);
  --fs-h3: clamp(1.3rem, 1.12rem + .7vw, 1.7rem);
  --fs-body: 1.0625rem;
  /* space: 4px scale */
  --s1: .25rem; --s2: .5rem; --s3: .75rem; --s4: 1rem; --s5: 1.5rem;
  --s6: 2rem; --s7: 3rem; --s8: 4rem; --s9: 6rem; --s10: 8rem;
  --radius-pill: 999px; --ease: cubic-bezier(.16, 1, .3, 1);
}"""
theme_json = json.dumps({
    "$schema": "https://schemas.wp.org/trunk/theme.json", "version": 3,
    "settings": {
        "color": {"defaultPalette": False, "palette": [{"slug": s, "name": n, "color": c} for s, n, c in [
            ("glaze", "Glaze", "#F3F5F9"), ("ink", "Ink", "#0B1A36"), ("cobalt", "Cobalt", "#1F3F80"), ("cobalt-line", "Cobalt Line", "#2E58A6"),
            ("wash", "Wash", "#D9E3F2"), ("enso", "Ensō Orange", "#F25A0A"), ("enso-ink", "Orange Ink", "#B5420A"), ("enso-light", "Orange Light", "#FF8540")]]},
        "typography": {"fluid": True, "fontFamilies": [
            {"slug": "display", "name": "Shippori Mincho B1", "fontFamily": "\"Shippori Mincho B1\", Georgia, serif"},
            {"slug": "sans", "name": "Zen Kaku Gothic New", "fontFamily": "\"Zen Kaku Gothic New\", system-ui, sans-serif"}],
            "fontSizes": [{"slug": "h3", "size": "1.7rem", "fluid": {"min": "1.3rem", "max": "1.7rem"}}, {"slug": "h2", "size": "3.6rem", "fluid": {"min": "2rem", "max": "3.6rem"}}, {"slug": "hero", "size": "5rem", "fluid": {"min": "2.5rem", "max": "5rem"}}]},
        "spacing": {"spacingScale": {"steps": 0}, "spacingSizes": [{"slug": str(i), "name": f"s{i}", "size": v} for i, v in zip(range(1, 11), [".25rem", ".5rem", ".75rem", "1rem", "1.5rem", "2rem", "3rem", "4rem", "6rem", "8rem"])]},
        "layout": {"contentSize": "760px", "wideSize": "1320px"}},
    "styles": {"color": {"background": "var(--wp--preset--color--glaze)", "text": "var(--wp--preset--color--ink)"},
               "typography": {"fontFamily": "var(--wp--preset--font-family--sans)", "lineHeight": "1.65"},
               "elements": {"heading": {"typography": {"fontFamily": "var(--wp--preset--font-family--display)", "fontWeight": "700", "lineHeight": "1.08"}},
                            "button": {"color": {"background": "var(--wp--preset--color--enso)", "text": "var(--wp--preset--color--ink)"}, "border": {"radius": "999px"}, "typography": {"fontWeight": "700"}}}}}, indent=2, ensure_ascii=False)

site_link = (f'<a class="btn" href="{SITE_URL}" target="_blank" rel="noopener">{ico("arrow")}Open the website prototype</a>' if SITE_URL else "")

PHOTOS = [("night.jpg", "Overhead table on dark wood (hero)", "Toast Sites CDN · OshareSushiBar4.png, cropped to remove logo panel"),
          ("spread.jpg", "Overhead table on marble", "Toast Sites CDN · OshareSushiBar_hero_2880x2304"), ("tray.jpg", "Nigiri Deluxe in lacquer tray", "Toast Sites CDN · OshareSushiBar_MiginDeluxe_2880x2304"),
          ("udon.jpg", "Stir-fried noodles, porcelain bowl", "Toast menu item image (About page)")] + [
          (f"{k}.jpg", n, "Toast online ordering menu item photo, 720px") for k, n in [("lobster", "Lobster Rangoon Maki"), ("firebender", "Firebender Maki"), ("crispyRice", "Tuna Crispy Rice"),
          ("santaka", "Santaka Beef Noodle"), ("bao", "Fried Chicken Bao"), ("karaage", "Chicken Karaage"), ("katsu", "Chicken Katsu"), ("beefTataki", "Beef Tataki"),
          ("crabSalad", "Crab Avocado Salad"), ("salmon", "Lemon Butter Salmon"), ("spicyChicken", "Spicy Chicken"), ("beefTeri", "Beef Teriyaki"), ("edamame", "Spicy Edamame"), ("stirfry", "Stir-Fried Noodles")]]
asset_rows = "".join(f'<tr><td><img src="img/{f}" alt="" width="64" height="51" style="width:64px;height:51px;object-fit:cover" loading="lazy"></td><td>{e(n)}</td><td>{e(s)}</td><td>{C("License")}</td></tr>' for f, n, s in PHOTOS)

CHECK = [
    ("Brand", [("c-dir", "Approve the Blue & White direction (cobalt, glaze, ensō orange)"), ("c-logo", "Approve the refined vector logo and supply original logo files"), ("c-tag", "Pick a line: “Dressed-up sushi on Market Street.” or an alternate"), ("c-name", "Tell us the story behind the name Oshare (or keep it untold)")]),
    ("Facts", [("c-hours", "Confirm hours (site: Sun 11:30–9, Mon closed, Tue–Thu 4–9, Fri–Sat 11:30–10)"), ("c-lunch", "Confirm lunch days and lunch hours"), ("c-res", "Confirm reservations: phone only, or add a booking tool"), ("c-park", "Confirm parking: street, adjacent lot, or both"), ("c-chefs", "Approve chef names, bios and photos for Bryan and Son"), ("c-acre", "Confirm the naming stories for The Acre, Red Sox and Celtic rolls")]),
    ("Menu", [("c-menu", "Confirm menu, prices and out-of-stock items against Toast"), ("c-bar", "Supply the cocktail, beer, sake and wine list"), ("c-advisory", "Approve the raw-food advisory and allergy wording"), ("c-desc", "Add descriptions for Spring, Kaizen, Toro Dragonfruit, Chirashi and other items without one")]),
    ("Accounts", [("c-social", "Confirm Instagram @osharesushibar and facebook.com/OshareSushiBar"), ("c-gbp", "Grant Google Business Profile access (hours, menu link, photos)"), ("c-toast", "Grant a Toast user with Manage Integrations, confirm Toast plan tier"), ("c-domain", "Grant domain and DNS access for osharesushi.com")]),
    ("Imagery", [("c-photos", "Confirm we may use the existing food photography (and photographer credit)"), ("c-shoot", "Schedule a half-day shoot: room, bar, chefs, guests"), ("c-delivery", "Confirm which third-party delivery apps to mention, if any")]),
]
check_html = "".join(f'<h4 style="margin-top:1.5rem">{g}</h4>' + "".join(f'<label for="{i}"><input type="checkbox" id="{i}"><span>{e(t)}</span><em>{g}</em></label>' for i, t in items) for g, items in CHECK)

SOURCES = [("Oshare Sushi + Bar website (home, about, hours)", "https://osharesushi.com/"), ("Oshare menu on osharesushi.com", "https://osharesushi.com/menu"),
           ("Toast online ordering for Oshare", "https://toast.app/r/osharesushibar/order"), ("OpenTable listing", "https://www.opentable.com/r/oshare-sushi-and-bar-lowell"),
           ("Restaurantji listing", "https://www.restaurantji.com/ma/lowell/oshare-sushi-bar-/"), ("Uber Eats store", "https://www.ubereats.com/store/oshare-sushi-+-bar-lowell/yFPUaBsTXxiNZnV-QOudEg"),
           ("Giftly listing (third-party gift, not official)", "https://www.giftly.com/gift-card/oshare-sushi-and-bar-lowell"), ("Tripadvisor sushi in Lowell", "https://www.tripadvisor.com/Restaurants-g60891-c38-Lowell_Massachusetts.html"),
           ("ThreeBestRated sushi in Lowell", "https://threebestrated.com/sushi-in-lowell-ma"), ("Koto Lowell (closed)", "https://www.kotolowell.com/"),
           ("Jisho: おしゃれ (oshare)", "https://jisho.org/search/oshare"), ("Toast Online Ordering FAQ", "https://support.toasttab.com/en/article/Online-Ordering-FAQ"),
           ("Toast API overview", "https://doc.toasttab.com/doc/devguide/apiOverview.html"), ("Toast standard API access", "https://doc.toasttab.com/doc/devguide/devApiAccessUserGuide.html"),
           ("Toast standard API access FAQs", "https://doc.toasttab.com/doc/devguide/devApiAccessFAQs.html"), ("Toast ordering integration checklist", "https://doc.toasttab.com/doc/cookbook/apiIntegrationChecklistOrdering.html")]
sources_html = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in SOURCES)

page = f"""<title>Oshare Brand Book</title>
<meta name="description" content="Brand book and build plan for Oshare Sushi + Bar, Lowell MA.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@500;700;800&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/oshare.css">
<link rel="stylesheet" href="assets/bb.css">
{ICONS}
<a class="skip" href="#main">Skip to content</a>
<details class="toc-m"><summary><span class="brand"><span class="enso" style="width:32px"></span><span class="wordmark"></span></span><span>Contents</span></summary><nav class="toc-m__list" aria-label="Contents">{toc_m}</nav></details>
<div class="bb">
<nav class="toc" aria-label="Contents"><a class="brand" href="#top"><span class="enso" aria-hidden="true"></span><span class="wordmark" role="img" aria-label="Oshare Sushi + Bar"></span></a><ol>{toc_html}</ol></nav>
<main class="bbmain" id="main">

<header class="cover field" id="top">
  <div class="cover__top"><span>Oshare Sushi + Bar · 350 Market Street, Lowell, MA</span><span>Proposal for owner review · October 2026</span></div>
  <div class="cover__mid">
    <div>
      <h1>Brand Book <span>Blue &amp; White</span></h1>
      <p class="cover__lede">A brand system built from what's already on Oshare's tables: cobalt porcelain, the orange brush ring, and a menu that names Lowell.</p>
      <div class="legend3" style="margin-top:1.75rem">{V}<span class="muted">researched and sourced</span>{R}<span class="muted">our proposal</span>{C()}<span class="muted">needs the owners</span></div>
    </div>
    <div class="cover__lockup"><span class="enso paint"></span><span class="wordmark"></span></div>
  </div>
  <div class="cover__base"><div><b>Prepared by</b>Jeremy Anderson · jeremyanderson.tech</div><div><b>Includes</b>Research, strategy, identity, applications, Toast + SEO + WordPress plan</div><div><b>Companion</b>Five-page website prototype using this system{' · <a href="' + SITE_URL + '" target="_blank" rel="noopener" style="color:var(--on-cobalt)">open it</a>' if SITE_URL else ''}</div></div>
</header>

{part("I", "Discovery", "What Oshare is today, sourced. Everything later in this book stands on this chapter.")}

<section class="ch" id="research">{chead("research", "What we found", "Public sources checked on October 8, 2026. Where sources disagree, the restaurant's own site wins.")}
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">Fact</th><th scope="col">What we found</th><th scope="col">Source</th><th scope="col">Status</th></tr></thead><tbody>
    <tr><td>Name</td><td>Oshare Sushi + Bar. Also appears as "Oshare Sushi Bar" and "Oshare Sushi &amp; Bar".</td><td>osharesushi.com, OpenTable, Yelp</td><td>{V} {C("Standardize")}</td></tr>
    <tr><td>Address · phone</td><td>350 Market Street, Lowell, MA 01852 · (978) 677-2636</td><td>osharesushi.com, Toast</td><td>{V}</td></tr>
    <tr><td>Hours</td><td>Sun 11:30 AM–9 PM · Mon closed · Tue–Thu 4–9 PM · Fri–Sat 11:30 AM–10 PM</td><td>osharesushi.com "All hours"; matches Restaurantji</td><td>{V}</td></tr>
    <tr><td>Chefs</td><td>Chefs Bryan and Son, more than 30 years of combined experience. No surnames, bios or founding date published.</td><td>osharesushi.com/about</td><td>{V} {C("Bios")}</td></tr>
    <tr><td>Menu</td><td>{n_items} items across specialty and classic maki, nigiri/sashimi, sets, sushi-bar and kitchen apps, rice plates, noodles, udon, lunch, desserts and sides. Specialty maki $12–22.</td><td>Toast online ordering, osharesushi.com/menu</td><td>{V}</td></tr>
    <tr><td>Cuisine</td><td>Japanese sushi with Korean-leaning kitchen dishes: bulgogi maki, Kogi beef bowl, spicy beef bao, Santaka noodles.</td><td>Menu; OpenTable lists Sushi, Japanese, Korean</td><td>{V}</td></tr>
    <tr><td>Ordering</td><td>Toast online ordering, pickup and delivery. Each dish has its own Toast link. Toast gift cards and rewards (1 point per $1) are live.</td><td>toast.app ordering page</td><td>{V}</td></tr>
    <tr><td>Third-party delivery</td><td>Uber Eats, DoorDash and Grubhub logos appear on Oshare's own promo graphic. Uber Eats store confirmed (4.9, 27 ratings).</td><td>osharesushi.com image, Uber Eats</td><td>{V}</td></tr>
    <tr><td>Reservations</td><td>No online booking. OpenTable says the restaurant isn't on its network and to call.</td><td>OpenTable</td><td>{V}</td></tr>
    <tr><td>Bar</td><td>Full bar, cocktails, counter seating. No drinks list published.</td><td>OpenTable features and reviews</td><td>{V} {C("Drinks list")}</td></tr>
    <tr><td>Ratings</td><td>Restaurantji 4.8 (68) · OpenTable 4.8 (10) · Uber Eats 4.9 (27) · Yelp 4.3 (6, via Giftly)</td><td>Each platform</td><td>{V}</td></tr>
    <tr><td>Review themes</td><td>Fish quality, presentation, friendly and attentive staff, cocktails, relaxed room, fair prices.</td><td>OpenTable, Restaurantji</td><td>{V}</td></tr>
    <tr><td>Social</td><td>Instagram @osharesushibar and facebook.com/OshareSushiBar appear under the name and match #OshareSushiBar on their graphic. Profiles could not be read by our tools.</td><td>Search results</td><td>{C("Confirm handles")}</td></tr>
  </tbody></table></div>
</section>

<section class="ch" id="conflicts">{chead("conflicts", "Conflicts &amp; open questions", "Things the public record gets wrong or leaves blank. Each one is on the owner checklist in 5.6.")}
  <div class="g3">
    <div class="panel"><h3>Hours disagree</h3><p>OpenTable says daily 11:30–9. Oshare's own site and Restaurantji say Monday closed and weekday dinner only. We used the restaurant's site. OpenTable and any other listings need correcting.</p>{C("Fix listings")}</div>
    <div class="panel"><h3>Parking</h3><p>OpenTable says street parking only. Restaurantji and ThreeBestRated mention an adjacent or free lot. The site says "parking nearby" until confirmed.</p>{C()}</div>
    <div class="panel"><h3>Party of 2 vs. 21</h3><p>The osharesushi.com menu text reads "Party of 21". Toast shows "Party of 2" at $96. We used Toast.</p>{C()}</div>
    <div class="panel"><h3>Lunch</h3><p>A lunch menu is published but no lunch hours are. Tue–Thu opens at 4 PM, so lunch likely runs Fri–Sun only.</p>{C()}</div>
    <div class="panel"><h3>Items without descriptions</h3><p>Spring Maki, Kaizen Maki, Toro Dragonfruit, Chirashi, Takoyaki, Otoro and others have no description. We left them blank rather than guess.</p>{C()}</div>
    <div class="panel"><h3>No room or people</h3><p>Every published photo is food. There are no images of the dining room, bar, chefs or guests, so the site can't yet show the "+ Bar" half of the name.</p>{C("Photo shoot")}</div>
  </div>
</section>

<section class="ch" id="market">{chead("market", "Lowell's sushi landscape", "Who else a Lowell diner finds when searching for sushi, and where Oshare can stand apart.")}
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">Competitor</th><th scope="col">Model</th><th scope="col">What it signals</th></tr></thead><tbody>
    <tr><td>Fooddy Goody Sushi &amp; Asian Cuisine</td><td>Chinese-Japanese, family-friendly, 101 Lakeview Ave</td><td>Value and variety</td></tr>
    <tr><td>Sugoi Restaurant</td><td>Pizza, sushi and burgers; all-you-can-eat; rooftop; 415 Lawrence St</td><td>Volume and novelty</td></tr>
    <tr><td>Fuji Sushi Chinese Bar</td><td>Chinese-Japanese combination menu</td><td>Convenience</td></tr>
    <tr><td>China Buffet</td><td>Buffet with sushi</td><td>Price</td></tr>
    <tr><td>Koto Lowell</td><td>Asian fusion + live music venue, 76 Merrimack St. Now permanently closed.</td><td>Leaves a gap for a stylish downtown sushi night out</td></tr>
  </tbody></table></div>
  <p class="big-statement" style="margin-top:2.5rem">Nobody in town owns <em>chef-made sushi with a real bar</em> at neighborhood prices. Oshare already does it. The brand just has to say so.</p>
  <p class="muted" style="margin-top:1rem;font-size:var(--fs-sm)">Sources: Tripadvisor and ThreeBestRated Lowell sushi listings, Koto's own site. We did not measure search volumes; see 5.2 for the keyword plan.</p>
</section>

<section class="ch" id="audit">{chead("audit", "Current identity audit")}
  <div class="g2">
    <div class="stack"><h3>Keep</h3>
      <p><b>The orange ensō.</b> A hand-brushed ring with real energy, and the only distinctive asset Oshare owns. We traced it to vector so it scales cleanly. {V}</p>
      <p><b>The photography.</b> A consistent professional shoot: white-grey marble, 3/4 angles, cobalt blue-and-white porcelain, a red-rimmed lacquer tray and edible flowers. {V}</p>
      <p><b>The menu names.</b> The Acre, Red Sox Maki and the Celtic Roll tie the menu to Lowell. {V}</p></div>
    <div class="stack"><h3>Replace</h3>
      <p><b>The Toast template site.</b> Generic layout with Shrikhand and Inter, yellow buttons that appear nowhere else in the brand, no menu content beyond Toast's list, and no story.</p>
      <p><b>The promo graphic.</b> Black panel with three delivery-app logos above the restaurant's own ordering link. It pushes guests to apps that cost the restaurant commission.</p>
      <p><b>The wordmark's "A".</b> The slashed A reads as a sword cut. We kept it in this proposal because it's theirs, but it leans on the samurai cliché the brief asks us to avoid. {C("Discuss")}</p></div>
  </div>
  <div class="g4" style="margin-top:2rem">
    <figure class="ph"><img src="img/tray.jpg" alt="Nigiri Deluxe in lacquer tray on marble" loading="lazy"><figcaption>Marble, lacquer, 3/4 angle</figcaption></figure>
    <figure class="ph"><img src="img/udon.jpg" alt="Noodles in a cobalt porcelain bowl" loading="lazy"><figcaption>The cobalt bowls the palette comes from</figcaption></figure>
    <figure class="ph"><img src="img/lobster.jpg" alt="Lobster Rangoon Maki" loading="lazy"><figcaption>Edible flowers, long plates</figcaption></figure>
    <figure class="ph"><img src="img/night.jpg" alt="Overhead table on dark wood" loading="lazy"><figcaption>The one evening shot</figcaption></figure>
  </div>
</section>

<section class="ch" id="word">{chead("word", "The word <i>oshare</i>")}
  <div class="g2" style="align-items:center">
    <p class="big-statement">おしゃれ <span style="font-size:.6em;color:var(--ink-2)">oshare</span><br>stylish, fashionable, <em>dressed up.</em></p>
    <div class="prose"><p>In everyday Japanese, <i>oshare</i> describes someone who dresses well or a place with good taste. It is usually written in kana. {V}</p><p>We use the idea, not the story. "Dressed-up sushi" in the homepage line is a nod to the meaning that works even if nobody knows the word. We won't present it as the origin of the name until the owners tell us why they chose it. {C("Naming intent")}</p><p class="muted" style="font-size:var(--fs-sm)">The kana appears here, in this book, only. The brief asks for no decorative Japanese characters on the site, and we agree.</p></div>
  </div>
</section>

{part("II", "Strategy", "Who Oshare is for, what it promises, and how it talks. All of this is our proposal, built on the facts in Part I.")}

<section class="ch" id="positioning">{chead("positioning", "Positioning")}
  <p class="big-statement">For Lowell diners who want sushi that feels like a night out without night-out prices, Oshare is the downtown sushi bar where <em>chef-made maki, Korean-leaning kitchen plates and a full bar</em> arrive dressed up on blue-and-white porcelain.</p>
  <p style="margin-top:1.5rem">{R}</p>
  <div class="g3" style="margin-top:2rem">
    <div class="rule-top stack"><h3>Versus combo menus</h3><p class="muted">Oshare is chef-run and sushi-first, not a Chinese-Japanese catch-all.</p></div>
    <div class="rule-top stack"><h3>Versus all-you-can-eat</h3><p class="muted">Plated with care, named and composed. Quality over volume.</p></div>
    <div class="rule-top stack"><h3>Versus Boston omakase</h3><p class="muted">Neighborhood prices, no reservations needed, and a menu that speaks Lowell.</p></div>
  </div>
</section>

<section class="ch" id="personality">{chead("personality", "Promise &amp; personality")}
  <p class="big-statement">Dressed up, <em>never uptight.</em></p><p style="margin-top:1rem">{R} The brand promise. Every plate looks like an occasion; every guest feels at home.</p>
  <div class="tbl-wrap" style="margin-top:2rem"><table class="tbl"><thead><tr><th scope="col">Trait</th><th scope="col">Means</th><th scope="col">Not</th></tr></thead><tbody>
    <tr><td>Stylish</td><td>Considered plating, porcelain, color, a good-looking room</td><td>Fussy, exclusive, precious</td></tr>
    <tr><td>Warm</td><td>Staff who explain the menu, regulars remembered</td><td>Slick or scripted</td></tr>
    <tr><td>Local</td><td>Rolls named for Lowell, downtown pride</td><td>Touristy or generic "Asian"</td></tr>
    <tr><td>Playful</td><td>Firebender, Red Sox Maki, a little wit in the copy</td><td>Gimmicky or jokey about the food</td></tr>
    <tr><td>Precise</td><td>Exact prices, real hours, clear raw and spice marks</td><td>Cold or clinical</td></tr>
  </tbody></table></div>
</section>

<section class="ch" id="audiences">{chead("audiences", "Audiences &amp; personas", "Primary: Lowell locals ordering or walking in. Secondary: planned nights out. Tertiary: visitors to downtown. Personas are illustrative, not research subjects.")}
  <p style="margin-bottom:1.5rem">{R} {C("Validate with owners")}</p>
  <div class="g3">
    <div class="persona"><h3>The weeknight regular</h3><dl><dt>Who</dt><dd>Lives or works near downtown, orders every week or two</dd><dt>Moment</dt><dd>5:15 PM on a phone, already hungry</dd><dt>Needs</dt><dd>Is it open? Reorder the usual fast. Pickup time.</dd><dt>Wins with</dt><dd>Live open status, one-tap order, dish links</dd></dl></div>
    <div class="persona"><h3>The night out</h3><dl><dt>Who</dt><dd>A couple or four friends planning dinner downtown</dd><dt>Moment</dt><dd>Two days ahead, on a laptop or in a group chat</dd><dt>Needs</dt><dd>The vibe, the bar, prices, whether to call ahead</dd><dt>Wins with</dt><dd>Food photography, the +Bar story, clear "call us" policy</dd></dl></div>
    <div class="persona"><h3>The downtown visitor</h3><dl><dt>Who</dt><dd>UMass Lowell families, park visitors, event-goers</dd><dt>Moment</dt><dd>Searching "sushi near me" on Market Street</dd><dt>Needs</dt><dd>Ratings, walkability, lunch on weekends</dd><dt>Wins with</dt><dd>Google profile, ratings, directions, lunch section</dd></dl></div>
  </div>
</section>

<section class="ch" id="experience">{chead("experience", "The guest experience", "How it should feel at each step, and what the brand does there.")}
  <div class="journey">
    <div><b>Hungry</b><span>Sees the hero dish ringed in orange and "Open now" before scrolling.</span></div>
    <div><b>Tempted</b><span>Real plates, real prices, Lowell names. Ordering is one tap away.</span></div>
    <div><b>Welcomed</b><span>Porcelain, color, staff who explain the specialty maki.</span></div>
    <div><b>Regular</b><span>Rewards on direct orders, a new roll to try, a reason to post it.</span></div>
  </div>
  <p style="margin-top:1rem">{R}</p>
</section>

<section class="ch" id="mission">{chead("mission", "Mission &amp; vision")}
  <div class="g2">
    <div class="rule-top stack"><h4>Mission</h4><p class="big-statement" style="font-size:clamp(1.4rem,1rem + 1.4vw,2rem)">Make any night in Lowell feel a little dressed up, with carefully made sushi, bold kitchen plates and warm service at neighborhood prices.</p>{R}</div>
    <div class="rule-top stack"><h4>Vision</h4><p class="big-statement" style="font-size:clamp(1.4rem,1rem + 1.4vw,2rem)">The first place Lowell thinks of for sushi, and the place locals bring visitors to show off downtown.</p>{R}</div>
  </div>
</section>

<section class="ch" id="voice">{chead("voice", "Voice &amp; tone", "Warm, direct and specific, with a little wit. Write like a good server talks you through the menu.")}
  <div class="voice">
    <div><h4>Say</h4><p class="say">Lobster tail tempura, plum sauce, crispy wontons. $19.</p></div><div><h4>Not</h4><p class="nosay">An unforgettable fusion of flavors that will tantalize your taste buds.</p></div>
    <div><h4>Say</h4><p class="say">Open until 9 tonight. Pickup in about 40 minutes.</p></div><div><h4>Not</h4><p class="nosay">We look forward to serving you during our operating hours.</p></div>
    <div><h4>Say</h4><p class="say">Very spicy. The ghost pepper is not a suggestion.</p></div><div><h4>Not</h4><p class="nosay">🔥🔥🔥 FIRE ROLL ALERT 🔥🔥🔥</p></div>
    <div><h4>Say</h4><p class="say">Call us or walk in. We don't take online reservations.</p></div><div><h4>Not</h4><p class="nosay">Reservations are currently unavailable at this time.</p></div>
  </div>
  <div class="g3" style="margin-top:2rem">
    <div class="stack"><h3>Name the food</h3><p class="muted">Ingredients and prices do the persuading. Skip adjectives like "delicious" and "authentic".</p></div>
    <div class="stack"><h3>Talk like Lowell</h3><p class="muted">Market Street, the Acre, game nights. Local, never touristy.</p></div>
    <div class="stack"><h3>No costume</h3><p class="muted">No faux-Japanese phrasing, no random characters, no "Konnichiwa" greetings.</p></div>
  </div>
</section>

<section class="ch" id="messaging">{chead("messaging", "Story &amp; messaging")}
  <p class="big-statement">Dressed-up sushi on <em>Market Street.</em></p>
  <p style="margin:1rem 0 2rem">{R} Primary line. Alternates: "Dressed up. Never uptight." · "Sushi, dressed for Lowell."</p>
  <div class="g4">
    <div class="rule-top stack"><h3>Made with care</h3><p class="muted">Chefs Bryan and Son, 30+ years combined. Nigiri and maki cut to order.</p>{V}</div>
    <div class="rule-top stack"><h3>Two counters</h3><p class="muted">A sushi bar and a Korean-leaning kitchen: bulgogi, bao, Santaka noodles.</p>{V}</div>
    <div class="rule-top stack"><h3>Named for Lowell</h3><p class="muted">The Acre, Red Sox Maki, the Celtic Roll.</p>{V} {C("Stories")}</div>
    <div class="rule-top stack"><h3>Easy to get</h3><p class="muted">Order direct for pickup or delivery. Open Tuesday to Sunday.</p>{V}</div>
  </div>
  <div class="panel" style="margin-top:2rem"><h4>The short story</h4><p class="big-statement" style="font-size:clamp(1.3rem,1rem + 1vw,1.8rem);max-width:46ch">Oshare is a neighborhood sushi bar on Market Street in downtown Lowell. Chefs Bryan and Son run a sushi counter and a kitchen side by side, so a night here can be nigiri and a Passion Roll or spicy bulgogi bao and Santaka noodles, with a cocktail from the full bar. Everything arrives on blue-and-white porcelain.</p>{R}</div>
</section>

<section class="ch" id="principles">{chead("principles", "Brand principles")}
  <div class="g3">
    <div class="rule-top stack"><h3>Real or labeled</h3><p class="muted">Every fact, price and photo is real, or it is marked for the owners to confirm.</p></div>
    <div class="rule-top stack"><h3>One hot note</h3><p class="muted">Orange appears once per view: the ring, the order button, or one word. Cobalt does the heavy lifting.</p></div>
    <div class="rule-top stack"><h3>The plate is the hero</h3><p class="muted">Photography leads. Type frames it. Nothing decorates over the food.</p></div>
    <div class="rule-top stack"><h3>Order is always one tap</h3><p class="muted">Direct ordering is visible on every page and every screen size.</p></div>
    <div class="rule-top stack"><h3>Lowell, not costume</h3><p class="muted">Identity comes from the tableware, the brush ring and the city, never from borrowed symbols.</p></div>
    <div class="rule-top stack"><h3>Owners can run it</h3><p class="muted">Every component maps to a WordPress block the restaurant can edit.</p></div>
  </div>
</section>

{part("III", "Identity", "The visual system. Every element traces back to an object already on Oshare's tables.")}

<section class="ch" id="directions">{chead("directions", "Directions explored", "The brief asked for three directions. Each was built from something real in Oshare's world. You chose Blue &amp; White.")}
  <div class="g3">
    <div class="dir dir--chosen">
      <div class="dir__art"><div class="artA"><p>Dressed-up sushi on <span>Market Street.</span></p><div><img src="img/night.jpg" alt=""><span class="enso"></span></div></div></div>
      <h3>A · Blue &amp; White <span class="tag tag--r" style="margin-left:.3rem">Selected</span></h3>
      <div class="dir__chips"><i style="background:#F3F5F9"></i><i style="background:#1F3F80"></i><i style="background:#F25A0A"></i><i style="background:#0B1A36"></i></div>
      <dl><dt>Brief lane</dt><dd>Contemporary Culinary Editorial</dd><dt>Source</dt><dd>Oshare's cobalt sometsuke bowls and the orange brush ring</dd><dt>Strength</dt><dd>Food-first, unmistakably theirs, calm enough to last years</dd><dt>Risk</dt><dd>Refined directions can drift toward "tasteful restaurant site". The orange ring and full cobalt fields keep it from going quiet.</dd></dl>
    </div>
    <div class="dir">
      <div class="dir__art"><div class="artB"><header>Oshare<small>Lowell, Mass.</small></header><section><figure><img src="img/tray.jpg" alt=""><b>1</b><figcaption>Nigiri Deluxe</figcaption></figure><figure><img src="img/santaka.jpg" alt=""><b>2</b><figcaption>Santaka Beef</figcaption></figure><figure><img src="img/lobster.jpg" alt=""><b>3</b><figcaption>Lobster Rangoon</figcaption></figure></section></div></div>
      <h3>B · Mill City Field Guide</h3>
      <div class="dir__chips"><i style="background:#121212"></i><i style="background:#F1EFE8"></i><i style="background:#F25A0A"></i></div>
      <dl><dt>Brief lane</dt><dd>Modern Neighborhood Hospitality</dd><dt>Source</dt><dd>Lowell National Historical Park's brochure system: black title band, strict grid, numbered stops</dd><dt>Strength</dt><dd>Deeply local; the menu becomes a guide to Oshare</dd><dt>Risk</dt><dd>Reads institutional; warmth depends entirely on photography</dd></dl>
    </div>
    <div class="dir">
      <div class="dir__art"><div class="artC"><h5>OSHARE</h5><p><b>The Acre, $18</b>Shrimp tempura, lobster mix, mango, plum sauce</p><img src="img/firebender.jpg" alt=""><span class="call" style="right:36cqw;top:44cqw">ghost pepper sate</span><span class="call" style="right:6cqw;top:38cqw">salmon</span></div></div>
      <h3>C · Oshare Magazine</h3>
      <div class="dir__chips"><i style="background:#FFD9C2"></i><i style="background:#1F3F80"></i><i style="background:#E2450A"></i><i style="background:#121212"></i></div>
      <dl><dt>Brief lane</dt><dd>Bold Japanese-Fusion Expression</dd><dt>Source</dt><dd>"Oshare" means stylish: Japanese street-style magazines, cover lines and outfit callouts for each dish</dd><dt>Strength</dt><dd>Loud, fun, very shareable</dd><dt>Risk</dt><dd>Tips into gimmick across a whole site; leans on the name's meaning before the owners confirm it</dd></dl>
    </div>
  </div>
  <p style="margin-top:2rem" class="muted">B and C stay on file. One idea from B survives in the chosen system: the menu legend that marks raw and spicy dishes, borrowed from a map key.</p>
</section>

<section class="ch" id="logo">{chead("logo", "Logo system", "Oshare's existing mark, traced from their file into clean vectors and organized into a family. The design is theirs; the system is new.")}
  <div class="g3">
    <div class="spec spec--white">{LOCKUP()}<span class="cap">Primary · on white or glaze</span></div>
    <div class="spec spec--cobalt">{LOCKUP("lockup--white")}<span class="cap">Reverse · on cobalt</span></div>
    <div class="spec spec--ink">{LOCKUP("lockup--white")}<span class="cap">Reverse · on ink</span></div>
    <div class="spec spec--glaze"><div class="hlock" style="color:var(--ink)"><span class="enso"></span><span class="wordmark"></span></div><span class="cap">Horizontal · headers, menus, receipts</span></div>
    <div class="spec spec--cobalt"><span class="enso" style="width:34%"></span><span class="cap">Compact mark · avatar, favicon, seal</span></div>
    <div class="spec spec--glaze"><span class="wordmark" style="width:62%;color:var(--ink)"></span><span class="cap">Wordmark · narrow spaces</span></div>
  </div>
  <h3 style="margin:2.5rem 0 1rem">One-color versions</h3>
  <div class="g4">
    <div class="spec spec--white">{LOCKUP("lockup--mono-cobalt")}<span class="cap">Cobalt · stamps, sleeves</span></div>
    <div class="spec spec--cobalt">{LOCKUP("lockup--mono-white")}<span class="cap">White · on dark photos</span></div>
    <div class="spec spec--white">{LOCKUP("lockup--mono-ink")}<span class="cap">Ink · receipts, fax</span></div>
    <div class="spec spec--enso">{LOCKUP("lockup--mono-ink")}<span class="cap">Ink on orange · stickers</span></div>
  </div>
  <div class="g2" style="margin-top:3rem;align-items:center">
    <div><div class="clear"><span class="clear__x">clear space = x, a quarter of the ring</span><span class="enso"></span><span class="wordmark"></span></div></div>
    <div class="stack"><h3>Clear space &amp; minimum sizes</h3><p>Keep a quarter of the ring's width clear on every side. Nothing else enters that space.</p>
      <div class="tbl-wrap"><table class="tbl" style="min-width:0"><tbody><tr><td>Primary lockup</td><td class="num">72 px wide · 20 mm print</td></tr><tr><td>Horizontal</td><td class="num">120 px wide · 30 mm</td></tr><tr><td>Compact ring</td><td class="num">16 px · 6 mm</td></tr><tr><td>Wordmark alone</td><td class="num">80 px wide · 22 mm</td></tr></tbody></table></div>
      <p class="muted" style="font-size:var(--fs-sm)">Vector files: lockup-color.svg, lockup-reverse.svg, lockup-mask.svg, enso.svg, wordmark.svg. {C("Compare against the original art")}</p></div>
  </div>
  <h3 style="margin:2.5rem 0 1rem">Don't</h3>
  <div class="g3">
    {''.join(f'<div class="misuse"><div class="spec {bg}">{inner}</div><span class="x" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M4 4l8 8M12 4l-8 8"/></svg></span><p>{t}</p></div>' for bg, inner, t in [
      ("spec--white", '<div class="lockup lockup--ink" style="transform:scaleX(1.45)"><span class="enso"></span><span class="wordmark"></span></div>', "Stretch or squash it."),
      ("spec--white", '<div class="lockup lockup--ink"><span class="enso" style="background:#2E58A6"></span><span class="wordmark"></span></div>', "Recolor the ring. It is always orange, or the single mono color."),
      ("spec--photo\" style=\"background-image:url(img/spread.jpg)", '<div class="lockup lockup--ink"><span class="enso"></span><span class="wordmark"></span></div>', "Set it on a busy photo without a cobalt or glaze field."),
      ("spec--white", '<div class="lockup lockup--ink" style="filter:drop-shadow(6px 6px 3px rgba(0,0,0,.45))"><span class="enso"></span><span class="wordmark"></span></div>', "Add shadows, glows or bevels."),
      ("spec--white", '<div class="lockup lockup--ink"><span class="enso"></span><span class="wordmark" style="transform:rotate(-18deg)"></span></div>', "Rotate or move the wordmark inside the ring."),
      ("spec--enso", '<div class="lockup lockup--white"><span class="enso"></span><span class="wordmark"></span></div>', "Put the color lockup on orange, where the ring disappears.")])}
  </div>
</section>

<section class="ch" id="color">{chead("color", "Color", "Two materials and one stroke: porcelain glaze, underglaze cobalt, and the orange ring.")}
  <div class="g4">{swatches}</div>
  <h3 style="margin:2.5rem 0 1rem">Proportion</h3>
  <div class="ratio"><div style="flex:58;background:#F3F5F9;color:#0B1A36;box-shadow:inset 0 0 0 1px var(--line)">Glaze 58%</div><div style="flex:30;background:#1F3F80;color:#F3F5F9">Cobalt 30%</div><div style="flex:8;background:#0B1A36;color:#F3F5F9">Ink</div><div style="flex:4;background:#F25A0A;color:#0B1A36">4</div></div>
  <p class="muted" style="margin-top:.75rem">Cobalt owns whole sections, never thin accents. Orange stays under 5% of any view.</p>
  <h3 style="margin:2.5rem 0 .5rem">Accessible pairs</h3><p class="muted" style="margin-bottom:1rem">Contrast ratios computed against WCAG 2.2. AA needs 4.5:1 for text, 3:1 for large text and graphics.</p>
  <div>{pairs}</div>
  <p class="muted" style="margin-top:1rem;font-size:var(--fs-sm)">A night palette (deep cobalt ground, glaze text) ships for visitors whose devices are set to dark mode. Same roles, same ratios.</p>
</section>

<section class="ch" id="type">{chead("type", "Typography", "Two faces from Japanese type foundries, both designed with Latin letters. Japanese menus set English this way, which makes the pairing feel at home without a single decorative character.")}
  <div class="g2">
    <div class="panel"><h4>Display · Shippori Mincho B1</h4><p class="alphabet">Aa Gg 18</p><p class="muted">Weights 500, 700, 800. The "B1" cut has softened, ink-pooled corners, like cobalt brushed onto glaze. Headlines, dish names, prices.</p></div>
    <div class="panel"><h4>Text · Zen Kaku Gothic New</h4><p class="alphabet" style="font-family:var(--sans);font-weight:700">Aa Gg 18</p><p class="muted">Weights 400, 500, 700. A calm gothic for menus, descriptions and buttons. Both faces are free on Google Fonts.</p></div>
  </div>
  <div style="margin-top:2rem">
    <div class="tspec"><small>Hero · Mincho 800<br>40–80 px · -0.03em</small><p style="font-family:var(--display);font-weight:800;font-size:var(--fs-hero);line-height:1;letter-spacing:-.03em">Dressed-up sushi</p></div>
    <div class="tspec"><small>H2 · Mincho 700<br>32–58 px · -0.02em</small><p style="font-family:var(--display);font-weight:700;font-size:var(--fs-h2);line-height:1.08">Three rolls named for home.</p></div>
    <div class="tspec"><small>Dish · Mincho 700<br>21–27 px</small><p style="font-family:var(--display);font-weight:700;font-size:var(--fs-h3)">Lobster Rangoon Maki <span style="color:var(--enso-ink)">$19</span></p></div>
    <div class="tspec"><small>Lead · Gothic 400<br>17–21 px · 1.6</small><p style="font-size:var(--fs-lead)">Specialty maki, nigiri and a Korean-leaning kitchen from Chefs Bryan and Son.</p></div>
    <div class="tspec"><small>Body · Gothic 400<br>17 px · 1.65</small><p>Lobster tail tempura, avocado, whipped cream cheese, plum sauce, spicy mayo, fried onions, crispy wontons.</p></div>
    <div class="tspec"><small>Label · Gothic 700<br>12 px caps · +0.12em</small><p style="font-size:var(--fs-xs);font-weight:700;letter-spacing:.12em;text-transform:uppercase">Served raw or undercooked</p></div>
  </div>
  <p class="muted" style="margin-top:1rem">Prices use tabular figures. Headlines balance across lines. Running text stays near 65 characters.</p>
</section>

<section class="ch" id="graphics">{chead("graphics", "Graphic system", "Three devices, all taken from the table.")}
  <div class="g3">
    <div class="stack"><div class="panel" style="min-height:180px;display:grid;place-items:center"><hr class="rim" style="width:100%"></div><h3>The rim rule</h3><p class="muted">A heavy line over a hairline, like the painted rim of Oshare's bowls. The only divider in the system. Under section heads, over menus, around packaging.</p></div>
    <div class="stack"><div class="panel" style="min-height:180px;display:grid;place-items:center;background:#1F3F80"><span class="enso" style="width:46%"></span></div><h3>The ensō frame</h3><p class="muted">The brush ring circles one thing per view: the hero dish, a featured plate on hover, the active menu section. It never becomes a pattern.</p></div>
    <div class="stack"><div class="panel field" style="min-height:180px"></div><h3>Cobalt field</h3><p class="muted">Solid cobalt with a faint grain, like glaze over clay. It holds headlines, the Lowell rolls, hours and the footer.</p></div>
  </div>
  <p class="muted" style="margin-top:1.5rem">Deliberately absent: cherry blossoms, waves, fans, kanji, samurai, red-and-black. The bowls' floral borders stay on the bowls.</p>
</section>

<section class="ch" id="icons">{chead("icons", "Icons &amp; marks", "One stroke family: 24 px grid, 1.7 px stroke, round caps. Menu marks never rely on color alone.")}
  <div class="icons">{''.join(f'<div>{ico(i)}<span>{t}</span></div>' for i, t in [("bag", "Order"), ("phone", "Call"), ("pin", "Location"), ("clock", "Hours"), ("search", "Search"), ("menu", "Menu"), ("gift", "Gift card"), ("car", "Parking"), ("glass", "Bar"), ("arrow", "Go to")])}</div>
  <div class="g3" style="margin-top:1.5rem">
    <div class="panel"><span class="mark mark--raw">RAW</span><p class="muted">Served raw or undercooked. Mirrors Toast's asterisk.</p></div>
    <div class="panel"><span class="mark mark--hot"><svg aria-hidden="true"><use href="#i-chili"/></svg></span><p class="muted">Spicy, only where the menu says so.</p></div>
    <div class="panel"><span class="mark mark--hot"><svg aria-hidden="true"><use href="#i-chili"/></svg><svg aria-hidden="true"><use href="#i-chili"/></svg></span><p class="muted">Very spicy: Firebender, Santaka, ghost pepper.</p></div>
  </div>
  <p class="muted" style="margin-top:1rem;font-size:var(--fs-sm)">No vegetarian, vegan or allergen marks until the kitchen confirms them. {C("Dietary marks")}</p>
</section>

<section class="ch" id="photo">{chead("photo", "Photography", "The existing shoot sets the standard. The gap is everything that isn't food.")}
  <div class="g3">
    <figure class="ph ph--do"><img src="img/crispyRice.jpg" alt="Tuna crispy rice on a long white plate" loading="lazy"><figcaption><b>Keep:</b> marble ground, soft daylight, 3/4 angle, edible flowers.</figcaption></figure>
    <figure class="ph ph--do"><img src="img/santaka.jpg" alt="Santaka noodles in porcelain" loading="lazy"><figcaption><b>Keep:</b> the cobalt porcelain in frame. It is the palette.</figcaption></figure>
    <figure class="ph ph--do"><img src="img/night.jpg" alt="Overhead table at night" loading="lazy"><figcaption><b>Keep:</b> overhead tables on dark wood for evening and bar stories.</figcaption></figure>
  </div>
  <div class="g2" style="margin-top:2.5rem">
    <div><h3>Shot list for the first shoot {C("Schedule")}</h3>
      <div>{''.join(f'<div class="shot"><b>{i:02d}</b><span>{t}</span></div>' for i, t in enumerate(["The bar at dusk from the door, lights on, one cocktail in focus", "Chefs at the sushi counter, hands slicing salmon belly", "Chef at the wok tossing Santaka noodles, motion blur allowed", "The Acre, Red Sox Maki and Celtic Roll, each on the long white plate", "Passion Roll overhead with the dragon fruit aioli visible", "The dining room full, guests with releases, faces optional", "Pickup bags on the counter with the rim band", "Market Street exterior and signage, day and evening", "Two cocktails on the bar, porcelain bowls behind", "A table of four sharing the Party of 2 set"], 1))}</div></div>
    <div class="stack"><h3>Rules</h3><p><b>Light:</b> daylight or warm tungsten, never colored LEDs.</p><p><b>Props:</b> only Oshare's own tableware, chopsticks and napkins.</p><p><b>Edit:</b> true color. No heavy filters, no added steam.</p><p><b>Crop:</b> leave space on one side for type, especially for social.</p><p><b>Never:</b> stock sushi, AI-generated food, or photos of other restaurants' dishes.</p></div>
  </div>
</section>

<section class="ch" id="layout">{chead("layout", "Layout &amp; spacing", "A 12-column grid, a 4 px spacing scale, generous space above headings.")}
  <div class="griddemo" aria-hidden="true">{'<i></i>' * 12}</div>
  <p class="muted" style="margin:.75rem 0 2rem">12 columns · max width 1320 px · gutter 16–48 px fluid · cobalt sections run full bleed</p>
  <div class="spacing">{''.join(f'<div><i style="width:{v}px;height:{v}px"></i>{v}</div>' for v in [4, 8, 12, 16, 24, 32, 48, 64, 96, 128])}</div>
  <div class="g3" style="margin-top:2rem">
    <div class="rule-top stack"><h3>Split hero</h3><p class="muted">Cobalt copy column (11 parts) against a photo (13 parts). The ring straddles the food.</p></div>
    <div class="rule-top stack"><h3>Plates grid</h3><p class="muted">One wide plate and one narrow, then three across. Never a wall of identical cards.</p></div>
    <div class="rule-top stack"><h3>Menu columns</h3><p class="muted">Two columns of dishes with hairlines, a rim rule under each section head.</p></div>
  </div>
</section>

<section class="ch" id="components">{chead("components", "UI components", "Live components from the website, rendered with the production CSS.")}
  <div class="board">
    <div class="row"><a class="btn" href="{ORDER}" target="_blank" rel="noopener">{ico("bag")}Order pickup</a><a class="btn btn--ghost" href="#components">See the menu</a><a class="btn btn--sm" href="#components">Small</a><span class="btn" aria-disabled="true">Ordering paused</span><a class="link-arrow" href="#components">Add to pickup order{ico("arrow")}</a></div>
    <div class="row"><span class="status" data-open="true"><span class="status__dot"></span><span><b>Open now</b> Until 9 PM tonight</span></span><span class="status" data-open="false"><span class="status__dot"></span><span><b>Closed now</b> Opens tomorrow at 4 PM</span></span><button class="chip" type="button" aria-pressed="true">No raw fish</button><button class="chip" type="button" aria-pressed="false">Spicy</button><span class="note">Pitch note</span></div>
    <ul class="mlist" role="list" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:1rem">
      <li class="mitem mitem--photo"><img class="mitem__img" src="img/firebender.jpg" alt=""><h3>Firebender Maki <span class="mark mark--raw">RAW</span><span class="mark mark--hot"><svg><use href="#i-chili"/></svg><svg><use href="#i-chili"/></svg></span></h3><span class="mitem__price">$17</span><p class="mitem__desc">Spicy tuna mix, salmon, apple, avocado, sweet potato tempura, ghost pepper sate</p><div class="mitem__act"><a href="{ORDER}/item-firebender-maki_1d96c5db-8b62-47e7-8c83-397c6780c539" target="_blank" rel="noopener">Add to order{ico("arrow")}</a></div></li>
      <li class="mitem" data-oos="true"><h3>Japanese Uni <span class="mark mark--raw">RAW</span></h3><span class="mitem__price">$20</span><p class="mitem__desc">Menu item, sold-out state.</p><div class="mitem__act"><span class="oos">Sold out today</span></div></li>
    </ul>
  </div>
</section>

<section class="ch" id="motion">{chead("motion", "Motion", "One authored moment: the brush paints its ring. Everything else is quiet.")}
  <div class="motion-demo">
    <div class="stage"><span class="enso paint" id="demo-ring"></span></div>
    <div class="stack"><h3>The brush stroke</h3><p>The ring is revealed by a sweeping mask that starts at the brush's opening and travels clockwise, 1.7 seconds, easing out fast like a real stroke.</p><p><b>Where:</b> hero load, page headers, hover on featured plates.</p><p><b>Reduced motion:</b> the finished ring appears with no sweep.</p><p><b>Never:</b> spinning, looping, or parallax on food.</p><div><button class="btn btn--ghost btn--sm" type="button" data-replay="demo-ring">Replay the stroke</button></div></div>
  </div>
</section>

{part("IV", "Applications", "The system at work, from the phone screen to the takeout bag.")}

<section class="ch" id="website">{chead("website", "Website", "Five pages built on this system with real menu data, real photos and live Toast links.")}
  <div class="g2" style="align-items:center">
    <figure class="ph" style="margin:0"><img src="img/night.jpg" alt="" loading="lazy"><figcaption>Homepage hero: the ring circles the Nigiri Deluxe tray at every screen size.</figcaption></figure>
    <div class="stack">
      <p><b>Home:</b> hero, live open status, the Lowell rolls, plates with order links, sushi bar vs kitchen, chefs, +Bar, ratings, visit.</p>
      <p><b>Menu:</b> all {n_items} dishes as indexable HTML with section nav, search, "no raw fish" and "spicy" filters, and a direct Toast link on every dish.</p>
      <p><b>Our story, Gallery, Visit:</b> verified facts only, with pitch notes marking every gap for the owners.</p>
      <p class="muted" style="font-size:var(--fs-sm)">Pitch notes can be hidden from the footer for a clean presentation.</p>
      <div>{site_link}</div>
    </div>
  </div>
</section>

<section class="ch" id="social">{chead("social", "Social", "Three templates. Real photos, a cobalt band, one orange note.")}
  <div class="g3" style="align-items:start">
    <div><div class="ig"><img src="img/lobster.jpg" alt="Instagram post template with Lobster Rangoon Maki"><span class="rimline" style="bottom:19cqw"></span><div class="bar"><b>Lobster Rangoon</b><span>$19</span></div></div><p class="mock-cap">Dish post · 1080 × 1080</p></div>
    <div><div class="ig ig--type"><span class="enso ring"></span><h5>The Acre</h5><p>Shrimp tempura, lobster mix, avocado, mango, shrimp, plum sauce, sriracha, fried shallots.</p><span class="p">$18</span></div><p class="mock-cap">Type post · named rolls, specials</p></div>
    <div style="max-width:300px"><div class="ig ig--story"><div class="top"><h5>Open tonight until 9</h5><p>Tuesday to Sunday on Market Street. Order pickup from the link.</p></div><img src="img/tray.jpg" alt="Story template with Nigiri Deluxe"><span class="cta">Order pickup</span></div><p class="mock-cap">Story · 1080 × 1920</p></div>
  </div>
  <p class="muted" style="margin-top:1.5rem">Captions follow the voice in 2.6. Hashtag: #OshareSushiBar. Link in bio goes to the Toast order page, not a delivery app. {C("Handles")}</p>
</section>

<section class="ch" id="print">{chead("print", "Printed menu", "A two-panel table menu: cobalt cover, dense glaze interior with the rim rule.")}
  <div class="desk"><div class="menucard">
    <div class="menucard__cover">{LOCKUP("lockup--white")}<p>350 Market Street · Lowell, MA<br>Sushi bar · Kitchen · Full bar</p></div>
    <div class="menucard__in">
      <div><h6>Signature Maki</h6><div class="r"></div><dl>{''.join(f"<div><dt><span>{e(n)}</span><span>{m(item(n)['p'])}</span></dt><dd>{e(item(n)['d'])}</dd></div>" for n in ["The Acre", "Passion Roll", "Lobster Rangoon Maki", "Red Sox Maki", "Celtic Roll Maki"])}</dl></div>
      <div><h6>From the Kitchen</h6><div class="r"></div><dl>{''.join(f"<div><dt><span>{e(n)}</span><span>{m(item(n)['p'])}</span></dt><dd>{e(item(n)['d'])}</dd></div>" for n in ["Santaka Beef Noodle", "Fried Chicken Bao", "Spicy Beef Bao", "Chicken Karaage", "Katsu Udon"])}</dl></div>
    </div>
  </div></div>
  <p class="muted" style="margin-top:1rem">11 × 17 in folded to 8.5 × 11. Uncoated bright white stock, cobalt as a spot color (nearest Pantone around 7687 C, match on press). {C("Print proof")}</p>
</section>

<section class="ch" id="packaging">{chead("packaging", "Packaging &amp; gift card", "White and cobalt so every pickup bag looks like the porcelain.")}
  <div class="desk"><div class="pack">
    <figure><div class="bag">{LOCKUP()}<div class="band"><p>350 Market St · Lowell</p></div></div><figcaption>Pickup bag · rim band printed in cobalt</figcaption></figure>
    <figure><div class="box"><div class="lid"></div><div class="sleeve"><span class="enso"></span><b>Oshare</b></div></div><figcaption>Sushi box sleeve · one-color cobalt</figcaption></figure>
    <figure><div class="sticks"><div><span class="enso"></span><span class="wordmark"></span></div></div><figcaption>Chopstick sleeve</figcaption></figure>
    <figure><div class="sticker">{LOCKUP()}</div><figcaption>Bag seal sticker · 2 in circle with rim</figcaption></figure>
    <figure><div class="giftcard"><b>Gift card</b><span class="enso"></span><span class="wordmark"></span></div><figcaption>Gift card · works with Toast gift cards</figcaption></figure>
  </div></div>
</section>

{part("V", "Build plan", "How the website gets built, connected to Toast, found on Google, and kept running.")}

<section class="ch field" id="toast">{chead("toast", "Toast integration", "Three levels. We recommend starting at Level 1 at launch and adding Level 2 once Toast access is confirmed.")}
  <div class="ladder">
    <div><span class="lvl">1</span><h3>Branded links {V}</h3><ul><li>Every order button goes to Oshare's Toast ordering page, which handles pickup, delivery, payment and rewards.</li><li>Every dish links to its own Toast item page. These links exist today.</li><li>Toast says its ordering page can't be embedded in another site, so we link instead.</li><li>Gift card link to Toast's gift card page.</li><li><b>Cost:</b> included. <b>Risk:</b> low.</li></ul></div>
    <div><span class="lvl">2</span><h3>Synced menu {C("Toast access")}</h3><ul><li>Toast's read-only standard API access can return the menu (menus v2) for one location.</li><li>Needs Toast's RMS Essentials plan or higher, and a user with the Manage Integrations permission to create credentials.</li><li>WordPress pulls the menu on a schedule, caches it, maps sections, and flags sold-out items.</li><li>Fallback with no API: owners edit the menu in WordPress, with a monthly check against Toast.</li><li><b>Cost:</b> development time; Toast's docs list no API fee, confirm with Toast. <b>Risk:</b> low.</li></ul></div>
    <div><span class="lvl">3</span><h3>Native ordering</h3><ul><li>A cart on osharesushi.com that sends orders into Toast.</li><li>Requires a partner or custom integration approved by Toast, with write access to orders and the credit card API.</li><li>Must handle modifiers, price checks, taxes, payments, stock, hours, voids and refunds.</li><li>Toast does not publish pricing or timelines for this access.</li><li><b>Recommendation:</b> not worth it for one location. Level 1 already gives a branded path to Toast.</li></ul></div>
  </div>
  <p class="muted" style="margin-top:1.5rem;font-size:var(--fs-sm)">Item links open the dish in Toast's ordering page. They don't pre-fill a cart. The links include Toast's item IDs, so the site regenerates them from Toast data and checks them nightly. Sources: Toast Online Ordering FAQ, API overview, standard API access guide and FAQs, ordering integration checklist.</p>
</section>

<section class="ch" id="seo">{chead("seo", "SEO &amp; local search", "Real menu content on Oshare's own domain, consistent business facts everywhere, and structured data that tells search engines and AI assistants exactly what Oshare is.")}
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">URL</th><th scope="col">Title tag</th><th scope="col">Main intent</th></tr></thead><tbody>
    <tr><td>/</td><td>Oshare Sushi + Bar | Sushi, Maki &amp; Cocktails on Market Street, Lowell MA</td><td>sushi Lowell MA, sushi bar Lowell, best sushi Lowell</td></tr>
    <tr><td>/menu/</td><td>Menu | Oshare Sushi + Bar, Lowell MA — Specialty Maki, Nigiri, Noodles</td><td>sushi takeout Lowell, sashimi Lowell, specific dish names</td></tr>
    <tr><td>/about/</td><td>Our Story | Oshare Sushi + Bar, Lowell MA</td><td>brand and chef searches</td></tr>
    <tr><td>/visit/</td><td>Hours &amp; Directions | Oshare Sushi + Bar, 350 Market St, Lowell MA</td><td>hours, parking, "near me", downtown Lowell sushi</td></tr>
    <tr><td>/gallery/</td><td>Gallery | Oshare Sushi + Bar, Lowell MA</td><td>image search, social sharing</td></tr>
  </tbody></table></div>
  <div class="g3" style="margin-top:2rem">
    <div class="rule-top stack"><h3>Structured data</h3><p class="muted">Restaurant (address, hours, cuisine, price range, menu, order action) on every page. Menu with sections, items and prices on /menu/. Breadcrumbs. No review or rating markup: Google doesn't show self-served review stars for local businesses.</p>{V}</div>
    <div class="rule-top stack"><h3>Google Business Profile</h3><p class="muted">Primary category Sushi restaurant, secondary Japanese restaurant and Bar. Hours matching the site. Menu link to /menu/, order link to Toast. Monthly photo uploads from the new shoot.</p>{C("Access")}</div>
    <div class="rule-top stack"><h3>Name consistency</h3><p class="muted">Pick one: "Oshare Sushi + Bar". Fix "Sushi &amp; Bar" and "Sushi Bar" variants and the stale OpenTable hours. Same address and phone format everywhere.</p>{C()}</div>
    <div class="rule-top stack"><h3>AI-ready facts</h3><p class="muted">A plain, factual paragraph on /visit/ with name, address, hours, cuisine, ordering and reservations, plus a short FAQ: parking, reservations, delivery, lunch, raw options.</p>{R}</div>
    <div class="rule-top stack"><h3>Performance</h3><p class="muted">AVIF/WebP photos with set sizes, the hero preloaded, fonts subset to Latin, no page builders, full-page caching. Target: all Core Web Vitals green on mobile.</p>{R}</div>
    <div class="rule-top stack"><h3>Content to add</h3><p class="muted">One post a month: a new roll, the story behind The Acre, a chef profile, game-night specials. Each links to the menu and Toast. No city doorway pages.</p>{R}</div>
  </div>
  <p class="muted" style="margin-top:1.5rem;font-size:var(--fs-sm)">Seed topics (sushi Lowell MA, best sushi Lowell, sushi takeout and delivery Lowell, Japanese restaurant Lowell, sashimi Lowell) are mapped to intent. We did not pull search volumes; add Search Console data after launch.</p>
</section>

<section class="ch" id="wordpress">{chead("wordpress", "WordPress &amp; hosting", "A custom block theme on the same managed stack Jeremy runs for his other clients.")}
  <div class="g2">
    <div class="stack"><h3>Theme</h3><p>A custom block theme. <code>theme.json</code> carries every token in 5.4, so editors can only pick brand colors and sizes.</p><p><b>Templates:</b> front page, menu, page, gallery, visit, single post.</p><p><b>Patterns:</b> hero, Lowell rolls, plates grid, two counters, chefs, +Bar band, ratings, visit block.</p><p><b>Custom blocks:</b> Order button (site-wide Toast URL), Open status (from the hours setting), Menu (server-rendered from synced data), Dish card.</p></div>
    <div class="stack"><h3>Data &amp; editing</h3><p><b>Settings page</b> (ACF options): hours, phone, Toast order URL, gift card URL, social links. Change once, updates everywhere including schema.</p><p><b>Menu:</b> Level 2 sync from Toast into a cached store. Fallback: Menu Item post type with sections, price, raw and spicy flags, edited by staff.</p><p><b>Hosting:</b> Cloudways on DigitalOcean with server and full-page caching, Cloudflare in front, daily backups, uptime monitoring.</p><p><b>Care plan:</b> monthly updates, menu and hours check against Toast, analytics and Search Console report.</p></div>
  </div>
  <div class="tbl-wrap" style="margin-top:2rem"><table class="tbl"><thead><tr><th scope="col">Phase</th><th scope="col">Work</th></tr></thead><tbody>
    <tr><td>1 · Approve</td><td>Owner checklist (5.6), photo license, accounts and access</td></tr>
    <tr><td>2 · Shoot</td><td>Half-day shoot from the shot list in 3.7</td></tr>
    <tr><td>3 · Build</td><td>Block theme, patterns, custom blocks, menu data, schema</td></tr>
    <tr><td>4 · Connect</td><td>Toast links (Level 1), API sync if available (Level 2), Google Business Profile</td></tr>
    <tr><td>5 · Launch</td><td>Redirects from current Toast site URLs, sitemap, Search Console, listing cleanup</td></tr>
  </tbody></table></div>
</section>

<section class="ch" id="tokens">{chead("tokens", "Design tokens", "Copy straight into the theme. These are the values the prototype runs on.")}
  <div class="g2">
    <div><h4>CSS custom properties</h4><div class="code"><button class="chip" type="button" data-copy-code="code-css">Copy</button><pre id="code-css">{e(css_tokens)}</pre></div></div>
    <div><h4>WordPress theme.json</h4><div class="code"><button class="chip" type="button" data-copy-code="code-json">Copy</button><pre id="code-json" style="max-height:520px">{e(theme_json)}</pre></div></div>
  </div>
</section>

<section class="ch" id="assets">{chead("assets", "Asset inventory", "Everything the prototype uses, where it came from, and what's still missing.")}
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col"><span class="sr-only">Preview</span></th><th scope="col">Asset</th><th scope="col">Source</th><th scope="col">Rights</th></tr></thead><tbody>
    <tr><td><img src="assets/lockup-color.svg" alt="" width="48" height="50"></td><td>Logo, traced to vector (ring + wordmark)</td><td>Logotransparency.png on Oshare's Toast site</td><td>{C("Originals")}</td></tr>
    {asset_rows}
    <tr><td></td><td>Menu text and prices ({n_items} items)</td><td>Toast online ordering, captured Oct 8, 2026</td><td>{V}</td></tr>
  </tbody></table></div>
  <h3 style="margin:2rem 0 1rem">Still needed from the owners</h3>
  <div class="g3">
    <div class="panel"><b>Original logo files</b><span class="muted">AI, EPS or SVG, plus any brand fonts used for the wordmark</span></div>
    <div class="panel"><b>Room, bar and chef photos</b><span class="muted">See the shot list in 3.7</span></div>
    <div class="panel"><b>Drinks list</b><span class="muted">Cocktails, beer, sake, wine, non-alcoholic</span></div>
    <div class="panel"><b>Chef bios</b><span class="muted">Full names, background, a few quotes</span></div>
    <div class="panel"><b>Story details</b><span class="muted">Opening year, the name, the Lowell roll names</span></div>
    <div class="panel"><b>Account access</b><span class="muted">Toast, Google Business Profile, domain, social</span></div>
  </div>
</section>

<section class="ch" id="checklist">{chead("checklist", "Owner approval checklist", "Tick items off as they're confirmed. Your ticks are saved in this browser only.")}
  <div class="progress" aria-hidden="true"><i style="width:0"></i></div><p class="muted" data-check-count style="margin-top:.6rem" aria-live="polite"></p>
  <div class="check">{check_html}</div>
</section>

<section class="ch" id="sources">{chead("sources", "Sources")}
  <ol class="sources">{sources_html}</ol>
  <p class="muted" style="margin-top:1.5rem;font-size:var(--fs-sm)">Instagram, Facebook and Yelp pages couldn't be read by our research tools, so nothing in this book is drawn from their content.</p>
</section>

<footer class="bbfoot field"><span>Oshare Sushi + Bar · Brand Book · Proposal, October 2026</span><span>Jeremy Anderson · jeremyanderson.tech</span></footer>
</main>
</div>
<script src="assets/bb.js"></script>
"""
os.makedirs(os.path.join(ROOT, "brand-book"), exist_ok=True)
open(os.path.join(ROOT, "brand-book", "index.html"), "w").write(page)
print("brandbook", len(page))

# design tokens as standalone files for the theme build
tok = os.path.join(ROOT, "design", "tokens"); os.makedirs(tok, exist_ok=True)
open(os.path.join(tok, "tokens.css"), "w").write(css_tokens + "\n")
open(os.path.join(tok, "theme.json"), "w").write(theme_json + "\n")
