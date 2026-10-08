---
name: Oshare Sushi + Bar
description: Blue & White — porcelain glaze, underglaze cobalt, one orange brush stroke.
colors:
  glaze: "#F3F5F9"
  glaze-recessed: "#E9EDF4"
  wash: "#D9E3F2"
  ink: "#0B1A36"
  ink-secondary: "#3E4D6B"
  cobalt: "#1F3F80"
  cobalt-line: "#2E58A6"
  on-cobalt: "#F3F5F9"
  on-cobalt-secondary: "#B9C9EA"
  enso: "#F25A0A"
  enso-ink: "#A83D08"
  enso-light: "#FF9A5C"
  cobalt-ink: "#1F3F80"
  band: "#0B1A36"
  ok: "#17703D"
  night-ground: "#0A1630"
  night-cobalt: "#15306A"
typography:
  display:
    fontFamily: "Shippori Mincho B1, Yu Mincho, Georgia, serif"
    fontSize: "clamp(2.5rem, 1.5rem + 3.6vw, 5rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Shippori Mincho B1, Yu Mincho, Georgia, serif"
    fontSize: "clamp(2rem, 1.35rem + 2.4vw, 3.6rem)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Shippori Mincho B1, Yu Mincho, Georgia, serif"
    fontSize: "clamp(1.3rem, 1.12rem + .7vw, 1.7rem)"
    fontWeight: 700
    lineHeight: 1.08
  body:
    fontFamily: "Zen Kaku Gothic New, Yu Gothic, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Zen Kaku Gothic New, Yu Gothic, system-ui, sans-serif"
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
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
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
  category-active:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.on-cobalt}"
    rounded: "{rounded.pill}"
  field:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.on-cobalt}"
    rounded: "{rounded.none}"
  photo:
    rounded: "{rounded.none}"
---

# Design System: Oshare Sushi + Bar

## Overview

**North star: Blue & White.** The identity is built from what is already on Oshare's tables: cobalt blue-and-white porcelain bowls, the red-rimmed lacquer tray, white-grey marble, and the restaurant's own hand-brushed orange ensō. Porcelain glaze is the ground, underglaze cobalt owns whole regions, and orange is a single hot stroke per view.

The plate is the hero. Real photography leads; Japanese-foundry typefaces (both drawn with Latin letters) frame it. The system deliberately refuses the dark-and-gold "luxury sushi" page, the zen-minimal blossom page, and all borrowed symbols (kanji, waves, samurai, red-and-black). Identity comes from tableware, the brush ring, and Lowell.

The build is a five-page Persuade surface (site) plus a Read surface (brand book) sharing one stylesheet, `site/assets/oshare.css`.

## Colors

- **Glaze `#F3F5F9`** — page ground, slightly cool so marble photography reads warm. ~58% of a view.
- **Cobalt `#1F3F80`** — sampled from the deepest strokes on the bowls. Full-bleed fields (hero copy, Lowell rolls, kitchen counter, visit, footer) with a faint fractal grain. ~30%.
- **Ensō Orange `#F25A0A`** — the brush ring and the primary button fill. Under 5% of a view. Text on it is always Ink (5.8:1).
- **Ink `#0B1A36`** — text; never pure black. Secondary text `#3E4D6B` on glaze (6.3:1), `#B9C9EA` on cobalt (6:1).
- Orange as text: `#A83D08` on glaze (5.8:1); `#FF9A5C` on cobalt (4.8:1). Never `#F25A0A` as small text.
- **Cobalt Ink `#1F3F80`** — cobalt used as text, rules and borders on the ground. It lightens to `#8FAEEA` in dark mode; never use the `cobalt` field color for foreground.
- **Band `#0B1A36`** — the deep band behind +Bar and the story gaps. It stays dark in both themes (`#050B1A` at night); never build a dark band from the `ink` text token, which flips light in dark mode.
- Night palette (prefers-color-scheme dark and `[data-theme=dark]`): ground `#0A1630`, cobalt fields `#15306A`, ink becomes `#EEF2FA`, cobalt ink `#8FAEEA`, band `#050B1A`, ok `#6FD39B`. Audit both themes with `tools/contrast_audit.js`.

**The One Hot Note rule:** orange appears once per view — the ring, the order button, or one word. Cobalt carries the color load.

## Typography

