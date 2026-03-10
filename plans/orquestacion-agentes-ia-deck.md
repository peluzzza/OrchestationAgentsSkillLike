# Orquestación de agentes de IA en desarrollo de software (estructura por bloques)
Duración total estimada: 31–34 min (11 slides)

## Slide 1 — Portada / objetivo
- Tiempo: ~1 min
- Tema: orquestación de trabajo con agentes IA (comportamiento)
- Objetivo: explicar roles, handoffs, puntos de control y economía de tokens
- Resultado esperado: un flujo repetible para construir software con menos retrabajo

## Slide 2 — Agenda (5 bloques)
- Tiempo: ~1 min
- Bloque 1: cómo funciona un agente “monolítico” (1 modelo hace todo)
- Bloque 2: qué es orquestación (principios + roles) + guía de modelos por rol (incl. frontend)
- Bloque 3: handoffs + configuración de IDE (paralelismo práctico)
- Bloque 4: puntos de control (quality gates) + flujo end‑to‑end
- Bloque 5: buenas prácticas + cierre



## Slide 3 — Bloque 1: el agente monolítico (un solo modelo para todo)
- Tiempo: ~4 min
- Flujo típico: investigar → diseñar → implementar → documentar → testear → “release” con el mismo modelo
- Dónde brilla: coherencia local y capacidad de razonamiento cuando el problema es difícil
- Dónde falla más: mezcla de roles (decidir + editar + validar), y contexto que crece sin control
- Coste operativo:
  - Prompts más grandes (historial + contexto) ⇒ más tokens por iteración
  - Más iteraciones “fallidas” (sin checkpoints) ⇒ más vueltas y más requests
- Ejemplo: usar un modelo potente tipo “Opus” para TODO puede ser efectivo, pero suele ser ineficiente (pagas potencia incluso para tareas mecánicas como localizar/recopilar)



## Slide 4 — Bloque 2: qué es orquestación (definición práctica)
- Tiempo: ~3 min
- Orquestación = dividir el trabajo por roles, coordinar handoffs y aplicar puntos de control (quality gates)
- Meta: flujo repetible end‑to‑end (plan → cambio mínimo → pruebas → revisión → entrega)
- Concurrencia: algunas tareas se pueden ejecutar en paralelo (p. ej., exploración + búsqueda de tests)
- Referencia (solo como ejemplo de enfoque): https://github.com/bigguy345/Github-Copilot-Atlas


## Slide 5 — Bloque 2: guía de modelos por rol (mapa rápido y tradeoffs)
- Tiempo: ~3 min
- Nota: ejemplos orientativos; depende de tu entorno/suscripción/latencia/coste. Los nombres y versiones cambian con frecuencia.
- Regla simple: modelo grande para “decidir”; modelo rápido para “buscar/sintetizar/verificar”; modelo code‑centric para “editar con precisión”.
- Heurística práctica:
  - Si el problema es ambiguo → suele ayudar subir “capacidad” (razonamiento)
  - Si el problema es mecánico/repetible → suele convenir bajar coste/latencia (iterar rápido)
  - Si el riesgo es alto → a menudo compensa gastar en un buen “reviewer” + gates
- Ejemplos típicos (según disponibilidad):
  - Razonamiento general (p. ej., GPT‑5.3, Opus 4.6, Sonnet 4.6): arquitectura, decisiones complejas; coste/latencia si lo usas para tareas mecánicas
  - Modelos rápidos (p. ej., Gemini Flash 3.0): exploración, búsquedas, resúmenes; puede flojear en decisiones profundas si falta contexto
  - Modelos “Pro”/equilibrados (p. ej., Gemini Pro 3.1): buen balance; no siempre supera a un “grande” en problemas muy difíciles
  - Modelos code‑centric (p. ej., GPT Codex 5.3): edición/refactors acotados; no sustituye a revisión/QA si no hay gates

## Slide 6 — Bloque 2: Gemini Pro (p. ej., 3.1) para frontend/UI (enfoque y ventajas)
- Tiempo: ~3 min
- Dónde suele encajar bien:
  - Implementación UI “pegada al diseño”: componentes, layouts, estados, responsive
  - Iteración rápida de variantes (copy, estructura, pequeñas mejoras de usabilidad)
  - Ajustes de CSS/Tailwind y composición de componentes con cambios acotados
