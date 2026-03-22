## Phase 1 Complete: Rename core specialists
Replaced the remaining functional specialist identities in the canonical pack and plugin mirror with mythological names, while keeping the same responsibilities and preserving `Hephaestus` as an explicit routed specialist. The legacy functional-name agent files were removed so the live pack no longer presents mixed naming.

**Files:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Afrodita-UX.agent.md`, `.github/agents/Atenea.agent.md`, `.github/agents/Clio.agent.md`, `.github/agents/Ariadna.agent.md`, `plugins/atlas-orchestration-team/agents/Atlas.agent.md`, `plugins/atlas-orchestration-team/agents/Afrodita-UX.agent.md`, `plugins/atlas-orchestration-team/agents/Atenea.agent.md`, `plugins/atlas-orchestration-team/agents/Clio.agent.md`, `plugins/atlas-orchestration-team/agents/Ariadna.agent.md`
**Functions:** Atlas routing policy, Atlas delegation briefs, Prometheus implementation-boundary guidance, mythological specialist prompt identities
**Implementation Scope:** Added `Afrodita-UX`, `Atenea`, `Clio`, and `Ariadna` in root and mirror; rewired root routing/docs to use the new names; removed legacy `Frontend-Engineer`, `Security`, `Documentation`, and `Dependencies` prompt files from root and mirror; replaced the misleading `disabled_agents: [Hephaestus]` example
**Review:** APPROVED with minor
**Testing (Argus):** PASSED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Edge cases: Verified that the mythological names are live on the requested canonical surfaces and that `Hephaestus` remains explicitly present; follow-up drift in the plugin mirror and project document was deferred to Phase 2.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A
- The status must be valid for the declared operations mode; do not mix tokens across modes.

**Git Commit:**
refactor: mythologize core specialist agents

- replace functional specialist prompts with mythological identities
- update atlas routing to use afrodita-ux, atenea, clio, and ariadna
- remove legacy frontend, security, documentation, and dependencies files
