#!/usr/bin/env python3
"""Builds the GitHub Pages site for Oshare Concept 1.

  python3 tools/build_pages.py

Outputs (all static, no build step on GitHub):
  index.html          concept hub
  brand-book/         the brand book
  site/               the five-page website prototype
Shared files live in assets/ and img/. Menu data: design/data/menu.json.
"""
import os, re, subprocess, sys, html, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/CptNope/Oshare-Concept-1"
e = html.escape

env = dict(os.environ, SITE_URL="../site/")
for script in ("build_assets.py", "build_site.py", "build_brandbook.py"):
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", script)], check=True, env=env, stdout=subprocess.DEVNULL)

ARROW = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'

def concept_bar(prefix, current):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return (f'<nav class="concept" aria-label="Oshare concept"><div class="concept__in">'
            f'<a class="concept__home" href="{prefix or "./"}"{" aria-current=\"page\"" if current == "home" else ""}><span class="enso" aria-hidden="true"></span><span>Oshare <span class="t">Concept 1</span></span></a>'
            f'<div class="concept__links">{link(prefix + "brand-book/", "Brand Book", "book")}{link(prefix + "site/", "Site Prototype", "site")}'
            f'{link(prefix + "#design-files", "Design Files", "files")}<a class="ext" href="{REPO}" rel="noopener">GitHub{ARROW}</a></div></div></nav>')

NOINDEX = '<meta name="robots" content="noindex, nofollow">'
JSFLAG = '<script>document.documentElement.classList.add("js")</script>'

def private_preview(s):
    """Keep the concept out of search: no canonical pointing at the real osharesushi.com, and noindex on every page."""
    s = re.sub(r'<link rel="canonical"[^>]*>\n?', '', s)
    if NOINDEX not in s:
        s = re.sub(r'(<meta name="viewport"[^>]*>)', r'\1\n' + NOINDEX, s, count=1)
    if JSFLAG not in s:
        s = s.replace(NOINDEX, NOINDEX + "\n" + JSFLAG, 1)
    return s

NEWTAB = '<span class="sr-only"> (opens in a new tab)</span>'
def announce_new_tabs(s):
    """Screen readers hear when a link leaves for Toast, Google Maps or GitHub."""
    def fix(m):
        tag, inner = m.group(1), m.group(2)
        return m.group(0) if NEWTAB in inner else f"{tag}{inner}{NEWTAB}</a>"
    return re.sub(r'(<a\b[^>]*target="_blank"[^>]*>)(.*?)</a>', fix, s, flags=re.S)

import hashlib
def _ver(name):
    try: return hashlib.sha1(open(os.path.join(ROOT, "assets", name), "rb").read()).hexdigest()[:8]
    except OSError: return ""

def bust(s):
    """Version-stamp CSS/JS links so browsers pick up changes right after a deploy."""
    return re.sub(r'((?:href|src)="(?:\.\./)?assets/)([\w.-]+\.(?:css|js))"', lambda m: f'{m.group(1)}{m.group(2)}?v={_ver(m.group(2))}"', s)

# ---- performance: self-hosted fonts + responsive images
GOOGLE_FONTS = re.compile(r'<link rel="(?:preconnect|stylesheet)" href="https://fonts\.(?:googleapis|gstatic)\.com[^"]*"[^>]*>\s*')
PRELOAD = ("shippori-mincho-b1-latin-800-normal.woff2",)  # the h1 face; body text swaps in without moving the layout

def self_host_fonts(s):
    """Fonts come from assets/fonts/ (declared in oshare.css); the h1 face is preloaded.
    Also drops any Google Fonts link a template might bring back."""
    s = GOOGLE_FONTS.sub("", s)
    def pre(m):
        links = "".join(f'<link rel="preload" href="{m.group(2)}fonts/{f}" as="font" type="font/woff2" crossorigin>\n' for f in PRELOAD)
        return links + m.group(1)
    return re.sub(r'(<link rel="stylesheet" href="((?:\.\./)?assets/)oshare\.css)', pre, s, count=1)

