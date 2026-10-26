"""Paper Tomorrows - generic Shorts pipeline.

Run:  modal run modal_app/pipeline.py --spec specs/001_mile_high.json

A spec file describes one short: narration lines, one or two shots per line
(still image with a camera move, or an animated "motion" shot), sound-effect cues,
music prompt and upload metadata. Everything generated is cached in a Modal volume,
keyed by its prompt, so editing a spec only regenerates what actually changed.
"""

import hashlib
import json
import os
import pathlib

import modal

app = modal.App("paper-tomorrows-pipeline")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "fonts-dejavu-core")
    .pip_install("fal-client", "requests")
)

KEYS = modal.Secret.from_name("paper-tomorrows-keys")
CACHE = modal.Volume.from_name("paper-tomorrows-cache", create_if_missing=True)

W, H, FPS = 1080, 1920, 30

# ---------------------------------------------------------------- channel defaults

DEFAULTS = {
    "style": (
        "Cinematic matte painting, painterly brushwork with near-photographic lighting, "
        "volumetric haze, subtle film grain, muted gold and deep blue colour palette, "
        "vertical composition. No text, no lettering, no signage, no watermark."
    ),
    "voice_id": "nPczCjzI2devNBz1zQrb",  # Brian
    "voice_model": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.35, "similarity_boost": 0.80, "style": 0.40,
        "use_speaker_boost": True, "speed": 0.94,
    },
    "music_prompt": (
        "Slow cinematic ambient underscore, warm analog synth pads, soft low strings, "
        "gentle sense of wonder and mystery, documentary score, no drums, no vocals, "
        "steady and calm, 70 bpm"
    ),
    "label": "AI CONCEPT VISUALIZATION",
    "label_seconds": 3.0,
    "min_split_seconds": 2.4,   # a line shorter than this keeps a single shot
    "min_first_shot": 2.4,      # the opening shot always lasts at least this long
}

SFX_PROMPTS = {
    "whoosh": ("Fast airy cinematic whoosh transition, clean swoosh sound effect, "
               "no music, no voice", 2),
    "impact": ("Deep cinematic boom impact with a long low rumble tail, sound effect, "
               "no music, no voice", 4),
    "riser": ("Slow rising cinematic tension riser building suspense, sound effect, "
              "no music, no voice", 4),
}

MOTION_NEGATIVE = "warping, melting, bending buildings, morphing, blur, distortion, text"


def key(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:10]


# ---------------------------------------------------------------- generators

@app.function(image=image, timeout=900, secrets=[KEYS])
def generate_image(prompt: str, seed: int) -> tuple[str, bytes]:
    import fal_client
    import requests

    args = {"prompt": prompt, "seed": seed, "output_format": "jpeg"}
    try:
        res = fal_client.subscribe(
            "fal-ai/flux-2-pro", arguments={**args, "image_size": {"width": W, "height": H}}
        )
    except Exception as exc:
        print(f"custom size failed: {str(exc)[:200]}")
        res = fal_client.subscribe(
            "fal-ai/flux-2-pro", arguments={**args, "image_size": "portrait_16_9"}
        )
    url = res["images"][0]["url"]
    return url, requests.get(url, timeout=120).content


@app.function(image=image, timeout=1500, secrets=[KEYS])
def generate_motion(image_url: str, motion_prompt: str) -> bytes:
    import fal_client
    import requests

    res = fal_client.subscribe(
        "fal-ai/kling-video/v3/pro/image-to-video",
        arguments={
            "start_image_url": image_url,
            "prompt": motion_prompt,
            "duration": "5",
            "generate_audio": False,
            "negative_prompt": MOTION_NEGATIVE,
        },
    )
    return requests.get(res["video"]["url"], timeout=300).content


