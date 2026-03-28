## Plan: Layered Runtime Followup
Pequeño pase de alineación para cerrar residuos del runtime por capas. El objetivo es dejar claro que Zeus sigue siendo la raíz, que los dioses opcionales no se invocan como superficie raíz, y que los hooks de `SpecifyAnalyze` conserven trazabilidad suficiente sin romper la compatibilidad existente.

**Phases 2**
1. **Phase 1: Clarify hierarchy semantics**
   - **Objective:** Eliminar wording ambiguo sobre capas y routing en el runtime raíz.
   - **Files/Functions:** `.github/agents/Zeus.agent.md`
   - **QA Focus:** Confirmar que la regla de jerarquía sigue coherente con `validate_layer_hierarchy.py`.
   - **Steps:** 1. Revisar wording ambiguo. 2. Ajustar la regla para distinguir superficies raíz estables de dioses opcionales y hojas. 3. Verificar que el cambio no contradiga validadores.
2. **Phase 2: Tighten shared analyze tracing**
   - **Objective:** Mejorar la semántica de traza del hook compartido de `SpecifyAnalyze` y documentar el parentado abstracto.
   - **Files/Functions:** `.specify/extensions.yml`, `.github/agents/SpecifyAnalyze.agent.md`
   - **QA Focus:** Confirmar que los hooks de análisis siguen siendo compatibles con SP-5 y EX-1.
   - **Steps:** 1. Ajustar el hook compartido de análisis. 2. Documentar en el agente por qué el parent es abstracto. 3. Correr validaciones/lint/tests puntuales.

**Open Questions 1**
1. ¿Conviene mantener `parent-agent` abstracto para `SpecifyAnalyze` o especializarlo por flujo? Recomendación actual: mantenerlo abstracto porque el hook es compartido entre Prometheus y Sisyphus.