# Expected Agent Flow — Specify Pipeline Demo

What each agent should do when you run the demo prompt via `@Atlas`.

---

## Atlas — Initialization

**Atlas** parses the request and identifies it as planning + implementation.

Expected output:
```
Goal: Plan and implement expense tracker CLI using the Specify pipeline.
Constraints: stdlib only, all artifacts in demos/specify-pipeline-demo/.
Success: py -m unittest -v passes (all test classes including integration).

Status: planning
Delegations: Routing to Prometheus for full Specify pipeline (SP-0..SP-5).
```

---

## SP-0 — Prometheus → Explorer + Oracle (parallel)

**Prometheus** dispatches Explorer and Oracle in parallel.

- **Explorer** scans `demos/specify-pipeline-demo/` → finds `spec_validator.py`,
  `fixtures/`, existing tests, no `.specify/` directory yet.
- **Oracle** reviews Python CLI patterns, argparse best practices, stdlib JSON persistence.

Expected return:
```
CONTEXT: demos/specify-pipeline-demo/ has validator + fixtures, no .specify/ yet
TECH_STACK_HINT: Python stdlib (json, argparse, pathlib, datetime)
FEATURE_DIR: demos/specify-pipeline-demo/.specify/specs/expense-tracker/
```

---

## SP-1 — Prometheus → SpecifyConstitution

SpecifyConstitution creates `.specify/memory/constitution.md`.

Expected principles:
- P1: Simplicity First
- P2: Test Coverage
- P3: stdlib Only
- P4: Fail Fast

Expected artifact:
```
.specify/memory/constitution.md  (new file)
CONSTITUTION_STATUS: CREATED
VERSION: 1.0.0
```

---

## SP-2 — Prometheus → SpecifySpec

SpecifySpec creates `.specify/specs/expense-tracker/spec.md`.

Must include:
- 3 user stories: US1 Add (P1), US2 List (P1), US3 Summary (P2)
- FR-001..FR-005 functional requirements
- Given/When/Then acceptance scenarios for each story
- Success Criteria SC-001..SC-004

Expected artifacts:
```
.specify/specs/expense-tracker/spec.md              (new)
.specify/specs/expense-tracker/checklists/requirements.md  (new)
SPEC_STATUS: READY_FOR_PLANNING
NEEDS_CLARIFICATION: 0
```

---

## SP-3 — Prometheus → SpecifyClarify (conditional)

Only runs if `NEEDS_CLARIFICATION > 0`. Expected: **SKIPPED** for this well-scoped feature.

If it runs, it should resolve questions about storage location and amount validation behavior before continuing.

---

## SP-4 — Prometheus → SpecifyPlan

SpecifyPlan executes two phases:

**Phase 0 (Research)** — dispatches Explorer/Oracle for:
- Python argparse subcommand patterns
- JSON file persistence approach
- Pathlib for cross-platform file paths

Produces `.specify/specs/expense-tracker/research.md` with decisions.

**Phase 1 (Design)** — produces:
- `plan.md` with Technical Context table + 5 implementation phases
- `data-model.md` with `Expense` entity (id, amount, category, description, date)
- `quickstart.md` with dev environment setup
- No external contracts (internal CLI tool)

Expected artifacts:
```
.specify/specs/expense-tracker/plan.md          (new)
.specify/specs/expense-tracker/data-model.md    (new)
.specify/specs/expense-tracker/research.md      (new)
.specify/specs/expense-tracker/quickstart.md    (new)
PLAN_STATUS: COMPLETE
CONSTITUTION_CHECK: PASS
TECH_STACK: Python 3.11+, stdlib only
```

---

## SP-5 — Prometheus → SpecifyAnalyze

SpecifyAnalyze performs 6 detection passes (READ-ONLY):

| Pass | Check | Expected |
|---|---|---|
| A — Duplication | Overlapping requirements | None |
| B — Ambiguity | Vague terms | May flag "positive number" → clarify to "> 0" |
| C — Underspecification | FRs without acceptance criteria | All covered |
| D — Constitution Alignment | stdlib constraint in plan | PASS |
| E — Coverage Gaps | All FRs traced to tasks | PASS (after tasks exist) |
| F — Inconsistency | data-model entities match spec | PASS |

Expected return:
```
READY_FOR_IMPLEMENTATION: true
FINDINGS: 0 CRITICAL, 0-2 MEDIUM (informational only)
ANALYSIS_REPORT: .specify/specs/expense-tracker/analysis-report.md
```

---

## EX-0 — Sisyphus → SpecifyTasks

SpecifyTasks generates `tasks.md` from plan.md + spec.md.

Must produce:
- T001..T016 in standard format `- [ ] T001 [P] [US1] Description`
- 6 phases: Setup, Foundational (CRITICAL), US1 MVP, US2, US3, Polish
- Parallel markers `[P]` on T004/T005 (independent dataclass + store)

Expected artifact:
```
.specify/specs/expense-tracker/tasks.md  (new)
TASKS_COUNT: 14-18
PHASES: 6
```

---

## EX-1 — Sisyphus → SpecifyAnalyze (gate)

Second analyze pass after tasks.md is generated.

Verifies:
- All user stories have corresponding tasks
- Phase sequencing is logical
- No task references undefined files/entities

Expected: `READY_FOR_IMPLEMENTATION: true`

---

## EX-2 — Sisyphus → SpecifyImplement

SpecifyImplement executes tasks phase by phase, marking `[x]` on each completed task.

**Phase 1** (T001-T003): `expenses.py` skeleton + `test_expenses.py` + `.gitignore`
**Phase 2** (T004-T006): `Expense` dataclass + `ExpenseStore` + save/load tests
**Phase 3** (T007-T009): `add` command + validation + tests
**Phase 4** (T010-T012): `list` command + `--category` filter + tests
**Phase 5** (T013-T014): `summary` command + monthly grouping tests
**Phase 6** (T015-T016): README + final test run

Expected outcome:
```
IMPLEMENT_STATUS: COMPLETE
TASKS_COMPLETED: 16/16
FILES_CREATED: expenses.py, test_expenses.py, .gitignore
TESTS_STATUS: PASS
```

---

## Final Verification

```bash
cd demos/specify-pipeline-demo
py -m unittest -v
```

| Test Class | Count | Should |
|---|---|---|
| TestConstitutionValidation | 3 | PASS |
| TestSpecValidation | 5 | PASS |
| TestPlanValidation | 4 | PASS |
| TestTasksValidation | 4 | PASS |
| TestValidateFile | 3 | PASS |
| TestPipelineIntegration | 7 | PASS (after SP-0..SP-5) |
| TestImplementationSmoke | 1 | PASS (after EX-0..EX-2) |

**Total: ~27 tests, all green.**

---

## What Each Test Validates

| Test | Validates |
|---|---|
| `test_constitution_artifact_is_valid` | SpecifyConstitution produced correct structure |
| `test_spec_artifact_is_valid` | SpecifySpec wrote user stories + FRs + GWT |
| `test_plan_artifact_is_valid` | SpecifyPlan wrote Technical Context + phases |
| `test_tasks_artifact_is_valid` | SpecifyTasks used T001..Tnnn format + phases |
| `test_data_model_artifact_exists` | SpecifyPlan Phase 1 ran (produced data-model.md) |
| `test_research_artifact_exists` | SpecifyPlan Phase 0 ran (produced research.md) |
| `test_full_pipeline_report_passes` | All 4 artifacts pass validator simultaneously |
| `test_expenses_module_imports_cleanly` | SpecifyImplement produced working Python module |
