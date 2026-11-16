"""Voice samples for choosing a narration style. Reads jobs/quick_tts.json:
{"out": "dir", "text": "...", "samples": {"name": {"voice_id": "...", "speed": 1.0}, ...}}"""
import json
import pathlib

import modal

app = modal.App("pyog-quick-tts")
image = modal.Image.debian_slim(python_version="3.11").pip_install("fal-client", "requests")


@app.function(image=image, timeout=600, secrets=[modal.Secret.from_name("paper-tomorrows-keys")])
def say(name: str, text: str, voice_id: str, speed: float, pitch: int):
    import fal_client
    import requests
    try:
        res = fal_client.subscribe("fal-ai/minimax/speech-2.8-hd", arguments={
            "prompt": text, "language_boost": "Korean", "output_format": "url",
            "voice_setting": {"voice_id": voice_id, "speed": speed, "vol": 1, "pitch": pitch}})
        return name, requests.get(res["audio"]["url"], timeout=120).content, ""
    except Exception as e:  # keep the other samples if one voice id is unknown
        return name, b"", str(e)[:300]


@app.local_entrypoint()
def main():
    job = json.loads(pathlib.Path("jobs/quick_tts.json").read_text())
    out = pathlib.Path("outputs") / job["out"]
    out.mkdir(parents=True, exist_ok=True)
    args = [(n, job["text"], s["voice_id"], float(s["speed"]), int(s.get("pitch", 0))) for n, s in job["samples"].items()]
    for name, data, err in say.starmap(args):
        if data:
            (out / f"{name}.mp3").write_bytes(data)
            print("SAVED", name)
        else:
            print("FAILED", name, err)
