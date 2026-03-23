# Demo Prompt — Specify RBAC Spring Boot

Copia y pega en VS Code Copilot Chat dirigido a `@Atlas`.

---

## Opción A — Pipeline completo (planificación + implementación)

```
@Atlas Usa el pipeline Specify completo para planificar e implementar una nueva
feature en el proyecto user-management-demo.

Feature: Role-Based Access Control (RBAC)

Los usuarios deben poder tener uno o varios roles (ADMIN, USER, VIEWER).
Cada endpoint REST debe aplicar autorización basada en el rol del usuario autenticado.

Requisitos funcionales:
- RF-01: Un usuario puede tener cero o varios roles.
- RF-02: El endpoint GET /users solo es accesible para ADMIN y VIEWER.
- RF-03: El endpoint POST /users solo es accesible para ADMIN.
- RF-04: El endpoint DELETE /users/{id} solo es accesible para ADMIN.
- RF-05: Un usuario no autenticado recibe HTTP 401; uno sin permiso recibe HTTP 403.

Pila tecnológica:
- Spring Boot 3.2.2
- Spring Security
- JPA / H2 (dev) / PostgreSQL (prod)
- Arquitectura Hexagonal (domain/model, domain/port, application/service, infrastructure/adapter)
- El proyecto vive en user-management-demo/

Proceso requerido — usa Prometheus para ejecutar el pipeline Specify completo antes de escribir código:
1. SpecifyConstitution → .specify/memory/constitution.md            (crear/actualizar)
2. SpecifySpec         → .specify/specs/rbac-spring/spec.md         (feature slug: rbac-spring)
3. SpecifyClarify      → hasta 3 preguntas de clarificación si hay ambigüedad
4. SpecifyPlan         → .specify/specs/rbac-spring/plan.md + data-model.md + research.md
5. SpecifyTasks        → .specify/specs/rbac-spring/tasks.md        (formato T001..Tnnn)
6. SpecifyAnalyze (SP-5) → validación de consistencia pre-implementación
7. Sisyphus (SpecifyImplement) → implementar fase por fase siguiendo tasks.md

Además:
- Consulta .github/plugin/pack-registry.json y justifica qué pack sería relevante activar.
- La implementación debe pasar por revisión de Atenea (es cambio de seguridad crítico).
- Incluye un plan de migración de BD en el plan técnico (Hephaestus modo maintenance).
- Cuando acabe la implementación ejecuta SpecifyAnalyze (EX-1) para la puerta post-implementación.

Criterion of done:
  cd demos/specify-rbac-springboot-demo
  py -m unittest -v
Todas las clases TestSpecifyArtifacts y TestPackRegistry deben pasar.
```

---

## Opción B — Solo planificación (más rápido, sin tocar código Java)

```
@Atlas Usa Prometheus para ejecutar el pipeline Specify para una nueva feature.
No implementes código todavía.

Feature: Role-Based Access Control (RBAC) en user-management-demo/
- Roles: ADMIN, USER, VIEWER
- Autorización por endpoint: GET /users (ADMIN+VIEWER), POST /users (ADMIN), DELETE /users/{id} (ADMIN)
- Spring Boot 3.2.2 + Spring Security + arquitectura hexagonal

Ejecuta:
  SpecifyConstitution → SpecifySpec → SpecifyPlan → SpecifyTasks → SpecifyAnalyze (SP-5)

Todos los artefactos van bajo: user-management-demo/.specify/specs/rbac-spring/
Feature slug: rbac-spring

Al terminar, revisa .github/plugin/pack-registry.json y dime qué pack activarías
y por qué (backend-workflow, devops-workflow u otro).

Luego ejecuta:
  cd demos/specify-rbac-springboot-demo
  py -m unittest -v
(TestSpecifyArtifacts y TestPackRegistry deben pasar; TestImplementationSmoke será SKIP)
```

---

## Opción C — Solo Pack Registry + Hephaestus (test de features nuevos)

```
@Atlas Quiero probar dos features nuevos del ecosistema:

1. Pack Registry:
   - Lee .github/plugin/pack-registry.json
   - Lista todos los packs con shipped=true y sus estados (defaultActive, marketplacePublished)
   - Recomienda cuál activar para un proyecto Spring Boot con RBAC y necesidades de DevOps

2. Hephaestus modo Maintenance:
   - El user-management-demo necesita una migración de BD para añadir tablas ROLES y USER_ROLES
   - Hephaestus debe generar un plan de migración (Flyway/Liquibase) y validar que
     no hay breaking changes en el esquema H2 existente
   - Devuelve: Mode: maintenance, Status: COMPLETED o NEEDS_WORK

Al terminar ejecuta:
  cd demos/specify-rbac-springboot-demo
  py -m unittest -v
```
