# Oshare Concept 1 · Blue & White

Brand book and website prototype for **Oshare Sushi + Bar**, 350 Market Street, Lowell, MA.
A spec concept by Jeremy Anderson ([jeremyanderson.tech](https://jeremyanderson.tech)), October 2026.

**Live:** https://cptnope.github.io/Oshare-Concept-1/

| Page | Path |
|---|---|
| Concept hub | [`/`](https://cptnope.github.io/Oshare-Concept-1/) |
| Brand Book | [`/brand-book/`](https://cptnope.github.io/Oshare-Concept-1/brand-book/) |
| Site Prototype | [`/site/`](https://cptnope.github.io/Oshare-Concept-1/site/) (Home, Menu, Our Story, Gallery, Visit) |

Every page shares a top bar for moving between the hub, the brand book and the prototype.

## What's in the repo

```
index.html            concept hub
brand-book/           brand book (research, strategy, identity, applications, build plan)
site/                 five-page website prototype
assets/               shared CSS, JS, runtime logo files and self-hosted fonts (assets/fonts, SIL OFL)
img/                  the restaurant's published photography (JPEG fallbacks)
img/w/                AVIF + WebP copies at 240–1600px wide, picked per screen by srcset
PRODUCT.md            product truth: users, positioning, verified facts, open questions
DESIGN.md             the Blue & White design system (tokens + rules)
.impeccable/          design-tool context (config, design.json sidecar, direction contract)
design/
  direction-contract.md   the direction the build was held to
  design.json             machine-readable design system sidecar
  tokens/tokens.css       CSS custom properties
  tokens/theme.json       WordPress block theme tokens
  logo/                   vector logo family + the original PNG it was traced from
  data/menu.json          124 menu items, prices and Toast item links (captured Oct 8, 2026)
tools/
  build_pages.py          regenerates index.html, brand-book/ and site/
  build_assets.py         image sizes (AVIF/WebP) and compact runtime SVGs; run by build_pages.py
  build_macron_fonts.py   one-off: adds ō / Ō to the brand fonts as small companion files (needs fontTools + brotli)
  build_site.py           site prototype templates
  build_brandbook.py      brand book template
  shoot.js                Playwright screenshot helper used for visual QA
```

## Rebuild

The pages are plain static HTML, and GitHub Pages serves them as-is. To regenerate after editing data or templates:

```sh
python3 tools/build_pages.py
```

Edit `design/data/menu.json` to change dishes or prices, then rebuild.

New or replaced photos go in `img/` as JPEG. The rebuild encodes their AVIF and WebP sizes into `img/w/`, which needs Pillow 11.3 or newer (`pip install -U pillow`). Logo masters live in `design/logo/`; the copies in `assets/` are generated from them with rounded coordinates.

## GitHub Pages

Settings → Pages → **Deploy from a branch** → `main` / `(root)`. The `.nojekyll` file makes Pages serve every file as-is.

## Notes

- Food photography and the logo belong to Oshare Sushi + Bar and are used for this proposal; usage permission is still to be confirmed with the owners.
- Menu, prices and hours were captured from the restaurant's own site and Toast ordering page on October 8, 2026.
- Orange dashed "pitch notes" on the prototype mark facts the owners still need to confirm. Hide them from the prototype footer for a clean presentation.
- Ordering buttons link to the restaurant's live Toast ordering page. Nothing on this site takes orders or payments.
- Sharing: each page carries an absolute `og:image` (1200×630 cards in `img/share/`) and `og:url` on GitHub Pages, so links unfurl in Slack, iMessage and email. Set `PAGES_URL` when rebuilding for another host. The favicon is the orange ensō.
- Performance: photos are served as AVIF/WebP at the width each layout slot needs, fonts are self-hosted (no Google Fonts requests), and only the headline face is preloaded.
- Every page carries `noindex, nofollow` and no canonical link, so search engines leave this concept alone. `tools/build_pages.py` adds both on every rebuild; remove `private_preview()` there if the concept ever should be indexed.
