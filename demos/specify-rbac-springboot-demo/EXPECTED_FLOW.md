# Flujo Esperado — Specify RBAC Spring Boot Demo

Traza detallada de lo que cada agente debe hacer cuando se ejecuta la Opción A.

---

## ATLAS — Inicialización

**Atlas** parsea la solicitud e identifica: planificación + implementación + seguridad + infra.

Output esperado:
```
Goal: RBAC para user-management-demo usando pipeline Specify completo.
Constraints: Spring Boot 3.2.2, arquitectura hexagonal, Atenea obligatoria, Hephaestus maintenance.
Success: py -m unittest -v pasa todas las clases TestSpecifyArtifacts y TestPackRegistry.

Status: planning
Phase: SP-0 — Context Discovery
Delegations: Routing a Prometheus para pipeline SP-0..SP-5 + implementación.
```

---

## SP-0 — Prometheus → Hermes + Oracle (paralelo)

**Hermes** escanea el workspace:
- `user-management-demo/src/main/java/com/accenture/usermgmt/domain/` → encuentra `model/` y `port/`
- `user-management-demo/src/main/java/com/accenture/usermgmt/application/service/` → servicios existentes
- `user-management-demo/src/main/java/com/accenture/usermgmt/infrastructure/` → adaptadores
- `.github/plugin/pack-registry.json` → detecta `backend-workflow` como relevante
- No hay `.specify/` todavía → pipeline arranca desde cero

**Oracle** investiga:
- Patrones de Spring Security para RBAC con arquitectura hexagonal
- Estrategia de permisos: `hasRole()` vs `@PreAuthorize` vs port de autorización en dominio
- Opciones de migración: Flyway vs Liquibase para H2 (dev) / PostgreSQL (prod)

Output esperado de Prometheus:
```
CONTEXT: hexagonal Spring Boot, no .specify/ previo, pack backend-workflow identificado
TECH_STACK: Java 17, Spring Boot 3.2.2, Spring Security, JPA/H2
SECURITY_PATTERN: @PreAuthorize con roles en capa application/service
MIGRATION_TOOL: Flyway (compatible con H2 y PostgreSQL)
FEATURE_DIR: user-management-demo/.specify/specs/rbac-spring/
FEATURE_ID: rbac-spring
```

---

## SP-1 — Prometheus → SpecifyConstitution

Crea o actualiza `.specify/memory/constitution.md`.

Principios esperados (adaptados a contexto Java/Spring):
- **P1:** Arquitectura Hexagonal — el dominio no depende de frameworks
- **P2:** Seguridad por defecto — denegar acceso si no hay rol explícito
- **P3:** Cobertura de tests ≥ 80% en capa de aplicación
- **P4:** Compatibilidad de BD — migraciones reversibles siempre

Artefacto esperado:
```
user-management-demo/.specify/memory/constitution.md  (nuevo)
CONSTITUTION_STATUS: CREATED
VERSION: 1.0.0
PRINCIPLES: 4
```

---

## SP-2 — Prometheus → SpecifySpec

Genera `.specify/specs/rbac-spring/spec.md`.

Secciones esperadas:
- **Overview** — propósito del RBAC, actores (Admin, User, Viewer)
- **User Stories** (US-01..US-05) mapeadas a RF-01..RF-05
- **Acceptance Criteria** — formato `GIVEN/WHEN/THEN` por user story
- **Out of Scope** — SSO, OAuth2, multi-tenant (explícitos)
- **Open Questions** — máximo 3 antes de SpecifyClarify

Artefacto esperado:
```
user-management-demo/.specify/specs/rbac-spring/spec.md  (nuevo)
SPEC_STATUS: DRAFT
USER_STORIES: 5
OPEN_QUESTIONS: ≤ 3
```

---

## SP-3 — Prometheus → SpecifyClarify (condicional)

Solo si hay preguntas abiertas en spec.md. Máximo 3 preguntas.

Preguntas típicas esperadas:
1. ¿Los roles son globales o por recurso? (R: globales para esta iteración)
2. ¿Se requiere persistencia de roles en BD o son estáticos? (R: persistencia JPA)
3. ¿H2 en tests — ¿en memoria o fichero? (R: en memoria)

Output esperado:
```
CLARIFY_STATUS: COMPLETE
ANSWERS_ENCODED: 3/3
SPEC_UPDATED: true
```

---

## SP-4 — Prometheus → SpecifyPlan

