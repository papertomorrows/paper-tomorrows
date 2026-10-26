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
    "C1_full_bleed": (
        "An open book seen from the front, a miniature city of folded and cut paper "
        "towers rising from its pages, the tallest a slender needle-shaped spire in the "
        "centre, lit warm gold from inside the book. The book and city fill most of the "
        "frame. Solid deep navy background reaching every edge and corner. "
    ),
    "C2_bold_silhouette": (
        "An open book with just five bold folded-paper towers rising from its pages, a "
        "tall needle-shaped spire in the middle, simple strong shapes, glowing gold light "
        "spilling up from the pages. Close framing, the book fills the lower half and the "
        "spire reaches near the top. Solid deep navy background reaching every edge. "
    ),
    "C3_night_spire": (
        "An open book glowing gold from within, a single slender folded-paper needle tower "
        "rising from its centre surrounded by a few smaller paper towers, faint stars in a "
        "deep navy night sky that fills the whole frame to every edge, soft cinematic light. "
    ),
}


@app.function(image=image, timeout=600, secrets=[KEYS])
def generate(name: str, prompt: str) -> tuple[str, bytes]:
    import fal_client
    import requests

    res = fal_client.subscribe(
        "fal-ai/flux-2-pro",
        arguments={"prompt": prompt + COMMON, "image_size": "square_hd",
                   "seed": 2027, "output_format": "png"},
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