@app.function(image=image, timeout=600, secrets=[KEYS])
def narrate(text: str, voice_id: str, model: str, settings: dict) -> tuple[bytes, dict]:
    import base64

    import requests

    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps",
        headers={"xi-api-key": os.environ["XI_KEY"], "Content-Type": "application/json"},
        params={"output_format": "mp3_44100_128"},
        json={"text": text, "model_id": model, "voice_settings": settings},
        timeout=300,
    )
    if not r.ok:
        raise RuntimeError(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    data = r.json()
    return base64.b64decode(data["audio_base64"]), data["alignment"]


@app.function(image=image, timeout=900, secrets=[KEYS])
def generate_audio(prompt: str, seconds: int) -> bytes:
    """Music or sound effects via Stable Audio 2.5 (trained on licensed data)."""
    import fal_client
    import requests

    last = None
    for args in ({"prompt": prompt, "seconds_total": seconds},
                 {"prompt": prompt, "duration": seconds},
                 {"prompt": prompt}):
        try:
            res = fal_client.subscribe("fal-ai/stable-audio-25/text-to-audio", arguments=args)
            audio = res.get("audio") or res.get("audio_file") or res.get("output")
            url = audio["url"] if isinstance(audio, dict) else audio
            return requests.get(url, timeout=120).content
        except Exception as exc:
            print(f"audio attempt failed ({list(args)}): {str(exc)[:200]}")
            last = exc
    raise RuntimeError(f"audio generation failed: {last}")


# ---------------------------------------------------------------- editing helpers

def run(cmd: list[str]) -> None:
    import subprocess

    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + p.stderr[-2000:])


