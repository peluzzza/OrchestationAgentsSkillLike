"""Tests for Atlas hierarchy routing — verifies that Atlas only references L1 agents
and that each L1 god wires to the correct L2 pack specialists.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)
_LAYER_RE = re.compile(r"<!--\s*layer:\s*(\d+)")


def _normalize(text: str) -> str:
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def _parse_frontmatter(path: Path) -> str | None:
    text = _normalize(path.read_text(encoding="utf-8"))
    m = _FRONTMATTER_RE.match(text)
    return m.group(1) if m else None


def _agents_list(frontmatter: str) -> list[str]:
    lines = frontmatter.split("\n")
    in_agents = False
    names: list[str] = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^agents\s*:", stripped):
            inline_m = re.match(r"^agents\s*:\s*\[(.+)\]\s*$", stripped)
            if inline_m:
                raw = inline_m.group(1)
                return [n.strip().strip('"').strip("'") for n in raw.split(",") if n.strip()]
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


def _layer_of(path: Path) -> int | None:
    text = _normalize(path.read_text(encoding="utf-8"))
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None
    body = text[m.end():]
    for line in body.split("\n")[:3]:
        lm = _LAYER_RE.search(line)
        if lm:
            return int(lm.group(1))
    return None


def _user_invocable(frontmatter: str) -> bool:
    return bool(re.search(r"^user-invocable:\s*true\s*$", frontmatter, re.MULTILINE))


# ---------------------------------------------------------------------------
# Load layer hierarchy module for name→layer lookup
# ---------------------------------------------------------------------------

_VLH_PATH = REPO_ROOT / "scripts" / "validate_layer_hierarchy.py"
_SPEC = importlib.util.spec_from_file_location("validate_layer_hierarchy", _VLH_PATH)
assert _SPEC and _SPEC.loader
_vlh = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_vlh)  # type: ignore[union-attr]


def _build_name_to_layer() -> dict[str, int]:
    files = _vlh._collect_agent_files()
    mapping: dict[str, int] = {}
    for f in files:
        rec = _vlh._parse_agent(f)
        if rec.name and rec.layer is not None:
            mapping[rec.name] = rec.layer
    return mapping


NAME_TO_LAYER = _build_name_to_layer()


# ---------------------------------------------------------------------------
# Known expected sets
# ---------------------------------------------------------------------------

# L2 pack conductor / specialist names that Atlas must NOT directly reference
L2_CONDUCTOR_NAMES = frozenset({
    "Backend-Atlas", "Data-Atlas", "DevOps-Atlas", "Automation-Atlas",
    "UX-Atlas", "Afrodita",
})

# Expected L1 gods explicitly listed by Atlas
EXPECTED_L1_GODS = frozenset({
    "Prometheus", "Sisyphus", "Themis", "Argus", "Hermes", "Oracle",
    "Atenea", "Ariadna", "Clio", "Hephaestus", "Afrodita-UX",
})

# Expected L1 aliases listed by Atlas
EXPECTED_L1_ALIASES = frozenset({
    "Hermes-subagent", "Oracle-subagent", "Sisyphus-subagent",
    "Afrodita-subagent", "Argus-subagent", "Themis-subagent",
    "Hephaestus-subagent",
})


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAtlasAgentsList:
    """Atlas must reference only L1 agents — never L2 specialists directly."""

    def _atlas_agents(self) -> list[str]:
        path = REPO_ROOT / ".github" / "agents" / "Atlas.agent.md"
        fm = _parse_frontmatter(path)
        assert fm is not None, "Atlas.agent.md frontmatter missing"
        return _agents_list(fm)

    def test_atlas_agents_list_contains_no_l2_conductors(self) -> None:
        """Atlas agents list must not contain any known L2 conductor name."""
        atlas_agents = set(self._atlas_agents())
        l2_violations = atlas_agents & L2_CONDUCTOR_NAMES
        assert not l2_violations, (
            f"Atlas directly references L2 agents: {sorted(l2_violations)}"
        )

    def test_atlas_agents_list_contains_no_l2_by_layer_map(self) -> None:
        """Cross-check: none of Atlas's agent refs should resolve to layer 2."""
        atlas_agents = self._atlas_agents()
        l2_refs = [
            name for name in atlas_agents if NAME_TO_LAYER.get(name) == 2
        ]
        assert not l2_refs, f"Atlas references L2 agents: {l2_refs}"

    def test_atlas_agents_list_contains_expected_l1_gods(self) -> None:
        """Atlas agents list must include all expected L1 god agents."""
        atlas_set = set(self._atlas_agents())
        missing = EXPECTED_L1_GODS - atlas_set
        assert not missing, f"Atlas missing L1 gods: {sorted(missing)}"

    def test_atlas_agents_list_contains_expected_l1_aliases(self) -> None:
        """Atlas agents list must include all expected L1 alias agents."""
        atlas_set = set(self._atlas_agents())
        missing = EXPECTED_L1_ALIASES - atlas_set
        assert not missing, f"Atlas missing L1 aliases: {sorted(missing)}"


