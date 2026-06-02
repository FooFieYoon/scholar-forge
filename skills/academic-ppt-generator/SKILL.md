---
name: academic-ppt-generator
description: >
  学术汇报PPT全流程生成器。从论文/发言稿出发，分析参考PPT设计DNA，
  生成学术发表级图表（matplotlib 300DPI），使用PptxGenJS程序化生成专业PPTX，
  支持Visual QA验证与迭代优化。触发场景：制作学术汇报PPT、学术分享PPT、
  论文答辩PPT、论坛发言PPT、科研汇报PPT。触发词：学术PPT、汇报PPT、
  论坛发言PPT、答辩PPT、科研汇报、制作PPT、生成PPT。
agent_created: true
---

# Academic PPT Generator — 学术汇报PPT全流程生成器

## 概述

从学术论文/发言稿出发，生成专业、美观、符合学术规范的汇报PPT。核心流程：
1. 解析源文档（论文+发言稿）
2. 分析参考PPT设计DNA（配色/字体/布局模式）
3. 使用matplotlib生成学术发表级图表（300DPI）
4. 使用PptxGenJS程序化生成PPTX文件
5. Visual QA验证（python-pptx检测遮挡/溢出）
6. 迭代优化至满意

## 触发条件

当用户需要制作学术汇报PPT时激活，包括但不限于：
- 学术论坛/会议发言PPT
- 论文答辩PPT
- 课题汇报PPT
- 科研成果分享PPT

## 核心工作流程

### Phase 1: 源文档解析

1. **读取论文原文**（.docx）：使用python-docx提取核心论点、数据、框架
2. **读取发言稿**（.md/.docx）：提取演讲逻辑、章节结构、关键数据点
3. **提取关键数据**：所有百分比、人数、金额、时间节点等量化信息
4. **确定PPT页数**：按发言时长估算（1分钟≈2-3页幻灯片）

### Phase 2: 参考PPT设计DNA分析（如用户提供参考PPT）

使用python-pptx深度分析参考PPT：

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu

prs = Presentation('reference.pptx')
for i, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        left = shape.left / 914400    # EMU to inches
        top = shape.top / 914400
        width = shape.width / 914400
        height = shape.height / 914400
        # Extract: fill color, font, font size, text content, position
```

**必须提取的设计DNA**：
- 主色/辅色/强调色/背景色的十六进制值
- 标题字体、正文字体、字号体系
- 封面页布局（背景色、标题位置、装饰元素）
- 章节过渡页布局（编号风格、标题大小、英文引言装饰）
- 内容页布局（导航栏、图文分区、数据卡片样式）
- 尾页布局

### Phase 3: 学术图表生成

使用matplotlib生成学术发表级图表，脚本模板见 `scripts/generate_charts.py`。

**学术图表规范**：
- **DPI**: 300（学术出版标准）
- **配色**: Nature/Science风格色盲友好调色板
- **边框**: 去除顶部和右侧spine，保留左侧和底部
- **字号**: 标题14pt、轴标签11pt、刻度9.5pt、图例9pt、脚注8pt
- **数据来源**: 每张图表底部必须添加数据来源脚注
- **图例**: 使用legend而非直接标注（除非空间不允许）
- **背景**: 纯白#FFFFFF，无网格装饰
- **导出格式**: PNG，透明背景（图表区域白色）

**常用学术图表类型**：
1. **水平柱状图** — 数据对比+目标参考线+差距区间
2. **概念框架图** — 中心辐射式/层次架构式，使用matplotlib patches
3. **对比表图** — 横向对比+交替行背景+箭头指示
4. **时间线图** — 水平时间轴+节点+事件详情
5. **结构示意图** — 矩形+箭头+标签的组合

**踩坑经验**：
- matplotlib中文字体必须显式设置`SimHei`或`Microsoft YaHei`
- 特殊Unicode字符（如▸▶）在某些字体中不存在，用普通点号·替代
- 缓存目录可能不可写，设置`MPLCONFIGDIR`环境变量
- 中文引号""在JS/Python字符串中会冲突，使用`\u201c`/`\u201d`转义

### Phase 4: PPTX生成（PptxGenJS）

使用PptxGenJS程序化生成PPTX，确保精确定位无遮挡。

**依赖安装**：
```bash
cd <workspace> && npm install pptxgenjs
```

**运行方式**：
```bash
NODE_PATH=<workspace>/node_modules node gen_ppt.js
```

**排版核心原则**：

1. **页面尺寸**: 13.33×7.5英寸（宽屏16:9）
2. **最小边距**: 0.5英寸，推荐0.55英寸
3. **字号体系**: 页标题28-32pt、节标题20-24pt、正文14-16pt、注释10-11pt
4. **内容区边界**: 侧边栏(w=1.0)时内容区x≥1.2；全幅布局时x≥0.55
5. **元素间距**: 最小0.15英寸，推荐0.2-0.3英寸
6. **对齐方式**: 标题居中，正文左对齐
7. **多样布局**: 避免每页相同布局，根据内容类型选择合适的排版

**布局模板**（参见 `references/layout_templates.md`）：
- 封面页：深色背景+大标题+英文副标题+装饰线
- 目录页：左侧列表+右侧概念卡片
- 章节过渡页：大编号+大标题+英文引言+装饰线+logo
- 数据页：图表+数据卡片+要点列表
- 对比页：图表+对比卡片+机制卡片
- 框架页：图表+要点面板+金句条
- 案例页：照片网格+信息卡+机制/维度卡片
- 时间线页：全幅时间线+里程碑卡片
- 贡献页：列表+成果面板
- 展望页：2×2网格卡片
- 尾页：深色背景+致谢+logo

**中文引号处理**：
在JS字符串中，中文引号""会导致语法错误。必须使用Unicode转义：
- `"` → `\u201c`
- `"` → `\u201d`

