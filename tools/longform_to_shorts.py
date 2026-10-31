import re,subprocess,sys,os,textwrap
O="/mnt/user-data/outputs/shorts_ep004"
def load(p):
    t=open(p).read();out=[]
    for m in re.finditer(r"(\d\d):(\d\d):(\d\d),(\d+) --> (\d\d):(\d\d):(\d\d),(\d+)\n(.*?)\n\n",t+"\n\n",re.S):
        g=m.groups();s=int(g[0])*3600+int(g[1])*60+int(g[2])+int(g[3])/1000;e=int(g[4])*3600+int(g[5])*60+int(g[6])+int(g[7])/1000
        out.append((s,e,g[8].replace("\n"," ")))
    return out
def at(x):
    h=int(x//3600);m=int(x%3600//60);s=x%60;return f"{h}:{m:02d}:{s:05.2f}"
def wrap(t,w,ko):
    if ko:
        words=t.split(" ");lines=[];cur=""
        for wd in words:
            if len(cur)+len(wd)+1>w and cur: lines.append(cur);cur=wd
            else: cur=(cur+" "+wd).strip()
        lines.append(cur);return "\\N".join(lines)
    return "\\N".join(textwrap.wrap(t,w))
def make(name,video,srt,a,b,title,cta,ko):
    cues=[c for c in load(srt) if c[1]>a and c[0]<b]
    W,H=1080,1920
    ass=["[Script Info]","ScriptType: v4.00+",f"PlayResX: {W}",f"PlayResY: {H}","WrapStyle: 2","","[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: T,Noto Sans CJK KR,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,3,8,60,60,250,1",
    "Style: C,Noto Sans CJK KR,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,2,8,70,70,1270,1",
    "Style: A,Noto Sans CJK KR,44,&H0060C8FF,&H0060C8FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,60,60,120,1",
    "","[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    D=b-a
    ass.append(f"Dialogue: 1,{at(0)},{at(D)},T,,0,0,0,,{title}")
    ass.append(f"Dialogue: 1,{at(0)},{at(D)},A,,0,0,0,,{cta}")
    for s,e,tx in cues:
        ass.append(f"Dialogue: 0,{at(max(0,s-a))},{at(min(D,e-a+0.15))},C,,0,0,0,,{{\\fad(120,120)}}{wrap(tx,16 if ko else 30,ko)}")
    open(f"{name}.ass","w").write("\n".join(ass))
    fc=(f"[0:v]split[a][b];[a]crop=1920:1080,scale=-2:1920,crop={W}:{H},boxblur=30:3,eq=brightness=-0.25[bg];"
        f"[b]crop=1920:800:0:0,scale={W}:-2[fg];[bg][fg]overlay=0:700,subtitles={name}.ass:fontsdir=/usr/share/fonts/opentype/noto,"
        f"fade=t=in:st=0:d=0.4,fade=t=out:st={D-0.5:.2f}:d=0.5,format=yuv420p[v];[0:a]afade=t=in:d=0.3,afade=t=out:st={D-0.5:.2f}:d=0.5[au]")
    subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",f"{a:.2f}","-t",f"{D:.2f}","-i",video,"-filter_complex",fc,"-map","[v]","-map","[au]",
        "-c:v","libx264","-preset","veryfast","-crf","21","-c:a","aac","-b:a","160k","-movflags","+faststart",f"{O}/{name}.mp4"],check=True)
KV="/mnt/user-data/outputs/당신만의게임_EP004_물병자리시대.mp4"; KS="/mnt/user-data/outputs/pyog_ep004.srt"
EV="/mnt/user-data/outputs/PlayYourOwnGame_EP004_Age_of_Aquarius.mp4"; ES="/mnt/user-data/outputs/PlayYourOwnGame_EP004_captions.srt"
KC="전체 이야기는 채널에서 ▶ 당신만의 게임"; EC="Full story on the channel ▶ Play Your Own Game"
jobs=[("KR1_잘사는사람이바뀐다",KV,KS,435.0,486.3,"물병자리 시대,\\N잘 사는 사람이 바뀝니다",KC,True),
("KR2_물병의물",KV,KS,580.0,633.8,"물병자리가 붓는 물,\\N사실 물이 아니에요",KC,True),
("KR3_차원상승",KV,KS,691.6,746.2,"차원 상승,\\N어디로 가는 걸까요?",KC,True),
("EN1_who_thrives",EV,ES,405.0,459.4,"The Age of Aquarius:\\NWho Thrives Now",EC,False),
("EN2_not_water",EV,ES,539.6,595.5,"Aquarius Isn't\\NPouring Water",EC,False),
("EN3_ascension",EV,ES,644.1,693.4,"Ascension Isn't\\NWhat You Think",EC,False)]
for j in jobs: make(*j); print("ok",j[0])
