## Phase 1 Complete: Optional parity regression matrix
Added focused parity tests for optional runtime contracts so the research and ops lanes now have explicit regression coverage for version drift, caller-target drift, valid-together behavior, and low-cost file discovery coverage. This phase hardened confidence before touching contract semantics.

**Files:** `scripts/test_validate_layer_hierarchy.py`
**Functions:** `TestOptionalRuntimeContracts`, `TestCollectAgentFiles`, `_collect_agent_files`
**Implementation Scope:** Added 7 pytest cases covering wrong optional version, wrong `accepts` drift for Hermes and Oracle, valid optional trio behavior, and direct `_collect_agent_files()` coverage.
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 7
- Edge cases: Optional agents valid together stay noise-free; file discovery handles empty repos and non-agent files

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: No deployment required for test-only phase

**Git Commit:**
test: add optional parity coverage

- cover optional contract version and accepts drift
- verify optional trio validity and file discovery behavior
