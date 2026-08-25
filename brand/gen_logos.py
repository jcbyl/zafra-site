#!/usr/bin/env python3
"""Zafra Trading Co. — FINAL logo system + packaging line generator.
Deterministic vector geometry. Palette locked per DESIGN.md + packaging spec §4.
Greens #0f2818 #1a3a24 #245234 #2d6b47 | Golds #a8853a #c4a04a #dab85e #e8d4a0 | Cream #faf8f3
Type: Cormorant Garamond (display) + Inter (functional). NO brown.
"""
import os, math

OUT = os.path.expanduser("~/workspace/zafra-site/brand")
os.makedirs(OUT, exist_ok=True)

G = dict(deep="#0f2818", band="#1a3a24", mid="#245234", leaf="#2d6b47",
         gold_d="#a8853a", gold="#c4a04a", gold_l="#dab85e", gold_p="#e8d4a0",
         cream="#faf8f3", mute="#5a6a5e",
         cherry_d="#a83232", cherry="#c4423a", kraft="#e6d9bd")

SERIF = "Cormorant Garamond, Georgia, serif"
SANS = "Inter, Helvetica Neue, Arial, sans-serif"

def w(name, svg):
    p = os.path.join(OUT, name)
    open(p, "w").write(svg)
    print("wrote", p, len(svg), "bytes")

def arc(cx, cy, r, a0, a1):
    """SVG arc path from angle a0 to a1 (deg, 0=east, CCW positive)."""
    x0 = cx + r * math.cos(math.radians(a0)); y0 = cy - r * math.sin(math.radians(a0))
    x1 = cx + r * math.cos(math.radians(a1)); y1 = cy - r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if a1 > a0 else 1  # CCW => sweep 0 in SVG (y down)
    return f"M {x0:.2f} {y0:.2f} A {r} {r} 0 {large} {sweep} {x1:.2f} {y1:.2f}"

# ─────────────────────────────────────────────────────────────────
# Shared engraved pieces
# ─────────────────────────────────────────────────────────────────
def sun_rays(cx, cy, r_in, r_out, n=12, w=5.0, color="#dab85e"):
    """Radiant engraved sun: rays only (for seal medallion)."""
    out = [f'<g stroke="{color}" stroke-width="{w}" stroke-linecap="round">']
    for i in range(n):
        a = i * 360 / n
        x0 = cx + r_in * math.cos(math.radians(a)); y0 = cy - r_in * math.sin(math.radians(a))
        x1 = cx + r_out * math.cos(math.radians(a)); y1 = cy - r_out * math.sin(math.radians(a))
        out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    out.append("</g>")
    return "\n".join(out)

def sun_disc(cx, cy, r, color="#dab85e", stroke="#c4a04a"):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="{stroke}" stroke-width="2.5"/>')

def ridges(x0, x1, ybase, color, peaks):
    """Mountain ridge polygon. peaks = [(x,peakY)...]"""
    pts = " ".join(f"{x},{y}" for x, y in peaks)
    return f'<path d="M {x0} {ybase} L {pts} L {x1} {ybase} Z" fill="{color}"/>'

def coffee_branch(mirror=False, scale=1.0, stroke="#dab85e", dx=0.0, dy=0.0):
    """Engraved coffee branch: curved stem, 4 leaves, 2 cherry pairs. ~120 wide at scale 1."""
    s = scale
    m = -1 if mirror else 1
    g = [f'<g transform="translate({dx} {dy}) scale({m*s} {s})" stroke="{stroke}" fill="none" stroke-linecap="round">']
    g.append(f'<path d="M -58 26 C -28 18 4 8 34 -8 C 44 -13 52 -19 58 -26" stroke-width="2.6"/>')
    # leaves (filled gold-pale, outlined)
    g.append(f'<path d="M -34 20 q 11 -13 24 -11 q -9 14 -24 11 z" fill="{stroke}" stroke="none"/>')
    g.append(f'<path d="M -12 12 q -11 -12 -24 -8 q 10 13 24 8 z" fill="{stroke}" stroke="none" opacity=".82"/>')
    g.append(f'<path d="M 14 2 q 11 -13 24 -11 q -9 14 -24 11 z" fill="{stroke}" stroke="none"/>')
    g.append(f'<path d="M 34 -8 q -11 -12 -23 -7 q 9 13 23 7 z" fill="{stroke}" stroke="none" opacity=".82"/>')
    # cherry pair A
    g.append(f'<line x1="-8" y1="9" x2="-11" y2="1" stroke-width="1.8"/>')
    g.append(f'<circle cx="-12.5" cy="-3" r="6" fill="#c4423a" stroke="none"/>')
    g.append(f'<line x1="-4" y1="8" x2="0" y2="0" stroke-width="1.8"/>')
    g.append(f'<circle cx="1.5" cy="-4" r="6" fill="#a83232" stroke="none"/>')
    # cherry pair B
    g.append(f'<line x1="22" y1="-4" x2="19" y2="-12" stroke-width="1.8"/>')
    g.append(f'<circle cx="17.5" cy="-16" r="6" fill="#c4423a" stroke="none"/>')
    g.append(f'<line x1="26" y1="-5" x2="30" y2="-13" stroke-width="1.8"/>')
    g.append(f'<circle cx="31.5" cy="-17" r="6" fill="#a83232" stroke="none"/>')
    g.append("</g>")
    return "\n".join(g)

