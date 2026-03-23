"""
Test suite para full_team_harness.py

Clases:
  TestHarnessUnit    — logica interna pura (Check, Suite, validaciones temporales)
  TestAgentRoster    — verifica los 26 agentes instalados globalmente (siempre activo)
  TestPackRegistry   — verifica pack-registry.json real (siempre activo)
  TestSpecifyArtifacts  — SKIP si pipeline no ejecutado
  TestImplementation    — SKIP si stats() no implementado
  TestDocsUpdated       — SKIP si README sin API Reference
  TestDepsAudited       — SKIP si no hay reporte de Ariadna

Ejecucion:
    cd demos/full-atlas-team-demo
    py -m unittest -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import full_team_harness as harness

WORKSPACE = Path(__file__).resolve().parent.parent.parent
DEMO_DIR  = WORKSPACE / "demos" / "full-atlas-team-demo"


# ── TestHarnessUnit ───────────────────────────────────────────────────────────

class TestHarnessUnit(unittest.TestCase):

    def test_check_pass(self):
        c = harness.Check("x", True)
        self.assertTrue(c.passed)
        self.assertEqual(c.detail, "")

    def test_check_fail(self):
        c = harness.Check("x", False, "razon")
        self.assertFalse(c.passed)

    def test_suite_all_pass(self):
        s = harness.Suite("S", [harness.Check("a", True), harness.Check("b", True)])
        self.assertTrue(s.passed)
        self.assertEqual(s.failures, [])

    def test_suite_with_failure(self):
        s = harness.Suite("S", [harness.Check("a", True), harness.Check("b", False)])
        self.assertFalse(s.passed)
        self.assertEqual(len(s.failures), 1)

    def test_implementation_no_stats(self):
        """task_service sin stats() debe fallar el check de implementacion."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "demos" / "full-atlas-team-demo"
            d.mkdir(parents=True)
            (d / "task_service.py").write_text("class TaskService: pass", encoding="utf-8")
            suite = harness.check_implementation(d)
            failed = [c.name for c in suite.checks if not c.passed]
            self.assertTrue(any("stats()" in n for n in failed))

    def test_implementation_not_implemented_error(self):
        """stats() con NotImplementedError aun debe fallar."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "demos" / "full-atlas-team-demo"
            d.mkdir(parents=True)
            code = "class TaskService:\n    def stats(self):\n        raise NotImplementedError\n"
            (d / "task_service.py").write_text(code, encoding="utf-8")
            suite = harness.check_implementation(d)
            failed_names = [c.name for c in suite.checks if not c.passed]
            self.assertTrue(any("NotImplementedError" in n for n in failed_names))

    def test_docs_missing_api_reference(self):
        """README sin API Reference debe fallar el check de Clio."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "demos" / "full-atlas-team-demo"
            d.mkdir(parents=True)
            (d / "README.md").write_text("# Demo\nSin API Reference aqui.", encoding="utf-8")
            suite = harness.check_docs(d)
            failed = [c for c in suite.checks if not c.passed]
            # El check falla cuando API Reference no esta en el README
            self.assertTrue(len(failed) > 0, "Deberia haber al menos un fallo")
            self.assertTrue(
                any("Reference" in c.name or "stats" in c.name for c in failed),
                f"Checks fallidos: {[c.name for c in failed]}"
            )

    def test_pack_registry_bad_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            plugin_dir = d / ".github" / "plugin"
            plugin_dir.mkdir(parents=True)
            (plugin_dir / "pack-registry.json").write_text("{bad", encoding="utf-8")
            suite = harness.check_pack_registry(d)
            self.assertFalse(suite.passed)

    def test_specify_dir_missing_returns_gracefully(self):
        with tempfile.TemporaryDirectory() as tmp:
            suite = harness.check_specify_artifacts(Path(tmp))
            self.assertIsInstance(suite, harness.Suite)
            self.assertGreater(len(suite.checks), 0)

    def test_print_report_true(self):
        ok = harness.print_report([harness.Suite("S", [harness.Check("c", True)])])
        self.assertTrue(ok)

    def test_print_report_false(self):
        ok = harness.print_report([harness.Suite("S", [harness.Check("c", False, "err")])])
        self.assertFalse(ok)


# ── TestAgentRoster — siempre activo ─────────────────────────────────────────

