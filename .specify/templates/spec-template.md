# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## Constitution Check

*Verify against `.specify/memory/constitution.md` before proceeding.*

- [ ] Spec-Driven Development gate: spec completes before any plan or implementation begins
- [ ] Scope is bounded to a single feature slug — no cross-feature pollution
- [ ] At most 3 `[NEEDS CLARIFICATION]` markers permitted

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE — if you implement just ONE of them,
  you should still have a viable MVP that delivers value.

  Assign priorities (P1, P2, P3…) to each story, where P1 is most critical.
  Think of each story as a standalone slice that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 — [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently — e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 — [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain value and priority]

**Independent Test**: [How this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 — [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain value and priority]

**Independent Test**: [How this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: Fill with concrete functional requirements.
  Use MUST/SHOULD/MAY language aligned with constitution principles.
  Limit [NEEDS CLARIFICATION] markers to 3 maximum throughout the document.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability]
- **FR-002**: System MUST [specific capability]
- **FR-003**: Users MUST be able to [key interaction]
- **FR-004**: System MUST [data requirement]
- **FR-005**: System MUST [behavior]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation detail]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  Define measurable, technology-agnostic outcomes.
  These feed directly into Argus verification after implementation.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric — e.g., "Users can complete [action] in under 2 minutes"]
- **SC-002**: [Agent-observable outcome — e.g., "Atlas routes [task type] to correct specialist 100% of the time"]
- **SC-003**: [Gate outcome — e.g., "SpecifyAnalyze reports zero blocking findings"]
- **SC-004**: [Quality metric — e.g., "All tasks marked [x] in tasks.md before PR is raised"]
