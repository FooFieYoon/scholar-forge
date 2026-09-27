---
name: video-slide-replica
description: 从教学/说课视频（B站、本地录屏、会议回放等）反向复刻出可编辑的 PPTX。当用户给出一个视频链接或视频文件并说"复刻这个视频里的PPT""照着视频做一份一样的幻灯片""还原视频中的课件"时使用。流程：取视频源 → 切页 → 逐页抽取干净背景（保留水墨/装饰/实拍图）+ 文字样式 → python-pptx 重建 → OCR 回验版式一致。
agent_created: true
---

# 视频课件复刻（video-slide-replica）

把一段"录屏式"教学视频反向还原成一份**可编辑**的 PPTX，视觉效果与视频一致。

核心思路：**背景用位图（保留装饰与图片），文字全部重绘为可编辑文本框**。
不要试图重画装饰，也不要让文字留在图里。

## 环境准备（Windows）

```bash
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"           # 本机必须
PY="C:/Users/foofi/.workbuddy/binaries/python/envs/video/Scripts/python.exe"
# 若不存在：
# "C:/Users/foofi/.workbuddy/binaries/python/versions/3.13.12/python.exe" -m venv "C:/Users/foofi/.workbuddy/binaries/python/envs/video"
# "$PY" -m pip install opencv-python-headless numpy pillow python-pptx rapidocr-onnxruntime
```

Python 执行**必须写 .py 文件再运行**，不要用 `python -c`（沙箱会拒绝读 Lib 下的文件而报 PermissionError）。

## 步骤

### 1. 取视频源
B站不需要 cookie：
```bash
# 先取 cid
curl -s -A "Mozilla/5.0" "https://api.bilibili.com/x/web-interface/view?bvid=<BV号>"
# 再取播放地址（必须带 Referer，否则 403）
curl -s -A "Mozilla/5.0 ... Chrome/120" -e "https://www.bilibili.com/video/<BV号>/" \
  "https://api.bilibili.com/x/player/playurl?bvid=<BV>&cid=<cid>&qn=64&fnval=1&platform=html5&high_quality=1"
# durl[0].url 即 mp4 直链，用同样的 -e 头下载（链接有时效）
```
`qn=64` 得 720P，够 OCR；要更清晰用 `qn=80`（需登录时降级到 64 也能用）。

### 2. 确定画面区域
`scripts/check_border.py`：逐帧统计 `rowmean>12 且 rowmax>60` 的上下边界，取中位数。
录屏常有上下黑边（本例：帧高 720，幻灯片只占 y=38..686）。

**这一步的 y0 必须与后面 OCR 用的一致**，否则全部错位。

### 3. 逐帧 OCR + 切页
`scripts/ocr_scan.py`：每 2s 一帧跑 rapidocr，输出 `ocr_frames.json`（每帧文本+bbox，坐标基于同一裁剪）。
`scripts/pages.py`：把每帧"页面内文字集合"做 Jaccard 相似度，< 0.55 判定为新页（不要用像素差，模板页之间像素差极小）；并过滤掉底部口播字幕（`y+h > 字幕带起点`）与水印（bilibili、UP主名）。

产出 `pages.json`（每页起止时间 + 代表帧）和 `pages_final.txt`（每页文字与坐标，人工核对）。

### 4. 抽取干净背景 + 文字样式
`scripts/extract_pages.py`：
- 每页取**动画播完的末帧**（元素最全）；
- mask = 该页所有文字 bbox（不同帧求并集，含 3px 膨胀）+ 左上水印区 + 底部字幕带；
- `cv2.inpaint(mask, 4, TELEA)` → `pages_bg/pNN.png`（同时留一份 `_raw.png` 原始帧用于对比）；
- 文字颜色：bbox 内最亮/最暗 10% 像素分别与框中位亮度比，偏离大的那个就是字色（自动区分"深字浅底"和"白字绿卡"）；
- 字号：`字高(px) × (页宽in/画宽px) × 72 × 0.9`。

**例外**：图片内部的文字（教材封面、示意图标注、嵌入视频字幕）不要重绘 —— 用 `is_image_text()` 排除，否则背景上会重影。

