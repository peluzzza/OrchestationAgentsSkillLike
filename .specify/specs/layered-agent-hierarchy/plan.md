# Implementation Plan: Layered Agent Hierarchy

**Branch**: `layered-agent-hierarchy` | **Date**: 2026-03-23
**Spec**: `.specify/specs/layered-agent-hierarchy/spec.md`

> **Note**: This file is produced by SP-4. It documents the complete design decisions, phase structure, and implementation contracts for the `layered-agent-hierarchy` feature.

---

## Summary

Establish a strict 3-layer agent hierarchy (Layer 0: Atlas, Layer 1: 11 gods + 7 aliases, Layer 2: all specialists) across the VS Code Copilot agent system. Simultaneously fix 20+ invalid VS Code tool declarations, integrate a 3-level persistent memory protocol, import non-duplicative external agents, and deliver a validation/demo suite targeting ≥250 total tests.

## Technical Context

**Language/Version**: Python 3.x (validation scripts); YAML/Markdown (agent config files); JSON (registry files); TypeScript (optional memory backend)
**Primary Dependencies**: VS Code Copilot agent runtime; `@modelcontextprotocol/server-memory` MCP package; existing `scripts/validate_*.py` infrastructure
**Storage**: File-based (`.specify/memory/*.md`, `.specify/specs/`); MCP Knowledge Graph (SQLite via `@modelcontextprotocol/server-memory`)
**Testing**: Python `pytest` (existing pattern in `scripts/test_*.py`)
**Target Platform**: VS Code workspace (Windows/Mac/Linux)
**Project Type**: Agent configuration + validation tooling
**Performance Goals**: N/A for config files; validation scripts must complete in <10s
**Constraints**: VS Code tool names are an exact validated set; `agents:` in frontmatter is declarative but enforced by validation scripts; parity between `.github/agents/` and `plugins/atlas-orchestration-team/agents/` must be maintained
**Scale/Scope**: Workspace-level configuration; affects all 89 agent files across 8 plugin packs

---

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Conductor-First Visibility | ✅ Pass | Phases 2+4 set pack conductors `user-invocable: false` |
| II. Spec-Driven Development | ✅ Pass | Spec gates plan; plan gates implementation |
| III. Progressive Delegation | ✅ Pass | Atlas→L1→L2 chain enforced by design |
| IV. Atomic Task Execution | ✅ Pass | Each phase is independently verifiable with named checkpoint |
| V. Root-First Bootstrap | ✅ Pass | `.specify/` directory exists; templates intact |
| VI. Gate-Based Progression | ✅ Pass | SP-5 analysis report gates Atlas execution |
| VII. Human Sovereignty | ✅ Pass | Human approves each phase before Sisyphus proceeds |

---

## Complexity Tracking

| Consideration | Decision | Rationale |
|---------------|----------|-----------|
| Memory god ("Mnemo") | Prometheus owns memory (conservative) | Avoids new god creation; Prometheus already manages `.specify/memory/` files |
| Oracle L2 specialists | Oracle is self-sufficient (no pack L2) | Oracle uses its own tools; planners stay in their domain packs |
| Reviewer dual ownership | Reviewers stay in domain packs; Themis references them | Avoids moving files; Themis becomes the cross-domain review conductor |
| Pack conductors `user-invocable` | Set to `false` in all packs | Constitution Principle I compliance; standalone pack use remains via Atlas |
| `agents:["*"]` replacement | Explicit named lists in all conductors | Enforces hierarchy; no agent escapes its layer |

---

## Complete Agent Inventory by Layer

### Layer 0 (1 agent)
| Agent | File | Status |
|-------|------|--------|
| Atlas | `.github/agents/Atlas.agent.md` | Requires L1-only `agents:` list, tool fix |

### Layer 1 (18 agents = 11 gods + 7 root-only aliases)

