"""Voice variants: three more gripping takes on the Brian voice.

1. expressive  - same text, lower stability and higher style on multilingual v2
2. v3_tags     - Eleven v3 model with performance tags
3. rhythm      - rewritten text with pauses and short beats, slightly slower
"""

import os
import pathlib

import modal

app = modal.App("paper-tomorrows-voice-variants")

image = modal.Image.debian_slim(python_version="3.11").pip_install("requests")

BRIAN = "nPczCjzI2devNBz1zQrb"

BASE_TEXT = (
    "In 1956, Frank Lloyd Wright unveiled a skyscraper one mile tall. "
    "Five hundred and twenty-eight floors. Seventy-six elevators. "
    "Room for a hundred thousand people. "
    "Chicago never built it. "
    "But if it had, this is what the city would look like today."
)

V3_TEXT = (
    "[curious] In 1956, Frank Lloyd Wright unveiled a skyscraper... one mile tall. "
    "[building tension] Five hundred and twenty-eight floors. Seventy-six elevators. "
    "Room for a hundred thousand people. "
    "[pause] [quietly] Chicago never built it. "
    "[intrigued] But if it had... this is what the city would look like today."
)

RHYTHM_TEXT = (
    "One mile. "
    "That's how tall Frank Lloyd Wright wanted to build... in 1956. "
    "Five hundred and twenty-eight floors. "
    "Seventy-six elevators. "
    "A hundred thousand people... living in the sky. "
    "Chicago said no. "
    "But imagine, for a moment... that it said yes."
)

VARIANTS = [
    (
        "1_expressive",
        BASE_TEXT,
        "eleven_multilingual_v2",
        {"stability": 0.30, "similarity_boost": 0.80, "style": 0.50, "use_speaker_boost": True},
    ),
    (
        "2_v3_tags",
        V3_TEXT,
        "eleven_v3",
        {"stability": 0.5},
    ),
    (
        "3_rhythm",
        RHYTHM_TEXT,
        "eleven_multilingual_v2",
        {"stability": 0.35, "similarity_boost": 0.80, "style": 0.40, "use_speaker_boost": True, "speed": 0.94},
    ),
]


@app.function(image=image, timeout=600)
def synthesize() -> list[tuple[str, bytes]]:
    import requests

    headers = {"xi-api-key": os.environ["XI_KEY"], "Content-Type": "application/json"}
    results = []
    for name, text, model, settings in VARIANTS:
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{BRIAN}",
            headers=headers,
            params={"output_format": "mp3_44100_128"},
            json={"text": text, "model_id": model, "voice_settings": settings},
            timeout=180,
        )
        if not r.ok:
            try:
                d = r.json().get("detail", {})
                msg = f"{d.get('status', '')} {d.get('message', '')}" if isinstance(d, dict) else str(d)
            except Exception:
                msg = r.text[:200]
            print(f"TTS FAILED {r.status_code} for {name}: {msg[:200]}")
            continue
        results.append((name, r.content))
    return results


@app.local_entrypoint()
def main():
    key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVENLABS")
    if not key:
        raise SystemExit("No ElevenLabs key found")
    secret = modal.Secret.from_dict({"XI_KEY": key})

    out_dir = pathlib.Path("outputs/voice_samples/brian_variants")
    out_dir.mkdir(parents=True, exist_ok=True)
    results = synthesize.with_options(secrets=[secret]).remote()
    for name, data in results:
        path = out_dir / f"brian_{name}.mp3"
        path.write_bytes(data)
        print(f"SAVED {path} ({len(data) // 1024} KB)")
    if not results:
        raise SystemExit("No voice samples were produced")
    print("VOICE VARIANTS OK")
