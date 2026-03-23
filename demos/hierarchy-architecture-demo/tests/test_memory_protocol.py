"""
test_memory_protocol.py — Verify the 3-level memory system is configured.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


class TestMCPConfiguration:
    """MCP memory server must be configured."""

    def test_vscode_mcp_json_exists(self) -> None:
        mcp_path = REPO_ROOT / ".vscode" / "mcp.json"
        assert mcp_path.exists(), ".vscode/mcp.json not found"

    def test_vscode_mcp_json_is_valid_json(self) -> None:
        mcp_path = REPO_ROOT / ".vscode" / "mcp.json"
        content = mcp_path.read_text(encoding="utf-8-sig")
        parsed = json.loads(content)
        assert isinstance(parsed, dict), "mcp.json must be a JSON object"

    def test_mcp_json_contains_memory_server(self) -> None:
        mcp_path = REPO_ROOT / ".vscode" / "mcp.json"
        content = mcp_path.read_text(encoding="utf-8-sig")
        assert "@modelcontextprotocol/server-memory" in content, (
            "mcp.json must reference @modelcontextprotocol/server-memory"
        )

    def test_mcp_json_has_servers_key(self) -> None:
        mcp_path = REPO_ROOT / ".vscode" / "mcp.json"
        parsed = json.loads(mcp_path.read_text(encoding="utf-8-sig"))
        assert "servers" in parsed, "mcp.json must have a 'servers' key"


class TestMemoryGuardianAgent:
    """Memory-Guardian agent must exist with correct configuration."""

    def _get_guardian_path(self) -> Path:
        return REPO_ROOT / "plugins" / "memory-system" / "agents" / "Memory-Guardian.agent.md"

    def test_memory_guardian_exists(self) -> None:
        assert self._get_guardian_path().exists(), "Memory-Guardian.agent.md not found"

    def test_memory_guardian_has_mcp_tool(self) -> None:
        content = self._get_guardian_path().read_text(encoding="utf-8-sig", errors="replace")
        fm_match = re.search(r"^---\n(.+?)^---", content, re.DOTALL | re.MULTILINE)
        assert fm_match, "Could not parse Memory-Guardian frontmatter"
        fm = fm_match.group(1)
        assert "mcp" in fm, "Memory-Guardian must have 'mcp' in its tools list"

    def test_memory_guardian_is_not_user_invocable(self) -> None:
        content = self._get_guardian_path().read_text(encoding="utf-8-sig", errors="replace")
        assert "user-invocable: false" in content, (
            "Memory-Guardian must be user-invocable: false"
        )


class TestMemorySystemPack:
    """memory-system pack must be properly structured."""

    def test_memory_system_readme_exists(self) -> None:
        readme = REPO_ROOT / "plugins" / "memory-system" / "README.md"
        assert readme.exists(), "plugins/memory-system/README.md not found"

    def test_memory_system_registered_in_pack_registry(self) -> None:
        registry_path = REPO_ROOT / ".github" / "plugin" / "pack-registry.json"
        content = registry_path.read_text(encoding="utf-8", errors="replace")
        parsed = json.loads(content)
        ids = [p["id"] for p in parsed.get("packs", [])]
        assert "memory-system" in ids, "memory-system pack not found in pack-registry.json"
