# Model selection strategy (role-specific)

This repo uses VS Code Copilot Custom Agents (`*.agent.md`). In these files, the `model:` field is an **ordered preference list**: VS Code will try models from top to bottom and pick the **first available** model.

This means we cannot "dynamically" swap models per subtask at runtime; instead, we:

1) Delegate the task to the *right specialist agent* (Oracle/Hermes/Sisyphus/…)
2) Give that specialist a **short, role-appropriate** model list

## Evidence-backed mapping

We prioritize model families based on vendor-documented positioning and the user-requested 2026 role policy:

- **GPT-5.4**: strongest general-purpose reasoning/orchestration option currently used in this repo.
- **Claude Opus 4.6**: top implementation-grade model for high-quality code generation.
- **Claude Sonnet 4.6**: best balance of speed and intelligence for planning, implementation fallback, and operations.
- **Claude Haiku 4.5**: fastest currently supported Claude tier.
- **Gemini 3 Flash (Preview)**: low-latency, high-volume choice for reconnaissance and frontend-specialist work.
- **GPT-5.3-Codex**: specialized software-engineering fallback when Codex behavior is preferred.

Important notes:

- Google’s docs indicate **Gemini 3 Pro Preview is deprecated and was shut down on 2026-03-09**, so we avoid it entirely.
- Some requested labels (for example a second newer Flash tier or `GPT-5.4-Codex`) are not currently accepted by the local prompt validator, so this repo uses the **closest currently supported Copilot labels** while preserving the intended role distribution.

## Current repo configuration (by role)

Workspace agents live in `.github/agents/`; mirrored orchestration copies live in `plugins/atlas-orchestration-team/agents/`; frontend-specialist workflow agents live in `plugins/frontend-workflow/agents/`.

- **Orchestrators** (`Atlas`, `Afrodita`): `GPT-5.4` → `Claude Sonnet 4.6`
- **Planning agents** (`Prometheus`, `Oracle`, `SpecifyAnalyze`, `SpecifyClarify`, `SpecifyConstitution`, `SpecifyPlan`, `SpecifySpec`, `SpecifyTasks`, `Frontend-Planner`): `GPT-5.4` → `Claude Sonnet 4.6` → `GPT-5.2`
- **Implementation agents** (`Sisyphus`, `SpecifyImplement`): `Claude Opus 4.6` → `Claude Sonnet 4.6` → `GPT-5.4` → `GPT-5.3-Codex`
- **Exploration agents** (`Hermes`, `PackCatalog`): `Gemini 3 Flash (Preview)` → `Claude Haiku 4.5` → `GPT-5.2`
- **Frontend specialists** (`Frontend-Engineer`, `UI-Designer`, `Style-Engineer`, `State-Manager`, `Component-Builder`, `A11y-Auditor`, `Frontend-Reviewer`): `Gemini 3 Flash (Preview)` → `Claude Haiku 4.5` → `Claude Sonnet 4.6`
- **Review** (`Themis`): `GPT-5.3-Codex`
- **Verification** (`Argus`): `Claude Sonnet 4.6`
- **Build / release** (`Hephaestus`): `Claude Sonnet 4.6` → `GPT-5.4` → `GPT-5.2`

## Sources

- Anthropic model overview (Opus/Sonnet/Haiku positioning):
  - https://platform.claude.com/docs/en/docs/about-claude/models
- Google Gemini model list (Flash positioning + Gemini 3 Pro Preview shutdown notice):
  - https://ai.google.dev/gemini-api/docs/models/gemini
- OpenAI Codex overview (Codex as software engineering agent):
  - https://openai.com/index/introducing-codex/
