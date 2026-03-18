# Tasks: Expense Tracker CLI

## Phase 1: Setup

**Goal**: Project skeleton, test harness, `.gitignore`
**Independent Test**: `python expenses.py --help` exits 0

- [ ] T001 Create `expenses.py` with argparse entry point and `--help`
- [ ] T002 Create `test_expenses.py` with one placeholder test class
- [ ] T003 Create `.gitignore` with Python patterns

## Phase 2: Foundational ⚠️ CRITICAL — do not skip

**Goal**: `Expense` dataclass + `ExpenseStore` JSON persistence
**Independent Test**: Save one expense, reload, compare — identical

- [ ] T004 [P] Implement `Expense` dataclass (id, amount, category, description, date)
- [ ] T005 [P] Implement `ExpenseStore.load()` and `ExpenseStore.save()` using `expenses.json`
- [ ] T006 Write `test_save_load_roundtrip` and `test_empty_store_returns_empty_list`

## Phase 3: US1 — Add Expense 🎯 MVP

**Goal**: Working `add` command
**Independent Test**: `python expenses.py add 10.0 food "test"` → stored and confirmed

- [ ] T007 Implement `add` command handler with amount > 0 validation
- [ ] T008 Write `test_add_valid_expense`
- [ ] T009 Write `test_add_invalid_amount_raises`

## Phase 4: US2 — List Expenses

**Goal**: Working `list` command with optional `--category` filter
**Independent Test**: `python expenses.py list` shows stored expenses

- [ ] T010 Implement `list` command with optional `--category` filter
- [ ] T011 Write `test_list_all_expenses`
- [ ] T012 Write `test_list_filtered_by_category`

## Phase 5: US3 — Monthly Summary

**Goal**: Working `summary` command
**Independent Test**: `python expenses.py summary` shows month totals

- [ ] T013 Implement `summary` command grouping by YYYY-MM
- [ ] T014 Write `test_summary_groups_by_month`

## Phase 6: Polish

- [ ] T015 Update README with usage examples
- [ ] T016 Run full test suite — confirm all pass
