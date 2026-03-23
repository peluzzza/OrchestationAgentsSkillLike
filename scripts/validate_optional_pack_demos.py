"""Validate that the optional plugin pack demo folders are complete and correct.

Checks performed for each registered demo:
- Demo directory exists under ``demos/``.
- Required documentation files (README.md, DEMO_PROMPT.md) are present.
- At least one non-test Python module is present.
- At least one test file (``test_*.py``) is present.
- No documentation file uses forbidden "enable all / plugin-only" activation
  language.
- Every documentation file references the canonical ``.github/agents`` path.
- DEMO_PROMPT.md references the demo's specific plugin path (not a different
  pack, and not a blanket all-packs reference).

Usage::

    python3 scripts/validate_optional_pack_demos.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

# Files that must exist inside every validated demo directory.
_REQUIRED_FILES: tuple[str, ...] = ("README.md", "DEMO_PROMPT.md")


def _load_demo_packs() -> tuple[tuple[str, str, str], ...]:
    """Load optional-pack demo entries from the pack registry.

    Returns a tuple of ``(demo_dir_name, pack_id, plugin_path_fragment)``
    for each registry entry that declares a ``demo`` key.  Falls back to an
    empty tuple when the registry file is absent.
    """
    registry_path = REPO_ROOT / ".github" / "plugin" / "pack-registry.json"
    if not registry_path.is_file():
        return ()
    with registry_path.open("r", encoding="utf-8") as handle:
        registry = json.load(handle)
    return tuple(
        (pack["demo"], pack["id"], pack["installPath"])
        for pack in registry.get("packs", [])
        if pack.get("demo") and pack.get("id") and pack.get("installPath")
    )


# Evaluated at import time against the real repo root.  Tests that exercise
# main() must supply a mock registry; tests that call _collect_errors()
# directly are unaffected by this constant.
OPTIONAL_PACK_DEMOS: tuple[tuple[str, str, str], ...] = _load_demo_packs()

# Phrases that indicate unsupported "enable everything" activation patterns.
_FORBIDDEN_PHRASES: tuple[str, ...] = (
    "enable all plugins",
    "activate all plugins",
    "all plugin packs",
    "install every plugin",
    "plugin-only activation",
    "activate all packs",
    "enable all packs",
)

# Every demo doc must mention the canonical agents location.
_CORE_AGENTS_PATH = ".github/agents"


def _read_lower(path: Path) -> str:
    """Return file contents in lowercase for case-insensitive checks."""
    return path.read_text(encoding="utf-8").lower()


def _required_file_errors(demo_dir_name: str, demo_path: Path) -> list[str]:
    """Validate the required documentation files for one demo."""
    errors: list[str] = []

    for filename in _REQUIRED_FILES:
        if not (demo_path / filename).is_file():
            errors.append(f"{demo_dir_name}: {filename} missing")

    return errors


def _python_file_errors(demo_dir_name: str, demo_path: Path) -> list[str]:
    """Validate that the demo contains both module and test Python files."""
    errors: list[str] = []
    py_files = sorted(demo_path.glob("*.py"))
    test_files = [f for f in py_files if f.stem.startswith("test_")]
    module_files = [f for f in py_files if not f.stem.startswith("test_")]

    if not module_files:
        errors.append(
            f"{demo_dir_name}: no Python module found"
            " (expected at least one non-test .py file)"
        )
    if not test_files:
        errors.append(
            f"{demo_dir_name}: no test file found"
            " (expected a file whose name starts with test_)"
        )

    return errors


def _documentation_errors(demo_dir_name: str, demo_path: Path) -> list[str]:
    """Validate docs content for one demo directory."""
    errors: list[str] = []

    for filename in _REQUIRED_FILES:
        doc_path = demo_path / filename
        if not doc_path.is_file():
            continue

        content_lower = _read_lower(doc_path)

        for phrase in _FORBIDDEN_PHRASES:
            if phrase in content_lower:
                errors.append(
                    f"{demo_dir_name}/{filename}: forbidden phrase '{phrase}'"
                    " — do not encourage enabling all or plugin-only activation"
                )

        if _CORE_AGENTS_PATH not in content_lower:
            errors.append(
                f"{demo_dir_name}/{filename}: must reference"
                f" '{_CORE_AGENTS_PATH}' (canonical agents path)"
            )

    return errors


def _prompt_plugin_errors(demo_dir_name: str, demo_path: Path, plugin_path_fragment: str) -> list[str]:
    """Validate that the prompt names the correct plugin path."""
    prompt_path = demo_path / "DEMO_PROMPT.md"
    if not prompt_path.is_file():
        return []

    prompt_lower = _read_lower(prompt_path)
    if plugin_path_fragment.lower() in prompt_lower:
        return []

    return [
        f"{demo_dir_name}/DEMO_PROMPT.md: must reference the plugin path"
        f" '{plugin_path_fragment}'"
    ]


def _collect_errors(demo_dir_name: str, plugin_path_fragment: str) -> list[str]:
    """Return a list of validation error strings for one demo directory.

    Args:
        demo_dir_name: Name of the directory under ``demos/``.
        plugin_path_fragment: The plugin path string that must appear in
            DEMO_PROMPT.md (e.g. ``plugins/automation-mcp-workflow``).

    Returns:
        A list of error strings.  Empty list means the demo is valid.
    """
    errors: list[str] = []
    demo_path = REPO_ROOT / "demos" / demo_dir_name

    if not demo_path.is_dir():
        errors.append(f"{demo_dir_name}: demo directory missing")
        return errors

    errors.extend(_required_file_errors(demo_dir_name, demo_path))
    errors.extend(_python_file_errors(demo_dir_name, demo_path))
    errors.extend(_documentation_errors(demo_dir_name, demo_path))
    errors.extend(_prompt_plugin_errors(demo_dir_name, demo_path, plugin_path_fragment))

    return errors


def main() -> int:
    """Run all optional pack demo validations.

    Returns:
        0 on success, 1 if any validation errors were found.
    """
    demo_packs = _load_demo_packs()
    all_errors: list[str] = []

    for demo_dir_name, _pack_id, plugin_path_fragment in demo_packs:
        all_errors.extend(_collect_errors(demo_dir_name, plugin_path_fragment))

    if all_errors:
        print("OPTIONAL PACK DEMO VALIDATION FAILED")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print(f"OPTIONAL PACK DEMO VALIDATION OK ({len(demo_packs)} demos checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
