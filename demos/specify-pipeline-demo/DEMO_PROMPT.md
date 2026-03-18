# Demo Prompt — Specify Pipeline

Copy and paste into VS Code Copilot Chat (`@Atlas`):

---

## Option A — Full Pipeline (Planning + Implementation)

```
@Atlas Use the full Specify pipeline to plan and implement a new feature in demos/specify-pipeline-demo.

Feature: Expense Tracker CLI

Build a CLI tool with three commands:
- python expenses.py add <amount> <category> "<description>"  → stores an expense
- python expenses.py list [--category <cat>]                  → lists all expenses
- python expenses.py summary                                  → totals grouped by month

Constraints:
- Python stdlib only (no pip installs)
- All files go inside demos/specify-pipeline-demo/
- Expenses stored in expenses.json inside the demo folder

Required process — use Prometheus to run the full Specify pipeline before any code:
1. SpecifyConstitution → .specify/memory/constitution.md
2. SpecifySpec         → .specify/specs/expense-tracker/spec.md
3. SpecifyPlan         → plan.md, data-model.md, research.md, quickstart.md
4. SpecifyTasks        → tasks.md with T001..Tnnn format
5. SpecifyAnalyze      → consistency validation
6. Sisyphus (SpecifyImplement) → implement following tasks.md phase by phase

Definition of done:
  cd demos/specify-pipeline-demo
  py -m unittest -v
All tests must pass, including TestPipelineIntegration and TestImplementationSmoke.
```

---

## Option B — Planning Only (faster, tests pipeline without implementation)

```
@Atlas Use Prometheus to run the full Specify pipeline for a new feature. Do not implement code yet.

Feature: Expense Tracker CLI in demos/specify-pipeline-demo/
- add <amount> <category> "<description>": store an expense
- list [--category <cat>]: list expenses
- summary: monthly totals

Run: SpecifyConstitution → SpecifySpec → SpecifyPlan → SpecifyTasks → SpecifyAnalyze

All artifacts go under demos/specify-pipeline-demo/.specify/
Feature slug: expense-tracker

After the pipeline, run:
  cd demos/specify-pipeline-demo
  py -m unittest -v
(TestPipelineIntegration tests should pass; TestImplementationSmoke will still be skipped)
```

---

## Expected Output After Option A

```
Ran 18 tests in 0.XXXs

test_valid_constitution_passes              ... ok
test_missing_principles_section_fails       ... ok
test_missing_version_metadata_fails         ... ok
test_valid_spec_passes                      ... ok
test_missing_user_stories_section_fails     ... ok
test_missing_functional_requirements_section_fails ... ok
test_missing_fr_references_fails            ... ok
test_missing_given_when_then_fails          ... ok
test_valid_plan_passes                      ... ok
test_missing_technical_context_fails        ... ok
test_missing_implementation_phases_fails    ... ok
test_missing_phase_headings_fails           ... ok
test_valid_tasks_passes                     ... ok
test_insufficient_tasks_fails               ... ok
test_missing_t001_fails                     ... ok
test_wrong_task_format_fails                ... ok
test_nonexistent_file_returns_failed_result ... ok
test_valid_fixture_constitution_via_validate_file ... ok
test_valid_fixture_tasks_via_validate_file  ... ok
--- TestPipelineIntegration ---
test_constitution_artifact_is_valid         ... ok
test_spec_artifact_is_valid                 ... ok
test_plan_artifact_is_valid                 ... ok
test_tasks_artifact_is_valid                ... ok
test_data_model_artifact_exists             ... ok
test_research_artifact_exists               ... ok
test_full_pipeline_report_passes            ... ok
--- TestImplementationSmoke ---
test_expenses_module_imports_cleanly        ... ok

OK
```
