# 学术PPT生成踩坑经验集

## matplotlib 图表相关

### 1. 中文字体显示为方框
**问题**：matplotlib默认不支持中文，图表中文字全部显示为方框。
**解决**：在脚本开头显式设置中文字体：
```python
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False  # 负号也用中文字体渲染
```

### 2. 特殊Unicode字符报错
**问题**：`▸` (U+25B8)、`▶` (U+25B6) 等特殊符号在Microsoft YaHei字体中不存在，导致Warning。
**解决**：使用普通点号`·`或短横线`—`替代。

### 3. matplotlib缓存目录不可写
**问题**：沙箱环境中`C:\Users\xxx\.matplotlib`目录无写入权限，产生Warning。
**解决**：设置环境变量 `MPLCONFIGDIR` 到可写目录，或忽略Warning（图表仍可正常生成）。

### 4. DPI选择
- 200 DPI：一般展示足够
- 300 DPI：学术出版标准，推荐
- 600 DPI：印刷级别，文件过大不推荐用于PPT

## PptxGenJS 生成相关

### 5. 中文引号导致JS语法错误（最常见！）
**问题**：发言稿中的中文引号`""`在JavaScript字符串中与ASCII引号`""`冲突，导致SyntaxError。
**解决**：使用Unicode转义：
- `"` → `\u201c`
- `"` → `\u201d`

批量替换命令：
```bash
node -e "const fs=require('fs'); let c=fs.readFileSync('gen_ppt.js','utf8'); c=c.replace(/\u201c/g,'\\u201c').replace(/\u201d/g,'\\u201d'); fs.writeFileSync('gen_ppt.js',c);"
```

⚠️ **重要**：这是最高频问题，每次创建JS脚本后必须检查！

### 6. XML特殊字符（&符号）
**问题**：文本中包含`&`符号时，PptxGenJS生成PPTX可能报XML解析错误。
**解决**：使用`&amp;`转义，或直接替换为"与"/"和"。

### 7. 图片路径必须使用绝对路径
**问题**：相对路径在Node.js中可能导致文件找不到。
**解决**：使用 `path.resolve(__dirname, 'xxx')` 或 `path.join()` 构建绝对路径。

### 8. 图片不存在导致生成中断
**问题**：`addImage()`引用不存在的文件路径，生成过程报错中断。
**解决**：始终用 `fs.existsSync()` 检查文件是否存在后再添加：
```javascript
if (fs.existsSync(imagePath)) {
  slide.addImage({ path: imagePath, x, y, w, h });
}
```

### 9. PptxGenJS运行方式
**问题**：直接运行 `node gen_ppt.js` 可能找不到pptxgenjs模块。
**解决**：设置NODE_PATH环境变量：
```bash
NODE_PATH=<workspace>/node_modules node gen_ppt.js
```
或在项目目录下先 `npm install pptxgenjs`。

## 排版相关

### 10. 页面尺寸
- 16:9宽屏：13.33 × 7.5 英寸（PptxGenJS的LAYOUT_WIDE）
- 4:3标准：10 × 7.5 英寸

### 11. 元素遮挡检测
**问题**：程序化生成的PPT容易出现元素重叠遮挡。
**解决**：
- 使用 `scripts/visual_qa.py` 进行自动化检测
- 关键原则：每个shape的(x, y, x+w, y+h)矩形不与其他shape相交
- 设计意图内的重叠（如全页背景矩形）会产生误报，需人工判断

### 12. 侧边栏 vs 全幅布局
- **侧边栏布局**：左侧导航栏(w=1.0)，内容区x≥1.2，空间受限但导航清晰
- **全幅布局**：无边栏，内容区x≥0.55，空间充裕但无导航
- **推荐**：学术汇报用全幅布局，内容更宽松

### 13. 数据卡片样式
标准数据卡片结构：
```
┌─────────────────┐  ← 阴影(偏移0.03)
│ ▎  58%          │  ← 左色条(0.06宽) + 数值(26pt粗体)
│    专业匹配度    │  ← 标签(11pt灰色)
└─────────────────┘
```

### 14. 多样化布局的重要性
**问题**：每页相同布局（如都是左图+右面板）会显得呆板。
**解决**：根据内容类型选择不同排版模板（参见layout_templates.md）。

## 照片素材相关

### 15. 照片来源优先级
1. **官方网站**（院校官网、央广网、新华网）— 最高质量，2-3MB/张
2. **新闻媒体**（中国日报、人民网）— 中高质量
3. **百度图片** — 质量差，不推荐（通常60-100KB）

### 16. 照片下载命令
```bash
curl -L -o output.png "https://example.com/image.png"
```
注意：某些网站需要添加User-Agent header。

## 参考PPT分析

### 17. python-pptx分析参考PPT
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu

prs = Presentation('reference.pptx')
for slide in prs.slides:
    for shape in slide.shapes:
        # 获取位置和尺寸
        left = shape.left / 914400    # EMU → 英寸
        top = shape.top / 914400
        width = shape.width / 914400
        height = shape.height / 914400

        # 获取填充色
        if hasattr(shape, 'fill'):
            fill = shape.fill
            # fill.type, fill.fore_color.rgb 等

        # 获取文本
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    # run.text, run.font.size, run.font.color.rgb
```

### 18. 设计DNA提取清单
分析参考PPT时必须提取：
- [ ] 主色、辅色、强调色的十六进制值
- [ ] 标题字体、正文字体名称
- [ ] 字号体系（标题/副标题/正文/注释）
- [ ] 封面页布局（背景色、标题位置、装饰元素坐标）
- [ ] 章节过渡页布局（编号风格、标题位置、装饰线位置）
- [ ] 内容页布局（导航栏位置、图文分区方式）
- [ ] 尾页布局
