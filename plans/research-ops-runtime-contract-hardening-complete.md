## Plan Complete: Research ops runtime contracts
Extended the repo’s runtime-contract hardening from the core Atlas loop into the exploration, research, and ops lanes. Hermes-subagent, Oracle-subagent, and HEPHAESTUS now expose explicit `stable-runtime-v1` envelopes, and the validator/tests now enforce those contracts when present without promoting them into the mandatory stable core.

**Phases:** 3 of 3
1. ✅ Phase 1: Contract the auxiliary lanes
2. ✅ Phase 2: Enforce optional-lane validation
3. ✅ Phase 3: Add regression coverage

**Files:** `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`, `scripts/validate_layer_hierarchy.py`, `scripts/test_validate_layer_hierarchy.py`, `plans/research-ops-runtime-contract-hardening-plan.md`
**Key Functions/Classes:** `Hermes-subagent`, `Oracle-subagent`, `HEPHAESTUS`, `_OPTIONAL_RUNTIME_AGENTS`, `_check_runtime_contract`, `validate`, `TestOptionalRuntimeContracts`
**Tests:** Total 70, All ✅

**Next Steps:**
- Optionally add low-priority parity tests for optional contract version mismatches and `accepts=parent-agent` drift
- Consider a later batch for explicit trace/session semantics if the repo introduces resumable research or ops workflows
