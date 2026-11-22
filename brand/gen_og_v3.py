#!/usr/bin/env python3
"""Zafra house OG card — v3 (JC Nov 22): full-bleed hero photo + house shield.
Kills the old logo-showcase card. Also writes og-image.jpg (same bytes) so
stale page caches pointing at the old URL serve the new design too."""
from PIL import Image, ImageDraw, ImageFont, ImageStat

W, H = 1200, 630
GOLD = (201, 169, 110)
CREAM = (242, 237, 227)
F = '/tmp/zafra-deploy/fonts/'
serif_sb = lambda s: ImageFont.truetype(F + 'f1.ttf', s)   # Cormorant SemiBold
sans_sb = lambda s: ImageFont.truetype(F + 'f3.ttf', s)    # Inter SemiBold

# --- hero photo: cover-crop 1600x893 -> 1200x630 (keep the land, trim sky) ---
src = Image.open('/Users/santiago/repos/zafra-site/images/hero-zafra.jpg')
sw, sh = src.size                      # 1600x893
target_ratio = W / H                   # 1.9048
crop_h = round(sw / target_ratio)      # 840
y0 = 40                                # trim sky-side, keep mountain+land
img = src.crop((0, y0, sw, y0 + crop_h)).resize((W, H), Image.Resampling.LANCZOS).convert('RGB')

# --- bottom scrim: black gradient, opaque at bottom edge, gone by ~42% height ---
scrim = Image.new('L', (1, H), 0)
for y in range(H):
    t = (y - int(H * 0.30)) / (H * 0.70)
    scrim.putpixel((0, y), int(255 * min(1.0, max(0.0, t) / 0.45) ** 0.9))
img.paste(Image.new('RGB', (W, H), (8, 12, 9)), (0, 0), scrim.resize((W, H)))
d = ImageDraw.Draw(img)

# --- house shield, bottom-left ---
seal = Image.open('/Users/santiago/repos/zafra-site/images/zafra-logo-shield.png').convert('RGBA')
SW = 300
seal = seal.resize((SW, round(SW * seal.height / seal.width)), Image.Resampling.LANCZOS)
LX, LY = 92, H - 78 - seal.height
img.paste(seal, (LX, LY), seal)

# --- text block, right of the shield ---
TX = LX + SW + 56

def tracked(xy, text, font, fill, track=5):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return x - track

# headline (rotating hero variant A) + its gold line
h1a, h1b, h1c = 'Before Kona grew a single bean,', "Puerto Rico\u2019s mountains", 'were covered in coffee.'
gold_line = 'Now it\u2019s finally leaving the island.'
f_head = None
for size in (44, 40, 36, 32):
    cand = serif_sb(size)
    if all(d.textlength(line, font=cand) <= W - TX - 64 for line in (h1a, h1b, h1c)):
        f_head, h_size = cand, size
        break
assert f_head, 'headline does not fit'
hy = LY + 10
d.text((TX, hy), h1a, font=f_head, fill=CREAM)
d.text((TX, hy + round(h_size * 1.22)), h1b, font=f_head, fill=CREAM)
d.text((TX, hy + round(h_size * 2.44)), h1c, font=f_head, fill=CREAM)
gy = hy + round(h_size * 2.44) + round(h_size * 0.42)
d.text((TX, gy), gold_line, font=serif_sb(round(h_size * 0.62)), fill=GOLD)

# footer caps
ft = 'ZAFRA TRADING CO. \u2022 SAN JUAN, PUERTO RICO'
fw = tracked((TX, gy + round(h_size * 0.85) + 14), ft, sans_sb(15), GOLD, 5.5)

# --- thin gold frame, house style ---
d.rectangle([18, 18, W - 19, H - 19], outline=GOLD, width=1)

img.save('/Users/santiago/repos/zafra-site/images/og-card.jpg', quality=92)
img.save('/Users/santiago/repos/zafra-site/images/og-image.jpg', quality=92)

# --- numeric QA (measured, not eyeballed) ---
g = img.convert('L')
band = g.crop((TX, hy, TX + int(d.textlength(h1a, font=f_head)), gy + round(h_size * 0.8)))
m = ImageStat.Stat(band).mean[0]
contrast = (242 + 0.05) / (m + 0.05)          # cream vs local bg
print(f'headline size {h_size}px | footer right edge {int(fw)} (limit {W - 64}) | '
      f'text-zone luminance {m:.1f} | cream contrast {contrast:.1f}:1 | seal at ({LX},{LY})')
assert contrast >= 4.5, 'text contrast below 4.5:1'
assert fw <= W - 64, 'footer overflows frame'
print('OK: og-card.jpg + og-image.jpg written')