**Canonical gods (in `.github/agents/` AND `plugins/atlas-orchestration-team/agents/`):**
| Agent | Domain | L2 Roster |
|-------|--------|-----------|
| Prometheus | Planning + Specification + Memory | 7 Specify agents |
| Sisyphus | Backend + Data Implementation | Backend-Atlas, Data-Atlas (L2 conductors) |
| Themis | Code Review + Quality Gate | Backend-Reviewer, Frontend-Reviewer, Data-Reviewer, Automation-Reviewer |
| Argus | QA + Testing | A11y-Auditor, [new] Test-Runner, Coverage-Analyst, Mutation-Tester |
| Hermes | Discovery + Codebase Mapping | (self-sufficient scout; no pack L2) |
| Oracle | Requirements + Architecture Research | (self-sufficient researcher; no pack L2) |
| Atenea | Security + Safety | Security-Guard, Security-Ops, [new] Compliance-Checker, Secret-Scanner |
| Ariadna | Dependency + Package Audit | (self-sufficient auditor; no pack L2) |
| Clio | Documentation | Frontend-Handoff |
| Hephaestus | Infrastructure + DevOps + Automation | DevOps-Atlas, Automation-Atlas (L2 conductors), [new] Cost-Optimizer, Incident-Responder |
| Afrodita-UX | Frontend + UX | Afrodita (plugin conductor), UX-Atlas (L2 conductor) |

**Root-only aliases (`.github/agents/` only — NOT in atlas-orchestration-team/agents/):**
- `Afrodita-subagent`, `Argus-subagent`, `Hermes-subagent`, `Hephaestus-subagent`, `Sisyphus-subagent`, `Themis-subagent`, `Oracle-subagent`

### Layer 2 (70+ agents across plugin packs)

| Pack | Conductor (L2) | Parent God (L1) | Specialists |
|------|----------------|-----------------|-------------|
| `backend-workflow` | Backend-Atlas | Sisyphus | API-Designer, Service-Builder, Database-Engineer, Performance-Tuner, Security-Guard, Backend-Planner, Backend-Reviewer |
| `data-workflow` | Data-Atlas | Sisyphus | Pipeline-Builder, ML-Scientist, Data-Architect, Analytics-Engineer, Data-Quality, Data-Planner, Data-Reviewer |
| `devops-workflow` | DevOps-Atlas | Hephaestus | Infra-Architect, Pipeline-Engineer, Container-Master, Deploy-Strategist, Monitor-Sentinel, Security-Ops, DevOps-Planner, [new] Cost-Optimizer, [new] Incident-Responder |
| `automation-mcp-workflow` | Automation-Atlas | Hephaestus | Workflow-Composer, MCP-Integrator, Automation-Planner, Automation-Reviewer, [new] n8n-Connector |
| `frontend-workflow` | Afrodita | Afrodita-UX | UI-Designer, Style-Engineer, State-Manager, Component-Builder, Frontend-Planner, Frontend-Reviewer, A11y-Auditor |
| `ux-enhancement-workflow` | UX-Atlas | Afrodita-UX | User-Flow-Designer, Design-Critic, Accessibility-Heuristics, Frontend-Handoff, UX-Planner |
| `qa-workflow` (new) | — | Argus | Test-Runner, Coverage-Analyst, Mutation-Tester |
| `security-workflow` (new) | — | Atenea | Compliance-Checker, Secret-Scanner |
| `memory-system` (new) | Memory-Guardian | Prometheus | (memory protocol specialist; standalone) |
| `atlas-orchestration-team` | — (canonical source) | — | Sync source for 19 canonical agents |
| `agent-pack-catalog` | PackCatalog | — (user-invocable exception) | agent-pack-search skill |

---

## Tool Name Correction Map

All occurrences of the following invalid patterns must be replaced:

| Invalid pattern | Corrected to | Affected agents |
|-----------------|-------------|-----------------|
| `web/fetch` | `web`, `fetch` | Atlas, Prometheus, Afrodita-UX, Afrodita-subagent, Oracle |
| `execute/runInTerminal` | `execute` | Atlas, Sisyphus, Afrodita-UX, Afrodita-subagent, Hephaestus, Atenea, many plugin agents |
| `execute/getTerminalOutput` | `execute` (deduplicate) | Atlas, Sisyphus, Hephaestus, many plugin agents |
| `read/terminalLastCommand` | `read` | Atlas, Sisyphus, Afrodita-UX, Afrodita-subagent, Hephaestus |
| `read/terminalSelection` | `read` (deduplicate) | Same as above |
| `read/problems` | `problems` | Sisyphus |
| `search/changes` | `changes` | Sisyphus |
| `runCommands` | `execute` | Afrodita (plugin conductor), UX-Atlas, Automation-Atlas |

> Deduplication rule: if corrected name already appears in the list, remove the duplicate. Final tool list must have only unique values.

---

