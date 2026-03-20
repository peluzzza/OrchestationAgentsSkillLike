# Model selection strategy (role-specific)

This repo uses VS Code Copilot Custom Agents (`*.agent.md`). In these files, the `model:` field is an **ordered preference list**: VS Code will try models from top to bottom and pick the **first available** model.

This means we cannot "dynamically" swap models per subtask at runtime; instead, we:

1) Delegate the task to the *right specialist agent* (Oracle/Hermes/Sisyphus/…)
2) Give that specialist a **short, role-appropriate** model list

## Evidence-backed mapping

We prioritize model families based on their vendor-documented positioning:

- **Codex**: optimized for software engineering workflows and coding tasks.
- **Claude Opus**: most intelligent for building agents and coding.
- **Claude Sonnet**: best balance of speed and intelligence.
- **Claude Haiku**: fastest option.
- **Gemini Flash**: low-latency, high-volume tasks.

Important: Google’s docs indicate **Gemini 3 Pro Preview is deprecated and was shut down on 2026-03-09**, so we avoid putting it in agent `model:` lists.

## Current repo configuration (by agent)

Workspace agents are in `.github/agents/` and plugin-pack copies (if used) are in `plugins/**/agents/`.

- `Atlas` (orchestrator): Opus → GPT-5.2 → Sonnet → Flash → Haiku → GPT-4.1
- `Oracle` (requirements/acceptance criteria): Opus → GPT-5.2 → Sonnet → GPT-4.1
- `Themis` (deep review): Opus → GPT-5.2 → Sonnet → GPT-4.1
- `Sisyphus` (implementation): GPT-5.3-Codex → Opus → GPT-5.2 → Sonnet → GPT-4.1
- `Hermes` (fast repo reconnaissance): Flash → Haiku → GPT-5.2 → Sonnet → GPT-4.1
- `Argus` (tests/log triage): Flash → Haiku → GPT-5.2 → GPT-4.1
- `Hephaestus` (build/release): Sonnet → GPT-5.2 → GPT-4.1
- `Frontend-Engineer` (UI work): Sonnet → GPT-5.2 → GPT-4.1
- `PackCatalog` (catalog/discovery): Flash → Haiku → GPT-5.2 → GPT-4.1

## Sources

- Anthropic model overview (Opus/Sonnet/Haiku positioning):
  - https://platform.claude.com/docs/en/docs/about-claude/models
- Google Gemini model list (Flash positioning + Gemini 3 Pro Preview shutdown notice):
  - https://ai.google.dev/gemini-api/docs/models/gemini
- OpenAI Codex overview (Codex as software engineering agent):
  - https://openai.com/index/introducing-codex/
