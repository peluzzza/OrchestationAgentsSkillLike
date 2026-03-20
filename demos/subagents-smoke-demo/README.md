# Subagents smoke demo

This folder is a tiny, self-contained demo to verify that subagents are running and can collaborate end-to-end.

## What you should see

- Tests pass.
- You can run an orchestration loop (Oracle → Hermes → Sisyphus → Themis → Argus) to implement a small change and re-verify.

## Run the tests (Windows)

Option A (recommended): from this folder:

```powershell
py -m unittest -v
# or
python -m unittest -v
```

Option B: from the repo root:

```powershell
py -m unittest -v demos/subagents-smoke-demo/test_calc.py
# or
python -m unittest -v demos/subagents-smoke-demo/test_calc.py
```

## Orchestrate the fix with subagents

Open Copilot Chat and use the prompt in `DEMO_PROMPT.md`.
