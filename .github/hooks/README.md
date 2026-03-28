# Zeus Hook Attendance Contract

This directory is the workspace-owned hook surface for **Zeus runtime attendance**.

## Purpose

The goal is not to create another monitoring agent. The goal is to let **Zeus** control a deterministic, auditable attendance sheet of every invoked subagent.

In practice, the first question this hook surface should answer is:

> Which subagents were actually invoked during this run, and in what order?

## Scope

This hook surface is for:

- global runtime attendance,
- observed subagent invocation order,
- hook-owned evidence artifacts,
- compact summaries that Zeus can report without dumping raw logs.

This hook surface is **not** for:

- replacing the runtime contracts inside `.github/agents/`,
- creating a hidden monitoring subagent,
- encoding business logic that belongs in prompts,
- long-running or opaque automation.

## Hook Strategy

Zeus attendance should prefer workspace hooks based on these lifecycle events:

- `SubagentStart`
- `SubagentStop`

Why:

- these events are global to the runtime,
- they are a better fit for a full attendance sheet than prompt-local hooks,
- they can observe **all** invoked subagents, not only Specify leaves.

## Evidence Model

Recommended artifacts:

- raw ledger: `.specify/traces/<trace-id>.jsonl`
- rendered summary: `.specify/traces/<trace-id>.md`

Minimum event fields:

- `trace_id`
- `timestamp`
- `event`
- `parent_agent`
- `child_agent`
- `layer_from`
- `layer_to`
- `status`
- `feature_id` when available
- `phase` when available

## Two Levels of Proof

### 1. Global attendance proof

Owned by workspace hooks in `.github/hooks/`.

This answers:

- which subagents were invoked,
- in which order,
- and whether the runtime path actually happened.

### 2. Stage-level proof

Owned by prompt-local stage hooks such as `.specify/extensions.yml`.

This answers:

- what happened inside the Specify pipeline,
- and provides finer-grained proof for stages like `SpecifyPlan`, `SpecifyTasks`, or `SpecifyImplement`.

## Zeus Summary Contract

Zeus should summarize attendance evidence compactly, for example:

- `TRACE_ID`
- `ATTENDANCE_COUNT`
- `OBSERVED_EDGES`
- `REPORT_PATH`

Zeus should **not** dump raw JSONL unless explicitly requested.

## Control Rules

1. Keep hooks small, deterministic, and auditable.
2. Prefer repo-owned scripts over ad-hoc shell one-liners.
3. Do not hardcode secrets.
4. Do not use hooks to silently mutate unrelated files.
5. Treat workspace hooks as the canonical attendance source; treat prompt-local hooks as deeper supplemental proof.

## Current Migration Rule

During the Zeus migration:

- the visible root conductor is `Zeus`,
- optional `Backend-Atlas`, `DevOps-Atlas`, `Data-Atlas`, `Automation-Atlas`, and `UX-Atlas` remain unchanged,
- the attendance system must be designed for **all invoked subagents**, even if the first proof slice is validated through the core Specify path.

## Memory Context Hook

A second hook surface exists at `.github/hooks/zeus-memory-context.json`. It fires `sync_memory_context.py` on every `SubagentStart` event to refresh `.specify/memory/zeus-context.md`.

These two hooks are intentionally separate:

| Hook file | Purpose | Output |
|---|---|---|
| `zeus-subagent-attendance.json` | Global subagent attendance ledger | `.specify/traces/<trace-id>.jsonl` + `.md` |
| `zeus-memory-context.json` | Compact session context for Zeus | `.specify/memory/zeus-context.md` |

The memory-context hook MUST NOT be used for attendance recording. Attendance stays in the trace ledger.