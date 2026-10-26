"""Style samples: renders the same scene in three candidate visual styles.

Also confirms the FAL_KEY secret works. Uses FLUX.2 [pro] on fal.
Writes images to outputs/style_samples/ on the machine that runs `modal run`.
"""

import os
import pathlib

import modal

app = modal.App("paper-tomorrows-style-samples")

image = modal.Image.debian_slim(python_version="3.11").pip_install("fal-client", "requests")

SCENE = (
    "a mile-high skyscraper, a slender tapering needle of steel and glass, "
    "rising far above the 1950s Chicago lakefront, Lake Michigan in the foreground"
)

STYLES = {
    "A_vintage_architectural": (
        f"Architectural watercolor and ink rendering of {SCENE}. Aged paper texture, "
        "faint blueprint linework overlay, muted sepia and slate blue palette, "
        "dramatic low-angle perspective, soft morning haze."
    ),
    "B_retro_pulp_futurism": (
        f"1950s gouache magazine illustration of {SCENE}. Saturated teal and tangerine "
        "palette, halftone print grain, optimistic atomic-age mood, bold graphic shapes, "
        "tiny streamlined cars and boats."
    ),
    "C_cinematic_matte_painting": (
        f"Cinematic matte painting of {SCENE}. Painterly brushwork with near-photographic "
        "lighting at dusk, volumetric fog, anamorphic wide composition, subtle film grain, "
        "muted gold and deep blue tones."
    ),
}


@app.function(image=image, timeout=600)
def generate(name: str, prompt: str) -> tuple[str, bytes, int]:
    import fal_client
    import requests

    result = fal_client.subscribe(
        "fal-ai/flux-2-pro",
        arguments={
            "prompt": prompt,
            "image_size": "portrait_16_9",
            "seed": 1955,
            "output_format": "jpeg",
        },
    )
    url = result["images"][0]["url"]
    data = requests.get(url, timeout=60).content
    return name, data, result.get("seed", 0)


@app.local_entrypoint()
def main():
    secret = modal.Secret.from_dict({"FAL_KEY": os.environ["FAL_KEY"]})
    out_dir = pathlib.Path("outputs/style_samples")
    out_dir.mkdir(parents=True, exist_ok=True)

    calls = [(n, p) for n, p in STYLES.items()]
    for name, data, seed in generate.with_options(secrets=[secret]).starmap(calls):
        path = out_dir / f"{name}.jpg"
        path.write_bytes(data)
        print(f"SAVED {path} ({len(data) // 1024} KB, seed {seed})")
    print("STYLE SAMPLES OK")