MANIFEST = json.load(open(os.path.join(ROOT, "img", "w", "manifest.json")))
IMG = re.compile(r'<img\b[^>]*?\bsrc="((?:\.\./)?)img/([\w-]+)\.jpg"[^>]*>')

def responsive(s):
    """Every photo becomes <picture> with AVIF and WebP srcsets; the JPEG stays as the fallback.
    The builders mark each <img> with a sizes hint for its layout slot (default 100vw)."""
    def fix(m):
        tag, pre, name = m.group(0), m.group(1), m.group(2)
        info = MANIFEST.get(name)
        if not info or "<picture" in s[max(0, m.start() - 9):m.start()]: return tag
        sm = re.search(r'\ssizes="([^"]*)"', tag)
        sizes = sm.group(1) if sm else "100vw"
        tag = re.sub(r'\ssizes="[^"]*"', "", tag)
        if not re.search(r'\swidth="', tag):
            tag = tag.replace("<img", f'<img width="{info["w"]}" height="{info["h"]}"', 1)
        if 'decoding="' not in tag and "fetchpriority" not in tag:
            tag = tag.replace("<img", '<img decoding="async"', 1)
        srcset = lambda ext: ", ".join(f"{pre}img/w/{name}-{w}.{ext} {w}w" for w in info["widths"])
        return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
                f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">{tag}</picture>')
    return IMG.sub(fix, s)

def perf(s):
    return responsive(self_host_fonts(s))

def rewrite_paths(s):
    s = re.sub(r'((?:href|src)=")(assets|img)/', r'\1../\2/', s)
    return s.replace("url(img/", "url(../img/")

def shell(body, title_fallback, desc):
    has_title = "<title>" in body[:4000]
    head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + ("" if has_title else f"<title>{e(title_fallback)}</title>\n")
            + (f'<meta name="description" content="{e(desc)}">\n' if desc else ""))
    # move <title>/<meta>/<link> lines that open the body into <head>
    lead = re.match(r'((?:\s*<(?:title|meta|link)[^>]*>(?:[^<]*</title>)?\s*)+)', body)
    if lead:
        head += lead.group(1).strip() + "\n"; body = body[lead.end():]
    return head + "</head>\n<body>\n" + body.strip() + "\n</body>\n</html>\n"

def inject_bar(s, bar):
    # right after the skip link so keyboard users can still skip straight to content
    return re.sub(r'(<a class="skip" href="#main">Skip to content</a>)', r'\1\n' + bar.replace("\\", "\\\\"), s, count=1)

# ---- site pages: already full documents
site_dir = os.path.join(ROOT, "site")
for f in sorted(os.listdir(site_dir)):
    if not f.endswith(".html"): continue
    p = os.path.join(site_dir, f); s = open(p).read()
    s = rewrite_paths(s)
    s = inject_bar(s, concept_bar("../", "site"))
    open(p, "w").write(bust(perf(private_preview(announce_new_tabs(s)))))

# ---- brand book: content-only page -> full document
bp = os.path.join(ROOT, "brand-book", "index.html")
s = rewrite_paths(open(bp).read())
s = s.replace('href="../site/" target="_blank" rel="noopener"', 'href="../site/"')
s = inject_bar(s, concept_bar("../", "book"))
open(bp, "w").write(bust(perf(private_preview(announce_new_tabs(shell(s, "Oshare Brand Book", ""))))))

# ---- hub
FILES = [
    ("PRODUCT.md", "Product truth: users, positioning, verified facts and open questions."),
    ("DESIGN.md", "The Blue & White design system: tokens, type, layout, components, do's and don'ts."),
    ("design/direction-contract.md", "The chosen direction and first-viewport contract the build was held to."),
    ("design/design.json", "Machine-readable design system sidecar: ramps, motion, components."),
    ("design/tokens/tokens.css", "CSS custom properties for the theme."),
    ("design/tokens/theme.json", "WordPress block theme tokens."),
    ("design/logo", "Vector logo family traced from the restaurant's mark, plus the original PNG."),
    ("design/data/menu.json", "All menu items, prices and Toast item links, captured Oct 8, 2026."),
    ("tools", "Python builders that regenerate every page from the data."),
]
files_rows = "".join(f'<li><a href="{REPO}/{"tree" if "." not in os.path.basename(p) else "blob"}/main/{p}" rel="noopener"><code>{e(p)}</code>{ARROW}</a><span>{e(d)}</span></li>' for p, d in FILES)

