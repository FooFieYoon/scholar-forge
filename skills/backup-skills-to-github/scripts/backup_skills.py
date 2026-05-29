#!/usr/bin/env python3
"""
Backup WorkBuddy original skills to GitHub via REST API.
Avoids git clone/push on Windows (schannel / sandbox issues).

Usage:
    python3 backup_skills.py <owner>/<repo> [--dir <subdir>] [--all] [--optimize]

Examples:
    python3 backup_skills.py FooFieYoon/workbuddy-skills --all
    python3 backup_skills.py FooFieYoon/workbuddy-skills --all --optimize
"""
import os
import sys
import json
import base64
import argparse
import subprocess
import urllib.request
import urllib.error
import re


SKILLS_DIR = os.path.expanduser("~/.workbuddy/skills")


def get_gh_token():
    result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
    token = result.stdout.strip()
    if not token:
        print("ERROR: Not logged into GitHub. Run: gh auth login --web")
        sys.exit(1)
    return token


def make_headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }


def api_request(url, method="GET", data=None, headers=None):
    """Make a GitHub API request. Returns (response_dict, error_dict)."""
    req = urllib.request.Request(url, headers=headers, method=method)
    if data is not None:
        req.data = json.dumps(data).encode("utf-8")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read())
        except Exception:
            err = {"message": str(e)}
        return None, err


def scan_original_skills():
    """Scan SKILLS_DIR for skills with agent_created: true in YAML frontmatter."""
    results = []
    for root, _dirs, files in os.walk(SKILLS_DIR):
        for fname in files:
            if fname != "SKILL.md":
                continue
            fp = os.path.join(root, fname)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
                m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
                if not m:
                    continue
                fm = {}
                for line in m.group(1).splitlines():
                    if ":" in line:
                        idx = line.index(":")
                        k = line[:idx].strip()
                        v = line[idx + 1:].strip().strip("\"'")
                        fm[k] = v
                ac = fm.get("agent_created", "")
                if str(ac).lower() in ("true", "true"):
                    rel = os.path.relpath(root, SKILLS_DIR)
                    results.append(rel)
            except Exception:
                pass
    return results


def collect_skill_files(skill_name):
    """Collect all files under a skill directory."""
    skill_path = os.path.join(SKILLS_DIR, skill_name)
    files = []
    for root, _dirs, fnames in os.walk(skill_path):
        for fname in fnames:
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, SKILLS_DIR).replace(os.sep, "/")
            files.append((rel, fpath))
    return files


def upload_file(repo, file_rel, file_local, headers, subdir=""):
    """Upload a single file to GitHub via REST API."""
    repo_path = f"{subdir}/{file_rel}" if subdir else file_rel
    repo_path = repo_path.lstrip("/")
    url = f"https://api.github.com/repos/{repo}/contents/{repo_path}"

    with open(file_local, "rb") as f:
        content_bytes = f.read()
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    # Check if file exists (to get SHA for update)
    _, err = api_request(url, "GET", headers=headers)
    if err and err.get("message", "").startswith("Not Found"):
        data = {"message": f"Add {repo_path}", "content": content_b64}
        _, err = api_request(url, "PUT", data=data, headers=headers)
        if err:
            print(f"  FAIL (create): {repo_path} — {err.get('message')}")
            return False
        print(f"  Created: {repo_path}")
        return True
    else:
        existing, _ = api_request(url, "GET", headers=headers)
        sha = existing.get("sha", "")
        data = {"message": f"Update {repo_path}", "content": content_b64, "sha": sha}
        _, err = api_request(url, "PUT", data=data, headers=headers)
        if err:
            print(f"  FAIL (update): {repo_path} — {err.get('message')}")
            return False
        print(f"  Updated: {repo_path}")
        return True


