"""Short #001 - Frank Lloyd Wright's mile-high skyscraper (The Illinois).

Pipeline, all inside Modal:
  1. Narration with word timings  (ElevenLabs, Brian, "rhythm" delivery)
  2. One image per script line     (FLUX.2 [pro] on fal, style C)
  3. One hero motion shot          (Kling v3 Pro image-to-video on fal)
  4. Edit: slow camera moves, cuts on each line, captions, label, colour grade
Outputs (written by the local entrypoint): short.mp4, scene images, metadata.md
"""

import os
import pathlib

import modal

app = modal.App("paper-tomorrows-short-001")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "fonts-dejavu-core")
    .pip_install("fal-client", "requests")
)

# ---------------------------------------------------------------- content

VOICE_ID = "nPczCjzI2devNBz1zQrb"  # Brian
VOICE_MODEL = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability": 0.35,
    "similarity_boost": 0.80,
    "style": 0.40,
    "use_speaker_boost": True,
    "speed": 0.94,
}

STYLE = (
    "Cinematic matte painting, painterly brushwork with near-photographic lighting, "
    "volumetric haze, subtle film grain, muted gold and deep blue colour palette, "
    "vertical composition. No text, no lettering, no signage, no watermark."
)

# (narration line, scene prompt, camera move)
SCENES = [
    ("One mile.",
     "Extreme low-angle view looking straight up a slender needle-shaped skyscraper "
     "of steel and glass whose top disappears into the clouds.", "push_in"),
    ("That's how tall Frank Lloyd Wright wanted to build... in 1956.",
     "A 1950s architect's drafting table under a warm desk lamp, a huge vertical "
     "drawing of a needle-shaped skyscraper pinned above it, pencils and rulers.", "pan_up"),
    ("Five hundred and twenty-eight floors.",
     "Looking straight up the side of an impossibly tall tapering tower, hundreds of "
     "floors of glass and gold fins converging to a vanishing point in the sky.", "pan_up"),
    ("Seventy-six elevators... powered by atomic energy.",
     "Inside a vast vertical shaft of a 1950s retro-futuristic tower, glowing elevator "
     "cabs racing upward on rails, atomic-age design, blue light.", "push_in"),
    ("Room for a hundred thousand people... working in the sky.",
     "1950s offices high inside a skyscraper above the clouds at sunrise, silhouettes "
     "of office workers at desks beside panoramic windows, a sea of clouds below.", "pull_out"),
    ("Parking for fifteen thousand cars. And a hundred helicopters.",
     "The base of a colossal tower with vast curved parking terraces full of 1950s "
     "cars, several 1950s helicopters landing on round pads, aerial view.", "push_in"),
    ("It was never built.",
     "An empty lakeside lot in 1950s Chicago at dusk, drifting fog, a single street "
     "lamp, the faint ghostly outline of a giant tower barely visible in the mist.", "pull_out"),
    ("But imagine, for a moment... that it was.",
     "Present-day Chicago skyline at dusk seen from Lake Michigan. In the centre stands "
     "one impossibly tall, slender, needle-shaped tower, five times taller than every "
     "other skyscraper around it. Its middle is wrapped in clouds and its glowing spire "
     "pierces far above the cloud layer near the top of the frame. The ordinary "
     "skyscrapers look tiny at its base. Full height of the needle tower visible.", "hero"),
    ("Even today, it would stand nearly twice as tall as the tallest building ever finished.",
     "A mile-high needle tower beside a modern supertall skyscraper for scale, the "
     "needle tower nearly twice as tall, dramatic dusk sky, city lights below.", "pull_out"),
]

HERO_MOTION_PROMPT = (
    "Slow, smooth upward crane shot rising along the tower, clouds drift gently, "
    "city lights twinkle, water ripples. The architecture stays rigid and unchanged."
)

LABEL = "AI CONCEPT VISUALIZATION"
LABEL_SECONDS = 3.0

W, H, FPS = 1080, 1920, 30

