---
name: backup-skills-to-github
author: Yin
description: "备份原创 Skills 到 GitHub ScholarForge 仓库。当用户说"备份 skills"、"备份 skill"、"上传 skills 到 github"、"backup my skills"、"sync skills to github"时触发。自动扫描 agent_created 的原创 skill，通过 API 上传所有文件，README 增量更新（只添加新条目不覆盖已有内容）。"
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
2. Base64 编码内容
3. 通过 `gh api --method PUT` 上传到仓库
4. 如果文件已存在则更新（带 SHA）
5. **增量更新 README.md**：读取现有 README → 解析已有 skill 列表 → 仅追加新条目

### 第四步（可选）：优化仓库结构

上传完成后，若需整理目录结构，运行：

```bash
python3 scripts/optimize_layout.py FooFieYoon/scholar-forge
```

将散落在根目录的 skill 移动到 `skills/` 子目录，同样采用增量 README 更新。

## README 增量更新机制

这是本技能最重要的设计原则：

```
已有 README 内容（手动撰写 + 历史自动生成）
    ↓ 读取
解析现有 skill 表格 → 提取已有 skill 名称集合
    ↓ 对比
本次上传的 skills 中哪些不在已有集合中
    ↓ 追加
只在表格末尾追加新条目，其余内容完全不触碰
```

**不会做的事**：全量重写 README、覆盖手动撰写的说明文字、重新排序已有条目。

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