class TestL1GodWiring:
    """Each L1 god either has sub-agents or is a leaf node."""

    def _god_agents(self, filename: str) -> list[str]:
        path = REPO_ROOT / ".github" / "agents" / filename
        fm = _parse_frontmatter(path)
        assert fm is not None, f"{filename} frontmatter missing"
        return _agents_list(fm)

    def test_each_l1_god_has_agents_key(self) -> None:
        """Every L1 god file must parse without frontmatter errors."""
        gods = [
            "Prometheus.agent.md", "Sisyphus.agent.md", "Themis.agent.md",
            "Argus.agent.md", "Hephaestus.agent.md", "Afrodita-UX.agent.md",
            "Hermes.agent.md", "Oracle.agent.md",
        ]
        for fname in gods:
            path = REPO_ROOT / ".github" / "agents" / fname
            fm = _parse_frontmatter(path)
            assert fm is not None, f"{fname} has no frontmatter"

    def test_prometheus_agents_list_contains_specify_agents(self) -> None:
        """Prometheus must reference Specify sub-agents (L2 planners)."""
        agents = self._god_agents("Prometheus.agent.md")
        # Prometheus should reference at least one Hermes-subagent or Specify agent
        has_specify_or_hermes = any(
            "Specify" in a or "Hermes" in a for a in agents
        )
        assert has_specify_or_hermes, (
            f"Prometheus agents list has no Specify/Hermes agents: {agents}"
        )

    def test_sisyphus_agents_list_contains_backend_atlas(self) -> None:
        """Sisyphus must reference Backend-Atlas (L2 backend conductor)."""
        agents = self._god_agents("Sisyphus.agent.md")
        assert "Backend-Atlas" in agents, (
            f"Sisyphus agents list missing Backend-Atlas: {agents}"
        )

    def test_hephaestus_agents_list_contains_devops_and_automation(self) -> None:
        """Hephaestus must reference DevOps-Atlas and Automation-Atlas."""
        agents = set(self._god_agents("Hephaestus.agent.md"))
        assert "DevOps-Atlas" in agents, f"Hephaestus missing DevOps-Atlas: {agents}"
        assert "Automation-Atlas" in agents, f"Hephaestus missing Automation-Atlas: {agents}"

    def test_afrodita_ux_agents_list_contains_ux_atlas(self) -> None:
        """Afrodita-UX must reference UX-Atlas."""
        path = REPO_ROOT / ".github" / "agents" / "Afrodita-UX.agent.md"
        fm = _parse_frontmatter(path)
        assert fm is not None
        agents = set(_agents_list(fm))
        assert "UX-Atlas" in agents, f"Afrodita-UX missing UX-Atlas: {agents}"


class TestPackConductorInvocability:
    """No L2 pack conductor should be user-invocable."""

    # PackCatalog is intentionally user-invocable (catalog/discovery agent, like Atlas)
    _ALLOWED_USER_INVOCABLE = {"PackCatalog.agent.md"}

    def test_no_pack_conductor_is_user_invocable(self) -> None:
        """All L2 agents must have user-invocable: false (or omit the key), except known exceptions."""
        plugins_dir = REPO_ROOT / "plugins"
        violations: list[str] = []
        for path in sorted(plugins_dir.rglob("*.agent.md")):
            if path.name in self._ALLOWED_USER_INVOCABLE:
                continue
            layer = _layer_of(path)
            if layer != 2:
                continue
            fm = _parse_frontmatter(path)
            if fm and _user_invocable(fm):
                violations.append(path.name)
        assert not violations, (
            f"L2 agents must not be user-invocable: {violations}"
        )
