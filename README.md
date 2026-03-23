# Atlas Agents For VS Code

A multi-agent team for VS Code Copilot Chat. You talk to `@Atlas`; it orchestrates a hidden team of 25 specialists covering planning, implementation, security, testing, documentation, and ops.

## Install (60 seconds)

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

## Global Install (available in any workspace)

To use Atlas in any project on your machine, without cloning this repo:

```powershell
.\scripts\install-agents-user-level.ps1 -Force
```

Then `Ctrl+Shift+P` → `Developer: Reload Window`. That's it.

## The Agent Team

All 26 agents live in `.github/agents/`. You only need to know about `@Atlas`.

| Role | Agent | Invoked by |
|---|---|---|
| Conductor | `Atlas` | **You** |
| Planner / Specify pipeline | `Prometheus` | Atlas |
| Code exploration | `Hermes` | Atlas, Prometheus |
| Deep research | `Oracle` | Atlas, Prometheus |
| Implementation | `Sisyphus` | Atlas |
| Frontend / UI | `Afrodita-UX` | Atlas |
| Code review | `Themis` | Atlas |
| Security review | `Atenea` | Atlas |
| Testing / QA | `Argus` | Atlas |
| Documentation | `Clio` | Atlas |
| Dependencies | `Ariadna` | Atlas |
| Ops / Deploy / Incidents | `Hephaestus` | Atlas |
| Specify: Constitution | `SpecifyConstitution` | Prometheus |
| Specify: Spec | `SpecifySpec` | Prometheus |
| Specify: Clarify | `SpecifyClarify` | Prometheus |
| Specify: Plan | `SpecifyPlan` | Prometheus |
| Specify: Tasks | `SpecifyTasks` | Prometheus |
| Specify: Consistency | `SpecifyAnalyze` | Prometheus, Sisyphus |
| Specify: Implement | `SpecifyImplement` | Sisyphus |

## How Atlas Works

```
You → @Atlas
         ├── Prometheus (planning + Specify pipeline: SP-5 gate)
         │       ├── Hermes (explore)
         │       ├── Oracle (research)
         │       └── SpecifyAnalyze (SP-5 consistency gate)
         ├── Sisyphus (implement, phase by phase)
         │       └── SpecifyAnalyze (EX-1 gate pre-implementation)
         ├── Themis (review)
         ├── Atenea (security — auto on any auth/secrets/permissions change)
         ├── Argus (testing)
         ├── Hephaestus (ops: deploy / release-readiness / incident / maintenance / performance)
         ├── Clio (docs)
         └── Ariadna (dependencies)
```

Atlas reads `.github/plugin/pack-registry.json` at startup to know which optional packs are shipped but inactive. If your task domain clearly matches one (e.g. Spring Boot → `backend-workflow`), Atlas will recommend activating it.

## Enable Optional Conductors

Optional domain conductors are shipped in `plugins/` but inactive by default. Add to `.vscode/settings.json` to activate:

```json
{
  "chat.agentFilesLocations": {
    ".github/agents": true,
    "plugins/frontend-workflow/agents": true,
    "plugins/backend-workflow/agents": true,
    "plugins/devops-workflow/agents": true,
    "plugins/data-workflow/agents": true,
    "plugins/automation-mcp-workflow/agents": true,
    "plugins/ux-enhancement-workflow/agents": true
  }
}
```

| Conductor | Domain |
|---|---|
| `@Afrodita` | UI/UX implementation (React, Vue, Angular) |
| `@Backend-Atlas` | API & database (Spring, Express, FastAPI) |
| `@DevOps-Atlas` | Infrastructure & CI/CD |
| `@Data-Atlas` | Data engineering & ML |
| `@Automation-Atlas` | MCP integrations & workflow automation |
| `@UX-Atlas` | UX research, flow critique, spec handoff |

## Spec-Driven Development (Specify pipeline)

For any implementation task, Atlas routes through Prometheus which runs the full Specify pipeline before writing code:

```
Constitution → Spec → Clarify → Plan → SP-5 gate → Tasks → EX-1 gate → Implement
```

Artifacts land in `.specify/specs/<feature-slug>/`. The SP-5 gate (pre-tasks) and EX-1 gate (pre-implementation) are consistency checkpoints that Atlas enforces before allowing Sisyphus to write code.

## Repository Layout

```
.github/agents/          ← 26 agent files (the only thing VS Code reads)
.github/plugin/
  pack-registry.json     ← activation map: which packs are shipped vs active
plugins/                 ← optional domain packs (inactive unless enabled above)
spec-kit/                ← Specify pipeline reference docs
demos/                   ← smoke tests per capability lane
scripts/                 ← sync and validation utilities
plans/                   ← Atlas orchestration artifacts
```

## Validation

```shell
py -m unittest -v scripts/test_validate_pack_registry.py
py -m unittest -v scripts/test_validate_atlas_pack_parity.py
py -m unittest -v demos/specify-rbac-springboot-demo/test_rbac_harness.py
```

### Cross-Workflow Handoffs

Workflows can hand off to each other:
- `Afrodita` → `Backend-Atlas`, `DevOps-Atlas`
- `Backend-Atlas` → `Afrodita`, `DevOps-Atlas`, `Data-Atlas`
- `DevOps-Atlas` → `Afrodita`, `Backend-Atlas`, `Data-Atlas`
- `Data-Atlas` → `Backend-Atlas`, `DevOps-Atlas`

See [plugins/README.md](plugins/README.md) only if you intentionally want distribution-pack mode.

