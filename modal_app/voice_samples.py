"""Voice samples: reads the same narration in several ElevenLabs voices.

Also confirms the ElevenLabs key works. Uses about 1,500 characters of credit.
Writes MP3 files to outputs/voice_samples/ on the machine that runs `modal run`.
"""

import os
import pathlib

import modal

app = modal.App("paper-tomorrows-voice-samples")

image = modal.Image.debian_slim(python_version="3.11").pip_install("requests")

NARRATION = (
    "In 1956, Frank Lloyd Wright unveiled a skyscraper one mile tall. "
    "Five hundred and twenty-eight floors. Seventy-six elevators. "
    "Room for a hundred thousand people. "
    "Chicago never built it. "
    "But if it had, this is what the city would look like today."
)

# Premade voices that suit documentary narration, in order of preference.
PREFERRED = ["George", "Brian", "Daniel", "Bill", "Adam", "Charlotte"]
MAX_VOICES = 4


@app.function(image=image, timeout=600)
def synthesize() -> list[tuple[str, bytes]]:
    import requests

    key = os.environ["XI_KEY"]
    headers = {"xi-api-key": key}

    voices = requests.get(
        "https://api.elevenlabs.io/v1/voices", headers=headers, timeout=60
    )
    voices.raise_for_status()
    available = {v["name"].split(" ")[0]: v["voice_id"] for v in voices.json()["voices"]}

    chosen = [(n, available[n]) for n in PREFERRED if n in available][:MAX_VOICES]
    if not chosen:
        chosen = list(available.items())[:MAX_VOICES]

    results = []
    for name, voice_id in chosen:
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={**headers, "Content-Type": "application/json"},
            params={"output_format": "mp3_44100_128"},
            json={"text": NARRATION, "model_id": "eleven_multilingual_v2"},
            timeout=120,
        )
        r.raise_for_status()
        results.append((name, r.content))
    return results


@app.local_entrypoint()
def main():
    key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVENLABS")
    if not key:
        raise SystemExit("No ElevenLabs key found in ELEVENLABS_API_KEY or ELEVENLABS")
    secret = modal.Secret.from_dict({"XI_KEY": key})

    out_dir = pathlib.Path("outputs/voice_samples")
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, (name, data) in enumerate(synthesize.with_options(secrets=[secret]).remote(), 1):
        path = out_dir / f"voice_{i}_{name}.mp3"
        path.write_bytes(data)
        print(f"SAVED {path} ({len(data) // 1024} KB)")
    print("VOICE SAMPLES OK")
