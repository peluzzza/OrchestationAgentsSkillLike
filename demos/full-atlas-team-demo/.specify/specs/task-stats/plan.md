# Plan: Implementar `stats()` en TaskService

**Feature slug:** `task-stats`
**Creado:** 2026-03-23
**Estado:** Listo para ejecución de Atlas

---

## Resumen

Implementar el método `stats()` en `TaskService` (`task_service.py`), actualmente presente solo como bloque de comentario/TODO. El método agrega estadísticas read-only del store en memoria, filtrable por fecha (`since`) y con límite de muestra (`limit` 1–500). Se añade un archivo de tests `test_task_stats.py` con cobertura completa de edge cases.

---

## Contexto y Análisis

**Ficheros relevantes:**

- `task_service.py`: Contiene `Task` (dataclass) y `TaskService` (in-memory store). El método `stats()` existe como comentario en el bloque `# TODO`. Se modificará para insertar la implementación real.
- `pyproject.toml`: Define las dependencias del proyecto. No requiere cambios para `stats()` (stdlib only). Ariadna lo auditará por separado.
- `test_task_stats.py` *(nuevo)*: Archivo de tests unitarios para `stats()`. Se creará desde cero.

**Funciones/Clases clave:**

- `Task` en `task_service.py`: Dataclass con campos `id`, `title`, `priority`, `done`, `created_at`, `tags`. `stats()` leerá todos estos campos.
- `TaskService._tasks` en `task_service.py`: `dict[int, Task]` — fuente de datos para `stats()`.
- `TaskService.stats()` en `task_service.py`: Método a implementar. Firma: `def stats(self, since: datetime = None, limit: int = 100) -> dict`.

**Dependencias:**

- `datetime` (stdlib): Ya importado en `task_service.py`. Usado para tipado de `since` y comparación con `task.created_at`.
- `collections` (stdlib): No necesario — el conteo por prioridad y tag se puede hacer con comprensiones de dict nativas.
- `unittest` (stdlib): Framework de tests ya usado en el proyecto.

**Patrones y convenciones:**

- Validación al inicio del método con `raise ValueError(mensaje)` — patrón ya establecido en `create()`.
- Uso de `dataclass` con `field(default_factory=...)` para valores mutables por defecto — `tags` ya usa este patrón.
- Tests en archivos `test_*.py` a nivel del directorio del demo — `test_full_team_harness.py` es el ejemplo.
- `py -m unittest -v` como comando de ejecución de tests.

---

## Fases de implementación

### Fase 1: Implementar `stats()` en `task_service.py`

**Objetivo:** Reemplazar el bloque de comentario TODO con una implementación funcional y validada del método `stats()`.

**Ficheros a modificar:**

- `task_service.py`: Reemplazar el bloque comentado `# def stats(...)` con la implementación real.

**Foco de QA:**

- Argus verificará: validación de `limit`, correcta aplicación del filtro `since`, retorno siempre con estructura completa (`by_priority` con 5 claves, `by_tag` como dict, nunca `None`).
- Atenea verificará: que `limit` previene DoS (no se itera sobre un conjunto ilimitado), que `since` no abre vectores de inyección (es comparación directa de tipos, sin eval ni SQL).

**Pasos:**

1. Localizar el bloque TODO comentado en `task_service.py` (líneas ~70-80).
2. Reemplazar el bloque comentado con la implementación:
   - Validar `limit`: `if not (1 <= limit <= 500): raise ValueError(...)`.
   - Filtrar por `since`: `tasks = [t for t in self._tasks.values() if since is None or t.created_at >= since]`.
   - Aplicar `limit`: `tasks = tasks[:limit]`.
   - Calcular `total`, `done`, `pending`.
   - Calcular `by_priority`: comprensión sobre rangos 1–5.
   - Calcular `by_tag`: iterar sobre `task.tags`, acumulando en dict.
   - Retornar el dict completo.
3. Verificar que el import de `datetime` ya está presente (sí lo está, línea 2).
4. Revisar que no se modifica ninguna variable de instancia (`self._tasks`, `self._next_id`).

**Criterios de aceptación:**

- [ ] Método `stats()` sin `NotImplementedError`.
- [ ] `ValueError` lanzado para `limit=0` y `limit=501`.
- [ ] `by_priority` siempre contiene exactamente las claves `{1, 2, 3, 4, 5}`.
- [ ] `by_tag` es `{}` cuando ninguna tarea tiene tags.
- [ ] El store no se modifica tras llamar a `stats()`.

---

### Fase 2: Crear `test_task_stats.py`

**Objetivo:** Crear suite completa de tests unitarios para `stats()` con cobertura de happy path, edge cases y casos de error.

**Ficheros a crear:**

- `test_task_stats.py`: Suite `unittest.TestCase` con ≥15 métodos de test.

**Foco de QA:**

- Argus verificará: ≥ 90% de cobertura de líneas en `stats()`, presencia de tests de `ValueError`, tests de filtro `since`, tests de `by_tag` y `by_priority`.
- Themis verificará: claridad de nombres de test, ausencia de lógica duplicada, uso correcto de `setUp`.

**Pasos:**

