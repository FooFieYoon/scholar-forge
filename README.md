# ScholarForge / 学术匠心工坊

> AI 驱动的学术写作与知识产权工具集 —— 从选题到成稿，从代码到软著，从讲稿到汇报。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-7-blue)](skills/)

---

## 简介

ScholarForge（学术匠心工坊）是一套面向研究人员、教师和开发者的 AI 技能合集，覆盖学术论文全流程写作、AIGC 检测降重改写、学术汇报PPT制作，以及软件著作权登记材料自动生成。

所有技能均为 Markdown 格式的指令文件（SKILL.md），可导入到支持自定义指令的主流 AI 编程平台使用。

---

## 仓库结构

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
│   └── backup-skills-to-github/               # 技能备份同步
│       └── scripts/                           #   扫描/上传/整理脚本
└── docs/                                      # 文档目录
    └── tools-guide.md                         #   工具配置指南
```

---

## 技能一览

### 1. 学术年会论文写作助手
**`academic-conference-paper-writer`**

基于目标报告文集的风格规范（自动分析 PDF 样本），从会议通知材料出发，全流程完成选题推荐、资料搜索、论文生成、图表匹配、排版输出到迭代修改。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 学术年会论文、会议征文、报告文集、年会投稿、会议论文写作 | 提供学术年会通知或往届论文集，需要撰写符合该会议风格的高质量学术报告 |

**核心能力：**
- PDF 风格自动学习 —— 从往届文集中提取结构模式、标题体例、句式特征
- 选题推荐 —— 综合分析政策/期刊/案例，生成 3–5 个选题并标注可行支撑
- 逐章生成 —— 引言→理论→核心实践→成效→启示→结论
- 图表匹配 —— 自动识别配图位置，生成流程图/柱状图/框架图
- Word 排版输出 —— 严格按会议模板输出格式化 .docx

---

### 2. 通用学术论文写作助手
**`academic-paper-writer`**

支持任意学科领域（工程、教育、社科、管理、医学、计算机等）的期刊论文、会议论文、研究报告端到端写作。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 学术论文写作、期刊投稿、论文选题、论文大纲、文献综述、SCI 论文、核心期刊、研究报告、论文润色 | 提供投稿通知或选题，需要从选题到成稿的完整写作流程支持 |

**核心能力：**
- 多学科适配 —— 支持实证研究/方法提出/综述/案例研究/理论构建等多种论文类型
- 文献检索与综述 —— 自动生成文献检索策略并整理资料清单
- 大纲设计 —— 根据论文类型推荐对应结构模板
- 逐章生成 —— 引言→文献综述→方法/机制→结果/成效→讨论→结论
- 参考文献管理 —— 支持 GB/T 7714、APA、IEEE、Vancouver 等多种格式

**内置参考文档：** 论文结构模板、写作风格指南、引文格式手册、默认排版规范

---

### 3. 教学科研论文撰写辅助
**`edu-research-paper`**

面向中小学及高校教师，专注教育科研论文的全流程写作指导，覆盖课题研究报告、期刊投稿论文、结题报告等常见类型。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 教学科研论文、教育论文、课题报告、结题报告、教研论文、教学方法、课例研究、教学案例、论文框架 | 教师需要撰写教育类论文，从选题策略到各章节规范的全流程指导 |

**核心能力：**
- 选题策略 —— 四大选题原则（创新性/真实性/切口精准/可行性）+ 题目拟定三要素
- 结构化框架 —— 期刊论文标准结构、课题结题报告完整结构
- 逐节撰写指南 —— 摘要四要素、引言三段式、文献综述"卖鞋逻辑"、研究设计方法选用
- 图表规范 —— 全文连续编号、图题表题位置、先文后图表原则、图表类型选用指南
- 质量检查清单 —— 15 条自查项覆盖全篇常见问题

---

### 4. AIGC 检测降重改写
**`paperyy-aigc-rewrite`**

针对 PaperYY 平台 AIGC 检测规则，对学术论文进行系统性人工化深度改写，目标将 AIGC 疑似率控制在 14%–16%。

| 触发关键词 | 适用场景 |
|-----------|---------|
| AIGC 降重、降 AIGC 率、去 AI 痕迹、论文人工化、PaperYY、人工智能检测、查重降重、论文改写 | 提供 .docx 论文文件，需要降低 AIGC 检测疑似率 |

**核心能力：**
- AI 特征识别 —— 自动定位政策引用开篇、演进叙事、"一方面…另一方面…"、"研究表明"等高风险句式
- 逐段改写 —— 摘要改写、引言重组、文献综述叙事化、结果分析去模板化、结论自然收尾
- 全局替换规则 —— 高风险词（深度融合/赋能/重构/路径优化→人工化替代表达）
- docx 格式保留 —— 替换脚本保持原文段落格式、字体、字号、表格、图片不变
- 数据安全约束 —— 统计数字、p 值、参考文献、标题层级、专业术语原样保留

---

### 5. 软件著作权材料生成器
**`project-softcopyright-generator`**

读取本地项目代码，自动分析项目结构、功能模块、技术架构，生成软著申请所需的系统说明文档与源代码文档。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 软著申请、软件著作权、著作权登记、代码文档、源码文档、软著材料、版权登记 | 已有本地项目代码，需要整理软著申请资料 |

**核心能力：**
- 项目扫描 —— 自动分析技术栈、目录结构、入口文件、核心模块
- 建议稿生成 —— 输出软件全称/简称/版本/功能/技术特点/模块划分建议
- 代码候选管理 —— 生成候选清单 + 可编辑选择 JSON，人工确认后生成正式文档
- 分页代码抽取 —— 前 30 页 + 后 30 页，每页 60 行，保持代码连续性
- 正式文档输出 —— 系统说明文档 .docx + 源代码文档 .docx + 申请信息 .txt

**内置模板脚本：** 项目扫描、建议稿生成、代码候选管理、说明文档生成、源代码文档生成、.docx 渲染

---

### 6. 学术汇报PPT生成器 ✨ NEW
**`academic-ppt-generator`**

从学术论文/发言稿出发，自动生成专业学术汇报PPT。支持参考PPT设计DNA提取、学术级图表绘制（matplotlib 300DPI）、多样化布局排版、Visual QA验证，实现"讲稿→PPT"的一键转换。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 学术PPT、汇报PPT、答辩PPT、论文汇报、学术报告PPT、制作PPT、生成PPT | 提供论文/发言稿，需要制作符合学术规范的高质量汇报PPT |

**核心能力：**
- 源文档解析 —— 自动提取发言稿/论文的章节结构、核心论点、关键数据
- 参考PPT设计DNA分析 —— 提取目标PPT的配色方案、字号体系、布局模式、设计元素
- 学术级图表生成 —— matplotlib 300DPI，6种专业图表类型（柱状图/框架图/架构图/保障图/对比图/时间线）
- 多样化布局排版 —— 10种学术PPT布局模板，每页根据内容类型选择最佳布局
- Visual QA验证 —— python-pptx自动检测元素遮挡、页面溢出、间距异常
- 迭代优化 —— 自动修复遮挡问题，支持多轮调整

**6种学术图表类型：**

| 图表类型 | 适用场景 | 学术规范 |
|---------|---------|---------|
| 水平柱状图+目标参考线 | 数据缺口/差距展示 | 图例+数据来源脚注+差距区间填充 |
| 中心辐射式概念框架图 | 理论框架/融合机制 | 双向箭头+连接标签框+装饰光环 |
| 层次架构模型图 | 实践模型/体系架构 | 多层结构+金色连线+虚线反馈 |
| 三柱保障体系图 | 保障机制/制度体系 | 色条强调+标题头+详情列表 |
| 范式对比表图 | 新旧对比/模式转型 | 多维度横向对比+箭头+交替行背景 |
| 实践时间线图 | 发展历程/里程碑 | 箭头末端+彩色节点+事件详情 |

**内置资源：**
- `scripts/generate_charts.py` — matplotlib 学术图表生成模板
- `scripts/gen_ppt_template.js` — PptxGenJS PPT 生成模板（含辅助函数）
- `scripts/visual_qa.py` — Visual QA 验证脚本（python-pptx 检测遮挡/溢出）
- `references/layout_templates.md` — 10 种学术 PPT 布局模板参考
- `references/pitfalls.md` — 18 条踩坑经验（中文引号/字体/路径等）

**技术栈：** PptxGenJS + matplotlib + python-pptx

---

### 7. 技能备份同步
**`backup-skills-to-github`**

将原创技能通过 GitHub REST API 自动上传到本仓库进行版本管理。**采用增量 README 更新机制**——每次只添加新技能条目，已有内容和手动撰写的说明完全保留。

| 触发关键词 | 适用场景 |
|-----------|---------|
| 备份技能、上传技能、同步到 GitHub、backup skills、sync to github | 需要将本地技能同步到远程仓库进行版本管理或分享 |

**核心特性：**
- 绕过 Windows git schannel 问题，通过 REST API 直接上传
- README 增量更新：每次只追加新条目，不覆盖已有内容
- 支持 `--all` 全量扫描和 `--skill` 指定上传

---

## 使用方法

### 平台兼容性

本仓库中的技能采用 Markdown + YAML frontmatter 格式（SKILL.md），兼容以下主流 AI 平台：

| 平台 | 使用方式 |
|------|---------|
| **CodeBuddy** | 「设置 → Skills 管理 → 从文件夹安装」，选择对应 skill 子目录 |
| **Cursor** | 将 `SKILL.md` 内容复制到项目根目录 `.cursorrules` 中，或将整个 `skills/` 目录放入项目的 `.cursor/instructions/` |
| **Claude Code** | 将 `SKILL.md` 内容放入 `CLAUDE.md` 文件（项目级）或通过 `/add-instructions` 导入 |
| **GitHub Copilot** | 将 `SKILL.md` 内容粘贴到 `.github/copilot-instructions.md` |
| **Windsurf** | 将 `SKILL.md` 内容写入 `.windsurfrules` |
| **ChatGPT Projects** | 在 ChatGPT 的「自定义指令」或 Project 设置中粘贴 `SKILL.md` 的核心指令部分 |
| **通用 AI 对话** | 将 `SKILL.md` 中 `---` 分隔线之后的内容作为系统提示词直接粘贴使用 |

### 快速导入（CodeBuddy）

```bash
git clone https://github.com/FooFieYoon/scholar-forge.git ~/scholar-forge/
# 然后在 CodeBuddy 设置中选择「从文件夹安装」，定位到 ~/scholar-forge/skills/
```

### 手动使用

1. 浏览 [skills/](skills/) 目录，找到你需要的技能
2. 打开对应的 `SKILL.md` 文件，阅读技能说明和触发关键词
3. 根据你使用的 AI 平台，按上表方式导入
4. 部分技能包含 `scripts/` 和 `templates/` 子目录，导入时请保持目录结构完整

### 跨平台迁移注意事项

部分技能包含 Python/Node.js 脚本，迁移到其他平台时需：

1. 复制完整的 skill 目录（包含 `scripts/`、`templates/`、`references/` 子目录）
2. 确保目标环境已安装 Python 3.x 及所需依赖（`python-docx`、`matplotlib` 等）
3. PPT 生成技能需额外安装 Node.js 及 `pptxgenjs` 依赖
4. 各技能的具体依赖见对应 `SKILL.md` 中的工具速查表

详细配置指南参见 [`docs/tools-guide.md`](docs/tools-guide.md)。

---

## 技术说明

- **语言**：所有技能以简体中文为核心工作语言
- **格式**：SKILL.md（Markdown + YAML frontmatter）
- **脚本依赖**：Python 3.x + Node.js 22.x（部分技能需要 `python-docx`、`matplotlib`、`pptxgenjs` 等库）
- **文档输出**：.docx（Word）、.pptx（PowerPoint）、.png（图表）、.txt、.md

---

## 更新日志

### 2026-06-02
- ✨ 新增 `academic-ppt-generator` 学术汇报PPT生成器
  - 6种学术级图表类型（matplotlib 300DPI）
  - 10种多样化布局模板
  - Visual QA 自动验证
  - 18条踩坑经验文档
  - 完整的 PptxGenJS + python-pptx 脚本模板

### 2026-05-30
- 🔧 新增 `backup-skills-to-github` 技能备份同步工具

### 2026-05-28
- 🔧 新增 `project-softcopyright-generator` 软著材料生成器

### 2026-05-25
- 🔧 新增 `paperyy-aigc-rewrite` AIGC 检测降重改写

### 2026-05-20
- 🔧 新增 `edu-research-paper` 教学科研论文撰写辅助

### 2026-05-15
- 🎉 初始版本发布
- 🔧 新增 `academic-conference-paper-writer` 学术年会论文写作助手
- 🔧 新增 `academic-paper-writer` 通用学术论文写作助手

---

## 维护者

**Yin** — 所有技能由 AI Agent 创建，Yin 负责维护与迭代。

---

## 许可证

[MIT License](LICENSE)

---

## 相关链接

- 仓库地址：[github.com/FooFieYoon/scholar-forge](https://github.com/FooFieYoon/scholar-forge)
- 问题反馈：[GitHub Issues](https://github.com/FooFieYoon/scholar-forge/issues)

---

*Made with ❤️ by Yin*
