"""Validate tool names in all agent markdown files.

Scans every *.agent.md file under:
  - .github/agents/
  - plugins/**/agents/

For each file the YAML frontmatter ``tools:`` block is parsed and every tool
name is checked against the authorised set. Unknown names are emitted as
violations.

Usage::

    python scripts/validate_tool_names.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

VALID_TOOLS: frozenset[str] = frozenset(
    {
        "agent",
        "search",
        "usages",
        "problems",
        "changes",
        "testFailure",
        "web",
        "fetch",
        "edit",
        "execute",
        "read",
        "mcp",
    }
)

_FRONTMATTER_RE = re.compile(
    r"^\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize(text: str) -> str:
    """Strip UTF-8 BOM and normalise CRLF / bare CR to LF."""
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def _collect_agent_files() -> list[Path]:
    """Return all *.agent.md files in the two canonical scan locations."""
    files: list[Path] = []

    root_dir = REPO_ROOT / ".github" / "agents"
    if root_dir.is_dir():
        files.extend(sorted(root_dir.glob("*.agent.md")))

    plugins_dir = REPO_ROOT / "plugins"
    if plugins_dir.is_dir():
        files.extend(sorted(plugins_dir.rglob("*.agent.md")))

    return files


def _extract_frontmatter(text: str) -> str | None:
    """Return the raw frontmatter body (between the two ``---`` fences) or None."""
    normalized = _normalize(text)
    match = _FRONTMATTER_RE.match(normalized)
    if not match:
        return None
    return match.group(1)


def _parse_tools(frontmatter: str) -> list[str] | None:
    """Extract the list of tool names from a frontmatter block.

    Returns ``None`` when no ``tools:`` key is present, an empty list when the
    key exists but has no entries.
    """
    lines = frontmatter.split("\n")

    # Locate the ``tools:`` key and determine its format.
    tools_start: int | None = None
    inline_value: str | None = None

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"^tools\s*:", stripped):
            # Check for an inline list: tools: ["a", "b"]  or  tools: [a, b]
            inline_match = re.match(
                r"^tools\s*:\s*\[(.+)\]\s*$", stripped
            )
            if inline_match:
                inline_value = inline_match.group(1)
            else:
                tools_start = idx
            break

    if tools_start is None and inline_value is None:
        return None  # No tools key found

    if inline_value is not None:
        # Parse comma-separated names, stripping quotes and whitespace.
        raw_names = [
            n.strip().strip('"').strip("'") for n in inline_value.split(",")
        ]
        return [n for n in raw_names if n]

    # Sequence style: collect indented ``- toolname`` items until a non-
    # indented, non-empty, non-comment line is encountered.
    tool_names: list[str] = []
    for line in lines[tools_start + 1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        item_match = re.match(r"^-\s+(\S+)", stripped)
        if item_match:
            tool_names.append(item_match.group(1))
        else:
            # A non-list line means we have left the tools block.
            break

    return tool_names


# ---------------------------------------------------------------------------
# Public validation API
# ---------------------------------------------------------------------------


def validate_file(path: Path) -> list[str]:
    """Return a list of violation strings for *path*. Empty list = OK."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return [f"{path} | read error"]

    frontmatter = _extract_frontmatter(text)
    if frontmatter is None:
        return []  # No frontmatter — skip silently

    tools = _parse_tools(frontmatter)
    if tools is None:
        return []  # No tools key — allowed

    violations: list[str] = []
    for tool in tools:
        if tool not in VALID_TOOLS:
            violations.append(f"{path} | tool: {tool} | INVALID")

    return violations


def validate_all(files: list[Path]) -> list[str]:
    """Run :func:`validate_file` over every file and aggregate violations."""
    all_violations: list[str] = []
    for path in files:
        all_violations.extend(validate_file(path))
    return all_violations


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    files = _collect_agent_files()
    violations = validate_all(files)

    if violations:
        for v in violations:
            print(v)
        print("TOOL NAME VALIDATION FAILED")
        sys.exit(1)
    else:
        print(f"TOOL NAME VALIDATION OK ({len(files)} files checked)")
        sys.exit(0)


if __name__ == "__main__":
    main()