KEYS = modal.Secret.from_name("paper-tomorrows-keys")
CACHE = modal.Volume.from_name("paper-tomorrows-cache", create_if_missing=True)
CACHE_DIR = pathlib.Path("/cache/short_001")


# ---------------------------------------------------------------- generation

@app.function(image=image, timeout=900, secrets=[KEYS])
def generate_image(index: int, prompt: str) -> tuple[int, str, bytes]:
    import fal_client
    import requests

    args = {"prompt": f"{prompt} {STYLE}", "seed": 1956 + index, "output_format": "jpeg"}
    try:
        res = fal_client.subscribe(
            "fal-ai/flux-2-pro", arguments={**args, "image_size": {"width": W, "height": H}}
        )
    except Exception as exc:  # fall back to the preset portrait size
        print(f"custom size failed for scene {index}: {exc}")
        res = fal_client.subscribe(
            "fal-ai/flux-2-pro", arguments={**args, "image_size": "portrait_16_9"}
        )
    url = res["images"][0]["url"]
    return index, url, requests.get(url, timeout=120).content


@app.function(image=image, timeout=1500, secrets=[KEYS])
def generate_hero_clip(image_url: str) -> bytes:
    import fal_client
    import requests

    res = fal_client.subscribe(
        "fal-ai/kling-video/v3/pro/image-to-video",
        arguments={
            "start_image_url": image_url,
            "prompt": HERO_MOTION_PROMPT,
            "duration": "5",
            "generate_audio": False,
            "negative_prompt": "warping, melting, bending buildings, morphing, blur, distortion, text",
        },
    )
    return requests.get(res["video"]["url"], timeout=300).content


@app.function(image=image, timeout=600, secrets=[KEYS])
def narrate(text: str) -> tuple[bytes, dict]:
    import base64

    import requests

    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps",
        headers={"xi-api-key": os.environ["XI_KEY"], "Content-Type": "application/json"},
        params={"output_format": "mp3_44100_128"},
        json={"text": text, "model_id": VOICE_MODEL, "voice_settings": VOICE_SETTINGS},
        timeout=300,
    )
    if not r.ok:
        raise RuntimeError(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    data = r.json()
    return base64.b64decode(data["audio_base64"]), data["alignment"]



MUSIC_PROMPT = (
    "Slow cinematic ambient underscore, warm analog synth pads, soft low strings, "
    "gentle sense of wonder and mystery, documentary score, no drums, no vocals, "
    "steady and calm, 70 bpm"
)


@app.function(image=image, timeout=900, secrets=[KEYS])
def generate_music(seconds: int) -> bytes:
    import fal_client
    import requests

    last_exc = None
    for args in (
        {"prompt": MUSIC_PROMPT, "seconds_total": seconds},
        {"prompt": MUSIC_PROMPT, "duration": seconds},
        {"prompt": MUSIC_PROMPT},
    ):
        try:
            res = fal_client.subscribe("fal-ai/stable-audio-25/text-to-audio", arguments=args)
            audio = res.get("audio") or res.get("audio_file") or res.get("output")
            url = audio["url"] if isinstance(audio, dict) else audio
            return requests.get(url, timeout=120).content
        except Exception as exc:
            print(f"music attempt failed ({list(args)}): {str(exc)[:200]}")
            last_exc = exc
    raise RuntimeError(f"music generation failed: {last_exc}")

# ---------------------------------------------------------------- editing helpers

def ass_time(t: float) -> str:
    t = max(t, 0)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def words_from_alignment(text: str, align: dict) -> list[tuple[str, float, float]]:
    chars = align["characters"]
    starts = align["character_start_times_seconds"]
    ends = align["character_end_times_seconds"]
    joined = "".join(chars)
    if joined != text:  # alignment covers the text we sent; fall back to its own chars
        text = joined
    words, cur, w_start, w_end = [], "", None, None
    for ch, s, e in zip(chars, starts, ends):
        if ch.isspace():
            if cur:
                words.append((cur, w_start, w_end))
            cur, w_start = "", None
            continue
        if w_start is None:
            w_start = s
        cur += ch
        w_end = e
    if cur:
        words.append((cur, w_start, w_end))
    return words


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
    out = []
    for i, c in enumerate(chunks):
        start = c[0][1]
        end = chunks[i + 1][0][1] if i + 1 < len(chunks) else c[-1][2] + 0.4
        text = " ".join(x[0] for x in c).replace("...", "").replace(",", "")
        text = text.strip(" .").upper()
        text = text.replace("{", "").replace("}", "")
        out.append((start, end, text))
    return out


def build_ass(chunks, total: float) -> str:
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
    lines = [f"Dialogue: 1,{ass_time(0)},{ass_time(LABEL_SECONDS)},Label,,0,0,0,,{{\\fad(200,500)}}{LABEL}"]
    for s, e, t in chunks:
        lines.append(
            f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Caption,,0,0,0,,{{\\fad(60,60)}}{t}"
        )
    return header + "\n".join(lines) + "\n"


def camera_filter(move: str, frames: int) -> str:
    big_w, big_h = W * 2, H * 2
    d = max(frames, 1)
    if move == "push_in":
        z, x, y = f"1+0.12*on/{d}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif move == "pull_out":
        z, x, y = f"1.12-0.12*on/{d}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    else:  # pan_up
        z, x, y = "1.12", "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*(1-on/{d})"
    return (
        f"scale={big_w}:{big_h}:force_original_aspect_ratio=increase,crop={big_w}:{big_h},"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={d}:s={W}x{H}:fps={FPS},format=yuv420p"
    )


def run(cmd: list[str]) -> None:
    import subprocess

    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + p.stderr[-2000:])


