# Frontend Workflow

A specialized multi-agent orchestration system for frontend development, following the bigguy345/Atlas conductor pattern.

## Architecture

```
Frontend-Atlas (Conductor - User Visible)
    ├── Frontend-Planner (Autonomous Planning)
    ├── UI-Designer (Design & Architecture)
    ├── Style-Engineer (CSS & Animations)
    ├── State-Manager (State Patterns)
    ├── Component-Builder (TDD Implementation)
    ├── A11y-Auditor (Accessibility Review)
    └── Frontend-Reviewer (Code Review Gate)
    
    Handoffs → Backend-Atlas, DevOps-Atlas
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| **Frontend-Atlas** | Conductor - orchestrates the team | Claude Opus 4.5 |
| **Frontend-Planner** | Autonomous planning for complex tasks | GPT-5.2 |
| **UI-Designer** | Component architecture & layout | Claude Sonnet 4.5 |
| **Style-Engineer** | CSS, animations, responsive | Claude Sonnet 4.5 |
| **State-Manager** | State management patterns | GPT-5.2 |
| **Component-Builder** | TDD component implementation | Claude Sonnet 4.5 |
| **A11y-Auditor** | Accessibility compliance | GPT-5.2 |
| **Frontend-Reviewer** | Code review gate | GPT-5.2 |

## Workflow

1. **Planning Phase** (for complex tasks)
   - `Frontend-Planner` researches and creates phased plan
   - User reviews and approves plan

2. **Design Phase**
   - `UI-Designer` creates component architecture
   - `Style-Engineer` aligns with design system
   - User approves design spec

3. **Implementation Phase**
   - `Component-Builder` implements with TDD (tests first)
   - `State-Manager` handles complex state patterns
   - `Style-Engineer` implements responsive styles

3. **Review Phase**
   - `A11y-Auditor` checks WCAG 2.1 AA compliance
   - `Frontend-Reviewer` validates code quality
   - Returns: APPROVED | NEEDS_REVISION | FAILED

4. **Completion**
   - Commit-ready code with full test coverage
   - Accessibility verified
   - Responsive design confirmed

## Usage

```
@Frontend-Atlas Build a dashboard widget showing user statistics with charts
```

Frontend-Atlas will:
1. Delegate design to UI-Designer
2. Research state patterns with State-Manager
3. Implement components via Component-Builder
4. Verify accessibility with A11y-Auditor
5. Code review via Frontend-Reviewer
6. Return completion summary

## Accessibility Standards

All components must meet:
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader compatibility
- Color contrast ratios (4.5:1)
- Respects `prefers-reduced-motion`

## Installation

Copy the `agents/` folder to your workspace or VS Code prompts directory.
