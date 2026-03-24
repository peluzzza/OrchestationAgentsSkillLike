## Plan Complete: Stable runtime contracts
The active Atlas runtime now has explicit `stable-runtime-v1` envelopes across its core planning, implementation, review, and QA surfaces, and the workspace validator can enforce those contracts. This tightens the system from prompt-only convention into prompt-plus-protocol behavior without adding new orchestration layers or frameworks.

**Phases:** 3 of 3
1. ✅ Phase 1: Define runtime envelopes
2. ✅ Phase 2: Enforce contract rules
3. ✅ Phase 3: Lock with regression tests

**Files:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Sisyphus-subagent.agent.md`, `.github/agents/Afrodita-subagent.agent.md`, `.github/agents/Themis-subagent.agent.md`, `.github/agents/Argus-subagent.agent.md`, `scripts/validate_layer_hierarchy.py`, `scripts/test_validate_layer_hierarchy.py`, `plans/stable-runtime-contract-hardening-plan.md`
**Key Functions/Classes:** `runtime-contract` envelope comments, `_parse_runtime_contract`, `_check_runtime_contract`, `validate`, `_extract_agents_list`, `TestRuntimeContractParsing`, `TestStableRuntimeContracts`, `TestStableAgentCompleteness`, `TestExtractAgentsList`
**Tests:** Total 57, All ✅

**Next Steps:**
- Extend the same contract pattern to `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS` in a second hardening batch.
- Add a lightweight trace or run-id field to the runtime envelope once the ops and exploration lanes join the same protocol.
