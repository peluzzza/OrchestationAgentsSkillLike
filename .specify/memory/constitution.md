<!--
SYNC IMPACT REPORT
==================
Version change: N/A → 1.0.0 (initial ratification)
Modified principles: none (initial)
Added sections: Core Principles (I–VII), Workflow Boundaries, Governance
Removed sections: none (initial)
Templates requiring updates:
  ✅ .specify/templates/constitution-template.md — sourced this document's shape
  ✅ .specify/templates/plan-template.md — Constitution Check section aligns with principles below
  ✅ .specify/templates/spec-template.md — Acceptance criteria guidance aligns with Principle III
  ✅ .specify/templates/tasks-template.md — Task format (T001..Tnnn, [P] tags) aligns with Principle VI
Follow-up TODOs: none
-->

# Atlas Orchestration Team — Constitution

## Core Principles

### I. Conductor-First Visibility (NON-NEGOTIABLE)
In the default root-first install mode, only `Atlas` is exposed as a user-visible agent. All specialist subagents (`Prometheus`, `Oracle`, `Hermes`, `Sisyphus`, `Argus`, `Themis`, `Hephaestus`, `Afrodita-UX`, `Atenea`, `Clio`, `Ariadna`, and Specify agents) MUST remain hidden (`user-invocable: false`).
- Any new agent added to `.github/agents/` or `plugins/**/agents/` MUST default to `user-invocable: false` unless it is a domain conductor explicitly approved as a second entry point.
- Users interact through `Atlas` by default, or through an approved domain conductor only when that workflow pack has been explicitly enabled. Hidden agents MUST NOT surface directly in the agent picker.

### II. Spec-Driven Development (NON-NEGOTIABLE)
No implementation code MAY be written until the Specify pipeline has produced a validated spec, plan, and task list:
- SP-1 `SpecifyConstitution` → `.specify/memory/constitution.md` (this file)
- SP-2 `SpecifySpec` → `.specify/specs/<slug>/spec.md`
- SP-3 `SpecifyClarify` (if ambiguities exist) → `spec.md` updated
- SP-4 `SpecifyPlan` → `plan.md`, `data-model.md`, `contracts/`, `research.md`
- SP-5 `SpecifyAnalyze` → `analysis-report.md` (consistency gate — blocking)
- EX-0 `SpecifyTasks` → `tasks.md` (T001..Tnnn)
- EX-1 `SpecifyAnalyze` (implementation gate — blocking)
- EX-2 `SpecifyImplement` → code, tests, `[x]` progress marks

Skipping any step or bypassing a blocking gate MUST be explicitly justified in the plan's `Complexity Tracking` table and approved by the human.

### III. Progressive Delegation (MUST follow)
Context efficiency is non-negotiable. Atlas MUST delegate aggressively:
- Exploration / codebase mapping → `Hermes`
- Deep subsystem analysis / risk → `Oracle`
- Full planning pipeline → `Prometheus`
- Backend/script implementation → `Sisyphus`
- Frontend implementation → `Afrodita-UX`
- Code review gate → `Themis`
- Verification and test triage → `Argus`
- Build / release checks → `Hephaestus`

Atlas MUST NOT perform deep multi-file reading or non-trivial implementation directly when a specialist is available. Atlas MAY still handle trivial synthesis, plan/completion file writing, and small non-code tasks when orchestration overhead would exceed execution value. Atlas synthesizes subagent outputs; it does not duplicate their work.

### IV. Atomic Task Execution (MUST follow)
Every implementation unit is expressed as an atomic, independently verifiable task:
- Format: `[ID] [P?] [USn] Description — file path`
- IDs are sequential: T001, T002, … Tnnn
- `[P]` tag signals tasks that can run in parallel (no shared file mutations)
- Each phase MUST have a named checkpoint that defines what "done" means before proceeding
- `SpecifyImplement` MUST mark `[x]` on each task immediately upon completion

### V. Root-First Bootstrap (MUST follow)
The `.specify/` directory MUST exist at repo root before any feature spec work begins:
```
.specify/
  memory/
    constitution.md     ← this file (established at SP-1)
  templates/
    constitution-template.md
    spec-template.md
    plan-template.md
    tasks-template.md
  specs/                ← one subdirectory per feature slug
    .gitkeep
```
`SpecifyConstitution` MUST read from `.specify/templates/constitution-template.md` when initialising a new project. If the template is absent, it MUST error rather than hallucinate a structure.

### VI. Gate-Based Progression (NON-NEGOTIABLE)
Two hard gates exist in every pipeline run:

| Gate | Agent | Condition to pass |
|------|-------|-------------------|
| Spec consistency | `SpecifyAnalyze` (SP-5) | Zero blocking findings before plan is handed to Atlas |
| Implementation consistency | `SpecifyAnalyze` (EX-1) | Zero blocking findings before `SpecifyImplement` begins |

If a gate fails, `Prometheus` or `Sisyphus` MUST surface the blocking findings to the human and MUST NOT proceed until resolved or explicitly overridden with documented justification.

### VII. Human Sovereignty (ALWAYS)
The human operator has unconditional authority to:
- Interrupt any pipeline phase at any time
- Override any gate finding with documented rationale
- Redirect the task scope or approach mid-execution
- Veto agent selection or disable specific agents via prompt-level controls

Atlas MUST honour `enabled_agents` / `disabled_agents` prompt-level controls before every delegation. No agent invocation bypasses this check.

---

## Workflow Boundaries

| Agent | May write to | May NOT write to |
|-------|-------------|-----------------|
| `Prometheus` | `plans/`, `.specify/` | `src/`, `tests/`, production code |
| `SpecifyConstitution` | `.specify/memory/`, `.specify/templates/` | anywhere else |
| `SpecifySpec` | `.specify/specs/<slug>/spec.md` | other spec directories |
| `SpecifyPlan` | `.specify/specs/<slug>/plan.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md` | `tasks.md`, production code |
| `SpecifyTasks` | `.specify/specs/<slug>/tasks.md` | production code |
| `SpecifyAnalyze` | `.specify/specs/<slug>/analysis-report.md` | anywhere else |
| `SpecifyImplement` | production code, tests, `tasks.md` (`[x]` marks) | `.specify/memory/`, templates |
| `Sisyphus` | assigned feature files per task scope | out-of-scope files |
| `Argus` | test result summaries only | production code |

New agents and plugins MUST document their write boundaries before being merged.

---

## Governance

### Amendment Procedure
1. Any change to a principle MUST be proposed as a pull request with a `docs: amend constitution` commit message.
2. Version must be incremented following semantic rules:
   - **MAJOR** — principle removed or backward-incompatible redefinition
   - **MINOR** — new principle or section, or materially expanded guidance
   - **PATCH** — clarifications, wording, typo fixes
3. After any amendment, `SpecifyConstitution` MUST run a consistency propagation pass over all four templates and update the Sync Impact Report comment at the top of this file.
4. The human operator MUST provide final approval before the amended constitution is merged.

### Compliance Review
All pull requests that add or modify agent files, templates, or `.specify/` artifacts MUST include a self-check confirming:
- [ ] No new `user-invocable: true` agent added without approval
- [ ] No implementation produced before matching spec + plan + tasks exist
- [ ] Gate findings addressed or overridden with documented justification
- [ ] Version line in this file matches any amendment made

---

**Version**: 1.0.0 | **Ratified**: 2026-03-19 | **Last Amended**: 2026-03-19
