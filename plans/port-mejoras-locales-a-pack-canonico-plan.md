# Plan: Port mejoras locales a pack canónico

**Created:** 2026-03-20
**Status:** Ready for Atlas Execution

## Summary

Este plan define cómo absorber en el pack canónico del proyecto (`.github/agents`) las mejores ventajas operativas del pack local de prompts sin perder la arquitectura superior ya conseguida en este repositorio. La estrategia es portar solo mejoras de alto valor y bajo acoplamiento: mejor narrativa operativa en `Atlas`, heurísticas avanzadas pero opcionales en `Argus`, una ampliación controlada de `Hephaestus`, y una comparación quirúrgica entre `Afrodita` local y `Frontend-Engineer` del proyecto. La primera fase ejecutable es intencionalmente pequeña: tocar solo `Atlas.agent.md` para ganar ergonomía diaria, mejor estado/checklist y una integración Atlassian explícita pero no obligatoria.

## Context & Analysis

**Relevant Files:**
- `.github/agents/Atlas.agent.md`: conductor canónico; ya contiene discovery, routing, artifacts, output contract y una arquitectura más sólida que la local.
- `/home/daniel/.config/Code - Insiders/User/prompts/Atlas.agent.md`: aporta mejores señales de seguimiento diario, estado operativo y un flujo Atlassian más explícito.
- `.github/agents/Argus.agent.md`: versión canónica limpia, enfocada y secuenciada correctamente hacia tests dirigidos primero.
- `/home/daniel/.config/Code - Insiders/User/prompts/Argus-subagent.agent.md`: suma mutation testing, property-based testing, mayor amplitud de edge cases y validación más agresiva, aunque con más verbosidad.
- `.github/agents/Hephaestus.agent.md`: versión canónica bien acotada para deploy/ops/build/readiness.
- `/home/daniel/.config/Code - Insiders/User/prompts/Hephaestus-subagent.agent.md`: añade valor en incidentes, mantenimiento, performance y capacidad, pero también empuja al agente hacia un rol demasiado amplio si se copia completo.
- `.github/agents/Frontend-Engineer.agent.md`: ya supera al local en estructura, cobertura de estados UI, accesibilidad y claridad canónica.
- `/home/daniel/.config/Code - Insiders/User/prompts/Afrodita-subagent.agent.md`: conserva algunas ventajas de implementación/pulido y detección contextual, pero no conviene portar ni su tono ni su amplitud completa.
- `README.md`: deja claro que `.github/agents` es la fuente de verdad principal; solo debe tocarse si el cambio en flujo es visible para el usuario.
- `docs/Atlas_Agents_Project_Document.md`: documentación extensa del pack canónico; conviene tocarla únicamente si el comportamiento operativo visible cambia de forma material.

**Key Functions/Classes:**
- `Atlas.agent.md` → `## 0. Start Of Run`, `## 5. Workflow`, `## 7. Output Contract`, `## 8. Delegation Briefs`.
- Local `Atlas.agent.md` → `Agent Controls`, `state_tracking`, `Atlassian Tools`, reglas de delegación y operación diaria.
- `Argus.agent.md` → `## Testing Workflow`, `## Return Format`.
- Local `Argus-subagent.agent.md` → `Advanced Testing Techniques`, `Edge Case Discovery`, `Regression Testing`, `Production-Like Environment Testing`.
- `Hephaestus.agent.md` → `## Workflow`, `## Operations Support`, `## Return Format`.
- `Frontend-Engineer.agent.md` → `## Core Workflow`, `## Quality Requirements`, `## UI State Coverage`, `## Output Format`.
- Local `Afrodita-subagent.agent.md` → `Core Workflow`, `Frontend Best Practices`, `Frontend-Specific Considerations`, cierre con recomendaciones para QA.

**Dependencies:**
- Convenciones de archivos de agentes en VS Code (frontmatter YAML válido, campos `name`, `description`, `tools`, `handoffs`).
- Regla de precedencia del repo: `.github/agents` como canónico, `plugins/` como distribución secundaria opcional.
- Documentación pública que ya comunica el flujo root-first y los roles de `Atlas`, `Argus`, `Hephaestus` y `Frontend-Engineer`.

**Patterns & Conventions:**
- Mejoras pequeñas y claramente delimitadas, no reescrituras completas.
- Especialistas con fronteras nítidas: cada agente debe seguir haciendo una cosa muy bien.
- El pack canónico debe ser portable y genérico; nada de rutas absolutas, dependencias ocultas o ecosistemas demasiado específicos.
- La mejora debe entrar primero en `.github/agents`; cualquier espejo o pack secundario queda fuera salvo necesidad explícita.
- Las capacidades avanzadas deben entrar como guía opcional o escalación justificada, no como comportamiento por defecto.

