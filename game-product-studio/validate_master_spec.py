#!/usr/bin/env python3
"""Quick validation script for skills - minimal version."""

import re
import sys
from pathlib import Path

import yaml

MAX_SKILL_NAME_LENGTH = 64


def validate_skill(skill_path):
    """Basic validation of a skill."""
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML in frontmatter: {exc}"

    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}
    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        return False, "Unexpected key(s) in SKILL.md frontmatter: " + ", ".join(sorted(unexpected_keys))
    if "name" not in frontmatter or "description" not in frontmatter:
        return False, "Missing name or description in frontmatter"

    name = frontmatter["name"]
    description = frontmatter["description"]
    if not isinstance(name, str) or not re.match(r"^[a-z0-9-]+$", name.strip()) or name.startswith("-") or name.endswith("-") or "--" in name or len(name) > MAX_SKILL_NAME_LENGTH:
        return False, "Invalid skill name"
    if not isinstance(description, str) or "<" in description or ">" in description or len(description.strip()) > 1024:
        return False, "Invalid skill description"
    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
