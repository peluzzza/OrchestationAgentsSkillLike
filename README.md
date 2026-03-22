# Atlas Agents For VS Code

This repo is set up so you can start from zero with a simple experience:

- In the default zero-setup mode, you see only `Atlas` in the agent picker.
- `Atlas` delegates internally to hidden specialist subagents when needed.
- For implementation or code-changing work, `Atlas` routes planning through hidden `Prometheus` so the Specify pipeline runs before execution.
- `.github/agents/` is the canonical source of truth for the agent system.
- `plugins/` is optional secondary distribution/organization for future agent packs and domain-specific conductors.
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

- Default mode visible agent: `Atlas` only.
- Hidden agents: `Prometheus`, `Oracle`, `Hermes`, `Sisyphus`, `Argus`, `Themis`, `Hephaestus`, `Afrodita-UX`, `Atenea`, `Clio`, `Ariadna`, and the Specify specialists (`SpecifyConstitution`, `SpecifySpec`, `SpecifyClarify`, `SpecifyPlan`, `SpecifyTasks`, `SpecifyAnalyze`, `SpecifyImplement`).
- `Atlas` chooses and calls subagents internally.

If you explicitly enable optional distribution packs, additional approved conductors such as `Afrodita`, `Backend-Atlas`, `DevOps-Atlas`, and `Data-Atlas` can also appear in the agent picker.

## Orchestration Style (Merged)

This setup blends two ideas:

- Skill-style progressive activation: only activate specialist agents when needed.
- Conductor lifecycle: plan -> implement -> review -> verify, with explicit routing by agent specialty.

For implementation or code-changing tasks, Atlas routes planning through `Prometheus` so the Specify pipeline runs before execution. For docs-only, meta, or orchestration-only work, Atlas can take a lighter planning path when that is the simpler fit.

## Optional Distribution Packs

In addition to the canonical `.github/agents` pack, the repo also ships optional distribution packs for future expansion, alternative organization, or explicitly enabled domain conductors. They are not required for the normal Atlas-first workflow.

| Workflow | Conductor | Agents | Purpose |
|----------|-----------|--------|---------|
| General | `Atlas` | 19 | General development orchestration |
| Frontend | `Afrodita` | 8 | UI/UX development (React, Vue, Angular) |
| Backend | `Backend-Atlas` | 8 | API & database development (Spring, Express, FastAPI) |
| DevOps | `DevOps-Atlas` | 8 | Infrastructure & CI/CD (Terraform, K8s, GitHub Actions) |
| Data | `Data-Atlas` | 8 | Data engineering & ML (dbt, Spark, ML pipelines) |

### Enable Optional Domain Conductors

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
- `@Afrodita` - UI/UX tasks
- `@Backend-Atlas` - API/Database tasks
- `@DevOps-Atlas` - Infrastructure/CI-CD tasks
- `@Data-Atlas` - Data pipelines/ML tasks

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

Use this only if you want secondary distribution through marketplace/plugin packs. It is not required for normal use, and future core improvements should land in `.github/agents` first.

- Marketplace definition: `.github/plugin/marketplace.json`
- Plugin packs: `plugins/atlas-orchestration-team`, `plugins/agent-pack-catalog`
- Domain workflow packs: `plugins/frontend-workflow`, `plugins/backend-workflow`, `plugins/devops-workflow`, `plugins/data-workflow`
- Sync helper script: `scripts/sync_agent_packs.ps1`

Example (optional):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agent_packs.ps1
```

## Keep Setup Agents-First (Recommended)

If you want the clean canonical experience, keep `.github/agents` active and ignore or remove `plugins/` to avoid duplicate sources:

```powershell
Remove-Item -Recurse -Force "plugins"
```

Then reload VS Code.

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
