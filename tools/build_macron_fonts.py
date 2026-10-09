#!/usr/bin/env python3
"""Adds ō / Ō to the brand faces, which ship without them.

  python3 tools/build_macron_fonts.py      (one-off; needs fontTools + brotli)

Neither Shippori Mincho B1 nor Zen Kaku Gothic New has the macron vowels, so "ensō"
fell back to a system font mid-word. This builds two tiny companion families from the
self-hosted Latin files (SIL OFL 1.1 allows derivatives; they get their own names):

  "Oshare Macron Mincho"  500 / 700 / 800   (from Shippori Mincho B1)
  "Oshare Macron Gothic"  400 / 500 / 700   (from Zen Kaku Gothic New)

Each holds only o, O, the macron and composite ō / Ō. The macron is centred over the
letter at the height the font's own dieresis sits on ö / Ö, so it matches the face's
accent placement. oshare.css lists them first in --display / --sans with a
unicode-range of U+014C-014D, so they load only on pages that use those letters.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent
from fontTools.subset import Subsetter, Options

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
JOBS = [("Oshare Macron Mincho", "oshare-macron-mincho", "shippori-mincho-b1", (500, 700, 800)),
        ("Oshare Macron Gothic", "oshare-macron-gothic", "zen-kaku-gothic-new", (400, 500, 700))]


def bbox(font, name):
    g = font["glyf"][name]; g.recalcBounds(font["glyf"])
    return g.xMin, g.yMin, g.xMax, g.yMax


def build(family, slug, src_slug, weight):
    src = os.path.join(FONTS, f"{src_slug}-latin-{weight}-normal.woff2")
    font = TTFont(src)
    cmap = font.getBestCmap()
    o, O, mac, od, Od, dier = (cmap[c] for c in (0x6F, 0x4F, 0xAF, 0xF6, 0xD6, 0xA8))

    # where this face puts an accent over a lowercase and a capital: the dieresis on ö / Ö
    _, d_y0, _, d_y1 = bbox(font, dier)
    _, m_y0, _, m_y1 = bbox(font, mac)
    m_x0, _, m_x1, _ = bbox(font, mac)
    placements = {}
    for base, accented in ((o, od), (O, Od)):
        bx0, _, bx1, _ = bbox(font, base)
        top = bbox(font, accented)[3]
        accent_mid = top - (d_y1 - d_y0) / 2
        dy = round(accent_mid - (m_y0 + m_y1) / 2)
        dx = round((bx0 + bx1) / 2 - (m_x0 + m_x1) / 2)
        placements[base] = (dx, dy)

    opts = Options(); opts.layout_features = []; opts.name_IDs = ["*"]; opts.notdef_outline = True
    opts.glyph_names = True; opts.hinting = False; opts.flavor = "woff2"
    sub = Subsetter(opts); sub.populate(glyphs=[o, O, mac]); sub.subset(font)

    glyf, hmtx = font["glyf"], font["hmtx"]
    for base, name, uni in ((o, "omacron", 0x14D), (O, "Omacron", 0x14C)):
        dx, dy = placements[base]
        g = Glyph(); g.numberOfContours = -1; g.components = []
        for gname, x, y in ((base, 0, 0), (mac, dx, dy)):
            c = GlyphComponent(); c.glyphName = gname; c.x, c.y = x, y; c.flags = 0x200 if gname == base else 0  # USE_MY_METRICS on the base letter
            g.components.append(c)
        glyf[name] = g  # glyf.__setitem__ also appends to the glyph order
        hmtx[name] = hmtx[base]
        if "vmtx" in font: font["vmtx"][name] = font["vmtx"][base]  # the Japanese faces carry vertical metrics too
        for t in font["cmap"].tables:
            if t.isUnicode(): t.cmap[uni] = name
    order = list(glyf.glyphOrder); font.setGlyphOrder(order)
    for n in ("omacron", "Omacron"): glyf[n].recalcBounds(glyf)
    font["maxp"].numGlyphs = len(order)
    if "post" in font: font["post"].formatType = 3.0  # no glyph names needed

    style = {400: "Regular", 500: "Medium", 700: "Bold", 800: "ExtraBold"}[weight]
    name = font["name"]
    for rec in list(name.names):
        if rec.nameID in (1, 2, 3, 4, 6, 16, 17): name.removeNames(nameID=rec.nameID)
    full = f"{family} {style}"
    for nid, val in ((1, family), (2, "Regular"), (3, f"{full}; derived from {src_slug} (SIL OFL 1.1)"), (4, full),
                     (6, full.replace(" ", "")), (16, family), (17, style)):
        name.setName(val, nid, 3, 1, 0x409)
    font.flavor = "woff2"
    out = os.path.join(FONTS, f"{slug}-{weight}-normal.woff2")
    font.save(out)
    return out, placements


if __name__ == "__main__":
    for family, slug, src_slug, weights in JOBS:
        for w in weights:
            out, pl = build(family, slug, src_slug, w)
            print(f"{os.path.basename(out):36} {os.path.getsize(out):>5} B  macron offsets {pl}")
