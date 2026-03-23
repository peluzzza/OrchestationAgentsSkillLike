# External Agent Sources — Evaluation Report

**Date:** 2026-03-23  
**Author:** Memory-Guardian (memory-system)  
**Purpose:** Assess five external agent/capability repositories for integration potential. Determine what is already integrated, what is non-duplicate and worth adding, and what duplicates existing system capabilities.

---

## Summary Table

| Source Repo | Agents / Files Evaluated | Already Integrated | Net New (non-duplicate) | Verdict |
|---|---|---|---|---|
| superpower-claude (superhuman) | ~8 agent packs, modular packaging patterns | Packaging conventions applied system-wide | 1 (observability pack pattern) | PARTIAL |
| everything-claude-code (lllyasviel) | Delegation ergonomics, code-critique agents | Delegation patterns applied to Atlas + pack conductors | 0 | DUPLICATE |
| UI-UX-Pro-Max (unknown/community) | UX research, deep-critique, accessibility agents | UX knowledge base (industry-verticals.md) <!-- SOURCE: UI-UX Pro Max --> | 0 additional | INTEGRATED |
| claude-mem / thedotmack | Memory architecture, session + decision log pattern | Memory-Guardian agent + `.specify/memory/` structure <!-- SOURCE: thedotmack/claude-mem --> | 0 | INTEGRATED |
| n8n-mcp (community) | n8n workflow automation via MCP connector | n8n-Connector agent + workflow templates <!-- SOURCE: n8n-mcp --> | 0 | INTEGRATED |

**Totals:** 5 sources evaluated · 3 fully integrated · 1 partial · 1 duplicate-only

---

## Detailed Evaluation

### Superpower Claude <!-- SOURCE: superpower-claude -->

| Source Repo | Agent / Capability | Equivalent in This System | Verdict |
|---|---|---|---|
| superpower-claude | Modular pack packaging (README + agents/ folder structure) | All plugin packs follow this structure | DUPLICATE |
| superpower-claude | Subagent invocation via `agent` tool | All pack conductors use `agent` tool | DUPLICATE |
| superpower-claude | Context-conservation delegation policy | `## 2) Context Conservation Strategy` in every conductor | DUPLICATE |
| superpower-claude | Observability / metrics agent pattern (run-summary node) | Not present as a standalone agent in any pack | NON-DUPLICATE |
| superpower-claude | Dynamic agent discovery at runtime (buscador pattern) | `## 1) Agent Buscador` in every conductor | DUPLICATE |

**Assessment:** The core packaging, delegation, and buscador conventions were directly inspired by this source and are fully applied. The one non-duplicate capability — a dedicated **Observability agent** that tracks run summaries and emits metrics — is not present. Worth considering in a future phase, but low priority given the `.specify/memory/decision-log.md` already captures durable decisions.

---

### Everything Claude Code <!-- SOURCE: everything-claude-code -->

| Source Repo | Agent / Capability | Equivalent in This System | Verdict |
|---|---|---|---|
| everything-claude-code | Delegation ergonomics: parallel subagent calls | Documented in conductor prompts | DUPLICATE |
| everything-claude-code | Code-critique specialist agent | `Design-Critic` (UX), `Code-Reviewer` equivalent in QA pack | DUPLICATE |
| everything-claude-code | Start-of-run context paragraph | `## 0) Start Of Run` in every conductor | DUPLICATE |
| everything-claude-code | Handoff-to-Afrodita pattern | Routing policy in UX-Atlas, Backend-Atlas | DUPLICATE |
| everything-claude-code | Test-generation subagent | `QA-Atlas` + `Test-Generator` in qa-workflow | DUPLICATE |

**Assessment:** This source contributed the delegation ergonomics pattern which is now systemic. No net-new capability is present that is not already covered by existing agents. Integration considered complete.

---

### UI-UX Pro Max <!-- SOURCE: UI-UX Pro Max -->

