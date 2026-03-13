# Atlas Agents For VS Code

This repo is set up so you can start from zero with a simple experience:

- You see only `Atlas` in the agent picker.
- `Atlas` delegates internally to hidden specialist subagents when needed.
- `Atlas` can optionally delegate planning to hidden `Prometheus` for larger tasks.
- No plugin marketplace setup is required for the default flow.

## Install From Zero (60 seconds)

1. Clone this repository.
2. Open the repository folder in VS Code.
3. Make sure Copilot Chat agents are enabled in your environment.
4. Confirm workspace setting `.vscode/settings.json` contains:

```json
{
  "chat.agentFilesLocations": {
    ".github/agents": true
  }
}
```

5. Run `Developer: Reload Window`.
6. Open Copilot Chat and select `Atlas`.
7. Ask for a task (for example: "Plan and implement X with tests").

Done. No extra installation steps are needed.

## What You Should See

- Visible agent: `Atlas` only.
- Hidden agents: `Prometheus`, `Oracle`, `Explorer`, `Sisyphus`, `Argus`, `Code-Review`, `Hephaestus`, `Frontend-Engineer`, `PackCatalog`.
- `Atlas` chooses and calls subagents internally.

## Orchestration Style (Merged)

This setup blends two ideas:

- Skill-style progressive activation: only activate specialist agents when needed.
- Conductor lifecycle: plan -> implement -> review -> verify, with explicit routing by agent specialty.

For medium/large tasks, Atlas can route planning to `Prometheus` and then execute phases with implementation/review/verification specialists.

## Domain-Specific Workflows (NEW)

In addition to the general-purpose `Atlas`, we now have specialized conductors for different domains:

| Workflow | Conductor | Agents | Purpose |
|----------|-----------|--------|---------|
| General | `Atlas` | 10 | General development orchestration |
| Frontend | `Frontend-Atlas` | 8 | UI/UX development (React, Vue, Angular) |
| Backend | `Backend-Atlas` | 8 | API & database development (Spring, Express, FastAPI) |
| DevOps | `DevOps-Atlas` | 8 | Infrastructure & CI/CD (Terraform, K8s, GitHub Actions) |
| Data | `Data-Atlas` | 8 | Data engineering & ML (dbt, Spark, ML pipelines) |

### Enable Domain Workflows

Add to `.vscode/settings.json`:

```json
{
  "chat.agentFilesLocations": {
    ".github/agents": true,
    "plugins/frontend-workflow/agents": true,
    "plugins/backend-workflow/agents": true,
    "plugins/devops-workflow/agents": true,
    "plugins/data-workflow/agents": true
  }
}
```

Then reload VS Code. You'll see these conductors in the agent picker:
- `@Atlas` - General orchestration
- `@Frontend-Atlas` - UI/UX tasks
- `@Backend-Atlas` - API/Database tasks
- `@DevOps-Atlas` - Infrastructure/CI-CD tasks
- `@Data-Atlas` - Data pipelines/ML tasks

### Cross-Workflow Handoffs

Workflows can hand off to each other:
- `Frontend-Atlas` → `Backend-Atlas`, `DevOps-Atlas`
- `Backend-Atlas` → `Frontend-Atlas`, `DevOps-Atlas`, `Data-Atlas`
- `DevOps-Atlas` → `Frontend-Atlas`, `Backend-Atlas`, `Data-Atlas`
- `Data-Atlas` → `Backend-Atlas`, `DevOps-Atlas`

See [plugins/README.md](plugins/README.md) for detailed documentation.

## Optional: Marketplace / Plugin Packs

Use this only if you want distribution through plugin packs. It is not required for normal use.

- Marketplace definition: `.github/plugin/marketplace.json`
- Plugin packs: `plugins/atlas-orchestration-team`, `plugins/agent-pack-catalog`
- Domain workflow packs: `plugins/frontend-workflow`, `plugins/backend-workflow`, `plugins/devops-workflow`, `plugins/data-workflow`
- Sync helper script: `scripts/sync_agent_packs.ps1`

Example (optional):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agent_packs.ps1
```

## Keep Setup Simple (Recommended)

If you are testing the default Atlas-only UX, remove `plugins/` to avoid duplicate sources:

```powershell
Remove-Item -Recurse -Force "plugins"
```

Then reload VS Code.

## Automatic Flow Source Selection (NEW)

Atlas now includes **intelligent flow source selection**. When you ask Atlas for a task, it automatically:

1. **Discovers all available flow sources** (`.github/agents` + `plugins/*/agents`)
2. **Analyzes the task type** (frontend, backend, devops, data, general)
3. **Selects the best workflow** based on:
   - Origin precedence (`github > plugin > other`)
   - Capability matching (task type + required skills)
   - Preferred source with fallback if unavailable
   - Deterministic tie-break for stable results

### Example Flow Selection

| Your Task | Selected Workflow | Why |
|-----------|-------------------|-----|
| "Create a React login form" | `frontend-workflow` | Has UI-Designer, Component-Builder, A11y-Auditor |
| "Add REST endpoint for users" | `backend-workflow` | Has API-Designer, Service-Builder, Security-Guard |
| "Deploy to Kubernetes" | `devops-workflow` | Has Container-Master, Pipeline-Engineer |
| "Train ML model" | `data-workflow` | Has ML-Scientist, Pipeline-Builder |
| "Fix this bug" | `.github/agents` | General-purpose, highest precedence |

### Demo: Test Source Selection

Two demos are included to verify the system works:

```powershell
# Smoke test (basic subagent delegation)
cd demos/subagents-smoke-demo
py -m unittest -v

# Source selection engine (multi-flow selection)
cd demos/atlas-source-selection-demo
py -m unittest -v
```

See [demos/atlas-source-selection-demo/DEMO_PROMPT.md](demos/atlas-source-selection-demo/DEMO_PROMPT.md) for a guided orchestration test.

## Troubleshooting

If you see more than one visible agent:

1. Check all subagents have `user-invocable: false`.
2. Check `Atlas` has `user-invocable: true`.
3. Remove duplicate plugin sources (`plugins/`) if you are not using plugin mode.
4. Reload VS Code.

If `Atlas` does not delegate:

1. Verify `Atlas` frontmatter includes `tools: [agent, ...]`.
2. Verify `Atlas` includes `agents: ["*"]`.
3. Confirm subagent files exist under `.github/agents`.

If flow selection seems wrong:

1. Check that domain workflows are enabled in `.vscode/settings.json`.
2. Verify the task description is clear about domain (e.g., "React component" vs "API endpoint").
3. Run the source selection demo to confirm the engine works: `py -m unittest -v demos/atlas-source-selection-demo/test_selection_engine.py`
