"""Play Your Own Game - calm Korean spiritual long-form pipeline.

Run: modal run modal_app/pyog.py --spec specs/pyog_ep001.json

The spec points to a Markdown script (pyog/*.md). Sections start with
<!-- section: name | visuals: kw1, kw2, ... -->. Every sentence is voiced on its own
(MiniMax Speech 2.8 HD via fal), so captions are timed exactly. Visuals are free
Pixabay stock videos found by the section keywords (AI image only as a fallback).
"""

import hashlib
import json
import math
import pathlib
import random
import re

import modal

app = modal.App("pyog-longform")
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "fonts-noto-cjk")
    .pip_install("fal-client", "requests")
)
KEYS = modal.Secret.from_name("paper-tomorrows-keys")
CACHE = modal.Volume.from_name("paper-tomorrows-cache", create_if_missing=True)
W, H, FPS = 1920, 1080, 30
CLIP = 7.0   # seconds each stock clip stays on screen


def key(t: str) -> str:
    return hashlib.sha1(t.encode()).hexdigest()[:12]


@app.function(image=image, timeout=600, secrets=[KEYS], max_containers=8)
def tts(text: str, voice_id: str, speed: float) -> bytes:
    import fal_client
    import requests

    res = fal_client.subscribe("fal-ai/minimax/speech-2.8-hd", arguments={
        "prompt": text, "language_boost": "Korean", "output_format": "url",
        "voice_setting": {"voice_id": voice_id, "speed": speed, "vol": 1, "pitch": 0}})
    return requests.get(res["audio"]["url"], timeout=120).content


@app.function(image=image, timeout=600, secrets=[KEYS])
def fallback_image(prompt: str, seed: int) -> bytes:
    import fal_client
    import requests

    res = fal_client.subscribe("fal-ai/flux-2-pro", arguments={
        "prompt": prompt, "seed": seed, "output_format": "jpeg", "image_size": {"width": W, "height": H}})
    return requests.get(res["images"][0]["url"], timeout=120).content


def parse_script(md: str):
    sections = []
    for block in re.split(r"<!--\s*section:", md)[1:]:
        head, body = block.split("-->", 1)
        name, _, vis = head.partition("| visuals:")
        paras = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
        sents = []
        for pi, p in enumerate(paras):
            p = p.replace("...", "…")
            parts = [s.strip() for s in re.split(r"(?<=[.?!])\s+", p) if s.strip()]
            for si, s in enumerate(parts):
                sents.append({"text": s, "para_end": si == len(parts) - 1})
        sections.append({"name": name.strip(), "visuals": [v.strip() for v in vis.split(",") if v.strip()],
                         "sentences": sents})
    return sections


def wrap(text: str, width: int = 22) -> str:
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return "\\N".join(lines)


def ass_time(t: float) -> str:
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


