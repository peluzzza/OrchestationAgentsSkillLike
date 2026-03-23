# Project Constitution — Full Atlas Team Demo

**Proyecto:** task-service (micro-servicio de gestión de tareas en memoria)
**Versión:** 1.0.0 → 1.1.0 (en curso)
**Fecha de constitución:** 2026-03-23
**Equipo:** Atlas full-team pipeline

---

## 1. Propósito del proyecto

Micro-servicio Python de ejemplo para la demo Full Atlas Team. Gestiona tareas en memoria con operaciones CRUD. El objetivo del ciclo actual es añadir la capacidad de estadísticas (`stats()`) con filtrado por fecha y limitación de tasa interna.

---

## 2. Stack tecnológico

| Componente | Versión actual | Notas |
|---|---|---|
| Python | ≥ 3.10 | Uso de `dataclass`, `typing`, `datetime` |
| FastAPI | 0.95.2 | Outdated — Ariadna debe auditar |
| Pydantic | 1.10.7 | EOL v1 branch — migración pendiente |
| uvicorn | 0.20.0 | Outdated |
| python-multipart | 0.0.5 | CVE conocido en versiones antiguas |
| pytest | 7.3.1 | Suite de tests — dev dep |

---

## 3. Principios de diseño

### 3.1 Pureza y separación de responsabilidades
- Los métodos de `TaskService` son puros si son de solo lectura: no deben modificar estado.
- `stats()` es **estrictamente read-only**: no crea, modifica ni elimina tareas.

### 3.2 Python stdlib only para nuevas features
- No se añaden dependencias de producción para funcionalidades que el stdlib puede cubrir.
- Las dependencias de producción sólo se justifican por requisitos HTTP/web externos al servicio de dominio.

### 3.3 Validación explícita en la frontera
- Los parámetros de entrada se validan al inicio del método, antes de cualquier lógica de negocio.
- Los errores de validación deben ser `ValueError` con mensajes descriptivos.
- Rangos válidos documentados en la firma y reforzados por código.

### 3.4 Cobertura de tests
- Toda lógica de negocio nueva requiere tests unitarios.
- Los edge cases (límite mínimo, límite máximo, parámetros opcionales None, colecciones vacías) deben estar cubiertos.
- Los tests residen en `test_task_stats.py` y siguen el patrón `unittest.TestCase`.

### 3.5 Tipos explícitos
- Las firmas de función deben tener anotaciones de tipo completas.
- Se usan `Optional[T]` o `T | None` (Python ≥ 3.10) según contexto.

---

## 4. Convenciones de código

- **Estilo:** PEP 8. Máximo 99 caracteres por línea.
- **Docstrings:** estilo Google para métodos públicos.
- **Imports:** stdlib → terceros → locales; separados por línea en blanco.
- **Dataclasses:** se prefieren sobre dicts para entidades de dominio.
- **Errores:** siempre `raise ValueError(mensaje_descriptivo)` para inputs inválidos.
- **Nombres:** snake_case para variables y métodos; PascalCase para clases.

---

## 5. Restricciones

- No persistencia en disco para el ciclo actual (in-memory store).
- No autenticación en el servicio de dominio (responsabilidad de la capa HTTP, futura).
- No concurrencia/threading en el store de esta fase — single-threaded by design.
- No dependencias externas nuevas para `stats()`.

---

## 6. Definición de Done

```
cd demos/full-atlas-team-demo
py -m unittest -v
```
**Todos los tests deben pasar sin errores ni skips inesperados.**

El harness `full_team_harness.py` verifica:
- `stats()` implementado (no `NotImplementedError`)
- `test_task_stats.py` existe con cobertura suficiente
- Pipeline Specify completo en `.specify/specs/task-stats/`

---

## 7. Directrices de calidad (QA Gate)

| Gate | Responsable | Criterio |
|---|---|---|
| SP-5 | SpecifyAnalyze | spec ↔ plan consistentes, sin bloqueantes |
| EX-1 | SpecifyAnalyze | plan ↔ tasks consistentes, listo para Sisyphus |
| Code review | Themis | Sin code smells, validación correcta |
| Security review | Atenea | Sin inyecciones, sin DoS, rate-limit correcto |
| Test coverage | Argus | ≥ 90% líneas en `stats()`, ≥ 10 casos de test |
