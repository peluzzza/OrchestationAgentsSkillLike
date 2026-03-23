# Automation MCP Workflow Smoke Demo

Tiny self-contained demo for the `automation-mcp-workflow` optional plugin pack.

## What this demo shows

A minimal `WorkflowBundle` module that models an ordered sequence of named steps
with basic safety validation. Use it as a sandbox to run an orchestration loop
involving the Automation pack agents while keeping changes confined to this folder.

## Requirements

| Layer | Path |
|-------|------|
| Canonical agents (required) | `.github/agents` |
| Optional plugin pack | `plugins/automation-mcp-workflow` |

The canonical agents under `.github/agents` provide Atlas and the core pipeline.
The plugin pack adds `Automation-Atlas`, `Automation-Planner`, `Workflow-Composer`,
and `Automation-Reviewer` as opt-in conductors.
Enable only the pack you need for this demo; do not enable unrelated packs.

## Run the tests

From this folder:

```shell
python3 -m unittest -v
```

From the repo root:

```shell
python3 -m unittest -v demos/automation-mcp-workflow-smoke/test_workflow_bundle.py
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
| `workflow_bundle.py` | Minimal workflow bundle abstraction |
| `test_workflow_bundle.py` | 15 passing tests |
| `DEMO_PROMPT.md` | Demo prompt to paste into Copilot Chat |
