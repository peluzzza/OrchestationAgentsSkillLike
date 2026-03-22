## Phase 3 Complete: Hephaestus con valor navaja suiza, pero con guardarraíl
Se amplió `Hephaestus.agent.md` con modos operativos explícitos para deploy, release-readiness, incident response, maintenance y performance/capacity, manteniendo límites de rol claros y un contrato estructurado consumible por `Atlas`. Además, `Atlas.agent.md` ahora enruta y resuelve de forma determinista los resultados no-deploy de `Hephaestus`, cerrando la brecha detectada por review y QA.

**Files:** `.github/agents/Hephaestus.agent.md`, `.github/agents/Atlas.agent.md`
**Functions:** `## Engagement Modes`, `## Release Readiness`, `## Deploy / Rollout Workflow`, `## Return Format & Capacity`, `#### 2F. Deploy (conditional)`, `**Hephaestus**` delegation brief, `<phase_complete_style_guide>`
**Implementation Scope:** Añadido frame de entrada por modo; enriquecida la cobertura operativa de incident/maintenance/performance/capacity; reforzado el patrón de acción segura y reversible; introducido contrato obligatorio `Mode:` + `Status:`; añadidos tokens de estado para fallos duros fuera de deploy; alineado Atlas con reglas explícitas de routing para modos no-deploy y con campos de artefacto de cierre compatibles.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Additional tests: 2 seguimientos no bloqueantes recomendados para endurecer exclusión mutua en artefactos y evitar que maintenance emita etiquetas de performance en el cuerpo.
- Edge cases: Resueltas las ambigüedades sobre `NEEDS_WORK`, `INVESTIGATING`, `BLOCKED` y fallos duros de maintenance/performance; queda riesgo bajo de drift terminológico menor entre labels de ayuda y tokens de retorno.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Git Commit:**
refactor: strengthen hephaestus ops contract

- add explicit non-deploy operations modes and status tokens
- align atlas routing with hephaestus mode outcomes
- preserve strict ops-only role boundaries
