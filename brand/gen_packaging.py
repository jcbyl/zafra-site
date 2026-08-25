#!/usr/bin/env python3
"""Zafra Trading Co. — FINAL packaging line generator.
Spec: product list 2026-08-14 §4 — matte deep forest green, gold foil accents,
engraved seal, SAN JUAN · PUERTO RICO. All products, one family.
"""
import os, math
from gen_logos import (G, SERIF, SANS, arc, sun_rays, sun_disc, ridges,
                       coffee_branch, glyph_coffee, glyph_orchid, glyph_cacao,
                       glyph_honey, diamond, w)

# ── shared label block (gold foil plate) ─────────────────────────
def foil_label(x, y, wd, ht, inner_pad=8):
    return f'''<g>
<rect x="{x}" y="{y}" width="{wd}" height="{ht}" fill="{G["gold"]}"/>
<rect x="{x+5}" y="{y+5}" width="{wd-10}" height="{ht-10}" fill="none" stroke="{G["deep"]}" stroke-width="1.6"/>
<rect x="{x+9}" y="{y+9}" width="{wd-18}" height="{ht-18}" fill="none" stroke="{G["deep"]}" stroke-width="0.8" opacity=".6"/>
</g>'''

def mini_seal(cx, cy, r, ring=True):
    """Compact engraved mark for labels: sun + one ridge + branch hint."""
    scale = r / 98
    g = [f'<g transform="translate({cx} {cy}) scale({scale})">']
    if ring:
        g.append(f'<circle r="98" fill="{G["deep"]}" stroke="{G["gold_d"]}" stroke-width="5"/>')
        g.append(f'<circle r="88" fill="{G["band"]}"/>')
    else:
        g.append(f'<circle r="98" fill="{G["band"]}" stroke="{G["gold_d"]}" stroke-width="5"/>')
    g.append(sun_rays(0, -26, 26, 42, n=12, w=3.6, color=G["gold_l"]))
    g.append(sun_disc(0, -26, 21, G["gold_l"], G["gold"]))
    g.append(ridges(-98, 98, 62, G["mid"], [(-98,8),(-58,-16),(-24,8),(12,-20),(48,6),(78,-12),(98,0),(98,62)]))
    g.append(ridges(-98, 98, 72, "#12241a", [(-98,34),(-46,14),(6,38),(56,16),(98,32),(98,72)]))
    g.append(glyph_coffee(0, 44, 1.5))
    g.append('</g>')
    return "\n".join(g)

# ── pouch (coffee / cacao / green-coffee) ────────────────────────
def pouch(fname, product, sub, extra_glyph, accent_row=None, body=G["band"], valve=True, footer="SAN JUAN · PUERTO RICO"):
    W, H = 420, 640
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Zafra {product} pouch">
<defs>
  <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000" stop-opacity=".22"/>
    <stop offset=".18" stop-color="#000" stop-opacity="0"/>
    <stop offset=".82" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity=".28"/>
  </linearGradient>
