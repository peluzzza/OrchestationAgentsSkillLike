"""Validate parity between the canonical shared Atlas source pack and the root runtime surface.

Rules enforced:

1. The shared surface (CANONICAL_SHARED, 19 files) must be present in both:
    - plugins/atlas-orchestration-team/agents/  (canonical shared source)
    - .github/agents/                           (default-active root runtime)

2. The root-only compatibility aliases (ROOT_ONLY, 7 files) are explicitly
    allowed only in .github/agents/. They must NOT appear in the shared source.

3. No extra agent files may exist in the shared source beyond CANONICAL_SHARED.

4. No extra agent files may exist in root beyond CANONICAL_SHARED | ROOT_ONLY.

5. Every shared-source file must contain a valid YAML frontmatter block.
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
SOURCE_AGENTS_DIR = (
    REPO_ROOT / "plugins" / "atlas-orchestration-team" / "agents"
)

# ---------------------------------------------------------------------------
# Canonical agent sets
# ---------------------------------------------------------------------------

# The 19 agent files shared between the canonical source pack and the root runtime surface.
CANONICAL_SHARED: frozenset[str] = frozenset(
    {
        "Afrodita-UX.agent.md",
        "Argus.agent.md",
        "Ariadna.agent.md",
        "Atenea.agent.md",
        "Atlas.agent.md",
        "Clio.agent.md",
        "Hephaestus.agent.md",
        "Hermes.agent.md",
        "Oracle.agent.md",
        "Prometheus.agent.md",
        "Sisyphus.agent.md",
        "SpecifyAnalyze.agent.md",
        "SpecifyClarify.agent.md",
        "SpecifyConstitution.agent.md",
        "SpecifyImplement.agent.md",
        "SpecifyPlan.agent.md",
        "SpecifySpec.agent.md",
        "SpecifyTasks.agent.md",
        "Themis.agent.md",
    }
)

# The 7 root-only compatibility-alias files.
# These live ONLY in .github/agents/ and must NOT appear in the shared source pack.
ROOT_ONLY: frozenset[str] = frozenset(
    {
        "Afrodita-subagent.agent.md",
        "Argus-subagent.agent.md",
        "Hephaestus-subagent.agent.md",
        "Hermes-subagent.agent.md",
        "Oracle-subagent.agent.md",
        "Sisyphus-subagent.agent.md",
        "Themis-subagent.agent.md",
    }
)

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
    """Validate the default-active root runtime surface against the known surfaces."""
    errors: list[str] = []
    present = _collect_names(root_dir)
    expected = CANONICAL_SHARED | ROOT_ONLY

    for name in sorted(CANONICAL_SHARED):
        if name not in present:
            errors.append(f"root: shared agent missing -> {name}")

    for name in sorted(ROOT_ONLY):
        if name not in present:
            errors.append(f"root: root-only alias missing -> {name}")

    for name in sorted(present - expected):
        errors.append(
            f"root: unexpected file (not in shared or root-only) -> {name}"
        )

    return errors


def check_source_agents(source_dir: Path) -> list[str]:
    """Validate the canonical shared source pack and its frontmatter."""
    errors: list[str] = []
    present = _collect_names(source_dir)

    # 1. Missing shared agents in source (content drift — absence side)
    for name in sorted(CANONICAL_SHARED):
        if name not in present:
            errors.append(f"source: shared agent missing -> {name}")

    # 2. Root-only aliases must NOT appear in the source pack
    for name in sorted(ROOT_ONLY):
        if name in present:
            errors.append(
                f"source: root-only alias must not appear in source -> {name}"
            )

    # 3. Extra files in source not part of CANONICAL_SHARED (content drift — addition side)
    for name in sorted(present - CANONICAL_SHARED):
        errors.append(f"source: unexpected extra file -> {name}")

    # 4. Frontmatter sanity check for every present shared file
    for name in sorted(CANONICAL_SHARED & present):
        raw = (source_dir / name).read_text(encoding="utf-8")
        if not _FRONTMATTER_RE.match(_normalize(raw)):
            errors.append(
                f"source: {name}: missing or malformed frontmatter block"
            )

    return errors


def check_shared_content(root_dir: Path, source_dir: Path) -> list[str]:
    """Validate normalized content parity for all shared files copied from source into root."""
    errors: list[str] = []
    root_present = _collect_names(root_dir)
    source_present = _collect_names(source_dir)
    shared_present = CANONICAL_SHARED & root_present & source_present

    for name in sorted(shared_present):
        source_text = _normalized_text(source_dir / name)
        root_text = _normalized_text(root_dir / name)
        if source_text != root_text:
            errors.append(f"parity: root runtime drift detected from source -> {name}")

    return errors


# ---------------------------------------------------------------------------
# Public entry point (also used by unit tests)
# ---------------------------------------------------------------------------


def run_checks(
    root_dir: Path = ROOT_AGENTS_DIR,
    source_dir: Path = SOURCE_AGENTS_DIR,
) -> list[str]:
    """Run all parity checks and return a flat list of error strings."""
    errors: list[str] = []
    errors.extend(check_root_agents(root_dir))
    errors.extend(check_source_agents(source_dir))
    errors.extend(check_shared_content(root_dir, source_dir))
    return errors


def main() -> int:
    errors = run_checks()
    if errors:
        for err in errors:
            print(f"FAIL  {err}", file=sys.stderr)
        print(
            f"\n{len(errors)} parity error(s) found.",
            file=sys.stderr,
        )
        return 1
    shared_n = len(CANONICAL_SHARED)
    root_only_n = len(ROOT_ONLY)
    print(
        f"ATLAS PACK PARITY OK  "
        f"source={shared_n} shared agents, "
        f"root={shared_n + root_only_n} agents "
        f"({shared_n} synced shared + {root_only_n} root-only)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
