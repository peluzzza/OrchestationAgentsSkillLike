## Phase 2 Complete: Tighten planning-stage preflight and context sync
Hardened `SpecifyPlan` with explicit preflight gates and a deterministic context-sync contract inspired by donor `update-agent-context.sh`, but adapted to the local repo boundary. Planning-stage sync is now constrained to `.specify/memory/decision-log.md` and `.specify/memory/session-memory.md` instead of mutating runtime agent files.

**Files:** `.github/agents/SpecifyPlan.agent.md`, `.specify/memory/decision-log.md`, `.specify/memory/session-memory.md`
**Functions:** `SpecifyPlan`
**Implementation Scope:** Added feature/artifact readiness checks, explicit `READY_FOR_PLANNING` gating, no-open-clarifications check, and normalized memory-update instructions for planning decisions.
**Review:** APPROVED with follow-up applied
**Testing (Argus):** SKIPPED
- Coverage: N/A
- Additional tests: 0
- Edge cases: Planning is now instructed to stop cleanly on missing spec artifacts or unresolved clarification markers.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: Prompt-only phase

**Git Commit:**
feat: tighten specify plan preflight

- add deterministic planning preflight gates
- constrain context sync to specify memory files
