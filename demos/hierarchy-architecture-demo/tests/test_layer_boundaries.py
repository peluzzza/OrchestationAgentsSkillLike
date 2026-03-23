"""
test_layer_boundaries.py — Verify the 3-layer agent hierarchy boundaries.
Requires: validate_layer_hierarchy.py in the scripts/ directory.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_layer_hierarchy as vlh  # type: ignore[import-not-found]


def _get_records_for_dir(target: Path, recursive: bool = False) -> list[vlh.AgentRecord]:
    if recursive:
        files = sorted(target.rglob("*.agent.md"))
    else:
        files = sorted(target.glob("*.agent.md"))
    return [vlh._parse_agent(f) for f in files]


class TestOrphanFreeWorkspace:
    """Every agent file must have a layer comment."""

    def test_no_orphans_in_github_agents(self) -> None:
        github_agents = REPO_ROOT / ".github" / "agents"
        records = _get_records_for_dir(github_agents)
        orphans = [r.path.name for r in records if r.layer is None]
        assert not orphans, f"Orphan agents in .github/agents/: {orphans}"

    def test_no_orphans_in_plugins(self) -> None:
        plugins_dir = REPO_ROOT / "plugins"
        records = _get_records_for_dir(plugins_dir, recursive=True)
        orphans = [r.path.name for r in records if r.layer is None]
        assert not orphans, f"Orphan agents in plugins/: {orphans}"


class TestLayerZero:
    """Atlas must be the only layer-0 agent."""

    def test_atlas_is_the_only_l0_agent(self) -> None:
        agents_dir = REPO_ROOT / ".github" / "agents"
        records = _get_records_for_dir(agents_dir)
        l0 = [r.path.name for r in records if r.layer == 0]
        assert l0 == ["Atlas.agent.md"], (
            f"Expected only Atlas.agent.md at layer 0, got: {l0}"
        )

    def test_no_plugin_agent_is_l0(self) -> None:
        plugins_dir = REPO_ROOT / "plugins"
        records = _get_records_for_dir(plugins_dir, recursive=True)
        # Atlas.agent.md in plugins/atlas-orchestration-team/ is a canonical source copy — allowed
        l0 = [r.path.name for r in records if r.layer == 0 and r.path.name != "Atlas.agent.md"]
        assert not l0, f"No plugin agent (other than canonical Atlas copy) should be layer 0, found: {l0}"


class TestLayerOneCounts:
    """Layer-1 agents (gods + aliases) must meet minimum count requirements."""

    def test_l1_total_at_least_18(self) -> None:
        """11 canonical gods + 7 aliases = 18 minimum."""
        agents_dir = REPO_ROOT / ".github" / "agents"
        records = _get_records_for_dir(agents_dir)
        l1 = [r for r in records if r.layer == 1]
        assert len(l1) >= 18, f"Expected ≥18 layer-1 agents in .github/agents, got {len(l1)}"

    def test_l1_canonical_gods_present(self) -> None:
        expected_gods = {
            "Prometheus.agent.md", "Sisyphus.agent.md", "Themis.agent.md",
            "Argus.agent.md", "Hermes.agent.md", "Oracle.agent.md",
            "Atenea.agent.md", "Ariadna.agent.md", "Clio.agent.md",
            "Hephaestus.agent.md", "Afrodita-UX.agent.md",
        }
        agents_dir = REPO_ROOT / ".github" / "agents"
        records = _get_records_for_dir(agents_dir)
        l1_files = {r.path.name for r in records if r.layer == 1}
        missing = expected_gods - l1_files
        assert not missing, f"Missing canonical gods at layer 1: {missing}"


class TestLayerTwoCounts:
    """Layer-2 specialist agents must meet minimum count requirements."""

    def test_l2_total_at_least_30(self) -> None:
        plugins_dir = REPO_ROOT / "plugins"
        records = _get_records_for_dir(plugins_dir, recursive=True)
        l2 = [r for r in records if r.layer == 2]
        assert len(l2) >= 30, (
            f"Expected ≥30 layer-2 specialists in plugins/, got {len(l2)}"
        )


class TestRootAtlasAgentsList:
    """Atlas agents: list must not reference layer-0 agents in a loop."""

    def test_atlas_agents_list_does_not_contain_atlas(self) -> None:
        atlas_path = REPO_ROOT / ".github" / "agents" / "Atlas.agent.md"
        record = vlh._parse_agent(atlas_path)
        assert "Atlas" not in record.agents_list, "Atlas should not reference itself"