</defs>
<!-- body -->
<rect x="40" y="52" width="340" height="548" rx="18" fill="{body}"/>
<!-- top crimp -->
<rect x="34" y="36" width="352" height="34" rx="8" fill="{G["deep"]}"/>
<line x1="44" y1="53" x2="376" y2="53" stroke="{G["gold_d"]}" stroke-width="1" opacity=".7"/>
<line x1="44" y1="60" x2="376" y2="60" stroke="{G["gold_d"]}" stroke-width="0.6" opacity=".4"/>
<!-- bottom gusset -->
<rect x="52" y="586" width="316" height="14" rx="7" fill="{G["deep"]}" opacity=".8"/>
<rect x="40" y="52" width="340" height="548" rx="18" fill="url(#sheen)"/>'''
    if valve:
        s += f'\n<circle cx="96" cy="96" r="7" fill="{G["deep"]}" stroke="{G["gold_d"]}" stroke-width="1.4"/>'
    # label
    lx, ly, lw, lh = 88, 118, 244, 330
    s += foil_label(lx, ly, lw, lh)
    cx = W / 2
    s += f'\n{mini_seal(cx, ly + 92, 62)}'
    s += f'\n<text x="{cx}" y="{ly+206}" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="600" fill="{G["deep"]}" letter-spacing="1.5">{product}</text>'
    s += f'\n<text x="{cx}" y="{ly+240}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" fill="{G["gold_d"]}" letter-spacing="4">{sub}</text>'
    if accent_row:
        s += f'\n<text x="{cx}" y="{ly+272}" text-anchor="middle" font-family="{SERIF}" font-size="17" font-style="italic" font-weight="500" fill="{G["mid"]}">{accent_row}</text>'
    s += f'\n{extra_glyph}'
    s += f'\n<line x1="{lx+34}" y1="{ly+lh-46}" x2="{lx+lw-34}" y2="{ly+lh-46}" stroke="{G["gold_d"]}" stroke-width="1.2"/>'
    s += f'\n<text x="{cx}" y="{ly+lh-20}" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{G["deep"]}" letter-spacing="3.5">{footer}</text>'
    s += '\n</svg>'
    w(fname, s)

# 1. Coffee — Medium Roast 12oz
pouch("pack-coffee-medium.svg", "CAFÉ", "MEDIUM ROAST", glyph_coffee(210, 448, 1.25),
      accent_row="Whole Bean · 12 oz · 100% Puerto Rican Arabica")

# 2. Coffee — Yauco Single-Origin
pouch("pack-coffee-yauco.svg", "CAFÉ", "YAUCO SINGLE-ORIGIN", glyph_coffee(210, 448, 1.25),
      accent_row="Whole Bean · 12 oz · Cordillera Central")

# 3. Cacao nibs
pouch("pack-cacao-nibs.svg", "CACAO", "FERMENTED NIBS", glyph_cacao(210, 448, 1.3),
      accent_row="Single Origin · 8 oz")

# 4. Green coffee — kraft
pouch("pack-coffee-green.svg", "GREEN COFFEE", "UNROASTED", glyph_coffee(210, 448, 1.25),
      accent_row="For Home Roasters · 1 lb", body=G["kraft"], valve=False)

# ── honey hex jar ────────────────────────────────────────────────
def honey_jar():
    W, H = 420, 640
    cx = W / 2
    honey = "#c98a2e"; honey_deep = "#a86e1f"
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Zafra honey jar">
<!-- jar glass: hexagonal silhouette -->
<polygon points="{cx-96},150 {cx-48},112 {cx+48},112 {cx+96},150 {cx+96},540 {cx+48},578 {cx-48},578 {cx-96},540" fill="#e9e4d2" opacity=".55"/>
<!-- honey fill -->
<polygon points="{cx-88},168 {cx-44},134 {cx+44},134 {cx+88},168 {cx+88},534 {cx+44},570 {cx-44},570 {cx-88},534" fill="{honey}"/>
<polygon points="{cx-88},168 {cx-44},134 {cx+44},134 {cx+88},168 {cx+88},300 {cx-88},300" fill="{honey_deep}" opacity=".45"/>
<!-- glass highlights -->
<line x1="{cx-64}" y1="160" x2="{cx-64}" y2="540" stroke="#fff" stroke-width="7" opacity=".35" stroke-linecap="round"/>
<line x1="{cx+58}" y1="170" x2="{cx+58}" y2="530" stroke="#fff" stroke-width="4" opacity=".2" stroke-linecap="round"/>
<!-- gold lid -->
<rect x="{cx-56}" y="76" width="112" height="44" rx="10" fill="{G["gold"]}"/>
<rect x="{cx-56}" y="76" width="112" height="10" fill="{G["gold_l"]}" opacity=".8"/>
<rect x="{cx-50}" y="118" width="100" height="7" fill="{G["gold_d"]}"/>
<ellipse cx="{cx}" cy="118" rx="50" ry="7" fill="{G["gold_d"]}"/>
<!-- green label -->
{foil_label(cx-84, 268, 168, 210)}
{mini_seal(cx, 332, 46)}
<text x="{cx}" y="416" text-anchor="middle" font-family="{SERIF}" font-size="27" font-weight="600" fill="{G["deep"]}" letter-spacing="1.5">MIEL</text>
<text x="{cx}" y="440" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{G["gold_d"]}" letter-spacing="3.5">MOUNTAIN WILDFLOWER</text>
{glyph_honey(cx, 462, 0.62)}
<line x1="{cx-52}" y1="500" x2="{cx+52}" y2="500" stroke="{G["gold_d"]}" stroke-width="1.1"/>
<text x="{cx}" y="518" text-anchor="middle" font-family="{SANS}" font-size="10.5" font-weight="600" fill="{G["deep"]}" letter-spacing="2.6">SAN JUAN · PUERTO RICO</text>
</svg>'''
    w("pack-honey.svg", s)

