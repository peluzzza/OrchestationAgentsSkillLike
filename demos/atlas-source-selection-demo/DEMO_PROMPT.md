Copy/paste this into Copilot Chat (as @Atlas):

Goal: implement and verify deterministic source selection in `demos/atlas-source-selection-demo`.

Requirements:
- Use Python stdlib only.
- Ensure selection logic supports:
  - origin precedence (`github > plugin > other`),
  - capability and task-type matching,
  - preferred source selection with fallback if unavailable,
  - deterministic tie-break for equivalent candidates.
- Keep all changes under `demos/atlas-source-selection-demo/`.

Process:
1) Ask Oracle to confirm acceptance criteria and edge cases.
2) Ask Hermes to inspect fixtures and identify minimal code surface.
3) Ask Sisyphus to implement or adjust tests-first.
4) Ask Themis to validate deterministic behavior and rationale clarity.
5) Ask Argus for exact verification command.

Definition of done:
- `py -m unittest -v` passes from this demo folder.
- Required tests pass:
  - deterministic tie-break,
  - capability matching by task type,
  - github precedence on duplicate source,
  - fallback when preferred source unavailable.
