#!/usr/bin/env python3
"""Zafra house OG card — v2: new hero + pillar language (JC Nov 22)."""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1200, 630
BG = (12, 18, 14)
GOLD = (201, 169, 110)
CREAM = (242, 237, 227)
MUTED = (205, 198, 184)
F = '/tmp/zafra-deploy/fonts/'
serif = lambda s: ImageFont.truetype(F + 'f2.ttf', s)      # Cormorant Medium
serif_sb = lambda s: ImageFont.truetype(F + 'f1.ttf', s)   # Cormorant SemiBold
sans_r = lambda s: ImageFont.truetype(F + 'f4.ttf', s)     # Inter Regular
sans_sb = lambda s: ImageFont.truetype(F + 'f3.ttf', s)    # Inter SemiBold

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

# --- double gold frame ---
for inset, wd in [(26, 2), (36, 1)]:
    d.rectangle([inset, inset, W - inset, H - inset], outline=GOLD, width=wd)

# --- house shield (nav/footer mark), right side — transparent PNG, no keying ---
seal = Image.open('/Users/santiago/repos/zafra-site/images/zafra-logo-shield.png').convert('RGBA')
SHIELD_W = 520
SHIELD_H = round(SHIELD_W * seal.height / seal.width)   # 1112x898 -> 520x420
seal = seal.resize((SHIELD_W, SHIELD_H), Image.Resampling.LANCZOS)
# centered in the right panel (x 620..1174, y 46..606)
CX, CY = (620 + 1174) // 2, (46 + 606) // 2
img.paste(seal, (CX - SHIELD_W // 2, CY - SHIELD_H // 2), seal)

# --- text block (left) ---
LX = 92
COLW = 520  # max text width — everything must measure under this

def tracked(draw, xy, text, font, fill, track=6):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
    return x

# eyebrow
eb = 'FROM THE CORDILLERA CENTRAL OF PUERTO RICO'
ew = sum(d.textlength(c, font=sans_sb(13)) + 3.5 for c in eb) - 3.5
assert ew <= COLW + 80, f'eyebrow too wide: {ew}'
tracked(d, (LX, 100), eb, sans_sb(13), GOLD, 3.5)
d.rectangle([LX, 132, LX + 64, 133], fill=GOLD)

# headline
h1a, h1b = "Half of Puerto Rico's coffee", 'is never picked. We pick it.'
f_head = None
for size in (72, 66, 60, 54, 48, 44):
    cand = serif_sb(size)
    if all(d.textlength(line, font=cand) <= 505 for line in (h1a, h1b)):
        f_head = cand
        h_size = size
        break
assert f_head is not None, 'headline does not fit at any size'
d.text((LX, 168), h1a, font=f_head, fill=CREAM)
d.text((LX, 168 + int(h_size * 1.18)), h1b, font=f_head, fill=CREAM)

# sub — four harvests + printed price
s1 = 'Shade-grown coffee, canopy honey,'
s2 = 'legacy cacao, heritage vanilla \u2014 four'
s3 = 'harvests off one mountain, farmer-priced.'
f_sub = sans_r(21)
for line in (s1, s2, s3):
    assert d.textlength(line, font=f_sub) <= 505, f'sub too wide: {line}'
d.text((LX, 372), s1, font=f_sub, fill=MUTED)
d.text((LX, 404), s2, font=f_sub, fill=MUTED)
d.text((LX, 436), s3, font=f_sub, fill=MUTED)

# footer
ft = 'ZAFRA TRADING CO. \u2022 SAN JUAN, PUERTO RICO'
fw = sum(d.textlength(c, font=sans_sb(15)) + 5.5 for c in ft) - 5.5
tracked(d, (LX, 518), ft, sans_sb(15), GOLD, 5.5)

img.save('/Users/santiago/repos/zafra-site/images/og-image.jpg', quality=92)
print('card written; footer width', int(fw), 'eyebrow width', int(ew))
