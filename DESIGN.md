---
name: Oshare Sushi + Bar
description: Blue & White — porcelain glaze, underglaze cobalt, one orange brush stroke.
colors:
  cobalt: "#1F3F80"
  cobalt-line: "#2E58A6"
  cobalt-ink: "#1F3F80"
  on-cobalt: "#F3F5F9"
  on-cobalt-secondary: "#B9C9EA"
  enso: "#F25A0A"
  enso-ink: "#A83D08"
  enso-light: "#FF9A5C"
  glaze: "#F3F5F9"
  glaze-recessed: "#E9EDF4"
  wash: "#D9E3F2"
  ink: "#0B1A36"
  ink-secondary: "#3E4D6B"
  band: "#0B1A36"
  ok: "#17703D"
  night-ground: "#0A1630"
  night-ground-recessed: "#0F1E3E"
  night-wash: "#1B305F"
  night-ink: "#EEF2FA"
  night-ink-secondary: "#AFBEDB"
  night-cobalt: "#15306A"
  night-cobalt-line: "#8FAEEA"
  night-on-cobalt-secondary: "#BFD0F0"
  night-enso: "#F46A1E"
  night-enso-ink: "#FF8A45"
  night-band: "#050B1A"
  night-ok: "#6FD39B"
typography:
  display:
    fontFamily: "Oshare Macron Mincho, Shippori Mincho B1, Hiragino Mincho ProN, Yu Mincho, Georgia, serif"
    fontSize: "clamp(2.5rem, 1.5rem + 3.6vw, 5rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Oshare Macron Mincho, Shippori Mincho B1, Hiragino Mincho ProN, Yu Mincho, Georgia, serif"
    fontSize: "clamp(2rem, 1.35rem + 2.4vw, 3.6rem)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Oshare Macron Mincho, Shippori Mincho B1, Hiragino Mincho ProN, Yu Mincho, Georgia, serif"
    fontSize: "clamp(1.3rem, 1.12rem + .7vw, 1.7rem)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Oshare Macron Gothic, Zen Kaku Gothic New, Hiragino Sans, Yu Gothic, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Oshare Macron Gothic, Zen Kaku Gothic New, Hiragino Sans, Yu Gothic, system-ui, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 700
    letterSpacing: "0.12em"
rounded:
  none: "0"
  pill: "999px"
spacing:
  s1: "0.25rem"
  s2: "0.5rem"
  s3: "0.75rem"
  s4: "1rem"
  s5: "1.5rem"
  s6: "2rem"
  s7: "3rem"
  s8: "4rem"
  s9: "6rem"
  s10: "8rem"
components:
  button-primary:
    backgroundColor: "{colors.enso}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.7em 1.35em"
    height: "48px"
  button-primary-small:
    backgroundColor: "{colors.enso}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.5em 1.05em"
    height: "40px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.7em 1.35em"
    height: "48px"
  button-ghost-on-cobalt:
    backgroundColor: "transparent"
    textColor: "{colors.on-cobalt}"
    rounded: "{rounded.pill}"
    padding: "0.7em 1.35em"
    height: "48px"
  chip:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.35rem 0.85rem"
    height: "40px"
  chip-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.glaze}"
    rounded: "{rounded.pill}"
  category:
    backgroundColor: "transparent"
    textColor: "{colors.ink-secondary}"
    rounded: "{rounded.pill}"
    padding: "0.5rem 0.95rem"
  category-active:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.on-cobalt}"
    rounded: "{rounded.pill}"
  mark-raw:
    textColor: "{colors.cobalt-line}"
    rounded: "{rounded.pill}"
    padding: "0.22em 0.45em 0.18em"
  field:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.on-cobalt}"
    rounded: "{rounded.none}"
  field-band:
    backgroundColor: "{colors.band}"
    textColor: "{colors.on-cobalt}"
    rounded: "{rounded.none}"
  photo:
    rounded: "{rounded.none}"
---

# Design System: Oshare Sushi + Bar

## Overview

**Creative North Star: "Blue & White"**

The identity is built from what is already on Oshare's tables: cobalt blue-and-white porcelain bowls, the red-rimmed lacquer tray, white-grey marble, and the restaurant's own hand-brushed orange ensō. Porcelain glaze is the ground, underglaze cobalt owns whole regions, and orange is a single hot stroke per view.

The plate is the hero. Real photography leads; Japanese-foundry typefaces (both drawn with Latin letters) frame it. The system deliberately refuses the dark-and-gold "luxury sushi" page, the zen-minimal blossom page, and all borrowed symbols (kanji, waves, samurai, red-and-black). Identity comes from tableware, the brush ring, and Lowell.

