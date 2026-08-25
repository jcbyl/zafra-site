#!/usr/bin/env python3
"""Zafra seals v3 — Areito register: deep green field, gold rings/text, FLUX gold-on-green emblems."""
import os, base64, re

TMP = "/tmp/zafra-fal"
OUT = os.path.expanduser("~/workspace/zafra-site/brand")

GREEN_BG = "#0f2818"; GREEN = "#1a3a24"
GOLD = "#c4a04a"; GOLD_D = "#a8853a"; GOLD_L = "#dab85e"; CREAM = "#e8d4a0"

SERIF = "Cormorant Garamond, Georgia, serif"
SANS = "Inter, Helvetica Neue, Arial, sans-serif"

def arc(cx, cy, r, a0, a1):
    import math
    x0 = cx + r * math.cos(math.radians(a0)); y0 = cy - r * math.sin(math.radians(a0))
    x1 = cx + r * math.cos(math.radians(a1)); y1 = cy - r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if a1 > a0 else 1
    return f"M {x0:.2f} {y0:.2f} A {r} {r} 0 {large} {sweep} {x1:.2f} {y1:.2f}"

def diamond(cx, cy, r, fill=GOLD):
    return f'<path d="M {cx} {cy-r} l {r} {r} l -{r} {r} l -{r} -{r} z" fill="{fill}"/>'

def green_seal(img_href, S=1400, emblem_frac=0.66):
    c = S/2
    e = int(S*emblem_frac/2)
    r_top = c - 58
    r_bot = c - 62
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">
<defs>
  <path id="t-top" d="{arc(c, c, r_top, 180, 0)}"/>
  <path id="t-bot" d="{arc(c, c, r_bot, 180, 360)}"/>
  <clipPath id="emblem-clip"><circle cx="{c}" cy="{c}" r="{e}"/></clipPath>
</defs>
<rect width="{S}" height="{S}" fill="{GREEN_BG}"/>
<circle cx="{c}" cy="{c}" r="{c-18}" fill="none" stroke="{GOLD}" stroke-width="5"/>
<circle cx="{c}" cy="{c}" r="{c-32}" fill="none" stroke="{GOLD_D}" stroke-width="1.8"/>
<text font-family="{SERIF}" font-size="76" font-weight="600" letter-spacing="16" fill="{GOLD_L}">
  <textPath href="#t-top" startOffset="50%" text-anchor="middle">ZAFRA TRADING CO.</textPath>
</text>
<text font-family="{SANS}" font-size="40" font-weight="500" letter-spacing="14" fill="{GOLD}">
  <textPath href="#t-bot" startOffset="50%" text-anchor="middle">SAN JUAN · PUERTO RICO</textPath>
</text>
{diamond(34, c, 16)}{diamond(S-34, c, 16)}
<circle cx="{c}" cy="{c}" r="{e+14}" fill="{GREEN_BG}" stroke="{GOLD}" stroke-width="3"/>
<image href="{img_href}" x="{c-e}" y="{c-e}" width="{2*e}" height="{2*e}"
       preserveAspectRatio="xMidYMid slice" clip-path="url(#emblem-clip)"/>
<circle cx="{c}" cy="{c}" r="{e+14}" fill="none" stroke="{GOLD}" stroke-width="3"/>
</svg>'''

def inline_jpg(svg, path):
    b64 = base64.b64encode(open(os.path.join(TMP, path), "rb").read()).decode()
    return svg.replace(f'href="{path}"', f'href="data:image/jpeg;base64,{b64}"')

opts = {
  "seal-g11": ("g11.jpg", "sun + ridges + coffee branch — the finalized brand motif"),
  "seal-g22": ("g22.jpg", "golden mountains + laurel wreath + red berries"),
  "seal-g31": ("g31.jpg", "crossed cane staffs + sun + palm fronds"),
}

for name, (jpg, _desc) in opts.items():
    frac = 0.60 if jpg == "g11.jpg" else 0.66
    svg = green_seal(jpg, emblem_frac=frac)
    svg = inline_jpg(svg, jpg)
    open(os.path.join(TMP, name + ".svg"), "w").write(svg)
    html = f'''<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>body{{margin:0;background:{GREEN_BG};}} img{{width:1400px;height:1400px;}}</style></head>
<body><img src="{name}.svg"></body></html>'''
    open(os.path.join(TMP, name + ".html"), "w").write(html)
    print("wrote", name)
print("DONE")
