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

# Matches: <!-- runtime-contract | key=value | key=value | ... -->
_RUNTIME_CONTRACT_RE = re.compile(r"<!--\s*runtime-contract\s*(.*?)-->")


# ---------------------------------------------------------------------------
# Stable runtime agent contract requirements
# ---------------------------------------------------------------------------
# Keys "request"/"response" hold frozensets of required field names.
# All other keys hold exact expected string values for the contract fields.

_STABLE_RUNTIME_AGENTS: dict[str, dict] = {
    "Atlas": {
        "version": "stable-runtime-v1",
        "role": "conductor",
        "layer": "0",
        "accepts": "user",
        "returns": "user",
        "approval": "explicit-only",
        "session": "required",
        "trace": "required",
        "request": frozenset({"goal", "constraints", "success_criteria"}),
        "response": frozenset({
            "status", "phase", "last_action_changes", "delegations",
            "decision", "pending_approvals", "next",
        }),
    },
    "Prometheus": {
        "version": "stable-runtime-v1",
        "role": "planner",
        "layer": "1",
        "accepts": "Atlas",
        "returns": "Atlas",
        "request": frozenset({"goal", "tech_stack", "feature_id", "plan_dir"}),
        "response": frozenset({
            "feature_id", "feature_dir", "spec_path", "plan_path",
            "analysis_report", "specify_pipeline_status", "open_questions", "atlas_notes",
        }),
    },
    "Sisyphus-subagent": {
        "version": "stable-runtime-v1",
        "role": "implementer",
        "layer": "1",
        "accepts": "Atlas",
        "returns": "Atlas",
        "request": frozenset({"feature_id", "phase", "acceptance_criteria", "constraints"}),
        "response": frozenset({
            "status", "scope_completed", "feature_id", "files_changed", "tests_added",
            "tasks_completed", "next_phase", "validation_run", "risks_found",
        }),
    },
    "Afrodita-subagent": {
        "version": "stable-runtime-v1",
        "role": "ui_implementer",
        "layer": "1",
        "accepts": "Atlas",
        "returns": "Atlas",
        "request": frozenset({"ui_scope", "component_patterns", "design_tokens", "acceptance_criteria"}),
        "response": frozenset({
            "status", "scope_completed", "files_changed", "ui_states_covered",
            "accessibility_notes", "responsive_notes", "validation_run", "tests_added", "risks_found",
        }),
    },
    "Themis Subagent": {
        "version": "stable-runtime-v1",
        "role": "reviewer",
        "layer": "1",
        "accepts": "Atlas",
        "returns": "Atlas",
        "request": frozenset({"phase_objective", "acceptance_criteria", "files_changed"}),
        "response": frozenset({
            "status", "summary", "strengths", "issues_found",
            "recommendations", "residual_risks", "next_steps",
        }),
    },
    "Argus - QA Testing Subagent": {
        "version": "stable-runtime-v1",
        "role": "qa_specialist",
        "layer": "1",
        "accepts": "Atlas",
        "returns": "Atlas",
        "request": frozenset({"phase_objective", "modified_files", "existing_tests"}),
        "response": frozenset({
            "status", "summary", "coverage_analysis", "edge_cases_discovered",
            "additional_tests_recommended", "test_execution_results", "next_steps",
        }),
    },
}


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


def _parse_runtime_contract(body: str) -> dict[str, str] | None:
    """Search the first 10 lines of *body* for a runtime-contract HTML comment.

    Returns a dict of raw key→value strings (values not further split),
    or None if no runtime-contract comment is present.
    """
    lines = body.split("\n")[:10]
    text = "\n".join(lines)
    m = _RUNTIME_CONTRACT_RE.search(text)
    if not m:
        return None
    result: dict[str, str] = {}
    for part in m.group(1).split("|"):
        part = part.strip()
        if "=" in part:
            key, _, value = part.partition("=")
            result[key.strip()] = value.strip()
    return result


def _extract_agents_list(frontmatter: str) -> list[str]:
    """Return names from the ``agents:`` YAML list.

    The full text after ``- `` is captured so multi-word names such as
    ``Themis Subagent`` or ``Argus - QA Testing Subagent`` are preserved.
    Blank lines and ``#`` comment lines inside the block are skipped without
    ending the block.  Any other non-list line terminates collection.
    """
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
                # Skip blank lines and comments without ending the block.
                continue
            item = re.match(r"^-\s+(.+)", stripped)
            if item:
                names.append(item.group(1).strip())
            else:
                # Non-list line (new YAML key or end of frontmatter) — stop.
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
        runtime_contract: dict[str, str] | None = None,
    ) -> None:
        self.path = path
        self.name = name
        self.layer = layer
        self.agents_list = agents_list
        self.runtime_contract = runtime_contract


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
    runtime_contract = _parse_runtime_contract(body)
    return AgentRecord(path, name, layer, agents_list, runtime_contract)


