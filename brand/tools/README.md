# Re-cutting the wordmark

The wordmark is built from Outfit 500 glyph outlines with a custom i (its dot replaced by a
leaflet) and LABS in spaced caps. Nothing is set as live text.

```sh
python3 -m venv .venv && .venv/bin/pip install fonttools
# glyphs.json already carries the outlines; to regenerate from the font file:
#   see final.py / render.py, which read Outfit[wght].ttf at weight 500 and Jost at 400
.venv/bin/python -c "
import tree
open('hickory-labs-dark.svg','w').write(tree.lockup('outfit','leaf','#EEF4F7','#38C6F2'))
open('mark-on-lake.svg','w').write(tree.mark('outfit','leaf','#EEF4F7','#0A1520'))
"
rsvg-convert -w 512 -h 512 mark-on-lake.svg -o avatar-512.png
```

`tree.lockup(font, "leaf", ink, accent=None, labs=True)` returns the SVG; `labs=False` drops the
LABS line. `tree.mark(font, "leaf", fg, bg=None, rib_ok=True)` returns the leaflet, on a circle
when `bg` is given, with the midrib cut in `bg`; pass `rib_ok=False` below 32 px.

Outfit is licensed under the SIL Open Font License. The outlines here are rendered artwork, which
the OFL permits; the font itself is not redistributed.