### 5. 生成 PPTX
`scripts/build_pptx.py`：
- 页面尺寸按视频画面比例设（本例 1106×648 → 13.333×7.8125 in），保证版式不失真；
- 每页铺满背景图，再按 bbox 加文本框；
- 文本框：`margin=0`、`word_wrap=False`、`auto_size=NONE`、`vertical_anchor=TOP`、`line_spacing` 用固定 Pt；
- 同列相邻行合并成一段（排序键用 `(y, x)`！用 `(x, y)` 会把首行甩到段尾）；
  合并阈值：`x 差<14` 且 `y 差 <= 上一行高×1.6+8`；
- 一行一个 run，行间插 `<a:br/>`，**每行可带自己的颜色**（保留红字高亮）；
- 字体用「宋体」（`a:latin/a:ea/a:cs` 三处都要设），别用只有你本机才有的艺术字体。

### 6. 回验
`scripts/render_check.py`：读回 pptx → 用 PIL 按文本框坐标重绘到背景图上 → 对预览图跑 OCR → 与原始 OCR 的 bbox 对比。
各页平均位置偏差 < 15px（≈0.2cm）即合格；某页突然几百 px 说明段落合并或坐标系出错。
`scripts/make_compare.py` 生成"上=原帧 / 下=复刻"的对照长图，交付时一并给用户看。

## 进阶：16:9 + 全可编辑模式
用户常常要"改成标准 16:9""所有元素都能编辑""不要整页截图"。做法是**放弃位图底图，全部用原生对象重绘**（`build_v2.py`）：

1. 页面 13.333×7.5 in；坐标 `x/1106*13.333`、`y/648*7.5`；字号 `字高px × (7.5/648×72×0.94)`。
2. 先探测几何，再重绘：
   - `detect_blocks.py / detect_blocks2.py`：背景色用**全图中位数**（用边框会被装饰污染）；
     连通域找卡片/图片；`fill=面积/外接矩形` 判断形状（0.78≈圆，0.55≈圆环）。
   - `probe.py`：区域中位数/标准差/饱和度 —— std 低(<25)是纯色块，std 高(40-70)是照片；
     再用"绿色掩码的行列投影"取卡片精确边界（比网格肉眼看准得多）。
   - `probe2.py`：3×3 子网格看块内是否还有内容、列/行投影定照片边界。
3. 元素映射：纯色块→ROUNDED_RECTANGLE/OVAL；圆环→OVAL 无填充+粗描边；
   装饰水彩→2~3 个半透明椭圆叠加；竹叶→`MSO_SHAPE.DIAMOND` 拉长后旋转（**没有 TEARDROP**）。
   透明度要写 XML：`srgbClr` 下加 `<a:alpha val="..."/>`（val = (1-不透明度)*100000）。
4. 照片/示意图：按探测出的 bbox 从 `_raw.png` 裁出存 `assets/`，用 `add_picture` 插入 ——
   是独立对象，可移动/替换/删除，不算"整页截图"。
5. `python-pptx` 新版没有 `pptx.oxml.OxmlElement`，用 `from pptx.oxml.xmlchemy import OxmlElement`。

**最常见的坑**：文本框宽度不够会静默换行，整页排版错位。
断行必须沿用原视频的换行点，且 `字号 × 每行字数 × 1.2 < 框宽`；
验证手段：`render_v2.py` 渲染（形状画在 overlay，文字最后画在最上层）再用 OCR 看有没有串行/重叠。
`check_content.py` 按"字符集合命中率"核对每页文字有没有丢。

## 质量检查清单
- [ ] 页数 = 视频里的翻页数（口播里常会念目录，可用它交叉验证）
- [ ] 视频自带字幕条、UP主水印没有混进 PPT
- [ ] 图片内文字没有重影
- [ ] 高亮色文字（红/橙）保留了颜色
- [ ] 竖排文字（如"入射光线"）设了 `vert="eaVert"`
- [ ] 每页 `_raw.png` 与 `preview/pNN.png` 并排看过，无错位、无缺字

## 交付
`present_files` 同时给出：pptx、对照长图。说明页面尺寸是按视频比例定的，若要改 16:9 需重排版。
