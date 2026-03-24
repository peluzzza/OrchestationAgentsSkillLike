## Phase 1 Complete: Define runtime envelopes
Added a shared `stable-runtime-v1` envelope to the core Atlas working loop so planning, implementation, review, and QA now advertise explicit request/response contracts. The changes stayed scoped to the stable runtime surfaces and preserved Atlas as the sole user-facing conductor.

**Files:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Sisyphus-subagent.agent.md`, `.github/agents/Afrodita-subagent.agent.md`, `.github/agents/Themis-subagent.agent.md`, `.github/agents/Argus-subagent.agent.md`
**Functions:** `runtime-contract` envelope comments, `Stable Runtime Envelope` prompt sections
**Implementation Scope:** Added machine-readable runtime-contract comments, aligned request/response prose with the declared contracts, corrected Atlas response-field contract to match its actual output discipline
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Edge cases: Deferred to validator enforcement and regression-testing phases

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A

**Git Commit:**
feat: add stable runtime envelopes

- add runtime-contract comments to Atlas core agents
- align prompt prose with request and response contracts
