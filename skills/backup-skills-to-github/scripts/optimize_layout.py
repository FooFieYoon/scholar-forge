#!/usr/bin/env python3
"""
Optimize GitHub repo layout for ScholarForge skills backup.
- Moves all skill dirs into skills/ subdirectory (if not already)
- Updates README.md incrementally (only adds new skill entries)

Usage:
    python3 optimize_layout.py <owner>/<repo>
"""
import os
import sys
import json
import base64
import subprocess
import urllib.request
import urllib.error
import re


def get_gh_token():
    result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
    return result.stdout.strip()


def make_headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }


def api_request(url, method="GET", data=None, headers=None):
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


def list_repo_files(repo, headers, path=""):
    """Recursively list all files in repo."""
    url = f"https://api.github.com/repos/{repo}/contents"
    if path:
        url += f"/{path}"
    items, _ = api_request(url, "GET", headers=headers)
    if not items:
        return []
    files = []
    for item in items:
        if item["type"] == "file":
            files.append(item["path"])
        elif item["type"] == "dir" and item["name"] != "skills":
            files.extend(list_repo_files(repo, headers, item["path"]))
    return files


def get_skill_names_from_repo(repo, headers):
    """Get skill names by listing skills/ dir, or root dir if skills/ doesn't exist."""
    url = f"https://api.github.com/repos/{repo}/contents/skills"
    items, err = api_request(url, "GET", headers=headers)
    if err:
        url = f"https://api.github.com/repos/{repo}/contents"
        items, _ = api_request(url, "GET", headers=headers)
        skills = [it["name"] for it in items
                  if it["type"] == "dir" and it["name"] != "skills"]
        return skills, False
    skills = [it["name"] for it in items if it["type"] == "dir"]
    return skills, True


def move_file(repo, old_path, new_path, headers):
    """Move a file by re-uploading to new path and deleting old."""
    old_url = f"https://api.github.com/repos/{repo}/contents/{old_path}"
    data, err = api_request(old_url, "GET", headers=headers)
    if err:
        print(f"  SKIP (not found): {old_path}")
        return False
    sha = data["sha"]
    content_b64 = data["content"].strip()

    new_url = f"https://api.github.com/repos/{repo}/contents/{new_path}"
    payload = {
        "message": f"Move {old_path} -> {new_path}",
        "content": content_b64,
    }
    _, err = api_request(new_url, "PUT", data=payload, headers=headers)
    if err:
        print(f"  FAIL move {old_path}: {err.get('message')}")
        return False

    del_payload = {
        "message": f"Delete old {old_path}",
        "sha": sha,
    }
    _, err = api_request(old_url, "DELETE", data=del_payload, headers=headers)
    if err:
        print(f"  WARN: could not delete old {old_path}: {err.get('message')}")
    return True


def build_initial_readme(skills):
    """Build a fresh README from scratch."""
    rows = []
    for s in sorted(skills):
        rows.append(f"| `{s}` | 原创 Skill |")
    skills_table = "\n".join(rows) if rows else "（无）"

    return f"""# ScholarForge / 学术匠心工坊

> **Author: Yin**
> AI 驱动的学术写作与知识产权工具集。

---

## 包含的 Skills

| Skill 名称 | 类型 |
|---|---|
{skills_table}

---

> 本 README 由优化脚本自动生成。
> 仓库地址：[github.com/FooFieYoon/scholar-forge](https://github.com/FooFieYoon/scholar-forge)

---
*By Yin*
"""


def parse_existing_skills_from_readme(readme_text):
    """Parse skill names already listed in the README table."""
    existing = set()
    for line in readme_text.splitlines():
        m = re.match(r'^\|\s*`([^`]+)`\s*\|', line)
        if m:
            existing.add(m.group(1))
    return existing


def generate_readme_incremental(existing_readme, new_skills):
    """Incrementally add new skill entries. Returns None if no changes needed."""
    existing_skills = parse_existing_skills_from_readme(existing_readme)
    truly_new = sorted([s for s in new_skills if s not in existing_skills])

    if not truly_new:
        return None

    new_rows = [f"| `{s}` | 原创 Skill |" for s in truly_new]

    lines = existing_readme.splitlines()
    last_skill_row = -1
    for i, line in enumerate(lines):
        if re.match(r'^\|\s*`[^`]+`\s*\|', line):
            last_skill_row = i

    if last_skill_row >= 0:
        lines = lines[:last_skill_row + 1] + new_rows + lines[last_skill_row + 1:]
    else:
        # Append table at end
        table_section = [
            "",
            "## 包含的 Skills",
            "",
            "| Skill 名称 | 类型 |",
            "|---|---|",
        ] + new_rows + [""]
        lines = lines + table_section

    print(f"  README: adding {len(truly_new)} new skill(s): {', '.join(truly_new)}")
    return "\n".join(lines)


def update_readme_incremental(repo, headers, skills):
    """Fetch existing README, incrementally add new skill entries, upload."""
    url = f"https://api.github.com/repos/{repo}/contents/README.md"
    existing, err = api_request(url, "GET", headers=headers)

    if err and err.get("message", "").startswith("Not Found"):
        content = build_initial_readme(skills)
        data = {"message": "Add README.md", "content": base64.b64encode(content.encode("utf-8")).decode("utf-8")}
        _, put_err = api_request(url, "PUT", data=data, headers=headers)
        if put_err:
            print(f"  README create FAIL: {put_err.get('message')}")
            return False
        print("  README.md created (initial)")
        return True

    existing_content = base64.b64decode(existing["content"]).decode("utf-8")
    new_content = generate_readme_incremental(existing_content, skills)

    if new_content is None:
        print("  README already up to date (no new skills)")
        return True

    content_b64 = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    data = {
        "message": "Add new skills to README (incremental)",
        "content": content_b64,
        "sha": existing["sha"],
    }
    _, put_err = api_request(url, "PUT", data=data, headers=headers)
    if put_err:
        print(f"  README update FAIL: {put_err.get('message')}")
        return False
    print("  README.md updated (incremental)")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 optimize_layout.py <owner>/<repo>")
        sys.exit(1)

    repo = sys.argv[1]
    token = get_gh_token()
    if not token:
        print("ERROR: Not logged in. Run: gh auth login")
        sys.exit(1)
    headers = make_headers(token)

    print(f"Optimizing {repo} ...")
    print()

    skills, already_in_subdir = get_skill_names_from_repo(repo, headers)
    print(f"Found skills: {', '.join(skills) if skills else '(none)'}")
    print(f"Already in skills/ subdir: {already_in_subdir}")
    print()

    if not already_in_subdir and skills:
        print("Moving skills into skills/ subdir...")
        moved = 0
        for skill_name in skills:
            files = list_repo_files(repo, headers, skill_name)
            ok = True
            for fpath in files:
                new_path = f"skills/{fpath}"
                if move_file(repo, fpath, new_path, headers):
                    moved += 1
                else:
                    ok = False
            if ok:
                print(f"  Moved: {skill_name}")
        print(f"  Total files moved: {moved}")
        print()

    print("Updating README.md (incremental)...")
    skills, _ = get_skill_names_from_repo(repo, headers)
    update_readme_incremental(repo, headers, skills)

    print()
    print(f"Done! Repo: https://github.com/{repo}")


if __name__ == "__main__":
    main()
