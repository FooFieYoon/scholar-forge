#!/usr/bin/env python3
"""
Backup original skills to GitHub ScholarForge via REST API.
Avoids git clone/push on Windows (schannel / sandbox issues).

README 更新策略：
  - 只在文件末尾的 "## 包含的 Skills" 汇总表格中增量追加新 skill
  - 扫描所有格式识别已有 skill（表格行 + 加粗标题行）
  - 不影响正文内容，不重复创建表格

Usage:
    python3 backup_skills.py <owner>/<repo> [--dir <subdir>] [--all] [--optimize]

Examples:
    python3 backup_skills.py FooFieYoon/scholar-forge --all
    python3 backup_skills.py FooFieYoon/scholar-forge --skill my-skill
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
                if str(ac).lower() in ("true",):
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


def get_skill_description(skill_name):
    """Extract description from a skill's SKILL.md frontmatter."""
    skill_md_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not m:
            return ""
        lines = m.group(1).splitlines()
        fm = {}
        i = 0
        while i < len(lines):
            line = lines[i]
            if ":" in line:
                idx = line.index(":")
                k = line[:idx].strip()
                v = line[idx + 1:].strip().strip("\"'")
                # Handle YAML folded block scalar (>)
                if v == ">":
                    folded = []
                    i += 1
                    while i < len(lines):
                        ln = lines[i]
                        # Indented lines are part of the block
                        if ln.startswith("  ") or ln.startswith("    "):
                            folded.append(ln.strip())
                        elif ln.strip() == "":
                            folded.append("")
                        else:
                            break
                        i += 1
                    v = " ".join(folded)
                fm[k] = v
            i += 1
        desc = fm.get("description", "")
        if isinstance(desc, str):
            return desc
        return ""
    except Exception:
        pass
    return ""


def parse_existing_skills_from_readme(readme_text):
    """Parse skill names from ALL formats in the README.

    Matches:
      - Table rows: | `skill-name` | ...
      - Bold titles: **`skill-name`** (used in the main skill sections)
    """
    existing = set()
    for line in readme_text.splitlines():
        # Format 1: markdown table row | `xxx` |
        m = re.match(r'^\|\s*`([^`]+)`\s*\|', line)
        if m:
            existing.add(m.group(1))
        # Format 2: bold inline code **`xxx`** (e.g. **`sensenova-image`**)
        m = re.search(r'\*\*`([^`]+)`\*\*', line)
        if m:
            existing.add(m.group(1))
    return existing


def generate_readme_incremental(existing_readme, new_skills):
    """Incrementally add new skill entries to the '## 包含的 Skills' table at EOF.

    Rules:
      1. Scan ALL formats to detect existing skills (prevents duplicates)
      2. Only append to the LAST '## 包含的 Skills' section at file end
      3. If no section exists, create one at EOF
      4. Never insert into main content — avoids breaking existing structure
    """
    existing_skills = parse_existing_skills_from_readme(existing_readme)
    truly_new = sorted([s for s in new_skills if s not in existing_skills])

    if not truly_new:
        return None  # Nothing to add

    # Build new table rows
    new_rows = [f"| `{s}` | {get_skill_description(s)} |" for s in truly_new]

    lines = existing_readme.splitlines()

    # Find the LAST occurrence of "## 包含的 Skills" section
    section_idx = None
    for i in range(len(lines) - 1, -1, -1):
        if re.match(r'^##\s+包含的\s+Skills\s*$', lines[i]):
            section_idx = i
            break

    if section_idx is not None:
        # Append new rows to the table in this section
        # Find the last existing table row after section_idx
        last_row = section_idx
        for i in range(section_idx + 1, len(lines)):
            if re.match(r'^\|\s*`[^`]+`\s*\|', lines[i]):
                last_row = i
            elif re.match(r'^##\s+', lines[i]):
                # Hit next section header — stop
                break

        # If last_row is still section_idx (no table rows found), create table
        if last_row == section_idx:
            table_section = [
                "",
                "| Skill 名称 | 功能说明 |",
                "|---|---|",
            ] + new_rows + [""]
            lines = lines[:section_idx + 1] + table_section + lines[section_idx + 1:]
        else:
            lines = lines[:last_row + 1] + new_rows + lines[last_row + 1:]
    else:
        # No section found — append at end
        table_section = [
            "",
            "---",
            "",
            "## 包含的 Skills",
            "",
            "| Skill 名称 | 功能说明 |",
            "|---|---|",
        ] + new_rows + [""]
        lines = lines + table_section

    new_readme = "\n".join(lines)
    print(f"  README: adding {len(truly_new)} new skill(s): {', '.join(truly_new)}")
    return new_readme


def upload_readme_incremental(repo, headers, skills):
    """Fetch existing README, incrementally add new skill entries, upload."""
    url = f"https://api.github.com/repos/{repo}/contents/README.md"
    existing, err = api_request(url, "GET", headers=headers)

    if err and err.get("message", "").startswith("Not Found"):
        # README doesn't exist — create from scratch
        rows = []
        for s in sorted(skills):
            desc = get_skill_description(s)
            rows.append(f"| `{s}` | {desc} |")
        readme_content = (
            "# ScholarForge / 学术匠心工坊\n\n"
            "> **Author: Yin**\n"
            "> AI 驱动的学术写作与知识产权工具集。\n\n"
            "---\n\n"
            "## 包含的 Skills\n\n"
            "| Skill 名称 | 功能说明 |\n"
            "|---|---|\n"
            + "\n".join(rows)
            + "\n"
        )
        data = {"message": "Add README.md",
                "content": base64.b64encode(readme_content.encode("utf-8")).decode("utf-8")}
        _, put_err = api_request(url, "PUT", data=data, headers=headers)
        if put_err:
            print(f"  README create FAIL: {put_err.get('message')}")
            return False
        print("  README.md created (initial)")
        return True

    # README exists — incremental update
    existing_content = base64.b64decode(existing["content"]).decode("utf-8")
    new_content = generate_readme_incremental(existing_content, skills)

    if new_content is None:
        print("  README already up to date (no new skills to add)")
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
    parser = argparse.ArgumentParser(description="Backup skills to GitHub ScholarForge")
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

    # Upload README (incremental — only adds new skill entries)
    print("\nUpdating README.md (incremental)...")
    upload_readme_incremental(args.repo, headers, skills)

    print(f"\nDone! Success: {ok}, Failed: {fail}")
    print(f"Repo: https://github.com/{args.repo}")


if __name__ == "__main__":
    main()
