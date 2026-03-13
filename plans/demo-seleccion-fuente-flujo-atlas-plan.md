# Plan: Demo de seleccion de fuente de flujo para Atlas

**Created:** 2026-03-12
**Status:** Ready for Atlas Execution

## Summary

Este plan crea un demo nuevo y autocontenido para demostrar que Atlas puede elegir la mejor fuente de flujo entre multiples fuentes. El demo usa Python stdlib, un motor de seleccion determinista basado en metadatos de fuentes, y pruebas unitarias que validan precedencia, compatibilidad, fallback y desempate. Se agregan README y DEMO_PROMPT para ejecutar un bucle de orquestacion. El alcance es pequeno pero realista, alineado con el estilo del demo existente.

## Context & Analysis

**Relevant Files:**
- demos/subagents-smoke-demo/README.md: patron para README del demo y pasos de ejecucion.
- demos/subagents-smoke-demo/DEMO_PROMPT.md: patron para el prompt de orquestacion.
- demos/subagents-smoke-demo/test_calc.py: estilo de tests con unittest y sys.path.
- .github/agents/: fuente de mayor precedencia para agentes/flujo.
- plugins/*/agents/: fuentes alternativas de flujo.

**Key Functions/Classes:**
- select_source(...) in demos/<nuevo-demo>/selection_engine.py: seleccion determinista y racional.
- SourceMetadata in demos/<nuevo-demo>/selection_engine.py: metadatos de cada fuente.
- TaskProfile in demos/<nuevo-demo>/selection_engine.py: perfil de tarea.
- SelectionResult in demos/<nuevo-demo>/selection_engine.py: resultado con fuente y razon.

**Dependencies:**
- Python stdlib: dataclasses, typing, unittest, pathlib.

**Patterns & Conventions:**
- Unittest con ejecucion via `python -m unittest -v`.
- Demo autocontenido en demos/<nuevo-demo>/ sin dependencias externas.
- README + DEMO_PROMPT similares al smoke demo.

## Implementation Phases

### Phase 1: Estructura del demo y motor base

**Objective:** Crear el esqueleto del demo y un motor de seleccion determinista con desempate estable.

**Files to Modify/Create:**
- demos/atlas-source-selection-demo/selection_engine.py: modelos (dataclasses) y logica base de seleccion con desempate.
- demos/atlas-source-selection-demo/fixtures.py: catalogo minimo de fuentes y perfiles de tareas.
- demos/atlas-source-selection-demo/test_selection_engine.py: pruebas para desempate determinista.
- demos/atlas-source-selection-demo/README.md: stub con como correr tests.
- demos/atlas-source-selection-demo/DEMO_PROMPT.md: stub del loop de orquestacion.

**Tests to Write:**
- test_deterministic_tie_break: mismo score, distinta clave, seleccion estable.

**Steps:**
1. Escribir test de desempate determinista.
2. Ejecutar tests (fallan).
3. Implementar dataclasses y select_source con ordenamiento estable (p. ej., por origin_priority, score, priority, name).
4. Ejecutar tests (pasan).
5. Limpieza basica (nombres claros, typing).

**Acceptance Criteria:**
- [ ] Existe un demo nuevo en demos/atlas-source-selection-demo.
- [ ] `select_source` retorna la misma fuente para entradas identicas.
- [ ] Test de desempate pasa.

---

### Phase 2: Compatibilidad por tipo de tarea y capacidades

**Objective:** Agregar matching por tipo de tarea y capacidades requeridas.

**Files to Modify/Create:**
- demos/atlas-source-selection-demo/selection_engine.py: scoring por task_type y capabilities.
- demos/atlas-source-selection-demo/fixtures.py: fuentes con task_types y capabilities.
- demos/atlas-source-selection-demo/test_selection_engine.py: test de compatibilidad.

**Tests to Write:**
- test_capability_matching_by_task_type: selecciona fuente con capacidades correctas.

**Steps:**
1. Escribir test de matching por task_type/capabilities.
2. Ejecutar tests (fallan).
3. Implementar logica de matching y scoring.
4. Ejecutar tests (pasan).
5. Refactor menor si es necesario.

**Acceptance Criteria:**
- [ ] Seleccion por tipo de tarea funciona.
- [ ] Test de compatibilidad pasa.

---

### Phase 3: Precedencia de .github sobre plugins en duplicados

**Objective:** Validar que una fuente de .github tiene precedencia sobre plugins cuando hay duplicados.

**Files to Modify/Create:**
- demos/atlas-source-selection-demo/selection_engine.py: prioridad por origen (github > plugin > other).
- demos/atlas-source-selection-demo/fixtures.py: duplicado con mismos capabilities y task_type.
- demos/atlas-source-selection-demo/test_selection_engine.py: test de precedencia.

**Tests to Write:**
- test_github_precedence_on_duplicate_source: elige .github cuando el duplicado existe.

**Steps:**
1. Escribir test de precedencia.
2. Ejecutar tests (fallan).
3. Implementar priority por origen en el ranking.
4. Ejecutar tests (pasan).
5. Ajustar razon/rationale para explicar precedencia.

**Acceptance Criteria:**
- [ ] El origen .github gana en duplicados equivalentes.
- [ ] Test de precedencia pasa.

---

### Phase 4: Fallback y documentacion del demo

**Objective:** Agregar fallback cuando la fuente preferida no esta disponible y finalizar README/DEMO_PROMPT.

**Files to Modify/Create:**
- demos/atlas-source-selection-demo/selection_engine.py: soporte de preferred_source y availability.
- demos/atlas-source-selection-demo/fixtures.py: fuentes con unavailable y preferred.
- demos/atlas-source-selection-demo/test_selection_engine.py: test de fallback.
- demos/atlas-source-selection-demo/README.md: pasos completos para ejecutar tests.
- demos/atlas-source-selection-demo/DEMO_PROMPT.md: prompt para Atlas con loop de orquestacion.

**Tests to Write:**
- test_fallback_when_preferred_unavailable: elige la siguiente mejor opcion.

**Steps:**
1. Escribir test de fallback.
2. Ejecutar tests (fallan).
3. Implementar la logica de fallback y rationale.
4. Ejecutar tests (pasan).
5. Completar README y DEMO_PROMPT.

**Acceptance Criteria:**
- [ ] Fallback funciona cuando preferred_source no esta disponible.
- [ ] README y DEMO_PROMPT explican la ejecucion del demo.
- [ ] Todos los tests pasan con `python -m unittest -v`.

## Open Questions

1. La seleccion debe leer fuentes reales desde .github/agents y plugins/*/agents o usar fixtures locales?
   - **Option A:** Fixtures locales (autocontenido, estable, rapido).
   - **Option B:** Lectura real del repo (mas realista, pero acopla a estructura).
   - **Recommendation:** Option A para mantener el demo pequeno y determinista.

