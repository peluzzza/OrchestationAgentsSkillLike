## Informe: External Ecosystem Investigation For OrchestationAgentsSkillLike
Este informe aterriza la investigación previa de ecosistemas externos sobre el repositorio `review_clones/OrchestationAgentsSkillLike`. El objetivo es preparar un merge por carpetas, incremental y reversible, centrado únicamente en capacidades de orquestación, agentes, memoria, plugins, automatización y demos. Queda explícitamente fuera cualquier lógica de negocio ajena al dominio de orquestación.

**Repositorio base**
- `review_clones/OrchestationAgentsSkillLike`
- Modelo actual: raíz canónica en `.github/agents/`, especialistas ocultos, `Atlas` como único conductor visible, `Prometheus` para planificación y `.specify/` como espina dorsal de diseño.

## Estado actual del repo
### Lo que ya resuelve bien
- Orquestación multiagente con patrón conductor + especialistas.
- Flujo Specify documentado y parcialmente operacional.
- Separación entre núcleo canónico (`.github/agents/`) y distribución opcional (`plugins/`).
- Demos pequeños y útiles para validar flujos.
- Marketplace y sincronización de packs ya esbozados.

### Lo que todavía falta o puede fortalecerse
- Memoria operativa persistente y disciplinada entre sesiones.
- Packs opcionales para automatización/MCP y UX especializados.
- Scripts de bootstrap, health checks y sincronización más robustos.
- Documentación explícita de “merge lanes” para nuevas capacidades externas.
- Política clara para mantener paridad entre raíz canónica y mirrors opcionales.

## Donantes externos y aporte recomendado
### Everything Claude Code
**Aportar**
- Mejores contratos de delegación.
- Instrucciones más compactas para conductores y especialistas.
- Patrones maduros de ergonomía para desarrollo dirigido por agentes.

**No aportar**
- Dialectos o convenciones demasiado específicas de otro runtime.
- Comandos o hábitos acoplados a una CLI concreta.

### Superpowers
**Aportar**
- Ideas de empaquetado modular.
- Helpers de instalación, bootstrap y sincronización.
- Capacidad de escalar el catálogo sin inflar el núcleo.

**No aportar**
- Automatismos opacos difíciles de depurar.
- Duplicación innecesaria entre raíz y plugins.

### UI UX Pro Max
**Aportar**
- Especialización frontend/UI como pack opcional.
- Demos y assets orientados a diseño para `Afrodita` o packs afines.
- Plantillas de flujos UX guiados.

**No aportar**
- Librerías visuales gigantes dentro del núcleo.
- Artefactos de showcase que no prueben flujos reales.

### Claude-Mem
**Aportar**
- Memoria ligera de sesión, decisiones y continuidad.
- Convenciones explícitas de write/read de memoria.
- Resúmenes persistentes, acotados y con intención.

**No aportar**
- Persistencia descontrolada.
- Dependencias pesadas o infraestructura nueva antes de validar utilidad.

### n8n-MCP
**Aportar**
- Packs opcionales para automatización y conectores MCP.
- Scripts/demo de integraciones.
- Documentación de capacidades externas controladas.

**No aportar**
- Dependencia rígida en un runtime de automatización externo para el core.
- Acoplar el repo a un único proveedor de automatización.

## Merge por carpeta
| Carpeta | Rol actual | Aporte recomendado | Prioridad |
|---|---|---|---|
| `.github/agents/` | Núcleo canónico de agentes | Ergonomía de delegación y contratos más finos | Alta |
| `.specify/` | Columna vertebral de planificación | Memoria ligera y mejores plantillas de continuidad | Alta |
| `plugins/` | Packs opcionales | UI/UX, MCP/automation, utilidades modulares | Alta |
| `scripts/` | Utilidades operativas | Sync, bootstrap, catálogo, diagnóstico | Media |
| `docs/` | Onboarding y arquitectura | Guías operativas cortas y rutas de adopción | Alta |
| `demos/` | Validación práctica | Demos pequeños de UX, memoria y MCP | Media |
| `.github/plugin/` | Marketplace/catalogación | Curación de packs y metadatos de instalación | Media |
| `.vscode/` | Activación local | Flags claras para root-first vs plugin mode | Baja |

## Principios de merge
- La raíz `.github/agents/` sigue siendo la fuente canónica.
- `plugins/` sigue siendo opt-in.
- Se importan capacidades, no dogmas ni productos enteros.
- Todo batch debe ser reversible y verificable.
- Primero documentación, memoria ligera y packs opcionales; después scripts y demos.
- No se mezcla lógica de negocio externa con el dominio del repo.

## Riesgos principales
1. **Deriva entre raíz y plugins**
   - Mitigación: documentar qué es canónico y qué es mirror opcional.
2. **Sobrecargar el core con features “bonitas” pero no esenciales**
   - Mitigación: dejar UX y automatización en `plugins/`.
3. **Memoria sin control**
   - Mitigación: comenzar con archivos acotados de sesión/decisión.
4. **Meter runtimes externos demasiado pronto**
   - Mitigación: empezar por demos y contratos, no por dependencia obligatoria.

## Orden recomendado de batches
1. **Batch 1 — Investigación + Merge Lanes + Roadmap**
   - `plans/`
   - `README.md`
   - `plugins/README.md`
2. **Batch 2 — Memory Layer Lite**
   - `.specify/memory/`
   - `docs/`
3. **Batch 3 — Optional Plugin Packs**
   - `plugins/automation-workflow/`
   - `plugins/frontend-workflow/` refinements
4. **Batch 4 — Scripts + Demos**
   - `scripts/`
   - `demos/`
5. **Batch 5 — Parity + Catalog Hygiene**
   - `.github/plugin/`
   - sync/parity helpers

## Batch que conviene ejecutar primero
El primer batch correcto es documental y estructural. Permite congelar criterios antes de tocar agentes reales y evita el clásico deporte extremo de “romper por entusiasmo”. Incluye:
- informe de investigación
- plan de merge por fases
- actualización de README raíz con merge lanes
- actualización de `plugins/README.md` para dejar claro el espacio de futuros packs opcionales

## Resultado esperado tras el ciclo completo
- Repo de orquestación más modular.
- Memoria útil y disciplinada.
- Packs opcionales para UI/UX y automatización/MCP.
- Mejor bootstrap y demos operativos.
- Núcleo Atlas/Prometheus/Sisyphus mantenido como experiencia por defecto.