批量替换命令：
```bash
node -e "const fs=require('fs'); let c=fs.readFileSync('gen_ppt.js','utf8'); c=c.replace(/\u201c/g,'\\u201c').replace(/\u201d/g,'\\u201d'); fs.writeFileSync('gen_ppt.js',c);"
```

**Logo添加**：
- 封面页：右上角，尺寸2.3×0.9英寸
- 章节过渡页：右上角，尺寸2.0×0.8英寸
- 尾页：底部居中，尺寸2.3×0.9英寸

### Phase 5: Visual QA验证

使用python-pptx检测遮挡和溢出问题：

```python
from pptx import Presentation

PAGE_W, PAGE_H = 13.33, 7.5
prs = Presentation('output.pptx')

for i, slide in enumerate(prs.slides, 1):
    rects = []
    for shape in slide.shapes:
        l = shape.left / 914400
        t = shape.top / 914400
        w = shape.width / 914400
        h = shape.height / 914400
        rects.append((l, t, l+w, t+h))

    # Check overflow
    for l, t, r, b in rects:
        if r > PAGE_W + 0.1 or b > PAGE_H + 0.1:
            print(f'Slide {i}: OVERFLOW detected')

    # Check significant overlaps
    for j in range(len(rects)):
        for k in range(j+1, len(rects)):
            l1,t1,r1,b1 = rects[j]
            l2,t2,r2,b2 = rects[k]
            ox = min(r1,r2) - max(l1,l2)
            oy = min(b1,b2) - max(t1,t2)
            if ox > 0.08 and oy > 0.08:
                overlap_area = ox * oy
                if overlap_area > 0.3:  # Report significant overlaps
                    print(f'Slide {i}: Overlap area={overlap_area:.2f}')
```

**注意**：设计意图内的重叠（如全页背景矩形、卡片阴影、色条装饰）会产生误报，需要人工判断。

### Phase 6: 迭代优化

根据用户反馈调整，常见优化方向：
- 配色鲜亮度：将暗色系替换为鲜亮色系
- 布局多样化：避免每页重复相同布局
- 图表专业度：增加图例、脚注、参考线
- 照片质量：使用官方新闻源高清照片
- 无遮挡：调整元素坐标确保无意外重叠

## 配色方案参考

### 学术深色系（适合严肃学术场合）
| 角色 | 颜色 | 用途 |
|------|------|------|
| 主色 | #17375E | 封面背景、章节标题、导航栏 |
| 辅色 | #3276CB | 内容强调、按钮、链接 |
| 金色 | #C9A84C | 装饰线、编号、高亮 |
| 强调红 | #C0392B | 数据警示、重点标注 |
| 强调绿 | #27AE60 | 正面数据、目标达成 |
| 强调紫 | #6C5B7B | 补充信息、第三层级 |
| 浅蓝背景 | #DBEEF4 | 卡片背景、区域分隔 |
| 浅灰背景 | #F2F2F2 | 交替行背景 |

### 鲜亮学术系（适合分享/汇报场合）
| 角色 | 颜色 | 用途 |
|------|------|------|
| 主色 | #2B7DE9 | 亮蓝，替代深蓝 |
| 强调红 | #E8453C | 亮红，数据警示 |
| 强调绿 | #2ECC71 | 亮绿，正面数据 |
| 强调紫 | #9B59B6 | 亮紫，补充信息 |
| 金色 | #F5A623 | 亮金，装饰高亮 |

## 完整项目结构示例

```
project/
├── 发言稿.md                    # 源文档：发言稿
├── 论文.docx                    # 源文档：论文原文
├── 参考模板.pptx                # 参考PPT（可选）
├── gen_charts.py                # 图表生成脚本
├── gen_ppt.js                   # PPT生成脚本
├── ppt_charts/                  # 图表输出目录
│   ├── fig1_data_gap.png
│   ├── fig2_framework.png
│   ├── fig3_model.png
│   ├── fig4_guarantee.png
│   ├── fig5_paradigm.png
│   └── fig6_timeline.png
├── ppt_images/                  # 照片素材目录
│   ├── case_photo_1.png
│   └── logo.png
└── output.pptx                  # 最终输出
```

## 注意事项

1. **中文引号是第一杀手**：发言稿中的""在JS字符串中必崩，务必第一时间用`\u201c`/`\u201d`转义
2. **matplotlib字体缓存**：中文显示方框时，检查字体设置和缓存目录权限
3. **照片来源**：优先从官方网站下载高清照片，百度图片质量差不推荐
4. **PPTX文件体积**：主要由嵌入图片决定，高清照片(2-3MB/张)会导致PPTX>10MB
5. **参考PPT分析是关键**：设计DNA（配色/字号/布局）决定了PPT的专业度上限
6. **多样布局比统一布局更专业**：每页根据内容类型选择不同排版，而非千篇一律
