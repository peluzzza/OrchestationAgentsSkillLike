## Phase 1 Complete: Confirm and close optional parity gaps
Focused parity coverage for optional runtime agents is now complete without changing validator behavior. The batch stayed tests-only: it added the missing regressions for optional `returns`, missing `version`, and `HEPHAESTUS` `accepts`, then cleaned touched negative fixtures so each one fails for exactly one reason.

**Files:** `scripts/test_validate_layer_hierarchy.py`
**Functions:** `validate`, `_check_runtime_contract` (covered by tests; no production changes)
**Implementation Scope:** Added five optional-contract regressions, normalized three existing negative fixtures to be single-fault-clean, preserved stable completeness semantics.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines 89%, Branches N/A, Functions N/A
- Additional tests: 6 recommended for future symmetry, 0 required for this phase
- Edge cases: Verified missing optional version, returns drift across all optional lanes, HEPHAESTUS accepts drift, and no stable-completeness coupling regressions

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: No deploy surface; tests-only batch

**Git Commit:**
test: expand optional runtime parity coverage

- add focused optional contract regression tests
- normalize touched fixtures to single-fault cases
