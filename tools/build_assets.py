#!/usr/bin/env python3
"""Runtime copies of the photos and logo files.

  python3 tools/build_assets.py        (tools/build_pages.py runs this first)

img/<name>.jpg     -> img/w/<name>-<width>.avif and .webp at the widths pages ask for.
                      The JPEG stays as the fallback for browsers without AVIF/WebP.
                      img/w/manifest.json records each photo's size and widths for the page builder.
design/logo/*.svg  -> assets/*.svg with path coordinates rounded to whole units and written
                      relative. Same shapes at screen sizes, about half the download.
                      design/logo/ keeps the full-precision masters.

Variants are only re-encoded when the source JPEG is newer, so a normal rebuild
does not need Pillow's AVIF support (Pillow 11.3+); a new or changed photo does.
"""
import os, re, json, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG, OUT = os.path.join(ROOT, "img"), os.path.join(ROOT, "img", "w")
STEPS = (240, 480, 720, 960, 1280, 1600)
AVIF_Q, WEBP_Q = 58, 80


def widths_for(w):
    # skip a step that sits within 10% of the original; the original width is always the top step
    return [s for s in STEPS if s < w * 0.9] + [w]


def build_images():
    from PIL import Image
    os.makedirs(OUT, exist_ok=True)
    manifest, made = {}, 0
    for src in sorted(glob.glob(os.path.join(IMG, "*.jpg"))):
        name = os.path.splitext(os.path.basename(src))[0]
        with Image.open(src) as im:
            W, H = im.size
            ws = widths_for(W)
            manifest[name] = {"w": W, "h": H, "widths": ws}
            todo = [(w, ext) for w in ws for ext in ("avif", "webp")
                    if not os.path.exists(p := os.path.join(OUT, f"{name}-{w}.{ext}")) or os.path.getmtime(p) < os.path.getmtime(src)]
            if not todo: continue
            rgb = im.convert("RGB")
            for w, ext in todo:
                r = rgb if w == W else rgb.resize((w, round(H * w / W)), Image.LANCZOS)
                p = os.path.join(OUT, f"{name}-{w}.{ext}")
                if ext == "avif": r.save(p, "AVIF", quality=AVIF_Q, speed=4)
                else: r.save(p, "WEBP", quality=WEBP_Q, method=6)
                made += 1
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    return made


# ---------- SVG: round to whole units, relative commands ----------
NUM = r"-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"
ARGS = {"M": 2, "L": 2, "C": 6, "Z": 0}


def fmt(nums):
    out = ""
    for n in nums:
        s = str(int(n))
        out += s if (out and s.startswith("-")) or not out else " " + s
    return out


def compact_path(d):
    toks = re.findall(r"[MLCZmlcz]|" + NUM, d)
    if any(t in "mlcz" for t in toks if t.isalpha()):
        return d  # masters are absolute M/L/C/Z; leave anything else untouched
    out, cur, start, cmd, last, i = [], (0, 0), (0, 0), None, None, 0
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]; i += 1
            if cmd == "Z":
                out.append("z"); cur = start; last = None
                continue
        n = ARGS[cmd]
        pts = [(round(float(toks[i + k])), round(float(toks[i + k + 1]))) for k in range(0, n, 2)]; i += n
        rel = [c for x, y in pts for c in (x - cur[0], y - cur[1])]
        letter = cmd.lower()
        if cmd == "M":
            start = pts[-1]; cmd = "L"  # pairs after M are implicit line-tos
        elif not any(rel):
            continue  # segment collapsed to nothing at this precision
        cur = pts[-1]
        body = fmt(rel)
        if letter == last and letter != "m":
            out.append(body if body.startswith("-") else " " + body)
        else:
            out.append(letter + body); last = letter
    return "".join(out)


def build_svgs():
    sizes = []
    for src in sorted(glob.glob(os.path.join(ROOT, "design", "logo", "*.svg"))):
        s = open(src).read()
        t = re.sub(r'\bd="([^"]*)"', lambda m: f'd="{compact_path(m.group(1))}"', s)
        open(os.path.join(ROOT, "assets", os.path.basename(src)), "w").write(t)
        sizes.append((os.path.basename(src), len(s), len(t)))
    return sizes


if __name__ == "__main__":
    for name, a, b in build_svgs():
        print(f"svg  {name:22} {a // 1024:>3} KB -> {b // 1024:>3} KB")
    print(f"img  {build_images()} variants encoded")
