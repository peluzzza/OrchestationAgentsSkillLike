## Phase 2 Complete: Minimal trace/session semantics
Extended the optional research and ops contracts with explicit `session` and `trace` semantics in a lightweight declarative form. Hermes, Oracle, and HEPHAESTUS now state that they participate in the caller’s active session context and delegation trace without implying resumability or checkpoint behavior.

**Files:** `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`, `scripts/validate_layer_hierarchy.py`
**Functions:** `Hermes-subagent`, `Oracle-subagent`, `HEPHAESTUS`, `_OPTIONAL_RUNTIME_AGENTS`
**Implementation Scope:** Added `session=inherited` and `trace=required` to optional runtime-contract comments and prose envelopes; updated the optional validator registry to require those fields.
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: Semantics remain metadata-only; no resume/checkpoint behavior introduced

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: No deployment required for agent contract/validator registry changes

**Git Commit:**
feat: add optional session trace fields

- declare session and trace semantics for research and ops lanes
- keep optional contract validation registry-driven and lightweight
