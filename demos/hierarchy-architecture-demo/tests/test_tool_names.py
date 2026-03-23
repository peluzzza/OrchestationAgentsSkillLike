"""
test_tool_names.py — Verify no invalid tool names exist in any agent file.
Uses the validate_tool_names script to scan the workspace.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = str(REPO_ROOT / "scripts" / "validate_tool_names.py")


def _run_validator(*extra_args: str) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, VALIDATOR, *extra_args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    return result.returncode, (result.stdout + result.stderr).strip()


class TestToolNamesValidation:
    """validate_tool_names.py must pass for all major agent directories."""

    def test_github_agents_directory_is_clean(self) -> None:
        code, output = _run_validator(str(REPO_ROOT / ".github" / "agents"))
        assert code == 0, f"Tool name violations in .github/agents/:\n{output}"

    def test_atlas_orchestration_team_is_clean(self) -> None:
        pack_dir = REPO_ROOT / "plugins" / "atlas-orchestration-team" / "agents"
        code, output = _run_validator(str(pack_dir))
        assert code == 0, f"Tool name violations in atlas-orchestration-team:\n{output}"

    def test_backend_workflow_is_clean(self) -> None:
        pack_dir = REPO_ROOT / "plugins" / "backend-workflow" / "agents"
        code, output = _run_validator(str(pack_dir))
        assert code == 0, f"Tool name violations in backend-workflow:\n{output}"

    def test_automation_mcp_workflow_is_clean(self) -> None:
        pack_dir = REPO_ROOT / "plugins" / "automation-mcp-workflow" / "agents"
        code, output = _run_validator(str(pack_dir))
        assert code == 0, f"Tool name violations in automation-mcp-workflow:\n{output}"

    def test_full_workspace_exits_zero(self) -> None:
        code, output = _run_validator()
        assert code == 0, f"Tool name violations found across workspace:\n{output}"
