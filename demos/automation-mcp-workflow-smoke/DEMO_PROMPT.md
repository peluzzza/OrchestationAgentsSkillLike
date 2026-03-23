# Demo Prompt — Automation MCP Workflow Pack

Copy/paste this into Copilot Chat:

---

**@Atlas** Add a `dry_run` flag to `demos/automation-mcp-workflow-smoke/workflow_bundle.py`.

## Context

This is a sandbox demo for the `automation-mcp-workflow` optional plugin pack located at
`plugins/automation-mcp-workflow`. The canonical agents live in `.github/agents`; the
plugin pack adds `Automation-Atlas`, `Automation-Planner`, `Workflow-Composer`, and
`Automation-Reviewer` as opt-in conductors for automation-specific orchestration.

## Feature to add

- Add `dry_run: bool = False` as a constructor parameter to `WorkflowBundle`.
- When `dry_run=True`, `add_step()` still records steps normally, but `is_safe()` always
  returns `True` regardless of step reversibility.
- Add two new tests:
  - `test_dry_run_bundle_always_safe_with_irreversible_step`
  - `test_dry_run_false_respects_reversibility`

## Constraints

- Only change files under `demos/automation-mcp-workflow-smoke/`.
- Keep the diff minimal (no refactors).
- Verification command:
  `python3 -m unittest -v demos/automation-mcp-workflow-smoke/test_workflow_bundle.py`

## Suggested process

1. **Hermes** (from `.github/agents`): locate the best insertion point in `workflow_bundle.py`.
2. **Sisyphus** (from `.github/agents`): implement the feature, tests-first.
3. **Themis** (from `.github/agents`): review for minimalism and correctness.
4. *(Optional)* **Automation-Reviewer** (from `plugins/automation-mcp-workflow`): run a
   safety gate pass and confirm reversibility semantics are preserved.

## Definition of done

- All tests pass including the two new tests.
- Only `workflow_bundle.py` and `test_workflow_bundle.py` were modified.
