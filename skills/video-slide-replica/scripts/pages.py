import json, os, re, glob
import numpy as np, cv2

W = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
IW, IH = 1106, 676
data = json.load(open(os.path.join(W, "ocr_frames.json"), encoding="utf-8"))

SKIP_WORDS = {"bilibili", "bilbili", "b站", "锅包漫", "锅 包 漫"}

def body_texts(fr):
    """texts excluding bottom subtitle band and watermark"""
    out = []
    for d in fr["texts"]:
        t = d["t"].strip()
        if not t or t.lower() in SKIP_WORDS:
            continue
        if d["y"] + d["h"] > 600:          # subtitle strip
            continue
        if d["x"] + d["w"] < 200 and d["y"] < 25:   # bilibili logo
            continue
        out.append(d)
    return out

def sig(fr):
    return set(re.sub(r"\s+", "", d["t"]) for d in body_texts(fr))

def jac(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)

# segment frames into pages using text similarity
pages = []
cur = None
for fr in data:
    s = sig(fr)
    if cur is None:
        cur = dict(start=fr["t"], frames=[fr], last_sig=s)
        continue
    j = jac(cur["last_sig"], s)
    if j < 0.55:
        cur["end"] = cur["frames"][-1]["t"]
        pages.append(cur)
        cur = dict(start=fr["t"], frames=[fr])
    else:
        cur["frames"].append(fr)
    cur["last_sig"] = s
if cur:
    cur["end"] = cur["frames"][-1]["t"]
    pages.append(cur)

# merge ultra-short pages (<4s) into previous unless very different
merged = []
for p in pages:
    dur = p["end"] - p["start"]
    if merged and dur < 3.0:
        merged[-1]["frames"].extend(p["frames"])
        merged[-1]["end"] = p["end"]
        merged[-1]["last_sig"] = p["last_sig"]
    else:
        merged.append(p)

print(f"pages: {len(merged)}")
report = []
for i, p in enumerate(merged, 1):
    best = max(p["frames"], key=lambda f: len(body_texts(f)))
    txts = body_texts(best)
    txts.sort(key=lambda d: (d["y"] // 26, d["x"]))
    report.append(f"\n===== PAGE {i}  {p['start']:.1f}-{p['end']:.1f}s (rep t={best['t']})  items={len(txts)} =====")
    for d in txts:
        report.append(f"  x={d['x']:4d} y={d['y']:4d} w={d['w']:4d} h={d['h']:3d} | {d['t']}")
    p["rep_t"] = best["t"]
txt = "\n".join(report)
open(os.path.join(W, "pages_final.txt"), "w", encoding="utf-8").write(txt)
print(txt)
json.dump([dict(index=i + 1, start=p["start"], end=p["end"], rep_t=p["rep_t"]) for i, p in enumerate(merged)],
          open(os.path.join(W, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
