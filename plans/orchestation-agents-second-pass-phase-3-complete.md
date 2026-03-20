## Phase 3 Complete: Wire Atlas And Align Docs
Aligned the repo’s orchestration contract end-to-end: Atlas now treats Prometheus as the mandatory planning path for implementation work, `SpecifyAnalyze` has a coherent SP-5/EX-1 model with `analysis-report.md` ownership, and the README/plugin docs now describe the real root-first setup without duplicate-source confusion.

**Files:** `.github/agents/Atlas.agent.md`, `.github/agents/SpecifyAnalyze.agent.md`, `.github/agents/SpecifyConstitution.agent.md`, `README.md`, `plugins/README.md`, `plugins/atlas-orchestration-team/agents/Atlas.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyAnalyze.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyConstitution.agent.md`
**Functions:** Atlas planning policy, SpecifyAnalyze gate model, SpecifyConstitution bootstrap/amendment flow, installation and workflow documentation
**Implementation Scope:** Added routing guidance for `Security`/`Dependencies`/`Documentation`, clarified default-visible vs explicitly enabled conductors, reframed source-selection docs as optional/demo behavior, corrected agent counts and setup syntax drift
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: N/A (pytest run, no coverage mode); 50 passed / 8 skipped demo tests
- Edge cases: Resolved contradictions around implementation planning, visibility rules, `analysis-report.md` ownership, and test-task guidance in the touched template surface

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Git Commit:**
fix: align atlas and specify docs

- reconcile Atlas, SpecifyAnalyze, and constitution workflow rules
- update README and plugin docs to match the root-first setup
