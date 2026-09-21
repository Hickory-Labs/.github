import json, re
from render import word, G
from final import caps, STEM, LSB
DARK="#0F1419"; CREAM="#E8EAE3"; AMBER="#F2A541"

def split_contours(d):
    parts=re.split(r'(?=M)', d.strip()); return [p for p in parts if p]
def contour_ymin(c):
    nums=[float(n) for n in re.findall(r'-?\d+\.?\d*', c)]; ys=nums[1::2]; return min(ys), max(ys)

def i_without_dot(font):
    g=G[font]["glyphs"]["i"]; xh=G[font]["xHeight"]
    keep=[c for c in split_contours(g["d"]) if contour_ymin(c)[0] < xh*0.9]
    return "".join(keep)

def leaflet_path(w, h):
    """A lanceolate leaflet, tip up-right, base at origin. w,h in local units."""
    return (f"M0 0 C {-w*0.18:.1f} {-h*0.42:.1f} {w*0.28:.1f} {-h*1.02:.1f} {w:.1f} {-h:.1f} "
            f"C {w*1.12:.1f} {-h*0.62:.1f} {w*0.62:.1f} {h*0.06:.1f} 0 0 Z")

def leaf_dot(font,size,x,base,scale=1.0,rot=-22):
    d=G[font]; s=size/d["upm"]; xh=d["xHeight"]*s; stem_w=STEM[font]*size
    g=d["glyphs"]["i"]; dot=[c for c in split_contours(g["d"]) if contour_ymin(c)[0] >= d["xHeight"]*0.9][0]
    ymin,ymax=contour_ymin(dot); nums=[float(n) for n in re.findall(r'-?\d+\.?\d*', dot)]; xs=nums[0::2]
    cx=x+(min(xs)+max(xs))/2*s; cy=base-(ymin+ymax)/2*s     # dot center in svg coords
    L=stem_w*2.5*scale; Wl=L*0.82
    p=leaflet_path(L, L*0.0+L)  # square-ish box, rotate to lean
    return f'<path transform="translate({cx-stem_w*0.15:.2f} {cy+L*0.42:.2f}) rotate({rot})" d="{leaflet_path(Wl, L)}"/>'

def h_fork(font,size,x,base,angle=28,length=0.42):
    d=G[font]; s=size/d["upm"]; stem_w=STEM[font]*size; asc={"outfit":0.70,"jost":0.72}[font]*size
    sx=x+LSB[font]*size+stem_w/2; top=base-asc
    import math
    y0=top+asc*0.48; L=asc*length
    ex=sx-math.sin(math.radians(angle))*L; ey=y0-math.cos(math.radians(angle))*L
    return f'<path d="M{sx:.2f} {y0:.2f} L{ex:.2f} {ey:.2f}" fill="none" stroke-width="{stem_w:.2f}" stroke-linecap="round"/>'

def lockup(font, variant, fg, accent=None, size=100, labs=True):
    x0=0; base=size*0.78
    if variant=="leaf":
        w,xs,width=word(font,"hickory",size,x0,base,skip={1})
        d=G[font]; s=size/d["upm"]
        istem=f'<path transform="translate({xs[1]:.2f} {base}) scale({s:.5f} {-s:.5f})" d="{i_without_dot(font)}"/>'
        extra=f'<g fill="{accent or fg}">{leaf_dot(font,size,xs[1],base)}</g>'
        w=w+istem
    else:
        w,xs,width=word(font,"hickory",size,x0,base)
        extra=f'<g stroke="{accent or fg}">{h_fork(font,size,xs[0],base)}</g>'
    if labs:
        lsize=size*0.24; ly=base+size*0.50
        lb,lw=caps(font,lsize,0,ly); lb,lw=caps(font,lsize,x0+width-lw-size*0.01,ly)
        H=ly+size*0.06
    else:
        lb=""; H=base+size*0.26
    Wd=width+size*0.02
    # allow the fork to poke left of the h
    vb_x=-size*0.16 if variant=="fork" else -size*0.02
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x:.1f} {-size*0.05:.1f} {Wd-vb_x:.1f} {H+size*0.05:.1f}"><g fill="{fg}">{w}</g>{extra}<g fill="{fg}" opacity="0.75">{lb}</g></svg>'

def mark(font, variant, fg, bg=None, size=100, rib_ok=True):
    circ=f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg}"/>' if bg else ""
    if variant=="leaf":
        L=size*0.52; Wl=L*0.82; rot=-22
        ox=size*0.40; oy=size*0.74
        p=f'<path transform="translate({ox:.1f} {oy:.1f}) rotate({rot})" d="{leaflet_path(Wl, L)}" fill="{fg}"/>'
        rib=(f'<path transform="translate({ox:.1f} {oy:.1f}) rotate({rot})" d="M{Wl*0.16:.1f} {-L*0.14:.1f} L{Wl*0.82:.1f} {-L*0.80:.1f}" '
             f'fill="none" stroke="{bg}" stroke-width="{size*0.026:.1f}" stroke-linecap="round"/>') if bg and rib_ok else ""
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{circ}{p}{rib}</svg>'
    else:
        import math; sw=size*0.10; cx=size/2
        y0=size*0.78; ytop=size*0.24; fy=size*0.50; L=size*0.36
        ex=cx-math.sin(math.radians(28))*L; ey=fy-math.cos(math.radians(28))*L
        p=f'<g fill="none" stroke="{fg}" stroke-width="{sw:.1f}" stroke-linecap="round"><path d="M{cx} {y0} V{ytop}"/><path d="M{cx} {fy} L{ex:.1f} {ey:.1f}"/></g>'
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{circ}{p}</svg>'

if __name__=="__main__":
    out={}
    for v in ("leaf","fork"):
        out[v]={"lockup":lockup("outfit",v,"currentColor"),"lockup_accent":lockup("outfit",v,"currentColor",AMBER),
                "mark_on_dark":mark("outfit",v,CREAM,DARK),"mark_on_cream":mark("outfit",v,DARK,CREAM),"mark_amber":mark("outfit",v,AMBER,DARK),
                "lockup_jost":lockup("jost",v,"currentColor")}
    json.dump(out,open("tree.json","w"))
    # proof sheet
    rows=[]; y=0
    for v in ("leaf","fork"):
        for font in ("outfit","jost"):
            m=mark(font,v,DARK,CREAM).replace("<svg ",'<svg width="120" height="120" ',1)
            lk=lockup(font,v,DARK); inner=lk[lk.index(">")+1:-6]
            rows.append(f'<rect y="{y}" width="1200" height="260" fill="{CREAM}"/>'
                        f'<g transform="translate(80 {y+40}) scale(1.6)">{inner}</g>'
                        f'<g transform="translate(980 {y+70})">{m}</g>'
                        f'<text x="1160" y="{y+30}" text-anchor="end" font-family="JetBrains Mono" font-size="14" fill="#5C6670">{v} · {font}</text>')
            y+=260
    open("tree-sheet.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{y}">{"".join(rows)}</svg>')
    print("ok")