## Memory Protocol (Standard Template for All L1 Gods)

Every L1 god agent file must include this section in its system prompt:

```markdown
## Memory Protocol

**On init (mandatory, first action):**
1. Read `.specify/memory/session-memory.md` for active session context.
2. Read `.specify/memory/decision-log.md` for architectural decisions affecting this domain.
3. If MCP `memory` tool is available: call `search_nodes` with relevant entities.

**On complete (mandatory, last action before handoff):**
1. Append key context, decisions, and blockers to `.specify/memory/session-memory.md`.
2. If an architectural decision was made, append it to `.specify/memory/decision-log.md`.
3. If MCP `memory` tool is available: call `add_observations` with outcomes.
```

---

## MCP Configuration (`.vscode/mcp.json`)

```json
{
  "servers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "type": "stdio"
    }
  }
}
```

> Note: If `.vscode/mcp.json` already exists, merge this entry into the existing `"servers"` object.

---

## Atlas L0 Routing Policy (Target State)

```yaml
# Atlas.agent.md frontmatter (target)
agents:
  - Prometheus
  - Sisyphus
  - Themis
  - Argus
  - Hermes
  - Oracle
  - Atenea
  - Ariadna
  - Clio
  - Hephaestus
  - Afrodita-UX
  - Hermes-subagent
  - Oracle-subagent
  - Sisyphus-subagent
  - Afrodita-subagent
  - Argus-subagent
  - Themis-subagent
  - Hephaestus-subagent
```

Routing policy section content change: add explicit prohibition "**Never call Layer 2 specialists directly.** All specialists are accessed exclusively through their L1 god domain conductor."

---

## Layer Metadata Comment Convention

Every agent file must include a `<!-- layer: N -->` comment immediately after the closing `---` of the frontmatter block, where N is 0, 1, or 2. Example:

```
---
name: Service-Builder
...
---
<!-- layer: 2 | parent: Sisyphus > Backend-Atlas -->
```

The validation script `validate_layer_hierarchy.py` uses this comment to assign and verify layers.

---

## New Files to Create

### New agent files
| File | Layer | Parent | Purpose |
|------|-------|--------|---------|
| `plugins/qa-workflow/agents/Test-Runner.agent.md` | 2 | Argus | Execute targeted test commands and report |
| `plugins/qa-workflow/agents/Coverage-Analyst.agent.md` | 2 | Argus | Measure and report test coverage gaps |
| `plugins/qa-workflow/agents/Mutation-Tester.agent.md` | 2 | Argus | Run mutation testing for high-risk logic |
| `plugins/security-workflow/agents/Compliance-Checker.agent.md` | 2 | Atenea | Policy and regulatory compliance audit |
| `plugins/security-workflow/agents/Secret-Scanner.agent.md` | 2 | Atenea | Detect secrets and credentials in code |
| `plugins/devops-workflow/agents/Cost-Optimizer.agent.md` | 2 | Hephaestus > DevOps-Atlas | Cloud resource cost analysis and optimization |
| `plugins/devops-workflow/agents/Incident-Responder.agent.md` | 2 | Hephaestus > DevOps-Atlas | Structured incident response and RCA |
| `plugins/automation-mcp-workflow/agents/n8n-Connector.agent.md` | 2 | Hephaestus > Automation-Atlas | Generate n8n workflow JSON via MCP |
| `plugins/memory-system/agents/Memory-Guardian.agent.md` | 2 | Prometheus | Memory capture, compression, and retrieval |

### New validation scripts
| File | Purpose | Test count target |
|------|---------|-------------------|
| `scripts/validate_tool_names.py` | Check all agents use only valid VS Code tool names | ≥20 test cases |
| `scripts/validate_layer_hierarchy.py` | Check all agents have layer metadata; no orphans | ≥25 test cases |
| `scripts/test_validate_tool_names.py` | Tests for tool name validator | ≥20 |
| `scripts/test_validate_layer_hierarchy.py` | Tests for layer validator | ≥25 |

### Registry and config updates
| File | Change |
|------|--------|
| `.github/plugin/pack-registry.json` | Add `qa-workflow`, `security-workflow`, `memory-system` entries with `parentGod` field |
| `.github/plugin/marketplace.json` | Add catalog entries for new packs |
| `.vscode/settings.json` | Add new agent path entries for new packs |
| `.vscode/mcp.json` | Create with `@modelcontextprotocol/server-memory` MCP server |

