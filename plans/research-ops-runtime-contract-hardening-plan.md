## Plan: Research ops runtime contracts
Extend the runtime-contract pattern to the exploration, research, and ops lanes so those agents become machine-describable without turning them into mandatory members of the core Atlas execution loop. The goal is stronger routing and safer delegation while preserving the repo’s current “optional when present” behavior.

**Phases 3**
1. **Phase 1: Contract the auxiliary lanes**
   - **Objective:** Add compact `runtime-contract` envelopes to Hermes-subagent, Oracle-subagent, and HEPHAESTUS, aligned with their existing prose output contracts.
   - **Files/Functions:** `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`
   - **QA Focus:** Ensure each contract reflects real request/response semantics already present in the prompt and does not invent new orchestration behavior.
   - **Steps:** 1. Add a stable-runtime-v1 contract comment to each target agent. 2. Add a short envelope section clarifying required inputs and outputs. 3. Preserve existing lane-specific semantics such as Hermes read-only behavior and HEPHAESTUS mode/status routing.
2. **Phase 2: Enforce optional-lane validation**
   - **Objective:** Teach the hierarchy validator to validate research/ops runtime contracts when those agents are present, without adding them to the mandatory core stable set.
   - **Files/Functions:** `scripts/validate_layer_hierarchy.py`
   - **QA Focus:** Reject missing or malformed contracts for present optional agents while preserving the current completeness rule for the core six stable agents.
   - **Steps:** 1. Add a separate optional runtime registry. 2. Reuse the existing contract checker for optional agents. 3. Avoid optional-set completeness coupling.
3. **Phase 3: Add regression coverage**
   - **Objective:** Lock the new optional-lane rules with focused tests.
   - **Files/Functions:** `scripts/test_validate_layer_hierarchy.py`
   - **QA Focus:** Cover valid optional contracts, missing/invalid optional contracts, and the absence of optional completeness requirements.
   - **Steps:** 1. Add contract fixtures for Hermes, Oracle, and HEPHAESTUS. 2. Add positive and negative validation tests. 3. Re-run validator tests and the workspace scan.

**Open Questions 2**
1. Should Hermes and Oracle use concrete caller names or abstract `parent-agent` in their contracts?
   - **Recommendation:** Use `parent-agent` for now because both are parent-invoked auxiliary lanes and the validator should stay lightweight.
2. Should HEPHAESTUS have per-mode subcontracts today?
   - **Recommendation:** No. Keep one unified runtime envelope first, then add mode-specific validation only if real drift appears later.
