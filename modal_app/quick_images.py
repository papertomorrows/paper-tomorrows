"""Quick still images (FLUX.2 [pro]) for thumbnails, outside the render queue.
Reads jobs/quick_images.json: {"out": "dir", "size": [w,h], "images": {"name": "prompt", ...}}
Writes outputs/<out>/<name>.jpg on the machine running `modal run`."""
import json
import pathlib

import modal

app = modal.App("pyog-quick-images")
image = modal.Image.debian_slim(python_version="3.11").pip_install("fal-client", "requests")


@app.function(image=image, timeout=600, secrets=[modal.Secret.from_name("paper-tomorrows-keys")])
def gen(name: str, prompt: str, w: int, h: int, seed: int):
    import fal_client
    import requests
    res = fal_client.subscribe("fal-ai/flux-2-pro", arguments={
        "prompt": prompt, "seed": seed, "output_format": "jpeg", "image_size": {"width": w, "height": h}})
    return name, requests.get(res["images"][0]["url"], timeout=120).content


@app.local_entrypoint()
def main():
    job = json.loads(pathlib.Path("jobs/quick_images.json").read_text())
    out = pathlib.Path("outputs") / job["out"]
    out.mkdir(parents=True, exist_ok=True)
    w, h = job.get("size", [1920, 1080])
    items = list(job["images"].items())
    for name, data in gen.starmap([(n, p, w, h, 700 + i) for i, (n, p) in enumerate(items)]):
        (out / f"{name}.jpg").write_bytes(data)
        print("SAVED", name)
