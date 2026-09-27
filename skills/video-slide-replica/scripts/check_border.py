import cv2, numpy as np, os
W = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
cap = cv2.VideoCapture(os.path.join(W, "src.mp4"))
fps = cap.get(cv2.CAP_PROP_FPS)
tops, bots = [], []
for t in range(0, 266, 6):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
    ok, f = cap.read()
    if not ok:
        continue
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
    rowmean = g.mean(axis=1)
    rowmax = g.max(axis=1)
    top = 0
    for i in range(len(rowmean)):
        if rowmean[i] > 12 and rowmax[i] > 60:
            top = i
            break
    bot = len(rowmean)
    for i in range(len(rowmean) - 1, -1, -1):
        if rowmean[i] > 12 and rowmax[i] > 60:
            bot = i + 1
            break
    tops.append(top)
    bots.append(bot)
print("top borders:", sorted(set(tops)))
print("bottom borders:", sorted(set(bots)))
print("median top", int(np.median(tops)), "median bottom", int(np.median(bots)))
