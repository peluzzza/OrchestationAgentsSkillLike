# Tasks: task-stats

**Feature slug:** `task-stats`
**Creado:** 2026-03-23
**Total tasks:** 15
**[P] markers:** tareas que deben completarse antes de que Sisyphus inicie la siguiente fase

---

## Fase 1: Implementar `stats()` en `task_service.py`

| ID | Prioridad | Descripción | Criterio de completación |
|---|---|---|---|
| T001 | [P] | Reemplazar el bloque comentado TODO de `stats()` en `task_service.py` con la firma real del método (sin implementación aún — solo descomentarlo y añadir `pass` para verificar la estructura) | `stats` aparece como método no-comentado en la clase |
| T002 | [P] | Añadir validación de `limit`: `if not (1 <= limit <= 500): raise ValueError(f"limit must be between 1 and 500, got {limit}")` | `ValueError` lanzado para `limit=0` y `limit=501` |
| T003 | [P] | Implementar filtro por `since`: `tasks = [t for t in self._tasks.values() if since is None or t.created_at >= since]` | Solo tareas con `created_at >= since` incluidas cuando `since` no es `None` |
| T004 | [P] | Aplicar `limit` al subconjunto filtrado: `tasks = tasks[:limit]` | `total` nunca supera `limit` en el retorno |
| T005 | [P] | Calcular `total`, `done`, `pending` sobre el subconjunto final | Suma `done + pending == total` siempre |
| T006 | [P] | Calcular `by_priority` con las 5 claves siempre presentes: `{p: sum(1 for t in tasks if t.priority == p) for p in range(1, 6)}` | Retorno tiene exactamente claves `{1, 2, 3, 4, 5}` |
| T007 | [P] | Calcular `by_tag`: iterar sobre `task.tags` de cada tarea, acumular en dict con `str(tag)` como clave | `by_tag == {}` cuando ninguna tarea tiene tags; claves correctas cuando las hay |
| T008 | [P] | Retornar el dict completo con las 5 claves: `total`, `done`, `pending`, `by_priority`, `by_tag` | Retorno contiene exactamente esas 5 claves |
| T009 | [P] | Añadir docstring al método con: firma, descripción de parámetros, descripción del retorno, nota sobre orden de iteración (inserción) y timezone (naive UTC) | Docstring presente y legible |

---

## Fase 2: Crear `test_task_stats.py`

| ID | Prioridad | Descripción | Criterio de completación |
|---|---|---|---|
| T010 | [P] | Crear `test_task_stats.py` con clase `TestTaskStats(unittest.TestCase)` y método `setUp` que inicializa `TaskService` limpio. Añadir helper `_add_task(days_ago, priority, done, tags)` que controla `created_at` | Archivo existe; `setUp` crea instancia fresca; helper crea tareas con `created_at` manipulado |
| T011 | [P] | Implementar tests de happy path: `test_stats_empty_store`, `test_stats_total_done_pending`, `test_stats_by_priority`, `test_stats_by_tag` | 4 tests pasan |
| T012 | [P] | Implementar tests de filtro temporal: `test_stats_since_filter` (exclusión de tareas antiguas), `test_stats_since_none` (sin filtro = todas las tareas) | 2 tests pasan; el filtro excluye correctamente |
| T013 | [P] | Implementar tests de límite: `test_stats_limit_default`, `test_stats_limit_max` (500), `test_stats_limit_min` (1), `test_stats_total_capped_by_limit` | 4 tests pasan |
| T014 | [P] | Implementar tests de ValueError: `test_stats_limit_zero_raises`, `test_stats_limit_501_raises` con `assertRaises(ValueError)` | 2 tests pasan; ValueError lanzado correctamente |
| T015 | [P] | Implementar tests de invariantes y combinaciones: `test_stats_by_priority_always_five_keys`, `test_stats_by_tag_empty`, `test_stats_since_and_limit_combined` | 3 tests pasan; invariantes verificados |

---

## Resumen de dependencias entre tasks

```
T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009
                                              ↓
                                    T010 → T011 → T012 → T013 → T014 → T015
```

- Todas las tasks de Fase 1 (T001–T009) deben completarse antes de comenzar Fase 2.
- Las tasks de Fase 2 (T010–T015) pueden implementarse secuencialmente o en grupos (T011–T015 dependen de T010).

---

## Definition of Done

- [x] T001–T009 completos: `stats()` implementado y documentado en `task_service.py`
- [x] T010–T015 completos: `test_task_stats.py` con ≥15 tests pasando
- [x] `py -m unittest -v` en `demos/full-atlas-team-demo/` — 0 errores, 0 fallos
- [x] `full_team_harness.py` — `TestSpecifyArtifacts` y `TestImplementation` en PASS