Motion has one authored moment: the ensō paints itself on (a conic mask sweeping 0→360° over 1.7s on an exponential ease-out, `cubic-bezier(.16, 1, .3, 1)`). Everything else is small state feedback, and every element is visible at rest. Reduced motion shows the finished ring. The build is a five-page Persuade surface (site) plus a Read surface (brand book) sharing one stylesheet, `assets/oshare.css`.

**Key Characteristics:**
- Glaze ground, cobalt fields that own whole sections, one orange note per view.
- Real food photography on square corners; never a stock or generated plate.
- Mincho display over a gothic UI face, both Japanese foundry cuts of Latin.
- Flat and tonal: depth from cobalt against glaze, not shadows.
- The rim rule and the traced ensō are the only ornaments.
- A full night palette that keeps the same roles, audited for AA in both themes.

## Colors

Cool porcelain and deep underglaze cobalt carry the page; orange is rationed like the single brush ring it comes from.

### Primary
- **Underglaze Cobalt** (`cobalt`): sampled from the deepest strokes on the bowls. Full-bleed fields (hero copy, Lowell rolls, kitchen counter, visit, footer, page headers) with a faint fractal grain at 7% (5% at night). About 30% of a view. A field color only, never foreground text.
- **Cobalt Ink** (`cobalt-ink`): cobalt used as text, rules and borders on the glaze ground (rating numbers, the rim rule). It lightens to `night-cobalt-line` at night.
- **Cobalt Line** (`cobalt-line`): links, link arrows, the RAW mark, the scrollbar thumb.
- **On Cobalt** (`on-cobalt`) and **On Cobalt Secondary** (`on-cobalt-secondary`): primary and secondary text inside fields (6:1 for the secondary).

### Secondary
- **Ensō Orange** (`enso`): the brush ring, the primary button fill, text selection, the focus ring, the active nav underline. Under 5% of a view. Text on it is always Ink (5.8:1).
- **Ensō Ink** (`enso-ink`): orange as text on glaze (5.8:1 on glaze, 4.9:1 on wash): prices, spicy marks, sold-out labels, pitch notes, the closed-status dot.
- **Ensō Light** (`enso-light`): orange as text on cobalt (4.8:1), such as the hero's "Market Street." Never use `enso` itself as small text.

### Neutral
- **Glaze** (`glaze`): page ground, slightly cool so marble photography reads warm. About 58% of a view.
- **Recessed Glaze** (`glaze-recessed`): photo placeholders, hover fills on category chips, the progress track.
- **Cobalt Wash** (`wash`): diluted cobalt panels such as the sushi guide.
- **Ink** (`ink`): text; never pure black. **Ink Secondary** (`ink-secondary`) for muted text on glaze (6.3:1).
- **Band** (`band`): the deep band behind +Bar and the story gaps. It stays dark in both themes.
- **Positive** (`ok`): the open-now dot and positive state text.

### Night palette
Under `prefers-color-scheme: dark` (unless `data-theme="light"`) and under `[data-theme="dark"]`, the same roles remap to the `night-*` tokens: ground, recessed ground, wash, ink, ink secondary, cobalt fields, cobalt line (which is also cobalt ink at night), on-cobalt secondary, ensō, ensō ink, band and positive. Light text tokens stay light inside fields. Audit both themes with `tools/contrast_audit.js`.

### Named Rules
**The One Hot Note Rule.** Orange appears once per view: the ring, the order button, or one word. Cobalt carries the color load.

**The Field-Is-Not-Ink Rule.** `cobalt` paints fields; `cobalt-ink` and `cobalt-line` paint foreground. Never build a dark band from `ink`, which flips light at night; use `band`.

## Typography

**Display Font:** Shippori Mincho B1 (with Hiragino Mincho ProN, Yu Mincho, Georgia)
**Body Font:** Zen Kaku Gothic New (with Hiragino Sans, Yu Gothic, system-ui)

