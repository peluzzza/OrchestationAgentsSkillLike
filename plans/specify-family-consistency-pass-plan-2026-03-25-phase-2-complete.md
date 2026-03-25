## Phase 2 Complete: Validate prompt integrity
This phase confirmed that the normalization patch did not break prompt-file integrity or the repo's layer-hierarchy enforcement. Diagnostics stayed clean, the hierarchy validator passed, the focused pytest suite passed, and the final wording drift noted in review was corrected.

**Files:** `scripts/validate_layer_hierarchy.py`, `scripts/test_validate_layer_hierarchy.py`, `.github/agents/SpecifyAnalyze.agent.md`, `plans/specify-family-consistency-pass-plan-2026-03-25.md`
**Functions:** Layer hierarchy validation, focused validator tests, final prompt wording normalization
**Implementation Scope:** Ran editor diagnostics, executed the layer hierarchy validator, executed the focused validator pytest suite, reviewed the batch, and normalized the remaining `Sisyphus-subagent` wording in `SpecifyAnalyze`.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: Confirmed no prompt diagnostics, no hierarchy regression, and no semantic drift in the planning pipeline.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: No deployment required for prompt-only repo changes.

**Git Commit:**
chore: finish specify prompt consistency pass

- validate remaining Specify prompt normalization with focused checks
- keep hierarchy rules green after the final wording cleanup
