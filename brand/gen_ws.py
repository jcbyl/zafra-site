#!/usr/bin/env python3
"""Williams-Sonoma register: restrained typographic mastheads + small product stamps.
Cream field, Cormorant Garamond serif, hairline rules, gold accents. Vector-only."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_logos import G, SERIF, SANS, glyph_coffee, glyph_orchid, glyph_cacao, glyph_honey

OUT = os.path.dirname(os.path.abspath(__file__))
CREAM = "#faf8f3"; GREEN = "#1a3a24"; DEEP = "#0f2818"
GOLD = "#a8853a"; GOLD_L = "#c4a04a"

def ws_masthead_pure(S=1400):
    """1 — pure type. Zafra title-case serif, tiny spaced caps, one hairline."""
    W, H = S, int(S*0.62)
    cx = W/2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<text x="{cx+3}" y="{H*0.42}" text-anchor="middle" font-family="{SERIF}" font-size="196" font-weight="500" fill="{GREEN}" letter-spacing="6">Zafra</text>
<line x1="{cx-280}" y1="{H*0.50}" x2="{cx+280}" y2="{H*0.50}" stroke="{GOLD}" stroke-width="1.4"/>
<text x="{cx+9}" y="{H*0.60}" text-anchor="middle" font-family="{SANS}" font-size="34" font-weight="500" fill="{GOLD}" letter-spacing="18">TRADING CO.</text>
<text x="{cx+4.5}" y="{H*0.72}" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="400" fill="{GREEN}" letter-spacing="9" opacity=".75">SAN JUAN · PUERTO RICO</text>
</svg>'''

def ws_masthead_stamp(S=1400):
    """2 — small engraved stamp above the wordmark."""
    W, H = S, int(S*0.70)
    cx = W/2
    r = 92
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<circle cx="{cx}" cy="{H*0.26}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="2.4"/>
<circle cx="{cx}" cy="{H*0.26}" r="{r-9}" fill="none" stroke="{GOLD}" stroke-width="0.9"/>
{glyph_coffee(cx, H*0.26, 1.05)}
<text x="{cx+3}" y="{H*0.56}" text-anchor="middle" font-family="{SERIF}" font-size="172" font-weight="500" fill="{GREEN}" letter-spacing="6">Zafra</text>
<text x="{cx+8}" y="{H*0.655}" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="500" fill="{GOLD}" letter-spacing="16">TRADING CO.</text>
<line x1="{cx-240}" y1="{H*0.705}" x2="{cx+240}" y2="{H*0.705}" stroke="{GOLD}" stroke-width="1.2"/>
<text x="{cx+4}" y="{H*0.775}" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="400" fill="{GREEN}" letter-spacing="8" opacity=".75">SAN JUAN · PUERTO RICO</text>
</svg>'''

def ws_masthead_frame(S=1400):
    """3 — hairline double-rule frame, classic label masthead."""
    W, H = S, int(S*0.66)
    cx = W/2
    m = 74
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>
<rect x="{m+9}" y="{m+9}" width="{W-2*m-18}" height="{H-2*m-18}" fill="none" stroke="{GOLD}" stroke-width="0.7"/>
<text x="{cx+3}" y="{H*0.40}" text-anchor="middle" font-family="{SERIF}" font-size="188" font-weight="500" fill="{GREEN}" letter-spacing="6">Zafra</text>
<line x1="{cx-260}" y1="{H*0.475}" x2="{cx-40}" y2="{H*0.475}" stroke="{GOLD}" stroke-width="1.2"/>
<line x1="{cx+40}" y1="{H*0.475}" x2="{cx+260}" y2="{H*0.475}" stroke="{GOLD}" stroke-width="1.2"/>
<text x="{cx}" y="{H*0.485}" text-anchor="middle" font-family="{SERIF}" font-size="30" font-style="italic" font-weight="500" fill="{GOLD}">est.</text>
<text x="{cx+8.5}" y="{H*0.60}" text-anchor="middle" font-family="{SANS}" font-size="32" font-weight="500" fill="{GREEN}" letter-spacing="17">TRADING CO.</text>
<text x="{cx+4}" y="{H*0.70}" text-anchor="middle" font-family="{SANS}" font-size="21" font-weight="400" fill="{GOLD}" letter-spacing="8">SAN JUAN · PUERTO RICO</text>
</svg>'''

def ws_masthead_wide(S=1400):
    """4 — wide letterspaced caps between hairlines, quiet italic descriptor."""
    W, H = S, int(S*0.56)
    cx = W/2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<line x1="{W*0.16}" y1="{H*0.30}" x2="{W*0.84}" y2="{H*0.30}" stroke="{GOLD}" stroke-width="1.4"/>
<text x="{cx+21}" y="{H*0.52}" text-anchor="middle" font-family="{SERIF}" font-size="124" font-weight="600" fill="{GREEN}" letter-spacing="42">ZAFRA</text>
<line x1="{W*0.16}" y1="{H*0.64}" x2="{W*0.84}" y2="{H*0.64}" stroke="{GOLD}" stroke-width="1.4"/>
<text x="{cx}" y="{H*0.79}" text-anchor="middle" font-family="{SERIF}" font-size="42" font-style="italic" font-weight="500" fill="{GOLD}">Trading Co.</text>
<text x="{cx+3.5}" y="{H*0.90}" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="400" fill="{GREEN}" letter-spacing="7" opacity=".7">SAN JUAN · PUERTO RICO</text>
</svg>'''

def product_stamp(name_es, glyph_fn, S=700, glyph_scale=1.35):
    """Small engraved product stamp: gold double ring + glyph, name beneath."""
    cx = S/2; cy = S*0.42; r = S*0.30
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">
<rect width="{S}" height="{S}" fill="{CREAM}"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{DEEP}"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD_L}" stroke-width="3"/>
<circle cx="{cx}" cy="{cy}" r="{r-8}" fill="none" stroke="{GOLD_L}" stroke-width="1" opacity=".8"/>
{glyph_fn(cx, cy, glyph_scale)}
<text x="{cx+5}" y="{cy + r + 74}" text-anchor="middle" font-family="{SERIF}" font-size="52" font-weight="600" fill="{GREEN}" letter-spacing="10">{name_es}</text>
</svg>'''

import subprocess
opts = {
    "ws-masthead-1-pure":   ws_masthead_pure(),
    "ws-masthead-2-stamp":  ws_masthead_stamp(),
    "ws-masthead-3-frame":  ws_masthead_frame(),
    "ws-masthead-4-wide":   ws_masthead_wide(),
    "ws-stamp-cafe":        product_stamp("CAFÉ", glyph_coffee, glyph_scale=1.8),
    "ws-stamp-cacao":       product_stamp("CACAO", glyph_cacao),
    "ws-stamp-miel":        product_stamp("MIEL", glyph_honey),
    "ws-stamp-vainilla":    product_stamp("VAINILLA", glyph_orchid),
    "ws-stamp-chocolate":   product_stamp("CHOCOLATE", glyph_cacao, glyph_scale=1.6),
    "ws-stamp-terroir":     product_stamp("TERROIR", glyph_coffee, glyph_scale=1.6),
}
for name, svg in opts.items():
    open(os.path.join(OUT, name + ".svg"), "w").write(svg)
    w, h = svg.split('viewBox="0 0 ')[1].split('"')[0].split()
    html = f'''<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>body{{margin:0;background:{CREAM};}} img{{width:{w}px;height:{h}px;}}</style></head>
<body><img src="{name}.svg"></body></html>'''
    open(os.path.join(OUT, name + ".html"), "w").write(html)
    print("wrote", name)
print("DONE")
