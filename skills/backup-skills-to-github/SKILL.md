---
name: backup-skills-to-github
author: Yin
agent_created: true
description: >
  备份原创 Skills 到 GitHub ScholarForge 仓库。当用户说“备份 skills”“备份 skill”
  “上传 skills 到 GitHub”“backup my skills”或“sync skills to GitHub”时触发。
  自动扫描 agent_created 的原创 skill，通过 API 上传全部必要文件，并以增量方式更新 README。
---

# Backup Skills to GitHub

将原创 Skills（`agent_created: true`）备份到 GitHub ScholarForge 仓库。

**核心原则：README 增量更新** — 每次备份只添加新 skill 条目到仓库 README，已有内容和手动撰写的部分完全保留不动。

## 触发条件

- 用户说"备份我的 skills"、"备份 skill"
- 用户说"上传 skills 到 github"、"sync to github"
- 用户说"把我的 skills 推送到远程仓库"

## 工作流程

### 第一步：扫描原创 Skills

运行 `scripts/scan_skills.py` 扫描 `~/.workbuddy/skills/` 目录，找出所有 `agent_created: true` 的 skill：

```bash
python3 scripts/scan_skills.py
```

### 第二步：检查 GitHub 认证

```bash
gh auth status
```

未登录时提示用户在终端运行 `gh auth login --web --hostname github.com` 完成授权。

### 第三步：上传文件

使用 `scripts/backup_skills.py` 通过 GitHub REST API 上传文件（绕过 git clone 的 Windows schannel 问题）：

```bash
# 上传所有原创 skill（推荐）
python3 scripts/backup_skills.py FooFieYoon/scholar-forge --all

# 上传指定 skill
python3 scripts/backup_skills.py FooFieYoon/scholar-forge --skill project-softcopyright-generator
```

脚本自动完成：
1. 读取所有原创 skill 文件
2. 自动跳过 `.env`、`__pycache__`、`.pyc`、日志和临时文件
3. Base64 编码内容
4. 通过 GitHub REST API 上传到仓库
5. 如果文件已存在则更新（带 SHA）
6. **增量更新 README.md**：读取现有 README → 解析已有 skill 列表 → 仅追加新条目

### 第四步（可选）：优化仓库结构

上传完成后，若需整理目录结构，运行：

```bash
python3 scripts/optimize_layout.py FooFieYoon/scholar-forge
```

将散落在根目录的 skill 移动到 `skills/` 子目录，同样采用增量 README 更新。

### 第五步（用户要求更新介绍页时）：整合 README 正文

增量同步只保证新技能不会遗漏，不负责维护完整介绍页。若用户同时要求“更新 GitHub 介绍页/README 内容”，应在上传完成后：

1. 重新 GET 最新 `README.md` 与 SHA，不能基于上传前的旧副本修改。
2. 更新 Skills 数量徽章、项目简介、技能详细介绍、项目结构和更新日志；中英双语 README 要同步修改。
3. 若增量同步在文件末尾生成 `## 包含的 Skills` 汇总表，而新技能已并入正文详细目录，应删除该临时汇总表，避免重复。
4. 修正其他已过期说明（例如模型版本、失效接口），但保留手工撰写的历史内容。
5. 通过 Contents API 携带当前 SHA 上传，再复查远程技能目录、README 技能名集合、数量徽章与最新提交。

## README 增量更新机制

这是本技能最重要的设计原则：

```
已有 README 内容（手动撰写 + 历史自动生成）
    ↓ 读取
扫描所有格式的已有 skill（表格行 | `xxx` | + 加粗标题行 **`xxx`**）
    ↓ 对比
本次上传的 skills 中哪些不在已有集合中
    ↓ 追加
只在文件末尾的 "## 包含的 Skills" 汇总表格中追加新条目
```

**关键修复（2026-09-27）**：

- `backup-skills-to-github` 本身纳入 `agent_created: true` 扫描范围，可同步自身更新。
- `scan_skills.py` 支持 YAML `>` / `|` 多行 description，不再把说明误读为单个符号。
- 上传器过滤缓存目录、Python 字节码、日志和临时文件，避免污染远程仓库。
- 补充“完整介绍页更新”分支：增量同步后再维护中英双语正文、数量、目录树和更新日志。

**关键修复（2026-08-18）**：

| 旧行为（有 bug） | 新行为（已修复） |
|---|---|
| 只匹配 `| \`xxx\` |` 表格行 | 同时匹配 `| \`xxx\` |` + `**\`xxx\`**` 加粗标题 |
| 找不到表格行时 fallback 到正文末尾追加 | 只在文件末尾的 `## 包含的 Skills` 汇总表追加 |
| 每次运行都在 EOF 创建新表格，导致重复 | 只在已有汇总表内增量追加行，不重复创建 |
| 在正文中插入行（破坏结构） | 只操作 EOF 的汇总表格，正文完全不受影响 |

**不会做的事**：全量重写 README、覆盖手动撰写的说明文字、重新排序已有条目、在正文中插入内容。

## 文件说明

| 文件 | 用途 |
|---|---|
| `scripts/scan_skills.py` | 扫描并列出所有原创 skill |
| `scripts/backup_skills.py` | 通过 API 上传文件 + 增量更新 README |
| `scripts/optimize_layout.py` | 整理仓库目录结构 + 增量更新 README |
| `references/github_api_notes.md` | GitHub REST API 使用要点 |

## 注意事项

- **README 增量模式**：不会覆盖已有内容，每次只追加新 skill
- **不要在 `/tmp` 写临时文件**，Windows 沙箱会拦截 —— 改用项目目录或直接使用内存
- **不要依赖 git clone/push**，Windows schannel 证书吊销检查会失败 —— 始终用 GitHub REST API
- **`gh api` 上传大文件前先检查是否已存在**（GET 获取 SHA，再 PUT 更新）
- 目标仓库：`FooFieYoon/scholar-forge`（ScholarForge / 学术匠心工坊）

## 一键运行

```bash
python3 scripts/backup_skills.py FooFieYoon/scholar-forge --all
```
