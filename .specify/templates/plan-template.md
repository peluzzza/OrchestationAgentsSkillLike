# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: `.specify/specs/[###-feature-name]/spec.md`  
**Input**: Feature specification from `.specify/specs/[###-feature-name]/spec.md`

**Note**: This file is produced by `SpecifyPlan` (SP-4). Do not edit manually until SP-5 `SpecifyAnalyze` gate has passed.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Fill in technical details. Mark unknowns as NEEDS CLARIFICATION.
  These are resolved in Phase 0 (research.md).
-->

**Language/Version**: [e.g., Python 3.12, TypeScript 5.x, Go 1.22 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, React, Gin or NEEDS CLARIFICATION]  
**Storage**: [e.g., PostgreSQL, Redis, files or N/A]  
**Testing**: [e.g., pytest, Vitest, go test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux container, browser, VS Code extension or NEEDS CLARIFICATION]  
**Project Type**: [e.g., agent-config/cli/web-service/library or NEEDS CLARIFICATION]  
**Performance Goals**: [domain-specific or N/A]  
**Constraints**: [e.g., context window limits, rate limits, agent tool restrictions or NEEDS CLARIFICATION]  
**Scale/Scope**: [e.g., single-user local, team workspace, multi-tenant or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Conductor-First Visibility | [ ] Pass / [ ] Violation | |
| II. Spec-Driven Development | [ ] Pass / [ ] Violation | |
| III. Progressive Delegation | [ ] Pass / [ ] Violation | |
| IV. Atomic Task Execution | [ ] Pass / [ ] Violation | |
| V. Root-First Bootstrap | [ ] Pass / [ ] Violation | |
| VI. Gate-Based Progression | [ ] Pass / [ ] Violation | |
| VII. Human Sovereignty | [ ] Pass / [ ] Violation | |

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|-----------|-------------------------------------|
| [principle name] | [current need] | [why compliant approach is insufficient] |

## Project Structure

### Documentation (this feature)

```text
.specify/specs/[###-feature]/
├── plan.md              ← this file (SP-4 output)
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
├── quickstart.md        ← Phase 1 output
├── contracts/           ← Phase 1 output
├── analysis-report.md   ← SP-5 / EX-1 output (SpecifyAnalyze)
└── tasks.md             ← EX-0 output (SpecifyTasks — NOT created by SpecifyPlan)
```

### Source Code (repository root)

<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout.
  Choose the option that matches the project type; delete unused options.
  The delivered plan MUST NOT contain Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Agent/config repository (DEFAULT for this repo)
.github/
  agents/
    [AgentName].agent.md
plugins/
  [plugin-name]/
    agents/
      [AgentName].agent.md
.specify/
  memory/
  templates/
  specs/

# [REMOVE IF UNUSED] Option 2: Single project (library/CLI/service)
src/
├── models/
├── services/
└── cli/
tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 3: Web application
backend/src/
frontend/src/
```

**Structure Decision**: [Document the selected structure and the real directories involved]
