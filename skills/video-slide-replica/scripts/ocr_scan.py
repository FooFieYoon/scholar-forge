import cv2, numpy as np, os, json, re
from rapidocr_onnxruntime import RapidOCR

SRC = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work/src.mp4"
OUT = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
os.makedirs(os.path.join(OUT, "keyframes"), exist_ok=True)

ocr = RapidOCR()
cap = cv2.VideoCapture(SRC)
fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# auto-detect letterbox black borders on a middle frame
cap.set(cv2.CAP_PROP_POS_FRAMES, total // 2)
ok, probe = cap.read()
g = cv2.cvtColor(probe, cv2.COLOR_BGR2GRAY)
rows = np.where(g.max(axis=1) > 30)[0]
cols = np.where(g.max(axis=0) > 30)[0]
y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
print("frame size", probe.shape, "content box", (x0, y0, x1, y1))
H, W = y1 - y0, x1 - x0
print("aspect", W / H)

step = int(fps * 2)
results = []
idx = 0
while True:
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ok, f = cap.read()
    if not ok:
        break
    t = idx / fps
    img = f[y0:y1, x0:x1]
    res, _ = ocr(img)
    texts = []
    if res:
        for box, txt, score in res:
            xs = [p[0] for p in box]; ys = [p[1] for p in box]
            texts.append(dict(t=txt, s=round(float(score), 2),
                              x=int(min(xs)), y=int(min(ys)),
                              w=int(max(xs) - min(xs)), h=int(max(ys) - min(ys))))
    texts.sort(key=lambda d: (d["y"] // 20, d["x"]))
    joined = " | ".join(d["t"] for d in texts)
    results.append(dict(t=round(t, 1), texts=texts, joined=joined))
    print(f"[{t:6.1f}s] {joined[:150]}")
    idx += step
cap.release()
json.dump(results, open(os.path.join(OUT, "ocr_frames.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done", len(results))
