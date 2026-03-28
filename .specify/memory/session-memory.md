# Session Memory

Use this file as the bounded working-memory layer for the current orchestration effort. It is intentionally file-backed, human-readable, and resettable.

## Rules
- Keep entries short and operational.
- Record only active context that will help the next session continue quickly.
- Remove stale notes instead of growing forever.
- Do not duplicate full plans that already live in `plans/` or `.specify/specs/`.

## Current Objective
- Zeus is the stable root conductor (`Layer 0`). Hook attendance is operational. Memory continuity (`zeus-context.md` + MCP `server-memory`) just landed.
- Next batch: CI wiring for repository validators.

## Active Repositories
- `review_clones/OrchestationAgentsSkillLike` — target orchestration repo

## In-Flight Decisions
- `.github/agents` is the authoring and runtime source of truth for this clone; `plugins/` remains compatibility/distribution material unless explicitly reactivated.
- Memory is 3-level: `session-memory.md` (L1), `decision-log.md` (L2), MCP knowledge graph (L3 via `.vscode/mcp.json`).
- Zeus reads `zeus-context.md` first (compact hook-refreshed snapshot); falls back to `session-memory.md`.
- Zeus MUST NOT invoke Memory-Guardian directly (Layer-0 → Layer-2 violation). All maintenance routed through Prometheus.

## Current Batch
- Zeus memory continuity landed: `sync_memory_context.py`, `zeus-memory-context.json` hook, `zeus-context.md` snapshot, `.vscode/mcp.json`, Memory-Guardian updated, all docs updated.

## Next Likely Moves
- Add CI wiring for `test_validate_atlas_pack_parity.py`, `test_validate_layer_hierarchy.py`, `test_trace_hook_event.py`, and `test_sync_memory_context.py`.
- Reuse the parity-validator pattern if more mirrored packs become marketplace surfaces.
- Keep `.github/agents` authoritative in this clone and treat plugin-pack paths as optional distribution metadata.

## Blockers
- None currently documented.

## Cleanup Guidance
- At the end of each meaningful batch, replace outdated notes with a compact fresh summary.
