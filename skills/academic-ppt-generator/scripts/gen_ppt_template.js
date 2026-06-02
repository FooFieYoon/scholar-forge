/**
 * 学术PPT PptxGenJS 生成脚本模板
 *
 * 依赖：pptxgenjs
 * 安装：npm install pptxgenjs
 * 运行：NODE_PATH=./node_modules node gen_ppt_template.js
 *
 * 注意事项：
 * 1. 中文引号 "" 在JS字符串中会导致语法错误，必须使用 \u201c \u201d 转义
 * 2. 所有shape坐标需精确计算，避免遮挡重叠
 * 3. 图片路径使用绝对路径或path.resolve
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ========== 配置 ==========
const FONT_CN = "Microsoft YaHei";
const FONT_EN = "Arial";
const CHART_DIR = path.resolve(__dirname, "ppt_charts");  // 图表目录
const IMG_DIR = path.resolve(__dirname, "ppt_images");     // 图片目录
const LOGO_PATH = path.join(IMG_DIR, "logo.png");          // Logo路径

// 配色方案（学术深色系）
const C = {
  navy:    "17375E",   // 主色-深蓝
  blue:    "3276CB",   // 辅色-蓝
  gold:    "C9A84C",   // 金色装饰
  red:     "C0392B",   // 强调-红
  green:   "27AE60",   // 强调-绿
  purple:  "6C5B7B",   // 强调-紫
  ltBlue:  "DBEEF4",   // 浅蓝背景
  ltGray:  "F2F2F2",   // 浅灰背景
  white:   "FFFFFF",
  black:   "333333",
  gray:    "666666",
};

const PAGE_W = 13.33;  // 16:9 宽屏
const PAGE_H = 7.5;

// ========== 辅助函数 ==========

/**
 * 创建章节过渡页
 * @param {Presentation} prs - pptxgenjs实例
 * @param {number} num - 章节编号
 * @param {string} title - 章节标题
 * @param {string} english - 英文引言
 * @param {string} accentColor - 强调色
 * @returns {Slide}
 */
function createChapterSlide(prs, num, title, english, accentColor) {
  const slide = prs.addSlide();

  // 大编号
  slide.addText(String(num).padStart(2, "0"), {
    x: 1.2, y: 1.8, w: 3.0, h: 1.0,
    fontSize: 56, fontFace: FONT_CN, color: C.navy,
    bold: true
  });

  // 金色短装饰线
  slide.addShape(prs.shapes.RECTANGLE, {
    x: 1.2, y: 2.9, w: 2.0, h: 0.02,
    fill: { color: C.gold }
  });

  // 章节标题
  slide.addText(title, {
    x: 1.2, y: 3.1, w: 8.0, h: 0.8,
    fontSize: 32, fontFace: FONT_CN, color: C.navy,
    bold: true
  });

  // 英文引言装饰
  slide.addText(english, {
    x: 1.2, y: 4.0, w: 8.0, h: 0.4,
    fontSize: 9, fontFace: FONT_EN, color: C.gray,
    italic: true
  });

  // Logo（右上角）
  if (fs.existsSync(LOGO_PATH)) {
    slide.addImage({ path: LOGO_PATH, x: 10.8, y: 0.25, w: 2.0, h: 0.8 });
  }

  // 底部金色长装饰线
  slide.addShape(prs.shapes.RECTANGLE, {
    x: 1.2, y: 6.2, w: 10.9, h: 0.02,
    fill: { color: C.gold }
  });

  return slide;
}

/**
 * 创建内容页顶栏
 * @param {Slide} slide
 * @param {string} title - 页面标题
 */
function addTopBar(slide, title) {
  // 顶栏背景
  slide.addShape(prs.shapes.RECTANGLE, {
    x: 0, y: 0, w: PAGE_W, h: 0.55,
    fill: { color: C.navy }
  });

  // 顶栏标题
  slide.addText(title, {
    x: 0.55, y: 0, w: 10.0, h: 0.55,
    fontSize: 18, fontFace: FONT_CN, color: C.white,
    bold: true, valign: "middle"
  });

  // 金色装饰线
  slide.addShape(prs.shapes.RECTANGLE, {
    x: 0, y: 0.55, w: PAGE_W, h: 0.02,
    fill: { color: C.gold }
  });
}

