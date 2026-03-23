# UX Enhancement Workflow Smoke Demo

Tiny self-contained demo for the `ux-enhancement-workflow` optional plugin pack.

## What this demo shows

A minimal `HandoffSpec` module that models the spec package assembled by the
Frontend-Handoff agent before implementation handoff. Use it as a sandbox to
run an orchestration loop involving the UX Enhancement pack agents while keeping
changes confined to this folder.

## Requirements

| Layer | Path |
|-------|------|
| Canonical agents (required) | `.github/agents` |
| Optional plugin pack | `plugins/ux-enhancement-workflow` |

The canonical agents under `.github/agents` provide Atlas and the core pipeline.
The plugin pack adds `UX-Atlas`, `UX-Planner`, `User-Flow-Designer`,
`Design-Critic`, `Accessibility-Heuristics`, and `Frontend-Handoff` as opt-in
conductors for UX-specific orchestration.
Enable only the pack you need for this demo; do not enable unrelated packs.

## Run the tests

From this folder:

```shell
python3 -m unittest -v
```

From the repo root:

```shell
python3 -m unittest -v demos/ux-enhancement-workflow-smoke/test_ux_handoff.py
```

## Orchestrate a feature with subagents

Open Copilot Chat and use the prompt in `DEMO_PROMPT.md`.

## Memory contract

This demo is stateless. It reads shared memory from
`.specify/memory/session-memory.md` and `.specify/memory/decision-log.md`
as defined by the pack contract. It does not create a duplicate memory store.

## Files

| File | Description |
|------|-------------|
| `ux_handoff.py` | Minimal UX handoff spec abstraction |
| `test_ux_handoff.py` | 17 passing tests |
| `DEMO_PROMPT.md` | Demo prompt to paste into Copilot Chat |
