# Feature Specification: Layered Agent Hierarchy

**Feature Branch**: `layered-agent-hierarchy`
**Created**: 2026-03-23
**Status**: READY_FOR_PLANNING: true
**Input**: Task: Design and implement a strict 3-layer agent architecture with external source integration and persistent memory for the VS Code Copilot agent system.

---

## Constitution Check

*Verified against `.specify/memory/constitution.md`.*

- [x] Spec-Driven Development gate: spec completes before any plan or implementation begins
- [x] Scope is bounded to a single feature slug — no cross-feature pollution
- [x] At most 3 `[NEEDS CLARIFICATION]` markers permitted

**Constitution violations to document in Plan:**

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Conductor-First Visibility | PASS | Pack conductors `user-invocable: true` → changing to `false` in Phase 4 aligns this |
| II. Spec-Driven Development | PASS | This spec precedes all implementation |
| III. Progressive Delegation | PASS | Hierarchy enforces delegation chains |
| IV. Atomic Task Execution | PASS | Each phase is independently verifiable |
| V. Root-First Bootstrap | PASS | `.specify/` exists; structure conformant |
| VI. Gate-Based Progression | PASS | SP-5 gate applied; Phase gates defined per phase |
| VII. Human Sovereignty | PASS | Human approves before Atlas executes each phase |

---

## Problem Statement

The current agent system lacks a strict layer model:

1. **Atlas calls any agent** — `agents: ["*"]` in Atlas frontmatter allows direct calls to L2 specialists, bypassing L1 orchestrators.
2. **Pack conductors are user-invocable** — `Afrodita`, `Backend-Atlas`, `DevOps-Atlas`, `UX-Atlas`, `Automation-Atlas` all have `user-invocable: true`, violating Constitution Principle I.
3. **Invalid tool declarations** — 20+ agent files use unsupported VS Code tool name patterns like `web/fetch`, `execute/runInTerminal`, `read/terminalLastCommand`, `search/changes`, `runCommands`.
4. **No persistent cross-session memory** — Memory files exist but no MCP knowledge graph; L1 gods inconsistently use them.
5. **Layer ownership gaps** — Argus has no L2 QA specialists; Atenea has no security specialists beyond what back-office packs provide; Hephaestus has no dedicated ops response agents.
6. **No hierarchy enforcement** — No validation script checks layer compliance; no `layer` assignment in agent metadata.

---

## User Stories & Testing

### User Story 1 — Atlas Layer-0 Boundary Enforcement (Priority: P1)

As a developer using this agent system, I want Atlas to only interact with Layer 1 gods so that no specialist agent is accidentally called directly without domain context.

**Why this priority**: Core architectural rule. All other hierarchy guarantees depend on Atlas respecting its boundary.

**Independent Test**: Can be fully tested by inspecting `Atlas.agent.md` frontmatter and verifying the `agents:` list contains **only** the 12 L1 gods (+ their `-subagent` aliases). No L2 pack specialists, no Specify agents (those belong to Prometheus).

**Acceptance Scenarios**:

1. **Given** Atlas.agent.md frontmatter, **When** reading the `agents:` list, **Then** every entry is an L1 god name (Prometheus, Sisyphus, Themis, Argus, Hermes, Oracle, Atenea, Ariadna, Clio, Hephaestus, Afrodita-UX) or an approved alias (-subagent variants).
2. **Given** Atlas routing policy section, **When** reading routing directives, **Then** NO L2 agent (Backend-Atlas, Service-Builder, UI-Designer, etc.) is mentioned as a direct target.
3. **Given** Atlas.agent.md in both `.github/agents/` and `plugins/atlas-orchestration-team/agents/`, **When** comparing content, **Then** both files are identical (parity rule preserved).

---

### User Story 2 — Layer-1 Domain Orchestrators with Explicit L2 Routing (Priority: P1)

As a system architect, I want each L1 god to have an explicit, bounded list of its L2 agents so that every specialist belongs to exactly one command chain.

**Why this priority**: Without explicit ownership, specialists float between chains, duplicating context and breaking auditability.

**Independent Test**: Each L1 god file has (a) an explicit `agents:` list containing only its L2 agents, and (b) a "Layer 2 Roster" section in its system prompt naming every specialist it can invoke.

**Acceptance Scenarios**:

