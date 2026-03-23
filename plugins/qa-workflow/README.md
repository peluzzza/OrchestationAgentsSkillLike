# QA Workflow

Specialized testing and quality assurance pack. Provides exhaustive test execution, coverage analysis, and mutation testing capabilities to the Argus quality gate.

## Architecture

```
Argus (L1 God — QA + Testing)
    └── qa-workflow pack
        ├── Test-Runner      (Execute test commands, return structured results)
        ├── Coverage-Analyst (Measure coverage, identify uncovered paths)
        └── Mutation-Tester  (Apply mutations, report mutation score)
```

## Agents

| Agent | Role | Invoked By |
|-------|------|-----------|
| **Test-Runner** | Execute targeted test suites | Argus |
| **Coverage-Analyst** | Measure and report coverage gaps | Argus |
| **Mutation-Tester** | Mutation testing and test suite strength | Argus |

## Usage

This pack is invoked by the `Argus` canonical god agent. It is not user-invocable.

Enable in `.vscode/settings.json`:
```json
"chat.agentFilesLocations": [
  "plugins/qa-workflow/agents"
]
```
