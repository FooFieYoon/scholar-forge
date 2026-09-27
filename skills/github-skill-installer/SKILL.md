---
name: github-skill-installer
description: >
  从 GitHub 仓库批量安装第三方 skill 到 WorkBuddy 用户技能目录的完整工作流。当用户说"安装/搜索某个
  GitHub 仓库里的 skill""把这个仓库的 skills 装上"时触发。覆盖：仓库获取（沙箱网络受限时走 ghfast.top
  加速镜像）、完整目录解压、安全审计扫描（P0/P1 风险判定）、整目录安装到 ~/.workbuddy/skills/、
  安装后校验与临时文件清理。
agent_created: true
author: WorkBuddy
---

# GitHub Skill 批量安装器

## 何时使用

用户给出一个 GitHub 仓库地址，要求安装其中的 skill（可能是单个，也可能是整个 `skills/` 目录）。

## 步骤

### 1. 确认仓库可达

```bash
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
git ls-remote https://github.com/<owner>/<repo> | head
```

本机沙箱内 `git clone` 常报 `CONNECT tunnel failed, response 502`；`github.com`、`api.github.com`、
`raw.githubusercontent.com`、`cdn.jsdelivr.net` 均不可达。**不要在此浪费超过 2 次尝试**，直接走第 2 步。

### 2. 走镜像下载整包（关键）

```bash
curl -sL --max-time 280 -o repo.zip --retry 3 --retry-all-errors \
  "https://ghfast.top/https://github.com/<owner>/<repo>/archive/refs/heads/main.zip"
```

- 直连 `codeload.github.com` 会在 4—12MB 随机截断，且**不支持 Range**，`curl -C -` 续传无效。
- 可用镜像：`ghfast.top`（已验证可下 35MB 完整包）、`ghproxy.net`、`gh-proxy.com`。
- 镜像前缀拼文件名时**不要**用 `tr -dc 'a-z' | cut -c1-6`，多个镜像会撞名互相覆盖。

### 3. 校验完整性 + 列目录

用 Write 写 `.py` 脚本再执行（**不要用 heredoc**，本机 shell 包装会解析异常）：

```python
import zipfile
z = zipfile.ZipFile('repo.zip')
assert z.testzip() is None          # 必须为 None 才算完整
P = '<repo>-main/skills/'            # 镜像包顶层目录名仍是 <repo>-main
skills = sorted({x[len(P):].split('/')[0] for x in z.namelist()
                 if x.startswith(P) and x != P})
```

### 4. 安全审计（必做，不可跳过）

本机没有 `skills-security-check` 技能，自写扫描脚本，对全部文本文件（.md/.py/.sh/.ps1/.js/.json/.yaml/.toml）
匹配以下模式并逐条人工判读：

| 类别 | 判定 |
| --- | --- |
| `(curl\|wget) ... \| sh` | **P0**，管道直连执行，拒绝安装 |
| `eval(` / `exec(` / `os.system(` | **P0**，需看上下文 |
| `rm -rf` / `shutil.rmtree` | P1，确认目标是否仅为自身临时目录 |
| 注册表、启动项、计划任务、crontab | **P0** |
| 凭据文件读取（`~/.ssh`、`.aws`、浏览器 cookie） | **P0** |
| base64 解码后执行 | **P0** |
| `subprocess` 调用本地工具（libreoffice/convert） | 正常 |
| `urllib`/`requests` 访问公开 API | 正常，属技能功能 |
| 用户自行输入的 API key 存本地 | 正常，需告知存放位置 |

结论必须向用户给出：**P0 遇阻并强警告 / P1 警告后确认 / P2 直接安装**。

### 5. 整目录安装

```python
import os, shutil
src, dst = 'staging', os.path.expanduser('~/.workbuddy/skills')
for s in sorted(os.listdir(src)):
    d = os.path.join(dst, s)
    if os.path.exists(d): shutil.rmtree(d)
    shutil.copytree(os.path.join(src, s), d)
```

- **必须整目录复制** `SKILL.md` + `references/` + `static/` + `scripts/` + `assets/` + `manifest.yaml`；
  只复制 SKILL.md 会因相对路径缺失而失效。
- 目录名与 frontmatter `name` 不一致时（如 `nature-proposal-writer` → `researchwrite`）**保留目录名**，
  因为技能内部用相对路径引用同级共享包（如 `../nature-shared`）。
- 共享包（*shared*）也要装，但要告诉用户它不作为独立技能触发。

### 6. 校验 + 清理

逐个检查 `SKILL.md` 存在且 frontmatter 可解析（`---\nname: ...\ndescription: ...\n---`），
输出表格（技能名 / 文件数 / 体积 / 状态）。最后删除临时目录与 zip。

### 7. 配置随技能附带的 MCP 服务（如有）

装完后先扫一遍有没有 MCP：`find <skill> -iname "*mcp*"`，以及 `grep -rl -i mcp <skill>/SKILL.md`。

- 配置写到 `~/.workbuddy/mcp.json`（**不是** `~/.workbuddy/.mcp.json`），
  `{"mcpServers": {"<name>": {"command": ..., "args": [...], "env": {...}}}}`，merge 时不要覆盖其他条目。
- 上游常给 `uv run --no-project --with ...` 的启动方式；**本机没有 uv**，改为建独立 venv
  `~/.workbuddy/binaries/python/envs/<name>`，command 指向该 venv 的 `Scripts\python.exe`，
  args 只放入口脚本的绝对路径（Python 会把脚本目录加入 `sys.path[0]`，同目录导入无需 PYTHONPATH / cwd）。
- 依赖装进 venv：`<venv>/Scripts/python.exe -m pip install -r <skill>/.../requirements.txt`。
  注意 Bash 里传给 Windows Python 的路径必须写成 `C:/...`，`/c/...` 会直接报文件不存在。
- 中文/Windows 环境建议加 `PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`。
- **必须实测**：写个 .py 用 `mcp` 的 `stdio_client` + `ClientSession`，按 mcp.json 的 command/args/env
  拉起服务，`initialize()` → `list_tools()` → 试调一个工具。很多技能包的上游缺陷只有拉起时才暴露。
- 常见上游缺陷：源文件漏写 `from __future__ import annotations`，导致用第三方库类型做的注解在导入期求值失败
  （如 `defusedxml.ElementTree` 不导出 `Element`），表现为服务器启动即崩、客户端只报 `Connection closed`。
  补一行 `from __future__ import annotations` 即可；**重装技能后需重新补**，并记入记忆。
- 配置完成后告诉用户：MCP 不会自动生效，需在连接器管理页右上角自定义连接器入口点「信任」。

## 交付

向用户给出：镜像来源与完整性校验结果、安全审计结论、安装清单表、需要单独安装的运行依赖
（`pip install -r requirements.txt`、MCP 服务配置、API key 环境变量），以及安装后需新开会话才生效的提示。
