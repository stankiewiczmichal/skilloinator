#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check the marketplace, plugin manifests and SKILL.md frontmatter."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Files copied into several skills so each skill installs on its own; copies must match.
SHARED = {
    "scripts/slop_score.py": ["humanizator", "slopperoinator"],
    "scripts/lexicon/en.json": ["humanizator", "slopperoinator"],
    "scripts/lexicon/pl.json": ["humanizator", "slopperoinator"],
}
errors = []


def err(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        err(path, f"invalid JSON ({e})")
        return None


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(path, "missing YAML frontmatter (--- ... ---)")
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def check_skill(skill_md):
    fm = frontmatter(skill_md)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        err(skill_md, "frontmatter needs 'name'")
    elif not NAME_RE.match(name) or len(name) > 64:
        err(skill_md, f"name '{name}' must be lowercase-hyphenated, max 64 chars")
    elif name != skill_md.parent.name:
        err(skill_md, f"name '{name}' must match folder '{skill_md.parent.name}'")
    if not desc:
        err(skill_md, "frontmatter needs 'description'")
    elif len(desc) > 1024:
        err(skill_md, f"description is {len(desc)} chars, max 1024")


def main():
    mp_path = ROOT / ".claude-plugin" / "marketplace.json"
    mp = load_json(mp_path) or {}
    listed = set()
    for p in mp.get("plugins", []):
        name, source = p.get("name", ""), p.get("source", "")
        if not NAME_RE.match(name):
            err(mp_path, f"plugin name '{name}' must be lowercase-hyphenated")
        listed.add(name)
        if isinstance(source, str) and source.startswith("./"):
            pdir = (ROOT / source).resolve()
            manifest = pdir / ".claude-plugin" / "plugin.json"
            if not manifest.is_file():
                err(mp_path, f"'{name}': {source}/.claude-plugin/plugin.json not found")
                continue
            pj = load_json(manifest) or {}
            if pj.get("name") != name:
                err(manifest, f"name '{pj.get('name')}' must equal '{name}' from marketplace.json")
            if "version" in p and p["version"] != pj.get("version"):
                err(manifest, f"version '{pj.get('version')}' differs from '{p['version']}' in marketplace.json")
            skills = list(pdir.glob("skills/*/SKILL.md"))
            if not skills and not (pdir / "commands").is_dir():
                err(manifest, "plugin has no skills/<name>/SKILL.md")
            for s in skills:
                check_skill(s)

    for manifest in ROOT.glob("plugins/*/.claude-plugin/plugin.json"):
        name = (load_json(manifest) or {}).get("name")
        if name not in listed:
            err(manifest, f"plugin '{name}' is not listed in marketplace.json")

    for rel, skills in SHARED.items():
        paths = [ROOT / "plugins" / s / "skills" / s / rel for s in skills]
        missing = [p for p in paths if not p.is_file()]
        for p in missing:
            err(p, "shared file is missing")
        if not missing and len({p.read_bytes() for p in paths}) > 1:
            err(paths[0], f"shared copies differ: {', '.join(str(p.relative_to(ROOT)) for p in paths)}")
        for p in paths:
            if p.suffix == ".json" and p.is_file():
                load_json(p)

    if errors:
        print("\n".join(f"✗ {e}" for e in errors))
        sys.exit(1)
    print(f"✓ {len(listed)} plugin(s) OK")


if __name__ == "__main__":
    main()
