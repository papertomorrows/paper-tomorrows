"""Build long-form #1: '6 Buildings the World Almost Built' (16:9) from the Never Built shorts.

Run from the repo root: python3 tools/build_longform_lf001.py OUTDIR
"""
import json
import pathlib
import subprocess
import sys

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
SH = pathlib.Path("outputs/shorts")
VO = SH / "lf001_never_built_six" / "voice"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H, FPS = 1920, 1080, 30

ORDER = [  # countdown: weakest first, strongest last
    ("n6", "006_newton_cenotaph", "#6", "A MONUMENT FOR NEWTON"),
    ("n5", "005_tatlins_tower", "#5", "THE TOWER THAT SPINS"),
    ("n4", "004_watkins_tower", "#4", "LONDON'S EIFFEL TOWER"),
    ("n3", "003_shimizu_pyramid", "#3", "A CITY IN A PYRAMID"),
    ("n2", "002_atlantropa", "#2", "DRAIN THE MEDITERRANEAN"),
    ("n1", "001_mile_high", "#1", "THE MILE-HIGH SKYSCRAPER"),
]


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def esc(t):
    return t.replace("'", "’").replace(":", "\\:")


ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
# vertical clip centred on a blurred, darkened copy of itself
WIDE = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"gblur=sigma=40,eq=brightness=-0.18[bg];[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0,fps={FPS}")


def short_segment(name, out):
    src = SH / name / "short.mp4"
    run(["ffmpeg", "-y", "-i", str(src), "-filter_complex", WIDE + "[v]", "-map", "[v]", "-map", "0:a", *ENC, str(out)])


def card(src_video, at, voice, big, small, out, extra=0.5):
    d = dur(voice) + extra
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=25,eq=brightness=-0.35,"
          f"zoompan=z='1+0.0008*on':d={int(d * FPS)}:s={W}x{H}:fps={FPS},"
          f"drawtext=fontfile={FONT}:text='{esc(big)}':fontsize=260:fontcolor=0xFFC83C:x=(w-tw)/2:y=h*0.30-th/2:"
          f"borderw=6:bordercolor=black,"
          f"drawtext=fontfile={FONT}:text='{esc(small)}':fontsize=84:fontcolor=white:x=(w-tw)/2:y=h*0.62:"
          f"borderw=4:bordercolor=black")
    run(["ffmpeg", "-y", "-ss", str(at), "-i", str(src_video), "-i", str(voice), "-filter_complex",
         f"[0:v]trim=end_frame=1,{vf}[v];[1:a]apad,atrim=0:{d:.2f}[a]", "-map", "[v]", "-map", "[a]",
         "-t", f"{d:.2f}", *ENC, str(out)])
    return d


def intro(out):
    d = dur(VO / "intro.mp3") + 0.6
    per = d / len(ORDER)
    parts = []
    for i, (_, name, _, _) in enumerate(reversed(ORDER)):  # strongest first in the teaser
        src = SH / name / "short.mp4"
        p = OUT / f"teaser_{i}.mp4"
        at = min(dur(src) * 0.45, dur(src) - per - 0.5)
        run(["ffmpeg", "-y", "-ss", f"{at:.2f}", "-t", f"{per:.2f}", "-i", str(src), "-filter_complex", WIDE + "[v]",
             "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", str(p)])
        parts.append(p)
    lst = OUT / "teaser.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(OUT / "teaser.mp4")])
    title = (f"drawtext=fontfile={FONT}:text='6 BUILDINGS':fontsize=150:fontcolor=0xFFC83C:x=(w-tw)/2:y=h*0.36:"
             f"borderw=6:bordercolor=black:enable='gte(t,{d - 3.2:.2f})',"
             f"drawtext=fontfile={FONT}:text='THE WORLD ALMOST BUILT':fontsize=90:fontcolor=white:x=(w-tw)/2:y=h*0.52:"
             f"borderw=5:bordercolor=black:enable='gte(t,{d - 3.2:.2f})'")
    run(["ffmpeg", "-y", "-i", str(OUT / "teaser.mp4"), "-i", str(VO / "intro.mp3"), "-filter_complex",
         f"[0:v]{title}[v];[1:a]apad,atrim=0:{d:.2f}[a]", "-map", "[v]", "-map", "[a]", "-t", f"{d:.2f}", *ENC, str(out)])
    return d


segs, chapters, t = [], [], 0.0
p = OUT / "s00_intro.mp4"
t += intro(p)
segs.append(p)
for i, (vo, name, num, title) in enumerate(ORDER):
    chapters.append((t, f"{num} {title.title()}"))
    src = SH / name / "short.mp4"
    c = OUT / f"s{i + 1:02d}a_card.mp4"
    t += card(src, dur(src) * 0.3, VO / f"{vo}.mp3", num, title, c)
    s = OUT / f"s{i + 1:02d}b_short.mp4"
    short_segment(name, s)
    t += dur(s)
    segs += [c, s]
last = SH / ORDER[-1][1] / "short.mp4"
o = OUT / "s99_outro.mp4"
chapters.append((t, "Which one should have been built?"))
t += card(last, dur(last) - 1.0, VO / "outro.mp3", "?", "WHICH ONE SHOULD HAVE BEEN BUILT", o, extra=1.5)
segs.append(o)

lst = OUT / "all.txt"
lst.write_text("".join(f"file '{p.resolve()}'\n" for p in segs))
final = OUT / "longform_lf001_six_buildings.mp4"
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
     *ENC, "-movflags", "+faststart", str(final)])
chap_text = "0:00 Intro\n" + "\n".join(f"{int(s // 60)}:{int(s % 60):02d} {n}" for s, n in chapters)
(OUT / "chapters.txt").write_text(chap_text)
print(chap_text)
print("TOTAL", round(dur(final), 1), final)
