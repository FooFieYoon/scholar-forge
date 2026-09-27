import cv2, numpy as np, os, json

W = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
IW, IH = 1106, 648
names = {1: "封面", 2: "目录", 3: "教材分析-教材图片", 4: "教材分析-作用和地位", 5: "学情分析",
         6: "教学目标", 7: "教学方法", 8: "教学资源", 9: "教学过程总览", 10: "环节一", 11: "环节二",
         12: "环节三", 13: "环节四", 14: "环节五", 15: "环节六", 16: "板书设计", 17: "致谢"}

out = []
for i in range(1, 18):
    img = cv2.imread(os.path.join(W, "pages_bg", f"p{i:02d}_raw.png"))
    if img is None:
        continue
    img = cv2.resize(img, (IW, IH))
    # page background = most common colour (median of border pixels)
    bg = np.median(img.reshape(-1, 3), axis=0).astype(np.int16)
    d = np.abs(img.astype(np.int16) - bg).max(axis=2)
    m = (d > 22).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, stats, cent = cv2.connectedComponentsWithStats(m, 8)
    out.append(f"\n=== p{i:02d} {names[i]}  bg=#{int(bg[2]):02X}{int(bg[1]):02X}{int(bg[0]):02X} ===")
    rows = []
    for k in range(1, n):
        x, y, w, h, a = stats[k]
        if a < 2500:
            continue
        roi = img[y:y + h, x:x + w]
        col = np.median(roi.reshape(-1, 3), axis=0)
        fill = a / (w * h)
        rows.append((a, x, y, w, h, col, fill))
    for a, x, y, w, h, col, fill in sorted(rows, key=lambda r: -r[0]):
        out.append(f"   ({x:4d},{y:4d}) {w:4d}x{h:3d} area={a:6d} fill={fill:.2f} "
                   f"col=#{int(col[2]):02X}{int(col[1]):02X}{int(col[0]):02X} "
                   f"[{x/IW*100:.0f}%,{y/IH*100:.0f}%,{(x+w)/IW*100:.0f}%,{(y+h)/IH*100:.0f}%]")
txt = "\n".join(out)
open(os.path.join(W, "blocks.txt"), "w", encoding="utf-8").write(txt)
print(txt)
