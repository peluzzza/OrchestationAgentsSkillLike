## Phase 2 Complete: Align runtime README surfaces
The runtime-facing README surfaces now match the current `stable-runtime-v1` truth. The root `README.md` and the atlas-pack metadata README both distinguish the mandatory stable core from the optional validated utility lanes and document the inherited-session / required-trace behavior without overstating runtime guarantees.

**Files:** `README.md`, `plugins/atlas-orchestration-team/README.md`
**Functions:** none
**Implementation Scope:** Split runtime docs into stable core vs optional validated utility lanes, added lightweight session/trace wording for `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS`, updated validation guidance, and replaced stale troubleshooting guidance about `agents: ["*"]` with the real specialist list.
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: N/A
- Additional tests: 0
- Edge cases: Documentation was reviewed against runtime-contract comments and validator behavior instead of running behavior tests

**Deployment (Hephaestus):** N/A
- Env: N/A
- Services: N/A
- Health: N/A
- Notes: Documentation-only phase

**Git Commit:**
docs: align atlas runtime readmes

- split stable core and optional runtime lanes
- refresh validation and troubleshooting guidance
