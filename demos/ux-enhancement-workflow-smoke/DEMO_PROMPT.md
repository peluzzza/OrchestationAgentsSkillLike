# Demo Prompt — UX Enhancement Workflow Pack

Copy/paste this into Copilot Chat:

---

**@Atlas** Add a `checklist()` method to `demos/ux-enhancement-workflow-smoke/ux_handoff.py`.

## Context

This is a sandbox demo for the `ux-enhancement-workflow` optional plugin pack located at
`plugins/ux-enhancement-workflow`. The canonical agents live in `.github/agents`; the
plugin pack adds `UX-Atlas`, `UX-Planner`, `User-Flow-Designer`, `Design-Critic`,
`Accessibility-Heuristics`, and `Frontend-Handoff` as opt-in conductors for UX-specific
orchestration.

## Feature to add

- Add `checklist() -> list[str]` to `HandoffSpec`.
- It should return an ordered list of checklist items, one per registered flow, prefixed
  by `[ ]` when `is_ready()` is False and `[x]` when `is_ready()` is True.
  Example (not ready): `["[ ] User enters credentials", "[ ] Forgot-password link"]`
  Example (ready):     `["[x] User enters credentials", "[x] Forgot-password link"]`
- Add two new tests:
  - `test_checklist_not_ready_uses_unchecked_prefix`
  - `test_checklist_ready_uses_checked_prefix`

## Constraints

- Only change files under `demos/ux-enhancement-workflow-smoke/`.
- Keep the diff minimal (no refactors).
- Verification command:
  `python3 -m unittest -v demos/ux-enhancement-workflow-smoke/test_ux_handoff.py`

## Suggested process

1. **Hermes** (from `.github/agents`): locate the best insertion point in `ux_handoff.py`.
2. **Sisyphus** (from `.github/agents`): implement the feature, tests-first.
3. **Themis** (from `.github/agents`): review for minimalism and correctness.
4. *(Optional)* **Frontend-Handoff** (from `plugins/ux-enhancement-workflow`): validate
   that the checklist format matches implementation team expectations.

## Definition of done

- All tests pass including the two new tests.
- Only `ux_handoff.py` and `test_ux_handoff.py` were modified.
