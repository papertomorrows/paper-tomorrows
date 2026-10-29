"""Calm spiritual long-form style test: slow drifting images, crossfades, voice + soft music.

Usage: python3 tools/build_pyog_test.py ASSET_DIR VOICE_FILE OUT_MP4
"""
import pathlib
import subprocess
import sys

A = pathlib.Path(sys.argv[1])
VOICE = pathlib.Path(sys.argv[2])
OUT = pathlib.Path(sys.argv[3])
W, H, FPS, XF = 1920, 1080, 30, 1.5


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


imgs = sorted(A.glob("img_*.jpg"))
total = dur(VOICE) + 3.0                      # 1 s lead-in, 2 s tail
n = len(imgs)
seg = (total + XF * (n - 1)) / n              # each image incl. crossfade overlap
frames = int(seg * FPS)
inputs, parts = [], []
for i, im in enumerate(imgs):
    inputs += ["-loop", "1", "-t", f"{seg:.2f}", "-i", str(im)]
    zin = i % 2 == 0                           # alternate slow push-in / pull-out
    z = f"'min(1+0.10*on/{frames},1.10)'" if zin else f"'max(1.10-0.10*on/{frames},1.0)'"
    parts.append(f"[{i}:v]scale=3840:2160,zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                 f"d={frames}:s={W}x{H}:fps={FPS},setsar=1[v{i}]")
chain, last = [], "v0"
for i in range(1, n):
    off = i * (seg - XF)
    chain.append(f"[{last}][v{i}]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}]")
    last = f"x{i}"
grade = f"[{last}]eq=contrast=1.04:saturation=1.08,vignette=PI/6,noise=alls=3:allf=t,format=yuv420p[v]"
vi = len(imgs)
audio = (f"[{vi}:a]adelay=1000|1000,apad,atrim=0:{total:.2f}[vo];"
         f"[{vi + 1}:a]aloop=loop=-1:size=2e9,atrim=0:{total:.2f},volume=0.16,"
         f"afade=t=in:d=2,afade=t=out:st={total - 3:.2f}:d=3[mu];"
         f"[vo][mu]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5[a]")
fc = ";".join(parts + chain + [grade, audio])
subprocess.run(["ffmpeg", "-y", *inputs, "-i", str(VOICE), "-i", str(A / "music.mp3"), "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium",
                "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(OUT)],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
print("OK", OUT, round(dur(OUT), 1))