2. El criterio de prioridad por origen debe ser configurable?
   - **Option A:** Hardcoded (github > plugin > other) para el demo.
   - **Option B:** Configurable via tabla de prioridades en fixtures.
   - **Recommendation:** Option B si se quiere variar escenarios sin tocar el motor.

## Risks & Mitigation

- **Risk:** Ambiguedad sobre que significa "flow source" en el repo.
  - **Mitigation:** Definir metadatos explicitos en fixtures y documentarlos en README.
- **Risk:** Tests acoplados a estructura real del repo.
  - **Mitigation:** Usar fixtures locales y solo simular origen.
- **Risk:** Rationale poco claro para el usuario.
  - **Mitigation:** Devolver lista de razones ordenadas en SelectionResult.

## Success Criteria

- [ ] Demo nuevo en demos/atlas-source-selection-demo, autocontenido.
- [ ] Motor determinista selecciona fuente y explica rationale.
- [ ] Tests cubren precedencia, matching, fallback y desempate.
- [ ] README y DEMO_PROMPT listos para orquestacion.
- [ ] Todas las pruebas pasan.

## Notes for Atlas

- Mantener el demo pequeno y sin dependencias externas.
- Seguir el estilo de unittest del smoke demo.
- Mantener nombres ASCII y paths consistentes.
