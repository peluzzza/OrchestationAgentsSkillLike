# Flujo Esperado — Full Atlas Team Demo (Opcion A)

Traza agente por agente. Cada bloque muestra el output esperado.

---

## ATLAS — Inicio

```
Goal: Implementar stats(), auditar dependencias, actualizar docs, release readiness v1.1.0.
Constraints: Pipeline Specify completo obligatorio. Todos los gates activos.
Success: py -m unittest -v pasa; Hephaestus release-readiness READY.

Status: planning
Pack Registry: backend-workflow disponible (Python/FastAPI) — no activado (shipped, inactive).
Delegations: Prometheus para SP-0..SP-5.
```

---

## SP-0 — Prometheus: Hermes + Oracle (paralelo)

**Hermes** descubre:
- `task_service.py` — clase `TaskService`, metodo `stats()` comentado
- `pyproject.toml` — deps: fastapi 0.95.2, pydantic 1.10.7, python-multipart 0.0.5
- `README.md` — sin seccion API Reference
- Sin `.specify/` previo

**Oracle** investiga:
- Patrones Python para stats con filtros de fecha
- Riesgo de pydantic v1 (EOL branch)
- CVE en python-multipart <= 0.0.5

```
CONTEXT: task_service.py sin stats(), pyproject.toml con deps antiguas, no .specify/
FEATURE_DIR: demos/full-atlas-team-demo/.specify/specs/task-stats/
FEATURE_ID: task-stats
SECURITY_SURFACE: validacion de limit (rate-limiting interno) -> Atenea obligatoria
```

---

## SP-1 — SpecifyConstitution

Artefacto: `demos/full-atlas-team-demo/.specify/memory/constitution.md`

Principios esperados:
- P1: Input validation at boundaries — nunca confiar en llamadas internas sin validar
- P2: Test coverage >= 80% en logica de negocio
- P3: No external side effects en metodos de solo lectura
- P4: Rate/limit defaults documentados en docstring

```
CONSTITUTION_STATUS: CREATED
VERSION: 1.0.0
```

---

## SP-2 — SpecifySpec

Artefacto: `demos/full-atlas-team-demo/.specify/specs/task-stats/spec.md`

Secciones esperadas:
- Overview: metodo stats() para analisis de carga de trabajo
- User Stories: US-01 stats basicas, US-02 filtro por fecha, US-03 limite de tasa
- Acceptance Criteria GIVEN/WHEN/THEN por story
- Out of Scope: persistencia, async, API REST (para esta iteracion)

```
SPEC_STATUS: DRAFT
USER_STORIES: 3
```

---

## SP-3 — SpecifyClarify (condicional)

Preguntas esperadas:
1. ¿El parametro limit aplica al numero de tareas evaluadas o al resultado devuelto?
   (R: tareas evaluadas)
2. ¿since filtra por created_at o por updated_at?
   (R: created_at)

```
CLARIFY_STATUS: COMPLETE
ANSWERS: 2/2
```

---

## SP-4 — SpecifyPlan

Artefactos:
```
demos/full-atlas-team-demo/.specify/specs/task-stats/
├── plan.md         <- diseno + fases
├── data-model.md   <- estructura del dict de retorno
└── research.md     <- ADR: iteracion vs generadores, datetime naive vs aware
```

`plan.md` fases esperadas:
- Fase 1: Implementar stats() con logica core
- Fase 2: Tests unitarios (edge cases: lista vacia, since futuro, limit=1)
- Fase 3: Validacion de inputs (ValueError si limit > 500 o limit < 1)

---

## SP-5 — SpecifyTasks

Artefacto: `demos/full-atlas-team-demo/.specify/specs/task-stats/tasks.md`

```markdown
## US-01: Core Stats
- T001: Implement stats() basic totals (total, done, pending)    [Sisyphus]
- T002: Implement by_priority aggregation {1..5: n}             [Sisyphus]
- T003: [P] Implement by_tag aggregation {tag: n}               [Sisyphus]

## US-02: Date Filter
- T004: Apply since filter (created_at >= since)                 [Sisyphus]
- T005: [P] Handle since=None (no filter)                        [Sisyphus]

## US-03: Rate Limit
- T006: Validate limit (1..500, raises ValueError)               [Sisyphus]
- T007: Apply limit to task slice before aggregation             [Sisyphus]

## Tests
- T008: [P] Unit tests for all user stories                      [Argus]
- T009: [P] Edge case: empty store, since in future, tags=[]    [Argus]
```

---

