# Memory System

Multi-level persistent memory management pack. Provides session memory, decision log, and MCP knowledge graph capabilities to the Prometheus planning god.

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
| **Memory-Guardian** | Capture, retrieve, and compress agent memory | Prometheus |

## Prerequisites

- Level 3 (MCP knowledge graph) requires `@modelcontextprotocol/server-memory` configured in `.vscode/mcp.json`.
- Levels 1 and 2 work with local markdown files only.

## Usage

This pack is invoked by the `Prometheus` canonical god agent. It is not user-invocable.

Enable in `.vscode/settings.json`:
```json
"chat.agentFilesLocations": [
  "plugins/memory-system/agents"
]
```
