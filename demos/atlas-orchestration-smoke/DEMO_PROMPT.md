# Demo Prompt for Atlas

Copy and paste this into VS Code Copilot Chat:

---

**@Atlas** Fix the priority validation bug in `demos/atlas-orchestration-smoke/`.

## Problem

The `TaskRepository._validate_priority()` method in `task_api.py` has a bug:
- Invalid priority values (0, -1, 5, 100, etc.) should raise `ValidationError`
- Currently, invalid values silently default to `Priority.MEDIUM`

## Evidence

Running tests shows 4 failures:
```
test_priority_zero_raises ... FAIL
test_priority_negative_raises ... FAIL
test_priority_five_raises ... FAIL
test_priority_hundred_raises ... FAIL
```

## Constraints

- Only modify files in `demos/atlas-orchestration-smoke/`
- Keep changes minimal (only fix the bug, no refactoring)
- Must pass all 21 tests after fix
- Verification command: `py -m unittest -v`

## Required Process

1. **Hermes**: Find `_validate_priority` method and understand current implementation
2. **Oracle**: Analyze the bug and confirm the fix approach
3. **Sisyphus**: Implement the fix (add range validation, raise ValidationError for invalid values)
4. **Themis**: Verify the fix is correct and minimal
5. **Argus**: Run all tests and confirm 20/20 pass

## Expected Fix

The `_validate_priority` method should:
1. Check if priority is within valid range (1-4)
2. Raise `ValidationError` with message including "priority" if invalid
3. Only then convert to `Priority` enum

## Definition of Done

- All 21 tests pass
- Only `task_api.py` was modified
- Change is in `_validate_priority` method only

---

## Alternative Short Prompt

If you want a simpler test:

```
@Atlas Fix the failing tests in demos/atlas-orchestration-smoke using your subagents.
```