| Source Repo | Agent / Capability | Equivalent in This System | Verdict |
|---|---|---|---|
| UI-UX Pro Max | Deep UX research agent | `UX-Planner` | DUPLICATE |
| UI-UX Pro Max | Heuristic critique agent | `Design-Critic` | DUPLICATE |
| UI-UX Pro Max | Accessibility review agent | `Accessibility-Heuristics` | DUPLICATE |
| UI-UX Pro Max | Industry-vertical UX knowledge base | `plugins/ux-enhancement-workflow/skills/industry-verticals.md` | INTEGRATED |
| UI-UX Pro Max | Frontend handoff spec packaging | `Frontend-Handoff` | DUPLICATE |

**Assessment:** All agent patterns from this source are covered. The industry-vertical knowledge base was the one genuinely additive artefact and has been created as `industry-verticals.md` in Phase 6. No further integration needed.

---

### claude-mem / thedotmack <!-- SOURCE: thedotmack/claude-mem -->

| Source Repo | Agent / Capability | Equivalent in This System | Verdict |
|---|---|---|---|
| thedotmack/claude-mem | Session memory file (`session-memory.md`) | `.specify/memory/session-memory.md` | INTEGRATED |
| thedotmack/claude-mem | Decision log / durable memory | `.specify/memory/decision-log.md` | INTEGRATED |
| thedotmack/claude-mem | Memory guardian agent (reads/writes memory) | `Memory-Guardian` agent in `memory-system` pack | INTEGRATED |
| thedotmack/claude-mem | Knowledge graph via MCP memory server | `.vscode/mcp.json` (MCP memory server) | INTEGRATED |
| thedotmack/claude-mem | Memory namespace isolation per task | `/memories/session/` vs `/memories/repo/` convention | PARTIAL |

**Assessment:** The core 3-level memory architecture (session / decision-log / MCP graph) is fully integrated. Namespace isolation per task is partially addressed through the session-memory convention but is not enforced programmatically. No blocking gaps remain.

---

### n8n-mcp <!-- SOURCE: n8n-mcp -->

| Source Repo | Agent / Capability | Equivalent in This System | Verdict |
|---|---|---|---|
| n8n-mcp | MCP server for n8n workflow creation | Referenced in `.vscode/mcp.json`, consumed by `n8n-Connector` | INTEGRATED |
| n8n-mcp | n8n workflow template patterns | `plugins/automation-mcp-workflow/templates/n8n-workflow-examples.md` | INTEGRATED |
| n8n-mcp | Webhook trigger patterns | Template 1 and Template 3 in n8n-workflow-examples.md | INTEGRATED |
| n8n-mcp | Schedule trigger patterns | Template 2 in n8n-workflow-examples.md | INTEGRATED |
| n8n-mcp | Agent-to-n8n round-trip bridge | Template 5 (Agent-to-n8n Bridge) in n8n-workflow-examples.md | INTEGRATED |
| n8n-mcp | n8n-Connector specialist agent | `plugins/automation-mcp-workflow/agents/n8n-Connector.agent.md` | INTEGRATED |

**Assessment:** Full integration. The `n8n-Connector` agent and the workflow template library cover all identified n8n-mcp capability patterns.

---

## Integration Decisions

The following non-duplicate capabilities were identified as worth integrating (now or in a future phase):

| Capability | Source | Status | Recommended Phase |
|---|---|---|---|
| Observability / run-metrics agent | superpower-claude | **Not yet integrated** | Phase 7+ |
| Per-task memory namespace enforcement | thedotmack/claude-mem | Partially addressed | Phase 7+ |

**Already integrated in Phase 6:**

- `n8n-Connector` agent (from `n8n-mcp`) <!-- SOURCE: n8n-mcp -->
- `Memory-Guardian` agent (from `thedotmack/claude-mem`) <!-- SOURCE: thedotmack/claude-mem -->
- Industry-vertical UX knowledge base `industry-verticals.md` (from `UI-UX Pro Max`) <!-- SOURCE: UI-UX Pro Max -->
- n8n workflow template library (from `n8n-mcp`) <!-- SOURCE: n8n-mcp -->

---

## Notes & Caveats

- Evaluation is based on documented agent instructions and README descriptions. No source code execution was performed.
- "DUPLICATE" verdict means the **capability** is covered, not necessarily that the source's exact implementation was copied.
- "PARTIAL" means the capability is present in a limited or non-enforced form.
- This document should be updated when new external sources are evaluated or when integration status changes.
- Superpower Claude packaging conventions are pervasive and credited in every pack README under "Donor inspiration".
