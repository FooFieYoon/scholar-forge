# WorkBuddy Skills Backup

本仓库备份 WorkBuddy AI 助手的**原创 Skills**（`agent_created: true`），可直接导入使用。

## 包含的 Skills

| Skill 名称 | 功能说明 | 触发词示例 |
|---|---|---|
| `academic-conference-paper-writer` | 学术年会论文全流程写作助手 | "写一篇学术会议论文" |
| `academic-paper-writer` | 通用学术论文全流程写作助手 | "帮我写论文" |
| `edu-research-paper` | 教学科研论文撰写辅助 | "写教学科研论文" |
| `paperyy-aigc-rewrite` | PaperYY AIGC 检测降重改写工具 | "降低 AIGC 检测率" |
| `backup-skills-to-github` | 备份 Skills 到 GitHub（本仓库） | "备份我的 skills" |

## 仓库结构

```
workbuddy-skills/
├── README.md
└── skills/
    ├── academic-conference-paper-writer/
    ├── academic-paper-writer/
    ├── edu-research-paper/
    ├── paperyy-aigc-rewrite/
    └── backup-skills-to-github/
        ├── SKILL.md
        ├── scripts/
        └── references/
```

## 安装方法

将需要的 skill 目录复制到 WorkBuddy 的 skills 目录：

```bash
# 用户级安装（所有项目可用）
cp -r skills/<skill-name> ~/.workbuddy/skills/

# 项目级安装（仅当前项目）
cp -r skills/<skill-name> <project-root>/.workbuddy/skills/
```

安装后重启 WorkBuddy 即可使用。

## 每个 Skill 的结构

```
skills/
└── <skill-name>/
    ├── SKILL.md          # 核心文件，定义 skill 的触发词、工作流程
    ├── references/       # 参考资料（可选）
    ├── scripts/          # 辅助脚本（可选）
    └── assets/          # 资源文件（可选）
```

## 使用 `backup-skills-to-github` Skill

安装 `backup-skills-to-github` skill 后，直接对 WorkBuddy 说：

> "备份我的 skills 到 github"

它会自动：
1. 扫描所有 `agent_created: true` 的原创 skill
2. 检查 GitHub 认证状态
3. 创建或确认 `workbuddy-skills` 仓库
4. 通过 REST API 上传所有文件（绕过 Windows git 问题）
5. 优化仓库目录结构（`skills/` 子目录）
6. 更新 README.md

## 关于 WorkBuddy

WorkBuddy 是一个强大的 AI 编程助手，支持通过 Skills 扩展能力。每个 Skill 是一个独立的能力模块，包含触发条件、工作流程和参考资料。

- 官网：https://www.workbuddy.ai
- Skills 文档：https://www.workbuddy.ai/docs/skills

## 贡献

这些是原创 Skill，如果你有改进建议，欢迎提 Issue 或 PR。

---
*由 WorkBuddy 自动备份 · 最后更新：2026-05-30*