Genera artefactos de diseño técnico.

Archivos esperados:
```
user-management-demo/.specify/specs/rbac-spring/
├── plan.md          ← diseño técnico + fases + mapa hexa
├── data-model.md    ← entidades Role, UserRole; esquema SQL; diagrama ER textual
├── research.md      ← ADRs: Spring Security vs filtros manuales, Flyway vs Liquibase
└── contracts/
    └── security-port.md  ← puerto de dominio IAuthorizationPort
```

`plan.md` debe incluir:
- **Fase 1** — Dominio: entidad `Role`, enum `Permission`, puerto `IAuthorizationPort`
- **Fase 2** — Aplicación: `RoleService`, decoración de `UserService` con chequeo de permisos
- **Fase 3** — Infraestructura: `SecurityConfig`, `JwtAuthFilter`, `RoleRepository`
- **Fase 4** — Migración BD: scripts Flyway `V2__add_roles.sql` + `V3__add_user_roles.sql`
- **Fase 5** — Tests: integración con `@WithMockUser`, unitarios de `RoleService`

`plan.md` debe mencionar:
- **Pack Registry**: recomienda activar `backend-workflow` (conductor `Backend-Atlas`)
- **Hephaestus maintenance**: Fase 4 requiere invocación explícita

---

## SP-5 — Prometheus → SpecifyTasks

Genera `tasks.md` en formato `T001..Tnnn`.

Estructura esperada:
```markdown
## US-01: Role Entity
- T001: Create Role enum (ADMIN, USER, VIEWER) in domain/model/       [Sisyphus]
- T002: Create Role JPA entity in infrastructure/persistence/          [Sisyphus]
- T003: [P] Create IAuthorizationPort in domain/port/                  [Sisyphus]
- T004: [P] Create IRoleRepository in domain/port/                     [Sisyphus]

## US-02: Service Layer Authorization
- T005: Implement RoleService in application/service/                  [Sisyphus]
- T006: Decorate UserService.getAll() with ADMIN+VIEWER check          [Sisyphus]
- T007: Decorate UserService.create() with ADMIN-only check            [Sisyphus]

## US-03: Spring Security Config
- T008: Add SecurityConfig (permitAll vs authenticated rules)          [Sisyphus]
- T009: [P] Add JwtAuthFilter skeleton                                 [Sisyphus]
- T010: [P] Wire RoleRepository adapter                                [Sisyphus]

## US-04: Database Migration
- T011: Flyway V2__add_roles.sql                                       [Hephaestus]
- T012: Flyway V3__add_user_roles.sql                                  [Hephaestus]

## US-05: Tests
- T013: [P] Unit tests for RoleService                                 [Argus]
- T014: [P] Integration tests with @WithMockUser                       [Argus]
```

Marcadores `[P]` indican tareas paralelizables.

---

## SP-5 GATE — SpecifyAnalyze (pre-implementación)

Primera puerta de consistencia: valida que spec + plan + tasks están alineados.

Output esperado:
```
GATE: SP-5
STATUS: PASSED
CHECKS:
  ✅ Todos los RF tienen user stories en spec.md
  ✅ Todas las user stories tienen tasks en tasks.md
  ✅ plan.md cubre todas las fases definidas
  ✅ data-model.md tiene entidades para T001, T002
  ✅ IAuthorizationPort en contracts/ referenciado en T003
  ✅ Flyway en plan.md alineado con T011, T012
WARNINGS: 0
BLOCKERS: 0
```

Si hay bloqueadores → Prometheus los resuelve antes de delegar a Sisyphus.

---

## EX-1..EX-4 — Sisyphus implementa fase por fase

### EX-1 — Sisyphus implementa Fase 1 (Dominio)

Archivos creados/modificados esperados:
```
user-management-demo/src/main/java/com/accenture/usermgmt/domain/model/Permission.java   (nuevo)
user-management-demo/src/main/java/com/accenture/usermgmt/domain/model/Role.java         (nuevo)
user-management-demo/src/main/java/com/accenture/usermgmt/domain/port/IAuthorizationPort.java (nuevo)
user-management-demo/src/main/java/com/accenture/usermgmt/domain/port/IRoleRepository.java    (nuevo)
```

**Themis → APPROVED** (clases de dominio sin dependencias de framework)

