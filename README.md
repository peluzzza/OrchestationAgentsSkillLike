# Atlas Agents For VS Code

A multi-agent runtime for VS Code Copilot Chat. In this clone, you talk to `@Atlas`; it orchestrates a stable hidden working surface for planning, implementation, review, QA, and ops from `.github/agents`.

> **Important for this repo:** the active agents you should edit live in `.github/agents`. Do not treat `plugins/` as the working runtime surface unless you are explicitly operating in plugin/distribution mode.

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

This repository ships many agent definitions in `.github/agents`, but the **stable zero-setup orchestration path** is intentionally narrower than the full file count. You only need to know about `@Atlas`.

Under `stable-runtime-v1`, the root runtime is split into a **mandatory stable core** and a few **optional validated utility lanes**. The validator requires the stable core to be complete; `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS` are validated when present, but they are not part of the stable-core completeness requirement.

### Stable core (mandatory)

| Role | Agent | Invoked by |
|---|---|---|
| Conductor | `Atlas` | **You** |
| Planner / Specify pipeline | `Prometheus` | Atlas |
| Implementation | `Sisyphus-subagent` | Atlas |
| Frontend / UI | `Afrodita-subagent` | Atlas |
| Code review | `Themis Subagent` | Atlas |
| Testing / QA | `Argus - QA Testing Subagent` | Atlas |

### Optional validated utility lanes

| Role | Agent | Invoked by | Runtime note |
|---|---|---|---|
| Code exploration | `Hermes-subagent` | Atlas, Prometheus | Validated when present; inherits session context and requires trace propagation |
| Deep research | `Oracle-subagent` | Atlas, Prometheus | Validated when present; inherits session context and requires trace propagation |
| Ops / Deploy / Incidents | `HEPHAESTUS` | Atlas | Validated when present; inherits session context and requires trace propagation |

### Hidden Specify pipeline agents

| Role | Agent | Invoked by |
|---|---|---|
| Specify: Constitution | `SpecifyConstitution` | Shipped helper agent (not in Prometheus default delegated path) |
| Specify: Spec | `SpecifySpec` | Prometheus |
| Specify: Clarify | `SpecifyClarify` | Shipped helper agent (not in Prometheus default delegated path) |
| Specify: Plan | `SpecifyPlan` | Prometheus |
| Specify: Tasks | `SpecifyTasks` | Sisyphus |
| Specify: Consistency | `SpecifyAnalyze` | Prometheus, Sisyphus |
| Specify: Implement | `SpecifyImplement` | Sisyphus |

Additional governance lanes such as `Atenea`, `Ariadna`, `Clio`, and the canonical Layer-1 gods are still shipped as definitions in the repo, but they are **optional runtime lanes**, not hard requirements for the default orchestration path.

## Duplicate-Looking Files: What Is Intentional

Some files may look duplicated at first glance, but they serve different purposes.

### 1. Canonical agent + compatibility alias

These are intentional pairs. The canonical agent keeps the richer domain definition; the alias provides the stable runtime handle used by the default Atlas surface.

| Canonical agent | Compatibility alias | Why both exist |
|---|---|---|
| `Hermes.agent.md` | `Hermes-subagent.agent.md` | Canonical discovery lane + stable Atlas alias |
| `Oracle.agent.md` | `Oracle-subagent.agent.md` | Canonical research lane + stable Atlas alias |
| `Sisyphus.agent.md` | `Sisyphus-subagent.agent.md` | Canonical implementation lane + stable Atlas alias |
| `Themis.agent.md` | `Themis-subagent.agent.md` | Canonical review lane + stable Atlas alias |
| `Argus.agent.md` | `Argus-subagent.agent.md` | Canonical QA lane + stable Atlas alias |
| `Hephaestus.agent.md` | `Hephaestus-subagent.agent.md` | Canonical ops lane + stable Atlas alias |

These are **not** exact duplicates. The alias files are marked with comments such as `type: alias` and `delegates-to: ...`.

### 2. The Afrodita cluster

Afrodita is the one that looks most duplicated but is actually a three-role stack:

| File | Role |
|---|---|
| `Afrodita-UX.agent.md` | Layer-1 canonical frontend/UX god |
| `Afrodita-subagent.agent.md` | Stable Atlas-facing alias for the default runtime |
| `Afrodita.agent.md` | Layer-2 optional workflow conductor for the frontend pack |

So:
- `Afrodita-UX` = canonical lane
- `Afrodita-subagent` = runtime compatibility alias
- `Afrodita` = optional nested conductor under the frontend workflow model

Optional nested conductors such as `Afrodita`, `Backend-Atlas`, `DevOps-Atlas`, `Data-Atlas`, `Automation-Atlas`, and `UX-Atlas` may still appear in `.github/agents` in this clone for hierarchy completeness and shipped-pack visibility. Unless their workflow is explicitly activated, treat them as **non-default lanes** that may operate in degraded/self-contained mode rather than as part of Atlas's stable root-runtime path.