def glyph_coffee(cx, cy, s=1.0, stroke="#dab85e"):
    return f'''<g transform="translate({cx} {cy}) scale({s})" fill="none" stroke="{stroke}" stroke-width="2.4" stroke-linecap="round">
<line x1="0" y1="-14" x2="0" y2="-4"/><line x1="0" y1="-14" x2="-6" y2="-8"/>
<circle cx="-6" cy="-2" r="6.4" fill="#c4423a" stroke="none"/><circle cx="6" cy="0" r="6.4" fill="#a83232" stroke="none"/>
<path d="M 0 4 q 9 -8 18 -6 q -7 9 -18 6 z" fill="{stroke}" stroke="none"/>
</g>'''

def glyph_orchid(cx, cy, s=1.0, stroke="#dab85e"):
    return f'''<g transform="translate({cx} {cy}) scale({s})" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round">
<line x1="0" y1="18" x2="0" y2="4"/>
<path d="M 0 -2 C -10 -4 -14 -12 -12 -18 C -6 -16 -2 -10 0 -4 C 2 -10 6 -16 12 -18 C 14 -12 10 -4 0 -2 Z"/>
<circle cx="0" cy="-9" r="2.6" fill="{stroke}" stroke="none"/>
<path d="M -7 6 q 7 -5 14 0" />
</g>'''

def glyph_cacao(cx, cy, s=1.0, stroke="#dab85e"):
    return f'''<g transform="translate({cx} {cy}) scale({s})" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round">
<line x1="0" y1="-18" x2="0" y2="-11"/>
<path d="M 0 -11 C -9 -8 -10 4 -6 12 C -3 17 3 17 6 12 C 10 4 9 -8 0 -11 Z"/>
<path d="M 0 -8 L 0 13" stroke-width="1.6"/>
</g>'''

def glyph_honey(cx, cy, s=1.0, stroke="#dab85e"):
    hex_pts = lambda r: " ".join(f"{r*math.cos(math.radians(60*i-30)):.1f},{r*math.sin(math.radians(60*i-30)):.1f}" for i in range(6))
    return f'''<g transform="translate({cx} {cy}) scale({s})" fill="none" stroke="{stroke}" stroke-width="2.2">
<polygon points="{hex_pts(7)}" transform="translate(-7.5 4)"/>
<polygon points="{hex_pts(7)}" transform="translate(7.5 4)"/>
<polygon points="{hex_pts(7)}" transform="translate(0 -8)"/>
</g>'''

def diamond(cx, cy, r, fill="#c4a04a"):
    return f'<path d="M {cx} {cy-r} l {r} {r} l -{r} {r} l -{r} -{r} z" fill="{fill}"/>'

# ═════════════════════════════════════════════════════════════════
# 1. THE SEAL — zafra-seal.svg  (480×480)
# ═════════════════════════════════════════════════════════════════
def seal_medallion(cx=240, cy=240, r=142):
    """Sun + three ridges + coffee branch sweeping the lower arc. Family language."""
    x0, x1 = cx - r, cx + r
    ybase = cy + r
    sun_cy = cy - 62
    branch = coffee_branch(scale=1.7, stroke=G["gold_l"], dx=cx, dy=cy + 60)
    return f'''{sun_rays(cx, sun_cy, 38, 64, n=12, w=4.5)}
{sun_disc(cx, sun_cy, 31)}
{ridges(x0, x1, cy + 48, G["mid"], [(x0,cy-2),(x0+42,cy-46),(x0+80,cy-14),(x0+124,cy-58),(x0+170,cy-10),(x0+214,cy-44),(x1,cy-18),(x1,ybase)])}
{ridges(x0, x1, cy + 66, G["band"], [(x0,cy+24),(x0+48,cy-8),(x0+98,cy+26),(x0+148,cy-14),(x0+196,cy+22),(x1,cy-6),(x1,ybase)])}
{ridges(x0, x1, cy + 92, "#12241a", [(x0,cy+52),(x0+62,cy+28),(x0+134,cy+56),(x1,cy+30),(x1,ybase)])}
{branch}'''

