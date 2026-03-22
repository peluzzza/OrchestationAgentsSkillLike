## Phase 2 Complete: Argus con heurísticas avanzadas opt-in
Se reforzó `Argus.agent.md` con una taxonomía más rica de edge cases y un carril explícito para técnicas avanzadas de QA cuando el riesgo lo justifique. El prompt conserva su principio de `targeted first`, mantiene el reporte compacto y ahora queda alineado con `Atlas` en los tokens de estado de testing.

**Files:** `.github/agents/Argus.agent.md`, `.github/agents/Atlas.agent.md`
**Functions:** `## Testing Workflow`, `Optional Advanced Techniques`, `## Return Format`, `<phase_complete_style_guide>`
**Implementation Scope:** Ampliados edge cases para fallos parciales, agotamiento de recursos, invariantes y corrupción de estado; añadidas técnicas avanzadas opcionales (mutation, property-based, particiones y state-transition/concurrency); corregido el contrato de handoff entre `Argus` y `Atlas` para usar `PASSED / NEEDS_MORE_TESTS / FAILED`.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 2 recomendaciones de clarificación contractual futura, no bloqueantes
- Edge cases: Confirmado que `SKIPPED` pertenece a Atlas y no contradice el formato de retorno de Argus; no se detectaron nuevas contradicciones tras alinear los tokens de estado.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: N/A

**Git Commit:**
refactor: deepen argus qa heuristics

- expand edge-case guidance for failure modes
- add opt-in advanced testing techniques
- align argus and atlas testing status tokens