- **Display / headline / title: Shippori Mincho B1** (500/700/800). The B1 cut's ink-pooled corners read like cobalt brushed on glaze. Hero 800 at up to 5rem, -0.03em; H2 700; dish names 700; prices in display face.
- **Body / UI: Zen Kaku Gothic New** (400/500/700). Menus, descriptions, buttons, labels.
- Labels: 12px caps, 700, +0.12em — used only in footers and brand-book table heads, never above headings.
- Prices and hours use tabular figures. Headings `text-wrap: balance`. Running text ~65ch.

## Layout

- 12-column grid, max width 1320px, fluid gutter `clamp(1rem, .4rem + 2.6vw, 3rem)`, 4px spacing scale.
- Hero: 11fr cobalt copy column / 13fr photo; the ensō is sized from the photo's rendered scale (`max(58cqw, 81cqh)`) and placed with matching `object-position` so it always circles the lacquer tray. Under 920px the hero stacks, photo at fixed aspect.
- Section padding `clamp(3.5rem, 2rem + 6vw, 8rem)`. More space above headings than below.
- Plates grid: one wide plate (8 cols, 5:2 crop) beside a narrow one, then three across; single column under 600px.
- Menu: two dish columns with hairlines, sticky section chips + search + filters under the header.
- Mobile: sticky header with short "Order" button; fixed bottom bar (Order pickup / Call / Directions).
- Breakpoints are written in **em** (26.25 / 37.5 / 45 / 53.75 / 57.5 / 65em) so layouts follow the reader's default text size, not just the window width.
- Narrowest phones (≤ 22.5em): the header shows the compact ensō mark only; the bottom bar stacks icon over label for Call and Directions.
- Menu toolbar on phones is one sticky row: category chips plus a "Search & filter" toggle (dot = filters active). Search and filters open beneath it.
- Short viewports (≤ 30em tall, phones held sideways): the header stops sticking and the bottom bar slims to 44px so content keeps the screen.
- Coarse pointers get 44px minimum targets; hover lift and rings are dropped on touch in favor of press feedback. Horizontal scrollers fade their trailing edge.

## Elevation & Depth

Flat and tonal. Depth comes from cobalt fields against glaze, not shadows. One soft shadow token (`0 18px 40px -22px rgba(11,26,54,.45)`) for floating labels and the open mobile nav. Hover on buttons draws a glaze gap ring plus a 1.5px outer ring in the button's color, echoing a bowl rim.

## Shapes

- Photos: square corners, no frames.
- Controls: pills (buttons, chips, status labels, category chips).
- **The rim rule:** a 3px line over a 1px hairline, like a bowl's painted rim — the only divider device.
- **The ensō:** traced vector of the restaurant's own mark (`enso.svg`), used as a CSS mask so it can paint itself; circles one thing per view.

## Components

- **Primary button** — orange pill, ink label, bag icon; hover lifts 1px and rings.
- **Ghost button** — transparent pill with 1.5px inset outline; on cobalt it turns glaze.
- **Status** — dot + bold state + detail ("Open now · Until 9 PM tonight"), computed from hours in America/New_York.
- **Dish row (menu)** — mincho name, RAW pill and chili marks (never color alone), right-aligned display-face price, gothic description, "Add to order" link to the Toast item. Optional 112px photo. Sold-out: struck price + orange "Sold out today".
- **Plate card (home)** — 5:4 photo (5:2 when wide), ensō fades in on hover/focus, name + price row, description, order link.
- **Rim rule**, **cobalt field**, **page header** (cobalt field with a painted ensō bleeding off the right edge).
- **Pitch note** — dashed orange pill marking facts that need owner confirmation; toggled from the footer. Prototype-only; remove in production.

## Do's and Don'ts

- Do use the restaurant's real photography, real menu text, real prices and real hours; label anything unverified.
- Do keep direct Toast ordering visible on every page and viewport.
- Do let cobalt own whole sections; keep orange to one note per view.
- Do mark raw and spicy with text/icon marks, not color alone.
- Don't use kanji, cherry blossoms, waves, fans, samurai imagery or red-and-black palettes.
- Don't put the color lockup on orange, recolor the ring, or stretch the mark.
- Don't add eyebrow labels above headings, gradient text, glass panels, or offset block shadows.
- Don't embed Toast in an iframe; link to it.