hub = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Oshare Concept 1</title>
<meta name="description" content="Brand book and website prototype for Oshare Sushi + Bar, Lowell MA. A spec concept by Jeremy Anderson.">
<meta property="og:title" content="Oshare Concept 1 · Blue & White">
<meta property="og:description" content="Brand book and website prototype for Oshare Sushi + Bar, Lowell MA.">
<meta property="og:image" content="img/preview-site.jpg">
<meta name="theme-color" content="#1F3F80">
<link rel="stylesheet" href="assets/oshare.css">
<link rel="stylesheet" href="assets/hub.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{concept_bar("", "home")}
<main id="main">
  <header class="hub-hero field">
    <div class="wrap hub-hero__in">
      <div class="hub-hero__copy">
        <h1>Concept 1 <span>Blue &amp; White</span></h1>
        <p>A brand book and a five-page website prototype for Oshare Sushi + Bar, 350 Market Street, Lowell. Built from the restaurant's own cobalt porcelain, its orange brush ring, and a menu that names Lowell.</p>
        <div class="hero__cta"><a class="btn" href="brand-book/">Open the Brand Book</a><a class="btn btn--ghost" href="site/">Open the Site Prototype</a></div>
        <p class="hub-meta">Spec pitch by Jeremy Anderson · jeremyanderson.tech · October 2026</p>
      </div>
      <div class="hub-lockup" aria-hidden="true"><span class="enso paint"></span><span class="wordmark"></span></div>
    </div>
  </header>

  <section class="sec" aria-label="Explore">
    <div class="wrap hub-cards">
      <a class="hub-card" href="brand-book/">
        <span class="hub-card__img"><img src="img/preview-brand-book.jpg" alt="Brand book cover in cobalt with the orange ensō" width="1200" height="750" loading="lazy" sizes="(max-width: 47.5em) 100vw, (min-width: 82.5em) 600px, 46vw"></span>
        <span class="hub-card__body"><b>Brand Book</b><span>Discovery, strategy, identity, applications and the build plan: Toast integration, SEO, WordPress, tokens, asset inventory and the owner checklist.</span><span class="link-arrow">Read it{ARROW}</span></span>
      </a>
      <a class="hub-card" href="site/">
        <span class="hub-card__img"><img src="img/preview-site.jpg" alt="Website homepage with the ensō circling a tray of nigiri" width="1200" height="750" loading="lazy" sizes="(max-width: 47.5em) 100vw, (min-width: 82.5em) 600px, 46vw"></span>
        <span class="hub-card__body"><b>Site Prototype</b><span>Home, Menu, Our Story, Gallery and Visit. Real photos, all 124 dishes with Toast order links, live open-now status.</span><span class="link-arrow">Explore it{ARROW}</span></span>
      </a>
    </div>
  </section>

  <section class="sec field" id="design-files" aria-labelledby="files-h">
    <div class="wrap hub-files">
      <div class="sec-head"><h2 id="files-h">Design files</h2><p>Everything behind the concept, in the repository.</p></div>
      <ul class="hub-list" role="list">{files_rows}</ul>
    </div>
  </section>

  <section class="sec sec--tight">
    <div class="wrap hub-notes">
      <p><b>About this concept.</b> Food photography and the logo belong to Oshare Sushi + Bar and are used here for a proposal, with permission still to be confirmed. Menu, prices and hours were captured from public sources on October 8, 2026. Orange dashed notes on the prototype mark facts the owners still need to confirm; they can be hidden from the site footer.</p>
    </div>
  </section>
</main>
</body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(bust(perf(private_preview(hub))))
print("built: index.html, brand-book/index.html, site/*.html")
