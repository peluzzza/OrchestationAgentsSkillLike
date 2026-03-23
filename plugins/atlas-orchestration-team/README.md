# Atlas Orchestration Team

Core end-to-end orchestration pack for plan → implement → review → verify flows.

This is the optional distribution-pack form of the repository's Atlas-style multi-agent workflow. It mirrors the root-first orchestration philosophy while remaining installable as a standalone pack through the marketplace surface.

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

Use marketplace mode or plugin-path mode if you want this pack as an optional distribution source. The canonical root-first experience still lives in `.github/agents`.

## Notes

- Root `.github/agents` remains canonical.
- This pack is a distribution/mirroring surface, not the authoritative source of truth.
- Memory continuity is shared through `.specify/memory/`.
