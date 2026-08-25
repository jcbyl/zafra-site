# Zafra Trading Co. — DESIGN.md

Extracted 2026-08-24 from the approved live site (index.html, main branch) by pixel/token audit.
This is the canonical system. The live cream-oval logo is FINAL (JC, 2026-08-24) — never regenerate or propose alternatives.
Rule of thumb: AGENTS.md says how to build; this file says how it must look.

## 1. Visual Theme & Atmosphere

Heritage agricultural trading house — Puerto Rican coffee, cacao, honey, vanilla. The register is
**engraved cream-and-green provenance**: warm cream canvas (never pure white), deep botanical greens
carrying authority, gold used as a *ceremony accent only* (labels, eyebrows, hairlines — never large
fills). Cormorant Garamond serif carries the brand voice; Inter does all the quiet work. The feel is
a sealed crate from a 19th-century trading house, not a tech product.

**Key characteristics:**
- Four-tier green system, each tier mapped to a surface role (see §2)
- Gold = provenance signal (origin labels, eyebrows) — NEVER a background or large fill
- Warm cream canvas instead of white; cream-2/cream-3 for zone separation
- Serif for display/voice, sans for utility — never mixed within one element
- Uppercase eyebrows with wide tracking (.08–.22em) as the signature label form
- Shadows are whispers (≤.06 alpha), never theatrical

## 2. Color Palette & Roles

### Greens (authority tiers)
- `--green-900 #0f2818` — deepest ground; hero band, footer, dark feature zones
- `--green-800 #1a3a24` — primary brand green; headings, nav brand text, emphasis
- `--green-700 #245234` — secondary surface green
- `--green-600 #2d6b47` — lightest accent green

### Gold (ceremony only)
- `--gold-600 #a8853a` — origin labels, harvest labels (text on cream)
- `--gold-500 #c4a04a` — mid gold, hairline rules
- `--gold-400 #dab85e` — hero eyebrow on dark green

### Creams (canvas)
- `--cream #faf8f3` — PRIMARY page canvas (never #ffffff as page bg)
- `--cream-2 #f5f1e8` — zone separator / alt section wash
- `--cream-3 #e8e2d4` — deepest cream, borders/dividers

### Ink & lines
- `--ink #1a2a1e` — body text (green-black, never pure black)
- `--ink-soft #4a5a4e`, `--ink-mute #5a6a5e` — secondary/muted text
- `--white #ffffff` — cards on cream
- `--line rgba(15,40,24,.06)` — hairline borders
- `--shadow-sm 0 2px 8px rgba(15,40,24,.04)`, `--shadow 0 8px 24px rgba(15,40,24,.06)`

## 3. Typography Rules

- **Sans (utility):** `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif` — body, nav, labels, buttons. 400/600 weights only.
- **Serif (voice):** `'Cormorant Garamond', Georgia, serif` — hero title, section titles, card names. Weights 500/600.

| Role | Font | Size | Weight | Tracking | Case | Color |
|------|------|------|--------|----------|------|-------|
| Hero title | serif | clamp(38px, 6.4vw, 78px) | 500 | -.01em | Title | cream (on green-900) |
| Section title | serif | clamp(30px, 4.5vw, 44px) | 500 | -.01em | Title | green-800 |
| Card title | serif | 22px | 600 | — | Title | green-800 |
| Harvest/feature h3 | serif | 30px | 500 | — | Title | green-800 |
| Hero eyebrow | sans | 12px | 600 | .22em | UPPER | gold-400 |
| Origin label | sans | 11px | 600 | .08em | UPPER | gold-600 |
| Harvest label | sans | 11px | 600 | .14em | UPPER | gold-600 |
| Nav brand | sans | 13px | 600 | .08em | UPPER | green-800 |
| Flow step label | sans | 13px | 600 | .06em | UPPER | cream |
| Body | sans | 16px | 400 | — | — | ink, line-height 1.6 |

**Tracking laws (Butterick):** caps tracking = 5–12% of point size (.22em on 12px is the one deliberate
exception, hero eyebrow). Kerning always on. Hierarchy by weight+color, not size inflation.
Optical correction: any letterspaced centered line needs `x += ls/2` (WebKit trailing-space shift).

## 4. Component Stylings

- **Eyebrow label** (signature): 11–12px/600/UPPERCASE, gold, wide tracking, 10–20px bottom margin — appears above every major title
- **Product card:** white bg, shadow-sm, serif name + gold origin eyebrow + sans body
- **Dark feature band:** green-900 bg, cream serif headline, cream/70 body, gold-400 eyebrow
- **Hairlines:** 1px gold-500 or line token — decoration stays hairline, never thick rules

## 5. Layout Principles

- Cream canvas breathes; separate sections with cream-2 wash or whitespace, NOT borders
- Dark-green bookends: hero band and footer in green-900/800 framing a cream body
- One primary action per view; labels do hierarchy work via tracking+case, not size

## 6. Do's and Don'ts

**Do**
- Warm cream canvas; four-tier greens mapped to roles; gold as text/hairline ceremony only
- Serif voice + sans utility; wide-tracked uppercase eyebrows as the signature label
- Whisper shadows; hairline gold rules

**Don't**
- Never pure white page bg, never pure black text
- Never gold fills/backgrounds or large gold surfaces
- Never sans for display titles or serif for body utility
- Never arbitrary tracking values — follow the % laws
- Never regenerate the logo (closed, fact 40)

## 7. Logo

`images/zafra-logo-final.jpg` — the cream-oval engraved seal. FINAL AND CLOSED (JC 2026-08-24).
Shown complete (seal + wordmark) or not at all. Do not crop, recolor, restyle, or "improve."
