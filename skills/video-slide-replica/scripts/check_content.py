# -*- coding: utf-8 -*-
import json, os, re
from pptx import Presentation
W = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/work"
PPTX = r"E:/User/Documents/Dev_Projects/WorkBuddy/PPT2/光的反射-说课（可编辑版）.pptx"
src = json.load(open(os.path.join(W, "pages_text.json"), encoding="utf-8"))
prs = Presentation(PPTX)

DROP = {"维能力有限", "时抽象概念的理解存"}

def norm(s):
    return re.sub(r"[\s，。、：；？！“”()（）《》]+", "", s)

report = []
for i, slide in enumerate(prs.slides, 1):
    got = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    got.append(r.text)
    gtext = norm("".join(got))
    want = [t["t"] for t in src[i - 1]["texts"] if t["t"] not in DROP]
    missing = []
    for t in want:
        key = norm(t)
        if not key:
            continue
        # accept if the whole string or 80% of its chars found
        if key in gtext:
            continue
        hit = sum(1 for ch in set(key) if ch in gtext) / len(set(key))
        if hit < 0.85:
            missing.append(t)
    report.append((i, len(want), missing))
    print(f"p{i:02d} 原文{len(want):2d}条  缺失{len(missing)}条  {missing}")
print("\n合计缺失:", sum(len(m) for _, _, m in report))
