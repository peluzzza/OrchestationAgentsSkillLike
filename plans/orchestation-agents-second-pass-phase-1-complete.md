## Phase 1 Complete: Bootstrap Specify Root Assets
Added the missing root `.specify` scaffold that the repo README and Specify agents already depended on. This closes the biggest structural gap in the spec-driven workflow and gives the pipeline a real root-first bootstrap.

**Files:** `.specify/memory/constitution.md`, `.specify/templates/constitution-template.md`, `.specify/templates/spec-template.md`, `.specify/templates/plan-template.md`, `.specify/templates/tasks-template.md`, `.specify/specs/.gitkeep`
**Functions:** Root Specify bootstrap, constitution governance model, spec/plan/tasks templates
**Implementation Scope:** Created a concrete constitution for Atlas orchestration, added minimal Spec Kit-derived templates, established tracked root `.specify/specs/`
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: N/A for this phase-only documentation/bootstrap work
- Edge cases: Verified the root bootstrap matches the documented `.specify` layout and avoids overbuilding unused ADR/PHR assets

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Git Commit:**
feat: bootstrap root specify assets

- add root .specify scaffold and concrete constitution
- add minimal spec, plan, and tasks templates
