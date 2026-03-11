Copy/paste this into Copilot Chat (as @Atlas):

Goal: Add a small feature to `demos/subagents-smoke-demo` with tests, using the smallest possible code change.

Feature:
- Add `mod(a, b)` to `calc.py`.
- Add tests for:
  - `mod(5, 2) == 1`
  - `mod(5, 5) == 0`
  - `mod(1, 0)` raises `ZeroDivisionError`

Constraints:
- Only change files under `demos/subagents-smoke-demo/`.
- Keep the diff minimal (no refactors).
- Verification command (Windows):
  - `py -m unittest -v` (fallback: `python -m unittest -v`)

Process:
1) Ask Oracle for acceptance criteria and risks.
2) Ask Explorer to locate the best place to add the feature with minimal surface area.
3) Ask Sisyphus to implement the feature (tests-first if appropriate).
4) Ask Code-Review to review the diff for minimalism and correctness.
5) Ask Argus to propose/confirm the exact command to verify.

Definition of done:
- All tests pass.
