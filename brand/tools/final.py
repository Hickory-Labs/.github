import json
from render import word, chevron_k, G
DARK="#0F1419"; CREAM="#E8EAE3"; AMBER="#F2A541"
STEM={"outfit":0.098,"jost":0.083}; LSB={"outfit":0.075,"jost":0.06}

def caps(font,size,x,y,text="LABS",spacing=0.28):
    d=G[font]; s=size/d["upm"]; parts=[]; cx=x
    for ch in text:
        g=d["glyphs"][ch]; parts.append(f'<path transform="translate({cx:.2f} {y}) scale({s:.5f} {-s:.5f})" d="{g["d"]}"/>'); cx+=g["adv"]*s+size*spacing
    return "".join(parts), cx-x-size*spacing

def chevron_only(font,size,x,base):
    d=G[font]; s=size/d["upm"]; xh=d["xHeight"]*s; stem_w=STEM[font]*size; sx=x+LSB[font]*size
    ax=sx+stem_w+stem_w*0.55; ay=base-xh*0.5; reach=xh*0.5; tipx=ax+reach; sw=stem_w
    return f'<path d="M{tipx:.2f} {base-xh+sw*0.5:.2f} L{ax:.2f} {ay:.2f} L{tipx:.2f} {base-sw*0.5:.2f}" fill="none" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round"/>'

def stem_only(font,size,x,base):
    stem_w=STEM[font]*size; asc={"outfit":0.70,"jost":0.72}[font]*size; sx=x+LSB[font]*size
    return f'<rect x="{sx:.2f}" y="{base-asc:.2f}" width="{stem_w:.2f}" height="{asc:.2f}" rx="{stem_w/2:.2f}"/>'

def lockup_svg(font, fg, accent=None, size=100):
    """Standalone SVG string, tight viewBox. fg/accent are CSS colors (currentColor allowed)."""
    x0=0; base=size*0.78
    w,xs,width=word(font,"hickory",size,x0,base,skip={3})
    st=stem_only(font,size,xs[3],base); ch=chevron_only(font,size,xs[3],base)
    lsize=size*0.24; ly=base+size*0.50
    lb,lw=caps(font,lsize,0,ly); lb,lw=caps(font,lsize,x0+width-lw-size*0.01,ly)
    H=ly+size*0.06; Wd=width+size*0.02
    body=(f'<g fill="{fg}">{w}{st}</g><g stroke="{accent or fg}">{ch}</g><g fill="{fg}" opacity="0.75">{lb}</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-size*0.02:.1f} 0 {Wd:.1f} {H:.1f}" width="{Wd:.0f}" height="{H:.0f}">{body}</svg>', Wd, H

def mark_svg(font, fg, bg=None, size=100):
    """The chevron alone in a square viewBox, optional circle behind it."""
    d=G[font]; xh=d["xHeight"]*(size/d["upm"]); sw=STEM[font]*size
    reach=xh*0.5; half=xh*0.5-sw*0.5
    cx=size/2; cy=size/2; ax=cx-reach*0.42; tipx=ax+reach
    circ=f'<circle cx="{cx}" cy="{cy}" r="{size/2}" fill="{bg}"/>' if bg else ""
    p=f'<path d="M{tipx:.2f} {cy-half:.2f} L{ax:.2f} {cy:.2f} L{tipx:.2f} {cy+half:.2f}" fill="none" stroke="{fg}" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{circ}{p}</svg>'

if __name__=="__main__":
    out={}
    for font in ("outfit","jost"):
        out[font]={"lockup":lockup_svg(font,"currentColor")[0],
                   "lockup_accent":lockup_svg(font,"currentColor",AMBER)[0],
                   "mark":mark_svg(font,"currentColor"),
                   "mark_on_dark":mark_svg(font,CREAM,DARK),
                   "mark_on_cream":mark_svg(font,DARK,CREAM),
                   "mark_amber":mark_svg(font,AMBER,DARK)}
    json.dump(out,open("final.json","w"))
    # quick proof render
    s=lockup_svg("outfit",DARK,AMBER,200)[0]
    open("proof.svg","w").write(s.replace('<svg ','<svg style="background:#E8EAE3" ',1))
    print("ok")
