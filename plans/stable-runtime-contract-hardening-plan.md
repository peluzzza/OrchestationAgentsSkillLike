## Plan: Stable runtime contracts
Strengthen the active Atlas runtime by adding machine-readable handoff contracts to the core working agents, then teach the hierarchy validator to enforce those contracts. This makes the current layered system more deterministic without introducing new orchestration layers.

**Phases 3**
1. **Phase 1: Define runtime envelopes**
   - **Objective:** Add a shared, machine-readable runtime-contract envelope to the stable planning, implementation, review, and QA surfaces.
   - **Files/Functions:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Sisyphus-subagent.agent.md`, `.github/agents/Afrodita-subagent.agent.md`, `.github/agents/Themis-subagent.agent.md`, `.github/agents/Argus-subagent.agent.md`
   - **QA Focus:** Validate that each stable runtime agent declares explicit requester, return target, status semantics, and run/session expectations.
   - **Steps:** 1. Define a compact `runtime-contract` comment format that can be parsed reliably. 2. Apply the envelope to Atlas, Prometheus, Sisyphus, Afrodita, Themis, and Argus. 3. Align the prose instructions in each agent with the new envelope so the contracts are not only decorative.
2. **Phase 2: Enforce contract rules**
   - **Objective:** Extend the hierarchy validator so it checks stable runtime contract presence and the most important routing invariants.
   - **Files/Functions:** `scripts/validate_layer_hierarchy.py`
   - **QA Focus:** Ensure the validator rejects missing runtime contracts and incorrect Atlas return-path semantics without breaking existing layer checks.
   - **Steps:** 1. Parse the runtime-contract comment. 2. Add checks for required stable agents. 3. Preserve the current layer rules and reporting clarity.
3. **Phase 3: Lock with regression tests**
   - **Objective:** Add focused regression tests for the new runtime-contract rules.
   - **Files/Functions:** `scripts/test_validate_layer_hierarchy.py`
   - **QA Focus:** Cover valid envelopes, missing envelopes, wrong return targets, and existing hierarchy edge cases.
   - **Steps:** 1. Add unit tests for runtime-contract parsing. 2. Add validation tests for stable-runtime agents. 3. Re-run the targeted validator test suite.

**Open Questions 2**
1. Should the stable-runtime contract live in YAML frontmatter or a top-of-body comment?
   - **Recommendation:** Use a top-of-body HTML comment because it is easy to parse with the existing lightweight validator and keeps the frontmatter from becoming a pseudo-schema.
2. Should this first batch cover Hermes, Oracle, and Hephaestus too?
   - **Recommendation:** No. First harden the core execution loop used in nearly every run, then expand the contract pattern to exploration and ops lanes in a follow-up batch.
