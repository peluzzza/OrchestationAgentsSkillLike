## Phase 2 Complete: Enforce contract rules
Extended the hierarchy validator so it now recognizes `runtime-contract` comments and enforces the stable Atlas-centered routing invariants for the six core runtime agents. The original layer checks were preserved while stable-runtime validation became explicit and machine-checkable.

**Files:** `scripts/validate_layer_hierarchy.py`
**Functions:** `_parse_runtime_contract`, `_check_runtime_contract`, `validate`, `_extract_agents_list`
**Implementation Scope:** Parsed runtime-contract comments, enforced `stable-runtime-v1`, validated required request/response fields, enforced stable-agent completeness, enforced non-Atlas role/layer contracts, hardened multi-word `agents:` parsing
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines 82%, Branches N/A, Functions N/A
- Edge cases: Stable-agent completeness, wrong version, wrong role/layer, wrong accepts/returns, multi-word agent names, blank/comment lines inside `agents:` blocks

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A

**Git Commit:**
feat: enforce runtime contract validation

- extend layer validator with stable-runtime contract checks
- harden agent list parsing for real runtime names
