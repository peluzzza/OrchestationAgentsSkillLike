# [PROJECT_NAME] Constitution
<!-- Example: Atlas Orchestration Team Constitution -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Conductor-First Visibility -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: In the default install mode only the primary conductor is user-visible. Approved domain conductors may also be user-visible when explicitly enabled; all specialist subagents MUST default to user-invocable: false. -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. Spec-Driven Development -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: No implementation begins without a validated spec, plan, and task list. Pipeline: SP-1 Constitution → SP-2 Spec → SP-3 Clarify → SP-4 Plan → SP-5 Analyze (gate) → EX-0 Tasks → EX-1 Analyze (gate) → EX-2 Implement -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Progressive Delegation -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: Atlas delegates to specialists aggressively. Atlas synthesizes; it does not duplicate non-trivial subagent work. Trivial synthesis, plan writing, and small non-code tasks may still be handled directly when orchestration overhead would exceed value. Routing: exploration → Hermes, analysis → Oracle, planning → Prometheus, implementation → Sisyphus/Afrodita-UX, review → Themis, verification → Argus, build → Hephaestus. -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Atomic Task Execution -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Tasks are T001..Tnnn format with [P] for parallel-safe tasks and [USn] for story alignment. Each phase has a named checkpoint. SpecifyImplement marks [x] immediately on completion. -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Root-First Bootstrap -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: .specify/ directory MUST exist at repo root before any feature spec work. Templates are sourced from .specify/templates/. SpecifyConstitution errors if templates are absent rather than hallucinating structure. -->

### [PRINCIPLE_6_NAME]
<!-- Example: VI. Gate-Based Progression -->
[PRINCIPLE_6_DESCRIPTION]
<!-- Example: Two hard blocking gates: SpecifyAnalyze at SP-5 (before plan delivery) and EX-1 (before implementation). Zero blocking findings required to pass. Overrides require documented justification in the plan. -->

### [PRINCIPLE_7_NAME]
<!-- Example: VII. Human Sovereignty -->
[PRINCIPLE_7_DESCRIPTION]
<!-- Example: Human operator has unconditional authority to interrupt, override, or redirect at any point. Atlas honours enabled_agents/disabled_agents prompt-level controls before every delegation. -->

## Workflow Boundaries
<!-- Example: Table of which agents may write where, to prevent scope creep -->

| Agent | May write to | May NOT write to |
|-------|-------------|-----------------|
| [AGENT_1] | [WRITE_SCOPE] | [EXCLUDED_SCOPE] |
| [AGENT_2] | [WRITE_SCOPE] | [EXCLUDED_SCOPE] |

## Governance

[GOVERNANCE_RULES]
<!-- Example:
### Amendment Procedure
1. Propose as a pull request with `docs: amend constitution` commit message.
2. Increment version: MAJOR (removal/redefinition), MINOR (addition), PATCH (clarification).
3. SpecifyConstitution runs consistency propagation over all four templates after any amendment.
4. Human operator provides final approval before merge.

### Compliance Review
All PRs modifying agent files, templates, or .specify/ artifacts MUST self-check:
- [ ] No user-invocable: true agent added without approval
- [ ] No implementation before matching spec + plan + tasks exist
- [ ] Gate findings addressed or overridden with documented justification
-->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