def generate_readme(skills):
    """Generate README.md content with full skill descriptions."""
    # Build table rows
    rows = []
    for s in sorted(skills):
        # Try to read description from SKILL.md
        skill_md_path = os.path.join(SKILLS_DIR, s, "SKILL.md")
        desc = ""
        trigger = ""
        try:
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Extract description from frontmatter
            m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if m:
                fm = {}
                for line in m.group(1).splitlines():
                    if ":" in line:
                        idx = line.index(":")
                        fm[line[:idx].strip()] = line[idx+1:].strip().strip("\"'")
                desc = fm.get("description", "")
        except Exception:
            pass
        rows.append(f"| `{s}` | {desc} |")
    skills_table = "\n".join(rows)

    return f"""# WorkBuddy Skills Backup

本仓库备份 WorkBuddy AI 助手的**原创 Skills**（`agent_created: true`），可直接导入使用。

## 包含的 Skills

| Skill 名称 | 功能说明 |
|---|---|
{skills_table}

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
    └── assets/           # 资源文件（可选）
```

## 触发示例

| 用户说 | 触发 Skill |
|---|---|
| "写一篇学术会议论文" | `academic-conference-paper-writer` |
| "帮我写论文" | `academic-paper-writer` |
| "写教学科研论文" | `edu-research-paper` |
| "降低 AIGC 检测率" | `paperyy-aigc-rewrite` |

## 关于 WorkBuddy

WorkBuddy 是一个强大的 AI 编程助手，支持通过 Skills 扩展能力。每个 Skill 是一个独立的能力模块，包含触发条件、工作流程和参考资料。

- 官网：https://www.workbuddy.ai
- Skills 文档：https://www.workbuddy.ai/docs/skills

## 贡献

这些是原创 Skill，如果你有改进建议，欢迎提 Issue 或 PR。

---
*由 WorkBuddy 自动备份 · 最后更新：2026-05-30*
"""


def upload_readme(repo, headers, skills, subdir=""):
    """Generate and upload README.md."""
    readme_content = generate_readme(skills)
    content_b64 = base64.b64encode(readme_content.encode("utf-8")).decode("utf-8")

    url = f"https://api.github.com/repos/{repo}/contents/README.md"
    _, err = api_request(url, "GET", headers=headers)
    if err and err.get("message", "").startswith("Not Found"):
        data = {"message": "Add README.md", "content": content_b64}
    else:
        existing, _ = api_request(url, "GET", headers=headers)
        data = {"message": "Update README.md", "content": content_b64, "sha": existing.get("sha", "")}

    _, err = api_request(url, "PUT", data=data, headers=headers)
    if err:
        print(f"  README upload FAIL: {err.get('message')}")
        return False
    print("  README.md uploaded")
    return True


def main():
    parser = argparse.ArgumentParser(description="Backup WorkBuddy skills to GitHub")
    parser.add_argument("repo", help="GitHub repo, e.g. owner/repo")
    parser.add_argument("--dir", default="skills", help="Subdirectory in repo (default: skills)")
    parser.add_argument("--all", action="store_true", help="Auto-scan and upload all original skills")
    parser.add_argument("--skill", action="append", help="Specify skill name(s) to upload")
    args = parser.parse_args()

    token = get_gh_token()
    headers = make_headers(token)

    # Determine skills to upload
    if args.all:
        skills = scan_original_skills()
        if not skills:
            print("No original skills found (agent_created: true).")
            sys.exit(0)
        print(f"Found {len(skills)} original skill(s): {', '.join(skills)}")
    elif args.skill:
        skills = args.skill
    else:
        print("ERROR: Specify --all or --skill <name>")
        sys.exit(1)

    # Collect all files
    all_files = []
    for skill in skills:
        files = collect_skill_files(skill)
        all_files.extend(files)
        print(f"  {skill}: {len(files)} file(s)")

    if not all_files:
        print("No files to upload.")
        sys.exit(0)

    print(f"\nTotal files to upload: {len(all_files)}")

    # Upload each file
    ok = 0
    fail = 0
    for rel, local in all_files:
        if upload_file(args.repo, rel, local, headers, subdir=args.dir):
            ok += 1
        else:
            fail += 1

    # Upload README
    print("\nUploading README.md...")
    upload_readme(args.repo, headers, skills, subdir=args.dir)

    print(f"\nDone! Success: {ok}, Failed: {fail}")
    print(f"Repo: https://github.com/{args.repo}")


if __name__ == "__main__":
    main()