## SP-5 GATE — SpecifyAnalyze (pre-implementacion)

```
GATE: SP-5
STATUS: PASSED
CHECKS:
  OK Todos los RF tienen user stories
  OK Todas las stories tienen tasks
  OK plan.md cubre fases 1-3
  OK Limite 500 mencionado en spec y plan
WARNINGS: 0
BLOCKERS: 0
```

---

## EX-1 GATE — SpecifyAnalyze (pre-implementacion Sisyphus)

```
GATE: EX-1
STATUS: PASSED
CHECKS:
  OK tasks.md existe con T001..T009
  OK Fases de plan.md mapeadas a tareas
  OK constitution.md sin cambios desde SP-1
BLOCKERS: 0
```

---

## EX-2..4 — Sisyphus implementa

Archivos creados/modificados:
```
demos/full-atlas-team-demo/task_service.py   (metodo stats() implementado)
demos/full-atlas-team-demo/test_task_stats.py (nuevo)
```

---

## 2B — Themis

```
Status: APPROVED
Summary: stats() correctamente implementado, validacion completa, sin efectos laterales.
```

---

## 2C — Atenea

```
Status: PASSED
Findings:
  OK limit validation lanza ValueError (no silencia el error)
  OK since acepta None sin crash
  OK No datos sensibles en el dict de retorno
  OK No side effects en metodo de solo lectura
Recommendations: considerar logging de intentos con limit > 500 en produccion.
```

---

## 2D — Argus

```
Status: PASSED
Coverage: Lines ~92%, Branches ~88%, Functions 100%
Edge cases covered:
  - Empty store returns zeros
  - since in future returns empty aggregations
  - limit=1 returns first task only
  - tags=[] task not counted in by_tag
  - All 5 priority levels tested
```

---

## 2E — Clio

Archivo modificado: `demos/full-atlas-team-demo/README.md`

Secciones anadidas:
- `## API Reference` con `stats(since, limit)` documentado
- Parametros, retorno, excepciones, y ejemplo de uso

```
Status: UPDATED
Files: README.md
Gaps: none
```

---

## 2E — Ariadna

```
Status: NEEDS_WORK
Findings:
  WARN fastapi 0.95.2 -> 0.115.x disponible (breaking changes en lifespan)
  WARN pydantic 1.10.7 -> v1 EOL, migrar a v2 recomendado
  HIGH python-multipart 0.0.5 -> CVE-2024-34621 (DoS via malformed boundary)
        Fix: actualizar a >= 0.0.9
  INFO uvicorn 0.20.0 -> 0.34.x (minor, sin breaking changes)
Recommended Actions:
  1. python-multipart >= 0.0.9 (urgente, CVE)
  2. fastapi >= 0.115.0 (planificar migracion)
  3. Evaluar pydantic v2 migration en siguiente sprint
```

---

## 2F — Hephaestus: release-readiness v1.1.0

```
Mode: release-readiness
Status: NEEDS_WORK
Blockers:
  - python-multipart CVE sin resolver (Ariadna finding HIGH)
  - Sin tests de integracion (solo unitarios)
  - pyproject.toml version no actualizada a 1.1.0
Risks:
  - pydantic v1 EOL — deuda tecnica
Recommendations:
  1. Resolver CVE python-multipart antes de release
  2. Bump version = "1.1.0" en pyproject.toml
  3. Añadir test de integracion minimo
Ready when blockers resueltos.
```

---

## ATLAS — Resumen final

```
Status: complete (con bloqueo de release)
Phase: All implementation phases complete. Release blocked by CVE.

Last Action & Changes:
  - task_service.py: stats() implementado (T001..T007)
  - test_task_stats.py: 12 tests, todos pasan
  - README.md: seccion API Reference anadida (Clio)
  - Ariadna: CVE HIGH en python-multipart detectado
  - Hephaestus: release NEEDS_WORK — CVE pendiente

Delegations: Prometheus, Hermes, Oracle, Specify x7, Sisyphus,
             Themis, Atenea, Argus, Clio, Ariadna, Hephaestus

Decision: implementacion completa y revisada. Release bloqueado hasta
          resolver CVE en python-multipart.

Next: usuario decide si parchea la dependencia ahora o pospone release.

Commit sugerido:
feat: add stats() method to TaskService

- Aggregates total/done/pending counts with optional date filter
- Supports by_priority and by_tag breakdowns
- Validates limit parameter (1-500 range)
- 12 unit tests covering edge cases
- Updated README API Reference
```
