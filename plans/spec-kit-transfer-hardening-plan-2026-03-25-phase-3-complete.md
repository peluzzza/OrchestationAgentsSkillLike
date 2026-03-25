## Phase 3 Complete: Verify prompt consistency and close the loop
Aligned the touched Specify agents with the local constitution after review. Layer-2 metadata now uses the constitution-required `domain` form, `SpecifyImplement` remains a true leaf by dropping the `agent` tool, and the updated prompts pass the hierarchy validator plus the focused validator test suite.

**Files:** `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyTasks.agent.md`, `.github/agents/SpecifyImplement.agent.md`
**Functions:** `SpecifySpec`, `SpecifyPlan`, `SpecifyTasks`, `SpecifyImplement`
**Implementation Scope:** Resolved review findings, normalized leaf metadata, removed downstream delegation capability from `SpecifyImplement`, and verified the repo remains green.
**Review:** APPROVED by conductor validation
**Testing (Argus):** PASSED
- Coverage: N/A for prompt files; validator suite passed
- Additional tests: 0 required
- Edge cases: Confirmed no executable leaf-to-leaf handoffs remain and hierarchy validation stays green.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: Validation-only phase

**Git Commit:**
chore: validate specify prompt hardening

- enforce layer-2 leaf boundaries in specify agents
- keep hierarchy validator and focused tests green
