# UX Enhancement Workflow

Opt-in plugin pack for UX research, spec writing, flow critique, and frontend handoff.

> **Donor inspiration:** UI UX Pro Max deep-research and critique patterns, Everything Claude Code delegation ergonomics, Superpowers modular packaging.
> **Memory contract:** Reads session continuity from `.specify/memory/session-memory.md` and durable decisions from `.specify/memory/decision-log.md`. Does not create a duplicate memory store.
> **Non-overlap:** This pack does **not** replace `frontend-workflow`. `Afrodita` / `frontend-workflow` handles implementation (React, Vue, Angular, TDD, styling). This pack handles research, flow design, heuristic critique, and spec packaging — upstream of implementation.

## Architecture

```
UX-Atlas (Conductor - User Visible)
    ├── UX-Planner (Autonomous Planning & Research)
    ├── User-Flow-Designer (User journey & flow mapping)
    ├── Design-Critic (Heuristic evaluation & critique)
    ├── Accessibility-Heuristics (WCAG & inclusion review)
    └── Frontend-Handoff (Spec packaging for implementation)

    Handoffs → Afrodita (implementation), Backend-Atlas (API contract)
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| **UX-Atlas** | Conductor - orchestrates the team | GPT-5.4 |
| **UX-Planner** | Autonomous planning & UX research | GPT-5.4 |
| **User-Flow-Designer** | User journey mapping and flow diagrams | Gemini 3 Flash (Preview) |
| **Design-Critic** | Heuristic evaluation and UX critique | Claude Opus 4.6 |
| **Accessibility-Heuristics** | WCAG 2.1 AA and inclusive design review | Claude Sonnet 4.6 |
| **Frontend-Handoff** | Spec packaging for Afrodita / implementation | Gemini 3 Flash (Preview) |

## Workflow

1. **Research & Planning Phase**
   - `UX-Planner` researches user goals and produces a UX research brief
   - User reviews and approves scope

2. **Design Phase**
   - `User-Flow-Designer` maps user journeys and interaction flows
   - User approves flow spec

3. **Critique Phase**
  - `Design-Critic` runs heuristic evaluation (Nielsen's 10 heuristics)
  - `Accessibility-Heuristics` runs after the critique to verify WCAG 2.1 AA and inclusive design
  - Returns: APPROVED | NEEDS_REVISION

4. **Handoff Phase**
   - `Frontend-Handoff` packages spec for implementation team
   - If API contracts are needed → handoff to `Backend-Atlas`
   - If ready to implement → handoff to `Afrodita`

## Usage

Enable in `.vscode/settings.json`:

```json
{
  "chat.agentFilesLocations": {
    ".github/agents": true,
    "plugins/ux-enhancement-workflow/agents": true
  }
}
```

Then invoke `@UX-Atlas` in Copilot Chat.

## Installation via Marketplace

```json
{
  "chat.plugins.marketplaces": [
    { "source": "peluzzza/OrchestationAgentsSkillLike" }
  ]
}
```

Install `ux-enhancement-workflow` from the marketplace panel, then reload VS Code.

## Non-Overlap With frontend-workflow

| Concern | Pack | Conductor |
|---------|------|-----------|
| UX research, flow mapping, heuristic critique, spec | `ux-enhancement-workflow` | UX-Atlas |
| Component implementation, TDD, styling, state | `frontend-workflow` | Afrodita |
| API contracts | `backend-workflow` | Backend-Atlas |
