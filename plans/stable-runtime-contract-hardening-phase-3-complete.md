## Phase 3 Complete: Lock with regression tests
Expanded the validator test suite so the new contract rules are protected by targeted regressions and one real-workspace integration scan. The final pass also covered hidden-case hardening around multi-word agent names and list parsing behavior.

**Files:** `scripts/test_validate_layer_hierarchy.py`
**Functions:** `TestRuntimeContractParsing`, `TestStableRuntimeContracts`, `TestStableAgentCompleteness`, `TestExtractAgentsList`, `TestRealWorkspace`
**Implementation Scope:** Added parsing tests, stable-runtime invariant tests, completeness tests, multi-word `agents:` parsing tests, and defensive unreadable-file coverage
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines 82%, Branches N/A, Functions N/A
- Edge cases: Wrong/missing version, missing contract, missing request/response fields, incomplete stable-agent set, multi-word agent names, blank/comment lines, unreadable file fallback

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A

**Git Commit:**
test: cover stable runtime validator edges

- add regression tests for runtime-contract invariants
- cover multi-word agent parsing and completeness rules
