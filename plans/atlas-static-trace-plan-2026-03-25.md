## Plan: Atlas static trace
This pass performs a non-executed desk-check of the Atlas orchestration flow. The goal is to validate that the documented and encoded control flow are coherent enough for a normal implementation task, and to record any breakpoints or semantic drift discovered during static tracing.

**Phases 2**
1. **Phase 1: Reconstruct Atlas flow**
   - **Objective:** Trace the end-to-end happy path and decision gates for a standard implementation request without executing tools or tests from the runtime being analyzed.
   - **Files/Functions:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Sisyphus-subagent.agent.md`, `.github/agents/Themis-subagent.agent.md`, `.github/agents/Argus-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`, `README.md`
   - **QA Focus:** Check control-flow coherence, gate ownership, delegation boundaries, and doc/runtime alignment.
   - **Steps:** 1. Map the happy path. 2. Mark each gate and return contract. 3. Record static breakpoints and mismatches.
2. **Phase 2: Write dry-run test case**
   - **Objective:** Produce a reusable manual trace artifact that can be reviewed later without running the pipeline.
   - **Files/Functions:** `plans/atlas-static-trace-test-case-2026-03-25.md`
   - **QA Focus:** Ensure the trace is deterministic, references real files, and distinguishes expected behavior from observed drift.
   - **Steps:** 1. Define a representative user request. 2. Walk each expected delegation step. 3. Capture invariants, weak points, and verdict.

**Open Questions 1**
1. Should Prometheus be aligned to truly invoke `SpecifyConstitution` and `SpecifyClarify`, or should README/docs be updated to describe the current degraded-path behavior explicitly?