**Atenea → PASSED** ← *agente nuevo en este flujo*  
Revisión específica esperada:
```
SECURITY: IAuthorizationPort no expone detalles de implementación de Spring Security al dominio ✅
SECURITY: Permission enum no usa strings libres (evita privilege escalation) ✅
SECURITY: Role entity no serializa permisos sensibles en JSON por defecto ✅
```

---

### EX-2 — Sisyphus implementa Fase 2 (Aplicación)

Archivos modificados esperados:
```
user-management-demo/src/main/java/com/accenture/usermgmt/application/service/RoleService.java  (nuevo)
user-management-demo/src/main/java/com/accenture/usermgmt/application/service/UserService.java  (modificado)
```

**Atenea → PASSED**  
- Verifica que UserService lanza `AccessDeniedException` estándar de Spring (no expone internals)

**Argus:** crea tests unitarios para `RoleService`

---

### EX-3 — Sisyphus implementa Fase 3 (Infraestructura)

Archivos esperados:
```
user-management-demo/src/main/java/com/accenture/usermgmt/infrastructure/config/SecurityConfig.java  (nuevo)
user-management-demo/src/main/java/com/accenture/usermgmt/infrastructure/adapter/RoleRepositoryAdapter.java (nuevo)
```

**Atenea → PASSED**  
- SecurityConfig no usa `permitAll()` en endpoints protegidos  
- No hay credenciales hardcodeadas

---

### EX-4 — Hephaestus modo Maintenance (Migración BD)

*Feature nuevo: Hephaestus con modo Maintenance*

Archivos esperados:
```
user-management-demo/src/main/resources/db/migration/V2__add_roles.sql       (nuevo)
user-management-demo/src/main/resources/db/migration/V3__add_user_roles.sql  (nuevo)
```

Output esperado de Hephaestus:
```
Mode: maintenance
Status: COMPLETED
Env: H2 (in-memory dev) + PostgreSQL (prod hint)
Health:
  ✅ V2__add_roles.sql — sintaxis válida, no elimina tablas existentes
  ✅ V3__add_user_roles.sql — FK referencia user.id y role.id correctamente
  ✅ Migraciones reversibles (comentarios DROP presentes)
  ✅ No breaking changes en esquema existente (tabla users sin modificar)
```

---

### EX-5 — Argus Fase 5 (Tests de integración)

Tests esperados:
```
UserControllerSecurityTest.java
  ✅ testGetUsers_AsAdmin_Returns200
  ✅ testGetUsers_AsViewer_Returns200
  ✅ testGetUsers_Unauthenticated_Returns401
  ✅ testCreateUser_AsUser_Returns403
  ✅ testDeleteUser_AsAdmin_Returns204
```

**Argus → PASSED**

---

## EX-1 GATE — SpecifyAnalyze (post-implementación)

Segunda puerta de consistencia: valida que lo implementado coincide con tasks.md.

Output esperado:
```
GATE: EX-1
STATUS: PASSED
CHECKS:
  ✅ T001..T014 todos marcados DONE en tasks.md
  ✅ IAuthorizationPort implementada en SecurityConfig
  ✅ Flyway migrations presentes en resources/db/migration/
  ✅ Tests de integración cubren todos los AC de spec.md
  ✅ constitution.md VERSION sin cambiar (sin regresión de principios)
DRIFT_DETECTED: false
```

---

## Atlas — Resumen Final

Output esperado:
```
Status: complete
Phase: All phases complete

Last Action & Changes:
- 12 archivos Java nuevos/modificados en user-management-demo/
- 2 scripts Flyway en resources/db/migration/
- 4 artefactos Specify en .specify/specs/rbac-spring/
- SP-5 gate: PASSED | EX-1 gate: PASSED

Delegations:
- Prometheus: pipeline SP-0..SP-5
- Sisyphus: fases EX-1..EX-3
- Hephaestus (maintenance): EX-4
- Argus: EX-5
- Atenea: revisión de seguridad en todas las fases
- Themis: code review EX-1..EX-3

Pack Registry: backend-workflow identificado como relevante (no activado, shipped+available)

Git Commit:
feat: add RBAC to user-management-demo via Specify pipeline

- Role entity, Permission enum, IAuthorizationPort in domain layer
- RoleService and UserService authorization in application layer
- SecurityConfig and RoleRepositoryAdapter in infrastructure layer
- Flyway migrations V2 (roles) and V3 (user_roles)
- Integration tests with @WithMockUser for all protected endpoints
- SP-5 and EX-1 Specify gates passed
```
