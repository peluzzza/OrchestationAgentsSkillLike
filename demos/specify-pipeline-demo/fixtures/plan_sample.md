# Technical Plan: Expense Tracker CLI

## Technical Context

| Field | Value |
|---|---|
| Language/Version | Python 3.11+ |
| Primary Dependencies | stdlib: `json`, `argparse`, `pathlib`, `datetime`, `collections` |
| Storage | `expenses.json` in demo folder |
| Testing | `unittest` (stdlib) |
| Target Platform | Cross-platform CLI (macOS, Windows, Linux) |
| Project Type | Single-module CLI tool |
| Performance Goals | < 100ms for any operation on up to 10,000 expenses |
| Constraints | stdlib only (constitution P3) |

## Constitution Check

| Principle | Status | Notes |
|---|---|---|
| P1: Simplicity First | PASS | Single-module design, no abstraction layers beyond what FR requires |
| P2: Test Coverage | PASS | test_expenses.py covers all public functions |
| P3: stdlib Only | PASS | json + argparse + pathlib + datetime — no pip installs |
| P4: Fail Fast | PASS | Amount validated at entry point before any storage write |

## Implementation Phases

### Phase 1: Project Setup

**Objective**: Create module skeleton and test harness.
**Files**: `expenses.py`, `test_expenses.py`, `.gitignore`
**Tests**: `test_cli_entry_point` — `python expenses.py --help` exits 0
**Done when**: Module imports without error, `--help` works

### Phase 2: Data Model

**Objective**: Implement `Expense` dataclass and JSON persistence.
**Files**: `expenses.py` (ExpenseStore class)
**Tests**: `test_save_load_roundtrip`, `test_empty_store_returns_empty_list`
**Done when**: Save + reload produces identical expense list

### Phase 3: Add Command

**Objective**: Implement `add` subcommand with validation.
**Files**: `expenses.py`
**Tests**: `test_add_valid_expense`, `test_add_invalid_amount_raises`
**Done when**: Valid add stores entry; invalid amount prints clear error and exits 1

### Phase 4: List Command

**Objective**: Implement `list` subcommand with optional `--category` filter.
**Files**: `expenses.py`
**Tests**: `test_list_all_expenses`, `test_list_filtered_by_category`
**Done when**: List shows all; `--category food` filters correctly

### Phase 5: Summary Command

**Objective**: Implement `summary` with year-month grouping.
**Files**: `expenses.py`
**Tests**: `test_summary_groups_by_month`
**Done when**: Summary output groups and totals correctly by YYYY-MM
