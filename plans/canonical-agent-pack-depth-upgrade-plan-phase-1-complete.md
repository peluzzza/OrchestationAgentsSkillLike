## Phase 1 Complete: Harden the research and planning layer
Strengthened the canonical research/planning agents so they now behave like real specialists instead of thin compatibility shells. The phase preserved local `.specify/specs/<feature>/` behavior and Prometheus fallback semantics while importing stronger structure, activation guards, delegation discipline, and return contracts from the donor pack.

**Files:** `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyAnalyze.agent.md`
**Functions:** `Hermes-subagent`, `Oracle-subagent`, `Prometheus`, `SpecifySpec`, `SpecifyPlan`, `SpecifyAnalyze`
**Implementation Scope:** Expanded thin research aliases into substantive specialists, hardened Prometheus planning/fallback contracts, aligned SpecifySpec↔Prometheus clarification semantics, standardized activation guards, and cleaned frontmatter/runtime compatibility.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0 executable tests; structural QA only
- Edge cases: verified unavailable-agent fallback behavior, clarification handshake consistency, constitution path consistency, and frontmatter/tool/agent contract sanity across all six files

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: Agent customization files only; no deploy surface involved

**Git Commit:**
chore: deepen planning agent contracts

- upgrade research and planning agents from thin aliases
- align Prometheus and Specify clarification contracts
- add activation guards and cleaner frontmatter semantics
