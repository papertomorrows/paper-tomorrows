"""Channel profile picture candidates (square, readable as a small circle)."""

import pathlib

import modal

app = modal.App("paper-tomorrows-branding")
image = modal.Image.debian_slim(python_version="3.11").pip_install("fal-client", "requests")
KEYS = modal.Secret.from_name("paper-tomorrows-keys")

COMMON = (
    "Centered emblem composition with generous empty margin so it still reads when "
    "cropped to a small circle. Deep navy blue background, warm gold light. "
    "Minimal, iconic, high contrast. No text, no letters, no watermark."
)

OPTIONS = {
    "A_needle_on_paper": (
        "A single slender needle-shaped skyscraper rising out of a folded sheet of aged "
        "cream drafting paper, glowing gold at its spire, painterly cinematic lighting. "
    ),
    "B_gold_blueprint": (
        "Elegant fine gold line drawing of a slender needle-shaped tower with faint "
        "architectural construction lines and a compass circle around it, like a "
        "luxurious blueprint emblem. "
    ),
    "C_paper_city": (
        "A miniature futuristic skyline of tall towers made of folded and cut paper, "
        "standing on an open book, lit warm gold from below, soft cinematic shadows. "
    ),
}


@app.function(image=image, timeout=600, secrets=[KEYS])
def generate(name: str, prompt: str) -> tuple[str, bytes]:
    import fal_client
    import requests

    res = fal_client.subscribe(
        "fal-ai/flux-2-pro",
        arguments={"prompt": prompt + COMMON, "image_size": "square_hd",
                   "seed": 2026, "output_format": "png"},
    )
    return name, requests.get(res["images"][0]["url"], timeout=120).content


@app.local_entrypoint()
def main():
    out = pathlib.Path("outputs/branding")
    out.mkdir(parents=True, exist_ok=True)
    for name, data in generate.starmap(list(OPTIONS.items())):
        (out / f"profile_{name}.png").write_bytes(data)
        print(f"SAVED profile_{name}.png")
    print("BRANDING OK")
