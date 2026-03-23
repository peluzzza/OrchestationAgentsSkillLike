from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = REPO_ROOT / ".github" / "plugin" / "marketplace.json"
PLUGIN_ROOT = REPO_ROOT / "plugins"
FRONTMATTER_RE = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


class ValidationError(Exception):
    pass


def load_marketplace() -> dict:
    with MARKETPLACE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def frontmatter_blocks(agent_files: Iterable[Path]) -> list[tuple[Path, str]]:
    blocks: list[tuple[Path, str]] = []
    for path in agent_files:
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            raise ValidationError(f"Missing frontmatter block: {path}")
        blocks.append((path, match.group(1)))
    return blocks


def count_user_invocable(frontmatters: list[tuple[Path, str]]) -> int:
    return sum(1 for _, block in frontmatters if re.search(r"^user-invocable:\s*true\s*$", block, re.MULTILINE))


def validate_declared_dirs(plugin_dir: Path, rel_dirs: Iterable[str], *, slug: str, label: str, pattern: str) -> tuple[list[str], list[Path]]:
    errors: list[str] = []
    collected_files: list[Path] = []

    for rel_dir in rel_dirs:
        target_dir = (plugin_dir / rel_dir).resolve()
        if not target_dir.is_dir():
            errors.append(f"{slug}: {label} directory missing -> {rel_dir}")
            continue

        files = sorted(target_dir.glob(pattern))
        if not files:
            errors.append(f"{slug}: no {pattern} files found in {rel_dir}")
            continue

        collected_files.extend(files)

    return errors, collected_files


def validate_plugin_entry(entry: dict) -> list[str]:
    errors: list[str] = []
    slug = entry.get("source")
    if not slug:
        return ["marketplace entry missing required 'source' field"]

    plugin_dir = PLUGIN_ROOT / slug
    readme_path = plugin_dir / "README.md"
    manifest_path = plugin_dir / ".github" / "plugin" / "plugin.json"

    if not plugin_dir.is_dir():
        errors.append(f"{slug}: plugin directory missing")
        return errors

    if not readme_path.is_file():
        errors.append(f"{slug}: README.md missing")

    if not manifest_path.is_file():
        errors.append(f"{slug}: .github/plugin/plugin.json missing")
        return errors

    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)

    agent_dirs = manifest.get("agents", [])
    if not agent_dirs:
        errors.append(f"{slug}: manifest has no agents entries")
        return errors

    agent_errors, all_agent_files = validate_declared_dirs(
        plugin_dir,
        agent_dirs,
        slug=slug,
        label="agent",
        pattern="*.agent.md",
    )
    errors.extend(agent_errors)

    if not all_agent_files:
        return errors

    try:
        frontmatters = frontmatter_blocks(all_agent_files)
    except ValidationError as exc:
        errors.append(str(exc))
        return errors

    invocable_count = count_user_invocable(frontmatters)
    if invocable_count > 1:
        errors.append(f"{slug}: expected at most 1 user-invocable conductor, found {invocable_count}")

    skill_dirs = manifest.get("skills", [])
    if skill_dirs:
        skill_errors, _ = validate_declared_dirs(
            plugin_dir,
            skill_dirs,
            slug=slug,
            label="skill",
            pattern="SKILL.md",
        )
        errors.extend(skill_errors)

    return errors


def main() -> int:
    marketplace = load_marketplace()
    entries = marketplace.get("plugins", [])
    all_errors: list[str] = []

    for entry in entries:
        all_errors.extend(validate_plugin_entry(entry))

    if all_errors:
        print("PLUGIN PACK VALIDATION FAILED")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print(f"PLUGIN PACK VALIDATION OK ({len(entries)} marketplace entries checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())