### 3. Exact duplicate names?

In the current clone, there are **no exact duplicate frontmatter `name:` values** across `.github/agents`.

## How Atlas Works

```
You → @Atlas
         ├── Prometheus (planning + Specify pipeline: SP-5 gate)
         │       ├── Hermes-subagent (explore)
         │       ├── Oracle-subagent (research)
         │       └── SpecifyAnalyze (SP-5 consistency gate)
         ├── Sisyphus-subagent (implement, phase by phase)
         │       └── SpecifyAnalyze (EX-1 gate pre-implementation)
         ├── Themis Subagent (review)
         ├── Argus - QA Testing Subagent (testing)
         ├── HEPHAESTUS (ops: deploy / release-readiness / incident / maintenance / performance)
         └── Optional lanes when explicitly available: Atenea / Clio / Ariadna
```

Atlas reads `.github/plugin/pack-registry.json` as a shipped-pack activation map. In this clone, the authoritative runtime is `.github/agents`; shipped plugin packs are optional and inactive unless you explicitly enable them.

In practice, Atlas's stable default path always expects the stable core above. `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS` remain available utility lanes in this checkout, but their runtime contract is intentionally softer: they must match `stable-runtime-v1` **when present**, they inherit the caller session, and they require trace propagation across delegated work.

## Enable Optional Conductors

Ignore this section unless you explicitly want plugin/distribution mode. Normal work in this repo should stay in `.github/agents`.

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

For any implementation task, Atlas routes through Prometheus which runs the effective Specify planning path before writing code. In the current default runtime, `SpecifyConstitution` and `SpecifyClarify` are still shipped as hidden helper agents, but Prometheus treats the ratified constitution file as the authority and applies conservative clarification defaults inline instead of invoking those two agents directly:

```
Constitution file → Spec → inline clarification defaults (if needed) → Plan → SP-5 gate → Tasks → EX-1 gate → Implement
```

Artifacts land in `.specify/specs/<feature-slug>/`. The SP-5 gate (pre-tasks) and EX-1 gate (pre-implementation) are consistency checkpoints that Atlas enforces before allowing Sisyphus to write code.

## Repository Layout

```
.github/agents/          ← active runtime surface and working edit target
.github/plugin/
  pack-registry.json     ← activation map: which packs are shipped vs active
plugins/                 ← optional distribution metadata / inactive packs in this clone
  atlas-orchestration-team/         ← metadata shell in this clone (no shipped agents/ folder)
spec-kit/                ← Specify pipeline reference docs
demos/                   ← smoke tests per capability lane
scripts/                 ← sync, validation, and fix utilities
plans/                   ← Atlas orchestration artifacts
```

## Validation

```shell
python3 scripts/validate_layer_hierarchy.py
python -m pytest scripts/ -q
```

Use the validation scripts to verify runtime and pack consistency after edits. The root runtime surface in `.github/agents` is the source you should validate first in this clone.

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

In the default runtime path today, Prometheus actively delegates to `SpecifySpec`, `SpecifyPlan`, and `SpecifyAnalyze`. `SpecifyConstitution` and `SpecifyClarify` remain shipped and hardened, but the planner currently handles those concerns through direct file authority and conservative inline defaults.

### Pipeline Flow

```
Atlas
 └─ Prometheus (planning)
  ├─ SP-0  Hermes + Oracle               → context mapping
  ├─ SP-1  constitution file authority   → .specify/memory/constitution.md
  ├─ SP-2  SpecifySpec                   → .specify/specs/<feature>/spec.md
  ├─ SP-3  inline clarification defaults → spec.md updated when needed
  ├─ SP-4  SpecifyPlan                   → plan.md, data-model.md, contracts/, research.md
  └─ SP-5  SpecifyAnalyze                → analysis-report.md → plan delivered to Atlas

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

Use this only if you want secondary distribution through marketplace/plugin packs. It is not required for normal use. In this clone, the operational runtime lives in `.github/agents`; `plugins/` is not the normal working surface.

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

If you want the clean zero-setup runtime experience, keep `.github/agents` active and leave plugin paths disabled unless you intentionally want distribution-pack mode.

For contributors in this clone: edit the active runtime in `.github/agents`. Do not default to `plugins/` as the authoring location here.

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
2. Verify `Atlas` frontmatter lists its stable specialists in `agents:` (`Prometheus`, `Hermes-subagent`, `Oracle-subagent`, `Sisyphus-subagent`, `Afrodita-subagent`, `Themis Subagent`, `Argus - QA Testing Subagent`, `HEPHAESTUS`).
3. Confirm subagent files exist under `.github/agents`.

If the flow-selection demo seems wrong:

1. Check that domain workflows are enabled in `.vscode/settings.json`.
2. Verify the task description is clear about domain (e.g., "React component" vs "API endpoint").
3. Run the source selection demo to confirm the engine works: `py -m unittest -v demos/atlas-source-selection-demo/test_selection_engine.py`
