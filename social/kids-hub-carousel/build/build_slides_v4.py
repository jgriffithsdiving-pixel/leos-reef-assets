import random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A='/home/claude/work/assets/'
FP='/home/claude/work/fonts/PatrickHand-400.ttf'
def F(s): return ImageFont.truetype(FP,s)
W,H=1080,1350
INK=(11,46,74);MUTED=(46,85,112);TEAL=(0,134,158);DEEP=(11,90,120);CORAL=(255,107,74);CORALD=(217,75,43)
SUN=(255,200,61);SUNL=(255,241,191);SKY=(168,230,255);FOAM=(227,248,255);MIST=(232,247,250);WHITE=(255,255,255)
random.seed(7)
def bg():
    im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H
        if t<.4: c=tuple(int(a+(b-a)*(t/.4)) for a,b in zip(FOAM,(255,255,255)))
        else: c=tuple(int(a+(b-a)*((t-.4)/.6)) for a,b in zip((255,255,255),(196,236,250)))
        d.line([(0,y),(W,y)],fill=c)
    im=im.convert('RGBA');ov=Image.new('RGBA',(W,H),(0,0,0,0));od=ImageDraw.Draw(ov)
    for i in range(26):
        r=random.randint(10,40);x=random.randint(0,W);y=random.randint(0,H)
        od.ellipse((x-r,y-r,x+r,y+r),outline=(0,134,158,90),width=4,fill=(168,230,255,60))
        od.ellipse((x-r*.5,y-r*.6,x-r*.18,y-r*.28),fill=(255,255,255,170))
    return Image.alpha_composite(im,ov)
def waves(im):
    d=ImageDraw.Draw(im,'RGBA')
    for col,y0,amp,ph in (((168,230,255,200),1245,18,0.5),((0,134,158,150),1280,16,2.0)):
        pts=[(0,H)]+[(x,y0+amp*math.sin(x/80+ph)) for x in range(0,W+10,10)]+[(W,H)];d.polygon(pts,fill=col)
    pts=[(0,H)]+[(x,1312+10*math.sin(x/60)) for x in range(0,W+10,10)]+[(W,H)];d.polygon(pts,fill=SUNL)
def tx(im,t,s,xy,fill=INK,anchor='l',bold=1,stroke=None,sw=0):
    d=ImageDraw.Draw(im);f=F(s);w=d.textlength(t,font=f)
    x,y=xy
    if anchor=='m':x-=w/2
    if anchor=='r':x-=w
    d.text((x,y),t,font=f,fill=fill,stroke_width=bold if not sw else sw,stroke_fill=stroke or fill);return w
def htx(im,t,sz,xy,fill,anchor='l'):
    tx(im,t,sz,xy,WHITE,anchor,6)
    return tx(im,t,sz,xy,fill,anchor,1)
def wraplines(t,f,maxw):
    d=ImageDraw.Draw(Image.new('RGB',(4,4)));L=[];l=''
    for w in t.split():
        c=(l+' '+w).strip()
        if d.textlength(c,font=f)<=maxw:l=c
        else:L.append(l);l=w
    L.append(l);return L
def para(im,t,s,xy,maxw,fill=INK,anchor='m',gap=6,bold=1):
    f=F(s);y=xy[1]
    for l in wraplines(t,f,maxw): tx(im,l,s,(xy[0],y),fill,anchor,bold);y+=s+gap
    return y
def sticker(im,path,w,xy,rot=0,outline=12):
    s=Image.open(A+path).convert('RGBA');s=s.resize((w,int(s.height*w/s.width)),Image.LANCZOS)
    pad=outline*2+4;c=Image.new('RGBA',(s.width+2*pad,s.height+2*pad),(0,0,0,0));c.paste(s,(pad,pad),s)
    a=c.getchannel('A');dil=a.filter(ImageFilter.MaxFilter(outline*2+1)).filter(ImageFilter.GaussianBlur(1.5))
    wh=Image.new('RGBA',c.size,(255,255,255,255));wh.putalpha(dil)
    sh=Image.new('RGBA',c.size,(11,46,74,0));sh.putalpha(dil.point(lambda v:int(v*.3)))
    o=Image.new('RGBA',c.size,(0,0,0,0));o.alpha_composite(sh,(5,9));o.alpha_composite(wh);o.alpha_composite(c)
    if rot:o=o.rotate(rot,expand=True,resample=Image.BICUBIC)
    im.alpha_composite(o,(int(xy[0]-o.width/2),int(xy[1]-o.height/2)))
