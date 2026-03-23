# Demo Prompt — Full Atlas Team Exercise

Copia y pega en Copilot Chat dirigido a `@Atlas`.
Hay 3 opciones según cuántos agentes quieras ejercitar.

---

## Opcion A — El equipo completo (todos los 19 agentes principales)

```
@Atlas Tengo un micro-servicio Python en demos/full-atlas-team-demo/ que necesita
varias cosas a la vez. Quiero que uses el equipo completo.

El proyecto: task_service.py — gestión de tareas en memoria.
pyproject.toml tiene las dependencias.

Lo que necesito:

1. FEATURE NUEVA — Implementa el método stats() que está comentado en task_service.py:
   - Acepta: since (datetime opcional), limit (int, default 100, max 500)
   - Devuelve dict con: total, done, pending, by_priority {1..5: n}, by_tag {tag: n}
   - Validación estricta de inputs (limit fuera de rango lanza ValueError)
   - Tests unitarios completos incluyendo edge cases

2. DEPENDENCIAS — Revisa pyproject.toml: hay versiones antiguas y posibles CVEs.
   Ariadna debe auditarlo y recomendar actualizaciones.

3. DOCS — El README.md de esta carpeta no documenta el método stats().
   Clio debe actualizarlo.

4. RELEASE READINESS — Al terminar, Hephaestus debe hacer un check de
   release readiness para la version v1.1.0 de este servicio.

Proceso requerido:
- Usa Prometheus + pipeline Specify completo antes de implementar
  (Constitution -> Spec -> Plan -> Tasks -> SP-5 gate -> Sisyphus -> EX-1 gate)
- Atenea debe revisar la implementacion (hay validacion de inputs y limite de tasa)
- Argus debe verificar cobertura de tests
- Clio actualiza la doc
- Ariadna audita pyproject.toml
- Hephaestus modo release-readiness al final

Feature slug: task-stats
Todos los artefactos Specify van en demos/full-atlas-team-demo/.specify/

Definition of done:
  cd demos/full-atlas-team-demo
  py -m unittest -v
Todos los tests deben pasar.
```

---

## Opcion B — Solo pipeline Specify + implementacion (mas rapido)

```
@Atlas Implementa el metodo stats() en demos/full-atlas-team-demo/task_service.py.

El metodo esta comentado en el archivo. Especificacion:
- Parametros: since: datetime = None, limit: int = 100
- limit maximo: 500 (lanza ValueError si se supera)
- Devuelve: {total, done, pending, by_priority: {1..5: n}, by_tag: {tag: n}}
- Solo cuenta tareas cuyo created_at >= since (si se proporciona)

Proceso:
1. Prometheus + Specify pipeline completo (feature slug: task-stats)
   Artefactos en: demos/full-atlas-team-demo/.specify/
2. SP-5 gate obligatorio antes de que Sisyphus empiece
3. EX-1 gate obligatorio al inicio de Sisyphus
4. Themis revisa el codigo
5. Atenea revisa (hay logica de limite/rate)
6. Argus verifica tests

Definition of done:
  cd demos/full-atlas-team-demo
  py -m unittest -v
Todos los tests pasan.
```

---

## Opcion C — Solo agentes de soporte (sin implementar codigo)

```
@Atlas Necesito tres cosas rapidas en demos/full-atlas-team-demo/, sin
implementar codigo nuevo:

1. Ariadna: audita pyproject.toml — identifica versiones desactualizadas,
   CVEs conocidos, y recomienda actualizaciones concretas.

2. Clio: el README.md de esta demo describe los agentes pero no tiene una
   seccion de "API Reference" para task_service.py. Añade una seccion
   documentando los metodos existentes (create, get, list_all, complete, delete).
   NO documentes el metodo stats() porque aun no existe.

3. Hephaestus modo maintenance: el proyecto no tiene ningun script de CI
   ni healthcheck. Genera un plan de mantenimiento minimo:
   - Que checks de CI recomendaria para este proyecto Python
   - Que healthcheck script seria apropiado
   Devuelve Mode: maintenance, Status: COMPLETED o NEEDS_WORK.

Al terminar:
  cd demos/full-atlas-team-demo
  py -m unittest -v
```

---

## Opcion D — Solo Pack Registry awareness

```
@Atlas Lee .github/plugin/pack-registry.json y dime:

1. Que packs estan shipped=true pero defaultActive=false
2. Para el proyecto demos/full-atlas-team-demo/ (Python, FastAPI, micro-servicio),
   que pack recomendarias activar y por que
3. Si activaras ese pack, que conductores adicionales tendria disponibles

No implementes nada, solo analiza y recomienda.
```
