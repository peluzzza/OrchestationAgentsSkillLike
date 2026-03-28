# Plan: Zeus Memory Continuity

**Created:** 2026-03-25
**Status:** Complete

## Summary

Add a deterministic, hook-backed memory continuity mechanism to the Zeus runtime. Zeus explicitly consults `.specify/memory/zeus-context.md` (a compact derived context snapshot) at run start. The snapshot is refreshed automatically by a `SubagentStart` workspace hook that invokes `scripts/sync_memory_context.py` — no Layer-0 → Layer-2 agent delegation is required.

This approach satisfies the memory continuity requirement without introducing a Zeus → Memory-Guardian direct path that would violate the layer hierarchy.

## Context & Analysis

- Zeus is Layer 0 (sole user-visible conductor).
- Memory-Guardian is Layer 2 (utility). Zeus MUST NOT call Layer 2 agents directly.
- The existing `zeus-subagent-attendance.json` hook uses `SubagentStart` / `SubagentStop` events — the same events are available for the memory context hook.
- `.specify/memory/` contains `session-memory.md` (Level 1) and `decision-log.md` (Level 2). A compact derived context file `zeus-context.md` bridges both without duplicating them.
- Level 3 (MCP knowledge graph) requires `@modelcontextprotocol/server-memory` configured in `.vscode/mcp.json`. The file is created as part of this work.

## Implementation Phases

### Phase 1: Memory context script and hook

**Files:**
- `scripts/sync_memory_context.py` — reads session-memory.md + decision-log.md, writes zeus-context.md
- `scripts/test_sync_memory_context.py` — deterministic tests for the script
- `.github/hooks/zeus-memory-context.json` — SubagentStart hook that invokes the script
- `.vscode/mcp.json` — MCP server-memory configuration for Level 3

**Acceptance criteria:**
- Script writes zeus-context.md with Current Objective, Blockers, Next Likely Moves, and recent decisions.
- Tests pass (16 test cases).
- Hook fires on SubagentStart without conflicting with existing attendance hook.
- MCP config enables Memory-Guardian Level 3 access.

### Phase 2: Agent and doc updates

**Files:**
- `.github/agents/Zeus.agent.md` — Shared Memory Consultation section added
- `.github/agents/Memory-Guardian.agent.md` — MCP-backed Level 3 behavior clarified without unsupported frontmatter tool declarations
- `plugins/memory-system/agents/Memory-Guardian.agent.md` — MCP-backed plugin wording aligned without unsupported frontmatter tool declarations
- `.github/hooks/README.md` — memory-context hook documented
- `.specify/memory/session-memory.md` — stale entries refreshed
- `.specify/memory/decision-log.md` — memory continuity decision recorded
- `README.md` — Shared Memory section updated with zeus-context.md
- `plugins/memory-system/README.md` — mcp.json prerequisite noted as present

**Acceptance criteria:**
- Zeus instructions are self-contained for memory consultation (no agent invocation needed).
- Memory-Guardian documents MCP-backed Level 3 behavior in supported fields/prose without overclaiming unsupported frontmatter tool access.
- Memory files reflect current repo state.

## Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| Hook-backed sync over direct Zeus → Memory-Guardian delegation | Preserves layer hierarchy; Layer 0 must not call Layer 2 |
| SubagentStart event (same as attendance hook) | Only supported hook event pattern in this repo |
| Separate hook file (zeus-memory-context.json) | Keeps attendance concern separate from memory concern |
| zeus-context.md as derived compact snapshot | Zeus gets fast path to prior context without full file read at every run |
| stdlib-only Python | No external dependencies introduced |

## Validation

```shell
python3 -m pytest scripts/test_sync_memory_context.py -q
python3 -m pytest scripts/test_trace_hook_event.py scripts/test_validate_atlas_pack_parity.py scripts/test_validate_layer_hierarchy.py -q
```
