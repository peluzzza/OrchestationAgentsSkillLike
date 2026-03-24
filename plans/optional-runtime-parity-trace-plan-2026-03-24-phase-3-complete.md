## Phase 3 Complete: Validator alignment and non-regression lock
Aligned the optional-contract test fixtures with the new `session`/`trace` semantics and added focused regressions for missing and wrong values. The validator logic itself did not need further changes, which confirms the registry-driven approach held up cleanly.

**Files:** `scripts/test_validate_layer_hierarchy.py`
**Functions:** `TestOptionalRuntimeContracts`, `_HERMES_CONTRACT`, `_ORACLE_CONTRACT`, `_HEPHAESTUS_CONTRACT`
**Implementation Scope:** Updated optional fixtures with `session=inherited` and `trace=required`, added 4 new regression tests for missing/wrong session/trace, preserved stable completeness behavior.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines 89%, Branches N/A, Functions N/A
- Additional tests: 4
- Edge cases: Optional-only inputs remain free of stable completeness violations; real workspace scan still passes

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: No deployment required for test alignment phase

**Git Commit:**
test: align optional trace coverage

- update optional fixtures for session and trace semantics
- lock non-regression for optional contract enforcement