def shadow_pill(im,box,fill,r,border=3,off=6):
    d=ImageDraw.Draw(im);d.rounded_rectangle((box[0],box[1]+off,box[2],box[3]+off),r,fill=INK)
    d.rounded_rectangle(box,r,fill=fill,outline=INK,width=border)
def btn(im,cx,y,t,s=46,w=None):
    d=ImageDraw.Draw(im);f=F(s);tw=d.textlength(t,font=f);w=w or tw+90
    shadow_pill(im,(cx-w/2,y,cx+w/2,y+84),CORAL,42,4,6);tx(im,t,s,(cx,y+16),WHITE,'m',1)
def arrow(im,x,y,col=WHITE):
    d=ImageDraw.Draw(im);d.line([(x,y),(x+34,y)],fill=col,width=7);d.polygon([(x+26,y-15),(x+50,y),(x+26,y+15)],fill=col)
def mark(im,xy,fill,txt,s,r=88,rot=-6,fg=WHITE):
    L=Image.new('RGBA',(r*2+60,r*2+60),(0,0,0,0));d=ImageDraw.Draw(L);c=(L.width//2,L.height//2)
    d.ellipse((c[0]-r+4,c[1]-r+12,c[0]+r+4,c[1]+r+12),fill=(11,46,74,90))
    d.ellipse((c[0]-r,c[1]-r,c[0]+r,c[1]+r),fill=fill,outline=WHITE,width=7)
    d.ellipse((c[0]-r-4,c[1]-r-4,c[0]+r+4,c[1]+r+4),outline=(185,207,202),width=2)
    f=F(s);w=d.textlength(txt,font=f);d.text((c[0]-w/2,c[1]-s*0.62),txt,font=f,fill=fg,stroke_width=1,stroke_fill=fg)
    L=L.rotate(rot,resample=Image.BICUBIC);im.alpha_composite(L,(int(xy[0]-L.width/2),int(xy[1]-L.height/2)))
def trail(im,pts,col=TEAL,dot=7,step=34):
    d=ImageDraw.Draw(im,'RGBA')
    # catmull-rom-ish via simple bezier through points using smoothing
    path=[]
    for i in range(len(pts)-1):
        p0=pts[max(i-1,0)];p1=pts[i];p2=pts[i+1];p3=pts[min(i+2,len(pts)-1)]
        for t in [k/40 for k in range(40)]:
            x=.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t*t+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t**3)
            y=.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t*t+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t**3)
            path.append((x,y))
    acc=0;last=path[0]
    for p in path[1:]:
        acc+=math.dist(p,last);last=p
        if acc>=step:
            acc=0;d.ellipse((p[0]-dot,p[1]-dot,p[0]+dot,p[1]+dot),fill=col+(170,))
SBD=Image.open('/home/claude/work/social/sbd-logo.png').convert('RGBA')
LEO=Image.open(A+'img/20170c179b.webp').convert('RGBA')
def logos(im,leo=True):
    s=SBD.resize((120,int(120*SBD.height/SBD.width)),Image.LANCZOS)
    ring=Image.new('RGBA',(s.width+10,s.height+10),(0,0,0,0));ImageDraw.Draw(ring).ellipse((0,0,ring.width-1,ring.height-1),fill=WHITE)
    im.alpha_composite(ring,(31,H-166));im.alpha_composite(s,(36,H-161))
    if leo:
        l=LEO.resize((200,int(200*LEO.height/LEO.width)),Image.LANCZOS);im.alpha_composite(l,(W-36-200,H-150))
def dots(im,n):
    d=ImageDraw.Draw(im)
    for i in range(5):
        x=W/2-80+i*40;d.ellipse((x-9,H-58-9,x+9,H-58+9),fill=INK if i==n-1 else WHITE,outline=INK,width=3)
