## Phase 1 Complete: Compress hot-path agent prompts
This phase reduced wording overhead in the most frequently traversed agent prompts while preserving the same routing and gate model. The edits made Atlas, Prometheus, and Sisyphus more direct, and kept README aligned with the current delegated runtime path.

**Files:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Sisyphus-subagent.agent.md`, `README.md`
**Functions:** Stable runtime wording, delegation rules, strict limits, implementation discipline, README runtime path summary
**Implementation Scope:** Shortened repeated conductor/planner/implementer language, kept optional-lane invariants explicit in Atlas, and cleaned the README pipeline block for readability and accuracy.
**Review:** APPROVED with minor follow-up applied
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Edge cases: Focused on semantic drift and prompt clarity rather than runtime execution.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A

**Git Commit:**
refactor: compress hot path agent prompts

- tighten Atlas, Prometheus, and Sisyphus wording
- keep README aligned with the active runtime path
