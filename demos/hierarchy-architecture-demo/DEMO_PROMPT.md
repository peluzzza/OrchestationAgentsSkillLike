# Hierarchy Architecture Demo Prompt

Use this prompt with `@Atlas` to trigger all three layer crossings in a single measurable session.

---

## Demo Prompt (copy into VS Code chat with @Atlas)

```
@Atlas

I need you to execute the following multi-domain task so every layer crossing in the 3-layer hierarchy is exercised. This is a hierarchy architecture validation run — please narrate each delegation boundary explicitly.

**Task:** Scaffold a minimal Python REST API project called `hierarchy-probe` with:
1. A single `GET /health` endpoint (FastAPI or Flask, your choice)
2. A unit test for the health endpoint
3. A `Dockerfile` with a multi-stage build
4. A `README.md` documenting local setup

**Constraints:**
- Use strict tests-first discipline
- Each delegation must be named when it happens (e.g., "Delegating to Prometheus for planning…")
- Do not skip any of the six delegation phases listed below

**Required layer crossings (measure each):**

### Crossing 1 — L0 → L1: Atlas → Prometheus (Planning)
Atlas must delegate research + planning to Prometheus.
Prometheus must invoke the Specify pipeline (SpecifySpec → SpecifyPlan → SpecifyTasks).
Expected: SpecifySpec, SpecifyPlan, and SpecifyTasks are all invoked as L1→L2 sub-delegations.

### Crossing 2 — L0 → L1: Atlas → Sisyphus (Implementation)
Atlas must delegate implementation to Sisyphus.
Sisyphus must route the backend API work to Backend-Atlas (L1→L2).
Backend-Atlas must invoke at least one specialist (API-Designer or Service-Builder).
Expected: Backend-Atlas is invoked — NOT directly by Atlas.

### Crossing 3 — L0 → L1: Atlas → Themis (Code Review)
After implementation, Atlas must delegate code review to Themis.
Themis performs a review pass and reports findings.

### Crossing 4 — L0 → L1: Atlas → Hephaestus (Docker build + DevOps)
Atlas must delegate Dockerfile validation and build test to Hephaestus.
Hephaestus must route to DevOps-Atlas (L1→L2).
Expected: DevOps-Atlas is invoked — NOT directly by Atlas.

### Crossing 5 — L0 → L1: Atlas → Argus (QA Gate)
Atlas must invoke Argus as the QA gate before declaring work complete.
Argus runs the unit test and reports coverage.

### Crossing 6 — L0 → L1: Atlas → Hermes (Documentation)
Atlas must delegate README.md creation to Hermes.

**After all delegations complete:**
- Print a delegation trace: list every agent that was invoked and at which layer.
- Flag any agent invocation that violated the hierarchy (e.g., Atlas invoking a L2 agent directly).
- Return HIERARCHY_VALID: true or HIERARCHY_VALID: false with a reason.
```

---

## What to Observe

When running this prompt, verify:

1. **Atlas's narration** explicitly names each delegation and the target agent.
2. **Prometheus** spawns SpecifySpec, SpecifyPlan, and SpecifyTasks as sub-agents.
3. **Sisyphus** spawns Backend-Atlas, NOT API-Designer directly.
4. **Hephaestus** spawns DevOps-Atlas, NOT Container-Master directly.
5. **No L2 agent** is invoked directly by Atlas.
6. The final delegation trace includes at least 6 L0→L1 crossings and at least 4 L1→L2 crossings.

## Passing Criteria

- 6/6 delegation phases completed with correct layer routing.
- `HIERARCHY_VALID: true` in the final report.
- No direct L0→L2 invocation in the trace.
