import json, sys
import os; G=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"glyphs.json")))

def word(font, text, size, x0, base, skip=None):
    """Return (svg, xpositions, width). y-up font units flipped into SVG."""
    d=G[font]; s=size/d["upm"]; x=x0; parts=[]; xs={}
    for i,ch in enumerate(text):
        g=d["glyphs"][ch]; xs[i]=x
        if not (skip and i in skip):
            parts.append(f'<path transform="translate({x:.2f} {base}) scale({s:.5f} {-s:.5f})" d="{g["d"]}"/>')
        x+=g["adv"]*s
    return "".join(parts), xs, x-x0

def chevron_k(font, size, x, base, gap_mult=0.55, stroke=None, lean=1.0):
    """Custom k: font stem kept via a rect, arm+leg as one detached chevron stroke."""
    d=G[font]; s=size/d["upm"]; xh=d["xHeight"]*s
    stem_w = {"outfit":0.098,"jost":0.083}[font]*size   # measured stem widths
    asc = {"outfit":0.70,"jost":0.72}[font]*size
    sx = x + {"outfit":0.075,"jost":0.06}[font]*size    # left side bearing
    sw = stroke or stem_w
    gap = stem_w*gap_mult
    ax = sx+stem_w+gap                     # chevron apex x
    ay = base - xh*0.5                     # apex at half x-height
    reach = (xh*0.5)*lean                  # horizontal reach of arms
    tipx = ax+reach
    top = base - xh + sw*0.5
    bot = base - sw*0.5
    rect=f'<rect x="{sx:.2f}" y="{base-asc:.2f}" width="{stem_w:.2f}" height="{asc:.2f}" rx="{stem_w/2:.2f}"/>'
    chev=f'<path d="M{tipx:.2f} {top:.2f} L{ax:.2f} {ay:.2f} L{tipx:.2f} {bot:.2f}" fill="none" stroke="currentColor" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round"/>'
    return rect+chev

def labs(font, size, x, y, spacing=0.25):
    d=G[font]; s=size/d["upm"]; parts=[]; cx=x
    for ch in "labs":
        g=d["glyphs"][ch]
        parts.append(f'<path transform="translate({cx:.2f} {y}) scale({s:.5f} {-s:.5f})" d="{g["d"]}"/>')
        cx+=g["adv"]*s+size*spacing
    return "".join(parts), cx-x-size*spacing

rows=[]; y=150; H=0
sheet=[]
for font,label in [("outfit","Outfit 500"),("jost","Jost 400")]:
    for variant,kw in [("gap 0.55",dict(gap_mult=0.55)),("gap 0.9, lean 1.15",dict(gap_mult=0.9,lean=1.15)),("attached",dict(gap_mult=0.0))]:
        size=120; x0=60; base=y
        w,xs,width=word(font,"hickory",size,x0,base,skip={3})
        k=chevron_k(font,size,xs[3],base,**kw)
        sheet.append(f'<g fill="#0F1419" color="#0F1419">{w}{k}</g>')
        sheet.append(f'<text x="{x0+width+40}" y="{base}" font-family="JetBrains Mono" font-size="16" fill="#5C6670">{label} · k {variant}</text>')
        y+=170
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{y}" viewBox="0 0 1100 {y}"><rect width="1100" height="{y}" fill="#E8EAE3"/>{"".join(sheet)}</svg>'
open("k-sheet.svg","w").write(svg)
