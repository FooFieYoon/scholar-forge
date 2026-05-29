# WorkBuddy Skills 备份仓库

> **作者：Yin**  
> 本仓库由 Yin 维护，存放 WorkBuddy AI 助手的原创 Skills（`agent_created: true`）。

---

## 关于作者

- **Author**: Yin
- **GitHub**: [@FooFieYoon](https://github.com/FooFieYoon)
- **说明**: 本仓库中的所有 Skills 均由 Yin 原创编写，`agent_created: true` 标识表明这些 Skills 由 AI Agent 在 Yin 的指导下自动创建和维护。

---

## 包含的 Skills

| Skill 名称 | 功能说明 | 适用场景 |
|---|---|---|
| `academic-conference-paper-writer` | 学术年会论文全流程写作助手 | 年会报告、会议论文 |
| `academic-paper-writer` | 通用学术论文全流程写作助手 | 期刊论文、学位论文 |
| `edu-research-paper` | 教学科研论文撰写辅助 | 教育科研论文、结题报告 |
| `paperyy-aigc-rewrite` | PaperYY AIGC 检测降重改写工具 | AIGC 率降低、论文人工化改写 |
| `backup-skills-to-github` | 备份 Skills 到 GitHub（通用型 Skill） | "备份我的 skills" |

---

## 仓库目录结构

```
workbuddy-skills/
├── README.md          ← 本文件
└── skills/            ← 所有 Skill 存放目录
    ├── academic-conference-paper-writer/
    ├── academic-paper-writer/
    ├── edu-research-paper/
    ├── paperyy-aigc-rewrite/
    └── backup-skills-to-github/
        ├── SKILL.md
        ├── scripts/
        └── references/
```

---

## 安装方法

将需要的 Skill 目录复制到 WorkBuddy 的 Skills 目录：

```bash
# 用户级安装（所有项目可用）
cp -r skills/<skill-name> ~/.workbuddy/skills/

# 项目级安装（仅当前项目）
cp -r skills/<skill-name> <project-root>/.workbuddy/skills/
```

安装后重启 WorkBuddy 即可使用。

---

## 每个 Skill 的结构

```
skills/
└── <skill-name>/
    ├── SKILL.md          # 核心文件，定义 Skill 的触发词、工作流程
    ├── references/       # 参考资料（可选）
    ├── scripts/          # 辅助脚本（可选）
    └── assets/          # 资源文件（可选）
```

---

## 触发示例

| 用户说 | 触发 Skill |
|---|---|
| "写一篇学术会议论文" | `academic-conference-paper-writer` |
| "帮我写论文" | `academic-paper-writer` |
| "写教学科研论文" | `edu-research-paper` |
| "降低 AIGC 检测率" | `paperyy-aigc-rewrite` |
| "备份我的 skills 到 github" | `backup-skills-to-github` |

---

## 关于 WorkBuddy

WorkBuddy 是一个强大的 AI 编程助手，支持通过 Skills 扩展能力。每个 Skill 是一个独立的能力模块，包含触发条件、工作流程和参考资料。

- 官网：https://www.workbuddy.ai
- Skills 文档：https://www.workbuddy.ai/docs/skills

---

## `backup-skills-to-github` Skill 使用说明

该 Skill 由 Yin 原创，用于自动备份 WorkBuddy 原创 Skills 到 GitHub。

**触发词**："备份我的 skills"、"上传 skills 到 github"、"backup my skills"

**工作流程**：
1. 扫描本地 `~/.workbuddy/skills/` 中所有 `agent_created: true` 的原创 Skill
2. 检查 GitHub 认证状态，必要时引导用户登录
3. 创建或更新 `workbuddy-skills` 仓库
4. 通过 GitHub REST API 上传所有文件（绕过 Windows git 问题）
5. 优化仓库目录结构（使用 `skills/` 子目录）
6. 自动生成并更新 README.md

---

## 版权与许可

- **作者**: Yin
- **Copyright**: © 2026 Yin. All rights reserved.
- **License**: MIT License（允许自由使用、修改和分发）
- **说明**: 本仓库中的 Skills 为原创作品，欢迎学习和改进，请注明出处。

---

## 贡献

欢迎提交 Issue 或 Pull Request 改进这些 Skills。

---

*由 Yin 维护 · 最后更新：2026-05-30*
