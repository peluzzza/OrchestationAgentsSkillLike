## Phase 1 Complete: Agent Pack Compatibility
The active root agent pack now includes the missing subagent-style aliases, Atlas and Prometheus point to runtime-safe names, and the root frontmatter no longer contains unsupported tool identifiers.

**Files:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyConstitution.agent.md`, `.github/agents/Afrodita-UX.agent.md`, `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Sisyphus-subagent.agent.md`, `.github/agents/Afrodita-subagent.agent.md`, `.github/agents/Argus-subagent.agent.md`, `.github/agents/Themis-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`
**Functions:** Agent frontmatter wiring, compatibility alias registration, active-pack routing preferences
**Implementation Scope:** Added functional compatibility aliases, rewired root orchestrators to subagent-style names, removed unsupported root tool entries, and preserved conditional fallback behavior for optional Specify agents.
**Review:** APPROVED with minor
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: Validated active pack syntax and searched the root pack for unsupported tool identifiers.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: N/A

**Git Commit:**
chore: normalize root agent pack

- add compatibility subagent aliases in .github/agents
- rewire atlas and prometheus to runtime-safe names
- remove unsupported tool identifiers from active agent files