def build_seal(dark=False):
    band_fill = G["band"] if not dark else G["deep"]
    bg = f'<rect width="480" height="480" fill="{G["cream"]}"/>' if not dark else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 480" role="img" aria-label="Zafra Trading Co. seal">
<defs>
  <path id="zt-top" d="{arc(240,240,182,180,0)}"/>
  <path id="zt-bot" d="{arc(240,240,180,180,360)}"/>
  <clipPath id="zt-med"><circle cx="240" cy="240" r="142"/></clipPath>
</defs>
{bg}
<circle cx="240" cy="240" r="234" fill="{G["deep"]}" stroke="{G["gold"]}" stroke-width="4"/>
<circle cx="240" cy="240" r="226" fill="none" stroke="{G["gold_d"]}" stroke-width="1.6"/>
<circle cx="240" cy="240" r="216" fill="{band_fill}"/>
<circle cx="240" cy="240" r="150" fill="{G["band"]}" stroke="{G["gold"]}" stroke-width="2.6"/>
<circle cx="240" cy="240" r="142" fill="{G["deep"]}"/>

<!-- band lettering -->
<text font-family="{SERIF}" font-size="33" font-weight="600" letter-spacing="7.5" fill="{G["cream"]}">
  <textPath href="#zt-top" startOffset="50%" text-anchor="middle">ZAFRA TRADING CO.</textPath>
</text>
<text font-family="{SANS}" font-size="16.5" font-weight="500" letter-spacing="6.5" fill="{G["gold_l"]}">
  <textPath href="#zt-bot" startOffset="50%" text-anchor="middle">SAN JUAN · PUERTO RICO</textPath>
</text>
{diamond(240-193, 240, 7)}{diamond(240+193, 240, 7)}

<!-- medallion -->
<g clip-path="url(#zt-med)">
  <rect x="98" y="98" width="284" height="284" fill="{G["deep"]}"/>
  {seal_medallion()}
</g>
<circle cx="240" cy="240" r="142" fill="none" stroke="{G["gold"]}" stroke-width="2.2"/>
</svg>'''
    return svg

w("zafra-seal.svg", build_seal())
w("zafra-seal-on-cream.svg", build_seal(dark=False))

# ═════════════════════════════════════════════════════════════════
# 2. WORDMARK — zafra-wordmark.svg  (900×330, cream bg)
# ═════════════════════════════════════════════════════════════════
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 330" role="img" aria-label="Zafra Trading Co. wordmark">
<rect width="900" height="330" fill="{G["cream"]}"/>
<text x="450" y="172" text-anchor="middle" font-family="{SERIF}" font-size="150" font-weight="600" letter-spacing="26" fill="{G["band"]}">ZAFRA</text>
<g stroke="{G["gold"]}" stroke-width="2.2">
  <line x1="150" y1="216" x2="407" y2="216"/><line x1="493" y1="216" x2="750" y2="216"/>
</g>
{diamond(450, 216, 8)}
<text x="450" y="258" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="600" letter-spacing="18" fill="{G["gold_d"]}">TRADING CO.</text>
<text x="450" y="296" text-anchor="middle" font-family="{SANS}" font-size="15.5" font-weight="500" letter-spacing="7" fill="{G["mute"]}">SAN JUAN · PUERTO RICO</text>
</svg>'''
w("zafra-wordmark.svg", svg)

