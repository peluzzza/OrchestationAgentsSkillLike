## Phase 3 Complete: Add regression coverage
Locked the optional research/ops contract behavior with focused regression tests and a small wording cleanup in validator diagnostics. The validator now has passing coverage for valid optional contracts, invalid optional contracts, and non-coupling with the core stable completeness rules.

**Files:** `scripts/validate_layer_hierarchy.py`, `scripts/test_validate_layer_hierarchy.py`
**Functions:** `_OPTIONAL_RUNTIME_AGENTS`, `_check_runtime_contract`, `TestOptionalRuntimeContracts`, `_HERMES_CONTRACT`, `_ORACLE_CONTRACT`, `_HEPHAESTUS_CONTRACT`
**Implementation Scope:** Added optional-lane contract fixtures, added 14 regression tests, kept stable completeness behavior intact, neutralized a missing-contract error message.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines 85%, Branches N/A, Functions N/A
- Additional tests: 4
- Edge cases: Optional agents do not trigger completeness for one another; stable completeness still triggers correctly when optional agents are present

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: No deployment required for test and validator updates

**Git Commit:**
test: cover optional runtime contracts

- add regression tests for Hermes, Oracle, and HEPHAESTUS contracts
- preserve stable completeness behavior while tightening optional validation
