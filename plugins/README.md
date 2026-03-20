# Agent Workflow Packs

This directory contains specialized multi-agent workflow packs following the bigguy345/Github-Copilot-Atlas orchestration pattern.

## Available Workflows

| Workflow | Conductor | Specialists | Purpose |
|----------|-----------|-------------|---------|
| [atlas-orchestration-team](./atlas-orchestration-team/) | Atlas | 19 agents | General-purpose orchestration, Specify pipeline, governance specialists (Security, Documentation, Dependencies) |
| [frontend-workflow](./frontend-workflow/) | Afrodita | 8 agents | UI/UX development |
| [backend-workflow](./backend-workflow/) | Backend-Atlas | 8 agents | API & database development |
| [devops-workflow](./devops-workflow/) | DevOps-Atlas | 8 agents | Infrastructure & CI/CD |
| [data-workflow](./data-workflow/) | Data-Atlas | 8 agents | Data engineering & ML |

## Cross-Workflow Handoffs

Workflows can hand off to each other for complex multi-domain tasks:

```
┌─────────────────┐     ┌─────────────────┐
│ Afrodita  │◄───►│  Backend-Atlas  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         │    ┌──────────────┐   │
         └───►│ DevOps-Atlas │◄──┘
              └──────┬───────┘
                     │
              ┌──────▼───────┐
              │  Data-Atlas  │
              └──────────────┘
```

| From | Can handoff to |
|------|----------------|
| Afrodita | Backend-Atlas, DevOps-Atlas |
| Backend-Atlas | Afrodita, DevOps-Atlas, Data-Atlas |
| DevOps-Atlas | Afrodita, Backend-Atlas, Data-Atlas |
| Data-Atlas | Backend-Atlas, DevOps-Atlas |

## Architecture Pattern

Each workflow follows the **conductor + planner + hidden specialists** pattern:

```
[Workflow]-Atlas (Conductor - User Visible)
    ├── [Workflow]-Planner (Autonomous Planning)
    ├── Specialist-1 (Hidden)
    ├── Specialist-2 (Hidden)
    ├── ...
    └── [Workflow]-Reviewer (Code Review Gate)
    
    Handoffs → Other workflow conductors
```

### Key Features

1. **Single Entry Point**: Only the conductor agent is user-invocable
2. **Autonomous Planning**: Planner agents research and create phased plans
3. **Agent Buscador**: Automatic agent discovery at runtime
4. **Context Conservation**: Delegates heavy work to preserve context
5. **Routing Policies**: Clear rules for which specialist handles what
6. **Output Contracts**: Structured responses from all agents
7. **TDD Discipline**: Tests-first approach in implementation agents
8. **Review Gates**: Code review before completion
9. **Cross-Workflow Handoffs**: Seamless delegation between domains

## Quick Reference

### Frontend Workflow
```
@Afrodita Build a dashboard component with charts
```
Specialists: UI-Designer, Style-Engineer, State-Manager, Component-Builder, A11y-Auditor, Frontend-Reviewer

### Backend Workflow
```
@Backend-Atlas Add user authentication with JWT
```
Specialists: API-Designer, Database-Engineer, Security-Guard, Service-Builder, Performance-Tuner, Backend-Reviewer

### DevOps Workflow
```
@DevOps-Atlas Set up Kubernetes cluster with CI/CD
```
Specialists: Infra-Architect, Pipeline-Engineer, Container-Master, Monitor-Sentinel, Security-Ops, Deploy-Strategist

### Data Workflow
```
@Data-Atlas Build customer analytics pipeline with ML
```
Specialists: Data-Architect, Pipeline-Builder, Analytics-Engineer, ML-Scientist, Data-Quality, Data-Reviewer

## Installation

### Option 1: Workspace (Project-Specific)
Copy desired workflow folders to your project's `.github/agents/` or configure in `.vscode/settings.json`:

```json
{
  "chat.agentFilesLocations": {
    "plugins/frontend-workflow/agents": true,
    "plugins/backend-workflow/agents": true,
    "plugins/devops-workflow/agents": true,
    "plugins/data-workflow/agents": true
  }
}
```

Enable only the workflow-pack locations you actually want active in the workspace to avoid duplicate sources.

### Option 2: User Data (Global)
Copy workflow folders to VS Code user prompts directory:
- **Windows**: `%APPDATA%\Code\User\prompts\`
- **macOS**: `~/Library/Application Support/Code/User/prompts/`
- **Linux**: `~/.config/Code/User/prompts/`

## Requirements

- VS Code Insiders (recommended)
- GitHub Copilot subscription with multi-agent support
- VS Code Settings:
  ```json
  {
    "chat.customAgentInSubagent.enabled": true,
    "github.copilot.chat.responsesApiReasoningEffort": "high"
  }
  ```

## Workflow Selection Guide

| I want to... | Use |
|--------------|-----|
| Build UI components with accessibility | `@Afrodita` |
| Create REST APIs with database | `@Backend-Atlas` |
| Set up cloud infrastructure | `@DevOps-Atlas` |
| Build data pipelines or ML models | `@Data-Atlas` |
| General development tasks | `@Atlas` |

## Agent Model Strategy

Each workflow uses optimized model selection:

| Role | Default Model | Rationale |
|------|---------------|-----------|
| Conductor | Claude Opus 4.5 | Complex orchestration |
| Research | GPT-5.2 | Broad knowledge retrieval |
| Implementation | Claude Sonnet 4.5 | High-quality code |
| Fast Tasks | Gemini 3 Flash | Speed optimization |
| Reviewer | GPT-5.2 | Analytical review |

## Creating Custom Workflows

1. Create folder: `plugins/[workflow-name]/agents/`
2. Create conductor: `[Name]-Atlas.agent.md` with `user-invocable: true`
3. Create specialists: `[Name].agent.md` with `user-invocable: false`
4. Add README.md documenting the workflow
5. Follow the output contract pattern from existing workflows

## License

MIT License - See individual workflow folders for details.
