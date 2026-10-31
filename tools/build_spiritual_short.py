"""Compose a vertical spiritual Short from assets made by the pipeline's assets mode.

Usage: python3 tools/build_spiritual_short.py specs/pyog_sh01_xxx.json OUT.mp4 [music.mp3]
Assets expected in outputs/shorts/<id>/: l00.mp3.. (voice per line), img_00..03.jpg, anim_00.mp4 (optional).
"""
import json, pathlib, re, subprocess, sys, textwrap

W, H, FPS = 1080, 1920, 30
FONT_DIR = "/usr/share/fonts/opentype/noto"


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def at(x):
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


def wrap_ko(t, w=13):
    words, lines, cur = t.split(" "), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > w and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    lines.append(cur)
    return "\\N".join(lines)


def main(spec_path, out, music=None):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    src = pathlib.Path("outputs/shorts") / spec["id"]
    work = pathlib.Path("/tmp/spshort") / spec["id"]
    work.mkdir(parents=True, exist_ok=True)
    voices = spec["assets"]["voices"]
    # --- narration: lines back to back with a short breath between them
    gap, t, events, parts = 0.25, 0.3, [], []
    for v in voices:
        f = src / f"voice_{v['name']}.mp3"
        d = dur(f)
        text = v.get("caption") or re.sub(r"<#[\d.]+#>", "", v["text"]).replace("  ", " ").strip()
        events.append((t, t + d, text))
        parts.append((f, t))
        t += d + gap
    total = t + 0.6
    args, fc = [], []
    for i, (f, st) in enumerate(parts):
        args += ["-i", str(f)]
        fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
    run(["ffmpeg", "-y", *args, "-filter_complex",
         ";".join(fc) + ";" + "".join(f"[a{i}]" for i in range(len(parts))) +
         f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total:.2f}[m]", "-map", "[m]", str(work / "nar.wav")])
    # --- visuals: motion clip first, then paintings with alternating slow push / pull
    imgs = sorted(src.glob("img_*.jpg"))
    anim = src / "anim_00.mp4"
    clips = []
    if anim.exists():
        clips.append(("video", anim))
        imgs = imgs[1:]
    for p in imgs:  # two different moves per painting so the picture changes every ~4 s
        clips += [("image", p), ("image2", p)]
    each = total / len(clips)
    segs = []
    for k, (kind, f) in enumerate(clips):
        fr = int(round(each * FPS))
        o = work / f"c{k}.mp4"
        fade = f"fade=t=in:st=0:d=0.15,fade=t=out:st={each-0.15:.2f}:d=0.15"
        if kind == "video":
            run(["ffmpeg", "-y", "-i", str(f), "-an", "-vf",
                 f"setpts={max(1.0, each / 5.8):.3f}*PTS,tpad=stop_mode=clone:stop_duration=20,fps={FPS},"
                 f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,{fade},format=yuv420p",
                 "-frames:v", str(fr), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(o)])
        else:
            if kind == "image":  # quick push in to the centre
                zp = f"z='1+0.18*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            else:  # tight framing drifting from top to bottom
                zp = f"z='1.35':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*on/{fr}'"
            run(["ffmpeg", "-y", "-loop", "1", "-i", str(f), "-vf",
                 f"scale={W*2}:{H*2},zoompan={zp}:d={fr}:s={W}x{H}:fps={FPS},"
                 f"{fade},format=yuv420p", "-frames:v", str(fr), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                 str(o)])
        segs.append(o)
    (work / "list.txt").write_text("".join(f"file '{s}'\n" for s in segs))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"), "-c", "copy", str(work / "v.mp4")])
    # --- text: hook at the top all the way through, big captions in the lower middle
    hook = spec.get("hook", "")
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
           "MarginR, MarginV, Encoding",
           "Style: Hook,Noto Sans CJK KR,92,&H0040D0FF,&H0040D0FF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,1,6,4,8,60,60,230,1",
           "Style: Cap,Noto Sans CJK KR,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,1,5,3,8,70,70,1180,1",
           "Style: Brand,Noto Sans CJK KR,40,&H90FFFFFF,&H90FFFFFF,&H90000000,&H00000000,1,0,0,0,100,100,2,0,1,2,0,2,60,60,110,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    ass.append(f"Dialogue: 2,{at(0)},{at(total)},Hook,,0,0,0,,{{\\fad(0,300)}}{wrap_ko(hook, 12)}")
    ass.append(f"Dialogue: 1,{at(0)},{at(total)},Brand,,0,0,0,,{spec.get('brand', '당신만의 게임')}")
    for st, en, tx in events:
        ass.append(f"Dialogue: 0,{at(st)},{at(en + 0.1)},Cap,,0,0,0,,{{\\fad(80,80)}}{wrap_ko(tx)}")
    (work / "t.ass").write_text("\n".join(ass))
    music = music or "outputs/shorts/pyog_test1/music.mp3"
    run(["ffmpeg", "-y", "-i", str(work / "v.mp4"), "-i", str(work / "nar.wav"), "-stream_loop", "-1", "-i", music,
         "-filter_complex",
         f"[0:v]subtitles={work / 't.ass'}:fontsdir={FONT_DIR},vignette=PI/5[v];"
         f"[2:a]atrim=0:{total:.2f},volume=0.22,afade=t=out:st={total-1:.2f}:d=1[mu];"
         f"[1:a][mu]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
         "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])
    print(f"ok {out} {total:.1f}s")


if __name__ == "__main__":
    main(*sys.argv[1:])