## Implementation Phases

### Phase 1: Uplift operativo de Atlas

**Objective:** Mejorar la narrativa de seguimiento, el checklist/estado y la ergonomía diaria de `Atlas` sin alterar su arquitectura de conductor ni convertirlo en un prompt dependiente de herramientas externas.

**Files to Modify/Create:**
- `.github/agents/Atlas.agent.md`: incorporar una capa de operación diaria más clara y una integración opcional de contexto tipo Atlassian/tickets/docs.

**QA Focus:**
- `Atlas.agent.md`: validar que la mejora no rompa discovery, routing, output contract ni el carácter canónico/root-first del pack.
- Confirmar que la nueva guía de estado/checklist no requiera una tool específica para existir.

**Steps:**
1. Reforzar el patrón de apertura y seguimiento del run para que `Atlas` mantenga mejor continuidad narrativa entre delegaciones, decisiones y siguiente acción.
2. Añadir una guía ligera de estado/checklist operativo para runs largos, pero expresada como disciplina de respuesta y no como dependencia de un `todo` tool concreto.
3. Incorporar una sección de “work item / doc ingestion” donde Jira/Confluence sean ejemplos explícitos de fuentes externas, pero siempre como integración opcional cuando exista helper/skill/herramienta disponible.
4. Mantener la parte Atlassian formulada como ejemplo reutilizable, nunca como flujo obligatorio ni como requisito del repositorio.
5. Revisar tras el cambio si el `README.md` necesita una nota mínima; si no hay impacto visible al usuario, dejar la documentación intacta en esta fase.

**Acceptance Criteria:**
- [ ] `Atlas.agent.md` conserva la arquitectura actual de discovery, routing, planes y artifacts.
- [ ] Atlas gana continuidad operativa visible: mejor “qué se hizo / qué sigue / por qué”.
- [ ] La guía de checklist/estado no depende de una tool específica para funcionar.
- [ ] La integración Atlassian queda explícita pero opcional, sin rutas absolutas ni dependencias del ecosistema personal/local.
- [ ] All tests pass.
- [ ] Code follows project conventions.

---

### Phase 2: Argus con heurísticas avanzadas opt-in

**Objective:** Enriquecer `Argus` con técnicas de QA más profundas donde aporten valor, sin convertir cada verificación en un proceso pesado o verboso.

**Files to Modify/Create:**
- `.github/agents/Argus.agent.md`: ampliar taxonomía de edge cases y añadir un carril opcional para técnicas avanzadas.

**QA Focus:**
- `Argus.agent.md`: comprobar que sigue comenzando por tests dirigidos y mantiene un reporte compacto y accionable.
- Verificar que las técnicas avanzadas queden claramente condicionadas a riesgo, soporte del proyecto o justificación explícita.

**Steps:**
1. Mantener “targeted first” como invariante principal.
2. Ampliar la matriz de edge cases con límites duros, corrupción parcial, resource exhaustion, invariantes, fallos parciales y estados inválidos más ricos.
3. Añadir mutation testing, property-based testing, state-transition testing y análisis de particiones como técnicas opcionales cuando el riesgo o el tipo de cambio lo justifiquen.
4. Integrar esas técnicas dentro del formato compacto actual de Argus en vez de portar el formato largo del local.
5. Mantener validaciones live/production-like solo cuando el scope lo pida explícitamente o el entorno ya esté claramente disponible.

**Acceptance Criteria:**
- [ ] `Argus.agent.md` sigue priorizando pruebas mínimas relevantes antes de escalar alcance.
- [ ] Mutation/property-based testing aparecen como guía opcional, no como obligación universal.
- [ ] El reporte de Argus sigue siendo compacto, claro y compatible con el flujo actual de Atlas.
- [ ] Se amplía el pensamiento de edge cases sin mezclar QA con code review.
- [ ] All tests pass.
- [ ] Code follows project conventions.

---

### Phase 3: Hephaestus con valor navaja suiza, pero con guardarraíl

**Objective:** Añadir a `Hephaestus` parte del valor operativo del prompt local sin romper su delimitación como agente de build/deploy/ops.

**Files to Modify/Create:**
- `.github/agents/Hephaestus.agent.md`: ampliar modos de uso y cobertura de operación, manteniendo límites de rol.

