"""Bold thumbnail v3 (text-dominant, Korean self-dev style): full-bleed photo, dark gradient,
small quote line on top, white main line(s), huge yellow punch line.
usage: thumb_v3.py photo.jpg out.jpg "small quote" "WHITE LINE[|WHITE LINE2]" "YELLOW LINE" """
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

photo, out, quote, white, yellow = sys.argv[1:6]
W, H = 1280, 720
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
FONT_B = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
YEL, WHT, BLK = (255, 212, 0), (255, 255, 255), (0, 0, 0)

im = Image.open(photo).convert('RGB')
r = max(W / im.width, H / im.height)
im = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
im = im.crop(((im.width - W) // 2, 0, (im.width - W) // 2 + W, H))
im = ImageEnhance.Contrast(im).enhance(1.12)
# darken right and bottom so text pops while the face stays bright
m = Image.new('L', (W, H)); md = ImageDraw.Draw(m)
for x in range(W):
    for_y = max(0.0, min(1.0, (x - 430) / 380))
    md.line([(x, 0), (x, H)], fill=int(for_y * 185))
m2 = Image.new('L', (W, H)); md2 = ImageDraw.Draw(m2)
for y in range(H):
    md2.line([(0, y), (W, y)], fill=int(max(0.0, min(1.0, (y - 380) / 340)) * 150))
from PIL import ImageChops
m = ImageChops.lighter(m, m2)
im = Image.composite(Image.new('RGB', (W, H), (5, 6, 10)), im, m)
d = ImageDraw.Draw(im)

x_left, area_w = 515, 745


def fit(text, start, minimum, path=FONT, idx=1):
    s = start
    while s > minimum:
        f = ImageFont.truetype(path, s, index=idx)
        if d.textlength(text, font=f) <= area_w:
            return f, s
        s -= 4
    return ImageFont.truetype(path, s, index=idx), s


blocks = []
if quote:
    blocks.append((quote, *fit(quote, 54, 30, FONT_B, 1), WHT, 'q'))
for ln in white.split('|'):
    if ln:
        blocks.append((ln, *fit(ln, 108, 60), WHT, "w"))
ys = [t for t in yellow.split('|') if t]
ysz = min(fit(t, 178, 80)[1] for t in ys)  # one shared size for all punch lines
for t in ys:
    blocks.append((t, ImageFont.truetype(FONT, ysz, index=1), ysz, YEL, 'y'))
gaps = {'q': 26, 'w': 14, 'y': 8}
total = sum(s for _, _, s, _, _ in blocks) + sum(gaps[k] for *_, k in blocks[:-1])
y = (H - total) // 2 + 30
for text, f, s, col, kind in blocks:
    w = d.textlength(text, font=f)
    x = x_left + (area_w - w) / 2
    sw = max(4, s // 16) if kind != 'q' else 3
    # soft shadow
    sh = Image.new('L', (W, H)); ImageDraw.Draw(sh).text((x + 8, y + 10), text, font=f, fill=200, stroke_width=sw)
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    im.paste(Image.new('RGB', (W, H), BLK), (0, 0), sh)
    d = ImageDraw.Draw(im)
    d.text((x, y), text, font=f, fill=col, stroke_width=sw, stroke_fill=BLK)
    y += s + gaps[kind]
im.save(out, quality=93)