**Character:** The B1 cut's ink-pooled corners read like cobalt brushed on glaze; the gothic is quiet, upright and legible at menu sizes. Both are self-hosted from `assets/fonts/` (Latin subsets, SIL OFL), with a four-kana subset for the brand book's one Japanese word. Neither face draws ō / Ō, so two tiny companion families ("Oshare Macron Mincho" and "Oshare Macron Gothic", built by `tools/build_macron_fonts.py` from the faces' own o, O and macron, placed at their dieresis height) sit first in each stack and load only where those letters appear.

### Hierarchy
- **Display** (800, `clamp(2.5rem, 1.5rem + 3.6vw, 5rem)`, 1.02, -0.03em): hero and page-header h1s; "The rolls Lowell named" set huge. The brand-book cover and hub run larger, up to 6rem.
- **Headline** (700, `clamp(2rem, 1.35rem + 2.4vw, 3.6rem)`, 1.08): section h2s.
- **Title** (700, `clamp(1.3rem, 1.12rem + .7vw, 1.7rem)`, 1.08): dish names, card titles, h3s. Prices also use the display face (700).
- **Body** (400, 1.0625rem, 1.65): running text at about 65ch; the lead paragraph steps up to `clamp(1.08rem, 1rem + .35vw, 1.3rem)`. UI and nav use 500; buttons 700.
- **Label** (700, 0.78rem, +0.12em, caps): footers and brand-book table heads only.

### Named Rules
**The No-Eyebrow Rule.** Labels never sit above headings. The heading carries its own weight.

**The Tabular Price Rule.** Prices, hours and counts use tabular figures; headings use `text-wrap: balance`.

**The Headline-First Load Rule.** Only Shippori 800 (every page's h1) is preloaded, so headlines don't reflow; body faces swap in without moving the layout.

**The One Face Per Word Rule.** No word mixes typefaces. A letter the brand faces lack gets a companion glyph drawn from their own parts, never a system fallback.

## Layout

- 12-column grid, max width 1320px, fluid gutter `clamp(1rem, .4rem + 2.6vw, 3rem)`, 4px spacing scale (`s1`–`s10`).
- Section padding `clamp(3.5rem, 2rem + 6vw, 8rem)` (tight: `clamp(2.5rem, 1.5rem + 4vw, 5rem)`). More space above headings than below.
- Hero: 11fr cobalt copy column / 13fr photo; the ensō is sized from the photo's rendered scale (`max(58cqw, 81cqh)`) and placed with matching `object-position` (37.5% 48.9%) so it always circles the lacquer tray. At 57.5em and below the hero stacks, photo at its own 1372:984 aspect.
- Page header: cobalt field with a painted ensō bleeding off the right edge (`clamp(240px, 34vw, 520px)`, rotated 12°; at 45em it shrinks to 62vw at 55% opacity).
- Plates grid: one wide plate (8 cols, 5:2 crop) beside a narrow one, then three across; two across at 60em, one column at 37.5em.
- Counters and story splits are two equal columns that stack at 53.75em.
- Menu: two dish columns with hairlines, sticky section chips + search + filters under the header.
- Mobile: sticky header with a short "Order" button; fixed bottom bar (Order pickup / Call / Directions).
- Breakpoints are written in **em** (22.5 / 26.25 / 32.5 / 37.5 / 40 / 45 / 47.5 / 53.75 / 57.5 / 60 / 65em, plus a 30em max-height) so layouts follow the reader's default text size, not just the window width.
- Narrowest phones (22.5em and below): the header shows the compact ensō mark only; the bottom bar stacks icon over label for Call and Directions.
- Menu toolbar on phones is one sticky row: category chips plus a "Search & filter" toggle (a dot means filters are active). Search and filters open beneath it.
- Short viewports (30em tall or less, phones held sideways): the header stops sticking and the bottom bar slims to 44px so content keeps the screen.
- Coarse pointers get 44px minimum targets; hover lift and rings are dropped on touch in favor of press feedback. Horizontal scrollers fade their trailing edge.

## Elevation & Depth

Flat and tonal. Depth comes from cobalt fields against glaze, not shadows. The sticky header is glaze at 92% with a light blur so content reads as passing under it.

### Shadow Vocabulary
- **Float** (`0 18px 40px -22px rgba(11, 26, 54, .45)`; night `0 18px 40px -20px rgba(0, 0, 0, .7)`): floating labels and the open mobile nav only.
- **Rim ring** (`0 0 0 3px <ground>, 0 0 0 4.5px <button color>`): button hover; a ground-colored gap plus a thin outer ring, like a bowl rim. On cobalt the gap is cobalt.

### Named Rules
**The Flat-By-Default Rule.** Surfaces are flat at rest. The only lift is a 1px hover rise on buttons, and it is dropped on touch.

## Shapes

- Photos: square corners, no frames.
- Controls: pills (buttons, chips, status labels, category chips, the RAW mark, pitch notes).
- The ensō: the traced vector of the restaurant's own mark (`assets/enso.svg`, generated from the master in `design/logo/`), used as a CSS mask so it can paint itself.

**The Rim Rule.** A 3px line over a 1px hairline (7px total, `cobalt-ink`; `on-cobalt-secondary` inside fields), like a bowl's painted rim, is the only divider device. As the top edge of a grid or table (ratings, brand-book tables, the Toast ladder, journey and voice grids) it is drawn as a border image, so no grid ever opens with a plain 3px bar.

**The One Ring Rule.** One ensō per view: circling the tray in the hero, bleeding off a page header, or over a hovered plate. It is never repeated as a pattern.

## Components

### Buttons
- **Shape:** full pill (999px), 48px minimum height (40px small, 44px on touch).
- **Primary:** Ensō Orange fill, Ink label at 700, bag icon; padding 0.7em 1.35em.
- **Hover / Focus:** rises 1px and draws the rim ring over 0.25s; focus is a 2.5px orange outline offset 3px (glaze outline inside fields).
- **Ghost:** transparent with a 1.5px inset outline in the text color; on cobalt it turns glaze and rings in `on-cobalt-secondary`.
- **Link arrow:** bold Cobalt Line text with an arrow that nudges up and right on hover.

### Chips
- **Filter chip:** transparent pill with a 1.5px hairline border, 500 weight; pressed (`aria-pressed`) fills Ink with Glaze text.
- **Category chip:** borderless pill in Ink Secondary; hover fills Recessed Glaze; the current category fills Cobalt with glaze text.

### Navigation
- **Header:** sticky, 68px tall, ensō + wordmark on the left, 500-weight links with an orange underline that grows from the left (0.35s), live status and Order pickup on the right. At 57.5em the links and status fold into a 48px round menu button.
- **Bottom order bar (phones):** fixed, three cells — Order pickup (orange, wider), Call, Directions.

### Status
Dot + bold state + detail ("Open now · Until 9 PM tonight"), computed from the hours in America/New_York. Positive dot when open, Ensō Ink when closed; without JavaScript it reads "Open Tue–Sun · Closed Mondays".

### Dish row (menu)
Mincho name, RAW pill and chili marks (never color alone), right-aligned display-face price in Ensō Ink, gothic description, and an "Add to order" link to the Toast item that names the dish for screen readers. Optional 112px photo (84px on the narrowest phones). Sold out: struck price + orange "Sold out today" from the live feed; the prototype's menu is a snapshot, so it dates the flag instead ("Sold out Oct 8").

### Plate card (home)
5:4 photo (5:2 when wide) that scales 3.5% over 1.2s on hover; the ensō fades and turns in over the corner on hover or focus; name + price row, description, order link.

### Photography
Every photo is a `<picture>` with AVIF and WebP sources and the JPEG as fallback; the builders give each image a `sizes` hint for its layout slot, and `tools/build_assets.py` makes the 240–1600px files. Above-the-fold photos load eagerly (the hero with high fetch priority); everything else is lazy. Failed images fall back to the brand ground.

### Icons and share cards
The favicon is the traced ensō in Ensō Orange on transparent (32px); the home-screen icons put it on Cobalt (180 and 192px). Shared links unfurl with 1200×630 cards rendered from each surface's first viewport, without the concept bar, pitch notes or anything time-dependent (the status reads "Open Tue–Sun").

### Pitch note
Dashed orange pill marking facts that need owner confirmation, toggled from the footer. Prototype-only; remove in production.

### Resilience
Every page works without JavaScript: a static status, a visible nav row on phones, and gallery tiles that link to the photos; search, filters, copy and the notes toggle are hidden. Order links that open Toast announce the new tab.

## Do's and Don'ts

### Do:
- **Do** use the restaurant's real photography, real menu text, real prices and real hours; label anything unverified.
- **Do** keep direct Toast ordering visible on every page and viewport.
- **Do** let cobalt own whole sections; keep orange to one note per view.
- **Do** mark raw and spicy with text/icon marks, not color alone.
- **Do** add new photos to `img/` as JPEG, give the `<img>` a `sizes` hint, and rebuild with `python3 tools/build_pages.py`.
- **Do** check new color pairs in both themes with `tools/contrast_audit.js` (AA: 4.5:1 text, 3:1 large text).

### Don't:
- **Don't** use kanji, cherry blossoms, waves, fans, samurai imagery or red-and-black palettes.
- **Don't** put the color lockup on orange, recolor the ring, or stretch the mark.
- **Don't** add eyebrow labels above headings, gradient text, glass panels, or offset block shadows.
- **Don't** embed Toast in an iframe; link to it.
- **Don't** load fonts from Google Fonts or another host; use the self-hosted files in `assets/fonts/`.
- **Don't** edit `assets/*.svg` by hand; change the masters in `design/logo/` and rebuild.