**QA Focus:**
- `Hephaestus.agent.md`: validar que el agente no absorbe responsabilidades de implementación, review o testing.
- Verificar que los outputs siguen siendo seguros, medibles y orientados a evidencia.

**Steps:**
1. Añadir un mini decision frame de entrada: deploy, release readiness, incident response, maintenance o performance.
2. Portar desde el local la mejor parte de incident/performance/maintenance/capacity como soporte operativo adicional, no como desborde de responsabilidades.
3. Reforzar el patrón “evidence first, smallest safe action, validate before apply”.
4. Mantener la separación explícita respecto a review, QA y code changes.
5. Ajustar el formato de salida para que cubra mejor readiness/incidents/performance sin crecer innecesariamente.

**Acceptance Criteria:**
- [ ] `Hephaestus.agent.md` soporta deploy/readiness/incident/performance con mejor claridad de entrada.
- [ ] El agente sigue sin invadir testing, review o implementación.
- [ ] El valor añadido del local entra como cobertura operativa, no como amplitud descontrolada.
- [ ] Las salidas siguen siendo estructuradas y basadas en evidencia.
- [ ] All tests pass.
- [ ] Code follows project conventions.

---

### Phase 4: Port selectivo de Afrodita hacia Frontend-Engineer

**Objective:** Comparar `Afrodita` local con `Frontend-Engineer` y portar solo capacidades o estructura útiles, preservando la superioridad del prompt canónico actual.

**Files to Modify/Create:**
- `.github/agents/Frontend-Engineer.agent.md`: incorporar únicamente mejoras concretas detectadas como faltantes.

**QA Focus:**
- `Frontend-Engineer.agent.md`: verificar que se conserva la cobertura de estados UI, accesibilidad y responsive behavior ya presentes.
- Confirmar que no se reintroduce un estilo más ruidoso o menos canónico.

**Steps:**
1. Comparar la detección de stack/diseño/build/browser-support del local con la del prompt canónico.
2. Portar solo aquello que realmente mejore el flujo del implementador frontend: mejor detección contextual, mejor cierre/polish, mejor señal hacia QA cuando corresponda.
3. No portar el tono/persona de Afrodita ni convertir `Frontend-Engineer` en un conductor o agente demasiado generalista.
4. Mantener como esqueleto principal la cobertura de estados, accesibilidad y responsive requirements del prompt canónico.
5. Si la comparación concluye que no hace falta tocar `Frontend-Engineer`, documentar explícitamente esa decisión y cerrar la fase sin churn innecesario.

**Acceptance Criteria:**
- [ ] Solo se portan mejoras concretas y justificadas desde Afrodita.
- [ ] `Frontend-Engineer` mantiene su estructura superior actual.
- [ ] No se importa el tono/persona ni la amplitud innecesaria del local.
- [ ] La fase puede cerrarse con “sin cambios” si el análisis demuestra que el prompt actual ya es mejor.
- [ ] All tests pass.
- [ ] Code follows project conventions.

---

### Phase 5: Documentación mínima solo si el flujo visible cambia

**Objective:** Reflejar en la documentación únicamente aquellas mejoras que cambien de verdad la experiencia observable del pack canónico.

**Files to Modify/Create:**
- `README.md`: nota breve solo si Atlas cambia su operación visible para el usuario.
- `docs/Atlas_Agents_Project_Document.md`: ajustar descripción operativa solo si el cambio supera el nivel de detalle interno del prompt.

**QA Focus:**
- Verificar que la documentación no se adelanta a comportamientos inexistentes.
- Evitar ruido documental si los cambios son internos o demasiado sutiles para el usuario final.

**Steps:**
1. Revisar tras las fases 1–4 si cambió el comportamiento visible del pack canónico.
2. Si cambió, documentar el mínimo necesario en `README.md` y, solo si aporta, en `docs/Atlas_Agents_Project_Document.md`.
3. Si el cambio es solo interno o de calidad de prompt, cerrar la fase sin tocar docs.
4. Mantener el mensaje central: `.github/agents` sigue siendo la fuente de verdad principal.
5. No tocar `plugins/README.md` en este pase salvo que exista una necesidad documental realmente directa.

**Acceptance Criteria:**
- [ ] Solo se actualiza documentación si el cambio es visible y útil para el usuario.
- [ ] `README.md` y docs siguen comunicando `.github/agents` como fuente de verdad principal.
- [ ] No se añade churn documental innecesario.
- [ ] All tests pass.
- [ ] Code follows project conventions.

## Open Questions

