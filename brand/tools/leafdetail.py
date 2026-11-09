"""The leaflet's detail, cut out of the leaf with a mask so the ground shows through on any surface.

Two levels, by the size the leaf renders at (BRAND.md, Mark):
- "line": the midrib alone. The leaf as the dot of the i, favicons, anything under 48 px.
- "veins": the midrib and three pairs of side veins curving to the tip. Stamps, avatars, anything 48 px and up.

Coordinates are the leaflet's own (tree.leaflet_path: base at the origin, tip at (w, -h)), drawn for w=42.6,
h=52 and scaled to the leaf, so the detail fits any leaflet the tools cut.
"""
import re

W0, H0 = 42.6, 52.0
LINE = ((6.8, -7.3), (35.0, -41.6))
MIDRIB = ((4.2, -4.5), (37.5, -44.6))
# Fitted inside the outline (64% of the way to the edge), each bowing toward the tip.
VEINS = [
    ((13.6, -15.5), (21.4, -15.4), (27.4, -18.6)), ((13.6, -15.5), (11.6, -24.7), (14.0, -32.6)),
    ((20.9, -24.5), (27.6, -24.4), (32.8, -27.1)), ((20.9, -24.5), (19.3, -32.3), (21.3, -39.0)),
    ((27.1, -32.0), (32.4, -31.9), (36.6, -34.1)), ((27.1, -32.0), (25.8, -38.1), (27.4, -43.4)),
]


def _pt(p, w, h):
    return f"{p[0] * w / W0:.2f} {p[1] * h / H0:.2f}"


def cuts(w, h, level):
    """The detail as black strokes, for the inside of a mask."""
    k = h / H0
    if level == "line":
        a, b = LINE
        return (f'<path d="M{_pt(a, w, h)} L{_pt(b, w, h)}" fill="none" stroke="black" '
                f'stroke-width="{2.6 * k:.2f}" stroke-linecap="round"/>')
    a, b = MIDRIB
    veins = " ".join(f"M{_pt(s, w, h)} Q{_pt(c, w, h)} {_pt(e, w, h)}" for s, c, e in VEINS)
    return (f'<g fill="none" stroke="black" stroke-linecap="round">'
            f'<path d="M{_pt(a, w, h)} L{_pt(b, w, h)}" stroke-width="{2.6 * k:.2f}"/>'
            f'<path d="{veins}" stroke-width="{1.8 * k:.2f}"/></g>')


def leaf(transform, d, level, mask_id, fill=None):
    """A leaflet path with its detail cut out. The mask sits in the leaf's own coordinates; its size is read from
    the path as written, so the generator and recut() agree to the digit."""
    w, h = size_of(d)
    fill_attr = f' fill="{fill}"' if fill else ""
    if not level:
        return f'<path transform="{transform}" d="{d}"{fill_attr}/>'
    return (f'<g transform="{transform}"><mask id="{mask_id}" maskUnits="userSpaceOnUse" x="-100" y="-100" '
            f'width="200" height="200"><rect x="-100" y="-100" width="200" height="200" fill="white"/>'
            f'{cuts(w, h, level)}</mask><path d="{d}"{fill_attr} mask="url(#{mask_id})"/></g>')


# An uncut leaflet as the tools write it, and the stroked midrib the marks used to carry.
LEAF_RE = re.compile(r'<path transform="([^"]*rotate\(-22\))" d="(M0 0 C [^"]*Z)"(?: fill="([^"]*)")?/>')
OLD_RIB_RE = re.compile(r'<path transform="[^"]*rotate\(-22\)" d="M[^"]*" fill="none" stroke="[^"]*" '
                        r'stroke-width="[^"]*" stroke-linecap="round"/>')
CUT_RE = re.compile(r'<g transform="([^"]*rotate\(-22\))"><mask id="[^"]*".*?</mask><path d="(M0 0 C [^"]*Z)"'
                    r'(?: fill="([^"]*)")? mask="url\(#[^)]*\)"/></g>')


def size_of(d):
    nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", d)]
    return nums[6], -nums[7]  # the first curve ends at the tip, (w, -h)


def recut(svg, level, prefix="hl-leaf"):
    """Give every leaflet in an SVG the detail for `level` (None for a plain leaf). Safe to run again."""
    svg = OLD_RIB_RE.sub("", svg)
    n = [0]

    def one(m):
        transform, d, fill = m.group(1), m.group(2), m.group(3)
        n[0] += 1
        return leaf(transform, d, level, f"{prefix}-{n[0]}", fill)

    svg = CUT_RE.sub(lambda m: f'<path transform="{m.group(1)}" d="{m.group(2)}"'
                               + (f' fill="{m.group(3)}"' if m.group(3) else "") + "/>", svg)
    return LEAF_RE.sub(one, svg)
