import os
from PIL import Image, ImageDraw, ImageFont

W = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
OUT = os.path.join(W, "compare")
os.makedirs(OUT, exist_ok=True)
SC = 0.62
pairs = []
for i in range(1, 18):
    a = Image.open(os.path.join(W, "pages_bg", f"p{i:02d}_raw.png")).convert("RGB")
    b = Image.open(os.path.join(W, "preview", f"p{i:02d}.png")).convert("RGB")
    b = b.resize(a.size)
    w, h = a.size
    tile = Image.new("RGB", (w, h * 2 + 14), (255, 255, 255))
    tile.paste(a, (0, 0))
    tile.paste(b, (0, h + 14))
    d = ImageDraw.Draw(tile)
    d.text((8, h + 1), f"p{i:02d}  upper = original video frame / lower = rebuilt slide",
           fill=(180, 0, 0))
    tile = tile.resize((int(w * SC), int((h * 2 + 14) * SC)))
    tile.save(os.path.join(OUT, f"cmp{i:02d}.jpg"), quality=88)
    pairs.append(tile)

# contact sheet: 2 columns
cols, cw, ch = 2, pairs[0].width, pairs[0].height
rows = (len(pairs) + cols - 1) // cols
sheet = Image.new("RGB", (cw * cols + 20, ch * rows + 20), (255, 255, 255))
for k, t in enumerate(pairs):
    sheet.paste(t, ((k % cols) * cw + 10, (k // cols) * ch + 10))
sheet.save(os.path.join(W, "compare_sheet.jpg"), quality=80)
print("compare sheet", sheet.size)
