import cv2, numpy as np, json, os

W = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
OUTDIR = os.path.join(W, "pages_bg")
os.makedirs(OUTDIR, exist_ok=True)

# slide area inside the letterboxed video frame
Y0, Y1 = 38, 686
IH, IW = Y1 - Y0, 1106          # 648 x 1106
SUBTITLE_Y = 596

ocr = json.load(open(os.path.join(W, "ocr_frames.json"), encoding="utf-8"))
cap = cv2.VideoCapture(os.path.join(W, "src.mp4"))
fps = cap.get(cv2.CAP_PROP_FPS)

# (index, name, frame time LAST in page -> elements fully animated)
PAGES = [
    (1, "封面", 6.5), (2, "目录", 14.0), (3, "教材分析-教材图片", 20.0),
    (4, "教材分析-作用和地位", 35.0), (5, "学情分析", 61.0), (6, "教学目标", 109.0),
    (7, "教学方法", 125.0), (8, "教学资源", 133.5), (9, "教学过程总览", 159.0),
    (10, "环节一-创设情境", 179.0), (11, "环节二-知识回顾", 195.0), (12, "环节三-实验探究", 209.0),
    (13, "环节四-课堂揭秘", 219.0), (14, "环节五-联系生活", 239.0), (15, "环节六-课外拓展", 255.0),
    (16, "板书设计", 263.0), (17, "致谢", 265.6),
]
RANGES = {1: (0, 7), 2: (7, 15), 3: (15, 21), 4: (21, 37), 5: (37, 63), 6: (63, 111),
          7: (111, 127), 8: (127, 135), 9: (135, 161), 10: (161, 181), 11: (181, 197),
          12: (197, 211), 13: (211, 221), 14: (221, 241), 15: (241, 257), 16: (257, 265),
          17: (265, 267)}
SKIP = ("bilibili", "bilbili", "锅包漫")

def is_image_text(pidx, d):
    """text that lives inside an embedded picture -- keep it inside the background
    bitmap and do not redraw it as an editable text box"""
    if pidx == 3 and d["x"] > 580 and d["y"] < 300:       # textbook cover artwork
        return True
    if pidx == 11 and d["t"].replace("人", "入").replace("财", "射").replace("时", "射") in ("入射光线", "反射光线"):
        return True                                        # ray labels inside the diagram
    if pidx == 15 and "跟前" in d["t"]:                    # frame of the embedded video clip
        return True
    return False

def read_slide(t):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
    ok, f = cap.read()
    return f[Y0:Y1, :] if ok else None

result = []
for idx, name, t in PAGES:
    a, b = RANGES[idx]
    fr = read_slide(t)
    if fr is None:      # last page may be past the end
        fr = read_slide(265.0)
    mask = np.zeros((IH, IW), np.uint8)
    mask[0:34, 0:140] = 255
    mask[SUBTITLE_Y:, :] = 255
    texts, seen = [], set()
    for f in ocr:
        if not (a <= f["t"] < b):
            continue
        for d in f["texts"]:
            s = d["t"].strip()
            if not s or s.lower() in SKIP:
                continue
            y = d["y"] - Y0
            if y + d["h"] > SUBTITLE_Y or y < -5:
                continue
            if is_image_text(idx, dict(d, y=y)):
                continue
            key = (d["x"] // 8, y // 8, s)
            if key in seen:
                continue
            seen.add(key)
            mask[max(0, y - 3):min(IH, y + d["h"] + 3),
                 max(0, d["x"] - 3):min(IW, d["x"] + d["w"] + 3)] = 255
            texts.append(dict(t=s, x=d["x"], y=y, w=d["w"], h=d["h"]))

    bgimg = cv2.inpaint(fr, cv2.dilate(mask, np.ones((3, 3), np.uint8)), 4, cv2.INPAINT_TELEA)
    cv2.imwrite(os.path.join(OUTDIR, f"p{idx:02d}.png"), bgimg)
    cv2.imwrite(os.path.join(OUTDIR, f"p{idx:02d}_raw.png"), fr)

    for d in texts:
        r0, r1 = max(0, d["y"]), min(IH, d["y"] + d["h"])
        c0, c1 = max(0, d["x"]), min(IW, d["x"] + d["w"])
        patch = fr[r0:r1, c0:c1].reshape(-1, 3).astype(np.float32)
        lum = patch @ np.array([0.114, 0.587, 0.299], dtype=np.float32)
        o = np.argsort(lum)
        lo = patch[o[:max(1, len(o) // 10)]].mean(axis=0)      # darkest 10%
        hi = patch[o[-max(1, len(o) // 10):]].mean(axis=0)     # brightest 10%
        med = np.median(patch, axis=0)
        d["lo"] = [int(c) for c in lo]
        d["hi"] = [int(c) for c in hi]
        d["med"] = [int(c) for c in med]
        d["lum_med"] = float(np.median(lum))
        # decide ink colour: whichever extreme deviates more from the bbox median
        def dist(c):
            return abs(float(c @ np.array([0.114, 0.587, 0.299])) - d["lum_med"])
        d["ink"] = d["hi"] if dist(hi) > dist(lo) else d["lo"]
    result.append(dict(index=idx, name=name, t=t, texts=texts))
    print(f"p{idx:02d} {name:14s} texts={len(texts):2d} mask={mask.mean()/255:.2f} "
          f"bg_med={np.median(fr.reshape(-1,3),axis=0)}")
cap.release()
json.dump(result, open(os.path.join(W, "pages_text.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("slide", IW, "x", IH, "aspect", round(IW / IH, 4))
