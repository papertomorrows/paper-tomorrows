"""Bold thumbnail v2: face image on the left (from assets), huge heavy text on the right.
usage: thumb_v2.py face.jpg out.jpg "LINE1|LINE2[|LINE3]" [highlight_line_index] [lang]"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
face, out, text = sys.argv[1], sys.argv[2], sys.argv[3]
hi = int(sys.argv[4]) if len(sys.argv) > 4 else -1
lang = sys.argv[5] if len(sys.argv) > 5 else 'ko'
W, H = 1280, 720
im = Image.open(face).convert('RGB').resize((W, H), Image.LANCZOS)
# darken the right half a little more for contrast
g = Image.new('L', (W, H)); gd = ImageDraw.Draw(g)
for x in range(W): gd.line([(x, 0), (x, H)], fill=int(max(0, min(1, (x - 520) / 300)) * 150))
im = Image.composite(Image.new('RGB', (W, H), (8, 12, 22)), im, g)
d = ImageDraw.Draw(im)
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
lines = text.split('|')
area_w, x0 = 600, 640
YEL, WHT, BLK = (255, 214, 0), (255, 255, 255), (0, 0, 0)
sizes = []
for ln in lines:  # largest size that fits the column, capped
    s = 170 if len(lines) < 3 else 132
    while s > 60:
        f = ImageFont.truetype(font_path, s, index=1)
        if d.textlength(ln, font=f) <= area_w: break
        s -= 4
    sizes.append(s)
total = sum(sizes) + 18 * (len(lines) - 1); y = (H - total) // 2 - 45
for i, (ln, s) in enumerate(zip(lines, sizes)):
    f = ImageFont.truetype(font_path, s, index=1)
    w = d.textlength(ln, font=f); x = x0 + (area_w - w) / 2
    col = YEL if i == hi else WHT
    d.text((x + 6, y + 8), ln, font=f, fill=BLK)
    d.text((x, y), ln, font=f, fill=col, stroke_width=max(6, s // 18), stroke_fill=BLK)
    y += s + 18
im.save(out, quality=93)
