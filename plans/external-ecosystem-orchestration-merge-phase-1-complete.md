## Phase 1 Complete: Freeze Merge Lanes
This phase established the orchestration-repo-specific investigation baseline and documented how external ecosystems should be merged by folder. It intentionally focused on safe, structural documentation changes before touching agents, plugins, or runtime behavior.

**Files:** `plans/external-ecosystem-orchestration-investigation.md`, `plans/external-ecosystem-orchestration-merge-plan.md`, `README.md`, `plugins/README.md`
**Functions:** N/A (documentation-only phase)
**Implementation Scope:** investigation report, phased merge roadmap, README merge-lane guidance, plugin-space merge guidance
**Review:** APPROVED with minor
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: Docs were checked for consistency with the repo's existing root-first and plugin-optional model.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: Documentation-only batch; no deployment surface changed.

**Git Commit:**
chore: add orchestration merge roadmap

- document external ecosystem investigation for orchestration repo
- add phased merge plan and first batch documentation updates
