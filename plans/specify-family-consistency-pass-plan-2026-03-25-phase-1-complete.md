## Phase 1 Complete: Normalize remaining agent metadata
This phase aligned the remaining Layer-2 `Specify*` prompts with the constitution-required metadata format and the leaf-agent guardrail language already established in the earlier hardening batches. The change was intentionally narrow: prompt governance and activation behavior only, with no workflow-step rewrites.

**Files:** `.github/agents/SpecifyAnalyze.agent.md`, `.github/agents/SpecifyClarify.agent.md`, `.github/agents/SpecifyConstitution.agent.md`
**Functions:** Layer metadata comments, activation guards, Layer-2 leaf guidance
**Implementation Scope:** Replaced outdated `parent:` metadata with constitution-compatible `domain:` metadata, added missing activation guard handling to `SpecifyClarify` and `SpecifyConstitution`, and reinforced leaf-only wording for the remaining Specify leaf agents.
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: Deferred to focused repo validator and prompt diagnostics in Phase 2.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: Prompt-only customization change; no runtime deployment surface involved.

**Git Commit:**
chore: normalize remaining specify prompts

- align remaining layer-2 Specify agents with domain metadata
- add missing activation guards and leaf guidance
