"""Render the synthetic search comparison as a poster, GIF and optionally MP4."""
from pathlib import Path
import argparse
import subprocess
import sys
from PIL import Image, ImageDraw
from build_control import font
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from labs.grid_search import example, search

OUT=Path(__file__).resolve().parent
BG,PANEL,TEXT,MUTED="#f2f3ed","#fbfcf8","#16353a","#466565"
OPEN,SEEN,WALL,ROUTE,START,GOAL="#ecf1e9","#b5dbcf","#476169","#168367","#f7b26e","#a367ad"
W,H,FPS=1280,680,8

def render(grid,start,goal,results,budget):
    im=Image.new("RGB",(W,H),BG);d=ImageDraw.Draw(im)
    d.text((45,24),"ROBOTICS LAB  /  GENERATED SIMULATION",font=font(16,True),fill="#3c6f60")
    d.text((43,62),"How much of the grid did each search explore?",font=font(39,True),fill=TEXT)
    d.text((46,125),"Same start, goal, obstacles, unit costs and tie order. One frame advances the same expansion budget.",font=font(19),fill=MUTED)
    for i,(name,result) in enumerate(zip(("Dijkstra","A*  /  Manhattan heuristic"),results)):
        left=44+i*611;top=174;cell=23;gx=left+37;gy=top+70
        d.rounded_rectangle((left,top,left+581,top+432),radius=14,fill=PANEL,outline="#c4d2c7",width=2)
        d.text((left+31,top+16),name,font=font(25,True),fill=TEXT)
        seen=set(result.expanded[:budget])
        for y in range(grid.height):
            for x in range(grid.width):
                p=(x,y);x0=gx+x*cell;y0=gy+y*cell
                color=WALL if p in grid.blocked else SEEN if p in seen else OPEN
                d.rectangle((x0,y0,x0+cell-2,y0+cell-2),fill=color)
        center=lambda p:(gx+p[0]*cell+cell//2,gy+p[1]*cell+cell//2)
        done=budget>=len(result.expanded)
        if done:d.line([center(c) for c in result.path],fill=ROUTE,width=5)
        for node,color,tag in ((start,START,"S"),(goal,GOAL,"G")):
            x,y=center(node);d.ellipse((x-10,y-10,x+10,y+10),fill=color)
            d.text((x,y-1),tag,font=font(13,True),fill="#18292c",anchor="mm")
        msg=f"Expanded  {min(budget,len(result.expanded))} cells"
        if done:msg+=f"     /     Route  {result.cost} steps"
        d.text((left+32,top+382),msg,font=font(21,True),fill=TEXT)
    d.text((48,632),"Shaded cells = expanded       Dark cells = obstacles       Green line = returned route",font=font(18),fill=MUTED)
    d.text((1235,635),"SYNTHETIC DATA",font=font(16,True),fill="#89572d",anchor="rt")
    return im

def main():
    args=argparse.ArgumentParser();args.add_argument("--mp4",action="store_true");options=args.parse_args()
    grid,start,goal=example()
    results=[search(grid,start,goal,astar=b) for b in (False,True)]
    maximum=max(len(r.expanded) for r in results)
    budgets=[0]*5+list(range(0,maximum+1,4))+[maximum]*12
    poster=render(grid,start,goal,results,maximum)
    poster.save(OUT/"grid-search.png",optimize=True)
    palette_ref=poster.resize((860,457),Image.Resampling.LANCZOS).convert("P",palette=Image.Palette.ADAPTIVE,colors=128)
    video=None
    if options.mp4:
        import imageio_ffmpeg
        video=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),"-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-crf","22","-pix_fmt","yuv420p","-movflags","+faststart",str(OUT/"grid-search.mp4")],stdin=subprocess.PIPE)
    previews=[]
    for budget in budgets:
        im=render(grid,start,goal,results,budget)
        if video:video.stdin.write(im.tobytes())
        im.thumbnail((860,457),Image.Resampling.LANCZOS)
        previews.append(im.quantize(palette=palette_ref,dither=Image.Dither.NONE))
    if video:
        video.stdin.close()
        if video.wait():raise RuntimeError("MP4 encoder failed")
    # GIF stores centiseconds. Quantize cumulative times to retain full duration.
    durations=[10*(round((i+1)*100/FPS)-round(i*100/FPS)) for i in range(len(previews))]
    previews[0].save(OUT/"grid-search.gif",save_all=True,append_images=previews[1:],duration=durations,loop=0,optimize=True)
    print(f"{len(budgets)/FPS:.1f} s; Dijkstra {len(results[0].expanded)}, A* {len(results[1].expanded)}, cost {results[0].cost}")

if __name__=="__main__":
    main()
