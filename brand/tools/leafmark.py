import math
from tree import leaflet_path
LAKE="#0A1520"; INK="#EEF4F7"; ACC="#38C6F2"; GOLD="#FFD23F"; LIGHT="#F2F7FA"; ACCL="#0A7FA8"
def bez(p0,p1,p2,p3,t): return tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t**2*c+t**3*d for a,b,c,d in zip(p0,p1,p2,p3))
def bbox_rot(w,h,rot):
    pts=[]
    for c in ([(0,0),(-w*0.18,-h*0.42),(w*0.28,-h*1.02),(w,-h)],[(w,-h),(w*1.12,-h*0.62),(w*0.62,h*0.06),(0,0)]):
        for i in range(101): pts.append(bez(*c,i/100))
    r=math.radians(rot); rp=[(x*math.cos(r)-y*math.sin(r), x*math.sin(r)+y*math.cos(r)) for x,y in pts]
    xs=[p[0] for p in rp]; ys=[p[1] for p in rp]; return min(xs),min(ys),max(xs),max(ys)
_n=[0]
def leaf_mark(size, fg, bg=None, scale=0.68, rot=-22, rib=True, rib_color=None, two_tone=None, circle=True):
    L=size*scale; W=L*0.82
    x0,y0,x1,y1=bbox_rot(W,L,rot); cx=size/2-(x0+x1)/2; cy=size/2-(y0+y1)/2
    d=leaflet_path(W,L); tr=f'translate({cx:.2f} {cy:.2f}) rotate({rot})'
    out=[]
    if circle and bg: out.append(f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg}"/>')
    out.append(f'<g transform="{tr}">')
    out.append(f'<path d="{d}" fill="{fg}"/>')
    if two_tone:
        _n[0]+=1; cid=f"lf{_n[0]}"
        out.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        # everything to the right of the midrib line, in local coords
        out.append(f'<path clip-path="url(#{cid})" d="M{W*0.16:.1f} {-L*0.14:.1f} L{W*0.82:.1f} {-L*0.80:.1f} L{W*3:.1f} {-L*3:.1f} L{W*3:.1f} {L*3:.1f} L{-W:.1f} {L*3:.1f} Z" fill="{two_tone}"/>')
    if rib:
        out.append(f'<path d="M{W*0.16:.1f} {-L*0.14:.1f} L{W*0.82:.1f} {-L*0.80:.1f}" fill="none" stroke="{rib_color or bg or "none"}" stroke-width="{size*0.026:.1f}" stroke-linecap="round"/>')
    out.append('</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{"".join(out)}</svg>'
if __name__=="__main__":
    variants=[
     ("A ink leaf, lake midrib (centered)", dict(fg=INK,bg=LAKE)),
     ("B ink leaf, blue midrib", dict(fg=INK,bg=LAKE,rib_color=ACC)),
     ("C two-tone, split on the midrib", dict(fg=INK,bg=LAKE,two_tone=ACC)),
     ("D two-tone, midrib in lake", dict(fg=INK,bg=LAKE,two_tone=ACC,rib_color=LAKE)),
     ("E blue leaf, lake midrib", dict(fg=ACC,bg=LAKE)),
     ("F light: lake leaf, blue midrib", dict(fg=LAKE,bg=LIGHT,rib_color=ACCL)),
     ("G light: two-tone", dict(fg=LAKE,bg=LIGHT,two_tone=ACCL,rib_color=LIGHT)),
     ("H plain, no circle (stamp)", dict(fg=LAKE,bg=None,rib_color=LIGHT,circle=False)),
    ]
    cells=[]
    for i,(label,kw) in enumerate(variants):
        svg=leaf_mark(100,**kw); inner=svg[svg.index(">")+1:-6]
        cx=30+(i%4)*290; cy=40+(i//4)*300
        cells.append(f'<g transform="translate({cx} {cy}) scale(1.8)">{inner}</g><g transform="translate({cx+200} {cy}) scale(0.48)">{inner}</g><g transform="translate({cx+200} {cy+60}) scale(0.24)">{inner}</g><g transform="translate({cx+200} {cy+95}) scale(0.16)">{inner}</g><text x="{cx}" y="{cy+205}" font-family="JetBrains Mono" font-size="12" fill="#546A7C">{label}</text>')
    open("avatar-grid.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1190" height="640"><rect width="1190" height="640" fill="#DDE6EC"/>{"".join(cells)}</svg>')
