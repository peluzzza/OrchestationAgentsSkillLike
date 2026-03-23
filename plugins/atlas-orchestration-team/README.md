# Atlas Orchestration Team

Core end-to-end orchestration pack for plan → implement → review → verify flows.

This is the canonical shared source for the repository's 19-agent Atlas orchestration pack. The root `.github/agents` surface stays active by default for zero-setup use, but its shared files are expected to remain synced from this pack while preserving 7 root-only compatibility aliases.

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
