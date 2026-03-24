## Plan Complete: Optional runtime parity and explicit trace/session semantics
Completed both requested tracks together: Option A added the missing parity regressions for optional runtime contracts, and Option B introduced a minimal third wave of explicit `session`/`trace` semantics for the research and ops lanes. The result is a more explicit, more test-hardened optional runtime surface without changing the mandatory stable core or inventing heavy resumability semantics.

**Phases:** 3 of 3
1. ✅ Phase 1: Optional parity regression matrix
2. ✅ Phase 2: Minimal wave-3 trace/session semantics
3. ✅ Phase 3: Validator alignment and non-regression lock

**Files:** `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`, `scripts/validate_layer_hierarchy.py`, `scripts/test_validate_layer_hierarchy.py`, `plans/optional-runtime-parity-trace-plan-2026-03-24.md`
**Key Functions/Classes:** `Hermes-subagent`, `Oracle-subagent`, `HEPHAESTUS`, `_OPTIONAL_RUNTIME_AGENTS`, `_check_runtime_contract`, `TestOptionalRuntimeContracts`, `TestCollectAgentFiles`
**Tests:** Total 81, All ✅

**Next Steps:**
- Optionally add the remaining low-priority parity cases for optional `returns`, missing optional `version`, and HEPHAESTUS `accepts` drift
- If you later want resumable research/ops workflows, do it as a separate batch with explicit persistence semantics rather than expanding these lightweight metadata contracts