- Ventajas típicas en práctica (cuando hay buen contexto):
  - A menudo propone alternativas razonables sin inflar demasiado el scope
  - Suele ser útil para “pulir”: consistencia visual, naming, props, estados vacíos
  - Puede ayudar a revisar accesibilidad básica (labels, focus) como checklist inicial
- Tradeoffs y cautelas:
  - Si faltan constraints puede inventar detalles → conviene anclar con design system real y “qué NO”
  - La verificación final suele requerir ejecución local y revisión humana



## Slide 7 — Bloque 3: handoffs y artefactos (lo que realmente escala)
- Tiempo: ~3 min
- Handoff = un paquete pequeño, verificable y reutilizable (entrada/salida) entre roles
- Ejemplos de handoffs (genéricos):
  - Objetivo + alcance (“qué NO”) + criterio de aceptación
  - Lista corta de archivos foco + “ruta crítica” + tests ancla
  - Diff acotado + explicación + comandos para verificar
  - Señales de QA/build + riesgos + checklist de entrega
- Regla de oro: devolver “high‑signal” (resumen accionable), no volcar el repo



## Slide 8 — Bloque 3: configuración típica en IDEs (VS Code / IntelliJ)
- Tiempo: ~3 min
- VS Code (lo típico para paralelismo):
  - Separar roles con hilos de chat/ventanas/sesiones
  - Usar Tasks/terminales para ejecutar tests/build de forma repetible
  - Si tu entorno soporta orquestación/multi‑agente: habilitar la opción equivalente (según versión/feature flag) y usar plantillas de prompts por rol
  - Ejemplos de settings que a veces se usan (dependen de versión): `chat.customAgentInSubagent.enabled`, `github.copilot.chat.responsesApiReasoningEffort`
  - Nota frecuente: algunos equipos usan VS Code Insiders para acceder antes a capacidades de orquestación
- IntelliJ (lo típico):
  - Copilot plugin (autocompletado + chat) como asistente dentro del IDE
  - Menos “multi‑agente” nativo en algunos setups ⇒ compensa con handoffs por artefactos (plan/checklist/comandos) y run configurations



## Slide 9 — Bloque 4: puntos de control (quality gates) — qué son y por qué
- Tiempo: ~4 min
- “Punto de control” = parada obligatoria con criterios objetivos antes de avanzar
- Ejemplos (mínimo viable):
  - Gate 1 (alcance): objetivo, “no hacer”, criterio de aceptación
  - Gate 2 (evidencia): tests que cubren el caso + cómo ejecutarlos
  - Gate 3 (entrega): suite verde + build limpio + pasos reproducibles
- Gates opcionales (si el cambio lo requiere): mapa de impacto, revisión arquitectónica, checklist de release
- Beneficio: menos retrabajo, menos re‑explicación, menos “vueltas” caras



## Slide 10 — Bloques 4–5: orquestación en práctica (roles + flujo + coste + anti‑patrones)
- Tiempo: ~6 min
- Roles “clásicos” (resumen): orquestador, explorador, implementador, reviewer, QA/tester, DevOps/release
- Flujo end‑to‑end (compacto):
  - 1) Planificar: DoD + límites + gates
  - 2) Explorar: entrypoints + dependencias + tests ancla
  - 3) Implementar: cambio mínimo + pruebas primero cuando aplica
  - 4) Revisar: contratos/arquitectura; frenar scope creep
  - 5) Verificar/Release: suite + build + comandos reproducibles
- Por qué suele ahorrar tokens y “premium requests”:
  - Contexto mínimo por rol (menos prompts gigantes)
  - Menos relectura (cada rol mira solo lo que necesita)
  - Menos iteraciones fallidas (gates reducen vueltas)
- Buenas prácticas (ultra‑compactas): límites explícitos, evidencia (tests/comandos), diffs pequeños, reproducibilidad
- Anti‑patrones: un rol lo hace todo, prompts kilométricos sin artefactos, cambios multi‑capa sin motivo, avanzar sin suite verde



## Slide 11 — Cierre + demo en vivo + Q&A
- Tiempo: ~2 min
- Demo en vivo (1 frase): reforzar un comportamiento con un test y un cambio mínimo, siguiendo gates
- Consejos accionables:
  - Empieza con 3 roles + 3 gates (no intentes “todo” el primer día)
  - Estandariza handoffs (plan, lista de archivos, comandos)
  - Mide señales simples: tamaño del diff, tiempo a tests verdes, número de iteraciones
- Preguntas
