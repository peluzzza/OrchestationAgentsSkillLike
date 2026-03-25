## Plan: Agent semantic compression pass
This pass trims high-frequency agent wording to make the runtime more concrete and less token-heavy without changing gates, routing, or contracts. It also captures the final validation needed before commit and push.

**Phases 2**
1. **Phase 1: Compress hot-path agent prompts**
   - **Objective:** Reduce redundant wording in the most frequently invoked agents while preserving behavior.
   - **Files/Functions:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Sisyphus-subagent.agent.md`, `README.md`
   - **QA Focus:** Verify that compression keeps routing, phase gates, and runtime contracts intact.
   - **Steps:** 1. Trim repeated policy wording. 2. Keep invariants explicit. 3. Tighten wording in README where helpful.
2. **Phase 2: Revalidate and package**
   - **Objective:** Confirm the compressed prompts remain syntactically clean and pass focused repo validation before commit.
   - **Files/Functions:** `scripts/validate_layer_hierarchy.py`, `scripts/test_validate_layer_hierarchy.py`
   - **QA Focus:** No prompt diagnostics, no hierarchy regression, no contract drift.
   - **Steps:** 1. Check editor diagnostics. 2. Run focused validator and pytest suite. 3. Record results and prepare commit.

**Open Questions 1**
1. Should the same compression pattern be extended later to optional lanes like Hermes/Oracle, or kept limited to the hot path for now?