@app.function(image=image, timeout=3000, secrets=[KEYS], volumes={"/cache": CACHE}, cpu=4, memory=8192)
def produce(spec: dict, script_md: str, music: bytes) -> dict:
    import os
    import subprocess

    import requests

    def run(cmd):
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    def dur(p):
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                     "csv=p=0", str(p)], capture_output=True, text=True).stdout)

    cache = pathlib.Path("/cache/pyog")
    (cache / "tts").mkdir(parents=True, exist_ok=True)
    (cache / "stock").mkdir(parents=True, exist_ok=True)
    work = pathlib.Path("/tmp/pyog")
    work.mkdir(parents=True, exist_ok=True)
    voice, speed = spec.get("voice_id", "Korean_CalmGentleman"), float(spec.get("speed", 0.92))
    sections = parse_script(script_md)

    # ---- voice: one clip per sentence (cached)
    allsent = [s for sec in sections for s in sec["sentences"]]
    todo = []
    for s in allsent:
        s["file"] = cache / "tts" / f"{key(s['text'] + voice + str(speed))}.mp3"
        if not s["file"].exists():
            todo.append(s)
    for s, audio in zip(todo, tts.starmap([(s["text"], voice, speed) for s in todo])):
        s["file"].write_bytes(audio)
    CACHE.commit()
    print(f"STEP voice: {len(todo)} new sentences, {len(allsent) - len(todo)} cached")

    # ---- timeline with calm pauses
    t, events, inputs = 1.0, [], []
    for si, sec in enumerate(sections):
        sec["start"] = t
        for s in sec["sentences"]:
            d = dur(s["file"])
            events.append((t, t + d, s["text"]))
            inputs.append((s["file"], t))
            t += d + (0.9 if s["para_end"] else 0.35)
        t += 0.8
        sec["end"] = t
    total = t + 2.0

    # ---- narration track
    nar = work / "narration.wav"
    # mix in chunks to keep the filter graph small
    chunk_files = []
    for c in range(0, len(inputs), 40):
        sub_args, sub_fc, sub_lab = [], [], []
        for j, (f, st) in enumerate(inputs[c:c + 40]):
            sub_args += ["-i", str(f)]
            sub_fc.append(f"[{j}:a]aresample=48000,aformat=channel_layouts=stereo,"
                          f"adelay={int(st * 1000)}|{int(st * 1000)}[a{j}]")
            sub_lab.append(f"[a{j}]")
        cf = work / f"nar_{c}.wav"
        run(["ffmpeg", "-y", *sub_args, "-filter_complex",
             ";".join(sub_fc) + ";" + "".join(sub_lab) + f"amix=inputs={len(sub_lab)}:normalize=0:duration=longest,"
             f"apad,atrim=0:{total:.2f}[m]", "-map", "[m]", str(cf)])
        chunk_files.append(cf)
    if len(chunk_files) == 1:
        chunk_files[0].rename(nar)
    else:
        run(["ffmpeg", "-y", *sum([["-i", str(c)] for c in chunk_files], []), "-filter_complex",
             "".join(f"[{i}:a]" for i in range(len(chunk_files))) +
             f"amix=inputs={len(chunk_files)}:normalize=0:duration=longest[m]", "-map", "[m]", str(nar)])

    # ---- stock clips per section (Pixabay): most relevant first, skip near-black clips
    pkey = os.environ.get("PIXABAY_API_KEY", "")
    used, clip_files, fallbacks, dark = set(), [], 0, 0
    min_luma = float(spec.get("min_luma", 55))

    def luma(f):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "2", "-i", str(f), "-frames:v", "1", "-vf",
                              "scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        return sum(raw) / max(len(raw), 1)

    for sec in sections:
        need = max(1, math.ceil((sec["end"] - sec["start"]) / CLIP))
        lists = []
        for kw in sec["visuals"] or ["calm nature"]:
            hits = []
            try:
                r = requests.get("https://pixabay.com/api/videos/", timeout=30, params={
                    "key": pkey, "q": kw, "per_page": 30, "safesearch": "true", "video_type": "film",
                    "order": "popular"}).json()
                for h in r.get("hits", []):
                    v = h["videos"].get("large") or h["videos"].get("medium")
                    if v and v.get("url") and h["duration"] >= CLIP + 2 and v.get("width", 1920) >= 1280:
                        hits.append((h["id"], v["url"], kw))
            except Exception as exc:
                print(f"PIXABAY FAILED '{kw}': {str(exc)[:200]}")
            lists.append(hits)
        picked = []
        depth = 0
        while len(picked) < need and any(depth < len(l) for l in lists):
            for l in lists:  # round-robin over keywords, best-ranked first
                if depth < len(l) and len(picked) < need:
                    cid, url, kw = l[depth]
                    if cid in used:
                        continue
                    f = cache / "stock" / f"px_{cid}.mp4"
                    if not f.exists():
                        try:
                            f.write_bytes(requests.get(url, timeout=300).content)
                        except Exception:
                            continue
                    used.add(cid)
                    if luma(f) < min_luma:
                        dark += 1
                        continue
                    picked.append(f)
            depth += 1
        sec["clips"] = [("video", f) for f in picked]
        clip_files += sec["clips"]
        for k in range(need - len(picked)):  # not enough stock: calm AI image instead
            prompt = (f"{(sec['visuals'] or ['calm cosmos'])[k % max(1, len(sec['visuals']))]}, cinematic, dreamy, "
                      "soft volumetric light, peaceful spiritual atmosphere, no text, no watermark")
            f = cache / "stock" / f"ai_{key(prompt)}.jpg"
            if not f.exists():
                if fallbacks >= int(spec.get("max_ai_fallbacks", 99)):
                    pool = sec["clips"] or clip_files  # budget reached: reuse a clip instead of paying
                    if pool:
                        sec["clips"].append(pool[k % len(pool)])
                        clip_files.append(pool[k % len(pool)])
                        continue
                f.write_bytes(fallback_image.remote(prompt, 100 + k))
                fallbacks += 1
            clip_files.append(("image", f))
            sec["clips"].append(("image", f))
    print(f"STEP visuals: skipped {dark} dark clips")
    CACHE.commit()
    print(f"STEP visuals: {len(clip_files)} clips ({fallbacks} AI fallbacks)")

    # ---- render clips section by section so pictures stay with their words
    segs, i = [], 0
    for si, sec in enumerate(sections):
        a = 0.0 if si == 0 else sections[si - 1]["end"]
        b = total if si == len(sections) - 1 else sec["end"]
        clips = sec["clips"] or clip_files[:1]
        d_each = (b - a) / len(clips)
        for kind, f in clips:
            D = round(d_each, 3)
            out = work / f"c{i:03d}.mp4"
            i += 1
            fade = f"fade=t=in:st=0:d=0.6,fade=t=out:st={D - 0.6:.3f}:d=0.6"
            base = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS},"
                    f"eq=contrast=1.03:saturation=1.05,{fade},format=yuv420p")
            fr = int(round(D * FPS))
            if kind == "video":
                run(["ffmpeg", "-y", "-ss", "1", "-i", str(f), "-an", "-vf",
                     f"setpts=1.15*PTS,tpad=stop_mode=clone:stop_duration=10,{base}", "-frames:v", str(fr),
                     "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(out)])
            else:
                run(["ffmpeg", "-y", "-loop", "1", "-i", str(f), "-vf",
                     f"scale=3840:2160,zoompan=z='min(1+0.08*on/{fr},1.08)':x='iw/2-(iw/zoom/2)':"
                     f"y='ih/2-(ih/zoom/2)':d={fr}:s={W}x{H}:fps={FPS},{fade},format=yuv420p",
                     "-frames:v", str(fr), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(out)])
            segs.append(out)
    (work / "list.txt").write_text("".join(f"file '{s}'\n" for s in segs))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"), "-c", "copy",
         str(work / "joined.mp4")])

    # ---- captions
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "",
           "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
           "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
           "Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Cap,Noto Sans CJK KR,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,"
           "3.5,2,2,140,140,80,1", "", "[Events]",
           "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for st, en, tx in events:
        ass.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en + 0.15)},Cap,,0,0,0,,{{\\fad(150,150)}}{wrap(tx)}")
    (work / "cap.ass").write_text("\n".join(ass))
    srt = []
    for i, (st, en, tx) in enumerate(events, 1):
        def ts(x):
            ms = int(x * 1000)
            return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
        srt.append(f"{i}\n{ts(st)} --> {ts(en)}\n{tx}\n")

    # ---- final mix
    (work / "music.mp3").write_bytes(music)
    final = work / "final.mp4"
    caps = f"subtitles={work / 'cap.ass'}:fontsdir=/usr/share/fonts/opentype/noto," if spec.get("captions", True) else ""
    run(["ffmpeg", "-y", "-i", str(work / "joined.mp4"), "-i", str(nar), "-i", str(work / "music.mp3"),
         "-filter_complex",
         f"[0:v]{caps}vignette=PI/6[v];"
         f"[1:a]asplit=2[vo][key];"
         f"[2:a]aloop=loop=-1:size=2e9,atrim=0:{total:.2f},volume=0.20,afade=t=in:d=3,"
         f"afade=t=out:st={total - 4:.2f}:d=4[mu];"
         f"[mu][key]sidechaincompress=threshold=0.02:ratio=4:attack=30:release=600[duck];"
         f"[vo][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium",
         "-crf", "23", "-maxrate", "4M", "-bufsize", "8M", "-c:a", "aac", "-b:a", "160k",
         "-movflags", "+faststart", str(final)], )
    return {"video": final.read_bytes(), "srt": "\n".join(srt),
            "report": {"duration": round(total, 1), "sentences": len(events), "clips": len(clip_files),
                       "ai_fallbacks": fallbacks, "chars": sum(len(e[2]) for e in events)}}


@app.local_entrypoint()
def main(spec: str):
    s = json.loads(pathlib.Path(spec).read_text())
    md = pathlib.Path(s["script"]).read_text()
    music = pathlib.Path(s["music"]).read_bytes()
    r = produce.remote(s, md, music)
    out = pathlib.Path("outputs/longform") / s["id"]
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{s['id']}.mp4").write_bytes(r["video"])
    (out / f"{s['id']}.srt").write_text(r["srt"])
    (out / "report.json").write_text(json.dumps(r["report"], indent=1))
    print(f"SHORT OK id={s['id']} {r['report']} size={len(r['video']) // 1024}KB")