# ═════════════════════════════════════════════════════════════════
# 3. COMPACT MARK — zafra-mark.svg (sun over ridge, ring)  (240×240)
# ═════════════════════════════════════════════════════════════════
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" role="img" aria-label="Zafra mark">
<circle cx="120" cy="120" r="116" fill="{G["deep"]}" stroke="{G["gold"]}" stroke-width="4"/>
<circle cx="120" cy="120" r="106" fill="none" stroke="{G["gold_d"]}" stroke-width="1.4"/>
<circle cx="120" cy="120" r="98" fill="{G["band"]}"/>
{sun_rays(120, 96, 26, 42, n=12, w=3.6, color=G["gold_l"])}
{sun_disc(120, 96, 21, G["gold_l"], G["gold"])}
{ridges(22, 218, 176, G["mid"], [(22,142),(58,116),(92,140),(128,110),(166,142),(196,120),(218,134),(218,176)])}
{ridges(22, 218, 186, "#12241a", [(22,162),(76,138),(132,166),(184,140),(218,158),(218,186)])}
{coffee_branch(mirror=False, scale=0.62, stroke=G["gold_l"]).replace("<g ", '<g transform="translate(120 214)" ', 1).replace(f'transform="scale(0.62 0.62)"','')}
</svg>'''
# simpler: embed branch with its own translate — rebuild cleanly
branch = coffee_branch(scale=0.62, stroke=G["gold_l"]).replace('transform="scale(0.62 0.62)"', 'transform="translate(120 212) scale(0.62 0.62)"')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" role="img" aria-label="Zafra mark">
<circle cx="120" cy="120" r="116" fill="{G["deep"]}" stroke="{G["gold"]}" stroke-width="4"/>
<circle cx="120" cy="120" r="106" fill="none" stroke="{G["gold_d"]}" stroke-width="1.4"/>
<circle cx="120" cy="120" r="98" fill="{G["band"]}"/>
{sun_rays(120, 96, 26, 42, n=12, w=3.6, color=G["gold_l"])}
{sun_disc(120, 96, 21, G["gold_l"], G["gold"])}
{ridges(22, 218, 176, G["mid"], [(22,142),(58,116),(92,140),(128,110),(166,142),(196,120),(218,134),(218,176)])}
{ridges(22, 218, 186, "#12241a", [(22,162),(76,138),(132,166),(184,140),(218,158),(218,186)])}
{glyph_coffee(120, 184, 1.68)}
</svg>'''
w("zafra-mark.svg", svg)

# ═════════════════════════════════════════════════════════════════
# 4. HORIZONTAL LOCKUP — zafra-lockup.svg (1060×280)
# ═════════════════════════════════════════════════════════════════
mark = build_seal()  # reuse medallion idea via scaled seal
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1060 280" role="img" aria-label="Zafra Trading Co. lockup">
<rect width="1060" height="280" fill="{G["cream"]}"/>
<g transform="translate(16 16) scale(0.933)">
  <image href="zafra-seal-on-cream.svg" x="0" y="0" width="240" height="240"/>
</g>
<text x="820" y="130" text-anchor="middle" font-family="{SERIF}" font-size="112" font-weight="600" letter-spacing="20" fill="{G["band"]}">ZAFRA</text>
<g stroke="{G["gold"]}" stroke-width="2">
  <line x1="560" y1="166" x2="772" y2="166"/><line x1="868" y1="166" x2="1080" y2="166"/>
</g>
{diamond(820, 166, 7)}
<text x="820" y="204" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="600" letter-spacing="14" fill="{G["gold_d"]}">TRADING CO.</text>
<text x="820" y="238" text-anchor="middle" font-family="{SANS}" font-size="13.5" font-weight="500" letter-spacing="6" fill="{G["mute"]}">SAN JUAN · PUERTO RICO</text>
</svg>'''
# image href to file is fragile for standalone; inline the mark instead:
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1060 280" role="img" aria-label="Zafra Trading Co. lockup">
<rect width="1060" height="280" fill="{G["cream"]}"/>
<g transform="translate(12 10) scale(1.05)">
  <circle cx="120" cy="120" r="116" fill="{G["deep"]}" stroke="{G["gold"]}" stroke-width="4"/>
  <circle cx="120" cy="120" r="106" fill="none" stroke="{G["gold_d"]}" stroke-width="1.4"/>
  <circle cx="120" cy="120" r="98" fill="{G["band"]}"/>
  {sun_rays(120, 96, 26, 42, n=12, w=3.6, color=G["gold_l"])}
  {sun_disc(120, 96, 21, G["gold_l"], G["gold"])}
  {ridges(22, 218, 176, G["mid"], [(22,142),(58,116),(92,140),(128,110),(166,142),(196,120),(218,134),(218,176)])}
  {ridges(22, 218, 186, "#12241a", [(22,162),(76,138),(132,166),(184,140),(218,158),(218,186)])}
  {glyph_coffee(120, 184, 1.68)}
</g>
<text x="820" y="130" text-anchor="middle" font-family="{SERIF}" font-size="112" font-weight="600" letter-spacing="20" fill="{G["band"]}">ZAFRA</text>
<g stroke="{G["gold"]}" stroke-width="2">
  <line x1="560" y1="166" x2="772" y2="166"/><line x1="868" y1="166" x2="1080" y2="166"/>
</g>
{diamond(820, 166, 7)}
<text x="820" y="204" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="600" letter-spacing="14" fill="{G["gold_d"]}">TRADING CO.</text>
<text x="820" y="238" text-anchor="middle" font-family="{SANS}" font-size="13.5" font-weight="500" letter-spacing="6" fill="{G["mute"]}">SAN JUAN · PUERTO RICO</text>
</svg>'''
w("zafra-lockup.svg", svg)

print("LOGOS DONE")
