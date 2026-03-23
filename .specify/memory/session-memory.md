# Session Memory

Use this file as the bounded working-memory layer for the current orchestration effort. It is intentionally file-backed, human-readable, and resettable.

## Rules
- Keep entries short and operational.
- Record only active context that will help the next session continue quickly.
- Remove stale notes instead of growing forever.
- Do not duplicate full plans that already live in `plans/` or `.specify/specs/`.

## Current Objective
- Stabilize and evolve `OrchestationAgentsSkillLike` as a plugin-authored, root-runtime orchestration repository.
- Merge selected external ecosystem capabilities incrementally by folder.

## Active Repositories
- `review_clones/OrchestationAgentsSkillLike` — target orchestration repo

## In-Flight Decisions
- `plugins/atlas-orchestration-team/agents` is the canonical shared source for the Atlas pack.
- `.github/agents` remains the default-active runtime surface plus root-only aliases.
- Supported packs can ship in-repo while staying available-but-inactive by default.
- Only the root runtime surface is default-active.
- Memory starts file-backed under `.specify/memory/`.
- UX and MCP automation stay outside the core until proven.

## Current Batch
- External ecosystem merge complete through Phase 5: memory, optional packs, demos, and atlas mirror parity all landed.

## Next Likely Moves
- Add CI wiring for the three repository validators.
- Reuse the parity-validator pattern if more mirrored packs become marketplace surfaces.
- Keep plugin-authored shared packs authoritative and sync `.github/agents` after shared changes stabilize.

## Blockers
- None currently documented.

## Cleanup Guidance
- At the end of each meaningful batch, replace outdated notes with a compact fresh summary.
