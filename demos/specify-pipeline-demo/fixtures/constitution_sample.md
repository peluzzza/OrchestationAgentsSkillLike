# Expense Tracker — Project Constitution

## Version

**Version**: 1.0.0 | **Ratified**: 2026-03-18 | **Last Amended**: 2026-03-18

## Principles

### P1: Simplicity First

Prefer simple, readable solutions over clever ones. Every line of complexity must justify itself against a concrete requirement.

### P2: Test Coverage

All public functions must have corresponding unit tests. No untested code ships.

### P3: stdlib Only

Use Python standard library unless a compelling, documented reason exists to add a dependency. External dependencies must appear in a dedicated section of the plan.

### P4: Fail Fast

Validate all inputs at entry points. Raise descriptive errors immediately rather than silently corrupting state or returning wrong results.
