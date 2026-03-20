# Expected Agent Flow

This document describes the expected behavior when Atlas processes this demo.

## Phase 0: Atlas Initialization

**Atlas** should:
1. Parse the user request
2. Identify available agents via Agent Buscador
3. Output initial status with goal, constraints, and success criteria

Example output:
```
**Goal:** Fix priority validation bug in demos/atlas-orchestration-smoke.
**Constraints:** Modify only demo folder, minimal changes, must pass all tests.
**Success:** All 20 tests pass after fix.

Status: planning
Delegations: Building agent index...
```

## Phase 1: Exploration

**Atlas delegates to: Hermes**

Prompt to Hermes:
> Find files related to priority validation in demos/atlas-orchestration-smoke.
> Identify the _validate_priority method and report its location and current implementation.

**Hermes returns:**
- File: `demos/atlas-orchestration-smoke/task_api.py`
- Method: `_validate_priority` at lines ~108-118
- Bug identified: Missing range check, silent fallback to MEDIUM

## Phase 2: Analysis

**Atlas delegates to: Oracle**

Prompt to Oracle:
> Analyze the priority validation bug in _validate_priority.
> The method should reject values outside 1-4 but currently defaults to MEDIUM.
> Provide fix approach and risks.

**Oracle returns:**
- Root cause: No range validation before enum conversion
- Fix: Add explicit range check before `Priority(priority)`
- Risk: Low - isolated change to single method
- Acceptance criteria: Tests for 0, -1, 5, 100 should pass

## Phase 3: Implementation

**Atlas delegates to: Sisyphus**

Prompt to Sisyphus:
> Fix _validate_priority in task_api.py
> - Add range check: if priority < 1 or priority > 4, raise ValidationError
> - Remove silent fallback to MEDIUM
> - Keep change minimal

**Sisyphus returns:**
- Modified: `task_api.py` lines 108-118
- Change: Added range validation, removed silent fallback
- Diff summary: ~5 lines changed

Expected fix:
```python
def _validate_priority(self, priority: int) -> Priority:
    """Validate and convert priority integer to enum."""
    if not isinstance(priority, int) or priority < 1 or priority > 4:
        raise ValidationError(
            f"Invalid priority {priority}. Must be 1 (LOW), 2 (MEDIUM), 3 (HIGH), or 4 (CRITICAL)."
        )
    return Priority(priority)
```

## Phase 4: Review

**Atlas delegates to: Themis**

Prompt to Themis:
> Review the changes to _validate_priority in task_api.py.
> Verify: correct validation logic, proper error message, minimal diff.

**Themis returns:**
- Status: APPROVED
- Findings:
  - ✅ Range check is correct (1-4)
  - ✅ Error message is descriptive
  - ✅ Change is minimal and focused
  - ✅ No unnecessary modifications

## Phase 5: Verification

**Atlas delegates to: Argus**

Prompt to Argus:
> Run tests in demos/atlas-orchestration-smoke.
> Command: py -m unittest -v
> Expected: 21 tests pass

**Argus returns:**
- Command executed: `py -m unittest -v`
- Result: 21 tests, 0 failures
- Status: PASS

## Phase 6: Completion

**Atlas final report:**
```
Status: complete

Delegations:
- Hermes: Located bug in task_api.py:_validate_priority
- Oracle: Confirmed fix approach (range validation)
- Sisyphus: Implemented fix (+5 lines)
- Themis: APPROVED
- Argus: 21/21 tests pass

Decision: Bug fixed successfully.
Next: None - task complete.

Files modified:
- demos/atlas-orchestration-smoke/task_api.py (1 method)
```

## Validation Checklist

After running the demo, verify:

- [ ] Atlas displayed agent index at start
- [ ] Hermes was invoked for file discovery
- [ ] Oracle analyzed the bug (optional but recommended)
- [ ] Sisyphus made the code change
- [ ] Themis validated the change
- [ ] Argus ran tests and reported results
- [ ] Final status showed "complete"
- [ ] Only task_api.py was modified
- [ ] All 21 tests pass