# ---------------------------------------------------------------- production

@app.function(image=image, timeout=3000, cpu=4.0, memory=4096, secrets=[KEYS],
              volumes={"/cache": CACHE})
def produce() -> dict:
    import hashlib
    import json
    import subprocess

    key = lambda text: hashlib.sha1(text.encode()).hexdigest()[:10]

    work = pathlib.Path("/tmp/short")
    work.mkdir(parents=True, exist_ok=True)

    lines = [s[0] for s in SCENES]
    narration_text = " ".join(lines)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = lambda name: (CACHE_DIR / name).exists()

    # 1+2: narration and images in parallel (reuse anything already generated)
    narration_call = None
    if not (cached("narration.mp3") and cached("alignment.json")):
        narration_call = narrate.spawn(narration_text)

    images, urls = {}, {}
    todo = []
    for i, s in enumerate(SCENES):
        name = f"scene_{i:02d}_{key(s[1] + STYLE)}"
        legacy = CACHE_DIR / f"scene_{i:02d}.jpg"  # files from before prompt-keyed caching
        if not cached(f"{name}.jpg") and legacy.exists() and s[2] != "hero":
            (CACHE_DIR / f"{name}.jpg").write_bytes(legacy.read_bytes())
            old_url = CACHE_DIR / f"scene_{i:02d}.url"
            if old_url.exists():
                (CACHE_DIR / f"{name}.url").write_text(old_url.read_text())
        if cached(f"{name}.jpg"):
            images[i] = (CACHE_DIR / f"{name}.jpg").read_bytes()
            url_file = CACHE_DIR / f"{name}.url"
            urls[i] = url_file.read_text() if url_file.exists() else ""
        else:
            todo.append((i, s[1]))
    for idx, url, data in (generate_image.starmap(todo) if todo else []):
        images[idx], urls[idx] = data, url
        name = f"scene_{idx:02d}_{key(SCENES[idx][1] + STYLE)}"
        (CACHE_DIR / f"{name}.jpg").write_bytes(data)
        (CACHE_DIR / f"{name}.url").write_text(url)
    CACHE.commit()
    for idx, data in images.items():
        (work / f"scene_{idx:02d}.jpg").write_bytes(data)
    print(f"GENERATED {len(todo)} new images, reused {len(SCENES) - len(todo)}")

    # 3: hero motion shot from the hero scene image
    hero_idx = next(i for i, s in enumerate(SCENES) if s[2] == "hero")
    music_name = f"music_{key(MUSIC_PROMPT)}.mp3"
    music_call = None if cached(music_name) else generate_music.spawn(45)
    print("STEP images done")
    hero_name = f"hero_{key(SCENES[hero_idx][1] + STYLE + HERO_MOTION_PROMPT)}.mp4"
    hero_call = None
    if not cached(hero_name):
        hero_call = generate_hero_clip.spawn(urls[hero_idx])

    if narration_call is not None:
        audio, align = narration_call.get()
        (CACHE_DIR / "narration.mp3").write_bytes(audio)
        (CACHE_DIR / "alignment.json").write_text(json.dumps(align))
        CACHE.commit()
    else:
        audio = (CACHE_DIR / "narration.mp3").read_bytes()
        align = json.loads((CACHE_DIR / "alignment.json").read_text())
    (work / "narration.mp3").write_bytes(audio)
    audio_len = float(
        subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
             str(work / "narration.mp3")],
            capture_output=True, text=True,
        ).stdout.strip()
    )

    # scene timing: cut slightly before each line begins
    joined = "".join(align["characters"])
    starts_chars, pos = [], 0
    for line in lines:
        idx = joined.find(line[:12], pos)
        if idx < 0:
            idx = pos
        starts_chars.append(idx)
        pos = idx + len(line)
    char_starts = align["character_start_times_seconds"]
    scene_starts = [0.0] + [max(char_starts[c] - 0.08, 0) for c in starts_chars[1:]]
    total = audio_len + 1.2
    scene_ends = scene_starts[1:] + [total]

    hero_path = work / "hero.mp4"
    hero_ok = True
    try:
        if hero_call is not None:
            (CACHE_DIR / hero_name).write_bytes(hero_call.get())
            CACHE.commit()
        hero_path.write_bytes((CACHE_DIR / hero_name).read_bytes())
    except Exception as exc:
        print(f"HERO CLIP FAILED, using camera move instead: {exc}")
        hero_ok = False

    # 4a: render each scene
    seg_paths = []
    for i, (line, _, move) in enumerate(SCENES):
        dur = scene_ends[i] - scene_starts[i]
        frames = max(int(round(dur * FPS)), 1)
        seg = work / f"seg_{i:02d}.mp4"
        if move == "hero" and hero_ok:
            vf = (
                f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
                f"tpad=stop_mode=clone:stop_duration=10,format=yuv420p"
            )
            run(["ffmpeg", "-y", "-i", str(hero_path), "-vf", vf, "-frames:v", str(frames),
                 "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(seg)])
        else:
            cam = "push_in" if move == "hero" else move
            run(["ffmpeg", "-y", "-i", str(work / f"scene_{i:02d}.jpg"),
                 "-vf", camera_filter(cam, frames), "-frames:v", str(frames),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(seg)])
        seg_paths.append(seg)

    concat_list = work / "concat.txt"
    concat_list.write_text("".join(f"file '{p}'\n" for p in seg_paths))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
         "-c", "copy", str(work / "joined.mp4")])

    # 4b: captions + label + grade + audio
    words = words_from_alignment(narration_text, align)
    chunks = caption_chunks(words)
    (work / "captions.ass").write_text(build_ass(chunks, total))

    grade = (
        "eq=contrast=1.06:saturation=0.95,"
        "vignette=PI/5,"
        "noise=alls=3:allf=t,"
        f"subtitles={work / 'captions.ass'}:fontsdir=/usr/share/fonts/truetype/dejavu,"
        f"fade=t=in:st=0:d=0.3,fade=t=out:st={total - 0.6:.2f}:d=0.6"
    )
    music_ok = True
    try:
        if music_call is not None:
            (CACHE_DIR / music_name).write_bytes(music_call.get())
            CACHE.commit()
        (work / "music.mp3").write_bytes((CACHE_DIR / music_name).read_bytes())
    except Exception as exc:
        print(f"MUSIC FAILED, continuing without music: {str(exc)[:300]}")
        music_ok = False
    print("STEP music done")

    final = work / "short.mp4"
    if music_ok:
        # music sits low and ducks further whenever the narrator speaks
        audio_graph = (
            f"[1:a]apad,atrim=0:{total:.2f},asplit=2[voice][key];"
            f"[2:a]aloop=loop=-1:size=2e9,atrim=0:{total:.2f},volume=0.22,"
            f"afade=t=in:st=0:d=1.0,afade=t=out:st={total - 1.5:.2f}:d=1.5[bed];"
            f"[bed][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[ducked];"
            f"[voice][ducked]amix=inputs=2:duration=first:normalize=0,"
            f"afade=t=out:st={total - 0.8:.2f}:d=0.8,alimiter=limit=0.95[a]"
        )
        inputs = ["-i", str(work / "joined.mp4"), "-i", str(work / "narration.mp3"),
                  "-i", str(work / "music.mp3")]
    else:
        audio_graph = f"[1:a]apad,atrim=0:{total:.2f},afade=t=out:st={total - 0.8:.2f}:d=0.8[a]"
        inputs = ["-i", str(work / "joined.mp4"), "-i", str(work / "narration.mp3")]
    run(["ffmpeg", "-y", *inputs,
         "-filter_complex", f"[0:v]{grade}[v];{audio_graph}",
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "10M",
         "-bufsize", "20M", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)])

    return {
        "short": final.read_bytes(),
        "images": {i: images[i] for i in images},
        "narration": audio,
        "captions": [(round(s, 2), round(e, 2), t) for s, e, t in chunks],
        "scene_starts": [round(s, 2) for s in scene_starts],
        "duration": round(total, 2),
        "hero_ok": hero_ok,
        "music_ok": music_ok,
    }


