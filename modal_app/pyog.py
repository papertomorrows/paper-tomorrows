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
CLIP = 7.0
BLOCK_TAGS = ("cigarette", "smoking", "smoker", "tobacco", "cigar", "vape", "beer", "wine", "alcohol", "whisky",
              "drunk", "gun", "weapon", "pistol", "rifle", "blood", "knife", "drug", "syringe", "pills")   # seconds each stock clip stays on screen


def key(t: str) -> str:
    return hashlib.sha1(t.encode()).hexdigest()[:12]


@app.function(image=image, timeout=600, secrets=[KEYS], max_containers=8)
def tts(text: str, voice_id: str, speed: float, lang: str = "Korean") -> bytes:
    import fal_client
    import requests

    res = fal_client.subscribe("fal-ai/minimax/speech-2.8-hd", arguments={
        "prompt": text, "language_boost": lang, "output_format": "url",
        "voice_setting": {"voice_id": voice_id, "speed": speed, "vol": 1, "pitch": 0}})
    return requests.get(res["audio"]["url"], timeout=120).content


@app.function(image=image, timeout=600, secrets=[KEYS], max_containers=4)
def tts_eleven(text: str, voice_id: str, settings: dict) -> bytes:
    import os
    import requests

    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                      headers={"xi-api-key": os.environ["XI_KEY"], "Content-Type": "application/json"},
                      params={"output_format": "mp3_44100_128"},
                      json={"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": settings},
                      timeout=300)
    if not r.ok:
        raise RuntimeError(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    return r.content


@app.function(image=image, timeout=1500, secrets=[KEYS], max_containers=6)
def animate(img: bytes, motion: str) -> bytes:
    """Hailuo 2.3 Fast image-to-video (768p, 6 s, about $0.19)."""
    import fal_client
    import requests

    import base64
    # fal storage upload started failing ("Invalid storage type"); send the image inline instead
    url = "data:image/jpeg;base64," + base64.b64encode(img).decode()
    res = fal_client.subscribe("fal-ai/minimax/hailuo-2.3-fast/standard/image-to-video",
                               arguments={"image_url": url, "prompt": motion, "duration": "6",
                                          "prompt_optimizer": False})
    return requests.get(res["video"]["url"], timeout=300).content


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
        fields = {}
        for part in head.split("|")[1:]:
            k, _, v = part.partition(":")
            fields[k.strip()] = v.strip()
        name = head.split("|")[0]
        vis = fields.get("visuals", "")
        paras = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
        sents = []
        for pi, p in enumerate(paras):
            p = p.replace("...", "…")
            parts = [s.strip() for s in re.split(r"(?<=[.?!…])\s+", p) if s.strip()]
            for si, s in enumerate(parts):
                # {pause:N} = hold N seconds of silence after the preceding sentence (guided breathing etc.)
                holds = [float(x) for x in re.findall(r"\{pause:([\d.]+)\}", s)]
                lead = re.match(r"^\s*\{pause:([\d.]+)\}", s)
                s = re.sub(r"\s*\{pause:[\d.]+\}\s*", " ", s).strip()
                if lead and sents:
                    sents[-1]["hold"] = sents[-1].get("hold", 0) + float(lead.group(1)); holds = holds[1:]
                if not s:
                    if sents and holds: sents[-1]["hold"] = sents[-1].get("hold", 0) + sum(holds)
                    if sents and si == len(parts) - 1: sents[-1]["para_end"] = True
                    continue
                sents.append({"text": s, "para_end": si == len(parts) - 1, "hold": sum(holds)})
        sections.append({"name": name.strip(), "visuals": [v.strip() for v in vis.split(",") if v.strip()],
                         "title": fields.get("title", ""),
                         "ai": [x.strip() for x in fields.get("ai", "").split(";") if x.strip()],
                         "paint": [x.strip() for x in fields.get("paint", "").split(";") if x.strip()],
                         "stock": fields.get("stock", "yes").lower() != "no",
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


@app.function(image=image, timeout=6000, secrets=[KEYS], volumes={"/cache": CACHE}, cpu=4, memory=8192)
def produce(spec: dict, script_md: str, music: bytes) -> dict:
    import os
    import time as _t
    _T0 = _t.time()
    import builtins
    _print = builtins.print
    def print(*a, **k):  # timestamp every log line so slow steps show up
        _print(f"[{_t.time() - _T0:5.0f}s]", *a, **k, flush=True)
    import subprocess

    import requests

    def run(cmd):
        # a broken input (e.g. a corrupt still with -loop 1) can make ffmpeg spin forever: cap each call
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=900)

    def bad_image(p):
        """True if a cached still is missing, tiny or can't be decoded (then it is regenerated)."""
        if not p.exists():
            return True
        if p.stat().st_size < 20000:
            return True
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-frames:v", "1", "-f", "null", "-"],
                           capture_output=True, text=True, timeout=60)
        return r.returncode != 0 or bool(r.stderr.strip())

    def dur(p):
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                     "csv=p=0", str(p)], capture_output=True, text=True).stdout)

    cache = pathlib.Path("/cache/pyog")
    (cache / "tts").mkdir(parents=True, exist_ok=True)
    (cache / "stock").mkdir(parents=True, exist_ok=True)
    work = pathlib.Path("/tmp/pyog")
    work.mkdir(parents=True, exist_ok=True)
    voice, speed = spec.get("voice_id", "Korean_CalmGentleman"), float(spec.get("speed", 0.92))
    lang = spec.get("lang", "Korean")
    provider = spec.get("voice_provider", "minimax")
    clip_s = float(spec.get("clip_seconds", CLIP))
    wrap_w = 42 if lang == "English" else 22
    cap_size = 62 if lang == "English" else 70
    sections = parse_script(script_md)

    # ---- voice: one clip per sentence (cached)
    allsent = [s for sec in sections for s in sec["sentences"]]
    todo = []
    for s in allsent:
        tag = voice + str(speed) + (json.dumps(spec.get("voice_settings", {}), sort_keys=True) if provider == "eleven" else "")
        s["file"] = cache / "tts" / f"{key(s['text'] + tag)}.mp3"
        if not s["file"].exists():
            todo.append(s)
    if provider == "eleven":
        vs = spec.get("voice_settings", {"stability": 0.35, "similarity_boost": 0.8, "style": 0.4,
                                         "use_speaker_boost": True, "speed": 0.94})
        audios = tts_eleven.starmap([(s["text"], voice, vs) for s in todo])
    else:
        audios = tts.starmap([(s["text"], voice, speed, lang) for s in todo], return_exceptions=True)
    failed = []
    for s, audio in zip(todo, audios):
        if isinstance(audio, Exception):
            failed.append((s["text"], str(audio)[:160]))
            continue
        s["file"].write_bytes(audio)
    CACHE.commit()
    if failed:
        for txt, err in failed:
            print(f"TTS_FAILED: {txt} :: {err}")
        raise RuntimeError(f"{len(failed)} sentence(s) failed TTS (saved the rest to cache); rephrase them: " +
                           " | ".join(t for t, _ in failed))
    print(f"STEP voice: {len(todo)} new sentences, {len(allsent) - len(todo)} cached")

    # ---- timeline with calm pauses
    t, events, inputs = 1.0, [], []
    for si, sec in enumerate(sections):
        sec["start"] = t
        for s in sec["sentences"]:
            d = dur(s["file"])
            events.append((t, t + d, s["text"]))
            inputs.append((s["file"], t))
            t += d + (float(spec.get("para_gap", 0.9)) if s["para_end"] else float(spec.get("sentence_gap", 0.35))) + float(s.get("hold", 0))
        t += float(spec.get("section_gap", 0.8))
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
    own_new, credits = [], {}
    reused_total = [0]
    anims_new = [0]
    min_luma = float(spec.get("min_luma", 55))

    def luma(f):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "2", "-i", str(f), "-frames:v", "1", "-vf",
                              "scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        return sum(raw) / max(len(raw), 1)

    def greenscreen(f):
        # reject chroma-key footage: a large share of strongly green pixels in two sample frames
        for t in ("1", "4"):
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", str(f), "-frames:v", "1", "-vf",
                                  "scale=64:36", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                                 capture_output=True).stdout
            px = [raw[i:i + 3] for i in range(0, len(raw) - 2, 3)]
            green = sum(1 for r, g, b in px if g > 120 and g > r + 50 and g > b + 50)
            if px and green / len(px) > 0.20:
                return True
        return False

    for sec in sections:
        reuse = [("vshort", pathlib.Path("/cache") / c) for c in spec.get("short_clips", {}).get(sec["name"], [])
                 if (pathlib.Path("/cache") / c).exists()]
        sec_clip = clip_s if sec.get("stock", True) else float(spec.get("paint_clip_seconds", 6))
        need = max(1, math.ceil((sec["end"] - sec["start"]) / sec_clip) - len(sec["ai"]) - len(reuse))
        reused_total[0] += len(reuse)
        lists = []
        for kw in (sec["visuals"] or ["calm nature"]) if sec.get("stock", True) else []:
            hits = []
            try:
                # editors' choice clips first (hand-picked, better looking), then the rest
                seen_ids, all_hits = set(), []
                for ec in (["true", "false"] if spec.get("editors_first", True) else ["false"]):
                    r = requests.get("https://pixabay.com/api/videos/", timeout=30, params={
                        "key": pkey, "q": kw, "per_page": 30, "safesearch": "true", "video_type": "film",
                        "editors_choice": ec, "order": "popular"}).json()
                    for h in r.get("hits", []):
                        if h["id"] not in seen_ids:
                            seen_ids.add(h["id"]); all_hits.append(h)
                for h in all_hits:
                    v = h["videos"].get("large") or h["videos"].get("medium")
                    tags = (h.get("tags") or "").lower()
                    if any(w in tags for w in BLOCK_TAGS):  # never show smoking, drinking, weapons etc.
                        continue
                    if spec.get("strict_topic"):  # off-topic subjects unless the keyword asks for them
                        kl = kw.lower()
                        offt = ["cat", "kitten", "dog", "puppy", "elephant", "cow", "cattle", "horse", "pet", "animal",
                                "christmas", "santa", "xmas", "guitar", "turntable", "piano", "violin", "underwater",
                                "swimming", "pool", "shower", "bathroom", "coffee", "food", "kitchen", "lipstick",
                                "makeup", "keyboard", "laptop", "computer", "phone", "car", "traffic", "wedding",
                                "drum", "drummer", "concert", "band", "musician", "goose", "geese", "duck", "chicken",
                                "cross", "church", "jesus", "business", "meeting", "office",
                                "mask", "masks", "carnival", "halloween", "bikini", "swimsuit", "incubator", "newborn",
                                "laboratory", "pharmacy", "scientist", "network", "internet", "technology", "digital",
                                "caterpillar", "snake", "insect", "worm", "spider", "bug", "larva", "reptile",
                                "plug", "socket", "outlet", "electric", "electricity", "power", "origami", "airplane", "plane",
                                "carpentry", "carpenter", "woodwork", "woodworking", "lava", "ruler", "measure", "measuring", "tool", "tools",
                                "dinosaur", "dino", "jurassic", "prehistoric", "trex", "monster", "dragon", "cartoon", "animation",
                                "illustration", "clipart", "vector", "infographic", "skeleton", "toy", "toys", "robot", "lingerie", "underwear", "bra", "animated"]
                        if any(re.search(r"\b" + w + r"s?\b", tags) and w not in kl for w in offt):
                            continue
                        if re.search(r"\b(woman|man|people|person|girl|silhouette|dancer|crowd|family|monk)\b", kl):
                            if not re.search(r"\b(woman|women|man|men|people|person|girl|boy|silhouette|dancer|dancing|dance|human|crowd|family|monk|lady|female|male|adult)\b", tags):
                                continue
                    need_tags = int(spec.get("tag_match", 0))  # relevance: keyword words must appear in the clip's tags
                    if need_tags:
                        words = [w[:4] for w in re.findall(r"[a-z]+", kw.lower()) if len(w) >= 4]
                        hit = sum(1 for w in words if w in tags)
                        if hit < min(need_tags, len(words)):
                            continue
                    if v and v.get("url") and h["duration"] >= clip_s + 2 and v.get("width", 1920) >= 1280:
                        hits.append((h["id"], v["url"], kw))
                        credits[h["id"]] = h.get("pageURL", f"https://pixabay.com/videos/id-{h['id']}/")
            except Exception as exc:
                print(f"PIXABAY FAILED '{kw}': {str(exc)[:200]}")
            lists.append(hits)
        picked, picked_ids = [], []
        depth = 0
        while len(picked) < need and any(depth < len(l) for l in lists):
            for l in lists:  # round-robin over keywords, best-ranked first
                if depth < len(l) and len(picked) < need:
                    cid, url, kw = l[depth]
                    if cid in used:
                        continue
                    f = cache / "stock" / f"px_{cid}.mp4"
                    fb = float(spec.get("fresh_before", 0))  # only clips never used in earlier videos
                    if fb and f.exists() and f.stat().st_mtime < fb:
                        used.add(cid)
                        continue
                    if not f.exists():
                        try:
                            f.write_bytes(requests.get(url, timeout=300).content)
                        except Exception:
                            continue
                    used.add(cid)
                    if luma(f) < min_luma or greenscreen(f):
                        dark += 1
                        continue
                    picked.append(f)
                    picked_ids.append(cid)
            depth += 1
        own = []
        for k, item in enumerate(sec["ai"]):  # the channel's own images (always paid, a few per video)
            prompt, _, motion = (x.strip() for x in item.partition(">>"))
            full = f"{prompt}, {spec.get('ai_style', 'cinematic, dreamy, soft volumetric light, deep blue and warm gold, no text, no watermark')}"
            f = cache / "stock" / f"own_{key(full)}.jpg"
            if f.exists() and bad_image(f):
                print(f"OWN IMAGE CORRUPT, regenerating '{prompt[:60]}'")
                f.unlink()
            if not f.exists():
                img = None
                for attempt, seed in enumerate((500 + k, 900 + k)):
                    try:
                        img = fallback_image.remote(full if attempt == 0 else f"{prompt}, cinematic painting, no text", seed)
                        break
                    except Exception as exc:
                        print(f"OWN IMAGE FAILED (try {attempt + 1}) '{prompt[:80]}': {str(exc)[:1500]}")
                if img is None:
                    continue
                f.write_bytes(img)
                if bad_image(f):
                    print(f"OWN IMAGE UNREADABLE, skipped '{prompt[:60]}'")
                    f.unlink()
                    continue
                own_new.append(prompt)
                CACHE.commit()
            if motion:
                mv = cache / "stock" / f"anim_{key(full + motion)}.mp4"
                if not mv.exists():
                    try:
                        mv.write_bytes(animate.remote(f.read_bytes(), motion))
                        anims_new[0] += 1
                        CACHE.commit()
                    except Exception as exc:
                        print(f"ANIMATE FAILED '{prompt[:80]}': {str(exc)[:600]}")
                if mv.exists():
                    own.append(("video", mv))
                    continue
            own.append(("image", f))
        stock = [("video", f) for f in picked]
        mixed = []
        for j in range(max(len(own), len(stock), len(reuse))):  # alternate reused shots, own images, stock
            for group in (reuse, own, stock):
                if j < len(group):
                    mixed.append(group[j])
        sec["clips"] = mixed
        sec["n_base"] = len(mixed)
        clip_files += sec["clips"]
        sec["stock_ids"] = picked_ids
        for k in range(need - len(picked)):  # not enough stock: calm AI image instead
            pool_p = sec.get("paint") or sec["visuals"] or ["calm cosmos"]
            prompt = (f"{pool_p[k % len(pool_p)]}, "
                      + spec.get("ai_style", "cinematic, dreamy, soft volumetric light, peaceful spiritual "
                                             "atmosphere, no text, no watermark"))
            f = cache / "stock" / f"ai_{key(prompt + ('' if k < len(pool_p) else str(k)))}.jpg"
            if f.exists() and bad_image(f):
                f.unlink()
            if not f.exists():
                if fallbacks >= int(spec.get("max_ai_fallbacks", 99)):
                    pool = sec["clips"] or clip_files  # budget reached: reuse a clip instead of paying
                    if pool:
                        sec["clips"].append(pool[k % len(pool)])
                        clip_files.append(pool[k % len(pool)])
                        continue
                try:
                    f.write_bytes(fallback_image.remote(prompt, 100 + k))
                except Exception as exc:
                    print(f"FALLBACK IMAGE FAILED '{prompt[:80]}': {str(exc)[:1500]}")
                    continue
                fallbacks += 1
            clip_files.append(("image", f))
            sec["clips"].append(("image", f))
    for sec in sections:  # spread extra painted scenes between the moving shots
        base, extra = sec["clips"][:sec.get("n_base", 0)], sec["clips"][sec.get("n_base", 0):]
        if base and extra:
            merged = []
            for j in range(max(len(base), len(extra))):
                if j < len(base):
                    merged.append(base[j])
                if j < len(extra):
                    merged.append(extra[j])
            sec["clips"] = merged
    print(f"STEP visuals: skipped {dark} dark/green-screen clips")
    CACHE.commit()
    print(f"STEP visuals: {len(clip_files)} clips ({fallbacks} AI fallbacks)")

    def kb(n, fr, z):
        # vary the still-image motion: push in, pull out, drift left, drift right
        mode = n % 4
        if mode == 0:
            return f"z='1+{z}*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        if mode == 1:
            return f"z='{1 + z}-{z}*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        if mode == 2:
            return f"z='{1 + z}':x='(iw-iw/zoom)*(1-on/{fr})':y='ih/2-(ih/zoom/2)'"
        return f"z='{1 + z}':x='(iw-iw/zoom)*on/{fr}':y='ih/2-(ih/zoom/2)'"

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
            if kind == "vshort" and spec.get("short_fit", "crop") == "crop":  # fill the wide frame
                run(["ffmpeg", "-y", "-i", str(f), "-an", "-vf",
                     f"setpts=1.1*PTS,tpad=stop_mode=clone:stop_duration=10,fps={FPS},"
                     f"scale={W}:-2,crop={W}:{H}:0:(ih-{H})*{float(spec.get('short_crop_y', 0.45))},"
                     f"setsar=1,eq=contrast=1.04:saturation=1.06,{fade},format=yuv420p",
                     "-frames:v", str(fr), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(out)])
            elif kind == "vshort":  # vertical clip from a short: sharp in the middle, blurred copy behind
                run(["ffmpeg", "-y", "-i", str(f), "-an", "-filter_complex",
                     f"[0:v]setpts=1.1*PTS,tpad=stop_mode=clone:stop_duration=10,fps={FPS},split[a][b];"
                     f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:4,"
                     f"eq=brightness=-0.12:saturation=0.9[bg];[b]scale=-2:{H}[fg];"
                     f"[bg][fg]overlay=(W-w)/2:0,setsar=1,eq=contrast=1.03:saturation=1.05,{fade},format=yuv420p[v]",
                     "-map", "[v]", "-frames:v", str(fr), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                     str(out)])
            elif kind == "video":
                run(["ffmpeg", "-y", "-ss", "1", "-i", str(f), "-an", "-vf",
                     f"setpts=1.15*PTS,tpad=stop_mode=clone:stop_duration=10,{base}", "-frames:v", str(fr),
                     "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(out)])
            else:
                run(["ffmpeg", "-y", "-loop", "1", "-i", str(f), "-vf",
                     f"scale=3840:2160,zoompan={kb(i, fr, float(spec.get('ken_burns', 0.08)))}:d={fr}:s={W}x{H}:fps={FPS},"
                     f"{fade},format=yuv420p",
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
           "Style: Cap,Noto Sans CJK KR," + str(cap_size) + ",&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,"
           "3.5,2,2,140,140,80,1",
           "Style: Chap,Noto Sans CJK KR,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,2,0,1,"
           "3,3,5,160,160,0,1",
           "Style: Kick,Noto Sans CJK KR,30,&H003CC8FF,&H003CC8FF,&H00000000,&H64000000,1,0,0,0,100,100,8,0,1,"
           "1.5,1,5,160,160,150,1",
           "Style: Mark,Noto Sans CJK KR,26,&HB4FFFFFF,&HB4FFFFFF,&HB4000000,&HFF000000,0,0,0,0,100,100,3,0,1,"
           "1,0,9,50,50,40,1", "", "[Events]",
           "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for st, en, tx in events:
        ass.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en + 0.15)},Cap,,0,0,0,,{{\\fad(150,150)}}{wrap(tx, wrap_w)}")
    for si, sec in enumerate(sections):
        if sec["title"]:
            a0 = 0.0 if si == 0 else sections[si - 1]["end"]
            ass.append(f"Dialogue: 1,{ass_time(a0 + 0.2)},{ass_time(a0 + 3.6)},Chap,,0,0,0,,"
                       f"{{\\pos({W // 2},{H // 2})\\fad(500,600)}}{sec['title']}")
            kick = spec.get("kicker_text", "PLAY YOUR OWN GAME" if spec.get("brand_mark", True) else "")
            if kick:
                ass.append(f"Dialogue: 1,{ass_time(a0 + 0.2)},{ass_time(a0 + 3.6)},Kick,,0,0,0,,"
                           f"{{\\pos({W // 2},{H // 2 - 105})\\fad(500,600)}}{kick}")
    if spec.get("label"):
        ass.append(f"Dialogue: 2,{ass_time(0)},{ass_time(float(spec.get('label_seconds', 4)))},Mark,,0,0,0,,"
                   f"{{\\an7\\pos(50,40)\\fad(200,400)}}{spec['label']}")
    if spec.get("brand_mark", True):
        ass.append(f"Dialogue: 2,{ass_time(0)},{ass_time(total)},Mark,,0,0,0,,{spec.get('mark_text', 'Play Your Own Game')}")
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
    credit_lines = [f"{sec['name']}: " + ", ".join(credits.get(c, str(c)) for c in sec.get("stock_ids", []))
                    for sec in sections]
    return {"video": final.read_bytes(), "srt": "\n".join(srt), "credits": "\n".join(credit_lines),
            "report": {"duration": round(total, 1), "sentences": len(events), "clips": len(clip_files),
                       "ai_fallbacks": fallbacks, "own_images_new": len(own_new), "short_clips_reused": reused_total[0], "anims_new": anims_new[0],
                       "chars": sum(len(e[2]) for e in events)}}


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
    (out / "pixabay_credits.txt").write_text(r.get("credits", ""))
    print(f"SHORT OK id={s['id']} {r['report']} size={len(r['video']) // 1024}KB")
