## Phase 2 Complete: Add Governance Specialists
Added generic governance specialists so Atlas can route security, dependency, and documentation-sensitive work without overloading the core implementation/review agents. The same specialist set was mirrored into the general plugin pack to preserve pack parity.

**Files:** `.github/agents/Security.agent.md`, `.github/agents/Documentation.agent.md`, `.github/agents/Dependencies.agent.md`, `plugins/atlas-orchestration-team/agents/Security.agent.md`, `plugins/atlas-orchestration-team/agents/Documentation.agent.md`, `plugins/atlas-orchestration-team/agents/Dependencies.agent.md`
**Functions:** Security review gate, dependency audit gate, documentation update gate
**Implementation Scope:** Adapted external specialist prompts to Atlas conventions, normalized handoffs to `Atlas`, kept responsibilities narrow and hidden by default, mirrored plugin copies
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: N/A for prompt-definition changes
- Edge cases: Specialists remain hidden, generic, and compatible with agent controls / allow-list behavior

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Git Commit:**
feat: add governance specialist agents

- add generic security, documentation, and dependency subagents
- mirror the new specialist set into the general plugin pack
