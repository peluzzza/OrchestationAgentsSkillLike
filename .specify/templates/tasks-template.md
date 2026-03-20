---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `.specify/specs/[###-feature-name]/`  
**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `research.md`, `data-model.md`, `contracts/`  
**Gate**: `analysis-report.md` from EX-1 `SpecifyAnalyze` MUST show zero blocking findings before `SpecifyImplement` begins.

**Tests**: Include test tasks whenever executable verification is needed for a user story, contract, or integration path. Skip them only when the spec explicitly records a justified no-test exception.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description — file/path`

- **[P]**: Can run in parallel (different files, no shared mutations)
- **[Story]**: User story this task belongs to (e.g., US1, US2)
- Include exact file paths in task descriptions

## Path Conventions

- **Agent/config repo** (default for this repo): `.github/agents/`, `plugins/`, `.specify/`
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- Adjust based on `plan.md` structure decision

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration only.

  SpecifyTasks MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3…)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Contracts from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create/verify project structure per implementation plan
- [ ] T002 [P] Initialize dependencies or agent scaffold files
- [ ] T003 [P] Configure linting, formatting, or validation tooling

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before any user story begins

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [description — foundational shared dependency]
- [ ] T005 [P] [description — foundational shared dependency]
- [ ] T006 [P] [description — foundational shared dependency]

**Checkpoint**: Foundation ready — user story implementation can begin in parallel

---

## Phase 3: User Story 1 — [Title] (Priority: P1) 🎯 MVP

**Goal**: [What this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Implementation for User Story 1

- [ ] T007 [P] [US1] [Description] — [file path]
- [ ] T008 [P] [US1] [Description] — [file path]
- [ ] T009 [US1] [Description] — [file path] (depends on T007, T008)
- [ ] T010 [US1] [Description] — [file path]

**Checkpoint**: User Story 1 fully functional and independently testable

---

## Phase 4: User Story 2 — [Title] (Priority: P2)

**Goal**: [What this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Implementation for User Story 2

- [ ] T011 [P] [US2] [Description] — [file path]
- [ ] T012 [US2] [Description] — [file path]
- [ ] T013 [US2] Integrate with User Story 1 components (if needed) — [file path]

**Checkpoint**: User Stories 1 AND 2 work independently and together

---

## Phase 5: User Story 3 — [Title] (Priority: P3)

**Goal**: [What this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Implementation for User Story 3

- [ ] T014 [P] [US3] [Description] — [file path]
- [ ] T015 [US3] [Description] — [file path]

**Checkpoint**: All user stories implemented and individually verifiable

---

## Phase 6: Integration & Quality Gate

**Purpose**: Verify the full feature works end-to-end and passes Argus

- [ ] T016 [P] Verify all spec acceptance scenarios pass
- [ ] T017 [P] Confirm all `[x]` marks complete in this file
- [ ] T018 Run `SpecifyAnalyze` final pass — confirm zero blocking findings
- [ ] T019 Verify constitution compliance (no `user-invocable: true` leaked, etc.)

**Final Checkpoint**: All tasks `[x]`, Argus green, ready for Themis gate
