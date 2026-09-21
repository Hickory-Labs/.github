# Hickory Labs brand

Draft 2026-09-21. The studio identity: wordmark, mark, palette, type, and the rules that keep
them consistent across the GitHub org, the site, the build log, and every product. V Formation's
own UI tokens live in [v-formation `design/tokens.md`](https://github.com/Hickory-Labs/v-formation/blob/main/design/tokens.md); they are the product layer under
this, and they share the palette on purpose.

Decided 2026-09-21: the leaf wordmark in Outfit 500, and the Lake palette. The other 26 palettes
explored that day live on as V Formation themes ([v-formation `design/themes.md`](https://github.com/Hickory-Labs/v-formation/blob/main/design/themes.md)).

## Why these colors

Blue and gold: maize and blue, by way of the Great Lakes and the Sky (V Formation's home screen).
The blue has some water in it, the gold is fall
hickory leaves, and neither is green (another company's look), terracotta (the common AI palette),
lavender (a well-known tracker's), or brown.

## Reference point

Linear's observable system, as read from their site in 2026, is the target for feel: a near-black
canvas, a ladder of four or five surfaces instead of shadows, hairline borders, one accent used
only for brand and focus, a narrow weight band, tight negative tracking on display type and none
on body, small radii, a 4 px spacing base. Airbnb's DLS is the target for rigor: every token named,
every component built from tokens, nothing hand-tuned in place. Nothing from either is copied;
the values below are Hickory's.

## Wordmark

`hickory` in lowercase, `LABS` in spaced capitals right-aligned under it. The i's dot is a single
hickory leaflet, leaning 22 degrees to the right, 2.5 stems tall. The wordmark is drawn from the
chosen face's outlines and shipped as an SVG; it is never set as live text.

- Minimum width 72 px. Below that, use the mark alone.
- Clear space around it: the height of the x-height on every side.
- One color. Cream on dark, dark on cream. The leaflet may take amber only when it is the sole
  accent on the surface.
- Never stretched, outlined, shadowed, or placed on a photograph without a solid tile behind it.

## Mark

The leaflet alone, same lean, with a midrib cut in the ground color. On a circle for avatars.

| Use | Size | Midrib |
| --- | --- | --- |
| GitHub org avatar | 512 px source, shown at 48 and 24 | yes at 48, no at 24 |
| Favicon | 32, 16 | no |
| README stamp, social cards | 64 and up | yes |

Products keep their own marks under the studio mark. V Formation's bird icon
(`M3 13c3-3 6-3 9 1 3-4 6-4 9-1` on a 24 grid) is the product's, not the studio's.

## Palette

Shared with V Formation. Dark is the native theme; the site and documents also need light.

### Dark (native): Lake

| Token | Value | Use |
| --- | --- | --- |
| `canvas` | `#0A1520` | Page ground, blue-black with deep water in it |
| `surface.1` | `#121F2C` | Cards, rows, tracks |
| `surface.2` | `#0E1A26` | Inputs, bars, code |
| `line` | `#1C2C3C` | Hairline borders, dividers |
| `ink.1` | `#EEF4F7` | Primary text, primary fills |
| `ink.2` | `#BFCCD6` | Body |
| `ink.3` | `#84A0B3` | Labels, hints, meta |
| `accent` | `#38C6F2` | Brand and focus: the leaf, selected tab, focus ring, primary button, links |
| `attention` | `#FFD23F` | The honk. Nothing else |

### Light (site, documents): Lake

| Token | Value | Use |
| --- | --- | --- |
| `canvas` | `#F2F7FA` | Page ground, a cool off-white with a little sky in it |
| `surface.1` | `#FFFFFF` | Cards |
| `surface.2` | `#E7EFF4` | Inputs, bars, code |
| `line` | `#D0DDE6` | Hairlines |
| `ink.1` | `#0A1520` | Primary text |
| `ink.2` | `#2B3E4F` | Body |
| `ink.3` | `#546A7C` | Labels, hints, meta |
| `accent` | `#0A7FA8` | Brand and focus, darkened to pass 4.5:1 as text on canvas |
| `attention` | `#B8860B` | The honk, darkened likewise |

### Semantic

Bird status, separate from the accent and never used as decoration. Dark: flying `#7BE0C5`
(teal, not green), gliding `#7C93A8` (slate), grounded `#FF7070` (coral red), honking is
`attention`. Light: flying `#0F8F7A`, gliding `#6B7787`, grounded `#D63C3C`, honking `#B8860B`.

### Rules

- One accent per surface. Attention (gold) is not a second accent; it marks a honk and nothing else.
- Depth comes from the surface ladder and hairlines, not shadows. No gradients, no glows, except
  the 4 px halo on a honking bird, which is a status signal.
- Green is never a brand or status color here.
- Neutrals carry blue: every gray above has some water in it. Never `#808080`, never brown.

## Type

| Role | Family | Weights | Notes |
| --- | --- | --- | --- |
| Display | Instrument Serif | 400 | Titles only. One size per surface. Line height 1. Tracking 0; the face is already tight. |
| UI and body | IBM Plex Sans | 400, 500, 600 | 500 is the emphasis weight; 600 only for section labels and primary buttons. Never 700. |
| Code | JetBrains Mono | 400, 500 | Anything a terminal or a shell would show. Never used for labels that are not code. |
| Wordmark | Outfit 500 | as drawn | Outlines only, cut by the tools in the `.github` repo. Not used anywhere else. |

- Body 14 to 16 px, line height 1.45 to 1.5, measure 60 to 70 characters.
- Section labels: 12 px, 600, uppercase, letter-spacing 1 px, `ink.3`.
- Display over 40 px: tracking -0.02 em. Under 40 px: 0.
- Tabular numerals wherever digits align.

## Shape and space

- Radii: 6 (chips), 9 (segments, keys), 12 (cards, inputs), 14 (rows, primary buttons), pill
  for tabs and avatars. Nothing between 14 and pill.
- Spacing base 4 px. Steps 4, 8, 12, 16, 24, 32, 48, 96.
- Touch targets 44 px on anything phone-first. Primary buttons 52 px.
- Hairlines are 1 px at 1x and stay 1 px at 2x.

## Voice, one line

Plain, direct, US spelling, no emoji, no em-dashes in anything published. Products are named in
sentence case ("V Formation", "the Sky"). The studio is "Hickory Labs", never "HL" in prose.

## Files

`Hickory-Labs/.github` holds `brand/`: the lockups (`hickory-labs-{dark,light}.svg`, mono
variants, `hickory-{dark,light}.svg` without LABS for places that already say labs), the marks
(`mark-on-lake.svg` for avatars, `mark-plain-*.svg` for stamping), PNG exports (512 avatar, 180
apple touch, 64/32/16 favicons), and `tools/` to re-cut all of it from the font outlines.

## Where this goes next

1. Upload `brand/avatar-512.png` as the org avatar (GitHub UI only; the API cannot).
2. The site at hickorylabs.dev builds from the light tokens with a dark toggle.
3. A Claude Design "Design System" artifact generated from this file so new mockups inherit it.
4. `FUNDING.yml` in `.github` once Sponsors is on.