honey_jar()

# ── vanilla tube ─────────────────────────────────────────────────
def vanilla_tube():
    W, H = 340, 640
    cx = W / 2
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Zafra vanilla tube">
<!-- glass tube -->
<rect x="{cx-46}" y="120" width="92" height="440" rx="14" fill="#e9e4d2" opacity=".55"/>
<!-- vanilla beans inside (3 dark pods) -->
<g stroke="#2a1f14" stroke-width="9" stroke-linecap="round" fill="none">
  <path d="M {cx-24} 530 C {cx-30} 430 {cx-16} 320 {cx-12} 210"/>
  <path d="M {cx+2} 534 C {cx-2} 420 {cx+6} 330 {cx+2} 214"/>
  <path d="M {cx+26} 530 C {cx+30} 440 {cx+18} 330 {cx+16} 212"/>
</g>
<line x1="{cx-32}" y1="150" x2="{cx-32}" y2="530" stroke="#fff" stroke-width="5" opacity=".35" stroke-linecap="round"/>
<!-- gold cap -->
<rect x="{cx-52}" y="72" width="104" height="54" rx="10" fill="{G["gold"]}"/>
<rect x="{cx-52}" y="72" width="104" height="10" fill="{G["gold_l"]}" opacity=".8"/>
<rect x="{cx-46}" y="122" width="92" height="8" fill="{G["gold_d"]}"/>
<!-- green wrap label -->
{foil_label(cx-64, 260, 128, 200)}
{mini_seal(cx, 322, 42)}
<text x="{cx}" y="398" text-anchor="middle" font-family="{SERIF}" font-size="24" font-weight="600" fill="{G["deep"]}" letter-spacing="1.5">VAINILLA</text>
<text x="{cx}" y="420" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="600" fill="{G["gold_d"]}" letter-spacing="3">GRADE A · 3 BEANS</text>
{glyph_orchid(cx, 448, 0.55)}
<line x1="{cx-40}" y1="478" x2="{cx+40}" y2="478" stroke="{G["gold_d"]}" stroke-width="1.1"/>
<text x="{cx}" y="496" text-anchor="middle" font-family="{SANS}" font-size="9.5" font-weight="600" fill="{G["deep"]}" letter-spacing="2.4">SAN JUAN · PUERTO RICO</text>
</svg>'''
    w("pack-vanilla.svg", s)

vanilla_tube()

# ── chocolate bar ────────────────────────────────────────────────
def choc_bar():
    W, H = 620, 430
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Zafra chocolate bar">
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="10" fill="{G["band"]}"/>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="10" fill="none" stroke="{G["gold_d"]}" stroke-width="2"/>
<!-- gold center band -->
<rect x="210" y="16" width="200" height="{H-32}" fill="{G["gold"]}"/>
<rect x="218" y="24" width="184" height="{H-48}" fill="none" stroke="{G["deep"]}" stroke-width="1.4"/>
{mini_seal(310, 128, 52)}
<text x="310" y="216" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="600" fill="{G["deep"]}" letter-spacing="1">CHOCOLATE</text>
<text x="310" y="244" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{G["gold_d"]}" letter-spacing="3.5">70% DARK · SINGLE ORIGIN</text>
<line x1="252" y1="268" x2="368" y2="268" stroke="{G["gold_d"]}" stroke-width="1.1"/>
{glyph_cacao(310, 306, 1.0)}
<text x="310" y="352" text-anchor="middle" font-family="{SANS}" font-size="11" font-weight="600" fill="{G["deep"]}" letter-spacing="2.8">SAN JUAN · PUERTO RICO</text>
<!-- cacao pod engraving left panel -->
{glyph_cacao(112, 215, 1.9, stroke=G["gold_l"])}
<!-- coquí-free leaf motif right panel -->
{glyph_orchid(508, 215, 1.9, stroke=G["gold_l"])}
</svg>'''
    w("pack-chocolate.svg", s)

choc_bar()