1. Crear `test_task_stats.py` con clase `TestTaskStats(unittest.TestCase)`.
2. Implementar `setUp` que crea una instancia de `TaskService` limpia.
3. Añadir método auxiliar `_make_task(days_ago, priority, done, tags)` que crea tareas con `created_at` controlado.
4. Implementar los 15 casos de test definidos en la spec.
5. Añadir guardia `if __name__ == "__main__": unittest.main()`.
6. Verificar con `py -m unittest test_task_stats -v` que todos los tests pasan.

**Criterios de aceptación:**

- [ ] Archivo `test_task_stats.py` existe en `demos/full-atlas-team-demo/`.
- [ ] Todos los tests pasan (`py -m unittest -v`).
- [ ] Al menos 15 métodos de test presentes.
- [ ] Tests de `ValueError` para `limit=0` y `limit=501` presentes.
- [ ] Test de filtro `since` presente y correcto.
- [ ] Test de combinación `since` + `limit` presente.

---

### Fase 3: Verificación de integración (harness check)

**Objetivo:** Confirmar que el harness `full_team_harness.py` registra PASS en las suites `TestSpecifyArtifacts` e `TestImplementation`.

**Ficheros a revisar (sin modificar):**

- `full_team_harness.py`: Verificar que `check_specify_artifacts()` y `check_implementation()` pasan con los artefactos generados.
- `test_full_team_harness.py`: Ejecutar la suite completa y confirmar que `TestSpecifyArtifacts` y `TestImplementation` ya no son SKIP.

**Foco de QA:**

- Argus verifica que el harness reconoce `spec.md`, `plan.md`, `tasks.md` en `.specify/specs/task-stats/`.
- Argus verifica que `stats()` supera el check de `NotImplementedError`.

**Pasos:**

1. Confirmar que `.specify/specs/task-stats/` contiene `spec.md`, `plan.md`, `tasks.md`.
2. Ejecutar `py -m unittest -v` y confirmar que `TestSpecifyArtifacts` pasa.
3. Ejecutar `py -m unittest -v` y confirmar que `TestImplementation` pasa.
4. Registrar resultado en `analysis-report.md`.

**Criterios de aceptación:**

- [ ] `TestSpecifyArtifacts` PASS (no SKIP, no FAIL).
- [ ] `TestImplementation` PASS.
- [ ] `TestTaskStats` PASS (todos los tests individuales).
- [ ] Salida de `py -m unittest -v` sin errores.

---

## Preguntas abiertas

1. **¿El orden de iteración en `self._tasks.values()` es determinístico para `limit`?**
   - **Opción A:** Iterar en orden de inserción (dict preserva inserción en Python ≥ 3.7) — resultado determinístico por `task_id`.
   - **Opción B:** Ordenar explícitamente por `created_at` antes de aplicar `limit`.
   - **Recomendación:** Opción A — el dict de Python ≥ 3.7 garantiza orden de inserción, que coincide con el orden de creación. Documentarlo en el docstring.

2. **¿Debe `since` compararse en UTC o en hora local?**
   - **Opción A:** Comparación directa sin conversión (usuario responsable de proveer mismo timezone).
   - **Opción B:** Normalizar a UTC con `datetime.utcnow()` para consistencia.
   - **Recomendación:** Opción A conservadora — `Task.created_at` usa `datetime.utcnow()` y si el caller pasa `since` en UTC todo funciona. Documentar en docstring que `since` debe estar en UTC.

---

## Riesgos y mitigación

- **Riesgo:** `task.tags` podría contener valores no-string (p.ej. `None`, `int`).
  - **Mitigación:** Iterar solo sobre `str(tag)` o filtrar con `isinstance(tag, str)`. Usar `str(tag)` para robustez.
- **Riesgo:** `limit` con tipo incorrecto (float, string) podría pasar la guarda.
  - **Mitigación:** La guarda `1 <= limit <= 500` con tipo `int` anotado es suficiente. Python no hace cast implícito desde el caller.
- **Riesgo:** Store muy grande puede ser lento si `limit=500` pero hay 100k tareas.
  - **Mitigación:** Aceptado — el store es in-memory y esta fase no requiere optimización de performance. El `limit` ya actúa como protección.

---

## Criterios de éxito globales

- [ ] `stats()` implementado y funcional en `task_service.py`.
- [ ] `test_task_stats.py` creado con ≥ 15 tests, todos pasando.
- [ ] Pipeline Specify completo: `spec.md`, `plan.md`, `tasks.md`, `analysis-report.md` en `.specify/specs/task-stats/`.
- [ ] `py -m unittest -v` en `demos/full-atlas-team-demo/` — todos los tests pasan.
- [ ] `full_team_harness.py` — `TestSpecifyArtifacts` y `TestImplementation` en PASS.

---

## Notas para Atlas

- **Dependencias entre fases:** La Fase 2 depende de que la Fase 1 esté completa (los tests importan `TaskService.stats()`). La Fase 3 depende de que las fases 1 y 2 estén completas.
- **No modificar:** `pyproject.toml` para esta feature — es territorio de Ariadna. `stats()` es stdlib only.
- **Skills recomendados para Sisyphus:** `python-dev`, `python-testing-patterns`.
- **Rollback:** Si `stats()` introduce regresiones en tests existentes, revertir a la versión comentada y depurar. Los tests de CRUD existentes en `test_full_team_harness.py` deben seguir pasando.
- **Gate EX-1:** Sisyphus debe leer `tasks.md` y confirmar que todos los tasks T001–T015 tienen especificación completa antes de iniciar la implementación.
