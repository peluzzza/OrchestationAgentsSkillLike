# Agent Pack Catalog

Minimal discovery pack for the `OrchestationAgentsSkillLike` marketplace.

This pack is intentionally small: it helps users inspect the available packs, choose the smallest useful installation set, and get exact VS Code setup instructions.

## Purpose

- read `.github/plugin/marketplace.json`
- summarize available packs
- recommend the right pack(s) for the current repo context
- explain installation via marketplace, plugin path, or agents-only fallback

## Conductor

| Agent | Role |
|-------|------|
| `PackCatalog` | User-invocable discovery conductor for pack selection and installation guidance |

## Installation

Use one of these approaches:

1. **Marketplace**
   - enable `chat.plugins.enabled`
   - add `peluzzza/OrchestationAgentsSkillLike` to `chat.plugins.marketplaces`
2. **Local plugin path**
   - add this repo's `plugins/` directory to `chat.plugins.paths`
3. **Agents-only fallback**
   - copy pack agents into a workspace agent directory if marketplace mode is unavailable

## Notes

- This pack complements `atlas-orchestration-team`; it does not replace it.
- Claude-Mem-inspired continuity already lives in `.specify/memory/`; no separate memory pack is required.
