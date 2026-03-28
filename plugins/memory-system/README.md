# Memory System

Multi-level persistent memory management pack. Provides session memory, decision log, and MCP knowledge graph maintenance for the shared runtime memory surface.

## Architecture

```
Prometheus (L1 God — Planning + Specification)
    └── memory-system pack
        └── Memory-Guardian  (Session capture, retrieval, and compression)
```

## Memory Levels

| Level | File | Purpose |
|-------|------|---------|
| 1 | `.specify/memory/session-memory.md` | Current session context, in-progress tasks |
| 2 | `.specify/memory/decision-log.md` | Key architectural decisions and rationale |
| 3 | MCP Knowledge Graph | Structured entity and relation graph |

## Agents

| Agent | Role | Invoked By |
|-------|------|-----------|
| **Memory-Guardian** | Capture, retrieve, and compress agent memory | Prometheus (explicit maintenance flows) |

## Prerequisites

- Level 3 (MCP knowledge graph) requires `@modelcontextprotocol/server-memory` configured in `.vscode/mcp.json`. **`.vscode/mcp.json` is now present in this repository** — run `npx -y @modelcontextprotocol/server-memory` to verify the server is available.
- Levels 1 and 2 work with local markdown files only.

## Usage

This pack is invoked by `Prometheus` for explicit maintenance flows. Zeus consumes the derived hook-refreshed snapshot at `.specify/memory/zeus-context.md` instead of delegating directly to Memory-Guardian. It is not user-invocable.

Enable in `.vscode/settings.json`:
```json
"chat.agentFilesLocations": [
  "plugins/memory-system/agents"
]
```
