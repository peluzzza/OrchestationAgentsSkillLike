# Feature: Expense Tracker CLI

## Summary

A CLI tool to track personal expenses, categorize them, and view monthly spending totals.

## User Stories

### US1 — Add Expense (P1)

As a user, I want to add an expense so that I can track my spending.

**Independent Test**: `python expenses.py add 25.50 food "Lunch"` → entry confirmed with ID, appears in `list` output.

**Acceptance Scenario**:
- Given the expense tracker is installed
- When I run `add 25.50 food "Lunch"`
- Then the expense is stored with amount 25.50, category "food", and description "Lunch"

---

### US2 — List Expenses (P1)

As a user, I want to list all expenses so that I can review my spending history.

**Independent Test**: `python expenses.py list` → shows all stored expenses with amounts, categories, dates.

**Acceptance Scenario**:
- Given one or more expenses have been added
- When I run `list`
- Then all expenses are shown with ID, amount, category, description, and date

---

### US3 — Monthly Summary (P2)

As a user, I want to see a monthly spending summary so that I can understand my budget.

**Independent Test**: `python expenses.py summary` → shows totals grouped by year-month.

**Acceptance Scenario**:
- Given expenses exist across multiple months
- When I run `summary`
- Then totals are shown grouped by year-month in descending order

## Functional Requirements

- FR-001: The system shall persist all expenses to a local JSON file
- FR-002: The system shall support three commands: `add`, `list`, `summary`
- FR-003: The system shall validate that amount is a positive number (> 0)
- FR-004: The system shall support filtering `list` output by `--category`
- FR-005: The `summary` command shall group totals by calendar month (YYYY-MM)

## Success Criteria

- SC-001: All expenses survive process restart (written to disk immediately on `add`)
- SC-002: Invalid amount input shows a clear, actionable error message and exits non-zero
- SC-003: `summary` output groups spending correctly by year-month
- SC-004: `list --category food` returns only food expenses
