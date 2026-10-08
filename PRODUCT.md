# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Prototype: static HTML/CSS/vanilla JS (no build step), published as hosted pages for client review. Production target: custom WordPress block theme (theme.json tokens, block patterns, ACF where justified) with Toast retained for ordering. Stated in the client brief; recorded here rather than asked again.

## Users

- **Primary — Lowell locals deciding dinner tonight.** On a phone, often already hungry, comparing "sushi near me." Job: see what's good, confirm it's open, order pickup or walk in. Decision happens in under a minute.
- **Secondary — the planned night out.** Dates, friends, small groups (the menu sells a "Party of 2" set). Job: judge vibe, bar, and whether it's worth the trip downtown.
- **Tertiary — visitors to downtown Lowell** (UMass Lowell, Lowell National Historical Park, events). Job: find a credible, well-reviewed spot nearby.
- **Business audience — the owners.** This is a speculative pitch by Jeremy Anderson (jeremyanderson.tech); the owners are the first audience and must see their real restaurant, not a fantasy brand.

## Product Purpose

A branded home for Oshare Sushi + Bar that out-performs its current Toast template site: make the food and the restaurant's personality legible in seconds, push guests to direct Toast ordering (not third-party delivery apps with marked-up prices), and earn local search visibility with indexable menu content on osharesushi.com.

Success: more direct Toast orders, more walk-ins and calls, ranking for Lowell sushi queries, and a site the owners can maintain in WordPress.

## Positioning

The only sushi bar in Lowell whose menu speaks Lowell. Verified menu items name the city's own references — **The Acre** (Lowell's historic immigrant neighborhood), **Red Sox Maki**, **Celtic Roll** — alongside Korean-leaning kitchen dishes (bulgogi maki, Kogi beef bowl, Santaka noodles, bao). It is a contemporary Japanese-Korean sushi bar with a full bar, at neighborhood prices ($$, most specialty maki $12–22). Competitors in town are Chinese-Japanese combos, buffets, or AYCE; Oshare is the chef-driven one.

## Operating Context

- Ordering: Toast Online Ordering (pickup + delivery), `https://toast.app/r/osharesushibar/order`. Item-level deep links exist on Toast (`/order/item-<slug>_<guid>`). Toast gift cards (`toasttab.com/osharesushibar/giftcards`) and Toast Rewards (1 pt per $1) are live. Third-party: Uber Eats, DoorDash, Grubhub (per their own promo graphic).
- Reservations: none online. OpenTable listing states the restaurant is not on the OpenTable network; guests call (978) 677-2636.
- Current site: Toast-hosted template (Shrikhand + Inter, yellow #F3D535 buttons) — no brand system.

## Capabilities and Constraints

- Verified facts: 350 Market Street, Lowell, MA 01852 · (978) 677-2636 · Hours per restaurant's own site (Oct 8, 2026): Sun 11:30a–9p, Mon closed, Tue–Thu 4–9p, Fri–Sat 11:30a–10p. OpenTable's "daily 11:30–9" is stale.
- Chefs: "Bryan and Son," 30+ years combined experience (About page). No surnames, bios, founding date, or ownership info published.
- Menu: full verified item list with prices captured from Toast on 2026-10-08 (`design/data/menu.json`). Prices change; Toast is the source of truth. Raw/undercooked items marked `*`. No allergen information published.
- Bar: "Full bar" and cocktails confirmed by OpenTable listing and reviews; no cocktail menu published.
- Parking: sources conflict (street only vs. adjacent lot). Unverified.
- Social: Instagram `@osharesushibar` and Facebook `/OshareSushiBar` surface in search under the restaurant name and match the hashtag `#OshareSushiBar` on their own promo graphic; profile contents could not be read (robots blocked). Treat as probable, confirm before linking.
- "Oshare" (おしゃれ) means stylish / fashionable / dressed up. Naming intent unconfirmed — do not tell it as an origin story.

## Brand Commitments

- Existing mark: hand-brushed **orange ensō ring** with a blocky geometric **OSHARE** wordmark and **SUSHI+BAR** subline. Preserve and refine; do not replace.
- Existing photography: professional, consistent shoot — white-grey marble, 3/4 angle, cobalt blue-and-white porcelain bowls, red-rim black lacquer sushi tray, edible flowers.
- Client brief bans: cherry blossoms, samurai imagery, random kanji, red-and-black stereotype palettes, decorative "Asian" patterns without rationale.

## Evidence on Hand

- 4 site photos + 15 menu-item photos on Toast's CDN (signed URLs captured in `assets/menu-data.js` (OSHARE_PHOTOS); local copies in `img/`). Usage rights: the restaurant's own published images; must confirm license with owner before production use.
- Ratings (aggregates only, Oct 2026): Restaurantji 4.8 (68), OpenTable 4.8 (10), Uber Eats 4.9 (27). Review themes: fish quality, presentation, friendly staff, cocktails, relaxed room.
- **No** interior/bar/staff/chef photography, no testimonials with permission, no press coverage found. Never fabricate any of these.

## Product Principles

1. **Real or labeled.** Every fact, price, photo, and claim is verified or visibly marked "confirm with client."
2. **Order is one tap away, everywhere.** Direct Toast ordering beats third-party apps on every page and viewport.
3. **The menu is the content.** Indexable, browsable, beautiful HTML menu — not a PDF, not an iframe.
4. **Lowell, not Tokyo cosplay.** Identity comes from the actual food, tableware, and the city the menu already names.
5. **Owner-maintainable.** Everything maps to WordPress blocks/patterns a restaurant can edit.

## Accessibility & Inclusion

WCAG 2.2 AA. Spice level and raw-fish indicators must not rely on color alone. Respect reduced motion. Phone-first touch targets (≥44px).
