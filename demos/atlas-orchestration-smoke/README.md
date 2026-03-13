# Atlas Orchestration Smoke Test

## Purpose

This demo validates that Atlas correctly delegates to specialized subagents in the expected order. It contains a **real bug** that requires the full orchestration pipeline to fix.

## The Bug

The `TaskRepository._validate_priority()` method has two issues:
1. It doesn't validate that priority is within range 1-4
2. It silently returns `MEDIUM` for invalid values instead of raising `ValidationError`

## Expected Test Results (Before Fix)

```
$ py -m unittest -v
...
test_priority_hundred_raises ... FAIL
test_priority_five_raises ... FAIL
test_priority_negative_raises ... FAIL
test_priority_zero_raises ... FAIL
...
Ran 21 tests in 0.XXXs
FAILED (failures=4)
```

## How to Run the Demo

### 1. Verify the Bug Exists

```powershell
cd demos/atlas-orchestration-smoke
py -m unittest -v
```

You should see **4 failing tests** related to priority validation.

### 2. Ask Atlas to Fix It

Open Copilot Chat and invoke Atlas:

```
@Atlas Fix the priority validation bug in demos/atlas-orchestration-smoke.
The tests show that invalid priorities (0, -1, 5, 100) should raise ValidationError
but currently don't. Use the full subagent pipeline.
```

Or use the detailed prompt in [DEMO_PROMPT.md](DEMO_PROMPT.md).

### 3. Verify the Fix

```powershell
py -m unittest -v
# Expected: 21 tests, 0 failures
```

## Expected Agent Flow

| Step | Agent | Task |
|------|-------|------|
| 1 | **Explorer** | Locate `task_api.py` and identify `_validate_priority` method |
| 2 | **Oracle** | Analyze the bug pattern and propose fix approach |
| 3 | **Sisyphus** | Implement the fix in `_validate_priority` |
| 4 | **Code-Review** | Validate the fix is correct and minimal |
| 5 | **Argus** | Run tests and confirm all 20 pass |

## Success Criteria

- [ ] Atlas invokes at least 3 different subagents
- [ ] Explorer identifies the correct file and method
- [ ] Sisyphus modifies only `_validate_priority` method
- [ ] All 21 tests pass after the fix
- [ ] No unnecessary files created or modified

## Files

| File | Description |
|------|-------------|
| `task_api.py` | Task API with validation bug |
| `test_task_api.py` | 21 tests (4 fail due to bug) |
| `DEMO_PROMPT.md` | Copy-paste prompt for Atlas |
| `EXPECTED_FLOW.md` | Detailed expected agent interactions |
