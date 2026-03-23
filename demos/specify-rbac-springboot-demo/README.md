# Demo: Specify Pipeline + RBAC en Spring Boot (Hexagonal)

Smoke test de extremo a extremo que ejercita:

1. **Pipeline Specify completo** (Prometheus → Constitution → Spec → Clarify → Plan → Tasks → Analyze → Implement)
2. **Pack Registry** (selección dinámica del pack `backend-workflow`)
3. **SpecifyAnalyze en doble puerta** (SP-5 pre-tareas + EX-1 post-implementación)
4. **Hephaestus modo Maintenance** (validación de migración de BD)
5. **Atenea** (revisión de seguridad por ser RBAC)

---

## Escenario

Añadir **Role-Based Access Control (RBAC)** al proyecto `user-management-demo`  
(Spring Boot 3.2.2, JPA, arquitectura hexagonal).

Roles: `ADMIN`, `USER`, `VIEWER`.  
Cada endpoint REST verifica que el usuario autenticado tenga el rol requerido.

---

## Prerrequisitos

- VS Code con GitHub Copilot habilitado
- Agentes activos: `@Atlas`, `@Prometheus`, todos los `Specify*`
- Java 17+ y Maven (solo para smoke de compilación)
- Python 3.9+ (para el harness de validación)

---

## Cómo ejecutar

### Paso 1 — Lanzar el pipeline

Copia el prompt de [DEMO_PROMPT.md](DEMO_PROMPT.md) y pégalo en el chat de Copilot dirigido a `@Atlas`.

### Paso 2 — Verificar artefactos Specify

```bash
cd demos/specify-rbac-springboot-demo
python rbac_harness.py
```

### Paso 3 — Ejecutar el test suite completo

```bash
cd demos/specify-rbac-springboot-demo
py -m unittest -v
```

Output esperado:
```
TestPackRegistry        ... ok   (pack-registry.json tiene backend-workflow y canonical-root)
TestSpecifyArtifacts    ... ok   (todos los artefactos .specify/ existen y están bien formados)
TestHarnessUnit         ... ok   (lógica interna del harness)
TestImplementationSmoke ... SKIP (se activa solo si user-management-demo fue modificado)
```

---

## Archivos

| Archivo | Propósito |
|---|---|
| `DEMO_PROMPT.md` | Prompt listo para pegar en `@Atlas` |
| `EXPECTED_FLOW.md` | Traza detallada de agentes y artefactos esperados |
| `rbac_harness.py` | Validador de artefactos Specify + Pack Registry + smoke de dominio |
| `test_rbac_harness.py` | Suite de pruebas del harness |

---

## Qué valida esta demo

| Feature | Agente/Componente | Gate de éxito |
|---|---|---|
| Pipeline Specify completo | Prometheus + Specify* | Artefactos en `.specify/specs/rbac-spring/` |
| Doble puerta Analyze | SpecifyAnalyze | Marcadores `SP-5` y `EX-1` en artifacts |
| Selección de pack | Pack Registry | `backend-workflow` detectado como relevante |
| Review de seguridad | Atenea | Informe presente en fase de implementación |
| Migración de BD | Hephaestus (maintenance) | Plan de migración en `plan.md` |
| Implementación hexagonal | Sisyphus | Nuevas clases en `domain/model/` y `domain/port/` |