# ── PR Terroir gift box ──────────────────────────────────────────
def gift_box():
    W, H = 640, 500
    cx = W / 2
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Zafra PR Terroir gift box">
<!-- box body -->
<rect x="40" y="90" width="560" height="360" rx="10" fill="{G["deep"]}"/>
<rect x="46" y="96" width="548" height="348" rx="8" fill="none" stroke="{G["gold_d"]}" stroke-width="1.6"/>
<!-- lid -->
<rect x="28" y="64" width="584" height="40" rx="8" fill="{G["band"]}"/>
<rect x="28" y="64" width="584" height="40" rx="8" fill="none" stroke="{G["gold_d"]}" stroke-width="1.4"/>
<!-- gold ribbon cross -->
<rect x="{cx-26}" y="64" width="52" height="386" fill="{G["gold"]}"/>
<rect x="28" y="206" width="584" height="40" fill="{G["gold"]}"/>
<rect x="{cx-26}" y="64" width="52" height="386" fill="none" stroke="{G["gold_d"]}" stroke-width="0.8" opacity=".5"/>
<!-- embossed seal -->
{mini_seal(cx, 206 - 92, 66)}
<text x="{cx}" y="{206+76}" text-anchor="middle" font-family="{SERIF}" font-size="34" font-weight="600" fill="{G["cream"]}" letter-spacing="2">PR TERROIR BOX</text>
<text x="{cx}" y="{206+106}" text-anchor="middle" font-family="{SANS}" font-size="13.5" font-weight="500" fill="{G["gold_l"]}" letter-spacing="4">COFFEE · HONEY · VANILLA · CACAO</text>
<line x1="{cx-150}" y1="336" x2="{cx+150}" y2="336" stroke="{G["gold_d"]}" stroke-width="1.2"/>
<text x="{cx}" y="364" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="600" fill="{G["gold_l"]}" letter-spacing="3">SAN JUAN · PUERTO RICO</text>
</svg>'''
    w("pack-giftbox.svg", s)

gift_box()

# ── provenance card ──────────────────────────────────────────────
def provenance_card():
    W, H = 640, 400
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Zafra provenance card">
<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="8" fill="{G["cream"]}" stroke="{G["gold_d"]}" stroke-width="1.6"/>
<rect x="18" y="18" width="{W-36}" height="{H-36}" rx="5" fill="none" stroke="{G["gold_d"]}" stroke-width="0.8" opacity=".7"/>
{mini_seal(84, 84, 44, ring=False)}
<text x="152" y="72" font-family="{SERIF}" font-size="26" font-weight="600" fill="{G["band"]}" letter-spacing="1.5">PROVENANCE</text>
<text x="152" y="98" font-family="{SANS}" font-size="11" font-weight="600" fill="{G["gold_d"]}" letter-spacing="3.5">HARVEST RECORD · ZAFRA TRADING CO.</text>
<line x1="44" y1="130" x2="596" y2="130" stroke="{G["gold_d"]}" stroke-width="1"/>
<g font-family="{SANS}" font-size="13" fill="{G["mid"]}">
<text x="44" y="160" font-weight="600">REGION</text><text x="200" y="160" fill="{G["deep"]}">Yauco · Cordillera Central</text>
<text x="44" y="188" font-weight="600">FARM / CO-OP</text><text x="200" y="188" fill="{G["deep"]}">Areito Cooperative</text>
<text x="44" y="216" font-weight="600">HARVEST</text><text x="200" y="216" fill="{G["deep"]}">Zafra 2026 · January – March</text>
<text x="44" y="244" font-weight="600">ALTITUDE</text><text x="200" y="244" fill="{G["deep"]}">3,900 ft · shade grown</text>
<text x="44" y="272" font-weight="600">VARIETAL</text><text x="200" y="272" fill="{G["deep"]}">Bourbon · Limaní</text>
<text x="44" y="300" font-weight="600">FARMER PRICE</text><text x="200" y="300" fill="{G["deep"]}">Paid direct · above fair-trade floor</text>
</g>
<line x1="44" y1="322" x2="596" y2="322" stroke="{G["gold_d"]}" stroke-width="1"/>
<text x="44" y="350" font-family="{SERIF}" font-size="15" font-style="italic" fill="{G["mid"]}">Every harvest has a home. Every farmer has a name.</text>
<text x="596" y="350" text-anchor="end" font-family="{SANS}" font-size="10" font-weight="600" fill="{G["gold_d"]}" letter-spacing="2.5">SAN JUAN · PR</text>
</svg>'''
    w("pack-provenance.svg", s)

provenance_card()

print("PACKAGING DONE")
