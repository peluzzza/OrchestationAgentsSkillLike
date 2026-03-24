# Atlas Orchestration Team

> **Note:** The `agents/` subfolder in this pack is intentionally empty. All 79 agents have been consolidated into `.github/agents/` as the single source of truth. This pack folder is retained for repository structure compatibility only.

Core end-to-end orchestration pack for plan → implement → review → verify flows.

The root `.github/agents/` surface is the canonical runtime location for all agents. It contains the full 3-layer hierarchy: Layer 0 (Atlas), Layer 1 (11 domain gods + 7 compatibility aliases), and Layer 2 (60+ domain specialists).

## Purpose

- provide a single visible conductor (`Atlas`)
- delegate planning to `Prometheus`
- route implementation, review, testing, and operations to focused specialists
- preserve context through structured delegation and phased execution

## Conductor

| Agent | Role |
|-------|------|
| `Atlas` | User-invocable conductor for end-to-end orchestration |

## Included Specialist Areas

- planning and specification
- exploration and research
- implementation
- review and QA
- deployment and operations
- documentation, dependency, and security governance

## Installation

Use marketplace mode or plugin-path mode if you want this pack as a standalone installable source. The default zero-setup runtime experience still lives in `.github/agents`, but shared Atlas-pack edits should originate here.

## Notes

- This pack is the authoritative shared source of truth for the 19-agent Atlas orchestration surface.
- Root `.github/agents` remains the default-active runtime copy plus root-only compatibility aliases.
- Memory continuity is shared through `.specify/memory/`.