# ---------------------------------------------------------------------------
# Runtime-contract validation helper
# ---------------------------------------------------------------------------


def _check_runtime_contract(
    rec: AgentRecord, spec: dict, violations: list[str]
) -> None:
    """Append violations for any runtime-contract invariants that fail for *rec*."""
    contract = rec.runtime_contract
    if contract is None:
        violations.append(
            f"MISSING RUNTIME CONTRACT: {rec.path} | "
            f"stable agent '{rec.name}' has no runtime-contract comment"
        )
        return

    # Check required string-value fields.
    for field in ("version", "role", "layer", "accepts", "returns", "approval", "session", "trace"):
        expected = spec.get(field)
        if expected is None:
            continue
        got = contract.get(field)
        if got != expected:
            violations.append(
                f"RUNTIME CONTRACT FIELD: {rec.path} | "
                f"'{rec.name}' field '{field}': expected '{expected}', got '{got}'"
            )

    # Check required request fields.
    required_req: frozenset[str] = spec.get("request", frozenset())
    if required_req:
        declared_req = {f.strip() for f in contract.get("request", "").split(",") if f.strip()}
        missing = required_req - declared_req
        if missing:
            violations.append(
                f"RUNTIME CONTRACT REQUEST FIELDS: {rec.path} | "
                f"'{rec.name}' missing request fields: {', '.join(sorted(missing))}"
            )

    # Check required response fields.
    required_resp: frozenset[str] = spec.get("response", frozenset())
    if required_resp:
        declared_resp = {f.strip() for f in contract.get("response", "").split(",") if f.strip()}
        missing = required_resp - declared_resp
        if missing:
            violations.append(
                f"RUNTIME CONTRACT RESPONSE FIELDS: {rec.path} | "
                f"'{rec.name}' missing response fields: {', '.join(sorted(missing))}"
            )


def _check_layer_rules(
    rec: AgentRecord, name_to_layer: dict[str, int], violations: list[str]
) -> None:
    """Append violations for the base layer hierarchy rules for *rec*."""
    if rec.layer is None:
        violations.append(f"ORPHAN: {rec.path}")
        return

    if rec.name == "Atlas" and rec.layer != 0:
        violations.append(
            f"ATLAS LAYER ERROR: {rec.path} | expected layer 0, got {rec.layer}"
        )

    if rec.layer == 0:
        for agent_name in rec.agents_list:
            if name_to_layer.get(agent_name) == 2:
                violations.append(
                    f"L0→L2 VIOLATION: {rec.path} | "
                    f"L0 agent references L2 agent '{agent_name}'"
                )

    if rec.layer == 1:
        for agent_name in rec.agents_list:
            if name_to_layer.get(agent_name) == 0:
                violations.append(
                    f"L1→L0 VIOLATION: {rec.path} | "
                    f"L1 agent references L0 agent '{agent_name}'"
                )


def _check_stable_agent_completeness(
    records: list[AgentRecord], violations: list[str]
) -> None:
    """Require the full stable runtime set when any stable agent is present."""
    found_stable_names = {rec.name for rec in records if rec.name in _STABLE_RUNTIME_AGENTS}
    if not found_stable_names:
        return

    for expected_name in _STABLE_RUNTIME_AGENTS:
        if expected_name not in found_stable_names:
            violations.append(
                f"MISSING STABLE AGENT: '{expected_name}' not found in the provided input set"
            )


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
        _check_layer_rules(rec, name_to_layer, violations)
        if rec.name in _STABLE_RUNTIME_AGENTS:
            _check_runtime_contract(rec, _STABLE_RUNTIME_AGENTS[rec.name], violations)

    _check_stable_agent_completeness(records, violations)

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
        print("\nLAYER HIERARCHY FAILED")
        sys.exit(1)
    else:
        print(f"LAYER HIERARCHY OK ({len(files)} files scanned)")
        sys.exit(0)


if __name__ == "__main__":
    main()
