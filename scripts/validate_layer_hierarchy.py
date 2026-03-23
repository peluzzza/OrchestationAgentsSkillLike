"""Validate the 3-layer agent hierarchy across the workspace.

Scans every *.agent.md file under:
  - .github/agents/
  - plugins/**/agents/

For each file the YAML frontmatter and the first ``<!-- layer: N -->`` comment
(within the first 3 lines after the closing ``---``) are parsed.

Enforced rules
--------------
1. Every agent must declare a layer comment — missing ones are flagged ORPHAN.
2. The ``Atlas`` agent (``name: Atlas``) must be layer 0.
3. No L0 agent's ``agents:`` list may reference an agent assigned layer 2.
4. No L1 agent's ``agents:`` list may reference an agent assigned layer 0.

Usage::

    python scripts/validate_layer_hierarchy.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

_FRONTMATTER_RE = re.compile(
    r"^\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)", re.DOTALL
)

# Matches: <!-- layer: N --> or <!-- layer: N | ... -->
_LAYER_COMMENT_RE = re.compile(r"<!--\s*layer:\s*(\d+)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize(text: str) -> str:
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def _collect_agent_files() -> list[Path]:
    files: list[Path] = []
    root_dir = REPO_ROOT / ".github" / "agents"
    if root_dir.is_dir():
        files.extend(sorted(root_dir.glob("*.agent.md")))
    plugins_dir = REPO_ROOT / "plugins"
    if plugins_dir.is_dir():
        files.extend(sorted(plugins_dir.rglob("*.agent.md")))
    return files


def _parse_frontmatter_and_body(text: str) -> tuple[str, str] | None:
    """Return (frontmatter_body, rest_of_file) or None if no valid frontmatter."""
    normalized = _normalize(text)
    match = _FRONTMATTER_RE.match(normalized)
    if not match:
        return None
    return match.group(1), match.group(2)


def _extract_name(frontmatter: str) -> str | None:
    m = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    return m.group(1).strip() if m else None


def _extract_layer_from_body(body: str) -> int | None:
    """Search within the first 3 lines of *body* for a layer comment."""
    lines = body.split("\n")[:3]
    for line in lines:
        m = _LAYER_COMMENT_RE.search(line)
        if m:
            return int(m.group(1))
    return None


def _extract_agents_list(frontmatter: str) -> list[str]:
    """Return names from the ``agents:`` YAML list."""
    lines = frontmatter.split("\n")
    in_agents = False
    names: list[str] = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^agents\s*:", stripped):
            in_agents = True
            continue
        if in_agents:
            if not stripped or stripped.startswith("#"):
                continue
            item = re.match(r"^-\s+(\S+)", stripped)
            if item:
                names.append(item.group(1))
            else:
                break
    return names


# ---------------------------------------------------------------------------
# Agent record
# ---------------------------------------------------------------------------


class AgentRecord:
    def __init__(
        self,
        path: Path,
        name: str | None,
        layer: int | None,
        agents_list: list[str],
    ) -> None:
        self.path = path
        self.name = name
        self.layer = layer
        self.agents_list = agents_list


def _parse_agent(path: Path) -> AgentRecord:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return AgentRecord(path, None, None, [])

    result = _parse_frontmatter_and_body(text)
    if result is None:
        return AgentRecord(path, None, None, [])

    frontmatter, body = result
    name = _extract_name(frontmatter)
    layer = _extract_layer_from_body(body)
    agents_list = _extract_agents_list(frontmatter)
    return AgentRecord(path, name, layer, agents_list)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate(files: list[Path]) -> tuple[list[AgentRecord], list[str]]:
    """Parse all files and return (records, violations)."""
    records = [_parse_agent(f) for f in files]

    # Build name→layer map for cross-agent checks.
    name_to_layer: dict[str, int] = {}
    for rec in records:
        if rec.name and rec.layer is not None:
            name_to_layer[rec.name] = rec.layer

    violations: list[str] = []

    for rec in records:
        # Rule 1: orphan check
        if rec.layer is None:
            violations.append(f"ORPHAN: {rec.path}")
            continue

        # Rule 2: Atlas must be layer 0
        if rec.name == "Atlas" and rec.layer != 0:
            violations.append(
                f"ATLAS LAYER ERROR: {rec.path} | expected layer 0, got {rec.layer}"
            )

        # Rule 3: L0 agents must not reference L2 agents
        if rec.layer == 0:
            for agent_name in rec.agents_list:
                if name_to_layer.get(agent_name) == 2:
                    violations.append(
                        f"L0→L2 VIOLATION: {rec.path} | "
                        f"L0 agent references L2 agent '{agent_name}'"
                    )

        # Rule 4: L1 agents must not reference L0 agents
        if rec.layer == 1:
            for agent_name in rec.agents_list:
                if name_to_layer.get(agent_name) == 0:
                    violations.append(
                        f"L1→L0 VIOLATION: {rec.path} | "
                        f"L1 agent references L0 agent '{agent_name}'"
                    )

    return records, violations


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _print_table(records: list[AgentRecord]) -> None:
    print(f"\n{'File':<55} {'Name':<25} {'Layer'}")
    print("-" * 90)
    for rec in sorted(records, key=lambda r: (r.layer if r.layer is not None else 99, str(r.path))):
        layer_str = str(rec.layer) if rec.layer is not None else "NONE"
        name_str = rec.name or "(unknown)"
        print(f"{str(rec.path.name):<55} {name_str:<25} {layer_str}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    files = _collect_agent_files()
    records, violations = validate(files)

    _print_table(records)
    print()

    if violations:
        for v in violations:
            print(v)
        print(f"\nLAYER HIERARCHY FAILED")
        sys.exit(1)
    else:
        print(f"LAYER HIERARCHY OK ({len(files)} files scanned)")
        sys.exit(0)


if __name__ == "__main__":
    main()
