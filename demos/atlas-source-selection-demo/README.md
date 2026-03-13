# Atlas source selection demo

This demo is a small, self-contained example of deterministic source selection for Atlas flow orchestration.

## What it demonstrates

- Origin precedence: github > plugin > other.
- Capability and task-type matching.
- Preferred source selection with fallback when preferred source is unavailable.
- Deterministic tie-break behavior.

## Files

- `selection_engine.py`: deterministic source selection logic and rationale generation.
- `fixtures.py`: deterministic task/source fixtures used by tests.
- `test_selection_engine.py`: unittest coverage for required selection behavior.

## Run tests (Windows)

From this demo folder:

```powershell
py -m unittest -v
# or
python -m unittest -v
```

From the repo root:

```powershell
py -m unittest -v demos/atlas-source-selection-demo/test_selection_engine.py
# or
python -m unittest -v demos/atlas-source-selection-demo/test_selection_engine.py
```
