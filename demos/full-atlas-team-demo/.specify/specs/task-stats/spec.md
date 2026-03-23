# Feature Spec: task-stats

**Feature slug:** `task-stats`
**Creado:** 2026-03-23
**Estado:** READY_FOR_PLANNING: true
**READY_FOR_PLANNING:** true

---

## 1. Descripción funcional

Implementar el método `stats()` en la clase `TaskService` del archivo `task_service.py`. El método existe actualmente como bloque de comentario/TODO y debe pasar a ser código funcional.

El método agrega estadísticas de lectura sobre el conjunto de tareas en memoria, con soporte de filtrado temporal y limitación de la muestra.

---

## 2. Firma del método

```python
def stats(self, since: datetime = None, limit: int = 100) -> dict:
```

### Parámetros

| Parámetro | Tipo | Default | Descripción |
|---|---|---|---|
| `since` | `datetime \| None` | `None` | Filtro temporal. Si se proporciona, solo se consideran tareas donde `task.created_at >= since`. Si es `None`, se consideran todas las tareas. |
| `limit` | `int` | `100` | Número máximo de tareas a agregar. Rango válido: **1–500**. Si está fuera del rango, se lanza `ValueError`. |

### Retorno

```python
{
    "total":       int,           # n.º de tareas consideradas (tras aplicar since y limit)
    "done":        int,           # tareas con done=True dentro del conjunto considerado
    "pending":     int,           # tareas con done=False dentro del conjunto considerado
    "by_priority": {              # siempre incluye claves 1..5, valor 0 si no hay tareas
        1: int,
        2: int,
        3: int,
        4: int,
        5: int,
    },
    "by_tag":      dict[str, int] # {tag: n.º de tareas que contienen ese tag}
}
```

---

## 3. Comportamiento detallado

### 3.1 Orden de aplicación de filtros

1. Se toma la lista completa de tareas del store (`self._tasks.values()`).
2. Si `since` no es `None`, se filtra: `task.created_at >= since`.
3. Se toman los primeros `limit` elementos del conjunto filtrado resultante.
4. Se calculan las estadísticas sobre ese subconjunto final.

> **Decisión de diseño (SP-3 clarify):**
> `limit` acota el subconjunto *después* del filtro `since`, no antes.
> Esto garantiza consistencia: `total` nunca supera `limit`.
> <!-- default: limit postcede a since — asumida conservadoramente -->

### 3.2 Validación de `limit`

```python
if not (1 <= limit <= 500):
    raise ValueError(f"limit must be between 1 and 500, got {limit}")
```

La validación ocurre **antes** de cualquier acceso al store.

### 3.3 `by_priority` siempre completo

Las cinco claves `1..5` **siempre** están presentes en el retorno, aunque su valor sea `0`.

> **Decisión de diseño (SP-3 clarify):**
> Incluir siempre las 5 claves evita que el consumidor tenga que manejar `KeyError` y simplifica la serialización JSON.
> <!-- default: siempre incluir 1..5 con value=0 — asumida conservadoramente -->

### 3.4 `by_tag` cuando no hay tags

Si ninguna tarea (dentro del subconjunto) tiene tags, `by_tag` retorna `{}` (dict vacío).

> **Decisión de diseño (SP-3 clarify):**
> Se retorna `{}` en lugar de `None` para mantener consistencia de tipo en el retorno.
> <!-- default: {} vacío, nunca None — asumida conservadoramente -->

### 3.5 Store vacío / filtro que no matchea ninguna tarea

Si el subconjunto resultante está vacío:
```python
{"total": 0, "done": 0, "pending": 0, "by_priority": {1:0,2:0,3:0,4:0,5:0}, "by_tag": {}}
```

### 3.6 Sin efectos secundarios

El método es estrictamente **read-only**. No modifica `self._tasks` ni ningún otro estado.

---

## 4. Restricciones técnicas

- **Solo stdlib Python** — no se añaden dependencias nuevas.
- **Sin I/O** — no logs, no ficheros, no red.
- **Compatibilidad Python ≥ 3.10** — puede usarse `list[Task]` y `dict[str, int]` como anotaciones.

---

## 5. Tests requeridos

Un archivo `test_task_stats.py` en `demos/full-atlas-team-demo/` con los siguientes casos:

| ID test | Descripción |
|---|---|
| `test_stats_empty_store` | Store vacío → zeros en todas las claves |
| `test_stats_total_done_pending` | Mix de tareas done/pending → valores correctos |
| `test_stats_by_priority` | Tareas de distintas prioridades → by_priority correcto |
| `test_stats_by_tag` | Tareas con tags → by_tag correcto |
| `test_stats_since_filter` | Filtro `since` excluye tareas antiguas |
| `test_stats_since_none` | `since=None` considera todas las tareas |
| `test_stats_limit_default` | Default `limit=100` funciona |
| `test_stats_limit_max` | `limit=500` es aceptado |
| `test_stats_limit_min` | `limit=1` es aceptado |
| `test_stats_limit_zero_raises` | `limit=0` lanza `ValueError` |
| `test_stats_limit_501_raises` | `limit=501` lanza `ValueError` |
| `test_stats_by_priority_always_five_keys` | Retorno siempre tiene 5 claves de prioridad |
| `test_stats_by_tag_empty` | Sin tags → by_tag == {} |
| `test_stats_total_capped_by_limit` | limit=1 → total=1 aunque hay más tareas |
| `test_stats_since_and_limit_combined` | Combinación de since + limit |

---

## 6. Criterios de aceptación

- [ ] `stats()` implementado (no raises `NotImplementedError`, no es stub).
- [ ] `ValueError` lanzado para `limit` fuera de `[1, 500]`.
- [ ] Retorno siempre contiene exactamente las claves: `total`, `done`, `pending`, `by_priority`, `by_tag`.
- [ ] `by_priority` siempre contiene claves `1`, `2`, `3`, `4`, `5`.
- [ ] `stats()` no modifica ningún estado del store.
- [ ] Todos los tests en `test_task_stats.py` pasan con `py -m unittest -v`.
- [ ] `full_team_harness.py` — suites `TestSpecifyArtifacts` e `TestImplementation` PASS.
