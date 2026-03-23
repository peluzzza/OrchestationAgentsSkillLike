"""Validate completeness of .github/agents/ — the single source of truth for all agents.

Rules enforced:

1. Every agent in ALL_AGENTS must be present in .github/agents/.

2. No files outside of ALL_AGENTS may exist in .github/agents/.

3. Every agent file must contain a valid YAML frontmatter block.
   CRLF line endings and UTF-8 BOM markers are normalised before the check.

Usage::

    python3 scripts/validate_atlas_pack_parity.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

ROOT_AGENTS_DIR = REPO_ROOT / ".github" / "agents"

# ---------------------------------------------------------------------------
# Canonical agent set — ALL 79 agents that must live in .github/agents/
# ---------------------------------------------------------------------------

ALL_AGENTS: frozenset[str] = frozenset(
    {
        # Layer 0 — Conductor
        "Atlas.agent.md",
        # Layer 1 — Domain gods
        "Afrodita-UX.agent.md",
        "Argus.agent.md",
        "Ariadna.agent.md",
        "Atenea.agent.md",
        "Clio.agent.md",
        "Hephaestus.agent.md",
        "Hermes.agent.md",
        "Oracle.agent.md",
        "Prometheus.agent.md",
        "Sisyphus.agent.md",
        "Themis.agent.md",
        # Layer 1 — Compatibility aliases
        "Afrodita-subagent.agent.md",
        "Argus-subagent.agent.md",
        "Hephaestus-subagent.agent.md",
        "Hermes-subagent.agent.md",
        "Oracle-subagent.agent.md",
        "Sisyphus-subagent.agent.md",
        "Themis-subagent.agent.md",
        # Specify pipeline
        "SpecifyAnalyze.agent.md",
        "SpecifyClarify.agent.md",
        "SpecifyConstitution.agent.md",
        "SpecifyImplement.agent.md",
        "SpecifyPlan.agent.md",
        "SpecifySpec.agent.md",
        "SpecifyTasks.agent.md",
        # Layer 2 — Backend specialists
        "API-Designer.agent.md",
        "Backend-Atlas.agent.md",
        "Backend-Planner.agent.md",
        "Backend-Reviewer.agent.md",
        "Database-Engineer.agent.md",
        "Performance-Tuner.agent.md",
        "Security-Guard.agent.md",
        "Service-Builder.agent.md",
        # Layer 2 — Data specialists
        "Analytics-Engineer.agent.md",
        "Data-Architect.agent.md",
        "Data-Atlas.agent.md",
        "Data-Planner.agent.md",
        "Data-Quality.agent.md",
        "Data-Reviewer.agent.md",
        "ML-Scientist.agent.md",
        "Pipeline-Builder.agent.md",
        # Layer 2 — DevOps specialists
        "Container-Master.agent.md",
        "Cost-Optimizer.agent.md",
        "Deploy-Strategist.agent.md",
        "DevOps-Atlas.agent.md",
        "DevOps-Planner.agent.md",
        "Incident-Responder.agent.md",
        "Infra-Architect.agent.md",
        "Monitor-Sentinel.agent.md",
        "Pipeline-Engineer.agent.md",
        "Security-Ops.agent.md",
        # Layer 2 — Frontend/UX specialists
        "A11y-Auditor.agent.md",
        "Accessibility-Heuristics.agent.md",
        "Afrodita.agent.md",
        "Component-Builder.agent.md",
        "Design-Critic.agent.md",
        "Frontend-Handoff.agent.md",
        "Frontend-Planner.agent.md",
        "Frontend-Reviewer.agent.md",
        "State-Manager.agent.md",
        "Style-Engineer.agent.md",
        "UI-Designer.agent.md",
        "UX-Atlas.agent.md",
        "UX-Planner.agent.md",
        "User-Flow-Designer.agent.md",
        # Layer 2 — Automation/MCP specialists
        "Automation-Atlas.agent.md",
        "Automation-Planner.agent.md",
        "Automation-Reviewer.agent.md",
        "MCP-Integrator.agent.md",
        "Workflow-Composer.agent.md",
        "n8n-Connector.agent.md",
        # Layer 2 — QA specialists
        "Coverage-Analyst.agent.md",
        "Mutation-Tester.agent.md",
        "Test-Runner.agent.md",
        # Layer 2 — Security specialists
        "Compliance-Checker.agent.md",
        "Secret-Scanner.agent.md",
        # Utility
        "Memory-Guardian.agent.md",
        "PackCatalog.agent.md",
    }
)

# Keep these names for backwards-compat with any external tooling
CANONICAL_SHARED = ALL_AGENTS
ROOT_ONLY: frozenset[str] = frozenset()

# Frontmatter pattern — tolerant of leading BOM and CRLF line endings.
_FRONTMATTER_RE = re.compile(
    r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize(text: str) -> str:
    """Strip UTF-8 BOM and normalise CRLF / bare CR to LF."""
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def _normalized_text(path: Path) -> str:
    """Read and normalize text from *path* for parity comparison."""
    return _normalize(path.read_text(encoding="utf-8"))


def _collect_names(directory: Path) -> frozenset[str]:
    """Return the set of ``*.agent.md`` filenames in *directory*."""
    return frozenset(p.name for p in directory.glob("*.agent.md"))


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def check_root_agents(root_dir: Path) -> list[str]:
    """Validate .github/agents/ contains all expected agents and nothing extra."""
    errors: list[str] = []
    present = _collect_names(root_dir)

    for name in sorted(ALL_AGENTS):
        if name not in present:
            errors.append(f"root: agent missing -> {name}")

    for name in sorted(present - ALL_AGENTS):
        errors.append(f"root: unexpected file -> {name}")

    # Frontmatter sanity check for every present agent file
    for name in sorted(ALL_AGENTS & present):
        raw = (root_dir / name).read_text(encoding="utf-8")
        if not _FRONTMATTER_RE.match(_normalize(raw)):
            errors.append(f"root: {name}: missing or malformed frontmatter block")

    return errors


def check_source_agents(source_dir: Path) -> list[str]:  # noqa: ARG001
    """Kept for backwards-compat — source pack no longer exists, always returns []."""
    return []


def check_shared_content(root_dir: Path, source_dir: Path) -> list[str]:  # noqa: ARG001
    """Kept for backwards-compat — source pack no longer exists, always returns []."""
    return []


# ---------------------------------------------------------------------------
# Public entry point (also used by unit tests)
# ---------------------------------------------------------------------------


def run_checks(
    root_dir: Path = ROOT_AGENTS_DIR,
    source_dir: Path | None = None,  # kept for backwards-compat, ignored
) -> list[str]:
    """Run all agent completeness checks and return a flat list of error strings."""
    return check_root_agents(root_dir)


def main() -> int:
    errors = run_checks()
    if errors:
        for err in errors:
            print(f"FAIL  {err}", file=sys.stderr)
        print(
            f"\n{len(errors)} error(s) found.",
            file=sys.stderr,
        )
        return 1
    total_n = len(ALL_AGENTS)
    print(f"ALL AGENTS OK  {total_n} agents present in .github/agents/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