1. **Given** `Prometheus.agent.md`, **When** checking `agents:` list, **Then** it contains exactly the 7 Specify agents and no others.
2. **Given** `Sisyphus.agent.md`, **When** checking `agents:` list, **Then** it contains Backend-Atlas and Data-Atlas (its L2 conductors) and no other non-Specify agents.
3. **Given** `Hephaestus.agent.md`, **When** checking `agents:` list, **Then** it contains DevOps-Atlas and Automation-Atlas and no L2 specialists from Sisyphus's domain.
4. **Given** `Afrodita-UX.agent.md`, **When** checking `agents:` list, **Then** it contains Afrodita (plugin conductor) and UX-Atlas and no backend specialists.
5. **Given** any L1 god file, **When** checking system prompt, **Then** a "Layer 2 Roster" section exists listing exactly the same agents as the `agents:` frontmatter.

---

### User Story 3 — Valid VS Code Tool Declarations in All Agent Files (Priority: P1)

As a developer loading agent files in VS Code Copilot, I want all `tools:` frontmatter entries to use only the valid tool names supported by VS Code so that no agent silently fails due to an unrecognised tool.

**Why this priority**: Invalid tool names cause silent failures in VS Code agent runtime. This is a correctness issue affecting all 89 agent files.

**Valid tool names**: `agent`, `search`, `usages`, `problems`, `changes`, `testFailure`, `web`, `fetch`, `edit`, `execute`, `read`, `mcp`

**Independent Test**: Run `scripts/validate_tool_names.py` and expect zero violations across all agent files.

**Acceptance Scenarios**:

1. **Given** any agent file in `.github/agents/`, **When** reading the `tools:` list in frontmatter, **Then** every entry is in the valid set above.
2. **Given** any agent file in `plugins/**/agents/`, **When** reading the `tools:` list, **Then** every entry is in the valid set above.
3. **Given** the known invalid patterns, **When** searching repo-wide, **Then** zero occurrences of `web/fetch`, `execute/runInTerminal`, `execute/getTerminalOutput`, `read/terminalLastCommand`, `read/terminalSelection`, `read/problems`, `search/changes`, `runCommands`.

---

### User Story 4 — Persistent Three-Level Memory Protocol (Priority: P2)

As an L1 god agent, I want to read session context at the start of each run and write key observations at the end so that knowledge persists across multi-session workflows.

**Why this priority**: Without memory continuity, each agent invocation starts cold, re-discovering context and repeating decisions.

**Independent Test**: Every L1 god file contains a "Memory Protocol" section with explicit read-on-init and write-on-complete instructions referencing the three memory levels.

**Acceptance Scenarios**:

1. **Given** any L1 god agent file, **When** reading its system prompt, **Then** a "Memory Protocol" section exists with read + write instructions.
2. **Given** `.vscode/mcp.json`, **When** checking its contents, **Then** a `@modelcontextprotocol/server-memory` MCP server entry exists.
3. **Given** the memory file `.specify/memory/session-memory.md`, **When** any L1 god completes a run, **Then** the file is updated with a new entry following the standard template.
4. **Given** `.specify/memory/decision-log.md`, **When** an architectural decision is made, **Then** it is appended with date, decision, rationale, and consequences.

---

### User Story 5 — Layer Assignment Metadata and Validation (Priority: P2)

As a workspace maintainer, I want every agent file to carry a `layer` metadata comment and a validation script to check hierarchy compliance so that orphaned agents cannot be introduced silently.

**Why this priority**: Without enforcement, future agent additions will drift from the hierarchy.

**Independent Test**: Run `scripts/validate_layer_hierarchy.py` — expects every agent to have a known layer assignment (0, 1, or 2) and zero orphans.

**Acceptance Scenarios**:

1. **Given** all agent files, **When** running `validate_layer_hierarchy.py`, **Then** exit code 0 and report: Layer 0: 1, Layer 1: 18 (11 gods + 7 aliases), Layer 2: 70+.
2. **Given** a new agent file with no layer comment, **When** running the validator, **Then** it errors with `ORPHAN` status.
3. **Given** `pack-registry.json`, **When** checking each pack, **Then** every pack has a `parentGod` field naming its L1 owner.

---

### User Story 6 — External Agent Integration (claude-night-market, claude-mem) (Priority: P3)

