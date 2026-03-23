"""Tests for scripts/validate_tool_names.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Load the module under test via importlib so we do not rely on package install.
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).resolve().parent
_MODULE_PATH = _SCRIPT_DIR / "validate_tool_names.py"

_SPEC = importlib.util.spec_from_file_location("validate_tool_names", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None, (
    f"Cannot load validator from {_MODULE_PATH}"
)
_vtn = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_vtn)  # type: ignore[union-attr]


# Convenience aliases
validate_file = _vtn.validate_file
validate_all = _vtn.validate_all
VALID_TOOLS = _vtn.VALID_TOOLS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_agent(tmp_path: Path, name: str, frontmatter_body: str) -> Path:
    """Create a minimal *.agent.md file with the given frontmatter body."""
    path = tmp_path / name
    content = f"---\n{frontmatter_body}\n---\nSome body text.\n"
    path.write_text(content, encoding="utf-8")
    return path


def _write_inline_agents(tmp_path: Path, name: str, tools_inline: str) -> Path:
    path = tmp_path / name
    content = f"---\nname: Test\ntools: {tools_inline}\n---\nBody.\n"
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


class TestValidFile:
    def test_all_valid_tools_returns_no_violations(self, tmp_path: Path) -> None:
        """File with all valid tools → PASS (no violations)."""
        body = "name: MyAgent\ntools:\n  - agent\n  - search\n  - edit\n"
        path = _write_agent(tmp_path, "good.agent.md", body)
        assert validate_file(path) == []

    def test_full_valid_set_returns_no_violations(self, tmp_path: Path) -> None:
        """File with ALL valid tools → PASS."""
        tools_block = "\n".join(f"  - {t}" for t in sorted(VALID_TOOLS))
        body = f"name: FullAgent\ntools:\n{tools_block}\n"
        path = _write_agent(tmp_path, "full.agent.md", body)
        assert validate_file(path) == []

    def test_mcp_is_valid(self, tmp_path: Path) -> None:
        """``mcp`` is in the valid set → no violation."""
        body = "name: M\ntools:\n  - mcp\n"
        path = _write_agent(tmp_path, "mcp.agent.md", body)
        assert validate_file(path) == []

    def test_testFailure_is_valid(self, tmp_path: Path) -> None:
        """``testFailure`` is a valid tool name → no violation."""
        body = "name: T\ntools:\n  - testFailure\n"
        path = _write_agent(tmp_path, "tf.agent.md", body)
        assert validate_file(path) == []

    def test_empty_tools_block_passes(self, tmp_path: Path) -> None:
        """Empty tools: list → PASS (nothing to violate)."""
        body = "name: Empty\ntools:\n"
        path = _write_agent(tmp_path, "empty_tools.agent.md", body)
        assert validate_file(path) == []

    def test_no_tools_key_passes(self, tmp_path: Path) -> None:
        """File with no tools: key → PASS (skip silently)."""
        body = "name: NoTools\ndescription: hello\n"
        path = _write_agent(tmp_path, "no_tools.agent.md", body)
        assert validate_file(path) == []

    def test_inline_valid_tools_passes(self, tmp_path: Path) -> None:
        """Inline ``tools: ["agent", "search"]`` → PASS."""
        path = _write_inline_agents(tmp_path, "inline_ok.agent.md", '["agent", "search"]')
        assert validate_file(path) == []

    def test_comment_lines_in_tools_block_skipped(self, tmp_path: Path) -> None:
        """Lines starting with ``#`` inside tools block → skip, no violation."""
        body = "name: C\ntools:\n  - agent\n  # this is a comment\n  - edit\n"
        path = _write_agent(tmp_path, "comment.agent.md", body)
        assert validate_file(path) == []

    def test_agents_list_not_confused_with_tools(self, tmp_path: Path) -> None:
        """``agents:`` list entries (including slash names) must NOT trigger violations."""
        body = (
            "name: Atlas\n"
            "tools:\n"
            "  - agent\n"
            "agents:\n"
            "  - Backend-Atlas\n"
            "  - Data/Analyst\n"
        )
        path = _write_agent(tmp_path, "atlas_like.agent.md", body)
        assert validate_file(path) == []