/**
 * 创建数据卡片
 * @param {Slide} slide
 * @param {number} x - 左上角x
 * @param {number} y - 左上角y
 * @param {number} w - 宽度
 * @param {string} value - 数值文本
 * @param {string} label - 标签文本
 * @param {string} accentColor - 左色条颜色
 */
function addDataCard(slide, x, y, w, value, label, accentColor) {
  const cardH = 1.8;

  // 卡片阴影（偏移0.03）
  slide.addShape(prs.shapes.RECTANGLE, {
    x: x + 0.03, y: y + 0.03, w: w, h: cardH,
    fill: { color: "E0E0E0" }, rectRadius: 0.08
  });

  // 卡片主体
  slide.addShape(prs.shapes.RECTANGLE, {
    x, y, w, h: cardH,
    fill: { color: C.white }, rectRadius: 0.08,
    line: { color: "E8E8E8", width: 0.5 }
  });

  // 左色条
  slide.addShape(prs.shapes.RECTANGLE, {
    x, y: y + 0.15, w: 0.06, h: cardH - 0.3,
    fill: { color: accentColor }, rectRadius: 0.03
  });

  // 数值
  slide.addText(value, {
    x: x + 0.2, y: y + 0.2, w: w - 0.3, h: 0.8,
    fontSize: 26, fontFace: FONT_CN, color: accentColor,
    bold: true, valign: "middle"
  });

  // 标签
  slide.addText(label, {
    x: x + 0.2, y: y + 1.0, w: w - 0.3, h: 0.5,
    fontSize: 11, fontFace: FONT_CN, color: C.gray,
    valign: "top"
  });
}

