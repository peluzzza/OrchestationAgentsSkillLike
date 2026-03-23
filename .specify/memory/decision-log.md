# Decision Log

This file records durable architecture and workflow decisions for the orchestration repository. Keep the log concise and bias toward decisions that change future implementation or review behavior.

| Date | Scope | Decision | Rationale | Consequence |
|------|-------|----------|-----------|-------------|
| 2026-03-22 | Merge strategy | Keep `.github/agents` as canonical and `plugins/` as optional | Preserves zero-setup path and avoids source ambiguity | All future imports must justify whether they belong in core or plugin space |
| 2026-03-22 | Memory | Start with file-backed memory under `.specify/memory/` | Lowest-risk way to validate continuity and recall value | No database/service dependency is introduced for memory yet |
| 2026-03-22 | External ecosystems | Import capabilities by folder instead of copying donor repos wholesale | Reduces drift, noise, and donor-specific coupling | Merge work will proceed through phased folder lanes |
| 2026-03-23 | Optional packs | Deliver automation/MCP and UX as opt-in plugin packs, not as core agents | Keeps external ecosystem capabilities available without weakening the root-first default experience | New workflow conductors live under `plugins/`, while core memory remains shared in `.specify/memory/` |
