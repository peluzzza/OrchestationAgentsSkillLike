## Phase 5 Complete: Clean Parity And Catalog Surface

This phase delivered parity tooling and catalog-metadata hygiene for the `atlas-orchestration-team` plugin pack. The canonical `.github/agents` root remains unchanged; all changes are additive or documentation-level.

**Files:**
- `scripts/validate_atlas_pack_parity.py` (new)
- `scripts/test_validate_atlas_pack_parity.py` (new)
- `plugins/atlas-orchestration-team/.github/plugin/plugin.json` (description updated)
- `.github/plugin/marketplace.json` (atlas-orchestration-team description updated)
- `plans/external-ecosystem-orchestration-merge-phase-5-complete.md` (this file)

**Implementation Scope:**

1. **`scripts/validate_atlas_pack_parity.py`** — stdlib-only parity validator.
   - Defines two explicit constants: `CANONICAL_SHARED` (19 shared agent filenames) and `ROOT_ONLY` (7 root-only compatibility-alias filenames).
   - `check_root_agents()` — enforces that root contains exactly `CANONICAL_SHARED ∪ ROOT_ONLY`; flags missing or unexpected files.
   - `check_mirror_agents()` — enforces that the plugin mirror contains exactly `CANONICAL_SHARED`; flags missing agents, extra files, root-only aliases leaking into the mirror, and agent files with missing/malformed YAML frontmatter.
   - `check_shared_content()` — compares normalized canonical-vs-mirror content for all mirrored shared agents and flags any true drift.
   - CRLF line endings and UTF-8 BOM markers are normalised before both frontmatter checks and content-parity comparisons so Windows-edited files do not produce false positives.
   - `run_checks()` is the parameterised public function used by both `main()` and the unit tests.

2. **`scripts/test_validate_atlas_pack_parity.py`** — 30 unit tests via `unittest` (stdlib only).
   - Module loaded via `importlib.util` (consistent with existing test conventions in this repo).
   - Coverage: `_normalize`, `_normalized_text`, `_collect_names`, `check_root_agents`, `check_mirror_agents`, `check_shared_content`, `run_checks`.
   - Key failure scenarios tested: missing shared agent (root and mirror), missing root-only alias, extra unexpected file in root, extra file in mirror, all 7 root-only aliases blocked from mirror, malformed frontmatter, CRLF, BOM, CRLF+BOM combined, content drift, and BOM/CRLF-only equivalence.

3. **Manifest wording** — `plugin.json` and `marketplace.json` descriptions updated to state explicitly that `atlas-orchestration-team` is the *optional distribution mirror* of the canonical root Atlas pack, and that `.github/agents` remains authoritative.

4. **Mirror resynchronization** — 11 shared mirrored agents were synced from `.github/agents/` into `plugins/atlas-orchestration-team/agents/` after the new parity validator surfaced real drift. This makes the optional pack an actual mirror again instead of a nostalgic approximation.

**Agent surface summary:**
| Surface | Count | Location |
|---|---|---|
| Canonical root agents | 26 | `.github/agents/` |
| Shared (mirrored) agents | 19 | `.github/agents/` + `plugins/atlas-orchestration-team/agents/` |
| Root-only compatibility aliases | 7 | `.github/agents/` only |
| Plugin mirror agents | 19 | `plugins/atlas-orchestration-team/agents/` only |

**Root-only aliases (explicitly allowed, never mirrored):**
`Afrodita-subagent`, `Argus-subagent`, `Hephaestus-subagent`, `Hermes-subagent`, `Oracle-subagent`, `Sisyphus-subagent`, `Themis-subagent`

**Review:** APPROVED
**Testing (Argus):** PASSED

- `python3 scripts/validate_plugin_packs.py` → `PLUGIN PACK VALIDATION OK (4 marketplace entries checked)`
- `python3 scripts/validate_optional_pack_demos.py` → `OPTIONAL PACK DEMO VALIDATION OK (2 demos checked)`
- `python3 scripts/validate_atlas_pack_parity.py` → `ATLAS PACK PARITY OK  root=26 agents (19 shared + 7 root-only), mirror=19 shared agents.`
- `python3 -m unittest -v scripts/test_validate_atlas_pack_parity.py` → `Ran 30 tests in 0.042s  OK`

**Deployment (Hephaestus):** N/A
- Plugin/documentation/validator-only phase; no runtime deployment surface changed.

**Git Commit:**
```
feat: add atlas pack parity validator and refresh catalog metadata (phase 5)

- add scripts/validate_atlas_pack_parity.py (19 shared + 7 root-only, normalized content parity, frontmatter, CRLF/BOM)
- add scripts/test_validate_atlas_pack_parity.py (30 stdlib unittest tests)
- refresh atlas-orchestration-team plugin.json and marketplace.json descriptions
  to clearly identify the pack as the optional distribution mirror of the canonical root
- sync 11 mirrored agents back to canonical parity and keep all validators green
```
