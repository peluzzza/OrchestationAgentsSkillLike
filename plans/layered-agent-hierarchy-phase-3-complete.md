## Phase 3 Complete: Layer 1 God Upgrades

Fixed all 11 canonical Layer-1 god agents and 7 root-only aliases. Every god now carries valid tool declarations, an explicit `agents:` list pointing to its L2 subtree, and a `<!-- layer: 1 -->` metadata comment. Parity between `.github/agents/` and `plugins/atlas-orchestration-team/agents/` is confirmed clean.

**Files:** `.github/agents/Prometheus.agent.md`, `.github/agents/Sisyphus.agent.md`, `.github/agents/Themis.agent.md`, `.github/agents/Argus.agent.md`, `.github/agents/Hermes.agent.md`, `.github/agents/Oracle.agent.md`, `.github/agents/Atenea.agent.md`, `.github/agents/Ariadna.agent.md`, `.github/agents/Clio.agent.md`, `.github/agents/Hephaestus.agent.md`, `.github/agents/Afrodita-UX.agent.md`, `plugins/atlas-orchestration-team/agents/<all 11 + Atlas>.agent.md`, `.github/agents/Afrodita-subagent.agent.md`, `.github/agents/Argus-subagent.agent.md`, `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`, `.github/agents/Sisyphus-subagent.agent.md`, `.github/agents/Themis-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`

**Functions:** N/A (configuration-only changes)

**Implementation Scope:**
- Invalid tool names eliminated across 11 god files: `web/fetch` → `web`+`fetch`; `execute/runInTerminal`, `execute/getTerminalOutput` → `execute` (dedup); `read/terminalLastCommand`, `read/terminalSelection` → `read` (dedup); `read/problems` → `problems`; `search/changes` → `changes`
- `agents:` frontmatter added/updated on every god to reference explicit L2 subtrees: Prometheus→9 Specify agents; Sisyphus→Backend-Atlas+Data-Atlas+3 Specify agents; Themis→4 reviewer agents; Argus→A11y-Auditor; Atenea→Security-Guard+Security-Ops; Clio→Frontend-Handoff; Hephaestus→DevOps-Atlas+Automation-Atlas; Afrodita-UX→Afrodita+UX-Atlas; Hermes→`[]`; Oracle→`[]`; Ariadna→`[]`
- `<!-- layer: 1 | domain: ... -->` metadata comment added to each god immediately after closing `---`
- 7 root-only aliases: tool name fixes applied to Afrodita-subagent, Argus-subagent, Hephaestus-subagent, Sisyphus-subagent, Oracle-subagent; agents list updated in Sisyphus-subagent (added Backend-Atlas, Data-Atlas); `<!-- layer: 1 | type: alias | delegates-to: <parent-god> -->` added to all 7
- Synced all 12 canonical files (.github/agents/Atlas + 11 gods) to `plugins/atlas-orchestration-team/agents/` via Copy-Item

**Review:** APPROVED
**Testing (Argus):** PASSED
- `validate_atlas_pack_parity.py` → `ATLAS PACK PARITY OK  source=19 shared agents, root=26 agents (19 synced shared)`
- Edge cases: deduplication of tool names verified; aliases not synced to plugins/ (correct — root-only by design)

**Deployment (Hephaestus):** N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A

**Git Commit:**
```
feat: enforce Layer-1 god isolation — fix tools, agents, layer comments

- Fix 20+ invalid tool names across 11 god files and 7 alias files
- Add explicit agents: lists on all 11 gods (L2 subtree references)
- Add <!-- layer: 1 --> metadata comment to all gods and aliases
- Update Sisyphus-subagent agents list to match canonical Sisyphus
- Sync all 12 canonical god files to plugins/ (parity confirmed OK)
```