As a project contributor, I want evaluated and adapted agents from `athola/claude-night-market` and the `thedotmack/claude-mem` memory system integrated where they are non-duplicative so that the system gains proven patterns without redundancy.

**Why this priority**: Reduces build effort for proven patterns; expands capability of the agent ecosystem.

**Independent Test**: New agents from external sources are present in `plugins/` with a `<!-- SOURCE: <repo> -->` comment in their frontmatter section and passing validation.

**Acceptance Scenarios**:

1. **Given** the `plugins/memory-system/` pack, **When** examining its agents, **Then** at least one Memory-Guardian agent exists implementing claude-mem session capture protocol.
2. **Given** any imported agent from claude-night-market, **When** comparing with existing agents, **Then** no functional duplication exists (confirmed in `research.md`).
3. **Given** `pack-registry.json`, **When** checking new entries, **Then** `memory-system` pack has `shipped: true`.

---

### User Story 7 — UX Industry Knowledge Base and n8n Automation Integration (Priority: P3)

As a UX or automation specialist using this system, I want Afrodita-UX/UX-Atlas to have rich industry-vertical knowledge and Automation-Atlas to be capable of generating real n8n workflows so that domain-specific work produces richer outputs.

**Why this priority**: Extends depth of two major specialist domains; completes promised P3 features.

**Independent Test**: `plugins/ux-enhancement-workflow/skills/industry-verticals.md` exists with ≥10 industry categories; `plugins/automation-mcp-workflow/agents/n8n-Connector.agent.md` exists with n8n MCP configuration.

**Acceptance Scenarios**:

1. **Given** `plugins/ux-enhancement-workflow/skills/industry-verticals.md`, **When** reading content, **Then** it covers at least 10 industry verticals with UX patterns per category.
2. **Given** `.vscode/mcp.json`, **When** checking MCP server entries, **Then** an n8n MCP server configuration exists.
3. **Given** `Automation-Atlas.agent.md`, **When** reading routing policy, **Then** `n8n-Connector` is listed as a specialist for n8n workflow generation.

---

### User Story 8 — Hierarchy Architecture Demo and Test Suite (Priority: P3)

As a developer evaluating the system, I want a runnable demo that exercises the full 3-layer hierarchy so I can verify it works end-to-end and serve as a regression anchor.

**Why this priority**: Demos act as living documentation and regression baselines. Validates the complete architecture.

**Independent Test**: `demos/hierarchy-architecture-demo/DEMO_PROMPT.md` runs successfully through all 3 layers; associated test suite has ≥24 test cases.

**Acceptance Scenarios**:

1. **Given** `demos/hierarchy-architecture-demo/DEMO_PROMPT.md`, **When** the demo is triggered, **Then** Atlas routes to ≥3 distinct L1 gods.
2. **Given** the demo test suite, **When** running all tests, **Then** ≥24 pass.
3. **Given** the full test suite (existing + new), **When** running all tests, **Then** total count ≥ 250.

---

### Edge Cases

- What if a pack has no god parent assigned? → `validate_layer_hierarchy.py` must surface this as `ORPHAN`.
- What if Atlas's `agents:` list in one file diverges from the canonical shared source? → `validate_atlas_pack_parity.py` catches this.
- What if a L2 conductor still declares `user-invocable: true` after Phase 4? → `validate_plugin_packs.py` must be updated to check for this.
- What if `.vscode/mcp.json` already existed with other servers? → The plan must merge, not overwrite.
- What if `claude-mem` (TypeScript, SQLite, ChromaDB, embeddings) requires a running server? → Document as "opt-in" memory backend; the standard `.specify/memory/*.md` files remain the primary fallback.

---

## Out of Scope

- No changes to `spec-kit/` (external upstream project).
- No changes to demo files other than adding `hierarchy-architecture-demo`.
- No implementation of production code unrelated to agent configuration files.
- Full implementation of `claude-mem` server setup (startup script is out of scope — document approach only in `research.md`).
- Creation of a new L1 "Mnemo" god — Prometheus handles memory ownership (conservative default; see Open Questions in `plan.md`).

---

**READY_FOR_PLANNING: true**
**NEEDS_CLARIFICATION: none** <!-- All ambiguities resolved with conservative defaults per SP-3 fallback -->
