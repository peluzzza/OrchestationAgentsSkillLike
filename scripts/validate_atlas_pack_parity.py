"""Validate parity between the canonical root agents and the atlas-orchestration-team plugin mirror.

Rules enforced:

1. The shared surface (CANONICAL_SHARED, 19 files) must be present in both:
   - .github/agents/                           (canonical root)
   - plugins/atlas-orchestration-team/agents/  (plugin mirror)

2. The root-only compatibility aliases (ROOT_ONLY, 7 files) are explicitly
   allowed only in .github/agents/.  They must NOT appear in the mirror.

3. No extra agent files may exist in the mirror beyond CANONICAL_SHARED.

4. No extra agent files may exist in root beyond CANONICAL_SHARED | ROOT_ONLY.

5. Every mirrored file must contain a valid YAML frontmatter block.
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
MIRROR_AGENTS_DIR = (
    REPO_ROOT / "plugins" / "atlas-orchestration-team" / "agents"
)

# ---------------------------------------------------------------------------
# Canonical agent sets
# ---------------------------------------------------------------------------

# The 19 agent files shared between the canonical root and the plugin mirror.
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
# These live ONLY in .github/agents/ and must NOT appear in the plugin mirror.
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
    """Validate the root canonical agent set against the known surfaces."""
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


def check_mirror_agents(mirror_dir: Path) -> list[str]:
    """Validate the plugin mirror agent set and frontmatter."""
    errors: list[str] = []
    present = _collect_names(mirror_dir)

    # 1. Missing shared agents in mirror (content drift — absence side)
    for name in sorted(CANONICAL_SHARED):
        if name not in present:
            errors.append(f"mirror: shared agent missing -> {name}")

    # 2. Root-only aliases must NOT appear in the mirror
    for name in sorted(ROOT_ONLY):
        if name in present:
            errors.append(
                f"mirror: root-only alias must not be mirrored -> {name}"
            )

    # 3. Extra files in mirror not part of CANONICAL_SHARED (content drift — addition side)
    for name in sorted(present - CANONICAL_SHARED):
        errors.append(f"mirror: unexpected extra file -> {name}")

    # 4. Frontmatter sanity check for every present shared file
    for name in sorted(CANONICAL_SHARED & present):
        raw = (mirror_dir / name).read_text(encoding="utf-8")
        if not _FRONTMATTER_RE.match(_normalize(raw)):
            errors.append(
                f"mirror: {name}: missing or malformed frontmatter block"
            )

    return errors


def check_shared_content(root_dir: Path, mirror_dir: Path) -> list[str]:
    """Validate normalized content parity for all mirrored shared files."""
    errors: list[str] = []
    root_present = _collect_names(root_dir)
    mirror_present = _collect_names(mirror_dir)
    shared_present = CANONICAL_SHARED & root_present & mirror_present

    for name in sorted(shared_present):
        root_text = _normalized_text(root_dir / name)
        mirror_text = _normalized_text(mirror_dir / name)
        if root_text != mirror_text:
            errors.append(f"parity: content drift detected -> {name}")

    return errors


# ---------------------------------------------------------------------------
# Public entry point (also used by unit tests)
# ---------------------------------------------------------------------------


def run_checks(
    root_dir: Path = ROOT_AGENTS_DIR,
    mirror_dir: Path = MIRROR_AGENTS_DIR,
) -> list[str]:
    """Run all parity checks and return a flat list of error strings."""
    errors: list[str] = []
    errors.extend(check_root_agents(root_dir))
    errors.extend(check_mirror_agents(mirror_dir))
    errors.extend(check_shared_content(root_dir, mirror_dir))
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
        f"root={shared_n + root_only_n} agents "
        f"({shared_n} shared + {root_only_n} root-only), "
        f"mirror={shared_n} shared agents."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