// ========== 主函数 ==========
function main() {
  const prs = new pptxgen();
  prs.layout = "LAYOUT_WIDE";  // 13.33 x 7.5

  // ====== Slide 1: 封面 ======
  const s1 = prs.addSlide();
  s1.addShape(prs.shapes.RECTANGLE, {
    x: 0, y: 0, w: PAGE_W, h: PAGE_H,
    fill: { color: C.navy }
  });
  // 金色装饰线1
  s1.addShape(prs.shapes.RECTANGLE, {
    x: 2.5, y: 2.0, w: 8.0, h: 0.015,
    fill: { color: C.gold }
  });
  // 主标题
  s1.addText("数字化赋能下应用型高校\n产教融合命运共同体的构建逻辑与路径", {
    x: 1.5, y: 2.2, w: 10.0, h: 1.5,
    fontSize: 36, fontFace: FONT_CN, color: C.white,
    bold: true, align: "center", lineSpacingMultiple: 1.3
  });
  // 副标题
  s1.addText("\u2014\u2014基于黑龙江省\u201c四链\u201d深度融合的思考", {
    x: 1.5, y: 3.8, w: 10.0, h: 0.6,
    fontSize: 18, fontFace: FONT_CN, color: "A8C8E8",
    align: "center"
  });
  // 金色装饰线2
  s1.addShape(prs.shapes.RECTANGLE, {
    x: 2.5, y: 4.5, w: 8.0, h: 0.015,
    fill: { color: C.gold }
  });
  // 作者信息
  s1.addText("汇报人：XXX    单位：XXX    2025年X月", {
    x: 1.5, y: 5.2, w: 10.0, h: 0.4,
    fontSize: 14, fontFace: FONT_CN, color: C.white,
    align: "center"
  });
  // Logo
  if (fs.existsSync(LOGO_PATH)) {
    s1.addImage({ path: LOGO_PATH, x: 10.5, y: 0.25, w: 2.3, h: 0.9 });
  }

  // ====== Slide 2: 目录 ======
  const s2 = prs.addSlide();
  addTopBar(s2, "汇报提纲");

  const tocItems = [
    { num: "01", title: "现实的困境", color: C.red },
    { num: "02", title: "逻辑重构", color: C.blue },
    { num: "03", title: "实践模型", color: C.green },
    { num: "04", title: "理论验证", color: C.purple },
    { num: "05", title: "保障与展望", color: C.gold },
  ];

  tocItems.forEach((item, idx) => {
    const y = 0.9 + idx * 1.1;
    // 左色条
    s2.addShape(prs.shapes.RECTANGLE, {
      x: 0.8, y: y, w: 0.08, h: 0.8,
      fill: { color: item.color }, rectRadius: 0.04
    });
    // 编号
    s2.addText(item.num, {
      x: 1.1, y: y, w: 0.8, h: 0.8,
      fontSize: 24, fontFace: FONT_EN, color: item.color,
      bold: true, valign: "middle"
    });
    // 标题
    s2.addText(item.title, {
      x: 2.0, y: y, w: 4.0, h: 0.8,
      fontSize: 20, fontFace: FONT_CN, color: C.black,
      bold: true, valign: "middle"
    });
  });

  // 右侧概念卡片
  s2.addShape(prs.shapes.RECTANGLE, {
    x: 7.0, y: 0.9, w: 5.5, h: 5.5,
    fill: { color: C.ltBlue }, rectRadius: 0.1
  });
  s2.addText("核心概念", {
    x: 7.3, y: 1.1, w: 5.0, h: 0.5,
    fontSize: 16, fontFace: FONT_CN, color: C.navy,
    bold: true
  });
  // 添加核心概念内容...

  // ====== Slide 3: 章节过渡页 ======
  createChapterSlide(prs, 1, "现实的困境", "The Realistic Dilemma in Industry-Education Integration", C.red);

  // ====== Slide 4: 数据页 ======
  const s4 = prs.addSlide();
  addTopBar(s4, "数据佐证：产教融合关键指标");

  // 图表
  const chartPath = path.join(CHART_DIR, "fig1_data_gap.png");
  if (fs.existsSync(chartPath)) {
    s4.addImage({ path: chartPath, x: 0.55, y: 0.75, w: 7.5, h: 4.2 });
  }

  // 右侧数据卡片
  addDataCard(s4, 8.5, 0.75, 2.2, "58%", "专业匹配度", C.red);
  addDataCard(s4, 11.0, 0.75, 2.2, "12.6%", "转化率", C.red);

  // 底部矛盾卡片
  const contradictions = [
    { title: "供需错配", desc: "人才供给与产业需求脱节" },
    { title: "合作浅层", desc: "校企合作停留在表面" },
    { title: "机制缺失", desc: "缺乏长效利益分配机制" },
  ];
  contradictions.forEach((item, idx) => {
    const x = 0.55 + idx * 4.2;
    s4.addShape(prs.shapes.RECTANGLE, {
      x, y: 5.2, w: 3.8, h: 1.6,
      fill: { color: C.white }, rectRadius: 0.08,
      line: { color: "E8E8E8", width: 0.5 }
    });
    s4.addText(item.title, {
      x: x + 0.2, y: 5.3, w: 3.4, h: 0.4,
      fontSize: 14, fontFace: FONT_CN, color: C.red,
      bold: true
    });
    s4.addText(item.desc, {
      x: x + 0.2, y: 5.8, w: 3.4, h: 0.8,
      fontSize: 11, fontFace: FONT_CN, color: C.gray
    });
  });

  // ... 更多页面按照上述模式创建 ...

  // ====== 最后页: 感谢 ======
  const sLast = prs.addSlide();
  sLast.addShape(prs.shapes.RECTANGLE, {
    x: 0, y: 0, w: PAGE_W, h: PAGE_H,
    fill: { color: C.navy }
  });
  sLast.addText("感谢聆听", {
    x: 0, y: 2.5, w: PAGE_W, h: 1.0,
    fontSize: 40, fontFace: FONT_CN, color: C.white,
    bold: true, align: "center"
  });
  sLast.addText("敬请批评指正", {
    x: 0, y: 5.72, w: PAGE_W, h: 0.28,
    fontSize: 13, fontFace: FONT_CN, color: C.gold,
    align: "center"
  });
  if (fs.existsSync(LOGO_PATH)) {
    sLast.addImage({ path: LOGO_PATH, x: 5.5, y: 6.2, w: 2.3, h: 0.9 });
  }

  // ====== 保存 ======
  const outputPath = path.resolve(__dirname, "academic-presentation.pptx");
  prs.writeFile({ fileName: outputPath })
    .then(() => console.log(`✅ PPT saved: ${outputPath}`))
    .catch(err => console.error(`❌ Error: ${err.message}`));
}

main();