METADATA = """# Short #001 - The Mile-High Skyscraper

## Title options
1. Chicago Almost Built a Mile-High Skyscraper
2. This 1956 Skyscraper Would Still Be the Tallest on Earth
3. Frank Lloyd Wright Wanted to Build One Mile Into the Sky

## Description
In 1956, Frank Lloyd Wright unveiled "The Illinois": a skyscraper one mile tall,
with 528 floors, 76 atomic-powered elevators and workspace for about 100,000 people.
It was never built. This is a concept visualization of what might have been.

Visuals are AI-generated concept art, not photographs or plans of a real building.

Sources:
- ASCE Civil Engineering magazine: "Visualization unveiled for unbuilt Frank Lloyd Wright tower" (2023)
- Wikipedia: The Illinois

#neverbuilt #architecture #franklloydwright #chicago #history

## Upload checklist
- Altered or synthetic content disclosure: YES (realistic AI-generated scenes)
- Made for kids: No
"""


@app.local_entrypoint()
def main():
    import json

    result = produce.remote()

    out = pathlib.Path("outputs/shorts/001_mile_high")
    (out / "scenes").mkdir(parents=True, exist_ok=True)
    (out / "short.mp4").write_bytes(result["short"])
    (out / "narration.mp3").write_bytes(result["narration"])
    for i, data in result["images"].items():
        (out / "scenes" / f"scene_{int(i):02d}.jpg").write_bytes(data)
    (out / "metadata.md").write_text(METADATA)
    (out / "timing.json").write_text(json.dumps(
        {k: result[k] for k in ("captions", "scene_starts", "duration", "hero_ok", "music_ok")}, indent=1
    ))
    print(f"SHORT OK duration={result['duration']}s hero_ok={result['hero_ok']} "
          f"music_ok={result['music_ok']} size={len(result['short']) // 1024}KB")