### Knowledge assets
| File | Purpose |
|------|---------|
| `plugins/ux-enhancement-workflow/skills/industry-verticals.md` | 161 industry category UX patterns |
| `plugins/automation-mcp-workflow/templates/n8n-workflow-examples.md` | n8n workflow template patterns |

### Demo
| File | Purpose |
|------|---------|
| `demos/hierarchy-architecture-demo/DEMO_PROMPT.md` | Runnable demo exercising full 3-layer hierarchy |
| `demos/hierarchy-architecture-demo/tests/` | ≥24 test cases verifying hierarchy behavior |

---

## Files to Modify

### Phase 2 (Atlas L0)
- `.github/agents/Atlas.agent.md` — Replace `agents: ["*"]` with explicit L1 list; fix tool names; add layer prohibition rule
- `plugins/atlas-orchestration-team/agents/Atlas.agent.md` — Identical update for parity

### Phase 3 (Layer 1 Gods — 10 canonical gods + Afrodita-UX)
For each of the 11 canonical gods × 2 locations = **22 files**:
- `.github/agents/<God>.agent.md`
- `plugins/atlas-orchestration-team/agents/<God>.agent.md`

Plus 7 root-only alias files (`.github/agents/` only) = **7 files**

### Phase 4 (Layer 2 Conductors)
- `plugins/backend-workflow/agents/Backend-Atlas.agent.md` — `user-invocable: false`; parent reference; explicit `agents:` list; fix tool names
- `plugins/data-workflow/agents/Data-Atlas.agent.md` — Same
- `plugins/devops-workflow/agents/DevOps-Atlas.agent.md` — Same
- `plugins/automation-mcp-workflow/agents/Automation-Atlas.agent.md` — Same; fix `runCommands`→`execute`
- `plugins/frontend-workflow/agents/Afrodita.agent.md` — Same; fix `runCommands`→`execute`
- `plugins/ux-enhancement-workflow/agents/UX-Atlas.agent.md` — Same

---

## Open Questions

1. **Should a "Mnemo" L1 god be created for memory/cross-cutting?**
   - **Option A:** Create Mnemo (new L1 god for memory, observability, shared knowledge graph). Pros: clean ownership, dedicated domain. Cons: adds complexity, requires updating Atlas routing.
   - **Option B (chosen):** Prometheus retains memory ownership (already manages `.specify/memory/`). Conservative default.
   - **Recommendation:** Option B for this plan. Revisit if memory management becomes a bottleneck.

2. **Should Hermes and Oracle have explicit L2 pack agents?**
   - **Option A:** Create dedicated "Research Pack" with domain planners as Oracle L2. Pros: clean hierarchy. Cons: planners duplicated.
   - **Option B (chosen):** Hermes and Oracle are self-sufficient; they rely on their tools (`search`, `usages`, `web`, `fetch`). No L2 pack needed. Existing planners remain in their domain packs.
   - **Recommendation:** Option B. Planners serve their domain conductors; Oracle does not need to orchestrate them.

3. **Should `claude-mem` server startup be automated?**
   - **Option A:** Add a VS Code task or script to start the SQLite+ChromaDB server. Pros: seamless. Cons: external runtime dependency.
   - **Option B (chosen):** Document the startup procedure in `research.md` and `memory-system/README.md`. The `.specify/memory/*.md` files remain the primary memory backend; MCP server is opt-in.
   - **Recommendation:** Option B for now. Production memory architecture can be elevated in a follow-up.

---

## Risks and Mitigation

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Parity validator fails after Phase 3 edits | High | Run `validate_atlas_pack_parity.py` at the END of Phase 3 as acceptance criteria |
| `validate_plugin_packs.py` breaks due to new `user-invocable: false` in conductors | Medium | Update validator to allow conductors to be non-user-invocable in Phase 7 |
| Invalid tool names in newly created agents | Medium | Phase 7 `validate_tool_names.py` catches any missed entries |
| Phase 3 creates 29 file edits — large surface area | High | Each god is an independent sub-task; run parity check after each god update |
| `.vscode/mcp.json` conflicts with existing workspace config | Low | Phase 5 checks existence before writing; merge strategy documented |
| n8n MCP server not available in environment | Medium | `n8n-Connector` agent is flagged as requiring n8n MCP server; ships with `enabled: false` by default |