class TestInvalidFile:
    def test_web_slash_fetch_fails(self, tmp_path: Path) -> None:
        """``web/fetch`` (slash notation) is invalid → FAIL."""
        body = "name: Bad\ntools:\n  - web/fetch\n"
        path = _write_agent(tmp_path, "bad_web_fetch.agent.md", body)
        violations = validate_file(path)
        assert len(violations) == 1
        assert "web/fetch" in violations[0]
        assert "INVALID" in violations[0]

    def test_execute_slash_runInTerminal_fails(self, tmp_path: Path) -> None:
        """``execute/runInTerminal`` → FAIL."""
        body = "name: Bad\ntools:\n  - execute/runInTerminal\n"
        path = _write_agent(tmp_path, "bad_run.agent.md", body)
        violations = validate_file(path)
        assert any("execute/runInTerminal" in v and "INVALID" in v for v in violations)

    def test_execute_slash_getTerminalOutput_fails(self, tmp_path: Path) -> None:
        """``execute/getTerminalOutput`` → FAIL."""
        body = "name: Bad\ntools:\n  - execute/getTerminalOutput\n"
        path = _write_agent(tmp_path, "bad_gto.agent.md", body)
        violations = validate_file(path)
        assert any("execute/getTerminalOutput" in v and "INVALID" in v for v in violations)

    def test_read_slash_terminalLastCommand_fails(self, tmp_path: Path) -> None:
        """``read/terminalLastCommand`` → FAIL."""
        body = "name: Bad\ntools:\n  - read/terminalLastCommand\n"
        path = _write_agent(tmp_path, "bad_tlc.agent.md", body)
        violations = validate_file(path)
        assert any("read/terminalLastCommand" in v and "INVALID" in v for v in violations)

    def test_read_slash_terminalSelection_fails(self, tmp_path: Path) -> None:
        """``read/terminalSelection`` → FAIL."""
        body = "name: Bad\ntools:\n  - read/terminalSelection\n"
        path = _write_agent(tmp_path, "bad_ts.agent.md", body)
        violations = validate_file(path)
        assert any("read/terminalSelection" in v and "INVALID" in v for v in violations)

    def test_read_slash_problems_fails(self, tmp_path: Path) -> None:
        """``read/problems`` is not the canonical ``problems`` tool → FAIL."""
        body = "name: Bad\ntools:\n  - read/problems\n"
        path = _write_agent(tmp_path, "bad_rp.agent.md", body)
        violations = validate_file(path)
        assert any("read/problems" in v and "INVALID" in v for v in violations)

    def test_search_slash_changes_fails(self, tmp_path: Path) -> None:
        """``search/changes`` → FAIL."""
        body = "name: Bad\ntools:\n  - search/changes\n"
        path = _write_agent(tmp_path, "bad_sc.agent.md", body)
        violations = validate_file(path)
        assert any("search/changes" in v and "INVALID" in v for v in violations)

    def test_runCommands_fails(self, tmp_path: Path) -> None:
        """``runCommands`` is not a valid tool name → FAIL."""
        body = "name: Bad\ntools:\n  - runCommands\n"
        path = _write_agent(tmp_path, "bad_rc.agent.md", body)
        violations = validate_file(path)
        assert any("runCommands" in v and "INVALID" in v for v in violations)

    def test_inline_invalid_tool_fails(self, tmp_path: Path) -> None:
        """Inline ``tools: ["agent", "web/fetch"]`` → FAIL."""
        path = _write_inline_agents(
            tmp_path, "inline_bad.agent.md", '["agent", "web/fetch"]'
        )
        violations = validate_file(path)
        assert any("web/fetch" in v and "INVALID" in v for v in violations)

    def test_multi_tool_only_bad_reported(self, tmp_path: Path) -> None:
        """Multi-tool file with one bad entry → report only the bad one."""
        body = (
            "name: M\n"
            "tools:\n"
            "  - agent\n"
            "  - search\n"
            "  - runCommands\n"
            "  - edit\n"
        )
        path = _write_agent(tmp_path, "multi.agent.md", body)
        violations = validate_file(path)
        assert len(violations) == 1
        assert "runCommands" in violations[0]


class TestEdgeCases:
    def test_empty_file_no_crash(self, tmp_path: Path) -> None:
        """Empty file → no crash, returns empty violations."""
        path = tmp_path / "empty.agent.md"
        path.write_text("", encoding="utf-8")
        violations = validate_file(path)
        assert isinstance(violations, list)

    def test_only_frontmatter_no_crash(self, tmp_path: Path) -> None:
        """File with only opening ``---`` and no closing fence → no crash."""
        path = tmp_path / "partial.agent.md"
        path.write_text("---\nname: Ghost\ntools:\n  - agent\n", encoding="utf-8")
        violations = validate_file(path)
        assert isinstance(violations, list)

    def test_agents_with_slash_names_no_violation(self, tmp_path: Path) -> None:
        """``agents:`` list with slash names must NOT trigger tool violations."""
        body = (
            "name: Atlas\n"
            "tools:\n"
            "  - agent\n"
            "agents:\n"
            "  - Backend/Specialist\n"
            "  - Data/Analyst\n"
        )
        path = _write_agent(tmp_path, "slash_agents.agent.md", body)
        assert validate_file(path) == []

    def test_bom_and_crlf_handled(self, tmp_path: Path) -> None:
        """UTF-8 BOM + CRLF line endings must be handled without error."""
        path = tmp_path / "bom.agent.md"
        content = "\ufeff---\r\nname: BOM\r\ntools:\r\n  - agent\r\n---\r\nBody.\r\n"
        path.write_bytes(content.encode("utf-8"))
        assert validate_file(path) == []

    def test_validate_all_aggregates_violations(self, tmp_path: Path) -> None:
        """``validate_all`` aggregates violations from multiple files."""
        good_body = "name: Good\ntools:\n  - agent\n"
        bad_body = "name: Bad\ntools:\n  - runCommands\n"
        good = _write_agent(tmp_path, "good.agent.md", good_body)
        bad = _write_agent(tmp_path, "bad.agent.md", bad_body)
        violations = validate_all([good, bad])
        assert len(violations) == 1
        assert "runCommands" in violations[0]

    def test_validate_all_empty_list(self) -> None:
        """``validate_all([])`` returns empty list without error."""
        assert validate_all([]) == []
