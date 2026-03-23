# Automation & MCP Workflow

Opt-in plugin pack for automation, Model Context Protocol (MCP) server integration, and multi-step workflow composition.

> **Donor inspiration:** n8n-MCP connector patterns, Superpowers modular packaging, Everything Claude Code delegation ergonomics.
> **Memory contract:** Reads session continuity from `.specify/memory/session-memory.md` and durable decisions from `.specify/memory/decision-log.md`. Does not create a duplicate memory store.

## Architecture

```
Automation-Atlas (Conductor - User Visible)
    ├── Automation-Planner (Autonomous Planning)
    ├── MCP-Integrator (MCP server connection & tool mapping)
    ├── Workflow-Composer (multi-step flow assembly)
    └── Automation-Reviewer (safety & correctness gate)

    Handoffs → Atlas, DevOps-Atlas
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| **Automation-Atlas** | Conductor - orchestrates the team | GPT-5.4 |
| **Automation-Planner** | Autonomous planning for automation tasks | GPT-5.4 |
| **MCP-Integrator** | MCP server setup, tool mapping, protocol wiring | Claude Opus 4.6 |
| **Workflow-Composer** | Multi-step flow assembly and trigger design | Claude Opus 4.6 |
| **Automation-Reviewer** | Safety, correctness, and reversibility gate | Claude Sonnet 4.6 |

## Workflow

1. **Planning Phase**
   - `Automation-Planner` researches integration requirements and produces phased plan
   - User reviews and approves

2. **Integration Phase**
   - `MCP-Integrator` wires MCP server connections and maps available tools
   - `Workflow-Composer` assembles multi-step flows from composed tools

3. **Review Phase**
   - `Automation-Reviewer` checks safety, reversibility, and correctness
   - Returns: APPROVED | NEEDS_REVISION | UNSAFE

4. **Completion**
   - Workflow definitions ready for deployment
   - Safety review passed

## Usage

Enable in `.vscode/settings.json`:

```json
{
  "chat.agentFilesLocations": {
    ".github/agents": true,
    "plugins/automation-mcp-workflow/agents": true
  }
}
```

Then invoke `@Automation-Atlas` in Copilot Chat.

## Installation via Marketplace

```json
{
  "chat.plugins.marketplaces": [
    { "source": "peluzzza/OrchestationAgentsSkillLike" }
  ]
}
```

Install `automation-mcp-workflow` from the marketplace panel, then reload VS Code.

## Non-Overlap

This pack does **not** replace `devops-workflow`. DevOps-Atlas handles infrastructure CI/CD; Automation-Atlas handles application-level workflow orchestration and MCP tool integration.
