import cv2, numpy as np, os

W = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
IW, IH = 1106, 648
def load(i):
    img = cv2.imread(os.path.join(W, "pages_bg", f"p{i:02d}_raw.png"))
    return cv2.resize(img, (IW, IH))

def grid(img, x0, y0, w, h, rows=3, cols=3, label=""):
    print(f"--- {label} ({x0},{y0}) {w}x{h} ---")
    for r in range(rows):
        line = []
        for c in range(cols):
            x = x0 + c * w // cols; y = y0 + r * h // rows
            roi = img[y:y + h // rows, x:x + w // cols]
            med = np.median(roi.reshape(-1, 3), axis=0)
            std = roi.reshape(-1, 3).std(axis=0).mean()
            line.append(f"#{int(med[2]):02X}{int(med[1]):02X}{int(med[0]):02X}/{std:.0f}")
        print("   " + "  ".join(line))

p13 = load(13)
grid(p13, 582, 190, 415, 290, 3, 3, "p13 右区(浅青?)")

p9 = load(9)
for nm, (x, y, w, h) in {"条目1": (100, 166, 260, 48), "条目2": (55, 308, 260, 48),
                         "条目3": (95, 458, 260, 48), "条目4": (740, 168, 260, 48),
                         "条目5": (795, 308, 260, 48), "条目6": (750, 458, 260, 48)}.items():
    roi = p9[y:y + h, x:x + w]
    med = np.median(roi.reshape(-1, 3), axis=0); std = roi.reshape(-1, 3).std(axis=0).mean()
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    print(f"p09 {nm} ({x},{y}) med=#{int(med[2]):02X}{int(med[1]):02X}{int(med[0]):02X} std={std:.0f} sat={hsv[:,:,1].mean():.0f}")

# p14 third photo boundaries: column profile of "非背景" pixels
for i in (14, 15):
    img = load(i)
    med_bg = np.median(img.reshape(-1, 3), axis=0).astype(np.int16)
    d = np.abs(img.astype(np.int16) - med_bg).max(axis=2)
    m = (d > 40).astype(np.uint8)
    col = m[150:500, :].sum(axis=0)
    runs = []
    s = None
    for c, v in enumerate(col):
        if v > 60 and s is None: s = c
        elif v <= 60 and s is not None:
            if c - s > 40: runs.append((s, c))
            s = None
    if s is not None: runs.append((s, len(col)))
    print(f"p{i:02d} 内容列区间 y150-500: {runs}")
    row = m[:, 0:1106].sum(axis=1)
    rr = []; s = None
    for r, v in enumerate(row):
        if v > 200 and s is None: s = r
        elif v <= 200 and s is not None:
            if r - s > 40: rr.append((s, r))
            s = None
    if s is not None: rr.append((s, len(row)))
    print(f"p{i:02d} 内容行区间: {rr}")