def save(im,n): im.convert('RGB').save('slides4/'+n)
# ---------- 1
im=bg()
l=LEO.resize((400,int(400*LEO.height/LEO.width)),Image.LANCZOS);im.alpha_composite(l,((W-400)//2,36))
tx(im,"Come see the kids hub!",92,(W/2,255),DEEP,'m',2);tx(im,"Meet Leo's Reef",124,(W/2,355),CORALD,'m',2)
art=Image.open(A+'img/fe4d7e0ce7.webp').convert('RGB').resize((900,426))
box=(80,540,1000,540+426+50);d=ImageDraw.Draw(im);d.rounded_rectangle((box[0],box[1]+10,box[2],box[3]+10),90,fill=INK)
d.rounded_rectangle(box,90,fill=WHITE,outline=INK,width=5)
m=Image.new('L',art.size,0);ImageDraw.Draw(m).rounded_rectangle((0,0,art.width,art.height),70,fill=255);im.paste(art,(90,565),m)
sticker(im,'sprites/timmy-the-turtle.png',210,(150,575),-10);sticker(im,'sprites/blue-tang.png',160,(935,590),12)
para(im,"Stories, games and activities for kids who love the sea",44,(W/2,1045),960,MUTED)
shadow_pill(im,(W/2-240,1128,W/2+240,1212),CORAL,42,4,6);tx(im,"Swipe right",46,(W/2-40,1144),WHITE,'m',1);arrow(im,W/2+80,1170);arrow(im,W/2+100,1192) if False else None
waves(im);logos(im,False);dots(im,1);save(im,'slide-1-cover.png')
# ---------- 2 meet the crew (flowing)
im=bg()
tx(im,"Meet the",110,(W/2,50),DEEP,'m',2);tx(im,"reef crew",126,(W/2,150),CORALD,'m',2)
stops=[('sprites/leo-the-lionfish.png',"I'm Leo! I have 18 spines. We look, but never touch!",(230,420),'L',CORAL),
('sprites/timmy-the-turtle.png',"I'm Timmy, a green sea turtle. I munch seagrass and algae!",(850,630),'R',TEAL),
('sprites/octopus.png',"I'm Ollie! I have three hearts and blue blood!",(230,850),'L',(120,100,200)),
('sprites/parrotfish.png',"I'm Polly. I crunch coral and make white sand!",(850,1040),'R',SUN)]
trail(im,[(230,420),(560,520),(850,630),(560,740),(230,850),(560,960),(850,1040)],TEAL)
for p,t,(x,y),side,c in stops:
    sticker(im,p,300 if 'parrot' not in p else 320,(x,y),random.choice([-5,5]),14)
    bw,bh=470,150
    if side=='L': bx=x+150
    else: bx=x-150-bw
    by=y-bh/2
    if side=='L': bx=min(bx,W-60-bw)
    shadow_pill(im,(bx,by,bx+bw,by+bh),WHITE,85,4,6)
    d=ImageDraw.Draw(im);d.ellipse((bx+26,by+bh/2-12,bx+50,by+bh/2+12),fill=c) if False else None
    ImageDraw.Draw(im).rounded_rectangle((bx+4,by+4,bx+bw-4,by+bh-4),81,outline=c,width=6)
    f=F(36);L=wraplines(t,f,bw-90);yy=by+(bh-len(L)*42)/2
    for l in L: tx(im,l,36,(bx+bw/2,yy),INK,'m',1);yy+=42
shadow_pill(im,(190,1150,820,1228),SUN,40,4,6);tx(im,"Which one is your favourite?",50,(505,1163),INK,'m',1)
waves(im);logos(im);dots(im,2);save(im,'slide-2-meet-the-crew.png')
# ---------- 3 play colour read learn (flowing)
im=bg()
tx(im,"Your own reef,",110,(W/2,50),DEEP,'m',2);tx(im,"right here",128,(W/2,150),CORALD,'m',2)
steps=[("1","Play","a reef game to play",CORAL,'sprites/blue-tang.png',(190,450),'L'),
("2","Colour","7 pages to print",TEAL,'sprites/leo-the-lionfish.png',(890,640),'R'),
("3","Read","Leo the Lionfish",(236,168,20),'sprites/timmy-the-turtle.png',(190,830),'L'),
("4","Learn","real reef facts",(120,100,200),'sprites/octopus.png',(890,1000),'R')]
trail(im,[(190,450),(540,420),(890,640),(540,740),(190,830),(540,930),(890,1000)],CORAL)
for num,name,sub,c,sp,(x,y),side in steps:
    mark(im,(x,y),c,num,84,88,-6 if side=='L' else 5)
    if side=='L':
        htx(im,name,66,(x+120,y-62),c if c!=(236,168,20) else (200,130,0),'l');htx(im,sub,40,(x+120,y+10),INK,'l')
        sticker(im,sp,170,(x+560,y+20),8,10)
    else:
        htx(im,name,66,(x-120,y-62),c if c!=(236,168,20) else (200,130,0),'r');htx(im,sub,40,(x-120,y+10),INK,'r')
        sticker(im,sp,170,(x-560,y+20),-8,10)
shadow_pill(im,(110,1125,830,1210),SUN,44,4,6);tx(im,"One day you could breathe underwater too!",40,(470,1145),INK,'m',1)
waves(im);logos(im);dots(im,3);save(im,'slide-3-play-colour-read.png')

# ---------- 4 phone
def phone(im,shot,x,y,w,rot):
    sw=w;sh=int(shot.height*w/shot.width);bt=44;b=14
    L=Image.new('RGBA',(sw+2*b+60,sh+bt+b+70),(0,0,0,0));d=ImageDraw.Draw(L)
    ox,oy=30,25;PW=sw+2*b;PH=sh+bt+b
    d.rounded_rectangle((ox+4,oy+14,ox+PW+4,oy+PH+14),54,fill=(11,46,74,110))
    d.rounded_rectangle((ox,oy,ox+PW,oy+PH),54,fill=INK)
    scr=shot.resize((sw,sh),Image.LANCZOS).convert('RGBA');m=Image.new('L',scr.size,0);ImageDraw.Draw(m).rounded_rectangle((0,0,sw,sh),30,fill=255)
    L.paste(scr,(ox+b,oy+bt),m)
    d.rounded_rectangle((ox+PW/2-48,oy+13,ox+PW/2+48,oy+33),10,fill=(60,90,115))
    L=L.rotate(rot,expand=True,resample=Image.BICUBIC)
    im.alpha_composite(L,(int(x-L.width/2),int(y-L.height/2)))
full=Image.open('/home/claude/work/hub-full.png').convert('RGB')
shotA=full.crop((0,170,780,1790));shotB=full.crop((0,2290,780,3910))
im=bg()
tx(im,"Peek inside",110,(W/2,50),DEEP,'m',2);tx(im,"the kids hub",126,(W/2,150),CORALD,'m',2)
phone(im,shotA,290,748,390,-4);phone(im,shotB,790,752,390,4)
mark(im,(965,355),SUN,"Free!",66,86,8,INK)
sticker(im,'sprites/blue-tang.png',140,(540,1190),-8,10)
waves(im);logos(im);dots(im,4);save(im,'slide-4-peek-inside-the-hub.png')
# ---------- 4
im=bg()
tx(im,"Your reef is",118,(W/2,60),DEEP,'m',2);tx(im,"waiting!",138,(W/2,175),CORALD,'m',2)
l=LEO.resize((720,int(720*LEO.height/LEO.width)),Image.LANCZOS);im.alpha_composite(l,((W-720)//2,380))
sticker(im,'sprites/timmy-the-turtle.png',210,(170,690),-12);sticker(im,'sprites/blue-tang.png',170,(920,700),14)
sticker(im,'sprites/octopus.png',170,(920,880),-8);sticker(im,'sprites/parrotfish.png',190,(170,880),10)
btn(im,W/2,1000,"Find Leo's Reef: link in our bio",46,w=800)
shadow_pill(im,(70,1125,1010,1205),SUNL,40,3,5)
para(im,"Grown-ups: Bubblemaker lets kids from age 8 try diving in the pool.",32,(W/2,1145),900,INK)
waves(im);logos(im,False);dots(im,5);save(im,'slide-5-your-reef-is-waiting.png')
