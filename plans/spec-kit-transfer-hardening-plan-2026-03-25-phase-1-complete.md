## Phase 1 Complete: Harden SP-stage lifecycle wrappers
Ported the high-value lifecycle wrapper behavior from `spec-kit` into the local Specify planning agents. `SpecifySpec`, `SpecifyPlan`, and `SpecifyTasks` now expose symmetrical pre/post hook handling with local conductor escalation semantics instead of implicit stage behavior.

**Files:** `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyTasks.agent.md`
**Functions:** `SpecifySpec`, `SpecifyPlan`, `SpecifyTasks`
**Implementation Scope:** Added `before_specify`, `after_specify`, `before_plan`, `after_plan`, `before_tasks`, and `after_tasks` hook semantics; normalized `enabled`/`optional`/`condition` handling; preserved leaf-agent boundaries.
**Review:** APPROVED with follow-up applied
**Testing (Argus):** SKIPPED
- Coverage: N/A
- Additional tests: 0
- Edge cases: Missing `.specify/extensions.yml`, disabled hooks, omitted `enabled`, and non-empty `condition` handling are now described consistently.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: Prompt-only phase

**Git Commit:**
feat: harden specify lifecycle hooks

- add spec-kit-style SP hook wrappers
- keep conductor ownership for mandatory hooks
