## Phase 2 Complete: Write dry-run test case
This phase wrote the reusable dry-trace artifact and reconciled the README with the flow actually encoded in Prometheus and Sisyphus. The documentation now distinguishes between shipped hidden Specify helpers and the active delegated path in the default runtime.

**Files:** `plans/atlas-static-trace-test-case-2026-03-25.md`, `README.md`
**Functions:** Static trace artifact, runtime/documentation alignment for the Specify planning path
**Implementation Scope:** Authored a non-executed test case for Atlas, documented expected gates and invariants, and updated README sections that previously overstated active Prometheus delegation to `SpecifyConstitution` and `SpecifyClarify` while also correcting `SpecifyTasks` ownership.
**Review:** APPROVED by desk-check synthesis
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: No execution performed by design; verification limited to static reasoning and editor diagnostics.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: Documentation-only change.

**Git Commit:**
docs: align atlas runtime trace docs

- document the effective Atlas dry-run flow and invariants
- align README with the current Prometheus delegated path
