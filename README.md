# ScholarForge / 学术匠心工坊

> **AI 驱动的学术写作与知识产权工具集**  
> 从选题到成稿，从代码到软著，从讲稿到汇报。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/FooFieYoon/scholar-forge?style=social)](https://github.com/FooFieYoon/scholar-forge)
[![GitHub Commits](https://img.shields.io/github/commit-activity/m/FooFieYoon/scholar-forge)](https://github.com/FooFieYoon/scholar-forge)
[![Python](https://img.shields.io/badge/Python-91%25-blue)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-9%25-yellow)](https://www.javascript.com/)
[![Skills](https://img.shields.io/badge/Skills-10-blue)](skills/)

---

## 📖 导航目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [技能一览](#技能一览)
- [安装使用](#安装使用)
- [技术说明](#技术说明)
- [更新日志](#更新日志)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [联系我们](#联系我们)
- [English Appendix](#english-appendix)

---

## 项目简介

**ScholarForge（学术匠心工坊）** 是一套面向研究人员、教师和开发者的 AI 技能合集，覆盖：

- 📝 **学术论文全流程写作**（期刊论文、会议论文、研究报告）
- 🔄 **AIGC 检测降重改写**（PaperYY 平台优化）
- 🎨 **学术汇报 PPT 制作**（自动化图表生成 + 专业排版）
- 📄 **软件著作权登记材料自动生成**（代码分析 + 文档输出）
- 🖼️ **图片知识提取与 OCR**（批量处理 + 智能分类）
- 🔧 **技能备份与同步**（GitHub 自动化管理）

所有技能均为 **Markdown 格式的指令文件（SKILL.md）**，可导入到支持自定义指令的主流 AI 编程平台使用。

### 🌟 项目特色

| 特色 | 说明 |
|------|------|
| 🤖 **AI 原生** | 所有技能由 AI Agent 创建，为 AI Agent 优化 |
| 🔌 **即插即用** | 简洁的 SKILL.md 格式，兼容多平台 |
| 🔄 **全生命周期** | 覆盖学术研究完整工作流 |
| 🎨 **多模态支持** | 文本、图表、演示文稿、代码文档 |
| 🌍 **开源共建** | MIT 许可证，社区驱动开发 |

---

## 核心特性

<table>
<tr>
<td width="50%">

### 📝 学术写作
- **多学科支持**：工程、教育、社科、医学、计算机等
- **智能选题推荐**：AI 驱动的研究方向分析
- **自动化结构生成**：遵循学术规范（IEEE、ACM、GB/T 7714）
- **参考文献管理**：自动格式化引文和参考书目

</td>
<td width="50%">

### 🎨 可视化与演示
- **学术图表**：300 DPI 出版级质量（Matplotlib）
- **PPT 自动生成**：学术汇报演示文稿（PptxGenJS）
- **视觉质量检查**：自动布局验证和错误检测
- **风格迁移**：从参考材料学习和应用设计模式

</td>
</tr>
<tr>
<td width="50%">

### 🔒 知识产权
- **软件著作权**：自动化文档生成和申请
- **代码分析**：智能项目结构扫描和文档化
- **模板驱动**：符合标准的申请材料生成

</td>
<td width="50%">

### 🖼️ 知识管理
- **OCR 批量处理**：多线程图像文字提取（RapidOCR）
- **自动分类**：智能内容分类（11 个类别）
- **多平台同步**：IMA/Notion/Obsidian 集成
- **断点续跑**：恢复中断的处理任务

</td>
</tr>
</table>

---

## 技能一览

### 📚 学术写作系列

#### 1️⃣ 学术年会论文写作助手
**`academic-conference-paper-writer`**

基于目标报告文集的风格规范（自动分析 PDF 样本），从会议通知材料出发，全流程完成：选题推荐 → 资料搜索 → 论文生成 → 图表匹配 → 排版输出 → 迭代修改。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 学术年会论文、会议征文、报告文集、年会投稿、会议论文写作 | 提供学术年会通知或往届论文集，需要撰写符合该会议风格的高质量学术报告 |

**核心能力：**
- 📄 **PDF 风格自动学习** —— 从往届文集中提取结构模式、标题体例、句式特征
- 💡 **选题推荐** —— 综合分析政策/期刊/案例，生成 3–5 个选题并标注可行支撑
- 📝 **逐章生成** —— 引言 → 理论 → 核心实践 → 成效 → 启示 → 结论
- 📊 **图表匹配** —— 自动识别配图位置，生成流程图/柱状图/框架图
- 📃 **Word 排版输出** —— 严格按会议模板输出格式化 .docx

---

#### 2️⃣ 通用学术论文写作助手
**`academic-paper-writer`**

支持任意学科领域（工程、教育、社科、管理、医学、计算机等）的期刊论文、会议论文、研究报告端到端写作。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 学术论文写作、期刊投稿、论文选题、论文大纲、文献综述、SCI 论文、核心期刊、研究报告、论文润色 | 提供投稿通知或选题，需要从选题到成稿的完整写作流程支持 |

**核心能力：**
- 🌐 **多学科适配** —— 支持实证研究/方法提出/综述/案例研究/理论构建等多种论文类型
- 🔍 **文献检索与综述** —— 自动生成文献检索策略并整理资料清单
- 📐 **大纲设计** —— 根据论文类型推荐对应结构模板
- 📖 **逐章生成** —— 引言 → 文献综述 → 方法/机制 → 结果/成效 → 讨论 → 结论
- 📚 **参考文献管理** —— 支持 GB/T 7714、APA、IEEE、Vancouver 等多种格式

**内置参考文档：** 论文结构模板、写作风格指南、引文格式手册、默认排版规范

---

#### 3️⃣ 教学科研论文撰写辅助
**`edu-research-paper`**

面向中小学及高校教师，专注教育科研论文的全流程写作指导，覆盖课题研究报告、期刊投稿论文、结题报告等常见类型。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 教学科研论文、教育论文、课题报告、结题报告、教研论文、教学方法、课例研究、教学案例、论文框架 | 教师需要撰写教育类论文，从选题策略到各章节规范的全流程指导 |

**核心能力：**
- 🎯 **选题策略** —— 四大选题原则（创新性/真实性/切口精准/可行性）+ 题目拟定三要素
- 📋 **结构化框架** —— 期刊论文标准结构、课题结题报告完整结构
- ✍️ **逐节撰写指南** —— 摘要四要素、引言三段式、文献综述"卖鞋逻辑"、研究设计方法选用
- 📈 **图表规范** —— 全文连续编号、图题表题位置、先文后图表原则、图表类型选用指南
- ✅ **质量检查清单** —— 15 条自查项覆盖全篇常见问题

---

### 🎨 可视化与演示系列

#### 4️⃣ 学术汇报 PPT 生成器 ✨
**`academic-ppt-generator`**

从学术论文/发言稿出发，自动生成专业学术汇报 PPT。支持参考 PPT 设计 DNA 提取、学术级图表绘制（matplotlib 300DPI）、多样化布局排版、Visual QA 验证，实现"讲稿 → PPT"的一键转换。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 学术PPT、汇报PPT、答辩PPT、论文汇报、学术报告PPT、制作PPT、生成PPT | 提供论文/发言稿，需要制作符合学术规范的高质量汇报PPT |

**核心能力：**
- 📖 **源文档解析** —— 自动提取发言稿/论文的章节结构、核心论点、关键数据
- 🎨 **设计 DNA 分析** —— 提取目标 PPT 的配色方案、字号体系、布局模式、设计元素
- 📊 **学术级图表生成** —— matplotlib 300DPI，6 种专业图表类型
- 📐 **多样化布局排版** —— 10 种学术 PPT 布局模板，每页根据内容类型选择最佳布局
- ✔️ **Visual QA 验证** —— python-pptx 自动检测元素遮挡、页面溢出、间距异常
- 🔄 **迭代优化** —— 自动修复遮挡问题，支持多轮调整

**6 种学术图表类型：**

| 图表类型 | 适用场景 | 学术规范 |
|---------|---------|---------|
| 水平柱状图 + 目标参考线 | 数据缺口/差距展示 | 图例 + 数据来源脚注 + 差距区间填充 |
| 中心辐射式概念框架图 | 理论框架/融合机制 | 双向箭头 + 连接标签框 + 装饰光环 |
| 层次架构模型图 | 实践模型/体系架构 | 多层结构 + 金色连线 + 虚线反馈 |
| 三柱保障体系图 | 保障机制/制度体系 | 色条强调 + 标题头 + 详情列表 |
| 范式对比表图 | 新旧对比/模式转型 | 多维度横向对比 + 箭头 + 交替行背景 |
| 实践时间线图 | 发展历程/里程碑 | 箭头末端 + 彩色节点 + 事件详情 |

**内置资源：**
- `scripts/generate_charts.py` — matplotlib 学术图表生成模板
- `scripts/gen_ppt_template.js` — PptxGenJS PPT 生成模板（含辅助函数）
- `scripts/visual_qa.py` — Visual QA 验证脚本（python-pptx 检测遮挡/溢出）
- `references/layout_templates.md` — 10 种学术 PPT 布局模板参考
- `references/pitfalls.md` — 18 条踩坑经验（中文引号/字体/路径等）

**技术栈：** PptxGenJS + matplotlib + python-pptx

---

### 🔒 知识产权系列

#### 5️⃣ 软件著作权材料生成器
**`project-softcopyright-generator`**

读取本地项目代码，自动分析项目结构、功能模块、技术架构，生成软著申请所需的系统说明文档与源代码文档。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 软著申请、软件著作权、著作权登记、代码文档、源码文档、软著材料、版权登记 | 已有本地项目代码，需要整理软著申请资料 |

**核心能力：**
- 🔍 **项目扫描** —— 自动分析技术栈、目录结构、入口文件、核心模块
- 📝 **建议稿生成** —— 输出软件全称/简称/版本/功能/技术特点/模块划分建议
- 📋 **代码候选管理** —— 生成候选清单 + 可编辑选择 JSON，人工确认后生成正式文档
- 📄 **分页代码抽取** —— 前 30 页 + 后 30 页，每页 60 行，保持代码连续性
- 📑 **正式文档输出** —— 系统说明文档 .docx + 源代码文档 .docx + 申请信息 .txt

**内置模板脚本：** 项目扫描、建议稿生成、代码候选管理、说明文档生成、源代码文档生成、.docx 渲染

---

### 🔄 内容优化系列

#### 6️⃣ PaperYY AIGC 检测降重改写
**`paperyy-aigc-rewrite`**

针对 PaperYY 平台 AIGC 检测规则，对学术论文进行系统性人工化深度改写，目标将 AIGC 疑似率控制在 14%–16%。

| 触发关键词 | 适用场景 |
|-----------|---------|
| AIGC 降重、降 AIGC 率、去 AI 痕迹、论文人工化、PaperYY、人工智能检测、查重降重、论文改写 | 提供 .docx 论文文件，需要降低 AIGC 检测疑似率 |

**核心能力：**
- 🤖 **AI 特征识别** —— 自动定位政策引用开篇、演进叙事、"一方面…另一方面…"、"研究表明"等高风险句式
- ✍️ **逐段改写** —— 摘要改写、引言重组、文献综述叙事化、结果分析去模板化、结论自然收尾
- 🔄 **全局替换规则** —— 高风险词（深度融合/赋能/重构/路径优化 → 人工化替代表达）
- 💾 **DOCX 格式保留** —— 替换脚本保持原文段落格式、字体、字号、表格、图片不变
- 🔒 **数据安全约束** —— 统计数字、p 值、参考文献、标题层级、专业术语原样保留

---

### 🖼️ 知识管理系列

#### 7️⃣ 图片知识提取（通用型）
**`image-knowledge-extractor`**

从任意图片文件夹中批量提取文字（OCR）、按用户指定类别或标签整理、输出为 Markdown 报告或上传至指定笔记/知识库平台的全流程自动化技能。支持 HEIC/JPG/PNG/WEBP/GIF/BMP 等格式。平台包括：IMA 知识库、Notion、Obsidian 目录、纯 Markdown 文件输出。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 整理图片知识、图片OCR、截图整理、知识提取、批量提取图片文字、截图转文字、从图片提取内容 | 批量处理手机截图中的知识内容、OCR 识别文档/照片文字、将提取内容分类整理为结构化笔记、上传至 IMA/Notion/Obsidian 等平台 |

**核心能力：**
- ⚡ **多进程 OCR 加速** —— RapidOCR 引擎支持中文，4 进程处理 171 张图片仅需 25 分钟
- 🌐 **多平台输出** —— IMA 知识库 / Notion / Obsidian / 纯 Markdown
- 🏷️ **4 种分类模式** —— 自动分类(11 类别) / 手动指定 / 标签模式 / 不分类
- 📱 **HEIC 格式支持** —— 完整读取 iPhone 截图
- 🔄 **断点续跑** —— checkpoint 机制，支持中断后继续

---

#### 8️⃣ 图片知识 OCR（IMA 专用）
**`image-knowledge-ocr`**

从图片文件夹中批量提取文字（OCR）、按内容分类整理知识、上传至 IMA 知识库的全流程自动化技能。适用于处理手机截图/照片中的知识内容，批量 OCR 识别图片文字，将 OCR 结果分类整理为知识笔记，上传笔记至 IMA"日常"知识库。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 整理图片知识、图片OCR、截图整理、知识提取、IMA 上传 | 处理手机截图中的知识内容、批量 OCR 识别图片文字、将 OCR 结果分类整理为知识笔记、上传笔记至 IMA"日常"知识库 |

**核心能力：**
- 🗂️ **9 大知识类别自动分类** —— AI/编程/科研/开源/论文/职场/网络/3D 设计/视频
- 📚 **IMA 知识库集成** —— import_doc API 创建详细笔记（3000-5000 字/篇）
- 🔗 **add_knowledge 知识库关联** —— base64 格式 KB ID + note_info 格式
- 🛠️ **常见问题解决** —— BOM 清除、note_id 不一致、认证失败

---

#### 9️⃣ 图片知识 OCR（IMA 专用 - 备份）
**`image-knowledge-ocr-ima`**

图片知识 OCR 提取与 IMA 上传的备份版本，与 `image-knowledge-ocr` 功能完全一致，为版本管理保留。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 整理图片知识、图片OCR、截图整理、知识提取、IMA 上传 | 同 `image-knowledge-ocr` |

**核心能力：** 同 `image-knowledge-ocr`

---

### 🔧 实用工具系列

#### 🔟 技能备份同步
**`backup-skills-to-github`**

将原创技能通过 GitHub REST API 自动上传到本仓库进行版本管理。**采用增量 README 更新机制** —— 每次只添加新技能条目，已有内容和手动撰写的说明完全保留。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 备份技能、上传技能、同步到 GitHub、backup skills、sync to github | 需要将本地技能同步到远程仓库进行版本管理或分享 |

**核心特性：**
- 🔓 **绕过 Windows git schannel 问题** —— 通过 REST API 直接上传
- 📝 **README 增量更新** —— 每次只追加新条目，不覆盖已有内容
- ⚙️ **灵活选项** —— 支持 `--all` 全量扫描和 `--skill` 指定上传

---

## 安装使用

### 🚀 快速开始

#### 前置要求

- **Python**: 3.x（推荐：3.13+）
- **Node.js**: 22.x（用于 PPT 生成功能）
- **Git**: 用于克隆仓库

#### 5 分钟快速上手

```bash
# 1. 克隆仓库
git clone https://github.com/FooFieYoon/scholar-forge.git ~/scholar-forge/

# 2. 选择你的 AI 平台
# 选项 A: CodeBuddy
#    进入「设置 → Skills 管理 → 从文件夹安装」，选择 ~/scholar-forge/skills/

# 选项 B: Cursor
#    将 SKILL.md 内容复制到项目根目录 .cursorrules 中，
#    或将整个 skills/ 目录放入项目的 .cursor/instructions/

# 选项 C: Claude Code
#    将 SKILL.md 内容放入 CLAUDE.md 文件（项目级）
#    或通过 /add-instructions 导入

# 3. 开始使用
#    使用关键词触发技能（参见各技能的"触发关键词"部分）
```

---

### 📦 安装方法

#### 方法 1：通过 Git 克隆（推荐）

```bash
git clone https://github.com/FooFieYoon/scholar-forge.git
cd scholar-forge
```

#### 方法 2：下载 ZIP

1. 访问 [GitHub 仓库](https://github.com/FooFieYoon/scholar-forge)
2. 点击「Code」→「Download ZIP」
3. 解压到你想放置的位置

#### 方法 3：安装特定技能

每个技能都是独立的。你可以只安装你需要的技能：

```bash
# 示例：只安装 academic-paper-writer
cp -r scholar-forge/skills/academic-paper-writer ~/my-skills/
```

---

### 📖 使用指南

#### 平台兼容性

本仓库中的技能采用 Markdown + YAML frontmatter 格式（SKILL.md），兼容以下主流 AI 平台：

| 平台 | 安装方式 |
|------|---------|
| **CodeBuddy** | 「设置 → Skills 管理 → 从文件夹安装」，选择对应 skill 子目录 |
| **Cursor** | 将 `SKILL.md` 内容复制到项目根目录 `.cursorrules` 中，或将整个 `skills/` 目录放入项目的 `.cursor/instructions/` |
| **Claude Code** | 将 `SKILL.md` 内容放入 `CLAUDE.md` 文件（项目级）或通过 `/add-instructions` 导入 |
| **GitHub Copilot** | 将 `SKILL.md` 内容粘贴到 `.github/copilot-instructions.md` |
| **Windsurf** | 将 `SKILL.md` 内容写入 `.windsurfrules` |
| **ChatGPT Projects** | 在 ChatGPT 的「自定义指令」或 Project 设置中粘贴 `SKILL.md` 的核心指令部分 |
| **通用 AI 对话** | 将 `SKILL.md` 中 `---` 分隔线之后的内容作为系统提示词直接粘贴使用 |

#### 典型工作流

```
1. 选择技能 → 2. 导入到 AI 平台 → 3. 使用关键词触发 → 4. 提供输入材料 → 5. AI 生成输出
```

#### 示例：使用学术论文写作助手

```
用户："我需要写一篇关于深度学习教育应用的论文，能帮我吗？"

AI：[自动加载 academic-paper-writer 技能]
    "我会帮你写这篇论文。让我先根据当前研究趋势推荐一些选题..."
    
    [生成选题推荐]
    [创建论文大纲]
    [逐章生成内容]
    [格式化参考文献]
    [输出 .docx 文件]
```

---

### 🔄 跨平台迁移注意事项

部分技能包含 Python/Node.js 脚本，迁移到其他平台时需：

1. 复制完整的 skill 目录（包含 `scripts/`、`templates/`、`references/` 子目录）
2. 确保目标环境已安装 Python 3.x 及所需依赖（`python-docx`、`matplotlib` 等）
3. PPT 生成技能需额外安装 Node.js 及 `pptxgenjs` 依赖
4. 各技能的具体依赖见对应 `SKILL.md` 中的工具速查表

详细配置指南参见 [`docs/tools-guide.md`](docs/tools-guide.md)。

---

## 技术说明

### 🏗️ 技术架构

```
┌─────────────────────────────────────────────────┐
│              ScholarForge 生态系统              │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐      ┌──────────────┐       │
│  │   SKILL.md   │──────│  AI 平台     │       │
│  │  (Markdown)  │      │  (CodeBuddy) │       │
│  └──────────────┘      └──────────────┘       │
│         │                                       │
│         ↓                                       │
│  ┌──────────────┐      ┌──────────────┐       │
│  │  Python 3.x  │──────│  Node.js 22  │       │
│  │  (后端)      │      │   (前端)      │       │
│  └──────────────┘      └──────────────┘       │
│         │                                       │
│         ↓                                       │
│  ┌──────────────────────────────────┐          │
│  │    输出格式                       │          │
│  │  .docx  .pptx  .png  .txt  .md │          │
│  └──────────────────────────────────┘          │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 📦 依赖项

<details>
<summary><b>Python 依赖（点击展开）</b></summary>

```txt
python-docx>=0.8.11     # Word 文档生成
matplotlib>=3.5.0       # 学术图表生成
python-pptx>=0.6.21     # PowerPoint 生成
rapidocr>=1.0.0         # OCR 处理
Pillow>=9.0.0           # 图像处理
pandas>=1.3.0           # 数据处理
numpy>=1.21.0           # 数值计算
```

</details>

<details>
<summary><b>Node.js 依赖（点击展开）</b></summary>

```txt
pptxgenjs>=3.12.0      # PPT 生成
```

</details>

---

## 项目结构

```
scholar-forge/
├── skills/                                   # 技能包目录
│   ├── academic-conference-paper-writer/      # 学术年会论文写作
│   ├── academic-paper-writer/                 # 通用学术论文写作
│   │   └── references/                        #   结构/引文/风格参考
│   ├── academic-ppt-generator/                # 学术PPT生成器
│   │   ├── scripts/                           #   图表/PPT/QA脚本
│   │   └── references/                        #   布局模板+踩坑经验
│   ├── edu-research-paper/                    # 教学科研论文写作
│   ├── paperyy-aigc-rewrite/                  # AIGC 检测降重改写
│   │   ├── references/                        #   检测规则+改写范例
│   │   └── scripts/                           #   docx 段落替换脚本
│   ├── project-softcopyright-generator/        # 软著材料生成
│   │   ├── templates/                         #   6 个流水线模板脚本
│   │   └── references/                        #   申请字段规范+设计规范
│   ├── image-knowledge-extractor/               # 图片知识提取（通用型）
│   │   └── references/                          #   多平台API参考
│   ├── image-knowledge-ocr/                     # 图片知识OCR（IMA专用）
│   │   └── references/                          #   IMA OpenAPI参考
│   ├── image-knowledge-ocr-ima/                 # 图片知识OCR（IMA专用-备份）
│   │   └── references/                          #   IMA OpenAPI参考
│   └── backup-skills-to-github/               # 技能备份同步
│       └── scripts/                           #   扫描/上传/整理脚本
├── docs/                                      # 文档目录
│   └── tools-guide.md                         #   工具配置指南
├── .gitignore
├── LICENSE
└── README.md                                  # 本文件
```

---

## 更新日志

### 📅 2026-06-08
- ✨ 更新 `image-knowledge-extractor` 图片知识提取（通用型）
  - 多进程OCR加速（RapidOCR引擎，4进程处理171张图片仅需25分钟）
  - 多平台输出（IMA知识库/Notion/Obsidian/纯Markdown）
  - 4种分类模式（自动分类/手动指定/标签模式/不分类）
  - HEIC格式支持，断点续跑机制
- ✨ 更新 `image-knowledge-ocr` 图片知识 OCR（IMA 专用）
  - 9大知识类别自动分类（AI/编程/科研/开源/论文/职场/网络/3D设计/视频）
  - IMA知识库集成（import_doc API创建3000-5000字/篇详细笔记）
  - add_knowledge知识库关联，支持base64格式KB ID
- ✨ 更新 `image-knowledge-ocr-ima` 图片知识 OCR（IMA 专用 - 备份）
  - `image-knowledge-ocr`的备份版本，功能完全一致，用于版本管理保留

### 📅 2026-06-02
- ✨ 新增 `academic-ppt-generator` 学术汇报 PPT 生成器
  - 6 种学术级图表类型（matplotlib 300DPI）
  - 10 种多样化布局模板
  - Visual QA 自动验证
  - 18 条踩坑经验文档
  - 完整的 PptxGenJS + python-pptx 脚本模板

### 📅 2026-05-30
- 🔧 新增 `backup-skills-to-github` 技能备份同步工具

### 📅 2026-05-28
- 🔧 新增 `project-softcopyright-generator` 软著材料生成器

### 📅 2026-05-25
- 🔧 新增 `paperyy-aigc-rewrite` AIGC 检测降重改写

### 📅 2026-05-20
- 🔧 新增 `edu-research-paper` 教学科研论文撰写辅助

### 📅 2026-05-15
- 🎉 初始版本发布
- 🔧 新增 `academic-conference-paper-writer` 学术年会论文写作助手
- 🔧 新增 `academic-paper-writer` 通用学术论文写作助手

---

## 贡献指南

我们欢迎社区的贡献！以下是一些你可以帮助改进项目的方式：

### 🤝 贡献方式

- 🐛 **报告 Bug**：打开一个 issue 描述问题
- 💡 **建议功能**：提出新技能或改进建议
- 📝 **改进文档**：修正错别字、添加示例、澄清说明
- 🔧 **提交 Pull Request**：修复 bug、添加功能、改进代码质量
- ⭐ **给仓库点星**：展示你的支持！

### 🔄 开发工作流

```bash
# 1. Fork 仓库
# 2. 创建你的功能分支
git checkout -b feature/AmazingFeature

# 3. 提交你的更改
git commit -m 'Add some AmazingFeature'

# 4. 推送到分支
git push origin feature/AmazingFeature

# 5. 打开 Pull Request
```

### 📋 技能开发指南

创建新技能时，请遵循以下指南：

1. **文件命名**：使用 kebab-case（例如，`academic-paper-writer`）
2. **SKILL.md 格式**：包含 YAML frontmatter + Markdown 指令
3. **文档**：在技能目录中添加详细的 README
4. **测试**：在至少 2 个 AI 平台上测试你的技能
5. **示例**：提供示例输入和预期输出

---

## 许可证

本项目采用 **MIT 许可证** —— 详情请参阅 [LICENSE](LICENSE) 文件。

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

---

## 联系我们

- **维护者**：Yin
- **GitHub Issues**：[打开 Issue](https://github.com/FooFieYoon/scholar-forge/issues)
- **仓库地址**：[https://github.com/FooFieYoon/scholar-forge](https://github.com/FooFieYoon/scholar-forge)

---

## 致谢

- 感谢所有帮助改进本项目的贡献者
- 特别感谢开源社区提供的优秀工具和库
- 灵感来源于 AI 时代对更好学术写作工具的需求

---

## 📌 引用

如果在研究或项目中使用 ScholarForge，请引用：

```bibtex
@software{scholarforge2026,
  author = {Yin},
  title = {ScholarForge: AI-Powered Academic Writing & IP Tools Collection},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/FooFieYoon/scholar-forge}
}
```

---

<div align="center">

**⭐ 如果觉得有帮助，请给仓库点星！**

Made with ❤️ by [Yin](https://github.com/FooFieYoon)

</div>

---

---

---

# English Appendix

> **AI-Powered Academic Writing & IP Tools Collection**  
> From topic selection to final manuscript, from code to software copyright.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/FooFieYoon/scholar-forge?style=social)](https://github.com/FooFieYoon/scholar-forge)
[![GitHub Commits](https://img.shields.io/github/commit-activity/m/FooFieYoon/scholar-forge)](https://github.com/FooFieYoon/scholar-forge)
[![Python](https://img.shields.io/badge/Python-91%25-blue)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-9%25-yellow)](https://www.javascript.com/)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Skill Collection](#skill-collection)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Technical Stack](#technical-stack)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

**ScholarForge (Academic Craftsmanship Workshop)** is a comprehensive collection of AI-driven academic tools designed to streamline the entire research and writing workflow. All tools are implemented as **Markdown-based instruction files (SKILL.md)** that can be imported into mainstream AI programming platforms.

### 🌟 What Makes ScholarForge Special?

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Native** | Every skill is crafted by AI agents for AI agents |
| 🔌 **Plug-and-Play** | Simple SKILL.md format, compatible with multiple platforms |
| 🔄 **Full Lifecycle** | Covers the entire academic workflow from topic selection to publication |
| 🎨 **Multi-Modal** | Supports text, charts, presentations, and code documentation |
| 🌍 **Open Source** | MIT licensed, community-driven development |

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 📝 Academic Writing
- **Multi-discipline Support**: Engineering, Education, Social Sciences, Medicine, Computer Science, etc.
- **Intelligent Topic Recommendation**: AI-powered research topic analysis and suggestion
- **Automated Structure Generation**: Follows academic standards (IEEE, ACM, GB/T 7714)
- **Reference Management**: Automatic citation formatting and bibliography generation

</td>
<td width="50%">

### 🎨 Visual & Presentation
- **Academic Charts**: 300 DPI publication-quality figures (Matplotlib)
- **PPT Generation**: Automated academic presentation creation (PptxGenJS)
- **Visual QA**: Automated layout validation and error detection
- **Style Transfer**: Learn and apply design patterns from reference materials

</td>
</tr>
<tr>
<td width="50%">

### 🔒 Intellectual Property
- **Software Copyright**: Automated documentation for software copyright registration
- **Code Analysis**: Intelligent project structure scanning and documentation
- **Template-Based**: Standard-compliant application materials generation

</td>
<td width="50%">

### 🖼️ Knowledge Management
- **OCR Batch Processing**: Multi-threaded image text extraction (RapidOCR)
- **Auto-Classification**: Intelligent content categorization (11 categories)
- **Multi-Platform Sync**: IMA/Notion/Obsidian integration
- **Breakpoint Recovery**: Resume interrupted processing tasks

</td>
</tr>
</table>

---

## 🛠️ Skill Collection

### 📚 Academic Writing Series

#### 1️⃣ Academic Conference Paper Writer
**`academic-conference-paper-writer`**

Automated academic conference paper writing based on target proceedings style (automatic PDF sample analysis). From conference call-for-papers to final manuscript: topic recommendation → literature search → paper generation → figure matching → formatting → iterative revision.

**Trigger Keywords**: Academic conference paper, conference call for papers, proceedings, conference submission, conference paper writing

**Core Capabilities:**
- 📄 **PDF Style Auto-Learning** —— Extract structural patterns, heading styles, sentence patterns from previous proceedings
- 💡 **Topic Recommendation** —— Generate 3–5 research topics with feasibility analysis
- 📝 **Chapter-by-Chapter Generation** —— Introduction → Theory → Core Practice → Results → Implications → Conclusion
- 📊 **Figure Matching** —— Automatically identify figure placement, generate flowcharts/bar charts/framework diagrams
- 📃 **Word Formatting Output** —— Strictly follow conference template to output formatted .docx

---

#### 2️⃣ General Academic Paper Writer
**`academic-paper-writer`**

End-to-end writing for journal papers, conference papers, and research reports across any discipline (engineering, education, social sciences, management, medicine, computer science, etc.).

**Trigger Keywords**: Academic paper writing, journal submission, paper topic selection, paper outline, literature review, SCI paper, core journal, research report, paper polishing

**Core Capabilities:**
- 🌐 **Multi-Discipline Adaptation** —— Support empirical research/method proposal/review/case study/theory building
- 🔍 **Literature Search & Review** —— Automatically generate search strategies and organize reference lists
- 📐 **Outline Design** —— Recommend structure templates based on paper type
- 📖 **Chapter-by-Chapter Generation** —— Introduction → Literature Review → Method/Mechanism → Results → Discussion → Conclusion
- 📚 **Reference Management** —— Support GB/T 7714, APA, IEEE, Vancouver formats

**Built-in References:** Paper structure templates, writing style guides, citation format manuals, default formatting specifications

---

#### 3️⃣ Educational Research Paper Assistant
**`edu-research-paper`**

Designed for K-12 and university teachers, providing full-process writing guidance for educational research papers, covering research reports, journal papers, project final reports, etc.

**Trigger Keywords**: Educational research paper, education paper, project report, final report, teaching research paper, teaching methods, lesson study, teaching cases, paper framework

**Core Capabilities:**
- 🎯 **Topic Strategy** —— Four principles (Innovation/Authenticity/Precision/Feasibility) + Three elements of title formulation
- 📋 **Structured Framework** —— Standard journal paper structure + Complete project report structure
- ✍️ **Section-by-Section Guide** —— Abstract four elements, Introduction three-paragraph structure, Literature review "shoe-selling logic"
- 📈 **Figure & Table Standards** —— Continuous numbering, caption placement, figure/table type selection guide
- ✅ **Quality Checklist** —— 15 self-check items covering common issues

---

### 🎨 Visualization & Presentation Series

#### 4️⃣ Academic PPT Generator ✨
**`academic-ppt-generator`**

Automatically generate professional academic presentation PPT from research papers/speech drafts. Supports reference PPT design DNA extraction, academic-grade chart generation (matplotlib 300DPI), diverse layout templates, Visual QA verification.

**Trigger Keywords**: Academic PPT, presentation PPT, defense PPT, paper presentation, academic report PPT, create PPT, generate PPT

**Core Capabilities:**
- 📖 **Source Document Parsing** —— Automatically extract chapter structure, core arguments, key data
- 🎨 **Design DNA Analysis** —— Extract color scheme, font system, layout patterns from reference PPT
- 📊 **Academic-Grade Charts** —— 6 types of 300 DPI professional charts (Matplotlib)
- 📐 **Diverse Layouts** —— 10 academic PPT layout templates, optimal layout selection
- ✔️ **Visual QA Verification** —— Automatically detect element overlap, page overflow, spacing anomalies
- 🔄 **Iterative Optimization** —— Automatically fix occlusion issues, support multiple rounds of adjustment

**6 Academic Chart Types:**

| Chart Type | Application Scenario | Academic Standards |
|------------|---------------------|-------------------|
| Horizontal Bar Chart + Target Reference Line | Data gap/difference demonstration | Legend + Data source footnote + Gap interval fill |
| Central Radiation Concept Framework Diagram | Theoretical framework/fusion mechanism | Bidirectional arrows + Connection label boxes + Decorative halo |
| Hierarchical Architecture Model Diagram | Practice model/system architecture | Multi-layer structure + Golden connectors + Dashed feedback |
| Three-Column Guarantee System Diagram | Guarantee mechanism/system framework | Color bar emphasis + Title header + Detail list |
| Paradigm Comparison Table | Old-new comparison/pattern transformation | Multi-dimensional horizontal comparison + Arrows + Alternating row background |
| Practice Timeline Diagram | Development history/milestones | Arrow end + Colorful nodes + Event details |

**Built-in Resources:**
- `scripts/generate_charts.py` — matplotlib academic chart generation template
- `scripts/gen_ppt_template.js` — PptxGenJS PPT generation template (with helper functions)
- `scripts/visual_qa.py` — Visual QA verification script (python-pptx detection)
- `references/layout_templates.md` — 10 academic PPT layout template references
- `references/pitfalls.md` — 18 pitfalls experience (Chinese quotes/fonts/paths, etc.)

**Tech Stack:** PptxGenJS + matplotlib + python-pptx

---

### 🔒 Intellectual Property Series

#### 5️⃣ Software Copyright Material Generator
**`project-softcopyright-generator`**

Read local project code, automatically analyze project structure, functional modules, technical architecture, generate system description document and source code document required for software copyright application.

**Trigger Keywords**: Software copyright application, software copyright, copyright registration, code document, source code document, software copyright materials, copyright registration

**Core Capabilities:**
- 🔍 **Project Scanning** —— Automatically analyze tech stack, directory structure, entry files, core modules
- 📝 **Draft Generation** —— Output software full name/short name, version, features, technical characteristics, module division suggestions
- 📋 **Code Candidate Management** —— Generate candidate list + editable selection JSON, manually confirm before generating official documents
- 📄 **Paginated Code Extraction** —— First 30 pages + last 30 pages, 60 lines per page, maintain code continuity
- 📑 **Official Document Output** —— System description document .docx + Source code document .docx + Application information .txt

**Built-in Template Scripts:** Project scanning, draft generation, code candidate management, description document generation, source code document generation, .docx rendering

---

### 🔄 Content Optimization Series

#### 6️⃣ PaperYY AIGC Rewrite
**`paperyy-aigc-rewrite`**

Systematic artificialization and deep rewriting of academic papers targeting PaperYY platform AIGC detection rules, aiming to control AIGC suspicion rate at 14%–16%.

**Trigger Keywords**: AIGC rewriting, reduce AIGC rate, remove AI traces, paper artificialization, PaperYY, AI detection, plagiarism check rewriting, paper rewriting

**Core Capabilities:**
- 🤖 **AI Feature Identification** —— Automatically locate high-risk sentence patterns
- ✍️ **Paragraph-by-Paragraph Rewriting** —— Abstract rewriting, introduction reorganization, literature review narrativization
- 🔄 **Global Replacement Rules** —— High-risk words replacement with artificial expressions
- 💾 **DOCX Format Preservation** —— Replacement script maintains original paragraph formatting, fonts, tables, images
- 🔒 **Data Security Constraints** —— Statistical numbers, p-values, references preserved as-is

---

### 🖼️ Knowledge Management Series

#### 7️⃣ Image Knowledge Extractor (General)
**`image-knowledge-extractor`**

Batch extract text from image folders (OCR), organize by user-specified categories or tags, output as Markdown reports or upload to specified note/knowledge base platforms. Supports HEIC/JPG/PNG/WEBP/GIF/BMP formats. Platforms include: IMA Knowledge Base, Notion, Obsidian directory, pure Markdown file output.

**Trigger Keywords**: Organize image knowledge, image OCR, screenshot organization, knowledge extraction, batch extract image text, screenshot to text, extract content from images

**Core Capabilities:**
- ⚡ **Multi-Process OCR Acceleration** —— RapidOCR engine supports Chinese, 4 processes processing 171 images in 25 minutes
- 🌐 **Multi-Platform Output** —— IMA Knowledge Base / Notion / Obsidian / Pure Markdown
- 🏷️ **4 Classification Modes** —— Auto-classification (11 categories) / Manual specification / Tag mode / No classification
- 📱 **HEIC Format Support** —— Complete iPhone screenshot reading
- 🔄 **Breakpoint Recovery** —— Checkpoint mechanism, support resuming after interruption

---

#### 8️⃣ Image Knowledge OCR (IMA Specialized)
**`image-knowledge-ocr`**

Batch extract text from image folders (OCR), classify and organize knowledge by content, upload to IMA Knowledge Base. Suitable for processing knowledge content in mobile screenshots/photos, batch OCR recognition of image text, classifying OCR results into knowledge notes, uploading notes to IMA "Daily" knowledge base.

**Trigger Keywords**: Organize image knowledge, image OCR, screenshot organization, knowledge extraction, IMA upload

**Core Capabilities:**
- 🗂️ **9 Knowledge Categories Auto-Classification** —— AI/Programming/Research/Open Source/Paper/Career/Network/3D Design/Video
- 📚 **IMA Knowledge Base Integration** —— import_doc API creates detailed notes (3000-5000 words/article)
- 🔗 **add_knowledge Knowledge Base Association** —— base64 format KB ID + note_info format
- 🛠️ **Common Problem Solutions** —— BOM removal, note_id inconsistency, authentication failure

---

#### 9️⃣ Image Knowledge OCR (IMA Specialized - Backup)
**`image-knowledge-ocr-ima`**

Backup version of image knowledge OCR extraction and IMA upload, functionally identical to `image-knowledge-ocr`, reserved for version management.

**Trigger Keywords**: Organize image knowledge, image OCR, screenshot organization, knowledge extraction, IMA upload

**Core Capabilities:** Same as `image-knowledge-ocr`

---

### 🔧 Utility Series

#### 🔟 Backup Skills to GitHub
**`backup-skills-to-github`**

Automatically upload original skills to this repository via GitHub REST API for version management. **Adopts incremental README update mechanism** —— only adds new skill entries each time, existing content and manually written descriptions are fully preserved.

**Trigger Keywords**: Backup skills, upload skills, sync to GitHub, backup skills, sync to github

**Core Features:**
- 🔓 **Bypass Windows git schannel issues** —— Direct upload via REST API
- 📝 **README incremental update** —— Only append new entries each time, don't overwrite existing content
- ⚙️ **Flexible options** —— Support `--all` full scan and `--skill` specified upload

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.x (Recommended: 3.13+)
- **Node.js**: 22.x (For PPT generation features)
- **Git**: For cloning the repository

### 5-Minute Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/FooFieYoon/scholar-forge.git ~/scholar-forge/

# 2. Choose your AI platform
# Option A: CodeBuddy
#   Go to "Settings → Skills Management → Install from Folder", select ~/scholar-forge/skills/

# Option B: Cursor
#   Copy SKILL.md content to project root .cursorrules,
#   or put entire skills/ directory into project's .cursor/instructions/

# Option C: Claude Code
#   Put SKILL.md content into CLAUDE.md file (project level)
#   or import via /add-instructions

# 3. Start using
#   Trigger the skill with keywords (see each skill's "Trigger Keywords" section)
```

---

## 📦 Installation

### Method 1: Clone via Git (Recommended)

```bash
git clone https://github.com/FooFieYoon/scholar-forge.git
cd scholar-forge
```

### Method 2: Download ZIP

1. Visit [GitHub Repository](https://github.com/FooFieYoon/scholar-forge)
2. Click "Code" → "Download ZIP"
3. Extract to your desired location

### Method 3: Install Specific Skills

Each skill is independent. You can install only the skills you need:

```bash
# Example: Install only academic-paper-writer
cp -r scholar-forge/skills/academic-paper-writer ~/my-skills/
```

---

## 📖 Usage Guide

### Platform Compatibility

Skills in this repository use Markdown + YAML frontmatter format (SKILL.md), compatible with the following mainstream AI platforms:

| Platform | Installation Method |
|----------|---------------------|
| **CodeBuddy** | "Settings → Skills Management → Install from Folder", select corresponding skill sub-directory |
| **Cursor** | Copy SKILL.md content to project root `.cursorrules`, or put entire `skills/` directory into project's `.cursor/instructions/` |
| **Claude Code** | Put SKILL.md content into `CLAUDE.md` file (project level) or import via `/add-instructions` |
| **GitHub Copilot** | Paste SKILL.md content to `.github/copilot-instructions.md` |
| **Windsurf** | Write SKILL.md content to `.windsurfrules` |
| **ChatGPT Projects** | Paste core instruction part of SKILL.md in ChatGPT's "Custom Instructions" or Project settings |
| **Generic AI Chat** | Directly paste content after `---` separator in SKILL.md as system prompt |

### Typical Workflow

```
1. Select Skill → 2. Import to AI Platform → 3. Trigger with Keywords → 4. Provide Input Materials → 5. AI Generates Output
```

### Example: Using Academic Paper Writer

```
User: "I need to write a paper about deep learning in education, can you help me?"

AI: [Automatically loads academic-paper-writer skill]
    "I'll help you write this paper. Let me start by recommending some topics based on current research trends..."
    
    [Generates topic recommendations]
    [Creates paper outline]
    [Generates content chapter by chapter]
    [Formats references]
    [Outputs .docx file]
```

---

## 🏗️ Technical Stack

### Core Technologies

```
┌─────────────────────────────────────────────────┐
│              ScholarForge Ecosystem             │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐      ┌──────────────┐       │
│  │   SKILL.md   │──────│  AI Platform │       │
│  │  (Markdown)  │      │  (CodeBuddy) │       │
│  └──────────────┘      └──────────────┘       │
│         │                                       │
│         ↓                                       │
│  ┌──────────────┐      ┌──────────────┐       │
│  │  Python 3.x  │──────│  Node.js 22  │       │
│  │  (Backend)   │      │   (Frontend) │       │
│  └──────────────┘      └──────────────┘       │
│         │                                       │
│         ↓                                       │
│  ┌──────────────────────────────────┐          │
│  │    Output Formats                │          │
│  │  .docx  .pptx  .png  .txt  .md │          │
│  └──────────────────────────────────┘          │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Dependencies

<details>
<summary><b>Python Dependencies (Click to expand)</b></summary>

```txt
python-docx>=0.8.11     # Word document generation
matplotlib>=3.5.0       # Academic chart generation
python-pptx>=0.6.21     # PowerPoint generation
rapidocr>=1.0.0         # OCR processing
Pillow>=9.0.0           # Image processing
pandas>=1.3.0           # Data processing
numpy>=1.21.0           # Numerical computation
```

</details>

<details>
<summary><b>Node.js Dependencies (Click to expand)</b></summary>

```txt
pptxgenjs>=3.12.0      # PPT generation
```

</details>

---

## 📂 Project Structure

```
scholar-forge/
├── skills/                                   # Skill packages directory
│   ├── academic-conference-paper-writer/      # Academic conference paper writing
│   ├── academic-paper-writer/                 # General academic paper writing
│   │   └── references/                        #   Structure/citation/style references
│   ├── academic-ppt-generator/                # Academic PPT generator
│   │   ├── scripts/                           #   Chart/PPT/QA scripts
│   │   └── references/                        #   Layout templates + Pitfalls
│   ├── edu-research-paper/                    # Educational research paper
│   ├── paperyy-aigc-rewrite/                  # AIGC detection rewrite
│   │   ├── references/                        #   Detection rules + Rewrite examples
│   │   └── scripts/                           #   docx paragraph replacement script
│   ├── project-softcopyright-generator/        # Software copyright material generation
│   │   ├── templates/                         #   6 pipeline template scripts
│   │   └── references/                        #   Application field specifications + Design specifications
│   ├── image-knowledge-extractor/               # Image knowledge extraction (general)
│   │   └── references/                          #   Multi-platform API references
│   ├── image-knowledge-ocr/                     # Image knowledge OCR (IMA specialized)
│   │   └── references/                          #   IMA OpenAPI reference
│   ├── image-knowledge-ocr-ima/                 # Image knowledge OCR (IMA specialized - backup)
│   │   └── references/                          #   IMA OpenAPI reference
│   └── backup-skills-to-github/               # Skill backup & sync
│       └── scripts/                           #   Scan/upload/organize scripts
├── docs/                                      # Documentation directory
│   └── tools-guide.md                         #   Tool configuration guide
├── .gitignore
├── LICENSE
└── README.md                                  # This file
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: Open an issue describing the bug
- 💡 **Suggest Features**: Propose new skills or improvements
- 📝 **Improve Documentation**: Fix typos, add examples, clarify instructions
- 🔧 **Submit Pull Requests**: Fix bugs, add features, improve code quality
- ⭐ **Star the Repo**: Show your support!

### Development Workflow

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Commit your changes
git commit -m 'Add some AmazingFeature'

# 4. Push to the branch
git push origin feature/AmazingFeature

# 5. Open a Pull Request
```

### Skill Development Guidelines

When creating a new skill, please follow these guidelines:

1. **File Naming**: Use kebab-case (e.g., `academic-paper-writer`)
2. **SKILL.md Format**: Include YAML frontmatter + Markdown instructions
3. **Documentation**: Add detailed README in skill directory
4. **Testing**: Test your skill on at least 2 AI platforms
5. **Examples**: Provide example inputs and expected outputs

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

---

## 📧 Contact

- **Maintainer**: Yin
- **GitHub Issues**: [Open an Issue](https://github.com/FooFieYoon/scholar-forge/issues)
- **Repository**: [https://github.com/FooFieYoon/scholar-forge](https://github.com/FooFieYoon/scholar-forge)

---

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Special thanks to the open-source community for providing excellent tools and libraries
- Inspired by the need for better academic writing tools in the AI era

---

## 📌 Citation

If you use ScholarForge in your research or project, please cite:

```bibtex
@software{scholarforge2026,
  author = {Yin},
  title = {ScholarForge: AI-Powered Academic Writing & IP Tools Collection},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/FooFieYoon/scholar-forge}
}
```

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [Yin](https://github.com/FooFieYoon)

</div>
