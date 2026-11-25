"""Render a labeled synthetic response. Run from the repository root."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labs.control_response import simulate

OUT = Path(__file__).resolve().parent
BG, PANEL, FG, MUTED = "#102d33", "#153840", "#f4f7eb", "#bed2ca"
MINT, ORANGE, GRID = "#9decc3", "#f2b881", "#35575a"

def font(size, bold=False):
    names = ["DejaVuSans-Bold.ttf","segoeuib.ttf"] if bold else ["DejaVuSans.ttf","segoeui.ttf"]
    for name in names:
        try:return ImageFont.truetype(name,size)
        except OSError:continue
    return ImageFont.load_default(size=size)

def main():
    image=Image.new("RGB",(1440,540),BG)
    d=ImageDraw.Draw(image)
    d.text((58,54),"JUNYOUNG GWAK",font=font(19,True),fill=MINT)
    d.text((56,124),"Command",font=font(68,True),fill=FG)
    d.text((56,206),"and response",font=font(58,True),fill=FG)
    d.text((60,330),"A step in commanded speed does not",font=font(23),fill=MUTED)
    d.text((60,367),"immediately change the modeled speed.",font=font(23),fill=MUTED)
    d.text((60,466),"SYNTHETIC MODEL  /  NO FIELD DATA",font=font(17,True),fill=ORANGE)
    d.rounded_rectangle((554,42,1396,495),radius=16,fill=PANEL)
    x0,y0,x1,y1=653,383,1350,134
    x=lambda t:x0+(x1-x0)*t/10
    y=lambda v:y0+(y1-y0)*v
    d.text((597,64),"Speed (m/s)",font=font(22,True),fill=FG)
    for v in (0,.25,.5,.75,1):
        d.line((x0,y(v),x1,y(v)),fill=GRID,width=2)
        d.text((x0-13,y(v)),f"{v:.2f}",font=font(15),fill=MUTED,anchor="rm")
    for t in range(0,11,2):
        d.line((x(t),y1,x(t),y0),fill=GRID,width=1)
        d.text((x(t),y0+8),str(t),font=font(16),fill=MUTED,anchor="mt")
    d.text((x1,y0+33),"Time (s)",font=font(16),fill=MUTED,anchor="rt")
    rows=simulate();last=rows[0];cmd=[(x(0),y(last.command))]
    for r in rows[1:]:
        cmd.extend([(x(r.time),y(last.command)),(x(r.time),y(r.command))])
        last=r
    d.line(cmd,fill=ORANGE,width=4)
    d.line([(x(r.time),y(r.speed)) for r in rows],fill=MINT,width=5)
    d.line((633,452,682,452),fill=ORANGE,width=5)
    d.text((696,451),"Command",fill=FG,font=font(18),anchor="lm")
    d.line((875,452,924,452),fill=MINT,width=5)
    d.text((938,451),"First-order response",fill=FG,font=font(18),anchor="lm")
    image.save(OUT/"control-response.png",optimize=True)

if __name__=="__main__":
    main()
