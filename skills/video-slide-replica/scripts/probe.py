import cv2, numpy as np, os, sys

W = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
IW, IH = 1106, 648

def load(i):
    img = cv2.imread(os.path.join(W, "pages_bg", f"p{i:02d}_raw.png"))
    return cv2.resize(img, (IW, IH))

def stat(img, x, y, w, h, label=""):
    roi = img[y:y + h, x:x + w]
    med = np.median(roi.reshape(-1, 3), axis=0)
    mean = roi.reshape(-1, 3).mean(axis=0)
    std = roi.reshape(-1, 3).std(axis=0).mean()
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1].mean()
    print(f"{label:28s} ({x:4d},{y:4d}) {w:3d}x{h:3d}  med=#{int(med[2]):02X}{int(med[1]):02X}{int(med[0]):02X} "
          f"mean=#{int(mean[2]):02X}{int(mean[1]):02X}{int(mean[0]):02X} std={std:5.1f} sat={sat:5.1f}")

# green mask projections, to find card boundaries
def green_rows(i, x0, x1):
    img = load(i)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = ((hsv[:, :, 0] >= 30) & (hsv[:, :, 0] <= 95) & (hsv[:, :, 1] > 35)).astype(np.uint8)
    colsum = m[:, x0:x1].sum(axis=1)
    rowsum = m.sum(axis=1)
    runs = []
    s = None
    for r, v in enumerate(rowsum):
        if v > 250 and s is None:
            s = r
        elif v <= 250 and s is not None:
            if r - s > 15:
                runs.append((s, r))
            s = None
    if s is not None:
        runs.append((s, len(rowsum)))
    print(f"p{i:02d} green row-runs (whole width): {runs}")
    # column profile inside first run
    if runs:
        y0, y1 = runs[0]
        col = m[y0:y1, :].sum(axis=0)
        cruns = []
        s = None
        for c, v in enumerate(col):
            if v > (y1 - y0) * 0.5 and s is None:
                s = c
            elif v <= (y1 - y0) * 0.5 and s is not None:
                if c - s > 30:
                    cruns.append((s, c))
                s = None
        if s is not None:
            cruns.append((s, len(col)))
        print(f"p{i:02d} green col-runs in y{runs[0]}: {cruns}")

print("--- 区域统计 ---")
p7 = load(7)
for lbl, (x, y, w, h) in {
    "p07 卡片L1(估)": (184, 305, 258, 100), "p07 卡片L2(估)": (184, 405, 258, 100),
    "p07 卡片L3(估)": (184, 505, 258, 100), "p07 卡片R1(估)": (585, 305, 258, 100),
    "p07 卡片R外(估)": (560, 300, 300, 310), "p07 左侧装饰": (0, 300, 180, 300),
}.items():
    stat(p7, x, y, w, h, lbl)
green_rows(7, 0, 1106)

print()
p13 = load(13)
for lbl, (x, y, w, h) in {"p13 右区": (697, 188, 333, 272), "p13 左照片": (96, 198, 432, 280),
                          "p13 右上": (697, 188, 333, 120)}.items():
    stat(p13, x, y, w, h, lbl)
green_rows(13, 600, 1106)

print()
for i, boxes in {10: {"右绿卡(估)": (697, 188, 333, 272), "左照片": (100, 180, 451, 304)},
                 11: {"右绿卡(估)": (697, 188, 333, 272), "左照片": (107, 152, 431, 336)},
                 12: {"右绿卡(估)": (697, 180, 333, 290), "左照片": (143, 146, 348, 342)},
                 9:  {"中央圆环": (337, 180, 433, 365), "条目1区域": (69, 165, 350, 55),
                      "条目4区域": (720, 165, 350, 55)},
                 14: {"右照片(估)": (730, 194, 260, 276), "中照片": (428, 194, 255, 276)},
                 15: {"视频截图(估)": (220, 190, 400, 300), "右侧块": (660, 190, 300, 300)},
                 16: {"板书区(估)": (110, 190, 880, 375), "板书外": (0, 100, 100, 100)},
                 }.items():
    img = load(i)
    for lbl, (x, y, w, h) in boxes.items():
        stat(img, x, y, w, h, f"p{i:02d} {lbl}")
    green_rows(i, 0, 1106)
