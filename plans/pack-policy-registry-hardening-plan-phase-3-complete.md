## Phase 3 Complete: Align pack discovery consumers
Updated pack discovery surfaces so they now distinguish the canonical default-active core from marketplace-installable packs and shipped-local inactive packs. This keeps recommendations honest and prevents the catalog from implying that every shipped pack is marketplace-installable.

**Files:** `plugins/agent-pack-catalog/agents/PackCatalog.agent.md`, `plugins/agent-pack-catalog/skills/agent-pack-search/SKILL.md`, `README.md`
**Functions:** N/A (agent/skill/docs surfaces)
**Implementation Scope:** Made discovery registry-aware, fixed skill metadata/frontmatter, added type-specific activation guidance, surfaced registry verification commands in the README.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Declarative surfaces validated indirectly through editor diagnostics and live registry/test runs
- Edge cases: canonical-core classification, local-path activation for shipped-local packs, marketplace-only install paths for published subset

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A

**Git Commit:**
fix: align pack discovery guidance

- classify packs by canonical core vs published vs local
- add valid metadata to agent-pack-search skill
- expose registry verification commands in docs
