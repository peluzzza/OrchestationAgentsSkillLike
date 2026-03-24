## Phase 1 Complete: Contract the auxiliary lanes
Added `stable-runtime-v1` envelopes to the exploration, research, and ops lanes without changing their role boundaries or execution behavior. Hermes, Oracle, and HEPHAESTUS now expose machine-readable request/response contracts that match their existing prose semantics.

**Files:** `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`
**Functions:** `Hermes-subagent`, `Oracle-subagent`, `HEPHAESTUS`
**Implementation Scope:** Added runtime-contract HTML comments, added `Stable Runtime Envelope` sections, preserved existing read-only/research/ops semantics.
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: Not applicable for this additive prompt-contract phase

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: No deployment required for agent instruction files

**Git Commit:**
chore: add research ops contracts

- add stable-runtime envelopes to Hermes, Oracle, and HEPHAESTUS
- preserve existing auxiliary lane behavior while making routing explicit