1. ¿La integración Atlassian en `Atlas` debe nombrar Jira/Confluence explícitamente o volverse completamente genérica?
   - **Option A:** Hablar solo de “tickets/docs externos” para máxima neutralidad.
   - **Option B:** Mencionar Jira/Confluence como ejemplos explícitos, junto a la regla de que la integración es opcional y depende de helpers disponibles.
   - **Recommendation:** **Option B**, porque cumple el pedido del usuario y mejora la ergonomía real, siempre que quede clarísimo que es ejemplo opcional y no dependencia.

2. ¿Las técnicas avanzadas de `Argus` deben quedarse solo en el prompt o también reflejarse en docs públicas?
   - **Option A:** Documentarlas en README/docs.
   - **Option B:** Mantenerlas solo dentro de `Argus.agent.md` salvo que cambien el flujo visible del usuario.
   - **Recommendation:** **Option B**, para no sobredocumentar heurísticas internas del agente.

3. ¿Conviene portar tono/persona de `Afrodita` al `Frontend-Engineer` canónico?
   - **Option A:** Sí, para heredar personalidad y especialización.
   - **Option B:** No; portar solo estructura/capacidades útiles y conservar el tono sobrio actual.
   - **Recommendation:** **Option B**, porque el prompt canónico ya es más claro y estable como pieza central.

4. ¿Este pase debe sincronizar también packs secundarios en `plugins/`?
   - **Option A:** Sí, en paralelo, para evitar drift inmediato.
   - **Option B:** No; primero estabilizar `.github/agents`, luego decidir si conviene reflejarlo en packs secundarios.
   - **Recommendation:** **Option B**, alineado con la restricción de mantener `.github/agents` como fuente de verdad principal y con el objetivo de cambios pequeños y coherentes.

## Risks & Mitigation

- **Risk:** Sobreportar el pack local y degradar la claridad del pack canónico.
  - **Mitigation:** Hacer cambios por fases, empezando por un único archivo (`Atlas.agent.md`) y definiendo explícitamente qué no se porta en cada agente.

- **Risk:** Convertir la integración Atlassian en una dependencia de entorno o de herramientas específicas.
  - **Mitigation:** Redactarla como integración opcional basada en ejemplos, sin paths absolutos ni herramientas obligatorias.

- **Risk:** Hacer que `Argus` se vuelva lento o excesivamente teórico.
  - **Mitigation:** Mantener “targeted first” como comportamiento por defecto y dejar mutation/property-based testing como escalación justificada.

- **Risk:** Diluir el rol de `Hephaestus` hasta volverlo un agente demasiado amplio.
  - **Mitigation:** Reforzar explícitamente lo que no hace: no review, no QA, no implementación.

- **Risk:** Introducir churn en `Frontend-Engineer` aunque ya sea mejor que Afrodita.
  - **Mitigation:** Permitir cierre explícito de la fase 4 con “no change needed” si la comparación no justifica edición.

- **Risk:** Documentar cambios invisibles y generar ruido.
  - **Mitigation:** Tratar la fase documental como estrictamente condicional.

## Success Criteria

- [ ] `Atlas` incorpora mejor narrativa operativa, mejor checklist/estado y mejor ergonomía diaria sin perder su arquitectura superior.
- [ ] `Atlas` gana una integración explícita con flujo tipo Atlassian/tickets/docs, pero opcional y no dependiente.
- [ ] `Argus` incorpora técnicas avanzadas como mutation/property-based testing de forma opcional y bien delimitada.
- [ ] `Hephaestus` amplía su valor operativo sin convertirse en un agente descontroladamente generalista.
- [ ] `Frontend-Engineer` solo absorbe mejoras realmente justificadas desde Afrodita, o se mantiene intacto si ya es superior.
- [ ] `.github/agents` permanece como fuente de verdad principal.
- [ ] Las mejoras propuestas son pequeñas, claras y coherentes con el estilo actual del proyecto.
- [ ] All phases complete with passing tests.
- [ ] Code reviewed and approved.

## Notes for Atlas

- **Primera fase ejecutable recomendada:** `Phase 1: Uplift operativo de Atlas`.
- Mantén la Fase 1 reducida a `Atlas.agent.md` salvo que, al terminarla, exista un motivo fuerte y visible para tocar `README.md`.
- No intentes sincronizar `plugins/` en este primer pase.
- No copies texto local “tal cual”; extrae principios operativos y reexprésalos en el estilo sobrio y portátil del pack canónico.
- En cada fase, registra también qué se decidió **no** portar y por qué; eso es parte del objetivo del usuario, no un detalle secundario.
