#!/usr/bin/env python3
"""
Scan WorkBuddy skills directory and list all original skills
(agent_created: true in YAML frontmatter).

Usage:
    python3 scan_skills.py
    python3 scan_skills.py --json
    python3 scan_skills.py --path /custom/skills/path
"""
import os
import sys
import re
import json
import argparse


DEFAULT_SKILLS_DIR = os.path.expanduser("~/.workbuddy/skills")


def parse_frontmatter(content):
    """Parse the simple YAML subset used by SKILL.md, including folded blocks."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    lines = match.group(1).splitlines()
    frontmatter = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" not in line:
            i += 1
            continue
        idx = line.index(":")
        key = line[:idx].strip()
        value = line[idx + 1:].strip().strip("\"'")
        if value in (">", "|"):
            folded = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                folded.append(lines[i].strip())
                i += 1
            value = " ".join(part for part in folded if part)
            if line[idx + 1:].strip() == "|":
                value = "\n".join(folded)
            frontmatter[key] = value
            continue
        frontmatter[key] = value
        i += 1
    return frontmatter


def scan_original_skills(skills_dir):
    """Scan for skills with agent_created: true in YAML frontmatter."""
    results = []
    for root, _dirs, files in os.walk(skills_dir):
        for fname in files:
            if fname != "SKILL.md":
                continue
            fp = os.path.join(root, fname)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
                fm = parse_frontmatter(content)
                if not fm:
                    continue
                ac = fm.get("agent_created", "")
                if str(ac).lower() == "true":
                    rel = os.path.relpath(root, skills_dir)
                    desc = fm.get("description", "")
                    results.append({"name": rel, "path": root, "description": desc})
            except Exception:
                pass
    return results


def main():
    parser = argparse.ArgumentParser(description="Scan WorkBuddy original skills")
    parser.add_argument("--path", default=DEFAULT_SKILLS_DIR, help="Skills directory path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    skills = scan_original_skills(args.path)
    if args.json:
        print(json.dumps(skills, ensure_ascii=False, indent=2))
    else:
        if not skills:
            print("No original skills found (agent_created: true).")
            sys.exit(0)
        print(f"Found {len(skills)} original skill(s):\n")
        for s in skills:
            print(f"  - {s['name']}")
            if s["description"]:
                desc = s["description"][:80] + ("..." if len(s["description"]) > 80 else "")
                print(f"    {desc}")
        print(f"\nTotal: {len(skills)} skill(s)")


if __name__ == "__main__":
    main()