class TestAgentRoster(unittest.TestCase):
    """
    Verifica que los 26 agentes estan instalados globalmente.
    Debe pasar SIEMPRE (pre y post demo).
    Para instalar: scripts/install-agents-user-level.ps1 -Force
    """

    def setUp(self):
        self.result = harness.check_agent_roster()

    def _get(self, substring):
        return next((c for c in self.result.checks if substring in c.name), None)

    def test_prompts_dir_exists(self):
        c = self._get("global de prompts")
        self.assertIsNotNone(c)
        self.assertTrue(c.passed, f"Directorio no encontrado: {c.detail}\n"
                        "Ejecuta: scripts\\install-agents-user-level.ps1 -Force")

    def test_atlas_installed(self):
        c = self._get("Atlas.agent.md")
        self.assertIsNotNone(c)
        self.assertTrue(c.passed, c.detail)

    def test_prometheus_installed(self):
        c = self._get("Prometheus.agent.md")
        self.assertIsNotNone(c)
        self.assertTrue(c.passed, c.detail)

    def test_all_specify_agents_installed(self):
        specify = [c for c in self.result.checks if "Specify" in c.name]
        self.assertGreaterEqual(len(specify), 7, "Deberia haber 7 agentes Specify")
        missing = [c for c in specify if not c.passed]
        self.assertEqual(len(missing), 0,
                         f"Agentes Specify faltantes: {[c.name for c in missing]}")

    def test_all_core_agents_installed(self):
        # Afrodita se instala como Afrodita-UX.agent.md (no Afrodita.agent.md)
        core = ["Hermes", "Oracle", "Sisyphus", "Themis", "Argus",
                "Atenea", "Clio", "Ariadna", "Hephaestus", "Afrodita-UX"]
        for name in core:
            c = self._get(f"{name}.agent.md")
            self.assertIsNotNone(c, f"Check para {name}.agent.md no encontrado")
            self.assertTrue(c.passed, f"{name}.agent.md no instalado: {c.detail if c else ''}")

    def test_atlas_has_wildcard_agents(self):
        c = self._get('agents: ["*"]')
        self.assertIsNotNone(c, "Check de agents:[*] no encontrado")
        self.assertTrue(c.passed, c.detail if c else "")

    def test_atlas_reads_pack_registry(self):
        c = self._get("pack-registry.json")
        self.assertIsNotNone(c, "Check de pack-registry no encontrado")
        self.assertTrue(c.passed, c.detail if c else "")

    def test_atlas_has_sp5_gate(self):
        c = self._get("SP-5 gate")
        self.assertIsNotNone(c, "Check de SP-5 no encontrado")
        self.assertTrue(c.passed, c.detail if c else "")

    def test_atlas_has_ex1_gate(self):
        c = self._get("EX-1 gate")
        self.assertIsNotNone(c, "Check de EX-1 no encontrado")
        self.assertTrue(c.passed, c.detail if c else "")

    def test_hephaestus_brief_has_5_modes(self):
        c = self._get("5 modos")
        self.assertIsNotNone(c, "Check de 5 modos Hephaestus no encontrado")
        self.assertTrue(c.passed, c.detail if c else "")


# ── TestPackRegistry — siempre activo ────────────────────────────────────────

class TestPackRegistry(unittest.TestCase):

    def setUp(self):
        self.result = harness.check_pack_registry(WORKSPACE)

    def _get(self, sub):
        return next((c for c in self.result.checks if sub in c.name), None)

    def test_registry_exists(self):
        c = self._get("existe")
        self.assertIsNotNone(c)
        self.assertTrue(c.passed, c.detail)

    def test_canonical_root_default_active(self):
        c = self._get("canonical-root defaultActive")
        self.assertIsNotNone(c)
        self.assertTrue(c.passed, c.detail)

    def test_domain_packs_shipped(self):
        for pid in ["backend-workflow", "frontend-workflow", "automation-mcp-workflow"]:
            c = self._get(f"{pid} shipped")
            self.assertIsNotNone(c, f"Check not found for {pid}")
            self.assertTrue(c.passed, c.detail)


# ── TestSpecifyArtifacts — SKIP pre-demo ──────────────────────────────────────

class TestSpecifyArtifacts(unittest.TestCase):

    SLUG = "task-stats"

    def setUp(self):
        feature_dir = DEMO_DIR / ".specify" / "specs" / self.SLUG
        if not feature_dir.exists():
            self.skipTest(
                f"Pipeline Specify no ejecutado — {feature_dir} no existe.\n"
                "Ejecuta la Opcion A o B de DEMO_PROMPT.md con @Atlas primero."
            )
        self.result = harness.check_specify_artifacts(DEMO_DIR, self.SLUG)

    def _get(self, sub):
        return next((c for c in self.result.checks if sub in c.name), None)

    def test_spec_exists(self):
        c = self._get("spec.md existe")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_plan_exists(self):
        c = self._get("plan.md existe")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_tasks_has_minimum_ids(self):
        c = self._get("al menos 5 tareas")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_analysis_report_exists(self):
        c = self._get("analysis-report.md existe")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_analysis_report_mentions_gate(self):
        c = self._get("SP-5 o EX-1")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)


# ── TestImplementation — SKIP pre-demo ───────────────────────────────────────

class TestImplementation(unittest.TestCase):

    def setUp(self):
        service = DEMO_DIR / "task_service.py"
        if not service.exists():
            self.skipTest("task_service.py no encontrado")
        import re as _re
        content = service.read_text(encoding="utf-8")
        has_stats_def = bool(_re.search(r"def\s+stats\s*\(", content))
        has_not_impl = bool(_re.search(r"raise\s+NotImplementedError", content))
        if not has_stats_def or has_not_impl:
            self.skipTest(
                "stats() no implementado aun — ejecuta la demo con @Atlas primero."
            )
        self.result = harness.check_implementation(DEMO_DIR)

    def _get(self, sub):
        return next((c for c in self.result.checks if sub in c.name), None)

    def test_stats_implemented(self):
        c = self._get("stats() esta definido")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_stats_not_stub(self):
        c = self._get("NotImplementedError")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_limit_validation(self):
        c = self._get("valida el parametro limit")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_test_file_exists(self):
        c = self._get("test_task_stats.py existe")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_sufficient_test_count(self):
        c = self._get("al menos 5 tests")
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)


# ── TestDocsUpdated — SKIP pre-demo ──────────────────────────────────────────

class TestDocsUpdated(unittest.TestCase):

    def setUp(self):
        readme = DEMO_DIR / "README.md"
        if not readme.exists():
            self.skipTest("README.md no encontrado")
        content = readme.read_text(encoding="utf-8")
        if "API Reference" not in content and "api reference" not in content.lower():
            self.skipTest("README sin API Reference — ejecuta la demo para que Clio lo actualice.")
        self.result = harness.check_docs(DEMO_DIR)

    def test_api_reference_present(self):
        c = next((x for x in self.result.checks if "API Reference" in x.name), None)
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)

    def test_stats_documented(self):
        c = next((x for x in self.result.checks if "stats()" in x.name), None)
        self.assertIsNotNone(c); self.assertTrue(c.passed, c.detail)


if __name__ == "__main__":
    unittest.main(verbosity=2)
