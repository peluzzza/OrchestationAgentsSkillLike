"""Tests for scripts/validate_layer_hierarchy.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Load module under test
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).resolve().parent
_MODULE_PATH = _SCRIPT_DIR / "validate_layer_hierarchy.py"

_SPEC = importlib.util.spec_from_file_location("validate_layer_hierarchy", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_vlh = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_vlh)  # type: ignore[union-attr]

validate = _vlh.validate
AgentRecord = _vlh.AgentRecord
_parse_agent = _vlh._parse_agent
_extract_layer_from_body = _vlh._extract_layer_from_body
_extract_agents_list = _vlh._extract_agents_list
REPO_ROOT = _vlh.REPO_ROOT


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_agent(
    tmp_path: Path,
    name: str,
    agent_name: str,
    layer_comment: str | None = None,
    agents: list[str] | None = None,
    extra_body: str = "",
) -> Path:
    path = tmp_path / name
    frontmatter_lines = [f"name: {agent_name}"]
    if agents:
        frontmatter_lines.append("agents:")
        for a in agents:
            frontmatter_lines.append(f"  - {a}")
    frontmatter = "\n".join(frontmatter_lines)

    layer_line = f"{layer_comment}\n" if layer_comment else ""
    content = f"---\n{frontmatter}\n---\n{layer_line}{extra_body}"
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Layer parsing
# ---------------------------------------------------------------------------


class TestLayerParsing:
    def test_layer_0_parsed(self, tmp_path: Path) -> None:
        """Agent with ``<!-- layer: 0 -->`` → parsed as layer 0."""
        p = _write_agent(tmp_path, "a.agent.md", "Atlas", "<!-- layer: 0 -->")
        rec = _parse_agent(p)
        assert rec.layer == 0

    def test_layer_1_with_domain(self, tmp_path: Path) -> None:
        """``<!-- layer: 1 | domain: Planning -->`` → parsed as layer 1."""
        p = _write_agent(tmp_path, "b.agent.md", "Prometheus", "<!-- layer: 1 | domain: Planning -->")
        rec = _parse_agent(p)
        assert rec.layer == 1

    def test_layer_2_with_parent(self, tmp_path: Path) -> None:
        """``<!-- layer: 2 | parent: X -->`` → parsed as layer 2."""
        p = _write_agent(tmp_path, "c.agent.md", "Backend-Atlas", "<!-- layer: 2 | parent: Sisyphus -->")
        rec = _parse_agent(p)
        assert rec.layer == 2

    def test_layer_1_alias(self, tmp_path: Path) -> None:
        """``<!-- layer: 1 | type: alias | delegates-to: Y -->`` → parsed as layer 1."""
        p = _write_agent(tmp_path, "d.agent.md", "Sisyphus-subagent", "<!-- layer: 1 | type: alias | delegates-to: Sisyphus -->")
        rec = _parse_agent(p)
        assert rec.layer == 1

    def test_no_layer_comment_returns_none(self, tmp_path: Path) -> None:
        """No layer comment → layer is None."""
        p = _write_agent(tmp_path, "e.agent.md", "Unknown")
        rec = _parse_agent(p)
        assert rec.layer is None

    def test_layer_comment_on_second_line_still_detected(self, tmp_path: Path) -> None:
        """Layer comment on second line after ``---`` → still detected."""
        p = tmp_path / "f.agent.md"
        p.write_text(
            "---\nname: F\n---\n\n<!-- layer: 1 | domain: Test -->\nBody.\n",
            encoding="utf-8",
        )
        rec = _parse_agent(p)
        assert rec.layer == 1

    def test_layer_comment_on_third_line_detected(self, tmp_path: Path) -> None:
        """Layer comment on third line after ``---`` → still detected."""
        p = tmp_path / "g.agent.md"
        p.write_text(
            "---\nname: G\n---\n\n\n<!-- layer: 2 | parent: X -->\nBody.\n",
            encoding="utf-8",
        )
        rec = _parse_agent(p)
        assert rec.layer == 2


# ---------------------------------------------------------------------------
# Orphan detection
# ---------------------------------------------------------------------------


class TestOrphanDetection:
    def test_missing_layer_creates_orphan_violation(self, tmp_path: Path) -> None:
        """Agent with no layer comment → ORPHAN violation."""
        p = _write_agent(tmp_path, "orphan.agent.md", "Wanderer")
        _, violations = validate([p])
        assert any("ORPHAN" in v and str(p) in v for v in violations)

    def test_multiple_orphans_all_reported(self, tmp_path: Path) -> None:
        """Multiple orphans are all reported."""
        p1 = _write_agent(tmp_path, "o1.agent.md", "Ghost1")
        p2 = _write_agent(tmp_path, "o2.agent.md", "Ghost2")
        _, violations = validate([p1, p2])
        assert len([v for v in violations if "ORPHAN" in v]) == 2


# ---------------------------------------------------------------------------
# Atlas-specific rules
# ---------------------------------------------------------------------------


class TestAtlasRules:
    def test_atlas_layer_0_valid(self, tmp_path: Path) -> None:
        """Atlas with ``<!-- layer: 0 -->`` → valid, no violation."""
        p = _write_agent(tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->")
        _, violations = validate([p])
        assert not any("ATLAS LAYER ERROR" in v for v in violations)

    def test_atlas_layer_1_violation(self, tmp_path: Path) -> None:
        """Atlas with ``<!-- layer: 1 -->`` → violation."""
        p = _write_agent(tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 1 -->")
        _, violations = validate([p])
        assert any("ATLAS LAYER ERROR" in v for v in violations)

    def test_atlas_agents_list_l1_only_no_violation(self, tmp_path: Path) -> None:
        """Atlas ``agents:`` list with only L1 agents → no L0→L2 violation."""
        l1a = _write_agent(tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 | domain: Planning -->")
        l1b = _write_agent(tmp_path, "Sisyphus.agent.md", "Sisyphus", "<!-- layer: 1 | domain: Implementation -->")
        atlas = _write_agent(
            tmp_path,
            "Atlas.agent.md",
            "Atlas",
            "<!-- layer: 0 -->",
            agents=["Prometheus", "Sisyphus"],
        )
        _, violations = validate([atlas, l1a, l1b])
        assert not any("L0→L2" in v for v in violations)

    def test_atlas_agents_list_with_l2_agent_violation(self, tmp_path: Path) -> None:
        """Atlas ``agents:`` list containing a known L2 agent name → violation."""
        l2 = _write_agent(tmp_path, "Backend-Atlas.agent.md", "Backend-Atlas", "<!-- layer: 2 | parent: Sisyphus -->")
        atlas = _write_agent(
            tmp_path,
            "Atlas.agent.md",
            "Atlas",
            "<!-- layer: 0 -->",
            agents=["Backend-Atlas"],
        )
        _, violations = validate([atlas, l2])
        assert any("L0→L2" in v and "Backend-Atlas" in v for v in violations)


# ---------------------------------------------------------------------------
# L1 rules
# ---------------------------------------------------------------------------


class TestL1Rules:
    def test_l1_referencing_l0_is_violation(self, tmp_path: Path) -> None:
        """L1 agent's ``agents:`` referencing an L0 agent → L1→L0 violation."""
        l0 = _write_agent(tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->")
        l1 = _write_agent(
            tmp_path,
            "Prometheus.agent.md",
            "Prometheus",
            "<!-- layer: 1 | domain: Planning -->",
            agents=["Atlas"],
        )
        _, violations = validate([atlas := l0, l1])
        assert any("L1→L0" in v for v in violations)

    def test_non_atlas_l0_agent_normal(self, tmp_path: Path) -> None:
        """A non-Atlas L0 agent (rare) should not trigger the Atlas-name rule."""
        p = _write_agent(tmp_path, "Conductor.agent.md", "Conductor", "<!-- layer: 0 -->")
        _, violations = validate([p])
        assert not any("ATLAS LAYER ERROR" in v for v in violations)

    def test_alias_with_correct_layer_valid(self, tmp_path: Path) -> None:
        """Alias agent at layer 1 with correct comment → no orphan."""
        p = _write_agent(
            tmp_path,
            "Sisyphus-subagent.agent.md",
            "Sisyphus-subagent",
            "<!-- layer: 1 | type: alias | delegates-to: Sisyphus -->",
        )
        _, violations = validate([p])
        assert not any("ORPHAN" in v for v in violations)

    def test_l1_referencing_l2_no_violation(self, tmp_path: Path) -> None:
        """L1 agent referencing L2 is allowed (normal delegation path)."""
        l2 = _write_agent(tmp_path, "Backend-Atlas.agent.md", "Backend-Atlas", "<!-- layer: 2 | parent: Sisyphus -->")
        l1 = _write_agent(
            tmp_path,
            "Sisyphus.agent.md",
            "Sisyphus",
            "<!-- layer: 1 | domain: Implementation -->",
            agents=["Backend-Atlas"],
        )
        _, violations = validate([l1, l2])
        assert not any("L1→L0" in v or "L0→L2" in v for v in violations)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_file_no_crash(self, tmp_path: Path) -> None:
        """Empty file → no crash, treated as ORPHAN."""
        p = tmp_path / "empty.agent.md"
        p.write_text("", encoding="utf-8")
        records, violations = validate([p])
        assert isinstance(violations, list)
        assert any("ORPHAN" in v for v in violations)

    def test_only_opening_fence_no_crash(self, tmp_path: Path) -> None:
        """File with only opening ``---`` (no closing) → no crash."""
        p = tmp_path / "partial.agent.md"
        p.write_text("---\nname: Ghost\n", encoding="utf-8")
        records, violations = validate([p])
        assert isinstance(violations, list)

    def test_layer_3_unknown_treated_as_valid_layer(self, tmp_path: Path) -> None:
        """Layer 3 is unusual but should not crash — only orphan check matters."""
        p = _write_agent(tmp_path, "deep.agent.md", "Deep", "<!-- layer: 3 | parent: X -->")
        records, violations = validate([p])
        # Should not be flagged as ORPHAN since it has a layer comment.
        assert not any("ORPHAN" in v for v in violations)

    def test_records_returned_for_each_file(self, tmp_path: Path) -> None:
        """``validate`` returns one record per input file."""
        p1 = _write_agent(tmp_path, "a.agent.md", "A", "<!-- layer: 1 -->")
        p2 = _write_agent(tmp_path, "b.agent.md", "B", "<!-- layer: 2 -->")
        records, _ = validate([p1, p2])
        assert len(records) == 2

    def test_validate_empty_list(self) -> None:
        """``validate([])`` returns empty records and violations."""
        records, violations = validate([])
        assert records == []
        assert violations == []

    def test_bom_crlf_file_parsed(self, tmp_path: Path) -> None:
        """BOM + CRLF line endings handled without crash."""
        p = tmp_path / "bom.agent.md"
        p.write_bytes(
            "\ufeff---\r\nname: BOM\r\n---\r\n<!-- layer: 1 -->\r\nBody.\r\n".encode("utf-8")
        )
        rec = _parse_agent(p)
        assert rec.layer == 1

    def test_name_extracted_correctly(self, tmp_path: Path) -> None:
        """Agent name is extracted from frontmatter."""
        p = _write_agent(tmp_path, "x.agent.md", "MyAgent", "<!-- layer: 1 -->")
        rec = _parse_agent(p)
        assert rec.name == "MyAgent"


# ---------------------------------------------------------------------------
# Real workspace scan (integration)
# ---------------------------------------------------------------------------


class TestRealWorkspace:
    def test_full_system_scan_no_orphans_no_violations(self) -> None:
        """Full workspace scan → 0 orphans, 0 violations (all agents have layer comments)."""
        from pathlib import Path as P

        root_dir = REPO_ROOT / ".github" / "agents"
        plugins_dir = REPO_ROOT / "plugins"

        files: list[Path] = []
        if root_dir.is_dir():
            files.extend(sorted(root_dir.glob("*.agent.md")))
        if plugins_dir.is_dir():
            files.extend(sorted(plugins_dir.rglob("*.agent.md")))

        assert files, "No agent files found — workspace path may be wrong"
        _, violations = validate(files)
        orphans = [v for v in violations if "ORPHAN" in v]
        assert orphans == [], f"Unexpected orphans: {orphans}"
        assert violations == [], f"Unexpected violations: {violations}"
