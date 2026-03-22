## Phase 3 Complete: Refresh strategy docs and validate consistency
Aligned the shared strategy and workflow documentation with the implemented role-based model policy, then completed a final consistency pass across visible plugin docs. The last remaining frontend README drift was fixed, shared workflow structure wording was generalized to support domain-specific end gates, and deprecated/unavailable model-label discussion is now intentionally confined to `plans/model-selection-strategy.md`.

**Files:** `plans/model-selection-strategy.md`, `plugins/README.md`, `docs/Atlas_Agents_Project_Document.md`, `plugins/frontend-workflow/README.md`, `plugins/backend-workflow/README.md`, `plugins/devops-workflow/README.md`, `plugins/data-workflow/README.md`
**Functions:** shared model strategy docs, workflow pack README tables, shared workflow architecture description, project-level model selection narrative
**Implementation Scope:** rewrote model strategy guidance to match the new role-based routing; refreshed plugin README tables; updated the shared plugin index to describe domain-specific final gates instead of a universal reviewer stage; restricted deprecated/unavailable model-label explanations to the strategy plan document only; validated that no stale visible workflow model tables remain
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 0
- Edge cases: Final scoped review confirmed the only remaining deprecated/unavailable-label references are intentional explanatory notes inside `plans/model-selection-strategy.md`; environment-relative unknown-agent warnings were treated as non-blocking runtime noise

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: N/A

**Git Commit:**
refactor: sync agent docs and model strategy

- align workflow readmes with implemented role model routing
- update shared docs for domain-specific final gates
- confine compatibility caveats to strategy planning docs
