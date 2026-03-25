## Atlas static trace test case

**Type:** Desk-check / dry trace / no execution
**Date:** 2026-03-25
**Scope:** `Atlas` stable runtime in `review_clones/OrchestationAgentsSkillLike`
**Goal:** Validate by code inspection that the normal orchestration path is well defined, identify where the flow branches, and flag any static inconsistencies before a live run.

### Representative input

> "Plan and implement a medium-size backend feature with tests, using the normal Atlas path and no manual approval checkpoints unless blocked."

### Preconditions

- `.github/agents` is the active runtime surface.
- No `disabled_agents.txt` file is present under `plans/`.
- No prompt-level `enabled_agents` or `disabled_agents` block is supplied.
- The task is large enough that Atlas should choose delegated planning, not an ultra-local direct plan.

### Expected top-level flow

1. **User → Atlas**
2. **Atlas → Prometheus** for planning
3. **Prometheus → Hermes/Oracle** for context mapping when needed
4. **Prometheus → SpecifySpec → SpecifyPlan → SpecifyAnalyze**
5. **Prometheus → Atlas** with `feature_id`, `plan_path`, `analysis_report`, and planning notes
6. **Atlas → Sisyphus-subagent** for a concrete implementation phase
7. **Sisyphus-subagent → SpecifyTasks / SpecifyAnalyze / SpecifyImplement**
8. **Sisyphus-subagent → Atlas** with phase completion status
9. **Atlas → Themis Subagent** for review
10. **Atlas → Argus - QA Testing Subagent** for QA
11. **Atlas → HEPHAESTUS** only if infra/deploy conditions apply
12. **Atlas** writes completion artifacts and returns control to the user

---

## Step-by-step dry trace

### Step 0 — Atlas accepts the request

**Source:** `.github/agents/Atlas.agent.md`

Atlas requires these user-side request fields conceptually:
- `goal`
- `constraints`
- `success_criteria`

**Static verdict:** PASS

The conductor contract is explicit and the runtime envelope is well declared. Atlas is clearly Layer 0 and returns a traceable state block.

### Step 1 — Atlas checks controls and plan directory

**Expected behavior:**
- Honor prompt-level `enabled_agents` / `disabled_agents` if present.
- Check for `plans/disabled_agents.txt`.
- If no `AGENTS.md` exists, default to `plans/`.

**Observed in this repo:**
- No `AGENTS.md` at repo root.
- No `plans/disabled_agents.txt` present.

**Static verdict:** PASS

No configuration ambiguity here; Atlas should default cleanly to `plans/`.

### Step 2 — Atlas chooses the planning path

**Expected behavior:**
- For implementation work, Atlas prefers `Prometheus` when available.
- It should only plan directly for tiny or non-code tasks.

**Observed in code:**
- `Atlas.agent.md` explicitly routes implementation/code work through `Prometheus` when available.

**Static verdict:** PASS

The handoff is clearly encoded and matches the intended stable runtime.

### Step 3 — Prometheus enters SP-0 research

**Expected behavior:**
- Use `Hermes-subagent` and/or `Oracle-subagent` to map context.
- Keep research within planning scope.

**Observed in code:**
- `Prometheus.agent.md` frontmatter exposes `Hermes-subagent`, `Oracle-subagent`, `SpecifySpec`, `SpecifyPlan`, and `SpecifyAnalyze`.
- It explicitly forbids implementation delegation.

**Static verdict:** PASS

The planner stays in its lane. Good boundary discipline.

### Step 4 — Prometheus and the Specify pipeline

**Documented expected flow (README):**
- SP-1 `SpecifyConstitution`
- SP-2 `SpecifySpec`
- SP-3 `SpecifyClarify`
- SP-4 `SpecifyPlan`
- SP-5 `SpecifyAnalyze`

**Actually encoded in `Prometheus.agent.md`:**
- `SpecifyConstitution` is treated as **not part of the runtime** for Prometheus; it uses `.specify/memory/constitution.md` directly.
- `SpecifyClarify` is also treated as **not part of the runtime**; Prometheus applies conservative defaults directly into `spec.md` instead of invoking the agent.
- The active delegated path is effectively:
  - `SpecifySpec`
  - `SpecifyPlan`
  - `SpecifyAnalyze`

**Static verdict:** WARN

This is the biggest semantic drift found in the desk-check.

**Why it matters:**
- The repo ships `SpecifyConstitution.agent.md` and `SpecifyClarify.agent.md`.
- README describes them as active Prometheus-invoked stages.
- But the real planner currently uses a degraded/manual fallback for both stages.

**Risk level:** Medium

It does not necessarily break the pipeline, but it can confuse contributors and make trace expectations diverge from real runtime behavior.

### Step 5 — Atlas receives planning output

