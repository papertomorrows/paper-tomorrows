"""Connection check: confirms GitHub -> Modal works and Modal can render video.

Renders a 5-second test clip with FFmpeg inside Modal and reports the file size
and how long the render took. No paid AI services are called.
"""

import modal

app = modal.App("paper-tomorrows-connection-check")

image = modal.Image.debian_slim(python_version="3.11").apt_install("ffmpeg")


@app.function(image=image, timeout=300)
def render_test_clip() -> dict:
    import os
    import subprocess
    import time

    out_path = "/tmp/test_clip.mp4"
    started = time.time()
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30:duration=5",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=5",
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", out_path,
        ],
        check=True,
        capture_output=True,
    )
    return {
        "file_size_kb": round(os.path.getsize(out_path) / 1024, 1),
        "render_seconds": round(time.time() - started, 1),
    }


@app.local_entrypoint()
def main():
    result = render_test_clip.remote()
    print("CONNECTION CHECK OK:", result)