## Specify Pipeline — Spec-Driven Development (NEW)

`Prometheus` now orchestrates a full **Spec-Driven Development** pipeline, based on [github/spec-kit](https://github.com/github/spec-kit), before producing any implementation plan. This ensures the *what* is fully defined and validated before the *how* is decided.

### Specify Agents (hidden, orchestrated by Prometheus / Sisyphus)

| Agent | Role | Based on |
|---|---|---|
| `SpecifyConstitution` | Establish & version project principles | `spec-kit/constitution` |
| `SpecifySpec` | Generate feature spec with user stories & acceptance criteria | `spec-kit/specify` |
| `SpecifyClarify` | Resolve ambiguities via taxonomy-driven Q&A | `spec-kit/clarify` |
| `SpecifyPlan` | Produce technical plan, data model, contracts & research | `spec-kit/plan` |
| `SpecifyTasks` | Break plan into atomic ordered tasks (T001..Tnnn) | `spec-kit/tasks` |
| `SpecifyAnalyze` | Cross-artifact consistency analysis (read-only) | `spec-kit/analyze` |
| `SpecifyImplement` | Execute tasks phase-by-phase, mark `[x]`, enforce checklist gate | `spec-kit/implement` |

### Pipeline Flow

```
Atlas
 └─ Prometheus (planning)
      ├─ SP-0  Hermes + Oracle          → context mapping
      ├─ SP-1  SpecifyConstitution        → .specify/memory/constitution.md
      ├─ SP-2  SpecifySpec                → .specify/specs/<feature>/spec.md
      ├─ SP-3  SpecifyClarify (if needed) → spec.md updated
      ├─ SP-4  SpecifyPlan                → plan.md, data-model.md, contracts/, research.md
      └─ SP-5  SpecifyAnalyze             → analysis-report.md → plan delivered to Atlas

Atlas
 └─ Sisyphus (implementation)
      ├─ EX-0  SpecifyTasks               → tasks.md (T001..Tnnn)
      ├─ EX-1  SpecifyAnalyze             → consistency gate
      └─ EX-2  SpecifyImplement           → code, tests, [x] progress marks
```

### Artifacts Generated per Feature

```
.specify/
  memory/
    constitution.md          ← project principles (versioned)
  specs/<feature-slug>/
    spec.md                  ← user stories, acceptance criteria, FRs
    plan.md                  ← technical plan
    data-model.md            ← entities & relationships
    contracts/               ← API/CLI/interface contracts
    research.md              ← decisions & alternatives
    quickstart.md            ← dev environment setup
    tasks.md                 ← atomic task list with [x] progress
    checklists/              ← quality gates for SpecifyImplement
    analysis-report.md       ← consistency findings
```

### Enable Specify Agents

Specify agents are already included in `.github/agents/` — no extra plugin source is needed. They are hidden from the agent picker and invoked automatically by `Prometheus` (during planning) and `Sisyphus` (during implementation). Just use `@Atlas` as normal.

---

## Optional: Distribution / Marketplace Packs

Use this only if you want secondary distribution through marketplace/plugin packs. It is not required for normal use. Shared Atlas-pack improvements should land in `plugins/atlas-orchestration-team/agents` first and then be synced into `.github/agents`.

Not every directory under `plugins/` is necessarily published in `.github/plugin/marketplace.json` at the same time: some packs can exist as shipped-but-inactive local plugin-path examples, mirrors, or pre-marketplace workflows.

- Marketplace definition: `.github/plugin/marketplace.json`
- Plugin packs: `plugins/atlas-orchestration-team`, `plugins/agent-pack-catalog`
- Domain workflow packs: `plugins/frontend-workflow`, `plugins/backend-workflow`, `plugins/devops-workflow`, `plugins/data-workflow`, `plugins/automation-mcp-workflow`, `plugins/ux-enhancement-workflow`
- Sync helper script: `scripts/sync_agent_packs.ps1`
- Validation helper script: `scripts/validate_plugin_packs.py`

Example (optional):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agent_packs.ps1
```

## Keep Setup Agents-First (Recommended)

If you want the clean zero-setup runtime experience, keep `.github/agents` active and avoid enabling duplicate plugin paths for the same shared agents. No repository deletion is required; just leave the plugin paths disabled in VS Code unless you intentionally want distribution-pack mode.

For contributors: do **not** hand-edit both copies of the shared Atlas pack. Edit `plugins/atlas-orchestration-team/agents/` first, then sync the shared files into `.github/agents/` so the root runtime surface stays aligned.

## Optional: Flow Source Selection Demo

This repo includes demos and reference logic for **intelligent flow source selection** in multi-workflow setups. That logic is useful if you build a custom Atlas variant or explicitly enable optional distribution packs, but it is **not** the default root-only `.github/agents` behavior documented above.

In the demo/reference model, a conductor can:

1. **Discovers all available flow sources** (`.github/agents` + `plugins/*/agents`)
2. **Analyzes the task type** (frontend, backend, devops, data, general)
3. **Selects the best workflow** based on:
   - Origin precedence (`github > plugin > other`)
   - Capability matching (task type + required skills)
   - Preferred source with fallback if unavailable
   - Deterministic tie-break for stable results

### Example Flow Selection Policy

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

If the flow-selection demo seems wrong:

1. Check that domain workflows are enabled in `.vscode/settings.json`.
2. Verify the task description is clear about domain (e.g., "React component" vs "API endpoint").
3. Run the source selection demo to confirm the engine works: `py -m unittest -v demos/atlas-source-selection-demo/test_selection_engine.py`
