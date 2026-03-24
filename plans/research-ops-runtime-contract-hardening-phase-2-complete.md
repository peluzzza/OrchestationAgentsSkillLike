## Phase 2 Complete: Enforce optional-lane validation
Extended the hierarchy validator so it checks runtime contracts for Hermes, Oracle, and HEPHAESTUS when those agents are present, while leaving the core stable six completeness rule untouched. This keeps auxiliary lanes explicit without over-coupling them to the default Atlas loop.

**Files:** `scripts/validate_layer_hierarchy.py`
**Functions:** `_OPTIONAL_RUNTIME_AGENTS`, `validate`, `_check_runtime_contract`, `_check_stable_agent_completeness`
**Implementation Scope:** Added a separate optional runtime registry, reused existing contract validation logic, preserved current core completeness semantics.
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: Review identified a wording-only follow-up for missing-contract diagnostics

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: No deployment required for validator-only code changes

**Git Commit:**
feat: validate optional agent contracts

- add optional runtime registry for research and ops lanes
- keep stable core completeness rules unchanged