**Expected behavior:**
- Atlas should receive `feature_id`, `feature_dir`, `spec_path`, `plan_path`, `analysis_report`, `specify_pipeline_status`, `open_questions`, and `atlas_notes`.
- If SP-5 is blocked, Atlas should not proceed to implementation.

**Observed in code:**
- `Prometheus` contract defines those return fields.
- `Atlas` explicitly says SP-5 must pass before delegating to Sisyphus.

**Static verdict:** PASS

The planning gate is explicit and coherent.

### Step 6 — Atlas delegates a concrete implementation phase to Sisyphus-subagent

**Expected behavior:**
- Atlas sends `feature_id`, `phase`, `acceptance_criteria`, and `constraints`.
- Sisyphus stays phase-scoped only.

**Observed in code:**
- `Sisyphus-subagent.agent.md` is strict about scoped delivery and escalation.
- It does not own review, QA, or completion artifacts.

**Static verdict:** PASS

Good separation of concerns.

### Step 7 — Sisyphus executes the EX-side Specify pipeline

**Expected flow:**
- EX-0: verify `spec.md`, `plan.md`, `tasks.md`, `analysis-report.md`
- EX-1: run `SpecifyTasks` if `tasks.md` is missing
- EX-2: run `SpecifyAnalyze`
- EX-3: run `SpecifyImplement`
- EX-4: post-phase verification

**Observed in code:**
- `Sisyphus-subagent` frontmatter includes exactly `SpecifyTasks`, `SpecifyAnalyze`, and `SpecifyImplement`.
- The control flow is explicit and deterministic.

**Static verdict:** PASS

This is one of the cleanest parts of the runtime.

### Step 8 — Atlas review and QA gates

**Expected flow:**
- `Themis Subagent` reviews correctness and quality
- `Argus - QA Testing Subagent` validates testing exhaustiveness

**Observed in code:**
- Themis and Argus have clear contracts and activation guards.
- Atlas is explicit that Argus should not be re-run against unchanged state after `NEEDS_MORE_TESTS`.

**Static verdict:** PASS

The loop is well defined, with a useful anti-ping-pong rule.

### Step 9 — Conditional deployment lane

**Expected flow:**
- Only call `HEPHAESTUS` when infra/deploy/release-readiness is relevant.

**Observed in code:**
- `HEPHAESTUS` is well bounded by mode and only activates for ops-facing work.

**Static verdict:** PASS

No static contradiction found here.

---

## Invariants that must hold in a real run

These are the things that should always remain true if the flow is healthy:

1. Atlas is the only user-visible conductor.
2. Prometheus must not implement code.
3. Sisyphus must not skip EX-2 consistency validation.
4. Themis must not implement fixes.
5. Argus must not become a code-review substitute.
6. HEPHAESTUS must remain conditional, not mandatory for every phase.
7. If SP-5 is blocked, Atlas must not move forward.
8. If EX-2 is blocked, Sisyphus must escalate instead of guessing.

---

## Static weak spots discovered

### Finding F1 — README/runtime drift around `SpecifyConstitution` and `SpecifyClarify`

**Observed:** README presents both as active Prometheus stages, while `Prometheus.agent.md` explicitly bypasses both.

**Impact:** Medium

**Consequence in practice:** A maintainer reading README expects a richer interactive planning flow than the planner actually executes.

### Finding F2 — Shipped agents that are currently dormant in the real planning path

**Observed:** `SpecifyConstitution` and `SpecifyClarify` are now internally cleaner and constitution-aligned, but Prometheus still treats them as out-of-runtime for the normal path.

**Impact:** Medium

**Consequence in practice:** Hardening those agents was still useful, but right now they are not first-class active stages in the main desk-checked path.

### Finding F3 — Live behavior depends heavily on artifact health

**Observed:** The happy path assumes `.specify/specs/<feature>/` artifacts stay synchronized; if not, both Prometheus and Sisyphus escalate quickly.

**Impact:** Low-to-Medium

**Consequence in practice:** The runtime is robust by design, but sensitive to plan/spec/task drift.

---

## Desk-check verdict

**Overall verdict:** PASS WITH WARNINGS

The orchestration flow is structurally well defined and does not look broken in the main happy path. The main issue is not a hard runtime rupture, but a **semantic mismatch between documentation and the planner's actual delegated path**.

If you asked me like a programmer doing a code walkthrough: **the flow does not look like it will collapse immediately**, but it does contain one misleading branch definition that should eventually be reconciled.

---

## Recommended follow-up

Choose one of these two directions:

1. **Make runtime match docs**
   - Re-enable true Prometheus invocation of `SpecifyConstitution` and `SpecifyClarify`.

2. **Make docs match runtime**
   - Update README and any related docs to explain that Prometheus currently uses a direct/degraded path for constitution and clarification stages.

**My recommendation:** Option 2 first, unless you specifically want the richer interactive SP-1/SP-3 behavior back in the live runtime.