def media_duration(path) -> float:
    import subprocess

    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(path)], capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def ass_time(t: float) -> str:
    t = max(t, 0)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def words_from_alignment(align: dict) -> list[tuple[str, float, float]]:
    words, cur, ws, we = [], "", None, None
    for ch, s, e in zip(align["characters"], align["character_start_times_seconds"],
                        align["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append((cur, ws, we))
            cur, ws = "", None
            continue
        if ws is None:
            ws = s
        cur += ch
        we = e
    if cur:
        words.append((cur, ws, we))
    return words


def clean_word(w: str) -> str:
    w = w.replace("...", "").replace(",", "").replace("{", "").replace("}", "")
    return w.strip(" .").upper()


def caption_chunks(words):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        text_len = len(" ".join(x[0] for x in cur))
        if len(cur) >= 3 or text_len >= 14 or w[0].rstrip('"').endswith((".", "?", "!", ",")):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def build_ass(chunks, label: str, label_seconds: float) -> str:
    gold = "&H3CC8FF&"   # #FFC83C in ASS BGR order
    white = "&HFFFFFF&"
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,DejaVu Sans,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,6,2,2,80,80,430,1
Style: Label,DejaVu Sans,26,&H00E6E6E6,&H00E6E6E6,&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,2,0,8,60,60,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    if label:
        events.append(f"Dialogue: 1,{ass_time(0)},{ass_time(label_seconds)},Label,,0,0,0,,"
                      f"{{\\fad(200,500)}}{label}")
    plain = []
    for ci, chunk in enumerate(chunks):
        chunk_end = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else chunk[-1][2] + 0.4
        texts = [clean_word(w[0]) for w in chunk]
        for wi, w in enumerate(chunk):
            start = chunk[0][1] if wi == 0 else w[1]
            end = chunk[wi + 1][1] if wi + 1 < len(chunk) else chunk_end
            parts = [f"{{\\c{gold}}}{t}{{\\c{white}}}" if j == wi else t
                     for j, t in enumerate(texts) if t]
            if not parts:
                continue
            events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Caption,,0,0,0,,"
                          + " ".join(parts))
        plain.append((round(chunk[0][1], 2), round(chunk_end, 2), " ".join(t for t in texts if t)))
    return header + "\n".join(events) + "\n", plain


def camera_filter(move: str, frames: int) -> str:
    big_w, big_h = W * 2, H * 2
    d = max(frames, 1)
    if move == "push_in":
        z, x, y = f"1+0.12*on/{d}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif move == "pull_out":
        z, x, y = f"1.12-0.12*on/{d}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif move == "pan_down":
        z, x, y = "1.12", "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*(on/{d})"
    else:  # pan_up
        z, x, y = "1.12", "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*(1-on/{d})"
    return (
        f"scale={big_w}:{big_h}:force_original_aspect_ratio=increase,crop={big_w}:{big_h},"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={d}:s={W}x{H}:fps={FPS},format=yuv420p"
    )


def plan_shots(lines, line_starts, total, cfg):
    """Returns a list of (line_index, shot_index, start, end)."""
    bounds = line_starts + [total]
    shots = []
    for li, line in enumerate(lines):
        s, e = bounds[li], bounds[li + 1]
        n = len(line["shots"])
        if n >= 2 and (e - s) >= cfg["min_split_seconds"]:
            mid = s + (e - s) / 2
            shots += [(li, 0, s, mid), (li, 1, mid, e)]
        else:
            shots.append((li, 0, s, e))
    # keep the opening shot on screen long enough to hook the viewer
    if shots and shots[0][3] < cfg["min_first_shot"] and len(shots) > 1:
        new_end = cfg["min_first_shot"]
        li, si, s, _ = shots[0]
        shots[0] = (li, si, s, new_end)
        while len(shots) > 1 and shots[1][3] - new_end < 0.8:
            shots.pop(1)
            shots[0] = (li, si, s, new_end)
        if len(shots) > 1:
            l2, s2, _, e2 = shots[1]
            shots[1] = (l2, s2, new_end, e2)
    return shots


def legacy_lookup(legacy_dir: pathlib.Path, pattern: str):
    if not legacy_dir or not legacy_dir.exists():
        return None
    hits = sorted(legacy_dir.glob(pattern))
    return hits[0] if hits else None


# ---------------------------------------------------------------- production

@app.function(image=image, timeout=3000, cpu=4.0, memory=4096, secrets=[KEYS],
              volumes={"/cache": CACHE})
def produce(spec: dict) -> dict:
    cfg = {**DEFAULTS, **spec.get("settings", {})}
    style = spec.get("style", cfg["style"])
    music_prompt = spec.get("music_prompt", cfg["music_prompt"])
    lines = spec["lines"]
    seed_base = int(spec.get("seed_base", 1000))

    cache = pathlib.Path("/cache") / spec["id"]
    cache.mkdir(parents=True, exist_ok=True)
    legacy = pathlib.Path("/cache") / spec["legacy_cache"] if spec.get("legacy_cache") else None
    work = pathlib.Path("/tmp/short")
    work.mkdir(parents=True, exist_ok=True)

    def have(name):
        return (cache / name).exists()

    def adopt(name, pattern):  # reuse a file made before this pipeline existed
        if not have(name):
            hit = legacy_lookup(legacy, pattern)
            if hit:
                (cache / name).write_bytes(hit.read_bytes())

    # ---- narration
    text = " ".join(l["text"] for l in lines)
    nkey = key(text + cfg["voice_id"] + cfg["voice_model"] + json.dumps(cfg["voice_settings"], sort_keys=True))
    adopt(f"narr_{nkey}.mp3", "narration.mp3")
    adopt(f"narr_{nkey}.json", "alignment.json")
    narr_call = None
    if not (have(f"narr_{nkey}.mp3") and have(f"narr_{nkey}.json")):
        narr_call = narrate.spawn(text, cfg["voice_id"], cfg["voice_model"], cfg["voice_settings"])

    # ---- images (one per shot)
    shot_specs = {}
    for li, line in enumerate(lines):
        for si, shot in enumerate(line["shots"]):
            prompt = shot["prompt"]
            ikey = key(prompt + style)
            name = f"img_{ikey}"
            adopt(f"{name}.jpg", f"scene_*_{ikey}.jpg")
            adopt(f"{name}.url", f"scene_*_{ikey}.url")
            shot_specs[(li, si)] = {
                "name": name, "prompt": f"{prompt} {style}",
                "seed": seed_base + li + 100 * si, **shot,
            }
    todo = [(k, v) for k, v in shot_specs.items() if not have(f"{v['name']}.jpg")]
    if todo:
        for (k, v), (url, data) in zip(
                todo, generate_image.starmap([(v["prompt"], v["seed"]) for _, v in todo])):
            (cache / f"{v['name']}.jpg").write_bytes(data)
            (cache / f"{v['name']}.url").write_text(url)
        CACHE.commit()
    print(f"STEP images: generated {len(todo)}, reused {len(shot_specs) - len(todo)}")

    # ---- motion shots, music and sound effects in parallel
    motion_calls = {}
    for k, v in shot_specs.items():
        if not v.get("motion"):
            continue
        mkey = key(lines[k[0]]["shots"][k[1]]["prompt"] + style + v["motion"])
        mname = f"motion_{mkey}.mp4"
        adopt(mname, f"hero_{mkey}.mp4")
        v["motion_file"] = mname
        if not have(mname):
            url_file = cache / f"{v['name']}.url"
            motion_calls[k] = generate_motion.spawn(url_file.read_text(), v["motion"])

    music_name = f"music_{key(music_prompt)}.mp3"
    adopt(music_name, music_name)
    music_call = None if have(music_name) else generate_audio.spawn(music_prompt, 45)

    sfx_calls = {}
    for sname, (prompt, secs) in SFX_PROMPTS.items():
        fname = f"sfx_{sname}_{key(prompt)}.mp3"
        if not have(fname):
            sfx_calls[sname] = (fname, generate_audio.spawn(prompt, secs))

    # ---- collect narration
    if narr_call is not None:
        audio, align = narr_call.get()
        (cache / f"narr_{nkey}.mp3").write_bytes(audio)
        (cache / f"narr_{nkey}.json").write_text(json.dumps(align))
        CACHE.commit()
    audio = (cache / f"narr_{nkey}.mp3").read_bytes()
    align = json.loads((cache / f"narr_{nkey}.json").read_text())
    (work / "narration.mp3").write_bytes(audio)
    audio_len = media_duration(work / "narration.mp3")

    joined = "".join(align["characters"])
    char_starts = align["character_start_times_seconds"]
    line_starts, pos = [], 0
    for line in lines:
        idx = joined.find(line["text"][:12], pos)
        idx = pos if idx < 0 else idx
        line_starts.append(idx)
        pos = idx + len(line["text"])
    line_starts = [0.0] + [max(char_starts[c] - 0.08, 0) for c in line_starts[1:]]
    total = round(audio_len + 1.2, 2)

    # ---- collect motion, music, sfx
    motion_ok = {}
    for k, call in motion_calls.items():
        try:
            (cache / shot_specs[k]["motion_file"]).write_bytes(call.get())
            motion_ok[k] = True
        except Exception as exc:
            print(f"MOTION FAILED for shot {k}: {str(exc)[:200]}")
    for k, v in shot_specs.items():
        if v.get("motion_file") and have(v["motion_file"]):
            motion_ok[k] = True
    music_ok = True
    try:
        if music_call is not None:
            (cache / music_name).write_bytes(music_call.get())
        (work / "music.mp3").write_bytes((cache / music_name).read_bytes())
    except Exception as exc:
        print(f"MUSIC FAILED: {str(exc)[:200]}")
        music_ok = False
    sfx_files = {}
    for sname, (prompt, _) in SFX_PROMPTS.items():
        fname = f"sfx_{sname}_{key(prompt)}.mp3"
        try:
            if sname in sfx_calls:
                (cache / fname).write_bytes(sfx_calls[sname][1].get())
            (work / f"sfx_{sname}.mp3").write_bytes((cache / fname).read_bytes())
            sfx_files[sname] = work / f"sfx_{sname}.mp3"
        except Exception as exc:
            print(f"SFX FAILED {sname}: {str(exc)[:200]}")
    CACHE.commit()
    print("STEP assets ready")

    # ---- render shots
    shots = plan_shots(lines, line_starts, total, cfg)
    seg_paths, cut_times = [], []
    for n, (li, si, s, e) in enumerate(shots):
        v = shot_specs[(li, si)]
        f0, f1 = int(round(s * FPS)), int(round(e * FPS))
        frames = max(f1 - f0, 1)
        seg = work / f"seg_{n:02d}.mp4"
        if motion_ok.get((li, si)):
            src = work / f"motion_{n}.mp4"
            src.write_bytes((cache / v["motion_file"]).read_bytes())
            clip_len = media_duration(src) or 5.0
            speed = min(max(clip_len / max(e - s, 0.1), 1.0), 2.0)
            vf = (f"setpts=PTS/{speed:.3f},"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
                  f"tpad=stop_mode=clone:stop_duration=15,format=yuv420p")
            run(["ffmpeg", "-y", "-i", str(src), "-vf", vf, "-frames:v", str(frames), "-an",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(seg)])
        else:
            img = work / f"img_{n}.jpg"
            img.write_bytes((cache / f"{v['name']}.jpg").read_bytes())
            run(["ffmpeg", "-y", "-i", str(img), "-vf",
                 camera_filter(v.get("move", "push_in"), frames), "-frames:v", str(frames),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(seg)])
        seg_paths.append(seg)
        if n > 0 and li != shots[n - 1][0]:
            cut_times.append(s)
    (work / "concat.txt").write_text("".join(f"file '{p}'\n" for p in seg_paths))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "concat.txt"),
         "-c", "copy", str(work / "joined.mp4")])

    # ---- captions
    words = words_from_alignment(align)
    chunks = caption_chunks(words)
    ass, plain_captions = build_ass(chunks, cfg["label"], cfg["label_seconds"])
    (work / "captions.ass").write_text(ass)

    # ---- sound-effect cue times
    cues = {"whoosh": [], "impact": [], "riser": []}
    sfx_cfg = spec.get("sfx", {})
    impact_t = [line_starts[i] for i in sfx_cfg.get("impact_on_lines", []) if i < len(lines)]
    riser_t = [line_starts[i] for i in sfx_cfg.get("riser_into_lines", []) if i < len(lines)]
    for t in impact_t:
        cues["impact"].append(max(t - 0.05, 0))
    if "riser" in sfx_files:
        rl = media_duration(sfx_files["riser"])
        for t in riser_t:
            cues["riser"].append(max(t - rl, 0))
    busy = impact_t + riser_t
    for t in cut_times:
        if all(abs(t - b) > 0.6 for b in busy):
            cues["whoosh"].append(max(t - 0.15, 0))
    levels = {"whoosh": 0.12, "impact": 0.55, "riser": 0.35}

    # ---- final mix and grade
    inputs = ["-i", str(work / "joined.mp4"), "-i", str(work / "narration.mp3")]
    graph = [f"[1:a]apad,atrim=0:{total},asplit=2[voice][key]"]
    mix = ["[voice]"]
    nxt = 2
    if music_ok:
        inputs += ["-i", str(work / "music.mp3")]
        graph.append(
            f"[{nxt}:a]aloop=loop=-1:size=2e9,atrim=0:{total},volume=0.22,"
            f"afade=t=in:st=0:d=1.0,afade=t=out:st={total - 1.5:.2f}:d=1.5[bed]")
        graph.append("[bed][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[ducked]")
        mix.append("[ducked]")
        nxt += 1
    else:
        graph.append("[key]anullsink")
    for sname, times in cues.items():
        if sname not in sfx_files or not times:
            continue
        inputs += ["-i", str(sfx_files[sname])]
        labels = [f"[{sname}{i}]" for i in range(len(times))]
        graph.append(f"[{nxt}:a]volume={levels[sname]},asplit={len(times)}" + "".join(labels))
        for i, t in enumerate(times):
            graph.append(f"[{sname}{i}]adelay=delays={int(t * 1000)}:all=1[{sname}d{i}]")
            mix.append(f"[{sname}d{i}]")
        nxt += 1
    graph.append(
        "".join(mix) + f"amix=inputs={len(mix)}:duration=first:normalize=0,"
        f"afade=t=out:st={total - 0.8:.2f}:d=0.8,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    grade = (
        "eq=contrast=1.06:saturation=0.95,vignette=PI/5,noise=alls=3:allf=t,"
        f"subtitles={work / 'captions.ass'}:fontsdir=/usr/share/fonts/truetype/dejavu,"
        f"fade=t=in:st=0:d=0.3,fade=t=out:st={total - 0.6:.2f}:d=0.6"
    )
    final = work / "short.mp4"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", f"[0:v]{grade}[v];" + ";".join(graph),
         "-map", "[v]", "-map", "[a]", "-t", f"{total}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "10M",
         "-bufsize", "20M", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(final)])

    first_images = {}
    for (li, si), v in shot_specs.items():
        first_images[f"line{li:02d}_shot{si}"] = (cache / f"{v['name']}.jpg").read_bytes()
    return {
        "short": final.read_bytes(),
        "images": first_images,
        "report": {
            "duration": total,
            "shots": [(li, si, round(s, 2), round(e, 2)) for li, si, s, e in shots],
            "motion_ok": sorted(f"{k[0]}:{k[1]}" for k in motion_ok),
            "music_ok": music_ok,
            "sfx": {k: [round(t, 2) for t in v] for k, v in cues.items() if k in sfx_files},
            "sfx_missing": sorted(set(SFX_PROMPTS) - set(sfx_files)),
            "captions": plain_captions,
            "images_generated": len(todo),
        },
    }


@app.local_entrypoint()
def main(spec: str):
    spec_data = json.loads(pathlib.Path(spec).read_text())
    result = produce.remote(spec_data)

    out = pathlib.Path("outputs/shorts") / spec_data["id"]
    (out / "scenes").mkdir(parents=True, exist_ok=True)
    (out / "short.mp4").write_bytes(result["short"])
    for name, data in result["images"].items():
        (out / "scenes" / f"{name}.jpg").write_bytes(data)
    (out / "metadata.md").write_text(spec_data.get("metadata", ""))
    (out / "report.json").write_text(json.dumps(result["report"], indent=1))
    r = result["report"]
    print(f"SHORT OK id={spec_data['id']} duration={r['duration']}s shots={len(r['shots'])} "
          f"motion={r['motion_ok']} music={r['music_ok']} sfx_missing={r['sfx_missing']} "
          f"new_images={r['images_generated']} size={len(result['short']) // 1024}KB")
